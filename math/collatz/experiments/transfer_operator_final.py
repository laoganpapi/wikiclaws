"""
Final analysis runner: produces JSON data tables for the writeup.

Outputs:
  data/spectrum_table_s0.json     -- untilted spectrum + invariant data, n=1..8
  data/spectrum_table_sstar.json  -- descent-balance tilt, n=2..6
  data/spectrum_table_s_neg.json  -- equidistributing tilt s = -0.5, n=2..6

Each entry contains: n, |U_n|, |lambda_2|, |lambda_perp|, TV(pi, U), E_n(pi),
pi_mod3, P_on_V_coeffs, top 10 moduli.
"""

from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from transfer_operator import (
    syracuse_kernel, invariant_distribution, mod3_obstruction_vectors,
    restricted_spectrum,
)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def analyze(n: int, s: float, a_max: int):
    P, U = syracuse_kernel(n, s=s, a_max=a_max)
    N = len(U)
    pi = invariant_distribution(P)
    pi = np.clip(pi, 0, None); pi /= pi.sum()
    unif = np.ones(N) / N
    tv = 0.5 * float(np.abs(pi - unif).sum())
    En = 2 * 3 ** (n - 1) * float(pi @ pi) - 1.0
    pi_mod3 = np.zeros(3)
    for i, u in enumerate(U):
        pi_mod3[u % 3] += pi[i]
    if N <= 1500:  # full eig affordable up to n=7
        eigs = np.linalg.eigvals(P)
    else:
        # use sparse for n=8
        from scipy.sparse import csr_matrix
        from scipy.sparse.linalg import eigs as sp_eigs
        Psp = csr_matrix(P)
        eigs = sp_eigs(Psp, k=40, which="LM", return_eigenvectors=False,
                       maxiter=20000, tol=1e-10, ncv=120)
    moduli = np.sort(np.abs(eigs))[::-1]
    # perp spectrum
    perp_top = None
    perp_top10 = []
    if N >= 3 and N <= 2000:
        V = mod3_obstruction_vectors(U)
        eigs_perp, _ = restricted_spectrum(P, V)
        perp_mods = np.sort(np.abs(eigs_perp))[::-1]
        perp_top = float(perp_mods[0])
        perp_top10 = [float(m) for m in perp_mods[:10]]
    return {
        "n": n, "s": s, "phi3n": N,
        "lambda2": float(moduli[1]) if len(moduli) > 1 else 0.0,
        "top10_moduli": [float(m) for m in moduli[:10]],
        "TV_pi_uniform": tv,
        "E_n_pi": En,
        "pi_mod3": pi_mod3.tolist(),
        "perp_top": perp_top,
        "perp_top10": perp_top10,
    }


def main():
    # Untilted
    print("=== UNTILTED s=0 ===")
    table_s0 = []
    for n in range(1, 9):
        t0 = time.time()
        a_max = 120 if n <= 6 else (80 if n == 7 else 60)
        res = analyze(n, 0.0, a_max)
        print(f"  n={n}: phi={res['phi3n']}, |lam_2|={res['lambda2']:.4e}, "
              f"TV={res['TV_pi_uniform']:.4f}, E_n={res['E_n_pi']:.4f}, "
              f"|lam_perp|={res['perp_top'] if res['perp_top'] is not None else 'n/a'}, "
              f"{time.time()-t0:.1f}s")
        table_s0.append(res)
    with open(os.path.join(DATA_DIR, "spectrum_table_s0.json"), "w") as f:
        json.dump(table_s0, f, indent=2)

    # Descent-balance tilt
    print("\n=== DESCENT-BALANCE TILT s=+0.438 ===")
    s_star = 0.43803
    table_sstar = []
    for n in range(2, 7):
        res = analyze(n, s_star, a_max=120)
        print(f"  n={n}: phi={res['phi3n']}, |lam_2|={res['lambda2']:.4e}, "
              f"TV={res['TV_pi_uniform']:.4f}, E_n={res['E_n_pi']:.4f}")
        table_sstar.append(res)
    with open(os.path.join(DATA_DIR, "spectrum_table_sstar.json"), "w") as f:
        json.dump(table_sstar, f, indent=2)

    # Equidistributing tilt
    print("\n=== EQUIDISTRIBUTING TILT s=-0.5 ===")
    table_sneg = []
    for n in range(2, 7):
        res = analyze(n, -0.5, a_max=120)
        print(f"  n={n}: phi={res['phi3n']}, |lam_2|={res['lambda2']:.4e}, "
              f"TV={res['TV_pi_uniform']:.4f}, E_n={res['E_n_pi']:.4f}")
        table_sneg.append(res)
    with open(os.path.join(DATA_DIR, "spectrum_table_s_neg.json"), "w") as f:
        json.dump(table_sneg, f, indent=2)

    # Plain-text dump
    with open(os.path.join(DATA_DIR, "spectrum_summary.txt"), "w") as f:
        f.write("# Spectral analysis of one-step Syracuse Markov transition operator\n")
        f.write("# on (Z/3^n Z)^x.  Eigenvalues by |.|, descending.\n\n")
        for label, table in [("s=0 UNTILTED", table_s0),
                              ("s=+0.438 DESCENT-BALANCE", table_sstar),
                              ("s=-0.5 EQUIDISTRIBUTING", table_sneg)]:
            f.write(f"\n## {label}\n")
            f.write(f"{'n':>3} {'|U_n|':>8} {'|lam_2|':>14} {'|lam_perp|':>14} "
                    f"{'TV(pi,U)':>10} {'E_n(pi)':>10} {'pi mod 3':>32}\n")
            for r in table:
                lp = r["perp_top"]
                lp_s = f"{lp:>14.4e}" if lp is not None else f"{'n/a':>14}"
                pm = r["pi_mod3"]
                pm_s = f"({pm[0]:.4f},{pm[1]:.4f},{pm[2]:.4f})"
                f.write(f"{r['n']:>3} {r['phi3n']:>8} {r['lambda2']:>14.4e} {lp_s} "
                        f"{r['TV_pi_uniform']:>10.4f} {r['E_n_pi']:>10.4f} {pm_s:>32}\n")
    print(f"\nWrote: {os.path.join(DATA_DIR, 'spectrum_summary.txt')}")


if __name__ == "__main__":
    main()
