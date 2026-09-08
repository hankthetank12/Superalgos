#!/usr/bin/env python3
"""Write summary.md and summary.html (Outlook-safe HTML) from dashboard/data.json.

The summary covers the latest complete week: DAU share and download share per broker
with deltas vs the prior week and the same week a year earlier, the biggest movers,
latest complete month YoY growth, and the standing caveats. Usage:

    python3 summarize.py [--dashboard-url URL]
"""
import json, os, sys, datetime as dt, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
D = json.load(open(os.path.join(ROOT, "dashboard", "data.json")))
ORDER = [b["id"] for b in D["brokers"]]
SCOPE = {b["id"]: b["scope"] for b in D["brokers"]}


def fdate(s):
    return dt.date.fromisoformat(s).strftime("%-d %b %Y")


def pct(x, d=None):
    if x is None:
        return "–"
    if d is None:
        d = 1 if abs(x) >= 0.01 else 2
    return f"{x*100:.{d}f}%"


def pp(x):
    if x is None:
        return "–"
    mag = f"{abs(x)*100:.{2 if abs(x)*100 < 0.1 else 1}f}"
    if float(mag) == 0:
        return f"{mag} pp"
    return f"{'+' if x > 0 else '−'}{mag} pp"


def yoy(x):
    if x is None:
        return "–"
    mag = round(abs(x) * 100)
    if mag == 0:
        return "0%"
    return f"{'+' if x > 0 else '−'}{mag:,.0f}%"


def num(x):
    return "–" if x is None else f"{x:,.0f}"


def complete_idx(b):
    return [i for i, c in enumerate(b["complete"]) if c]


def shares(b, i, ids):
    vals = {k: b["series"][k][i] for k in ids if b["series"][k][i] is not None}
    tot = sum(vals.values())
    return {k: (vals[k] / tot if k in vals and tot > 0 else None) for k in ids}


def block_summary(metric, gran, lag):
    b = D[gran][metric]
    ids = [k for k in ORDER if k in b["series"]]
    idx = complete_idx(b)
    i = idx[-1]
    cur, prev = shares(b, i, ids), shares(b, i - 1, ids)
    yr = shares(b, i - lag, ids) if i - lag >= 0 else {k: None for k in ids}
    rows = []
    for k in ids:
        lvl, lvl_y = b["series"][k][i], (b["series"][k][i - lag] if i - lag >= 0 else None)
        cov, days = b["coverage"][k][i], b["days"][i]
        rows.append({
            "broker": k, "share": cur[k], "coverage": cov, "days": days, "partial": cov < days,
            "d_prev": (cur[k] - prev[k]) if cur[k] is not None and prev[k] is not None else None,
            "d_year": (cur[k] - yr[k]) if cur[k] is not None and yr[k] is not None else None,
            "level": lvl, "yoy": (lvl / lvl_y - 1) if lvl and lvl_y else None,
        })
    rows.sort(key=lambda r: -(r["share"] or 0))
    return {"period": b["periods"][i], "rows": rows, "metric": metric}


def main(url=None):
    dau_w = block_summary("dau", "weekly", 52)
    dl_w = block_summary("downloads", "weekly", 52)
    dau_m = block_summary("dau", "monthly", 12)
    dl_m = block_summary("downloads", "monthly", 12)
    web_d = block_summary("web_desktop", "weekly", 52)
    web_m = block_summary("web_mobile", "weekly", 52)
    v = D["vintages"][-1]
    through = D["data_through"]

    def movers(rows, key):
        r = [x for x in rows if x[key] is not None]
        if not r:
            return None, None
        return max(r, key=lambda x: x[key]), min(r, key=lambda x: x[key])

    up_d, dn_d = movers(dau_w["rows"], "d_prev")
    up_w, dn_w = movers(dl_w["rows"], "d_prev")
    upy_d, dny_d = movers(dau_w["rows"], "d_year")
    upy_w, dny_w = movers(dl_w["rows"], "d_year")

    title = f"Sweden Retail Brokers – market share update, week ending {fdate(dau_w['period'])}"
    md, H = [], []
    md.append(f"# {title}\n")
    md.append(f"Source: Walleye Data Science relay email of {fdate(v['email_date'])} ({v.get('attachment','')}); SensorTower app data through {fdate(through['dau'])}, SimilarWeb web data through {fdate(through['web_desktop'])}.")
    if url:
        md.append(f"\nDashboard: {url}\n")
    H.append(f"<h2>{html.escape(title)}</h2>")
    H.append(f"<p>Source: Walleye Data Science relay email of {fdate(v['email_date'])} ({html.escape(v.get('attachment',''))}). SensorTower app data through {fdate(through['dau'])}; SimilarWeb web data through {fdate(through['web_desktop'])}.</p>")
    if url:
        H.append(f'<p><b>Dashboard:</b> <a href="{html.escape(url)}">{html.escape(url)}</a></p>')

    # headline bullets
    bl = []
    bl.append(f"DAU share, week ending {fdate(dau_w['period'])}: " + ", ".join(f"{r['broker']} {pct(r['share'])} ({pp(r['d_prev'])} w/w, {pp(r['d_year'])} y/y)" for r in dau_w["rows"]) + ".")
    bl.append(f"Download share, week ending {fdate(dl_w['period'])}: " + ", ".join(f"{r['broker']} {pct(r['share'])} ({pp(r['d_prev'])} w/w, {pp(r['d_year'])} y/y)" for r in dl_w["rows"]) + ".")
    if up_d and dn_d:
        s_ = f"Biggest DAU-share movers on the week: {up_d['broker']} {pp(up_d['d_prev'])}, {dn_d['broker']} {pp(dn_d['d_prev'])}."
        if upy_d and dny_d:
            s_ += f" On the year: {upy_d['broker']} {pp(upy_d['d_year'])}, {dny_d['broker']} {pp(dny_d['d_year'])}."
        bl.append(s_)
    if up_w and dn_w:
        s_ = f"Biggest download-share movers on the week: {up_w['broker']} {pp(up_w['d_prev'])}, {dn_w['broker']} {pp(dn_w['d_prev'])}."
        if upy_w and dny_w:
            s_ += f" On the year: {upy_w['broker']} {pp(upy_w['d_year'])}, {dny_w['broker']} {pp(dny_w['d_year'])}."
        bl.append(s_)

    def growth_item(r):
        # a partial month is shown with its coverage; for downloads the relay email sums the period,
        # so its y/y counts unreported days as zero and comes out lower than this average-based figure
        return f"{r['broker']} {yoy(r['yoy'])}" + (f" ({r['coverage']} of {r['days']} days)" if r["partial"] else "")
    bl.append(f"Latest complete month ({dt.date.fromisoformat(dau_m['period']).strftime('%B %Y')}) DAU growth y/y: " + ", ".join(growth_item(r) for r in dau_m["rows"]) + ". Downloads y/y: " + ", ".join(growth_item(r) for r in dl_m["rows"]) + ".")
    bl.append(f"Web (desktop uniques, week ending {fdate(web_d['period'])}, three sites only): " + ", ".join(f"{r['broker']} {pct(r['share'])} ({pp(r['d_year'])} y/y)" for r in web_d["rows"]) + ". Mobile web: " + ", ".join(f"{r['broker']} {pct(r['share'])} ({pp(r['d_year'])} y/y)" for r in web_m["rows"]) + ".")
    md.append("\n## Headlines\n")
    md += [f"- {x}" for x in bl]
    H.append("<h3>Headlines</h3><ul>" + "".join(f"<li>{html.escape(x)}</li>" for x in bl) + "</ul>")

    def table(title_, blk, unit):
        md.append(f"\n## {title_} – week ending {fdate(blk['period'])}\n")
        md.append(f"| Broker | Share | vs prior week | vs year ago | Avg per day | y/y growth |\n|---|---:|---:|---:|---:|---:|")
        rows, notes = [], []
        for r in blk["rows"]:
            name = r["broker"] + ("*" if r["partial"] else "")
            if r["partial"]:
                if blk["metric"] == "downloads":
                    notes.append(f"* {r['broker']}: averaged over the {r['coverage']} of {r['days']} days with data. The relay email sums downloads over the period, so unreported days count as zero there and its y/y is lower.")
                else:
                    notes.append(f"* {r['broker']}: averaged over the {r['coverage']} of {r['days']} days with data. The relay email averages reported days too, so its y/y matches.")
            md.append(f"| {name} | {pct(r['share'])} | {pp(r['d_prev'])} | {pp(r['d_year'])} | {num(r['level'])} | {yoy(r['yoy'])} |")
            rows.append("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in [name, pct(r["share"]), pp(r["d_prev"]), pp(r["d_year"]), num(r["level"]), yoy(r["yoy"])]) + "</tr>")
        H.append(f"<h3>{html.escape(title_)} – week ending {fdate(blk['period'])}</h3>"
                 f"<table><tr><th>Broker</th><th>Share</th><th>vs prior week</th><th>vs year ago</th><th>Avg {html.escape(unit)}</th><th>y/y growth</th></tr>" + "".join(rows) + "</table>")
        for n_ in notes:
            md.append(f"\n{n_}")
            H.append(f"<p><i>{html.escape(n_)}</i></p>")

    table("Share of daily active users", dau_w, "DAU")
    table("Share of app downloads", dl_w, "downloads/day")

    cav = [
        "Shares are of the tracked comp set only, not the total market. Avanza and Montrose are total-company series; the others are Sweden-only.",
        "Revolut Sweden is the whole Revolut app, so its DAU is not a trading-app figure. The dashboard lets you drop it from the comp set.",
        "Montrose has downloads and web only (below SensorTower's usage panel threshold).",
        "The connector delivers the Excel as text capped at 200k characters: Downloads and DAU sheets are complete, the Web Uniques sheet is cut off (through " + fdate(through["web_desktop"]) + ") and a fourth sheet is not delivered.",
    ]
    md.append("\n## Caveats\n"); md += [f"- {c}" for c in cav]
    H.append("<h3>Caveats</h3><ul>" + "".join(f"<li>{html.escape(c)}</li>" for c in cav) + "</ul>")
    H.append(f"<p>Generated {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} by sweden-brokers/pipeline/summarize.py.</p>")

    open(os.path.join(ROOT, "summary.md"), "w").write("\n".join(md) + "\n")
    open(os.path.join(ROOT, "summary.html"), "w").write("\n".join(H) + "\n")
    json.dump({"subject": title, "period": dau_w["period"], "email_date": v["email_date"]}, open(os.path.join(ROOT, "summary.json"), "w"), indent=1)
    print(title)


if __name__ == "__main__":
    url = None
    if "--dashboard-url" in sys.argv:
        url = sys.argv[sys.argv.index("--dashboard-url") + 1]
    main(url)
