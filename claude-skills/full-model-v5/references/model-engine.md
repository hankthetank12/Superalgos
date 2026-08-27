# Model-tab engine spec

Read this in full before build-order step 3 (scaffold) and keep it open through step 9 (Model
audit). It is the complete mechanical spec for the Model tab. Formatting canon (colors, fills,
fonts, number formats, banner/border/box mechanics) lives in `references/format-spec.md` — this file
assumes it. Sector engines (retail broker, alt manager) REPLACE the revenue-engine section only;
everything else here applies to every sector.

## Table of contents
1. Adaptive grid & header scaffold  ·  2. EPS strip  ·  3. Summary Income Statement  ·
4. P&L layout (business rollup)  ·  5. %-row conventions  ·  6. Memo blocks  ·  7. Scenario memos &
toggleable overlays  ·  8. Consensus-source ladder  ·  9. Actuals (press release / Daloopa)  ·
10. Estimates (seed to consensus, then sensitize)  ·  11. Forecast mechanisms  ·  12. Market-data
blocks & TAM→share ladders  ·  13. Per-unit intensity  ·  14. Market-vs-organic bridge & seasoning  ·
15. Rate-path scaffold & NII  ·  16. Rollforwards & checks  ·  17. Up-C / two-tier tax & NCI  ·
18. Per-share discipline  ·  19. Capital & Returns module  ·  20. Balance sheet & cash flow in
estimates  ·  21. Annual columns  ·  22. Guidance rows (pointer)

## 1. Adaptive grid & header scaffold
- **Default layout**: columns A–G indent; H–I label helpers; J–K main labels (K doubles as the
  source/ticker tag column); L… one column per quarter; after a spacer, ANNUAL columns. Express this
  as two variables the whole build consumes: `label_end_col` (default K) and `first_data_col`
  (default L). A wider label block (e.g. through N, data from O) is fine when the company needs
  deeper indent (fund-level builds) — set the variables once and keep every downstream tab and
  format sweep on them. When UPDATING an existing workbook, discover and respect its layout
  (legacy models may interleave annual columns between quarters — read-compatibility only, never
  build that layout fresh).
- **History/horizon defaults** (when the user doesn't specify): all available printed quarters from
  the disclosure source (min ~12), 8–10 estimate quarters, annual columns from the first fully
  displayed fiscal year through the last estimate year. **Focal quarter** = the next unreported
  quarter; **focal year** = its fiscal year.
- Scaffold rows (gray-italic mechanical memos, centered in data columns): month-end EOMONTH chains
  (3 rows); quarter-end date; days in quarter (`=+curQEnd−priorQEnd`); annualization factor;
  fiscal-year integer (the SUMIFS key); quarter label ("1Q"/"2Q"/…); Actual/Estimate marker row.
  Where trading days matter, compute them with NETWORKDAYS off the quarter-end row.
- **Bloomberg period strings** (ONLY if BQL formulas are being written — see §8): two scaffold rows
  per estimate column derive the BQL/BDP period arguments from the banner label (e.g. from "3Q26" →
  `=+"20"&MID(<label>,3,2)&…` and `=+LEFT(<label>,2)&"FY-20"&MID(<label>,3,2)`) — never typed.
- Period banner row per format-spec (formula labels, white year separators, last frozen row).
  Gridlines off; freeze below the banner / after `label_end_col`.

## 2. EPS strip
Sits in the scaffold directly above the period banner — the at-a-glance model-vs-Street tie:
- **Quarterly model-EPS row**: `=<EPS row below>` links, bold GREEN `$#,##0.00` on a gray #F2F2F2
  band spanning the ESTIMATE columns only; label ("<Firm> Estimates") bold on gray IN the first
  column of the band. **"Annual" row** beneath: bold `=SUM(4 trailing qtrs)` (no fill), green while
  estimate, black once fully reported; each 4Q value gets a clean 4-sided thin box (two-phase).
- **Quarterly consensus row**: bold RED on the same band (label "Consensus"), with its own boxed
  Annual row. Source per the consensus ladder (§8): VAActuals links, or red hardcodes; a live-BQL
  strip is written only in a Bloomberg-alive environment and is never used for build-time ties.

## 3. Summary Income Statement (top of the Model tab)
Directly below the frozen scaffold, BEFORE the deep P&L: a compact ~30–40-row headline view — the
first thing the user sees. One row per headline: revenue lines by business, total revenues, key
expense totals, PPNR/EBITDA/FRE (whatever the sector's profit lens is), pretax income, taxes, net
income, EPS, diluted shares, 1–3 headline margins/returns, and the 2–4 marquee KPIs from Step 0.
Every cell is a **dark-green #006600 same-tab link** into the deep P&L/engines below (no drivers, no
hardcodes here); % Y/Y gray rows under the majors. Section banner "Summary Income Statement" or
"<Company> (<TICKER>)" at tier 1. The deep P&L then restates the full detail — the Summary IS is a
read surface, never a build surface.

## 4. P&L layout — business rollup with detail inside
Organize the P&L by BUSINESS, not the GAAP line-item cut, mirroring how MANAGEMENT presents the
company (Step 0 materials). Statement-level sections at C ("Revenues", "Expenses", "Profit"); inside
Revenues the deepest detail lines at G rolling to E-level business subtotals, then D "Total
Revenues". Expenses: F-level lines → D "Operating Expenses" → D "Efficiency Ratio" (gray band) with
a "# Y/Y" row. Profit: D PPNR → F Provision → D PT Income → E Taxes/Tax Rate (+" # Y/Y") → E Pref
Dividends → C Net income → C EPS → E Diluted Shares. Key statement lines sit OUT at C — the further
left, the more headline. Engines below follow the same segment cut so each P&L business line has
its engine; engine outputs feed green links up into the P&L.
- **Incremental Margins row** directly beneath the PT-margin block: `=Δ pretax income / Δ revenue`
  vs the same quarter prior year, gray computed both sides — every model gets one; it is the fastest
  tell on whether estimates respect the business's incremental economics.
- **Core / adjusted parallel P&L (only when the company leads with one)**: when the company's
  headline basis is "Core"/"Adjusted" (core revenue, core NIE, core PPNR, adjusted EPS), build the
  parallel rows — non-recurring lines isolated (marks, restructuring, TRA-type items, currency
  strategies) with the adjusted stream computed from the core components, and run the EPS strip and
  consensus ties on the company's headline basis. Skip entirely when the company reports plain GAAP.

## 5. %-row conventions
- **% Y/Y** beneath every level line (gray computed in actuals; the blue input in estimates for
  YoY-driven lines). **% Q/Q** beneath the % Y/Y on DRIVER lines and engine levels — always gray
  computed both sides.
- **"# Y/Y"** (point delta) beneath every RATIO line — computed `=(cur−prior-year)` gray; where the
  ratio is input-driven, the Δ IS the input. Never a %Y/Y growth row under a percentage line.
- **"$ Y/Y" / "$ Q/Q"** dollar-delta rows beneath balance/stock lines where the DOLLAR change is the
  story.
- **Seasonality rows** (red italic): under % Q/Q on seasonal drivers — `=AVERAGE(prior 4 same-quarter
  %Q/Q)` placed in estimate columns as the benchmark the input is set against.
- **% M/M / # M/M monthly sub-blocks** on monthly-disclosed KPIs: labeled `% M/M` (and `# M/M` where
  levels matter) with Month 1/2/3 rows, plus a monthly `% Y/Y` sub-block. **Each month row gets a
  `Seasonals` row (`=AVERAGE(prior years' same-month value)`) and a `Vs Normal Seasonality` delta
  row beneath it** — the intra-quarter nowcast-vs-norm lens; both red italic.
- **2Q-stack rows** (gray): for young products where Y/Y is meaningless, a 2-quarter stacked growth
  row (`=cur/two-quarters-ago−1`) alongside % Q/Q.

## 6. Memo blocks
Standardized sanity-check frameworks, labeled `Memo: <name>` at F with a G-level stack; every
`Memo:` header label carries the #CCCCFF fill. Memos are informational (gray/black with blue-on-
yellow memo inputs) — the live input lives in the engine, never in a memo.
- **Ratio memos** (Memo: Comp Ratio; Memo: Transaction-Based Expenses): numerator level, denominator
  level, the ratio, "# Y/Y", boxed Annual pair.
- **Competitor read-across memo**: when an undisclosed intra-quarter driver can be triangulated from
  peers disclosing earlier/more often — each peer's metric as its own labeled row (level + % Q/Q),
  proxy-adjustment rows, and a bolded derived-signal row. Source every figure. The model's input
  stays a blue assumption set WITH the read-across, never linked to it.
- **Alt-data memo**: third-party data that leads a disclosed KPI (downloads, web traffic, card data)
  — Month 1/2/3 + Total, % Y/Y / % Q/Q, Annual pair, monthly % Y/Y sub-block; staged on its own tab
  when history is long (see §12 staging).
- **Normalized-earnings memo**: restate a rate/mark-distorted line at a normalized blue input; show
  normalized level, margin, and headline-vs-normalized gap.
- **RIF / cost-action memos** under the comp line: annualized comp × reduction % → impact.

## 7. Scenario memos & toggleable overlays
- **Inline scenario memos** (default): stress cases as labeled MEMO rows under the line they stress
  (`Memo: <line> — Downside ('08-style)` / Base / Bear) — informational, never feeding the live P&L.
  Typical: credit losses at prior-crisis severity, flow downside, buyback paths.
- **Toggleable thematic overlays** (when Step 0 surfaced a material thematic upside/downside the
  analyst wants mechanized): a labeled block computing the uplift bottom-up (e.g. adoption % ×
  base exposed × allocation × (activity multiple − 1) × take rate, per product), a blue **Phase-in**
  ramp row, a Total, and a blue **on/off (1/0) input row**; the engine adds `overlay total × on/off`
  into the affected line. Base case ships with the toggle at 0 unless the user says otherwise, and a
  `Memo: overlay EPS impact` row shows the delta. This is the sanctioned way for a scenario to feed
  the P&L — everything else stays informational.
- **New-initiative valuation stub** (optional, parked beside the engine): run-rate revenue × multiple
  × haircut/tax × ownership → per-share value contribution — informational.
- Sidecar what-if TABS (a separate tab feeding one blue driver) are allowed when the analysis is too
  big for a memo block — same toggle discipline; default off. See `references/driver-grammars.md`.

## 8. Consensus-source ladder (applies to the EPS strip, estimate seeding, Drivers, Qtr, Mini Model)
Resolve the Street source ONCE at scoping and use it everywhere:
1. **A VAActuals / consensus tab in the workbook** → link consensus rows to it (red; `/100` on
   whole-percent ratios). This is the normal case and the only source that supports build-time
   value verification.
2. **No consensus tab** → red HARDCODED consensus snapshot transcribed from what the user provides
   (paste, screenshot, message); state the values and their as-of date in the reply.
3. **Bloomberg BQL/BDP formulas** are written ONLY as clearly-flagged refresh-on-open formulas —
   they cannot evaluate in this build environment, are NEVER the Model's spine, and are NEVER used
   to verify a tie. Appropriate on the 1 Pager / NTM PE (they self-heal on the user's desktop) and,
   if the user asks, as a dormant consensus strip beside the hardcoded one. No canary-cell
   requirement in a Bloomberg-dead environment.
Market data has no consensus — seed market-volume %Y/Y to a transparent stated assumption and FLAG
it; back-solve the capture/share input so the revenue line still ties consensus at seed.

## 9. Actuals must tie to the dollar
- **Default**: reported totals are BLUE HARDCODES from the press release in actual columns, one RED
  PLUG per block so components reconcile to the dollar; NI ties to reported NI-to-common with a red
  $0 tie-memo row. Tag every actual row's source in the K column ('Press Release', 'Presentation',
  'Monthly', 'xls Supp', '10-Q'); use 'Est per Claude' on any figure the agent estimated.
- **Daloopa mode (opt-in)**: when the workbook has a Daloopa staging tab (or the user asks), column
  A holds the Daloopa series ID per row and actual columns pull
  `=INDEX(Daloopa!$D:$XFD,MATCH($A<r>,Daloopa!$D:$D,0),MATCH(<periodKey>,Daloopa!$1:$1,0))` in dark
  green #006600, with blue hardcodes only where no series exists. Never guess series IDs; the tie
  discipline (plugs, $0 memos) is unchanged. Do not build Daloopa wiring when no Daloopa surface
  exists.

## 10. Estimates — seed to consensus, then sensitize
Every estimate level is a formula off a flexible input; every seed back-solved from the matching
consensus figure (`%YY_seed = consensus / SameQtrPriorYr − 1`; ETR back-solved from consensus NI;
diluted shares = cons NI / cons EPS). Plugs & reconciliation lines are hardcoded blue-on-yellow
inputs in estimate columns (a live-link plug neutralizes drivers). Never let an estimate column
contain a blue non-yellow hardcode; never yellow-fill a formula cell. Re-run the wiggle test after
converting any plug.

## 11. Forecast mechanisms — reference
- **Operating-driver lines**: `volume × price × days / scale`; driver levels `=SameQtrPriorYr*(1+%YY)`
  with blue %YY below.
- **Market-pool × capture**: revenue = market volume (tracking block) × $-capture rate; capture gray
  computed in history, blue LEVEL input in estimates, back-solved to consensus at seed. With a
  TAM→share ladder the share row plays the capture role; detail lines beneath become informational.
- **Vintage roll-on/roll-off yield engine** (spread books with repricing lag): split float (rides the
  rate path) vs fixed; roll-off yield = trailing average of the new-money yield from N years back
  (N = book duration, `=AVERAGE` over the 4 quarters ending N years prior); roll-on = current
  new-money yield; portfolio yield $ = `prior + roll-on × additions − roll-off × maturities`, /4
  quarterly. Symmetric on asset yields and cost of funds. History must reach back N years — extend
  or flag.
- **Headcount × comp-per-employee** (default for people businesses): employees roll `=prior + net
  new hires` (blue); comp/employee `=prior × (1 + %Q/Q input)` with a Seasonal benchmark row (Q1
  resets, Q4 true-ups); comp = employees × comp/employee / scale; productivity memos beneath; seed
  so LTM comp ratio ties consensus/guided.
- **YoY%-driven lines**: `=SameQtrPriorYr*(1+%YY)`, blue %YY input. **Ratios**: Δ/level inputs only.
- Subtotals: explicit cell sums `SUM(cell,cell,…)` — never `=SUM(range-with-%-rows)`.
- **EPS basis**: match the consensus basis before any GAAP-vs-operating bridge; never divide model
  EPS by a gap row.
- Advanced grammars (cohort triangle, attach engine, event calendar, staging feeds):
  `references/driver-grammars.md` — scan its menu during Step 0 KPI selection.

## 12. Market-data tracking blocks & TAM → share ladders
When a revenue engine rides MARKET data, build a tracking block with full provenance directly above
the line it drives:
- Region/market sub-header; **Month 1/2/3 rows + a quarterly Average (or Sum) row**; source-URL row
  (italic gray) under the block header; **column-K tags** — short source tag ("SIFMA", "OCC") on
  hand-tracked rows, the Bloomberg ticker string on live rows.
- **Every web-sourced hardcode carries a cell note** (source + URL + derivation). Unsourced gaps
  stay BLANK blue inputs — never interpolate silently; flag them.
- **Staging tabs**: long histories (Bloomberg BDH, alt-data feeds, data-team extracts) live on a
  dedicated staging tab — date + value columns, header naming the series — and the Model block pulls
  by month-end date (`VLOOKUP`/`XLOOKUP` on the EOMONTH scaffold rows). Keep raw history off the
  Model tab. Where a live source is unavailable, leave rows blank/erroring with a note — never paste
  static numbers pretending to be live.
- Dash-tolerant guards (`IFERROR(...,"-")`, `IF(x="","-",…)`) on every computed row over gappy
  history.
- **TAM → share ladder**: (1) industry pool level (sourced, tracked); (2) company share row — gray
  computed in history, blue LEVEL input in estimates; (3) company line `=share × pool`. Optional:
  competitor share table (named players, sourced, K-tags), read-across memos, FX row for
  international TAMs.

## 13. Per-unit intensity blocks
For any business with a countable unit base (accounts, clients, members, subscribers, seats): express
every major balance and activity line as a per-unit intensity and FORECAST the intensity — 
`<Line> per <unit>` block (Month 1/2/3 where monthly, EOP or annualized total, % Y/Y, % Q/Q,
Seasonality where seasonal); in estimates the intensity carries the blue input and the line rebuilds
as `intensity × units`. Typical set: balance per unit, activity per unit (annualized), monetization
per unit. Derived-only intensities stay gray with a small scaffold above making the division
auditable.

## 14. Market-vs-organic bridge & balance seasoning
Any client balance that moves with markets (client equity, AUM, custody assets) gets its change
DECOMPOSED — never forecast such a balance with a single %Y/Y:
- **Market Assumptions block**: the relevant index (ticker as the sourced row label), Month 1/2/3
  levels, quarter row, % Y/Y / % Q/Q, % M/M sub-block; actual months blue from published levels,
  estimate months blue % M/M (or flat-level) inputs.
- **Decomposition** beneath the balance: `# M/M from market returns` (= BoP × levered index return),
  `# M/M total change`, `# M/M Change ex Markets` (organic) with quarterly total, % Q/Q, Seasonality.
  The compact quarterly variant: `BOP + NNA/flows + Market (residual red in actuals; = BoP × return
  input in estimates) = EOP`, tying the EOP level with a check.
- **`Memo: <Balance> Seasoning Framework`** (#CCCCFF header): implied-EOP bridge rebuilding the
  balance bottom-up (BoP; less non-market components; × levered market return with leverage ratio ×
  index %Q/Q + alpha input; plus new-unit funding = new units × initial funding; plus backbook adds;
  plus non-market components back) → **Implied vs Modeled EOP check row** (red italic; small
  persistent gaps are the seasoning signal, large gaps a build error).

## 15. Rate-path scaffold & NII
When floating-rate exposure or a cuts/hikes narrative matters:
- **Live-rates block** heads the NII engine ("Rates" sub-section): one row per benchmark with Month
  1/2/3 + a quarterly Average row and a Sequential-change row; the ticker string sits as a row label
  beside each series (plus the K-tag). Actual months hardcode from published fixings.
- **Rate path**: per-month Δbps blue inputs (−0.25% on cut months), a cumulative-change counter, a
  monthly chain `=prior + Δ`, and the quarterly AVERAGE (which drives yields, not EOP).
- Floating lines = floating balance × (rate average + spread); pair with a fixed/floating exposure
  split row. Betas stay for administered-rate products.
- **Blended multi-currency mix**: per-currency rate rows, blue mix weights, blended rate =
  Σ(mix × rate); product betas expressed as cum-beta / %-of-blended rows.
- **Rate-paying vs non-rate-paying split** where only a subset earns/pays full yield — drive interest
  off the sensitive piece with a `Memo: % of balances earning full yield`.
- **NII presentation bridge**: engine NII → Less/Plus each presentation item → **Reported NII** (the
  consensus-tied line) with % rows and the Annual pair. Never let the P&L link an unreconciled
  engine total.
- Optional informational blocks: alternative rate paths (Alt 1 / Alt 2 curve blocks + scenario
  NII/EPS-impact memo rows), rate-sensitivity ladder (FFR bands × NII/EPS impact).

## 16. Rollforwards & checks
- **Every stock rolls forward**: AUM, invested assets, deposits, book equity, share count —
  `BoP (=prior EoP) + inflows − outflows ± market/other = EoP`, each flow driven by its own input.
  Never let a balance jump between quarters without a rollforward. Split inflow sources (captive /
  third-party / new initiatives) as separate rows.
- **Check rows at every seam** (`Check: <what ties>`, red italic, must read 0/"-"): rollforward vs
  flows block, sum of segments vs consolidated, equity build vs balance sheet, capital generated vs
  deployed+returned. A capital-feasibility check is mandatory for balance-sheet businesses. Any
  nonzero check fails the build.

## 17. Up-C / two-tier tax & NCI (only when the structure applies)
Never blend rates when the public co owns a slice of an operating partnership: Tier 1 (op sub): PT
income → sub tax (own rate + # Y/Y) → NI to members. Tier 2 (HoldCo): NI to members × ownership %
(average + annual rows; rolls with buybacks/exchanges) → less HoldCo tax → **NI to common** (the EPS
numerator). **NCI cross-check block**: implied NCI rebuilt independently with a red Plug row ~0.
Public-ownership share block in the share section; dividend block (`DPS input × shares = divs paid`)
feeding the equity roll. A simpler unit-structure variant (alt managers): DE × %-to-common off
common-vs-total-units, partnership units as the red residual — see alt-manager-engine.md.

## 18. Per-share discipline
Every segment earnings stream gets a per-share row (`=stream / diluted shares`, gray, beneath its
Annual pair). Share count: seed diluted shares from consensus (`cons NI / cons EPS`); optionally add
the share-count roll engine (`BoP − repurchased (=$ buyback / avg price) + issued (SBC) = EoP`,
weighted-average feeding EPS) — then back-solve buyback $ so shares tie consensus at seed, with a
check row. Never approximate diluted shares as an ad-hoc average.

## 19. Capital & Returns module (default for brokers, banks, asset managers; recommended everywhere)
After the Tax/NCI section: **payout block** — dividends per share × shares = aggregate dividends;
$ repurchases; total dollar payout; dividend/repurchase/total payout ratios (% of operating NI, blue
italic); **returns block** — ROA and ROE (annualized, `/avg equity`), ROTCE, GAAP and adjusted
variants, each with Annual + # Y/Y; **book value block** — BVPS and TBVPS with % rows; TCE/TA;
**minority-interest %** memo where NCI exists; **operating-leverage rows** (YoY and YTD: core
revenue growth − core expense growth); **change-in-share-count** row. All gray/black computed; the
only inputs are DPS and buyback $ (or the share roll's inputs).

## 20. Balance sheet & cash flow in estimates
- Actual BS columns: blue hardcodes (or Daloopa pulls) by line, roll-up sums, balance check row.
- Estimate BS: rebuild off drivers, not %Y/Y — client-driven lines as %-of-their-driver (receivables
  as % of margin loans, payables as % of client cash…), total assets scaled to the driven balance
  base, **liabilities as the red plug** (assets − equity), equity through its roll (BoP + NI − divs
  − buybacks ± other), preferred/NCI carried, `Total L+E = Total assets` green check. BS-driver
  ratio rows may park in a labeled helper block.
- **Basic cash-flow calc**: NI + D&A + SBC ± working-capital plug → CFO tying the reported line
  ('Actuals' tag); $ Y/Y and Annual rows. Deeper FCF only where the sector engine needs it.

## 21. Annual columns
Flows `=SUMIFS($<first_data_col><row>:$<last><row>, <fiscal-year scaffold row range>, <yearCell>)`;
EOP stocks link the 4Q value; ratios recompute from annual numerator/denominator; averages via
AVERAGEIFS; ADV-type metrics = annual volume / annual days. %Y/Y columns off the prior annual column.
**The SUMIFS range is ONE fixed range, identical in every annual column and every row — never
patched per column.** It must cover every quarter of every displayed annual year (it may start at
the earliest displayed year's 1Q and run through the spacer harmlessly). A range that stops short of
the last quarter column silently drops quarters. When quarters are appended, extend the range
everywhere in one pass and re-verify.
Annual + % Y/Y boxed pairs also live as ROWS under every P&L and engine subtotal (format-spec).

## 22. Guidance rows
If a "Guidance" tab exists, guidance rows are RESERVED during the P&L skeleton (fresh build) or
inserted via `scripts/insert_guidance_rows.py` (existing model). Violet #7030A0 italic, verbatim,
period-aligned, excluded from border sweeps, no cell notes. Full mechanics:
`references/guidance-overlay.md`. No Guidance tab → skip silently.
