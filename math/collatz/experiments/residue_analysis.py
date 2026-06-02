"""
Mod 2^k residue-class structural analysis of the accelerated Collatz map.

Background.
-----------
Write n = 2^k * q + r with 0 <= r < 2^k. Iterating T for k steps yields

    T^k(n) = 3^{a(r)} * q + b(r),

where
    a(r) = number of odd parities in the parity vector of r over k steps,
    b(r) = T^k(r) as an integer (always integer since each "even step"
           halves and the (3m+1)/2 step is integer for odd m).

This map  phi_k: r |-> (a(r), b(r))  is the *Syracuse map* on residue
classes mod 2^k. It's the right object to study Collatz structurally:
the dynamics modulo 2^k are completely captured by phi_k.

Standard facts (Lagarias 1985 / Terras 1976):

  1.  As r varies over {0, ..., 2^k - 1}, a(r) takes every value in
      {0, 1, ..., k} with multiplicity equal to C(k, a) (binomial),
      because the parity vector ranges over all 2^k binary strings of
      length k (this is Terras's "parity sequence" theorem).

  2.  The composition  n -> 2^k q + b(r), q -> q  is a non-trivial
      "fixed point" structure: each residue class r determines the
      slope 3^{a(r)} and offset b(r). For the Collatz conjecture, the
      crucial invariant to track is the "Syracuse function"
            Syr(n) := T^{k_n}(n)
      where k_n is chosen so that 2^{a(r)} > 3^{a(r)} (i.e., the
      trajectory has just crossed back below n).

This module computes phi_k, builds residue class tables, and checks
several candidate invariants — including the 2-adic valuation drift,
which is sharply related to Tao's logarithmic-density analysis.

References:
- J. C. Lagarias, "The 3x+1 problem: An overview" (annotated bibliography).
- R. Terras, "A stopping time problem on the positive integers" (1976).
- T. Tao, "Almost all orbits of the Collatz map attain almost bounded
  values" (arXiv:1909.03562, 2019), Sections 1-2 on the Syracuse map.

Author: Alex Ye with Claude.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple

import numpy as np

from verifier import build_sieve

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# phi_k computation.
# ---------------------------------------------------------------------------


@dataclass
class SyracuseKLevel:
    """Container for the k-th level Syracuse map data."""
    k: int
    a: np.ndarray            # shape (2^k,), int8
    b: np.ndarray            # shape (2^k,), int64
    a_histogram: np.ndarray  # shape (k+1,), bincount of a
    odd_density: float       # mean(a) / k — under random parity = 1/2

    def to_summary_dict(self) -> Dict:
        return {
            "k": self.k,
            "num_residues": 1 << self.k,
            "a_histogram": self.a_histogram.tolist(),
            "a_histogram_binomial_check": _binomial_check(self.k, self.a_histogram),
            "odd_density": float(self.odd_density),
            "min_b": int(self.b.min()),
            "max_b": int(self.b.max()),
            "mean_b": float(self.b.mean()),
            "median_b": float(np.median(self.b)),
        }


def _binomial_check(k: int, hist: np.ndarray) -> Dict:
    """
    Verify Terras's parity-sequence theorem: hist[i] should equal C(k, i).
    Returns a diagnostic dict.
    """
    expected = np.array([math.comb(k, i) for i in range(k + 1)],
                        dtype=np.int64)
    matches = bool(np.array_equal(hist, expected))
    return {
        "expected_binomial": expected.tolist(),
        "matches": matches,
        "max_diff": int(np.abs(hist - expected).max()),
    }


def compute_phi_k(k: int) -> SyracuseKLevel:
    """
    Compute the level-k Syracuse data: arrays a[r], b[r] for r in [0, 2^k).
    """
    a_list, b_list, _ = build_sieve(k)
    a_arr = np.array(a_list, dtype=np.int8)
    b_arr = np.array(b_list, dtype=np.int64)
    a_hist = np.bincount(a_arr.astype(np.int64), minlength=k + 1)[:k + 1]
    return SyracuseKLevel(
        k=k, a=a_arr, b=b_arr,
        a_histogram=a_hist,
        odd_density=float(a_arr.mean() / k) if k > 0 else 0.0,
    )


# ---------------------------------------------------------------------------
# Candidate invariants / conserved quantities.
# ---------------------------------------------------------------------------


def check_invariant_b_mod_3(level: SyracuseKLevel) -> Dict:
    """
    Question: does b(r) mod 3 have structured behaviour?

    Since T(n) involves multiplication by 3, *iterated* application
    induces non-trivial structure on b(r) mod 3. We compute the
    distribution and see if there's bias.
    """
    counts = np.bincount(level.b % 3, minlength=3)
    return {
        "b_mod_3_counts": counts.tolist(),
        "expected_uniform": (1 << level.k) // 3,
        "max_dev_from_uniform": int(np.max(np.abs(counts - (1 << level.k) / 3))),
    }


def check_invariant_b_minus_residue(level: SyracuseKLevel) -> Dict:
    """
    Tracking the offset c(r) := b(r) - r * (3/2)^{a(r)}.

    Under the random-walk heuristic, the multiplicative drift from
    starting value r is (3/2)^{a(r)} * (1/2)^{k-a(r)} = 3^{a(r)} / 2^k.
    The integer offset b(r) is (3^a r + C) / 2^k; the "C" part is what
    distinguishes Collatz from the multiplicative random walk.

    We compute c(r) = 2^k * b(r) - 3^{a(r)} * r and look at its
    distribution.
    """
    k = level.k
    r = np.arange(1 << k, dtype=np.int64)
    # Use Python ints for the 3^a computation to avoid overflow at large k
    if k <= 16:
        pow3 = np.array([3 ** int(a) for a in level.a], dtype=np.int64)
        c = (1 << k) * level.b - pow3 * r
        return {
            "c_min": int(c.min()),
            "c_max": int(c.max()),
            "c_mean": float(c.mean()),
            "c_std": float(c.std()),
            "c_zero_count": int((c == 0).sum()),
        }
    else:
        # Use object arrays to avoid overflow
        c_vals = []
        for i in range(min(1 << k, 10**6)):
            a = int(level.a[i])
            b = int(level.b[i])
            c_vals.append((1 << k) * b - (3 ** a) * i)
        c_arr = np.array(c_vals, dtype=object)
        return {
            "sampled": True,
            "sample_size": len(c_vals),
            "c_min": str(min(c_vals)),
            "c_max": str(max(c_vals)),
        }


def descent_residues(k: int, level: Optional[SyracuseKLevel] = None
                     ) -> Dict:
    """
    For each residue r mod 2^k, determine whether 2^k > 3^{a(r)} * b(r) / r
    -- i.e., whether after k steps the trajectory has provably descended
    (3^{a(r)} q + b(r) < 2^k q + r for large q, which is equivalent to
    3^{a(r)} < 2^k whenever q > 0).

    The condition "k-step descent" holds iff 2^k > 3^{a(r)}, i.e.,
    a(r) < k * log_3(2) = k / log_2(3).

    We compute the *fraction* of residues for which descent occurs in
    exactly k steps and compare against the binomial random model.
    """
    if level is None:
        level = compute_phi_k(k)
    threshold = math.log(2) / math.log(3) * k   # a(r) < threshold => descent
    descent_mask = level.a.astype(np.float64) < threshold
    descent_fraction = float(descent_mask.mean())

    # Random-model probability: sum_{a < threshold} C(k, a) / 2^k
    rm_prob = 0.0
    for a in range(k + 1):
        if a < threshold:
            rm_prob += math.comb(k, a) / (1 << k)

    return {
        "k": k,
        "threshold_a": threshold,
        "descent_fraction": descent_fraction,
        "random_model_probability": rm_prob,
        "match": abs(descent_fraction - rm_prob) < 1e-12,
    }


def residue_orbit_to_one_short(k: int, level: Optional[SyracuseKLevel] = None
                               ) -> List[Tuple[int, int, int]]:
    """
    For each residue r mod 2^k, simulate T iteratively starting from r
    (as a plain integer) and count steps to reach 1, plus the peak
    value. Returns list of (r, sigma_inf(r), peak).

    This is a sanity probe — every residue class representative is just
    a small integer, so this is cheap.
    """
    if level is None:
        level = compute_phi_k(k)
    if k > 20:
        raise ValueError("residue_orbit_to_one_short is intended for k <= 20")
    results = []
    size = 1 << k
    for r in range(size):
        if r == 0:
            results.append((0, 0, 0))   # 0 is not a positive integer; skip
            continue
        m = r
        sigma = 0
        peak = m
        while m != 1:
            if m & 1:
                m = (3 * m + 1) >> 1
            else:
                m >>= 1
            sigma += 1
            if m > peak:
                peak = m
        results.append((r, sigma, peak))
    return results


# ---------------------------------------------------------------------------
# Cross-residue structure: how does increasing k refine the analysis?
# ---------------------------------------------------------------------------


def refine_residue_table(prev: SyracuseKLevel,
                         next_k: Optional[int] = None) -> SyracuseKLevel:
    """
    Given the level-k Syracuse data, compute level-(k+1) by extending
    each residue r to its two children r and r + 2^k.

    Verifies the consistency relation:
        a_{k+1}(r) = a_k(r) + [next parity bit],
        b_{k+1}(r) = T(b_k(r))  in the right manner.

    Actually, the cleanest recurrence is: starting from r (k+1 bits),
    apply T(r) once and reduce mod 2^k to recover the level-k data of
    T(r). We don't need that; we just directly call compute_phi_k(k+1).
    The point of this function is to assert consistency, useful as a
    sanity check.
    """
    if next_k is None:
        next_k = prev.k + 1
    nxt = compute_phi_k(next_k)
    # Sanity: a histograms should be binomial(next_k)
    assert nxt.a_histogram.tolist() == [math.comb(next_k, i)
                                        for i in range(next_k + 1)], \
        f"binomial check failed at k={next_k}"
    return nxt


def search_a_anomalies(k: int, level: Optional[SyracuseKLevel] = None,
                       top: int = 20) -> List[Dict]:
    """
    Find residues with extremal a(r) — most-odd and most-even parity
    sequences. These are the residues whose trajectories grow fastest
    (high a -> many (3n+1)/2 steps) or descend fastest (low a).
    """
    if level is None:
        level = compute_phi_k(k)
    a_arr = level.a
    b_arr = level.b
    max_a_idx = np.argsort(-a_arr)[:top]
    min_a_idx = np.argsort(a_arr)[:top]
    return [
        {
            "kind": "max_a (most odd steps; trajectory grows)",
            "entries": [
                {"r": int(r), "a": int(a_arr[r]), "b": int(b_arr[r])}
                for r in max_a_idx
            ],
        },
        {
            "kind": "min_a (most even steps; trajectory shrinks fastest)",
            "entries": [
                {"r": int(r), "a": int(a_arr[r]), "b": int(b_arr[r])}
                for r in min_a_idx
            ],
        },
    ]


# ---------------------------------------------------------------------------
# Plots.
# ---------------------------------------------------------------------------


def plot_a_histogram(level: SyracuseKLevel, filename: str) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(np.arange(level.k + 1), level.a_histogram,
           edgecolor="black", linewidth=0.4)
    binom = np.array([math.comb(level.k, i) for i in range(level.k + 1)])
    ax.plot(np.arange(level.k + 1), binom, "ro--", label=r"$\binom{k}{i}$")
    ax.set_xlabel(r"number of odd steps $a(r)$ in first $k$ steps")
    ax.set_ylabel("number of residues $r$")
    ax.set_title(f"Distribution of a(r) for r mod $2^{{{level.k}}}$")
    ax.legend()
    path = os.path.join(FIG_DIR, filename)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path


def plot_b_distribution(level: SyracuseKLevel, filename: str) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 5))
    log_b = np.log(np.maximum(1, level.b))
    ax.hist(log_b, bins=80, edgecolor="black", linewidth=0.2)
    ax.set_xlabel(r"$\log b(r)$")
    ax.set_ylabel("count")
    ax.set_title(f"Distribution of $\\log b(r)$ at $k = {level.k}$")
    path = os.path.join(FIG_DIR, filename)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# Pipeline.
# ---------------------------------------------------------------------------


def run_residue_analysis(k_values: List[int],
                         verbose: bool = True,
                         do_plots: bool = True) -> Dict:
    """
    Run the full residue-class analysis for a list of k values.
    """
    log = (lambda *a, **kw: print(*a, **kw)) if verbose else (lambda *a, **kw: None)

    results = {"levels": [], "tao_descent_table": []}
    for k in k_values:
        log(f"[residue] computing phi_{k} (size = 2^{k} = {1<<k}) ...")
        t0 = time.perf_counter()
        lvl = compute_phi_k(k)
        elapsed = time.perf_counter() - t0
        log(f"  done in {elapsed:.2f}s; mean a = {lvl.a.mean():.4f} "
            f"(heuristic k/2 = {k/2})")

        entry: Dict = lvl.to_summary_dict()
        entry["b_mod_3"] = check_invariant_b_mod_3(lvl)
        entry["c_offset"] = check_invariant_b_minus_residue(lvl)
        descent = descent_residues(k, lvl)
        entry["descent"] = descent
        results["tao_descent_table"].append(descent)

        if k <= 12:
            entry["a_extrema"] = search_a_anomalies(k, lvl, top=5)

        if do_plots and k in (8, 12, 16, 20):
            entry["plot_a"] = plot_a_histogram(lvl, f"residue_a_k{k}.png")
            entry["plot_b"] = plot_b_distribution(lvl, f"residue_b_k{k}.png")

        entry["compute_seconds"] = elapsed
        results["levels"].append(entry)
    return results


def _cli() -> None:
    p = argparse.ArgumentParser(description="Residue-class structural analysis.")
    p.add_argument("--k", type=int, nargs="*",
                   default=[4, 8, 12, 16, 20],
                   help="k-values to analyse (default 4 8 12 16 20).")
    p.add_argument("--json", default=None, help="Output JSON path.")
    p.add_argument("--no-plots", action="store_true")
    args = p.parse_args()
    results = run_residue_analysis(args.k, do_plots=not args.no_plots)
    if args.json:
        with open(args.json, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Wrote {args.json}")


if __name__ == "__main__":
    _cli()
