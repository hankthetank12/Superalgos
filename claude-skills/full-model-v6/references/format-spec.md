# Format spec — the single source of truth for colors, fonts, number formats, borders, banners

Read this before laying out any tab, and treat it as canonical: SKILL.md and the other references
POINT here rather than restating these rules. If another file appears to conflict with this one,
this file wins. `scripts/audit_model.py` enforces the machine-checkable subset.

## Font
- **Base font: Calibri 9pt for every tab this skill builds** (Model + all downstream tabs). A cell in
  another font/family is a formatting error on a NEW build. Exception: when UPDATING an existing
  workbook that uses another face (e.g. a legacy Arial 10 model), match the existing tab's font —
  never reformat a living workbook wholesale.
- Block headers (statement sections, engine block titles, driven-block headers) are **bold +
  single-underline** — the underline means "a block builds to this line". Subtotals/totals bold.

## Font-color roles (what a color MEANS)
- **Blue #0000FF, no fill** — hardcoded ACTUALS (press release, monthly disclosures, sourced market
  data — with cell-note citations on web-sourced figures).
- **Blue #0000FF on #FFFFCC** — forward ASSUMPTION inputs, estimate columns only; never on a formula
  cell. Every forecast rests on one.
- **Green #008000** — engine output → P&L links and other cross-row/cross-tab MODEL links.
- **Dark green #006600** — links whose source is a DATA surface: VAActuals/consensus-tab actual
  values (Mini Model actual years, Summary IS pulls where used), Daloopa staging pulls, 1 Pager →
  Model EPS links. Distinguishes "pulled from data" from "engine wiring" green.
- **Red #FF0000 (italic for memo rows)** — plugs/residuals, consensus/Street/benchmark rows, check
  rows, seasonality rows (see below). Red OVERRIDES green: a consensus link is red, never green.
- **Red on #FFCCCC** — balance-sheet cash plug.
- **Black** — calculations.
- **Gray #7F7F7F italic** — computed % Y/Y, % Q/Q, # Y/Y, ratio memos, derived-KPI rows.
- **Italic #333F4F, centered in data columns** — mechanical scaffold memos (day counts,
  annualization factors, avg-price memos).
- **#D9D9D9 (or #B2B2B2) font** — parked/de-emphasized helper and commentary labels.
- **Violet #7030A0 italic** — management guidance ONLY (label `Mgmt Guidance (source, date)`').
  Never reuse violet for any computed row.
- **Seasonality rows are red #FF0000 italic** — both the `Seasonality` rows under % Q/Q blocks and
  the `Seasonals` / `Vs Normal Seasonality` rows under monthly % M/M / # M/M blocks. (Live builds
  historically mixed brown #833C0C and red; red is the standard going forward.)
- Optional workflow convention (never required): an input awaiting better data may carry a
  **#C00000 red fill** as an attention flag for the analyst; list any such cells in the reply.

## Fills (role-locked)
- **#FFFFCC** — assumption inputs (with blue font) only. One sanctioned exception: a *self-setting*
  input — a cell the analyst treats as an input that computes its own default, e.g. the 1 Pager's
  valuation-date `=TODAY()` — keeps the blue-on-#FFFFCC input treatment even though it holds a
  formula, because its ROLE is "type over this to pin a date". These are rare and must be named in
  the reply; every other formula on yellow is a build error.
- **#F2F2F2** — headline ratio bands (margins, efficiency) and the EPS-strip band.
- **#375623** — tier-1 banners: the period banner row and MAJOR engine-section rows (white bold,
  title at the label start column, terse titles).
- **#FFF2CC** — tier-2 sub-section banners (black bold, title one column right of tier 1).
- **#FFEA8F** — tier-3 banners for REPEATING CHILD blocks inside an engine — one per product
  (Options / Equities / Crypto), per fund (each flagship), per region — placed one column right of
  tier 2. Use tier 3 only when an engine repeats the same block shape N times; a two-level model
  never needs it.
- **#CCCCFF** — `Memo:` block header labels only.
- **#DAE9F8** — DCF terminal-multiple inputs; **#FBE2D5** — DCF section boxes & scenario overrides.
- These fills never appear in any other role. No other fills without a stated reason.

## Number formats (exact strings)
- $mm accounting: `_(* #,##0_);_(* (#,##0);_(* "-"?_);_(@_)` (single `?` pad on whole-number rows).
- 2-dp accounting: `_(* #,##0.00_);_(* (#,##0.00);_(* "-"??_);_(@_)` (`??` pads dashes).
- Growth: `0.0%;(0.0%);-` · rates/spreads/NIM: `0.00%` · EPS: `$#,##0.00` · shares: `#,##0.0`.
- Per-unit capture: `$#,##0.00` or `$#,##0.000` · dates: `m/d/yyyy` · bps deltas: `#,##0;(#,##0);-`.
- VA/Daloopa whole-percent ratios: `0.000` and divide by 100 wherever they meet a fraction.
- Multiples: `0.0"x"`.
- Any `*1000` / `/1000000` scaler requires units in the row label or header ("$mm", "$bn", "#") —
  no bare unit scalers; mismatched units between engine and P&L are a build error.

## Label indentation
The further left, the more headline: C statement lines (Revenues, Expenses, Profit, Net income,
EPS) → D key totals / engine outputs feeding the P&L → E business subtotals / primary lines → F
sub-components → G deepest detail and operating-driver rows (deep intensity blocks may go H–J).
% rows sit in the same column as (or one right of) their line, with leading spaces. These are
OFFSETS from the label origin — see "Adaptive grid" in model-engine.md; the hierarchy shape is the
rule, not the absolute letters.

## Period banner row (tier-1, exact spec)
The single dark-green period-header row is the visual spine:
- **Placement & freeze**: the LAST row of the frozen header block — freeze panes immediately below
  it and after the last label column. Compact row height (~12pt).
- **Fill & font**: #375623, white bold, base font. Fill runs CONTINUOUSLY from column B (or the
  label origin) through the last quarter column, BREAKS at the spacer column(s), resumes over the
  annual columns. Column A stays unfilled.
- **Alignment**: left over the label area; right-aligned in the tag column and every data column.
- **Labels are formulas, never typed**: each quarter cell concatenates the scaffold rows
  (`=<qtrLabel>&<fiscalYear>` → "1Q26"); annual cells show the fiscal-year INTEGER linked /
  incremented (`=prior+1`) from the scaffold.
- **White fiscal-year separators**: MEDIUM WHITE vertical borders inside the banner group each
  fiscal year into a 4-quarter block — (a) right edge of the last label column; (b) left edge of
  every 1Q column AND right edge of every 4Q column (set both edges — the rule survives either
  neighbor being reformatted); (c) the spacer seam after the last quarter. Banner row only. These
  are the ONLY medium-weight and only white borders on the sheet.
- **Maintenance**: when quarter columns are appended, extend fill + label formulas and RE-DRAW the
  separators; verify by image — border correctness cannot be confirmed from value reads.

## Borders & boxes
- **Subtotal top/bottom rules span from the row's label column through the last data column** —
  covering label text and indent cells, continuous. Monthly blocks: thin bottom rule under Month 3,
  thin top rule on the Total row, both label→numbers. Sweep mechanics: for each non-pair row read
  EdgeTop/EdgeBottom over the data range; `Continuous` or `null` (mixed) → re-apply uniformly across
  `{labelCol}:{lastDataCol}`. Skip banner rows; EXCLUDE Annual-pair rows and guidance rows from the
  sweep (a full-width rule cuts through their boxes/annotations).
- **Annual + % Y/Y boxed pairs** on the P&L AND every engine subtotal/output line, in 4Q columns
  only: Annual `=SUM(4 trailing qtrs)` bold (EOP stocks link the 4Q value), % Y/Y vs the prior
  year's annual beneath, labels in the parent's column. **Draw each box as ONE 2-cell range setting
  all four edges at once, with a two-phase clear-then-box write** (clear all pair-row borders
  full-width, sync, then draw boxes, sync) — a cell's right edge is its neighbor's left edge and
  single-pass clearing wipes box right borders.
- Driver-block top-rule: thin black top border on every driver-fed line.
- **Focal columns are SHAPES** (weight 1, y=0, full model height) — one on the focal quarter, one on
  the focal annual column; resize after row inserts. (The Qtr tab is the exception — no focal shape.)

## Gridlines & panes
Gridlines OFF on every built tab. Freeze panes below the period banner / after the label block on
the Model tab; per-tab rules in each tab's reference (Mini Model: no freeze panes).

## Verification split
- `scripts/audit_model.py` checks the static subset (fonts, fill/color roles, yellow-on-formula,
  SUMIFS identity, link policy, error cells).
- Borders, banner separators, boxes, and shapes are verified **by image** (`getImage`) — they cannot
  be confirmed from value reads. Two-phase writes above exist precisely because of this.
