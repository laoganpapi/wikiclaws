"""
second_moment.py — Second-moment / variance valid-inequality probe on Frankl's
union-closed conjecture.

Author: Alex Ye (no AI on author line).
[NOVELTY UNVERIFIED — second-moment / Reimer-on-pairs framings of Frankl very
likely exist in the literature (Reimer 2003, Kleitman-style correlation); arXiv
inaccessible this session. Every "new" framing flagged in second_moment.md.]

----------------------------------------------------------------------------------
THE LEVER (from lp_duality.md §6).
----------------------------------------------------------------------------------

For a union-closed F (m = |F| members, ground set [n]):
  freq_i = |{A in F : i in A}|,   ab_i = freq_i / m.

First moment (exact averaging identity):
  M1 := sum_i freq_i = sum_{A in F} |A| = m * sum_i ab_i.

Second moment:
  M2 := sum_i freq_i^2.

KEY COMBINATORIAL IDENTITY (task a). Counting ordered triples (i, A, B) with
i in A and i in B:
  M2 = sum_i freq_i^2 = sum_i |{A : i in A}| * |{B : i in B}|
     = #{(i, A, B) : i in A, i in B}
     = sum_{(A,B) in F x F} |A ∩ B|.
So the second moment equals the TOTAL PAIRWISE-INTERSECTION SIZE over F x F.

Inclusion-exclusion |A ∩ B| = |A| + |B| - |A ∪ B| gives
  M2 = sum_{A,B} (|A| + |B| - |A ∪ B|)
     = 2 m * sum_A |A|  -  sum_{A,B} |A ∪ B|       (since sum_{A,B}|A| = m sum_A|A|)
     = 2 m * M1  -  U,
where  U := sum_{(A,B) in F x F} |A ∪ B|.

Union-closure enters HERE: A ∪ B in F for all A, B. Writing r(C) = #{(A,B) in F x F :
A ∪ B = C} (the "join multiplicity"), we have sum_C r(C) = m^2 and
  U = sum_{C in F} |C| * r(C).
Union-closure forces r(C) >= 1 for every C in F (take A = B = C), and more.

The power-mean ("weighted-by-itself") bound (the reason a LOWER bound on M2 matters):
  max_i ab_i  >=  (sum_i ab_i^2) / (sum_i ab_i)  =  M2 / (m * M1).
A LOWER bound M2 >= g(m, n) would push max-abundance up.

----------------------------------------------------------------------------------
WHAT THIS SCRIPT DOES
----------------------------------------------------------------------------------
For all UC families with |F| >= 2, n <= 5 (orbit reps), compute
  m, n, M1, M2, avg_set_size, U, the power-mean ratio M2/(m*M1), true abundance,
  the join-multiplicities r(C) (min, and the "diagonal lower bound" sum_C |C|),
and test:
  (b) the strongest closed-form lower bound g(m,n) on M2 holding on ALL families;
  (c) whether the Boolean cube minimizes the power-mean ratio M2/(m*M1);
  (d) the multiplicity r(C) sub-direction (is r(C) >= something useful?).

Outputs:
  data/secmom_n{0..5}.jsonl   — per-family rows
  data/secmom_summary.txt     — human-readable summary
  data/secmom_run.txt         — full run log
"""

from __future__ import annotations

import json
import math
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from uc_family import Family, frequencies, abundance, ground_set  # noqa: E402
from enumerate import all_uc_families  # noqa: E402

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def popcount(m: int) -> int:
    return bin(m).count("1")


def family_stats(F: Family, n: int) -> dict:
    """Compute all second-moment quantities for one UC family F on ground set [n]."""
    members = list(F)
    m = len(members)
    freqs = frequencies(F, n)

    M1 = sum(freqs)                      # = sum_A |A|
    M2 = sum(f * f for f in freqs)       # = sum_{A,B} |A ∩ B|
    avg_set_size = M1 / m
    sum_ab = M1 / m                      # = sum_i ab_i
    sum_ab2 = M2 / (m * m)               # = sum_i ab_i^2

    # Union term U = sum_{A,B} |A ∪ B|, and join multiplicities r(C).
    rC: dict[int, int] = defaultdict(int)
    U = 0
    for a in members:
        for b in members:
            c = a | b
            U += popcount(c)
            rC[c] += 1
    # identity check: M2 == 2*m*M1 - U
    M2_from_U = 2 * m * M1 - U

    # power-mean ratio = M2 / (m * M1) = sum_i ab_i^2 / sum_i ab_i  (if M1 > 0)
    if M1 > 0:
        power_mean = M2 / (m * M1)
    else:
        power_mean = 0.0

    true_ab = abundance(F)

    # multiplicity statistics
    r_values = [rC[c] for c in members]    # r(C) for C in F (every C in F is a join)
    r_min = min(r_values) if r_values else 0
    # diagonal lower bound on U: each C in F contributes >= |C| (A=B=C), and there
    # are m such diagonal pairs; more strongly U >= sum_C |C| * r(C) with r(C)>=1.
    # Reverse: an UPPER bound on U gives a LOWER bound on M2.
    # Trivial upper bound: |A ∪ B| <= n  =>  U <= n*m^2  =>  M2 >= 2 m M1 - n m^2.
    M2_lb_trivial_union = 2 * m * M1 - n * m * m

    # number of ground elements actually used (freq>0)
    n_active = sum(1 for f in freqs if f > 0)

    return {
        "n": n,
        "m": m,
        "freqs_sorted": sorted(freqs),
        "M1": M1,
        "M2": M2,
        "M2_from_U_check": M2_from_U,
        "U": U,
        "avg_set_size": avg_set_size,
        "sum_ab": sum_ab,
        "sum_ab2": sum_ab2,
        "power_mean_ratio": power_mean,
        "true_abundance": true_ab,
        "r_min_over_F": r_min,
        "n_active": n_active,
        "M2_lb_trivial_union": M2_lb_trivial_union,
    }


# Candidate closed-form lower bounds g(m, n) for M2 = sum_i freq_i^2.
# Each is a function (m, n, M1, ...) -> value; we test M2 >= candidate on ALL families.
def candidate_bounds(s: dict) -> dict:
    m = s["m"]
    n = s["n"]
    M1 = s["M1"]
    n_active = s["n_active"]
    cands = {}
    # (1) Cauchy-Schwarz over ACTIVE coordinates: M2 >= M1^2 / n_active.
    #     This is the raw power-mean identity, NOT a union-closure input.
    cands["cauchy_schwarz_active"] = (M1 * M1) / n_active if n_active > 0 else 0.0
    # (2) Cauchy-Schwarz over ALL n coordinates: M2 >= M1^2 / n.
    cands["cauchy_schwarz_all_n"] = (M1 * M1) / n if n > 0 else 0.0
    # (3) Trivial-union lower bound (union-closure-free, uses |A∪B|<=n): 2mM1 - n m^2.
    cands["trivial_union"] = 2 * m * M1 - n * m * m
    # (4) Diagonal contribution alone: the diagonal pairs A=B give sum_A |A|^2 to M2's
    #     "intersection" reading: sum_{A=B}|A∩B| = sum_A |A|. That's only M1; the
    #     interesting content is off-diagonal. Record sum_A|A| = M1 as a floor
    #     (M2 >= M1 always, since freq_i^2 >= freq_i for integer freq_i).
    cands["int_floor_M1"] = M1
    return cands


def boolean_cube_reference(k: int) -> dict:
    """Exact second-moment quantities for the Boolean cube 2^[k]."""
    m = 2 ** k
    freqs = [2 ** (k - 1)] * k
    M1 = sum(freqs)                       # k * 2^(k-1)
    M2 = sum(f * f for f in freqs)        # k * 4^(k-1)
    power_mean = M2 / (m * M1) if M1 > 0 else 0.0
    return {
        "k": k, "m": m, "n": k, "M1": M1, "M2": M2,
        "power_mean_ratio": power_mean,
        "true_abundance": 0.5,
    }


def sweep(max_n: int = 5):
    log_lines = []

    def log(s: str = ""):
        print(s)
        log_lines.append(s)

    log("=" * 78)
    log("SECOND-MOMENT / VARIANCE VALID-INEQUALITY PROBE (Frankl UCC)")
    log("Author: Alex Ye.  [NOVELTY UNVERIFIED]")
    log("=" * 78)

    # --- (c) cube reference table -----------------------------------------
    log("\n(c) BOOLEAN CUBE 2^[k] REFERENCE  (freq_i = 2^{k-1}, M2 = k*4^{k-1}):")
    log(f"{'k':>3} {'m=2^k':>7} {'M1':>8} {'M2':>10} {'power_mean=M2/(mM1)':>20} {'abund':>7}")
    for k in range(1, 8):
        c = boolean_cube_reference(k)
        log(f"{c['k']:>3} {c['m']:>7} {c['M1']:>8} {c['M2']:>10} "
            f"{c['power_mean_ratio']:>20.10f} {c['true_abundance']:>7.4f}")
    log("  => cube power-mean ratio = (k*4^{k-1})/(2^k * k*2^{k-1}) = "
        "4^{k-1}/(2^k * 2^{k-1}) = 4^{k-1}/4^... = 1/2 EXACTLY for every k.")

    # --- sweep over all UC families ---------------------------------------
    overall = {
        "n_families": 0,
        "identity_violations": 0,          # M2 == 2mM1 - U
        "powermean_below_half": [],        # families with M2/(mM1) < 1/2
        "min_power_mean": (None, 2.0),     # (row, value)
        "candidate_violations": defaultdict(int),
        "candidate_min_slack": {},         # candidate -> min (M2 - cand)
        "r_min_global": None,              # min over all C in F of r(C)
        "powermean_ratio_min_by_iso": 2.0,
    }

    for n in range(0, max_n + 1):
        rows = []
        for F in all_uc_families(n):
            if len(F) < 2:
                continue
            # restrict to families whose ground set is [n] genuinely; ground_set
            # gives the active span; we keep n as the nominal ground size (matches
            # the other sweeps which use the family's own active n). Use active n.
            gn = ground_set(F)
            if gn == 0:
                continue
            s = family_stats(F, gn)
            rows.append(s)

            overall["n_families"] += 1

            # identity check
            if s["M2"] != s["M2_from_U_check"]:
                overall["identity_violations"] += 1

            pm = s["power_mean_ratio"]
            if pm < overall["min_power_mean"][1]:
                overall["min_power_mean"] = (s, pm)
            if pm < 0.5 - 1e-12:
                overall["powermean_below_half"].append((s["freqs_sorted"], s["m"],
                                                         s["n"], round(pm, 6),
                                                         round(s["true_abundance"], 6)))

            # candidate bounds
            cands = candidate_bounds(s)
            for name, val in cands.items():
                slack = s["M2"] - val
                if slack < -1e-9:
                    overall["candidate_violations"][name] += 1
                prev = overall["candidate_min_slack"].get(name)
                if prev is None or slack < prev[0]:
                    overall["candidate_min_slack"][name] = (slack, s["freqs_sorted"],
                                                            s["m"], s["n"])

            # multiplicity
            rmn = s["r_min_over_F"]
            if overall["r_min_global"] is None or rmn < overall["r_min_global"]:
                overall["r_min_global"] = rmn

        # write jsonl
        out_path = os.path.join(DATA_DIR, f"secmom_n{n}.jsonl")
        with open(out_path, "w") as fh:
            for s in rows:
                fh.write(json.dumps(s) + "\n")
        log(f"\n n={n}: {len(rows)} UC families (|F|>=2) -> {out_path}")

    # --- (a) identity verdict ---------------------------------------------
    log("\n" + "=" * 78)
    log("(a) IDENTITY  M2 = sum_i freq_i^2 = sum_{A,B}|A∩B| = 2 m M1 - U")
    log(f"    checked on {overall['n_families']} families; "
        f"violations = {overall['identity_violations']}")

    # --- (b) strongest lower bound ----------------------------------------
    log("\n" + "=" * 78)
    log("(b) CANDIDATE LOWER BOUNDS  M2 >= g(m,n):  violations / min slack")
    for name in sorted(overall["candidate_min_slack"]):
        v = overall["candidate_violations"][name]
        slack, fv, m, nn = overall["candidate_min_slack"][name]
        log(f"  {name:>22}: violations={v:>5}   min_slack={slack:>12.4f}  "
            f"(at freqs={fv}, m={m}, n={nn})")
    log("  NOTE: a bound is VALID iff violations==0. Cauchy-Schwarz over active")
    log("        coords is the raw identity (no union-closure); 'trivial_union' is")
    log("        the only one that USES union-closure (via |A∪B|<=n) -- check below.")

    # --- (c) power-mean ratio minimizer -----------------------------------
    log("\n" + "=" * 78)
    log("(c) POWER-MEAN RATIO  M2/(m*M1) = (sum ab^2)/(sum ab):")
    srow, sval = overall["min_power_mean"]
    log(f"    GLOBAL MIN ratio over all UC families n<=5 = {sval:.6f}")
    log(f"      at freqs={srow['freqs_sorted']}, m={srow['m']}, n={srow['n']}, "
        f"abund={srow['true_abundance']:.4f}")
    log(f"    cube ratio = 0.5 exactly. Is cube the MINIMIZER? "
        f"{'NO' if sval < 0.5 - 1e-9 else 'YES (=0.5 is the floor)'}")
    log(f"    families with power-mean ratio < 1/2: "
        f"{len(overall['powermean_below_half'])}")
    for row in sorted(overall["powermean_below_half"], key=lambda x: x[3])[:12]:
        log(f"      freqs={row[0]} m={row[1]} n={row[2]} ratio={row[3]} "
            f"true_abund={row[4]}")

    # --- (d) multiplicity -------------------------------------------------
    log("\n" + "=" * 78)
    log("(d) JOIN-MULTIPLICITY r(C)=#{(A,B):A∪B=C}:")
    log(f"    min over all C in F over all families = {overall['r_min_global']}")
    log("    (union-closure gives r(C)>=1 for every C in F via A=B=C; the question")
    log("     is whether a larger structural lower bound on r(C) bounds U from ABOVE,")
    log("     hence M2 from BELOW. See secmom_summary.txt / second_moment.md.)")

    # --- write summary ----------------------------------------------------
    summary_path = os.path.join(DATA_DIR, "secmom_summary.txt")
    with open(summary_path, "w") as fh:
        fh.write("\n".join(log_lines) + "\n")
    run_path = os.path.join(DATA_DIR, "secmom_run.txt")
    with open(run_path, "w") as fh:
        fh.write("\n".join(log_lines) + "\n")

    log(f"\nWrote {summary_path} and {run_path}")
    return overall


if __name__ == "__main__":
    mn = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    sweep(mn)
