"""
extremal_search.py — Find UC families with the smallest max-abundance.

Definitions.

  φ(F) := max_x |{A ∈ F : x ∈ A}| / |F|.

Frankl's conjecture asserts φ(F) ≥ 1/2 for every nonempty UC family F
with F ≠ {∅}.  This module exhaustively searches small UC families to
locate the extremal ones — those minimising φ — and catalogues them.

Findings of interest:
  * The minimal achievable φ(F) over all UC F ⊆ 2^[n] with |F| ≥ 2
    appears to be exactly 1/2 (the conjecture is tight).
  * Identifying the families achieving 1/2 gives us a library of
    "hard examples" Phase-2 theory work can refine against.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

from uc_family import (
    Family,
    abundance,
    family_to_sets,
    frequencies,
    ground_set,
    min_abundance_element,
)
from enumerate import all_uc_families


@dataclass(frozen=True)
class ExtremalRecord:
    """A single UC family flagged as (near-)extremal in the search."""
    n: int
    size: int
    abundance: float
    most_abundant_element: int
    family: Family

    def as_sets(self) -> list[list[int]]:
        return [sorted(s) for s in family_to_sets(self.family)]


def search_extremal(
    n: int,
    max_size: int | None = None,
    include_singleton_empty: bool = False,
    keep_top_k: int = 10,
    tol: float = 1e-12,
) -> list[ExtremalRecord]:
    """
    Enumerate UC families on [n] and return those with the lowest abundance.

    Parameters
    ----------
    n
        Ground-set size.
    max_size
        Upper bound on |F|.
    include_singleton_empty
        Whether to consider F = {∅} (degenerate; abundance is undefined / 0).
    keep_top_k
        How many distinct *abundance tiers* (within ``tol``) to keep.
        Setting this to 1 keeps only the minimisers.

    Returns
    -------
    list[ExtremalRecord]
        Sorted by abundance ascending, ties broken by |F| ascending.
    """
    by_phi: dict[float, list[ExtremalRecord]] = defaultdict(list)

    for F in all_uc_families(n, max_size=max_size):
        if not F:
            continue
        if F == frozenset({0}):  # this is F = {∅}
            if not include_singleton_empty:
                continue
            phi = 0.0
            x_star = -1
        else:
            x_star, phi = min_abundance_element(F)
        rec = ExtremalRecord(
            n=n,
            size=len(F),
            abundance=phi,
            most_abundant_element=x_star,
            family=F,
        )
        # Bucket by rounded abundance so ties are clustered.
        key = round(phi / tol) * tol if tol > 0 else phi
        by_phi[key].append(rec)

    # Choose top-k smallest distinct φ tiers.
    sorted_tiers = sorted(by_phi.keys())
    out: list[ExtremalRecord] = []
    for tier in sorted_tiers[:keep_top_k]:
        out.extend(sorted(by_phi[tier], key=lambda r: r.size))
    return out


def extremal_curve(
    n_range: Iterable[int],
    max_size: int | None = None,
) -> dict[int, float]:
    """
    For each n in ``n_range``, return the minimum abundance over UC families
    on [n] (excluding F = {∅}).

    This curve gives the n-by-n picture of how tight Frankl's bound is.
    """
    out: dict[int, float] = {}
    for n in n_range:
        best = float("inf")
        for F in all_uc_families(n, max_size=max_size):
            if not F:
                continue
            if F == frozenset({0}):  # {∅}
                continue
            phi = abundance(F)
            if phi < best:
                best = phi
        out[n] = best if best != float("inf") else float("nan")
    return out


def family_summary(F: Family) -> str:
    """Human-readable summary line for a UC family."""
    sets = [sorted(s) for s in family_to_sets(F)]
    freqs = frequencies(F, ground_set(F))
    return f"|F|={len(F)}  sets={sets}  freqs={freqs}  φ={abundance(F):.6f}"


__all__ = [
    "ExtremalRecord",
    "search_extremal",
    "extremal_curve",
    "family_summary",
]
