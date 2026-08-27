# Gap analysis: full-model-v5 skill vs the user's three FINISHED models

The user (a buyside analyst) runs the `full-model-v5` skill to scaffold a full quarterly earnings
model workbook, then manually builds on top until it reaches the "finished" state. Three finished
workbooks were provided as ground truth: **HOOD_Model.xlsx** (Robinhood — closest to skill output +
heavy user additions), **BX_Mini_Model.xlsx** (Blackstone — full alt-manager build), and
**IBKR_Model.xlsx** (Interactive Brokers — the analyst's LEGACY house model, Arial 10, predating the
skill; the house style the skill tries to encode). The goal: make the skill's first-pass output land
as close to the finished state as possible.

## A. Whole tabs the finished models contain that the skill NEVER builds

1. **"1 Pager" risk/reward + relative-valuation dashboard** (HOOD + BX, identical B1:O64 layout).
   Bear/Base/Bull EPS × multiple grids for TWO out-years; base EPS green-linked to Model annual EPS,
   Street EPS red-linked; share-price targets, Upside/Downside, R/R (for LONG) Base & Upside ratios;
   Key stats block of Bloomberg BDP/BDH pulls (price, mkt cap, EV, 90D ADTV, 90D realized vol,
   implied 1-day move, SI % float, 90D correlations to SPX and GS L/S factor baskets — GRVL, Cycl/Def,
   Momo, Quality, Crowded); relative-multiple grids (stock P/E ladder ÷ SPX and QQQ multiple ladder)
   with blue-on-yellow "1 St. Cheap / Average / 1 St. Expensive" sigma thresholds; trailing stock
   performance (YTD/1w/1m/3m/2y); IR contact block.
2. **"NTM PE" valuation-history tab** (HOOD + BX, identical): 3 Bloomberg BDH spills (subject +
   2 indices, BEST_PE_RATIO 1BF), date-aligned via VLOOKUP, relative multiples, median/±1σ bands
   (~6,500 rows). Feeds the 1 Pager thresholds. The user wrote a "Replication Guide" tab documenting
   how to copy this pair between models (3 touch-points: ticker cell, 2 EPS links) — proof they
   re-create it every time and want it automated.
3. **Alt-data staging tabs**: "Sensor Tower" (app downloads/MAU), "Relay Data" (2,036-row card/visit
   feed from the Walleye internal data team, VLOOKUP'd into the Model by month-end date), "Citadel
   Monthly Index" (peer read-across). The skill mentions alt-data memos but not the staging-tab +
   VLOOKUP-by-date plumbing pattern from a data-team feed.
4. **Thematic what-if tabs**: "Agentic impact" (HOOD) — standalone TAM/what-if engine (adoption % ×
   portfolio allocation × activity multiple × take rate, per product, with sensitivity columns);
   "EU Other country TAM" — international-expansion driver build (Sensor Tower international MAUs ×
   conversion → international customers feeding the Model). The skill's "scenario memo" concept is
   too small for these; they are separate side tabs that FEED a driver or quantify an upside.
5. **"PE Flagship Fundraising" / "RE Flagship Fundraising"** (BX): per-fund fundraising research tabs
   supporting the Model's fund engines.
6. **Guidance tab** (BX): flat list (Date Given / Target Period / Line Item / Verbatim quote /
   Source citation) built from AlphaSense-style citations — matches the skill's guidance-overlay input.
7. **IBKR legacy**: "Daloopa" staging tab + "Monthly" tab + "JBCM vs. VA" comparison tab.

## B. Architecture divergences on the Model tab

1. **Actuals ingestion via Daloopa tag IDs** (IBKR): column A holds a Daloopa series ID per P&L/BS
   row; actual columns are `=INDEX(Daloopa!$D:$XFD, MATCH($A<r>,Daloopa!$D:$D,0), MATCH(<period>,...))`
   pulls from a Daloopa staging tab. Actuals REFRESH mechanically; hardcodes only where Daloopa lacks
   a line. The skill mandates hand-keyed blue hardcodes from the press release — much slower to
   update and no audit trail. (HOOD/BX still hand-key blue, but the user's end-state IBKR model
   automates it; K/N-column tags name the source: 'Press Release', 'Presentation', 'Monthly',
   'xls Supp', 'Used cons tax rate', 'Est per Claude'.)
2. **Consensus display rows pull from the workbook's own consensus surface** — `=VAActuals!…` red
   rows, or `='Drivers HOOD'!AC306` (the Model reads Street KPIs back from the Drivers tab staging!)
   — and the EPS-strip consensus row in HOOD is **hardcoded red values**, not live BQL. The skill
   mandates live `BQL(...)` pulls with derived period strings; in the user's no-Bloomberg build
   environment those produce dead formulas, so the finished models use VAActuals links / hardcodes.
   BX consensus strip: `=VAActuals!AO232` + red hardcodes.
3. **Fund-level engines for alt managers** (BX): each flagship fund (BCP VIII/IX, BREP IX/X, Asia,
   Energy…) gets a ~50-row lifecycle block: fee-rate assumptions (investment-period rate, step-down
   rate as static blue inputs in the label area) → Commitments walk (BOP + New Closes[residual red in
   actuals / blue input fwd] = EOP[press-release blue]) → Capital Invested walk + Dry Powder + %
   Called → Realizations walk + % returned → NAV walk (BOP + deployed − realized + market change
   [red residual, % Chg blue input fwd] = EOP) → Total Value + MOIC → FPAUM walk with a **"Step-Down
   Trigger (enter 1 in trigger qtr only)"** binary input row, cumulative post-step-down flag, step-down
   impact → Mgmt fees = FPAUM × IF(post-stepdown, stepdown rate, investment rate)/4. Perpetual
   vehicles (BXGP/BIP/BXINFRA/BXPE) carry per-product AUM + fee-rate rows, blended via SUMPRODUCT.
   Segment AUM Walk: BOP + Inflows(% of BOP) + Outflows(% of BOP) [+ Flagship/Perpetual/Non-flagship
   flow decomposition with red residual] + Realized(% of BOP input) + Market(% of BOP input) +
   Stepdown(link) = EOP FEAUM; Avg FEAUM; Memo: Total AUM with FEAUM-%-of-total. The skill's
   asset-manager sector variant is one sentence ("AUM roll-forward × fee rate → FRE") — nowhere near.
4. **Cohort/vintage triangle** (HOOD, `Memo: Per account Build / Cohort Analysis`): quarterly cohort
   matrix — one row per cohort (1Q21…4Q28), retention/decay multipliers (100%→70%→60%→50% blue
   diagonal inputs), New Customers diagonal, per-cohort contribution roll-up → Calculated NNA vs
   Actual NNA with plug, Modeled vs Consensus rows. The skill mentions "cohort memos" in passing;
   the real thing is a triangular engine with its own grammar.
5. **Subscription attach engine** (HOOD Gold): penetration rate (# Q/Q input) × funded → subscribers;
   New-user attach rate vs Backbook attach decomposition (# Q/Q modeled with red residual,
   as-%-of-backbook gray); SLICE alt-data % chg check row; Cost per user memo.
6. **Deal/event-driven blocks**: IPO Access (deal size × HOOD allocation × fee rate); event-contract
   calendar (World Cup matches × contracts/match; NFL Normal/Marquee/Playoff/Superbowl multipliers;
   "NFL as % of Fall Sports Volume" [K-tag: 'Est per Claude'], assumed market share, "Cases >>>>"
   scenario input rows); "Trump Accounts" placeholder line.
7. **Thematic uplift engine WITH on/off switch** (HOOD Agentic memo on the Model tab): per-product
   uplift = volumes × adoption × portfolio-allocation × (activity multiple −1) × take rate, a
   "Phase in" ramp row, a Total, and an **"on / off" blue input row** — i.e., a toggleable scenario
   overlay, more mechanized than the skill's "informational only" scenario memos.
8. **New-initiative valuation mini-block** (HOOD "Rothera Valuation >>>>>": revenue run-rate ×
   multiple × haircut/tax × ownership → per-share value contribution) parked beside the engine.
9. **Seasonals + "Vs Normal Seasonality" rows** under monthly % M/M and # M/M blocks (each month's
   seasonal norm = AVERAGE of prior years' same-month, plus a delta row) — the intra-quarter
   nowcast-vs-normal lens. Skill has Seasonality rows on %Q/Q only.
10. **"2Q Stack" rows** (2-quarter stacked growth, gray) for young products where Y/Y is meaningless
    (prediction markets).
11. **Alt 1 / Alt 2 rate-path scenario columns** (IBKR legacy): parallel FTE NII / Core PPNR /
    Operating EPS variants under alternative rate paths — skill mentions alt curve blocks but not
    the chained Alt-EPS variant rows.
12. **Core vs GAAP duality** (IBKR): Core fee income / Core NIE / Core PPNR / Core revenue (+ ex-Sec
    lending variants) with non-recurring lines isolated (currency diversification, MTM, TRA
    remeasurement, restructuring). Skill covers adjusted bridges but not the "Core" parallel P&L.
13. **Simple Income Statement** (BX): a compact ~35-row linked summary IS at the top of the Model tab
    (dark-green #006600 same-tab links into the full IS below) — headline view before the detail.
    HOOD similarly opens with a "Summary Income Statement".
14. **Capital & returns depth** (IBKR/HOOD): payout-ratio block (dividend/repurchase/total % of op NI),
    BVPS/TBVPS with growth, TCE/TA, ROE/ROTCE GAAP + adjusted, Minority Interest %, YoY/YTD operating
    leverage rows, "Change in share count" row; HOOD adds ROA/ROE blocks + Incremental EBITDA margin.
15. **Balance sheet in estimates** (HOOD): Total assets scaled off IEA growth; liabilities as red
    plug; equity roll (BOP deficit + NI − divs − buybacks); convertible-note lines; BS-driver ratios
    parked in a far-right scratch column. Cash-flow section: NI + D&A + SBC ± WC plug ties to reported
    CFO ('Actuals' K-tag).

## C. Formatting-convention mismatches (skill says X, finished models do Y)

1. **Fonts**: skill mandates Calibri 9 everywhere. HOOD/BX conform; HOOD's Revisions tab is Aptos
   Narrow 9 (per the older standalone skill); legacy IBKR is Arial 10/9/8 (grandfathered).
2. **Input fill**: skill #FFFFCC; HOOD/BX use #FFFFCC (IBKR legacy uses #FFFF99). OK.
3. **Sub-section banner**: skill says #FFF2CC gold at C. HOOD actually uses **#FFEA8F** fills on
   D-level product headers (Options/Equities/Crypto/Prediction Markets); BX uses theme-gold (bgth7)
   at C ('Flagship Funds', 'Perpetual', 'AUM Walk', 'PnL') and theme-red-ish (bgth5) at D for
   per-fund headers — i.e., a THIRD banner tier (fund-level) exists in BX.
4. **Guidance color**: BX uses #7030A0 italic 'Mgmt Guidance (source, date)' rows (matches skill) —
   but ALSO drops violet guidance values inline into Annual #Y/Y row columns. HOOD uses **#800080**
   purple 'Guide' rows placed under Annual pairs. IBKR's Monthly tab uses #7030A0 for MoM/YoY
   computed rows (collision: violet ≠ guidance there).
5. **Seasonality rows**: skill says brown #833C0C memos; HOOD uses **red #FF0000** for most
   Seasonality rows and #A66500 brown for a few — inconsistent, but red is dominant in the live model.
6. **Grays**: three grays coexist (#7F7F7F italic %, #808080 helper, #4D4D4D bps memos, plus #777777
   in HOOD). Skill only defines #7F7F7F.
7. **Green shades carry meaning**: #008000 for cross-tab/cross-row links, **#006600 dark green** for
   VAActuals links (BX Mini Model, BX Simple IS, 1 Pager Model links). The skill bans green-to-
   VAActuals outright — the finished BX/HOOD workbooks link actuals to VAActuals in green
   everywhere (see D.1).
8. **Red fills as attention flags**: blue inputs on #C00000/#FF0000 fills mark cells needing update
   (BX non-flagship flows, common shares) — a live workflow convention the skill doesn't know.
9. **Number/label hygiene**: finished models are full of typos ('Tale Rate', 'Crrypto',
   'Seasonalirt') — skill output is cleaner; not a gap, just noise to ignore when learning from them.

## D. Downstream-tab divergences

1. **Mini Model**: the skill mandates SELF-CONTAINED (blue hardcode actuals, NO VAActuals/Model
   links, no green). Both finished mini models violate this by design: actual years are **green
   links to VAActuals** (`=VAActuals!BT38` in #006600 / #008000), some estimate-year TOTALS also link
   to VAActuals (totals pinned AT consensus) with an "Other / reconciling" residual row absorbing
   the wedge, plus a blue "Consensus reconciliation (VA roll-up)" input row; drivers are blue-on-
   yellow inputs; red Street memo rows; a "Checks & Sources" section (revenue component check, NI
   tie to VA); "Base Case" scenario label above year headers. This matches the user's newer
   standalone mini-model skills (v7-x: "actuals link DIRECTLY to VA") — full-model-v5's mini-model
   reference has drifted from the user's current preference.
2. **Qtr / Drivers / Revisions**: finished versions conform closely to the skill (they came from it).
   Qtr uses NOT(ISNUMBER()) guards vs the skill's IF(...="") — same effect.
3. **DCF**: absent from all three finished workbooks (BX has none; HOOD has none — the 1 Pager +
   NTM PE serve as the valuation layer instead). The skill builds a DCF every time; the user's
   day-to-day valuation surface is the 1 Pager/NTM PE pair.

## E. Workflow / process gaps

1. **Bloomberg-dead environment**: skill demands live BQL/BDP formulas + canary. Claude's build
   environment can't evaluate them; finished models show the user replaced strip consensus with
   VAActuals links or hardcodes. Skill should prefer VAActuals when present and write BQL only as
   documented-but-dead formulas (or on the 1 Pager where they self-heal on the user's machine).
4. **Maintenance loop absent**: the skill describes a one-shot build. The finished models are LIVING
   workbooks — monthly ops updates, new quarters appended, Old/New snapshots rolled, guidance
   vintages stacked, cells flagged red for follow-up. No skill section covers "update mode": append a
   quarter, roll the focal column, restate seasonals, refresh Daloopa/Monthly, re-snapshot Revisions.
5. **Model tab column-layout variance**: HOOD label cols B–K data from L; BX label cols B–N data from
   O; IBKR data from E with interleaved annual columns. The skill hard-codes A–K/L… — should be
   presented as a default, not an absolute, and the interleaved-annual legacy layout acknowledged for
   compatibility reads.
