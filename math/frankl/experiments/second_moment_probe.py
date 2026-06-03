"""
second_moment_probe.py — deeper probes for the union-term U and multiplicity r(C).

Author: Alex Ye (no AI on author line). [NOVELTY UNVERIFIED]

Questions:
 (P1) Does union-closure force U = sum_{A,B}|A∪B| to be SMALLER than a generic
      family with the same (m, M1), thereby forcing M2 = 2mM1 - U LARGER?
      We compare U(F) against the generic baseline and against the cube.
 (P2) Is the power-mean ratio M2/(m M1) minimized by the cube AMONG families
      with the same true abundance? (If the dip below 1/2 only happens at
      abundance > 1/2, the lever never threatens Frankl.)
 (P3) Multiplicity r(C): is there a structural lower bound r(C) >= f(...) beyond
      r(C) >= 1?  In particular is the bottom element ∅ (if present) always
      r(∅)=1, and does the TOP element T=∪F have large r(T)?
 (P4) The decisive test: among ALL families with the SAME m (=|F|), what is the
      MINIMUM of M2?  Is the cube (when m=2^k) the minimizer of M2 for its m,
      or do other families go lower?
"""

from __future__ import annotations

import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from uc_family import Family, frequencies, abundance, ground_set  # noqa: E402
from enumerate import all_uc_families  # noqa: E402


def popcount(m: int) -> int:
    return bin(m).count("1")


def stats(F: Family, n: int):
    members = list(F)
    m = len(members)
    freqs = frequencies(F, n)
    M1 = sum(freqs)
    M2 = sum(f * f for f in freqs)
    U = 0
    rC = defaultdict(int)
    for a in members:
        for b in members:
            c = a | b
            U += popcount(c)
            rC[c] += 1
    has_empty = (0 in F)
    top = 0
    for a in members:
        top |= a
    return {
        "m": m, "n": n, "M1": M1, "M2": M2, "U": U,
        "abund": abundance(F),
        "pm": M2 / (m * M1) if M1 else 0.0,
        "r_empty": rC[0] if has_empty else None,
        "r_top": rC[top],
        "has_empty": has_empty,
        "freqs": sorted(freqs),
    }


def main(max_n=5):
    # collect, bucket by m, and by (rounded abundance)
    by_m_min_pm = {}        # m -> (min pm, row)
    by_m_min_M2 = {}        # m -> (min M2, row)
    pm_below_half = []
    # check: for families with abundance EXACTLY 0.5, is pm always >= 0.5?
    abund_half_pm = []      # list of pm for families with abundance==0.5
    # r(top) statistics
    r_top_eq_1 = 0
    r_top_total = 0
    # does pm < 0.5 ever co-occur with abundance == 0.5?  (the dangerous case)
    danger = []

    n_fam = 0
    for n in range(0, max_n + 1):
        for F in all_uc_families(n):
            if len(F) < 2:
                continue
            gn = ground_set(F)
            if gn == 0:
                continue
            s = stats(F, gn)
            n_fam += 1
            m = s["m"]
            if m not in by_m_min_pm or s["pm"] < by_m_min_pm[m][0]:
                by_m_min_pm[m] = (s["pm"], s)
            if m not in by_m_min_M2 or s["M2"] < by_m_min_M2[m][0]:
                by_m_min_M2[m] = (s["M2"], s)
            if s["pm"] < 0.5 - 1e-12:
                pm_below_half.append(s)
            if abs(s["abund"] - 0.5) < 1e-12:
                abund_half_pm.append(s["pm"])
                if s["pm"] < 0.5 - 1e-12:
                    danger.append(s)
            r_top_total += 1
            if s["r_top"] == 1:
                r_top_eq_1 += 1

    print("=" * 78)
    print(f"SECOND-MOMENT DEEP PROBE   ({n_fam} UC families |F|>=2, n<=5)")
    print("=" * 78)

    print("\n(P2/decisive) Among families with TRUE ABUNDANCE EXACTLY 1/2,")
    print(f"   number = {len(abund_half_pm)}")
    if abund_half_pm:
        print(f"   min power-mean ratio = {min(abund_half_pm):.6f}")
        print(f"   max power-mean ratio = {max(abund_half_pm):.6f}")
    print(f"   families with abundance==1/2 AND power-mean < 1/2: {len(danger)}")
    print("   => if 0, the power-mean ratio NEVER drops below 1/2 on the Frankl-")
    print("      tight families; the sub-1/2 dips all have abundance strictly > 1/2,")
    print("      so the lever's failure is HARMLESS (it never threatens a true")
    print("      counterexample) but also USELESS (cube pins it, others undercut).")

    print("\n(P4) MIN of M2 = sum freq^2 for each m=|F| (is the cube minimal at m=2^k?):")
    print(f"   {'m':>4} {'min M2':>8} {'cube M2 (if m=2^k)':>18} {'argmin freqs':>22} {'argmin pm':>10}")
    cubes = {2 ** k: k * 4 ** (k - 1) for k in range(1, 6)}
    for m in sorted(by_m_min_M2):
        mn_M2, row = by_m_min_M2[m]
        cube_M2 = cubes.get(m, None)
        cube_str = str(cube_M2) if cube_M2 is not None else "-"
        flag = ""
        if cube_M2 is not None:
            if mn_M2 < cube_M2:
                flag = "  <-- cube NOT min M2"
            elif mn_M2 == cube_M2:
                flag = "  <-- cube IS min M2"
        print(f"   {m:>4} {mn_M2:>8} {cube_str:>18} {str(row['freqs']):>22} "
              f"{by_m_min_pm[m][0]:>10.5f}{flag}")

    print("\n(P3) MULTIPLICITY r(top): r(top)=1 on "
          f"{r_top_eq_1}/{r_top_total} families.")
    print("   (r(top) > 1 means several pairs join to the top; r(top)=1 iff the top")
    print("    is join-irreducible as a pair-join, i.e. only (T,T) maps to T.)")

    print("\n(P1) UNION-TERM lower bound on M2 from r(C)>=1:")
    print("   U = sum_C |C| r(C), sum_C r(C)=m^2, r(C)>=1 for C in F.")
    print("   To LOWER-bound M2 = 2mM1 - U we need an UPPER bound on U.")
    print("   Generic upper bound |A∪B|<=max(|A|,|B|,...)<=max_set_size; the")
    print("   tightest m-free bound is |A∪B|<=|T|=size of top. Then U<=|T|*m^2 and")
    print("   M2 >= 2mM1 - |T| m^2.  Test whether THIS (a union-closure-aware bound,")
    print("   since T=∪F in F) beats Cauchy-Schwarz M2>=M1^2/n_active:")

    # test M2 >= 2mM1 - |T|*m^2 vs M2 >= M1^2/n_active, count which is tighter / valid
    viol_top = 0
    top_tighter = 0
    cs_tighter = 0
    for n in range(0, max_n + 1):
        for F in all_uc_families(n):
            if len(F) < 2:
                continue
            gn = ground_set(F)
            if gn == 0:
                continue
            members = list(F)
            m = len(members)
            freqs = frequencies(F, gn)
            M1 = sum(freqs)
            M2 = sum(f * f for f in freqs)
            top = 0
            for a in members:
                top |= a
            tsz = popcount(top)
            n_active = sum(1 for f in freqs if f > 0)
            top_bound = 2 * m * M1 - tsz * m * m
            cs_bound = (M1 * M1) / n_active if n_active else 0.0
            if M2 < top_bound - 1e-9:
                viol_top += 1
            if top_bound > cs_bound + 1e-9:
                top_tighter += 1
            elif cs_bound > top_bound + 1e-9:
                cs_tighter += 1
    print(f"   M2 >= 2mM1 - |T|m^2 : violations = {viol_top}")
    print(f"     it is STRICTLY tighter than Cauchy-Schwarz on {top_tighter} families,")
    print(f"     Cauchy-Schwarz strictly tighter on {cs_tighter} families.")
    print("   (If the top-bound is essentially never tighter, union-closure adds")
    print("    nothing beyond Cauchy-Schwarz for the second moment.)")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
