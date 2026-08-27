# 1. Consensus (endorsed by 3+ reviewers)

1.  **Replace mandatory DCF with "1 Pager" + "NTM PE" tabs as the default valuation layer.** (A, B, C, D)
2.  **Create a full `asset-manager-engine.md` reference for alternative managers (BX).** (A, B, C, D)
3.  **Update Mini Model convention to allow VAActuals-linked actuals, dropping the "self-contained/no green" mandate.** (A, B, C, D)
4.  **Fix the consensus-source hierarchy: prioritize VAActuals/workbook surfaces over live BQL.** (A, B, C, D)
5.  **Add a "Simple Income Statement" summary block at the top of the Model tab.** (A, B, C, D)
6.  **Strip the version-history/changelog preamble from SKILL.md.** (A, B, C, D)
7.  **Add an "Update Mode" for maintaining living models (append quarter, roll focal, refresh).** (A, B, C, D)
8.  **Add a cohort/vintage triangle engine grammar.** (A, B, C)
9.  **Add a toggleable scenario/overlay mechanism (on/off switch) beyond informational memos.** (A, C, D)
10. **Add a capital & returns block (payout, ROE, BVPS) as a default module.** (A, C, D)
11. **Consolidate duplicated formatting specs into a single reference file.** (A, C, D)
12. **Create verification scripts (`audit_model.py`) to replace manual checklist checks.** (A, C)

# 2. Disputes — take a side

**Dispute 1: How rigidly should column layout (A-K labels, L data) be enforced?**
- **Critique C/D:** Make layout adaptive; default to B-K/L but respect existing layouts (e.g., IBKR legacy) in update mode.
- **Critique A:** Keep as default but acknowledge variance for compatibility reads.
- **My Side:** **Adopt adaptive default.** The skill's hard-coded rule is a primary cause of layout mismatch with BX (data starts at O) and breaks any "update legacy model" use case. SKILL.md should define `label_end_col` and `first_data_col` as variables derived from the workbook (defaulting to K and L), consumed by all downstream tabs and formatting sweeps. This is essential for generality and prevents the agent from corrupting existing workbooks.

**Dispute 2: Should Daloopa-based actuals ingestion be added as an optional pattern?**
- **Critique A/C/D:** Yes, add optional mode with column A tag IDs and INDEX/MATCH pulls.
- **Critique B:** Implied gap, but not prioritized.
- **My Side:** **Yes, but as a lightweight optional module.** The gap is high-value for maintenance (IBKR) and aligns with the "living model" goal. However, it must not replace the core "actuals tie to press release" discipline. Create `references/daloopa-actuals.md` that specifies: if a `Daloopa` tab exists, column A can hold series IDs; actual formulas become `IFERROR(INDEX(...), blue_hardcode)`; source tags in column K. This is a targeted addition, not a rewrite.

**Dispute 3: Should a third banner tier (e.g., for per-fund headers) be formally added?**
- **Critique A/D:** Yes, permit a third fill (e.g., #FFEA8F) at D-level.
- **Critique C:** Add but keep generic.
- **My Side:** **Yes, but as a defined role, not a free-for-all.** The two-tier rule is too rigid for BX's fund-level depth, a legitimate sector need. In `references/formatting-and-audit.md`, define a third tier: "Product/Fund Headers" at column D, fill `#FFEA8F` (light gold), black bold. This standardizes the pattern seen in HOOD/BX without overfitting to theme colors. Update the "two-tier" rule language accordingly.

**Dispute 4: How to handle the "No green links to VAActuals" hard rule?**
- **All critiques:** Remove the absolute ban; finished models violate it.
- **My Side:** **Replace with a source-role policy.** The rule is the largest single cause of Mini Model divergence. New rule: "Actual values in the *Model tab* are blue hardcodes (or Daloopa pulls). Actual values in the *Mini Model tab* may be green (`#006600`) links to VAActuals/Model annuals. Consensus/Street values are always red (`#FF0000`) links or hardcodes." This aligns with ground truth while preserving the Model tab's audit trail.

**Dispute 5: Should the skill bundle an alt-data staging tab ingestion script?**
- **Critique B:** Strong yes, create `ingest_staging_data.py`.
- **Others:** Mention pattern but not script.
- **My Side:** **Yes, but only as a simple helper.** Manually writing 2,000 rows of Relay Data via openpyxl is token-prohibitive. A bundled script (`scripts/ingest_csv_to_staging.py`) that creates a tab from a provided CSV and writes a VLOOKUP scaffold is a high-leverage automation for a common, painful task. It respects the token/constraint budget by offloading work from the LLM to code.

# 3. Rejects

1.  **Encode specific HOOD/BX examples (Trump Accounts, BCP IX) into SKILL.md.** (Overfit; keep examples only in sector references.)
2.  **Force all seasonality rows to be red to match HOOD.** (Overfit; the brown vs. red in finished models is inconsistent noise; keep defined color roles.)
3.  **Add "Alt 1 / Alt 2 rate-path EPS variant columns" as a default.** (Overfit to IBKR legacy; scenario toggle pattern covers this generically.)
4.  **Demote BQL entirely to "never write" status.** (Wrong; BQL formulas are valuable as refresh-on-open formulas for the 1 Pager stats; write them as documented-dead strings.)
5.  **Create a full "Replication Guide" tab.** (Redundant; the automation *is* the replication.)
6.  **Formalize "PE/RE Fundraising" research tabs.** (Overfit; these are external research dumps, not model components.)
7.  **Keep DCF as a mandatory tab.** (Consensus reject; contradicts all finished models.)
8.  **Add "Agentic Impact" thematic tab as a default.** (Overfit; the generic "sidecar what-if tab with toggle" pattern suffices.)

# 4. Final ranked top 10

**1. Replace DCF with 1 Pager + NTM PE as Default Valuation**
- **Implementation:** Delete `references/dcf-tab.md`. Create `references/one-pager-ntm-pe.md` with exact B1:O64 layout spec for the 1 Pager (Bear/Base/Bull grids, Bloomberg stats, relative valuation) and the NTM PE tab (3 BDH spills, VLOOKUP alignment). In SKILL.md, rewrite § Downstream tabs and Build Order: after Qtr tab, build 1 Pager then NTM PE. Remove DCF from checklist.
- **Impact:** **HIGH.** Eliminates the most wasteful mandatory tab and delivers the valuation surface the user actually builds manually every time.

**2. Create Full Alternative Asset Manager Engine Reference**
- **Implementation:** New `references/asset-manager-engine.md`. Detail: flagship fund lifecycle (commitments → capital invested → realizations → NAV → FPAUM with binary step-down trigger), perpetual vehicle SUMPRODUCT blend, segment AUM walk with flow/market decomposition, FRE/PRE/carry bridges. In SKILL.md § Sector variants, add "Alternative Asset Managers (BX, KKR, APO): read `asset-manager-engine.md` before building — mandatory for this sector."
- **Impact:** **HIGH.** Closes the massive architectural gap for a core sector; first-pass BX model becomes usable.

**3. Fix Mini Model to Allow VAActuals-Linked Actuals**
- **Implementation:** Rewrite `references/mini-model.md`. New spec: Actual years are green (`#006600`) links to VAActuals (or Model annuals if no VA). Estimate years built from blue driver inputs. Allow a "Consensus reconciliation / Other" residual row. Add "Checks & Sources" block. In SKILL.md, update § Downstream tabs and Hard Rules to reflect this policy change, explicitly reversing the "no green to VA" rule for Mini Model.
- **Impact:** **HIGH.** Aligns the skill's output with the user's current mini-model standard and finished workbooks, eliminating immediate rework.

**4. Implement Adaptive Consensus Source Hierarchy**
- **Implementation:** In SKILL.md § Research first ("Data & consensus sources"), § EPS strip, § Estimates, and § Downstream tabs, insert a clear decision box: "1. If a VAActuals/consensus tab exists, use red links (`=VAActuals!...`) for Street figures. 2. Else, use red hardcodes seeded from user-provided consensus. 3. BQL formulas are written only as refresh-on-open placeholders (e.g., in 1 Pager stats)." Remove the BQL canary cell from the checklist.
- **Impact:** **HIGH.** Solves the "dead-environment verification paradox," prevents agent hallucinations, and matches the user's no-Bloomberg build workflow.

**5. Add "Update Mode" for Living Models**
- **Implementation:** New `references/update-mode.md`. In SKILL.md, add a new § Modes after § When to use: "If the user asks to 'update,' 'roll,' or 'append' a quarter, follow Update Mode." Steps: append column(s), extend period banner/SUMIFS/white separators, roll focal shape, refresh Daloopa/Monthly tabs, re-snapshot Revisions Old, stack guidance vintage, red-flag stale inputs. Update Build Order to reference this mode.
- **Impact:** **HIGH.** Acknowledges that models are living documents; first-pass output is no longer a one-shot artifact but part of a maintainable system.

**6. Strip Changelog & Collapse SKILL.md to a Router**
- **Implementation:** Delete the first ~40 lines of SKILL.md (from "Naming: this combined skill is *v5*..." through the v6.1 changelog). Replace with a 3-bullet summary: "v5 adds Step 0 source-materials gate. Retail broker engine mandatory for that sector. Builds Model + five downstream tabs." Move detailed formatting, BQL strings, Up-C tax math, vintage roll-on mechanics, and border-sweep minutiae to a new `references/model-engine-spec.md`. SKILL.md becomes ~150 lines of routing, philosophy, and gates.
- **Impact:** **HIGH (Prompt Engineering).** Radically improves instruction-following by removing noise and placing detail behind progressive disclosure.

**7. Add Simple Income Statement Headline Block**
- **Implementation:** In SKILL.md § P&L layout, insert a new first subsection: "Summary Income Statement." Mandate a compact ~35-row block at the top of the Model tab (rows 1-40) with: Total Revenues, Op Inc, PT Income, Net Income, EPS, key margins, ROE, diluted shares. Format: dark-green (`#006600`) same-tab links to the deep P&L below. Update Build Order to place this before the deep P&L skeleton.
- **Impact:** **MED-HIGH.** Directly mimics the finished-model hierarchy, providing immediate headline visibility.

**8. Create Verification Scripts (`audit_model.py`)**
- **Implementation:** New `scripts/audit_workbook.py`. Checks: font family/size, fill role violations (yellow on formula, #FFFFCC on non-input), SUMIFS range identity, check rows ≈ 0, Mini Model forbidden references, hidden column errors. In SKILL.md § Verify and report, replace the manual 13-point list with: "Run `audit_workbook.py` and report its JSON output. Resolve any FAILs before proceeding."
- **Impact:** **MED-HIGH.** Replaces unauditable prose checks with automated, actionable validation, drastically reducing compliance drift.

**9. Add Toggleable Scenario Overlay & Cohort Engine Grammars**
- **Implementation:** New `references/driver-grammars.md`. Contains two concise patterns: (1) **Toggleable Overlay:** Blue on/off input (1/0), stressed driver block, engine formula `=BASE + (STRESSED - BASE) * TOGGLE`, memo delta. (2) **Cohort Triangle:** Vintage rows, diagonal retention decay inputs, new-customer diagonal, rollup to implied KPI vs actual with plug. Reference this file in SKILL.md § Scenario memos and § Forecast mechanisms.
- **Impact:** **MED.** Captures high-value, reusable mechanics from HOOD (Agentic, cohort) without overfitting to specific themes, enhancing generality.

**10. Make Column Layout Adaptive with Named Variables**
- **Implementation:** In SKILL.md § Sheet grid & header scaffold, replace the rigid "Columns A–G indent; H–I label helpers; J–K main label columns..." with: "Discover layout: `label_end_col` = last column with bold section headers (default K). `first_data_col` = `label_end_col + 1` (default L). Set `freeze_col = label_end_col`. Respect existing layout when updating." Propagate these variables to all formatting sweeps and downstream tab builds.
- **Impact:** **MED.** Enables compatibility with BX/legacy layouts and makes the skill robust for update scenarios, closing a key architectural divergence.