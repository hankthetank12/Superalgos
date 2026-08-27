# 1 Pager + NTM PE — the default valuation pair (built after the Qtr tab)

Two linked tabs forming a self-contained risk/reward + relative-multiple dashboard. This pair — not
a DCF — is the standing valuation surface of the finished models; build it on every full-model pass
(the DCF is opt-in only, see SKILL.md). Spec distilled from the live HOOD/BX pair and the analyst's
own "Replication Guide". The pair couples to the rest of the workbook through only THREE
touch-points: the ticker cell and two Model-EPS links.

**Bloomberg reality**: both tabs are BDP/BDH-formula-driven. Those formulas CANNOT evaluate in this
build environment — write them anyway, exactly as specified; they self-heal when the user opens the
file with the Bloomberg add-in. Never fake pulled values; never "verify" these cells at build time
beyond formula-string correctness. State in the reply that the Bloomberg cells will populate on the
user's desktop.

## Tab 1 — "1 Pager" (layout ~B1:O64, Calibri 9, gridlines off)

- **B1**: the master ticker, blue-on-#FFFFCC input, e.g. `HOOD US Equity` — drives every pull on
  both tabs. **H1**: `=TODAY()` (blue-on-yellow).
- **B3**: title `Risk reward / comp summary` (bold).
- **Valuation scenarios — two out-year blocks** (rows ~4–22): pick the out-year (FY+2) and the
  near year (FY+1).
  - Header row: `Bear` / `Base` / `Bull` / `Street*` across C:F; `Valuation Date:` label with the
    date (blue) at B5.
  - Per block: `<Year> EPS` — Bear and Bull are blue inputs; **Base = dark-green #006600 link to the
    Model's annual EPS cell**; Street = red link to the consensus source (VAActuals annual EPS or
    the Model's consensus strip). `% Y/Y` gray row under the EPS row (vs the current base year).
  - `Multiple` row — three blue inputs (Bear/Base/Bull); `PEG` gray memo row (`=multiple/(growth×100)`).
  - `Share Price` = EPS × multiple (bold); Street column `=BDP($B$1,"PX_LAST")` red.
  - `Upside/Downside` = scenario price / current price − 1 (italic).
  - `R/R (for LONG) - Base` `=base upside / bear downside × −1` and `R/R (for LONG) - Upside`
    `=bull upside / bear downside × −1` (bold).
- **Key stats block** (H4:I11, all `_xll.`-prefix-free BDP/BDH formulas keyed off $B$1): Stock price
  (`=F19`-style link to the live Street price cell), Market Cap (`BDH CUR_MKT_CAP`), Enterprise
  Value (`BDH CURR_ENTP_VAL`), ADTV (`BDP VOLUME_AVG_90D × price /1e6`), 90D Realized Vol
  (`BDH "VOLATILITY 90D"/100`), Implied 1-Day Move (`=vol/SQRT(252)`), SI % of float.
- **Correlation stack** (K5:L10): 90D CORR COEF vs SPX and the house factor baskets the user tracks
  (long/short baskets, momentum, quality, crowding indices) via
  `BDP($B$1,"CORR COEF","BETA_OVERRIDE_START_DT",TEXT(H$1-90,"YYYYMMDD"),"BETA_OVERRIDE_END_DT",TEXT(H$1,"YYYYMMDD"),"BETA_OVERRIDE_REL_INDEX=<idx>")`,
  IFERROR-wrapped. Keep the basket list from the reference build unless the user gives their own.
- **Relative-multiple grids ×2** (vs index 1, e.g. SPX, rows ~13–30; vs index 2, e.g. QQQ, rows
  ~34–50): `Current Multiples` — index NTM P/E `='NTM PE'!H7` (green), subject NTM P/E
  `='NTM PE'!C7` (green), ratio row `=subject/index` with a concatenated label (`=H16&" / "&H15`);
  then the grid: index-multiple ladder across the top (blue anchor + `=prior+2` steps), subject-P/E
  ladder down the left (blue anchor + `=prior+5` steps), body `=$subject-multiple / index-multiple`
  — the relative-multiple surface. Beneath each grid: `1 St. Cheap:` / `Average:` / `1 St.
  Expensive:` — blue-on-yellow thresholds, ideally LINKED to the NTM PE stat cells (`='NTM PE'!L7`,
  `J7`, `K7` and `R7/P7/Q7`) so they self-update.
- **Stock performance block** (H52+): YTD / last week / last month / last 3 months / 2 years —
  `=current px / BDH("PX LAST", <date math on H1>) − 1`.
- **IR contact block** (B52+): names/emails from the company's IR page (Step 0 materials).

## Tab 2 — "NTM PE" (valuation history engine)

- **D1**: `='1 Pager'!B1` (subject ticker — auto-follows; never edit). **V1 / Y1**: comparison
  index tickers, blue inputs (defaults `SPX Index`, `CCMP Index` — swap per user).
- **Three BDH history spills** (~10 years, weekly or daily per the reference): `B7` subject
  `=BDH(D1,"BEST_PE_RATIO",<start>,<end>,"BEST_FPERIOD_OVERRIDE=1BF",…)` spilling date+value into
  B:C; `U7` index-1 and `X7` index-2 pulls spilling into U:V and X:Y. At build time these are dead
  formulas — do NOT attempt to write 6,000 rows of values.
- **Date alignment**: `H7`/`N7` columns VLOOKUP the subject dates into the index spills so the three
  series align by date. **Relative multiples**: `I7` = subject ÷ index-1, `O7` = subject ÷ index-2.
- **Stat bands**: `D7/E7/F7` = median / +1σ / −1σ of the subject's own NTM P/E; `J7/K7/L7` same for
  relative-to-index-1; `P7/Q7/R7` for relative-to-index-2 (MEDIAN / MEDIAN+STDEV.P / MEDIAN−STDEV.P
  over the aligned history).
- These stat cells are what the 1 Pager thresholds link to (I15/I16/I33 current multiples;
  I28:I30 and I46:I48 bands).

## Replication contract (state in the reply)

The pair's only external wiring: `'1 Pager'!B1` (ticker), `'1 Pager'!D7` and `D15` (Model annual-EPS
links for the two valuation years — POINT THESE AT THE JUST-BUILT MODEL's annual EPS cells and name
them in the reply). Everything else is internal or Bloomberg-driven. When the Model's annual columns
move (update mode), re-point these two links.

## Verify before done
1. Ticker cell, both Model-EPS links, and the Street EPS links resolve to the intended cells (read
   the formula strings; the Model links must show live values).
2. Scenario math chains compute (price = EPS × multiple; upside; R/R) off the linked Base EPS.
3. Grid ladders and ratio bodies compute; threshold cells linked to NTM PE stats (or blue inputs if
   the user prefers static).
4. Bloomberg formulas are string-correct (`BDP`/`BDH` argument order, TEXT date math) — no fabricated
   values anywhere; NTM PE spills left dead with a note.
5. Both tabs Calibri 9, gridlines off; 1 Pager fits one screen (~B1:O64).
