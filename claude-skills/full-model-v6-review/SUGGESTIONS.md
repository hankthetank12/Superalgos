# full-model-v6 — Multi-model critique: final suggestion list

**Process.** The full SKILL.md + reference digest + a programmatic gap analysis of the three finished
workbooks (HOOD, BX, IBKR) were sent to five frontier models via OpenRouter — GPT-5.5,
Gemini 3.1 Pro, Grok 4.6, DeepSeek V3.2, Kimi K2.6 — for independent critiques (round 1), then each
model refereed the other four critiques (round 2: consensus / disputes / rejects / final top-10).
Claude's own critique ran alongside. Raw transcripts are in `review/debate/`.

## Unanimous consensus (all 5 models + Claude)

1. **Default valuation layer is wrong.** All three finished workbooks carry a **1 Pager (risk/reward)
   + NTM PE** pair — none kept the DCF the skill builds every time. HOOD even contains a
   hand-written "Replication Guide" tab for copying the pair between models. → Build 1 Pager + NTM PE
   by default (new `references/one-pager-ntm-pe.md`); demote the DCF to opt-in (keep `dcf-tab.md`,
   stop loading it unless asked).
2. **The Mini Model spec contradicts the user's own current standard.** Finished mini models
   green-link actual years to VAActuals (`#006600`), pin some estimate totals to consensus with an
   "Other / reconciling" residual, and carry a "Consensus reconciliation (VA roll-up)" input row and
   a Checks & Sources block — exactly like the standalone mini-model-v7-x skills. The full-model
   pack's "SELF-CONTAINED, no links, no green ever" rule is stale. → Rewrite `mini-model.md`; delete
   the "No green links to VAActuals, ever" hard rule (replace with a role-based link-color policy).
3. **The live-Bloomberg mandate creates a verification paradox.** BQL/BDP cannot evaluate in the
   build environment; the skill still demands live consensus pulls + a canary and "ties to the cent".
   The agent can only hallucinate that check. Finished EPS strips are VAActuals links or red
   hardcodes. → Consensus-source ladder: (1) VAActuals/consensus tab → red links; (2) red hardcoded
   consensus snapshot; (3) BQL written only as clearly-flagged refresh-on-open formulas (1 Pager /
   NTM PE), never the Model's spine, never a verification source. Canary dropped as a gate.
4. **Asset managers are catastrophically under-specified.** BX's finished Model builds each flagship
   fund's lifecycle (~50 rows/fund: commitments walk → capital invested/dry powder/% called →
   realizations → NAV walk with market residual → MOIC → FPAUM with a binary step-down trigger →
   fees = FPAUM × rate/4), perpetual vehicles blended by SUMPRODUCT, and a segment AUM walk with
   %-of-BOP inputs. The skill's coverage was one sentence. → New `references/alt-manager-engine.md`,
   gated exactly like the retail-broker reference (mandatory for BX/KKR/APO/ARES/CG/BAM-type names).
5. **SKILL.md is a changelog wearing a skill.** ~2,500 words of v1→v6.1 lineage occupy the
   highest-attention context; rules repeat 3–4× (body / Hard rules / checklist); deep mechanics
   (BQL strings, border recipes, Up-C math) sit inline while references go underused; the 19-item
   checklist exceeds working memory. → Restructure: SKILL.md becomes a ~150-line router
   (modes → Step 0 gate → sector router → source ladder → build order with a read-X-before-step-N
   table → 5 verification gates); mechanics move to `references/model-engine.md` +
   `references/format-spec.md`; lineage moves to `references/changelog.md`.
6. **A Summary Income Statement belongs at the top of the Model tab.** Both HOOD and BX open with a
   ~30–40-row headline IS (dark-green #006600 same-tab links into the deep P&L). → Add to the P&L
   layout spec and build order.
7. **The skill only knows how to be born, not how to live.** The finished workbooks are maintained:
   quarters appended, focal shapes rolled, monthlies refreshed, Revisions re-snapshotted, guidance
   vintages stacked. → New `references/update-mode.md` + a fresh-vs-update fork at the top.

## Strong majority (4–5 backers)

8. **Reusable driver grammars** (new `references/driver-grammars.md`), distilled generically — no
   HOOD/BX names: (a) cohort/vintage triangle (vintage rows × decay-multiplier diagonal, new-unit
   diagonal, roll-up vs actual with plug); (b) subscription/attach engine (penetration × units,
   new-user vs backbook attach with residual); (c) event/deal calendar (units × per-event activity ×
   share × take rate); (d) **toggleable thematic overlay** — a blue on/off (1/0) row + phase-in ramp
   that feeds the live P&L when switched on (legalizing HOOD's agentic-uplift pattern; replaces the
   blanket "scenarios never feed the P&L" ban, which stays true for inline memos only);
   (e) new-initiative valuation stub (revs × multiple × haircuts × ownership → per-share value);
   (f) alt-data staging tab + XLOOKUP-by-month-end plumbing (generalizing Sensor Tower/Relay);
   (g) Seasonals + "Vs Normal Seasonality" delta rows under monthly % M/M / # M/M blocks;
   (h) 2Q-stack rows for young products where Y/Y is meaningless.
9. **Capital & Returns as a default closing module** — payout ratios (div/buyback/total % of op NI),
   BVPS/TBVPS + growth, ROE/ROTCE (GAAP + adjusted), TCE/TA, minority-interest %, operating-leverage
   rows, change-in-share-count — plus the estimate-column balance sheet recipe (driven asset scale,
   liability plug, equity roll).
10. **Adaptive column layout.** Default stays labels→K / data from L, but expressed as named
    variables (label_end_col, first_data_col) discovered per workbook — BX runs B–N/O, legacy IBKR
    interleaves annual columns (read-compat only). Stops the agent from smashing existing books.
11. **Scripted audit over prose theater.** New `scripts/audit_model.py` doing the checks openpyxl can
    do deterministically (fonts, fill-role violations, yellow-on-formula, blue-formula collisions,
    SUMIFS range identity, link-policy per tab, error cells incl. hidden Qtr columns) with a
    report-don't-loop contract; the 19-item checklist collapses to 5 gates, tab-specific checks move
    into each tab's reference. (Gemini dissented on script brittleness — resolved by scoping the
    script to static checks only and keeping image checks for borders/shapes.)
12. **Third banner tier + color-role cleanup.** Repeating child blocks (per-fund, per-product) get a
    third banner tier (#FFEA8F at D) — BX/HOOD both needed it; seasonality rows standardize on red
    italic (HOOD majority); #7030A0 stays guidance-only; the "fills belong ONLY to those roles"
    absolutism is relaxed to defined roles.
13. **Optional Daloopa actuals ingestion.** When a Daloopa tab exists (IBKR pattern): column-A series
    IDs + INDEX/MATCH actuals with blue-hardcode fallback and source K-tags. Strictly opt-in — HOOD/BX
    still hand-key, and IDs can't be guessed.

## Disputes and how they were resolved

- **Delete `dcf-tab.md` vs opt-in** (Gemini wanted deletion): keep the file, remove from default
  flow — 4-to-1.
- **Dual-mode Mini Model** (GPT-5.5 wanted a self-contained "export mode" too): single VA-linked
  default — dual modes are a classification trap; the standalone mini-model skills cover the rest.
- **Audit script vs prose gates** (Gemini: scripts brittle → infinite loops): adopted with scope
  limits — static checks only, never value-evaluation; report failures, don't block in a loop.
- **Bundled CSV-ingest script** (Gemini/DeepSeek wanted `ingest_staging_data.py`): rejected — the
  staging PATTERN goes in driver-grammars; a generic ingest script breaks on schema variance.
- **Red-fill "needs update" attention flags**: one line in format-spec as an optional convention
  (not a SKILL.md rule) — agents would otherwise paint random cells red.
- **Core-vs-GAAP parallel P&L** (IBKR pattern): applicability-gated paragraph in model-engine.md,
  only when the company leads with a "Core"/adjusted presentation.
- **Sidecar what-if tabs** (Agentic/EU TAM): optional grammar, default off; inline toggle rows are
  the standard mechanism.

## Unanimous rejects (won't implement)

- Encoding HOOD/BX specifics (Trump Accounts, Rothera, NFL calendar contents, BCP IX fund names,
  Sensor Tower/Relay/Citadel tab names) into SKILL.md — grammars only.
- Adopting IBKR's legacy Arial-10 / interleaved-annual layout for new builds (read-compat only).
- Replicating the finished models' typos/label noise.
- Keeping live-BQL EPS-strip ties as a verification gate.
- Building every advanced module on every model (Up-C, vintage roll, rate-path, cohort, etc. stay
  applicability-gated).

## Implementation map (applied in this edit)

| # | Change | Files |
|---|--------|-------|
| 1 | SKILL.md → ~150-line router; lineage out; 5 gates; read-before-step table | `SKILL.md`, `references/changelog.md` |
| 2 | Model-tab mechanics consolidated (all v5 content preserved, plus Summary IS, Capital & Returns, estimate BS, consensus ladder, Daloopa option, adaptive layout) | `references/model-engine.md` |
| 3 | Formatting/color/border/number-format canon (single source; 3-tier banners; link-color roles; seasonality red; audit workflow) | `references/format-spec.md` |
| 4 | Alt-manager fund-lifecycle engine (BX-grade), sector-gated | `references/alt-manager-engine.md` |
| 5 | 1 Pager + NTM PE valuation pair (default; replaces DCF in the flow) | `references/one-pager-ntm-pe.md` |
| 6 | Reusable driver grammars (cohort triangle, attach, event calendar, on/off overlay, staging, Vs-Normal seasonals, 2Q stack, initiative stub) | `references/driver-grammars.md` |
| 7 | Living-model update mode | `references/update-mode.md` |
| 8 | Mini Model rewritten to VA-linked convention | `references/mini-model.md` |
| 9 | Static audit script (report-don't-loop) | `scripts/audit_model.py` |
| 10 | DCF marked opt-in | `references/dcf-tab.md` (header note), SKILL.md |
| — | Unchanged: retail-broker-engine.md (+cohort/attach pointer), revisions-tab.md, drivers-tab.md, qtr-model-vs-street.md, guidance-overlay.md, insert_guidance_rows.py | |
