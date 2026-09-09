# Publishing the dashboard to Kit

Kit (kit.walleyetrading.net) is Walleye's internal app platform. It is reachable only from
inside the firm's network and it serves a frozen copy of whatever was last pushed, so the
publish has to run from a Walleye machine with the kit skill installed
(`~\.claude\skills\kit\SKILL.md`, per the 9 July 2026 "Walleye Kit" announcement).
The cloud session that rebuilds this dashboard cannot reach Kit.

## One-time publish

1. Make sure the repo is cloned locally and on the branch:
   `git clone https://github.com/hankthetank12/Superalgos C:\Users\hstauber\Superalgos`
   `git -C C:\Users\hstauber\Superalgos checkout claude/sweden-brokers-market-share-1kmz2n`
2. In Claude Code on your machine, paste the prompt in `KIT_PROMPT.txt` (adjust the path if
   the clone lives elsewhere). `dashboard.html` is a single self-contained file with no
   external requests, so Kit can serve it as a static page.
3. Copy the app slug Kit returns (the last path segment of
   `https://kit.walleyetrading.net/kit/v1/apps/<slug>`) into `KIT_APP` in `refresh-kit.cmd`.
4. Optional: add a card to the Dashboards hub (`Dashboards\index.html`) with the Kit link,
   the way the Securitize Live AUM card does.

## Keeping the Kit copy current

The cloud Routine rebuilds `dashboard.html` when a new relay email arrives and pushes it to
this branch. Kit never pulls, so run `refresh-kit.cmd` afterwards, or register it with Task
Scheduler for weekday mornings after the 13:07 UTC cloud run. It pulls the branch, copies
the page into the Dashboards hub, and republishes to Kit through the kit skill.

If your existing `rothera-dashboard\update.cmd` pushes to Kit with a direct command rather
than through the skill, swap that command into step 3 of `refresh-kit.cmd`; the rest of the
script is the same shape.
