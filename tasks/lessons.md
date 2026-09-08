# Lessons

- 2026-09-08: Email-driven tasks in a remote session need the Microsoft 365 connector enabled
  in the chat, not just installed for the org. Check `ListConnectors.enabledInChat` before
  planning around inbox access, and say so up front instead of building on a guessed schema.
- The Microsoft 365 connector exposes search/read tools only (no send-mail). "Email me" has to
  go through a Routine completion notification or another sender.
