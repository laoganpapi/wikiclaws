"""
Follow-up probe for sieve_analytic_probe.py:

  F1. Q3 stratification: is the smoothness signal an artifact of smooth
      integers being smaller? Compute mean(sigma_inf / log2 n) restricted
      to (y-smooth, log2 n in [L, L+1)) for L = 4, 8, 12, 16.

  F2. Q4 centering: replace P(n) with P_tilde(n) = P(n) - mu(log2 n) and
      re-run exponential sums to test whether the 0.83 exponent survives.

Author: Alex Ye.
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from math import gcd
from typing import Dict, List

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, "data")

sys.path.insert(0, THIS_DIR)
from sieve_analytic_probe import (
    build_sigma_table,
    largest_prime_factor_table,
)


def f1_stratified_smoothness(N: int = 1_000_000,
                              y_values: List[int] = [10, 50, 100, 500, 1000],
                              shells: List[float] = [4, 8, 12, 16, 20]) -> Dict:
    print(f"[F1] N = {N}, building tables ...", flush=True)
    t0 = time.time()
    pmax = largest_prime_factor_table(N)
    tab = build_sigma_table(N)
    print(f"[F1]   tables done in {time.time() - t0:.2f}s", flush=True)

    # Define dyadic shells: shell k = [shells[k], shells[k+1]) on log2 n.
    nshells = len(shells) - 1
    # All-n baseline per shell
    base_sum = [0.0] * nshells
    base_count = [0] * nshells
    for n in range(2, N + 1):
        ln = math.log2(n)
        for k in range(nshells):
            if shells[k] <= ln < shells[k+1]:
                base_sum[k] += tab[n] / ln
                base_count[k] += 1
                break
    base_mean = [
        (base_sum[k] / base_count[k]) if base_count[k] > 0 else None
        for k in range(nshells)
    ]

    # By y, by shell
    by_y = {}
    for y in y_values:
        sums = [0.0] * nshells
        counts = [0] * nshells
        for n in range(2, N + 1):
            if pmax[n] > y:
                continue
            ln = math.log2(n)
            for k in range(nshells):
                if shells[k] <= ln < shells[k+1]:
                    sums[k] += tab[n] / ln
                    counts[k] += 1
                    break
        by_y[str(y)] = [
            {
                "shell": [shells[k], shells[k+1]],
                "count": counts[k],
                "mean": (sums[k] / counts[k]) if counts[k] > 0 else None,
                "baseline_mean": base_mean[k],
                "ratio_smooth_over_baseline": (
                    (sums[k] / counts[k]) / base_mean[k]
                    if counts[k] > 0 and base_mean[k] is not None
                    else None
                ),
            }
            for k in range(nshells)
        ]
    return {
        "N": N,
        "shells": shells,
        "y_values": y_values,
        "baseline_per_shell": base_mean,
        "baseline_counts": base_count,
        "by_y_by_shell": by_y,
    }


def f2_centered_circle(N: int = 1_000_000, q_max: int = 30,
                       shells: List[float] = [4, 8, 12, 16, 20]) -> Dict:
    try:
        import numpy as np
    except ImportError:
        return {"error": "numpy required"}

    print(f"[F2] N = {N}, building parity table ...", flush=True)
    t0 = time.time()
    P_tab = [0] * (N + 1)
    for n in range(2, N + 1):
        m = n
        p = 0
        while m != 1:
            if m & 1:
                p += 1
                m = (3 * m + 1) >> 1
            else:
                m >>= 1
        P_tab[n] = p
    print(f"[F2]   parity table done in {time.time() - t0:.2f}s", flush=True)

    # Compute mean and std of P(n) per shell
    nshells = len(shells) - 1
    shell_sum = [0.0] * nshells
    shell_sumsq = [0.0] * nshells
    shell_count = [0] * nshells
    shell_idx = [-1] * (N + 1)
    for n in range(2, N + 1):
        ln = math.log2(n)
        for k in range(nshells):
            if shells[k] <= ln < shells[k+1]:
                shell_sum[k] += P_tab[n]
                shell_sumsq[k] += P_tab[n] * P_tab[n]
                shell_count[k] += 1
                shell_idx[n] = k
                break
    shell_mean = [
        (shell_sum[k] / shell_count[k]) if shell_count[k] > 0 else 0.0
        for k in range(nshells)
    ]
    shell_std = [
        math.sqrt(max(shell_sumsq[k] / shell_count[k] - shell_mean[k] ** 2, 1e-12))
        if shell_count[k] > 0 else 1.0
        for k in range(nshells)
    ]
    print(f"[F2]   shell means: {[f'{x:.2f}' for x in shell_mean]}")
    print(f"[F2]   shell stds:  {[f'{x:.2f}' for x in shell_std]}")

    # Centered & normalized parity: P_tilde(n) = (P(n) - mu_k) / sigma_k for n in shell k
    P_arr = np.zeros(N + 1, dtype=np.float64)
    for n in range(2, N + 1):
        k = shell_idx[n]
        if k >= 0:
            P_arr[n] = (P_tab[n] - shell_mean[k]) / shell_std[k]
        # else: n outside all shells, leave as 0 (these are excluded below)

    # Mask: only n inside a shell
    mask = np.array([shell_idx[n] >= 0 for n in range(N + 1)], dtype=bool)
    P_centered = P_arr[mask]
    N_eff = int(P_centered.shape[0])
    print(f"[F2]   {N_eff} integers in shells", flush=True)

    # Farey fractions, q >= 2
    fractions = []
    for q in range(2, q_max + 1):
        for p in range(1, q):
            if gcd(p, q) == 1:
                fractions.append((p, q))

    X_list = [10**k for k in range(2, int(math.log10(N)) + 1)]
    if X_list[-1] != N:
        X_list.append(N)

    # Cumulative restriction: we need n <= X among masked integers.
    # The mask preserves order, so we re-index by position in masked array.
    # For each X compute prefix count: how many masked n <= X
    # Build cumulative count of mask
    mask_int = mask.astype(np.int64)
    prefix = np.cumsum(mask_int)  # prefix[X] = #(masked n in [0, X])

    results = []
    for X in X_list:
        n_in = int(prefix[X])
        if n_in < 10:
            continue
        slice_ = P_centered[: n_in]
        best_abs = 0.0
        best_frac = None
        for (p, q) in fractions:
            alpha = p / q
            theta = (2 * math.pi * alpha) * slice_
            re = float(np.cos(theta).sum())
            im = float(np.sin(theta).sum())
            mag = math.sqrt(re * re + im * im)
            if mag > best_abs:
                best_abs = mag
                best_frac = (p, q)
        if best_abs > 1 and n_in > 1:
            exp_est = math.log(best_abs) / math.log(n_in)
        else:
            exp_est = float("nan")
        results.append({
            "X": X,
            "n_in_shells_<=X": n_in,
            "best_abs_over_n": best_abs / n_in,
            "best_abs": best_abs,
            "best_frac": best_frac,
            "exponent_log_best_over_log_n": exp_est,
        })

    return {
        "N": N, "q_max": q_max, "n_fractions": len(fractions),
        "shells": shells,
        "shell_mean": shell_mean, "shell_std": shell_std,
        "shell_count": shell_count,
        "results": results,
    }


def main() -> int:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--N", type=int, default=1_000_000)
    p.add_argument("--q_max", type=int, default=30)
    p.add_argument("--skip", default="")
    args = p.parse_args()
    skip = set(s.strip() for s in args.skip.split(",") if s.strip())

    out = {"N": args.N, "q_max": args.q_max}
    t = time.time()

    if "F1" not in skip:
        print("=" * 60)
        print("[F1] Q3 stratified smoothness")
        print("=" * 60)
        out["F1"] = f1_stratified_smoothness(args.N)
        for y, lst in out["F1"]["by_y_by_shell"].items():
            print(f"  y = {y}:")
            for entry in lst:
                if entry["mean"] is None:
                    continue
                shell = entry["shell"]
                print(f"    log2 n in [{shell[0]}, {shell[1]}):  "
                      f"count = {entry['count']:>7}  "
                      f"smooth mean = {entry['mean']:.4f}  "
                      f"baseline = {entry['baseline_mean']:.4f}  "
                      f"ratio = {entry['ratio_smooth_over_baseline']:.4f}")

    if "F2" not in skip:
        print("=" * 60)
        print("[F2] Q4 centered/normalized circle method")
        print("=" * 60)
        out["F2"] = f2_centered_circle(args.N, args.q_max)
        for r in out["F2"]["results"]:
            print(f"     X = {r['X']:>8}  n_in = {r['n_in_shells_<=X']:>8}  "
                  f"max |S|/n = {r['best_abs_over_n']:.6f}  "
                  f"best frac = {r['best_frac']}  "
                  f"exponent = {r['exponent_log_best_over_log_n']:.4f}")

    out["wall_time_seconds"] = time.time() - t
    out_path = os.path.join(DATA_DIR, "sieve_analytic_followup.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\n[done] wrote {out_path}  (wall = {out['wall_time_seconds']:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
