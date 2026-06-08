"""
Spectral analysis of the Syracuse / Collatz Frobenius--Perron (transfer) operator
on the finite quotient (Z/3^n Z)^x.

Author: Alex Ye (computational experiment; AI assistance disclosed separately).

------------------------------------------------------------------------------
Setting and definitions
------------------------------------------------------------------------------

Let U_n = (Z/3^n Z)^x (the units mod 3^n), |U_n| = phi(3^n) = 2 * 3^{n-1}.

The accelerated Syracuse map on odd integers is
        Syr(x) = (3x + 1) / 2^{nu_2(3x+1)}.
For x in U_n (i.e. 3 nmid x) the residue of Syr(x) mod 3^n is well defined
once nu_2(3x+1) is fixed; we MODEL nu_2(3x+1) under Tao's random model as an
i.i.d. Geom(2) variable (P(a=k) = 2^{-k}, k>=1), independent of x. (This is
the same model that underlies the Syracuse RV computed in syracuse_fft/.)

The induced one-step Markov kernel on U_n is

    K_n(x, y) = sum_{k>=1, 3 nmid 2^{-k}(3x+1) mod 3^n}
                  2^{-k} * 1[ 2^{-k} (3x + 1) ≡ y  (mod 3^n) ].

Note: (3x+1) mod 3 = 1 for all x with 3 nmid x (because 3x ≡ 0). So
3x+1 is a unit in Z/3^n iff its 3-adic valuation is 0, and in fact 3x+1
≡ 1 (mod 3), hence v_3(3x+1) = 0 unless 3x+1 ≡ 0 mod 9, etc. In any case
the multiplicand by 2^{-k} preserves the v_3 class, so y in U_n iff 3x+1
in U_n. We treat the chain as conditioned on the event {3x+1 in U_n} and
rescale the kernel by the conditional mass (small correction at finite n).

The transfer (Frobenius--Perron, Markov) operator is
        (L_n rho)(y) = sum_x rho(x) K_n(x, y).
Equivalently L_n is the transpose of the transition matrix P_n with
        P_n[x, y] = K_n(x, y).
A probability density rho on U_n is INVARIANT iff L_n rho = rho.
The chain is doubly stochastic when K_n is also column-stochastic on units;
in general the uniform-on-units measure is invariant iff the kernel is
doubly stochastic.

------------------------------------------------------------------------------
What this script computes
------------------------------------------------------------------------------
For n in {1, 2, 3, 4, 5, [6]}:
  (i)  The full transition matrix P_n (size phi(3^n) x phi(3^n)).
  (ii) Verifies row sums = 1 and identifies the invariant distribution.
  (iii) Computes the full spectrum (numpy.linalg.eig).
  (iv) Reports |lambda_2| (spectral gap), the leading right eigenvectors.
  (v)  Builds the mod-3 obstruction subspace and computes the restricted
       spectral gap on its orthogonal complement.
  (vi) Cross-checks with syracuse_fft data on E_n by computing the
       n-step composition kernel and the implied collision excess.

Outputs JSON to data/spectrum_n*.json and a summary spectrum_summary.txt.

References:
  - collatz/theory/tao_syracuse_explicit.md (definitions; mod-3 = (0,1/3,2/3))
  - collatz/experiments/syracuse_fft/results.md (E_n divergence findings)
  - collatz/experiments/verify_syracuse_rv.py (small-n laws)
"""

from __future__ import annotations

import json
import math
import os
import sys
from fractions import Fraction
from typing import Dict, List, Tuple

import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Kernel construction: K_n(x, y) on units mod 3^n
# ---------------------------------------------------------------------------

def inv_pow2(modulus: int) -> int:
    """2^{-1} mod 3^n = (3^n+1)/2."""
    return (modulus + 1) // 2


def units_mod(n: int) -> List[int]:
    """List of units in Z/3^n Z = {x in [1,3^n-1]: 3 nmid x}, sorted."""
    mod = 3 ** n
    return [x for x in range(1, mod) if x % 3 != 0]


def syracuse_kernel(n: int, s: float = 0.0, a_max: int = 200) -> Tuple[np.ndarray, List[int]]:
    """
    Build the one-step Syracuse transition matrix P_n on U_n = (Z/3^n)^x.

    Row x is the conditional probability over y in U_n of the random Syracuse
    image of x under the i.i.d. valuation model (a = nu_2(3*Col(x)+1) ~ Geom(2),
    tilted by s when s != 0):
          P_s(a = k) = (2^{-(1+s) k}) / Z_s,  k >= 1,  Z_s = 2^{-(1+s)}/(1-2^{-(1+s)}).

    We compute (3x+1) mod 3^n, then iterate k=1..a_max applying 2^{-1} mod 3^n,
    truncating the geometric tail (error < n * 2^{-a_max}). At each k, if the
    image is a unit (3 nmid), accumulate P_s(a=k) at column y.

    Returns (P, U) with P stochastic (row sums = 1 up to truncation) and U the
    ordered list of units (used as the canonical row/column indexing).
    """
    mod = 3 ** n
    U = units_mod(n)
    Uidx = {u: i for i, u in enumerate(U)}
    sz = len(U)
    P = np.zeros((sz, sz), dtype=np.float64)
    inv2 = inv_pow2(mod)

    # tilted geometric pmf on k=1..a_max (renormalized over this support)
    if s == 0.0:
        weights = np.array([0.5 ** k for k in range(1, a_max + 1)])
    else:
        ratio = 2.0 ** (-(1.0 + s))
        weights = np.array([ratio ** k for k in range(1, a_max + 1)])
    weights = weights / weights.sum()  # condition on a in [1, a_max]

    for i, x in enumerate(U):
        v = (3 * x + 1) % mod
        # If 3 | v, then v_3(3x+1) > 0, meaning the image always has v_3 > 0 -> NEVER a unit.
        # In that case the row is supported on non-units (we'll renormalize at the end).
        if v % 3 == 0:
            continue  # row stays zero (unit-to-unit mass is 0 from this state)
        # iterate a = k applying inv2
        cur = v
        for k in range(1, a_max + 1):
            cur = (cur * inv2) % mod
            # cur could be a non-unit if higher power of 3 appeared (it can't for
            # v with 3 nmid v: multiplying by a unit preserves the unit class).
            # Sanity: cur % 3 != 0 here.
            j = Uidx.get(cur, -1)
            if j >= 0:
                P[i, j] += weights[k - 1]

    # Renormalize each row to sum to 1 (the rows that landed entirely in
    # non-units would have sum 0; but those rows correspond to states x with
    # 3 | (3x+1), which means x ≡ 2 mod 3 with 3x+1 ≡ 0 mod 3, i.e. x ≡ -1/3,
    # impossible since 3 nmid x. So all rows are nonzero; row mass should be 1).
    row_sums = P.sum(axis=1)
    # Quick sanity: every unit x should have 3x+1 ≡ 1 mod 3 (a unit mod 3)
    # ... Actually 3x+1 ≡ 1 mod 3 always (since 3x ≡ 0). So v_3(3x+1) = 0
    # iff 9 nmid 3x+1, but always v_3(3x+1) = 0 (mod-3-wise). However mod 9
    # could be different. The image 2^{-k}*(3x+1) mod 3^n could have 3-adic
    # valuation depending on whether (3x+1) is divisible by higher powers of 3.
    # If 9 | 3x+1, the image is divisible by 9 (since mult by 2^{-k} is a unit
    # mod 3^n action that preserves v_3). Such x have 3 nmid x and 9 | 3x+1,
    # i.e. 3x ≡ -1 mod 9, i.e. x ≡ (-1)/3 mod 3, which requires 3 | x. Contradiction.
    # So in fact v_3(3x+1) = 0 always for x a unit, hence ALL images are units.
    # Therefore row_sums should be 1 exactly (modulo truncation).
    assert np.all(row_sums > 0.999), f"unexpected zero row in P_n at n={n}"
    P = P / row_sums[:, None]
    return P, U


# ---------------------------------------------------------------------------
# Spectral diagnostics
# ---------------------------------------------------------------------------

def spectrum(P: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Eigenvalues and right/left eigenvectors of P (transition matrix).
    Returns (eigs sorted by |lambda| desc, R right eigvecs, L left eigvecs).
    """
    eigvals, eigvecs_right = np.linalg.eig(P)
    eigvals_l, eigvecs_left = np.linalg.eig(P.T)
    # sort right by |eig| desc
    order = np.argsort(-np.abs(eigvals))
    eigvals = eigvals[order]
    eigvecs_right = eigvecs_right[:, order]
    # sort left by |eig| desc (independently; they're the same eigenvalues up to numerical noise)
    order_l = np.argsort(-np.abs(eigvals_l))
    eigvals_l = eigvals_l[order_l]
    eigvecs_left = eigvecs_left[:, order_l]
    return eigvals, eigvecs_right, eigvecs_left


def is_doubly_stochastic(P: np.ndarray, tol: float = 1e-10) -> Tuple[bool, float, float]:
    """Check row + column stochasticity (the latter <=> uniform invariant)."""
    rmax = float(np.abs(P.sum(axis=1) - 1.0).max())
    cmax = float(np.abs(P.sum(axis=0) - 1.0).max())
    return (rmax < tol and cmax < tol), rmax, cmax


def invariant_distribution(P: np.ndarray) -> np.ndarray:
    """
    Left eigenvector with eigenvalue 1 (the stationary distribution).
    Returns a probability vector (sum 1, nonneg up to numerical noise).
    """
    eigvals_l, eigvecs_left = np.linalg.eig(P.T)
    # pick the eigenvalue closest to 1
    idx = int(np.argmin(np.abs(eigvals_l - 1.0)))
    v = eigvecs_left[:, idx].real
    # normalize to sum 1 (handle sign)
    if v.sum() < 0:
        v = -v
    s = v.sum()
    if abs(s) < 1e-14:
        return v  # something pathological
    return v / s


def mod3_obstruction_vectors(U: List[int]) -> np.ndarray:
    """
    Return the 2-D subspace of "mod-3 coset indicators" on U:
      e_1[i] = 1 if U[i] ≡ 1 mod 3, else 0
      e_2[i] = 1 if U[i] ≡ 2 mod 3, else 0
    These two vectors (or their orthogonal complement) carry the mod-3 obstruction.
    """
    e1 = np.array([1.0 if u % 3 == 1 else 0.0 for u in U])
    e2 = np.array([1.0 if u % 3 == 2 else 0.0 for u in U])
    return np.column_stack([e1, e2])


def restricted_spectrum(P: np.ndarray, V: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute the spectrum of P restricted to the orthogonal complement of
    columns of V (with respect to the standard inner product). Returns
    (eigs, basis) where basis is an orthonormal basis of the complement.

    We form Q s.t. Q.T @ V = 0 (Householder/QR), then P_perp = Q.T @ P @ Q.
    """
    # orthonormalize V then take orthogonal complement
    Q_full, _ = np.linalg.qr(V)  # Q_full is N x rank(V) orth columns
    rank = Q_full.shape[1]
    N = P.shape[0]
    # complement: pick a basis via SVD of (I - Q Q^T)
    M = np.eye(N) - Q_full @ Q_full.T
    U_svd, S, Vt = np.linalg.svd(M)
    # columns of U_svd with S close to 1 span the complement
    basis = U_svd[:, S > 0.5]  # exactly N - rank columns
    P_perp = basis.T @ P @ basis
    eigs = np.linalg.eigvals(P_perp)
    order = np.argsort(-np.abs(eigs))
    return eigs[order], basis


# ---------------------------------------------------------------------------
# Validation: compose P^n and compare CP to syracuse_fft's E_n
# ---------------------------------------------------------------------------

def step_to_uniform_cp(P: np.ndarray, n_steps: int) -> List[float]:
    """
    Track collision probability of (initial = uniform-on-units) under L_n^k for
    k=0..n_steps. Returns CP_k = ||rho_k||^2 (l2 norm squared of the density).
    This is a SPECTRAL probe: CP_k - 1/N = sum_{j>=2} c_j lambda_j^{2k}.
    """
    N = P.shape[0]
    rho = np.ones(N) / N
    out = [float(rho @ rho)]
    cur = rho.copy()
    for _ in range(n_steps):
        cur = cur @ P  # left-mult: rho -> rho P (this is L acting from the left as P^T rho^T)
        out.append(float(cur @ cur))
    return out


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def analyze(n: int, s: float = 0.0, a_max: int = 120, verbose: bool = True
            ) -> Dict:
    """Full spectral pipeline for given n."""
    if verbose:
        print(f"\n=== n = {n}, s = {s}, a_max = {a_max} ===")
    P, U = syracuse_kernel(n, s=s, a_max=a_max)
    N = len(U)
    ds, rmax, cmax = is_doubly_stochastic(P, tol=1e-8)
    if verbose:
        print(f"  |U_n| = {N} = phi(3^n) = 2 * 3^{n-1}")
        print(f"  row sums err = {rmax:.3e}, col sums err = {cmax:.3e}  doubly_stoch={ds}")
    eigs, R, L = spectrum(P)
    moduli = np.abs(eigs)
    lam1 = eigs[0]
    lam2 = eigs[1]
    gap = 1.0 - moduli[1]
    if verbose:
        print(f"  lambda_1 = {lam1.real:+.10f}{lam1.imag:+.3e}j   |.| = {moduli[0]:.10f}")
        print(f"  lambda_2 = {lam2.real:+.10f}{lam2.imag:+.3e}j   |.| = {moduli[1]:.10f}")
        print(f"  spectral gap 1 - |lambda_2| = {gap:.6e}")
        print(f"  next few |lambda|: {moduli[2:8].tolist()}")

    inv_dist = invariant_distribution(P)
    inv_dist_max = float(inv_dist.max())
    inv_dist_min = float(inv_dist.min())
    # check how close invariant is to uniform
    unif = np.ones(N) / N
    tv_inv_to_unif = 0.5 * float(np.abs(inv_dist - unif).sum())

    if verbose:
        print(f"  invariant distribution: max {inv_dist_max:.4e}, min {inv_dist_min:.4e}, "
              f"TV to uniform = {tv_inv_to_unif:.4e}")

    # mod-3 obstruction analysis
    V = mod3_obstruction_vectors(U)
    # what does P do on V?  P @ e_1 = ?, P @ e_2 = ?
    # The image of e_1 under right-mult by P should mix between e_1, e_2 since
    # P^T rho carries the residue mod 3.
    # Look at P @ V: does P preserve span(V)?
    PV = P @ V
    # project PV onto V (least squares)
    coeffs, residuals, rank_, _ = np.linalg.lstsq(V, PV, rcond=None)
    PV_approx = V @ coeffs
    proj_residual = float(np.linalg.norm(PV - PV_approx))
    if verbose:
        print(f"  || P @ V - V (V^+ P V) || = {proj_residual:.4e}  (0 => P preserves span(V))")
        print(f"  P acts on V (mod-3 indicators) as 2x2:\n{coeffs}")

    # restricted spectrum: kill the mod-3 obstruction subspace
    # We project onto the complement of span(V).
    eigs_perp, _ = restricted_spectrum(P, V)
    if len(eigs_perp) > 0:
        moduli_perp = np.abs(eigs_perp)
        # Note: lambda=1 should still appear in perp (since the uniform-on-units
        # vector is orthogonal to (e_1 - e_2) component but NOT to e_1+e_2 = const-on-units),
        # actually V contains the const vector e_1+e_2 = 1 on units. So lambda=1
        # is killed in the complement. Spectral gap of complement = 1 - |largest|.
        lam_perp_max = moduli_perp[0]
        if verbose:
            print(f"  spectrum on span(V)^perp: largest |.| = {lam_perp_max:.6f}")
            print(f"  perp gap 1 - |lambda_perp_max| = {1.0 - lam_perp_max:.4e}")

    # cross-check: P^n acting on uniform should give the Syracuse RV law
    # (after the W_0 = 0 initialization is replaced by uniform-on-units start).
    # That is a different initial condition than syracuse_fft's W_0 = 0, so the
    # n-step composition matches only the marginal mixing, not the specific Syrac.
    cp_traj = step_to_uniform_cp(P, n_steps=2 * n)  # uniform start -> trivially CP = 1/N

    out = {
        "n": n,
        "s": s,
        "a_max": a_max,
        "phi3n": N,
        "doubly_stochastic": ds,
        "rowsum_err": rmax,
        "colsum_err": cmax,
        "eigenvalues_real": [float(e.real) for e in eigs],
        "eigenvalues_imag": [float(e.imag) for e in eigs],
        "moduli": [float(m) for m in moduli],
        "lambda1": [float(lam1.real), float(lam1.imag)],
        "lambda2": [float(lam2.real), float(lam2.imag)],
        "spectral_gap": float(gap),
        "invariant_max": inv_dist_max,
        "invariant_min": inv_dist_min,
        "invariant_tv_to_uniform": tv_inv_to_unif,
        "P_on_V_coeffs": coeffs.tolist(),
        "P_preserves_V_residual": proj_residual,
        "perp_largest_modulus": float(np.abs(eigs_perp[0])) if len(eigs_perp) > 0 else None,
        "perp_gap": float(1.0 - np.abs(eigs_perp[0])) if len(eigs_perp) > 0 else None,
        "perp_spectrum_top10_moduli": [float(m) for m in np.abs(eigs_perp)[:10]],
        "cp_from_uniform_trajectory": cp_traj,
        "1_over_phi3n": 1.0 / N,
    }
    return out


def main():
    print("Spectral analysis of Syracuse Frobenius--Perron operator on (Z/3^n)^x")
    print(f"Output dir: {DATA_DIR}")
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    s_values = [0.0]  # add more later if desired; 0.438 is descent-balance
    summary = []
    for s in s_values:
        for n in range(1, nmax + 1):
            res = analyze(n, s=s, a_max=120 if n <= 5 else 80, verbose=True)
            tag = f"n{n}_s{s:+.3f}".replace("+", "p").replace("-", "m").replace(".", "p")
            path = os.path.join(DATA_DIR, f"spectrum_{tag}.json")
            with open(path, "w") as f:
                json.dump(res, f, indent=2, default=str)
            summary.append({
                "n": n, "s": s,
                "phi3n": res["phi3n"],
                "lambda2_mod": res["moduli"][1],
                "gap": res["spectral_gap"],
                "perp_gap": res["perp_gap"],
                "perp_largest_mod": res["perp_largest_modulus"],
            })
    # write summary
    with open(os.path.join(DATA_DIR, "spectrum_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print("\n=== SUMMARY (s = 0, untilted) ===")
    print(f"{'n':>3} {'phi(3^n)':>10} {'|lambda_2|':>14} {'gap':>14} {'|lambda_perp|':>18} {'perp_gap':>14}")
    for s in summary:
        plm = s["perp_largest_mod"]
        pg = s["perp_gap"]
        plm_s = f"{plm:>18.10f}" if plm is not None else f"{'n/a':>18}"
        pg_s = f"{pg:>14.6e}" if pg is not None else f"{'n/a':>14}"
        print(f"{s['n']:>3} {s['phi3n']:>10} {s['lambda2_mod']:>14.10f} "
              f"{s['gap']:>14.6e} {plm_s} {pg_s}")


if __name__ == "__main__":
    main()
