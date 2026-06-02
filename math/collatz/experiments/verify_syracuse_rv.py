"""
Step-1 verification for the Syracuse-random-variable exposition in
`collatz/theory/tao_syracuse_explicit.md`.

Goal: numerically reproduce, for small n, the objects on which the
log-density-vs-natural-density analysis rests, and check that our written
definitions match Tao (arXiv:1909.03562):

  (1) The n-Syracuse offset map / Syracuse random variable
          Syrac(Z/3^n Z) = sum_{j=1}^{n} 3^{n-j} 2^{-(a_j + a_{j+1} + ... + a_n)}  (mod 3^n)
      with (a_1, ..., a_n) i.i.d. Geom(2),  P(a = k) = 2^{-k}, k >= 1.
      (2^{-m} mod 3^n means the inverse of 2^m in (Z/3^n Z)^x, which exists
      since gcd(2,3)=1.)

  (2) The constant
          c_n := min_{b in (Z/3^n Z), 3 nmid b} P(Syrac(Z/3^n Z) = b),
      Tao's submultiplicativity  c_{n1+n2-1} >= c_{n1} c_{n2},
      and the "beta = 1" target  c_n = 3^{-n+o(n)}, i.e. c_n * 3^n -> not too small.

  (3) The Fourier / characteristic-function decay
          phi_n(xi) := E[ e(-xi * Syrac / 3^n) ],   e(t) = exp(2 pi i t),
      Proposition 1.17 of Tao:  |phi_n(xi)| <<_A n^{-A}  for 3 nmid xi,
      uniformly in xi.  We check the *empirical* magnitude and, crucially,
      whether sup_{3 nmid xi} |phi_n(xi)| looks polynomial in 1/n
      (consistent with Tao) versus exponential in 3^{-n} (the conjectural
      beta=1 strength that natural density would want).

Because Geom(2) is unbounded we truncate the tails at a_j <= A_MAX and
renormalize; the truncation error is < n * 2^{-A_MAX}, reported below.

We compute the law of Syrac(Z/3^n Z) EXACTLY (as rationals over the
truncated support) by dynamic programming over the skew-convolution
recursion, so there is no Monte-Carlo error beyond truncation.

Author: Alex Ye with Claude (laoganpapi@gmail.com).
"""

from __future__ import annotations

import cmath
import math
from fractions import Fraction
from typing import Dict, List, Tuple


def inv_pow2_mod(m: int, modulus: int) -> int:
    """Return (2^{-m}) mod `modulus`, i.e. inverse of 2^m. Requires gcd(2,modulus)=1."""
    # 2^{-1} mod 3^n is (3^n + 1)//2 since 2 * ((3^n+1)/2) = 3^n + 1 = 1 mod 3^n.
    inv2 = (modulus + 1) // 2
    return pow(inv2, m, modulus)


def syracuse_law(n: int, a_max: int = 40) -> Tuple[Dict[int, Fraction], Fraction]:
    """
    Exact law of Syrac(Z/3^n Z) over the truncated geometric support a_j in [1, a_max].

    Uses the closed form
        Syrac = sum_{j=1}^{n} 3^{n-j} * 2^{-(a_j + ... + a_n)}   (mod 3^n).
    Let S_j = a_j + a_{j+1} + ... + a_n  (a partial *suffix* sum).  Then
        Syrac = sum_{j=1}^{n} 3^{n-j} * inv2(S_j) mod 3^n.
    We build the distribution of the vector of contributions by DP from j=n
    down to j=1, tracking (current residue mod 3^n) as we add each term, where
    S_j = a_j + S_{j+1}.  We carry the running suffix-sum's *exponent class*
    only through inv2, so we track (residue, S_current) — but S can be large,
    so instead we track residue and accumulate by conditioning on a_j directly.

    Returns (law, trunc_mass) where law maps residue -> probability (Fraction),
    and trunc_mass is the total probability mass retained (1 - truncation loss).
    """
    modulus = 3 ** n
    half = Fraction(1, 2)
    # geom pmf on [1, a_max]
    geom = {k: half ** k for k in range(1, a_max + 1)}
    retained = sum(geom.values())  # < 1 by tail 2^{-a_max}

    # DP from j = n down to j = 1.
    # State after processing terms j, j+1, ..., n is:
    #   - the partial residue  R = sum_{i=j}^{n} 3^{n-i} 2^{-S_i}  (mod 3^n)
    #   - the current suffix exponent  E = S_j = a_j + ... + a_n
    # We need E to form S_{j-1} = a_{j-1} + E for the next (outer) term.
    # dist: dict[(R, E)] -> prob.  E can be up to n*a_max; that's fine for small n.
    dist: Dict[Tuple[int, int], Fraction] = {(0, 0): Fraction(1)}
    for j in range(n, 0, -1):
        new: Dict[Tuple[int, int], Fraction] = {}
        coeff = pow(3, n - j, modulus)
        for (R, E), p in dist.items():
            for k, pk in geom.items():
                S_j = E + k  # = a_j + (a_{j+1}+...+a_n)
                term = (coeff * inv_pow2_mod(S_j, modulus)) % modulus
                R2 = (R + term) % modulus
                key = (R2, S_j)
                new[key] = new.get(key, Fraction(0)) + p * pk
        dist = new

    law: Dict[int, Fraction] = {}
    for (R, _E), p in dist.items():
        law[R] = law.get(R, Fraction(0)) + p
    total = sum(law.values())
    return law, total


def c_n_value(law: Dict[int, Fraction], n: int) -> Fraction:
    """c_n = min over b with 3 nmid b of P(Syrac = b). Support is on (Z/3^n)^x anyway."""
    modulus = 3 ** n
    best = None
    for b in range(modulus):
        if b % 3 == 0:
            continue
        p = law.get(b, Fraction(0))
        if best is None or p < best:
            best = p
    return best if best is not None else Fraction(0)


def char_fn_sup(law: Dict[int, Fraction], n: int) -> Tuple[float, int]:
    """
    Return (max over xi with 3 nmid xi of |phi_n(xi)|, argmax xi),
    phi_n(xi) = sum_b law[b] * e(-xi b / 3^n).
    """
    modulus = 3 ** n
    best = -1.0
    arg = -1
    for xi in range(1, modulus):
        if xi % 3 == 0:
            continue
        s = 0j
        ang = -2.0 * math.pi * xi / modulus
        for b, p in law.items():
            s += float(p) * cmath.exp(1j * ang * b)
        m = abs(s)
        if m > best:
            best = m
            arg = xi
    return best, arg


def tilt_check() -> bool:
    """
    Verify the descent-balance tilt s* used in tao_syracuse_explicit.md eq (5.2).
    Tilted geometric P_s(a=k) propto 2^{-k(1+s)} on k>=1 has mean 1/(1-2^{-(1+s)}).
    s* solves E_{s*}[a] = log_2 3.  Doc claims r*=2^{-(1+s*)}=0.36907, s*~0.438.
    """
    import math

    def Es(s: float) -> float:
        r = 2.0 ** (-(1.0 + s))
        return 1.0 / (1.0 - r)

    target = math.log(3, 2)
    r_star = 1.0 - 1.0 / target
    s_star = -math.log2(r_star) - 1.0
    ok = (
        abs(Es(0.0) - 2.0) < 1e-12
        and abs(Es(s_star) - target) < 1e-9
        and abs(r_star - 0.36907) < 1e-4
        and abs(s_star - 0.438) < 1e-3
    )
    print("\n[tilt s* check]")
    print("  E_0[a] = %.6f (expect 2.0); target log_2 3 = %.6f" % (Es(0.0), target))
    print("  r* = 2^{-(1+s*)} = %.6f (doc: 0.36907)" % r_star)
    print("  s* = %.6f (doc: ~0.438)" % s_star)
    print("  E_{s*}[a] = %.9f (expect = log_2 3 = %.9f)" % (Es(s_star), target))
    print("  tilt check match: %s" % ok)
    return ok


def main() -> None:
    print("=" * 72)
    print("Syracuse random variable Syrac(Z/3^n Z): structural verification")
    print("Definition cross-check against Tao arXiv:1909.03562")
    print("=" * 72)

    # ----- sanity: n = 1.  Syrac(Z/3Z) = 2^{-a_1} mod 3, a_1 ~ Geom(2).
    # 2^{-1} = 2 mod 3, 2^{-2} = 1 mod 3, 2^{-3} = 2, 2^{-4} = 1, ...
    # So Syrac mod 3 = 2 if a_1 odd (prob 2/3), = 1 if a_1 even (prob 1/3).
    # Hence law: P(1) = 1/3, P(2) = 2/3, P(0) = 0.  c_1 = 1/3.
    law1, tot1 = syracuse_law(1, a_max=40)
    print("\n[n=1]  retained mass = %s (1 - 2^{-40} ~ 1)" % (float(tot1),))
    p1 = {b: float(law1.get(b, Fraction(0)) / tot1) for b in range(3)}
    print("  P(Syrac=0)=%.6f  P(=1)=%.6f  P(=2)=%.6f" % (p1[0], p1[1], p1[2]))
    print("  EXPECTED (hand calc): 0.000000, 0.333333, 0.666667")
    ok1 = abs(p1[0]) < 1e-9 and abs(p1[1] - 1 / 3) < 1e-6 and abs(p1[2] - 2 / 3) < 1e-6
    print("  match: %s" % ok1)

    # ----- general n: report c_n, c_n * 3^n, and the char-fn sup.
    print("\n%-4s %-14s %-14s %-16s %-16s" % ("n", "c_n", "c_n*3^n", "sup|phi(xi)|", "argmax xi"))
    rows = []
    cn_norm = {}
    for n in range(1, 6):
        law, tot = syracuse_law(n, a_max=40)
        # renormalize to remove truncation mass
        law = {b: p / tot for b, p in law.items()}
        cn = c_n_value(law, n)
        cn3 = float(cn) * (3 ** n)
        cn_norm[n] = float(cn)
        sup, arg = char_fn_sup(law, n)
        rows.append((n, float(cn), cn3, sup, arg))
        print("%-4d %-14.3e %-14.6f %-16.6f %-16d" % (n, float(cn), cn3, sup, arg))

    # ----- submultiplicativity check: c_{n1+n2-1} >= c_{n1} c_{n2}
    print("\nSubmultiplicativity  c_{n1+n2-1} >= c_{n1} c_{n2}  (Tao 2020 blog):")
    allgood = True
    for n1 in range(1, 4):
        for n2 in range(1, 4):
            n3 = n1 + n2 - 1
            if n3 in cn_norm and n1 in cn_norm and n2 in cn_norm:
                lhs = cn_norm[n3]
                rhs = cn_norm[n1] * cn_norm[n2]
                good = lhs >= rhs - 1e-15
                allgood = allgood and good
                print("  n1=%d n2=%d: c_%d=%.4e >= c_%d*c_%d=%.4e  %s"
                      % (n1, n2, n3, lhs, n1, n2, rhs, "OK" if good else "FAIL"))
    print("  submultiplicativity holds on tested range: %s" % allgood)

    # ----- the key qualitative question for the theory doc:
    # Does sup|phi_n(xi)| decay only polynomially in 1/n (Tao, n^{-A}),
    # and does c_n * 3^n shrink (so c_n > 3^{-n} strictly fails to be ~1)?
    print("\nKEY OBSERVATIONS for the log->natural analysis:")
    print("  c_n * 3^n column: if this stays >= constant, beta=1 (c_n ~ 3^{-n}) holds for small n.")
    print("  sup|phi| column : Tao proves this is <<_A n^{-A}; for small n it is O(1),")
    print("                    decay only becomes visible at larger n (not reachable by brute force).")
    print("  (These small-n values are a definitional sanity check, NOT a test of the")
    print("   asymptotic Fourier bound, which lives at n -> infinity.)")

    tilt_check()


if __name__ == "__main__":
    main()
