"""
boolean_fourier_sweep.py — Sweep all UC families (orbit reps) up to n=5,
compute Fourier spectra + derived quantities, test hypotheses H1–H4 from the
brief, and write data + summary.

Outputs:
    data/fourier_n{k}.jsonl           — per-family rows
    data/fourier_summary.txt          — human-readable rundown
    data/fourier_hypotheses.txt       — H1–H4 status, counter-examples (if any)
"""
from __future__ import annotations

import json
import os
import sys
import time

# Local imports — relative to this directory.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from enumerate import all_uc_families
from uc_family import abundance, frequencies, ground_set
from boolean_fourier import (
    fourier_spectrum,
    level_weights,
    influences,
    total_influence,
    noise_stability,
    singleton_coeffs,
    verify_abundance_identity,
    parseval,
)


DATA_DIR = os.path.join(HERE, "data")
os.makedirs(DATA_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Per-family record
# ---------------------------------------------------------------------------

def fourier_record(F, n: int) -> dict:
    """One-row dict with all features for a UC family ``F``."""
    F_list = list(F)
    size_F = len(F_list)
    p = size_F / (1 << n) if n >= 0 else 0.0  # = f̂(∅)
    freqs = frequencies(F_list, n)
    abs_i = [freqs[i] / size_F for i in range(n)] if size_F else []
    spec = fourier_spectrum(F_list, n)

    # Singleton coeffs
    singletons = [spec.get(1 << i, 0.0) for i in range(n)]

    # Level weights
    W = [0.0] * (n + 1)
    for S, v in spec.items():
        W[bin(S).count("1")] += v * v

    # Influences
    inf = [0.0] * n
    for S, v in spec.items():
        if v == 0.0:
            continue
        v2 = v * v
        for i in range(n):
            if (S >> i) & 1:
                inf[i] += v2
    tot_inf = sum(bin(S).count("1") * (v * v) for S, v in spec.items())

    # Noise stability at several ρ
    stab = {}
    for rho in (0.25, 0.5, 0.75, 0.9):
        stab[rho] = sum(
            (rho ** bin(S).count("1")) * (v * v) for S, v in spec.items()
        )

    abund_max = max(abs_i) if abs_i else 0.0
    return {
        "n": n,
        "size": size_F,
        "p": p,
        "abund_per_elem": abs_i,
        "abund_max": abund_max,
        "abund_min": min(abs_i) if abs_i else 0.0,
        "singletons": singletons,
        "level_weights": W,
        "influences": inf,
        "total_influence": tot_inf,
        "min_influence": min(inf) if inf else 0.0,
        "max_influence": max(inf) if inf else 0.0,
        "stab": stab,
        # Identity check
        "abundance_identity_ok": all(
            abs(singletons[i] - p * (1.0 - 2.0 * abs_i[i])) < 1e-10
            for i in range(n)
        ),
    }


# ---------------------------------------------------------------------------
# Sweep
# ---------------------------------------------------------------------------

def run_sweep(max_n: int = 5) -> None:
    summary_lines: list[str] = []
    summary_lines.append("Boolean-Fourier sweep over UC orbit representatives")
    summary_lines.append("=" * 64)

    totals_by_n: dict[int, int] = {}
    grand_total = 0

    for n in range(0, max_n + 1):
        path = os.path.join(DATA_DIR, f"fourier_n{n}.jsonl")
        count = 0
        t0 = time.time()
        with open(path, "w") as fh:
            for F in all_uc_families(n, include_empty_family=True):
                if not F:
                    # Empty family - skip (no abundance defined)
                    continue
                rec = fourier_record(F, n)
                # Also record the family itself (sorted list) for reproducibility.
                rec["F"] = sorted(F)
                fh.write(json.dumps(rec) + "\n")
                count += 1
        dt = time.time() - t0
        totals_by_n[n] = count
        grand_total += count
        summary_lines.append(
            f"  n={n}: {count} UC families, computed in {dt:.2f}s "
            f"→ {os.path.relpath(path, HERE)}"
        )

    summary_lines.append(f"  TOTAL across n≤{max_n}: {grand_total}")
    summary_lines.append("")

    # Validate the abundance identity globally
    bad = 0
    for n in range(0, max_n + 1):
        path = os.path.join(DATA_DIR, f"fourier_n{n}.jsonl")
        with open(path) as fh:
            for line in fh:
                rec = json.loads(line)
                if not rec["abundance_identity_ok"]:
                    bad += 1
    summary_lines.append(
        f"Sanity check  f̂({{i}}) = f̂(∅)·(1−2·abund_i):  "
        f"{'PASS (0 failures)' if bad == 0 else f'FAIL ({bad} failures)'}"
    )
    summary_lines.append("")

    out = "\n".join(summary_lines)
    print(out)
    with open(os.path.join(DATA_DIR, "fourier_summary.txt"), "w") as fh:
        fh.write(out + "\n")


if __name__ == "__main__":
    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    run_sweep(max_n=max_n)
