# Driver grammars — reusable engine patterns beyond the core forecast mechanisms

A menu of build grammars distilled from the live finished models, kept GENERIC — no company names,
no theme names. Scan this menu during Step 0 when deciding how to model each unique KPI; build a
grammar only when the company's disclosure or the analyst's question calls for it. Each pattern
follows the standard conventions (drivers above the line, blue-on-yellow inputs, red residuals,
%-row stacks, memo fills) from model-engine.md + format-spec.md.

## G1. Cohort / vintage triangle
For unit-based businesses where per-cohort behavior drives a flow (deposits per account vintage,
retention, spend ramp). Structure — a `Memo:`-headed block or its own sub-section:
- **Cohort rows**: one row per acquisition cohort ("1Q21", "2Q21", … through the forecast horizon).
  Row content starts in that cohort's own quarter column (a triangle).
- **Cohort size diagonal**: each cohort row's first cell links that quarter's new units
  (`=<new units row><that quarter col>`).
- **Behavior/decay multipliers**: per-cohort per-age multipliers as blue inputs on the diagonal
  (e.g. contribution decaying 100% → 70% → 60% → 50% of initial as the cohort ages) — the forecast
  lever; hardcode history where disclosed.
- **Contribution matrix**: cohort size × multiplier × per-unit intensity per quarter.
- **Roll-up + tie**: `Calculated <KPI>` = column sum of all cohort rows; `Actual <KPI>` green link to
  the disclosed line; a `Plug` (ratio or $) row between them — small stable plugs mean the triangle
  is calibrated; a `Modeled` vs `Consensus` (red) pair where the Street models the KPI.
Forecast quarters extend the triangle with new cohorts at assumed sizes and the input multipliers.

## G2. Attach / penetration engine (subscriptions, premium tiers, add-on products)
- `Penetration Rate` = subscribers / unit base — gray in history, driven by a blue `# Q/Q` (or level)
  input in estimates; `NNA`-style annual average row + # Y/Y.
- `Subscribers` = penetration × unit base (bold; presentation blue in actuals).
- **New-vs-backbook decomposition**: `Total Units Q/Q` × blue `New attach rate` → `New User Attach`;
  `Backbook attach` = red residual (= total subscriber adds − new-user attach) with an
  `as % of backbook` gray memo — separates sell-to-new from sell-to-existing.
- Alt-data check row (% Q/Q from a tracker vs modeled % Q/Q) where a feed exists.
- Monetization: subscribers × price (annual/4) with a `Cost per user` memo where rewards/costs
  offset.

## G3. Event / deal calendar build
For young, event-driven volume products (event contracts, IPO windows, launch calendars):
- **Calendar scaffold**: rows for event counts per month/quarter by tier (regular / marquee /
  playoff / finals — whatever the real tiers are), blue where scheduled, sourced.
- **Per-event intensity**: `Contracts (units) per event` derived from a disclosed anchor period,
  then blue multipliers per tier (`Multiple vs <anchor>` inputs).
- **Share/participation input** where an industry pool exists (`as % of <pool>` blue).
- Roll-up: Σ(tier events × per-event units × multiplier) → product volumes feeding the standard
  pool × share × rate engine. `Cases >>>` scenario input rows (bear/base/bull event counts or
  multipliers) may sit beside it, informational.
- Contra-revenue memo where promos net against revenue (`take rate ex-contra` as the clean rate).

## G4. Toggleable thematic overlay (the sanctioned way a scenario feeds the P&L)
- Block per affected line: base exposure (green link) × blue `Adoption %` × blue `Allocation %` ×
  (blue `Activity multiple` − 1) × take rate (green link) = uplift; sum across products.
- Blue **`Phase in`** ramp row (e.g. +15%/qtr toward 100%).
- Blue **`on / off` (1/0)** row — the engine adds `uplift × phase-in × toggle` into the driven line.
  Ship with the toggle at 0 (base case) unless the user says otherwise.
- `Memo: overlay EPS impact` row (red italic) showing included-vs-excluded delta. Everything else
  about inline scenario memos stays informational-only.

## G5. New-initiative valuation stub (informational)
Parked beside a new product's engine: estimated run-rate revenue (×4 where quarterly) → blue
multiple → implied value → blue haircut/tax → blue ownership/attribution → value per share
(`/diluted shares`). Never feeds the P&L; flags what the option is worth if it works.

## G6. Alt-data staging tab + date-keyed pull
For any long-history external feed (app downloads, web/card trackers, internal data-team extracts,
peer monthlies):
- **Staging tab** per source: raw table with a DATE column (normalized to month-end) + value
  column(s), header row naming series + source + as-of date; keep ALL raw history here, never on the
  Model tab.
- **Model-side pull**: Month 1/2/3 rows pull by the EOMONTH scaffold dates —
  `=VLOOKUP(<month-end cell>, '<Staging>'!$A:$C, <col>, FALSE)` (or XLOOKUP/INDEX-MATCH) in dark
  green #006600 — then the standard Sum/Average + %-row + Seasonals/Vs-Normal stack computes on the
  Model tab.
- Missing months stay blank with a note; K-tag the source on every pulled row. A feed used only as a
  lead indicator stays a `Memo:` block; a feed that DRIVES a line gets the full driver treatment.

## G7. Monthly Seasonals + Vs-Normal (nowcast lens)
Under every monthly % M/M and # M/M block (already in model-engine §5, restated here as the pattern):
`Seasonals` = AVERAGE of prior years' same-month change; `Vs Normal Seasonality` = current − normal.
Red italic. This pair is how the intra-quarter print is judged against history when setting the
next input.

## G8. 2Q-stack rows
For products too young for Y/Y: `2Q Stack` = `=cur / two quarters ago − 1` (gray), alongside % Q/Q,
until four year-ago quarters exist.

## G9. Sidecar what-if tab (use sparingly)
When a thematic analysis outgrows a memo block (international TAM build, adoption study): a separate
tab building the case bottom-up (its own pools, conversion inputs, sensitivity columns), feeding the
Model through EXACTLY ONE blue driver cell (or a G4 toggle block) — labeled on both sides
(`Feeds Model!<cell>` / `From '<tab>'`). Default: not built; add when Step 0 surfaces a material
non-consensus theme or the user asks.
