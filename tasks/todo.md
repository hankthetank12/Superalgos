# Sweden retail brokers — market-share dashboard

Goal: track Swedish retail-broker market share from the recurring "Sweden Retail Brokers"
email (body + Excel attachment) in the Outlook folder "Relay". Rebuild the dashboard on every
new email and deliver a summary of the main charts.

## Status

Built and published. Dashboard: https://claude.ai/code/artifact/5bb7e287-b511-4405-bef7-d01f13959629
Scheduled refresh: Routine `trig_012yp2jWq94QxguCssTQ6QaF`, 13:07 and 23:07 UTC daily, bound to the
build session; procedure in `sweden-brokers/RUNBOOK.md`.

## Plan

- [x] 1. Enable the Microsoft 365 connector for this chat (user did this).
- [x] 2. Find the "Sweden Retail Brokers" emails in the Relay folder; pull body + attachment.
      Two so far: 2026-09-01 and 2026-09-07, from relay@walleyecapital.com (Walleye Data Science).
- [x] 3. Profile the workbook. Sheets: Downloads Daily, DAU Daily, Web Uniques Daily (+ a fourth
      sheet the connector never delivers). Daily since 2022-01-01, Excel serial dates, blanks =
      not reported. SensorTower restates the trailing ~8 days between emails.
- [x] 4. `pipeline/ingest.py` — dump -> `data/daily.csv` (long: date, metric, broker, value,
      vintage). Newest email wins cell by cell, blanks never overwrite. Re-run adds 0 rows.
- [x] 5. `pipeline/build.py` + `pipeline/template.html` — weekly (Sunday-ending) and monthly means
      with coverage -> `dashboard.html`. Charts: share scoreboard, 100% stacked share, small
      multiples, YoY heatmaps, web-share lines, levels. Comp-set toggle recomputes shares.
- [x] 6. `pipeline/summarize.py` — `summary.md` / `summary.html` / `summary.json`.
- [x] 7. Auto-update Routine (self-bound; the org does not allow connector grants on Routines).
- [x] 8. Summary email: connector is drafts-only, so each run leaves a ready-to-send draft in
      Outlook Drafts addressed to henry@serenovalp.com.
- [x] 9. Verify: ingest idempotent (md5 unchanged on re-run); palette validator passes light and
      dark; render checked at 1280px in both themes; August 2026 y/y matches the email's own
      tables for every broker except Trade Republic (unreported days, flagged in the output).
- [x] 10. First scheduled firing (2026-09-08 23:09 UTC) ran with Outlook access: it paged all 63
      relay emails since 6 Sep, found no new Sweden Retail Brokers email, and left the dashboard
      unchanged.

- [x] 11. Dashboards hub (SharePoint `JBCM/Shared Documents/NewCo/HS/Dashboards`): `build.py` now also
      writes `sweden-brokers/hub/Sweden Retail Brokers.html` (standalone copy); uploaded to the hub
      folder, card added at the top of the auto-refreshed grid in `index.html` (backup kept as
      `index.html.bak-pre-swedenbrokers-20260910`; SharePoint version history has the exact prior
      version), counts bumped to 54 / 40 auto-refreshed. Note: the connector's text upload path
      cannot carry CR bytes, so `index.html` is now LF-terminated (was CRLF); harmless for HTML.
      Runbook step 5b re-uploads the dashboard file on every refresh; the card carries no dates.
- [ ] 12. Post to Kit. Kit is internal-network and push-only, so the publish must run on Henry's
      machine. The hub folder's own `kit-publish.ps1` (PUT to nnj2-seal7742…/kit/v1/apps/<slug>,
      tracked in `kit-apps.json`) is the way the other 50+ hub pages got there; run it for
      `Sweden Retail Brokers.html`, or paste `sweden-brokers/kit/KIT_PROMPT.txt` into local Claude
      Code. Then put the slug into `kit/refresh-kit.cmd` and add the Kit link to the hub card.
- [x] 13. Morning email: Outlook draft to henry@serenovalp.com with the headlines, share tables and
      links to the hub file, hub page and artifact (connector is drafts-only, so it is not sent).

## Open items

1. Web Uniques arrive truncated (through 2026-07-25) and the fourth sheet is missing because the
   connector caps the attachment rendering at 200k characters. Ask Walleye Data Science to move
   Web Uniques ahead of the daily sheets, or to ship a second, smaller workbook, if the web view
   matters.
2. Missing-day treatment differs from the relay email (we average reported days; the email sums,
   so its y/y treats a missing day as zero). Flagged wherever it bites.

## Review

Independent verification (four reviewers, each finding attacked by a skeptic before it counted):

- Numbers: every weekly mean, share, pp delta and y/y in the summary reproduced from the raw dumps
  and matched the relay email's own tables. One inaccuracy: the Trade Republic footnote claimed the
  email zero-fills missing days for DAU; it only does so for downloads. Footnote is now metric-specific.
- Merge: cell diff between the two emails matched ingest's counts exactly (174 new, 81 restated).
  Defects fixed: the possibly partial last row before the 200k truncation marker was ingested as a
  real value (43967 instead of 43967.606); vintage attribution depended on ingest order across runs;
  an unmapped column would have crashed the save. All three fixed, order independence re-verified.
- Dashboard: zero console errors across every control at 1280 and 800px, colours stable under
  comp-set toggles, incomplete week excluded everywhere, all tokens defined in all three theme
  scopes. Defects fixed: heatmap labels overflowed cells at half width (a "+289%" read as "−289%")
  and weekly heatmaps showed no numbers; both replaced by a scrollable grid that always prints
  values. Also fixed: 2.5% gridlines labelled "3%", "0.0" baselines, "−0%", no year on monthly
  heat ticks, empty web charts when all three sites are toggled off.
- Runbook: rewritten to survive a half-finished run (clean-tree check), page the email search by
  date instead of relevance, skip and record a bad email instead of retrying it forever, commit
  before publish/draft, and recover from a rejected push.
