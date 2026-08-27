# Update mode — maintaining a living model

These workbooks are living documents: quarters print, monthlies drop, guidance restates, estimates
roll. When the user asks to "update", "roll the quarter", "add the new month", "refresh", or hands
you a new press release for an EXISTING model built on this system, follow this file — do NOT
rebuild from scratch, and do NOT reformat tabs you aren't touching. Discover the workbook's layout
first (label/data columns, period banner row, SUMIFS ranges, which tabs exist) and respect it —
including legacy layouts that differ from the fresh-build defaults.

Ordering rule: snapshot Revisions FIRST (step 5 below runs before Model estimates change if the
user wants the revision measured against the old estimates — confirm which side of the update the
snapshot belongs on; default: snapshot BEFORE re-estimating), then actualize, then extend.

## 1. Actualize the printed quarter
- Convert the newly reported quarter's column from estimate to actual: overwrite driver-built
  estimate cells with BLUE HARDCODES from the press release (or Daloopa pulls in Daloopa mode) on
  every reported line; re-wire the block plugs (one red plug per block) so components tie to the
  dollar; the NI tie-memo reads $0.
- Kill the now-stale blue-on-yellow inputs in that column (they become gray/blank or the computed
  version); the EPS strip cell for that quarter flips from green estimate to black/blue actual.
- Update the Actual/Estimate scaffold marker row and any "A/E" labels; move the FOCAL designation to
  the next unreported quarter and MOVE the focal-column shapes (Model, Mini Model, Drivers).
- Fill the quarter's monthly rows from the monthly disclosures; set the new latest-undisclosed month
  as the blue-on-yellow nowcast input.

## 2. Append new estimate columns (when the horizon rolls)
- Insert/extend quarter columns at the right of the quarter block: copy the prior estimate column's
  formulas, re-seed the new quarter's inputs (seasonality-aware), extend the scaffold rows (EOMONTH
  chain, day counts, fiscal-year integers, quarter labels).
- **Extend the period banner** — fill + formula labels — and RE-DRAW the white year separators.
- **Extend the fixed SUMIFS range everywhere in one pass** (it is ONE identical range on every
  annual row/column); re-verify annuals afterward. Add a new annual column when a new fiscal year
  enters the horizon.
- Re-run the border sweep on new columns only; extend gray bands / EPS strip band.

## 3. Refresh data surfaces
- Monthly tab / monthly-in-quarter rows: append the new months (K-tag the source).
- Staging tabs (alt-data, Bloomberg, Daloopa): append new rows; the date-keyed pulls pick them up —
  spot-check the latest month landed.
- VAActuals/consensus: if the user provides refreshed consensus, update the red consensus surface
  (links repoint automatically; hardcoded snapshots get re-keyed with the new as-of date).
- Rates blocks: hardcode the newly published fixings; roll the rate-path Δ inputs.

## 4. Re-seed and sensitize
- Re-seed estimate inputs the user wants marked to the new consensus (ask which: full re-seed vs
  keep the analyst's variant view — DEFAULT: keep existing inputs, report the new model-vs-consensus
  gaps rather than silently re-seeding).
- Re-run the wiggle test on one driver; restore.

## 5. Roll the downstream tabs
- **Revisions**: paste-special VALUES of each New column into its Old column (freezing the prior
  estimates), confirm New stays live off the Model and Chg shows the revision. Never overwrite New
  with values.
- **Drivers / Qtr**: extend period columns to match the Model; move the focal-quarter column/boxes;
  confirm actual periods now tie Street (Vs Street ≈ 0) for the printed quarter.
- **Mini Model**: extend/re-label year columns if a new fiscal year entered; re-seed drivers to the
  Model's updated annuals; actual-year links pick up VAActuals automatically.
- **1 Pager / NTM PE**: re-point the two Model-EPS links if the valuation years rolled; confirm the
  ticker cell; Bloomberg cells refresh on the user's desktop.
- **Guidance**: stack a new violet vintage row per restated item — on a frozen map ALWAYS via
  `scripts/insert_guidance_rows.py` (never hand-insert; it repairs every reference workbook-wide),
  then re-verify anchors.

## 6. Re-audit and report
- Run `scripts/audit_model.py`; fix FAILs. Image-verify the banner (separators at the new year
  boundary), the new Annual boxes, and the moved focal shapes.
- All check rows 0/"-"; actuals tie $0 for the printed quarter; annuals include the new quarter.
- Reply with: what printed vs what was estimated (the beat/miss on the KPI set), which inputs were
  re-seeded vs kept, new data gaps, and any cells flagged for follow-up.
