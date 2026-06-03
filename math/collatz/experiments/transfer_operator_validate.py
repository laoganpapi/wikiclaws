"""
Critical validation: verify that the invariant distribution pi_n of the
one-step Syracuse Markov transition kernel P_n on (Z/3^n)^x is EQUAL
to the Syracuse RV law from syracuse_fft.

This is the key structural claim implied by the deep-analysis output:
    pi_n  =  law of Syrac(Z/3^n Z) (the n-step recursion limit)
and explains why  E_n(pi_n) == E_n from syracuse_fft.

We compute pi_n via left-eigenvector of P_n and via syracuse_fft, and
compare directly (l_inf norm of the diff).
"""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from transfer_operator import syracuse_kernel, invariant_distribution, units_mod
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "syracuse_fft"))
from syracuse_fft import syracuse_law_fft  # type: ignore


def main():
    for n in range(1, 7):
        P, U = syracuse_kernel(n, s=0.0, a_max=200)
        pi = invariant_distribution(P)
        pi = np.clip(pi, 0, None)
        pi = pi / pi.sum()
        # syracuse_fft law on full Z/3^n; restrict to units
        full = syracuse_law_fft(n, s=0.0)
        unit_mask = np.array([i for i, x in enumerate(range(3 ** n)) if x % 3 != 0])
        # but U_n's ordering matches our `units_mod(n)` (which is in ascending integer order)
        # syracuse_fft's vector is indexed by residue r in [0, 3^n), so restrict by [r for r in U]
        nu_units = full[U]
        # nu_units should sum to 1 (since the Syracuse RV is supported on units)
        print(f"n={n}: nu_units sum = {nu_units.sum():.10f}")
        # normalize
        nu_units = nu_units / nu_units.sum()
        diff = np.abs(pi - nu_units).max()
        l2_diff = np.linalg.norm(pi - nu_units)
        print(f"  ||pi_n - Syracuse RV law||_inf = {diff:.4e}, l2 = {l2_diff:.4e}")
        # also TV
        tv = 0.5 * np.abs(pi - nu_units).sum()
        print(f"  TV(pi_n, Syracuse RV law) = {tv:.4e}")


if __name__ == "__main__":
    main()
