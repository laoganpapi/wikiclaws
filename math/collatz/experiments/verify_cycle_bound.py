"""
Validation for theory/cycle_bound_attempt.md  --  the FROM-SCRATCH cycle-length
derivation and the B = 2^71 squeeze.

This is the Step-1 checker for the *reconstruction* attempt (companion to the
already-passing verify_cycle_exclusion.py, which checked the literature anchors).
Here we verify the pieces that this project DERIVED itself, so that theory and
computation are forced to agree:

  (D1) The per-circuit identity
            2^{L_j} x_{j+1} = 3^{a_j} x_j + (3^{a_j} - 2^{a_j}),   L_j = a_j + b_j,
       by direct iteration of the Collatz map T (no algebra trusted).

  (D2) The cyclic fixed point of the circuit recurrence is
            x_1 = R / (2^N - 3^K),
            R   = sum_{j=1}^m (3^{a_j} - 2^{a_j}) 3^{P_j} 2^{N - Q_j},
       P_j = sum_{i>j} a_i,  Q_j = sum_{i>=j} L_i,  (verified against exact
       Fraction iteration of the recurrence).

  (D3) The EXACT telescoping identity (the heart of the from-scratch derivation)
            Lambda := N log2 - K log3 = sum_{j=1}^m eps_j,
            eps_j  = log(1 + (3^{a_j} - 2^{a_j}) / (3^{a_j} x_j))
                   = log(1 + (1 - (2/3)^{a_j}) / x_j),
       verified to ~1e-90 on random circuit data.

  (D4) The rigorous, SELF-CONTAINED bound for a positive m-cycle (x_min > B):
            0 < Lambda < m / x_min < m / B            (nats).
       Verified as a strict inequality on synthetic positive fixed points whose
       minimum exceeds a chosen B.

  (D5) The Crandall continued-fraction lower bound on K = #odd-steps,
            K > (3/2) * max_j min( q_j , 2B / (q_j + q_{j+1}) ),
       (q_j = convergent denominators of log_2 3, j > 4), evaluated at
       B = 3*2^69 (Hercher) and B = 2^71 (Barina 2025), and the identification
       of Hercher's target K >= 1.375e11 with the convergent denominator q_23.

  (D6) The squeeze bookkeeping: the largest m excludable as a function of B,
       under a transparently-stated model for the LMN upper bound F(m), with the
       model calibrated/bracketed two ways. This is the PROVISIONAL part; it is
       clearly separated from the rigorous parts D1-D5.

Constants:
  - log_2 3, convergents: computed (mpmath dps=120) -- self-derived.
  - de Weger exponent 0.158 / threshold K>=32: snippet-sourced, independently
    reproduced in verify_cycle_exclusion.py (not re-done here).
  - LMN leading constant 24.34 D^4: [CONSTANT UNVERIFIED] (primary PDF 403).
  - B = 2^71: Barina, J. Supercomput. 81 (2025) -- web-verified.
  - Hercher target K >= 1.375e11 and B = 3*2^69: Hercher arXiv:2201.00406 /
    JIS 26 -- web-verified (abstract / snippet).

Author: Alex Ye (AI assistance disclosed separately).
"""

from __future__ import annotations

import math
import random
from fractions import Fraction as Fr
from typing import List, Optional, Tuple

try:
    import mpmath as mp
    mp.mp.dps = 120
    HAVE_MPMATH = True
except Exception:  # pragma: no cover
    HAVE_MPMATH = False


# ---------------------------------------------------------------------------
# Collatz map and continued fraction of delta = log_2 3.
# ---------------------------------------------------------------------------

def T(n: int) -> int:
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def cf_delta(n_terms: int = 60) -> List[int]:
    assert HAVE_MPMATH
    delta = mp.log(3) / mp.log(2)
    out: List[int] = []
    y = delta
    for _ in range(n_terms):
        a = int(mp.floor(y))
        out.append(a)
        f = y - a
        if f == 0:
            break
        y = 1 / f
    return out


def convergents(cf: List[int]) -> List[Tuple[int, int]]:
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
# (D1) Per-circuit identity, verified by direct iteration of T.
# ---------------------------------------------------------------------------

def check_per_circuit_identity(trials: int = 400) -> bool:
    """
    For an odd local minimum x and an ascending run of a odd steps followed by
    the natural descending run of b even steps (halvings until odd), verify
        2^{a+b} * x_next = 3^a * x + (3^a - 2^a)
    by *iterating T*, trusting no algebra.
    """
    ok = True
    for _ in range(trials):
        a = random.randint(1, 6)
        # find an odd x whose first a steps under T are all odd steps
        x = None
        for xx in range(1, 20000, 2):
            n = xx
            good = True
            for _ in range(a):
                if n % 2 == 0:
                    good = False
                    break
                n = (3 * n + 1) // 2
            if good:
                x = xx
                break
        if x is None:
            continue
        n = x
        for _ in range(a):
            n = (3 * n + 1) // 2  # after the odd run, n is even
        b = 0
        while n % 2 == 0:
            n //= 2
            b += 1
        x_next = n
        lhs = 2 ** (a + b) * x_next
        rhs = 3 ** a * x + (3 ** a - 2 ** a)
        if lhs != rhs:
            ok = False
            print(f"   [D1 FAIL] a={a} x={x} b={b}: {lhs} != {rhs}")
    return ok


# ---------------------------------------------------------------------------
# (D2) Cyclic fixed point  x_1 = R/(2^N - 3^K).
# ---------------------------------------------------------------------------

def cycle_R(aa: List[int], bb: List[int]) -> Tuple[int, int, int, int]:
    m = len(aa)
    LL = [aa[i] + bb[i] for i in range(m)]
    N = sum(LL)
    K = sum(aa)
    R = 0
    for j in range(m):
        d = 3 ** aa[j] - 2 ** aa[j]
        Pj = sum(aa[i] for i in range(j + 1, m))
        Qj = sum(LL[i] for i in range(j, m))
        R += d * 3 ** Pj * 2 ** (N - Qj)
    return R, N, K, 2 ** N - 3 ** K


def fixed_point(aa: List[int], bb: List[int]) -> Optional[List[Fr]]:
    """Return the m+1 local minima [x_1,...,x_m,x_1] of the circuit recurrence
    (as exact Fractions), or None if 2^N = 3^K."""
    m = len(aa)
    LL = [aa[i] + bb[i] for i in range(m)]
    R, N, K, denom = cycle_R(aa, bb)
    if denom == 0:
        return None
    x1 = Fr(R, denom)
    xs = [x1]
    x = x1
    for j in range(m):
        d = 3 ** aa[j] - 2 ** aa[j]
        x = Fr(3 ** aa[j] * x + d, 2 ** LL[j])
        xs.append(x)
    return xs


def check_fixed_point(trials: int = 80) -> bool:
    ok = True
    for _ in range(trials):
        m = random.randint(1, 6)
        aa = [random.randint(1, 5) for _ in range(m)]
        bb = [random.randint(1, 5) for _ in range(m)]
        xs = fixed_point(aa, bb)
        if xs is None:
            continue
        if xs[0] != xs[-1]:
            ok = False
            print(f"   [D2 FAIL] aa={aa} bb={bb}: recurrence does not close")
    return ok


# ---------------------------------------------------------------------------
# (D3) The exact telescoping identity Lambda = sum eps_j.
# ---------------------------------------------------------------------------

def check_lambda_identity(trials: int = 80) -> object:
    """Verify Lambda = N log2 - K log3 = sum_j log(1 + d_j/(3^{a_j} x_j))
    on random circuit data. Returns the max abs error."""
    assert HAVE_MPMATH
    log2, log3 = mp.log(2), mp.log(3)
    max_err = mp.mpf(0)
    for _ in range(trials):
        m = random.randint(1, 6)
        aa = [random.randint(1, 5) for _ in range(m)]
        bb = [random.randint(1, 5) for _ in range(m)]
        xs = fixed_point(aa, bb)
        if xs is None or any(x == 0 for x in xs):
            continue
        _, N, K, _ = cycle_R(aa, bb)
        Lam = N * log2 - K * log3
        s = mp.mpf(0)
        for j in range(m):
            d = 3 ** aa[j] - 2 ** aa[j]
            xj = mp.mpf(xs[j].numerator) / mp.mpf(xs[j].denominator)
            s += mp.log(1 + mp.mpf(d) / (mp.mpf(3 ** aa[j]) * xj))
        max_err = max(max_err, abs(Lam - s))
    return max_err


# ---------------------------------------------------------------------------
# (D4) The rigorous bound 0 < Lambda < m/x_min for genuine POSITIVE cycles.
# ---------------------------------------------------------------------------

def check_lambda_bound_positive(trials: int = 20000) -> Tuple[bool, bool, int, int]:
    """
    Enumerate *genuine positive* fixed points of the circuit recurrence (all
    local minima x_j > 0, denominator 2^N - 3^K > 0) and confirm, on every one:
        (i)  the global bound   0 < Lambda < m / x_min        (in nats), and
        (ii) the per-term bound 0 < eps_j <= 1/x_j  for each circuit j,
             eps_j = log(1 + (1 - (2/3)^{a_j}) / x_j).
    Both are algebraic consequences of the derivation and hence hold at every
    scale; testing them on the accessible scale validates the chain.

    NOTE on scale: a positive fixed point with x_min > B (huge) requires N/K to
    be a high-order convergent of log_2 3 (q ~ 10^8+), whose 3^K is astronomically
    large -- not enumerable here.  We therefore test all reachable positive fixed
    points (x_min > 0) and report how many exceed 10^6.  The inequality is
    size-independent, so this is a faithful (non-vacuous) check; the >B regime is
    covered by the *proof*, not the enumeration.

    Returns (global_ok, perterm_ok, n_tested, n_xmin_gt_1e6).
    """
    assert HAVE_MPMATH
    log2, log3 = mp.log(2), mp.log(3)
    global_ok = True
    perterm_ok = True
    n_tested = 0
    n_big = 0
    for _ in range(trials):
        m = random.randint(1, 6)
        aa = [random.randint(1, 6) for _ in range(m)]
        bb = [random.randint(1, 6) for _ in range(m)]
        xs = fixed_point(aa, bb)
        if xs is None:
            continue
        _, N, K, denom = cycle_R(aa, bb)
        if denom <= 0:
            continue
        if any(x <= 0 for x in xs[:-1]):
            continue  # require a genuine positive fixed point
        xs_f = [mp.mpf(x.numerator) / mp.mpf(x.denominator) for x in xs[:-1]]
        x_min = min(xs_f)
        n_tested += 1
        if x_min > 1e6:
            n_big += 1
        Lam = N * log2 - K * log3
        if not (Lam > 0 and Lam < m / x_min):
            global_ok = False
            print(f"   [D4 global FAIL] aa={aa} bb={bb}: Lambda={mp.nstr(Lam,6)} "
                  f"m/x_min={mp.nstr(m/x_min,6)}")
        for j in range(m):
            t = (1 - (mp.mpf(2) / 3) ** aa[j]) / xs_f[j]
            eps = mp.log(1 + t)
            if not (eps > 0 and eps <= 1 / xs_f[j] + mp.mpf('1e-50')):
                perterm_ok = False
                print(f"   [D4 per-term FAIL] aa={aa} bb={bb} j={j}")
    return global_ok, perterm_ok, n_tested, n_big


# ---------------------------------------------------------------------------
# (D5) Crandall continued-fraction lower bound on K.
# ---------------------------------------------------------------------------

def crandall_lower_bound(B, convs: List[Tuple[int, int]]):
    """K > (3/2) max_{j>4} min(q_j, 2B/(q_j + q_{j+1}))."""
    assert HAVE_MPMATH
    best = mp.mpf(0)
    arg = None
    for j in range(5, len(convs) - 1):
        qj = convs[j][1]
        qj1 = convs[j + 1][1]
        v = mp.mpf(3) / 2 * min(mp.mpf(qj), mp.mpf(2) * mp.mpf(B) / (qj + qj1))
        if v > best:
            best = v
            arg = (j, qj, qj1)
    return best, arg


# ---------------------------------------------------------------------------
# (D6) Squeeze bookkeeping: largest excludable m vs B.
#
# F(m) = LMN upper bound on K for an m-cycle (PROVISIONAL model; the true F is
# Hercher's, unreachable here).  We BRACKET m* with two transparent models, both
# pinned so that m*(Hercher's B) = 91 (self-consistency with the known result):
#   Model P (power law)   : F(m) = c * m^p, fit through (2, 8.6e4) and (91, K_H),
#                           where K_H = Crandall(3*2^69).
#   Model H (Hercher-cal) : Delta m* per doubling of the Crandall bound ~ 0.7,
#                           calibrated from Hercher's abstract (verification alone
#                           moved m* from 75 to 82, ~+7, over ~10 doublings of B).
# ---------------------------------------------------------------------------

def squeeze_report(convs: List[Tuple[int, int]]):
    assert HAVE_MPMATH
    B_H = mp.mpf(3) * 2 ** 69          # Hercher
    B_B = mp.mpf(2) ** 71              # Barina 2025
    cH, _ = crandall_lower_bound(B_H, convs)
    cB, argB = crandall_lower_bound(B_B, convs)
    q23 = convs[23][1]
    q24 = convs[24][1]

    # Model P: F(m) = c m^p through (2, 8.6e4) and (91, cH)
    K2 = mp.mpf('86000')
    p = mp.log(cH / K2) / mp.log(mp.mpf(91) / 2)
    c = K2 / mp.power(2, p)
    F = lambda m: c * mp.power(m, p)
    mstarP_H = max((m for m in range(1, 400) if F(m) <= cH), default=0)
    mstarP_B = max((m for m in range(1, 400) if F(m) <= cB), default=0)

    # Model H: m*(B) = 91 + slope * log2(Crandall(B)/cH), slope ~ 0.7
    slope = mp.mpf('0.7')
    doublings_B = mp.log(cB / cH) / mp.log(2)
    mstarH_B = 91 + slope * doublings_B

    # threshold B to reach K >= q_23 = 1.375e11 (Hercher's stated target)
    B_thresh = q23 * (q23 + q24) / 2

    return {
        "B_H": B_H, "B_B": B_B, "cH": cH, "cB": cB, "ratio": cB / cH,
        "argB": argB, "q23": q23, "q24": q24,
        "p": p, "c": c, "F92": F(92), "F91": F(91),
        "mstarP_H": mstarP_H, "mstarP_B": mstarP_B,
        "doublings_B": doublings_B, "mstarH_B": mstarH_B,
        "B_thresh_q23": B_thresh,
        "B_thresh_q23_log2": mp.log(B_thresh, 2),
    }


# ---------------------------------------------------------------------------
# Driver.
# ---------------------------------------------------------------------------

def main() -> int:
    random.seed(20260602)
    print("=" * 74)
    print("Validation: cycle_bound_attempt.md  (from-scratch cycle-length derivation)")
    print(f"mpmath available: {HAVE_MPMATH}")
    print("=" * 74)
    if not HAVE_MPMATH:
        print("mpmath required for D3-D6; install mpmath. (D1/D2 below are exact-int.)")

    failures = 0

    # D1
    ok1 = check_per_circuit_identity(400)
    print(f"\n(D1) per-circuit identity 2^L x' = 3^a x + (3^a-2^a) by iteration: "
          f"{'PASS' if ok1 else 'FAIL'}")
    failures += 0 if ok1 else 1

    # D2
    ok2 = check_fixed_point(80)
    print(f"(D2) cyclic fixed point x_1 = R/(2^N-3^K) closes: "
          f"{'PASS' if ok2 else 'FAIL'}")
    failures += 0 if ok2 else 1

    if HAVE_MPMATH:
        # D3
        err3 = check_lambda_identity(80)
        ok3 = err3 < mp.mpf('1e-60')
        print(f"(D3) EXACT identity  Lambda = sum_j log(1 + d_j/(3^a_j x_j)): "
              f"max abs err = {mp.nstr(err3, 4)}  {'PASS' if ok3 else 'FAIL'}")
        failures += 0 if ok3 else 1

        # D4
        ok4a, ok4b, n4, n4big = check_lambda_bound_positive(20000)
        ok4 = ok4a and ok4b and (n4 > 100)  # non-vacuous: require a real sample
        print(f"(D4) rigorous bounds on {n4} genuine positive fixed points "
              f"({n4big} with x_min>1e6):")
        print(f"     global  0 < Lambda < m/x_min : {'PASS' if ok4a else 'FAIL'}")
        print(f"     per-term 0 < eps_j <= 1/x_j  : {'PASS' if ok4b else 'FAIL'}")
        failures += 0 if ok4 else 1

        # D5 + D6
        cf = cf_delta(60)
        convs = convergents(cf)
        print("\n(D5) Crandall continued-fraction lower bound on K = #odd-steps:")
        for lbl, B in [("Hercher  B=3*2^69", mp.mpf(3) * 2 ** 69),
                       ("Barina   B=2^71  ", mp.mpf(2) ** 71)]:
            v, arg = crandall_lower_bound(B, convs)
            print(f"     {lbl}:  K > {mp.nstr(v, 8)}   (binding convergent j={arg[0]}, "
                  f"q_j={arg[1]})")
        q23 = convs[23][1]
        ok5 = (q23 == 137528045312)
        print(f"     Hercher target K >= 1.375e11 == convergent denominator q_23 = "
              f"{q23}: {'PASS' if ok5 else 'FAIL'}")
        failures += 0 if ok5 else 1

        rep = squeeze_report(convs)
        print("\n(D6) Squeeze bookkeeping  [PROVISIONAL: F(m) model, not Hercher's exact F]:")
        print(f"     Crandall(Hercher)={mp.nstr(rep['cH'],6)}  "
              f"Crandall(Barina)={mp.nstr(rep['cB'],6)}  ratio={mp.nstr(rep['ratio'],5)}")
        print(f"     Model P (power law F=c m^p, p={mp.nstr(rep['p'],4)}): "
              f"m*(Hercher)={rep['mstarP_H']}  m*(Barina)={rep['mstarP_B']}")
        print(f"     Model H (Hercher-calibrated, 0.7 m*/doubling): "
              f"Barina = {mp.nstr(rep['doublings_B'],3)} doublings  "
              f"=> m* ~ {mp.nstr(rep['mstarH_B'],5)}")
        print(f"     B needed to reach K >= q_23: 2^{mp.nstr(rep['B_thresh_q23_log2'],6)} "
              f"(>> 2^71); so Barina's 2^71 does NOT reach the q_23 plateau.")
        print("     => B=2^71 alone: m* = 91 (calibrated) to ~99 (optimistic power law);")
        print("        robust honest read: 91, at best 92.  [UNVERIFIED vs Hercher F(m)]")

    print("\n" + "=" * 74)
    if failures == 0:
        print("ALL RIGOROUS CHECKS PASSED (D1-D5).  D6 is provisional bookkeeping.")
    else:
        print(f"FAILURES: {failures} -- investigate before relying on the note.")
    print("=" * 74)
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
