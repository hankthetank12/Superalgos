#!/usr/bin/env python3
"""Two-round multi-model critique/debate of the full-model-v5 skill via OpenRouter.

Round 1: each model independently critiques the skill given the full SKILL.md, a digest of its
reference files, and the ground-truth gap analysis vs the user's three finished models.
Round 2: each model sees the other models' anonymized round-1 critiques and debates them,
producing a refereed final top-10 list.

Usage: OPENROUTER_API_KEY=... python3 run_debate.py [round1|round2|all]
Outputs: debate/out/round1_<slug>.md, debate/out/round2_<slug>.md (+ .json raw)
"""
import json, os, sys, time, pathlib, urllib.request, urllib.error

BASE = pathlib.Path(__file__).resolve().parent
OUT = BASE / "out"
OUT.mkdir(exist_ok=True)

API_KEY = os.environ.get("OPENROUTER_API_KEY", "").strip()
if not API_KEY:
    kf = BASE / "key.txt"
    if kf.exists():
        API_KEY = kf.read_text().strip()
if not API_KEY:
    sys.exit("No OPENROUTER_API_KEY found (env or debate/key.txt)")

MODELS = [
    ("openai/gpt-5.5", "gpt55"),
    ("google/gemini-3.1-pro-preview", "gemini31pro"),
    ("x-ai/grok-4.6", "grok46"),
    ("deepseek/deepseek-v3.2", "deepseekv32"),
    ("moonshotai/kimi-k2.6", "kimik26"),
]

SKILL = (pathlib.Path("/root/.claude/skills/synced/full-model-v5/SKILL.md")).read_text()
DIGEST = (BASE / "reference_digest.md").read_text()
GAPS = (BASE.parent / "analysis" / "GAP_ANALYSIS.md").read_text()

SYSTEM = (
    "You are an expert reviewer with two specialties: (1) prompt/skill engineering for LLM coding "
    "agents (you know how long instruction files degrade instruction-following, how to structure "
    "progressive disclosure, and what makes agents actually comply), and (2) institutional buyside "
    "equity-research financial modeling in Excel (driver-based quarterly earnings models, Street "
    "formatting conventions, consensus workflows). Be blunt, specific, and concrete. No flattery, "
    "no generic advice. Every suggestion must be actionable as an edit to the skill files."
)

CONTEXT = f"""## CONTEXT

A buyside analyst uses a Claude Code "skill" (a markdown instruction pack: SKILL.md always loaded on
trigger, plus 7 reference .md files loaded on demand, plus 1 python helper script) to build full
institutional quarterly earnings models in Excel (via openpyxl / an Office-JS bridge — NOT a human
driving Excel; Bloomberg formulas cannot evaluate in the build environment). The skill builds a deep
"Model" tab plus five downstream tabs (Mini Model, Revisions, Drivers, Qtr, DCF).

The analyst then manually extends the generated workbook until it reaches its "finished" state. They
provided three FINISHED models (HOOD/Robinhood, BX/Blackstone, IBKR/Interactive Brokers legacy) as
ground truth for what they actually want. An exhaustive structural analysis of those workbooks vs the
skill is given below as "GROUND-TRUTH GAP ANALYSIS" — treat it as reliable evidence extracted
programmatically from the real files.

The goal of this review: propose how to edit the skill so its FIRST-PASS output lands as close as
possible to the finished models, while keeping the skill maintainable and general across sectors
(brokers, exchanges, banks, asset managers, advisory) — not overfit to these three companies.

Constraints to respect:
- SKILL.md is ~278 lines but extremely dense (~74KB); total pack ~1,100 lines. There is a real
  instruction-following cost to bloat; progressive disclosure via reference files is the escape valve.
- The agent building the model cannot evaluate Bloomberg BQL/BDP/BDH at build time (formulas can be
  written but return nothing until the user opens the file with the add-in).
- The user keeps versioned skills (v1..v5); this edit produces the next iteration of full-model-v5.
"""

R1_TASK = """## YOUR TASK (Round 1 — independent critique)

Produce a critique with EXACTLY these markdown sections:

# 1. Weaknesses as a prompt artifact
The skill as an instruction pack for an LLM agent: structure, length, redundancy, ambiguity,
contradictions, misplaced content (things in SKILL.md that belong in references or vice versa),
instruction-following risks, missing verification/automation leverage (bundled scripts etc.).

# 2. Content gaps vs the finished models
Work through the gap analysis: which gaps are the highest-value to close, which are noise or
overfit to one company. Add anything you infer is missing that the gap analysis didn't call out.

# 3. Prioritized suggestions (max 15)
Each: **S<n>. <title>** — what to change, where (SKILL.md section / which reference file / new
reference file / new script), expected impact (HIGH/MED/LOW) on "distance to finished model",
and effort/risk. Order by impact.

# 4. What to remove or simplify
Concrete deletions/simplifications with rationale.

Keep the whole response under ~2500 words. Be specific enough that an engineer could implement
each suggestion without asking follow-ups.
"""

def call(model, messages, max_tokens=9000, temperature=0.4, retries=4):
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://claude.ai/code",
            "X-Title": "skill-critique-debate",
        },
    )
    delay = 5
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                data = json.loads(r.read().decode())
            if "error" in data and data.get("error"):
                raise RuntimeError(str(data["error"])[:500])
            msg = data["choices"][0]["message"]
            content = msg.get("content") or ""
            if isinstance(content, list):  # some providers return parts
                content = "".join(p.get("text", "") for p in content)
            if not content.strip():
                raise RuntimeError("empty content")
            return content, data
        except Exception as e:
            print(f"  [{model}] attempt {attempt+1} failed: {e}", flush=True)
            if attempt == retries - 1:
                raise
            time.sleep(delay)
            delay *= 2

def round1():
    user = (
        CONTEXT
        + "\n\n## THE SKILL (SKILL.md, verbatim)\n\n```markdown\n" + SKILL + "\n```\n\n"
        + "## DIGEST OF THE 7 REFERENCE FILES\n\n" + DIGEST + "\n\n"
        + "## GROUND-TRUTH GAP ANALYSIS (from the three finished workbooks)\n\n" + GAPS + "\n\n"
        + R1_TASK
    )
    msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]
    for model, slug in MODELS:
        outf = OUT / f"round1_{slug}.md"
        if outf.exists() and outf.stat().st_size > 500:
            print(f"skip {slug} (exists)")
            continue
        print(f"ROUND 1: {model} ...", flush=True)
        t0 = time.time()
        content, raw = call(model, msgs)
        outf.write_text(content)
        (OUT / f"round1_{slug}.json").write_text(json.dumps(raw.get("usage", {}), indent=1))
        print(f"  done {len(content)} chars in {time.time()-t0:.0f}s", flush=True)

def round2():
    crits = {}
    for model, slug in MODELS:
        f = OUT / f"round1_{slug}.md"
        if f.exists():
            crits[slug] = f.read_text()
    letters = "ABCDEFG"
    for model, slug in MODELS:
        outf = OUT / f"round2_{slug}.md"
        if outf.exists() and outf.stat().st_size > 500:
            print(f"skip {slug} (exists)")
            continue
        others = [(s, t) for s, t in crits.items() if s != slug]
        blocks = []
        for i, (s, t) in enumerate(others):
            blocks.append(f"### Critique {letters[i]}\n\n{t}")
        user = (
            CONTEXT
            + "\n\n## THE SKILL (SKILL.md, verbatim)\n\n```markdown\n" + SKILL + "\n```\n\n"
            + "## GROUND-TRUTH GAP ANALYSIS\n\n" + GAPS + "\n\n"
            + "## YOUR OWN ROUND-1 CRITIQUE\n\n" + crits.get(slug, "(none)") + "\n\n"
            + "## FOUR OTHER REVIEWERS' CRITIQUES (anonymized)\n\n" + "\n\n---\n\n".join(blocks)
            + "\n\n## YOUR TASK (Round 2 — debate & referee)\n\n"
            "Now act as the debate referee. Produce EXACTLY these sections:\n\n"
            "# 1. Consensus (endorsed by 3+ reviewers)\nList each consensus recommendation in one "
            "line with which critiques back it.\n\n# 2. Disputes — take a side\nFor each point where "
            "reviewers disagree (or where you disagree with a popular idea), state the disagreement "
            "and argue a side with concrete reasoning grounded in the constraints (context budget, "
            "agent instruction-following, no live Bloomberg, generality across sectors).\n\n"
            "# 3. Rejects\nIdeas from any critique (including your own) that should NOT be adopted — "
            "overfit, bloat, redundant, or wrong — with one-line reasons.\n\n"
            "# 4. Final ranked top 10\nYour final ranked list of the 10 edits that most reduce the "
            "distance between the skill's first-pass output and the finished models. Each: title, "
            "one-paragraph implementation spec (which file, what text/structure changes), impact.\n\n"
            "Under ~2000 words."
        )
        msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]
        print(f"ROUND 2: {model} ...", flush=True)
        t0 = time.time()
        content, raw = call(model, msgs)
        outf.write_text(content)
        (OUT / f"round2_{slug}.json").write_text(json.dumps(raw.get("usage", {}), indent=1))
        print(f"  done {len(content)} chars in {time.time()-t0:.0f}s", flush=True)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("round1", "all"):
        round1()
    if mode in ("round2", "all"):
        round2()
    print("DONE")
