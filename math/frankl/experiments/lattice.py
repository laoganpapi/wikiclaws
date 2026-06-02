"""
lattice.py — Lattice-theoretic view of a union-closed family.

A union-closed family F ⊆ 2^[n] (bitmask encoding, see uc_family.py) is a
*join-semilattice* under set-inclusion ⊆ with join = ∪ (bitwise OR). To make it
a *lattice* L we adjoin a bottom 0̂ when ∅ ∉ F: a finite join-semilattice with a
minimum is automatically a lattice (the meet a ∧ b is the join of all common
lower bounds, which exists because the set of common lower bounds is nonempty —
it contains 0̂ — and join-closed).

This module computes, for a union-closed family F:
  * the lattice L (= F with a bottom adjoined if needed);
  * the cover relation (Hasse diagram);
  * join-irreducible elements (elements with exactly one lower cover);
  * meet-irreducible elements (elements with exactly one upper cover);
  * the principal filter ↑a = {x ∈ L : a ≤ x} and its size;
  * standard lattice invariants: height, width (max antichain), number of
    join-irreducibles, number of atoms, lower-/upper-semimodularity,
    modularity, distributivity;
  * the bridge to abundance (Poonen's formulation).

Convention. We treat the lattice L = (elements, ⊆). The "Poonen frequency" of a
join-irreducible j is |↑j| = #{x ∈ L : j ≤ x}. The Poonen lattice form of
Frankl's conjecture (Poonen 1992, [STATEMENT UNVERIFIED — primary source
inaccessible this session]) asserts: every finite lattice L with |L|>1 has a
join-irreducible j with |↑j| ≤ |L|/2.

WARNING on the F-vs-L size mismatch. Frankl's set form counts members of F (the
family). Poonen's lattice form counts members of L (= F plus possibly an adjoined
bottom). The two |·|/2 thresholds differ by the bottom. We track BOTH and the
exact dictionary between them is established empirically in
lattice_correspondence() and in the writeup. The safe, self-contained object we
use for the *abundance* question is always the family F and ground-set frequency;
the lattice invariants are computed on L and related to F.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import FrozenSet, Iterable

Family = FrozenSet[int]


# ---------------------------------------------------------------------------
# Building the lattice from a union-closed family
# ---------------------------------------------------------------------------

def as_lattice(F: Iterable[int]) -> tuple[list[int], int, int]:
    """
    Return (elements, bottom, top) for the lattice L of union-closed F.

    elements: sorted list of bitmasks of L (= F, with ∅ adjoined as 0̂ if F has
              no empty set). top = ∪ of all sets in F.
    bottom:   the minimum element (0 i.e. ∅).
    top:      the maximum element (bitwise OR of everything).

    Requires F union-closed (so that ∪ is the join and L is a lattice). We do
    NOT re-verify union-closure here for speed; callers pass UC families.
    """
    S = set(F)
    if not S:
        return [0], 0, 0
    top = 0
    for m in S:
        top |= m
    # Adjoin bottom 0̂ = ∅ if absent. (∅ is the identity for ∪, so adding it
    # keeps the family union-closed and makes it a lattice.)
    S.add(0)
    elements = sorted(S)
    return elements, 0, top


# ---------------------------------------------------------------------------
# Order relation and covers
# ---------------------------------------------------------------------------

def leq(a: int, b: int) -> bool:
    """a ≤ b in the inclusion order ⇔ a is a subset of b ⇔ a & b == a."""
    return (a & b) == a


def cover_relation(elements: list[int]) -> dict[int, list[int]]:
    """
    Return lower-cover lists: covers[y] = list of x with x ⋖ y (x covered by y),
    i.e. x < y and no z with x < z < y.

    O(|L|^3) worst case; fine for |L| ≤ few hundred. We restrict the inner
    search to elements between x and y in the inclusion order.
    """
    elem_set = elements
    below: dict[int, list[int]] = {y: [] for y in elem_set}
    for y in elem_set:
        # candidates strictly below y
        cands = [x for x in elem_set if x != y and leq(x, y)]
        for x in cands:
            # x is a lower cover of y iff no z strictly between
            is_cover = True
            for z in cands:
                if z == x:
                    continue
                if leq(x, z) and z != x and leq(z, y) and z != y:
                    # x < z < y ?  need x ≤ z, z ≤ y, x≠z, z≠y, and x<z
                    if x != z and (x & z) == x:  # x ⊆ z, x<z
                        is_cover = False
                        break
            if is_cover:
                below[y].append(x)
    return below


def upper_covers(elements: list[int]) -> dict[int, list[int]]:
    """above[x] = list of y with x ⋖ y (y is an upper cover of x)."""
    below = cover_relation(elements)
    above: dict[int, list[int]] = {x: [] for x in elements}
    for y, xs in below.items():
        for x in xs:
            above[x].append(y)
    return above


# ---------------------------------------------------------------------------
# Join- and meet-irreducibles
# ---------------------------------------------------------------------------

def join_irreducibles(elements: list[int]) -> list[int]:
    """
    Elements with exactly one lower cover (≠ bottom). In a finite lattice these
    are exactly the join-irreducibles: j is join-irreducible iff j is not the
    bottom and j ≠ a ∨ b for a,b < j, equivalently j has a unique lower cover.
    """
    below = cover_relation(elements)
    bottom = elements[0]  # sorted, ∅ is smallest
    return [y for y in elements if y != bottom and len(below[y]) == 1]


def meet_irreducibles(elements: list[int]) -> list[int]:
    """Elements with exactly one upper cover (≠ top)."""
    above = upper_covers(elements)
    top = elements[-1]
    return [x for x in elements if x != top and len(above[x]) == 1]


def atoms(elements: list[int]) -> list[int]:
    """Elements covering the bottom."""
    below = cover_relation(elements)
    bottom = elements[0]
    return [y for y in elements if below[y] == [bottom]]


# ---------------------------------------------------------------------------
# Principal filters and the Poonen frequency
# ---------------------------------------------------------------------------

def principal_filter_size(elements: list[int], a: int) -> int:
    """|↑a| = #{x ∈ L : a ≤ x}."""
    return sum(1 for x in elements if leq(a, x))


def poonen_min_filter(elements: list[int]) -> tuple[int, int]:
    """
    Return (j*, |↑j*|) minimising |↑j| over join-irreducibles j.

    Poonen's conjecture: min over join-irreducibles of |↑j| ≤ |L|/2.
    """
    jis = join_irreducibles(elements)
    if not jis:
        # Only the 2-element lattice {0̂, top}={∅,T}: the single join-irreducible
        # is top itself? Actually top has one lower cover (∅), so it's a JI.
        # If jis empty, L is trivial.
        return (-1, len(elements))
    best = min(jis, key=lambda j: principal_filter_size(elements, j))
    return best, principal_filter_size(elements, best)


# ---------------------------------------------------------------------------
# Lattice invariants
# ---------------------------------------------------------------------------

def height(elements: list[int]) -> int:
    """
    Length of the longest chain from bottom to top, counted in EDGES (so the
    2-element lattice has height 1). Equivalently the rank of the longest
    maximal chain.
    """
    below = cover_relation(elements)
    # longest path in the DAG of covers, from bottom upward
    # memoized longest chain ending at x (in edges)
    order = sorted(elements)  # ascending by mask; not a linear extension in
    # general, so compute via recursion with memo over "longest chain up to x"
    memo: dict[int, int] = {}

    def longest_down(x: int) -> int:
        if x in memo:
            return memo[x]
        if not below[x]:
            memo[x] = 0
            return 0
        v = 1 + max(longest_down(z) for z in below[x])
        memo[x] = v
        return v

    return max(longest_down(x) for x in elements)


def longest_chain(elements: list[int]) -> list[int]:
    """A longest chain bottom = c_0 ⋖ c_1 ⋖ … ⋖ c_h = top (as a list of masks)."""
    below = cover_relation(elements)
    memo: dict[int, tuple[int, list[int]]] = {}

    def lc(x: int) -> tuple[int, list[int]]:
        if x in memo:
            return memo[x]
        if not below[x]:
            memo[x] = (0, [x])
            return memo[x]
        best = max((lc(z) for z in below[x]), key=lambda t: t[0])
        memo[x] = (best[0] + 1, best[1] + [x])
        return memo[x]

    top = elements[-1]
    return lc(top)[1]


def height_lower_bound_witness(F: Iterable[int]) -> tuple[int, int, int]:
    """
    Return (x, freq_x, height) certifying the structural inequality

        abundance(F) ≥ height(L) / |L|

    Proof (elementary, lattice-structural — NOT entropy):
      Take a longest chain ∅ = c_0 ⋖ c_1 ⋖ … ⋖ c_h = T in L (length h = height).
      Pick any ground element x ∈ c_1 (c_1 is an atom, nonempty). Since
      c_1 ⊆ c_2 ⊆ … ⊆ c_h, x ∈ c_i for every i ≥ 1, so x lies in at least h
      members of F. Hence max_x freq(x) ≥ h, i.e. abundance ≥ h/|L|.

    Whenever 2·height ≥ |L| (a "tall" lattice) this gives abundance ≥ 1/2,
    recovering Frankl for that class (chains, and more generally any lattice whose
    longest chain covers at least half the elements).

    [PRIOR-ART CHECK PENDING] This is elementary and almost surely folklore /
    subsumed by chain-condition results (e.g. Colbert 2024 for short chains, and
    Frankl-for-chains is classical). Recorded as an internal sanity certificate,
    NOT claimed novel.
    """
    S = frozenset(F)
    elements, _, _ = as_lattice(S)
    if len(elements) <= 1:
        return (-1, 0, 0)
    h = height(elements)
    chain = longest_chain(elements)
    if len(chain) < 2:
        return (-1, 0, 0)
    c1 = chain[1]                      # first atom on the chain (nonempty)
    x = (c1 & -c1).bit_length() - 1    # some element of c1
    bit = 1 << x
    freq_x = sum(1 for A in S if A & bit)
    return (x, freq_x, h)


def width(elements: list[int]) -> int:
    """
    Width = size of the largest antichain. Computed exactly via Dilworth /
    bipartite matching (minimum chain cover = max antichain). For |L| up to a
    few hundred this is fine.
    """
    n = len(elements)
    idx = {e: i for i, e in enumerate(elements)}
    # Strict order edges u < v
    # Build adjacency for bipartite matching on the "strict-less-than" relation.
    less: list[list[int]] = [[] for _ in range(n)]
    for i, u in enumerate(elements):
        for j, v in enumerate(elements):
            if u != v and leq(u, v):
                less[i].append(j)
    # Max matching in bipartite graph (left=elements, right=elements) where
    # i~j iff elements[i] < elements[j]. Min chain cover = n - max_matching,
    # and by Dilworth width = min chain cover.
    match_right = [-1] * n

    def try_augment(u: int, seen: list[bool]) -> bool:
        for v in less[u]:
            if not seen[v]:
                seen[v] = True
                if match_right[v] == -1 or try_augment(match_right[v], seen):
                    match_right[v] = u
                    return True
        return False

    matching = 0
    for u in range(n):
        seen = [False] * n
        if try_augment(u, seen):
            matching += 1
    return n - matching


def is_distributive(elements: list[int]) -> bool:
    """
    Test the distributive law a ∧ (b ∨ c) = (a∧b) ∨ (a∧c) for all triples.

    Join = ∪ (bitwise OR). Meet must be computed in L (the join of common lower
    bounds), which for a sublattice of 2^[n] that happens to be closed under ∩
    equals ∩, but in general is NOT ∩. We compute meet via meet_in_L.
    """
    meet = _meet_table(elements)
    join = _join_table(elements)
    es = elements
    for a in es:
        for b in es:
            for c in es:
                lhs = meet[(a, join[(b, c)])]
                rhs = join[(meet[(a, b)], meet[(a, c)])]
                if lhs != rhs:
                    return False
    return True


def is_modular(elements: list[int]) -> bool:
    """
    Test the modular law: a ≤ c ⇒ a ∨ (b ∧ c) = (a ∨ b) ∧ c, for all b.
    """
    meet = _meet_table(elements)
    join = _join_table(elements)
    es = elements
    for a in es:
        for c in es:
            if not leq(a, c):
                continue
            for b in es:
                lhs = join[(a, meet[(b, c)])]
                rhs = meet[(join[(a, b)], c)]
                if lhs != rhs:
                    return False
    return True


def is_lower_semimodular(elements: list[int]) -> bool:
    """
    Lower semimodular: a ∧ b ⋖ a and a ∧ b ⋖ b together would require ... use
    the covering characterization: L is lower semimodular iff for all a,b:
    (a ⋖ a∨b and b ⋖ a∨b) ⇒ (a∧b ⋖ a and a∧b ⋖ b). We test the dual
    covering condition: if a∨b covers a and covers b then a covers a∧b and b
    covers a∧b. Equivalent standard form: a∧b ⋖ a  ⟹  b ⋖ a∨b.
    """
    meet = _meet_table(elements)
    join = _join_table(elements)
    covers = _is_cover_pred(elements)
    es = elements
    for a in es:
        for b in es:
            m = meet[(a, b)]
            if covers(m, a):  # a∧b ⋖ a
                if not covers(b, join[(a, b)]):  # need b ⋖ a∨b
                    return False
    return True


def is_upper_semimodular(elements: list[int]) -> bool:
    """Upper semimodular: a∧b ⋖ a ⟸ b ⋖ a∨b ... standard: b ⋖ a∨b ⟹ a∧b ⋖ a.

    We test: if a ⋖ a∨b then a∧b ⋖ b (the symmetric upper form
    a ⋖ a∨b ⟹ a∧b ⋖ b)."""
    meet = _meet_table(elements)
    join = _join_table(elements)
    covers = _is_cover_pred(elements)
    es = elements
    for a in es:
        for b in es:
            j = join[(a, b)]
            if covers(a, j):  # a ⋖ a∨b
                if not covers(meet[(a, b)], b):  # need a∧b ⋖ b
                    return False
    return True


# ---------------------------------------------------------------------------
# Meet / join tables (cached per call)
# ---------------------------------------------------------------------------

def meet_in_L(elements: list[int], a: int, b: int) -> int:
    """
    Meet a ∧ b in L = join of all common lower bounds. Since join = ∪ (OR),
    a∧b = OR of all x ∈ L with x ⊆ a and x ⊆ b. (This is the largest element
    of L below both — exists & unique because L is join-closed and contains 0̂.)
    """
    common = 0
    for x in elements:
        if (x & a) == x and (x & b) == x:  # x ⊆ a and x ⊆ b
            common |= x
    # common is the OR of common lower bounds; it is itself in L (L is
    # join-closed) and is ⊆ a, ⊆ b, hence the meet.
    return common


def _meet_table(elements: list[int]) -> dict[tuple[int, int], int]:
    es = elements
    # Precompute, for each element, its "downset OR" trick is not directly
    # usable per-pair; do the straightforward O(|L|^2 · |L|) build but cache.
    table: dict[tuple[int, int], int] = {}
    for a in es:
        for b in es:
            common = 0
            for x in es:
                if (x & a) == x and (x & b) == x:
                    common |= x
            table[(a, b)] = common
    return table


def _join_table(elements: list[int]) -> dict[tuple[int, int], int]:
    # join = OR. For a union-closed family (with ∅ adjoined) the OR of two
    # members is always a member, so a|b ∈ elements. We guard anyway: if a|b
    # is not literally in the element set the family was not union-closed, which
    # is a caller error — surface it loudly.
    elem_set = set(elements)
    table: dict[tuple[int, int], int] = {}
    for a in elements:
        for b in elements:
            j = a | b
            if j not in elem_set:
                raise ValueError(
                    f"join {a:b} ∨ {b:b} = {j:b} ∉ L; family is not union-closed"
                )
            table[(a, b)] = j
    return table


def _is_cover_pred(elements: list[int]):
    below = cover_relation(elements)
    cover_set = set()
    for y, xs in below.items():
        for x in xs:
            cover_set.add((x, y))

    def covers(x: int, y: int) -> bool:
        """True iff x ⋖ y (x covered by y)."""
        return (x, y) in cover_set

    return covers


# ---------------------------------------------------------------------------
# Aggregate invariant record
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LatticeInvariants:
    n_L: int            # |L|  (family + adjoined bottom)
    n_F: int            # |F|  (the union-closed family itself, incl. ∅ if present)
    height: int
    width: int
    n_join_irred: int
    n_meet_irred: int
    n_atoms: int
    poonen_min_filter: int   # min over JIs of |↑j|
    distributive: bool
    modular: bool
    lower_semimodular: bool
    upper_semimodular: bool


def invariants(F: Iterable[int]) -> LatticeInvariants:
    """
    Compute the bundle of lattice invariants for union-closed F.

    Optimised: the cover relation and the meet table are each computed ONCE and
    shared across all the semimodularity / (dis)modularity tests, rather than
    rebuilt per-property. join = OR is free.
    """
    S = frozenset(F)
    elements, bottom, top = as_lattice(S)
    n_L = len(elements)
    n_F = len(S)
    if n_L <= 1:
        return LatticeInvariants(n_L, n_F, 0, 1, 0, 0, 0, n_L,
                                 True, True, True, True)

    below = cover_relation(elements)
    cover_set = {(x, y) for y, xs in below.items() for x in xs}

    def covers(x: int, y: int) -> bool:
        return (x, y) in cover_set

    # meet table (shared). O(|L|^3) once.
    meet = _meet_table(elements)
    # join is OR; validate union-closure once.
    elem_set = set(elements)

    bottom_e = elements[0]
    top_e = elements[-1]
    # join-irreducibles / meet-irreducibles / atoms from covers
    above: dict[int, list[int]] = {x: [] for x in elements}
    for (x, y) in cover_set:
        above[x].append(y)
    jis = [y for y in elements if y != bottom_e and len(below[y]) == 1]
    mis = [x for x in elements if x != top_e and len(above[x]) == 1]
    atms = [y for y in elements if below[y] == [bottom_e]]

    # Poonen min filter over JIs
    if jis:
        pmin = min(sum(1 for x in elements if leq(j, x)) for j in jis)
    else:
        pmin = n_L

    # union-closure guard (join = OR must land in L)
    for a in elements:
        for b in elements:
            if (a | b) not in elem_set:
                raise ValueError("family not union-closed")

    # distributivity: a ∧ (b ∨ c) = (a∧b) ∨ (a∧c) for all triples
    distributive = True
    for a in elements:
        for b in elements:
            for c in elements:
                lhs = meet[(a, b | c)]
                rhs = meet[(a, b)] | meet[(a, c)]
                if lhs != rhs:
                    distributive = False
                    break
            if not distributive:
                break
        if not distributive:
            break

    # modularity: a ≤ c ⇒ a ∨ (b∧c) = (a∨b) ∧ c
    modular = True
    for a in elements:
        for c in elements:
            if not leq(a, c):
                continue
            for b in elements:
                lhs = a | meet[(b, c)]
                rhs = meet[(a | b, c)]
                if lhs != rhs:
                    modular = False
                    break
            if not modular:
                break
        if not modular:
            break

    # lower semimodular: a∧b ⋖ a ⟹ b ⋖ a∨b
    lsm = True
    for a in elements:
        for b in elements:
            m = meet[(a, b)]
            if covers(m, a) and not covers(b, a | b):
                lsm = False
                break
        if not lsm:
            break
    # upper semimodular: a ⋖ a∨b ⟹ a∧b ⋖ b
    usm = True
    for a in elements:
        for b in elements:
            if covers(a, a | b) and not covers(meet[(a, b)], b):
                usm = False
                break
        if not usm:
            break

    return LatticeInvariants(
        n_L=n_L,
        n_F=n_F,
        height=height(elements),
        width=width(elements),
        n_join_irred=len(jis),
        n_meet_irred=len(mis),
        n_atoms=len(atms),
        poonen_min_filter=pmin,
        distributive=distributive,
        modular=modular,
        lower_semimodular=lsm,
        upper_semimodular=usm,
    )


__all__ = [
    "Family",
    "as_lattice",
    "leq",
    "cover_relation",
    "upper_covers",
    "join_irreducibles",
    "meet_irreducibles",
    "atoms",
    "principal_filter_size",
    "poonen_min_filter",
    "height",
    "longest_chain",
    "height_lower_bound_witness",
    "width",
    "is_distributive",
    "is_modular",
    "is_lower_semimodular",
    "is_upper_semimodular",
    "meet_in_L",
    "LatticeInvariants",
    "invariants",
]
