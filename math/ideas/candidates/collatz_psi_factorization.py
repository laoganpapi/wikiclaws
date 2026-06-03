"""
collatz_psi_factorization.py
============================

THE DECIDING EXPERIMENT (ergodic-E2 / probability-B.4): does the joint
(residue, drift) law of the n-step Syracuse system FACTORIZE at the
descent-balance Esscher tilt?

Object under test
-----------------
For the n-step Syracuse random variable on (Z/3^n)^x,
    R_n  = Syrac(Z/3^n Z)  = sum_{j=1}^n 3^{n-j} 2^{-(a_j+...+a_n)}  (mod 3^n)
    S_n  = a_1 + a_2 + ... + a_n              (total valuation sum)
    D_n  = S_n * log 2 - n * log 3            (log-drift; descent variable)
with a_1,...,a_n i.i.d. Geom(2) (or its Esscher-tilted version).  We build the
EXACT joint law p(R, S) by dynamic programming, then form the joint
characteristic / generating function

    Psi_n(xi, t) = E[ e(xi R_n / 3^n) * e^{-t D_n} ],   e(x) = exp(2 pi i x),

and test the multiplicative FACTORIZATION DEFECT off the frozen mod-3 coset:

    Delta_n = max_{xi : 3 nmid xi} | Psi_n(xi, t*) / (Psi_n(xi,0) Psi_n(0,t*)) - 1 |

at the descent-balance tilt t* = s* (where E_{t*}[D_n] = 0).

Disjointness (Delta_n -> 0 with a power saving in n)  =>  a genuine route to
quotient the frozen mod-3 factor and run a descent argument on the complement,
escaping the TV >= 1/6 barrier.  Bounded-below Delta_n => residue and drift are
COUPLED => the joint-law route is obstructed (a clean, publishable negative).

We also measure the full-resolution mutual information I(R_n mod 3^k; sgn D_n)
for k=1,2,3 as an independent statistic on the coupling (the reviewer's probe).

Imports the exact tilted-geometric / residue DP machinery from
collatz/experiments/verify_syracuse_rv.py (READ-ONLY).

ABSOLUTE-RULES note: this file lives under ideas/candidates/; it only reads from
collatz/experiments/.  Author: Alex Ye (no AI on author line).
Status: [NOVELTY UNVERIFIED]. Numerics, not proof.
"""
from __future__ import annotations

import cmath
import json
import math
import os
import sys
from typing import Dict, Tuple

# ---- read-only import of the exact Syracuse machinery -----------------------
EXP_DIR = "/home/user/wikiclaws/math/collatz/experiments"
if EXP_DIR not in sys.path:
    sys.path.insert(0, EXP_DIR)
from verify_syracuse_rv import inv_pow2_mod  # noqa: E402

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Esscher / descent-balance tilt
# ---------------------------------------------------------------------------
def s_star() -> float:
    """Descent-balance tilt: E_{s*}[a] = log_2 3, so log-drift mean is 0."""
    target = math.log(3, 2)
    r_star = 1.0 - 1.0 / target
    return -math.log2(r_star) - 1.0


# ---------------------------------------------------------------------------
# EXACT joint law of (R_n mod 3^n, S_n = sum a_j), as a function of the tilt s
# ---------------------------------------------------------------------------
def joint_law_RS(n: int, a_max: int = 60, s: float = 0.0
                 ) -> Tuple[Dict[Tuple[int, int], float], float]:
    """
    Exact (truncated) joint law p(R, S) of the Syracuse residue R = Syrac(Z/3^n)
    and the total valuation sum S = a_1+...+a_n, under the s-tilted geometric
    valuation law P_s(a=k) propto 2^{-k(1+s)}, k>=1.

    DP runs j = n down to 1 over the suffix recursion (same skew-convolution as
    verify_syracuse_rv.syracuse_law), but here we keep the FULL valuation sum S
    as part of the returned key (verify_syracuse_rv collapses it).  S accumulates
    exactly across all j, so the final suffix exponent S_1 = a_1+...+a_n IS S_n.

    Returns (law, retained_mass) where law[(R,S)] is the (un-normalized over the
    retained support, then normalized) probability, and retained_mass is the
    geometric tail mass kept per draw (for reporting truncation error).
    """
    modulus = 3 ** n
    if s == 0.0:
        geom = {k: (0.5) ** k for k in range(1, a_max + 1)}
    else:
        ratio = 2.0 ** (-(1.0 + s))
        geom = {k: ratio ** k for k in range(1, a_max + 1)}
    retained = sum(geom.values())

    # State: (R, E) where R = partial residue, E = suffix valuation sum so far.
    # After all n terms, E = S_n exactly (it is the running sum of all a_j).
    dist: Dict[Tuple[int, int], float] = {(0, 0): 1.0}
    for j in range(n, 0, -1):
        new: Dict[Tuple[int, int], float] = {}
        coeff = pow(3, n - j, modulus)
        for (R, E), p in dist.items():
            for k, pk in geom.items():
                S_j = E + k
                term = (coeff * inv_pow2_mod(S_j, modulus)) % modulus
                R2 = (R + term) % modulus
                key = (R2, S_j)
                new[key] = new.get(key, 0.0) + p * pk
        dist = new

    total = sum(dist.values())
    law = {key: p / total for key, p in dist.items()}
    # per-draw retained mass (n independent draws); truncation loss ~ n*(1-retained)
    return law, retained


# ---------------------------------------------------------------------------
# Vectorized: t-weighted residue marginal q_t(R) = sum_S p(R,S) e^{-t D(S)}.
# Then Psi_n(.,t) is the (sign +) DFT of q_t over R, computed by one FFT.
# This makes the full off-coset sweep O(3^n log 3^n) instead of O(3^n * support).
# ---------------------------------------------------------------------------
import numpy as np  # noqa: E402


def q_marginal(law: Dict[Tuple[int, int], float], n: int, t: float) -> "np.ndarray":
    """q_t(R) = sum_S p(R,S) e^{-t D},  D = S log2 - n log3, as a length-3^n array."""
    modulus = 3 ** n
    log2 = math.log(2.0)
    log3 = math.log(3.0)
    q = np.zeros(modulus, dtype=np.float64)
    for (R, S), p in law.items():
        q[R] += p * math.exp(-t * (S * log2 - n * log3))
    return q


def psi_all(q: "np.ndarray") -> "np.ndarray":
    """Return Psi(xi) = sum_R q[R] e(+xi R / 3^n) for all xi, via FFT.
    np.fft.ifft(q)*N = sum_R q[R] exp(+2pi i xi R / N) at index xi."""
    N = q.shape[0]
    return np.fft.ifft(q) * N


def psi(law: Dict[Tuple[int, int], float], n: int, xi: int, t: float) -> complex:
    modulus = 3 ** n
    log2 = math.log(2.0)
    log3 = math.log(3.0)
    ang = 2.0 * math.pi * xi / modulus
    acc = 0j
    for (R, S), p in law.items():
        D = S * log2 - n * log3
        acc += p * cmath.exp(1j * ang * R) * math.exp(-t * D)
    return acc


def drift_mean(law: Dict[Tuple[int, int], float], n: int, t: float) -> float:
    """E_t[D_n] under the t-Esscher reweighting e^{-t D} (normalized)."""
    log2 = math.log(2.0)
    log3 = math.log(3.0)
    Z = 0.0
    num = 0.0
    for (R, S), p in law.items():
        D = S * log2 - n * log3
        w = p * math.exp(-t * D)
        Z += w
        num += w * D
    return num / Z


def tilted_factor_defect(law, n, t_star):
    """
    A BOUNDED, normalization-free disjointness statistic computed INSIDE the
    descent-balance (t*-tilted) joint measure p_{t*}: the off-coset max of the
    residue-character / centered-drift CORRELATION defect

        rho(xi) = | E_{t*}[e(xi R) g] / (E_{t*}[e(xi R)] * E_{t*}[g]) - 1 |,
        g = exp(-(D - E_{t*}[D])),    e(x) = exp(2 pi i x).

    Everything is an expectation under the SAME measure p_{t*}, so rho cannot be
    inflated by the tilt's normalization scale; it is the genuine residue-vs-drift
    coupling seen at the descent-balance point.  If residue _|_ drift, rho -> 0.
    Computed via two FFTs.
    """
    modulus = 3 ** n
    log2 = math.log(2.0)
    log3 = math.log(3.0)
    # tilted residue marginal q1(R) = sum_S p_{t*}(R,S);  and q2(R) = sum_S p_{t*}(R,S) g(S)
    q1 = np.zeros(modulus, dtype=np.float64)
    Zt = 0.0
    for (R, S), p in law.items():
        w = p * math.exp(-t_star * (S * log2 - n * log3))
        q1[R] += w
        Zt += w
    q1 /= Zt
    mean = 0.0
    for (R, S), p in law.items():
        w = p * math.exp(-t_star * (S * log2 - n * log3)) / Zt
        mean += w * (S * log2 - n * log3)
    q2 = np.zeros(modulus, dtype=np.float64)
    Eg = 0.0
    for (R, S), p in law.items():
        w = p * math.exp(-t_star * (S * log2 - n * log3)) / Zt
        g = math.exp(-((S * log2 - n * log3) - mean))
        q2[R] += w * g
        Eg += w * g
    Ec = psi_all(q1)        # E_{t*}[e(xi R)] for all xi
    Ecg = psi_all(q2)       # E_{t*}[e(xi R) g] for all xi
    worst = -1.0
    arg = -1
    for xi in range(1, modulus):
        if xi % 3 == 0:
            continue
        if abs(Ec[xi]) < 1e-13:
            continue
        rho = abs(Ecg[xi] / (Ec[xi] * Eg) - 1.0)
        if rho > worst:
            worst = rho
            arg = xi
    return worst, arg


# ---------------------------------------------------------------------------
# The factorization defect Delta_n  (FFT-vectorized over all xi)
# ---------------------------------------------------------------------------
def factorization_defect(law, n, t_star, by_v3=True):
    """
    Delta_n = max_{xi: 3 nmid xi} | Psi(xi,t*) / (Psi(xi,0) Psi(0,t*)) - 1 |.

    Also returns the argmax xi and the worst defect within each v3(xi) stratum
    (mod-3 / mod-9 / mod-27 coset tower) for localizing where the coupling lives.
    Uses two FFTs: Psi(.,0) = DFT of q_0,  Psi(.,t*) = DFT of q_{t*}.
    """
    modulus = 3 ** n
    q0 = q_marginal(law, n, 0.0)
    qt = q_marginal(law, n, t_star)
    Psi0 = psi_all(q0)        # Psi(xi, 0)   = residue characteristic function
    Psit = psi_all(qt)        # Psi(xi, t*)
    psi0_t = Psit[0]          # Psi(0, t*)
    worst = -1.0
    arg = -1
    defects_by_v3: Dict[int, float] = {}
    for xi in range(1, modulus):
        v3 = 0
        z = xi
        while z % 3 == 0:
            z //= 3
            v3 += 1
        denom = Psi0[xi] * psi0_t
        if abs(denom) < 1e-15:
            continue
        defect = abs(Psit[xi] / denom - 1.0)
        if defect > defects_by_v3.get(v3, -1.0):
            defects_by_v3[v3] = defect
        if v3 == 0 and defect > worst:
            worst = defect
            arg = xi
    return worst, arg, defects_by_v3


# ---------------------------------------------------------------------------
# Mutual information I(R mod 3^k ; sgn D_n)  (independent coupling statistic)
# ---------------------------------------------------------------------------
def mutual_information_res_drift(law, n, k):
    """
    I(R mod 3^k ; sgn D_n) in bits, under the UNTILTED law (the reviewer's
    statistic).  sgn D_n = 1[D_n >= 0].  Resolving the residue to mod 3^k.
    """
    log2 = math.log(2.0)
    log3 = math.log(3.0)
    mod_k = 3 ** k
    # joint p(r mod 3^k, sign)
    joint: Dict[Tuple[int, int], float] = {}
    p_res: Dict[int, float] = {}
    p_sgn: Dict[int, float] = {}
    for (R, S), p in law.items():
        D = S * log2 - n * log3
        sg = 1 if D >= 0 else 0
        r = R % mod_k
        joint[(r, sg)] = joint.get((r, sg), 0.0) + p
        p_res[r] = p_res.get(r, 0.0) + p
        p_sgn[sg] = p_sgn.get(sg, 0.0) + p
    I = 0.0
    for (r, sg), pj in joint.items():
        if pj <= 0:
            continue
        I += pj * math.log2(pj / (p_res[r] * p_sgn[sg]))
    return I


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------
def mod3_marginal(law, n):
    m = {0: 0.0, 1: 0.0, 2: 0.0}
    for (R, S), p in law.items():
        m[R % 3] += p
    return m


def residue_char_fn(law, n, xi):
    """Psi_n(xi,0) = E[e(xi R/3^n)] = the known residue characteristic function."""
    return psi(law, n, xi, 0.0)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def main():
    n_max = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    a_max = int(sys.argv[2]) if len(sys.argv) > 2 else 70
    t_star = s_star()

    print("=" * 74)
    print("Psi_n(xi,t) FACTORIZATION PROBE  (residue _|_ drift disjointness test)")
    print("=" * 74)
    print(f"descent-balance Esscher tilt  t* = s* = {t_star:.6f}")
    print(f"  (E_{{t*}}[a] should equal log_2 3 = {math.log(3,2):.6f})")
    print()

    results = []
    for n in range(2, n_max + 1):
        law, retained = joint_law_RS(n, a_max=a_max, s=0.0)
        trunc = n * (1.0 - retained)

        # --- validation ---
        m3 = mod3_marginal(law, n)
        dmean = drift_mean(law, n, t_star)
        dmean0 = drift_mean(law, n, 0.0)
        # cross-check residue char fn against direct (Psi(xi,0)); pick a sample xi
        sample_xi = 1
        cf = residue_char_fn(law, n, sample_xi)

        # --- the defect (raw multiplicative, off-coset) ---
        delta, arg, by_v3 = factorization_defect(law, n, t_star)
        # --- bounded cross-check: tilted-measure correlation defect ---
        rho, rho_arg = tilted_factor_defect(law, n, t_star)

        # --- mutual information vs resolution ---
        I_by_k = {k: mutual_information_res_drift(law, n, k)
                  for k in (1, 2, 3) if 3 ** k <= 3 ** n}
        I_full = mutual_information_res_drift(law, n, n)

        row = {
            "n": n,
            "size_units": 2 * 3 ** (n - 1),
            "trunc_loss": trunc,
            "mod3_marginal": [m3[0], m3[1], m3[2]],
            "drift_mean_untilted": dmean0,
            "drift_mean_at_tstar": dmean,
            "Delta_n": delta,
            "argmax_xi": arg,
            "rho_tilted_corr_defect": rho,
            "rho_argmax_xi": rho_arg,
            "defect_by_v3": {str(k): v for k, v in sorted(by_v3.items())},
            "sample_xi": sample_xi,
            "Psi_sample_re": cf.real,
            "Psi_sample_im": cf.imag,
            "Psi_sample_abs": abs(cf),
            "I_res_mod3k_drift": {str(k): v for k, v in I_by_k.items()},
            "I_full_res_drift": I_full,
        }
        results.append(row)
        print(f"n={n}  size={row['size_units']}  trunc<{trunc:.1e}")
        print(f"   mod3 marginal = ({m3[0]:.6f}, {m3[1]:.6f}, {m3[2]:.6f})   "
              f"[exact target (0, 1/3, 2/3)]")
        print(f"   drift mean: untilted={dmean0:+.4f}  at t*={dmean:+.2e}  "
              f"[should be ~0 at t*]")
        print(f"   Delta_n = {delta:.6e}   (argmax 3 nmid xi = {arg})")
        print(f"   rho (tilted-measure corr defect, bounded) = {rho:.6e}  "
              f"(argmax xi = {rho_arg})")
        print(f"   defect by v3(xi): " +
              "  ".join(f"v3={k}:{by_v3[k]:.4e}" for k in sorted(by_v3)))
        print(f"   I(R mod 3^k; sgn D): " +
              "  ".join(f"k={k}:{I_by_k[k]:.4f}" for k in sorted(I_by_k)) +
              f"   I_full={I_full:.4f} bits")
        print()
        # incremental dump
        with open(os.path.join(DATA_DIR, "psi_factorization.json"), "w") as f:
            json.dump(results, f, indent=2)

    # --- trend analysis: is Delta_n a power-law decay or bounded below? ---
    print("=" * 74)
    print("TREND ANALYSIS")
    print("=" * 74)
    print(f"{'n':>3} {'Delta_n':>14} {'ratio':>8} {'log3 Delta':>12} "
          f"{'rho':>12} {'I_full':>8}")
    prev = None
    for row in results:
        d = row["Delta_n"]
        ratio = (d / prev) if (prev and prev > 0) else float("nan")
        log3d = math.log(d, 3) if d > 0 else float("nan")
        print(f"{row['n']:>3} {d:>14.6e} {ratio:>8.3f} {log3d:>12.4f} "
              f"{row['rho_tilted_corr_defect']:>12.6e} "
              f"{row['I_full_res_drift']:>8.4f}")
        prev = d
    print()
    print("Power-law read: if Delta_n ~ 3^{-theta n}, then 'log3 Delta' is ~ linear")
    print("in n with slope -theta < 0 (clean decay) and 'ratio' ~ 3^theta > 1 stable.")
    print("If Delta_n is bounded below, 'log3 Delta' flattens and ratio -> 1.")

    with open(os.path.join(DATA_DIR, "psi_factorization.json"), "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {os.path.join(DATA_DIR, 'psi_factorization.json')}")


if __name__ == "__main__":
    main()
