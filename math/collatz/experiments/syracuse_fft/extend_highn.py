"""
Phase-3 hardening run: push the collision diagnostic E_n to the memory frontier.

Computes E_n = phi(3^n) CP_n - 1 for the Syracuse RV on (Z/3^n)^x at large n for
the two decisive scalar tilts:
    * untilted        s = 0
    * descent-balance s = s* ~ 0.438033   (E_{s*}[a] = log_2 3)
plus, at each n, the Plancherel cross-validation of CP_n and the support-on-units
and non-negativity checks (same rigor as the n<=15 table in results.md).

Memory: O(3^n) float64.  n=16 ~3.3 GB peak, n=17 ~9-10 GB peak.  Do NOT run n>=18
on a 16 GB box (it needs ~30 GB).  Pass the n values on the command line.

Run:  python3 extend_highn.py 16 17
Output: appends rows to data/En_highn.json and prints a table.
"""
from __future__ import annotations

import json
import math
import os
import resource
import sys
import time

import numpy as np

from syracuse_fft import GroupStructure, syracuse_law_fft

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

S_STAR = -math.log2(1 - 1 / math.log(3, 2)) - 1.0  # ~0.438033


def char_mass_plancherel(law: np.ndarray) -> float:
    """CP_n via Plancherel: (1/3^n) sum_xi |phi(xi)|^2.  Independent of sum law^2."""
    phi = np.fft.fft(law)
    return float(np.vdot(phi, phi).real) / law.size


def run_one(n: int, s: float) -> dict:
    t0 = time.time()
    law = syracuse_law_fft(n, s=s)
    mod = 3 ** n
    phi3n = 2 * 3 ** (n - 1)
    cp_direct = float(np.dot(law, law))
    cp_planch = char_mass_plancherel(law)
    En = phi3n * cp_direct - 1.0
    # support / non-negativity diagnostics
    nonunit_mask = np.zeros(mod, dtype=bool)
    nonunit_mask[::3] = True  # multiples of 3 are non-units
    mass_nonunits = float(law[nonunit_mask].sum())
    min_atom = float(law.min())
    dt = time.time() - t0
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 / 1024  # GB
    return {
        "n": n, "s": s, "CP_n": cp_direct,
        "CP_n_plancherel": cp_planch,
        "cp_rel_discrepancy": abs(cp_direct - cp_planch) / cp_direct,
        "E_n": En, "phi3n": phi3n,
        "mass_on_nonunits": mass_nonunits,
        "min_atom": min_atom,
        "time_s": dt, "peak_rss_gb": peak,
    }


def main(ns):
    out_path = os.path.join(DATA_DIR, "En_highn.json")
    results = []
    if os.path.exists(out_path):
        with open(out_path) as f:
            results = json.load(f)
    print("=" * 92)
    print("Phase-3 hardening: E_n at the memory frontier (untilted and s*)")
    print(f"s* = {S_STAR:.6f}")
    print("=" * 92)
    print(f"{'n':>3} {'tilt':>10} {'E_n':>14} {'CP_n':>14} "
          f"{'CPrelDisc':>11} {'massNonU':>10} {'minAtom':>10} {'t(s)':>7} {'RSS(GB)':>8}")
    for n in ns:
        for tag, s in [("untilted", 0.0), ("s*", S_STAR)]:
            r = run_one(n, s)
            r["tag"] = tag
            results.append(r)
            print(f"{n:>3} {tag:>10} {r['E_n']:>14.6f} {r['CP_n']:>14.6e} "
                  f"{r['cp_rel_discrepancy']:>11.2e} {r['mass_on_nonunits']:>10.2e} "
                  f"{r['min_atom']:>10.2e} {r['time_s']:>7.1f} {r['peak_rss_gb']:>8.2f}")
            # flush after each case so partial progress survives an OOM/timeout
            with open(out_path, "w") as f:
                json.dump(results, f, indent=2)
    print(f"\nSaved -> {out_path}")


if __name__ == "__main__":
    ns = [int(a) for a in sys.argv[1:]] or [16]
    main(ns)
