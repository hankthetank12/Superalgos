# Publishing the dashboard to Kit

Kit (kit.walleyetrading.net) is Walleye's internal app platform. It is reachable only from
inside the firm's network and it serves a frozen copy of whatever was last pushed, so the
publish has to run from a Walleye machine. The cloud session that rebuilds this dashboard
cannot reach Kit (its hosts answer 502 from outside the network).

## How the other hub dashboards get to Kit

The SharePoint Dashboards hub (`JBCM/Shared Documents/NewCo/HS/Dashboards`) already carries the
publisher used for its other pages:

- `kit-publish.ps1` — pushes a self-contained HTML page with an HTTP PUT to
  `https://nnj2-seal7742.walleyetrading.net/kit/v1/apps/<slug>` (Kerberos auth, the same
  `--negotiate -u:` login the Kit setup command uses), then reads the app back and checks the
  round trip is byte-identical.
- `kit-apps.json` — the manifest it maintains: one entry per app with `file`, `slug`, `put`,
  `url` (`https://kit.walleyetrading.net/kit/v1/apps/<slug>`), `scope` (`team`), `version`,
  `bytes` and the round-trip result.

Kit assigns the slug on first publish; later publishes to the same slug replace the page.
Setup for the kit skill, from the 9 July 2026 "Walleye Kit" announcement (Tyler Wilson):
`curl.exe -sL --negotiate -u: https://nnj2-seal7742.walleyetrading.net/kit/public/skill.md -o "$HOME\.claude\skills\kit\SKILL.md"`;
docs at https://kit.walleyetrading.net/kit#setup, apps list at https://kit.walleyetrading.net/kit#apps.

## First publish

The cloud refresh uploads the page to the hub folder as `Sweden Retail Brokers.html` and the hub
card is already in `index.html`, so the file to publish is the hub copy.

1. On your machine, open PowerShell in the synced Dashboards folder and run `kit-publish.ps1`
   for `Sweden Retail Brokers.html` (see the script's parameter block for how it takes a file
   or title; it is the same call used for the other hub pages). It records the new slug in
   `kit-apps.json`.
   Alternative: paste `KIT_PROMPT.txt` into Claude Code, which publishes through the kit skill.
2. Copy the slug into `KIT_APP` in `refresh-kit.cmd`.
3. Add the Kit link to the hub card: in `index.html`, change the Sweden Retail Brokers card's
   `<div class="o">Open&nbsp;&rarr;</div>` to the two-link form the Securitize Live AUM card uses
   (`Open in Kit ↗ · Dashboard file →`).

## Keeping the Kit copy current

Every refresh in the cloud rewrites `Sweden Retail Brokers.html` in the hub folder (and
`sweden-brokers/dashboard.html` on this branch). Kit never pulls, so after a refresh run
`refresh-kit.cmd`, or register it with Task Scheduler for weekday mornings after the 13:07 UTC
cloud run. It pulls the branch, copies the page into the hub folder and republishes to Kit.
