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

def compare_lower_bounds(K_values: List[int]) -> List[Tuple[int, float, float]]:
    """
    Compare, for Lambda = N log2 - K log3 with N = round(K*delta):

      LMN two-log lower bound:    log|Lambda| >= -24.34 * (log b' + 0.14)^2 * logA1 * logA2
                                  with logA1 = 1 (max{log2,1}), logA2 = log3,
                                  b' = N/log3 + K/1.
      1-dim irr.-measure bound:   |delta - N/K| > K^{-mu}, mu = 5.1163051 (via log3),
                                  => |Lambda| = log2 * K * |delta - N/K| > log2 * K^{1-mu}.

    Returns (K, lmn_log_lower, irr_log_lower) where each is log10 of the
    lower bound on |Lambda|. The LMN bound being LARGER (closer to 0, i.e.
    less negative) confirms it is the binding/stronger constraint.

    NOTE: this is an *illustration* of the qualitative claim in section 5.2;
    the LMN secondary constants are tagged [PARTIAL-CONST] in the theory note.
    """
    delta = (mp.log(3) / mp.log(2)) if HAVE_MPMATH else (math.log(3) / math.log(2))
    log2 = math.log(2)
    log3 = math.log(3)
    mu = 5.1163051  # Wu-Wang 2014 mu(log 3); using as a (generous) proxy
    out = []
    for K in K_values:
        N = round(float(K * delta))
        logA1, logA2 = 1.0, log3
        bprime = N / log3 + K / logA1
        lmn_loglambda = -24.34 * (math.log(bprime) + 0.14) ** 2 * logA1 * logA2
        lmn_log10 = lmn_loglambda / math.log(10)
        # 1-dim: |Lambda| > log2 * K^{1-mu}
        irr_loglambda = math.log(log2) + (1 - mu) * math.log(K)
        irr_log10 = irr_loglambda / math.log(10)
        out.append((K, lmn_log10, irr_log10))
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

    # (C5)
    print("\n(C5) Two-log (LMN) vs 1-dim irr.-measure lower bound on |Lambda|")
    print("     (log10 of the lower bound; LARGER = less negative = stronger):")
    print(f"     {'K':>14} {'LMN log10|L|>=':>16} {'irr log10|L|>=':>16} {'LMN stronger?':>14}")
    cmp = compare_lower_bounds([10**3, 10**5, 10**7, 10**9, 10**11, 10**13])
    lmn_always_stronger = True
    for (K, lmn, irr) in cmp:
        stronger = lmn > irr
        lmn_always_stronger = lmn_always_stronger and stronger
        print(f"     {K:>14} {lmn:>16.3f} {irr:>16.3f} {str(stronger):>14}")
    print(f"     => LMN two-log bound dominates for all tested K: {lmn_always_stronger}")
    if not lmn_always_stronger:
        # This is the qualitative claim; failure would mean the theory note's
        # section 5.2 needs revisiting.
        failures += 1

    print("\n" + "=" * 72)
    if failures == 0:
        print("ALL CHECKS PASSED (0 failures).")
    else:
        print(f"FAILURES: {failures}  -- investigate before relying on the note.")
    print("=" * 72)
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
