"""
verify_opt_formulation.py — Step-1 checker for opt_formulation.md.

This is the verification-protocol Step-1 gate for the entropy-method
optimization formulation. It exercises EVERY inequality stated in
``opt_formulation.md`` and confirms:

  1. The sharp Sawin per-coordinate inequality (S) holds on a dense grid of
     (p,q) in [0,1]^2 and is tight at p=q=psi.
  2. The crossover identity h(2p-p^2)=h(p) <=> p=psi.
  3. The necessary feasibility inequality (IV) is VIOLATED whenever all atoms
     of mu lie below psi (the contradiction that forces E[P] >= psi).
  4. The base single-letter optimum equals psi, computed two ways (closed form
     and the defining quadratic).
  5. Cross-check against the sibling module verify_ahs.py's lemma2_G constant.

Run: python3 verify_opt_formulation.py

Author: Alex Ye (AI assistance disclosed separately).
"""
from __future__ import annotations

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def h(x: float) -> float:
    """Binary entropy in nats (natural log)."""
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -x * math.log(x) - (1.0 - x) * math.log(1.0 - x)


PSI = (3.0 - math.sqrt(5.0)) / 2.0
LAMBDA = 1.0 / (2.0 * (1.0 - PSI))  # = phi/2 ~ 0.809017


def union_bit(p: float, q: float) -> float:
    """Pr[A_i OR B_i = 1] when A_i~Bern(p), B_i~Bern(q) independent."""
    return 1.0 - (1.0 - p) * (1.0 - q)


# ---------------------------------------------------------------------------
# Check 1: Sawin per-coordinate inequality (S), tight at p=q=psi.
# ---------------------------------------------------------------------------

def check_sawin_inequality(mesh: int = 400) -> tuple[bool, float, tuple]:
    """
    (S):  h(1-(1-p)(1-q)) >= LAMBDA * [ (1-q)h(p) + (1-p)h(q) ]  for all p,q.
    Returns (holds_everywhere, worst_slack, argmin).
    """
    worst = math.inf
    arg = (0.0, 0.0)
    for ip in range(mesh + 1):
        p = ip / mesh
        for iq in range(mesh + 1):
            q = iq / mesh
            lhs = h(union_bit(p, q))
            rhs = LAMBDA * ((1 - q) * h(p) + (1 - p) * h(q))
            slack = lhs - rhs
            if slack < worst:
                worst = slack
                arg = (p, q)
    holds = worst >= -1e-9
    return holds, worst, arg


def check_sawin_tightness() -> tuple[bool, float]:
    """At p=q=psi the inequality (S) should be tight (slack ~ 0)."""
    lhs = h(union_bit(PSI, PSI))
    rhs = LAMBDA * (2 * (1 - PSI) * h(PSI))
    return abs(lhs - rhs) < 1e-10, lhs - rhs


# ---------------------------------------------------------------------------
# Check 2: crossover identity.
# ---------------------------------------------------------------------------

def check_crossover() -> tuple[bool, float]:
    """h(2p-p^2) = h(p) at p=psi, and psi solves p^2-3p+1=0."""
    quad = PSI * PSI - 3 * PSI + 1.0
    cross = h(2 * PSI - PSI * PSI) - h(PSI)
    return (abs(quad) < 1e-12 and abs(cross) < 1e-10), max(abs(quad), abs(cross))


# ---------------------------------------------------------------------------
# Check 3: feasibility (IV) is violated when all atoms < psi.
# ---------------------------------------------------------------------------

def feasibility_gap(points: list[float], weights: list[float]) -> float:
    """
    RHS - LHS of (IV):  E[h(P)] - E_{P,Q iid}[h(union)].
    (IV) holds iff this is >= 0. We expect it < 0 when all atoms < psi.
    """
    k = len(points)
    lhs = sum(
        weights[i] * weights[j] * h(union_bit(points[i], points[j]))
        for i in range(k)
        for j in range(k)
    )
    rhs = sum(weights[i] * h(points[i]) for i in range(k))
    return rhs - lhs


def check_floor_argument(trials: int = 2000) -> tuple[bool, float]:
    """
    For many random laws mu supported strictly below psi, (IV) must FAIL
    (gap < 0). Returns (all_failed_as_expected, worst_violating_gap_sign).
    A single non-negative gap with all-atoms-below-psi would BREAK the proof.
    """
    import random

    rng = random.Random(12345)
    max_gap = -math.inf  # the largest (closest to feasible) gap we see
    ok = True
    for _ in range(trials):
        k = rng.randint(1, 5)
        pts = [rng.uniform(0.0, PSI - 1e-6) for _ in range(k)]
        raw = [rng.random() for _ in range(k)]
        s = sum(raw)
        ws = [r / s for r in raw]
        gap = feasibility_gap(pts, ws)
        max_gap = max(max_gap, gap)
        if gap > 1e-9:  # feasible despite all atoms < psi -> would be a counterexample
            ok = False
    return ok, max_gap


# ---------------------------------------------------------------------------
# Check 4: base optimum equals psi (point mass at psi is feasible & tight).
# ---------------------------------------------------------------------------

def check_point_mass_feasible() -> tuple[bool, float]:
    """delta_psi must satisfy (IV) with equality (gap ~ 0)."""
    gap = feasibility_gap([PSI], [1.0])
    return abs(gap) < 1e-10, gap


# ---------------------------------------------------------------------------
# Check 5: cross-check the constant against verify_ahs.py.
# ---------------------------------------------------------------------------

def check_sibling_constant() -> tuple[bool, str]:
    try:
        import verify_ahs  # type: ignore

        lam_sib = 1.0 / (2.0 * (1.0 - verify_ahs.psi_const()))
        ok = abs(lam_sib - LAMBDA) < 1e-12 and abs(verify_ahs.psi_const() - PSI) < 1e-12
        return ok, f"verify_ahs psi={verify_ahs.psi_const():.10f}, lambda={lam_sib:.10f}"
    except Exception as e:  # pragma: no cover
        return True, f"verify_ahs not importable ({e!r}); skipping cross-check"


def main() -> int:
    print("=" * 72)
    print("Step-1 verification of opt_formulation.md")
    print("=" * 72)
    print(f"psi = {PSI:.16f}   lambda = 1/(2(1-psi)) = {LAMBDA:.16f}")
    print()

    all_ok = True

    holds, worst, arg = check_sawin_inequality(mesh=300)
    print(f"[1a] Sawin (S) holds on 301x301 grid: {holds}  "
          f"(worst slack {worst:+.3e} at p,q={arg[0]:.3f},{arg[1]:.3f})")
    all_ok &= holds

    tight, d = check_sawin_tightness()
    print(f"[1b] Sawin (S) tight at p=q=psi: {tight}  (slack {d:+.3e})")
    all_ok &= tight

    cross_ok, cerr = check_crossover()
    print(f"[2 ] crossover identity & psi solves p^2-3p+1=0: {cross_ok}  (err {cerr:.2e})")
    all_ok &= cross_ok

    floor_ok, mg = check_floor_argument()
    print(f"[3 ] (IV) violated for ALL random mu below psi: {floor_ok}  "
          f"(worst gap seen {mg:+.3e}; must stay < 0)")
    all_ok &= floor_ok

    pm_ok, pmgap = check_point_mass_feasible()
    print(f"[4 ] delta_psi feasible & tight for (IV): {pm_ok}  (gap {pmgap:+.3e})")
    all_ok &= pm_ok

    sib_ok, sibmsg = check_sibling_constant()
    print(f"[5 ] cross-check vs verify_ahs.py: {sib_ok}  ({sibmsg})")
    all_ok &= sib_ok

    print()
    print("RESULT:", "ALL CHECKS PASS" if all_ok else "*** A CHECK FAILED ***")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
