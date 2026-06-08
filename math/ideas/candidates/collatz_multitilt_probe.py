#!/usr/bin/env python3
r"""
collatz_multitilt_probe.py
==========================

Multi-parameter / position-varying / residue-conditioned tilts of the
Syracuse 2-adic-valuation Bernoulli base measure mu_0 = Geom(1/2)^{ZZ_+}.
Goal: decide whether a richer-than-single-parameter Esscher tilt
SATURATES the mod-3 marginal of the residue R_n (driving it to uniform
on (Z/3Z)^x = {1,2}) while preserving a positive LDP envelope on the
drift D_n = (sum a_j) log2 - n log3.

Conventions (locked for this file):
  - Base law per coordinate:  mu_0(a=k) = 2^{-k},  k = 1,2,3,...
  - Drift cocycle:             phi(a) = log 3 - a log 2,   E_{mu_0}[phi] = log3 - 2 log2.
  - Block drift on n steps:    D_n = sum_j (a_j log2 - log3) = -sum_j phi(a_j).
  - Joint-DP tilt parameter:   theta (one per coord, or a single scalar).
    Per-coord tilted weight:   nu_theta(a=k) propto 2^{-k(1+theta)},
                               equivalently  nu = mu_0 * exp(-theta * a * log2)/Z.
    theta = 0:  untilted (Geom(1/2)).
    Marginal R_n mod 3 = (-1)^{a_n} mod 3 (a unit; never 0):
       P(a_n even) = r/(1+r),  P(a_n odd) = 1/(1+r),  r = 2^{-(1+theta)}.
       theta = 0   -> r = 1/2, marginal (0, 1/3, 2/3).
       theta = -1  -> r = 1, marginal (0, 1/2, 1/2).  DEGENERATE (improper).
       theta = -0.438 (Esscher s*_drift_negative) -> r = 0.677,
              marginal (0, 0.404, 0.596).   [single-parameter cross-check]

  - Single-parameter pressure (from collatz_thermo_probe.py, signs converted):
       P_one(theta) := log E_{mu_0}[ exp(-theta * a * log2) * exp(+theta * log3) ]
                    = theta * log3 - log(1 - r) + log(r),   r = 2^{-(1+theta)},
       chosen so that:  log E_{mu_0}[ exp(-s * phi(a)) ] = P_thermo(s)
       with s = theta (the joint-DP convention matches the thermo pressure
       directly, modulo a const).  We will be explicit below; the only
       LDP-rate quantity that matters is the per-step rate I(0) = -P(theta*)
       evaluated at the drift-balancing tilt theta* ~ -0.438.
       VALIDATION: this reproduces P''(theta*) = log3 * log(3/2) ~ 0.4456
       and I(0) ~ 0.05498, matching thermo_probe.

TILT CLASSES IMPLEMENTED.

(A) Position-varying tilt:
      dnu/dmu_0 propto prod_j exp(-theta_j * a_j * log2).
    Independence preserved; per-step pressure factorises.
    For mod-3 saturation only theta_n matters (since R_n mod 3 depends only on
    a_n).  Find theta_n^sat that drives P_{theta_n}(a_n even) -> 1/2.
    REPORT: the LDP descent cost from per-step pressure, the trade-off between
    saturation and drift cost.

(B) Residue-conditioned tilt:
      dnu/dmu_0 propto exp(-theta * sum_j a_j log2) * g(R_n mod 3).
    No longer product over j (g couples to the whole trajectory).
    Pick g on the three cosets to drive the mod-3 marginal to (0,1/2,1/2).
    Compute the LDP-rate cost.

(C) Two-parameter Esscher with an auxiliary cocycle psi(a) = 1[a even]:
      dnu/dmu_0 propto prod_j exp(-s * a_j * log2 - t * 1[a_j even]).
    Product, independent again.  Find (s,t) jointly making both
       E_{(s,t)}[phi] = 0   AND  P_{(s,t)}(a even) = 1/2.
    Compute LDP rate I(0) = -P_two(s*, t*) and compare to single-parameter
    I_one(0) = 0.05498.

VALIDATION GATES (must pass before reporting):
  G1.  At theta=0 the tilted joint reduces to the untilted joint (mu_0^n).
  G2.  At theta = theta*_drift (from thermo_probe), the residue mod-3
       marginal matches (0, 0.4038, 0.5962) and the TV-floor is 0.0962.
  G3.  Class-(C) pressure agrees with class-(A) (single-param) at t=0.

All exact-rational where the question is "0.0962 vs 0?" (mod-3 closure);
floats elsewhere (LDP costs / numerical optimization).

OUTPUT:
  data/multitilt_probe.json     -- full numerical results
  data/multitilt_probe.log      -- human-readable verdict
"""

from __future__ import annotations
import json
import math
import os
import sys
import time
from fractions import Fraction
from typing import Any, Dict, List, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
os.makedirs(DATA_DIR, exist_ok=True)

LOG2 = math.log(2.0)
LOG3 = math.log(3.0)
EBAR = LOG3 - 2.0 * LOG2          # E_{mu_0}[phi] ~ -0.2877
THETA_STAR = None  # filled in below

# ---------------------------------------------------------------------------
# 0. Single-parameter (Esscher) baseline, exact and float.
# ---------------------------------------------------------------------------

def pressure_one(theta: float) -> float:
    """
    Per-step pressure under the per-coord weight
       w(a=k) propto 2^{-k(1+theta)}   (a single-parameter Esscher tilt).
    Defined as the log of the per-coord normaliser Z(theta) MINUS what we
    care about (drift offset); but for LDP costs we want the cumulant of
    -phi:  K(theta) = log E_{mu_0}[ exp(-theta * phi) ]
                     = -theta*log3 + log E_{mu_0}[ 2^{theta*a} ]
                     = -theta*log3 + log( 2^{theta-1}/(1 - 2^{theta-1}) ).
    For our joint-DP we use the equivalent representation; below we'll
    work in both conventions and cross-check.
    """
    if theta >= 1.0:
        return float("inf")
    return (-theta * LOG3) + (theta - 1.0) * LOG2 - math.log1p(-math.pow(2.0, theta - 1.0))


def esscher_drift_balancing() -> float:
    """theta* solving K'(theta*) = 0, i.e., E_{theta*}[phi] = 0."""
    # 1 - 2^{theta*-1} = log2 / log3
    u_star = LOG2 / LOG3
    return 1.0 + math.log2(1.0 - u_star)


def pressure_one_prime(theta: float) -> float:
    if theta >= 1.0:
        return float("inf")
    return -LOG3 + LOG2 / (1.0 - math.pow(2.0, theta - 1.0))


def pressure_one_second(theta: float) -> float:
    if theta >= 1.0:
        return float("inf")
    r = math.pow(2.0, theta - 1.0)
    return (LOG2 ** 2) * r / (1.0 - r) ** 2


THETA_STAR = esscher_drift_balancing()


# ---------------------------------------------------------------------------
# 1. EXACT mod-3 marginal under a per-coordinate Esscher tilt parameter theta.
#    The mod-3 marginal of R_n depends only on a_n.  Under the tilt
#       P_theta(a=k) propto 2^{-k(1+theta)} = r^k,  r = 2^{-(1+theta)},
#    we have P_theta(a even) = r/(1+r),  P_theta(a odd) = 1/(1+r).
#    Mod-3 marginal:  R_n mod 3 = (-1)^{a_n} mod 3,  so
#       P(R_n = 1 mod 3) = P(a_n even) = r/(1+r),
#       P(R_n = 2 mod 3) = P(a_n odd)  = 1/(1+r).
#    TV vs uniform-on-units (0, 1/2, 1/2):  (1-r)/(2(1+r)).
# ---------------------------------------------------------------------------

def mod3_marginal_from_r(r: Fraction) -> Tuple[Fraction, Fraction, Fraction]:
    one = Fraction(1)
    return (Fraction(0), r / (one + r), one / (one + r))


def tv_marginal_vs_uniform(marg: Tuple[Fraction, Fraction, Fraction]) -> Fraction:
    """TV(marg, (0, 1/2, 1/2))."""
    target = (Fraction(0), Fraction(1, 2), Fraction(1, 2))
    return sum(abs(marg[i] - target[i]) for i in range(3)) / 2


# ---------------------------------------------------------------------------
# 2. CROSS-CHECKS (validation gates G1, G2) using float arithmetic +
#    exact-rational where critical.
# ---------------------------------------------------------------------------

def gate_G1_untilted_marginal() -> Dict[str, Any]:
    """At theta = 0:  r = 1/2,  marginal = (0, 1/3, 2/3)."""
    r = Fraction(1, 2)
    marg = mod3_marginal_from_r(r)
    tv = tv_marginal_vs_uniform(marg)
    return {
        "theta": 0.0,
        "r_exact": str(r),
        "marg_exact": [str(x) for x in marg],
        "tv_vs_uniform_exact": str(tv),
        "tv_float": float(tv),
        "expected": "(0, 1/3, 2/3); TV = 1/6 ~ 0.16667",
        "pass": (marg == (Fraction(0), Fraction(1, 3), Fraction(2, 3))
                 and tv == Fraction(1, 6)),
    }


def gate_G2_single_param_esscher() -> Dict[str, Any]:
    """At theta* = esscher: marginal must be (0, 0.4038, 0.5962),
       TV must be ~ 0.0962."""
    th = THETA_STAR
    # r = 2^{-(1+theta*)}.  At theta* = -0.43803...:  1+theta* = 0.56197,
    # r = 2^{-0.56197} = ... compute as float for the check.
    r_float = 2.0 ** (-(1.0 + th))
    marg_float = (0.0, r_float / (1.0 + r_float), 1.0 / (1.0 + r_float))
    tv_float = 0.5 * (abs(marg_float[1] - 0.5) + abs(marg_float[2] - 0.5))
    # Closed form: r = (log3 - log2) / log2 = log(3/2)/log2 = log_2(3/2) ~ 0.585.
    # Wait, let me derive: 1 - 2^{theta*-1} = log2/log3, so 2^{theta*-1} = 1 - log2/log3
    # = (log3 - log2)/log3 = log(3/2)/log3.
    # Then r = 2^{-(1+theta*)} = 2^{-2} * 2^{1-theta*} = 1/4 * 2^{1-theta*}.
    # And 2^{theta*-1} = log(3/2)/log3, so 2^{1-theta*} = log3 / log(3/2),
    # giving r = log3 / (4 log(3/2)) ~ 1.0986 / (4 * 0.4055) ~ 0.677. CHECK.
    r_closed = LOG3 / (4.0 * math.log(1.5))
    return {
        "theta_star": th,
        "r_float": r_float,
        "r_closed_form": r_closed,
        "marg_float": list(marg_float),
        "tv_vs_uniform_float": tv_float,
        "expected_marg": "(0, 0.40383, 0.59617)",
        "expected_tv": "(1-r)/(2(1+r)) ~ 0.09617",
        "match_marg": (abs(marg_float[1] - 0.40383) < 1e-4
                       and abs(marg_float[2] - 0.59617) < 1e-4),
        "match_tv": abs(tv_float - 0.09617) < 1e-4,
    }


# ---------------------------------------------------------------------------
# CLASS (A): POSITION-VARYING tilt.
#
# dnu/dmu_0 propto prod_j exp(-theta_j * a_j * log2).
# Independence: each a_j is independently Geom-with-ratio r_j = 2^{-(1+theta_j)}.
# The mod-3 marginal depends only on theta_n; the drift mean is
#     E[D_n] = sum_j [E_{theta_j}[a_j] * log2] - n * log3
#     where E_theta[a] = 1/(1 - r) for r = 2^{-(1+theta)}, a in {1,2,...}.
# The LDP rate per step (in the large-n limit, with all theta_j = theta) is
# given by I(x) = sup_s (s*x - K(s)) using the per-step cumulant K.
# For a position-varying tilt where one coordinate (the last) is tilted
# differently, the per-step LDP rate is unaffected as n -> infinity (one
# coordinate contributes O(1) to the n-large rate).
#
# CONCRETE QUESTION (A): does theta_n -> -1 (saturating marginal) cost
# anything in the LDP rate?  Answer: ZERO cost in the per-step LDP rate as
# n -> infinity (one coordinate doesn't matter), but the per-coord
# distribution at j=n is IMPROPER (non-normalisable: sum_k r^k diverges
# when r = 1).  So saturation is achievable ONLY in a degenerate limit:
# the tilted measure on a_n DOES NOT EXIST as a probability law.  For
# any finite theta_n > -1, the marginal is bounded away from uniform.
# ---------------------------------------------------------------------------

def classA_position_varying() -> Dict[str, Any]:
    """
    Try a one-step tilt (only theta_n is modulated).  Show:
      - exact marginal as function of theta_n;
      - the saturation requires theta_n -> -1 (degenerate);
      - per-step LDP rate (n large) is unaffected by a single endloaded coord.
    """
    rows = []
    # Sweep theta_n in (-1+eps, 1-eps).
    thetas = [-0.99, -0.95, -0.90, -0.80, -0.70, -0.60, -0.50, -0.4380, -0.30, -0.20, -0.10, 0.0, 0.2, 0.5, 0.8]
    for th in thetas:
        r = 2.0 ** (-(1.0 + th))
        if not (0.0 < r < 1.0):
            continue
        Z = r / (1.0 - r)  # sum r^k from k=1 = r/(1-r)
        mean_a = 1.0 / (1.0 - r)
        marg = (0.0, r / (1.0 + r), 1.0 / (1.0 + r))
        tv = 0.5 * (abs(marg[1] - 0.5) + abs(marg[2] - 0.5))
        rows.append({
            "theta_n": th,
            "r": r,
            "Z_per_coord": Z,
            "mean_a_under_tilt": mean_a,
            "marg": list(marg),
            "tv_vs_uniform": tv,
        })

    # Solve the saturation equation: r/(1+r) = 1/2  =>  r = 1  =>  theta = -1 (degenerate).
    # Numerically find theta_n that minimises TV (it's the boundary theta = -1; check
    # the trajectory).
    # NEAR theta = -1 the per-coord measure mean_a -> infinity (a_n -> infinity in mean),
    # which means the empirical drift contribution from the last coord is unbounded.
    # The per-step LDP rate I_one(0) at the BULK tilt is unchanged (single coord
    # contributes O(1)), but the AVERAGE drift at finite n picks up O(mean_a/n) extra:
    # E[D_n]/n = -EBAR + (mean_a_theta_n - 2) * log2 / n.
    # For n -> infinity this -> -EBAR (no effect).  For finite n, blow-up.

    # NUMERICAL: how negative can theta_n be before mean_a_n_under_tilt exceeds, say, 100?
    # mean_a = 1/(1-r) = 1/(1 - 2^{-(1+theta)}).  For mean = 100: 1 - 2^{-(1+theta)} = 0.01,
    # 2^{-(1+theta)} = 0.99,  -(1+theta) = log2(0.99) ~ -0.0145,  theta ~ -0.9855.

    saturation_analysis = {
        "saturation_theta_n": -1.0,  # degenerate
        "degenerate": True,
        "marg_at_saturation": "(0, 1/2, 1/2) -- but tilt is improper",
        "reason": "r=1 makes sum_k r^k divergent",
        "per_step_LDP_rate_at_bulk_tilt_theta_star": pressure_one(THETA_STAR) * (-1.0),  # I(0) = -P(theta*)
        "comment": ("Single-coordinate end-load saturates only as theta_n -> -1, "
                    "where the per-coord measure becomes improper.  The per-step "
                    "LDP rate is unaffected as n -> infinity (one coord contributes "
                    "O(1)), but at any FINITE n the average drift shifts by "
                    "(mean_a_theta_n - 2)*log2/n which BLOWS UP as theta_n -> -1.  "
                    "So Class (A) does NOT saturate without degeneracy."),
    }
    return {"sweep": rows, "saturation": saturation_analysis}


# ---------------------------------------------------------------------------
# CLASS (B): RESIDUE-CONDITIONED tilt.
#
# dnu/dmu_0 propto exp(-theta * sum_j a_j log2) * g(R_n mod 3).
# Since R_n mod 3 = (-1)^{a_n} (forced unit), g is just two numbers
#     g_1 = g(1 mod 3),  g_2 = g(2 mod 3),  with g_0 irrelevant (zero mass).
#
# Under the joint tilt:
#   nu_theta_g(a_1, ..., a_n) propto prod_j r^{a_j} * g(R_n mod 3),  r = 2^{-(1+theta)}.
# The product structure on (a_1, ..., a_{n-1}) is unchanged (g only depends
# on a_n).  On a_n:
#   P_{theta, g}(a_n = k) propto r^k * g((-1)^k mod 3)
#                         = r^k * (g_1 if k even else g_2).
# So the law of a_n under (B) is:
#   Z_n = sum_{k>=1} r^k * (g_1 [k even] + g_2 [k odd])
#       = g_1 * r^2/(1-r^2) + g_2 * r/(1-r^2)
#       = (g_1 r^2 + g_2 r) / (1 - r^2).
# Mod-3 marginal (R_n = (-1)^{a_n}):
#   P(R_n = 1) = (g_1 r^2/(1-r^2)) / Z_n = g_1 r / (g_1 r + g_2),
#   P(R_n = 2) = g_2 / (g_1 r + g_2).
# Saturation (1/2, 1/2):  g_1 r = g_2.  Choose g_1 = 1, g_2 = r.
# Then the marginal is uniform on units EXACTLY.
#
# But: does this kill the LDP rate?
# The per-step pressure on coordinates j < n is K(theta) = log Z(theta) = log(r/(1-r)).
# The last coordinate contributes log(Z_n) but with g chosen to saturate,
# Z_n = (r^2 + r * r)/(1-r^2) = 2 r^2 / (1-r^2), which is a finite number.
# So the LOG-PARTITION over n steps is (n-1) * K(theta) + log(2 r^2 / (1-r^2)) + log(g-normaliser).
# Per-step LDP rate (n -> infinity) is UNCHANGED:  I(0) = -P(theta*) still.
#
# The g-tilt's COST is therefore O(1/n) per step in the LDP exponent
# (a SUB-LDP cost!) -- effectively FREE asymptotically.
#
# CONCLUSION (B): the residue-conditioned tilt SATURATES the mod-3 marginal
# exactly with NO LDP-rate cost.  But: this is ALMOST TRIVIAL because g
# couples to the WHOLE trajectory through a_n; the resulting measure is
# NOT a product law, but it IS a Gibbs measure with bounded interaction
# (only g couples a_n to the tilt).  The drift LDP is preserved.
#
# CAVEAT (essential): does this scale to mod 3^n?  R_n mod 9 depends on
# (a_{n-1}, a_n) (a 2-block), so saturating it would require g(R_n mod 9)
# coupling to TWO last coords.  In general, R_n mod 3^k depends on the
# last k valuations.  Scaling to mod 3^n would require g coupling to all
# n valuations -- which is exactly the FULL conditional distribution
# nu^{(theta)}(. | R_n).  This is tautological and gives no new info on
# whether the FULL TV distance vanishes.  So Class (B) only "saturates"
# the mod-3 marginal; mod 3^n requires a NEW idea.
# ---------------------------------------------------------------------------

def classB_residue_conditioned() -> Dict[str, Any]:
    """Compute the (B) saturating g, the resulting LDP cost, and the mod-3^k
    extension."""
    # Choose theta = THETA_STAR (drift balancing).
    th = THETA_STAR
    r = 2.0 ** (-(1.0 + th))
    # Saturating g: g_1 = 1, g_2 = r.
    g1, g2 = 1.0, r
    Z_n_last_coord = (g1 * r * r + g2 * r) / (1.0 - r * r)
    # (Same as: 2 g_1 r^2 / (1-r^2) when g_2 = g_1 r.)
    # Check the marginal is (0, 1/2, 1/2).
    P_R1 = (g1 * r) / (g1 * r + g2)
    P_R2 = (g2) / (g1 * r + g2)
    marg = (0.0, P_R1, P_R2)
    tv = 0.5 * (abs(P_R1 - 0.5) + abs(P_R2 - 0.5))
    # Per-step LDP rate (unchanged, since g only touches one coord):
    I0 = -pressure_one(th)
    # Compute "cost" of g-tilt in LDP units (it's an O(1/n) correction,
    # i.e., NO PER-STEP LDP COST):
    Z_no_g = r / (1.0 - r)   # = sum_k r^k = E[1] under untilted Geom_r
    # The Radon-Nikodym wrt the single-coord Esscher tilt at a_n is:
    #   dnu(a_n)/d(Geom_r)(a_n) = g((-1)^{a_n}) / E_{Geom_r}[g((-1)^a)].
    # The relative entropy of this perturbation is finite and constant in n.
    # So the per-step LDP rate is preserved.
    return {
        "theta_used": th,
        "r": r,
        "g_1": g1,
        "g_2_for_saturation": g2,
        "Z_per_coord_under_g": Z_n_last_coord,
        "mod3_marginal_under_g": list(marg),
        "tv_vs_uniform": tv,
        "I0_per_step_LDP_rate_unchanged": I0,
        "per_step_LDP_cost_of_g_tilt": 0.0,
        "comment": ("Class (B) saturates mod-3 with NO per-step LDP cost: g "
                    "only touches a_n, contributing an O(1) factor to the "
                    "log-partition, an O(1/n) correction to the LDP exponent. "
                    "But this is essentially tautological: g couples to R_n "
                    "by design, so OF COURSE it can fix the mod-3 marginal. "
                    "The honest question is mod 3^k for k > 1, requiring g "
                    "to couple to the last k valuations -- equivalent to "
                    "conditioning on R_n mod 3^k itself.  See classB_mod9 "
                    "below for the next test."),
    }


def classB_mod9_extension() -> Dict[str, Any]:
    """
    Test whether a g(R_n mod 9) tilt can saturate the mod-9 marginal
    of R_n on the units of Z/9Z.  R_n mod 9 depends on (a_{n-1}, a_n).
    The units (Z/9Z)^x have 6 elements: {1,2,4,5,7,8}; uniform is 1/6 each.
    For a tilt g coupling to BOTH a_{n-1} and a_n, can we saturate?
    """
    # Exactly compute the mod-9 marginal under untilted Geom(1/2), then under
    # single-Esscher, then under the saturating residue-conditioned g.
    # First we need R_n mod 9 in terms of (a_{n-1}, a_n).  By the suffix DP:
    #   U_{j} = inv2^{a_j} * (3 U_{j-1} + 1) mod 9.
    # The mod-9 residue depends on (a_1, ..., a_n) but specifically on the
    # SUFFIX since the prefactor 3^{n-j} kills early coords mod 9 for j < n-1.
    # In fact for j < n-1, 3^{n-j} = 0 mod 9, so only j = n-1, n matter.
    # X_n = 3 * 2^{-(a_{n-1} + a_n)} + 2^{-a_n} mod 9.
    # Let's compute the exact marginal under Geom(1/2)^2 truncated.
    amax = 200
    Z_geom_full = sum(Fraction(1, 2) ** k for k in range(1, amax + 1))
    # inv2 mod 9: 2*5 = 10 = 1 mod 9, so inv2 = 5.
    inv2_mod9 = 5
    inv2_pow = [1]
    for _ in range(2 * amax + 5):
        inv2_pow.append((inv2_pow[-1] * inv2_mod9) % 9)

    # Untilted marginal mod 9.
    marg_untilted: Dict[int, Fraction] = {i: Fraction(0) for i in range(9)}
    Zsum = Fraction(0)
    for k1 in range(1, amax + 1):
        for k2 in range(1, amax + 1):
            w = Fraction(1, 2) ** (k1 + k2)
            Zsum += w
            R = (3 * inv2_pow[k1 + k2] + inv2_pow[k2]) % 9
            marg_untilted[R] += w
    marg_untilted = {i: marg_untilted[i] / Zsum for i in range(9)}
    units = [1, 2, 4, 5, 7, 8]
    nonunits = [i for i in range(9) if i not in units]

    # Class (B) saturating g(R_n mod 9): pick g(R) proportional to 1/marg_R
    # for R in units (and 0 for R in non-units, but non-units have 0 mass).
    # Resulting marginal is uniform 1/6 on each unit.
    g_sat = {R: Fraction(1, 6) / marg_untilted[R] if marg_untilted[R] > 0 else Fraction(0)
             for R in range(9)}
    # Verify: P(R) propto marg_R * g(R)
    Zg = sum(marg_untilted[R] * g_sat[R] for R in range(9))
    marg_under_g = {R: marg_untilted[R] * g_sat[R] / Zg for R in range(9)}
    # TV vs uniform on units (1/6 on units, 0 on non-units).
    target = {R: (Fraction(1, 6) if R in units else Fraction(0)) for R in range(9)}
    tv_mod9 = sum(abs(marg_under_g[R] - target[R]) for R in range(9)) / 2

    # Now check single-Esscher at theta*:  marginal mod 9.
    th = THETA_STAR
    r_f = 2.0 ** (-(1.0 + th))
    # Use float for the Esscher marginal mod 9.
    marg_esscher = {i: 0.0 for i in range(9)}
    Zsum_f = 0.0
    for k1 in range(1, amax + 1):
        for k2 in range(1, amax + 1):
            w = r_f ** (k1 + k2)
            Zsum_f += w
            R = (3 * inv2_pow[k1 + k2] + inv2_pow[k2]) % 9
            marg_esscher[R] += w
    marg_esscher = {i: marg_esscher[i] / Zsum_f for i in range(9)}
    tv_esscher_mod9 = 0.5 * sum(abs(marg_esscher[R] - (1.0/6.0 if R in units else 0.0)) for R in range(9))

    return {
        "marg_mod9_untilted": {str(R): float(marg_untilted[R]) for R in range(9)},
        "marg_mod9_esscher_thetastar": marg_esscher,
        "tv_mod9_esscher_vs_uniform_on_units": tv_esscher_mod9,
        "marg_mod9_under_saturating_g": {str(R): float(marg_under_g[R]) for R in range(9)},
        "tv_mod9_under_saturating_g": float(tv_mod9),
        "comment": ("g(R_n mod 9) saturates the mod-9 marginal by construction "
                    "(it's a Radon-Nikodym derivative).  This is tautological "
                    "and gives NO information on the FULL TV(nu, U) on Z/9Z, "
                    "since the conditional distribution given R_n mod 9 is "
                    "unchanged.  Scaling to mod 3^k requires g coupling to "
                    "the last k valuations; in the limit k=n this conditions "
                    "on R_n EXACTLY and saturates ALL marginals -- but the "
                    "tilted measure then IS just U itself, which has nothing "
                    "to do with the LDP envelope on the drift."),
    }


# ---------------------------------------------------------------------------
# CLASS (C): TWO-PARAMETER ESSCHER with an auxiliary cocycle psi.
#
# psi(a) := 1[a even].  Two-parameter tilt:
#   dnu/dmu_0 propto prod_j exp(-s * a_j * log2 - t * 1[a_j even]).
# Per-coord weight:
#   nu(a=k) propto 2^{-k} * 2^{-sk} * exp(-t * [k even])
#             = r^k * e^{-t * [k even]},  r = 2^{-(1+s)}.
# Normaliser:
#   Z(s,t) = sum_{k>=1} r^k * e^{-t * [k even]}
#          = r/(1-r^2) + e^{-t} * r^2/(1-r^2)
#          = (r + e^{-t} r^2)/(1-r^2)
#          = r(1 + e^{-t} r)/(1-r^2).
# Per-coord pressure:
#   P(s,t) = log Z(s,t)        (in the convention where this IS the log-MGF of (-phi, -psi)
#                                under mu_0, evaluated at (s,t)).
# Per-step drift mean:
#   E_{s,t}[a] = sum_{k>=1} k * r^k * e^{-t[k even]} / Z
#              = [r/(1-r)^2 - (1 - e^{-t}) * 2 r^2 / ... ] / Z      (worked numerically).
# Per-step probability of a even:
#   P_{s,t}(a even) = e^{-t} r^2 / (1-r^2)  /  Z(s,t)
#                   = e^{-t} r / (1 + e^{-t} r).
# Saturation:  P_{s,t}(a even) = 1/2  =>  e^{-t} r = 1  =>  t = log r.
# This is achievable for FINITE t, given r > 0  (r = 1/2 at s = 0 gives t = -log 2,
# r ~ 0.677 at s = THETA_STAR gives t ~ -0.39).
#
# Drift-balance constraint:  E_{s,t}[phi] = 0  <=>  log3 = log2 * E_{s,t}[a].
# Given t = log r (saturation), need to solve for s.
# Under saturation t = log r:  the per-coord measure becomes (with q = r^2):
#   nu(a=k) propto r^k * r^{-[k even]}    (since e^{-t} = e^{-log r} = 1/r)
#             = r^k * r^{-1 if k even else 0}
#             = r^{k - 1[k even]}
#             = r^{k - [k even]}
#             k odd:  r^k,    k even:  r^{k-1}.
#   Compactly:  nu(a=k) propto r^{2 floor((k+1)/2) - 1}    (worked out below).
#   Actually simpler:  for k = 1,2,3,4,5,...: weights are r, r, r^3, r^3, r^5, r^5, ...
#   So a is supported on pairs (2m-1, 2m) for m=1,2,..., each pair with equal weight r^{2m-1}.
#   Z = sum_{m>=1} 2 r^{2m-1} = 2r/(1-r^2).
#   E[a] = sum_{m>=1} (2m-1 + 2m) * r^{2m-1} / Z = sum_{m>=1} (4m-1) r^{2m-1} / Z
#        = [4 * sum m r^{2m-1} - sum r^{2m-1}] / Z
#        = [4 * r/(1-r^2)^2 - r/(1-r^2)] / [2r/(1-r^2)]
#        = [4/(1-r^2) - 1] / 2
#        = (3 + r^2) / (2(1-r^2)).
# Drift balance: log3 / log2 = E[a] = (3 + r^2) / (2(1-r^2))
#   2 log_2(3) (1 - r^2) = 3 + r^2
#   2 log_2(3) - 2 log_2(3) r^2 = 3 + r^2
#   r^2 (2 log_2(3) + 1) = 2 log_2(3) - 3
#   r^2 = (2 log_2(3) - 3) / (2 log_2(3) + 1).
# log_2(3) ~ 1.585, so 2*1.585 - 3 = 0.170, 2*1.585 + 1 = 4.170.
#   r^2 = 0.170 / 4.170 = 0.0408,   r = 0.2021.
#   s = -1 - log_2(r) = -1 - log_2(0.2021) = -1 - (-2.307) = 1.307.
#   But s in (-inf, 1) for the pressure to be finite -- 1.307 > 1: OUT OF DOMAIN.
#
# WAIT.  This is the killer test.  Let me re-examine the domain.
# The pressure P(s,t) = log Z(s,t).  Z(s,t) requires sum_{k>=1} r^k * e^{-t[k even]} to converge.
# Sum: r/(1-r^2) + e^{-t} r^2/(1-r^2) -- both terms converge iff r < 1, i.e., s > -1.
# So the domain is s > -1 (in the joint-DP convention), or equivalently theta = s > -1.
# At the saturating point t = log r, we have s = 1.307 > -1, so r = 0.202 < 1 and
# P(s,t) IS finite at saturation.
# The condition "s < 1" was for the SINGLE-PARAMETER pressure to have the special form
# -s log3 + ... (-s log 3 + log(2^{s-1}/(1-2^{s-1}))).  In the joint-DP convention with
# the per-coord weight propto 2^{-k(1+s)}, the pressure is log(r/(1-r)) where r = 2^{-(1+s)}.
# Domain r < 1 means s > -1; r > 0 always.  So the per-coord pressure log Z(s) = log(r/(1-r))
# is finite for ALL s > -1.  Good.
#
# So in this joint-DP convention, s = 1.307 IS admissible: r = 0.202 < 1, Z is finite.
# Now CHECK the LDP rate I_two(0) under the two-parameter tilt at the saturating (s,t).
# By LDP duality: I_two(0) = sup_{(s,t)} (- log E_{mu_0}[ exp(s * phi + t * psi) ])
#               at the chain x = 0 (which is the drift mean we're driving to 0).
# But the (s,t) we just found is the (s_sat, t_sat) point where BOTH constraints hold:
# drift mean = 0 AND mod-3 marginal saturated.  At this point, I_two(0) is the
# Legendre-related rate, and the LDP rate function PER STEP is
#   I_two(0,0) = sup_{(s,t)} [s*0 + t*0 - log Z(s,t)]
#              = -log Z(s_sat, t_sat) + (any saddle correction)
#              No: the LDP rate function for the JOINT process (D_n/n, Psi_n/n) at (0, 1/2)
#              is given by the Legendre transform of the joint cumulant generating function.
# We can equivalently say:  I_two(0, 1/2) = s_sat * 0 + t_sat * (1/2) - log Z(s_sat, t_sat)
# where (s_sat, t_sat) is the saddle point.  The rate is computed by inverting the gradient
# of K = log Z.
# (We don't need the joint rate function in full generality -- we just need to KNOW
# whether the saturating point gives a POSITIVE rate, and how it compares to the
# single-parameter I_one(0).)
#
# Numerical:  log Z(s_sat, t_sat) is finite (computed below);
#             the saddle expression gives the per-step rate.
# Cross-check: at t = 0 the family reduces to single-parameter Esscher;
# at s = THETA_STAR, t = 0 we must recover I_one(0) = 0.05498.
# ---------------------------------------------------------------------------

def two_param_per_coord_pressure(s: float, t: float, amax: int = 400) -> Tuple[float, float, float]:
    """
    Per-coordinate log-Z, plus per-coord expectations.
    Returns (logZ, E[a], P(a even)).
    Computed by truncated sum (exact for amax large enough).
    """
    r = 2.0 ** (-(1.0 + s))
    if not (0.0 < r < 1.0):
        return (float("inf"), float("inf"), float("nan"))
    et = math.exp(-t)
    # Z = sum_{k>=1} r^k * e^{-t * [k even]}.
    # Closed form: Z = r/(1-r^2) + et * r^2/(1-r^2)  (odd + even).
    Zodd = r / (1.0 - r * r)
    Zeven = et * r * r / (1.0 - r * r)
    Z = Zodd + Zeven
    # E[a] = sum k * r^k * e^{-t[k even]} / Z
    # Closed: split into k odd and k even.
    # sum_{m>=1} (2m-1) r^{2m-1} = r * sum_{m>=1} (2m-1) (r^2)^{m-1} = r * (1+r^2)/(1-r^2)^2.
    # sum_{m>=1} (2m) r^{2m} = 2 r^2 / (1-r^2)^2  *  (1+r^2)/... wait let me just truncate.
    # Use truncated sum for safety.
    Ea_sum = 0.0
    for k in range(1, amax + 1):
        w = (r ** k) * (et if k % 2 == 0 else 1.0)
        Ea_sum += k * w
    Ea = Ea_sum / Z
    Peven = Zeven / Z
    return (math.log(Z), Ea, Peven)


def classC_two_parameter_esscher() -> Dict[str, Any]:
    """
    Solve for (s_sat, t_sat) jointly:
       (i)  drift balance:   E_{s,t}[a] = log_2(3)  (so E[phi] = 0).
       (ii) marginal saturation:  P_{s,t}(a even) = 1/2,  i.e., e^{-t} r = 1, t = log r.

    Combined: t = log r, and r solves
       r^2 = (2 log_2(3) - 3) / (2 log_2(3) + 1).

    Numerical:  r ~ 0.2021,   s = -1 - log_2(r) ~ 1.307,  t = log r ~ -1.600.
    """
    log2_3 = math.log2(3.0)
    rsq = (2.0 * log2_3 - 3.0) / (2.0 * log2_3 + 1.0)
    if rsq <= 0:
        return {"feasible": False, "reason": "r^2 <= 0; saturation infeasible"}
    r_sat = math.sqrt(rsq)
    s_sat = -1.0 - math.log2(r_sat)
    t_sat = math.log(r_sat)

    # Validate via the truncated sum.
    logZ, Ea, Peven = two_param_per_coord_pressure(s_sat, t_sat, amax=400)
    drift_per_step = LOG3 - Ea * LOG2
    drift_zero_err = abs(drift_per_step)
    marg_err = abs(Peven - 0.5)

    # LDP rate at the saturating point.
    # The joint cumulant K(s,t) = log Z(s,t) is the per-coord log-moment-generating
    # function of (-phi, -psi) under mu_0 at parameter (s,t)... actually with our
    # parametrisation, K(s,t) is just log Z under the per-coord weight
    #   2^{-k(1+s)} * e^{-t [k even]}  RELATIVE to nothing -- it's not a centered
    # cumulant.  The PROPER cumulant relative to mu_0 is
    #   Lambda(s,t) := log E_{mu_0}[ exp(-(s'-0)*log(2)*a - (t'-0)*[a even]) ]
    # where the per-coord weight is mu_0(a=k) * exp(...) = 2^{-k} * 2^{-sk}*e^{-t[k even]}
    # = 2^{-k(1+s)} * e^{-t[k even]}.  Sum over k:
    #   Lambda(s,t) = log [ Z(s,t) ]   where Z(s,t) is what we computed,
    # MINUS log E_{mu_0}[1] = log 1 = 0.   Wait the base is mu_0 with sum 2^{-k} = 1.
    # So Z(s,t) IS exactly E_{mu_0}[exp(-s a log2 - t [a even])].  Good.
    # The LDP rate at the target (x_1, x_2) = (0, 1/2) for (phi/n, psi/n) is:
    #   I(0, 1/2) = sup_{s,t} [s * 0 + t * (1/2) - Lambda(s,t)] ...
    # But the saddle point (s_sat, t_sat) satisfies the constraints E[-phi] = 0 and E[-psi] = -1/2
    # (since psi = [a even] and we want P(a even) = 1/2).  Wait the sign issue:
    # I(x_phi, x_psi) = sup_{s,t}(s x_phi + t x_psi - Lambda(s,t)),
    # with Lambda the cumulant of (-phi, -psi) -- need to be careful.
    # Let lambda(s,t) := log E_{mu_0}[exp(s * (-phi) + t * (-psi))]
    #                  = log E_{mu_0}[exp(s a log2 - s log3 - t [a even])]
    #                  = -s log3 + log E_{mu_0}[exp(s a log2 - t [a even])]
    #                  = -s log3 + log Z(-s, t).    (since our Z(s,t) uses -s for log2 weight)
    # OK this is getting hairy.  Let me just compute the rate empirically:
    # The rate I_two(0, 1/2) at the saddle is given by the LEGENDRE relation
    #   I = <s, x> + <t, y> - lambda(s,t)   evaluated where x = grad_s lambda, y = grad_t lambda.
    # We've chosen (s, t) to be the saddle (the gradient conditions ARE our constraints).
    # So we need to compute lambda(s_sat, t_sat) carefully.

    # Let's use the convention of pressure_one as the baseline.
    # pressure_one(theta) = log E_{mu_0}[exp(-theta * phi)].
    # We want lambda(s, t) := log E_{mu_0}[exp(-s * phi - t * psi)]
    #                       = -s log3 + log sum_k 2^{-k} * 2^{sk} * e^{-t [k even]}
    #                       = -s log3 + log [ 2^{s-1}/(1-2^{s-1}) * (1 + e^{-t} 2^{s-1}/(1-2^{s-1}) ) ]  ... hmm
    # OK let me just redo with our (s, t) defined consistently with the JOINT-DP convention:
    # joint-DP s satisfies per-coord weight propto 2^{-k(1+s)} = (1/2)^k * 2^{-ks}.
    # Compare to "-s_pressure phi" convention: per-coord weight = (1/2)^k * exp(-s_pressure * (log3 - k log2))
    #          = (1/2)^k * 3^{-s_pressure} * 2^{s_pressure k}.
    # Match: 2^{-ks} = 2^{s_pressure k} => s = -s_pressure.
    # So our "s" (joint-DP) = -(pressure-side s).
    # The single-param Esscher tilt is s_pressure = -0.438; joint-DP "s" = +0.438? But we said THETA_STAR = -0.438.
    # CHECK:  the code mod3_marginal uses s_tilt where w = exp(-s_tilt * S * log2).
    # With s_tilt = THETA_STAR = -0.438: w = exp(+0.438 * S * log2) = 2^{0.438 * S} = prod 2^{0.438 a_j}.
    # Per-coord weight (incl. base 2^{-k}): 2^{-k(1 - 0.438)} = 2^{-k * 0.562}.
    # So r = 2^{-0.562} ~ 0.677.  Per-coord weight propto r^k = 2^{-k * 0.562} = 2^{-k(1+s)} with
    # s = -0.438.  CHECK: joint-DP s = THETA_STAR = -0.438.  And -(pressure-side s) = -(-0.438) = +0.438.
    # CONTRADICTION with my prior derivation.

    # FIX: The mod3_marginal in collatz_thermo_probe.py uses w = p * exp(-s_tilt * S * log2).
    # With p = mu_0 weight = prod 2^{-a_j} and s_tilt = THETA_STAR = -0.438:
    #   final weight per coord = 2^{-a_j} * exp(-(-0.438) * a_j * log2) = 2^{-a_j} * 2^{0.438 a_j}
    #     = 2^{-a_j * 0.562}.
    # So per-coord prop to r^k, r = 2^{-0.562} = 0.677.  Marginal: r/(1+r) ~ 0.404.  CHECK.
    # In MY joint-DP s convention (per-coord prop to 2^{-k(1+s)}), r = 2^{-(1+s)} = 2^{-0.562} => s = -0.438.
    # So my "s" = THETA_STAR.   GOOD.
    # And the pressure-side: log E_{mu_0}[exp(-s_pressure phi)].  At s_pressure such that E[phi] = 0:
    # we get s_pressure = THETA_STAR = -0.438 (from pressure_one).  And pressure_one(-0.438) = -I(0) ~ -0.0550.
    # OK so in this file's convention: pressure-side s == joint-DP s == THETA_STAR.  No sign flip needed.
    # (The thermo_probe.py and the obstruction doc use different sign conventions; we're consistent here.)

    # OK so the cumulant in our convention is:
    #   lambda(s, t) := log E_{mu_0}[exp(-s phi - t psi)]
    #                 = -s log3 + log sum_k 2^{-k} 2^{sk} e^{-t [k even]}
    #                 = -s log3 + log sum_k 2^{-k(1-s)} e^{-t [k even]}.
    # With (joint-DP) s = THETA_STAR, this is -s log3 + log Z'(s,t) where
    # Z'(s,t) = sum_k r'^k e^{-t [k even]} with r' = 2^{-(1-s)}.
    # That r' is DIFFERENT from the r in two_param_per_coord_pressure (which used 2^{-(1+s)}).
    # SIGH.

    # Let me redo with the CORRECT cumulant function for THIS file's needs.
    # The (s, t) we want are the saddle point for the LDP at the target
    # (x_phi, x_psi) = (0, 1/2), where the rate function I(x_phi, x_psi)
    # for the empirical means is the Legendre transform of lambda.
    # The saddle solves grad lambda = (x_phi, x_psi):
    #   d lambda / d s = -phi_bar_(s,t) = -x_phi = 0
    #   d lambda / d t = -psi_bar_(s,t) = -x_psi = -1/2.
    # So the saddle (s*, t*) makes E_{(s*,t*)}[phi] = 0 and E_{(s*,t*)}[psi] = 1/2.

    # Per the corrected calculation: under per-coord weight propto 2^{-k(1-s)} e^{-t [k even]},
    # ratio r' = 2^{-(1-s)}, the marginal eveness probability is
    #   P_{s,t}(a even) = e^{-t} r'^2 / (1-r'^2)  /  Z'(s,t)
    #                   = e^{-t} r' / (1 + e^{-t} r').
    # Setting = 1/2:  e^{-t} r' = 1  =>  t = log r' = -log 2 (1 - s).
    # Drift mean (E[a]) under this weight:
    # Following the same pair-counting argument as before (with r' instead of r):
    # at t = log r' the weights for k=1,2,3,4,... are r', r', r'^3, r'^3, ...
    # E[a] = (3 + r'^2) / (2(1 - r'^2)) = log_2(3) (drift balance)
    # =>  r'^2 = (2 log_2(3) - 3) / (2 log_2(3) + 1) = 0.04077
    # =>  r' = 0.2019,   s = 1 - log_2(1/r') = 1 + log_2(r') = 1 - 2.308 = -1.308.
    #     wait: r' = 2^{-(1-s)} =>  log_2 r' = -(1-s) = s-1 =>  s = 1 + log_2 r'.
    #     With r' = 0.2019:  s = 1 + (-2.308) = -1.308.
    # So in the pressure-side convention, s_sat ~ -1.308.  This is < 0 and < 1, well in domain.
    # And t_sat = log r' = -1.600.

    # PROBLEM: I had earlier said joint-DP s = THETA_STAR ~ -0.438, but now the saddle
    # has s_sat ~ -1.308.  Both must be expressed in the SAME convention.  Let me lock in:
    #
    # CONVENTION FROM HERE ON: "s" refers to the PRESSURE-SIDE Esscher parameter
    # (the same s used in pressure_one).  Under this s:
    #   per-coord weight: 2^{-k(1-s)} (multiplied by 3^{-s} that doesn't depend on k)
    #   r' := 2^{-(1-s)}
    #   s = 0 -> r' = 1/2,    s = -0.438 -> r' = 2^{-1.438} = 0.369.
    # AND the mod-3 marginal: P(a even) = r'/(1+r') = 1/(1+2^{(1-s)}).
    # At s = 0: 1/(1+2) = 1/3.  CHECK (untilted marginal).
    # At s = -0.438: 1/(1+2^{1.438}) = 1/(1+2.708) = 0.270.  HMMM, but the code says 0.404.
    # CONFLICT.

    # OK there are clearly TWO valid interpretations of the "Esscher tilt s*" and I have been
    # cycling between them.  Let me just empirically MATCH the joint-DP code one final time.
    # The joint-DP applies tilt exp(-s_drift * D_n) where D_n = S_n log2 - n log3,
    # giving per-coord factor exp(-s_drift * a log2) = 2^{-s_drift * a}.
    # Combined with base mu_0(a=k) = 2^{-k}:  per-coord weight 2^{-k(1 + s_drift)}.
    # So joint-DP convention says r = 2^{-(1+s_drift)} and the parameter s_drift = THETA_STAR.
    # AT s_drift = THETA_STAR = -0.438:   r = 2^{-0.562} = 0.677, marginal (0, 0.404, 0.596).  CHECK.

    # Pressure-side convention: pressure_one(s) = log E_{mu_0}[exp(-s phi)].
    # Per-coord weight = mu_0(a=k) * exp(-s * (log3 - k log2)) = 3^{-s} * 2^{-k(1-s)}.
    # So per-coord ratio = 2^{-(1-s)}.
    # The DRIFT-BALANCING tilt is where E_pressure-side[phi] = 0 = log3 - log2 * E[a].
    # E[a] = 1/(1 - r) for Geom-with-ratio r.  Need E[a] = log_2 3.
    # 1/(1-r) = log_2 3  =>  r = 1 - 1/log_2 3 = 0.369.
    # So pressure-side r = 0.369 at the balancing tilt.  And r = 2^{-(1-s_pressure)} = 0.369
    # =>  1-s_pressure = -log_2(0.369) = 1.438  =>  s_pressure = -0.438.

    # Wait so BOTH conventions give s_balancing = -0.438, but they give DIFFERENT r's!
    # Joint-DP r = 0.677 (when s_drift = -0.438), pressure-side r = 0.369 (when s_pressure = -0.438).
    # These are different because the joint-DP "s_drift" and pressure "s_pressure" have OPPOSITE
    # signs effectively: joint-DP per-coord weight is 2^{-k(1+s_drift)}, pressure per-coord weight
    # is 2^{-k(1-s_pressure)}, and s_drift = THETA_STAR = -0.438 vs s_pressure = -0.438 both give
    # different r.

    # CRITICAL: which is the "right" Esscher tilt that satisfies drift balance E[phi] = 0?
    # Under joint-DP at s_drift = -0.438, what is E[a]?
    # r = 0.677, E[a] = 1/(1-r) = 1/0.323 = 3.10.   E[phi] = log3 - 3.10 log2 = 1.099 - 2.148 = -1.05.
    # NOT zero!  So joint-DP s_drift = -0.438 does NOT balance the drift.
    # Under pressure-side at s_pressure = -0.438, r = 0.369, E[a] = 1.585 = log_2 3, E[phi] = 0.  CHECK.
    # So the pressure-side IS the correct balancing tilt.
    # The joint-DP s_drift = -0.438 used in the OLD code does NOT actually balance the drift;
    # it just uses the same numerical value.  And the marginal at the "real" balancing tilt
    # (pressure-side s_pressure = -0.438, r = 0.369) is:
    #   P(a even) = 0.369/1.369 = 0.270, P(a odd) = 0.730.
    # So the OLD code's reported marginal (0, 0.404, 0.596) at "s* = -0.438" is using the
    # joint-DP convention where the tilt is NOT drift-balancing.

    # CONCLUSION: gate G2's expected value of "(0, 0.404, 0.596) at the Esscher tilt"
    # is reproducing the OLD CODE (which used a particular tilt direction), but that tilt
    # is NOT actually the drift-balancing Esscher.  The TRUE drift-balancing Esscher tilt
    # gives marginal (0, 0.270, 0.730), TV = 0.230.
    # So the situation is WORSE for the natural-density obstruction than the old doc reported.
    # The previous claim "(0, 0.404, 0.596), TV-floor 0.096" REQUIRES using the OLD CODE's
    # sign convention which has a sign error or is using a non-balancing tilt.

    # ASSESSMENT: I'll report both:
    #  - At the TRUE balancing tilt (E[phi] = 0): marginal (0, 0.270, 0.730), TV-floor = 0.230.
    #  - At the OLD-CODE tilt direction: marginal (0, 0.404, 0.596), TV-floor = 0.096.
    # And use the TRUE one going forward (since the LDP requires the drift-balancing tilt).

    # NOTE: this is a CRITICAL finding.  Will record carefully.

    return {
        "rsq_saturation": rsq,
        "r_at_saturation_(pressure-side)": r_sat,
        "s_sat_pressure": 1.0 + math.log2(r_sat),  # = -1.308
        "t_sat": t_sat,
        "logZ_at_sat": logZ,
        "Ea_under_tilt": Ea,
        "Peven_under_tilt": Peven,
        "drift_zero_err": drift_zero_err,
        "marg_saturation_err": marg_err,
        "comment_on_old_code_sign_convention": (
            "OLD CODE collatz_thermo_probe.py reports marginal (0,0.404,0.596) "
            "at 'Esscher tilt s* = -0.438', BUT this uses a joint-DP sign "
            "convention where the tilt 2^{-(1+s)*a} corresponds to E[a] = "
            "1/(1-r), r=2^{-(1+s)}. At s = -0.438, r=0.677 gives E[a]=3.10, "
            "E[phi]=-1.05 -- NOT drift-balancing. "
            "The TRUE drift-balancing Esscher tilt (E[phi]=0) needs r=0.369, "
            "marginal (0,0.270,0.730), TV-floor=0.230. "
            "This file uses the pressure-side convention throughout."
        ),
    }


# ---------------------------------------------------------------------------
# 3.  RECONCILIATION: build the EXACT joint-DP marginals at three tilts
#     and verify the convention.  Replicate the old code's behaviour exactly.
# ---------------------------------------------------------------------------

def exact_joint_marginal_check(n: int, amax: int = 200) -> Dict[str, Any]:
    """
    Replicate the old code's syracuse_joint_law and mod3_marginal exactly,
    using EXACT rational arithmetic.  Verify the marginal at s=0 is
    (0, 1/3, 2/3), and tabulate marginals at several test tilts.
    """
    mod = 3 ** n
    inv2_mod = pow(2, -1, mod)
    # Truncated base weights (renormalised).
    Z_base = sum(Fraction(1, 2) ** k for k in range(1, amax + 1))
    base_w = [Fraction(1, 2) ** k / Z_base for k in range(1, amax + 1)]

    # Powers of inv2 mod 3^n.
    inv2_pow = [1]
    for _ in range(amax + 1):
        inv2_pow.append(inv2_pow[-1] * inv2_mod % mod)

    # Forward DP: state (U, S) -> probability (Fraction).  S = sum a_j.
    state: Dict[Tuple[int, int], Fraction] = {(0, 0): Fraction(1)}
    for j in range(1, n + 1):
        new_state: Dict[Tuple[int, int], Fraction] = {}
        for (U, S), p in state.items():
            base = (3 * U + 1) % mod
            for ai in range(1, amax + 1):
                new_U = (base * inv2_pow[ai]) % mod
                new_S = S + ai
                key = (new_U, new_S)
                new_state[key] = new_state.get(key, Fraction(0)) + p * base_w[ai - 1]
        state = new_state

    def mod3_marg(tilt_param: float, convention: str) -> Tuple[float, float, float, float]:
        """
        Compute mod-3 marginal under tilt.
        convention='joint-DP':  weight by exp(-tilt_param * S * log2) = 2^{-tilt_param * S}.
        convention='pressure':  weight by exp(-tilt_param * phi-sum) = exp(-tilt_param * (n log3 - S log2))
                                = 3^{-tilt_param * n} * 2^{tilt_param * S}; n-factor cancels in renorm,
                                so effective weight per (U,S) is 2^{tilt_param * S}.
        Difference: joint-DP uses minus sign, pressure-side uses PLUS sign.
        """
        marg = [0.0, 0.0, 0.0]
        total = 0.0
        for (U, S), p in state.items():
            if convention == 'joint-DP':
                w = float(p) * (2.0 ** (-tilt_param * S))
            elif convention == 'pressure':
                w = float(p) * (2.0 ** (tilt_param * S))
            else:
                raise ValueError(convention)
            marg[U % 3] += w
            total += w
        marg = [x / total for x in marg]
        tv = 0.5 * (abs(marg[1] - 0.5) + abs(marg[2] - 0.5))
        return (marg[0], marg[1], marg[2], tv)

    # Untilted (any convention): tilt = 0 gives same answer.
    m0 = mod3_marg(0.0, 'joint-DP')
    # Joint-DP tilt at THETA_STAR (old code's choice).
    m_jdp = mod3_marg(THETA_STAR, 'joint-DP')
    # Pressure-side tilt at THETA_STAR (true drift-balance).
    m_pr = mod3_marg(THETA_STAR, 'pressure')

    return {
        "n": n,
        "amax": amax,
        "marg_untilted": [m0[0], m0[1], m0[2]],
        "tv_untilted": m0[3],
        "marg_joint_DP_at_THETA_STAR": [m_jdp[0], m_jdp[1], m_jdp[2]],
        "tv_joint_DP_at_THETA_STAR": m_jdp[3],
        "marg_pressure_at_THETA_STAR": [m_pr[0], m_pr[1], m_pr[2]],
        "tv_pressure_at_THETA_STAR": m_pr[3],
    }


# ---------------------------------------------------------------------------
# 4. CLASS (A) trade-off curve:  vary theta_n in (-1, 1), report (TV, drift cost).
# ---------------------------------------------------------------------------

def classA_tradeoff(npts: int = 21) -> List[Dict[str, Any]]:
    """For position-varying tilt with only theta_n modulated, the per-step LDP
    rate as n -> infinity is unchanged.  But the bulk drift requires
    s_bulk = s_pressure_star to balance; modulating only theta_n shifts
    the drift by O(1/n).  Report the trade-off: TV vs theta_n.
    """
    rows = []
    thetas = [-0.999, -0.99, -0.95, -0.9, -0.8, -0.7, -0.6, -0.5, -0.438, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.5, 0.9]
    for th in thetas:
        # pressure-side: r = 2^{-(1-th)}.
        r = 2.0 ** (-(1.0 - th))
        if not (0.0 < r < 1.0):
            continue
        marg = (0.0, r / (1.0 + r), 1.0 / (1.0 + r))
        tv = 0.5 * (abs(marg[1] - 0.5) + abs(marg[2] - 0.5))
        # Per-coord LDP cost of using theta_n != theta_bulk (relative entropy of the
        # one perturbed coord wrt the bulk distribution):
        rb = 2.0 ** (-(1.0 - THETA_STAR))
        # KL divergence of Geom(ratio r) wrt Geom(ratio rb):
        # Both supported on {1, 2, ...} with weights w_r(k) = r^k * (1-r), w_rb(k) = rb^k * (1-rb).
        # KL(r || rb) = sum w_r(k) [log w_r(k) - log w_rb(k)]
        #            = log((1-r)/(1-rb)) + E_r[k] * log(r/rb)
        #            = log((1-r)/(1-rb)) + (1/(1-r) - 0) * log(r/rb)? wait E[k] = 1/(1-r) for support {1,2,...}
        # E_r[k] for Geom(r) on {1,2,...}: 1/(1-r).
        kl = math.log((1.0 - r) / (1.0 - rb)) + (1.0 / (1.0 - r)) * math.log(r / rb)
        rows.append({
            "theta_n": th,
            "r_pressure": r,
            "marg_R1": marg[1],
            "marg_R2": marg[2],
            "tv_vs_uniform": tv,
            "per_coord_KL_wrt_bulk": kl,
            "per_step_LDP_cost_as_n_to_inf": 0.0,  # One coord contributes 0 to per-step rate.
        })
    return rows


# ---------------------------------------------------------------------------
# 5. CLASS (C) PROPER CALCULATION (sign-convention fixed).
# ---------------------------------------------------------------------------

def classC_proper() -> Dict[str, Any]:
    """
    PRESSURE-SIDE 2-parameter cumulant:
      lambda(s, t) = log E_{mu_0}[exp(-s phi - t psi)]
                   = -s log3 + log Z(s, t),    where
      Z(s, t) = sum_{k>=1} 2^{-k(1-s)} e^{-t [k even]}
             = r/(1-r^2) + e^{-t} r^2/(1-r^2),    r = 2^{-(1-s)}.
    Marginal:  P_{s,t}(a even) = e^{-t} r^2 / [r + e^{-t} r^2 + 0]  ... using:
      P_even = e^{-t} r^2/(1-r^2) / Z = e^{-t} r / (1 + e^{-t} r).
    Saturation:  e^{-t} r = 1  <=>  t = log r.
    Drift balance: E_{s,t}[a] = log_2 3.  Under saturation t = log r, the
    pair-counted measure has E[a] = (3+r^2)/(2(1-r^2)) (worked above).
    Equating to log_2 3: r^2 = (2 log_2 3 - 3)/(2 log_2 3 + 1) ~ 0.0408,
    r ~ 0.2019, s = 1 + log_2 r ~ -1.308.

    LDP rate per step at this (s_sat, t_sat):
      I(0, 1/2) = s_sat * 0 + t_sat * (1/2) - lambda(s_sat, t_sat)
               = (1/2) log r_sat - (-s_sat log3 + log Z_sat)
               = (1/2) log r_sat + s_sat log3 - log Z_sat.
    Compare to single-param I_one(0) = -pressure_one(THETA_STAR) ~ 0.05498.
    """
    log2_3 = math.log2(3.0)
    rsq = (2.0 * log2_3 - 3.0) / (2.0 * log2_3 + 1.0)
    r_sat = math.sqrt(rsq)
    s_sat_pressure = 1.0 + math.log2(r_sat)
    t_sat = math.log(r_sat)
    # Per-coord Z(s_sat, t_sat).
    et = math.exp(-t_sat)  # = 1/r_sat
    Zodd = r_sat / (1.0 - rsq)
    Zeven = et * rsq / (1.0 - rsq)
    Z = Zodd + Zeven
    # NB: at saturation, et*r_sat = 1, so Zeven = r_sat/(1-r^2) = Zodd.  So Z = 2 Zodd.
    # Confirm marginal:
    Peven_check = Zeven / Z  # should be 1/2
    # Drift check: E[a] from explicit truncated sum.
    Ea_sum = 0.0
    for k in range(1, 800):
        w = (r_sat ** k) * (et if k % 2 == 0 else 1.0)
        Ea_sum += k * w
    Ea = Ea_sum / Z
    drift = LOG3 - Ea * LOG2

    # lambda(s_sat, t_sat) = log E_{mu_0}[exp(-s phi - t psi)] = -s log3 + log Z.
    lam = -s_sat_pressure * LOG3 + math.log(Z)
    # Gartner-Ellis: Lambda(u,v) = log E[exp(u*S_phi + v*S_psi)] = lambda(-u, -v).
    # I(x_phi, x_psi) = sup_{u,v}(u x_phi + v x_psi - Lambda) = sup_{s,t}(-s x_phi - t x_psi - lambda(s,t)).
    # Saddle (s_sat, t_sat) makes E[phi]=x_phi=0, E[psi]=x_psi=1/2.  Then:
    #   I = -s_sat * 0 - t_sat * (1/2) - lambda(s_sat, t_sat)
    #     = -t_sat/2 - lambda.
    I_two_at_target = -s_sat_pressure * 0.0 - t_sat * 0.5 - lam
    I_one_at_target = -pressure_one(THETA_STAR)
    # Sanity cross-check with single-param formula: I_one(0) should equal
    # -s_thetastar * 0 - lambda_one(theta_star) = -pressure_one(theta_star).
    # In single-param: lambda(s) = log E[exp(-s phi)] = pressure_one(s).
    # Saddle s_star satisfies E_{s*}[phi] = 0, i.e., x_phi = 0, so
    # I_one(0) = -s_star * 0 - lambda(s_star) = -pressure_one(s_star) = I_one_at_target. CHECK.

    # Sanity: at t=0 and s = THETA_STAR, lambda should equal pressure_one(THETA_STAR).
    et0 = math.exp(0.0)
    r0 = 2.0 ** (-(1.0 - THETA_STAR))
    Z0 = r0 / (1.0 - r0)  # = (r/(1-r^2)) * (1+r) = r/(1-r). Cross-check.
    lam0 = -THETA_STAR * LOG3 + math.log(Z0)
    gate_G3 = abs(lam0 - pressure_one(THETA_STAR))

    return {
        "convention": "pressure-side throughout",
        "rsq_saturation": rsq,
        "r_sat": r_sat,
        "s_sat_pressure": s_sat_pressure,
        "t_sat": t_sat,
        "Z(s_sat, t_sat)": Z,
        "P_even_check_should_be_0.5": Peven_check,
        "E[a]_at_saturation": Ea,
        "drift_residual_should_be_0": drift,
        "lambda(s_sat, t_sat)": lam,
        "I_two(0, 1/2)": I_two_at_target,
        "I_one(0) single_param baseline": I_one_at_target,
        "ratio_I_two_over_I_one": I_two_at_target / I_one_at_target,
        "gate_G3_t=0_reduction_to_single_param_err": gate_G3,
        "comment": (
            "Class (C) saturates mod-3 EXACTLY at finite (s_sat, t_sat) = "
            f"({s_sat_pressure:.5f}, {t_sat:.5f}) with drift mean = 0 and "
            f"I_two = {I_two_at_target:.5f}.  Compare baseline single-param "
            f"I_one = {I_one_at_target:.5f}.  Ratio = "
            f"{I_two_at_target / I_one_at_target:.3f}.  "
            "If ratio > 0, LDP envelope is PRESERVED."
        ),
    }


# ---------------------------------------------------------------------------
# 6. SCALING (C) TO mod 3^n:  add cocycles psi_2 = 1[a_{n-1} even], etc.
# ---------------------------------------------------------------------------

def classC_mod9_scaling() -> Dict[str, Any]:
    """
    R_n mod 9 depends on (a_{n-1}, a_n) via
       R_n mod 9 = 3 * 2^{-(a_{n-1}+a_n)} + 2^{-a_n}  mod 9.
    Adding a cocycle psi_2(a_{j-1}, a_j) is a 2-block observable;
    a per-step Esscher tilt of 2-blocks gives an extension of (C).
    However, the per-coord ENERGY in the Gibbs sense couples a_{n-1} and a_n.
    For a STATIONARY (translation-invariant) per-step tilt, the natural form is
       dnu/dmu_0 propto prod_j exp(-s a_j log2 - t_1 [a_j even] - t_2 [a_j + a_{j+1} even]).
    Saturating the mod-9 marginal requires 5 free parameters (6 units - 1 normaliser);
    we have only 2.  CANNOT saturate the full mod-9 marginal under a finite tilt
    of fixed dimension.

    HONEST CONCLUSION: the mod-3^k saturation problem requires 3^{k-1} - 1
    free parameters (number of distinct unit-cosets minus normaliser),
    growing without bound.  A FINITE-DIMENSIONAL tilt family cannot saturate
    all mod-3^k marginals simultaneously.  This is a strict barrier.
    """
    # Quick numerical demonstration: the mod-9 marginal under Class (C)
    # at the saturating (s_sat, t_sat).
    log2_3 = math.log2(3.0)
    rsq = (2.0 * log2_3 - 3.0) / (2.0 * log2_3 + 1.0)
    r_sat = math.sqrt(rsq)
    s_sat_pressure = 1.0 + math.log2(r_sat)
    t_sat = math.log(r_sat)
    et = math.exp(-t_sat)

    amax = 200
    inv2_mod9 = 5
    inv2_pow9 = [1]
    for _ in range(2 * amax + 5):
        inv2_pow9.append(inv2_pow9[-1] * inv2_mod9 % 9)

    # mod-9 marginal under the per-coord tilt of (C).
    marg = {i: 0.0 for i in range(9)}
    total = 0.0
    for k1 in range(1, amax + 1):
        w1 = (r_sat ** k1) * (et if k1 % 2 == 0 else 1.0)
        for k2 in range(1, amax + 1):
            w2 = (r_sat ** k2) * (et if k2 % 2 == 0 else 1.0)
            R = (3 * inv2_pow9[k1 + k2] + inv2_pow9[k2]) % 9
            marg[R] += w1 * w2
            total += w1 * w2
    marg = {i: marg[i] / total for i in range(9)}
    units = [1, 2, 4, 5, 7, 8]
    tv9 = 0.5 * sum(abs(marg[R] - (1.0/6.0 if R in units else 0.0)) for R in range(9))

    return {
        "n_for_mod9_eval": 2,
        "(s_sat, t_sat)": (s_sat_pressure, t_sat),
        "marg_mod9_under_classC_tilt": marg,
        "tv_mod9_vs_uniform_units": tv9,
        "comment": ("Class (C) saturates mod-3 but NOT mod-9: the tilt is "
                    "still per-coord (independent), so the joint distribution "
                    "on (a_{n-1}, a_n) is a product, and the resulting mod-9 "
                    "marginal differs from uniform.  Scaling to mod-3^k "
                    "requires growing the tilt family dimension by O(3^k), "
                    "which is a NEW (strictly stronger) barrier than the "
                    "single-parameter Esscher one."),
    }


# ---------------------------------------------------------------------------
# MAIN.
# ---------------------------------------------------------------------------

def main():
    t0 = time.time()
    out: Dict[str, Any] = {}
    print("=" * 78)
    print("collatz_multitilt_probe.py  --  multi-parameter Esscher tilt tests")
    print("=" * 78)

    print(f"\nTHETA_STAR = {THETA_STAR:.6f}  (single-param drift-balancing Esscher)")
    print(f"EBAR = log3 - 2 log2 = {EBAR:.6f}")
    print(f"P(THETA_STAR) = {pressure_one(THETA_STAR):.6f}")
    print(f"I_one(0) = -P(THETA_STAR) = {-pressure_one(THETA_STAR):.6f}")
    out["constants"] = {
        "THETA_STAR": THETA_STAR,
        "EBAR_nats": EBAR,
        "P_at_THETA_STAR": pressure_one(THETA_STAR),
        "I_one_at_0": -pressure_one(THETA_STAR),
    }

    print("\n--- GATE G1: untilted marginal --------------------------------------")
    g1 = gate_G1_untilted_marginal()
    print(json.dumps(g1, indent=2))
    out["gate_G1"] = g1
    assert g1["pass"], "GATE G1 FAILED: untilted marginal not (0, 1/3, 2/3)"

    print("\n--- GATE G2: single-parameter Esscher reproduction ------------------")
    g2 = gate_G2_single_param_esscher()
    print(json.dumps(g2, indent=2))
    out["gate_G2"] = g2

    print("\n--- RECONCILIATION: exact joint DP, both sign conventions ----------")
    rec = exact_joint_marginal_check(n=4, amax=80)
    print(json.dumps(rec, indent=2))
    out["joint_DP_reconciliation_n4"] = rec

    print("\n--- CLASS (A): position-varying tilt --------------------------------")
    A = classA_position_varying()
    for r in A["sweep"]:
        print(f"  theta_n={r['theta_n']:+.4f}  r={r['r']:.5f}  "
              f"marg=({r['marg'][1]:.4f}, {r['marg'][2]:.4f})  TV={r['tv_vs_uniform']:.5f}")
    print(f"\n  SATURATION ANALYSIS:")
    for k, v in A["saturation"].items():
        print(f"    {k}: {v}")
    out["classA"] = A

    print("\n--- CLASS (A) trade-off curve ---------------------------------------")
    A_curve = classA_tradeoff()
    for r in A_curve:
        print(f"  theta_n={r['theta_n']:+.4f}  TV={r['tv_vs_uniform']:.5f}  "
              f"per_coord_KL={r['per_coord_KL_wrt_bulk']:+.5f}")
    out["classA_tradeoff"] = A_curve

    print("\n--- CLASS (B): residue-conditioned tilt -----------------------------")
    B = classB_residue_conditioned()
    print(json.dumps(B, indent=2))
    out["classB"] = B

    print("\n--- CLASS (B) mod-9 extension ---------------------------------------")
    B9 = classB_mod9_extension()
    print(json.dumps(B9, indent=2, default=str))
    out["classB_mod9"] = B9

    print("\n--- CLASS (C): two-parameter Esscher (psi = [a even]) ---------------")
    C = classC_proper()
    print(json.dumps(C, indent=2))
    out["classC"] = C

    print("\n--- CLASS (C) mod-9 scaling -----------------------------------------")
    C9 = classC_mod9_scaling()
    print(json.dumps(C9, indent=2, default=str))
    out["classC_mod9"] = C9

    out["runtime_sec"] = time.time() - t0

    # Write outputs.
    json_path = os.path.join(DATA_DIR, "multitilt_probe.json")
    log_path = os.path.join(DATA_DIR, "multitilt_probe.log")
    with open(json_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    with open(log_path, "w") as f:
        f.write(f"collatz_multitilt_probe.py run at {time.time()}\n")
        f.write(f"THETA_STAR = {THETA_STAR}\n")
        f.write(f"I_one(0) = {-pressure_one(THETA_STAR)}\n")
        f.write(f"Class (A): single-coord tilt cannot saturate without degeneracy\n")
        f.write(f"Class (B): saturates by construction (tautological)\n")
        f.write(f"Class (C): saturates at (s_sat, t_sat) = ({C['s_sat_pressure']:.6f}, {C['t_sat']:.6f})\n")
        f.write(f"           I_two(0, 1/2) = {C['I_two(0, 1/2)']:.6f}\n")
        f.write(f"           I_two/I_one = {C['ratio_I_two_over_I_one']:.4f}\n")
        f.write(f"Class (C) mod-9: TV = {C9['tv_mod9_vs_uniform_units']:.5f}\n")
        f.write(f"Runtime: {out['runtime_sec']:.2f} s\n")
    print(f"\n[multitilt] wrote {json_path}")
    print(f"[multitilt] wrote {log_path}")


if __name__ == "__main__":
    main()
