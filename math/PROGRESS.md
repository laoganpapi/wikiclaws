# Project Progress Tracker

Living status of the Collatz & Frankl multi-agent research effort. Updated as phases complete.

## Phase 1 — Foundation

| Agent | Track | Status | Output |
|-------|-------|--------|--------|
| Shared infra | both | ✅ done | notation, paper_targets, ai_norms, verification_protocol, dead_ends |
| Frankl literature | Frankl | ✅ done | survey.md (7 slack points), bibliography.bib, open_problems.md |
| Collatz literature | Collatz | ✅ done | survey.md (6 approach families, gap analysis), bibliography.bib, open_problems.md |
| Frankl toolkit | Frankl | ⏳ running | uc_family, enumerate, entropy_bounds, extremal_search, verify_frankl |
| Collatz toolkit | Collatz | ⏳ running | verifier, stats, residue_analysis, cycles + figures |
| Paper/Lean scaffold | both | ⏳ running | frankl+collatz main.tex, lean Lake project |

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
