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
        # uc_family.canonical_form (brute force) — slower but used as reference.
        F = family_from_sets([[0], [0, 1], [0, 1, 2]])
        cf = canonical_form(F, 3)
        for perm in [[0, 1, 2], [1, 0, 2], [2, 1, 0], [0, 2, 1]]:
            assert canonical_form(relabel(F, perm), 3) == cf

    def test_canonical_form_distinguishes_non_iso(self):
        F1 = family_from_sets([[], [0], [0, 1]])         # chain
        F2 = family_from_sets([[], [0], [1], [0, 1]])    # square
        assert canonical_form(F1, 2) != canonical_form(F2, 2)

    def test_canonical_form_fast_orbit_invariant(self):
        # canonical_form_fast (used by the enumerator) — must be a true orbit invariant.
        from _canonical import canonical_form_fast
        F = family_from_sets([[0, 1], [0, 2]])
        cf = canonical_form_fast(F, 3)
        from itertools import permutations
        for perm in permutations(range(3)):
            assert canonical_form_fast(relabel(F, list(perm)), 3) == cf

    def test_canonical_form_fast_agrees_with_brute_on_orbit_count(self):
        # canonical_form_fast may pick a *different* canonical rep than canonical_form,
        # but the number of orbits they identify must agree.
        from _canonical import canonical_form_fast
        from enumerate import all_uc_families
        n = 3
        fast_orbits = set()
        brute_orbits = set()
        for F in all_uc_families(n, dedupe_isomorphic=False):
            if not F:
                continue
            fast_orbits.add(canonical_form_fast(F, n))
            brute_orbits.add(canonical_form(F, n))
        assert len(fast_orbits) == len(brute_orbits)


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
        """h(p) ≤ h(2p − p²) for p ∈ (0, c]."""
        c = ahs_constant()
        for p in [0.05, 0.1, 0.2, 0.3, 0.35, c - 1e-3]:
            lhs, rhs, holds = binary_entropy_inequality_check(p)
            assert holds, f"h(p) ≤ h(2p-p²) should hold at p={p}; got h(p)={lhs} h(2p-p²)={rhs}"

    def test_binary_entropy_inequality_equality_at_constant(self):
        """h(p) = h(2p - p²) at p = c, since 2c - c² = 1 - c and h(p) = h(1-p)."""
        c = ahs_constant()
        lhs, rhs, holds = binary_entropy_inequality_check(c)
        assert abs(lhs - rhs) < 1e-9, f"expected equality at p=c; got {lhs} vs {rhs}"

    def test_binary_entropy_inequality_fails_above_constant(self):
        """h(p) > h(2p − p²) for p > c (strictly)."""
        c = ahs_constant()
        for p in [c + 1e-3, 0.42, 0.48, 0.5]:
            lhs, rhs, holds = binary_entropy_inequality_check(p)
            assert not holds, f"h(p) ≤ h(2p-p²) should fail at p={p}; got h(p)={lhs} h(2p-p²)={rhs}"

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


# ---------------------------------------------------------------------------
# vector3_delta2_nonproduct — Δ₂ recapture at a non-product extremizer
# ---------------------------------------------------------------------------

class TestVector3Delta2NonProduct:
    """Load-bearing invariants of the Δ₂-recapture obstruction (theory/
    vector3_delta2_nonproduct.md)."""

    def test_shared_u_delta2_le_ICU_and_per_coord_vanishes(self):
        # Lemma 3: Δ₂ ≤ I(C;U); Cor 4: Δ₂/n → 0 (bounded by H(U)=O(1)).
        from vector3_delta2_nonproduct import SharedUCoupling
        cpl = SharedUCoupling([0.05, 0.2, 0.38, 0.5, 0.7, 0.9], [1 / 6] * 6)
        HU = cpl.H_U()
        for n in (2, 4, 8, 16):
            d2 = cpl.delta2(n)
            icu = cpl.I_C_U(n)
            assert d2 >= -1e-9                      # Δ₂ ≥ 0
            assert d2 <= icu + 1e-9                 # Lemma 3
            assert icu <= HU + 1e-9                 # I(C;U) ≤ H(U)
            assert d2 / n <= HU / n + 1e-12         # per-coord bound
        # per-coordinate Δ₂ strictly shrinks for large n
        assert cpl.delta2(32) / 32 < cpl.delta2(8) / 8

    def test_shared_u_limit_is_diagonal_mixture(self):
        # H(A)/n → E[h(p)], H(C)/n → E[h(u)] (the diagonal U-mixture); the gap
        # decays like H(U)/n, so it shrinks as n grows and is O(H(U)/n).
        from vector3_delta2_nonproduct import SharedUCoupling
        cpl = SharedUCoupling([0.1, 0.3, 0.5, 0.7], [0.25] * 4)
        HU = cpl.H_U()
        r64, r256 = cpl.report(64), cpl.report(256)
        gap64 = abs(r64["H_A_per"] - r64["E_h_p"])
        gap256 = abs(r256["H_A_per"] - r256["E_h_p"])
        assert gap256 < gap64                       # converging to the mixture
        assert gap256 <= HU / 256 + 1e-9            # gap ≤ H(U)/n (H(A)=H(U)+nE[h])
        assert abs(r256["H_union_per"] - r256["E_h_u"]) < 1.5e-2
        assert r256["delta2_per"] < 1.5e-2          # Δ₂/n → 0

    def test_recapture_moves_constant_wrong_way(self):
        # Honest ledger: c_aug (budget H(C)) ≤ c_AHS, equality iff Δ₂=0.
        from vector3_delta2_nonproduct import (SharedUCoupling,
                                               shared_u_augmented_constant)
        cpl = SharedUCoupling([0.1, 0.3, 0.5, 0.7], [0.25] * 4)
        for n in (2, 4, 8):
            d = shared_u_augmented_constant(cpl, n)
            assert d["c_aug"] <= d["c_ahs"] + 1e-9     # wrong-way direction
            assert d["delta2"] >= -1e-9

    def test_budget_mismatch_artifact_is_one_half_on_powerset(self):
        # The dishonest H(A)-budget ledger reproduces the documented 0.5 on 2^[2].
        from vector3_delta2_nonproduct import augmented_constant_iid_family
        F = frozenset(range(1 << 2))  # 2^[2]
        d = augmented_constant_iid_family(F, 2)
        assert abs(d["c_aug_HA"] - 0.5) < 1e-9          # the artifact
        assert d["delta2"] < 1e-9                        # Δ₂=0 (product)
        assert abs(d["c_aug_HC"] - d["c_ahs"]) < 1e-9    # honest == AHS when Δ₂=0

    def test_certification_gate_flips_at_psi(self):
        # The Sawin lower bound (S_c) is valid iff c ≤ ψ.
        from vector3_delta2_nonproduct import sawin_lower_bound_min, PSI
        assert sawin_lower_bound_min(PSI - 1e-2)[0] >= -1e-6   # valid below ψ
        assert sawin_lower_bound_min(PSI)[0] >= -1e-6          # valid at ψ
        assert sawin_lower_bound_min(PSI + 1e-2)[0] < -1e-4    # INVALID above ψ

    def test_correlated_crossover_psi_at_rho_zero(self):
        # ρ=0 gives exactly ψ; ρ>0 raises (the trap), ρ<0 lowers.
        from vector3_delta2_nonproduct import correlated_crossover, PSI
        assert abs(correlated_crossover(0.0) - PSI) < 1e-4
        assert correlated_crossover(0.3) > PSI + 1e-2
        assert correlated_crossover(-0.3) < PSI - 1e-2


class TestLatticeAttack:
    """Lattice-structural view (lattice.py, lattice_cone.py): invariants and the
    abundance-is-not-a-lattice-invariant obstruction."""

    def test_known_lattice_invariants(self):
        import lattice as Lat
        from uc_family import family_from_sets
        B2 = family_from_sets([[], [0], [1], [0, 1]])
        M3 = family_from_sets([[], [0, 1], [0, 2], [1, 2], [0, 1, 2]])
        N5 = family_from_sets([[], [0], [0, 1], [1, 2], [0, 1, 2]])
        iB2, iM3, iN5 = Lat.invariants(B2), Lat.invariants(M3), Lat.invariants(N5)
        # B2 distributive; M3 modular non-distributive; N5 non-modular
        assert iB2.distributive and iB2.modular
        assert iM3.modular and not iM3.distributive
        assert (not iN5.modular) and (not iN5.distributive)
        # M3 is semimodular both ways; N5 neither
        assert iM3.lower_semimodular and iM3.upper_semimodular
        assert (not iN5.lower_semimodular) and (not iN5.upper_semimodular)

    def test_join_irreducibles_are_unique_lower_cover(self):
        import lattice as Lat
        from uc_family import family_from_sets
        # chain: every non-bottom element is join-irreducible
        C = family_from_sets([[], [0], [0, 1], [0, 1, 2]])
        els, _, _ = Lat.as_lattice(C)
        assert len(Lat.join_irreducibles(els)) == 3
        # B3: exactly the 3 atoms are join-irreducible
        B3 = family_from_sets([[], [0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1, 2]])
        els3, _, _ = Lat.as_lattice(B3)
        assert len(Lat.join_irreducibles(els3)) == 3

    def test_poonen_statement_holds_small(self):
        # min over JIs of |↑j| ≤ |L|/2 on every UC family n≤4.
        import lattice as Lat
        from enumerate import all_uc_families
        for n in range(5):
            for F in all_uc_families(n):
                if len(F) < 2:
                    continue
                els, _, _ = Lat.as_lattice(F)
                pj = Lat.poonen_min_filter(els)[1]
                assert pj <= len(els) / 2 + 1e-12

    def test_cone_is_lattice_iso_and_pushes_abundance_up(self):
        # The obstruction engine: cone(G) ≅ G (lattice), abundance = 1 − 1/|L|.
        from lattice_cone import cone, boolean_pair
        from lattice_minab import exact_lattice_iso
        import lattice as Lat
        from uc_family import abundance
        for k in range(1, 5):
            low, high = boolean_pair(k)
            assert exact_lattice_iso(low, high)          # same abstract lattice
            assert Lat.invariants(low) == Lat.invariants(high)  # identical invariants
            assert abs(abundance(low) - 0.5) < 1e-12     # cube at 1/2
            assert abs(abundance(high) - (1 - 1.0 / (1 << k))) < 1e-12

    def test_cone_construction_exhaustive_small(self):
        # (C1) UC, (C2) lattice-iso, (C3) abundance=1−1/|L| over all G, n≤3.
        from lattice_cone import check_construction
        total, bad = check_construction(3)
        assert total > 0 and bad == []

    def test_abundance_not_determined_by_invariants(self):
        # Two UC families, identical LatticeInvariants, different abundance.
        import lattice as Lat
        from uc_family import family_from_sets, abundance
        F1 = family_from_sets([[], [0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1, 2]])
        F2 = family_from_sets([[], [0, 3], [1, 3], [2, 3], [0, 1, 3], [0, 2, 3],
                               [1, 2, 3], [0, 1, 2, 3]])
        assert Lat.invariants(F1) == Lat.invariants(F2)
        assert abs(abundance(F1) - 0.5) < 1e-12
        assert abs(abundance(F2) - 0.875) < 1e-12

    def test_boolean_lattices_stay_at_half(self):
        # B_k has abundance exactly 1/2 with #JI=k, width=C(k,⌊k/2⌋) → ∞:
        # no monotone function of coarse invariants can exceed 1/2.
        import lattice as Lat
        from lattice_parametric import boolean
        from uc_family import abundance
        for k in range(1, 7):
            F = boolean(k)
            inv = Lat.invariants(F)
            assert abs(abundance(F) - 0.5) < 1e-12
            assert inv.n_join_irred == k

    def test_height_lower_bound(self):
        # abundance ≥ height/|L| on every UC family n≤4, via the explicit
        # longest-chain-atom witness; certifies Frankl for tall lattices.
        import lattice as Lat
        from enumerate import all_uc_families
        from uc_family import abundance
        certified_tall = 0
        for n in range(5):
            for F in all_uc_families(n):
                if len(F) < 2:
                    continue
                els, _, _ = Lat.as_lattice(F)
                nL = len(els)
                x, freq_x, h = Lat.height_lower_bound_witness(F)
                assert freq_x >= h                       # witness valid
                assert abundance(F) >= h / nL - 1e-12    # the inequality
                if 2 * h >= nL:                          # tall ⇒ Frankl certified
                    assert abundance(F) >= 0.5 - 1e-12
                    certified_tall += 1
        assert certified_tall > 0

    def test_height_bound_tight_on_chains(self):
        # The height bound is TIGHT on chains: abundance = height/|L|.
        import lattice as Lat
        from lattice_parametric import chain
        from uc_family import abundance
        for h in range(1, 7):
            F = chain(h)
            els, _, _ = Lat.as_lattice(F)
            _, freq_x, hh = Lat.height_lower_bound_witness(F)
            assert hh == h
            assert abs(abundance(F) - h / len(els)) < 1e-12


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
