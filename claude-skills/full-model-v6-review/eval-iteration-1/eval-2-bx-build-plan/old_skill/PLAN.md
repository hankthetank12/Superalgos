# Build Plan — Blackstone (BX) Full Model (full-model-v5)

Deliverable: one workbook — a deep quarterly Model tab (actuals hardcoded to the press release, estimates
driver-built and seeded to consensus) plus five downstream tabs in the same pass: Mini Model, Revisions,
Drivers, Qtr, DCF. BX is an ALTERNATIVE ASSET MANAGER, so the generic transactional engine is replaced by
the asset-manager variant (AUM rollforwards -> fee rates -> FRE; realizations -> performance income) per
SKILL.md "Sector variants"; the v4 retail-broker engine does NOT apply. Nothing is built until Step 0 clears.

## 1. What I need from the user first (v5 Step 0 gate — mandatory, before any scoping or build)
1. **Most recent earnings release** — the 2Q26 press release (BX's release doubles as the financial
   supplement: segment P&Ls, AUM/FEAUM rollforwards, perpetual capital, dry powder, share/unit detail).
2. **Earnings/investor presentations** — 2Q26 earnings deck and any recent investor-day materials.
   Purpose per the skill: (a) mirror how MANAGEMENT presents the business (segment DE format: Management
   fees -> Fee Related Earnings -> Net Realizations -> Distributable Earnings), not the GAAP cut; (b) mine
   for company-only KPIs absent from VAActuals/consensus to build as drivers (flagged in the reply).
3. **The target workbook** (or confirm fresh build) and whether it contains: a **VAActuals/consensus tab**
   (decides the Street source), a **Guidance tab** (decides whether the guidance overlay applies), a
   Monthly tab, a 1 Pager (live price cell for the DCF).
4. **Consensus values** if there is no VAActuals tab: a Visible Alpha export or per-line Street figures
   (segment mgmt fees, FRE, DE, DE/share to the cent, FEAUM by segment) for the focal quarter + 2 FYs —
   required because every estimate seed is back-solved from consensus and live Bloomberg does not
   calculate in this headless environment (see §5).
5. **Confirmations**: consensus EPS basis (DE per share — match before any GAAP bridge), focal quarter
   (expect 3Q26E; 2Q26 printed in July), history depth (propose 1Q21-forward), the firm label for the EPS
   strip ("<Firm> Estimates"), and any vehicles to break out explicitly (BREIT, BCRED, BXPE, BIP).

## 2. Skill references I would read, and why (in build-order sequence)
- **SKILL.md** end-to-end — the v6.1 Model-tab engine spec: scaffold, period banner, EPS strip, color/
  border system, rollforward+check rules, Up-C variant, market-vs-organic bridge, annual SUMIFS, audit.
- **references/guidance-overlay.md** — ONLY if the workbook has a "Guidance" tab: reserve violet guidance
  rows during the P&L skeleton (step 4), never insert later. No Guidance tab -> skip silently.
- **references/mini-model.md** (at build step 10) — self-contained annual Mini Model: blue hardcoded
  actuals transcribed from audited Model annuals, in-tab blue drivers, zero Model/VAActuals links.
- **references/revisions-tab.md** (step 11) — Old/New/Chg tracker off a hidden "From Model" staging block.
- **references/drivers-tab.md** (step 12) — model-vs-Street 8-row KPI blocks; it names the alt-asset-manager
  standard KPI set and the AUM/FPAUM-by-strategy sections with annual-basis rules (stocks = 4Q value,
  averages = AVERAGE of 4 quarters) — directly load-bearing for BX.
- **references/qtr-model-vs-street.md** (step 13) — v2 GS-format Qtr spec (column-B banners, #FFFFCC actual
  band, blank-Street guards, /100 VA ratios, typed FY bases, hidden AE:AG block).
- **references/dcf-tab.md** (step 14) — segment-level hedge-fund DCF; asset-manager stream framing
  (FRE + performance), stream-specific FCF conversion, per-stream exit-multiple TVs.
- **references/retail-broker-engine.md** — NOT read: mandatory only for retail brokers; BX is not one.
- `scripts/insert_guidance_rows.py` — only if guidance must be overlaid onto an already-built model.

## 3. Research pass (after materials arrive; before any P&L skeleton)
Per the skill, I must be able to state the revenue build in one paragraph first. Working statement to
verify against the release/10-Q/transcript (EDGAR + company IR are reachable here): BX earns (1) management
fees = average Fee-Earning AUM x effective fee rate, across four segments (Real Estate, Private Equity,
Credit & Insurance, Multi-Asset Investing), each FEAUM stock rolling BoP + inflows - outflows -
realizations +/- market appreciation; (2) fee-related performance revenues (perpetual-vehicle
crystallizations, seasonal); (3) realized performance revenues and principal investment income driven by
realization activity against the net-accrued-carry balance. Fee-related comp + opex -> FRE; FRE + Net
Realizations -> Segment DE -> taxes/NCI (Up-C) -> DE and DE/share, with ~85%-of-DE dividend payout.
Step-0 KPI hunt — company-disclosed, typically thin/absent in consensus, prime driver candidates:
perpetual capital AUM by vehicle, AUM not yet earning fees (fee pipeline), dry powder, deployment,
fund-level appreciation by flagship fund, net accrued performance revenue ($ and per share), BREIT/BCRED
flows and repurchases, insurance-channel and private-wealth-channel AUM/inflows.

## 4. Exact tab list, in build order (skill "Order" rule)
1. **Model** — the deep quarterly tab (built via build-order steps 1-9; audit gate before anything else).
2. *(staging, as needed)* market-data staging sheet(s) for long index histories; BQL consensus staging.
3. **Mini Model** — second tab overall; self-contained annual summary.
4. **Revisions** — Old/New/Chg across next ~3 unreported quarters + current & next 2 FYs.
5. **Drivers** — model-vs-Street KPI blocks + AUM/FEAUM/perf-income by segment.
6. **Qtr** — focal-quarter Model/Street/Actual one-pager (v2 spec).
7. **DCF** — always last (consumes finished Model annuals, Drivers consensus, 1 Pager price).
Guidance overlay rows are reserved inside the Model P&L at step 4 only if a Guidance tab exists.

## 5. Sourcing actuals and consensus in THIS build environment
- **Actuals**: BLUE HARDCODES from the user-provided 2Q26 press release/supplement (prior quarters from
  earlier releases via SEC EDGAR, which is web-reachable here; Daloopa if the user provides exports).
  One red plug per block; NI ties reported with a red $0 tie memo. **Hard rule: no green links to
  VAActuals, ever** — VAActuals appears only as red-italic Street on Drivers/Qtr/EPS blocks.
- **Consensus (Street source priority per the skill)**: (1) a VAActuals tab in the workbook, if present —
  Drivers/Qtr/EPS-strip Street cells link to it (ratios /100); (2) else Bloomberg BQL/BDP. This
  environment has no live Bloomberg terminal, so: write the BQL formulas per spec (adjusted-EPS pull with
  FPR linked to the derived period-string scaffold, canary cell included) and let them error/blank with a
  note — never paste static numbers pretending to be live; take the NUMERIC seeds for back-solving from
  the user-provided VA export/consensus figures (item 1.4) and flag them as stated seeds.
- **Market data** (SPX, credit index, rates for appreciation drivers): sourced web hardcodes with a cell
  note (source + URL) on every cell, K-column tags, Month 1/2/3 + Average blocks; gaps stay blank and
  flagged. Market data has no consensus — seed market %Y/Y to a stated assumption and back-solve the
  linked driver so revenue still ties consensus at seed.

## 6. Engines to build for BX specifically (Model tab, below the P&L, two-tier banners)
- **Per-segment AUM & FEAUM rollforward engines** (Real Estate, PE, Credit & Insurance, Multi-Asset):
  BoP + inflows - outflows - realizations +/- market appreciation = EoP, each flow on its own blue input;
  inflow sources SPLIT (institutional drawdown vs private-wealth perpetual vs insurance/captive SMAs) per
  the skill's inflow-split rule; check rows tying FEAUM to total-AUM flows; $ Y/Y rows where the dollar
  change is the story. Market appreciation gets the **market-vs-organic bridge**: index tracking blocks
  (SPX; HY/IG credit; 10Y) with beta inputs, "from market returns / total / ex-markets" decomposition,
  red appreciation plug in actuals, and a seasoning-framework memo with Implied-vs-Modeled check.
- **Perpetual capital & fee-pipeline block** (Step-0 company-only KPIs): perpetual AUM by major vehicle,
  AUM not yet earning fees, dry powder, deployment — driver rows feeding inflow/fee timing.
- **Management-fee engine per segment**: effective fee rate (bps of average FEAUM) computed gray in
  history, blue level/Δ input in estimates ("# Y/Y" under every rate row); fees = avg FEAUM x rate / 4;
  fee-holiday memo where applicable (BREIT-style waivers).
- **Fee-related performance revenue engine**: by crystallizing vehicle where disclosed; brown seasonality
  memos (4Q-heavy crystallizations).
- **FRE build**: fee-related comp ratio (Δ input + # Y/Y) and other opex %Y/Y -> FRE, FRE margin on the
  gray band with # Y/Y; **Incremental Margins row** under the margin block (mandatory); `Memo: Comp Ratio`
  (#CCCCFF header) plus a headcount x comp-per-employee productivity memo (people-business check).
- **Realizations engine**: net accrued performance revenue (carry) BALANCE rollforward (accrual +/-
  marks - realizations), realization-rate driver on performance-eligible AUM, realized perf comp ratio,
  realized principal investment income -> Net Realizations; scenario memo `Memo: Realizations — Downside
  ('08-style)` and a BREIT-redemption stress memo on perpetual AUM (informational only).
- **Up-C / two-tier tax & NCI waterfall (mandatory — structure applies)**: Blackstone Inc. vs Blackstone
  Holdings partnership units (SMD-held): tier-1 entity taxes -> net income to members; tier-2 public
  ownership % block (rolls with exchanges/buybacks, Annual # Q/Q) x HoldCo tax -> NI to common; implied-
  NCI rebuild with red plug ~0; **dividend block** (blue payout-%-of-DE input, BX's ~85% policy, feeding
  the equity roll) and a **share-count roll** (buyback $ / avg price back-solved to tie consensus shares).
- **GAAP-vs-DE bridge** so the EPS strip and consensus tie on the DE/share basis; per-share rows on every
  stream (FRE/share, Net Realizations/share, net accrued carry/share). Per-unit intensity blocks are N/A
  (no countable unit base) — noted in the reply per the checklist.

## 7. Downstream tab specifics for BX
- **Drivers/Qtr KPI set** (alt-manager standard set from drivers-tab.md + Step-0 additions): Management
  fees (total + by segment), Fee-related performance revenues, Total fee revenues, Fee-related expenses,
  FRE, FRE margin, Net Realizations, DE, After-tax DE, DE/share; driver sections for Total AUM, FEAUM by
  segment (annual = 4Q value for stocks, AVERAGE for average-FEAUM rows), inflows, perpetual AUM.
  One-sided metrics stay one-sided (green model-only / red Street-only); perf-income gross-vs-net caveat
  confirmed with the user before pairing.
- **DCF streams**: FRE stream (capital-light, FCF-yield conversion, premium exit multiple) and Net
  Realizations stream (low multiple), channel-pool/TAM foundation on private-wealth and insurance
  channels with named competitors (APO, KKR, ARES, CG) and Modeled-vs-Consensus check; NPV -> implied
  price vs live/1-Pager price; market-implied-multiple back-solve on the FRE stream.

## 8. Verification (§ Verify and report + final acceptance checklist)
1. Model gate before any downstream tab: full rebuild; every reported quarter ties to $0 (tie memos);
   estimates tie consensus at seed (DE/share to the cent; back-solved capture/share on market lines);
   wiggle test (one fee-rate/flow input + one market %Y/Y — line, subtotal, EPS move; restore); ALL check
   rows 0 (AUM/FEAUM rollforward ties, segment sums, implied-NCI plug, share-count tie, capital
   feasibility); zero error cells; border/format verification BY IMAGE (banner white year separators,
   label-through-numbers rules, clean 4-sided Annual boxes, two-tier banners, Calibri 9pt).
2. Downstream: Mini Model self-containment scan (no Model!/VAActuals! refs outside red consensus block,
   blue actuals tie Model annuals, wiggle test); Revisions Chg all 0 at build; Drivers actual-period
   Vs-Street ≈ 0 with breakdowns summing; Qtr hidden AE:AG read back for errors, blank-Street guards,
   Street ties source; DCF actual years tie Model, attribution/NPV-allocation checks ~0, growth decays.
3. Reply reports: tie numbers, assumption-cell addresses, unsourced gaps, stated seeds, scenario-memo
   locations, which drivers came from company-only disclosure vs consensus, consensus source used per
   tab, and guidance-overlay status (applied lines + unmatched items, or "no Guidance tab — skipped").
