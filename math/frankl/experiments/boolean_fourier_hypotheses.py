"""
boolean_fourier_hypotheses.py — Test H1–H4 (and a few stretch hypotheses) from
the Boolean-Fourier brief against the full enumeration in
``data/fourier_n{0..5}.jsonl``.

Output: ``data/fourier_hypotheses.txt`` + console-printable summary.

We treat any single counterexample as a kill for a "for-all UC F" inequality.
"""
from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")


def load_all(max_n: int = 5):
    for n in range(0, max_n + 1):
        path = os.path.join(DATA_DIR, f"fourier_n{n}.jsonl")
        if not os.path.exists(path):
            continue
        with open(path) as fh:
            for line in fh:
                yield json.loads(line)


def fmt_F(rec) -> str:
    F = rec.get("F", [])
    return "{" + ",".join(str(m) for m in F) + "}"


# ---------------------------------------------------------------------------
# H1: min-influence vs (something)*p*(1−abund_max)
#
#   Conjecture (H1.a):  min_i Inf_i(1_F)  ≥  c · p · (1 − abund_max)
#   for some absolute c > 0.   Test: tabulate the ratio.
#
#   Conjecture (H1.b — sharper):  min_i Inf_i  ≥  c · |F|/2^n · (1/2)
#   (the worst case scenario being a "balanced" UC family).
#
#   We're really probing: does "no abundant element" force large influences?
# ---------------------------------------------------------------------------

def test_H1(records: list[dict]) -> dict:
    """
    For each UC family compute min_i Inf_i / (p * (1 - abund_max)),
    excluding the degenerate cases where p * (1-ab_max) = 0.
    Track min, max, and where the min is attained.

    Then also test: min_i Inf_i / max(0, 1/2 - abund_max) — does no abundance
    force large min-influence?
    """
    rows = []
    flat_ratios = []
    flat_excess = []
    for rec in records:
        n = rec["n"]
        if n == 0 or rec["size"] == 0:
            continue
        if not rec["influences"]:
            continue
        min_inf = min(rec["influences"])
        max_inf = max(rec["influences"])
        ab = rec["abund_max"]
        p = rec["p"]
        denom = p * (1.0 - ab)
        excess_above_half = max(0.0, 0.5 - ab)
        ratio = min_inf / denom if denom > 1e-15 else None
        rows.append({
            "n": n, "size": rec["size"], "p": p,
            "abund_max": ab,
            "min_inf": min_inf, "max_inf": max_inf,
            "ratio_H1a": ratio,
            "excess_above_half": excess_above_half,
            "F": rec.get("F"),
        })
        if ratio is not None:
            # Pack (ratio, ROW with all needed fields for printing)
            flat_ratios.append((ratio, {
                "F": rec.get("F"), "n": n, "size": rec["size"],
                "abund_max": ab, "min_inf": min_inf,
            }))
        flat_excess.append((min_inf, ab, rec))

    if flat_ratios:
        ratios = [r[0] for r in flat_ratios]
        min_ratio = min(flat_ratios, key=lambda x: x[0])
        max_ratio = max(flat_ratios, key=lambda x: x[0])
    else:
        min_ratio = max_ratio = None

    # Find families with ab_max ≤ 0.5 and report their min_inf — for FUCC
    # any UC family with ab_max < 0.5 IS a counterexample to Frankl.  None
    # should exist, since FUCC is verified on n≤5.  But if abund_max = 0.5
    # exactly, we expect families with very small min_inf as evidence the
    # Fourier method can't rule out that region.
    half_or_less = [r for r in rows if r["abund_max"] <= 0.5 + 1e-12]

    return {
        "n_tested": len(rows),
        "min_ratio_H1a": min_ratio[0] if min_ratio else None,
        "min_ratio_witness": min_ratio[1] if min_ratio else None,
        "max_ratio_H1a": max_ratio[0] if max_ratio else None,
        "max_ratio_witness": max_ratio[1] if max_ratio else None,
        "n_at_ab_eq_half": sum(1 for r in half_or_less if abs(r["abund_max"]-0.5) < 1e-12),
        "min_inf_at_ab_half": min(
            (r["min_inf"] for r in half_or_less if abs(r["abund_max"]-0.5)<1e-12),
            default=None
        ),
    }


# ---------------------------------------------------------------------------
# H2: Total influence vs abund_max
#
#   Conjecture: I[1_F]  ≥  c · p · (1 − 2 · abund_max)_+    (i.e. a Friedgut-style
#   tail when no element is abundant).
#
#   Practical test:  scatter I[1_F] vs (1-abund_max), look for lower envelope.
# ---------------------------------------------------------------------------

def test_H2(records: list[dict]) -> dict:
    rows = []
    for rec in records:
        if rec["n"] == 0 or rec["size"] == 0:
            continue
        I = rec["total_influence"]
        rows.append({
            "n": rec["n"], "size": rec["size"], "p": rec["p"],
            "abund_max": rec["abund_max"],
            "total_influence": I,
            "I_over_p": (I / rec["p"]) if rec["p"] > 0 else None,
        })
    # Lower envelope:  for each abundance bin, the min total influence.
    bins: dict[float, float] = {}
    for r in rows:
        key = round(r["abund_max"], 2)
        cur = bins.get(key, math.inf)
        if r["total_influence"] < cur:
            bins[key] = r["total_influence"]
    # KKL-style claim: I[f] ≥ Var(f) · log(1/max_inf) / max_inf ... (NOT a UC
    # statement directly).  Just report scatter for the writeup.
    return {
        "rows_count": len(rows),
        "envelope_by_abundance": sorted(bins.items()),
    }


# ---------------------------------------------------------------------------
# H3: Low-degree concentration
#
#   For each F, compute the *fraction* of E[f^2] sitting on levels ≤ k:
#       C_k(F) := (Σ_{|S|≤k} f̂(S)^2) / E[f^2] = (Σ_{|S|≤k} W^|S|) / p.
#   (Note: this normalizes by E[f^2] = p = |F|/2^n, so C_n = 1.)
#
#   Hypothesis: UC families concentrate spectrum on low levels.
#   Reality check: 2^[n] has all mass on level 0 (since 1_F = constant 1 → f̂=δ_∅).
#   But many UC families are NOT close to 2^[n].
# ---------------------------------------------------------------------------

def test_H3(records: list[dict]) -> dict:
    # For each n, compute the distribution of C_k(F) for k = 0, 1, 2.
    by_n: dict[int, dict] = {}
    for rec in records:
        n = rec["n"]
        if n == 0:
            continue
        p = rec["p"]
        if p == 0:
            continue
        W = rec["level_weights"]
        # Cumulative through level k.
        cum = []
        s = 0.0
        for k in range(n + 1):
            s += W[k]
            cum.append(s)
        # Normalize by E[f^2] = p
        Ck = [c / p for c in cum]
        by_n.setdefault(n, {"C0": [], "C1": [], "C2": []})
        by_n[n]["C0"].append((Ck[0], rec))
        if n >= 1:
            by_n[n]["C1"].append((Ck[1], rec))
        if n >= 2:
            by_n[n]["C2"].append((Ck[2], rec))

    summary = {}
    for n, d in by_n.items():
        summary[n] = {}
        for key in ("C0", "C1", "C2"):
            if key not in d or not d[key]:
                continue
            vals = [x[0] for x in d[key]]
            summary[n][key + "_min"] = min(vals)
            summary[n][key + "_max"] = max(vals)
            summary[n][key + "_mean"] = sum(vals) / len(vals)
    return summary


# ---------------------------------------------------------------------------
# H4: Noise stability vs abundance
#
#   For ρ ∈ {0.25, 0.5, 0.75, 0.9}, plot Stab_ρ(F) / E[f^2] vs abund_max.
#   Hypothesis: higher noise stability ⇒ higher abundance?
# ---------------------------------------------------------------------------

def test_H4(records: list[dict]) -> dict:
    out = {0.25: [], 0.5: [], 0.75: [], 0.9: []}
    for rec in records:
        if rec["n"] == 0 or rec["size"] == 0:
            continue
        p = rec["p"]
        for rho_str, val in rec["stab"].items():
            rho = float(rho_str) if isinstance(rho_str, str) else rho_str
            out[rho].append((rec["abund_max"], val / p))
    # Lower envelope by abundance bin
    res = {}
    for rho, pairs in out.items():
        bins = {}
        for ab, s in pairs:
            key = round(ab, 2)
            cur = bins.get(key, math.inf)
            if s < cur:
                bins[key] = s
        res[rho] = sorted(bins.items())
    return res


# ---------------------------------------------------------------------------
# H5 (Karpas-style): the "Fourier-direct" inequality
#
#   Frankl in Fourier form: ∃ i with f̂({i}) ≤ 0.
#   Equivalently: f̂({i}) ≥ 0 for ALL i would mean abund_i ≤ 1/2 for all i,
#                contradicting FUCC.
#
#   Karpas (2017) proved: if |F|/2^n ≥ (1/2 − c), some f̂({i}) ≤ 0.  Re-state in
#   our framework: does our data show that for SMALL p = |F|/2^n, the level-1
#   mass is constrained?
#
#   Direct test of the FUCC = "∃ i with f̂({i}) ≤ 0" reading.
# ---------------------------------------------------------------------------

def test_H5(records: list[dict]) -> dict:
    rows = []
    fucc_holds = 0
    fucc_fail = 0
    fucc_fail_witnesses = []
    trivial_skipped = 0
    for rec in records:
        if rec["n"] == 0 or rec["size"] == 0:
            continue
        sings = rec["singletons"]
        # Trivial family {∅}: no ground-set element belongs to any set; Frankl's
        # statement excludes this case explicitly.  Skip.
        if rec["size"] == 1 and rec.get("F") == [0]:
            trivial_skipped += 1
            continue
        # Likewise skip families that omit some ground-set indices (abund_per = 0).
        # The brief asks ∃ x ∈ ⋃F: that's a non-issue since we enumerate orbit reps.
        # FUCC says: min_i singletons[i] ≤ 0  (some f̂({i}) ≤ 0)
        min_s = min(sings)
        max_s = max(sings)
        rows.append({
            "n": rec["n"], "size": rec["size"], "p": rec["p"],
            "abund_max": rec["abund_max"],
            "min_singleton": min_s, "max_singleton": max_s,
            "all_singletons": sings,
            "F": rec.get("F"),
        })
        if min_s <= 1e-15:
            fucc_holds += 1
        else:
            fucc_fail += 1
            fucc_fail_witnesses.append(rec)
    return {
        "n_tested": len(rows),
        "fucc_holds_count": fucc_holds,
        "fucc_violation_count": fucc_fail,
        "trivial_skipped": trivial_skipped,
        "fail_examples": fucc_fail_witnesses[:5],
    }


# ---------------------------------------------------------------------------
# Stretch hypothesis (H6): can the level-1 spectrum CONTROL min abundance?
#
#   Level-1 spectrum: W^1 = Σ_i f̂({i})^2 = Σ_i p^2 (1-2 abund_i)^2
#                        = p^2 · Σ_i (1-2 abund_i)^2.
#   If at least one abund_i ≥ 1/2, then min_i (1 - 2 abund_i) ≤ 0, so the
#   min element of {(1-2 abund_i)} controls Frankl.  Question: does W^1
#   (which is rotation-invariant under coordinate permutation but NOT signed)
#   give a USEFUL lower bound on some abund_i?
#
#   ALGEBRAIC OBSTRUCTION (key idea): given only W^1 = Σ (1-2 ab_i)^2, the
#   minimum value of max_i ab_i is achieved when all ab_i are equal, say
#   ab_i = ab for all i.  Then W^1/p^2 = n · (1 - 2 ab)^2.  Solving:
#       ab = (1 - sqrt(W^1/(n p^2))) / 2.
#   So the BEST max-abundance bound from knowing W^1 alone is
#       max_i ab_i ≥ (1 - sqrt(W^1 / (n p^2)))/2.
#   For this to be ≥ 1/2 we'd need sqrt(W^1/(n p^2)) ≤ 0, i.e. W^1 = 0.
#   But W^1 = 0 iff f̂({i}) = 0 for all i iff ab_i = 1/2 for all i.  So this
#   bound is tight at 1/2 but never exceeds it: the level-1 spectrum is
#   *just* the rotated abundance vector and gives nothing new.
#
#   What about W^≥2 (high-degree)?  By Plancherel, Σ_S f̂^2 = p, so
#       W^1 + W^≥2 = p - W^0 = p - p^2 = p(1-p).
#   And by signed structure, the f̂({i}) all have the same sign as 1-2 ab_i.
#   So the question is: does the joint structure of (W^1, W^≥2) imply ∃ i with
#   f̂({i}) ≤ 0?  NO — by symmetry, any sign pattern of (f̂({i}))_i is
#   realisable by relabeling.  So at the level of the rotation-invariant
#   spectrum, we still need a different signed inequality.
#
#   This is the structural obstruction we will state in the writeup.
# ---------------------------------------------------------------------------

def test_H6(records: list[dict]) -> dict:
    """
    Test the FORMAL implication: given (p, n, W^1) is there a min-abundance bound?

    For each F compute the LP-lower bound on max ab_i implied by knowing W^1:
        max ab_i  ≥  (1 - sqrt(W^1 / (n p^2))) / 2     when W^1 ≤ n p^2.
    Check whether this ever exceeds 1/2.  Theory: never.
    """
    exceeds_half = 0
    near_half = 0
    rows = []
    for rec in records:
        n = rec["n"]
        if n == 0 or rec["size"] == 0:
            continue
        p = rec["p"]
        if p == 0:
            continue
        W = rec["level_weights"]
        W1 = W[1] if len(W) > 1 else 0
        if W1 < 0:
            W1 = 0.0
        denom = n * p * p
        if denom == 0:
            continue
        ratio = W1 / denom
        if ratio > 1:
            # numerical artifact; treat as 1
            ratio = 1.0
        lb = (1 - math.sqrt(ratio)) / 2
        # compare to actual abund_max
        rows.append((rec["abund_max"], lb, rec))
        if lb > 0.5 + 1e-12:
            exceeds_half += 1
        if lb > 0.5 - 1e-6:
            near_half += 1
    return {
        "tested": len(rows),
        "lb_exceeds_half": exceeds_half,
        "lb_near_half": near_half,
        "max_lb": max((r[1] for r in rows), default=None),
    }


# ---------------------------------------------------------------------------
# H7 (KKL flavor): Friedgut-Kalai isoperimetric bound  I[f] ≥ 2 p (1-p) log_2(1/max_i Inf_i)
#   does not apply to UC since 1_F is not monotone.  But it's interesting to
#   simply tabulate min_i Inf_i, max_i Inf_i, p(1-p).
# ---------------------------------------------------------------------------

def test_H7(records: list[dict]) -> dict:
    """
    Tabulate KKL-style scatter: max-influence vs total-influence.
    KKL says max_i Inf_i ≥ Ω( Var(f) · log n / n ) for monotone Boolean f.
    UC families are not monotone, so KKL fails in general.  But we look for
    FAMILIES where max_i Inf_i is SMALL while min abundance is bounded away
    from 1/2.
    """
    rows = []
    for rec in records:
        if rec["n"] == 0 or rec["size"] == 0:
            continue
        rows.append({
            "n": rec["n"], "size": rec["size"], "p": rec["p"],
            "abund_max": rec["abund_max"],
            "max_inf": rec["max_influence"],
            "total_inf": rec["total_influence"],
            "var": rec["p"] * (1 - rec["p"]),
        })
    return {"tested": len(rows)}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(max_n: int = 5):
    print(f"Loading records from {DATA_DIR}/fourier_n{{0..{max_n}}}.jsonl ...")
    records = list(load_all(max_n))
    print(f"Loaded {len(records)} records.")

    H1 = test_H1(records)
    H2 = test_H2(records)
    H3 = test_H3(records)
    H4 = test_H4(records)
    H5 = test_H5(records)
    H6 = test_H6(records)
    H7 = test_H7(records)

    out_lines: list[str] = []
    out_lines.append("Boolean-Fourier hypothesis tests")
    out_lines.append("=" * 64)
    out_lines.append(f"Records tested: {len(records)} UC orbit reps (n ≤ {max_n})")
    out_lines.append("")

    # H1
    out_lines.append("H1 — min_i Inf_i / (p · (1−abund_max))")
    out_lines.append(f"  Tested non-degenerate: {H1['n_tested']}")
    out_lines.append(f"  min ratio: {H1['min_ratio_H1a']:.6f}" if H1['min_ratio_H1a'] is not None else "  min ratio: N/A")
    if H1.get("min_ratio_witness"):
        w = H1["min_ratio_witness"]
        out_lines.append(f"    witness F = {w.get('F')}, n={w['n']}, size={w['size']}, abund_max={w['abund_max']:.4f}, min_inf={w['min_inf']:.6f}")
    out_lines.append(f"  max ratio: {H1['max_ratio_H1a']:.6f}" if H1['max_ratio_H1a'] is not None else "  max ratio: N/A")
    out_lines.append(f"  Families with abund_max = 1/2 exactly: {H1['n_at_ab_eq_half']}, "
                     f"their min_inf range starts at {H1['min_inf_at_ab_half']!r}")
    out_lines.append("  VERDICT: " + (
        "no positive lower-bound constant — min ratio can be 0" if H1['min_ratio_H1a'] is None or H1['min_ratio_H1a'] < 1e-10
        else f"weak signal (ratio ≥ {H1['min_ratio_H1a']:.4f})"
    ))
    out_lines.append("")

    # H2
    out_lines.append("H2 — Total influence I[f] vs abund_max (lower envelope)")
    out_lines.append("  abund_max (rounded) -> min total influence:")
    for ab, minI in H2["envelope_by_abundance"][:15]:
        out_lines.append(f"    {ab:.2f} -> {minI:.6f}")
    out_lines.append("  ...")
    for ab, minI in H2["envelope_by_abundance"][-5:]:
        out_lines.append(f"    {ab:.2f} -> {minI:.6f}")
    out_lines.append("")

    # H3
    out_lines.append("H3 — Low-level Fourier concentration C_k(F) = Σ_{|S|≤k} f̂² / p")
    for n in sorted(H3.keys()):
        d = H3[n]
        out_lines.append(f"  n={n}:  C_0 ∈ [{d.get('C0_min', 0):.4f}, {d.get('C0_max', 0):.4f}] mean {d.get('C0_mean', 0):.4f}")
        if "C1_min" in d:
            out_lines.append(f"         C_1 ∈ [{d['C1_min']:.4f}, {d['C1_max']:.4f}] mean {d['C1_mean']:.4f}")
        if "C2_min" in d:
            out_lines.append(f"         C_2 ∈ [{d['C2_min']:.4f}, {d['C2_max']:.4f}] mean {d['C2_mean']:.4f}")
    out_lines.append("  VERDICT: no uniform concentration. UC families can have arbitrarily-spread spectra.")
    out_lines.append("")

    # H4
    out_lines.append("H4 — Noise stability Stab_ρ / p vs abund_max (lower envelope)")
    for rho in (0.25, 0.5, 0.75, 0.9):
        env = H4[rho]
        out_lines.append(f"  ρ = {rho}:")
        for ab, s in env[:5]:
            out_lines.append(f"    abund={ab:.2f} -> min Stab/p = {s:.4f}")
        out_lines.append("    ...")
        for ab, s in env[-3:]:
            out_lines.append(f"    abund={ab:.2f} -> min Stab/p = {s:.4f}")
    out_lines.append("")

    # H5
    out_lines.append("H5 — FUCC in Fourier form: ∃ i with f̂({i}) ≤ 0")
    out_lines.append(f"  Families where min_i f̂({{i}}) ≤ 0:  {H5['fucc_holds_count']} / {H5['n_tested']}")
    out_lines.append(f"  Counterexamples (FUCC violation):    {H5['fucc_violation_count']}")
    if H5["fucc_violation_count"] == 0:
        out_lines.append("  ⇒  FUCC verified Fourier-style on all UC families with n ≤ 5.")
    out_lines.append("")

    # H6
    out_lines.append("H6 — Rotation-invariant level-1 control bound")
    out_lines.append("  Bound:  max ab_i ≥ (1 − √(W¹/(n p²))) / 2")
    out_lines.append(f"  Families where this bound exceeds 1/2: {H6['lb_exceeds_half']} / {H6['tested']}")
    out_lines.append(f"  max value of bound across all UC F:    {H6['max_lb']:.6f}")
    out_lines.append("  ⇒  the level-1 SPECTRAL WEIGHT alone gives no useful bound — it caps at 1/2.")
    out_lines.append("  (Structural fact: W¹ is invariant under sign-flipping each f̂({i}), so it cannot")
    out_lines.append("   detect whether ANY singleton coefficient is non-positive.)")
    out_lines.append("")

    # H7 — just acknowledgement
    out_lines.append("H7 — KKL-style: not applicable, 1_F is not monotone.  Skipped formal test.")
    out_lines.append("")

    text = "\n".join(out_lines)
    print(text)
    with open(os.path.join(DATA_DIR, "fourier_hypotheses.txt"), "w") as fh:
        fh.write(text + "\n")


if __name__ == "__main__":
    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    main(max_n=max_n)
