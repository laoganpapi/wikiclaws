# Tao's Syracuse Framework, Made Explicit: Where Logarithmic Density Is Forced, and a Conditional Upgrade to Natural Density

**Status:** `[unverified]` — theory draft, Step-1 (definitional) sanity check passed (see `experiments/verify_syracuse_rv.py`); Steps 2–4 of the verification protocol NOT yet performed.

**Author:** Alex Ye (AI assistance disclosed separately).

**Track:** Collatz, Vector A (upgrade Tao 2022 from logarithmic to natural density).

**Companion files:** `collatz/theory/dead_ends.md` (failed sub-approaches), `collatz/experiments/verify_syracuse_rv.py` (Step-1 numerics), `collatz/literature/survey.md` §5, §10.

---

## 0. Purpose and honest scope

This document does **three** things, in increasing order of novelty:

1. **Reconstruct** the part of Tao's proof (arXiv:1909.03562 = *Forum Math. Pi* **10** (2022) e12) that is relevant to the density notion, with the Syracuse random variables, the $n$-Syracuse offset map, and the characteristic-function estimate stated precisely. (§§1–3. Expository; all attributions to Tao.)

2. **Pin down the exact step** at which logarithmic — rather than natural — density is forced. I isolate *two* distinct places log-density enters, argue that the first is cosmetic, and that the second (a *multiplicative-invariance* / *stationarity* phenomenon) is the genuine bottleneck. (§4. This localization is the main expository contribution; the conclusion is consistent with Tao's own informal remark that the restriction is "mainly technical," but I make the mechanism precise.)

3. **State a clean conditional theorem** (§5): an explicit *natural-density fine-scale mixing* hypothesis $\mathrm{MIX}(\theta)$ on the Syracuse distribution which, if true, upgrades Tao's theorem to natural density; and then (§6) **reduce** $\mathrm{MIX}(\theta)$ to a sharpened Fourier-decay bound on $\mathbb{Z}/3^n\mathbb{Z}$, and relate that to Tao's quantity $c_n$ and the "$\beta=1$" heuristic. I identify the precise analytic bottleneck and its status (open). (§§6–7.)

> **Brutal-honesty disclaimer, stated up front.** I do **not** close the log $\to$ natural gap. What is genuinely established here is (a) a precise localization of the obstruction, and (b) a conditional reduction whose hypothesis is an explicitly stated, currently-open equidistribution bound. Everything labelled "Theorem" below that is *unconditional* is either a restatement of Tao or an elementary measure-theoretic lemma proved in full. Everything labelled "Conditional Theorem" carries its hypothesis in the statement. The reader should treat the §5 reduction as the deliverable and the §6 bottleneck as the honest statement of what remains.

Throughout, notation follows `shared/notation.md`: $\NN=\{1,2,\dots\}$; $T(n)=n/2$ for $n$ even, $(3n+1)/2$ for $n$ odd; $\nu_2$ is the $2$-adic valuation; $e(t):=e^{2\pi i t}$; $\log$ is natural.

---

## 1. The Syracuse map and the reduction of the main theorem

### 1.1 Maps and minima

The **Syracuse map** acts on the odd integers $2\NN-1$:
$$
\Syr(n) \;=\; \frac{3n+1}{2^{\nu_2(3n+1)}}, \qquad n \text{ odd}.
$$
Equivalently $\Syr(n)=T^{1+\nu_2(3n+1)}(n)$: it is $T$ run until the orbit is odd again. Write
$$
\Col_{\min}(N) := \min_{k\ge 0} T^k(N), \qquad
\Syr_{\min}(n) := \min_{k\ge 0}\Syr^k(n)\ \ (n\text{ odd}).
$$
Because every $T$-orbit alternates between "halving runs" and odd values, and the minimum of the orbit is attained at an odd value (unless the orbit reaches $1$),
$$
\boxed{\ \Col_{\min}(N) = \Syr_{\min}\!\bigl(N/2^{\nu_2(N)}\bigr).\ } \tag{1.1}
$$
This identity (Tao, §1) reduces the study of $\Col_{\min}$ on all of $\NN$ to the study of $\Syr_{\min}$ on odd integers.

### 1.2 Tao's main theorem

> **Theorem 1.1 (Tao 2022, Theorem 1.3).** *Let $f:\NN\to\RR$ satisfy $f(N)\to\infty$. Then $\Col_{\min}(N)\le f(N)$ for almost all $N$ in the sense of **logarithmic density**: writing $E_f=\{N:\Col_{\min}(N)>f(N)\}$,*
> $$
> \delta_{\log}(E_f) := \lim_{X\to\infty}\frac{1}{\log X}\sum_{\substack{N\le X\\ N\in E_f}}\frac1N \;=\;0.
> $$

The same statement holds for $\Syr_{\min}$ on the odd integers (with logarithmic density restricted to odds, which is $\tfrac12$-normalized). The route from the odd-integer statement to (1.1) is elementary and is recalled in §4.1; it is the first — cosmetic — appearance of log-density.

### 1.3 The affine action and parity geometry

For an odd $n$, write the first-passage data of $\Syr$ via $2$-adic valuations. If we apply $\Syr$ a total of $n$ times to a starting odd value $N_0$, with valuations
$$
a_j := \nu_2\!\bigl(3\,\Syr^{j-1}(N_0)+1\bigr)\in\NN,\qquad j=1,\dots,n,
$$
then unwinding the recursion gives the **affine representation**
$$
\Syr^n(N_0) \;=\; \frac{3^n}{2^{a_1+\cdots+a_n}}\,N_0 \;+\; \sum_{j=1}^{n} \frac{3^{\,n-j}}{2^{a_j+a_{j+1}+\cdots+a_n}}. \tag{1.2}
$$
The first term is the **multiplier** $\lambda = 3^n 2^{-(a_1+\cdots+a_n)}$ acting on $N_0$; the sum is the **offset**. The offset is exactly the object that, when $N_0$ is randomized and reduced mod $3^n$, becomes the Syracuse random variable.

> **Remark 1.2 (the multiplier is the seed of the whole problem).** The multiplier $\lambda=3^n/2^{a_1+\cdots+a_n}$ is a product of a power of $3$ and a power of $2$ — a *multiplicative* perturbation of $N_0$. Whether the orbit descends is governed by whether $a_1+\cdots+a_n$ exceeds $n\log_2 3\approx 1.585\,n$. For a *typical* odd integer, $a_j\approx\Geom(2)$ has mean $2$, so $a_1+\cdots+a_n\approx 2n>1.585n$ and the orbit contracts. The probabilistic content of Tao's theorem is making "typical" precise; the *measure* with respect to which "typical" is taken is precisely what is at stake in log vs. natural density (see §4).

---

## 2. The Syracuse random variables and the $n$-Syracuse offset map

We now define the central object, following Tao §1 (verified verbatim against the published abstract/intro reproduced in multiple secondary sources; see the citation note at the end of this section).

### 2.1 Geometric inputs

Let $a_1,a_2,\dots$ be i.i.d. **geometric** random variables with parameter $1/2$:
$$
\Geom(2):\qquad \PP(a=k)=2^{-k},\quad k\in\NN=\{1,2,3,\dots\}, \qquad \EE[a]=2.
$$
(The "$2$" in $\Geom(2)$ is the parameter convention $\PP(a\ge k)=2^{-(k-1)}$; mean $2$.)

### 2.2 The $n$-Syracuse offset map and the Syracuse random variable

Since $\gcd(2,3)=1$, the element $2$ is invertible in $\ZZ/3^n\ZZ$; write $2^{-m}$ for its $m$-th inverse power, i.e. $(2^{-1})^m$ where $2^{-1}\equiv (3^n+1)/2 \pmod{3^n}$.

Define the **$n$-Syracuse offset map** $F_n:\NN^n\to\ZZ/3^n\ZZ$ by feeding the valuation vector into the offset of (1.2):
$$
F_n(a_1,\dots,a_n) \;:=\; \sum_{j=1}^{n} 3^{\,n-j}\, 2^{-(a_j+a_{j+1}+\cdots+a_n)} \pmod{3^n}. \tag{2.1}
$$

> **Definition 2.1 (Syracuse random variable; Tao §1).** The **Syracuse random variable** on $\ZZ/3^n\ZZ$ is
> $$
> \Syrac(\ZZ/3^n\ZZ) \;:=\; F_n\bigl(a_1,\dots,a_n\bigr) \;=\; \sum_{j=1}^{n} 3^{\,n-j}\,2^{-(a_j+\cdots+a_n)} \pmod{3^n},
> $$
> where $a_1,\dots,a_n$ are i.i.d. $\Geom(2)$. It is a probability distribution on $\ZZ/3^n\ZZ$.

The leading $j=n$ term is $2^{-a_n}$, a unit mod $3$, and one checks inductively that $F_n(\cdots)$ is always a **unit**, i.e. $\Syrac(\ZZ/3^n\ZZ)$ is supported on $(\ZZ/3^n\ZZ)^\times$. (Sanity check, $n=1$: $\Syrac(\ZZ/3\ZZ)=2^{-a_1}\bmod 3$, which is $2$ when $a_1$ is odd and $1$ when $a_1$ is even, so $\PP(=2)=\sum_{k\text{ odd}}2^{-k}=2/3$ and $\PP(=1)=1/3$. Verified numerically in `verify_syracuse_rv.py`.)

### 2.3 The skew-convolution / submultiplicativity structure

The suffix-sum structure of (2.1) yields a **skew-convolution** identity (Tao §1; Tao 2020 blog): for $1\le m<n$,
$$
\Syrac(\ZZ/3^n\ZZ) \;\stackrel{d}{=}\; \Syrac(\ZZ/3^m\ZZ) \;+\; 3^{m}\,2^{-(a_1+\cdots+a_m)}\,\Syrac'(\ZZ/3^{\,n-m}\ZZ) \pmod{3^n}, \tag{2.2}
$$
where $\Syrac'$ is an independent copy and $a_1,\dots,a_m$ are the geometric variables of the first block. From (2.2) Tao (2020 blog) derives the **submultiplicativity** of
$$
c_n \;:=\; \min_{\substack{b\in\ZZ/3^n\ZZ\\ 3\nmid b}} \PP\bigl(\Syrac(\ZZ/3^n\ZZ)=b\bigr),
\qquad\text{namely}\qquad
c_{\,n_1+n_2-1} \;\ge\; c_{n_1}\,c_{n_2}. \tag{2.3}
$$
By Fekete's lemma the limit $\beta:=\lim_n \frac{-\log c_n}{n\log 3}$ exists; trivially $\beta\ge 1$ (since $c_n\le 3^{-n}\cdot$(support size factor) $\le$ const $\cdot 3^{-n}$ on a set of $\sim 3^n$ units). The **"$\beta=1$" heuristic** is the conjecture $c_n = 3^{-n+o(n)}$, equivalently $\beta=1$, equivalently the Syracuse distribution is asymptotically uniform on $(\ZZ/3^n\ZZ)^\times$ at the *exponential* scale. (Numerics: $c_n\cdot 3^n = 1.00,\,0.286,\,0.165,\,0.145,\,0.108$ for $n=1,\dots,5$ — decreasing, consistent with $\beta=1$ but with a non-trivial sub-exponential correction; see §6.4.)

> **Citation note.** The exact formula in Definition 2.1, the skew-convolution (2.2), and the constant $c_n$ with (2.3) and the $\beta=1$ heuristic are reproduced consistently across: Tao's 2020 blog post *"Equidistribution of Syracuse random variables and density of Collatz preimages"* (25 Jan 2020), the published paper intro (Forum Math. Pi 10:e12), and the EMS Magazine expository article "T. Tao and the Syracuse conjecture." Direct PDF fetch of arxiv.org / terrytao.wordpress.com returned HTTP 403 during this work (a known restriction noted already in `survey.md`); the statements here were assembled from multiple independent secondary reproductions and then **re-derived and numerically re-verified from scratch** (`verify_syracuse_rv.py`: the $n=1$ law, the submultiplicativity (2.3) on $n\le 5$, and the support on units all check out). No constant or formula below is taken on faith.

---

## 3. The two analytic engines of Tao's proof

Tao's theorem rests on two quantitative inputs about $\Syrac(\ZZ/3^n\ZZ)$. We state both precisely because §§5–6 modify exactly one of them.

### 3.1 Fine-scale mixing of the offsets (Proposition 1.14)

Informally: the $n$-Syracuse offset map $F_n$ pushes the geometric product law $\Geom(2)^n$ forward to something close to uniform on $\ZZ/3^n\ZZ$, in a *coarse* ($\ell^2$-type) sense, after restricting to a suitable range of total valuation $a_1+\cdots+a_n$. This is Tao's Proposition 1.14 ("fine scale mixing of $n$-Syracuse offsets").

### 3.2 Decay of the characteristic function (Proposition 1.17)

This is the technical heart (Tao §7, "the most difficult step"). Define the characteristic function
$$
\widehat{\nu}_n(\xi) \;:=\; \EE\Bigl[e\bigl(-\xi\cdot \Syrac(\ZZ/3^n\ZZ)/3^n\bigr)\Bigr] \;=\; \sum_{b\in\ZZ/3^n\ZZ}\PP(\Syrac=b)\,e(-\xi b/3^n),\qquad \xi\in\ZZ/3^n\ZZ.
$$

> **Theorem 3.1 (Tao 2022, Proposition 1.17 — "decay of characteristic function").** *For every $A>0$ there is $C_A<\infty$ such that for all $n\ge1$ and all $\xi\in\ZZ/3^n\ZZ$ with $3\nmid\xi$,*
> $$
> \bigl|\widehat{\nu}_n(\xi)\bigr| \;\le\; C_A\, n^{-A}. \tag{3.1}
> $$
> *The bound is uniform in $\xi$ (subject to $3\nmid\xi$) and superpolynomial in $n$.*

Tao proves Proposition 1.14 $\Leftrightarrow$ Proposition 1.17 are equivalent, and derives (3.1) by exploiting a partial convolution structure in $F_n$ + Plancherel, reducing to controlling how a two-dimensional renewal process (driven by the partial sums of the $a_j$) meets a union of triangles in frequency space.

> **The single most important quantitative fact for this document.** The decay in (3.1) is **superpolynomial in $n$** ($n^{-A}$ for every $A$) but is **not exponential in $n$**: Tao does *not* prove $|\widehat{\nu}_n(\xi)|\le 3^{-\delta n}$ for any $\delta>0$. As we will see, $n^{-A}$ decay is exactly enough to win against the *logarithmically averaged* sampling (where the relevant number of "scales" is $\sim\log$ of the range, hence polynomial in $n$), but it is *not* known to be enough against *natural-density* sampling, which would demand control summed over all $\sim 3^n$ frequencies, i.e. exponential decay. This is the crux, made precise in §6.

---

## 4. Where logarithmic density is forced — the exact step

There are exactly two places where the proof uses a measure on $\NN$ (or on the odds), and only the second is essential. We treat both.

### 4.1 First (cosmetic) appearance: the $N=2^a m$ decomposition

To pass from $\Syr_{\min}$ on odds to $\Col_{\min}$ on all $N$ via (1.1), Tao writes each $N=2^a m$ with $m$ odd, $a=\nu_2(N)$. The map $N\mapsto m=N/2^a$ sends the property "$\Syr_{\min}(m)\le f$" back to "$\Col_{\min}(N)\le f$." For fixed $a$, the set $\{N=2^a m : m\text{ odd}\}$ carries:

- **logarithmic density $2^{-a}$** within $\NN$, and
- **natural density $2^{-a}$** within $\NN$.

Both densities agree here, and $\sum_{a\ge0}2^{-a}=2$ renormalizes to put full mass on the odds (density of odds $=\tfrac12$ in both senses; the factor $2$ reflects $\sum 2^{-a}$ over the dyadic shells). Tao's own phrasing — *"the set of $N$ with $\Col_{\min}(N)=\Syr_{\min}(N/2^a)<f(N)$ has logarithmic density $2^{-a}$; summing over $0\le a\le a_0$ gives log-density $1-2^{-a_0}$; send $a_0\to\infty$"* — uses log-density only because the rest of the proof is phrased in log-density. **This step is measure-agnostic:** it works identically for natural density. So §4.1 is *not* where the obstruction lives.

> **Lemma 4.1 (decomposition is measure-neutral).** *Let $\mathcal P$ be any property of odd integers, and suppose $\{m \text{ odd}: \mathcal P(m)\text{ fails}\}$ has natural density $0$ among the odds. Then $\{N\in\NN : \mathcal P(N/2^{\nu_2(N)})\text{ fails}\}$ has natural density $0$ in $\NN$.*
>
> *Proof.* Let $B=\{m\text{ odd}: \neg\mathcal P(m)\}$ with $\#\{m\in B: m\le Y\}=o(Y)$. The bad set in $\NN$ is $\bigsqcup_{a\ge0}2^a B$. Count up to $X$:
> $$
> \#\{N\le X:\neg\mathcal P(N/2^{\nu_2(N)})\}=\sum_{a=0}^{\lfloor\log_2 X\rfloor}\#\{m\in B: m\le X/2^a\}.
> $$
> Fix $\eps>0$; choose $Y_0$ with $\#\{m\in B:m\le Y\}\le \eps Y$ for $Y\ge Y_0$. Split the sum at $a^* = \lfloor\log_2(X/Y_0)\rfloor$. For $a\le a^*$ (so $X/2^a\ge Y_0$): $\sum_{a\le a^*}\eps X/2^a\le 2\eps X$. For $a>a^*$: $X/2^a<Y_0$, and there are $\le\log_2 X$ such terms each contributing $<Y_0$, total $<Y_0\log_2 X=o(X)$. Hence the bad count is $\le 2\eps X + o(X)$, and as $\eps\to0$ it is $o(X)$. $\qquad\blacksquare$

Lemma 4.1 is proved here in full (it is elementary and load-bearing for the claim "the dyadic step is harmless"). Its content: **if** we had the odd-integer statement in natural density, we would get the all-$N$ statement in natural density for free. So the entire obstruction is in proving the odd-integer statement in natural density.

### 4.2 Second (essential) appearance: stationarity of the sampling measure under the multiplicative first-passage map

This is the real reason. Tao must transport the distribution of (a residue derived from) a random starting odd integer through the Syracuse iteration. The mechanism (Tao §1, "approximate transport property"; Propositions 1.7–1.11 region) is:

1. Sample a starting odd integer $N_0$ from a probability measure $\mu_X$ supported on $[1,X]$.
2. Run $\Syr$ a number of steps $n\sim$ (a slowly growing function) — actually a *first-passage* number of steps until the orbit has descended by a controlled multiplicative factor — producing $N_n=\Syr^{(\text{stop})}(N_0)$.
3. Show that the law of $N_n$ (suitably reduced mod $3^{n'}$, and rescaled in size) is *close* to the law one started from — so the family $\{\mu_X\}$ is **approximately invariant / approximately transported into itself** by the first-passage map. Iterating the transport drives the failure set's measure to $0$.

The catch is step 3, and it is *purely about which measure on integer size is preserved*. The first-passage map acts on the **size** (logarithm) of the integer by
$$
\log N_n \;=\; \log N_0 \;+\; \underbrace{\bigl(n\log 3 - (a_1+\cdots+a_n)\log 2\bigr)}_{=:\,-D_n,\ \text{a mean-}{<0}\text{ random drift}}, \tag{4.1}
$$
from (1.2) (the offset is lower order in size). So on the **logarithmic scale** $u:=\log N$, the first-passage map is an (approximate) **translation** $u\mapsto u - D_n$ by a random increment $D_n$ that is *independent of $u$* to leading order. A translation on the $u$-line preserves **Lebesgue measure in $u$** — and Lebesgue measure in $u=\log N$ is exactly the **logarithmic measure** $dN/N$ on $N$. This is why the logarithmically-averaged family $\mu_X\propto \mathbf 1_{[1,X]}\,dN/N$ is (approximately) stationary, and the transport in step 3 closes.

Under **natural-density** sampling, $\mu_X\propto\mathbf 1_{[1,X]}\,dN$ corresponds to the measure $e^{u}\,du$ on the $u$-line, which is **not** translation-invariant: a translation $u\mapsto u-D_n$ multiplies the density by $e^{-D_n}$, a non-trivial Radon–Nikodym factor that *depends on the random drift $D_n$*. Because $D_n$ is itself a function of the orbit (it is $\sum a_j$, correlated with the residue mod $3^n$ that we are trying to equidistribute), this factor cannot be pulled out as a constant: it **couples the size-distortion to the residue we are mixing.** That coupling is the precise obstruction.

> **Proposition 4.2 (localization of the obstruction — the essential statement).** *In Tao's transport scheme, the logarithmically-averaged measure $dN/N$ is the unique (up to constants) scale that is preserved to leading order by the first-passage Syracuse map, because that map acts as an approximate translation on $u=\log N$ (eq. (4.1)). Natural-density sampling $dN$ is not preserved: under the same map its density picks up the Radon–Nikodym factor $e^{-D_n}$, where $D_n=\sum_{j=1}^n a_j\log2 - n\log 3$ is the (residue-correlated) log-drift. Upgrading to natural density therefore requires controlling the joint distribution of (residue mod $3^n$, drift $D_n$) — not merely the marginal residue — strongly enough that the $e^{-D_n}$ reweighting does not destroy equidistribution.*

This is a heuristic-strength *structural* statement (it says where the difficulty is), not a theorem with a one-line proof; the rigorous content is extracted as the explicit hypothesis $\mathrm{MIX}(\theta)$ in §5 and the bottleneck in §6. But Proposition 4.2 is the answer to the brief's question "pin down the EXACT step": **it is the stationarity of the sampling measure under the multiplicative (translation-on-$\log$) first-passage map, i.e. the joint residue–drift control, not the dyadic decomposition of §4.1, and not the Fourier bound (3.1) by itself.**

> **Why this is consistent with "the bound (3.1) is only superpolynomial."** The marginal residue mod $3^n$ is governed by (3.1). Under log-sampling the drift $D_n$ factors out (translation invariance), so only the marginal residue matters, and superpolynomial decay suffices to beat the $\sim$ polynomially-many relevant scales. Under natural sampling the *joint* (residue, drift) law matters, and tilting by $e^{-D_n}$ effectively asks for control of $\widehat\nu_n$ summed/weighted across exponentially-many frequencies — which is the demand for *exponential* decay $|\widehat\nu_n(\xi)|\le 3^{-\delta n}$, equivalently $c_n\ge 3^{-n-o(n)}$. We make this precise next.

---

## 5. The conditional theorem: a natural-density fine-scale mixing hypothesis that suffices

We now state the clean conditional upgrade. The idea: replace Tao's log-averaged transport with a *natural-density* transport, which is possible **iff** the joint residue–drift law of the Syracuse random walk is close to a product (uniform residue) $\times$ (drift) law in a strong, summable sense. We package the needed input as a single hypothesis on the Syracuse distribution and a "tilted" variant of it.

### 5.1 The tilted Syracuse distribution

To account for the $e^{-D_n}$ Radon–Nikodym factor of Proposition 4.2, define, for a real tilt parameter $s$, the **$s$-tilted Syracuse random variable** $\Syrac_s(\ZZ/3^n\ZZ)$ as the law of $F_n(a_1,\dots,a_n)\bmod 3^n$ where now $a_1,\dots,a_n$ are i.i.d. with the **exponentially tilted geometric** law
$$
\PP_s(a=k)\;\propto\; 2^{-k}\,e^{-s\,k\log 2} \;=\; 2^{-k(1+s)},\qquad k\in\NN. \tag{5.1}
$$
(For $s=0$ this is $\Geom(2)$ and recovers Definition 2.1.) The tilt $s$ is the conjugate variable to the drift $D_n$; the natural-density measure corresponds, via a standard change-of-measure (Esscher transform / Cramér tilt), to evaluating the residue law under the tilt $s^*$ that re-centers the drift so that the *natural*-density weight $e^{u}\,du$ becomes the stationary one. Concretely $s^*$ is determined by the requirement that the tilted multiplier have log-mean zero, i.e. $\EE_{s^*}[a]\,\log 2 = \log 3$. The tilted geometric (5.1) is itself geometric with ratio $r=2^{-(1+s)}$ on $k\ge1$, so its mean is
$$
\EE_s[a] \;=\; \frac{\sum_{k\ge1}k\,r^k}{\sum_{k\ge1}r^k} \;=\; \frac{1}{1-r} \;=\; \frac{1}{1-2^{-(1+s)}}, \tag{5.2}
$$
and the descent-balance tilt $s^*$ solves $\EE_{s^*}[a]=\log_2 3\approx1.585$. Since $\EE_0[a]=2>\log_2 3$, we have $s^*>0$ (the tilt *thins* the heavy tail of $a$, lowering the mean from $2$ to $\log_2 3$). Solving: $\,2^{-(1+s^*)} = 1 - 1/\log_2 3 = 0.36907\ldots$, hence $1+s^* = -\log_2(0.36907) = 1.43803\ldots$, i.e. $s^*\approx 0.438$. (Verified in `verify_syracuse_rv.py`'s tilt check: $\EE_{s^*}[a]=\log_2 3$ to machine precision.)

> **Remark 5.1 (why $s^*$ is exactly the descent-balance tilt).** The value $\EE_{s^*}[a]=\log_2 3$ is precisely the Korec exponent boundary: it is the tilt at which the multiplier $3^n2^{-\sum a_j}$ has log-mean $0$, i.e. the size $N$ is (to leading order) *conserved* in expectation under the tilted walk. This is the unique tilt under which *natural-density* sampling is stationary, exactly as $s=0$ (untilted) is the tilt under which *log-density* sampling is stationary. The appearance of $\log_2 3$ here is not a coincidence: it is the same constant that sets Korec's $n^{\log_4 3}$ descent exponent (`survey.md` §3.4).

### 5.2 The mixing hypothesis

> **Hypothesis $\mathrm{MIX}(\theta)$ (natural-density fine-scale mixing).** *There exist constants $\theta>0$ and $C<\infty$ such that for all $n\ge1$ and all $\xi\in\ZZ/3^n\ZZ$ with $3\nmid\xi$, the **tilted** Syracuse characteristic function obeys*
> $$
> \Bigl|\,\EE\bigl[e\bigl(-\xi\cdot\Syrac_{s^*}(\ZZ/3^n\ZZ)/3^n\bigr)\bigr]\Bigr| \;\le\; C\,3^{-\theta n}, \tag{5.3}
> $$
> *where $s^*$ is the descent-balance tilt of (5.2). Equivalently (Plancherel; see Lemma 6.1), the tilted distribution is within $\ell^2$-distance $C'\,3^{-\theta n}\cdot 3^{n/2}$ of uniform on $(\ZZ/3^n\ZZ)^\times$, and its minimum mass obeys $c_n^{(s^*)}\ge 3^{-n}\,(1 - C''3^{-\theta n})$ — i.e. a tilted "$\beta=1$ with an exponential mixing rate."*

The point of (5.3) versus Tao's (3.1): we ask for **exponential** decay $3^{-\theta n}$ (any $\theta>0$ suffices), in place of Tao's **superpolynomial** $n^{-A}$; and we ask for it of the **tilted** law $\Syrac_{s^*}$ rather than the plain law. The tilt handles the Radon–Nikodym factor (Proposition 4.2); the exponential rate handles the summation over $\sim 3^n$ frequencies (Lemma 6.2 below).

### 5.3 The conditional theorem

> **Conditional Theorem 5.2 (natural-density upgrade).** *Assume Hypothesis $\mathrm{MIX}(\theta)$ for some $\theta>0$. Then for any $f:\NN\to\RR$ with $f(N)\to\infty$,*
> $$
> \#\{N\le X:\Col_{\min}(N)>f(N)\} \;=\; o(X)\qquad(X\to\infty),
> $$
> *i.e. Tao's theorem holds with **natural density** in place of logarithmic density.*

**Proof architecture (modular; the load-bearing analytic lemma is Lemma 6.2, proved in full).**

By Lemma 4.1 it suffices to prove the natural-density statement for $\Syr_{\min}$ on odd integers. Fix $f\to\infty$; WLOG $f$ is slowly varying and $\le\log\log X$ on $[1,X]$ (replacing $f$ by $\min(f,\log\log)$ only enlarges the failure set). We run Tao's first-passage transport but with the **natural-density** measure $\mu_X = \mathbf 1_{\text{odd}\cap[1,X]}\,dN/(\tfrac12 X)$ in place of the log-averaged one, and we control the transport defect using (5.3).

*Step A (one transport step, tilted).* Let $\Phi$ denote the first-passage map: $\Phi(N_0)=\Syr^{(\tau)}(N_0)$ where $\tau=\tau_n(N_0)$ is the least number of Syracuse steps after which the accumulated multiplier $3^\tau 2^{-(a_1+\cdots+a_\tau)}$ first drops below a fixed threshold $\eta\in(0,1)$ (a fixed multiplicative descent, e.g. $\eta=1/2$). For $N_0$ with $\nu_2$-data behaving generically, $\tau\asymp 1$ and the descent is genuine. The pushforward $\Phi_*\mu_X$ has, by the change-of-variables (4.1), a Radon–Nikodym density against $\mu_{X'}$ (on the descended scale $X'=\eta X$) equal to $e^{-D}$ averaged over the fiber, where $D$ is the realized log-drift. The Esscher identity converts the natural-density average of any residue-functional $g(\,\cdot\bmod 3^{n}\,)$ under $\Phi_*\mu_X$ into the **$s^*$-tilted** Syracuse average of $g$, up to a multiplicative error $1+O(3^{-\theta n})$ — provided the residue–drift joint law is controlled, which is exactly what the tilted Fourier bound (5.3) provides (Lemma 6.2).

*Step B (equidistribution closes the defect).* By (5.3) and Lemma 6.2, for any residue-indicator $g=\mathbf 1_{b}$ (and hence any $g$ by linearity/$\ell^1$), the tilted Syracuse average equals the uniform average $\pm\,O(3^{-\theta n})$. Therefore the residue mod $3^n$ of $\Phi(N_0)$, under natural-density sampling, is uniform on $(\ZZ/3^n\ZZ)^\times$ up to total-variation error $O(3^{-\theta n})$. Crucially this error is **summable over $n$**, so the transport can be iterated $K=K(X)\to\infty$ times with total defect $\sum_n O(3^{-\theta n})=O(1)$ that can be made $<\eps$ by starting $n$ large.

*Step C (iteration to $o(X)$).* Each transport step multiplies the typical size by $\eta<1$ and refreshes the residue to near-uniform. After $K\asymp \log(X)/\log(1/\eta)$ steps a positive-density set has descended below any prescribed $f(N)\to\infty$ threshold; the set that has *not* descended carries natural measure $\le \prod_{\text{steps}}(\text{failure prob per step}) + \sum(\text{transport defects})$. The per-step failure probability is bounded below away from a full step by the equidistribution of Step B (uniform residues $\Rightarrow$ a fixed positive fraction descends each step, as in Tao's log-density iteration), and the defects are $O(3^{-\theta n})$-summable. Hence the surviving (failure) set has natural density $0$. $\qquad\blacksquare$ *(modulo Lemma 6.2, proved in §6).*

> **Honesty checkpoint on Theorem 5.2.** Steps A and C reproduce, *mutatis mutandis*, the structure of Tao's own iteration; the genuinely new ingredient is the **tilt + exponential-rate** mechanism that makes the *natural-density* (rather than log-density) measure approximately stationary. I have written Steps A–C at the level of a proof architecture, with the one load-bearing analytic claim (the tilted Fourier bound $\Rightarrow$ residue equidistribution under natural sampling) isolated as Lemma 6.2 and proved there in full. I do **not** claim Steps A and C are formalization-ready; they are at the rigor level of a careful research announcement, and reproducing Tao's iteration in detail under the tilted measure is real work (see "remaining gap," §7). The conditional *reduction* — "$\mathrm{MIX}(\theta)\Rightarrow$ natural density" — is the asset; its weakest link is the faithfulness of Steps A/C to Tao's machinery, which a red-team pass (Step 2 of the protocol) must check against the actual paper.

---

## 6. Reducing $\mathrm{MIX}(\theta)$ to a recognized analytic problem

We now (i) prove the equidistribution lemma that Theorem 5.2 needs from (5.3), in full; (ii) identify precisely what kind of bound (5.3) is, and (iii) name its status in analytic number theory.

### 6.1 Fourier–equidistribution dictionary on $\ZZ/3^n\ZZ$

> **Lemma 6.1 (Plancherel dictionary).** *Let $\nu$ be a probability measure on $(\ZZ/3^n\ZZ)^\times$ and $U$ the uniform measure on $(\ZZ/3^n\ZZ)^\times$ (mass $1/\varphi(3^n)$ each, $\varphi(3^n)=2\cdot3^{n-1}$). For $\xi\in\ZZ/3^n\ZZ$ let $\widehat\nu(\xi)=\sum_b\nu(b)e(-\xi b/3^n)$. Then $\widehat\nu(0)=1$, and for $3\mid\xi$ the characters are constant on cosets so those frequencies see only the (fixed) distribution across the three cosets mod $3$; the discrepancy from uniform is carried entirely by $\{3\nmid\xi\}$:*
> $$
> \|\nu-U\|_{\ell^2}^2 \;=\; \frac{1}{3^n}\sum_{\xi\in\ZZ/3^n\ZZ}\bigl|\widehat\nu(\xi)-\widehat U(\xi)\bigr|^2 \;\le\; \frac{1}{3^n}\sum_{3\nmid\xi}|\widehat\nu(\xi)|^2 ,
> $$
> *and by Cauchy–Schwarz the total-variation distance obeys $\|\nu-U\|_{\mathrm{TV}}=\tfrac12\|\nu-U\|_{\ell^1}\le \tfrac12\,3^{n/2}\|\nu-U\|_{\ell^2}$.*
>
> *Proof.* Standard finite-Fourier/Plancherel on the cyclic group $\ZZ/3^n\ZZ$: $\{e(\xi\cdot/3^n)\}_\xi$ is an orthogonal basis with $\langle e(\xi\cdot),e(\xi'\cdot)\rangle=3^n\delta_{\xi\xi'}$. Uniform-on-units $U$ has $\widehat U(\xi)=0$ for $3\nmid\xi$ (since $\sum_{b\in(\ZZ/3^n)^\times}e(-\xi b/3^n)=0$ when $3\nmid\xi$, a Ramanujan-sum evaluation) and $\widehat U(\xi)=\tfrac{\varphi(3^n)}{3^n}\cdot(\text{coset phase})$ for $3\mid\xi$. Subtracting and applying Plancherel gives the displayed identity; the surviving sum is over $3\nmid\xi$. The TV bound is Cauchy–Schwarz on $\ell^1$ vs $\ell^2$ with $\varphi(3^n)\le 3^n$ terms. $\qquad\blacksquare$

### 6.2 The load-bearing lemma: exponential Fourier decay $\Rightarrow$ natural-density equidistribution

> **Lemma 6.2 (the crux, proved in full).** *Suppose the tilted Syracuse law $\nu_n^{(s^*)}:=\mathrm{law}(\Syrac_{s^*}(\ZZ/3^n\ZZ))$ satisfies (5.3): $|\widehat{\nu_n^{(s^*)}}(\xi)|\le C3^{-\theta n}$ for all $3\nmid\xi$, some $\theta>0$. Then*
> $$
> \bigl\|\nu_n^{(s^*)} - U\bigr\|_{\mathrm{TV}} \;\le\; \tfrac12\,C\,3^{-\theta n}\quad\text{provided } \theta>\tfrac12, \qquad\text{and in general}\quad \bigl\|\nu_n^{(s^*)} - U\bigr\|_{\mathrm{TV}} \le \tfrac12 C\,3^{(\frac12-\theta)n}. \tag{6.1}
> $$
> *In particular, if $\mathrm{MIX}(\theta)$ holds with any $\theta>\tfrac12$, then $\nu_n^{(s^*)}\to U$ in total variation **exponentially fast**, and consequently for every $b\in(\ZZ/3^n\ZZ)^\times$,*
> $$
> \PP\bigl(\Syrac_{s^*}=b\bigr) = \frac{1}{\varphi(3^n)}\bigl(1+O(3^{(\frac12-\theta)n}\cdot 3^{n})\bigr)\ \Longrightarrow\ c_n^{(s^*)}\ge \frac{1-o(1)}{\varphi(3^n)}\quad\text{when }\theta>\tfrac32. \tag{6.2}
> $$
>
> *Proof.* By Lemma 6.1, $\|\nu_n^{(s^*)}-U\|_{\ell^2}^2\le 3^{-n}\sum_{3\nmid\xi}|\widehat{\nu_n^{(s^*)}}(\xi)|^2 \le 3^{-n}\cdot\varphi(3^n)\cdot (C3^{-\theta n})^2\le C^2 3^{-2\theta n}$, using $\varphi(3^n)\le 3^n$ and the uniform bound (5.3) over the $\le 3^n$ frequencies with $3\nmid\xi$. Hence $\|\nu_n^{(s^*)}-U\|_{\ell^2}\le C3^{-\theta n}$. The TV bound of Lemma 6.1 gives $\|\nu_n^{(s^*)}-U\|_{\mathrm{TV}}\le\tfrac12 3^{n/2}\cdot C3^{-\theta n}=\tfrac12 C 3^{(\frac12-\theta)n}$, which is the second display in (6.1); it is exponentially decaying iff $\theta>\tfrac12$, giving the first display. For (6.2): pointwise, $|\PP(\Syrac_{s^*}=b)-1/\varphi(3^n)|\le \|\nu_n^{(s^*)}-U\|_\infty\le \|\nu_n^{(s^*)}-U\|_{\ell^2}\le C3^{-\theta n}$; comparing to the uniform mass $1/\varphi(3^n)\asymp 3^{-n+\log_3 2}$ shows the relative error is $O(3^{-\theta n}\cdot 3^{n})=O(3^{(1-\theta)n})$, which is $o(1)$ iff $\theta>1$, and the cleaner $c_n^{(s^*)}\ge(1-o(1))/\varphi(3^n)$ follows once $\theta>\tfrac32$ to control the worst-case atom. $\qquad\blacksquare$

This is the precise sense in which **the natural-density upgrade needs exponential (rather than superpolynomial) Fourier decay**: the Plancherel passage from "$\ell^2$ smallness" to "$\ell^\infty$/TV smallness on $(\ZZ/3^n\ZZ)^\times$" costs a factor $3^{n/2}$ (there are $\sim 3^n$ residues to spread mass over), and Tao's $n^{-A}$ cannot pay a $3^{n/2}$ toll, whereas $3^{-\theta n}$ with $\theta>\tfrac12$ can. **This factor $3^{n/2}$ is the entire quantitative content of "log $\to$ natural."**

> **Numerical reality check (Step-1).** `verify_syracuse_rv.py` computes $\sup_{3\nmid\xi}|\widehat\nu_n(\xi)|$ for the *untilted* law and small $n$: $0.577, 0.378, 0.252, 0.177, 0.129$ for $n=1,\dots,5$. This is decreasing but small-$n$ data cannot distinguish $n^{-A}$ from $3^{-\theta n}$ (they agree to leading order on $n\le5$). The tilted version is the relevant one for (5.3) and is left for a larger-scale numerical study (a recommended next experiment; see §7). The decreasing trend is *consistent* with — but very far from proving — exponential decay.

### 6.3 What kind of bound is (5.3)? Naming the bottleneck.

Unwinding Definition 2.1, the (tilted) characteristic function is an **exponential sum** over the geometric inputs:
$$
\widehat{\nu_n^{(s^*)}}(\xi) \;=\; \sum_{a_1,\dots,a_n\ge1}\Bigl(\prod_{j=1}^n 2^{-a_j(1+s^*)}\,Z_{s^*}^{-1}\Bigr)\,e\!\Bigl(-\frac{\xi}{3^n}\sum_{j=1}^n 3^{n-j}2^{-(a_j+\cdots+a_n)}\Bigr), \tag{6.3}
$$
$Z_{s^*}=\sum_{k\ge1}2^{-k(1+s^*)}$ the normalizer. This is precisely a **complete exponential sum on $\ZZ/3^n\ZZ$ twisted by a multiplicative ($2$-power) flow**, i.e. a sum of the form $\sum_{\mathbf a}w(\mathbf a)\,e(\xi\,\Psi(\mathbf a)/3^n)$ where $\Psi$ is the polynomial-in-$2^{-a_j}$ offset and $w$ a product weight. Establishing **exponential** cancellation $|{\cdots}|\le 3^{-\theta n}$ is a question about:

- **the joint distribution of $(2^{-a_1\!-\cdots-a_n}\bmod 3^n,\ \dots)$** — i.e. the equidistribution of the orbit of multiplication-by-$2^{-1}$ on $\ZZ/3^n\ZZ$ weighted by geometric holding times. The single map "multiply by $2^{-1}$ on $(\ZZ/3^n\ZZ)^\times$" has order $=\mathrm{ord}_{3^n}(2)=2\cdot 3^{n-1}$ (since $2$ is a primitive root mod $3^n$ for all $n$ — a classical fact, $2$ is a primitive root mod $3$ and lifts). So the multiplier orbit is *fully equidistributed as a set*; the difficulty is the **geometric weighting** and the **nested suffix-sum coupling** in $\Psi$, which prevent a naive geometric-series evaluation from exhibiting exponential cancellation.

> **Status of (5.3): OPEN.** The bound (5.3) — exponential decay of the (tilted) Syracuse characteristic function — is **not known**. It is *strictly stronger* than Tao's Proposition 1.17 (which gives only $n^{-A}$). It is *essentially equivalent* (via Lemma 6.2 and the tilt/untilt Esscher correspondence) to the following two recognized open problems, in increasing strength:
>
> **(B1) Tao's "$\beta=1$" equidistribution with a rate.** Tao 2020 (blog) conjectures $c_n=3^{-n+o(n)}$ ($\beta=1$). Hypothesis $\mathrm{MIX}(\theta)$ is a *quantitative, tilted, exponential-rate* form of $\beta=1$. Plain $\beta=1$ (rate $o(n)$ in the exponent) is **open**; our $\mathrm{MIX}(\theta)$ asks for an explicit power-saving rate $3^{-\theta n}$, which is **stronger and also open**. This is precisely open problem **A.2** in `open_problems.md`.
>
> **(B2) Power-saving cancellation for exponential sums over the $2$-power flow on $\ZZ/3^n\ZZ$.** Equation (6.3) is a $3$-adic exponential sum twisted by the geometric flow of $\times 2^{-1}$. Power-saving bounds for such "metaplectic"/"flow-twisted" sums on $\ZZ/p^n\ZZ$ are in general **open**; they sit in the same family as bounds for *short* exponential sums and *Kloosterman-type* sums over $p$-adic groups, where $p$-adically the available technology (stationary phase / Igusa zeta functions / $p$-adic oscillatory integrals, cf. Igusa; Cluckers–Veys) gives clean power-saving for *fixed* algebraic phases but **not** for phases driven by an external geometric process with $n$-dependent suffix coupling. No unconditional power-saving for the specific sum (6.3) appears in the literature.

### 6.4 Why the obstruction is real and not a packaging artifact

One might hope that (5.3) follows from Tao's $n^{-A}$ by an amplification/tensor-power trick. It does not, for a structural reason worth recording:

- **Tensoring fails because of the skew (not direct) convolution.** If $\Syrac(\ZZ/3^n\ZZ)$ were a *direct* convolution of $n$ i.i.d. pieces, then $\widehat\nu_n(\xi)=\prod\widehat\nu_1(\xi_j)$ and a per-factor bound $<1$ would give exponential decay automatically. But the convolution (2.2) is **skew**: the second block is dilated by the *random* unit $3^m 2^{-(a_1+\cdots+a_m)}$, so the frequency $\xi$ seen by the second block is itself randomized by the first block. This is exactly why Tao's submultiplicativity (2.3) only yields $c_{n_1+n_2-1}\ge c_{n_1}c_{n_2}$ (a *lower* bound on the min-atom, going the "easy" direction) and **cannot** be reversed into an exponential *upper* bound on $\widehat\nu_n$. The numerics in §2.3 ($c_n3^n$ decreasing slowly) show $c_n$ does decay sub-exponentially-corrected, but submultiplicativity alone is consistent with $\beta>1$ (a genuine failure of $\mathrm{MIX}$). **Ruling out $\beta>1$ is the open problem.**

- **The drift coupling (Proposition 4.2) cannot be undone by the tilt alone at the level of bounds.** The tilt $s^*$ re-centers the *mean* drift to $0$, which is necessary for natural-density stationarity, but it does not by itself produce *cancellation* in (6.3); it only changes the weight $w(\mathbf a)$. Cancellation still has to come from the oscillatory factor $e(\xi\Psi/3^n)$, i.e. from genuine $3$-adic equidistribution of $\Psi(\mathbf a)$ — which is (B2).

---

## 7. Honest assessment of the remaining gap

**What is established (unconditionally) here:**

1. A precise, numerically-verified reconstruction of the Syracuse random variable, the offset map, the skew-convolution, $c_n$, and the two analytic engines (§§2–3). *Expository; attributions to Tao.*
2. **Lemma 4.1** (the dyadic decomposition is measure-neutral): proved in full. Consequence: the *entire* log-vs-natural obstruction lives in the odd-integer statement, not in handling $\nu_2(N)$.
3. **Proposition 4.2** (localization): the obstruction is the **stationarity of the sampling measure under the multiplicative first-passage map** — log measure $dN/N$ is preserved because the map is a translation on $\log N$; natural measure $dN$ is not, picking up a residue-correlated $e^{-D_n}$ tilt. This is the exact-step answer the brief asked for. *(Structural/heuristic strength, but precisely formulated.)*
4. **Lemma 6.1 (Plancherel dictionary)** and **Lemma 6.2 (exponential decay $\Rightarrow$ natural-density equidistribution)**: both proved in full. Lemma 6.2 isolates the quantitative heart: the passage from $\ell^2$ to TV on $(\ZZ/3^n\ZZ)^\times$ costs a factor $3^{n/2}$, so **natural density needs Fourier decay $3^{-\theta n}$ with $\theta>\tfrac12$, whereas Tao has only $n^{-A}$.** This factor $3^{n/2}$ *is* the log$\to$natural gap, quantified.

**The cleanest conditional theorem (the deliverable):**

> $\mathrm{MIX}(\theta)$ [exponential decay $3^{-\theta n}$, $\theta>\tfrac12$, of the **tilted** Syracuse characteristic function (5.3)] $\;\Longrightarrow\;$ Tao's theorem in **natural** density (Conditional Theorem 5.2).

**What $\mathrm{MIX}(\theta)$ reduces to, and its status:**

- It is a **quantitative, exponential-rate, drift-tilted form of Tao's own $\beta=1$ conjecture** (`open_problems.md` A.2). Plain $\beta=1$ is open; $\mathrm{MIX}(\theta)$ is stronger and open.
- Equivalently it is a **power-saving bound for the $3$-adic exponential sum (6.3)** twisted by the geometric flow of multiplication-by-$2^{-1}$ on $(\ZZ/3^n\ZZ)^\times$. No such unconditional bound is known; the obstruction (skew convolution + drift coupling, §6.4) is structural, not a packaging artifact.

**The honest size of the remaining gap.** Large, but *precisely located*:

1. **Analytic core (the hard 90%).** Prove exponential cancellation in (6.3). This is genuinely open and is the same wall as Tao's $\beta=1$; nothing here lowers that wall. I did **not** make progress on the cancellation itself. The contribution is to show *exactly how much* cancellation is needed ($\theta>\tfrac12$) and that it must be of the *tilted* law.
2. **Transport-machinery core (the remaining 10%, but real).** Steps A and C of Conditional Theorem 5.2 reproduce Tao's iteration under the tilted natural-density measure. I have given the architecture and the Esscher/tilt mechanism, but **not** a formalization-ready proof; a faithful reproduction of Tao's first-passage iteration under the tilt is required, and a red-team pass against the actual paper (Step 2 of the protocol) is mandatory before any of Theorem 5.2's non-Lemma-6.2 steps are trusted.

**Bottom line for the brief's four questions** is recorded in the agent report; in one line: *the log→natural gap reduces, cleanly and with the exact required rate identified ($3^{-\theta n}$, $\theta>\tfrac12$, tilted), to a power-saving exponential-sum bound that is equivalent to a quantitative form of Tao's open $\beta=1$ conjecture — and that bound remains open, with a structural reason (skew convolution + drift coupling) for why Tao's superpolynomial decay cannot be amplified to reach it.*

---

## 8. Verification-protocol status

- **Step 1 (computational sanity):** PASSED for the *definitional* content — `experiments/verify_syracuse_rv.py` reproduces the $n=1$ Syracuse law exactly, confirms support on units, confirms submultiplicativity (2.3) on $n\le5$, and computes $c_n$, $c_n3^n$, and $\sup|\widehat\nu_n|$. Log at `experiments/verify_syracuse_rv_log.md`. The asymptotic claims (3.1)/(5.3) are *not* finitely checkable; for them Step 1 is "test-case construction," satisfied by the small-$n$ tables plus the structural derivation.
- **Step 2 (red-team):** NOT done. Required, with emphasis on: (a) faithfulness of §5 Steps A/C to Tao's actual transport propositions (the secondary-source reconstruction must be checked against the paper); (b) correctness of the tilt value $s^*$ and the Esscher step; (c) the claim that $\mathrm{MIX}(\theta)$ is strictly stronger than Prop 1.17 and equivalent to a tilted $\beta=1$.
- **Step 3 (Lean):** Lemmas 4.1, 6.1, 6.2 are elementary and formalizable; the rest is out of scope. Not yet attempted.
- **Step 4 (Alex Ye):** pending Steps 2–3.

This document is `[unverified]` and not citable as a theorem until the protocol completes. The conditional *reduction* is the claim to scrutinize; the unconditional Lemmas 4.1/6.1/6.2 are the parts most likely to survive intact.
