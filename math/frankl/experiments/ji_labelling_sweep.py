"""
ji_labelling_sweep.py — Sweep H1-H4 over all UC families n<=5.

Writes:
  data/ji_sweep_n{0..5}.jsonl  (per-family fibre/JI records)
  data/ji_summary.txt          (H1-H4 aggregate findings)

Author: Alex Ye. [NOVELTY UNVERIFIED]. No proof claimed.
"""
from __future__ import annotations

import json
import sys
import time

from enumerate import all_uc_families
from uc_family import abundance, frequencies, ground_set
import ji_labelling as jl
import lattice as lat


def sweep(n_max: int = 5) -> None:
    EPS = 1e-9
    summary = {
        "total": 0,
        # H1: principal-filter (JI) fibres
        "h1_ji_reaches_abundance": 0,   # max JI-filter density == abundance
        "h1_ji_ge_half": 0,             # some JI-filter density >= 1/2
        "h1_min_max_ji_density": 2.0,   # min over families of max JI density
        "h1_families_ji_lt_half": 0,    # families where NO JI fibre reaches 1/2
        "h1_examples_ji_lt_half": [],
        # also all-principal-filter (every element generates one)
        "h1b_principal_reaches_abundance": 0,
        # H2: co-atom / meet-irreducible
        "h2_coatom_ge_half": 0,
        "h2_min_max_coatom_density": 2.0,
        "h2_mi_reaches_abundance": 0,
        "h2_max_coatom_density_overall": 0.0,
        # H3: counting identity check Sum_x|Fib(x)| = Sum_A|A|
        "h3_identity_violations": 0,
        # general
        "abundance_below_half": 0,
        "min_abundance": 2.0,
        # how often abundance is achieved by a principal (JI) fibre vs non-principal
        "abund_by_principal": 0,
        "abund_by_nonprincipal": 0,
    }

    for n in range(n_max + 1):
        path = f"data/ji_sweep_n{n}.jsonl"
        t = time.time()
        cnt = 0
        with open(path, "w") as fh:
            for F in all_uc_families(n, dedupe_isomorphic=True,
                                     include_empty_family=False):
                if len(F) < 2:
                    continue
                L = jl.with_bottom(F)
                nn = ground_set(L)
                if nn == 0:
                    continue
                rep = jl.ji_fibre_report(F, nn)
                ab = rep["abundance"]
                m = rep["m"]
                elements = rep["elements"]

                summary["total"] += 1
                cnt += 1
                summary["min_abundance"] = min(summary["min_abundance"], ab)
                if ab < 0.5 - EPS:
                    summary["abundance_below_half"] += 1

                # H1
                maxji = rep["max_principal_ji_density"]
                summary["h1_min_max_ji_density"] = min(
                    summary["h1_min_max_ji_density"], maxji)
                if maxji >= 0.5 - EPS:
                    summary["h1_ji_ge_half"] += 1
                if abs(maxji - ab) < EPS:
                    summary["h1_ji_reaches_abundance"] += 1
                else:
                    if maxji < 0.5 - EPS:
                        summary["h1_families_ji_lt_half"] += 1
                        if len(summary["h1_examples_ji_lt_half"]) < 12:
                            summary["h1_examples_ji_lt_half"].append({
                                "sets": [sorted(jl.mask_to_set(a)) for a in
                                         sorted(F)],
                                "ab": round(ab, 4),
                                "maxji": round(maxji, 4),
                                "m": m,
                            })
                if abs(rep["max_principal_density"] - ab) < EPS:
                    summary["h1b_principal_reaches_abundance"] += 1

                # Is abundance achieved by a principal fibre?
                # find the most abundant element and check principal flag
                freqs = frequencies(L, nn)
                bestx = max(range(nn), key=lambda i: freqs[i])
                if rep["principal"].get(bestx):
                    summary["abund_by_principal"] += 1
                else:
                    summary["abund_by_nonprincipal"] += 1

                # H2
                maxco = rep["max_coatom_filter_density"]
                summary["h2_min_max_coatom_density"] = min(
                    summary["h2_min_max_coatom_density"], maxco)
                summary["h2_max_coatom_density_overall"] = max(
                    summary["h2_max_coatom_density_overall"], maxco)
                if maxco >= 0.5 - EPS:
                    summary["h2_coatom_ge_half"] += 1
                if abs(rep["max_mi_density"] - ab) < EPS:
                    summary["h2_mi_reaches_abundance"] += 1

                # H3: counting identity
                lhs = sum(rep["fib_size"][x] for x in range(nn))
                rhs = sum(bin(A).count("1") for A in L)
                if lhs != rhs:
                    summary["h3_identity_violations"] += 1

                fh.write(json.dumps({
                    "n": n,
                    "m": m,
                    "ab": ab,
                    "maxji": maxji,
                    "maxco": maxco,
                    "max_mi": rep["max_mi_density"],
                    "principal": rep["principal"],
                    "freq_sorted": sorted(freqs, reverse=True),
                }) + "\n")
        print(f"n={n}: {cnt} families, {round(time.time()-t,1)}s")

    # finalize
    with open("data/ji_summary.txt", "w") as fh:
        def w(s=""):
            print(s)
            fh.write(s + "\n")
        w("=" * 72)
        w("JI / FIBRE LABELLING SWEEP — H1-H4 (Alex Ye) [NOVELTY UNVERIFIED]")
        w("=" * 72)
        w(f"Total UC families (|F|>=2, n<={n_max}): {summary['total']}")
        w(f"min abundance over all families: {summary['min_abundance']:.4f}")
        w(f"families with abundance < 1/2: {summary['abundance_below_half']}")
        w("")
        w("--- H1: PRINCIPAL (join-irreducible) fibres ---")
        w(f"  max JI-filter density >= 1/2 in: {summary['h1_ji_ge_half']} "
          f"/ {summary['total']} families")
        w(f"  max JI-filter density == abundance in: "
          f"{summary['h1_ji_reaches_abundance']} families")
        w(f"  min over families of (max JI-filter density): "
          f"{summary['h1_min_max_ji_density']:.4f}")
        w(f"  families where NO JI fibre reaches 1/2 (and ji<ab): "
          f"{summary['h1_families_ji_lt_half']}")
        w(f"  max-over-ALL-principal-filters == abundance in: "
          f"{summary['h1b_principal_reaches_abundance']} families")
        w(f"  abundance achieved by a PRINCIPAL fibre: "
          f"{summary['abund_by_principal']}; by NON-principal: "
          f"{summary['abund_by_nonprincipal']}")
        w("  Examples where max JI density < 1/2 < abundance:")
        for ex in summary["h1_examples_ji_lt_half"]:
            w(f"    sets={ex['sets']} m={ex['m']} ab={ex['ab']} "
              f"maxji={ex['maxji']}")
        w("")
        w("--- H2: CO-ATOM / MEET-IRREDUCIBLE fibres ---")
        w(f"  some co-atom filter density >= 1/2 in: "
          f"{summary['h2_coatom_ge_half']} families")
        w(f"  max-over-families of (max co-atom filter density): "
          f"{summary['h2_max_coatom_density_overall']:.4f}")
        w(f"  min-over-families of (max co-atom filter density): "
          f"{summary['h2_min_max_coatom_density']:.4f}")
        w(f"  max MI-filter density == abundance in: "
          f"{summary['h2_mi_reaches_abundance']} families")
        w("")
        w("--- H3: counting identity Sum_x|Fib(x)| = Sum_A|A| ---")
        w(f"  violations: {summary['h3_identity_violations']} (expect 0)")
        w("")

    with open("data/ji_summary.json", "w") as fh:
        json.dump(summary, fh, indent=2)
    print("\nwrote data/ji_summary.txt, data/ji_summary.json")


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    sweep(nmax)
