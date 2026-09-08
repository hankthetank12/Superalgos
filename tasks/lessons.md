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
