"""
uc_family.py — Core data structures for union-closed family experiments.

A family F over ground set [n] = {0, 1, ..., n-1} is represented as a
``frozenset`` of nonnegative Python ints, where each int encodes a subset
of [n] via its binary expansion: bit k set ⇔ element k ∈ subset.

Bitmask representation is chosen because:
  * union  → bitwise OR (single machine instruction).
  * membership tests on individual elements → bit test.
  * frozenset(int) is hashable, so families are first-class hashable values.

For n ≤ 30 the encoding fits in one machine word; for larger n Python's
arbitrary-precision ints take over without code changes.

Notation matches Frankl's union-closed conjecture: F is *union-closed* if
A, B ∈ F implies A ∪ B ∈ F. Frankl conjectures that whenever F is union-closed
and F ≠ {∅}, there exists some element x ∈ [n] contained in at least |F|/2
members of F.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import FrozenSet

# A family is a frozenset of subset-bitmasks.
Family = FrozenSet[int]


# ---------------------------------------------------------------------------
# Encoding helpers
# ---------------------------------------------------------------------------

def set_to_mask(s: Iterable[int]) -> int:
    """Encode a set of nonnegative integers as a bitmask."""
    m = 0
    for x in s:
        if x < 0:
            raise ValueError(f"element {x!r} is negative")
        m |= 1 << x
    return m


def mask_to_set(m: int) -> frozenset[int]:
    """Decode a bitmask into the set of element indices."""
    return frozenset(_iter_bits(m))


def _iter_bits(m: int) -> Iterator[int]:
    """Yield positions of set bits in increasing order."""
    while m:
        low = m & -m  # isolate lowest set bit
        yield low.bit_length() - 1
        m ^= low


def family_from_sets(sets: Iterable[Iterable[int]]) -> Family:
    """Convenience constructor: family from an iterable of iterable sets."""
    return frozenset(set_to_mask(s) for s in sets)


def family_to_sets(F: Family) -> list[frozenset[int]]:
    """Decode a family to a sorted list of frozensets (for display/tests)."""
    return sorted((mask_to_set(m) for m in F), key=lambda s: (len(s), sorted(s)))


def ground_set(F: Family) -> int:
    """Return n such that the family lives on [0, n).  n = 0 if F = {∅} or empty."""
    if not F:
        return 0
    union_all = 0
    for m in F:
        union_all |= m
    return union_all.bit_length()


# ---------------------------------------------------------------------------
# Union-closure
# ---------------------------------------------------------------------------

def is_union_closed(F: Iterable[int]) -> bool:
    """Return True iff F is closed under pairwise union (and hence all unions)."""
    F_set = frozenset(F)
    if not F_set:
        return True  # vacuously closed
    # The empty union (over zero sets) is the empty set; conventionally we do
    # *not* require ∅ ∈ F (Frankl's standard formulation allows or excludes
    # ∅ — the conjecture is unaffected because ∅ contains no elements).
    F_list = list(F_set)
    for i, a in enumerate(F_list):
        for b in F_list[i:]:
            if (a | b) not in F_set:
                return False
    return True


def union_closure(F: Iterable[int]) -> Family:
    """
    Return the smallest union-closed family containing F.

    Implementation: repeatedly take pairwise unions until no new element appears.
    Worst-case O(|F|^2) per round and at most O(log |F|) rounds (each round at
    least doubles the closure or terminates), but in practice termination is
    fast because closures stabilize quickly.
    """
    current = set(F)
    while True:
        added = False
        items = list(current)
        for i, a in enumerate(items):
            for b in items[i + 1:]:
                u = a | b
                if u not in current:
                    current.add(u)
                    added = True
        if not added:
            return frozenset(current)


# ---------------------------------------------------------------------------
# Frequencies / abundance
# ---------------------------------------------------------------------------

def frequency(F: Iterable[int], x: int) -> int:
    """Number of A ∈ F with x ∈ A."""
    bit = 1 << x
    return sum(1 for m in F if m & bit)


def frequencies(F: Iterable[int], n: int | None = None) -> list[int]:
    """Return [frequency(F, 0), …, frequency(F, n-1)]."""
    F_list = list(F)
    if n is None:
        n = ground_set(frozenset(F_list))
    freqs = [0] * n
    for m in F_list:
        mm = m
        while mm:
            low = mm & -mm
            idx = low.bit_length() - 1
            if idx < n:
                freqs[idx] += 1
            mm ^= low
    return freqs


def abundance(F: Iterable[int]) -> float:
    """
    max_x frequency(F, x) / |F|, the maximum element abundance.

    Frankl's conjecture says this is ≥ 1/2 for every nonempty union-closed
    family (excluding the degenerate F = {∅}).  By convention we return
    0.0 when |F| = 0 and 0.0 when F = {∅} (no elements to be abundant).
    """
    F_list = list(F)
    if not F_list:
        return 0.0
    n = ground_set(frozenset(F_list))
    if n == 0:
        return 0.0
    freqs = frequencies(F_list, n)
    return max(freqs) / len(F_list)


def min_abundance_element(F: Iterable[int]) -> tuple[int, float]:
    """
    Return (x*, abundance) for the most abundant element x*.

    The name follows the brief: we want the element with the *most*
    occurrences (which equivalently *minimises* the conjecture's slack).
    Ties are broken by smallest index.

    Raises ``ValueError`` on the degenerate family F = {} or F = {∅}.
    """
    F_list = list(F)
    if not F_list:
        raise ValueError("undefined on empty family")
    n = ground_set(frozenset(F_list))
    if n == 0:
        raise ValueError("undefined on F = {∅}: no elements in ground set")
    freqs = frequencies(F_list, n)
    best_x = max(range(n), key=lambda i: (freqs[i], -i))
    return best_x, freqs[best_x] / len(F_list)


# ---------------------------------------------------------------------------
# Misc utilities (used by the rest of the toolkit)
# ---------------------------------------------------------------------------

def relabel(F: Iterable[int], perm: list[int]) -> Family:
    """
    Apply permutation ``perm`` of [n] to every set in F.

    ``perm[i] = j`` means element i is renamed to j.
    """
    n = len(perm)
    out = set()
    for m in F:
        new = 0
        for i in range(n):
            if (m >> i) & 1:
                new |= 1 << perm[i]
        out.add(new)
    return frozenset(out)


def canonical_form(F: Iterable[int], n: int) -> Family:
    """
    A canonical representative of F's S_n-orbit under relabeling of [n].

    Strategy: sort element indices by (frequency, sorted multiset of subset
    sizes containing them) descending, then pick the lex-smallest family over
    all permutations that respect this signature.  For n ≤ 6 this brute force
    is fine; for larger n we'd switch to a Read-Faradžev-style canonization.

    This is *not* a state-of-the-art nauty-style canonization, but it is
    correct: two families produce the same output iff they are isomorphic
    under relabeling.
    """
    from itertools import permutations
    F_set = frozenset(F)
    if not F_set:
        return F_set
    best: Family | None = None
    for perm in permutations(range(n)):
        cand = relabel(F_set, list(perm))
        cand_key = tuple(sorted(cand))
        if best is None or cand_key < tuple(sorted(best)):
            best = cand
    assert best is not None
    return best


__all__ = [
    "Family",
    "set_to_mask",
    "mask_to_set",
    "family_from_sets",
    "family_to_sets",
    "ground_set",
    "is_union_closed",
    "union_closure",
    "frequency",
    "frequencies",
    "abundance",
    "min_abundance_element",
    "relabel",
    "canonical_form",
]
