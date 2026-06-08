# Decisive FFT experiment: the Syracuse collision diagnostic E_n at large n

**Track:** Collatz, Vector A (Tao log → natural density via Syracuse mixing on
`(Z/3^n Z)^x`).
**Author:** Alex Ye (computational experiment; AI assistance disclosed separately).
**Status:** `[numerics]` — reproducible; this informs, but does not resolve, an
analytic question. All numbers come from the committed scripts in this directory.
**Date:** 2026-06-02.

This experiment resolves the open question flagged in
`theory/tao_syracuse_explicit.md` §6.4/§7 and `PROGRESS.md` (Phase-3 task 1):
the prior agent found, on `n ≤ 6`, that the collision diagnostic

> `E_n := φ(3^n) · CP_n − 1`,  `CP_n = Σ_b P(Syrac=b)^2`,  `φ(3^n)=2·3^{n-1}`,
> `TV(ν_n, U) ≤ ½√(E_n)`,  so **`E_n → 0` is the (exact-leading-constant)
> natural-density requirement**,

appears to **diverge** — both untilted and at the descent-balance Esscher tilt
`s* ≈ 0.438` (the tilt with `E_{s*}[a]=log_2 3`, which makes natural-density
sampling stationary). The prior agent could not tell whether this was a genuine
obstruction or a small-`n` artifact, and recommended pushing `E_n` to `n ≈ 10–14`
via FFT and testing ξ-dependent tilts. That is done here.

---

## 1. Method and the mandatory cross-check

**Algorithm (`syracuse_fft.py`).** The Syracuse RV admits the forward recursion
(derived and Monte-Carlo–verified, `reference_bruteforce.py` + `crosscheck.py`)

> `W_m = 2^{-a_m} (W_{m-1} + 3^{n-m})  (mod 3^n)`,  `W_0 = 0`,  `X_n = W_n`,

whose state is a single residue in `Z/3^n`. Each step is (i) add the constant
`3^{n-m}` (a cyclic shift of the length-`3^n` law vector), then (ii) multiply by
`2^{-a_m}`, `a_m` ~ `s`-tilted geometric. Since `2` is a primitive root mod `3^n`,
multiply-by-`2^{-k}` is a **shift in the discrete log within each 3-adic
valuation shell**, so the geometric average is an **FFT cyclic correlation per
shell**. This gives the **exact** law in `O(n·3^n·log 3^n)` time and `O(3^n)`
memory — no truncation (geometric tails summed in closed form), no Monte-Carlo
error. This is what breaks the `n ≤ 6` ceiling of the direct `(R, suffix-sum)` DP
(which is `O(3^{2n})`).

**Cross-check `n=2..6` (NON-NEGOTIABLE): PASS.** `crosscheck.py` compares the FFT
law against an independent exact direct DP (the prior agent's algorithm,
re-implemented from scratch) and against the prior agent's *published* `E_n`
values, for **both** tilts:

| n | E_n (FFT) untilted | published | E_n (FFT) s* | published | max law err |
|---|--------------------|-----------|--------------|-----------|-------------|
| 2 | 0.428571 | 0.429 | 0.853606 | 0.854 | 5.6e-17 |
| 3 | 0.736288 | 0.736 | 1.771860 | 1.772 | 5.6e-17 |
| 4 | 1.045764 | 1.046 | 3.090289 | 3.090 | 8.3e-17 |
| 5 | 1.356107 | 1.356 | 4.972008 | 4.972 | 4.2e-17 |
| 6 | 1.666887 | 1.667 | 7.642963 | 7.643 | 2.4e-17 |

FFT law = exact DP law to `< 1e-15` everywhere; `E_n` matches the published values
exactly at their printed precision. **CP_n is additionally cross-validated by
Plancherel** (`CP_n = (1/3^n)Σ|φ_n(ξ)|^2`) at every `n` to `~1e-16`, the law is
verified supported on units (zero mass on multiples of 3), and is non-negative.

**Largest `n` reached: `n = 15`** (`3^15 ≈ 1.43×10^7`; ~52 s/case). The trend
tables go to `n = 14`; spot values at `n = 15` confirm them.

---

## 2. Results: E_n vs n (the verdict)

Raw data: `data/En_results.json`, `data/En_*.csv`, run log `data/run_log.txt`.
Figures: `figures/fig1_En_logscale.png` … `fig4_xi_dependent.png`.

### 2.1 Untilted (`s = 0`) — **DIVERGES LINEARLY** (no turnover)

`E_n` for `n = 2..14`: `0.429, 0.736, 1.046, 1.356, 1.667, 1.977, 2.288, 2.599,
2.911, 3.223, 3.535, 3.848, 4.162` (and `E_15 = 4.476`). The successive
differences are essentially constant at `≈ 0.312`:

> **`E_n ≈ 0.3117·n − 0.2045`** (linear fit on `n ≥ 5`, residual `< 2.7e-3`).

No turnover anywhere up to `n = 15`. So `TV(ν_n,U) ~ ½√(0.31 n) → ∞`, slowly. This
**confirms and extends** the prior agent's `n≤6` finding (`E_n ≈ 0.31 n`): the
untilted Syracuse law is `CP_n = 3^{-n}·poly(n)` — exactly **`β=1` order with a
linearly growing polynomial correction** — and does **not** approach uniform in
total variation.

### 2.2 Descent-balance Esscher tilt (`s* ≈ 0.438`) — **DIVERGES EXPONENTIALLY**

`E_n` for `n = 2..14`: `0.85, 1.77, 3.09, 4.97, 7.64, 11.42, 16.74, 24.22, 34.70,
49.36, 69.85, 98.42, 138.23` (and `E_15 = 193.6`). This is **geometric growth**:

> **`E_n ≈ 0.92·(1.434)^n`** (log-linear fit on `n ≥ 6`).

The successive ratios `E_n/E_{n-1}` decline slowly (`2.08 → 1.40`) but stay
**firmly above 1** (extrapolating to `≈ 1.32–1.40`); the increments `dE` themselves
grow geometrically. There is **no turnover and no sign of one** up to `n = 15`.

> **VERDICT (decisive question).** `E_n^{(s*)}` does **not** plateau and does **not**
> turn over: it **grows exponentially** (`~1.43^n`), confirmed to `n = 15`. The
> prior agent's `n ≤ 6` finding that "the descent-balance tilt makes equidistribution
> worse, not better" is **NOT a small-`n` artifact** — it is the genuine asymptotic
> behavior, and far stronger than the small-`n` data alone suggested (super-linear
> at `n≤6` sharpens into clean exponential by `n≈10`).

So **via this diagnostic, `β=1` is necessary but provably insufficient** for the
natural-density upgrade as routed through `MIX(θ)`: even granting `β=1`
(`CP_n = 3^{-n+o(n)}`, i.e. `E_n = 3^{o(n)}`), the *exact-leading-constant*
requirement `E_n^{(s*)} → 0` that Conditional Theorem 5.2 needs **fails** for the
descent-balance-tilted law, for **both** `s=0` and `s=s*`.

### 2.3 The new structural finding: an equidistribution **phase transition** in tilt space

Computing `E_n(s)` over the full valid tilt range `s > −1` (the tilted geometric
`P_s(a=k) ∝ 2^{-k(1+s)}` is summable only for `s > −1`) reveals a clean
transition (`figures/fig3_tilt_sweep.png`):

- **For `s ≲ −0.45`: `E_n` is BOUNDED in `n`** — the `n=4, 8, 12` curves *coincide*
  (the law equidistributes). Examples (flat across `n = 2..15`):
  `s=−0.50 → E_n = 0.149`; `s=−0.90 → E_n = 0.00445` (constant to `1e-16`);
  `s=−0.95 → E_n = 0.0011`. As `s → −1^+`, the bounded limit `→ 0`.
- **For `s ≳ −0.4`: `E_n` GROWS with `n`** — slowly near the crossover (`s=−0.3`:
  `E_n → ~0.47`, creeping), linearly at `s=0`, exponentially at `s=s*`.
- The crossover sits near `s_c ≈ −0.4`, i.e. mean valuation `E[a] ≈ 3` — a tail
  **fatter** than the untilted `E[a]=2` (more valuation-entropy ⇒ better mixing).

**Why this is the crux, stated honestly.** Equidistribution (`E_n` bounded, even
`→ 0`) **is achievable** by a single ξ-independent tilt — but only with a
**negative** tilt `s ≲ −0.45` that *fattens* the valuation tail. The
**descent-balance** tilt that the natural-density transport mechanism *requires*
is **positive** (`s* = +0.438`, `E_{s*}[a] = log_2 3 ≈ 1.585`, tail *thinned*),
which is **deep in the divergent regime**, on the opposite side of `s_c` from the
equidistributing tilts. The two requirements pull in opposite directions:

> mean-drift-neutrality (needed for *natural-density stationarity*) wants
> `E[a] = log_2 3 ≈ 1.585` (`s* > 0`); high-entropy spreading (needed for
> *residue equidistribution*, `E_n → 0`) wants `E[a] ≳ 3` (`s ≲ −0.45`).
> **No scalar tilt satisfies both.** `s*` lands firmly on the non-equidistributing
> side.

This is a sharper, quantified version of the prior agent's §6.5 remark ("the tilt
re-centers the mean but does not by itself produce cancellation"): the
descent-balance constraint forces a tilt at which, empirically, there is no
exponential (or even bounded-TV) cancellation.

---

## 3. ξ-dependent tilts (do they change the picture?) — **NO**

Two schemes (`run_experiment.py`), since the prior agent conjectured a ξ- or
n-dependent tilt "might behave differently":

- **XI-A, per-ξ "best-envelope":** for each frequency `ξ`, take the *minimum*
  `|φ_n^{(s)}(ξ)|` over a grid of scalar tilts, then form `E_n` from this
  optimistic lower envelope. This is **degenerate**: the per-ξ argmin collapses to
  a *single* near-edge tilt `s ≈ −0.95` for **all** `ξ`, and the envelope value
  just tracks that one scalar plateau tilt (`E_n ≈ 0.001`, flat). It exhibits **no
  genuine ξ-dependence** — it merely rediscovers §2.3.

- **XI-B, `v_3(ξ)`-stratified tilt:** assign the tilt by the frequency's 3-adic
  valuation `L = v_3(ξ)` — the only natural invariant of `ξ` under the
  `(Z/3^n)^x` action. Tested schedule: descent-balance `s*` on the genuinely
  oscillatory strata (`L ≤ n/2`) and a plateau tilt `−0.5` on the near-DC strata
  (`L > n/2`). Result: `E_n` still **diverges** (`E_12 = 65.0`), tracking the pure
  `s*` curve (`figures/fig4_xi_dependent.png`). The divergence is **driven by the
  small-`v_3` (high-frequency) strata**, which is exactly where the
  descent-balance tilt must be applied — so frequency-localizing the tilt cannot
  rescue it.

- **n-dependent partial Esscher** (`s_n = s*(1 − 1/√n)`): intermediate; still
  diverges (`E_14 = 57.9`).

> **VERDICT (ξ-dependence).** Within the natural family of frequency-localized
> Esscher tilts, **ξ-/n-dependence does not change the picture.** The only way the
> data find to make `E_n` bounded is a single *scalar negative* tilt — which
> violates the descent-balance constraint. So reading (ii) of §6.4 ("the correct
> object is a ξ-dependent tilt") is **not supported** by these experiments: no
> frequency-local Esscher reweighting beats one scalar plateau tilt, and the one
> that bounds `E_n` is the wrong tilt for the transport argument.

---

## 4. What this does and does NOT tell us about β=1

**What the data DO suggest (quantified):**

1. The **untilted** Syracuse law has `E_n ≈ 0.31 n → ∞` (linear), confirmed to
   `n = 15`. TV does not go to 0. *(So `β=1` order alone ⇏ TV→0.)*
2. The **descent-balance-tilted** law has `E_n ≈ 0.92·1.43^n → ∞` (exponential),
   confirmed to `n = 15`, **no turnover**. The single scalar Esscher tilt `s*` that
   the natural-density transport needs makes equidistribution *exponentially*
   worse. *(So the specific hypothesis `MIX(θ)` — `E_n^{(s*)}→0` at a geometric
   rate — is, on this evidence, FALSE: `E_n^{(s*)}` grows geometrically, the exact
   opposite.)*
3. Equidistribution (`E_n` bounded, `→0`) is achievable, but only by **negative**
   tilts `s ≲ −0.45` that violate descent-balance. There is a clean phase
   transition at `s_c ≈ −0.4` (`E[a] ≈ 3`); `s*` is on its divergent side.
4. **ξ-/n-dependent tilts do not help** (within frequency-localized Esscher
   schemes).

**What the data do NOT establish (the honest limits):**

- **This is numerics, not proof.** "`E_n^{(s*)} → ∞`" is an empirical trend fit on
  `n = 2..15`; the ratios `E_n/E_{n-1}` are *still slowly decreasing* (`→ ~1.32–
  1.40`). The data **strongly** indicate exponential divergence with no turnover,
  but cannot logically exclude a turnover at some `n ≫ 15`. To push the verdict
  from "strongly suggested" to "morally certain," one would want `n ≈ 18–20`
  (feasible memory-wise at `n=16`: `3^16≈4.3×10^7` floats `≈ 0.35 GB`; `n=18`:
  `~3 GB`; the FFT cost is `~3×` per step in `n`). Nothing in the *shape* of the
  data hints at a turnover, however.
- **`β=1` itself is untouched.** `β=1` is the statement `CP_n = 3^{-n+o(n)}`, i.e.
  `E_n = 3^{o(n)}`. Our `E_n` (even the exponential `s*` case, `~1.43^n`) is
  `3^{o(n)}` since `1.43 < 3` — so **all of these results are perfectly consistent
  with `β=1`**, and say nothing for or against it. What they address is the
  *strictly stronger* exact-leading-constant requirement `E_n → 0` that
  `MIX(θ)`/Conditional Theorem 5.2 needs. The experiment confirms, decisively and
  at large `n`, that **`β=1` is necessary but not sufficient for the
  natural-density upgrade via this route**, and that the drift-tilt does not
  repair the gap — it widens it.
- **Whether natural density holds is still an analytic question.** A failure of
  `E_n^{(s*)} → 0` does **not** prove natural density fails for Collatz: (a) the
  conditional theorem's hypothesis could be loosened (e.g. a different
  change-of-measure than the single Esscher tilt, or a genuinely multi-parameter /
  operator tilt outside the scalar-geometric family tested here), or (b) the
  natural-density upgrade could hold by a mechanism that does not factor through
  `MIX(θ)` at all. What the data *do* sharpen: the **specific** route in
  `tao_syracuse_explicit.md` (scalar Esscher tilt at descent-balance ⇒ exponential
  Fourier decay) is, on this evidence, **not viable as stated** — the tilt it
  prescribes is on the wrong side of the equidistribution transition.

**Bottom line.** The "`E_n` diverges, so `β=1` is insufficient (via this route)"
finding is **real, not a small-`n` artifact**: untilted `E_n` diverges linearly and
descent-balance-tilted `E_n` diverges *exponentially*, both with no turnover up to
`n=15`. The new structural fact — an equidistribution phase transition at
`s_c ≈ −0.4`, with the descent-balance tilt `s* = +0.438` stranded on its divergent
side — explains *why* and shows the obstruction is the **incompatibility of
drift-neutrality with residue-spreading under any single scalar tilt**, not a
shortage of data. This points away from a natural-density upgrade *through the
scalar-Esscher `MIX(θ)` route specifically*, while leaving the broader
natural-density question (and `β=1`) open and analytic.

---

## 5. Files

| File | Purpose |
|------|---------|
| `syracuse_fft.py` | FFT W-recursion: exact law on `Z/3^n`, `E_n`, `CP_n`. O(3^n) memory. |
| `reference_bruteforce.py` | Independent exact direct-DP reference (prior agent's algorithm). |
| `crosscheck.py` | **Mandatory `n=2..6` check** vs DP and published values. Run: `python3 crosscheck.py` (exit 0 = PASS). |
| `run_experiment.py` | Driver: all tilt schemes + tilt-sweep → `data/`. Run: `python3 run_experiment.py 14`. |
| `make_figures.py` | Builds the four figures from `data/En_results.json`. |
| `data/En_results.json`, `data/En_*.csv`, `data/run_log.txt` | Raw results. |
| `figures/fig1_En_logscale.png` | `E_n` vs `n` (log y), all scalar schemes. |
| `figures/fig2_tilted_vs_untilted.png` | untilted (linear fit) vs `s*` (exp fit). |
| `figures/fig3_tilt_sweep.png` | `E_n(s)` — the equidistribution phase transition. |
| `figures/fig4_xi_dependent.png` | ξ-dependent schemes vs scalar baselines. |

**Reproduce:** `python3 crosscheck.py && python3 run_experiment.py 14 && python3 make_figures.py`.
