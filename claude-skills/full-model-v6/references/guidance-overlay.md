# Guidance overlay — detailed mechanics

Read this when build-order step 4 reaches a model whose workbook contains a **"Guidance"** tab. The overlay annotates the Model so management's stated guidance sits directly beneath what the company actually delivered (the actual columns) and what it's modeled to deliver (the estimate columns) — a fast read on said-vs-delivered, backward and forward. If there is **no** tab named "Guidance," skip the overlay entirely and build the Model normally.

## Why the timing matters (read this first)
Guidance rows are **planned into the P&L skeleton as you lay it out** (step 4), before the Model's row/column map is frozen and before any downstream tab is built. This is not optional polish — it's the only safe order. openpyxl does **not** re-point formulas when rows are inserted, so dropping guidance rows into a finished sheet would leave every engine link, annual SUMIFS, EPS-strip reference, and downstream-tab link (Mini Model / Revisions / Drivers / Qtr all reference Model cells by row number) pointing at the wrong rows — a silent, sheet-wide break. Reserve the rows up front and every formula is written against the final row numbers from the start. (Overlaying onto an already-built model instead of a fresh build is a different, sanctioned path — see § Applying to a model that already exists, which uses the bundled helper to insert and repair references safely rather than hand-re-pointing.)

## Step 1 — Read the Guidance tab adaptively (no fixed layout)
The tab has no prescribed structure, so read its full used range (values **and** any cell notes) and work out its shape before extracting. It is usually one of:
- a **flat list** — one row per guidance item, with columns for the metric/line, the period, the guidance itself, and often a source/date; or
- a **matrix** — metrics down the rows, periods across the columns.

Column names, order, and formatting vary; infer them. Whatever the shape, extract for each item a triple: **(line/metric name, the period it applies to, the guidance exactly as stated)**, plus any **source/date**.

**Preserve guidance verbatim.** The whole point is fidelity to what management said, so keep ranges, inequalities, units, and qualifiers intact ("$2.1–2.3bn", ">15%", "~flat", "mid-single-digit growth", "low-20s% margin"). Never round a range to its midpoint, never convert a qualitative guide into a number, never impose more precision than management gave.

## Step 2 — Match each item to a P&L line
Match the item's metric name to a Model P&L row by **label**, using judgment rather than exact-string equality ("Adjusted operating expenses" → the Operating Expenses line; "NII" → Net Interest Income; "EPS" → the EPS line). Attach **segment** guidance to that segment's line, not to the total.
- **Basis mismatch** (an adjusted/non-GAAP guide against a GAAP line, or vice-versa): annotate the closest line and record the basis in the displayed text (e.g. "(adj. basis)") — don't force a false match or silently treat adjusted as GAAP.
- **Ambiguous** (two plausible lines) or **unmatched** (no reasonable line, or a metric the model doesn't carry): do **not** guess destructively. Collect these into an "unmatched / ambiguous guidance" list and surface it in the final reply so the analyst can place them. (Optionally park them in a single labeled `Memo: Unmapped guidance` block at the foot of the P&L so they're visible in-sheet — but reporting them is the requirement.)

## Step 3 — Reserve the guidance row (during skeleton layout)
As you lay out each P&L line and its %-/Annual rows, if that line is in the guidance set, allocate the **next row immediately beneath the line's complete block** (after its %Y/Y, %Q/Q, #Y/Y, and Annual pair — before the next P&L line) for the annotation, and advance your row cursor so all following rows use the post-annotation numbering. Placing it below the whole block (rather than wedged between the line and its %-rows) leaves the line's own %-row references and the two-phase Annual-box draw completely undisturbed.
- **One row per line** by default, carrying that line's guidance across all the periods it was given for.
- If the Guidance tab tracks a **revision history** for a line (guidance restated on different dates), stack **one row per vintage**, each date-stamped, so the progression of what management said is visible — this is often exactly what you want to see against delivery.

## Step 4 — Place the guidance period-aligned
Put each figure in the **column of the period it pertains to**, so it lands under the model's own number for that period:
- a **fiscal-year** guide → that year's **annual** column (under the model's FY estimate, or under the FY actual once reported — so you can see whether they hit it);
- a **quarterly** guide → that **quarter's** column;
- an **exit-rate / run-rate / point-in-time** guide → the nearest applicable period column, noted.

Write the guidance as a **string** so ranges and qualifiers render faithfully (a text cell is ignored by the row's SUMIFS, so it can't corrupt any annual). A clean single figure in the line's own units may be entered as a number with the line's number format if you prefer alignment, but default to the string to avoid implying precision management didn't give. **Period-agnostic** guidance (a long-term target, an undated framework) goes as **left-aligned text in the label / first-data area** rather than a single period column. The guidance value is a display annotation only — it **never** feeds a formula.

## Step 5 — Format
- **Violet `#7030A0`, italic**, Calibri 9pt (the whole-tab base). A new, dedicated color so guidance reads instantly as "management-stated," distinct from blue actuals, green links, red plugs/consensus, and gray computed memos.
- **Row label** at the line's indent column: `Mgmt Guidance` (or `Mgmt Guidance (M/D/YY)` when you've stacked a row per revision vintage), violet italic.
- **NO embedded cell notes/comments on guidance cells.** Keep guidance cells clean. Show the **source** (which call / release / investor day and the date management said it) visibly instead — in the "Mgmt Guidance" row label (e.g. "Mgmt Guidance (4Q25 call, 1/29/26)") or a small gray italic source cell in the label area — and list all sources in the reply. If the visible cell had to abbreviate a verbatim guide, put the full verbatim text in the reply, not a note.
- **Exclude guidance rows from the border sweeps.** Add them to the same exclusion set as Annual-pair rows so the subtotal/driver rule sweep and the two-phase Annual-box draw skip them — otherwise a full-width rule or box edge would cut through the annotation. (Detect by the guidance row-label tag or by tracking the reserved rows explicitly.)

## Step 6 — Report
In the final reply, state that the overlay was applied, how many lines were annotated and which, and **list any unmatched or ambiguous guidance items** and any **basis mismatches** (adjusted-vs-GAAP) or **period-mapping caveats** (e.g. a guide for a year beyond the model's horizon — extend the model if reasonable, otherwise park the item and say so; never fabricate a period column to hold it).

## Applying to a model that already exists — the bundled helper
Steps 3–5 above assume you're building the model now and can reserve rows before the map is frozen. When the model **already exists** (or you're re-running guidance after the Model's map is frozen), you can't reserve rows — you have to insert them, and every formula reference at or below each insertion has to move with them. Do **not** do this by hand: `openpyxl.insert_rows()` shifts cells but leaves formula strings untouched, so links, SUMIFS, the EPS strip, and every downstream-tab reference silently point at the wrong rows.

Use the bundled **`scripts/insert_guidance_rows.py`**, which does it safely: it inserts the rows and then rewrites every A1 reference across the whole workbook by the correct row shift — handling bare vs sheet-qualified refs, `$` anchors, and range endpoints where the tail inherits the head's sheet (`'Model'!H6:H11` — the `H11` is on `Model` too). Steps 1–2 (adaptive read, semantic match) and the period-alignment / formatting rules are unchanged; you just hand the results to the helper instead of laying rows out by cursor.

Build a JSON spec — one entry per guided line — and run it:
```bash
python scripts/insert_guidance_rows.py MODEL.xlsx --sheet Model --spec guidance_spec.json --out MODEL.xlsx
```
```json
[{"after_row": 42, "label_col": 4,
  "rows": [{"label": "Mgmt Guidance",
            "cells": {"28": {"value": "$12.4-12.6bn"}}}]}]
```
`after_row` = the last row of the line's block; `label_col` = the line's indent column; `cells` keys are column indices; give a line several `rows` for multiple guidance vintages (inserted contiguously). The helper applies violet #7030A0 italic for you; do NOT pass `note` payloads — guidance cells carry no embedded notes (put the source in the row label).

**Then prove it.** Before inserting, capture a battery of anchor values via recalc (every subtotal, EPS, net income, each downstream-tab headline link). After running the helper, recalc again and confirm **every anchor is unchanged**. If any moved, the repair didn't cover something — almost always **INDIRECT / OFFSET / named ranges / structured references**, which the helper does not adjust — so fix those by hand (or rebuild via the fresh-build path). Never deliver a model whose anchors moved.

## Edge cases
- **No "Guidance" tab** → skip the overlay entirely; build the Model normally.
- **Empty tab / header only** → nothing to overlay; note it and move on.
- **Metric not in the P&L** → report in the reply (don't drop).
- **Guide beyond the model horizon** → extend if sensible, else park + note.
- **Adjusted vs GAAP** → annotate the closest line, note the basis.
- **Adding to a finished / already-built model** → use the bundled `scripts/insert_guidance_rows.py` (inserts + repairs references), then verify anchors via recalc — never hand-insert. See § Applying to a model that already exists.

## Worked example
Guidance tab (flat list) row: metric **"Full-year adjusted operating expenses"**, period **"FY2026"**, guidance **"$12.4–12.6bn"**, source **"4Q25 call, 1/29/26"**. The Model carries an **Operating Expenses** line at row R with FY2026 in annual column AB.
→ During skeleton layout, reserve row R+k directly beneath the Opex block and label it `Mgmt Guidance` in violet italic. In column **AB** on that row, write the string `$12.4–12.6bn` in violet italic; label the row `Mgmt Guidance (4Q25 call, 1/29/26, adj. basis)` so the source is visible — no cell note. The analyst now reads the model's FY26 Opex estimate in AB and, a few rows below in the same column, exactly what management guided — and for any already-reported year with a prior guide, the guide sits under the actual, showing at a glance whether they delivered.
