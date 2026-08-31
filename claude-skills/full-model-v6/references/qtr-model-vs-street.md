# Qtr tab — Model vs Street vs Actual (last of the Model-linked tabs, before the valuation pair)

**Spec source: `qtr-model-vs-street-v2`.** This is the v2 build — the v1 spec corrected against a
live audited build. Every v2 correction is marked **[v2]** below. If you have seen the v1 layout
(title/banners in column C, no-fill derived actuals, SUM bases everywhere in the FY block), those
are the exact things v2 fixes; follow this file, not memory.

Read this when you reach the **Qtr build-order step**, after the Model, Mini Model, Revisions, and
Drivers tabs are done. Prerequisite: the Model tab has passed its audit and its row/column map is
frozen. You built that map — do **not** re-discover it.

## What it is
A one-page quarterly analysis: ~9 historical quarters of model-linked KPIs, then for the **focal**
(upcoming/just-reported) quarter three columns — the model estimate, **Street** consensus, and
**Actual** — plus variance columns (Model vs Street; Actual vs Model; Actual vs Street) and a hidden
FY comparison block. GS "Qtr" format (colors, borders, bps rows). One Qtr tab per workbook. KPIs must
mirror the company's own P&L structure on the Model tab — do NOT force GS line items onto another company.

## How the chained flow changes the standalone steps
- **No recon pass.** The standalone skill opens by reading the Model tab to find P&L rows and the
  quarterly column letters (skipping interleaved annual/FY columns). You already have that map from
  building the Model — reuse it. You also already know the focal quarter (the Model's first estimate
  quarter / just-reported quarter) and whether it has reported.
- **Consensus source = whatever the Model used** (same ladder as the Drivers tab): a **VAActuals /
  consensus tab** if the workbook has one (Street links are `=VAActuals!$<focalCol>$<row>`), else the
  **red hardcoded consensus snapshot / staging block** the Model seeded from — substitute
  `{consensusRef}` for `VAActuals` in the formulas below.
- **Actual column comes from the Model.** If the focal quarter has already reported, its actuals are
  already hardcoded (blue) on the Model tab — link column X to that Model quarter column (or copy the
  values, keeping the blue/#FFFFCC actual treatment). If it has not reported, leave X blank.
- **Model-estimate column label.** Use your model/PM label convention; keep it consistent with the
  other tabs.
- **KPI banner content is already decided.** The 5–10 KPIs identified in the model's research step
  are the KPI block — do not re-derive them here.
- **Font is already Calibri 9pt** — consistent with the harmonized workbook.
- **Order.** Model (audited) → Mini Model → Revisions → Drivers → **Qtr** → 1 Pager + NTM PE (the valuation pair follows this tab).

## Step A — KPI selection **[v2 — explicit rule, was analyst judgment]**
From the frozen Model map, expose a line ONLY if it satisfies at least one of:
- **(a) Headline** — the line the print will be judged on (total revenues, total expenses, PT income,
  net income, EPS, shares out).
- **(b) Street-comparable** — consensus publishes it, so a genuine Street tie is possible.
- **(c) Reconciling** — required to make a subtotal foot (the red plug line).

Additional rules:
- **Pick detail at the granularity consensus publishes.** Where the Model is finer than consensus,
  roll up before exposing the line. Where consensus lacks an aggregate the Model has, compute Street
  in-tab from its components (bold black — see Formulas).
- **Exclude** Model detail with neither a consensus figure nor press-release disclosure — it can never
  be validated and adds noise.
- **The KPI banner carries the company's real 5–10 KPI set** (net new assets, client assets, DARTs,
  cash-sweep balances, AUM/FPAUM, RWAs, CET1/Tier 1 — whatever the research step established). A KPI
  section holding a single ratio is an incomplete build.

Record the QUARTERLY column letters for the last ~9 quarters + the focal quarter (skip annual/FY
columns interleaved between quarters), the focal-quarter consensus column (single absolute column),
and the consensus row for each KPI; note which KPIs consensus does NOT publish (those Street cells are
computed or left blank — see Formulas and the blank-cell guard).
Done when: every line on the tab maps to (a), (b) or (c), and the KPI banner is populated.

## Sheet setup
- Sheet name "Qtr". Gridlines OFF. Freeze panes at **A1:L6** (6 rows, 12 cols). Row height 12. Entire
  tab **Calibri 9pt**.
- Column widths (pts): A:E = 14.3; F:G = 18.8; H = 24; I:L = 48; M:V = 55.5; W = 60.8; X = 50.3;
  Y = 14.3 (spacer); Z = 80.3; AA = 14.3 (spacer); AB:AC = 50.3; AD = 14.3 (spacer); AE:AG = 0
  (**hidden FY block**).
- **[v2] No focal-column shape on this tab** — the V:X header box already frames the focal quarter.
  Shapes belong to the Mini Model and Drivers tabs.

## Frame, title band, banners **[v2 — column B, not C]**
- Frame: thin bottom border across B1:AG1; thin top across C2:AG2; thin right down A2:A(last); thin
  left down B2:B(last).
- **Title in B3**: "<TICKER> EPS", bold. Medium bottom border B3:AG3 AND medium top border B4:AG4
  (double medium rule under the title band).
- **Section banners sit in column B**: "PnL" in **B7**, boxed (thin left + right edges on the banner,
  thin top+bottom across the label span). Second banner is **"KPIs"** — or "Balance Sheet" for a bank
  presenting RWAs/capital — same treatment, placed above its block.

## Header rows (5–6), all bold Calibri 9
- M6:U6: historical quarter labels as text ("1Q24" … "1Q26"), right-aligned.
- V5: focal quarter label, right-aligned, thin bottom border V5:X5; V6 = model name, W6 = "Street",
  X6 = "Actual" — thin top+bottom border V6:X6.
- Z5 thin bottom; Z6 = "<Model> vs Street" (top+bottom).
- AB5 = "Actual vs…." (bottom AB5:AC5); AB6 = "<Model>", AC6 = "Street" (top+bottom), right-aligned.
- AE5 = "FY 20XX"; AE6 = "<Model>", AF6 = "Street", AG6 = "<Model> vs Street" (AE5:AG5 bottom;
  AE6:AG6 top+bottom).
- Row 7: thin top border across M7:X7, Z7, AB7:AC7, AE7:AG7 (closes the header box).

## KPI block pattern (repeat per KPI): value, % Y/Y, % Q/Q, then one blank row
- Label indent hierarchy: major totals (Total Revenues, Total Expenses, PT Income, Net Income, EPS,
  and top-level KPIs) in **D**; mid-level (segment subtotals, NII, Fee income, Comp, Taxes, Tax Rate,
  Pref dividends, Other plug, Shares Out, PT Margin, NIM) in **F**; detail sub-lines in **H**. All KPI
  labels bold.
- % row labels sit ONE column right of the KPI label (E for D-level, G for F-level, I for H-level),
  regular weight: "% Y/Y" then "% Q/Q".
- Detail sub-lines come FIRST, the subtotal after them.
- A rate/margin line (NIM, PT margin, efficiency, tax rate) sits directly BELOW the line it measures.
- Borders: thin top border on each value row spanning label column → X, and on AE:AF of that row
  (i.e. one rule between blocks).

### **[v2]** Exceptions to the 3-row block
The value+Y/Y+Q/Q block applies to every line EXCEPT the following, which carry a **bare value row**:
preferred dividends, share counts, and any memo ratio sitting under its driver line where a Y/Y delta
is not the analytical point (e.g. tax rate presented under Taxes). Decide the exception list up front
and apply it consistently — a tab where some ratios have bps rows and others don't is a build error,
not a judgment call.

## Columns & formulas per block (value row)
`{consensusRef}` = VAActuals tab or BQL/BDP consensus staging (see sourcing above).
- **M:U (history)** & **V (focal, model)**: `=Model!<qtrCol><row>`. Bold **green #008000**.
- **W (Street)**: `={consensusRef}!$<focalCol>$<row>` (absolute). Bold **red #FF0000**. Where consensus
  doesn't publish a line but publishes its components, COMPUTE W from other W cells (Fee income W =
  sum of the fee component W cells; Non-comp W = TotalCosts−Comp; PT W = PPNR−Provisions) — computed
  W cells bold **black**.
- **X (Actual)**: link to the Model's reported-actual quarter column (or hardcode consistent with it),
  bold **blue #0000FF** on **#FFFFCC**. Leave X blank pre-print.
- In-tab derived lines are computed in ALL columns (not linked): plugs (residual segment = TotalRev −
  other segments; Other = TotalExp − Comp), ratios (Efficiency = Costs/Rev; Tax Rate = Taxes/PT;
  PT Margin = PT/Rev), and PPNR = Rev − Costs.

### **[v2]** Actual-column colour convention (corrects v1's "no fill on derived actuals")
The `#FFFFCC` band runs across the **WHOLE Actual column on value rows**, so the column reads as one
continuous "Actual" block. FONT carries the meaning:
- **Blue #0000FF bold on #FFFFCC** — hardcoded from the press release / linked to the Model's actuals.
- **Black bold on #FFFFCC** — derived in-tab from other X cells (e.g. `X_PT = X_Rev − X_Exp`).
- **Red bold, NO fill** — the reconciling plug.
- **No fill at all on the X %/bps rows** — the band is only on value cells.

### **[v2]** Assumed actuals must be inputs, not calcs
If a reported line isn't in the press release at print time and you derive it from an assumption
(e.g. taxes = assumed ETR × pretax), the ASSUMPTION cell is a **blue-on-#FFFFCC input**, never black.
A black hardcoded rate is indistinguishable from a calculation and will be trusted as reported.

## % rows — the Actual column (X) always carries populated, guarded % rows
- **% Y/Y** (first % row): `=<cell>/<cell 4 cols left>-1`; populate from the 5th history column onward
  (needs a year-ago quarter on the page). For W and X the Y/Y base is the year-ago MODEL column.
  **X %Y/Y** = `=IF(X<r>="","",IFERROR(X<r>/<yearAgoModelCol><r>-1,""))`.
- **% Q/Q** (second % row): `=<cell>/<prior col>-1` from the 2nd column on — a TRUE sequential % Q/Q in
  every column (incl. the focal model V). **X %Q/Q = Actual vs the prior quarter column (the last
  history quarter on the page), NOT Actual vs Street**:
  `=IF(X<r>="","",IFERROR(X<r>/<priorQtrCol><r>-1,""))`.
- **Always write both X % formulas at build time**, guarded so they render blank until the Actual
  value cell is filled — never leave X % cells empty.
- **Ratio lines** use "# Y/Y" / "# Q/Q" bps point-deltas `=(curr-prior)*10000`; for X, same guards with
  the same bases: `=IF(X<r>="","",(X<r>-<base><r>)*10000)`. Variance columns are bps too.
- **Format**: black regular; % rows `0.0%;(0.0%);-`, bps rows `#,##0;(#,##0);-`.

### **[v2]** Whole-percent conversion on consensus ratio rows
VA/Daloopa publish ratios as whole percents (1.425 means 1.425%). Every Street ratio cell divides by
100 so both sides are fractions: `={consensusRef}!$<col>$<row>/100`. Never display a bare `0.000`
where a percent belongs. This applies to the FY Street column (**AF**) as well as W.

### **[v2]** Guard every variance against a blank Street or Actual cell
Where consensus doesn't publish a period (common: a capital ratio published FY-only, not quarterly),
leave the Street cell **BLANK — never 0** — and guard every dependent cell:
- `Z<r>` = `=IF($W<r>="","",V<r>/W<r>-1)` — or for ratio lines `=IF($W<r>="","",(V<r>-W<r>)*10000)`
- `AC<r>` = `=IF(OR($W<r>="",$X<r>=""),"",X<r>/W<r>-1)`
- Street %/bps rows: same `IF($W<r>="","",…)` wrapper.

Without the guard, `=(V-W)*10000` against an empty W returns V×10000 and renders as a large, entirely
fictitious bps miss that looks like a real result.

## Variance columns (value rows only; % rows stay empty)
- **Z** = Model vs Street: `=V/W-1` (bps for ratio lines), guarded per above. **AB** = Actual vs Model:
  `=X/V-1`; **AC** = Actual vs Street: `=X/W-1`, guarded. Format `0.0%`. Y, AA, AD are blank spacers.

## FY block (AE:AG — build it, keep columns hidden at width 0)
- **AE** = model FY value: link to THIS workbook's Model FY column for the focal fiscal year — link
  internally, never an external workbook. Bold green. **AF** = Street FY from the consensus FY column
  (with `/100` on ratios). Bold red. **AG** = `=AE/AF-1` (bps for ratios), black `0.0%`.

### **[v2]** Derived and plug rows in the FY block
v1 only covered *linked* FY cells, which is how live builds end up with `=#REF!-AE43-#REF!` on the plug
row. Rule: **plug and ratio rows in AE:AG are computed from AE:AG cells on this tab, using the
identical formula as column X** — e.g. `AE46 = AE49-AE43`, `AE_TaxRate = AE_Taxes/AE_PT`. Never a chain
of subtractions against another workbook or a deleted range.

### **[v2]** FY comparison base depends on line type
v1 gave one formula for all lines. Correct bases for the FY % row:
- **Flows** (revenues, expenses, income): `=AE<r>/SUM($Q<r>:$T<r>)-1` — sum of the prior fiscal year's
  four quarters, `$`-fixed.
- **Rates / margins / ratios**: `=(AE<r>-AVERAGE($Q<r>:$T<r>))*10000` — AVERAGE, not SUM, in bps.
- **EOP stocks** (balances, share counts, client assets): compare to the prior year's **4Q cell**, not
  a sum or an average.

## Number formats
- Values `_(* #,##0_);_(* (#,##0);_(* "-"_);_(@_)`; EPS `_($* #,##0.00_);_($* (#,##0.00);_($* "-"??_);_(@_)`.
- **[v2]** Ratio value rows split by precision: **`0.00%`** where bps precision is the point (NIM,
  capital ratios, spreads); **`0.0%`** for tax rate, margins, efficiency. v1's blanket `0.0%` hides
  basis-point movement on rate lines.
- % rows and Z/AB/AC/AG: `0.0%`; bps rows: `#,##0;(#,##0);-`.

## Block order (adapt line items to the company's P&L)
PnL banner → interest income / interest expense → NII → NIM (ratio, bps rows) → fee detail lines →
Fee income → other revenue → **Total Revenues** → Comp, other expense lines, Other (plug) →
**Total Expenses** → PT Income → PT Margin (bps) → Taxes, Tax Rate → Pref dividends → **Net Income to
common** → **EPS** ($ format) → Shares Out → **KPIs banner** → the company's KPI set (capital ratios,
balances, volumes) with bps rows on the ratios. For non-bank sectors, use the company's own segment
cut from the Model rather than the GS bank lines.

## Verify before done
1. **Read back the FULL tab including AE:AG.** Those columns are hidden at width 0, so `#REF!`/`#VALUE!`
   there survives every visual check. Zero error cells anywhere.
2. Spot-check: focal-quarter W cells tie to the consensus source; M:V tie to Model QUARTERLY columns
   (not FY columns); plugs and ratios recompute; Z/AB/AC signs sensible; if the quarter printed, X ties
   to the Model's actual column.
3. **[v2] Blank-cell sweep**: for every row where W or X is empty, confirm the Z/AC/AF-dependent cells
   render blank — not a number. A populated variance against a blank Street cell is a failed build.
4. **[v2]** Confirm no ratio row displays as a bare decimal (missing `/100`), and that rate lines use
   `0.00%` while margins/tax/efficiency use `0.0%`.
5. **[v2]** Confirm the FY % bases match line type (flows SUM, rates AVERAGE in bps, EOP stocks vs the
   prior 4Q cell) and that FY plug/ratio rows are computed from AE:AG cells on this tab.
6. Formatting read-back: green/red/blue-on-#FFFFCC convention **with the v2 font rules** (continuous
   #FFFFCC band on X value rows; black derived, red plug no-fill; no fill on X % rows), block top-rules,
   **banner boxes in column B**, hidden AE:AG, freeze at A1:L6, gridlines off, whole tab Calibri 9pt.
7. Actual column (X): every block has guarded % formulas (populated, blank pre-print) — no empty X %
   cells; X %Q/Q references the prior quarter column, not Street.
8. State in the reply: the consensus source used (VAActuals vs Bloomberg staging), whether the focal
   quarter has printed, any KPI where consensus publishes no quarterly figure (blank by design), and
   any assumed-actual input cells.

Done when: read-back matches this spec, all v2 checks pass, and the KPI set matches the company's own
P&L and driver disclosure.
