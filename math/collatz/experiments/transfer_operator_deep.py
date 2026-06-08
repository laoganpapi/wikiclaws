"""
Deeper diagnostics on the Syracuse transfer operator.

Goals:
  (a) Verify the explicit structural finding: P_n is NOT doubly-stochastic and
      its invariant distribution pi_n IS the natural "Syracuse-stationary"
      measure, which is NOT uniform on units. Compare pi_n's TV distance to
      uniform with the syracuse_fft E_n diagnostic.
  (b) Identify the mod-3^k coset structure in the spectrum: the operator should
      have blocks/eigenvectors lifted from lower n.
  (c) Compute the n-step EVOLUTION starting from the W_0 = 0 indicator:
        rho_0 = delta_{somewhere};  apply L_n n times; compare to the
      Syracuse RV law from syracuse_fft.  Note: the Syracuse RV uses a
      "growing" W_m = 2^{-a_m}(W_{m-1} + 3^{n-m}) recursion -- the additive
      shift depends on m, so it is NOT exactly the same as iterating the
      Syracuse map on a fixed residue. But the mixing rate the operator
      captures bounds the per-step contraction of any starting density to
      the invariant pi_n.

  (d) Quantify the SPECTRAL GAP scaling with n, and compare with what would
      be needed for a natural-density argument.

  (e) Identify the specific eigenvector / eigenvalue carrying the mod-3
      obstruction.

Author: Alex Ye.
"""

from __future__ import annotations

import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from transfer_operator import (
    syracuse_kernel, spectrum, invariant_distribution,
    mod3_obstruction_vectors, units_mod, restricted_spectrum,
)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def detailed_analysis(n: int, s: float = 0.0, a_max: int = 120) -> dict:
    print(f"\n=== DEEP analysis: n={n}, s={s} ===")
    P, U = syracuse_kernel(n, s=s, a_max=a_max)
    N = len(U)
    print(f"  |U_n| = {N}")

    # row sums
    row_err = float(np.abs(P.sum(axis=1) - 1.0).max())
    col_sums = P.sum(axis=0)
    col_min = float(col_sums.min())
    col_max = float(col_sums.max())
    col_mean = float(col_sums.mean())
    print(f"  row sums err: {row_err:.3e}")
    print(f"  col sums: min={col_min:.6f}, max={col_max:.6f}, mean={col_mean:.6f}")
    print(f"  (col_mean should be 1.0 if doubly stochastic; sum/N = {col_sums.sum()/N:.6f})")

    # invariant distribution
    pi = invariant_distribution(P)
    pi = pi.clip(min=0)
    pi = pi / pi.sum()
    print(f"  pi: max={pi.max():.6e}, min={pi.min():.6e}")
    unif = np.ones(N) / N
    tv_pi_unif = 0.5 * float(np.abs(pi - unif).sum())
    print(f"  TV(pi, uniform) = {tv_pi_unif:.6f}")

    # mod-3 marginal of pi
    pi_mod3 = np.zeros(3)
    for i, u in enumerate(U):
        pi_mod3[u % 3] += pi[i]
    print(f"  pi mod 3: {pi_mod3.tolist()}  (expected (0, 1/3, 2/3))")

    # mod-9 marginal of pi (if n >= 2)
    if n >= 2:
        pi_mod9 = np.zeros(9)
        for i, u in enumerate(U):
            pi_mod9[u % 9] += pi[i]
        # only residues 1,2,4,5,7,8 (units mod 9) should have mass
        print(f"  pi mod 9: {pi_mod9.tolist()}")
        # Expected from n=2 Syracuse law: see verify_syracuse_rv.py
        # The Syracuse RV at n=2 has law on U_2 = {1,2,4,5,7,8}.

    # compare to syracuse_fft E_n: load if available
    en_uni = compute_En_from_pi(pi, n)
    print(f"  E_n from pi = phi(3^n)*||pi||^2 - 1 = {en_uni:.6f}")
    # this is the E_n of the invariant distribution, NOT the W_n=Syracuse RV law.
    # They differ; let's still report.

    # spectrum
    eigs, R, L = spectrum(P)
    moduli = np.abs(eigs)
    print(f"  spectrum (top 10 moduli): {moduli[:10].tolist()}")

    # mod-3 obstruction
    V = mod3_obstruction_vectors(U)
    PV = P @ V
    coeffs, _, _, _ = np.linalg.lstsq(V, PV, rcond=None)
    res_norm = float(np.linalg.norm(PV - V @ coeffs))
    print(f"  P preserves span(V) (mod-3 indicators)? residual = {res_norm:.3e}")
    print(f"  P|_V (2x2):\n{coeffs}")
    # eigenvalues of P|_V
    eigs_V = np.linalg.eigvals(coeffs)
    print(f"  eigenvalues of P|_V: {eigs_V}")

    # The mod-3 obstruction eigenvector: in span(V), there's the constant
    # direction (e_1 + e_2 = const-on-units, lambda=1) and the
    # "deviation from stationary" direction.
    # Eigenvector for lambda=1 of P|_V: solve (P|_V - I) x = 0
    # P|_V = [[1/3, 2/3],[1/3, 2/3]], so eigenvec for lambda=1 is [1/3, 2/3]^T
    # (scaled). This means: the residue-mod-3 distribution that's STATIONARY
    # under one Syracuse step is (1/3 on class-1, 2/3 on class-2). This is
    # exactly the (0,1/3,2/3) law that's been bothering us.

    # Now also compute spectrum on perpendicular complement
    if N > 2:
        eigs_perp, _ = restricted_spectrum(P, V)
        mod_perp = np.abs(eigs_perp)
        print(f"  perp spectrum (top 10 moduli): {mod_perp[:10].tolist()}")
        perp_top = float(mod_perp[0]) if len(mod_perp) > 0 else None
    else:
        perp_top = None
        eigs_perp = np.array([])

    return {
        "n": n,
        "s": s,
        "|U_n|": N,
        "row_err": row_err,
        "col_sum_min": col_min,
        "col_sum_max": col_max,
        "pi_max": float(pi.max()),
        "pi_min": float(pi.min()),
        "TV_pi_unif": tv_pi_unif,
        "pi_mod3": pi_mod3.tolist(),
        "E_n_of_pi": en_uni,
        "top10_moduli": [float(m) for m in moduli[:10]],
        "perp_top10_moduli": [float(m) for m in np.abs(eigs_perp)[:10]] if len(eigs_perp) > 0 else [],
        "perp_top_modulus": perp_top,
        "P_on_V_coeffs": coeffs.tolist(),
        "P_on_V_eigs_real": [float(e.real) for e in eigs_V],
        "P_on_V_eigs_imag": [float(e.imag) for e in eigs_V],
    }


def compute_En_from_pi(pi: np.ndarray, n: int) -> float:
    """E_n equivalent for the invariant pi (not the Syracuse RV)."""
    phi3n = 2 * 3 ** (n - 1)
    return phi3n * float(pi @ pi) - 1.0


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    results = []
    for n in range(1, nmax + 1):
        r = detailed_analysis(n, s=0.0, a_max=120)
        results.append(r)
    with open(os.path.join(DATA_DIR, "spectrum_deep.json"), "w") as f:
        json.dump(results, f, indent=2)

    print("\n\n=== SCALING TABLE ===")
    print(f"{'n':>3} {'|U_n|':>8} {'|lambda_2|':>14} {'1-|lambda_2|':>14} {'|lambda_perp|':>16} {'TV(pi,U)':>12} {'E_n(pi)':>10}")
    for r in results:
        lam2 = r["top10_moduli"][1] if len(r["top10_moduli"]) > 1 else 0.0
        gap = 1.0 - lam2
        lamp = r["perp_top_modulus"]
        print(f"{r['n']:>3} {r['|U_n|']:>8} {lam2:>14.6e} {gap:>14.6e} "
              f"{(lamp if lamp is not None else 0):>16.6e} {r['TV_pi_unif']:>12.6f} {r['E_n_of_pi']:>10.4f}")


if __name__ == "__main__":
    main()
