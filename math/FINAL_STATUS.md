# Final Status — Collatz & Frankl Research Effort

**Authors:** Alex Ye (AI assistance via Claude, disclosed in-paper, not as author).
**Branch:** `claude/epic-dirac-p1oQo` · **PR:** #1

---

## Bottom line (read this first)

**No proof of either conjecture. No improved bound on either.** This was expected — these are famously open problems. What the effort produced instead is two complete, honest, internally-verified papers (survey + reconstruction + rigorous negative results), and a clear map of why the natural attacks fail.

The single most valuable thing the process did was **catch its own near-misses**: a spurious "0.43–0.50" Frankl improvement (a budget-mismatch artifact) was independently flagged and rejected **three times** (Vector-2 agent, red-team, Δ₂ agent) instead of being shipped as a false result. The honesty discipline held.

## What exists, and its verification status

| Artifact | State | Verified? |
|---|---|---|
| `frankl/paper/main.tex` | Complete draft, 14pp, compiles (exit 0, 0 undef) | Internal math red-team-sound; **external constants UNVERIFIED** (9 prior-art + 21 constant flags) |
| `collatz/paper/main.tex` | Complete draft, compiles (exit 0, 0 undef) | Same posture; obstruction re-derived + FFT-corroborated to n=17 |
| `RED_TEAM_REPORT.md` | 5/6 docs internally sound; 1 blocking error found & fixed | — |
| Frankl theory (AHS recon, V1, V2, V3, lattice) | All negative results, internally sound | Novelty UNVERIFIED |
| Collatz theory (obstruction, cycle bound) | Negative results + 2 clean self-contained identities | Cycle F(m) step needs Hercher PDF |
| Computational toolkits + tests | Frankl 59 tests, Collatz 61 tests, all pass | Reproducible |

## The mathematical results (all honest, all caveated)

**Frankl:**
- Self-contained reconstruction of the entropy-method bound ψ = (3−√5)/2, with a genuinely rigorous interval-arithmetic certificate (red-team confirmed it fails when λ is perturbed — not a rubber stamp).
- Three negative results delimiting the i.i.d. entropy method: (V1) Δ₂ ≡ 0 at the product extremizer; (V2) the intersection term has no valid budget; (V3) recapturing Δ₂ off-product moves the constant *down*. Together: the i.i.d./shared-U entropy method caps at ψ.
- Lattice angle: abundance is provably **not** a lattice invariant (the cone construction), so no invariant-based bound exists; explains why special-case results restrict the class.
- **Did NOT** reach Liu's 0.38271 (his construction is behind the 403 wall) or beat it.

**Collatz:**
- A natural-density **obstruction**: the scalar-Esscher route to upgrading Tao 2022 is blocked because the Syracuse law mod 3 is permanently (0,⅓,⅔) ⇒ TV ≥ 1/6. Re-derived analytically (red-team) and corroborated numerically by exact FFT to n=17 (collision diagnostic diverges, with a tilt-space phase transition).
- Cycle-exclusion: full from-scratch reconstruction + a new telescoping identity Λ = Σⱼ εⱼ and citation-free bound 0 < Λ < m/B (both verified). Did **not** beat m=91; corrected the project's own optimistic estimate (B=2⁷¹ gives ~+0.3, not +1–3).

## The ONE blocker to publishability

Every external constant/citation is **snippet-sourced** (arXiv + all journals returned HTTP 403 this entire session), and the **novelty** of the negative-result observations is unverified — they may already be in Sawin / Cambie / Tao. Per arXiv's anti-slop policy and the project's own norms, **neither paper is submittable until this is cleared.**

## NEXT SESSION — exact steps to finish (network required)

1. **Start a fresh Claude Code on the web session with a widened network policy** (arXiv + journal access). The policy is set at environment creation; this session's 403s cannot be lifted in-place. (Alternative: drop the key PDFs into `math/*/literature/pdfs/`.)
2. Run **one verification agent** to:
   - Resolve all `[CONSTANT UNVERIFIED]` flags (≈21 Frankl + the Collatz set) against primary sources.
   - Settle every `[PRIOR-ART CHECK PENDING]` — especially: is "entropy caps at ψ" already in Sawin (arXiv:2211.11504/2211.13139) or Cambie (2212.12500)? Is the mod-3 obstruction in Tao's paper/blog? Is `abundance ≥ height/|L|` folklore?
   - Fetch Hercher 2023 to close the cycle-bound F(m) step and confirm m* ∈ {91,92}.
   - Reconcile the enumeration count (29,738 vs 29,743) discrepancy.
3. Based on novelty findings, **reframe each paper's contribution honestly** (if the observations are known, the papers are expository/pedagogical notes — still legitimate, but framed as such).
4. Secure an **arXiv endorser** in math.CO and math.NT before first upload.
5. Optional further attacks (all lower-odds): Frankl upper-semimodular lattices; Collatz Vector B (2-adic Lyapunov); push FFT to n≈20 to further harden the obstruction.

## Honesty discipline (maintained throughout)
- No fabricated theorems, constants, or citations.
- Every "result" that's actually a reconstruction or a negative is labeled as such.
- Dead ends (incl. the artifacts) recorded in `*/theory/dead_ends.md` and `shared/dead_ends.md`.
- Two complete papers that claim exactly what was proven — and nothing more.
