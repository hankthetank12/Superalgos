# 1. Consensus (endorsed by 3+ reviewers)

- **Delete the v1–v6.1 changelog from SKILL.md** (Me, A, B, C, D).
- **DCF is not the valuation layer; default is 1 Pager + NTM PE** (Me, A, B, C, D).
- **Mini Model actuals green-link VAActuals (or Model annuals); drop “self-contained / no green”** (Me, A, B, C, D).
- **Consensus ladder: VAActuals/workbook first → red hardcodes → BQL only as heal-on-open** (Me, A, B, C, D).
- **Kill “No green links to VAActuals, ever” as a universal hard rule** (Me, A, B, C, D).
- **New mandatory `alt-manager-engine.md` (flagship lifecycle, not “AUM × fee”)** (Me, A, B, C, D).
- **SKILL.md is a router; formatting/BQL/borders/SUMIFS/Up-C/vintage leave the main file** (Me, A, B, C, D).
- **Collapse the 19-item checklist; tab checks live in their refs** (Me, A, B, D).
- **Add update mode** (append quarter, roll focal, restack seasonals, re-snapshot Revisions) (Me, A, B, D).
- **Summary/Simple IS (~30–40 rows) at top of Model, same-tab #006600 links** (Me, A, B, D).
- **Column map is a default, not law** (Me, A, B, D).
- **On/off scenario overlays may feed P&L; drop “never as separate tabs / never feed”** (Me, A, B, D).
- **Cohort/vintage triangle is an engine grammar, not a memo** (Me, A, B, D).
- **Third banner tier for repeating child blocks (fund/product)** (Me, A, B, D).
- **Programmatic audit script over prose `getImage` theater** (Me, A, C, D).
- **Capital & returns as a default module** (Me, A, D).
- **Optional Daloopa INDEX/MATCH when a Daloopa tab exists; not the default** (Me, A, D).

# 2. Disputes — take a side

**Delete `dcf-tab.md` (B) vs keep opt-in (Me, A, D).** Keep the file. Deleting it is spite, not routing. Default build order must not load it. “Only if the user asks for DCF/intrinsic.” First-pass never spends tokens on it.

**Two Mini Model modes (A) vs one flipped default (Me).** One default. Dual modes are a classification trap; the agent will pick the stale one. Default = VA-linked actuals + in-tab blue drivers + optional VA-pinned totals with an Other/reconciling residual + Checks & Sources. No “export mode” until someone asks.

**VAActuals link color: red vs #006600.** Role, not source: **actuals** pulled from VA/Daloopa = dark green #006600; **Street/consensus** = red italic; **engine→P&L** = #008000. Model-tab reported totals stay **blue hardcodes** (HOOD/BX) unless Daloopa mode is on. Consensus is never green.

**BQL canary as optional (A) vs skip in dead env (D, B).** Skip on the Model spine. Canary + live BQL on EPS strip is the verification paradox: openpyxl cannot tie EPS to the cent. Write BQL only on 1 Pager/NTM PE (heal-on-open). Model/Drivers/Qtr seed from VA or red hardcodes.

**Attention-flag red fills (A, B) vs omit (Me).** Omit from the skill. It is a human markup habit, not a first-pass contract. Agents will paint random inputs red.

**Named alt-data tabs + ingest script (A, B) vs generic staging pattern (Me).** Pattern only in a short ref: date/value table, EOMONTH, XLOOKUP into Model, missing-month flags. Optional `ingest_staging_data.py` if a CSV is in the workspace. Do **not** name Sensor Tower/Relay/Citadel in SKILL.md.

**Sidecar TAM tabs as a default module (A) vs optional (Me, D).** Optional, after Model audit, only if Step 0 found a material non-consensus TAM/what-if. Default off. Grammar = toggle + inclusion check, not Agentic/EU contents.

**Core vs GAAP always (A) vs only when the company leads with Core (Me, B).** Applicability gate. IBKR-shaped, not HOOD/BX default.

**Seasonality color brown vs red.** One rule: **red italic** for Seasonality / Vs Normal (HOOD majority). Brown is retired. Two colors for one role is how agents coin a third.

**Fundraising research tabs inside the AM engine (A).** Reject as default. Parameterize funds from the supplement; PE/RE research dumps are analyst homework, not first-pass.

**How small is SKILL.md.** Target ~120–150 lines: trigger, STOP for source materials, sector router table, source ladder, do-not-build list, short build order with “read X before step N,” 5 gates. Not a 20-line stub — the agent still needs the contract in the always-loaded file.

# 3. Rejects

- **Encode Agentic/EU TAM/NFL/Trump/IPO Access/Rothera/BX fund names in SKILL.md** — overfitting; grammars only.
- **IBKR Arial 10 + interleaved annuals as new-build style** — read-compat only.
- **Replicate user typos** — noise.
- **Delete `dcf-tab.md`** — keep opt-in; stop loading it.
- **Mandatory Daloopa / guessed series IDs** — HOOD/BX still hand-key; IDs are not inferable.
- **Red-fill “needs update” as a format law** — workflow graffiti.
- **NTM PE 6,500 BDH values at build** — scaffold 3 spills + VLOOKUP; leave refresh to Excel.
- **Always-on Up-C, vintage roll-on, rate-path, per-unit, market-vs-organic** — sector/applicability modules, not soup.
- **Two Mini Model modes** — instruction collision.
- **Fundraising research tabs as AM deliverables** — not first-pass.
- **Calibri-9 restated 6× in SKILL.md** — once in format-spec + audit script.
- **Live-BQL EPS-strip as a gate** — unverifiable in the build env.
- **`getImage` as the format audit** — keep as optional human check; script is the gate.
- **Attention to Revisions Aptos Narrow** — force Calibri 9 on new tabs; don’t special-case.

# 4. Final ranked top 10

**1. Strip SKILL.md to router + gates; dump mechanics into refs**  
Rewrite the YAML description to current behavior (no lineage). Delete the v5/v4/v3/v6.1 preamble. Keep: Step 0 STOP, sector-router table (retail broker → `retail-broker-engine.md`; alt manager → `alt-manager-engine.md`; else transactional + applicability flags), 10-line philosophy, source ladder, **Do not build** (DCF, sidecar TAM, Daloopa, Up-C, vintage, Core P&L, 1 Pager BDH values unless conditions), build order with an explicit `read X before step N` table, 5 gates. Move number formats, banners, boxes, SUMIFS, EPS-strip formulas, Up-C, vintage math to `references/model-engine.md` (or `format-spec.md` + engine). Impact: **HIGH** — without this, items 2–10 will not be followed.

**2. Default valuation = 1 Pager + NTM PE; DCF opt-in only**  
New `references/one-pager-ntm-pe.md`: 1 Pager B1:O64 (two out-year Bear/Base/Bull EPS×multiple, Model EPS #006600, Street EPS red, R/R, BDP/BDH key stats, relative P/E vs SPX/QQQ with blue σ inputs, trailing performance, IR). NTM PE: 3 BDH spills, date-align VLOOKUP, median/±1σ — formulas only, no spilled values at build. Clone = ticker cell + 2 EPS links. SKILL.md Downstream + build order: Model → Mini → Revisions → Drivers → Qtr → **1 Pager → NTM PE**. DCF only on explicit ask; do not open `dcf-tab.md` otherwise. Impact: **HIGH**.

**3. `references/alt-manager-engine.md` + same-strength sector gate as retail broker**  
Flagship ~lifecycle: fee-rate inputs in label area; commitments / invested / dry powder / % called / realizations / NAV (red residual in actuals, blue % chg fwd) / MOIC / FPAUM; **binary step-down trigger** (1 in trigger qtr) → rate switch → fees = FPAUM × rate/4. Perpetual SUMPRODUCT. Segment AUM walk with flow/market/stepdown + red residual. FRE/PRE bridge. Fund list from 10-K/supplement — no hardcoded BCP IX. Mandatory read when sector = alt manager. Impact: **HIGH**.

**4. Flip Mini Model contract in SKILL.md + `mini-model.md`**  
Actual years: green #006600 to VAActuals if present, else blue from Model annuals. Estimate years: blue-on-yellow drivers in-tab; totals **may** pin to VA with Other/reconciling residual + “Consensus reconciliation” row. Checks & Sources. Red Street memos only for consensus. Delete every “self-contained / no Model! / no VAActuals / no green” sentence. Impact: **HIGH**.

**5. Consensus source ladder (one box) on Model + Drivers + Qtr + EPS strip**  
(1) VAActuals/consensus tab → red italic links. (2) Else red hardcodes from user paste. (3) BQL never the spine; optional on 1 Pager/NTM PE. Delete canary, derived-FPR-as-gate, checklist “live BQL.” Verify ties only against (1)/(2). Impact: **HIGH** — stops hallucinated seed-ties.

**6. Summary IS as Model rows 1–~40**  
In `model-engine.md` + build-order step 4: compact headline IS (rev, key KPI, PPNR/FRE, NI, EPS, margins, shares), #006600 same-tab links into the deep rollup, no drivers. Deep P&L starts below. Impact: **MED-HIGH**.

**7. `references/driver-grammars.md` — menu for Step 0 unique KPIs**  
Short patterns only: (a) cohort triangle + plug vs actual; (b) attach new vs backbook + residual; (c) event/deal calendar (units × take × share); (d) on/off overlay that **does** feed P&L + delta memo; (e) staging tab + XLOOKUP by month-end; (f) Vs Normal = AVERAGE prior same-months + delta under %M/M/#M/M; (g) 2Q stack for young products. Point Step 0 at this menu. No HOOD names. Impact: **MED-HIGH**.

**8. Capital & returns + estimate BS as default closing modules**  
After tax/NCI in engine ref: payout mix, BVPS/TBVPS, ROE/ROTCE, op leverage, Δ share count, share roll tied to consensus. Estimate BS: driven asset scale, liability plug, equity roll. Not sector-optional for brokers/banks/AMs. Impact: **MED**.

**9. `references/update-mode.md` + trigger fork at top of SKILL.md**  
First question after Step 0 materials: **fresh vs update**. Update: append quarter, extend banner/SUMIFS/white year rules, roll focal shape, restack seasonals, refresh Daloopa/Monthly/VA, freeze Revisions Old, stack guidance vintage via `insert_guidance_rows.py` (never hand-insert). Impact: **MED** on first-pass, **HIGH** on living books.

**10. `scripts/audit_model.py` + 5 gates; layout/banner/color lock**  
Script: font size, fill-role whitelist, yellow-on-formula, blue-on-formula, SUMIFS range identity, check rows ≈0, Mini Model ref policy, # errors incl. hidden cols. Gate for downstream. SKILL.md: default labels B–K / data L; freeze after label block; match existing books. Banners: #375623 @B, #FFF2CC @C, child #FFEA8F @D. Guidance only #7030A0. Seasonality red italic. Impact: **MED** on compliance; prevents BX/IBKR layout smash.