# Phase 2 Agent Brief Templates

Templates for the 4 Phase 2 agents. Fill in `{{...}}` from Phase 1 outputs.

---

## A2 — Frankl Theory Agent

> You are doing primary theoretical research on Frankl's union-closed sets conjecture. Authorship: Alex Ye with Claude.
>
> Prior work to build on:
> - Read `/home/user/wikiclaws/math/frankl/literature/survey.md` (do NOT re-survey; build on its findings).
> - Read `/home/user/wikiclaws/math/shared/strategic_attack_vectors.md` for hypothesized slack points.
> - Phase 1 identified the highest-slack step as: **{{HIGHEST_SLACK_STEP}}**.
>
> YOUR TASK: Attempt to tighten {{HIGHEST_SLACK_STEP}} in the current best entropy-method proof (Cambie / Alweiss-Huang-Sellke). Specifically:
> 1. Reproduce the proof in full mathematical detail in `frankl/theory/cambie_proof_explicit.md`. Every inequality justified.
> 2. Identify the *exact* point where slack is introduced (e.g., a Jensen step, a Pinsker bound, a union bound).
> 3. Attempt a sharper inequality at that point. Try at least 3 variations: Rényi entropy, max-entropy, conditional-entropy decomposition, KL-divergence-based.
> 4. For each variant, check it numerically on the small union-closed families enumerated by the experiments track (read from `frankl/experiments/data/baseline.json`).
> 5. If any variant gives a strictly better constant than (3-√5)/2, write it up in `frankl/theory/new_inequality.md` with full proof and computational evidence.
> 6. If all variants fail, write `frankl/theory/dead_ends.md` documenting what was tried and why each failed.
>
> No fabricated math. Every claimed inequality must be proven from scratch in the file.
>
> Report: (1) files written, (2) new constant achieved (or honest "no improvement"), (3) most promising direction still untested.

---

## A3 — Frankl Experiments Agent

> You are running computational experiments on Frankl's conjecture. Authorship: Alex Ye with Claude.
>
> Tools available at `/home/user/wikiclaws/math/frankl/experiments/` (built by infra agent C2). Read its `README.md` first.
>
> YOUR TASK:
> 1. Run `enumerate.py` to get all union-closed families on [n] for n=5 and n=6.
> 2. For each family, compute: max-abundance, Shannon entropy of uniform random A ∈ F, the Gilmer LHS-RHS slack, and the (A∪B) marginal distribution.
> 3. Find the families that achieve abundance closest to 1/2 from above. These are "near-tight" examples — catalog them.
> 4. For each near-tight family, check whether the current best inequality ((3-√5)/2) is tight on it. Where is the gap?
> 5. Generate visualizations: histograms, scatter plots, lattice diagrams of small extremal families.
> 6. Write findings to `frankl/experiments/results.md` with figures in `frankl/experiments/figures/`.
> 7. Output a clean dataset `frankl/experiments/data/extremal_families.json` for the theory agent to use.
>
> Report: (1) results.md path, (2) catalog of extremal families found, (3) any pattern that would suggest a new conjecture (e.g., "all extremal families have property P").

---

## B2 — Collatz Theory Agent

> You are doing theoretical research on the Collatz Conjecture. Authorship: Alex Ye with Claude.
>
> Prior work:
> - Read `/home/user/wikiclaws/math/collatz/literature/survey.md`.
> - Read `/home/user/wikiclaws/math/shared/strategic_attack_vectors.md`.
> - Phase 1 identified the most tractable angle as: **{{MOST_TRACTABLE_COLLATZ_ANGLE}}**.
>
> YOUR TASK: Pick the most tractable angle and pursue it rigorously.
>
> Three options to consider (pick based on Phase 1 findings):
>
> (a) **Cycle exclusion improvement**: Read Steiner 1977 and Simons-de Weger. Use modern linear-forms-in-logarithms bounds (Mignotte, Laurent, Matveev) to improve the m-cycle exclusion bound. Concrete deliverable: cycles of length ≤ {{NEW_BOUND}} ruled out.
>
> (b) **Syracuse map invariant search**: Analyze the induced map T^k mod 2^k for k=10..20. Look for: conservation laws, Lyapunov functions, or structural constraints. Concrete deliverable: a non-trivial invariant or a proof that no polynomial-degree invariant exists below degree D.
>
> (c) **Tao 2019 refinement**: Read Tao's proof. Identify whether the f(N) → ∞ constraint can be sharpened to f(N) = O((log N)^A) or O(1). Even a partial sharpening is publishable.
>
> Write to `collatz/theory/` — proof files in markdown with LaTeX, dead ends documented.
>
> No fabricated math. Each claimed lemma proven in full.

---

## B3 — Collatz Experiments Agent

> You are running computational experiments on Collatz. Authorship: Alex Ye with Claude.
>
> Tools available at `/home/user/wikiclaws/math/collatz/experiments/` (built by C1). Read README first.
>
> YOUR TASK:
> 1. Run verification on [1, 10^9] using `verifier.py`. Record timing and any anomalous trajectories.
> 2. Run `residue_analysis.py` for k=10..20. Save the Syracuse tables.
> 3. Statistical analysis: compute distribution of τ(n)/log n for n ∈ [1, 10^7]. Tao's heuristic predicts this concentrates near a constant. Test empirically; quantify the deviation.
> 4. Search for "long-stopping-time outliers" — n with σ∞(n) > C log n for large C. Catalog them.
> 5. Try to extend verification frontier toward 2^70 using your fastest implementation. If you hit time limits, document the frontier reached.
> 6. Write `collatz/experiments/results.md` with figures.
>
> Report: (1) verification frontier reached, (2) empirical distribution match with Tao's prediction, (3) any anomalous pattern.

---

## Reconciliation Step (before launching Phase 2)

After Phase 1 returns, perform reconciliation:
1. Read all Phase 1 outputs.
2. Update strategic_attack_vectors.md with verified facts (cross out hypotheses that the literature already refutes; promote ones supported by the survey).
3. Fill in the {{...}} placeholders above based on what the literature agents identified.
4. Decide order: launch all 4 Phase 2 agents in parallel (they don't depend on each other).
