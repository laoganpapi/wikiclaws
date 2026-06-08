# Sieve Q3 smoothness signal — triple (v_2, log_2 k, ω(k)) control + N = 10^9 scan

**Track:** Collatz Vector A — Wave 5 alt-angle third-tier control (follow-up to `sieve_q3_joint_control.md`). The deciding test.
**Author:** Alex Ye.
**Date:** 2026-06-08.
**Status:** `[CANDIDATE — outcome: F1 TRIGGERED. The ω(k) control at N=10^6 does NOT shrink the joint-matched gap (the omega distribution of the matched non-smooth subsample is already close to smooth's by construction once (v_2, log_2 k) is fixed). However, the N=10^9 scan at shell [2^25, 2^30) — once pool sampling is large enough to avoid deficit inflation — shows the C1 v_2-only matched drop collapse from 13-14% (at N≤10^8) to 6.25% [4.31, 8.21]%, the C2 joint drop collapse to 3.83% [1.64, 5.98]%, and the C3 triple-matched drop to 2.69% [0.56, 4.65]% (restricted: 2.12%, CI95 [-0.08, 4.48]% — includes zero). The residual signal is dying as N grows. Per the brief's 3-cell verdict matrix: the N=10^9 result is firmly in the "≤ 3%" / "F1 triggered" band. Verdict: SIGNAL DOES NOT ROBUSTLY SURVIVE. The Hildebrand program in `collatz_hildebrand_program.md` is closed under the falsifier F1 + F2 it specified for itself.]` `[NOVELTY UNVERIFIED]`.
**Code:** `sieve_q3_omega_N1e9_probe.py`. **Data:** `data/sieve_q3_omega_N1e9_partA.json`, `data/sieve_q3_omega_N1e9_partB.json`, `data/sieve_q3_omega_N1e9.json`, plus the corresponding `.log` files.

---

## 0. Verdict (read first)

The mission: settle whether the residual 5-8% effect (post v_2 + log_2 k matching) is a real arithmetic phenomenon or a confounder artifact. Two finer tests:

1. **Triple control (v_2, log_2 k, ω(k))** at N = 10^6. Does adding ω(k) — the number of distinct odd prime factors of the odd kernel — eat the remaining gap?
2. **N = 10^9 scan** at y = 10 in shell [2^25, 2^30). Does the joint-matched gap stabilize or shrink further at one more decade of N?

### Headline numbers

| Test | y=10 drop | CI95 | n_smooth | n_matched | notes |
|------|-----------|------|----------|-----------|-------|
| **A:** C2 joint, N=10^6 (reproduction) | 10.71% | [6.38, 15.00] | 660 | 644 | re-runs the prior probe with new seed; the prior reported 8.50% — variation is seed sensitivity |
| **A:** C3 triple (+ω), N=10^6  | **11.92%** | [7.49, 16.41] | 660 | 644 | adding ω does NOT shrink |
| **A:** C3 restricted, N=10^6 | 10.45% | [6.23, 14.66] | 644 | 644 | drop unmatchable cells |
| **B:** C1 v_2-only, N=10^9, shell [25,30) | **6.25%** | [4.31, 8.21] | 2428 | 2428 | dropped from ~14% at N=10^8 |
| **B:** C2 joint, N=10^9 | **3.83%** | [1.64, 5.98] | 2428 | 2390 | dropped from 5.3% at N=10^8 |
| **B:** C3 triple, N=10^9 | **2.69%** | [0.56, 4.65] | 2428 | 2389 | |
| **B:** C3 restricted, N=10^9 | **2.12%** | [-0.08, 4.48] | 2408 | 2389 | **CI includes zero** |

### THE VERDICT (per the brief's 3-cell decision matrix)

> The brief defined three outcomes:
>   - ω(k)-matched stays ≥ 5% AND N=10^9 stabilizes ≥ 4% → signal robustly real
>   - ω(k)-matched drops to ~3% OR N=10^9 collapses → **F1 triggered**, program dies
>   - mixed → inconclusive
>
> **We are in cell 2: F1 triggered.** The ω(k) control at N=10^6 does not shrink the signal (it actually nudges up to 11.92%, well above 5%), so the ω axis alone is not a confounder. **But the N=10^9 result collapses every gap by 30-60%:** C1 from 14% to 6.25%, C2 from 5.3% to 3.83%, C3 triple to 2.69%, C3 restricted to 2.12% with CI95 including zero. The decisive test is the N-scaling collapse: the signal shrinks toward zero as N grows, exactly the F2 pattern that `collatz_hildebrand_program.md` itself flagged as a program-killer.

### Mechanistic read of why ω(k) didn't do work

The omega-distribution within the matched non-smooth subsample (after (v_2, log_2 k) joint matching at y=10, N=10^6) is already very close to smooth's:

|     | ω=0 | ω=1 | ω=2 | ω=3 | ω=4 | ω=5 |
|-----|-----|-----|-----|-----|-----|-----|
| smooth | 4   | 98  | 338 | 220 | 0   | 0   |
| matched (joint, no ω) | 0   | 86  | 338 | 220 | 0   | 0   |
| nonsmooth pool (unmatched) | 0 | 153,742 | 380,827 | 306,103 | 86,419 | 6,656 |

So **the joint (v_2, log_2 k) matching already nearly equates ω(k) between smooth and matched non-smooth** — small odd kernel and low ω(k) are very strongly correlated, so the kernel-size match implicitly enforces ω(k) match. There is no further confounder to extract on the ω(k) axis. Adding ω(k) as a third matching axis at the same N just causes more deficits (the 5+|0-2|1 cell can't be filled by non-smooth either) without shifting the gap meaningfully. This is a *non-finding* on the ω(k) axis, but it is a clean non-finding.

The interesting confound the brief flagged — "matching on ω(k) may force the non-smooth subsample to be unusually structured (low ω(k), large prime factors)" — does occur but is absorbed within the existing (v_2, log_2 k) match. Matching on ω(k) on top changes the matched subsample by only ~10 elements (out of 644), and the recovered gap is statistically indistinguishable from the C2 result at the same N. **ω(k) is not the load-bearing confounder.**

### What killed the signal was N-scaling, not ω(k)

The C1 v_2-only matched gap evolves with N as:

| N | shell | n_smooth | C1 drop | C1 CI95 |
|---|-------|----------|---------|---------|
| 10^6 | [16, 20) | 660  | 13.44% | [~10, 17]% (prior probe) |
| 10^8 | [20, 26) | 1888 | 14.38% | [12.17, 16.47]% |
| **10^9** | **[25, 30)** | **2428** | **6.25%** | **[4.31, 8.21]%** |

C2 joint:

| N | shell | C2 drop | C2 CI95 |
|---|-------|---------|---------|
| 10^6 | [16, 20) | 8.5-10.7% (seed dep.) | [3.6, 15]% |
| 10^8 | [20, 26) | 5.26% | [2.72, 7.61]% |
| **10^9** | **[25, 30)** | **3.83%** | **[1.64, 5.98]%** |

This is monotone collapse with N. Falsifier F2 of `collatz_hildebrand_program.md` ("matched gap decays with shell index → effect is finite-size, no Hildebrand asymptotic applies") is therefore triggered. Combined with the C3 triple at N=10^9 dropping to 2.7% (CI lower bound 0.56%, restricted CI lower bound -0.08%), every reasonable read says the asymptotic effect is at or below ~3%.

### Caveats — read these before believing the verdict

1. **Pool sampling at N=10^9 was non-trivial.** A naive 500k uniform-shell sample under-supplied the high-v_2 cells (v_2 ≥ 5 with small odd kernel is rare), giving spurious 9-12% gaps from deficit inflation. The reported numbers use uniform sampling + targeted v_2-stratified oversampling (60k extra samples per v_2 ∈ {3,4,...,12,15,18,22,25,27} where supply allows), bringing deficits down to 2-3 cells (the structurally-inaccessible ones). The first naive run is in `data/sieve_q3_omega_N1e9_partB_naive_500k.log` (see git history if needed); the clean run is in `data/sieve_q3_omega_N1e9_partB.log`.
2. **Sample sizes are smaller than ideal.** n_smooth = 2,428 at N=10^9 in shell [25, 30) — comparable to the N=10^8 n_smooth = 1,888 in shell [20, 26), so we are at roughly the same statistical resolution per shell decade. The CIs reflect this: ±1.5pp on C2, ±2pp on C3.
3. **The C2 joint number at N=10^6 in Part A is 10.71%, not the 8.5% the prior md reports.** This is RNG seed sensitivity in the matching draw — different rng.sample seeds pick slightly different non-smooth representatives. Magnitudes agree (both inside the 95% CI of the other). The qualitative finding — joint-matched gap at N=10^6 is in the 8-11% range — is robust to the seed.
4. **F1's threshold was "drops to ~3%".** C2 at N=10^9 is 3.83%, just above; C3 is 2.69%, just below. Calling this "definitely F1" requires accepting that the joint-matched 5.3% at N=10^8 and the C2 3.83% at N=10^9 are on the same scaling curve heading toward zero; calling this "inconclusive" would also be defensible. **My honest read is "F1 triggered" because the trend is unambiguous (every additional decade of N or finer control shrinks the gap) and the C3 restricted CI includes zero.**

---

## 1. Methodology

### Part A: triple control at N = 10^6

Reuses the same primitives as `sieve_q3_joint_control_probe.py`:
- `N = 10^6`, accelerated Syracuse map for `σ∞(n)`.
- Shell: `log_2 n ∈ [16, 20)`, |shell| = 934,465.
- Smoothness via largest-prime-factor sieve (`P^+(n) ≤ y`).
- v_2 buckets: {0, 1, 2, 3, 4, 5+}.
- log_2(k) buckets: {0-2, 3-5, 6-8, 9-11, 12-14, 15+}.
- **ω(k) buckets:** {0, 1, 2, 3, 4+}. For y=10, k = 3^a · 5^b · 7^c so ω(k) ∈ {0, 1, 2, 3} only; the 4+ bucket appears only in the non-smooth pool.
- Matched-subsample without replacement; bootstrap CI with 1000 resamples.

### Part B: N = 10^9 scan at shell [2^25, 2^30)

Cannot keep a full sigma table for N = 10^9 in 15 GB RAM (`list[int]` of length 10^9 is ~ 6-30 GB). Instead:

- **Smooth enumeration** is direct: y=10 smooth in shell are exactly the integers 2^a · 3^b · 5^c · 7^d in [2^25, 2^30). Enumeration is exhaustive in microseconds (2,428 such integers).
- **Non-smooth pool** is built by sampling rather than enumerated. Two-phase:
  - Phase 1: 500,000 uniform draws from shell, classify by (v_2, log_2 k, ω(k)).
  - Phase 2 (added after a first run showed cell deficits): targeted v_2-stratified oversampling. For each v ∈ {3,4,...,12,15,18,22,25,27}, sample up to 60,000 random odd k in the corresponding sub-range and form n = k · 2^v.
- **σ∞** is computed via `verifier.sigma_inf_fast` using the Oliveira-e-Silva-style 16-bit residue sieve + cache up to 2^20. Only computed for the smooth set + matched subsamples (~2,400-2,500 integers per control), so total `σ∞` work is negligible.
- Bootstrap CI with 1000 resamples on each gap.

Wall time: **93.5 s** total for the N = 10^9 scan (570k pool draws + sigma on 7.3k integers + 3 × 1000 bootstrap resamples + 14 v_2-stratified oversample passes).

---

## 2. Detailed results

### 2.1 Part A: triple control at N = 10^6, shell [16, 20)

**Reproduction of C2 baseline + addition of ω(k).**

| y | n_smooth | smooth mean | C2 drop | C2 CI95 | C3 drop | C3 CI95 | C3-restricted drop | n_smooth retained |
|---|----------|-------------|---------|---------|---------|---------|---------------------|--------------------|
| 10  | 660    | 3.6184 | 10.71% | [6.38, 15.00] | **11.92%** | [7.49, 16.41] | 10.45% | 644 |
| 20  | 5,914  | 4.2651 | 2.72%  | [1.14, 4.27]  | 2.59%      | [1.14, 3.95]  | 2.07% | 5,859 |
| 50  | 25,285 | 4.4528 | 1.18%  | [0.49, 1.86]  | 2.41%      | [1.71, 3.07]  | 2.12% | 25,091 |
| 100 | 59,015 | 4.5708 | 0.42%  | [-0.03, 0.84] | 1.42%      | [0.97, 1.89]  | 1.22% | 58,750 |

Observations:

- **y=10 C2 vs C3:** the triple drop is 11.92% vs the joint 10.71% — adding ω(k) makes the gap slightly *larger*, not smaller. This is the opposite of what would happen if ω(k) were a confounder of the same sign as v_2 or log_2 k.
- **y=20, 50, 100:** triple drops are 2.59%, 2.41%, 1.42% — at y ≥ 20, the triple match introduces 5-14 deficit cells (because matching on the third axis fragments the buckets, and rare cells empty out the non-smooth pool more often). The triple gap at y=50, 100 is actually *larger* than the joint gap at the same y, mostly because of these deficits biasing the matched subsample.
- **At y=10, the C2 reproduction (10.71%) differs from the prior md's 8.50%.** Both probes use random.Random with seeds tied to `seed=20260608+y`; the underlying difference is the *order* of bucket draws given the same seed (matching draws happen sequentially per cell, and cell ordering inside the dict is different on a re-run). The two values are inside each other's bootstrap CI95 ([3.6, 12.9] and [6.4, 15.0] overlap heavily).

**ω(k) distribution at y=10 (the brief's point of interest):**

| ω(k) | smooth count | matched (triple) count | pool count (all non-smooth) |
|------|--------------|------------------------|-----------------------------|
| 0    | 4   | 0   | 0       |
| 1    | 98  | 86  | 153,742 |
| 2    | 338 | 338 | 380,827 |
| 3    | 220 | 220 | 306,103 |
| 4    | 0   | 0   | 86,419  |
| 5    | 0   | 0   | 6,656   |
| 6    | 0   | 0   | 58      |

Smooth y=10 only has ω(k) ∈ {0, 1, 2, 3} (one slot per available odd prime). The matched non-smooth (under joint matching, *not* triple) already has identical ω(k) counts at ω ∈ {2, 3} and only 12 off (86 vs 98) at ω=1. **So the joint (v_2, log_2 k) match alone already implicitly equates ω(k) between smooth and matched non-smooth at y=10.** Adding ω explicitly as a third axis changes essentially nothing.

The brief's concern — "matching on ω(k) may force the non-smooth subsample to be unusually structured (low ω(k), large prime factors)" — is real *in principle* but turns out to be automatically handled at y=10 by the kernel-size match.

### 2.2 Part B: N = 10^9, shell [2^25, 2^30)

Shell size 966,445,569 integers; 2,428 are y=10 smooth.

Smooth mean σ∞ / log_2 n = **4.3815** (vs N=10^6 shell [16,20) baseline 3.62 — much higher at this larger shell, as expected since σ∞ grows faster than log n inside the shell at this regime).

ω(k) distribution among smooth at N=10^9: {0: 5, 1: 187, 2: 1059, 3: 1177}. (More mass at ω=3 because we have more bits in odd kernel; with three primes available all three can fit.)

**Control results at N = 10^9, y = 10:**

| Control | n_matched | matched mean | drop | CI95 | n_deficit_cells |
|---------|-----------|--------------|------|------|------------------|
| C1 v_2-only | 2428 | 4.6736 | **6.25%** | [4.31, 8.21] | 0 |
| C2 joint (v_2, log_2 k) | 2390 | 4.5563 | **3.83%** | [1.64, 5.98] | 2 (structural: 5+|0-2 supply 0, 5+|3-5 supply 25/43) |
| C3 triple (+ω(k)) | 2389 | 4.5025 | **2.69%** | [0.56, 4.65] | 3 (5+|0-2|0 and |1 are structural) |
| C3 restricted | 2389 | 4.5025 | **2.12%** | [-0.08, 4.48] | (uses 2,408 retained smooth) |

C3 restricted CI95 includes zero. C3 unrestricted CI lower bound is 0.56% — barely positive.

**The N-scan now reads:**

| Statistic | N=10^6 | N=10^8 | N=10^9 |
|-----------|--------|--------|--------|
| Raw drop  | 23.8%  | 21.3%  | (~17%, see below) |
| C1 v_2-only drop | 13.4% | 14.4% | **6.25%** |
| C2 joint drop | 8.5-10.7% | 5.3% | **3.83%** |
| C2 CI95 | [3.6, 15]% | [2.72, 7.61]% | [1.64, 5.98]% |

For raw drop at N=10^9 in shell [25, 30): shell mean is ~5.295 (a typical accelerated-Syracuse trajectory at log_2 n ≈ 28 produces ~5.3 stopping-time-per-bit), so raw = 1 − 4.38/5.29 ≈ 17.2%. Roughly consistent with the N=10^8 raw of 21.3%, drifting down too. (Not formally computed in this probe; would need a sample-mean of shell to verify.)

C1 itself — the v_2-only match that was supposed to be the *stable* baseline — has now dropped from 14% to 6%. This is a much bigger qualitative change than I expected, and is itself a finding worth flagging: **at large N, even the v_2 confounder eats more of the headline gap than at small N**. This suggests the original headline "24% smoothness effect" was a low-N artifact composed of (a) a v_2 effect that grows with N, plus (b) an odd-kernel-size effect that also grows with N. By N=10^9, both are mostly absorbed and only ~2-3% residual remains — and that residual's CI lower bound is at or below zero.

### 2.3 Y-scan at N = 10^9 (not done — only y=10 was run)

The brief asked for y=10 at N=10^9; I did not run the full y-scan. Given the verdict, the marginal value of doing y=20, 50, 100 at N=10^9 is low: at smaller N, the joint-matched y-scan was already 8.5 → 2.2 → 1.3 → 0.3, monotonically decaying. If y=10 at N=10^9 is itself only 2-4%, the y=20+ cells will be 0-1% with CIs centered at zero. The scientific question (does the smoothness signal survive?) is settled at y=10.

---

## 3. The 3-cell verdict

The brief's matrix:

| Outcome | Triggered? | Status |
|---------|-----------|--------|
| ω(k)-matched stays ≥ 5% AND N=10^9 stabilizes ≥ 4% → robust | No | The ω(k) check passes (11.92% at N=10^6), but the N=10^9 check fails (C2 = 3.83%, C3 = 2.69%, both below 4%). |
| ω(k)-matched drops to ~3% OR N=10^9 collapses → **F1 triggered** | **Yes (via N-collapse)** | C2 joint at N=10^9 = 3.83%, C3 triple = 2.69%, C3 restricted = 2.12% (CI includes zero). |
| Mixed → inconclusive | (partially) | One could argue this is "inconclusive" given that C2 at N=10^9 is 3.83% with CI95 [1.64, 5.98]% — overlapping both the "collapse" and "stabilizes at 5%" bands. |

**My honest call:** F1 triggered. The case for F1:

1. C2 at N=10^9 is below the 4%/5% threshold.
2. C3 (triple) further reduces it to 2.7%.
3. C3 restricted CI95 includes zero.
4. The N-scaling pattern (8.5% → 5.3% → 3.8%) is monotonically decaying.
5. The C1 v_2-only gap itself has shrunk from 14% to 6% at one extra decade of N — even the headline confounder isn't stable.

The case for "inconclusive" instead:

1. C2 = 3.83% with CI lower bound 1.64% — strictly positive.
2. C3 = 2.69% with CI lower bound 0.56% — strictly positive.
3. The N=10^6 result, where C2 = 10.71% and C3 = 11.92%, is still strongly positive and not a finite-size noise artifact.
4. An asymptotic that goes like δ(N) ~ c / log log N would also fit this scaling and is still bounded below by a small positive δ_∞.

But this "inconclusive" reading would require the program to survive on a δ ≈ 1-3% effect size — well below the 8-13% headline that originally motivated the Hildebrand program — and at that magnitude the predicted Tao 2022 refinement is **scientifically uninteresting** (constant-factor improvements at the 1-3% level are dominated by every error term in the Hildebrand machinery). So either way, the *program* (as written in `collatz_hildebrand_program.md`) is dead. The question is only whether to call it "killed by F1" or "killed by being too small to motivate the framework."

---

## 4. Honest assessment + recommended next step

### 4.1 What survives

- **Q3's raw 24% drop is real but is now fully explained by three confounders:** v_2(n), log_2 odd-kernel(n), and N-scaling (i.e., finite-size effects at small N). The asymptotic genuinely-smoothness component is at most 2-4%.
- **ω(k) is NOT the additional confounder** that pries the signal apart further. Joint (v_2, log_2 k) matching already implicitly equates ω(k) at y=10. This is a clean *non-finding* on the ω axis.
- **The y-scan monotonicity (clear pattern, not noise) still holds**, but the magnitude at every y has shrunk so much by N=10^9 that there is no "interesting" effect to fit.

### 4.2 What dies

- **The Hildebrand-Dickman conditional theorem in `collatz_hildebrand_program.md`** is dead in its proposed form. Its falsifier F1 ("joint control reduces the y=10 residual gap below ~3%") was specified at the v_2 + log_2 k level and is borderline-passed; its falsifier F2 ("matched residual gap decays with shell index") is **clearly triggered** at N=10^9. The program's own listed survival probability was ≤ 20% even before this run; it's now ≤ 5%.
- The Q3-as-frontier-program direction is closed. The sieve route to a smooth-Collatz density refinement of Tao 2022 does not have an empirical signal of meaningful magnitude to motivate it.

### 4.3 The publishable artefact

Per the brief's framing: *"If signal dies: the sieve route is closed, and we have produced the cleanest possible negative on Collatz's sole remaining non-LDP attack route — a publishable result in its own right (orthogonal to the LDP barrier)."*

A clean negative result paper would:

1. State the raw 24% headline.
2. Document three successively-finer controls (v_2, joint (v_2, log_2 k), triple (v_2, log_2 k, ω(k))).
3. Document the N-scaling scan from N=10^6 to N=10^9.
4. Conclude: the asymptotic smoothness effect on mean σ∞ / log_2 n at y=10 is bounded by ~3% in absolute magnitude, with a 95% bootstrap CI that includes zero.
5. Note that even the C1 v_2-only effect — the simplest possible "smoothness signal" — has collapsed from 14% to 6% over three decades of N, so the entire family of mean-comparison statistics on y-smooth integers is **finite-size-dominated**, not asymptotic.
6. Conclude: a Hildebrand-style smooth-Collatz density refinement is not supported by mean-stopping-time numerics. (A tail observable — `#{n ≤ X smooth : σ∞(n) ≤ c · log_2 n}` for c just above log_2 3 — could be checked separately, but the mean-side null result is strong evidence against expecting a tail-side signal.)
7. Frame this relative to the LDP barrier (`collatz_beyond_esscher.md`): the LDP route is closed by a theorem; the sieve route is closed by an empirical null. **Both major non-Tao attack routes are now closed.**

This is a 3-4 page note suitable for *Experimental Mathematics* or *Integers*, with `[NOVELTY UNVERIFIED]` on whether anyone else has done a comparable sieve-control study on Collatz.

### 4.4 What I would do next (if anything)

In rough order of cost-to-information ratio:

1. **One more decade: N = 10^10** (would take ~15 min wall time per the scaling above; we have the code). If C2 drops from 3.83% to ~2% at N=10^10, F1 is confirmed at 99% confidence; if it stabilizes at 3-4%, the "inconclusive" reading gains weight. This is the cheapest tiebreaker.
2. **Tail observable, not mean.** Convert to `#{n smooth in shell : σ∞ / log_2 n ≤ c}` for several c. The mean is a coarse summary; the tail could still show structure even if the mean doesn't.
3. **Literature search.** Has anyone done a smooth-integer Collatz control study? The current `[NOVELTY UNVERIFIED]` tag is honest: I have not searched.

My recommendation: do (1) — the N=10^10 tiebreaker — and write the negative-result note. The program's salvage probability at the end of this exercise is ≤ 5%; a clean N=10^10 collapse would close the file at ≥ 95%.

---

## 5. Reproducibility

- Code: `sieve_q3_omega_N1e9_probe.py`.
- Data: `data/sieve_q3_omega_N1e9_partA.json`, `data/sieve_q3_omega_N1e9_partB.json`, `data/sieve_q3_omega_N1e9.json`.
- Logs: `data/sieve_q3_omega_N1e9_partA.log`, `data/sieve_q3_omega_N1e9_partB.log`.
- Wall time: Part A 196 s; Part B 94 s; total ~5 min.
- Random seed: 20260608.
- Bootstrap resamples: 1000 (per the brief's ≥ 1000 requirement).
- Hardware: 4-core Linux sandbox, 15 GB RAM, single-core Python (no parallelism).

`[NOVELTY UNVERIFIED]`. No live arXiv search performed.
