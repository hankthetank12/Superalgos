# Sweden retail brokers — market-share dashboard

Goal: track Swedish retail-broker market share from the recurring "Sweden retail brokers"
email (body + Excel attachment) in the Outlook relay folder. Rebuild the dashboard on every
new email and send a summary of the main charts.

## Status

Blocked on data access. The Microsoft 365 connector (Outlook search + read) is installed for
the org but not enabled in this chat, so the relay folder cannot be read from this session.
Everything below that does not need the email is planned; nothing is built against a guessed
schema.

## Plan

- [ ] 1. Enable the Microsoft 365 connector for this chat (user action), or drop the .eml/.msg
      and .xlsx into `sweden-brokers/data/raw/` on this branch.
- [ ] 2. Find the "Sweden retail brokers" email(s) in the relay folder; pull body + attachment.
- [ ] 3. Profile the workbook: sheets, brokers, metrics, periods, units. Decide the charts.
- [ ] 4. `sweden-brokers/pipeline/ingest.py` — attachment -> `data/market_share.csv`
      (long format: `period, broker, metric, value, source_date, source_file`). Idempotent:
      re-running on the same file adds zero rows; a new month appends.
- [ ] 5. `sweden-brokers/pipeline/render.py` — CSV -> `dashboard.html` (dataviz skill palette,
      light/dark safe). Publish as an Artifact; keep one stable URL and redeploy in place.
- [ ] 6. `sweden-brokers/pipeline/summarize.py` — latest-month summary of the main charts
      (share levels, MoM/YoY deltas, leaders/laggards) as plain text for the email.
- [ ] 7. Auto-update: a Routine (fresh session per fire, Microsoft 365 connector attached)
      on a weekday schedule. Each run: search the relay folder for emails newer than
      `data/state.json`, ingest, render, republish, commit + push this branch.
- [ ] 8. Summary email: the Microsoft 365 connector is search/read only (no send tool), so the
      Routine's completion email carries the summary. Confirm this is acceptable, or pick a
      different sender.
- [ ] 9. Verify: re-run ingest on the same file (0 new rows), screenshot the dashboard, check
      the numbers on the charts against the Excel by hand for one month.

## Open questions for the user

1. Exact folder name in Outlook ("Relay"? "Email Relay"?) and the sender / subject pattern.
2. Which market-share series matter most (turnover share, trade-count share, customers,
   net inflows?) — will propose after seeing the workbook.
3. OK for the summary to arrive as the Routine's completion email rather than a mail sent
   from your own mailbox?

## Review

(filled in when the work is done)
