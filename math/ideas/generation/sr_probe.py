"""
sr_probe.py  --  Stanley-Reisner / monomial-resolution probe for Frankl.
Lives under math/ideas/generation/ (idea generation only; touches nothing else).

SET-UP.  Encode a union-closed family F (over [n]) as squarefree monomials:
    A in F  <->  m_A = prod_{i in A} x_i  in  k[x_1..x_n].
Then  union = lcm,  so F union-closed  <=>  {m_A} is closed under lcm
    <=>  the LCM-LATTICE of the monomial ideal  I_F = ( m_A : A a MINIMAL member )
         is exactly  L = (F, subset, union).
By Gasharov-Peeva-Welker, the multigraded Betti numbers of I_F are
    beta_{i, A}(I_F) = dim_k  H~_{i-2}( open interval (0hat, A) in L ),   A in L,
so the WHOLE free resolution is read off the order complexes of open intervals of L.

TWO regimes, and the cone test that separates them:
 * The Z-graded (coarse) Betti numbers / projective dimension / regularity are
   determined by the ABSTRACT lattice L up to relabeling => KILLED by the cone
   (lattice_attack.md sec.4: cone(G) ~= G as a lattice, abundance .5 -> 1-1/|L|).
   We compute them as a CONTROL and expect them flat/dead under coning.
 * The FINE multigrading beta_{i,A} is indexed by the actual subsets A<=[n]; the
   cone shifts every multidegree A -> A u {z}.  The "abundant element" shows up
   homologically as a variable x_z that DIVIDES every minimal generator (a cone
   apex of the support complex): then projdim drops and z is in every facet.
   We test exactly this bridge: does a homological "splitting/apex" variable force
   abundance >= 1/2, and is the cube NON-degenerate for it?

Invariants per family (F with emptyset adjoined as 0hat):
  - abundance = max_x freq(x)/|F|
  - projdim, reg, total Betti of I_F via lcm-lattice open-interval homology (GPW)
  - the multidegree-A homology profile: max over x of
        S(x) := sum_{A : x in A} dim H~(open interval (0,A))     [labelling-weighted]
    and whether argmax_x S(x) is an abundant element.
  - "common divisor" / cone-apex variable: x dividing every minimal generator.

Run:  python3 sr_probe.py 5
"""
from __future__ import annotations
import sys, os, json, itertools
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.normpath(os.path.join(HERE, "..", "..", "frankl", "experiments"))
sys.path.insert(0, EXP)
from enumerate import all_uc_families  # noqa: E402
from uc_family import frequencies, ground_set  # noqa: E402


# --------------------------------------------------------------------------
# F_p rank for boundary maps (faithful Betti for the tiny complexes here)
# --------------------------------------------------------------------------
def _rank_mod_p(rows, p=1000003):
    M = [list(r) for r in rows]
    if not M:
        return 0
    ncol = len(M[0])
    rank, col, nrow, r = 0, 0, len(M), 0
    while r < nrow and col < ncol:
        piv = next((i for i in range(r, nrow) if M[i][col] % p), None)
        if piv is None:
            col += 1
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][col] % p, p - 2, p)
        M[r] = [(v * inv) % p for v in M[r]]
        for i in range(nrow):
            if i != r and M[i][col] % p:
                f = M[i][col] % p
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
        rank += 1
        col += 1
    return rank


def reduced_betti_of_poset_open_interval(elements, leq):
    """Reduced Betti numbers H~_k of the ORDER COMPLEX of a poset given by its
    element list and a leq(a,b) predicate (strict order used for chains).
    elements: list; returns list b[k] for k = -1, 0, 1, ...  (k = chain_len-2).
    Order complex faces = chains (totally ordered subsets), reduced homology."""
    els = list(elements)
    # build all chains (antisymmetric: a<b)
    def lt(a, b):
        return a != b and leq(a, b)
    # faces = nonempty chains + empty face
    # enumerate chains by extending
    chains = [tuple()]  # empty face (dim -1)
    # singletons
    singles = [(e,) for e in els]
    frontier = list(singles)
    chains.extend(singles)
    while frontier:
        nf = []
        for ch in frontier:
            top = ch[-1]
            for e in els:
                if lt(top, e):
                    nc = ch + (e,)
                    nf.append(nc)
        chains.extend(nf)
        frontier = nf
    # group by dim
    by_dim = {}
    for ch in chains:
        by_dim.setdefault(len(ch) - 1, []).append(ch)
    if not by_dim:
        return []
    maxd = max(by_dim)
    for d in by_dim:
        by_dim[d].sort()
    idx = {d: {f: i for i, f in enumerate(by_dim[d])} for d in by_dim}
    ranks = {}
    for k in range(0, maxd + 1):
        if k not in by_dim or (k - 1) not in by_dim:
            ranks[k] = 0
            continue
        mat = []
        for f in by_dim[k]:
            col = [0] * len(idx[k - 1])
            for j in range(len(f)):
                face = f[:j] + f[j + 1:]
                col[idx[k - 1][face]] += -1 if (j % 2) else 1
            mat.append(col)
        ranks[k] = _rank_mod_p(mat)
    betti = []
    for k in range(-1, maxd + 1):
        ck = len(by_dim.get(k, []))
        betti.append(ck - ranks.get(k, 0) - ranks.get(k + 1, 0))
    return betti


# --------------------------------------------------------------------------
# GPW: betti_{i,A} = H~_{i-2}( open interval (0hat, A) )
# --------------------------------------------------------------------------
def gpw_betti(masks):
    """masks: the UC family WITH 0 (emptyset) as bottom.
    Returns:
      total_betti (Z-graded, summed),
      projdim,
      betti_by_A: dict A -> total reduced betti of open interval (0,A)
                  (= sum_i beta_{i,A}),
      pos_homology_degrees: list of A (as int masks) carrying nonzero homology.
    The element 0hat itself has trivial interval; atoms (covers of 0) give the
    generators (homology in degree -1 of empty interval -> beta_{0,A})."""
    L = sorted(set(masks) | {0})
    Lset = set(L)

    def leq(a, b):
        return (a & b) == a

    betti_by_A = {}
    pos = []
    total = 0
    projdim = 0
    for A in L:
        if A == 0:
            continue
        # open interval (0, A) = { z : 0 < z < A } = { z in L : z|A, z!=0, z!=A }
        inter = [z for z in L if z != 0 and z != A and (z & A) == z]
        if not inter:
            # empty interval: H~_{-1} = k  -> beta_{0,A} (a generator) if A is an atom
            b = [1]  # reduced betti of empty complex: b_{-1}=1
        else:
            b = reduced_betti_of_poset_open_interval(inter, leq)
        # beta_{i,A} = b_{i-2}, i.e. homology in degree (i-2). i ranges:
        tb = sum(abs(v) for v in b)
        betti_by_A[A] = tb
        total += tb
        if tb:
            pos.append(A)
        # projective dimension contribution: max i with beta_{i,A}>0.
        # b is indexed k=-1,0,1,...; beta index i = k+2.
        for k, v in enumerate(b, start=-1):
            if v:
                projdim = max(projdim, k + 2)
    return total, projdim, betti_by_A, pos


# --------------------------------------------------------------------------
def minimal_members(masks):
    ms = [m for m in masks if m != 0]
    out = []
    for a in ms:
        if not any(a != b and (b & a) == b for b in ms):  # b proper subset of a
            out.append(a)
    return out


def common_divisor_vars(masks, n):
    """variables x dividing EVERY minimal generator (cone apex of the resolution);
    forces that x is in every minimal member -> in every member by up-closure."""
    gens = minimal_members(masks)
    if not gens:
        return []
    return [x for x in range(n) if all(g & (1 << x) for g in gens)]


def main(nmax):
    rows = []
    for n in range(0, nmax + 1):
        for F in all_uc_families(n):
            if not F:
                continue
            masks = set(F) | {0}
            nn = ground_set(frozenset(masks))
            if nn == 0:
                continue
            freqs = frequencies(list(masks), nn)
            sizeF = len(masks)
            abund = max(freqs) / sizeF

            total, projdim, betti_by_A, pos = gpw_betti(masks)

            # labelling-weighted homology load per ground element x:
            # S(x) = sum_{A : x in A} betti_by_A[A]
            S = [0] * nn
            for A, tb in betti_by_A.items():
                for x in range(nn):
                    if A & (1 << x):
                        S[x] += tb
            best_x_S = max(range(nn), key=lambda x: (S[x], freqs[x]))
            # is the homology-heaviest element the abundance-heaviest?
            argmax_freq = max(range(nn), key=lambda x: freqs[x])
            S_picks_abundant = (freqs[best_x_S] == max(freqs))

            cdvars = common_divisor_vars(masks, nn)

            rows.append({
                "n": nn, "sizeF": sizeF, "abund": round(abund, 6),
                "total_betti": total, "projdim": projdim,
                "n_pos_homology": len(pos),
                "S": S, "best_x_S": best_x_S,
                "S_picks_abundant": S_picks_abundant,
                "freq_best_xS": freqs[best_x_S],
                "max_freq": max(freqs),
                "n_common_div": len(cdvars),
                "freqs": sorted(freqs, reverse=True),
                "freq_vec": list(freqs),   # aligned with S, per-element
            })
    return rows


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    rows = main(nmax)
    with open(os.path.join(HERE, f"sr_probe_n{nmax}.jsonl"), "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")

    import statistics
    N = len(rows)
    print(f"# families (emptyset adjoined, nonempty ground): {N}")

    # ---- CONTROL: is total_betti / projdim flat-on-cube and abundance-blind? ----
    print("\n[CONTROL] coarse homology vs abundance (expect DEAD by cone):")
    cubes = [r for r in rows if r["sizeF"] in (2, 4, 8, 16, 32)
             and r["abund"] == 0.5 and len(set(r["freqs"])) == 1]
    for r in sorted({(r["sizeF"],) : r for r in cubes}.values(),
                    key=lambda r: r["sizeF"]):
        print(f"  cube |F|={r['sizeF']:2d}: total_betti={r['total_betti']} "
              f"projdim={r['projdim']} n_pos_homology={r['n_pos_homology']}")
    lo = [r["total_betti"] for r in rows if r["abund"] < 0.55]
    hi = [r["total_betti"] for r in rows if r["abund"] >= 0.55]
    if lo and hi:
        print(f"  total_betti  abund<.55: mean {statistics.mean(lo):.2f} "
              f"max {max(lo)} | abund>=.55: mean {statistics.mean(hi):.2f} "
              f"max {max(hi)}  -> overlap means coarse Betti does NOT separate")

    # ---- TEST 1: common-divisor (cone-apex) variable forces abundance? ----
    cd = [r for r in rows if r["n_common_div"] > 0]
    print(f"\n[TEST1] families with a common-divisor variable (resolution cone "
          f"apex): {len(cd)} / {N}")
    if cd:
        # such a variable is in every minimal member => in every member => freq=|F|
        print(f"  all such families have abundance 1.0? "
              f"{all(r['abund'] == 1.0 for r in cd)}  "
              f"(min abund {min(r['abund'] for r in cd):.4f})")
    nocd = [r for r in rows if r["n_common_div"] == 0]
    print(f"  families with NO common divisor: {len(nocd)}; "
          f"their min abundance {min(r['abund'] for r in nocd):.4f} "
          f"(these are the real Frankl content)")

    # ---- TEST 2: does the homology-weighted heaviest element pick an abundant one? ----
    picks = [r for r in rows if r["S_picks_abundant"]]
    print(f"\n[TEST2] 'homology-weighted-heaviest element is abundance-heaviest': "
          f"{len(picks)} / {N}  ({100*len(picks)/N:.1f}%)")
    miss = [r for r in rows if not r["S_picks_abundant"]]
    if miss:
        print(f"  misses: {len(miss)}; example freqs/S of a miss:")
        m = miss[0]
        print(f"    n={m['n']} |F|={m['sizeF']} abund={m['abund']} "
              f"freqs={m['freqs']} S={m['S']}")

    # ---- TEST 3: candidate inequality  abundance >= f(S) ? ----
    # normalized homology load of the heaviest element:
    print("\n[TEST3] does S-heaviest element clear 1/2 frequency?")
    viol = [r for r in rows if r["freq_best_xS"] / r["sizeF"] < 0.5]
    print(f"  families where S-heaviest element has freq/|F| < 1/2: {len(viol)} "
          f"/ {N}")
    if viol:
        worst = min(viol, key=lambda r: r["freq_best_xS"] / r["sizeF"])
        print(f"  worst: freq/|F|={worst['freq_best_xS']/worst['sizeF']:.4f} "
              f"abund={worst['abund']} freqs={worst['freqs']} S={worst['S']}")

    # ---- TEST 4 (INVERTED): is the abundant element the homology-LIGHTEST /
    #      most cone-apex-like one?  (S(x) small <=> x trivializes homology) ----
    def lightest_clears(r):
        S = r["S"]; fv = r["freq_vec"]; nn = r["n"]
        mn = min(S)
        cands = [x for x in range(nn) if S[x] == mn]
        # pick the most frequent among homology-lightest (break ties toward heavy)
        x = max(cands, key=lambda i: fv[i])
        return fv[x] / r["sizeF"]
    inv_viol = [r for r in rows if lightest_clears(r) < 0.5]
    print(f"\n[TEST4 INVERTED] 'homology-LIGHTEST element clears 1/2 freq': "
          f"fails {len(inv_viol)} / {N}")
    if inv_viol:
        w = min(inv_viol, key=lambda r: lightest_clears(r))
        print(f"  worst: freq/|F|={lightest_clears(w):.4f} abund={w['abund']} "
              f"freqs={w['freqs']} S={w['S']} freq_vec={w['freq_vec']}")

    # ---- TEST 5: correlation sign of (freq, S) within each family ----
    import statistics
    neg = pos = zero = 0
    for r in rows:
        S = r["S"]; fv = r["freq_vec"]; nn = r["n"]
        if nn < 2 or len(set(S)) == 1 or len(set(fv)) == 1:
            zero += 1
            continue
        # sign of Pearson-ish: compare ranking
        mf = statistics.mean(fv); ms = statistics.mean(S)
        cov = sum((fv[i] - mf) * (S[i] - ms) for i in range(nn))
        if cov > 1e-9:
            pos += 1
        elif cov < -1e-9:
            neg += 1
        else:
            zero += 1
    print(f"\n[TEST5] within-family cov(freq, S): "
          f"positive {pos}, NEGATIVE {neg}, flat/zero {zero}  "
          f"(negative => abundant element is homology-light, an APEX, "
          f"as the parasite mechanism predicts)")
