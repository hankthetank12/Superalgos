# Claude's own round-1 critique (from direct workbook analysis)

# 1. Weaknesses as a prompt artifact
- **The version-history preamble is dead weight in the hottest context slot.** Lines 10–14 spend
  ~2,500 words narrating v5-vs-v4-vs-v3-vs-v2 lineage plus a parallel "v6/v6.1 engine" numbering that
  collides with the skill's own version number. Zero build value, real confusion risk. Move to a
  `references/changelog.md`; keep a 3-line "what this skill builds" summary.
- **Operative content is buried at the end.** Build order (step list), Hard rules, and the acceptance
  checklist — the things the agent must actually execute — sit after ~200 lines of dense convention
  prose. Restructure SKILL.md as a short workflow spine (research → scope → build steps → audit →
  downstream tabs) that POINTS to conventions, with the deep formatting/engine specs demoted to
  references (`references/formatting.md`, `references/model-engine.md`).
- **Massive redundancy = drift risk.** "Calibri 9pt" is stated ~12 times; the two-phase border write
  3 times; guidance rules 4 times (section, hard rules, checklist, reference). Each restatement is an
  opportunity for future edits to diverge. One canonical statement + pointers.
- **Almost no automation leverage.** Only one bundled script. The spec demands exactly the operations
  LLM agents do worst by hand and redo every build: border sweeps with exclusions, two-phase annual
  boxes, banner year separators, whole-tab font normalization, color-vs-role audit, fixed-range
  SUMIFS verification, zero-error scans, focal shapes. Bundle a `scripts/` toolkit:
  `format_model.py` (apply banners/borders/boxes/fonts/number formats from a row-map JSON) and
  `audit_model.py` (machine-check the acceptance checklist and print a pass/fail report). This both
  raises reliability and lets hundreds of lines of formatting prose shrink to "run the scripts".
- **The Bloomberg mandate contradicts the build environment.** The skill demands live BQL/BDP pulls +
  a canary cell; openpyxl cannot evaluate them, and the finished HOOD/BX models show the user
  replaced strip consensus with VAActuals links or red hardcodes. The skill should define a
  consensus-source policy: VAActuals when present (default), else red hardcoded consensus snapshot
  (values stated in the reply), with BQL formulas written only as clearly-flagged dormant formulas
  the user can activate — never presented as live.

# 2. Content gaps vs the finished models
Highest value first: (a) the 1 Pager + NTM PE valuation pair (in BOTH finished models, with a
user-written Replication Guide tab — they rebuild it every time); (b) Mini Model spec contradicts
the user's current practice (finished mini models are VA-linked green with consensus-pinned totals
and residual rows — the skill's "self-contained, no links, no green" rule is stale vs their
mini-model-v7-8-26 standalone skill); (c) alt-manager fund-level engine (BX builds each flagship
fund's commitments→deployment→realizations→NAV→FPAUM-with-step-down lifecycle and blends perpetual
fee rates by SUMPRODUCT — the skill's asset-manager coverage is one sentence); (d) cohort/vintage
triangle for NNA (HOOD); (e) toggleable thematic upside engines (agentic block with on/off + phase-in)
and new-initiative valuation mini-blocks (Rothera); (f) Seasonals + "Vs Normal" rows on monthly
% M/M / # M/M; (g) subscription attach engine (penetration × funded, new-user vs backbook attach);
(h) Summary/Simple Income Statement at the top of the Model tab (both HOOD and BX); (i) alt-data
staging-tab plumbing (Sensor Tower layout, data-team feed VLOOKUP by month-end date); (j) an
update/maintenance mode — the models are living workbooks and the skill only covers greenfield;
(k) DCF should be optional — neither finished workbook kept one; the 1 Pager/NTM PE pair is the
valuation layer the user actually maintains. Noise/overfit to skip: IBKR legacy Arial-10 formatting,
label typos, `_kpi_ctrl_` rows, interleaved annual columns (legacy layout — acknowledge for reads,
don't build).

# 3. Prioritized suggestions (max 15)
**S1. Build the 1 Pager + NTM PE pair as a standard downstream tab pair** — new
`references/one-pager-ntm-pe.md` encoding the exact B1:O64 layout, the 3 touch-points, Bloomberg
field list, sigma thresholds linked to NTM PE stats; chain after Qtr. HIGH.
**S2. Rewrite `references/mini-model.md` to the VA-linked spec** (green VA links for actual years,
consensus-pinned totals with reconciling residual + blue "Consensus reconciliation" row, in-tab
drivers for estimates, Checks & Sources block, Base Case label). HIGH.
**S3. New `references/alt-manager-engine.md`** — fund-lifecycle blocks, step-down triggers,
perpetual fee-rate SUMPRODUCT stack, segment AUM walk (% of BOP inputs), DE waterfall with
% -to-common; mandatory for alt managers (mirror of the retail-broker gate). HIGH.
**S4. Bundle `scripts/audit_model.py` + `scripts/format_model.py`**; acceptance checklist becomes
machine-checked; formatting prose shrinks. HIGH.
**S5. Consensus-source policy section** (VAActuals-first; dormant BQL; hardcoded red snapshot
fallback with values reported). HIGH.
**S6. Restructure SKILL.md**: workflow spine first; conventions to references; changelog out. HIGH
(reliability) though no new content.
**S7. Cohort-triangle subsection** in retail-broker-engine.md. MED-HIGH.
**S8. Optionality blocks section**: toggleable upside engines (adoption × allocation × activity ×
take rate, phase-in, on/off switch) + new-initiative valuation mini-block + "Cases >>>" scenario
input rows. MED.
**S9. Seasonals + Vs-Normal monthly rows and 2Q-stack rows** added to %-row conventions. MED.
**S10. Summary IS block** at top of Model tab spec. MED.
**S11. Update-mode reference** (`references/update-mode.md`): append quarter, roll focal shapes,
actualize printed quarter, refresh monthlies, re-snapshot Revisions Old, guidance vintages, re-audit.
MED (big real-world value, small text).
**S12. Alt-data staging-tab pattern** (generalize the Bloomberg staging rule to any long-history
feed; VLOOKUP-by-month-end contract; K-tags). MED.
**S13. Subscription attach engine** upgrade in broker ref Layer 5. MED.
**S14. Make the DCF opt-in** ("build when asked or when no 1 Pager exists"). MED.
**S15. Flag-for-follow-up convention** (red fill on inputs awaiting data) + 'Est per Claude' K-tag
for agent-estimated figures. LOW.

# 4. What to remove or simplify
Version narrative (→ changelog); v6/v6.1 engine-numbering; dedupe Calibri/border/guidance
restatements (single source + pointers); collapse the five separate downstream-tab verify lists into
each tab's reference file (SKILL.md keeps one line each); drop the BQL canary as a requirement
(meaningless in a dead-Bloomberg build) in favor of the consensus-source policy.
