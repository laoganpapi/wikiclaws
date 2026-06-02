# A Natural-Density Obstruction for the Scalar-Esscher Mixing Route to Tao's Syracuse Theorem

**Track:** Collatz, Vector A (upgrade Tao 2022 from logarithmic to natural density).
**Author:** Alex Ye (AI assistance disclosed separately).
**Status:** `[result — negative]`. The obstruction below is an unconditional, elementary fact about the Syracuse random variable; it has been re-derived from scratch (analytically and with two independent numerical implementations) for this document. Its *novelty* is **unverified** — see §6.
**Date:** 2026-06-02.

> **What this document is.** A clean, correct, standalone statement and proof of a **structural obstruction**: the specific change-of-measure route proposed in `tao_syracuse_explicit.md` §5–6 — upgrade Tao's logarithmic-density theorem to natural density by re-centering the Syracuse walk with a *single scalar Esscher tilt* `s*` and then asking for total-variation equidistribution of the tilted Syracuse law — **cannot work as stated**, because the Syracuse law's projection mod 3 is permanently `(0, 1/3, 2/3)`, never uniform, forcing `TV(nu_n, U) >= 1/6` for every `n`. This kills the stated Lemmas 6.1/6.2 of that document and the conditional theorem they support.
>
> **What this document is NOT.** It is **not** a proof of the Collatz conjecture, **not** a proof that Collatz natural density fails, and **not** a refutation of Tao's (logarithmic-density) theorem, which stands. It obstructs *one reduction strategy*, not the destination. Other change-of-measure mechanisms (coset-respecting reference measures; multi-parameter / operator tilts; arguments that never pass through this TV statement) remain entirely open. See §5 for the precise scope.
>
> **Supersedes** §§5–6 of `tao_syracuse_explicit.md` (the conditional theorem and its Plancherel lemmas), which are retracted; that document is retained for history and its surviving §4 localization is reproduced here in §2. The refutation originates in the red-team audit (`/home/user/wikiclaws/math/RED_TEAM_REPORT.md`, Doc 5); the analytic core has been independently verified for this writeup (§3.4).

---

## 1. Setup and notation

Notation follows `shared/notation.md` and `tao_syracuse_explicit.md`. Write `e(t) = e^{2*pi*i*t}`; `log` is natural; `nu_2`, `nu_3` are the `2`- and `3`-adic valuations; `phi(3^n) = 2*3^{n-1}` is Euler's totient.

The **Syracuse random variable** on `Z/3^n Z` is
$$
X_n \;:=\; \Syrac(\Z/3^n\Z) \;=\; \sum_{j=1}^{n} 3^{\,n-j}\,2^{-(a_j + a_{j+1} + \cdots + a_n)} \pmod{3^n},
$$
where `a_1, ..., a_n` are i.i.d. with the geometric law `P(a = k) = 2^{-k}`, `k in {1,2,3,...}` (mean `2`), and `2^{-1} = (3^n+1)/2 mod 3^n`. Its law is denoted `nu_n`; it is supported on the units `(Z/3^n Z)^x` (the leading `j=n` term `2^{-a_n}` is a unit mod 3 and an induction shows every partial sum stays a unit). We write `U` for the uniform measure on `(Z/3^n Z)^x`, i.e. `U(b) = 1/phi(3^n)` for `3 nmid b` and `0` otherwise.

For a real tilt `s > -1`, the **`s`-tilted Syracuse variable** `X_n^{(s)}` uses i.i.d. valuations with the exponentially-tilted geometric law
$$
P_s(a = k) \;\propto\; 2^{-k(1+s)}, \qquad k \ge 1,
$$
which is itself geometric with ratio `r = 2^{-(1+s)} in (0,1)` and mean `E_s[a] = 1/(1-r)`. The **descent-balance tilt** `s*` is the unique `s` with `E_s[a] = log_2 3 ~ 1.585` (so the multiplier `3^n 2^{-sum a_j}` has log-mean `0` and natural-density sampling is, to leading order, stationary). Solving `1/(1-r) = log_2 3` gives `r = 1 - 1/log_2 3 = 0.36907...`, hence
$$
s^* \;=\; -\log_2\!\big(1 - 1/\log_2 3\big) - 1 \;=\; 0.438033\ldots
$$
`% [CONSTANT UNVERIFIED vs primary]` — `s*` is an internal definition (not from the literature); its value is reproduced numerically below and in `experiments/verify_syracuse_rv.py`.

The collision diagnostic is
$$
\CP_n := \sum_b \nu_n(b)^2 = \|\nu_n\|_{\ell^2}^2, \qquad E_n := \varphi(3^n)\,\CP_n - 1 .
$$

---

## 2. The surviving localization: where log-density is forced (recap of `tao_syracuse_explicit.md` §4)

This section reproduces, unchanged in substance, the one part of the superseded document that survives the red-team. It is the honest *positive* expository content and the reason the scalar-Esscher route was proposed in the first place. Two facts:

**(L1) The dyadic decomposition is measure-neutral (Lemma 4.1 of the old doc, proved there in full).** Passing from `Syr_min` on odd integers to `Col_min` on all `N` via `N = 2^a m` (`m` odd) preserves natural-density-zero failure sets: if `{m odd : P(m) fails}` has natural density 0 among the odds, then `{N : P(N/2^{nu_2(N)}) fails}` has natural density 0 in `N`. *Consequence: the entire log-vs-natural gap lives in the odd-integer (Syracuse) statement, not in handling `nu_2`.*

**(L2) The essential appearance: stationarity of the sampling measure (Proposition 4.2 of the old doc).** Tao's transport scheme samples a starting odd `N_0`, runs the Syracuse first-passage map, and needs the sampling measure to be (approximately) preserved. On the log scale `u = log N`, the first-passage map acts as an approximate **translation** `u -> u - D_n` by the random log-drift
$$
D_n \;=\; \Big(\sum_{j=1}^n a_j\Big)\log 2 \;-\; n\log 3 .
$$
Lebesgue measure in `u` — i.e. the **logarithmic** measure `dN/N` — is translation-invariant, so it is (approximately) stationary; this is *why* Tao gets logarithmic density. Under **natural-density** sampling `dN`, the density on the `u`-line is `e^u du`, which a translation multiplies by the Radon–Nikodym factor `e^{-D_n}`. Because `D_n = (sum a_j)log2 - n log3` is itself a function of the orbit — correlated with the very residue mod `3^n` one is trying to equidistribute — this factor **couples size-distortion to residue**. Upgrading to natural density therefore requires controlling the *joint* law of `(residue mod 3^n, drift D_n)`, not merely the marginal residue.

> **The (now-refuted) hope.** The old §5 tried to discharge the `e^{-D_n}` factor by a single scalar Esscher tilt `s*` (the Cramér/Esscher conjugate to the drift), reducing the requirement to total-variation equidistribution `nu_n^{(s*)} -> U`. §3 shows this last step is impossible: no scalar tilt — `s*` or any other — can drive `nu_n` to `U` in TV, because the obstruction below is invariant under *every* scalar tilt.

This localization (L1)+(L2) is retained as **correct and the genuine expository contribution**; only the §5–6 attempt to *act* on it via a scalar tilt is withdrawn.

---

## 3. The mod-3 projection obstruction

### 3.1 The projection of `X_n` mod 3 is `(0, 1/3, 2/3)`, for every `n`

> **Lemma 3.1 (permanent mod-3 imbalance).** *For every `n >= 1`, the reduction `X_n mod 3` satisfies*
> $$
> \PP(X_n \equiv 0) = 0, \qquad \PP(X_n \equiv 1) = \tfrac13, \qquad \PP(X_n \equiv 2) = \tfrac23 .
> $$

*Proof.* Reduce the defining sum mod 3. For each `j < n` the term carries a factor `3^{n-j}` with `n - j >= 1`, hence `3^{n-j} \equiv 0 \pmod 3`. Only the `j = n` term survives:
$$
X_n \;\equiv\; 3^0 \cdot 2^{-a_n} \;=\; 2^{-a_n} \pmod 3 .
$$
Now `2 \equiv -1 \pmod 3`, so `2^{-a_n} \equiv (-1)^{-a_n} = (-1)^{a_n} \pmod 3`. Thus `X_n \equiv 1` iff `a_n` is even and `X_n \equiv 2 (\equiv -1)` iff `a_n` is odd; and `X_n \not\equiv 0` always (it is a unit). With `P(a = k) = 2^{-k}`,
$$
\PP(a_n \text{ even}) = \sum_{k \ge 1, \ k \text{ even}} 2^{-k} = \frac{1/4}{1 - 1/4} = \tfrac13, \qquad
\PP(a_n \text{ odd}) = \sum_{k \ge 1, \ k \text{ odd}} 2^{-k} = \frac{1/2}{1 - 1/4} = \tfrac23 .
$$
Hence `P(X_n \equiv 1) = 1/3`, `P(X_n \equiv 2) = 2/3`, `P(X_n \equiv 0) = 0`. The result is independent of `n` (the entire dependence collapsed to the single last valuation `a_n`). `∎`

Two remarks that make the obstruction robust:

- **It is exactly the `n=1` law.** `X_1 = 2^{-a_1} mod 3`, so the mod-3 marginal of `X_n` *equals* the law of `X_1` for all `n`. The imbalance is not an asymptotic artifact; it is frozen in at every level.
- **Under any scalar tilt it persists (and at `s*` it worsens).** Repeating the computation with `P_s(a = k) \propto r^k`, `r = 2^{-(1+s)}`, gives `P(a even) = r/(1+r)` and `P(a odd) = 1/(1+r)`, so
$$
\PP(X_n^{(s)} \equiv 1) = \frac{r}{1+r}, \qquad \PP(X_n^{(s)} \equiv 2) = \frac{1}{1+r}, \qquad \PP(X_n^{(s)} \equiv 0) = 0,
$$
which equals uniform-on-units (`1/2, 1/2`) only in the degenerate limit `r -> 1`, i.e. `s -> -1` (the non-summable edge). At the descent-balance tilt `s* = 0.438`, `r = 0.36907`, giving `(0, 0.2696, 0.7304)` — *more* imbalanced than untilted. **No admissible scalar tilt `s > -1` removes the mod-3 imbalance.**

### 3.2 Total variation is bounded below by the marginal imbalance

Let `pi : Z/3^n Z -> Z/3 Z` be reduction mod 3. Total variation cannot increase under a (deterministic) pushforward — the **data-processing inequality for total variation**:

> **Lemma 3.2 (TV data-processing).** *For probability measures `mu, rho` on a finite set `Omega` and any map `pi : Omega -> Omega'`,*
> $$
> \TV(\pi_*\mu, \ \pi_*\rho) \;\le\; \TV(\mu, \rho).
> $$
> *Proof.* `TV(mu, rho) = sup_{A subset Omega} |mu(A) - rho(A)|`. For any `B subset Omega'`, the preimage `pi^{-1}(B) subset Omega` satisfies `pi_*mu(B) - pi_*rho(B) = mu(pi^{-1}B) - rho(pi^{-1}B)`, whose absolute value is `<= TV(mu, rho)`. Taking the sup over `B` gives the claim. `∎`

### 3.3 The obstruction

> **Theorem 3.3 (the scalar-Esscher route is obstructed).** *For every `n >= 1` and every admissible scalar tilt `s > -1` (including `s = 0` and the descent-balance `s = s*`),*
> $$
> \boxed{\ \TV\big(\nu_n^{(s)}, \ U\big) \;\ge\; \frac{1}{1+r} - \frac12 \;=\; \frac{1 - r}{2(1+r)} \;>\; 0, \qquad r = 2^{-(1+s)},\ }
> $$
> *and in particular for the untilted law (`s = 0`, `r = 1/2`),*
> $$
> \TV(\nu_n, U) \;\ge\; \tfrac16 \qquad\text{for all } n .
> $$
> *Hence `nu_n^{(s)}` can never converge to `U` in total variation, for any fixed scalar tilt. The TV equidistribution demanded by Lemma 6.2 / Hypothesis MIX(theta) of `tao_syracuse_explicit.md` is unattainable; the conditional natural-density theorem (§5.3 there) fails in its stated form.*

*Proof.* Apply Lemma 3.2 with `mu = nu_n^{(s)}`, `rho = U`, `pi = (mod 3)`. The pushforward `pi_* nu_n^{(s)}` is the mod-3 marginal `(0, r/(1+r), 1/(1+r))` from §3.1. The pushforward `pi_* U` is the mod-3 marginal of uniform-on-units: the units `(Z/3^n Z)^x` split evenly between residues `1` and `2` mod 3 (the map `b -> b + 3^{n-1}` is a fixed-point-free involution... more simply, exactly `phi(3^n)/2 = 3^{n-1}` units lie in each class `1, 2 mod 3`), so `pi_* U = (0, 1/2, 1/2)`. Therefore
$$
\TV(\nu_n^{(s)}, U) \;\ge\; \TV\big(\pi_*\nu_n^{(s)},\, \pi_* U\big) \;=\; \tfrac12\Big( \big|\tfrac{r}{1+r} - \tfrac12\big| + \big|\tfrac{1}{1+r} - \tfrac12\big| \Big) \;=\; \big|\tfrac{1}{1+r} - \tfrac12\big| \;=\; \frac{1-r}{2(1+r)},
$$
using `|r/(1+r) - 1/2| = |1/(1+r) - 1/2| = (1-r)/(2(1+r))` and that the mass at residue 0 contributes `|0 - 0| = 0`. For `s = 0`, `r = 1/2`: `(1 - 1/2)/(2 * 3/2) = (1/2)/3 = 1/6`. `∎`

> **Corollary 3.4 (the diagnostic must diverge — the Plancherel reading).** *Since the `ell^2 -> TV` Cauchy–Schwarz bound `TV(nu_n, U) <= (1/2) sqrt(E_n)` (with `E_n = phi(3^n) CP_n - 1`, derived below) is the only lever MIX(theta) pulls, and the left side is bounded below by `1/6 > 0`, the bound can deliver `TV -> 0` only if `E_n -> 0`. The obstruction does not by itself force `E_n -> infinity` (TV is the marginal-controlled quantity, `E_n` the full-ring `ell^2` quantity), but it removes the only mechanism by which small `E_n` could have been argued, and §4 shows that in fact `E_n` diverges — so both the necessary condition fails and the sufficient mechanism is gone.*

For completeness, the `ell^2`-to-TV chain used throughout (verified numerically in §3.4): because `nu_n` and `U` are both supported on the `phi(3^n)` units, `nu_n - U` is supported there, so
$$
\langle \nu_n, U\rangle = \tfrac{1}{\varphi(3^n)}, \qquad
\|\nu_n - U\|_{\ell^2}^2 = \CP_n - \tfrac{1}{\varphi(3^n)}, \qquad
\TV(\nu_n,U) = \tfrac12\|\nu_n-U\|_{\ell^1} \le \tfrac12\sqrt{\varphi(3^n)}\,\|\nu_n-U\|_{\ell^2} = \tfrac12\sqrt{E_n}.
$$
The last step is Cauchy–Schwarz over the `phi(3^n)`-element support. This is the (correct) content of the old Lemma 6.1 once the `3 | xi` Fourier mass is *not* discarded; the old doc's error was to drop it (see §3.5).

### 3.4 Independent verification (this writeup did not trust the red-team)

Per the project's adversarial protocol, every load-bearing claim here was re-derived and re-checked with code that does **not** share the FFT pipeline of `experiments/syracuse_fft/`. An independent forward-DP implementation of `nu_n` (brute-force distribution propagation, geometric tail truncated at `a <= 55` and renormalized) gives, for `n = 1, ..., 6`:

| `n` | mod-3 marginal of `nu_n` | marginal-`TV` vs `(0,1/2,1/2)` | full `TV(nu_n, U)` | full `>=` marginal? |
|---|---|---|---|---|
| 1 | `(0, 0.33333, 0.66667)` | `0.16667` | `0.16667` | yes (tight) |
| 2 | `(0, 0.33333, 0.66667)` | `0.16667` | `0.27778` | yes |
| 3 | `(0, 0.33333, 0.66667)` | `0.16667` | `0.34601` | yes |
| 4 | `(0, 0.33333, 0.66667)` | `0.16667` | `0.37054` | yes |
| 5 | `(0, 0.33333, 0.66667)` | `0.16667` | `0.38887` | yes |
| 6 | `(0, 0.33333, 0.66667)` | `0.16667` | `0.39855` | yes |

The mod-3 marginal is exactly `(0, 1/3, 2/3)` at every `n`; the full TV exceeds `1/6` and grows (toward, empirically, `~0.4`); the data-processing inequality `full >= marginal` holds with equality only at `n = 1`. The identities `<nu, U> = 1/phi`, `||nu - U||_2^2 = CP - 1/phi`, and `TV <= (1/2)sqrt(E_n)` were each checked to machine precision. The tilted marginals `(0, r/(1+r), 1/(1+r))` were verified at `s = 0, s*, -0.5`, giving marginal-TV `0.16667, 0.23042, 0.08579` respectively, matching §3.1. **The red-team's claim is correct.** (Had it been wrong, this section would say so; it is not.)

### 3.5 What exactly was wrong in the superseded document

For the record (and to prevent the error recurring): old Lemma 6.1 wrote
$$
\|\nu - U\|_{\ell^2}^2 \;\stackrel{(\times)}{\le}\; \frac{1}{3^n}\sum_{3\nmid\xi}|\widehat\nu(\xi)|^2,
$$
i.e. it discarded the Fourier mass at frequencies `3 | xi`, asserting the discrepancy is "carried entirely by `{3 nmid xi}`." But the mod-3 imbalance of Lemma 3.1 means precisely that `nu_n` differs from `U` *across the cosets mod 3*, and that difference is encoded exactly in the `3 | xi` coefficients. Numerically the inequality `(×)` is **false** already at `n = 2` (LHS `0.0714 >` claimed bound `0.0529`) and `n = 3` (`0.0409 > 0.0171`). Since `MIX(theta)` only controls the `3 nmid xi` coefficients, it cannot bound the `3 | xi` mass, cannot bound the full `ell^2` distance, and cannot deliver `TV -> 0`. The exponent `3^{n/2}` in the `ell^2 -> TV` passage is correct; the error was *which* frequencies `MIX` governs. (Charitable note: Tao's actual Proposition 1.17 also bounds only `3 nmid xi` — consistent with the truth that the coset part is handled by a separate device in his framework, further evidence that folding it into one Plancherel line over-claims.)

---

## 4. Numerical corroboration: the diagnostic `E_n` diverges, and a phase transition

The obstruction (§3) is exact and `n`-independent. The companion FFT experiment (`experiments/syracuse_fft/`, exact law on `Z/3^n` via an `O(3^n)`-memory forward recursion, cross-checked against an independent direct DP for `n = 2..6` and Plancherel-validated at every `n`) measures the *full-ring* diagnostic `E_n` and shows it not only fails to vanish but **diverges**, with no turnover, out to the memory frontier.

**Untilted (`s = 0`) — linear divergence.** `E_n` for `n = 2..17`:
`0.429, 0.736, 1.046, 1.356, 1.667, 1.977, 2.288, 2.599, 2.911, 3.223, 3.535, 3.848, 4.162, 4.476, 4.790, ...`
with constant successive differences `~0.312`:
$$
E_n \approx 0.3117\,n - 0.2045 \quad (\text{fit on } n \ge 5,\ \text{residual} < 3\times10^{-3}).
$$
So `CP_n = 3^{-n} poly(n)` (exactly `beta = 1` order with a linearly growing polynomial correction) and `TV(nu_n, U) ~ (1/2)sqrt(0.31 n) -> infinity` (slowly). **No turnover through `n = 17`.**

**Descent-balance Esscher tilt (`s = s* = 0.438`) — exponential divergence.** `E_n^{(s*)}` for `n = 2..17`:
`0.85, 1.77, 3.09, 4.97, 7.64, 11.42, 16.74, 24.22, 34.70, 49.36, 69.85, 98.42, 138.23, 193.6, ...`, fitting
$$
E_n^{(s*)} \approx 0.92 \cdot (1.434)^n \quad (\text{log-linear fit on } n \ge 6),
$$
successive ratios declining slowly (`2.08 -> 1.40`) but staying firmly above 1. **No turnover and no sign of one through `n = 17`.** The single scalar tilt the natural-density transport *requires* makes equidistribution *exponentially worse*.

**The phase transition (the structural explanation).** Sweeping `E_n(s)` over `s > -1` reveals a clean transition near `s_c ~ -0.4` (mean valuation `E[a] ~ 3`):
- for `s <~ -0.45` (tail *fattened*, `E[a] > 2`), `E_n` is **bounded** in `n` and `-> 0` as `s -> -1^+` (e.g. `s = -0.9` gives `E_n = 0.0044` flat across `n`); the law equidistributes;
- for `s >~ -0.4`, `E_n` **grows** (linearly at `s = 0`, exponentially at `s*`).

The two requirements are **incompatible under any scalar tilt**:
> *mean-drift-neutrality* (needed for natural-density **stationarity**, §2-L2) wants `E[a] = log_2 3 ~ 1.585`, i.e. `s* = +0.438`;
> *residue-spreading* (needed for **equidistribution**, `E_n -> 0`) wants `E[a] >~ 3`, i.e. `s <~ -0.45`.
> `s*` lands firmly on the **non-equidistributing** side of `s_c`.

Frequency-localized (`v_3(xi)`-stratified) and `n`-dependent tilts were tested and **do not change the picture** (`E_n` still diverges, driven by the high-frequency / small-`v_3` strata where the descent-balance tilt must be applied). Full data, figures, and the divergence/turnover analysis are in `experiments/syracuse_fft/results.md`.

> **Consistency with §3.** The exact obstruction `TV >= 1/6` lives in the **mod-3 marginal** (the `3 | xi` frequencies). The diagnostic `E_n` is the **full-ring** `ell^2` excess (all frequencies). These are different quantities — `E_n` could in principle diverge while the marginal stays balanced, or vice versa — and the experiment shows they fail *together*: the marginal is permanently imbalanced (§3), *and* the full diagnostic diverges (§4). The phase transition explains the mechanism: the unique scalar tilt that re-centers the drift is exactly the one that maximizes (rather than cancels) the residue collision.

---

## 5. Honest scope: what is and is not obstructed

**Obstructed (this is the result):** The route of `tao_syracuse_explicit.md` §5–6 — discharge the natural-density Radon–Nikodym factor `e^{-D_n}` by a **single scalar Esscher tilt** `s`, then obtain natural density from **total-variation convergence** `nu_n^{(s)} -> U` of the tilted Syracuse law toward uniform-on-units. By Theorem 3.3 this convergence is impossible for every scalar `s`; by §4 the associated diagnostic diverges. Lemmas 6.1/6.2 and Conditional Theorem 5.2 of that document are withdrawn.

**NOT obstructed (open):**
1. **Coset-respecting reference.** Compare `nu_n` not to uniform-on-units `U` but to the measure that is uniform *within* the mod-`3^k` coset structure the offset actually realizes (so the fixed coset masses are not counted as discrepancy). The mod-3 imbalance is *built into the correct target* and the TV obstruction evaporates by construction. Whether the rest of Tao's transport then closes in natural density is open — this is the natural next reduction and is **not** addressed here. (Tao's own framework handles the coset part by a separate device, consistent with this.)
2. **Non-scalar change of measure.** A genuinely multi-parameter tilt, an operator/`xi`-dependent reweighting outside the scalar-geometric family, or a tilt acting on the *joint* `(residue, drift)` law rather than the marginal valuation, is not covered by Theorem 3.3 (which is specifically about scalar tilts of the i.i.d. valuation law). The phase-transition data suggest scalar tilts cannot satisfy both constraints, but a non-scalar mechanism is unconstrained by it.
3. **Mechanisms that never pass through this TV statement.** Any natural-density argument that does not factor through "`nu_n^{(s)} -> U` in TV" is untouched.

**Says nothing about:**
- **Whether Collatz natural density is true.** A failure of *this reduction* is not evidence either way for the destination. Tao's logarithmic-density theorem is unaffected and stands.
- **Tao's `beta = 1` conjecture.** All of `E_n` here (even the exponential `s*` case, `~1.43^n < 3^n`) is `3^{o(n)}`, hence perfectly consistent with `beta = 1` (`CP_n = 3^{-n + o(n)}`). The obstruction concerns the strictly stronger *exact-leading-constant* requirement `E_n -> 0`, not `beta = 1`, which remains open and untouched.

In one line: **the scalar-Esscher MIX(theta) route to natural density is dead; the natural-density question, and every other route to it, is alive.**

---

## 6. Novelty and verification status

`% [PRIOR-ART CHECK PENDING]` **The novelty of this obstruction is UNVERIFIED.** The mod-3 imbalance of the Syracuse random variable is elementary (it is literally the `n = 1` law) and is very plausibly **already known to Tao or folklore** — Tao's Proposition 1.17 bounding only the `3 nmid xi` frequencies is *consistent with his being aware* that the coset part needs separate treatment. We therefore phrase the contribution defensively: **we observe / make explicit** that this elementary fact *obstructs the specific scalar-Esscher TV-equidistribution reduction*, and we corroborate it numerically (the `E_n` divergence and the tilt-space phase transition, which we do believe are not previously recorded *in this packaging* — also `% [PRIOR-ART CHECK PENDING]`). We do **not** claim to have discovered the mod-3 imbalance. Settling priority requires the primary sources (Tao arXiv:1909.03562 §1, §7; Tao's 2020 blog "Equidistribution of Syracuse random variables"), which were HTTP-403 in this environment.

**Constants/citations.** `s* = 0.438033...` is an internal definition, reproduced numerically. The `E_n` data are from the committed scripts (`experiments/syracuse_fft/`), cross-validated two independent ways. No external numerical constant is load-bearing for §3 (the obstruction is exact rational arithmetic: `1/3, 2/3, 1/2, 1/6`). The framework attributions (Syracuse RV, offset map, `beta`, Prop 1.17) are to Tao and are reproduced from secondary sources in `tao_syracuse_explicit.md` §2 (`% [CONSTANT UNVERIFIED vs primary]` for anything traced only to secondary reproductions).

**Protocol status.** §3 (the obstruction) is elementary and has passed independent re-derivation (analytic + two numerical implementations); it is the citable deliverable. §4 is numerics (reproducible; informs but does not prove the asymptotic). §2 is expository (attributions to Tao). This document is `[result — negative]`; its weakest non-elementary point is the *novelty* question of §6, which a prior-art pass against the primary sources must close before any "we make explicit" is upgraded.

---

## 7. Summary

1. **`X_n mod 3` is permanently `(0, 1/3, 2/3)`** (Lemma 3.1): it equals the `n = 1` law for all `n`, because only the last valuation `a_n` survives mod 3, and `2^{-a_n} \equiv (-1)^{a_n}`.
2. **Hence `TV(nu_n^{(s)}, U) >= (1-r)/(2(1+r)) > 0` for every scalar tilt `s` (`r = 2^{-(1+s)}`)**, in particular `>= 1/6` untilted (Theorem 3.3), by TV data-processing under reduction mod 3. **No scalar Esscher tilt can equidistribute the Syracuse law in TV.**
3. **The full-ring diagnostic `E_n` diverges** — linearly untilted, exponentially (`~1.43^n`) at the required descent-balance tilt — with no turnover to `n = 17`, and there is a tilt-space **phase transition** at `s_c ~ -0.4` that strands the descent-balance tilt on the non-equidistributing side (§4).
4. **Therefore the scalar-Esscher MIX(theta) route of `tao_syracuse_explicit.md` §5–6 is obstructed** (those sections are superseded). This says **nothing** about whether Collatz natural density holds, leaves coset-respecting and non-scalar reductions **open**, and does not touch Tao's theorem or `beta = 1`.
5. **Novelty unverified** (§6): the mod-3 fact is likely folklore/known to Tao; we make it explicit *as an obstruction to this reduction* and corroborate numerically, pending a primary-source prior-art pass.
