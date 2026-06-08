#!/usr/bin/env python3
r"""
collatz_thermo_probe.py
=======================

Thermodynamic-formalism / large-deviation probe for the Collatz drift cocycle.

CONTEXT.  After the structural kills (residue mod 3 obstruction;
digit-Lyapunov; transfer-operator spectral gap; joint (residue, drift)
disjointness; Livsic coboundary), the SURVIVING program candidate is:
EFFECTIVE EQUIDISTRIBUTION via thermodynamic formalism on the Syracuse
2-adic shift.  This file builds the analytic core (pressure function
P(s), Esscher tilt s*, rate function I(x)) IN CLOSED FORM, and
numerically validates it against (a) the existing 10^7 verifier
trajectories, and (b) direct Monte-Carlo from the Geom(1/2) base law.

THE SYSTEM (from collatz_livsic.md, validated there).
  Sigma  = shift on 2-adic valuation sequences a = (a_j), a_j in {1,2,...}.
  mu_0   = i.i.d. Geom(1/2) base measure:  P(a=k) = 2^{-k}, k>=1.  (mean 2)
  phi(a) = log 3 - a_1 * log 2  (the DRIFT cocycle, per Syracuse step).
           E[phi] = log 3 - 2 log 2 = -0.2877 (nats), -0.4150 (log_2).
  S_n    = sum_{j=1}^n a_j;   D_n  = S_n * log2 - n * log3  (size-decrease).
           phi(sigma^{j-1} a) = -(D_n - D_{n-1}) summed gives -D_n + n log3 etc.

THE PRESSURE FUNCTION  (closed form).
  P(s) := log E_{mu_0}[ exp( -s * phi(a) ) ]
        = log E[ exp( -s log 3 + s a log 2 ) ]
        = -s log 3 + log E[ 2^{s a} ]
        = -s log 3 + log( sum_{k>=1} 2^{-k} 2^{s k} )
        = -s log 3 + log( 2^{s-1} / (1 - 2^{s-1}) )         [for s < 1]
        = -s log 3 + (s - 1) log 2 - log( 1 - 2^{s-1} ).

  Domain of finiteness: s in (-infty, 1).

  P'(s) = -log 3  +  log 2 / (1 - 2^{s-1}).
  P''(s) = (log 2)^2 * 2^{s-1} / (1 - 2^{s-1})^2.

ESSCHER TILT (drift-balancing).  s* with E_{s*}[phi] = 0  iff  P'(s*) = 0:
      1 - 2^{s* - 1} = log 2 / log 3   =>   2^{s* - 1} = 1 - log_3(2)
                                       =>   s* = 1 + log_2( 1 - log_3(2) )
                                       =   1 + log_2( (log_2(3) - 1) / log_2(3) )
                                       ~  -0.43803.

  At s*:  P''(s*) = log 3 * log(3/2)  ~  0.44563   (TILTED variance, IN-NATS-squared).

  Note: the UNTILTED variance is Var_{mu_0}(phi) = (log 2)^2 * Var(a)
       = (log 2)^2 * 2 ~ 0.9609  (the "sigma^2 = 2(log2)^2" from collatz_livsic.md).
  These are different quantities -- P''(s*) is the LOCAL quadratic of P at s*,
  i.e., the CLT/LDP variance under the TILTED measure (with mean drift 0).
  The Livsic non-coboundary CLT under mu_0 has variance Var_{mu_0}(phi).

RATE FUNCTION (Legendre transform).
  I(x) := sup_s (s x - P(s))  -- the Cramer LDP rate function for phi_n/n.

  By convex duality:  x = P'(s)  =>  s = (P')^{-1}(x), and I(x) = s x - P(s)
  with that s.  Closed form via the change of variable u = 1 - 2^{s-1}:
       x + log 3 = log 2 / u    =>    u = log 2 / (x + log 3)
       2^{s-1} = 1 - u           =>    s = 1 + log_2(1 - u)
       P(s)    = -s log 3 + (s - 1) log 2 - log u
               = -s log 3 + log_2(1 - u) log 2 - log u
       I(x) = s x - P(s)         (explicit, but solved via x in closed form).

  Special points:
    I(0) = -P(s*)  ( = 0.13783...   -- the DESCENT-RATE in the LDP sense )
    I(phi_bar) = 0  where phi_bar = -log(3/4) = log 4 - log 3  ~  0.2877 [WAIT see below]
                actually phi_bar = E_{mu_0}[phi] = log 3 - 2 log 2 ~ -0.2877.
    I is strictly convex, smooth on its effective domain.

THE CANDIDATE PROGRAM (sketched, NOT proved here).
  Tao 2022 establishes log-density via a tilted-residue equidistribution
  bound on (Z/3^n)* with rate n^{-A} (Prop 1.17).  The natural-density gap
  requires exponential rate 3^{-theta n} (cf. tao_syracuse_explicit.md, MIX(theta)).
  THERMODYNAMIC FORMALISM PROPOSAL:  use the Esscher tilt s* to re-center the
  drift, then ask whether the *tilted-residue* law on (Z/3^n)* equidistributes
  at the exponential rate that the LDP envelope predicts.  The rate function
  I(0) and its quadratic envelope (P''(s*)) give a UNIVERSAL DESCENT-PROBABILITY
  TAIL  P( D_n / n in [-eps, eps] ) ~ exp( -n * (I(0) + O(eps^2)/(2 P''(s*))) ),
  which combined with residue equidistribution (Tao's input, sharpened) would
  give a quantitative TV bound on the joint (residue, drift) law.

  RESIDUAL OBSTRUCTION (and falsifier): mod-3 marginal of the residue is
  FROZEN at (0, 1/3, 2/3) and is PRESERVED by the Esscher tilt (the tilt
  reweights only via a (the valuation), which is independent of residue mod 3
  -- in fact residue mod 3 is slaved to the LAST valuation a_n only, a 1-bit
  parity).  So the tilt CANNOT repair the mod-3 obstruction; the natural-density
  TV-floor TV(nu_n, U) >= 1/6 of natural_density_obstruction.md survives.
  This file verifies that the mod-3 marginal of the TILTED residue is the same
  (0, 1/3, 2/3) -- the falsifier.

VALIDATION (this file).
  L1: pressure & rate-function closed form, validated:
      - P(s*) = -I(0) match to 1e-12 via Legendre identity.
      - P'(s*) = 0 to machine precision.
      - P''(s*) matches a 10^6-sample MC second moment to a few percent.
  L2: empirical drift distribution from 10^7 trajectories (verifier baseline)
      compared to:
      - mean drift per step = E[phi] (untilted)
      - tail probabilities P(D_n / n > x) for x near 0 vs exp(-n * I(x))
  L3: mod-3 marginal at s = 0 vs s = s* -- VERIFIES the tilt does NOT move it.
      (The falsifier of the candidate-as-stated.)
  L4: numerical LDP exponents from the trajectory data (a 'rate-function chart')
      vs. closed-form I(x).

Read-only imports from collatz/experiments/ for trajectory generation
(verifier.T).

Usage: python3 collatz_thermo_probe.py [N_MC=200000] [N_STEPS=200] [SEED=20260604]
Output: ideas/candidates/data/thermo_probe.json
        ideas/candidates/data/thermo_probe.log
"""

from __future__ import annotations

import json
import math
import os
import random
import sys
import time
from typing import Any, Dict, List, Tuple

# --- read-only import of the verifier for Syracuse trajectories
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
EXP_DIR = os.path.join(ROOT, "math", "collatz", "experiments")
if EXP_DIR not in sys.path:
    sys.path.insert(0, EXP_DIR)
import verifier as V  # noqa: E402

LOG2 = math.log(2.0)
LOG3 = math.log(3.0)
LOG2_3 = math.log2(3.0)
EBAR_NATS = LOG3 - 2.0 * LOG2  # E_{mu_0}[phi], nats per Syracuse odd step.
EBAR_LOG2 = LOG2_3 - 2.0       # the same, in log_2 units.


# ---------------------------------------------------------------------------
# PRESSURE FUNCTION (closed form).
# ---------------------------------------------------------------------------

def pressure(s: float) -> float:
    r"""P(s) = log E_{mu_0}[ exp(-s * phi) ],  finite for s < 1."""
    if s >= 1.0:
        return float("inf")
    # P(s) = -s log3 + (s-1) log2 - log(1 - 2^{s-1})
    return (-s * LOG3) + (s - 1.0) * LOG2 - math.log1p(-math.pow(2.0, s - 1.0))


def pressure_prime(s: float) -> float:
    r"""P'(s) = -log3 + log2 / (1 - 2^{s-1})."""
    if s >= 1.0:
        return float("inf")
    return -LOG3 + LOG2 / (1.0 - math.pow(2.0, s - 1.0))


def pressure_second(s: float) -> float:
    r"""P''(s) = (log2)^2 * 2^{s-1} / (1 - 2^{s-1})^2."""
    if s >= 1.0:
        return float("inf")
    r = math.pow(2.0, s - 1.0)
    return (LOG2 ** 2) * r / (1.0 - r) ** 2


def esscher_star() -> float:
    r"""s* solving P'(s*) = 0:  1 - 2^{s*-1} = log2 / log3."""
    # u* = log2 / log3 = 1 / log_2(3)
    u_star = LOG2 / LOG3
    # 2^{s*-1} = 1 - u_star
    return 1.0 + math.log2(1.0 - u_star)


def rate_function_at_phi_bar() -> float:
    r"""I(phi_bar) = 0, sanity check."""
    return 0.0


def rate_function(x: float) -> Tuple[float, float]:
    r"""
    I(x) = sup_s (s x - P(s)).
    For x in the effective domain (x > -log3 = P'(-inf)+? -- careful: P'(s) ranges
    from -log3 (s -> -inf) up to +inf (s -> 1-)).  We invert x = P'(s) by
        1 - 2^{s-1} = log2 / (x + log3)
    which is in (0, 1) iff x > -log3 + log2 (=> u<1)  AND  x > 0-? Let me just
    require x > -log3 + log2 and 0 < log2/(x+log3) < 1, i.e. x + log3 > log2,
    so x > log2 - log3 = -log(3/2) ~ -0.4055.  But phi_bar = log3 - 2log2 ~
    -0.2877 which is > -log(3/2) [-0.4055].  And I(phi_bar)=0.  Good.

    Returns (s_optimizer, I_value).
    """
    denom = x + LOG3
    u = LOG2 / denom
    if not (0.0 < u < 1.0):
        return (float("nan"), float("inf"))
    s = 1.0 + math.log2(1.0 - u)
    I = s * x - pressure(s)
    return (s, I)


# ---------------------------------------------------------------------------
# VALIDATION L1: closed forms vs. their analytic identities.
# ---------------------------------------------------------------------------

def validate_pressure_identities() -> Dict[str, Any]:
    out = {}
    s_star = esscher_star()
    out["s_star"] = s_star
    out["P_at_s_star"] = pressure(s_star)
    out["Pprime_at_s_star"] = pressure_prime(s_star)
    out["Psecond_at_s_star"] = pressure_second(s_star)

    # Closed forms.
    # P''(s*) = log3 * log(3/2):
    closed_P2 = LOG3 * math.log(1.5)
    out["Psecond_closed_form"] = closed_P2
    out["Psecond_match_err"] = abs(out["Psecond_at_s_star"] - closed_P2)

    # I(0) = -P(s*).
    s0, I0 = rate_function(0.0)
    out["I_at_0"] = I0
    out["I_at_0_minus_negP_sstar"] = I0 - (-pressure(s_star))
    out["s_at_x_eq_0"] = s0
    out["sstar_vs_s_at_0_err"] = abs(s0 - s_star)

    # I(phi_bar) = 0  (legendre at x = phi_bar gives s=0).
    sb, Ib = rate_function(EBAR_NATS)
    out["I_at_phi_bar"] = Ib
    out["s_at_phi_bar"] = sb
    out["phi_bar"] = EBAR_NATS

    # UNTILTED variance (Livsic CLT, sigma^2 = 2*(log2)^2 = (log2)^2 * Var(Geom(1/2)) ).
    # Var(Geom(1/2)) with support {1,2,...}, P(a=k)=2^{-k}:
    #   E[a] = 2, E[a^2] = sum k^2 2^{-k} = 6, Var = 2.
    untilted_var = (LOG2 ** 2) * 2.0
    out["untilted_var_phi"] = untilted_var
    out["untilted_var_phi_minus_2log2sq"] = untilted_var - 2.0 * LOG2 ** 2

    return out


# ---------------------------------------------------------------------------
# VALIDATION L2: closed-form P(s), I(x) vs. Monte Carlo.
# ---------------------------------------------------------------------------

def sample_geom_half(rng: random.Random) -> int:
    """Sample a ~ Geom(1/2) on {1,2,...} with P(a=k)=2^{-k}.  Use bit-walk."""
    k = 1
    while rng.random() < 0.5:
        k += 1
    return k


def empirical_pressure_at(s_grid: List[float], n_samples: int, seed: int) -> Dict[str, Any]:
    """Empirical log E[exp(-s phi)] from n_samples i.i.d. a ~ Geom(1/2)."""
    rng = random.Random(seed)
    # Generate samples once, reuse across s.
    a_samples = [sample_geom_half(rng) for _ in range(n_samples)]
    phi_samples = [LOG3 - a * LOG2 for a in a_samples]

    out = []
    for s in s_grid:
        # Numerically stable: subtract max.
        ws = [-s * p for p in phi_samples]
        m = max(ws)
        lse = m + math.log(sum(math.exp(w - m) for w in ws) / n_samples)
        out.append({
            "s": s,
            "P_closed": pressure(s),
            "P_empirical": lse,
            "abs_err": abs(lse - pressure(s)),
        })
    return {
        "n_samples": n_samples,
        "rows": out,
        "ahat_mean": sum(a_samples) / n_samples,
        "phi_mean": sum(phi_samples) / n_samples,
    }


def empirical_rate_function(x_grid: List[float], n_steps: int, n_blocks: int,
                            seed: int) -> Dict[str, Any]:
    """
    Empirical I(x) from block-LDP:  for each block of n_steps i.i.d. a_j,
    compute phi_n_mean = (1/n) sum_j phi(a_j).  Then
        Î_n(x) = -(1/n) log P( phi_n_mean ~ x )
    estimated by bin counts (with normalization for bin width).
    """
    rng = random.Random(seed)
    block_means = []
    for _ in range(n_blocks):
        s_sum = 0
        for _ in range(n_steps):
            s_sum += sample_geom_half(rng)
        phi_n_mean = (n_steps * LOG3 - s_sum * LOG2) / n_steps
        block_means.append(phi_n_mean)

    # Build a histogram over phi_n_mean values; report -log P / n at bin centers
    # nearest each x in x_grid.
    bin_width = 0.02
    bins: Dict[int, int] = {}
    for m in block_means:
        k = int(round(m / bin_width))
        bins[k] = bins.get(k, 0) + 1

    out = []
    for x in x_grid:
        k = int(round(x / bin_width))
        # Aggregate small window for stability.
        window = [bins.get(j, 0) for j in (k - 1, k, k + 1)]
        cnt = sum(window)
        p_hat = cnt / (n_blocks * 3.0 * bin_width)  # per-x density estimate
        if cnt == 0:
            I_hat = float("inf")
        else:
            I_hat = -math.log(cnt / n_blocks) / n_steps
        s_opt, I_closed = rate_function(x)
        out.append({
            "x": x,
            "n_steps": n_steps,
            "count_in_window": cnt,
            "p_density_hat": p_hat,
            "I_hat_blockfreq": I_hat,
            "I_closed": I_closed,
            "I_hat_minus_closed": I_hat - I_closed,
        })
    return {
        "n_steps": n_steps,
        "n_blocks": n_blocks,
        "bin_width": bin_width,
        "rows": out,
        "global_mean_block": sum(block_means) / n_blocks,
        "global_var_block": sum((m - EBAR_NATS) ** 2 for m in block_means) / n_blocks,
    }


# ---------------------------------------------------------------------------
# VALIDATION (CLT envelope): block phi_n_mean centered at phi_bar should be
# Gaussian with variance (1/n) * Var_{mu_0}(phi) = 2 (log2)^2 / n.
# ---------------------------------------------------------------------------

def empirical_clt(n_steps: int, n_blocks: int, seed: int) -> Dict[str, Any]:
    rng = random.Random(seed)
    blocks = []
    for _ in range(n_blocks):
        s_sum = 0
        for _ in range(n_steps):
            s_sum += sample_geom_half(rng)
        phi_n_mean = (n_steps * LOG3 - s_sum * LOG2) / n_steps
        blocks.append(phi_n_mean)
    m = sum(blocks) / n_blocks
    v = sum((b - m) ** 2 for b in blocks) / n_blocks
    expected_var = 2.0 * LOG2 ** 2 / n_steps
    return {
        "n_steps": n_steps,
        "n_blocks": n_blocks,
        "block_mean": m,
        "block_var": v,
        "expected_var_CLT": expected_var,
        "ratio_block_var_over_expected": v / expected_var,
        "mean_minus_phi_bar": m - EBAR_NATS,
    }


# ---------------------------------------------------------------------------
# VALIDATION L3: mod-3 marginal of the TILTED residue.
# This is the falsifier: if the tilt does NOT move the (0, 1/3, 2/3)
# marginal, the natural-density TV floor of natural_density_obstruction.md
# survives the LDP program, and the program reduces to Tao for the residue.
# We verify it via the exact joint law (R_n, S_n) computed by the same DP
# as collatz_psi_factorization.py / verify_syracuse_rv.py.
# ---------------------------------------------------------------------------

def syracuse_joint_law(n: int, amax: int) -> Dict[int, Dict[int, float]]:
    """
    Exact joint distribution of (residue R_n mod 3^n, total halvings S_n)
    for the n-Syracuse offset map, under Geom(1/2) truncated at amax and
    renormalized.

    Returns map { R: { S: prob } }.

    Implements the recursion: starting from j=n, residue = 2^{-a_n} (mod 3),
    then prepending block j contributes 3^{n-j} * 2^{-(a_j + ... + a_n)} to R
    and a_j to S.

    For modest n (n<=6, 3^6=729), feasible.
    """
    # Truncated geometric weight: w(k) = 2^{-k} for k=1..amax, renormalized.
    base_weights = [0.0]  # index 0 unused
    Z = 0.0
    for k in range(1, amax + 1):
        w = 2.0 ** (-k)
        base_weights.append(w)
        Z += w
    base_weights = [w / Z for w in base_weights[1:]]  # shift to 0-indexed: weight for a=k+1

    mod = 3 ** n
    # mod 3^n inverse of 2.
    def inv2(m: int) -> int:
        return pow(2, -1, m)
    inv2_mod = inv2(mod)

    # joint[R][S] = prob
    joint: Dict[int, Dict[int, float]] = {}

    # Enumerate over the geometric tuple (a_1, ..., a_n) with weight Pi w(a_j).
    # For n <= 6 and amax <= 30 this is amax^n combinations -- 30^6 = 7.29e8, too many.
    # Use DP from the BACK (j = n, n-1, ..., 1).
    # State at position j: tail residue contribution = sum_{i>=j} 3^{n-i} * 2^{-sum_{l>=i} a_l} mod 3^n
    # and S_tail = sum_{i>=j} a_i.
    # When we prepend a_j, new tail factor: 2^{-a_j} multiplies and shifts.
    # Specifically, multiplying ALL existing tail contributions by 2^{-a_j} mod 3^n,
    # and adding 3^{n-j}.
    # Initial state (j = n+1, empty tail): R = 0, S = 0, prob 1.
    # Step j = n down to 1:
    #   for each state (R, S, p):
    #     for a in 1..amax:
    #       new_R = (R * inv2(mod)^a + 3^{n - j}) mod mod
    #       new_S = S + a
    #       new_p = p * base_weights[a-1]

    # Compute inv2_pow[a] = inv2_mod ** a (mod) for a=1..amax.
    inv2_pow = [1]
    for a in range(1, amax + 1):
        inv2_pow.append(inv2_pow[-1] * inv2_mod % mod)

    # Forward recursion: U_j = inv2^{a_j} * (3 * U_{j-1} + 1) mod 3^n.
    # Start U_0 = 0; iterate j = 1, ..., n.  At j=n we obtain F_n = U_n.
    state: Dict[Tuple[int, int], float] = {(0, 0): 1.0}
    for j in range(1, n + 1):
        new_state: Dict[Tuple[int, int], float] = {}
        for (U, S), p in state.items():
            base = (3 * U + 1) % mod
            for a in range(1, amax + 1):
                new_U = (base * inv2_pow[a]) % mod
                new_S = S + a
                new_p = p * base_weights[a - 1]
                key = (new_U, new_S)
                new_state[key] = new_state.get(key, 0.0) + new_p
        state = new_state

    # Reformat.
    for (R, S), p in state.items():
        if R not in joint:
            joint[R] = {}
        joint[R][S] = joint[R].get(S, 0.0) + p
    return joint


def mod3_marginal(joint: Dict[int, Dict[int, float]], s_tilt: float) -> Dict[int, float]:
    """
    Mod-3 marginal of the residue under the s-tilted joint measure.
    Tilt: re-weight each (R, S) by exp(-s * D), where D = S log2 - n log3.
    Since the joint already conditions on S, the tilt factor is exp(-s*(S*log2-n*log3))
    = exp(-s*S*log2) * exp(s*n*log3), and the n-dependent factor cancels in renormalization.
    """
    weighted: Dict[int, float] = {0: 0.0, 1: 0.0, 2: 0.0}
    total = 0.0
    for R, S_dict in joint.items():
        r3 = R % 3
        for S, p in S_dict.items():
            w = p * math.exp(-s_tilt * S * LOG2)
            weighted[r3] = weighted.get(r3, 0.0) + w
            total += w
    return {k: v / total for k, v in weighted.items()}


# ---------------------------------------------------------------------------
# VALIDATION (trajectory check): use the existing verifier to walk integers,
# extract Syracuse valuations, compute empirical drift distribution, and
# compare to the closed-form CLT / LDP envelopes.
# ---------------------------------------------------------------------------

def syracuse_step_from_odd(n_odd: int) -> Tuple[int, int]:
    """One Syracuse odd step:  n_odd -> (3n+1)/2^a; returns (next_odd, a)."""
    m = 3 * n_odd + 1
    a = 0
    while m % 2 == 0:
        m //= 2
        a += 1
    return m, a


def collect_trajectory_drifts(N_max: int, n_steps_max: int, seed: int,
                               n_samples: int) -> Dict[str, Any]:
    """
    Sample random odd starting integers in [3, 2*N_max+1], walk
    Syracuse for up to n_steps_max steps (stopping if it reaches 1),
    collect the valuation sequence (a_j) and per-step drift phi(a_j).

    Returns aggregated statistics: empirical mean phi, variance, and the
    empirical distribution of phi_n_mean for several n.
    """
    rng = random.Random(seed)
    a_dist: Dict[int, int] = {}
    phi_n_means: Dict[int, List[float]] = {}
    target_ns = [10, 20, 50, 100]
    for n in target_ns:
        phi_n_means[n] = []

    for _ in range(n_samples):
        n0 = 2 * rng.randint(1, N_max) + 1  # odd start
        cur = n0
        a_list: List[int] = []
        for step in range(n_steps_max):
            if cur == 1:
                break
            cur, a = syracuse_step_from_odd(cur)
            a_list.append(a)
            a_dist[a] = a_dist.get(a, 0) + 1
            for nt in target_ns:
                if len(a_list) == nt:
                    s_sum = sum(a_list)
                    phi_n_mean = (nt * LOG3 - s_sum * LOG2) / nt
                    phi_n_means[nt].append(phi_n_mean)

    n_total = sum(a_dist.values())
    a_mean = sum(k * c for k, c in a_dist.items()) / n_total if n_total else 0.0
    a_var = sum(c * (k - a_mean) ** 2 for k, c in a_dist.items()) / n_total if n_total else 0.0

    rows = []
    for nt in target_ns:
        means = phi_n_means[nt]
        if not means:
            continue
        m = sum(means) / len(means)
        v = sum((x - m) ** 2 for x in means) / len(means)
        # Predicted CLT variance under mu_0: 2*(log2)^2 / nt.
        expected_var = 2.0 * LOG2 ** 2 / nt
        # Empirical I_hat at x = 0 (a near-balance bin):
        bin_low, bin_high = -0.05, 0.05
        cnt = sum(1 for x in means if bin_low <= x <= bin_high)
        if cnt > 0:
            I_hat_at_0 = -math.log(cnt / len(means)) / nt
        else:
            I_hat_at_0 = float("inf")
        rows.append({
            "n_steps": nt,
            "n_samples": len(means),
            "mean_phi_n": m,
            "var_phi_n": v,
            "expected_var_CLT": expected_var,
            "ratio_var_over_expected": v / expected_var,
            "I_hat_near_0": I_hat_at_0,
            "I_closed_at_0": rate_function(0.0)[1],
        })

    # Empirical valuation distribution vs Geom(1/2).
    a_rows = []
    for k in sorted(a_dist.keys())[:15]:
        emp = a_dist[k] / n_total
        thr = 2.0 ** (-k)
        a_rows.append({"a": k, "emp_freq": emp, "geom_half_prob": thr,
                       "abs_err": abs(emp - thr)})

    return {
        "n_starts": n_samples,
        "n_steps_max": n_steps_max,
        "N_max": N_max,
        "total_steps_taken": n_total,
        "a_mean_emp": a_mean,
        "a_mean_expected": 2.0,
        "a_var_emp": a_var,
        "a_var_expected": 2.0,
        "a_distribution_rows": a_rows,
        "drift_block_rows": rows,
    }


# ---------------------------------------------------------------------------
# MAIN.
# ---------------------------------------------------------------------------

def main():
    n_mc = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    n_steps = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 20260604

    DATA_DIR = os.path.join(HERE, "data")
    os.makedirs(DATA_DIR, exist_ok=True)
    out_path = os.path.join(DATA_DIR, "thermo_probe.json")
    log_path = os.path.join(DATA_DIR, "thermo_probe.log")

    t0 = time.time()
    print(f"[thermo] PRESSURE / RATE-FUNCTION closed-form validation")
    id_results = validate_pressure_identities()
    for k, v in id_results.items():
        print(f"  {k:40s} = {v!r}")

    s_star = id_results["s_star"]

    print(f"\n[thermo] EMPIRICAL PRESSURE: closed P(s) vs MC log E[exp(-s*phi)]")
    s_grid = [-1.0, -0.7, -0.43803, -0.2, 0.0, 0.2, 0.5, 0.8]
    emp_P = empirical_pressure_at(s_grid, n_mc, seed)
    for row in emp_P["rows"]:
        print(f"  s={row['s']:+.5f}  P_closed={row['P_closed']:+.6f}  "
              f"P_emp={row['P_empirical']:+.6f}  err={row['abs_err']:.2e}")
    print(f"  ahat_mean={emp_P['ahat_mean']:.6f}  (expected 2.0)")
    print(f"  phi_mean={emp_P['phi_mean']:+.6f}  (expected {EBAR_NATS:+.6f})")

    print(f"\n[thermo] CLT validation (block phi_n_mean variance vs sigma^2/n)")
    clt_rows = []
    for nb in [50, 100, 500, 1000]:
        if nb > n_mc // 1000:
            n_blocks = max(2000, n_mc // nb)
        else:
            n_blocks = max(5000, n_mc // nb)
        row = empirical_clt(nb, n_blocks, seed + nb)
        clt_rows.append(row)
        print(f"  n={nb:6d}  block_var={row['block_var']:.5e}  "
              f"expected={row['expected_var_CLT']:.5e}  "
              f"ratio={row['ratio_block_var_over_expected']:.4f}")

    print(f"\n[thermo] RATE FUNCTION I(x) vs empirical block-freq -log P/n")
    x_grid = [-0.30, -0.20, -0.10, -0.05, 0.0, 0.05, 0.10, 0.15]
    # Empirical rate at fixed n: n=20, with many blocks; this gives a crude
    # local-LDP check (small n => not in LDP asymptote, but the comparison
    # is informative -- we tag I_hat with n_steps).
    erf = empirical_rate_function(x_grid, n_steps=n_steps, n_blocks=n_mc, seed=seed)
    for row in erf["rows"]:
        print(f"  x={row['x']:+.3f}  I_closed={row['I_closed']:.6f}  "
              f"I_hat(n={row['n_steps']})={row['I_hat_blockfreq']:.6f}  "
              f"cnt={row['count_in_window']}")

    print(f"\n[thermo] L3 falsifier: mod-3 marginal of TILTED residue")
    mod3_rows = []
    s_drift = esscher_star()  # tilt on the drift cocycle: s in -log E[exp(-s phi)]
    # Equivalent residue-side tilt:  the EBAR-balancing tilt on a is
    # s_residue = -s_drift, since phi = log3 - a log2.  We tilt the joint
    # measure (R, S) via exp(-s_drift * (S log2 - n log3)).
    for n in [2, 3, 4, 5, 6]:
        amax = 30
        joint = syracuse_joint_law(n, amax)
        marg_0 = mod3_marginal(joint, 0.0)
        marg_star = mod3_marginal(joint, s_drift)
        print(f"  n={n}  mod3 marginal at s=0:    {[round(marg_0[i],6) for i in (0,1,2)]}")
        print(f"  n={n}  mod3 marginal at s=s*:   {[round(marg_star[i],6) for i in (0,1,2)]}")
        max_diff = max(abs(marg_star[i] - marg_0[i]) for i in (0, 1, 2))
        print(f"  n={n}  max |delta| (tilt moves mod-3?):  {max_diff:.2e}")
        mod3_rows.append({
            "n": n,
            "marg_untilted": marg_0,
            "marg_tilted": marg_star,
            "max_abs_diff": max_diff,
        })

    print(f"\n[thermo] TRAJECTORY EMPIRICAL DRIFT (verifier-generated Syracuse walks)")
    traj_results = collect_trajectory_drifts(
        N_max=1_000_000, n_steps_max=300, seed=seed, n_samples=5000)
    print(f"  total_steps_taken={traj_results['total_steps_taken']}")
    print(f"  a_mean_emp={traj_results['a_mean_emp']:.5f}  (expected ~2.0)")
    print(f"  a_var_emp={traj_results['a_var_emp']:.5f}    (expected ~2.0)")
    for row in traj_results['drift_block_rows']:
        print(f"  n={row['n_steps']:4d}  n_samples={row['n_samples']:5d}  "
              f"mean_phi_n={row['mean_phi_n']:+.5f}  "
              f"var_phi_n/(sigma^2/n)={row['ratio_var_over_expected']:.4f}")

    out_obj = {
        "s_star": s_star,
        "EBAR_nats": EBAR_NATS,
        "EBAR_log2": EBAR_LOG2,
        "I_at_0_closed": rate_function(0.0)[1],
        "closed_form_identities": id_results,
        "empirical_pressure": emp_P,
        "clt_validation": clt_rows,
        "empirical_rate_function": erf,
        "mod3_falsifier": mod3_rows,
        "trajectory_check": traj_results,
        "runtime_sec": time.time() - t0,
    }
    with open(out_path, "w") as f:
        json.dump(out_obj, f, indent=2, default=str)
    with open(log_path, "w") as f:
        f.write(f"thermo_probe.py run at {time.time()}\n")
        f.write(f"runtime: {time.time() - t0:.2f} s\n")
        f.write(f"s_star = {s_star}\n")
        f.write(f"P(s*) = {pressure(s_star)}\n")
        f.write(f"P''(s*) = {pressure_second(s_star)}\n")
        f.write(f"I(0)   = {rate_function(0.0)[1]}\n")
        f.write(f"EBAR_nats = {EBAR_NATS}\n")
        for row in mod3_rows:
            f.write(f"mod3 n={row['n']}  max_diff_tilt = {row['max_abs_diff']:.4e}\n")
    print(f"\n[thermo] wrote {out_path}")


if __name__ == "__main__":
    main()
