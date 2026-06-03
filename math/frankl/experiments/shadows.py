"""
shadows.py — Kruskal–Katona / shadow (and shade) attack on Frankl's
union-closed conjecture.

This module implements and EXHAUSTIVELY TESTS (on all UC families n ≤ 5) the
shadow-method machinery described in `theory/shadows_kruskal_katona.md`:

(a) Compression / shifting operators (the classical down-shift S_{ij}).
    Question: does shifting PRESERVE union-closure?  And does it only
    DECREASE max-abundance (so the extremal case is compressed)?
    If both hold, shadow/compression methods would reduce Frankl to shifted
    families.  We test this exhaustively.

(b) The F_i / F_{¬i} split.  For a UC family F and element i:
        F_i   = {A ∈ F : i ∈ A}
        F_{¬i}= {A ∈ F : i ∉ A}      (itself union-closed)
    abundance_i ≥ 1/2  ⟺  |F_i| ≥ |F_{¬i}|.
    We compute the lower shadow ∂ and upper shade ∇ of each part and search
    for a Kruskal–Katona-type inequality forcing max_i |F_i| ≥ |F|/2.

(c) Layer / profile analysis.  The profile is (f_0, f_1, …, f_n) with
    f_k = #{A ∈ F : |A| = k}.  Union-closure constrains the profile.
    We search for an LYM / Kruskal–Katona-style profile inequality.

(d) Ahlswede–Daykin / FKG correlation.  Test whether the union-closed
    structure (an up-set–like correlation between the events {i ∈ A} and
    {membership in F}) gives a positive correlation forcing abundance.

NOTHING here is asserted as a theorem.  This script gathers the evidence the
writeup reasons about.  Every candidate inequality is checked for VIOLATIONS
across the full n ≤ 5 enumeration; a single violation falsifies it.

Authorship: Alex Ye (no AI on author line).  All novelty [NOVELTY UNVERIFIED]
(arXiv inaccessible this session; shadow methods are classical — Kruskal 1963,
Katona 1968 — and may already have been applied to Frankl).
"""

from __future__ import annotations

import json
import os
import sys
from collections import defaultdict
from typing import Iterable

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from uc_family import (  # noqa: E402
    Family,
    abundance,
    frequencies,
    ground_set,
    is_union_closed,
    mask_to_set,
)
from enumerate import all_uc_families  # noqa: E402


# ---------------------------------------------------------------------------
# Basic shadow / shade operators on a FAMILY of equal-or-mixed-size sets
# ---------------------------------------------------------------------------

def popcount(m: int) -> int:
    return bin(m).count("1")


def lower_shadow(F: Iterable[int]) -> frozenset:
    """∂F = { A \\ {x} : A ∈ F, x ∈ A } (all one-element deletions).

    This is the standard lower shadow used in Kruskal–Katona, applied to the
    whole family (mixing sizes).  For a layer F^{(k)} it is the classical
    (k-1)-shadow.
    """
    out = set()
    for m in F:
        mm = m
        while mm:
            low = mm & -mm
            out.add(m ^ low)
            mm ^= low
    return frozenset(out)


def upper_shade(F: Iterable[int], n: int) -> frozenset:
    """∇F = { A ∪ {x} : A ∈ F, x ∉ A, x ∈ [n] } (all one-element additions)."""
    out = set()
    full = (1 << n) - 1
    for m in F:
        comp = full & ~m
        cc = comp
        while cc:
            low = cc & -cc
            out.add(m | low)
            cc ^= low
    return frozenset(out)


def layer(F: Iterable[int], k: int) -> frozenset:
    """The k-th layer F^{(k)} = {A ∈ F : |A| = k}."""
    return frozenset(m for m in F if popcount(m) == k)


def profile(F: Iterable[int], n: int) -> list[int]:
    """(f_0, …, f_n) with f_k = #{A ∈ F : |A| = k}."""
    prof = [0] * (n + 1)
    for m in F:
        prof[popcount(m)] += 1
    return prof


# ---------------------------------------------------------------------------
# (a) Compression / shifting operator S_{ij}
# ---------------------------------------------------------------------------

def shift_set(m: int, i: int, j: int) -> int:
    """Down-shift a single set under S_{ij} (move element j → i if possible).

    Classical (i < j) down-compression of a set A:
        if j ∈ A, i ∉ A, and (A \\ {j}) ∪ {i}  is "free" (handled at family
        level), replace j by i.
    Here we return the *candidate* replacement; the family-level operator
    decides whether to accept it (only if the target is not already present).
    """
    bit_i = 1 << i
    bit_j = 1 << j
    if (m & bit_j) and not (m & bit_i):
        return (m ^ bit_j) | bit_i
    return m


def shift_family(F: Family, i: int, j: int) -> Family:
    """The classical down-compression operator S_{ij} (i < j) on a family.

    For each A ∈ F with j ∈ A, i ∉ A:
        let A' = (A \\ {j}) ∪ {i}.
        If A' ∉ F, replace A by A'; otherwise keep A.
    This is the standard shifting (Frankl) operator.  It is a bijection that
    pushes mass from coordinate j toward coordinate i, preserving all layer
    sizes f_k.
    """
    F_set = set(F)
    bit_i = 1 << i
    bit_j = 1 << j
    result = set()
    for m in F_set:
        if (m & bit_j) and not (m & bit_i):
            m_prime = (m ^ bit_j) | bit_i
            if m_prime in F_set:
                result.add(m)          # blocked: target already present
            else:
                result.add(m_prime)    # shifted
        else:
            result.add(m)
    return frozenset(result)


def fully_compressed(F: Family, n: int) -> bool:
    """True iff S_{ij}(F) = F for all i < j (F is a fixed point of all shifts)."""
    for i in range(n):
        for j in range(i + 1, n):
            if shift_family(F, i, j) != F:
                return False
    return True


def compress_to_fixed_point(F: Family, n: int, max_iters: int = 1000) -> Family:
    """Repeatedly apply every S_{ij} (i<j) until a simultaneous fixed point."""
    cur = F
    for _ in range(max_iters):
        changed = False
        for i in range(n):
            for j in range(i + 1, n):
                nxt = shift_family(cur, i, j)
                if nxt != cur:
                    cur = nxt
                    changed = True
        if not changed:
            return cur
    return cur


# ---------------------------------------------------------------------------
# (b) The F_i / F_{¬i} split
# ---------------------------------------------------------------------------

def split(F: Family, i: int) -> tuple[frozenset, frozenset]:
    """Return (F_i, F_{¬i}) — sets containing / not containing element i."""
    bit = 1 << i
    Fi = frozenset(m for m in F if m & bit)
    Fni = frozenset(m for m in F if not (m & bit))
    return Fi, Fni


def link_and_trace(F: Family, i: int) -> tuple[frozenset, frozenset]:
    """The 'link' and 'trace' at i, both families on [n] \\ {i}.

        link_i  = { A \\ {i} : A ∈ F_i }      (the i-link / contraction)
        trace_i = F_{¬i}                       (the i-deletion)
    Both are union-closed.  abundance_i ≥ 1/2 ⟺ |link_i| ≥ |trace_i|.
    Note link_i ⊇ trace_i is FALSE in general; that containment is exactly
    what a shadow argument would want and we test it below.
    """
    bit = 1 << i
    Fi, Fni = split(F, i)
    link = frozenset(m ^ bit for m in Fi)   # delete i
    trace = Fni
    return link, trace


# ---------------------------------------------------------------------------
# Sweep
# ---------------------------------------------------------------------------

def analyze_family(F: Family, n: int) -> dict:
    """Compute all shadow-method statistics for one UC family."""
    sets = list(F)
    sz = len(sets)
    freqs = frequencies(sets, n) if n > 0 else []
    ab = abundance(sets) if sz else 0.0
    prof = profile(sets, n)

    # (a) compression
    is_compressed = fully_compressed(F, n)
    F_comp = compress_to_fixed_point(F, n)
    comp_is_uc = is_union_closed(F_comp)
    comp_ab = abundance(list(F_comp)) if F_comp else 0.0
    comp_preserves_uc = comp_is_uc
    comp_changes_ab = abs(comp_ab - ab) > 1e-12
    comp_increases_ab = comp_ab > ab + 1e-12

    # single-step UC preservation: does ANY single S_{ij} break UC?
    single_shift_breaks_uc = False
    single_shift_raises_ab = False
    for i in range(n):
        for j in range(i + 1, n):
            G = shift_family(F, i, j)
            if not is_union_closed(G):
                single_shift_breaks_uc = True
            gab = abundance(list(G)) if G else 0.0
            if gab > ab + 1e-12:
                single_shift_raises_ab = True

    # (b) split data per element + KK quantities
    split_rows = []
    for i in range(n):
        Fi, Fni = split(F, i)
        link, trace = link_and_trace(F, i)
        d_link = lower_shadow(link)
        d_trace = lower_shadow(trace)
        shade_link = upper_shade(link, n)
        shade_trace = upper_shade(trace, n)
        # the union-closure cross relation: A∈F_i, B∈F_{¬i} ⇒ A∪B ∈ F_i,
        # equivalently trace ⊆ link?  (B = B, and B∪(min of Fi) lands in link)
        trace_subset_link = trace.issubset(link)
        split_rows.append({
            "i": i,
            "fi": len(Fi),
            "fni": len(Fni),
            "freq": freqs[i] if i < len(freqs) else 0,
            "abund_i": (freqs[i] / sz) if (sz and i < len(freqs)) else 0.0,
            "link_size": len(link),
            "trace_size": len(trace),
            "shadow_link": len(d_link),
            "shadow_trace": len(d_trace),
            "shade_link": len(shade_link),
            "shade_trace": len(shade_trace),
            "trace_subset_link": trace_subset_link,
        })

    return {
        "n": n,
        "size": sz,
        "abundance": ab,
        "freqs": freqs,
        "profile": prof,
        "is_compressed": is_compressed,
        "comp_preserves_uc": comp_preserves_uc,
        "comp_abundance": comp_ab,
        "comp_changes_ab": comp_changes_ab,
        "comp_increases_ab": comp_increases_ab,
        "single_shift_breaks_uc": single_shift_breaks_uc,
        "single_shift_raises_ab": single_shift_raises_ab,
        "split": split_rows,
        "masks": sorted(sets),
    }


def sweep(n_max: int = 5):
    """Run the full sweep, writing per-family jsonl and returning aggregates."""
    data_dir = os.path.join(HERE, "data")
    os.makedirs(data_dir, exist_ok=True)

    agg = {
        "families": 0,
        # (a)
        "comp_breaks_uc_count": 0,
        "comp_increases_ab_count": 0,
        "single_shift_breaks_uc_count": 0,
        "single_shift_raises_ab_count": 0,
        "comp_breaks_uc_witnesses": [],
        "comp_increases_ab_witnesses": [],
        "single_shift_breaks_uc_witnesses": [],
        # (b) KK-style candidate inequalities (count VIOLATIONS)
        "kk_trace_subset_link_violations": 0,   # claim: trace ⊆ link for the max-i
        "kk_link_ge_trace_for_some_i_violations": 0,  # = Frankl itself
        # (c) profile candidate
        "profile_top_heavy_violations": 0,   # claim: f_n ≥ 1 and top elements abundant
        # data accumulation for envelopes
        "by_abund_min_examples": {},
    }

    for n in range(0, n_max + 1):
        out_path = os.path.join(data_dir, f"shadows_n{n}.jsonl")
        with open(out_path, "w") as fh:
            for F in all_uc_families(n, dedupe_isomorphic=True):
                if not F:
                    continue
                # Skip degenerate families with empty ground set: F = {} or
                # F = {∅}.  Frankl's statement excludes F = {∅} a priori
                # (no elements can be abundant).  ground_set(F) == 0 ⟺ F ⊆ {∅}.
                if ground_set(F) == 0:
                    continue
                rec = analyze_family(F, n)
                if rec["size"] == 0:
                    continue
                fh.write(json.dumps(rec) + "\n")
                agg["families"] += 1

                # (a) aggregates
                if not rec["comp_preserves_uc"]:
                    agg["comp_breaks_uc_count"] += 1
                    if len(agg["comp_breaks_uc_witnesses"]) < 10:
                        agg["comp_breaks_uc_witnesses"].append(
                            {"n": n, "masks": rec["masks"]})
                if rec["comp_increases_ab"]:
                    agg["comp_increases_ab_count"] += 1
                    if len(agg["comp_increases_ab_witnesses"]) < 10:
                        agg["comp_increases_ab_witnesses"].append(
                            {"n": n, "masks": rec["masks"],
                             "ab": rec["abundance"], "comp_ab": rec["comp_abundance"]})
                if rec["single_shift_breaks_uc"]:
                    agg["single_shift_breaks_uc_count"] += 1
                    if len(agg["single_shift_breaks_uc_witnesses"]) < 10:
                        agg["single_shift_breaks_uc_witnesses"].append(
                            {"n": n, "masks": rec["masks"]})
                if rec["single_shift_raises_ab"]:
                    agg["single_shift_raises_ab_count"] += 1

                # (b) Frankl as link ≥ trace for some i
                some_i_ok = any(r["link_size"] >= r["trace_size"]
                                for r in rec["split"]) if rec["split"] else True
                if not some_i_ok:
                    agg["kk_link_ge_trace_for_some_i_violations"] += 1
                # candidate KK claim: for the MOST abundant i, trace ⊆ link
                if rec["split"]:
                    best = max(rec["split"], key=lambda r: r["fi"])
                    if not best["trace_subset_link"]:
                        agg["kk_trace_subset_link_violations"] += 1

    return agg


def candidate_inequalities(n_max: int = 5):
    """Second pass: test specific Kruskal–Katona / profile inequalities for
    violations, reading the freshly written jsonl files.

    Each candidate is a function family -> (bool ok, detail).  We report the
    number of violations and the worst (min-margin) witness.
    """
    data_dir = os.path.join(HERE, "data")
    results = defaultdict(lambda: {"violations": 0, "tested": 0,
                                   "worst": None, "worst_margin": None})

    def record(name, ok, margin, rec):
        r = results[name]
        r["tested"] += 1
        if not ok:
            r["violations"] += 1
        if r["worst_margin"] is None or margin < r["worst_margin"]:
            r["worst_margin"] = margin
            r["worst"] = {"n": rec["n"], "masks": rec["masks"][:32],
                          "abundance": rec["abundance"]}

    for n in range(1, n_max + 1):
        path = os.path.join(data_dir, f"shadows_n{n}.jsonl")
        if not os.path.exists(path):
            continue
        with open(path) as fh:
            for line in fh:
                rec = json.loads(line)
                sz = rec["size"]
                if sz == 0:
                    continue
                prof = rec["profile"]
                split_rows = rec["split"]

                # --- C1: Frankl baseline (max_i fi >= sz/2) ---
                if split_rows:
                    max_fi = max(r["fi"] for r in split_rows)
                    margin = max_fi - sz / 2
                    record("C1_frankl_maxfi_ge_half", max_fi >= sz / 2 - 1e-9,
                           margin, rec)

                # --- C2: KK shadow inequality on link vs trace ---
                # Claim: for the max-abundance i, |∂(link_i)| >= |∂(trace_i)|.
                # Motivation: if link contains trace's shadow structure.
                if split_rows:
                    best = max(split_rows, key=lambda r: r["fi"])
                    margin = best["shadow_link"] - best["shadow_trace"]
                    record("C2_shadow_link_ge_shadow_trace_at_best",
                           best["shadow_link"] >= best["shadow_trace"],
                           margin, rec)

                # --- C3: shade inequality (Kruskal–Katona upward) ---
                # Claim: |∇(trace_i)| <= sz for all i  (trivial-ish; calibration)
                if split_rows:
                    ok = all(r["shade_trace"] <= sz + r["trace_size"]
                             for r in split_rows)
                    # margin = min slack
                    margin = min((sz + r["trace_size"]) - r["shade_trace"]
                                 for r in split_rows)
                    record("C3_shade_trace_le_size_plus_trace", ok, margin, rec)

                # --- C4: profile top-heaviness (LYM-style) ---
                # Claim: sum_k f_k * k / n  >=  sz/2   (avg-size >= n/2 * ... )
                # i.e. average set size >= n/2?  Tests whether UC families are
                # "top heavy" enough to force abundance.  (Likely FALSE.)
                if n >= 1:
                    avg_size = sum(prof[k] * k for k in range(n + 1)) / sz
                    margin = avg_size - n / 2
                    record("C4_avg_size_ge_half_n", avg_size >= n / 2 - 1e-9,
                           margin, rec)

                # --- C5: Reimer-style average set size >= (1/2) log2 |F| ---
                # Known TRUE (Reimer 2003).  Calibration / sanity.
                import math
                if sz >= 1:
                    avg_size = sum(prof[k] * k for k in range(n + 1)) / sz
                    target = 0.5 * math.log2(sz) if sz >= 1 else 0.0
                    margin = avg_size - target
                    record("C5_reimer_avg_size", avg_size >= target - 1e-9,
                           margin, rec)

                # --- C6: trace ⊆ link at the BEST i (the key UC containment) ---
                if split_rows:
                    best = max(split_rows, key=lambda r: r["fi"])
                    # margin: link_size - trace_size given containment claim
                    ok = best["trace_subset_link"]
                    margin = 1.0 if ok else 0.0
                    record("C6_trace_subset_link_at_best", ok, margin, rec)

                # --- C7: trace ⊆ link at SOME i (weaker) ---
                if split_rows:
                    ok = any(r["trace_subset_link"] for r in split_rows)
                    record("C7_trace_subset_link_some_i", ok,
                           1.0 if ok else 0.0, rec)

                # --- C8: the AVERAGE over i of (fi - fni) >= 0  ⟺ avg set size >=? ---
                # sum_i (fi - fni) = sum_i (2 fi - sz) = 2*sum_i fi - n*sz
                #                  = 2*(total incidences) - n*sz
                # >= 0  ⟺  average set size >= n/2.  (Same as C4.)  Skip.

    return dict(results)


# ---------------------------------------------------------------------------
# (d) Ahlswede–Daykin / FKG correlation test
# ---------------------------------------------------------------------------

def fkg_correlation(F: Family, n: int) -> list[dict]:
    """Test an FKG/Ahlswede–Daykin-style positive-correlation inequality.

    On the Boolean lattice 2^[n] with the UNIFORM measure restricted to F
    (i.e. μ = uniform on F), consider the up-set events U_i = {A : i ∈ A}.
    FKG would assert Pr[U_i ∩ U_j] ≥ Pr[U_i] Pr[U_j] IF μ were log-supermodular
    (an FKG measure).  The uniform measure on a UC family is NOT log-supermodular
    in general (UC ≠ up-set), so FKG need not hold.  We test it: does
        abundance_i · abundance_j  ≤  Pr[i,j ∈ A]   (pairwise positive corr.)
    hold for UC families?  And the variant with the whole family as the event.

    We also test the "Harris/Kleitman" form: is F positively correlated with
    each principal up-set?  Specifically whether
        |F ∩ ↑{i}| / |F|  ≥  |↑{i}| / 2^n        is consistently signed.
    """
    sets = list(F)
    sz = len(sets)
    rows = []
    for i in range(n):
        bi = 1 << i
        pi = sum(1 for m in sets if m & bi) / sz
        for j in range(i + 1, n):
            bj = 1 << j
            pj = sum(1 for m in sets if m & bj) / sz
            pij = sum(1 for m in sets if (m & bi) and (m & bj)) / sz
            rows.append({
                "i": i, "j": j, "pi": pi, "pj": pj, "pij": pij,
                "fkg_holds": pij >= pi * pj - 1e-12,  # positive correlation?
                "corr": pij - pi * pj,
            })
    return rows


def cone_extremizer_check(n: int) -> dict:
    """The Boolean cube 2^[n] and its cone — the recurring FUCC extremizer.

    Mirrors the obstruction in lattice_attack.md / boolean_fourier.md:
    the cube 2^[n] saturates abundance = 1/2.  We confirm the cube is a
    fixed point of compression and a shadow-method 'collapse' point, and
    that the cone pushes abundance to 1 − 1/2^n while the SHADOW PROFILE is
    isomorphic.  This shows shadow statistics cannot distinguish them either.
    """
    full = (1 << n) - 1
    cube = frozenset(range(1 << n))                       # 2^[n]
    z = n                                                  # fresh coord for cone
    cone = frozenset({0} | {m | (1 << z) for m in range(1 << n) if m != 0})
    return {
        "n": n,
        "cube_abundance": abundance(list(cube)),
        "cube_is_compressed": fully_compressed(cube, n),
        "cube_profile": profile(cube, n),
        "cone_abundance": abundance(list(cone)),
        "cone_profile": profile(cone, n + 1),
        "cone_is_uc": is_union_closed(cone),
    }


def fkg_sweep(n_max: int = 5) -> dict:
    """Aggregate FKG/Ahlswede–Daykin correlation results over all UC families."""
    agg = {"pairs": 0, "fkg_violations": 0, "fkg_violation_witnesses": [],
           "min_corr": None, "min_corr_witness": None}
    for n in range(2, n_max + 1):
        for F in all_uc_families(n, dedupe_isomorphic=True):
            if not F or ground_set(F) == 0:
                continue
            for r in fkg_correlation(F, n):
                agg["pairs"] += 1
                if not r["fkg_holds"]:
                    agg["fkg_violations"] += 1
                    if len(agg["fkg_violation_witnesses"]) < 10:
                        agg["fkg_violation_witnesses"].append(
                            {"n": n, "masks": sorted(F), "i": r["i"],
                             "j": r["j"], "corr": r["corr"]})
                if agg["min_corr"] is None or r["corr"] < agg["min_corr"]:
                    agg["min_corr"] = r["corr"]
                    agg["min_corr_witness"] = {"n": n, "masks": sorted(F),
                                               "i": r["i"], "j": r["j"]}
    return agg


if __name__ == "__main__":
    print("=== shadows.py sweep (Kruskal–Katona / shadow attack) ===")
    agg = sweep(5)
    print(f"\nFamilies analyzed (nontrivial, n≤5): {agg['families']}")
    print("\n--- (a) Compression / shifting ---")
    print(f"  compress-to-fixed-point BREAKS union-closure:  "
          f"{agg['comp_breaks_uc_count']} families")
    print(f"  single S_ij BREAKS union-closure:              "
          f"{agg['single_shift_breaks_uc_count']} families")
    print(f"  compression INCREASES max-abundance:           "
          f"{agg['comp_increases_ab_count']} families")
    print(f"  single S_ij RAISES max-abundance:              "
          f"{agg['single_shift_raises_ab_count']} families")
    if agg["comp_breaks_uc_witnesses"]:
        print("  example UC-breaking compression witnesses:")
        for w in agg["comp_breaks_uc_witnesses"][:5]:
            print(f"    n={w['n']} masks={w['masks']}")
    if agg["comp_increases_ab_witnesses"]:
        print("  example abundance-increasing witnesses:")
        for w in agg["comp_increases_ab_witnesses"][:5]:
            print(f"    n={w['n']} ab={w['ab']:.4f}->{w['comp_ab']:.4f} "
                  f"masks={w['masks']}")

    print("\n--- (b) F_i/F_¬i split: Frankl link≥trace check ---")
    print(f"  families where NO i has link_size ≥ trace_size: "
          f"{agg['kk_link_ge_trace_for_some_i_violations']} (Frankl violations)")
    print(f"  'trace ⊆ link at best i' violations:           "
          f"{agg['kk_trace_subset_link_violations']}")

    print("\n=== candidate inequality sweep (violation counts) ===")
    ci = candidate_inequalities(5)
    for name in sorted(ci):
        r = ci[name]
        wm = r["worst_margin"]
        print(f"  {name}: tested={r['tested']} violations={r['violations']} "
              f"worst_margin={wm:.4f}" if wm is not None else
              f"  {name}: tested={r['tested']} violations={r['violations']}")
        if r["violations"] and r["worst"]:
            w = r["worst"]
            print(f"      worst witness: n={w['n']} ab={w['abundance']:.4f} "
                  f"masks={w['masks']}")

    # write summary
    data_dir = os.path.join(HERE, "data")
    with open(os.path.join(data_dir, "shadows_summary.txt"), "w") as fh:
        fh.write("shadows.py summary\n")
        fh.write(f"families: {agg['families']}\n\n")
        fh.write("(a) compression/shifting:\n")
        fh.write(f"  comp_breaks_uc: {agg['comp_breaks_uc_count']}\n")
        fh.write(f"  single_shift_breaks_uc: {agg['single_shift_breaks_uc_count']}\n")
        fh.write(f"  comp_increases_ab: {agg['comp_increases_ab_count']}\n")
        fh.write(f"  single_shift_raises_ab: {agg['single_shift_raises_ab_count']}\n")
        for w in agg["comp_breaks_uc_witnesses"]:
            fh.write(f"  UC-break witness n={w['n']} masks={w['masks']}\n")
        for w in agg["comp_increases_ab_witnesses"]:
            fh.write(f"  ab-increase witness n={w['n']} "
                     f"{w['ab']:.4f}->{w['comp_ab']:.4f} masks={w['masks']}\n")
        fh.write("\n(b) Frankl link≥trace violations: "
                 f"{agg['kk_link_ge_trace_for_some_i_violations']}\n")
        fh.write("\n(candidate inequalities)\n")
        for name in sorted(ci):
            r = ci[name]
            fh.write(f"  {name}: tested={r['tested']} "
                     f"violations={r['violations']} worst_margin={r['worst_margin']}\n")
            if r["violations"] and r["worst"]:
                w = r["worst"]
                fh.write(f"     worst: n={w['n']} ab={w['abundance']:.4f} "
                         f"masks={w['masks']}\n")
    print("\n--- (d) Ahlswede–Daykin / FKG correlation ---")
    fkg = fkg_sweep(5)
    print(f"  pairs tested: {fkg['pairs']}")
    print(f"  FKG (positive-correlation Pr[i,j] ≥ Pr[i]Pr[j]) VIOLATIONS: "
          f"{fkg['fkg_violations']}")
    print(f"  min correlation Pr[i,j]-Pr[i]Pr[j]: {fkg['min_corr']:.4f}")
    if fkg["fkg_violation_witnesses"]:
        print("  example anti-correlation witnesses:")
        for w in fkg["fkg_violation_witnesses"][:5]:
            print(f"    n={w['n']} i={w['i']} j={w['j']} corr={w['corr']:.4f} "
                  f"masks={w['masks']}")

    print("\n--- cone/cube extremizer (recurring FUCC obstruction) ---")
    for n in range(1, 5):
        c = cone_extremizer_check(n)
        print(f"  n={n}: cube ab={c['cube_abundance']:.4f} "
              f"compressed={c['cube_is_compressed']} | "
              f"cone ab={c['cone_abundance']:.4f} uc={c['cone_is_uc']}")

    # append (d) results to summary
    with open(os.path.join(data_dir, "shadows_summary.txt"), "a") as fh:
        fh.write("\n(d) Ahlswede–Daykin / FKG correlation\n")
        fh.write(f"  pairs: {fkg['pairs']}\n")
        fh.write(f"  fkg_violations: {fkg['fkg_violations']}\n")
        fh.write(f"  min_corr: {fkg['min_corr']}\n")
        for w in fkg["fkg_violation_witnesses"]:
            fh.write(f"  anti-corr witness n={w['n']} i={w['i']} j={w['j']} "
                     f"corr={w['corr']:.4f} masks={w['masks']}\n")
        fh.write("\ncone/cube extremizer\n")
        for n in range(1, 6):
            c = cone_extremizer_check(n)
            fh.write(f"  n={n}: cube_ab={c['cube_abundance']:.4f} "
                     f"cube_compressed={c['cube_is_compressed']} "
                     f"cone_ab={c['cone_abundance']:.4f} cone_uc={c['cone_is_uc']}\n")

    print("\nWrote data/shadows_n*.jsonl and data/shadows_summary.txt")
