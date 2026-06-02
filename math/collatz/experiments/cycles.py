"""
Search for non-trivial cycles in the accelerated Collatz map T.

Background.
-----------
A "cycle" is a finite orbit of T. The known cycle in positive integers
is the trivial one: 1 -> 2 -> 1 -> 2 -> ... (under T; equivalently the
1 -> 4 -> 2 -> 1 cycle of the standard map).

For the accelerated map, a positive m-cycle is determined by an
m-step parity sequence p = (p_0, ..., p_{m-1}) and corresponds to a
starting value n satisfying

    T^m(n) = n,

i.e.,
    3^k * n + R(p) = 2^m * n              (cycle equation)

where k = sum(p) is the number of odd steps and R(p) is an integer
that depends only on the parity sequence (specifically, R(p) = sum
over odd-index positions of 3^{(odd steps before position)} * 2^{(even
steps after position)}). Hence

    n = R(p) / (2^m - 3^k).

For the cycle to consist of positive integers, n must be a positive
integer and the trajectory must remain positive (no overflow into the
negative trio of cycles -1 -> -1, -5 -> -7 -> -10 -> -5, etc.).

The Steiner-Simons-de Weger framework (Steiner 1977; Simons-de Weger
2005) bounds non-trivial cycle parameters using Baker's theorem on
linear forms in logarithms. In particular, a non-trivial m-cycle
requires k/m to be a particularly good rational approximation to
log_2(3) - 1 / 1 (after some rearrangement). For m < 10^11 the
known bound rules out non-trivial cycles.

What this module does.
----------------------
1. Enumerate parity sequences of length m <= L_max.
2. For each "candidate" sequence (those with 2^m > 3^k), compute n
   from the cycle equation and check whether it's a positive integer
   with a consistent parity sequence.
3. Report any cycle candidates found.

For m up to ~40 the brute force is feasible (about 2^40 sequences,
which is too many — we prune aggressively).

The pruning trick: a true cycle must have its parity sequence equal
to the *actual* parity vector of T iterated on n. So we generate
candidates by starting from n and iterating T until we either close
(found cycle) or go above a bound. This avoids enumerating 2^m
sequences directly.

Author: Alex Ye with Claude.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Set, Tuple

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Cycle equation arithmetic.
# ---------------------------------------------------------------------------


def cycle_n_from_parity(parity: List[int]) -> Optional[int]:
    """
    Given a parity sequence (p_0, ..., p_{m-1}) for T, compute the
    starting value n in Q satisfying the cycle equation T^m(n) = n.

    The recurrence: starting with x_0 = n, x_{i+1} = (3 x_i + 1)/2 if
    p_i = 1, else x_i / 2. Closed form:

        x_m = (3^k / 2^m) * n + S
              where S = sum_{i : p_i = 1} 3^{(odd count before i)} / 2^{m - i}

    Setting x_m = n:
        (1 - 3^k / 2^m) n = S
        n = 2^m * S / (2^m - 3^k)

    The numerator 2^m * S is an integer (because every term in S has a
    factor of 2^{m - i} <= 2^m). The denominator 2^m - 3^k can be 0 if
    2^m = 3^k, which has no positive integer solution, but is sometimes
    near zero -> giant n.

    Returns the integer n if n is a positive integer, else None.
    """
    m = len(parity)
    if m == 0:
        return None
    k = sum(parity)
    denom = (1 << m) - 3 ** k
    if denom == 0:
        return None
    # Compute the numerator 2^m * S
    numer = 0
    odd_before = 0
    for i, p in enumerate(parity):
        if p == 1:
            # contribution: 3^{odd_before} * 2^{i}   (because 2^m * 1/2^{m-i} = 2^i)
            numer += (3 ** odd_before) * (1 << i)
            odd_before += 1
    if denom > 0:
        # 2^m > 3^k, so denom > 0; we need numer > 0 too.
        if numer == 0:
            return None
        if numer % denom != 0:
            return None
        n = numer // denom
        return n if n > 0 else None
    else:
        # 2^m < 3^k => negative denom; cycle would have n < 0. Skip
        # (we're searching for positive cycles only).
        return None


def verify_cycle(n: int, parity: List[int]) -> bool:
    """
    Given a candidate cycle starting value n and parity sequence,
    iterate T m times and confirm
      (a) the iterate returns to n exactly,
      (b) the actual parities match the proposed parity sequence.

    Returns True iff both hold and the cycle stays in the positive
    integers throughout.
    """
    m = n_val = n
    for p in parity:
        actual_p = m & 1
        if actual_p != p:
            return False
        if actual_p:
            m = (3 * m + 1) >> 1
        else:
            m >>= 1
        if m <= 0:
            return False
    return m == n_val


# ---------------------------------------------------------------------------
# Steiner/Simons-de Weger admissibility heuristics.
# ---------------------------------------------------------------------------


def is_steiner_admissible(m: int, k: int) -> bool:
    """
    Necessary condition for a non-trivial cycle with m total steps and
    k odd steps to exist (positive case):

      1. 2^m > 3^k (so denom is positive and orbit can descend).
      2. k / m must be a Diophantine approximation to log(2)/log(3) ~ 0.6309.
      3. m >= 2 (m = 1 only gives the trivial cycle).

    We just check #1 and a *very* loose version of #2 (|k/m - log_2(3)/log_2(3)|
    might be too aggressive; we accept any k with 2^m > 3^k > 2^{m-1}
    which makes |k log_2(3) - m| < 1).

    This isn't a strict admissibility test from Steiner — it's a coarse
    sieve to focus the search.
    """
    if m < 1 or k < 0 or k > m:
        return False
    if (1 << m) <= 3 ** k:
        return False
    # log_2(3) ~ 1.585; k * 1.585 should be close to m
    # We accept if |k * log_2(3) - m| < 1.5 (very loose)
    diff = abs(k * math.log2(3) - m)
    return diff < 1.5


# ---------------------------------------------------------------------------
# Brute search.
# ---------------------------------------------------------------------------


def search_cycles_by_parity(max_m: int = 20,
                            min_m: int = 2,
                            verbose: bool = True) -> List[Dict]:
    """
    Enumerate parity sequences of lengths in [min_m, max_m] and check
    each for a valid positive-integer cycle.

    For each m we only enumerate (k, m) with is_steiner_admissible(m, k);
    within that, we iterate over all C(m, k) parity sequences.
    Total work: sum over admissible (m, k) of C(m, k). For m <= 20 this
    is < 2^20 ~ 1M, feasible.

    Returns a list of dicts describing any candidates that pass the
    n-positivity test.
    """
    from itertools import combinations
    log = (lambda *a, **kw: print(*a, **kw)) if verbose else (lambda *a, **kw: None)
    out = []
    for m in range(min_m, max_m + 1):
        # Determine admissible k values
        candidates_k = [k for k in range(0, m + 1)
                        if is_steiner_admissible(m, k)]
        total_for_m = 0
        for k in candidates_k:
            for odd_positions in combinations(range(m), k):
                parity = [0] * m
                for p in odd_positions:
                    parity[p] = 1
                n = cycle_n_from_parity(parity)
                if n is None or n <= 0:
                    continue
                # Strong test: does the actual iteration close?
                if verify_cycle(n, parity):
                    # Reconstruct full orbit to detect trivial cycle
                    # (which contains 1).
                    orbit_set = set()
                    m_iter = n
                    for _ in range(m):
                        orbit_set.add(m_iter)
                        if m_iter & 1:
                            m_iter = (3 * m_iter + 1) >> 1
                        else:
                            m_iter >>= 1
                    is_trivial = 1 in orbit_set
                    out.append({
                        "m": m, "k": k, "n": n,
                        "parity": parity,
                        "orbit_min": min(orbit_set),
                        "orbit_max": max(orbit_set),
                        "is_trivial": is_trivial,
                    })
                total_for_m += 1
        log(f"  m={m}: examined {total_for_m} parity sequences "
            f"with admissible k {candidates_k}; found {sum(1 for r in out if r['m']==m)} cycle(s)")
    return out


# ---------------------------------------------------------------------------
# Fixed-point search via trajectory.
# ---------------------------------------------------------------------------


def search_cycles_by_orbit(N_max: int, L_max: int = 100,
                           verbose: bool = True) -> List[Dict]:
    """
    Alternative brute search: for each n in [2, N_max], iterate T up to
    L_max steps and check whether the orbit revisits n. If so, we've
    found a cycle containing n.

    This catches cycles whose minimum element is <= N_max, and whose
    period is <= L_max. Quick sanity check for the absence of
    counterexamples below N_max.
    """
    log = (lambda *a, **kw: print(*a, **kw)) if verbose else (lambda *a, **kw: None)
    seen_in_cycle: Set[int] = set()
    cycles_found: List[Dict] = []
    for n in range(2, N_max + 1):
        if n in seen_in_cycle:
            continue
        m = n
        path = []
        for step in range(L_max):
            path.append(m)
            if m & 1:
                m = (3 * m + 1) >> 1
            else:
                m >>= 1
            if m == n:
                # Found a cycle
                cycles_found.append({
                    "min_n": min(path), "length": step + 1, "elements": path,
                })
                seen_in_cycle.update(path)
                break
            if m == 1:
                break  # converged to the trivial cycle, no new cycle
            if m in seen_in_cycle:
                break
    if verbose:
        log(f"  scanned n in [2, {N_max}] up to {L_max} steps; "
            f"found {len(cycles_found)} cycle(s) not equal to {{1,2}}")
    return cycles_found


# ---------------------------------------------------------------------------
# Negative-orbit cycles (sanity check on known small negative cycles).
# ---------------------------------------------------------------------------


def find_known_negative_cycles() -> List[Dict]:
    """
    The standard 3n+1 map has three known negative cycles. Under the
    accelerated map T(n) = n/2 if n even, (3n+1)/2 if n odd, applied to
    negative integers, we have:
      Cycle A:  n = -1     ; T(-1) = (3*(-1)+1)/2 = (-2)/2 = -1.
      Cycle B:  n = -5     ; T(-5) = -7 ; T(-7) = -10 ; T(-10) = -5.
      Cycle C:  n = -17    ; T(-17) = -25, ..., closes at -17.

    We trace these and confirm. This is a unit test on the implementation.
    """
    def trace(start: int, max_steps: int = 200) -> Tuple[List[int], bool]:
        orbit = [start]
        m = start
        for _ in range(max_steps):
            if m % 2 == 0:
                m //= 2
            else:
                m = (3 * m + 1) // 2
            if m == start:
                return orbit + [m], True
            orbit.append(m)
        return orbit, False

    results = []
    for start in (-1, -5, -17):
        orbit, closed = trace(start)
        results.append({"start": start, "orbit": orbit, "closed": closed,
                        "length": len(orbit) - 1 if closed else None})
    return results


# ---------------------------------------------------------------------------
# Pipeline.
# ---------------------------------------------------------------------------


def run_cycle_search(parity_max_m: int = 20,
                     orbit_N_max: int = 10**6,
                     orbit_L_max: int = 1000,
                     verbose: bool = True) -> Dict:
    """
    Full cycle search: parity-based enumeration up to length parity_max_m,
    plus orbit-based search up to N_max with period up to L_max.
    """
    log = (lambda *a, **kw: print(*a, **kw)) if verbose else (lambda *a, **kw: None)
    out: Dict = {}

    log(f"[cycles] parity-based search, m in [2, {parity_max_m}] ...")
    t0 = time.perf_counter()
    parity_candidates = search_cycles_by_parity(parity_max_m, verbose=verbose)
    out["parity_search"] = {
        "candidates": parity_candidates,
        "non_trivial_count": sum(1 for c in parity_candidates
                                 if not c["is_trivial"]),
        "elapsed_seconds": time.perf_counter() - t0,
    }
    log(f"  done in {out['parity_search']['elapsed_seconds']:.2f}s; "
        f"non-trivial cycles found: {out['parity_search']['non_trivial_count']}")

    log(f"[cycles] orbit-based search, n in [2, {orbit_N_max}] ...")
    t0 = time.perf_counter()
    orbit_cycles = search_cycles_by_orbit(orbit_N_max, orbit_L_max,
                                          verbose=verbose)
    out["orbit_search"] = {
        "cycles": orbit_cycles,
        "elapsed_seconds": time.perf_counter() - t0,
    }
    log(f"  done in {out['orbit_search']['elapsed_seconds']:.2f}s; "
        f"cycles found: {len(orbit_cycles)}")

    log(f"[cycles] sanity-check known negative-orbit cycles ...")
    out["negative_cycles"] = find_known_negative_cycles()
    for nc in out["negative_cycles"]:
        log(f"  n = {nc['start']:>3}: closed = {nc['closed']}, length = {nc['length']}")

    return out


def _cli() -> None:
    p = argparse.ArgumentParser(description="Collatz cycle search.")
    p.add_argument("--parity-m", type=int, default=20,
                   help="Max parity sequence length (default 20).")
    p.add_argument("--orbit-n", type=int, default=10**5,
                   help="Max n for orbit-based search (default 10^5).")
    p.add_argument("--orbit-l", type=int, default=1000,
                   help="Max period in orbit search (default 1000).")
    p.add_argument("--json", default=None, help="Output JSON path.")
    args = p.parse_args()
    res = run_cycle_search(args.parity_m, args.orbit_n, args.orbit_l)
    if args.json:
        with open(args.json, "w") as f:
            json.dump(res, f, indent=2)
        print(f"Wrote {args.json}")


if __name__ == "__main__":
    _cli()
