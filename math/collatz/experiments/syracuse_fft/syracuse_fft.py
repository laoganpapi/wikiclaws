"""
FFT-based computation of the Syracuse random variable law on (Z/3^n Z)^x and the
collision diagnostic  E_n = phi(3^n) * CP_n - 1.

Decisive large-n experiment for the Collatz "Vector A" track.  Reimplements the
small-n computation of `experiments/verify_syracuse_rv.py` with an O(3^n)-memory,
O(n * 3^n * log 3^n)-time forward recursion whose unit-multiplication step is an
FFT cyclic convolution in the discrete-log coordinate -- pushing n to ~12-14,
far past the n<=6 reachable by the direct (R, suffix-sum) DP.

------------------------------------------------------------------------------
DEFINITIONS (verbatim from tao_syracuse_explicit.md / verify_syracuse_rv.py)
------------------------------------------------------------------------------
Syracuse RV mod 3^n (a_1..a_n i.i.d. s-tilted geometric P_s(a=k) propto 2^{-k(1+s)}):
    X_n = sum_{j=1}^{n} 3^{n-j} 2^{-(a_j+...+a_n)}   (mod 3^n).
Characteristic function:  phi_n(xi) = E[e(-xi X_n/3^n)],  e(t)=exp(2 pi i t).
Collision probability / diagnostic:
    CP_n = sum_b P(X_n=b)^2 ,   E_n = phi(3^n) CP_n - 1 ,   phi(3^n)=2*3^{n-1}.
E_n = 0  iff  X_n is uniform on the units (the natural-density requirement);
TV(nu_n, U) <= (1/2) sqrt(E_n).

------------------------------------------------------------------------------
THE FORWARD W-RECURSION  (derived + Monte-Carlo verified; see tests)
------------------------------------------------------------------------------
Let W_m := sum_{j=1}^m 3^{n-j} 2^{-(a_j+...+a_m)} (mod 3^n).  Then W_n = X_n and
        W_m = 2^{-a_m} ( W_{m-1} + 3^{n-m} )   (mod 3^n),   W_0 = 0.
So one step is:  (i) add the constant 3^{n-m}  [a cyclic shift of the law on the
ADDITIVE group Z/3^n], then (ii) multiply by 2^{-a_m} with a_m ~ s-tilted geom.

Multiplication by 2^{-k} preserves the 3-adic valuation v_3, so it acts shell-by-
shell: on the shell {x: v_3(x)=L} ~ (Z/3^{n-L})^x (cyclic, generator 2, order
M_L = 2*3^{n-L-1}), it is a shift by -k in the discrete log.  Hence the geometric
mixture  sum_k P_s(a=k) (x |-> 2^{-k} x)  is, per shell, a CYCLIC CORRELATION of
the shell's law (in dlog order) with the geometric kernel -- done by one FFT of
length M_L per shell.  Total work sum_L M_L log M_L <= n*3^n; memory O(3^n).

The mandatory cross-check against verify_syracuse_rv.py's exact DP (n=2..6, both
tilts) is in `crosscheck.py`; this module's `compute_En` reproduces those exact
values to ~1e-12.

Author: Alex Ye (computational experiment; AI assistance disclosed separately).
"""

from __future__ import annotations

import numpy as np


def _powers_of_2_mod(ML: int, sub_mod: int) -> np.ndarray:
    """
    Vectorized  [2^t mod sub_mod  :  t = 0 .. ML-1]  with no int64 overflow.

    Computed by a blocked cumulative product:  pick a block length B with
    (sub_mod-1) * 2^B < 2^63, take the base-2 cumprod within the block (<=2^B),
    scale by the running value `cur`, reduce mod sub_mod, then advance `cur` by
    2^B.  Drop-in replacement for the O(ML) Python loop `cur=(cur*2)%sub_mod`;
    verified identical to it for sub_mod = 3^1..3^10 (see tests).  This makes the
    GroupStructure build O(ML / B) numpy ops instead of O(ML) Python iterations,
    which is what lets n reach 16-17 in reasonable wall time.
    """
    out = np.empty(ML, dtype=np.int64)
    B = 60
    while sub_mod > 1 and (1 << B) >= (2 ** 63) // sub_mod:
        B -= 1
    if B < 1:
        B = 1
    base_cum = np.left_shift(np.int64(1), np.arange(B, dtype=np.int64))  # [1,2,..,2^(B-1)]
    cur = 1
    t = 0
    while t < ML:
        L = min(B, ML - t)
        out[t:t + L] = (cur * base_cum[:L]) % sub_mod
        cur = int((cur * (1 << L)) % sub_mod)
        t += L
    return out


# ----------------------------------------------------------------------------
# Precomputed group structure on Z/3^n:  valuation shells + discrete logs
# ----------------------------------------------------------------------------
class GroupStructure:
    """
    For a fixed n, precompute everything needed to apply 'multiply by 2^{-k}' as a
    per-shell dlog convolution and 'add 3^{n-m}' as an additive roll.

    Attributes
    ----------
    n, modulus (=3^n)
    val[x]        : 3-adic valuation of x in {0,..,n} (val[0]=n by convention)
    shell_idx[L]  : int64 array of the elements x with v_3(x)=L, ORDERED so that
                    shell_idx[L][t] = 3^L * (2^t mod 3^{n-L})   (dlog order)
    M[L]          : length of shell L = 2*3^{n-L-1}  (for L<n); shell n is {0}
    inv2          : 2^{-1} mod 3^n
    """

    def __init__(self, n: int):
        self.n = n
        modulus = 3 ** n
        self.modulus = modulus
        self.inv2 = (modulus + 1) // 2
        self._val = None  # computed lazily (only the xi-dependent schemes need it)

        # shells in dlog order (vectorized via modular cumulative products)
        # shell L = { 3^L * 2^t mod 3^n : t=0..M_L-1 }, ML = 2*3^{n-L-1}
        self.shell_idx: list[np.ndarray] = []
        self.M: list[int] = []
        for L in range(n):
            sub_mod = 3 ** (n - L)           # shell ~ (Z/sub_mod)^x scaled by 3^L
            ML = 2 * 3 ** (n - L - 1)         # = phi(sub_mod) = ord(2 mod sub_mod)
            mult3 = 3 ** L
            # powers of 2 mod sub_mod for t=0..ML-1, then scale by 3^L (mod modulus).
            # Vectorized blocked cumprod (was an O(ML) Python loop); identical output.
            p2 = _powers_of_2_mod(ML, sub_mod)
            idx = (mult3 * p2) % modulus
            self.shell_idx.append(idx)
            self.M.append(ML)
        # shell L=n is just {0}
        self.shell_idx.append(np.array([0], dtype=np.int64))
        self.M.append(1)

        # roll amounts cache (3^{n-m} for m=1..n)
        self.add_const = [pow(3, n - m, modulus) for m in range(1, n + 1)]

    @property
    def val(self) -> np.ndarray:
        """
        3-adic valuation v_3(x) for every x in Z/3^n (v_3(0):=n).  Computed lazily
        and assembled directly from the already-known valuation shells (shell L has
        v_3 == L), which is O(3^n) memory writes -- far cheaper than n full-array
        modulo passes.  Only the xi-dependent (v_3-stratified) schemes consult this;
        the scalar E_n large-n runs never touch it, so they pay nothing for it.
        """
        if self._val is None:
            v = np.empty(self.modulus, dtype=np.int64)
            for L in range(self.n):
                v[self.shell_idx[L]] = L
            v[0] = self.n
            self._val = v
        return self._val


def geom_kernel_dlog(ML: int, s: float) -> np.ndarray:
    """
    Geometric (s-tilted) kernel for the dlog SHIFT induced by x |-> 2^{-k} x on a
    shell of size ML.  Multiply-by-2^{-k} shifts the discrete log by -k, so the
    correlation we need is
        (out)[t] = sum_{k>=1} P_s(a=k) * (law)[(t + k) mod ML]      ... see note
    Wait: if shell value at dlog position t is 2^t, then 2^{-k}*2^t = 2^{t-k},
    i.e. mass at dlog t moves to dlog t-k.  So out[t-k] += law[t], equivalently
        out[u] = sum_{k>=1} P_s(a=k) * law[(u + k) mod ML].
    We return the kernel g over Z/ML with the geometric tail summed EXACTLY (closed
    form per residue class -- NO a_max truncation), then the caller does the
    correlation by FFT.
    """
    if s <= -1.0:
        raise ValueError(
            f"tilt s={s} <= -1: the tilted geometric P_s(a=k) propto 2^{{-k(1+s)}} "
            "is non-summable (ratio 2^{-(1+s)} >= 1). Valid range is s > -1.")
    ratio = 0.5 ** (1.0 + s)          # in (0,1) for s > -1
    Z = ratio / (1.0 - ratio)
    rM = ratio ** ML
    r = np.arange(ML)
    k0 = np.where(r != 0, r, ML)
    g = (ratio ** k0) / (1.0 - rM) / Z
    return g


def _apply_multiply_geom(law: np.ndarray, gs: GroupStructure, s: float,
                         kernel_cache: dict) -> np.ndarray:
    """
    In place-ish: return new law after multiplying the underlying RV by 2^{-a},
    a ~ s-tilted geometric.  Done per valuation shell via FFT correlation in dlog.
    """
    out = np.empty_like(law)
    out[0] = law[0]  # shell L=n is the fixed point {0}
    for L in range(gs.n):
        ML = gs.M[L]
        idx = gs.shell_idx[L]
        sub = law[idx]
        key = (ML, s)
        if key not in kernel_cache:
            kernel_cache[key] = np.fft.rfft(geom_kernel_dlog(ML, s), n=ML)
        ghat = kernel_cache[key]
        # correlation out[u] = sum_k g[k] sub[(u+k) mod ML]
        #   = IFFT( FFT(sub) * conj(FFT(g)) )   (cross-correlation)
        sub_hat = np.fft.rfft(sub, n=ML)
        corr = np.fft.irfft(sub_hat * np.conj(ghat), n=ML)
        out[idx] = corr
    return out


def syracuse_law_fft(n: int, s: float = 0.0) -> np.ndarray:
    """
    Compute the EXACT law of Syrac_s(Z/3^n) as a length-3^n float64 vector via the
    forward W-recursion with per-shell FFT multiplication.  No truncation error
    (geometric tails summed in closed form).  Returns a probability vector summing
    to 1, supported on (Z/3^n)^x.
    """
    gs = GroupStructure(n)
    modulus = gs.modulus
    kernel_cache: dict = {}
    law = np.zeros(modulus, dtype=np.float64)
    law[0] = 1.0  # W_0 = 0 deterministically
    for m in range(1, n + 1):
        c = gs.add_const[m - 1]            # 3^{n-m}
        law = np.roll(law, c)             # additive shift: W_{m-1} -> W_{m-1}+3^{n-m}
        law = _apply_multiply_geom(law, gs, s, kernel_cache)  # multiply by 2^{-a_m}
    # numerical hygiene: clamp tiny negatives from FFT, renormalize
    law = np.clip(law, 0.0, None)
    law /= law.sum()
    return law


def collision_excess_from_law(law: np.ndarray, n: int) -> float:
    """E_n = phi(3^n) CP_n - 1, CP_n = sum_b law[b]^2,  phi(3^n)=2*3^{n-1}."""
    cp = float(np.dot(law, law))
    phi = 2 * 3 ** (n - 1)
    return phi * cp - 1.0


def collision_probability(law: np.ndarray) -> float:
    return float(np.dot(law, law))


def compute_En(n: int, s: float = 0.0) -> dict:
    """
    Convenience: return a dict with n, s, CP_n, E_n, and basic law diagnostics
    (support size on units, max atom, min atom on units).
    """
    law = syracuse_law_fft(n, s=s)
    cp = collision_probability(law)
    phi = 2 * 3 ** (n - 1)
    En = phi * cp - 1.0
    # min/max atom on units (3 nmid b)
    modulus = 3 ** n
    mask_units = np.ones(modulus, dtype=bool)
    mask_units[::3] = False  # multiples of 3 are non-units
    unit_law = law[mask_units]
    return {
        "n": n,
        "s": s,
        "CP_n": cp,
        "phi3n": phi,
        "E_n": En,
        "phi_CP": phi * cp,
        "max_atom": float(law.max()),
        "min_unit_atom": float(unit_law.min()),
        "cn_times_3n": float(unit_law.min()) * modulus,
        "tv_upper": 0.5 * np.sqrt(max(En, 0.0)),
        "mass_on_nonunits": float(law[~mask_units].sum()),
    }
