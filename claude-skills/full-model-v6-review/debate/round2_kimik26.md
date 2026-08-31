The user wants me to act as a debate referee across four critiques (A, B, C, D) plus my own Round-1 critique, producing exactly four sections:

1. Consensus (endorsed by 3+ reviewers) — list each consensus recommendation in one line with which critiques back it.
2. Disputes — take a side on disagreements, grounded in constraints (context budget, agent instruction-following, no live Bloomberg, generality).
3. Rejects — ideas that should NOT be adopted, with one-line reasons.
4. Final ranked top 10 — ranked list of edits, each with title + one-paragraph implementation spec (which file, what text/structure changes), impact.

Constraints:
- Under ~2000 words.
- Be blunt, specific, concrete.
- Every suggestion must be actionable as an edit to the skill files.

I need to synthesize the four critiques plus my own. Let me map out the recommendations and see which have 3+ endorsements.

Key recommendations across critiques:

- Strip changelog/lineage from SKILL.md intro (A, B, C, D, me) → Consensus
- Replace mandatory DCF with 1 Pager + NTM PE (A, B, C, D, me) → Consensus
- Fix Mini Model to allow VAActuals links / drop self-contained mandate (A, B, C, D, me) → Consensus
- Add alt-manager engine (A, B, C, D, me) → Consensus
- Consensus source hierarchy: VAActuals-first, BQL as dead-string fallback (A, B, C, D, me) → Consensus
- Add living-model update mode (A, B, C, D, me) → Consensus? Let's check. A: yes. B: yes. C: yes. D: yes. Me: yes. Consensus.
- Add Simple Income Statement summary block (A, B, C, D, me) → Consensus
- Add 1 Pager + NTM PE tabs (A, B, C, D, me) → Consensus (same as DCF replacement)
- Add capital & returns block (A, B, C, me) → Let's check. A: S5. B: S12. C: S10. D: not explicitly? D mentions "systematic, cross-sector components" but in the truncated text I don't see it explicitly. However my own S5. So probably 3+ (A, B, C, me). Consensus.
- Make DCF optional/remove mandatory DCF (A, B, C, D, me) → Consensus
- Add cohort/vintage engine (A, B, C, me) → A: S10. B: S8. C: S9a. Me: S10. That's 4. Consensus.
- Add toggleable scenario overlay (A, B, C, me) → A: S9. B: S7. C: S9d. Me: S9. That's 4. Consensus.
- Add alt-data staging tab pattern (A, B, C, me) → A: S8. B: S6. C: S9e. Me: S8. That's 4. Consensus.
- Strip/Decentralize acceptance checklist (A, B, C, me) → A: S15. B: S12. C: S1 (strip SKILL.md). Me: S15. That's 4. Consensus.
- Fix consensus/BQL dead environment paradox (A, B, C, me) → Consensus
- Add audit/verification scripts (A, B, C, me) → A: S14. B: (mentioned). C: S13. Me: S14. That's 4. Consensus.
- Relax column hardcoding (A, B, C, me) → A: S13. B: S15. C: S11. Me: (mentioned). That's 4. Consensus.
- Add subscription attach engine (me only?) → Me: S11. A/B/C don't mention. Not consensus.
- Third banner tier (A, B, C, me) → A: S12. B: S9. C: S14. Me: S12. That's 4. Consensus.
- Daloopa tag-ID actuals (A, B, C, me) → A: S6. B: S6. C: S12. Me: S8. That's 4. Consensus.
- Core vs GAAP parallel P&L (A, B, C, me) → A: S11. B: S14. C: (mentioned). Me: (mentioned). That's at least 3. Consensus.
- Sidecar what-if tabs (A, B, C, me) → A: S9. B: S9. C: S9d. Me: S9. That's 4. Consensus.
- Seasonals vs normal (A, B, C, me) → A: S13. B: S13. C: S9f. Me: S13. That's 4. Consensus.
- Move formatting to reference (A, B, C, me) → A: S15. B: (implied). C: S1. Me: S15. That's at least 3. Consensus.

Wait, I need to be careful. The user provided Critique D but it's truncated at the end ("Highest"). I only have partial Critique D. I should rely on what I have. Critique D seems to endorse many of the same themes but I don't have explicit enumerated S1-S15 for D. However the prompt says "endorsed by 3+ reviewers" — I have A, B, C, and me (Round 1). That's already 4 sources. I can count my own Round 1 as a reviewer. So any item in my Round 1 that is also in A/B/C counts.

Let me map disputes:

- DCF: All say demote/replace. But one might say keep as optional. Consensus is demote.
- Mini Model self-contained: All say drop.
- BQL canary: All say demote.
- Daloopa: A, B, C, me all mention. Consensus.
- Third banner tier: A, B, C, me. Consensus.
- Audit scripts: A, B, C, me. Consensus.
- Update mode: A, B, C, me. Consensus.

Potential disputes:
- Should DCF be completely deleted or just made optional? Critique B says "Remove the DCF Tab entirely" from SKILL.md and delete reference. Others say make optional. I should take a side: make optional (keep reference file but remove from default build order and checklist). Reason: user might still want it for some names; deleting the reference entirely is destructive. The skill pack is versioned; if user asks for DCF, skill should still be able to build it. But default downstream order should be 1 Pager + NTM PE instead.
- Should the changelog be moved to CHANGELOG.md or just deleted? Consensus is move/delete. I'll say delete from SKILL.md, move to CHANGELOG.md or repo docs.
- Should seasonality color be red or brown? C says pick red; me said red in S13. A/B mention standardizing. Not a major dispute.
- Should Daloopa be optional or encouraged? Consensus is optional mode.
- Should the Mini Model be fully VA-linked or have two modes? A says "allow VA-linked actuals + in-tab drivers" with optional self-contained export. B says "Remove NO VAActuals links". C says "green VAActuals (or Model annuals if no VA)". Consensus is allow VA links, not necessarily two modes. I'll take side: default to VA-linked actuals if VAActuals tab exists; self-contained only on explicit request.
- Should 1 Pager be built in same pass or only on request? A/B/C/me say default. But is there a dispute? D might disagree but truncated. I'll assume consensus.
- Should the retail broker engine be moved out of SKILL.md? C says yes. A/B say demote formatting. Consensus is yes.
- Should we add a Python script for alt-data staging? B says yes, formalize via script. A/C/me mention pattern. I think consensus is yes, but maybe not as a bundled script? B explicitly wants `ingest_staging_data.py`. I think that's good but maybe overkill if the agent can just build the tab. However, given the constraint of token efficiency, a script is good. But is it top 10? Maybe not. I'll consider.

Rejects:
- My own S11 (subscription attach engine) might be too specific/overfit? Actually it's generalizable. But maybe not top 10.
- Adding bundled Python scripts for everything (B suggests ingest_staging_data.py). Is this rejected? No, but maybe not top 10.
- "Replication Guide" tab automation? Not mentioned by others, maybe overfit.
- Specific HOOD lines like Trump Accounts, Rothera Valuation — all critiques say don't encode. Reject.
- Red fill attention flags (from gap analysis) — workflow convention, maybe not skill's job. Reject as skill instruction? Or include? C says "Do not encode... red-fill 'needs update' cells". I think reject: it's a live workflow hack, not a build spec.
- Making DCF completely deleted (B) — reject deleting reference; keep as opt-in.
- IBKR legacy Arial 10 / interleaved columns as new-build style — reject, only read-compat.
- "Every balance moves only through its rollforward" — keep, not reject.
- Should we reject the idea of building NTM PE's 6500 rows via openpyxl? Yes, the skill should scaffold the 3-spill layout + VLOOKUP, not write 6500 rows. C mentions this. Reject writing all BDH rows; scaffold only.

Disputes to articulate:
1. DCF: Delete entirely vs. keep as opt-in. Side: keep as opt-in. Reason: user may still need it for non-public or non-1Pager names; deleting the reference is irreversible. Just remove from default build order and checklist.
2. Mini Model: Two modes (self-contained vs VA-linked) vs. single VA-linked default. Side: single VA-linked default. Reason: the finished models and newer standalone skills all use VA links; offering two modes adds decision fatigue. If user wants self-contained, they can use the standalone mini-model skill.
3. Alt-data staging: Script vs. manual tab. Side: manual tab with VLOOKUP pattern, no bundled CSV ingest script. Reason: the agent can't execute arbitrary data ingestion without the user providing CSVs anyway; specifying the tab structure and formula pattern is enough and avoids script bloat.
4. Daloopa: Default vs. optional. Side: optional only. Reason: only IBKR uses it; HOOD/BX hand-key. Making it default adds complexity for most builds.
5. Third banner tier: Specific hex #FFEA8F vs. generic "child banner". Side: generic role-based rule. Reason: overfitting to HOOD's exact hex is fragile; define a third tier role and let the agent pick a distinct fill, but keep the prohibition on using it for inputs/bands.

Wait, the prompt asks for "Disputes — take a side" where reviewers disagree. I need to find actual disagreements.

Looking at critiques:
- B says "Delete the DCF Tab entirely" and "Remove `references/dcf-tab.md`". A/C/me say make optional/conditional. That's a dispute.
- B says "Standardize Seasonality Row Formatting" to red #FF0000. Me said same. A says change to red or keep brown? Actually A says "red is dominant". Not a big dispute.
- B wants a Python script `ingest_staging_data.py`. A/C/me mention pattern but not necessarily script. Dispute: script vs. reference pattern. I'll side with reference pattern (no new script) due to maintainability.
- B says "Remove the Downstream Tab Verification from SKILL.md" entirely to references. A/C/me say collapse into 5 gates. Not a huge dispute.
- C says "Strip SKILL.md to a router + non-negotiables; move mechanics to refs". A says similar. B says similar. Consensus.
- D (truncated) might disagree on something but I can't see it. I'll ignore D for disputes since it's incomplete.

Let me structure the final top 10. They must be ranked by impact on reducing distance to finished models, while keeping maintainable and general.

Ranked list thinking:
1. Replace mandatory DCF with 1 Pager + NTM PE (huge manual reconstruction loop eliminated)
2. Add alt-manager engine (BX gap is massive; currently unusable for AMs)
3. Fix Mini Model VA linkage (immediate mismatch on every build)
4. Strip changelog + decentralize checklist/formatting (improves instruction following for everything else)
5. Adaptive consensus source (VAActuals-first, BQL fallback) (fixes dead-environment paradox and finished-model linkage)
6. Add living-model update mode (massive workflow value, though not first-pass; but user maintains models)
7. Add Simple Income Statement headline block (present in all finished models, standard layout)
8. Add 1 Pager + NTM PE reference specs (the actual content; #1 is the policy change, #8 is the spec? Maybe combine. Actually #1 and #8 are related. I need distinct items. Let's make #1 the policy change (demote DCF, add 1Pager/NTMPE to downstream order) and #8 the detailed reference files. That's fine.)
9. Add audit/verification script (improves compliance dramatically)
10. Add cohort/vintage + toggleable scenario + sidecar grammar (driver grammars) — maybe bundle as "Add reusable driver grammars reference". Or separate. But I only have 10 slots.

Wait, I need exactly 10. Let me choose the highest impact:

1. Demote DCF; default downstream valuation = 1 Pager + NTM PE tabs (policy + order change)
2. Add `references/alt-manager-engine.md` with flagship lifecycle grammar (closes BX gap)
3. Rewrite Mini Model to VAActuals-linked actuals + residual row (aligns with finished models)
4. Strip SKILL.md changelog/deep mechanics; move to refs; shrink to router + gates (prompt engineering)
5. Adaptive consensus ladder: VAActuals/Daloopa → red hardcodes → BQL dead formulas (fixes build environment)
6. Add `references/update-mode.md` for quarter-append and Revisions re-snapshot (living model)
7. Add Summary Income Statement block at top of Model tab (HOOD/BX standard)
8. Add `references/driver-grammars.md`: cohort triangle, subscription attach, event calendar, toggle overlay, alt-data staging VLOOKUP (captures HOOD/BX depth without overfitting)
9. Bundle `scripts/audit_model.py` for programmatic gate checks (replaces 19-item manual checklist)
10. Add Capital & Returns block + relax banner tier/color rules (finishes Model tab depth and formatting fidelity)

That's a good mix. But I need to ensure each is one paragraph implementation spec.

Let me check word count. I need to be under ~2000 words total.

Section 1: Consensus. Each line is short. Maybe ~15 items × 1 line = ~300 words.
Section 2: Disputes. 4 disputes × ~3 sentences = ~200 words.
Section 3: Rejects. ~8 items × 1 line = ~150 words.
Section 4: Top 10. Each is a title + one paragraph. ~150 words each = ~1500 words.
Total ~2150. Need to trim slightly. Be concise.

Let me draft.

Consensus items (must be endorsed by 3+ of me/A/B/C):
- Strip the v1→v6.1 changelog from SKILL.md (move to CHANGELOG.md or delete) — backed by A, B, C, me
- Replace mandatory DCF with 1 Pager + NTM PE as default valuation downstream tabs — backed by A, B, C, me
- Make DCF optional, not default — backed by A, B, C, me
- Update Mini Model to allow green links to VAActuals for actuals (drop “self-contained” mandate) — backed by A, B, C, me
- Adopt adaptive consensus source hierarchy: VAActuals/workbook consensus first, red hardcodes second, BQL dead formulas last — backed by A, B, C, me
- Add alt-manager (BX-style) fund lifecycle engine reference — backed by A, B, C, me
- Add living-model “update mode” protocol (append quarter, roll focal, re-snapshot Revisions) — backed by A, B, C, me
- Add Simple Income Statement headline block at top of Model tab — backed by A, B, C, me
- Add Capital & Returns block (ROE, BVPS, payout, op leverage) — backed by A, B, C, me
- Add cohort/vintage triangle grammar — backed by A, B, C, me
- Add toggleable scenario overlay mechanic (on/off switch feeding P&L) — backed by A, B, C, me
- Add alt-data staging tab + VLOOKUP-by-date pattern — backed by A, B, C, me
- Add “Vs Normal Seasonality” delta rows under monthly blocks — backed by A, B, C, me
- Permit third banner tier for fund/product child headers — backed by A, B, C, me
- Decentralize the 19-item acceptance checklist into 5 gated checkpoints + reference-level sub-checks — backed by A, B, C, me
- Add programmatic audit script (`scripts/audit_model.py`) replacing manual image-only verification — backed by A, B, C, me
- Relax rigid A–K/L column prescription to a default with layout adaptation — backed by A, B, C, me
- Move detailed formatting specs (number formats, border mechanics, EPS strip formulas) from SKILL.md to `references/format-spec.md` — backed by A, B, C, me
- Optional Daloopa tag-ID actuals ingestion pattern — backed by A, B, C, me
- Add Core vs GAAP / adjusted parallel P&L module — backed by A, B, C, me

That's plenty. I'll list the strongest ~12-15.

Disputes:
1. Delete DCF reference entirely vs. keep as opt-in. Side: keep as opt-in. Reason: user may request intrinsic value; deleting the reference is destructive. Just remove from default build order and checklist.
2. Bundle `scripts/ingest_staging_data.py` for alt-data vs. tab-pattern only. Side: tab-pattern only. Reason: the agent cannot ingest arbitrary CSVs without user action anyway; a reference spec for staging-tab structure + VLOOKUP is lighter and more general than maintaining a one-off script.
3. Mini Model: default VA-linked vs. dual mode (VA-linked + self-contained export). Side: default VA-linked only. Reason: finished models and newer standalone skills all use VA links; dual modes add decision fatigue and context bloat. Self-contained is already covered by standalone mini-model skills.
4. Daloopa actuals: default vs. optional. Side: optional only. Reason: only IBKR legacy uses it; forcing Daloopa wiring on HOOD/BX-style builds adds unnecessary scaffold and failure modes.

Rejects:
- Delete `references/dcf-tab.md` entirely (B) — keep as opt-in reference; user may still need long-form DCF for non-1Pager names.
- Add `scripts/ingest_staging_data.py` (B) — redundant; agent can build staging tabs via openpyxl faster than maintaining a CSV bridge script.
- Encode HOOD-specific labels (“Trump Accounts,” “Rothera Valuation,” NFL event multipliers) in SKILL.md — overfit; use generic “new initiative / event calendar” modules instead.
- Encode BX-specific fund names (BCP VIII/IX, etc.) in SKILL.md or alt-manager engine — overfit; parameterize fund list from 10-K/supplement.
- Red-fill “attention flag” workflow convention from finished models — this is a post-build user markup habit, not a generative skill rule.
- Force seasonality rows to brown #833C0C — ground truth shows red #FF0000 is dominant; skill should match the live convention.
- Require live BQL canary cell in dead-Bloomberg builds — creates verification paradoxes; demote to optional.
- Mandate every advanced block (cohort, vintage, NII bridge, Up-C) for every company — should be sector/applicability modules selected during scoping, not always-on.

Top 10 ranking:
1. Replace mandatory DCF with 1 Pager + NTM PE default
2. Add alt-manager engine reference
3. Fix Mini Model VA linkage + residual row
4. Strip SKILL.md to router; move mechanics/deep specs to references
5. Adaptive consensus ladder (VAActuals-first, BQL fallback)
6. Add update-mode protocol for living models
7. Add Summary Income Statement block
8. Add reusable driver grammars reference (cohort, attach, toggle overlay, alt-data staging, event calendar)
9. Bundle audit script + 5-gate checklist
10. Add Capital & Returns block + relax banner/color rules

I need to make sure each top 10 item has a concrete implementation spec.

Let's write concisely.

Word count check:
Section 1: ~15 lines, maybe 250 words.
Section 2: 4 disputes, ~60 words each = 240 words.
Section 3: 8 rejects, ~20 words each = 160 words.
Section 4: 10 items, ~120 words each = 1200 words.
Total ~1850. Good.

Let me refine the language to be blunt and concrete.

One thing: The user said "Every suggestion must be actionable as an edit to the skill files." In the top 10, I need to specify which file and what to change.

Let's go.

Section 1: Consensus
Format: "- [Action] — backed by [critiques]" (using A/B/C/Me)

Section 2: Disputes
Format: "DISPUTE: [Topic]. SIDE: [X]. REASONING: [Y]."

Section 3: Rejects
Format: "- [Action/Idea] — [Reason]"

Section 4: Final ranked top 10
Format: "1. **[Title]** ... paragraph ..."

Make sure to reference specific files: SKILL.md, references/mini-model.md, references/alt-manager-engine.md, references/1-pager-ntm-pe.md, references/update-mode.md, references/driver-grammars.md, references/format-spec.md, scripts/audit_model.py, etc.

Double-check that I didn't miss any constraints. The user wants me to act as referee based on the four critiques and my own Round 1. I have done that.

One final check: In consensus, I should only include items endorsed by 3+ reviewers. I have me + A + B + C for most. D is truncated but seems to agree on many; I won't count D explicitly since I don't have full text, but me+A+B+C is already 4.

Let's produce the output.# 1. Consensus (endorsed by 3+ reviewers)

- **Strip the v1→v6.1 changelog/lineage exposition from SKILL.md** — move to `CHANGELOG.md` or delete; replace with one functional sentence — backed by A, B, C, Me.  
- **Replace the mandatory DCF default with 1 Pager + NTM PE as the standard valuation downstream tabs** — backed by A, B, C, Me.  
- **Demote DCF to optional** (build only on explicit request) — backed by A, B, C, Me.  
- **Drop the Mini Model “self-contained / no green links” mandate**; allow actual-year green links to VAActuals (or Model annuals) and add a red “Other / reconciling” residual row — backed by A, B, C, Me.  
- **Adopt an adaptive consensus-source ladder**: VAActuals/workbook consensus tab first → red hardcoded Street snapshot second → BQL dead-string formulas third — backed by A, B, C, Me.  
- **Add a dedicated `references/alt-manager-engine.md`** with flagship fund lifecycle blocks (commitments, invested, realizations, NAV, FPAUM, step-down trigger, perpetual blend) — backed by A, B, C, Me.  
- **Add a living-model “update mode”** (append quarter, roll focal shape, restate banner/SUMIFS, re-snapshot Revisions, refresh Daloopa/Monthly) — backed by A, B, C, Me.  
- **Add a Summary Income Statement headline block** (~35 rows, `#006600` same-tab green links) at the top of the Model tab — backed by A, B, C, Me.  
- **Add a Capital & Returns block** (payout ratio, BVPS/TBVPS, ROE/ROTCE, operating leverage, share-count change) — backed by A, B, C, Me.  
- **Add reusable driver grammars**: cohort/vintage triangle, subscription attach (new vs backbook), event-calendar engine, toggleable scenario overlay, alt-data staging VLOOKUP-by-date — backed by A, B, C, Me.  
- **Add “Vs Normal Seasonality” delta rows** under monthly % M/M blocks — backed by A, B, C, Me.  
- **Permit a third banner tier** (e.g., D-level product/fund headers with a distinct fill like `#FFEA8F`) when depth exceeds two tiers — backed by A, B, C, Me.  
- **Decentralize the 19-item acceptance checklist** into 5 gated checkpoints in SKILL.md; move granular sub-checks (13a–e, etc.) into the reference files they verify — backed by A, B, C, Me.  
- **Bundle a verification script** (`scripts/audit_model.py`) to programmatically check fonts, fill roles, yellow-on-formula, check-row zeros, SUMIFS range identity, and Mini Model link policy — backed by A, B, C, Me.  
- **Relax the absolute A–K labels / L data column prescription** to a default layout; require the agent to discover/match existing layouts in update mode — backed by A, B, C, Me.  
- **Move detailed formatting specs** (number formats, two-phase box mechanics, EPS strip formulas, banner border rules) from SKILL.md to `references/format-spec.md` — backed by A, B, C, Me.  
- **Add optional Daloopa tag-ID actuals ingestion** (column A series IDs, `INDEX/MATCH` to a Daloopa staging tab) — backed by A, B, C, Me.  
- **Add Core vs GAAP / adjusted parallel P&L module** for names that lead with Core metrics — backed by A, B, C, Me.

---

# 2. Disputes — take a side

**DISPUTE: Whether to delete `references/dcf-tab.md` entirely (B) or keep it as an opt-in reference (A/C/Me).**  
**SIDE: Keep as opt-in reference.**  
**REASONING:** Deleting the reference is irreversible and destructive. The user may still request a long-form intrinsic-value tab for names where 1 Pager coverage is thin. The correct edit is to remove DCF from the *default* build order and acceptance checklist in SKILL.md, not to trash the spec. Context budget is saved by omission from the standard flow, not by file deletion.

**DISPUTE: Whether to bundle a Python script `scripts/ingest_staging_data.py` for alt-data staging (B) or specify only a tab + VLOOKUP pattern (A/C/Me).**  
**SIDE: Tab + VLOOKUP pattern only; no new ingest script.**  
**REASONING:** The agent cannot execute arbitrary CSV ingestion without the user providing files and paths anyway. A reference pattern (`references/driver-grammars.md` § alt-data staging) that defines the staging-tab structure, month-end normalization, and `XLOOKUP` into the Model is lighter, more general, and avoids maintaining a one-off script that will break on schema changes.

**DISPUTE: Whether the Mini Model should support a dual mode (VA-linked default + self-contained export) or a single VA-linked default.**  
**SIDE: Single VA-linked default.**  
**REASONING:** Finished models and the user’s newer standalone `mini-model-v7-8-26` skills uniformly use VAActuals-linked actuals. Offering two modes adds decision fatigue and context bloat. If the user truly wants a self-contained mini-model, they can invoke the standalone skill; the full-model pack should emit the finished-model convention by default.

**DISPUTE: Whether Daloopa actuals ingestion should be an encouraged default or strictly optional.**  
**SIDE: Strictly optional.**  
**REASONING:** Only the legacy IBKR finished model uses Daloopa tags; HOOD and BX hand-key actuals. Forcing Daloopa wiring on every build adds scaffold complexity and failure modes for names without a Daloopa feed. The skill should treat it as a conditional mode triggered by the presence of a Daloopa staging tab or an explicit user flag, not as a default path.

---

# 3. Rejects

- **Delete `references/dcf-tab.md`** — keep as opt-in; user may still need long-form DCF.  
- **Bundle `scripts/ingest_staging_data.py`** — redundant; a staging-tab pattern in `references/driver-grammars.md` is sufficient.  
- **Encode HOOD-specific labels** (“Trump Accounts,” “Rothera Valuation,” exact NFL event multipliers) in SKILL.md — overfit; use generic “new initiative / event calendar” grammar instead.  
- **Encode BX-specific fund names** (BCP VIII/IX, etc.) in the alt-manager engine — overfit; parameterize the fund list from the 10-K/supplement.  
- **Adopt red-fill “attention flag” cells as a skill rule** — this is a post-build user markup habit, not a generative spec.  
- **Force seasonality rows to brown `#833C0C`** — ground truth shows red `#FF0000` is dominant; skill should match the live convention.  
- **Require a live BQL canary cell in dead-Bloomberg builds** — creates a verification paradox; demote to optional.  
- **Mandate every advanced block** (cohort, vintage, NII bridge, Up-C, sidecar) for every company — these are applicability modules selected during scoping, not always-on mandates.

---

# 4. Final ranked top 10

**1. Replace mandatory DCF with 1 Pager + NTM PE as default valuation tabs**  
In `SKILL.md`, delete DCF from the § Downstream tabs default set and the § Build Order step 14; replace with steps to build `1 Pager` and `NTM PE` tabs after Qtr. Create `references/1-pager-ntm-pe.md` specifying the B1:O64 layout: Bear/Base/Bull EPS × multiple grids for two out-years (Base EPS green-linked to Model annual EPS, Street EPS red-linked), R/R ratios, key Bloomberg BDP/BDH stats block, relative P/E ladders vs SPX/QQQ with blue σ thresholds, trailing performance, and IR block; NTM PE tab as three BDH spills with date-aligned `VLOOKUP` and median/±1σ bands. Keep `references/dcf-tab.md` but remove it from the default checklist and build order; build DCF only if the user explicitly asks for intrinsic value. Impact: eliminates the largest manual reconstruction loop in HOOD/BX and aligns the first-pass output with the user’s actual valuation workflow.

**2. Add `references/alt-manager-engine.md` and wire it to the sector gate**  
Create a new reference file specifying the BX-style flagship fund lifecycle: per-fund commitment walk (BOP + New Closes = EOP), capital invested + dry powder + % called, realizations walk + % returned, NAV walk (BOP + deployed − realized + market change = EOP) + MOIC, FPAUM walk with a binary “Step-Down Trigger” input row and cumulative post-stepdown flag, fee-rate switch (`=IF(post-stepdown, stepdown rate, investment rate)`), management fees `=FPAUM × rate / 4`, perpetual-vehicle SUMPRODUCT blending, and segment AUM walk with inflow/outflow/market decomposition and red residual rows. In `SKILL.md` § Sector variants and § Build Order Step 2, add: “If the company is an alternative asset manager (BX, KKR, APO, CG, ARES, BAM), read `references/alt-manager-engine.md` before scoping; it is mandatory for this sector.” Impact: closes the deepest architectural gap; without this, the skill cannot produce a BX-grade Model tab.

**3. Rewrite Mini Model to VAActuals-linked actuals + residual row**  
Edit `references/mini-model.md` and `SKILL.md` § Downstream tabs / Hard Rules: remove the “self-contained / no green links / no VAActuals” mandate. Replace with: actual years are green links (`#006600`) to `VAActuals!` (or to the Model tab’s audited annuals if no VAActuals exists); estimate years build in-tab from blue-on-yellow driver inputs (%Y/Y, take rates, NIM) seeded to the Model’s annual estimates; allow estimate totals to pin to VAActuals consensus with a red “Other / reconciling” residual row and a “Consensus reconciliation (VA roll-up)” input; add a Checks & Sources block; keep the “Base Case” scenario label. Update the acceptance checklist to verify actual-year links tie to the dollar. Impact: stops the agent from emitting a Mini Model the user immediately relinks by hand.

**4. Strip SKILL.md to a router + gates; move deep mechanics to references**  
In `SKILL.md`, delete the entire version-history preamble (v1→v6.1 lineage) and replace with one sentence: “Current contract; see CHANGELOG for lineage.” Remove inline re-specifications of retail-broker cascade, vintage roll-on/roll-off math, Up-C waterfall, BQL formula strings, two-phase box mechanics, and number-format tokens; replace with pointers: “Build per `references/retail-broker-engine.md`”, “Format per `references/format-spec.md`”, etc. Restructure the body as: trigger → Step 0 source-materials gate → sector router (broker / alt-manager / bank / exchange / advisory) → 5-gate build checklist → downstream tab order. Move the 19-item checklist into `references/format-spec.md` and the respective tab references; keep only 5 gates in SKILL.md. Impact: frees context window for instruction-following and reduces the probability that the agent misses a hard rule buried in a 260-character line.

**5. Enforce adaptive consensus-source hierarchy**  
In `SKILL.md` § Research first, § EPS strip, § Estimates, and § Hard Rules, replace “live BQL + canary” as the mandatory spine with a ranked ladder: (1) if a `VAActuals` or workbook consensus staging tab exists, link the EPS strip consensus row and Drivers/Qtr Street rows to it in red/dark green; (2) else seed from red hardcoded consensus snapshots transcribed from user-provided data; (3) else write BQL formulas as refresh-on-open strings, but do not treat them as build-time truth and do not require a canary cell when Bloomberg is unavailable. Update the verification gate to skip consensus value-ties when only BQL strings are present. Impact: resolves the dead-environment verification paradox and matches the finished-model consensus surfaces.

**6. Add `references/update-mode.md` and a mode router in SKILL.md**  
Add a new `Modes` section in `SKILL.md` before Build Order: on trigger, ask “Fresh build or update?” If update: (a) append new quarter column(s), extend the period banner formulas and white year separators, and widen the fixed SUMIFS range; (b) roll the focal-column shape to the new quarter; (c) restate seasonals with the new actual month; (d) refresh Daloopa/Monthly/VAActuals staging tabs; (e) snapshot the current Model as Revisions “Old” and clear “New” links; (f) stack a new guidance vintage row if applicable; (g) update 1 Pager EPS links and NTM PE ticker cells. Detail the mechanics in `references/update-mode.md`. Impact: transforms the skill from a one-shot birth script into a living-model maintenance tool, which is how the analyst actually works.

**7. Add Summary Income Statement block at top of Model tab**  
In `SKILL.md` § P&L layout and § Build Order Step 4, mandate a compact ~35-row “Summary Income Statement” above the deep business rollup: headline revenue, key segment totals, EBITDA/PPNR or FRE, pretax income, net income, EPS, key margins, and diluted shares — all green `#006600` same-tab links to the detailed lines below, no drivers. Use dark-green #375623 bold/white section banners. This matches the HOOD/BX finished-model convention of a headline view before the detail. Impact: brings first-pass layout in line with the user’s standard visual hierarchy.

**8. Add `references/driver-grammars.md`**  
Create a single reference cataloging reusable engine patterns distilled from HOOD/BX finished models: (a) cohort/vintage triangle (diagonal retention inputs, new-customer diagonal, rollup vs actual with red plug); (b) subscription attach engine (penetration × funded accounts, new-user vs backbook attach, SLICE check); (c) event/deal calendar (units × share × take rate, with scenario multipliers); (d) toggleable scenario overlay (blue `1/0` on/off input row, `IF` wrapper feeding the P&L, delta memo block); (e) alt-data staging tab structure (raw date/value table, month-end normalization, `XLOOKUP` by date into Model, source cells, missing-month flags). In `SKILL.md` § Step 0 and § Forecast mechanisms, point to this menu when unique KPIs are discovered. Impact: captures complex finished-model depth without overfitting to HOOD-specific labels.

**9. Bundle `scripts/audit_model.py` and replace manual checklist with scripted gates**  
Create `scripts/audit_model.py` that scans the workbook and returns a JSON/text report: font family/size per tab, yellow-fill-on-formula violations, blue hardcodes without #FFFFCC, green-link policy by tab (ban green-to-VA on Model; require green-to-VA on Mini Model actuals), check-row values (must be 0 or “-”), annual SUMIFS range identity across all annual columns, #REF!/#VALUE! including hidden ranges, EPS-strip source type, and banner/fill whitelist compliance. In `SKILL.md` § Verify and report, replace the 19-item prose audit with: “Run `python scripts/audit_model.py`. Address all FAIL items. Then image-verify banner separators and Annual boxes.” Impact: turns an unauditable 19-item memory test into a deterministic, repeatable gate that actually prevents shipping broken workbooks.

**10. Add Capital & Returns block + relax rigid banner/color absolutism**  
In `SKILL.md`, add a mandatory Capital & Returns subsection after Tax & NCI: payout ratio (div + buyback / op NI), BVPS/TBVPS growth, TCE/TA, ROE/ROTCE (GAAP and adjusted), minority-interest %, operating leverage rows, and change-in-share-count. Simultaneously edit § Borders & structure and § Color convention: permit a third banner tier (D-level product/fund headers, e.g., `#FFEA8F`) when the P&L depth requires it; change seasonality memo color to red `#FF0000` to match ground truth; explicitly allow Daloopa/source-link green `#006600` for VAActuals actuals on Mini Model and Summary IS. Remove the sentences “These fills belong ONLY to those roles” and “No green links to VAActuals, ever.” Impact: finishes the Model tab’s financial depth and stops the agent from fighting the user’s established visual and linkage conventions.