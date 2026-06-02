"""
lattice_sweep.py — Sweep all union-closed families n ≤ 5 and parametric lattice
classes, recording lattice invariants vs abundance.

Goal (per the lattice-attack brief):
  1. Look for a STRUCTURAL inequality  abundance ≥ f(lattice invariants)  that the
     entropy method (capped at ψ) misses — in particular whether some structural
     parameter (height, #join-irreducibles, width, modularity defect) FORCES an
     element of abundance ≥ 1/2.
  2. Look for an OBSTRUCTION: two UC families with identical lattice invariants but
     different abundance, proving the invariants alone do not control abundance.

Outputs:
  * data/lattice_sweep_n{N}.jsonl  — one JSON record per family.
  * Console summary: min abundance within each invariant class; collision search
    (same invariant signature, different abundance); candidate inequality checks.

This is a Step-1 (computational) artifact. No theorem is asserted here; the script
gathers the evidence that the writeup reasons about.
"""

from __future__ import annotations

import json
import os
import sys
import time
from collections import defaultdict
from dataclasses import asdict

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from uc_family import abundance, frequencies, ground_set, family_to_sets  # noqa: E402
from enumerate import all_uc_families  # noqa: E402
import lattice as Lat  # noqa: E402


def family_record(F) -> dict:
    """Compute abundance + lattice invariants for one UC family (|F| ≥ 2)."""
    inv = Lat.invariants(F)
    phi = abundance(F)
    n = ground_set(F)
    fr = frequencies(F, n)
    rec = asdict(inv)
    rec["abundance"] = phi
    rec["max_freq"] = max(fr) if fr else 0
    rec["ground_n"] = n
    # modularity defect proxies
    rec["mod_defect"] = 0 if inv.modular else 1
    rec["distrib_defect"] = 0 if inv.distributive else 1
    # the family itself (sorted sets) for collision witnesses
    rec["sets"] = [sorted(s) for s in family_to_sets(F)]
    return rec


def sweep(n_max: int = 5, write: bool = True) -> dict:
    """Run the full sweep n=0..n_max over UC families with |F| ≥ 2."""
    summary = {"n_max": n_max, "by_n": {}}
    data_dir = os.path.join(HERE, "data")
    os.makedirs(data_dir, exist_ok=True)

    for n in range(n_max + 1):
        t0 = time.time()
        records = []
        for F in all_uc_families(n):
            if len(F) < 2:
                continue
            # skip F = {∅} (single empty set) — abundance undefined; |F|<2 anyway
            records.append(family_record(F))
        elapsed = time.time() - t0

        if write:
            out = os.path.join(data_dir, f"lattice_sweep_n{n}.jsonl")
            with open(out, "w") as f:
                for r in records:
                    f.write(json.dumps(r) + "\n")

        # min abundance overall
        min_phi = min((r["abundance"] for r in records), default=None)
        summary["by_n"][n] = {
            "count": len(records),
            "min_abundance": min_phi,
            "elapsed_s": elapsed,
        }
        print(f"n={n}: {len(records)} families, min abundance={min_phi}, "
              f"t={elapsed:.1f}s")

    return summary


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--n-max", type=int, default=5)
    args = p.parse_args()
    sweep(n_max=args.n_max)
