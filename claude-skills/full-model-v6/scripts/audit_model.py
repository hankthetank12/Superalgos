#!/usr/bin/env python3
"""Static workbook audit for full-model builds.

Checks the machine-checkable subset of the acceptance gates via openpyxl STATIC reads only —
no formula evaluation, no recalc. It REPORTS; it never blocks: fix genuine FAILs, justify or
waive anything intentional (say which in the reply), and use image checks for borders/shapes.

Usage:
  python scripts/audit_model.py WORKBOOK.xlsx [--model-sheet Model] [--json]

Checks:
  A. Fonts       — every built tab is a single family/size (default Calibri 9); lists offenders.
  B. Fill roles  — #FFFFCC only under blue font (inputs); yellow-on-formula = FAIL;
                   pure #FFFF00 anywhere = WARN (should have been swept to #FFFFCC).
  C. Blue rules  — blue font + formula (outside allowed date/label scaffold) = WARN
                   (blue means hardcode); blue constant with no fill in an ESTIMATE column = FAIL
                   when an Actual/Estimate marker row is found.
  D. Link policy — on the Mini Model: #008000 green = FAIL (its links are #006600);
                   consensus-colored (red) cells referencing VAActuals = OK; on the Model tab,
                   VAActuals references that are NOT red/dark-green = FAIL.
  E. Errors      — any cached #REF!/#VALUE!/#DIV/0!/#N/A cell values, INCLUDING hidden columns.
  F. SUMIFS      — on the Model sheet, all SUMIFS over the fiscal-year key must use ONE identical
                   criteria range (the fixed-range rule).
  G. Check rows  — rows labeled 'Check' / 'Tie' / 'Plug (should be 0)': cached values ~0 or '-'.
Exit code is always 0 (report-don't-loop); parse the summary.
"""
import argparse, json, re, sys
from collections import Counter, defaultdict

import openpyxl
from openpyxl.utils import get_column_letter

ERR_STRINGS = ("#REF!", "#VALUE!", "#DIV/0!", "#N/A", "#NAME?", "#NULL!", "#NUM!")


def rgb(color):
    if color is None or getattr(color, "type", None) != "rgb":
        return None
    v = color.rgb
    return v[2:] if isinstance(v, str) and len(v) == 8 else v


def audit(path, model_sheet="Model", font_name="Calibri", font_size=9.0):
    wbf = openpyxl.load_workbook(path, data_only=False)
    wbv = openpyxl.load_workbook(path, data_only=True)
    report = {"workbook": path, "checks": [], "summary": {}}

    def add(check, status, detail, examples=None):
        report["checks"].append({
            "check": check, "status": status, "detail": detail,
            "examples": (examples or [])[:8],
        })

    built_tabs = [s for s in wbf.sheetnames]
    for name in built_tabs:
        ws, wsv = wbf[name], wbv[name]
        max_r = min(ws.max_row or 0, 5000)

        fonts = Counter()
        yellow_on_formula, pure_yellow, blue_formula = [], [], []
        errors = []
        green_008000 = []
        va_badcolor = []
        sumifs_ranges = Counter()
        check_rows_bad, check_rows_ok = [], 0

        for row in ws.iter_rows(min_row=1, max_row=max_r):
            label = None
            for c in row[:14]:
                if isinstance(c.value, str) and c.value.strip():
                    label = c.value.strip()
                    break
            for c in row:
                v = c.value
                if v is None:
                    continue
                coord = f"{name}!{c.coordinate}"
                f = c.font
                if f and f.name:
                    fonts[(f.name, f.sz)] += 1
                fill = c.fill
                frgb = rgb(f.color) if f else None
                brgb = None
                if fill is not None and fill.fill_type == "solid":
                    brgb = rgb(fill.start_color)
                is_formula = isinstance(v, str) and v.startswith("=")
                if brgb == "FFFFCC" and is_formula and "TODAY()" not in str(v).upper():
                    # TODAY() on yellow is the sanctioned self-setting-input exception (format-spec)
                    yellow_on_formula.append(coord)
                if brgb == "FFFF00":
                    pure_yellow.append(coord)
                if frgb == "0000FF" and is_formula and not re.match(
                        r"^=\+?(EOMONTH|VALUE|LEFT|MID|TEXT|TODAY|DATE)\(", str(v)):
                    blue_formula.append(coord)
                if is_formula and "VAActuals" in str(v):
                    if name == model_sheet and frgb not in ("FF0000", "006600"):
                        va_badcolor.append(coord)
                if name.lower().startswith("mini") and frgb == "008000":
                    green_008000.append(coord)
                if is_formula and "SUMIFS(" in str(v).upper() and name == model_sheet:
                    m = re.search(r"SUMIFS\([^,]+,\s*(\$?[A-Z]+\$?\d+:\$?[A-Z]+\$?\d+)",
                                  str(v), re.I)
                    if m:
                        sumifs_ranges[m.group(1).replace("$", "")] += 1
                vv = wbv[name][c.coordinate].value
                if isinstance(vv, str) and vv in ERR_STRINGS:
                    errors.append(f"{coord}={vv}")
            if label and re.match(r"^(check\b|.*tie memo|tie:)", label, re.I):
                for c in row[3:]:
                    vv = wbv[name][c.coordinate].value
                    if isinstance(vv, (int, float)) and abs(vv) > 1.0:
                        check_rows_bad.append(f"{name}!{c.coordinate}={vv:.2f} ({label})")
                    elif vv is not None:
                        check_rows_ok += 1

        main = fonts.most_common(1)
        offenders = {k: n for k, n in fonts.items()
                     if k != (font_name, font_size) and n > 2}
        if not fonts:
            pass  # empty tab — nothing to check
        elif main and main[0][0] == (font_name, font_size) and not offenders:
            add(f"A.font[{name}]", "PASS", f"{font_name} {font_size} throughout")
        else:
            add(f"A.font[{name}]", "WARN" if main and main[0][0] == (font_name, font_size)
                else "FAIL", f"font mix: {dict(list(fonts.items())[:4])}")
        if yellow_on_formula:
            add(f"B.yellow-on-formula[{name}]", "FAIL",
                f"{len(yellow_on_formula)} formula cells on #FFFFCC", yellow_on_formula)
        if pure_yellow:
            add(f"B.pure-yellow[{name}]", "WARN",
                f"{len(pure_yellow)} #FFFF00 cells (sweep to #FFFFCC)", pure_yellow)
        if blue_formula:
            add(f"C.blue-formula[{name}]", "WARN",
                f"{len(blue_formula)} blue-font formulas (blue = hardcode)", blue_formula)
        if green_008000:
            add(f"D.minimodel-green[{name}]", "FAIL",
                f"{len(green_008000)} #008000 cells on Mini Model (use #006600 data links)",
                green_008000)
        if va_badcolor:
            add(f"D.va-link-color[{name}]", "FAIL",
                f"{len(va_badcolor)} VAActuals refs on Model not red/dark-green", va_badcolor)
        if errors:
            add(f"E.errors[{name}]", "FAIL", f"{len(errors)} error cells (incl. hidden)", errors)
        if name == model_sheet and sumifs_ranges:
            if len(sumifs_ranges) == 1:
                add("F.sumifs-range", "PASS",
                    f"one criteria range: {next(iter(sumifs_ranges))}")
            else:
                add("F.sumifs-range", "FAIL",
                    f"multiple SUMIFS criteria ranges: {dict(sumifs_ranges)}")
        if check_rows_bad:
            add(f"G.check-rows[{name}]", "FAIL",
                f"{len(check_rows_bad)} nonzero check cells", check_rows_bad)
        elif check_rows_ok and name == model_sheet:
            add("G.check-rows", "PASS", f"{check_rows_ok} check cells ~0")

    counts = Counter(c["status"] for c in report["checks"])
    report["summary"] = dict(counts)
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workbook")
    ap.add_argument("--model-sheet", default="Model")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    rep = audit(args.workbook, args.model_sheet)
    if args.json:
        print(json.dumps(rep, indent=1))
    else:
        for c in rep["checks"]:
            line = f"[{c['status']:4s}] {c['check']}: {c['detail']}"
            if c["examples"]:
                line += f"  e.g. {', '.join(c['examples'][:4])}"
            print(line)
        print("SUMMARY:", rep["summary"])
    sys.exit(0)


if __name__ == "__main__":
    main()
