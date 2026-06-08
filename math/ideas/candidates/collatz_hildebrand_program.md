# A conditional Hildebrand-style program for smooth-restricted Collatz descent

**Track:** Collatz Vector A — Wave 5 frontier-theory writeup. Builds a
research program around the partially-surviving Q3 smoothness signal of
`sieve_q3_control.md`, using the Hildebrand / Dickman / Tenenbaum
analytic-number-theory framework for `y`-smooth integers.
**Author:** Alex Ye (no AI on the author line per project rules).
**Date:** 2026-06-08.
**Status:** `[CANDIDATE — theory program; entirely CONDITIONAL on the
parallel joint-(v_2, odd-kernel) control test. If that control kills the
~13% residual gap, this program is dead; if it survives, this is a
candidate frontier direction.]` `[NOVELTY UNVERIFIED]`.
**No probe.** This is a theory-program writeup, not a computation.
**Companion files (read-only references; do not modify):**
- `sieve_q3_control.md` — the surviving 13% residual after v_2 matching.
- `sieve_analytic.md` — original Q3 setup and the four sub-probes.
- `collatz_beyond_esscher.md` — the LDP-tractable barrier theorem.
- `natural_density_obstruction.md` — the mod-3 TV floor on the residue side.

---

## 0. Verdict (read first)

> This document is a *conditional* research-program writeup. It builds a
> Hildebrand-style framework around the empirical Q3 smoothness signal
> that survived a first control test (`sieve_q3_control.md`: raw 24%
> drop in mean `σ∞ / log_2 n` on y=10 smooth integers reduced to a
> **13% residual** after v_2(n)-matched-subsample control; the
> residualized-observable control preserves a 29% drop; both controls
> show clean monotone decay in y, supporting "underlying effect is real").
> A finer joint-(v_2, odd-kernel) control is running in parallel.
>
> **The program in one sentence.** If the joint control preserves a
> non-trivial residual effect size δ > 0 (at y = 10, in shell
> `log_2 n ∈ [16, 20)`), then the natural target is a Hildebrand-style
> asymptotic for the restricted counting function
> `M(X, y) := #{n ≤ X : P^+(n) ≤ y AND Col_min(n) ≤ f(n)}` of the
> form `M(X, y) / Ψ(X, y) → 1` (or `→ 1 − exp(−c(δ) · u)`, etc.) with
> controllable rate as `X → ∞` along `u = log X / log y`. This would
> deliver a *smoothness-restricted Collatz density theorem* — a
> genuinely new analytic-NT entry point, weaker than the conjecture
> itself but a real arithmetic refinement of Tao 2022's log-density-1
> result.
>
> **Why the program is conditional and not yet a theorem candidate.**
> Three independent things would have to hold simultaneously:
> 1. The joint-(v_2, odd-kernel) matched control preserves a residual
>    effect (parallel agent's verdict pending).
> 2. The effect scales structurally with N (i.e., the residual gap at
>    N = 10^9 is comparable to or larger than at N = 10^6 — currently
>    unmeasured beyond N = 10^6).
> 3. The Hildebrand saddle-point machinery (`Ψ(X, y) ~ X · ρ(u)` with
>    explicit error terms) can be adapted to a Collatz-indicator-weighted
>    counting function — a non-trivial extension since the indicator
>    `1[Col_min(n) ≤ f(n)]` is not multiplicative.
>
> Only (1) is being decided this week. (2) and (3) are downstream
> contingencies, each capable of independently killing the program.
> Honest paper-readiness: **§7**.
>
> `[NOVELTY UNVERIFIED]`. The Hildebrand–Dickman machinery for `Ψ(X, y)`
> is textbook ANT (Tenenbaum III.5). Its application to a Collatz-side
> counting function is, to my project-context knowledge, new — but I
> have not searched arXiv (403 from this sandbox) for "Collatz Dickman"
> or "smooth Collatz density", and the prior should be that *some*
> sieve-flavored author has at least raised the question.

---

## 1. The empirical hook (recap)

From `sieve_q3_control.md`, on `n ≤ 10^6`, dyadic shell
`log_2 n ∈ [16, 20)`:

- `y = 10` smooth integers (primes from {2, 3, 5, 7}), n_smooth = 660:
  - mean `σ∞ / log_2 n` = 3.618 vs shell baseline 4.751 — raw drop
    **23.8%**.
  - After v_2-bucket matched-subsample control: matched non-smooth mean
    4.180, residual drop **13.4%**.
  - Residualized-observable (subtract `v_2(n)` from `σ∞(n)`) drop **28.8%**.
  - y-scan (matched): **13.4% → 3.5% → 1.6% → 0.4%** for
    y ∈ {10, 20, 50, 100}.

The y-scan monotonicity is the load-bearing piece of "the underlying
effect is real": a pure v_2 artifact under matched control should
fluctuate near zero across y, not show structured monotone decay.

Two open empirical questions whose answers determine whether the program
below is alive:

- **Joint (v_2, odd-kernel) matched control** (running in parallel
  this wave). If matching on `(v_2(n), ⌊log_2(n / 2^{v_2(n)})⌋)` jointly
  kills the 13.4% residual at y = 10, the signal is fully explained
  by the size distribution of the odd kernel and the program below
  collapses.
- **N-scaling.** The probe is at N = 10^6 with only 660 smooth points
  in the shell. A future probe at N = 10^9 will say whether the
  residual gap grows, shrinks, or holds steady; only a non-shrinking
  gap is consistent with a Hildebrand-style asymptotic.

---

## 2. Precise formulation: the restricted counting function M(X, y)

### 2.1 Definitions

Let `P^+(n)` denote the largest prime factor of n, with `P^+(1) = 1`.
The standard smooth-integer counting function is

```
   Ψ(X, y) := #{ n ≤ X : P^+(n) ≤ y },     u := log X / log y.
```

The Hildebrand–Dickman theorem [Hildebrand 1986; Tenenbaum
III.5] gives
```
   Ψ(X, y) = X · ρ(u) · (1 + O_ε(1/log y))
```
uniformly in the range `1 ≤ u ≤ (log y)^{1−ε}`, where ρ is the Dickman
function (the continuous solution of `u ρ'(u) + ρ(u−1) = 0`, `ρ(u) = 1`
on `[0, 1]`). `[CONSTANT UNVERIFIED]` for the precise admissible range
of u — this is the headline asymptotic; the precise uniformity range
involves Saias-style refinements I have not re-derived here.

For a Collatz-friendly observable, define (writing `σ∞(n)` for the total
stopping time of n under the accelerated Syracuse map, and `f` for an
auxiliary threshold function):

```
   M(X, y; f) := #{ n ≤ X : P^+(n) ≤ y AND σ∞(n) ≤ f(log_2 n) }.
```

The most natural choice — matching the Tao 2022 framing
"`Col_min(n) ≤ f(n)`" for a slow function f — is

```
   f(L) = c · L           with c ∈ (log_2 3, log_2 3 + δ_0)   for some δ_0 > 0,
```

where `log_2 3 ≈ 1.585` is the asymptotic mean of `σ∞ / log_2 n`
under the Tao i.i.d. Syracuse heuristic. The Q3 numerics measure the
*mean* of `σ∞ / log_2 n`; the precise observable for a Hildebrand
program is the *tail* `#{n ≤ X : σ∞ / log_2 n ≤ c}`, not the mean.
Conversion between the two requires assumptions about the conditional
variance, which the present probes do not pin down.

### 2.2 What the 13% mean-drop would say about the tail

If on y = 10 smooth n in shell `[16, 20)` the mean of `σ∞ / log_2 n`
is 13% below the shell baseline (after v_2 matching), then under any
unimodal model with bounded variance per shell, the *median*
`σ∞ / log_2 n` on y-smooth n is also depressed — by Markov-style
inequalities, a 13% mean drop with shell baseline ~4.75 corresponds
to a baseline-shift of about 0.62 in raw `σ∞ / log_2 n` units.

For a tail observable, this would translate (under the model:
conditional law of `σ∞ / log_2 n` given (smooth, shell) is
approximately Gaussian with variance comparable to the unrestricted
shell variance) to a **constant-factor enrichment** of the
`{σ∞ / log_2 n ≤ c}` tail at c just above `log_2 3`:

```
   #{n ≤ X : P^+(n) ≤ y, σ∞/log_2 n ≤ c}  /  Ψ(X, y)
       ≳   #{n ≤ X : σ∞/log_2 n ≤ c}  /  X
```
with a multiplicative bonus depending on how far c sits above the
y-smooth conditional mean. **None of these conversions is rigorous** —
they are *predictions* the program would have to substantiate.

### 2.3 The conjectured asymptotic (target)

The cleanest target the program would aim at:

> **Conjecture (Smooth-Collatz Dickman, conditional).** Assume the
> joint-(v_2, odd-kernel) control preserves a non-trivial residual
> effect size δ(y) > 0 at y = 10. Then there exist
> constants c, δ_0 > 0, depending on y, such that, with
> `f(L) = (log_2 3 + δ_0) · L`,
> ```
>    M(X, y; f)  =  Ψ(X, y) · (1 − ε(X, y))
> ```
> with `ε(X, y) → 0` along `u = log X / log y → ∞` at a rate at least
> as fast as the unrestricted Collatz density-zero rate
> `#{n ≤ X : σ∞(n) > f(log_2 n)} / X` from Tao 2022.

The honest weaker form (which is what the empirical signal directly
motivates):

> **Weak form.** With the same hypotheses, the **density of y-smooth
> n ≤ X that fail Col_min(n) ≤ f(n)** is bounded by a constant strictly
> less than the unrestricted Tao 2022 bound, with the constant a
> decreasing function of the surviving effect size δ.

The weak form is the one that does NOT require the saddle-point
machinery of Hildebrand to be adapted; it just packages the empirical
signal as a quantitative refinement.

---

## 3. Connection to Tao 2022

### 3.1 What Tao 2022 says

Tao's theorem (2022): for any function `f(n) → ∞`, the set
`{ n : Col_min(n) ≤ f(n) }` has **logarithmic density 1** in ℕ. This
is the strongest unconditional density result on Collatz.

### 3.2 Does the smoothness signal sharpen Tao 2022?

Two ways the program might intersect Tao 2022:

**(a) Sharper bound on a restricted set.** If one could show
`M(X, y; f) / Ψ(X, y) → 1` *with explicit faster rate* than Tao's
unrestricted rate, that would be a quantitative refinement on a
density-zero subset (y-smooth integers have density zero — by the
Dickman theorem, `Ψ(X, y) / X = ρ(u) → 0` for fixed y as X → ∞).
This is **interesting but NOT a sharpening of Tao 2022 on its own
turf**: Tao gives log-density 1 on a density-1 set; we would be
giving (conditional) log-density 1 on a density-0 subset, possibly
with better rate.

**(b) "Smooth integers behave the same way."** If the conjecture in
§2.3 holds with the same rate as Tao 2022, then the result is "the
smoothness restriction is invisible to Collatz density" — interesting
descriptively (smooth integers are not special for Collatz) but not
a sharpening.

**Honest read of which option the empirical signal supports.** The
Q3 numerics measure the *mean* of `σ∞ / log_2 n` on smooth vs all
n in a shell. The mean is 13% lower on smooth integers (after v_2
match). A *lower mean stopping-time-per-bit* on smooth integers
suggests option (a) — they descend faster — but does not by itself
distinguish "smooth integers are easier" (i.e., M(X, y; f) saturates
faster than the unrestricted analog) from "smooth integers are
smaller-typical-orbit but same-asymptotic-density" (i.e., a constant
shift in the conditional mean but no change in the rate of approach
to density 1).

This is the program's first scientific question: **does the 13%
effect produce a *rate* improvement or a *level* improvement in the
density bound?** The numerics needed to answer this are an N-scan,
not currently available beyond N = 10^6.

### 3.3 Sharper question: is the smooth subset "harder" or "easier" than the full set?

The Q3 sign — smooth integers descend *faster* — says smooth integers
should be **easier** for Collatz than typical n, conditional on size.
This is the right sign to *support* (a) "sharper bound on a restricted
set." If the sign had been reversed (smooth integers descend slower),
the program would be aimed at "smooth integers are a Tao-2022
counterexample candidate," which is a much more dangerous and
less defensible direction.

---

## 4. The conditional theorem skeleton

Below, δ denotes the surviving y = 10 effect size under the
joint-(v_2, odd-kernel) matched control (currently being measured).
The theorem template adapts to the verdict:

**Template (Theorem? — conditional).** Assume:

- (H1) **Signal survival.** δ > 0; specifically, on dyadic shell
  `log_2 n ∈ [L, L+4)` and y = 10, the (v_2, odd-kernel)-matched mean
  of `σ∞(n) / log_2 n` on y-smooth n is at least δ below the matched
  baseline, uniformly for L in a range L ≤ log_2 X − 4.
- (H2) **N-scaling.** δ does not decay to zero as L → ∞; i.e., the
  matched gap is bounded below uniformly in shell.
- (H3) **Hildebrand machinery.** The standard saddle-point
  estimate `Ψ(X, y) = X · ρ(u) · (1 + O_ε(1/log y))` extends to the
  weighted counting function `Ψ_w(X, y; w) := Σ_{n ≤ X, P^+(n) ≤ y} w(n)`
  with `w(n) = 1[σ∞(n) ≤ f(log_2 n)]`, with an error term that does
  not destroy the δ-sized correction.

Then:

> **Conditional Conclusion.** With `f(L) = (log_2 3 + δ_0) · L` for
> some δ_0 > 0 (a function of δ to be determined),
> ```
>    M(X, y; f) / Ψ(X, y)  =  1 − exp(−c(δ) · u) · (1 + o(1)),
>    u = log X / log y,
> ```
> for some `c(δ) > 0` depending on δ (and increasing in δ).

The functional form `exp(−c(δ) · u)` is a *guess* motivated by the
Dickman framework's exponential decay in u; it is one of several
plausible shapes (Saias gives a refined `ρ` with sub-exponential
corrections in some ranges). The honest minimal claim is

> **Minimal conditional claim.** Under (H1)+(H2), the log-density of
> `{n ≤ X, P^+(n) ≤ y : Col_min(n) > f(n)}` *relative to* `Ψ(X, y)`
> is strictly smaller than the corresponding unrestricted log-density
> from Tao 2022 — i.e., a smooth-restricted *quantitative refinement*
> of Tao's bound.

The minimal claim does NOT require (H3) and is therefore the safer
target. The exponential-rate claim is a stretch goal whose feasibility
depends on whether the Hildebrand saddle-point method can absorb the
non-multiplicative weight w(n).

---

## 5. The falsifier

Two clean falsifiers, ordered by what would kill the program first:

**F1 (this week's verdict — joint control).** If the joint
(v_2, odd-kernel) matched control reduces the y = 10 residual gap
from 13% to below ~3% (the y = 20 level — a noise-band threshold
consistent with no genuine smoothness effect), then the program is
dead. The 13% effect was just a finer confounder — the conditional
σ∞ given (size, v_2, odd-kernel-size) is the same whether the
remaining prime factors are small or large. Nothing arithmetic
distinguishes y-smooth n once those three numerical features are
matched.

**F2 (the N-scaling / shell-index falsifier).** If the matched
residual gap *decays with shell index* — e.g., 13.4% at shell
[16, 20), but 5% at [20, 24), 2% at [24, 28) — then the effect is
a finite-size phenomenon, not an asymptotic one, and no Hildebrand
asymptotic applies. **Concretely: if the matched mean-gap satisfies
`g(L) → 0` as `L → ∞`**, then the conjecture in §2.3 fails (its
hypothesis cannot hold). A constant-or-growing g(L) is what the
program needs.

**F3 (the smoothness-monotonicity falsifier).** If the y-scan (under
the joint control) is *not* monotone — e.g., the y=20 matched gap is
larger than the y=10 matched gap — then the effect is not coupled to
smoothness in the Hildebrand sense, and the framework (which is
fundamentally an asymptotic in u = log X / log y) cannot describe it.
The current y-scan (13.4% → 3.5% → 1.6% → 0.4%) is monotone *under
the v_2-only control*; whether it survives joint control monotonically
is a finer check.

Any of F1, F2, F3 kills the program. The current evidence speaks only
to a partial form of "F1 not triggered yet" (v_2-only control was
passed); F2 and F3 require N-scaling and joint-control y-scans not
yet measured.

---

## 6. Connection to the proven barrier (LDP-tractable closure)

The Wave-2 barrier theorem (`collatz_beyond_esscher.md`) closes every
**translation-invariant Gibbs-style reweighting of the i.i.d.
Geom(1/2) base measure** on the Syracuse symbol space `ℤ_+^ℕ` with
finite per-step KL rate. Specifically, no measure ν that is a
joint-stationary Markov reweighting of μ_0 on residues mod 6 can
simultaneously
(a) drive the mod-3^k residue marginal to uniform on (ℤ/3^k)^× for
k ≥ 2, and
(b) achieve drift balance E_ν[a] = log_2 3.

The robustness margin is 0.294 in the relevant gap quantity (per the
team's strengthened theorem).

**Where the Hildebrand-style smoothness program lives relative to
this barrier.** The smoothness restriction `P^+(n) ≤ y` is an
**integer-side** condition on n — it is a property of the prime
factorization of n as an integer, not a property of the Syracuse
valuation sequence `(a_1, a_2, ...)` derived from n's orbit. In
the symbol-space picture, `P^+(n) ≤ y` does NOT factor through any
cocycle of the shift on `ℤ_+^ℕ`:
- It does not factor through finite-d windows of `(a_j)` (it depends
  on the whole integer n, including its multiplicative structure
  *before* the orbit starts).
- It is not translation-invariant (shifting the Syracuse step
  sequence has no canonical effect on `P^+(n)`).
- It is not a Gibbs reweighting of μ_0 (smooth integers form a
  *density-zero* subset, not a tilted measure on the full integers).

Therefore the LDP-tractable barrier does NOT apply: the barrier
proves that a certain class of reweightings cannot give natural
density on the residue side; the smoothness program is a restriction
on the **input set on the integer side** and asks for a smaller
question (density along the smooth subset, not along all of ℕ). The
two live in different categories.

**More precisely**: the barrier theorem is a "no-go for natural
density via measure-side tilts." The Hildebrand program is a
"conditional refinement of Tao 2022 on a measure-zero
integer-side subset." Neither subsumes the other; the smoothness
program does not violate the barrier because it does not attempt
the construction the barrier forbids.

**Honest caveat.** This independence is structural ("the smoothness
condition is integer-side; the barrier closes a measure-side route"),
not a theorem that any smoothness-density argument *automatically*
escapes the barrier. A more sophisticated future program could try
to encode `P^+(n) ≤ y` into a symbol-space cocycle (e.g., via the
arithmetic of the odd kernel mod small primes); such a program could
in principle reactivate the barrier. The minimal Hildebrand-style
program in §2.3 — counting smooth integers with `Col_min(n) ≤ f(n)`
— does not do this and is barrier-free.

---

## 7. Honest assessment of paper-readiness

### 7.1 What this document is

A **theory-program writeup** that packages an empirical signal (the
partly-surviving Q3 smoothness drop) inside a textbook ANT framework
(Hildebrand–Dickman–Tenenbaum) and provides a clean conditional
statement plus three explicit falsifiers. It is NOT a theorem, NOT
a proof, NOT a probe — it is a **frontier-theory candidate** in the
sense of project Wave 5 alt-angles: a precise direction with a clear
go/no-go criterion tied to currently-running computation.

### 7.2 What would make this paper-ready

In rough increasing order of difficulty:

1. **Joint control verdict** (this week): if the parallel agent's
   joint-(v_2, odd-kernel) matched control preserves a δ > 0 gap,
   condition (H1) is supported and the program survives F1.
2. **N-scaling probe** (a couple of CPU-hours at N = 10^9):
   measure whether the matched gap shrinks, holds, or grows with
   shell index. Survival of F2 is necessary.
3. **Joint-control y-scan** (one probe): monotone matched-gap decay
   in y at fixed shell. Survival of F3 is necessary.
4. **Tail observable, not mean.** Convert the present mean-of-`σ∞ /
   log_2 n`-based numerics into a *tail* count `#{n in shell, y-smooth :
   σ∞ / log_2 n ≤ c}` for c just above `log_2 3`. This is the actual
   quantity §2.3's conjecture is about.
5. **arXiv literature search** for "Collatz Dickman", "Collatz smooth
   number", "smooth integer Collatz", "Syracuse smooth", "ψ-Collatz".
   The Hildebrand framework is too obvious not to have been at least
   attempted; the project has not done this search (arXiv 403 from the
   sandbox).
6. **Hildebrand machinery review.** Tenenbaum III.5; Hildebrand 1986;
   Saias refinements. Decide whether the saddle-point method extends
   to a non-multiplicative weighted Ψ_w(X, y; 1[Col_min ≤ f]).
7. **A precise theorem statement, refereeable.** The §4 template is
   too soft; a real paper would need exact uniformity ranges in u,
   explicit error terms, and a proof or proof sketch for the
   conditional conclusion. None of this is done here.

### 7.3 Status as a paper

**This is not a paper.** It is **at most** a "Section 6: Discussion"
in a future paper whose theorems are the §4-template's conditional
conclusions, conditioned on:
- the joint control surviving (F1 not triggered),
- the N-scaling not decaying (F2 not triggered),
- the y-scan staying monotone under joint control (F3 not triggered),
- and an actual analytic result connecting the empirical δ to a
  Hildebrand asymptotic (the real mathematical content, none of which
  is present in this writeup).

Honest count: **0 of 4** of the above are established right now.
The first is being decided this week; the others are downstream
and require months of work each.

### 7.4 The right framing for a paper-shaped artefact

If the joint control survives (F1 not triggered) AND a quick N-scaling
probe shows a non-shrinking gap (F2 not triggered), the immediate
paper-shaped artefact would be a **technical note**:

> "On a smoothness bias in mean Collatz stopping-time-per-bit:
> numerical evidence for y-smooth integers and a conditional
> Hildebrand-style refinement of Tao 2022."

That note would contain:
- The Q3 + control numerics (already done in
  `sieve_analytic.md`, `sieve_q3_control.md`, and the pending
  joint-control probe).
- The §2.3 conjecture, stated cleanly with the §4 conditional theorem
  template.
- The §5 falsifiers, with which-falsifiers-have-been-checked tagged.
- A literature-survey section pinning the position relative to
  Hildebrand 1986, Tenenbaum III.5, Tao 2022, and Lagarias 2010
  survey.
- The §6 barrier-compatibility argument.

Such a note is **publishable as a research announcement / Q-style
note** (e.g., *Experimental Mathematics*, *Integers*) but not as a
theorem paper. The genuine theorem (the §4 conditional conclusion)
is years away.

### 7.5 What the program is worth

- If F1 kills the signal: program dead, document archived as
  "Wave 5 conditional follow-up; refuted." Cost: 0 (the writeup is
  the artefact).
- If F1 survives and F2, F3 are not yet measured: program **alive
  and in the Wave 6 to-do**. The above note becomes the next
  candidate paper.
- If all three falsifiers survive AND the Hildebrand machinery does
  extend: program becomes a real research direction, candidate for a
  full paper or even a small section in a future Collatz survey.

The most honest current estimate: **probability the program survives
all three falsifiers ≤ 20%**, given that the v_2 control already cut
the headline effect in half and the joint control has historically
been the more decisive cut on these kinds of signals.

---

## 8. Citations and references

All citations are project-context level (no live arXiv); precise
constants and uniformity ranges should be re-verified at refereeing
time.

- **Hildebrand 1986**, "On the number of positive integers ≤ x and
  free of prime factors > y", *J. Number Theory* 22 (1986). Saddle-
  point method giving `Ψ(X, y) = X ρ(u) (1 + O_ε(1/log y))` in the
  appropriate range. `[CONSTANT UNVERIFIED]` — the precise uniformity
  range in u depends on whether one uses the original
  Hildebrand estimate or the Saias-style refinement.
- **Tenenbaum**, *Introduction to Analytic and Probabilistic Number
  Theory* (CUP), §III.5 ("Smooth numbers") for the modern treatment.
  Standard reference for ρ(u), `Ψ(X, y)`, and the Dickman–de Bruijn
  framework. `[CONSTANT UNVERIFIED]` — exact section number may have
  shifted between editions.
- **Saias** (early 1990s), refinements of `Ψ(X, y)` asymptotics
  beyond the Hildebrand range. `[CONSTANT UNVERIFIED]`.
- **Tao 2022**, "Almost all orbits of the Collatz map attain almost
  bounded values", *Forum of Mathematics, Pi* 10 (2022). The
  log-density-1 baseline this program would refine on the smooth
  subset.
- **Lagarias 2010 survey**, *The Ultimate Challenge: The 3x+1
  Problem*, AMS. Catalogs prior arithmetic-flavored Collatz
  approaches; would need to be checked carefully for any prior
  smooth-integer-Collatz coupling.

All references are project-context; **arXiv unreachable** from this
sandbox (403). A real lit-search before any paper.

`[NOVELTY UNVERIFIED]` for the entire program. The Hildebrand
machinery is textbook; its application to a Collatz-indicator-weighted
counting function may or may not be original — the prior should
be high (this is an obvious thing to try) that *someone* has at least
raised the question. The conjectural asymptotic in §2.3 with explicit
δ-dependent rate I have not seen written down, but I have not searched.

---

## 9. One-line summary for the team

> Conditional on the joint-(v_2, odd-kernel) control preserving the
> y = 10 residual gap, the natural target is `M(X, y) / Ψ(X, y) → 1`
> with a quantitative δ-dependent rate refining Tao 2022 on the
> y-smooth subset. Falsifiers F1/F2/F3 are precise and tied to
> currently-running or near-future probes. Paper-readiness: **not a
> paper, at best a §6-discussion** in a future note pending joint-control
> verdict; honest survival probability of the full program ≤ 20%.
