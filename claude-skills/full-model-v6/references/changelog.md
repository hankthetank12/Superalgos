# Changelog / lineage (maintainer notes — NOT build instructions)

Nothing in this file changes how a model is built. It exists so the current SKILL.md can stay a
build contract instead of a version history.

- **v6 (this revision — the multi-model-critique edit).** Restructured: SKILL.md became a short
  router/contract; Model-tab mechanics moved to `references/model-engine.md`; all formatting canon
  moved to `references/format-spec.md`. New content, distilled from the analyst's three FINISHED
  workbooks (HOOD, BX, IBKR): the **1 Pager + NTM PE valuation pair** is now the default valuation
  layer and the **DCF is opt-in only**; the **Mini Model flipped to VA-linked actuals** (matching the
  standalone mini-model-v7-x skills); a **consensus-source ladder** replaced the live-BQL mandate
  (fixes the dead-Bloomberg verification paradox); a full **alt-manager fund-lifecycle engine**
  (`references/alt-manager-engine.md`); **reusable driver grammars** (cohort triangle, attach engine,
  event calendar, toggleable overlays, alt-data staging, Vs-Normal seasonals, 2Q stacks); a
  **Summary Income Statement** at the top of the Model tab; a **Capital & Returns** default module;
  an **update mode** for living models; a third banner tier for repeating child blocks; an optional
  **Daloopa actuals-ingestion** pattern; and `scripts/audit_model.py` (static workbook audit).
  Seasonality rows standardized to red italic. The old "No green links to VAActuals, ever" hard rule
  was replaced by the role-based link-color policy in format-spec.md.
- **v5.** Added the mandatory Step 0 source-materials gate: FIRST ask the user for the most recent
  earnings release and investor presentations; mirror management's own presentation; mine them for
  company-only KPIs absent from VAActuals/consensus and build the best as drivers.
- **v4.** Added the Retail Broker engine (`references/retail-broker-engine.md`), distilled from the
  live IBKR / HOOD / BULL builds: five-layer cascade (user funnel → asset ecosystem → per-product
  engines → broker NII stack → expenses/monetization/capital return), monthly-disclosure plumbing,
  canonical broker KPI set, R1–R8 acceptance additions.
- **v3.** Upgraded the Model-tab engine spec to "v6.1" (conventions audited off the live reference
  build: two-tier banners, memo fills, per-unit intensity blocks, market-vs-organic bridge +
  seasoning framework, structured read-across memos, NII refinements, Up-C tax/NCI variant,
  Bloomberg canary + derived period strings, corrected annual-SUMIFS rule) and added the DCF as a
  fifth downstream tab (`references/dcf-tab.md`).
- **v2.** Added the optional Guidance overlay (violet management-guidance rows; fresh-build row
  reservation or `scripts/insert_guidance_rows.py` insertion with workbook-wide reference repair).
- **v1.** Combined the quarterly Model-tab build with four downstream tabs (Mini Model, Revisions,
  Drivers, Qtr) in one pass.
- **Engine-numbering note.** Older SKILL.md text referred to a parallel "v5/v6/v6.1" MODEL-ENGINE
  lineage distinct from the skill's own version number. That numbering is retired; the current
  engine spec simply lives in `references/model-engine.md`.
