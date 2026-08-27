 # 1. Weaknesses as a prompt artifact

**Lineage bloat at the top.** The first 278-line SKILL.md opens with 4 paragraphs of v1→v6.1 changelog before stating what to do. That history belongs in a `CHANGELOG.md` or the repo README, not in the agent's working context. It dilutes the instruction signal before the model even reaches "Research first."

**Ultra-long lines = parsing risk.** 74KB across 278 lines means ~260 chars/line. LLM agents tokenize and attend poorly to horizontal wrapping; boundary rules like "medium WHITE vertical borders inside the banner" get lost when the line also contains 6 other formatting directives. Break formatting specs into bullet tables or move them to a dedicated `references/format-spec.md`.

**The 19-item acceptance checklist is unauditable.** A single LLM pass cannot hold 19 checklist items plus sub-items 13a–13e in working memory while also writing formulas. Progressive disclosure fails when the verification step is the heaviest part. The checklist should be a 5-gate pass/fail protocol; granular checks belong in the reference files they relate to.

**Contradictions between body and Hard Rules.** The body says Mini Model is "self-contained … no green links"; the finished models and the user's newer standalone `mini-model-v7-8-26` skills explicitly green-link actuals to VAActuals. The Hard Rule "No green links to VAActuals, ever" forces the agent to produce output the user immediately overrides. When skill output is known to be rewritten within minutes, the skill is wrong.

**Build order is 15 steps with no escape hatches.** Steps 10–14 (downstream tabs) each demand a full sub-audit but offer no "skip" condition. If the user only wants a Model tab, the agent has no off-ramp. More importantly, Step 0 ("Research first") has no structural pause—there is no explicit "STOP; wait for user to upload files before scoping" guard.

**Color/format rules are duplicated, not canonical.** #FFFFCC, #F2F2F2, #FFF2CC, #CCCCFF, and banner rules appear in the body, then again in Hard Rules, then again in the checklist. An edit to one does not propagate. Consolidate to a single `references/format-spec.md` table; the body and Hard Rules should reference it, not restate it.

**Reference files are "loaded on demand" but the skill never verifies they were read.** The retail-broker engine is "mandatory" but the build order says "read … NOW" at Step 2—there is no agent-side gate confirming ingestion. If the context window trims the reference, the agent silently proceeds with generic engines.

**insert_guidance_rows.py is under-leveraged.** It is described in the Guidance overlay section but never appears in the Build Order. An agent following Step 4 linearly will hand-insert rows because the script is not tied to the ordered workflow.

**"When the structure applies" appears 8+ times.** The agent must classify Up-C, rate-sensitive splits, retail-broker status, and alt-manager status without a decision tree. That classification should be a top-level fork (a short "Sector router" table at the top of Build Order), not buried qualifiers.

---

# 2. Content gaps vs the finished models

**1 Pager + NTM PE tabs are missing entirely.** These exist in HOOD and BX with identical B1:O64 layouts. The user re-creates them every model and even wrote a "Replication Guide" tab proving the workflow. Automating this pair would remove more manual work than any other single addition.

**Alternative asset manager engine is one sentence.** BX finished models contain 50+ row fund lifecycle blocks per flagship (commitments, capital invested, realizations, NAV, step-down triggers, FPAUM, fee-rate step-downs). The skill offers "AUM roll-forward × fee rate → FRE." That is a non-starter for BX-level builds.

**Mini Model linkage model is wrong.** Finished mini models green-link actuals to VAActuals and carry a "Consensus reconciliation" residual row—matching the user's standalone v7-x mini-model skills. The skill's "self-contained" mandate produces work the user immediately relinks.

**Consensus philosophy mismatches the build environment.** The skill mandates live BQL formulas + a Bloomberg canary, but the agent cannot evaluate BQL. Finished models replace the EPS strip consensus with red VAActuals links or hardcodes, and the 1 Pager runs Bloomberg pulls only where they self-heal on the user's desktop. The skill should treat BQL as documented-dead formulas and prefer VAActuals/Daloopa when present.

**Simple Income Statement summary block.** Both HOOD and BX place a compact dark-green headline summary at the top of the Model tab. The skill starts straight into deep P&L detail. A headline summary is standard buyside layout.

**Capital & returns block.** ROE/ROTCE, BVPS/TBVPS, payout ratios, operating leverage, and change-in-share-count rows appear in finished models but not in the skill's P&L/expense section. These are standard for financials.

**Daloopa tag-ID actuals pattern.** IBKR finished model automates actuals via column-A Daloopa series IDs. The skill mandates hand-keyed blue hardcodes from the press release. Even if not universal, an optional Daloopa ingestion pattern dramatically speeds maintenance—a "living model" concern entirely absent from the skill.

**Toggleable scenario overlays vs static memos.** HOOD's "Agentic" overlay uses an on/off toggle feeding the live P&L. The skill restricts scenarios to "informational only … never feed a formula." The finished model proves the user wants mechanized scenario levers, not footnotes.

**Cohort/vintage triangle.** HOOD's cohort matrix is a driver engine, not a memo. It needs its own grammar (vintage rows, decay diagonal, new-customer diagonal, rollup to implied NNA).

**Subscription attach engine.** HOOD Gold uses penetration × funded accounts, with new-user vs backbook attach splits. This is generalizable to any subscription/Desktop tier product (e.g., BX's wealth subscriptions, trading platforms).

**Living-model maintenance workflow absent.** The skill describes a one-shot birth. Finished models are maintained—quarters appended, Revisions re-snapshotted, seasonals restated, Daloopa refreshed. There is no "update mode" section.

**"Vs Normal Seasonality" under monthly blocks.** Finished models compute a seasonal norm and delta; the skill only provides a Seasonals row under %Q/Q.

**Third banner tier in BX.** The skill bans any fill except #375623 majors and #FFF2CC subs. BX uses theme-gold at C (subs) and theme-red-ish at D (per-fund). A rigid 2-tier rule forces the agent to flatten BX's fund depth, breaking the user's visual hierarchy.

---

# 3. Prioritized suggestions (max 15)

**S1. Replace mandatory DCF with 1 Pager + NTM PE as the default valuation downstream tabs**  
*Where:* New `references/1-pager-dashboard.md` and `references/ntm-pe-history.md`; edit SKILL.md § Downstream tabs.  
*Impact:* HIGH. Eliminates the biggest manual reconstruction loop in HOOD/BX. DCF becomes optional or removed unless user explicitly requests it.  
*Effort/Risk:* MED. Layout is already standardized (B1:O64) from ground truth; risk is overfitting the multi-row stat block, but the parameters are generic tickers and EPS links.

**S2. Add `references/alternative-asset-manager-engine.md`**  
*Where:* New reference; edit SKILL.md § Sector variants.  
*Impact:* HIGH. The skill currently cannot produce a BX-grade Model tab. The reference must specify: per-fund commitment/capital-invested/realization/NAV rolls, step-down trigger binary inputs, FPAUM × fee-rate tiering, perpetual-vehicle blending, segment AUM walk with market/flow decomposition, and the Total AUM memo.  
*Effort/Risk:* MED-HIGH. Large spec, but bx ground truth is rich.

**S3. Make Mini Model VAActuals-linkable (drop "self-contained" mandate)**  
*Where:* Edit `references/mini-model.md` and SKILL.md § Downstream tabs + Hard Rules.  
*Impact:* HIGH. Aligns full-model-v5 with the user's newer standalone mini-model skills and finished workbooks. Allow actual-year lines to green-link to VAActuals; add a red "Consensus reconciliation / Other reconciling" residual row; keep estimate drivers as blue inputs.  
*Effort/Risk:* LOW. Policy change, not structural.

**S4. Add Simple Income Statement headline block to Model tab**  
*Where:* Edit SKILL.md § P&L layout.  
*Impact:* MED-HIGH. Place a ~35-row dark-green (#006600) summary at the top: headline revenue, PT income, EPS, key margins, ROE, diluted shares—green-linked to the deep P&L below. This matches HOOD/BX finished tabs.  
*Effort/Risk:* LOW.

**S5. Add Capital & Returns block to Model tab**  
*Where:* Edit SKILL.md, new subsection after Tax & NCI.  
*Impact:* MED. Block: payout ratio (div + buyback / op NI), BVPS/TBVPS growth, TCE/TA, ROE/ROTCE (GAAP and adjusted), operating leverage rows. Standard for financials and present in both HOOD and IBKR finished models.  
*Effort/Risk:* LOW.

**S6. Add living-model "Update mode" protocol**  
*Where:* New section in SKILL.md before Build Order.  
*Impact:* MED-HIGH. Specify: (a) append new quarter columns, restate period banner labels + SUMIFS range + white separators; (b) roll focal-column shape; (c) re-snapshot Revisions "Old" from current Model; (d) restate seasonals with new actual month; (e) refresh Daloopa/Monthly staging; (f) red-flag any hardcoded estimate that became actual.  
*Effort/Risk:* MED.

**S7. Make consensus adaptive: VAActuals-first, BQL as dead-string fallback**  
*Where:* Edit SKILL.md § EPS strip, § Downstream tabs, Hard Rules.  
*Impact:* MED-HIGH. If a VAActuals or consensus staging tab exists, the EPS strip consensus row and Drivers/Qtr Street rows must link there first. BQL strings are written only when no staging tab exists, and the user is warned they are dead until opened on a Bloomberg desktop. Remove the canary-cell requirement in dead-Bloomberg environments.  
*Effort/Risk:* LOW.

**S8. Add optional Daloopa tag-ID actuals ingestion pattern**  
*Where:* Edit SKILL.md § Sheet grid or under Actuals.  
*Impact:* MED. Column A optionally holds Daloopa series IDs; actual columns pull via INDEX/MATCH from a "Daloopa" staging tab. Fallback to blue hardcodes where IDs are missing. Include K-tag convention for source tracking ('Press Release', 'Monthly', 'Daloopa', 'Est per Claude').  
*Effort/Risk:* MED.

**S9. Add toggleable scenario overlay mechanic**  
*Where:* Edit SKILL.md § Scenario memos.  
*Impact:* MED-HIGH. Replace "informational only" with a live overlay: a blue on/off toggle input (1/0), stressed driver rows, and an IF wrapper in the engine so the stressed path flows into the P&L when toggled on. Keep the base case as the default. Add a "Memo: Scenario delta" block showing the dollar impact vs base.  
*Effort/Risk:* MED.

**S10. Add `references/cohort-vintage-engine.md`**  
*Where:* New reference; link from SKILL.md § Per-unit intensity blocks or Sector variants.  
*Impact:* MED. Triangular cohort build: vintage rows (1Q21…), diagonal retention-decay inputs (100%→70%…), new-customer diagonal, per-cohort contribution rollup, implied balance/NNA check vs actual. Generalizes to any unit-based business with disclosed cohorts.  
*Effort/Risk:* MED.

**S11. Add subscription attach engine**  
*Where:* Edit `references/retail-broker-engine.md` or new `references/subscription-engine.md`.  
*Impact:* MED. Penetration rate × funded accounts → subscribers; split into new-user attach vs backbook attach with #Q/Q inputs and red residual; SLICE/data checks. Applicable to HOOD Gold and any premium tier.  
*Effort/Risk:* LOW-MED.

**S12. Permit third banner tier and relax fill absolutism**  
*Where:* Edit SKILL.md § Borders & structure and Color convention.  
*Impact:* MED. Allow #FFEA8F/theme-gold at D-level (HOOD product headers) and theme-derived fills at E-level (BX per-fund) when P&L depth exceeds two tiers. Remove the sentence "These fills belong ONLY to those roles." Keep the prohibition on reusing them for inputs/bands.  
*Effort/Risk:* LOW.

**S13. Add "Vs Normal Seasonality" row under monthly % M/M blocks**  
*Where:* Edit SKILL.md § %-row conventions.  
*Impact:* LOW-MED. For each monthly-disclosed KPI, add a row computing the historical same-month average as the "norm" and a delta row vs that norm.  
*Effort/Risk:* LOW.

**S14. Bind `insert_guidance_rows.py` into the Build Order for living models**  
*Where:* Edit SKILL.md § Build Order Step 4 and § Guidance overlay.  
*Impact:* MED. Explicit instruction: "If adding guidance to an EXISTING workbook (update mode), run `python scripts/insert_guidance_rows.py --config <json>` BEFORE building downstream tabs. Never hand-insert."  
*Effort/Risk:* LOW.

**S15. Collapse final checklist into 5 gated checkpoints**  
*Where:* Edit SKILL.md § Verify and report.  
*Impact:* MED (maintainability). Replace 19 enumerated items with: Gate A (Actuals tie + plugs), Gate B (Estimate seed + wiggle), Gate C (Engine checks + rollforwards all 0), Gate D (Format image-verify: banner separators, boxes, rules), Gate E (Downstream tab links + hidden columns). Move granular sub-checks (13a–13e) into their respective reference files as build-verify bullets.  
*Effort/Risk:* LOW.

---

# 4. What to remove or simplify

**Delete the v1→v6.1 lineage exposition from SKILL.md intro.** Move it to `CHANGELOG.md`. Replace with one sentence: "This is v5; see CHANGELOG for lineage."

**Remove the mandatory DCF from the default downstream tab set.** The user never uses it; it burns build time and context window. Make DCF conditional ("Build DCF only if user explicitly requests a long-form intrinsic value tab").

**Delete the Hard Rule "No green links to VAActuals, ever."** Replace with: "Actuals may be blue hardcodes, blue hardcodes with Daloopa tags, or green links to VAActuals/Daloopa staging. Green links may NOT be used for estimate columns or consensus data." This matches finished-model practice.

**Remove the absolute column-layout prescription (labels A–K, data from L).** Replace with: "Default layout: labels through K, data from L; respect existing label width in update mode or when the workbook uses an interleaved layout (e.g., legacy IBKR)." This prevents layout corruption on living-model updates.

**Consolidate duplicated color/format specifications.** The body, Hard Rules, and checklist all repeat hex codes and banner rules. Pick one canonical location (`references/format-spec.md`); reduce SKILL.md body to "Apply standard format spec; exceptions noted below."

**Remove "BQL live pulls" as the mandatory EPS-strip consensus source.** Replace with adaptive rule (see S7). Keep the derived period-string scaffold for when BQL is used, but do not require a dead canary cell when Bloomberg is unavailable.

**Condense the monthly rate-path, TAM→share, and rollforward sub-specs in SKILL.md.** They are already in reference files or are standard enough to reference. SKILL.md should state "Build per `references/rate-scaffold.md`" rather than re-specifying roll-on/roll-off mechanics in the main file.

**Remove the "Scenario memos are informational only" blanket ban.** Replace with "Base case drivers live on the Model. Optional toggleable scenario overlays may feed the P&L via an on/off switch; document stressed assumptions in a memo block." This legalizes the finished-model pattern.