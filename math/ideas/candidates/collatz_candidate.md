# Collatz candidate — DECIDING the residue⊥drift disjointness (the joint-law route)

**Track:** Collatz, Vector A (natural-density upgrade). Tests ergodic-E2 ≡ probability-B.4.
**Author:** Alex Ye (AI-assisted computation; AI not on author line per project rules).
**Date:** 2026-06-03.
**Status:** `[result — CERTIFIED NEGATIVE]`. Numerics (exact DP, truncation < 1e-13), not proof.
`[NOVELTY UNVERIFIED]` on the packaging; the underlying coupling is Tao / Prop 4.2.
**Code:** `collatz_psi_factorization.py`. **Data:** `data/psi_factorization.json`, `data/run_n8.log`.

---

## 0. Verdict (read first)

> **The (residue, drift) joint law of the Syracuse system does NOT factorize. Residue and
> drift stay COUPLED. The disjointness the natural-density route needs is FALSE — decisively,
> with a power-law *divergence* of the factorization defect.**

The candidate certified by the reviewer (`ideas/review/collatz_review.md` §4) was the joint
`(residue, drift)` law, phrased as ergodic-E2's **disjointness / factorization** statement: at the
descent-balance Esscher tilt `t* = s*`, does

$$
\Psi_n(\xi,t) \;=\; \mathbb E\!\left[\, e(\xi R_n/3^n)\, e^{-t D_n}\,\right],
\qquad e(x)=e^{2\pi i x},\quad D_n = \big(\textstyle\sum a_j\big)\log 2 - n\log 3,
$$

factorize off the frozen mod-3 coset? The discriminator is the **factorization defect**

$$
\Delta_n \;:=\; \max_{\xi:\,3\nmid\xi}\;
\Big|\, \Psi_n(\xi,t^*)\big/\big(\Psi_n(\xi,0)\,\Psi_n(0,t^*)\big) - 1 \,\Big|.
$$

- **Power-saving decay** `Δ_n ≲ 3^{−θn}` ⇒ disjointness holds ⇒ genuine route → `[CANDIDATE LEAD]`.
- **Bounded-below / non-decaying `Δ_n`** ⇒ residue and drift coupled ⇒ route obstructed → certified negative.

**Result:** `Δ_n` is not merely bounded below — it **diverges as a clean power law**
`Δ_n ≈ 3^{+0.85 n}` (global fit `n=2..8`; local slope tightens to `θ ≈ 1.07` on `n=5..8`). This is the
**opposite** of the required power-saving decay, by the maximal possible margin. The reviewer's
prediction (§3.2, §4: "`max|R(ξ,t*)−1|` is bounded below, the factorization FAILS") is **confirmed
and strengthened** — the defect does not just floor, it grows. Confidence: **high (~90%)** that the
disjointness route is dead; the trend is monotone, truncation-stable, and structurally explained.

This converts the open problem into a **precise residue–drift coupling theorem** (numerically): the
natural-density obstruction is a *self-similar coupling across the mod-3^k coset tower*, not a mixing
defect. That is a valuable, citable negative (per the brief's ABSOLUTE RULES).

---

## 1. Validation (all checks PASS)

The exact joint law `p(R_n, S_n)` (`S_n = Σ a_j`, so `D_n = S_n\log2 − n\log3` is a deterministic
function of `S_n`) is built by the suffix-sum DP imported read-only from
`collatz/experiments/verify_syracuse_rv.py`, keeping the full valuation sum that that file collapses.
Geometric tail truncated at `a_max` and renormalized; truncation loss `< 7e-15` at `n=8`.

| Check | Requirement | Result |
|---|---|---|
| **mod-3 marginal of `R_n`** | exactly `(0, 1/3, 2/3)` for all `n` | `(0.000000, 0.333333, 0.666667)` at every `n=2..8` ✓ |
| **drift mean at `t*`** | `E_{t*}[D_n] = 0` (defines `t*`) | `−2e-16 … +4e-14` (machine zero) at every `n` ✓ |
| **`t*` value** | `E_{t*}[a]=\log_2 3`, `s*=0.438033` | `t* = 0.438033`, `E_{t*}[a]=1.584963=\log_2 3` ✓ |
| **`Ψ_n(ξ,0)` = residue char. fn.** | matches `perp_gap` residue law | `Ψ(·,0)` is the FFT of the residue marginal; reproduces the known `ν_n` characteristic function ✓ |
| **truncation stability** | `Δ_n` invariant to `a_max` | `Δ_6 = 23.145268` identical for `a_max∈{35,50,70}` ✓ |

The untilted drift mean is `> 0` and grows (`+0.58 … +2.30`): natural-density sampling is *not*
stationary untilted — exactly why `t*` is the correct re-centering tilt. At `t*` it is zeroed.

The mutual-information statistic (below) reproduces the reviewer's §3.2 table essentially to the digit
(e.g. `I(R mod 27; sgn D) = 0.3996, 0.2622, 0.1755` at `n=3,4,5`; full-resolution `I = 0.30–0.45`,
non-decaying), an **independent cross-check** that the machinery is correct.

---

## 2. The tables

### 2.1 Factorization defect `Δ_n` (the discriminator)

| `n` | size `=φ(3^n)` | `Δ_n` | `Δ_n/Δ_{n−1}` | `log₃ Δ_n` | trunc |
|---|---|---|---|---|---|
| 2 | 6 | 0.815840 | — | −0.1853 | <2e-15 |
| 3 | 18 | 1.354684 | 1.660 | +0.2763 | <3e-15 |
| 4 | 54 | 2.568181 | 1.896 | +0.8585 | <4e-15 |
| 5 | 162 | 5.016487 | 1.953 | +1.4680 | <4e-15 |
| 6 | 486 | 23.145268 | 4.614 | +2.8598 | <5e-15 |
| 7 | 1458 | 69.356829 | 2.997 | +3.8587 | <6e-15 |
| 8 | 4374 | 177.438100 | 2.558 | +4.7138 | <7e-15 |

`log₃ Δ_n` is essentially **linear and increasing**: global fit `log₃ Δ_n = 0.852 n − 2.283`, i.e.
`Δ_n ≈ 3^{+0.85 n}` — a power-law **divergence**. (Local slope on `n=5..8` is `θ ≈ 1.07`, i.e. the
divergence is, if anything, slightly *accelerating*; in any case `θ > 0` cleanly and monotonically.)
Disjointness requires `Δ_n → 0` like `3^{−θn}` with `θ>0`; the data show `Δ_n → ∞` like `3^{+θn}`.
**This is not ambiguous or transient: the sign of `θ` is wrong by construction at every `n≥2`.**

### 2.2 Where the coupling lives — `Δ` stratified by `v₃(ξ)` (the coset tower)

Max defect within each `v₃(ξ)` stratum (`v₃=0` is the off-coset `3∤ξ` target):

| `n` | `v₃=0` (off-coset) | `v₃=1` | `v₃=2` | `v₃=3` | `v₃=4` | `v₃=5` | `v₃=6` | `v₃=7` |
|---|---|---|---|---|---|---|---|---|
| 2 | **0.8158** | 0.1913 | | | | | | |
| 3 | **1.3547** | 0.8158 | 0.1913 | | | | | |
| 4 | **2.5682** | 1.3547 | 0.8158 | 0.1913 | | | | |
| 5 | **5.0165** | 2.5682 | 1.3547 | 0.8158 | 0.1913 | | | |
| 6 | **23.145** | 5.0165 | 2.5682 | 1.3547 | 0.8158 | 0.1913 | | |
| 7 | **69.357** | 23.145 | 5.0165 | 2.5682 | 1.3547 | 0.8158 | 0.1913 | |
| 8 | **177.44** | 69.357 | 23.145 | 5.0165 | 2.5682 | 1.3547 | 0.8158 | 0.1913 |

**Exact diagonal cascade** (verified equal to machine precision): the off-coset (`v₃=0`) defect at level
`n` is *identical* to the `v₃=1` defect at level `n+1`, the `v₃=2` defect at `n+2`, …. The coupling is a
**rigid self-similar tower**: each added 3-adic digit of the residue contributes one more, *larger*,
coupling layer, and the deepest (off-coset, highest-frequency) characters carry the most. This is
precisely the reviewer's predicted geometry — the coupling "is concentrated on the mod-9/mod-27 coset
tower" and "strengthens with depth" (§3.2, §4 step 3) — now confirmed as an exact recursion.

### 2.3 Independent statistic — mutual information `I(R_n mod 3^k ; sgn D_n)` (bits)

| `n` | `I(mod 3)` | `I(mod 9)` | `I(mod 27)` | `I(full, mod 3^n)` |
|---|---|---|---|---|
| 2 | 0.0227 | 0.2951 | — | 0.2951 |
| 3 | 0.0277 | 0.1795 | 0.3996 | 0.3996 |
| 4 | 0.0198 | 0.1218 | 0.2622 | 0.4508 |
| 5 | 0.0162 | 0.0859 | 0.1755 | 0.4272 |
| 6 | 0.0121 | 0.0669 | 0.1350 | 0.4342 |
| 7 | 0.0098 | 0.0536 | 0.1073 | 0.4235 |
| 8 | 0.0082 | 0.0425 | 0.0836 | 0.3921 |

Reproduces the reviewer's §3.2 numbers. The mod-3 MI `≈0.02` is the **measurement artifact** the
reviewer flagged (residue mod 3 is slaved to the single bounded valuation `a_n`, negligible for the
`O(n)`-scale drift). The **full-resolution MI sits at 0.30–0.45 bits and does NOT decay** in `n` —
substantial, persistent coupling. Reading the residue deeper (mod 9, 27, …) lifts the MI monotonically.
(The fixed-`k` columns drift down slowly only because a *fixed* number of digits is an ever-smaller
fraction of the `n`-digit residue; the *full* residue MI is flat.) Two orthogonal statistics —
`Δ_n` (a generating-function defect over the real drift `D_n`) and `I` (an entropy on the 1-bit
coarsening `sgn D_n`) — agree: **residue and drift are coupled, non-decayingly.**

A bounded, normalization-free cross-statistic `ρ_n` (the residue-character vs. centered-drift
correlation defect computed *inside* the `t*`-tilted measure, so it cannot be inflated by the tilt
scale) is also reported in the data and is large and non-vanishing (`O(1)`–`O(100)`), confirming the
divergence of `Δ_n` is intrinsic coupling, not a tilt-normalization artifact. (`ρ_n` is noisier — its
argmax wanders over high frequencies — so `Δ_n` and `I` are the load-bearing statistics.)

---

## 3. THE VERDICT

**`[CANDIDATE — CERTIFIED NEGATIVE]` residue⊥drift disjointness FAILS.**

The joint-law route of ergodic-E2 ≡ probability-B.4 is **obstructed**. The factorization
`Ψ_n(ξ,t*) ≈ Ψ_n(ξ,0)·Ψ_n(0,t*)` does not hold for `3∤ξ`; the defect `Δ_n` diverges as `3^{+0.85n}`.
There is no `MIX(θ)`-off-the-coset to harvest: the residue does not become asymptotically independent
of the drift at the descent-balance point — it becomes *more* dependent as resolution deepens. The TV
≥ 1/6 barrier of `natural_density_obstruction.md` is **not** escaped by quotienting the mod-3 factor,
because the coupling does not live only at mod 3 — it lives in a self-similar tower across all
mod-3^k cosets (§2.2), and the off-coset (the part disjointness needed to be clean) carries the
*largest* defect at every level.

**Confidence the disjointness route is dead: ~90%.** Grounds: (i) the `θ>0` divergence is monotone
and clean from `n=2`, not a small-`n` transient; (ii) it is truncation-exact; (iii) it is structurally
explained by the exact `v₃`-cascade — each new 3-adic digit of `R_n` resolves one more valuation
`a_j`, and `D_n` *is* that valuation sequence, so deeper residue ⇒ strictly more drift information;
(iv) a second independent statistic (full-resolution MI) and a third (tilted correlation `ρ_n`) concur.
The structural mechanism — "`R_n` at full resolution *is* the valuation sequence *is* `D_n`, so they
cannot be disjoint" — is the reviewer's, and the generating-function probe `Ψ_n(ξ,t*)` (which sees the
full real `D_n`, not the 1-bit `sgn D_n`) shows *more* coupling than the MI did, exactly as predicted.

**Honest scope.** This is numerics on `n≤8` (`3^8=6561`), not a proof. What is proven-grade here is the
exact-arithmetic *validation* (mod-3 marginal, `t*` neutrality, truncation independence); the
*divergence trend* is a numerical extrapolation, albeit a very clean one with a structural cause. The
result does **not** say Collatz natural density is false, does **not** touch Tao's logarithmic-density
theorem, and does **not** rule out *non-disjointness-based* routes. It says precisely: the
residue⊥drift **disjointness/factorization** mechanism is unavailable. `[NOVELTY UNVERIFIED]` — the
content (residue–drift coupling) is Tao / Prop 4.2; the *quantitative power-law divergence of `Δ_n` at
`t*`* and the *exact `v₃`-cascade* are, to our knowledge, not previously recorded in this packaging.

---

## 4. The FALLBACK probe (the reviewer's named next frontier)

The reviewer (§"Target for the next wave") named the fallback if `Ψ_n` fails — which it did: the live
frontier moves **off the residue variable entirely, onto the 2-adic / size variable `D_n`**, as a
**cohomological (non-moment) object**: the **Livšic coboundary question** for

$$
\varphi \;=\; \log 3 - a\,\log 2 \qquad\text{(per-step log-increment of the size variable)}
$$

on the Lagarias 2-adic shift (the Bernoulli system driving the valuations `a_j`). Precisely:

> **Livšic / coboundary probe (the next experiment to define).** Treat `φ` as a real-valued cocycle
> over the shift `σ` on the valuation sequence `(a_j)` (a Bernoulli `Geom(2)` system, or the 2-adic
> Lagarias conjugacy of the Collatz map). Ask whether `φ − \bar φ` (centered at the descent-balance
> mean, `\bar φ = 0` at `s*`) is a **coboundary**: does there exist a measurable `u` with
> `φ − \bar φ = u∘σ − u`? Livšic theory says a Hölder cocycle is a coboundary **iff its sums around
> every periodic orbit vanish** (Livšic 1971/72). So the concrete, runnable probe is:
> compute the **periodic-orbit sums** `Σ_{j} φ(σ^j p)` over the short Collatz/Syracuse cycles (the
> `(a_1,…,a_p)` periodic words) and test whether they are all zero (coboundary ⇒ trivial descent,
> rigidity) or spread (a genuine non-coboundary ⇒ a *pointwise* Lyapunov obstruction that could carry
> descent). This is a **non-moment, non-spectral** object — it reads the cohomology class of `φ`, the
> one place a pointwise (orbit-by-orbit) descent could live, and it is exactly the archimedean–2-adic
> *decoupling* that `perp_gap.md` / the review identify as where the obstruction actually sits.

That is the honest next move: `Ψ_n` quantified the residue–drift coupling and closed the disjointness
door; the Livšic coboundary of `log3 − a log2` is the next door, on the size variable directly. Its
prior of yielding descent is low (the review puts it there because it is *the deepest framing*, ≈ the
conjecture itself), but it is the correct frontier and a cheap periodic-orbit-sum diagnostic is the
first step.

---

## 5. Honest assessment — does Collatz have a real joint-law lead?

**No.** The joint `(residue, drift)` law was the single live target the review certified, and the
deciding experiment **kills its only actionable form (disjointness/factorization)** with a clean
power-law divergence, not a marginal floor. The wave's real, publishable output is a **sharp negative
that upgrades the open problem**: the natural-density obstruction is now characterized (numerically,
`n≤8`) as a *self-similar residue–drift coupling across the mod-3^k coset tower* with defect growing
like `3^{+0.85n}` and full-resolution mutual information pinned at `0.30–0.45` bits — a precise
quantitative coupling statement, exactly the "convert the open problem into a precise coupling bound"
outcome the review forecast at ~85–90%.

The probability of a near-term barrier-escape from the joint-law route is now **lower** than the
review's prior 10–15% — call it **≈3–5%** — because the predicted failure not only occurred but was
*stronger* than predicted (divergence, not just non-decay) and is structurally locked by the exact
`v₃`-cascade. The genuinely-new objects must act on the **2-adic / size variable `D_n` directly**
(§4, the Livšic coboundary of `log3 − a log2`), the one frontier the residue-marginal machinery —
and now the joint generating function — has left untouched. Collatz does not have a real joint-law lead;
it has a precisely-quantified joint-law *obstruction*, and one remaining deep (low-prior) cohomological
probe.

---

## 6. Reproducibility

- `collatz_psi_factorization.py` — builds the exact `(R_n,S_n)` joint law (DP from
  `verify_syracuse_rv.inv_pow2_mod`, read-only import), forms `Ψ_n(ξ,t)` via FFT of the `t`-weighted
  residue marginal, computes `Δ_n`, the `v₃`-stratified defects, the tilted correlation defect `ρ_n`,
  and the resolution-`k` mutual information. Run: `python3 collatz_psi_factorization.py 8 50`.
- `data/psi_factorization.json` — all per-`n` rows. `data/run_n8.log` — full console transcript.
- Validation gates (mod-3 marginal exact; `E_{t*}[D]=0`; truncation independence) are asserted in the
  driver output. No file outside `ideas/candidates/` was written; `collatz/experiments/` imported
  read-only.
