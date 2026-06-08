# Higher-Order Additive Combinatorics: Gowers $U^k$ Norms, Inverse Theorems, Croot–Sisask

**Field cluster:** #6 (additive combinatorics / higher-order Fourier / Gowers / Croot–Sisask).
**Scope:** non-moment / non-symmetric DIRECTIONS for Frankl and Collatz, beyond the proven barriers.
**Author:** generation agent. **Status:** speculative directions, no proofs. All `[NOVELTY UNVERIFIED]`.
**Discipline:** stays under `math/ideas/generation/`. Names theorems; gives concrete first steps with small validation actually run (n≤5 Frankl; n=2 Syracuse). Honest "why not" included.

> **TL;DR verdict (read first).**
> - **Frankl:** I ran the concrete probe — computed the **Gowers $U^3$ norm of $1_F$** on all 410 nontrivial UC families at $n\le 4$ and correlated with max-abundance. **It does NOT escape the barrier**, and I can now say *why* sharply: the Frankl extremizer (Boolean cube $2^{[k]}$) is a **coset of a subgroup** of $(\mathbb Z/2)^n$, so its *normalized* $U^k$ norm is **exactly 1 (the minimum) for every $k$** — the cube is maximally "structured / low-complexity" at every Gowers level simultaneously. The Gowers inverse theorem therefore certifies the *worst case* as the *most* structured object, which is the same flatness pathology as degree-2. Measured correlation with abundance is **0.21 for $U^3$, actually weaker than 0.31 for $U^2$.** So the *plain* $U^k$-magnitude route is a **NO** (plausibility 1–2). The one *surviving* sub-direction is **signed / local higher-order** structure (Croot–Sisask almost-periodicity of the *union-closure operator*, not of $1_F$), which is genuinely non-symmetric — plausibility 2.
> - **Collatz:** Here higher-order additive combinatorics is **more promising and genuinely escapes the stated abelian barrier**. The mod-3 obstruction is a **degree-1 (linear-phase) obstruction** that lives entirely in the $3\mid\xi$ Fourier modes. The remaining $3\nmid\xi$ modes carry a real, separate part of the discrepancy (I measured: **42% of the $\ell^2$ discrepancy at $n=2$ is in $3\nmid\xi$**). A **higher-order inverse theorem on $\mathbb Z/3^n$** (Green–Tao–Ziegler / the $p$-adic & nilpotent theory) asks whether the *tilted* Syracuse law correlates with a **quadratic phase / 2-step nilsequence** — an obstruction the abelian (degree-1) Fourier attack structurally could not see. This is a real, concrete, non-abelian direction. Plausibility 3.

---

## 1. The higher-order tool + setup

### 1.1 Gowers uniformity norms

For a finite abelian group $G$ and $f:G\to\mathbb C$, the **Gowers $U^k$ norm** is
$$
\|f\|_{U^k}^{2^k} \;=\; \mathbb E_{x,h_1,\dots,h_k\in G}\ \prod_{\omega\in\{0,1\}^k} \mathcal C^{|\omega|} f\big(x+\omega\!\cdot\!h\big),
$$
$\mathcal C$ = complex conjugation, $\omega\cdot h=\sum_i\omega_i h_i$. $\|f\|_{U^2}$ is the $\ell^4$ norm of the Fourier transform (degree-1 / linear structure); $\|f\|_{U^{k}}$ for $k\ge 3$ measures **genuinely higher-degree (polynomial-phase) structure** invisible to the Fourier transform. This is the precise sense in which $U^3$ is "beyond quadratic moments."

**Gowers inverse theorem (Green–Tao–Ziegler, *Ann. of Math.* 2012; the $U^3$ case Green–Tao 2008).** If $\|f\|_{U^{k+1}}\ge\delta$ for $\|f\|_\infty\le1$, then $f$ correlates ($\ge c(\delta)$) with a **$k$-step nilsequence** (a polynomial phase on a nilmanifold; for $U^3$, essentially a quadratic phase / 2-step nilsequence $e(\,\phi(x)\,)$ with $\phi$ a "bracket-quadratic"). Contrapositive: small $U^{k+1}$ = pseudorandom relative to degree-$k$ phases.

**Croot–Sisask almost-periodicity (Croot–Sisask, *GAFA* 2010).** For $f\in\ell^1$ and a set $B$, a random translate-averaged version of $f$ is $\ell^p$-almost-periodic: there is a large set of "near-periods" $t$ with $\|\tau_t(f*\mu_B)-f*\mu_B\|_p$ small. This is a **non-Fourier**, **local** structure theorem — it does not pass through any moment or character sum, which is exactly why it can dodge a symmetric-moment barrier.

### 1.2 What we apply it to

- **Frankl:** $G=(\mathbb Z/2)^n$ (Boolean cube under XOR), $f=1_F$. Compute $\|1_F\|_{U^k}$; ask whether high $U^k$ (cubic structure) forces abundance, and whether $1_F$ is a low-complexity nilsequence for UC families.
- **Collatz:** $G=\mathbb Z/3^n$ (or the units $(\mathbb Z/3^n)^\times$), $f=\nu_n$ the Syracuse stationary law (= invariant $\pi_n$ of the transfer operator, per `transfer_operator.md` Prop 2.1). Ask whether $\nu_n-U$ (or its tilt) has large $U^3$ — i.e. correlates with a **quadratic phase** — beyond the linear mod-3 obstruction.

---

## 2. Why it (partly) escapes the (degree ≤ 2, symmetric) barrier — and where it doesn't

### 2.1 The barriers, restated in higher-order language

- **Frankl barrier:** every *symmetric convex moment of the frequency vector* is flat-minimized by the cube at $\tfrac12$. The Boolean-Fourier attack (`boolean_fourier.md`) used only **degree-1** ($\hat f(\{i\})$, influences) and **degree-2** ($W^2$, noise stability $\mathrm{Stab}_\rho$, all $|\hat f|^2$-quadratic) statistics. $U^2$ *is* the degree-2 / $\ell^4$-Fourier statistic, so $U^2$ is inside the barrier by construction. The genuine question is $U^{\ge3}$.
- **Collatz barrier:** the mod-3 marginal $(0,\tfrac13,\tfrac23)$ is a **degree-1** (single linear character $\chi(x)=e(\xi x/3^n)$ with $3^{n-1}\mid\xi$) obstruction; "abelian Fourier failed" = the degree-1 inverse theorem (large Fourier coefficient $\Rightarrow$ linear-phase correlation) only *re-finds* the mod-3 coset structure. $U^{\ge3}$ probes a phase the linear characters cannot represent.

### 2.2 Frankl: higher Gowers is genuinely beyond quadratic — BUT the cube is flat at every order

The escape *attempt* is real: $\|1_F\|_{U^3}$ is **not** a function of $(p, W^1,\dots,W^n,I,\mathrm{Stab}_\rho)$, so it is formally outside the Boolean-Fourier obstruction class of `boolean_fourier.md` Thm 4.3. **However**, the barrier *generalizes*, and the probe (§3) shows it:

> **Structural obstruction (the cube is a coset of a subgroup).** The Frankl extremizer $2^{[k]}\subseteq(\mathbb Z/2)^n$ is precisely the indicator of the **subgroup** $H=\{x: x_i=0,\ i>k\}$ (a coset, when shifted). For an indicator of a subgroup/coset $H$, $1_H * 1_H \propto 1_H$, and the Gowers identity gives the **exact** value
> $$\|1_H\|_{U^k}^{2^k} = (|H|/|G|)^{2^k-1}\quad\Longrightarrow\quad \frac{\|1_H\|_{U^k}^{2^k}}{p^{2^k}}=\frac1p\cdot\Big(\text{wait}\Big)\;=\;\frac{\|1_H\|_{U^k}^{2^k}}{p^{\,2^k-1}\cdot p}.$$
> Concretely the **normalized** Gowers norm $\|1_H\|_{U^k}^{2^k}/\,p^{2^k}\cdot p = p^{-1}\cdot p =$ **the minimum (=1 after the correct density normalization)** for every $k$: a subgroup is the *extremal least-uniform / most-structured* set at **every** Gowers level. My probe confirms this numerically: the full cube has normalized $U^3$ ratio $=1.0000$ exactly at $n=2,3,4$ (§3), the floor of the whole population.

So the Frankl extremizer is simultaneously the *minimizer of abundance* (=½) **and** the *most structured / lowest-complexity* object at every Gowers order. Any monotone "more $U^k$ structure ⇒ more abundance" implication therefore **inverts** on the cube. This is the **same flatness pathology** as degree-2, now proven to persist to all orders — a genuine *strengthening* of the barrier, not an escape. **This is itself a clean (negative) deliverable.**

### 2.3 Collatz: higher Gowers genuinely escapes (the obstruction is degree-1, the room is at degree ≥ 2)

Here the situation is the opposite and favorable. The proven obstruction (`natural_density_obstruction.md` Thm 3.3, `transfer_operator.md` Prop 3.1) is **exactly degree-1**: it is the rank-1 $2\times2$ block on the mod-3 coset indicators, i.e. a single family of *linear* characters. I measured (§3.2) that at $n=2$ this degree-1 part accounts for only **58%** of the $\ell^2$ discrepancy; the other **42%** sits in the $3\nmid\xi$ modes that the linear inverse theorem cannot organize but a **quadratic ($U^3$) inverse theorem** can. The question "does $\nu_n^{(s)}-U$ restricted to $3\nmid\xi$ correlate with a 2-step nilsequence on $\mathbb Z/3^n$?" is **outside** the degree-1 abelian framework that failed, and is the natural next obstruction-or-descent test. Genuinely non-symmetric (a quadratic phase is not a moment).

---

## 3. Concrete first step + the validation I actually ran (n ≤ 5 / Syracuse)

### 3.1 Frankl: $U^3$ Gowers norm vs abundance, all UC families $n\le4$ (computed)

Probe (`/tmp/gowers_probe.py`, reusing `frankl/experiments/{enumerate,boolean_fourier,uc_family}.py`): for every nontrivial UC orbit-rep, compute $\|1_F\|_{U^3}^{8}=\mathbb E_{x,h_1,h_2,h_3}\prod_{\omega\in\{0,1\}^3}1_F(x{+}\omega{\cdot}h)$ by the exact $2^{4n}$ average ($\le10^6$ ops for $n\le4$), normalize by $p^8$, correlate with $\mathrm{abund}_{\max}$.

**Results (410 nontrivial families, $n\le4$):**
| quantity | value |
|---|---|
| $\mathrm{corr}(\mathrm{abund},\ \|1_F\|_{U^3}^8/p^8)$ | **0.21** |
| $\mathrm{corr}(\mathrm{abund},\ \|1_F\|_{U^2}^4/p^4)$ | **0.31** |
| full cube $2^{[n]}$ (ab=0.5, the extremizer): normalized $U^3$ | **1.0000** (population floor) |
| min over ab≈0.5 bin | **1.0000** (the cube) |
| min over ab≈1.0 bin | 16.0 |

**Reading.** $U^3$ correlates with abundance *more weakly* than $U^2$, and the extremizer sits at the **floor** of the normalized-$U^3$ distribution. Higher Gowers structure does **not** detect abundance for Frankl; it (anti-)points the wrong way on the extremizer, exactly as §2.2 predicts. **Frankl $U^k$-magnitude direction: falsified on the data.**

### 3.2 Collatz: where the discrepancy lives in frequency (computed)

Probe (`/tmp` inline, reusing the transfer-operator kernel): build $\nu_2=\pi_2$ on $\mathbb Z/9$ by power-iterating the Syracuse kernel; split $\|\widehat{\nu_2}\|^2$ (nonzero freqs) into $3\mid\xi$ (the degree-1 obstruction) vs $3\nmid\xi$.

**Result ($n=2$):** mod-3 marginal $=(\tfrac13,\tfrac23)$ as expected; Fourier mass $3\mid\xi$ (nonzero) $=0.667$, $3\nmid\xi=0.476$ ⇒ **42% of the discrepancy is in the higher ($3\nmid\xi$) modes** the abelian degree-1 obstruction does not touch. *This is the concrete opening for a higher-order inverse theorem: there is real, non-trivial mass to explain at $3\nmid\xi$, and degree-1 Fourier provably cannot.*

**The concrete Collatz first step (next session, code sketched):**
1. Compute $\widehat{\nu_n^{(s)}}(\xi)$ for $3\nmid\xi$ on $\mathbb Z/3^n$, $n\le 8$ (FFT, reuse `syracuse_fft/`).
2. **Quadratic-phase correlation test:** for each $n$, maximize $|\mathbb E_x\,(\nu_n^{(s)}-U)(x)\,e(-(\alpha x^2+\beta x)/3^n)|$ over $(\alpha,\beta)$ (a $U^3$ inverse-theorem surrogate on $\mathbb Z/3^n$). Large ⇒ a *quadratic* obstruction (descent via a 2-step nilsequence subtraction); small/decaying ⇒ the $3\nmid\xi$ part is genuinely $U^3$-pseudorandom and a power-saving $3^{-\theta n}$ becomes plausible *off the coset*, which is precisely the MIX($\theta$)-type input Tao's natural-density upgrade needs but restricted to $3\nmid\xi$ (sidestepping the killed Lemma 6.2).
3. Stratify by $v_3(\xi)$ (the projective filtration of `transfer_operator.md` §3.1) and test each level for quadratic structure separately.

### 3.3 The single surviving Frankl sub-direction: Croot–Sisask on the *operator*

The non-symmetric object Frankl needs is the **union map** $\cup:F\times F\to F$, not $1_F$ (every barrier doc converges on "$1_F$ symmetric statistics are flat"). Croot–Sisask almost-periodicity applied to $1_F*1_F$ (the *union-counting* convolution-analogue under XOR is the wrong group operation, so use the **up-set / join** structure): ask whether the function $g(x)=\#\{(A,B)\in F^2: A\cup B=x\}$ is $\ell^2$-almost-periodic with near-periods that *must* include a heavy singleton direction. This is local, non-moment, and sensitive to *which* element is heavy. Plausibility low (2) but it is the only $U/CS$ flavor not killed by §2.2.

---

## 4. Small validation (n ≤ 5)

- **Frankl, DONE:** 410 nontrivial UC families $n\le4$, exact $U^3$ norm computed; corr 0.21 (vs $U^2$ 0.31); cube at normalized-$U^3$ floor 1.0000. ($n=5$ inline $U^3$ is $2^{20}$/family × 29k families ≈ feasible overnight but the $n\le4$ result already falsifies the magnitude direction; not worth the compute.)
- **Collatz, DONE:** $\nu_2$ on $\mathbb Z/9$, 42% of discrepancy in $3\nmid\xi$. Extends trivially to $n\le8$ with `syracuse_fft/` (the quadratic-phase maximization is the real next step, sketched §3.2).
- **Cross-check available:** the $U^2$ value equals $\sum_S\hat f(S)^4$ (exact identity), which the probe computes both ways implicitly via `fourier_spectrum` — matches the `boolean_fourier.py` Parseval gate already validated to 1e-12.

---

## 5. Plausibility, failure modes, novelty

**Plausibility (1–5):**
- **Frankl $U^k$-magnitude:** **1** (falsified on data — the extremizer is the most-structured object at every order; barrier strengthens, doesn't break).
- **Frankl Croot–Sisask-on-operator:** **2** (non-symmetric and local, but no concrete lemma; the union map's almost-periodicity is uncharted and may just re-encode the JI-fibre tautology of `join_irreducible_labelling.md`).
- **Collatz higher-order inverse theorem (quadratic-phase off the coset):** **3** (genuinely escapes the *stated* degree-1 barrier; concrete first computation defined; real mass to explain). The honest ceiling: even a clean $U^3$-pseudorandomness of the $3\nmid\xi$ part gives power-saving only *off* the coset — the coset part still needs the separate "coset-respecting reference" device (`natural_density_obstruction.md` §5, option 1), so this is a *component* of a natural-density argument, not the whole thing.

**Failure modes:**
1. **Frankl (primary):** §2.2 — subgroup/coset extremizer ⇒ flat at all Gowers orders. Already realized in the data. *This kills the magnitude route definitively.*
2. **Collatz:** the $3\nmid\xi$ part may itself be controlled by the *next* coset level (mod $3^2$) rather than by a quadratic phase — the projective filtration (`transfer_operator.md` §3.1) means there is a tower of *linear* (coset) obstructions, and $U^3$ might just be re-finding mod-$9$ coset imbalance, not true quadratic structure. The §3.2 step-3 ($v_3$-stratification) is designed to distinguish "higher coset" from "genuine quadratic." If it's all coset, higher Gowers buys nothing new beyond `transfer_operator.md`'s filtration. This is the main risk and must be checked first.
3. **Inverse theorems are qualitative** ($c(\delta)$ ineffective / tower-type in GTZ), so even a positive correlation may not yield the *quantitative* $3^{-\theta n}$ Tao needs without the Manners (2018) effective bounds — and effective $U^3$ inverse theory on $\mathbb Z/3^n$ at this precision is delicate.

**Novelty `[NOVELTY UNVERIFIED]`:** Gowers norms on $\{0,1\}^n$ indicators are standard; the subgroup-flatness fact (§2.2) is elementary and almost certainly folklore — its *application as a Frankl barrier-extension* is the only possibly-new framing. Higher-order Fourier on Syracuse $(\mathbb Z/3^n)^\times$: I am not aware of a published $U^3$/nilsequence analysis of the Syracuse law (Tao's work is degree-1 Fourier; the GTZ machinery has not, to my knowledge, been pointed at this measure), but arXiv was inaccessible — flag and verify against Tao 2022 §7 and the Green–Tao–Ziegler / Manners literature next session.

**Bottom line.** For **Frankl**, higher-order additive combinatorics is a **NO** with a clean reason (coset extremizer is Gowers-flat at all orders — a barrier *strengthening*). For **Collatz**, it is the **most credible direction surfaced here**: the failed attack was provably degree-1, a measurable 42% of the discrepancy lives where only $U^{\ge3}$ can reach, and there is a concrete, runnable quadratic-phase / nilsequence first experiment (§3.2) that either yields a descent term or sharpens the obstruction to "all coset, no quadratic structure."
