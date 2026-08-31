---
name: full-model-v6
description: "Build a full institutional quarterly earnings/KPI model on one deep Model tab — actuals hardcoded to the press release, estimates driver-built and seeded to consensus — plus Mini Model, Revisions, Drivers, Qtr, and the 1 Pager + NTM PE valuation pair in the same pass (DCF only on request). Step 0 gate: FIRST ask for the latest earnings release and investor presentations, mirror management's presentation, and mine them for KPIs absent from VAActuals/consensus to build as drivers. Mandatory sector engines: RETAIL BROKER (funded-account roll, NNA/market bridge, pool x share x activity x take-rate engines, broker NII stack) for any broker or trading app; ALT MANAGER (per-fund lifecycle blocks with step-down triggers, perpetual fee stacks, AUM walks, FRE/DE waterfall) for any alternative asset manager. Handles UPDATE MODE (roll the quarter, append months, re-snapshot Revisions) and guidance overlays. Use whenever someone wants to build, forecast, update, roll, or model out a quarterly, earnings, or KPI model."
---

# Full Model v6

Builds a full quarterly earnings model on a single deep **Model** tab — quarterly history +
forecasts, monthly detail inside each quarter, annual SUMIFS columns, driver engines below the P&L,
actuals tied to the dollar, estimates seeded to consensus and fully driver-flexible, strict Street
formatting — then, in the same pass, the downstream tabs: **Mini Model → Revisions → Drivers → Qtr →
1 Pager + NTM PE**. (Lineage/history: `references/changelog.md` — not needed for building.)

## When to use
Full quarterly earnings model for a public company, or maintenance of one built on this system.
Trigger phrases: "build the full model", "quarterly model", "earnings model", "model this like
IBKR/HOOD", "retail broker model", "update the model", "roll the quarter". For a single standalone
tab on an existing model, the lighter standalone skills (`mini-model-v7-*`, `revisions-tab`,
`drivers-kpi-vs-consensus-v2`, `qtr-model-vs-street-v2`, `relative-valuation-1pager-dashboard`,
`dcf`) are the better path; for annual-only mini-models alone use the `mini-model-*` skills.

## Mode fork (decide FIRST)
- **Fresh build** — no existing model workbook (or the user wants a rebuild): follow the build order
  below.
- **Update mode** — the workbook already has a Model built on this system and the user wants it
  rolled/refreshed (new quarter printed, new monthlies, new guidance): read
  `references/update-mode.md` and follow it instead. Never rebuild or reformat a living workbook,
  and respect its existing layout.

## Step 0 — source materials gate (fresh builds; STOP here first)
The very first action: **ask the user for the company's most recent earnings release and
earnings/investor presentations** (press release, deck, financial supplement), unless already in the
workspace. Do not scope, research from memory, or touch the sheet until they arrive. They serve two
mandatory purposes:
1. **Mirror management.** The release/deck reveals the segment cut, disclosure order, preferred
   non-GAAP presentation, and the metrics management leads with — the P&L rollup, engine structure,
   and headline lines mirror MANAGEMENT's framing, not a generic template or the GAAP cut.
2. **Hunt for company-only KPIs.** Systematically scan for operating metrics the company discloses
   that VAActuals/consensus does NOT carry (cohort stats, per-account intensities, product volumes,
   attach rates, funnel metrics, monthly stats). These are prime driver candidates precisely because
   the Street isn't modeling them — check `references/driver-grammars.md` for the right grammar
   (cohort triangle, attach engine, event calendar, staging feed, toggleable overlay) and build the
   best ones into the driver stack. Flag in the reply which drivers are company-only vs
   consensus-carried.

Then research the business (release + deck first, then 10-K/10-Q business section, latest call
transcript, IR site): revenue build and unit economics per segment; the 5–10 operating drivers that
actually move earnings and how they combine; disclosure cadence (monthly vs quarterly); actuals
source (press release / Daloopa) and the consensus source per the ladder below; peers and structural
quirks (pro-forma periods, M&A, Up-C structure, share events). **Do not start the skeleton until you
can state, in one paragraph, this company's revenue build and its KPI set.** Carry those drivers into
the P&L layout, the engines, and the Drivers/Qtr KPI selection.

## Sector router (read the engine reference BEFORE scoping the sheet)
| Company type | Mandatory read | Engine it replaces |
|---|---|---|
| Retail broker / neobroker / trading app (IBKR, HOOD, BULL, SCHW-retail…) | `references/retail-broker-engine.md` | Revenue + NII engines (five-layer broker cascade) |
| Alternative asset manager (BX, KKR, APO, ARES, CG, BAM, TPG, OWL…) | `references/alt-manager-engine.md` | Revenue engine (fund lifecycles → AUM walks → FRE/DE) |
| Bank / broker-dealer | model-engine §15–16, 19–20 (driven balance sheet + capital layer) | NII/balance-sheet layer |
| Exchange / per-unit transactional (default) | model-engine §11–12 (volume × price, pool × capture) | — |
| Advisory / people business | model-engine §11 (headcount × comp engine) | Comp engine |
Spread books with repricing lag add the vintage roll-on/roll-off engine (model-engine §11); Up-C /
listed-partnership structures add the two-tier tax/NCI waterfall (§17). Translate time grain per
engine: sequential balance rolls use prior-quarter Ending; YoY-driven levels use the same quarter one
year back.

## Core design philosophy
1. **One sheet, everything visible.** Summary IS, then the P&L; every driver engine BELOW it in
   banner-labeled sections; engine outputs feed green links up into the P&L.
2. **Actual vs. estimate duality.** ACTUAL quarters: reported totals are blue hardcodes (or Daloopa
   pulls) with one red plug per block so components reconcile to the dollar. ESTIMATE quarters:
   components build bottom-up from drivers; totals become black sums.
3. **Monthly granularity inside quarters** for company KPIs AND market data; latest undisclosed
   month is the blue-on-yellow nowcast input.
4. **Every forecast rests on a small blue-on-yellow input** — %Y/Y, Δ on a ratio, beta, level, or
   capture rate. Never hardcode a black forecast number; never drive a % line with a %Y/Y input.
5. **Every stock rolls forward and every seam has a check row** (0/"-"); per-share expression on
   every earnings stream.

## Consensus-source ladder (resolve once; details model-engine §8)
(1) A **VAActuals/consensus tab** in the workbook → red links everywhere consensus appears (the only
source that supports build-time value verification). (2) Else a **red hardcoded consensus snapshot**
from what the user provides (state values + as-of date in the reply). (3) **Bloomberg BQL/BDP** only
as clearly-flagged refresh-on-open formulas (1 Pager / NTM PE) — they cannot evaluate at build time,
are never the Model's spine, and are never claimed as verified.

## Do-not-build list (unless the condition is met or the user asks)
- **DCF** — only on explicit request (`references/dcf-tab.md`); the 1 Pager + NTM PE pair is the
  default valuation layer.
- **Daloopa actuals wiring** — only when a Daloopa tab exists (model-engine §9).
- **Up-C waterfall, vintage roll-on/roll-off, rate-path scaffold, market-vs-organic bridge,
  per-unit intensity, cohort triangle, sidecar what-if tabs** — applicability-gated (their sections
  say when).
- **Guidance overlay** — only when a "Guidance" tab exists (`references/guidance-overlay.md`).
- Live-BQL consensus spines, canary cells, fabricated "live" data — never in a Bloomberg-dead build.

## Build order (fresh build)
Read `references/model-engine.md` + `references/format-spec.md` before step 3 and keep both open.
1. **Step 0 + research** (above); sector reference per the router.
2. **Scope**: layout variables (`label_end_col`/`first_data_col`, defaults K/L), history/horizon
   (defaults: all printed quarters ≥12, 8–10 estimate quarters), focal quarter = next unreported;
   disclosure cadence; consensus source; market-data tickers; spread-book duration N if applicable.
3. **Header scaffold** (model-engine §1), period banner, freeze panes, EPS strip (§2).
4. **Summary Income Statement** (§3), then the **P&L skeleton** (§4) — business rollup with %Y/Y,
   %Q/Q, #Y/Y and Annual pairs; blue actuals; plugs wired. If a "Guidance" tab exists, read it NOW
   and reserve guidance rows in the skeleton (`references/guidance-overlay.md`) — before the map
   freezes.
5. **Revenue engines** with inline drivers (§11–12 + sector reference + driver grammars): tracking
   blocks, TAM→share ladders, per-unit intensity (§13), market-vs-organic bridges (§14), read-across
   / alt-data memos (§6), staging tabs (G6); link outputs up.
6. **NII / balance engines** (§15), comp engine, tax/NCI (§17), Capital & Returns (§19), balance
   sheet + cash flow (§20), per-share rows + Incremental Margins, share-count roll, check rows at
   every seam (§16).
7. **Annual columns** (§21 — one fixed SUMIFS range) and EPS-strip wiring.
8. **Formatting + audit sweep** per format-spec: banners + separators, boxes, rules, number formats,
   color-role re-derivation, focal shapes.
9. **Verify the Model (gates below).** This audit GATES the downstream tabs — the row/column map
   freezes here.
10. **Mini Model** — `references/mini-model.md` (VA-linked actuals, in-tab drivers).
11. **Revisions** — `references/revisions-tab.md`.
12. **Drivers** — `references/drivers-tab.md` (Street source per the ladder).
13. **Qtr** — `references/qtr-model-vs-street.md` (v2 spec).
14. **1 Pager + NTM PE** — `references/one-pager-ntm-pe.md` (default valuation pair; DCF only if
    explicitly requested, LAST, per `references/dcf-tab.md`).
15. **Verify downstream tabs and the whole workbook** (gates below), then report.

## Verification — five gates
Run `python scripts/audit_model.py <workbook>` first and fix genuine FAILs (it reports, never
loops); image-verify what it can't see (banner separators, Annual boxes, focal shapes, rules).
- **Gate 1 — Research/scope**: Step 0 materials obtained; P&L mirrors management; company-only KPIs
  scanned and built; sector reference applied.
- **Gate 2 — Model financial audit**: full rebuild; every reported quarter ties to $0 (tie memos);
  estimates tie consensus at seed per the ladder (EPS to the cent when a consensus tab exists;
  market-pool lines via back-solved capture); wiggle test passes and seeds restored; ALL check rows
  0/"-"; zero error cells; annuals off ONE fixed SUMIFS range.
- **Gate 3 — Sector/module audit**: the sector engine's own acceptance list passes (R1–R8 broker;
  A1–A6 alt manager); applicability modules built where their conditions hold (per-unit, bridges,
  Up-C, guidance rows placed and excluded from sweeps).
- **Gate 4 — Format audit**: format-spec conventions hold (fonts, color roles, fills, banners +
  white year separators, boxed Annual pairs, label-through-numbers rules, focal shapes, gridlines/
  freeze); verified by script + image.
- **Gate 5 — Downstream tabs**: each tab passes the verify list IN ITS OWN reference file; links tie
  the frozen Model map; consensus source consistent everywhere; hidden Qtr FY columns read back
  clean.

## Report (the reply after building)
State: tie numbers and where assumption cells live; the consensus source used (and snapshot as-of
date if hardcoded); stated (non-consensus) seeds and data gaps; which drivers came from company-only
disclosure; scenario-memo/overlay locations and toggle states (overlays ship OFF); guidance items
placed/unmatched (if a Guidance tab exists); the 1 Pager's two Model-EPS link cells; Bloomberg
formulas left to heal on the user's desktop; any cells flagged for follow-up.

## Reference index
`model-engine.md` (Model-tab mechanics — read at step 3) · `format-spec.md` (formatting canon — read
at step 3) · `retail-broker-engine.md` / `alt-manager-engine.md` (sector gates — read at step 1) ·
`driver-grammars.md` (KPI grammar menu — scan at Step 0) · `mini-model.md`, `revisions-tab.md`,
`drivers-tab.md`, `qtr-model-vs-street.md`, `one-pager-ntm-pe.md` (read at their build step) ·
`dcf-tab.md` (opt-in only) · `guidance-overlay.md` + `scripts/insert_guidance_rows.py` (only when a
Guidance tab exists) · `update-mode.md` (update mode) · `scripts/audit_model.py` (gates) ·
`changelog.md` (lineage — never needed for building).
