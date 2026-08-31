# HOOD valuation layer — build notes

## What was built

Per `full-model-v5` build step 14, the **default valuation pair** from
`references/one-pager-ntm-pe.md`: two new tabs, **"1 Pager"** and **"NTM PE"**, inserted
after `HOOD Mini Model v2` (scratch tabs stay behind them). **No DCF** — it is opt-in
only and was not requested. No existing tab was modified: the sheets were spliced into
the xlsx package surgically, so every pre-existing part (all 14 worksheets, 20 charts,
3 drawings, comments, external links) is **byte-identical** to the input file; only
`workbook.xml`, its rels, `[Content_Types].xml`, and `styles.xml` (append-only) changed.

### 1 Pager (B1:O58, Calibri 9, gridlines off)
- **B1** `HOOD US Equity` master ticker (blue on #FFFFCC); **H1** `=TODAY()` (blue-on-yellow
  per the tab spec — see waivers).
- **Valuation scenarios**, two blocks, Bear/Base/Bull/Street* across C:F:
  - Rows 7–14 **FY2028** (out-year): EPS row — Bear 3.40 / **Base `=Model!BH98`** (dark
    green) / Bull 6.00 / Street `=VAActuals!BA165` (red); % Y/Y vs the FY27 row below;
    Multiple 18x/30x/38x (blue); PEG; Share Price = EPS x multiple, Street
    `=BDP($B$1,"PX_LAST")`; Upside/Downside vs $F$19; R/R (for LONG) Base and Upside.
  - Rows 15–22 **FY2027** (near year): Bear 2.90 / **Base `=Model!BG98`** / Bull 4.60 /
    Street `=VAActuals!AZ165`; % Y/Y vs FY26 (`Model!$BF$98`; Street column vs
    `VAActuals!$AY$165`); Multiple 20x/32x/40x; same math stack. **F19 is the canonical
    live price cell** both blocks' upside rows divide by.
- **Key Stats** (H4:I11): price `=F19`, BDH CUR_MKT_CAP / CURR_ENTP_VAL, ADTV
  (VOLUME_AVG_90D x price / 1e6), BDH VOLATILITY_90D/100, implied 1-day move
  `=vol/SQRT(252)`, SI % of float.
- **90D Correlation** stack (K4:L10), IFERROR-wrapped BDP "CORR COEF" with
  BETA_OVERRIDE_START/END_DT keyed off H1 and `BETA_OVERRIDE_REL_INDEX="&K<r>`.
- **Two relative-multiple grids**: vs SPX (rows 13–30) and vs CCMP (rows 31–48). Current
  multiples `='NTM PE'!H7` / `'NTM PE'!C7` (green) with concatenated ratio label; index
  ladder across the top (blue anchor, +2 steps), subject P/E ladder down the left (blue
  anchor 20x, +5 steps), body `=$H../I$..` relative-multiple surface; beneath each:
  `1 St. Cheap:` / `Average:` / `1 St. Expensive:` **linked** to the NTM PE stat cells
  (L7/J7/K7 and R7/P7/Q7).
- **Stock Performance** (H52+): YTD / week / month / 3M / 2Y via
  `=$I$5/BDH(...,"PX_LAST",<TEXT date math on H1>)-1`.
- **IR Contacts** (B52+) + footnotes on Street sourcing and Bloomberg healing.

### NTM PE
- **D1** `='1 Pager'!B1` (green, auto-follows); **V1/Y1** index tickers `SPX Index` /
  `CCMP Index` (blue inputs).
- Three **BDH BEST_PE_RATIO** spill anchors (B7 subject, U7 index-1, X7 index-2): 10Y
  weekly, `BEST_FPERIOD_OVERRIDE=1BF`, `Per=W`,`Days=T`,`Fill=P`,`Sort=D` (newest first,
  so row 7 = current). Left dead with an on-sheet note — no values fabricated.
- **Date alignment** H7:H550 / N7:N550 `=IFERROR(VLOOKUP($B7,$U:$V,2,0),"")`; relative
  multiples I / O = subject / index; **stat bands** D7/E7/F7, J7/K7/L7, P7/Q7/R7 =
  MEDIAN / MEDIAN+STDEV.P / MEDIAN−STDEV.P over the aligned history, IFERROR-wrapped so
  the tab reads clean before Bloomberg populates. Spill landing zones pre-formatted to
  row 550 (522 weekly points + margin).

## Replication contract (re-point these in update mode)
- `'1 Pager'!B1` — ticker driving every pull on both tabs.
- `'1 Pager'!D7` = **Model!BH98** (FY2028 annual EPS) and `'1 Pager'!D15` = **Model!BG98**
  (FY2027 annual EPS) — the two Model-EPS links.
- Disclosed additional wiring beyond the three touch-points: Street EPS red links
  `VAActuals!BA165` / `AZ165` (F7/F15), and the % Y/Y denominators `Model!$BF$98`
  (C16:E16) and `VAActuals!$AY$165` (F16). When the Model's annual columns move, re-point
  D7/D15 and the C16:E16/F16 denominators.

## Consensus source
Ladder rung 1: the workbook's **VAActuals tab**, red links. EPS row 165 ("EPS - Diluted"),
the same row every existing tab (Qtr, Drivers, Mini Model) uses — consistent everywhere.
VAActuals cells are live `_xll.VAData` pulls, dead in this environment, so Street cells
display after the VA add-in refreshes (same status as all consensus cells in the book).

## Judgment calls (and the questions I would have asked)
1. **Bear/Bull EPS and all multiples are placeholder analyst inputs**, seeded off the
   model's own path (Revisions snapshot: FY26 2.84 / FY27 3.88 / FY28 4.90; last actual
   buyback price ~$94, forward assumption $90): FY28 3.40/6.00 EPS, 18/30/38x; FY27
   2.90/4.60 EPS, 20/32/40x. *Would have asked: your bear/bull cases and target
   multiples.*
2. **Correlation basket list**: the reference says keep the reference build's baskets;
   that build isn't in this workspace and the workbook holds no basket list, so I used a
   standard placeholder set — SPX, CCMP, GSTHHVIP (HF VIP longs), GSCBMSAL (most-short),
   GSMEFMOM (momentum), GSMEFQUA (quality). *Would have asked: your house factor/crowding
   baskets — swap the K5:K10 labels and the formulas follow.*
3. **Grid anchors**: SPX ladder 18x+2, CCMP ladder 24x+2, subject ladder 20x+5 — centered
   on plausible Aug-2026 levels; blue inputs, analyst-adjustable.
4. **Threshold cells linked, colored green**: the tab spec calls them "blue-on-yellow
   thresholds, ideally LINKED"; format-spec (canonical on conflicts) bans yellow fill on
   formulas, and the verify list accepts linked or static. I linked them (self-updating)
   with green link font.
5. **H1 `=TODAY()` kept blue-on-yellow** exactly as the tab spec demands (it is the date
   driver analysts overwrite with a static date). `audit_model.py` flags it as
   yellow-on-formula — **intentional, waived**.
6. **Valuation date**: label at B5 per spec; the blue date (8/31/2026) sits at B6 because
   C5 holds the Bear header. *Would have asked: preferred placement.*
7. **IR contacts**: Step 0 source materials are not in this workspace, so the block
   carries Robinhood's public IR channels (ir@robinhood.com, press@robinhood.com,
   investors.robinhood.com) with an on-sheet reminder to add named contacts from the
   latest release. *Would have asked: the release/deck for named IR contacts.*
8. **Tab position**: inserted after `HOOD Mini Model v2` (end of the built-tab chain);
   the previously active tab stays active.

## Bloomberg reality (flag for the user)
All BDP/BDH cells on both tabs are dead formula strings that self-heal on a desktop with
the Bloomberg add-in (`fullCalcOnLoad` is already set). Note: the **Model tab's own
estimate spine also rides on live Bloomberg cells** (rate stack rows 996–1015 `.NP*`
UD_RATE pulls and QQQ BQL market rows 461–464 / 1501–1505 — pre-existing fixture
property), so `'1 Pager'!D7/D15` display numbers when the file is opened **with**
Bloomberg; without the add-in they inherit the Model's #NAME? from those rate rows.

## Verification (one-pager-ntm-pe.md verify list)
Environment note: LibreOffice's xlsx import is broken in this sandbox and the `formulas`
package OOM-kills on this workbook, so I verified with the skill's audit script plus a
purpose-built formula evaluator (parses/evaluates the actual cell formulas; live
Bloomberg functions stubbed only inside the evaluator — flat 4.00% rate path, QQQ $600 —
**nothing written to the file**).

1. **Links resolve, Model links show live values — PASS.** Under evaluation
   `'1 Pager'!D7 == Model!BH98` and `D15 == Model!BG98` to 1e-12 (5.0003 / 4.0159 with
   the stub rate path). Quarterly EPS sums tie the SUMIFS annuals exactly for both years;
   zero residual error cells and zero circular refs in the closure. Cross-check vs the
   Revisions snapshot: transaction revenue FY27/FY28 within 0.1%; EPS within 2.0–3.4%,
   fully attributable to the stubbed rate/market path (NII deltas +5.1%/+2.3%). Street
   links point at VAActuals row 165 (AZ/BA), the workbook's standard consensus row.
2. **Scenario math chains compute off linked Base EPS — PASS.** %Y/Y (Base FY28 +24.5%
   vs FY27; Base FY27 +33.9% vs FY26), PEG, Share Price (Base28 $150.01 = 5.0003 x 30x;
   Base27 $128.51), bear/bull prices. Upside/Downside and R/R correctly wait only on the
   live `BDP PX_LAST` price cell.
3. **Grid ladders/bodies compute; thresholds linked — PASS.** Ladders step +2/+5
   (I19→O19 = 18→30; H20→H27 = 20→55); body cells evaluate ($H/I$: 1.111 top-left, 1.833
   bottom-right vs SPX; 1.528 vs CCMP); band cells link 'NTM PE'!L7/J7/K7 and R7/P7/Q7.
4. **Bloomberg formulas string-correct, no fabricated values — PASS.** All 2,403
   formulas on the two tabs tokenize/parse clean (balanced, valid argument order,
   TEXT(...,"YYYYMMDD") date math); BDH spills left dead with the on-sheet note; newer
   functions stored with the `_xlfn.` prefix (STDEV.P) so Excel resolves them.
5. **Calibri 9, gridlines off, one screen — PASS.** `audit_model.py`: single-font PASS
   for both new tabs; gridlines off in both sheetViews; 1 Pager spans B1:O58 (< O64).
   The only audit flag on the new tabs is the intentional H1 waiver (item 5 above). All
   other audit FAILs sit on pre-existing tabs that are byte-identical to the input
   fixture (Model yellow-on-formula guide cells, Revisions Aptos font, scratch tabs) —
   out of scope for this pass. Borders/shapes image-verification was not applicable (the
   pair specifies no boxes, banners, or focal shapes); fills/fonts/gridlines were
   verified from the file directly.

## Files
- `HOOD_with_valuation.xlsx` — the input workbook plus the two new tabs.
- Build/verify scripts live in the session scratchpad (`build_valuation_pair.py`,
  `eval_model.py`); they are not needed to use the workbook.
