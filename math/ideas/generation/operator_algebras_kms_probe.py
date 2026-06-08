"""
Operator-algebras / KMS probe for the Collatz Syracuse transfer operator.

Sub-direction (i) of the brief: build the Syracuse transfer-operator
Markov C*-algebra at n=2, identify the KMS_β states of its associated
modular automorphism group, and check whether ANY β gives a stationary
state whose mod-3 / mod-9 marginal escapes the Tao plateau.

For a faithful state ω on the finite-dim C*-algebra A = C(X) ⋊ T
(equivalently here a matrix algebra M_k with diagonal weight), the
Tomita-Takesaki modular automorphism is

    σ_t^ω(a) = Δ^{it} a Δ^{-it},

with modular operator Δ = ρ ⊗ ρ^{-1} (on M_k via the canonical Hilbert
space M_k with HS inner product, ρ = density matrix of ω).

KMS_β condition for σ_t (the "tracial" modular flow corresponding to
ω = trace) reads, for the dynamical automorphism induced by a Hamiltonian
H = −log P_n (formally, where P_n is the Markov kernel and we think
of −log P entry-wise on the support graph):

    ω_β KMS_β  ⇔  ω_β(ab) = ω_β(b α_{iβ}(a)),  α_t = e^{itH} · e^{-itH}.

For a *commutative* finite C*-algebra A = C(X) (which is what we get if
we take only the diagonal of the matrix view), the dynamical KMS_β
states are EXACTLY the Gibbs measures

    π_β(x) ∝ exp(−β H(x))                       (commutative case)

where H is a chosen "Hamiltonian" function. To get a genuinely
NONCOMMUTATIVE structure we must include the off-diagonal Markov
transitions. The natural object is the *Cuntz–Krieger* C*-algebra
O_A of the 0/1 transition matrix A on (Z/9)*, or — finite-dimensionally
— the path-space algebra Aₙ = matrix algebra of length-N paths in the
Syracuse transition graph.

This probe:

1. Builds the Syracuse Markov kernel P on (Z/9)*  = {1,2,4,5,7,8}.
2. Builds the path-space matrix algebra A_N for N = 1, 2, 3.
3. For each β in a grid, computes the KMS_β state associated to the
   Cuntz-Krieger dynamics with Hamiltonian H(x) = −log a(x) where
   a(x) is the average 2-adic valuation of 3·x+1 weighted by the
   transition kernel (= the natural "energy" of a state).
4. Computes the mod-3 and mod-9 marginal of each KMS_β state.
5. Reports whether ANY β achieves
      (mod-3 marginal) = (0, 1/3, 2/3)   AND drift balance,
   i.e. the Tao saturation with non-divergent E[a].

If every KMS_β state has E[a] ≥ 5/2 (the Wave-2 LP-min), the NC route
is closed by the same barrier as the commutative one — the noncommutative
LDP rate function is just relative entropy and the Donsker-Varadhan
infimum is unchanged.
"""

from __future__ import annotations
import json
import math
from typing import Iterable

import numpy as np
from numpy.linalg import eigh, eigvals


# -----------------------------------------------------------------------
# 1. The Syracuse Markov kernel on (Z/9Z)^*
# -----------------------------------------------------------------------

def syracuse_step_mod(x: int, mod: int) -> list[tuple[int, float, int]]:
    """
    Given odd residue x mod 'mod' = 3^k, return list of (y, prob, a)
    where y is the next odd residue mod 'mod', prob is its conditional
    probability under the Tao-Bernoulli model of a = nu_2(3x+1)
    (= Geom(1/2) on positive integers), and a is the corresponding
    valuation that yields y. We truncate to a <= A_MAX since prob
    decays as 2^{-a}.

    NB: under the lifting to Z, 3x+1 has some fixed nu_2 = a*(x). But
    in the *transfer-operator* sense on (Z/9)^*, we are pushing forward
    a random a ~ Geom(1/2) (= Tao's "Syracuse random variable"
    distribution) and reading off y = (3x+1)/2^a mod 9.
    """
    A_MAX = 30
    out = []
    for a in range(1, A_MAX + 1):
        # We must condition on this a-value being consistent with x mod 9:
        # 3x+1 mod 9 has a fixed value; the *actual* nu_2 depends on the
        # lift. The Tao-Bernoulli model TREATS a as i.i.d. Geom(1/2),
        # decoupled from x mod 9. So we just compute
        #     y = ( (3x+1) * 2^{-a} ) mod 9
        # provided gcd((3x+1), 2^a) makes sense; here 3x+1 is even
        # exactly when 3x+1 ≡ 0 mod 2, which for x coprime to 3 (so x odd)
        # is always: 3x+1 is even iff x is odd. Since x mod 9 in (Z/9)^*
        # is coprime to 3, and we run only over a ≥ 1, we always need
        # 2^a | (3x+1) as integers — but mod 9 we work formally with
        # 2^{-a} mod 9 (since gcd(2, 9) = 1, 2 is invertible mod 9).
        inv2_a = pow(pow(2, a, mod), mod - 1 if mod == 9 else _euler_phi(mod) - 1, mod)
        # For mod = 9, phi(9) = 6, so 2^{-1} ≡ 2^5 mod 9 = 32 mod 9 = 5.
        # We'll just use pow(2, -1, mod) for clarity.
        inv2_a = pow(pow(2, a, mod), -1, mod)
        y = ((3 * x + 1) * inv2_a) % mod
        prob = 2.0 ** (-a)
        # Only keep y coprime to 3 (i.e. y in (Z/9)^*); otherwise the
        # Syracuse map exits the unit group. Under (Z/9)^* dynamics this
        # never happens because (3x+1)/2^a is forced to be odd, and the
        # 3-part: (3x+1) is congruent to 1 mod 3 (since 3x ≡ 0), so
        # y ≡ 2^{-a} mod 3, which is in {1, 2} — always coprime to 3.
        # Sanity check:
        if math.gcd(y, mod) != 1:
            continue
        out.append((y, prob, a))
    return out


def _euler_phi(n: int) -> int:
    r = n
    p = 2
    nn = n
    while p * p <= nn:
        if nn % p == 0:
            while nn % p == 0:
                nn //= p
            r -= r // p
        p += 1
    if nn > 1:
        r -= r // nn
    return r


def build_syracuse_kernel(k: int) -> tuple[np.ndarray, list[int], np.ndarray]:
    """
    Build the Tao-Bernoulli transfer kernel P on (Z/3^k)^*.

    Returns (P, states, A_mean) where P[i, j] = sum_a 2^{-a} * 1[step
    from i with valuation a lands at j] = transition probability under
    Geom(1/2) a-distribution; states is the list of unit residues mod
    3^k; A_mean[i] = E[a | x = states[i]] = expected valuation (a) of
    the step originating at i, under Tao-Bernoulli.

    Because a ~ Geom(1/2) is i.i.d., A_mean[i] = E[Geom(1/2)] = 2 for
    EVERY i — but on the Markov state space the *conditional* sum of
    transitions decomposes by valuation, so the row-sums of P are 1
    automatically and the average-valuation function on the transitions
    is a nontrivial labelling.

    A_mean here is the entries-of-(weighted-edges) mean, not the
    Geom(1/2) mean.
    """
    mod = 3 ** k
    states = [x for x in range(1, mod) if math.gcd(x, mod) == 1]
    idx = {x: i for i, x in enumerate(states)}
    P = np.zeros((len(states), len(states)))
    A_mean = np.zeros(len(states))
    for i, x in enumerate(states):
        edges = syracuse_step_mod(x, mod)
        # Normalise (truncation effect)
        Z = sum(p for _, p, _ in edges)
        for y, p, a in edges:
            j = idx[y]
            P[i, j] += p / Z
            A_mean[i] += (p / Z) * a
    return P, states, A_mean


# -----------------------------------------------------------------------
# 2. The Markov C*-algebra and its KMS_β states (Cuntz-Krieger style)
# -----------------------------------------------------------------------

def adjacency(P: np.ndarray, tol: float = 1e-14) -> np.ndarray:
    """0/1 adjacency matrix from a (possibly weighted) kernel."""
    return (P > tol).astype(int)


def perron_frobenius(A: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    """
    For an irreducible nonneg matrix A, return (rho, left, right) =
    spectral radius and corresponding (positive) left/right eigenvectors,
    normalised so left . right = 1.
    """
    w, V = np.linalg.eig(A.astype(float))
    # pick the eigenvalue with largest real part
    k = np.argmax(np.real(w))
    rho = float(np.real(w[k]))
    right = np.real(V[:, k])
    if right.sum() < 0:
        right = -right
    # left eigenvector: same procedure on A^T
    w2, V2 = np.linalg.eig(A.astype(float).T)
    k2 = np.argmin(np.abs(w2 - rho))
    left = np.real(V2[:, k2])
    if left.sum() < 0:
        left = -left
    s = float(left @ right)
    left = left / s
    return rho, left, right


def kms_state_ck(P: np.ndarray, A_mean_per_row: np.ndarray,
                  beta: float) -> tuple[np.ndarray, float, float]:
    """
    Compute the (unique, when it exists) KMS_β state of the Cuntz-Krieger
    algebra O_B associated with the *weighted* transition matrix
        B_β[i, j] = P[i, j]^β · (Geom(1/2) factor)^β,
    by Renault-Enomoto-Fujii-Watatani: a KMS_β state for the gauge action
    on O_A exists iff the spectral radius of e^{-β H_loc} A is 1; the
    KMS_β state is determined by the Perron-Frobenius eigenvectors.

    Here we take H_loc[i, j] = a-value of the (i->j) edge weighted by
    its Tao-Bernoulli probability, summed; equivalently H is the "log
    inverse transition probability" (= Bernoulli-Gibbs Hamiltonian).

    Returns (pi_β, lambda_β, E_beta_a):
        pi_β       = the stationary measure (= mod-3^k marginal of the
                     KMS_β state restricted to the diagonal subalgebra)
        lambda_β   = spectral radius of the deformed transition matrix
        E_beta_a   = expected valuation E_{π_β}[a] under the KMS_β state.

    The classical Bernoulli case is β = 1 and yields the *uniform* mod-9
    marginal (Tao's plateau).
    """
    # Deformed (Renault) transition matrix
    # B_β[i,j] = P[i,j]^β  if P[i,j] > 0 else 0
    # (Cuntz-Krieger gauge KMS_β formula for the "log P" potential)
    eps = 1e-300
    B = np.where(P > 0, np.power(P + eps, beta), 0.0)
    rho, left, right = perron_frobenius(B)
    # Normalised KMS_β marginal pi_β[i] = left[i] * right[i]
    pi_beta = left * right
    pi_beta = pi_beta / pi_beta.sum()
    # E[a] under pi_β: weighted by pi_β and row-averaged a-value
    E_a = float(pi_beta @ A_mean_per_row)
    return pi_beta, float(rho), E_a


# -----------------------------------------------------------------------
# 3. Marginals
# -----------------------------------------------------------------------

def mod3_marginal(pi: np.ndarray, states: list[int]) -> dict[int, float]:
    out: dict[int, float] = {0: 0.0, 1: 0.0, 2: 0.0}
    for p, s in zip(pi, states):
        out[s % 3] += float(p)
    return out


def mod9_marginal(pi: np.ndarray, states: list[int]) -> dict[int, float]:
    out: dict[int, float] = {r: 0.0 for r in range(9)}
    for p, s in zip(pi, states):
        out[s % 9] += float(p)
    return out


# -----------------------------------------------------------------------
# 4. Tomita-Takesaki modular operator (commutative case: trivial; matrix
#    case: compute explicitly).
# -----------------------------------------------------------------------

def modular_spectrum_matrix(rho: np.ndarray) -> np.ndarray:
    """
    For a faithful density matrix ρ on M_n, the Tomita-Takesaki modular
    operator Δ on the GNS Hilbert space (=HS space) has spectrum
        {λ_i / λ_j : i, j = 1..n}
    where {λ_i} = eigenvalues of ρ. Return the sorted list of these
    ratios.
    """
    lam = np.linalg.eigvalsh(rho)
    lam = lam[lam > 1e-15]
    out = []
    for a in lam:
        for b in lam:
            out.append(a / b)
    return np.sort(np.array(out))


def density_from_pi(pi: np.ndarray) -> np.ndarray:
    """Diagonal density matrix from a probability vector."""
    return np.diag(pi)


# -----------------------------------------------------------------------
# 5. Run the probe
# -----------------------------------------------------------------------

def main():
    LOG2_3 = math.log2(3)
    results = {"version": "wave4-opalg-kms-v1"}

    for k in (1, 2, 3):
        P, states, A_mean = build_syracuse_kernel(k)
        n = len(states)
        # Stationary distribution of P (β = 1, the trace)
        rho1, left1, right1 = perron_frobenius(P)
        pi1 = left1 / left1.sum()
        mod3_1 = mod3_marginal(pi1, states)
        E_a_1 = float(pi1 @ A_mean)
        block = {
            "k": k,
            "modulus": 3 ** k,
            "n_states": n,
            "states": states,
            "A_mean_per_row": A_mean.tolist(),
            "beta=1": {
                "spectral_radius": rho1,
                "pi": pi1.tolist(),
                "mod3_marginal": mod3_1,
                "E_a": E_a_1,
                "log2_3": LOG2_3,
                "drift_gap": E_a_1 - LOG2_3,
            },
        }
        if k >= 2:
            block["beta=1"]["mod9_marginal"] = mod9_marginal(pi1, states)

        # KMS_β grid
        betas = np.concatenate(
            [
                np.linspace(0.1, 0.9, 9),
                [1.0],
                np.linspace(1.1, 5.0, 40),
                [10.0, 50.0, 100.0],
            ]
        )
        kms_table = []
        for beta in betas:
            pi_b, lam_b, E_a_b = kms_state_ck(P, A_mean, float(beta))
            entry = {
                "beta": float(beta),
                "spectral_radius_B_beta": lam_b,
                "pi_beta": pi_b.tolist(),
                "mod3_marginal": mod3_marginal(pi_b, states),
                "E_a_beta": E_a_b,
                "drift_gap": E_a_b - LOG2_3,
            }
            if k >= 2:
                entry["mod9_marginal"] = mod9_marginal(pi_b, states)
            kms_table.append(entry)
        block["kms_table"] = kms_table

        # Tomita-Takesaki: modular spectrum of the diagonal density at β=1
        rho_mat = density_from_pi(pi1)
        mod_spec = modular_spectrum_matrix(rho_mat).tolist()
        block["modular_spectrum_beta=1"] = mod_spec

        results[f"k={k}"] = block

    # Top-line summary: for k=2, scan beta-grid and report
    #   (a) min and max E_a_beta over beta in (0, 100]
    #   (b) the beta closest to Tao saturation (mod-3 marginal (0,1/3,2/3))
    #   (c) the beta minimising drift gap |E_a − log_2 3|.
    k2 = results["k=2"]["kms_table"]
    E_a_vals = [e["E_a_beta"] for e in k2]
    mod3_dists = [
        abs(e["mod3_marginal"][0] - 0.0)
        + abs(e["mod3_marginal"][1] - 1 / 3)
        + abs(e["mod3_marginal"][2] - 2 / 3)
        for e in k2
    ]
    drift_gaps = [abs(e["drift_gap"]) for e in k2]
    summary = {
        "k=2_E_a_min": min(E_a_vals),
        "k=2_E_a_min_beta": k2[E_a_vals.index(min(E_a_vals))]["beta"],
        "k=2_E_a_max": max(E_a_vals),
        "k=2_best_mod3_L1_dist": min(mod3_dists),
        "k=2_best_mod3_beta": k2[mod3_dists.index(min(mod3_dists))]["beta"],
        "k=2_best_drift_gap": min(drift_gaps),
        "k=2_best_drift_beta": k2[drift_gaps.index(min(drift_gaps))]["beta"],
        "log2_3": LOG2_3,
    }
    results["summary"] = summary

    with open(
        "/home/user/wikiclaws/math/ideas/generation/data/operator_algebras_kms_probe.json",
        "w",
    ) as f:
        json.dump(results, f, indent=2, default=float)

    # Print compact human-readable summary
    print("=== KMS_β probe on Syracuse transfer operator ===")
    for k in (1, 2, 3):
        b = results[f"k={k}"]
        print(f"\n--- k = {k}  (mod {3**k}, n_states = {b['n_states']}) ---")
        print(f"  β=1: spectral_radius={b['beta=1']['spectral_radius']:.6f}")
        print(f"  β=1: mod-3 marginal = {b['beta=1']['mod3_marginal']}")
        print(f"  β=1: E[a] = {b['beta=1']['E_a']:.6f}, log2(3) = {LOG2_3:.6f}")
        print(f"  β=1: drift gap = {b['beta=1']['drift_gap']:.6f}")
        if k == 2:
            print(f"  β=1: mod-9 marginal = {b['beta=1']['mod9_marginal']}")
    print("\n=== k=2 KMS_β scan: E[a] (min, max), best mod-3 L1 ===")
    s = results["summary"]
    print(f"  min_β E[a] = {s['k=2_E_a_min']:.4f} at β = {s['k=2_E_a_min_beta']:.3f}")
    print(f"  max_β E[a] = {s['k=2_E_a_max']:.4f}")
    print(
        f"  best mod-3 L1 dist to (0,1/3,2/3) = {s['k=2_best_mod3_L1_dist']:.6f} "
        f"at β = {s['k=2_best_mod3_beta']:.3f}"
    )
    print(
        f"  smallest |E[a] - log2 3| = {s['k=2_best_drift_gap']:.6f} "
        f"at β = {s['k=2_best_drift_beta']:.3f}"
    )

    # Print β-table for k=2
    print("\n=== β-table at k=2 (selection) ===")
    print(f"{'beta':>8s} {'spec_rad':>10s} {'E[a]':>8s} {'drift':>9s} "
          f"{'mod3=1':>8s} {'mod3=2':>8s}")
    for e in k2:
        if abs(e["beta"] - round(e["beta"] * 4) / 4) < 1e-9 or e["beta"] in (
            0.1, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0, 50.0, 100.0):
            print(
                f"{e['beta']:8.3f} {e['spectral_radius_B_beta']:10.5f} "
                f"{e['E_a_beta']:8.4f} {e['drift_gap']:9.4f} "
                f"{e['mod3_marginal'][1]:8.4f} {e['mod3_marginal'][2]:8.4f}"
            )

    # Tomita modular spectrum at β = 1, k = 2
    spec = results["k=2"]["modular_spectrum_beta=1"]
    print("\n=== Tomita modular spectrum (Δ) at β=1, k=2 ===")
    print(f"  #eigenvalues = {len(spec)}")
    print(f"  range: [{min(spec):.4f}, {max(spec):.4f}]")
    print(f"  log-spectrum range: [{math.log(min(spec)):.4f}, "
          f"{math.log(max(spec)):.4f}]")


if __name__ == "__main__":
    main()
