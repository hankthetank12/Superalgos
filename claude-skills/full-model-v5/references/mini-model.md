# Mini Model tab — VA-linked annual mini-model (second tab built)

Read this when you reach the Mini Model build-order step — the first downstream build after the
Model audit gate, making it the second tab in the workbook. Prerequisite: the Model has passed its
audit and its row/column map is frozen.

## What it is — a compact annual KPI model on the workbook's DATA surface
A KPI-driven **annual** mini-model in Street "Mini Model" format — one column per fiscal year, the
P&L plus key KPIs/drivers, per-share and Street-comparison blocks, strict color convention, and the
focal forecast year framed by a floating shape. It matches the analyst's standalone mini-model
convention (mini-model-v7-x): **actual years link to the data surface; estimate years build in-tab
from blue drivers.**

- **Actual years**: every P&L line, KPI level, and share count links to **VAActuals** (the Visible
  Alpha tab) in **dark green #006600** — `=VAActuals!BT38`-style, `/100` on whole-percent ratios.
  If the workbook has NO VAActuals/consensus tab, link the Model tab's audited annual columns
  instead (same dark green). Subtotals may be in-tab sums of the linked lines; a red tie memo covers
  any wedge. Actual-year links must tie the audited Model annuals to the dollar.
- **Estimate years**: each line is a formula off Mini Model cells driven by a **blue-on-#FFFFCC
  input** (driver rows above the line they drive; %YY inputs below the level they grow):
  transactional lines as `volume × take-rate` with blue volume/rate inputs; spread lines as
  `avg balance × NIM`; everything else `=Prior*(1+%YY)`. Seed every driver so the estimate ties the
  Model's annual estimate at seed.
- **Consensus-pinned totals (the finished-model pattern)**: key TOTALS (total revenues or its
  transactional subtotal, total opex, the headline adjusted metric) MAY link to the consensus tab's
  estimate-year values so the tab sits AT consensus by construction — then an **`Other /
  reconciling`** residual row (red-logic residual: `=total − Σ components`) absorbs the wedge between
  the driver-built components and the pinned total, and a blue **`Consensus reconciliation (VA
  roll-up)`** input row carries any small roll-up plug to pretax. Use this when the user wants the
  mini model marked to Street; skip the pinning (pure driver build) when they want it fully
  independent — say which was built.
- **% rows**: all % Y/Y, margins, and ratio rows compute IN-TAB off Mini Model cells (`=Cur/Prior-1`,
  IFERROR-wrapped), gray italic. Effective tax rate, % of revenue expense ratios: gray in history,
  blue-on-yellow italic inputs in estimates.
- **Street / Consensus block** near the foot: red italic rows for Street revenue, the headline
  adjusted metric, and EPS (linked to the consensus tab across ALL years), each with a `Model vs
  Street` red row (`=IFERROR(model/street−1,"")`) — actual years ≈ 0, estimate years show the
  variant view.
- **Checks & Sources block** at the foot: revenue component check (`=total − SUM(components)` → 0),
  net-income tie to the data surface, and any source notes.
- **"Base Case"** label above the year headers; header rows `FY22A … FY28E`; an `Actuals` /
  `Estimates` split label pair (dark green / blue bold).
- Layout: title at the top-left; ~5–6 actual years + 3 estimate years; label indent D (sections +
  final subtotals) → E (primary lines) → F (sub-components) → G (drivers/KPIs); data columns ~J–R.
  Calibri 9pt, gridlines OFF, **no freeze panes** (house style), focal-year SHAPE (weight 1, y=0,
  full height) on the focal estimate year.
- Include the company's 4–8 marquee KPIs (from Step 0) as a `Customer & Platform KPIs`-style section
  with the same actual-link / estimate-driver duality.

## Color convention (audit at the end)
- **Dark green #006600** — links to VAActuals (or Model annuals) — actual years, and any
  consensus-pinned totals.
- **Blue #0000FF on #FFFFCC** — estimate-year driver inputs. Never on a formula.
- **Black** — in-tab calcs. **Gray #7F7F7F italic** — computed % rows/ratios.
- **Red #FF0000 italic** — Street/consensus comparison rows, tie memos, residual/reconciling rows.
- **#008000 green** — not used on this tab (its links are data-surface links, which are #006600).

## Verify before done
1. `fullRebuild`; zero `#REF!/#VALUE!`.
2. Spot-check 3 actual-year lines (Total revenues, Net income, EPS): the dark-green links equal the
   audited Model annuals to the dollar (and the VAActuals actuals, which must agree).
3. Spot-check the same lines in the focal estimate year: driver-built values tie the Model's annual
   estimates at seed; if totals are consensus-pinned, the residual rows absorb the wedge and are
   small — flag a residual > ~2% of its total.
4. Wiggle test one blue driver — line, subtotal, EPS move; restore the seed.
5. % rows compute in-tab; whole-percent VA ratios carry `/100`; no yellow on formulas.
6. Formatting read-back: link/driver/computed/Street colors per above, focal-year SHAPE at y=0 full
   height, gridlines off, no freeze panes, whole tab Calibri 9pt.
7. Reply states: the data surface used (VAActuals vs Model annuals), whether totals were
   consensus-pinned or fully driver-built, and the seed-tie numbers.
