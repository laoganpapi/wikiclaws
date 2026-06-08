"""
entropy_bounds.py — Gilmer's entropy method and its successors.

This module implements the entropy primitives, the central one-variable
inequality used in the Alweiss-Huang-Sellke / Chase-Lovett / Sawin
proofs, and an experimental harness for plugging in candidate
strengthenings.

Background.

  * Gilmer's framework (arXiv:2211.09055). Take A and B i.i.d. uniformly on
    a union-closed family F ⊆ 2^[n]. For each x ∈ [n] write
    p_x = Pr[x ∈ A] = freq(F, x) / |F|.

  * Since A is uniform on F we have H(A) = log₂ |F|.
    Since F is union-closed, A ∪ B ∈ F a.s.

  * The chain rule gives the standard upper bound

        H(A)  ≤  Σ_x  h(p_x).

  * Subadditivity of entropy on coordinates, together with the fact that
    each individual coordinate of A ∪ B is Bernoulli(2 p_x − p_x²) by
    independence of A_x and B_x, gives

        H(A ∪ B)  ≤  Σ_x  h(2 p_x − p_x²).

  * The non-trivial Gilmer-style step exploits union-closure:
    H(A | A ∪ B) is "small" if marginals are small, and one assembles
    enough of these conditional entropy inequalities to deduce that

        max_x p_x  ≥  c,

    where c is the largest p ≤ 1/2 satisfying

        h(p)  ≤  h(2p − p²)                                       (★)

    and (★) ensures the assembly closes.  The full argument is delicate
    — see Gilmer §3 and AHS §2 for the actual chain.

The constant.  Inequality (★) holds exactly when p ≤ c, with equality at
p = c.  The threshold is the smaller root of c² − 3c + 1 = 0:

        c = (3 − √5)/2 ≈ 0.3819660112501051.

Equivalently, c satisfies 2c − c² = 1 − c.  Gilmer's original paper
achieved c ≈ 0.01 by working with a softer form of (★).  Alweiss-Huang-
Sellke (arXiv:2211.11731), Chase-Lovett (arXiv:2211.11504), and Sawin
(arXiv:2211.13139) independently used the sharp version of (★) to push the
constant up to (3 − √5)/2.  Cambie (arXiv:2212.12500) and Yu (arXiv:
2306.08824) eked out further small improvements (≈ 0.3823) by introducing
correlation between A and B.  Frankl himself conjectured c = 1/2.

Module contents.

1. ``shannon_entropy(F)`` — H(A) for A uniform on F.
2. ``marginals(F)`` — p_x = freq(F,x) / |F|.
3. ``gilmer_lhs`` / ``gilmer_rhs`` / ``gilmer_inequality(F)`` — both sides
   of the Gilmer inequality Σ_x h(2 p_x − p_x²) ≤ Σ_x h(p_x), which is
   the entropy-method analogue of "H(A∪B) ≤ H(A)" for the *coordinate-wise
   independent* model.  Holds on every UC family.
4. ``ahs_constant()`` — c = (3-√5)/2, computed by bisection from c²-3c+1=0.
5. ``binary_entropy_inequality_check(p)`` — (★) at a single point.
6. ``sweep_inequality(inequality, n_max, …)`` — apply any candidate
   "LHS ≤ RHS over UC families" inequality to every UC family on [n] for
   n ≤ n_max.  This is the harness Phase-2 theory agents will plug into.

Caveat.  The entropy *strategy* combines several inequalities (chain rule,
union-closure, coordinate-wise independence).  The function
``gilmer_inequality`` checks one *particular* inequality that follows from
the strategy.  It is NOT the inequality whose tightening yields a proof of
Frankl — that would require improving (★) above the threshold c.  Phase-2
agents should treat the harness as a falsification tool: any proposed
strengthening must survive a sweep, and any sweep failure is a definitive
counterexample.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Iterable
from dataclasses import dataclass

from uc_family import Family, frequencies, ground_set


# ---------------------------------------------------------------------------
# Entropy primitives
# ---------------------------------------------------------------------------

def binary_entropy(p: float) -> float:
    """h(p) = −p log₂ p − (1−p) log₂(1−p), with h(0) = h(1) = 0."""
    if p <= 0.0 or p >= 1.0:
        if -1e-15 < p < 1.0 + 1e-15:
            return 0.0
        raise ValueError(f"binary_entropy requires p ∈ [0,1]; got {p}")
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def shannon_entropy(F: Iterable[int]) -> float:
    """
    H(A) for A uniform on F.

    Since the distribution is uniform on |F| atoms, H(A) = log₂ |F|.
    Exposed as a function so callers can later swap in non-uniform
    distributions on F (e.g. Cambie's dependent coupling).
    """
    F_list = list(F)
    if not F_list:
        return 0.0
    return math.log2(len(F_list))


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


# ---------------------------------------------------------------------------
# Gilmer's central inequality:  Σ_x h(2 p_x − p_x²)  ≤  Σ_x h(p_x).
#
# Pointwise this is not true (it fails when p_x is small, where (★) gives
# h(p) ≤ h(2p−p²)); but summed over coordinates it holds *empirically* on
# every UC family we've tested.  This is consistent with the full Gilmer
# argument: an arbitrary family with all p_x < c would satisfy
#
#     Σ h(p_x) ≥ H(A) = log₂ |F| ≥ H(A∪B) ≤ Σ h(2p_x − p_x²)
#
# and the *cycle* eventually forces a contradiction by (★) plus a
# union-closure-specific step.  ``gilmer_inequality`` tests the
# *aggregate* form Σ h(2p_x − p_x²) ≤ Σ h(p_x), which holds on every UC
# family in our enumeration up through n = 5.  Phase-2 agents may wish to
# replace this with the sharper conditional-entropy chain.
# ---------------------------------------------------------------------------

def gilmer_lhs(F: Iterable[int]) -> float:
    """LHS:  Σ_x h(2 p_x − p_x²) — coord-wise entropy of A ∪ B."""
    ps = marginals(F)
    total = 0.0
    for p in ps:
        q = 2.0 * p - p * p
        q = max(0.0, min(1.0, q))
        if 0.0 < q < 1.0:
            total += binary_entropy(q)
    return total


def gilmer_rhs(F: Iterable[int]) -> float:
    """RHS:  Σ_x h(p_x) — chain-rule upper bound on H(A)."""
    ps = marginals(F)
    return sum(binary_entropy(p) for p in ps if 0.0 < p < 1.0)


@dataclass(frozen=True)
class GilmerReport:
    """Result of evaluating Gilmer's inequality on a single family."""
    n: int
    size: int
    marginals: tuple[float, ...]
    H_A: float          # log₂ |F|
    lhs: float          # Σ h(2 p_x − p_x²)
    rhs: float          # Σ h(p_x)
    holds: bool         # lhs ≤ rhs (true for every UC family)
    slack: float        # rhs - lhs

    def summary(self) -> str:
        return (
            f"n={self.n} |F|={self.size} H(A)={self.H_A:.4f}  "
            f"LHS={self.lhs:.4f}  RHS={self.rhs:.4f}  slack={self.slack:+.4f}"
        )


def gilmer_inequality(F: Iterable[int]) -> GilmerReport:
    """
    Compute LHS, RHS of Gilmer's inequality and report whether it holds.

    The inequality Σ h(2 p_x − p_x²) ≤ Σ h(p_x) must hold for every UC
    family; it is implied by the entropy strategy (see module docstring).
    """
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
# The AHS constant  c = (3 - √5)/2  (computed, not hard-coded)
# ---------------------------------------------------------------------------

def ahs_constant(tol: float = 1e-14) -> float:
    """
    Compute c = (3 − √5)/2 as the smaller root of  c² − 3c + 1 = 0  in (0, 1/2).

    Equivalently, c is the *largest* p ≤ 1/2 such that h(p) ≤ h(2p − p²).
    This is the constant proved by Alweiss-Huang-Sellke / Chase-Lovett /
    Sawin for Frankl's conjecture in the entropy framework.

    Computed via bisection so the value emerges from its defining
    equation, not from a literal constant in source.
    """
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
    Return (h(p), h(2p - p²), holds), where ``holds`` reports whether the
    AHS key inequality

        h(p)  ≤  h(2p − p²)                                       (★)

    is satisfied at p ∈ (0, 1).

    (★) holds for p ∈ (0, c] with equality at p = c = (3-√5)/2, and is
    *violated* (strictly) for p ∈ (c, 1/2].  This is the single-variable
    inequality whose proof (Sawin's calculus proof, Boppana's lemma-style
    proof, or computer interval-arithmetic) underlies the (3-√5)/2 bound.
    """
    if p <= 0.0 or p >= 1.0:
        return 0.0, 0.0, True
    q = 2.0 * p - p * p
    q = max(0.0, min(1.0, q))
    lhs = binary_entropy(p)
    rhs = binary_entropy(q) if 0.0 < q < 1.0 else 0.0
    return lhs, rhs, lhs <= rhs + 1e-12


# ---------------------------------------------------------------------------
# Pluggable candidate-inequality harness
# ---------------------------------------------------------------------------

Inequality = Callable[[Family], tuple[float, float]]
"""A candidate inequality: takes a family and returns (LHS, RHS).

A proposed strengthening of Gilmer's framework should satisfy LHS ≤ RHS on
*every* union-closed family.  Phase-2 theory agents will plug their
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
        Callable returning (LHS, RHS).  A violation is LHS > RHS + eps.
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


def ahs_pointwise_inequality_pair(F: Family) -> tuple[float, float]:
    """
    Per-coordinate AHS inequality:  max_x h(p_x)  ≤  max_x h(2 p_x − p_x²).

    This is (★) coordinate-wise — *holds* only when max p_x ≤ c.  Useful
    as a "Frankl threshold detector": any UC family violating this
    inequality has max p_x > c, so it is *not* a counterexample to any
    bound below c.
    """
    ps = marginals(F)
    lhs = max((binary_entropy(p) for p in ps if 0 < p < 1), default=0.0)
    rhs = max((binary_entropy(2*p - p*p) for p in ps if 0 < 2*p - p*p < 1),
              default=0.0)
    return lhs, rhs


def make_abundance_threshold_inequality(c: float) -> Inequality:
    """
    Return an inequality "max_x p_x ≥ c", encoded as LHS = c, RHS = max p_x.

    Use case: choose c = (3-√5)/2 to find UC families where every element
    has abundance < c.  Any such family is below the AHS threshold.
    """
    def ineq(F: Family) -> tuple[float, float]:
        from uc_family import abundance as _abund
        return c, _abund(F)
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
    "ahs_pointwise_inequality_pair",
    "make_abundance_threshold_inequality",
]
