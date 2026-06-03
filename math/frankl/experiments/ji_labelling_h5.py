"""
ji_labelling_h5.py — H5: labelling freedom on a FIXED abstract lattice.

For each abstract lattice L (grouped by an exact iso-invariant fingerprint +
exact iso check), collect ALL concrete realizations F' (UC families with
emptyset, n<=5) whose lattice is iso to L, and compute:
    minab(L) = min over realizations of abundance(F')
    maxab(L) = max over realizations of abundance(F')
plus the realization achieving the MIN (the "worst labelling").

We then test the H5 questions:
  (a) Is minab(L) >= 1/2 for EVERY lattice?  (this IS Frankl on the iso class)
  (b) Is the worst labelling's abundance == 1/2 EXACTLY when it is 1/2 (cube-like)?
  (c) WHAT structural feature of the worst labelling forces >= 1/2?
      In particular: at the worst labelling, is the heavy element the meet of a
      maximal-density NON-principal fibre, i.e. does the labelling freedom always
      bottom out at a "balanced" assignment?

Also H4: restrict to RIGID lattices (every element join-irreducible, or
|JI| == n at the realization) and report minab there.

Writes:
  data/ji_h5_classes.jsonl   (one record per iso class)
  data/ji_h5_summary.txt

Author: Alex Ye. [NOVELTY UNVERIFIED]. No proof claimed.

Note on exact iso: we reuse the strong fingerprint from ji_labelling plus an
exact back-tracking lattice isomorphism on the cover digraph (same approach as
lattice_minab.exact_lattice_iso). To stay self-contained and avoid touching
other agents' files, we re-implement a compact exact iso check here.
"""
from __future__ import annotations

import json
import sys
import time
from collections import defaultdict

from enumerate import all_uc_families
from uc_family import abundance, frequencies, ground_set, frequencies as freqs_of
import ji_labelling as jl
import lattice as lat


# ---------------------------------------------------------------------------
# Exact lattice isomorphism (cover-digraph iso, refined by principal-filter size)
# ---------------------------------------------------------------------------

def _cover_digraph(F):
    L = jl.with_bottom(F)
    elements, bottom, top = lat.as_lattice(L)
    below = lat.cover_relation(elements)
    pf = {e: lat.principal_filter_size(elements, e) for e in elements}
    # downset size too (dual)
    ds = {e: sum(1 for x in elements if (x & e) == x) for e in elements}
    idx = {e: i for i, e in enumerate(elements)}
    n = len(elements)
    # adjacency of cover relation (lower-cover): cov[a] = set of upper covers
    above = lat.upper_covers(elements)
    cov = [set(idx[y] for y in above[e]) for e in elements]
    colour = [(pf[e], ds[e]) for e in elements]
    return n, cov, colour


def exact_lattice_iso(F1, F2) -> bool:
    n1, cov1, col1 = _cover_digraph(F1)
    n2, cov2, col2 = _cover_digraph(F2)
    if n1 != n2:
        return False
    # quick colour-multiset check
    if sorted(col1) != sorted(col2):
        return False
    # backtracking iso on the cover digraph respecting colour
    # precompute reverse adjacency
    rev1 = [set() for _ in range(n1)]
    for a in range(n1):
        for b in cov1[a]:
            rev1[b].add(a)
    rev2 = [set() for _ in range(n2)]
    for a in range(n2):
        for b in cov2[a]:
            rev2[b].add(a)
    # candidate targets by colour
    cand = [[j for j in range(n2) if col2[j] == col1[i]] for i in range(n1)]
    mapping = [-1] * n1
    used = [False] * n2
    order = sorted(range(n1), key=lambda i: len(cand[i]))

    def ok(i, j):
        # check consistency with already-mapped neighbours
        for a in cov1[i]:
            if mapping[a] != -1 and mapping[a] not in cov2[j]:
                return False
        for a in rev1[i]:
            if mapping[a] != -1 and mapping[a] not in rev2[j]:
                return False
        # degree match
        if len(cov1[i]) != len(cov2[j]) or len(rev1[i]) != len(rev2[j]):
            return False
        return True

    def bt(k):
        if k == n1:
            return True
        i = order[k]
        for j in cand[i]:
            if used[j] or not ok(i, j):
                continue
            mapping[i] = j
            used[j] = True
            if bt(k + 1):
                return True
            mapping[i] = -1
            used[j] = False
        return False

    return bt(0)


# ---------------------------------------------------------------------------
# H5 driver
# ---------------------------------------------------------------------------

def run(n_max: int = 5) -> None:
    EPS = 1e-9
    # bucket realizations by fingerprint
    buckets = defaultdict(list)  # fp -> list of (F, abundance, n)
    t = time.time()
    total = 0
    for n in range(n_max + 1):
        for F in all_uc_families(n, dedupe_isomorphic=True,
                                 include_empty_family=False):
            if len(F) < 2:
                continue
            L = jl.with_bottom(F)
            nn = ground_set(L)
            if nn == 0:
                continue
            fp = jl.lattice_fingerprint(F)
            buckets[fp].append((F, abundance(L), nn))
            total += 1
    print(f"collected {total} families into {len(buckets)} fingerprint buckets "
          f"({round(time.time()-t,1)}s)")

    # within each fingerprint bucket, split into exact iso classes
    classes = []  # each: list of (F, ab, n)
    for fp, members in buckets.items():
        reps = []  # list of (representative_F, [members])
        for (F, ab, nn) in members:
            placed = False
            for r in reps:
                if exact_lattice_iso(F, r[0]):
                    r[1].append((F, ab, nn))
                    placed = True
                    break
            if not placed:
                reps.append((F, [(F, ab, nn)]))
        for r in reps:
            classes.append(r[1])
    print(f"refined into {len(classes)} exact lattice-iso classes "
          f"({round(time.time()-t,1)}s)")

    # analyze
    summary = {
        "n_classes": len(classes),
        "classes_minab_below_half": 0,
        "global_min_minab": 2.0,
        "min_at_half_classes": 0,       # classes whose minab == 1/2 exactly
        "min_above_half_classes": 0,    # classes whose minab > 1/2
        "worst_label_ab_distribution": defaultdict(int),  # rounded minab -> count
        "spread_examples": [],          # classes with large maxab-minab spread
        # H4 rigid: classes where every element is a JI (all_join_irreducible)
        "rigid_alljisi_classes": 0,
        "rigid_alljisi_minab_below_half": 0,
        "rigid_alljisi_min_minab": 2.0,
        "rigid_jieqn_classes": 0,
        "rigid_jieqn_min_minab": 2.0,
    }

    class_records = []
    for members in classes:
        abs_ = [ab for (_, ab, _) in members]
        minab = min(abs_)
        maxab = max(abs_)
        # worst (min-ab) realization
        worstF, _, worstn = min(members, key=lambda t: t[1])
        rep0 = members[0][0]
        rigid = jl.ji_rigidity_class(rep0, members[0][2])

        summary["global_min_minab"] = min(summary["global_min_minab"], minab)
        if minab < 0.5 - EPS:
            summary["classes_minab_below_half"] += 1
        if abs(minab - 0.5) < EPS:
            summary["min_at_half_classes"] += 1
        elif minab > 0.5 + EPS:
            summary["min_above_half_classes"] += 1
        summary["worst_label_ab_distribution"][round(minab, 4)] += 1

        if rigid["all_join_irreducible"]:
            summary["rigid_alljisi_classes"] += 1
            summary["rigid_alljisi_min_minab"] = min(
                summary["rigid_alljisi_min_minab"], minab)
            if minab < 0.5 - EPS:
                summary["rigid_alljisi_minab_below_half"] += 1
        if rigid["ji_eq_n"]:
            summary["rigid_jieqn_classes"] += 1
            summary["rigid_jieqn_min_minab"] = min(
                summary["rigid_jieqn_min_minab"], minab)

        rec = {
            "m": len(jl.with_bottom(rep0)),
            "n_realizations": len(members),
            "minab": round(minab, 5),
            "maxab": round(maxab, 5),
            "spread": round(maxab - minab, 5),
            "all_join_irreducible": rigid["all_join_irreducible"],
            "ji_eq_n_rep": rigid["ji_eq_n"],
            "worst_sets": [sorted(jl.mask_to_set(a)) for a in sorted(worstF)],
        }
        class_records.append(rec)
        if rec["spread"] >= 0.2 and len(summary["spread_examples"]) < 15:
            summary["spread_examples"].append({
                "m": rec["m"], "minab": rec["minab"], "maxab": rec["maxab"],
                "worst_sets": rec["worst_sets"],
            })

    with open("data/ji_h5_classes.jsonl", "w") as fh:
        for rec in class_records:
            fh.write(json.dumps(rec) + "\n")

    with open("data/ji_h5_summary.txt", "w") as fh:
        def w(s=""):
            print(s)
            fh.write(s + "\n")
        w("=" * 72)
        w("H5: LABELLING FREEDOM on a FIXED abstract lattice (Alex Ye)")
        w("[NOVELTY UNVERIFIED]  no proof claimed")
        w("=" * 72)
        w(f"exact lattice-iso classes (|L|, n<={n_max}): {summary['n_classes']}")
        w(f"global min over classes of minab(L): "
          f"{summary['global_min_minab']:.4f}")
        w(f"classes with minab(L) < 1/2 (would refute Frankl): "
          f"{summary['classes_minab_below_half']}")
        w(f"classes with minab(L) == 1/2 EXACTLY (worst label is cube-like): "
          f"{summary['min_at_half_classes']}")
        w(f"classes with minab(L) > 1/2 (cone-forced / non-distributive heavy): "
          f"{summary['min_above_half_classes']}")
        w("")
        w("Distribution of worst-labelling abundance minab(L) (rounded):")
        for k in sorted(summary["worst_label_ab_distribution"]):
            w(f"    minab={k:.4f} : {summary['worst_label_ab_distribution'][k]} "
              f"classes")
        w("")
        w("--- H4: RIGID lattices (every L-element is a join-irreducible) ---")
        w(f"  classes with all-elements-join-irreducible: "
          f"{summary['rigid_alljisi_classes']}")
        w(f"  ...of those with minab < 1/2: "
          f"{summary['rigid_alljisi_minab_below_half']}")
        w(f"  ...min minab among them: "
          f"{summary['rigid_alljisi_min_minab']:.4f}")
        w(f"  classes with |JI| == n at the representative: "
          f"{summary['rigid_jieqn_classes']} "
          f"(min minab {summary['rigid_jieqn_min_minab']:.4f})")
        w("")
        w("--- Large-spread classes (labelling freedom maximally exploited) ---")
        for ex in summary["spread_examples"]:
            w(f"  m={ex['m']} minab={ex['minab']} maxab={ex['maxab']} "
              f"worst={ex['worst_sets']}")

    # JSON (convert defaultdict)
    summary["worst_label_ab_distribution"] = dict(
        summary["worst_label_ab_distribution"])
    with open("data/ji_h5_summary.json", "w") as fh:
        json.dump(summary, fh, indent=2)
    print("\nwrote data/ji_h5_classes.jsonl, ji_h5_summary.txt, ji_h5_summary.json")


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    run(nmax)
