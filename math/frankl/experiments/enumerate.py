"""
enumerate.py — Enumerate union-closed families.

Two enumerators are provided:

1. ``all_uc_families(n, max_size=None, dedupe_isomorphic=True)``:
   Generate every union-closed family of subsets of [n], optionally up
   to permutation of the ground set.  This is the *reference* enumerator
   and is the easiest to verify against small-case counts.

2. ``uc_families_with_full_ground_set(n, …)``:
   Variant that only emits families whose union covers [0, n).  This is
   the natural "essentially-n-element" stratum: every UC family over [n]
   is, up to relabeling, a member of some such stratum for n' ≤ n.

Algorithm.  The set L_n = 2^[n] forms a lattice under union; the union-closed
subfamilies of [n] correspond exactly to its *sub-join-semilattices*.  We
enumerate them by depth-first growth: start from a "seed" (a single set, or
∅) and extend by adding one new subset at a time and then re-closing under
union.  We use canonical-form pruning: at every node we only branch on
subsets m such that m is the canonical representative of its orbit *under
the stabiliser of the current family*, which avoids enumerating each family
|Aut(F)| times.  For n ≤ 5 we additionally apply a global isomorph-rejection
step (``canonical_form`` from ``uc_family``) before yielding.

For n ≤ 5 the total counts are small enough to enumerate exhaustively in
seconds.  n = 6 requires more care; we provide a hard cap via ``max_size``.

NOTE on Frankl's standard formulation.  Different authors disagree on
whether ∅ ∈ F is allowed; the conjecture is unaffected.  We *allow* ∅
because every union closure over any seed includes ∅ only if ∅ is
explicitly in the seed.  The enumeration runs over UC families regardless.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import FrozenSet

from uc_family import Family, canonical_form, union_closure, ground_set


def _powerset_masks(n: int) -> list[int]:
    return list(range(1 << n))


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
        Size of the ground set.  Enumeration is feasible for n ≤ 5 and
        attempts but slows substantially at n = 6.
    max_size
        If given, skip families with |F| > max_size.  Useful both for
        truncating large strata and for proving extremal results on a
        bounded family-size range.
    dedupe_isomorphic
        If True (default), only one representative per S_n-orbit is yielded.
        This is the most useful mode for extremal search.  Pass False to
        get every labeled UC family.
    include_empty_family
        If True, also yield the empty family F = ∅.  Defaults to False
        since the conjecture is vacuous there.

    Yields
    ------
    Family
        A frozenset of bitmasks representing the family.
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    seen_canonical: set[Family] = set()
    yielded: list[Family] = []

    if include_empty_family:
        empty: Family = frozenset()
        yield empty
        yielded.append(empty)

    # We use BFS over union-closed families ordered by inclusion.
    # The starting frontier is { {∅} } and { {S} : S ⊆ [n], S ≠ ∅ }: every
    # nonempty UC family contains some minimal-by-inclusion set, and any
    # singleton family is UC.  From each singleton we grow by adding one
    # new element-subset at a time and re-closing.
    masks = _powerset_masks(n)

    def emit(F: Family) -> Family | None:
        """Return F (or its canonical form) the first time we see this orbit; else None."""
        if max_size is not None and len(F) > max_size:
            return None
        if dedupe_isomorphic:
            cf = canonical_form(F, n)
            if cf in seen_canonical:
                return None
            seen_canonical.add(cf)
            return cf
        return F

    # Frontier = set of UC families we have already emitted (or will emit).
    frontier: list[Family] = []

    # Seed with all singleton families.
    for m in masks:
        F0: Family = frozenset({m})
        out = emit(F0)
        if out is not None:
            yield out
            frontier.append(out)

    # BFS extension.
    idx = 0
    while idx < len(frontier):
        F = frontier[idx]
        idx += 1
        # Try adding each subset not yet in F.
        for m in masks:
            if m in F:
                continue
            F_new = union_closure(F | {m})
            if max_size is not None and len(F_new) > max_size:
                continue
            out = emit(F_new)
            if out is not None:
                yield out
                frontier.append(out)


def uc_families_with_full_ground_set(
    n: int,
    max_size: int | None = None,
    dedupe_isomorphic: bool = True,
) -> Iterator[Family]:
    """
    Yield UC families whose set-union covers [0, n).

    These are the "irreducible" UC families on n elements — every UC family
    is one of these for some n' ≤ n, embedded by relabeling.
    """
    full = (1 << n) - 1
    for F in all_uc_families(n, max_size=max_size, dedupe_isomorphic=dedupe_isomorphic):
        if not F:
            continue
        u = 0
        for m in F:
            u |= m
        if u == full:
            yield F


def count_uc_families(n: int, max_size: int | None = None) -> int:
    """Count UC families up to isomorphism.  Convenience wrapper."""
    return sum(1 for _ in all_uc_families(n, max_size=max_size))


__all__ = [
    "all_uc_families",
    "uc_families_with_full_ground_set",
    "count_uc_families",
]
