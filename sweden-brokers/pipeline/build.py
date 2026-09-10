#!/usr/bin/env python3
"""Aggregate data/daily.csv to weekly + monthly series and render dashboard.html.

Weekly periods end on Sunday (matching the relay email's "Week Ending" convention).
Each period carries, per broker, the mean of the reported daily values and the number of
days with data (coverage). A period is "complete" when its last day is on or before the
metric's data-through date. Shares, deltas and YoY are computed client-side so the
comp-set filter can re-slice everything without a rebuild.

Outputs: dashboard/data.json (the payload) and dashboard.html (template + payload).
"""
import csv, json, os, datetime as dt
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")

BROKERS = [  # fixed categorical slot order = legend order = stack order (never re-ranked)
    {"id": "Avanza", "slot": 1, "scope": "Total company (in practice ~all Sweden)", "ticker": "AZA SS"},
    {"id": "Nordnet", "slot": 2, "scope": "Sweden only", "ticker": "SAVE SS"},
    {"id": "Revolut", "slot": 3, "scope": "Sweden only · the whole Revolut app, not a trading app", "ticker": "private"},
    {"id": "IBKR", "slot": 4, "scope": "Sweden only · IBKR Mobile + GlobalTrader", "ticker": "IBKR US"},
    {"id": "Montrose", "slot": 5, "scope": "Total company · downloads and web only (below SensorTower's usage-panel threshold)", "ticker": "private"},
    {"id": "Trade Republic", "slot": 6, "scope": "Sweden only", "ticker": "private"},
    {"id": "Robinhood", "slot": 7, "scope": "Sweden only", "ticker": "HOOD US"},
]
METRICS = {
    "downloads": {"label": "App downloads", "short": "Downloads", "unit": "downloads per day", "source": "SensorTower, iOS + Android"},
    "dau": {"label": "App daily active users", "short": "DAU", "unit": "daily active users", "source": "SensorTower, iOS + Android"},
    "web_desktop": {"label": "Desktop web unique visitors", "short": "Desktop web", "unit": "unique visitors per day", "source": "SimilarWeb, worldwide panel"},
    "web_mobile": {"label": "Mobile web unique visitors", "short": "Mobile web", "unit": "unique visitors per day", "source": "SimilarWeb, worldwide panel"},
}


def week_end(d):  # Sunday on/after d
    return d + dt.timedelta(days=6 - d.weekday())


def month_end(d):
    nxt = (d.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
    return nxt - dt.timedelta(days=1)


def aggregate(rows, keyfn):
    """rows: list of (date, metric, broker, value). Returns {metric: {period: {broker: [sum, n]}}}."""
    acc = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [0.0, 0])))
    for d, m, b, v in rows:
        cell = acc[m][keyfn(d).isoformat()][b]
        cell[0] += v; cell[1] += 1
    return acc


def series_block(acc_m, through, period_days):
    periods = sorted(acc_m)
    brokers = [b["id"] for b in BROKERS]
    out = {"periods": periods, "complete": [], "days": [], "series": {}, "coverage": {}}
    for p in periods:
        pe = dt.date.fromisoformat(p)
        out["complete"].append(pe <= through)
        out["days"].append(period_days(pe))
    for b in brokers:
        vals, cov = [], []
        for p in periods:
            s, n = acc_m[p].get(b, [0.0, 0])
            vals.append(round(s / n, 3) if n else None)
            cov.append(n)
        if any(v is not None for v in vals):
            out["series"][b] = vals
            out["coverage"][b] = cov
    return out


def build():
    rows = []
    with open(os.path.join(DATA, "daily.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            rows.append((dt.date.fromisoformat(r["date"]), r["metric"], r["broker"], float(r["value"])))
    through = {}
    for d, m, b, v in rows:
        through[m] = max(through.get(m, d), d)
    weekly = aggregate(rows, week_end)
    monthly = aggregate(rows, lambda d: month_end(d))
    payload = {
        "generated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "brokers": BROKERS,
        "metrics": METRICS,
        "data_through": {m: through[m].isoformat() for m in sorted(through)},
        "vintages": json.load(open(os.path.join(DATA, "vintages.json")))["vintages"],
        "weekly": {m: series_block(weekly[m], through[m], lambda pe: 7) for m in weekly},
        "monthly": {m: series_block(monthly[m], through[m], lambda pe: pe.day) for m in monthly},
    }
    # keep only the fields of vintages the page needs
    payload["vintages"] = [
        {k: v.get(k) for k in ("email_date", "subject", "received", "attachment", "truncation", "cells_added", "cells_changed", "web_link")}
        for v in payload["vintages"]
    ]
    os.makedirs(os.path.join(ROOT, "dashboard"), exist_ok=True)
    with open(os.path.join(ROOT, "dashboard", "data.json"), "w") as fh:
        json.dump(payload, fh, separators=(",", ":"))
    tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    html = tpl.replace("/*__DATA__*/null", json.dumps(payload, separators=(",", ":")))
    with open(os.path.join(ROOT, "dashboard.html"), "w", encoding="utf-8") as fh:
        fh.write(html)
    # Standalone copy for the Dashboards hub / Kit: same page with an explicit doctype and head so a
    # browser opens it in standards mode when it is a plain file rather than an artifact.
    os.makedirs(os.path.join(ROOT, "hub"), exist_ok=True)
    # The data goes in as base64 gzip (page inflates it with DecompressionStream) so the file stays
    # small enough to pass through the SharePoint upload tool in one call.
    import gzip, base64, io
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as gz:
        gz.write(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    packed = json.dumps(base64.b64encode(buf.getvalue()).decode("ascii"))
    standalone = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                  '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                  + tpl.replace("/*__DATA__*/null", packed) + '\n</html>\n')
    with open(os.path.join(ROOT, "hub", "Sweden Retail Brokers.html"), "w", encoding="utf-8") as fh:
        fh.write(standalone)
    print(f"built dashboard.html: data through {payload['data_through']}, {len(payload['vintages'])} vintages, "
          f"{len(payload['weekly']['dau']['periods'])} weeks, {len(payload['monthly']['dau']['periods'])} months")
    return payload


if __name__ == "__main__":
    build()
