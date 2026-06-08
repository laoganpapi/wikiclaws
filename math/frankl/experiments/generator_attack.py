"""
generator_attack.py — Non-symmetric, generator-incidence attack on Frankl's
union-closed conjecture.

Author: Alex Ye (no AI on author line in the writeup).

CONTEXT.  The project's BARRIER THEOREM (PROGRESS.md) says: all eight prior
methods reduce to a SYMMETRIC convex moment of the frequency vector, and every
such moment is flat-minimized by the Boolean cube at exactly 1/2.  So no
symmetric moment can prove Frankl.  This file attacks the ONE class the barrier
does not immediately kill: NON-SYMMETRIC, generator-incidence quantities.

A union-closed family F (with the convention ∅ ∈ F) is exactly the set of all
unions of subsets of its GENERATORS

    G = { members of F not expressible as a union of strictly smaller members }

(the join-irreducibles of the union-semilattice).  Then
    F = { ⋃ S : S ⊆ G }                                            (Birkhoff/Poonen)
(with ⋃ ∅ = ∅).  G is encoded as a 0-1 incidence matrix M[g, x] = 1 iff x ∈ g.
Frankl becomes a statement about M that is NOT symmetric in the elements x: it
depends on the actual covering structure of G.

This module:
  (a) extracts generators G and the incidence matrix M, gives the exact
      abundance formula via the lattice of unions, verifies it on all families;
  (b) tests ASYMMETRIC weighting schemes (size / lower-cover / order-weighted
      generator weights; the "most frequent generator element" heuristic);
  (c) tests the deletion/induction pivot structure;
  (d) reconstructs the Knill/Wójcik generator graph and tests graph parameters.

ALL numbers validated on the standard census: every UC family (|F|≥2) with n≤5
ground elements (orbit representatives), the same 29,723-family census the rest
of the project uses.  No proof of Frankl is claimed; all novelty
[NOVELTY UNVERIFIED].
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from itertools import combinations

from uc_family import (
    abundance,
    family_from_sets,
    frequencies,
    ground_set,
    mask_to_set,
)
from enumerate import all_uc_families


# ---------------------------------------------------------------------------
# (a) Generators and the incidence matrix
# ---------------------------------------------------------------------------

def generators(F):
    """
    Return the sorted list of GENERATOR masks of a union-closed family F:
    the members m (m ≠ ∅) that are NOT the union of the strictly-smaller
    members of F below them.

    These are exactly the join-irreducibles of the lattice (F, ∪): a member is
    redundant iff it is the union of the F-members strictly contained in it.
    F = { ⋃ S : S ⊆ G } ∪ {∅}.
    """
    Fset = set(F)
    gens = []
    for m in Fset:
        if m == 0:
            continue
        u = 0
        for a in Fset:
            if a != m and (a | m) == m:   # a ⊊ m and a ∈ F
                u |= a
        if u != m:                         # m is not covered by smaller members
            gens.append(m)
    return sorted(gens)


def incidence_matrix(gens, n):
    """
    0-1 incidence matrix M as a list of rows, one per generator g (sorted),
    M[i][x] = 1 iff x ∈ gens[i].  Shape |G| × n.
    """
    return [[(g >> x) & 1 for x in range(n)] for g in gens]


def closure_of_generators(gens):
    """Return the union-closure (with ∅) of the generator set, as a set of masks."""
    closure = {0}
    # all unions of subsets of gens.  Do it incrementally (subset-sum over OR).
    for g in gens:
        closure |= {c | g for c in closure}
    return closure


# ---------------------------------------------------------------------------
# (a) The exact abundance formula in terms of M and the lattice of unions
# ---------------------------------------------------------------------------

def abundance_from_generators(gens, n):
    """
    Compute the frequency vector and abundance using ONLY the generators,
    via the lattice of unions L = { ⋃ S : S ⊆ G }.

    The exact identity used:
        freq(x) = #{ A ∈ L : x ∈ A }
                = #{ DISTINCT unions ⋃S (S ⊆ G) that contain x }.
    Crucially DISTINCT: different subsets S can yield the same union, so we count
    distinct members, not subsets S.  We enumerate L directly from G.

    Returns (freqs, |L|, max_freq, abundance).
    """
    L = closure_of_generators(gens)         # the distinct members (incl ∅)
    m = len(L)
    freqs = [0] * n
    for A in L:
        for x in range(n):
            if (A >> x) & 1:
                freqs[x] += 1
    if m == 0:
        return freqs, 0, 0, 0.0
    mx = max(freqs) if freqs else 0
    return freqs, m, mx, (mx / m if m else 0.0)


# ---------------------------------------------------------------------------
# (b) Generator-element frequency (NON-SYMMETRIC): the incidence statistic
# ---------------------------------------------------------------------------

def generator_element_freq(gens, n):
    """
    gfreq(x) = #{ g ∈ G : x ∈ g } = column sums of the incidence matrix M.
    This is NON-SYMMETRIC: it privileges the generator incidence, not the
    F-frequencies.  Returns the integer vector (gfreq(0), …, gfreq(n-1)).
    """
    gfreq = [0] * n
    for g in gens:
        for x in range(n):
            if (g >> x) & 1:
                gfreq[x] += 1
    return gfreq


def most_frequent_generator_element(gens, n):
    """
    Return (x*, gfreq(x*)) where x* maximises gfreq (ties -> smallest index).
    The HEURISTIC under test: is x* always ≥ 1/2-abundant in F?
    """
    gfreq = generator_element_freq(gens, n)
    if not gens:
        return (-1, 0)
    x_star = max(range(n), key=lambda x: (gfreq[x], -x))
    return x_star, gfreq[x_star]


def invsize_score(gens, n):
    """
    invsize(x) = Σ_{g ∈ G, x ∈ g} 1/|g|.  A NON-SYMMETRIC element score that
    weights each generator INVERSELY by its size (privileges elements that live
    in SMALL generators).  Note the exact identity  Σ_x invsize(x) = |G|  (each
    generator g contributes |g|·(1/|g|) = 1 spread over its elements).
    """
    s = [0.0] * n
    for g in gens:
        sz = bin(g).count("1")
        if sz == 0:
            continue
        for x in range(n):
            if (g >> x) & 1:
                s[x] += 1.0 / sz
    return s


def combined_pick(gens, n):
    """
    The COMBINED non-symmetric pick rule, [EXTRAORDINARY — PRESUMED FLAWED]:
      * if some generator is a singleton {x}, pick that x
        (then {x} ∈ F and the injection A ↦ A∪{x} proves freq(x) ≥ |F|/2 —
         the classical singleton case);
      * otherwise pick x maximising invsize(x) (no proof; heuristic).
    Returns x* (or -1 if no generators).
    """
    if not gens:
        return -1
    for g in gens:
        if bin(g).count("1") == 1:
            return g.bit_length() - 1
    s = invsize_score(gens, n)
    return max(range(n), key=lambda i: (s[i], -i))


# ---------------------------------------------------------------------------
# (b) Asymmetric weighting schemes
# ---------------------------------------------------------------------------

def weighted_generator_abundance(gens, n, weight_fn):
    """
    A generator-weighted 'abundance'.  Assign each generator g a weight w(g)
    (generator-dependent, NOT element-symmetric).  For each element x define

        Wab(x) = ( Σ_{g ∋ x} w(g) ) / ( Σ_{g} w(g) ).

    Return (x*, Wab(x*)) maximising Wab.  weight_fn(g, gens, n) -> float.
    This is a genuinely asymmetric statistic IF w depends on g's structure.
    """
    weights = [weight_fn(g, gens, n) for g in gens]
    total = sum(weights)
    if total <= 0:
        return (-1, 0.0)
    best_x, best_v = -1, -1.0
    for x in range(n):
        s = sum(w for g, w in zip(gens, weights) if (g >> x) & 1)
        v = s / total
        if v > best_v:
            best_v, best_x = v, x
    return best_x, best_v


# weight functions -----------------------------------------------------------

def w_by_size(g, gens, n):
    """Weight a generator by its size |g| (a non-symmetric structural weight)."""
    return bin(g).count("1")


def w_by_inv_size(g, gens, n):
    """Weight by 1/|g| (privileges small generators)."""
    s = bin(g).count("1")
    return 1.0 / s if s else 0.0


def w_uniform(g, gens, n):
    return 1.0


def w_by_filter_size(g, gens, n):
    """
    Weight a generator g by the size of its principal filter in L:
    |↑g| = #{ A ∈ L : g ⊆ A }.  This is the Poonen frequency of the
    generator — a structural, non-symmetric weight.
    """
    L = closure_of_generators(gens)
    return sum(1 for A in L if (A | g) == A)


def w_by_lower_covers(g, gens, n):
    """
    Weight g by 1 + (number of generators strictly contained in g) — a proxy
    for its position/rank in the generation order (non-symmetric).
    """
    return 1 + sum(1 for h in gens if h != g and (h | g) == g)


# ---------------------------------------------------------------------------
# (d) Knill / Wójcik generator graph
# ---------------------------------------------------------------------------

def generator_graph_shared_element(gens, n):
    """
    Graph H on the generators: g ~ g' iff they share a ground element
    (g & g' != 0).  Returns adjacency as a dict idx -> set(idx).
    """
    adj = {i: set() for i in range(len(gens))}
    for i in range(len(gens)):
        for j in range(i + 1, len(gens)):
            if gens[i] & gens[j]:
                adj[i].add(j)
                adj[j].add(i)
    return adj


def max_degree_generator_element_in_F(gens, n, F):
    """
    For diagnostics: among generators, find the element of maximum generator-
    degree and report its TRUE abundance in F.
    """
    x_star, _ = most_frequent_generator_element(gens, n)
    if x_star < 0:
        return None
    freqs = frequencies(F, n)
    return x_star, freqs[x_star] / len(F)


# ---------------------------------------------------------------------------
# (c) Deletion / induction pivot
# ---------------------------------------------------------------------------

def family_with_generator_removed(gens, removed_idx):
    """
    Return the union-closure (with ∅) of the generator set with one generator
    removed.  Used to test induction on the number of generators.
    """
    sub = [g for i, g in enumerate(gens) if i != removed_idx]
    return closure_of_generators(sub)


# ---------------------------------------------------------------------------
# Per-family record
# ---------------------------------------------------------------------------

def analyze_family(F, n):
    """Compute every generator-incidence statistic for one family F."""
    Fset = set(F)
    if 0 not in Fset:
        Fset = Fset | {0}      # adjoin ∅ so the generator picture is exact
    F = frozenset(Fset)
    m = len(F)
    gens = generators(F)
    ng = len(gens)
    freqs = frequencies(F, n)
    true_ab = (max(freqs) / m) if m and freqs else 0.0
    true_x = max(range(n), key=lambda x: (freqs[x], -x)) if n else -1

    # (a) abundance reconstructed from generators (must equal direct)
    rf, rm, rmx, rab = abundance_from_generators(gens, n)
    recon_ok = (rf == freqs) and (rm == m)

    # (b) generator-element frequency and the heuristic
    gfreq = generator_element_freq(gens, n)
    gx_star, gx_val = most_frequent_generator_element(gens, n)
    # TRUE abundance of the most-frequent-generator element:
    heur_ab = (freqs[gx_star] / m) if (gx_star >= 0 and m) else 0.0

    # (b) asymmetric weighted abundances
    w_size_x, w_size_v = weighted_generator_abundance(gens, n, w_by_size)
    w_invsize_x, w_invsize_v = weighted_generator_abundance(gens, n, w_by_inv_size)
    w_filt_x, w_filt_v = weighted_generator_abundance(gens, n, w_by_filter_size)
    w_lc_x, w_lc_v = weighted_generator_abundance(gens, n, w_by_lower_covers)

    # whether the TRUE abundant element coincides with the heuristic pick
    heur_picks_true = (gx_star == true_x)

    # the COMBINED non-symmetric pick rule (singleton-branch / invsize-branch)
    has_singleton = any(bin(g).count("1") == 1 for g in gens)
    cpick = combined_pick(gens, n)
    comb_ab = (freqs[cpick] / m) if (cpick >= 0 and m) else 0.0
    # invsize-only pick (the unproven branch), tracked separately
    ivs = invsize_score(gens, n)
    iv_pick = max(range(n), key=lambda i: (ivs[i], -i)) if (n and gens) else -1
    iv_ab = (freqs[iv_pick] / m) if (iv_pick >= 0 and m) else 0.0

    return {
        "n": n,
        "m": m,
        "ngens": ng,
        "gen_masks": gens,
        "freqs": freqs,
        "gfreq": gfreq,
        "true_ab": true_ab,
        "true_x": true_x,
        "recon_ok": recon_ok,
        # heuristic: most frequent generator element, its true abundance
        "gx_star": gx_star,
        "heur_ab": heur_ab,
        "heur_picks_true": heur_picks_true,
        # combined non-symmetric pick rule [PRESUMED FLAWED]
        "has_singleton": has_singleton,
        "comb_pick": cpick,
        "comb_ab": comb_ab,
        "iv_pick": iv_pick,
        "iv_ab": iv_ab,
        # asymmetric weighted abundances (these are statistics, not true ab):
        "w_size_v": w_size_v,
        "w_invsize_v": w_invsize_v,
        "w_filt_v": w_filt_v,
        "w_lc_v": w_lc_v,
    }


# ---------------------------------------------------------------------------
# Sweep driver
# ---------------------------------------------------------------------------

def sweep(nmax, out_prefix):
    summary = {
        "total": 0,
        "recon_violations": 0,
        # heuristic "most freq generator element >= 1/2 abundant in F"
        "heur_fail": 0,                 # families where heur_ab < 1/2
        "heur_fail_examples": [],
        "heur_min_ab": 1.0,
        "heur_min_example": None,
        "heur_picks_true_count": 0,
        # weighted-abundance certificate failures (statistic < 1/2)
        "w_size_fail": 0, "w_size_min": 1.0, "w_size_min_ex": None,
        "w_invsize_fail": 0, "w_invsize_min": 1.0, "w_invsize_min_ex": None,
        "w_filt_fail": 0, "w_filt_min": 1.0, "w_filt_min_ex": None,
        "w_lc_fail": 0, "w_lc_min": 1.0, "w_lc_min_ex": None,
        # COMBINED non-symmetric pick rule [PRESUMED FLAWED] — singleton / invsize
        "comb_fail": 0, "comb_min": 1.0, "comb_min_ex": None,
        "comb_eq_count": 0,
        # invsize-only branch (the unproven part), restricted to no-singleton families
        "nosingleton_total": 0,
        "iv_nosingleton_fail": 0, "iv_nosingleton_min": 1.0, "iv_nosingleton_min_ex": None,
        "iv_nosingleton_fail_ex": [],
        # singleton branch (the provable part)
        "singleton_total": 0,
        "singleton_fail": 0, "singleton_min": 1.0,
        # cube equality check (the discipline gate): on cubes must be exactly 1/2
        "cube_checks": [],
    }

    for n in range(nmax + 1):
        recs = []
        for F in all_uc_families(n):
            if len(F) < 2:
                continue
            # need ∅ for the lattice; analyze_family adjoins it
            rec = analyze_family(F, n)
            recs.append(rec)
            summary["total"] += 1
            if not rec["recon_ok"]:
                summary["recon_violations"] += 1

            # heuristic
            ha = rec["heur_ab"]
            if ha < summary["heur_min_ab"]:
                summary["heur_min_ab"] = ha
                summary["heur_min_example"] = {
                    "n": n, "gens": [bin(g) for g in rec["gen_masks"]],
                    "freqs": rec["freqs"], "gx_star": rec["gx_star"],
                    "heur_ab": ha, "true_ab": rec["true_ab"],
                }
            if ha < 0.5 - 1e-12:
                summary["heur_fail"] += 1
                if len(summary["heur_fail_examples"]) < 25:
                    summary["heur_fail_examples"].append({
                        "n": n, "gens": [bin(g) for g in rec["gen_masks"]],
                        "freqs": rec["freqs"], "gx_star": rec["gx_star"],
                        "gfreq": rec["gfreq"],
                        "heur_ab": ha, "true_ab": rec["true_ab"],
                        "true_x": rec["true_x"],
                    })
            if rec["heur_picks_true"]:
                summary["heur_picks_true_count"] += 1

            # weighted-abundance statistics as standalone certificates
            for key, val in (("w_size", rec["w_size_v"]),
                             ("w_invsize", rec["w_invsize_v"]),
                             ("w_filt", rec["w_filt_v"]),
                             ("w_lc", rec["w_lc_v"])):
                if val < summary[key + "_min"]:
                    summary[key + "_min"] = val
                    summary[key + "_min_ex"] = {
                        "n": n, "gens": [bin(g) for g in rec["gen_masks"]],
                        "freqs": rec["freqs"], "val": val,
                        "true_ab": rec["true_ab"],
                    }
                if val < 0.5 - 1e-12:
                    summary[key + "_fail"] += 1

            # COMBINED non-symmetric pick rule
            ca = rec["comb_ab"]
            if ca < summary["comb_min"]:
                summary["comb_min"] = ca
                summary["comb_min_ex"] = {
                    "n": n, "gens": [bin(g) for g in rec["gen_masks"]],
                    "freqs": rec["freqs"], "pick": rec["comb_pick"], "comb_ab": ca,
                }
            if ca < 0.5 - 1e-12:
                summary["comb_fail"] += 1
            if abs(ca - 0.5) < 1e-12:
                summary["comb_eq_count"] += 1

            # branch breakdown
            if rec["has_singleton"]:
                summary["singleton_total"] += 1
                if rec["comb_ab"] < summary["singleton_min"]:
                    summary["singleton_min"] = rec["comb_ab"]
                if rec["comb_ab"] < 0.5 - 1e-12:
                    summary["singleton_fail"] += 1
            else:
                summary["nosingleton_total"] += 1
                iva = rec["iv_ab"]
                if iva < summary["iv_nosingleton_min"]:
                    summary["iv_nosingleton_min"] = iva
                    summary["iv_nosingleton_min_ex"] = {
                        "n": n, "gens": [bin(g) for g in rec["gen_masks"]],
                        "freqs": rec["freqs"], "pick": rec["iv_pick"], "iv_ab": iva,
                    }
                if iva < 0.5 - 1e-12:
                    summary["iv_nosingleton_fail"] += 1
                    if len(summary["iv_nosingleton_fail_ex"]) < 25:
                        summary["iv_nosingleton_fail_ex"].append({
                            "n": n, "gens": [bin(g) for g in rec["gen_masks"]],
                            "freqs": rec["freqs"], "pick": rec["iv_pick"], "iv_ab": iva,
                        })

        # write per-n jsonl
        with open(f"{out_prefix}_n{n}.jsonl", "w") as fh:
            for rec in recs:
                fh.write(json.dumps(rec) + "\n")

    # cube discipline check: the standard cubes 2^[k], k=1..nmax
    for k in range(1, nmax + 1):
        masks = list(range(1 << k))
        cube = frozenset(masks)   # full power set = 2^[k]
        rec = analyze_family(cube, k)
        summary["cube_checks"].append({
            "k": k, "m": rec["m"], "ngens": rec["ngens"],
            "true_ab": rec["true_ab"], "heur_ab": rec["heur_ab"],
            "comb_ab": rec["comb_ab"], "comb_pick": rec["comb_pick"],
            "w_size_v": rec["w_size_v"], "w_invsize_v": rec["w_invsize_v"],
            "w_filt_v": rec["w_filt_v"], "w_lc_v": rec["w_lc_v"],
        })

    return summary


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    out_prefix = "data/genattack"
    summary = sweep(nmax, out_prefix)

    with open("data/genattack_summary.json", "w") as fh:
        json.dump(summary, fh, indent=2)

    lines = []
    P = lines.append
    P("=" * 72)
    P("GENERATOR-INCIDENCE (NON-SYMMETRIC) ATTACK — SUMMARY")
    P("=" * 72)
    P(f"Total UC families (|F|>=2, n<=%d, orbit reps): {summary['total']}" % nmax)
    P(f"Reconstruction-from-generators violations: {summary['recon_violations']}  "
      "(abundance via L = {{⋃S : S⊆G}} == direct)")
    P("")
    P("-" * 72)
    P("(b) HEURISTIC: 'most frequent GENERATOR element is >= 1/2-abundant in F'")
    P("-" * 72)
    P(f"  families where it FAILS (true ab of that element < 1/2): {summary['heur_fail']}")
    P(f"  min true-abundance of the most-frequent-generator element: {summary['heur_min_ab']:.6f}")
    P(f"  (the heuristic picks the genuinely most-abundant element in "
      f"{summary['heur_picks_true_count']}/{summary['total']} families)")
    if summary["heur_min_example"]:
        e = summary["heur_min_example"]
        P(f"  worst example: gens={e['gens']} freqs={e['freqs']} "
          f"gx*={e['gx_star']} heur_ab={e['heur_ab']:.4f} true_ab={e['true_ab']:.4f}")
    if summary["heur_fail_examples"]:
        P(f"  first failures (<1/2):")
        for e in summary["heur_fail_examples"][:10]:
            P(f"    n={e['n']} gens={e['gens']} gfreq={e['gfreq']} "
              f"gx*={e['gx_star']} heur_ab={e['heur_ab']:.4f} "
              f"true_ab={e['true_ab']:.4f} true_x={e['true_x']}")
    P("")
    P("-" * 72)
    P("(b) ASYMMETRIC WEIGHTED 'abundance' statistics (generator-dependent w):")
    P("-" * 72)
    for key, label in (("w_size", "w(g)=|g|"),
                       ("w_invsize", "w(g)=1/|g|"),
                       ("w_filt", "w(g)=|↑g| in L"),
                       ("w_lc", "w(g)=1+#{gens ⊊ g}")):
        ex = summary[key + "_min_ex"]
        P(f"  {label:24s} : min over families = {summary[key+'_min']:.6f}, "
          f"#(<1/2) = {summary[key+'_fail']}")
        if ex:
            P(f"        worst: gens={ex['gens']} freqs={ex['freqs']} "
              f"val={ex['val']:.4f} true_ab={ex['true_ab']:.4f}")
    P("")
    P("-" * 72)
    P("(b+c) COMBINED NON-SYMMETRIC PICK RULE  [EXTRAORDINARY — PRESUMED FLAWED]")
    P("      singleton-generator branch (PROVABLE)  /  invsize-argmax branch (UNPROVEN)")
    P("-" * 72)
    P(f"  combined rule over all {summary['total']} families:")
    P(f"    #fail(<1/2): {summary['comb_fail']}    min pick-abundance: {summary['comb_min']:.6f}"
      f"    #equality(=1/2): {summary['comb_eq_count']}")
    if summary["comb_min_ex"]:
        e = summary["comb_min_ex"]
        P(f"    worst: gens={e['gens']} freqs={e['freqs']} pick={e['pick']} ab={e['comb_ab']:.4f}")
    P(f"  singleton branch: {summary['singleton_total']} families, "
      f"#fail={summary['singleton_fail']}, min={summary['singleton_min']:.6f}  "
      "(provable: {x}∈F ⇒ freq(x)≥|F|/2 via A↦A∪{x})")
    P(f"  invsize branch (no-singleton): {summary['nosingleton_total']} families, "
      f"#fail={summary['iv_nosingleton_fail']}, min={summary['iv_nosingleton_min']:.6f}  "
      "(NO PROOF — heuristic)")
    if summary["iv_nosingleton_fail_ex"]:
        P("    invsize-branch FAILURES (none expected on n<=5):")
        for e in summary["iv_nosingleton_fail_ex"][:10]:
            P(f"      n={e['n']} gens={e['gens']} freqs={e['freqs']} "
              f"pick={e['pick']} iv_ab={e['iv_ab']:.4f}")
    P("")
    P("-" * 72)
    P("DISCIPLINE GATE — Boolean cubes 2^[k] (must be EXACTLY 1/2 if a proof):")
    P("-" * 72)
    for c in summary["cube_checks"]:
        P(f"  k={c['k']} m={c['m']} ngens={c['ngens']} true_ab={c['true_ab']:.6f} "
          f"comb_ab={c['comb_ab']:.6f} heur_ab={c['heur_ab']:.6f} "
          f"w_size={c['w_size_v']:.6f} w_invsize={c['w_invsize_v']:.6f} "
          f"w_filt={c['w_filt_v']:.6f} w_lc={c['w_lc_v']:.6f}")
    P("=" * 72)

    text = "\n".join(lines)
    with open("data/genattack_summary.txt", "w") as fh:
        fh.write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
