# Non-Moment Idea Search — Plan

**Goal:** Surface at least ONE promising NON-MOMENT / NON-SYMMETRIC attack candidate for EACH problem (Frankl, Collatz) that genuinely escapes the barriers this project proved. Output = directions/research programs, not proofs.

## Why (the barriers we must escape)
- **Frankl:** Proven barrier — *every* symmetric convex moment of the frequency vector is flat-minimized by the Boolean cube at ½, so no such moment can prove Frankl. The barrier also extends to separable generator-asymmetric quantities. The cube is the unique extremal lattice (verified n≤5). Frankl reformulated as a non-separable inequality on join-irreducible fibre overlaps. ⇒ Need a genuinely NON-symmetric / NON-moment ingredient (homological, representation-theoretic, higher-degree SOS, asymmetric/structural induction, definability-based, …).
- **Collatz:** The scalar-Esscher mixing route to natural density is obstructed; the obstruction is the *exact* non-uniform stationary distribution π_n of the transfer operator (mod-3 rank-1 block; P_n−Π nilpotent), NOT a mixing-rate defect. Moment/averaging/spectral-radius arguments are inert. ⇒ Need an idea exploiting the *exact* π_n structure or a fundamentally different invariant (homological, automorphic, p-adic/Berkovich, ergodic-rigidity, …).

## Phases
1. **Generation (wide):** ~12 agents, each keyed to a distinct field/cluster of mathematics, propose concrete non-moment attack sketches for Frankl and/or Collatz. Each must (a) state how the field's tools could escape the relevant barrier, (b) give a concrete first step + a small validation, (c) self-assess plausibility and honestly flag speculation. Write to `ideas/generation/<field>.md`.
2. **Review/triage:** review agents read ALL proposals, score each on four axes — *escapes-the-barrier*, *concreteness/actionability*, *plausibility*, *novelty-potential* — and produce a ranked shortlist per problem. Write to `ideas/review/`.
3. **Deep-dive:** for the top 1–2 per problem, an agent fleshes the idea into an actionable research program (definitions, first lemmas to attempt, a computational probe on the n≤5 / 3^n data). Write to `ideas/candidates/`.
4. **Iterate** if no candidate clears the bar: a second targeted generation wave at the gaps the reviewers flag. Repeat until ≥1 solid candidate per problem.

## Discipline
- These are SPECULATIVE directions. No proofs claimed. Every idea flagged with a plausibility rating and `[NOVELTY UNVERIFIED]`.
- An idea only counts as a "candidate" if a reviewer certifies it genuinely escapes the proven barrier (not a disguised symmetric moment) AND has a concrete first step.
- Honesty over enthusiasm: a well-argued "this field cannot help, because X" is a valid and useful generation output.

## Field clusters (generation wave 1)
1. SOS / Lasserre / Positivstellensatz (degree ≥ 4 — beyond the moment-LP)
2. Commutative algebra / Stanley–Reisner / free resolutions / local cohomology
3. Algebraic & poset topology / discrete Morse / Möbius / homotopy type
4. Representation theory & non-abelian harmonic analysis
5. Ergodic theory / joinings / Furstenberg / Sarnak-type rigidity
6. Additive combinatorics / higher-order Fourier / Gowers / Croot–Sisask
7. Matroid / oriented-matroid / tropical & min-plus
8. Probability beyond moments: couplings / optimal transport / martingale embedding / Stein
9. Number-theoretic heavy artillery (Collatz): p-adic & Berkovich dynamics, automorphic/modular, heights/Arakelov
10. Model theory / logic / descriptive set theory / proof-theoretic strength
11. Category theory / topos / sheaf cohomology
12. Spectral graph theory / high-dimensional expanders / Garland method
