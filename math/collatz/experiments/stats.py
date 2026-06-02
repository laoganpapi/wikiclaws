"""
Statistical analysis of Collatz stopping times.

Quantities computed:

  tau(n)        — stopping time (steps until trajectory drops below n);
                  E[tau(n)] under the random model is about 1/log_2(4/3) ~ 6.95.
  sigma_inf(n)  — total stopping time (steps until trajectory hits 1);
                  Terras (1976) / Lagarias predict sigma_inf(n) ~ c log n
                  with c = 2 / log_2(4/3) ~ 9.96... in the accelerated map.

  Log-density observable (Tao 2019, arXiv:1909.03562):
      Tao proves that for almost all n (in logarithmic density), Coll_min(n)
      attains "almost bounded" values. The natural normalized observable
      we expose is:
            r(n) := (log T^tau(n)(n) - log n) / log(3/4)
      i.e., the rate at which the trajectory descends, measured in units of
      the "expected" descent rate log(3/4). Under the random model, r(n)
      should concentrate at 1 as n -> infinity. (We use accelerated T; the
      "expected" multiplicative drift per step is sqrt(3)/2 = (3/4)^{1/2},
      so per drop-below-n event the multiplicative ratio averages 3/4.)

Outputs: numeric summaries + PNG plots in `experiments/figures/`.

Author: Alex Ye with Claude.
"""

from __future__ import annotations

import json
import math
import os
import time
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple

import numpy as np

from verifier import (
    total_stopping_time, stopping_time, trajectory,
    _build_small_cache, build_sieve, T,
)

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Bulk computations using cache.
# ---------------------------------------------------------------------------


def compute_stopping_times(N: int) -> np.ndarray:
    """
    Return an ndarray sigma of shape (N+1,) with sigma[n] = sigma_inf(n)
    for n = 0..N. sigma[0] is unused (set to 0).

    Uses the same chained DP as verifier._build_small_cache.
    """
    cache = _build_small_cache(N + 1)
    arr = np.array(cache, dtype=np.int64)
    return arr


def compute_tau(N: int) -> np.ndarray:
    """
    Return an ndarray tau of shape (N+1,) with tau[n] = stopping_time(n)
    for n = 0..N. tau[0], tau[1] = 0.

    We compute directly (cheaper than sigma_inf since trajectories drop
    quickly): for each n, simulate T until the value is < n.
    """
    arr = np.zeros(N + 1, dtype=np.int64)
    for n in range(2, N + 1):
        m = n
        count = 0
        while True:
            if m & 1:
                m = (3 * m + 1) >> 1
            else:
                m >>= 1
            count += 1
            if m < n:
                break
        arr[n] = count
    return arr


# ---------------------------------------------------------------------------
# Anomaly search.
# ---------------------------------------------------------------------------


@dataclass
class Anomaly:
    """Record of an n with the longest stopping time in a range."""
    n: int
    sigma_inf: int
    tau: int
    peak: int                  # max value seen in orbit
    log_ratio: float = 0.0     # sigma_inf / log(n)

    def to_dict(self) -> Dict:
        return asdict(self)


def find_anomalies(start: int, stop: int, k_per_decade: int = 5,
                   sigma_arr: Optional[np.ndarray] = None) -> List[Anomaly]:
    """
    Find the top-k longest-stopping-time integers in [start, stop).

    Subdivides the range into per-decade buckets and reports the longest
    sigma_inf in each bucket — so the result is a "record progression"
    rather than a flat top-k. For each anomaly we also record peak orbit
    height.

    sigma_arr can be precomputed via compute_stopping_times(stop-1).
    """
    if sigma_arr is None:
        sigma_arr = compute_stopping_times(stop - 1)

    # Build per-decade buckets (10^d, 10^{d+1}].
    log_start = max(0, int(math.floor(math.log10(max(start, 1)))))
    log_stop = int(math.floor(math.log10(stop - 1))) + 1
    anomalies: List[Anomaly] = []
    for d in range(log_start, log_stop):
        lo = max(10 ** d, start)
        hi = min(10 ** (d + 1), stop)
        if lo >= hi:
            continue
        sub = sigma_arr[lo:hi]
        if len(sub) == 0:
            continue
        # top-k by sigma
        ks = min(k_per_decade, len(sub))
        top_idx = np.argpartition(-sub, ks - 1)[:ks]
        top_idx_sorted = top_idx[np.argsort(-sub[top_idx])]
        for idx in top_idx_sorted:
            n = int(lo + idx)
            sig = int(sub[idx])
            t = stopping_time(n)
            # Peak: scan the orbit (cheap for moderate n)
            orbit = trajectory(n)
            peak = max(orbit)
            anomalies.append(Anomaly(
                n=n, sigma_inf=sig, tau=t, peak=peak,
                log_ratio=sig / math.log(n) if n > 1 else 0.0,
            ))
    return anomalies


def progressive_records(N: int,
                        sigma_arr: Optional[np.ndarray] = None) -> List[Anomaly]:
    """
    Return all "record-setting" n in [1, N]: n such that sigma_inf(n) is
    strictly larger than sigma_inf(m) for every m < n.
    """
    if sigma_arr is None:
        sigma_arr = compute_stopping_times(N)
    records: List[Anomaly] = []
    cur = -1
    for n in range(1, N + 1):
        sig = int(sigma_arr[n])
        if sig > cur:
            cur = sig
            orbit = trajectory(n)
            records.append(Anomaly(
                n=n, sigma_inf=sig, tau=stopping_time(n),
                peak=max(orbit),
                log_ratio=sig / math.log(n) if n > 1 else 0.0,
            ))
    return records


# ---------------------------------------------------------------------------
# Density / distribution analysis.
# ---------------------------------------------------------------------------


def empirical_tau_distribution(tau_arr: np.ndarray,
                               max_tau: Optional[int] = None
                               ) -> Tuple[np.ndarray, np.ndarray]:
    """
    Histogram of tau(n) values. Returns (bin_centers, counts).
    """
    if max_tau is None:
        max_tau = int(tau_arr[2:].max())
    # n=0,1 excluded
    counts = np.bincount(tau_arr[2:], minlength=max_tau + 1)[: max_tau + 1]
    centers = np.arange(max_tau + 1)
    return centers, counts


def log_descent_observable(N: int,
                           tau_arr: Optional[np.ndarray] = None
                           ) -> np.ndarray:
    """
    For each n in [2, N], compute r(n) = (log T^{tau(n)}(n) - log n) / log(3/4).

    Under the standard heuristic (Terras random model), r(n) is concentrated
    at 1 — each step at random parity gives expected log-ratio
    (1/2) * log(1/2) + (1/2) * log(3/2) = (1/2) log(3/4), so tau(n) ~ const
    and the drop ratio per tau-event averages 3/4.

    Returns an ndarray of length N - 1 (entries for n = 2..N).
    """
    if tau_arr is None:
        tau_arr = compute_tau(N)
    out = np.empty(N - 1, dtype=np.float64)
    denom = math.log(3 / 4)
    for n in range(2, N + 1):
        t = int(tau_arr[n])
        m = n
        for _ in range(t):
            if m & 1:
                m = (3 * m + 1) >> 1
            else:
                m >>= 1
        out[n - 2] = (math.log(m) - math.log(n)) / denom
    return out


def stopping_time_log_regression(N: int,
                                 sigma_arr: Optional[np.ndarray] = None
                                 ) -> Tuple[float, float, float]:
    """
    Linear regression sigma_inf(n) ~ a + b * log(n) over n in [2, N].

    Theoretical slope (heuristic, accelerated map): b = 2 / log_2(4/3)
        = 2 / log(4/3) * log(2) ~ 4.819...
    Wait — the right slope under the random-walk heuristic for the
    accelerated map T is:
        E[log T(n)/n | parity] = (1/2) [log(1/2) + log(3/2)]
                               = (1/2) log(3/4)
    So per step the log decreases by (1/2) |log(3/4)| ~ 0.1438.
    Hence sigma_inf(n) ~ log(n) / (0.1438...) = log(n) * 2 / log(4/3)
                       ~ log(n) * 6.952...
    (This is the natural-log slope; log_2 slope would be ~ 4.819.)

    Returns (intercept, slope_natural_log, R^2).
    """
    if sigma_arr is None:
        sigma_arr = compute_stopping_times(N)
    ns = np.arange(2, N + 1)
    sigmas = sigma_arr[2: N + 1].astype(np.float64)
    logs = np.log(ns.astype(np.float64))
    # Standard OLS
    m = logs.mean()
    s = sigmas.mean()
    slope = ((logs - m) * (sigmas - s)).sum() / ((logs - m) ** 2).sum()
    intercept = s - slope * m
    pred = intercept + slope * logs
    ss_res = ((sigmas - pred) ** 2).sum()
    ss_tot = ((sigmas - s) ** 2).sum()
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return float(intercept), float(slope), float(r2)


# ---------------------------------------------------------------------------
# Plots.
# ---------------------------------------------------------------------------


def plot_tau_histogram(tau_arr: np.ndarray, title: str,
                       filename: str) -> str:
    """
    Histogram of stopping time tau. Save PNG. Return filepath.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    centers, counts = empirical_tau_distribution(tau_arr)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(centers, counts, width=0.95, edgecolor="black", linewidth=0.3)
    ax.set_xlabel(r"$\tau(n)$ (stopping time, accelerated map)")
    ax.set_ylabel("count")
    ax.set_title(title)
    ax.set_yscale("log")
    path = os.path.join(FIG_DIR, filename)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path


def plot_sigma_vs_log_n(sigma_arr: np.ndarray, title: str,
                        filename: str, sample: int = 50000) -> str:
    """
    Scatter sigma_inf(n) vs log(n), with theoretical slope overlay.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    N = len(sigma_arr) - 1
    ns = np.arange(2, N + 1)
    if N - 1 > sample:
        idx = np.random.default_rng(42).choice(N - 1, sample, replace=False)
        ns = ns[idx]
    sigmas = sigma_arr[ns]
    logs = np.log(ns.astype(np.float64))

    # Theoretical line
    theo_slope = 2.0 / math.log(4 / 3)  # ~6.952
    intercept, slope, r2 = stopping_time_log_regression(N, sigma_arr)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(logs, sigmas, s=2, alpha=0.25, label="data")
    xs = np.linspace(logs.min(), logs.max(), 200)
    ax.plot(xs, intercept + slope * xs, color="red",
            label=f"OLS: slope = {slope:.3f} (R^2={r2:.4f})")
    ax.plot(xs, theo_slope * xs, color="green", linestyle="--",
            label=f"Heuristic slope 2/log(4/3) = {theo_slope:.3f}")
    ax.set_xlabel(r"$\log n$")
    ax.set_ylabel(r"$\sigma_\infty(n)$")
    ax.set_title(title)
    ax.legend()
    path = os.path.join(FIG_DIR, filename)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path


def plot_log_descent_observable(rvals: np.ndarray, title: str,
                                filename: str, bins: int = 200) -> str:
    """
    Histogram of r(n) = (log T^tau(n)(n) - log n) / log(3/4).
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Restrict to a sensible range (handles outliers)
    finite = rvals[np.isfinite(rvals)]
    lo, hi = np.percentile(finite, [0.5, 99.5])
    finite = finite[(finite >= lo) & (finite <= hi)]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(finite, bins=bins, edgecolor="black", linewidth=0.2)
    ax.axvline(1.0, color="red", linestyle="--",
               label="heuristic concentration value r = 1")
    ax.set_xlabel(r"$r(n) = (\log T^{\tau(n)}(n) - \log n)/\log(3/4)$")
    ax.set_ylabel("count")
    ax.set_title(title)
    ax.legend()
    path = os.path.join(FIG_DIR, filename)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# Pipeline runner.
# ---------------------------------------------------------------------------


def run_full_stats(N: int, prefix: str = "baseline",
                   verbose: bool = True) -> Dict:
    """
    Compute and emit the standard stats package for n in [1, N].

    Returns a dict ready to be JSON-dumped.
    """
    log = (lambda *a, **kw: print(*a, **kw)) if verbose else (lambda *a, **kw: None)

    timings: Dict[str, float] = {}

    t = time.perf_counter()
    log(f"[stats] computing sigma_inf for n in [1, {N}] ...")
    sigma_arr = compute_stopping_times(N)
    timings["sigma_inf"] = time.perf_counter() - t
    log(f"  done in {timings['sigma_inf']:.2f}s")

    t = time.perf_counter()
    log(f"[stats] computing tau for n in [1, {N}] ...")
    tau_arr = compute_tau(N)
    timings["tau"] = time.perf_counter() - t
    log(f"  done in {timings['tau']:.2f}s")

    t = time.perf_counter()
    log(f"[stats] computing log-descent observable ...")
    rvals = log_descent_observable(N, tau_arr)
    timings["log_descent"] = time.perf_counter() - t
    log(f"  done in {timings['log_descent']:.2f}s")

    t = time.perf_counter()
    log(f"[stats] regression sigma_inf ~ log(n) ...")
    intercept, slope, r2 = stopping_time_log_regression(N, sigma_arr)
    timings["regression"] = time.perf_counter() - t
    log(f"  intercept={intercept:.3f} slope={slope:.4f} R^2={r2:.5f}"
        f"  (heuristic slope = {2/math.log(4/3):.4f})")

    t = time.perf_counter()
    log(f"[stats] anomaly search (per-decade top-5) ...")
    anomalies = find_anomalies(1, N + 1, k_per_decade=5, sigma_arr=sigma_arr)
    timings["anomalies"] = time.perf_counter() - t
    log(f"  found {len(anomalies)} anomalies in {timings['anomalies']:.2f}s")

    t = time.perf_counter()
    log(f"[stats] progressive records ...")
    records = progressive_records(N, sigma_arr=sigma_arr)
    timings["records"] = time.perf_counter() - t
    log(f"  {len(records)} records up to n = {N} (in {timings['records']:.2f}s)")

    log(f"[stats] generating plots ...")
    tau_path = plot_tau_histogram(
        tau_arr,
        f"Distribution of stopping time tau(n) for n in [1, {N}]",
        f"{prefix}_tau_histogram.png",
    )
    sigma_path = plot_sigma_vs_log_n(
        sigma_arr,
        f"sigma_inf(n) vs log n for n in [1, {N}]",
        f"{prefix}_sigma_vs_logn.png",
    )
    desc_path = plot_log_descent_observable(
        rvals,
        f"Log-descent observable r(n) for n in [2, {N}]",
        f"{prefix}_log_descent.png",
    )
    log(f"  saved {tau_path}")
    log(f"  saved {sigma_path}")
    log(f"  saved {desc_path}")

    # Summary statistics
    sigma_view = sigma_arr[1:]
    tau_view = tau_arr[2:]
    finite_r = rvals[np.isfinite(rvals)]

    summary = {
        "N": N,
        "max_sigma_inf": int(sigma_view.max()),
        "argmax_sigma_inf": int(sigma_view.argmax()) + 1,
        "mean_sigma_inf": float(sigma_view.mean()),
        "median_sigma_inf": float(np.median(sigma_view)),
        "regression": {
            "intercept": intercept,
            "slope_natural_log": slope,
            "R_squared": r2,
            "heuristic_slope": 2 / math.log(4 / 3),
        },
        "tau": {
            "max": int(tau_view.max()),
            "argmax_n": int(tau_view.argmax()) + 2,
            "mean": float(tau_view.mean()),
            "median": float(np.median(tau_view)),
            "heuristic_mean": 1.0 / (math.log(2) - 0.5 * math.log(3)),
        },
        "log_descent_observable": {
            "mean_r": float(finite_r.mean()),
            "median_r": float(np.median(finite_r)),
            "std_r": float(finite_r.std()),
            "heuristic_value": 1.0,
        },
        "anomalies_per_decade": [a.to_dict() for a in anomalies],
        "progressive_records": [a.to_dict() for a in records],
        "figures": {
            "tau_histogram": tau_path,
            "sigma_vs_logn": sigma_path,
            "log_descent": desc_path,
        },
        "timing_seconds": timings,
    }
    return summary


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------


def _cli() -> None:
    import argparse
    p = argparse.ArgumentParser(description="Collatz statistics.")
    p.add_argument("--N", type=int, default=10**6,
                   help="Upper bound (default 10^6).")
    p.add_argument("--prefix", default="baseline")
    p.add_argument("--json", default=None,
                   help="Path to write JSON summary.")
    args = p.parse_args()
    summary = run_full_stats(args.N, prefix=args.prefix)
    if args.json:
        with open(args.json, "w") as f:
            json.dump(summary, f, indent=2)
        print(f"Wrote {args.json}")


if __name__ == "__main__":
    _cli()
