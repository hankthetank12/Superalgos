# DCF tab — driver-based, segment-level intrinsic value (built after the Model tab)

Annual valuation tab fed by the Model. Distilled from two audited live builds (a 10-yr channel/TAM-framed DCF and a refined stream-engine DCF); this spec merges both. Adapt streams and drivers to the company's industry — the framework is the skeleton, not a rigid template.

## Philosophy
This is NOT a textbook banker DCF (no UFCF/WACC build, no perpetuity growth). It is a hedge-fund-style DCF:
1. **Earnings are built from operating drivers, not grown as a blob.** Every revenue line = driver × rate (AUM × fee rate, volume × price, balances × spread, units × ARPU), reusing the SAME driver grammar as the Model tab. Growth then decays naturally and every assumption is auditable.
2. **The DCF EXTENDS the Model, it never re-derives it.** Actual years (and Model-covered estimate years) link green to the Model's annual columns; the DCF adds ~10 forecast years beyond the Model horizon driven only by blue inputs and prior columns. Never hardcode a computed number.
3. **FCF conversion is stream-specific.** Capital-light earnings convert at an FCF-yield input; balance-sheet/capital-consumptive earnings convert via dividend-out + book-value reinvestment roll-forward.
4. **Terminal value = exit multiple per earnings stream** (SOTP terminal) applied to final-year after-tax earnings in the final column only. Different quality streams get different multiples.
5. **One discount rate input**, NPV over the FCF+TV row, bridged to an implied share price (or vs live market cap) → upside.

## Step 0 — Research and scope
- Inventory the workbook: the Model tab's annual columns and the row addresses of every line to link (segment revenues, AUM/balances, flows, comp, non-comp, interest, taxes, book value, shares); an Industry/TAM tab if present; the 1 Pager or a live price/market-cap cell.
- Identify the company's 2–4 earnings streams and their economics (asset manager: FRE + spread + performance; bank: NII + fees; broker/exchange: transactional + NII; SaaS: ARR cohorts). Decide the driver stack per stream and whether a channel-pool × market-share framing is available (preferred for the biggest third-party growth engine).
Done when: each stream, its driver formula, and its Model-tab cell addresses can be listed in chat.

## Step 1 — Sheet setup
- New tab "DCF" (or "<TICKER> DCF"). Gridlines off. Whole tab Calibri 9pt. Title in B2, medium bottom border under row 2.
- Labels stair-step B→H (B = section, C = subsection, D–F = lines, F–H = drivers) so hierarchy reads by indent; years across columns from ~col G/I.
- Years: last ~5 fiscal actuals + ~10 forecast years; first year typed, every later year `=prior+1`.
- Scenario markers are allowed as small notes ABOVE the year row (e.g. "Recession" over the stress-start column); stress inputs mid-timeline sit on the distinct scenario fill #FBE2D5 so they read as scenario overrides, not base-case inputs.

## Step 2 — Channel/TAM foundation (build FIRST when share-of-market frames the growth)
For each distribution channel or market pool the company competes in (e.g. insurance/institutional/wealth; retail/institutional; on-platform/off-platform):
- **Pool row**: total channel assets/volume — blue level + blue % Y/Y growth inputs (sourced note), or green link to an Industry tab.
- **Company row**: green Model link in covered years; forward = share engine or growth input.
- **Named-competitor rows** where disclosed (each green-linked to that peer's figure or sourced blue) so the share input is set against real players; competitor and company **market-share rows** beneath (gray calc), "# Y/Y" bps rows on share.
- Residual channel components computed as red back-solves (= total − named pieces).
- **Breakdown cross-check block**: channel pieces re-summed against the company's total AUM/volume (green Model link, residual red), a "Multiple vs <base-year>" row (how many × the base year the forecast implies), and a **Modeled vs Consensus row pair** (modeled total vs green/red consensus link from the Drivers/VA tab) so the DCF's trajectory is checked against Street before it is discounted.
- Optional **product-mix block** (e.g. yield/hybrid/PE) with mix % rows when mix drives the fee rate.

## Step 3 — Earnings engine (per stream, boxed section label B:H filled #FBE2D5)
Canonical fee/revenue pattern (rows in order): balance/volume row (green Model link in covered years; forward `=prior*(1+growth)` off a blue input or the TAM engine); rate row (actuals implied `=fee/AVERAGE(prior:current balance)` black; forward blue input); fee row (actuals green Model link; forward `=rate*AVERAGE(prior:current)`); % Y/Y gray beneath every line, "# Y/Y" bps under every ratio/share row, "$ Y/Y" where the dollar delta is the story.
- **Captive/strategic/third-party split** for multi-client fee books: captive client balances green-linked from the Model, strategic clients hardcoded-then-grown, third-party as the red residual framed by the TAM × share engine (share = `prior + bps_gain/10000`, blue bps input).
- **Flows roll-forward** (balance-sheet streams): organic inflows (%Y/Y input), outflows (blue % of prior invested assets), net flows, share captured, then BOP / net flows / Mkt Perf $ (red plug in actuals, `=BOP × blue perf %` forward) / EOP feeding the fee/spread base.
- **ROA/ROE incremental-reinvestment engine** (alternative for spread/insurance streams): prior-period operating earnings ÷ blue % ROA ⇒ implied prior-period assets; incremental equity (= the reinvestment row from Step 4) × blue ROE ⇒ incremental earnings; optional loss row = blue % of prior assets (stress it via the scenario fill); stream earnings = prior earnings + incremental earnings ± losses. This makes the FCF↔growth trade-off explicit: cutting the dividend raises reinvestment, compounds earnings, and shows up in the DCF.
- **Expenses**: comp via comp-ratio path (`ratio(t)=ratio(t−1)+bps_delta/10000`, blue bps row), non-comp %Y/Y; stream earnings; margin row on gray #F2F2F2 with "# Y/Y".
- **P&L rollup**: segment/total income (bold, top border); holdco interest; taxes = blue rate × pretax (actual years show the implied rate); Adjusted Net Income bold, % Y/Y. Actual-year subtotals must tie the Model to the dollar.

## Step 4 — FCF conversion (boxed "FCF" section, #FBE2D5)
- **Capital-light streams** (fees, performance income): FCF = earnings × blue "Assumed FCF Yield" (e.g. 80%).
- **Balance-sheet streams**: Dividend to HoldCo row (blue seed, grows at blue %); Reinvested = earnings − dividend (a forward-looking capital-need variant is allowed: reinvestment = next-year earnings × capital factor − dividend); BV roll-forward `=prior BV + reinvested × blue retention%`; ROE memo row = earnings/BV. **Final year: no reinvestment** — full final-year earnings flow to FCF; note it.
- Total FCF row bold.
- **Per-stream FCF attribution block**: Net FCF split back to each stream (allocated by % of earnings, plus that stream's TV and less its reinvestment), with a **red italic Check row** proving the stream FCFs sum to total FCF — this is what feeds the NPV-allocation block.

## Step 5 — Terminal value (final column only)
Per stream: terminal earnings = final-year earnings × (1 − tax) − allocated interest; TV = terminal earnings × blue exit multiple on light-blue #DAE9F8, format `0.0"x"` (high multiple for recurring fees, ~book multiple × BV for spread earnings, low multiple for volatile performance income). "FCF + EV" row = annual FCF, plus all TVs added in the final column only.

## Step 6 — NPV & allocation block (boxed "NPV", #FBE2D5)
- Discount Rate blue (e.g. 10%); EV `=NPV(rate, <FCF+EV range>)`; Shares Out green Model link; **Implied Share Price** bold; Current Px green (1 Pager or `BDP("<TICKER> Equity","PX_LAST")`; a market-cap variant compares NPV to `BDP(...,"CUR_MKT_CAP")` directly); **Upside** `=implied/current−1`.
- **NPV allocation**: NPV per stream (NPV of each stream's attributed FCF row), % of total NPV, and a **market-implied-multiple back-solve** — credit the non-core streams at chosen multiples, subtract from the CURRENT market cap, and show what multiple the market is paying for the residual core stream. Red italic check that stream NPVs sum to total. This is the row that turns the DCF into a variant-view statement.

## Formatting (match the Model tab conventions)
Green #008000 cross-tab links; blue #0000FF on #FFFFCC forward inputs; blue on #DAE9F8 terminal multiples; #FBE2D5 section boxes AND scenario-override inputs; red #FF0000 plugs/back-solves; red italic checks (~0); gray #F2F2F2 margin/rate bands; bold subtotals with thin top border. Number formats: `#,##0` $mm; `0.0%` growth; `0.00%` fee rates/spreads; bps rows `_(* #,##0.0_);_(* (#,##0.0);_(* "-"?_);_(@_)`; multiples `0.0"x"`; price accounting `$#,##0.00`. Manual calc during bulk writes; restore after.

## Verification (mandatory)
1. Zero error cells; actual years tie the Model to the dollar; estimate columns trace only to blue inputs, priors, and green links.
2. Modeled-vs-consensus rows populated; growth decays plausibly over the 10 forecast years (no un-input hockey sticks).
3. Final column includes TVs + no-reinvest treatment; attribution and NPV-allocation checks ~0; NPV range and anchor year correct.
Report: implied price (or NPV vs mkt cap), upside, the market-implied multiple on the core stream, and the 3–4 assumptions that matter most (with cell cites).
