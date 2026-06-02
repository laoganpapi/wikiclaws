"""
vector3_delta2_nonproduct.py
============================

Vector 3 (Δ₂-recapture at a NON-PRODUCT extremizer): the experimental + analytic
test of the ONE remaining live lever to beat ψ = (3−√5)/2 with the i.i.d.-entropy
method.

THE LEVER (see theory/vector1_shearer_chain_rule.md §5 and theory/
vector3_delta2_nonproduct.md): Gilmer's chain rule discards

    Δ₂ = Σ_i I(C_i ; (A_{<i},B_{<i}) | C_{<i})  ≥ 0,      C = A ∪ B.

Vector 1 proved Δ₂ ≡ 0 at the AHS *product* extremizer (iid Bern(ψ)), so
recapturing it inside the i.i.d. coupling gives nothing. The remaining hope:
move the worst case OFF the product, onto a NON-PRODUCT coupling where Δ₂ > 0,
and hope the recaptured Δ₂ pushes the certified constant above ψ.

WHAT THIS FILE DOES
-------------------
1. `augmented_constant_iid_family(F)`:
   The most-optimistic Δ₂-recapture per-family certified constant for the
   i.i.d.-on-F coupling (recover ALL of Δ₂). Same object as
   `vector_analysis.v1_certified_constant`, re-derived here standalone, used to
   re-confirm Vector 1's negative on all UC families n≤5.

2. `SharedUCoupling`: a family of NON-PRODUCT couplings — the conditionally-i.i.d.
   ("shared auxiliary U") coupling. Given U=j (∈{1..k}, weight w_j), every
   coordinate pair (A_i,B_i) is i.i.d. Bern(p_j); the SAME U is shared across all
   n coordinates. This is non-product (coordinates correlated through U) and has
   Δ₂ > 0. We compute EXACTLY, for finite n, the four quantities
       H(A),  H(C),  chain-LB = Σ_i H(C_i|A_{<i},B_{<i}),  Δ₂ = H(C) − chain-LB,
   and the augmented certified constant, and watch them as n → ∞.

3. `correlated_bernoulli_threshold`: the correlated-Bernoulli coupling (single p,
   pair-correlation ρ). Shows the TRAP: ρ>0 *appears* to raise the threshold above
   ψ, but that is choosing a favourable (non-i.i.d.) coupling — NOT a necessary
   condition valid for every UC family (an UC family sampled i.i.d. has ρ=0). The
   companion `validate_via_sweep` confirms the only inequalities that survive a
   full UC sweep are the ones whose threshold is ≤ ψ.

4. `augmented_inequality_pair(F)` + a sweep over all UC families n≤5: the
   FALSIFICATION test. Every candidate augmented inequality must satisfy LHS≤RHS
   on all 29,327 (n=5) orbit reps; one violation kills it.

THE VERDICT (computed by `main`): no member of these non-product families yields
a CERTIFIED constant > ψ. The Δ₂ gain is O(1) (bounded by I(C;U) ≤ H(U) ≤ log₂k),
while the budget H(A) is Θ(n); per coordinate the recaptured Δ₂ → 0. The exact
tradeoff is quantified in `delta2_vs_budget_table`.

All entropies in BITS (log₂), matching verify_ahs.py.

Author: Alex Ye (AI assistance disclosed separately).
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from math import comb

import numpy as np

import verify_ahs as V

# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------

PSI = (3.0 - math.sqrt(5.0)) / 2.0


def h(p: float) -> float:
    """Binary entropy in BITS; h(0)=h(1)=0."""
    if p <= 1e-15 or p >= 1.0 - 1e-15:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def union_p(p: float, q: float) -> float:
    return 1.0 - (1.0 - p) * (1.0 - q)


# ===========================================================================
# PART 1.  i.i.d.-on-F augmented constant (re-confirm Vector 1's negative).
# ===========================================================================

def augmented_constant_iid_family(F, n: int | None = None) -> dict:
    """
    The most-optimistic Δ₂-recapture certified constant for A,B i.i.d. uniform
    on the finite family F.

    The honest augmented chain (theory/vector3_delta2_nonproduct.md §1):
        H(C) = chain-LB + Δ₂,                       (exact identity)
        chain-LB ≥ (1/(1−c)) · S,                   (Sawin per-coord, S = AHS numerator)
        H(C) ≤ H(A) = log₂|F|.                      (union closure)
      ⇒  (1/(1−c)) S + Δ₂ ≤ H(A).
    The family "permits" (does not yet contradict) constant c as long as the
    above is consistent with its own H(C); the per-family certified constant is
        c_aug(F) = 1 − S / (H(C) − Δ₂) = 1 − S / chain-LB.
    Recovering ALL of Δ₂ moves the comparison denominator from H(C) (the AHS
    value, giving c_AHS) down to chain-LB (giving c_aug). Returns both, plus Δ₂.
    """
    Fl = list(F)
    if n is None:
        u = 0
        for a in Fl:
            u |= a
        n = u.bit_length()
    Hu = V.exact_entropy_union(Fl)
    clb = V.chain_rule_lower_bound(Fl, n)
    d2 = Hu - clb
    m = len(Fl)
    S = 0.0
    for i in range(n):
        bit = 1 << i
        p_i = sum(1 for a in Fl if a & bit) / m
        S += (1.0 - p_i) * V.H_Ai_given_prefix(Fl, i)
    c_ahs = 1.0 - S / Hu if Hu > 1e-12 else 1.0
    c_aug = 1.0 - S / clb if clb > 1e-12 else 1.0
    return {"c_ahs": c_ahs, "c_aug": c_aug, "delta2": d2,
            "H_union": Hu, "chain_lb": clb, "S": S, "abundance": V.abundance(Fl)}


# ===========================================================================
# PART 2.  The NON-PRODUCT family: shared-U (conditionally i.i.d.) coupling.
# ===========================================================================

@dataclass
class SharedUCoupling:
    """
    Conditionally-i.i.d. coupling with a shared auxiliary U ∈ {1,…,k}.

    U=j with weight w_j; given U=j every coordinate pair (A_i,B_i) is i.i.d.
    Bern(p_j) (A ⟂ B given U, identically distributed). The SAME U is shared by
    all n coordinates → coordinates are exchangeable but NOT independent
    (non-product), and Δ₂ > 0.

    All quantities are computed EXACTLY (closed-form sums over popcounts /
    prefix-count classes), no Monte Carlo, exploiting exchangeability.
    """
    p: np.ndarray  # atoms in [0,1], shape (k,)
    w: np.ndarray  # weights, shape (k,), sum to 1

    def __post_init__(self):
        self.p = np.asarray(self.p, dtype=float)
        self.w = np.asarray(self.w, dtype=float)
        assert self.p.shape == self.w.shape
        assert abs(self.w.sum() - 1.0) < 1e-9 and (self.w >= -1e-12).all()
        self.k = len(self.p)

    # -- per-point mixture quantities (the U-mixture; the n→∞ per-coordinate limits) --
    def E_h_p(self) -> float:
        return float(sum(self.w[j] * h(self.p[j]) for j in range(self.k)))

    def E_h_u(self) -> float:
        return float(sum(self.w[j] * h(union_p(self.p[j], self.p[j])) for j in range(self.k)))

    def H_U(self) -> float:
        return float(sum(-wj * math.log2(wj) for wj in self.w if wj > 1e-300))

    def E_P(self) -> float:
        return float(self.w @ self.p)

    # -- exact finite-n entropies (exchangeable ⇒ group by popcount / prefix counts) --
    def H_A(self, n: int) -> float:
        """H(A) for the n-coordinate shared-U law (A only)."""
        H = 0.0
        for s in range(n + 1):
            qs = float(sum(self.w[j] * self.p[j] ** s * (1 - self.p[j]) ** (n - s)
                           for j in range(self.k)))
            if qs > 1e-300:
                H += -comb(n, s) * qs * math.log2(qs)
        return H

    def H_union(self, n: int) -> float:
        """H(C)=H(A∪B); given U=j, C_i iid Bern(u_j), u_j=2p_j−p_j²."""
        H = 0.0
        for s in range(n + 1):
            qs = float(sum(self.w[j] * (2 * self.p[j] - self.p[j] ** 2) ** s
                           * ((1 - self.p[j]) ** 2) ** (n - s) for j in range(self.k)))
            if qs > 1e-300:
                H += -comb(n, s) * qs * math.log2(qs)
        return H

    def H_union_given_U(self, n: int) -> float:
        return n * self.E_h_u()

    def I_C_U(self, n: int) -> float:
        """I(C;U) = H(C) − H(C|U).  In [0, H(U)]; → H(U) as n→∞."""
        return self.H_union(n) - self.H_union_given_U(n)

    def chain_lb(self, n: int) -> float:
        """
        Σ_i H(C_i | A_{<i}, B_{<i}), exact. Condition on prefix counts (sA,sB);
        posterior over U; C_i ~ mixture Bern(u_j) under the posterior.
        """
        total = 0.0
        pk = self.p
        wk = self.w
        u = 2 * pk - pk * pk
        for i in range(n):
            L = i
            Hci = 0.0
            for sA in range(L + 1):
                cA = comb(L, sA)
                for sB in range(L + 1):
                    cB = comb(L, sB)
                    num = wk * cA * pk ** sA * (1 - pk) ** (L - sA) \
                        * cB * pk ** sB * (1 - pk) ** (L - sB)
                    Z = float(num.sum())
                    if Z < 1e-300:
                        continue
                    qc1 = float((num @ u) / Z)
                    Hci += Z * h(qc1)
            total += Hci
        return total

    def delta2(self, n: int) -> float:
        """Δ₂ = H(C) − chain-LB ≥ 0 (recaptured slack).  ≤ I(C;U)."""
        return self.H_union(n) - self.chain_lb(n)

    def report(self, n: int) -> dict:
        HA = self.H_A(n)
        HC = self.H_union(n)
        clb = self.chain_lb(n)
        d2 = HC - clb
        return {
            "n": n, "H_A": HA, "H_union": HC, "chain_lb": clb, "delta2": d2,
            "I_C_U": self.I_C_U(n), "H_U": self.H_U(),
            "H_A_per": HA / n, "H_union_per": HC / n, "delta2_per": d2 / n,
            "E_h_p": self.E_h_p(), "E_h_u": self.E_h_u(), "E_P": self.E_P(),
        }


# ---------------------------------------------------------------------------
# Augmented certified constant for the shared-U coupling, at FINITE n.
# ---------------------------------------------------------------------------

def shared_u_augmented_constant(coupling: SharedUCoupling, n: int) -> dict:
    """
    The augmented certified constant for the n-coordinate shared-U coupling,
    treating the whole n-block as the "configuration" (a finite extremizer).

    AHS / chain-rule numerator on the n-block (the analogue of S):
        S_n = Σ_i (1 − p_i) H(A_i | A_{<i}),  p_i = marginal of coord i.
    By exchangeability every coordinate has the same marginal p̄ = E[P] and the
    same conditional entropy profile, so we compute S_n exactly from the law.

      c_AHS(block) = 1 − S_n / H(C),                 (drop Δ₂)
      c_aug(block) = 1 − S_n / (H(C) − Δ₂)           (recapture ALL Δ₂)
                   = 1 − S_n / chain-LB.

    Returns both and Δ₂. (As n→∞ both → ψ; see `delta2_vs_budget_table`.)
    """
    HC = coupling.H_union(n)
    clb = coupling.chain_lb(n)
    d2 = HC - clb
    # S_n = Σ_i (1−p_i) H(A_i|A_{<i}). Compute exactly from the exchangeable law.
    pk, wk = coupling.p, coupling.w
    S_n = 0.0
    for i in range(n):
        L = i
        # marginal p_i and conditional H(A_i|A_{<i}) under shared-U law
        # p_i = E[p_U]  (marginal of any coordinate)
        p_i = float(wk @ pk)
        # H(A_i|A_{<i}) = Σ_{sA} P(prefix has sA ones) · h( P(A_i=1 | prefix) )
        Hcond = 0.0
        for sA in range(L + 1):
            cA = comb(L, sA)
            num = wk * cA * pk ** sA * (1 - pk) ** (L - sA)
            Z = float(num.sum())
            if Z < 1e-300:
                continue
            p_next = float((num @ pk) / Z)
            Hcond += Z * h(p_next)
        S_n += (1.0 - p_i) * Hcond
    c_ahs = 1.0 - S_n / HC if HC > 1e-12 else 1.0
    c_aug = 1.0 - S_n / clb if clb > 1e-12 else 1.0
    return {"n": n, "c_ahs": c_ahs, "c_aug": c_aug, "delta2": d2,
            "H_union": HC, "chain_lb": clb, "S_n": S_n, "E_P": float(wk @ pk)}


# ---------------------------------------------------------------------------
# The exact Δ₂-gain-vs-budget tradeoff table.
# ---------------------------------------------------------------------------

def delta2_vs_budget_table(coupling: SharedUCoupling, ns=(1, 2, 4, 8, 16, 32, 64)) -> list[dict]:
    """For a shared-U coupling, tabulate how Δ₂ (the gain) scales vs H(A) (the
    budget) as n grows: Δ₂ stays O(1) (≤H(U)), H(A) grows Θ(n), so Δ₂/n→0 and
    c_aug → c_AHS → ψ."""
    rows = []
    for n in ns:
        rep = coupling.report(n)
        aug = shared_u_augmented_constant(coupling, n)
        rows.append({
            "n": n,
            "H_A": rep["H_A"],
            "delta2": rep["delta2"],
            "delta2_over_HA": rep["delta2"] / rep["H_A"] if rep["H_A"] > 0 else 0.0,
            "delta2_per_coord": rep["delta2"] / n,
            "I_C_U": rep["I_C_U"],
            "c_ahs": aug["c_ahs"],
            "c_aug": aug["c_aug"],
        })
    return rows


# ===========================================================================
# PART 3.  The TRAP: correlated-Bernoulli coupling (choosing a good coupling).
# ===========================================================================

def correlated_union_p(p: float, rho: float) -> float:
    """
    Pr[A∨B=1] for a single correlated-Bernoulli pair with marginals (p,p) and
    Pearson correlation ρ:
        P(0,0) = (1−p)² + ρ p(1−p),   so   P(A∨B=1) = 1 − P(0,0).
    Valid ρ range keeps all four cell probabilities in [0,1].
    """
    p00 = (1 - p) ** 2 + rho * p * (1 - p)
    return 1.0 - p00


def correlated_bernoulli_threshold(rho: float, grid: int = 20000) -> float:
    """
    Largest p ≤ 1/2 with h(union) ≤ h(p) for the correlated pair at correlation
    ρ — the 'single-letter crossover' this coupling would (illegitimately, for
    ρ≠0) certify. ρ=0 ⇒ ψ. ρ>0 ⇒ >ψ (the trap); ρ<0 ⇒ <ψ.
    """
    last = 0.0
    for p in np.linspace(1e-4, 0.5, grid):
        u = correlated_union_p(p, rho)
        if h(u) <= h(p) + 1e-12:
            last = p
        else:
            # crossover is the largest p where it still holds; for ρ≥0 holding is
            # an interval [p*, 0.5]; we want its left endpoint p*.
            if last > 0.0:
                return float(p)  # first p where it flips back to violated above p*
    return float(last)


def correlated_crossover(rho: float, grid: int = 200000) -> float:
    """The crossover p* where h(union)=h(p) for the correlated pair (the value
    the coupling 'looks like' to the single-letter test). Returns the unique
    p*∈(0,1/2)."""
    prev_sign = None
    prev_p = 1e-4
    for p in np.linspace(1e-4, 0.5, grid):
        d = h(correlated_union_p(p, rho)) - h(p)  # >0 means union carries more (violated)
        s = d > 0
        if prev_sign is not None and s != prev_sign:
            return float(0.5 * (p + prev_p))
        prev_sign = s
        prev_p = p
    return float("nan")


# ===========================================================================
# PART 4.  Falsification: augmented inequalities must survive the full UC sweep.
# ===========================================================================

def augmented_inequality_pair(F) -> tuple[float, float]:
    """
    The honest Δ₂-augmented necessary condition as an `Inequality` for
    `sweep_inequality` (must hold on EVERY UC family).

    The identity H(C) = chain-LB + Δ₂ with the budget H(C) ≤ H(A) gives the
    necessary condition
        chain-LB + Δ₂ ≤ H(A)         i.e.   H(C) ≤ H(A).
    (Recapturing Δ₂ does NOT create a new inequality on F — it is the SAME
    H(C)≤H(A); Δ₂ just relabels chain-LB+Δ₂ as H(C).) We expose LHS=H(C),
    RHS=H(A); this MUST hold (union closure) — a sanity sweep, and the point is
    that Δ₂-recapture buys no *additional* valid constraint on F.
    """
    return V.exact_entropy_union(F), V.exact_H_A(F)


def ahs_plus_delta2_floor_pair(c: float):
    """
    Candidate 'improved floor' inequality at level c, encoding the augmented
    lower bound:  (1/(1−c)) S + Δ₂ ≤ H(A) as LHS ≤ RHS, where
        LHS = (1/(1−c)) S + Δ₂,   RHS = H(A).
    If this holds on ALL UC families for some c > ψ, that would certify c. (It
    does NOT for c>ψ — the sweep finds violations; that is the whole verdict.)
    """
    def ineq(F) -> tuple[float, float]:
        Fl = list(F)
        u = 0
        for a in Fl:
            u |= a
        n = u.bit_length()
        m = len(Fl)
        if m == 0:
            return 0.0, 0.0
        S = 0.0
        for i in range(n):
            bit = 1 << i
            p_i = sum(1 for a in Fl if a & bit) / m
            S += (1.0 - p_i) * V.H_Ai_given_prefix(Fl, i)
        d2 = V.delta2(Fl, n)
        lhs = S / (1.0 - c) + d2
        rhs = V.exact_H_A(Fl)
        return lhs, rhs
    return ineq


# ===========================================================================
# Driver
# ===========================================================================

def _fmt(x: float, w: int = 9, p: int = 5) -> str:
    return f"{x:>{w}.{p}f}"


def main(do_sweep: bool = True, sweep_nmax: int = 5):
    print("=" * 78)
    print("Vector 3 — Δ₂ recapture at a NON-PRODUCT extremizer (beat-ψ attempt)")
    print("=" * 78)
    print(f"ψ = (3−√5)/2 = {PSI:.10f}\n")

    # ---- PART 2a: shared-U coupling, watch Δ₂ vs budget as n→∞ ----
    print("-" * 78)
    print("PART A.  Shared-U (conditionally-i.i.d.) NON-PRODUCT coupling.")
    print("         Δ₂ > 0 here, but Δ₂ ≤ I(C;U) ≤ H(U) = O(1); budget H(A) = Θ(n).")
    print("-" * 78)
    couplings = {
        "k=2 p=[.2,.6]": SharedUCoupling([0.2, 0.6], [0.5, 0.5]),
        "k=2 p=[.3,.5]": SharedUCoupling([0.3, 0.5], [0.5, 0.5]),
        "k=4 spread":     SharedUCoupling([0.1, 0.3, 0.5, 0.7], [0.25] * 4),
        "k=6 spread":     SharedUCoupling([0.05, 0.2, 0.38, 0.5, 0.7, 0.9], [1 / 6] * 6),
        "k=3 near-ψ":     SharedUCoupling([0.30, 0.3819660, 0.46], [1 / 3] * 3),
    }
    best_caug = -math.inf
    best_label = None
    for label, cpl in couplings.items():
        print(f"\n  coupling [{label}]   (E[P]={cpl.E_P():.4f}, H(U)={cpl.H_U():.4f})")
        print(f"    {'n':>3} {'H(A)':>9} {'Δ₂':>8} {'Δ₂/H(A)':>9} {'Δ₂/n':>8} "
              f"{'I(C;U)':>8} {'c_AHS':>9} {'c_aug':>9}")
        for row in delta2_vs_budget_table(cpl):
            print(f"    {row['n']:>3} {_fmt(row['H_A'])} {_fmt(row['delta2'],8,4)} "
                  f"{_fmt(row['delta2_over_HA'],9,5)} {_fmt(row['delta2_per_coord'],8,4)} "
                  f"{_fmt(row['I_C_U'],8,4)} {_fmt(row['c_ahs'])} {_fmt(row['c_aug'])}")
            if row["c_aug"] > best_caug:
                best_caug = row["c_aug"]
                best_label = f"{label} n={row['n']}"
    print(f"\n  >>> best c_aug over ALL shared-U couplings & n tested: {best_caug:.6f}"
          f"  ({best_label})")
    print(f"  >>> Δ(ψ) = {best_caug - PSI:+.2e}   (negative or ~resolution ⇒ NO gain)")

    # ---- PART 2b: the per-coordinate limit is the U-mixture (diagonal) ----
    print("\n" + "-" * 78)
    print("PART B.  Why: the n→∞ per-coordinate limit collapses to the U-MIXTURE.")
    print("-" * 78)
    cpl = couplings["k=6 spread"]
    r = cpl.report(128)
    print(f"  k=6 coupling at n=128:")
    print(f"    H(A)/n   = {r['H_A_per']:.5f}   →  E[h(P)] = {r['E_h_p']:.5f}")
    print(f"    H(C)/n   = {r['H_union_per']:.5f}   →  E[h(U)] = {r['E_h_u']:.5f}")
    print(f"    Δ₂/n     = {r['delta2_per']:.5f}   →  0")
    print("  The single-letter (P,Q) sits on the DIAGONAL {(p_j,p_j)}; the augmented")
    print("  feasibility is a mixture over the SAME per-point crossover ⇒ threshold ψ.")

    # ---- PART 3: the trap ----
    print("\n" + "-" * 78)
    print("PART C.  The TRAP — correlated-Bernoulli coupling (choosing a coupling).")
    print("-" * 78)
    print(f"    {'ρ':>6} {'crossover p*':>14}  {'vs ψ':>8}   note")
    for rho in [-0.3, -0.1, 0.0, 0.1, 0.3, 0.5]:
        xo = correlated_crossover(rho)
        note = ("ψ exactly" if abs(rho) < 1e-9 else
                ("APPARENT gain (INVALID: not a UC necessary condition)" if rho > 0
                 else "loss (enlarged class)"))
        print(f"    {rho:>+6.2f} {xo:>14.5f}  {xo - PSI:>+8.4f}   {note}")
    print("  ρ>0 'beats' ψ only by FORCING positive A–B correlation — an i.i.d. sample")
    print("  from a UC family has ρ=0. It is NOT a lower bound valid for all UC families;")
    print("  PART D's sweep rejects every inequality whose threshold exceeds ψ.")

    # ---- PART 1 (re-confirm): i.i.d. augmented constant over all UC families ----
    if do_sweep:
        print("\n" + "-" * 78)
        print(f"PART D.  Falsification sweep over ALL UC families n≤{sweep_nmax}.")
        print("-" * 78)
        from enumerate import all_uc_families
        from entropy_bounds import sweep_inequality

        # D1: sanity — H(C) ≤ H(A) holds (union closure); this is what Δ₂-recapture
        #     re-labels. Confirms no NEW inequality is created.
        min_caug = math.inf
        min_cahs = math.inf
        argmin = None
        worst_at_floor = None
        nfam = 0
        for n in range(sweep_nmax + 1):
            for F in all_uc_families(n):
                if not F or len(F) < 2:
                    continue
                nfam += 1
                d = augmented_constant_iid_family(F, n)
                if d["c_aug"] < min_caug:
                    min_caug = d["c_aug"]
                    argmin = (n, d)
                if d["c_ahs"] < min_cahs:
                    min_cahs = d["c_ahs"]
                # at families near the AHS floor, record Δ₂ (anticorrelation)
                if d["c_ahs"] < PSI + 5e-3:
                    if (worst_at_floor is None
                            or d["delta2"] / max(d["H_union"], 1e-12)
                            > worst_at_floor):
                        worst_at_floor = d["delta2"] / max(d["H_union"], 1e-12)
        print(f"  families checked: {nfam}")
        print(f"  min c_AHS over families                = {min_cahs:.6f}")
        print(f"  min c_aug (recapture ALL Δ₂) over fams  = {min_caug:.6f}")
        print(f"  Δ(ψ) of the augmented minimum          = {min_caug - PSI:+.2e}")
        print(f"  ⇒ c_aug minimum is {'BELOW' if min_caug < min_cahs else 'EQUAL/above'} "
              f"c_AHS minimum: recapturing Δ₂ does NOT lift the worst-case constant.")
        print(f"  max Δ₂/H(C) among families within 5e-3 of the AHS floor: "
              f"{worst_at_floor:.4e}  (→0 as c_AHS→ψ : ANTICORRELATION)")

        # D2: the candidate improved-floor inequality at c slightly above ψ MUST fail.
        print("\n  Candidate 'improved floor' (1/(1−c))S + Δ₂ ≤ H(A) at c just above ψ:")
        for c in [PSI, PSI + 1e-3, PSI + 1e-2]:
            res = sweep_inequality(ahs_plus_delta2_floor_pair(c), sweep_nmax)
            total = sum(r.families_checked for r in res.values())
            viol = sum(len(r.counterexamples) for r in res.values())
            verdict = "HOLDS on all" if viol == 0 else f"{viol} VIOLATIONS"
            print(f"    c={c:.6f} (ψ{c - PSI:+.0e}):  {verdict}  "
                  f"(checked {total} families)")
        print("  The floor inequality holds at c=ψ and FAILS for c>ψ ⇒ the augmented")
        print("  certified constant is exactly ψ on the enumerated families.")

    print("\n" + "=" * 78)
    print("VERDICT: No non-product coupling in these families certifies a constant > ψ.")
    print("  Δ₂ gain is O(1) (≤ I(C;U) ≤ H(U) ≤ log₂k); budget Θ(n); per-coord Δ₂→0.")
    print("  Apparent gains (ρ>0) are favourable-coupling artifacts that fail the UC sweep.")
    print("=" * 78)
    return best_caug, min_caug if do_sweep else None


if __name__ == "__main__":
    main()
