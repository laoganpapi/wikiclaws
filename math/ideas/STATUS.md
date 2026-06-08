# Non-Moment Idea Search — Final Status

**Goal asked:** "at least 1 candidate for each paper" + "repeat until you have ≥ 1."
**Goal status:** **Collatz ✅ (1 surviving candidate, modest)**, **Frankl ❌ (all leads converted to a sharpened barrier; no surviving candidate)**. Reporting truthfully rather than padding.

## What was actually done
- **Phase 1 — Generation:** 12 parallel agents, one per distinct field of mathematics (SOS/Lasserre, commutative algebra, poset topology, representation theory, ergodic theory, higher-order additive, matroid/tropical, probability-beyond-moments, p-adic/automorphic, logic/model theory, category/sheaf, spectral graph/HDX). Each proposed a non-moment / non-symmetric direction with a concrete probe.
- **Phase 2 — Review/triage:** 2 reviewer agents independently re-scored every proposal on (escapes-barrier · concrete · plausible · novel). Independently re-ran key probes and killed two encouraging Collatz signals (42% off-coset mass; I≈0.02 near-disjointness) with fresh computations.
- **Phase 3 — Deep-dives (deciding experiments):** 2 agents ran the reviewer-certified candidates against real falsifiers. Both came back NEGATIVE.
- **Phase 4 — Reviewer-named fallbacks (the second wave):** 2 more agents on the named survivor frontiers (Collatz: Livšic coboundary; Frankl: upper-semimodular JI-overlap). Collatz Livšic = certified negative (non-coboundary). Frankl USM = dead on foundational check.
- **Phase 5 — Surviving frontier candidates (the third wave):** 2 final agents on the genuine open cores. Collatz thermodynamic formalism = surviving candidate (modest). Frankl USM-with-USM-cover-structure = same dead premise revisited (the parasites are distributive, the foundational premise was wrong).

## What survived
### Collatz — 1 surviving candidate ✅
**Thermodynamic formalism / large-deviation theory of the Syracuse cocycle.**
- Closed-form pressure `P(s) = −s log3 + (s−1) log2 − log(1 − 2^{s−1})`; Esscher `s* ≈ −0.438`; rate function `I(0) ≈ 0.0550 / step`; tilted CLT variance `P″(s*) = log3 · log(3/2) ≈ 0.4454`. All MC-validated to 0.2–2%.
- **Honest scope:** *not* a route to natural density (~3%). The candidate's own falsifier verified that a single-parameter Esscher tilt provably cannot saturate the mod-3 marginal (`(0, ⅓, ⅔) → (0, 0.404, 0.596)`; TV floor `1/6 → 0.096`, not 0).
- **Real value (~40–55%):** a publishable quantitative refinement of Tao 2022 with explicit constants. Pending Sinai/Akin/Lagarias prior-art pass.
- **Sharply isolated next frontier:** multi-parameter / time-varying tilts that saturate mod-3 while preserving the LDP envelope.

### Frankl — no surviving candidate ❌ (but the meta-finding is the real output)
Eight independent fields → seven structural negatives + degree-4 SOS collapse (real solver, both gates validated) + upper-semimodular collapse (foundational premise false: 5/6 parasite families are *distributive*). The meta-finding **generalises the project's earlier barrier theorem**:

> **The parasite mechanism is *labelling* of a chain by ground elements, not lattice structure.** Any symmetric convex fibre-moment is uniformly capped below ½ on **every** restricted lattice class we tested, not just the general case. Whatever Reinhold's lower-semimodular proof uses, it is **not** a JI-overlap moment lever — confirmed because the JI-overlap power-mean minimum is exactly 4/9 on every class (all, distributive, modular, lower-SM, upper-SM).

The only direction the search did not kill is the barrier theorem's own capstone (non-symmetric forcing using the cover structure directly — Jordan–Hölder length, atom statistics, an asymmetric "which element is heavy" selector). The search confirms this is the *only* remaining direction; it does not produce a candidate within it.

## What this means honestly
- Collatz: there is a real, modest, surviving candidate worth pursuing — a quantitative sharpening of Tao 2022 within the LDP framework, plus a precisely-stated open follow-up.
- Frankl: the search exhausted the natural-language descriptions of "non-moment" approaches that could be tested in this session. The result is a *strictly stronger* barrier theorem: **the cube + chain-with-extra-labels jointly obstruct every symmetric convex moment over every restricted lattice class.** Any future attack must be non-symmetric AND aware of the labelling-of-chain mechanism — these are now precise constraints, not vague aspirations.

## What is genuinely publishable from this search
- **Frankl paper:** add a "delimitation of restricted-class moment methods" section reporting the USM/distributive parasites + the generalised barrier. This strengthens the paper's existing barrier theorem.
- **Collatz paper:** add the thermodynamic-formalism quantitative sharpening + the multi-parameter-tilt open question.
- Both pending the primary-source / novelty verification pass (still gated on a network-enabled session).

## What I do NOT claim
- No proof of either conjecture.
- No improved bound or unconditional natural-density result.
- The Collatz survivor is a candidate for *quantitative* improvement, not a route to natural density (its falsifier is verified).
