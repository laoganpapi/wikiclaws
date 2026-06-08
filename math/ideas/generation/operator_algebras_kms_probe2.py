"""
Sharper KMS probe (probe 2): include a per-edge energy a (valuation) so
that the KMS_β state genuinely re-weights the valuation distribution.

Setup (Cuntz-Krieger / Renault):
    edges labelled by (i, j, a) with weight P[i,j,a] = 2^{-a} · 1[
       (3 i + 1)/2^a ≡ j (mod 9)
    ]                                                         (Bernoulli base)
    Hamiltonian H(i,j,a) = a   (the natural valuation energy)
    Deformed weight: B_β[i,j,a] = exp(-β · a) · P[i,j,a]^0
                                = e^{-β a} on allowed edges,
       OR (Bernoulli-tilted) B_β[i,j,a] = P[i,j,a] · e^{-(β−1) a}.

Use the SECOND form: it is the unique tilt that recovers β=1 = Tao
Bernoulli base, and corresponds to the Esscher tilt of the Geom(1/2)
i.i.d. valuation distribution (which is what the project's Wave-2 barrier
analyzes).

This is *exactly* the commutative Esscher tilt, dressed up in the
Cuntz-Krieger gauge language. The question: does going noncommutative
(allowing off-diagonal coherences in the KMS state) help?

Spoiler: NO. The KMS_β state restricted to the diagonal subalgebra
= C((Z/9)^*) is a probability measure π_β on (Z/9)^*, and:

    E_{π_β}[a] = E_{Esscher-β}[Geom(1/2)] = 2 / (2^β − 1) · 2^β / 1
              = (... Esscher tilted geom mean ...).

The off-diagonal coherences do NOT contribute to the mod-3^k marginal
(which is a diagonal observable). So the noncommutative KMS state
gives the same marginal — and the same drift gap — as the commutative
Esscher tilt. This is the precise statement of why the LDP barrier
transfers.

This probe verifies that prediction numerically.
"""

from __future__ import annotations
import json
import math
import numpy as np


def build_edges(k: int, a_max: int = 40) -> tuple[list[int], list[tuple[int, int, int, float]]]:
    """
    Returns (states, edges) where
        states = list of x in (Z/3^k)^*
        edges  = list of (i, j, a, prob) with prob = 2^{-a}, j = ((3 x + 1) * 2^{-a}) mod 3^k.
    """
    mod = 3 ** k
    states = [x for x in range(1, mod) if math.gcd(x, mod) == 1]
    idx = {x: i for i, x in enumerate(states)}
    edges = []
    inv2 = pow(2, -1, mod)
    for i, x in enumerate(states):
        inv2_a = 1
        for a in range(1, a_max + 1):
            inv2_a = (inv2_a * inv2) % mod
            y = ((3 * x + 1) * inv2_a) % mod
            if math.gcd(y, mod) != 1:
                continue
            prob = 2.0 ** (-a)
            j = idx[y]
            edges.append((i, j, a, prob))
    return states, edges


def transfer_matrix(states: list[int], edges: list[tuple[int, int, int, float]],
                    beta: float) -> np.ndarray:
    """
    Build M_β[i, j] = Σ_a 2^{-a · β} · 1[edge (i, j, a) allowed].

    For β = 1 this is the Bernoulli transition matrix.
    For β > 1 this Esscher-tilts the valuation distribution toward smaller a.
    For β < 1 this tilts toward larger a.
    """
    n = len(states)
    M = np.zeros((n, n))
    for (i, j, a, _) in edges:
        M[i, j] += 2.0 ** (-a * beta)
    return M


def perron(M: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    w, V = np.linalg.eig(M)
    k = np.argmax(np.real(w))
    rho = float(np.real(w[k]))
    right = np.real(V[:, k])
    if right.sum() < 0:
        right = -right
    w2, V2 = np.linalg.eig(M.T)
    k2 = np.argmin(np.abs(w2 - rho))
    left = np.real(V2[:, k2])
    if left.sum() < 0:
        left = -left
    return rho, left, right


def kms_state(states, edges, beta: float):
    """
    Construct the KMS_β state of the Cuntz-Krieger algebra for the
    Bernoulli-Esscher tilt with energy H(edge) = a.

    Returns:
        pi_beta      = diagonal marginal (probability on (Z/3^k)^*)
        rho_beta     = spectral radius of M_β
        Ea_beta      = E_{KMS_β}[a-valuation] computed from the edge
                       distribution
        E_min_2pow_a = E[2^{-a}] under tilted dist (sanity)
    """
    M = transfer_matrix(states, edges, beta)
    rho, left, right = perron(M)
    # Stationary measure of the normalised tilted Markov chain
    # P_β[i,j] = M_β[i,j] * right[j] / (rho * right[i])
    n = len(states)
    P_beta = np.zeros_like(M)
    for i in range(n):
        for j in range(n):
            if right[i] > 0:
                P_beta[i, j] = M[i, j] * right[j] / (rho * right[i])
    # Stationary distribution = left * right normalised
    pi_beta = left * right
    pi_beta = np.maximum(pi_beta, 0)
    pi_beta = pi_beta / pi_beta.sum()
    # Edge expectation E[a] under the tilted chain
    Ea = 0.0
    for (i, j, a, _) in edges:
        # weight = (pi_beta[i] * P_beta[i,j])^? — actually the edge prob
        # under the stationary chain is pi_beta[i] * P_beta[i,j] times
        # the fraction of the (i,j) transition coming from valuation a.
        # The a-fraction is 2^{-a β} / sum_{a'} 2^{-a' β} 1[edge (i,j,a')]
        # which is M_β[i,j]_{a-th term} / M_β[i,j]_{total}.
        if M[i, j] == 0:
            continue
        frac_a = (2.0 ** (-a * beta)) / M[i, j]
        Ea += pi_beta[i] * P_beta[i, j] * a * frac_a
    return pi_beta, rho, Ea


def mod_marginal(pi, states, mod):
    out = {r: 0.0 for r in range(mod)}
    for p, s in zip(pi, states):
        out[s % mod] += float(p)
    return out


def main():
    LOG2_3 = math.log2(3)
    out = {"version": "wave4-opalg-kms-v2-tilted-valuation"}

    for k in (1, 2, 3):
        states, edges = build_edges(k, a_max=50)
        block = {
            "k": k,
            "n_states": len(states),
            "n_edges": len(edges),
            "states": states,
        }
        beta_table = []
        betas = (
            [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
            + [0.95, 1.0, 1.05, 1.1, 1.2, 1.3, 1.4, 1.5, 1.7, 2.0]
            + [2.5, 3.0, 4.0, 5.0, 10.0, 20.0]
        )
        for beta in betas:
            pi_b, rho_b, Ea_b = kms_state(states, edges, float(beta))
            row = {
                "beta": beta,
                "spectral_radius": rho_b,
                "pi_beta": pi_b.tolist(),
                "mod3": mod_marginal(pi_b, states, 3),
                "E_a": Ea_b,
                "drift_gap": Ea_b - LOG2_3,
            }
            if k >= 2:
                row["mod9"] = mod_marginal(pi_b, states, 9)
            beta_table.append(row)
        block["beta_table"] = beta_table

        # Find β that minimises |E[a] - log_2 3| (drift balance)
        gaps = [abs(r["drift_gap"]) for r in beta_table]
        i_min = int(np.argmin(gaps))
        block["best_drift_beta"] = beta_table[i_min]["beta"]
        block["best_drift_gap"] = beta_table[i_min]["drift_gap"]
        block["best_drift_E_a"] = beta_table[i_min]["E_a"]
        block["best_drift_mod3"] = beta_table[i_min]["mod3"]
        if k >= 2:
            block["best_drift_mod9"] = beta_table[i_min]["mod9"]

        out[f"k={k}"] = block

    with open(
        "/home/user/wikiclaws/math/ideas/generation/data/operator_algebras_kms_probe2.json",
        "w",
    ) as f:
        json.dump(out, f, indent=2, default=float)

    # Print results
    print("=== KMS_β probe with edge-valuation energy (Esscher tilt of Geom(1/2)) ===")
    for k in (1, 2, 3):
        b = out[f"k={k}"]
        print(f"\n--- k={k} (mod {3**k}, {b['n_states']} states, {b['n_edges']} edges) ---")
        print(f"{'beta':>7s} {'spec_rad':>10s} {'E[a]':>8s} {'drift_gap':>10s}", end="")
        if k == 1:
            print(f" {'mod3=1':>8s} {'mod3=2':>8s}")
        else:
            print(f" {'mod3=1':>8s} {'mod3=2':>8s}")
        for r in b["beta_table"]:
            print(f"{r['beta']:7.3f} {r['spectral_radius']:10.5f} "
                  f"{r['E_a']:8.4f} {r['drift_gap']:10.4f} "
                  f"{r['mod3'][1]:8.4f} {r['mod3'][2]:8.4f}")
        print(f"  -> best drift β = {b['best_drift_beta']}, "
              f"E[a] = {b['best_drift_E_a']:.5f}, "
              f"gap = {b['best_drift_gap']:.5f}, "
              f"mod-3 = {b['best_drift_mod3']}")
        if k >= 2:
            print(f"  -> mod-9 at best β = {b['best_drift_mod9']}")
            # Compare to Tao saturation: (0, 1/3, 2/3) on mod-3
            tao_dist = (abs(b["best_drift_mod3"][0])
                        + abs(b["best_drift_mod3"][1] - 1/3)
                        + abs(b["best_drift_mod3"][2] - 2/3))
            print(f"  -> L1 distance to Tao mod-3 plateau (0,1/3,2/3): {tao_dist:.6f}")


if __name__ == "__main__":
    main()
