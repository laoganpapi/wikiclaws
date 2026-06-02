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
| Frankl analytic | Frankl | ⏳ running | Vectors 1 & 2 (Shearer chain rule, intersection term) |
| Frankl computational | Frankl | ⏳ running | Vector 3 (joint optimization + certification) |
| Collatz Tao-density | Collatz | ⏳ running | Vector A (log→natural density, conditional reduction) |
| Collatz cycle-exclusion | Collatz | ⏳ running | Vector C (push m past 91) |
| Collatz experiments | Collatz | ⏸ pending toolkit | verification frontier + Syracuse tables |

## Honesty Ledger
- No proof claims yet. Any constant improvement must pass: numerical validation on all small UC families → red-team → (Lean where feasible) → human review.
- Realistic best case Frankl: a rigorously certified constant slightly above 0.38271, or a sharp account of why entropy methods plateau.
- Realistic best case Collatz: verification frontier extension + structural observations; NOT a proof.

## Next Decisions
- Launch Collatz Phase 2 agents once Collatz literature + toolkit land.
- Authorship: paper author = **Alex Ye**; Claude credited in AI-disclosure statement (no venue permits AI co-authorship).
- arXiv endorsement needed before first upload (math.CO / math.NT).
