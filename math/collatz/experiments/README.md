# Collatz Computational Toolkit

Production-grade infrastructure for computational investigation of the Collatz
(3n+1) conjecture. Built for the multi-agent research effort under
`/home/user/wikiclaws/math/collatz/` (authors: Alex Ye with Claude).

## Map convention

Throughout this toolkit we use the **accelerated Collatz map**
(also called the *Syracuse map*):

```
T(n) = n / 2          if n is even
T(n) = (3n + 1) / 2   if n is odd
```

One application of T compresses an odd-rule step and the immediately-following
halving step from the standard map. So if `s_std(n)` is the OEIS A006577
standard total stopping time and `k(n)` is the number of odd-rule applications
along the orbit, then `sigma_inf(n) = s_std(n) - k(n)`.

The accelerated map is preferred for analysis because

1. It has the cleanest random-walk heuristic: each step is "halve" (factor 1/2)
   or "multiply by ~3/2" (factor 3/2), expected log-change
   `(1/2)log(1/2) + (1/2)log(3/2) = (1/2)log(3/4)`.
2. The expected stopping time `E[tau(n)]` is finite under the random model:
   `1 / (log 2 - (1/2) log 3) = 6.952...`.
3. Most modern papers (Tao 2019, Korec 1994, Sinai 2003) work with T.

## Files

| File | Purpose |
|---|---|
| `verifier.py` | Core: `total_stopping_time`, `stopping_time`, `trajectory`, `parity_vector`, `verify_range`, and the Oliveira-e-Silva-style `build_sieve` for batch verification. |
| `stats.py` | Distribution of stopping times, log-density regression, anomaly search, progressive records, plots. |
| `residue_analysis.py` | Structural analysis mod 2^k: the Syracuse map `phi_k: r |-> (a(r), b(r))`, descent fractions, candidate invariants. |
| `cycles.py` | Search for non-trivial cycles via (i) parity-sequence enumeration with the cycle equation, (ii) orbit-following. |
| `run_baseline.py` | Driver script: runs verification + stats on `n in [1, 10^7]` and writes data + figures. |
| `tests/test_verifier.py` | pytest suite (61 tests, all OEIS-cross-checked). |
| `data/` | JSON output of pipelines (gitignored if you prefer). |
| `figures/` | PNG plots. |

## Quick-start

```bash
cd math/collatz/experiments

# Run the tests
python -m pytest tests/ -v

# Verify all n in [1, 10^6] (benchmark)
python verifier.py --benchmark --upper 1000000

# Single-value queries
python verifier.py --sigma 27          # prints 70 (accelerated)
python verifier.py --trajectory 27     # prints full orbit

# Verify a specific range
python verifier.py --verify 1 100001

# Run the full baseline pipeline (≈ a few minutes for 10^7)
python run_baseline.py

# Quick smoke test (N = 10^5)
python run_baseline.py --quick

# Statistics only
python stats.py --N 1000000 --json data/stats_1e6.json

# Residue analysis only
python residue_analysis.py --k 4 8 12 16 20 --json data/residue_k4_to_20.json

# Cycle search only
python cycles.py --parity-m 22 --orbit-n 1000000 --json data/cycles.json
```

## Performance

On a single core (Python 3.11, no JIT):

| Range | Time | Throughput |
|---|---|---|
| `verify_range(1, 10^6)` | ~0.6 s | ~1.7 M n/s |
| `verify_range(1, 10^7)` | ~6 s | ~1.7 M n/s |
| `stats.run_full_stats(10^6)` | ~10 s | -- |
| `stats.run_full_stats(10^7)` | ~3 min | -- |
| `residue_analysis(k=20)` | ~3 s | -- |

The performance target was: verify `[1, 10^6]` in under 60 s on one core.
We're roughly 100x under budget.

### Optimization notes

1. **Closed-form k-step jumps** (Oliveira e Silva 2010). For `n = 2^k * q + r`,
   `T^k(n) = 3^{a(r)} * q + b(r)` where `a(r), b(r)` depend only on the bottom
   `k` bits. Hence we can advance `k` steps with O(1) integer operations after
   precomputing `(a, b)` for all `r < 2^k` (cost `O(k * 2^k)` once).

2. **Convergence cache**. We precompute `sigma_inf(n)` for `n < cache_limit`
   (default `2^18`); range verification then trades sieve jumps until the
   trajectory descends below `cache_limit`, at which point a table lookup
   gives the rest of `sigma_inf` for free.

3. **No arbitrary-precision blowup**. Python's int is arbitrary-precision,
   so we never overflow. For the ranges this toolkit targets (`n < 10^9`
   or so) the trajectory values stay comfortably within 64-bit; Python
   handles this efficiently.

## Extending the verification frontier

The current state-of-the-art is `n < 2^68 ~ 2.95 * 10^20` (Bareiss / Honda
/ Roosendaal verification efforts, completed 2017-2020). Extending this with
*pure Python* is not realistic: at our current ~2 M n/s, verifying `n < 2^68`
would take ~5 million CPU-years.

The recipe to push the frontier:

1. **Use larger k**. Build a sieve with `k = 30..40` (table size `~10^9` to
   `10^12`). The table generation cost grows with `2^k`; you'll want C or Rust.

2. **Restrict to non-descending residues**. Of the `2^k` residue classes mod
   `2^k`, only those with `a(r) >= k * log_2(3) / log_2(2) ~ 0.63 k` correspond
   to potential non-descent. For `k = 40` this prunes ~99% of residues.

3. **Parallelize across `q`**. The verification for `n = 2^k q + r`
   decomposes over `q`; embarrassingly parallel.

4. **Rewrite in a compiled language**. The hot loop is integer arithmetic;
   PyPy / Cython / C / Rust all give 50–500x speedup. A C extension wrapping
   our `verify_range` would let us hit ~10^11 / hour on a single core.

5. **Use GPU**. Trajectories under the sieve are pure integer arithmetic
   amenable to CUDA / OpenCL. Honda's verification used GPUs.

Hooks in the codebase for these extensions:
- `verifier.build_sieve` is pure Python; replace with NumPy or compiled
  version when needed.
- `verifier.verify_range` accepts a `sieve_k` parameter; raise it to 24–28
  once you have memory budget.
- `_build_small_cache` similarly accepts a `cache_limit`.

## Mathematical background and references

- J. C. Lagarias, *The 3x+1 problem: An overview* (annotated bibliography,
  multiple editions; arXiv:math/0309224 for the early version).
- R. Terras, *A stopping time problem on the positive integers*,
  Acta Arith. 30 (1976), 241–252.
- T. Tao, *Almost all orbits of the Collatz map attain almost bounded
  values*, Forum of Mathematics, Pi 10 (2022), e12 (arXiv:1909.03562).
- I. Korec, *A density estimate for the 3x+1 problem*, Math. Slovaca 44
  (1994), 85–89.
- Ya. G. Sinai, *Statistical (3x+1) problem*, Comm. Pure Appl. Math. 56
  (2003), 1016–1028.
- T. Oliveira e Silva, *Empirical verification of the 3x+1 and related
  conjectures*, in *The Ultimate Challenge: The 3x+1 Problem* (ed.
  Lagarias), AMS 2010.
- J. Simons, B. de Weger, *Theoretical and computational bounds for
  m-cycles of the 3x+1 problem*, Acta Arith. 117 (2005), 51–70.
- R. P. Steiner, *A theorem on the Syracuse problem*, Proc. 7th Manitoba
  Conf. on Numerical Math. (1977), 553–559.

OEIS sequences referenced:
- A006577 — total stopping time, standard map (used for cross-checking).
- A006370 — the standard Collatz function n -> n/2 or 3n+1.
- A014682 — the Syracuse / accelerated function.

## Honesty notes

This toolkit was built and verified against OEIS A006577 (every "known
value" hard-coded in tests was cross-checked by direct simulation against
the standard map and matched the OEIS values). Performance numbers in
this README were measured on the development machine.

The `cycles.py` module returns *only* the trivial cycle {1, 2} for all
search settings we've run; this is consistent with all prior work
(non-trivial cycles are ruled out below the verification frontier).
If you ever see a non-trivial cycle reported, double-check immediately —
something is wrong.

The "anomalies" reported by `stats.find_anomalies` are *not* anomalies in
any mathematical sense; they're simply the n with the largest stopping
time in each decade bucket. The terminology is conventional.
