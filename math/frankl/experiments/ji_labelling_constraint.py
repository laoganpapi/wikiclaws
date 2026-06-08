"""
ji_labelling_constraint.py — the reconstruction constraint and the candidate
forcing structural lemma on the fibre system.

THE CONSTRAINT (made precise)
-----------------------------
Let L = (F, cup) with emptyset, JI(L) = join-irreducibles. By Birkhoff every
A in L is A = cup{ j in JI : j <= A }. For a ground element x:
    Fib(x) = { A : x in A } = union over { j in JI : x in j } of  up(j).
i.e. each fibre is the UNION of the principal JI-filters of the JIs that
*contain x as a ground element*. Equivalently, define for each JI j its label
set lab(j) = { x : x in j and j is the minimal member of Fib(x) generated... }.
Operationally we just compute, for each x, the set  J(x) = { j in JI : x in j and
j minimal in Fib(x) }, and verify  Fib(x) = union_{j in J(x)} up(j).

KEY QUANTITIES per family:
  - density of a single JI-filter:  d(j) = |up(j)| / |L|
  - the fibre of x is a union of |J(x)| such filters; its density is abundance-
    relevant. The "inclusion-exclusion gain" g(x) = |Fib(x)| - max_j |up(j)| over
    j in J(x) measures how much the UNION beats the best single JI-filter.

CANDIDATE FORCING CONSTRAINT (tested, NOT proved):
  (C1) Coverage identity: sum_{j in JI} |up(j)| relates to sum_x |Fib(x)| via the
       JI-incidence; we test the exact identity and whether it forces a heavy x.
  (C2) The "shared-top" mechanism: every JI-filter contains the top T, so any two
       JI-filters overlap (in >= the up-set of their join). Test whether the
       max fibre density is forced >= f(#JI, |L|).
  (C3) Per-JI label-disjointness: the label sets {lab(j)} of distinct JIs need
       NOT be disjoint, but their UNION is [n] and each A = union of labels of
       JIs <= A. This is the reconstruction map. We measure the worst case.

Author: Alex Ye. [NOVELTY UNVERIFIED]. No proof claimed; validated on all n<=5.
Writes data/ji_constraint_summary.txt
"""
from __future__ import annotations

import json
import sys
import time

from enumerate import all_uc_families
from uc_family import abundance, frequencies, ground_set
import ji_labelling as jl
import lattice as lat


def analyze_family(F, n):
    L = jl.with_bottom(F)
    elements, bottom, top = lat.as_lattice(L)
    m = len(elements)
    fibs = jl.fibres(L, n)
    jis = lat.join_irreducibles(elements)
    ji_filter_size = {j: lat.principal_filter_size(elements, j) for j in jis}

    out = {
        "m": m, "n_ji": len(jis), "abundance": abundance(L),
        "max_single_ji_density": (max(ji_filter_size.values()) / m) if jis else 0.0,
    }

    # for each ground element, its fibre as union of JI-filters (minimal gens)
    recon_ok = True
    max_union_gain = 0.0       # |Fib(x)| - best single JI filter inside
    n_jis_in_fibre = []
    for x in range(n):
        S = fibs[x]
        if not S:
            continue
        # minimal members of S are exactly the JIs j with x in j that are
        # minimal in Fib(x)
        minimal = [A for A in S
                   if not any((B & A) == B and B != A for B in S)]
        # reconstruct union of up(min)
        union = set()
        for mn in minimal:
            for e in elements:
                if (mn & e) == mn:
                    union.add(e)
        if frozenset(union) != S:
            recon_ok = False
        n_jis_in_fibre.append(len(minimal))
        best_single = max((lat.principal_filter_size(elements, mn)
                           for mn in minimal), default=0)
        gain = (len(S) - best_single) / m
        max_union_gain = max(max_union_gain, gain)

    out["recon_ok"] = recon_ok
    out["max_jis_per_fibre"] = max(n_jis_in_fibre, default=0)
    out["max_union_gain"] = max_union_gain
    return out


def run(n_max=5):
    EPS = 1e-9
    t = time.time()
    summary = {
        "total": 0,
        "recon_violations": 0,
        # how often abundance EXCEEDS the best single JI-filter density (i.e. a
        # genuine union effect is needed):
        "union_strictly_beats_single_ji": 0,
        "min_max_single_ji_density": 2.0,
        "max_jis_per_fibre_overall": 0,
        # the candidate constraint: abundance >= max_single_ji_density always?
        "abund_ge_single_ji": 0,
        # and the GAP abundance - max_single_ji_density distribution
        "max_gap_abund_minus_singleji": 0.0,
        # families where even the FULL union of ALL JI-filters of contained JIs
        # is needed to reach >=1/2 (single never does)
        "need_union_for_half": 0,
    }
    examples = []
    for n in range(n_max + 1):
        for F in all_uc_families(n, dedupe_isomorphic=True,
                                 include_empty_family=False):
            if len(F) < 2:
                continue
            L = jl.with_bottom(F)
            nn = ground_set(L)
            if nn == 0:
                continue
            a = analyze_family(F, nn)
            summary["total"] += 1
            if not a["recon_ok"]:
                summary["recon_violations"] += 1
            ab = a["abundance"]
            sji = a["max_single_ji_density"]
            summary["min_max_single_ji_density"] = min(
                summary["min_max_single_ji_density"], sji)
            summary["max_jis_per_fibre_overall"] = max(
                summary["max_jis_per_fibre_overall"], a["max_jis_per_fibre"])
            if ab >= sji - EPS:
                summary["abund_ge_single_ji"] += 1
            if ab > sji + EPS:
                summary["union_strictly_beats_single_ji"] += 1
            summary["max_gap_abund_minus_singleji"] = max(
                summary["max_gap_abund_minus_singleji"], ab - sji)
            # need_union_for_half: abundance>=1/2 but NO single JI-filter >=1/2
            if ab >= 0.5 - EPS and sji < 0.5 - EPS:
                summary["need_union_for_half"] += 1
                if len(examples) < 12:
                    examples.append({
                        "sets": [sorted(jl.mask_to_set(x)) for x in sorted(F)],
                        "ab": round(ab, 4), "max_single_ji": round(sji, 4),
                        "m": a["m"], "n_ji": a["n_ji"],
                    })
    out = "data/ji_constraint_summary.txt"
    with open(out, "w") as fh:
        def w(s=""):
            print(s)
            fh.write(s + "\n")
        w("=" * 72)
        w("FIBRE-SYSTEM RECONSTRUCTION CONSTRAINT (Alex Ye) [NOVELTY UNVERIFIED]")
        w("=" * 72)
        w(f"total families (n<={n_max}): {summary['total']}  "
          f"({round(time.time()-t,1)}s)")
        w(f"reconstruction Fib(x)=union of JI-filters: "
          f"{summary['recon_violations']} violations (expect 0)")
        w("")
        w("--- single JI-filter vs the union (abundance) ---")
        w(f"  abundance >= max single-JI-filter density: "
          f"{summary['abund_ge_single_ji']} / {summary['total']} (expect ALL)")
        w(f"  abundance STRICTLY beats best single JI-filter "
          f"(union effect needed): {summary['union_strictly_beats_single_ji']}")
        w(f"  min over families of (max single-JI-filter density): "
          f"{summary['min_max_single_ji_density']:.4f}  "
          f"(<1/2 => single JI NEVER suffices for those)")
        w(f"  max gap abundance - max_single_ji_density: "
          f"{summary['max_gap_abund_minus_singleji']:.4f}")
        w(f"  max #JIs whose filters union to one fibre: "
          f"{summary['max_jis_per_fibre_overall']}")
        w("")
        w(f"--- families where abundance>=1/2 but NO single JI-filter reaches "
          f"1/2 (the UNION is essential): {summary['need_union_for_half']} ---")
        for ex in examples:
            w(f"  sets={ex['sets']} m={ex['m']} #JI={ex['n_ji']} "
              f"ab={ex['ab']} max_single_ji={ex['max_single_ji']}")
    with open("data/ji_constraint_summary.json", "w") as fh:
        json.dump(summary, fh, indent=2)
    print("\nwrote", out)


if __name__ == "__main__":
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
