"""
boolean_fourier.py — Walsh-Hadamard / Boolean-Fourier toolkit for UC families.

For a UC family F ⊆ 2^[n], we treat the indicator 1_F : {0,1}^n → {0,1} as a real
function on the Boolean cube and compute its Walsh–Hadamard transform:

    f̂(S) = (1/2^n) Σ_{x ∈ {0,1}^n} f(x) · χ_S(x),     χ_S(x) = (-1)^{|S ∩ x|}.

Convention.  We use the L^2-normalized FOURIER transform (Plancherel-friendly):
Σ_S f̂(S)^2 = E_x[f(x)^2] = |F|/2^n.  This matches O'Donnell "Analysis of Boolean
Functions", Karpas (2017), and the Friedgut/Bourgain/KKL literature.

Key derived quantities, for f = 1_F :
    * Level-k Fourier weight   W^k[f] := Σ_{|S|=k} f̂(S)^2.
    * Influence of coord i     Inf_i(f) := Σ_{S ∋ i} f̂(S)^2.
      For Boolean f this equals (1/2) · Pr_{x ~ {0,1}^n}[f(x) ≠ f(x ⊕ e_i)]
      (with our normalization).  Subtle: O'Donnell defines Inf_i without the 1/2
      via *bias-1* characters χ_i(x) = 1-2x_i and the *uniform* prob measure on
      {-1,+1}^n; we keep BOTH conventions explicit (see ``influence_boolean``).
    * Total influence  I[f] := Σ_i Inf_i(f).
    * Noise stability  Stab_ρ(f) := Σ_S ρ^{|S|} f̂(S)^2.

The fundamental identity used throughout this writeup:

    abundance(i; F) = (f̂(∅) − f̂({i})) / (2 f̂(∅))           (★)

i.e.   f̂({i}) = f̂(∅) · (1 − 2 · abundance_i).

Proof.  Let p = |F|/2^n.  Then f̂(∅) = p, and
   f̂({i}) = (1/2^n) Σ_x (-1)^{x_i} f(x)
          = (1/2^n) (#{A ∈ F : i ∉ A} − #{A ∈ F : i ∈ A})
          = (|F| − 2 · freq_i) / 2^n
          = p · (1 − 2 · abundance_i).

Consequence: Frankl's conjecture, in Fourier language, reads

    ∃ i ∈ [n] :  f̂({i}) ≥ 0       (equivalently, the level-1 mass has a
                                    non-negative singleton).

This file provides:
    * walsh_hadamard(values)      — fast in-place WHT (radix-2 butterfly), O(n·2^n).
    * fourier_spectrum(F, n)      — full spectrum as a dict {S_mask : f̂(S)}.
    * level_weights(F, n)         — W^k[f] for k = 0,…,n.
    * influences(F, n)            — [Inf_0(f), …, Inf_{n-1}(f)].
    * noise_stability(F, n, ρ)    — Σ_S ρ^{|S|} f̂(S)^2.
    * verify_abundance_identity(F, n) — runtime check of (★) against direct count.
"""
from __future__ import annotations

from collections.abc import Iterable

from uc_family import Family, abundance, frequencies, ground_set


# ---------------------------------------------------------------------------
# Walsh–Hadamard transform
# ---------------------------------------------------------------------------

def walsh_hadamard(values: list[float]) -> list[float]:
    """
    In-place radix-2 Walsh–Hadamard transform.

    Input: a length-2^n vector ``values`` indexed by bitmasks 0,…,2^n−1.
    Output: the unnormalized Hadamard transform

        Ĥ(S) = Σ_x (-1)^{|S ∩ x|} · values[x],     S ∈ {0,…,2^n−1}.

    To get the L²-normalized Fourier coefficient divide by 2^n.

    Operates in O(n · 2^n) time.  Returns a new list (does not mutate input).
    """
    n_len = len(values)
    if n_len == 0:
        return []
    # Check power of two
    if n_len & (n_len - 1) != 0:
        raise ValueError(f"length {n_len} is not a power of 2")
    a = list(values)  # copy
    h = 1
    while h < n_len:
        for i in range(0, n_len, h * 2):
            for j in range(i, i + h):
                x = a[j]
                y = a[j + h]
                a[j] = x + y
                a[j + h] = x - y
        h *= 2
    return a


def fourier_spectrum(F: Iterable[int], n: int) -> dict[int, float]:
    """
    Return {S_mask : f̂(S)} for f = 1_F on {0,1}^n.

    Uses the WHT for O(n · 2^n) speed.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    size = 1 << n
    indicator = [0.0] * size
    for m in F:
        if m < 0 or m >= size:
            raise ValueError(f"mask {m} outside [0, 2^{n})")
        indicator[m] = 1.0
    hat_unnorm = walsh_hadamard(indicator)
    inv = 1.0 / size if size else 1.0
    return {S: hat_unnorm[S] * inv for S in range(size)}


def fourier_spectrum_direct(F: Iterable[int], n: int) -> dict[int, float]:
    """
    Direct definition implementation (O(4^n)).  Used only as a sanity check.
    """
    size = 1 << n
    inv = 1.0 / size
    F_list = list(F)
    out: dict[int, float] = {}
    for S in range(size):
        acc = 0
        for m in F_list:
            # parity of |S ∩ m|
            par = bin(S & m).count("1") & 1
            acc += -1 if par else 1
        out[S] = acc * inv
    return out


# ---------------------------------------------------------------------------
# Derived quantities
# ---------------------------------------------------------------------------

def level_weights(F: Iterable[int], n: int) -> list[float]:
    """
    Return [W^0[f], W^1[f], …, W^n[f]] where W^k[f] = Σ_{|S|=k} f̂(S)^2.

    Sanity:  Σ_k W^k[f] = E[f^2] = |F|/2^n.
    """
    spec = fourier_spectrum(F, n)
    weights = [0.0] * (n + 1)
    for S, val in spec.items():
        k = bin(S).count("1")
        weights[k] += val * val
    return weights


def influences(F: Iterable[int], n: int) -> list[float]:
    """
    Fourier influence per coord: Inf_i(f) = Σ_{S ∋ i} f̂(S)^2  (no 1/2 factor).

    For Boolean-valued f and the convention here (L²-normalized over {0,1}^n
    with uniform measure), this equals (1/4) · Pr_x[f(x) ≠ f(x⊕e_i)] when f
    is a {0,1}-valued indicator.  See ``influence_flip_probability``.
    """
    spec = fourier_spectrum(F, n)
    inf = [0.0] * n
    for S, val in spec.items():
        if val == 0.0:
            continue
        v2 = val * val
        for i in range(n):
            if (S >> i) & 1:
                inf[i] += v2
    return inf


def total_influence(F: Iterable[int], n: int) -> float:
    """I[f] = Σ_i Inf_i(f) = Σ_S |S| · f̂(S)^2."""
    spec = fourier_spectrum(F, n)
    return sum(bin(S).count("1") * (v * v) for S, v in spec.items())


def noise_stability(F: Iterable[int], n: int, rho: float) -> float:
    """Stab_ρ(f) = Σ_S ρ^{|S|} f̂(S)^2."""
    spec = fourier_spectrum(F, n)
    return sum((rho ** bin(S).count("1")) * (v * v) for S, v in spec.items())


def singleton_coeffs(F: Iterable[int], n: int) -> list[float]:
    """Return [f̂({0}), f̂({1}), …, f̂({n-1})]."""
    spec = fourier_spectrum(F, n)
    return [spec.get(1 << i, 0.0) for i in range(n)]


def influence_flip_probability(F: Iterable[int], n: int) -> list[float]:
    """
    Direct (non-Fourier) compute of Pr_x[f(x) ≠ f(x ⊕ e_i)] for f = 1_F
    over uniform x ∈ {0,1}^n.  Used as a cross-check.

    Returns ``[p_0, …, p_{n-1}]``.
    """
    size = 1 << n
    F_set = frozenset(F)
    out = [0] * n
    for x in range(size):
        in_F = x in F_set
        for i in range(n):
            y = x ^ (1 << i)
            in_F_y = y in F_set
            if in_F != in_F_y:
                out[i] += 1
    return [c / size for c in out]


# ---------------------------------------------------------------------------
# Identity checks  (cheap; called from tests + reports)
# ---------------------------------------------------------------------------

def verify_abundance_identity(
    F: Iterable[int], n: int, tol: float = 1e-12
) -> tuple[bool, list[tuple[float, float, float]]]:
    """
    Verify  f̂({i}) = f̂(∅) · (1 − 2 · abundance_i)  for each i.

    Returns (ok, rows) where rows[i] = (abundance_i, f̂({i}), f̂(∅)·(1−2·ab_i)).
    """
    F_list = list(F)
    if not F_list:
        return True, []
    size = 1 << n
    p = len(F_list) / size
    spec = fourier_spectrum(F_list, n)
    freqs = frequencies(F_list, n)
    F_size = len(F_list)
    rows: list[tuple[float, float, float]] = []
    ok = True
    for i in range(n):
        ab_i = freqs[i] / F_size
        lhs = spec.get(1 << i, 0.0)
        rhs = p * (1.0 - 2.0 * ab_i)
        rows.append((ab_i, lhs, rhs))
        if abs(lhs - rhs) > tol:
            ok = False
    return ok, rows


# ---------------------------------------------------------------------------
# Parseval / consistency
# ---------------------------------------------------------------------------

def parseval(F: Iterable[int], n: int) -> tuple[float, float]:
    """
    Return (Σ_S f̂(S)^2 , |F|/2^n).  Equal iff convention is correct.
    """
    spec = fourier_spectrum(F, n)
    lhs = sum(v * v for v in spec.values())
    rhs = sum(1 for _ in F) / (1 << n)
    return lhs, rhs


__all__ = [
    "walsh_hadamard",
    "fourier_spectrum",
    "fourier_spectrum_direct",
    "level_weights",
    "influences",
    "total_influence",
    "noise_stability",
    "singleton_coeffs",
    "influence_flip_probability",
    "verify_abundance_identity",
    "parseval",
]
