# Collatz — the Livšic coboundary of the drift cocycle: a COHOMOLOGICAL NEGATIVE

**Track:** Collatz, the next-wave fallback after the joint-(residue,drift) disjointness route was
certified NEGATIVE (`collatz_candidate.md`). Moves OFF the residue variable onto the 2-adic/size
variable, as the reviewer + prior deep-dive named.
**Author:** Alex Ye (AI-assisted computation; AI not on author line per project rules).
**Date:** 2026-06-03.
**Status:** `[CANDIDATE — CERTIFIED NEGATIVE]`. The non-coboundary core is **proof-grade** (an exact
closed form, not an extrapolation); the distributional characterization is exact combinatorics.
`[NOVELTY UNVERIFIED]` — cocycle/Livšic views of Collatz may exist; see §6.
**Code:** `collatz_livsic_probe.py`. **Data:** `data/livsic_probe.json`.

---

## 0. Verdict (read first)

> **The Collatz drift cocycle `φ = log3 − a·log2` on the Syracuse valuation shift is NOT a
> coboundary.** Its periodic-orbit sums do not vanish — they are an *unbounded, diffusively spreading*
> family `Σψ = (2p − S)·log2` (centered), with a clean **proof-grade** witness: the constant-word
> period-`p` orbits give `Σψ = p(2−c)·log2`, which is linear in `p` and nonzero for every valuation
> `c ≠ 2` (the all-ones word `→ +p·log2`, the all-threes word `→ −p·log2`). By Livšic's theorem the
> drift class `[φ]` is **nontrivial in H¹**: there is **no** bounded/continuous transfer function `ψ`
> with `φ − φ̄ = ψ∘σ − ψ`. **The drift cannot be trivialized into a continuous Lyapunov/conjugacy of
> this form — a rigid cohomological obstruction.**

This is the *expected* outcome given the archimedean/2-adic decoupling diagnosis
(`function_field.md` §4): the obstruction that the function-field analog *removes* (there the
multiplier and divisor share one place, so the analogous cocycle telescopes to a coboundary — degree
is a Lyapunov) is exactly the obstruction that survives over `ℤ`, and we now name it precisely: the
drift cocycle is a **non-trivial cohomology class**. The decoupling IS the non-vanishing of the
periodic sums.

**Confidence: very high (~98%) on the negative**, because the non-coboundary is not numerics — it is a
two-line exact computation (the constant-word witness is rigorous). The 2% is reserved only for the
`[NOVELTY UNVERIFIED]` flag and the modeling choice of "which cocycle" (§1, addressed).

**Honest scope (read with the verdict).** A non-coboundary kills exactly **one** class of argument —
"trivialize the drift by a continuous coboundary, exhibiting a pointwise Lyapunov/conjugacy." It says
**NOTHING** about whether Collatz is true. The on-average descent (`φ̄ < 0`) is untouched and is what
all probabilistic routes (Tao) actually use; those do **not** need `φ` to be a coboundary. See §4.

---

## 1. The cocycle and the system (and why this is the right object)

### 1.1 The system

Via the Syracuse encoding (Lagarias's `Q`-conjugacy of the Collatz map to a 2-adic shift), the
Collatz dynamics on **odd** integers is conjugate to the one-sided shift `σ` on the space of
**2-adic valuation sequences**
$$
a = (a_1, a_2, \dots), \qquad a_j = \nu_2(3x_j + 1) \in \{1, 2, 3, \dots\},
$$
where `x_{j+1} = (3 x_j + 1)/2^{a_j}` is one Syracuse (odd→odd) step. The natural
("descent-balance") shift-invariant measure is the i.i.d. **Geometric(1/2)** product law
`P(a = k) = 2^{−k}` (mean `2`) — this is precisely the Syracuse random variable's driving law of
`natural_density_obstruction.md` §1 and Tao's model. We work on this Bernoulli shift `(({1,2,…})^ℕ, σ, μ)`.

> **Why the Syracuse-valuation shift, not the raw accelerated-`T` parity shift.** The two encodings
> carry the *same* drift but the valuation shift is the natural Livšic object: it is Bernoulli (i.i.d.
> geometric), genuinely shift-invariant, and its cocycle is Hölder (here: a *function of finitely many
> coordinates* — in fact one coordinate — hence trivially Hölder/locally constant, the cleanest case
> for Livšic). The raw `{n/2, (3n+1)/2}` parity shift bundles the deterministic even-steps with the
> odd-steps; folding the even-steps into the valuation `a_j` is exactly the acceleration that makes the
> system i.i.d. and the cocycle a clean function of `a`. (`function_field.md` §4 identifies the
> archimedean magnitude × 2-adic valuation *mixing* as the source of difficulty; the valuation shift is
> the coordinate that carries the 2-adic valuation, so it is where a coboundary trivialization, if it
> existed, would have to live.)

### 1.2 The cocycle

One Syracuse odd-step `x → (3x+1)/2^{a}` changes the log-magnitude by, to leading order
(the `+1` contributes `O(1/x) → 0`),
$$
\boxed{\;\varphi(a) \;=\; \log 3 \;-\; a\,\log 2\;}\qquad\text{(the DRIFT COCYCLE, nats).}
$$
It is a 1-coboundary candidate over `σ`: it depends on the single coordinate `a = a_1` (locally
constant ⇒ Hölder of every exponent). Its mean is
$$
\bar\varphi \;=\; \mathbb E_\mu[\varphi]
\;=\; \log 3 - (\mathbb E[a])\log 2
\;=\; \log 3 - 2\log 2
\;=\; (\log_2 3 - 2)\,\log 2 \;<\; 0,
$$
i.e. **`−0.41504` in `log₂` units per odd step** (`= log₂3 − 2`), the known Syracuse descent rate.
The accelerated-`T` per-step rate is half this, `(log₂3 − 2)/2 = −0.20752` (because there are on
average `ā = 2` parity-steps per odd step), matching `digit_lyapunov.md` §4 exactly. The centered
cocycle is `ψ := φ − φ̄`.

### 1.3 Validation (all checks PASS — exact arithmetic)

| Check | Requirement | Result |
|---|---|---|
| **`E[a]`** | `= 2` (Geom(1/2) mean) | `2.0000000000`, err `2.2e-16` ✓ |
| **`E[φ]` nats** | `= log3 − 2log2 = −0.2876820725` | `−0.2876820725`, err `5.6e-17` ✓ |
| **`E[φ]` log₂** | `= log₂3 − 2 = −0.4150375` (per odd step) | `−0.4150375` ✓ |
| **acc-`T` rate** | `(log₂3 − 2)/2 = −0.2075187` | matches `digit_lyapunov.md` §4 ✓ |
| **trivial cycle {1,2}** | `Σφ = −Λ`; centered `Σψ = 0` | `Σφ = −0.2876821 = −Λ` ✓; `Σψ = 0` (machine) ✓ |
| **`Σφ = −Λ` on real cycles** | matches `cycles.py` fixed points | all `match = True` (read-only cross-check) ✓ |
| **centered mean per period** | `= 0` exactly | `0.000000` at every `p` (amax=30) ✓ |

The cocycle's ergodic average reproduces the known drift `(log₂3 − 2)/2 < 0`; the trivial cycle
`{1,2}` is the period-1 word `(a) = (2)` (`ν₂(3·1+1) = ν₂(4) = 2`), giving `Σφ = log3 − 2log2 = −Λ`
and centered `Σψ = 0` exactly. **Both required validation gates pass.**

---

## 2. The periodic-orbit sums (the Livšic obstruction set)

### 2.1 The closed form — periodic sums *are* the telescoping `Λ`

A period-`p` point of `σ` is a cyclic valuation word `(a_1, …, a_p)`. The uncentered cocycle sum is
$$
\Sigma_\varphi \;=\; \sum_{j=1}^p \varphi(a_j) \;=\; p\log 3 - S\log 2,
\qquad S := \sum_{j=1}^p a_j .
$$
With `K = p` odd steps and total halvings `S`, this is **exactly** `Σφ = K log3 − S log2 = −Λ`, where
`Λ = S log2 − K log3` is the telescoping invariant of `cycle_bound_attempt.md` Thm 3
(`Λ = Σ ε_j`). *The Livšic periodic-orbit sums of the drift cocycle ARE the cycle-equation two-log
forms `Λ`.* A genuine nontrivial Collatz cycle would be a periodic orbit with `Σφ = 0` (`2^S = 3^K`),
which is impossible — recovering "no nontrivial cycle" as the `Σφ = 0` slice. The **finer** Livšic
question is the *distribution* of the `Σφ` (equivalently centered `Σψ`), not just whether any equals 0.

The **centered** periodic sum has an even cleaner closed form. Since `φ̄ = log3 − 2log2`,
$$
\boxed{\;\Sigma_\psi \;=\; \Sigma_\varphi - p\,\bar\varphi
\;=\; (p\log3 - S\log2) - p(\log3 - 2\log2)
\;=\; (2p - S)\,\log 2.\;}
$$
**The centered periodic sum is `(2p − S)·log2`: it measures, in `log₂` units, how far a word's total
halving count `S` deviates from its expected value `2p`.** It is an *integer multiple of `log2`* —
the obstruction lives on a lattice.

### 2.2 The distribution vs period (exact combinatorics, amax=30)

`Σψ = (2p − S)·log2` and `S` is a sum of `p` i.i.d. Geom(1/2) (mean 2, **variance 2**), so in `log₂`
units `Σψ/log2 = 2p − S` has mean `0` and variance `Var(S) = 2p`, i.e. std `= √(2p)`. The exact
weighted distribution (DP over `S`, geometric tail truncated at `a ≤ 30`, renormalized):

| `p` | mean (log₂) | std (log₂) | min | max | `P(Σψ = 0)` | support |
|---|---|---|---|---|---|---|
| 1 | 0.0000 | 1.4142 | −28 | 1 | 0.25000 | 30 |
| 2 | 0.0000 | 2.0000 | −56 | 2 | 0.18750 | 59 |
| 3 | 0.0000 | 2.4495 | −84 | 3 | 0.15625 | 88 |
| 4 | 0.0000 | 2.8284 | −112 | 4 | 0.13672 | 117 |
| 5 | 0.0000 | 3.1623 | −140 | 5 | 0.12305 | 146 |
| 6 | 0.0000 | 3.4641 | −168 | 6 | 0.11279 | 175 |
| 7 | 0.0000 | 3.7417 | −196 | 7 | 0.10474 | 204 |
| 8 | 0.0000 | 4.0000 | −224 | 8 | 0.09819 | 233 |
| 9 | 0.0000 | 4.2426 | −252 | 9 | 0.09274 | 262 |
| 10 | 0.0000 | 4.4721 | −280 | 10 | 0.08810 | 291 |
| 11 | 0.0000 | 4.6904 | −308 | 11 | 0.08409 | 320 |
| 12 | 0.0000 | 4.8990 | −336 | 12 | 0.08059 | 349 |
| 13 | 0.0000 | 5.0990 | −364 | 13 | 0.07749 | 378 |
| 14 | 0.0000 | 5.2915 | −392 | 14 | 0.07472 | 407 |

- **`std = √(2p)`** exactly (e.g. `p=2 → √4 = 2.000`, `p=8 → √16 = 4.000`): the periodic sums
  **spread diffusively** — the classic CLT signature of a non-coboundary (a coboundary would have
  `Σψ ≡ 0`, std `= 0`, at every `p`).
- **`P(Σψ = 0) = P(S = 2p)` decays like `~1/√(4πp)`** (local CLT): the "balanced" orbits become a
  vanishing fraction — `0.250 → 0.075` over `p = 1..14`, `→ 0`.
- **Support spreads linearly**: `max − min ≈ 29p` (since `a_j ∈ [1, 30]`), unbounded with `p`.

### 2.3 The proof-grade non-vanishing (not numerics)

The constant-word period-`p` orbits give a closed, exact, unbounded family:
$$
\text{word } (c,c,\dots,c):\quad S = pc,\quad \Sigma_\psi = (2p - pc)\log 2 = p(2-c)\,\log 2.
$$
For every valuation `c ≠ 2` this is nonzero and **grows linearly in `p`**:
$$
\text{all-ones } (1)^p:\ \Sigma_\psi = +p\log 2 \to +\infty;
\qquad
\text{all-threes } (3)^p:\ \Sigma_\psi = -p\log 2 \to -\infty.
$$
So the periodic sums are **not all zero** (only `c = 2`, the trivial-cycle valuation, balances) and
are **unbounded**. This is a two-line exact argument, not an extrapolation — it is the proof-grade
core of the negative.

---

## 3. THE VERDICT — non-coboundary / cohomological negative

**`[CANDIDATE — CERTIFIED NEGATIVE]`: the drift cocycle `φ = log3 − a log2` is NOT a coboundary.**

Livšic's theorem (Livšic 1971/72): a Hölder cocycle over a hyperbolic / mixing shift is a coboundary
(`ψ = u∘σ − u` for continuous/Hölder `u`) **iff all periodic-orbit sums vanish**. Here:

1. The periodic sums do **not** vanish — `Σψ = (2p − S)log2`, with the proof-grade constant-word
   witnesses `Σψ = p(2−c)log2 ≠ 0` for `c ≠ 2` (§2.3).
2. They are **unbounded** (linear in `p`), so not even a *bounded* coboundary plus constant exists:
   any `u` with `φ − φ̄ = u∘σ − u` would satisfy `u(σ^p x) − u(x) = Σψ → ±∞` on constant-word orbits,
   forcing `u` unbounded.
3. Hence `[φ] ≠ 0` in `H¹(σ, ℝ)`: the drift is a **non-trivial cohomology class**.

**Consequence:** there is **no continuous/Hölder Lyapunov of the form `φ = ψ∘σ − ψ + φ̄`** — i.e. the
drift cannot be conjugated to its constant mean by a continuous transfer function. The single missing
ingredient that would have trivialized descent (a bounded `ψ` turning per-step drift into an exact
telescoping coboundary, making `log x_n − ψ(orbit)` a monotone-on-average-to-pointwise Lyapunov) **does
not exist**. The route is rigidly obstructed.

**Confidence: ~98%.** The non-coboundary is an exact computation (the witness is rigorous, not
`n ≤ N` numerics); the distributional shape (`std = √(2p)`, lattice support, `P(Σψ=0) ~ p^{−1/2}`) is
exact combinatorics. The residual 2% is the `[NOVELTY UNVERIFIED]` flag and the (defended, §1) choice
of cocycle/system.

> **Distinguishing "provably spreads" from "couldn't reach large `p`"** (per ABSOLUTE RULES): this is
> the former. We do not rely on a finite-`p` table to *infer* spreading — the spreading is the
> closed-form identity `Σψ = (2p − S)log2` with `Var(S) = 2p`, and the non-vanishing is the exact
> constant-word family. The table (§2.2) merely *exhibits* the proven shape; it is not the evidence.

---

## 4. What this says about the decoupling — and what it does NOT say about Collatz

### 4.1 It names the archimedean/2-adic decoupling *cohomologically*

`function_field.md` §4 diagnosed: over `𝔽₂[T]` the multiplier `(T+1)` and the divisor `T` act at the
**same** (non-archimedean) place, so the per-step degree-change cocycle telescopes to `0` and degree is
a Lyapunov (convergence is provable). Over `ℤ`, the `3n+1` step's archimedean magnitude (`×3`) and the
2-adic halving (`÷2^a`) live at **different** places and are not tied by an identity. This file converts
that diagnosis into a precise theorem:

> **The 𝔽₂[T] degree cocycle is a coboundary (periodic sums vanish: every polynomial reaches a fixed
> point, the analog of `Σψ ≡ 0`); the ℤ drift cocycle `log3 − a log2` is NOT (periodic sums spread,
> `[φ] ≠ 0` in H¹).** The archimedean/2-adic *decoupling* IS the non-triviality of the drift cohomology
> class. The two valuations being "decoupled" means precisely that `S` (the 2-adic data) fluctuates
> around `2p` with variance `2p` *independently* of being forced to equal `p·log₂3` (the archimedean
> balance) — and that fluctuation is the non-zero `Σψ`.

This matches the companion negative (`collatz_candidate.md`): the joint `(residue, drift)` route died
because "`R_n` at full resolution **is** the valuation sequence **is** `D_n`." Here the *same*
valuation sequence, viewed as the cocycle's argument, has a non-trivial cohomology class — the residue
route and the cohomology route are two faces of the one decoupling.

### 4.2 What a non-coboundary does NOT say (honest scope)

- **It does NOT disprove Collatz.** Coboundary-ness is a property of *one trivialization strategy*, not
  of the conjecture. A cocycle can be a non-coboundary while the dynamics still converges.
- **It does NOT touch the on-average descent.** `φ̄ = (log₂3 − 2)/2 < 0` is intact and is what Tao's
  logarithmic-density theorem and every probabilistic descent argument actually use. Those arguments
  need `φ̄ < 0` and *mixing/equidistribution*, **not** `φ` to be a coboundary. Non-coboundary is fully
  compatible with (indeed *typical* for) a system whose ergodic average gives descent.
- **It is, in fact, the GENERIC situation.** A non-degenerate real-valued cocycle over a Bernoulli
  shift is generically a non-coboundary (coboundaries are a meagre/measure-zero exceptional set); a
  non-constant cocycle with `Var > 0` *cannot* be a coboundary (a coboundary has zero asymptotic
  variance, but here the CLT variance is `2·(log2)² > 0` per step). So this negative was structurally
  forced — which is exactly why it is a clean, citable *obstruction* rather than a surprise.

In one line: **the drift cocycle is non-trivial in H¹, so no continuous-coboundary Lyapunov exists;
this obstructs one (pointwise-trivialization) class of argument and leaves the on-average descent and
every mixing-based route entirely intact.**

---

## 5. Honest assessment — and whether a further fallback exists

**Is there a real lead here?** No — this is the negative the decoupling predicted, now made
proof-grade and cohomologically precise. It is the *deepest* of the framings (the review placed it as
"≈ the conjecture itself"), and it closes cleanly: the drift class is non-trivial in H¹, so the
"trivialize-the-drift-by-a-bounded-coboundary" door is shut by a rigid (not numerical) obstruction.

**Does a further fallback exist?** The coboundary question was the *last* of the structured frontiers
the reviewer + prior deep-dive named on the size variable. Honest options remaining, in decreasing
prior:

1. **Asymptotic-variance / CLT route (open, mixing-based, NOT obstructed here).** The non-coboundary
   gives `σ² = Var(Σψ)/p = 2(log2)² > 0`: the drift satisfies a non-degenerate CLT. A *quantitative*
   descent bound (e.g. an effective stopping-time tail via the cocycle's large-deviation rate function,
   the Esscher tilt of `collatz_candidate.md` §1) does **not** need a coboundary — it needs only the
   rate function `I(0)` and a mixing/equidistribution input. This is morally Tao's route and is **not**
   killed; it is where the on-average descent already lives. The Livšic negative tells us *not* to look
   for a pointwise trivialization and *to* invest in the large-deviation/equidistribution side.
2. **Transfer-operator (Ruelle/thermodynamic) spectral gap** for the tilted cocycle — the `transfer_operator*.py`
   experiments in `collatz/experiments/` already probe this; the cocycle's pressure function `P(t)` and
   its zero at the descent-balance tilt are the natural next object. (Non-coboundary ⇒ `P` is strictly
   convex, `P'' = σ² > 0`, consistent.)
3. **Beyond that, the framings on `ℤ` are exhausted** at the structured level: residue (joint-law,
   dead), magnitude/digit Lyapunov (dead, `digit_lyapunov.md`), and now cohomology (dead). What remains
   is the genuinely hard analytic core — effective equidistribution of the Syracuse map (Tao's `β=1`
   neighborhood), which no cheap diagnostic decides.

**Bottom line.** The Livšic probe delivers a clean, proof-grade **cohomological negative**: `[φ] ≠ 0`
in H¹, no continuous-coboundary Lyapunov, the archimedean/2-adic decoupling named as the
non-triviality of the drift class. It obstructs the pointwise-trivialization class of argument and
**only** that; the on-average descent and the mixing/large-deviation route (where Tao's theorem lives)
are untouched and are the correct remaining frontier. Collatz does not gain a lead from this wave; it
gains its sharpest statement yet of *why* the size variable resists pointwise control.

---

## 6. Novelty, reproducibility, scope

`[NOVELTY UNVERIFIED]`. **Cocycle / Livšic / thermodynamic-formalism views of Collatz plausibly exist**
(the Syracuse map as a skew-product, Lagarias's 2-adic conjugacy, and the cycle two-log form `Λ` are
all classical; reading `Λ` as a Livšic periodic-orbit sum is a short step). We have **not** located a
reference stating "the drift cocycle is a non-coboundary / `[φ] ≠ 0` in H¹" in this packaging, but it
is elementary enough to be folklore. We claim no priority on the *fact*; the contribution is the
**explicit identification** `(Livšic periodic sums) = (the cycle-equation `Λ` forms)` and the exact
distributional characterization `Σψ = (2p − S)log2`, `std = √(2p)`, tying the cohomology negative to
the existing cycle-exclusion and decoupling work. A prior-art pass (Lagarias survey; ergodic-theory
treatments of `3x+1`; Möller / Matthews skew-product literature) should close the flag.

**Reproducibility.**
- `collatz_livsic_probe.py` — defines `φ`, validates the mean (exact, `< 6e-17`) and the trivial
  cycle `{1,2}` (`Σφ = −Λ`, `Σψ = 0`), tabulates the periodic-sum distribution by a DP over `S`
  (geometric tail at `amax`, renormalized), gives the proof-grade constant-word witnesses, and
  cross-checks `Σφ = −Λ` against `cycles.py` fixed points (read-only import). Run:
  `python3 collatz_livsic_probe.py 14 30`.
- `data/livsic_probe.json` — all rows + verdict.
- No file outside `ideas/candidates/` written; `collatz/experiments/cycles.py` imported read-only.

**Validation gates (both required by the brief, both PASS):** (i) the cocycle's mean reproduces the
known average drift `(log₂3 − 2)` per odd step `= (log₂3 − 2)/2` per accelerated step; (ii) the trivial
cycle `{1,2}` gives `Σφ = −Λ` and centered `Σψ = 0`. Asserted in the driver.

**What is proof-grade vs numerical.** Proof-grade: the closed form `Σψ = (2p − S)log2`, the constant-word
non-vanishing/unboundedness, hence the non-coboundary verdict and `[φ] ≠ 0` in H¹. Exact combinatorics:
the full distribution (`std = √(2p)`, lattice support, `P(Σψ=0) ~ p^{−1/2}`). Nothing here is an
`n ≤ N` extrapolation.
