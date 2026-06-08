"""
Probe 2: isolate where the residue-mod-9 Fourier spectrum concentrates,
to confirm the mod-3 obstruction is the entirety of the "Bohr-AP" signal.

We split xi mod 9 into:
   xi = 0      (DC mode)
   xi in {3, 6} (= multiples of 3, the mod-3 quotient sub-character group)
   xi in {1,2,4,5,7,8} (the "interior" characters)

If all the mass is at xi in {3,6}, then the Bohr-AP signal is EXACTLY the
mod-3 obstruction known to the project (perpendicular to U_n, kernel of
P_n - identity, Tao-erratum). NOTHING NEW. This is the test.
"""

import numpy as np
from math import sqrt


def syracuse_step(n):
    assert n % 2 == 1
    m = 3 * n + 1
    a = 0
    while m % 2 == 0:
        m //= 2
        a += 1
    return m, a


def residue_sequence(N0, length, k=2):
    mod = 3 ** k
    cur = N0
    seq = []
    for j in range(length):
        try:
            cur, _ = syracuse_step(cur)
        except AssertionError:
            break
        if cur == 1:
            break
        seq.append(cur % mod)
    return seq


def fourier_breakdown(seq, k=2):
    mod = 3 ** k
    L = len(seq)
    arr = np.array(seq)
    spec_xi = {}
    for xi in range(mod):
        s = np.sum(np.exp(2j * np.pi * xi * arr / mod))
        spec_xi[xi] = abs(s)**2 / L**2
    # Partition by whether 3 | xi (i.e. the mod-3 projection)
    mod3_xi = [xi for xi in range(mod) if xi != 0 and xi % 3 == 0]
    interior_xi = [xi for xi in range(mod) if xi != 0 and xi % 3 != 0]
    mass_mod3 = sum(spec_xi[xi] for xi in mod3_xi)
    mass_interior = sum(spec_xi[xi] for xi in interior_xi)
    return spec_xi, mass_mod3, mass_interior, L


def main():
    print("Residue-mod-9 Fourier breakdown - PER ORBIT.")
    print("(Bohr-AP signal for a single orbit; not the ensemble Tao-distribution.)")
    print("=" * 80)
    print(f"{'N0':>10} {'L':>5} {'max@3|xi':>10} {'max@3∤xi':>10} {'baseline':>10} {'verdict':>15}")
    print("-" * 80)

    for N0 in [27, 871, 6171, 77031, 837799, 8400511]:
        seq = residue_sequence(N0, length=3000, k=2)
        if len(seq) < 30:
            continue
        spec, mm3, mint, L = fourier_breakdown(seq)
        max_mod3 = max((spec[xi] for xi in [3, 6]), default=0)
        max_interior = max((spec[xi] for xi in [1, 2, 4, 5, 7, 8]), default=0)
        baseline = 1.0 / L
        verdict = "MOD-3 ONLY" if max_mod3 > 0.1 and max_interior < 3 * baseline else \
                  "BROADER AP" if max_interior > 5 * baseline else "PSEUDORAND"
        print(f"{N0:>10} {L:>5} {max_mod3:>10.4f} {max_interior:>10.4f} {baseline:>10.4f}  {verdict:>15}")

    # The honest ENSEMBLE test:
    # Take ALL odd N0 <= M and look at R_n mod 9 for fixed n (single step depth).
    # Tao's analysis predicts this approaches a known limit law on (Z/9)*.
    print()
    print("ENSEMBLE TEST: across all odd N0 <= 99999, at fixed Syracuse depth n=20,")
    print("look at distribution of R_n mod 9 and its Fourier coefficients.")
    print()
    n_steps = 20
    M = 99999
    samples = []
    for N0 in range(1, M, 2):
        cur = N0
        ok = True
        for _ in range(n_steps):
            try:
                cur, _ = syracuse_step(cur)
            except AssertionError:
                ok = False; break
            if cur == 1:
                ok = False; break
        if ok:
            samples.append(cur % 9)
    arr = np.array(samples)
    L = len(arr)
    print(f"  ensemble size: {L}")
    print(f"  histogram of R_n mod 9 at depth n=20:")
    for r in range(9):
        print(f"    {r}: {np.mean(arr == r):.4f}")
    # Fourier
    print(f"  Fourier coefficients:")
    for xi in range(9):
        s = np.mean(np.exp(2j * np.pi * xi * arr / 9))
        print(f"    xi={xi}: |coef|={abs(s):.4f}  (3|xi: {'yes' if xi%3==0 and xi>0 else 'no'})")
    # mod-3 ensemble
    print(f"  mod-3 ensemble histogram: 0->{np.mean(arr%3==0):.4f}, 1->{np.mean(arr%3==1):.4f}, 2->{np.mean(arr%3==2):.4f}")
    print("  (Tao prediction: 0, 1/3, 2/3 - the permanent mod-3 obstruction)")

    print()
    print("If column 'max@3|xi' stays large (independent of L) AND")
    print("'max@3∤xi' decays at ~ 1/L baseline rate, then the entire Bohr-AP")
    print("content of R_n mod 9 is the known mod-3 obstruction -> nothing new.")
    print()
    print("Theoretical prediction: R_n mod 3 = (2 * Syr(n) mod 3) cycle is forced")
    print("by Tao's analysis (b(r) mod 3 frequencies = (0, 1/3, 2/3) for r in (Z/3)*).")
    print("So |E[e(xi * R_n / 9)]|^2 at xi=3 (= mod-3 projection) is exactly the")
    print("squared distance from uniform on {0,1,2} mod 3 = 5/9 ≈ 0.555 max.")

    # Cross check: compute analytic prediction for xi=3.
    # E[e(2pi i (3/9) R_n)] = E[e(2pi i R_n / 3)].
    # The mod-3 distribution converges to (0, 1/3, 2/3) (Tao law).
    # So E[e(2pi i / 3 * R_n)] -> 0 * 1 + (1/3) * w + (2/3) * w^2
    # where w = e(1/3) = -1/2 + i sqrt(3)/2
    # = w/3 + 2 w^2 / 3.
    # |...|^2 = (1/3 + 2/3 w)(conj) hmm let me just compute
    w = np.exp(2j * np.pi / 3.0)
    expected = (1.0/3) * w + (2.0/3) * w**2
    print(f"\nAnalytic |E[e(R_n/3)]|^2 at mod-3 limit (0, 1/3, 2/3): {abs(expected)**2:.4f}")
    print("This is the floor that |xi=3 Fourier| approaches as L -> infinity.")


if __name__ == "__main__":
    main()
