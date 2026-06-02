"""
Independent brute-force / exact reference for the Syracuse RV law, used ONLY to
cross-check the FFT recursion.  Two independent reference implementations:

  (R1) reference_law_dp   : the EXACT (R, suffix-sum) dynamic program, identical
                            in spirit to verify_syracuse_rv.py (the prior agent's
                            code), truncating a_j <= a_max.  Returns law over
                            Z/3^n as a numpy float vector (renormalized).

  (R2) reference_phi_direct: phi_n(xi) computed directly from the law vector R1.

These let us check the FFT recursion's phi_n(xi) and E_n against the exact DP for
n=2..6 (the mandatory checkpoint).
"""

from __future__ import annotations

import numpy as np


def inv_pow2_mod(m: int, modulus: int) -> int:
    inv2 = (modulus + 1) // 2
    return pow(inv2, m, modulus)


def reference_law_dp(n: int, a_max: int = 60, s: float = 0.0) -> np.ndarray:
    """
    EXACT law of Syrac_s(Z/3^n) over truncated support a_j in [1,a_max], returned
    as a float numpy vector of length 3^n (renormalized to sum 1).  Mirrors the
    DP of verify_syracuse_rv.py: DP from j=n down to j=1 carrying (residue R,
    suffix exponent E=S_j).
    """
    modulus = 3 ** n
    ratio = 0.5 ** (1.0 + s)
    geom = {k: ratio ** k for k in range(1, a_max + 1)}

    dist = {(0, 0): 1.0}
    for j in range(n, 0, -1):
        new: dict[tuple[int, int], float] = {}
        coeff = pow(3, n - j, modulus)
        for (R, E), p in dist.items():
            for k, pk in geom.items():
                S_j = E + k
                term = (coeff * inv_pow2_mod(S_j, modulus)) % modulus
                R2 = (R + term) % modulus
                key = (R2, S_j)
                new[key] = new.get(key, 0.0) + p * pk
        dist = new

    law = np.zeros(modulus, dtype=np.float64)
    for (R, _E), p in dist.items():
        law[R] += p
    law /= law.sum()
    return law


def reference_phi_direct(law: np.ndarray, xi: int, n: int) -> complex:
    """phi_n(xi) = sum_b law[b] e(-xi b / 3^n), computed directly."""
    modulus = 3 ** n
    b = np.arange(modulus)
    return complex(np.sum(law * np.exp(-2j * np.pi * xi * b / modulus)))


def reference_En(n: int, a_max: int = 60, s: float = 0.0) -> float:
    """E_n = phi(3^n) * CP_n - 1, from the exact DP law vector."""
    law = reference_law_dp(n, a_max=a_max, s=s)
    cp = float(np.sum(law * law))
    phi = 2 * 3 ** (n - 1)
    return phi * cp - 1.0


def reference_law_via_fft_of_phi(n: int, s: float = 0.0, a_max: int = 60) -> np.ndarray:
    """
    Alternative exact law: build via the EXACT DP, then this is identical to R1.
    Kept as a hook; not used.
    """
    return reference_law_dp(n, a_max=a_max, s=s)
