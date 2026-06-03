"""
poset_topology_probe.py — sanity probe for the poset-topology direction on Frankl.

Computes, for every UC family F (n<=N), on the lattice L = (F, subseteq, cup)
adjoined with bottom:

  * Moebius function mu_L(0_hat, 1_hat) of the whole lattice  (= reduced Euler
    char of the order complex of the OPEN interval (0_hat,1_hat) =
    Delta(proper part of L), by Philip Hall's theorem).
  * The crosscut complex Cr(JI) on the set of join-irreducibles: a face is a
    subset S of JI whose join is NOT the top T (equivalently S has an upper bound
    < 1_hat). [crosscut theorem: the order complex of the proper part of L is
    homotopy equivalent to this crosscut complex when JI is a crosscut.]
    We compute its reduced Euler characteristic chi~(Cr).
  * Correlate these topological invariants with abundance(F).

This is a SANITY / EXPLORATION probe for math/ideas/generation/poset_topology.md.
No proof is claimed. [NOVELTY UNVERIFIED]
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


def mobius_lattice(elements):
    """Full Moebius matrix; return mu(bottom, top) and dict mu(0_hat, x)."""
    elements = sorted(elements)
    bottom = elements[0]
    # mu(x,x)=1 ; mu(x,y) = -sum_{x<=z<y} mu(x,z)  for x<y ; 0 if x not<=y.
    # We only need mu(bottom, y) for all y.
    mu = {}
    for y in elements:
        if y == bottom:
            mu[y] = 1
            continue
        if not leq(bottom, y):
            mu[y] = 0
            continue
        s = 0
        for z in elements:
            if z == y:
                continue
            if leq(bottom, z) and leq(z, y):
                s += mu[z]
        mu[y] = -s
    return mu


def crosscut_euler_on_JI(elements, top, JI):
    """
    Reduced Euler characteristic of the crosscut complex Cr on the join-
    irreducibles JI: faces = subsets S of JI with join(S) != top (i.e. S has a
    common upper bound strictly below top -> bounded above by a proper element).
    By convention the empty set is a face (join = bottom != top when |L|>1).

    chi~(Cr) = sum_{faces S, S possibly empty} (-1)^{|S|-1}  ... reduced.
    Standard reduced Euler char of an (abstract) simplicial complex K:
        chi~(K) = -1 + sum_{nonempty faces F} (-1)^{|F|-1}
                = sum over faces incl. empty of (-1)^{|F|} * (-1)   ... we just
    compute chi~ = (number weighted) :  chi~ = sum_{i>=-1} (-1)^i f_i  with
    f_{-1}=1 (empty face).  i.e. chi~ = -f_{-1}+f_0-f_1+... reduced
    => chi~_reduced = sum_{nonempty F}(-1)^{|F|-1} - 1.
    We return reduced Euler characteristic.
    """
    JI = list(JI)
    r = len(JI)
    # face test: subset S is a face iff join(S) != top.
    # join of empty set = bottom.  As long as |L|>1, bottom != top, so empty is a face.
    # Build f-vector by sizes.
    f = defaultdict(int)  # f[k] = number of faces of cardinality k
    f[0] = 1  # empty face
    for k in range(1, r + 1):
        for S in combinations(JI, k):
            j = 0
            for x in S:
                j |= x
            if j != top:
                f[k] += 1
        if f[k] == 0:
            break
    # reduced Euler char = sum_{k>=0} (-1)^{k-1} f[k]   (with empty face k=0 giving -1)
    chi_red = 0
    for k, fk in f.items():
        chi_red += ((-1) ** (k - 1)) * fk
    fvec = {k: f[k] for k in sorted(f)}
    return chi_red, fvec


def is_crosscut(elements, bottom, top, JI):
    """A crosscut C of a lattice: an antichain that is maximal and such that
    every maximal chain meets it. The set of ATOMS is always a crosscut; the
    set of join-irreducibles is NOT generally an antichain. We just report
    whether JI is an antichain (a necessary condition to invoke the classical
    crosscut theorem on JI directly)."""
    for a, b in combinations(JI, 2):
        if leq(a, b) or leq(b, a):
            return False
    return True


def main(N=5):
    by_chi_abund = defaultdict(list)
    mu_vs_abund = defaultdict(list)
    n_fam = 0
    cube_rows = []
    # crosscut-on-atoms euler too (atoms always form a crosscut)
    for n in range(0, N + 1):
        for F in all_uc_families(n):
            if len(F) < 2:
                continue
            elements, bottom, top = L.as_lattice(F)
            if len(elements) < 2:
                continue
            m = len(elements)
            JI = L.join_irreducibles(elements)
            atoms = L.atoms(elements)
            ab = abundance(F)
            mu = mobius_lattice(elements)
            mu_top = mu[top]
            chi_ji, _ = crosscut_euler_on_JI(elements, top, JI)
            chi_at, _ = crosscut_euler_on_JI(elements, top, atoms)
            n_fam += 1
            mu_vs_abund[mu_top].append(ab)
            by_chi_abund[chi_ji].append(ab)
            # Detect Boolean cube: F == full powerset of its support of size k
            supp = top
            k = bin(supp).count("1")
            is_cube = (m == (1 << k)) and (len(F) in (1 << k, (1 << k) - 1))
            if is_cube:
                cube_rows.append((k, m, mu_top, chi_ji, chi_at, round(ab, 4)))
    print(f"# families processed (|F|>=2, n<= {N}): {n_fam}")
    print()
    print("## Moebius mu_L(0,1) value  ->  abundance distribution")
    print(f"{'mu':>6} {'#fam':>7} {'min_ab':>8} {'max_ab':>8} {'mean_ab':>8} {'#below_half':>11}")
    for muv in sorted(mu_vs_abund):
        a = mu_vs_abund[muv]
        below = sum(1 for x in a if x < 0.5 - 1e-12)
        print(f"{muv:>6} {len(a):>7} {min(a):>8.4f} {max(a):>8.4f} {sum(a)/len(a):>8.4f} {below:>11}")
    print()
    print("## crosscut-on-JI reduced Euler char chi~ -> abundance distribution")
    print(f"{'chi~':>6} {'#fam':>7} {'min_ab':>8} {'max_ab':>8} {'mean_ab':>8} {'#below_half':>11}")
    for c in sorted(by_chi_abund):
        a = by_chi_abund[c]
        below = sum(1 for x in a if x < 0.5 - 1e-12)
        print(f"{c:>6} {len(a):>7} {min(a):>8.4f} {max(a):>8.4f} {sum(a)/len(a):>8.4f} {below:>11}")
    print()
    print("## Boolean cube sanity rows (k, |L|, mu_L(0,1), chi~_JI, chi~_atoms, abund)")
    seen = set()
    for row in cube_rows:
        key = row[0]
        if key in seen:
            continue
        seen.add(key)
        print("   k=%d |L|=%2d  mu=%+d  chi~_JI=%+d  chi~_atoms=%+d  abund=%.4f"
              % row)
    print()
    # Correlation headline: does any topological value force abundance >= 1/2?
    print("## Headline: families with abundance EXACTLY 0.5 (the extremal cubes-and-friends)")
    half = [(muv, c) for muv in mu_vs_abund for c in [0]]  # placeholder
    # Recompute joint mu x abundance==0.5
    print("   (see correlation tables above; min abundance over all families is the Frankl bound)")


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    main(N)
