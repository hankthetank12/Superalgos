# 1. Weaknesses as a prompt artifact

**1. The "Dead-Environment Verification" Paradox**
The prompt mandates live `BQL(...)` formulas for consensus, but also mandates a strict verification gate: "Estimates tie consensus at seed (EPS to the cent)... Verify the Model... do not start step 10 until it passes." Because Claude Code uses openpyxl/Python, it cannot evaluate BQL formulas at build time. When the agent reads the workbook back to verify the tie, the BQL cells will yield `None` or string literals, not numbers. The agent will either hallucinate a successful verification, silently overwrite the BQL with hardcodes to force a pass, or fail in a loop. 

**2. Context-Window Pollution (The Changelog)**
The first 400 words of `SKILL.md` are a changelog ("v6 changes vs v5", "Prior lineage — v4 vs v3"). LLMs do not need to know what v3 did in 2024 to build a model today. This wastes premium early-context tokens, dilutes the system prompt's weight, and pushes actual build instructions further down the context window where attention degrades.

**3. Checklist Fatigue and Centralization**
The 19-point "Final acceptance checklist" in `SKILL.md` is an anti-pattern for coding agents. By the time the agent is building the Qtr tab (Step 13), it has to hold the entire 19-point checklist in context. Progressive disclosure is broken here: tab-specific verification rules should live *only* in their respective reference files, not in the master `SKILL.md`.

**4. Contradictory Instructions on VAActuals**
The master skill screams "**No green links to VAActuals, ever.**" But the user's newer standalone mini-model skills (and the finished ground-truth models) explicitly use green links to VAActuals. Forcing the agent to obey an outdated master rule while trying to emulate a newer reference pattern creates instruction-following collisions.

**5. Missing Automation Leverage for Staging**
The agent is told to build market-data tracking blocks and alt-data memos, but the ground truth shows the user relies on massive VLOOKUP/INDEX-MATCH staging tabs (Sensor Tower, Relay Data, Daloopa). Writing 2,000 rows of alt-data via openpyxl cell-by-cell is incredibly slow and token-heavy. The skill lacks a bundled Python script (like the guidance overlay) to ingest CSVs into staging tabs mechanically.

# 2. Content gaps vs the finished models

**High-Value Gaps (Must Close):**
*   **The Valuation Layer Mismatch:** The skill forces a DCF every time. The user *never* uses the DCF in the finished models, relying instead on a "1 Pager" (Risk/Reward, multiples, Bloomberg stats) and an "NTM PE" valuation history tab. The skill is wasting tokens building a tab the user deletes or ignores.
*   **Alt-Manager Engine:** The skill has a massive `retail-broker-engine.md` but dismisses asset managers with one sentence ("AUM roll-forward × fee rate"). The BX ground truth proves alt-managers require a deep, 50-row per-fund lifecycle engine (Commitments → Deployed → Realized → NAV → FPAUM with step-down triggers).
*   **Summary Income Statement:** Both HOOD and BX feature a ~35-row "Simple Income Statement" at the top of the Model tab. The skill jumps straight into the deep business rollup.
*   **Toggleable Scenario Switches:** The HOOD model uses explicit "on / off" binary input rows (e.g., Agentic impact, step-down triggers in BX) that mechanically feed the P&L. The skill only knows about "informational" scenario memos.
*   **Cohort/Vintage Matrix:** The HOOD model uses a triangular cohort retention matrix. The skill mentions "cohort stats" as a generic KPI but lacks the structural grammar to build a retention triangle.

**Noise / Overfit (Ignore):**
*   "Trump Accounts" or specific "Agentic impact" thematic tabs (the *mechanics* of the toggle switch are general, the specific themes are not).
*   Specific Daloopa series IDs in column A (unless the user provides a mapping CSV, the agent can't guess these).
*   Typos in the user's finished models.

**Inferred Gaps (Process):**
*   **"Update Mode" vs "Fresh Build":** The finished models are living documents. The skill assumes a 100% fresh build every time. There is no instruction path for "Append Q3, roll the focal column, and update the Revisions snapshot."

# 3. Prioritized suggestions (max 15)

**S1. Replace the DCF with "1 Pager" and "NTM PE" tabs**
*   **Where:** Delete `references/dcf-tab.md`. Create `references/1-pager-valuation.md`. Edit `SKILL.md` downstream tabs section.
*   **What:** Instruct the agent to build the 1 Pager (Base/Bear/Bull EPS x multiple grids, R/R ratios, Bloomberg BDP/BDH key stats block) and the NTM PE tab (3 BDH spills + VLOOKUP alignment).
*   **Impact:** HIGH. Directly aligns the output with the user's actual valuation workflow.
*   **Effort/Risk:** Low risk. The BDP/BDH formulas will be dead at build time, but this is acceptable for the 1 Pager as they will self-heal when the user opens Excel.

**S2. Fix the Consensus Verification Paradox (VAActuals Fallback)**
*   **Where:** `SKILL.md` (§ EPS strip, § Estimates, § Verify and report).
*   **What:** Change the rule to: "If a `VAActuals` tab exists, the EPS strip and consensus seeds MUST link to it (`=VAActuals!...` in dark green #006600). ONLY use BQL formulas if `VAActuals` is missing. If using BQL, skip the automated value-tie verification for consensus, as openpyxl cannot read uncalculated BQL."
*   **Impact:** HIGH. Prevents agent loops/hallucinations during the verification step.

**S3. Create `references/alt-manager-engine.md`**
*   **Where:** New reference file. Add trigger to `SKILL.md` Step 2.
*   **What:** Define the flagship fund lifecycle block: Fee rate inputs → Commitments walk → Capital Invested walk → Realizations walk → NAV walk → FPAUM walk with a binary "Step-Down Trigger" row → Mgmt fees. Include Perpetual vehicle SUMPRODUCT rollups.
*   **Impact:** HIGH. Closes the massive architectural gap for the BX use case.

**S4. Update Mini Model to match current VAActuals linking preference**
*   **Where:** `references/mini-model.md` and `SKILL.md` (§ Downstream tabs).
*   **What:** Remove the "NO VAActuals links" rule. Instruct that actual years should be green links (`#006600`) to VAActuals, and estimate totals can pin to VAActuals with an "Other / reconciling" residual row.
*   **Impact:** HIGH. Aligns with the user's newer v7 mini-model skills and ground truth.

**S5. Add "Summary Income Statement" to the Model tab skeleton**
*   **Where:** `SKILL.md` (§ P&L layout).
*   **What:** Mandate a compact, ~35-row linked Summary IS at the top of the Model tab (rows 1-40), using same-tab green links (`#006600`) to pull from the deep business rollup below it.
*   **Impact:** MED. Matches the visual hierarchy of HOOD and BX.

**S6. Formalize Alt-Data Staging Tabs via Python Script**
*   **Where:** `SKILL.md` (§ Market-data tracking) and new script `scripts/ingest_staging_data.py`.
*   **What:** Instead of writing 2,000 rows of alt-data via openpyxl cell-by-cell, instruct the agent: "If the user provides raw alt-data (e.g., Sensor Tower, card data), use `ingest_staging_data.py` to create a staging tab and write the data. On the Model tab, use `EOMONTH` and `VLOOKUP` to pull from the staging tab."
*   **Impact:** MED. Drastically reduces token usage and build time for data-heavy models.

**S7. Introduce the "Toggleable Scenario Switch" Pattern**
*   **Where:** `SKILL.md` (§ Scenario memos).
*   **What:** Upgrade scenario memos to active switches. "For thematic uplifts or step-downs, build an 'On/Off' blue input row (1=on, 0=off). Multiply the scenario's output by this switch before adding it to the live P&L."
*   **Impact:** MED. Captures the HOOD "Agentic" and BX "Step-down" mechanics.

**S8. Add Cohort/Vintage Retention Matrix Grammar**
*   **Where:** `SKILL.md` (§ Forecast mechanisms).
*   **What:** Define the cohort triangle: "Quarterly cohort matrix: one row per cohort vintage, diagonal blue retention/decay multipliers, New Customers diagonal, per-cohort contribution roll-up → Calculated NNA vs Actual NNA with red plug."
*   **Impact:** MED. Standardizes a complex structure the user clearly values.

**S9. Standardize 3rd-Tier Banners and Attention Flags**
*   **Where:** `SKILL.md` (§ Borders & structure, § Color & format).
*   **What:** Add a 3rd banner tier: D-level product/fund headers use `#FFEA8F` (gold). Add a rule for attention flags: "Use `#C00000` (red) fill with white text for blue inputs that require urgent user review/update."
*   **Impact:** LOW. Minor visual alignment, but improves the user's post-generation workflow.

**S10. Add "Update Mode" Routing**
*   **Where:** `SKILL.md` (§ When to use, § Build order).
*   **What:** Add a trigger: "If the user asks to 'roll the quarter' or 'update the model', do NOT build fresh. 1. Append a new quarter column. 2. Roll the focal column shapes. 3. Update actuals from the new press release. 4. Run the Revisions snapshot."
*   **Impact:** MED. Expands the skill's utility to the maintenance phase of the model lifecycle.

**S11. Strip the Changelog from SKILL.md**
*   **Where:** `SKILL.md` (Top section).
*   **What:** Delete the entire "v6 changes vs v5", "v6.1", "Prior lineage", etc.
*   **Impact:** HIGH (Prompt Engineering). Saves ~400 tokens of prime context window, improving instruction adherence for the actual build rules.

**S12. Decentralize the Acceptance Checklist**
*   **Where:** `SKILL.md` (§ Final acceptance checklist).
*   **What:** Keep items 0-14 (Model tab checks) in `SKILL.md`. Move items 15-19 into their respective reference files (`mini-model.md`, `revisions-tab.md`, etc.).
*   **Impact:** HIGH (Prompt Engineering). Reduces context bloat. The agent only reads the Mini Model checklist when it is actually building the Mini Model.

**S13. Standardize Seasonality Row Formatting**
*   **Where:** `SKILL.md` (§ Color & format convention).
*   **What:** Change seasonality memos from brown `#833C0C` to red `#FF0000` to match the HOOD ground truth. Add the "Vs Normal Seasonality" delta row definition.
*   **Impact:** LOW. Pure formatting alignment.

**S14. Standardize "Core vs GAAP" Parallel P&L**
*   **Where:** `SKILL.md` (§ P&L layout).
*   **What:** Add instruction: "If the company heavily adjusts earnings, build a 'Core' parallel P&L block (Core Revenue, Core PPNR) isolating non-recurring lines (MTM, restructuring) from the GAAP rollup."
*   **Impact:** LOW. Captures the IBKR architecture.

**S15. Relax Column Hardcoding**
*   **Where:** `SKILL.md` (§ Sheet grid & header scaffold).
*   **What:** Change "Columns A–G indent; H–I label helpers; J–K main label columns" to "Adapt to existing layouts if updating (e.g., IBKR legacy uses E for data). For fresh builds, default to B-K for labels, L for first data column."
*   **Impact:** LOW. Prevents the agent from destroying the legacy IBKR layout if asked to update it.

# 4. What to remove or simplify

**1. Remove the DCF Tab entirely**
*   *Rationale:* The gap analysis proves the user doesn't use it. They use the 1 Pager and NTM PE tabs. Forcing the agent to build a complex DCF wastes API costs, context window, and time, while increasing the surface area for build errors. Delete `references/dcf-tab.md` and remove all DCF mentions from `SKILL.md`.

**2. Remove the Changelog / Lineage text**
*   *Rationale:* LLMs do not need to know the version history of their own prompt. Delete the paragraphs starting with "Naming: this combined skill is v5...", "Prior lineage...", and "v6 changes vs v5". Keep only the functional description of what the skill *does*.

**3. Simplify the "No Green Links to VAActuals" rule**
*   *Rationale:* It contradicts the user's current workflow (BX Mini Model, HOOD). Remove the absolute ban. Replace it with: "Use green links (`#006600`) to VAActuals for historical periods in the Mini Model and Summary IS. For the main Model tab, actuals remain blue hardcodes."

**4. Remove the Downstream Tab Verification from SKILL.md**
*   *Rationale:* Items 15-19 in the Final Acceptance Checklist bloat the main prompt. Move them into the respective `.md` reference files. The agent should only see the Qtr tab verification rules when it loads `qtr-model-vs-street.md`. This is the essence of progressive disclosure.