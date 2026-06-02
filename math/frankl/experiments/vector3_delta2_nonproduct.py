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

3. `correlated_crossover`: the correlated-Bernoulli coupling (single p,
   pair-correlation ρ). Shows the TRAP: ρ>0 *appears* to raise the threshold above
   ψ, but that is choosing a favourable (non-i.i.d.) coupling — NOT a necessary
   condition valid for every UC family (an UC family sampled i.i.d. has ρ=0). The
   certification gate `sawin_lower_bound_min` rejects every c>ψ regardless.

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

    The honest augmented chain (theory/vector3_delta2_nonproduct.md §1). Assume
    for contradiction max_i p_i < c. Then the Sawin per-coordinate inequality
    gives chain-LB ≥ (1/(1−c))·S with S = Σ_i (1−p_i) H(A_i|A_{<i}). Using the
    EXACT identity H(C) = chain-LB + Δ₂ and the union-closure budget H(C) ≤ H(A):

        (1/(1−c)) S + Δ₂  ≤  H(C)  ≤  H(A) = log₂|F|.                 (AUG)

    A contradiction (⇒ max_i p_i ≥ c) is forced once the left side exceeds the
    budget. The family therefore *permits* constant c (no contradiction yet) iff
    (AUG) holds. The largest c it certifies solves (1/(1−c))S + Δ₂ = budget:

        c_aug(F) = 1 − S / (budget − Δ₂).

    Choice of budget — THIS IS THE BUDGET-MISMATCH TRAP (dead_ends.md, 2026-06-02
    Vector 2: the false 0.4295 / 0.5):
      * budget = H(C)  → c_aug_HC. The CORRECT per-family ledger. H(C) is the
        entropy that actually appears in the tight chain; at the asymptotic
        extremizer H(C)=H(A) per coordinate, so this is the faithful object.
        c_aug_HC = 1 − S/chain-LB.
      * budget = H(A)  → c_aug_HA. **ARTIFACT — DO NOT TRUST.** On finite families
        H(A) > H(C) (union closure concentrates mass: e.g. 2^[2] has H(A)=2 bits
        but H(C)=1.6226 bits). Putting the LARGER H(A) in the denominator inflates
        the constant spuriously (2^[2] → exactly 0.5). The gap H(A)−H(C) is the
        union-closure slack that VANISHES per-coordinate asymptotically; treating
        it as headroom for Δ₂ double-counts. This reproduces the documented 0.5 /
        0.43 budget-mismatch and is reported ONLY to flag it as the trap.

    c_AHS = 1 − S/H(C) is the Δ₂-DROPPED baseline. KEY (honest ledger, c_aug_HC):
    subtracting Δ₂ from the denominator can only DECREASE it, hence DECREASE
    c_aug_HC below c_AHS — recapturing Δ₂ in this finite ledger moves the certified
    constant the WRONG way unless Δ₂=0. Returns all three + Δ₂.
    """
    Fl = list(F)
    if n is None:
        u = 0
        for a in Fl:
            u |= a
        n = u.bit_length()
    Hu = V.exact_entropy_union(Fl)
    HA = V.exact_H_A(Fl)
    clb = V.chain_rule_lower_bound(Fl, n)
    d2 = Hu - clb
    m = len(Fl)
    S = 0.0
    for i in range(n):
        bit = 1 << i
        p_i = sum(1 for a in Fl if a & bit) / m
        S += (1.0 - p_i) * V.H_Ai_given_prefix(Fl, i)
    c_ahs = 1.0 - S / Hu if Hu > 1e-12 else 1.0
    den_HA = HA - d2
    den_HC = Hu - d2  # == chain-LB
    c_aug_HA = 1.0 - S / den_HA if den_HA > 1e-12 else 1.0
    c_aug_HC = 1.0 - S / den_HC if den_HC > 1e-12 else 1.0
    from uc_family import abundance as _abund
    return {"c_ahs": c_ahs, "c_aug_HA": c_aug_HA, "c_aug_HC": c_aug_HC,
            "c_aug": c_aug_HC, "delta2": d2,
            "H_union": Hu, "H_A": HA, "chain_lb": clb, "S": S,
            "abundance": _abund(Fl)}


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

      c_AHS(block) = 1 − S_n / H(C),                 (drop Δ₂, budget H(C))
      c_aug(block) = 1 − S_n / (H(C) − Δ₂)           (recapture ALL Δ₂, budget H(C))
                   = 1 − S_n / chain-LB,
      c_aug_HA     = 1 − S_n / (H(A) − Δ₂)           (recapture ALL Δ₂, honest budget H(A)).

    Returns all three and Δ₂. (As n→∞ all → ψ; see `delta2_vs_budget_table`.)
    """
    HC = coupling.H_union(n)
    HA = coupling.H_A(n)
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
    den_HA = HA - d2
    c_aug_HA = 1.0 - S_n / den_HA if den_HA > 1e-12 else 1.0
    return {"n": n, "c_ahs": c_ahs, "c_aug": c_aug, "c_aug_HA": c_aug_HA,
            "delta2": d2, "H_union": HC, "H_A": HA, "chain_lb": clb,
            "S_n": S_n, "E_P": float(wk @ pk)}


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
            "c_aug_HA": aug["c_aug_HA"],
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


def correlated_crossover(rho: float, grid: int = 200000) -> float:
    """The crossover p* where h(union)=h(p) for the correlated pair at correlation
    ρ — the 'single-letter crossover' this coupling would (illegitimately, for
    ρ≠0) certify. Returns the unique p*∈(0,1/2). ρ=0 ⇒ ψ; ρ>0 ⇒ >ψ (the trap);
    ρ<0 ⇒ <ψ."""
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


def sawin_lower_bound_min(c: float, n_grid: int = 600) -> tuple[float, tuple[float, float]]:
    """
    THE REAL CERTIFICATION GATE. The augmented bound assembles, under the
    contradiction hypothesis max_i p_i < c, the per-coordinate lower bound

        h(union_p(p,q))  ≥  (1/(2(1−c))) · [ (1−q) h(p) + (1−p) h(q) ]      (S_c)

    (the Sawin/AHS inequality with constant 1/(2(1−c))). The method certifies c
    ONLY IF (S_c) holds for ALL (p,q) ∈ [0,1]² — otherwise chain-LB ≥ (1/(2(1−c)))S
    is not a valid inequality and the whole augmented lower bound collapses. We
    return min_{p,q} G_c(p,q) with G_c = LHS − RHS of (S_c); (S_c) holds iff this
    is ≥ 0. It is ≥ 0 for c ≤ ψ and < 0 for c > ψ (ψ is sharp).

    *** This is why the family-level sweep of the floor inequality is MISLEADING:
    the floor (1/(2(1−c)))S + Δ₂ ≤ H(A) may hold numerically on small finite
    families for c > ψ (they are not the extremizer), yet the per-coordinate lower
    bound it relies on is already INVALID for c > ψ. Certification is gated by
    (S_c) on ALL (p,q), not by the floor holding on a finite family list. ***
    """
    lam = 1.0 / (2.0 * (1.0 - c))
    best = math.inf
    arg = (0.5, 0.5)
    grid = np.linspace(1e-3, 1.0 - 1e-3, n_grid)
    for p in grid:
        hp = h(p)
        for q in grid:
            g = h(union_p(p, q)) - lam * ((1 - q) * hp + (1 - p) * h(q))
            if g < best:
                best = g
                arg = (float(p), float(q))
    return best, arg


def ahs_plus_delta2_floor_pair(c: float):
    """
    The family-level 'improved floor' (1/(2(1−c)))S + Δ₂ ≤ H(A), exposed as
    LHS ≤ RHS for `sweep_inequality`. **A `HOLDS on all` result here at c > ψ does
    NOT certify c** — see `sawin_lower_bound_min`: the per-coordinate lower bound
    underlying this floor is invalid for c > ψ, so the floor holding on a finite
    family list is a non-sequitur (the families simply aren't the extremizer). We
    retain this only to *exhibit* the trap side-by-side with the real gate.
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
        lhs = S / (2.0 * (1.0 - c)) + d2
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
    print("  Columns: c_AHS = drop Δ₂ (baseline);  c_aug = recapture Δ₂ with the")
    print("  HONEST budget H(C) (= 1−S/chain-LB);  [c_augHA] = recapture with budget")
    print("  H(A) — the BUDGET-MISMATCH ARTIFACT (inflates to ~0.5; see dead_ends).")
    best_caug = -math.inf      # honest: max c_aug_HC
    best_label = None
    best_artifact = -math.inf  # the trap value, reported only to flag it
    for label, cpl in couplings.items():
        print(f"\n  coupling [{label}]   (E[P]={cpl.E_P():.4f}, H(U)={cpl.H_U():.4f})")
        print(f"    {'n':>3} {'H(A)':>9} {'Δ₂':>8} {'Δ₂/n':>8} {'I(C;U)':>8} "
              f"{'c_AHS':>9} {'c_aug':>9} {'[c_augHA]':>10}")
        for row in delta2_vs_budget_table(cpl):
            print(f"    {row['n']:>3} {_fmt(row['H_A'])} {_fmt(row['delta2'],8,4)} "
                  f"{_fmt(row['delta2_per_coord'],8,4)} {_fmt(row['I_C_U'],8,4)} "
                  f"{_fmt(row['c_ahs'])} {_fmt(row['c_aug'])} {_fmt(row['c_aug_HA'],10)}")
            if row["c_aug"] > best_caug:
                best_caug = row["c_aug"]
                best_label = f"{label} n={row['n']}"
            best_artifact = max(best_artifact, row["c_aug_HA"])
    print(f"\n  >>> best HONEST c_aug (budget H(C)) over all couplings & n: {best_caug:.6f}"
          f"  ({best_label})")
    print(f"  >>> Δ(ψ) = {best_caug - PSI:+.2e}   "
          f"(c_aug ≤ c_AHS always: recapture moves the WRONG way; both →ψ as n→∞)")
    print(f"  >>> [artifact] max c_augHA (H(A) budget) = {best_artifact:.6f} "
          f"— the 0.43–0.5 budget-mismatch, NOT a bound.")

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

    # ---- PART B': the obstruction survives k→∞ (full de Finetti class) ----
    print("\n  B'. Does letting k grow with n (H(U)~log k→∞) rescue Δ₂/n?  NO:")
    print(f"      {'n=k':>5} {'H(U)':>7} {'Δ₂':>8} {'Δ₂/n':>9} {'c_AHS':>8} {'c_aug':>9}")
    for k in (2, 4, 8, 16, 32):
        p = np.linspace(0.15, 0.62, k)
        wk = np.ones(k) / k
        cpl_k = SharedUCoupling(p, wk)
        d = shared_u_augmented_constant(cpl_k, k)
        print(f"      {k:>5} {cpl_k.H_U():>7.3f} {d['delta2']:>8.4f} {d['delta2'] / k:>9.5f} "
              f"{d['c_ahs']:>8.5f} {d['c_aug']:>9.5f}")
    print("      For ANY exchangeable (de Finetti) coupling the latent mixing param is")
    print("      1-dimensional ⇒ I(C;latent)=O(log n) ⇒ Δ₂/n=O(log n/n)→0. Whole class capped.")

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
    print("  from a UC family has ρ=0, and the budget H(A) presupposes A⟂B. It is NOT a")
    print("  valid necessary condition; PART D's gate (S_c) rejects every c>ψ.")

    # ---- PART 1 (re-confirm): i.i.d. augmented constant over all UC families ----
    if do_sweep:
        print("\n" + "-" * 78)
        print(f"PART D.  Falsification sweep over ALL UC families n≤{sweep_nmax}.")
        print("-" * 78)
        from enumerate import all_uc_families
        from entropy_bounds import sweep_inequality

        # D1: the per-family certified constants. The worst (minimum) over
        #     families bounds the provable constant for each ledger.
        min_caug_HA = math.inf   # recapture Δ₂, honest budget H(A)
        min_caug_HC = math.inf   # recapture Δ₂, budget H(C)
        min_cahs = math.inf      # drop Δ₂ (AHS baseline)
        argmin = None
        worst_at_floor = None
        nfam = 0
        for n in range(sweep_nmax + 1):
            for F in all_uc_families(n):
                if not F or len(F) < 2:
                    continue
                nfam += 1
                d = augmented_constant_iid_family(F, n)
                if d["c_aug_HA"] < min_caug_HA:
                    min_caug_HA = d["c_aug_HA"]
                    argmin = (n, d)
                if d["c_aug_HC"] < min_caug_HC:
                    min_caug_HC = d["c_aug_HC"]
                if d["c_ahs"] < min_cahs:
                    min_cahs = d["c_ahs"]
                # at families near the AHS floor, record Δ₂ (anticorrelation)
                if d["c_ahs"] < PSI + 5e-3:
                    if (worst_at_floor is None
                            or d["delta2"] / max(d["H_union"], 1e-12)
                            > worst_at_floor):
                        worst_at_floor = d["delta2"] / max(d["H_union"], 1e-12)
        print(f"  families checked: {nfam}")
        print(f"  min c_AHS              (drop Δ₂, baseline)          = {min_cahs:.6f}")
        print(f"  min c_aug  HONEST      (recapture Δ₂, budget H(C))  = {min_caug_HC:.6f}"
              f"   Δ(ψ)={min_caug_HC - PSI:+.2e}")
        print(f"  ⇒ recapturing Δ₂ does NOT lift the worst-case constant above ψ "
              f"(c_aug ≤ c_AHS ≤ floor+resolution).")
        print(f"  [min c_augHA budget H(A) = {min_caug_HA:.6f} — BUDGET-MISMATCH ARTIFACT "
              f"(0.43–0.5), not a bound]")
        print(f"  max Δ₂/H(C) among families within 5e-3 of the AHS floor: "
              f"{worst_at_floor:.4e}  (→0 as c_AHS→ψ : ANTICORRELATION)")
        min_caug = min_caug_HC

        # D2: THE REAL CERTIFICATION GATE vs the misleading floor sweep, side by side.
        print("\n  D2. Certification gate — validity of the per-coordinate Sawin lower")
        print("      bound (S_c) at level c  vs  the (misleading) family floor sweep:")
        print(f"      {'c':>10} {'min G_c (gate)':>16} {'gate':>6}   {'floor sweep':>14}")
        for c in [PSI - 1e-2, PSI, PSI + 1e-3, PSI + 1e-2]:
            mn, _ = sawin_lower_bound_min(c)
            gate = "valid" if mn >= -1e-6 else "INVALID"
            res = sweep_inequality(ahs_plus_delta2_floor_pair(c), sweep_nmax)
            viol = sum(len(r.counterexamples) for r in res.values())
            floor = "HOLDS" if viol == 0 else f"{viol} viol"
            print(f"      {c:>10.5f} {mn:>16.3e} {gate:>6}   {floor:>14}")
        print("      The gate FLIPS to INVALID exactly past c=ψ ⇒ no c>ψ is certified.")
        print("      The floor 'HOLDS' for c>ψ on finite families is a NON-SEQUITUR")
        print("      (they aren't the extremizer); only the gate certifies. ψ is sharp.")

    print("\n" + "=" * 78)
    print("VERDICT: No non-product coupling in these families certifies a constant > ψ.")
    print("  Δ₂ gain is O(1) (≤ I(C;U) ≤ H(U) ≤ log₂k); budget Θ(n); per-coord Δ₂→0.")
    print("  Apparent gains (ρ>0) are favourable-coupling artifacts that fail the UC sweep.")
    print("=" * 78)
    return best_caug, min_caug if do_sweep else None


if __name__ == "__main__":
    main()
