"""
entropy_bounds.py — Gilmer's entropy method and its successors.

Background (all of this is well-documented in the literature; see
``literature/survey.md`` once written).

Gilmer's framework (arXiv:2211.09055).  Take A and B independent and
identically distributed uniformly on a union-closed family F ⊆ 2^[n].
Each element x ∈ [n] has *marginal* p_x = Pr[x ∈ A] = freq(x) / |F|.
Since F is union-closed, A ∪ B is also in F, so

    H(A ∪ B)  ≤  H(A)  =  log₂ |F|.

Computing H(A ∪ B) directly is hard, but Gilmer bounds it below by a
*sum* of binary entropies of independent coordinates:

    H(A ∪ B)  ≥  Σ_x h(2 p_x − p_x²),

where h(t) = −t log₂ t − (1−t) log₂(1−t) is the binary entropy.

On the other hand, since A's coordinates are *not* independent under the
uniform-on-F distribution, the chain rule gives

    H(A)  ≤  Σ_x h(p_x).

Combining the two:

    Σ_x h(2 p_x − p_x²)  ≤  Σ_x h(p_x).                       (*)

If every coordinate has p_x < c, where c is the threshold beyond which
h(2t − t²) > 2 h(t) (so 2 h(t) ≤ h(2t − t²) ⇔ … no, see below), then (*)
yields a contradiction, proving that *some* p_x ≥ c — i.e., some element
is in at least a c-fraction of F.

The critical constant.  The threshold c is the supremum of p ∈ (0, 1/2]
with h(2p − p²) ≥ 2 h(p).  This c is also characterised algebraically
as the smaller root of

    c² − 3c + 1 = 0,            i.e.       c = (3 − √5) / 2 ≈ 0.3819660.

Gilmer's original paper achieved c ≈ 0.01 by working through a weaker
form of (*).  Alweiss-Huang-Sellke (arXiv:2211.11731), Chase-Lovett
(arXiv:2211.11504), and Sawin (arXiv:2211.13139) all independently
pushed the constant up to (3 − √5)/2.  Cambie (arXiv:2212.12500) and
Yu (arXiv:2306.08824) shaved tiny further amounts; the current world
record is around 0.3823 with no improvement having broken 0.39.

The "Frankl frontier" is c = 1/2.  The entropy method is bottlenecked
by inequality (*) being tight near p_x = 1/2 along the *Bernoulli(1/2)*
direction.

What this module provides:

1. ``shannon_entropy(F)`` — H(A) for A uniform on F.
2. ``gilmer_lhs / gilmer_rhs / gilmer_inequality(F)`` — both sides of (*).
3. ``ahs_constant()`` — the constant (3-√5)/2 computed (not hard-coded).
4. ``binary_entropy / binary_entropy_inequality_check`` — h(2p-p²) vs 2h(p).
5. ``check_candidate_inequality(F, lhs, rhs)`` — plug in a conjectured
   improved inequality and check it on F.  The Phase-2 theory agents will
   use this to falsify or empirically support proposed strengthenings.
6. ``sweep_inequality(inequality, n_max, …)`` — apply such a check to
   every UC family up to size n_max, returning any counterexample found.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Iterable
from dataclasses import dataclass

from uc_family import Family, frequencies, ground_set


# ---------------------------------------------------------------------------
# Entropy primitives
# ---------------------------------------------------------------------------

LN2 = math.log(2.0)


def binary_entropy(p: float) -> float:
    """h(p) = -p log2 p - (1-p) log2 (1-p), with h(0) = h(1) = 0."""
    if p <= 0.0 or p >= 1.0:
        # Guard against tiny negative floats from arithmetic.
        if -1e-15 < p < 1.0 + 1e-15:
            return 0.0
        raise ValueError(f"binary_entropy requires p ∈ [0,1]; got {p}")
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def shannon_entropy(F: Iterable[int]) -> float:
    """
    H(A) for A uniform on F.  Since the distribution is uniform on |F|
    atoms, H(A) = log2 |F| exactly.

    We expose this as a function (rather than inlining log2 |F|) so callers
    can later swap in non-uniform distributions if desired.
    """
    F_list = list(F)
    if not F_list:
        return 0.0
    return math.log2(len(F_list))


# ---------------------------------------------------------------------------
# Gilmer inequality
# ---------------------------------------------------------------------------

def marginals(F: Iterable[int], n: int | None = None) -> list[float]:
    """p_x = freq(F, x) / |F| for x = 0, …, n-1."""
    F_list = list(F)
    if not F_list:
        return []
    if n is None:
        n = ground_set(frozenset(F_list))
    if n == 0:
        return []
    freqs = frequencies(F_list, n)
    m = len(F_list)
    return [f / m for f in freqs]


def gilmer_lhs(F: Iterable[int]) -> float:
    """
    LHS of inequality (*):  Σ_x h(2 p_x − p_x²).

    This is Gilmer's lower bound on H(A ∪ B) coming from coordinate-wise
    independence of the union.  See arXiv:2211.09055, eq. (4) (with the
    small adjustment in Alweiss-Huang-Sellke eq. (1.4)).
    """
    ps = marginals(F)
    total = 0.0
    for p in ps:
        q = 2.0 * p - p * p
        # Numerical guards.
        q = max(0.0, min(1.0, q))
        total += binary_entropy(q) if 0.0 < q < 1.0 else 0.0
    return total


def gilmer_rhs(F: Iterable[int]) -> float:
    """
    RHS of inequality (*):  Σ_x h(p_x).

    This is the chain-rule upper bound on H(A) = log2 |F| obtained by
    dropping conditioning — the *largest* the RHS can be.  Gilmer's
    inequality is the assertion ``gilmer_lhs(F) ≤ gilmer_rhs(F)`` for
    every UC family F.
    """
    ps = marginals(F)
    return sum(binary_entropy(p) for p in ps if 0.0 < p < 1.0)


@dataclass(frozen=True)
class GilmerReport:
    """Result of evaluating Gilmer's inequality on a single family."""
    n: int
    size: int
    marginals: tuple[float, ...]
    H_A: float
    lhs: float        # Σ h(2p - p^2)  (lower bound on H(A∪B))
    rhs: float        # Σ h(p)         (upper bound on H(A))
    holds: bool       # lhs ≤ rhs (true for UC families)
    slack: float      # rhs - lhs

    def summary(self) -> str:
        return (
            f"n={self.n} |F|={self.size} H(A)={self.H_A:.4f}  "
            f"LHS={self.lhs:.4f}  RHS={self.rhs:.4f}  slack={self.slack:+.4f}"
        )


def gilmer_inequality(F: Iterable[int]) -> GilmerReport:
    """Compute LHS and RHS of (*) and check it holds for F."""
    F_list = list(F)
    n = ground_set(frozenset(F_list))
    ps = marginals(F_list, n)
    lhs = 0.0
    for p in ps:
        q = 2.0 * p - p * p
        q = max(0.0, min(1.0, q))
        if 0.0 < q < 1.0:
            lhs += binary_entropy(q)
    rhs = sum(binary_entropy(p) for p in ps if 0.0 < p < 1.0)
    return GilmerReport(
        n=n,
        size=len(F_list),
        marginals=tuple(ps),
        H_A=shannon_entropy(F_list),
        lhs=lhs,
        rhs=rhs,
        holds=lhs <= rhs + 1e-12,
        slack=rhs - lhs,
    )


# ---------------------------------------------------------------------------
# The constant c = (3 - sqrt(5))/2  (computed, not hard-coded)
# ---------------------------------------------------------------------------

def ahs_constant(tol: float = 1e-14) -> float:
    """
    Compute c = (3 − √5)/2 by bisection on the fixed-point equation
    (1 − p)^2 = p, equivalently p² − 3p + 1 = 0 with p ∈ (0, 1).

    This is the largest p ≤ 1/2 such that the entropy inequality
    h(2p − p²) ≥ 2 h(p) bites along Bernoulli marginals; equivalently
    it is the abundance threshold proved by Alweiss-Huang-Sellke.

    We compute it from the algebraic characterisation rather than
    hard-coding to verify the value emerges naturally.
    """
    # f(p) = p^2 - 3p + 1, has roots (3 ± √5)/2.
    # The smaller root lies in (0, 1/2).
    f = lambda p: p * p - 3.0 * p + 1.0
    lo, hi = 0.0, 0.5
    assert f(lo) > 0 and f(hi) < 0, "wrong bracketing"
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def binary_entropy_inequality_check(p: float) -> tuple[float, float, bool]:
    """
    Return (h(2p - p^2), 2 h(p), holds), where ``holds`` reports whether
    the AHS inequality h(2p - p²) ≥ 2 h(p) is satisfied at p.

    The inequality is true for all p ∈ [0, c], where c = (3 − √5)/2.
    """
    q = 2.0 * p - p * p
    q = max(0.0, min(1.0, q))
    lhs = binary_entropy(q) if 0.0 < q < 1.0 else 0.0
    rhs = 2.0 * binary_entropy(p) if 0.0 < p < 1.0 else 0.0
    return lhs, rhs, lhs >= rhs - 1e-12


# ---------------------------------------------------------------------------
# Pluggable candidate inequality harness
# ---------------------------------------------------------------------------

Inequality = Callable[[Family], tuple[float, float]]
"""A candidate inequality: takes a family and returns (LHS, RHS).

A proposed strengthening of Gilmer's inequality should satisfy LHS ≤ RHS
on *every* union-closed family.  Phase-2 theory agents will plug their
candidate inequalities in here and call :func:`sweep_inequality` to look
for counterexamples on small UC families.
"""


@dataclass(frozen=True)
class SweepResult:
    """Result of sweeping a candidate inequality over all UC families."""
    n: int
    max_size: int | None
    families_checked: int
    counterexamples: list[tuple[Family, float, float]]   # (F, LHS, RHS) with LHS > RHS

    @property
    def passed(self) -> bool:
        return not self.counterexamples

    def summary(self) -> str:
        if self.passed:
            return (
                f"sweep n={self.n} checked {self.families_checked} UC families "
                f"(max_size={self.max_size}): inequality HELD on all"
            )
        worst = max(self.counterexamples, key=lambda t: t[1] - t[2])
        return (
            f"sweep n={self.n} checked {self.families_checked} UC families "
            f"(max_size={self.max_size}): {len(self.counterexamples)} "
            f"counterexamples found.  Worst gap: LHS={worst[1]:.4f} RHS={worst[2]:.4f}"
        )


def sweep_inequality(
    inequality: Inequality,
    n_max: int,
    max_size: int | None = None,
    eps: float = 1e-9,
    stop_at_first: bool = False,
) -> dict[int, SweepResult]:
    """
    Apply ``inequality`` to every UC family on [n] for n = 0, …, n_max.

    Parameters
    ----------
    inequality
        Callable returning (LHS, RHS); a violation is LHS > RHS + eps.
    n_max
        Sweep n = 0 through n = n_max inclusive.
    max_size
        Bound on |F| for enumeration; if None, all sizes are checked.
    eps
        Slack tolerance for floating-point comparisons.
    stop_at_first
        If True, stop sweeping the current n on the first counterexample.

    Returns
    -------
    dict
        Maps n → SweepResult.
    """
    from enumerate import all_uc_families
    out: dict[int, SweepResult] = {}
    for n in range(n_max + 1):
        checked = 0
        counter: list[tuple[Family, float, float]] = []
        for F in all_uc_families(n, max_size=max_size):
            if not F:
                continue
            lhs, rhs = inequality(F)
            checked += 1
            if lhs > rhs + eps:
                counter.append((F, lhs, rhs))
                if stop_at_first:
                    break
        out[n] = SweepResult(
            n=n,
            max_size=max_size,
            families_checked=checked,
            counterexamples=counter,
        )
    return out


# ---------------------------------------------------------------------------
# Canned inequalities ready to be swept
# ---------------------------------------------------------------------------

def gilmer_inequality_pair(F: Family) -> tuple[float, float]:
    """Adapter exposing Gilmer's LHS/RHS as an Inequality."""
    return gilmer_lhs(F), gilmer_rhs(F)


def make_threshold_inequality(c: float) -> Inequality:
    """
    Return an inequality that *would* prove "Frankl with constant c":

        LHS(F)  =  (number of elements with marginal < c) · |F| · 0
        RHS(F)  =  log2 |F|

    That is, the inequality "max_x p_x ≥ c" expressed as LHS ≤ RHS.  This
    is *not* a useful theorem-style inequality; rather it's a test fixture:
    sweeping a candidate constant c lets us empirically locate the
    minimum-abundance UC family at each n.

    Use case: pass c just below 1/2 and look for "violations" — those
    are extremal candidates with max-abundance below c.
    """
    def ineq(F: Family) -> tuple[float, float]:
        from uc_family import abundance as _abund
        phi = _abund(F)
        # Encode "phi >= c" as LHS = c, RHS = phi; violation iff phi < c.
        return c, phi
    return ineq


__all__ = [
    "binary_entropy",
    "shannon_entropy",
    "marginals",
    "gilmer_lhs",
    "gilmer_rhs",
    "gilmer_inequality",
    "GilmerReport",
    "ahs_constant",
    "binary_entropy_inequality_check",
    "Inequality",
    "SweepResult",
    "sweep_inequality",
    "gilmer_inequality_pair",
    "make_threshold_inequality",
]
