# Sustained Collatz Team — Wave 1 Results + Live Status

**Mission:** continuous progress on real open frontiers until a breakthrough or genuine exhaustion. Each agent has a standing role; when one reports, commit and relaunch on the next-deepest open question or pivot based on the result.

## Wave 1 — outcomes

| Role | Wave 1 outcome | Disposition |
|------|----------------|-------------|
| **Paper Synthesis** | ✅ Section 8 added (18pp); fixed propagating 0.096 error; folded Class (C) as headline. **Caught Verifier's n=1-vs-n≥2 misread on mod-9 TV** — paper's 0.31299 (steady-state) is correct, Verifier's 0.626 was n=1 only. | idle (next: fold d=5 obstruction into paper) |
| **Independent Verifier** | ✅ Confirmed Class (C) core (clean closed form r_C² = log(9/8)/log 18, I = 0.227908…). Caught its own role: flagged a misread that Synthesis verified. | idle (next: red-team d=5 obstruction theorem) |
| **Frontier Theory** | ✅ **d=5/6 tilt for mod-9: STRUCTURAL OBSTRUCTION, decisively.** Upgraded the multi-tilt heuristic dimension argument to a proper theorem: for k≥2, the unique mod-3^k-saturating per-coord distribution is uniform on residue classes; this violates drift balance by gap_k = 3^(k−1) + 1/2 − log₂3 (growing as Θ(3^(k−1))). The translation-invariant per-coord Esscher route to natural density is **closed for k ≥ 2.** | needs relaunch |
| **Cycle Bound** | ✅ v1 done (couldn't reach F(m) without Hercher's PDF; new Legendre/convergent pinch; honest m\*(2^71) ∈ {91,92}). ⏳ v2 running: conditional theorem combining κ-improvement with B=2^71. | v2 in flight |
| **Alt-Angle** | ✅ Wave 1: κ-improvement leverage curve (m\* ≈ 1/√κ). ✅ Wave 2: sum-product/Markoff cleanly negative (4 structural obstructions catalogued). | idle (next: another untried field) |

## The headline of this wave

**The translation-invariant per-coordinate Esscher route to natural density is now closed for k ≥ 2** — and the obstruction is a clean theorem (gap_k growing as Θ(3^(k−1))). Class C's mod-3 success was a *finite-volume coincidence* (the saturating mean 1.5 happens to be < log₂3), not the first step of a viable iteration. This is the strongest negative-result theorem this entire effort has produced, and it precisely demarcates where the natural-density route is barred from this framework.

The corollary for the live frontier: any route to closing the log→natural gap must EXIT the translation-invariant per-coord Esscher framework. The Frontier Theory agent itself names two candidates:
- **Block cocycles** ψ(a_j, a_{j+1}) — but these don't change the per-coord marginal sum, so the obstruction still applies.
- **Non-product Markov tilts** — these leave the Cramér / Gärtner-Ellis framework and degenerate to conditioning tautologies (Class B trivial saturation).

So the obstruction is *quite* strong: it rules out essentially all natural Esscher generalizations. The remaining direction is a non-Esscher reweighting — fundamentally different machinery.

## Wave 2 — next missions

| Role | Wave 2 mission |
|------|----------------|
| Frontier Theory | Beyond Esscher: a structured non-Markov / quenched / Pinsker-style tilt that EXITS the Cramér framework. Long shot but the obstruction is now precise enough to attack it. |
| Independent Verifier | Red-team the d=5 obstruction theorem (sympy uniqueness proof; the Θ(3^(k−1)) growth). |
| Cycle Bound | (v2 in flight; awaiting κ conditional theorem) |
| Alt-Angle | Another untried field: noncommutative ergodic theory / Heisenberg-style nilmanifolds? Pisot/Salem number theory of log_2 3? |
| Paper Synthesis | Fold the d=5 obstruction theorem into the paper as the proper version of Proposition `prop:mod9` / Remark `rem:dimbarrier`. |

## Live frontier open questions
1. **Mod-3^k for k≥2 via non-Esscher reweighting** (only direction left; structurally very hard)
2. **Cycle bound past m=91** via sharper κ in the LMN inequality (conditional theorem in flight)
3. **Prior-art check** for thermodynamic formalism + Class C + the d=5 obstruction (gated on network)
4. **Quantitative refinement of Tao 2022's β=1** independent of the natural-density question

## Discipline notes
- **No silent rewrites:** every claim gets a correction banner if disputed; mutual checking is mandatory.
- **The iteration loop is now demonstrably working:** Verifier caught the multi-tilt agent's 0.096 propagating error; Synthesis caught Verifier's n=1-vs-n≥2 misread; both right at their level.
- **Honest negatives are the team's deliverable when they're real.** The d=5 obstruction is paper-worthy precisely *because* it's a clean structural no-go — not despite it.
