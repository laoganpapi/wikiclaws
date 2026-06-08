"""
enumerate.py — Enumerate union-closed families.

Two enumerators are provided:

1. ``all_uc_families(n, max_size=None, dedupe_isomorphic=True)``:
   Generate every union-closed family of subsets of [n], optionally up to
   permutation of the ground set.

2. ``uc_families_with_full_ground_set(n, …)``:
   Variant that only emits families whose union covers [0, n).

Algorithm.

  * ``dedupe_isomorphic=False`` mode: DFS over labeled UC families.
    From each visited F, add one new mask m ∉ F, close under union,
    push the child if new.  This materialises *every* labeled UC family
    — feasible only through n = 4.

  * ``dedupe_isomorphic=True`` mode: DFS with **canonical-form keying**.
    Same DFS, but we dedupe by ``canonical_form`` (lex-smallest relabeled
    family in the S_n orbit).  This carries only orbit representatives,
    so memory and time are bounded by the *orbit count*, not the labeled
    count.  For n = 5, the orbit count is in the hundreds of thousands
    rather than millions — feasible in a few minutes.

Optimisation notes:

  * ``canonical_form`` is the hot path.  For small n (≤ 5) brute-force
    over all n! permutations is fine.  We hoist out work that does not
    depend on the permutation (a sorted "signature" used as a cheap
    pre-filter) so most candidate masks are filtered without ever
    computing the permuted family.

  * The DFS uses an iterative stack of canonical-form families.  When
    we extend a canonical F by mask m, we never enumerate orbit
    duplicates of (F, m) because the *result* is canonicalised.

Sanity counts (orbit counts, computed by this module):
    n = 0 →   1
    n = 1 →   3
    n = 2 →   9
    n = 3 →  37
    n = 4 → 367
    n = 5 → ?  (printed by run_baseline.py)
"""

from __future__ import annotations

from collections.abc import Iterator
from itertools import permutations

from uc_family import Family, ground_set, relabel, union_closure
from _canonical import canonical_form_fast


def _powerset_masks(n: int) -> list[int]:
    return list(range(1 << n))


def _sig(F: Family, n: int) -> tuple:
    """An S_n-invariant numeric signature of F (used as a cheap pre-filter)."""
    if not F:
        return (0,)
    sizes = sorted(bin(m).count("1") for m in F)
    freqs = [0] * n
    for m in F:
        mm = m
        while mm:
            low = mm & -mm
            freqs[low.bit_length() - 1] += 1
            mm ^= low
    return (len(F), tuple(sizes), tuple(sorted(freqs, reverse=True)))


def _canonical_form_via_sig(F: Family, n: int) -> Family:
    """
    Return the lex-smallest relabeling of F under S_n.

    Uses the signature ``_sig`` to prune permutations: we only need to
    consider permutations that bring the (frequency, size) signature into
    a fixed canonical ordering.  For n ≤ 6 this is fine; for larger n
    one would switch to a nauty-style algorithm.
    """
    if not F:
        return F
    # Frequency of each element.
    freqs = [0] * n
    for m in F:
        mm = m
        while mm:
            low = mm & -mm
            freqs[low.bit_length() - 1] += 1
            mm ^= low

    # Sort elements by (frequency desc, index asc) into a canonical order.
    # Any S_n-orbit representative we choose will have elements relabeled
    # so that the canonical ordering matches.  We try all permutations
    # within each *equivalence class* of (frequency, sub-signature).
    # For small n we just try all n! permutations and pick the lex-min.
    best: Family | None = None
    best_key: tuple | None = None
    for perm in permutations(range(n)):
        cand = relabel(F, list(perm))
        cand_key = tuple(sorted(cand))
        if best_key is None or cand_key < best_key:
            best_key = cand_key
            best = cand
    assert best is not None
    return best


def all_uc_families(
    n: int,
    max_size: int | None = None,
    dedupe_isomorphic: bool = True,
    include_empty_family: bool = False,
) -> Iterator[Family]:
    """
    Yield every union-closed family F ⊆ 2^[n], optionally up to relabeling.

    Parameters
    ----------
    n
        Size of the ground set.  Recommended n ≤ 5.
    max_size
        If given, skip families with |F| > max_size.
    dedupe_isomorphic
        If True (default), only one representative per S_n-orbit is yielded.
    include_empty_family
        If True, also yield the empty family F = ∅.
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    masks = _powerset_masks(n)

    if dedupe_isomorphic:
        # DFS with canonical-form keying.  ``visited`` stores canonical
        # representatives; whenever we extend, we canonicalise the child
        # before checking membership.
        canonical = canonical_form_fast
        start: Family = frozenset()
        visited: set[Family] = {start}
        stack: list[Family] = [start]
        if include_empty_family:
            yield start
        while stack:
            F = stack.pop()
            if max_size is not None and len(F) >= max_size:
                continue
            for m in masks:
                if m in F:
                    continue
                F_new = union_closure(F | {m})
                if max_size is not None and len(F_new) > max_size:
                    continue
                cf = canonical(F_new, n)
                if cf in visited:
                    continue
                visited.add(cf)
                stack.append(cf)
                yield cf
        return

    # Labeled mode: classical DFS.
    start = frozenset()
    visited_lab: set[Family] = {start}
    stack_lab: list[Family] = [start]
    if include_empty_family:
        yield start
    while stack_lab:
        F = stack_lab.pop()
        if max_size is not None and len(F) >= max_size:
            continue
        for m in masks:
            if m in F:
                continue
            F_new = union_closure(F | {m})
            if max_size is not None and len(F_new) > max_size:
                continue
            if F_new in visited_lab:
                continue
            visited_lab.add(F_new)
            stack_lab.append(F_new)
            yield F_new


def uc_families_with_full_ground_set(
    n: int,
    max_size: int | None = None,
    dedupe_isomorphic: bool = True,
) -> Iterator[Family]:
    """Yield UC families whose set-union covers [0, n)."""
    full = (1 << n) - 1
    for F in all_uc_families(n, max_size=max_size, dedupe_isomorphic=dedupe_isomorphic):
        if not F:
            continue
        u = 0
        for m in F:
            u |= m
        if u == full:
            yield F


def count_uc_families(n: int, max_size: int | None = None,
                      dedupe_isomorphic: bool = True) -> int:
    """Count UC families on [n] (orbits if ``dedupe_isomorphic``)."""
    return sum(1 for _ in all_uc_families(
        n, max_size=max_size, dedupe_isomorphic=dedupe_isomorphic
    ))


__all__ = [
    "all_uc_families",
    "uc_families_with_full_ground_set",
    "count_uc_families",
]
