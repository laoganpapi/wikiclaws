"""
Noncommutative ergodic theory / Heisenberg-nilmanifold probe for Collatz.

We test sub-direction (i)+(ii) of the alt-angle brief:
  - Encode the Syracuse iteration as orbit-data of a translation on the
    Heisenberg nilmanifold X = H_3(R)/H_3(Z), via the natural map
       n -> (alpha * S_n, beta * (S_n)*(j-index), gamma * Q_n) mod 1
    where S_n = a_1 + ... + a_n is the cumulative 2-adic-valuation sum, Q_n
    encodes the second-order Furstenberg-type bracket (sum_{i<j} a_i),
    and (alpha, beta, gamma) = (log_2 3, 1, log_2 3) are the natural drift
    constants. The nilmanifold has degree-2 (quadratic) fundamental class.
  - Test Bohr / Besicovitch almost-periodicity of the Syracuse RESIDUE
    R_n mod 3^k by computing the empirical Fourier spectrum on the
    drift sequence (not its residue mod 3^k).

The PURPOSE of the probe is to expose, numerically, whether the Syracuse
sequence "lives" on a sub-nilmanifold (= structured non-equidistribution)
or is equidistributed (= Bohr-trivial in the higher-order sense).

OUTPUT: data/noncommutative_nilmanifold_probe.json
        + summary printed.

Author: Alex Ye (AI-assisted; not on author line).
"""

import json
import os
from math import log, pi, cos, sin, sqrt
from fractions import Fraction

import numpy as np


# ---------------------------------------------------------------------------
# Syracuse iteration on odd integers
# ---------------------------------------------------------------------------

def syracuse_step(n):
    """Syracuse map: n -> (3n+1)/2^{v_2(3n+1)}, n odd."""
    assert n % 2 == 1
    m = 3 * n + 1
    a = 0
    while m % 2 == 0:
        m //= 2
        a += 1
    return m, a


def syracuse_data(N0, length):
    """Generate (a_1, ..., a_L), (S_1,...,S_L), R_n = N_L mod 3^k for various k."""
    n = N0
    a_seq = []
    S_seq = []
    cur = n
    S = 0
    L = 0
    for j in range(length):
        try:
            cur, a = syracuse_step(cur)
        except AssertionError:
            break
        if cur == 1:
            break
        a_seq.append(a)
        S += a
        S_seq.append(S)
        L += 1
    return a_seq, S_seq, cur


# ---------------------------------------------------------------------------
# Heisenberg nilmanifold embedding
#
# H_3(R) = { [[1,x,z],[0,1,y],[0,0,1]] : x,y,z in R }
# X = H_3(R) / H_3(Z) is a 3-dim nilmanifold; left translation by
#   g_n = exp( n * (alpha X + beta Y + 0 Z) )  in BCH expansion gives
#   coordinates  (n*alpha mod 1, n*beta mod 1, (n^2 alpha beta / 2) mod 1).
# So the "quadratic phase" coordinate is the genuinely 2-step datum.
#
# For Collatz, we replace n -> S_n (the cumulative 2-adic valuation sum) and
# put alpha = log_2(3), beta = 1, so that drift balance corresponds to
#   alpha * j - S_j  is small (the multiplier 3^j / 2^{S_j} is bounded).
# ---------------------------------------------------------------------------

LOG2_3 = log(3.0) / log(2.0)  # ~ 1.58496

def nilmanifold_coords(a_seq, S_seq, alpha=LOG2_3, beta=1.0):
    """
    For each j, compute the Heisenberg coordinate
       (x_j, y_j, z_j) = (alpha*j mod 1, S_j mod 1, alpha*S_j*(j-1)/2 mod 1)
    The third coordinate is the "quadratic Furstenberg bracket" - the
    integral of x dy along the orbit, discretised.
    """
    coords = []
    # NOTE on y-coordinate: S_j is an integer, so (1*S_j) mod 1 = 0 trivially.
    # The interesting drift coordinate is the DRIFT residual
    #    y = (alpha * j - S_j) mod 1  =  (S_j - alpha*j) mod 1 reversed
    # i.e. the fractional part of the multiplier logarithm. This is the
    # natural "Furstenberg-y" datum for Collatz.
    for j, S in enumerate(S_seq, start=1):
        x = (alpha * j) % 1.0
        y = (alpha * j - S) % 1.0  # drift residual; fractional log of multiplier

        # z = sum_{i<j} a_i * alpha * (something) - use the canonical
        #   Furstenberg quadratic bracket: z_j = alpha * sum_{i<j} (i * a_i) mod 1
        # but we want a closed-form; use the trapezoidal version:
        # z_j = alpha * (j*S_j - sum_i S_i) / 1 mod 1 - this is the
        # discrete integral of x dy along the path.
        # Compute incrementally outside; here we just record (x,y,j,S).
        coords.append((x, y, j, S))
    # Now compute z_j = alpha * sum_{i<=j} (S_i) - alpha*j*S_j approximation
    z_list = []
    cum_S = 0.0
    for (x, y, j, S) in coords:
        cum_S += S
        # Heisenberg z-coord under BCH: discrete approximation of int x dy
        z_disc = (alpha * cum_S - alpha * j * S / 2.0) % 1.0
        z_list.append(z_disc)
    return [(c[0], c[1], z) for c, z in zip(coords, z_list)]


# ---------------------------------------------------------------------------
# 1. Equidistribution test on the Heisenberg nilmanifold
#
# Theorem (Furstenberg/Green-Tao folklore): a linear orbit on H_3(R)/H_3(Z)
# is equidistributed iff (alpha, beta, 1) are Q-linearly independent.
# (alpha=log_2 3, beta=1) -> alpha irrational, beta=1, so (alpha, 1, 1) has
# rank 2 over Q -> orbit equidistributes on a 2-dim sub-nilmanifold.
#
# We CHECK this numerically: compute the L^2 discrepancy of the empirical
# distribution of (x_j, y_j, z_j) against the uniform measure on a sub-
# nilmanifold.
# ---------------------------------------------------------------------------

def grid_discrepancy(coords, B=8):
    """Compute Linfty discrepancy: max over bins of |emp - 1/B^3|."""
    bins = np.zeros((B, B, B))
    for (x, y, z) in coords:
        ix = min(int(x * B), B-1)
        iy = min(int(y * B), B-1)
        iz = min(int(z * B), B-1)
        bins[ix, iy, iz] += 1
    bins /= len(coords)
    expected = 1.0 / (B**3)
    return float(np.max(np.abs(bins - expected))), float(bins.mean()), float(bins.std())


def marginal_test(coords):
    """Marginal in (x,y) plane (linear part) - should equidistribute fast.
    Marginal in z (quadratic part) - the Bohr-almost-periodicity test."""
    xs = np.array([c[0] for c in coords])
    ys = np.array([c[1] for c in coords])
    zs = np.array([c[2] for c in coords])

    # The 1D marginals
    def discrepancy_1d(arr, B=32):
        h = np.histogram(arr, bins=B, range=(0, 1))[0] / len(arr)
        return float(np.max(np.abs(h - 1.0/B)))

    return {
        "x_discrepancy_1d": discrepancy_1d(xs),
        "y_discrepancy_1d": discrepancy_1d(ys),
        "z_discrepancy_1d": discrepancy_1d(zs),
        "x_mean": float(xs.mean()),
        "y_mean": float(ys.mean()),
        "z_mean": float(zs.mean()),
    }


# ---------------------------------------------------------------------------
# 2. Bohr / Besicovitch test of (R_n mod 3^k):
#
# Compute the empirical Fourier spectrum on Z/3^k Z of the indicator
# sequence R_n mod 3^k, and compare to a "pure Bohr almost-periodic"
# baseline = a phase exp(2pi i alpha n) sampled at the same length.
#
# For a Bohr-AP sequence, the Fourier spectrum is supported on a countable
# set with summable amplitude. For a Weyl-equidistributed sequence on
# Z/3^k Z, the spectrum is roughly flat.
# ---------------------------------------------------------------------------

def syracuse_residue_sequence(N0, length, k=3):
    """Generate R_n mod 3^k by iterating Syracuse from N0."""
    mod = 3 ** k
    cur = N0
    seq = []
    for j in range(length):
        try:
            cur, _a = syracuse_step(cur)
        except AssertionError:
            break
        if cur == 1:
            break
        seq.append(cur % mod)
    return seq


def residue_fourier(seq, k=3):
    """Compute |DFT(1_{R_n = r})|^2 averaged over r, on Z/3^k.
    Returns the spectrum, normalised so that sum = 1."""
    mod = 3 ** k
    L = len(seq)
    if L < 10:
        return None
    arr = np.array(seq) % mod
    # Compute character sum: sum_{n} e^{2pi i xi r_n / mod}, for xi = 0..mod-1
    xis = np.arange(mod)
    # Use FFT-like direct computation
    spec = np.zeros(mod)
    for xi in range(mod):
        s = np.sum(np.exp(2j * np.pi * xi * arr / mod))
        spec[xi] = abs(s)**2 / L**2  # normalised
    # Drop the DC mode and look at the tail
    return spec.tolist()


# ---------------------------------------------------------------------------
# 3. The KEY structural test: does the Syracuse residue R_n mod 3^k correlate
# with a degree-2 nilsequence?
#
# A degree-2 nilsequence on Z is F(n alpha, n^2 alpha beta / 2 mod 1) for
# F Lipschitz on the torus. The natural candidate here:
#    Psi(n) = e( S_n * log_2 3 - n * log_2 3 ) - the "drift phase"
# We test <1_{R_n=r}, Psi(n)> averaged over the orbit.
#
# By Green-Tao / Tao's inverse theorem for Gowers norms, if Psi correlates
# with R_n nontrivially, then R_n is NOT pseudorandom on Z/3^k Z, i.e. NOT
# equidistributed. This is the precise way to ask: "does Collatz live on a
# nilmanifold?"
# ---------------------------------------------------------------------------

def nilsequence_correlation(seq, S_seq, alpha=LOG2_3, k=3):
    """For each residue r in Z/3^k, compute |E[1_{R_n=r} e(alpha*(S_n - j*alpha))]|.
    Large => the residue R_n is partly determined by the drift phase.
    Small => the residue is pseudorandom relative to the drift."""
    mod = 3 ** k
    L = min(len(seq), len(S_seq))
    if L < 10:
        return None
    correlations = {}
    for r in range(mod):
        # Indicator of R_n = r
        ind = np.array([1.0 if seq[j] == r else 0.0 for j in range(L)])
        # Drift phase: psi_j = exp(2pi i * (S_j*alpha - (j+1)*alpha))
        #            = exp(2pi i * alpha * (S_j - j - 1))
        S_arr = np.array(S_seq[:L])
        j_arr = np.arange(1, L+1)
        phase = np.exp(2j * np.pi * alpha * (S_arr - j_arr))
        corr = np.abs(np.sum(ind * phase)) / L
        correlations[r] = float(corr)
    return correlations


# ---------------------------------------------------------------------------
# 4. The "Heisenberg cocycle" view
#
# Sub-direction (iii): H_3(Z) acts on Z^3 by [[1,a,c],[0,1,b],[0,0,1]] -> upper
# triangular automorphism. Does the (2,3,carry) triple of Collatz embed?
#
# Concretely: the Collatz step on the binary expansion of an odd integer is
#   n = sum b_i 2^i -> 3n+1 = sum b'_i 2^i  (with carry propagation)
# The carry sequence c_i depends on previous carries (a triangular dependence)
# This is precisely the structure of a Heisenberg COCYCLE: if we encode
#   (sum_i b_i, sum_i c_i, sum_{i<j} b_i c_j)
# the third quantity has Heisenberg-quadratic structure.
#
# Probe: compute this triple over an orbit and test whether the third
# coordinate equidistributes (= Heisenberg orbit is dense) or sits in a
# sub-torus (= structured obstruction).
# ---------------------------------------------------------------------------

def bit_carry_heisenberg(N0, length=200):
    """Track the "carry-Heisenberg triple" along an orbit."""
    cur = N0
    triples = []
    for step in range(length):
        try:
            nxt, _a = syracuse_step(cur)
        except AssertionError:
            break
        if nxt == 1 or cur == 1:
            break
        # Compute carries from 3*cur+1 vs the new value
        m = 3 * cur + 1
        bits_old = []
        x = cur
        while x > 0:
            bits_old.append(x & 1)
            x >>= 1
        bits_new = []
        y = m
        while y > 0:
            bits_new.append(y & 1)
            y >>= 1
        # Carry sequence: in adding (n + 2n + 1), carries arise
        # Compute carry pattern at each bit
        carries = []
        c = 0
        for i in range(len(bits_old) + 2):
            bi = bits_old[i] if i < len(bits_old) else 0
            twice_bi = bits_old[i-1] if 0 < i <= len(bits_old) else 0
            init = 1 if i == 0 else 0
            tot = bi + twice_bi + init + c
            c = tot // 2
            carries.append(c)
        # The Heisenberg triple
        sum_b = sum(bits_old)
        sum_c = sum(carries)
        # The CRUCIAL quadratic invariant: sum_{i<j} b_i c_j
        Q = 0
        cum_c = 0
        for i in range(len(bits_old)):
            cum_c += carries[i] if i < len(carries) else 0
            Q += bits_old[i] * (sum_c - cum_c)
        triples.append((sum_b, sum_c, Q))
        cur = nxt
    return triples


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def main():
    print("=" * 72)
    print("Noncommutative ergodic / Heisenberg-nilmanifold probe for Collatz")
    print("=" * 72)

    # Test orbit: a fairly long Collatz orbit
    # 27 has orbit length ~ 70 steps via Syracuse; 27 * 2^k - 1 has long orbits
    # We use N0 = 871 (known long-orbit-starting odd number) and N0=27.

    out = {}

    for N0 in [27, 871, 6171, 77031, 837799]:
        print(f"\n--- N0 = {N0} ---")
        a_seq, S_seq, final = syracuse_data(N0, length=2000)
        L = len(a_seq)
        if L < 30:
            print(f"  orbit too short ({L} steps), skipping")
            continue
        print(f"  orbit length: {L}")
        print(f"  E[a] = {sum(a_seq)/L:.4f}  (compare log_2(3) = {LOG2_3:.4f})")

        # 1. Heisenberg embedding equidistribution
        coords = nilmanifold_coords(a_seq, S_seq)
        disc, mean, std = grid_discrepancy(coords, B=4)
        marg = marginal_test(coords)
        print(f"  3D grid L_inf discrepancy (B=4): {disc:.4f}  (target: small if equidistributes)")
        print(f"  x-marginal disc: {marg['x_discrepancy_1d']:.4f}")
        print(f"  y-marginal disc: {marg['y_discrepancy_1d']:.4f}")
        print(f"  z-marginal disc: {marg['z_discrepancy_1d']:.4f}")

        # 2. Bohr test on residues
        seq3 = syracuse_residue_sequence(N0, length=L, k=2)  # mod 9
        spec = residue_fourier(seq3, k=2)
        spec_max_nontrivial = max(spec[1:]) if spec else None
        print(f"  Residue mod 9, Fourier max (xi != 0): {spec_max_nontrivial:.4f}")
        print(f"  (Random/uniform expectation: ~ 1/L = {1.0/L:.4f})")

        # 3. Nilsequence correlation
        corr = nilsequence_correlation(seq3, S_seq[:len(seq3)], k=2)
        if corr is not None:
            corr_vals = list(corr.values())
            print(f"  Nilseq correlation max: {max(corr_vals):.4f}")
            print(f"  Nilseq correlation mean: {sum(corr_vals)/len(corr_vals):.4f}")
            print(f"  (Pseudorandom expectation: ~ sqrt(1/9 * 8/9 / L) = {sqrt(1.0/9 * 8.0/9 / L):.4f})")

        out[str(N0)] = {
            "orbit_length": L,
            "E_a": sum(a_seq)/L,
            "heisenberg_disc_B4": disc,
            "heisenberg_disc_mean": mean,
            "heisenberg_disc_std": std,
            "x_disc": marg["x_discrepancy_1d"],
            "y_disc": marg["y_discrepancy_1d"],
            "z_disc": marg["z_discrepancy_1d"],
            "residue_mod9_fourier_max_nontrivial": spec_max_nontrivial,
            "nilseq_correlation_max": max(corr.values()) if corr else None,
            "nilseq_correlation_mean": sum(corr.values())/len(corr) if corr else None,
            "pseudorandom_baseline": sqrt(1.0/9 * 8.0/9 / L),
        }

    # 4. Bit-carry Heisenberg triple
    print("\n--- Carry-Heisenberg cocycle (sub-direction iii) ---")
    triples = bit_carry_heisenberg(27, length=20)
    if triples:
        print(f"  steps recorded: {len(triples)}")
        print(f"  first few triples (sum_b, sum_c, Q): {triples[:5]}")
        # The KEY question: is Q correlated with (sum_b, sum_c)?
        # If yes (linear relation) -> degenerate, lives on a sub-nilmanifold
        # If no -> genuinely 2-step structure
        arr = np.array(triples, dtype=float)
        if arr.shape[0] > 5:
            # Linear regression: Q ~ alpha * sum_b + beta * sum_c + gamma
            from numpy.linalg import lstsq
            X = np.column_stack([arr[:, 0], arr[:, 1], np.ones(arr.shape[0])])
            y = arr[:, 2]
            coef, res, rank, sv = lstsq(X, y, rcond=None)
            pred = X @ coef
            ss_res = float(np.sum((y - pred)**2))
            ss_tot = float(np.sum((y - y.mean())**2))
            r2 = 1.0 - ss_res/ss_tot if ss_tot > 0 else None
            print(f"  R^2 of Q vs (sum_b, sum_c, 1): {r2}")
            out["bit_carry"] = {
                "n_triples": len(triples),
                "linear_R2": r2,
                "first_triples": triples[:10],
            }

    # 5. SUMMARY / verdict
    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print("If nilseq_correlation_max >> pseudorandom_baseline,")
    print("then R_n IS partly determined by a degree-2 nilsequence -> structured.")
    print("If they are comparable, the residue is pseudorandom relative to the")
    print("drift phase -> no nilsequence obstruction; Heisenberg angle inert.")
    print()
    print("Interpretation per orbit:")
    for N0, d in out.items():
        if N0 == "bit_carry":
            continue
        if d.get("nilseq_correlation_max") is None:
            continue
        ratio = d["nilseq_correlation_max"] / d["pseudorandom_baseline"]
        verdict = "STRUCTURED" if ratio > 5.0 else ("WEAK" if ratio > 2.0 else "PSEUDORANDOM")
        print(f"  N0={N0}: correlation/baseline = {ratio:.2f} -> {verdict}")

    # Save
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    out_path = os.path.join(data_dir, "noncommutative_nilmanifold_probe.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
