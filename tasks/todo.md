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
- [ ] 10. Confirm the first scheduled firing (2026-09-08 23:07 UTC) still has Outlook tools. If
      not, recreate the Routine from the claude.ai Routines UI with the same prompt so a
      connector can be attached.

## Open items

1. Web Uniques arrive truncated (through 2026-07-25) and the fourth sheet is missing because the
   connector caps the attachment rendering at 200k characters. Ask Walleye Data Science to move
   Web Uniques ahead of the daily sheets, or to ship a second, smaller workbook, if the web view
   matters.
2. Missing-day treatment differs from the relay email (we average reported days; the email sums,
   so its y/y treats a missing day as zero). Flagged wherever it bites.

## Review

Filled in after the independent verification workflow (see git log for follow-up fixes).
