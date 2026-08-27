# 1. Weaknesses as a prompt artifact

SKILL.md is a changelog wearing a skill. The first ~40 lines (v5 vs v4 vs v3 vs v2, then “v6 vs v5”, then “v6.1”) are maintainer archaeology. The agent does not need lineage to build a sheet; it needs a current contract. That dump burns the highest-attention tokens and collides names (`full-model-v5` vs engine “v6.1”).

**Equal-weight MUST soup.** Philosophy, Hard rules, and a 19-item checklist (13a–e, 18a) restate the same laws 3× (Calibri 9, two-tier banners, SUMIFS one-range, no green-to-VA, yellow-on-formulas). Agents drop late items. Progressive disclosure is fake: references exist, but SKILL.md still inlines BQL strings, number-format tokens, two-phase box writes, SUMIFS `$X:$BL` patterns, Up-C waterfalls, vintage roll-on math.

**Contradictions the agent cannot resolve:**
- Hard rule: “No green links to VAActuals, ever.” Finished HOOD/BX Mini Models and the user’s newer mini-model skills *require* green VAActuals actuals. Mini-model.md is stale vs the analyst’s current preference.
- Consensus: live `BQL(...)` + canary is mandatory; build env cannot evaluate BQL; finished EPS strips are VAActuals links or red hardcodes.
- DCF is in the same-pass order and checklist 18a; **none of the three finished books have a DCF**. Valuation surface is 1 Pager + NTM PE.
- Scenario memos “never as separate tabs”; finished HOOD has Agentic / EU TAM **tabs that feed drivers**.
- Column grid A–K / data from L is written as law; BX starts data at O; IBKR interleaves annuals.

**Sector routing is a paragraph, not a gate.** Retail broker gets a mandatory 130-line ref. Asset managers get one sentence (“AUM roll-forward × fee rate → FRE”). BX is a different product. Banks/exchanges/advisory are similarly underspecified. The agent will apply the transactional/broker cascade off-sector or emit a generic P&L.

**No “do not build” list.** Every optional overlay (guidance, rate-path, Up-C, vintage, DCF, monthly-in-quarter) reads mandatory unless a tiny “if applies” clause is noticed. Combined with Step 0 + 15-step build order, first-pass overbuilds (DCF, dead BQL, gold banners on everything) and underbuilds (summary IS, fund engines, 1 Pager).

**Verification is theater.** “Border correctness via `getImage`”, 13 downstream checks, wiggle tests — none are scripted except `insert_guidance_rows.py`. The agent will claim the checklist. Missing leverage: a Python auditor (font, fill roles, SUMIFS range identity, check-row ≈ 0, no yellow-on-formula, Mini Model link policy).

**Update mode is absent.** The pack is one-shot. Living books need append-quarter, roll focal, restack seasonals, refresh Daloopa/Monthly, re-snapshot Revisions. The agent has no path except “rebuild.”

# 2. Content gaps vs the finished models

**Close these (high leverage, cross-name):**

1. **1 Pager + NTM PE pair** — identical HOOD/BX layout; user wrote a Replication Guide (ticker + 2 EPS links). This *is* the valuation layer. Automating it closes more “distance to finished” than the unused DCF.
2. **Asset-manager fund lifecycle engine** — BX flagship ~50-row blocks (commitments / invested / dry powder / realizations / NAV / MOIC / FPAUM + binary step-down trigger → fees) plus perpetual SUMPRODUCT and segment AUM walk with red residuals. Without a new `references/alt-manager-engine.md`, AM first-pass is a toy.
3. **Mini Model contract** — flip to: actual years green-link VAActuals (or Model annuals if no VA); estimate *drivers* blue-on-yellow in-tab; estimate *totals* may pin to VA with an Other/reconciling residual; Checks & Sources block. Align SKILL.md + mini-model.md with the user’s v7 mini-model, not v5’s self-contained myth.
4. **Consensus source priority** — VAActuals if present → red Model/Drivers/Qtr/EPS-strip links; else red hardcodes seeded from whatever the user pasted; BQL only as optional formulas that heal on the user’s machine (1 Pager stats, not the Model spine).
5. **Summary Income Statement** at top of Model (HOOD/BX): ~30–40 headline rows, dark-green same-tab links into the deep IS. First-pass currently dumps the user into row 80.
6. **Seasonals vs normal** — `AVERAGE` of prior same-months + “Vs Normal” delta under monthly %M/M / #M/M. This is the nowcast lens; skill only has Seasonality on %Q/Q.
7. **Capital & returns block as a default module** (payout mix, BVPS/TBVPS, ROE/ROTCE, operating leverage, share-count change) — present in HOOD and IBKR, not sector-specific.

**Close these (medium, reusable grammars — not HOOD-only):**
- Cohort/vintage **triangle** grammar (diagonal new units, decay multipliers, roll-up vs actual + plug). HOOD-shaped but applies to any subscriber/account business.
- Attach/penetration engine (new vs backbook, residual).
- Event/deal calendar (units × take × share) as a named pattern, not “World Cup.”
- Toggleable thematic overlay (`on/off` blue row that *does* feed P&L when on) vs purely informational memos. Keep side TAM tabs optional, not every build.
- Alt-data **staging tab + VLOOKUP/XLOOKUP by month-end date** (pattern), not Sensor Tower by name.
- Daloopa INDEX/MATCH via col-A IDs: optional when a Daloopa tab exists; do not replace press-release hardcodes as the default (HOOD/BX still hand-key).
- Third banner tier for repeating child blocks (per-fund / per-product): gold parent, distinct child fill. Don’t overfit BX theme colors; specify a role.
- Core vs GAAP parallel P&L: only when the company leads with “Core.” IBKR-specific as a named variant, not default.

**Do not encode (overfit / noise):** Agentic/EU TAM tab contents; PE/RE fundraising research dumps; Trump Accounts / IPO Access lines; IBKR Arial 10 and interleaved annuals (read-compat only); red-fill “needs update” cells; user’s typos; Alt-1/Alt-2 EPS columns unless a rate-path scenario is in scope; DCF as default.

**Inferred, not in the gap file:**
- History depth / forecast horizon (how many printed quarters, how many estimate quarters, annual block start year) is unspecified → agents guess.
- Focal quarter/year selection rule is implicit.
- VAActuals line-mapping procedure (semantic match + unmatched list) exists for Guidance but not for consensus KPIs.
- Units: AUM $bn vs P&L $mm, and the no-bare-scaler rule needs an AM example.
- “What the first pass may omit” (thematic side tabs, fundraising research, NTM PE’s 6,500 BDH rows if Bloomberg dead — scaffold the 3-spill layout + VLOOKUP, leave spills to refresh on open).

# 3. Prioritized suggestions (max 15)

**S1. Strip SKILL.md to a router + non-negotiables; move mechanics to refs** — Keep: trigger, Step 0, sector gate, 10-line philosophy, build order (short), source-priority, “do not build,” pointer list. Move: BQL strings, number formats, border/box/SUMIFS recipes, Up-C, vintage math, EPS-strip cell formulas → `references/model-engine.md`. Impact **HIGH**. Effort low; risk: missed pointers — add an explicit “read X before step N” table.

**S2. New `references/one-pager-ntm-pe.md` + clone script** — Spec the B1:O64 1 Pager (Bear/Base/Bull EPS×multiple, Model-green vs Street-red EPS, R/R, BDP/BDH key stats, relative P/E vs SPX/QQQ with blue σ thresholds, trailing performance, IR block) and NTM PE (3 BDH spills, date-align VLOOKUP, median/±1σ). Script: copy layout, write ticker + 2 EPS link cells. Build **after Model audit, instead of DCF**. Impact **HIGH**. Effort med; Bloomberg formulas dead at build — document “heal on open,” don’t fake values.

**S3. Make DCF opt-in; default valuation = 1 Pager + NTM PE** — SKILL.md Downstream + build order 14 + checklist 18a: DCF only if user asks. Impact **HIGH** (stops wasted 60-line tab). Effort low.

**S4. New `references/alt-manager-engine.md`; sector gate like retail-broker** — Flagship lifecycle, perpetual SUMPRODUCT, segment AUM walk, FRE = FPAUM × rate/4, PRE realization engine, red residuals in actuals, binary step-down. Mandatory read for alt managers (BX, KKR, APO, CG, ARES, BAM). Impact **HIGH**. Effort high; risk of BX-overfit — parameterize fund list from the 10-K/supplement, don’t hardcode BCP IX.

**S5. Fix Mini Model to VA-linked actuals** — Rewrite mini-model.md + SKILL.md Downstream/checklist 15: green VAActuals (or Model annuals if no VA); no “self-contained” ban; residual row; Checks & Sources. Impact **HIGH**. Effort low. Reverse the green-to-VA ban **for Mini Model actuals only**; keep Model-tab actuals as blue hardcodes (or Daloopa pulls).

**S6. Consensus source ladder in SKILL.md (one box)** — (1) VAActuals/visible consensus tab → red links; (2) else hardcoded red Street seeded by user/paste; (3) BQL optional, never the only spine. EPS strip follows (1)/(2). Delete “must be live BQL” from checklist 8. Impact **HIGH**. Effort low.

**S7. Summary IS module in model-engine.md** — First 30–40 rows: Revenues / key KPI / PPNR or FRE / NI / EPS, `#006600` same-tab links, then the deep P&L. Impact **MED-HIGH**. Effort low.

**S8. `references/update-mode.md`** — Append quarter column, extend banner/SUMIFS/year separators, roll focal shape, recompute seasonals, refresh Daloopa/Monthly, freeze Revisions Old snapshot, stack guidance vintage. Trigger phrases: “update the model”, “roll 2Q”. Impact **MED-HIGH** on living books, not first-pass. Effort med.

**S9. Add reusable driver grammars (short ref `driver-grammars.md`)** — (a) cohort triangle, (b) attach new/backbook, (c) event calendar, (d) on/off thematic overlay that feeds P&L, (e) monthly staging VLOOKUP-by-date, (f) vs-normal seasonals, (g) 2Q stack for young products. Point Step 0 “unique KPIs” at this menu. Impact **MED**. Effort med; keeps HOOD patterns without HOOD names.

**S10. Capital & returns + BS-in-estimates as default closing modules** — Payout %, BVPS, ROE, op leverage, share roll; estimate BS: assets scaled to a driven balance, liabilities plug, equity roll. Impact **MED**. Effort med.

**S11. Column map as default, not law** — “Default labels B–K, data from L; freeze after label block. If an existing book differs, match it.” Mention interleaved-annual only as read-compat. Impact **MED** for BX/IBKR overlays. Effort low.

**S12. Optional Daloopa wiring when tab exists** — Col A series IDs; actuals `INDEX/MATCH`; K-tag source. Else press-release hardcodes. Impact **MED** for IBKR-like names. Effort med. Don’t make it default.

**S13. Bundled `scripts/audit_model.py`** — Font family/size, fill-role whitelist, yellow-on-formula, blue-on-formula, SUMIFS range identity, check rows, Mini Model forbidden/allowed refs, EPS-strip source type. Agent must run it at the Model gate. Impact **MED** on compliance. Effort med.

**S14. Third banner tier + guidance color lock** — Major #375623 @B, sub #FFF2CC @C, repeating child (fund/product) a third fill @D (pick one hex, e.g. #FFEA8F). Guidance only #7030A0 italic; never reuse violet for MoM calcs. Seasonality: pick **red italic** (matches HOOD majority) or brown — not both. Impact **LOW-MED**. Effort low.

**S15. History/horizon + focal rules** — Default: ≥12 printed quarters if available, ≥8 estimate quarters, annuals from first full FY displayed; focal = next unreported quarter / its FY. Impact **MED** on layout match. Effort low.

# 4. What to remove or simplify

- **Delete the entire version-lineage preamble** (v5 vs v4 … v6.1). One line: “Current contract. Older notes live in git.”
- **Collapse Hard rules ∩ checklist ∩ Color section.** Keep Color once in model-engine.md; SKILL.md checklist = 8 gates (research, ties, wiggle, audit script pass, sector engine, downstream present, source ladder, reply contents). Kill 13a–e as separate boxes; fold into sector refs.
- **Remove mandatory DCF** from When-to-use, Downstream, build order, checklist 18a. Keep `dcf-tab.md` for opt-in.
- **Remove live-BQL-as-spine** (canary, derived FPR, exact BQL blob) from SKILL.md. Park in 1 Pager ref as optional.
- **Remove “Mini Model self-contained / no Model! / no VAActuals!”** everywhere.
- **Remove “scenario memos never as separate tabs.”** Replace: informational memos on Model; material TAM/what-ifs may be a side tab that links to one blue driver.
- **Don’t restate retail-broker five-layer cascade in SKILL.md** — one sentence + “read the ref.” Same for guidance overlay (pointer + “reserve rows before freeze”).
- **Drop Calibri-9 as a SKILL.md hard rule repeated 6×** — once in engine ref + audit script. Don’t fight IBKR Arial on legacy reads.
- **Do not add** Sensor Tower/Relay/Citadel tab names, BX fund names, or Agentic formulas into SKILL.md.

Net: SKILL.md should shrink toward ~120–150 lines of routing and gates; new refs for AM, 1 Pager/NTM PE, driver grammars, update-mode; DCF demoted; Mini Model and consensus ladder aligned to the finished books. That is the only way first-pass moves without making the pack un-followable.