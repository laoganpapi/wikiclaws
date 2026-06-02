"""
lattice_parametric.py — Parametric lattice families, to (a) probe candidate
structural bounds beyond the n≤5 enumeration, and (b) confirm that the apparent
"floors above 1/2" seen for large width / many join-irreducibles at n≤5 are
small-n ARTIFACTS, not structural bounds.

Generators (all return UC families as frozenset of bitmasks, with ∅ ∈ F):
  * chain(h)              : the (h+1)-element chain 0 ⊂ {0} ⊂ {0,1} ⊂ … . abundance→?
  * boolean(k)            : 2^[k]. abundance = 1/2 exactly.
  * product(Gs)           : disjoint-support product of UC families. abundance =
                            max abundance of factors; invariants multiply/add.
  * cube_minus_top(k)     : 2^[k] \ {top}? (not UC in general) — skip.
  * powerset_chain(k, h)  : product of a Boolean B_k and a chain C_h — distributive,
                            tunable width (from B_k) and height (k+h), abundance 1/2.
  * antichain_cone(t)     : t incomparable atoms with a common top {0..t-1}; ∅.
                            ( = the height-2 lattice M_t ), abundance (t)/(t+1)? check.

The headline check: a DISTRIBUTIVE lattice (product of a wide Boolean and a tall
chain) has abundance EXACTLY 1/2 while its width and #join-irreducibles and height
are all large — directly contradicting any "width ≥ 4 ⇒ abundance > 1/2" or
"#JI large ⇒ abundance > 1/2" reading of the n≤5 data.
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from uc_family import (abundance, frequencies, ground_set, is_union_closed,  # noqa: E402
                       family_to_sets)
import lattice as Lat  # noqa: E402


def chain(h):
    """(h+1)-element chain: ∅ ⊂ {0} ⊂ {0,1} ⊂ … ⊂ {0,…,h-1}."""
    out = {0}
    m = 0
    for i in range(h):
        m |= 1 << i
        out.add(m)
    return frozenset(out)


def boolean(k):
    return frozenset(range(1 << k))


def shift(F, by):
    return frozenset((m << by) for m in F)


def product(Gs):
    """Disjoint-support product: place each factor on its own block of bits, the
    family is all unions of one member from each factor (= elementwise OR)."""
    families = []
    offset = 0
    for G in Gs:
        width = max((m.bit_length() for m in G), default=0)
        families.append(shift(G, offset))
        offset += width
    # all combinations of OR
    result = {0}
    for fam in families:
        result = {a | b for a in result for b in fam}
    return frozenset(result)


def powerset_chain(k, h):
    """Distributive lattice B_k × C_h (product). Width ≈ from B_k, height = k+h."""
    return product([boolean(k), chain(h)])


def antichain_top(t):
    """M_t-like: ∅, t singletons {0},…,{t-1}? NOT UC (need pairwise unions).
    Instead: ∅, t incomparable middles each = [t]\{i}? Their pairwise unions = [t].
    Realize the height-2 lattice with t coatoms and top [t]."""
    full = (1 << t) - 1
    out = {0, full}
    for i in range(t):
        out.add(full ^ (1 << i))  # [t] minus element i  (t coatoms)
    return frozenset(out)


def report(name, F):
    assert is_union_closed(F), f"{name} not UC"
    inv = Lat.invariants(F)
    print(f"  {name:24s}: |L|={inv.n_L:4d} h={inv.height} w={inv.width} "
          f"#JI={inv.n_join_irred} #MI={inv.n_meet_irred} "
          f"distrib={int(inv.distributive)} mod={int(inv.modular)} "
          f"lsm={int(inv.lower_semimodular)} usm={int(inv.upper_semimodular)} "
          f"abundance={abundance(F):.4f}")
    return inv


if __name__ == "__main__":
    print("=" * 78)
    print("Parametric lattice classes vs abundance")
    print("=" * 78)

    print("\nChains C_h  (distributive, width 1):")
    for h in [1, 2, 3, 5, 8]:
        report(f"chain C_{h}", chain(h))

    print("\nBoolean B_k  (distributive):")
    for k in [1, 2, 3, 4, 5]:
        report(f"boolean B_{k}", boolean(k))

    print("\nDISTRIBUTIVE B_k × C_h  (large width AND height, abundance = 1/2):")
    for (k, h) in [(2, 3), (3, 2), (2, 5), (3, 3), (4, 1)]:
        report(f"B_{k} x C_{h}", powerset_chain(k, h))

    print("\nHeight-2 lattices M_t (t coatoms, top, bottom):")
    for t in [3, 4, 5, 6]:
        report(f"M_{t}", antichain_top(t))

    print()
    print("=" * 78)
    print("KEY: a distributive lattice with width≥4 and #JI large at abundance 1/2")
    print("  (refutes any 'width≥4 ⇒ abundance>1/2' or '#JI large ⇒ >1/2' reading)")
    print("=" * 78)
    F = powerset_chain(3, 3)  # B_3 × C_3
    inv = Lat.invariants(F)
    print(f"  B_3 × C_3: width={inv.width}, #JI={inv.n_join_irred}, "
          f"height={inv.height}, abundance={abundance(F):.4f}  "
          f"[distributive={inv.distributive}]")
    F2 = powerset_chain(4, 0)
    inv2 = Lat.invariants(boolean(4))
    print(f"  B_4: width={inv2.width}, #JI={inv2.n_join_irred}, "
          f"abundance={abundance(boolean(4)):.4f}")
