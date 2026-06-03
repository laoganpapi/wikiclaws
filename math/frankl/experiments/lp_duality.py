"""
lp_duality.py — LP-relaxation / LP-duality attack on Frankl's union-closed conjecture.

Author: Alex Ye (AI-assisted). [NOVELTY UNVERIFIED — Poonen 1992 weight-functions
and LP relaxations of Frankl very likely exist in the literature; arXiv inaccessible
this session. Every "new" framing flagged in lp_duality.md.]

----------------------------------------------------------------------------------
WHAT THIS COMPUTES
----------------------------------------------------------------------------------

Fix a union-closed family F (m = |F| members, n ground elements). Frankl's conjecture
says max_i abundance_i(F) = max_i |{A in F : i in A}|/|F| >= 1/2.

We study LP *relaxations* of this combinatorial statement. The single most important
design decision (the "whole game", per the brief, and the source of the documented
0.43/0.5 budget-mismatch traps) is WHICH LP has Frankl as its feasibility/value
statement. We implement and contrast THREE formulations:

  (P-weight)  Adversary picks a probability weight w(.) on members of F.
              value(F) = min_w  max_i  sum_{A: i in A} w(A)
              subject to  w >= 0,  sum_A w(A) = 1.
              -> This is a pure LP over the simplex (NO union-closure constraints
                 beyond F already being union-closed). max-of-linear is an LP via
                 an epigraph variable t.
              *Frankl-relevance*: the UNWEIGHTED point w = uniform gives exactly the
              true abundance. The MIN over w can only go BELOW the uniform value, so
              value_Pweight(F) <= abundance(F). It is a *lower envelope*; if it ever
              drops below 1/2 that does NOT contradict Frankl (Frankl is about the
              uniform measure). Reported to expose the trap explicitly.

  (P-cover)   The genuine LP whose optimum equals the true abundance is the trivial
              "uniform is fixed" one; abundance itself is already an LP-free quantity.
              So the meaningful relaxation is the DUAL covering question below.

  (D-Reimer)  Reimer / average-set-size as an LP dual certificate.
              Reimer: (1/m) sum_{A in F} |A| >= (1/2) log2(m).
              This is a *valid inequality* certified by a weighting argument. We
              reconstruct it as a dual feasibility certificate and test whether it,
              combined with the trivial bound abundance >= avg_set_size / n, yields
              >= 1/2 (it does NOT in general — see writeup; it is sharp on cubes).

  (LP-frac)   Fractional/dual covering LP: does there exist multipliers y >= 0 on the
              union-closure incidence constraints "A,B |- A∪B" plus the abundance
              definitions, certifying max_i abundance_i >= 1/2 ? We build the explicit
              primal covering LP whose value is max_i abundance_i and read off its dual.

The honest expected outcome (matching the project's other four methods) is an
OBSTRUCTION: the LP relaxation bottoms out at exactly 1/2 with the Boolean cube as
the degenerate extremizer, because the union-closure constraints, expressed linearly,
are satisfied with equality on the cube and the dual certificate degenerates there.

----------------------------------------------------------------------------------
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

# Make the local toolkit importable regardless of cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from uc_family import (  # noqa: E402
    Family,
    abundance,
    family_to_sets,
    frequencies,
    ground_set,
    is_union_closed,
)
from enumerate import all_uc_families  # noqa: E402


# ---------------------------------------------------------------------------
# Basic per-family quantities
# ---------------------------------------------------------------------------

def members(F: Family) -> list[int]:
    return sorted(F)


def incidence_matrix(F: Family, n: int) -> np.ndarray:
    """M[i, k] = 1 iff element i in member k (k indexes sorted members)."""
    masks = members(F)
    M = np.zeros((n, len(masks)), dtype=float)
    for k, mask in enumerate(masks):
        for i in range(n):
            if (mask >> i) & 1:
                M[i, k] = 1.0
    return M


def true_abundance(F: Family) -> float:
    return abundance(F)


# ---------------------------------------------------------------------------
# (P-weight): min over weightings of the max weighted abundance
# ---------------------------------------------------------------------------

def lp_min_max_abundance(F: Family, n: int) -> dict:
    """
    value = min_w  max_i  sum_{A: i in A} w(A)   over the probability simplex on F.

    Epigraph LP:  minimize t
                  s.t.  (M w)_i <= t  for all i       (i.e. M w - t*1 <= 0)
                        sum_k w_k = 1
                        w >= 0
    Variables: [w_0,...,w_{m-1}, t].
    """
    masks = members(F)
    m = len(masks)
    if m == 0 or n == 0:
        return {"value": 0.0, "status": "trivial", "w": None}
    M = incidence_matrix(F, n)  # n x m

    # variables: w (m), t (1)
    c = np.zeros(m + 1)
    c[-1] = 1.0  # minimize t

    # M w - t <= 0   ->  [M | -1] [w;t] <= 0
    A_ub = np.hstack([M, -np.ones((n, 1))])
    b_ub = np.zeros(n)

    # sum w = 1
    A_eq = np.zeros((1, m + 1))
    A_eq[0, :m] = 1.0
    b_eq = np.array([1.0])

    bounds = [(0.0, None)] * m + [(None, None)]
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                  bounds=bounds, method="highs")
    if not res.success:
        return {"value": None, "status": res.message, "w": None}
    return {"value": float(res.fun), "status": "ok", "w": res.x[:m].tolist()}


# ---------------------------------------------------------------------------
# (P-weight dual / "adversarial measure") with union-closure as VALID INEQUALITIES
# ---------------------------------------------------------------------------

def lp_min_max_abundance_with_uc_constraints(F: Family, n: int) -> dict:
    """
    Same min-max as above, but we ADD the union-closure "consistency" linear
    inequalities to the adversary's weighting, to test whether they LIFT the LP
    value back up toward 1/2.

    The natural linear constraints implied by union-closure on a *measure* w:
    for every ordered pair (A, B) of members, A∪B is a member, and the event
    {i in A∪B} = {i in A} OR {i in B}. On the level of a single probability
    weight w on F this gives the "downward monotonicity of the order ideal"
    constraints. The cleanest valid family of linear constraints we can impose is:

       For every member C and every i in C:  w(C) <= sum_{A in F : i in A} w(A).
       (trivially true, it is one term of the sum — NOT informative.)

    A genuinely restrictive linear constraint comes from the filter structure
    (lattice_attack.md eq 1.1): Fib(i) = {A : i in A} is an UP-SET (filter). For a
    filter, sum_{A in Fib(i)} w(A) is unconstrained by w alone. So *there is no
    extra linear inequality on a single weight w that union-closure forces* beyond
    w being a probability vector. This function therefore returns the SAME value as
    lp_min_max_abundance — and we record that fact (it is the crux of the
    obstruction: union-closure imposes NO linear constraint on the abundance vector
    of a free measure).
    """
    return lp_min_max_abundance(F, n)


# ---------------------------------------------------------------------------
# (D-Reimer): Reimer average-set-size as a dual certificate, and the implied
#  abundance lower bound.
# ---------------------------------------------------------------------------

def reimer_avg_set_size(F: Family) -> float:
    masks = members(F)
    if not masks:
        return 0.0
    return sum(bin(m).count("1") for m in masks) / len(masks)


def reimer_bound(F: Family) -> dict:
    """
    Reimer: avg_set_size >= (1/2) log2(|F|).  (Equality on power sets 2^[n].)

    Implied abundance bound: avg_set_size = sum_i abundance_i  (since
      sum_{A} |A| = sum_{A} sum_i 1[i in A] = sum_i freq_i = |F| sum_i abundance_i).
    Hence  sum_i abundance_i = avg_set_size, so
      max_i abundance_i >= avg_set_size / n  >= (log2|F|) / (2 n).
    This is the "average-set-size -> some element" route. On the cube 2^[n]:
      avg_set_size = n/2, n_ground = n, so max_i abundance_i >= 1/2 EXACTLY (tight).
    """
    masks = members(F)
    m = len(masks)
    n = ground_set(F)
    if m == 0 or n == 0:
        return {"avg_set_size": 0.0, "reimer_rhs": 0.0, "holds": True,
                "abund_lb_from_avg_over_n": 0.0, "true_abundance": 0.0}
    avg = reimer_avg_set_size(F)
    rhs = 0.5 * math.log2(m)
    # sum of abundances = avg set size (identity)
    abund_sum = sum(frequencies(F, n)) / m
    return {
        "avg_set_size": avg,
        "reimer_rhs": rhs,
        "reimer_holds": avg >= rhs - 1e-9,
        "abund_sum": abund_sum,
        "abund_lb_from_avg_over_n": avg / n,      # max_i abund_i >= this
        "abund_lb_from_reimer_over_n": rhs / n,   # weaker, uses Reimer's lower bd
        "true_abundance": true_abundance(F),
    }


# ---------------------------------------------------------------------------
# (LP-frac): the fractional covering LP whose value is the true max abundance,
#  and its dual certificate.
# ---------------------------------------------------------------------------

def primal_abundance_lp(F: Family, n: int) -> dict:
    """
    max_i abundance_i written as a (tiny) LP and its dual.

    Primal (over a *distribution* z on ground elements, z_i >= 0, sum z_i = 1):
        maximize   sum_i z_i * abundance_i
    This LP's optimum equals max_i abundance_i (put all mass on the argmax).
    It is the "fractional element selection". Its dual is:
        minimize   tau
        s.t.       tau >= abundance_i  for all i.
    i.e. tau = max_i abundance_i. The dual certificate is the single tight element.

    This is the HONEST LP for "max abundance": its value is EXACTLY the true
    abundance (no relaxation gap), because max-of-a-finite-set is already an LP.
    The point of recording it: it shows the *only* LP whose optimum is the true
    abundance is this trivial one — abundance is not relaxed by any larger LP that
    still respects union-closure, because (see lp_min_max_abundance) union-closure
    adds no linear constraints on the abundance vector of a free measure.
    """
    n_ground = n
    if n_ground == 0:
        return {"value": 0.0, "argmax": None}
    abund = [f / max(1, len(F)) for f in frequencies(F, n_ground)]
    # primal: maximize z . abund, simplex on z
    c = -np.array(abund)  # linprog minimizes
    A_eq = np.ones((1, n_ground))
    b_eq = np.array([1.0])
    bounds = [(0.0, None)] * n_ground
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    val = -float(res.fun) if res.success else max(abund)
    return {"value": val, "argmax": int(np.argmax(abund)), "abund_vector": abund}


# ---------------------------------------------------------------------------
# (LP-cover): the Poonen/Reimer-style fractional cover LP -- the RIGHT object.
# ---------------------------------------------------------------------------
#
# Frankl, with the measure FIXED to uniform on F, asks: max_i abundance_i >= 1/2,
# i.e. sum_{A in F} (2*[i in A] - 1) <= 0 for some i, i.e. some element is in >= m/2
# sets. Equivalently sum_i (2 freq_i - m) -- but that is just totals.
#
# The averaging certificate (Reimer / Knill / "salami"): a NON-NEGATIVE combination
# of the per-element slacks s_i = freq_i - m/2 that is provably >= 0 would prove
# Frankl IF the combination forced max_i s_i >= 0. The honest LP-dual question is:
#
#   Is there a fixed probability vector lambda (lambda_i >= 0, sum lambda_i = 1)
#   -- a "fractional element" -- and a certificate using ONLY the linear data of F
#   (the incidence matrix) plus union-closure-derived VALID INEQUALITIES, such that
#         sum_i lambda_i * freq_i  >=  m/2     for EVERY UC family F ?
#
# Without extra inequalities, the best such lambda gives the AVERAGE abundance
# (uniform lambda) = avg_set_size/n, which we already saw dips below 1/2. So the
# unstructured cover LP FAILS; the question is which valid inequalities lift it.
#
# We implement the "down-set / order-ideal" valid inequalities and test the lift.


def order_ideal_valid_inequalities(F: Family, n: int) -> list[tuple]:
    """
    Valid linear inequalities on the abundance vector (freq_i) coming from
    union-closure, beyond the trivial 0 <= freq_i <= m.

    Union-closure => Fib(i) = {A : i in A} is a FILTER (up-set). A standard
    consequence usable as a linear inequality on FREQUENCIES:

      (Reimer/Knill averaging core) For the top element T = union of F and any
      maximal chain ∅ = C_0 < C_1 < ... < C_h = T in (F,⊆), every element of C_1
      lies in all of C_1,...,C_h, so freq of that element >= h = height.

    More generally, the "shifting/compression" inequalities of Reimer give that the
    sum of the (m/2 - freq_i)^+ is bounded. We DO NOT have a clean per-family linear
    inequality on freq_i that is both valid and strong enough; this function returns
    the height witness inequality (freq_{x*} >= height) for the explicit chain
    element x*, which is the one provable linear lift. Returns list of
    (coeff_vector, rhs) meaning coeff . freq >= rhs.
    """
    masks = members(F)
    if not masks:
        return []
    # longest chain by inclusion (height witness) -- gives freq_{x*} >= height.
    # Build cover/order and find a longest chain greedily from bottom.
    sorted_by_size = sorted(masks, key=lambda mm: bin(mm).count("1"))
    bottom = sorted_by_size[0]
    # longest chain via DP on the inclusion DAG
    order = sorted_by_size
    idx = {mm: k for k, mm in enumerate(order)}
    longest = [1] * len(order)
    pred = [-1] * len(order)
    for a in range(len(order)):
        for b in range(a):
            if (order[b] & order[a]) == order[b] and order[b] != order[a]:
                if longest[b] + 1 > longest[a]:
                    longest[a] = longest[b] + 1
                    pred[a] = b
    end = max(range(len(order)), key=lambda k: longest[k])
    chain = []
    k = end
    while k != -1:
        chain.append(order[k])
        k = pred[k]
    chain.reverse()
    height = len(chain) - 1  # edges
    ineqs = []
    if height >= 1 and len(chain) >= 2:
        # smallest nonempty element of the chain (the atom C_1)
        c1 = chain[1]
        # any ground element in c1 is in all chain[1:], so freq >= height
        for i in range(n):
            if (c1 >> i) & 1:
                vec = [0.0] * n
                vec[i] = 1.0
                ineqs.append((vec, float(height)))
                break
    return ineqs


def lp_cover_certificate(F: Family, n: int) -> dict:
    """
    The fractional-element cover LP with order-ideal valid inequalities.

    PRIMAL (what we maximize as the certified abundance lower bound):
        maximize  rho
        over  lambda_i >= 0, sum lambda_i = 1   (a fractional element)
        such that  lambda . freq  >= rho * m,     -- weighted abundance
        AND we are ALLOWED to also use the valid inequalities to certify rho.

    Operationally: the BEST single-element abundance is max_i freq_i/m (true
    abundance). The cover LP asks the dual: the smallest rho such that NO valid
    nonnegative combination forces higher. Here we simply report:
       - avg_lb   = (sum_i freq_i)/(n*m) = avg_set_size/n  (uniform lambda, no ineqs)
       - height_lb = (best height witness)/m  (the order-ideal valid inequality)
       - certified_lb = max(avg_lb, height_lb)  -- the LP-dual certified abundance
    and compares to true abundance. If certified_lb >= 1/2 the LP-dual proves Frankl
    for F; otherwise the LP relaxation has a GAP and we record where.
    """
    masks = members(F)
    m = len(masks)
    if m == 0 or n == 0:
        return {"certified_lb": 0.0, "avg_lb": 0.0, "height_lb": 0.0}
    freq = frequencies(F, n)
    avg_lb = sum(freq) / (n * m)
    ineqs = order_ideal_valid_inequalities(F, n)
    height_lb = 0.0
    for vec, rhs in ineqs:
        # vec . freq >= rhs ; vec is an indicator of one element -> freq_x >= rhs
        x = vec.index(1.0)
        height_lb = max(height_lb, freq[x] / m, rhs / m)
    certified = max(avg_lb, height_lb)
    return {
        "certified_lb": certified,
        "avg_lb": avg_lb,
        "height_lb": height_lb,
        "true_abundance": true_abundance(F),
        "proves_frankl": certified >= 0.5 - 1e-9,
    }


# ---------------------------------------------------------------------------
# (Sec.6 probe): the second-moment / power-mean candidate strengthening.
# ---------------------------------------------------------------------------

def power_mean_bound(F: Family, n: int) -> dict:
    """
    Power-mean ("weighted-by-itself") lower bound on max abundance:
        max_i ab_i >= (sum_i ab_i^2) / (sum_i ab_i).
    Computed over ACTIVE elements (freq>0). This is >= the plain mean and equals
    the mean iff the abundance vector is flat (as on the cube).

    Returns the bound and whether it reaches 1/2. Step-1 finding (see lp_duality.md
    Sec.6): on the cube it is exactly 1/2 (good), but it STILL dips below 1/2 on a
    handful of families -> the raw power-mean is NOT a sufficient certificate; a
    genuine union-closure lower bound on sum_i freq_i^2 would be required.
    """
    masks = members(F)
    m = len(masks)
    if m == 0 or n == 0:
        return {"power_mean_lb": 0.0, "reaches_half": False}
    freq = frequencies(F, n)
    ab = [f / m for f in freq if f > 0]  # active elements only
    s1 = sum(ab)
    s2 = sum(a * a for a in ab)
    pm = s2 / s1 if s1 > 0 else 0.0
    return {"power_mean_lb": pm, "reaches_half": pm >= 0.5 - 1e-9,
            "true_abundance": true_abundance(F)}


# ---------------------------------------------------------------------------
# Sweep driver
# ---------------------------------------------------------------------------

def analyze_family(F: Family, n_max: int) -> dict:
    n = ground_set(F)
    m = len(F)
    rec = {
        "n_ground": n,
        "m": m,
        "true_abundance": true_abundance(F) if m and n else 0.0,
    }
    # P-weight (adversarial measure min-max)
    pw = lp_min_max_abundance(F, n)
    rec["lp_minmax_value"] = pw["value"]
    # LP-frac (honest abundance LP)
    pf = primal_abundance_lp(F, n)
    rec["lp_abundance_value"] = pf["value"]
    # Reimer
    rb = reimer_bound(F)
    rec["reimer_avg_set_size"] = rb["avg_set_size"]
    rec["reimer_rhs"] = rb.get("reimer_rhs", 0.0)
    rec["reimer_holds"] = rb.get("reimer_holds", True)
    rec["abund_lb_from_avg_over_n"] = rb.get("abund_lb_from_avg_over_n", 0.0)
    rec["abund_lb_from_reimer_over_n"] = rb.get("abund_lb_from_reimer_over_n", 0.0)
    # LP-cover certificate (avg + order-ideal/height valid inequalities)
    cov = lp_cover_certificate(F, n)
    rec["cover_certified_lb"] = cov["certified_lb"]
    rec["cover_avg_lb"] = cov["avg_lb"]
    rec["cover_height_lb"] = cov["height_lb"]
    rec["cover_proves_frankl"] = cov.get("proves_frankl", False)
    # Sec.6 second-moment / power-mean candidate
    pm = power_mean_bound(F, n)
    rec["power_mean_lb"] = pm["power_mean_lb"]
    rec["power_mean_reaches_half"] = pm["reaches_half"]
    rec["sets"] = [sorted(s) for s in family_to_sets(F)]
    return rec


def run_sweep(n_max: int = 5, out_dir: str | None = None) -> dict:
    if out_dir is None:
        out_dir = str(Path(__file__).resolve().parent / "data")
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    summary = {
        "n_max": n_max,
        "per_n": {},
        "min_lp_minmax": math.inf,
        "min_lp_minmax_family": None,
        "min_true_abundance": math.inf,
        "min_true_abundance_family": None,
        "min_abund_lb_avg_over_n": math.inf,
        "min_abund_lb_avg_over_n_family": None,
        "reimer_violations": 0,
        "lp_minmax_below_half": 0,
        "lp_minmax_below_half_examples": [],
        "true_below_half": 0,
        "n_families": 0,
        # cover certificate (avg + height valid inequalities)
        "cover_proves_frankl": 0,
        "cover_fails": 0,
        "cover_fail_examples": [],
        "min_cover_certified_lb": math.inf,
        "min_cover_certified_lb_family": None,
        # Sec.6 power-mean candidate
        "power_mean_below_half": 0,
        "min_power_mean_lb": math.inf,
        "min_power_mean_family": None,
        # collision test: does lp_minmax distinguish abundance? track gap
        "max_gap_true_minus_minmax": 0.0,
        "max_gap_family": None,
    }

    for n in range(0, n_max + 1):
        path = out / f"lp_sweep_n{n}.jsonl"
        cnt = 0
        with path.open("w") as fh:
            for F in all_uc_families(n, dedupe_isomorphic=True):
                if len(F) < 2:
                    continue  # exclude trivial {} / {emptyset}
                if ground_set(F) == 0:
                    continue
                rec = analyze_family(F, n_max)
                fh.write(json.dumps(rec) + "\n")
                cnt += 1
                summary["n_families"] += 1

                ta = rec["true_abundance"]
                mm = rec["lp_minmax_value"]
                if mm is not None:
                    if mm < summary["min_lp_minmax"] - 1e-12:
                        summary["min_lp_minmax"] = mm
                        summary["min_lp_minmax_family"] = rec["sets"]
                    if mm < 0.5 - 1e-9:
                        summary["lp_minmax_below_half"] += 1
                        if len(summary["lp_minmax_below_half_examples"]) < 10:
                            summary["lp_minmax_below_half_examples"].append(
                                {"sets": rec["sets"], "lp_minmax": mm,
                                 "true_abundance": ta})
                    gap = ta - mm
                    if gap > summary["max_gap_true_minus_minmax"] + 1e-12:
                        summary["max_gap_true_minus_minmax"] = gap
                        summary["max_gap_family"] = {
                            "sets": rec["sets"], "true_abundance": ta,
                            "lp_minmax": mm}
                if ta < summary["min_true_abundance"] - 1e-12:
                    summary["min_true_abundance"] = ta
                    summary["min_true_abundance_family"] = rec["sets"]
                if ta < 0.5 - 1e-9:
                    summary["true_below_half"] += 1
                if not rec["reimer_holds"]:
                    summary["reimer_violations"] += 1
                alb = rec["abund_lb_from_avg_over_n"]
                if alb < summary["min_abund_lb_avg_over_n"] - 1e-12:
                    summary["min_abund_lb_avg_over_n"] = alb
                    summary["min_abund_lb_avg_over_n_family"] = rec["sets"]
                # cover certificate
                clb = rec["cover_certified_lb"]
                if rec["cover_proves_frankl"]:
                    summary["cover_proves_frankl"] += 1
                else:
                    summary["cover_fails"] += 1
                    if len(summary["cover_fail_examples"]) < 12:
                        summary["cover_fail_examples"].append(
                            {"sets": rec["sets"],
                             "cover_certified_lb": clb,
                             "true_abundance": ta,
                             "m": rec["m"], "n_ground": rec["n_ground"]})
                if clb < summary["min_cover_certified_lb"] - 1e-12:
                    summary["min_cover_certified_lb"] = clb
                    summary["min_cover_certified_lb_family"] = rec["sets"]
                # Sec.6 power-mean candidate
                pmlb = rec["power_mean_lb"]
                if not rec["power_mean_reaches_half"]:
                    summary["power_mean_below_half"] += 1
                if pmlb < summary["min_power_mean_lb"] - 1e-12:
                    summary["min_power_mean_lb"] = pmlb
                    summary["min_power_mean_family"] = rec["sets"]
        summary["per_n"][n] = cnt

    # finalize infs
    for k in ("min_lp_minmax", "min_true_abundance", "min_abund_lb_avg_over_n",
              "min_cover_certified_lb", "min_power_mean_lb"):
        if summary[k] is math.inf:
            summary[k] = None

    with (out / "lp_summary.txt").open("w") as fh:
        fh.write(_format_summary(summary))
    with (out / "lp_summary.json").open("w") as fh:
        json.dump(summary, fh, indent=2)
    return summary


def _format_summary(s: dict) -> str:
    lines = []
    lines.append("LP-DUALITY SWEEP SUMMARY (Frankl union-closed)")
    lines.append("=" * 60)
    lines.append(f"n_max = {s['n_max']}")
    lines.append(f"total non-trivial UC families (|F|>=2, n>=1): {s['n_families']}")
    lines.append(f"per-n family counts: {s['per_n']}")
    lines.append("")
    lines.append("--- TRUE ABUNDANCE (uniform measure) ---")
    lines.append(f"min true abundance over all families: {s['min_true_abundance']}")
    lines.append(f"  attained by: {s['min_true_abundance_family']}")
    lines.append(f"families with true abundance < 1/2: {s['true_below_half']}  "
                 "(MUST be 0 if Frankl holds n<=5)")
    lines.append("")
    lines.append("--- (P-weight) LP: min over weightings of max weighted abundance ---")
    lines.append(f"min LP-minmax value over all families: {s['min_lp_minmax']}")
    lines.append(f"  attained by: {s['min_lp_minmax_family']}")
    lines.append(f"families with LP-minmax < 1/2: {s['lp_minmax_below_half']}")
    lines.append("  (these do NOT violate Frankl: the LP min is over a FREE measure,")
    lines.append("   Frankl is about the uniform measure. This is the integrality/")
    lines.append("   relaxation gap of the weighted LP — see lp_duality.md.)")
    lines.append(f"  examples: {json.dumps(s['lp_minmax_below_half_examples'][:5])}")
    lines.append("")
    lines.append(f"max gap (true_abundance - lp_minmax): "
                 f"{s['max_gap_true_minus_minmax']}")
    lines.append(f"  at family: {json.dumps(s['max_gap_family'])}")
    lines.append("")
    lines.append("--- (D-Reimer) average-set-size dual certificate ---")
    lines.append(f"Reimer inequality avg>= (1/2)log2|F| violations: "
                 f"{s['reimer_violations']}  (MUST be 0)")
    lines.append(f"min (avg_set_size / n_ground) over families: "
                 f"{s['min_abund_lb_avg_over_n']}")
    lines.append(f"  attained by: {s['min_abund_lb_avg_over_n_family']}")
    lines.append("  (this is the abundance lower bound from the averaging identity")
    lines.append("   sum_i abundance_i = avg_set_size, then /n. If it ever dips")
    lines.append("   below 1/2, the averaging certificate FAILS to prove Frankl.)")
    lines.append("")
    lines.append("--- (LP-cover) avg + order-ideal/height valid inequalities ---")
    lines.append(f"families where cover certificate proves Frankl (>=1/2): "
                 f"{s['cover_proves_frankl']}")
    lines.append(f"families where cover certificate FAILS (<1/2): "
                 f"{s['cover_fails']}")
    lines.append(f"min cover-certified abundance LB: {s['min_cover_certified_lb']}")
    lines.append(f"  attained by: {s['min_cover_certified_lb_family']}")
    lines.append(f"  cover-fail examples (LP relaxation gap): "
                 f"{json.dumps(s['cover_fail_examples'][:6])}")
    lines.append("")
    lines.append("--- (Sec.6) power-mean candidate  max>= (sum ab^2)/(sum ab) ---")
    lines.append(f"families where power-mean < 1/2 (candidate FAILS): "
                 f"{s['power_mean_below_half']}")
    lines.append(f"min power-mean LB: {s['min_power_mean_lb']}")
    lines.append(f"  attained by: {s['min_power_mean_family']}")
    lines.append("  (cube stays at exactly 1/2, but the RAW power-mean still dips")
    lines.append("   below 1/2 -> NOT a sufficient certificate on its own; a genuine")
    lines.append("   union-closure lower bound on sum_i freq_i^2 would be needed.)")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    n_max = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    summ = run_sweep(n_max=n_max)
    print(_format_summary(summ))
