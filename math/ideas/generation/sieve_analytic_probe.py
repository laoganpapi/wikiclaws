"""
Sieve / analytic-NT probe on integer Collatz orbits.

Four sub-probes (cf. sieve_analytic.md):

  Q1. Multiplicativity defect Delta(a, b) = sigma_inf(ab) - sigma_inf(a) - sigma_inf(b)
      on coprime pairs.

  Q2. Partial Dirichlet series F_X(s) = sum_{n <= X} sigma_inf(n) * n^{-s}
      and its ratio to zeta_X(s).

  Q3. Smooth-Collatz density: mean(sigma_inf(n) / log2(n)) restricted to
      y-smooth integers, vs. unrestricted mean.

  Q4. Hardy-Littlewood exponential sum S_alpha(X) = sum_{n <= X} e(alpha * P(n))
      where P(n) is the odd-parity count of the Syracuse word of n.

Author: Alex Ye.
"""

from __future__ import annotations

import json
import math
import os
import random
import sys
import time
from math import gcd
from typing import Dict, List, Tuple

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)


# -----------------------------------------------------------------------------
# Core Collatz primitives
# -----------------------------------------------------------------------------

def sigma_inf(n: int) -> int:
    """Total stopping time of n under accelerated map."""
    if n < 1:
        raise ValueError("n >= 1 required")
    c = 0
    while n != 1:
        if n & 1:
            n = (3 * n + 1) >> 1
        else:
            n >>= 1
        c += 1
    return c


def parity_word_count(n: int) -> int:
    """Total odd-parity count P(n) of the Syracuse word."""
    if n < 1:
        raise ValueError
    p = 0
    while n != 1:
        if n & 1:
            p += 1
            n = (3 * n + 1) >> 1
        else:
            n >>= 1
    return p


def build_sigma_table(N: int) -> List[int]:
    """Tabulate sigma_inf(n) for n in [1, N] via iterative memoization."""
    t = [0] * (N + 1)
    t[1] = 0
    for n in range(2, N + 1):
        # Walk until we hit something already in table or 1.
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
        # Assign in reverse
        k = len(path)
        for j, mm in enumerate(path):
            if mm <= N and t[mm] == 0:
                t[mm] = base + (k - j)
    return t


def build_parity_table(N: int) -> List[int]:
    """Tabulate P(n) for n in [1, N]."""
    t = [-1] * (N + 1)
    t[1] = 0
    for n in range(2, N + 1):
        path = []
        m = n
        while m > N or t[m] < 0:
            path.append(m)
            if m & 1:
                path[-1] = (m, 1)  # mark odd step
                m = (3 * m + 1) >> 1
            else:
                path[-1] = (m, 0)
                m >>= 1
            if m == 1:
                break
        base = 0 if m == 1 else t[m]
        # Sum parities from the END of path back to the front
        acc = base
        for j in range(len(path) - 1, -1, -1):
            mm, parity_bit = path[j]
            acc = acc + parity_bit
            if mm <= N and t[mm] < 0:
                t[mm] = acc
    return t


# -----------------------------------------------------------------------------
# Q1: Multiplicativity defect
# -----------------------------------------------------------------------------

def probe_multiplicativity(num_samples: int = 5000,
                            a_max: int = 10_000,
                            seed: int = 20260608) -> Dict:
    rng = random.Random(seed)
    deltas: List[int] = []
    log_min: List[float] = []
    sign_pos = 0
    sign_zero = 0
    sign_neg = 0
    attempts = 0
    while len(deltas) < num_samples and attempts < num_samples * 20:
        attempts += 1
        a = rng.randint(2, a_max)
        b = rng.randint(2, a_max)
        if gcd(a, b) != 1:
            continue
        try:
            sa = sigma_inf(a)
            sb = sigma_inf(b)
            sab = sigma_inf(a * b)
        except Exception:
            continue
        d = sab - sa - sb
        deltas.append(d)
        log_min.append(math.log(min(a, b)))
        if d > 0:
            sign_pos += 1
        elif d == 0:
            sign_zero += 1
        else:
            sign_neg += 1

    n = len(deltas)
    mean = sum(deltas) / n
    sorted_d = sorted(deltas)
    median = sorted_d[n // 2]
    var = sum((d - mean) ** 2 for d in deltas) / n
    std = math.sqrt(var)

    # Regression delta = a + b * log_min
    sx = sum(log_min)
    sy = sum(deltas)
    sxx = sum(x * x for x in log_min)
    sxy = sum(x * y for x, y in zip(log_min, deltas))
    denom = n * sxx - sx * sx
    slope = (n * sxy - sx * sy) / denom if denom != 0 else float("nan")
    intercept = (sy - slope * sx) / n if denom != 0 else float("nan")
    ybar = sy / n
    ss_tot = sum((d - ybar) ** 2 for d in deltas)
    ss_res = sum((d - (intercept + slope * x)) ** 2 for d, x in zip(deltas, log_min))
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")

    return {
        "n_samples": n,
        "attempts": attempts,
        "mean_delta": mean,
        "median_delta": median,
        "std_delta": std,
        "min_delta": min(deltas),
        "max_delta": max(deltas),
        "sign_pos": sign_pos,
        "sign_zero": sign_zero,
        "sign_neg": sign_neg,
        "neg_fraction": sign_neg / n,
        "regression_slope_log_min": slope,
        "regression_intercept": intercept,
        "regression_R2": r_squared,
        "a_max": a_max,
    }


# -----------------------------------------------------------------------------
# Q2: Partial Dirichlet series
# -----------------------------------------------------------------------------

def probe_dirichlet(N: int, s_values: List[float]) -> Dict:
    """Build sigma_inf table once and compute partial sums at multiple s, X."""
    print(f"[Q2] building sigma_inf table for N = {N} ...", flush=True)
    t0 = time.time()
    tab = build_sigma_table(N)
    t1 = time.time()
    print(f"[Q2]   done in {t1 - t0:.2f}s", flush=True)

    X_list = [10**k for k in range(2, int(math.log10(N)) + 1)]
    if not X_list or X_list[-1] != N:
        X_list.append(N)
    results = {}
    for s in s_values:
        per_s = []
        # Compute cumulative sums:
        F_sum = 0.0
        Z_sum = 0.0
        next_X_idx = 0
        for n in range(2, N + 1):
            ns = n ** (-s)
            F_sum += tab[n] * ns
            Z_sum += ns
            if next_X_idx < len(X_list) and n == X_list[next_X_idx]:
                per_s.append({
                    "X": n,
                    "F_X": F_sum,
                    "Z_X": Z_sum,
                    "ratio_F_over_Z": F_sum / Z_sum if Z_sum > 0 else float("nan"),
                })
                next_X_idx += 1
        results[str(s)] = per_s
    return {"N": N, "X_list": X_list, "by_s": results}


# -----------------------------------------------------------------------------
# Q3: Smooth-Collatz density
# -----------------------------------------------------------------------------

def largest_prime_factor_table(N: int) -> List[int]:
    """Compute P^+(n) for n in [1, N] via a modified sieve."""
    pmax = [0] * (N + 1)
    for p in range(2, N + 1):
        if pmax[p] == 0:  # p prime
            for k in range(p, N + 1, p):
                pmax[k] = p
    return pmax


def probe_smoothness(N: int, y_values: List[int]) -> Dict:
    print(f"[Q3] sieving P^+ for N = {N} ...", flush=True)
    t0 = time.time()
    pmax = largest_prime_factor_table(N)
    print(f"[Q3]   sieve done in {time.time() - t0:.2f}s", flush=True)

    print(f"[Q3] building sigma_inf table ...", flush=True)
    t0 = time.time()
    tab = build_sigma_table(N)
    print(f"[Q3]   sigma table done in {time.time() - t0:.2f}s", flush=True)

    # Unrestricted baseline
    sum_ratio = 0.0
    count = 0
    for n in range(2, N + 1):
        sum_ratio += tab[n] / math.log2(n)
        count += 1
    mean_unrestricted = sum_ratio / count

    by_y = {}
    for y in y_values:
        s = 0.0
        c = 0
        sigma_sum = 0
        for n in range(2, N + 1):
            if pmax[n] <= y:
                s += tab[n] / math.log2(n)
                c += 1
                sigma_sum += tab[n]
        by_y[str(y)] = {
            "y": y,
            "count_smooth": c,
            "mean_sigma_over_log2n": s / c if c > 0 else None,
            "mean_sigma_inf": sigma_sum / c if c > 0 else None,
        }
    return {
        "N": N,
        "mean_sigma_over_log2n_unrestricted": mean_unrestricted,
        "by_y": by_y,
    }


# -----------------------------------------------------------------------------
# Q4: Circle method on parity-count
# -----------------------------------------------------------------------------

def probe_circle_method(N: int, q_max: int = 30) -> Dict:
    try:
        import numpy as np
    except ImportError:
        np = None
    print(f"[Q4] building parity-count table for N = {N} ...", flush=True)
    t0 = time.time()
    # Build P(n) for n in [2, N] via direct iteration. For each n, walk the
    # full Syracuse orbit until 1, accumulating odd-step count. This is O(sigma_inf)
    # per n; for N = 10^6 this is roughly 10^6 * 60 = 6*10^7 ops, fast enough.
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
    print(f"[Q4]   parity table done in {time.time() - t0:.2f}s", flush=True)

    X_list = [10**k for k in range(2, int(math.log10(N)) + 1)]
    if not X_list or X_list[-1] != N:
        X_list.append(N)
    # Enumerate non-trivial Farey fractions p/q with q <= q_max, 1 <= p < q,
    # gcd(p,q) = 1. We EXCLUDE alpha = 0 (trivial; would give |S| = X-1 always).
    fractions = []
    for q in range(2, q_max + 1):
        for p in range(1, q):
            if gcd(p, q) == 1:
                fractions.append((p, q))
    print(f"[Q4]   {len(fractions)} Farey fractions with q <= {q_max}", flush=True)

    results = []
    if np is not None:
        P_arr = np.array(P_tab[2:N+1], dtype=np.int64)
        for X in X_list:
            P_slice = P_arr[: X - 1]  # n = 2..X
            best_abs = 0.0
            best_frac = None
            for (p, q) in fractions:
                alpha = p / q
                theta = (2 * math.pi * alpha) * P_slice
                re = float(np.cos(theta).sum())
                im = float(np.sin(theta).sum())
                mag = math.sqrt(re * re + im * im)
                if mag > best_abs:
                    best_abs = mag
                    best_frac = (p, q)
            if best_abs > 0 and X > 1:
                exp_est = math.log(best_abs) / math.log(X)
            else:
                exp_est = float("nan")
            results.append({
                "X": X,
                "best_abs_over_X": best_abs / X,
                "best_abs": best_abs,
                "best_frac": best_frac,
                "exponent_log_best_over_log_X": exp_est,
            })
    else:
        for X in X_list:
            best_abs = 0.0
            best_frac = None
            for (p, q) in fractions:
                alpha = p / q
                re = 0.0
                im = 0.0
                for n in range(2, X + 1):
                    theta = 2 * math.pi * alpha * P_tab[n]
                    re += math.cos(theta)
                    im += math.sin(theta)
                mag = math.sqrt(re * re + im * im)
                if mag > best_abs:
                    best_abs = mag
                    best_frac = (p, q)
            if best_abs > 0 and X > 1:
                exp_est = math.log(best_abs) / math.log(X)
            else:
                exp_est = float("nan")
            results.append({
                "X": X,
                "best_abs_over_X": best_abs / X,
                "best_abs": best_abs,
                "best_frac": best_frac,
                "exponent_log_best_over_log_X": exp_est,
            })
    return {"N": N, "q_max": q_max, "n_fractions": len(fractions),
            "results": results}


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> int:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--N", type=int, default=10**6)
    p.add_argument("--Q1_samples", type=int, default=5000)
    p.add_argument("--q_max", type=int, default=30)
    p.add_argument("--skip", default="", help="Comma-separated subset of Q1,Q2,Q3,Q4 to skip.")
    args = p.parse_args()

    skip = set(s.strip() for s in args.skip.split(",") if s.strip())

    out = {
        "N": args.N,
        "Q1_samples": args.Q1_samples,
        "q_max": args.q_max,
    }
    t_total = time.time()

    if "Q1" not in skip:
        print("=" * 60)
        print("[Q1] Multiplicativity defect")
        print("=" * 60)
        t0 = time.time()
        out["Q1"] = probe_multiplicativity(num_samples=args.Q1_samples)
        print(f"[Q1] done in {time.time() - t0:.2f}s")
        print(f"     mean Delta = {out['Q1']['mean_delta']:.2f}")
        print(f"     median Delta = {out['Q1']['median_delta']}")
        print(f"     neg fraction = {out['Q1']['neg_fraction']:.4f}")
        print(f"     regression slope on log(min(a,b)) = {out['Q1']['regression_slope_log_min']:.3f}")
        print(f"     R^2 = {out['Q1']['regression_R2']:.4f}")

    if "Q2" not in skip:
        print("=" * 60)
        print("[Q2] Partial Dirichlet series")
        print("=" * 60)
        t0 = time.time()
        out["Q2"] = probe_dirichlet(args.N, s_values=[1.5, 2.0, 3.0])
        print(f"[Q2] done in {time.time() - t0:.2f}s")
        for s, lst in out["Q2"]["by_s"].items():
            print(f"  s = {s}:")
            for entry in lst:
                print(f"    X = {entry['X']:>9}  F_X/Z_X = {entry['ratio_F_over_Z']:.6f}")

    if "Q3" not in skip:
        print("=" * 60)
        print("[Q3] Smooth-Collatz density")
        print("=" * 60)
        t0 = time.time()
        out["Q3"] = probe_smoothness(args.N, y_values=[10, 50, 100, 500, 1000])
        print(f"[Q3] done in {time.time() - t0:.2f}s")
        print(f"     unrestricted mean(sigma_inf / log2 n) = {out['Q3']['mean_sigma_over_log2n_unrestricted']:.4f}")
        for y_str, info in out["Q3"]["by_y"].items():
            print(f"     y = {y_str:>5}  count = {info['count_smooth']:>9}  "
                  f"mean = {info['mean_sigma_over_log2n']:.4f}")

    if "Q4" not in skip:
        print("=" * 60)
        print("[Q4] Hardy-Littlewood circle method on parity count")
        print("=" * 60)
        t0 = time.time()
        out["Q4"] = probe_circle_method(args.N, q_max=args.q_max)
        print(f"[Q4] done in {time.time() - t0:.2f}s")
        for r in out["Q4"]["results"]:
            print(f"     X = {r['X']:>8}  max |S|/X = {r['best_abs_over_X']:.6f}  "
                  f"best frac = {r['best_frac']}  exponent = {r['exponent_log_best_over_log_X']:.4f}")

    out["wall_time_seconds"] = time.time() - t_total
    out_path = os.path.join(DATA_DIR, "sieve_analytic_probe.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\n[done] wrote {out_path}  (wall = {out['wall_time_seconds']:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
