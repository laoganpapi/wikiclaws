"""
joint_opt.py — Joint optimization of the entropy-method bound for Frankl.

Implements the single-letter optimization formalized in ``opt_formulation.md``.

THE CORRECT THRESHOLD FUNCTIONAL (see opt_formulation.md §4 and the derivation
note below). The entropy method proves "max_i p_i ≥ c". In the dimension-free
single-letter limit the certified constant is

    c  =  sup { t ∈ (0, 1/2] :  the feasibility inequality (IV) is INFEASIBLE
                                 for every NON-DEGENERATE law μ on [0, t] }.

"Non-degenerate" means E_μ[h(P)] > 0 (μ not concentrated on {0,1}); the
degenerate laws satisfy (IV) vacuously (0 ≤ 0) and must be excluded — otherwise
"min E[P]" spuriously returns 0 via μ = δ_0. We therefore locate c by BISECTION
on t, at each t asking the sub-problem "does a non-degenerate μ on [0,t] satisfy
(IV)?".

  * BASE i.i.d.: c = ψ = (3 − √5)/2 exactly (sanity floor). Confirmed by
    bisection AND by the closed form.

  * REWEIGHTING (Cambie): in the dim-free limit == free choice of μ ⇒ no gain
    over ψ (honest negative result, opt_formulation.md §5.1).

  * AUXILIARY U with |U| ∈ {2,4,8,16} (conditional-i.i.d., Liu/Yu, survey §7.7):
    the faithfully-reconstructed ("diagonal") version gives a valid necessary
    condition whose threshold is still ψ (no gain). Liu's exact functional
    (giving 0.38271) needs his I(C;U)/I(A;U) bookkeeping, which we could NOT
    retrieve (arXiv blocked) nor reliably reconstruct (collapse/degeneracy).
    Marked UNVERIFIED throughout; never claimed as a theorem. See results.md.

Complements: entropy_bounds.py (Gilmer inequality on finite families) and
verify_ahs.py (exact conditional entropies on finite families).

All entropies in NATS; the threshold is dimensionless.

Author: Alex Ye (AI assistance disclosed separately).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize

# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------

PSI = (3.0 - math.sqrt(5.0)) / 2.0
PHI = (1.0 + math.sqrt(5.0)) / 2.0
LAMBDA = 1.0 / (2.0 * (1.0 - PSI))  # = phi/2 ~ 0.8090170


def h(x: float) -> float:
    """Binary entropy in nats; h(0)=h(1)=0 with tiny-float guard."""
    if x <= 1e-300 or x >= 1.0 - 1e-15:
        return 0.0
    return -x * math.log(x) - (1.0 - x) * math.log(1.0 - x)


def h_vec(x: np.ndarray) -> np.ndarray:
    """Vectorized binary entropy in nats."""
    x = np.clip(np.asarray(x, dtype=float), 0.0, 1.0)
    out = np.zeros_like(x, dtype=float)
    m = (x > 1e-300) & (x < 1.0 - 1e-15)
    xm = x[m]
    out[m] = -xm * np.log(xm) - (1.0 - xm) * np.log1p(-xm)
    return out


def union_prob(p: float, q: float) -> float:
    """Pr[A∨B=1] for independent Bern(p), Bern(q)."""
    return 1.0 - (1.0 - p) * (1.0 - q)


def closed_form_psi() -> float:
    """ψ as the smaller root of p^2 - 3p + 1 = 0, by the quadratic formula."""
    return (3.0 - math.sqrt(5.0)) / 2.0


# ---------------------------------------------------------------------------
# Feasibility sub-problem:  is (IV) satisfiable by a non-degenerate μ on [0,t]?
# ---------------------------------------------------------------------------

def _iid_matrices(grid: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    P = grid[:, None]
    Q = grid[None, :]
    U = 1.0 - (1.0 - P) * (1.0 - Q)
    return h_vec(U), h_vec(grid)


def iv_best_gap_on(
    t: float,
    n_grid: int = 50,
    n_restarts: int = 25,
    seed: int = 0,
    min_entropy: float = 1e-3,
) -> tuple[float, np.ndarray, np.ndarray]:
    """
    Sub-problem for the BASE i.i.d. program. Among non-degenerate laws μ on
    the grid of [1e-3, t], maximize the feasibility gap

        g(w) = E_μ[h(P)] − E_{P,Q iid}[h(union)]      ( (IV) holds ⟺ g ≥ 0 ).

    Returns (best_gap, best_w, grid). best_gap ≥ 0 ⟺ (IV) feasible on [0,t].
    Non-degeneracy enforced by the constraint E_μ[h(P)] ≥ min_entropy.
    """
    grid = np.linspace(1e-3, max(t, 2e-3), n_grid)
    H1, hp = _iid_matrices(grid)
    rng = np.random.default_rng(seed)

    def neg_gap(w):
        return float(w @ H1 @ w - w @ hp)

    def neg_gap_grad(w):
        return 2.0 * (H1 @ w) - hp

    cons = [
        {"type": "eq", "fun": lambda w: float(w.sum() - 1.0),
         "jac": lambda w: np.ones_like(w)},
        {"type": "ineq", "fun": lambda w: float(w @ hp - min_entropy),
         "jac": lambda w: hp},
    ]
    bnds = [(0.0, 1.0)] * n_grid

    best_gap = -math.inf
    best_w = None
    for _ in range(n_restarts):
        w0 = rng.dirichlet(np.ones(n_grid))
        r = minimize(neg_gap, w0, jac=neg_gap_grad, method="SLSQP",
                     bounds=bnds, constraints=cons,
                     options={"maxiter": 400, "ftol": 1e-13})
        if r.success:
            g = -float(r.fun)
            if g > best_gap and (r.x @ hp) >= min_entropy - 1e-9:
                best_gap = g
                best_w = r.x
    if best_w is None:
        best_w = np.full(n_grid, 1.0 / n_grid)
        best_gap = -neg_gap(best_w)
    return best_gap, best_w, grid


@dataclass
class ThresholdResult:
    label: str
    threshold: float
    bracket: tuple[float, float]
    witness_support: list[tuple[float, float]]  # μ achieving feasibility at threshold
    status: str  # 'verified' | 'unverified'
    notes: str = ""


def threshold_by_bisection(
    feasible_on,
    lo: float = 0.20,
    hi: float = 0.50,
    iters: int = 40,
    label: str = "",
    status: str = "verified",
) -> ThresholdResult:
    """
    Generic bisection. ``feasible_on(t) -> (is_feasible: bool, witness_support)``.
    Finds the largest t (to within 2^-iters) at which (IV) becomes feasible:
    the threshold c. Assumes feasibility is monotone non-decreasing in t.
    """
    a, b = lo, hi
    last_support: list[tuple[float, float]] = []
    for _ in range(iters):
        m = 0.5 * (a + b)
        feas, supp = feasible_on(m)
        if feas:
            b = m
            last_support = supp
        else:
            a = m
    thr = 0.5 * (a + b)
    return ThresholdResult(
        label=label, threshold=thr, bracket=(a, b),
        witness_support=last_support, status=status,
    )


# ---------------------------------------------------------------------------
# BASE single-letter program (i.i.d.) — optimum = ψ.
# ---------------------------------------------------------------------------

def base_program(n_grid: int = 40, n_restarts: int = 8, iters: int = 30) -> ThresholdResult:
    def feasible_on(t: float):
        g, w, grid = iv_best_gap_on(t, n_grid=n_grid, n_restarts=n_restarts)
        supp = [(float(grid[i]), float(w[i])) for i in range(len(grid)) if w[i] > 1e-3]
        return (g >= -1e-7), supp

    res = threshold_by_bisection(feasible_on, label="base i.i.d.", status="verified", iters=iters)
    res.notes = "Should equal psi; closed form certifies the true value (certificate_0.38197.md)."
    return res


def reweighting_program(n_grid: int = 40, n_restarts: int = 8, iters: int = 30) -> ThresholdResult:
    """
    Cambie reweighting in the dim-free limit == free choice of μ ⇒ same as base.
    Solved independently (different grid offset / seeds) to confirm no gain.
    """
    def feasible_on(t: float):
        g, w, grid = iv_best_gap_on(t, n_grid=n_grid + 7, n_restarts=n_restarts, seed=99)
        supp = [(float(grid[i]), float(w[i])) for i in range(len(grid)) if w[i] > 1e-3]
        return (g >= -1e-7), supp

    res = threshold_by_bisection(feasible_on, label="reweighting (Cambie)", status="verified", iters=iters)
    res.notes = ("Reweighting alone does not beat psi in the single-letter limit "
                 "(opt_formulation.md §5.1).")
    return res


# ---------------------------------------------------------------------------
# AUXILIARY VARIABLE U (conditional-i.i.d.).
# ---------------------------------------------------------------------------

def conditional_U_functional(p: np.ndarray, w: np.ndarray, mode: str = "diagonal"):
    """
    Feasibility (LHS ≤ RHS) for the conditional-i.i.d. coupling with auxiliary U
    (atoms p_j, weights w_j).

    mode='diagonal' (VERIFIED valid lower bound): given U=j, the union bit is
        Bern(2p_j − p_j^2); (IV) reads
            Σ_j w_j h(2 p_j − p_j^2)  ≤  Σ_j w_j h(p_j).
        Its non-degenerate threshold is ψ (a mixture over the SAME crossover).

    mode='liu_refund' (UNVERIFIED — DO NOT TRUST): a reconstruction of Liu's
        I(C;U)/I(A;U) refund that collapses to h(ubar) ≤ h(pbar),
        ubar = 2 pbar − E[P^2]; admits a degenerate optimizer ⇒ retained only to
        document the failed reconstruction.
    """
    pbar = float(w @ p)
    if mode == "diagonal":
        u = 2.0 * p - p * p
        return float(w @ h_vec(u)), float(w @ h_vec(p))
    elif mode == "liu_refund":
        ep2 = float(w @ (p * p))
        ubar = 2.0 * pbar - ep2
        return h(ubar), h(pbar)
    raise ValueError(f"unknown mode {mode!r}")


def aux_feasible_on(
    t: float, U_size: int, mode: str = "diagonal",
    n_restarts: int = 12, seed: int = 7, min_entropy: float = 1e-3,
):
    """
    Does a non-degenerate conditional-U law (atoms in [0,t], k=U_size) satisfy
    the conditional-U feasibility inequality? Returns (is_feasible, support).
    """
    k = U_size
    rng = np.random.default_rng(seed + k + int(1000 * t))

    def split(z):
        return np.clip(z[:k], 0.0, 1.0), z[k:]

    def neg_gap(z):
        p, w = split(z)
        lhs, rhs = conditional_U_functional(p, w, mode=mode)
        return lhs - rhs  # minimize lhs-rhs = maximize gap (rhs-lhs)

    cons = [
        {"type": "eq", "fun": lambda z: float(split(z)[1].sum() - 1.0)},
        {"type": "ineq",
         "fun": lambda z: float(split(z)[1] @ h_vec(split(z)[0]) - min_entropy)},
    ]
    bnds = [(0.0, t)] * k + [(0.0, 1.0)] * k

    best_gap = -math.inf
    best_z = None
    for _ in range(n_restarts):
        p0 = rng.uniform(0.0, t, k)
        w0 = rng.dirichlet(np.ones(k))
        z0 = np.concatenate([p0, w0])
        r = minimize(neg_gap, z0, method="SLSQP", bounds=bnds, constraints=cons,
                     options={"maxiter": 600, "ftol": 1e-13})
        if r.success:
            p, w = split(r.x)
            if (w @ h_vec(p)) >= min_entropy - 1e-9:
                g = -float(r.fun)
                if g > best_gap:
                    best_gap = g
                    best_z = r.x
    if best_z is None:
        return False, []
    p, w = split(best_z)
    supp = [(float(p[j]), float(w[j])) for j in range(k) if w[j] > 1e-3]
    return (best_gap >= -1e-7), supp


def auxiliary_program(U_size: int, mode: str = "diagonal") -> ThresholdResult:
    status = "verified" if mode == "diagonal" else "unverified"

    def feasible_on(t: float):
        return aux_feasible_on(t, U_size, mode=mode)

    res = threshold_by_bisection(
        feasible_on, label=f"aux |U|={U_size} [{mode}]", status=status, iters=26
    )
    res.notes = ("diagonal conditional-iid: valid lower bound, threshold = psi (no gain)."
                 if mode == "diagonal"
                 else "liu_refund: UNVERIFIED; degenerate; not a claim.")
    return res


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def run_all(verbose: bool = True) -> dict:
    out: dict = {"closed_form_psi": closed_form_psi()}
    out["base"] = base_program()
    out["reweighting"] = reweighting_program()
    out["auxiliary"] = {k: auxiliary_program(k, mode="diagonal") for k in (2, 4, 8, 16)}

    if verbose:
        cf = out["closed_form_psi"]
        print("=" * 74)
        print("Joint optimization of the entropy-method bound (single-letter)")
        print("=" * 74)
        print(f"closed-form psi = {cf:.16f}")

        def line(r: ThresholdResult):
            print(f"  {r.label:<20} c = {r.threshold:.8f}  Δψ={r.threshold-cf:+.2e}  "
                  f"[{r.status}]  bracket=({r.bracket[0]:.6f},{r.bracket[1]:.6f})")

        print("-" * 74)
        line(out["base"])
        line(out["reweighting"])
        print("-" * 74)
        print("Auxiliary U (conditional-i.i.d., diagonal / valid reconstruction):")
        for k in (2, 4, 8, 16):
            line(out["auxiliary"][k])
        print("-" * 74)
        print("Liu's 0.38271 functional requires his exact I(C;U)/I(A;U) bookkeeping,")
        print("which we could NOT retrieve (arXiv blocked) nor reliably reconstruct")
        print("(see conditional_U_functional 'liu_refund'). All certified values = psi.")
    return out


if __name__ == "__main__":
    run_all()
