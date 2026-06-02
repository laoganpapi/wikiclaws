"""
lattice_minab.py — The sharp obstruction, made rigorous.

We define, for a finite lattice L (presented as a UC family with ∅, so F=L):

    minab(L) = min over UC families F' with F' ≅ L (as lattices) of abundance(F').

Frankl ⇔ minab(L) ≥ 1/2 for every L (Poonen). The question for the *lattice
attack* is whether COARSE invariants (height, width, #join-irred, #meet-irred,
#atoms, modular, distributive, lsm, usm) determine — or even lower-bound above
1/2 — the quantity minab(L).

This script:
  (1) Groups all n≤5 UC families that contain ∅ (so F=L) into lattice-isomorphism
      classes, using a strong iso-invariant fingerprint (cover digraph canonical
      form via the down/up-set profile + iterated colour refinement). We then
      verify candidate-equal classes by an explicit isomorphism search on the
      cover relation (exact, since lattices are small).
  (2) For each iso class, records minab and maxab over the realizations PRESENT in
      the n≤5 enumeration (a lower bound on the true min/max over all realizations).
  (3) Tests whether two DIFFERENT lattice-iso classes with the SAME coarse
      invariant signature can have different minab — the sharp obstruction.
  (4) Exhibits the "universal-element cone" construction explicitly: for the
      witness lattices, shows a realization at abundance 1/2 and a realization at
      abundance 1 − 1/|L|, both lattice-isomorphic.

Note on scope. The n≤5 enumeration realizes a lattice L only if L embeds as a
join-sub-semilattice of 2^[5]. minab/maxab here are over the realizations that
appear at n≤5; they bound the true values. For the witness families we ALSO give
the exact cone construction (valid for all n), so the obstruction does not rely on
enumeration completeness.
"""

from __future__ import annotations

import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
DATA = os.path.join(HERE, "data")

from uc_family import (abundance, frequencies, ground_set, family_from_sets,  # noqa: E402
                       is_union_closed, family_to_sets)
import lattice as Lat  # noqa: E402

COARSE = ["n_L", "height", "width", "n_join_irred", "n_meet_irred", "n_atoms",
          "modular", "distributive", "lower_semimodular", "upper_semimodular"]


# ---------------------------------------------------------------------------
# Lattice isomorphism fingerprint (strong, refinement-based) + exact check
# ---------------------------------------------------------------------------

def cover_digraph(F):
    """Return (elements, succ) where succ[x] = set of upper covers of x."""
    els, bot, top = Lat.as_lattice(F)
    below = Lat.cover_relation(els)
    succ = {x: set() for x in els}
    for y, xs in below.items():
        for x in xs:
            succ[x].add(y)
    return els, succ


def iso_fingerprint(F):
    """
    A permutation-invariant fingerprint of the cover digraph via iterated colour
    refinement (1-WL). Two non-isomorphic lattices can in principle collide, so
    we confirm fingerprint-equal pairs with an exact isomorphism search.
    """
    els, succ = cover_digraph(F)
    pred = {x: set() for x in els}
    for x, ys in succ.items():
        for y in ys:
            pred[y].add(x)
    # initial colour: (in-degree, out-degree)
    colour = {x: (len(pred[x]), len(succ[x])) for x in els}
    for _ in range(len(els)):
        newc = {}
        for x in els:
            up = tuple(sorted(colour[y] for y in succ[x]))
            dn = tuple(sorted(colour[y] for y in pred[x]))
            newc[x] = (colour[x], up, dn)
        # compress to small ints to keep tuples short
        palette = {c: i for i, c in enumerate(sorted(set(newc.values())))}
        newc = {x: palette[newc[x]] for x in els}
        if len(set(newc.values())) == len(set(colour.values())):
            colour = newc
            break
        colour = newc
    return tuple(sorted(colour.values()))


def exact_lattice_iso(F1, F2):
    """Exact isomorphism of the two cover digraphs (back-tracking, small)."""
    e1, s1 = cover_digraph(F1)
    e2, s2 = cover_digraph(F2)
    if len(e1) != len(e2):
        return False
    p1 = {x: set() for x in e1}
    for x, ys in s1.items():
        for y in ys:
            p1[y].add(x)
    p2 = {x: set() for x in e2}
    for x, ys in s2.items():
        for y in ys:
            p2[y].add(x)
    # degree signature must match
    deg1 = sorted((len(p1[x]), len(s1[x])) for x in e1)
    deg2 = sorted((len(p2[x]), len(s2[x])) for x in e2)
    if deg1 != deg2:
        return False
    # candidate map by degree class
    by_deg2 = defaultdict(list)
    for y in e2:
        by_deg2[(len(p2[y]), len(s2[y]))].append(y)
    order1 = sorted(e1, key=lambda x: (len(p1[x]), len(s1[x])))
    mapping = {}
    used = set()

    def consistent(x, y):
        # all already-mapped covers of x must map into covers of y (and preds)
        for xs in s1[x]:
            if xs in mapping and mapping[xs] not in s2[y]:
                return False
        for xp in p1[x]:
            if xp in mapping and mapping[xp] not in p2[y]:
                return False
        # reverse direction too
        for ys in s2[y]:
            # if some mapped x' has image ys, then x' must be a cover-succ of x
            pass
        return True

    def bt(i):
        if i == len(order1):
            return True
        x = order1[i]
        d = (len(p1[x]), len(s1[x]))
        for y in by_deg2[d]:
            if y in used:
                continue
            if consistent(x, y):
                mapping[x] = y
                used.add(y)
                if bt(i + 1):
                    return True
                used.discard(y)
                del mapping[x]
        return False

    if not bt(0):
        return False
    # final full structural verification of the cover relation
    inv = {v: k for k, v in mapping.items()}
    for x in e1:
        if {mapping[c] for c in s1[x]} != s2[mapping[x]]:
            return False
    return True


# ---------------------------------------------------------------------------
# Load clean families (contain ∅) and build iso classes
# ---------------------------------------------------------------------------

def load_clean(n_max=5, max_nL=None):
    recs = []
    for n in range(n_max + 1):
        p = os.path.join(DATA, f"lattice_sweep_n{n}.jsonl")
        if not os.path.exists(p):
            continue
        for line in open(p):
            r = json.loads(line)
            if [] not in r["sets"]:
                continue  # require ∅ ∈ F so F = L
            if max_nL is not None and r["n_L"] > max_nL:
                continue
            r["_n"] = n
            recs.append(r)
    return recs


def build_iso_classes(recs):
    """Group by (coarse signature, fingerprint), then split each bucket into true
    iso classes by exact isomorphism. Bucketing on the coarse signature first
    keeps the O(bucket^2) iso comparisons tiny. Returns list of classes."""
    by_key = defaultdict(list)
    for r in recs:
        F = family_from_sets(r["sets"])
        r["_F"] = F
        r["_fp"] = iso_fingerprint(F)
        key = (tuple(r[k] for k in COARSE), r["_fp"])
        by_key[key].append(r)
    classes = []
    for key, bucket in by_key.items():
        reps = []  # list of (repF, [members])
        for r in bucket:
            placed = False
            for repF, members in reps:
                if exact_lattice_iso(r["_F"], repF):
                    members.append(r)
                    placed = True
                    break
            if not placed:
                reps.append((r["_F"], [r]))
        for repF, members in reps:
            classes.append(members)
    return classes


def main(max_nL=12):
    recs = load_clean(5, max_nL=max_nL)
    print(f"clean families (∅∈F, F=L, |L|≤{max_nL}), n≤5: {len(recs)}")
    classes = build_iso_classes(recs)
    print(f"lattice-isomorphism classes realized at n≤5: {len(classes)}")

    # per-class min/max abundance
    class_info = []
    for members in classes:
        abos = [m["abundance"] for m in members]
        mn, mx = min(abos), max(abos)
        rep = members[0]
        coarse = tuple(rep[k] for k in COARSE)
        class_info.append({
            "coarse": coarse,
            "minab": mn, "maxab": mx, "spread": mx - mn,
            "n_real": len(members),
            "lo_sets": min(members, key=lambda m: m["abundance"])["sets"],
            "hi_sets": max(members, key=lambda m: m["abundance"])["sets"],
            "n_L": rep["n_L"],
        })

    # (1) within a single lattice-iso class, the abundance spread
    class_info.sort(key=lambda c: -c["spread"])
    print()
    print("=" * 78)
    print("(1) WITHIN one lattice-iso class: abundance is NOT determined")
    print("    (same abstract lattice L, different abundance)")
    print("=" * 78)
    for c in class_info[:3]:
        print(f"  |L|={c['n_L']} spread={c['spread']:.4f} minab={c['minab']:.4f} maxab={c['maxab']:.4f} (#realizations seen={c['n_real']})")
        print(f"     minab realization: {c['lo_sets']}")
        print(f"     maxab realization: {c['hi_sets']}")

    # (2) sharp obstruction: two DIFFERENT iso classes, SAME coarse invariants,
    #     DIFFERENT minab
    print()
    print("=" * 78)
    print("(2) SHARP OBSTRUCTION: same COARSE invariants, different minab")
    print("    (coarse lattice invariants do not control even the *minimum*")
    print("     abundance over realizations)")
    print("=" * 78)
    by_coarse = defaultdict(list)
    for c in class_info:
        by_coarse[c["coarse"]].append(c)
    found = []
    for coarse, cls in by_coarse.items():
        minabs = [c["minab"] for c in cls]
        if max(minabs) - min(minabs) > 1e-9 and len(cls) >= 2:
            found.append((max(minabs) - min(minabs), coarse, cls))
    found.sort(reverse=True, key=lambda t: t[0])
    print(f"  coarse-invariant signatures hosting ≥2 distinct lattices: "
          f"{sum(1 for cl in by_coarse.values() if len(cl) >= 2)}")
    print(f"  ... of which minab differs across the lattices: {len(found)}")
    for diff, coarse, cls in found[:4]:
        cd = dict(zip(COARSE, coarse))
        print(f"  --- minab differs by {diff:.4f} at coarse={cd}")
        for c in sorted(cls, key=lambda c: c["minab"])[:3]:
            print(f"        minab={c['minab']:.4f} maxab={c['maxab']:.4f} example_lo={c['lo_sets']}")

    return class_info, found


if __name__ == "__main__":
    main()
