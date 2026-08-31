# 1. Weaknesses as a prompt artifact

The skill is overstuffed. SKILL.md is trying to be the router, the style guide, the sector taxonomy, the Excel-build spec, the audit checklist, the downstream-tab spec, and the changelog. That is why compliance will degrade. The model-builder agent will miss important rules because every rule is marked mandatory.

Specific prompt problems:

- **The opening changelog is poison.** The first ~1,500 words are lineage/version history. It burns context and attention before the agent gets operational instructions. Move almost all of it to `references/version-history.md` or delete it.
- **Too many “mandatory” rules compete.** Step 0, retail broker reading, Calibri 9, annual SUMIFS, BQL canary, DCF, guidance overlay, two-tier banners, all downstream tabs, etc. are all framed as hard gates. The agent cannot prioritize. Finished-model gaps show some “mandatory” rules are actually wrong for the user, especially DCF and Mini Model self-contained actuals.
- **Consensus-source logic contradicts real workflow.** SKILL.md says BQL canary/live pulls are core. Finished models use VAActuals links/hardcodes because Bloomberg cannot evaluate in build. This is not a cosmetic mismatch; it affects EPS strip, Drivers, Qtr, Mini Model, 1 Pager, and update workflow.
- **Mini Model spec is stale versus user preference.** The skill mandates no Model/VAActuals links. Ground truth says the newer preference is VAActuals-linked actuals and sometimes consensus-pinned totals with residual rows. The full-model pack is behind the standalone mini-model lineage.
- **DCF is overweighted and likely wrong as default.** DCF is absent from all finished models. The actual valuation surface is 1 Pager + NTM PE. Building DCF every time consumes agent effort and workbook complexity while moving away from finished state.
- **Sector depth is lopsided.** Retail broker is detailed. Asset manager is basically a sentence in SKILL.md despite BX being one of the most important finished models. There is no alt-manager flagship fund lifecycle grammar.
- **Too much formatting minutiae is in SKILL.md.** Number formats, border mechanics, EPS strip, annual boxes, fills, and banner rules should be consolidated into a `formatting-and-audit.md` reference plus a helper script. Right now repeated formatting rules bloat the main file and still require the agent to implement fragile openpyxl behavior manually.
- **Verification is prose-only where scripts should enforce.** There should be scripts for: formula scan by color/fill role, annual SUMIFS range consistency, yellow-on-formula detection, Model-reference scan on Mini Model, font scan, check-row scan, # error scan including hidden ranges, and banner/annual-box border checks as far as openpyxl can inspect. The skill relies on “verify by image” too heavily.
- **Build modes are missing.** The finished workbooks are living models. The skill only describes fresh build. There is no mode for quarterly roll-forward, monthly update, guidance refresh, Revisions snapshot, focal quarter roll, or appending periods.
- **Column-layout rigidity will break compatibility.** SKILL.md hard-codes A–K labels / L data. Finished models vary materially. The skill should define a default layout and a discovery/adaptation layer, not an absolute.
- **Scenario guidance is internally inconsistent with finished models.** SKILL.md says scenarios are informational and never feed the P&L. HOOD uses toggleable thematic overlays that can feed/bridge to modeled drivers. The skill is forbidding something the user actually builds.
- **Reference-file loading is underused.** SKILL.md contains deep details for retail broker, DCF, Qtr, formatting, guidance, etc., even though references exist. The main file should be a short decision tree plus build checklist. Sector engine specifics should be loaded only after sector selection.
- **Acceptance checklist is too long to be useful.** 20 numbered items with subitems becomes noise. Split into: build gates, model-tab audit, downstream-tab audit, optional-module audit. Put detailed checks in scripts/reference files.

# 2. Content gaps vs the finished models

Highest-value gaps to close:

1. **1 Pager + NTM PE tabs.** These appear in HOOD and BX with consistent layout and a replication guide. They are more central than DCF. Add them as default valuation outputs, or at minimum default-on when user asks for “full model.”
2. **Consensus-source hierarchy.** Prefer workbook-native VAActuals/consensus surfaces when present; allow red hardcoded consensus snapshots; use Bloomberg formulas as refresh-on-open formulas, not build-time truth. This affects first-pass usefulness immediately.
3. **Mini Model actuals/linking convention.** Finished models want VAActuals-linked actuals and consensus-pinned estimate totals with residual/reconciliation rows in some cases. The current “self-contained/no green anywhere” rule is contrary to ground truth.
4. **Alt-manager / fund lifecycle engine.** BX’s finished model is far beyond “AUM × fee rate.” Need a dedicated `asset-manager-engine.md` with flagship fund blocks, perpetual vehicles, FPAUM step-down triggers, NAV/fundraising/capital-called/realization walks, FRE/PRE/carry bridges, and fundraising research tabs.
5. **Alt-data staging tabs and VLOOKUP-by-date plumbing.** The skill mentions alt-data memos but not real staging tabs: Sensor Tower, Relay Data, Citadel Monthly Index. Finished models use data-team feeds as model inputs, not just memos.
6. **Thematic/sidecar what-if tabs.** Agentic impact and EU TAM are not simple scenario memos. They are sidecar driver engines with optional feed/toggle into the Model. The skill needs a pattern for “sidecar tab supports driver.”
7. **Daloopa actuals ingestion.** IBKR legacy uses Daloopa tag IDs and INDEX/MATCH pulls. Even if HOOD/BX hand-key actuals, this is a high-value update workflow feature. Add optional Daloopa mode instead of banning actual links.
8. **Update mode.** Monthly updates, quarter append, focal roll, guidance vintage stacking, Revisions snapshot, NTM PE refresh, and red attention flags are essential to living models.
9. **Same-tab simple summary IS.** BX/HOOD open with Summary/Simple Income Statement. The skill jumps directly into a deep Model. Add a compact linked summary at top as default.
10. **Core vs GAAP / adjusted parallel P&L.** IBKR and HOOD/BX isolate core/adjusted metrics, one-timers, sec lending, TRA, restructuring, etc. Current adjusted-bridge language is too generic.
11. **Capital/returns depth.** Finished models have payout, ROE/ROTCE, BVPS/TBVPS, TCE/TA, minority interest %, operating leverage, share-count changes. Skill mentions some, but not as a required capital/returns module.
12. **Cohort/vintage triangle.** HOOD cohort analysis is a real triangular engine, not a memo. Add a generic cohort engine for account/customer/subscriber businesses.
13. **Seasonality diagnostics.** Finished HOOD has “Vs Normal Seasonality” and 2Q stack rows. These are useful and general for young/high-growth products.
14. **Third banner tier.** BX uses fund/product-level headers beneath sub-sections. Current two-tier rule is too rigid for fund-heavy models.
15. **Attention-flag cells.** Red fills mark cells needing update. This is a workflow convention the skill lacks.

Noise / likely overfit:

- IBKR legacy Arial 10 and interleaved annual columns should be compatibility-read only, not new-build style.
- Typos/label messiness in finished models should not be replicated.
- Specific HOOD novelty lines like “Trump Accounts,” “Rothera Valuation,” and exact NFL event structure should become generic “new initiative / event calendar / optional valuation stub” modules, not hardcoded examples.
- BX-specific named funds should be examples inside an alt-manager engine, not embedded in SKILL.md.

# 3. Prioritized suggestions (max 15)

**S1. Replace mandatory DCF default with 1 Pager + NTM PE default valuation package**  
Where: SKILL.md `Downstream tabs`, `Build order`, `Final acceptance`; new `references/one-pager.md`, `references/ntm-pe.md`.  
Change: Build order becomes Model → Mini Model → Revisions → Drivers → Qtr → **1 Pager → NTM PE**; DCF becomes optional when user asks for intrinsic/DCF. Specify B1:O64 1 Pager layout, bear/base/bull EPS × multiple grids for two out-years, key BDP/BDH stats, relative valuation bands fed by NTM PE, IR block.  
Impact: HIGH. Effort/risk: MED; mostly templating plus Bloomberg formulas that refresh later.

**S2. Rewrite consensus-source hierarchy around VAActuals/workbook surfaces first**  
Where: SKILL.md `Data & consensus sources`, `EPS strip`, `Estimates`, `Downstream tabs`, `Hard rules`; references for Drivers/Qtr/Mini.  
Change: Source priority: (1) VAActuals / workbook consensus tab, (2) existing Drivers consensus staging, (3) red hardcoded consensus snapshot, (4) BQL formulas refresh-on-open. BQL canary optional, not gate. EPS strip may be red VAActuals links/hardcodes.  
Impact: HIGH. Effort/risk: LOW.

**S3. Update Mini Model reference to current user convention**  
Where: `references/mini-model.md`, SKILL.md downstream/acceptance.  
Change: Replace “self-contained/no green/no VAActuals” with two modes: default **VA-linked actuals + in-tab drivers**; optional self-contained export mode. Allow consensus-pinned totals, “Other/reconciling” residual, “Consensus reconciliation (VA roll-up)” row, Checks & Sources block, Base Case label.  
Impact: HIGH. Effort/risk: MED due to reversal of hard rule.

**S4. Add full alt-manager engine**  
Where: new `references/asset-manager-engine.md`; SKILL.md `Sector variants`, `Build order`.  
Change: Mandatory for BX-like asset managers. Include flagship fund lifecycle blocks: commitments walk, closes, capital invested, dry powder, % called, realizations, NAV, market change residual, MOIC, FPAUM, step-down trigger binary, cumulative post-stepdown flag, fee-rate switch. Add perpetual vehicles, segment AUM walk, FRE/PRE/performance fee/carry bridge, fundraising research tabs.  
Impact: HIGH. Effort/risk: HIGH but necessary.

**S5. Add living-model update mode**  
Where: SKILL.md new `Modes` section; new `references/update-mode.md`; optional script.  
Change: At trigger, ask fresh build vs update. Update tasks: append quarter/month, roll period banner/focal shapes, refresh Daloopa/Monthly/VAActuals, stack guidance vintage, roll Revisions Old/New snapshot, update 1 Pager EPS links, refresh NTM PE formulas, rerun checks.  
Impact: HIGH. Effort/risk: MED.

**S6. Add optional Daloopa actuals ingestion mode**  
Where: SKILL.md `Actuals must tie`; new `references/daloopa-actuals.md`.  
Change: Allow column A Daloopa tag IDs and actual formulas from `Daloopa` staging via INDEX/MATCH. Actual formula cells should use designated source-link green/dark-green, with hardcoded blue fallback where missing. Keep tie checks to press release.  
Impact: MED/HIGH. Effort/risk: MED; conflicts with current “blue hardcodes only” rule must be explicitly resolved.

**S7. Add Summary Income Statement at top of Model tab**  
Where: SKILL.md `P&L layout`, `Build order`; formatting reference.  
Change: Reserve a compact 30–40 row Summary/Simple IS above the detailed model: revenues, expenses, EBITDA/PTI/NI/EPS, key margins, core/adjusted lines, shares. Green links to deep Model lines; no drivers.  
Impact: HIGH. Effort/risk: LOW/MED.

**S8. Add alt-data staging-tab pattern**  
Where: new `references/alt-data-staging.md`; SKILL.md `Market-data tracking`, `Memo blocks`.  
Change: Define staging tabs for Sensor Tower/Relay/internal feeds: raw date/value table, month-end normalization, VLOOKUP/XLOOKUP by month-end into Model, source/date cells, data-team citation, missing-month flags. Distinguish “memo only” vs “feeds driver.”  
Impact: MED/HIGH. Effort/risk: MED.

**S9. Add sidecar what-if tab pattern with optional driver feed/toggle**  
Where: new `references/sidecar-whatif-tabs.md`; SKILL.md `Scenario memos`.  
Change: Allow separate tabs for thematic TAM/agentic/international expansion/event opportunities. Require clear “Feeds Model?” toggle, on/off row in Model, base-case off unless user instructs, check row showing included vs excluded EPS impact.  
Impact: MED/HIGH. Effort/risk: MED.

**S10. Add cohort/vintage triangle engine**  
Where: new section in `retail-broker-engine.md` or new `references/cohort-engine.md`.  
Change: One row per cohort, diagonal new customers, retention/decay assumptions, cohort contribution roll-up, calculated vs actual KPI, plug, modeled vs consensus rows. Use for accounts, subscribers, AUM cohorts, product adoption.  
Impact: MED. Effort/risk: MED.

**S11. Add core-vs-GAAP / adjusted parallel P&L module**  
Where: SKILL.md `P&L layout`; new `references/core-adjusted-bridge.md`.  
Change: Require separate GAAP, adjusted, and core rows where company reports them; isolate sec lending, marks, TRA, restructuring, currency diversification, NCI/tax differences. Add core PPNR/core EPS if relevant.  
Impact: MED. Effort/risk: MED.

**S12. Strengthen capital/returns module**  
Where: SKILL.md `Per-share discipline`, `Rollforwards`; new `references/capital-returns.md`.  
Change: Add payout ratios, BVPS/TBVPS, ROE/ROTCE, TCE/TA, minority-interest %, operating leverage/YTD op leverage, share-count change, buyback/dividend sensitivity. Mandatory for brokers/banks/asset managers.  
Impact: MED. Effort/risk: LOW/MED.

**S13. Make layout adaptive, not fixed**  
Where: SKILL.md `Sheet grid & header scaffold`; new `references/layout-discovery.md`.  
Change: Define default B:K labels / L data, but allow B:N/O and legacy E-data layouts. Require named variables: `label_start_col`, `source_tag_col`, `first_period_col`, `annual_start_col`. Downstream tabs consume map, not hard-coded columns.  
Impact: MED. Effort/risk: MED.

**S14. Add verification scripts**  
Where: new `scripts/audit_workbook.py`; SKILL.md `Verify and report`.  
Change: Script checks fonts, yellow formulas, blue estimate hardcodes without fill, green/VAActuals references by mode, # errors including hidden columns, check rows nonzero, annual SUMIFS range consistency, Mini Model reference policy, Qtr hidden AE:AG, workbook links. Output JSON/text report.  
Impact: MED/HIGH. Effort/risk: MED.

**S15. Move detailed formatting into one reference and shrink SKILL.md**  
Where: new `references/formatting-and-audit.md`; edit SKILL.md.  
Change: SKILL.md keeps only top 20 formatting invariants. Move number formats, border mechanics, EPS strip minutiae, annual boxes, color table, banner specs, image-check instructions to reference.  
Impact: MED for compliance. Effort/risk: LOW.

# 4. What to remove or simplify

- **Delete the long version-history/changelog from SKILL.md.** Keep three bullets: “v5 requires source materials,” “retail broker reference mandatory,” “downstream tabs built after Model audit.” Move lineage to reference or omit.
- **Stop making DCF mandatory.** Change to optional module. Finished models do not use it; mandatory DCF increases distance to desired workbook.
- **Remove “Mini Model must be self-contained/no green/no VAActuals” as the default hard rule.** Replace with mode-specific rules. Current rule directly conflicts with finished models.
- **Demote BQL canary and live BQL consensus from hard requirement.** Keep formulas where useful, but do not make dead Bloomberg formulas the canonical seed source.
- **Collapse repeated formatting rules.** Period banner, Calibri, annual SUMIFS, annual boxes, #FFFFCC inputs, and two/three-tier banners should be stated once in SKILL.md and fully specified in `formatting-and-audit.md`.
- **Simplify acceptance checklist.** Replace the 20-item wall with four gates:
  1. Research/source-material gate.
  2. Model-tab financial/audit gate.
  3. Optional-sector module gate.
  4. Downstream/valuation tabs gate.  
  Put subchecks in references/scripts.
- **Remove absolute column assumptions from hard rules.** Use named layout variables. Keep default layout only.
- **Relax “scenario memos never feed P&L.”** Replace with: “inline scenario memos do not feed P&L; sidecar what-if modules may feed via explicit on/off toggle and inclusion bridge.”
- **Do not encode one-off HOOD/BX labels in SKILL.md.** Keep specific examples inside sector references only.
- **Remove “No green links to VAActuals, ever” as universal law.** Replace with source-role color policy: press-release hardcodes blue; VAActuals/consensus links red or dark green depending tab/mode; Model engine links green; actual-link mode permitted with source tags and tie checks.
- **Do not require every possible advanced block for every company.** Per-unit, market-vs-organic, Up-C, roll-on/off, NII bridge, cohort, sidecar, alt-data should be sector/applicability modules selected during scoping, not always-on mandates.