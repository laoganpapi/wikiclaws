# Open Problems in the Collatz Conjecture

**Compiled by:** Alex Ye with Claude (June 2026)
**Companion to:** `survey.md`, `bibliography.bib`

This document enumerates concrete open subproblems extracted from the Collatz literature, organized by approach family and rated for **(D)** difficulty (1 = tractable in months, 5 = an open conjecture in its own right) and **(P)** payoff toward the full conjecture (1 = incremental, 5 = would close it).

We deliberately list subproblems that are concretely formulated and that, in our judgment, are *false-flag-able* — i.e., it is possible to write down what success would look like.

---

## A. Density / statistical (Family 1, 6)

### A.1 Upgrade Tao 2022 from logarithmic density to natural density.
- **Statement.** Prove that, for any $f \to \infty$, $\#\{N \le X : \mathrm{Col}_{\min}(N) > f(N)\} = o(X)$ — i.e., natural density of the failure set is $0$.
- **What is known.** Tao 2022 gives this in logarithmic density. The expected approach is via a fine-scale mixing result for the Syracuse Markov chain.
- **D = 4, P = 3.** Closing this is widely expected to be technically deep but achievable, building directly on Tao's framework. Does *not* close the conjecture but is the most important next step.

### A.2 Prove the "$\beta = 1$" equidistribution.
- **Statement.** Define $c_n := \inf_{3 \nmid b} \mathbb{P}(\mathrm{Syrac}(\mathbb{Z}/3^n\mathbb{Z}) = b)$. Prove $c_n \ge 3^{-n - o(n)}$.
- **What is known.** Tao 2020 (blog) proves submultiplicativity $c_{n_1 + n_2 - 1} \ge c_{n_1} c_{n_2}$. The "$\beta = 1$" lower bound is conjectural.
- **D = 4, P = 4.** Would yield preimage density $x^{1-o(1)}$ — quantitatively much stronger than Krasikov–Lagarias $x^{0.84}$.

### A.3 Improve the Krasikov–Lagarias exponent $\gamma > 0.84$.
- **Statement.** Refine the difference-inequality LP to push $\gamma$ closer to $1$.
- **What is known.** Stalled at $0.84$ since 2003. Best lower-bound proof in the family.
- **D = 3, P = 1.** Marginal payoff but tractable.

### A.4 Total stopping time bound.
- **Statement.** Prove $\sigma_\infty(N) = O(\log N)$ for almost all (natural density) $N$.
- **What is known.** Lagarias–Weiss 1992 predicts $\sigma_\infty(N) \approx \gamma_{LW} \log N$ with $\gamma_{LW} = 2/\log(4/3) \approx 6.95$, heuristically. No unconditional theorem matches this.
- **D = 4, P = 2.** Hard but moves the field toward quantitative control.

---

## B. 2-adic / 3-adic structure (Family 2)

### B.1 Construct a Lyapunov function on $\mathbb{N}$ realized via 2-adic restriction.
- **Statement.** Find $V : \mathbb{Z}_2 \to \mathbb{R}_{\ge 0}$ continuous such that
  $V(\Phi(\sigma(x))) \le V(\Phi(x)) - \epsilon$
  for all $x \in \Phi^{-1}(\mathbb{N})$ and some $\epsilon > 0$, except on a sparse set.
- **What is known.** Akin 2004 frames this. No candidate $V$ has been proposed that distinguishes $\mathbb{N}$ from $\mathbb{Z}_2 \setminus \mathbb{N}$ in a useful way.
- **D = 5, P = 5.** A success would close the conjecture; the difficulty is in distinguishing $\mathbb{N}$ from a 2-adic measure-zero set.

### B.2 Refine Bernstein–Lagarias mod-$2^n$ permutation structure.
- **Statement.** The map $\Phi$ descends to a permutation $\Phi_n$ of $\mathbb{Z}/2^n\mathbb{Z}$ of order $\sim 2^{n-4}$. Identify nontrivial $\Phi_n$-invariant subsets containing arithmetic-progression cosets — these constrain the Collatz dynamics on small residue classes.
- **D = 3, P = 2.** Tractable but unclear how it helps.

---

## C. Computational verification (Family 3)

### C.1 Verify the conjecture to $2^{N}$ for $N \ge 72$.
- **Statement.** Extend Barina 2025's $2^{71}$ bound. Each doubling roughly requires $\sim 1$ year of supercomputer time at current GPU throughput.
- **D = 2, P = 1.** Almost entirely an engineering task. Improves cycle-exclusion bounds (Eliahou 1993, Hercher 2023) marginally.

### C.2 Verify "no nontrivial cycle of total length $\le L$ exists" for $L \ge 10^{8}$.
- **Statement.** Currently Eliahou 1993 gives $L \ge 1.7 \times 10^7$ for the period. Combine direct simulation with continued-fraction sharpening to push beyond this.
- **D = 2, P = 1.** Tractable; useful for cycle exclusion.

### C.3 Statistical fit of Lagarias–Weiss heuristic to high-$N$ trajectories.
- **Statement.** Compute the empirical distribution of $\sigma_\infty(N) / \log N$ for $N$ near $2^{60}, 2^{65}, 2^{70}$ and fit deviations from the predicted $\gamma_{LW}$. This may guide which Lyapunov functions (Problem B.1) are plausible.
- **D = 1, P = 1–3.** Cheap, immediately informative.

### C.4 GPU-accelerated path-record search.
- **Statement.** Find new path-record-holders (orbits achieving exceptional excursions). These provide data for the random-walk model and for the Lyapunov question.
- **D = 1, P = 1.** Continuing Roosendaal's program.

---

## D. Cycle exclusion (Family 4)

### D.1 Extend Hercher 2023 to $m \le M$ for larger $M$.
- **Statement.** Hercher 2023 proves no nontrivial $m$-cycle for $1 \le m \le 91$. Push to $m \le 200, 500, \ldots$.
- **What is known.** Each extension requires a better effective irrationality measure of $\log_2 3$.
- **D = 3, P = 2.** Tractable in principle; requires Diophantine-approximation expertise.

### D.2 Improve effective irrationality measure of $\log_2 3$.
- **Statement.** Sharpen the bound $|\log_2 3 - p/q| > C/q^\mu$ for some $\mu < 5$ unconditional.
- **What is known.** Baker-type bounds give $\mu \approx 5.something$ effective; conjecturally $\mu = 2 + \epsilon$.
- **D = 5, P = 2.** Hard external problem. Improvements feed directly into cycle exclusion (D.1).

### D.3 Rule out divergent orbits unconditionally.
- **Statement.** Prove that no $n$ has $T^k(n) \to \infty$.
- **What is known.** Modulo the conjecture itself, no direct proof exists. Lagarias–Weiss random-walk heuristic predicts no divergence (it gives drift $\to -\infty$).
- **D = 5, P = 4.** Combined with cycle exclusion would close the conjecture. Often considered "the deeper half".

### D.4 Characterize cycles via the Wirsching/Goodwin representation.
- **Statement.** Use the 1998 Wirsching framework of predecessor sets to constrain which residue classes can host a cycle.
- **D = 3, P = 2.**

---

## E. Generalizations & undecidability (Family 5)

### E.1 Identify the boundary of decidability for "Conway-style" Collatz maps.
- **Statement.** Conway 1972 and Kurtz–Simon 2007 prove undecidability for the generalized family. Identify a sub-family containing the classical $T$ for which the orbit-reachability problem is decidable.
- **D = 4, P = 3.** Theoretical computer science angle.

### E.2 FRACTRAN-style obstructions to "pure" $3x+1$.
- **Statement.** Show that the specific arithmetic of $T(n) = n/2$ or $(3n+1)/2$ is *not* obtainable as a FRACTRAN halting question; reduce $T$'s halting question to a simpler sub-problem.
- **D = 4, P = 3.** Speculative; would clarify why classical $T$ might be decidable.

### E.3 Quantitative bounds for the generalized Collatz halting problem.
- **Statement.** For each level of the arithmetic hierarchy, give an explicit example in that level. Useful for placing $T$ in context.
- **D = 3, P = 1.**

---

## F. Cross-cutting / methodological

### F.1 Bridge between Tao 2022 (log-density) and Krasikov–Lagarias 2003 (positive density of pre-images).
- **Statement.** Reconcile: Tao gives a density-1 statement for some descent; Krasikov–Lagarias gives a density-$x^{0.84}$ statement for *every* fixed value. Find a unified framework.
- **D = 3, P = 3.**

### F.2 ML / data-driven discovery of Collatz invariants.
- **Statement.** Train transformer-based or graph-NN models on Collatz orbits and look for learned features that correspond to candidate Lyapunov functions or to cycle obstructions. Recent 2025 preprints (e.g., transformer learning of Collatz) suggest this is a live direction.
- **D = 2, P = 2.** Low risk, exploratory; produces hypotheses for B.1 or D.1.

### F.3 Formal verification of existing Collatz proofs.
- **Statement.** Formalize Tao 2022, Krasikov–Lagarias 2003, Steiner 1977 in Lean / Coq / Isabelle. The Collatz Conjecture Challenge (ccchallenge.org) is doing this in 2025.
- **D = 3, P = 2.** Stabilizes the literature; finds gaps in published proofs.

### F.4 Erdős-style problems on parity sequences.
- **Statement.** Parity-vector statistics (the indicator of $T^k(n)$ being odd) have a deep connection to Tao's argument. Direct statistical study of these sequences (their correlations, autocorrelations, large-deviation rates) may yield independent leverage.
- **D = 3, P = 2.**

---

## Highest-priority shortlist

For a Phase-2 research effort with limited resources, we recommend:

1. **A.1 + A.2 (Tao's program).** Highest expected payoff per unit effort, direct continuation of the SOTA.
2. **D.1 + D.2 (cycle exclusion).** Lowest-risk parallel track; well-defined techniques.
3. **C.3 + F.2 (computational + ML).** Cheap, fast-feedback exploration that feeds hypotheses into (B.1) and (D.3).

We **do not** recommend pursuing (B.1) or (D.3) as primary tracks: they are the highest-payoff problems, but they are also the ones where decades of effort by experts have produced essentially no traction. They are best treated as background exploratory problems while concrete progress is sought via (A) and (D).
