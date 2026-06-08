# Sieve Q3 smoothness signal — joint (v_2, log_2 odd-kernel) control

**Track:** Collatz Vector A — Wave 5 alt-angle second-tier control (follow-up to `sieve_q3_control.md`).
**Author:** Alex Ye.
**Date:** 2026-06-08.
**Status:** `[CANDIDATE — outcome: SIGNAL SURVIVES BUT DOWNGRADED AGAIN. The C1 v_2-only matched 13.4% drop at y=10 is reproduced. Joint matching on (v_2, log_2 odd_kernel) shrinks the drop further to 8.5% with bootstrap CI95 [3.6, 12.9]%. Under the apples-to-apples restriction to joint cells with non-empty non-smooth pool supply, the drop is 6.7% with CI95 [2.07, 11.14]%. The y-scan under joint matching is still monotone (8.5, 2.2, 1.3, 0.3 for y=10, 20, 50, 100). N=10^8 spot check in shell [20, 26) gives 5.3% (CI95 [2.7, 7.6]%) — same sign, slightly smaller magnitude. Verdict: PARTIALLY REAL. The genuinely-smoothness component is roughly 5-9% at y=10, well below the headline 24% but above zero with statistical confidence.]` `[NOVELTY UNVERIFIED]`.
**Code:** `sieve_q3_joint_control_probe.py`. **Data:** `data/sieve_q3_joint_control_probe.json`, `data/sieve_q3_joint_control_restricted.json`, `data/sieve_q3_joint_control_N1e8.json`.

---

## 0. Verdict (read first)

> The prior probe (`sieve_q3_control.md`) controlled for `v_2(n)` and
> reduced the headline 24% Q3 smoothness drop to **13.4%**. It honestly
> flagged the next-finer confounder: the **log_2 of the odd kernel**
> `k = n / 2^{v_2(n)}`, which inside each v_2 bucket can still differ
> between smooth and non-smooth integers. This probe runs that control.
>
> ### Results at N = 10^6, shell log_2 n in [16, 20)
>
> | y | n_smooth | smooth mean | C1 v_2-only matched | C1 drop% | joint matched | joint drop% | joint CI95 |
> |---|----------|-------------|---------------------|----------|---------------|-------------|------------|
> | 10  | 660    | 3.618 | 4.180 | **13.44%** | 3.955 | **8.50%** | [3.60, 12.89]% |
> | 20  | 5,914  | 4.265 | 4.400 | 3.07%      | 4.360 | 2.17%     | [0.68, 3.72]%  |
> | 50  | 25,285 | 4.453 | 4.539 | 1.90%      | 4.513 | 1.34%     | [0.65, 2.01]%  |
> | 100 | 59,015 | 4.571 | 4.580 | 0.20%      | 4.584 | 0.29%     | [-0.14, 0.71]% |
>
> ### What the joint control did
>
> - **Reproduced C1.** The v_2-only matched 13.44% drop at y=10 (and
>   3.07, 1.90, 0.20 for y=20, 50, 100) matches the prior probe almost
>   exactly. (Small numerical drift vs the prior 13.4% / 3.5% / 1.6% / 0.4%
>   is from different RNG seed for the matched-subsample draw; magnitudes
>   agree.)
> - **Joint matching shrinks the residual.** At y=10 the drop falls from
>   13.4% to 8.5%, a further ~5 percentage points absorbed by odd-kernel
>   matching. The Hildebrand-direction "real-smoothness" effect is now
>   ~8.5%, not ~13%.
> - **CI95 excludes zero.** The bootstrap 1000-resample CI on the y=10
>   joint-matched gap is [3.60, 12.89]% — narrow enough that the signal
>   is **not noise**, but wide enough that 8.5% should be read as
>   "between ~4% and ~13%".
> - **Y-scan still monotone.** 8.5% → 2.2% → 1.3% → 0.3% under joint
>   matching. The shape is the same as under C1 (just lower magnitudes).
>   The y=10 / y=100 ratio is ~30x — clearly structured, not flat noise.
>
> ### What changed under the apples-to-apples restriction
>
> The joint matching has one structural complication: at y=10, **16 of
> the 660 smooth integers** sit in a joint cell `(v_2=5+, log_2 k=0-2)`
> for which the non-smooth pool is **structurally empty** (a non-smooth
> integer with v_2 ≥ 5 and odd kernel ≤ 4 in shell [2^16, 2^20) would
> need v_2 ≥ 14, contradicting kernel > 7-multiple-of-small-prime — but
> non-smooth needs a prime > 10 in the kernel, so kernel ≥ 11. So the
> cell is genuinely inaccessible to non-smooth integers in this shell).
>
> Dropping those 16 unmatchable smooth integers (2.4% of the smooth
> population) and re-comparing gives:
>
> | y | n_smooth_retained | dropped | restricted drop% | restricted CI95 |
> |---|-------------------|---------|------------------|-----------------|
> | 10  | 644    | 16  | **6.68%** | [2.07, 11.14]% |
> | 20  | 5,898  | 16  | 2.81%     | [1.27, 4.30]%  |
> | 50  | 25,269 | 16  | 1.24%     | [0.56, 1.92]%  |
> | 100 | 58,889 | 126 | 0.07%     | [-0.41, 0.54]% |
>
> So the "fairest" reading is roughly **5-9% drop at y=10 with non-trivial
> uncertainty**, ~2.8% at y=20, ~1.2% at y=50, zero at y=100.
>
> ### N = 10^8 cross-check at y=10, shell [20, 26)
>
> | quantity | value |
> |----------|-------|
> | n_smooth | 1,888 |
> | smooth mean | 3.7456 |
> | C1 v_2-only matched mean | 4.3746 |
> | C1 drop | 14.38% (CI95 [12.17, 16.47]%) |
> | Joint matched mean | 3.9537 |
> | **Joint drop** | **5.26% (CI95 [2.72, 7.61]%)** |
>
> At three-times-larger smooth sample (1888 vs 660) and a different shell
> at 100x larger N, the joint-matched drop is 5.3% with a tighter CI that
> excludes zero. **The effect is not just a small-sample fluke at
> N = 10^6**; it persists.
>
> ### THE VERDICT: REAL BUT SMALL
>
> - The original 24% drop overstated the genuinely-smoothness effect by
>   roughly **3-5x**. The first control (v_2) explained about half;
>   the second (joint with log_2 odd kernel) explained another third of
>   what remained.
> - What is left after two controls is in the **5-9% range** at y=10,
>   monotonically decaying with y, with bootstrap CIs that exclude zero
>   at all y < 100, and a confirmed N=10^8 spot check.
> - This is the "(a) genuine smoothness effect" branch the task spec
>   described as "survives joint matching ≥ ~8%". We are at the lower
>   boundary of that band (8.5% under the unrestricted matching, 6.7%
>   under the apples-to-apples restriction). Calling it "robustly alive"
>   would be slightly too strong; calling it "killed" would be wrong.
> - **My honest read:** the smoothness signal is real and arithmetic, but
>   the effect size is small enough that motivating a Hildebrand-style
>   smooth-Collatz Dickman programme on its strength alone is much
>   weaker than the original 24% number would have suggested. The
>   original sieve route is alive but downgraded for a second time.

---

## 1. Why a joint (v_2, log_2 k) control?

Write `n = 2^{v_2(n)} * k` where `k` is the **odd kernel**. The C1 control
matched `v_2(n)` between smooth and non-smooth, but within each v_2 bucket
the *odd kernels* of smooth integers are still structurally different from
typical:

- A y=10-smooth integer has odd kernel `k = 3^a · 5^b · 7^c` (with primes
  drawn from {3, 5, 7}). In any shell, the typical magnitude of such a
  kernel is constrained — it is biased toward smaller values because only
  three odd primes are admissible.
- A non-smooth integer in the same v_2 bucket has odd kernel drawn from
  a much larger set of multiplicative compositions, biased toward larger
  values per a Dickman-like argument.
- Collatz orbits of `n` are determined entirely by `n` (not separately by
  v_2 and k), so a smaller odd kernel — even at the same v_2 — could
  systematically produce shorter orbits. This is *not* captured by the v_2
  control.

The joint control matches the non-smooth subsample on the **joint
distribution** of (v_2 bucket, log_2 k bucket), neutralizing the most
obvious second-order confounder.

---

## 2. Methodology

### Pool, observables, primitives

Identical to `sieve_q3_control_probe.py`:
- `N = 10^6`, accelerated Collatz map.
- `sigma_inf(n)` total stopping time, observable `sigma_inf(n) / log_2 n`.
- Shell: `log_2 n in [16, 20)`, n in [65536, 1048576), 934,465 integers.
- Smoothness: `P^+(n) <= y`, computed via the same modified sieve.
- `v_2(n)`: standard. **Odd kernel:** `k(n) := n >> v_2(n)`.

### Bucket choices

- **v_2 buckets:** {0, 1, 2, 3, 4, 5+} (same as C1, for consistency).
- **log_2(k) buckets:** {0-2, 3-5, 6-8, 9-11, 12-14, 15+} (6 buckets,
  3-bit wide). This is the resolution suggested by the task spec.
  In shell [16, 20), log_2(k) ranges up to ~19 (when v_2 = 0).

Total cells: 6 × 6 = 36 possible; smooth populations occupy 11-13 cells
non-trivially at y in {10, ..., 100}.

### Matching

For each y, partition the non-smooth pool by joint cell (v_2 bucket,
log_2 k bucket). Then for each smooth-cell count, draw without
replacement from the corresponding non-smooth bucket to match. Capped
at pool supply when supply is smaller than smooth target (a deficit).

### Bootstrap CI

For each y, after computing smooth and joint-matched mean ratios,
resample each population with replacement 1000 times and compute the
empirical (2.5%, 97.5%) percentiles of the gap `1 - smooth/matched`.

### Restricted comparison (auxiliary)

For honest apples-to-apples reporting: in cells where the non-smooth pool
supply is zero (the joint cell is structurally unreachable for non-smooth
integers in shell), drop those smooth integers and recompute. This gives
the gap on the portion of the smooth population that *could be matched
at all*.

---

## 3. Results

### (1) C1 reproduction

| y | smooth mean | C1 matched mean | drop | (prior probe drop) |
|---|-------------|-----------------|------|---------------------|
| 10  | 3.618 | 4.180 | 13.44% | 13.4% ✓ |
| 20  | 4.265 | 4.400 | 3.07%  | 3.5%   |
| 50  | 4.453 | 4.539 | 1.90%  | 1.6%   |
| 100 | 4.571 | 4.580 | 0.20%  | 0.4%   |

The y=10 reproduction is essentially exact. Slight drift at y=20, 50, 100
is from a different RNG seed for the matched-subsample draw (this probe
uses seed 20260608+y per y; the prior probe used 20260608 once). All
within sampling noise.

### (2) Joint distribution and bucket supports

Smooth y=10 in shell [16, 20) occupies 13 joint cells. Selected key cells:

| (v_2 bucket, log_2 k bucket) | smooth count | non-smooth pool supply | achieved |
|------------------------------|--------------|------------------------|----------|
| (0, 15+)        | 87  | 467,145 | 87  |
| (1, 15+)        | 80  | 233,536 | 80  |
| (2, 12-14)      | 15  | 8,177   | 15  |
| (2, 15+)        | 55  | 108,561 | 55  |
| (3, 12-14)      | 29  | 12,259  | 29  |
| (3, 15+)        | 35  | 46,081  | 35  |
| (4, 12-14)      | 40  | 14,296  | 40  |
| (4, 15+)        | 17  | 14,849  | 17  |
| (5+, 0-2)       | 16  | **0**   | **0** (deficit) |
| (5+, 3-5)       | 35  | 75      | 35  |
| (5+, 6-8)       | 62  | 813     | 62  |
| (5+, 9-11)      | 114 | 6,888   | 114 |
| (5+, 12-14)     | 75  | 21,125  | 75  |

The (5+, 0-2) cell is the only structural deficit at y=10. For the
non-smooth pool: an integer with v_2 ≥ 5 and odd kernel ≤ 4 would have
n ≤ 2^v · 4. In shell [2^16, ∞), we need n ≥ 2^16, so v ≥ 14. But the
v_2 bucket "5+" includes all v ≥ 5, so it could in principle contain
elements with v = 14, 15, 16, 17, 18, 19 and odd kernel ≤ 4. **However**,
"non-smooth" means there is a prime factor > 10 in n; if the odd kernel
k ≤ 4 then k ∈ {1, 3} (must be odd), neither of which has a prime > 10.
So the (5+, 0-2) cell is empty in the non-smooth pool by definition.
This is **not a sampling artifact** but a structural constraint;
smoothness *enables* this combination in a way non-smoothness cannot.

At y=20, an additional deficit appears at (5+, 3-5): smooth wants 71
samples, pool supplies only 39. At y=50, the (5+, 3-5) deficit grows to
98 wanted vs 12 supplied. At y=100, additional deficits at (5+, 3-5) and
(5+, 6-8).

These deficits introduce a small inconsistency in the joint-matching
comparison (the matched mean is computed on a slightly smaller subsample
than the smooth mean). The "restricted" comparison below quantifies the
impact.

### (3) Joint-matched gap with bootstrap CI

| y | smooth mean | joint matched mean | drop% | CI95 | n_smooth | n_matched |
|---|-------------|--------------------|-------|------|----------|-----------|
| 10  | 3.6184 | 3.9547 | **8.50%** | [3.60, 12.89]% | 660    | 644    |
| 20  | 4.2651 | 4.3599 | 2.17%     | [0.68, 3.72]%  | 5,914  | 5,866  |
| 50  | 4.4528 | 4.5131 | 1.34%     | [0.65, 2.01]%  | 25,285 | 25,187 |
| 100 | 4.5708 | 4.5842 | 0.29%     | [-0.14, 0.71]% | 59,015 | 58,683 |

- **y=10**: the drop falls from 13.44% (C1) to 8.50% (joint). About a
  third of the C1 residual was the odd-kernel-size confounder. The CI is
  [3.6, 12.9]% — narrow enough to exclude zero, wide enough that the
  point estimate has ~3% uncertainty.
- **y=20**: falls from 3.07% to 2.17%, CI [0.68, 3.72]% — still excludes
  zero.
- **y=50**: 1.34%, CI [0.65, 2.01]% — still positive, very narrow.
- **y=100**: 0.29%, CI [-0.14, 0.71]% — **includes zero**. At y=100 the
  joint-matched signal is statistically indistinguishable from zero.

### (4) Restricted comparison (cells with non-empty non-smooth supply)

Dropping the smooth integers in cells where non-smooth pool supply = 0
(the structurally-inaccessible cells) gives the cleanest apples-to-apples
comparison:

| y | n_smooth_retained | n_dropped | drop% | CI95 |
|---|-------------------|-----------|-------|------|
| 10  | 644    | 16 (2.4%) | **6.68%** | [2.07, 11.14]% |
| 20  | 5,898  | 16 (0.3%) | 2.81%     | [1.27, 4.30]%  |
| 50  | 25,269 | 16 (0.1%) | 1.24%     | [0.56, 1.92]%  |
| 100 | 58,889 | 126 (0.2%)| 0.07%     | [-0.41, 0.54]% |

Under this strictest reading the y=10 drop is **6.68%, CI [2.07, 11.14]**.
Still positive, but on the small side of the "(a) genuine smoothness
effect ≥ 8%" threshold suggested by the task spec.

### (5) Y-scan under joint matching — monotone decay confirmed

Joint-matched drop% (unrestricted): 8.50% → 2.17% → 1.34% → 0.29%.
Restricted drop%: 6.68% → 2.81% → 1.24% → 0.07%.

Both versions:
- Decay monotonically as y grows. ✓
- Are at-or-above the prior C1 y-scan in *direction* but *smaller in
  magnitude* at every y, by roughly the same proportion (~30-40%
  of the C1 residual eaten by odd-kernel matching at y=10, much less at
  larger y where smoothness barely correlates with kernel size).
- Show the y=10 / y=100 ratio of ~30x for unrestricted, ~95x for
  restricted — a structured pattern, not flat noise.

This is what one would expect if the signal is real but the y=10 case is
the only one where the smoothness-vs-kernel-size correlation matters
inside v_2 buckets. At larger y, smoothness admits enough kernels that
the kernel-size distribution inside each v_2 bucket is close to
non-smooth's, so the joint correction matters less.

### (6) N = 10^8 spot check at y=10

To check whether the residual gap is an N = 10^6 small-sample artifact,
re-ran at N = 10^8 with shell `log_2 n in [20, 26)` (so n in
[2^20, 2^26) ≈ [10^6, 6.7·10^7]). This is a *different* shell at a
*different* scale.

| quantity | value |
|----------|-------|
| shell size | 66,060,288 |
| n_smooth (y=10) | 1,888 |
| smooth mean | 3.7456 |
| shell baseline mean | 4.7613 |
| raw drop | 21.3% |
| C1 v_2-only matched mean | 4.3746 |
| C1 drop | **14.38%**, CI95 [12.17, 16.47]% |
| Joint matched mean | 3.9537 |
| **Joint drop** | **5.26%**, CI95 [2.72, 7.61]% |
| Joint deficit cells | 1 (5+, 0-2) only |

Wall time: 174 s (single-core Python).

- **Headline behaviour reproduced** at a different shell, larger N. Raw
  drop 21.3% (vs 23.8% at N=10^6 shell [16, 20)).
- **C1 v_2-only drop 14.38%** is close to the N=10^6 value of 13.44%,
  with much tighter CI [12.17, 16.47]% on the larger sample.
- **Joint drop 5.26%** is a bit smaller than the N=10^6 value 8.50%.
  Both CIs exclude zero, and the higher-N value (CI95 [2.72, 7.61]) is
  comfortably tighter. The two are within their respective CIs of each
  other.

**The residual joint-matched signal persists at N = 10^8.** Magnitude
is small (~5%) but statistically clean. This is the strongest
evidence the effect is real and not a small-sample fluke.

---

## 4. Verdict

**Outcome: PARTIALLY REAL.** Both first-tier (v_2) and second-tier
(v_2, log_2 odd kernel) controls leave a small residual gap that is
statistically distinguishable from zero. The "genuine smoothness" effect
size at y=10 is roughly **5-9%**, depending on how strictly one accounts
for structurally inaccessible joint cells, and **drops monotonically with y**.

| Question (per task spec) | Answer |
|--------------------------|--------|
| C1 13.4% reproduced? | Yes, 13.44% at y=10. |
| Joint distribution + buckets reported? | Yes (13 cells at y=10). |
| Joint-matched gap with bootstrap CI? | 8.5%, CI95 [3.6, 12.9]% (or 6.7%, CI95 [2.1, 11.1]% restricted). |
| Y-scan under joint matching monotone? | Yes: 8.5%→2.2%→1.3%→0.3% (unrestricted), 6.7%→2.8%→1.2%→0.07% (restricted). |
| N=10^8 cross-check? | Yes, joint drop = 5.3%, CI95 [2.7, 7.6]%. |
| Three-way verdict (real / partial / artifact)? | **Real, but small.** At the lower edge of the "≥8% survives" branch (8.5% unrestricted), at the upper edge of "shrinks to 3-5%" (6.7% restricted, 5.3% at N=10^8). The honest call is **partially real**. |

### Honest assessment

What I am confident in:
- The C1 v_2-matched 13.4% is reproduced exactly; the prior probe was correct.
- Joint matching on (v_2, log_2 k) further reduces the y=10 gap by 4-5 pp,
  to roughly 8.5% (unrestricted) or 6.7% (restricted to comparable cells).
- The 95% bootstrap CI excludes zero at y in {10, 20, 50} under both
  versions of the comparison; it includes zero at y = 100.
- The y-scan monotone decay structure (~30x reduction from y=10 to y=100)
  survives the joint control.
- N=10^8 confirms the signal at a different shell and scale.

What I am NOT confident in:
- Whether the residual 5-9% is "genuinely arithmetic" or a third
  unidentified confounder (e.g., joint matching on (v_2, log_2 k) does
  *not* match on, say, `v_3(k)` or the number of distinct odd prime
  factors of k). The pattern of "every finer control eats some of the
  signal" suggests further controls might keep shrinking it.
- Whether the effect at y=10 fully closes at very large N. The drift
  from 8.5% (N=10^6) to 5.3% (N=10^8) is in the direction of further
  shrinkage; another decade (N=10^9 or 10^{10}) would clarify.
- The structurally-unreachable cells (e.g. (5+, 0-2) for y=10) are a
  genuinely awkward feature of joint matching at low y. A more
  sophisticated control might project the smooth distribution onto the
  non-smooth-feasible subspace before matching; I have not done this.

### Comparison to task spec's three outcomes

The task spec listed three possible outcomes:
- **(a) Gap survives substantively (≥ ~8%)**: 8.5% unrestricted is at
  the boundary; 6.7% restricted is just below. ~Marginal positive.
- **(b) Gap shrinks to ~3-5%**: at N=10^8, joint drop is 5.3%, which
  *is* in this band. The N-shift suggests we may be in this band rather
  than (a) at scale.
- **(c) Gap vanishes**: clearly not — CI excludes zero at all probed N.

**My honest call: between (a) and (b).** The y=10 signal at N=10^6 is
borderline-(a); at N=10^8 it slides into (b). The Hildebrand direction
is **alive but with a smaller effect size than the prior probe
suggested**, in line with the pattern that every additional control eats
some fraction of what remains.

### What I would do next (not done here)

1. **Match on (v_2, log_2 k, ω(k))** where `ω(k)` is the number of
   distinct odd prime factors of k. This is the natural next-finer
   control — smooth integers have small `ω(k)`, and this might explain
   another chunk of the residual.
2. **Run at N = 10^9 or 10^{10}** at y=10 to confirm or refute the
   apparent drift from 8.5% to 5.3% as N scales. If the joint drop
   keeps drifting toward 3-4%, the effect is dying out at scale.
3. **Test the Hildebrand functional form directly.** Compute
   `M(X, y) / M(X, ∞)` as a function of u = log X / log y in the
   joint-matched setting and check whether the curve has Dickman-like
   shape — this is the actual question a smooth-Collatz theorem would
   answer.

`[NOVELTY UNVERIFIED]`. No live arXiv search performed in this session.
The pattern of "obvious confounders that successively eat the signal"
is suspicious enough that I would strongly recommend an ANT-expert
literature review before pursuing this further.
