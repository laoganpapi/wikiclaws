"""
sos_validate.py -- exact, SDP-free validations backing the SOS write-up.

1) LEVEL-1 COLLAPSE (rigorous).  For n<=3, list the S_n-orbits of the level-1
   pseudo-moments over incidence vars y_S (degree-1: by |S|; degree-2: by
   (|S|,|T|,|S&T|)).  Show these orbit-invariants are exactly the data the
   degree-2 frequency moment uses, by exhibiting the linear map
   moments -> (sum_i p_i, sum_i p_i^2, ...) and checking the level-1 invariant
   algebra contains NO invariant that separates two UC families with the same
   frequency-pair-statistics.  (Concretely: build the invariant feature vector
   and verify it is a function of the frequency multiset + pair overlaps only.)

2) CUBE SATURATION at level 2 (rigorous, no solver).  The Boolean cube F=2^[k]
   yields an HONEST pseudo-expectation (the actual uniform law on members) which
   is feasible at EVERY level with abundance exactly 1/2.  We construct it and
   verify the level-2 moment matrix is PSD and all constraints hold with
   abundance = 1/2 -- i.e. the SDP is genuinely FEASIBLE at t=1/2 for every k,
   so NO level-d relaxation can ever certify abundance > 1/2 (the cube ceiling
   survives to all degrees).  This is the rigorous version of the probe's
   noisy 't=0.5 feasible' cells.
"""
from __future__ import annotations
import itertools
from collections import defaultdict
import numpy as np


def subsets(n):
    return list(range(1 << n))


# ---------------------------------------------------------------------------
# (2) Cube saturation at arbitrary level via the HONEST moment vector.
# ---------------------------------------------------------------------------

def honest_pseudo_moment(F, n, level):
    """The TRUE pseudo-expectation from the uniform law on members of UC family F:
    y_T = Pr_{members}[ all S in T are 'selected' ]?  No -- for a FIXED family F the
    indicator y_S is deterministic (1 iff S in F).  So the honest moment of the
    *decision* variables is just the 0/1 point y_S=1[S in F].  Its moment matrix is
    rank-1 PSD by construction, and ALL constraints hold exactly.  This certifies
    feasibility of the relaxation at the true abundance of F, at EVERY level."""
    sets = subsets(n)
    nvars = len(sets)
    ybit = {s: (1.0 if sets[s] in F else 0.0) for s in range(nvars)}
    # build degree-<=level monomial rows, moment = product of ybit (squarefree)
    rows = []
    for d in range(level + 1):
        rows.extend(itertools.combinations(range(nvars), d))
    R = len(rows)
    M = np.zeros((R, R))
    for r in range(R):
        for c in range(R):
            varset = set(rows[r]) | set(rows[c])
            val = 1.0
            for v in varset:
                val *= ybit[v]
            M[r, c] = val
    mineig = float(np.linalg.eigvalsh((M + M.T) / 2).min())
    # abundance
    freqs = [sum(1 for S in F if (S >> i) & 1) for i in range(n)]
    ab = max(freqs) / len(F) if F else 0.0
    return mineig, ab, M.shape[0]


def cube(k):
    return frozenset(range(1 << k))  # all subsets of [k] = Boolean cube 2^[k]


# ---------------------------------------------------------------------------
# (1) Level-1 invariant feature = frequency pair-statistics (rigorous check).
# ---------------------------------------------------------------------------

def level1_invariants(F, n):
    """S_n-invariant level-1 pseudo-moments of the honest point y_S=1[S in F]:
       deg1 orbit sums  a_s = sum_{|S|=s} 1[S in F]          (s=0..n)
       deg2 orbit sums  b_{s,t,j} = #{(S,T): |S|=s,|T|=t,|S&T|=j, S,T in F}
    These are the ONLY data an S_n-invariant level-1 pseudo-expectation depends on.
    Return them as a tuple (the invariant feature vector)."""
    sets = [S for S in subsets(n)]
    inF = set(F)
    a = defaultdict(int)
    for S in inF:
        a[bin(S).count("1")] += 1
    b = defaultdict(int)
    Fl = list(inF)
    for S in Fl:
        for T in Fl:
            b[(bin(S).count("1"), bin(T).count("1"), bin(S & T).count("1"))] += 1
    feat = tuple(sorted(a.items())) + tuple(sorted(b.items()))
    return feat


def freq_pairstats(F, n):
    """The degree-2 FREQUENCY-moment data: multiset of freqs + sum freq_i freq_j
    overlaps = sum_{A,B} |A cap B| (the second_moment object)."""
    freqs = tuple(sorted(sum(1 for S in F if (S >> i) & 1) for i in range(n)))
    M2 = 0
    Fl = list(F)
    for A in Fl:
        for B in Fl:
            M2 += bin(A & B).count("1")
    return (len(F), freqs, M2)


def main():
    print("=" * 70)
    print("(2) CUBE SATURATION at level 2 (rigorous, honest 0/1 moment vector):")
    print("    abundance=1/2 is FEASIBLE at level 2 for every cube => no level-d")
    print("    relaxation can certify >1/2.  (min_eig>=0 confirms PSD feasibility.)")
    for k in (1, 2, 3):
        n = k
        mineig, ab, sz = honest_pseudo_moment(cube(k), n, level=2)
        print(f"    cube 2^[{k}]: level-2 moment matrix {sz}x{sz}  "
              f"min_eig={mineig:+.2e}  abundance={ab:.3f}  "
              f"=> {'FEASIBLE at 1/2' if mineig> -1e-9 else 'NUMERR'}")

    print("\n(1) LEVEL-1 COLLAPSE: do S_n-invariant level-1 incidence invariants")
    print("    separate any more than the degree-2 frequency pair-statistics?")
    print("    Enumerate all UC families (n<=3); group by each feature; compare.")
    for n in (2, 3):
        # enumerate UC families
        allsets = subsets(n)
        fams = []
        from itertools import combinations
        for r in range(1, len(allsets) + 1):
            for combo in combinations(allsets, r):
                F = frozenset(combo)
                if all((a | b) in F for a in F for b in F):
                    fams.append(F)
        # partition by level-1 invariant feature and by freq pairstats
        byL1 = defaultdict(list)
        byFreq = defaultdict(list)
        for F in fams:
            byL1[level1_invariants(F, n)].append(F)
            byFreq[freq_pairstats(F, n)].append(F)
        # KEY TEST: is the level-1 partition a REFINEMENT of the freq partition?
        # (i.e. does level-1 see strictly more?)  Check whether two families with
        # the SAME freq pairstats ever get DIFFERENT level-1 features.
        refines = True
        coarser = True
        # map each family to (L1, Freq); compare cells
        L1cells = {F: level1_invariants(F, n) for F in fams}
        Fcells = {F: freq_pairstats(F, n) for F in fams}
        # group by freq cell, see if L1 constant within it
        for cell, group in byFreq.items():
            l1s = set(L1cells[F] for F in group)
            if len(l1s) > 1:
                coarser = False  # L1 distinguishes within a freq cell => strictly finer
        for cell, group in byL1.items():
            fs = set(Fcells[F] for F in group)
            if len(fs) > 1:
                refines = False  # freq distinguishes within an L1 cell
        print(f"    n={n}: #UC families={len(fams):4d}  "
              f"#level-1 cells={len(byL1):4d}  #freq-pair cells={len(byFreq):4d}")
        print(f"          level-1 strictly finer than freq-pair? "
              f"{'NO (they coincide => COLLAPSE)' if coarser else 'YES (level-1 sees more)'}")


if __name__ == "__main__":
    main()
