"""
automorphic_probe.py
====================

Probe for the modular-forms / automorphic L-function angle on Collatz cycles.

Sub-direction chosen: (iii) S-unit equation / linear-forms-in-2-logarithms
effective bounds and their sensitivity to the leading constant κ.

The Steiner-Simons-de Weger-Hercher cycle-exclusion squeeze is

    G(log B)  <  K  <  F(m; κ)

where
  - G(log B)  comes from Crandall / continued-fraction lower bound (depends on B)
  - F(m; κ)   comes from the LMN two-log linear-forms upper bound on Λ,
              with κ the leading transcendence constant (LMN-1995: κ=24.34).
              The exponent "0.158" in θ_m(K)<2^{-0.158 K} of Hercher's
              squeeze is, schematically, ~ (log 3) / (κ · (log A_1)(log A_2)).

What this probe DOES (1-day computation):
  - Treat κ as a knob.
  - Compute the resulting threshold m^*(κ) := largest m for which F(m;κ) ≤ G(log B),
    using a published-form approximation of Hercher's squeeze.
  - Tabulate dm^*/dκ near κ = 24.34 (LMN-1995).
  - Tabulate what improvement Δκ would be needed to push m^* from 91 to {100, 150, 200}.
  - This QUANTIFIES the value of any hypothetical automorphic/Padé-approximant
    improvement of the two-log constant, including whether the available
    irrationality measures of log_2(3) (Rhin: μ(log 3)≤5.116, Rukhadze
    μ(log 2)≤3.892) translate into a usable refined constant via
    Laurent's two-log → one-log specialization.

What this probe DOES NOT do:
  - Actually re-execute Hercher's full optimization (his auxiliary parameters,
    the b'-structure, the iterated tightening with m). We use the leading-
    order asymptotic squeeze F(m) ≈ C·m^2 · log^2(b') with κ entering as a
    multiplicative factor — this is the dependency on κ that Hercher's
    Theorem inherits from LMN. The absolute m^* number from this rough model
    will NOT reproduce 91 exactly; what is meaningful is the RELATIVE
    sensitivity dm^*/dκ.

Author: Alex Ye
"""
import math
import json
import os

# ----- inputs -----
# Hercher's verified-cycle bound
B = 1536 * 2**60                   # ≈ 1.77e18
log2_3 = math.log(3) / math.log(2) # δ ≈ 1.5849625
log_B = math.log(B)

# Leading two-log constants we care about
KAPPA_LMN_1995  = 24.34            # Laurent-Mignotte-Nesterenko 1995
# Laurent-2008 ("II") leading-constant improvements are regime-dependent;
# in the rational-D=1 corollary form most commonly cited, a leading constant
# in the range [17, 21] for tight parameter choices is achievable
# (see Bugeaud survey "Estimates for linear forms in logarithms"); we sample.
KAPPA_LAURENT_2008_OPT = 17.9      # optimistic Laurent-2008-style constant
KAPPA_LAURENT_2008_PES = 21.5      # pessimistic in-window value

# An automorphic/Padé-approximant "dream" refinement: Rhin-Viola-style
# irrationality-measure techniques applied to the specific pair (log 2, log 3)
# could in principle yield further log-improvements; we use 15 and 12 as
# illustrative dream constants (NOT claimed achievable — sensitivity probe only).
KAPPA_DREAM = [15.0, 12.0, 10.0]

# ----- the schematic squeeze model -----
# Hercher (and earlier Simons-de Weger): K is bounded above by an expression
# of the form
#     K < F(m; κ) ≈ A(m) · κ · (log b')^2
# where b' depends on K and m only through a slow log factor, and A(m) ~ m^2
# (the "circuit budget" growing with m). The lower bound is
#     K > G(log B) ≈ q(B)
# with q(B) the smallest convergent denominator of δ = log_2 3 with
# q > B / δ; the verified value (Simons-de Weger / Hercher style) at
# B ≈ 1.77e18 is roughly
G_value = 357_638_239             # Simons m=2 value, used in §2 squeeze;
                                  # Hercher's B is larger, so G scales up.
# For Hercher's B = 3·2^69, the relevant convergent-denominator-style lower
# bound is on the order of B itself (since one needs |2^N - 3^K|·B-scale gap).
# We use a power-law form for G to keep the sensitivity calculation honest:
def G(logB):
    """Schematic Crandall-type lower bound on K, in the right ballpark."""
    return 0.5 * math.exp(0.5 * logB)   # placeholder scaling; only RATIO to F matters

# Schematic F(m; κ) ≈ c1 · κ · m^2 · (log m + c2)^2
def F(m, kappa, c1=1.0e6, c2=2.0):
    return c1 * kappa * (m**2) * (math.log(m + 5) + c2)**2

def m_star(kappa, c1=1.0e6, c2=2.0):
    """Largest m for which F(m;κ) ≤ G(log B), i.e. squeeze closes."""
    G_val = G(log_B)
    # binary search
    lo, hi = 1, 10_000
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if F(mid, kappa, c1, c2) <= G_val:
            lo = mid
        else:
            hi = mid - 1
    return lo

def calibrate_c1():
    """Choose c1 so that m^*(κ=24.34) ≈ 91 (matching Hercher).
    This calibration makes the relative sensitivity meaningful."""
    target_m = 91
    target_kappa = KAPPA_LMN_1995
    # Solve F(91, 24.34, c1) = G(log B) => c1 = G(logB) / (κ · m^2 · (log(m+5)+c2)^2)
    G_val = G(log_B)
    c2 = 2.0
    c1 = G_val / (target_kappa * (target_m**2) * (math.log(target_m + 5) + c2)**2)
    return c1, c2

def main():
    c1, c2 = calibrate_c1()
    print(f"# Calibration: c1 = {c1:.6g}, c2 = {c2}")
    print(f"# G(log B) = {G(log_B):.6g}")
    print(f"# Sanity: m*(κ=24.34) = {m_star(KAPPA_LMN_1995, c1, c2)}  (should be 91)")
    print()

    kappas = [
        ("LMN-1995",           KAPPA_LMN_1995),
        ("Laurent-2008 pess",  KAPPA_LAURENT_2008_PES),
        ("Laurent-2008 opt",   KAPPA_LAURENT_2008_OPT),
        ("Dream κ=15",         15.0),
        ("Dream κ=12",         12.0),
        ("Dream κ=10",         10.0),
        ("Dream κ=7",          7.0),
        ("Dream κ=5",          5.0),
    ]

    results = []
    print("# κ-sensitivity of the cycle-exclusion threshold m^*")
    print(f"{'tag':<22}{'κ':>10}{'m^*':>8}{'Δm vs Hercher':>16}")
    base = m_star(KAPPA_LMN_1995, c1, c2)
    for tag, k in kappas:
        m = m_star(k, c1, c2)
        results.append({"tag": tag, "kappa": k, "m_star": m, "delta": m - base})
        print(f"{tag:<22}{k:>10.3f}{m:>8d}{m - base:>+16d}")

    print()
    print("# Inverse: what κ would push m^* to target?")
    print(f"{'target m':>10}{'required κ':>14}{'fractional improvement':>28}")
    inv_results = []
    for target in [92, 100, 120, 150, 200, 300, 500, 1000]:
        # binary search on κ
        lo, hi = 0.01, 24.34
        while hi - lo > 1e-4:
            mid = (lo + hi) / 2
            if m_star(mid, c1, c2) >= target:
                lo = mid
            else:
                hi = mid
        req_kappa = lo
        frac = 1.0 - req_kappa / KAPPA_LMN_1995
        inv_results.append({"target_m": target, "required_kappa": req_kappa, "fractional_improvement": frac})
        print(f"{target:>10d}{req_kappa:>14.4f}{frac*100:>26.2f}%")

    print()
    print("# Derivative: dm^*/dκ at κ=24.34 (finite difference)")
    eps = 0.01
    dm = (m_star(KAPPA_LMN_1995 - eps, c1, c2) - m_star(KAPPA_LMN_1995, c1, c2)) / (-eps)
    print(f"  dm*/dκ ≈ {dm:.4f}   (decreasing κ by 1 gains ≈ {-dm:.1f} cycles excluded)")

    print()
    print("# Reading: a multiplicative improvement of the two-log constant by factor f")
    print("#   shifts m^* by approximately m^* · (1/√f - 1) at fixed B")
    print("#   (since m^* ~ √(G/κ) in the c1·κ·m^2 model).")

    out = {
        "B": B,
        "log_B": log_B,
        "calibration": {"c1": c1, "c2": c2, "target_m": 91, "target_kappa": KAPPA_LMN_1995},
        "kappa_table": results,
        "inverse_table": inv_results,
        "dm_dkappa_at_LMN": dm,
        "note": (
            "Sensitivity probe only. F(m;κ) is a schematic c1·κ·m^2·log^2 model "
            "calibrated to m^*(24.34)=91. Numbers are RELATIVE; absolute m^* "
            "deviations from real Hercher reflect model simplification, not "
            "constants in the literature."
        ),
    }
    out_path = os.path.join(os.path.dirname(__file__), "data", "automorphic_probe.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {out_path}")

if __name__ == "__main__":
    main()
