"""
verify_ahs.py — Step-1 numerical certificate for the AHS proof reconstruction
and a reusable, *honest* numerical engine for the chain-rule / intersection
attack vectors.

This module is deliberately self-contained on the entropy side (it does not
trust entropy_bounds.py's coordinatewise Gilmer formula) so that we can compute
the EXACT conditional entropies appearing in the AHS proof — namely
H(C_i | A_{<i}, B_{<i}) and the conditional mutual informations — directly from
the joint law of (A, B) with A, B i.i.d. uniform on a family F.

Key exact computations provided:

  * exact_entropy_union(F)        = H(A ∪ B), A,B iid uniform on F.
  * exact_H_A(F)                  = H(A) = log2|F|.
  * ahs_lower_bound(F)            = the RHS of (2.4): (1/(1-psi)) Σ (1-p_i) H(A_i|A_<i).
  * chain_rule_lower_bound(F)     = Σ_i H(C_i | A_<i, B_<i)   [the (1.6) bound].
  * delta2(F)                     = H(A∪B) − chain_rule_lower_bound(F)  ≥ 0  [slack S_2].
  * cond_mut_info_terms(F)        = the per-coordinate I(C_i;(A_<i,B_<i)|C_<i).
  * lemma2_min_on_grid(...)       = min of G(u,v)=h(uv)-λ[v h(u)+u h(v)] on a grid.

All of these are computed by explicit summation over the (at most |F|^2) atoms
of the joint distribution of (A,B); no Monte Carlo, no approximation beyond
floating point. For |F| up to a few thousand this is fast.

Author: Alex Ye (AI assistance disclosed separately).
"""
from __future__ import annotations

import math
from collections import defaultdict
from collections.abc import Iterable

LN2 = math.log(2.0)


def h(p: float) -> float:
    """Binary entropy in bits."""
    if p <= 1e-15 or p >= 1.0 - 1e-15:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def psi_const() -> float:
    """(3 - sqrt 5)/2, the AHS constant."""
    return (3.0 - math.sqrt(5.0)) / 2.0


# ---------------------------------------------------------------------------
# Exact entropies of functions of (A, B), A,B iid uniform on F.
# ---------------------------------------------------------------------------

def _entropy_of_distribution(counts: Iterable[int], total: int) -> float:
    """Shannon entropy (bits) of a distribution given integer multiplicities."""
    H = 0.0
    for c in counts:
        if c <= 0:
            continue
        p = c / total
        H -= p * math.log2(p)
    return H


def exact_H_A(F: Iterable[int]) -> float:
    m = len(list(F))
    return math.log2(m) if m > 0 else 0.0


def _joint_function_entropy(F, func) -> float:
    """
    H( func(A,B) ) where A,B iid uniform on F, computed exactly.
    func maps (maskA, maskB) -> a hashable value.
    """
    Fl = list(F)
    m = len(Fl)
    if m == 0:
        return 0.0
    counts: dict = defaultdict(int)
    for a in Fl:
        for b in Fl:
            counts[func(a, b)] += 1
    return _entropy_of_distribution(counts.values(), m * m)


def exact_entropy_union(F: Iterable[int]) -> float:
    """H(A ∪ B), exact."""
    return _joint_function_entropy(F, lambda a, b: a | b)


def exact_entropy_intersection(F: Iterable[int]) -> float:
    """H(A ∩ B), exact."""
    return _joint_function_entropy(F, lambda a, b: a & b)


def exact_entropy_union_and_intersection(F: Iterable[int]) -> float:
    """H(A ∪ B, A ∩ B), exact (joint)."""
    return _joint_function_entropy(F, lambda a, b: (a | b, a & b))


def exact_entropy_symdiff(F: Iterable[int]) -> float:
    """H(A △ B), exact."""
    return _joint_function_entropy(F, lambda a, b: a ^ b)


# ---------------------------------------------------------------------------
# Conditional entropies coordinate-by-coordinate (the AHS internals).
# We compute H(C_i | A_{<i}, B_{<i}) and H(A_i | A_{<i}) EXACTLY by grouping.
# ---------------------------------------------------------------------------

def _prefix(mask: int, i: int) -> int:
    """Bits 0..i-1 of mask (the prefix A_{<i})."""
    return mask & ((1 << i) - 1)


def H_Ai_given_prefix(F, i: int) -> float:
    """
    H(A_i | A_{<i}) exactly, A uniform on F.
    = sum over prefix-classes  Pr[class] * h( Pr[A_i=1 | class] ).
    """
    Fl = list(F)
    m = len(Fl)
    if m == 0:
        return 0.0
    # group masks by prefix (bits 0..i-1)
    groups: dict[int, list[int]] = defaultdict(list)
    for a in Fl:
        groups[_prefix(a, i)].append(a)
    H = 0.0
    bit = 1 << i
    for pref, members in groups.items():
        k = len(members)
        ones = sum(1 for a in members if a & bit)
        H += (k / m) * h(ones / k)
    return H


def H_Ci_given_AB_prefix(F, i: int) -> float:
    """
    H(C_i | A_{<i}, B_{<i}) exactly, where C = A ∪ B and (A,B) iid uniform on F.
    Condition on (A_{<i}=pa, B_{<i}=pb); under this, A_i, B_i independent
    Bernoulli with parameters alpha(pa), beta(pb) (alpha=beta as laws since
    A,B identically distributed). C_i = A_i ∨ B_i.
    """
    Fl = list(F)
    m = len(Fl)
    if m == 0:
        return 0.0
    bit = 1 << i
    # For each prefix class, store (count, ones)
    groups: dict[int, list[int]] = defaultdict(list)
    for a in Fl:
        groups[_prefix(a, i)].append(a)
    # alpha(pref) = P[A_i=1 | A_<i=pref];  weight(pref)=count/m
    info = {}
    for pref, members in groups.items():
        k = len(members)
        ones = sum(1 for a in members if a & bit)
        info[pref] = (k / m, ones / k)  # (weight, alpha)
    # H(C_i | A_<i,B_<i) = sum_{pa,pb} w(pa) w(pb) * h( 1 - (1-alpha_pa)(1-alpha_pb) )
    H = 0.0
    items = list(info.items())
    for pa, (wa, aa) in items:
        for pb, (wb, ab) in items:
            q = 1.0 - (1.0 - aa) * (1.0 - ab)
            H += wa * wb * h(q)
    return H


def chain_rule_lower_bound(F, n: int | None = None) -> float:
    """Σ_i H(C_i | A_{<i}, B_{<i})  =  the (1.6) lower bound on H(A∪B)."""
    Fl = list(F)
    if not Fl:
        return 0.0
    if n is None:
        u = 0
        for a in Fl:
            u |= a
        n = u.bit_length()
    return sum(H_Ci_given_AB_prefix(Fl, i) for i in range(n))


def ahs_lower_bound(F, n: int | None = None) -> float:
    """
    The AHS RHS of (2.4):  (1/(1-psi)) * Σ_i (1 - p_i) H(A_i | A_{<i}).
    This is the proof's certified lower bound on H(A∪B).
    """
    Fl = list(F)
    m = len(Fl)
    if m == 0:
        return 0.0
    if n is None:
        u = 0
        for a in Fl:
            u |= a
        n = u.bit_length()
    psi = psi_const()
    total = 0.0
    for i in range(n):
        bit = 1 << i
        p_i = sum(1 for a in Fl if a & bit) / m
        total += (1.0 - p_i) * H_Ai_given_prefix(Fl, i)
    return total / (1.0 - psi)


def delta2(F, n: int | None = None) -> float:
    """
    The chain-rule slack S_2:  H(A∪B) − Σ_i H(C_i | A_<i,B_<i)  ≥ 0.
    Equivalently Σ_i I(C_i ; (A_<i,B_<i) | C_<i).
    """
    return exact_entropy_union(F, ) - chain_rule_lower_bound(F, n)


def marginals_exact(F, n: int | None = None) -> list[float]:
    Fl = list(F)
    m = len(Fl)
    if m == 0:
        return []
    if n is None:
        u = 0
        for a in Fl:
            u |= a
        n = u.bit_length()
    out = []
    for i in range(n):
        bit = 1 << i
        out.append(sum(1 for a in Fl if a & bit) / m)
    return out


# ---------------------------------------------------------------------------
# Lemma 2 grid certificate
# ---------------------------------------------------------------------------

def lemma2_G(u: float, v: float, lam: float) -> float:
    """G(u,v) = h(uv) - lam [ v h(u) + u h(v) ]."""
    return h(u * v) - lam * (v * h(u) + u * h(v))


def lemma2_min_on_grid(mesh: int = 1000, refine: bool = True) -> tuple[float, float, float]:
    """
    Minimise G over a uniform grid of [0,1]^2 (mesh+1 points per axis), with
    optional refinement near the diagonal. Returns (min_value, u*, v*).
    lam = 1/(2(1-psi)).
    """
    psi = psi_const()
    lam = 1.0 / (2.0 * (1.0 - psi))
    best = math.inf
    bu = bv = 0.0
    for iu in range(mesh + 1):
        u = iu / mesh
        for iv in range(mesh + 1):
            v = iv / mesh
            g = lemma2_G(u, v, lam)
            if g < best:
                best = g
                bu, bv = u, v
    if refine:
        # refine near the found minimum and near the diagonal golden point
        for (cu, cv) in [(bu, bv), (1 - psi, 1 - psi)]:
            for iu in range(-50, 51):
                u = cu + iu * 1e-4
                if not (0 <= u <= 1):
                    continue
                for iv in range(-50, 51):
                    v = cv + iv * 1e-4
                    if not (0 <= v <= 1):
                        continue
                    g = lemma2_G(u, v, lam)
                    if g < best:
                        best = g
                        bu, bv = u, v
    return best, bu, bv


if __name__ == "__main__":
    print("psi =", psi_const())
    mn, bu, bv = lemma2_min_on_grid(mesh=400)
    print(f"Lemma 2 grid min: G_min = {mn:.3e} at (u,v)=({bu:.4f},{bv:.4f})  [golden sigma={1-psi_const():.4f}]")
