# Revisions tab — estimate-revision tracker (downstream of the Model tab)

Read this when you reach **Build order step 9**. Prerequisite: the Model tab is fully built and
has passed its audit (actuals tie to $0, estimates tie consensus, every check row 0), and the
Model row/column map is frozen. You built that map — do **not** re-discover it here.

## What it is
A one-page tracker showing, for the next ~3 unreported quarters plus the current and next two
fiscal years, three columns per period — **Old** (frozen snapshot of prior estimates, blue
hardcodes), **New** (live green links to the Model tab), **Chg** (black formula, red when
negative) — for the key income-statement lines and KPIs. A hidden-to-the-right **"From Model"
staging block** does all the Model linking so the display block stays clean.

## How the chained flow changes the standalone steps
- **No discovery pass.** The standalone skill opens by locating the Model tab and recording row
  numbers and quarter columns. You already hold that map from building the Model — reuse it. The
  only thing to confirm is which rows you want to *track* (below).
- **Font is Calibri 9pt**, matching the harmonized workbook — NOT Aptos Narrow. This overrides the
  standalone skill's default. Everything else about the format is unchanged.
- **No external reference workbook.** The standalone skill points at `HOOD Model vHS1.xlsx` as a
  visual template; here you're building on the model you just made, so links are all local (`Model!…`).
- **Consensus is not needed.** Revisions is Old-vs-New-vs-Chg; both sides come from the model, so
  there's no Street/consensus dependency (that's the Drivers tab's concern, not this one).

## Step A — Pick the rows to track (from the map you already have)
Track: revenue lines + total, opex lines + total, pretax income, tax rate, net income, diluted EPS,
EBITDA (if the model carries it), and 3-5 operating KPIs (platform assets, net deposits, customers,
ARPU — adapt per company/sector). Write the line-item → Model row map and the period → Model column
map (next 3 unreported quarters + current FY + 2 forward FYs) into your plan before touching cells.

## Step B — Sheet skeleton (rows and labels)
Create sheet "Revisions". Font everywhere: **Calibri 9pt**. Column widths: A–C ≈ 8.25, D = 12
(section-label column), E ≈ 160 (line labels), each Old/New/Chg column ≈ 55, one narrow spacer
(~10) between period blocks.

Row layout (keep the gaps — they carry the visual rhythm):

| Row | Content |
|---|---|
| 2 | Title "Revisions" in B2, bold; **medium bottom border across B2:H2** |
| 3 | Period headers (bold, one per block, medium top border across each block) |
| 4 | "Old" / "New" / "Chg" — italic, right-aligned, thin bottom border |
| 8 | Section label in D: "Revenue" (bold + underline) |
| 9–11 | Revenue line items (labels in E) |
| 12 | Total net revenue (bold label) |
| 14 | Section label "% Y/Y" (italic + underline) |
| 15–18 | Same revenue lines, Y/Y % (row above total gets underline border style) |
| 20 | Section label "Operating Expenses" (bold + underline) |
| 21–26 | Opex line items |
| 27 | Total operating expenses |
| 28 | % Y/Y |
| 30–33 | PT Income / % Y/Y / PT Margin / # Y/Y (bps) |
| 35–36 | Tax Rate / Net Income (bold) |
| 38–39 | EPS (Diluted) (bold) / % Y/Y |
| 41–43 | EBITDA / % Y/Y / EBITDA Margin |
| 44 | Section label "KPIs" (bold + underline) |
| 45–48 | KPI lines |

Adapt row counts to the company's line items but keep the section order and blank-row rhythm.
Done when: labels render in D/E with correct bold/italic/underline styling.

## Step C — Staging block ("From Model"), far right (start ~col AD)
- AD2: "From Model" (bold, medium bottom border).
- Row 3: one column per historical + forecast quarter ("1Q25" … "4Q28", bold, centered, medium top
  border), then annual columns "2026E", "2027E", "2028E".
- **Quarterly columns**: each line links DIRECTLY to the Model tab cell, e.g. `=Model!AO23`. Totals
  computed in-block: `=SUM(AI9:AI11)`. Derived rows computed in-block off Model prior-year cells:
  - % Y/Y: `=IFERROR(AI9/Model!AK23-1,0)` (same quarter prior year)
  - PT Income: `=AI12-AI27`; PT Margin: `=IFERROR(AI30/AI12,0)`
  - Margin Δ bps: `=(AI32-IFERROR(Model!AK74/Model!AK26,0))*10000`
- **Annual columns**: flows are 4-quarter sums of Model rows, e.g. `=SUM(Model!AN23:AQ23)`;
  point-in-time items (period-end KPIs, tax rate, EPS if the model has an annual EPS row) link to
  the Q4 or annual Model cell; Y/Y off the prior annual staging column once one exists
  (`=IFERROR(AV30/AU30-1,0)`).
- All staging cells: **green font (#008000)**, same number formats as the display block.
Done when: staging values tie to the Model tab (spot-check total revenue and EPS per period).

## Step D — Display blocks (Old / New / Chg per period)
One 3-column block per display period, separated by one spacer column (blocks at F:H, J:L, N:P,
R:T, V:X, Z:AB in the reference layout).
- **Old** column: HARDCODED values (blue font #0000FF) — snapshot the current staging values (paste
  the staging column's computed values as static numbers).
- **New** column: simple green links to the matching staging column, `=AI9`, `=AI10`, … one-for-one
  by row.
- **Chg** column (black font), formula depends on row type:
  - $ line items & KPIs: `=IFERROR((New-Old)/Old,0)` formatted `0.0%;(0.0%);-`
  - % rows (Y/Y %, margins, tax rate): `=(New-Old)*10000` formatted `#,##0;(#,##0);-` (bps)
  - Already-in-bps rows: `=New-Old`
Done when: every Chg cell is 0 (or ~0) immediately after building, since Old was just snapshotted
from New.

## Step E — Number formats & emphasis
- $ millions: `_(* #,##0_);_(* (#,##0);_(* "-"_);_(@_)`
- Percent: `0.0%;(0.0%);-`  ·  bps: `#,##0;(#,##0);-`
- EPS: `$#,##0.00;($#,##0.00);-`  ·  KPI $: `$#,##0;($#,##0);-`  ·  KPI counts: `#,##0.0;(#,##0.0);-`
- Bold: total net revenue, Net Income, EPS rows (label + all three columns).
- Color convention: blue = hardcode (Old), green = link (New + staging), black = calc (Chg).
Done when: a read-back of one full period block shows the formats above.

## Step F — Conditional formatting on Chg columns
For EACH Chg column, rows 9:48 (or your last row), add two CellValue rules:
- value < 0 → font red #FF0000
- value > 0 → font black #000000
Use `execute_office_js` `conditionalFormats.add("CellValue")`.
Done when: reading conditionalFormats back shows 2 rules per Chg column.

## Step G — Verify
- Spot-check 3 lines per period: New ties to staging, staging ties to Model.
- Check no #REF!/#VALUE! anywhere on the sheet.
- Confirm Chg columns are all zero at build time.
- Confirm the whole tab is Calibri 9pt (font harmonization with the Model + Drivers tabs).

## Ongoing workflow (state this in the reply)
When new estimates are published: copy each **New** column → paste-special **values** into the
adjacent **Old** column. New stays live off the model; Chg then shows the revision vs the frozen
snapshot. Never overwrite New with values.
