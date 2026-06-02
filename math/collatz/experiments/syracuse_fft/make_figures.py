"""
Generate figures for the decisive Collatz Vector A experiment from data/En_results.json.

Figures (saved to figures/):
  fig1_En_logscale.png   : E_n vs n, log-y, all scalar schemes (untilted, s*, plateau tilts)
  fig2_tilted_vs_untilted.png : E_n vs n, linear-y, untilted vs descent-balance s*
  fig3_tilt_sweep.png    : E_n(s) at fixed n in {4,8,12} -- the equidistribution phase transition
  fig4_xi_dependent.png  : xi-dependent variants (XI-A envelope, XI-B v3-stratified) vs scalar baselines

Run:  python3 make_figures.py
"""

from __future__ import annotations

import json
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "data", "En_results.json")
FIGDIR = os.path.join(HERE, "figures")
os.makedirs(FIGDIR, exist_ok=True)


def load():
    with open(DATA) as f:
        return json.load(f)


def seq_xy(R, tag):
    s = R["schemes"][tag]
    return np.array([r["n"] for r in s]), np.array([r["E_n"] for r in s])


def main():
    R = load()
    sstar = R["s_star"]
    schemes = R["schemes"]

    # ---------- Figure 1: E_n vs n, log scale ----------
    plt.figure(figsize=(7.5, 5.2))
    plot_specs = [
        ("untilted", "untilted  s=0  (linear growth)", "o-", "tab:blue"),
        ("esscher_sstar", f"descent-balance  s*={sstar:.3f}  (exponential growth)", "s-", "tab:red"),
        ("scalar_neg_m030", "s=-0.30  (slow growth)", "^-", "tab:orange"),
        ("scalar_neg_m050", "s=-0.50  (bounded plateau)", "v-", "tab:green"),
        ("scalar_neg_m090", "s=-0.90  (bounded ~0.004)", "D-", "tab:purple"),
    ]
    for tag, lab, mk, col in plot_specs:
        if tag in schemes:
            n, E = seq_xy(R, tag)
            plt.semilogy(n, E, mk, color=col, label=lab, ms=4)
    plt.xlabel("n")
    plt.ylabel(r"$E_n = \varphi(3^n)\,\mathrm{CP}_n - 1$   (log scale)")
    plt.title("Syracuse collision diagnostic $E_n$ vs $n$ (FFT, exact)\n"
              r"$E_n\to 0$ is the natural-density requirement; $TV\leq\frac{1}{2}\sqrt{E_n}$")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend(fontsize=8, loc="best")
    plt.tight_layout()
    p1 = os.path.join(FIGDIR, "fig1_En_logscale.png")
    plt.savefig(p1, dpi=140)
    plt.close()

    # ---------- Figure 2: tilted vs untilted, linear ----------
    plt.figure(figsize=(7.5, 5.2))
    n, E = seq_xy(R, "untilted")
    plt.plot(n, E, "o-", color="tab:blue", label="untilted s=0")
    # linear fit overlay
    m = n >= 5
    a, b = np.polyfit(n[m], E[m], 1)
    plt.plot(n, a * n + b, "--", color="tab:blue", alpha=0.6,
             label=f"linear fit  {a:.3f} n {b:+.3f}")
    n2, E2 = seq_xy(R, "esscher_sstar")
    plt.plot(n2, E2, "s-", color="tab:red", label=f"descent-balance s*={sstar:.3f}")
    lr = np.polyfit(n2[n2 >= 6], np.log(E2[n2 >= 6]), 1)
    plt.plot(n2, np.exp(lr[1]) * np.exp(lr[0] * n2), "--", color="tab:red", alpha=0.6,
             label=f"exp fit  {math.exp(lr[1]):.2f}·{math.exp(lr[0]):.3f}$^n$")
    plt.xlabel("n")
    plt.ylabel(r"$E_n$")
    plt.title("Descent-balance tilt makes equidistribution WORSE\n"
              "(untilted: linear divergence; tilted s*: exponential divergence)")
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=8)
    plt.tight_layout()
    p2 = os.path.join(FIGDIR, "fig2_tilted_vs_untilted.png")
    plt.savefig(p2, dpi=140)
    plt.close()

    # ---------- Figure 3: tilt sweep E_n(s) -- phase transition ----------
    sw = R["tilt_sweep"]
    s_vals = np.array(sw["s_vals"])
    plt.figure(figsize=(7.5, 5.2))
    for nk, col in [("4", "tab:gray"), ("8", "tab:cyan"), ("12", "tab:brown")]:
        if nk in sw["E_by_n"]:
            plt.semilogy(s_vals, sw["E_by_n"][nk], "-", color=col, label=f"n={nk}")
    # mark reference tilts
    plt.axvline(0.0, color="tab:blue", ls=":", alpha=0.7, label="untilted s=0")
    plt.axvline(sstar, color="tab:red", ls=":", alpha=0.7, label=f"descent-balance s*={sstar:.3f}")
    plt.axvspan(-0.95, -0.45, color="green", alpha=0.08, label="bounded/plateau region")
    plt.xlabel("tilt parameter s")
    plt.ylabel(r"$E_n(s)$  (log scale)")
    plt.title("Equidistribution phase transition in tilt space\n"
              "curves COINCIDE for s<~-0.45 (E_n n-independent) and FAN OUT for s>~-0.4 (E_n grows in n)")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend(fontsize=8, loc="upper left")
    plt.tight_layout()
    p3 = os.path.join(FIGDIR, "fig3_tilt_sweep.png")
    plt.savefig(p3, dpi=140)
    plt.close()

    # ---------- Figure 4: xi-dependent variants ----------
    plt.figure(figsize=(7.5, 5.2))
    for tag, lab, mk, col in [
        ("untilted", "scalar untilted s=0", "o-", "tab:blue"),
        ("esscher_sstar", f"scalar s*={sstar:.3f}", "s-", "tab:red"),
        ("xi_best_envelope", "XI-A per-xi-min envelope (degenerate->edge tilt)", "x--", "tab:green"),
        ("xi_v3_stratified", "XI-B v3(xi)-stratified tilt", "P-", "tab:purple"),
    ]:
        if tag in schemes:
            n, E = seq_xy(R, tag)
            plt.semilogy(n, np.clip(E, 1e-6, None), mk, color=col, label=lab, ms=4)
    plt.xlabel("n")
    plt.ylabel(r"$E_n$  (log scale)")
    plt.title("xi-dependent tilting schemes vs scalar baselines\n"
              "(no genuine xi-dependence beats a single scalar plateau tilt)")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend(fontsize=8, loc="best")
    plt.tight_layout()
    p4 = os.path.join(FIGDIR, "fig4_xi_dependent.png")
    plt.savefig(p4, dpi=140)
    plt.close()

    print("Figures written:")
    for p in (p1, p2, p3, p4):
        print("  ", p)


if __name__ == "__main__":
    main()
