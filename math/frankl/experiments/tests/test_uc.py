"""
Tests for the Frankl experimental toolkit.

Run with:

    cd math/frankl/experiments
    pytest tests/

Test policy: every claim in ``uc_family.py``, ``enumerate.py``,
``entropy_bounds.py``, and ``extremal_search.py`` should have at least one
test here.  Number-theoretic and entropy-method sanity checks are
*computational* rather than analytical.
"""

from __future__ import annotations

import math
import os
import sys

import pytest

# Allow running pytest from the experiments dir without an editable install.
HERE = os.path.dirname(os.path.abspath(__file__))
EXP_DIR = os.path.dirname(HERE)
if EXP_DIR not in sys.path:
    sys.path.insert(0, EXP_DIR)

from uc_family import (  # noqa: E402
    abundance,
    canonical_form,
    family_from_sets,
    family_to_sets,
    frequencies,
    frequency,
    ground_set,
    is_union_closed,
    mask_to_set,
    min_abundance_element,
    relabel,
    set_to_mask,
    union_closure,
)
from enumerate import all_uc_families, count_uc_families  # noqa: E402
from entropy_bounds import (  # noqa: E402
    ahs_constant,
    binary_entropy,
    binary_entropy_inequality_check,
    gilmer_inequality,
    gilmer_lhs,
    gilmer_rhs,
    marginals,
    shannon_entropy,
    sweep_inequality,
    gilmer_inequality_pair,
)
from extremal_search import extremal_curve, search_extremal  # noqa: E402
from verify_frankl import verify, verify_range  # noqa: E402


# ---------------------------------------------------------------------------
# uc_family: encoding round-trips, ground set
# ---------------------------------------------------------------------------

class TestEncoding:
    def test_set_mask_roundtrip(self):
        for s in [set(), {0}, {0, 2}, {1, 3, 5}]:
            assert mask_to_set(set_to_mask(s)) == frozenset(s)

    def test_set_to_mask_rejects_negatives(self):
        with pytest.raises(ValueError):
            set_to_mask({-1})

    def test_family_constructor(self):
        F = family_from_sets([[], [0], [0, 1], [1, 2]])
        assert len(F) == 4
        sets = family_to_sets(F)
        assert sets == [
            frozenset(),
            frozenset({0}),
            frozenset({0, 1}),
            frozenset({1, 2}),
        ]

    def test_ground_set(self):
        assert ground_set(frozenset()) == 0
        assert ground_set(family_from_sets([[]])) == 0
        assert ground_set(family_from_sets([[0]])) == 1
        assert ground_set(family_from_sets([[0, 4]])) == 5


# ---------------------------------------------------------------------------
# uc_family: closure
# ---------------------------------------------------------------------------

class TestUnionClosure:
    def test_singleton_is_uc(self):
        assert is_union_closed(family_from_sets([[0]]))

    def test_empty_family_is_uc(self):
        assert is_union_closed(frozenset())

    def test_known_uc(self):
        # F = {∅, {0}, {0,1}}, manually union-closed
        F = family_from_sets([[], [0], [0, 1]])
        assert is_union_closed(F)

    def test_known_not_uc(self):
        F = family_from_sets([[0], [1]])  # missing {0,1}
        assert not is_union_closed(F)

    def test_closure_matches_manual(self):
        F = family_from_sets([[0], [1]])
        closed = union_closure(F)
        assert closed == family_from_sets([[0], [1], [0, 1]])
        assert is_union_closed(closed)

    def test_closure_idempotent(self):
        F = family_from_sets([[0], [1], [2]])
        F1 = union_closure(F)
        F2 = union_closure(F1)
        assert F1 == F2

    def test_full_powerset_is_uc(self):
        # 2^[3]
        F = frozenset(range(1 << 3))
        assert is_union_closed(F)
        assert union_closure(F) == F


# ---------------------------------------------------------------------------
# uc_family: frequency & abundance
# ---------------------------------------------------------------------------

class TestFrequency:
    def test_frequency_simple(self):
        F = family_from_sets([[0], [0, 1], [1]])
        assert frequency(F, 0) == 2
        assert frequency(F, 1) == 2
        assert frequency(F, 2) == 0

    def test_frequencies_vector(self):
        F = family_from_sets([[0], [0, 1], [0, 1, 2]])
        assert frequencies(F, 3) == [3, 2, 1]

    def test_abundance(self):
        F = family_from_sets([[0], [0, 1]])
        assert abs(abundance(F) - 1.0) < 1e-12  # element 0 is in both

    def test_abundance_half(self):
        # F = {∅, {0,1}}: element 0 and 1 each in 1 out of 2 → abundance 1/2
        F = family_from_sets([[], [0, 1]])
        assert abs(abundance(F) - 0.5) < 1e-12

    def test_min_abundance_element(self):
        F = family_from_sets([[0], [0, 1], [0, 1, 2]])
        x, phi = min_abundance_element(F)
        assert x == 0
        assert phi == 1.0

    def test_min_abundance_undefined_on_empty(self):
        with pytest.raises(ValueError):
            min_abundance_element(frozenset())
        with pytest.raises(ValueError):
            min_abundance_element(family_from_sets([[]]))


# ---------------------------------------------------------------------------
# uc_family: relabel / canonical_form
# ---------------------------------------------------------------------------

class TestCanonical:
    def test_relabel_identity(self):
        F = family_from_sets([[0], [0, 1]])
        assert relabel(F, [0, 1]) == F

    def test_relabel_swap(self):
        F = family_from_sets([[0], [0, 1]])
        # Swap 0 and 1: {0} becomes {1}, {0,1} stays
        out = relabel(F, [1, 0])
        assert out == family_from_sets([[1], [0, 1]])

    def test_canonical_form_invariant_under_relabel(self):
        F = family_from_sets([[0], [0, 1], [0, 1, 2]])
        cf = canonical_form(F, 3)
        for perm in [[0, 1, 2], [1, 0, 2], [2, 1, 0], [0, 2, 1]]:
            assert canonical_form(relabel(F, perm), 3) == cf

    def test_canonical_form_distinguishes_non_iso(self):
        F1 = family_from_sets([[], [0], [0, 1]])         # chain
        F2 = family_from_sets([[], [0], [1], [0, 1]])    # square
        assert canonical_form(F1, 2) != canonical_form(F2, 2)


# ---------------------------------------------------------------------------
# enumerate
# ---------------------------------------------------------------------------

class TestEnumerate:
    EXPECTED_ORBIT_COUNTS = {0: 1, 1: 3, 2: 9, 3: 37, 4: 367}

    @pytest.mark.parametrize("n", sorted(EXPECTED_ORBIT_COUNTS))
    def test_orbit_counts(self, n):
        assert count_uc_families(n, dedupe_isomorphic=True) == self.EXPECTED_ORBIT_COUNTS[n]

    def test_all_yielded_are_uc(self):
        for F in all_uc_families(3):
            if F:
                assert is_union_closed(F)

    def test_orbit_dedupe_yields_unique_canonicals(self):
        seen = set()
        for F in all_uc_families(3):
            cf = canonical_form(F, 3)
            assert cf not in seen
            seen.add(cf)


# ---------------------------------------------------------------------------
# entropy_bounds
# ---------------------------------------------------------------------------

class TestEntropy:
    def test_binary_entropy_endpoints(self):
        assert binary_entropy(0.0) == 0.0
        assert binary_entropy(1.0) == 0.0
        assert abs(binary_entropy(0.5) - 1.0) < 1e-12

    def test_binary_entropy_symmetric(self):
        for p in [0.1, 0.2, 0.4]:
            assert abs(binary_entropy(p) - binary_entropy(1 - p)) < 1e-12

    def test_shannon_entropy_uniform(self):
        F = family_from_sets([[0], [0, 1], [1]])
        assert abs(shannon_entropy(F) - math.log2(3)) < 1e-12

    def test_ahs_constant_value(self):
        c = ahs_constant()
        # Expected: (3 - √5)/2 ≈ 0.3819660112501051
        expected = (3.0 - math.sqrt(5.0)) / 2.0
        assert abs(c - expected) < 1e-10

    def test_ahs_constant_algebraic(self):
        c = ahs_constant()
        # c satisfies c^2 - 3c + 1 = 0
        assert abs(c * c - 3.0 * c + 1.0) < 1e-10
        # equivalently (1-c)^2 = c
        assert abs((1 - c) ** 2 - c) < 1e-10

    def test_binary_entropy_inequality_holds_below_constant(self):
        c = ahs_constant()
        for p in [0.05, 0.1, 0.2, 0.3, 0.35, c - 1e-3]:
            lhs, rhs, holds = binary_entropy_inequality_check(p)
            assert holds, f"h(2p-p²) >= 2 h(p) should hold at p={p}; got {lhs} vs {rhs}"

    def test_binary_entropy_inequality_fails_above_constant(self):
        c = ahs_constant()
        for p in [c + 1e-3, 0.42, 0.48, 0.5]:
            lhs, rhs, holds = binary_entropy_inequality_check(p)
            assert not holds, f"h(2p-p²) >= 2 h(p) should fail at p={p}"

    def test_gilmer_inequality_on_uc_families(self):
        # Gilmer's inequality LHS ≤ RHS should hold for every UC family.
        # (This is the foundational entropy inequality that powers the bound.)
        violations = 0
        for n in range(4):
            for F in all_uc_families(n):
                if not F:
                    continue
                rep = gilmer_inequality(F)
                if not rep.holds:
                    violations += 1
        assert violations == 0, f"Gilmer's inequality failed on {violations} UC families"

    def test_sweep_inequality_returns_results(self):
        results = sweep_inequality(gilmer_inequality_pair, n_max=3)
        for n, res in results.items():
            assert res.passed, res.summary()


# ---------------------------------------------------------------------------
# extremal_search
# ---------------------------------------------------------------------------

class TestExtremal:
    def test_extremal_curve_at_least_half(self):
        curve = extremal_curve(range(4))
        for n, phi in curve.items():
            if n == 0:
                continue  # nothing nontrivial on empty ground set
            assert phi >= 0.5 - 1e-12, f"Frankl violated at n={n}: φ={phi}"

    def test_search_extremal_returns_minimisers(self):
        recs = search_extremal(3, keep_top_k=1)
        assert recs, "should find at least one extremal record"
        for r in recs:
            assert r.abundance >= 0.5 - 1e-12


# ---------------------------------------------------------------------------
# verify_frankl
# ---------------------------------------------------------------------------

class TestVerify:
    def test_verify_small(self):
        for n in range(4):
            res = verify(n)
            assert res.all_pass, res.summary()

    def test_verify_range(self):
        results = verify_range(3)
        for n, res in results.items():
            assert res.all_pass


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
