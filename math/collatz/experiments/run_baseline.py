"""
Run the baseline verification + stats pipeline for n in [1, 10^7].

Outputs:
  experiments/data/baseline_stats.json       — full stats summary
  experiments/data/baseline_residue.json     — residue-class analysis k = 4..20
  experiments/data/baseline_cycles.json      — cycle search results
  experiments/data/baseline_verification.json — verifier sanity result
  experiments/figures/baseline_*.png         — distribution plots

Usage:
  python run_baseline.py [--N 10000000] [--quick]

--quick reduces N to 10^5 for fast smoke-testing.

Author: Alex Ye with Claude.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, "data")
FIG_DIR = os.path.join(THIS_DIR, "figures")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--N", type=int, default=10**7,
                   help="Upper bound for verification + stats (default 10^7).")
    p.add_argument("--quick", action="store_true",
                   help="Quick smoke-test (N=10^5, fewer k values).")
    p.add_argument("--no-residue", action="store_true",
                   help="Skip residue-class analysis (saves time).")
    p.add_argument("--no-cycles", action="store_true",
                   help="Skip cycle search (saves time).")
    args = p.parse_args()

    if args.quick:
        args.N = 10**5

    from verifier import verify_range, total_stopping_time

    total_t0 = time.perf_counter()

    # -------------------- 1. Verification --------------------
    print(f"=" * 70)
    print(f"[baseline] step 1: verify_range(1, {args.N + 1})")
    print(f"=" * 70)
    t0 = time.perf_counter()
    verified, max_sigma, arg_max = verify_range(1, args.N + 1, quiet=False)
    verify_elapsed = time.perf_counter() - t0
    print(f"[verify] {verified} integers verified in {verify_elapsed:.2f}s "
          f"({verified / verify_elapsed:,.0f} n/s)")
    print(f"[verify] longest sigma_inf = {max_sigma} at n = {arg_max}")
    # Cross-check the longest with the reference implementation
    cross = total_stopping_time(arg_max)
    assert cross == max_sigma, f"cross-check failed: {cross} vs {max_sigma}"
    print(f"[verify] cross-check OK: total_stopping_time({arg_max}) = {cross}")

    verify_result = {
        "N": args.N,
        "verified_count": verified,
        "max_sigma_inf": max_sigma,
        "argmax_n": arg_max,
        "elapsed_seconds": verify_elapsed,
        "throughput_n_per_sec": verified / verify_elapsed,
    }
    with open(os.path.join(DATA_DIR, "baseline_verification.json"), "w") as f:
        json.dump(verify_result, f, indent=2)
    print(f"[verify] wrote data/baseline_verification.json")

    # -------------------- 2. Stats --------------------
    print()
    print(f"=" * 70)
    print(f"[baseline] step 2: stats on n in [1, {args.N}]")
    print(f"=" * 70)
    # For N=10^7 this can use significant memory (~80MB for sigma_arr + tau_arr).
    # That's fine.
    from stats import run_full_stats
    summary = run_full_stats(args.N, prefix="baseline", verbose=True)
    with open(os.path.join(DATA_DIR, "baseline_stats.json"), "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"[stats] wrote data/baseline_stats.json")

    # -------------------- 3. Residue analysis --------------------
    if not args.no_residue:
        print()
        print(f"=" * 70)
        print(f"[baseline] step 3: residue analysis")
        print(f"=" * 70)
        from residue_analysis import run_residue_analysis
        k_vals = [4, 8, 12, 16] if args.quick else [4, 8, 12, 16, 20]
        residue_result = run_residue_analysis(k_vals, verbose=True)
        with open(os.path.join(DATA_DIR, "baseline_residue.json"), "w") as f:
            json.dump(residue_result, f, indent=2, default=str)
        print(f"[residue] wrote data/baseline_residue.json")

    # -------------------- 4. Cycle search --------------------
    if not args.no_cycles:
        print()
        print(f"=" * 70)
        print(f"[baseline] step 4: cycle search")
        print(f"=" * 70)
        from cycles import run_cycle_search
        cycle_result = run_cycle_search(
            parity_max_m=18 if args.quick else 22,
            orbit_N_max=min(args.N, 10**5 if args.quick else 10**6),
            orbit_L_max=1000,
            verbose=True,
        )
        with open(os.path.join(DATA_DIR, "baseline_cycles.json"), "w") as f:
            json.dump(cycle_result, f, indent=2, default=str)
        print(f"[cycles] wrote data/baseline_cycles.json")

    # -------------------- 5. Final summary --------------------
    total_elapsed = time.perf_counter() - total_t0
    print()
    print(f"=" * 70)
    print(f"BASELINE COMPLETE in {total_elapsed:.2f}s")
    print(f"=" * 70)
    print(f"  N = {args.N}")
    print(f"  verified count = {verified}")
    print(f"  longest sigma_inf = {max_sigma} (at n = {arg_max})")
    print(f"  mean sigma_inf / log(n) regression slope = "
          f"{summary['regression']['slope_natural_log']:.4f}")
    print(f"  heuristic slope = "
          f"{summary['regression']['heuristic_slope']:.4f}")
    print(f"  log-descent observable mean r = "
          f"{summary['log_descent_observable']['mean_r']:.4f}  "
          f"(heuristic 1.0)")
    print(f"  output dir: {DATA_DIR}")
    print(f"  figures: {FIG_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
