# HOOD Mini Model — build notes

Deliverable: `HOOD_with_minimodel.xlsx` — the fixture workbook plus a new **"Mini Model"**
tab, inserted directly after the Model tab (position 3 of 17). Built per
`full-model-v5` → `references/mini-model.md`. **No existing tab was modified**: the sheet
was injected at zip level, and every original worksheet/drawing/chart/comment part in the
output is byte-identical to the fixture (verified by SHA-256). Only the four workbook-level
plumbing parts that must reference a new sheet changed: `[Content_Types].xml`,
`xl/workbook.xml`, `xl/_rels/workbook.xml.rels` (sheet registration), and `xl/styles.xml`
(new style entries appended after the existing ones; all pre-existing style indices untouched).

## What was built

A self-contained ANNUAL mini-model, one column per Model annual-block year — 2022A–2025A
(actuals), 2026E–2028E (estimates), focal year **2026E** (column N, framed by a floating
rectangle shape at y=0, full sheet height, 1pt outline). Data in J:P, labels D:I, Calibri 9pt
throughout, gridlines off, no freeze panes, D:I boxed white section banners, thin top rules on
subtotals/driver-fed lines, key bottom rules under Total net revenues / Total opex / Net
income / Adj. EBITDA / Diluted EPS, medium rule under the title.

Sections (mirroring the Model's retail-broker P&L rollup):
- **User & Asset Build** — Funded customers (EOP) + %Y/Y; ARPU (derived, gray); platform
  assets walk: BOP → Net deposits (NNA-rate driven) → Market & other (return-% driven) →
  EOP platform assets.
- **Revenue Build** — per-product engines, driver rows above the line they drive:
  Options (contracts × $/contract), Equities (notional × bp take), Crypto (notional × bp
  take), Prediction markets (contracts × $/contract), Other transaction (%Y/Y) →
  **Transaction based revenues** (sum). NII stack: margin book / cash & deposits / cash
  sweep / credit card (avg $mm, %Y/Y-driven) → IEA (sum) × blended NIM (level input) →
  **Net interest revenues**. Gold subs (KPI) + Gold revenue (%Y/Y) + Other (residual) →
  **Other revenues**. → **Total net revenues**.
- **Operating Expenses** — Brokerage & transaction (driven as % of options+equities
  revenues, matching the Model's engine) + Opex ex-brokerage (%Y/Y) → Total opex.
- **Profit** — Other income/(expense) net (level input), Pretax income, tax-rate input →
  Taxes, NCI (level input), Net income, margins.
- **Adj. EBITDA Bridge** — NI + credit-facility interest + taxes + D&A + NCI = EBITDA;
  + SBC (%Y/Y) + unrealized gains = Adj. EBITDA + margin (exactly the Model's r116–r129
  bridge).
- **Per Share** — Diluted shares (avg, %Y/Y-driven), **Diluted EPS (GAAP)** = NI/shares;
  red-italic **Consensus EPS – diluted** from `VAActuals` (row 165, FY columns AU:BA) and a
  single Model-vs-Consensus (%) delta row (the Model is GAAP-basis — its own consensus pull
  is VA "EPS - Diluted" — so the single-EPS variant of the reference's EPS block applies).

Color convention as specified: blue #0000FF no-fill hardcoded actuals; blue on #FFFFCC
driver inputs (estimate columns only, never on formulas); black in-tab calcs; gray #7F7F7F
italic computed %Y/Y/margins/derived KPIs; red #FF0000 italic consensus rows (the only
cross-tab references); **zero green cells**; **zero Model! references**.

## Where the numbers came from (nothing fabricated)

- **Actual years (2022–2025 + 1H26 inside FY26)**: recomputed to the dollar from the Model's
  quarterly cells (press-release hardcodes plus small in-sheet sums), using the Model's own
  annual conventions — SUMIFS-equivalent sums for flows, 4Q value for EOP stocks, average of
  quarterly averages for balances, sum of quarterly EPS for annual EPS. Identity checks all
  pass (PT = Rev − Opex + Other; NI = PT − Taxes − NCI; EBITDA bridge check = 0 every year).
- **Estimate seeds (2026E–2028E)**: the workbook's own frozen record of the Model's
  estimates — the **Revisions tab "Old" snapshot** (G/K/O/S/W columns). This was necessary,
  not merely convenient: the Model's estimate quarters chain off live Bloomberg pulls
  (`_xll.BDP` fed-funds forwards for the NII yield stack, `_xll.BQL` QQQ for the AUM market
  bridge and equity-volume path), so the file's estimate cells are literally indeterminate
  offline (no cached values exist — the fixture was last saved without Excel). The snapshot
  is internally consistent with the 1H26 actual hardcodes to 3 decimals (e.g. FY26 txn-rev
  snapshot 4,005.663 − 3Q26E 968.150 − 4Q26E 1,638.512 = 1,399.000 = 1Q26A 623 + 2Q26A 776),
  proving it was frozen from the current post-2Q26 model state.
- **Lines not carried in the snapshot** (SBC, D&A, credit-facility interest, NCI, gold,
  IEA components): reconstructed from the Model's estimate columns, which for these lines are
  pure literal input chains (e.g. SBC = prior + 2/qtr, D&A 23/qtr, NCI 12/qtr, margin book =
  %-of-platform-assets inputs, cash/sweep = +4%/qtr chains, credit card +20%/+10%/qtr, gold
  penetration +100bps/qtr on the funded roll). The AUM path was pinned to the snapshot's
  3Q26/4Q26 EOPs and then rolls on the literal NNA-rate/market inputs; the reconstruction
  reproduces the snapshot's 4Q27 (468.154) and 4Q28 (602.265) EOPs exactly, and the funded-
  customer roll reproduces 29.216 / 30.024 / 33.175 / 36.202 exactly once the snapshot-era
  +0.3mm 3Q26 "Acquired customers" input (cleared in the live file after the snapshot) is
  restored.
- Every driver input is seeded so the estimate column ties its target: %Y/Y seeds are exact
  year-over-year ratios of seed values; rates are blended (rev ÷ volume; NII ÷ avg IEA;
  taxes ÷ PT), so products, NII, taxes, NI and EPS reproduce the targets by construction.

## Judgment calls (what I would have asked the user, and what I did)

1. **Seed vintage.** Live Bloomberg state is unreachable offline; I seeded to the Revisions
   "Old" snapshot — the only determinate in-workbook record of the Model's estimates, and
   consistent with 1H26 actuals. Would have confirmed this with the user (vs. waiting for a
   Bloomberg-connected session to re-seed).
2. **Snapshot vintage skew.** The snapshot's P&L rows are one consistent vintage, but its
   product-detail rows don't sum to its transaction-revenue total (products + other + agentic
   ≠ txn total by ~$69mm in FY26). The P&L rows are king: product lines are seeded to the
   product vintage and **"Other transaction (incl. agentic, rebates)" is the residual** so
   the transaction subtotal ties the P&L vintage exactly (same construction in actual years,
   where the residual = the Model's own r908 plug + agentic).
3. **FY26 EBITDA snapshot is stale** (3,328.6 vs the identity PT + credit-facility interest
   + D&A = 3,408.6; FY27/FY28 snapshot values match the identity exactly). The mini's bridge
   computes in-tab, so it shows the internally consistent 3,408.6; noted here rather than
   forcing a tie to a stale row.
4. **Diluted shares** are the Model-implied count (annual NI ÷ annual EPS, the consensus-
   seeding construction), so EPS ties the Model's annual EPS to the cent; labeled "avg".
5. **ARPU and Gold rev/sub are EOP-based** (total revenue ÷ EOP funded), keeping every ratio
   computable from Mini Model cells only (an average-based ARPU would need FY21 counts on
   the tab). Derived gray KPIs only — they drive nothing.
6. **NIM is the blended yield on avg IEA** (includes sec lending net, other interest, and the
   credit-facility expense inside NII), matching NII ÷ IEA identically in every year.
7. **Opex is two lines** (brokerage %-of-revenue engine + ex-brokerage %Y/Y), mirroring how
   the Model itself forecasts opex (its estimate columns don't populate the six-line detail;
   Trump-accounts and RIF items are folded into ex-brokerage, as the Model's total does).
8. **The snapshot embeds a −12% 3Q26 market return** on platform assets (back-solved; the
   QQQ %M/M chain at freeze time), producing FY26 "Market & other" of −$30.3bn. Faithful to
   the Model's frozen state — flagged for the user to review on a live re-seed.
9. **Prediction-markets 2024**: the Model's engine tracks event contracts only from 2025
   (4Q24 launch revenue sits in its Other-transaction plug), so the mini shows 0 volume in
   2022–24 with dash-guarded ratios.
10. **Step 0 of the skill** (ask for the latest release/deck) is a Model-tab gate; this task
    only adds the downstream Mini Model to an already-audited frozen Model, so the research
    step reduces to mirroring the Model's own management-aligned rollup, which the tab does.

## Verification (per references/mini-model.md "Verify before done")

1. **Rebuild / error scan** — every formula on the tab was evaluated offline with a formula
   evaluator; **592 data cells all match their expected values (0 mismatches)**; no
   #REF!/#VALUE! anywhere; div-by-zero cells are IFERROR/IF-guarded to "-".
2. **No external links except red consensus rows** — formula scan of the final file: zero
   `Model!` references; `VAActuals!` appears only in the seven J126:P126 consensus cells.
3. **Spot-check ties** — actual years equal the Model's audited annuals to the dollar
   (Total net revenues 1,358 / 1,865 / 2,951 / 4,473; Net income −996 / −547 / 1,391 /
   1,883; EPS −1.138 / −0.610 / 1.536 / 2.059). Focal-year driver-built estimates tie the
   Model's estimate seeds at seed: 2026E Total net revenues 6,111.964; PT 3,282.649; NI
   2,591.058; **EPS $2.8438 — to the cent** (likewise 2027E $3.8822, 2028E $4.9001).
4. **Wiggle test** — +5pts on the 2026E options-contracts %Y/Y input (N26): contracts
   3,187→3,302, options revenue +50.5, transaction subtotal +50.5, total revenue +50.5,
   PT +43.4, NI +34.6, EPS $2.8438→$2.8818 (and 2027/28 chain through); +20bps on NIM (N64):
   NII +134.2, EPS +$0.118; +20bps on tax rate (N96): EPS −$0.007. All inputs restored to
   seed after testing (verified equal to baseline).
5. **%Y/Y and ratios in-tab** — every %/margin/ratio row computes off Mini Model cells; no
   VA-scaled whole-percent ratios are displayed (take rates are bp/$-per-unit model-native
   scales), so the `0.000` VA format case does not arise.
6. **Formatting read-back** — whole tab Calibri 9pt (only font present); blue hardcodes,
   blue-on-#FFFFCC inputs confirmed on no-formula cells only; gray computed rows; red
   consensus rows; D:I banner boxes 4-edged; subtotal/key rules present; focal-year SHAPE
   over column N anchored at y=0, full height, 1pt black outline, no fill; gridlines off;
   no freeze panes; **no green cells; no yellow on formulas**.
7. **Consensus source** — VAActuals (Visible Alpha) "EPS - Diluted" (tab row 165, FY-2022…
   FY-2028 columns AU:BA), the same basis as the Model's own EPS-strip consensus pull. The
   cells display once the VA add-in refreshes (the fixture carries no cached VA values, so
   they render blank/0 offline; the delta row is guarded to "-"). The Mini Model is
   **self-contained**: flexing the Model does not move this tab; re-transcribe/re-seed to
   re-sync if the Model changes materially.

Workbook integrity: all 61 original zip parts except the four plumbing files are
byte-identical to the fixture; merged styles validated (counts, xf/font/fill/border/numFmt
index bounds); workbook opens with `fullCalcOnLoad` already set, so Excel computes the new
tab on first open.
