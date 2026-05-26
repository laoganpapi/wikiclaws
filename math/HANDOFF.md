# Handoff — Collatz & Frankl Research Project

**Last session date:** 2026-05-26
**Branch:** `claude/epic-dirac-p1oQo` (repo: laoganpapi/wikiclaws)
**User:** laoganpapi@gmail.com
**Status:** Planning complete, agents NOT yet launched. User is moving to a new working directory.

---

## What this project is

Multi-agent research effort to make serious progress on two famous unsolved problems, with the end goal of a publishable paper:

1. **Collatz Conjecture** (3n+1) — every positive integer eventually reaches 1 under iteration of n→n/2 if even, n→3n+1 if odd.
2. **Frankl's Union-Closed Sets Conjecture** — for any finite union-closed family (other than {∅}), some element appears in at least half the sets.

User's directive: "we're gonna do it and you have to have the confidence and belief that we'll eventually get there." Heavy compute budget (many agents, multi-day). Both problems run in parallel; whichever makes more progress before resources run out becomes the lead deliverable.

## Realistic framing (do not lose this)

These problems have resisted decades of effort. The realistic best-case output of agentic work is:
- A high-quality survey-with-experiments paper
- Possibly a minor partial result (e.g., pushing Frankl's entropy constant past current ~0.38)
- Identification of new attack vectors

The user understands this and still wants to push. Do not over-promise "we proved it" — verify any proof claims rigorously via a red-team agent.

## State of the art (anchors)

**Frankl:**
- Gilmer 2022 (arXiv:2211.09055): first constant via entropy (~0.01)
- Sawin, Chase-Lovett, Alweiss-Huang-Sellke, Cambie: improved to ≈ (3-√5)/2 ≈ 0.38
- Frontier: push toward 0.5. This is the live, tractable angle.

**Collatz:**
- Lagarias survey (canonical reference)
- Terras 1976: density results
- Tao 2019 (arXiv:1909.03562): "Almost all Collatz orbits attain almost bounded values" — logarithmic density via PDE-style heuristics
- Computational verification ≈ 2^68
- Frontier: closing the gap from "almost all almost-bounded" → "all bounded"

## File layout already created

```
/home/user/wikiclaws/math/
├── MASTER_PLAN.md          # Full strategic plan (read this first)
├── HANDOFF.md              # This file
├── collatz/
│   ├── literature/         # (empty) survey output goes here
│   ├── experiments/        # (empty) computational work
│   ├── theory/             # (empty) theoretical analysis
│   └── paper/              # (empty) draft paper sections
├── frankl/
│   ├── literature/
│   ├── experiments/
│   ├── theory/
│   └── paper/
└── shared/                 # cross-cutting bibliography, notation
```

NOTE: The repo root (`/home/user/wikiclaws/`) contains an unrelated legal-analysis project (00_*.md through 25_*.md). Do not touch those files — the math project is isolated under `math/`.

## Phase plan (from MASTER_PLAN.md)

**Phase 1 — Foundation (NOT yet started):**
- Agent A1: Frankl literature survey → `frankl/literature/`
- Agent B1: Collatz literature survey → `collatz/literature/`
- Agent S0: Shared bibliography & notation → `shared/`

**Phase 2 — Investigation:**
- A2 Frankl theory, A3 Frankl experiments
- B2 Collatz theory, B3 Collatz experiments

**Phase 3 — Synthesis:** A4 / B4 paper drafts + cross-pollination agent X

**Phase 4 — Adversarial:** red-team for errors/prior art; Lean 4 verifier for key lemmas

## How to resume (concrete next steps)

1. `cd /home/user/wikiclaws/math && cat MASTER_PLAN.md` to refresh.
2. Launch Phase 1 agents in **parallel** (single message, 3 Agent tool calls). Suggested briefs:

   **A1 (Frankl literature)** — general-purpose agent:
   > Survey the union-closed sets conjecture (Frankl). Trace the entropy-method line: Gilmer 2022 → Sawin → Chase-Lovett → Alweiss-Huang-Sellke → Cambie → any 2024-2025 work. For each paper: extract the technique, the constant achieved, and the bottleneck that prevents pushing further. Write to `/home/user/wikiclaws/math/frankl/literature/survey.md`. Also create `/home/user/wikiclaws/math/frankl/literature/bibliography.bib`. Identify which step in the current best proof has the most slack — that's where future work should attack.

   **B1 (Collatz literature)** — general-purpose agent:
   > Survey the Collatz conjecture. Anchor on Lagarias's annotated bibliography, then Terras 1976, Tao 2019 ("Almost all Collatz orbits…"), and 2024-2025 work. Catalog approaches by family: ergodic/statistical, 2-adic / automaton, dynamical, computational verification. For each: best known result, key obstruction. Write to `/home/user/wikiclaws/math/collatz/literature/survey.md` and `bibliography.bib`. Identify the gap between Tao's "almost all, almost bounded" and the full conjecture — what would need to change?

   **S0 (Shared infra)** — general-purpose agent:
   > Set up `/home/user/wikiclaws/math/shared/`: create `notation.md` (standard notations for both problems), `paper_targets.md` (candidate journals/arXiv categories — likely math.CO for Frankl, math.NT or math.DS for Collatz), and `ai_collaboration_norms.md` documenting how AI-assisted math results should be disclosed in publications (cite norms from recent AlphaProof, FunSearch papers).

3. After Phase 1 returns, review outputs, then launch Phase 2 (theory + experiments, four parallel agents).

4. Commit after each phase with descriptive messages. Push to `claude/epic-dirac-p1oQo`. Open a draft PR once Phase 1 lands.

## Important constraints

- Branch must remain `claude/epic-dirac-p1oQo`.
- All work under `/home/user/wikiclaws/math/` — do NOT modify the legal-analysis files in repo root.
- AI-only proofs of these conjectures are extremely unlikely. Verifier/red-team passes are mandatory before any "we proved X" claim.
- Agents must write concrete artifacts (markdown + code + data), not vague summaries.
- Negative results go in `dead_ends.md` per track — they're valuable.
- Honesty discipline: if no real progress, the deliverable is a strong survey, not an inflated proof claim.

## User communication style preference

- Direct, no excess hedging once a plan is set
- The user pushed back when I was overly cautious; commit to the plan, but verify rigorously
- Short status updates between phases, not running narration

## Open questions to confirm with user on resume

- Target venue / arXiv category preference (math.CO and math.NT are defaults)
- Whether to attempt Lean 4 formalization in Phase 4 (compute-expensive, high signal)
- Authorship line — currently assumed: human author, AI-assisted methodology disclosed
