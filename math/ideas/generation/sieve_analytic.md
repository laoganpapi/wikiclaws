# Analytic / sieve methods on integer Collatz orbits

**Track:** Collatz Vector A — Wave 5 alt-angle (sieve / analytic number theory).
**Author:** Alex Ye.
**Date:** 2026-06-08.
**Status:** `[CANDIDATE — outcome (b)/(c) mix: two clean nulls (Q1 Euler-product, Q2 Dirichlet pole), TWO non-trivial positive signals (Q3 smoothness, Q4 circle-method exponent 0.83 above √-cancellation)]`. `[NOVELTY UNVERIFIED]`.
**Code:** `sieve_analytic_probe.py`. **Data:** `data/sieve_analytic_probe.json`, `data/sieve_analytic_probe.log`.

---

## 0. Verdict (read first)

> The entire prior alt-angle team has worked inside a measure-theoretic /
> cocycle frame on the symbol space `ℤ₊^ℕ`. This document is the first to
> try **classical analytic / sieve number theory directly on the integer
> sequence `σ∞(n)`**, treating Collatz convergence as an arithmetic
> indicator on `ℕ`. The deliverable is a *concrete probe*, run on
> `n ≤ 10^6` in ~21 seconds (single-core, Python+numpy), that answers four
> questions:
>
> 1. **Multiplicativity of σ∞** on coprime pairs: clean kill of any
>    Euler-product ansatz, but *not* the strong directional kill I had
>    sketched a priori.
> 2. **Partial Dirichlet series** `F_X(s) = Σ_{n ≤ X} σ∞(n) n^{-s}`:
>    saturates cleanly at `s ∈ {2, 3}`, drifts at `s = 1.5`. No clean
>    Riemann-style pole, but the saturation values are arithmetic and worth
>    recording.
> 3. **Smooth-Collatz coupling**: the mean `σ∞(n) / log₂ n` drops from
>    `4.75` (all `n ≤ 10^6`) to `3.70` for `10`-smooth `n` — a **22%
>    speedup**, large and monotonic in smoothness `y`. NOT predicted by the
>    Cramér / LDP frame.
> 4. **Circle-method exponential sum on parity counts**: `max_α |S_α(X)|`
>    decays like `X^{0.83}`, **NOT** the square-root `X^{1/2}` of the null
>    hypothesis. There IS a residual major-arc-like contribution, the best
>    rational `α` is `12/29` at `X = 10^6`, and the exponent `≈ 0.83` is
>    well above the i.i.d. square-root threshold. **Genuinely surprising**.
>
> ### Headline measurements (n ≤ 10^6):
>
> | Probe | Quantity | Value (X = 10^6) |
> |-------|----------|------------------|
> | Q1 | mean `Δ(a,b) = σ∞(ab)−σ∞(a)−σ∞(b)` on coprime pairs | `−5.43` |
> | Q1 | median `Δ` | `−5` |
> | Q1 | fraction `Δ < 0` | `0.534` |
> | Q1 | regression `Δ` vs `log min(a,b)`, slope / R² | `0.842` / `0.0003` |
> | Q2 | `F_X(s) / Z_X(s)` at `s = 3.0` (converged) | `2.5526` |
> | Q2 | same at `s = 2.0` (converged) | `5.2105` |
> | Q2 | same at `s = 1.5` (drifting) | `12.09 →` ? |
> | Q3 | mean `σ∞/log₂ n` unrestricted | `4.7499` |
> | Q3 | same on `10`-smooth `n` | `3.6952` (22% lower) |
> | Q3 | same on `50`-smooth `n` | `4.4561` (6% lower) |
> | Q4 | `max_α |S_α|/X` at `X = 10^6`, `q ≤ 30` | `0.0982` |
> | Q4 | best fraction at `X = 10^6` | `12/29` |
> | Q4 | implied exponent `log|S|/log X` | `0.832` |
>
> **Plausibility (1–5): 2.5**, *up from my a-priori estimate of 2*. The Q4
> exponent `0.83 > 0.5` is unexpected and the smoothness signal Q3 is
> bigger than expected. Both deserve a 10^9-scale follow-up.
>
> See §5 for full honest assessment, including the most likely *failure
> mode* of the Q4 signal (parity-count finite-mean concentration causing
> spurious major-arc concentration at small `q`).

---

## 1. Why this angle escapes the prior barriers

The Wave-2 LDP-tractable barrier (`collatz_beyond_esscher.md`) closes every
**translation-invariant Gibbs-style reweighting of the Bernoulli base
measure** `μ₀` on the symbol space `ℤ₊^ℕ` with finite per-step KL rate.
Every prior alt-angle (representation theory, automorphic, nilmanifold,
operator algebras, sum-product, etc.) eventually reduces to a *measure on
symbols*, and so falls inside the Wave-2 frame.

The four objects above are NOT measures on the symbol space. They are
*functions on `ℕ` indexed by integer arithmetic*:
- `σ∞(n)` is an arithmetic function in the classical sense.
- `F(s) = Σ σ∞(n) n^{-s}` is a Dirichlet series on `ℕ`, not on a shift space.
- `ψ_C(X, y)` is a smoothness density, an object of ANT.
- `S_α(X) = Σ_{n ≤ X} e(α · P(n))` is a Hardy–Littlewood
  exponential sum indexed by `n`, not by the cylinder events of `μ₀`.

The reduction "measure on symbols ↦ density on integers" goes one way:
every Gibbs measure on `ℤ₊^ℕ` gives a density on integers via Tao's coupling,
but **not every integer-indexed sum is the pushforward of a symbol measure**.
Specifically, the Dirichlet series weights `n^{-s}` and the smoothness
indicator `1_{P^+(n) ≤ y}` *do not factor through the symbolic dynamics*.

**Comparison to the three prior structural kills:**
- **Mod-3 rigidity** (Tao 2022 / the project's transfer operator): asymmetric
  stationary `π_n` on `(ℤ/3ⁿℤ)ˣ`. This is a constraint on a *finite mod-3ⁿ
  marginal*. Our probes Q1–Q4 do not touch any mod-3 marginal: the
  multiplicative structure, the Dirichlet series, the smoothness
  filtration, and the parity-count exponential sums all live on the integer
  side and ignore mod-3.
- **LTE rigidity** (sum-product alt-angle): `ord_{3ⁿ}(2) = 2·3ⁿ⁻¹` forces
  full-orbit doubling structure mod `3ⁿ`. This concerns `2`-orbits in
  `(ℤ/3ⁿℤ)ˣ`. Our Q1 (multiplicativity of `σ∞`) and Q3 (smoothness) are
  *Z-side* objects and bypass LTE entirely. Q4 *could* interact with
  LTE through the parity word (which encodes mod-3 information via the
  Syracuse offset), but the major-arc concentration we observe is at
  denominator `q = 29`, coprime to `2·3` — no obvious LTE coupling.
- **3-adic blindness** (p-adic / Berkovich heights): the `3`-adic completion
  loses the integer ordering that drives the stopping-time question. Our
  probes use the *full integer structure*, including the archimedean
  ordering `n ≤ X`, so the 3-adic blindness does not apply.

Additionally, the angle escapes the LDP-tractable barrier specifically
because (Q3) and (Q4)'s positive signals do not factor through any
shift-invariant Gibbs reweighting:
- Smoothness `P^+(n) ≤ y` is a *non-shift-invariant* condition on `n`,
  not on the Syracuse word.
- The major-arc fraction `12/29` is a denominator coprime to the entire
  Tao mod-`3ⁿ` story; it is a Diophantine feature of the *integer side*,
  not the symbol side.

---

## 2. The four sub-direction objects in precise form

### (Q1) Multiplicativity defect

Define the **multiplicativity defect** of `σ∞` on coprime pairs:
```
   Δ(a, b) := σ∞(ab) − σ∞(a) − σ∞(b),   gcd(a, b) = 1.
```
If `σ∞` were additive on coprime pairs (the natural analog of "completely
multiplicative" for an additive arithmetic function), one would have `Δ ≡ 0`.

### (Q2) Partial Dirichlet series

Define
```
   F_X(s) := Σ_{n ≤ X, n ≥ 2} σ∞(n) · n^{-s},   s ∈ (1, ∞).
   Z_X(s) := Σ_{n ≤ X, n ≥ 2} n^{-s}.
```
The ratio `F_X(s) / Z_X(s)` is the `n^{-s}`-weighted mean of `σ∞(n)`.
A stable ratio in `X` would suggest meromorphic continuation analogous to
`Σ d(n) n^{-s} = ζ(s)²`. A drifting ratio suggests divergence near `s = 1`.

### (Q3) Smooth-Collatz density

For smoothness parameter `y` and threshold `X`, define
```
   M(X, y) := mean_{n ≤ X, P^+(n) ≤ y}  (σ∞(n) / log₂ n).
```
The question: does `M(X, y) → C_y` with `C_y` strictly less than the
unrestricted mean `M(X, ∞) ≈ log₂ 3 + (lower order)`?

### (Q4) Circle-method exponential sums on parity counts

For each `n`, let `P(n) ∈ ℤ₊` be the number of odd-parity steps in the
accelerated Syracuse orbit (`P(n)` = the number of times we apply
`m → (3m+1)/2`). Define
```
   S_α(X) := Σ_{n ≤ X, n ≥ 2} e(α P(n)),   e(x) := exp(2πi x).
```
The circle-method question: is `max_α |S_α(X)| ≫ X^{1/2 + ε}` (residual
major arc), or is `max_α |S_α(X)| = O(X^{1/2})` (square-root cancellation)?

---

## 3. First probe — results

Run on `n ≤ 10^6`, wall time `21 s`, single-core, Python + numpy. Detailed
output in `data/sieve_analytic_probe.log`, JSON in
`data/sieve_analytic_probe.json`.

### Q1: multiplicativity defect

- 5000 coprime pairs `(a, b)` sampled uniform in `[2, 10^4]`.
- Mean `Δ = −5.43`, median `−5`, std `≈ 47`, range `[−356, 280]`.
- Sign distribution: `53.4%` negative, `< 0.5%` zero, `46.1%` positive.
- Regression `Δ ~ log(min(a,b))`: slope `0.84`, **R² = 0.0003** — i.e.,
  no detectable linear correlation between `Δ` and the size scale.

**Interpretation.** `σ∞` fails additivity on coprime pairs with a bias
`E[Δ] < 0` (`σ∞(ab)` tends to be *smaller* than `σ∞(a) + σ∞(b)`), but
the failure is **not size-dependent** in the regression sense, and the
sign is only mildly skewed (53/46). The "orbits merge" cartoon I sketched
a priori was qualitatively right (`Δ < 0` on average) but quantitatively
weaker than expected.

**Consequence for Euler products.** Any Dirichlet-convolution / Euler-product
identity would require `σ∞(ab) = σ∞(a) + σ∞(b)` on coprime pairs (since
`σ∞` is *additive* in spirit), i.e., `Δ ≡ 0`. With mean `−5.43` and std
`47`, the additive structure is decisively absent: **no Euler product**.

### Q2: partial Dirichlet series

`F_X(s) / Z_X(s)` for `s ∈ {1.5, 2.0, 3.0}` and `X ∈ {10^2, ..., 10^6}`:

| s | X = 10² | 10³ | 10⁴ | 10⁵ | 10⁶ |
|---|---------|-----|-----|-----|------|
| 1.5 | 7.516 | 10.209 | 11.402 | 11.895 | 12.092 |
| 2.0 | 4.685 | 5.134 | 5.201 | 5.209 | 5.211 |
| 3.0 | 2.545 | 2.553 | 2.553 | 2.553 | 2.553 |

- `s = 3.0`: converged to `2.5526` by `X = 10^4`. `s = 2.0`: converged to
  `5.2105` by `X = 10^5`. `s = 1.5`: still drifting at `X = 10^6`,
  consistent with `F(s)` having a singularity at `s = 1` (since
  `σ∞(n) ~ log₂(3) log₂ n`, so `F(s) ~ ζ'(s−0)` style behavior near
  `s = 1`).
- **No clean pole structure**: the limit values `2.5526` and `5.2105` do
  not match any simple `ζ`-function expression I can identify in 30 sec
  of mental algebra. No Riemann hypothesis analog.

### Q3: smooth-Collatz density

`y`-smooth integers `n ≤ 10^6`:

| y | # smooth n | mean σ∞/log₂n | drop vs unrestricted |
|---|------------|---------------|----------------------|
| 10 | 1272 | **3.695** | −22.2% |
| 50 | 32 875 | 4.456 | −6.2% |
| 100 | 72 270 | 4.574 | −3.7% |
| 500 | 250 686 | 4.659 | −1.9% |
| 1000 | 344 298 | 4.684 | −1.4% |
| ∞ | 999 999 | 4.750 | — |

**This is the most striking signal.** Smooth integers descend monotonically
*faster* than typical, by 22% at `y = 10`. The Cramér / LDP frame does NOT
predict this — under the i.i.d. parity heuristic `σ∞(n) ~ log₂(3) log₂ n`
plus mean-zero noise, smoothness should be invisible because the
Syracuse map mixes residues mod every modulus coprime to 6.

**Why might smoothness help?** A speculative non-rigorous reason: smooth
integers `n` are typically small *products of small primes*, hence have
*more compact 2-adic expansion structure* under the multiplicative-by-3
flow, and their orbits join the "highway" of repeated `→ 1` descent
faster. But this is heuristic; the genuinely arithmetic-NT question is
whether `M(X, y)` admits a Hildebrand-Tenenbaum-style asymptotic
expansion in `u = log X / log y`.

### Q4: circle method on parity counts

`max_α |S_α(X)| / X` over Farey fractions `α = p/q`, `1 ≤ q ≤ 30`,
`gcd(p,q) = 1` (excluding `α = 0`):

| X | max\|S\|/X | best frac | exponent log\|S\|/log X |
|---|----------|-----------|--------------------------|
| 10² | 0.7706 | 1/30 | 0.943 |
| 10³ | 0.4349 | 1/30 | 0.880 |
| 10⁴ | 0.2067 | 1/30 | 0.829 |
| 10⁵ | 0.1010 | 1/30 | 0.801 |
| 10⁶ | 0.0982 | **12/29** | 0.832 |

**Surprising:** the exponent is `≈ 0.83`, not `0.5`. The null (i.i.d.
parity count, mean grows linearly in `σ∞(n) ~ log n`) would predict
square-root cancellation `|S_α| = O(X^{1/2} (log X)^c)`.

**The honest caveat** (probable failure mode of this signal): `P(n)` has
**bounded variance per `n`** if conditioned on `log n`, and the parity
count `P(n)` is concentrated around `log₂(3)/log₂(3) · log₂ n = log₂ n`
(roughly). When all `P(n)` cluster in a narrow band, `e(α P(n))` for
small denominator `α` aligns coherently across many `n`, producing a
**spurious major-arc signal** that has nothing to do with arithmetic
structure. The exponent `0.83 → ?` could drift to `0.5` at much larger
`X`, or it could stabilize, indicating a real signal.

**Mitigation idea (NOT done in this probe):** subtract the *mean* and
*standard deviation* per dyadic shell, then re-do the exponential sum on
the centered, normalized parity count. If the exponent then drops to
`0.5`, the signal is heuristic concentration. If it stays above `0.5`,
it is genuine.

---

## 4. Why this angle is genuinely novel (snippet-search flag)

I have NOT executed a live web search inside this session; the following
is from project context and standard ANT knowledge:

- **Tao 2022 (Almost all orbits attain almost-bounded values)** uses
  harmonic analysis on `(ℤ/3ⁿℤ)ˣ` (Fourier on a *finite group*), NOT
  classical sieves and NOT the integer-side machinery (Dirichlet series,
  Dickman, circle-method on integer orbits).
- **Lagarias (1985, 1990, 2010 surveys)** discusses arithmetic structure
  of orbits, but to my knowledge does not present the explicit
  multiplicativity defect statistic `Δ(a, b)` or the smoothness-coupling
  signal.
- **Dickman / smooth-number techniques applied to Collatz**: I am not
  aware of any. `[NOVELTY UNVERIFIED]`
- **Hardy–Littlewood circle method on the integer parity-count
  exponential sum `S_α(X) = Σ e(α P(n))`**: I am not aware of any prior
  treatment. `[NOVELTY UNVERIFIED]`
- **Tao's harmonic-analysis frame is "on the residue side"**; the
  classical-Vinogradov circle method "on the integer side" is genuinely
  distinct.

Honest note: I am *not certain* about the literature; a follow-up should
include a careful arXiv search for "Collatz Dickman", "Collatz smooth
number", "3n+1 Hardy-Littlewood", "Collatz exponential sum", "Syracuse
parity Dirichlet". All four phrases I would expect to return very few or
zero hits, but I have not verified this here.

---

## 5. Plausibility, failure modes, honest assessment

**Plausibility (1–5): 2.5.**

### What worked

- Q3 (smoothness) gave a clean, monotonic, large signal not predicted by
  the LDP frame.
- Q4 (circle method) gave an exponent `0.83` above the square-root null,
  which is surprising if it survives the centering correction.

### Failure modes

- **Q1 / Q2 kills are textbook negatives**: no Euler product, no clean
  Dirichlet pole. These close two of the four standard ANT routes.
- **Q3's smoothness signal might be an integer-density artifact**: y-smooth
  integers are *less dense* and *more clustered near small n*; small `n`
  have smaller `σ∞`, so the comparison should be *stratified* by `log n`.
  If the gap survives stratification, Q3 is real. If not, it is the trivial
  "smooth numbers are small" artifact. **Not yet done.**
- **Q4's exponent `0.83` is the most likely candidate for a spurious
  signal**: parity-count concentration around `log₂ n` could explain the
  coherent alignment at small `q`. The decisive test is the centered,
  per-dyadic-shell normalised exponential sum; **not yet done**.
- **The whole angle remains a long shot**: even a genuine Q3+Q4 signal
  does not give a density theorem by itself. The route to a proof would
  require:
  - For Q3: a Hildebrand-style asymptotic `M(X, y) ~ ρ_C(u)` with explicit
    `ρ_C`, plus a Tao-style decomposition `M(X, ∞) = ∫ M(X, y) dμ(y)`.
  - For Q4: a Vinogradov-style minor-arc bound `|S_α| = O(X^{1−δ})` for
    `α` away from small-denominator fractions, plus a major-arc analysis
    that recovers the density of `n` with `σ∞(n)` in a given range.
  Both are *years* of additional work and require expert ANT review.

### Best-case scenario

- Q3 survives stratification → a "smooth-Collatz Dickman theorem"
  becomes a candidate research problem.
- Q4 survives centering → "Collatz parity sums have a non-trivial major
  arc at denominator `q ≈ √log X`" becomes a candidate observation.
- Neither *proves* the Collatz conjecture, but they would be the **first
  genuinely classical-ANT entry points** into the problem.

### Most likely scenario

Outcome (b)/(c) mix: Q1, Q2 are *clean structural kills* of two of the
four standard ANT routes (decisive, even if negative). Q3 and Q4 give
*partial positive signals* that are mostly explained by simple
artifacts (size stratification for Q3, parity concentration for Q4) and
fade under proper normalisation. Net: useful diagnostic, low probability
of breakthrough.

`[NOVELTY UNVERIFIED]` for all four sub-questions.

### Concrete follow-up plan (1 week, NOT executed here)

1. **Scale Q3 to `N = 10^9`** with explicit stratification by `log n`
   in deciles. If the smoothness gap persists in each decile, the signal
   is real.
2. **Q4 centering**: compute `P̃(n) := (P(n) − μ(log₂ n))/σ(log₂ n)` using
   the existing `10^7` trajectory data, then re-run `S_α(X) = Σ e(α P̃(n))`.
   If `max_α |S_α|/X` drops to `X^{−1/2}` exponent, signal is artifact.
   If it stays at exponent `> 1/2`, the signal is real.
3. **arXiv lit search** for the four NT phrases listed in §4 to confirm
   `[NOVELTY UNVERIFIED]` status.
4. **Q1 follow-up**: stratify the regression `Δ ~ log min(a,b)` by
   *residue class* of `a` and `b` mod 6. The mod-3 stationary `π_n` may
   leak into `Δ` through arithmetic constraints on coprime pairs.

`[NOVELTY UNVERIFIED]` overall.
