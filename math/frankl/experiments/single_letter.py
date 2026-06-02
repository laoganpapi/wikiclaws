"""
single_letter.py — The rigorous single-letter optimization that governs the
asymptotic constant of each entropy strategy.

This is THE correct object (not per-family heuristics). For each strategy we
identify:
  * the per-coordinate LOWER bound  Φ(α,β)  on the tracked entropy increment,
  * the per-coordinate BUDGET numerator  B(α,β) coming from the upper bound,
  * the closing factor (whether the upper budget is H(A) or 2H(A)).

The certified constant is then  c = 1 - (closing_factor)/μ  with
  μ = inf_{(α,β)∈[0,1]^2}  Φ(α,β) / B(α,β),
where the closing factor is 1 for a budget of 2H(A) and 1/2 for a budget of H(A)
(see derivations in theory/*.md).

We expose a generic optimizer `sharp_ratio` and the specific strategies.

VALIDATION ANCHOR: strategy 'ahs' MUST return exactly psi=(3-sqrt5)/2.

Author: Alex Ye (AI assistance disclosed separately).
"""
from __future__ import annotations
import math

LN2 = math.log(2.0)


def h(p: float) -> float:
    p = float(p)
    if p <= 1e-15 or p >= 1.0 - 1e-15:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


PSI = (3.0 - math.sqrt(5.0)) / 2.0
SIGMA = 1.0 - PSI


def union_p(a, b):
    return 1.0 - (1.0 - a) * (1.0 - b)


def inter_p(a, b):
    return a * b


def H_pair_CD(a, b):
    """Entropy of (A_i∨B_i, A_i∧B_i) = entropy of the multiset {A_i,B_i}."""
    p00 = (1 - a) * (1 - b)
    p11 = a * b
    p10 = a + b - 2 * a * b
    H = 0.0
    for p in (p00, p11, p10):
        if p > 1e-15:
            H -= p * math.log2(p)
    return H


def sharp_ratio(phi, budget, N=800, refine=True):
    """
    Compute μ = inf_{(a,b) in (0,1)^2} phi(a,b)/budget(a,b), avoiding 0/0 corners,
    plus the argmin. Refines around the grid minimizer.
    """
    best = math.inf
    arg = (0.5, 0.5)
    for ia in range(1, N):
        a = ia / N
        for ib in range(1, N):
            b = ib / N
            d = budget(a, b)
            if d > 1e-12:
                r = phi(a, b) / d
                if r < best:
                    best = r
                    arg = (a, b)
    if refine:
        ca, cb = arg
        step = 1.0 / N
        for _ in range(3):
            improved = False
            for da in range(-20, 21):
                a = ca + da * step * 0.1
                if not (1e-6 < a < 1 - 1e-6):
                    continue
                for db in range(-20, 21):
                    b = cb + db * step * 0.1
                    if not (1e-6 < b < 1 - 1e-6):
                        continue
                    d = budget(a, b)
                    if d > 1e-12:
                        r = phi(a, b) / d
                        if r < best:
                            best = r
                            ca, cb = a, b
                            improved = True
            step *= 0.1
            if not improved:
                break
        arg = (ca, cb)
    return best, arg


# Standard AHS budget numerator (per coordinate) for an UPPER bound of H(A) [= log m]:
def budget_ahs(a, b):
    """ (1-b)h(a) + (1-a)h(b).  Closing factor 1/2 (budget = H(A)). """
    return (1 - b) * h(a) + (1 - a) * h(b)


def budget_symmetric(a, b):
    """ h(a)+h(b).  Closing factor 1 (budget = 2H(A) = H(A,B)). """
    return h(a) + h(b)


STRATEGIES = {}


def register(name, phi, budget, closing_factor, note=""):
    STRATEGIES[name] = (phi, budget, closing_factor, note)


# --- AHS baseline: track H(A∪B), budget H(A), closing 1/2 ---
register(
    "ahs",
    phi=lambda a, b: h(union_p(a, b)),
    budget=budget_ahs,
    closing_factor=0.5,
    note="AHS baseline; must give psi.",
)

# --- V2 joint: track H(A∪B,A∩B)=H(multiset), budget 2H(A), closing 1 ---
# Lower bound per coord = H_pair_CD(a,b); budget numerator = h(a)+h(b) (=2H(A) total).
register(
    "v2_joint_sym",
    phi=H_pair_CD,
    budget=budget_symmetric,
    closing_factor=1.0,
    note="track (∪,∩); honest budget 2H(A).",
)

# --- V2 joint but compared (incorrectly) to AHS budget, closing 1/2: the WRONG one,
#     kept to demonstrate the artifact. ---
register(
    "v2_joint_ahsbudget_WRONG",
    phi=H_pair_CD,
    budget=budget_ahs,
    closing_factor=0.5,
    note="ARTIFACT: wrong budget; do not use.",
)

# --- V2 weighted union+lam*inter, HONEST: budget is log m + lam*log|F^cap|.
#     There is NO uniform single-letter budget for log|F^cap| (it is not a sum of
#     per-coordinate h's in general), so this strategy CANNOT be cast as a clean
#     single-letter optimization. Documented in theory; not registered. ---


def report():
    print(f"PSI = {PSI:.6f}   SIGMA = {SIGMA:.6f}\n")
    print(f"{'strategy':<26} {'mu':>9} {'closing':>8} {'constant c':>12}  argmin")
    print("-" * 78)
    for name, (phi, budget, cf, note) in STRATEGIES.items():
        mu, arg = sharp_ratio(phi, budget)
        c = 1.0 - cf / mu if mu > 0 else float("-inf")
        flag = ""
        if name == "ahs":
            flag = "  <-- must equal psi" if abs(c - PSI) < 1e-4 else "  <-- MISMATCH!"
        print(f"{name:<26} {mu:9.5f} {cf:8.2f} {c:12.6f}  ({arg[0]:.3f},{arg[1]:.3f}){flag}")
    print()


if __name__ == "__main__":
    report()
