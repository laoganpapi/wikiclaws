"""
lattice_cone.py — The explicit "universal-element cone" construction behind the
obstruction, with an exact proof-by-construction and validation.

CONSTRUCTION (cone over a fresh universal coordinate z).
Let G ⊆ 2^[n] be ANY union-closed family with ∅ ∈ G (so G = its own lattice L_G).
Pick a fresh ground element z = n. Define

    cone_k(G) := {∅} ∪ { A ∪ {z} : A ∈ G, A ≠ ∅ }          (single new coordinate)

i.e. keep the bottom ∅, and adjoin z to every NON-empty member of G.

CLAIMS (all proved below in code by exhaustive check on small G, and argued in the
writeup):
  (C1) cone(G) is union-closed.
  (C2) cone(G) is LATTICE-ISOMORPHIC to G (the map ∅↦∅, A↦A∪{z} is an order-iso
       preserving joins). Hence ALL lattice invariants of cone(G) equal those of G.
  (C3) abundance(cone(G)) = (|G| − 1)/|G| = 1 − 1/|L_G|, attained by z, since z is
       in every member except ∅.

So: starting from a realization G of L at abundance φ, cone(G) is another
realization of the SAME abstract lattice L at abundance 1 − 1/|L| (which → 1).
Therefore the abundance of a UC family is NOT a function of its lattice; the only
lattice-invariant lower bound on abundance is the trivial one implied by Poonen
(min over JIs of |↑j| ≤ |L|/2 ⇒ abundance ≥ 1/2), and NO coarse invariant
(height, width, #JI, modularity defect) can improve on 1/2 — because cone fixes
all of them while sending abundance to 1.

We also build the symmetric LOW witness: any lattice L that arises as 2^[k] (a
Boolean lattice) has a realization at EXACTLY abundance 1/2 (the standard cube),
and cone of it at 1 − 1/2^k. Both realize B_k. This is the minimal clean pair.
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from uc_family import (abundance, frequencies, ground_set, is_union_closed,  # noqa: E402
                       family_to_sets, mask_to_set)
from enumerate import all_uc_families  # noqa: E402
import lattice as Lat  # noqa: E402


def cone(G_masks, z=None):
    """cone over a fresh universal coordinate z (default = next free bit)."""
    G = set(G_masks)
    G.add(0)  # ensure bottom present
    if z is None:
        n = max((m.bit_length() for m in G), default=0)
        z = n  # fresh bit above all used
    zbit = 1 << z
    out = {0}
    for A in G:
        if A == 0:
            continue
        out.add(A | zbit)
    return frozenset(out)


def lattice_iso_to_original(G_masks):
    """Check cone(G) ≅ G as lattices via the cover-digraph isomorphism."""
    from lattice_minab import exact_lattice_iso
    G = frozenset(set(G_masks) | {0})
    Gc = cone(G)
    return exact_lattice_iso(G, Gc)


def check_construction(n_max=4):
    """Exhaustively verify (C1),(C2),(C3) over all UC families G (∅∈G) at n≤n_max."""
    from lattice_minab import exact_lattice_iso
    total = 0
    bad = []
    for n in range(n_max + 1):
        for G in all_uc_families(n):
            if 0 not in G:        # require ∅ ∈ G
                continue
            if len(G) < 2:
                continue
            total += 1
            Gc = cone(G)
            # (C1) union-closed
            c1 = is_union_closed(Gc)
            # (C2) lattice iso to G
            c2 = exact_lattice_iso(G, Gc)
            # (C3) abundance == 1 - 1/|G|
            c3 = abs(abundance(Gc) - (1 - 1.0 / len(G))) < 1e-12
            if not (c1 and c2 and c3):
                bad.append((n, sorted(sorted(s) for s in family_to_sets(G)),
                            c1, c2, c3, abundance(Gc), 1 - 1.0 / len(G)))
    return total, bad


def boolean_pair(k):
    """The minimal clean witness pair realizing the Boolean lattice B_k:
       LOW  = 2^[k] (abundance 1/2),  HIGH = cone(2^[k]) (abundance 1 - 1/2^k)."""
    full = (1 << k) - 1
    low = frozenset(range(1 << k))          # all subsets of [k] = 2^[k]
    high = cone(low, z=k)
    return low, high


if __name__ == "__main__":
    print("=" * 78)
    print("Exhaustive verification of the cone construction (C1)–(C3), n≤4")
    print("=" * 78)
    total, bad = check_construction(4)
    print(f"  UC families G (∅∈G, |G|≥2) tested: {total}")
    print(f"  failures of (C1 UC ∧ C2 lattice-iso ∧ C3 abundance=1−1/|L|): {len(bad)}")
    if bad:
        for b in bad[:10]:
            print("   FAIL:", b)
    else:
        print("  ALL PASS — cone(G) is union-closed, lattice-isomorphic to G, "
              "and has abundance 1 − 1/|L|.")

    print()
    print("=" * 78)
    print("Minimal clean witness pairs: Boolean lattice B_k at abundance 1/2 vs")
    print("its cone at 1 − 1/2^k (SAME abstract lattice, SAME invariants)")
    print("=" * 78)
    from lattice_minab import exact_lattice_iso
    for k in range(1, 5):
        low, high = boolean_pair(k)
        il = Lat.invariants(low)
        ih = Lat.invariants(high)
        iso = exact_lattice_iso(low, high)
        same_inv = (il == ih)
        print(f"  k={k}: |L|={il.n_L}  lattice-iso={iso}  identical-invariants={same_inv}")
        print(f"        LOW  2^[{k}]      abundance={abundance(low):.4f}")
        print(f"        HIGH cone(2^[{k}]) abundance={abundance(high):.4f}  "
              f"(=1−1/{il.n_L})")
        # show the invariants are literally equal
        if not same_inv:
            print("        !! invariants differ:", il, ih)
