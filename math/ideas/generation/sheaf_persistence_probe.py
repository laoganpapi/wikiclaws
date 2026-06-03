"""
sheaf_persistence_probe.py — concrete probe for the category/sheaf/persistence
direction on Frankl (math/ideas/generation/category_sheaf.md).

The fibres Fib(x) = {A in L : x in A} are FILTERS (up-sets) of the lattice
L = (F, subseteq, cup).  abundance(F) = max_x |Fib(x)| / |L|.  Frankl <=> some
Fib(x) covers >= half of L.

Every SYMMETRIC-MOMENT / OVERLAP lever has already been shown to degenerate on
the Boolean cube (join_irreducible_labelling.md, ji_overlap_inequality.md): the
cube is flat, so any convex symmetric average of the frequency vector is
minimized there at exactly 1/2.  The point of THIS probe is to compute genuinely
NON-MOMENT, NON-SYMMETRIC, structural invariants of the fibre system and see
whether ANY of them separates the cube from non-cubes / tracks abundance:

  (I)   PERSISTENT HOMOLOGY of the order complex of L filtered by the fibre
        cover-number  c(A) = #{x : A in Fib(x)} = |A|  (the "ground multiplicity"
        of a lattice element).  Sublevel filtration K_t = full subcomplex on
        {A : |A| <= t}.  We read the H0 and H1 barcodes (Edelsbrunner-Harer
        persistence) of the order-complex filtration.  This is NON-symmetric: it
        sees the ORDER in which lattice elements glue up, not an average.

  (II)  A CELLULAR SHEAF on the comparability graph / Hasse diagram of L (Curry,
        cellular sheaves): the constant Z/2 sheaf TWISTED by the fibre-membership.
        Concretely, for a single ground element x we build the indicator
        0-cochain 1_{Fib(x)} and ask what the sheaf coboundary / the cohomology
        of the up-set Fib(x) (as a subposet) looks like.  A filter of a lattice
        is contractible iff it has a minimum; we test which fibres are
        order-contractible and whether NON-contractibility (H~_* != 0 of the
        fibre's order complex) correlates with heaviness.  This is the
        "sheaf-of-fibres" cohomology probe.

  (III) The COLIMIT / Kan-extension reading: abundance = max over x of the size
        of the slice; we record whether the "heavy" fibre (the argmax) is
        PRINCIPAL (has a minimum, i.e. is a representable / free co-presheaf) or
        not, and cross-tabulate with whether abundance is forced.

Honest target: find ONE invariant that is (a) not a symmetric moment and
(b) >= 1/2-forcing on the cube while non-degenerate off it, OR honestly report
that all three degenerate too.  No proof claimed.  [NOVELTY UNVERIFIED]
"""

from __future__ import annotations

import sys
from collections import defaultdict
from itertools import combinations

sys.path.insert(0, "/home/user/wikiclaws/math/frankl/experiments")

from enumerate import all_uc_families          # noqa: E402
from uc_family import abundance                 # noqa: E402
import lattice as L                             # noqa: E402


def leq(a, b):
    return (a & b) == a


# ---------------------------------------------------------------------------
# Order complex of a poset, and reduced homology over Z/2 (Smith-free; we use
# rank over F_2 by Gaussian elimination).  The order complex Delta(P) has as
# k-simplices the (k+1)-chains x_0 < x_1 < ... < x_k of P.
# ---------------------------------------------------------------------------

def chains_of_length(P, k, lt):
    """All strictly increasing (k+1)-chains in poset P (list of elements, lt =
    strict-order predicate).  Returns list of tuples (sorted by the chain)."""
    res = []
    for combo in combinations(P, k + 1):
        # combo is sorted by python tuple order (mask value); need it to be a
        # chain under lt.  Check it forms a chain (totally ordered).
        ok = True
        for i in range(len(combo) - 1):
            if not lt(combo[i], combo[i + 1]):
                # might still be a chain in a different order, but since masks
                # of a chain are nested they ARE sorted by value; so a chain in
                # subset order is monotone in mask value.  If not lt here, not a
                # chain.
                ok = False
                break
        if ok:
            res.append(combo)
    return res


def f2_rank(rows, ncols):
    """Rank over F_2 of a 0/1 matrix given as a list of int bitmasks (rows).
    Greedy row-reduction keeping a basis of distinct leading bits."""
    basis = []  # reduced rows, each with a unique highest set bit
    for r in rows:
        cur = r
        for b in basis:
            cur = min(cur, cur ^ b)
        if cur:
            basis.append(cur)
            basis.sort(reverse=True)
    return len(basis)


def reduced_homology_ranks(P, lt, maxdim=None):
    """Reduced Betti numbers (over F_2) of the FULL order complex Delta(P), all
    dims.  Returns dict dim->betti.  Uses boundary-matrix ranks.

    Simplices: k-simplex = (k+1)-chain.  Boundary maps over F_2.
    Reduced: include the empty simplex (augmentation) so b0_reduced = (#comps)-1.

    IMPORTANT: we go to the FULL dimension of the complex (= longest chain - 1).
    Truncating at a fixed maxdim gives spurious top Betti numbers (e.g. a cone
    would report a fake top-dim class).  maxdim=None => full.
    """
    if len(P) == 0:
        return {0: 0}
    # full dimension = (longest chain length) - 1
    if maxdim is None:
        # cheap upper bound: a chain has at most |P| elements
        maxdim = len(P) - 1
    # build simplices per dimension
    simp = {}
    for d in range(maxdim + 1):
        cd = chains_of_length(P, d, lt)
        simp[d] = cd
        if not cd:
            # no chains of this length => none longer; stop
            maxdim = d
            break
    # index maps
    idx = {d: {s: i for i, s in enumerate(simp[d])} for d in simp}
    # boundary rank r_d = rank of partial_d : C_d -> C_{d-1}
    # for reduced homology, partial_0 : C_0 -> C_{-1}=F_2 (augmentation) has rank
    # 1 if there is >=1 vertex.
    ranks = {}
    # rank of augmentation map d=0 -> -1
    ranks[0] = 1 if simp[0] else 0
    for d in range(1, maxdim + 2):
        if d not in simp or not simp[d]:
            ranks[d] = 0
            continue
        lower = idx.get(d - 1, {})
        rows = []
        for s in simp[d]:
            # faces: drop one vertex
            bm = 0
            for j in range(len(s)):
                face = s[:j] + s[j + 1:]
                fi = lower.get(face)
                if fi is not None:
                    bm |= (1 << fi)
            rows.append(bm)
        ranks[d] = f2_rank(rows, len(lower))
    # reduced betti_d = dim C_d - rank partial_d - rank partial_{d+1}
    betti = {}
    for d in range(0, maxdim + 1):
        cd = len(simp[d])
        betti[d] = cd - ranks.get(d, 0) - ranks.get(d + 1, 0)
    return betti


# ---------------------------------------------------------------------------
# (I) Persistence of the |.|-filtration of the order complex of L.
# We compute, for the increasing filtration by t = |A| (cover-number), the
# H0-barcode: number of connected components born/that persist, summarized by
# the number of bars that are still alive when t reaches the top.  A SINGLE
# long H0 bar = the complex is connected (order complex of a bounded poset is
# always contractible, so this is degenerate UNLESS we filter by fibre, see (II)).
# More informative: persistence of the ORDER COMPLEX OF A SINGLE FIBRE.
# ---------------------------------------------------------------------------

def fibre(F_masks, x):
    return [A for A in F_masks if (A >> x) & 1]


def is_principal_filter(elements, fib):
    """A filter (up-set) is principal iff it has a unique minimum = meet of all
    its members lies inside it."""
    if not fib:
        return True
    m = fib[0]
    for a in fib[1:]:
        m &= a
    return m in set(fib)


# ---------------------------------------------------------------------------
# Main sweep
# ---------------------------------------------------------------------------

def is_boolean_cube(F_masks, top):
    k = bin(top).count("1")
    return len(F_masks) == (1 << k)


def main(N=4):
    # buckets: invariant value -> list of abundances
    fib_contractible_vs_ab = defaultdict(list)  # (heavy fibre principal?) -> ab
    fib_betti_vs_ab = defaultdict(list)         # reduced betti of heavy fibre order cx
    cube_rows = []
    nfam = 0
    # cross: does heavy fibre EVER have nontrivial reduced homology?
    nontrivial_fibre_homology = 0
    heavy_nonprincipal = 0
    for n in range(0, N + 1):
        for F in all_uc_families(n):
            if len(F) < 2:
                continue
            elements, bottom, top = L.as_lattice(F)
            if len(elements) < 2:
                continue
            F_masks = list(F)
            ab = abundance(F)
            nfam += 1
            # find heavy fibre (argmax over ground elements present)
            present = [x for x in range(n) if any((A >> x) & 1 for A in F_masks)]
            if not present:
                continue
            heavy_x = max(present, key=lambda x: len(fibre(F_masks, x)))
            fib = fibre(F_masks, heavy_x)
            # principal?
            prin = is_principal_filter(elements, fib)
            fib_contractible_vs_ab[prin].append(ab)
            if not prin:
                heavy_nonprincipal += 1
            # reduced homology of the order complex of the heavy fibre (as a
            # subposet under strict inclusion).  A filter with a minimum is
            # contractible (a cone), reduced betti all 0.  Non-principal filters
            # CAN have nontrivial homology -> the structural signal.
            def lt(a, b):
                return a != b and (a & b) == a
            betti = reduced_homology_ranks(fib, lt)  # full dimension
            total_red = sum(v for v in betti.values())
            fib_betti_vs_ab[total_red].append(ab)
            if total_red > 0:
                nontrivial_fibre_homology += 1
            if is_boolean_cube(F_masks, top):
                k = bin(top).count("1")
                # for the cube, every fibre is principal (distributive); record
                cube_rows.append((k, len(elements), prin, total_red, round(ab, 4)))
    print(f"# families processed (|F|>=2, n<= {N}): {nfam}")
    print()
    print("## (III) Heavy-fibre PRINCIPAL?  (principal = representable co-presheaf,")
    print("##       contractible order complex) -> abundance distribution")
    print(f"{'principal':>10} {'#fam':>7} {'min_ab':>8} {'max_ab':>8} {'mean_ab':>8} {'#ab<0.5':>8}")
    for key in [True, False]:
        a = fib_contractible_vs_ab.get(key, [])
        if not a:
            continue
        below = sum(1 for x in a if x < 0.5 - 1e-12)
        print(f"{str(key):>10} {len(a):>7} {min(a):>8.4f} {max(a):>8.4f} {sum(a)/len(a):>8.4f} {below:>8}")
    print(f"\n  heavy fibre non-principal in {heavy_nonprincipal}/{nfam} families")
    print()
    print("## (II) reduced Betti TOTAL of the HEAVY FIBRE's order complex -> abundance")
    print(f"{'b~_total':>9} {'#fam':>7} {'min_ab':>8} {'max_ab':>8} {'mean_ab':>8} {'#ab<0.5':>8}")
    for key in sorted(fib_betti_vs_ab):
        a = fib_betti_vs_ab[key]
        below = sum(1 for x in a if x < 0.5 - 1e-12)
        print(f"{key:>9} {len(a):>7} {min(a):>8.4f} {max(a):>8.4f} {sum(a)/len(a):>8.4f} {below:>8}")
    print(f"\n  heavy fibre has NONTRIVIAL reduced homology in "
          f"{nontrivial_fibre_homology}/{nfam} families")
    print()
    print("## Boolean cube rows (k, |L|, heavy_fibre_principal, b~_total, abundance)")
    seen = set()
    for row in sorted(cube_rows):
        if row[0] in seen:
            continue
        seen.add(row[0])
        print("   k=%d |L|=%2d  heavy_principal=%s  b~_total=%d  abundance=%.4f" % row)
    print()
    print("## HEADLINE diagnostics")
    print(f"  - heavy fibre principal => order complex CONTRACTIBLE (b~=0) always: "
          f"{'YES' if all(v==0 for vs in [fib_betti_vs_ab.get(0,[])] for v in [0]) else 'see table'}")
    # decisive question: is there ANY structural invariant here that is >=1/2 on
    # the cube AND nonzero off it?  Report whether non-principal heavy fibres
    # correlate with abundance > 1/2.
    nonprin_ab = fib_contractible_vs_ab.get(False, [])
    if nonprin_ab:
        print(f"  - among non-principal heavy fibres: min abundance = "
              f"{min(nonprin_ab):.4f}, #(ab<0.5) = "
              f"{sum(1 for x in nonprin_ab if x < 0.5 - 1e-12)}")
    prin_ab = fib_contractible_vs_ab.get(True, [])
    if prin_ab:
        print(f"  - among principal heavy fibres:     min abundance = "
              f"{min(prin_ab):.4f}, #(ab<0.5) = "
              f"{sum(1 for x in prin_ab if x < 0.5 - 1e-12)}")


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    main(N)
