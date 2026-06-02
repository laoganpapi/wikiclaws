# Open Problems on the Frankl Union-Closed Sets Conjecture

**Companion to** `survey.md`, `bibliography.bib`.
**Compiled:** 2 June 2026.

Each entry below is an open subproblem with concrete numerical targets, drawn directly from the cited literature (verified). Items I could not independently verify a *specific* number for are flagged `[UNVERIFIED]`.

---

## A. The main conjecture and direct strengthenings

### A.1 FUCC itself

> Show that every nonempty union-closed family `F ⊆ 2^[n]` has an element `x` belonging to `≥ |F|/2` sets.

Open since 1979. Best known constant: `(3 − √5)/2 ≈ 0.38197` (Alweiss–Huang–Sellke 2024). Best published numerical: ≈ `0.38271` (Liu 2024).

### A.2 The lattice formulation (Poonen 1992)

> Every finite lattice `L` with `|L| > 1` has a join-irreducible element `j` such that `j ≤ x` for at most `|L|/2` elements `x ∈ L`.

Equivalent to A.1 (Poonen).

### A.3 The graph formulation (Bruhn–Charbit–Schaudt–Telle 2015)

> In every finite bipartite graph `G` with `≥ 1` edge, there are two adjacent vertices each belonging to `≤ half` of the maximal stable sets of `G`.

Equivalent to A.1.

---

## B. Numerical-constant subproblems (the entropy frontier)

### B.1 Beat `0.38271` (the Liu numerical bound)

> Prove a constant lower bound `c > 0.38271`.

Most direct entry point in 2026. Liu's bound is contingent on numerical verification of a finite-dimensional optimization.

### B.2 Make Liu's `0.38271` fully rigorous

> Replace the numerical optimization in Liu (2024) by an analytic proof.

Liu sketches an analytic equation whose solution is the optimum; this has not been verified analytically.

### B.3 Cross the `0.40` threshold

> Prove a constant lower bound `c ≥ 0.40`.

This number is the qualitative "halfway point" in the gap `[0.38, 0.50]` and would constitute strong evidence that an entropy-only proof of FUCC is achievable.

### B.4 Cross the `1/2` line (full FUCC)

The endpoint.

### B.5 Determine the optimum of the conditional-i.i.d.-coupling optimization

> Compute `lim_{k→∞} OPT_k`, where `OPT_k` is the value of Liu/Yu's optimization with auxiliary `|U| = k`.

Currently `OPT_k` is unknown analytically for `k ≥ 4`. Yu shows `OPT_2 ≈ 0.38234` and Liu pushes to small `k > 2`. The limit may or may not equal `1/2`.

### B.6 Find a Shearer-type chain rule respecting union closure

> Replace Gilmer's chain-rule reduction `H(A ∪ B) = Σ_i H((A∪B)_i | (A∪B)_{<i})` with a Shearer-style inequality that uses structural correlations across coordinates induced by union-closure.

Not attempted in any 2022–2025 entropy paper. Identified in §7.2 of `survey.md`.

### B.7 Joint optimization over couplings *and* measures

> Optimize simultaneously over couplings `(A, B)` and weighted measures on `F` (à la Cambie's Maxwell–Boltzmann).

Open as of arXiv 2306.12351 §3.

---

## C. Finite-case subproblems

### C.1 FUCC for ground sets `|⋃ F| = 12`

> Computer-verify FUCC for ground-set size `n = 12`.

Done by Vučković–Živković 2017 (computer-assisted). Next target: `n = 13`. Status: *open*.

### C.2 FUCC for ground sets `|⋃ F| = 13`

Open. Likely requires advances in FC-family enumeration (cf. Marić 2019 for `m = 6`).

### C.3 FUCC for `|F| ≤ K` for `K > 46`

> Roberts–Simpson (2010) prove FUCC for `|F| ≤ 46`. Open: push to `|F| ≤ 100`.

### C.4 Enumerate FC-families for `m = 7`

> Marić (2019, arXiv:1902.08765) completes `m = 6` in Isabelle/HOL. Open: `m = 7`.

A computational target — combinatorially expensive but well-defined.

---

## D. Variants Strengthening or Weakening FUCC

### D.1 Approximate FUCC for `ε ≤ ε_crit`

> Chase–Lovett 2022: for `ε`-approximate union-closed `F`, the bound `(3 − √5)/2` is *optimal*.

Open: identify the sharp `ε_crit`-vs.-constant trade-off curve.

### D.2 Stronger averaging — Cambie's UC_x family

> Bouchard (arXiv:2310.02482) proves `UC_x` for `x ≤ ⌈n/3⌉ + 1`. Open: push `x` higher.

### D.3 Non-uniform-distribution FUCC

> Cambie (2305.19338) proves FUCC for Maxwell–Boltzmann distributions with inverse temperature `≥ β_0`. Open: shrink `β_0` to `0`.

### D.4 Weighted-cube FUCC

> Gendler (2504.13347) generalizes Karpas + Knill to the weighted Boolean cube with success probabilities `(p_1, ..., p_d)`. Open: a unified constant for all `p_i ∈ (0, 1)`.

### D.5 Two stronger conjectures

There exist strict strengthenings of FUCC where one element is in `≥ ½|F| + Ω(1)` sets, or where two specified elements together exceed `|F|`. These were collected in (Pulaj–Raymond–Theis 2016, arXiv:1512.00083) and Sun (arXiv:1711.04276). Open in general.

---

## E. Structural / lattice / graph subproblems

### E.1 FUCC for lower semimodular lattices — settled (Reinhold)

Done; included for completeness.

### E.2 FUCC for *upper* semimodular lattices

Open. Reinhold's argument does not dualize. Status: open.

### E.3 FUCC for graphs of girth `g`

> Bruhn–Charbit–Schaudt–Telle 2015 proved FUCC for chordal bipartite, subcubic bipartite, series-parallel bipartite, and bipartite circular interval graphs. Open: general bipartite graphs of large girth.

### E.4 Necessary conditions on a minimum lattice counterexample

> Bouchard (2503.00277) derives several. Open: extend.

### E.5 FUCC under chain-length restrictions `> 3`

> Colbert (2412.18740) settles chains of length `≤ 3`. Open: length `4`.

---

## F. Methodological / conceptual problems

### F.1 Constructive (algorithmic) proof

> Find an explicit polynomial-time procedure that, given `F`, identifies an element of frequency `≥ c` matching the current best constant.

All known entropy proofs are non-constructive (in the sense that they don't produce the heavy element). Cf. §7.6 of `survey.md`.

### F.2 Identify the "right" structural inequality for union closure

> Articulate an entropy / information inequality that holds *iff* the family is union-closed, in the spirit of Shearer's inequality for graphs.

No known paper proposes one; addressing this would unlock §7.2 of `survey.md`.

### F.3 Add an intersection term

> Show that for some `λ > 0`, augmenting `H(A∪B)` by `λH(A∩B)` improves the per-coordinate bound. (See §7.4 of `survey.md`.)

### F.4 Disprove Sawin's strict inequality

> Sawin sketches that the entropy method can beat `(3 − √5)/2` by some absolute amount `δ > 0`. Open: determine `δ`.

### F.5 Probabilistic / random union-closed families

> Show FUCC holds for the natural model of random union-closed families with high probability.

Cf. Bruhn et al. (2013, arXiv:1302.7141) — FUCC almost holds for almost all random bipartite graphs. Open: a fully probabilistic statement.

---

## G. Connections to other problems

### G.1 Erdős–Ko–Rado-type bounds for union-closed families

> Find the analogue of EKR for union-closed (rather than intersecting) families.

### G.2 Connection to lattice walks / log-concavity

> Several authors (Cambie, Bouchard) hint at log-concavity-type constraints satisfied by counterexamples. Open: formalize and exploit.

---

## H. Concrete numerical targets table

| # | Target | Current | Source |
|---|---|---|---|
| B.1 | `c > 0.38271` | `0.38197` (rigorous), `0.38271` (numerical) | Liu 2024 |
| B.3 | `c ≥ 0.40` | as above | (no paper) |
| C.1 | `n = 12` ground set | done | Vučković–Živković 2017 |
| C.2 | `n = 13` ground set | open | — |
| C.3 | `|F| ≤ 100` | `|F| ≤ 46` | Roberts–Simpson 2010 |
| C.4 | `m = 7` FC | `m = 6` done | Marić 2019 |

---

*Phase 2 will prioritize: B.6, F.3, B.7 (top three actionable theory targets); C.2 and C.4 (computational); and revisiting B.2 by re-running Liu's optimization with extra structural constraints.*
