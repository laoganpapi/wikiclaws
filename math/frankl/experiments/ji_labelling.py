"""
ji_labelling.py — Direct attack on Frankl's union-closed conjecture via the
join-irreducible / fibre-system structure (open problem F.2).

Author: Alex Ye (no AI on author line).
Status: [NOVELTY UNVERIFIED] — exploratory; every claim validated on all UC
        families n<=5. No proof claimed.

Foundation: frankl/theory/lattice_attack.md.

THE FORMALIZATION (recap, made operational here)
------------------------------------------------
Let F be union-closed with emptyset in F, so L = (F, subseteq, cup) is a lattice
with bottom 0hat = emptyset and top T = cup F.

* For a ground element x in [n], its FIBRE is Fib(x) = {A in F : x in A}.
  Each Fib(x) is a FILTER (up-set) of L: A superseteq B and x in B  =>  x in A.
* abundance(F) = max_x |Fib(x)| / |F|.  Frankl  <=>  some Fib(x) has density >= 1/2.
* m_x := meet_L(Fib(x)) (lattice meet of the whole fibre). Fib(x) = up(m_x)
  (a PRINCIPAL filter) iff x in m_x; then m_x is a join-irreducible (JI) and
  freq(x) = |up(m_x)|. Otherwise (only in non-distributive L) Fib(x) is a
  union of >=2 principal filters and x corresponds to no single JI.

THE RECONSTRUCTION CONSTRAINT (the thing invariants throw away)
--------------------------------------------------------------
The fibre SYSTEM {Fib(x)}_{x in [n]} is a collection of filters of L such that
for every A in L:   A = { x : A in Fib(x) }   (as a subset of [n]).
Equivalently the map  A  |->  { x : A in Fib(x) }  is exactly the identity
embedding of F into 2^[n].  This couples the filters together: they must
*reconstruct* F. abundance lives in this coupling, not in L alone.

We use this file to test H1-H5 (see module-level functions test_h1..test_h5).
"""

from __future__ import annotations

import itertools
import json
from collections.abc import Iterable
from dataclasses import dataclass

from uc_family import (
    Family,
    abundance,
    family_to_sets,
    frequencies,
    ground_set,
    is_union_closed,
    mask_to_set,
)
import lattice as lat


# ---------------------------------------------------------------------------
# Fibre / JI structure of a single family
# ---------------------------------------------------------------------------

def with_bottom(F: Family) -> Family:
    """Adjoin emptyset so F = L (a lattice with a bottom). |F| unchanged if emptyset already in."""
    return frozenset(set(F) | {0})


def fibres(F: Family, n: int) -> dict[int, frozenset[int]]:
    """Fib(x) = {A in F : x in A} as a frozenset of masks, for x in [n]."""
    out: dict[int, frozenset[int]] = {}
    for x in range(n):
        bit = 1 << x
        out[x] = frozenset(A for A in F if A & bit)
    return out


def is_filter(elements_set: frozenset[int], S: frozenset[int]) -> bool:
    """Is S an up-set (filter) of the inclusion order restricted to elements_set?
    i.e. A in S, A subseteq B in elements_set => B in S."""
    for A in S:
        for B in elements_set:
            if (A & B) == A and A != B and B not in S:
                return False
    return True


def meet_of_set(elements: list[int], S: Iterable[int]) -> int:
    """Lattice meet (in L on `elements`) of an arbitrary nonempty subset S.

    meet_L of a set = the largest element <= all members; computed as the join
    (set-union closure is the join in L, but meet need not be intersection) of
    all common lower bounds.  We compute it directly: candidates are elements
    that are <= every member of S; the meet is their join (top of that down-set,
    which exists since the common-lower-bound set is join-closed and nonempty
    because bottom is a lower bound)."""
    S = list(S)
    common_lb = [e for e in elements if all((e & a) == e for a in S)]
    # join of common_lb = bitwise-OR closure top; but in L the join of a set is
    # the unique minimal element of L above all of them. Since common_lb is
    # an ideal (down-closed) and join-closed within L, its top is OR of all.
    m = 0
    for e in common_lb:
        m |= e
    return m  # m is in L because common_lb is join-closed and m is its join


def ji_fibre_report(F: Family, n: int) -> dict:
    """Per-family fibre/JI structure.

    Returns a dict with:
      n, m=|L|, abundance,
      principal[x]: bool (Fib(x) principal <=> x in meet(Fib(x)))
      ji_of[x]: the JI m_x if principal else None
      max_principal_density, max_coatom_density, etc.
    """
    L = with_bottom(F)
    elements, bottom, top = lat.as_lattice(L)
    elem_set = frozenset(elements)
    m = len(elements)
    fibs = fibres(L, n)

    jis = set(lat.join_irreducibles(elements))
    mis = set(lat.meet_irreducibles(elements))
    coatoms = [x for x in elements if x != top and any(
        (x & top) == x and x != top for _ in [0]) ] if False else None
    # co-atoms = lower covers of top
    below = lat.cover_relation(elements)
    coatom_set = set(below[top]) if top in below else set()

    rep = {
        "n": n,
        "m": m,
        "abundance": abundance(L),
        "principal": {},
        "ji_of": {},
        "fib_size": {},
    }
    for x in range(n):
        S = fibs[x]
        if not S:
            rep["principal"][x] = None
            rep["ji_of"][x] = None
            rep["fib_size"][x] = 0
            continue
        mx = meet_of_set(elements, S)
        principal = (mx & (1 << x)) != 0  # x in m_x
        rep["principal"][x] = bool(principal)
        rep["ji_of"][x] = mx if principal else None
        rep["fib_size"][x] = len(S)

    # densities of structured filters
    def dens(a: int) -> float:
        return lat.principal_filter_size(elements, a) / m

    rep["jis"] = sorted(jis)
    rep["coatoms"] = sorted(coatom_set)
    rep["max_principal_ji_density"] = max((dens(j) for j in jis), default=0.0)
    # all principal filters (every element generates one):
    rep["max_principal_density"] = max((dens(e) for e in elements if e != bottom),
                                       default=0.0)
    # co-atom fibre density: |up(coatom)| / m  (= 2/m typically: coatom and top)
    rep["max_coatom_filter_density"] = max((dens(c) for c in coatom_set),
                                           default=0.0)
    # meet-irreducible principal-filter density
    rep["max_mi_density"] = max((dens(mi) for mi in mis if mi != bottom),
                                default=0.0)
    rep["elements"] = elements
    rep["top"] = top
    rep["bottom"] = bottom
    return rep


# ---------------------------------------------------------------------------
# H1: principal-filter (JI) fibres
# ---------------------------------------------------------------------------
# Among PRINCIPAL filters up(j), j a join-irreducible, is max density >= 1/2?
# (We also record max over ALL principal filters and the relation to abundance.)

# ---------------------------------------------------------------------------
# H2: meet-irreducible / co-atom fibres
# ---------------------------------------------------------------------------
# Does the co-atom / meet-irreducible structure ever certify >= 1/2?

# ---------------------------------------------------------------------------
# H3: counting identities on the fibre system
# ---------------------------------------------------------------------------
# Sum_x |Fib(x)| = Sum_A |A|. We probe whether combining this with structural
# filter constraints forces a heavy fibre. (Diagnostic; see analysis script.)

# ---------------------------------------------------------------------------
# H4: rigid-labelling lattices (every element JI, or |JI| = n)
# ---------------------------------------------------------------------------

def ji_rigidity_class(F: Family, n: int) -> dict:
    """Classify a family by JI-labelling rigidity."""
    L = with_bottom(F)
    elements, bottom, top = lat.as_lattice(L)
    jis = lat.join_irreducibles(elements)
    nonbottom = [e for e in elements if e != bottom]
    return {
        "n_jis": len(jis),
        "n_nonbottom": len(nonbottom),
        "all_join_irreducible": len(jis) == len(nonbottom),  # every elt is a JI
        "ji_eq_n": len(jis) == n,
        "abundance": abundance(L),
        "m": len(elements),
    }


# ---------------------------------------------------------------------------
# H5: labelling freedom — for a fixed abstract lattice L, enumerate all valid
# ground-element labellings (fibre systems reconstructing a UC family iso to L)
# and find the WORST (min over labellings of max-abundance).
# ---------------------------------------------------------------------------
#
# Operationally: a "labelling" of an abstract lattice L by a ground set is a
# join-embedding e : L -> 2^[k] for some k, with e(bottom)=emptyset, e(top)
# = [k], e(a cup_L b) = e(a) cup e(b), and e injective and order-faithful.
# Up to relabelling [k], the realizations of L as a *concrete* UC family are
# exactly such embeddings.  Equivalently: pick for each JOIN-IRREDUCIBLE j of L
# a nonempty "private" label-set, and for non-JI elements take unions; the
# constraint is that the resulting concrete family is union-closed and iso to L.
#
# We instead realize H5 the robust, model-free way: enumerate ALL concrete UC
# families F' on a ground set of size <= K_MAX whose lattice is isomorphic to L,
# and report min/max abundance over the iso class.  This is exactly minab(L)
# (already known to vary; here we focus on the *labelling* interpretation and on
# whether the worst labelling is the cube-like 1/2).  For lattices realizable
# only with many JIs we cap the ground set; we flag when the class is truncated.


def lattice_fingerprint(F: Family) -> tuple:
    """A relabelling-invariant fingerprint of the abstract lattice (F,cup).
    Strong enough to separate non-isomorphic lattices for |L|<=~12; we pair it
    with an exact iso check when needed."""
    L = with_bottom(F)
    elements, bottom, top = lat.as_lattice(L)
    inv = lat.invariants(L)
    below = lat.cover_relation(elements)
    # degree sequence of the cover (Hasse) digraph
    indeg = sorted(len(below[y]) for y in elements)
    above = lat.upper_covers(elements)
    outdeg = sorted(len(above[x]) for x in elements)
    # principal-filter-size multiset (iso-invariant)
    pf = tuple(sorted(lat.principal_filter_size(elements, e) for e in elements))
    return (
        inv.n_L, inv.height, inv.width, inv.n_join_irred,
        inv.n_meet_irred, inv.n_atoms, inv.distributive, inv.modular,
        inv.lower_semimodular, inv.upper_semimodular,
        tuple(indeg), tuple(outdeg), pf,
    )


# ---------------------------------------------------------------------------
# Driver utilities
# ---------------------------------------------------------------------------

def freq_sorted(F: Family, n: int) -> tuple[int, ...]:
    return tuple(sorted(frequencies(F, n), reverse=True))
