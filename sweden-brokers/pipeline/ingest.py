#!/usr/bin/env python3
"""Ingest Walleye Data Science "Sweden Retail Brokers" workbook dumps into data/daily.csv.

Input format (what the Microsoft 365 connector returns when it reads the .xlsx attachment):

    === Sheet: Downloads Daily ===
    date<TAB>Avanza - Total<TAB>IBKR - Sweden<TAB>...
    44562<TAB>1339<TAB>8<TAB><TAB>147<TAB>435<TAB><TAB>3
    ...
    [truncated: 3 of 4 sheets included]

Dates are Excel serials. A blank cell means "not reported". Rows may be shorter than the
header when trailing cells are blank.

Merge rule (newest vintage wins, cell by cell): every non-blank cell in a newer dump
replaces the stored value for that (metric, broker, date). A blank never overwrites a
value, so a broker that lags in SensorTower keeps its last reported figure until the
provider fills it in. Re-ingesting the same dump is a no-op.

Usage:
    python3 ingest.py data/raw/dump_2026-09-01.tsv data/raw/dump_2026-09-07.tsv
Dump files must be named dump_YYYY-MM-DD.tsv (the email date is the vintage). An optional
sidecar dump_YYYY-MM-DD.meta.json (message id, subject, ...) is recorded in vintages.json.
"""
import csv, json, os, re, sys, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
DAILY = os.path.join(DATA, "daily.csv")
VINTAGES = os.path.join(DATA, "vintages.json")

# sheet name -> metric id(s). Web uniques carry the metric in the column suffix.
SHEETS = {
    "Downloads Daily": {"metric": "downloads"},
    "DAU Daily": {"metric": "dau"},
    "Web Uniques Daily": {"metric": None},  # per-column
}
COLUMN_SUFFIX = {
    " - Total": None, " - Sweden": None,          # scope suffixes on app metrics
    " - Desktop Uniques": "web_desktop", " - Mobile Web Uniques": "web_mobile",
}


def excel_serial(n):
    return (dt.date(1899, 12, 30) + dt.timedelta(days=int(float(n)))).isoformat()


def split_column(col, default_metric):
    """'Avanza - Total' -> ('Avanza', 'downloads'); 'Nordnet - Desktop Uniques' -> ('Nordnet','web_desktop')."""
    for suffix, metric in COLUMN_SUFFIX.items():
        if col.endswith(suffix):
            return col[: -len(suffix)].strip(), (metric or default_metric)
    return col.strip(), default_metric


def parse_dump(path):
    """Return ({(metric, broker, date): value}, sheet_report, truncation_note)."""
    cells, report, note = {}, {}, None
    cur, hdr = None, None
    with open(path, encoding="utf-8") as fh:
        for raw in fh.read().split("\n"):
            m = re.match(r"=== Sheet: (.*) ===", raw)
            if m:
                cur, hdr = m.group(1), None
                report[cur] = {"rows": 0, "first": None, "last": None, "known": cur in SHEETS}
                continue
            if raw.startswith("[truncated"):
                note = raw.strip("[]")
                continue
            if cur is None or not raw.strip():
                continue
            parts = raw.split("\t")
            if hdr is None:
                hdr = parts
                continue
            if cur not in SHEETS:
                report[cur]["rows"] += 1
                continue
            try:
                date = excel_serial(parts[0])
            except ValueError:
                continue  # a stray non-data row
            rep = report[cur]
            rep["rows"] += 1
            rep["first"] = rep["first"] or date
            rep["last"] = date
            default_metric = SHEETS[cur]["metric"]
            for i, col in enumerate(hdr[1:], start=1):
                v = parts[i].strip() if i < len(parts) else ""
                if v == "":
                    continue
                broker, metric = split_column(col, default_metric)
                cells[(metric, broker, date)] = float(v)
    return cells, report, note


def load_daily():
    rows = {}
    if os.path.exists(DAILY):
        with open(DAILY, newline="") as fh:
            for r in csv.DictReader(fh):
                rows[(r["metric"], r["broker"], r["date"])] = (float(r["value"]), r["vintage"])
    return rows


def save_daily(rows):
    tmp = DAILY + ".tmp"
    with open(tmp, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["date", "metric", "broker", "value", "vintage"])
        for (metric, broker, date) in sorted(rows, key=lambda k: (k[0], k[2], k[1])):
            v, vint = rows[(metric, broker, date)]
            w.writerow([date, metric, broker, ("%d" % v) if v == int(v) else repr(v), vint])
    os.replace(tmp, DAILY)


def load_vintages():
    if os.path.exists(VINTAGES):
        return json.load(open(VINTAGES))
    return {"vintages": []}


def ingest(paths):
    rows = load_daily()
    vint = load_vintages()
    done = {v["email_date"] for v in vint["vintages"]}
    # oldest first so "newest wins" holds regardless of argument order
    for path in sorted(paths, key=os.path.basename):
        m = re.search(r"dump_(\d{4}-\d{2}-\d{2})\.tsv$", os.path.basename(path))
        if not m:
            print(f"skip {path}: name must be dump_YYYY-MM-DD.tsv", file=sys.stderr)
            continue
        email_date = m.group(1)
        cells, report, note = parse_dump(path)
        added = changed = kept = 0
        for key, v in cells.items():
            old = rows.get(key)
            if old is None:
                rows[key] = (v, email_date); added += 1
            elif abs(old[0] - v) > 1e-9:
                if email_date >= old[1]:
                    rows[key] = (v, email_date); changed += 1
                else:
                    kept += 1  # an older dump re-ingested after a newer one: newer value stands
        meta_path = path[:-4] + ".meta.json"
        meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
        entry = {"email_date": email_date, "dump_file": os.path.relpath(path, ROOT), "sheets": report,
                 "truncation": note, "cells_added": added, "cells_changed": changed, "cells_kept_newer": kept,
                 "ingested_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), **meta}
        prior = next((v for v in vint["vintages"] if v["email_date"] == email_date), None)
        if prior is not None:  # a re-ingest is a no-op on the data; keep the first ingest's counts
            entry.update({k: prior[k] for k in ("cells_added", "cells_changed", "cells_kept_newer", "ingested_at") if k in prior})
            entry["reingested_at"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        vint["vintages"] = [v for v in vint["vintages"] if v["email_date"] != email_date] + [entry]
        status = "re-ingested" if prior is not None else "ingested"
        print(f"{status} {os.path.basename(path)}: +{added} cells, {changed} restated, {kept} kept (newer vintage present); {note or 'complete'}")
    vint["vintages"].sort(key=lambda v: v["email_date"])
    save_daily(rows)
    json.dump(vint, open(VINTAGES, "w"), indent=1)
    return rows


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        raw = os.path.join(DATA, "raw")
        args = [os.path.join(raw, f) for f in os.listdir(raw) if f.endswith(".tsv")]
    ingest(args)
