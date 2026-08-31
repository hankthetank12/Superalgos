# 1. Consensus (endorsed by 3+ reviewers)
*   **Replace mandatory DCF with 1 Pager + NTM PE tabs**: All 4 critiques agree the DCF is unused ground-truth bloat; the real valuation surface is the 1 Pager/NTM PE pair.
*   **Add an Alt-Manager Engine reference**: All 4 agree the single-sentence AM instruction fails the BX ground truth; a 50-row fund-lifecycle engine is required.
*   **Fix the Consensus/VAActuals paradox**: All 4 agree the strict "live BQL" and "no VAActuals links" rules break the build environment and contradict the user's actual Mini Model workflow.
*   **Add a Summary Income Statement**: All 4 note HOOD and BX use a 30–40 row headline block at the top of the Model tab.
*   **Add an "Update Mode" workflow**: All 4 point out the skill assumes a one-shot birth, ignoring the living-model maintenance loop (appending quarters, rolling Revisions).
*   **Strip the changelog/lineage**: All 4 identify the 400-word version history at the top of `SKILL.md` as prime context-window poison.
*   **Decentralize the 19-point checklist**: All 4 agree the monolithic checklist breaks progressive disclosure; tab-specific checks belong in tab-specific reference files.
*   **Add a Capital & Returns block**: 3 critiques (A, B, D) note ROE, BVPS, and payout ratios are standard financials modules missing from the P&L skeleton.
*   **Add Cohort Triangle & Toggleable Scenarios**: All 4 agree HOOD's cohort matrix and "on/off" scenario toggles are reusable grammars, not one-off memos.
*   **Relax hardcoded column layouts**: 4 critiques agree forcing A–K labels breaks compatibility with legacy models (like IBKR).

# 2. Disputes — take a side

**Dispute 1: Should we move ALL formatting rules to a new reference file?**
*   *Critiques A & B* want to move colors, borders, and fonts to a `references/formatting-and-audit.md` to shrink `SKILL.md`.
*   *My Side:* **Keep the top 5 invariants in `SKILL.md`, move the rest.** If you move *all* formatting to a reference, the agent will hallucinate colors and fonts while building the initial P&L skeleton before it decides to load the formatting reference. Keep Calibri 9, the blue/green/red/yellow color dictionary, and the two-tier banner rule in `SKILL.md`. Move the EPS strip minutiae, two-phase box writes, and SUMIFS `$X:$BL` string patterns to a reference.

**Dispute 2: Python Audit Script vs. Prose Checklist**
*   *Critiques A & B* suggest writing a `scripts/audit_model.py` to programmatically verify fonts, SUMIFS ranges, and check rows.
*   *My Side:* **Reject the script; use a 5-gate prose checklist.** Writing a bulletproof Python Excel auditor for dynamic, multi-sector financial models is highly brittle (openpyxl struggles with evaluated formula states and complex merged ranges). A failing, buggy audit script will trap the agent in an infinite loop. Collapse the prose checklist into 5 strict gates instead.

**Dispute 3: Daloopa INDEX/MATCH vs. Press Release Hardcodes**
*   *Critiques A, B, D* suggest adding Daloopa column-A tag IDs as an actuals ingestion method.
*   *My Side:* **Make it an explicit opt-in, not the default.** The prompt constraints emphasize "actuals tied to the dollar against the press release." Daloopa requires a specific column-A mapping that the agent cannot guess without a pre-existing staging sheet. Add it to `SKILL.md` as: *"If a 'Daloopa' tab exists, use Col A for series IDs and INDEX/MATCH for actuals; otherwise, use blue hardcodes."*

**Dispute 4: Sidecar What-If Tabs vs. Inline Toggleable Rows**
*   *Critique A* wants separate sidecar tabs for thematic scenarios (like HOOD's Agentic/EU TAM).
*   *My Side:* **Use inline toggleable rows.** Mandating sidecar tabs for every thematic scenario bloat the workbook and overfits to HOOD. A blue `1/0` toggle row directly above the affected P&L line (which multiplies the scenario output before adding it to the base case) achieves the exact same mechanical feed with 90% fewer tokens.

# 3. Rejects

*   **Overfitting to HOOD/BX names:** Do not encode "Trump Accounts," "NFL Event Structure," or "BCP IX" into the skill. Use generic "Event Calendar" and "Flagship Fund I" grammars.
*   **Mandatory DCF:** Do not keep the DCF as a default. It wastes API costs and context window for a tab the user ignores.
*   **Dead BQL Canary:** Do not force the agent to write a `BDP` canary cell that evaluates to `#N/A` or `None` in the Python build environment. It breaks the verification step.
*   **"No green links to VAActuals, ever":** Reject this absolute ban. It directly contradicts the user's newer v7 mini-model skills and the finished ground truth.

# 4. Final ranked top 10

**1. Strip Changelog & Collapse Checklist (Prompt Engineering)**
*   *Where:* `SKILL.md` (Top intro & § Verify and report).
*   *What:* Delete the entire "v6 changes vs v5", "Prior lineage", etc. Replace with: *"This is v5. See git for lineage."* Replace the 19-point checklist with 5 gates: 1. Research/Scope, 2. Model Tab Audit (ties, checks=0), 3. Sector Module Audit, 4. Formatting Audit, 5. Downstream Tabs Audit. Move items 15–19 into their respective `references/*.md` files.
*   *Impact:* HIGH. Saves ~800 tokens of prime context window, immediately improving instruction adherence for the actual build rules.

**2. Replace DCF with 1 Pager + NTM PE (Valuation Layer)**
*   *Where:* `SKILL.md` (§ Downstream tabs, Build Order 14); delete `dcf-tab.md`; create `references/1-pager-ntm-pe.md`.
*   *What:* Remove DCF from the default build (make it trigger-only). Instruct the agent to build the 1 Pager (B1:O64 layout, Base/Bear/Bull EPS × multiple grids, relative P/E vs SPX, IR block) and NTM PE tab (3 BDH spills, VLOOKUP date alignment). Note that BQL/BDH formulas will be dead at build time but will heal on the user's desktop.
*   *Impact:* HIGH. Eliminates the largest architectural gap between the skill's output and the user's finished workbooks.

**3. Add Alt-Manager Engine (Sector Architecture)**
*   *Where:* `SKILL.md` (§ Sector variants); create `references/alt-manager-engine.md`.
*   *What:* Replace the single-sentence AM instruction. Define the flagship fund lifecycle block: Fee rate inputs → Commitments walk → Capital Invested walk → Realizations walk → NAV walk → FPAUM walk with a binary "Step-Down Trigger (1/0)" row → Mgmt fees. Include Perpetual vehicle SUMPRODUCT rollups and a Segment AUM walk with red residuals.
*   *Impact:* HIGH. The skill currently cannot produce a functional Blackstone (BX) or alternative asset manager model.

**4. Fix Consensus Hierarchy & Mini Model Linking (Instruction Collision)**
*   *Where:* `SKILL.md` (§ EPS strip, § Estimates, Hard Rules); `references/mini-model.md`.
*   *What:* Change the consensus rule: *(1) VAActuals tab (green links for actuals, red for consensus) → (2) Red hardcodes seeded by user → (3) BQL formulas (optional, skip automated value-tie verification since openpyxl cannot read them).* In the Mini Model, explicitly allow green links to VAActuals for historical years and a "Consensus reconciliation" residual row for estimates.
*   *Impact:* HIGH. Stops the agent from hallucinating during verification and aligns the output with the user's actual linking preferences.

**5. Add Summary Income Statement Block (P&L Layout)**
*   *Where:* `SKILL.md` (§ P&L layout, Build Order 4).
*   *What:* Mandate a compact, 30–40 row "Summary Income Statement" at the top of the Model tab (rows 1–40). It must contain headline revenues, key KPIs, PPNR/EBITDA, Net Income, and EPS. Use dark-green (`#006600`) same-tab links to pull from the deep business rollup below it.
*   *Impact:* MED-HIGH. Matches the visual hierarchy and executive-summary layout of both HOOD and BX.

**6. Add "Update Mode" Workflow (Living Model Maintenance)**
*   *Where:* `SKILL.md` (New section: § Update Mode, before Build Order).
*   *What:* Add a routing instruction: *"If the user asks to 'update', 'roll', or 'append', DO NOT build fresh. 1. Append a new quarter column. 2. Roll the focal column shapes. 3. Update actuals from the new press release. 4. Run the Revisions 'Old' snapshot. 5. Restate seasonals. 6. Run `insert_guidance_rows.py` if adding guidance."*
*   *Impact:* MED-HIGH. Expands the agent's utility from one-shot generation to the actual day-to-day maintenance of the models.

**7. Add Capital & Returns Block (P&L Layout)**
*   *Where:* `SKILL.md` (§ P&L layout, after Tax & NCI).
*   *What:* Define a standard Capital & Returns block: Payout ratio (dividend + buyback / op NI), BVPS/TBVPS with growth rows, ROE/ROTCE (GAAP and adjusted), operating leverage YoY, and a Change in Share Count row.
*   *Impact:* MED. Standardizes a critical financial module present in the finished HOOD and IBKR models that the skill currently omits.

**8. Add Cohort Triangle & Toggleable Scenarios (Driver Grammars)**
*   *Where:* `SKILL.md` (§ Forecast mechanisms, § Scenario memos).
*   *What:* Define the Cohort Triangle: Vintage rows, diagonal retention/decay blue inputs, new-customer diagonal, and rollup to implied NNA vs Actual. Upgrade scenarios: Allow a blue `1/0` "On/Off" toggle row that multiplies a stressed driver block, feeding the live P&L when toggled on.
*   *Impact:* MED. Captures the complex, mechanized driver structures the user builds manually, without overfitting to specific company themes.

**9. Add Alt-Data Staging Pattern (Data Plumbing)**
*   *Where:* `SKILL.md` (§ Market-data tracking blocks).
*   *What:* Define the staging pattern: *"For large alt-data feeds (e.g., app downloads, card data), create a raw staging tab. On the Model tab, use `EOMONTH` and `VLOOKUP` or `INDEX/MATCH` to pull the month-end values into the Month 1/2/3 structure."*
*   *Impact:* MED. Prevents the agent from trying to write 2,000 rows of raw data directly into the Model tab's memo blocks via openpyxl.

**10. Relax Column Layouts & Allow 3rd Banner Tier (Formatting)**
*   *Where:* `SKILL.md` (§ Sheet grid, § Borders & structure).
*   *What:* Change column rules to: *"Default: labels B–K, data from L. If updating an existing workbook, respect its layout (e.g., IBKR data from E)."* Update banner rules: Allow a 3rd tier for repeating child blocks (e.g., per-fund or per-product) using `#FFEA8F` (gold) at column D.
*   *Impact:* LOW-MED. Prevents the agent from destroying legacy layouts during updates and allows the necessary visual depth for complex asset managers.