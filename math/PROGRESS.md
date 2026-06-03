# Project Progress Tracker

Living status of the Collatz & Frankl multi-agent research effort. Updated as phases complete.

## Phase 1 — Foundation

| Agent | Track | Status | Output |
|-------|-------|--------|--------|
| Shared infra | both | ✅ done | notation, paper_targets, ai_norms, verification_protocol, dead_ends |
| Frankl literature | Frankl | ✅ done | survey.md (7 slack points), bibliography.bib, open_problems.md |
| Collatz literature | Collatz | ✅ done | survey.md (6 approach families, gap analysis), bibliography.bib, open_problems.md |
| Frankl toolkit | Frankl | ✅ done | 44 tests pass; all 29,743 UC families (n≤5) enumerated; Gilmer ineq + Frankl verified on all; sweep_inequality() harness for Phase 2 |
| Collatz toolkit | Collatz | ✅ likely done | verifier, stats, residue_analysis, cycles, run_baseline + figures + data |
| Paper/Lean scaffold | both | ✅ done | both papers compile (verified); Lean Lake project typechecks (sorries) |

### Infrastructure constraints discovered
- **Lean/Mathlib is firewalled in-sandbox**: release.lean-lang.org, reservoir.lean-lang.org, and the Mathlib Azure binary cache all return 403. From-source Mathlib build ≈ 1–2 h. Scaffold ships conjecture statements against Lean core/stdlib only (`sorry`). ⇒ **Phase 4 Lean verification limited to statement-level formalization** unless network policy widens. Heavy-lemma formalization deferred.
- **arXiv WebFetch blocked (403)** during literature work; surveys verified via search snippets + secondary sources, flagged `[PARTIAL]`/`[UNVERIFIED]` where uncertain.
- CI LaTeX build fixed (added `lmodern`); both PDFs verified to compile with resolved citations.

## Key Phase 1 Findings

### Frankl — verified state of the art
- Entropy method (Gilmer 2022, arXiv:2211.09055): first constant ~0.01.
- Closed form **(3−√5)/2 ≈ 0.38197** — Nov 2022, four independent proofs (Sawin; Chase–Lovett; Alweiss–Huang–Sellke; Pebody).
- Numerical refinements: Yu 0.38234; **Liu 2024 ≈ 0.38271** (current record); Cambie reweighting.
- Target: 0.5. Frontier gap: 0.383 → 0.5.
- **7 slack points** identified (survey §7). Top 3 attack vectors:
  1. Shearer-style chain rule recapturing discarded conditional mutual information.
  2. Intersection term H(A∩B) (never used; Reimer's bound is intersection-side).
  3. Joint optimization over couplings (larger |U|) + reweighted measure (how records were set).

### Collatz — computational baseline (toolkit, N=10^7)
- 10^7/10^7 verified to reach 1. Throughput ~1.05M n/s single-core (beat target ~100×).
- Longest σ∞ = 429 at n=8,400,511 (peak ≈ 7.97×10^10). Max τ = 246 at n=8,088,063 (note: σ∞-record ≠ τ-record).
- σ∞ OLS slope 6.9325 vs heuristic 2/log(4/3)=6.9521 (within 0.3%) — matches Tao-style random model.
- No non-trivial cycle up to parity-length m=22 and orbit-following n≤10^6.
- **Observation to vet for novelty (likely NOT novel):** Syracuse offset b(r) in T^k(n)=3^{a(r)}q+b(r) has b(r) mod 3 distributed exactly (0,1,2) → frequencies (1, (2^k−1)/3, 2(2^k−1)/3) for all even k≤20 (a rigid 1:2 ratio). Almost certainly derivable from the 3^a multiplier structure; flagged for red-team to confirm it is known before any writeup.

### Collatz — verified state of the art
- Tao 2022 (Forum of Math Pi, arXiv:1909.03562): almost all orbits (LOG density) attain almost bounded values, via Syracuse random variables on (ℤ/3ⁿℤ)ˣ.
- Computational verification: **2^71** (Barina 2025), up from Oliveira e Silva (20·2^58) and Barina 2021 (2^68).
- Cycle exclusion: **m ≤ 91** (Hercher 2023), via Simons–de Weger Diophantine method; rate-limited by irrationality measure of log₂3.
- Generalized Collatz is Π⁰₂-complete (Kurtz–Simon 2007); FRACTRAN (Conway).
- Three attack vectors:
  - **A (primary, hard):** Tao log→natural density via Syracuse mixing on (ℤ/3ⁿℤ)ˣ; target c_n ≥ 3^(−n−o(n)).
  - **C (low-risk):** push cycle exclusion past m=91 via improved log₂3 irrationality measure.
  - **B (exploratory):** 2-adic Lyapunov function (Akin 2004 style).

## Phase 2 — Investigation

| Agent | Track | Status | Target |
|-------|-------|--------|--------|
| Frankl analytic | Frankl | ✅ done | Vectors 1 & 2 both FAILED (rigorous negative results); no improvement claimed |
| Frankl computational | Frankl | ⏳ running | Vector 3 (joint optimization + certification) |
| Collatz Tao-density | Collatz | ✅ done | Vector A — conditional reduction (see below); [UNVERIFIED] pending red-team |
| Collatz cycle-exclusion | Collatz | ✅ done | Did NOT beat m≤91 (PDF access blocked); corrected survey's bottleneck framing; found cheap improvement route |
| Frankl computational | Frankl | ✅ done | Certified ψ=(3−√5)/2 (closed-form + interval arith); plateaus at ψ; richer couplings move WRONG way |

**Phase 2 verdict: no proof, no improved constant.** Both Frankl agents independently converged: entropy method caps at ψ; only escape is recapturing Δ₂ at a non-product extremizer. Both Collatz tracks: honest negatives + one conditional theorem. ALL [UNVERIFIED] pending red-team.

## Phase 3 — Verification & Decisive Experiments

| Agent | Status | Target |
|-------|--------|--------|
| Collatz FFT experiment | ✅ done | E_n DIVERGES to n=15 (no turnover); cross-check passed; scalar-Esscher route obstructed; phase transition at s_c≈−0.4 |
| Internal-logic red-team | ✅ done | 5/6 docs sound; 1 blocks-publication error found (Tao §6); novelty = biggest risk. See RED_TEAM_REPORT.md |
| Author-line fix | ✅ done | Removed Claude as co-author from both papers; AI disclosed via \thanks only |
| Frankl paper draft | ✅ done | 14pp, compiles clean (exit 0, 0 undefined). 9 prior-art + 21 const-unverified markers. Claims NO improvement. |
| Frankl Δ₂ attack | ✅ done | FAILED (clean): recapturing Δ₂ at non-product extremizer moves constant DOWN; best certified = ψ. Artifact re-caught & rejected. |
| Collatz consolidate+draft | ✅ done | Obstruction doc written; FFT hardened to n=16/17 (divergence holds); paper compiles clean. |

## Phase 3 verdict — DRAFTS COMPLETE, both papers compile
- **Frankl paper**: honest survey + (3−√5)/2 reconstruction + two negatives + ψ certificate. No improved constant.
- **Collatz paper**: honest survey + natural-density obstruction (TV≥1/6, doubly supported) + cycle reconstruction. No proof.
- **Frankl Δ₂ attack** sharpened the ceiling result: recapturing Δ₂ provably backfires (c_aug ≤ ψ over all 29,723 families).
- Net mathematical result of the whole effort: **no proof, no improved constant** — two honest expository+negative-result papers, all claims red-team-checked for internal soundness, all external facts flagged for the (blocked) primary-source pass.

### FFT verdict (Collatz Vector A) — corroborates red-team
- n=2..6 cross-check PASS (matches independent DP to <1e-15). Reached n=15.
- Untilted E_n ≈ 0.31n (linear divergence); tilted s* E_n ≈ 0.92·1.434^n (EXPONENTIAL divergence) — the required tilt makes equidistribution worse.
- **Phase transition at s_c≈−0.4:** E_n bounded only for s≲−0.45 (tail-fattening negative tilts), divergent for s≳−0.4. Drift-neutrality (E[a]=log₂3) and residue-spreading (E[a]≳3) incompatible under any scalar tilt.
- Honest scope: does NOT touch β=1 (all E_n are 3^{o(n)}); shows β=1 insufficient *for the scalar-Esscher MIX route*; does NOT prove Collatz natural density fails. Numerics, not proof (n≈18–20 would harden).
- ⇒ **Collatz contribution = doubly-supported NEGATIVE result** (analytic TV≥1/6 + numerical E_n divergence), replacing the refuted conditional theorem.

## Phase 2 Findings (ALL [UNVERIFIED] until red-team + human review)

### Collatz Vector A — Tao log→natural density (tao_syracuse_explicit.md)
- **Conditional theorem:** exponential Fourier-decay bound MIX(θ), θ>½, on the *tilted* Syracuse characteristic function ⇒ Tao's theorem in natural density. Hypothesis MIX(θ) is open and strictly stronger than Tao's β=1 conjecture.
- **Unconditional (claimed, needs check):** (a) log-density is forced by stationarity of the sampling measure under the multiplicative first-passage map (Prop 4.2), NOT the dyadic step (Lemma 4.1 shows that's measure-neutral); (b) the obstruction is quantified as a 3^{n/2} Plancherel loss (Lemma 6.2, proved in full).
- **Negative finding — DO NOT TRUST YET:** numerics on n≤6 suggest β=1 is insufficient (collision diagnostic E_n diverges ~0.31n untilted; tilted is worse). Agent itself flags this may be a small-n artifact. **Decisive test required:** push E_n^(s*) to n≈10–14 via FFT + test ξ-dependent tilts. Until then this is a conjecture, not a result.
- Transport steps are at "research-announcement rigor," not formalization-ready. Red-team against the actual Tao paper is mandatory.

### Frankl Vectors 1 & 2 — both FAILED (rigorous negatives)
- Best certified = ψ=(3−√5)/2≈0.381966 (AHS baseline reconstructed from scratch). Does NOT beat Liu 0.38271. No improvement claimed.
- V1 (Shearer recapture): discarded term Δ₂ ≡ 0 at the AHS *product* extremizer ⇒ recapturing it gains nothing there. Empirical anticorrelation: large Δ₂ ⟺ already-high abundance.
- V2 (intersection term): no valid budget — H(A∩B) ≤ H(A) is FALSE for UC families (22,361/29,738 violations, ratio up to 1.53). Union-closure's asymmetry (A∪B∈F, A∩B∉F) is exactly the obstruction.
- ⚠️ Agent caught + discarded TWO artifacts (false "0.4295", buggy "0.5") as budget-mismatch traps. Logged so no later agent resurrects them.
- Live follow-up: recapture Δ₂ at Liu's *non-product* extremizer (Δ₂>0 there) — only route that escapes the V1 obstruction.

### Collatz Vector C — cycle exclusion (cycle_exclusion_explicit.md)
- Did NOT beat m≤91 (Hercher PDF + Laurent-2008 constant unreachable; 403 wall). Reproduced the Steiner–Simons–de Weger–Hercher squeeze; checker confirms largest solution at K=29, none for K≥32.
- **Corrects our own survey.md error:** bottleneck is a *two-log linear form* (Laurent–Mignotte–Nesterenko, const 24.34·D⁴), NOT μ(log₂3). Also: "m≤68" is the circuit count; local-minima convention is m≥76 (S–dW) / m≥92 (Hercher). ⇒ survey.md §7.5/§11 + open_problems.md D.1/D.2 must be fixed.
- Cheapest improvement route: re-run squeeze with B=2^71 (Barina 2025) vs 3·2^69 ⇒ est. +1–3 in m*. Tractable Phase 3 task IF the primary PDFs become reachable.
- Constants tagged [PARTIAL-CONST] (snippet-sourced); F(m) derivation [PARTIAL-DERIV]; "μ useless" claim [CLAIM-UNVERIFIED].

## ⚠️ Structural blocker: network policy
Recurring across ALL research agents: arXiv + every journal/PDF host return **HTTP 403**. Consequences:
- Citations & numerical constants are **snippet-sourced, not primary-verified** — unacceptable for final submission (arXiv's anti-slop policy bans unchecked refs). Must be resolved before any external release.
- Lean **Mathlib** unreachable ⇒ only statement-level formalization possible.
- The concrete Collatz improvement (re-run with Laurent-2008 / B=2^71) is blocked on reading Hercher's explicit cycle-length function.
**Action needed from user:** widen the environment's network policy to allow arXiv/journal access, or supply key PDFs manually. Until then, results stay [UNVERIFIED] at the primary-source level.

### Frankl Vector 3 — computational optimization (results.md, certificate_0.38197.md)
- **Certified ψ=(3−√5)/2≈0.3819660** two independent ways: closed-form (hand-verifiable) + interval arithmetic (mpmath.iv). Reproduced as sanity floor.
- **Did NOT reproduce Liu 0.38271** (Liu's paper inaccessible; two from-scratch reconstructions of the conditional-U bookkeeping failed — one gains nothing, one degenerates to 0). No constant claimed from reconstruction.
- **Plateaus exactly at ψ.** Key certified sub-result: enlarging the coupling class moves the threshold the WRONG way (down to ≈0.359) — a larger class weakens the feasibility necessary-condition. ⇒ the lever to beat ψ is NOT a richer coupling/measure (literal open-problem B.7) but a tighter H(A∪B) lower bound capturing union-closure (the Δ₂ chain-rule slack). **Independently corroborates the Vector-1 agent.**

## Red-Team Results (Phase 3) — see RED_TEAM_REPORT.md
**5 of 6 documents internally sound** (re-derived by hand + independent code):
- ✅ AHS (3−√5)/2 reconstruction — λ=φ/2 provably sharp; 0 violations on 4389 families.
- ✅ Frankl Vector 1 (Δ₂≡0 at product extremizer) — confirmed independently.
- ✅ Frankl Vector 2 + the 0.4295/0.5 artifacts — artifacts are genuine errors that do NOT leak into live claims.
- ✅ ψ interval-arithmetic certificate — genuinely rigorous (certifies at true λ, FAILS when λ bumped 0.1%; not a rubber stamp).
- ✅ Cycle-exclusion reconstruction — de Weger threshold verified exactly (largest soln K=29, none K≥32, checked to K=4999).

**1 publication-blocking error** (now flagged with erratum in the doc):
- ❌ Collatz Tao §6 Lemmas 6.1/6.2 are FALSE. They drop Fourier mass at 3|ξ, but the Syracuse law mod 3 is permanently (0,⅓,⅔). ⇒ TV(ν,U) ≥ 1/6 always; MIX(θ) (only 3∤ξ) does NOT give natural density. The **conditional theorem §5.2 is invalid as stated.** The 3^{n/2} exponent is fine; the error is *which* frequencies are controlled. **Reframe as a clean negative result** (mod-3 projection obstructs natural-density-via-TV) in Phase 3 consolidation.
- Minor: TV→∞ overstatement, n=1 Ramanujan slip, Lemma-2 typo (all hedged in-doc).

**Biggest risk = NOVELTY, not correctness.** The sound results are reconstructions or negatives. The "entropy caps at ψ" observation is very likely already in Sawin / Cambie. Prior-art check is the #1 blocker to any "new observation" framing — REQUIRES primary sources (blocked this session).

## Network status
User chose to **widen network policy**, but arXiv still returns 403 this session (policy is set at env creation; takes effect on a NEW session). ⇒ Primary-source verification + prior-art pass deferred to next session with open network. All constants/citations remain snippet-sourced this session.

## Phase 4 — Extended attacks (per "keep attacking")
| Agent | Status | Verdict |
|-------|--------|---------|
| Collatz cycle from scratch | ✅ done | PROVISIONALLY no robust gain past m=91; new self-contained identity Λ=Σεⱼ + bound 0<Λ<m/B (verified). Corrected our "+1–3" prior to "+0.3, best case +1". |
| Frankl lattice attack | ✅ done | NO invariant bound possible (proved); "cone" construction = sharp obstruction (abundance not a lattice invariant). One folklore-likely conditional bound. |

**ALL AGENTS COMPLETE (17 total across 4 phases).** CI flipped back to blocking (both papers compile).

## Phase 5 — Novel-angle attacks (per "keep attacking; new approaches")
| Agent | Status | Angle |
|-------|--------|-------|
| Frankl polynomial method | ✅ done | Clean STRUCTURAL OBSTRUCTION (proved + verified): slice-rank(T_F) = \|F\|, vacuous against abundance. Diagnoses why cap-set machinery doesn't apply. |
| Collatz digit-sum + 𝔽_p[T] | ⏳ running | Hamming-weight Lyapunov candidates + function-field analog cross-check (not 2-adic). |
| Frankl Boolean Fourier | ✅ done | Third proved obstruction: rotation+sign-invariant quadratic spectral stats CANNOT determine min abundance (Boolean cube saturates Frankl AND has trivial spectrum). Karpas 2017 acknowledged as prior. |
| Frankl LP duality / Poonen | ✅ done | Sixth obstruction: correct dual = Reimer in multiplier form, degenerates on the cube; gap is exactly max-vs-mean (fails on 6 families). Surfaced the second-moment lever. |
| Frankl Kruskal–Katona/shadows | ✅ done | Fifth obstruction: shifting breaks union-closure; AD/FKG wrong sign. ALL FIVE METHODS CONVERGE on the join-irreducible labelling. |
| Frankl second-moment | ✅ done | Seventh obstruction: cube minimizes the power-mean ratio at ½; union-closure bounds U the wrong way. |
| Frankl JI-labelling (frontier) | ⏳ finishing | Direct attack on the convergence chokepoint; H5 labelling-freedom sweep. (deliverable data committed; awaiting report) |
| Collatz transfer operator | ✅ done | Sharpest obstruction reformulation: mod-3 block = [[1/3,2/3],[1/3,2/3]] (eigvals {1,0}); Syracuse RV = unique invariant π_n (proved). Names the uniform-perp-gap path forward. |
| Collatz digit-Lyapunov + 𝔽_p[T] | ⏳ running | (first Phase-5 wave; still running) |

### Emerging theme: FIVE PROVED OBSTRUCTIONS on Frankl, all converging on ONE chokepoint
| # | Method | Obstruction theorem (informal) |
|---|--------|--------------------------------|
| 1 | i.i.d. entropy (Gilmer–Sawin–AHS line) | Caps at ψ=(3−√5)/2; Δ₂≡0 at the product extremizer; richer couplings move the wrong way; Δ₂-recapture backfires. |
| 2 | Polynomial method (Croot–Lev–Pach / slice rank) | slice-rank(T_F) = \|F\| exactly; CLP bound vacuous; A∪B=C is fully determinative + degree Ω(n) per coordinate. |
| 3 | Lattice invariants | Abundance is NOT a lattice invariant (cone construction: lattice-isomorphic, ab 0.5 vs 0.875). |
| 4 | Boolean Fourier (quadratic statistics) | Rotation+sign-invariant W^k / influences / noise-stability cannot determine min abundance (Boolean cube extremizer has trivial spectrum). |
| 5 | Kruskal–Katona / shadows / compression | Shifting does NOT preserve union-closure (and raises max-abundance 77% when it survives); AD/FKG fails (40.5% anti-correlated pairs); no new forcing inequality. |
| 6 | LP duality / fractional relaxation | Correct dual = Reimer in multiplier form; degenerates on the cube (zero margin); residual gap is exactly max-vs-mean (6 families). Free-measure LP is the budget-mismatch trap. |
| 7 | Second-moment / variance inequality | Σ freq² = Σ_{A,B}\|A∩B\| = 2mM₁−U; union-closure bounds U the wrong way. Cube minimizes the power-mean ratio at ½ (variance partner of Reimer). |

**⭐ THE CONVERGENCE (strongest emergent result):** all five orthogonal methods bottom out at the SAME structural obstacle — **the labelling of join-irreducibles** (open problem F.2) — and the SAME universal extremizer (the Boolean cube 2^[n], where abundance = ½ and every invariant/spectral/shadow feature degenerates). The lesson: no coordinatewise / order / spectral / shadow / polynomial *invariant* can control abundance; the crux is the JI-fibre labelling. This is a genuine, publishable "delimiting the methods" contribution that also tells future work exactly where to aim. All [NOVELTY UNVERIFIED]; honest prior-art expected for #1 (Sawin) and #4 (Karpas 2017).

### Frankl polynomial method (polynomial_method.md) — proved obstruction
- **Theorem 2.1:** slice-rank(T_F) = |F| (lower bound via identity submatrix on {(C,C):C∈F}; upper = standard CLP). Verified exactly: 1664/1664 at n≤4, 8561/8561 at n=5, zero deviations across fields 𝔽_{2,3,5,7}. The CLP-style slice-rank bound carries NO abundance information.
- **Diagnosis:** cap-set works because (i) x+y+z=0 is non-determinative + (ii) indicator polynomial has fixed degree 2. Frankl: A∪B=C is fully determinative (transport-plan structure ⇒ unfolding rank = |F|); polynomial has degree Ω(n) per coordinate ⇒ rank bound is Ω(4ⁿ), vacuous against |F|≤2ⁿ.
- Near-miss caught: a weak T_△ correlation with abundance — candidate inequality FALSIFIED by explicit counterexample. 0.43/0.5 trap not hit.
- [NOVELTY UNVERIFIED] — needs prior-art check against Naslund / CLP successor literature next session. Tells the field where NOT to look (polynomial method is structurally inapplicable).

Honest framing: "no one has tried" is unverifiable this session (arXiv 403). These are orthogonal to (a) every prior agent's angle and (b) the entropy/Tao paradigm. All claims flagged `[NOVELTY UNVERIFIED]`.

### Frankl lattice attack (lattice_attack.md) — honest negative + structural insight
- **Proves no general bound from lattice invariants is possible.** The "universal-element cone" cone(G)={∅}∪{A∪{z}:A∈G,A≠∅} is union-closed, lattice-ISOMORPHIC to G (identical invariants) but has abundance 1−1/|L|. Verified: 0 failures over all 206 families at n≤4. Minimal witness: B₃ at abundance 0.5 vs cone at 0.875, same invariants.
- Mechanism: abundance = max filter-density of ground-element fibres; the cone shows this labelling is FREE given L ⇒ invariants powerless. This is exactly why every known special-case result restricts the lattice CLASS, not an invariant.
- One conditional bound (tall lattices): abundance ≥ height(L)/|L|, 0 violations over 29,723 families — but [PRIOR-ART PENDING], likely folklore, NOT claimed new.
- Best future direction: upper-semimodular lattices (Reinhold's lower-semimodular proof doesn't dualize; those classes forbid the cone).

### Collatz cycle bound (cycle_bound_attempt.md) — honest negative + a clean byproduct
- Re-derived from scratch (no Hercher PDF): per-circuit identity, cycle equation, NEW telescoping identity Λ=N log2−K log3=Σⱼ log(1+(1−(2/3)^{aⱼ})/xⱼ) (verified to 1e−120), NEW citation-free bound 0<Λ<m/B (verified on 17,762 fixed points).
- Reconstructs the lower-bound (Crandall) side; does NOT reproduce Hercher's upper bound F(m) — that single step needs his 403-blocked PDF. [PARTIAL-DERIV] now sharply localized.
- **Corrected this project's own prior:** B=2^71 gives only ~+0.3 (m*∈{91,92}, best case +1), NOT the "+1 to +3" my brief assumed. Next convergent plateau needs B≥2^75.7. All [PROVISIONAL/UNVERIFIED vs Hercher 2023].
- The telescoping identity + m/B bound are clean, self-contained additions to the Collatz paper's cycle section (pending verification pass).

## Honesty Ledger
- **Phase 2 produced NO proof and NO improved constant.** This is the expected outcome and is being reported as-is. Frankl best = ψ ≈ 0.382 (below Liu 0.38271). Collatz: no new cycle bound, one conditional theorem.
- The strongest internal result — "entropy method caps at ψ, escape only via Δ₂ at non-product extremizer" — is corroborated by two independent agents BUT is **very likely already known** (Sawin/Cambie discussed the method's ceiling). Red-team must check prior art before any "new observation" claim. Do NOT inflate.
- Two false-improvement artifacts (0.4295, 0.5) were caught and killed; logged in dead_ends.md so no later agent resurrects them.
- Any constant improvement must pass: numerical validation → red-team → (Lean where feasible) → human review → primary-source verification.
- Realistic deliverable now: a survey-with-reconstruction paper (Frankl) + a conditional-reduction note (Collatz), both honest about being expository/partial. NOT a proof of either conjecture.

## Next Decisions
- Authorship: paper author = **Alex Ye**; Claude credited in AI-disclosure statement (no venue permits AI co-authorship).
- arXiv endorsement needed before first upload (math.CO / math.NT).

## CI reminder
- LaTeX paper-build job is **temporarily non-blocking** (`continue-on-error`) because WIP draft commits don't compile and CI runs on every push. **FLIP BACK to blocking** (remove that line in `.github/workflows/math-build.yml`) once both drafts are finalized and verified to build.

## Phase 3 Task Queue (after remaining Phase 2 agents finish)
1. **Decisive Collatz FFT experiment**: push collision diagnostic E_n^(s*) to n≈10–14, test ξ-dependent tilts → resolve whether the "β=1 insufficient" negative finding is real or a small-n artifact. Write to collatz/experiments/syracuse_fft/ (isolated dir, no collision).
2. **Fix survey.md errors** the cycle-exclusion agent caught: μ(log₂3) → two-log linear form (LMN); m-convention (circuits vs local minima). Propagate to open_problems.md.
3. **Red-team agents** (one per track): independently check every claimed lemma against sources; hunt for errors, prior art, and overstatement. Mandatory before any writeup. Special focus: re-derive the Tao "β=1 insufficient" negative finding at larger n; stress-test the Frankl Δ₂≡0-at-extremizer claim.
3. **Paper drafting**: integrate verified findings into the LaTeX skeletons. Survey-with-results framing; do not inflate conditional/partial results.
4. Reconcile strategic_attack_vectors.md hypotheses against what Phase 2 actually found.
