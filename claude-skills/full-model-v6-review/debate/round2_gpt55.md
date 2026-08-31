# 1. Consensus (endorsed by 3+ reviewers)

- **Delete/move the v1→v6.1 changelog from SKILL.md** — backed by Own, A, B, C, D.
- **Shrink SKILL.md into a router + gates; move mechanics into references** — backed by Own, A, B, C, D.
- **Make DCF non-default and add 1 Pager + NTM PE as the default valuation package** — backed by Own, A, B, D.
- **Fix consensus-source hierarchy: VAActuals/workbook consensus first, BQL only fallback/refresh-on-open** — backed by Own, A, B, D.
- **Rewrite Mini Model spec to allow VAActuals-linked actuals and reconciliation/residual rows** — backed by Own, A, B, D.
- **Add a real alternative-asset-manager engine reference** — backed by Own, A, B, D.
- **Add a top-of-Model Summary/Simple Income Statement** — backed by Own, A, B, D.
- **Add living-model update mode** — backed by Own, A, B, D.
- **Add optional Daloopa actual-ingestion mode** — backed by Own, B, D.
- **Add alt-data staging-tab + date lookup plumbing** — backed by Own, A, B.
- **Allow toggleable scenario/sidecar overlays instead of banning all scenario feeds** — backed by Own, A, B, D.
- **Add cohort/vintage triangle grammar** — backed by Own, A, B, D.
- **Make column layout adaptive via a map, not hard-coded A:K/L** — backed by Own, A, B, D.
- **Add audit scripts instead of prose-only verification** — backed by Own, A, B, C.
- **Permit a third banner tier for fund/product child blocks** — backed by Own, B, D.

# 2. Disputes — take a side

**DCF: delete entirely vs keep opt-in.**  
Take the opt-in side. Do not delete `references/dcf-tab.md`; demote it. Some future user may explicitly ask for intrinsic valuation. But the default full build should produce **1 Pager + NTM PE**, not DCF, because all finished evidence points there. Edit SKILL.md so DCF is loaded only on “DCF,” “intrinsic value,” “long-term cash flow,” or explicit user request.

**VAActuals links: allow everywhere vs restrict by role.**  
Do not make “green VAActuals everywhere” the new law. That creates a different mess. Use role-based rules: Model-tab reported actuals default to blue press-release hardcodes unless Daloopa/actual-link mode is selected; Mini Model actual years may green-link to VAActuals; Street/consensus rows should be red or dark-green depending tab convention, but never treated as build-time truth. This preserves auditability while matching finished Mini Models.

**BQL canary: remove vs demote.**  
Demote. BQL formulas are useful on the user’s Bloomberg machine, especially 1 Pager/NTM PE. They are useless for build-time verification. Remove “BQL canary live” from gates. Add text: “BQL formulas are refresh-on-open formulas; do not claim numeric verification from them in Python/openpyxl.”

**Scenario memos: informational only vs feeding P&L.**  
Allow feeding only through an explicit toggle bridge. Inline scenario memos remain informational. Sidecar/thematic modules may feed the model if there is a blue `Include? 1/0` row, base case defaults to 0 unless user says otherwise, and an EPS/revenue impact bridge is shown. This matches HOOD without turning every memo into a hidden driver.

**Third banner tier: strict two-tier vs flexible tiers.**  
Permit a third tier. The existing two-tier rule is too rigid for BX-style fund blocks. But do not encode BX theme colors as universal. Define roles: major section, sub-section, repeating child/product/fund header. Give a default child fill such as `#FFEA8F`; allow theme-equivalent fills when copying an existing workbook.

**Seasonality color: switch to red vs keep brown.**  
Do not waste prompt budget enforcing a color migration. Add the actual analytical structure — “Vs Normal Seasonality” — and leave color under the formatting reference. The finished books are inconsistent. The row matters more than the hex.

**Summary IS placement: rows 1–40 vs current scaffold.**  
Do not break the period scaffold. Add a Summary IS immediately below the frozen period banner and above the detailed P&L, or reserve a clearly defined top block if the workbook style already supports it. The actionable rule: the Model should open with a compact linked headline view before the deep engines.

**Asset-manager depth: put full BX grammar in SKILL.md vs reference.**  
Reference only. SKILL.md should say “If alt manager, read `references/alternative-asset-manager-engine.md` before scoping.” Putting fund lifecycle mechanics into SKILL.md repeats the retail-broker bloat problem.

# 3. Rejects

- **Delete `dcf-tab.md` outright** — unnecessary; make it opt-in.
- **Make all Model-tab actuals green VAActuals links by default** — weakens press-release tie discipline and conflicts with HOOD/BX Model tabs.
- **Encode specific HOOD lines like Trump Accounts, Rothera, NFL structure, Agentic formulas** — overfit; convert to generic new-initiative/event/thematic grammars.
- **Encode BX fund names in SKILL.md** — overfit; fund list must come from the company supplement/10-K.
- **Adopt IBKR legacy Arial/interleaved annual layout for new builds** — compatibility only, not new standard.
- **Replicate user typos or messy labels** — noise.
- **Make red attention-flag fills a major rule** — useful but low-value; mention as optional workflow convention in formatting reference, not SKILL.md.
- **Require fundraising research tabs by default** — too company-specific; build only if source materials include fund-level fundraising data or user asks.
- **Build every optional advanced module every time** — destroys compliance and bloats output.
- **Keep live BQL consensus as a hard verification gate** — impossible in the build environment.

# 4. Final ranked top 10

**1. Rewrite SKILL.md as a short router + gate file**  
Edit `SKILL.md`: delete the lineage/changelog, remove repeated formatting minutiae, collapse the 19-item checklist into 5 gates, and add a “References to load by decision” table. Move detailed period banner, annual boxes, number formats, EPS strip, Up-C, roll-on/off, and downstream verification into references. Target ~120–150 readable lines. Impact: **highest instruction-following improvement**; current file is too dense to obey reliably.

**2. Add an explicit consensus-source hierarchy**  
Edit `SKILL.md`, `references/drivers-tab.md`, `references/qtr-model-vs-street.md`, and `references/mini-model.md`. New hierarchy: `(1) VAActuals/workbook consensus tab, (2) existing Drivers/consensus staging, (3) red hardcoded consensus snapshot, (4) BQL refresh-on-open formulas.` State that BQL cannot be evaluated at build time and is never a verification source in openpyxl. Impact: **fixes a core contradiction and prevents fake tie checks.**

**3. Replace default DCF with 1 Pager + NTM PE valuation package**  
Create `references/one-pager.md` and `references/ntm-pe.md`; edit SKILL.md Downstream/Build Order. Default downstream becomes Model → Mini Model → Revisions → Drivers → Qtr → 1 Pager → NTM PE. DCF becomes opt-in. 1 Pager spec: B1:O64 risk/reward, bear/base/bull EPS × multiple grids for two out-years, Model EPS green links, Street EPS red links, key Bloomberg stats, relative P/E vs SPX/QQQ, trailing performance, IR block. NTM PE spec: subject + two index BDH spills, VLOOKUP date alignment, median/±1σ bands. Impact: **matches the actual finished valuation layer.**

**4. Update Mini Model to current VA-linked convention**  
Rewrite `references/mini-model.md`; edit SKILL.md hard rules and acceptance text. Default Mini Model: actual years green-link to VAActuals if present, otherwise hardcode/link from audited Model annuals; estimates are driven in-tab by blue-on-yellow drivers; estimate totals may pin to VA/consensus with “Other / reconciling” residual; include “Checks & Sources” and “Base Case” label. Keep “self-contained” only as optional export mode. Impact: **removes a direct conflict with finished HOOD/BX.**

**5. Add `references/alternative-asset-manager-engine.md`**  
New mandatory sector reference for BX/KKR/APO/ARES/BAM/CG-style companies. Include flagship fund lifecycle block: fee-rate assumptions, commitments walk, capital invested/dry powder, realizations, NAV walk with market residual, MOIC, FPAUM walk, binary step-down trigger, cumulative post-stepdown flag, management fees. Add perpetual vehicle SUMPRODUCT fee blocks, segment AUM walk, FRE/PRE/carry bridge, and fundraising-support-tab rules. Impact: **turns asset-manager output from toy to usable.**

**6. Add Summary/Simple Income Statement at top of Model**  
Edit `SKILL.md` P&L layout and `references/model-engine.md`. Reserve a compact 30–40 row headline summary before the detailed business rollup: revenue, expenses, PPNR/FRE/EBITDA as relevant, PTI, tax, NI, EPS, shares, key margins, ROE/ROTCE where relevant. It green-links to the detailed Model lines; no drivers. Impact: **large visual/architectural match to finished HOOD/BX.**

**7. Add living-model update mode**  
Create `references/update-mode.md`; add a top-level mode router in SKILL.md: “fresh build vs update existing workbook.” Update mode steps: append quarter/month columns, extend SUMIFS ranges, redraw period separators, roll focal shapes, refresh Monthly/Daloopa/VAActuals/staging tabs, convert newly reported quarter to actuals, stack guidance vintage using script, re-snapshot Revisions Old/New, update 1 Pager EPS links and NTM PE ticker formulas. Impact: **aligns the skill with how these workbooks are actually maintained.**

**8. Add reusable driver grammars reference**  
Create `references/driver-grammars.md`; link from Step 0 KPI scan and sector scoping. Include cohort/vintage triangle, subscription attach/new-vs-backbook engine, event/deal calendar, new-initiative valuation stub, toggleable thematic overlay with on/off row, 2Q stack rows, and “Vs Normal Seasonality” for monthly blocks. Keep examples generic; no HOOD-specific labels. Impact: **captures the manual analytical depth without overfitting.**

**9. Add staging/actuals infrastructure: alt-data + Daloopa + Monthly**  
Create `references/data-staging.md` and optionally `scripts/ingest_staging_data.py`. Define raw staging tabs for internal feeds, Sensor Tower/card/app/peer data, month-end normalization, XLOOKUP/VLOOKUP by date into Model, source/date cells, missing-month flags, and K-column tags. Add optional Daloopa mode: column A tag IDs, actual formulas via INDEX/MATCH to `Daloopa`, blue hardcode fallback where no tag exists, press-release tie checks retained. Impact: **reduces manual data plumbing and supports living models.**

**10. Add `scripts/audit_workbook.py` and make it a gate**  
Create a workbook audit script checking: font family/size, yellow formula cells, blue estimate hardcodes without yellow, error cells including hidden Qtr ranges, check rows nonzero, annual SUMIFS range consistency, Mini Model reference policy by mode, VAActuals/BQL source policy, and basic color-role violations. Edit SKILL.md Verify section: agent must run script and report failures; image checks remain only for borders/shapes that openpyxl cannot fully validate. Impact: **cuts hallucinated compliance and makes the long spec enforceable.**