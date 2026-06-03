"""
frankl_freqsos.py -- the clean, fully-validated companion instrument:
the degree-2 vs degree-4 SOS lower bound on  max_i freq_i / |F|  for a fixed
family, where the relaxation knows F only through the S_n-invariant frequency
power sums p_k = sum_i freq_i^k (k <= 2d).  These power sums ARE the symmetric
degree-<=2d incidence moments:
    p1 = sum_S |S|                (deg-1 incidence orbit data)
    p2 = sum_{A,B in F} |A cap B| (deg-2 incidence orbit data; the JI-overlap/2nd moment)
    p3 = sum_{A,B,C} |A&B&C|      (deg-3 / subset-triple orbit data)
    p4 = sum over quadruples      (deg-4 / subset-quadruple orbit data)

This isolates the FREQUENCY-MOMENT content of the Lasserre hierarchy.  The
companion frankl_sos_las2.py runs the FULL incidence SDP (which additionally
carries the genuinely-non-frequency subset-configuration moments); comparing the
two tells us whether the full incidence level-2 buys anything BEYOND the
frequency power-sum content.

Author: Alex Ye (no AI on author line).

Bounds computed for each family F and level d in {1,2}:
  * power-mean (the project's quoted lb_1) = p2/p1/|F|  (a SPECIFIC valid deg-2
    certificate: max_i x_i >= (sum x_i^2)/(sum x_i)).
  * Hankel min-max lb_d = the TIGHTEST degree-2d certified lower bound on
    max_i x_i using only p_1..p_{2d}: the smallest L such that a nonneg measure
    with averaged moments mu_k=p_k/n exists supported on [0, L] (a 1-D truncated
    moment / principal-representation problem), as a fraction of |F|.

VALIDATION the instrument must pass:
  (a) cube 2^[k]: all freqs equal => the measure is a single atom => Hankel lb_d =
      true = 1/2 at EVERY d (the ceiling, reached).
  (b) level-1 reference equals / brackets the power-mean.

Run: python3 frankl_freqsos.py
"""
from __future__ import annotations
import json
import os
import numpy as np

LOPSIDED = {
    "n5_F3a_minimal": (5, [0, 16, 31]),
    "n4_F3":          (4, [0, 8, 15]),
    "n5_F3b":         (5, [0, 16, 23]),
    "n5_F5":          (5, [0, 8, 16, 24, 31]),
    "n5_F6":          (5, [0, 8, 16, 23, 24, 31]),
    "n5_F7":          (5, [0, 8, 15, 16, 23, 24, 31]),
}


def freqs_of(F, n):
    return [sum(1 for S in F if (S >> i) & 1) for i in range(n)]


def power_sums(fr, upto):
    return [float(sum(f ** k for f in fr)) for k in range(upto + 1)]


def power_mean(fr, M):
    p1 = sum(fr); p2 = sum(f * f for f in fr)
    return (p2 / p1) / M if p1 else 0.0


def hankel_lb(fr, d, M):
    """Tightest degree-2d certified lower bound on max_i fr_i, /M.

    The empirical freq measure nu = (1/n) sum delta_{fr_i} has averaged moments
    mu_k = (sum fr_i^k)/n, KNOWN for k=0..2d (mu_0=1).  The certified lower bound
    on the largest support point of ANY measure with those moments is the smallest
    t for which a representing measure supported on [0,t] EXISTS, i.e. the
    truncated [0,t]-moment problem is feasible:
        Hankel  H_d = [mu_{i+j}]_{0<=i,j<=d}              >= 0
        x>=0:   H'_{d-1} = [mu_{i+j+1}]_{0<=i,j<=d-1}     >= 0
        x<=t:   t*H_{d-1} - H'_{d-1}                       >= 0
    (mu fixed; only t varies).  Bisect on t.  Return t/M."""
    n = len(fr)
    mu = [sum(f ** k for f in fr) / n for k in range(2 * d + 1)]

    def feas(t):
        Hd = np.array([[mu[i + j] for j in range(d + 1)] for i in range(d + 1)])
        if np.linalg.eigvalsh(Hd).min() < -1e-9:
            return False
        if d >= 1:
            Hx = np.array([[mu[i + j + 1] for j in range(d)] for i in range(d)])
            Htx = np.array([[t * mu[i + j] - mu[i + j + 1] for j in range(d)] for i in range(d)])
            if np.linalg.eigvalsh(Hx).min() < -1e-9:
                return False
            if np.linalg.eigvalsh(Htx).min() < -1e-9:
                return False
        return True

    lo, hi = 0.0, max(fr) + 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if feas(mid):
            hi = mid
        else:
            lo = mid
    return hi / M


def main():
    print("=" * 76)
    print("Frequency power-sum SOS lower bound on max_i freq_i/|F|  (levels 1,2)")
    print("=" * 76)
    print("\n[VALIDATION a] cube 2^[k]: all freqs equal -> single atom -> lb=1/2 each d")
    cube_rows = []
    for k in (1, 2, 3, 4):
        F = list(range(1 << k))
        fr = freqs_of(F, k)
        M = len(F)
        l1 = hankel_lb(fr, 1, M)
        l2 = hankel_lb(fr, 2, M)
        print(f"   cube 2^[{k}]: freqs={fr} |F|={M}  hankel_lb1={l1:.4f} "
              f"hankel_lb2={l2:.4f}  (expect 0.5)")
        cube_rows.append(dict(k=k, lb1=l1, lb2=l2))

    print("\n[MAIN] 6 lopsided families: power-mean (project lb_1) vs Hankel lb_1, lb_2")
    table = []
    for name, (n, F) in LOPSIDED.items():
        fr = freqs_of(F, n)
        M = len(F)
        pm = power_mean(fr, M)
        h1 = hankel_lb(fr, 1, M)
        h2 = hankel_lb(fr, 2, M)
        ta = max(fr) / M
        table.append(dict(name=name, n=n, sizeF=M, freqs=fr, true_ab=ta,
                          power_mean=pm, hankel_lb1=h1, hankel_lb2=h2,
                          gap_h2_h1=h2 - h1, gap_h2_pm=h2 - pm))
        print(f"   {name:16s} freqs={str(fr):16s} true={ta:.4f}  pm={pm:.4f}  "
              f"h_lb1={h1:.4f}  h_lb2={h2:.4f}  (h2-h1={h2-h1:+.4f})")

    out = dict(cube=cube_rows, families=table)
    os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)
    path = os.path.join(os.path.dirname(__file__), "data", "freqsos_results.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {path}")


if __name__ == "__main__":
    main()
