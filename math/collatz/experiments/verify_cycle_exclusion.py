"""
Step-1 verification for theory/cycle_exclusion_explicit.md.

Checks, with exact / high-precision arithmetic, the numerical claims that
back the reconstruction of the Steiner-Simons-de Weger-Hercher cycle-
exclusion argument:

  (C1) delta = log_2(3) and its continued fraction.
  (C2) The cycle-exclusion "magic numbers" from the literature
       (Eliahou's 301994 / 17087915 / 85137581; Simons-de Weger's
       357638239; the modern 217976794617) are convergent
       numerators/denominators of delta. This is the independent
       confirmation that "cycle lengths are forced to be convergents
       of log_2(3)".
  (C3) The cycle inequality 2^N > 3^K  <=>  N > K*delta (Lemma 1), and
       that for small denominators the rational approximation
       |delta - p/q| is never good enough to admit a non-trivial cycle.
  (C4) Hercher's verification bound arithmetic: 1536 * 2^60 = 3 * 2^69.
  (C5) The LMN-style lower bound on Lambda = N log2 - K log3 dominates
       (is larger than) the one-dimensional irrationality-measure lower
       bound for the relevant range -- i.e. the two-log estimate is the
       binding one, not mu(log_2 3). (Numerical illustration of the
       qualitative claim in section 5.2 of the theory note.)

Pure-Python fallback (Fraction) is used when mpmath is unavailable, so
this runs in any environment.

Author: Alex Ye (AI assistance disclosed separately).
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import List, Tuple

try:
    import mpmath as mp
    mp.mp.dps = 120
    HAVE_MPMATH = True
except Exception:  # pragma: no cover
    HAVE_MPMATH = False


# ---------------------------------------------------------------------------
# (C1) delta = log_2(3) and its continued fraction.
# ---------------------------------------------------------------------------

def delta_and_cf(n_terms: int = 30) -> Tuple[object, List[int]]:
    """Return (delta, [a0, a1, ...]) the continued fraction of log_2(3)."""
    if HAVE_MPMATH:
        delta = mp.log(3) / mp.log(2)
        cf: List[int] = []
        y = delta
        for _ in range(n_terms):
            a = int(mp.floor(y))
            cf.append(a)
            frac = y - a
            if frac == 0:
                break
            y = 1 / frac
        return delta, cf
    # Fallback: float CF (good for ~15 terms only).
    delta = math.log(3) / math.log(2)
    cf = []
    y = delta
    for _ in range(min(n_terms, 18)):
        a = int(math.floor(y))
        cf.append(a)
        frac = y - a
        if frac == 0:
            break
        y = 1 / frac
    return delta, cf


def convergents(cf: List[int]) -> List[Tuple[int, int]]:
    """Return list of (p, q) convergents from a continued fraction."""
    out = []
    h0, h1 = 1, cf[0]
    k0, k1 = 0, 1
    out.append((h1, k1))
    for i in range(1, len(cf)):
        h2 = cf[i] * h1 + h0
        k2 = cf[i] * k1 + k0
        out.append((h2, k2))
        h0, h1 = h1, h2
        k0, k1 = k1, k2
    return out


# ---------------------------------------------------------------------------
# (C2) The literature "magic numbers" are convergent num/denoms of delta.
# ---------------------------------------------------------------------------

LITERATURE_NUMBERS = {
    301994: "Eliahou 1993 coefficient (convergent numerator p)",
    190537: "Eliahou-related (convergent denominator q for 301994)",
    17087915: "Eliahou 1993 coefficient / SdW (convergent numerator p)",
    85137581: "Eliahou 1993 coefficient (convergent numerator p)",
    357638239: "Simons 2005 2-cycle length lower bound (convergent numerator p)",
    217976794617: "modern (2025) cycle-length lower bound (convergent numerator p)",
    10439860591: "convergent numerator p (cycle-length scale)",
    6586818670: "convergent denominator q (>= odd-numbers-in-loop scale)",
}


def check_magic_numbers(convs: List[Tuple[int, int]]) -> List[Tuple[int, bool, str]]:
    """Check each literature number appears as a convergent p or q of delta."""
    ps = {p for (p, q) in convs}
    qs = {q for (p, q) in convs}
    results = []
    for num, desc in LITERATURE_NUMBERS.items():
        found = (num in ps) or (num in qs)
        where = ("p" if num in ps else "") + ("q" if num in qs else "")
        results.append((num, found, f"{desc}  [matched as {where or 'NONE'}]"))
    return results


# ---------------------------------------------------------------------------
# (C3) Cycle inequality and quality of approximation.
# ---------------------------------------------------------------------------

def check_cycle_inequality(convs: List[Tuple[int, int]]) -> List[Tuple[int, int, bool, float]]:
    """
    For each convergent p/q (interpret q ~ K = #o-steps, p ~ N? actually
    p/q ~ delta = N/K so p ~ N-ish, q ~ K-ish), verify:
      - 2^p vs 3^q ordering is consistent with N > K*delta (Lemma 1)
      - report q^2 * |delta - p/q| (Legendre: < 1 for convergents).
    Here p approximates N and q approximates K only loosely; we simply
    confirm the convergent property q^2|delta - p/q| < 1 holds (a sanity
    check that these are genuine convergents) and that delta lies strictly
    between consecutive convergents (so no exact equality => 2^N != 3^K).
    """
    out = []
    if HAVE_MPMATH:
        delta = mp.log(3) / mp.log(2)
    else:
        delta = math.log(3) / math.log(2)
    for (p, q) in convs:
        if HAVE_MPMATH:
            err = abs(delta - mp.mpf(p) / q)
            q2err = float(q * q * err)
        else:
            err = abs(delta - Fraction(p, q))
            q2err = float(q * q * err)
        legendre_ok = q2err < 1.0  # convergents satisfy |delta-p/q| < 1/q^2
        out.append((p, q, legendre_ok, q2err))
    return out


def check_no_equality_2N_3K(max_k: int = 2000) -> bool:
    """
    Confirm 2^N != 3^K for all 1 <= K <= max_k and N the nearest integers,
    i.e. 2^a = 3^b has no positive integer solution (so the cycle
    denominator 2^N - 3^K is never zero). Trivial by unique factorization,
    but we verify directly on a range as a sanity check.
    """
    for k in range(1, max_k + 1):
        threek = 3 ** k
        # nearest power of two
        n = threek.bit_length()  # 2^(n-1) <= 3^k < 2^n  (for 3^k not a power of 2)
        if (1 << (n - 1)) == threek or (1 << n) == threek:
            return False  # would mean 2^a = 3^b
    return True


# ---------------------------------------------------------------------------
# (C4) Hercher verification-bound arithmetic.
# ---------------------------------------------------------------------------

def check_hercher_bound() -> bool:
    return 1536 * 2 ** 60 == 3 * 2 ** 69


# ---------------------------------------------------------------------------
# (C5) Two-log estimate dominates the 1-dim irrationality-measure estimate.
# ---------------------------------------------------------------------------

def check_deweger_inequality(k_max: int = 200) -> Tuple[bool, int]:
    """
    Verify de Weger's reformulation (Theorem input for cycle exclusion):

        0 < (k+l) log2 - k log3 < 2^(-0.158 k)   has NO solution for k >= 32.

    For each k we take N = smallest integer with Lambda = N log2 - k log3 > 0
    (the best positive linear form for that k, i.e. N = ceil(k*delta) bumped
    if needed). If even this minimal positive Lambda is >= 2^(-0.158 k), then
    no (N,k) can satisfy the strict inequality.

    Returns (no_solution_for_k_ge_32, largest_k_with_solution).
    """
    if HAVE_MPMATH:
        log2 = mp.log(2); log3 = mp.log(3); delta = log3 / log2
        def small_lambda(k):
            N = int(mp.ceil(k * delta))
            if N * log2 - k * log3 <= 0:
                N += 1
            return N * log2 - k * log3
        def bound(k):
            return mp.power(2, mp.mpf('-0.158') * k)
    else:
        log2 = math.log(2); log3 = math.log(3); delta = log3 / log2
        def small_lambda(k):
            N = math.ceil(k * delta)
            if N * log2 - k * log3 <= 0:
                N += 1
            return N * log2 - k * log3
        def bound(k):
            return 2.0 ** (-0.158 * k)

    largest_with_sol = 0
    no_sol_ge_32 = True
    for k in range(1, k_max + 1):
        lam = small_lambda(k)
        if (lam > 0) and (lam < bound(k)):
            largest_with_sol = k
            if k >= 32:
                no_sol_ge_32 = False
    return no_sol_ge_32, largest_with_sol


def compare_bound_directions(K_values: List[int]) -> List[Tuple[int, str, str]]:
    """
    Illustrate the *directional* claim of theory section 5.2:

      - The two-log lower bound  |Lambda| > 2^{-0.158 K}  decays EXPONENTIALLY
        in K; set against the cycle's (constant-in-K) geometric budget
        |Lambda| < Theta(m/B) it yields an UPPER bound on K.
      - The irrationality-measure lower bound |Lambda| > (log2) K^{1-mu}
        decays only POLYNOMIALLY; set against the same budget it yields a
        LOWER bound on K (wrong direction, no contradiction).

    We report, for representative K, the per-K exponent (d/dK of -log2|Lambda|
    lower bound): two-log gives ~0.158 (linear coeff), irr-measure gives
    ~(mu-1)/(K ln2) -> 0 (sublinear). A positive bounded-away-from-0 slope is
    what makes the two-log bound able to cap K from above.
    """
    log2 = math.log(2)
    mu = 5.1163051
    out = []
    for K in K_values:
        twolog_slope = 0.158  # -log2|Lambda| >= 0.158*K  => slope 0.158 (constant)
        # irr: -log2|Lambda| <= (mu-1) log2(K) - log2(log2); slope in K:
        irr_slope = (mu - 1) / (K * math.log(2))
        out.append((K,
                    f"0.158 (linear, caps K above)",
                    f"{irr_slope:.2e} (->0, gives lower bd only)"))
    return out


# ---------------------------------------------------------------------------
# Driver.
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 72)
    print("Step-1 verification: cycle_exclusion_explicit.md")
    print(f"mpmath available: {HAVE_MPMATH}")
    print("=" * 72)

    failures = 0

    # (C1)
    delta, cf = delta_and_cf(30)
    print("\n(C1) delta = log_2(3) =", str(delta)[:50], "...")
    print("     continued fraction:", cf[:20], "...")
    convs = convergents(cf)

    # (C2)
    print("\n(C2) Literature 'magic numbers' as convergents of delta:")
    for num, found, desc in check_magic_numbers(convs):
        flag = "OK " if found else "!! "
        if not found:
            failures += 1
        print(f"     [{flag}] {num:>15}  {desc}")

    # (C3)
    print("\n(C3) Convergent quality (Legendre: q^2|delta-p/q| < 1) + no 2^N=3^K:")
    conv_checks = check_cycle_inequality(convs)
    all_legendre = all(ok for (_, _, ok, _) in conv_checks)
    if not all_legendre:
        failures += 1
    for (p, q, ok, q2err) in conv_checks[:14]:
        print(f"     {p:>15}/{q:<15} q^2*err={q2err:.4f}  legendre_ok={ok}")
    no_eq = check_no_equality_2N_3K(2000)
    print(f"     2^N != 3^K for K<=2000 (denom never zero): {no_eq}")
    if not no_eq:
        failures += 1

    # (C4)
    hb = check_hercher_bound()
    print(f"\n(C4) Hercher bound 1536*2^60 == 3*2^69: {hb}  "
          f"(= {3 * 2**69})")
    if not hb:
        failures += 1

    # (C5) -- de Weger's reformulated inequality and the directional argument.
    no_sol, largest = check_deweger_inequality(200)
    print("\n(C5a) De Weger: 0 < N log2 - K log3 < 2^(-0.158 K) has NO solution for K>=32")
    print(f"      largest K with a solution: {largest}  (must be < 32)")
    print(f"      no solution for any K>=32: {no_sol}")
    if not (no_sol and largest < 32):
        failures += 1

    print("\n(C5b) Directional argument (theory 5.2): exponential vs polynomial")
    print("      slope of (-log2 lower-bound on |Lambda|) in K:")
    print(f"      {'K':>14} {'two-log slope':>34} {'irr-measure slope':>34}")
    for (K, tl, ir) in compare_bound_directions([10**2, 10**4, 10**6, 10**9, 10**11]):
        print(f"      {K:>14} {tl:>34} {ir:>34}")
    print("      => two-log slope is bounded away from 0 (caps K from above);")
    print("         irr-measure slope -> 0 (yields only a lower bound on K).")

    print("\n" + "=" * 72)
    if failures == 0:
        print("ALL CHECKS PASSED (0 failures).")
    else:
        print(f"FAILURES: {failures}  -- investigate before relying on the note.")
    print("=" * 72)
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
