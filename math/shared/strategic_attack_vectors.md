# Strategic Attack Vectors — Pre-Phase-2 Notes

**Status:** Author-level strategic notes written before Phase 1 literature surveys complete. To be reconciled with literature findings before launching Phase 2.

These are *priors* — hypotheses about where genuine progress is possible, to be tested against the literature survey output and refined.

---

## Frankl Union-Closed: Where the Slack Is

The post-Gilmer 2022 line of work all uses some variant of:

> If F is union-closed and the most frequent element has frequency ratio < 1/2 - ε, then a careful entropy calculation on a uniform random pair (A, B) ∈ F × F derives a contradiction (or a bound on ε).

The current best constant is ≈ 0.381966 = (3-√5)/2 from Alweiss-Huang-Sellke and refined by Cambie. To verify and pin down: which step in their proof has slack?

### Candidate slack points to test

1. **The "approximately union-closed" relaxation.** Gilmer-style proofs do not use full union-closure of F; they use a weaker probabilistic statement like P(A∪B ∈ F | A,B independent uniform from F) ≥ 1 - δ. This is strictly weaker than union-closure. *Hypothesis: any constant proved by these methods applies to a much larger class than union-closed families, so the true Frankl constant might be strictly larger than what entropy methods can reach. If true, we need a different ingredient — but it also means we should look for a counter-example in the relaxed class to delimit the method.*

2. **The independence assumption on A,B.** The entropy proofs use A and B independent uniform from F. F is not a product distribution under union-closure — there may be a better-tailored coupling (e.g., conditioned on |A| < |B|, or on A ⊆ B, or correlated via some natural Markov chain on F).

3. **The "small element" trick.** Cambie's improvement exploits the existence of a relatively small element. The exact threshold for "small" is tunable. Can we get a sharper bound by optimizing this threshold differently for families with extreme size distribution?

4. **Iteration.** Each entropy bound is one-shot. What if we apply the entropy inequality, derive a sub-family with a better-controlled structure, and iterate? Reimer 2003 (average set size) gives a complementary inequality — combining the two iteratively?

5. **Lattice structure.** F under ⊆ and ∪ forms a join-semilattice. The entropy proofs don't use this. Poonen showed Frankl is equivalent to a statement about finite lattices. There's an entire algebraic structure being ignored — that's slack, possibly the deepest kind.

### Strongest computational experiment to run

Enumerate all union-closed families on [n] for n=5,6 (≈ feasible). For each, compute:
- Empirical abundance
- The "Gilmer slack" — i.e., the difference between (3-√5)/2 and the actual abundance
- Conditional entropy H(A∪B | A, B) divided by H(A) — the ratio Gilmer's method controls

Plot the joint distribution. If a region of the (slack, ratio) plane is unexpectedly empty, that's a structural fact that may enable a sharper inequality.

---

## Collatz: Where the Slack Is

Tao 2019 proved that for any function f(N) → ∞, almost all (in logarithmic density) Collatz orbits starting in [1, N] stay below f(N)·N for all time. This is the closest anyone has gotten to "almost all orbits are bounded."

### Where the gap is

To upgrade Tao's result to the full conjecture, we'd need:
- **(i)** From "logarithmic density 1" → "density 1" → "all".
- **(ii)** From "almost bounded" (≤ f(N)·N) → "bounded" (≤ C·N for some absolute C, or returns to fixed level).
- **(iii)** Bridge from boundedness to convergence (this is the easier step — if orbits return to a bounded set, classical arguments handle the rest).

The deep gap is (ii): Tao's PDE-style argument allows orbits to grow polylogarithmically. Closing this would require a much sharper diffusion estimate, which seems to need fundamentally new analytic tools — i.e., this is the "needs a genius" gap.

### Candidate angles that are more tractable

1. **Computational frontier extension.** Current verification ≈ 2^68 (Barina 2020). With modern GPUs and the right sieve, 2^72 or 2^75 is realistic. Not a proof, but a publishable computational result (Experimental Mathematics or similar).

2. **Stopping-time distribution structure.** Empirical stopping-time distributions look log-normal-ish. Tao's heuristic predicts log τ(n) / log n → constant in some sense. Can we prove tighter moment bounds on τ(n) for n in residue classes?

3. **Syracuse map mod 2^k.** For each k, T^k partitions [1,∞) into 2^k residue classes mod 2^k. The induced map on residues is well-studied but not exhausted. Can we find a non-trivial invariant or Lyapunov function on the 2-adic side?

4. **Cycle exclusion progress.** Steiner ruled out 1-cycles other than {1,2}. Simons-de Weger ruled out m-cycles for m ≤ ~91. Pushing this bound is a concrete, ordinary-math problem; with modern Diophantine techniques (linear forms in logarithms, recent Baker-bound improvements), there's room.

5. **Parity vector / 2-adic measure.** Each n has a parity vector p(n) ∈ {0,1}^∞. The map n → p(n) is well-studied (Lagarias). Conway's FRACTRAN connection shows generalized Collatz is undecidable, but the specific 3n+1 case has more structure. Look for an unused invariant of the parity sequence.

### Strongest computational experiment

For each k ∈ [10, 20], compute T^k for all n ∈ [1, 2^k] mod 2^k. Build the "Syracuse table" τ_k : Z/2^k → Z/2^k. Look for: cycles in the residue map, fixed points, and the distribution of "drift" (n / T^k(n)). Tao's framework predicts drift ≈ (3/4)^k. Does the empirical distribution match? Deviations would be interesting.

### Realistic deliverables

- **Survey paper** (Experimental Mathematics / arXiv math.NT): "The Collatz Conjecture: A Survey and Computational Notes". Includes our 2^72 verification (if achievable) and Syracuse-table observations.
- **Lean 4 formalization** of T's definition, Steiner's 1-cycle result, and Tao's main theorem statement (proof of Tao would be a separate huge project).

---

## Decision Criterion for Phase 3 Lead

After Phase 2:
- If Frankl track produces an entropy-method refinement with a concretely improved constant (even 0.40 instead of 0.38), that's lead-paper material. Realistic.
- If Collatz track produces a verification extension + a clean Syracuse-table observation, that's a solid second paper, not a Collatz proof.

Lead track: most likely Frankl. Backup: Collatz survey-with-computation.

## Open meta-questions

- Should we attempt Lean formalization of *the conjectures themselves* (as `sorry`'d theorems) plus key surrounding lemmas, even without proofs? This is publishable as a Mathlib contribution.
- Should we engage external mathematicians (e.g., post on Tao's blog comments, MathOverflow) to sanity-check any claimed observation before paper submission? Strongly recommend yes.
