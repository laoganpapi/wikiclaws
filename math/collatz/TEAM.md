# Sustained Collatz Team

**Mission:** continuous progress on real open frontiers until a breakthrough or genuine exhaustion. Each agent has a standing role; when one reports, commit and relaunch on the next-deepest open question or pivot based on the result.

## Roles

| Role | File prefix | Standing mission |
|------|-------------|------------------|
| Frontier Theory | `collatz_d{N}_tilt*`, `collatz_frontier*` | Push the multi-parameter / time-varying tilt; resolve mod-3^k saturation for each k |
| Cycle Bound | `cycle_bound_push*`, `cycle_*` | Push m past 91; refine F(m); apply newer Diophantine constants |
| Independent Verifier | `verifier_*` | Red-team every theory claim with exact-rational replication; catch errors |
| Alt-Angle Explorer | `ideas/generation/<field>*` | One fresh field per cycle; report direction + small probe (or "why not") |
| Paper Synthesis | `collatz/paper/main.tex` | Keep manuscript current with verified results; flag refuted claims |

## Wave 1 (in flight)
- d=5 tilt for mod-9 saturation
- Cycle bound push with B=2^71 + from-scratch F(m)
- Clean-sheet replication of Class C
- Automorphic / modular-L alt angle
- Paper revision folding in Class C

## Iteration rule
When an agent reports:
1. Commit its output.
2. If a finding is significant (positive lead, decisive negative with structural reason, or error found): note it loudly here and adjust the next wave.
3. Relaunch the same role on the next-deepest open question OR pivot the role.
4. Continue until a breakthrough or the actionable frontier is genuinely dry.

## Live frontier open questions
1. **Mod-3^k saturation for k ≥ 2** via finite-d tilt (d=5 is the next test for k=2; if it works, d=17 for k=3; etc.)
2. **Cycle bound past m=91** with B=2^71 and tighter F(m)
3. **The Sinai/Akin/Lagarias prior-art check** for thermodynamic formalism (gated on network — every result currently `[NOVELTY UNVERIFIED]`)
4. **Effective S-unit bounds vs Hercher squeeze** (if alt-angle agent surfaces something)
5. **Quantitative form of "no finite-d translation-invariant tilt saturates mod-3^k for k > k_*"** — turning the heuristic dimension argument into a proper theorem

## Discipline
- Every claim flagged `[NOVELTY UNVERIFIED]` until primary-source check.
- Every numerical constant flagged `[CONSTANT UNVERIFIED]` until primary-source check.
- Errors caught by the verifier role are reported loudly, not silent-rewritten.
- A clean negative with a structural reason is a valid endpoint and is recorded as a barrier strengthening.
- "Don't stop" does not mean "claim success." It means "keep doing real work."

## Current status
- One surviving candidate: Class C two-parameter Esscher saturates mod-3 with 4.15× LDP rate; finite-d obstruction at mod-9 (provisional).
- Prior sign-convention error caught and corrected; correction banners on the affected docs.
- Paper revision in progress to make Class C the corrected headline.
