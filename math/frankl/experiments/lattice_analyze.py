"""
lattice_analyze.py — Analyse the lattice_sweep data for structural inequalities
and obstructions.

Reads data/lattice_sweep_n{0..5}.jsonl and answers:

  (A) Class minima. For each special lattice class (distributive, modular,
      lower-/upper-semimodular), what is the minimum abundance? (Frankl is
      KNOWN for these classes — Poonen/Abe/Reinhold — so the min should be ≥1/2;
      we re-confirm and check tightness.)

  (B) Candidate structural inequalities of the form
          abundance ≥ g(invariants)
      We test several natural g and report the worst-case slack and whether the
      inequality ever fails. A FAIL kills that candidate.

  (C) OBSTRUCTION search. Group families by an invariant signature
      (n_L, height, width, #JI, #MI, #atoms, modular, distributive, lsm, usm).
      Within each signature, report the spread of abundance (max - min). A large
      spread = the invariants in the signature do NOT control abundance. We
      surface the extremal witness pair (same signature, abundances far apart),
      and specifically a pair where one is < 1/2 ... (none exist, since Frankl
      holds at n≤5) — so instead the sharpest witness is min vs max within a
      signature that includes the abundance-1/2 extremizers.

  (D) The Poonen filter check: min over JIs of |↑j| ≤ |L|/2 (Poonen's lattice
      statement) on every family — a direct test of the lattice formulation.
"""

from __future__ import annotations

import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

INVARIANT_KEYS = [
    "n_L", "height", "width", "n_join_irred", "n_meet_irred", "n_atoms",
    "modular", "distributive", "lower_semimodular", "upper_semimodular",
]


def load(n_max=5):
    recs = []
    for n in range(n_max + 1):
        path = os.path.join(DATA, f"lattice_sweep_n{n}.jsonl")
        if not os.path.exists(path):
            continue
        with open(path) as f:
            for line in f:
                r = json.loads(line)
                r["_n"] = n
                recs.append(r)
    return recs


def part_A_class_minima(recs):
    print("=" * 78)
    print("(A) Minimum abundance within special lattice classes")
    print("=" * 78)
    classes = {
        "ALL": lambda r: True,
        "distributive": lambda r: r["distributive"],
        "modular": lambda r: r["modular"],
        "modular_nondistrib": lambda r: r["modular"] and not r["distributive"],
        "lower_semimodular": lambda r: r["lower_semimodular"],
        "upper_semimodular": lambda r: r["upper_semimodular"],
        "NON-modular": lambda r: not r["modular"],
        "NON-lsm": lambda r: not r["lower_semimodular"],
    }
    for name, pred in classes.items():
        sub = [r for r in recs if pred(r)]
        if not sub:
            print(f"  {name:22s}: (empty)")
            continue
        mn = min(r["abundance"] for r in sub)
        cnt = len(sub)
        n_below_half = sum(1 for r in sub if r["abundance"] < 0.5 - 1e-12)
        print(f"  {name:22s}: count={cnt:6d}  min_abundance={mn:.6f}  "
              f"#(<1/2)={n_below_half}")


def part_B_candidate_inequalities(recs):
    print()
    print("=" * 78)
    print("(B) Candidate structural lower bounds  abundance ≥ g(invariants)")
    print("=" * 78)
    # Each candidate: (name, g(r)). Report min slack = min(abundance - g) and
    # whether it is ever violated (slack < 0).
    candidates = {
        # trivial sanity
        "1/2 (Frankl itself)": lambda r: 0.5,
        # height-based: abundance ≥ 1/height ?  (chain has abundance=h/(h+? ))
        "1/height": lambda r: 1.0 / r["height"] if r["height"] else 0.0,
        # tallest-chain element heuristic: ≥ height/|L|
        "height/n_L": lambda r: r["height"] / r["n_L"],
        # 1/width
        "1/width": lambda r: 1.0 / r["width"] if r["width"] else 0.0,
        # join-irreducible density
        "1/n_join_irred": lambda r: 1.0 / r["n_join_irred"] if r["n_join_irred"] else 0.0,
        # Poonen filter form: (n_L - poonen_min_filter)/n_L is the abundance of the
        # most-frequent JI in the Birkhoff re-encoding; compare to family abundance
        "poonen_complement": lambda r: (r["n_L"] - r["poonen_min_filter"]) / r["n_L"],
    }
    for name, g in candidates.items():
        worst = min(r["abundance"] - g(r) for r in recs)
        viol = [r for r in recs if r["abundance"] - g(r) < -1e-9]
        flag = "HOLDS" if not viol else f"VIOLATED ×{len(viol)}"
        print(f"  abundance ≥ {name:24s}: min slack={worst:+.6f}  [{flag}]")
        if viol:
            w = min(viol, key=lambda r: r["abundance"] - g(r))
            print(f"      worst violator: n={w['_n']} sets={w['sets']} "
                  f"abundance={w['abundance']:.4f} g={g(w):.4f}")


def signature(r):
    return tuple(r[k] for k in INVARIANT_KEYS)


def part_C_obstruction(recs):
    print()
    print("=" * 78)
    print("(C) OBSTRUCTION: families with IDENTICAL invariant signature but")
    print("    DIFFERENT abundance  (invariants do not determine abundance)")
    print("=" * 78)
    groups = defaultdict(list)
    for r in recs:
        groups[signature(r)].append(r)
    # find signature with the largest abundance spread
    spreads = []
    for sig, members in groups.items():
        abos = [m["abundance"] for m in members]
        spread = max(abos) - min(abos)
        if spread > 1e-9:
            spreads.append((spread, sig, members))
    spreads.sort(reverse=True, key=lambda t: t[0])
    print(f"  #distinct invariant signatures = {len(groups)}")
    print(f"  #signatures with abundance spread > 0 = {len(spreads)}")
    print()
    print("  Top signature collisions (same full invariant signature, "
          "different abundance):")
    for spread, sig, members in spreads[:6]:
        lo = min(members, key=lambda m: m["abundance"])
        hi = max(members, key=lambda m: m["abundance"])
        sigd = dict(zip(INVARIANT_KEYS, sig))
        print(f"  --- spread={spread:.4f}  signature={sigd}")
        print(f"        LOW  abundance={lo['abundance']:.4f}  n={lo['_n']}  sets={lo['sets']}")
        print(f"        HIGH abundance={hi['abundance']:.4f}  n={hi['_n']}  sets={hi['sets']}")
    return spreads


def part_C2_minimal_obstruction(recs):
    """Smallest (|L| minimal) witness pair with same signature, different abundance.

    We want the *cleanest* obstruction: smallest lattice, ideally same |L|, with
    same (height,width,#JI,#MI,#atoms,modularity flags) but different abundance.
    Prefer a pair where abundance differs and at least one equals 1/2 (the
    extremizer), to show invariants can't certify the 1/2 boundary.
    """
    print()
    print("=" * 78)
    print("(C2) Minimal / cleanest obstruction witnesses")
    print("=" * 78)
    groups = defaultdict(list)
    for r in recs:
        groups[signature(r)].append(r)
    best = None  # (n_L, spread, pair)
    best_half = None  # a pair straddling/at 1/2
    for sig, members in groups.items():
        abos = sorted(set(round(m["abundance"], 9) for m in members))
        if len(abos) < 2:
            continue
        lo = min(members, key=lambda m: m["abundance"])
        hi = max(members, key=lambda m: m["abundance"])
        n_L = sig[0]
        spread = hi["abundance"] - lo["abundance"]
        cand = (n_L, -spread, lo, hi)
        if best is None or cand[:2] < best[:2]:
            best = cand
        # one at exactly 1/2
        if abs(lo["abundance"] - 0.5) < 1e-9:
            ch = (n_L, -spread, lo, hi)
            if best_half is None or ch[:2] < best_half[:2]:
                best_half = ch
    if best:
        n_L, negspread, lo, hi = best
        print(f"  Smallest-|L| signature collision (|L|={n_L}, spread={-negspread:.4f}):")
        print(f"     LOW  abundance={lo['abundance']:.4f} sets={lo['sets']}")
        print(f"     HIGH abundance={hi['abundance']:.4f} sets={hi['sets']}")
        sigd = dict(zip(INVARIANT_KEYS, signature(lo)))
        print(f"     shared signature = {sigd}")
    if best_half:
        n_L, negspread, lo, hi = best_half
        print()
        print(f"  Cleanest collision with LOW exactly at abundance 1/2 "
              f"(|L|={n_L}, spread={-negspread:.4f}):")
        print(f"     LOW  abundance={lo['abundance']:.4f} sets={lo['sets']}  [the Frankl-extremal one]")
        print(f"     HIGH abundance={hi['abundance']:.4f} sets={hi['sets']}")
        sigd = dict(zip(INVARIANT_KEYS, signature(lo)))
        print(f"     shared signature = {sigd}")


def part_D_poonen(recs):
    print()
    print("=" * 78)
    print("(D) Poonen lattice statement: min_{JI} |↑j| ≤ |L|/2 on every family?")
    print("=" * 78)
    viol = [r for r in recs if r["poonen_min_filter"] > r["n_L"] / 2 + 1e-12]
    print(f"  families checked = {len(recs)}")
    print(f"  Poonen violations (min filter > |L|/2) = {len(viol)}")
    if viol:
        for r in viol[:5]:
            print(f"    n={r['_n']} sets={r['sets']} poonen_min={r['poonen_min_filter']} |L|/2={r['n_L']/2}")
    # also: is the Frankl abundance ≥ 1/2 equivalent (per-family) to Poonen here?
    # Frankl uses |F| threshold; Poonen uses |L|. Report any family where Frankl
    # holds but the |L|-normalized Poonen statement is tight/violated.
    tight = sum(1 for r in recs if abs(r["poonen_min_filter"] - r["n_L"] / 2) < 1e-9)
    print(f"  Poonen-tight families (min filter == |L|/2 exactly) = {tight}")


if __name__ == "__main__":
    recs = load(5)
    print(f"loaded {len(recs)} families (|F| ≥ 2, n ≤ 5)\n")
    part_A_class_minima(recs)
    part_B_candidate_inequalities(recs)
    part_C_obstruction(recs)
    part_C2_minimal_obstruction(recs)
    part_D_poonen(recs)
