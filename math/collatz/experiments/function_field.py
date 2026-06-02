"""
Function-field analog of the Collatz map over F_p[T].

We pick ONE concrete analog (stated precisely below) and study its
orbit structure. The choice is dictated by what makes the analog
*structurally faithful* (an analog of "n -> n/2 if 2 | n; n -> (3n+1)/2 else")
while remaining computable.

  Setup (the chosen analog):
    Fix a prime p (default p = 2 means F_2[T]; we also support p=3, p=5).
    Replace 2 with T (the indeterminate), and replace "3n+1" with
    "((T+1) * f(T) + 1) / T" -- the unique smallest analog where:
      - "even" means T | f(T)              <-> 2 | n
      - the "halve" branch divides by T    <-> divide by 2
      - the "odd" branch multiplies by (T+1) and adds 1 so that the
        result is divisible by T          <-> (3n+1) is divisible by 2

    Concretely:
      Phi : F_p[T] -> F_p[T]
        Phi(f) = f / T                       if T | f
        Phi(f) = ((T+1) * f + 1) / T         else

    Why (T+1)*f + 1 and not other choices?
      - We need (T+1)*f + 1 to be divisible by T when T does NOT divide f.
        Reducing mod T: ((T+1)*f + 1) mod T = (0+1)*f(0) + 1 = f(0) + 1.
        So we need f(0) = -1 mod T. In F_p[T], f(0) is the constant
        term, and "T nmid f" means f(0) != 0. For this to be -1 mod T
        always (independent of which nonzero f(0)), we need p = 2:
        then any nonzero constant term is 1 = -1 mod 2, so f(0) + 1 = 0,
        and (T+1)*f + 1 is divisible by T. Beautiful and exclusive to p=2.
      - For p > 2 we need a slightly different multiplier whose constant
        term times f(0) is forced to be -1; this is impossible to do
        uniformly without making the choice depend on f. We can fix it
        by using "(T + c(f))*f + ..." but that breaks the analogy with
        a fixed multiplier "3". So we restrict to p = 2 for the main
        analog. The p = 2 case is the cleanest and most-cited choice
        in the function-field-Collatz literature [SOURCE SNIPPET ONLY --
        Mathstodon/Lagarias survey mentions the F_2[T] version; see
        also Hicks-Mullen-Yucas 2008 "Polynomial analogues of the
        3x+1 problem"]. Strictly: novelty UNVERIFIED.

  Lyapunov candidate: deg f.
    Under the "halve" branch deg(f/T) = deg(f) - 1 (always strict decrease).
    Under the "odd" branch deg((T+1)*f + 1)/T) = (deg(f) + 1) - 1 = deg(f).
    So deg is *non-increasing* and strictly decreasing on the halve
    branch. This is the Lyapunov function ALMOST works, but is constant
    on odd steps. To conclude termination from this we need: starting
    from any f, you eventually hit a "halve" branch.

  Termination claim (to test):
    Claim: every orbit of Phi reaches the fixed point f = 0 (or the
    cycle {1, T+1}, etc; we identify the actual fixed-point structure
    empirically).

  Implementation: polynomials in F_2[T] are encoded as Python ints
  (bit i = coefficient of T^i), additions = XOR, multiplications =
  carry-less. Division-by-T = right shift.

Author: Alex Ye with Claude. NOVELTY: the precise map and the deg-Lyapunov
argument are routine, and the F_2[T] Collatz analog likely appears in
folklore / Lagarias surveys; we [NOVELTY UNVERIFIED] mark all observations.
"""

from __future__ import annotations

import json
import math
import os
import time
from typing import Dict, List, Optional, Tuple

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# F_2[T] arithmetic (polynomials encoded as bitmask Python ints, bit i = T^i).
# ---------------------------------------------------------------------------


def f2_deg(f: int) -> int:
    """Degree of f in F_2[T] (with deg(0) = -1 by convention)."""
    if f == 0:
        return -1
    return f.bit_length() - 1


def f2_add(f: int, g: int) -> int:
    """Addition in F_2[T] = XOR."""
    return f ^ g


def f2_mul(f: int, g: int) -> int:
    """Carry-less multiplication in F_2[T]."""
    result = 0
    a = f
    while g:
        if g & 1:
            result ^= a
        a <<= 1
        g >>= 1
    return result


def f2_div_by_T(f: int) -> Tuple[int, int]:
    """
    Return (quotient, remainder) for division of f by T.
    Since T = 0b10, division by T is right-shift, remainder is the
    low bit (constant term).
    """
    return f >> 1, f & 1


def f2_str(f: int) -> str:
    """Pretty-print a polynomial in F_2[T]."""
    if f == 0:
        return "0"
    terms = []
    i = 0
    g = f
    while g:
        if g & 1:
            if i == 0:
                terms.append("1")
            elif i == 1:
                terms.append("T")
            else:
                terms.append(f"T^{i}")
        i += 1
        g >>= 1
    return " + ".join(reversed(terms))


# Sanity self-test
def _selftest_f2():
    # (T+1)^2 = T^2 + 1 in F_2[T]
    Tplus1 = 0b11  # T + 1
    sq = f2_mul(Tplus1, Tplus1)
    assert sq == 0b101, f"expected T^2+1=5, got {sq}"
    # deg
    assert f2_deg(0) == -1
    assert f2_deg(1) == 0
    assert f2_deg(0b101) == 2
    # div_by_T
    q, r = f2_div_by_T(0b110)
    assert (q, r) == (0b11, 0)
    q, r = f2_div_by_T(0b111)
    assert (q, r) == (0b11, 1)


_selftest_f2()


# ---------------------------------------------------------------------------
# The F_2[T] Collatz analog.
# ---------------------------------------------------------------------------


def phi(f: int) -> int:
    """
    Phi(f) in F_2[T]:
      if T | f (i.e. f's low bit is 0): return f / T (right shift).
      else: return ((T+1)*f + 1) / T.

    For "odd" f (low bit 1), we have f = 1 + 2*g for some g in F_2[T]
    (g = f >> 1). Then
       (T+1)*f + 1 = T*f + f + 1 = T*f + (f + 1).
    Since f has low bit 1, f + 1 has low bit 0, so we can divide by T:
       ((T+1)*f + 1) / T = f + (f+1)/T = f + ((f^1) >> 1).
    This is the fast formula we use.
    """
    if f == 0:
        return 0
    if f & 1 == 0:
        return f >> 1
    # odd branch
    return f ^ ((f ^ 1) >> 1)


def orbit(f: int, max_steps: int = 100_000) -> List[int]:
    """
    Return the full orbit [f, Phi(f), Phi^2(f), ...] until either:
      - the orbit enters a previously-seen value (cycle), in which case
        we stop at the second occurrence;
      - max_steps reached.
    """
    seen = {f: 0}
    orb = [f]
    m = f
    for k in range(1, max_steps + 1):
        m = phi(m)
        orb.append(m)
        if m in seen:
            return orb
        seen[m] = k
    return orb


def reaches_fixed_set(f: int, fixed_set: set, max_steps: int = 100_000) -> Tuple[bool, int]:
    """Returns (reached, steps_to_reach_or_max)."""
    if f in fixed_set:
        return True, 0
    m = f
    for k in range(1, max_steps + 1):
        m = phi(m)
        if m in fixed_set:
            return True, k
    return False, max_steps


def find_fixed_points_and_cycles(deg_limit: int = 6) -> Dict:
    """
    For all f in F_2[T] of degree <= deg_limit, compute the cycle/fixed point
    the orbit enters, and tabulate.
    """
    cycle_reps: Dict[int, Dict] = {}  # map from "canonical cycle element" to info
    # First find all fixed points and cycles in this range by orbit exploration.
    seen_canonical: Dict[int, int] = {}  # f -> canonical cycle id

    cycles: List[Dict] = []
    cycle_id_of: Dict[int, int] = {}
    next_id = 0
    for f in range(2 ** (deg_limit + 1)):
        if f in cycle_id_of:
            continue
        # Trace orbit until we hit either a known cycle id or a repeated value
        path: List[int] = []
        path_set: Dict[int, int] = {}
        m = f
        cid: Optional[int] = None
        steps_seen = 0
        max_loop = 10 * (2 ** (deg_limit + 1)) + 200
        while True:
            if m in cycle_id_of:
                cid = cycle_id_of[m]
                break
            if m in path_set:
                # New cycle discovered from path_set[m] onward
                cycle_start = path_set[m]
                cyc = path[cycle_start:]
                # Canonical: sort by degree then int (smallest int first)
                canon = min(cyc)
                cid = next_id
                next_id += 1
                cycles.append({
                    "id": cid,
                    "canonical": canon,
                    "length": len(cyc),
                    "elements": sorted(cyc),
                    "max_deg": max(f2_deg(x) for x in cyc),
                })
                for x in cyc:
                    cycle_id_of[x] = cid
                break
            path_set[m] = len(path)
            path.append(m)
            m = phi(m)
            steps_seen += 1
            if steps_seen > max_loop:
                # Should not happen if Phi is bounded; just abort
                raise RuntimeError(f"orbit of {f} did not close in {max_loop} steps")
        # Now propagate the cid to the entire path (everything that was traversed
        # eventually enters cycle cid).
        for x in path:
            if x not in cycle_id_of:
                cycle_id_of[x] = cid

    # Tally basins
    basin_sizes: Dict[int, int] = {c["id"]: 0 for c in cycles}
    for x in range(2 ** (deg_limit + 1)):
        basin_sizes[cycle_id_of[x]] += 1

    for c in cycles:
        c["basin_size_below_2^{}".format(deg_limit + 1)] = basin_sizes[c["id"]]
        c["element_strs"] = [f2_str(x) for x in c["elements"]]

    return {
        "deg_limit": deg_limit,
        "n_polynomials": 2 ** (deg_limit + 1),
        "n_cycles": len(cycles),
        "cycles": cycles,
    }


def stopping_times_distribution(deg_limit: int = 10,
                                target_set: Optional[set] = None) -> Dict:
    """
    Compute stopping time (steps until reaching `target_set`, default = {0})
    for all f in F_2[T] with deg(f) <= deg_limit.

    Empirical Lyapunov check: at each step k, log how many distinct f-values
    have orbit_step(f, k) of each degree.
    """
    if target_set is None:
        target_set = {0}
    n_polys = 2 ** (deg_limit + 1)
    stopping_t: Dict[int, int] = {}  # f -> sigma(f)
    max_orbit_deg: Dict[int, int] = {}

    # First fully resolve target_set (cycles to which we report convergence).
    # Then compute stopping time by reverse-induction (BFS from target_set).
    # Simpler approach: forward simulation per f with memoization.

    INF = -1
    sigma = [INF] * n_polys
    for x in target_set:
        if 0 <= x < n_polys:
            sigma[x] = 0
    for f in range(n_polys):
        if sigma[f] != INF:
            continue
        path = []
        m = f
        peak = m
        while True:
            if m < n_polys and sigma[m] != INF:
                base = sigma[m]
                break
            if m >= n_polys:
                # We left the range; trust that orbit is finite-length, simulate
                # until we re-enter or hit a known fixed point. For F_2[T] the
                # degree is non-increasing under phi, so once m exceeds n_polys
                # we never return -- but actually phi keeps degree or decreases.
                # So m >= n_polys shouldn't happen if f < n_polys.
                raise RuntimeError(f"orbit of f={f} (deg {f2_deg(f)}) escaped: m={m} deg {f2_deg(m)}")
            path.append(m)
            m = phi(m)
            if f2_deg(m) > f2_deg(peak):
                peak = m
        # Walk back assigning
        for i, x in enumerate(reversed(path)):
            sigma[x] = base + i + 1
        max_orbit_deg[f] = f2_deg(peak)

    by_deg: Dict[int, List[int]] = {}
    for f in range(n_polys):
        d = f2_deg(f)
        by_deg.setdefault(d, []).append(sigma[f])

    summary = {}
    for d, vals in by_deg.items():
        non_inf = [v for v in vals if v != INF]
        summary[str(d)] = {
            "count": len(vals),
            "n_converged": len(non_inf),
            "max_sigma": max(non_inf) if non_inf else None,
            "mean_sigma": (sum(non_inf) / len(non_inf)) if non_inf else None,
        }

    return {
        "deg_limit": deg_limit,
        "n_polynomials": n_polys,
        "by_deg": summary,
        "target_set_size": len(target_set),
    }


# ---------------------------------------------------------------------------
# Degree-as-Lyapunov verification.
# ---------------------------------------------------------------------------


def verify_degree_lyapunov(deg_limit: int = 12) -> Dict:
    """
    For all f with deg(f) <= deg_limit, check that deg(Phi(f)) <= deg(f).
    Report:
      - n_strict_decrease (deg drops; happens iff T | f)
      - n_equal           (deg stays the same; happens iff T nmid f)
      - n_increase        (deg grows -- should be 0!)
      - any counterexample
    """
    n_polys = 2 ** (deg_limit + 1)
    n_dec = 0
    n_eq = 0
    n_inc = 0
    n_zero = 0
    counterexs: List[Tuple[int, int, int]] = []
    for f in range(n_polys):
        df = f2_deg(f)
        pf = phi(f)
        dp = f2_deg(pf)
        if f == 0:
            n_zero += 1
            continue
        if dp < df:
            n_dec += 1
        elif dp == df:
            n_eq += 1
        else:
            n_inc += 1
            if len(counterexs) < 10:
                counterexs.append((f, df, dp))
    return {
        "deg_limit": deg_limit,
        "n_polynomials": n_polys,
        "n_strict_decrease": n_dec,
        "n_equal": n_eq,
        "n_increase": n_inc,
        "n_zero_excluded": n_zero,
        "counterexamples": counterexs,
        "lyapunov_status": "PASS_NONINCREASING" if n_inc == 0 else "FAIL",
    }


# ---------------------------------------------------------------------------
# Termination proof (constructive).
# ---------------------------------------------------------------------------


def two_step_drift_table(deg_limit: int = 8) -> Dict:
    """
    Because deg is constant on odd steps, the relevant question is:
    do we eventually hit an even step? Equivalently: is the orbit on
    {odd polynomials} not closed?

    For each *odd* f (low bit 1), check whether Phi(f) is even or odd.
      Phi(f) = f + (f+1)/2 where (f+1) is even (low bit 0).
      So Phi(f) has low bit (f & 1) XOR (((f+1) >> 1) & 1) = 1 XOR (((f+1)>>1) & 1).
      We are odd, f & 1 = 1; so Phi(f) is even iff (((f+1) >> 1) & 1) = 1
      i.e. iff the SECOND-LOWEST bit of (f+1) is 1
      i.e. iff bit-1 of (f+1) is 1
      i.e. iff (f+1) mod 4 in {2, 3}
      i.e. (f mod 4) in {1, 2}: but f is odd so f mod 4 in {1, 3}.
        f mod 4 = 1 -> f+1 mod 4 = 2 -> bit-1 of f+1 is 1 -> Phi(f) even.
        f mod 4 = 3 -> f+1 mod 4 = 0 -> bit-1 of f+1 is 0 -> Phi(f) odd.

    NOTE: this is integer arithmetic, not F_2[T] arithmetic; we want
    the F_2[T] version. In F_2[T], + is XOR, not integer plus. So:
      f odd  <-> f & 1 = 1
      f + 1 in F_2[T] = f XOR 1 = (f with low bit flipped to 0)
      Phi(f) = f XOR ((f XOR 1) >> 1)
      Phi(f) is even <-> low bit of Phi(f) is 0
                    <-> low bit of (f XOR ((f XOR 1) >> 1)) is 0
                    <-> (f & 1) XOR (((f XOR 1) >> 1) & 1) = 0
                    <-> 1 XOR ((f >> 1) & 1) = 0   [since f XOR 1 flips
                                                    only the low bit;
                                                    (f XOR 1) >> 1 = f >> 1
                                                    because the low bit
                                                    is removed by shift]
                    <-> (f >> 1) & 1 = 1
                    <-> bit-1 of f is 1.

    So in F_2[T]: an odd polynomial f gives Phi(f) even iff the
    coefficient of T^1 in f is 1 (i.e. f mod T^2 = T + 1, NOT = 1).

    Therefore the only odd polynomials whose Phi-image is still odd
    are those with f mod T^2 = 1, i.e. those with no T-term.

    Following the chain: if Phi(f) is again odd (so f mod T^2 = 1, i.e.
    f = 1 + g*T^2 for some g), what is Phi(f) mod T^2?
      f = 1 + T^2 * g
      f XOR 1 = T^2 * g
      (f XOR 1) >> 1 = T * g
      Phi(f) = (1 + T^2 g) XOR (T g)
             = 1 + T*g + T^2*g (since these are different bits when g != 0).
      Phi(f) mod T^2 = 1 + T * (g mod 2) = 1 + T * (g & 1).
      Phi(f) mod T^2 = T + 1 iff g & 1 = 1, else = 1.

    So an odd f = 1 + T^2 g has Phi(f) odd-and-stays-bad iff g is even
    (g & 1 = 0), i.e. iff bit-2 of f is 0. Cascading:

      f = 1 + T^2 g, g & 1 = 0  =>  Phi(f) = 1 + T^2 g
                                               + T (g shift but cancelled)
      ... (a longer analysis follows; full induction in writeup)

    This tabulates: for each odd f with deg <= deg_limit, count the
    number of consecutive Phi-applications before an EVEN value appears.
    """
    n_polys = 2 ** (deg_limit + 1)
    runs = []
    max_run = 0
    arg_max = 0
    # Exclude the fixed point f=1 (phi(1)=1 stays odd forever).
    cap = 4 * deg_limit + 10
    for f in range(3, n_polys, 2):  # odd f != 1
        m = f
        k = 0
        while m & 1 and k < cap:
            m_next = phi(m)
            if m_next == m:
                break  # we are at a fixed point that is odd
            m = m_next
            k += 1
        runs.append(k)
        if k > max_run:
            max_run = k
            arg_max = f
    return {
        "deg_limit": deg_limit,
        "n_odd_polynomials_nonfixed": len(runs),
        "max_consecutive_odd_steps": max_run,
        "argmax_odd_polynomial_str": f2_str(arg_max),
        "argmax_odd_polynomial_int": arg_max,
        "mean_consecutive_odd_steps": sum(runs) / max(len(runs), 1),
    }


# ---------------------------------------------------------------------------
# Top-level runner.
# ---------------------------------------------------------------------------


def main(deg_limit_cycles: int = 8,
         deg_limit_sigma: int = 14,
         deg_limit_lyap: int = 16,
         out_path: Optional[str] = None) -> Dict:
    print(f"F_2[T] Collatz analog: fixed points and cycles, deg <= {deg_limit_cycles} ...")
    cyc = find_fixed_points_and_cycles(deg_limit=deg_limit_cycles)
    print(f"  found {cyc['n_cycles']} cycle(s) among {cyc['n_polynomials']} polynomials")
    for c in cyc["cycles"]:
        print(f"   cycle id {c['id']}: length {c['length']}, max_deg {c['max_deg']}, "
              f"elements {c['element_strs']}, basin {c[f'basin_size_below_2^{deg_limit_cycles+1}']}")

    print(f"Stopping-time distribution, deg <= {deg_limit_sigma} ...")
    fixed_set = set()
    for c in cyc["cycles"]:
        for e in c["elements"]:
            fixed_set.add(e)
    sd = stopping_times_distribution(deg_limit=deg_limit_sigma,
                                     target_set=fixed_set)
    print(f"  done; n_polys {sd['n_polynomials']}")

    print(f"Degree-Lyapunov verification, deg <= {deg_limit_lyap} ...")
    lyap = verify_degree_lyapunov(deg_limit=deg_limit_lyap)
    print(f"  status: {lyap['lyapunov_status']}; "
          f"strict_decrease {lyap['n_strict_decrease']}, equal {lyap['n_equal']}, "
          f"increase {lyap['n_increase']}")

    print(f"Two-step drift table (consecutive odd-step runs)...")
    tsd = two_step_drift_table(deg_limit=min(deg_limit_lyap, 14))
    print(f"  max consecutive odd steps = {tsd['max_consecutive_odd_steps']} "
          f"at {tsd['argmax_odd_polynomial_str']}")

    summary = {
        "version": 1,
        "description": "F_2[T] Collatz analog: orbit and Lyapunov structure.",
        "cycles": cyc,
        "stopping_distribution": sd,
        "degree_lyapunov": lyap,
        "consecutive_odd_steps": tsd,
    }
    if out_path is None:
        out_path = os.path.join(DATA_DIR, "function_field.json")
    with open(out_path, "w") as fp:
        json.dump(summary, fp, indent=2)
    print(f"Wrote {out_path}")
    return summary


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--deg-cycles", type=int, default=8)
    p.add_argument("--deg-sigma", type=int, default=14)
    p.add_argument("--deg-lyap", type=int, default=16)
    p.add_argument("--out", type=str, default=None)
    args = p.parse_args()
    main(deg_limit_cycles=args.deg_cycles,
         deg_limit_sigma=args.deg_sigma,
         deg_limit_lyap=args.deg_lyap,
         out_path=args.out)
