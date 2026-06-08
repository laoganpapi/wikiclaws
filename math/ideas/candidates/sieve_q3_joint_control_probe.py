"""
Q3 smoothness signal — joint (v_2, log2 odd-kernel) control probe.

Background. The prior probe (sieve_q3_control_probe.py) v_2-matched a
non-smooth subsample to the y=10 smooth population in shell [16, 20) and
reduced the headline 24% drop in mean sigma_inf/log2(n) to 13.4%. The
remaining 13% could still be a confounder living *inside* each v_2 bucket:
the odd-kernel size. Write n = 2^{v_2(n)} * k with k odd; smooth integers
have k built from {3, 5, 7} (for y=10), which biases log2(k) downward
relative to a random odd integer in the same v_2-bucket.

This probe performs the natural next-finer control: jointly match the
non-smooth subsample on (v_2 bucket, log2(odd_kernel) bucket).

Tasks:
  (1) Reproduce the C1 v_2-only matched 13.4% drop at y=10 (sanity).
  (2) Build joint (v_2, log2 k) distribution for y=10 smooth in shell.
  (3) Joint-matched non-smooth subsample; compute mean sigma_inf/log2(n).
  (4) Bootstrap 95% CI on the matched gap (1000 resamples).
  (5) y-scan: repeat at y in {10, 20, 50, 100} under joint matching.
  (6) (Optional) N=10^8 spot check at y=10.

Author: Alex Ye.
"""

from __future__ import annotations

import json
import math
import os
import random
import sys
import time
from typing import Dict, List, Tuple, Sequence

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)


# -----------------------------------------------------------------------------
# Tables (same primitives as sieve_q3_control_probe.py)
# -----------------------------------------------------------------------------

def build_sigma_table(N: int) -> List[int]:
    """sigma_inf(n) under accelerated map (even n -> n/2; odd n -> (3n+1)/2)."""
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


# -----------------------------------------------------------------------------
# Bucketing
# -----------------------------------------------------------------------------

V2_BUCKETS = ("0", "1", "2", "3", "4", "5+")


def v2_bucket(v: int) -> str:
    if v >= 5:
        return "5+"
    return str(v)


# log2(k) buckets. For shell [16, 20), n in [2^16, 2^20). With v_2 up to 5+,
# k = n / 2^v_2 can range widely. Use buckets that cover the realized range.
# Realized log2(k) for shell + v_2 buckets is up to ~19 (n ~ 2^20 / 2^0 = 2^20).
LOG2K_BUCKETS = ("0-2", "3-5", "6-8", "9-11", "12-14", "15+")


def log2k_bucket(k: int) -> str:
    if k <= 0:
        return "0-2"
    lg = k.bit_length() - 1  # floor(log2 k)
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
    return "15+"


def joint_bucket(n: int, v: int) -> Tuple[str, str]:
    k = n >> v  # odd kernel
    return (v2_bucket(v), log2k_bucket(k))


# -----------------------------------------------------------------------------
# Histograms / means
# -----------------------------------------------------------------------------

def hist_v2(idx: Sequence[int], v2: Sequence[int]) -> Dict[str, int]:
    h = {b: 0 for b in V2_BUCKETS}
    for n in idx:
        h[v2_bucket(v2[n])] += 1
    return h


def hist_joint(idx: Sequence[int], v2: Sequence[int]) -> Dict[Tuple[str, str], int]:
    h: Dict[Tuple[str, str], int] = {}
    for n in idx:
        b = joint_bucket(n, v2[n])
        h[b] = h.get(b, 0) + 1
    return h


def mean_ratio(idx: Sequence[int], sigma_tab: Sequence[int]) -> Tuple[float, int]:
    s = 0.0
    c = 0
    for n in idx:
        if n >= 2:
            s += sigma_tab[n] / math.log2(n)
            c += 1
    return (s / c if c > 0 else float("nan")), c


# -----------------------------------------------------------------------------
# Matched-subsample routines
# -----------------------------------------------------------------------------

def matched_subsample_v2(target_hist: Dict[str, int],
                          pool_idx: Sequence[int],
                          v2: Sequence[int],
                          rng: random.Random) -> Tuple[List[int], Dict[str, int], Dict[str, int]]:
    """v_2-only matched subsample (for C1 reproduction)."""
    buckets: Dict[str, List[int]] = {b: [] for b in V2_BUCKETS}
    for n in pool_idx:
        buckets[v2_bucket(v2[n])].append(n)
    pool_hist = {k: len(v) for k, v in buckets.items()}

    sample: List[int] = []
    achieved: Dict[str, int] = {}
    for bk, want in target_hist.items():
        have = buckets[bk]
        take = min(want, len(have))
        if take < len(have):
            sample.extend(rng.sample(have, take))
        else:
            sample.extend(have)
        achieved[bk] = take
    return sample, achieved, pool_hist


def matched_subsample_joint(target_hist: Dict[Tuple[str, str], int],
                             pool_idx: Sequence[int],
                             v2: Sequence[int],
                             rng: random.Random
                             ) -> Tuple[List[int], Dict[Tuple[str, str], Dict[str, int]]]:
    """Joint (v_2, log2 k)-matched subsample. Returns (sample, coverage)."""
    buckets: Dict[Tuple[str, str], List[int]] = {}
    for n in pool_idx:
        b = joint_bucket(n, v2[n])
        buckets.setdefault(b, []).append(n)

    sample: List[int] = []
    coverage: Dict[Tuple[str, str], Dict[str, int]] = {}
    for bk, want in target_hist.items():
        have = buckets.get(bk, [])
        take = min(want, len(have))
        if take < len(have):
            sample.extend(rng.sample(have, take))
        else:
            sample.extend(have)
        coverage[bk] = {"target": want, "achieved": take, "pool_supply": len(have)}
    # Also note any pool-only buckets (these are non-smooth-only cells, fine).
    return sample, coverage


# -----------------------------------------------------------------------------
# Bootstrap CI helpers
# -----------------------------------------------------------------------------

def bootstrap_gap_ci(smooth_vals: Sequence[float],
                      matched_vals: Sequence[float],
                      n_boot: int = 1000,
                      seed: int = 1,
                      alpha: float = 0.05) -> Dict[str, float]:
    """Bootstrap the gap (1 - mean(smooth)/mean(matched)) by resampling both
    populations independently with replacement. Returns mean of each, gap,
    and (alpha/2, 1-alpha/2) CI on the gap percentage.
    """
    rng = random.Random(seed)
    s_arr = list(smooth_vals)
    m_arr = list(matched_vals)
    n_s = len(s_arr)
    n_m = len(m_arr)
    gaps: List[float] = []
    for _ in range(n_boot):
        # Resample with replacement.
        ss = sum(s_arr[rng.randrange(n_s)] for _ in range(n_s)) / n_s
        mm = sum(m_arr[rng.randrange(n_m)] for _ in range(n_m)) / n_m
        if mm > 0:
            gaps.append(1.0 - ss / mm)
    gaps.sort()
    lo = gaps[int(alpha / 2 * n_boot)]
    hi = gaps[int((1 - alpha / 2) * n_boot) - 1]
    smooth_mean = sum(s_arr) / n_s
    matched_mean = sum(m_arr) / n_m
    point_gap = 1.0 - smooth_mean / matched_mean
    return {
        "smooth_mean": smooth_mean,
        "matched_mean": matched_mean,
        "point_gap_pct": point_gap * 100,
        "gap_ci_lo_pct": lo * 100,
        "gap_ci_hi_pct": hi * 100,
        "n_boot": n_boot,
        "n_smooth": n_s,
        "n_matched": n_m,
    }


# -----------------------------------------------------------------------------
# Probe
# -----------------------------------------------------------------------------

def shell_indices(N: int, L_lo: int, L_hi: int) -> List[int]:
    lo = max(2, 1 << L_lo)
    hi = min(N + 1, 1 << L_hi)
    return list(range(lo, hi))


def smooth_filter(idx: Sequence[int], pmax: Sequence[int], y: int) -> List[int]:
    return [n for n in idx if pmax[n] <= y]


def ratio_vals(idx: Sequence[int], sigma_tab: Sequence[int]) -> List[float]:
    """Per-element sigma_inf(n)/log2(n) (skipping n<2)."""
    out: List[float] = []
    for n in idx:
        if n >= 2:
            out.append(sigma_tab[n] / math.log2(n))
    return out


def run_probe(N: int = 10**6,
              shell: Tuple[int, int] = (16, 20),
              y_values: Tuple[int, ...] = (10, 20, 50, 100),
              seed: int = 20260608,
              n_boot: int = 1000) -> Dict:
    rng = random.Random(seed)
    out: Dict = {
        "N": N,
        "shell": list(shell),
        "y_values": list(y_values),
        "seed": seed,
        "n_boot": n_boot,
        "v2_buckets": list(V2_BUCKETS),
        "log2k_buckets": list(LOG2K_BUCKETS),
    }

    print(f"[setup] N = {N}, shell log2 n in [{shell[0]}, {shell[1]})", flush=True)

    t0 = time.time()
    print("[1/3] sigma_inf table ...", flush=True)
    sigma_tab = build_sigma_table(N)
    print(f"      done in {time.time()-t0:.2f}s", flush=True)

    t0 = time.time()
    print("[2/3] largest-prime-factor sieve ...", flush=True)
    pmax = largest_prime_factor_table(N)
    print(f"      done in {time.time()-t0:.2f}s", flush=True)

    t0 = time.time()
    print("[3/3] v_2 table ...", flush=True)
    v2 = v2_table(N)
    print(f"      done in {time.time()-t0:.2f}s", flush=True)

    L_lo, L_hi = shell
    shell_all = shell_indices(N, L_lo, L_hi)
    print(f"[shell] |shell_all| = {len(shell_all)}", flush=True)

    shell_mean_baseline, _ = mean_ratio(shell_all, sigma_tab)
    out["shell_size_all"] = len(shell_all)
    out["shell_mean_baseline"] = shell_mean_baseline
    print(f"[xref] shell baseline mean sigma_inf/log2 n = {shell_mean_baseline:.4f}",
          flush=True)

    out["per_y"] = {}
    for y in y_values:
        smooth = smooth_filter(shell_all, pmax, y)
        smooth_vals = ratio_vals(smooth, sigma_tab)
        smooth_mean = sum(smooth_vals) / len(smooth_vals)
        n_smooth = len(smooth)
        smooth_set = set(smooth)
        nonsmooth_pool = [n for n in shell_all if n not in smooth_set]

        # ---- C1: v_2-only matched (sanity reproduction) ----
        hist_smooth_v2 = hist_v2(smooth, v2)
        matched_v2, achieved_v2, pool_hist_v2 = matched_subsample_v2(
            hist_smooth_v2, nonsmooth_pool, v2, rng)
        matched_v2_vals = ratio_vals(matched_v2, sigma_tab)
        matched_v2_mean = sum(matched_v2_vals) / len(matched_v2_vals)
        c1_drop = 1.0 - smooth_mean / matched_v2_mean

        # ---- Joint matching ----
        hist_smooth_joint = hist_joint(smooth, v2)
        matched_joint, coverage_joint = matched_subsample_joint(
            hist_smooth_joint, nonsmooth_pool, v2, rng)
        matched_joint_vals = ratio_vals(matched_joint, sigma_tab)
        if matched_joint_vals:
            matched_joint_mean = sum(matched_joint_vals) / len(matched_joint_vals)
            joint_drop = 1.0 - smooth_mean / matched_joint_mean
        else:
            matched_joint_mean = float("nan")
            joint_drop = float("nan")

        # Sample-deficient cells (target>achieved) — important to report.
        deficit_cells = {
            f"{k[0]}|{k[1]}": v
            for k, v in coverage_joint.items()
            if v["target"] > v["achieved"]
        }

        # ---- Bootstrap CI on joint-matched gap ----
        ci = bootstrap_gap_ci(smooth_vals, matched_joint_vals,
                              n_boot=n_boot, seed=seed + y, alpha=0.05) \
            if matched_joint_vals else {}

        # ---- Also bootstrap for C1 baseline (for completeness) ----
        ci_c1 = bootstrap_gap_ci(smooth_vals, matched_v2_vals,
                                  n_boot=n_boot, seed=seed + y + 1, alpha=0.05) \
            if matched_v2_vals else {}

        print(f"\n[y={y}] n_smooth={n_smooth}  smooth_mean={smooth_mean:.4f}",
              flush=True)
        print(f"      [C1 v_2-only]  matched_mean={matched_v2_mean:.4f}  "
              f"drop={c1_drop*100:.2f}%  "
              f"CI95=[{ci_c1.get('gap_ci_lo_pct',float('nan')):.2f}, "
              f"{ci_c1.get('gap_ci_hi_pct',float('nan')):.2f}]%",
              flush=True)
        print(f"      [JOINT      ]  matched_mean={matched_joint_mean:.4f}  "
              f"drop={joint_drop*100:.2f}%  "
              f"CI95=[{ci.get('gap_ci_lo_pct',float('nan')):.2f}, "
              f"{ci.get('gap_ci_hi_pct',float('nan')):.2f}]%",
              flush=True)
        print(f"      joint hist cells (smooth): {len(hist_smooth_joint)}; "
              f"deficient cells: {len(deficit_cells)}", flush=True)
        if deficit_cells:
            print(f"      deficits: {deficit_cells}", flush=True)

        out["per_y"][str(y)] = {
            "y": y,
            "n_smooth": n_smooth,
            "smooth_mean": smooth_mean,
            "shell_mean_baseline": shell_mean_baseline,
            "raw_drop_pct": (1 - smooth_mean / shell_mean_baseline) * 100,

            "c1_v2_only": {
                "n_matched": len(matched_v2),
                "matched_mean": matched_v2_mean,
                "drop_pct": c1_drop * 100,
                "bootstrap_ci": ci_c1,
                "achieved_hist": achieved_v2,
                "pool_hist": pool_hist_v2,
                "target_hist": hist_smooth_v2,
            },
            "joint": {
                "n_matched": len(matched_joint),
                "matched_mean": matched_joint_mean,
                "drop_pct": joint_drop * 100,
                "bootstrap_ci": ci,
                "smooth_hist": {f"{k[0]}|{k[1]}": v for k, v in hist_smooth_joint.items()},
                "coverage": {f"{k[0]}|{k[1]}": v for k, v in coverage_joint.items()},
                "deficient_cells": deficit_cells,
            },
        }

    return out


def main() -> int:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--N", type=int, default=10**6)
    p.add_argument("--shell_lo", type=int, default=16)
    p.add_argument("--shell_hi", type=int, default=20)
    p.add_argument("--y_values", type=str, default="10,20,50,100")
    p.add_argument("--n_boot", type=int, default=1000)
    p.add_argument("--out", type=str, default="sieve_q3_joint_control_probe.json")
    args = p.parse_args()

    y_values = tuple(int(s) for s in args.y_values.split(","))
    t0 = time.time()
    out = run_probe(N=args.N, shell=(args.shell_lo, args.shell_hi),
                    y_values=y_values, n_boot=args.n_boot)
    out["wall_time_seconds"] = time.time() - t0

    # Make tuples JSON-serializable.
    out_path = os.path.join(DATA_DIR, args.out)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\n[done] wrote {out_path}  wall = {out['wall_time_seconds']:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
