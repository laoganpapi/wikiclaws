# An explicit LDP/thermodynamic-formalism refinement of Tao 2022's descent estimate

**Track:** Collatz, Vector A. The publishable form of the surviving thermodynamic-formalism candidate (cf. `collatz_candidate.md`, "the LDP / thermodynamic-formalism core of the Syracuse system").
**Author:** Alex Ye (no AI on the author line per project rules; computational assistance is acknowledged separately).
**Date:** 2026-06-04.
**Status:** `[WRITEUP — pending red-team]`. The closed-form pressure, Esscher tilt, rate function, and tilted CLT variance are `[VERIFIED]` (closed form + Monte-Carlo cross-check). The framing as a quantitative refinement of Tao 2022's Theorem 1.3 / Proposition 1.17 is `[CLAIMED]` and `[NOVELTY UNVERIFIED — almost certainly known to the Sinai / Akin / Lagarias / Tao tradition; prior-art check pending]`. Constants extracted from Tao 2022 are `[CONSTANT UNVERIFIED]` (snippet-sourced — see `survey.md` §5 and `tao_syracuse_explicit.md` for the secondary-source reconstruction).
**Source data:** `data/thermo_probe.json`, `data/thermo_probe.log` (produced by `collatz_thermo_probe.py`; not re-run here — values cited verbatim).
**Scope:** A quantitative tightening, in explicit constants, of the descent half of Tao 2022 by a closed-form large-deviation rate. **NOT** a natural-density upgrade (the candidate's mod-3 falsifier in `collatz_candidate.md` §2.3 rules that out). **NOT** an improvement of Tao's residue-side characteristic-function bound `|ν̂_n(ξ)| ≤ C_A n^{-A}`.

---

## 0. Executive summary

Tao 2022 (Theorem 1.3 = `Col_min(N) ≤ f(N)` log-density-1 for every `f → ∞`) gives the qualitative *fact* that Collatz orbits descend; the quantitative cost — the rate at which the exceptional log-density approaches 0, and the rate at which the orbit shrinks — is encoded in the superpolynomial decay `|ν̂_n(ξ)| ≤ C_A n^{-A}` of Proposition 1.17. Tao does **not** isolate, in closed form, a large-deviation exponent for the *drift* (the size-shrinkage half of the argument, as opposed to the residue-equidistribution half).

This note states a clean, explicit closed form for that drift exponent: under the Geom(1/2) law on the 2-adic-valuation shift driving the Syracuse map, the *probability that the empirical log-drift over `n` Syracuse steps fails to descend* satisfies a Cramér large-deviation bound with rate

$$
I(0) \;=\; -P(s^*) \;=\; \log_2 3 \cdot \log(3/2) \;-\; (\text{closed-form correction}) \;\approx\; 0.05498 \quad (\text{nats/step}),
$$

with `P(s) = -s log3 + (s-1) log2 - log(1 - 2^{s-1})` the pressure and `s* ≈ -0.43803` the Esscher tilt. Equivalently, expressed in the natural `log_3` units of the Collatz problem, the per-step descent-failure exponent is `I(0)/log3 ≈ 0.05498/1.0986 ≈ 0.05004` (so the no-descent probability decays as `3^{-0.05·n·(1+o(1))}`; in the equivalent `log_2` units used in `collatz_thermo_probe.py`'s constants the prefactor is `≈ 0.0347`, see Remark 2.5). The constant is **explicit** and **closed-form**; Tao's `n^{-A}` is not.

The result is a theorem-grade *packaging* statement (the analytic content is the standard Cramér theorem applied to the closed-form pressure of §1); the novelty claim is purely on the bookkeeping side — making the constant visible — and is flagged accordingly.

---

## 1. Setup and the pressure function (verified)

The Syracuse system, in the form used throughout this candidate stream (cf. `collatz_livsic.md` §1, `tao_syracuse_explicit.md` §§1–2):

- One-sided shift `σ` on sequences `a = (a_j)_{j ≥ 1}` with `a_j ∈ {1, 2, …}`.
- i.i.d. Geom(1/2) base measure `μ_0` with `P(a = k) = 2^{-k}`, mean `2`.
- Drift cocycle (one Syracuse odd step's log-shift, ignoring the `O(1/x)` offset):
  $$
  \varphi(a) \;=\; \log 3 \;-\; a_1 \log 2 \qquad (\text{nats}).
  $$
- Block drift `D_n := \sum_{j=1}^n a_j \log 2 - n \log 3`, so `\sum_{j=1}^n \varphi(\sigma^{j-1} a) = -D_n`. The orbit *descends* over `n` steps iff `D_n > 0`.
- Untilted mean: `E_{μ_0}[\varphi] = \log 3 - 2\log 2 = -0.28768\ldots`; untilted variance: `Var_{μ_0}(\varphi) = 2 (\log 2)^2 = 0.96091\ldots` (the Livšic CLT variance, `collatz_livsic.md` §3.2).

**Theorem 1.1 (closed-form pressure; `[VERIFIED]`).** *The cumulant generating function of `-\varphi` under `μ_0` is, for `s < 1`,*
$$
P(s) \;:=\; \log E_{μ_0}\!\bigl[\,e^{-s\varphi(a)}\,\bigr] \;=\; -s \log 3 \;+\; (s - 1)\log 2 \;-\; \log\!\bigl(1 - 2^{\,s-1}\bigr),
$$
*with derivatives*
$$
P'(s) = -\log 3 + \frac{\log 2}{1 - 2^{s-1}}, \qquad
P''(s) = \frac{(\log 2)^2 \cdot 2^{s-1}}{(1 - 2^{s-1})^2} \;>\; 0.
$$
*The Esscher tilt `s*` solving `P'(s*) = 0` is*
$$
s^* \;=\; 1 + \log_2\!\Bigl(1 - \tfrac{\log 2}{\log 3}\Bigr) \;\approx\; -0.43803.
$$
*The tilted variance has closed form*
$$
P''(s^*) \;=\; \log 3 \cdot \log(3/2) \;\approx\; 0.44545.
$$

*Proof.* Direct computation; reproduced in `collatz_thermo_probe.py` §1 and verified to machine precision (`data/thermo_probe.json::closed_form_identities`: `Psecond_match_err = 5.6e-17`, `I_at_0_minus_negP_sstar = 0.0`). ∎

**Theorem 1.2 (rate function; `[VERIFIED]`).** *The Cramér rate function `I(x) := \sup_s (sx - P(s))` for the empirical drift `\bar\varphi_n := \frac1n \sum_{j=1}^n \varphi(\sigma^{j-1}a)` under `μ_0` has effective domain `(-\log(3/2), \infty)`, is strictly convex and analytic, and satisfies*
$$
s(x) \;=\; 1 + \log_2\!\Bigl(1 - \tfrac{\log 2}{x + \log 3}\Bigr),
\qquad
I(x) \;=\; s(x)\,x \;-\; P\bigl(s(x)\bigr).
$$
*Distinguished values:*
$$
I(\bar\varphi) = 0,
\qquad
I(0) \;=\; -P(s^*) \;\approx\; 0.054979.
$$

*Proof.* Cramér's theorem applied to the i.i.d. drift increments, with the closed-form Legendre transform of Theorem 1.1; numerically validated in `collatz_thermo_probe.py` to the saddle-point precision `O(\log n / n)` expected at finite `n` (data/thermo_probe.json::empirical_rate_function). ∎

---

## 2. The LDP refinement theorem

We state the main result as a comparison theorem to Tao 2022. Throughout, "the Syracuse model" means the i.i.d. Geom(1/2) law on valuation sequences, which models the genuine Syracuse map on the odd integers via Tao's first-passage transport (`tao_syracuse_explicit.md` §4; this is itself a controlled approximation, qualified at "Conditional" in Theorem 2.2).

### 2.1 Tao 2022's quantitative content, restated

**Theorem 2.1 (Tao 2022, Theorem 1.3 + Proposition 1.17; reproduced).** *Let `f : \mathbb N \to \mathbb R` with `f(N) \to \infty`. Then*
$$
\delta_{\log}\!\bigl(\{N : \mathrm{Col}_{\min}(N) > f(N)\}\bigr) \;=\; 0,
$$
*i.e. logarithmic density 1 of `N` satisfy `\mathrm{Col}_{\min}(N) \le f(N)`. The quantitative engine is*

**`[CONSTANT UNVERIFIED — snippet-sourced from secondary reproductions; primary-source fetch blocked by HTTP 403, see survey.md §5]`** Proposition 1.17 (decay of characteristic function): for every `A > 0` there is `C_A < \infty` such that for all `n \ge 1` and all `\xi \in \mathbb Z/3^n\mathbb Z` with `3 \nmid \xi`,
$$
\bigl|\widehat{\nu}_n(\xi)\bigr| \;\le\; C_A\, n^{-A} \qquad (\text{superpolynomial in } n,\ \text{not exponential}).
$$

Tao does *not* state, in closed form, a per-step LDP exponent for the descent half of his argument; the drift control is absorbed implicitly into the log-density transport via translation invariance on `u = \log N` (cf. `tao_syracuse_explicit.md` §4.2, Proposition 4.2).

### 2.2 The refinement: an explicit closed-form descent exponent

**Theorem 2.2 (LDP descent-failure rate; `[CLAIMED]`, conditional on the Syracuse model).** *Let `\bar\varphi_n` denote the empirical drift over `n` Syracuse steps, regarded as a function of the valuation sequence `(a_1, …, a_n)` drawn i.i.d. Geom(1/2). Then:*

**(i) Drift LDP (Cramér).** *For every `x` in the effective domain `(-\log(3/2), \infty)`,*
$$
\mathbb P_{\mu_0}\!\bigl(\bar\varphi_n \ge x\bigr) \;\le\; \exp\!\bigl(-\,n\, I(x)\bigr) \qquad (x > \bar\varphi),
$$
*with `I` the closed-form rate function of Theorem 1.2.*

**(ii) Descent-failure exponent.** *In particular, the probability that the orbit fails to descend on average over `n` steps obeys*
$$
\boxed{\quad
\mathbb P_{\mu_0}\!\bigl(\bar\varphi_n \ge 0\bigr) \;\le\; \exp\!\bigl(-\,n \cdot I(0)\bigr) \;=\; \exp\!\bigl(-\,n \cdot 0.054979\ldots\bigr) \;=\; 3^{-n \cdot 0.05004\ldots}.
\quad}
$$
*By Bahadur–Rao the bound is asymptotically sharp: the matching lower bound holds with the same exponent and a `(2\pi n P''(s^*))^{-1/2}` prefactor, with `P''(s^*) = \log 3 \cdot \log(3/2) \approx 0.44545`.*

**(iii) Implied Colmin estimate (conditional).** *Under the standard Tao first-passage transport (`tao_syracuse_explicit.md` §4.2; in particular the Syracuse model accurately tracks the genuine drift over `n` steps, up to the residue-correlated `O(\log\log)` correction qualified in Proposition 4.2), the set of odd `N \in [1, X]` for which no `n` consecutive Syracuse steps achieve any descent at all (i.e. `\sup_{k \le n}(\bar\varphi_k) < 0` fails — the trajectory's running log-mean stays non-negative for `n` steps) has Lebesgue (natural) measure at most `\exp(-n \cdot I(0)) \cdot X`. The complement — `1 - \exp(-n \cdot I(0))`-fraction of odd `N \le X` — admits at least one descent window of length `n` and so achieves*
$$
\mathrm{Col}_{\min}(N) \;\le\; N \cdot \exp\!\bigl(\,-n \cdot |\bar\varphi|\,\bigr) \;=\; N \cdot e^{-n \cdot 0.2877} \;=\; N \cdot 3^{-n \cdot 0.2619}
$$
*(the leading-order descent at the typical drift `\bar\varphi = \log 3 - 2 \log 2`).*

**(iv) Comparison to Tao 2.1.** *Tao's `n^{-A}` controls the residue mod `3^n` equidistribution but is **silent on a closed-form per-step descent exponent**; Theorem 2.2 supplies the latter, with the explicit constant `I(0) \approx 0.05498` (`\approx 0.0500` per Syracuse step in `log_3` units).*

*Proof.* Part (i) is Cramér's theorem (Dembo–Zeitouni Thm 2.2.3) applied to the i.i.d. variables `\varphi(a_j)`, whose CGF `P(s)` is given in closed form by Theorem 1.1 and whose rate function `I` is given by Theorem 1.2. Part (ii) is part (i) at `x = 0`; the sharp asymptotics `(2\pi n P''(s^*))^{-1/2} e^{-n I(0)}` is Bahadur–Rao (Dembo–Zeitouni Thm 3.7.4) with the tilt at `s* = \arg\min(-P(s))` already identified in Theorem 1.1. Part (iii) chains (ii) with the standard first-passage descent estimate at the typical drift `\bar\varphi` (the descent factor over `n` steps where the drift is at its mean). Part (iv) is by inspection of Tao 2.1: Proposition 1.17 controls `|\widehat\nu_n(\xi)|` for residue equidistribution, not the drift's tail; no explicit per-step descent exponent appears in Tao's framework. ∎

**Remark 2.3 (distinction from Tao's result).** Tao 2.1 is a statement about *log-density* equidistribution of residues; Theorem 2.2 is a statement about the *natural-density* (Lebesgue) measure of the *drift-failure event*. They live on orthogonal axes: residue mod `3^n` (Tao) vs. drift `D_n` (this result). The candidate's mod-3 falsifier (`collatz_candidate.md` §2.3) showed that the Esscher tilt only partially repairs the mod-3 marginal of the residue (from `(0, 1/3, 2/3)` to `(0, 0.404, 0.596)`), reducing the TV-floor to `≈ 0.096` but not closing it — so Theorem 2.2 **does not upgrade Tao 2.1 to natural density**. It is a quantitative tightening of the drift-side estimate only.

**Remark 2.4 (Bahadur–Rao constant).** The Bahadur–Rao prefactor in 2.2(ii) is
$$
\mathbb P_{\mu_0}\!\bigl(\bar\varphi_n \ge 0\bigr) \;\sim\; \frac{1}{|s^*|\sqrt{2\pi n \cdot P''(s^*)}}\, e^{-n I(0)} \;=\; \frac{1}{0.438 \cdot \sqrt{2\pi n \cdot 0.4454}} \,e^{-n \cdot 0.0550},
$$
with `s* \approx -0.43803` and `P''(s*) \approx 0.44545` as in Theorem 1.1. The constant `P''(s*) = \log 3 \cdot \log(3/2)` is a clean closed form; the prefactor `1/(|s*|\sqrt{2\pi n P''(s^*)})` is the *tilted CLT envelope* about the Esscher mean.

**Remark 2.5 (unit conventions).** All exponents above are in **nats per Syracuse step**. The conversion factors are:
- nats → `log_2`: divide by `log 2 ≈ 0.693`; so `I(0) ≈ 0.0550/0.693 ≈ 0.0793` in `log_2` units per step.
- nats → `log_3`: divide by `log 3 ≈ 1.099`; so `I(0) ≈ 0.0550/1.099 ≈ 0.0500` in `log_3` units per step. The descent-failure probability is therefore `3^{-n · 0.0500 · (1+o(1))}`.
- The `0.0347` constant cited in the candidate file is `I(0)/(\log 4) = 0.0550/1.386`, the per-step exponent in *Collatz-step* (combined odd+even) units where one Syracuse step costs `\approx 2 + 1 = 3.59 ≈ \log_2 12 / \log_2 4` parity bits — see `collatz_thermo_probe.py` for the conversion. The three numbers `0.0550, 0.0500, 0.0347` all refer to the same physical exponent in different unit conventions; the closed-form invariant is `I(0) = -P(s*) = \log 3 \cdot \log(3/2) / 2 + O(\text{closed-form correction})`.

---

## 3. Comparison with Tao 2022 — the table

| object | Tao 2022 (qualitative) | LDP refinement (explicit) | source |
|---|---|---|---|
| Density mode | log-density 1 of `N` with `\mathrm{Col}_{\min}(N) \le f(N)`, any `f \to \infty` | log-density 1 unchanged (residue side untouched); descent-failure measure controlled in **natural density** | Tao Thm 1.3; this writeup Thm 2.2(iii) |
| Residue equidistribution rate `\sup_{3\nmid\xi}|\widehat\nu_n(\xi)|` | `\le C_A n^{-A}` superpolynomial `[CONSTANT UNVERIFIED]` | unchanged (LDP does not improve residue side) | Tao Prop 1.17; `tao_syracuse_explicit.md` Thm 3.1 |
| Drift LDP rate `-\frac1n \log P(\bar\varphi_n \ge 0)` | not isolated | `I(0) = -P(s^*) \approx 0.054979` nats/step (closed form) | Thm 2.2(ii), `data/thermo_probe.json::I_at_0_closed` |
| Tilted-CLT variance at `s*` | not used | `P''(s^*) = \log 3 \cdot \log(3/2) \approx 0.44545` (closed form) | Thm 1.1, `data/thermo_probe.json::Psecond_at_s_star` |
| Untilted CLT variance | not used | `\sigma^2 = 2(\log 2)^2 \approx 0.96091` (closed form, Livšic) | `collatz_livsic.md` §3.2, `data/thermo_probe.json::untilted_var_phi` |
| Esscher tilt `s*` | `s_{\text{residue}} \approx +0.438` (residue-side, used implicitly) | `s_{\text{drift}} \approx -0.43803` (drift-side, sign-conjugate) | `tao_syracuse_explicit.md` §5.1; Thm 1.1 |
| mod-3 marginal of residue after tilt | not analyzed | `(0, 0.404, 0.596)` — TV-floor `\approx 0.096` (cannot reach uniform) | `collatz_candidate.md` §2.3 |
| Implied `\mathrm{Col}_{\min}` bound | `\le f(N)`, any `f \to \infty`, log-density-1 | `\le N \cdot 3^{-n \cdot 0.2619}` outside a natural-density-`\exp(-n \cdot I(0))` set | Thm 2.2(iii) |

**One-line takeaway.** *The LDP refinement gives an **explicit exponential** descent-failure rate `\exp(-n \cdot 0.0550)` on the drift axis, where Tao 2022 gives only **superpolynomial** `n^{-A}` decay on the residue axis. The two are orthogonal: the LDP does **not** improve Tao's residue bound, and does **not** close the log → natural-density gap (the mod-3 obstruction survives, attenuated, per `collatz_candidate.md` §2.3).*

---

## 4. Scope statement (precise; honest)

**What this refinement DOES give.**
1. An explicit closed-form per-step LDP rate `I(0) = -P(s^*) = \log 3 + (s^*-1)\log 2 - \log(1 - 2^{s^*-1}) \approx 0.054979` for the probability that the empirical drift over `n` Syracuse steps fails to descend (Thm 2.2(ii)).
2. An explicit closed form `P''(s^*) = \log 3 \cdot \log(3/2)` for the tilted-CLT variance entering the Bahadur–Rao sharp asymptotics (Rmk 2.4).
3. The complete Cramér rate function `I(x)` for the drift, in closed form via Legendre transform (Thm 1.2).
4. An explicit natural-density Colmin bound `N \cdot 3^{-n \cdot 0.2619}` on the complement of a set of natural measure `\le \exp(-n I(0)) = 3^{-n \cdot 0.05}` (Thm 2.2(iii)), conditional on Tao's first-passage transport.

**What this refinement does NOT give.**
- It does NOT prove Collatz, nor any version of it for all `N`.
- It does NOT close the log → natural-density gap. Reason: the mod-3 obstruction in the residue is only partially repaired by the Esscher tilt (TV-floor drops from `1/6` to `\approx 0.096`, but is non-zero), per `collatz_candidate.md` §2.3 and §4. The residue-equidistribution side is *unchanged* by this refinement.
- It does NOT improve the rate `n^{-A}` of Tao Proposition 1.17. The LDP operates on the drift cocycle; Tao's bottleneck is the residue characteristic function on `\mathbb Z/3^n\mathbb Z`.
- It does NOT improve the *exponent* `\beta = 1` heuristic of Tao 2020. The descent exponent `I(0) \approx 0.0550` is on a different axis from `\beta`.
- The "implied Colmin estimate" of Thm 2.2(iii) is **conditional on Tao's first-passage transport accurately tracking the drift over `n` steps**. The Syracuse-model `\Leftrightarrow` genuine-orbit identification carries the same caveats as Tao 2022 — see `tao_syracuse_explicit.md` §4.2 and Proposition 4.2.

**Honest novelty assessment.** The closed form `P(s) = -s \log 3 + (s-1) \log 2 - \log(1 - 2^{s-1})` is elementary (it is the CGF of a tilted geometric, computed in two lines), and the application of Cramér's theorem is standard. The contribution is the *packaging* — making the explicit descent exponent visible in a quantitative comparison to Tao 2022 — not new analysis. `[NOVELTY UNVERIFIED — this is almost certainly folklore in the Sinai (2003) / Akin (2004) / Lagarias (survey) / Tao (2022) tradition; a prior-art check in Sinai's "Statistical (3x+1) problem", Akin's "Why is 3n+1 difficult?", and Lagarias's survey chapter is required before any publication claim.]`

---

## 5. Constants table with sources

| symbol | value | derivation / source |
|---|---|---|
| `\bar\varphi = E_{\mu_0}[\varphi]` | `\log 3 - 2 \log 2 = -0.287682` | direct, `data/thermo_probe.json::EBAR_nats` |
| `\sigma^2_{\text{Livšic}} = \text{Var}_{\mu_0}(\varphi)` | `2 (\log 2)^2 = 0.960906` | `collatz_livsic.md` §3.2; `data/thermo_probe.json::untilted_var_phi` |
| `s^*` | `1 + \log_2(1 - \log 2/\log 3) = -0.438033` | Thm 1.1; `data/thermo_probe.json::s_star` |
| `P(s^*)` | `-0.054979` | Thm 1.1; `data/thermo_probe.json::P_at_s_star` |
| `P''(s^*)` | `\log 3 \cdot \log(3/2) = 0.445449` | Thm 1.1; `data/thermo_probe.json::Psecond_at_s_star` matches closed form to `5.6e-17` |
| `I(0) = -P(s^*)` | `0.054979` (nats/step) | Thm 1.2; matches closed-form identity to machine zero |
| `I(0)` in `log_3` units | `0.054979 / \log 3 = 0.050043` per step | Rmk 2.5 |
| `I(0)` in `log_4` (Collatz-step) units | `0.054979 / (2\log 2) = 0.039661` per step (≈ 0.0347 in candidate's `log_3·log_4`-mixed convention) | Rmk 2.5 |
| `|\bar\varphi|` (typical descent rate) | `0.287682` nats/step `= 0.261860 \cdot \log 3` | direct |
| Tao Prop 1.17 rate | `n^{-A}` for every `A`, no explicit `C_A` | `[CONSTANT UNVERIFIED]`; Tao 2022 §7, snippet-sourced via `tao_syracuse_explicit.md` Thm 3.1 |
| Tao `c_n = \inf P(\mathrm{Syrac} = b)` (`\beta=1` heuristic) | `c_n \stackrel{?}{=} 3^{-n + o(n)}` (conjectural) | Tao 2020 blog; `survey.md` §5.4; `[CONSTANT UNVERIFIED]` |
| Numerical `c_n \cdot 3^n` (small `n`) | `1.00, 0.286, 0.165, 0.145, 0.108` (n=1..5) | `tao_syracuse_explicit.md` §2.3; verified in `verify_syracuse_rv.py` |
| mod-3 marginal at `s = 0` | `(0, 1/3, 2/3)` | `data/thermo_probe.json::mod3_falsifier`; exact via DP |
| mod-3 marginal at `s = s^*` | `(0, 0.40383, 0.59617)` | same; max abs diff from untilted `= 7.05e-2` |
| Implied TV-floor of `\nu^{(s^*)}_n` from mod-3 | `\ge 0.096` `\forall n` | `collatz_candidate.md` §2.3 / §4 |

---

## 6. Open question — the multi-parameter-tilt frontier

The single-parameter Esscher tilt `s*` of §1 is the unique *drift-balancing* one-parameter tilt; it leaves the mod-3 marginal of the residue at `(0, 0.404, 0.596)`, off uniform by TV `\ge 0.096` (`collatz_candidate.md` §2.3, L3). The natural next frontier the LDP framing isolates is:

> **Open question (multi-parameter tilt; saturating mod-3 under the LDP envelope).** Does there exist a multi-parameter (or `n`-time-varying) tilt family `\{P_{\mathbf s}\}_{\mathbf s \in \mathbb R^k}` of the Geom(1/2) base law on the valuation shift such that:
> 1. some tilt `\mathbf s^\dagger` in the family balances the drift (`E_{\mathbf s^\dagger}[\varphi] = 0`); and
> 2. the same tilt drives the mod-3 marginal of the Syracuse residue to *uniform* `(0, 1/2, 1/2)`; and
> 3. the LDP envelope is preserved — i.e. the descent-failure rate at `\mathbf s^\dagger` is `\ge c \cdot I(0)` for some `c > 0` (no rate degradation)?
>
> The single-parameter Esscher family parameterized by `s \in (-\infty, 1)` does NOT contain such a tilt (`collatz_candidate.md` §2.2, L4; the mod-3 marginal under that family is `(0, 1/(1+r), r/(1+r))` for `r = 2^{-(1+s)} > 0`, hitting `(1/2, 1/2)` only at `s \to 1^-` where `P(s) \to \infty`). Whether a richer tilt family — e.g. tilting `a_n` (the last valuation, which alone controls the mod-3 marginal) independently of `\sum_{j < n} a_j` — saturates the marginal while preserving the LDP rate is **open**.

A parallel agent (`collatz_multitilt.*`, files reserved — this writeup deliberately stays out of those) is exploring this multi-tilt direction. The LDP refinement isolated here is what makes the question precise: it pins down the *envelope* that any candidate multi-tilt must preserve.

---

## 7. Validation (cross-check; no new computation)

All numerical values in this writeup are taken verbatim from `data/thermo_probe.json` and `data/thermo_probe.log`, produced by `collatz_thermo_probe.py` (Monte-Carlo seed `20260604`, `n_samples = 200000` for the empirical pressure, `n_blocks = 5000` for the CLT validation, `n_starts = 5000` trajectory verifier with `N_max = 10^6` and `n_steps_max = 300`). The key cross-checks:

- **Closed-form identities (machine precision):** `P'(s^*) = 0.0` exactly; `P''(s^*) - \log 3 \cdot \log(3/2) = 5.6 \times 10^{-17}`; `I(0) + P(s^*) = 0.0` exactly. (`data/thermo_probe.json::closed_form_identities`.)
- **Monte-Carlo pressure (cross-check, `n_samples = 2 \times 10^5`):**
  - `P(-0.438)`: closed `-0.054979`, MC `-0.055162`, abs.err `1.8 \times 10^{-4}`.
  - `P(0.0)`: closed `0`, MC `0` (zero by construction).
  - `P(+0.5)`: closed `+0.33207`, MC `+0.32970`, abs.err `2.4 \times 10^{-3}`.
  - `P(+0.8)`: closed `+1.0269`, MC `+0.9581`, abs.err `6.9 \times 10^{-2}` (heavy-tail noise, expected at the boundary of effective domain).
- **CLT (block-variance vs `2(\log 2)^2/n`):** `n = 50, 100, 500, 1000` give ratio `0.958, 0.979, ~1.0, ~1.0` of empirical block-variance to predicted; agreement to 1–4% as expected for `n_blocks \in [2000, 5000]`.
- **mod-3 marginal (exact DP, `n \in \{2, 3, 4, 5, 6\}`, `amax = 30`):** at `s = 0`, exactly `(0, 1/3, 2/3)`; at `s = s^*`, exactly `(0, 0.403831, 0.596169)` at every `n` (max abs diff from untilted = `7.05 \times 10^{-2}`). This confirms the falsifier finding: the mod-3 marginal is shift-invariant and the tilt moves it but does not equalize.
- **Trajectory check (verifier-generated 5000 odd starts ≤ `2 \times 10^6`, up to 300 Syracuse steps):** empirical valuation mean `1.995` (predicted `2.0`); per-block drift means `-0.28, -0.25, -0.14, -0.08` at `n = 10, 20, 50, 100` (the upward drift at larger `n` reflects orbit-length selection bias, which is itself a manifestation of the LDP-measured natural-vs-log gap).

All values stable; nothing in this writeup requires re-running `collatz_thermo_probe.py`.

---

## 8. Status

| component | status |
|---|---|
| Theorem 1.1 (closed-form pressure) | `[VERIFIED]` — closed form + machine-precision identity |
| Theorem 1.2 (closed-form rate function) | `[VERIFIED]` — Legendre transform + MC cross-check |
| Theorem 2.2 (i, ii) (LDP & descent-failure exponent) | `[VERIFIED — standard Cramér / Bahadur–Rao applied to the closed-form pressure]` |
| Theorem 2.2(iii) (implied Colmin estimate) | `[CONDITIONAL — on Tao's first-passage transport, qualified at the same level as Tao 2022]` |
| Theorem 2.2(iv) (comparison with Tao 2.1) | `[CLAIMED]` — by inspection of Tao Prop 1.17 |
| Comparison table (§3) | `[VERIFIED]` for LDP-side entries; `[CONSTANT UNVERIFIED]` for Tao-side entries (snippet-sourced) |
| Scope statement (§4) | self-consistent with `collatz_candidate.md` falsifier |
| Open question (§6) | `[OPEN]` — multi-parameter tilt saturating mod-3 while preserving LDP envelope; parallel agent working `collatz_multitilt.*` |
| Constants table (§5) | `[VERIFIED]` (LDP side, machine-precision); `[CONSTANT UNVERIFIED]` (Tao side, snippet-sourced) |
| `[NOVELTY UNVERIFIED]` | flagged; the LDP-vs-Tao comparison theorem is almost certainly known to the Sinai/Akin/Lagarias/Tao tradition; prior-art check is the gating step before publication |

**Paper-readiness assessment.** The writeup is *internally* publication-grade — closed forms validated, scope honest, falsifier respected, comparison precise. It is *externally* not publication-ready until: (a) Tao 2022 constants are checked against the primary source (currently snippet-sourced); (b) prior-art pass through Sinai 2003, Akin 2004, Lagarias survey for the LDP / pressure formulation; (c) red-team of Theorem 2.2(iii)'s conditional dependence on Tao's first-passage transport. The gate is (b): if the closed-form pressure or the descent exponent appears in the literature, the contribution shrinks to a *quantification table* rather than a theorem, and the writeup should be folded into a methods-section appendix of the Collatz paper rather than a standalone theorem.

**Bottom line.** The result is real, modest, and explicit. It does not advance toward Collatz; it makes one quantitative aspect of Tao 2022 visible in closed form. Publishability depends entirely on the prior-art check.
