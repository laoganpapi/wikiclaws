"""
make_figures.py — Figures for the entropy-method joint-optimization study.

Produces (into figures/):
  1. crossover.png        — h(2p-p^2) vs h(p), crossover at p=psi.
  2. sawin_slack.png      — slack of the Sawin inequality (S) on the diagonal and a slice.
  3. threshold_vs_U.png   — certified threshold c vs |U| (flat at psi; the plateau).
  4. feasibility_vs_t.png — best feasibility gap of (IV) on [0,t] vs t, zero-crossing at psi.

Author: Alex Ye (AI assistance disclosed separately).
"""
from __future__ import annotations

import math
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
FIG = os.path.join(HERE, "figures")
os.makedirs(FIG, exist_ok=True)

from joint_opt import PSI, LAMBDA, h_vec, iv_best_gap_on  # noqa: E402


def fig_crossover():
    p = np.linspace(1e-4, 1 - 1e-4, 600)
    u = 2 * p - p * p
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(p, h_vec(u), label=r"$h(2p-p^2)$  (union coordinate)", lw=2)
    ax.plot(p, h_vec(p), label=r"$h(p)$  (single coordinate)", lw=2)
    ax.axvline(PSI, color="k", ls="--", alpha=0.7,
               label=fr"$\psi=(3-\sqrt5)/2\approx{PSI:.5f}$")
    ax.set_xlabel("marginal $p$")
    ax.set_ylabel("entropy (nats)")
    ax.set_title("Crossover of union vs single-coordinate entropy at $p=\\psi$")
    ax.legend(loc="lower center", fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "crossover.png"), dpi=140)
    plt.close(fig)


def fig_sawin_slack():
    # slack G(p,p) on the diagonal, and a horizontal slice q=0.5.
    def h1(x):
        x = np.clip(x, 1e-12, 1 - 1e-12)
        return -x * np.log(x) - (1 - x) * np.log1p(-x)

    p = np.linspace(1e-3, 1 - 1e-3, 600)
    # diagonal
    ud = 1 - (1 - p) ** 2
    Gd = h1(ud) - LAMBDA * (2 * (1 - p) * h1(p))
    # slice q=0.5
    q = 0.5
    us = 1 - (1 - p) * (1 - q)
    Gs = h1(us) - LAMBDA * ((1 - q) * h1(p) + (1 - p) * h1(q))

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(p, Gd, label=r"$G(p,p)$ (diagonal)", lw=2)
    ax.plot(p, Gs, label=r"$G(p,0.5)$ (slice $q=0.5$)", lw=2)
    ax.axhline(0, color="k", lw=0.8)
    ax.axvline(PSI, color="k", ls="--", alpha=0.7, label=fr"$p=\psi\approx{PSI:.5f}$")
    ax.scatter([PSI], [0], color="red", zorder=5, label="equality point $(\\psi,\\psi)$")
    ax.set_xlabel("$p$")
    ax.set_ylabel(r"$G = h(\mathrm{union}) - \lambda[(1-q)h(p)+(1-p)h(q)]$")
    ax.set_title(r"Sawin inequality slack $G\ge0$ (tight only at $p=q=\psi$)")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "sawin_slack.png"), dpi=140)
    plt.close(fig)


def fig_threshold_vs_U(thresholds: dict[int, float] | None = None):
    if thresholds is None:
        # default: the plateau at psi (all our certified values)
        thresholds = {1: PSI, 2: PSI, 4: PSI, 8: PSI, 16: PSI}
    ks = sorted(thresholds)
    vals = [thresholds[k] for k in ks]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(ks, vals, "o-", lw=2, ms=8, label="certified threshold $c$")
    ax.axhline(PSI, color="k", ls="--", alpha=0.7, label=fr"$\psi\approx{PSI:.5f}$ (sanity floor)")
    ax.axhline(0.38271, color="green", ls=":", alpha=0.8, label="Liu 2024 (numerical, not reproduced)")
    ax.set_xscale("log", base=2)
    ax.set_xticks(ks)
    ax.set_xticklabels([str(k) for k in ks])
    ax.set_xlabel(r"auxiliary cardinality $|U|$")
    ax.set_ylabel("certified constant $c$")
    ax.set_ylim(0.380, 0.384)
    ax.set_title("Certified threshold vs $|U|$ — plateau at $\\psi$\n"
                 "(diagonal conditional-i.i.d. gives no gain; see results.md)")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "threshold_vs_U.png"), dpi=140)
    plt.close(fig)


def fig_feasibility_vs_t(n_grid: int = 40, n_restarts: int = 8):
    ts = np.linspace(0.33, 0.43, 21)
    gaps = []
    for t in ts:
        g, _, _ = iv_best_gap_on(float(t), n_grid=n_grid, n_restarts=n_restarts)
        gaps.append(g)
    gaps = np.array(gaps)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(ts, gaps, "o-", lw=2, label="best feasibility gap of (IV) on $[0,t]$")
    ax.axhline(0, color="k", lw=0.8)
    ax.axvline(PSI, color="k", ls="--", alpha=0.7, label=fr"$\psi\approx{PSI:.5f}$")
    ax.set_xlabel("$t$ (upper bound on support of $\\mu$)")
    ax.set_ylabel(r"$\max_\mu\;[\,E_\mu h(P)-E\,h(\mathrm{union})\,]$")
    ax.set_title("(IV) flips from infeasible to feasible exactly at $t=\\psi$")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "feasibility_vs_t.png"), dpi=140)
    plt.close(fig)


def main():
    print("Generating figures into", FIG)
    fig_crossover()
    print("  crossover.png")
    fig_sawin_slack()
    print("  sawin_slack.png")
    fig_threshold_vs_U()
    print("  threshold_vs_U.png")
    fig_feasibility_vs_t()
    print("  feasibility_vs_t.png")
    print("done.")


if __name__ == "__main__":
    main()
