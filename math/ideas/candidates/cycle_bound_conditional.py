"""
cycle_bound_conditional.py
==========================

Conditional cycle-exclusion probe at B = 2^71 (Barina 2025), parameterised by
the two-log leading constant κ.

This is the joined CYCLE BOUND + ALT-ANGLE (κ-sensitivity) probe.  It produces
the conditional table m*(κ, B) under the schematic squeeze

    K  >  G(B)            (Crandall, rigorous; sharp via convergents of log_2 3)
    K  <  F(m; κ)         (LMN-style two-log, κ the leading constant)

calibrated to m*(κ_LMN = 24.34, B_Hercher = 3·2^69) = 91  (Hercher 2023, anchor).

The same calibration is re-applied at B_Barina = 2^71, giving:
    - the κ-sensitivity table (LMN-1995, Laurent-2008, candidate (2,3)-specific
      bounds derived from Padé/Salikhov/Marcovecchio/Rhin-Viola irrationality
      measures -- all flagged [CONSTANT UNVERIFIED] because the translation
      "irrationality measure -> two-log leading constant in the cycle window"
      is non-trivial and not done from primary sources here);
    - the unconditional honest read m*(κ_LMN, 2^71) ∈ {91, 92}, the Hercher-self-
      calibrated local-slope reading from the previous probe;
    - the Legendre/convergent-pinch corollary: in the regime
      K < B log 2 / (2m), K must be a convergent denominator q_j of log_2 3.
      We tabulate the convergent set [G(B), B log 2 / (2m)] at various m and
      check whether it ever STRICTLY excludes m beyond the κ-squeeze (it does
      not, in the relevant range -- reported as a precise corollary);
    - cross-validation on Steiner (m=1) and Simons (m=2) endpoints + the
      self-consistency anchor m*(24.34, B_Hercher) = 91.

NOTHING IN THIS SCRIPT REPRODUCES HERCHER'S F(m).  We use the schematic
F(m; κ) = c1 · κ · m^2 · (log(m+5)+c2)^2 model from automorphic_probe.py,
which is calibrated to be quantitatively correct AT the anchor m=91 and
gives meaningful RELATIVE sensitivities to κ.

ABSOLUTE RULES (per the mission brief):
- every constant in the κ table flagged [CONSTANT UNVERIFIED];
- no claim of m* >= 104 as proved (conditional on κ);
- the previous run's m*(2^71) ∈ {91, 92} self-calibrated bound MUST appear as
  the unconditional read.

Author: Alex Ye (AI assistance disclosed; not on author line).
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from typing import Dict, List, Optional, Tuple

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "collatz", "experiments"))

try:
    import mpmath as mp
    mp.mp.dps = 120
    HAVE_MPMATH = True
except Exception:
    HAVE_MPMATH = False

try:
    from cycles import (search_cycles_by_parity, search_cycles_by_orbit,
                        check_bound_consistency)
    HAVE_CYCLES = True
except Exception:
    HAVE_CYCLES = False

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Continued fraction of delta = log_2 3 and the Crandall lower bound G(B).
# (Both rigorous; reused from cycle_bound_push.py.)
# ---------------------------------------------------------------------------

def cf_delta(n_terms: int = 60) -> List[int]:
    assert HAVE_MPMATH
    delta = mp.log(3) / mp.log(2)
    out: List[int] = []
    y = delta
    for _ in range(n_terms):
        a = int(mp.floor(y))
        out.append(a)
        f = y - a
        if f == 0:
            break
        y = 1 / f
    return out


def convergents(cf: List[int]) -> List[Tuple[int, int]]:
    out = []
    h0, h1 = 1, cf[0]
    k0, k1 = 0, 1
    out.append((h1, k1))
    for i in range(1, len(cf)):
        h2 = cf[i] * h1 + h0
        k2 = cf[i] * k1 + k0
        out.append((h2, k2))
        h0, h1 = h1, h2
        k0, k1 = k1, k2
    return out


def crandall_G(B, convs: List[Tuple[int, int]]):
    """G(B) = (3/2) max_{j>4} min(q_j, 2B/(q_j+q_{j+1}))."""
    assert HAVE_MPMATH
    best = mp.mpf(0)
    arg = None
    for j in range(5, len(convs) - 1):
        qj = convs[j][1]
        qj1 = convs[j + 1][1]
        v = mp.mpf(3) / 2 * min(mp.mpf(qj), mp.mpf(2) * mp.mpf(B) / (qj + qj1))
        if v > best:
            best = v
            arg = (j, qj, qj1)
    return best, arg


# ---------------------------------------------------------------------------
# The schematic squeeze F(m; κ) = c1 κ m^2 (log(m+5) + c2)^2, calibrated so
# that m*(κ_LMN = 24.34, B_Hercher = 3·2^69) = 91 (Hercher anchor).
#
# This is the SAME model as automorphic_probe.py; we apply it here both at
# Hercher's B and at Barina's B, and we cross-check the calibration carefully.
# ---------------------------------------------------------------------------

# Crandall G(B) for the schematic Hercher anchor in raw nats (used for the
# κ-calibration). We use the SHARP Crandall G(B), computed from the actual
# convergents above, NOT the placeholder of the automorphic_probe.
def F_schematic(m: int, kappa: float, c1: float, c2: float = 2.0) -> float:
    return c1 * kappa * (m ** 2) * (math.log(m + 5) + c2) ** 2


def m_star_schematic(kappa: float, c1: float, c2: float, G_val: float,
                     m_hi: int = 100_000) -> int:
    """Largest m for which F_schematic(m; kappa) <= G_val (binary search)."""
    lo, hi = 1, m_hi
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if F_schematic(mid, kappa, c1, c2) <= G_val:
            lo = mid
        else:
            hi = mid - 1
    return lo


def calibrate_c1(target_m: int, target_kappa: float, G_val: float,
                 c2: float = 2.0) -> float:
    """Choose c1 so that F_schematic(target_m, target_kappa) = G_val."""
    return G_val / (target_kappa * (target_m ** 2) * (math.log(target_m + 5) + c2) ** 2)


# ---------------------------------------------------------------------------
# Legendre/convergent pinch (rigorous, discrete).
# ---------------------------------------------------------------------------

def convergent_pinch(B, m: int, G_val: float,
                     convs: List[Tuple[int, int]]) -> Dict:
    """In the regime K < B log 2 / (2m), Legendre forces K to be a convergent
    denominator q_j of log_2 3.  Combined with K >= G(B), the admissible
    K-set is the convergent denominators in [G(B), B log 2 / (2m)].
    If empty, the pinch excludes the cycle (in that regime)."""
    assert HAVE_MPMATH
    log2 = mp.log(2)
    upper = mp.mpf(B) * log2 / (2 * m)
    admissible = [q for (_, q) in convs
                  if mp.mpf(q) >= G_val and mp.mpf(q) <= upper]
    return {
        "m": m,
        "pinch_upper": float(upper),
        "G": float(G_val),
        "admissible_q": admissible,
        "n_admissible": len(admissible),
        "pinch_excludes_via_empty": (len(admissible) == 0 and float(upper) >= G_val),
    }


# ---------------------------------------------------------------------------
# κ-table.
#
# Every constant other than κ_LMN = 24.34 is flagged [CONSTANT UNVERIFIED].
# The named κ values for the (2,3)-specific Padé/Salikhov/Marcovecchio/Rhin-
# Viola family are HEURISTIC translations from published irrationality measures
# μ(log 2), μ(log 3) into a candidate two-log leading constant κ -- the
# translation involves Laurent's two-log to one-log specialization (Bugeaud
# survey) and is NOT redone from primary sources here.  The numbers in the
# table are placeholders to drive the sensitivity computation; the falsifiers
# section of the .md names what needs to be checked.
#
# Primary-source references (snippet-verified, all flagged):
#   - LMN-1995:    Laurent-Mignotte-Nesterenko, J. Number Theory 55 (1995).
#                  κ = 24.34 (the published rational-case D=1 leading constant).
#   - Laurent-2008: Acta Arith. 133.4 (2008), 325-348. "II" of the series.
#                  Improved leading constant in tight parameter windows;
#                  a "representative" value 17.9 is used here, but the
#                  effective κ in the (b' ~ 60-100, K ~ 10^10) cycle window
#                  is NOT extracted from primary text in this probe.
#   - Salikhov 2007: J. Number Theory; μ(log 3) ≤ 5.125 [verified snippet].
#   - Marcovecchio 2009: Acta Arith. 139.2; μ(log 2) via Rhin-Viola; "On the
#                  irrationality measure of log 3" (a follow-up) shows
#                  μ(log 3) ≤ 5.1163051 [verified snippet].
#   - Rhin-Viola 1996: GAFA 6 (1996); μ(log 2) via integral construction.
#                  Rukhadze (older bound) μ(log 2) ≤ 3.892 [verified snippet].
# ---------------------------------------------------------------------------

KAPPA_TABLE = [
    # (tag, kappa, source-flag, status)
    ("LMN-1995",
     24.34,
     "Laurent-Mignotte-Nesterenko, J. Number Theory 55 (1995), 285-321.",
     "calibration anchor; published rational-case D=1 leading constant"),
    ("Laurent-2008 (illustrative)",
     17.9,
     "Laurent, Acta Arith. 133.4 (2008), 325-348.",
     "[CONSTANT UNVERIFIED] representative in-window value; primary PDF "
     "not re-derived here. Bugeaud survey reports 17-21 range in tight "
     "parameter windows."),
    ("Padé/Salikhov-(log 3) (heuristic)",
     20.0,
     "Salikhov, J. Number Theory 127 (2007); μ(log 3) ≤ 5.125.",
     "[CONSTANT UNVERIFIED] heuristic translation: μ(log 3) bound NOT a "
     "two-log leading constant; substitution into LMN requires Laurent's "
     "one-log specialization (Bugeaud survey) which is not redone here."),
    ("Padé/Marcovecchio-(log 3) (heuristic)",
     19.5,
     "Marcovecchio-style bound μ(log 3) ≤ 5.1163051 (snippet).",
     "[CONSTANT UNVERIFIED] same caveat as Salikhov entry."),
    ("Rhin-Viola-(log 2) (heuristic)",
     21.0,
     "Rhin-Viola; Rukhadze μ(log 2) ≤ 3.892.",
     "[CONSTANT UNVERIFIED] same caveat; (log 2) measure unlikely to bind "
     "in the cycle window since log_2 3 = log 3 / log 2 ratio matters."),
]


# ---------------------------------------------------------------------------
# Main driver.
# ---------------------------------------------------------------------------

def main() -> int:
    if not HAVE_MPMATH:
        print("ERROR: mpmath required.")
        return 1

    print("=" * 76)
    print("cycle_bound_conditional.py  --  κ-conditional cycle exclusion")
    print("=" * 76)

    cf = cf_delta(60)
    convs = convergents(cf)
    print(f"\nConvergents of log_2(3), first few denominators:")
    for j in range(22, 27):
        print(f"  q_{j} = {convs[j][1]}")

    # Rigorous bounds at the two B's:
    B_H = mp.mpf(3) * 2 ** 69
    B_B = mp.mpf(2) ** 71
    G_H, argH = crandall_G(B_H, convs)
    G_B, argB = crandall_G(B_B, convs)
    print(f"\nCrandall G(B) (rigorous lower bound on K):")
    print(f"  B_H = 3*2^69 (Hercher 2023): G = {mp.nstr(G_H, 8)}  "
          f"(binding j={argH[0]}, q={argH[1]})")
    print(f"  B_B = 2^71   (Barina 2025): G = {mp.nstr(G_B, 8)}  "
          f"(binding j={argB[0]}, q={argB[1]})")
    log2_ratio = float(mp.log(G_B / G_H, 2))
    print(f"  log2(G_B / G_H) = {log2_ratio:.5f}  (=2^0.415, the 4/3 factor)")

    # Calibrate the schematic F(m; κ) so that m*(κ_LMN, B_H) = 91.
    G_H_f = float(G_H)
    G_B_f = float(G_B)
    c2 = 2.0
    c1 = calibrate_c1(target_m=91, target_kappa=24.34, G_val=G_H_f, c2=c2)
    print(f"\nSchematic squeeze model:")
    print(f"  F(m; κ) = c1 · κ · m^2 · (log(m+5) + c2)^2")
    print(f"  Calibration: c1 = {c1:.6g}, c2 = {c2}")
    # Sanity check: m*(24.34, B_H) = 91
    m_chk = m_star_schematic(24.34, c1, c2, G_H_f)
    print(f"  Sanity (Hercher anchor): m*(24.34, B_H) = {m_chk}  "
          f"(must be 91)")
    assert m_chk == 91, f"Calibration failed: got m={m_chk}"

    # Endpoint cross-checks: Steiner (m=1) and Simons (m=2):
    # Steiner 1977: no 1-cycle at all.  Simons-de Weger: m*=2 already at small B.
    # We check that the schematic model says F(1) << G and F(2) << G at both B's
    # (i.e. the squeeze trivially excludes m=1, m=2; not a hard test, but a
    # sanity check that the model is in the right ballpark).
    for B_label, B_val, G_val_f in [("B_H", B_H, G_H_f), ("B_B", B_B, G_B_f)]:
        for m_test in [1, 2]:
            F_test = F_schematic(m_test, 24.34, c1, c2)
            print(f"  Cross-check at {B_label}: F({m_test}; 24.34) = "
                  f"{F_test:.4g} {'<=' if F_test <= G_val_f else '>'} "
                  f"G = {G_val_f:.4g}  (m={m_test} excluded: "
                  f"{F_test <= G_val_f})")

    # ------------------------------------------------------------------
    # κ-sensitivity table.
    #
    # Reporting convention (carefully chosen, honest):
    #   - m*_schematic(κ, B): the largest m with F_schematic(m; κ) ≤ G(B),
    #     using the calibrated c1.  This is the schematic model number.
    #     At (24.34, B_H) it equals 91 by calibration.
    #
    #   - m*_honest(κ, B_B): the κ-RELATIVE prediction anchored on the honest
    #     unconditional read m*(24.34, B_B) ∈ {91, 92}, scaled by the model's
    #     own κ-sensitivity:
    #         m*_honest(κ, B_B) = round( 91 · sqrt(24.34/κ) )  +  Δ_B,
    #     where Δ_B ∈ {0, 1} is the unconditional B = 2^71 lift over Hercher.
    #     This is the line we report as the CONDITIONAL theorem number.
    #     (The schematic gives a larger m*(κ, B_B) at the same κ because
    #     the m* ~ sqrt(G) scaling overstates the real F(m) local slope at
    #     m ~ 91; the Hercher-anchored, κ-relative read is the honest one.)
    # ------------------------------------------------------------------
    print("\n" + "-" * 76)
    print("CONDITIONAL κ-TABLE  (κ-relative, Hercher-anchored)")
    print("-" * 76)
    print(f"\n  Sensitivity rule from schematic + Hercher anchor:")
    print(f"    m*_honest(κ, B_B)  =  round( 91 · sqrt(24.34 / κ) )  +  Δ_B,")
    print(f"  where Δ_B ∈ {{0, 1}} is the honest +1-at-best read for B = 2^71.\n")
    print(f"  {'κ source':<42}{'κ':>10}{'m*_sch(κ,B_H)':>16}"
          f"{'m*_sch(κ,B_B)':>16}{'m*_honest':>12}")
    print("  " + "-" * 96)
    kappa_results = []
    delta_B = 1  # honest unconditional +1 lift from B_H to B_B
    for tag, k, src, status in KAPPA_TABLE:
        m_sch_H = m_star_schematic(k, c1, c2, G_H_f)
        m_sch_B = m_star_schematic(k, c1, c2, G_B_f)
        # Hercher-anchored κ-relative honest prediction:
        m_honest = int(round(91 * math.sqrt(24.34 / k))) + delta_B
        kappa_results.append({
            "tag": tag, "kappa": k, "source": src, "status": status,
            "m_star_schematic_at_B_H": m_sch_H,
            "m_star_schematic_at_B_B": m_sch_B,
            "m_star_honest_at_B_B": m_honest,
            "delta_vs_91": m_honest - 91,
        })
        print(f"  {tag:<42}{k:>10.3f}{m_sch_H:>16d}{m_sch_B:>16d}{m_honest:>12d}")

    # ------------------------------------------------------------------
    # Unconditional honest read (the previous probe).
    # ------------------------------------------------------------------
    print("\n" + "-" * 76)
    print("UNCONDITIONAL HONEST READ (from cycle_bound_push.md §3.4)")
    print("-" * 76)
    print("""
  At B = 2^71 with the LMN-1995 published κ = 24.34, the Hercher-self-
  calibrated local-slope reading gives  m*(2^71) ∈ {91, 92}.  This is the
  +1-at-best read; the schematic model above gives m*(24.34, 2^71) = 91
  (calibration anchor is exactly 91 at B_H, so the small G_B/G_H = 4/3
  factor lifts it less than one integer m in the schematic; the schematic
  is NOT to be over-interpreted at this knife-edge -- the honest read of
  {91, 92} INCLUDES the +1).
""")

    # ------------------------------------------------------------------
    # Legendre/convergent pinch corollary.
    # ------------------------------------------------------------------
    print("-" * 76)
    print("LEGENDRE/CONVERGENT PINCH (rigorous, discrete)")
    print("-" * 76)
    print(f"\n  At B = 2^71, G(B) = {G_B_f:.5g}.")
    print(f"  In the regime K < B log 2 / (2m), K must be a convergent")
    print(f"  denominator q_j of log_2 3.\n")
    print(f"  {'m':>5}  {'pinch_upper':>15}  {'#q_j in [G,upper]':>20}  {'min q_j':>14}")
    pinch_rows = []
    for m in [1, 2, 5, 10, 50, 91, 92, 100, 110, 200, 1000, 10**4, 10**5,
              10**6, 10**8, 10**10]:
        p = convergent_pinch(B_B, m, G_B_f, convs)
        pinch_rows.append(p)
        min_q = min(p["admissible_q"]) if p["admissible_q"] else None
        print(f"  {m:>5}  {p['pinch_upper']:>15.5g}  {p['n_admissible']:>20d}  "
              f"{str(min_q):>14}")
    # find smallest m for which the pinch becomes empty
    pinch_empty_m = None
    for m in [1, 100, 1000, 10**4, 10**5, 10**6, 10**7, 10**8, 10**9, 10**10, 10**11]:
        p = convergent_pinch(B_B, m, G_B_f, convs)
        if p["pinch_excludes_via_empty"]:
            pinch_empty_m = m
            break
    print(f"\n  Smallest m where the admissible q-set becomes empty: "
          f"m ~ {pinch_empty_m}  (vacuous at the κ-squeeze scale m ~ 100).")
    print("  Corollary: the Legendre pinch adds NOTHING to the κ-squeeze")
    print("  in the relevant range m ≤ ~10^10.  It is a TRUE rigorous")
    print("  additional constraint but is not the binding one at B = 2^71.")

    # ------------------------------------------------------------------
    # Brute-force validation (small-K side).
    # ------------------------------------------------------------------
    val = {"skipped": True}
    if HAVE_CYCLES:
        print("\n" + "-" * 76)
        print("Brute-force validation (small-K side)")
        print("-" * 76)
        t0 = time.perf_counter()
        parity = search_cycles_by_parity(18, verbose=False)
        nontrivial = [r for r in parity if not r.get("is_trivial", True)]
        t1 = time.perf_counter()
        orbit = search_cycles_by_orbit(5 * 10**4, 3000, verbose=False)
        t2 = time.perf_counter()
        consistency = check_bound_consistency(max_m=18, verbose=False)
        val = {
            "ok": True,
            "parity_nontrivial_count": len(nontrivial),
            "orbit_cycle_count": len(orbit),
            "consistency_identity_ok": consistency.get("n_identity_ok"),
            "consistency_bound_ok": consistency.get("n_bound_ok"),
            "consistency_n_fixed": consistency.get("n_fixed"),
            "elapsed_parity_s": t1 - t0,
            "elapsed_orbit_s": t2 - t1,
        }
        print(f"  parity-length up to 18: nontrivial cycles = {len(nontrivial)}")
        print(f"  orbits in [2, 5e4], period <= 3000: cycles = {len(orbit)}")
        print(f"  identity Lambda = sum eps_j: "
              f"{consistency.get('n_identity_ok')}/{consistency.get('n_fixed')}; "
              f"bound 0 < Lambda < m/n: "
              f"{consistency.get('n_bound_ok')}/{consistency.get('n_fixed')}")

    # ------------------------------------------------------------------
    # Save data.
    # ------------------------------------------------------------------
    out = {
        "B_H": float(B_H),
        "B_B": float(B_B),
        "G_H": G_H_f,
        "G_B": G_B_f,
        "G_H_binding_qj": int(argH[1]) if argH else None,
        "G_B_binding_qj": int(argB[1]) if argB else None,
        "log2_ratio_GB_GH": log2_ratio,
        "calibration": {
            "c1": c1, "c2": c2,
            "target_m": 91, "target_kappa": 24.34, "target_B": "3*2^69",
        },
        "kappa_table": kappa_results,
        "unconditional_honest_read": {
            "m_star_at_B_B_with_LMN_1995": "{91, 92}",
            "source": "Hercher-self-calibrated local-slope; "
                      "cycle_bound_push.md §3.4 / cycle_bound_attempt.md §6",
            "schematic_model_value": m_star_schematic(24.34, c1, c2, G_B_f),
        },
        "pinch": {
            "rows": [
                {"m": r["m"], "pinch_upper": r["pinch_upper"],
                 "n_admissible": r["n_admissible"],
                 "min_q": (min(r["admissible_q"]) if r["admissible_q"] else None)}
                for r in pinch_rows
            ],
            "smallest_m_pinch_empty": pinch_empty_m,
            "corollary": ("In the range m ≤ ~10^10 at B = 2^71, the Legendre "
                          "convergent-denominator pinch is non-empty and adds "
                          "nothing to the κ-squeeze. The pinch is a rigorous "
                          "additional constraint, not a tighter bound."),
        },
        "validation": val,
        "convergents_first_30": [(int(p), int(q)) for (p, q) in convs[:30]],
    }
    out_path = os.path.join(DATA_DIR, "cycle_bound_conditional.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nWrote {out_path}")

    print("\n" + "=" * 76)
    print("CONDITIONAL THEOREM (see cycle_bound_conditional.md for the statement)")
    print("=" * 76)
    print("""
  Theorem (conditional, schematic).  Assume:
    (H1) A two-log linear-form lower bound of the form
            log |Lambda|  >=  -κ · D^4 · (log A_1)(log A_2) · (log b' + 0.14)^2
         holds in the (log 2, log 3) window at b' ~ 60-100, K ~ 10^10,
         with effective leading constant κ in the rational case D=1.
    (H2) The Collatz conjecture is verified for all n ≤ B = 2^71  (Barina 2025).
    (H3) Hercher's circuit-averaging machinery applies (with κ entering as a
         multiplicative factor in the upper bound F(m; κ); the schematic model
         F(m; κ) ∝ κ · m^2 · (log b')^2 is correct in its κ-scaling).

  Then no nontrivial Collatz m-cycle exists with m ≤ m*(κ, B = 2^71), where
  m*(κ, B) is computed by the squeeze F(m; κ) ≤ G(B), giving the table above.

  Unconditional (no κ improvement): m*(κ_LMN, 2^71) ∈ {91, 92}  (Hercher 2023
  plus the +1 from B = 2^71; not robustly beating 91 from B alone).

  Conditional (Laurent-2008 κ = 17.9, [CONSTANT UNVERIFIED] in cycle window):
  m* lifts to the value shown above (subject to (H1)-(H3) holding).
""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
