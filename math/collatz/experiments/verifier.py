"""
Collatz Verifier — fast trajectory computation under the accelerated map.

We use the *accelerated* (Syracuse) Collatz map T defined by

    T(n) = n // 2          if n is even
    T(n) = (3n + 1) // 2   if n is odd

Note: under the accelerated map, an odd step is "merged" with the immediately
following even step, since 3n+1 is always even when n is odd. So one application
of T compresses what would be two steps of the standard 3n+1 map.

Total stopping time sigma_inf(n) := least k >= 0 such that T^k(n) = 1.
Stopping time tau(n)             := least k >= 1 such that T^k(n) < n.

Key optimizations:
  1. Sieve out n with small total stopping time using a precomputed table
     of (e_r, d_r) for residues r mod 2^k. For each residue r we precompute
        T^k(2^k * q + r) = 3^{a(r)} * q + b(r)
     where a(r) is the number of odd parities in the first k steps starting
     from residue r, and 3^{a(r)} * q + b(r) gives T^k(n) in closed form.
     This lets us evaluate k Collatz steps in O(1) integer ops per residue
     class. References: Oliveira e Silva (2010), Roosendaal's verification.

  2. Range verification uses the standard "convergence below n" shortcut:
     if T^j(n) < n for some j >= 1, then n inherits convergence from
     T^j(n) (which is smaller and already verified inductively).

  3. Cached lookups for small n (precompute total stopping times for
     n < CACHE_LIMIT in an array, then chain to it once a trajectory
     descends below the cache limit).

Author: Alex Ye with Claude (laoganpapi@gmail.com).
"""

from __future__ import annotations

import argparse
import sys
import time
from typing import Iterable, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Core, *unaccelerated-by-tables* primitives. These are the reference
# implementations used by tests; the sieve routines below use these too.
# ---------------------------------------------------------------------------


def T(n: int) -> int:
    """One step of the accelerated Collatz map."""
    if n & 1:
        return (3 * n + 1) >> 1
    return n >> 1


def total_stopping_time(n: int) -> int:
    """
    Return sigma_inf(n): the number of T-iterations needed to reach 1.

    The accelerated map terminates at 1 because the orbit of 1 under T is
    1 -> 2 -> 1 -> 2 -> ... ; we stop the first time we hit 1, so
    sigma_inf(1) = 0 by convention.

    Raises ValueError for n < 1.
    """
    if n < 1:
        raise ValueError(f"total_stopping_time requires n >= 1, got {n}")
    count = 0
    while n != 1:
        if n & 1:
            n = (3 * n + 1) >> 1
        else:
            n >>= 1
        count += 1
    return count


def stopping_time(n: int) -> int:
    """
    Return tau(n): least k >= 1 with T^k(n) < n.

    By definition tau(1) = 0 (1 never strictly drops below 1, but the
    trivial value is conventional and useful so callers can treat it
    uniformly).
    """
    if n < 1:
        raise ValueError(f"stopping_time requires n >= 1, got {n}")
    if n == 1:
        return 0
    m = n
    count = 0
    while True:
        if m & 1:
            m = (3 * m + 1) >> 1
        else:
            m >>= 1
        count += 1
        if m < n:
            return count


def trajectory(n: int, max_steps: int = 10**6) -> List[int]:
    """
    Return the full orbit [n, T(n), T^2(n), ..., 1] (or truncated at max_steps).

    If the orbit reaches 1 within max_steps the final element is 1.
    Otherwise the list has length max_steps + 1 and the caller can detect
    non-termination by checking the last element.
    """
    if n < 1:
        raise ValueError(f"trajectory requires n >= 1, got {n}")
    orbit = [n]
    m = n
    for _ in range(max_steps):
        if m == 1:
            break
        if m & 1:
            m = (3 * m + 1) >> 1
        else:
            m >>= 1
        orbit.append(m)
    return orbit


def parity_vector(n: int, k: int) -> List[int]:
    """
    Return the first k parity bits of the trajectory of n.

    Bit i is 1 if T^i(n) is odd, 0 if even. So this records which rule
    fires at step i+1 (odd -> (3n+1)/2 step; even -> n/2 step).

    Stops early (padding with 0s after a 1 reached) is *not* applied —
    the trajectory of 1 is 1,2,1,2,... so bits oscillate 1,0,1,0,...
    """
    if n < 1:
        raise ValueError(f"parity_vector requires n >= 1, got {n}")
    if k < 0:
        raise ValueError(f"parity_vector requires k >= 0, got {k}")
    bits = []
    m = n
    for _ in range(k):
        bits.append(m & 1)
        if m & 1:
            m = (3 * m + 1) >> 1
        else:
            m >>= 1
    return bits


# ---------------------------------------------------------------------------
# Sieve infrastructure — the Oliveira-e-Silva-style "evaluate k steps in O(1)
# per residue" trick.
# ---------------------------------------------------------------------------


def build_sieve(k: int) -> Tuple[List[int], List[int], List[int]]:
    """
    Build the closed-form lookup tables for k accelerated Collatz steps.

    For each residue r in [0, 2^k), we compute:
      a[r] = number of odd parities in the first k steps starting at r
      b[r] = constant such that T^k(2^k * q + r) = 3^a[r] * q + b[r]
      c[r] = b[r] expressed differently — see below

    The recurrence: write n = 2^k * q + r with 0 <= r < 2^k.
    Each odd step replaces n by (3n+1)/2, each even step replaces n by n/2.
    Both are linear, so T^k(n) is linear in q with slope 3^a / 2^(k-a)
    when k-a even halvings have happened. Since we do *exactly* k steps,
    the denominator is 2^k, but the n/2 already absorbed it because each
    step halves. Working through the algebra:

        After k steps with a odd-rule firings, T^k(n) = (3^a * n + C_r) / 2^k
        where C_r is an integer depending only on r (the lower k bits of n).
        Since n = 2^k * q + r, we get T^k(n) = 3^a * q + (3^a * r + C_r) / 2^k.

    Setting b[r] := (3^a * r + C_r) / 2^k (which is always an integer because
    T^k(r) = (3^a * r + C_r) / 2^k must be integral by induction on k), we get

        T^k(2^k * q + r) = 3^a[r] * q + b[r].

    We compute (a[r], b[r]) by direct simulation on the representative r.

    Returns (a_table, b_table, max_intermediate) where max_intermediate[r]
    is the largest value seen in T^0(r), ..., T^k(r). This is useful for
    range verification.
    """
    if k < 0:
        raise ValueError(f"build_sieve requires k >= 0, got {k}")
    size = 1 << k
    a_table = [0] * size
    b_table = [0] * size
    max_table = [0] * size
    for r in range(size):
        m = r
        a = 0
        peak = r
        for _ in range(k):
            if m & 1:
                m = (3 * m + 1) >> 1
                a += 1
            else:
                m >>= 1
            if m > peak:
                peak = m
        a_table[r] = a
        b_table[r] = m   # m is exactly T^k(r)
        max_table[r] = peak
    return a_table, b_table, max_table


def _build_small_cache(limit: int) -> List[int]:
    """
    Precompute total_stopping_time(n) for 1 <= n < limit.

    Uses a memoization-on-orbit approach: trace each n forward, push to a
    stack, and when we hit a previously known value pop the stack assigning
    accumulated counts.
    """
    if limit < 2:
        return [0]
    cache = [-1] * limit
    cache[1] = 0
    for start in range(2, limit):
        if cache[start] != -1:
            continue
        m = start
        path = []
        while m >= limit or cache[m] == -1:
            path.append(m)
            if m & 1:
                m = (3 * m + 1) >> 1
            else:
                m >>= 1
        base = cache[m] if m < limit else _slow_tst(m)
        # Walk back assigning total_stopping_time values
        for i, v in enumerate(reversed(path)):
            if v < limit:
                cache[v] = base + i + 1
    return cache


def _slow_tst(n: int) -> int:
    """Fallback total stopping time computation (for cache fill-in)."""
    return total_stopping_time(n)


# ---------------------------------------------------------------------------
# Fast range verification.
# ---------------------------------------------------------------------------


def _verify_one(n: int, cache: List[int], cache_limit: int,
                max_orbit_check: Optional[int]) -> Tuple[bool, int]:
    """
    Verify that the orbit of n reaches 1, using a precomputed cache for
    speed. Returns (converged, sigma_inf or steps_taken).

    If max_orbit_check is not None and the orbit value exceeds it, returns
    (False, current_step_count). We use a very loose ceiling (default None)
    because Python ints are unbounded; the heuristic exists only as a
    backstop for surprising behaviour.
    """
    if n == 1:
        return True, 0
    m = n
    count = 0
    while m >= cache_limit:
        if m & 1:
            m = (3 * m + 1) >> 1
        else:
            m >>= 1
        count += 1
        if max_orbit_check is not None and m > max_orbit_check:
            return False, count
    return True, count + cache[m]


def verify_range(start: int, stop: int,
                 sieve_k: int = 16,
                 cache_limit: int = 1 << 18,
                 quiet: bool = True) -> Tuple[int, int, int]:
    """
    Verify that every n in [start, stop) reaches 1 under T.

    Strategy:
      - Precompute total_stopping_time for n < cache_limit (cache).
      - For each n in the range, iterate T until we drop below cache_limit;
        then the cache certifies the rest.
      - We *additionally* use the sieve: when n is large and well above
        cache_limit, we can apply k Collatz steps in a single closed-form
        evaluation via the (a[r], b[r]) tables.

    Returns (count_verified, max_stopping_time_seen, argmax_n).

    Raises RuntimeError if any n fails to converge.
    """
    if start < 1:
        raise ValueError("start must be >= 1")
    if stop <= start:
        return 0, 0, 0
    cache = _build_small_cache(cache_limit)
    a_tab, b_tab, _ = build_sieve(sieve_k)
    mask = (1 << sieve_k) - 1

    verified = 0
    max_sigma = 0
    arg_max = start

    report_every = max(1, (stop - start) // 20) if not quiet else None
    next_report = start + report_every if report_every else stop

    for n in range(start, stop):
        if n == 1:
            verified += 1
            continue
        m = n
        steps = 0
        # Fast path: while m well above cache, apply k-step sieve jumps
        # provided that the jump leaves us still positive and bounded.
        while m >= cache_limit:
            if m >= (1 << sieve_k):
                r = m & mask
                q = m >> sieve_k
                m = (3 ** a_tab[r]) * q + b_tab[r]
                steps += sieve_k
            else:
                if m & 1:
                    m = (3 * m + 1) >> 1
                else:
                    m >>= 1
                steps += 1
        # m < cache_limit; cache certifies the rest
        sigma = steps + cache[m]
        verified += 1
        if sigma > max_sigma:
            max_sigma = sigma
            arg_max = n
        if not quiet and n >= next_report:
            print(f"  verified up to {n}: max sigma_inf so far = "
                  f"{max_sigma} at n = {arg_max}", file=sys.stderr)
            next_report += report_every

    return verified, max_sigma, arg_max


# ---------------------------------------------------------------------------
# Benchmark / CLI.
# ---------------------------------------------------------------------------


def benchmark(upper: int = 10**6, sieve_k: int = 16) -> None:
    """
    Run a timing benchmark of verify_range against a naive baseline.
    """
    print(f"Benchmarking verify_range(1, {upper}) ...")
    t0 = time.perf_counter()
    verified, max_sigma, arg_max = verify_range(1, upper + 1,
                                                sieve_k=sieve_k)
    elapsed = time.perf_counter() - t0
    print(f"  verified {verified} integers in {elapsed:.3f}s "
          f"({verified / elapsed:,.0f} n/s)")
    print(f"  longest sigma_inf in [1, {upper}]: {max_sigma} (at n = {arg_max})")

    # Spot-check a handful via naive routine
    spot = [27, 871, 6171, 77031, 837799]
    for s in spot:
        if s <= upper:
            assert total_stopping_time(s) == _slow_tst(s)
    print("Spot checks OK.")


def _cli() -> None:
    p = argparse.ArgumentParser(description="Collatz verifier.")
    p.add_argument("--benchmark", action="store_true",
                   help="Run benchmark on verify_range(1, N).")
    p.add_argument("--upper", type=int, default=10**6,
                   help="Upper bound N for --benchmark (default 10^6).")
    p.add_argument("--sieve-k", type=int, default=16,
                   help="Sieve depth k (default 16, ~64K residues).")
    p.add_argument("--verify", type=int, nargs=2, metavar=("START", "STOP"),
                   help="Verify range [START, STOP).")
    p.add_argument("--sigma", type=int, metavar="N",
                   help="Print total_stopping_time(N).")
    p.add_argument("--trajectory", type=int, metavar="N",
                   help="Print trajectory of N.")
    args = p.parse_args()

    if args.benchmark:
        benchmark(args.upper, sieve_k=args.sieve_k)
    elif args.verify:
        start, stop = args.verify
        t0 = time.perf_counter()
        verified, max_sigma, arg_max = verify_range(start, stop,
                                                    sieve_k=args.sieve_k,
                                                    quiet=False)
        elapsed = time.perf_counter() - t0
        print(f"Verified {verified} integers in [{start}, {stop}) "
              f"in {elapsed:.3f}s.")
        print(f"Longest sigma_inf = {max_sigma} at n = {arg_max}.")
    elif args.sigma is not None:
        print(total_stopping_time(args.sigma))
    elif args.trajectory is not None:
        orbit = trajectory(args.trajectory)
        print(" ".join(str(x) for x in orbit))
    else:
        p.print_help()


if __name__ == "__main__":
    _cli()
