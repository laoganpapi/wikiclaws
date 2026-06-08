"""
Q3 smoothness signal — triple control (v_2, log2 k, omega(k)) + N=1e9 scan.

This probe extends sieve_q3_joint_control_probe.py with two finer tests:

  (A) Triple matching on (v_2 bucket, log2 odd-kernel bucket, omega(k) bucket)
      at N = 10^6, shell [16, 20), y = 10. (Reproduces C2 baseline at the
      same time using the joint matcher.)

  (B) N = 10^9 scan: at y = 10 in a shell large enough to give a
      meaningful smooth count, run C1 (v_2-only) and C2 (joint v_2, log2 k)
      matched gaps. Cannot keep a full sigma table for N = 10^9 in memory
      (~6 GB list). Instead:
        - Enumerate y-smooth integers in shell directly (n = 2^a 3^b 5^c 7^d)
          — only a few thousand.
        - Sample a large non-smooth pool uniformly from shell, classify by
          (v_2, log2 k, omega(k)) without computing sigma.
        - Compute sigma_inf only for smooth + matched subsamples using the
          accelerated Collatz primitives from verifier.py.

Three outcomes per the brief:
  - omega-matched stays >= 5% AND N=1e9 stabilizes >= 4%  -> signal robust
  - omega-matched drops to ~3% OR N=1e9 collapses        -> F1 triggered
  - mixed                                                 -> inconclusive

Author: Alex Ye.
"""
from __future__ import annotations

import json
import math
import os
import random
import sys
import time
from typing import Dict, List, Optional, Sequence, Tuple

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Make verifier importable for the accelerated sigma routines.
VERIFIER_DIR = os.path.abspath(os.path.join(
    THIS_DIR, "..", "..", "collatz", "experiments"))
if VERIFIER_DIR not in sys.path:
    sys.path.insert(0, VERIFIER_DIR)
import verifier  # noqa: E402

# =============================================================================
# Sigma tables / smoothness sieves (small N, in-memory).
# =============================================================================


def build_sigma_table(N: int) -> List[int]:
    """sigma_inf(n) under accelerated map. Same primitive as the joint probe."""
    t = [0] * (N + 1)
    for n in range(2, N + 1):
        if t[n] != 0:
            continue
        path = []
        m = n
        while m > N or t[m] == 0:
            path.append(m)
            if m & 1:
                m = (3 * m + 1) >> 1
            else:
                m >>= 1
            if m == 1:
                break
        base = 0 if m == 1 else t[m]
        k = len(path)
        for j, mm in enumerate(path):
            if mm <= N and t[mm] == 0:
                t[mm] = base + (k - j)
    return t


def largest_prime_factor_table(N: int) -> List[int]:
    pmax = [0] * (N + 1)
    for p in range(2, N + 1):
        if pmax[p] == 0:
            for k in range(p, N + 1, p):
                pmax[k] = p
    return pmax


def v2_table(N: int) -> List[int]:
    out = [0] * (N + 1)
    for n in range(2, N + 1):
        m = n
        c = 0
        while m & 1 == 0:
            m >>= 1
            c += 1
        out[n] = c
    return out


# =============================================================================
# Bucketing (same as joint probe + omega(k) bucket).
# =============================================================================

V2_BUCKETS = ("0", "1", "2", "3", "4", "5+")
LOG2K_BUCKETS = ("0-2", "3-5", "6-8", "9-11", "12-14", "15+",
                 "18+", "21+", "24+", "27+")  # extended for N=1e9
OMEGA_BUCKETS = ("0", "1", "2", "3", "4+")


def v2_bucket(v: int) -> str:
    return "5+" if v >= 5 else str(v)


def log2k_bucket(k: int) -> str:
    if k <= 0:
        return "0-2"
    lg = k.bit_length() - 1
    if lg <= 2:
        return "0-2"
    if lg <= 5:
        return "3-5"
    if lg <= 8:
        return "6-8"
    if lg <= 11:
        return "9-11"
    if lg <= 14:
        return "12-14"
    if lg <= 17:
        return "15+"
    if lg <= 20:
        return "18+"
    if lg <= 23:
        return "21+"
    if lg <= 26:
        return "24+"
    return "27+"


def omega_bucket(w: int) -> str:
    if w <= 3:
        return str(w)
    return "4+"


def omega_of_odd(k: int) -> int:
    """Number of distinct prime factors of odd k (k >= 1)."""
    if k <= 1:
        return 0
    w = 0
    # k is odd; trial-divide odd primes.
    p = 3
    m = k
    while p * p <= m:
        if m % p == 0:
            w += 1
            while m % p == 0:
                m //= p
        p += 2
    if m > 1:
        w += 1
    return w


def omega_of_odd_via_pmax(k: int, pmax: Sequence[int]) -> int:
    """Same as above but using a precomputed largest-prime-factor table."""
    if k <= 1:
        return 0
    w = 0
    while k > 1:
        p = pmax[k]
        w += 1
        while k % p == 0:
            k //= p
    return w


# =============================================================================
# Matched-subsample primitives.
# =============================================================================


def matched_subsample(target_hist: Dict[tuple, int],
                      pool_by_bucket: Dict[tuple, List[int]],
                      rng: random.Random) -> Tuple[List[int],
                                                    Dict[tuple, Dict[str, int]]]:
    """Match on arbitrary-tuple buckets. Returns (sample, coverage)."""
    sample: List[int] = []
    coverage: Dict[tuple, Dict[str, int]] = {}
    for bk, want in target_hist.items():
        have = pool_by_bucket.get(bk, [])
        take = min(want, len(have))
        if take < len(have):
            sample.extend(rng.sample(have, take))
        else:
            sample.extend(have)
        coverage[bk] = {"target": want, "achieved": take,
                        "pool_supply": len(have)}
    return sample, coverage


def bootstrap_gap_ci(smooth_vals: Sequence[float],
                     matched_vals: Sequence[float],
                     n_boot: int = 1000,
                     seed: int = 1,
                     alpha: float = 0.05) -> Dict[str, float]:
    rng = random.Random(seed)
    s = list(smooth_vals)
    m = list(matched_vals)
    n_s, n_m = len(s), len(m)
    if n_s == 0 or n_m == 0:
        return {}
    gaps: List[float] = []
    for _ in range(n_boot):
        ss = sum(s[rng.randrange(n_s)] for _ in range(n_s)) / n_s
        mm = sum(m[rng.randrange(n_m)] for _ in range(n_m)) / n_m
        if mm > 0:
            gaps.append(1.0 - ss / mm)
    gaps.sort()
    lo = gaps[int(alpha / 2 * n_boot)]
    hi = gaps[int((1 - alpha / 2) * n_boot) - 1]
    sm = sum(s) / n_s
    mm = sum(m) / n_m
    return {
        "smooth_mean": sm, "matched_mean": mm,
        "point_gap_pct": (1 - sm / mm) * 100,
        "gap_ci_lo_pct": lo * 100, "gap_ci_hi_pct": hi * 100,
        "n_boot": n_boot, "n_smooth": n_s, "n_matched": n_m,
    }


# =============================================================================
# PART A: triple (v_2, log2 k, omega(k)) control at N=1e6.
# =============================================================================


def run_triple_N1e6(N: int = 10**6,
                    shell: Tuple[int, int] = (16, 20),
                    y_values: Tuple[int, ...] = (10, 20, 50, 100),
                    seed: int = 20260608,
                    n_boot: int = 1000) -> Dict:
    """C2 reproduction + triple (v_2, log2 k, omega) matching at small N."""
    rng = random.Random(seed)
    out: Dict = {"N": N, "shell": list(shell), "y_values": list(y_values),
                 "seed": seed, "n_boot": n_boot}

    t0 = time.time()
    print(f"[A1] sigma table N={N} ...", flush=True)
    sigma_tab = build_sigma_table(N)
    print(f"     {time.time()-t0:.1f}s", flush=True)

    t0 = time.time()
    print("[A2] largest-prime-factor table ...", flush=True)
    pmax = largest_prime_factor_table(N)
    print(f"     {time.time()-t0:.1f}s", flush=True)

    t0 = time.time()
    print("[A3] v_2 table ...", flush=True)
    v2 = v2_table(N)
    print(f"     {time.time()-t0:.1f}s", flush=True)

    L_lo, L_hi = shell
    lo = max(2, 1 << L_lo)
    hi = min(N + 1, 1 << L_hi)
    shell_all = list(range(lo, hi))

    def ratio(n): return sigma_tab[n] / math.log2(n)

    shell_mean = sum(ratio(n) for n in shell_all) / len(shell_all)
    out["shell_size"] = len(shell_all)
    out["shell_mean"] = shell_mean
    print(f"[A4] shell size {len(shell_all)}, mean {shell_mean:.4f}",
          flush=True)

    out["per_y"] = {}
    for y in y_values:
        print(f"\n--- y={y} ---", flush=True)
        smooth = [n for n in shell_all if pmax[n] <= y]
        n_smooth = len(smooth)
        smooth_vals = [ratio(n) for n in smooth]
        smooth_mean = sum(smooth_vals) / n_smooth
        smooth_set = set(smooth)
        nonsmooth = [n for n in shell_all if n not in smooth_set]

        # Compute (v_2, log2 k) joint key for every shell element once.
        def joint_key(n):
            v = v2[n]
            k = n >> v
            return (v2_bucket(v), log2k_bucket(k))

        def triple_key(n):
            v = v2[n]
            k = n >> v
            w = omega_of_odd_via_pmax(k, pmax) if k > 1 else 0
            return (v2_bucket(v), log2k_bucket(k), omega_bucket(w))

        # ---- C2 joint match (reproduction) ----
        hist_joint: Dict[tuple, int] = {}
        for n in smooth:
            b = joint_key(n)
            hist_joint[b] = hist_joint.get(b, 0) + 1
        pool_joint: Dict[tuple, List[int]] = {}
        for n in nonsmooth:
            pool_joint.setdefault(joint_key(n), []).append(n)
        mj, cov_j = matched_subsample(hist_joint, pool_joint, rng)
        mj_vals = [ratio(n) for n in mj]
        c2_ci = bootstrap_gap_ci(smooth_vals, mj_vals, n_boot=n_boot,
                                 seed=seed + y, alpha=0.05)
        deficits_j = {f"{k[0]}|{k[1]}": v for k, v in cov_j.items()
                      if v["target"] > v["achieved"]}

        # ---- Triple match (v_2, log2 k, omega) ----
        hist_trip: Dict[tuple, int] = {}
        smooth_triple_keys = []
        for n in smooth:
            b = triple_key(n)
            smooth_triple_keys.append(b)
            hist_trip[b] = hist_trip.get(b, 0) + 1
        pool_trip: Dict[tuple, List[int]] = {}
        for n in nonsmooth:
            pool_trip.setdefault(triple_key(n), []).append(n)
        mt, cov_t = matched_subsample(hist_trip, pool_trip, rng)
        mt_vals = [ratio(n) for n in mt]
        c3_ci = bootstrap_gap_ci(smooth_vals, mt_vals, n_boot=n_boot,
                                 seed=seed + y + 1, alpha=0.05)
        deficits_t = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in cov_t.items()
                      if v["target"] > v["achieved"]}

        # ---- Restricted triple (drop smooth in zero-supply cells) ----
        zero_cells_t = {k for k, v in cov_t.items() if v["pool_supply"] == 0}
        retained_idx = [i for i, b in enumerate(smooth_triple_keys)
                        if b not in zero_cells_t]
        smooth_vals_r = [smooth_vals[i] for i in retained_idx]
        # Matched subsample is already restricted to non-empty cells.
        c3r_ci = (bootstrap_gap_ci(smooth_vals_r, mt_vals, n_boot=n_boot,
                                   seed=seed + y + 2, alpha=0.05)
                  if smooth_vals_r and mt_vals else {})

        # ---- omega distribution among smooth ----
        omega_dist_smooth: Dict[int, int] = {}
        for n in smooth:
            v = v2[n]; k = n >> v
            w = omega_of_odd_via_pmax(k, pmax) if k > 1 else 0
            omega_dist_smooth[w] = omega_dist_smooth.get(w, 0) + 1

        # ---- omega distribution within MATCHED non-smooth subsample ----
        omega_dist_matched: Dict[int, int] = {}
        for n in mt:
            v = v2[n]; k = n >> v
            w = omega_of_odd_via_pmax(k, pmax) if k > 1 else 0
            omega_dist_matched[w] = omega_dist_matched.get(w, 0) + 1

        # ---- Unmatched omega distribution in nonsmooth pool (for context) ----
        omega_dist_pool: Dict[int, int] = {}
        for n in nonsmooth:
            v = v2[n]; k = n >> v
            w = omega_of_odd_via_pmax(k, pmax) if k > 1 else 0
            omega_dist_pool[w] = omega_dist_pool.get(w, 0) + 1

        print(f"  n_smooth={n_smooth}  smooth_mean={smooth_mean:.4f}",
              flush=True)
        print(f"  [C2 joint]  drop={c2_ci.get('point_gap_pct',float('nan')):.2f}%  "
              f"CI95=[{c2_ci.get('gap_ci_lo_pct',float('nan')):.2f}, "
              f"{c2_ci.get('gap_ci_hi_pct',float('nan')):.2f}]%  "
              f"n_match={len(mj)}  deficits={len(deficits_j)}", flush=True)
        print(f"  [C3 triple] drop={c3_ci.get('point_gap_pct',float('nan')):.2f}%  "
              f"CI95=[{c3_ci.get('gap_ci_lo_pct',float('nan')):.2f}, "
              f"{c3_ci.get('gap_ci_hi_pct',float('nan')):.2f}]%  "
              f"n_match={len(mt)}  deficits={len(deficits_t)}", flush=True)
        print(f"  [C3r rest ] drop={c3r_ci.get('point_gap_pct',float('nan')):.2f}%  "
              f"CI95=[{c3r_ci.get('gap_ci_lo_pct',float('nan')):.2f}, "
              f"{c3r_ci.get('gap_ci_hi_pct',float('nan')):.2f}]%  "
              f"n_smooth_retained={len(smooth_vals_r)}", flush=True)
        print(f"  omega smooth   : {omega_dist_smooth}", flush=True)
        print(f"  omega matched  : {omega_dist_matched}", flush=True)
        print(f"  omega pool     : "
              f"{ {k: v for k, v in sorted(omega_dist_pool.items())} }",
              flush=True)

        out["per_y"][str(y)] = {
            "y": y, "n_smooth": n_smooth, "smooth_mean": smooth_mean,
            "shell_mean": shell_mean,
            "c2_joint": {
                "n_matched": len(mj),
                "matched_mean": (sum(mj_vals) / len(mj_vals)) if mj_vals else float("nan"),
                "drop_pct": c2_ci.get("point_gap_pct"),
                "bootstrap_ci": c2_ci,
                "n_deficit_cells": len(deficits_j),
                "deficits_sample": dict(list(deficits_j.items())[:8]),
            },
            "c3_triple": {
                "n_matched": len(mt),
                "matched_mean": (sum(mt_vals) / len(mt_vals)) if mt_vals else float("nan"),
                "drop_pct": c3_ci.get("point_gap_pct"),
                "bootstrap_ci": c3_ci,
                "n_deficit_cells": len(deficits_t),
                "deficits_sample": dict(list(deficits_t.items())[:8]),
                "smooth_cells": len(hist_trip),
            },
            "c3_triple_restricted": {
                "n_smooth_retained": len(smooth_vals_r),
                "n_dropped": n_smooth - len(smooth_vals_r),
                "drop_pct": c3r_ci.get("point_gap_pct"),
                "bootstrap_ci": c3r_ci,
            },
            "omega_distribution": {
                "smooth": {str(k): v for k, v in sorted(omega_dist_smooth.items())},
                "matched": {str(k): v for k, v in sorted(omega_dist_matched.items())},
                "pool": {str(k): v for k, v in sorted(omega_dist_pool.items())},
            },
        }
    return out


# =============================================================================
# PART B: N = 1e9 (or 3e8) scan via sampling — no full sigma table.
# =============================================================================


def enumerate_y10_smooth(N: int, L_lo: int, L_hi: int) -> List[int]:
    """All n in [2^L_lo, min(N+1, 2^L_hi)) with prime factors in {2,3,5,7}."""
    lo = max(2, 1 << L_lo)
    hi = min(N + 1, 1 << L_hi)
    out = []
    n = 1
    # Enumerate (a,b,c,d): 2^a 3^b 5^c 7^d in [lo, hi).
    a = 0
    while (1 << a) < hi:
        pa = 1 << a
        b = 0
        while pa * (3 ** b) < hi:
            pb = pa * (3 ** b)
            c = 0
            while pb * (5 ** c) < hi:
                pc = pb * (5 ** c)
                d = 0
                while pc * (7 ** d) < hi:
                    val = pc * (7 ** d)
                    if val >= lo:
                        out.append(val)
                    d += 1
                c += 1
            b += 1
        a += 1
    out.sort()
    return out


SMALL_PRIMES_UP_TO_10 = (2, 3, 5, 7)
SMALL_PRIMES_3_5_7 = (3, 5, 7)


def is_y10_smooth(n: int) -> bool:
    m = n
    for p in SMALL_PRIMES_UP_TO_10:
        while m % p == 0:
            m //= p
    return m == 1


def odd_kernel_and_v2(n: int) -> Tuple[int, int]:
    v = 0
    m = n
    while m & 1 == 0:
        m >>= 1
        v += 1
    return m, v


def omega_of_odd_trial(k: int) -> int:
    """Number of distinct prime factors of odd k via trial division."""
    if k <= 1:
        return 0
    w = 0
    m = k
    p = 3
    while p * p <= m:
        if m % p == 0:
            w += 1
            while m % p == 0:
                m //= p
        p += 2
    if m > 1:
        w += 1
    return w


def _build_acc_helpers(sieve_k: int = 16, cache_limit: int = 1 << 20):
    a_tab, b_tab, _ = verifier.build_sieve(sieve_k)
    cache = verifier._build_small_cache(cache_limit)
    return a_tab, b_tab, cache, sieve_k, cache_limit


def sigma_inf_fast(n: int, helpers) -> int:
    a_tab, b_tab, cache, sieve_k, cache_limit = helpers
    if n == 1:
        return 0
    if n < cache_limit:
        return cache[n]
    mask = (1 << sieve_k) - 1
    m = n
    steps = 0
    while m >= cache_limit:
        if m >= (1 << sieve_k):
            r = m & mask
            q = m >> sieve_k
            m = (3 ** a_tab[r]) * q + b_tab[r]
            steps += sieve_k
        else:
            if m & 1:
                m = (3 * m + 1) >> 1
            else:
                m >>= 1
            steps += 1
    return steps + cache[m]


def run_large_N_scan(N: int,
                     shell: Tuple[int, int],
                     n_pool_samples: int,
                     seed: int = 20260608,
                     n_boot: int = 1000,
                     include_triple: bool = True) -> Dict:
    """C1 (v_2-only) + C2 (joint v_2, log2 k) + C3 (triple) matched gaps.

    Strategy:
      - Enumerate all y=10 smooth in shell (small set).
      - Sample n_pool_samples random non-smooth integers from shell, keep
        their (v_2, log2 k, omega(k)) classification.
      - Match smooth subsample on each control, compute sigma_inf on
        smooth + matched only.
    """
    rng = random.Random(seed)
    L_lo, L_hi = shell
    lo = max(2, 1 << L_lo)
    hi = min(N + 1, 1 << L_hi)
    shell_size = hi - lo
    print(f"[B-setup] N={N}, shell [2^{L_lo}, 2^{L_hi})  size={shell_size}",
          flush=True)

    # Enumerate smooth.
    t0 = time.time()
    smooth = enumerate_y10_smooth(N, L_lo, L_hi)
    print(f"[B1] y=10 smooth in shell: {len(smooth)} integers  "
          f"({time.time()-t0:.1f}s)", flush=True)

    # Build accelerated helpers.
    print(f"[B2] building accelerated Collatz helpers ...", flush=True)
    t0 = time.time()
    helpers = _build_acc_helpers(sieve_k=16, cache_limit=1 << 20)
    print(f"     {time.time()-t0:.1f}s", flush=True)

    # sigma for smooth.
    print(f"[B3] sigma_inf for {len(smooth)} smooth integers ...", flush=True)
    t0 = time.time()
    smooth_sigma = [sigma_inf_fast(n, helpers) for n in smooth]
    print(f"     {time.time()-t0:.1f}s", flush=True)
    smooth_vals = [smooth_sigma[i] / math.log2(smooth[i])
                   for i in range(len(smooth))]
    smooth_mean = sum(smooth_vals) / len(smooth_vals)

    # Classify smooth.
    print(f"[B4] classifying smooth (joint + triple keys) ...", flush=True)
    smooth_v2_keys = []
    smooth_joint_keys = []
    smooth_triple_keys = []
    omega_dist_smooth: Dict[int, int] = {}
    for n in smooth:
        k, v = odd_kernel_and_v2(n)
        w = omega_of_odd_trial(k)
        smooth_v2_keys.append(v2_bucket(v))
        smooth_joint_keys.append((v2_bucket(v), log2k_bucket(k)))
        smooth_triple_keys.append((v2_bucket(v), log2k_bucket(k),
                                   omega_bucket(w)))
        omega_dist_smooth[w] = omega_dist_smooth.get(w, 0) + 1

    hist_v2: Dict[str, int] = {}
    for k in smooth_v2_keys:
        hist_v2[k] = hist_v2.get(k, 0) + 1
    hist_joint: Dict[tuple, int] = {}
    for k in smooth_joint_keys:
        hist_joint[k] = hist_joint.get(k, 0) + 1
    hist_triple: Dict[tuple, int] = {}
    for k in smooth_triple_keys:
        hist_triple[k] = hist_triple.get(k, 0) + 1

    # Sample non-smooth pool — uniform shell sample.
    print(f"[B5a] uniform shell sampling ({n_pool_samples} samples) ...",
          flush=True)
    t0 = time.time()
    pool_v2: Dict[str, List[int]] = {}
    pool_joint: Dict[tuple, List[int]] = {}
    pool_triple: Dict[tuple, List[int]] = {}
    seen = set()
    drawn = 0
    rejected_smooth = 0
    attempts = 0
    target = n_pool_samples
    sampler = random.Random(seed + 1)
    while drawn < target:
        n = sampler.randrange(lo, hi)
        attempts += 1
        if n in seen:
            continue
        seen.add(n)
        if is_y10_smooth(n):
            rejected_smooth += 1
            continue
        k, v = odd_kernel_and_v2(n)
        w = omega_of_odd_trial(k)
        kb_v2 = v2_bucket(v)
        kb_j = (kb_v2, log2k_bucket(k))
        kb_t = (kb_v2, log2k_bucket(k), omega_bucket(w))
        pool_v2.setdefault(kb_v2, []).append(n)
        pool_joint.setdefault(kb_j, []).append(n)
        pool_triple.setdefault(kb_t, []).append(n)
        drawn += 1
        if drawn % 200_000 == 0:
            print(f"     drawn={drawn} (attempts={attempts}) "
                  f"elapsed={time.time()-t0:.0f}s", flush=True)
    print(f"     {time.time()-t0:.1f}s  attempts={attempts}  "
          f"rejected_smooth={rejected_smooth}", flush=True)

    # ---- B5b: targeted oversampling for high-v_2 cells ----
    # For v_2 buckets {3, 4, 5+}, sample directly within the v_2-stratified
    # subshell to populate rare (v_2, log2 k [, omega]) cells.
    # n with v_2 = v >= 1 has form n = 2^v * k with k odd in [ceil(lo/2^v),
    # floor((hi-1)/2^v)].
    print(f"[B5b] targeted v_2 stratified oversampling ...", flush=True)
    t0 = time.time()
    targeted_per_v = max(60_000, n_pool_samples // 10)
    for v in (3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 18, 22, 25, 27):
        if (1 << (v + 1)) > hi:  # even 2^(v+1) larger than shell top
            continue
        k_lo = (lo + (1 << v) - 1) >> v  # ceil(lo / 2^v)
        k_hi = (hi - 1) >> v             # floor((hi-1)/2^v)
        if k_hi < k_lo:
            continue
        # Force k odd: take k_lo to next odd, step 2.
        if k_lo % 2 == 0:
            k_lo += 1
        if k_hi % 2 == 0:
            k_hi -= 1
        if k_hi < k_lo:
            continue
        # Sample odd k uniformly.
        target_v = min(targeted_per_v,
                       max(0, (k_hi - k_lo) // 2 + 1))
        drawn_v = 0
        attempts_v = 0
        kb_v2 = v2_bucket(v)
        while drawn_v < target_v and attempts_v < target_v * 4:
            attempts_v += 1
            k = sampler.randrange(k_lo, k_hi + 2, 2)
            n = (k << v)
            if n in seen or n < lo or n >= hi:
                continue
            seen.add(n)
            if is_y10_smooth(n):
                continue
            w = omega_of_odd_trial(k)
            kb_j = (kb_v2, log2k_bucket(k))
            kb_t = (kb_v2, log2k_bucket(k), omega_bucket(w))
            pool_v2.setdefault(kb_v2, []).append(n)
            pool_joint.setdefault(kb_j, []).append(n)
            pool_triple.setdefault(kb_t, []).append(n)
            drawn_v += 1
        print(f"     v_2={v}: drew {drawn_v}", flush=True)
    print(f"     {time.time()-t0:.1f}s", flush=True)

    out: Dict = {
        "N": N, "shell": list(shell), "shell_size": shell_size,
        "n_pool_samples": n_pool_samples, "seed": seed,
        "n_boot": n_boot,
        "n_smooth": len(smooth), "smooth_mean": smooth_mean,
        "omega_dist_smooth": {str(k): v for k, v in sorted(omega_dist_smooth.items())},
    }

    # ---- C1: v_2-only match ----
    print(f"[B6] C1 v_2-only matched ...", flush=True)
    t0 = time.time()
    sample_c1, cov_c1 = matched_subsample(hist_v2, pool_v2, rng)
    sigma_c1 = [sigma_inf_fast(n, helpers) for n in sample_c1]
    vals_c1 = [sigma_c1[i] / math.log2(sample_c1[i])
               for i in range(len(sample_c1))]
    ci_c1 = bootstrap_gap_ci(smooth_vals, vals_c1, n_boot=n_boot,
                             seed=seed + 100, alpha=0.05)
    deficits_c1 = {k: v for k, v in cov_c1.items()
                   if v["target"] > v["achieved"]}
    print(f"     {time.time()-t0:.1f}s  drop={ci_c1.get('point_gap_pct'):.2f}%  "
          f"CI95=[{ci_c1.get('gap_ci_lo_pct'):.2f},"
          f"{ci_c1.get('gap_ci_hi_pct'):.2f}]%  n_match={len(sample_c1)}",
          flush=True)

    out["c1_v2_only"] = {
        "n_matched": len(sample_c1),
        "matched_mean": (sum(vals_c1) / len(vals_c1)) if vals_c1 else float("nan"),
        "drop_pct": ci_c1.get("point_gap_pct"),
        "bootstrap_ci": ci_c1,
        "deficits": deficits_c1,
    }

    # ---- C2: joint match ----
    print(f"[B7] C2 joint (v_2, log2 k) matched ...", flush=True)
    t0 = time.time()
    sample_c2, cov_c2 = matched_subsample(hist_joint, pool_joint, rng)
    sigma_c2 = [sigma_inf_fast(n, helpers) for n in sample_c2]
    vals_c2 = [sigma_c2[i] / math.log2(sample_c2[i])
               for i in range(len(sample_c2))]
    ci_c2 = bootstrap_gap_ci(smooth_vals, vals_c2, n_boot=n_boot,
                             seed=seed + 101, alpha=0.05)
    deficits_c2 = {f"{k[0]}|{k[1]}": v for k, v in cov_c2.items()
                   if v["target"] > v["achieved"]}
    print(f"     {time.time()-t0:.1f}s  drop={ci_c2.get('point_gap_pct'):.2f}%  "
          f"CI95=[{ci_c2.get('gap_ci_lo_pct'):.2f},"
          f"{ci_c2.get('gap_ci_hi_pct'):.2f}]%  n_match={len(sample_c2)}  "
          f"deficits={len(deficits_c2)}", flush=True)

    out["c2_joint"] = {
        "n_matched": len(sample_c2),
        "matched_mean": (sum(vals_c2) / len(vals_c2)) if vals_c2 else float("nan"),
        "drop_pct": ci_c2.get("point_gap_pct"),
        "bootstrap_ci": ci_c2,
        "n_deficit_cells": len(deficits_c2),
        "deficits_sample": dict(list(deficits_c2.items())[:8]),
    }

    if include_triple:
        # ---- C3: triple match ----
        print(f"[B8] C3 triple (v_2, log2 k, omega) matched ...", flush=True)
        t0 = time.time()
        sample_c3, cov_c3 = matched_subsample(hist_triple, pool_triple, rng)
        sigma_c3 = [sigma_inf_fast(n, helpers) for n in sample_c3]
        vals_c3 = [sigma_c3[i] / math.log2(sample_c3[i])
                   for i in range(len(sample_c3))]
        ci_c3 = bootstrap_gap_ci(smooth_vals, vals_c3, n_boot=n_boot,
                                 seed=seed + 102, alpha=0.05)
        deficits_c3 = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in cov_c3.items()
                       if v["target"] > v["achieved"]}

        # Restricted (drop smooth in zero-supply cells)
        zero_cells_c3 = {k for k, v in cov_c3.items()
                         if v["pool_supply"] == 0}
        retained = [i for i, b in enumerate(smooth_triple_keys)
                    if b not in zero_cells_c3]
        smooth_vals_r = [smooth_vals[i] for i in retained]
        ci_c3r = (bootstrap_gap_ci(smooth_vals_r, vals_c3, n_boot=n_boot,
                                   seed=seed + 103, alpha=0.05)
                  if smooth_vals_r else {})

        print(f"     {time.time()-t0:.1f}s  drop={ci_c3.get('point_gap_pct'):.2f}%  "
              f"CI95=[{ci_c3.get('gap_ci_lo_pct'):.2f},"
              f"{ci_c3.get('gap_ci_hi_pct'):.2f}]%  n_match={len(sample_c3)}  "
              f"deficits={len(deficits_c3)}", flush=True)
        print(f"     restricted drop={ci_c3r.get('point_gap_pct',float('nan')):.2f}% "
              f"CI95=[{ci_c3r.get('gap_ci_lo_pct',float('nan')):.2f},"
              f"{ci_c3r.get('gap_ci_hi_pct',float('nan')):.2f}]%  "
              f"n_retained={len(smooth_vals_r)}", flush=True)

        out["c3_triple"] = {
            "n_matched": len(sample_c3),
            "matched_mean": (sum(vals_c3) / len(vals_c3)) if vals_c3 else float("nan"),
            "drop_pct": ci_c3.get("point_gap_pct"),
            "bootstrap_ci": ci_c3,
            "n_deficit_cells": len(deficits_c3),
            "deficits_sample": dict(list(deficits_c3.items())[:8]),
        }
        out["c3_triple_restricted"] = {
            "n_smooth_retained": len(smooth_vals_r),
            "n_dropped": len(smooth_vals) - len(smooth_vals_r),
            "drop_pct": ci_c3r.get("point_gap_pct"),
            "bootstrap_ci": ci_c3r,
        }

    return out


# =============================================================================
# Main.
# =============================================================================


def main() -> int:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["triple_1e6", "scan_large", "all"],
                   default="all")
    p.add_argument("--N_large", type=int, default=10**9)
    p.add_argument("--shell_large", type=str, default="25,30")
    p.add_argument("--pool_samples", type=int, default=300_000)
    p.add_argument("--n_boot", type=int, default=1000)
    args = p.parse_args()

    results: Dict = {}
    wall = time.time()

    if args.mode in ("triple_1e6", "all"):
        print("\n========== PART A: triple control at N=1e6 ==========\n",
              flush=True)
        a = run_triple_N1e6(n_boot=args.n_boot)
        results["partA_triple_N1e6"] = a
        with open(os.path.join(DATA_DIR,
                               "sieve_q3_omega_N1e9_partA.json"), "w") as f:
            json.dump(a, f, indent=2, default=str)

    if args.mode in ("scan_large", "all"):
        L_lo, L_hi = (int(x) for x in args.shell_large.split(","))
        print(f"\n========== PART B: N={args.N_large}, shell "
              f"[2^{L_lo}, 2^{L_hi}) ==========\n", flush=True)
        b = run_large_N_scan(N=args.N_large, shell=(L_lo, L_hi),
                             n_pool_samples=args.pool_samples,
                             n_boot=args.n_boot, include_triple=True)
        results["partB_scan_large"] = b
        with open(os.path.join(DATA_DIR,
                               "sieve_q3_omega_N1e9_partB.json"), "w") as f:
            json.dump(b, f, indent=2, default=str)

    results["wall_time_total_seconds"] = time.time() - wall
    out_path = os.path.join(DATA_DIR, "sieve_q3_omega_N1e9.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n[done] wrote {out_path}  total wall = "
          f"{results['wall_time_total_seconds']:.1f}s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
