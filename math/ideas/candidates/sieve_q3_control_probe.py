"""
Q3 smoothness signal — 2-adic-valuation control probe.

Background. The alt-angle sieve_analytic_probe found:
   On y=10 smooth integers in dyadic shell log2 n in [16, 20),
   mean sigma_inf / log2 n drops ~24% vs. the unrestricted population.
The signal survived dyadic shell stratification but the obvious confounder
   v_2(n) := 2-adic valuation
was NOT controlled. y=10 smooth means primes in {2, 3, 5, 7}; small smooth
integers are heavily biased to large v_2(n), and each factor of 2 is a "free
halving" step in the Collatz orbit — trivially shorter sigma_inf.

This probe runs three independent v_2 controls:
  (A) Reproduce the 24% headline drop in shell [16, 20).
  (B) Tabulate v_2(n) distribution on smooth vs. all.
  (C1) Matched-subsample control: subsample non-smooth integers so their
       v_2 histogram matches the smooth histogram (bucketed {0,1,2,3,4,5+}).
       Compute mean sigma_inf / log2 n on matched subsample.
  (C2) Residualized observable: sigma_inf_residual(n) := sigma_inf(n) - v_2(n).
       Re-run the smooth-vs-all comparison on the residualized observable
       and on (residualized) / log2(n).
  (D) Scan more y values: y in {10, 20, 50, 100}. If smoothness signal is
      truly arithmetic, effect should scale structurally with y. If it's
      v_2-confounded, larger y dilutes the v_2 bias and the gap should close.

Author: Alex Ye.
"""

from __future__ import annotations

import json
import math
import os
import random
import sys
import time
from typing import Dict, List, Tuple

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)


# -----------------------------------------------------------------------------
# Core: Collatz total stopping time table (accelerated map, matching sieve_analytic_probe.py)
# -----------------------------------------------------------------------------

def build_sigma_table(N: int) -> List[int]:
    """Tabulate sigma_inf(n) for n in [1, N] via iterative memoization.

    Accelerated Collatz: even n -> n/2; odd n -> (3n+1)/2. Stop when n=1.
    """
    t = [0] * (N + 1)
    t[1] = 0
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
    """P^+(n) for n in [1, N]."""
    pmax = [0] * (N + 1)
    for p in range(2, N + 1):
        if pmax[p] == 0:  # p is prime
            for k in range(p, N + 1, p):
                pmax[k] = p
    return pmax


def v2_table(N: int) -> List[int]:
    """v_2(n) for n in [0, N]."""
    out = [0] * (N + 1)
    for n in range(1, N + 1):
        m = n
        c = 0
        while m & 1 == 0:
            m >>= 1
            c += 1
        out[n] = c
    return out


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def v2_bucket(v: int) -> str:
    """Buckets: '0','1','2','3','4','5+'."""
    if v >= 5:
        return "5+"
    return str(v)


def hist_v2(idx: List[int], v2: List[int]) -> Dict[str, int]:
    h = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5+": 0}
    for n in idx:
        h[v2_bucket(v2[n])] += 1
    return h


def mean_ratio(idx: List[int], sigma_tab: List[int]) -> Tuple[float, int]:
    """Mean of sigma_inf(n) / log2(n) over idx."""
    s = 0.0
    c = 0
    for n in idx:
        if n >= 2:
            s += sigma_tab[n] / math.log2(n)
            c += 1
    return (s / c if c > 0 else float("nan")), c


def mean_sigma(idx: List[int], sigma_tab: List[int]) -> Tuple[float, int]:
    s = 0
    c = 0
    for n in idx:
        s += sigma_tab[n]
        c += 1
    return (s / c if c > 0 else float("nan")), c


def mean_residualized_ratio(idx: List[int], sigma_tab: List[int],
                            v2: List[int]) -> Tuple[float, int]:
    """Mean of (sigma_inf(n) - v_2(n)) / log2(n)."""
    s = 0.0
    c = 0
    for n in idx:
        if n >= 2:
            s += (sigma_tab[n] - v2[n]) / math.log2(n)
            c += 1
    return (s / c if c > 0 else float("nan")), c


def mean_residualized_sigma(idx: List[int], sigma_tab: List[int],
                            v2: List[int]) -> Tuple[float, int]:
    s = 0.0
    c = 0
    for n in idx:
        s += sigma_tab[n] - v2[n]
        c += 1
    return (s / c if c > 0 else float("nan")), c


# -----------------------------------------------------------------------------
# Shell selection & smooth selection
# -----------------------------------------------------------------------------

def shell_indices(N: int, L_lo: int, L_hi: int) -> List[int]:
    """n in [2, N] with log2(n) in [L_lo, L_hi). Equivalently 2^L_lo <= n < 2^L_hi."""
    lo = max(2, 1 << L_lo)
    hi = min(N + 1, 1 << L_hi)
    return list(range(lo, hi))


def smooth_filter(idx: List[int], pmax: List[int], y: int) -> List[int]:
    return [n for n in idx if pmax[n] <= y]


# -----------------------------------------------------------------------------
# Matched-subsample (v_2-histogram match)
# -----------------------------------------------------------------------------

def matched_subsample(target_hist: Dict[str, int],
                       pool_idx: List[int],
                       v2: List[int],
                       rng: random.Random) -> Tuple[List[int], Dict[str, int], Dict[str, int]]:
    """Draw from pool_idx a subsample whose v_2 bucket counts equal target_hist
    (each bucket capped at the pool's count). Returns (sample, achieved_hist,
    pool_hist) for transparency.
    """
    # Partition pool by bucket.
    buckets: Dict[str, List[int]] = {"0": [], "1": [], "2": [], "3": [], "4": [], "5+": []}
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


# -----------------------------------------------------------------------------
# Main probe
# -----------------------------------------------------------------------------

def run_control(N: int = 10**6,
                shell: Tuple[int, int] = (16, 20),
                y_values: Tuple[int, ...] = (10, 20, 50, 100),
                seed: int = 20260608) -> Dict:
    rng = random.Random(seed)
    out: Dict = {
        "N": N,
        "shell": list(shell),
        "y_values": list(y_values),
        "seed": seed,
    }

    print(f"[setup] N = {N}", flush=True)
    print(f"[setup] shell = log2 n in [{shell[0]}, {shell[1]}) "
          f"-> n in [{1 << shell[0]}, {1 << shell[1]})", flush=True)

    t0 = time.time()
    print("[1/3] sigma_inf table ...", flush=True)
    sigma_tab = build_sigma_table(N)
    print(f"      done in {time.time() - t0:.2f}s", flush=True)

    t0 = time.time()
    print("[2/3] largest-prime-factor sieve ...", flush=True)
    pmax = largest_prime_factor_table(N)
    print(f"      done in {time.time() - t0:.2f}s", flush=True)

    t0 = time.time()
    print("[3/3] v_2 table ...", flush=True)
    v2 = v2_table(N)
    print(f"      done in {time.time() - t0:.2f}s", flush=True)

    # ---- Task (1): reproduce headline drop ----
    L_lo, L_hi = shell
    shell_all = shell_indices(N, L_lo, L_hi)
    print(f"[shell] |shell_all| = {len(shell_all)}", flush=True)

    out["shell_size_all"] = len(shell_all)

    # Also compute over the WHOLE range [2, N] for cross-check vs the doc.
    full_idx = list(range(2, N + 1))
    full_mean, _ = mean_ratio(full_idx, sigma_tab)
    out["full_range_mean_sigma_over_log2n"] = full_mean
    print(f"[xref] full-range mean sigma_inf/log2 n = {full_mean:.4f}", flush=True)

    shell_mean_all, _ = mean_ratio(shell_all, sigma_tab)
    out["shell_mean_all"] = shell_mean_all

    out["per_y"] = {}
    for y in y_values:
        smooth = smooth_filter(shell_all, pmax, y)
        smooth_mean, n_smooth = mean_ratio(smooth, sigma_tab)
        ratio = smooth_mean / shell_mean_all if shell_mean_all else float("nan")
        drop = 1.0 - ratio
        print(f"[Q3] y={y:>4}  count_smooth = {n_smooth:>6}  "
              f"mean = {smooth_mean:.4f}  vs baseline {shell_mean_all:.4f}  "
              f"ratio = {ratio:.3f}  drop = {drop*100:.1f}%", flush=True)

        # v_2 histograms
        hist_smooth = hist_v2(smooth, v2)
        hist_shell = hist_v2(shell_all, v2)

        # Non-smooth pool = shell_all minus smooth
        smooth_set = set(smooth)
        nonsmooth_pool = [n for n in shell_all if n not in smooth_set]
        nonsmooth_mean, n_nonsmooth = mean_ratio(nonsmooth_pool, sigma_tab)
        hist_nonsmooth = hist_v2(nonsmooth_pool, v2)

        # ---- (C1) Matched-subsample control ----
        matched, achieved, pool_hist = matched_subsample(
            hist_smooth, nonsmooth_pool, v2, rng)
        matched_mean, n_matched = mean_ratio(matched, sigma_tab)
        matched_ratio = (smooth_mean / matched_mean) if matched_mean else float("nan")
        matched_drop = 1.0 - matched_ratio

        # Coverage diagnostic: did achieved match target?
        coverage = {bk: {"target": hist_smooth[bk],
                          "achieved": achieved[bk],
                          "pool_supply": pool_hist[bk]}
                    for bk in hist_smooth}

        # ---- (C2) Residualized observable: sigma_inf - v_2 ----
        # On smooth:
        smooth_resmean_ratio, _ = mean_residualized_ratio(smooth, sigma_tab, v2)
        # On shell baseline:
        shell_resmean_ratio, _ = mean_residualized_ratio(shell_all, sigma_tab, v2)
        # Also on non-smooth pool:
        nonsmooth_resmean_ratio, _ = mean_residualized_ratio(nonsmooth_pool, sigma_tab, v2)
        # Ratio after residualization:
        res_ratio = (smooth_resmean_ratio / shell_resmean_ratio
                     if shell_resmean_ratio else float("nan"))
        res_drop = 1.0 - res_ratio

        # Mean v_2 per group (sanity):
        def mean_v2(idx):
            return sum(v2[n] for n in idx) / max(1, len(idx))
        mean_v2_smooth = mean_v2(smooth)
        mean_v2_shell = mean_v2(shell_all)
        mean_v2_nonsmooth = mean_v2(nonsmooth_pool)
        mean_v2_matched = mean_v2(matched) if matched else float("nan")

        out["per_y"][str(y)] = {
            "y": y,
            "n_smooth": n_smooth,
            "smooth_mean": smooth_mean,
            "shell_mean_baseline": shell_mean_all,
            "drop_pct": drop * 100,
            "nonsmooth_mean": nonsmooth_mean,
            "n_nonsmooth": n_nonsmooth,

            "v2_hist_smooth": hist_smooth,
            "v2_hist_shell": hist_shell,
            "v2_hist_nonsmooth": hist_nonsmooth,

            "mean_v2_smooth": mean_v2_smooth,
            "mean_v2_shell": mean_v2_shell,
            "mean_v2_nonsmooth": mean_v2_nonsmooth,
            "mean_v2_matched": mean_v2_matched,

            "matched_subsample": {
                "n_matched": n_matched,
                "matched_mean": matched_mean,
                "smooth_over_matched_ratio": matched_ratio,
                "smooth_vs_matched_drop_pct": matched_drop * 100,
                "coverage": coverage,
            },
            "residualized": {
                "smooth_mean_residual_over_log2n": smooth_resmean_ratio,
                "shell_mean_residual_over_log2n": shell_resmean_ratio,
                "nonsmooth_mean_residual_over_log2n": nonsmooth_resmean_ratio,
                "smooth_over_shell_ratio_residual": res_ratio,
                "drop_pct_residual": res_drop * 100,
            },
        }

        print(f"      v_2 hist smooth  : {hist_smooth}  mean_v2={mean_v2_smooth:.2f}", flush=True)
        print(f"      v_2 hist shell   : {hist_shell}  mean_v2={mean_v2_shell:.2f}", flush=True)
        print(f"      [C1 matched]    n_matched = {n_matched}  matched_mean = {matched_mean:.4f}  "
              f"drop_smooth_vs_matched = {matched_drop*100:.1f}%", flush=True)
        print(f"      [C2 residual]   smooth = {smooth_resmean_ratio:.4f}  "
              f"shell = {shell_resmean_ratio:.4f}  drop = {res_drop*100:.1f}%", flush=True)

    return out


def main() -> int:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--N", type=int, default=10**6)
    p.add_argument("--shell_lo", type=int, default=16)
    p.add_argument("--shell_hi", type=int, default=20)
    p.add_argument("--y_values", type=str, default="10,20,50,100")
    args = p.parse_args()

    y_values = tuple(int(s) for s in args.y_values.split(","))
    t0 = time.time()
    out = run_control(N=args.N, shell=(args.shell_lo, args.shell_hi),
                      y_values=y_values)
    out["wall_time_seconds"] = time.time() - t0

    out_path = os.path.join(DATA_DIR, "sieve_q3_control_probe.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\n[done] wrote {out_path}  wall = {out['wall_time_seconds']:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
