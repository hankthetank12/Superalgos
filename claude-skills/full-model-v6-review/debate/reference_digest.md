# Digest of the skill's 7 bundled reference files (loaded on demand by the agent)

- **retail-broker-engine.md** (~130 lines): mandatory for retail brokers. Five-layer cascade: (1) user
  funnel & funded-account rollforward (alt-data download memos, registered users, funded accounts with
  full %/# stacks, funded-customer roll BOP+new+resurrected+acquired−churned, MAU/engagement, ARPU,
  average-accounts denominator); (2) customer-asset ecosystem (market-vs-organic bridge, NNA %
  annualized, asset rollforward, assets-per-account, credit-balance splits); (3) per-product
  transaction engines (industry pool → market share → company volumes → per-account intensity →
  read-across memos → take rate → revenue; product table for equities/options/crypto/prediction
  markets/commission-DARTs; event-calendar builds; contra-rev memos); (4) broker NII stack (BB live
  rates block with the standard ticker set, balances as % of assets, rate-sensitive split, yields as %
  of benchmark / CTD betas, sec lending, NIM calc vs reported, presentation bridge, rate-sensitivity
  ladder); (5) expenses (brokerage expense as % of options+equities revenue — never %Y/Y; marketing
  alt-data lead; comp = headcount × comp/employee; adj-vs-GAAP opex bridge; RIF memos), other revs
  (subscription, fee stack, other-rev plug), adjusted-earnings bridges, share roll, returns block,
  Up-C/NCI, customer-driven balance sheet. Monthly plumbing: monthly-in-quarter rows (default) or a
  dedicated Monthly tab with INDEX/MATCH pulls. Canonical broker KPI set. R1–R8 acceptance checklist.
- **mini-model.md** (~130 lines): the Mini Model tab is SELF-CONTAINED — actual years are blue
  hardcodes transcribed from the Model's audited annuals, estimates build in-tab from blue driver
  inputs seeded to the Model, all % rows computed in-tab, NO links to Model or VAActuals (red
  consensus memo rows are the only cross-tab reference), no green anywhere, focal-year shape,
  wiggle test.
- **revisions-tab.md** (~115 lines): Old (frozen blue snapshot) / New (green links) / Chg (black, red
  if negative) per period; hidden "From Model" staging block far right; conditional formatting on Chg;
  Calibri 9pt override.
- **drivers-tab.md** (~165 lines): 8-row KPI blocks (Value green on #F2F2F2 / %Y/Y / %Q/Q / Street red
  / Street %Y/Y / %Q/Q / Vs Street / spacer); consensus source priority (VAActuals if present, else
  BQL/BDP staging); annual basis typed by metric (SUM flows, 4Q stocks, AVERAGE averages); one-sided
  metrics; label-swap handling; top border only on true sum rows; focal-period box shapes.
- **qtr-model-vs-street.md** (~225 lines): GS-format Qtr tab, ~9 history quarters + focal quarter as
  Model/Street/Actual + variance columns + hidden FY block (AE:AG); column-B banners; continuous
  #FFFFCC band on the Actual column with font carrying meaning; blank-Street IF guards; /100 on VA
  ratios; FY bases typed by line type; no focal shape; detailed verify list.
- **dcf-tab.md** (~60 lines): hedge-fund DCF (no WACC/perpetuity): actual/Model years green-linked,
  ~10 forecast years from blue inputs, channel-pool/TAM foundation with named competitors,
  per-stream earnings engines, stream-specific FCF conversion (FCF-yield or dividend+BV-reinvest
  roll), per-stream exit-multiple TVs, NPV → implied price → upside, NPV-allocation/market-implied-
  multiple back-solve, #FBE2D5 section boxes, #DAE9F8 terminal multiples.
- **guidance-overlay.md** (~75 lines) + scripts/insert_guidance_rows.py: read a "Guidance" tab
  adaptively, match items to P&L lines semantically, reserve violet #7030A0 italic "Mgmt Guidance"
  rows during skeleton build (fresh build) or insert with the bundled reference-repairing script
  (existing model); period-aligned verbatim strings; excluded from border sweeps; unmatched items
  reported.
