"""
run_baseline.py — End-to-end smoke + baseline statistics run.

Runs:
  1. UC family enumeration for n = 0 … 5 (orbit counts).
  2. Extremal search: per-n minimum-abundance UC families.
  3. Direct verification of Frankl on every n ≤ 5 family.
  4. Gilmer's entropy inequality sweep across the same range.
  5. Computes and reports the AHS constant (3 - √5)/2.

Outputs:
  * Pretty-printed summary to stdout.
  * Machine-readable JSON snapshot at ``data/baseline.json``.

Intended to take <10 minutes on a laptop.  Heavier sweeps (n = 6, large
sizes) should be wrapped in separate driver scripts so this baseline
stays a fast pre-flight check.
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from dataclasses import asdict
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from uc_family import abundance, family_to_sets, frequencies, ground_set  # noqa: E402
from enumerate import all_uc_families, count_uc_families  # noqa: E402
from entropy_bounds import (  # noqa: E402
    ahs_constant,
    binary_entropy,
    gilmer_inequality,
    gilmer_inequality_pair,
    sweep_inequality,
)
from extremal_search import search_extremal, family_summary  # noqa: E402
from verify_frankl import verify  # noqa: E402


def _fmt_family(F) -> list[list[int]]:
    return [sorted(s) for s in family_to_sets(F)]


def main(n_max: int = 5, max_size_for_n5: int | None = None) -> dict[str, Any]:
    """
    Run the baseline sweep through n = 0 … n_max.

    Parameters
    ----------
    n_max
        Largest ground-set size to enumerate.  Default 5 (the standard
        Bošnjak-Marković verification range).
    max_size_for_n5
        Optional cap on |F| for n = 5 — useful when running on a small
        machine.  Default ``None`` (no cap).
    """
    snapshot: dict[str, Any] = {
        "schema": "frankl-baseline/v1",
        "n_range": list(range(n_max + 1)),
        "by_n": {},
    }

    # ----- The AHS constant (computed) -----
    c = ahs_constant()
    expected_c = (3.0 - math.sqrt(5.0)) / 2.0
    print(f"AHS constant (3 - √5)/2 ≈ {c:.16f}  (closed form {expected_c:.16f}, diff {abs(c - expected_c):.2e})")
    snapshot["ahs_constant_computed"] = c
    snapshot["ahs_constant_closed_form"] = expected_c

    print()
    print("=" * 78)
    print("Per-n statistics")
    print("=" * 78)
    print(f"{'n':>3}  {'orbits':>10}  {'min φ':>10}  {'extremal |F|':>12}  "
          f"{'verify':>10}  {'time (s)':>10}")
    print("-" * 78)

    grand_t0 = time.time()
    for n in range(n_max + 1):
        size_cap = max_size_for_n5 if n == 5 else None
        t0 = time.time()
        # Enumeration (orbit count).
        orbit_count = 0
        # Track extremal data while iterating.
        best_phi = float("inf")
        best_F = None
        best_size = 0
        gilmer_pass = True
        gilmer_min_slack = float("inf")
        for F in all_uc_families(n, max_size=size_cap):
            if not F:
                continue
            orbit_count += 1
            if F == frozenset({0}):
                continue  # F = {∅}, exclude
            phi = abundance(F)
            if phi < best_phi:
                best_phi = phi
                best_F = F
                best_size = len(F)
            rep = gilmer_inequality(F)
            if rep.slack < gilmer_min_slack:
                gilmer_min_slack = rep.slack
            if not rep.holds:
                gilmer_pass = False
        elapsed = time.time() - t0

        # Direct Frankl verification (redundant but explicit).
        verify_res = verify(n, max_size=size_cap)

        row = {
            "n": n,
            "size_cap": size_cap,
            "orbit_count": orbit_count,
            "min_abundance": best_phi if best_phi != float("inf") else None,
            "extremal_family_size": best_size,
            "extremal_family": _fmt_family(best_F) if best_F is not None else None,
            "extremal_freqs": frequencies(best_F, ground_set(best_F)) if best_F else None,
            "verify_passed": verify_res.all_pass,
            "verify_failures": len(verify_res.failures),
            "gilmer_inequality_held_everywhere": gilmer_pass,
            "gilmer_min_slack": gilmer_min_slack if gilmer_min_slack != float("inf") else None,
            "elapsed_seconds": elapsed,
        }
        snapshot["by_n"][str(n)] = row

        phi_str = f"{best_phi:.6f}" if best_phi != float("inf") else "  —   "
        size_str = f"{best_size}" if best_size else "—"
        ver_str = "PASS" if verify_res.all_pass else f"FAIL×{len(verify_res.failures)}"
        print(f"{n:>3}  {orbit_count:>10}  {phi_str:>10}  {size_str:>12}  "
              f"{ver_str:>10}  {elapsed:>10.2f}")
    grand_elapsed = time.time() - grand_t0
    snapshot["total_elapsed_seconds"] = grand_elapsed
    print("-" * 78)
    print(f"total time: {grand_elapsed:.2f}s")

    # ----- Show extremal families per n -----
    print()
    print("=" * 78)
    print("Extremal UC families per n (minimum abundance)")
    print("=" * 78)
    for n in range(n_max + 1):
        row = snapshot["by_n"][str(n)]
        if row["extremal_family"] is None:
            continue
        print(f"n = {n}:  |F| = {row['extremal_family_size']}, "
              f"φ = {row['min_abundance']:.6f}, "
              f"freqs = {row['extremal_freqs']}, "
              f"sets = {row['extremal_family']}")

    # ----- Sweep Gilmer's inequality through n ≤ n_max -----
    print()
    print("=" * 78)
    print("Sweep Gilmer's inequality through n ≤", n_max)
    print("=" * 78)
    sweeps = sweep_inequality(gilmer_inequality_pair, n_max=n_max,
                              max_size=max_size_for_n5)
    for n, res in sweeps.items():
        print(res.summary())
    snapshot["gilmer_sweep"] = {
        str(n): {
            "families_checked": r.families_checked,
            "passed": r.passed,
            "counterexamples": len(r.counterexamples),
        }
        for n, r in sweeps.items()
    }

    # ----- Persist -----
    data_dir = os.path.join(HERE, "data")
    os.makedirs(data_dir, exist_ok=True)
    out_path = os.path.join(data_dir, "baseline.json")
    with open(out_path, "w") as f:
        json.dump(snapshot, f, indent=2, default=str)
    print()
    print(f"snapshot written → {out_path}")

    return snapshot


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--n-max", type=int, default=5)
    p.add_argument("--max-size-n5", type=int, default=None,
                   help="optional |F| cap when enumerating n=5")
    args = p.parse_args()
    main(n_max=args.n_max, max_size_for_n5=args.max_size_n5)
