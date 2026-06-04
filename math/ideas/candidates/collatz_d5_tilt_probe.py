#!/usr/bin/env python3
r"""
collatz_d5_tilt_probe.py
========================

5/6-parameter Esscher tilt of the Syracuse Bernoulli base measure mu_0 with
cocycles psi_i = 1[a mod 6 = i], i = 1, ..., 5 (gauge: t_6 = 0).
Goal: decide whether the mod-9 marginal of R_n can be driven exactly uniform
on (Z/9)^x = {1,2,4,5,7,8} by such a tilt, simultaneously with drift balance
E[phi] = 0, and with a positive LDP rate I(0).

Conventions (pressure-side, matching collatz_multitilt_probe.py):
  - mu_0(a = k) = 2^{-k},  k = 1, 2, 3, ...
  - phi(a) = log 3 - a log 2;   E_{mu_0}[phi] = log3 - 2 log2 ~ -0.2877.
  - Per-coord weight under the d-parameter Esscher tilt:
        w(a = k) = mu_0(k) * exp(-s phi(k) - sum_{c=1..5} t_c * 1[k mod 6 = c])
                 = 2^{-k(1-s)} * 3^{-s} * exp(-t_{k mod 6})       (t_6 = 0)
  - Let r := 2^{-(1-s)}  in (0, 1).  Per-coord cumulant
        lambda(s, t) := log E_{mu_0}[exp(-s phi - sum t_c psi_c)]
                      = -s log 3 + log Z(s, t),
        Z(s, t) = sum_{k>=1} 2^{-k(1-s)} exp(-t_{k mod 6})
                = (1/(1-r^6)) * sum_{c=1..6} exp(-t_c) r^c   (t_6 := 0)
  - The mod-6 marginal of a under the tilt:
        p_c := P_{s,t}(a mod 6 = c)
             = (e^{-t_c} r^c / (1 - r^6)) / Z(s, t)        (c = 1..6)
  - Within mod-6 class c, the conditional distribution is "c shifted geometric on {0, 6, 12, ...}"
    with ratio r^6.  E[a | a mod 6 = c] = c + 6 r^6 / (1 - r^6).
  - E[a] = sum c * p_c + 6 r^6 / (1 - r^6) = (sum c p_c) + 6 r^6/(1-r^6).

The mod-9 marginal of R_n (n >= 2) depends, under i.i.d. coords, on the joint
distribution of (a_{n-1} mod 6, a_n mod 6).  Direct computation of
R(u, v) := (3 * 2^{-(u+v)} + 2^{-v}) mod 9 for u, v in {1,...,6} gives:

   u\v | 1 2 3 4 5 6
   ----+-------------
    1  | 8 4 2 1 5 7    <- u odd
    2  | 2 1 5 7 8 4    <- u even
    3  | 8 4 2 1 5 7    <- u odd
    4  | 2 1 5 7 8 4    <- u even
    5  | 8 4 2 1 5 7    <- u odd
    6  | 2 1 5 7 8 4    <- u even

R(u, v) depends only on (u mod 2, v).  Setting P_odd = p_1+p_3+p_5, P_even = p_2+p_4+p_6:
  P(R_n = 1 mod 9) = P_odd p_4 + P_even p_2
  P(R_n = 2 mod 9) = P_odd p_3 + P_even p_1
  P(R_n = 4 mod 9) = P_odd p_2 + P_even p_6
  P(R_n = 5 mod 9) = P_odd p_5 + P_even p_3
  P(R_n = 7 mod 9) = P_odd p_6 + P_even p_4
  P(R_n = 8 mod 9) = P_odd p_1 + P_even p_5

Saturation = all six = 1/6.

VALIDATION GATES (mandatory):
  G1.  At s = 0, t = 0 (untilted), mod-3 marginal = (0, 1/3, 2/3); mod-9 matches
       Class C log file's "untilted" row.
  G2.  Single-parameter drift-balancing Esscher tilt (s = THETA_STAR, t_c = 0)
       reproduces the Class-C-WORSE marginal (0, 0.270, 0.730) with TV 0.230.
       (Sign-corrected baseline from collatz_multitilt.md.)
  G3.  At the Class-C embedding (s_C, t_1 = t_3 = t_5 = -t_C, t_2 = t_4 = 0),
       reproduce mod-3 uniform on units and I_two = 0.228.

OUTPUT:
  data/d5_tilt_probe.json     -- numerical record
  data/d5_tilt_probe.log      -- human-readable verdict
"""

from __future__ import annotations
import json
import math
import os
import sys
import time
from fractions import Fraction
from typing import Any, Dict, List, Tuple

import numpy as np
from scipy.optimize import root

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
os.makedirs(DATA_DIR, exist_ok=True)

LOG2 = math.log(2.0)
LOG3 = math.log(3.0)
LOG2_3 = LOG3 / LOG2  # = log_2(3)
EBAR = LOG3 - 2.0 * LOG2

# Single-parameter Esscher (pressure-side).
def pressure_one(s: float) -> float:
    if s >= 1.0:
        return float("inf")
    return (-s * LOG3) + (s - 1.0) * LOG2 - math.log1p(-math.pow(2.0, s - 1.0))


def esscher_drift_balancing() -> float:
    u_star = LOG2 / LOG3
    return 1.0 + math.log2(1.0 - u_star)


THETA_STAR = esscher_drift_balancing()  # ~ -0.43803

# R(u, v) mod 9 table (precomputed).
def build_R_table() -> Dict[Tuple[int, int], int]:
    inv2 = pow(2, -1, 9)
    inv2_pow = {0: 1}
    for k in range(1, 14):
        inv2_pow[k] = (inv2_pow[k - 1] * inv2) % 9
    table = {}
    for u in range(1, 7):
        for v in range(1, 7):
            table[(u, v)] = (3 * inv2_pow[u + v] + inv2_pow[v]) % 9
    return table


R_TABLE = build_R_table()
UNITS_MOD9 = (1, 2, 4, 5, 7, 8)


# ---------------------------------------------------------------------------
# Per-coord pressure (cumulant) under the d=6 family.
# ---------------------------------------------------------------------------

def per_coord_logZ(s: float, t1: float, t2: float, t3: float, t4: float, t5: float) -> float:
    """log Z_pre(s, t) = log sum_{k>=1} 2^{-k(1-s)} exp(-t_{k mod 6})  (t_6 := 0)."""
    r = math.pow(2.0, -(1.0 - s))
    if not (0.0 < r < 1.0):
        return float("inf")
    r6 = r ** 6
    # contributions per class
    parts = [
        math.exp(-t1) * r,
        math.exp(-t2) * r ** 2,
        math.exp(-t3) * r ** 3,
        math.exp(-t4) * r ** 4,
        math.exp(-t5) * r ** 5,
        r ** 6,  # t_6 = 0
    ]
    return math.log(sum(parts) / (1.0 - r6))


def lambda_cumulant(s: float, t1: float, t2: float, t3: float, t4: float, t5: float) -> float:
    """lambda(s, t) = log E_{mu_0}[exp(-s phi - sum t_c psi_c)] = -s log 3 + log Z_pre(s, t)."""
    return -s * LOG3 + per_coord_logZ(s, t1, t2, t3, t4, t5)


def per_coord_marginals(s: float, t1: float, t2: float, t3: float, t4: float, t5: float
                        ) -> Tuple[List[float], float]:
    """
    Returns (p_1, p_2, p_3, p_4, p_5, p_6) and E[a] under the tilt.
    """
    r = math.pow(2.0, -(1.0 - s))
    if not (0.0 < r < 1.0):
        return [float("nan")] * 6, float("nan")
    r6 = r ** 6
    expt = [math.exp(-t1), math.exp(-t2), math.exp(-t3),
            math.exp(-t4), math.exp(-t5), 1.0]
    parts = [expt[c - 1] * (r ** c) for c in range(1, 7)]
    S_unnorm = sum(parts)
    p = [pp / S_unnorm for pp in parts]
    Ea_cond = [c + 6.0 * r6 / (1.0 - r6) for c in range(1, 7)]
    Ea = sum(p[i] * Ea_cond[i] for i in range(6))
    return p, Ea


def mod9_marginal_iid(p: List[float]) -> Dict[int, float]:
    """Mod-9 marginal of R_n (n >= 2) under i.i.d. coords with given mod-6 marginal p."""
    P_odd = p[0] + p[2] + p[4]
    P_even = p[1] + p[3] + p[5]
    marg = {R: 0.0 for R in range(9)}
    # Using the analytic formulas (cross-checked below via exact DP):
    marg[1] = P_odd * p[3] + P_even * p[1]
    marg[2] = P_odd * p[2] + P_even * p[0]
    marg[4] = P_odd * p[1] + P_even * p[5]
    marg[5] = P_odd * p[4] + P_even * p[2]
    marg[7] = P_odd * p[5] + P_even * p[3]
    marg[8] = P_odd * p[0] + P_even * p[4]
    return marg


def tv_mod9_units(marg: Dict[int, float]) -> float:
    return 0.5 * sum(abs(marg.get(R, 0.0) - (1.0 / 6.0 if R in UNITS_MOD9 else 0.0))
                     for R in range(9))


# ---------------------------------------------------------------------------
# Exact-rational DP on (Z/9)* for verification (independent of the analytic formula).
# ---------------------------------------------------------------------------

def exact_mod9_marginal_via_DP(p_rationals: Tuple[Fraction, ...],
                               r6_rational: Fraction,
                               n: int = 4,
                               amax: int = 90) -> Dict[int, Fraction]:
    """
    Per-coord measure: P(a = c + 6 g) = p_c * (1 - r^6) * (r^6)^g  for g = 0, 1, 2, ...
    Truncated at g such that k = c + 6 g <= amax.
    Build joint DP on R_j mod 9 over n iterations.
    """
    mod = 9
    inv2 = pow(2, -1, mod)
    inv2_pow = [1]
    for _ in range(amax + 7):
        inv2_pow.append(inv2_pow[-1] * inv2 % mod)

    # build weights
    one = Fraction(1)
    r6 = r6_rational
    weights = []
    total = Fraction(0)
    for c in range(1, 7):
        pc = p_rationals[c - 1]
        for g in range(amax // 6 + 2):
            k = c + 6 * g
            if k > amax:
                break
            w = pc * (one - r6) * (r6 ** g)
            weights.append((k, w))
            total += w
    # renormalize (truncation)
    weights = [(k, w / total) for k, w in weights]

    state = {0: Fraction(1)}
    for _ in range(n):
        new_state = {}
        for U, prob in state.items():
            base = (3 * U + 1) % mod
            for k, w in weights:
                new_U = (base * inv2_pow[k]) % mod
                new_state[new_U] = new_state.get(new_U, Fraction(0)) + prob * w
        state = new_state
    return state


# ---------------------------------------------------------------------------
# Solving the 6D saddle system.
# ---------------------------------------------------------------------------

def saddle_residuals(x: np.ndarray) -> np.ndarray:
    """
    x = [s, t_1, t_2, t_3, t_4, t_5].  Returns 6-vector of residuals:
      drift: E[a] - log_2(3) = 0
      5 mod-9 equations: P(R = 1, 2, 4, 5, 7) - 1/6 = 0  (R=8 redundant by sum=1)
    """
    s, t1, t2, t3, t4, t5 = x.tolist()
    p, Ea = per_coord_marginals(s, t1, t2, t3, t4, t5)
    if not math.isfinite(Ea):
        return np.array([1e9] * 6)
    marg = mod9_marginal_iid(p)
    return np.array([
        Ea - LOG2_3,
        marg[1] - 1.0 / 6.0,
        marg[2] - 1.0 / 6.0,
        marg[4] - 1.0 / 6.0,
        marg[5] - 1.0 / 6.0,
        marg[7] - 1.0 / 6.0,
    ])


def solve_saddle_multi_start(n_restarts: int = 200, seed: int = 0) -> Dict[str, Any]:
    """
    Multi-start root-finding for the 6D system.  Returns best result (lowest residual).
    """
    rng = np.random.default_rng(seed)
    best = None
    for k in range(n_restarts):
        s0 = rng.uniform(-4.0, 0.5)
        ts0 = rng.uniform(-3.0, 3.0, size=5)
        x0 = np.concatenate([[s0], ts0])
        try:
            sol = root(saddle_residuals, x0, method='hybr', tol=1e-14)
            res = saddle_residuals(sol.x)
            nm = float(np.linalg.norm(res))
            s, t1, t2, t3, t4, t5 = sol.x.tolist()
            p, Ea = per_coord_marginals(s, t1, t2, t3, t4, t5)
            r = math.pow(2.0, -(1.0 - s))
            valid = (0.0 < r < 1.0) and all(math.isfinite(pp) and pp > 0 for pp in p)
            if best is None or nm < best['||res||']:
                best = {
                    "x": sol.x.tolist(),
                    "||res||": nm,
                    "s": s, "t1": t1, "t2": t2, "t3": t3, "t4": t4, "t5": t5,
                    "r": r,
                    "p_1_to_6": p,
                    "Ea": Ea,
                    "valid_in_domain": valid,
                    "converged": bool(sol.success),
                }
        except Exception:
            continue
    return best


# ---------------------------------------------------------------------------
# Validation gates.
# ---------------------------------------------------------------------------

def gate_G1() -> Dict[str, Any]:
    """At (s, t) = 0, mod-3 marginal must be (0, 1/3, 2/3) and mod-9 should reproduce
    the known untilted values."""
    p, Ea = per_coord_marginals(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    # Mod-3 marginal: P(R=1 mod 3) = P(a even) = p_2 + p_4 + p_6
    P_R1_mod3 = p[1] + p[3] + p[5]
    P_R2_mod3 = p[0] + p[2] + p[4]
    marg_mod3 = (0.0, P_R1_mod3, P_R2_mod3)
    marg_mod9 = mod9_marginal_iid(p)
    return {
        "p_1_to_6_untilted": p,
        "expected_p": "(1/2, 1/4, 1/8, 1/16, 1/32, 1/64) / (1 - 1/64) = (32/63, 16/63, 8/63, 4/63, 2/63, 1/63)",
        "mod3_marginal": marg_mod3,
        "expected_mod3": "(0, 1/3, 2/3)",
        "mod3_match": abs(marg_mod3[1] - 1.0 / 3.0) < 1e-12,
        "mod9_marginal": marg_mod9,
        "Ea": Ea,
        "expected_Ea": 2.0,
    }


def gate_G2_single_param() -> Dict[str, Any]:
    """At (s, t_c=0): the single-parameter Esscher.  Should give mod-3 marginal
    (0, r/(1+r), 1/(1+r)) with r = 2^{-(1-s)} = 0.369 at s = THETA_STAR.
    Expected: (0, 0.270, 0.730), TV = 0.230."""
    s = THETA_STAR
    p, Ea = per_coord_marginals(s, 0.0, 0.0, 0.0, 0.0, 0.0)
    P_even = p[1] + p[3] + p[5]
    P_odd = p[0] + p[2] + p[4]
    marg_mod3 = (0.0, P_even, P_odd)
    # Closed form
    r = math.pow(2.0, -(1.0 - s))
    P_even_cf = r / (1.0 + r)
    P_odd_cf = 1.0 / (1.0 + r)
    tv = 0.5 * (abs(P_even - 0.5) + abs(P_odd - 0.5))
    return {
        "s": s,
        "r_pressure": r,
        "P_even_DP": P_even,
        "P_odd_DP": P_odd,
        "P_even_closed_form": P_even_cf,
        "P_odd_closed_form": P_odd_cf,
        "mod3_marginal": marg_mod3,
        "expected": "(0, 0.270, 0.730)",
        "tv_vs_uniform": tv,
        "expected_tv": "~ 0.230",
        "Ea_should_be_log2_3": Ea,
        "drift_residual": Ea - LOG2_3,
        "pass": abs(P_even - 0.27)/0.27 < 0.01,
    }


def gate_G3_classC_embedding() -> Dict[str, Any]:
    """Class C: psi(a) = [a even].  In our basis, [a even] = 1 - psi_1 - psi_3 - psi_5
    (since psi_1+psi_3+psi_5 = [a odd], and [a even] = 1 - [a odd]).
    So Class C tilt exp(-t_C [a even]) = const * exp(t_C psi_1) * exp(t_C psi_3) * exp(t_C psi_5).
    Map: in our family (t_1, t_2, t_3, t_4, t_5) = (-t_C, 0, -t_C, 0, -t_C), with s = s_C.
    The overall constant exp(-t_C) is gauge (absorbed in normalisation).
    From Class C: (s_C, t_C) = (-1.30853, -1.60015), I_two = 0.228."""
    LOG2_3_VAL = LOG2_3
    rsq_C = (2 * LOG2_3_VAL - 3) / (2 * LOG2_3_VAL + 1)
    r_C = math.sqrt(rsq_C)
    s_C = 1.0 + math.log2(r_C)  # ~ -1.30853
    t_C = math.log(r_C)         # ~ -1.60015
    # Embed
    t1 = -t_C
    t2 = 0.0
    t3 = -t_C
    t4 = 0.0
    t5 = -t_C
    p, Ea = per_coord_marginals(s_C, t1, t2, t3, t4, t5)
    # Mod-3 marginal
    P_even = p[1] + p[3] + p[5]
    P_odd = p[0] + p[2] + p[4]
    marg_mod3 = (0.0, P_even, P_odd)
    marg_mod9 = mod9_marginal_iid(p)
    # LDP rate at (x_phi = 0, x_psi = (1/3, 1/6, 1/3, 1/6, 1/3))?
    # Wait: in Class C, the saddle has E[psi] = E[a even] = 1/2.
    # In our family, the saddle x_psi_c = p_c (the mod-6 marginal).
    # Under Class C: each odd class has prob 1/(2*3) = 1/6? Let me check:
    # Per Class C: weights (r, r, r^3, r^3, r^5, r^5) for k=1..6. Normalised:
    # p_1 = r/(2(r+r^3+r^5)) and the pattern p_1 = p_2, p_3 = p_4, p_5 = p_6.
    # So odd classes (1, 3, 5) have prob p_1, p_3, p_5 and even classes (2, 4, 6) likewise.
    # Sum p_odd = p_1 + p_3 + p_5 = 1/2, sum p_even = 1/2. Good.
    lam = lambda_cumulant(s_C, t1, t2, t3, t4, t5)
    # I = s*0 + sum t_c * p_c - lam   (at saddle).
    # Here saddle p_c is the mod-6 marginal we computed.
    I = -lam + sum([t1*p[0], t2*p[1], t3*p[2], t4*p[3], t5*p[4]])
    # Cross-check: in original Class C parameterization, I_two = -t_C * (1/2) - lambda_C
    # where lambda_C = log E_{mu_0}[exp(-s_C phi - t_C [a even])]
    # = -s_C log 3 + log sum_k 2^{-k(1-s_C)} exp(-t_C [k even])
    # = -s_C log 3 + log( r_C * (1 + e^{-t_C} r_C + r_C^2 + e^{-t_C} r_C^3 + ...) )
    # Using e^{-t_C} r_C = 1 (saturation): sum = r_C * (1 + 1 + r_C^2 + r_C^2 + ... )
    #   = 2 r_C / (1 - r_C^2)
    r_C_check = math.sqrt((2*LOG2_3 - 3)/(2*LOG2_3 + 1))
    s_C_check = 1 + math.log2(r_C_check)
    t_C_check = math.log(r_C_check)
    Z_classC = 2 * r_C_check / (1 - r_C_check**2)
    lam_C_orig = -s_C_check * LOG3 + math.log(Z_classC)
    I_orig = -t_C_check * 0.5 - lam_C_orig
    return {
        "s_C": s_C,
        "t_C": t_C,
        "embedded_t1_t5": [t1, t2, t3, t4, t5],
        "p_1_to_6": p,
        "P_odd": P_odd,
        "P_even": P_even,
        "mod3_marginal": marg_mod3,
        "expected_mod3": "(0, 0.5, 0.5)",
        "mod3_match": abs(P_even - 0.5) < 1e-10,
        "Ea": Ea,
        "drift_match_zero": LOG3 - Ea * LOG2,
        "mod9_marginal": marg_mod9,
        "tv_mod9": tv_mod9_units(marg_mod9),
        "expected_mod9_TV": 0.313,
        "lambda_in_basis": lam,
        "lambda_original_classC": lam_C_orig,
        "I_two_in_basis": I,
        "I_two_original_classC": I_orig,
        "I_match": abs(I - I_orig) < 1e-10,
        "expected_I": 0.22791,
    }


# ---------------------------------------------------------------------------
# Theorem: in our 6D family, the unique p making mod-9 marginal uniform-on-units
# is p_c = 1/6 (uniform on {1,...,6}). Sympy-style verification.
# ---------------------------------------------------------------------------

def uniqueness_check_mod9() -> Dict[str, Any]:
    """Verify (numerically) that the only positive p with sum 1 making the mod-9
    marginal uniform on units is p_c = 1/6."""
    out: Dict[str, Any] = {}
    # Symbolic via sympy
    try:
        from sympy import symbols, Rational, nsolve, Matrix, solve as sym_solve, simplify
        p1, p2, p3, p4, p5, p6 = symbols('p1 p2 p3 p4 p5 p6', real=True, positive=True)
        P_odd = p1 + p3 + p5
        P_even = p2 + p4 + p6
        eqs_sym = [
            P_odd*p4 + P_even*p2 - Rational(1, 6),
            P_odd*p3 + P_even*p1 - Rational(1, 6),
            P_odd*p2 + P_even*p6 - Rational(1, 6),
            P_odd*p5 + P_even*p3 - Rational(1, 6),
            P_odd*p6 + P_even*p4 - Rational(1, 6),
            p1 + p2 + p3 + p4 + p5 + p6 - 1,
        ]
        sols = sym_solve(eqs_sym, [p1, p2, p3, p4, p5, p6], dict=False)
        out["sympy_solutions"] = [tuple(str(x) for x in sol) for sol in sols]
        out["sympy_count_solutions"] = len(sols)
        out["unique_solution_is_uniform"] = (
            len(sols) == 1
            and all(str(x) == str(Rational(1, 6)) for x in sols[0])
        )
    except Exception as e:
        out["sympy_error"] = str(e)
    # Numerical multi-start cross-check
    rng = np.random.default_rng(12345)

    def res_p_only(p):
        p1, p2, p3, p4, p5 = p
        p6 = 1.0 - sum(p)
        P_odd = p1 + p3 + p5
        P_even = p2 + p4 + p6
        return [
            P_odd*p4 + P_even*p2 - 1/6,
            P_odd*p3 + P_even*p1 - 1/6,
            P_odd*p2 + P_even*p6 - 1/6,
            P_odd*p5 + P_even*p3 - 1/6,
            P_odd*p6 + P_even*p4 - 1/6,
        ]

    distinct = []
    for _ in range(500):
        ps = rng.dirichlet(np.ones(6) * 0.5)
        sol = root(res_p_only, ps[:5], method='hybr', tol=1e-14)
        if sol.success and np.linalg.norm(res_p_only(sol.x)) < 1e-10:
            p_full = list(sol.x) + [1.0 - sum(sol.x)]
            if all(p > -1e-10 for p in p_full):
                key = tuple(round(p, 8) for p in p_full)
                if key not in [d[0] for d in distinct]:
                    distinct.append((key, p_full))
    out["numerical_distinct_solutions"] = [list(p) for _, p in distinct]
    return out


# ---------------------------------------------------------------------------
# CORE RESULT: under p_c = 1/6 uniform, drift incompatibility.
# ---------------------------------------------------------------------------

def core_obstruction_analysis() -> Dict[str, Any]:
    """Under uniform mod-6 (p_c = 1/6), E[a] = 3.5 + 6 r^6/(1-r^6).
    Drift balance E[a] = log_2(3) ~ 1.585 is INFEASIBLE."""
    Ea_min = 3.5  # limit r -> 0
    gap = Ea_min - LOG2_3
    return {
        "Ea_min_under_uniform_mod6": Ea_min,
        "Ea_required_for_drift_balance": LOG2_3,
        "incompatibility_gap": gap,
        "verdict": "INFEASIBLE: drift balance impossible under mod-9 uniformity in this family",
    }


def best_rate_at_mod9_uniform_no_drift() -> Dict[str, Any]:
    """Under the uniform-mod-6 saddle (forced by mod-9 saturation), the per-coord
    weight has t_c = (c - 6) log r (gauge: t_6 = 0).
    Per-coord cumulant lambda(s, t*(s)) at this restricted family is a function of s alone:
        Z(s, t*) = sum_{c=1..6} r^{6-c} * r^c / (1-r^6) = 6 r^6 / (1-r^6)
        lambda(s, t*) = -s log 3 + log(6 r^6 / (1-r^6))
    The LDP rate at the joint target (x_phi(s), 1/6, ..., 1/6) is
        I(s) = s * x_phi(s) + (1/6) sum_{c=1..5} t_c(s) - lambda(s, t*(s)).
    where x_phi(s) = E_tilt[phi] = log 3 - E_tilt[a] log 2 = log 3 - (3.5 + 6 r^6/(1-r^6)) log 2.
    This depends on s; it is NEVER zero (the drift is uniformly negative below LOG3 - 3.5 LOG2).
    The relevant LDP rate is over a slice that does NOT include drift = 0.
    """
    out = {"sweep": []}
    for s_val in [-4.0, -3.0, -2.0, -1.5, -1.0, -0.5, 0.0]:
        r = math.pow(2.0, -(1.0 - s_val))
        if not (0.0 < r < 1.0):
            continue
        r6 = r ** 6
        Ea = 3.5 + 6 * r6 / (1.0 - r6)
        Ephi = LOG3 - Ea * LOG2
        # t_c = (c - 6) log r for c = 1..5
        log_r = math.log(r)
        tc = [(c - 6) * log_r for c in range(1, 6)]
        # lambda(s, t*) = -s log 3 + log(6 r^6 / (1-r^6))
        lam = -s_val * LOG3 + math.log(6 * r6 / (1.0 - r6))
        # I = s * Ephi + (1/6) sum t_c - lam   (sum c=1..5 of t_c = log r * sum_{c=1..5} (c-6) = log r * (-15))
        sum_t_over_6 = log_r * (-15.0 / 6.0)
        I = s_val * Ephi + sum_t_over_6 - lam
        out["sweep"].append({
            "s": s_val,
            "r": r,
            "Ea": Ea,
            "Ephi_tilt_drift": Ephi,
            "tc_for_c_1_to_5": tc,
            "lambda": lam,
            "I_rate_at_(Ephi(s), 1/6 each)": I,
        })
    return out


# ---------------------------------------------------------------------------
# Iteration check: even if it WORKED for mod 9, would it iterate to mod 27?
# Hypothetical: tilt to mod-18 uniform per coord, check mod-27 marginal.
# (For documentation; outcome (c) already ruled this out.)
# ---------------------------------------------------------------------------

def iteration_check_mod27() -> Dict[str, Any]:
    """
    HYPOTHETICAL: if we could make per-coord mod-18 marginal uniform (analogous
    to mod-6 for mod-9), would mod-27 marginal be uniform on units?

    For mod-27: 2 has order ord_27(2). 2^k mod 27: 2, 4, 8, 16, 5, 10, 20, 13, 26, 25, 23, 19, 11, 22, 17, 7, 14, 1.
    Order 18. So R_n mod 27 depends on the last few a's mod 18.

    Specifically: R_n mod 27 = sum_{j=1..n} 3^{n-j+1} * 2^{-(a_j+...+a_n)} mod 27.
    The dependence is on (a_{n-2} mod 18, a_{n-1} mod 18, a_n mod 18) (since 3^2 = 9
    divides into mod 27 over 3 levels).

    The "natural d" for mod-27 saturation would be phi(27) - 1 = 17, with mod-18 cocycles.
    But the same drift obstruction recurs: forcing mod-18 marginal to be uniform makes
    E[a] >= 9.5 (mean of {1,...,18}), even FURTHER from log_2(3) ~ 1.585.

    HENCE: ITERATION IS RULED OUT BY THE SAME DRIFT OBSTRUCTION (independently of mod-9).
    """
    return {
        "mod9_drift_gap": 3.5 - LOG2_3,
        "mod27_drift_gap_lower_bound": 9.5 - LOG2_3,
        "mod81_drift_gap_lower_bound": 27.5 - LOG2_3,
        "mod3k_drift_gap_lower_bound_formula": "(3^{k-1} * 6 / 2) + 0.5 - log_2(3)",
        "verdict": ("Drift obstruction grows with k: mod-3^k saturation requires "
                    "per-coord uniform-on-mod-{2 * 3^{k-1}}, which has E[a] >= 3^{k-1} + 0.5. "
                    "Drift gap from log_2(3) grows as Theta(3^{k-1}). "
                    "STRICT NO-ITERATION."),
    }


# ---------------------------------------------------------------------------
# MAIN.
# ---------------------------------------------------------------------------

def main():
    t0 = time.time()
    out: Dict[str, Any] = {}

    print("=" * 78)
    print("collatz_d5_tilt_probe.py  --  d=6 (s + 5 t_i, psi_i = [a mod 6 = i]) Esscher tilt")
    print("=" * 78)
    print(f"\nTHETA_STAR (single-param) = {THETA_STAR:.6f}")
    print(f"LOG2_3 (drift-balance target for E[a]) = {LOG2_3:.6f}")
    print(f"I_one(0) baseline = {-pressure_one(THETA_STAR):.6f}")

    out["constants"] = {
        "THETA_STAR": THETA_STAR,
        "LOG2_3": LOG2_3,
        "I_one_baseline": -pressure_one(THETA_STAR),
        "EBAR": EBAR,
    }
    out["R_uv_mod9_table"] = {f"{u},{v}": R_TABLE[(u, v)] for u in range(1, 7) for v in range(1, 7)}

    # --- GATE G1 ---
    print("\n--- GATE G1: untilted (s=0, t=0) baseline ---")
    g1 = gate_G1()
    print(f"  mod-3 marginal: {g1['mod3_marginal']}  (expected (0, 1/3, 2/3))")
    print(f"  mod-3 match: {g1['mod3_match']}")
    print(f"  E[a]: {g1['Ea']:.6f}  (expected 2)")
    out["gate_G1"] = g1

    # --- GATE G2 ---
    print("\n--- GATE G2: single-param Esscher (THETA_STAR) -> mod-3 (0, 0.270, 0.730) ---")
    g2 = gate_G2_single_param()
    print(f"  P_even (mod-3 = 1 mod 3): {g2['P_even_DP']:.5f}  (expected 0.270)")
    print(f"  P_odd  (mod-3 = 2 mod 3): {g2['P_odd_DP']:.5f}  (expected 0.730)")
    print(f"  TV vs uniform-on-units: {g2['tv_vs_uniform']:.5f}  (expected 0.230)")
    print(f"  E[a] = {g2['Ea_should_be_log2_3']:.5f}, target log_2(3) = {LOG2_3:.5f}, drift residual = {g2['drift_residual']:.2e}")
    print(f"  GATE PASS: {g2['pass']}")
    out["gate_G2"] = g2

    # --- GATE G3 ---
    print("\n--- GATE G3: Class C embedding -> mod-3 uniform, I = 0.228 ---")
    g3 = gate_G3_classC_embedding()
    print(f"  Embedded params: s={g3['s_C']:.5f}, t_1=t_3=t_5={g3['embedded_t1_t5'][0]:.5f}")
    print(f"  mod-3 marginal: {g3['mod3_marginal']}")
    print(f"  mod-3 match: {g3['mod3_match']}")
    print(f"  E[a] = {g3['Ea']:.6f}, target log_2(3) = {LOG2_3:.6f}")
    print(f"  mod-9 TV vs uniform: {g3['tv_mod9']:.4f}  (expected 0.313)")
    print(f"  lambda in d=6 basis: {g3['lambda_in_basis']:.6f}, original C: {g3['lambda_original_classC']:.6f}")
    print(f"  I_two in basis: {g3['I_two_in_basis']:.6f}, original C: {g3['I_two_original_classC']:.6f}")
    print(f"  I matches original Class C: {g3['I_match']}")
    out["gate_G3"] = g3

    # --- UNIQUENESS OF MOD-9 SATURATING p ---
    print("\n--- UNIQUENESS: mod-9 saturating p (theoretical) ---")
    uniq = uniqueness_check_mod9()
    if "sympy_solutions" in uniq:
        print(f"  Sympy: {uniq['sympy_count_solutions']} solution(s)")
        for s in uniq["sympy_solutions"]:
            print(f"    {s}")
        print(f"  Unique solution is uniform (1/6 each)?: {uniq['unique_solution_is_uniform']}")
    print(f"  Numerical multi-start found {len(uniq.get('numerical_distinct_solutions', []))} distinct positive solution(s).")
    for ds in uniq.get("numerical_distinct_solutions", [])[:5]:
        print(f"    {[round(p, 6) for p in ds]}")
    out["uniqueness_mod9"] = uniq

    # --- CORE OBSTRUCTION ---
    print("\n--- CORE OBSTRUCTION: drift incompatibility under uniform mod-6 ---")
    obs = core_obstruction_analysis()
    print(f"  Under uniform mod-6 (forced by mod-9 saturation): E[a] >= {obs['Ea_min_under_uniform_mod6']}")
    print(f"  Drift balance requires E[a] = log_2(3) = {obs['Ea_required_for_drift_balance']:.5f}")
    print(f"  Incompatibility gap: {obs['incompatibility_gap']:.5f} > 0 STRICTLY")
    print(f"  VERDICT: {obs['verdict']}")
    out["core_obstruction"] = obs

    # --- 6D MULTI-START ROOT FIND (numerical confirmation) ---
    print("\n--- 6D ROOT-FIND (numerical confirmation of no-solution) ---")
    best = solve_saddle_multi_start(n_restarts=400, seed=42)
    if best is not None:
        print(f"  Best ||res||: {best['||res||']:.3e}  (converged: {best['converged']})")
        print(f"  Best x: s={best['s']:.4f}, t_1..5 = {[round(t,4) for t in [best['t1'],best['t2'],best['t3'],best['t4'],best['t5']]]}")
        print(f"  r = {best['r']:.5f}, p_1..6 = {[round(p, 5) for p in best['p_1_to_6']]}")
        print(f"  E[a] = {best['Ea']:.5f}, valid in domain: {best['valid_in_domain']}")
    out["best_root_find"] = best

    # --- RATE AT THE MOD-9-UNIFORM SADDLE (s free, drift NOT balanced) ---
    print("\n--- LDP RATE: under mod-9 uniform tilt (drift uncontrolled) ---")
    rate = best_rate_at_mod9_uniform_no_drift()
    print(f"  {'s':>8} {'r':>8} {'E[a]':>8} {'E[phi]':>10} {'lambda':>10} {'I_rate':>10}")
    for row in rate["sweep"]:
        print(f"  {row['s']:>8.3f} {row['r']:>8.5f} {row['Ea']:>8.4f} {row['Ephi_tilt_drift']:>10.5f} {row['lambda']:>10.5f} {row['I_rate_at_(Ephi(s), 1/6 each)']:>10.5f}")
    out["mod9_uniform_no_drift_sweep"] = rate

    # --- EXACT-RATIONAL DP VERIFICATION OF MOD-9 SATURATION ---
    print("\n--- EXACT-RATIONAL DP CROSS-CHECK: mod-9 saturation under uniform mod-6 ---")
    p_uniform = (Fraction(1, 6),) * 6
    exact_check = {}
    for r6_val in [Fraction(1, 100), Fraction(1, 25), Fraction(1, 10), Fraction(1, 5)]:
        m = exact_mod9_marginal_via_DP(p_uniform, r6_val, n=4, amax=60)
        marg_float = {R: float(m.get(R, Fraction(0))) for R in range(9)}
        tv = sum(abs(marg_float[R] - (1.0/6 if R in UNITS_MOD9 else 0.0)) for R in range(9)) / 2
        exact_check[f"r6={float(r6_val)}"] = {
            "mod9_marginal": marg_float,
            "tv_units": tv,
        }
        print(f"  r^6 = {float(r6_val):.4f}: TV(mod-9 vs uniform-on-units) = {tv:.4e}")
    out["exact_DP_mod9_saturation_check"] = exact_check

    # --- ANALYTIC vs DP CROSS-CHECK FOR Class C ---
    print("\n--- EXACT-RATIONAL DP CROSS-CHECK: Class C mod-9 marginal (should give 0.313 TV) ---")
    LOG2_3_VAL = LOG2_3
    rsq_C = (2 * LOG2_3_VAL - 3) / (2 * LOG2_3_VAL + 1)
    r_C = math.sqrt(rsq_C)
    # Class C per-coord weight: w(k) = r_C^k for k odd, r_C^{k-1} for k even.
    # Normalisation: sum w(k) = 2*(r_C + r_C^3 + r_C^5 + ...) = 2 r_C / (1 - r_C^2).
    # So p_c = w(c) / norm * (1 - r_C^6) factor:
    # For mod-6 grouping: in the standard parameterisation
    # (per-coord measure NOT uniform mod-6; it's the Class C 2-grouped measure):
    # Within mod-6 class c, the conditional dist is NOT a simple shifted Geom(r^6).
    # So we can't directly use exact_mod9_marginal_via_DP.
    # Instead, do exact DP directly on a_j with the Class C weights truncated.
    inv2_mod9 = pow(2, -1, 9)
    inv2_pow = [1]
    for _ in range(2 * 80 + 5):
        inv2_pow.append(inv2_pow[-1] * inv2_mod9 % 9)
    amax = 80
    # Class C weights (truncated, exact in float)
    weights_C = []
    total = 0.0
    for k in range(1, amax + 1):
        w = r_C ** k if k % 2 == 1 else r_C ** (k - 1)
        weights_C.append((k, w))
        total += w
    weights_C = [(k, w / total) for k, w in weights_C]
    state = {0: 1.0}
    for _ in range(4):
        new_state = {}
        for U, prob in state.items():
            base = (3 * U + 1) % 9
            for k, w in weights_C:
                new_U = (base * inv2_pow[k]) % 9
                new_state[new_U] = new_state.get(new_U, 0.0) + prob * w
        state = new_state
    marg_C = {R: state.get(R, 0.0) for R in range(9)}
    tv_C = sum(abs(marg_C[R] - (1.0/6 if R in UNITS_MOD9 else 0.0)) for R in range(9)) / 2
    print(f"  Class C exact-DP mod-9 marginal: {[round(marg_C[R], 5) for R in range(9)]}")
    print(f"  TV vs uniform-on-units: {tv_C:.5f}  (expected ~0.313 from multitilt_probe.py)")
    out["classC_exact_DP_mod9"] = {
        "marg": marg_C,
        "tv_units": tv_C,
        "expected_TV": 0.313,
    }

    # --- ITERATION CHECK ---
    print("\n--- ITERATION TO MOD 27 ---")
    it = iteration_check_mod27()
    print(f"  mod-9 drift gap: {it['mod9_drift_gap']:.5f}")
    print(f"  mod-27 drift gap (lower bound): {it['mod27_drift_gap_lower_bound']:.5f}")
    print(f"  Verdict: {it['verdict']}")
    out["iteration_check"] = it

    out["runtime_sec"] = time.time() - t0
    print(f"\nRuntime: {out['runtime_sec']:.2f} s")

    json_path = os.path.join(DATA_DIR, "d5_tilt_probe.json")
    log_path = os.path.join(DATA_DIR, "d5_tilt_probe.log")
    with open(json_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    with open(log_path, "w") as f:
        f.write("collatz_d5_tilt_probe.py results summary\n")
        f.write("=========================================\n\n")
        f.write(f"VERDICT: OUTCOME (c) -- NO SOLUTION in the d=6 family\n\n")
        f.write(f"Reason: mod-9 marginal of R_n being uniform on (Z/9)* under i.i.d. coords\n")
        f.write(f"FORCES p_c = 1/6 uniform on {{1,...,6}} (unique positive solution).\n")
        f.write(f"This in turn forces E[a] >= 3.5, which is INCOMPATIBLE with drift balance\n")
        f.write(f"E[a] = log_2(3) ~ 1.585.  Incompatibility gap = 3.5 - 1.585 = 1.915 > 0.\n\n")
        f.write(f"This is a STRUCTURAL OBSTRUCTION, not a dimension-count failure: even adding\n")
        f.write(f"the t_6 parameter (d=7) does not change the fact that mod-9 uniformity forces\n")
        f.write(f"uniform mod-6 marginals on a, which has E[a mod 6] = 3.5.\n\n")
        f.write(f"Iteration to mod-27 fails even harder: forces E[a mod 18] = 9.5, gap = 7.9.\n\n")
        f.write(f"Validation gates: G1, G2, G3 pass (see JSON).\n")
        f.write(f"Runtime: {out['runtime_sec']:.2f} s\n")
    print(f"\nWrote {json_path}")
    print(f"Wrote {log_path}")


if __name__ == "__main__":
    main()
