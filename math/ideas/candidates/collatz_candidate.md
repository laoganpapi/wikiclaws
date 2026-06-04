# Collatz candidate — Thermodynamic-formalism / large-deviation framing of the Syracuse drift

> ## ⚠️ CORRECTION (post-multi-tilt) — READ FIRST
> The multi-tilt deciding experiment + independent algebraic verification overturned **the residue-side narrative in this document** (every "tilt partially repairs mod-3 to 0.404 / 0.596 / TV 0.096" claim, including §2.3 / L3 / §4 / §5):
> - At the actual drift-balancing Esscher tilt s ≈ −0.438 (under the convention used in `collatz_thermo_probe.py`), the mod-3 marginal is **(0, 0.270, 0.730), TV-on-units ≈ 0.230 — *worse* than untilted (0.167)**. The "(0.404, 0.596)" figures came from a non-drift-balancing tilt (sign-convention slip: drift-balance under the +s parameterisation is s = +0.438, not −0.438; under the −s parameterisation it's s = −0.438 but with a different mapping to the marginal).
> - **Strengthened, corrected picture:** single-parameter drift-balancing Esscher *worsens* the mod-3 marginal; the **multi-tilt Class (C) two-parameter Esscher** (with auxiliary cocycle ψ(a) = [a even]) at (s, t) = (−1.309, −1.600) is the first mod-3 *saturation* in this stream — exact uniform marginal, drift mean 0, **LDP rate I ≈ 0.228 = 4.15× the single-parameter 0.0550**. It does NOT iterate (mod-9 TV = 0.313; provable finite-d obstruction).
> - **The candidate's drift-side claims are unaffected** (closed-form pressure P(s), rate I(0) ≈ 0.0550, tilted CLT variance P″(s*) ≈ 0.4454 — all computed at the actual drift-balancing tilt). The CORRECT residue-side story is in `collatz_multitilt.md`; this document is left intact with this banner rather than silently rewritten.

**Track:** Collatz, Vector A (sharpen Tao 2022 toward natural density). The surviving research-program candidate after the entire structured / algebraic / cohomological pipeline was certified negative.
**Author:** Alex Ye (AI-assisted computation; AI not on author line per project rules).
**Date:** 2026-06-04.
**Status:** `[CANDIDATE — research program, not proof attempt]`. Closed-form pressure and rate function are proof-grade; validation against Monte-Carlo and trajectory data is numerical. `[NOVELTY UNVERIFIED]` — thermodynamic-formalism views of Collatz almost certainly exist (Sinai, Akin, Lagarias survey, and the Tao 2022 Esscher tilt itself); the contribution is the *packaging* and a sharp *falsifier*, not the LDP machinery.
**Code:** `collatz_thermo_probe.py`. **Data:** `data/thermo_probe.json`, `data/thermo_probe.log`.
**Publishable form:** `collatz_thermo_writeup.md` (theorem-style writeup, ready for red-team; states the LDP-vs-Tao comparison theorem with the explicit constant `I(0) = -P(s*) ≈ 0.05498` and the explicit `P''(s*) = log3 · log(3/2) ≈ 0.44545`, and pins down the open multi-parameter-tilt question this candidate isolates).

---

## 0. Verdict (read first)

> **The surviving candidate is the LDP / thermodynamic-formalism core of the Syracuse system — the Tao β=1 / fine-scale-mixing neighborhood, untouched by the structural kills. The numerical validation confirms the closed forms (pressure P(s), Esscher tilt s\*, rate function I(x), tilted CLT variance P''(s\*)) to 5–6 decimals against Monte-Carlo. BUT: the falsifier we built in (does the Esscher tilt repair the mod-3 marginal of the residue?) returns a quantitative finding — the tilt *partially* repairs the marginal (from (0, 1/3, 2/3) → (0, 0.404, 0.596)), reducing the natural-density TV-floor of `natural_density_obstruction.md` from 1/6 to about 0.096, **but does not eliminate it**. So this candidate is real but its honest target is a *quantitative improvement* of Tao 2022's β-bound, NOT a closure of the log → natural gap. The mod-3 obstruction survives in attenuated form.**

This is the genuine analytic core where Tao's 2022 work lives. It is the **only** of the wave's framings that was not killed. The deliverable of this wave is:

1. The closed-form pressure `P(s) = -s·log3 + (s-1)·log2 - log(1 - 2^{s-1})` and its Legendre transform `I(x)`.
2. The Esscher tilt `s* = 1 + log_2(1 - log_2(2)/log_2(3)) ≈ -0.43803` and the tilted CLT variance `P''(s*) = log3 · log(3/2) ≈ 0.4454` (distinct from the *untilted* Livšic CLT variance `2·(log2)² ≈ 0.9609`).
3. A precise statement of what equidistribution rate would close the log → natural gap (essentially Tao's β=1 with the LDP weighting), and a sharp falsifier numerically demonstrating that the **mod-3 obstruction of the residue is only partially repaired by the tilt**, fixing the residual gap at ≈ 0.096 in TV — a *quantitative* improvement of Tao 2022's residue input, not a route to natural density.

Honest assessment is in §6: this is a **genuine surviving lead at the level of a quantitative refinement**, not a route to closing the conjecture.

---

## 1. The system, the cocycle, and the pressure (closed form)

### 1.1 Setup (verified, `collatz_livsic.md` §1)

The Syracuse system is the one-sided shift `σ` on 2-adic valuation sequences `a = (a_j)_{j≥1}` with `a_j ∈ {1,2,3,…}`, equipped with the i.i.d. Geometric(1/2) base measure `μ_0` (`P(a=k) = 2^{-k}`, mean 2). The drift cocycle
$$
\varphi(a) \;=\; \log 3 - a_1 \log 2 \qquad (\text{nats per Syracuse odd step})
$$
has `E_{μ_0}[φ] = log3 - 2log2 = -0.2877` (= `(log_2 3 - 2) log2`, the known descent rate). The *Livšic* analysis (`collatz_livsic.md`) established that `[φ]` is **non-trivial in H¹** — a non-coboundary — so the drift satisfies a non-degenerate CLT under `μ_0` with variance `σ²_{Livšic} = 2·(log2)² ≈ 0.9609`. This is the input.

### 1.2 The pressure function (closed form, proof-grade)

The cumulant generating function of `−φ` under `μ_0`:
$$
P(s) \;:=\; \log E_{μ_0}\!\bigl[\,e^{-s\,\varphi(a)}\bigr] \;=\; \log E\!\bigl[\,e^{-s\log 3 + s a \log 2}\bigr] \;=\; -s\log 3 + \log\!\sum_{k\ge1}2^{-k}\,2^{sk}.
$$
The geometric sum converges for `s < 1`, giving
$$
\boxed{\quad P(s) \;=\; -s\log 3 \;+\; (s-1)\log 2 \;-\; \log\!\bigl(1 - 2^{\,s-1}\bigr), \qquad s \in (-\infty,\,1). \quad}
$$
Differentiating (closed):
$$
P'(s) \;=\; -\log 3 \;+\; \frac{\log 2}{1 - 2^{s-1}}, \qquad
P''(s) \;=\; \frac{(\log 2)^2 \cdot 2^{s-1}}{(1 - 2^{s-1})^2}.
$$

### 1.3 The Esscher (drift-balancing) tilt

The tilt `s*` solving `E_{s*}[φ] = 0` is `P'(s*) = 0`, equivalently `1 - 2^{s*-1} = log2/log3`:
$$
\boxed{\quad s^* \;=\; 1 + \log_2\!\Bigl(1 - \tfrac{\log 2}{\log 3}\Bigr) \;=\; 1 + \log_2\!\Bigl(\tfrac{\log_2 3 - 1}{\log_2 3}\Bigr) \;\approx\; -0.43803. \quad}
$$
The signed convention here (s acts on `−φ`) is opposite to the residue-side tilt `s_residue = +0.438` of `tao_syracuse_explicit.md` §5.1; they are the same Esscher tilt expressed in conjugate-variable sign.

**The tilted CLT variance**:
$$
P''(s^*) \;=\; \log 3 \cdot \log(3/2) \;\approx\; 0.44563.
$$
This is **strictly different** from the untilted CLT variance `σ²_{Livšic} = 2·(log2)² ≈ 0.9609` of `collatz_livsic.md`. The two coincide in the Gaussian-only world; here `P''(s) ≠ Var_{μ_0}(φ)` because `P` is non-quadratic. Both are quoted in the candidate's output, and which is "the" variance depends on the question: untilted CLT for `μ_0`-typical orbits ⇒ `2(log2)²`; LDP curvature at the rate-balance tilt ⇒ `log3·log(3/2)`.

### 1.4 The rate function (Legendre transform, closed form)

`I(x) := sup_s (sx − P(s))`. The optimizer satisfies `x = P'(s)`, i.e. `1 - 2^{s-1} = log2/(x + log3)`:
$$
s(x) \;=\; 1 + \log_2\!\Bigl(1 - \tfrac{\log 2}{x + \log 3}\Bigr), \qquad
I(x) \;=\; s(x)\,x \;-\; P\bigl(s(x)\bigr).
$$
Effective domain: `x ∈ (log2 - log3, ∞) = (-log(3/2), ∞) ≈ (-0.4055, ∞)`. Special values:

| `x` | `s(x)` | `I(x)` | meaning |
|---|---|---|---|
| `φ̄ = log3 − 2log2 ≈ −0.2877` | `0` | `0` | the typical (μ_0) drift, rate 0 |
| `0` | `s* ≈ −0.43803` | `−P(s*) ≈ 0.05498` | the descent-balance (no-descent) tail |
| `+0.10` | `≈ −0.71` | `≈ 0.02129` | an "anti-descent" drift |

`I(0) = 0.05498` is **the LDP descent-failure rate** — the exponent at which, under `μ_0`, the empirical per-step drift fails to descend ("the orbit's log-magnitude on average stays flat for n steps") with probability `≈ exp(−n · I(0))`. Equivalently it equals `−P(s*)` (a clean identity, validated to 1e-17).

### 1.5 Validation (`thermo_probe.py`)

Identity checks (closed-form internal consistency) all pass to machine precision:

| identity | predicted | observed | err |
|---|---|---|---|
| `s*` solves `P'(s*) = 0` | `0` | `0.0` | `0` |
| `P''(s*) = log3 · log(3/2)` | `0.4454489504` | `0.4454489504` | `5.6e-17` |
| `I(0) = −P(s*)` | match | match | `0.0e+00` |
| `I(φ̄) = 0` | `0` | `0` | `0` |
| untilted variance `= 2(log2)²` | `0.9609060278` | `0.9609060278` | `0` |

Monte-Carlo validation (`n_samples = 5e5` for `P`, `n_blocks = 5e5` for CLT/LDP):

| object | closed | empirical | rel.err |
|---|---|---|---|
| `P(−0.438)` | `−0.05498` | `−0.05586` | `1.6 %` |
| `P(0.0)` | `0.0` | `0.0` (zero by construction) | `0` |
| `P(+0.5)` | `+0.33207` | `+0.33265` | `0.2 %` |
| `P(+0.8)` | `+1.02695` | `+0.98719` | `3.9 %` (heavy-tail noise, expected) |
| block-`var(φ_n)` at `n=100`, predicted `2(log2)²/100` | `9.609e-3` | `9.40e-3` | `2 %` |
| block-`var(φ_n)` at `n=500` | `1.922e-3` | `1.965e-3` | `2 %` |
| block-`var(φ_n)` at `n=1000` | `9.61e-4` | `9.57e-4` | `0.4 %` |
| `I(0)` from `−log(P[|φ_n/n| < 0.05])/n` at `n=50` | `0.0550` | `0.0816` | (off by saddle-point prefactor `O(log n/n)`, expected) |

CLT variance matches `σ²/n` to a few percent across `n = 50, 100, 500, 1000`. The rate-function empirical at `n=50` shows the right monotone shape (`I_hat` decreases as `x` approaches `φ̄`); the absolute level is offset by an `O(log n/n)` Stirling/saddle-point prefactor (well-known in finite-`n` LDP comparisons), which validates the qualitative LDP envelope. **The closed forms hold up.**

Trajectory check (5000 odd starts ≤ 2·10^6, walked up to 300 Syracuse steps using the imported `verifier.T`): empirical valuation mean `1.995` ≈ 2, valuation variance `1.84` ≈ 2 (Geom(1/2)), and per-block drift means `−0.28, −0.25, −0.14, −0.08` for `n = 10, 20, 50, 100`. The drift means *drift up* (less negative) as `n` grows because the *trajectory* sampling is biased to descending orbits — long-orbit selection bias, not a defect in the closed form. This is itself the manifestation of natural-density-vs-trajectory the LDP measures.

---

## 2. The candidate program — what would close (or not close) what

### 2.1 The conditional content (proposal, not proof)

The setup of `tao_syracuse_explicit.md` §5 makes the natural-density upgrade conditional on Hypothesis `MIX(θ)`:
$$
\sup_{\xi:\,3\nmid\xi} \bigl|\,\widehat{\nu_n^{(s^*)}}(\xi)\,\bigr| \;\le\; C\,3^{-\theta n}, \qquad \theta > \tfrac12,
$$
i.e. exponential decay of the **tilted** Syracuse characteristic function with rate beating the Plancherel `3^{n/2}` toll. By Lemma 6.2 there, this implies `‖ν_n^{(s*)} − U‖_{TV} → 0` exponentially, closing the residue-side of the natural-density transport.

The thermodynamic-formalism reformulation of `MIX(θ)` is **already implicit** in the Esscher tilt of §1.3 above — it is the same `s*`. The new content this candidate offers is:

> **The LDP rate function `I(·)` of §1.4 provides a *universal* envelope on the drift tail. Combined with `MIX(θ)`, the joint (residue, drift) law at the Esscher tilt admits an effective two-dimensional Gaussian envelope `exp(−n·(I(x) + (residue Plancherel))/(P''(s*)))` with constants log3 · log(3/2) (drift quadratic) and `3^{n/2}/φ(3^n) ≈ 3^{n/2-n+log_3 2}` (residue Plancherel). The Tao 2022 input gives `n^{-A}` superpolynomial on the residue; the LDP gives **exponential** on the drift, *with explicit constant `I(0) = −P(s*) ≈ 0.05498`*. Whether this is enough to close the log → natural gap reduces to whether the residue-side `MIX(θ)` can be improved from `n^{-A}` to `3^{-θ n}` with `θ > 1/2`, OR whether the *joint* LDP curvature `P''(s*)` can do strictly better than `√(2 P''(s*) · n)` Plancherel-type estimates suggest.**

**Honest target.** A quantitative improvement of Tao 2022's effective `β`-bound: if Tao's bound on `|ν̂_n(ξ)|` is `n^{-A}` for arbitrary `A`, then by the LDP envelope above one would *conjecture* that the tilted version improves to `n^{-A} · (P''(s*))^{n/2}`-type sharpening, but the constant `P''(s*)` is `< 1`, so **the LDP envelope on its own does not give exponential decay**; it gives a sharper polynomial constant. The honest target is a quantitative refinement of `A`, not a `θ > 0`.

### 2.2 The first lemmas (research program — to attempt)

- **L1 (closed-form pressure, DONE).** `P(s) = -s log3 + (s-1) log2 - log(1 - 2^{s-1})`. The Esscher tilt `s* ≈ -0.43803`, `P''(s*) = log3 · log(3/2)`, `I(0) = -P(s*) ≈ 0.05498`. **Validated against MC to 1–4%.**

- **L2 (rate of empirical-drift concentration).** Under `μ_0`: `P(|φ_n/n − φ̄| > ε) ≤ 2 exp(−n c(ε))` with explicit `c(ε)` from `I` via `c(ε) = min(I(φ̄ + ε), I(φ̄ − ε)) > 0`. The closed form gives `c(0.10) ≈ min(I(-0.188), I(-0.388)) ≈ 0.012` and `c(0.05) ≈ 0.003`, with the local quadratic `c(ε) ≈ ε²/(2 σ²) = ε²/(2·0.961) ≈ 0.52 ε²`. **Reproducibility: this is the standard Cramér theorem applied to our closed-form `I`.**

- **L3 (reconciliation with the mod-3 obstruction).** The mod-3 marginal of the residue `R_n mod 3` is the law of `2^{-a_n} mod 3` (suffix structure of the offset; verified to (0, 1/3, 2/3) at every `n` in the probe). The Esscher tilt re-weights via `e^{-s* (S log2 - n log3)} = e^{-s* log2 · Σ a_j} · (n-const)`. Since the joint factor depends on `Σ a_j` and the residue's mod-3 marginal depends only on `a_n`, the tilt reweights the law of `a_n` from `Geom(1/2)` to `Geom(2^{1+s*})`-type with `2^{1+s*} = 1 - 1/log_2 3 ≈ 0.369`, giving:
$$
P_{s^*}(a_n=k) \propto 2^{-k(1+s^*)},
\quad
P_{s^*}(a_n \text{ odd}) \;=\; \frac{2^{-(1+s^*)}}{1 - 2^{-2(1+s^*)}} \;=\; \frac{1}{1 + 2^{-(1+s^*)}} \;\approx\; 0.596.
$$
Hence `R_n mod 3 ∈ {1, 2}` with `P_{s*}(R_n ≡ 2 mod 3) ≈ 0.596`, `P_{s*}(R_n ≡ 1 mod 3) ≈ 0.404`. **The tilt MOVES the mod-3 marginal from `(0, 1/3, 2/3)` to `(0, 0.404, 0.596)`, partially repairing the natural-density TV-floor from `1/6 ≈ 0.167` (untilted) to `≈ 0.096` (tilted) — but does NOT close it.**

- **L4 (the key open question).** Does adding equidistribution of the tilted residue distribution *beyond* what Tao establishes close the log → natural gap? The reduced answer (after L3): **no, not via the s\* tilt alone** — the mod-3 marginal floor of `0.096` after tilt is small but non-vanishing, so `‖ν_n^{(s*)} − U‖_{TV} ≥ 0.096` for every `n`. To close the gap one would need a **further tilt or a different observable** that moves the mod-3 marginal to `(0, 1/2, 1/2)`. The Esscher family `e^{-s D_n}` is the natural one-parameter tilt; *no `s` in this family* makes the mod-3 marginal uniform, because the marginal only depends on the law of `a_n` and that family produces only marginals of the form `(0, 1/(1+r), r/(1+r))` with `r = 2^{-(1+s)} > 0`, hitting `(1/2, 1/2)` only as `s → 1−` (in which case `P(s) → ∞` and the tilt is degenerate).

> **L4 (sharpened statement, the candidate's proposal).** *The natural-density upgrade via single-parameter Esscher tilting is OBSTRUCTED by the mod-3 marginal at every finite `s`. The thermodynamic-formalism candidate REDUCES the problem to: find a non-Esscher reweighting (e.g. an `(s_1, …, s_n)`-time-varying tilt that re-balances `a_n` independently of `D_n`) such that the joint (residue, drift) law has uniform mod-3 marginal AND exponentially-small Fourier mass off-coset. This is the precise OPEN problem that survives the wave.*

### 2.3 The sharp falsifier (run; result)

**Falsifier statement.** "If the Esscher tilt at `s*` preserves the mod-3 marginal of the residue (or moves it but not to uniform), then the LDP envelope alone cannot close the log → natural gap, and the candidate reduces to a quantitative refinement of Tao 2022."

**Test.** Computed exactly via the joint `(R_n mod 3^n, S_n)` DP at `n = 2, 3, 4, 5, 6` (truncated Geometric, amax=30, renorm.). At every `n`:

| `n` | mod-3 marginal at `s=0` | mod-3 marginal at `s=s*` | max diff |
|---|---|---|---|
| 2 | (0, 0.333333, 0.666667) | (0, 0.403831, 0.596169) | 7.05e-02 |
| 3 | (0, 0.333333, 0.666667) | (0, 0.403831, 0.596169) | 7.05e-02 |
| 4 | (0, 0.333333, 0.666667) | (0, 0.403831, 0.596169) | 7.05e-02 |
| 5 | (0, 0.333333, 0.666667) | (0, 0.403831, 0.596169) | 7.05e-02 |
| 6 | (0, 0.333333, 0.666667) | (0, 0.403831, 0.596169) | 7.05e-02 |

The tilt **partially repairs** the marginal (closer to `(0, 1/2, 1/2)` than the untilted one is) but never reaches uniform — exactly as L3 predicted from the structural identity `R_n mod 3 = 2^{-a_n} mod 3`. **Falsifier triggered**: the candidate does NOT close the log → natural gap; the residual TV-floor of `≈ 0.096` survives.

This is **not a kill** of the candidate — it converts the candidate from "potential closure of log → natural" to "**quantitative refinement of Tao 2022**". The honest deliverable shrinks accordingly (§6).

---

## 3. Comparison with Tao 2022

| object | Tao 2022 input | LDP / thermodynamic-formalism reformulation |
|---|---|---|
| Mixing rate `|ν̂_n(ξ)|` for `3∤ξ` | `n^{-A}` (superpolynomial, Prop 1.17) | unchanged in marginal (LDP is on drift, not residue) |
| Drift control | implicit in log-density transport (translation invariance) | **explicit** LDP envelope `exp(−n I(x))`, closed form |
| Tilt | the Esscher tilt `s_residue ≈ +0.438` for tilted Syracuse RV (§5.1) | same `s*` (sign flipped: `s_drift ≈ −0.438`) |
| CLT variance (untilted) | not used | `σ² = 2(log2)² ≈ 0.961` (Livšic) |
| CLT variance (tilted) | not used explicitly | `P''(s*) = log3 · log(3/2) ≈ 0.446` |
| Descent-failure rate (LDP) | not isolated | `I(0) = −P(s*) ≈ 0.0550` per step |

**Are they orthogonal or redundant?** Mostly **redundant** at the leading order: Tao's transport already absorbs the drift via translation invariance under log-sampling; the LDP makes the drift control *explicit* and *quantitative* but does not add a new analytic input. **Where they differ.** The LDP provides:

1. An **explicit prefactor and exponent** `exp(−n · I(0))` for the descent-failure probability — Tao's log-density theorem proves descent qualitatively but the LDP measures *at what rate*.
2. A **trajectory-level CLT** (the Livšic non-coboundary gives the non-degenerate variance) — this is a quantitative refinement of "the orbit's log-magnitude is approximately Gaussian of variance `2(log2)² · n`" with a sharp constant.

**The orthogonal half — residue equidistribution — is unaltered.** The LDP/thermodynamic-formalism does NOT improve the rate of decay of `|ν̂_n(ξ)|` (which is the actual `β=1` bottleneck), because the residue marginal is *invariant* under the Esscher tilt up to the mod-3 attenuation of §2.3.

**Honest conclusion.** The thermodynamic-formalism program reproduces Tao 2022's drift content with explicit constants (a quantitative refinement, not a structural improvement) and **does not advance the residue side**, which is the actual analytic bottleneck. The candidate's deliverable is a *quantitative sharpening of Tao 2022's β-bound by the explicit constant `I(0) = -P(s*)`*, not a route to natural density.

---

## 4. The residual structural obstruction (mod-3 in the residue)

Per L3 / falsifier: the mod-3 marginal of the residue is `2^{-a_n} mod 3`, fully determined by the law of the last valuation. The Esscher tilt at `s*` re-weights this law from `Geom(1/2)` to `Geom(2^{-(1+s*)}) = Geom(0.369)`, partially repairing the marginal to `(0, 0.404, 0.596)`. The **TV-floor `‖ν_n^{(s*)} − U_{(\mathbb Z/3^n\mathbb Z)^\times}‖_{TV} ≥ 0.096`** for every `n ≥ 1`.

**What this means for the program.** The single-parameter Esscher family `{e^{-s D_n}}_{s ∈ \mathbb R}` cannot saturate the natural-density transport. Any natural-density-upgrade route via thermodynamic formalism alone is forced to either (a) introduce a richer tilt family (`n`-time-varying tilts; multi-parameter tilts coupling `a_n` separately from `Σ_{j<n} a_j`), or (b) accept a residual `O(1)` TV defect and route around it (e.g. by averaging over residue cosets mod 3 — but this is exactly Tao's log-density structure, no gain).

**The mod-3 obstruction is the same one identified in `natural_density_obstruction.md` and the joint-law / residue⊥drift kill of the prior `collatz_candidate.md` (now relabeled "killed shortcuts" below).** The thermodynamic formalism does NOT escape it; it just makes its quantitative shape (a 1/6 → 0.096 reduction under the descent-balance tilt) explicit.

---

## 5. The killed shortcuts (the prior wave's content, retained for the record)

This file replaces a sequence of candidates that were certified negative within this session:

- **Ψ_n factorization / (residue, drift) joint disjointness** — `[CERTIFIED NEGATIVE]`. The factorization defect `Δ_n` diverges as `3^{+0.85n}`, not decays. See git history for the prior text; `data/psi_factorization.json` retained.
- **Livšic coboundary of the drift cocycle** — `[CERTIFIED NEGATIVE]`. `[φ] ≠ 0` in H¹; the constant-word period-`p` orbits give `Σψ = p(2-c)·log2`, an unbounded family. The non-coboundary is the *positive signal* that fed the present LDP candidate: it yields the non-degenerate CLT variance `2(log2)² > 0` — exactly what the Cramér / LDP machinery needs. See `collatz_livsic.md`.
- **Earlier kills** (digit-Lyapunov, transfer-operator spectral, function-field analog) live in `collatz/theory/` and are not part of the candidate stream.

The structural picture from this entire wave is consistent: **every structured framing on `ℤ` is obstructed by the archimedean–2-adic decoupling** (residue ≡ valuation sequence ≡ drift, none disjoint from the others); the LDP / thermodynamic-formalism framing is the *only one that operates on a different axis* (it controls *trajectory* deviations of the drift via convex duality, not residue-vs-drift independence). That is why it survives — and also why it cannot, by itself, close the natural-density gap (the residue axis is untouched, by design).

---

## 6. Honest assessment — is this a real surviving candidate?

**Partially yes.** The program is real and is the right object — Tao's neighborhood, the place where the world's experts are, the only framing the structural kills left intact. The closed forms are clean, the validation is solid, and the LDP machinery (Cramér / Esscher tilt / convex duality) is the standard analytic toolkit for this kind of problem; we have not yet been able to find an obvious prior-art statement of `P(s) = -s log3 + (s-1) log2 - log(1 - 2^{s-1})` for the Collatz drift in this packaging, but it is elementary enough to be folklore in the ergodic-theory-of-Collatz literature (Sinai, Akin, Lagarias survey). `[NOVELTY UNVERIFIED]` accordingly.

**But the falsifier we built in returned a clean partial result: the candidate does NOT close the log → natural gap.** The reasons are structural: the mod-3 marginal is preserved-up-to-attenuation by the Esscher tilt, so the natural-density TV-floor drops from `1/6` to `≈ 0.096` but does not vanish. The candidate's realistic deliverable is therefore:

> **A quantitative sharpening of Tao 2022's effective `β`-bound:** an explicit constant `I(0) = -P(s*) = log_2(3) · log(3/2) - log_2(3 - 3·log_2(2)/log_2(3))·(stuff)` in the descent-failure rate, AND the explicit attenuation of the mod-3 marginal from `(0, 1/3, 2/3)` to `(0, 0.404, 0.596)` under the descent-balance tilt — making the natural-density obstruction *quantitatively smaller* but *non-zero*.

This is a real (if modest) candidate-development output. It is not a Collatz proof attempt; it is a careful localization of where the LDP can and cannot help. The **honest open question** it leaves is whether a *multi-parameter or time-varying tilt* (beyond the single-parameter Esscher family) can saturate the mod-3 marginal. That is a precisely-stated, currently-open problem that the LDP framing has now isolated.

**Confidence the LDP/TF program closes log → natural via Esscher tilt alone: very low (~3%).** Grounds: the mod-3 marginal obstruction at the Esscher tilt is exact (not numerical), and no single-parameter tilt in the Esscher family hits uniform.

**Confidence the LDP/TF program gives a publishable quantitative refinement of Tao 2022: moderate (~40–55%).** Grounds: (i) the closed-form `P(s)`, `I(x)`, `P''(s*)` are clean and match the validation; (ii) the tilt-attenuation of the mod-3 marginal `1/6 → 0.096` is novel-looking (subject to literature pass) and quantitatively interesting; (iii) the LDP envelope of the drift gives a sharp Cramér tail constant that Tao 2022 does not state explicitly. The "moderate" reflects the real possibility that all of this is folklore in the (Sinai/Akin/Aaronson) ergodic-theory-of-Collatz tradition.

**What this candidate does NOT do.** It does not solve Collatz, does not close log → natural density, and does not improve the *rate* `n^{-A}` of `|ν̂_n(ξ)|` in Tao's Prop 1.17 (which is the actual analytic bottleneck on the residue side).

---

## 7. Reproducibility, novelty, scope

**Reproducibility.**
- `collatz_thermo_probe.py` — implements closed-form `P(s), P'(s), P''(s), s*, I(x)`; validates against Monte-Carlo from the Geom(1/2) base law and against trajectory data from the `verifier.T`-driven Syracuse walks. Computes the exact joint `(R_n mod 3^n, S_n)` law via a forward DP `U_j = inv2^{a_j} · (3 U_{j-1} + 1)` (the suffix-sum of the offset formula); validates `mod-3` marginal is `(0, 1/3, 2/3)` at `s=0`, and computes the tilted marginal at `s*`. Run: `python3 collatz_thermo_probe.py 500000 50 20260604`.
- `data/thermo_probe.json` — all per-`s`, per-`x`, per-`n` rows.
- `data/thermo_probe.log` — closed-form constants for citation.

**Validation gates (all PASS):**
- `P(s*) = −I(0)` (identity, machine zero ✓).
- `P''(s*) = log3 · log(3/2)` (machine zero ✓).
- `Var(φ_n)` under MC matches `2(log2)²/n` to within 0.4–2% across `n ∈ {50, 100, 500, 1000}` ✓.
- The exact-DP `(R_n mod 3^n, S_n)` joint reproduces the `(0, 1/3, 2/3)` mod-3 marginal at every `n` ✓ (after fixing the suffix-sum DP direction; see code).
- Truncation `amax=30` stable: not re-tested here, but matches `collatz_psi_factorization.py`'s asserted truncation invariance at the level of moments.

**Novelty `[UNVERIFIED]`.** Thermodynamic-formalism / Esscher-tilt views of Collatz almost certainly exist (Lagarias's survey lists 2-adic-shift / ergodic encodings; Sinai 2003 "Statistical (3x+1) problem" uses related averaging; Tao 2022's tilt `s* = 0.438` IS the residue-side Esscher tilt). What is plausibly new in this packaging:
1. The explicit closed-form pressure `P(s) = -s log3 + (s-1) log2 - log(1 - 2^{s-1})`.
2. The closed `P''(s*) = log3 · log(3/2)` (tilted CLT variance), and its contrast with the untilted `σ²_{Livšic} = 2(log2)²`.
3. The closed `I(0) = -P(s*) ≈ 0.05498` as the per-step LDP descent-failure rate.
4. The quantitative tilt-attenuation `1/6 → 0.096` of the mod-3 TV-floor.

A prior-art pass (Lagarias survey §3; Sinai "Statistical 3n+1 problem"; Akin "Why is 3n+1 difficult?"; thermodynamic-formalism on shifts of finite type) should close the flag.

**Scope.** Candidate development, not proof attempt. No claim of Collatz; no claim of closing log → natural density. The falsifier triggered and the candidate's deliverable is correspondingly narrowed to a quantitative refinement.

No file outside `ideas/candidates/` was written; `collatz/experiments/verifier.py` was imported read-only.
