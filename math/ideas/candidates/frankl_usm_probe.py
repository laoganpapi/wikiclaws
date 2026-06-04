"""
frankl_usm_probe.py -- Foundational computational probe for the surviving Frankl
                       candidate: JI-overlap / max-vs-mean spread restricted to
                       the upper-semimodular (USM) class of lattices.

Author: Alex Ye (no AI on author line).   [NOVELTY UNVERIFIED]

--------------------------------------------------------------------------------
WHAT THIS DECIDES
--------------------------------------------------------------------------------
The "cone-blocked-class" research program (`frankl_candidate.md`, §A) asserts:

  (P1) the 6 parasite families that defeat the JI-overlap / power-mean lever on
       the full UC census ARE STRUCTURALLY EXCLUDED from the upper-semimodular
       class, because the cone construction (which produces them) typically
       breaks upper-semimodularity (Reinhold's lower-semimodular case dualised);
  (P2) consequently the JI-overlap inequality
            2 * OVL(L) >= |F| * P1(L)
       (equivalently: power-mean density P2/P1/|F| >= 1/2) holds with strict
       slack on every USM family, with the cube unique tight extremiser;
  (P3) so a restricted Frankl program "USM => JI-overlap" is the live target.

THIS PROBE RUNS THE FOUNDATIONAL CHECK (P1) DIRECTLY ON THE FULL n<=5 UC CENSUS
AND THEN, IF (P1) HOLDS, THE FALSIFIER FOR (P2).

It reads only from frankl/experiments/ (the canonical UC enumeration + lattice
module) and writes data under ideas/candidates/data/.  No mutation outside
ideas/candidates/.

--------------------------------------------------------------------------------
OUTPUT
--------------------------------------------------------------------------------
ideas/candidates/data/usm_probe.json contains:

  parasite_check         the 6 named parasite families and their semimodularity
                         flags (the foundational check; should be USM=False if
                         the program premise holds)

  usm_census             |L|, abundance, P1, P2, power-mean density, true
                         abundance, JI-overlap inequality LHS-RHS for EVERY
                         USM family at n <= 5

  class_minima           min power-mean density (the JI-overlap lever value)
                         over the distributive, modular, LSM, USM, and full
                         classes -- so we can see whether USM truly carves away
                         the parasite, or whether the parasite mechanism
                         survives every restricted class

  falsifier_result       precise YES/NO: is there a USM family with true
                         abundance > 1/2 AND JI-overlap LHS-RHS < 0?
                         (yes => the surviving candidate ALSO dies; report it
                          no  => the candidate survives the foundational test,
                                 list strictness slack distribution)

--------------------------------------------------------------------------------
HONEST FRAMING
--------------------------------------------------------------------------------
This is a *foundational verification*, not a proof attempt.  If the parasites
DO sit inside USM, the program is dead before it starts and we report that
loudly: another "the restricted class doesn't help" negative.  If the parasites
are excluded, this probe still does NOT prove anything for n > 5; it only
upgrades the candidate from "guess" to "consistent with all n<=5 data".
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data"
DATA_DIR.mkdir(exist_ok=True)

# Read-only imports from frankl/experiments
FRANKL_EXP = HERE.parent.parent / "frankl" / "experiments"
sys.path.insert(0, str(FRANKL_EXP))

from enumerate import all_uc_families  # noqa: E402
from lattice import invariants  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def ground_size(F):
    if not F:
        return 0
    u = 0
    for m in F:
        u |= m
    return u.bit_length()


def abundance(F):
    n = ground_size(F)
    if not F or n == 0:
        return 0.0
    counts = [0] * n
    for m in F:
        for i in range(n):
            if m & (1 << i):
                counts[i] += 1
    return max(counts) / len(F)


def overlap_stats(F):
    """Return (P1, P2, OVL_minus_half_F_times_P1, power_mean_density)."""
    F_list = list(F)
    P1 = sum(bin(m).count("1") for m in F_list)
    # OVL = sum_{A,B in F} |A cap B|  (= P2 by the fibre identity)
    OVL = sum(bin(a & b).count("1") for a in F_list for b in F_list)
    P2 = OVL  # identity 1.1 of ji_overlap_inequality.md
    # Target-F lever: 2*OVL >= |F| * P1  <=>  power_mean / |F| >= 1/2
    lhs_minus_rhs = 2 * OVL - len(F_list) * P1
    pm_density = (P2 / P1) / len(F_list) if P1 else 0.0
    return P1, P2, lhs_minus_rhs, pm_density


# ---------------------------------------------------------------------------
# The 6 named parasite families (overlap_counterexamples.txt)
# ---------------------------------------------------------------------------

PARASITES = [
    # (name, n, masks)
    ("n5_F3a_minimal", 5, [0, 16, 31]),
    ("n4_F3",          4, [0, 8, 15]),
    ("n5_F3b",         5, [0, 16, 23]),
    ("n5_F5",          5, [0, 8, 16, 24, 31]),
    ("n5_F6",          5, [0, 8, 16, 23, 24, 31]),
    ("n5_F7",          5, [0, 8, 15, 16, 23, 24, 31]),
]


def parasite_check():
    """Foundational check: are the 6 parasites all NON-upper-semimodular?

    The candidate program REQUIRES this to be YES.  We report the actual flags
    honestly; if any parasite is USM, the program premise is FALSE.
    """
    rows = []
    n_usm = 0
    for name, n, masks in PARASITES:
        F = frozenset(masks)
        inv = invariants(F)
        ab = abundance(F)
        P1, P2, slack, pm = overlap_stats(F)
        row = {
            "name": name,
            "n": n,
            "masks": sorted(masks),
            "abs_size_F": len(F),
            "abs_size_L": inv.n_L,
            "true_abundance": ab,
            "power_mean_density": pm,
            "target_LHS_minus_RHS": slack,
            "distributive": inv.distributive,
            "modular": inv.modular,
            "lower_semimodular": inv.lower_semimodular,
            "upper_semimodular": inv.upper_semimodular,
        }
        rows.append(row)
        if inv.upper_semimodular:
            n_usm += 1
    return {
        "rows": rows,
        "n_parasites": len(PARASITES),
        "n_parasites_that_are_USM": n_usm,
        "premise_holds": n_usm == 0,
        "premise_text": (
            "Program premise: all 6 parasite families are NON-upper-semimodular. "
            "If any parasite is USM, the cone-blocked-class candidate is "
            "structurally false: USM does NOT exclude the parasite mechanism."
        ),
    }


# ---------------------------------------------------------------------------
# Census sweep: every UC family at n<=5, tabulate by class
# ---------------------------------------------------------------------------

def census_sweep(max_n=5):
    """Walk the canonical n<=5 enumeration; per family, record class flags +
    abundance + power-mean density + target inequality slack."""
    by_class = {
        "all": {"count": 0, "min_pm": 1.0, "worst": None,
                "n_target_F_fail": 0, "n_above_half_target_fail": 0,
                "n_at_half": 0},
        "distributive": {"count": 0, "min_pm": 1.0, "worst": None,
                          "n_target_F_fail": 0, "n_above_half_target_fail": 0,
                          "n_at_half": 0},
        "modular": {"count": 0, "min_pm": 1.0, "worst": None,
                     "n_target_F_fail": 0, "n_above_half_target_fail": 0,
                     "n_at_half": 0},
        "lower_semimodular": {"count": 0, "min_pm": 1.0, "worst": None,
                               "n_target_F_fail": 0, "n_above_half_target_fail": 0,
                               "n_at_half": 0},
        "upper_semimodular": {"count": 0, "min_pm": 1.0, "worst": None,
                               "n_target_F_fail": 0, "n_above_half_target_fail": 0,
                               "n_at_half": 0},
    }

    # Slack distribution on the USM class -- the candidate's home.
    usm_slacks = []
    # Tightest USM cases
    usm_at_half_families = []
    # Falsifier candidates: USM with true abundance > 1/2 yet target_LHS_minus_RHS < 0
    falsifier_witnesses = []

    total = 0
    for n in range(max_n + 1):
        for F in all_uc_families(n, dedupe_isomorphic=True):
            if len(F) < 2:
                continue
            inv = invariants(F)
            ab = abundance(F)
            P1, P2, slack_target, pm = overlap_stats(F)
            total += 1

            def update(key, flag):
                if not flag:
                    return
                d = by_class[key]
                d["count"] += 1
                if pm < d["min_pm"]:
                    d["min_pm"] = pm
                    d["worst"] = {
                        "n": n, "masks": sorted(F), "true_abundance": ab,
                        "power_mean_density": pm,
                        "target_LHS_minus_RHS": slack_target,
                    }
                if slack_target < 0:
                    d["n_target_F_fail"] += 1
                    if ab > 0.5 + 1e-12:
                        d["n_above_half_target_fail"] += 1
                if abs(ab - 0.5) < 1e-12:
                    d["n_at_half"] += 1

            update("all", True)
            update("distributive", inv.distributive)
            update("modular", inv.modular)
            update("lower_semimodular", inv.lower_semimodular)
            update("upper_semimodular", inv.upper_semimodular)

            if inv.upper_semimodular:
                usm_slacks.append({
                    "n": n, "masks": sorted(F), "abundance": ab,
                    "pm_density": pm, "target_slack": slack_target,
                    "distributive": inv.distributive,
                    "modular": inv.modular,
                })
                if abs(ab - 0.5) < 1e-12:
                    usm_at_half_families.append({
                        "n": n, "masks": sorted(F),
                        "distributive": inv.distributive,
                        "|L|": inv.n_L,
                        "height": inv.height,
                        "width": inv.width,
                    })
                if slack_target < 0 and ab > 0.5 + 1e-12:
                    falsifier_witnesses.append({
                        "n": n, "masks": sorted(F),
                        "true_abundance": ab,
                        "pm_density": pm,
                        "target_slack": slack_target,
                        "distributive": inv.distributive,
                        "modular": inv.modular,
                    })

    # Strict slack distribution on USM (target_slack >= 0 is the lever holding;
    # > 0 strict).
    n_strict = sum(1 for s in usm_slacks if s["target_slack"] > 0)
    n_eq     = sum(1 for s in usm_slacks if s["target_slack"] == 0)
    n_fail   = sum(1 for s in usm_slacks if s["target_slack"] < 0)

    return {
        "total_families": total,
        "by_class": by_class,
        "usm_target_F_strict_count": n_strict,
        "usm_target_F_equality_count": n_eq,
        "usm_target_F_failure_count": n_fail,
        "usm_at_half_families": usm_at_half_families,
        "usm_at_half_count": len(usm_at_half_families),
        "falsifier_witnesses": falsifier_witnesses,
        "n_falsifier_witnesses": len(falsifier_witnesses),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(max_n=5, out_path=None):
    print(f"[usm_probe] Walking UC census n<={max_n}...")
    pc = parasite_check()
    print()
    print("=== PARASITE CHECK (the program's foundational premise) ===")
    print(f"  premise (all parasites NON-USM): {pc['premise_holds']}")
    print(f"  parasites that ARE USM:          {pc['n_parasites_that_are_USM']}/{pc['n_parasites']}")
    for r in pc["rows"]:
        flags = []
        if r["distributive"]:      flags.append("dist")
        if r["modular"]:           flags.append("mod")
        if r["lower_semimodular"]: flags.append("lsm")
        if r["upper_semimodular"]: flags.append("USM")
        print(f"  {r['name']:<20s} ab={r['true_abundance']:.4f} pm={r['power_mean_density']:.4f} "
              f"slack={r['target_LHS_minus_RHS']:>3d} flags={','.join(flags)}")

    sweep = census_sweep(max_n=max_n)
    print()
    print("=== CLASS MINIMA OF JI-OVERLAP POWER-MEAN DENSITY (target lever) ===")
    print("  (the lever holds <=> pm density >= 1/2)")
    for cls_name, d in sweep["by_class"].items():
        worst = d["worst"]
        wstr = (f"worst: ab={worst['true_abundance']:.4f}, pm={worst['power_mean_density']:.4f}, "
                f"slack={worst['target_LHS_minus_RHS']}, F={worst['masks']}") if worst else "-"
        print(f"  {cls_name:<20s} count={d['count']:<6d} min_pm={d['min_pm']:.4f}  "
              f"target_F_fails={d['n_target_F_fail']:<3d}  at_half={d['n_at_half']:<3d}")
        print(f"    {wstr}")

    print()
    print("=== USM CLASS BREAKDOWN ===")
    print(f"  total USM families:           {sweep['by_class']['upper_semimodular']['count']}")
    print(f"  USM target_F strict (>0):     {sweep['usm_target_F_strict_count']}")
    print(f"  USM target_F equality (=0):   {sweep['usm_target_F_equality_count']}")
    print(f"  USM target_F FAILURE (<0):    {sweep['usm_target_F_failure_count']}")
    print(f"  USM at abundance ==1/2:       {sweep['usm_at_half_count']}")

    print()
    print("=== FALSIFIER: USM family with abundance > 1/2 AND target_F < 0 ===")
    if sweep["n_falsifier_witnesses"] == 0:
        print("  NONE FOUND.  Candidate target inequality survives the n<=5 USM census.")
    else:
        print(f"  FOUND {sweep['n_falsifier_witnesses']} witnesses -- candidate DIES.")
        for w in sweep["falsifier_witnesses"]:
            tag = []
            if w["distributive"]: tag.append("dist")
            if w["modular"]:      tag.append("mod")
            print(f"  n={w['n']} masks={w['masks']} ab={w['true_abundance']:.4f} "
                  f"pm={w['pm_density']:.4f} slack={w['target_slack']} flags={','.join(tag)}")

    out = {
        "parasite_check": pc,
        "census_summary": sweep,
    }
    if out_path is None:
        out_path = DATA_DIR / "usm_probe.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print()
    print(f"[usm_probe] wrote {out_path}")
    return out


if __name__ == "__main__":
    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    main(max_n=max_n)
