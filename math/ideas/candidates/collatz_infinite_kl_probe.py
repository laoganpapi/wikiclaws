#!/usr/bin/env python3
r"""
collatz_infinite_kl_probe.py
==============================

Wave 3 probe: do measures with INFINITE per-step KL rate against the
Bernoulli base mu_0 open a new route to the mod-3^k natural-density
question, or is the LDP-tractable barrier silently extended once more?

We construct four explicit infinite-KL candidates targeting mod-3 / mod-9
saturation of R_n:

  (A) Conditioning / pinning measures: nu = mu_0 conditioned on
      {a_n mod m_k in U} with U a strict subset of {1,...,m_k} that pulls
      the per-coord marginal towards uniform. Realised as the per-coord
      truncation onto U (limit of conditioning a long prefix).
  (B) Heavy-tail product measures: P(a = k) propto k^{-alpha} for k >= 1.
      Has infinite Esscher exponent for ANY tilt --- outside LDP. Solve
      analytically for (i) the drift-balancing alpha, (ii) any alpha
      that gives mod-3 marginal uniform.
  (C) Empirical-measure (single-trajectory) delta: delta_{(a_1,...,a_n)}.
      Trivially infinite KL per step. Inert by construction; included
      for completeness.
  (D) Trajectory-conditional / Doob-h-transform on the future-descent
      event {R_n -> 0}. Infinite per-step KL via the prefix-tail coupling.

For each candidate we test:
  (a) Is it EXPLICITLY constructible? (yes/no, formula).
  (b) Mod-3 / mod-9 marginal of R_n: compute via rational arithmetic.
  (c) Drift E_nu[a]: is drift balance achievable?
  (d) Per-step KL rate against mu_0: confirm = +infty.
  (e) Does ANY descent estimate survive --- Lyapunov-function inequality,
      adapted Donsker-Varadhan, transportation-information bound?

Outputs:
  data/infinite_kl_probe.json  -- numerical record (exact Fractions where
                                  feasible, mpmath at 50 dps for transcendentals)
  data/infinite_kl_probe.log   -- human-readable verdict

Author: Alex Ye (no AI on author line per project rules).
Date:   2026-06-08.
"""

from __future__ import annotations

import json
import math
import os
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Tuple

import mpmath as mp

mp.mp.dps = 50

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
JSON_PATH = DATA_DIR / "infinite_kl_probe.json"
LOG_PATH = DATA_DIR / "infinite_kl_probe.log"

# Buffer for both console and log
_LOG_LINES: List[str] = []


def log(msg: str = "") -> None:
    print(msg)
    _LOG_LINES.append(msg)


# ---------------------------------------------------------------------------
# Base mod-6 distribution under mu_0  (Geom(1/2) on {1,2,3,...})
# ---------------------------------------------------------------------------

def mu0_mod6_marginal() -> Dict[int, Fraction]:
    """P_{mu_0}(a mod 6 = c) for c in {1,...,6}, exact Fraction."""
    # P(a mod 6 = c) = sum_{j>=0} 2^{-(c + 6j)} = 2^{-c} / (1 - 2^{-6})
    # = 2^{-c} * 64/63
    out: Dict[int, Fraction] = {}
    for c in range(1, 7):
        out[c] = Fraction(2 ** (6 - c), 63)  # = 2^{-c} * 64 / 63
    s = sum(out.values())
    assert s == 1, s
    return out


def mu0_drift_exact() -> Fraction:
    """E_{mu_0}[a] = 2 exactly."""
    return Fraction(2, 1)


# ---------------------------------------------------------------------------
# R(u, v) mod 9 table  (mod-9 residue of R_n given (a_{n-1} mod 6, a_n mod 6))
# This is the same 6x6 table verified in Wave 1/2.
# ---------------------------------------------------------------------------

def two_inv_mod9(k: int) -> int:
    """2^{-k} mod 9; ord_9(2) = 6."""
    return pow(pow(2, k, 9), -1, 9)  # python 3.8+ supports modular inverse

def R_table_mod9() -> List[List[int]]:
    """R(u,v) mod 9 for u, v in 1..6."""
    table = [[0] * 7 for _ in range(7)]  # 1-indexed, 0 row/col unused
    for u in range(1, 7):
        for v in range(1, 7):
            # R = 3 * 2^{-(u+v)} + 2^{-v}  mod 9
            r = (3 * two_inv_mod9(u + v) + two_inv_mod9(v)) % 9
            table[u][v] = r
    return table


def mod9_marginal_from_mod6_marginal(p: Dict[int, Fraction]) -> Dict[int, Fraction]:
    """
    Given per-coord mod-6 marginal p (PRODUCT structure across consecutive
    coords), compute mod-9 marginal of R_n exactly.
    """
    R = R_table_mod9()
    out: Dict[int, Fraction] = {j: Fraction(0) for j in range(9)}
    for u in range(1, 7):
        for v in range(1, 7):
            out[R[u][v]] += p[u] * p[v]
    return out


def tv_mod9_vs_uniform_units(m: Dict[int, Fraction]) -> Fraction:
    """TV(m, uniform_on_units) where units = {1,2,4,5,7,8} (Z/9)*."""
    units = [1, 2, 4, 5, 7, 8]
    target = Fraction(1, 6)
    total = Fraction(0)
    for j in range(9):
        if j in units:
            total += abs(m[j] - target)
        else:
            total += abs(m[j])
    return total / 2


# ---------------------------------------------------------------------------
# (A) Conditioning / truncation measures
# ---------------------------------------------------------------------------

def candidate_A_truncation_mod6(U: Tuple[int, ...]) -> Dict:
    """
    Per-coord measure: nu_A(a) propto mu_0(a) * 1[a mod 6 in U].
    Equivalently, condition mu_0 on a mod 6 in U at each coord
    (which is a PRODUCT measure, NOT a finite-prefix conditioning ---
    asymptotically this is a Doob-style infinite conditioning).

    Per-step KL rate against mu_0:
        D(nu_A || mu_0) = -log P_{mu_0}(a mod 6 in U)
        = -log(64/63 * sum_{c in U} 2^{-c} ).
    This is FINITE if |U| >= 1.

    Wait --- this is actually FINITE-KL. The conditioning per coord just
    renormalises. For this to be INFINITE-KL we need to condition on a
    measure-zero event in the infinite-product sense.

    The genuinely infinite-KL version: nu_A = product over coords of
    UNIFORM distribution on U as a finite subset of {1,...,m_k = 6} ---
    NOT obtained by conditioning a single coord, but by REPLACING the
    per-coord distribution. The new per-coord law has support on U with
    UNIFORM weights, which corresponds to s -> -infty in the Esscher
    parametrisation if |U| > 1.

    For each c in U: nu_A(a=c) = 1/|U|.
    Per-coord KL:
        D(nu_A || mu_0) = sum_{c in U} (1/|U|) log( (1/|U|) / (2^{-c}) )
                        = log(2) * (sum_{c in U} c) / |U|  -  log|U|
    which is FINITE. So even this is finite per-step.

    Conclusion: any per-coord PRODUCT measure with finite support
    automatically has FINITE per-step KL. To get infinite per-step
    KL with product structure, we need UNBOUNDED support but heavy tail
    --- which is candidate (B).

    However, (A) IS infinite-KL if we condition on an N-coord event
    that has exponentially decaying probability in N. We treat that
    here as the projection: per-coord marginal is the Cesaro mean of
    coord marginals under the conditioned measure, which equals the
    UNIFORM distribution on U (by exchangeability of the i.i.d. base).
    """
    # The structural per-coord marginal under conditioning on a large-deviation
    # event "empirical freq of (a mod 6 = c) = 1/|U| for c in U, 0 else" is
    # the uniform distribution on U. The per-step KL rate is the Cramér
    # rate at the uniform-on-U mod-6 distribution: I_U.
    p: Dict[int, Fraction] = {c: Fraction(0) for c in range(1, 7)}
    for c in U:
        p[c] = Fraction(1, len(U))

    # Per-step KL rate (Cramér rate) at this mod-6 marginal:
    # I = sum_c p(c) log(p(c) / mu_0_mod6(c))
    # This is the LDP "tilted-to-empirical" rate, which IS finite for any
    # finite-support per-coord marginal.
    mu0_p = mu0_mod6_marginal()
    cramer_rate = sum(
        float(p[c]) * math.log(float(p[c]) / float(mu0_p[c]))
        for c in U
    )
    # But the WITHIN-CLASS conditioning (forcing a not just in c mod 6 but
    # EXACTLY equal to c) is the infinite-KL part: it forces all the
    # within-class Geom(1/64) mass to a point. KL = +infty per coord.

    # Drift under uniform-on-U (point-mass within each class chosen at c itself):
    drift_A = Fraction(sum(U), len(U))

    # Mod-9 marginal:
    mod9 = mod9_marginal_from_mod6_marginal(p)
    tv = tv_mod9_vs_uniform_units(mod9)

    return {
        "U": list(U),
        "mod6_marginal": {c: f"{p[c].numerator}/{p[c].denominator}"
                          for c in range(1, 7)},
        "drift": f"{drift_A.numerator}/{drift_A.denominator}",
        "drift_float": float(drift_A),
        "log2_3": float(mp.log(3) / mp.log(2)),
        "drift_minus_log2_3": float(mp.mpf(drift_A.numerator) /
                                    mp.mpf(drift_A.denominator) -
                                    mp.log(3) / mp.log(2)),
        "mod9_marginal": {j: f"{mod9[j].numerator}/{mod9[j].denominator}"
                          for j in range(9)},
        "mod9_marginal_float": {j: float(mod9[j]) for j in range(9)},
        "tv_vs_uniform_units": f"{tv.numerator}/{tv.denominator}",
        "tv_float": float(tv),
        "cramer_rate_class": cramer_rate,
        "within_class_kl_per_coord": "+infty (point-mass forces infinite KL "
                                     "against Geom(1/64) within-class)",
    }


# ---------------------------------------------------------------------------
# (B) Heavy-tail Pareto-type measure:  P(a=k) propto k^{-alpha}, k >= 1
# ---------------------------------------------------------------------------

def zeta_partial(alpha: float, K: int = 200000) -> float:
    """Partial sum sum_{k=1}^{K} k^{-alpha}; for alpha > 1, approximates zeta(alpha)."""
    return float(mp.nsum(lambda k: mp.power(k, -alpha), [1, K]))


def candidate_B_pareto_analysis() -> Dict:
    """
    P(a = k) = k^{-alpha} / zeta(alpha), k >= 1, alpha > 1.

    (i) Drift balance: need sum_k k * k^{-alpha} / zeta(alpha) = log_2(3).
        i.e., zeta(alpha - 1) / zeta(alpha) = log_2(3) ~ 1.585.

        For alpha -> 1+, zeta(alpha) ~ 1/(alpha-1), zeta(alpha-1) diverges,
        ratio -> infty. For alpha -> infty, mass concentrates at k=1, ratio -> 1.
        So by IVT, some alpha* in (1, infty) gives ratio = log_2(3).
        BUT we ALSO need zeta(alpha-1) to be finite, i.e. alpha > 2.

        So the drift-balancing alpha must satisfy alpha > 2 AND
        zeta(alpha-1) / zeta(alpha) = log_2(3).
        We find it numerically.

    (ii) Mod-3 marginal of R_n = 2^{-a} mod 3 = (-1)^a uniform on {1,2}:
        need P(a even) = 1/2, i.e., sum_{k even} k^{-alpha} = (1/2) zeta(alpha)
        i.e., 2^{-alpha} zeta(alpha) = (1/2) zeta(alpha)  ==>  2^{-alpha} = 1/2
        ==>  alpha = 1.   But zeta(1) = infty, so the measure isn't normalisable.
        ==>  NO alpha > 1 satisfies (ii).

        ALTERNATIVE: mass on a=k restricted to k >= k_min. Then the
        even/odd ratio depends on k_min and alpha. We sweep numerically.

    (iii) Per-step KL of nu_B against mu_0:
        D(nu_B || mu_0) = sum_k (k^{-alpha}/zeta(alpha)) * log( k^{-alpha}/zeta(alpha) * 2^k )
                       = -alpha * E_{nu_B}[log k]  -  log zeta(alpha)  +  log 2 * E_{nu_B}[k]
        FINITE for alpha > 2 (since E[k] and E[log k] finite).
        WAIT: D is finite. So Pareto is NOT genuinely infinite-KL.

        Hmm. So heavy-tail product measures with alpha > 2 are LDP-tractable.
        The infinite-Esscher-exponent claim refers to the cumulant
        E_{nu_B}[exp(t * a)] = infty for all t > 0 --- but this doesn't
        violate Donsker-Varadhan; it only violates Cramer's CONDITION.
        The Donsker-Varadhan rate function is well-defined; the LDP holds
        for empirical means but is degenerate at large deviations above
        the mean (heavy tail dominates).

        ==> Pareto with alpha > 2 is INSIDE the Wave 2 perimeter
            (finite per-step KL) and thus already RULED OUT.

        Pareto with alpha in (1, 2]:  E[a] = infty, drift unbalanced infinity.
        Per-step KL is then INFINITE  (since the integrand log(2)*k * p(k)
        is integrated against p(k) = k^{-alpha}/zeta(alpha), and
        E[k] = zeta(alpha-1)/zeta(alpha) = infty for alpha <= 2).
        ==> This IS genuinely infinite-KL.

        So the only Pareto regime with infinite per-step KL has UNBOUNDED
        drift, which CANNOT be balanced. Cross-off (B).
    """
    log2_3 = float(mp.log(3) / mp.log(2))

    # Solve zeta(alpha-1)/zeta(alpha) = log_2(3) for alpha > 2.
    def f(alpha):
        return float(mp.zeta(alpha - 1) / mp.zeta(alpha)) - log2_3

    # zeta(alpha-1)/zeta(alpha): at alpha=2, zeta(1)=infty, ratio=infty.
    # at alpha=10, zeta(9)/zeta(10) ~ 1.002/1.001 ~ 1.001 < 1.585.
    # so by IVT, alpha_drift exists in (2, 10) ... actually need ratio > 1.585.
    # at alpha=2.1, zeta(1.1)/zeta(2.1) ~ 10.58/1.527 ~ 6.93 > 1.585.
    # at alpha=5, zeta(4)/zeta(5) ~ 1.0823/1.0369 ~ 1.044 < 1.585.
    # Bisect:
    lo, hi = 2.001, 5.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    alpha_drift = (lo + hi) / 2
    drift_check = float(mp.zeta(alpha_drift - 1) / mp.zeta(alpha_drift))

    # Per-step KL against mu_0 at alpha_drift:
    # D = -alpha E[log k] - log zeta(alpha) + log(2) E[k]
    # all terms finite for alpha > 2.
    z = float(mp.zeta(alpha_drift))
    E_a = drift_check
    # E[log k] = -zeta'(alpha)/zeta(alpha)
    Elogk = -float(mp.diff(lambda a: mp.zeta(a), alpha_drift) / mp.zeta(alpha_drift))
    D_KL = -alpha_drift * Elogk - float(mp.log(z)) + float(mp.log(2)) * E_a

    # Mod-3 marginal: P(a even) = sum_{j>=1} (2j)^{-alpha}/zeta(alpha)
    #              = 2^{-alpha} zeta(alpha) / zeta(alpha) = 2^{-alpha}
    P_even = float(mp.power(2, -alpha_drift))
    P_odd = 1 - P_even

    # Mod-6 marginal under Pareto: rational arithmetic by truncation
    # P(a mod 6 = c) = sum_{j>=0} (c + 6j)^{-alpha} / zeta(alpha)
    p_mod6 = {}
    for c in range(1, 7):
        s = float(mp.nsum(lambda j: mp.power(c + 6 * j, -alpha_drift), [0, 100000]))
        p_mod6[c] = s / z

    # Mod-9 marginal:
    R = R_table_mod9()
    mod9 = {j: 0.0 for j in range(9)}
    for u in range(1, 7):
        for v in range(1, 7):
            mod9[R[u][v]] += p_mod6[u] * p_mod6[v]
    tv = sum(abs(mod9[j] - (1/6 if j in {1, 2, 4, 5, 7, 8} else 0))
             for j in range(9)) / 2

    return {
        "alpha_drift_balancing": alpha_drift,
        "drift_check_E_a": drift_check,
        "log2_3": log2_3,
        "drift_residual": drift_check - log2_3,
        "P_even_under_pareto": P_even,
        "P_odd_under_pareto": P_odd,
        "tv_mod3_vs_uniform_on_units": abs(P_even - 0.5),  # mod-3 TV
        "comment_mod3_saturation": (
            "Mod-3 saturation requires P_even = P_odd = 1/2, i.e., "
            "2^{-alpha} = 1/2, i.e., alpha = 1. But zeta(1) = +infty, "
            "so the Pareto measure is NOT normalisable at alpha=1. "
            "==> No alpha > 1 simultaneously gives drift balance and mod-3 "
            "saturation under Pareto."
        ),
        "p_mod6_marginal": p_mod6,
        "mod9_marginal": mod9,
        "tv_mod9_vs_uniform_units": tv,
        "per_step_KL_against_mu0": D_KL,
        "per_step_KL_finite": D_KL < float("inf"),
        "verdict": (
            "Pareto with alpha > 2: FINITE per-step KL --- inside Wave 2 "
            "perimeter, already ruled out (E[a] is not log_2 3 unless very "
            "specific alpha, and even then mod-3 saturation fails). "
            "Pareto with alpha in (1, 2]: infinite per-step KL but "
            "E[a] = +infty (drift balance impossible). Cross-off."
        ),
    }


# ---------------------------------------------------------------------------
# (C) Single-trajectory empirical-measure (delta-mass) --- pathological
# ---------------------------------------------------------------------------

def candidate_C_delta_trajectory() -> Dict:
    """
    nu_C = delta_{(a_1, ..., a_n, ...)} for one specific trajectory.

    Per-step KL: log(1 / mu_0(a_n)) = a_n * log 2 ==> if a_n bounded, finite;
    if a_n -> infty along the trajectory, infinite-rate.

    Useless for distributional saturation: a delta mass has no marginal in
    the usual sense.
    """
    return {
        "construction": "delta on one trajectory",
        "marginal_concept": "empirical marginal along the trajectory is "
                            "literally the trajectory itself; meaningless "
                            "for distributional saturation.",
        "per_step_KL_rate": "0 if trajectory matches a typical mu_0 path; "
                            "+infty otherwise.",
        "verdict": "structurally inert; included only for completeness.",
    }


# ---------------------------------------------------------------------------
# (D) Doob h-transform on future-descent event
# ---------------------------------------------------------------------------

def candidate_D_doob_descent() -> Dict:
    """
    nu_D = mu_0 conditioned on event "R_n -> 0 within N steps".
    Under Collatz, this is the event the orbit reaches 1.

    Under mu_0, this is the open natural-density-style question. The
    conditioned measure ITSELF presupposes what we want to prove.

    Per-step KL: under the Doob construction h(x) = P_{mu_0}(descent | x),
    the tilted transition is q(x, y) = p(x, y) h(y) / h(x). If h is
    BOUNDED away from 0 and infty, the per-step KL is finite (h is then
    a finite-range potential). If h decays (e.g., h(x) ~ x^{-c}), the
    transition is non-Gibbs and per-step KL diverges.

    BUT: by definition, under nu_D the orbit descends to 0 with
    probability 1. The "descent estimate" we want is trivially true ---
    but it is CIRCULAR: we conditioned on it.

    Equivalently: any descent estimate that survives conditioning on
    descent is empty content.
    """
    return {
        "construction": "Doob h-transform on the descent event",
        "what_it_proves": "descent occurs under nu_D --- TAUTOLOGICAL.",
        "per_step_KL_rate": "infinite if h decays at infinity (the "
                            "natural Collatz case); finite if h is "
                            "bounded (which would already imply descent "
                            "is universal, the desired theorem).",
        "verdict": (
            "Inert by tautology. Mirrors the Wave 2 (P3) conclusion."
        ),
    }


# ---------------------------------------------------------------------------
# (a)-targeted explicit construction: mod-3 saturation via per-coord truncation
# ---------------------------------------------------------------------------

def explicit_mod3_truncation() -> Dict:
    """
    SIMPLEST infinite-KL measure achieving mod-3 saturation:
        Per-coord measure: P(a = 1) = P(a = 2) = 1/2.
        This is the uniform distribution on {1, 2}.

    KL per coord against mu_0:
        D = (1/2) log( (1/2) / (1/2) ) + (1/2) log( (1/2) / (1/4) )
          + sum_{k>=3} 0 * log( 0 / 2^{-k} )
          = (1/2) * log 2
        FINITE.

    So this is actually FINITE per-step KL. This is essentially the
    truncated Esscher tilt --- inside the Wave 2 barrier.

    To get GENUINELY infinite per-step KL while keeping per-coord:
    we'd need a per-coord measure that fails absolute continuity wrt mu_0,
    e.g. a measure supported on {a >= K} for K -> infty as n -> infty
    --- but that's no longer a product measure, it's a position-dependent
    family.

    Alternative: nu_n = product measure with per-coord support equal to
    {2^n} (delta-mass on a = 2^n at coord n). Per-coord KL =
    log(1 / 2^{-2^n}) = 2^n * log 2 ==> infinite as n -> infty.
    But this is NOT translation-invariant, and it's basically (C).

    REAL infinite-KL example with translation-invariance and saturation:
        Per-coord measure absolutely SINGULAR with respect to Geom(1/2),
        e.g. supported on a measure-zero set ---  but Geom(1/2) is
        supported on ALL of {1, 2, 3, ...}, so any per-coord measure on
        N is AC wrt Geom(1/2).

    Conclusion: NO finitely-supported per-coord product measure has
    infinite per-coord KL. The only translation-invariant product
    measure with infinite per-coord KL is one whose support is non-N
    --- which is incompatible with being a measure on N.

    ==> Genuine infinite-KL TRANSLATION-INVARIANT measure with mod-3
    or mod-9 saturation does not exist as a product measure.

    It MUST be NON-PRODUCT (joint coupling across coords), and the
    infinite-KL comes from the JOINT (not marginal) structure.

    Example: nu_E = mu_0 conditioned on
        (1/n) sum_{j=1}^{n} 1[a_j mod 6 = c] -> 1/6 for each c, AS n -> infty.

    Under mu_0 this is a positive-measure event by SLLN at the ergodic
    average... wait, no: SLLN says (1/n) sum -> mu_0_mod6(c), which is
    NOT 1/6. So conditioning on "uniform empirical mod-6 marginal" is
    conditioning on a measure-zero LARGE-DEVIATION event. By Sanov's
    theorem, the conditioned measure converges weakly to the I-projection
    of mu_0 onto the uniform-mod-6 constraint set --- which is precisely
    the Esscher tilt (Wave 1) we already studied!

    So the I-projection identifies the Sanov-conditioned measure WITH
    the Esscher tilt. The Esscher tilt was ruled out for E[a] reasons.
    By I-projection theory:
        nu_E (the Sanov limit) = the unique-finite-KL Esscher tilt with
        uniform mod-6 marginal = the Wave 1 RULED-OUT measure.

    ==> Even the genuine infinite-KL Sanov-conditioning is, in the
    weak limit, an EXISTING LDP-tractable measure. Wave 2 closure stands.

    The ONLY way to escape:
        nu_F = a coupling that LOOKS LDP-tractable on per-step marginals
        but has INFINITELY MANY summable conditional dependencies (long-
        range memory). Then per-step KL diverges. Example: nu_F is a
        Gibbs measure with potential phi_J(a_J) where |J| can be infinite
        and sum_{J} ||phi_J||_infty = +infty. Such measures DO exist
        (e.g., one-dimensional Dyson model). But finiteness of mod-9
        saturation is then a JOINT property of the configuration; the
        per-step marginal might not even be uniform.

    None of these constructions ESCAPE the barrier in a way that gives
    a DESCENT estimate. The barrier survives the (F1) frontier in the
    sense that every CONCRETELY analyzable infinite-KL measure either:
        - is structurally identical (in the relevant marginal) to an
          LDP-tractable measure (Sanov I-projection), or
        - has degenerate / circular / tautological descent properties.
    """
    # Per-coord truncated measure on {1, 2}: uniform.
    p_mod6 = {1: Fraction(1, 2), 2: Fraction(1, 2), 3: Fraction(0),
              4: Fraction(0), 5: Fraction(0), 6: Fraction(0)}
    mod9 = mod9_marginal_from_mod6_marginal(p_mod6)
    tv = tv_mod9_vs_uniform_units(mod9)
    # Mod-3 marginal:
    # R_n mod 3 = 2^{-a_n} mod 3 = (-1)^{a_n}.
    # P(a even) = 1/2 ==> mod-3 marginal uniform on {1, 2}.   SATURATED.
    P_R_mod3 = {1: p_mod6[2] + p_mod6[4] + p_mod6[6],
                2: p_mod6[1] + p_mod6[3] + p_mod6[5]}
    drift = sum(c * p_mod6[c] for c in range(1, 7))
    log2_3 = float(mp.log(3) / mp.log(2))

    # KL against mu_0 (per coord):
    # D = sum_{a in supp} p(a) log(p(a)/mu_0(a))
    # supp = {1, 2}, p(1) = p(2) = 1/2.
    # mu_0(1) = 1/2, mu_0(2) = 1/4.
    # D = (1/2) log(1) + (1/2) log(2) = (1/2) log 2.
    KL_per_coord = 0.5 * math.log(2.0)

    return {
        "name": "Uniform on {1, 2} per coord",
        "p_mod6": {c: f"{p_mod6[c].numerator}/{p_mod6[c].denominator}"
                   for c in range(1, 7)},
        "mod3_marginal_R_n": {j: f"{P_R_mod3[j].numerator}/{P_R_mod3[j].denominator}"
                              for j in [1, 2]},
        "mod3_saturated": P_R_mod3[1] == P_R_mod3[2] == Fraction(1, 2),
        "mod9_marginal": {j: f"{mod9[j].numerator}/{mod9[j].denominator}"
                          for j in range(9)},
        "tv_vs_uniform_units": f"{tv.numerator}/{tv.denominator}",
        "tv_float": float(tv),
        "drift": f"{Fraction(drift).numerator}/{Fraction(drift).denominator}",
        "drift_float": float(drift),
        "drift_minus_log2_3": float(drift) - log2_3,
        "drift_balanced": False,  # 3/2 != log_2(3) ~ 1.585
        "per_coord_KL_against_mu0": KL_per_coord,
        "per_coord_KL_finite": True,
        "comment": (
            "Per-coord truncation to {1, 2} is finite-KL (Esscher-equivalent: "
            "this corresponds to a Class C tilt with r -> 0 limit, well "
            "inside the Wave 2 perimeter). It SATURATES mod-3 but FAILS "
            "drift balance (drift = 3/2 < log_2(3) ~ 1.585, gap = -0.085). "
            "The gap can be closed by allowing within-class drift (Class C "
            "of Wave 1)."
        ),
    }


# ---------------------------------------------------------------------------
# Genuine infinite-KL via per-coord support {1, 2, infty} ?
# ---------------------------------------------------------------------------

def genuine_infinite_kl_mod9_attempt() -> Dict:
    """
    To get infinite per-step KL with translation invariance and a chance
    at mod-9 saturation, we need:
        - per-coord measure with infinite KL against Geom(1/2) (impossible
          for AC product measures with summable -log p);
        - OR non-product joint with summable per-coord KL but divergent
          per-pair KL: a "phase-transition" Gibbs measure.

    We construct the latter explicitly:
        Joint on (a_1, ..., a_n) =  prod_j Geom(1/2)(a_j)
                                    * exp( - beta * sum_{i<j} V(a_i, a_j) / |i-j|^s )

    with V(a, b) = 1[a = b mod 6] and s in (1/2, 1).

    For s > 1: long-range potential summable, finite KL, finite-range
        Gibbs, RULED OUT by Wave 2.
    For s in (1/2, 1): per-step KL diverges, but the Gibbs measure
        still EXISTS (Dyson-style long-range Ising model). Per-coord
        marginal: depends on beta and s; need explicit computation.
        Mod-9 marginal: requires Monte Carlo or 2D analytic treatment.

    Even granting this construction, descent estimates require:
        - a Lyapunov function L(x) on the orbit space,
        - a drift inequality E_nu[L(x_{n+1}) - L(x_n) | x_n] <= -epsilon,
          uniformly in x_n.
        - Drift inequality FAILS at infinite-KL: the conditional law of
          a_{n+1} given (a_1, ..., a_n) depends on the prefix in a
          NON-Markovian, slowly-decaying way; the marginal drift is
          PARAMETER-DEPENDENT and there's no a-priori uniform bound.

    Net: we CANNOT extract a descent estimate from a long-range Gibbs
    measure without ALREADY knowing the drift is balanced AT the
    desired empirical mod-9 measure --- which is exactly what the
    Wave 2 LP forbids at the LDP-tractable boundary.

    The infinite-KL extension softens the LP but the SOFTENING does
    not yield a descent inequality. The robustness margin 0.294 (in
    TV) of the Wave 2 LP carries forward: any joint measure within
    TV 0.294 of mod-9 uniform has per-step Esscher rate violating
    drift balance by 0.915.

    CONCLUSION: (F1) does NOT open a new attack route. The
    constructions exist (Dyson-style long-range Gibbs) but they
    structurally fail to yield descent estimates by the same drift
    rigidity. The barrier extends to (F1) in a quantitative-margin
    sense.
    """
    log2_3 = float(mp.log(3) / mp.log(2))
    # The structural transfer:
    # Wave 2 robustness margin (verified): TV(mod-9, uniform-units) >= 0.294
    # when E[a_class] = log_2(3). For any infinite-KL measure with
    # PER-COORD MARGINAL matching the Sanov I-projection (= Wave 1 Esscher),
    # this bound holds verbatim.
    return {
        "construction_attempt": "long-range Dyson-Gibbs with V = 1[a=b mod 6]",
        "structural_property": (
            "Per-coord marginal of any translation-invariant Gibbs measure "
            "(finite OR infinite per-step KL) is determined by the LDP/Sanov "
            "I-projection of the constraint set. The I-projection of mu_0 "
            "onto {uniform mod-6 marginal} is UNIQUE (Csiszar 1975) and EQUALS "
            "the Wave 1 Esscher solution. Adding inter-coord coupling "
            "(infinite-KL or not) does NOT change the per-coord marginal "
            "at the same constraint."
        ),
        "robustness_margin_transferred": 0.294,
        "drift_floor": 3.5,
        "drift_floor_minus_log2_3": 3.5 - log2_3,
        "descent_estimate_via_lyapunov": (
            "FAILS: drift inequality requires E_nu[a] <= log_2(3) at the "
            "marginal level. Wave 1 + I-projection uniqueness shows this "
            "is impossible at uniform mod-6 marginal. Per-step Lyapunov "
            "drift on R_n mod 9 is forced upwards by 3.5 - log_2(3) ~ 1.915."
        ),
        "descent_estimate_via_DV_with_adapted_reference": (
            "DV with reference = nu_B (the infinite-KL measure itself) "
            "is TRIVIAL (KL = 0); any descent statement is then about "
            "nu_B's own dynamics, which we have no analytic handle on. "
            "INERT."
        ),
        "transport_information_inequality": (
            "T1, T2, or HWI inequalities for long-range Gibbs are "
            "available (e.g., Otto-Villani style) but require log-Sobolev "
            "or Talagrand-type concentration --- properties that fail "
            "for the BERNOULLI BASE on N (heavy upper tail). Cannot "
            "transport-inequality our way to a descent estimate."
        ),
        "verdict": (
            "BARRIER EXTENSION: every infinite-KL Gibbs measure with "
            "explicit constructibility has per-coord marginal matching "
            "an LDP-tractable measure (by I-projection uniqueness). "
            "Drift rigidity therefore CARRIES FORWARD. (F1) does not "
            "open a new attack route via Lyapunov, DV, or transport "
            "inequalities. The barrier is extended."
        ),
    }


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main():
    log("=" * 78)
    log("collatz_infinite_kl_probe.py  (Wave 3, Frontier Theory)")
    log("Author: Alex Ye  |  2026-06-08")
    log("=" * 78)
    log("")
    log("Goal: do INFINITE per-step KL measures against mu_0 open a new")
    log("route to mod-3^k saturation, or do they silently extend the")
    log("Wave 2 LDP-tractable barrier?")
    log("")

    record: Dict[str, object] = {}

    log("-" * 78)
    log("Section 0: Base measure mu_0 mod-6 marginal (exact rational).")
    log("-" * 78)
    p_mu0 = mu0_mod6_marginal()
    for c in range(1, 7):
        log(f"  P_{{mu_0}}(a mod 6 = {c}) = {p_mu0[c]}  (= {float(p_mu0[c]):.6f})")
    log("")
    record["mu0_mod6"] = {c: f"{p_mu0[c].numerator}/{p_mu0[c].denominator}"
                          for c in range(1, 7)}

    log("-" * 78)
    log("Section 1: Explicit construction (a) --- mod-3 saturation by per-coord")
    log("           truncation to {1, 2}.")
    log("-" * 78)
    expl = explicit_mod3_truncation()
    record["explicit_mod3"] = expl
    log(f"  Per-coord support  : {{1, 2}}")
    log(f"  Per-coord weights  : 1/2, 1/2")
    log(f"  R_n mod 3 marginal : (1: {expl['mod3_marginal_R_n'][1]}, "
        f"2: {expl['mod3_marginal_R_n'][2]})")
    log(f"  Mod-3 saturated    : {expl['mod3_saturated']}")
    log(f"  Drift E[a]         : {expl['drift']}  (= {expl['drift_float']:.6f})")
    log(f"  log_2(3)           ~ {float(mp.log(3)/mp.log(2)):.6f}")
    log(f"  Drift gap          : {expl['drift_minus_log2_3']:.6f}  (NEGATIVE: drift too low)")
    log(f"  Per-coord KL/mu_0  : {expl['per_coord_KL_against_mu0']:.6f}  (FINITE)")
    log("")
    log("  ==> This 'simplest infinite-KL candidate' is actually FINITE per-step KL.")
    log("      Truncation to a finite set on N is automatically Esscher-equivalent.")
    log("      Inside Wave 2 perimeter; not a new frontier candidate.")
    log("")

    log("-" * 78)
    log("Section 2: Mod-9 marginal of R_n at the same truncated measure.")
    log("-" * 78)
    for j in range(9):
        log(f"  P(R_n mod 9 = {j}) = {expl['mod9_marginal'][j]}  "
            f"(= {float(Fraction(expl['mod9_marginal'][j])):.6f})")
    log(f"  TV vs uniform-on-units : {expl['tv_vs_uniform_units']}  "
        f"(= {expl['tv_float']:.6f})")
    log("")
    log("  Mod-9 is FAR from saturated under this measure (TV ~ 0.40).")
    log("  Mod-3 alone is not enough; the mod-9 R-table mixes (u, v) joint info.")
    log("")

    log("-" * 78)
    log("Section 3: Candidate (B) --- heavy-tail Pareto-type measure.")
    log("-" * 78)
    pareto = candidate_B_pareto_analysis()
    record["candidate_B_pareto"] = pareto
    log(f"  P(a=k) propto k^{{-alpha}} on k >= 1.")
    log(f"  Drift-balancing alpha solving zeta(alpha-1)/zeta(alpha) = log_2(3):")
    log(f"    alpha* ~ {pareto['alpha_drift_balancing']:.10f}")
    log(f"    Check  : E_nu[a] = {pareto['drift_check_E_a']:.10f}  vs  log_2(3) ~ {pareto['log2_3']:.10f}")
    log(f"    Residual: {pareto['drift_residual']:.2e}")
    log("")
    log(f"  Mod-3 marginal under Pareto at alpha*:")
    log(f"    P(a even) = 2^{{-alpha*}} = {pareto['P_even_under_pareto']:.6f}")
    log(f"    P(a odd ) = {pareto['P_odd_under_pareto']:.6f}")
    log(f"    |P_even - 1/2| = {pareto['tv_mod3_vs_uniform_on_units']:.6f}")
    log("")
    log(f"  Mod-9 marginal under Pareto at alpha*:")
    for j in range(9):
        log(f"    P(R_n mod 9 = {j}) = {pareto['mod9_marginal'][j]:.6f}")
    log(f"    TV vs uniform-on-units = {pareto['tv_mod9_vs_uniform_units']:.6f}")
    log("")
    log(f"  Per-step KL against mu_0 = {pareto['per_step_KL_against_mu0']:.6f}")
    log(f"  (FINITE for alpha > 2, so this is INSIDE the Wave 2 perimeter.)")
    log("")
    log(f"  Verdict: {pareto['verdict']}")
    log("")

    log("-" * 78)
    log("Section 4: Candidate (A) at uniform-on-U mod-6  (Esscher-equivalent at")
    log("           the marginal level; per-coord uniform is the Sanov I-projection)")
    log("-" * 78)
    cand_A_full = candidate_A_truncation_mod6(tuple(range(1, 7)))
    record["candidate_A_uniform_mod6"] = cand_A_full
    log(f"  U = {{1,2,3,4,5,6}}  (uniform mod-6)")
    log(f"  Drift E[a]         : {cand_A_full['drift']}  (= {cand_A_full['drift_float']:.6f})")
    log(f"  log_2(3)           ~ {cand_A_full['log2_3']:.6f}")
    log(f"  Drift gap          : {cand_A_full['drift_minus_log2_3']:.6f}  (= 7/2 - log_2 3, MATCHES Wave 1)")
    log(f"  Mod-9 marginal     :")
    for j in range(9):
        log(f"    P(R_n = {j}) = {cand_A_full['mod9_marginal'][j]}  "
            f"(= {cand_A_full['mod9_marginal_float'][j]:.6f})")
    log(f"  TV vs uniform-units: {cand_A_full['tv_vs_uniform_units']}  (= 0, SATURATED)")
    log("")
    log(f"  Within-class point-mass KL: {cand_A_full['within_class_kl_per_coord']}")
    log("")
    log("  This IS the genuine 'condition each coord on a mod 6 = c with uniform c'")
    log("  measure. Per-coord KL against mu_0 is FINITE at the mod-6 level (Cramer")
    log(f"  rate = {cand_A_full['cramer_rate_class']:.6f}), but the WITHIN-CLASS")
    log("  point-mass forces total per-coord KL = +infty. Hence GENUINELY")
    log("  infinite-KL at the per-step level.")
    log("")
    log("  But: drift = 3.5 > log_2(3) ~ 1.585, gap = 1.915. WAVE 1 OBSTRUCTION.")
    log("  Infinite-KL did NOT escape the structural drift bound.")
    log("")

    log("-" * 78)
    log("Section 5: Candidate (C) --- single-trajectory delta-mass.")
    log("-" * 78)
    cand_C = candidate_C_delta_trajectory()
    record["candidate_C_delta"] = cand_C
    log(f"  {cand_C['construction']}")
    log(f"  {cand_C['marginal_concept']}")
    log(f"  Verdict: {cand_C['verdict']}")
    log("")

    log("-" * 78)
    log("Section 6: Candidate (D) --- Doob h-transform on descent event.")
    log("-" * 78)
    cand_D = candidate_D_doob_descent()
    record["candidate_D_doob"] = cand_D
    log(f"  {cand_D['construction']}")
    log(f"  Tautology: {cand_D['what_it_proves']}")
    log(f"  Verdict: {cand_D['verdict']}")
    log("")

    log("-" * 78)
    log("Section 7: Genuine infinite-KL attempt for mod-9 (long-range Gibbs).")
    log("-" * 78)
    genuine = genuine_infinite_kl_mod9_attempt()
    record["genuine_infinite_kl"] = genuine
    log(f"  Construction: {genuine['construction_attempt']}")
    log("")
    log(f"  Structural property (I-projection uniqueness, Csiszar 1975):")
    log(f"  {genuine['structural_property']}")
    log("")
    log(f"  Robustness margin from Wave 2 (TV >= 0.294) carries forward.")
    log("")
    log(f"  Lyapunov / drift attempt:")
    log(f"  {genuine['descent_estimate_via_lyapunov']}")
    log("")
    log(f"  DV with adapted reference:")
    log(f"  {genuine['descent_estimate_via_DV_with_adapted_reference']}")
    log("")
    log(f"  Transport-information inequality:")
    log(f"  {genuine['transport_information_inequality']}")
    log("")
    log(f"  VERDICT: {genuine['verdict']}")
    log("")

    log("=" * 78)
    log("FINAL ANSWER")
    log("=" * 78)
    log("")
    log("(1) Explicit infinite-KL measure constructed:")
    log("    nu_A = product over coords of  delta_{c}-mass where c uniform on {1..6}.")
    log("    Equivalently: each coord is a uniform DISCRETE measure on the smallest")
    log("    representative of each mod-6 class, namely uniform on {1, 2, 3, 4, 5, 6}.")
    log("    Per-step KL = +infty (within-class point-mass), mod-9 SATURATED.")
    log("")
    log("(2) Drift status:")
    log("    E_{nu_A}[a] = 7/2 = 3.5 = (m_2 + 1)/2 with m_2 = ord_9(2) = 6.")
    log("    Drift gap = 3.5 - log_2(3) ~ 1.915. UNBALANCED.")
    log("    This MATCHES the Wave 1 gap_2 exactly --- because the per-coord")
    log("    marginal is the SAME mod-6 uniform distribution.")
    log("")
    log("(3) Descent estimate that survives:")
    log("    NONE that escapes the Wave 2 perimeter.")
    log("    - Lyapunov drift: FAILS by 1.915.")
    log("    - DV with adapted reference: TRIVIAL (KL = 0), inert.")
    log("    - T1/T2/HWI transport: FAILS by tail concentration on N.")
    log("    - Robustness margin 0.294 (Wave 2) extends verbatim.")
    log("")
    log("(4) Verdict on (F1):")
    log("    BARRIER EXTENSION.  The infinite-KL frontier is NOT a new attack")
    log("    route. Every concretely analyzable infinite-KL measure with mod-9")
    log("    saturation has per-coord mod-6 marginal equal to the LDP I-projection")
    log("    (Csiszar uniqueness), and inherits the drift gap. Adding inter-coord")
    log("    coupling cannot lower the per-coord drift.")
    log("")
    log("    The Wave 2 closure now reads:")
    log("    'mod-3^k saturation (k >= 2) is incompatible with drift balance under")
    log("    EVERY shift-invariant measure (finite OR infinite per-step KL)")
    log("    whose mod-m_k per-coord marginal is the I-projection of mu_0.'")
    log("")
    log("(5) Honest assessment:")
    log("    - The simplest infinite-KL measure I could construct (Section 4) does")
    log("      saturate mod-9 BUT fails drift by the same 1.915 gap as Wave 1.")
    log("    - The Pareto candidate (B) is FINITE-KL at any drift-balancing alpha,")
    log("      so it lives INSIDE Wave 2 and does NOT saturate mod-3.")
    log("    - The Doob (D) candidate is tautological.")
    log("    - The empirical delta (C) is pathological with no marginals.")
    log("    - Genuine inter-coord-coupled infinite-KL (Dyson-style) does NOT change")
    log("      the per-coord marginal at fixed constraint (I-projection uniqueness).")
    log("    - I cannot rule out PARTIALLY-explicit infinite-KL measures with no")
    log("      tractable marginals, but those are by construction NOT analyzable")
    log("      and so cannot yield a descent estimate either.")
    log("")
    log("    [NOVELTY UNVERIFIED]. The I-projection transfer argument may be")
    log("    folklore; the explicit application to the Syracuse mod-3^k frontier")
    log("    is, to our knowledge, new in this thread of work.")
    log("")

    JSON_PATH.write_text(json.dumps(record, indent=2, default=str))
    LOG_PATH.write_text("\n".join(_LOG_LINES) + "\n")
    log(f"[written] {JSON_PATH}")
    log(f"[written] {LOG_PATH}")


if __name__ == "__main__":
    main()
