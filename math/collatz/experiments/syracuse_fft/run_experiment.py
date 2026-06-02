"""
Main driver for the decisive Collatz "Vector A" experiment.

Computes the collision diagnostic  E_n = phi(3^n) CP_n - 1  for the Syracuse
random variable on (Z/3^n Z)^x, for n = 2 .. NMAX, under several tilting schemes:

  * UNTILTED          s = 0                 (plain Geom(2); prior agent's baseline)
  * SCALAR ESSCHER    s = s* ~ 0.438        (descent-balance tilt; E_{s*}[a]=log_2 3)
  * n-DEPENDENT TILT  s = s_n               (a schedule of scalar tilts; see below)
  * xi-DEPENDENT TILT (Fourier-side reweighting per frequency; see compute_En_xitilt)

Saves raw data to data/ and prints tables.  All laws are computed EXACTLY (up to
double-precision FFT round-off, validated <1e-15 against the direct DP for n<=6 by
crosscheck.py, and CP_n cross-validated by Plancherel at every n).

Run:  python3 run_experiment.py [NMAX]
"""

from __future__ import annotations

import json
import math
import os
import sys
import time

import numpy as np

from syracuse_fft import (GroupStructure, syracuse_law_fft,
                          collision_excess_from_law, geom_kernel_dlog)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

S_STAR = -math.log2(1 - 1 / math.log(3, 2)) - 1.0  # descent-balance tilt ~0.438033


# ---------------------------------------------------------------------------
# xi-dependent tilt:  a Fourier-side scheme.
# ---------------------------------------------------------------------------
# Motivation (tao_syracuse_explicit.md sec 6.4, reading (ii)): the single scalar
# Esscher tilt may be "too crude"; the correct object may be a xi- or n-dependent
# tilt.  We implement TWO concrete xi-dependent schemes (plus the n-dependent one):
#
# XI-A ("frequency-adaptive lower envelope"): per xi take the MINIMUM
# |phi_n^{(s)}(xi)| over a grid of scalar tilts, then form E_n from that envelope:
#    E_n^{xi-best} = phi(3^n) * (1/3^n) sum_xi min_s |phi_n^{(s)}(xi)|^2 - 1.
# CAVEAT (found empirically): this envelope is DEGENERATE -- the per-xi argmin
# collapses to a single near-edge tilt s ~ -0.9 for ALL xi, and the "envelope"
# value -> 0 as the grid is extended toward s -> -1.  So XI-A does NOT exhibit
# genuine xi-dependence; it merely rediscovers that one scalar negative tilt
# already equidistributes (see scheme `scalar_plateau`).  Reported as such.
#
# XI-B ("v_3(xi)-stratified tilt"): a genuinely xi-dependent assignment that
# respects the only natural invariant of a frequency under the (Z/3^n)^x action,
# namely L(xi) = v_3(xi) (its 3-adic valuation, 0..n).  We pick a tilt s_L for
# each stratum L and assemble the hybrid characteristic function
#    phi_hybrid(xi) = phi_n^{(s_{L(xi)})}(xi),   E_n^{XI-B} = phi(3^n)*||phi_hybrid||_2^2/3^n - 1.
# This asks: if the tilt may depend on the frequency's 3-adic scale, does E_n->0?


def char_fn_from_law(law: np.ndarray) -> np.ndarray:
    """phi_n(xi) for all xi = FFT of the law (with the e(-xi b/3^n) convention)."""
    return np.fft.fft(law)


def compute_En_scalar(n: int, s: float) -> dict:
    law = syracuse_law_fft(n, s=s)
    En = collision_excess_from_law(law, n)
    cp = float(np.dot(law, law))
    return {"n": n, "scheme": f"scalar(s={s:.6f})", "s": s, "CP_n": cp, "E_n": En}


def compute_En_xitilt(n: int, s_grid: np.ndarray) -> dict:
    """XI-A: per-xi minimum |phi^{(s)}(xi)| envelope (optimistic; see header caveat)."""
    modulus = 3 ** n
    best = None
    for s in s_grid:
        law = syracuse_law_fft(n, s=float(s))
        phi = char_fn_from_law(law)
        mag2 = (phi.real ** 2 + phi.imag ** 2)
        mag2[0] = 1.0
        best = mag2 if best is None else np.minimum(best, mag2)
    cp = float(best.sum()) / modulus
    phi3n = 2 * 3 ** (n - 1)
    return {"n": n, "scheme": "xi-best-envelope", "s_grid": [float(x) for x in s_grid],
            "CP_n": cp, "E_n": phi3n * cp - 1.0}


def _v3_of_xi(n: int) -> np.ndarray:
    """3-adic valuation L(xi)=v_3(xi) for all xi in Z/3^n (v_3(0):=n)."""
    modulus = 3 ** n
    gs = GroupStructure(n)
    return gs.val  # already computed there


def compute_En_v3_stratified(n: int, s_by_L) -> dict:
    """
    XI-B: assemble phi_hybrid(xi) = phi^{(s_{L(xi)})}(xi) with L=v_3(xi), using the
    tilt schedule s_by_L (a callable L -> s, or a dict).  Returns E_n from the
    hybrid L2 mass.  Computes the law once per DISTINCT tilt value actually used.
    """
    modulus = 3 ** n
    L = _v3_of_xi(n)
    # distinct tilts needed
    Ls = list(range(n + 1))
    tilts = {}
    for Lv in Ls:
        tilts[Lv] = float(s_by_L(Lv)) if callable(s_by_L) else float(s_by_L[Lv])
    # group strata by tilt value to avoid recomputation
    uniq = {}
    for Lv, sv in tilts.items():
        uniq.setdefault(round(sv, 10), []).append(Lv)
    mag2_hybrid = np.empty(modulus, dtype=np.float64)
    for sv, Lgroup in uniq.items():
        law = syracuse_law_fft(n, s=float(sv))
        phi = char_fn_from_law(law)
        m2 = phi.real ** 2 + phi.imag ** 2
        sel = np.isin(L, Lgroup)
        mag2_hybrid[sel] = m2[sel]
    mag2_hybrid[0] = 1.0  # xi=0 normalization
    cp = float(mag2_hybrid.sum()) / modulus
    phi3n = 2 * 3 ** (n - 1)
    return {"n": n, "scheme": "v3-stratified", "tilts_by_L": tilts,
            "CP_n": cp, "E_n": phi3n * cp - 1.0}


def main(nmax: int = 14) -> None:
    print("=" * 78)
    print("Collatz Vector A: collision diagnostic E_n = phi(3^n) CP_n - 1")
    print(f"FFT W-recursion, n=2..{nmax}, descent-balance tilt s* = {S_STAR:.6f}")
    print("=" * 78)

    results = {"s_star": S_STAR, "schemes": {}}

    # ---- (1) untilted and (2) scalar Esscher s* ----
    for tag, s in [("untilted", 0.0), ("esscher_sstar", S_STAR)]:
        seq = []
        print(f"\n[{tag}]  s = {s:.6f}")
        print(f"  {'n':>2} {'CP_n':>16} {'E_n':>14} {'dE':>11} {'ratio':>8}")
        prev = None
        for n in range(2, nmax + 1):
            t0 = time.time()
            r = compute_En_scalar(n, s)
            dt = time.time() - t0
            dE = (r["E_n"] - prev) if prev is not None else float("nan")
            ratio = (r["E_n"] / prev) if prev is not None else float("nan")
            r["dE"] = dE
            r["ratio"] = ratio
            r["time_s"] = dt
            seq.append(r)
            print(f"  {n:>2} {r['CP_n']:>16.6e} {r['E_n']:>14.6f} "
                  f"{dE:>11.5f} {ratio:>8.4f}")
            prev = r["E_n"]
        results["schemes"][tag] = seq

    # ---- (3) scalar PLATEAU tilts (the key new finding): negative tilts ----
    # For s <~ -0.45 the law equidistributes: E_n is BOUNDED in n (-> const, and
    # const -> 0 as s -> -1+).  These tilts FATTEN the valuation tail (E[a] > 2),
    # the opposite of the descent-balance tilt s*>0.  We record three.
    for s_val in [-0.30, -0.50, -0.90]:
        tag = f"scalar_neg_{s_val:+.2f}".replace("+", "p").replace("-", "m").replace(".", "")
        seq = []
        print(f"\n[scalar plateau]  s = {s_val:+.3f}  (E[a]={1/(1-0.5**(1+s_val)):.3f})")
        print(f"  {'n':>2} {'CP_n':>16} {'E_n':>14} {'dE':>11}")
        prev = None
        for n in range(2, nmax + 1):
            r = compute_En_scalar(n, s_val)
            dE = (r["E_n"] - prev) if prev is not None else float("nan")
            r["dE"] = dE
            seq.append(r)
            print(f"  {n:>2} {r['CP_n']:>16.6e} {r['E_n']:>14.6f} {dE:>11.5f}")
            prev = r["E_n"]
        results["schemes"][tag] = seq

    # ---- (4) n-dependent scalar tilt schedule (partial Esscher) ----
    seq = []
    tag = "ndep_partial_esscher"
    print(f"\n[{tag}]  s_n = s* * (1 - 1/sqrt(n))  (-> s* slowly; exploratory)")
    print(f"  {'n':>2} {'s_n':>9} {'CP_n':>16} {'E_n':>14} {'dE':>11}")
    prev = None
    for n in range(2, nmax + 1):
        s_n = S_STAR * (1.0 - 1.0 / math.sqrt(n))
        r = compute_En_scalar(n, s_n)
        r["s"] = s_n
        dE = (r["E_n"] - prev) if prev is not None else float("nan")
        r["dE"] = dE
        seq.append(r)
        print(f"  {n:>2} {s_n:>9.4f} {r['CP_n']:>16.6e} {r['E_n']:>14.6f} {dE:>11.5f}")
        prev = r["E_n"]
    results["schemes"][tag] = seq

    # ---- (5) xi-dependent scheme XI-A: best-envelope (optimistic; DEGENERATE) ----
    seq = []
    tag = "xi_best_envelope"
    s_grid = np.linspace(-0.95, 1.2, 22)  # wide, includes near-edge negative tilts
    n_cap = min(nmax, 12)
    print(f"\n[{tag}]  XI-A per-xi min over s in [{s_grid[0]:.2f},{s_grid[-1]:.2f}] "
          f"({len(s_grid)} pts), n=2..{n_cap}  (NOTE: degenerate, see header)")
    print(f"  {'n':>2} {'CP_n':>16} {'E_n':>14} {'dE':>11}")
    prev = None
    for n in range(2, n_cap + 1):
        r = compute_En_xitilt(n, s_grid)
        dE = (r["E_n"] - prev) if prev is not None else float("nan")
        r["dE"] = dE
        seq.append(r)
        print(f"  {n:>2} {r['CP_n']:>16.6e} {r['E_n']:>14.6f} {dE:>11.5f}")
        prev = r["E_n"]
    results["schemes"][tag] = seq

    # ---- (6) xi-dependent scheme XI-B: v_3(xi)-stratified tilt ----
    # Tilt depends on the frequency's 3-adic valuation L=v_3(xi).  We test a
    # schedule that uses the descent-balance s* on the "coarse" (small-L, high-
    # frequency) strata and a plateau tilt on "fine" (large-L) strata, to see if
    # frequency-localizing the tilt repairs the s* divergence.  Schedule:
    #   s_L = s*           for L <= n/2   (the genuinely oscillatory frequencies)
    #   s_L = -0.5         for L >  n/2   (low-frequency, near-DC strata)
    seq = []
    tag = "xi_v3_stratified"
    print(f"\n[{tag}]  XI-B s_L = s* for v_3(xi)<=n/2 else -0.5,  n=2..{n_cap}")
    print(f"  {'n':>2} {'CP_n':>16} {'E_n':>14} {'dE':>11}")
    prev = None
    for n in range(2, n_cap + 1):
        sched = (lambda L, n=n: S_STAR if L <= n / 2 else -0.5)
        r = compute_En_v3_stratified(n, sched)
        dE = (r["E_n"] - prev) if prev is not None else float("nan")
        r["dE"] = dE
        seq.append(r)
        print(f"  {n:>2} {r['CP_n']:>16.6e} {r['E_n']:>14.6f} {dE:>11.5f}")
        prev = r["E_n"]
    results["schemes"][tag] = seq

    # ---- (7) tilt sweep E_n(s) at fixed n, for the phase-transition figure ----
    sweep = {}
    s_vals = list(np.round(np.linspace(-0.95, 0.6, 32), 4))
    print(f"\n[tilt sweep]  E_n(s) for n in {{4,8,12}}, s in [-0.95,0.6]")
    for n in [4, 8, 12]:
        row = []
        for s in s_vals:
            law = syracuse_law_fft(n, s=float(s))
            row.append(collision_excess_from_law(law, n))
        sweep[n] = row
    results["tilt_sweep"] = {"s_vals": [float(s) for s in s_vals],
                             "E_by_n": {str(k): v for k, v in sweep.items()}}

    # ---- save raw ----
    out = os.path.join(DATA_DIR, "En_results.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved raw results -> {out}")

    # also dump compact CSVs per scheme for figures
    for tag, seq in results["schemes"].items():
        path = os.path.join(DATA_DIR, f"En_{tag}.csv")
        with open(path, "w") as f:
            f.write("n,s,CP_n,E_n\n")
            for r in seq:
                f.write(f"{r['n']},{r.get('s','')},{r['CP_n']:.12e},{r['E_n']:.12e}\n")
        print(f"  wrote {path}")


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    main(nmax)
