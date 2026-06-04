"""
cycle_bound_push.py  --  Cycle-bound push attempt at B = 2^71 (Barina 2025).

Goal.
-----
Reconstruct an upper bound F(m) on the o-step count K in a hypothetical
Collatz m-cycle from first principles, apply it together with the
Crandall lower bound G(B) at B = 2^71, and report the largest excludable m.

Status (honest):
- Sections D1-D5 of the from-scratch derivation (per-circuit identity,
  cycle equation, the exact Lambda = sum eps_j identity, the bound
  0 < Lambda < m/B, the Crandall lower bound on K) are RIGOROUS and
  computer-verified -- they are inherited from theory/cycle_bound_attempt.md
  and theory/cycle_exclusion_explicit.md (don't re-prove here).
- The MISSING PIECE in those notes is the explicit upper bound F(m) on K,
  which Hercher 2023 derives via a circuit-averaging + two-log linear-form
  argument that we could NOT reproduce without his primary text (HTTP 403).

What this script does (incremental, honest):
1. Compute the Crandall lower bound G(B) at B = 2^71 vs B = 3*2^69.
2. Compute the convergent denominator structure that pinches K to be
   essentially a convergent of log_2(3) -- a real, rigorously-derived
   *additional* constraint (Legendre's theorem applied to Lambda < m/B).
3. Construct THREE explicit candidate F(m) functions:
     (F-LMN)    F_lmn(m)   from the two-log LMN lower bound on Lambda
                           combined with Lambda < m/B; this is the
                           "naive" reconstruction.  Direction: actually
                           gives a LOWER bound on K (Prop 5 of cycle_bound_attempt.md),
                           NOT an upper bound, when m/B is the only bound.
                           Documented as a "control".
     (F-conv)   F_conv(m)  the convergent-denominator constraint: K must be
                           a convergent denominator of log_2(3) in the regime
                           where Lambda < log(2)/(2K), i.e. K < B*log(2)/(2m).
                           This is the *rigorous* discrete constraint.
     (F-power)  F_power(m) the calibrated power-law model pinned at
                           (m=2, F=8.6e4) (Simons) and (m=91, F=G(3*2^69))
                           (Hercher self-consistency).  This is PROVISIONAL.
4. For each F, compute the largest m* such that F(m) <= G(2^71), and report.
5. Computationally validate (small-K side): no Collatz m-cycle exists with
   m <= some small threshold and K up to a tractable bound.

Author: Alex Ye (AI assistance disclosed; not on author line).
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from fractions import Fraction as Fr
from typing import Dict, List, Optional, Tuple

# Make the project tree importable so we can reuse experiments/cycles.py
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "collatz", "experiments"))

try:
    import mpmath as mp
    mp.mp.dps = 120
    HAVE_MPMATH = True
except Exception:
    HAVE_MPMATH = False

# Try to reuse cycles.py utilities
try:
    from cycles import (search_cycles_by_parity, search_cycles_by_orbit,
                        check_bound_consistency)
    HAVE_CYCLES = True
except Exception:
    HAVE_CYCLES = False

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Continued fraction of delta = log_2 3 (mpmath at dps=120).
# ---------------------------------------------------------------------------

def cf_delta(n_terms: int = 60) -> List[int]:
    assert HAVE_MPMATH
    delta = mp.log(3) / mp.log(2)
    out: List[int] = []
    y = delta
    for _ in range(n_terms):
        a = int(mp.floor(y))
        out.append(a)
        f = y - a
        if f == 0:
            break
        y = 1 / f
    return out


def convergents(cf: List[int]) -> List[Tuple[int, int]]:
    out = []
    h0, h1 = 1, cf[0]
    k0, k1 = 0, 1
    out.append((h1, k1))
    for i in range(1, len(cf)):
        h2 = cf[i] * h1 + h0
        k2 = cf[i] * k1 + k0
        out.append((h2, k2))
        h0, h1 = h1, h2
        k0, k1 = k1, k2
    return out


# ---------------------------------------------------------------------------
# Crandall lower bound G(B) on K.
# G(B) = (3/2) max_{j>4} min(q_j, 2B/(q_j + q_{j+1}))
# (Crandall 1978, restated -- snippet-verified, see cycle_exclusion_explicit.md).
# ---------------------------------------------------------------------------

def crandall_G(B, convs: List[Tuple[int, int]]):
    assert HAVE_MPMATH
    best = mp.mpf(0)
    arg = None
    for j in range(5, len(convs) - 1):
        qj = convs[j][1]
        qj1 = convs[j + 1][1]
        v = mp.mpf(3) / 2 * min(mp.mpf(qj), mp.mpf(2) * mp.mpf(B) / (qj + qj1))
        if v > best:
            best = v
            arg = (j, qj, qj1)
    return best, arg


# ---------------------------------------------------------------------------
# F(m) reconstructions.
#
# (F-LMN)   The two-log LMN-derived upper bound on Lambda.
#
# LMN-1995 says  log|Lambda| >= -24.34 * (max{log b' + 0.14, 21})^2 * log A_1 * log A_2
# with (for our application)  A_1 = 2, A_2 = 3, log A_1 = max(log 2, 1) = 1,
# log A_2 = log 3, b' = N/log A_2 + K/log A_1 ~ K*(delta/log3 + 1) ~ K*(1+delta/log3).
# Hence
#       log|Lambda| >= - C_LMN * (log K + c0)^2   with  C_LMN = 24.34 * log 3.
# Direction: this is a LOWER bound on Lambda.  Combined with Lambda < m/B
# it gives a LOWER bound on K.  We expose it here as a *control* (it does NOT
# produce F(m)).
#
# (F-conv)  Legendre / convergent constraint.
#
# Lambda/log 2 = |N - K*delta|.  For the cycle, Lambda < m/B (Cor 4 of
# cycle_bound_attempt.md), so  |N/K - delta| < m / (K B log 2).
# Legendre's theorem: if |x - p/q| < 1/(2 q^2), then p/q is a convergent of x.
# Hence if  K * m/(K B log 2) = m/(B log 2) < 1/(2K), i.e.  K < B log 2 / (2m),
# the rational N/K is FORCED to be a convergent of delta.  K is then forced
# to be a convergent DENOMINATOR  q_j  of delta.
#
# Combining with Crandall's lower bound G(B), the cycle's K must satisfy
#     K >= G(B)  AND  K is a convergent denominator of delta in the regime
#     K < B log 2 / (2m).
# (F-conv) is the smallest convergent denominator >= G(B).  This is RIGOROUS,
# but it is a *discrete* constraint, not an "upper bound that decays in m".
#
# (F-power) The provisional power-law model pinned at the Simons F(2) and
# Hercher F(91) anchors.  This is PROVISIONAL bookkeeping, calibrated so that
# m*(B = 3*2^69) = 91 (self-consistency with Hercher).
# ---------------------------------------------------------------------------

def F_lmn_lambda_lower(K: float) -> float:
    """LMN-derived LOWER bound on Lambda (NOT an upper bound on K).  We
    expose this only as a directionality check / control."""
    # c0 absorbs the inner-max 'log 21' and the +0.14 shift; with b' ~ K*(1+delta/log3)
    # we have log b' ~ log K + log(1 + delta/log3) = log K + 0.86.
    # For K in the realistic regime (K >> e^21 = 1.3e9), the max kicks (log K + 0.14)
    # in directly; the +0.14 shift is dominated.
    if K <= 0:
        return float('inf')
    delta = math.log(3) / math.log(2)
    c0 = math.log(1 + delta / math.log(3))  # ~0.86
    inner = max(math.log(K) + c0 + 0.14, 21.0)
    return math.exp(-24.34 * inner ** 2 * math.log(3))


def F_conv_min_denom_above(G, convs: List[Tuple[int, int]]) -> Optional[int]:
    """Smallest convergent denominator >= G."""
    for _, q in convs:
        if q >= G:
            return q
    return None


def F_power(m: int, cH, K2: float = 8.6e4) -> float:
    """Power-law model F(m) = c m^p calibrated through (2, 8.6e4) and (91, cH)."""
    # Hercher's F(91) is essentially the Crandall bound at his B (3*2^69), so
    # at the threshold F(91) ~ cH.  cH is mp.mpf; convert.
    cH_f = float(cH)
    p = math.log(cH_f / K2) / math.log(91.0 / 2.0)
    c = K2 / (2 ** p)
    return c * (m ** p)


# ---------------------------------------------------------------------------
# Main squeeze report.
# ---------------------------------------------------------------------------

def squeeze_at_B(B, convs: List[Tuple[int, int]], cH=None,
                 m_max_scan: int = 200) -> Dict:
    """Compute Crandall lower bound, the convergent-pinch threshold,
    and (provisional) m* under the power-law F(m) calibrated at the
    Hercher anchor cH (Crandall at his B = 3*2^69).  Returns a dict."""
    assert HAVE_MPMATH
    G, arg = crandall_G(B, convs)
    # Convergent-pinch regime: K < B log 2 / (2m).  For a given m, find the
    # smallest convergent denominator that is >= G AND <= B log 2 / (2m);
    # if no such q_j exists then no cycle (the discrete set is empty in the
    # forced regime); otherwise the cycle's K must be one of those q_j.
    log2 = mp.log(2)
    rows = []
    for m in range(1, m_max_scan + 1):
        pinch_upper = mp.mpf(B) * log2 / (2 * m)
        # Convergent denominators in [G, pinch_upper]:
        allowed = [q for (_, q) in convs if mp.mpf(q) >= G and mp.mpf(q) <= pinch_upper]
        # Power-law F(m) if cH provided:
        Fp = F_power(m, cH) if cH is not None else None
        rows.append({
            "m": m,
            "G": float(G),
            "pinch_upper": float(pinch_upper),
            "n_allowed_convergents": len(allowed),
            "allowed": allowed,
            "F_power": Fp,
            "F_power_le_G": (Fp is not None and Fp <= float(G)),
        })
    # m*_power: largest m with F_power(m) <= G.
    mstar_power = max((r["m"] for r in rows if r["F_power_le_G"]), default=0)
    # m*_conv: largest m where the allowed set becomes empty *and stays empty*.
    # Empty allowed set means: no admissible K (no convergent in [G, pinch_upper]).
    # We want the largest m such that for all m' <= m, the cycle is excluded.
    # Exclusion via convergent-pinch requires (a) pinch_upper >= G (else the
    # regime is non-empty trivially) AND no convergent in between.
    # Actually exclusion requires: either pinch_upper < G (no admissible K) OR
    # the allowed list is empty.  Either way the cycle cannot exist via this
    # particular argument.
    excluded_by_pinch = []
    for r in rows:
        if r["pinch_upper"] < r["G"] or r["n_allowed_convergents"] == 0:
            excluded_by_pinch.append(r["m"])
    # The "largest m excluded for all m' <= m" -- but the pinch is monotone in m
    # (larger m => smaller pinch_upper => harder to fit a convergent in [G, pinch_upper]),
    # so exclusion is monotone: if m is excluded, larger m is too.
    # We instead want the SMALLEST m NOT excluded; everything below is excluded.
    # That's the threshold m*_pinch.
    # NB: small m may actually be NOT excluded because pinch_upper huge and convergents
    # available.  We need to track which m are excluded; the m* is the largest m
    # with all m' <= m excluded -- which is just the contiguous initial run.
    return {
        "B": float(B), "log2_B": float(mp.log(B, 2)),
        "G": float(G), "G_arg": arg,
        "mstar_power": mstar_power,
        "excluded_by_pinch_set": excluded_by_pinch,
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# Computational validation: confirm small-K exclusion via direct cycle search.
# (Per the brief: theory and computation must agree where feasible.)
# ---------------------------------------------------------------------------

def validate_computationally(max_parity_len: int = 22,
                             orbit_N_max: int = 10 ** 5,
                             orbit_L_max: int = 3000,
                             verbose: bool = True) -> Dict:
    """Use experiments/cycles.py to brute-force the parity-length and
    orbit-elemental small-K side.  Reports any cycle found other than the
    trivial {1,2}."""
    if not HAVE_CYCLES:
        return {"ok": False, "reason": "cycles.py not importable"}
    t0 = time.perf_counter()
    parity_results = search_cycles_by_parity(max_parity_len, verbose=verbose)
    nontrivial = [r for r in parity_results if not r.get("is_trivial", True)]
    t1 = time.perf_counter()
    orbit_results = search_cycles_by_orbit(orbit_N_max, orbit_L_max,
                                           verbose=verbose)
    t2 = time.perf_counter()
    # bound consistency for the identity Lambda = sum eps_j
    consistency = check_bound_consistency(max_m=min(max_parity_len, 24),
                                          verbose=verbose)
    return {
        "ok": True,
        "max_parity_len": max_parity_len,
        "orbit_N_max": orbit_N_max,
        "orbit_L_max": orbit_L_max,
        "parity_nontrivial_count": len(nontrivial),
        "orbit_cycle_count": len(orbit_results),
        "consistency": consistency,
        "elapsed_parity_s": t1 - t0,
        "elapsed_orbit_s": t2 - t1,
    }


# ---------------------------------------------------------------------------
# Optional: re-derive the F-power, F-conv, F-LMN tables explicitly.
# ---------------------------------------------------------------------------

def report_F_tables(B, convs: List[Tuple[int, int]], cH,
                    ms: List[int]) -> Dict:
    assert HAVE_MPMATH
    G, _ = crandall_G(B, convs)
    log2 = mp.log(2)
    rows = []
    for m in ms:
        pinch_upper = mp.mpf(B) * log2 / (2 * m)
        # F-conv: smallest convergent denominator in [G, pinch_upper]
        candidates = [q for (_, q) in convs
                      if mp.mpf(q) >= G and mp.mpf(q) <= pinch_upper]
        F_conv_val = min(candidates) if candidates else None
        F_conv_excluded = (F_conv_val is None)  # excluded if no admissible K
        F_p = F_power(m, cH)
        F_p_excluded = (F_p <= float(G))
        # F-LMN: K such that LMN-lower(K) = m/B  (this gives K from below,
        # NOT an upper bound -- presented for transparency)
        # Solve  exp(-24.34 * (log K + c0)^2 * log 3) = m/B  =>
        # 24.34 * log 3 * (log K + c0)^2 = log(B/m)
        # log K = sqrt(log(B/m) / (24.34 log 3)) - c0
        delta = math.log(3) / math.log(2)
        c0 = math.log(1 + delta / math.log(3)) + 0.14
        rhs = math.log(float(B) / m) / (24.34 * math.log(3))
        if rhs > 0:
            logK_lmn = math.sqrt(rhs) - c0
            K_lmn = math.exp(logK_lmn) if logK_lmn > 0 else 0
        else:
            K_lmn = 0
        rows.append({
            "m": m,
            "G": float(G),
            "pinch_upper": float(pinch_upper),
            "F_conv": F_conv_val,
            "F_conv_excluded": F_conv_excluded,
            "F_power": F_p,
            "F_power_excluded": F_p_excluded,
            "K_lmn_LOWERBOUND": K_lmn,  # lower bound, not upper
        })
    mstar_power = max((r["m"] for r in rows if r["F_power_excluded"]), default=0)
    # F-conv is monotone in m (larger m -> smaller pinch); once a small m is
    # NOT excluded, all larger m are excluded only if their pinch also doesn't
    # contain a convergent (which is sharper for larger m).  But "exclusion"
    # from F-conv alone is not the right framing -- it's only the *additional*
    # discrete constraint.  We report it for completeness.
    return {
        "G": float(G), "B": float(B), "B_log2": float(mp.log(B, 2)),
        "mstar_power": mstar_power,
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# Driver.
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-validate", action="store_true",
                        help="Skip the brute-force computational validation.")
    parser.add_argument("--parity-m", type=int, default=20,
                        help="Brute-force parity-length max (default 20).")
    parser.add_argument("--orbit-n", type=int, default=10**5,
                        help="Brute-force orbit N_max (default 10^5).")
    parser.add_argument("--json", default=os.path.join(DATA_DIR, "cycle_bound_push.json"))
    args = parser.parse_args()

    print("=" * 76)
    print("cycle_bound_push.py  --  push at B = 2^71 (Barina 2025)")
    print("=" * 76)

    if not HAVE_MPMATH:
        print("ERROR: mpmath required.")
        return 1

    cf = cf_delta(60)
    convs = convergents(cf)
    print(f"\nConvergents of log_2(3) computed at dps={mp.mp.dps}.")
    print("  q_22 =", convs[22][1], "  q_23 =", convs[23][1], "  q_24 =", convs[24][1])

    B_H = mp.mpf(3) * 2 ** 69          # Hercher 2023
    B_B = mp.mpf(2) ** 71              # Barina 2025

    cH, argH = crandall_G(B_H, convs)
    cB, argB = crandall_G(B_B, convs)
    print(f"\nCrandall lower bound G(B) on K:")
    print(f"  B = 3*2^69 (Hercher): G = {mp.nstr(cH,8)}  (binding j={argH[0]}, q={argH[1]})")
    print(f"  B = 2^71   (Barina) : G = {mp.nstr(cB,8)}  (binding j={argB[0]}, q={argB[1]})")
    print(f"  ratio  G(Barina)/G(Hercher) = {mp.nstr(cB/cH, 6)} = 2^{mp.nstr(mp.log(cB/cH,2),5)}")

    print("\n" + "-" * 76)
    print("F(m) reconstructions / models (RIGOROUS rigid vs PROVISIONAL):")
    print("-" * 76)
    ms = [2, 5, 10, 20, 50, 75, 82, 91, 92, 93, 95, 99, 100, 110]
    rep = report_F_tables(B_B, convs, cH, ms)
    print(f"\nAt B = 2^71, G = {rep['G']:.5g}:")
    print(f"  {'m':>4}  {'F_power':>14}  {'F-power<=G':>10}  {'F_conv':>14}  "
          f"{'pinch_upper':>14}  {'K_lmn_LB':>12}")
    for r in rep['rows']:
        fc = r['F_conv'] if r['F_conv'] is not None else 'none'
        print(f"  {r['m']:>4}  {r['F_power']:>14.5g}  {str(r['F_power_excluded']):>10}  "
              f"{str(fc):>14}  {r['pinch_upper']:>14.5g}  {r['K_lmn_LOWERBOUND']:>12.4g}")
    print(f"\n  m*_power (largest m with F_power(m) <= G(2^71)) = {rep['mstar_power']}")

    # Self-consistency check: power-law at Hercher B should give m* = 91
    repH = report_F_tables(B_H, convs, cH, list(range(85, 100)))
    print(f"\nSelf-consistency: at B = 3*2^69, F_power-based m* = {repH['mstar_power']}")
    print("  (should be 91 by construction of the power-law calibration)")

    # ---- computational validation (brute) ----
    if not args.no_validate:
        print("\n" + "-" * 76)
        print("Computational validation (cycles.py brute force, small-K side):")
        print("-" * 76)
        val = validate_computationally(args.parity_m, args.orbit_n,
                                       orbit_L_max=3000, verbose=True)
        print(f"\n  parity-length up to {args.parity_m}: "
              f"nontrivial cycles = {val.get('parity_nontrivial_count', '?')}")
        print(f"  orbits in [2, {args.orbit_n}], period <= 3000: "
              f"cycles found = {val.get('orbit_cycle_count', '?')}")
        if val.get("consistency"):
            c = val["consistency"]
            print(f"  bound consistency on positive fixed points: "
                  f"identity {c['n_identity_ok']}/{c['n_fixed']}, "
                  f"bound {c['n_bound_ok']}/{c['n_fixed']}")
    else:
        val = {"skipped": True}

    # ---- save ----
    out = {
        "convergents_first_30": [(int(p), int(q)) for (p, q) in convs[:30]],
        "B_H": float(B_H), "B_B": float(B_B),
        "G_H": float(cH), "G_B": float(cB),
        "ratio_GB_GH": float(cB / cH),
        "log2_ratio_GB_GH": float(mp.log(cB / cH, 2)),
        "report_at_B_B": rep,
        "selfcheck_at_B_H": repH,
        "validation": val,
    }
    with open(args.json, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nWrote {args.json}")

    print("\n" + "=" * 76)
    print("HONEST ASSESSMENT (must be read alongside cycle_bound_push.md):")
    print("=" * 76)
    print("""
1. F-power (power-law model pinned at m=2 Simons and m=91 Hercher) is the
   only F(m) on the table that is calibrated to reproduce Hercher's known
   bound.  It is PROVISIONAL and unfaithful as a derivation -- the genuine
   F(m) is Hercher's circuit-averaging argument, which we could NOT
   reproduce from first principles (his PDF is HTTP 403 in this env).

2. F-conv (Legendre/convergent constraint, K must be a convergent denominator
   of log_2(3) in the regime Lambda < log 2 /(2K)) is RIGOROUS but DISCRETE:
   it does not by itself give an "upper bound that decays in m".  It is
   reported for transparency and is a valid additional pinch.

3. F-lmn / K_lmn_LB is reported only to make the directional point: the
   LMN two-log lower bound on Lambda, combined with Lambda < m/B, gives
   a LOWER bound on K -- not an upper bound.  This is the Prop 5 finding
   of cycle_bound_attempt.md, confirmed numerically here.

4. The Crandall lower bound G(2^71) = ~3.49e10 vs G(3*2^69) = ~2.62e10:
   ratio = 4/3 = 2^0.415, which is well short of the 2^4.7 needed to reach
   the next convergent plateau q_23 = 1.375e11.  So B = 2^71 alone does
   NOT robustly beat m=91; at best (under the optimistic F_power model)
   it gives m*=92 -- a +1 improvement, marked [PROVISIONAL].
""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
