# Drivers tab — model estimate vs Street consensus (downstream of the Model tab)

Read this when you reach the Drivers build-order step. Prerequisite: the Model tab is fully built and has
passed its audit, and the Model row/column map is frozen. You built that map — do **not** re-discover
it. This is the v2 Drivers build (KPI-vs-consensus **plus** operating-driver breakdowns: AUM, FPAUM,
performance income by strategy).

A **Drivers** tab is a side-by-side "model estimate vs Street consensus" view of the company's key
income-statement KPIs (and operating drivers), across annual and quarterly periods.

## How the chained flow changes the standalone steps
- **No discovery pass for the Model.** The standalone skill opens by finding the Model period-header
  row, quarter columns, and KPI rows. You already hold all of that from building the Model — reuse it.
- **Consensus source = the ladder the Model resolved** (SKILL.md § Consensus-source ladder):
  1. If the workbook has a **VAActuals / consensus tab**, link Street columns to it (the formula
     patterns below use `VAActuals!…`).
  2. Otherwise point the Street columns at the Model's **red hardcoded consensus snapshot** (build a
     small consensus staging block on the Drivers tab holding those per-KPI values if the Model
     doesn't already stage them; dormant BQL formulas may sit beside it only if the user wants
     refresh-on-open pulls). Substitute `{consensusRef}` for `VAActuals` in every Street formula
     below.
  Either way the actuals-tie discipline is identical (see "Map by economic equivalence").
- **Font is already Calibri 9pt** — consistent with the harmonized Model + Revisions tabs; no change.
- **No external reference workbook.** Model/consensus links are local tabs, not an external file.

## Inputs to confirm (mostly already in hand)
1. **Model tab** — you know the period header row and which columns are which quarter/annual. Note:
   annual columns in the detailed/summary-IS section are frequently **empty**, so annual figures are
   built by SUMMing the 4 quarter columns.
2. **Consensus source** — resolved per the priority above. If a VAActuals tab: find the line-item
   label column (often col C) and the period columns; record quarterly AND annual columns; watch for
   a **gap column** in the consensus quarterly strip (one blank column between the last actual quarter
   and the first estimate quarter). If a BQL/BDP staging block: lay out one column per period matching
   the Model's quarters/years.
3. **Reference Drivers tab (optional visual template).** If the user points at an existing Drivers tab
   for the exact look, read its title, header rows, one full KPI block (`includeStyles:true`), column
   widths, and freeze panes. Absent one, use the layout below.

Done when: you have a column-mapping table (Drivers column → Model column(s) → consensus column) for
every period, and a KPI row map (KPI → Model row → consensus row/field).

## Layout
- **Title** in B2 (bold ~14pt) with a medium bottom border across the used width.
- **Annual columns** K:Q (e.g. 2022A…2028E), **gap column R**, then **quarterly columns S onward**
  (e.g. 1Q24…4Q28 = 20 quarters). Period labels in row 4 (bold 9pt, right-aligned, thin bottom
  border). Actual years get "A"; estimates get "E".
- **Freeze panes** (e.g. A1:J4). Column widths: label col B ~180, spacer cols C:J ~3.8, annual ~62,
  gap R ~12, quarterly ~54.
- **Section bands**: full-width row, gray fill (#D9D9D9), bold ~10pt, thin top+bottom borders
  (e.g. "REVENUE", "EARNINGS").
- **KPI blocks = 8 rows each**, value row = block start `s`: `s` Value, `s+1` % Y/Y, `s+2` % Q/Q,
  `s+3` Street, `s+4` % Y/Y (Street), `s+5` % Q/Q (Street), `s+6` Vs Street, `s+7` blank spacer.

## Color & number-format convention (Street style)
- **Value row** (model): green **#008000**, bold 9pt, light-gray fill **#F2F2F2** across the row
  (incl. gap R). $ lines: `_(* #,##0_);_(* (#,##0);_(* "-"_);_(@_)`; per-share: 2-decimal variant;
  margin/ratio: `0.0%;(0.0%);"-"`.
- **Value label** (col B): bold 9pt black, #F2F2F2 fill.
- **Street row**: red **#FF0000**, bold 9pt; same number format as its value row. Label "Street" bold red.
- **Growth labels** ("% Y/Y","% Q/Q"): italic 9pt gray **#7F7F7F**.
- **Model growth data** (s+1,s+2): black 9pt, `0.0%;(0.0%);"-"`. **Street growth** (s+4,s+5): red 9pt,
  same. **Vs Street** (s+6): black bold 9pt, same.
- Default font Calibri 9pt throughout.

## Formula patterns (wrap every formula in `IFERROR(...,"")`)
`{consensusRef}` = the VAActuals tab or the BQL/BDP consensus staging block (see sourcing above).
For a KPI with Model row `mr`, consensus row `vr`, value-row start `s`:
- **Annual value (model)** = `=IFERROR(SUM(Model!{q1col}{mr}:{q4col}{mr}),"")` (year's 4 Model quarter cols).
- **Annual Street** = `=IFERROR({consensusRef}!{annualCol}{vr},"")`.
- **Quarterly value (model)** = `=IFERROR(Model!{qcol}{mr},"")`. **Quarterly Street** =
  `=IFERROR({consensusRef}!{qcol}{vr},"")` (mind the gap column if using VAActuals).
- **% Y/Y**: annual = `={col}{s}/{prevAnnualCol}{s}-1` (blank for first annual col); quarterly =
  `={col}{s}/{col-4quarters}{s}-1` (blank for first 4 quarters). Street rows mirror on `s+3`.
- **% Q/Q**: annual = blank; quarterly = `={col}{s}/{prevQtrCol}{s}-1` (blank for first quarter).
- **Vs Street** (every column) = `={col}{s}/{col}{s+3}-1`.
- **Margin lines**: model annual = `=SUM(Model!{q1}{FRErow}:{q4}{FRErow})/SUM(Model!{q1}{REVrow}:{q4}{REVrow})`;
  quarterly = model's margin row. If consensus stores margin ×100 (21.0 = 21%), divide by 100 so both
  sides are fractions; format `0.0%`.

Suspend calculation before bulk-writing (`calculationMode="Manual"`), restore after, then
`application.calculate(FullRebuild)` — else a manual-calc workbook shows stale zeros.

## KPI mapping (the analytical core)
Map each KPI to its Model row and consensus row/field. Alt-asset-manager standard set: Management
fees, Fee-related performance revenue, Transaction/monitoring & other fees, **Total fee-related
revenue**, Fee-related expenses, **Fee-Related Earnings (FRE)**, FRE margin, Distributable Earnings,
After-tax DE, **EPS (after-tax DE/share)**. Adapt to sector — for brokers/exchanges use the model's
own segment cut (commissions, NII, transaction-based, etc.).

**Map by economic equivalence, not by label.** In actual periods the model links to reported actuals
and Street for a reported quarter *is* the reported actual, so model and consensus for the same line
MUST match (Vs Street ≈ 0). Validate by probing an actual quarter. **If two lines have swapped labels
between Model and consensus** (e.g. Credit vs Real Estate), pair by matching amount so actuals tie,
display the more-authoritative (Visible Alpha, if used) label, and flag the swap.

## Revenue / segment breakdown
Place component blocks **directly above** the line they sum to (e.g. the platform blocks immediately
above the "Management fees" total). Build each component the same way (model + Street + growth + Vs
Street).

## Supplementary driver sections (AUM / FPAUM / performance income by strategy)
Beyond fee KPIs, users often want operating drivers by strategy/segment, each as its own section
(same 8-row block, same colors).
- **Annual treatment depends on metric type:** flow metrics (fees, performance income) = SUM of the 4
  quarter columns; stock/period-end metrics (AUM) = the year-end (4Q) value, *not* a sum (map both
  model and Street annual to each year's Q4 column); average measures (Average FPAuM) = AVERAGE of the
  4 quarter values (mind the consensus gap column when the four quarters are non-contiguous, e.g.
  AVERAGE of AC, AE, AF, AG).
- **One-sided metrics:** a metric may exist only in the Model (e.g. net performance income) or only in
  consensus (e.g. Average FPAuM by strategy). Populate the side that has it; leave the other blank
  until the counterpart is found — green = model, red = Street. Vs Street stays blank when one side is
  empty.
- **Filling a deferred side later:** when the user points you to source rows (e.g. "Model FPAUM by
  product starts at row 185"), map each product to its Model row, write value/%Y/Y/%Q/Q and the
  now-computable Vs Street, and use the SAME annual basis as the already-populated side (e.g. AVERAGE
  of 4 quarters to match consensus "Average FPAuM"). Verify the product rows tie to the section total.
- **Basis mismatches:** if one strategy is on a different basis in the Model (e.g. Market Solutions AUM
  stored as an average while others are period-end), map it to the consensus row with the matching
  value so actuals tie, and note it.
- **Model-own series won't tie perfectly:** when the model figure is the analyst's own estimate (not a
  link to reported actuals), expect small non-zero Vs Street even in actual periods (e.g. model FPAUM
  vs consensus Average FPAuM ran ~1–4%). That is a real difference, not a wiring error.
- **Performance income caveat:** by-strategy "performance fees" rows often do NOT reconcile to net
  "Total performance income" (gross fee-related perf revenue vs net realized performance income are
  different concepts). Confirm which the user means; build a single total block if only the net total
  is clean.

## Borders: top rule only on sum rows
Do **not** put a top border on every block. Put a thin top border (across the data columns) **only on
rows where the lines directly above sum to it** — true subtotals/totals (e.g. "Management fees" = sum
of the segment blocks above; "Total fee-related revenue"; "Total AUM"). Clear EdgeTop on all other
value rows.

## Focal-period boxes (floating shapes, not cell borders)
Frame the current/focal forecast periods with floating rectangle **shapes** overlaid on the grid (so
they don't disturb data or fills):
- One rectangle around the **focal annual column** (current estimate year, e.g. 2026E) and one around
  the **focal quarter column** (next/current estimate quarter, e.g. 2Q26E — the first estimate quarter,
  right after the last actual).
- Each shape: **no fill**, thin black outline (weight ~1pt, single solid #000000), one column wide,
  spanning the full height of the grid (top 0, height covering all blocks — make it tall enough to
  cover later-added sections).
- Position by points: cumulate column widths from A for the left edge; set `width` to that column's width.
```javascript
const box = sh.shapes.addGeometricShape(Excel.GeometricShapeType.rectangle);
box.left = focalColLeftPts; box.top = 0; box.width = focalColWidthPts; box.height = gridHeightPts;
box.fill.clear();
box.lineFormat.color = "#000000"; box.lineFormat.weight = 1; box.lineFormat.style = "Single";
await context.sync();
```

## Verification before reporting done
1. Recalc (FullRebuild) and scan the whole grid for `#` errors — expect zero.
2. Confirm **actual periods tie to Street** (Vs Street ≈ 0) and estimate periods diverge — proves the
   mapping (except analyst-own driver series, which may show small actual-period differences — see above).
3. Confirm any **breakdown sums to its total** in every column.
4. If rows were inserted in the Model after this build, confirm Excel auto-adjusted the Drivers
   cross-sheet references (spot-check a cell) and they still tie — and re-run the Model audit.
5. Render an image of a section to confirm format (colors, single top rule on sum rows, focal-period
   boxes) and that the tab is Calibri 9pt.
6. Flag data caveats: label swaps, pro-forma vs as-reported periods, consensus stub-period quirks,
   one-sided/own-series metrics, and which consensus source (VAActuals vs Bloomberg staging) was used.
