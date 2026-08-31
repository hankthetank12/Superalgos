# Retail Broker Engine (v4)

Sector reference for RETAIL BROKERS — distilled from three live audited builds: **IBKR** (Interactive Brokers — commission broker, global multi-currency NII, Up-C/NCI), **HOOD** (Robinhood — PFOF/take-rate broker, multi-product transactional stack incl. crypto and prediction markets, subscription revenue), and **BULL** (Webull — capture-rate broker, guidance-overlaid, DCF-chained). Read this whole file before building any retail broker (online broker, neobroker, discount broker, trading app). Everything here layers ON TOP of the main SKILL.md conventions (colors, banners, Annual pairs, monthly-in-quarter, SUMIFS, audit) — this file specifies WHAT to build for a retail broker and the broker-specific engine grammar, not the formatting system.

## The retail broker identity

Every retail broker model is the same five-layer cascade. Build the layers in this order because each feeds the next:

```
1. USER FUNNEL      downloads → registered users → funded accounts (the unit base)
2. ASSET ECOSYSTEM  customer assets = f(accounts, net deposits, market)  (the balance base)
3. TRANSACTION REV  per product: volume/pool × share × per-account activity × take/capture rate
4. NII              balance stack (% of assets) × yield stack (% of policy rate / betas)
5. MONETIZATION+    other revs (subs, PFOF, fees), expenses keyed to revenue & funnel, capital return
```

Revenue = (3) + (4) + (5); every line in each layer must express itself **per funded account** (per-unit intensity discipline from the main skill) and every market-sensitive balance carries the **market-vs-organic bridge**. The funnel is the master driver: accounts drive per-account intensities everywhere below.

## Layer 1 — User funnel & funded-account build

Section banner "User Build" (or "Operating Metrics & KPIs"). Sits immediately below the P&L, ABOVE the transaction engines, because everything downstream is per-account.

- **Alt-data top-of-funnel memos** (informational, `Memo:` CCCCFF headers, staged on their own tabs if history is long): app downloads (Sensor Tower) and DAU/visit data (SLICE, SimilarWeb) with Month 1/2/3 + Sum, % Y/Y, % Q/Q, and monthly % M/M sub-blocks. These LEAD funded-account adds — the read the analyst uses to set the net-adds input intra-quarter. K-column source tags on every row.
- **Registered users** (where disclosed, e.g. Webull): Month 1/2/3 (K:"Monthly") → EOP, % Y/Y, % Q/Q, % M/M sub-block. Funded/registered conversion is a useful gray memo ratio.
- **Funded accounts / funded customers — the unit base.** Monthly rows → EOP level, then the FULL %-row stack: % Y/Y, Seasonality, % Q/Q, **# Y/Y and # Q/Q** (net adds in units — the dollar-delta rule applied to units), plus % M/M and # M/M and monthly % Y/Y sub-blocks. Forecast via a blue net-adds input (# Q/Q) or % M/M path, set against the alt-data memos.
- **Funded-customer rollforward** (when the company discloses the components — HOOD pattern): `BOP + New funded + Resurrected + Acquired (M&A) − Churned = EOP`, each component its own row (K:"Presentation"), churn expressible as a % of BOP (gray memo). This is the rollforward-discipline rule applied to the unit base; a check row ties it to the EOP level above.
- **Engagement**: MAU (and DAU where available) with `MAU as % of Funded` (# Y/Y, # Q/Q, Annual) — the engagement ratio that leads activity-per-account.
- **ARPU** (total net revenues / average funded accounts, annualized): gray computed both sides with % Y/Y / % Q/Q — the summary monetization intensity everything else decomposes.
- **Average accounts** row (`=AVERAGE(BoP,EoP)` or monthly average) — the denominator for all per-account intensities; build it once here, link everywhere.

## Layer 2 — Customer asset ecosystem

Section banner "Platform Assets" / "Customer Assets". The balance base for NII, asset-linked fees, and the margin book.

- **Customer/platform assets (EOP)**: Month 1/2/3 → EOP, full % stack + % M/M sub-block. NEVER a single %Y/Y forecast — always the market-vs-organic bridge (main skill § Market-vs-organic bridge):
  - **Market Assumptions block**: the tracking index (QQQ and/or S&P 500 as sourced rows) with Month 1/2/3, % Y/Y, % Q/Q, monthly % Chg rows; actual months blue from published levels, estimate months blue % M/M inputs.
  - **Net deposits / NNA**: Month 1/2/3 (K:"Monthly") → quarter total, % Y/Y, Seasonality, % Q/Q, plus **% NNA annualized** rows (monthly and quarterly: net deposits ÷ BoP assets, annualized) — the organic-growth lens the input is set in. Per-account net-deposit / cohort memos (HOOD pattern) where the disclosure supports them.
  - **Customer Asset Rollforward**: `BOP Assets + Deposits (= NNA % input × BoP) + Market Returns (= market return % × BoP) = EOP Assets` — the BULL pattern; the NNA % and the market-return link are the two drivers, and EOP ties the level block with a check.
- **Assets per account** intensity block (equity per account, $000s) with % Y/Y / % Q/Q — separates unit growth from wallet deepening.
- **Client credit balances / cash** split where disclosed (IBKR: FDIC-program credits vs credits held at broker, % of total mix row; credits per account intensity). These feed the NII balance stack.

## Layer 3 — Transaction revenue engines (one per product)

Section banner "Transaction Based Revenues" (or "Trading Revenue Engine"), one sub-section (#FFF2CC) per product: **Equities, Options, Crypto, Prediction Markets / Event Contracts, Futures** — whichever the company has. Every product block follows the same grammar; the monetization unit differs:

| Product | Volume unit | Rate unit | Revenue |
|---|---|---|---|
| Equities | notional $ volume (ADTV × days, or total) | capture/take rate (bps of notional) | volume × bps |
| Options | contracts (mm) | rate per contract ($) | contracts × $/contract |
| Crypto | notional $ volume | take rate (bps) | volume × bps |
| Prediction markets | contracts | take rate ($/contract or bps) | contracts × rate |
| Commission model (IBKR) | cleared trades (DARTs × days) | commission per cleared DART ($) | trades × commission |

**The per-product block, in order (top → bottom, drivers above the line they build):**
1. **Industry pool** (where one exists): OCC total options volumes for options; industry crypto volumes (the Block / exchange-volume data) for crypto; Kalshi + total event-contract volumes for prediction markets. Month 1/2/3 + quarter total, sourced per the market-data rules (source-URL row, K-tags, cell notes), % M/M sub-block.
2. **Company market share**: gray computed monthly + quarterly in history (`=company/pool`), the blue LEVEL input in estimates (# M/M memo rows optional). This is the TAM → share ladder specialized to the product.
3. **Company volumes**: Month 1/2/3 (K:"Monthly" — from the monthly ops release) → quarter total, % Y/Y, **Seasonality**, % Q/Q, Annual pair, % M/M + monthly % Y/Y sub-blocks. Where the company discloses ADTV instead of totals, carry both (ADTV block × trading-days row → total). A red `Consensus >>` memo row beside the volume line where the Street models the KPI.
4. **Per-account activity intensity**: trades (or $ volume, or contracts) per average funded account, annualized — % Y/Y, Seasonality, % Q/Q, Annual pair. In estimates the intensity or the share input drives; volumes rebuild as intensity × accounts (or share × pool) — never forecast raw volume with a bare %Y/Y when either decomposition is available.
5. **Read-across / alt-data memos** (CCCCFF `Memo:` headers, informational only): Yipit product-level trackers, SLICE, Reg NMS dashboard revenue estimates (BULL pattern: tracked revenue $ with % Y/Y/% Q/Q vs the modeled line), Coinbase/exchange-volume read-across for crypto, peer monthlies. Structured per the main skill's competitor read-across spec.
6. **Rate line** (take rate bps / rate per contract / capture bps / commission per DART): gray computed in history (`=revenue/volume`), blue LEVEL input in estimates, back-solved to consensus at seed; % Y/Y, Seasonality, % Q/Q, **Annual** pair; # Q/Q where the story is sequential rate drift. Mgmt-guidance rows attach here when a Guidance tab exists (rate and volume guides are common).
7. **Product revenue** = volume × rate (D-level output feeding the P&L green link), % Y/Y, Seasonality, % Q/Q, Annual pair.

**Product-specific notes:**
- **Options**: the industry pool is OCC volumes (dashboard/staging feed); HOOD and BULL both carry `HOOD/BULL Market Share of OCC Volumes` with monthly # M/M. DATs/DARTs sub-blocks where the company discloses trade counts alongside contracts.
- **Prediction markets / event contracts**: young, event-driven product — build an **event-calendar scaffold** memo when volumes are driven by scheduled events (HOOD pattern: World Cup matches × contracts per match; NFL games split Normal/Marquee/Playoff/Superbowl × contracts per game tier × assumed market share vs Kalshi), rolling to a Fall Sports / Total contracts build; carry a `Memo: Contra Rev` block where customer-match promos net against revenue (take rate ex-contra as the clean rate), and new-initiative memos (e.g. Rothera) as separate informational builds until disclosed. 2Q-stack rows are useful where Y/Y is meaningless.
- **Crypto**: read-across pool = tracked exchange volumes (Coinbase via Yipit, Bitstamp/theBlock); company app ADTV where trackable; a red Check/Plug row reconciling tracked components to the company total.
- **Commission brokers (IBKR)**: the funnel metric is **DARTs** — total and cleared, DARTs per account (annualized) with a `per bp` sensitivity memo vs the policy rate, trades = DARTs × trading days, revenue = cleared trades × commission per cleared DART; `Implied commissions from Monthly` vs reported (% of reported memo) ties the monthly disclosure to the P&L line.
- **DARTs total block** (BULL pattern): where the company discloses blended DARTs, carry per-product DARTs (Equities/Options/Other) Month 1/2/3 → quarter average (K:"Presentation") rolling to Total DARTs with % Y/Y / % Q/Q — a disclosure-tie block, with the revenue engines still running off volumes × rates.
- **Roll-up**: `Total Transaction Revenues` with the full % stack + Annual pair, then a **Rev $ / Mix % block** (each product's revenue $ and % of transactional mix) — the at-a-glance product-mix read. Thematic uplift memos (e.g. agentic-trading adoption ladders) live here as informational scenario memos.

## Layer 4 — NII engine (broker variant)

Section banner "Net Interest Revenue Build" / "Interest Income Engine". The broker NII stack is balances-as-%-of-assets × yields-as-%-of-policy-rate:

- **Rates — BB Live Formulas block first** (main skill § live-rates): the standard broker ticker set — `.NPEFF` (Fed Funds upper), `.BBFFR` (FF fwd curve), `.NPSOFR`/`.NP30SOF`/`.NP90SOF`/`.NP6MSOF` (SOFR family), `.NP1ML`/`.NP3ML`, `.NPPRIM`, UST curve, MBS coupons — each with Month 1/2/3 + Average and a Sequential-change row. Multi-currency books (IBKR) add foreign benchmarks (EURIBOR) and the **blended mix block**: blue mix weights (Fed Funds / EURIBOR / …) × each curve → a Blended benchmark row that the yield lines ride. Alternative rate paths (Alt 1 / Alt 2 — e.g. more/fewer cuts) get parallel curve blocks + a scenario NII-impact memo, informational.
- **Balance stack — every interest-earning/bearing balance is expressed as a % of customer/platform assets** (or of AUM/credits), each with monthly rows, the full % + $ delta stack, per-account intensity, and an average-vs-presentation plug:
  - **Margin book**: Margin as % of platform assets (# Y/Y, # Q/Q, NNA-rate framing), monthly EOP → average, `% Y/Y growth: margin book vs platform assets vs margin-growth-LESS-asset-growth` memo (the gearing read), Average Calc vs Presentation average with a red Diff/Plug row.
  - **Client cash / deposits / sweep**: cash & deposits as % of AUM; **cash sweep** with the enrollment sub-build (funded customers enrolled, % funded, funded per account) where sweep is opt-in (HOOD); client bank deposits (BULL); corporate cash (own yield).
  - **Segregated cash & securities** (IBKR): seg cash/securities as % of customer credits; securities borrowed/loaned as % of client equity.
  - **Credit cards / other IEA** where present.
  - Roll to **Average interest-earning assets** and **Average IBL** with % Y/Y / Seasonality / % Q/Q + Annual-average pairs.
- **Rate-sensitive split** (IBKR pattern, main skill § rate-paying split): fully-rate-sensitive vs non/partially-rate-sensitive customer credit balances (EOP and average), mix row — interest paid rides the sensitive piece only (e.g. "BM − 0.50% on eligible cash").
- **Yield stack**: each balance's yield expressed as **% of Fed Funds (or the blended benchmark)** — gray computed in history, blue %-of-benchmark or CTD-beta input in estimates (`CTD beta` rows per balance, IBKR). Yields: margin yield, seg-cash yield, sweep/deposit rate paid, sec-borrowed/loaned net, credit-card yield.
- **Sec lending, net** as its own sub-block (own drivers; IBKR carries `NII ex. Sec lending` memo lines on the P&L because the Street strips it).
- **NIM block**: NIM calc (= NII annualized / avg IEA) with # Y/Y / # Q/Q + Annual NIM, vs **Reported NIM** memo; **Betas** summary block; **Interest income / Interest expense** split tying to the reported lines.
- **Presentation bridge** (main skill § NII presentation bridge): engine NII → less/plus interest reported in other-fees / other-income lines → Reported NII (the consensus-tied line). IBKR pattern: `Interest reported in other fees and services` / `in other income (loss)` rows with a %-of-Other memo.
- **Rate-sensitivity ladder** (informational): the FFR range table (0–25bp bands ×N) mapping NII/EPS impact per band — the scenario-memo pattern for cuts/hikes.

## Layer 5 — Expenses, other revenues, capital return

**Expenses** (broker-specific keys; the rest follows the main skill):
- **Brokerage & transaction expense is VARIABLE — model it as % of transactional revenue**, specifically of the clearing-heavy products: `Transaction expenses as % of (Options + Equities) revenues` gray in history, blue % input in estimates, with an Annual-AVG row (HOOD and BULL both). Never %Y/Y this line.
- **Marketing**: alt-data lead block (Total Paid Visits / Affiliate Visits, Month 1/2/3 + Sum, % Y/Y, sequential-change rows — BULL/SimilarWeb pattern), Marketing as % of revenue memo; marketing is the growth-spend swing line, guidance-prone.
- **Comp**: headcount × comp-per-employee engine (main skill spec; IBKR carries the BoP/net-change/EoP/average headcount roll + annualized comp per employee + comp-margin bps rows).
- **Adjusted-vs-GAAP opex bridge**: Total Opex → less SBC (split restructuring/one-timer SBC), provisions, restructuring → Adj Opex (+ SBC add-back variant tying to the company's presented "Adj Opex + SBC" guide line — HOOD). RIF/cost-action memos (`Memo: <date> X% RIF`: annualized comp × reduction → impact) under the comp line. Efficiency ratio + # Y/Y on the P&L.
- **Provision for credit losses** (margin books): its own line, consensus-seeded go-forward.

**Other revenues:**
- **Subscription** (HOOD Gold pattern): subscribers (monthly, % of funded memo) × price → revenue; `Cost per user — Annual` memo for the rewards/deposit-match cost side.
- **Fee stack** (IBKR Other Fees & Services pattern): market data, risk exposure, PFOF (options contracts × PFOF per contract), FDIC sweep fees (balance × fee yield), min-activity fees, other — each with % Y/Y and a per-avg-account intensity row.
- IPO access, new-product placeholders, and an **Other-revenue plug** line (red, K:"Plug") absorbing the residual to the reported total.

**Profitability & capital return:**
- **Adjusted earnings bridges** where the company leads non-GAAP: EBITDA → Adj EBITDA (SBC, unrealized marks) with margins + **Incremental EBITDA margin** (HOOD); GAAP NI → Adjusted NI (SBC, deferred-tax effects, FX/one-timers) (BULL); Core vs GAAP everything (IBKR: core NII/fee/NIE/PPNR with `Core` %-row variants). Pick the company's own headline basis for the EPS strip and consensus ties.
- **Share roll**: `BoP diluted − repurchased (+$ repurchased / price per share rows) + issued (SBC) = EoP diluted`, % Q/Q — the main skill share-roll spec; payout-ratio block (dividend/repurchase/total payout % of adjusted NI) and DPS × shares where dividends exist.
- **Returns block**: ROA/ROE (annualized, with Annual + # Y/Y), ROTCE and BVPS/TBVPS where capital matters (IBKR); TCE/TA.
- **Up-C / NCI** (IBKR): the main skill's two-tier waterfall applies — Minority-interest % memo (`=NCI/NI`), public-ownership roll; never a blended rate.
- **Balance sheet**: the broker BS is customer-driven — seg cash & securities, receivables from customers (margin), securities borrowed/repo, financial instruments vs customer payables, broker payables, securities loaned; the balance check row and the `cash+securities+margin as % of customer payables + prior-qtr equity` feasibility memo (IBKR); BS-drivers section expressing each major BS line as a % of its client-balance driver (% of client equity, % of margin loans, % of credits) so estimate columns rebuild the BS off the Layer-2 ecosystem.

## Monthly disclosure plumbing

Retail brokers disclose monthly operating metrics — the model's cadence advantage. Two acceptable patterns (pick per build):
- **Monthly-in-quarter on the Model tab** (HOOD, BULL — the v4 default): Month 1/2/3 rows inside each quarter per the main skill, K:"Monthly" tags, latest undisclosed month blue-on-yellow.
- **Dedicated Monthly tab + INDEX/MATCH pulls** (IBKR legacy): a Monthly tab holding the full monthly history, Model-tab quarterly blocks pulling via INDEX/MATCH on the metric label + period; `Implied <line> from Monthly` vs reported memos tie the two. Use when the monthly history is very long or shared across many blocks; the Model rows are then green pulls, and the % blocks still compute on-Model.
Either way: every monthly KPI carries % M/M, # M/M (units/$ where levels matter), and monthly % Y/Y sub-blocks, plus Seasonality rows — monthly seasonality is how the intra-quarter nowcast is set.

## Retail-broker KPI set (for Research-first, Drivers tab & Qtr tab selection)

The canonical KPI banner: funded accounts (+ net adds), customer/platform assets, net deposits (+ NNA %), per-product volumes (equity notional, options contracts, crypto notional, event contracts, DARTs), per-product take/capture rates, margin balances, client cash/sweep balances, NIM/NII, transactional revenue by product, ARPU, Adj EBITDA (or the company's headline basis), EPS. Carry this set into the Drivers and Qtr tabs; the monthly-disclosed subset is the Revisions-tab focus.

## Advanced grammars used by live broker builds
When the disclosure supports them, pull these from `references/driver-grammars.md`: the
**cohort/vintage triangle** (G1 — per-cohort deposit/retention build tying calculated vs actual NNA),
the **attach/penetration engine** (G2 — subscription tiers: penetration × funded, new-user vs
backbook attach), the **event/deal calendar** (G3 — prediction-market and IPO-window builds), the
**toggleable thematic overlay** (G4), and **staging-tab feeds** (G6) for app-download/card/visit
data. The monthly Seasonals + Vs-Normal rows (G7) and 2Q stacks (G8) apply throughout the funnel and
product engines.

## Retail-broker acceptance additions (run with the main checklist)

R1. ☐ Funnel built first: funded-account level + roll (where disclosed) with net-adds # rows; average-accounts row is THE per-account denominator everywhere.
R2. ☐ Customer assets carry the full market-vs-organic bridge: index block, NNA %-annualized rows, and the BoP + deposits + market = EoP rollforward tying the EOP level.
R3. ☐ Every product engine has: pool (where one exists) → share → company volumes → per-account intensity → rate → revenue, with monthly sub-blocks and Seasonality rows; rates back-solved to consensus at seed; read-across memos informational only.
R4. ☐ NII: balances expressed as % of assets, yields as % of benchmark (or CTD betas), rate-sensitive split where applicable, engine NII reconciled to the reported line via the presentation bridge; NIM calc vs reported memo.
R5. ☐ Brokerage/transaction expense modeled as % of (options + equities) transactional revenue — never bare %Y/Y.
R6. ☐ Adjusted basis matches the company's headline (Adj EBITDA / Adj NI / Core); EPS strip and consensus ties on that basis.
R7. ☐ Monthly plumbing consistent (in-quarter rows or Monthly-tab pulls with implied-vs-reported ties); latest undisclosed month is the blue-on-yellow nowcast input.
R8. ☐ Balance sheet rebuilds off the client-balance ecosystem (%-of-driver rows) and balances every column.
