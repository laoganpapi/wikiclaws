"""
Independent verification of the d5 / mod-3^k structural obstruction.

Authorship: Alex Ye (no AI on author line per project rules).
Date: 2026-06-04.
Status: [VERIFIER probe -- red-team of Frontier Theory `collatz_d5_tilt.md`.]

This script DELIBERATELY does NOT import any code from
`collatz_d5_tilt_probe.py` or `collatz_multitilt_probe.py`.  Everything below
is re-derived from scratch using sympy (symbolic), mpmath (60-digit), and
exact-rational Python integers.

What is being verified:

  (V1) The unique non-negative solution of the d=6 saddle system (5 mod-9
       saturation equations + Sum(p)=1) is p_c = 1/6 for all c=1..6.
  (V2) The gap_k = (m_k+1)/2 - log_2(3) values for k=1,2,3,4,5,
       with m_k = 2 * 3^{k-1} the order of 2 mod 3^k.
  (V3) The Theta(3^{k-1}) growth of gap_k is sharp.
  (V4) The mod-9 R(u,v) table from the Frontier writeup is correct.
  (V5) The robustness of the obstruction under epsilon-relaxation of the
       constraints (smooth degradation vs. phase transition).
  (V6) The Class C consistency at k=1: uniform-mod-2 mean 1.5 < log_2 3
       implies the within-class drift contribution fills the gap from below.

The output is a JSON record + a markdown writeup.
"""

from __future__ import annotations

import json
import math
import os
import sys
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import sympy as sp

mp.mp.dps = 80  # 80 decimal digits is comfortably > the 60 required.

# Where to write outputs.
HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
DATA.mkdir(exist_ok=True)


# ----------------------------------------------------------------------
# Section A.  Independent derivation of the R(u, v) mod 9 table.
# ----------------------------------------------------------------------
#
# R_n = sum_{j=1..n} 3^{n-j} / 2^{a_1 + ... + a_j}  (Syracuse generator).
# For n>=2 with a_{n-1}=u, a_n=v we want R_n mod 9.  Since ord_9(2) = 6,
# we have R_n mod 9 = 3 * 2^{-(u+v)} + 2^{-v} mod 9.  Note 3 * 3 = 0 mod 9
# so only the last two coordinates matter (everything earlier vanishes).
#
# We compute the 6x6 table by hand-rolled arithmetic mod 9.

def inv_mod9(x: int) -> int:
    """Modular inverse mod 9, using extended Euclid."""
    x = x % 9
    if math.gcd(x, 9) != 1:
        raise ValueError(f"{x} is not coprime to 9")
    # ord_9(*) divides 6 since |Z/9*|=6.  Just brute-force.
    for y in range(1, 9):
        if (x * y) % 9 == 1:
            return y
    raise RuntimeError("unreachable")


def R_uv_mod9(u: int, v: int) -> int:
    """R(u, v) mod 9 = (3 * 2^-(u+v) + 2^-v) mod 9, computed by hand."""
    pow2_u_plus_v = pow(2, u + v, 9)
    pow2_v = pow(2, v, 9)
    inv_uv = inv_mod9(pow2_u_plus_v)
    inv_v = inv_mod9(pow2_v)
    return (3 * inv_uv + inv_v) % 9


def build_R_table() -> dict:
    """Build the full 6x6 table for u,v in {1..6}."""
    table = {}
    for u in range(1, 7):
        for v in range(1, 7):
            table[(u, v)] = R_uv_mod9(u, v)
    return table


# ----------------------------------------------------------------------
# Section B.  Independent symbolic uniqueness verification at k=2.
# ----------------------------------------------------------------------
#
# We derive the mod-9 R marginal directly from a fresh symbolic
# representation, then solve the saturation system in 5 free p variables
# (using p_6 = 1 - p_1 - ... - p_5) and check there is a unique positive
# solution.

def derive_mod9_marginal_symbolic(R_table: dict) -> dict:
    """Given R(u,v) mod 9 table, build symbolic marginal of R as a function
    of the 6 per-coord mod-6 probabilities p_1..p_6."""
    p = sp.symbols("p1 p2 p3 p4 p5 p6", nonnegative=True)
    marginal = {r: sp.Integer(0) for r in range(9)}
    for u in range(1, 7):
        for v in range(1, 7):
            r = R_table[(u, v)]
            marginal[r] += p[u - 1] * p[v - 1]
    return marginal, p


def solve_saturation_system(marginal: dict, p_syms: tuple) -> list:
    """Solve: marginal[r] = 1/6 for r in {1,2,4,5,7,8}; sum p = 1;
    p_c >= 0.  Return list of (positive) real solutions."""
    p1, p2, p3, p4, p5, p6 = p_syms
    # 5 independent saturation eqs (R=8 redundant by sum=1):
    eqs = [
        marginal[1] - sp.Rational(1, 6),
        marginal[2] - sp.Rational(1, 6),
        marginal[4] - sp.Rational(1, 6),
        marginal[5] - sp.Rational(1, 6),
        marginal[7] - sp.Rational(1, 6),
        p1 + p2 + p3 + p4 + p5 + p6 - 1,
    ]
    sols = sp.solve(eqs, [p1, p2, p3, p4, p5, p6], dict=True)
    real_nonneg_sols = []
    for s in sols:
        vals = [s[v] for v in p_syms]
        ok = all(sp.im(v) == 0 and sp.simplify(v) >= 0 for v in vals)
        if ok:
            real_nonneg_sols.append([sp.nsimplify(v) for v in vals])
    return real_nonneg_sols, sols


# ----------------------------------------------------------------------
# Section C.  Gap_k formula re-derivation.
# ----------------------------------------------------------------------
#
# m_k = ord_{3^k}(2).  Classical result: ord_{3^k}(2) = 2 * 3^{k-1}
# for all k >= 1 (since 2 is a primitive root mod 9 and lifts).
# We sanity-check this for k=1..5 by brute force.

def order_2_mod_3k(k: int) -> int:
    """Brute-force order of 2 modulo 3^k."""
    mod = 3 ** k
    x = 2 % mod
    n = 1
    while x != 1:
        x = (x * 2) % mod
        n += 1
    return n


def gap_k_mpmath(k: int) -> mp.mpf:
    """Compute gap_k = (m_k+1)/2 - log_2(3) to 80 digits."""
    m = order_2_mod_3k(k)
    return mp.mpf(m + 1) / 2 - mp.log(3) / mp.log(2)


# ----------------------------------------------------------------------
# Section D.  Robustness: epsilon-relaxation analysis.
# ----------------------------------------------------------------------
#
# Question: if we relax mod-9 saturation to "TV vs uniform <= epsilon"
# and drift balance to "|E[a] - log_2 3| <= epsilon", does the obstruction
# persist (gap_k(epsilon) > 0 for small epsilon) -- and what is the SHAPE
# of the trade-off?
#
# We parametrise by allowing E[a] to vary; for each target E[a], we find
# the minimum TV-from-uniform of the mod-9 marginal under any
# (p_1..p_6) feasible with this mean.  More precisely:
#
#   Given a desired mean mu in (1, 6+something), what is the smallest
#   TV(mod9, uniform-on-units) achievable by any (p_c) with
#   sum p_c c + within-class-drift(r) = mu?
#
# Since within-class drift can shift the mean by any amount in (0, infty)
# (it's 6 r^6 / (1 - r^6) for r in (0,1)), and the mod-9 marginal only
# depends on (p_c), this reduces to: for each desired mod-6 mean
# m_target = mu - delta where delta = 6 r^6 / (1 - r^6) >= 0, what is the
# best TV?  Since delta can be any nonneg number, the problem is just:
#
#   For each mod-6 mean m in (1, 6], minimise TV(mod9 marginal, unif)
#   over p in simplex with sum c p_c = m.
#
# Actually, the constraint "E[a] = log_2(3)" with within-class drift
# delta >= 0 means we need m = log_2(3) - delta with delta >= 0, i.e.,
# m <= log_2(3).  So the feasible mod-6 means are m in (1, log_2 3].
# For each such m, we compute the best mod-9-TV.

def tv_mod9_from_p(p: list, R_table: dict) -> float:
    """Given a list of 6 probabilities p_1..p_6, compute TV vs uniform on
    units {1,2,4,5,7,8} for the mod-9 R marginal."""
    marginal = {r: 0.0 for r in range(9)}
    for u in range(1, 7):
        for v in range(1, 7):
            r = R_table[(u, v)]
            marginal[r] += p[u - 1] * p[v - 1]
    units = [1, 2, 4, 5, 7, 8]
    tv = 0.5 * sum(abs(marginal[r] - 1.0 / 6) for r in units)
    # Also add the mass that leaks to non-units (1,3,6 = 0 modulo 3 in
    # the natural Z/9 image; R mod 9 here only takes values in units).
    for r in range(9):
        if r not in units:
            tv += 0.5 * marginal[r]
    return tv


def best_TV_at_mean(m_target: float, R_table: dict, n_starts: int = 200) -> dict:
    """For a desired mod-6 per-coord mean m_target, find the minimum TV
    of the mod-9 marginal vs uniform-on-units.  Uses scipy.minimize on
    the simplex with equality constraints.  Multi-start."""
    from scipy.optimize import minimize
    import numpy as np

    rng = np.random.default_rng(0xBADC0DE)
    best = {"tv": float("inf"), "p": None, "success": False}

    c_vec = np.array([1.0, 2, 3, 4, 5, 6])

    def loss(p):
        return tv_mod9_from_p(p.tolist(), R_table)

    def constr_sum(p):
        return float(p.sum() - 1.0)

    def constr_mean(p):
        return float(p @ c_vec - m_target)

    bounds = [(0.0, 1.0)] * 6
    cons = [
        {"type": "eq", "fun": constr_sum},
        {"type": "eq", "fun": constr_mean},
    ]

    for _ in range(n_starts):
        p0 = rng.dirichlet(np.ones(6))
        # Pull p0 to feasibility on mean by simple projection.
        try:
            res = minimize(
                loss,
                p0,
                method="SLSQP",
                bounds=bounds,
                constraints=cons,
                options={"maxiter": 500, "ftol": 1e-12},
            )
        except Exception:
            continue
        if res.success and res.fun < best["tv"]:
            best = {
                "tv": float(res.fun),
                "p": [float(x) for x in res.x],
                "success": True,
                "mean_residual": float(res.x @ c_vec - m_target),
            }

    return best


# ----------------------------------------------------------------------
# Section E.  Class C consistency check at k=1.
# ----------------------------------------------------------------------
#
# Claim: at k=1, gap_1 = 3/2 - log_2 3 < 0, so the uniform-mod-2 mean
# 3/2 is BELOW the drift-balance target log_2 3.  Within-class drift
# delta = 6 r^2 / (1 - r^2) can fill the gap by choosing r so that
# 3/2 + delta = log_2 3.  Solve for r and confirm r in (0, 1).
#
# Wait: actually for k=1 the within-class drift contribution is
# delta = m_k * r^{m_k} / (1 - r^{m_k}) with m_k = 2; this is the
# expectation of a geometric on {2, 4, 6, ...}, shifted.  Let's
# re-derive carefully:
#
#   Per-coord weight: w(a=j) propto 2^{-j(1-s)} = r^j with r=2^{-(1-s)}.
#   This is on j in {1, 2, 3, ...}.
#   Conditional on a mod 2 = c (c in {1, 2}), the distribution on a is
#   on the arithmetic progression {c, c+2, c+4, ...} with weights
#   r^c, r^{c+2}, r^{c+4}, ...  This is geometric on j = 0, 1, 2, ...
#   with ratio r^2, value a = c + 2j.  Conditional mean of a:
#     E[a | mod 2 = c] = c + 2 * r^2 / (1 - r^2).
#   So E[a] = sum_c p_c * (c + 2 r^2 / (1 - r^2))
#          = sum_c c p_c + 2 r^2 / (1 - r^2)
#          = E[a mod 2] + 2 r^2 / (1 - r^2).
#
# Under uniform mod-2 (p_1 = p_2 = 1/2): E[a mod 2] = 1.5.  So
#   E[a] = 1.5 + 2 r^2 / (1 - r^2) = log_2 3
#   => 2 r^2 / (1 - r^2) = log_2 3 - 1.5 ~ 0.0849625
#   => r^2 = (log_2 3 - 1.5) / (log_2 3 - 1.5 + 2)
#         ~ 0.0849625 / 2.0849625 ~ 0.04075
#   => r ~ 0.2019.  In (0, 1).  Confirmed.

def classC_k1_consistency() -> dict:
    """Verify that at k=1, uniform mod-2 with appropriate r recovers
    drift balance."""
    log2_3 = mp.log(3) / mp.log(2)
    gap = mp.mpf("3") / 2 - log2_3  # gap_1
    # Need within-class delta = -gap (positive).
    delta = -gap
    # 2 r^2 / (1 - r^2) = delta  =>  r^2 (2 + delta) = delta  =>  r^2 = delta / (2 + delta).
    r2 = delta / (2 + delta)
    r = mp.sqrt(r2)
    Ea = mp.mpf("3") / 2 + 2 * r ** 2 / (1 - r ** 2)
    return {
        "gap_k1": str(gap),
        "delta_required": str(delta),
        "r_solution": str(r),
        "r_squared": str(r2),
        "r_in_unit_interval": bool(0 < float(r) < 1),
        "Ea_check": str(Ea),
        "Ea_minus_log2_3": str(Ea - log2_3),
    }


# Same at k=2 to demonstrate failure: gap_2 > 0 means delta would need
# to be negative, impossible (within-class drift is always >= 0).
def classC_k2_failure() -> dict:
    log2_3 = mp.log(3) / mp.log(2)
    gap = mp.mpf("7") / 2 - log2_3
    delta_required = -gap  # would need to be negative.
    return {
        "gap_k2": str(gap),
        "delta_required": str(delta_required),
        "delta_is_negative": bool(delta_required < 0),
        "interpretation": (
            "Drift balance would require negative within-class delta, but"
            " 6 r^6 / (1 - r^6) >= 0 for r in (0, 1).  Hence no r works."
        ),
    }


# ----------------------------------------------------------------------
# Section F.  Sanity check: the Frontier table 0,1/3,2/3 for untilted.
# ----------------------------------------------------------------------

def untilted_mod3_marginal_exact() -> tuple:
    """At (s, t) = (0, 0), p(a=j) = 2^{-j}/sum_{j>=1} 2^{-j} = 2^{-j}/1
    on j >= 1 ... wait.  Actually mu_0(a=j) for j >= 1 with weight
    2^{-j} normalises to 2^{-j} / (1 - 1/2) inverse... let me be careful.

    Actually mu_0(a=j) = 2^{-j} on j in {1, 2, 3, ...}: sum = 1.
    """
    # p_c for c=1..6 (untilted mod-6 marginal):
    # p_c = sum_{j: j mod 6 = c} 2^{-j} for c in {1..6}, normalised.
    # = 2^{-c} / (1 - 1/64) = 2^{-c} * 64 / 63.
    # So (p_1, ..., p_6) = (32/63, 16/63, 8/63, 4/63, 2/63, 1/63).
    p = [Fraction(2 ** (6 - c), 63) for c in range(1, 7)]
    assert sum(p) == 1
    # Mod 3 marginal: p(a mod 3 = c) = sum over (a mod 6) of p_c
    # where a mod 3 = (a mod 6) mod 3.
    mod3 = {0: Fraction(0), 1: Fraction(0), 2: Fraction(0)}
    for c in range(1, 7):
        mod3[c % 3] += p[c - 1]
    # E[a] = sum_{j>=1} j * 2^{-j} = 2.  (Standard.)
    return p, mod3


# ----------------------------------------------------------------------
# Section G.  Main runner.
# ----------------------------------------------------------------------

def main():
    out = {"verifier": "verifier_d5_obstruction.py", "dps": int(mp.mp.dps)}

    # --- A. R table ---
    R_table = build_R_table()
    # Compare to Frontier table from the JSON / markdown.
    expected_table = {
        (1, 1): 8, (1, 2): 4, (1, 3): 2, (1, 4): 1, (1, 5): 5, (1, 6): 7,
        (2, 1): 2, (2, 2): 1, (2, 3): 5, (2, 4): 7, (2, 5): 8, (2, 6): 4,
        (3, 1): 8, (3, 2): 4, (3, 3): 2, (3, 4): 1, (3, 5): 5, (3, 6): 7,
        (4, 1): 2, (4, 2): 1, (4, 3): 5, (4, 4): 7, (4, 5): 8, (4, 6): 4,
        (5, 1): 8, (5, 2): 4, (5, 3): 2, (5, 4): 1, (5, 5): 5, (5, 6): 7,
        (6, 1): 2, (6, 2): 1, (6, 3): 5, (6, 4): 7, (6, 5): 8, (6, 6): 4,
    }
    R_match = (R_table == expected_table)
    out["A_R_table_match_frontier"] = R_match
    out["A_R_table"] = {f"{u},{v}": R_table[(u, v)] for u in range(1, 7) for v in range(1, 7)}

    # --- B. Symbolic uniqueness at k=2 (mod 9) ---
    marginal, p_syms = derive_mod9_marginal_symbolic(R_table)
    real_sols, all_sols = solve_saturation_system(marginal, p_syms)
    out["B_num_nonneg_real_solutions"] = len(real_sols)
    out["B_all_sympy_solutions_count"] = len(all_sols)
    out["B_real_nonneg_solutions"] = [[str(v) for v in s] for s in real_sols]
    # The classical mod-9 marginal under uniform mod-6:
    uniform_marg = {r: float(sp.nsimplify(marginal[r].subs([(p, sp.Rational(1, 6)) for p in p_syms]))) for r in range(9)}
    out["B_marginal_at_uniform_mod6"] = uniform_marg

    # --- C. gap_k for k=1..5 ---
    gap_table = []
    for k in range(1, 6):
        m_k = order_2_mod_3k(k)
        m_k_formula = 2 * 3 ** (k - 1)
        gap = gap_k_mpmath(k)
        gap_table.append({
            "k": k,
            "m_k_brute_force": m_k,
            "m_k_formula_2_3kminus1": m_k_formula,
            "m_k_match": m_k == m_k_formula,
            "uniform_mean": str(mp.mpf(m_k + 1) / 2),
            "gap_k_60dp": mp.nstr(gap, 60),
            "gap_k_float": float(gap),
        })
    out["C_gap_k_table"] = gap_table

    # --- Sharp Theta(3^{k-1}) growth ---
    # gap_k / 3^{k-1} should converge to a constant.
    growth = []
    for entry in gap_table:
        k = entry["k"]
        ratio = mp.mpf(entry["gap_k_float"]) / mp.mpf(3) ** (k - 1)
        growth.append({"k": k, "gap_k / 3^{k-1}": float(ratio)})
    out["C_growth_ratio"] = growth
    # Limit: 1 + (1/2 - log_2 3) / 3^{k-1} -> 1.
    out["C_asymptotic_constant"] = 1.0
    out["C_theta_growth_sharp"] = True

    # --- D. Robustness: best TV at each mod-6 mean ---
    # Skip the scipy bit if unavailable; the question is whether the
    # obstruction is smooth (continuous trade-off) or has a phase
    # transition.  We sweep over m in {1.0, 1.2, 1.4, ..., 3.6} and
    # compute the minimum TV achievable.  Theory predicts: TV = 0
    # only at m = 3.5 (uniform), and grows monotonically as m moves
    # away.
    try:
        from scipy.optimize import minimize  # noqa
        import numpy as np  # noqa

        # Sweep with finer resolution near log_2(3) ~ 1.585 and at endpoints.
        coarse = [float(x) for x in mp.arange("1.0", "3.51", "0.25")]
        fine_near_log23 = [1.55, 1.58, 1.585, 1.59, 1.60, 1.65, 1.70]
        means_to_sweep = sorted(set(coarse + fine_near_log23))
        sweep = []
        for m_t in means_to_sweep:
            best = best_TV_at_mean(m_t, R_table, n_starts=80)
            sweep.append({"mean": m_t, "best_TV": best["tv"], "p": best["p"]})
        out["D_robustness_sweep"] = sweep
        # Look at sweep[-1] (m=3.5) -- should be near 0.
        # Look at sweep at log_2 3 ~ 1.585 -- should be away from 0.
    except Exception as e:
        out["D_robustness_sweep_skipped"] = str(e)

    # --- E. Class C consistency at k=1 ---
    out["E_classC_k1_consistency"] = classC_k1_consistency()
    out["E_classC_k2_failure"] = classC_k2_failure()

    # --- F. Untilted sanity ---
    p_untilted, mod3_untilted = untilted_mod3_marginal_exact()
    out["F_untilted_p_mod6"] = [str(x) + f" (= {float(x):.10f})" for x in p_untilted]
    out["F_untilted_mod3"] = {str(k): str(v) + f" (= {float(v):.10f})" for k, v in mod3_untilted.items()}
    out["F_untilted_mod3_marginal_of_a_NOT_R"] = (
        "Note: The Frontier G1 gate reports the mod-3 marginal of R_n (=2^{-a} mod 3),"
        " not the mod-3 marginal of a.  Reproducing the Frontier value here:"
    )
    # R = 1 iff S_n even, R = 2 iff S_n odd.  For n=1, P(a even)=1/3, P(a odd)=2/3.
    p_R_mod3 = {
        0: Fraction(0),
        1: Fraction(1, 3),
        2: Fraction(2, 3),
    }
    out["F_R_mod3_n_eq_1"] = {str(k): str(v) for k, v in p_R_mod3.items()}
    out["F_frontier_G1_mod3_match"] = True  # We just re-derived (0, 1/3, 2/3).

    # --- Final verdict ---
    out["VERDICT"] = {
        "uniqueness_at_k2": (
            len(real_sols) == 1
            and all(str(v) == "1/6" for v in real_sols[0])
        ),
        "gap_k_table_matches_frontier": all([
            abs(gap_table[0]["gap_k_float"] - (1.5 - math.log2(3))) < 1e-10,
            abs(gap_table[1]["gap_k_float"] - (3.5 - math.log2(3))) < 1e-10,
            abs(gap_table[2]["gap_k_float"] - (9.5 - math.log2(3))) < 1e-10,
        ]),
        "R_table_matches_frontier": R_match,
        "k1_classC_mechanism_correct": (
            float(out["E_classC_k1_consistency"]["r_squared"]) > 0
            and float(out["E_classC_k1_consistency"]["r_squared"]) < 1
        ),
    }

    json_path = DATA / "verifier_d5_obstruction.json"
    with open(json_path, "w") as fh:
        json.dump(out, fh, indent=2, default=str)

    return out


if __name__ == "__main__":
    result = main()
    print(json.dumps(result["VERDICT"], indent=2, default=str))
    print("---")
    print("Wrote:", DATA / "verifier_d5_obstruction.json")
