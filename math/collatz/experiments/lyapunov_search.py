"""
Lyapunov candidate search for the accelerated Collatz map T.

We test whether various functions L : N -> R can serve as Lyapunov functions
for T -- i.e., whether L(T(n)) <= L(n) holds always / almost always / on
average. The aim is NOT to find a true Lyapunov function (none can exist
unless Collatz is proved), but to *quantify the obstruction*: for each
candidate L in an explicit family, measure E[L(T(n)) - L(n)] empirically
and (where possible) under the Tao/Lagarias-Weiss random parity model.

Candidate families (binary-structure, NOT 2-adic norm):

  s(n)   = Hamming weight (popcount): number of 1-bits of n.
  r(n)   = run-count: number of maximal binary runs of n
           (each maximal block of equal bits counts once).
  c(n)   = carry count: number of carries when n is added to (n-1)/2 in
           binary, for n odd. (For odd n, computing (3n+1)/2 in binary
           amounts to n + (n+1)/2 -- one addition. The number of carries
           is the Kummer-theorem-style observable. For even n we declare
           c(n) := 0 because the n/2 step is a free shift.)
  log2n  = floor(log_2 n) -- this is the *non*-binary-structural "size"
           coordinate, used as a control / linear combinator.

Hybrid candidates: L_{alpha,beta}(n) = alpha * X(n) + beta * log2(n), where
X is one of s, r, c. We sweep (alpha, beta) over a fine grid and measure:

   drift_mean    = mean over starting n in [N0, N0+M) of L(T(n)) - L(n)
   drift_step    = mean over orbit steps in {(m, T(m)) : m visited from
                   trajectories of n in [N0, N0+M)} of L(T(m)) - L(m)
                   (this is the *Birkhoff* drift along trajectories,
                   which is what a true Lyapunov bound has to control)
   prob_decrease = empirical P[L(T(n)) <= L(n)] (on trajectory steps)
   strict_dec    = empirical P[L(T(n)) <  L(n)] (on trajectory steps)
   max_increase  = max observed L(T(n)) - L(n)  over orbit steps
   counterex_ct  = number of orbit steps with L(T(n)) > L(n)

If any (alpha, beta) gives drift_step <= 0 AND prob_decrease very close to 1
AND counterex_ct = 0 over the 10^7-trajectory dataset, that would be a
candidate -- but Collatz being open means it must fail somewhere (or there
must be a subtle bug). We flag such candidates as PENDING RED-TEAM rather
than success.

We also separately compute the random-parity-model expected drift:
  Under the Tao/Lagarias-Weiss random model, the parity at each step is
  i.i.d. uniform on {0, 1}. We compute E[L(T(n)) - L(n) | parity(n) = b]
  by averaging over a *batch* of n with given parity (this is the right
  conditional expectation; the random model in this codebase is on the
  parity sequence, not on n itself, which is fixed by the start).

Author: Alex Ye with Claude. NOVELTY: this is a digit-structure Lyapunov
search; prior literature has tested s(n) as a Lyapunov directly (see
Lagarias's survey, where it is noted that s(n) does not decrease) but a
systematic (alpha, beta) sweep with quantified drift is, to the best of
our knowledge, not in the literature. [NOVELTY UNVERIFIED -- check next
session.]
"""

from __future__ import annotations

import json
import math
import os
import time
from dataclasses import dataclass, asdict
from typing import Callable, Dict, List, Tuple, Optional

# Import T from the in-tree verifier
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verifier import T  # type: ignore

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Statistics on n.
# ---------------------------------------------------------------------------


def hamming_weight(n: int) -> int:
    """s(n): number of 1-bits of n. Uses int.bit_count() (Py 3.10+)."""
    return n.bit_count()


def run_count(n: int) -> int:
    """
    r(n): number of maximal binary runs of n.

    Examples:
      r(0b10110)  = 4   (1, 0, 11, 0)
      r(0b11111)  = 1
      r(0b101010) = 6
      r(1)        = 1
      r(0)        = 0 by convention.

    Implementation: XOR n with (n >> 1), shift-extract the high bit, and
    count the 1-bits + 1 (each transition gives a new run).
    """
    if n == 0:
        return 0
    if n < 0:
        raise ValueError("run_count requires n >= 0")
    transitions = n ^ (n >> 1)
    # The high bit of transitions encodes the boundary between the
    # leading run and "nothing above"; we count it normally because that
    # is the boundary at the top end of the run pattern.
    # Number of runs = number of bit-flips going from bit 0 upward + 1
    # if the integer is nonzero. The XOR trick gives a bit-flip pattern
    # whose 1-count = number_of_runs (each run ends with one 1 in the
    # transitions pattern, including the topmost).
    return transitions.bit_count()


def carry_count(n: int) -> int:
    """
    c(n): number of carries in the binary addition n + (n+1)/2  (for n odd).
    For n even, returns 0 (the n/2 step is a free shift -- no carries).

    Rationale: for n odd, T(n) = (3n+1)/2. Now 3n+1 = n + n + (n+1), but
    a cleaner formulation: T(n) = (n + (n+1)/2) when n is odd, since
    n + (n+1)/2 = (2n + n + 1)/2 = (3n+1)/2. So T(n) for n odd is the
    sum of n and (n+1)/2 in binary, and the number of carries in this
    addition equals the # of positions where the bit-sum overflows.

    By Kummer's theorem, the number of carries when adding a + b in base
    p equals nu_p( binomial(a+b, a) ). So c(n) is a quantity with a
    classical interpretation.

    Implementation: count_carries(a, b) = popcount(a) + popcount(b) -
    popcount(a + b). This is the standard identity for base-2 carries.
    """
    if n & 1 == 0:
        return 0
    a = n
    b = (n + 1) >> 1
    return a.bit_count() + b.bit_count() - (a + b).bit_count()


def log2_floor(n: int) -> int:
    """floor(log_2 n) -- the standard bit-length proxy. log2_floor(1) = 0."""
    if n < 1:
        raise ValueError("log2_floor requires n >= 1")
    return n.bit_length() - 1


def log2_real(n: int) -> float:
    """Real log_2 n, which is the actual size coordinate used in L_{a,b}."""
    if n < 1:
        raise ValueError("log2_real requires n >= 1")
    return math.log2(n)


# ---------------------------------------------------------------------------
# Per-step drifts.
# ---------------------------------------------------------------------------


def step_drift(stat: Callable[[int], int], n: int) -> Tuple[int, int, int]:
    """
    For statistic stat(.) returning an int, return (stat(n), stat(T(n)),
    stat(T(n)) - stat(n)).
    """
    sn = stat(n)
    tn = T(n)
    st = stat(tn)
    return sn, st, st - sn


def step_drift_hybrid(stat: Callable[[int], int],
                      alpha: float, beta: float,
                      n: int) -> Tuple[float, float, float]:
    """
    L_{alpha,beta}(n) = alpha * stat(n) + beta * log2(n).
    Return (L(n), L(T(n)), L(T(n)) - L(n)). T(n) is computed once.

    log2(n) is taken as a real number (math.log2). For n = 1, log2(1) = 0,
    which is the right value; T(1) = 2, so the log2 contribution flips
    1 -> 2 with delta = 1. Not pathological.
    """
    if n < 1:
        raise ValueError("step_drift_hybrid requires n >= 1")
    sn = stat(n)
    tn = T(n)
    st = stat(tn)
    log_n = math.log2(n) if n > 1 else 0.0
    log_t = math.log2(tn) if tn > 1 else 0.0
    Ln = alpha * sn + beta * log_n
    Lt = alpha * st + beta * log_t
    return Ln, Lt, Lt - Ln


# ---------------------------------------------------------------------------
# Bulk trajectory sweep.
# ---------------------------------------------------------------------------


@dataclass
class DriftStats:
    """Summary statistics on one (statistic, parity) drift distribution."""
    n_samples: int
    mean: float
    var: float                  # sample variance (unbiased)
    stderr: float               # standard error of the mean
    p_decrease: float           # P(delta <= 0)
    p_strict_dec: float         # P(delta < 0)
    p_zero: float               # P(delta == 0)
    max_increase: float
    max_decrease: float

    def asdict(self) -> Dict:
        return asdict(self)


def _np_summarize(arr) -> Dict:
    """Fast numpy summary returning a JSON-ready dict."""
    import numpy as _np
    n = arr.shape[0]
    if n == 0:
        return DriftStats(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0).asdict()
    mean = float(arr.mean())
    if n > 1:
        var = float(arr.var(ddof=1))
        stderr = math.sqrt(var / n)
    else:
        var = 0.0
        stderr = 0.0
    dec = int(_np.count_nonzero(arr <= 0))
    sdec = int(_np.count_nonzero(arr < 0))
    zeros = int(_np.count_nonzero(arr == 0))
    return DriftStats(
        n_samples=int(n),
        mean=mean,
        var=var,
        stderr=stderr,
        p_decrease=dec / n,
        p_strict_dec=sdec / n,
        p_zero=zeros / n,
        max_increase=float(arr.max()),
        max_decrease=float(arr.min()),
    ).asdict()


def summarize(deltas: List[float]) -> DriftStats:
    """Standard summary stats with proper unbiased variance."""
    n = len(deltas)
    if n == 0:
        return DriftStats(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    mean = sum(deltas) / n
    if n > 1:
        var = sum((d - mean) ** 2 for d in deltas) / (n - 1)
        stderr = math.sqrt(var / n)
    else:
        var = 0.0
        stderr = 0.0
    decreases = sum(1 for d in deltas if d <= 0)
    strict_dec = sum(1 for d in deltas if d < 0)
    zeros = sum(1 for d in deltas if d == 0)
    return DriftStats(
        n_samples=n,
        mean=mean,
        var=var,
        stderr=stderr,
        p_decrease=decreases / n,
        p_strict_dec=strict_dec / n,
        p_zero=zeros / n,
        max_increase=max(deltas),
        max_decrease=min(deltas),
    )


def trajectory_drifts(
    n_start: int,
    n_end: int,
    stat: Callable[[int], int],
    max_steps_per_traj: int = 4000,
) -> Tuple[List[float], List[float], List[float]]:
    """
    For each n in [n_start, n_end), simulate the full Collatz trajectory
    (down to 1) and record:

      single_drifts:  L(T(n)) - L(n) for each starting n     -- length M
      odd_drifts:     L(T(m)) - L(m) for each ODD m visited  -- in-trajectory
      even_drifts:    L(T(m)) - L(m) for each EVEN m > 1 visited

    Only the bare statistic (no log component) is recorded here -- the
    hybrid drift L_{alpha,beta} can be computed from these plus log2 drifts
    in a post-processing pass; we record log2 drifts separately for that.

    Returns (single_drifts, odd_drifts, even_drifts).

    All drifts are floats so the consumer can mix in log2 terms.
    """
    single_drifts: List[float] = []
    odd_drifts: List[float] = []
    even_drifts: List[float] = []
    for n in range(n_start, n_end):
        if n < 2:
            continue
        sn, tn, d = step_drift(stat, n)
        single_drifts.append(float(d))
        m = n
        for _ in range(max_steps_per_traj):
            if m <= 1:
                break
            sm = stat(m)
            tm = T(m)
            sm2 = stat(tm)
            dd = float(sm2 - sm)
            if m & 1:
                odd_drifts.append(dd)
            else:
                even_drifts.append(dd)
            m = tm
    return single_drifts, odd_drifts, even_drifts


def trajectory_log_drifts(
    n_start: int,
    n_end: int,
    max_steps_per_traj: int = 4000,
) -> Tuple[List[float], List[float]]:
    """
    Same sweep but recording log2 drifts (real), separated odd vs even.
    Combined with the statistic drifts this gives the hybrid drift for any
    (alpha, beta).
    """
    odd_logs: List[float] = []
    even_logs: List[float] = []
    for n in range(n_start, n_end):
        if n < 2:
            continue
        m = n
        for _ in range(max_steps_per_traj):
            if m <= 1:
                break
            tm = T(m)
            ln_m = math.log2(m) if m > 1 else 0.0
            ln_t = math.log2(tm) if tm > 1 else 0.0
            d = ln_t - ln_m
            if m & 1:
                odd_logs.append(d)
            else:
                even_logs.append(d)
            m = tm
    return odd_logs, even_logs


# ---------------------------------------------------------------------------
# Sweep harness.
# ---------------------------------------------------------------------------


def sweep_candidates(
    n_start: int,
    n_end: int,
    stats: Dict[str, Callable[[int], int]],
    alphas: List[float],
    betas: List[float],
    max_steps_per_traj: int = 4000,
) -> Dict:
    """
    Run the trajectory sweep once per statistic (and once for log2), then
    for each (alpha, beta) in the cross-product compute the combined drift.

    Returns a JSON-serializable dict:

      {
        "n_start": ..., "n_end": ...,
        "stats": [name, ...],
        "alphas": [...], "betas": [...],
        "per_stat": {
            name: {
                "single": DriftStats,
                "odd": DriftStats,
                "even": DriftStats,
                "all_steps": DriftStats,
            },
            ...
        },
        "log2": { "odd": DriftStats, "even": DriftStats, "all_steps": DriftStats },
        "hybrid": [
            { "stat": name, "alpha": ..., "beta": ...,
              "odd": DriftStats, "even": DriftStats, "all_steps": DriftStats },
            ...
        ],
        "timing": { "n_traj": M, "n_odd_steps": ..., "n_even_steps": ..., "secs": ... }
      }

    The hybrid drifts are recovered by zipping the per-step lists of stat
    delta with the per-step log2 delta -- this requires consistent ordering,
    so we use a single shared sweep that emits both kinds at once.
    """
    per_stat_steps: Dict[str, Tuple[List[float], List[float]]] = {}
    log_odd: List[float] = []
    log_even: List[float] = []
    single_stat: Dict[str, List[float]] = {name: [] for name in stats}
    single_log: List[float] = []

    t0 = time.perf_counter()
    for name in stats:
        per_stat_steps[name] = ([], [])  # (odd, even)

    for n in range(max(n_start, 2), n_end):
        # Record single-step (initial) drifts for each statistic
        m = n
        tm = T(m)
        ln_m = math.log2(m) if m > 1 else 0.0
        ln_t = math.log2(tm) if tm > 1 else 0.0
        single_log.append(ln_t - ln_m)
        for name, fn in stats.items():
            single_stat[name].append(float(fn(tm) - fn(m)))

        # Trajectory
        m = n
        for _ in range(max_steps_per_traj):
            if m <= 1:
                break
            tm = T(m)
            ln_m = math.log2(m) if m > 1 else 0.0
            ln_t = math.log2(tm) if tm > 1 else 0.0
            d_log = ln_t - ln_m
            is_odd = bool(m & 1)
            if is_odd:
                log_odd.append(d_log)
            else:
                log_even.append(d_log)
            for name, fn in stats.items():
                d = float(fn(tm) - fn(m))
                if is_odd:
                    per_stat_steps[name][0].append(d)
                else:
                    per_stat_steps[name][1].append(d)
            m = tm

    elapsed = time.perf_counter() - t0

    out: Dict = {
        "n_start": n_start,
        "n_end": n_end,
        "stats": list(stats.keys()),
        "alphas": list(alphas),
        "betas": list(betas),
        "per_stat": {},
        "log2": {
            "odd": summarize(log_odd).asdict(),
            "even": summarize(log_even).asdict(),
            "all_steps": summarize(log_odd + log_even).asdict(),
        },
        "hybrid": [],
        "timing": {
            "n_traj": n_end - max(n_start, 2),
            "n_odd_steps": len(log_odd),
            "n_even_steps": len(log_even),
            "secs": elapsed,
        },
    }

    for name in stats:
        odd, even = per_stat_steps[name]
        out["per_stat"][name] = {
            "single": summarize(single_stat[name]).asdict(),
            "odd": summarize(odd).asdict(),
            "even": summarize(even).asdict(),
            "all_steps": summarize(odd + even).asdict(),
        }

    # Hybrid drifts L(T(m)) - L(m) = alpha * (stat) + beta * (log2)
    # Use numpy for efficiency over the cross-product (alpha, beta).
    import numpy as _np
    log_odd_np = _np.asarray(log_odd, dtype=_np.float64)
    log_even_np = _np.asarray(log_even, dtype=_np.float64)
    for name in stats:
        odd_s, even_s = per_stat_steps[name]
        odd_s_np = _np.asarray(odd_s, dtype=_np.float64)
        even_s_np = _np.asarray(even_s, dtype=_np.float64)
        for alpha in alphas:
            for beta in betas:
                odd_hy = alpha * odd_s_np + beta * log_odd_np
                even_hy = alpha * even_s_np + beta * log_even_np
                all_hy = _np.concatenate([odd_hy, even_hy])
                out["hybrid"].append({
                    "stat": name,
                    "alpha": alpha,
                    "beta": beta,
                    "odd": _np_summarize(odd_hy),
                    "even": _np_summarize(even_hy),
                    "all_steps": _np_summarize(all_hy),
                })

    return out


# ---------------------------------------------------------------------------
# Random-parity model expected drift (Tao/Lagarias-Weiss).
# ---------------------------------------------------------------------------


def random_model_step_drift(
    stat: Callable[[int], int],
    sample_n_start: int = 10 ** 6 + 1,
    sample_count: int = 100_000,
    seed: int = 1,
) -> Dict[str, float]:
    """
    Under the random-parity model, each step's parity is i.i.d. uniform.
    But the drift of stat(.) under one application of T at a *given* n
    is a deterministic function of n. So the random-parity model's
    expected drift is the average of step_drift over a *uniform sample
    of n*, weighted by the random walk's stationary distribution on
    residues mod 2^k.

    Under the standard random model (independent fair parity bits), the
    stationary distribution on the integer is *not* well-defined (the
    walk on log n drifts), so we instead compute:

      E_odd[stat(T(n)) - stat(n)]  averaged over a sample of ODD n
      E_even[stat(T(n)) - stat(n)] averaged over a sample of EVEN n
      E_avg                        = 0.5 * E_odd + 0.5 * E_even

    This is the *Lagarias-Weiss / Tao* expected drift along one parity
    step. We sample n from a large range to approximate the natural
    measure on residues; for digit-structure statistics the sample size
    determines accuracy of the binary-digit averages.

    Note: we explicitly avoid the (much harder) issue of long-term
    correlations -- the random model treats successive parities as iid,
    which is exactly the regime where Lagarias-Weiss predict a logarithmic
    descent. So a positive drift of L on EVERY parity step would be a
    serious obstruction; a *negative* drift on odd steps that's compensated
    by smaller drift on even steps is the typical pattern for a function
    that "tries" to be Lyapunov.
    """
    import random
    rng = random.Random(seed)

    odd_deltas: List[float] = []
    even_deltas: List[float] = []
    sampled_odd = 0
    sampled_even = 0
    # Sample from [sample_n_start, sample_n_start + 4 * sample_count),
    # filter into odd / even buckets until we have ~sample_count/2 of each.
    target_each = sample_count // 2
    candidate = sample_n_start
    span = 64 * sample_count
    sampled_n = rng.sample(range(sample_n_start, sample_n_start + span),
                           min(span, 8 * sample_count))
    for n in sampled_n:
        if sampled_odd >= target_each and sampled_even >= target_each:
            break
        _, _, d = step_drift(stat, n)
        if n & 1:
            if sampled_odd < target_each:
                odd_deltas.append(float(d))
                sampled_odd += 1
        else:
            if sampled_even < target_each:
                even_deltas.append(float(d))
                sampled_even += 1

    e_odd = sum(odd_deltas) / len(odd_deltas) if odd_deltas else 0.0
    e_even = sum(even_deltas) / len(even_deltas) if even_deltas else 0.0
    e_avg = 0.5 * (e_odd + e_even)
    return {
        "E_odd": e_odd,
        "E_even": e_even,
        "E_avg_iid_parity": e_avg,
        "n_odd_sample": len(odd_deltas),
        "n_even_sample": len(even_deltas),
    }


# ---------------------------------------------------------------------------
# Closed-form expected drifts under a uniform-bit model (for s, r, c).
# ---------------------------------------------------------------------------


def closed_form_uniform_drift_summary(
    bit_length: int = 30,
    samples: int = 50_000,
    seed: int = 1,
) -> Dict[str, Dict[str, float]]:
    """
    Compute the expected drift of s, r, c under the simple model where n is
    a uniform random integer of bit-length bit_length (so n in [2^(L-1),
    2^L) uniformly), separately for odd and even n.

    The point: this exhibits the *digit-model* expected drift without
    trajectory effects. If even under this benign iid-bit model the drift
    is strictly positive on average for every statistic, that's the
    cleanest obstruction theorem.

    For s(n): even n -- n/2 just shifts bits, so s(n/2) = s(n) (no change).
              odd n  -- (3n+1)/2: this is the nontrivial case.
                       Heuristically s grows by ~ 1/2 on average because
                       3n+1 ~ n + 2n, and the second addition adds about
                       a bit on average due to carries.
    """
    import random
    rng = random.Random(seed)

    lo = 1 << (bit_length - 1)
    hi = 1 << bit_length

    results: Dict[str, Dict[str, float]] = {}
    for name, fn in [("hamming", hamming_weight),
                     ("runs", run_count),
                     ("carry", carry_count)]:
        odd_d: List[float] = []
        even_d: List[float] = []
        for _ in range(samples):
            n = rng.randrange(lo, hi)
            sn = fn(n)
            tn = T(n)
            st = fn(tn)
            d = float(st - sn)
            if n & 1:
                odd_d.append(d)
            else:
                even_d.append(d)
        results[name] = {
            "bit_length": bit_length,
            "n_samples_odd": len(odd_d),
            "n_samples_even": len(even_d),
            "E_odd": sum(odd_d) / max(len(odd_d), 1),
            "E_even": sum(even_d) / max(len(even_d), 1),
            "E_avg": (sum(odd_d) + sum(even_d)) / samples,
            "Var_odd": sum((d - (sum(odd_d) / max(len(odd_d), 1))) ** 2
                           for d in odd_d) / max(len(odd_d) - 1, 1),
            "Var_even": sum((d - (sum(even_d) / max(len(even_d), 1))) ** 2
                            for d in even_d) / max(len(even_d) - 1, 1),
            "max_inc_odd": max(odd_d) if odd_d else 0.0,
            "max_inc_even": max(even_d) if even_d else 0.0,
        }
    return results


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------


def main(n_start: int = 1,
         n_end: int = 10_001,
         alphas: Optional[List[float]] = None,
         betas: Optional[List[float]] = None,
         out_path: Optional[str] = None,
         random_sample_size: int = 50_000,
         random_sample_start: int = 10_000_001,
         closed_form_bit_lengths: Optional[List[int]] = None,
         closed_form_samples: int = 30_000) -> Dict:
    """Run the full Part A pipeline. Returns the summary dict and writes JSON."""
    if alphas is None:
        alphas = [0.0, 0.25, 0.5, 1.0, 2.0, 5.0]
    if betas is None:
        betas = [0.0, 0.25, 0.5, 1.0, 2.0]
    if closed_form_bit_lengths is None:
        closed_form_bit_lengths = [16, 24, 32]

    stats = {
        "hamming": hamming_weight,
        "runs": run_count,
        "carry": carry_count,
    }
    print(f"Trajectory sweep n in [{n_start}, {n_end}) over {len(stats)} stats ...")
    sweep_data = sweep_candidates(n_start, n_end, stats, alphas, betas)
    print(f"  done: {sweep_data['timing']['n_odd_steps']} odd-steps, "
          f"{sweep_data['timing']['n_even_steps']} even-steps in "
          f"{sweep_data['timing']['secs']:.2f}s")

    print("Random-parity model expected drift (sampling from large n)...")
    rand_data: Dict[str, Dict[str, float]] = {}
    for name, fn in stats.items():
        rand_data[name] = random_model_step_drift(
            fn, sample_n_start=random_sample_start,
            sample_count=random_sample_size)
    print("  done.")

    print("Closed-form uniform-bit model drift...")
    cf_data: Dict[str, Dict] = {}
    for L in closed_form_bit_lengths:
        cf_data[f"L={L}"] = closed_form_uniform_drift_summary(
            bit_length=L, samples=closed_form_samples)
    print("  done.")

    summary = {
        "version": 1,
        "description": "Digit-structure Lyapunov candidate search for accelerated Collatz T.",
        "sweep": sweep_data,
        "random_parity_model": rand_data,
        "closed_form_uniform_bit": cf_data,
    }

    if out_path is None:
        out_path = os.path.join(DATA_DIR, "lyapunov_sweep.json")
    with open(out_path, "w") as fp:
        json.dump(summary, fp, indent=2)
    print(f"Wrote {out_path}")
    return summary


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--n-start", type=int, default=1)
    p.add_argument("--n-end", type=int, default=10_001)
    p.add_argument("--random-sample-size", type=int, default=50_000)
    p.add_argument("--out", type=str, default=None)
    args = p.parse_args()
    main(n_start=args.n_start, n_end=args.n_end,
         random_sample_size=args.random_sample_size,
         out_path=args.out)
