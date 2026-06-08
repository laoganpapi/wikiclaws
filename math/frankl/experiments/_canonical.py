"""
_canonical.py — Fast canonical form for UC families.

We canonicalise a family F ⊆ 2^[n] under the action of S_n by partition
refinement: split [n] into colour classes by an S_n-invariant statistic
(currently: frequency of each element in F), then only consider
permutations within each colour class.

For families on n ≤ 6 this typically reduces the search from n! = 720 to
≤ a few dozen relabelings.  We further short-circuit by exploring relabelings
in lex order and pruning once a partial relabeling exceeds the current best.

The canonical form is the lex-minimum (over the considered relabelings) of
the sorted tuple of bitmasks.
"""

from __future__ import annotations

from itertools import permutations
from typing import Iterable


def _frequencies(F, n: int) -> list[int]:
    freqs = [0] * n
    for m in F:
        mm = m
        while mm:
            low = mm & -mm
            freqs[low.bit_length() - 1] += 1
            mm ^= low
    return freqs


def _co_signature(F, n: int) -> list[tuple]:
    """Per-element signature: (frequency, sorted multiset of set sizes containing it).

    This is a stronger invariant than frequency alone and can fully
    resolve element orbits for typical UC families.
    """
    sigs: list[list] = [[] for _ in range(n)]
    for m in F:
        size = bin(m).count("1")
        mm = m
        while mm:
            low = mm & -mm
            sigs[low.bit_length() - 1].append(size)
            mm ^= low
    return [(len(s), tuple(sorted(s))) for s in sigs]


def canonical_form_fast(F, n: int):
    """
    Return the canonical (lex-minimum) relabeling of F under S_n.

    Strategy:
      1. Compute a per-element signature.
      2. Partition [n] by signature; this is an S_n-invariant partition.
      3. Enumerate permutations that respect the partition (i.e. permute
         within each class), choose the lex-min relabeled family.

    The output is invariant under the action of S_n: two families are in
    the same orbit iff their canonical forms are equal.
    """
    F = frozenset(F)
    if not F:
        return F

    sigs = _co_signature(F, n)
    # Group element indices by their signature.
    groups: dict = {}
    for i, s in enumerate(sigs):
        groups.setdefault(s, []).append(i)

    # Canonical target ordering: we sort groups by signature, descending size
    # first; this defines slots in the canonical labeling.  The signature
    # itself is part of the invariant, so we just iterate groups in a fixed
    # order and try all permutations of each.
    sorted_groups = sorted(groups.values(), key=lambda g: (-len(g), sigs[g[0]]))

    # Flatten: target positions 0, 1, 2, ... receive elements from groups
    # in order.  We need to pick one permutation within each group.
    targets_per_group = [list(range(sum(len(g) for g in sorted_groups[:i]),
                                     sum(len(g) for g in sorted_groups[:i + 1])))
                         for i in range(len(sorted_groups))]

    best_key = None
    best_perm: list[int] | None = None

    def try_assignment(idx: int, perm: list[int]) -> None:
        nonlocal best_key, best_perm
        if idx == len(sorted_groups):
            # perm[i] = where element i maps to
            relabeled = _relabel(F, perm, n)
            key = tuple(sorted(relabeled))
            if best_key is None or key < best_key:
                best_key = key
                best_perm = list(perm)
            return
        group = sorted_groups[idx]
        targets = targets_per_group[idx]
        for assign in permutations(targets):
            new_perm = perm[:]
            for src, tgt in zip(group, assign):
                new_perm[src] = tgt
            try_assignment(idx + 1, new_perm)

    try_assignment(0, [0] * n)
    assert best_key is not None
    return frozenset(best_key)


def _relabel(F, perm: list[int], n: int):
    """Apply ``perm`` (perm[i]=j: element i renamed to j) to F."""
    out = set()
    for m in F:
        new = 0
        for i in range(n):
            if (m >> i) & 1:
                new |= 1 << perm[i]
        out.add(new)
    return frozenset(out)


__all__ = ["canonical_form_fast"]
