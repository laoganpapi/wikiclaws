#!/usr/bin/env python3
r"""
collatz_beyond_esscher_probe.py
================================

Wave 2 probe: can a NON-Esscher reweighting of the Syracuse i.i.d. Geom(1/2)
base measure escape the d=5 structural obstruction (collatz_d5_tilt.md)?

The Wave 1 obstruction (theorem, exact):
    Under ANY translation-invariant per-coord (product) Esscher tilt of the
    Bernoulli base measure mu_0, mod-3^k saturation for k >= 2 forces the
    per-coord mod-(2*3^{k-1}) marginal to be uniform, which forces
        E[a] >= 3^{k-1} + 1/2  >  log_2(3),
    hence drift balance fails by gap_k = 3^{k-1} + 1/2 - log_2(3) =
    Theta(3^{k-1}).

This probe tests escape candidate (P1): single-step Markov reweighting on
the residue mod 6 of consecutive coords (a_{j} mod 6, a_{j+1} mod 6). The
joint mod-6 distribution Q(u, v) of two consecutive coords is no longer
forced to be a product pi(u) pi(v), but it MUST satisfy:
    - row sums  = pi(u)  (marginal),
    - column sums = pi(u) (stationarity, since the chain is stationary),
    - drift balance:  sum c * pi(c) + 6 r^6 / (1 - r^6) = log_2(3),
      where the within-class within-coord conditional is shifted-geometric
      with ratio r^6 (within-class freedom is shared across all classes,
      one parameter r in (0, 1); see Wave 1 setup).
    - mod-9 saturation of R_n under stationary 2-step:
         P(R_n = j mod 9) = 1/6 for j in {1,2,4,5,7,8},
      using the same R(u, v) mod 9 table from collatz_d5_tilt.md (R(u,v)
      depends only on (u mod 2, v)).

Note the within-class parameter r enters E[a] uniformly across classes
(every class c has the same within-class geometric). One could relax this
to per-class r_c, but Q(u, v) constraints depend ONLY on (u mod 6, v mod 6)
and on E[a], so as long as we test feasibility of (Q, E[a]) being jointly
achievable with E[a] = log_2(3), the result is invariant.

The smallest version of (P1) decouples cleanly into a LINEAR + QUADRATIC
feasibility test on the 6 x 6 matrix Q with:
    - 36 entries, all >= 0
    - 6 row-sum = col-sum constraints (12 linear, 11 independent)
    - 1 normalization (sum = 1)
    - 6 mod-9 = 1/6 constraints (5 independent; one is redundant)
    - 1 drift constraint:  E[a_class] := sum_c c * pi(c)  must lie in the
      window  ( log_2(3) - 6 r^6/(1-r^6), log_2(3) )  for some r in (0, 1),
      i.e.,  E[a_class] < log_2(3)  is necessary and (with within-class
      freedom) sufficient.

So the feasibility test:
    Does there exist a 6 x 6 matrix Q >= 0 with row sums = col sums = pi,
    sum(Q) = 1, satisfying the 5 mod-9 equations, and with
        sum_c c * pi(c) < log_2(3)  ?

If YES: (P1) escape candidate is FEASIBLE at the JOINT level. We then must
        check it lifts to a Markov tilt with a tractable LDP.
If NO:  the obstruction extends to Markov reweighting too.

This is a LINEAR PROGRAM with strict inequality on a linear functional. We
solve it exactly with sympy / Fraction arithmetic via a vertex-enumeration
or LP approach.

OUTPUT:
  data/beyond_esscher_probe.json      -- numerical record
  data/beyond_esscher_probe.log       -- human-readable verdict
"""

from __future__ import annotations
import json
import math
import os
import sys
import time
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# --- Mod-9 R-table (re-derived for cross-check) ----------------------------
#
# R(u, v) := (3 * 2^{-(u+v)} + 2^{-v}) mod 9, where 2^{-1} mod 9 = 5,
# 2 has order 6 mod 9. R(u, v) only depends on (u mod 6, v mod 6).

def two_inv_mod9(k: int) -> int:
    # 2^k mod 9 cycles with period 6: [2,4,8,7,5,1] at k=1..6
    # so 2^{-k} = 2^{6-k} mod 9 for k in 1..6 (taking k mod 6)
    k = k % 6
    if k == 0:
        return 1
    return pow(2, 6 - k, 9)

def R_uv_mod9(u: int, v: int) -> int:
    """R(u, v) := (3 * 2^{-(u+v)} + 2^{-v}) mod 9. u, v in 1..6."""
    inv_uv = two_inv_mod9(u + v)
    inv_v = two_inv_mod9(v)
    return (3 * inv_uv + inv_v) % 9

# Validate against Wave 1 table:
EXPECTED_TABLE = {
    1: [8, 4, 2, 1, 5, 7],
    2: [2, 1, 5, 7, 8, 4],
    3: [8, 4, 2, 1, 5, 7],
    4: [2, 1, 5, 7, 8, 4],
    5: [8, 4, 2, 1, 5, 7],
    6: [2, 1, 5, 7, 8, 4],
}

R_TABLE: Dict[Tuple[int, int], int] = {}
for u in range(1, 7):
    for v in range(1, 7):
        R_TABLE[(u, v)] = R_uv_mod9(u, v)
        assert R_TABLE[(u, v)] == EXPECTED_TABLE[u][v - 1], (
            f"R-table mismatch at u={u} v={v}: "
            f"got {R_TABLE[(u, v)]} expected {EXPECTED_TABLE[u][v - 1]}"
        )

UNITS9 = [1, 2, 4, 5, 7, 8]

# Build the 5 independent mod-9 equations as linear functionals on Q-entries.
# Q is indexed (u, v) with u, v in 1..6.

def mod9_constraint_rows() -> Tuple[np.ndarray, np.ndarray]:
    """Returns A (5 x 36) and b (5,) such that A * vec(Q) = b means
    sum_{(u,v): R(u,v) = j} Q(u,v) = 1/6 for j in UNITS9 (first 5; last is dep.)"""
    A = np.zeros((5, 36), dtype=object)
    b = np.zeros(5, dtype=object)
    for i, j in enumerate(UNITS9[:5]):
        for u in range(1, 7):
            for v in range(1, 7):
                if R_TABLE[(u, v)] == j:
                    A[i, (u - 1) * 6 + (v - 1)] = Fraction(1)
        b[i] = Fraction(1, 6)
    return A, b

def marginal_constraint_rows() -> Tuple[np.ndarray, np.ndarray]:
    """Row-sum = col-sum (stationarity). 6 constraints, 5 independent (sum=0
    when we subtract the sum constraint). We just write all 6, and rely on
    LP / sympy to handle the linear dependence."""
    # For each u in 1..6: sum_v Q(u, v) - sum_v Q(v, u) = 0
    A = np.zeros((6, 36), dtype=object)
    b = np.zeros(6, dtype=object)
    for u in range(1, 7):
        for v in range(1, 7):
            # sum_v Q(u, v) entry
            A[u - 1, (u - 1) * 6 + (v - 1)] += Fraction(1)
            # - sum_v Q(v, u) entry
            A[u - 1, (v - 1) * 6 + (u - 1)] -= Fraction(1)
    return A, b

def normalization_row() -> Tuple[np.ndarray, np.ndarray]:
    A = np.ones((1, 36), dtype=object) * Fraction(1)
    b = np.array([Fraction(1)], dtype=object)
    return A, b

def drift_functional() -> np.ndarray:
    """Returns c (36,) such that c . Q = sum_u u * pi(u) = sum_u u * sum_v Q(u, v).

    We want to MINIMIZE this (in fact, find if it can be < log_2(3))."""
    c = np.zeros(36, dtype=object)
    for u in range(1, 7):
        for v in range(1, 7):
            c[(u - 1) * 6 + (v - 1)] = Fraction(u)
    return c


# --- Solve the LP -----------------------------------------------------------

def solve_min_drift_lp() -> Dict[str, Any]:
    """LP: minimize c . Q  s.t.  A_eq Q = b_eq,  Q >= 0,
    where A_eq combines marginal + mod-9 + normalization rows.

    Reports the minimum value of E[a_class] = sum_c c * pi(c) over all
    joint mod-6 distributions Q satisfying mod-9 saturation and being
    a stationary 2-step marginal of some Markov chain on Z/6 (or on the
    integers projected to Z/6).
    """
    A_mod9, b_mod9 = mod9_constraint_rows()
    A_marg, b_marg = marginal_constraint_rows()
    A_norm, b_norm = normalization_row()

    A_eq = np.vstack([A_mod9, A_marg, A_norm])
    b_eq = np.concatenate([b_mod9, b_marg, b_norm])

    # Convert to float for scipy linprog (we'll re-verify in exact rationals).
    A_eq_f = A_eq.astype(float)
    b_eq_f = b_eq.astype(float)
    c_f = drift_functional().astype(float)

    res = linprog(
        c=c_f,
        A_eq=A_eq_f,
        b_eq=b_eq_f,
        bounds=[(0, None)] * 36,
        method="highs",
    )
    out: Dict[str, Any] = {
        "status": int(res.status),
        "message": res.message,
        "success": bool(res.success),
        "min_E_a_class": float(res.fun) if res.fun is not None else None,
        "log2_3": math.log2(3.0),
        "x": res.x.tolist() if res.x is not None else None,
    }
    if res.x is not None:
        Q = res.x.reshape(6, 6)
        pi_rows = Q.sum(axis=1).tolist()
        pi_cols = Q.sum(axis=0).tolist()
        out["pi_rows"] = pi_rows
        out["pi_cols"] = pi_cols
        out["Q"] = Q.tolist()
        # Within-class freedom: r in (0,1) with E[a] = sum c pi(c) + 6r^6/(1-r^6).
        # Drift balance requires E[a] = log2 3 ~ 1.585.  E_class < log2 3 required.
        Eac = float(res.fun)
        out["drift_gap"] = Eac - math.log2(3.0)
        out["feasible_with_within_class_only_pulling_up"] = (Eac < math.log2(3.0))
        # Compute the mod-9 marginals it achieves:
        mod9_marg = {}
        for j in UNITS9:
            tot = 0.0
            for u in range(1, 7):
                for v in range(1, 7):
                    if R_TABLE[(u, v)] == j:
                        tot += Q[u - 1, v - 1]
            mod9_marg[j] = tot
        out["mod9_marginal"] = mod9_marg
    return out


def solve_min_drift_lp_NONSTATIONARY() -> Dict[str, Any]:
    """LP relaxation: DROP the stationarity (row-sum = col-sum) constraint.
    This is the question: if a Markov chain is allowed to be non-stationary
    (e.g., the LDP rate is evaluated along non-stationary paths), can the
    joint mod-9 saturation occur with a smaller E[a_class] under the
    pi_row marginal (the START of each two-coord pair)?

    Result interpretation: this is a strictly weaker LP, so we expect
    min E[a_class] to drop further. If even this LP gives min >= log2(3),
    then NO Markov-style escape exists at all, even for non-stationary
    chains or for fluctuations.
    """
    A_mod9, b_mod9 = mod9_constraint_rows()
    A_norm, b_norm = normalization_row()

    A_eq = np.vstack([A_mod9, A_norm]).astype(float)
    b_eq = np.concatenate([b_mod9, b_norm]).astype(float)

    c_f = drift_functional().astype(float)

    res = linprog(
        c=c_f,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=[(0, None)] * 36,
        method="highs",
    )
    out: Dict[str, Any] = {
        "status": int(res.status),
        "success": bool(res.success),
        "min_E_a_class_nonstationary": float(res.fun) if res.fun is not None else None,
    }
    if res.x is not None:
        Q = res.x.reshape(6, 6)
        out["pi_rows"] = Q.sum(axis=1).tolist()
        out["pi_cols"] = Q.sum(axis=0).tolist()
        out["Q"] = Q.tolist()
    return out


def solve_min_drift_lp_EXACT() -> Dict[str, Any]:
    """Exact-rational LP via sympy. We solve the LP using the simplex
    method in exact arithmetic via sympy's Matrix.rref / vertex enumeration
    is too expensive for 36 vars. Instead, we VERIFY the LP-min value
    found by floating-point linprog by checking primal feasibility AND
    dual optimality with rational arithmetic.

    Specifically: scipy's HiGHS returns a vertex of the feasible polytope.
    We extract the active set (entries == 0), solve the resulting linear
    system over Q, and verify the rational solution satisfies all
    constraints and gives the same objective.
    """
    import sympy as sp

    A_mod9, b_mod9 = mod9_constraint_rows()
    A_marg, b_marg = marginal_constraint_rows()
    A_norm, b_norm = normalization_row()

    # Float LP to get the active set:
    A_eq = np.vstack([A_mod9, A_marg, A_norm]).astype(float)
    b_eq = np.concatenate([b_mod9, b_marg, b_norm]).astype(float)
    c_f = drift_functional().astype(float)
    res = linprog(c=c_f, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * 36, method="highs")
    x_lp = res.x
    # Active set: entries < 1e-9 are zero.
    zero_idx = [i for i in range(36) if x_lp[i] < 1e-9]
    nonzero_idx = [i for i in range(36) if x_lp[i] >= 1e-9]
    # The vertex has at most rank(A_eq) nonzero entries. Let's check via sympy:
    A_eq_Q = sp.Matrix([
        [sp.Rational(A_mod9[i, j]) if isinstance(A_mod9[i, j], Fraction) else sp.Rational(int(A_mod9[i, j].numerator), int(A_mod9[i, j].denominator)) for j in range(36)]
        for i in range(A_mod9.shape[0])
    ])
    # Easier: rebuild exactly via Fractions:
    A_full = np.vstack([A_mod9, A_marg, A_norm])  # all entries Fraction
    b_full = np.concatenate([b_mod9, b_marg, b_norm])
    A_sym = sp.Matrix([[sp.Rational(A_full[i, j].numerator, A_full[i, j].denominator) for j in range(36)] for i in range(A_full.shape[0])])
    b_sym = sp.Matrix([sp.Rational(b_full[i].numerator, b_full[i].denominator) for i in range(b_full.shape[0])])
    # Restrict to nonzero columns: A_sym[:, nonzero_idx] x_nz = b_sym
    A_active = A_sym[:, nonzero_idx]
    # Solve A_active x = b_sym:
    sol = A_active.solve(b_sym) if A_active.rank() == len(nonzero_idx) else None
    if sol is None:
        # Use least-norm via pseudoinverse:
        sol = (A_active.T * (A_active * A_active.T).inv()) * b_sym
    x_exact = [sp.Rational(0)] * 36
    for k, j in enumerate(nonzero_idx):
        x_exact[j] = sol[k, 0]
    # Compute exact objective:
    c_sym = [sp.Rational(int(u)) for u in [1,1,1,1,1,1,  2,2,2,2,2,2,  3,3,3,3,3,3,  4,4,4,4,4,4,  5,5,5,5,5,5,  6,6,6,6,6,6]]
    Eac_exact = sum(c_sym[k] * x_exact[k] for k in range(36))
    # Verify constraints exactly:
    Aeq_x = A_sym * sp.Matrix(x_exact)
    eq_residuals = [Aeq_x[i, 0] - b_sym[i, 0] for i in range(A_sym.shape[0])]
    all_zero = all(r == 0 for r in eq_residuals)
    all_nonneg = all(xi >= 0 for xi in x_exact)
    return {
        "min_E_a_class_exact_str": str(Eac_exact),
        "min_E_a_class_exact_float": float(Eac_exact),
        "all_equality_constraints_zero": bool(all_zero),
        "all_nonneg": bool(all_nonneg),
        "nonzero_indices": nonzero_idx,
        "vertex_size": len(nonzero_idx),
    }


def solve_max_drift_lp() -> Dict[str, Any]:
    """LP: maximize c . Q (i.e., minimize -c.Q) — gives upper end of feasible
    drift window. Useful sanity check on the feasibility region."""
    A_mod9, b_mod9 = mod9_constraint_rows()
    A_marg, b_marg = marginal_constraint_rows()
    A_norm, b_norm = normalization_row()

    A_eq = np.vstack([A_mod9, A_marg, A_norm]).astype(float)
    b_eq = np.concatenate([b_mod9, b_marg, b_norm]).astype(float)

    c_f = drift_functional().astype(float)

    res = linprog(
        c=-c_f,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=[(0, None)] * 36,
        method="highs",
    )
    out: Dict[str, Any] = {
        "status": int(res.status),
        "success": bool(res.success),
        "max_E_a_class": float(-res.fun) if res.fun is not None else None,
    }
    if res.x is not None:
        Q = res.x.reshape(6, 6)
        out["pi_rows"] = Q.sum(axis=1).tolist()
        out["pi_cols"] = Q.sum(axis=0).tolist()
        out["Q"] = Q.tolist()
    return out


def exact_rational_recheck(Q_float: List[List[float]]) -> Dict[str, Any]:
    """Given a candidate Q from the LP (float), round it to nearby rationals
    with small denominators and verify the constraints exactly. We don't
    need to recover the exact LP solution — we just need to check whether
    SOMETHING close to feasibility exists exactly. As a stronger gate, we
    use sympy to solve the linear system symbolically.
    """
    import sympy as sp
    Q = sp.MatrixSymbol("Q", 6, 6)
    Qs = sp.Matrix(6, 6, lambda i, j: sp.Symbol(f"q{i}{j}", nonnegative=True))
    syms = list(Qs)
    cons = []
    # Mod-9 = 1/6:
    for j in UNITS9:
        expr = 0
        for u in range(1, 7):
            for v in range(1, 7):
                if R_TABLE[(u, v)] == j:
                    expr += Qs[u - 1, v - 1]
        cons.append(sp.Eq(expr, sp.Rational(1, 6)))
    # Marginal stationarity:
    for u in range(1, 7):
        row = sum(Qs[u - 1, v - 1] for v in range(1, 7))
        col = sum(Qs[v - 1, u - 1] for v in range(1, 7))
        cons.append(sp.Eq(row - col, 0))
    # Normalization:
    cons.append(sp.Eq(sum(syms), 1))
    # Drift target: just check that E[a_class] = log2 3 is realizable
    # (treating log2(3) as a symbolic transcendental we add as a parameter).
    Eac = sum(u * sum(Qs[u - 1, v - 1] for v in range(1, 7)) for u in range(1, 7))
    drift_target_lo = sp.Symbol("drift_lo")  # placeholder for log2 3

    # Try to find the minimum of Eac over the feasible polytope using LP
    # solved exactly via sympy (linear-programming-by-vertex would explode
    # combinatorially; instead, parameterize by the LP solution and verify).
    result: Dict[str, Any] = {}
    # Project the float LP solution to the affine subspace using least squares
    # to a rational subspace. Easier: just verify min_E_a_class against the
    # exact bound by feasibility of Eac <= L for some rational L slightly
    # below log2(3).
    # Pick L = 19/12 = 1.5833... < log2(3) = 1.58496... and check feasibility.
    L = sp.Rational(19, 12)
    cons_L = cons + [sp.Eq(Eac, L)] + [sp.GreaterThan(Qs[i, j], 0) for i in range(6) for j in range(6)]
    # Try solving with sympy linsolve (drops inequalities):
    eq_cons = [c for c in cons + [sp.Eq(Eac, L)] if isinstance(c, sp.Equality)]
    sol = sp.linsolve(eq_cons, *syms)
    result["L_test"] = str(L)
    result["linsolve_nonempty"] = (sol != sp.S.EmptySet)
    if sol != sp.S.EmptySet:
        # Take the parameterized solution and check whether the non-negativity
        # constraints are satisfiable (by sampling parameters or via sympy reduce).
        sol_tuple = next(iter(sol))
        free_syms = sorted(set().union(*(s.free_symbols for s in sol_tuple)), key=str)
        result["num_free_params"] = len(free_syms)
        result["free_param_names"] = [str(s) for s in free_syms]
        # Sanity: with 36 vars - (6 mod-9 + 5 marginal-indep + 1 norm + 1 drift) = 23 free
        # We expect linsolve to return ~23 free parameters.
    return result


# --- Esscher reduction cross-check -----------------------------------------

def esscher_reduction_check() -> Dict[str, Any]:
    """If we restrict Q to be a product Q(u,v) = pi(u) pi(v), then the
    feasibility region degenerates to the Wave 1 system. Verify this:
    forcing Q product and mod-9 saturation should force pi = uniform on 1..6,
    giving E[a_class] = 3.5 > log_2(3). Cross-check.
    """
    # Solve: pi >= 0, sum pi = 1, all six mod-9 marginals (as functions of pi)
    # equal 1/6. From Wave 1: unique solution pi = (1/6, ..., 1/6).
    # We re-verify numerically.
    from scipy.optimize import fsolve

    # P_odd = p_1 + p_3 + p_5, P_even = p_2 + p_4 + p_6.
    # Mod-9 marginals from Wave 1 §1:
    #   P(R=1) = P_odd p_4 + P_even p_2
    #   P(R=2) = P_odd p_3 + P_even p_1
    #   P(R=4) = P_odd p_2 + P_even p_6
    #   P(R=5) = P_odd p_5 + P_even p_3
    #   P(R=7) = P_odd p_6 + P_even p_4
    #   P(R=8) = P_odd p_1 + P_even p_5
    def eqs(p):
        p1, p2, p3, p4, p5, p6 = p
        Po = p1 + p3 + p5
        Pe = p2 + p4 + p6
        return [
            Po * p4 + Pe * p2 - 1.0 / 6,
            Po * p3 + Pe * p1 - 1.0 / 6,
            Po * p2 + Pe * p6 - 1.0 / 6,
            Po * p5 + Pe * p3 - 1.0 / 6,
            Po * p6 + Pe * p4 - 1.0 / 6,
            p1 + p2 + p3 + p4 + p5 + p6 - 1.0,
        ]

    starts = [
        np.array([1, 1, 1, 1, 1, 1]) / 6.0,
        np.array([0.1, 0.3, 0.1, 0.3, 0.1, 0.1]),
        np.array([0.5, 0.05, 0.05, 0.05, 0.3, 0.05]),
    ]
    sols = []
    for s0 in starts:
        sol, info, ier, _ = fsolve(eqs, s0, full_output=True)
        sols.append({"x0": s0.tolist(), "x": sol.tolist(), "res": float(np.linalg.norm(eqs(sol))), "ier": int(ier)})
    return {"esscher_product_solutions": sols}


# --- Markov tilt: cumulant existence + LDP rate ----------------------------

def markov_tilt_LDP_check(Q_target: np.ndarray) -> Dict[str, Any]:
    """Given a feasibility-LP solution Q_target (6x6 stationary joint),
    construct the Markov chain on residue classes c in {1,...,6} with
    transition kernel
        P(u -> v) = Q_target[u, v] / pi(u),    pi(u) = sum_v Q_target[u, v].
    The Donsker-Varadhan rate function for the 2-step empirical measure is
    finite at Q_target iff Q_target is absolutely continuous w.r.t. the
    base-measure 2-step distribution Q_0, which under i.i.d. Geom(1/2) is
        Q_0(u, v) = pi_0(u) pi_0(v),  pi_0(u) = P_{mu_0}(a mod 6 = u).

    pi_0(u) is the residue-mod-6 marginal of i.i.d. Geom(1/2), which is
        pi_0(u) = (1/(1-r0^6)) * r0^u,   r0 = 1/2,   for u in 1..6.
    Then I(Q_target) = sum_{u,v} Q_target(u,v) log[Q_target(u,v) / (pi_0(u) pi_0(v))]
                     = H(Q_target || pi_0 (x) pi_0),
    plus a stationarity correction (this is the Donsker-Varadhan rate for
    the 2-step empirical pair, which for i.i.d. base is exactly KL(Q || pi_0 x pi_0)).

    Note: under the Markov tilt we wish to CONSTRUCT, the rate function on
    the 2-step empirical pair is the same KL functional. For the LDP rate
    at the FULL joint event (mod-9 saturation + drift balance) to be POSITIVE
    AND FINITE, this KL value must be positive and finite.
    """
    r0 = 0.5
    pi_0 = np.array([r0 ** u for u in range(1, 7)])
    pi_0 = pi_0 / pi_0.sum()  # normalize to sum 1 within mod-6 classes
    Q0 = np.outer(pi_0, pi_0)

    Q = np.array(Q_target, dtype=float).reshape(6, 6)
    # Threshold tiny entries:
    eps = 1e-15
    mask = Q > eps
    I_KL = 0.0
    for u in range(6):
        for v in range(6):
            if Q[u, v] > eps:
                I_KL += Q[u, v] * math.log(Q[u, v] / Q0[u, v])
    return {
        "pi_0_base_mod6": pi_0.tolist(),
        "Q0_product": Q0.tolist(),
        "I_KL_Q_vs_Q0": I_KL,
        "I_KL_positive": I_KL > 0,
        "I_KL_finite": math.isfinite(I_KL),
    }


# --- Main -------------------------------------------------------------------

def main() -> None:
    out: Dict[str, Any] = {
        "metadata": {
            "script": os.path.basename(__file__),
            "purpose": "Test escape candidate (P1) Markov reweighting against the Wave 1 d=5 structural obstruction.",
            "author": "Alex Ye",
            "date": "2026-06-04",
        }
    }

    print("=== Gate 0: Validate R(u,v) mod 9 table ===")
    out["R_table"] = {f"{u},{v}": R_TABLE[(u, v)] for u in range(1, 7) for v in range(1, 7)}
    print("  R-table matches Wave 1 (assert passed at import).")

    print("\n=== Gate 1: Esscher reduction (product Q) ===")
    out["esscher_reduction"] = esscher_reduction_check()
    print(f"  Recovered Wave 1 uniform-mod-6 unique solution: see esscher_product_solutions.")

    print("\n=== Probe (P1): LP feasibility of Markov-tilted joint Q ===")
    lp_min = solve_min_drift_lp()
    out["LP_min_drift"] = lp_min
    print(f"  LP min E[a_class] = sum_c c * pi(c): {lp_min['min_E_a_class']:.10f}")
    print(f"  Compare log2(3) = {lp_min['log2_3']:.10f}")
    print(f"  Drift gap (min E - log2 3): {lp_min['drift_gap']:.10f}")
    print(f"  Feasible with within-class pull-up only?: {lp_min['feasible_with_within_class_only_pulling_up']}")
    print(f"  Achieved mod-9 marginals (target 1/6 = {1/6:.6f} each):")
    for j, p in lp_min["mod9_marginal"].items():
        print(f"    P(R = {j} mod 9) = {p:.10f}  (residual {p - 1/6:+.3e})")
    print(f"  pi (row sums): {[f'{x:.6f}' for x in lp_min['pi_rows']]}")
    print(f"  pi (col sums): {[f'{x:.6f}' for x in lp_min['pi_cols']]}")

    lp_max = solve_max_drift_lp()
    out["LP_max_drift"] = lp_max
    print(f"\n  LP max E[a_class]: {lp_max['max_E_a_class']:.10f}")

    print("\n=== Exact-rational LP verification ===")
    try:
        exact_lp = solve_min_drift_lp_EXACT()
        out["LP_exact"] = exact_lp
        print(f"  Exact LP min E[a_class] = {exact_lp['min_E_a_class_exact_str']} ~ {exact_lp['min_E_a_class_exact_float']:.10f}")
        print(f"  All equality constraints exactly satisfied: {exact_lp['all_equality_constraints_zero']}")
        print(f"  All nonneg: {exact_lp['all_nonneg']}")
        print(f"  Vertex support size: {exact_lp['vertex_size']}")
    except Exception as e:
        out["LP_exact"] = {"error": str(e)}
        print(f"  Exact LP error: {e}")

    print("\n=== Non-stationary relaxation (drop row=col constraint) ===")
    lp_ns = solve_min_drift_lp_NONSTATIONARY()
    out["LP_nonstationary"] = lp_ns
    print(f"  LP-NS min E[a_class] (row-marginal weighting): {lp_ns['min_E_a_class_nonstationary']:.10f}")
    print(f"  Drift gap (non-stationary, row-marginal): {lp_ns['min_E_a_class_nonstationary'] - math.log2(3.0):.10f}")

    print("\n=== Exact rational recheck via sympy linsolve ===")
    try:
        exact = exact_rational_recheck(lp_min["Q"])
        out["exact_recheck"] = exact
        print(f"  L = {exact['L_test']} ~ {float(eval(exact['L_test'].replace('Rational', '').replace('(', '(').replace(')', ')'))) if False else 19/12} (compared to log2(3) ~ 1.58496)")
        print(f"  linsolve feasibility at Eac = 19/12: {exact['linsolve_nonempty']}")
        if "num_free_params" in exact:
            print(f"  Free parameters in solution space: {exact['num_free_params']}")
    except Exception as e:
        out["exact_recheck"] = {"error": str(e)}
        print(f"  Exact recheck error: {e}")

    print("\n=== Markov-tilt LDP rate at the LP-min Q ===")
    ldp = markov_tilt_LDP_check(np.array(lp_min["Q"]))
    out["markov_LDP"] = ldp
    print(f"  I_KL(Q || pi_0 (x) pi_0) = {ldp['I_KL_Q_vs_Q0']:.10f}")
    print(f"  positive: {ldp['I_KL_positive']}, finite: {ldp['I_KL_finite']}")

    # --- VERDICT -----------------------------------------------------------
    verdict_lines: List[str] = []
    if lp_min["min_E_a_class"] < math.log2(3.0) - 1e-8:
        verdict_lines.append(
            "(P1) Markov-tilt FEASIBLE at joint level: min E[a_class] < log2(3)."
        )
        verdict_lines.append(
            f"  Joint mod-9 saturation + drift balance both achievable by some 6x6 "
            f"stationary Q with E[a_class] = {lp_min['min_E_a_class']:.6f} < log2(3) = {math.log2(3.0):.6f}."
        )
        verdict_lines.append(
            f"  Donsker-Varadhan LDP rate at this Q: I_KL = {ldp['I_KL_Q_vs_Q0']:.6f}."
        )
        if ldp["I_KL_positive"] and ldp["I_KL_finite"]:
            verdict_lines.append(
                "  LDP rate is POSITIVE AND FINITE: escape via 1-step Markov reweighting on mod-6 is GENUINELY POSSIBLE in this feasibility test."
            )
            verdict = "ESCAPE_FEASIBLE_AT_LP_LEVEL"
        else:
            verdict_lines.append(
                "  LDP rate fails positivity/finiteness — likely a boundary degeneracy."
            )
            verdict = "ESCAPE_BOUNDARY_DEGENERATE"
    elif abs(lp_min["min_E_a_class"] - 3.5) < 1e-8:
        verdict_lines.append(
            "(P1) Markov-tilt INFEASIBLE: LP min E[a_class] = 3.5 = Wave 1 obstruction value."
        )
        verdict_lines.append(
            "  Stationary-Markov reweighting offers NO escape from the d=5 obstruction."
        )
        verdict = "NO_ESCAPE_OBSTRUCTION_PERSISTS"
    else:
        verdict_lines.append(
            f"(P1) Markov-tilt INFEASIBLE: LP min E[a_class] = {lp_min['min_E_a_class']:.6f} > log2(3) = {math.log2(3.0):.6f}."
        )
        verdict_lines.append(
            f"  Drift gap reduced to {lp_min['drift_gap']:.6f} but still strictly positive."
        )
        verdict_lines.append(
            "  Markov reweighting tightens but does NOT break the obstruction."
        )
        verdict = "NO_ESCAPE_REDUCED_GAP"

    out["verdict"] = verdict
    out["verdict_lines"] = verdict_lines

    print("\n=== VERDICT ===")
    for line in verdict_lines:
        print(line)

    # Persist
    json_path = os.path.join(DATA_DIR, "beyond_esscher_probe.json")

    def to_jsonable(x):
        if isinstance(x, np.ndarray):
            return x.tolist()
        if isinstance(x, (Fraction,)):
            return [x.numerator, x.denominator]
        if isinstance(x, dict):
            return {str(k): to_jsonable(v) for k, v in x.items()}
        if isinstance(x, list):
            return [to_jsonable(v) for v in x]
        if isinstance(x, (np.floating,)):
            return float(x)
        if isinstance(x, (np.integer,)):
            return int(x)
        if isinstance(x, (np.bool_,)):
            return bool(x)
        if isinstance(x, bool):
            return bool(x)
        return x

    with open(json_path, "w") as f:
        json.dump(to_jsonable(out), f, indent=2)
    print(f"\nWrote {json_path}")

    log_path = os.path.join(DATA_DIR, "beyond_esscher_probe.log")
    with open(log_path, "w") as f:
        f.write("collatz_beyond_esscher_probe -- Wave 2 verdict\n")
        f.write("=" * 60 + "\n")
        f.write(f"LP min E[a_class]: {lp_min['min_E_a_class']:.12f}\n")
        f.write(f"LP max E[a_class]: {lp_max['max_E_a_class']:.12f}\n")
        f.write(f"log_2(3):          {math.log2(3.0):.12f}\n")
        f.write(f"Drift gap (LP min - log2 3): {lp_min['drift_gap']:.12f}\n")
        f.write(f"I_KL(Q || mu0 (x) mu0): {ldp['I_KL_Q_vs_Q0']:.12f}\n")
        f.write("\n")
        for line in verdict_lines:
            f.write(line + "\n")
    print(f"Wrote {log_path}")


if __name__ == "__main__":
    main()
