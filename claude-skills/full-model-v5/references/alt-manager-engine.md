# Alternative Asset Manager engine

Sector reference for ALTERNATIVE ASSET MANAGERS — private markets / credit / PE / RE / infrastructure
managers (BX, KKR, APO, ARES, CG, BAM, TPG, OWL, PGHN and comparable names). Distilled from a live
audited Blackstone build. **Read this whole file before building any alt manager — it is mandatory
for the sector**, exactly as the retail-broker reference is for brokers. It layers on top of
`model-engine.md` + `format-spec.md`: this file specifies WHAT to build and the AM-specific engine
grammar, not the formatting system. Names below (fund names, strategy cuts) are EXAMPLES — take the
real fund list and segment cut from the company's supplement/10-K/deck (Step 0 materials), never
from this file.

## The alt-manager identity

The P&L is a fee waterfall on managed assets, so the model is an ASSET machine first:

```
1. PER-FUND / PER-VEHICLE ENGINES   flagship drawdown funds + perpetual vehicles (the fee base)
2. SEGMENT AUM WALK                 BOP → flows → realized → market → step-downs → EOP FEAUM
3. SEGMENT PnL                      mgmt fees = Σ(AUM × rate); FRE = fees − fee comp − opex
4. PERFORMANCE / REALIZATIONS       realized perf revenue − perf comp + principal inv income
5. GROUP ROLLUP                     segments → FRE → DE → DE/share, unit structure, dividend
```

Each reportable segment (e.g. Private Equity / Real Estate / Multi-Asset / Credit & Insurance) gets
its own tier-1 section containing layers 1–3; performance income and the group rollup close the tab.
Fee-earning AUM (FEAUM/FPAUM) is the revenue base — track it separately from total AUM everywhere.

## Layer 1a — Flagship (drawdown) fund engine — one block per fund

Sub-section banner (tier 2) "Flagship Funds"; each fund gets a tier-3 child banner and the same
~40–50-row lifecycle block. Fund list = every active + in-market flagship from the supplement, plus
the NEXT vintage when management has guided to it (fundraising targets from Step 0/Guidance).

Per-fund block, in order:
1. **Mgmt Fee Rate Assumptions** — two static blue inputs parked in the label area: `Investment
   period` rate and `Step Down` rate (post-investment-period rate, often on invested cost).
2. **Commitments walk (AUM basis)**: `BOP Commitments (=prior EOP)` green · `New Closes — Flow into
   AUM` (red residual in actual columns `=EOP−BOP`; blue input in estimates, seeded to the
   fundraising target/guide) · `Commitments (EOP)` — press-release/supplement blue in actuals,
   `=BOP+closes` in estimates.
3. **Capital Invested walk**: `Available Capital (Dry Powder)` (blue in actuals; `=EOP commitments −
   EOP invested` red in estimates) · `BOP Capital Invested` · `Capital Deployed in Period` (formula
   in actuals `=EOP−BOP`; blue deployment-pace input in estimates) · `Capital Invested (EOP)` ·
   `% Called` on a gray band (`=invested/commitments`, IFERROR-guarded) with a `# Q/Q (bps)` gray
   memo.
4. **Realizations walk**: `BOP Cumulative Realized Proceeds` · `Realized Proceeds in Period` (blue
   input in estimates — the realization-pace lever) · `Cumulative Realized Proceeds` ·
   `% of Capital Invested Returned` (gray band).
5. **NAV walk**: `BOP NAV` · `+ Capital Deployed` (green link) · `− Realized Proceeds` · `Market
   Change` (red residual in actuals; `=BOP NAV × % Chg` in estimates with a blue `% Chg` input) ·
   `NAV (EOP)` (supplement blue in actuals). Then `Total Value (NAV + Cum. Realized)` and
   **`MOIC (x)`** on a gray band (`=total value / invested`, format `0.0"x"`).
6. **FEAUM & step-down**: `Step-Down Trigger (enter 1 in trigger qtr only)` — a blue BINARY input
   row · `Post Step-Down? (cumulative)` gray helper `=SUM($<start>:cur)` · `BOP FPAUM` · `Flows into
   FPAUM` `=IF(post-stepdown, deployed, new closes)` (fee basis switches from commitments to
   invested at step-down — adjust if the fund's basis differs) · `Step-Down Impact (one-time)` red
   `=IF(trigger=1, invested − commitments, 0)` · `FPAUM (EOP)`.
7. **Management fees**: `Fee Rate (annual)` gray band `=IF(post-stepdown, stepdown rate, investment
   rate)` · `Mgmt Fees ($mm) = FPAUM × rate / 4` · `# Q/Q` gray memo.
Fee holidays: model as the trigger/rate mechanics of the fund (a 0% investment-period rate until the
holiday ends, or a delayed activation quarter) — management's guided activation dates come from
Step 0/Guidance and belong period-aligned in the fund's block.

## Layer 1b — Perpetual / semi-liquid vehicles

Sub-section "Perpetual": one row per vehicle (e.g. core-PE, infrastructure, retail/wealth vehicles)
with EOP AUM (supplement blue in actuals; grown by blue % or NNA inputs in estimates), an average
row per vehicle, and a `Total` roll. In the segment PnL, each vehicle carries its **own fee-rate row**
(blue, often guided) and the blended perpetual fee rate computes as
`=SUMPRODUCT(vehicle AUMs, vehicle rates) / total perpetual AUM`.

## Layer 2 — Segment AUM walk (the reported bridge)

Sub-section "AUM Walk" per segment — this is the block that ties the company's reported FEAUM bridge:
- `BOP FPAUM` green · `Inflows` (press-release blue in actuals; estimates driven `as % of BOP` blue
  input) with an `as % of BOP` gray row · `Outflows` (same pattern, negative) · flow decomposition
  memo rows where the fund engines exist: `Flagship Flows` (green from layer 1a), `Perpetual Flows`
  (green from 1b), `Non-Flagship Flows` (red residual) · `Net Flows` bold with `as % of BOP` ·
  `Realized` (blue in actuals; `=BOP × blue % input × −1` in estimates) · `Market appreciation /
  (depreciation)` (blue in actuals; `=BOP × blue % input`) — optionally decomposed into
  perpetual-linked vs other with a red residual · `Stepdown` (dark-green link from the fund engines)
  · **`Ending fee-earning AUM`** (supplement blue in actuals, sum in estimates) with % rows and the
  Annual (=4Q value) pair · `Average fee-earning AUM` (supplement blue in actuals — companies often
  report a weighted average; `=AVERAGE(BOP,EOP)` in estimates with the diff noted) with % rows.
- **`Memo: Total AUM`** (#CCCCFF): `FEAUM % of total AUM` (blue input in estimates) → `Total AUM
  (EOP)` — ties the headline AUM number the Street quotes.
- Mgmt-guidance rows (violet) attach here heavily — fundraising targets, activation timing,
  flow guides.

## Layer 3 — Segment PnL

Sub-section "PnL" per segment:
- **Fee-rate stack**: perpetual per-vehicle average-AUM helper rows + per-vehicle fee-rate inputs →
  blended `Total Fee Rate` (SUMPRODUCT); `Flagship Fee Rate` = SUMPRODUCT(fund fees, fund AUMs)/
  flagship AUM (or Σ fund fees directly); `Other Fees` back-solved on the residual AUM (red) —
  each rate with # Y/Y / # Q/Q gray memos and Annual pairs.
- `Base management fees` = Σ(per-fund fees) + Σ(perpetual AUM × rates) + other — blue press-release
  hardcode in actuals with the engine formula in estimates; `Base Fee Rate` check row
  (`=fees×4/avg FPAUM`) against the blended stack.
- `Transaction & other fees`, `Mgmt fee offsets` (underline), → `Total management & advisory fees`.
- `Fee-related performance revenues` (FRPR) — %Y/Y driven or crystallization-scheduled (guidance
  often names the schedule; scheduled crystallizations get their own memo rows).
- `Fee-related compensation` (%-of-fee-revs or %Y/Y input; note guided comp-offset mechanics),
  `Other operating expenses` (%Y/Y with decelerating-growth guides) → **`Fee-Related Earnings
  (FRE)`** with `FRE margin` on the gray band + # Y/Y; `FRE Comp Ratio` / `Other Opex Ratio` gray
  bands.
- Segment DE: FRE + realized performance income (below) where the company presents it per segment.

## Layer 4 — Performance / realizations (group or per segment, per disclosure)

`Realized performance revenues` (blue actuals; blue %Y/Y or realization-pace inputs in estimates —
tie to the funds' realization walks where built) · `Realized performance compensation` (% of perf
revs input) · `Realized principal investment income` → **`Total net realizations`**. Where the
company schedules crystallizations (e.g. institutional infra on a 3-yr cycle), a `Memo:` block lays
out the schedule and the estimate quarters it lands in.

## Layer 5 — Group rollup, unit structure, capital return

- `Total segment distributable earnings` = Σ segments (press-release blue in actuals) · `Net
  interest income/(loss)` · `Pre-tax DE` · `Income taxes` (`=PT DE × ETR` with blue ETR inputs; # Y/Y)
  → **`Distributable Earnings`**.
- **Unit waterfall** (publicly-traded partnership / Up-C-lite): `DE Before Payables` (+/− payables
  rows) · `Percent to Common` `=common shares / total units` · `DE to Common` · **`DE Per Share`**
  (press-release blue in actuals; `=DE to common / units` estimates) with % rows and Annual pair ·
  `Common Shares` (blue) · `Partnership Units` (red residual `=total − common`) · `Diluted DE
  shares/units` with the share roll where buybacks matter. Full two-tier tax builds: model-engine
  §17.
- `Dividend per share` (policy % of DE — blue input or guided) with `Payout ratio` gray row.
- Capital & Returns module per model-engine §19 (FRE/DE per share replace EPS in the per-share
  rows; add `FRE, net of equity-based comp` and after-tax variants where the Street quotes them).

## KPI set (for Step 0, Drivers tab & Qtr tab selection)

Canonical AM KPI banner: Total AUM, Fee-earning AUM (total + by segment), inflows/net flows (+
fundraising toward targets), deployment, realizations, dry powder, perpetual AUM, base management
fees, FRPR, FRE + FRE margin, net realizations, DE, DE/share, dividend. The Drivers tab's
supplementary sections (AUM/FPAUM by strategy) map 1:1 to the segment walks.

## Acceptance additions (run with the main gates)

A1. ☐ Every flagship fund has the full lifecycle block; step-down triggers are binary blue inputs;
      fee rate switches at the trigger; fund fees roll to the segment fee stack.
A2. ☐ Segment AUM walks tie reported EOP/average FEAUM to the dollar in actuals; flows decompose
      (flagship/perpetual/residual) with red residuals; step-down links flow through.
A3. ☐ Blended fee rates are SUMPRODUCT stacks, never a single typed rate; base-fee check row ties
      the P&L fee line to the AUM × rate build.
A4. ☐ FRE and margin computed with comp/opex ratio bands; guided items (fee holidays, comp offsets,
      crystallization schedules) carry violet guidance rows period-aligned.
A5. ☐ DE waterfall reaches DE/share through the % -to-common unit structure with the partnership-
      unit residual; dividend policy is driven, not hardcoded.
A6. ☐ Fund names, segment cuts, and targets came from the company's own materials, not this file.
