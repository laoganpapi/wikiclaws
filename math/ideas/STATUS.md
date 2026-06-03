# Non-Moment Idea Search — Status

## Pipeline: Generation (12) → Review (2) → Deep-dive (2, deciding now)

### Certified candidates (≥1 per problem — goal met)
| Problem | Certified candidate | Why it's the target | Deciding experiment (RUNNING) | Reviewer confidence |
|---|---|---|---|---|
| **Frankl** | **Lasserre level-2 (degree-4) incidence SOS** | level-1 = the proven barrier *exactly*; level-2 moments are subset-triple orbit-functions that provably don't factor through the frequency vector ⇒ barrier-as-stated doesn't cover them. Cube-capped at ½ (can prove, not beat). | LAS-2 SDP (cvxpy+SCS, now installed) on the 6 lopsided families: lb_2=½>lb_1 ⇒ separation/lead; lb_2=lb_1 ⇒ collapse/negative. | ~30% real lead |
| **Collatz** | **Joint (residue, drift) law — disjointness (E2≡B.4)** | the only formulation leaving the frozen mod-3 marginal intact (quotients it instead of fighting TV→uniform); not a moment/spectral-radius of P_n. | Ψ_n(ξ,t*) factorization defect Δ_n: →0 power-saving ⇒ disjointness/lead; bounded-below ⇒ coupled/negative. | ~10–15% (reviewer predicts negative) |

### What the wave established (the real output)
- **Frankl:** 7/10 fields' ideas provably RELOCATE to the JI-overlap/Poonen kernel (rep-theory separator broke 245/320; matroid Gram PD ⇒ no Hodge; category dichotomy = Poonen; Gowers flat at all orders; order-only spectra cone-killed). Only 2 have an unfalsified escape (SOS L2, Alexander-dual Betti) — both decidable by computation now running / pending.
- **Collatz:** the cluster splits into **A** (rep-theory ≡ ergodic-E1 ≡ 3-adic Wasserstein = one inert nilpotent operator, descent-blind) and **B** (joint residue-drift). Reviewer KILLED two encouraging signals: the "42% quadratic off-coset mass" (= mod-9/27 coset tower, not quadratic) and the "I≈0.02 near-disjoint" (mod-3 artifact; full-resolution I≈0.3–0.45 bits non-decaying).
- **First invariant ever found non-flat on the cube:** Stanley–Reisner Betti numbers (2^k−1) — the runner-up Frankl lead.

### If both deciding experiments come back negative
Reviewer-named next targets:
- **Frankl:** attack the max-vs-mean spread of the JI-overlap **restricted to the cone-blocked (upper-semimodular) class** where the 6-family parasite cannot be built (three independent notes converge here).
- **Collatz:** drop Cluster A; if Ψ_n fails, attack the 2-adic/size variable directly — the **Livšic coboundary** of φ = log3 − a·log2 (cohomological, non-moment).

### Infra note
cvxpy 1.9.1 + SCS installed this session (unblocked the Frankl SOS deciding test). arXiv still 403 ⇒ all novelty `[NOVELTY UNVERIFIED]`.
