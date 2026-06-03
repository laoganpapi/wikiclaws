"""
jordan_probe.py -- ergodic-theory generation probe.

Two concrete computations on the EXACT Syracuse transfer operator P_n
(reusing the exact rational kernel idea from collatz/experiments/perp_gap.py):

(A) JORDAN / nilpotent-tower structure of N := P_n - Pi (Pi = rank-1 stationary
    projector).  We already know (perp_gap.md) N is nilpotent of index n with
    rank(P^k)=2*3^{n-1-k}.  QUESTION: does the generalized-eigenvector flag of N
    coincide with the mod-3^k coset filtration V^(1) c V^(2) c ... c V^(n) ?
    If ker(N^k) = (mod-3^{n-k+1}-measurable functions), the nilpotent tower is
    EXACTLY a graded "descent / scale" filtration -- a Pollicott-Ruelle resonance
    ladder where each rung strips one 3-adic digit.  We test this exactly over Q.

(B) JOINING / disjointness probe.  Drift D_k = (a_1+...+a_k) - k*log2(3) is the
    log-size change; residue R = Syrac mod 3^n.  Sarnak/Furstenberg-style
    disjointness would want the (R, sign of cumulative drift) process to be
    asymptotically a PRODUCT (independent) -- i.e. residue carries NO information
    about whether the orbit is currently descending.  We measure the mutual
    information I(R mod 3 ; a_n parity) and I(R ; first-passage descent event)
    on the exact law, to see if there is a residue<->drift COUPLING (the obstruction
    of natural_density_obstruction.md Prop 4.2) that a joining argument must break.

Pure self-contained; uses only sympy + numpy + python stdlib.  Writes nothing
outside this _probe dir's stdout.
"""
from __future__ import annotations
from fractions import Fraction
import sympy as sp
import numpy as np
import itertools, math


def units_mod(n):
    mod = 3 ** n
    return [x for x in range(1, mod) if x % 3 != 0]


def exact_kernel(n):
    """Exact rational one-step Syracuse kernel P_n on (Z/3^n)^x (untilted Geom(2))."""
    mod = 3 ** n
    U = units_mod(n)
    idx = {u: i for i, u in enumerate(U)}
    sz = len(U)
    L = 2 * 3 ** (n - 1)
    i2 = (mod + 1) // 2
    denom = 1 - Fraction(1, 2 ** L)
    P = [[Fraction(0) for _ in range(sz)] for _ in range(sz)]
    cur = 1
    invs, weights = [], []
    for r in range(1, L + 1):
        cur = (cur * i2) % mod
        invs.append(cur)
        weights.append(Fraction(1, 2 ** r) / denom)
    for i, x in enumerate(U):
        v = (3 * x + 1) % mod
        for r in range(L):
            y = (v * invs[r]) % mod
            P[i][idx[y]] += weights[r]
    return P, U


def to_sympy(P):
    return sp.Matrix([[sp.Rational(c.numerator, c.denominator) for c in row] for row in P])


def mod3k_subspace_dim_in_kernel(n):
    """
    (A) Compare the nilpotent flag ker(N^k) to the mod-3^j coset filtration.

    V^(j) := span of indicator functions of residue classes mod 3^j  (as COLUMN
    functions on U_n), dimension phi(3^j) = 2*3^{j-1}.  These are P_n-invariant
    (perp_gap / transfer_operator sec 3.1).  N = P - Pi.  We compute dim ker(N^k)
    and check whether ker(N^k) equals the span of {1} + (V^(j) for the matching j).

    Returns a table: for each k, dim ker(N^k), and the matching coset level.
    """
    P, U = exact_kernel(n)
    N = len(U)
    M = to_sympy(P)
    # stationary pi (left eigenvector), Pi = 1 (x) pi
    A = M.T - sp.eye(N)
    pi = A.nullspace()[0]
    pi = pi / sum(pi)
    ones = sp.ones(N, 1)
    Pi = ones * pi.T  # rank-1 projector onto stationary line (row pi, col 1)
    Nil = M - Pi

    # coset-indicator subspaces V^(j): columns = indicators of residue class mod 3^j
    def Vsub(j):
        mod = 3 ** j
        classes = {}
        for i, u in enumerate(U):
            classes.setdefault(u % mod, []).append(i)
        cols = []
        for r, idxs in classes.items():
            v = sp.zeros(N, 1)
            for i in idxs:
                v[i] = 1
            cols.append(v)
        return sp.Matrix.hstack(*cols)

    Vdims = {j: Vsub(j).shape[1] for j in range(1, n + 1)}

    rows = []
    cur = sp.eye(N)
    for k in range(0, n + 1):
        if k > 0:
            cur = cur * Nil
        kerdim = N - cur.rank()
        # find coset level j with phi(3^j)=2*3^{j-1} closest from below matching kerdim
        rows.append((k, kerdim))
    return rows, Vdims, U, M, Nil


def kernel_equals_coset_flag(n):
    """
    Sharper (A): test the EXACT set equality  ker(N^k) ?= column-span(V^(n-k))
    (suitably including the stationary direction).  We test via rank of the
    stacked basis.  If equal, the nilpotent tower IS the 3-adic scale filtration.
    """
    P, U = exact_kernel(n)
    N = len(U)
    M = to_sympy(P)
    A = M.T - sp.eye(N)
    pi = A.nullspace()[0]; pi = pi / sum(pi)
    Pi = sp.ones(N, 1) * pi.T
    Nil = M - Pi

    def Vsub_cols(j):
        mod = 3 ** j
        classes = {}
        for i, u in enumerate(U):
            classes.setdefault(u % mod, []).append(i)
        cols = []
        for r, idxs in classes.items():
            v = sp.zeros(N, 1)
            for i in idxs:
                v[i] = 1
            cols.append(v)
        return cols

    results = []
    curpow = sp.eye(N)
    for k in range(0, n + 1):
        if k > 0:
            curpow = curpow * Nil
        # ker(N^k) basis
        ker = curpow.nullspace()
        kdim = len(ker)
        # candidate coset level: we expect ker(N^k) ~ functions measurable mod 3^k
        # (image side) -- test against V^(k): is V^(k) subset ker(N^k)?
        if 1 <= k <= n:
            vcols = Vsub_cols(k)
            stacked = sp.Matrix.hstack(*(ker + vcols)) if ker else sp.Matrix.hstack(*vcols)
            rank_union = stacked.rank()
            # V^(k) subset ker(N^k)  iff  rank(ker) == rank(ker + V^(k))
            ker_only_rank = sp.Matrix.hstack(*ker).rank() if ker else 0
            v_in_ker = (rank_union == ker_only_rank)
            vdim = len(vcols)
            results.append((k, kdim, vdim, v_in_ker))
        else:
            results.append((k, kdim, None, None))
    return results


def joining_mutual_info(n):
    """
    (B) Exact law of Syrac mod 3^n via DP over the n geometric valuations.
    Compute:
      - I(R mod 3 ; parity of a_n)   [should be HIGH: residue mod 3 == (-1)^a_n]
      - I(R mod 3^n ; total drift sign)   proxy for residue<->descent coupling.
    We compute the JOINT law of (R, S) where S = sum a_j (the log-drift driver),
    truncating the geometric tail at a_max and renormalizing.
    """
    mod = 3 ** n
    a_max = 40
    inv2 = pow(2, -1, mod)
    # joint law over (residue, total S=sum a_j).  state: build offset incrementally.
    # F_n = sum_{j=1}^n 3^{n-j} 2^{-(a_j+...+a_n)}.  Process j=n down to 1.
    # Maintain dist over (partial residue, suffix_valuation_sum used so far) is heavy;
    # instead sample exhaustively over (a_1..a_n) with weights -- feasible for small n.
    pa = [Fraction(1, 2 ** k) for k in range(1, a_max + 1)]
    Z = sum(pa); pa = [p / Z for p in pa]
    joint_R_anpar = {}      # (R mod 3, a_n parity) -> prob
    joint_R_Ssign = {}      # (R mod 3, sign(S - n*1.585)) -> prob
    drift_thresh = n * math.log(3, 2)
    # enumerate -- limit total combos
    if a_max ** n > 4_000_000:
        a_max_eff = max(2, int(round(4_000_000 ** (1.0 / n))))
    else:
        a_max_eff = a_max
    pae = pa[:a_max_eff]
    Ze = sum(pae); pae = [p / Ze for p in pae]
    for combo in itertools.product(range(1, a_max_eff + 1), repeat=n):
        w = 1.0
        for k in combo:
            w *= float(pae[k - 1])
        # residue
        suf = 0
        R = 0
        for j in range(n, 0, -1):
            suf += combo[j - 1]
            term = (3 ** (n - j)) * pow(inv2, suf, mod) % mod
            R = (R + term) % mod
        an_par = combo[-1] % 2
        S = sum(combo)
        Ssign = 1 if S >= drift_thresh else 0
        joint_R_anpar[(R % 3, an_par)] = joint_R_anpar.get((R % 3, an_par), 0.0) + w
        joint_R_Ssign[(R % 3, Ssign)] = joint_R_Ssign.get((R % 3, Ssign), 0.0) + w
    return joint_R_anpar, joint_R_Ssign, a_max_eff


def mutual_information(joint):
    tot = sum(joint.values())
    j = {k: v / tot for k, v in joint.items()}
    px = {}; py = {}
    for (x, y), p in j.items():
        px[x] = px.get(x, 0.0) + p
        py[y] = py.get(y, 0.0) + p
    I = 0.0
    for (x, y), p in j.items():
        if p > 0:
            I += p * math.log2(p / (px[x] * py[y]))
    return I


if __name__ == "__main__":
    print("=" * 72)
    print("(A) Nilpotent flag  ker(N^k)  vs  mod-3^k coset subspace V^(k)")
    print("=" * 72)
    for n in range(1, 6):
        rows = kernel_equals_coset_flag(n)
        print(f"\n n={n}  (size phi(3^n)={2*3**(n-1)})")
        print(f"  {'k':>3} {'dim ker(N^k)':>13} {'dim V^(k)':>10} {'V^(k) ⊆ ker(N^k)?':>18}")
        for (k, kdim, vdim, v_in) in rows:
            print(f"  {k:>3} {kdim:>13} {str(vdim):>10} {str(v_in):>18}")

    print()
    print("=" * 72)
    print("(B) Residue <-> drift coupling (the joining/disjointness obstruction)")
    print("=" * 72)
    for n in range(1, 5):
        jpar, jS, amax = joining_mutual_info(n)
        I_par = mutual_information(jpar)
        I_S = mutual_information(jS)
        print(f" n={n} (a_max_eff={amax}): "
              f"I(R mod3 ; a_n parity)={I_par:.4f} bits, "
              f"I(R mod3 ; drift-sign)={I_S:.4f} bits")
