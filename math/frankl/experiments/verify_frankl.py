"""
verify_frankl.py — Direct verification of Frankl's conjecture on small UC families.

Frankl's conjecture: for every union-closed family F with F ≠ ∅ and F ≠ {∅},
some element x ∈ ⋃F is contained in at least |F|/2 sets of F.

This module enumerates all UC families on [n] for small n, checks the
conjecture on each, and reports any candidate counterexample.  No
counterexample should be found — Frankl is known to hold for |F| ≤ 50
(Vučković-Živković and refinements; see Bošnjak-Marković).
"""

from __future__ import annotations

from dataclasses import dataclass

from uc_family import (
    Family,
    abundance,
    family_to_sets,
    min_abundance_element,
)
from enumerate import all_uc_families


@dataclass(frozen=True)
class VerificationResult:
    n: int
    max_size: int | None
    families_checked: int
    failures: list[Family]
    extremal_abundance: float
    extremal_family: Family | None

    @property
    def all_pass(self) -> bool:
        return not self.failures

    def summary(self) -> str:
        status = "PASS" if self.all_pass else f"FAIL ({len(self.failures)} counterexamples)"
        return (
            f"n={self.n} max_size={self.max_size} checked={self.families_checked}  "
            f"min φ = {self.extremal_abundance:.6f}  →  {status}"
        )


def verify(n: int, max_size: int | None = None) -> VerificationResult:
    """
    Verify Frankl's conjecture on all UC families ⊆ 2^[n] of size ≤ max_size.

    The conjecture asserts ``abundance(F) ≥ 1/2`` for every UC family F
    other than F = ∅ or F = {∅}.  We check this strict bound minus a
    tiny floating-point cushion.
    """
    failures: list[Family] = []
    families_checked = 0
    best_phi = float("inf")
    best_F: Family | None = None
    for F in all_uc_families(n, max_size=max_size):
        if not F:
            continue
        if F == frozenset({0}):  # {∅}
            continue
        families_checked += 1
        phi = abundance(F)
        if phi < best_phi:
            best_phi = phi
            best_F = F
        if phi < 0.5 - 1e-12:
            failures.append(F)
    if best_F is None:
        best_phi = float("nan")
    return VerificationResult(
        n=n,
        max_size=max_size,
        families_checked=families_checked,
        failures=failures,
        extremal_abundance=best_phi,
        extremal_family=best_F,
    )


def verify_range(n_max: int, max_size: int | None = 50) -> dict[int, VerificationResult]:
    """Verify Frankl for n = 0, …, n_max, each with optional |F| ≤ max_size."""
    out: dict[int, VerificationResult] = {}
    for n in range(n_max + 1):
        out[n] = verify(n, max_size=max_size)
    return out


__all__ = ["VerificationResult", "verify", "verify_range"]
