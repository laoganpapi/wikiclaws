"""
frankl_isotypic.py -- Aut(L)-isotypic decomposition of the abundance/frequency
data of a union-closed family, to expose NON-SYMMETRIC structure invisible to the
S_n-symmetric convex moments that the proven barrier flat-minimizes at the cube.

Author: representation-theory generation agent (idea-search, NOT a proof).
Status: [NOVELTY UNVERIFIED].  Direction-finding numerics only.

CONTEXT (frankl/theory/{boolean_fourier,join_irreducible_labelling}.md):
  * BARRIER: every S_n-SYMMETRIC convex moment of the frequency vector
    (freq_x)_{x in [n]} is flat-minimized by the Boolean cube at abundance 1/2.
    Symmetric moments only see the average / the S_n-trivial component.
  * The prior Boolean-Fourier attack used ABELIAN (Z/2)^n characters; quadratic
    statistics are flat on the cube.  It FAILED.
  * Frankl  <=>  some fibre Fib(x) = { A in F : x in A } has density >= 1/2.
  * Fib(x) = union of principal JI-filters (reconstruction identity (R)); abundance
    is a UNION-of-filters quantity, NOT a single-JI quantity (H1 false).

THE NON-ABELIAN / ISOTYPIC IDEA.
  G := Aut(L) (lattice automorphisms) acts on the ground set [n] (equivalently
  permutes the join-irreducibles), hence permutes the fibres:  Fib(g.x) = g.Fib(x),
  so the frequency vector  v = (|Fib(x)|)_x  is G-INVARIANT (v in the trivial
  isotype of the permutation rep C^[n] under G).  GOOD NEWS / GOOD NEWS:
   - The S_n-symmetric barrier only controls the S_n-trivial (constant) component
     <v,1>/n = mean frequency, which the cube pins at exactly 1/2.
   - But C^[n] as a G = Aut(L)-module decomposes into ISOTYPES
        C^[n] = trivial  (+)  (nontrivial isotypes W_rho).
     The barrier is blind to the nontrivial isotypes.  KEY DIAGNOSTIC:
     does abundance correlate with a NON-symmetric, G-equivariant functional that
     is supported on the nontrivial isotypes?  If a fixed such functional separates
     "cube (abundance exactly 1/2)" from "all other lattices (abundance > 1/2)",
     it escapes the symmetric-moment barrier.

  Concretely we build, for each UC family:
    (1) the permutation rep of G = Aut(L) on [n], its isotypic projectors
        (via the group-algebra averaging / Reynolds operator, Maschke/Peter-Weyl);
    (2) the per-element frequency vector v and the JI-overlap matrix
        M[x,y] = |Fib(x) cap Fib(y)| / |L|   (the SECOND-order fibre data the
        symmetric first moment discards);
    (3) the G-isotypic decomposition of M (a G-equivariant operator on C^[n]):
        block-diagonalize M by isotype, and read the spectrum of the NONTRIVIAL
        blocks.  The brief's thesis: the cube is the UNIQUE lattice whose nontrivial
        isotypic blocks of M are degenerate/flat, while every other lattice has a
        nontrivial-isotype signal -- a genuinely non-symmetric separator.

  WHY IT ESCAPES THE BARRIER.  Symmetric convex moments factor through the
  S_n-orbit-average == the trivial isotype.  A functional reading the nontrivial
  Aut(L)-isotypes of M is by construction orthogonal to every symmetric moment, so
  the "flat at the cube" barrier (which is a statement about the trivial component)
  does not apply.  The Boolean cube has Aut = S_n acting transitively with the
  permutation rep = trivial (+) standard; we test whether on the cube the
  *abundance-carrying* part of M sits ENTIRELY in the trivial isotype (=> any
  separator must use the standard/nontrivial isotype, which is exactly what
  symmetric moments cannot see).

Run:  python3 frankl_isotypic.py [n_max]
Writes data/frankl_isotypic.json + prints a verdict.
"""
from __future__ import annotations
import json, os, sys, itertools
from fractions import Fraction
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA, exist_ok=True)


# --------------------------------------------------------------------------
# Minimal union-closed family enumeration up to n (orbit reps not needed; we want
# a few diverse families incl. the cube and the non-distributive witnesses).
# --------------------------------------------------------------------------
def union_closed_families(n, limit=None):
    """Yield union-closed families F (as frozensets of frozensets) over [n] that
    contain the empty set and have |F|>=2.  Small n only (n<=4)."""
    ground = list(range(n))
    all_subsets = [frozenset(s) for k in range(n + 1)
                   for s in itertools.combinations(ground, k)]
    # too many to enumerate all closed families for n=4 by brute subsets; instead
    # generate by closing random/structured seed collections.  For determinism we
    # enumerate all families that are CLOSURES of small generating sets.
    seen = set()
    out = []
    # generators: all collections of up to 3 nonempty subsets, closed under union
    nonempty = [s for s in all_subsets if s]
    import random
    random.seed(0)
    seeds = []
    # structured seeds: singletons, pairs, plus a few random
    for r in range(1, min(4, len(nonempty)) + 1):
        for combo in itertools.combinations(nonempty, r):
            seeds.append(combo)
            if len(seeds) > 4000:
                break
        if len(seeds) > 4000:
            break
    for gen in seeds:
        F = set(gen)
        F.add(frozenset())
        changed = True
        while changed:
            changed = False
            for a in list(F):
                for b in list(F):
                    u = a | b
                    if u not in F:
                        F.add(u); changed = True
        key = frozenset(F)
        if key in seen or len(F) < 2:
            continue
        seen.add(key)
        out.append(sorted(F, key=lambda s: (len(s), sorted(s))))
        if limit and len(out) >= limit:
            break
    return out


# --------------------------------------------------------------------------
# Aut(L) on the ground set: permutations of [n] that preserve membership in F.
# (A lattice automorphism of L=(F,union) restricts to a permutation of the ground
#  elements; conversely a ground permutation preserving F induces a lattice auto.)
# --------------------------------------------------------------------------
def ground_set(F):
    return sorted(set().union(*[set(s) for s in F]))


def automorphisms(F):
    g = ground_set(F)
    Fset = set(F)
    autos = []
    for perm in itertools.permutations(g):
        sigma = dict(zip(g, perm))
        ok = True
        for A in F:
            B = frozenset(sigma[x] for x in A)
            if B not in Fset:
                ok = False; break
        if ok:
            autos.append([perm[g.index(x)] for x in g])  # image list aligned to g
    return g, autos


# --------------------------------------------------------------------------
# Frequency vector and JI-overlap (second-order fibre) matrix.
# --------------------------------------------------------------------------
def fibre_data(F):
    g = ground_set(F)
    L = len(F)
    # Fib(x) as a bitmask over members
    members = list(F)
    fib = {x: set(i for i, A in enumerate(members) if x in A) for x in g}
    v = np.array([len(fib[x]) / L for x in g])      # frequency densities
    M = np.zeros((len(g), len(g)))
    for i, x in enumerate(g):
        for j, y in enumerate(g):
            M[i, j] = len(fib[x] & fib[y]) / L
    return g, v, M


# --------------------------------------------------------------------------
# Isotypic decomposition of the permutation rep of G=Aut(L) on C^[g].
# We use Reynolds projectors onto isotypes via the GROUP-ALGEBRA central
# idempotents only implicitly: practically we compute the COMMUTANT-based block
# structure.  Cleanly: P_triv = (1/|G|) sum_g rho(g) projects onto G-invariants
# (the trivial isotype, dimension = #orbits).  The nontrivial isotypes are the
# orthogonal complement of fix(G).  We further split the complement by the
# canonical decomposition using the projection  e_rho = (dim_rho/|G|) sum_g
# conj(chi_rho(g)) rho(g) -- but characters need the abstract group.  For the
# DIAGNOSTIC we only need: (i) trivial part, (ii) its complement, and (iii) the
# spectrum of M restricted to each.  M is G-equivariant (commutes with rho),
# so it preserves both, and the nontrivial-isotype spectrum is the non-symmetric
# signal.
# --------------------------------------------------------------------------
def perm_matrices(g, autos):
    idx = {x: i for i, x in enumerate(g)}
    mats = []
    for img in autos:
        P = np.zeros((len(g), len(g)))
        for i, x in enumerate(g):
            P[idx[img[i]], i] = 1.0
        mats.append(P)
    return mats


def isotypic_split(g, autos, M, v):
    mats = perm_matrices(g, autos)
    G = len(mats)
    n = len(g)
    Reyn = sum(mats) / G                       # projector onto G-invariants (trivial isotype)
    # eigen-decompose Reyn: eigenvalue 1 -> trivial isotype, 0 -> complement
    w, Q = np.linalg.eigh(Reyn)
    triv_cols = Q[:, np.abs(w - 1) < 1e-8]     # basis of fix(G)
    comp_cols = Q[:, np.abs(w) < 1e-8]         # basis of complement (nontrivial isotypes)
    # verify M commutes with G (equivariance)
    equiv_defect = max((np.linalg.norm(P @ M - M @ P) for P in mats), default=0.0)
    # spectrum of M on trivial isotype and on complement
    def spec(B):
        if B.shape[1] == 0:
            return []
        blk = B.T @ M @ B
        return sorted(np.linalg.eigvalsh((blk + blk.T) / 2).tolist())
    triv_spec = spec(triv_cols)
    comp_spec = spec(comp_cols)
    # the frequency vector v: its component in the nontrivial isotype
    v_triv = triv_cols @ (triv_cols.T @ v) if triv_cols.shape[1] else np.zeros(n)
    v_comp = v - v_triv
    return {
        "n": n,
        "|Aut|": G,
        "num_orbits_dim_trivial": int(triv_cols.shape[1]),
        "dim_nontrivial": int(comp_cols.shape[1]),
        "M_equivariance_defect": float(equiv_defect),
        "M_trivial_isotype_spectrum": [round(x, 6) for x in triv_spec],
        "M_nontrivial_isotype_spectrum": [round(x, 6) for x in comp_spec],
        "freq_nontrivial_norm": float(np.linalg.norm(v_comp)),
        "freq_mean": float(v.mean()),
        "abundance": float(v.max()),
    }


# --------------------------------------------------------------------------
def classify(F):
    n = len(ground_set(F))
    L = len(F)
    g, autos = automorphisms(F)
    g2, v, M = fibre_data(F)
    info = isotypic_split(g, autos, M, v)
    # is it (iso to) the Boolean cube 2^[k]?
    is_cube = (L == 2 ** n) and all(frozenset(s) in set(F)
                                    for k in range(n + 1)
                                    for s in itertools.combinations(range(n), k))
    info["is_boolean_cube"] = bool(is_cube)
    info["|L|"] = L
    return info


def main():
    n_max = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    results = []
    for n in range(1, n_max + 1):
        fams = union_closed_families(n, limit=400)
        for F in fams:
            try:
                info = classify(F)
            except Exception as e:
                continue
            info["family_size"] = len(F)
            results.append(info)
    # summary: among families with abundance EXACTLY 1/2, who is the cube?
    half = [r for r in results if abs(r["abundance"] - 0.5) < 1e-9]
    cubes = [r for r in results if r["is_boolean_cube"]]
    # the headline diagnostic: nontrivial-isotype spectral spread vs abundance==1/2
    def nontriv_signal(r):
        s = r["M_nontrivial_isotype_spectrum"]
        return (max(s) - min(s)) if s else 0.0
    print("=== Aut(L)-isotypic decomposition of fibre-overlap M ===")
    print(f"families analyzed: {len(results)}")
    print(f"abundance == 1/2 exactly: {len(half)}  | boolean cubes among them: "
          f"{sum(r['is_boolean_cube'] for r in half)}")
    print()
    print("Boolean cubes (the symmetric-moment extremizers):")
    for r in cubes:
        print(f"  n={r['n']} |L|={r['|L|']:3d} |Aut|={r['|Aut|']:4d} "
              f"abund={r['abundance']:.3f} "
              f"dim_nontriv={r['dim_nontrivial']} "
              f"M_nontriv_spec={r['M_nontrivial_isotype_spectrum']} "
              f"freq_nontriv_norm={r['freq_nontrivial_norm']:.2e}")
    print()
    print("A few NON-cube families (abundance > 1/2 generally) for contrast:")
    noncube = [r for r in results if not r["is_boolean_cube"] and r["n"] >= 2]
    # show those with the largest nontrivial-isotype signal
    noncube.sort(key=nontriv_signal, reverse=True)
    for r in noncube[:8]:
        print(f"  n={r['n']} |L|={r['|L|']:3d} |Aut|={r['|Aut|']:4d} "
              f"abund={r['abundance']:.3f} "
              f"M_nontriv_spec={r['M_nontrivial_isotype_spectrum']} "
              f"signal={nontriv_signal(r):.3f}")
    with open(os.path.join(DATA, "frankl_isotypic.json"), "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {os.path.join(DATA, 'frankl_isotypic.json')}")


if __name__ == "__main__":
    main()
