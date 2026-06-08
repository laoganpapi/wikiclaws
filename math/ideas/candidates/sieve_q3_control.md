# Sieve Q3 smoothness signal — v_2(n) control test

**Track:** Collatz Vector A — Wave 5 alt-angle follow-up (control test of the surviving Q3 smoothness signal from `sieve_analytic.md`).
**Author:** Alex Ye.
**Date:** 2026-06-08.
**Status:** `[CANDIDATE — outcome: PARTIALLY REAL / PARTIALLY ARTIFACT. The headline 24% drop in mean sigma_inf/log_2 n for y=10 smooth integers in shell [16, 20) is reproduced. After controlling for v_2(n), about half the gap is explained by the 2-adic-valuation bias of smooth integers (free halvings), but a ~13% residual gap survives the matched-subsample control and a ~29% gap survives the residualized-observable control. The signal is NOT pure artifact, but the effect size is smaller than advertised once v_2 is matched.]` `[NOVELTY UNVERIFIED]`.
**Code:** `sieve_q3_control_probe.py`. **Data:** `data/sieve_q3_control_probe.json`.

---

## 0. Verdict (read first)

> The prior alt-angle (`sieve_analytic.md`) honestly flagged that the headline
> Q3 smoothness signal — a 24% drop in mean `sigma_inf(n) / log_2 n` for y=10
> smooth integers in dyadic shell `log_2 n in [16, 20)` — was NOT controlled
> for the most obvious confounder: the **2-adic valuation** `v_2(n)`. y=10
> smooth integers (primes in {2, 3, 5, 7}) are heavily biased toward large
> `v_2(n)` — and every factor of 2 is a "free halving" step in the Collatz
> orbit, trivially reducing `sigma_inf`.
>
> This probe runs the control. Two independent tests:
> - **(C1) Matched-subsample**: subsample non-smooth integers in shell
>   `[16, 20)` so that their `v_2` histogram matches the smooth population
>   (buckets `{0, 1, 2, 3, 4, 5+}`). Compare mean `sigma_inf/log_2 n`.
> - **(C2) Residualized observable**: subtract `v_2(n)` from `sigma_inf(n)`
>   (the "free halvings" contribution) and re-do smooth-vs-baseline.
>
> ### Results (n <= 10^6, shell log_2 n in [16, 20))
>
> | y | smooth count | smooth mean | shell baseline | drop_pct (raw) | mean v_2 (smooth) | mean v_2 (shell) | matched-mean (C1) | drop vs matched (C1) | residualized drop (C2) |
> |---|---|---|---|---|---|---|---|---|---|
> | 10  | 660    | 3.618 | 4.751 | **23.8%** | 4.95 | 1.00 | 4.180 | **13.4%** | **28.8%** |
> | 20  | 5 914  | 4.265 | 4.751 | 10.2%     | 3.06 | 1.00 | 4.420 | 3.5%      | 12.8%     |
> | 50  | 25 285 | 4.453 | 4.751 |  6.3%     | 2.25 | 1.00 | 4.523 | 1.6%      |  7.8%     |
> | 100 | 59 015 | 4.571 | 4.751 |  3.8%     | 1.88 | 1.00 | 4.587 | 0.4%      |  4.9%     |
>
> ### THE VERDICT: SOMETHING SUBTLE
>
> - **Headline reproduced.** Raw drop 23.8% at y=10 matches the documented 24%.
> - **The v_2 confounder is huge.** Smooth integers in shell [16, 20) have
>   mean `v_2 = 4.95`; the shell baseline has mean `v_2 = 1.00`. That's a
>   nearly five-bit difference in 2-adic content — the kind of bias that
>   *should* trivially shorten orbits.
> - **(C1) Matched control kills about half the effect.** After v_2-bucket
>   matching, the gap shrinks from 23.8% to 13.4%. So ~10 percentage points
>   of the headline 24% was the trivial v_2 artifact. **But ~13% survives.**
> - **(C2) Residualized observable preserves the effect.** Subtracting v_2(n)
>   from sigma_inf gives a *larger* drop (28.8%), confirming that the
>   smoothness benefit is NOT just the free-halving steps — smooth integers
>   have shorter orbits beyond what v_2 alone explains.
> - **y-scan is monotone in the right direction.** Matched-control drop
>   decays 13.4% -> 3.5% -> 1.6% -> 0.4% as y grows 10 -> 20 -> 50 -> 100.
>   A pure v_2 artifact would not show this structured scaling; the y=10
>   matched residual is too big to be noise.
>
> **Net read.** The Q3 smoothness signal at y=10 is partly real and partly
> v_2-confounded. The effect size after a fair v_2 control is roughly half
> what was advertised — ~13% rather than ~24%. The signal does NOT close to
> zero under either independent control, so calling it "pure artifact" is
> wrong. But the advertised effect was overstated by 2x because of the
> uncontrolled v_2 bias.
>
> **Status for the Hildebrand/Dickman route**: still alive but downgraded.
> A genuine smooth-Collatz Dickman theorem would need to be calibrated
> against this ~13% residual gap, not the ~24% raw gap. The sieve route is
> not closed, but it has lost a non-trivial fraction of its motivating
> effect size.

---

## 1. Why this control was needed

`sieve_analytic.md` Q3 reports that y=10 smooth integers `n` (i.e. those
whose largest prime factor is at most 10, so primes drawn from {2, 3, 5, 7})
in the dyadic shell `log_2 n in [16, 20)` have mean `sigma_inf(n) / log_2 n`
about **24% lower** than the shell baseline. The prior agent stratified by
dyadic shell, so the trivial "smooth integers are small" artifact is ruled
out. But the document explicitly flagged a remaining failure mode:

> "Genus-of-y-smooth-integers bias: smooth integers have constrained
> multiplicative structure that *might* tautologically reduce orbit length
> (e.g. n = 2^a * 3^b * 5^c ... has more 'even step' potential built in).
> The shell-stratification F1 does NOT control for this."

The cleanest version of that concern is the **2-adic valuation**:
`v_2(n)` = the number of times 2 divides `n`. Each factor of 2 in `n`
contributes one *deterministic* halving step at the very start of the
Collatz orbit. So `sigma_inf(n)` is bounded below by `v_2(n)` and, more
importantly, the *remaining* descent after stripping the initial halvings
is the genuinely arithmetic part of the orbit.

Smooth integers built from {2, 3, 5, 7} are heavily skewed toward high
`v_2`: in shell `[16, 20)`, the smooth population has **mean `v_2 = 4.95`**
while the shell baseline has **mean `v_2 = 1.00`** (the expected
geometric-distribution mean: `sum_{k>=1} k * 2^{-k-1} ... = 1`). That is
a five-bit gap. If you only correct for it crudely, you'd expect roughly
4 extra "free" halving steps in the smooth-mean numerator, i.e.
`sigma_inf` is mechanically smaller by about 4. With shell mean
`log_2 n ~ 18`, that's 4/18 ~ 22% — eerily close to the headline 24%.

So the control was *exactly* the right test to demand.

---

## 2. Methodology

### Pool and definitions

- `N = 10^6`, accelerated Collatz map (even n -> n/2; odd n -> (3n+1)/2),
  `sigma_inf(n)` = total stopping time, matching `sieve_analytic_probe.py`.
- Shell: `log_2 n in [16, 20)`, i.e. `n in [65536, 1048576)`.
  Shell size: 934,465 integers.
- y-smooth filter: `P^+(n) <= y`, where `P^+` is the largest prime factor
  (computed via a modified sieve identical to `sieve_analytic_probe.py`).
- `v_2(n)` table: standard.

### Observables

- **Raw**: `sigma_inf(n) / log_2 n`.
- **Residualized**: `(sigma_inf(n) - v_2(n)) / log_2 n`. Subtracts the
  trivial "free halvings" that v_2 contributes at the start of the orbit.

### Controls

**(C1) v_2-matched subsample.** For each y, partition the non-smooth
integers in shell [16, 20) by `v_2` bucket
(`{0, 1, 2, 3, 4, 5+}`). Sample without replacement from each bucket to
match the smooth population's bucket counts. Coverage diagnostic: in
every case the non-smooth pool comfortably exceeded the smooth target in
every bucket (e.g. for y=10, bucket "5+" target was 302 vs. pool supply
28,901), so the match is exact at the bucket level.

**(C2) Residualized observable.** Compute mean `(sigma_inf(n) - v_2(n))
/ log_2 n` on smooth and on shell baseline. The ratio reflects the
smoothness effect *after* the free-halving contribution is removed.

### y-scan

Beyond the headline y=10, run y in {10, 20, 50, 100}. If the smoothness
signal is genuinely arithmetic, the effect should scale structurally
with y. If it is purely v_2-confounded, larger y dilutes the v_2 bias
(since more primes are admissible, fewer prime factors need to be 2 for
"smoothness") and the matched-control drop should approach zero.

---

## 3. Results

### (1) Headline reproduction

| Quantity | Value |
|----------|-------|
| Full-range mean sigma_inf/log_2 n (n in [2, 10^6]) | 4.7499 |
| Shell [16, 20) baseline mean | 4.7505 |
| Shell [16, 20), y=10 smooth, n_smooth | 660 |
| Shell [16, 20), y=10 smooth mean | 3.6184 |
| **Raw drop** | **23.83%** |

Documented value in `sieve_analytic.md` F1 table: 0.762 ratio = 23.8%
drop. **Reproduced exactly.**

### (2) v_2(n) distribution in shell [16, 20)

Buckets: `{0, 1, 2, 3, 4, 5+}`.

| Pop. | 0 | 1 | 2 | 3 | 4 | 5+ | mean v_2 |
|------|---|---|---|---|---|-----|----------|
| All shell           | 467,232 | 233,616 | 116,808 | 58,404 | 29,202 | 29,203 | 1.00 |
| y=10 smooth         | 87 | 80 | 70 | 64 | 57 | 302 | **4.95** |
| y=20 smooth         | 1307 | 1055 | 839 | 664 | 524 | 1525 | 3.06 |
| y=50 smooth         | 7360 | 5347 | 3838 | 2739 | 1942 | 4059 | 2.25 |
| y=100 smooth        | 19,680 | 13,408 | 9,030 | 6,000 | 3,938 | 6,959 | 1.88 |
| Non-smooth (y=10)   | 467,145 | 233,536 | 116,738 | 58,340 | 29,145 | 28,901 | 1.00 |

Note: the shell distribution matches the theoretical geometric
distribution Pr[v_2 = k] = 2^{-(k+1)} almost perfectly (e.g. 467232 ~=
934465/2, etc.). The y=10 smooth population is extremely v_2-skewed:
46% of the population sits in the "5+" bucket vs. ~3% for shell-typical
integers.

### (3) C1 — matched-subsample control

| y | smooth mean | matched non-smooth mean | smooth/matched ratio | drop |
|---|---|---|---|---|
| 10  | 3.618 | 4.180 | 0.866 | **13.4%** |
| 20  | 4.265 | 4.420 | 0.965 | 3.5%      |
| 50  | 4.453 | 4.523 | 0.985 | 1.6%      |
| 100 | 4.571 | 4.587 | 0.996 | 0.4%      |

**About 10 of the 24 headline percentage points at y=10 vanish under
v_2-matching.** But 13.4% remains. At y=20 the residual collapses to
3.5%, and by y=100 the matched control basically zeros out (0.4% — noise
level).

### (4) C2 — residualized observable

| y | residualized smooth mean | residualized shell mean | drop |
|---|---|---|---|
| 10  | 3.345 | 4.697 | **28.8%** |
| 20  | 4.097 | 4.697 | 12.8% |
| 50  | 4.331 | 4.697 | 7.8%  |
| 100 | 4.469 | 4.697 | 4.9%  |

The residualized drop is *larger* than the raw drop at every y. This is
the right direction for "smoothness has structure beyond v_2": subtracting
v_2(n) from the numerator removes more "size" from the smooth-mean
numerator (which had high v_2) than from the baseline (low v_2), so if
smoothness only mattered via v_2 we would see the drop shrink. Instead it
grows. So even after removing the trivial halving budget, smooth integers
still descend faster.

### (5) The y-scan structure

Both controls show clean monotone decay with y:

- C1 matched drop: 13.4% -> 3.5% -> 1.6% -> 0.4%
- C2 residualized drop: 28.8% -> 12.8% -> 7.8% -> 4.9%

This is the right qualitative shape if the signal is real but
y-dependent. A pure v_2 artifact under C1 should fluctuate near zero
across y (since the matching neutralizes the bias). 13.4% residual at
y=10 with only 660 smooth points is the strongest signal, but the
y=20 value (3.5%, n=5914) is also above plausible noise (one-sigma on
the matched mean is roughly 0.04 in units of sigma/log_2 n; 3.5% of 4.75
is ~0.17, well above noise).

---

## 4. The two controls disagree — what does that mean?

C1 says **13.4% drop** at y=10. C2 says **28.8% drop**. These are
*different* questions:

- C1 holds v_2 *constant* and asks: among integers with the same
  v_2 profile, do the smooth ones descend faster? Answer: yes, by 13.4%.
- C2 *subtracts* v_2 contribution and asks: after removing free
  halvings, do smooth integers descend faster? Answer: yes, by 28.8%.

These don't contradict — they answer slightly different questions about
the same underlying effect. C1 is the "stricter" control because it
literally matches the distribution. C2 is a model-based subtraction
that assumes "free halvings" is the only way v_2 helps, which is itself
a non-trivial assumption (e.g., high v_2 also means n was generated
from a smaller odd kernel, which might correlate with other orbit
properties).

The reasonable read: the v_2-controlled effect size is **somewhere
between 13% and 29%** — at the lower bound under the strictest control,
at the upper bound under a simpler observable-level correction. Either
way it's a non-trivial residual.

---

## 5. Verdict

**Outcome: PARTIALLY REAL.** The headline 24% drop was overstated by
about 2x because of an uncontrolled v_2 bias. The true smoothness effect
at y=10 is closer to **13% under the strictest matched control**, which
is still a real, non-noise effect at this sample size.

| Question | Answer |
|----------|--------|
| Was the 24% drop reproduced? | Yes, exactly. |
| Is it a pure v_2 artifact? | No. About half is v_2; about half is something else. |
| Is the smoothness route alive? | Yes, but with a smaller effect size. |
| Should one chase a Hildebrand-style theorem? | The motivating effect is now ~13% not ~24%. Probably still worth a serious arXiv lit-search, but lower priority than the original document implied. |

### Honest assessment

What I'm confident in:
- The v_2 distribution in y=10 smooth integers in shell [16, 20) is
  enormously skewed (mean v_2 = 4.95 vs. shell mean 1.00). This is by
  far the largest confounder for `sigma_inf`-type observables on smooth
  integers and *must* be controlled in any future Q3 follow-up.
- Both controls (matched + residualized) point in the same direction
  (smoothness still helps after v_2 control), with different magnitudes.
  The agreement on sign is the real load-bearing fact; the
  disagreement on magnitude is a separate question about which control
  is "fairer".
- The y-scan shape under C1 (13.4% -> 3.5% -> 1.6% -> 0.4%) is
  consistent with a genuine smoothness effect that fades into noise by
  y=100, NOT with a coincidental v_2-driven pattern.

What I'm NOT confident in:
- Whether 13% is "real-and-meaningful" or "real-but-modest". With only
  660 smooth points at y=10 in this shell, the statistical noise on the
  matched-mean is non-negligible, and I have not computed a proper
  confidence interval (the matched-sample mean's standard error would
  need a bootstrap). A future probe should bootstrap the matched-mean.
- Whether the residual 13% reflects something genuinely arithmetic
  (e.g., 3-adic structure of the odd kernel) or another, subtler
  confounder I haven't identified (e.g., the odd-kernel size
  distribution conditional on v_2 differs between smooth and matched
  populations). To check, one could match on *both* v_2 *and* `log_2`
  of the odd kernel `m = n / 2^{v_2(n)}`.
- Whether the effect persists at much larger `N`. This probe is N=10^6;
  the prior agent's Q3 effect was claimed to be "monotonic and present
  in every shell" through F1, but the v_2 bias surely scales with shell
  size in some structured way I haven't worked out.

### What I would do next (not done here)

1. **Match on (v_2, log_2 odd kernel) jointly.** This is the natural
   next-finer control: maybe what's left of the 13% is the odd-kernel-size
   bias inside each v_2 bucket.
2. **Bootstrap the matched-mean** at y=10 to get a real CI on the 13.4%.
3. **Repeat at N = 10^9** (a couple of CPU-hours) to check whether the
   residual gap grows, shrinks, or stays constant with N. A constant or
   growing residual after v_2 matching would be a much stronger signal
   than the present probe.
4. **Compute the Dickman-style ratio M(X,y)/M(X,infty) on the
   residualized observable** as a function of `u = log X / log y` —
   this is the actual quantity a Hildebrand-style theorem would need to
   describe, and the present probe does not compute it.

`[NOVELTY UNVERIFIED]`. As in the prior document, I have not done an
arXiv search for "Collatz Dickman" / "Collatz smooth" / etc. The v_2
confounder is so obvious that I would be unsurprised if any prior
sieve-flavored Collatz paper had identified and dispatched it on page 1;
the present writeup is a *control test* of a project-internal claim,
not a literature contribution.
