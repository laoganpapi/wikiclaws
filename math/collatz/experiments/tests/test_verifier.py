"""
Tests for verifier.py.

Reference: OEIS A006577 (number of halving and tripling steps to reach 1
in the standard Collatz problem). For the *accelerated* map T used in
this codebase, the corresponding stopping times equal the *standard*
stopping time minus the number of odd-rule applications (since the
accelerated odd step (3n+1)/2 merges the standard's odd step with the
immediately-following halving step).

We hard-code accelerated-map values in this test file. They are derived
by direct computation from the recurrence T(n) = n/2 if even,
(3n+1)/2 if odd, which we have independently verified against the OEIS
A006577 series for the standard map (every standard value we listed was
double-checked: see the cross-check section in the module docstring).
"""

from __future__ import annotations

import os
import sys

import pytest

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from verifier import (
    T, total_stopping_time, stopping_time, trajectory, parity_vector,
    verify_range, build_sieve, _build_small_cache,
)


# ---------------------------------------------------------------------------
# Single-step map T.
# ---------------------------------------------------------------------------


class TestT:
    def test_T_of_even(self):
        assert T(2) == 1
        assert T(4) == 2
        assert T(100) == 50

    def test_T_of_odd(self):
        # T(1) = (3*1+1)/2 = 2
        assert T(1) == 2
        # T(3) = (9+1)/2 = 5
        assert T(3) == 5
        # T(27) = (81+1)/2 = 41
        assert T(27) == 41
        # T(7) = 22/2 = 11
        assert T(7) == 11

    def test_T_preserves_positivity(self):
        for n in range(1, 1000):
            assert T(n) >= 1, f"T({n}) = {T(n)} <= 0"


# ---------------------------------------------------------------------------
# total_stopping_time (accelerated map sigma_infty).
# ---------------------------------------------------------------------------


# Accelerated-map total stopping times. Independently verified by direct
# simulation. These differ from OEIS A006577 (which is the standard map)
# by the number of odd-rule applications.
ACCELERATED_SIGMA_TABLE = {
    1: 0,
    2: 1,
    3: 5,
    4: 2,
    5: 4,
    6: 6,
    7: 11,
    8: 3,
    9: 13,
    10: 5,
    11: 10,
    12: 7,
    13: 7,
    14: 12,
    15: 12,
    16: 4,
    17: 9,
    18: 14,
    19: 14,
    20: 6,
    27: 70,
    28: 13,
    100: 18,
    871: 113,
    6171: 165,
    77031: 221,
    837799: 329,
}


class TestTotalStoppingTime:
    def test_trivial(self):
        assert total_stopping_time(1) == 0

    @pytest.mark.parametrize("n, expected", ACCELERATED_SIGMA_TABLE.items())
    def test_table(self, n: int, expected: int):
        assert total_stopping_time(n) == expected

    def test_invalid_input(self):
        with pytest.raises(ValueError):
            total_stopping_time(0)
        with pytest.raises(ValueError):
            total_stopping_time(-1)

    def test_powers_of_2(self):
        # T applied to 2^k is k steps to reach 1 (just keep halving).
        for k in range(1, 25):
            assert total_stopping_time(1 << k) == k


# ---------------------------------------------------------------------------
# stopping_time tau(n).
# ---------------------------------------------------------------------------


class TestStoppingTime:
    def test_n_eq_1(self):
        assert stopping_time(1) == 0

    def test_n_eq_2(self):
        # 2 -> 1, immediate drop
        assert stopping_time(2) == 1

    def test_n_eq_3(self):
        # 3 -> 5 -> 8 -> 4 -> 2 (drops below 3 at step 4)
        # Accelerated: 3 -> 5 -> 8 -> 4 -> 2 (drops at step 4)
        assert stopping_time(3) == 4

    def test_consistency_with_trajectory(self):
        # For each n, the value at step tau(n) must be < n
        for n in [3, 7, 11, 27, 41, 100, 6171]:
            t = stopping_time(n)
            orbit = trajectory(n, max_steps=t)
            assert orbit[t] < n, f"orbit[{t}] = {orbit[t]} not < {n}"
            # And for steps 1..t-1, orbit values are >= n
            for i in range(1, t):
                assert orbit[i] >= n, \
                    f"n={n}, orbit[{i}] = {orbit[i]} dropped early"

    def test_tau_le_sigma(self):
        for n in range(2, 200):
            assert stopping_time(n) <= total_stopping_time(n)


# ---------------------------------------------------------------------------
# trajectory.
# ---------------------------------------------------------------------------


class TestTrajectory:
    def test_starts_with_n(self):
        for n in [1, 2, 7, 27, 100]:
            assert trajectory(n)[0] == n

    def test_ends_at_one(self):
        for n in [1, 2, 7, 27, 100, 6171]:
            assert trajectory(n)[-1] == 1

    def test_length_matches_sigma(self):
        for n in [2, 7, 27, 100, 6171]:
            orb = trajectory(n)
            assert len(orb) == total_stopping_time(n) + 1

    def test_max_steps_truncation(self):
        # Use a small max_steps and confirm we stop early
        orb = trajectory(27, max_steps=5)
        assert len(orb) == 6   # n + 5 successive iterates
        # The 6th element is T^5(27) — we verify directly
        m = 27
        for _ in range(5):
            m = T(m)
        assert orb[-1] == m

    def test_n_27_known_orbit(self):
        # First few accelerated iterates of 27:
        # 27 -> 41 -> 62 -> 31 -> 47 -> 71 -> 107 -> 161 -> 242 -> 121
        expected_prefix = [27, 41, 62, 31, 47, 71, 107, 161, 242, 121]
        assert trajectory(27)[: len(expected_prefix)] == expected_prefix


# ---------------------------------------------------------------------------
# parity_vector.
# ---------------------------------------------------------------------------


class TestParityVector:
    def test_empty(self):
        assert parity_vector(27, 0) == []

    def test_n_27_first_bits(self):
        # 27 is odd, T(27)=41 is odd, T(41)=62 is even, ...
        # bits: 1, 1, 0, 1, 1, 1, 1, 1, 0, 1
        assert parity_vector(27, 10) == [1, 1, 0, 1, 1, 1, 1, 1, 0, 1]

    def test_bits_are_0_or_1(self):
        bits = parity_vector(1234567, 50)
        assert all(b in (0, 1) for b in bits)
        assert len(bits) == 50

    def test_bit_count_consistent_with_T(self):
        # Reconstruct trajectory from parity and starting value
        n = 27
        bits = parity_vector(n, 20)
        m = n
        for i, b in enumerate(bits):
            assert (m & 1) == b, f"step {i}: m={m} bit={b}"
            if b:
                m = (3 * m + 1) >> 1
            else:
                m >>= 1


# ---------------------------------------------------------------------------
# verify_range.
# ---------------------------------------------------------------------------


class TestVerifyRange:
    def test_small_range(self):
        verified, max_sigma, arg_max = verify_range(1, 101)
        assert verified == 100
        # Independently verified: n=97 holds the record in [1, 100]
        # with accelerated sigma_inf = 75 (standard map step count 118
        # per OEIS A006577).
        assert arg_max == 97
        assert max_sigma == 75

    def test_singleton(self):
        verified, max_sigma, arg_max = verify_range(7, 8)
        assert verified == 1
        assert max_sigma == 11
        assert arg_max == 7

    def test_empty_range(self):
        verified, _, _ = verify_range(10, 10)
        assert verified == 0

    def test_known_max_in_1_to_10000(self):
        _, max_sigma, arg_max = verify_range(1, 10001)
        assert arg_max == 6171
        assert max_sigma == 165

    def test_known_max_in_1_to_100000(self):
        _, max_sigma, arg_max = verify_range(1, 100001)
        # n=77031 holds the record in this range (independently verified)
        # accelerated sigma_inf = 221 (standard sigma = 350 per OEIS).
        assert arg_max == 77031
        assert max_sigma == 221

    def test_matches_direct_computation(self):
        # Spot-check that verify_range agrees with total_stopping_time
        # by recomputing the max
        _, max_sigma, arg_max = verify_range(1, 1001)
        direct = total_stopping_time(arg_max)
        assert direct == max_sigma

    def test_invalid_start(self):
        with pytest.raises(ValueError):
            verify_range(0, 100)


# ---------------------------------------------------------------------------
# Sieve correctness.
# ---------------------------------------------------------------------------


class TestSieve:
    def test_k_0(self):
        a, b, _ = build_sieve(0)
        assert a == [0]
        assert b == [0]   # T^0(0) is 0

    def test_k_1(self):
        # r=0: T(0) is undefined for the positive integer interpretation,
        # but our sieve just computes T iteratively with 0 -> 0 (since 0 is
        # treated as even). So a[0] = 0, b[0] = 0.
        # r=1: 1 is odd, T(1) = 2. a[1] = 1, b[1] = 2.
        a, b, _ = build_sieve(1)
        assert a == [0, 1]
        assert b == [0, 2]

    def test_closed_form_relation(self):
        # T^k(2^k * q + r) = 3^a[r] * q + b[r]
        for k in [4, 6, 8, 10]:
            a, b, _ = build_sieve(k)
            mask = (1 << k) - 1
            for n in [37, 101, 99999, 555555]:
                m = n
                for _ in range(k):
                    if m & 1:
                        m = (3 * m + 1) >> 1
                    else:
                        m >>= 1
                expected = m
                r = n & mask
                q = n >> k
                predicted = (3 ** a[r]) * q + b[r]
                assert predicted == expected, \
                    f"k={k}, n={n}: predicted {predicted}, got {expected}"


# ---------------------------------------------------------------------------
# Small-cache.
# ---------------------------------------------------------------------------


class TestSmallCache:
    def test_cache_matches_direct(self):
        cache = _build_small_cache(1000)
        # cache[n] should equal total_stopping_time(n) for 1 <= n < 1000
        for n in range(1, 1000):
            assert cache[n] == total_stopping_time(n), f"n={n}"

    def test_cache_n1(self):
        cache = _build_small_cache(10)
        assert cache[1] == 0


# ---------------------------------------------------------------------------
# Large-integer trajectory smoke test.
# ---------------------------------------------------------------------------


class TestLargeIntegers:
    def test_no_overflow(self):
        # Python ints are unbounded; verify a big starting value
        n = 10 ** 12 + 1
        # Just verify it terminates and doesn't crash
        sigma = total_stopping_time(n)
        assert sigma > 0
        # And verify it via trajectory
        orb = trajectory(n)
        assert orb[-1] == 1
        assert len(orb) == sigma + 1

    def test_peak_calculation(self):
        # For n=27 the peak in the accelerated trajectory is 4616
        orb = trajectory(27)
        assert max(orb) == 4616
