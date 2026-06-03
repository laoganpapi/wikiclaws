"""
ji_overlap.py — The JI-filter OVERLAP <-> abundance identity, and the exact
overlap lower bound that would close Frankl via Cauchy-Schwarz / power-mean.

Author: Alex Ye (no AI on author line).
Status: [NOVELTY UNVERIFIED] — exploratory; every claim validated on all UC
        families n<=5. No proof claimed. Writes data/overlap_*.{jsonl,txt}.

Foundation:
  frankl/theory/join_irreducible_labelling.md   (Fib(x) = U_{j: x in j} up(j))
  frankl/theory/second_moment.md                (Sum freq^2 = Sum_{A,B}|A cap B|)
  frankl/theory/lp_duality.md  §6               (max-vs-mean / power-mean lever)

THE TARGET CHAIN (precise)
--------------------------
Work in L = (F, cup) WITH the bottom emptyset adjoined, |L| = m.  (This is the
lattice; abundance is about Fib(x) which are filters of L. We track BOTH the
L-normalisation |L|/2 and the family normalisation |F|/2; they differ by the
bottom which is in no fibre.)

For a ground element x, Fib(x) = {A in L : x in A}.  The two moments of the
fibre-size vector (freq_x := |Fib(x)|, x in [n]):
    P1 := Sum_x |Fib(x)|  = Sum_{A in L} |A|              (first moment)
    P2 := Sum_x |Fib(x)|^2                                 (second moment)

EXACT IDENTITY (the whole game), derived by swapping summation order:
    |Fib(x)|^2 = #{(A,B) in L x L : x in A, x in B}
    P2 = Sum_x #{(A,B): x in A cap B} = Sum_{(A,B) in LxL} |A cap B|.
So
    P2 = Sum_{(A,B) in LxL} |A cap B|   =:  OVL(L)        (total overlap).

POWER-MEAN (weighted-by-itself) bound, over ground elements x:
    max_x |Fib(x)|  >=  P2 / P1  =  OVL(L) / Sum_{A in L}|A|.
Hence the SUFFICIENT overlap inequality for Frankl (L-normalised) is
    (TARGET-L)   OVL(L) >= (|L|/2) * Sum_{A in L}|A|.
And the family-normalised sufficient inequality (abundance := max freq / |F|)
uses P1' = Sum_{A in F}|A| (= P1 since bottom contributes 0) and needs
    max_x |Fib(x)| >= |F|/2, i.e. via power-mean
    (TARGET-F)   OVL(F) >= (|F|/2) * Sum_{A in F}|A|,
where OVL(F) = Sum_{(A,B) in FxF}|A cap B| (= P2 computed without the bottom,
which equals OVL(L) since the empty set contributes 0 to every intersection).

NOTE: P2 = OVL(L) = OVL(F) exactly (emptyset adds nothing). The ONLY difference
between TARGET-L and TARGET-F is the threshold |L|/2 vs |F|/2 and whether the
bottom is counted in P1 (it is not, |emptyset|=0). So when emptyset in F,
|L|=|F| and the two coincide; when emptyset not in F, |L|=|F|+1 and TARGET-L is
the STRONGER ask (bigger threshold). We test BOTH and report.

THE JI-FILTER DECOMPOSITION OF OVL (the structural lever)
---------------------------------------------------------
By Birkhoff, Fib(x) = U_{j in JI, x in j} up(j). Inclusion-exclusion on this
union is what the brief asks for. We ALSO compute the raw JI-filter overlap
    JIOVL := Sum_{(j,k) in JI x JI} |up(j) cap up(k)|
and the structured lower bound from up(j) cap up(k) >= up(j v k):
    JIOVL_lb := Sum_{(j,k)} |up(j v k)|   (j v k is in L since L is a lattice).
These probe whether the *structured* overlap (via the join) is enough.

We compute every quantity in EXACT integer arithmetic and check the inequalities
as exact rationals (cross-multiplied) to avoid float error.
"""
from __future__ import annotations

import json
import sys
import time
from fractions import Fraction

from enumerate import all_uc_families
from uc_family import abundance, frequencies, ground_set
import ji_labelling as jl
import lattice as lat


def analyze_family(F, n):
    """Return the exact overlap/abundance quantities for one UC family F.

    All sums are exact integers. Inequalities checked as exact rationals.
    """
    L = jl.with_bottom(F)               # adjoin emptyset
    elements, bottom, top = lat.as_lattice(L)
    mL = len(elements)                  # |L|
    # |F|: family WITHOUT the artificially adjoined bottom counts as Frankl's |F|.
    # The project census uses F as enumerated (which may or may not contain ∅).
    Fset = frozenset(F)
    mF = len(Fset)

    # fibre sizes over ground [n]
    freqs = frequencies(elements, n)    # |Fib(x)| for x in [n], over L (=over F)
    P1 = sum(freqs)                     # Sum_x |Fib(x)| = Sum_{A in L}|A|
    P2 = sum(f * f for f in freqs)      # Sum_x |Fib(x)|^2
    maxfib = max(freqs) if freqs else 0

    # OVL via the identity, computed the OTHER way as a cross-check
    elist = elements
    OVL = 0
    for A in elist:
        for B in elist:
            OVL += bin(A & B).count("1")
    # sanity: P2 == OVL exactly
    assert P2 == OVL, (P2, OVL, sorted(elements))

    # Sum_{A in L}|A| both ways
    sumA = sum(bin(A).count("1") for A in elist)
    assert sumA == P1, (sumA, P1)

    # JI-filter overlap and its structured lower bound
    jis = lat.join_irreducibles(elements)
    # filter membership: up(a) = {x in L : a subset x}
    def upset(a):
        return [x for x in elist if (a & x) == a]
    up_sizes = {a: len(upset(a)) for a in elist}
    JIOVL = 0
    JIOVL_lb = 0     # via up(j) cap up(k) >= up(j v k)
    JIOVL_exact_cap = 0
    for j in jis:
        upj = set(upset(j))
        for k in jis:
            upk = set(upset(k))
            cap = upj & upk
            JIOVL += len(cap)
            jvk = j | k                 # join in L (= OR; in L since UC)
            JIOVL_lb += up_sizes[jvk]
            JIOVL_exact_cap += len(cap)
    # sanity on the structured bound: up(j) cap up(k) ⊇ up(j v k) so JIOVL >= JIOVL_lb
    assert JIOVL >= JIOVL_lb, (JIOVL, JIOVL_lb)

    sum_ji_filter = sum(up_sizes[j] for j in jis)   # Sum_j |up(j)|

    # --- the TARGET inequalities, exact rationals ---
    # TARGET-L:  OVL >= (|L|/2) * P1   <=>  2*OVL >= |L|*P1
    target_L_holds = (2 * P2 >= mL * P1)
    target_L_slack = Fraction(2 * P2 - mL * P1)      # >=0 means holds
    # TARGET-F:  2*OVL >= |F|*P1
    target_F_holds = (2 * P2 >= mF * P1)
    target_F_slack = Fraction(2 * P2 - mF * P1)

    # the achieved power-mean lower bound on max fibre (as a Fraction of |L|)
    # pm = P2/P1 ; abundance_L = maxfib/|L| ; Frankl_L: maxfib/|L| >= 1/2
    pm = Fraction(P2, P1) if P1 else Fraction(0)
    pm_density_L = Fraction(P2, P1 * mL) if P1 and mL else Fraction(0)  # pm/|L|
    pm_density_F = Fraction(P2, P1 * mF) if P1 and mF else Fraction(0)
    true_abund_L = Fraction(maxfib, mL) if mL else Fraction(0)
    true_abund_F = Fraction(maxfib, mF) if mF else Fraction(0)

    # cube detection: is this the Boolean cube 2^[k]?
    k = n
    is_cube = (mF == (1 << k)) and (Fset == frozenset(range(1 << k)))

    return {
        "n": n,
        "mL": mL,
        "mF": mF,
        "n_ji": len(jis),
        "P1": P1,
        "P2": P2,
        "OVL": OVL,
        "JIOVL": JIOVL,
        "JIOVL_lb": JIOVL_lb,
        "sum_ji_filter": sum_ji_filter,
        "maxfib": maxfib,
        "true_abund_L": float(true_abund_L),
        "true_abund_F": float(true_abund_F),
        "pm_density_L": float(pm_density_L),
        "pm_density_F": float(pm_density_F),
        "target_L_holds": bool(target_L_holds),
        "target_F_holds": bool(target_F_holds),
        "target_L_slack": int(target_L_slack),     # 2*P2 - |L|*P1
        "target_F_slack": int(target_F_slack),     # 2*P2 - |F|*P1
        "is_cube": bool(is_cube),
        "family": sorted(Fset),
    }


def run(nmax):
    t0 = time.time()
    rows = []
    per_n = {}
    for n in range(nmax + 1):
        cnt = 0
        for F in all_uc_families(n):
            Fset = frozenset(F)
            if len(Fset) < 2:
                continue
            r = analyze_family(Fset, n)
            rows.append(r)
            cnt += 1
        per_n[n] = cnt
        with open(f"data/overlap_n{n}.jsonl", "w") as fh:
            for r in rows:
                if r["n"] == n:
                    fh.write(json.dumps(r) + "\n")
    summarize(rows, per_n, time.time() - t0, nmax)
    return rows


def summarize(rows, per_n, dt, nmax):
    total = len(rows)
    # TARGET-L
    L_fail = [r for r in rows if not r["target_L_holds"]]
    F_fail = [r for r in rows if not r["target_F_holds"]]
    # tightness on the cube: slack == 0 exactly
    cubes = [r for r in rows if r["is_cube"]]
    cube_L_slack = sorted(set(r["target_L_slack"] for r in cubes))
    cube_F_slack = sorted(set(r["target_F_slack"] for r in cubes))
    # equality (slack 0) families for TARGET-L
    L_eq = [r for r in rows if r["target_L_slack"] == 0]
    F_eq = [r for r in rows if r["target_F_slack"] == 0]
    # families where Frankl true-abundance is exactly 1/2 (tight)
    tight_L = [r for r in rows if abs(r["true_abund_L"] - 0.5) < 1e-12]
    tight_F = [r for r in rows if abs(r["true_abund_F"] - 0.5) < 1e-12]

    # min power-mean density (the lever's achieved value)
    min_pm_L = min((r["pm_density_L"] for r in rows), default=0.0)
    min_pm_F = min((r["pm_density_F"] for r in rows), default=0.0)

    # Among Frankl-tight families, does TARGET hold with equality?
    tightL_targetL_eq = all(r["target_L_slack"] == 0 for r in tight_L)
    tightF_targetF_eq = all(r["target_F_slack"] == 0 for r in tight_F)

    # the JI structured bound: is JIOVL >= JIOVL_lb always (sanity), and does
    # JIOVL_lb feed anything? report range of JIOVL/JIOVL_lb
    lines = []
    def p(s=""):
        lines.append(s)

    p(f"# JI-overlap <-> abundance identity & the target overlap inequality")
    p(f"# families (|F|>=2, n<=" + str(nmax) + f"): {total}")
    p(f"# per-n counts: {per_n}")
    p(f"# elapsed {dt:.1f}s")
    p()
    p("IDENTITY  P2 = Sum_x|Fib(x)|^2 = Sum_{A,B in L}|A cap B| = OVL :"
      f"  0 violations / {total}  (asserted exact)")
    p()
    p("TARGET-L:  2*OVL >= |L| * Sum_A|A|   (sufficient for max|Fib| >= |L|/2)")
    p(f"  holds on {total - len(L_fail)} / {total};  FAILS on {len(L_fail)}")
    p(f"  TARGET-L equality (slack==0) families: {len(L_eq)}")
    p()
    p("TARGET-F:  2*OVL >= |F| * Sum_A|A|   (sufficient for abundance >= |F|/2)")
    p(f"  holds on {total - len(F_fail)} / {total};  FAILS on {len(F_fail)}")
    p(f"  TARGET-F equality (slack==0) families: {len(F_eq)}")
    p()
    p("CUBE TIGHTNESS (the unique extremizer must satisfy with EQUALITY):")
    p(f"  cube families found: {len(cubes)}  (n=0..{nmax})")
    p(f"  cube TARGET-L slacks (2*OVL-|L|*P1): {cube_L_slack}")
    p(f"  cube TARGET-F slacks (2*OVL-|F|*P1): {cube_F_slack}")
    p()
    p("POWER-MEAN lever achieved value (min over families):")
    p(f"  min P2/(P1*|L|)  = {min_pm_L:.6f}   (need >= 0.5 for Frankl-L)")
    p(f"  min P2/(P1*|F|)  = {min_pm_F:.6f}   (need >= 0.5 for Frankl-F)")
    p()
    p("DECOUPLING CHECK (does the lever touch the Frankl-tight families?):")
    p(f"  abundance-1/2 families (L-norm): {len(tight_L)};"
      f"  all satisfy TARGET-L with equality? {tightL_targetL_eq}")
    p(f"  abundance-1/2 families (F-norm): {len(tight_F)};"
      f"  all satisfy TARGET-F with equality? {tightF_targetF_eq}")
    p()
    if L_fail:
        p("TARGET-L COUNTEREXAMPLES (worst slack first):")
        for r in sorted(L_fail, key=lambda r: r["target_L_slack"])[:12]:
            p(f"  n={r['n']} |F|={r['mF']} |L|={r['mL']} "
              f"abund_L={r['true_abund_L']:.4f} abund_F={r['true_abund_F']:.4f} "
              f"pmL={r['pm_density_L']:.4f} slackL={r['target_L_slack']} "
              f"F={r['family']}")
        p()
    if F_fail:
        p("TARGET-F COUNTEREXAMPLES (worst slack first):")
        for r in sorted(F_fail, key=lambda r: r["target_F_slack"])[:12]:
            p(f"  n={r['n']} |F|={r['mF']} |L|={r['mL']} "
              f"abund_F={r['true_abund_F']:.4f} pmF={r['pm_density_F']:.4f} "
              f"slackF={r['target_F_slack']} F={r['family']}")
        p()

    out = "\n".join(lines)
    with open("data/overlap_summary.txt", "w") as fh:
        fh.write(out + "\n")
    print(out)

    js = {
        "total": total, "per_n": per_n,
        "target_L_fail": len(L_fail), "target_F_fail": len(F_fail),
        "target_L_eq": len(L_eq), "target_F_eq": len(F_eq),
        "cube_L_slack": cube_L_slack, "cube_F_slack": cube_F_slack,
        "min_pm_L": min_pm_L, "min_pm_F": min_pm_F,
        "tightL_targetL_eq": tightL_targetL_eq,
        "tightF_targetF_eq": tightF_targetF_eq,
        "n_tight_L": len(tight_L), "n_tight_F": len(tight_F),
        "L_fail_examples": [r["family"] for r in
                            sorted(L_fail, key=lambda r: r["target_L_slack"])[:20]],
        "F_fail_examples": [r["family"] for r in
                            sorted(F_fail, key=lambda r: r["target_F_slack"])[:20]],
    }
    with open("data/overlap_summary.json", "w") as fh:
        json.dump(js, fh, indent=2)


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    run(nmax)
