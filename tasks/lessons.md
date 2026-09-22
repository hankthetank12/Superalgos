# Lessons

- 2026-09-08: Email-driven tasks in a remote session need the Microsoft 365 connector enabled
  in the chat, not just installed for the org. Check `ListConnectors.enabledInChat` before
  planning around inbox access, and say so up front instead of building on a guessed schema.
- The Microsoft 365 connector exposes search/read tools only (no send-mail). "Email me" has to
  go through a Routine completion notification or another sender.
- The Microsoft 365 connector renders an .xlsx attachment as tab-separated text with Excel serial
  dates and a hard 200,000-character cap ("[truncated: N of M sheets included]"). Big workbooks lose
  their tail sheets. Check for that marker on every attachment read and record it.
- `create_trigger` `connectors` is not available in this org, and a self-bound Routine reports "no
  passable connector grants". Test connector availability on the first firing before promising an
  unattended email-driven job; the fallback is a Routine created in the claude.ai Routines UI.
- SensorTower restates the trailing ~8 days between weekly emails: merge whole cells by date with
  the newest vintage winning, never append-only.
- Cross-check derived numbers against the source's own tables before shipping. The one mismatch
  (Trade Republic) came from missing-day treatment, not a bug, and needed a footnote, not a fix.
- A footnote that explains a discrepancy must be checked per metric. The same missing-day gap
  produced a difference for downloads (summed) but none for DAU (averaged); one generic sentence
  was wrong for half its uses.
- When a provider truncates a text export, the last row before the marker may be cut mid-number.
  Drop it and say so; a "43967" that should be "43967.606" is silent until a later restatement.
- In-cell chart labels need a measured fit, not a fixed pixel threshold; a lost leading sign flips
  the meaning of the number. Prefer an HTML grid that sizes to content over hand-placed SVG text.

## 2026-09-10 — large payloads through MCP tool parameters
- Bash/MCP tool output above ~20 KB is persisted to a file and not shown; a 120 KB file cannot be
  read whole. Read it in slices (`sed -n`, `cut -c` on long lines) that each stay under ~15 KB.
- A single tool call whose parameter is ~120 KB hit the per-turn output limit and was cut off.
  Shrink the payload at the source instead (here: gzip+base64 the embedded JSON, page inflates it
  with DecompressionStream; 120 KB → 70 KB) and pass `expectedBytes` so a bad transcription is
  refused. Then read the uploaded file back and `cmp`/md5 it against the local copy.
- Don't hand a subagent a job that is blocked by the same limits; it stalled for 35 minutes.
  Check `ListAgents` early and take over or redesign.

## 2026-09-10 — claims after a context reset
- After compaction, never quote a link, id or "done" state from memory. Re-find it with a search
  (here: `outlook_email_search` in Drafts) and cite the tool result. A reply to "send me the email"
  carried a draft link that was not in context; the real draft's webLink was found afterwards.
- The hub folder is shared with Henry's local build of the same pipeline (full workbook, CRLF,
  later web data). Before overwriting any shared file, read the live copy and compare freshness.

## 2026-09-16 — finish the runbook in one turn
- A scheduled run is not done until step 8's report is written. After the 2026-09-14 ingest the
  turn ended after the publish; the draft and report slipped two days and three firings answered
  with nothing. Do the remaining steps (upload guard, draft, push, report) in the same turn, and
  never answer a wake-up with an empty reply while a run is half finished.

## 2026-09-19 — make the no-op path cheap
- A polling Routine is mostly no-ops, and every firing pays for the whole conversation context. Two
  levers: fire less often (14/week -> 5, aimed at the Monday ~11:01 UTC arrival) and make the check
  one narrow call. Searching the Relay folder by sender+date paged through ~50 unrelated emails;
  `query: "Sweden Retail Brokers"` in that folder returns just the three matching messages.
- Gate the expensive work behind the cheap check: no git pull, no file reads, nothing until the
  search proves there is a new email.

## Put the deliverable before the polish
A long turn can be cut off at any point, and whatever is still pending is simply lost. Order a runbook's
steps by who is waiting on them, not by what feels logical: the email Henry reads comes before
republishing the artifact and before uploading to SharePoint, because a draft nobody wrote is invisible
while a dashboard published a few minutes later is not. Twice the refresh ended between the republish and
the draft; the fix was reordering the runbook, not another reminder to finish.
