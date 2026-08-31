# NOTES — Mini Model tab rebuild (HOOD), full-model-v5 / references/mini-model.md

## What was built
One new tab, **"Mini Model"**, inserted immediately after the Model tab (position 3). No other
tab was touched — a cell-by-cell diff of all 16 pre-existing tabs (values + formulas, including
the full Model grid) against the input fixture shows **0 differences**; all 20 chart parts, the
external links, defined names, and calcPr (manual + fullCalcOnLoad + iterate) are preserved.

Layout per the spec: annual columns **J–Q = FY21A…FY25A | FY26E…FY28E** (VAActuals annuals begin
at FY-2021, so 5 actual years); "Base Case" label above the headers; dark-green bold **Actuals** /
blue bold **Estimates** split labels; label indents D (sections/final totals) → E (primary) →
F (sub-lines) → G (drivers) with % rows one column right; Calibri 9 throughout; gridlines OFF;
**no freeze panes**; focal-year **shape** on FY26E (column O, weight 1pt, y=0, full height —
injected at the XML level since openpyxl has no shape API).

Sections: Revenues (per-product driver stacks → Total transaction based revenues; IEA × NIM →
Net interest revenues; Other revenues %Y/Y) → Operating Expenses → Other income → Pretax → taxes/
NCI → Net income → shares → EPS → Adjusted EBITDA reconciliation → Customer & Platform KPIs
(funded customers, MAU, Gold subs, ARPU, NNA/market-gains/acquired → Total platform assets walk)
→ Street/Consensus block → Checks & Sources.

## Data surface and build mode (spec-mandated statements)
- **Actual years (FY21A–FY25A) link VAActuals** (the Visible Alpha tab, as-of 8/10/2026) in dark
  green #006600 — every P&L line, KPI level, and the share count. Subtotals link VA directly
  (Total txn rev → VA52, Total net revenues → VA125, Total opex → VA147, Pretax → VA155, Net
  income → VA161, EPS → VA165); red check rows at the foot cover any component wedge.
- **Estimate years (FY26E–FY28E) are a PURE DRIVER BUILD — totals are NOT consensus-pinned.**
  Question I would have asked (non-interactive run): *"Do you want the Mini Model marked to
  Street (consensus-pinned totals with an Other/reconciling residual), or fully independent?"*
  I proceeded with the pure driver build because the audited Model tab is the workbook's spine
  and its estimates are already consensus-seeded; the Street block still shows Model-vs-VA per
  year. Pinning can be added later by re-pointing the three totals at VAActuals AY/AZ/BA.
- **Street/Consensus rows** (red italic): VA Total revenue (r125), Adjusted EBITDA
  ("EBITDA - Operating", r259), diluted EPS (r165) across ALL years + `Model vs Street` rows.
- Estimate grammars: transactional lines = volume × take-rate (options contracts × $/contract;
  equity/crypto notional × bps; other = prior×(1+%Y/Y)); NII = avg interest-earning assets × NIM;
  all remaining lines prior×(1+%Y/Y) or level inputs. Driver rows sit ABOVE the line they drive;
  %Y/Y inputs sit BELOW the level they grow. 84 blue-on-#FFFFCC inputs; zero yellow on formulas;
  zero blue on formulas.

## Seed-tie numbers (Mini at seed vs the Model's annual estimates — recalc-verified)
| Line | FY26E | FY27E | FY28E |
|---|---|---|---|
| Total net revenues | 6,185.5 = Model BF26 | 7,863.8 | 9,416.4 |
| Total transaction rev | 4,075.0 | 5,148.8 | 6,065.2 |
| Net interest revenues | 1,600.0 | 2,017.9 | 2,581.8 |
| Total opex | 2,911.5 | 3,202.4 | 3,522.6 |
| Pretax income | 3,409.0 | 4,661.4 | 5,893.8 |
| Net income | 2,690.2 | 3,550.4 | 4,414.7 |
| EPS (diluted) | $2.95 | $3.91 | $4.87 |
| Adjusted EBITDA | 3,818.0 | 5,193.4 | 6,457.8 |
| Funded customers / Gold / Platform assets | 29.7mm / 5.66mm / $407.4bn | 32.9 / 7.58 / 524.1 | 35.9 / 9.72 / 674.2 |

All ties verified to <0.001% by full recalculation (LibreOffice) of a verification copy; actual-
year links tie the audited Model FY actuals to the dollar (FY25: rev 4,473 / NI 1,883 / EPS 2.06
/ Adj EBITDA 2,525). Seeds are pasted at full float precision so the ties are exact; display
formats keep them readable.

## Judgment calls
1. **Opex altitude = 2 lines** (Brokerage and transaction + All other operating expenses). The
   frozen Model forecasts opex only at the total and brokerage level (tech/ops/marketing/G&A/
   provision rows have no estimate values), so a 6-line component forecast would have been
   fabricated granularity. Actual years: brokerage links VA132; "all other" = VA147 − VA132.
2. **"Other (incl. event contracts)"** maps to VA row 47 (reported Other transaction rev) and in
   estimates covers the Model's Event Contracts engine (r924) PLUS its small residual Other txn
   line (r908) — combined FY25 302 → FY26E 1,760 (the +482.7% input reflects the event-contracts
   ramp). Note: the existing Drivers tab pairs VA47 against r924 only; the Mini's pairing is the
   composition-consistent one.
3. **"Revenue upside from AI initiatives"** is the Model's own overlay (r976, ON in the Model:
   36.3 / 286.1 / 517.3) — carried as blue level inputs so the txn total ties; blank in actual
   years (no VA counterpart; company-only/model-only line).
4. **"Plus: Discrete tax adj (2Q26 recon)" (−80 in FY26E)**: the Model's Adj EBITDA recon adds
   back $56m of taxes for 2Q26A vs $136m P&L taxes; this explicit row keeps the FY26 Adj EBITDA
   tie transparent instead of burying it in another add-back.
5. **Diluted shares** are %Y/Y-driven and back-solved (NI ÷ Model annual EPS → 911.1 / 908.2 /
   906.5) so EPS ties the Model's SUMIFS-annual EPS exactly; FY25 base is the FY25 average of the
   Model's quarterly diluted shares (913.5) as the proxy for VA r168 — if VA's FY25 weighted
   average differs slightly, EPS moves by <0.1%.
6. **MAU has no Model anchor** (the Model parks its MAU forecast — estimate inputs zeroed; the
   house Drivers tab also leaves model-side annual MAU blank). Driver used: "MAU as % of funded
   customers" held at the FY25A ratio (48.1%) → 14.3 / 15.8 / 17.3mm. Flagged as a stated,
   non-Model seed.
7. **Event-contract volume is not a separate KPI row** because the Model only carries PM contract
   volumes through FY26; the revenue line label and this note carry the composition instead.
8. **NCI, other income, interest expense, legal/FV adj** are blue level inputs (allowed input
   type) seeded to the Model's annuals (NCI 32/48/48; other income 135/0/0; int exp 36/40/40;
   legal/FV −8/0/0).

## Environment caveats (fixture is Bloomberg/VA-dead) — how seeds and verification were done
- The fixture carries **no cached formula values anywhere**, VAActuals is live `_xll.VAData()`
  (evaluates only with the VA add-in), and the Model contains live BDP/BQL rate/market cells. On
  this machine those evaluate to #NAME?; **they heal on the analyst's desktop**. Consequently the
  Mini Model's dark-green VA links and red Street rows show #NAME? until opened with the add-in —
  this is the spec's intended wiring (same as the existing Qtr/Drivers tabs).
- To obtain the Model's annual-estimate values for seeding, I recalculated a SCRATCH copy with
  LibreOffice after substituting, in that scratch copy only (never in the deliverable):
  (a) the forward Fed-funds path row (Model r996, live BDP) with a **flat 3.73%** — the rate
  implied by the workbook's own 2Q26 actual yields divided by the analyst's own forward beta
  inputs (0.0452/1.2, 0.0202/0.54, 0.0059/0.16); and (b) the 3Q26 market-nowcast month cells
  (r1502–1505, live BQL) with the last known index close (flat QTD → the Model's own −1% 3Q26
  market-return plug governs). **Effect on seeds**: the NII stack (IEA/NIM), FY26 market-gain
  ($9.3bn) and downstream PT/NI/EPS/Adj-EBITDA seeds embed this flat-rate / flat-market snapshot;
  on the desktop the live Model will drift with rates and markets, and the blue seeds can be
  re-marked in seconds. No live-data value was fabricated in the deliverable — estimates are
  formulas off blue assumption inputs; actuals are links.
- Verification used a throwaway copy with Model-derived literal values injected into the exact
  VAActuals cells the Mini links (valid because the Model is audited to tie VA actuals); the
  deliverable keeps pure links.

## Verification results (mini-model.md "Verify before done")
1. **Full rebuild, zero #REF!/#VALUE!** — PASS (LibreOffice full recalc of the verification copy;
   the only non-clean cells are two #NAME? at J93/J95 in that copy — FY21 NNA/market-gain VAData
   cells that were not injected; in the deliverable they are ordinary VA links that heal on
   desktop).
2. **Actual-year spot checks** (Total revenues, Net income, EPS + 8 more, FY25): dark-green links
   equal the audited Model annuals to the dollar — PASS (diff 0.0000 on all).
3. **Focal-year (FY26E) and FY27/28E spot checks**: driver-built values tie the Model's annual
   estimates at seed — PASS (23 lines per year, worst relative difference ~3e-10). Totals not
   consensus-pinned, so no residual rows exist; all four red check rows read 0/"-" everywhere.
4. **Wiggle test**: FY26E options contracts +10% → Options rev +140.9, txn total/total rev/PT
   +140.9, taxes +28.4 (at the 20.1% input), NI +112.5, EPS +$0.124, EBITDA/Adj EBITDA +140.9 —
   chain is live; performed on a scratch copy, deliverable seeds untouched.
5. **% rows compute in-tab** (IFERROR-wrapped, off Mini cells); VA whole-percent handling: no VA
   ratio rows are linked (NIM/tax-rate/margins computed in-tab; AUC/NNA/market/acquired links
   carry /1000 for $bn), so no /100 cells were needed. No yellow on any formula — PASS (0).
6. **Formatting read-back** — PASS: whole tab Calibri 9 (0 violations); color roles exact
   (#006600 links only to VAActuals, 165 cells; blue #0000FF only on inputs (84, all on #FFFFCC)
   plus the bold "Estimates" header label; gray #7F7F7F italic computed rows; red #FF0000 italic
   Street/check rows, 76 cells; no #008000 anywhere); gridlines off; no freeze panes; focal
   FY26E shape present at column O, weight 12700 EMU (1pt), y=0, rows 1–117 (verified in the
   drawing XML and by PDF image render of the sheet).
7. This file is the spec's item-7 statement: data surface = **VAActuals**; totals **fully
   driver-built** (not consensus-pinned); seed-tie numbers in the table above.

## Follow-ups for the analyst
- Open on a Bloomberg/VA desktop and let VAActuals refresh; the actual-year columns, Street rows,
  and the four red check rows then read against live VA (check rows should sit at ~0; the
  platform-assets walk row will absorb any VA acquired-assets vs NNA composition differences).
- If rates/markets have moved, re-mark the blue NII (IEA, NIM), market-gain, and AI-overlay seeds
  to the live Model annuals (cells O31:Q31, O33:Q33, O95:Q95, O27:Q27).
- If you prefer the consensus-pinned variant, say so and the three totals + residual rows can be
  switched per the finished-model pattern.
