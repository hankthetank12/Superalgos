# Mini Model tab — self-contained annual mini-model (second tab built)

Read this when you reach the Mini Model build-order step — the **first downstream build, right after
the Model audit gate**, making it the **second tab** in the workbook (Model → **Mini Model** →
Revisions → Drivers → Qtr). Prerequisite: the Model tab has passed its audit and its row/column map is
frozen (you'll transcribe values FROM it, but the finished Mini Model carries **no live links to it**).

## What it is — SELF-CONTAINED, not a linked mirror
A KPI-driven **annual** mini-model in Street "Mini Model" format — one column per fiscal year, the P&L
plus key KPIs/drivers, a GAAP-vs-Operating EPS reconciliation, strict color convention, accounting
borders, and the focal forecast year framed by a floating shape.

**The Mini Model is driven from the Mini Model.** It does NOT reference the Model tab, and it does NOT
link to a VAActuals/VA tab. Every number on the tab is either (a) a **blue hardcode**, (b) a formula
off **this tab's own cells**, or (c) a red consensus memo. Concretely:
- **Historicals (actual years) are BLUE HARDCODES** — transcribe the values from the Model's audited
  annual columns (which tie to the dollar), but paste them as static blue numbers. No green links to
  the Model; no green links to VAActuals. Never.
- **Estimates build in-tab from HARDCODED blue drivers**: every forward line runs off a blue driver
  input living on this tab — `% Y/Y` growth rates, take rates (% of volume/AUM), NIM/yield levels,
  fee rates, ratio Δs. Seed each driver to the Model's implied annual value (so the Mini Model's
  estimates match the Model/consensus at seed), but the driver itself is a hardcoded blue input, not
  a link. Level lines = `=Prior*(1+%YY)` or `=driver × base` off Mini Model cells only.
- **All % Y/Y, margins, take rates, NIM and ratio rows are COMPUTED IN-TAB** off this tab's own
  figures (`=Cur/Prior-1`, `=rev/volume`, `=NII/avg balance`) — never linked to VAActuals, never
  linked to the Model. In actual years they compute gray off the blue hardcodes; in estimate years
  the driver version IS the blue input and the computed version is omitted (one source of truth).
- **Result**: the tab is a standalone flexable sandbox by construction. Flexing the Model does NOT
  move the Mini Model; re-sync by re-transcribing/re-seeding if the Model changes materially. State
  this in the reply.
- **Font is Calibri 9pt.** Keep the mini-model house style: **gridlines OFF, NEVER freeze panes**.

## Step A — Map Mini Model lines to Model rows (transcription map only)
The Mini Model mirrors the Model's own P&L structure (the Model already has the sector-appropriate
lines). From the frozen Model map:
- Identify the Model's **annual columns** (one per fiscal year) and their year labels; these become
  the Mini Model's year columns, 1:1.
- For each Mini Model P&L line and KPI, record the Model **row** it corresponds to — this map is used
  ONLY to read values for transcription and driver seeding, never to write link formulas.
Typical layout: J=FY-5A … O=FY0A, P=FY1E (focal), Q=FY2E, R=FY3E — but read the Model's annual block
to confirm the count and which years are A vs E.

## Step B — Sheet skeleton
Calibri 9pt. Gridlines OFF, no freeze panes. Columns: A–C narrow (~12pt), D–H label-indent (~14–20pt),
data J–R (~78–80pt). One blank row between major sections. Label indentation by hierarchy:
- **Col D** — section headers (Volume Build, Revenue Build, Operating Expenses, Adj. EBITDA Bridge, Per
  Share) AND final subtotals/outputs (Total net revenues, Total operating expenses, Operating income,
  Pretax income, Net income, Adj. EBITDA, Diluted EPS).
- **Col E** — primary line items beneath each subtotal (opex lines, non-op, tax, EBITDA bridge, diluted
  shares, consensus-comparison rows), primary revenue lines/segment subtotals.
- **Col F** — sub-components rolling up to E lines (each revenue detail line; segment detail).
- **Col G** — deepest detail: driver/KPI rows (ADV, RPC, AUM, fee rate, take rate, NIM, etc.), sitting
  above the line they drive. `% Y/Y`/margin/ratio rows carry a leading-space label and sit in the same
  column as the line they relate to.
Title row with a medium black bottom border; year-header row with a thin black bottom border; Actuals /
Estimates banners; a units note.

## Step C — Historicals: blue hardcodes; Estimates: in-tab driver builds
- **Actual years**: for every P&L line, KPI level, and share count, write the Model's audited annual
  VALUE as a static **blue #0000FF hardcode** (no fill). Subtotals may be black in-tab sums of the
  blue detail lines (`=SUM(cell,cell,…)`), provided they still tie the Model's transcribed subtotal —
  add a red tie memo if a plug is needed.
- **Estimate years**: never hardcode a black number and never link out. Each line is a formula off
  Mini Model cells driven by a **blue-on-#FFFFCC driver input** placed per mini-model convention
  (driver rows above the line they drive; `%YY` inputs below the level they grow):
  - Transactional lines: `volume × take-rate` or `=Prior*(1+%YY)` with the blue %YY below.
  - Spread/NII lines: `avg balance × NIM` with balance rolled off a blue growth input and NIM a blue
    level input (Δ input for ratio lines).
  - Everything else: `=Prior*(1+%YY)` with blue %YY.
  Seed every driver so the estimate ties the Model's annual estimate (which is at consensus) — then
  the tab is free to flex independently.
- **Wiggle test** is mandatory here (unlike a linked build): bump one %YY / take rate / NIM input —
  line, subtotal, and EPS move; restore the seed.

## Step D — Drivers/KPIs and % rows (all in-tab)
- Driver/KPI levels in actual years: blue hardcodes (transcribed). Derived KPIs (blended take rate,
  NIM, fee rate) in actual years: gray italic computed off THIS tab's figures (e.g. `=rev/volume`,
  `0.000` format for whole-percent ratios) — never a link to VAActuals or the Model.
- In estimate years the driver IS the blue input (take rate level, NIM level, %YY).
- `% Y/Y`, margins, and ratio rows compute off Mini Model cells (`=Cur/Prior-1`), gray italic, beneath
  every main line. Whole-percent ratios (take rates, yields, fee rates) use `0.000` (1.425 = 1.425%),
  NOT a percent format.

## Step E — EPS comparison block (match the Model's basis)
Mirror the Model's EPS basis. The model side computes in-tab (Net income / diluted shares, both Mini
Model cells); the consensus side is shown from the Model's consensus source (VAActuals tab if the
workbook has one, else the Bloomberg BQL/BDP staging the Model used), **red italic memo values** —
consensus display rows are the ONLY rows that may reference another tab, and they are red, never green.
- If the Model reports GAAP EPS with an operating add-back: **Diluted EPS (GAAP)** (bold, in-tab);
  **Model Operating EPS** (in-tab `=(NI − adj×(1−ETR))/Shares`, black italic memo); **Consensus
  Operating EPS** (red italic); **Model vs Consensus ($)** and **(%)** = `=IF(Cons=0,"-",Model/Cons-1)`
  (red italic). Never divide by a gap row — the % denominator is consensus EPS.
- If the Model is already operating-basis: a single EPS line and ONE delta row vs consensus.
Because drivers are seeded to the Model (at consensus), the model-vs-consensus deltas sit near 0 in the
seed year — that's the expected tie, and a useful check.

## Color convention (audit at the end)
- **Blue `#0000FF`, no fill** — hardcoded historical actuals (transcribed from the audited Model).
- **Blue `#0000FF` on `#FFFFCC`** — forward driver inputs (%YY, take rate, NIM, ratio Δs) in estimate
  years. Every estimate rests on one; never on a formula cell.
- **Black `#000000`** — in-tab calcs referencing only Mini Model cells (estimate levels, subtotals,
  EBITDA bridge, operating-EPS memo).
- **Gray `#7F7F7F`, italic** — computed `% Y/Y`, margins, ratios, derived KPI rows.
- **Red `#FF0000`, italic** — consensus-comparison memo rows and tie memos. The only permitted
  cross-tab references on this tab, and they are red.
- **Green** — NONE. No green links to the Model, no green links to VAActuals. A green cell on this tab
  is a build error.

## Borders & focal shape (mini-model house style)
- Subtotal top-rules: thin black top border on every bold subtotal/total row, label column → last data
  column. Section-label boxes: thin-black border around the header spanning **D:I** (banner, white fill,
  all four edges) — never a single cell. Key-subtotal bottom-rules under Total net revenues, Total
  operating expenses, Net income, Adj. EBITDA, Diluted EPS. Bold only on subtotals/totals.
- **Focal-year box is a SHAPE, never cell borders**: thin outline (weight 1), pinned to y=0, full model
  height, one column wide, over the focal forecast year. Create the shape, then set weight in a separate
  sync (integer) to avoid InvalidArgument.

## Verify before done
1. `fullRebuild`, then scan the whole tab for `#REF!/#VALUE!` — expect zero.
2. **No external links except red consensus rows**: search formulas for `Model!` and `VAActuals!` —
   any hit outside the red consensus block fails the build.
3. Spot-check 3 actual-year lines (Total net revenues, Net income, EPS): the blue hardcodes equal the
   Model's audited annual values to the dollar. Spot-check the same 3 lines in the focal estimate year:
   the driver-built values tie the Model's annual estimates (at consensus) at seed.
4. Wiggle test: bump one blue driver (%YY, take rate, NIM) — line, subtotal, EPS all move; restore.
5. Confirm `% Y/Y`/ratio rows compute off Mini Model cells; whole-percent ratios formatted `0.000`;
   no yellow on formulas; no green anywhere.
6. Formatting read-back (`includeStyles:true`): blue hardcoded actuals, blue-on-yellow drivers, gray
   computed rows, red consensus rows, D:I banners boxed, subtotal rules, focal-year SHAPE at y=0 full
   height, gridlines off, no freeze panes, whole tab Calibri 9pt.
7. Note the consensus source used for the EPS block (VAActuals vs Bloomberg staging) and state that the
   Mini Model is self-contained (flexing the Model does not move it).
