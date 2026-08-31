# HOOD valuation layer — build notes

## What was built

One new tab — **`DCF`** — appended as the last sheet of `HOOD_with_valuation.xlsx`. Per the
full-model-v5 SKILL.md, the workbook order is Model → Mini Model → Revisions → Drivers → Qtr →
**DCF**, and the DCF is the valuation layer ("the DCF tab — the valuation layer, built last").
This workbook was complete through Qtr, so the DCF is the only tab v5's flow still calls for;
built exactly to `references/dcf-tab.md`. **No existing tab was touched** (verified: sheet list
is fixture + `DCF`; 5,600-cell random spot-diff across all 14 pre-existing sheets shows zero
value/format differences; drawing parts pass through byte-identical).

Layout (18 year columns J:AA = FY2021–FY2038; labels stair-step B→H; freeze panes J7;
gridlines off; whole tab Calibri 9pt):

- **Platform Assets & Customers** (rows 8–24): funded-account roll (green 4Q links to Model
  row 246), AUC walk — BOP + Net deposits + Market performance = EOP (Model rows 1327/1279),
  organic-growth %-of-BOP driver, market-return driver, avg-AUC row, and a **Modeled-vs-VA-consensus
  pair for AUC** (red links to `VAActuals!AT101:BA101/1000`).
- **Transaction Revenues** (26–57): five product engines — Options / Equities / Crypto /
  Prediction Markets / Other (Model rows 921/922/923/924/908) — each as *rev-per-avg-funded-customer
  (rate) × avg funded customers (balance)*, covered years green-SUMIFS-linked, forward off blue
  %Y/Y intensity inputs; a **red residual row** "Agentic uplift & other" (back-solved so covered
  years tie Model row 23 to the dollar — it captures the Model's agentic-uplift memo engine, r976,
  plus anything unnamed); bold total with check row.
- **Net Interest Revenues** (59–64): NII yield in bps of avg AUC (implied black in covered years,
  blue levels forward), NII = bps × $bn ÷ 10, covered green to Model row 24.
- **Other Revenues** (66–70): rev-per-avg-customer engine (Gold subscription story), green to
  Model row 25.
- **Total Revenues** (72–77): sum + red check vs Model row 26 + **Modeled-vs-VA-consensus pair
  for total revenue** (red links to `VAActuals!AT125:BA125`).
- **Expenses & Earnings** (79–104): brokerage & transaction expense as blue % of transaction
  revenue (Model's own broker convention; covered green-SUMIFS to row 32); opex ex-brokerage
  %Y/Y path; total opex green to row 55; opex-ratio gray band + #Y/Y bps; **red back-solve
  "Other income (warrants & other)"** so pretax ties Model row 83 exactly; tax-rate row (implied
  in covered years, blue 24.5%→25.0% forward); NCI (green SUMIFS r91; blue $48mm/yr forward);
  net income with red check vs Model row 93; margin bands.
- **Stream Earnings & FCF Conversion** (106–124): central costs allocated pro-rata revenue;
  per-stream pretax and NOPAT; blue **Assumed FCF yield** per stream (Transactions 90%, NII 75%,
  Other 90% — 100% in FY2038, i.e. no terminal-year reinvestment); stream FCF rows (built over
  the FY2027+ NPV horizon); NCI leakage; Total FCF; two red checks (Σ stream pretax = PT;
  Σ NOPAT − NCI = NI).
- **Terminal Values — 2038 exit** (126–134): per-stream exit multiples, blue on #DAE9F8,
  `0.0"x"` — Transactions 16.0x, NII 12.0x, Other 20.0x × FY2038 stream NOPAT, in the final
  column only.
- **FCF Attribution** (136–142): per-stream FCF+TV rows (TV added in FY2038 only), NCI leakage
  row, total, red check.
- **NPV & Valuation** (144–166): discount rate (blue 10.0%, J145); `EV =NPV(J145,P141:AA141)`
  (FY2027–FY2038, i.e. value as of FY2026 year-end); diluted shares green to `Model!AO107`
  (2Q26A, 912mm); **implied share price** (boxed); current price red live
  `=_xll.BDP("HOOD US Equity","PX_LAST")`; upside; **NPV allocation by stream** with % of EV and
  a red Σ-vs-EV check; **market-implied-multiple back-solve** (mkt cap − NII stream at 12.0x −
  Other stream at 20.0x ⇒ implied multiple the market pays on 2027E Transactions NOPAT).
- Scenario discipline per the spec: "Recession"/"Rebound"/"Election" markers above the year row;
  the FY2030 stress inputs (mkt return −12%, organic 8%, negative intensity growth) and the
  FY2031 rebound sit on the salmon **#FBE2D5** scenario fill; FY2032/FY2036 prediction-market
  election-year bumps are flagged by the markers. Section headers are #FBE2D5 boxed B:H;
  formats follow the spec (`#,##0` $mm, `0.0%` growth, bps accounting, `0.0"x"`, accounting $ price).

## Verification (per dcf-tab.md's mandatory list)

Method note: the workbook's live functions (`_xll.VAData`, `_xll.BDP/BQL`) cannot evaluate
outside Excel+add-ins, so verification ran on a **scratch copy** in which only those live cells
were stubbed with static placeholders (Model fed-funds forward row 996, QQQ rows 1502-1504, VA
consensus rows 101/125, the DCF's BDP price cell → $100). The **delivered file keeps every live
formula unevaluated** — nothing was fabricated in it. Results on the recalculated scratch copy:

1. **Zero error cells** on the DCF tab (LibreOffice full recalc; label strings excluded).
2. **Covered years tie the Model to the dollar** — all 23 spot pairs exact (TotRev/NII/Other/
   TxnRev/Opex/PT/NI vs Model annuals BB:BH for 2022–2028; EOP AUC and funded customers vs Model
   4Q cells for 2021/2025/2028), e.g. 2025: TotRev 4,473 / PT 2,108 / NI 1,883; 2028: 9,162.8 /
   5,640.2 / 4,222.7. FY2021 (no Model annual column) rebuilds via the same fixed-range SUMIFS
   the Model's annual columns use and lands on reported FY21 revenue of $1,815mm.
3. **Every forecast-year cell traces only to blue inputs, prior columns, or green links** —
   no hardcoded computed numbers; color audit: 0 blue-without-input-fill cells, 0 yellow-on-formula
   cells, whole tab Calibri 9pt (0 exceptions).
4. **All check rows read 0** across all populated years: components-vs-total (r57), vs-Model
   revenue/PT/NI (r75/96/104), stream-pretax-vs-PT (r111), ΣNOPAT−NCI−NI (r124), attribution
   (r142), and the NPV-allocation check (J157).
5. **Modeled-vs-consensus rows populated** for AUC and total revenue through the consensus
   horizon (FY2028); with test stubs they showed Model ~+1.6%/+6.5%/+6.5% vs Street revenue
   FY26/27/28 — live values will come from VAActuals in Excel.
6. **Growth decays plausibly**: total-revenue %Y/Y 2027→2038 = 25.5, 17.8, 16.5, 1.4 (recession),
   13.5 (rebound), 16.2 (election-year prediction-markets bump — input-flagged), 10.5, 10.4, 9.2,
   10.0 (election), 6.9, 6.8. No un-input hockey sticks.
7. **Final column carries the three TVs + no-reinvest treatment** (FCF yields = 100% in FY2038);
   NPV range/anchor correct (P141:AA141, FY2026-year-end anchor).
8. **Wiggle test**: bumping 2032 Options intensity %Y/Y 5%→10% moved Options revenue 2,632→2,758,
   total revenue, EV 103,801→104,811 and implied price 113.82→114.92 with every check still 0;
   input restored (test ran on the scratch copy; the delivered file holds the base inputs).
9. Border/format image check: 4-page render inspected — section boxes, top rules on every
   subtotal, gray ratio bands, boxed implied price, #DAE9F8 multiples, scenario fills all correct.

## Results to report (from the stubbed scratch recalc — will restate live in Excel)

- **EV ≈ $103.8bn → implied share price ≈ $113.82** (912mm 2Q26A diluted shares).
- Upside computes off the live BDP price in Excel (vs the $100 test stub it showed +13.8%).
- **NPV split**: Transactions 63.5%, NII 25.3%, Other 11.6%, NCI leakage −0.3%.
- **Market-implied multiple back-solve**: at the $100 test price, the market pays **~32.5x 2027E
  Transactions NOPAT** after crediting NII at 12x and Other at 20x (J164 recomputes off the live price).
- The 3–4 assumptions that matter most (all blue, wiggle-ready): discount rate **J145** (10.0%);
  exit multiples **AA128/AA130/AA132** (16x/12x/20x); organic-growth path **R16:AA16**
  (15%→4.5% of BOP AUC) with market return **R18:AA18**; prediction-markets intensity path
  **R43:AA43** (the biggest single revenue driver by 2038); FCF yields **P116:AA118**.

## Judgment calls (what I would have asked the user)

- **Which valuation tab(s)?** The task said "the valuation layer the skill's flow calls for
  next"; v5's flow prescribes exactly one — the DCF (v6 is the version with the 1 Pager/NTM-PE
  pair). Built only the DCF.
- **Stream cut**: 3 streams (Transactions / Net interest / Other) matching the Model's P&L
  rollup, with the 5 disclosed products + agentic residual inside Transactions. Would have
  confirmed whether the user wants Prediction Markets broken out as its own valued stream with
  its own exit multiple.
- **Driver grammar**: annual product engines as intensity (rev per avg funded customer) ×
  avg funded customers, and NII as bps of avg AUC — the annual-altitude collapse of the Model's
  pool×share×activity×take-rate and balance×yield engines. The quarter-level engines stay in
  the Model; the DCF extends, never re-derives.
- **FCF conversion**: all three streams use the FCF-yield method (capital-light retail broker;
  HOOD pays no dividend), with NII at a lower 75% yield to reflect regulatory/margin-book capital
  consumption, instead of a dividend-out + BV-reinvestment roll. Final-year yields 100%.
- **Terminal grammar**: TV = FY2038 stream NOPAT × multiple. No "allocated interest" deduction —
  HOOD's credit-facility interest is already netted inside the Model's reported NII line, and
  there is no holdco debt (noted on the tab). NCI carries no TV (small conservatism).
- **Current price / market cap**: no "1 Pager" tab and no live price cell exists in the workbook,
  so per the spec the current price is a red live `_xll.BDP` pull (the workbook's add-in prefix
  convention) and market cap = price × shares. Would have asked whether a 1 Pager price cell is
  preferred.
- **Consensus source**: VAActuals FY columns (AT:BA), the same Street source the Model/Drivers/Qtr
  tabs use — red italic links only, per the no-green-links-to-VAActuals hard rule.
- **NPV block scalars** (discount rate, back-solve multiples) sit in the J/K columns of the
  valuation block, where year columns no longer carry period meaning — the audited-build layout.
- **Recession + election cycle**: one mid-timeline stress year (FY2030) with FY2031 rebound on
  the #FBE2D5 scenario fill, and prediction-markets election-year bumps in FY2032/FY2036 — kept
  in the base path, hedge-fund style, and flagged with markers above the year row.
- **Model-inherited quirks carried, not "fixed"**: FY2021 columns reflect the Model's own 2021
  basis (the red "Other income" residual absorbs ~$2.0bn there, reconciling to the Model's 2021
  PT of ~$402mm rather than GAAP's IPO-charge loss); 2024's negative effective tax rate (DTA
  release) flows into that year's informational NOPAT history. Forecast years use clean 24.5%→25%
  rates.
- **Seeding the forward inputs**: the Model's 2026–2028 estimate columns depend on live Bloomberg
  rate/QQQ feeds, so the decay paths were seeded off a scratch recalc with a stated fed-funds
  stub (3.75%→3.25%) and flat ~1.5%/qtr market drift — the same figures the Model's blue inputs
  already imply elsewhere. In Excel the covered years re-price automatically off the live feeds;
  the DCF's blue forward inputs are analyst assumptions regardless.

## Files

- `HOOD_with_valuation.xlsx` — the fixture plus the new `DCF` tab (live formulas unevaluated;
  `fullCalcOnLoad` is set, so Excel recalculates on open).
- `NOTES.md` — this file.
