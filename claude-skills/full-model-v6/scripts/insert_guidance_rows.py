#!/usr/bin/env python3
"""
insert_guidance_rows.py  --  safely insert "Mgmt Guidance" rows into an EXISTING model.

The hazard this solves: openpyxl's ws.insert_rows() shifts cells down but does NOT rewrite
formula strings, so any formula that referenced a shifted cell -- on the model tab OR on a
downstream tab that links into it -- silently points at the wrong row. This module inserts the
rows AND repairs every affected A1 reference across the whole workbook, so the model still ties.

Programmatic API
----------------
    insert_guidance_rows(wb, sheet_name, insertions)

      wb            : an openpyxl Workbook (already loaded)
      sheet_name    : the model tab to insert into (e.g. "Model")
      insertions    : list of dicts, one per guided line:
          {
            "after_row": int,          # insert the guidance row(s) directly BELOW this row
            "label_col": int,          # column index for the "Mgmt Guidance" label
            "rows": [                   # one entry per guidance row (usually 1; >1 for vintages)
               { "label": "Mgmt Guidance",
                 "cells": { col_idx: {"value": "$12.4-12.6bn"} , ... } },  # no embedded notes — source goes in the row label
               ...
            ]
          }

    Returns: dict with "final_rows" (after_row -> [inserted row numbers]) for caller verification.

Design notes / assumptions
--------------------------
* No merged cells in the affected region (the models this targets avoid merged cells).
* Standard A1 formulas only (arithmetic, SUM/SUMIFS, cross-sheet links). INDIRECT/OFFSET and
  named ranges are NOT reference-adjusted -- if present, verify via recalc and handle manually.
* Guidance values are written as text and never feed a formula, so they cannot corrupt a range
  that happens to grow across the insertion point (SUMIFS ignores text).
* Callers MUST recalc afterwards and confirm a battery of anchor cells is unchanged (safety gate).
"""
import re
import bisect
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

VIOLET = "FF7030A0"

# One A1 reference OR range. A range's sheet qualifier sits on the HEAD ('Model'!H6:H11); the
# tail endpoint (H11) is implicitly on that same sheet even though it carries no qualifier -- so
# ranges must be matched as a unit, not token-by-token. Trailing lookahead avoids grabbing the
# digits of a token like "LOG10(" or "R2D2".
_REF_RE = re.compile(
    r"(?P<s1>(?:'(?:[^']|'')+'|[A-Za-z_][A-Za-z0-9_.]*)!)?"
    r"(?P<c1>\$?[A-Za-z]{1,3})(?P<r1>\$?[0-9]{1,7})"
    r"(?:"
    r":"
    r"(?P<s2>(?:'(?:[^']|'')+'|[A-Za-z_][A-Za-z0-9_.]*)!)?"
    r"(?P<c2>\$?[A-Za-z]{1,3})(?P<r2>\$?[0-9]{1,7})"
    r")?"
    r"(?![A-Za-z0-9_(])"
)


def _split_out_strings(formula):
    """Yield (segment, is_string_literal) so we never rewrite refs that live inside "..." text."""
    out, i, n = [], 0, len(formula)
    while i < n:
        if formula[i] == '"':
            j = i + 1
            while j < n:
                if formula[j] == '"':
                    if j + 1 < n and formula[j + 1] == '"':   # escaped "" inside a string
                        j += 2
                        continue
                    j += 1
                    break
                j += 1
            out.append((formula[i:j], True))
            i = j
        else:
            j = i
            while j < n and formula[j] != '"':
                j += 1
            out.append((formula[i:j], False))
            i = j
    return out


def _norm_sheet(q):
    """'Model'! or Model! -> 'model' (lowercased, unquoted) ; None -> None."""
    if not q:
        return None
    name = q[:-1]                      # drop trailing '!'
    if name.startswith("'") and name.endswith("'"):
        name = name[1:-1].replace("''", "'")
    return name.lower()


def _make_repair(sheet_name, insert_points):
    """insert_points: sorted list of (pos, amount). Returns a formula-string repair function.

    shift(rr) = total rows inserted at a position <= rr  (a ref to original row rr moves down that many).
    An unqualified ref belongs to the sheet the formula lives on; a qualified ref belongs to its sheet.
    """
    pts = sorted(insert_points)
    positions = [p for p, _ in pts]
    cum = []
    run = 0
    for _, amt in pts:
        run += amt
        cum.append(run)

    def shift(rr):
        k = bisect.bisect_right(positions, rr)   # how many insertion positions are <= rr
        return cum[k - 1] if k > 0 else 0

    tgt = sheet_name.lower()

    def repair(formula, home_sheet):
        if not isinstance(formula, str) or not formula.startswith("="):
            return formula
        home = home_sheet.lower()

        def _adj(row_tok, sheet_for):
            if sheet_for != tgt:
                return row_tok
            dollar = row_tok.startswith("$")
            rr = int(row_tok[1:] if dollar else row_tok)
            return ("$" if dollar else "") + str(rr + shift(rr))

        def _sub(m):
            s1 = _norm_sheet(m.group("s1"))
            head_sheet = s1 if s1 is not None else home
            out = (m.group("s1") or "") + m.group("c1") + _adj(m.group("r1"), head_sheet)
            if m.group("r2") is not None:                      # it's a range
                s2 = _norm_sheet(m.group("s2"))
                # tail inherits the head's qualifier when it has none of its own
                tail_sheet = s2 if s2 is not None else (s1 if s1 is not None else home)
                out += ":" + (m.group("s2") or "") + m.group("c2") + _adj(m.group("r2"), tail_sheet)
            return out

        pieces = []
        for seg, is_str in _split_out_strings(formula):
            pieces.append(seg if is_str else _REF_RE.sub(_sub, seg))
        return "".join(pieces)

    return repair, shift


def insert_guidance_rows(wb, sheet_name, insertions):
    ws = wb[sheet_name]

    # collapse to insertion points (pos = after_row + 1, amount = number of guidance rows there)
    points = {}
    for ins in insertions:
        pos = ins["after_row"] + 1
        points[pos] = points.get(pos, 0) + len(ins["rows"])
    point_list = sorted(points.items())

    repair, _ = _make_repair(sheet_name, point_list)

    # 1) physical shift: insert bottom-up so earlier (smaller) positions stay valid
    for pos, amt in sorted(point_list, reverse=True):
        ws.insert_rows(pos, amount=amt)

    # 2) repair every formula reference in the whole workbook (model tab + downstream tabs)
    for sh in wb.worksheets:
        for row in sh.iter_rows():
            for c in row:
                v = c.value
                if isinstance(v, str) and v.startswith("="):
                    c.value = repair(v, sh.title)

    # 3) write the guidance payloads at their FINAL positions
    def final_start(pos):
        return pos + sum(a for p, a in point_list if p < pos)

    final_rows = {}
    for ins in insertions:
        pos = ins["after_row"] + 1
        start = final_start(pos)
        placed = []
        for offset, rowspec in enumerate(ins["rows"]):
            r = start + offset
            placed.append(r)
            lab = ws.cell(r, ins["label_col"], rowspec.get("label", "Mgmt Guidance"))
            lab.font = Font(name="Calibri", size=9, italic=True, color=VIOLET)
            for col_idx, payload in rowspec.get("cells", {}).items():
                cell = ws.cell(r, col_idx, payload.get("value"))
                cell.font = Font(name="Calibri", size=9, italic=True, color=VIOLET)
                # Guidance cells carry NO embedded notes/comments — source is shown
                # visibly in the row label instead. "note" payloads are ignored.
        final_rows.setdefault(ins["after_row"], []).extend(placed)

    return {"final_rows": final_rows}


# ------------------------------------------------------------------ CLI (JSON spec) ----------
if __name__ == "__main__":
    import argparse, json, openpyxl
    ap = argparse.ArgumentParser(description="Insert Mgmt Guidance rows into an existing model, repairing formulas.")
    ap.add_argument("workbook")
    ap.add_argument("--sheet", default="Model")
    ap.add_argument("--spec", required=True, help="Path to a JSON file: [{after_row,label_col,rows:[{label,cells:{col:{value}}}]}]")
    ap.add_argument("--out", default=None, help="Output path (defaults to overwriting the input).")
    a = ap.parse_args()
    wb = openpyxl.load_workbook(a.workbook)
    spec = json.load(open(a.spec))
    # JSON keys are strings; coerce column indices to int
    for ins in spec:
        for r in ins["rows"]:
            r["cells"] = {int(k): v for k, v in r.get("cells", {}).items()}
    res = insert_guidance_rows(wb, a.sheet, spec)
    wb.save(a.out or a.workbook)
    print(json.dumps(res))
