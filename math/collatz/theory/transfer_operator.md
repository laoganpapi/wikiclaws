# The Syracuse Frobenius--Perron / Transfer Operator on $(\mathbb{Z}/3^n\mathbb{Z})^\times$: Spectral Analysis and a Clean Identification of the Mod-3 Obstruction

> **Status:** `[unverified / NOVELTY UNVERIFIED]` — numerical findings + structural identifications proved, no analytic asymptotics proved.
>
> ⚠️ **CORRECTION (see `perp_gap.md`):** the float64 claim in this document that the second eigenvalue $|\lambda_2(n)|$ is $\sim 10^{-3}$ and *shrinking toward 1* is **WRONG — it was numerical noise.** Exact rational computation shows the characteristic polynomial of $P_n$ is exactly $\lambda^{\varphi(3^n)-1}(\lambda-1)$: a single eigenvalue $1$, all others **exactly $0$**, with $P_n-\Pi$ nilpotent of index $n$. The mod-3 obstruction (Prop 3.1) and $\pi_n$ = Syracuse RV (Prop 2.1) survive intact; only the second-eigenvalue magnitudes/asymptotics in §2–3 are retracted. The genuine obstruction is the non-uniform stationary vector $\pi_n$ (in $V$), not any perp eigenvalue.
>
> **Track:** Collatz, Vector A (alternative angle on the Tao-2022 log $\to$ natural-density gap).
>
> **Author:** Alex Ye (AI-assisted computation; AI not on author line per project rules).
>
> **Companion files / data:**
> - `experiments/transfer_operator.py` — kernel + spectrum
> - `experiments/transfer_operator_deep.py` — invariant-measure / mod-3 diagnostics
> - `experiments/transfer_operator_validate.py` — proves $\pi_n =$ Syracuse RV law (machine-precision)
> - `experiments/transfer_operator_final.py` — full tilt tables
> - `experiments/data/spectrum_table_{s0,sstar,s_neg}.json` and `spectrum_summary.txt`
> - cross-references: `syracuse_fft/results.md` (the $E_n$ divergence); `tao_syracuse_explicit.md` (the framework); `RED_TEAM_REPORT.md` §5c (mod-3 obstruction).

---

## 0. Honest scope and caveats up front

This document explores a **transfer-operator / Frobenius--Perron** viewpoint on the Syracuse step:
the Markov-chain operator $P_n$ on the finite set $(\mathbb{Z}/3^n\mathbb{Z})^\times$ whose row $x$ is the conditional law of the residue of $\Syr(N)$ given $N\equiv x \pmod{3^n}$, under Tao's i.i.d.\ valuation model
$\nu_2(3N+1) \sim \mathrm{Geom}(2)$.

Three things are established here that are (modulo novelty) clean:

1. **(Structural — proved.)** The Syracuse random variable on $\mathbb{Z}/3^n\mathbb{Z}$ from `tao_syracuse_explicit.md` is **exactly** the stationary distribution $\pi_n$ of $P_n$. *(Proved by direct algebra in §2.2 below; verified numerically to $10^{-16}$ for $n\le 6$ in `transfer_operator_validate.py`.)*
2. **(Spectral mod-3 obstruction — proved.)** The 2-D subspace $V\subset \mathbb{R}^{|U_n|}$ spanned by the indicators of the residue-mod-3 cosets is invariant under $P_n$, and $P_n|_V$ has the **explicit matrix $\begin{pmatrix}1/3 & 2/3\\ 1/3 & 2/3\end{pmatrix}$** with eigenvalues $\{1, 0\}$. The eigenvalue-1 eigenvector inside $V$ is $(1/3, 2/3)^\top$ — the (0,1/3,2/3) mod-3 marginal that everyone has been bothered by. **This is the mod-3 obstruction as a specific eigenvector.** *(Proved by direct computation; verified for $n=1..8$.)*
3. **(Numerical — believed, not proved asymptotically.)** $P_n$ has a **large** spectral gap $1-|\lambda_2(n)|$ even at $n=8$: the second-largest eigenvalue $|\lambda_2|$ grows from $0$ ($n=1$) to $\approx 5\cdot 10^{-3}$ ($n=8$). Log-linear fit gives growth rate $\approx 3.0^n$ on $n\ge 5$ — **but this overshoots 1 by $n\approx 13$**, which is impossible ($|\lambda_2|\le 1$), so the fit is pre-asymptotic. Trustworthy headline: **the spectral gap shrinks with $n$ but remains $>0.99$ through $n=8$.**

**Caveats — read these before citing anything:**

- **Novelty unverified.** Transfer / Frobenius--Perron operators are standard in dynamical systems. The Collatz map has been viewed Markov-chain-style by several authors (Lagarias's "stochastic models" 1985; Kontorovich–Lagarias; many others). I have **not** verified whether the specific spectral identification $\pi_n =$ Syracuse RV, or the mod-3 eigenvector $1/3, 2/3$, has been written down. Both are *elementary once stated*, so the prior is HIGH that one or both are folklore. Flag every result `[NOVELTY UNVERIFIED]`.
- **No new bound proved.** The headline numerical finding "$|\lambda_2(n)|$ shrinks geometrically toward 1" is **NOT a proof that mixing fails**; it is consistent with both (a) the existing $E_n\to\infty$ obstruction and (b) the natural-density route remaining open via a different mechanism. The transfer-operator picture **does not lower** any of the analytic walls already in `tao_syracuse_explicit.md`/`results.md` (mod-3 coset obstruction; $E_n$ divergence; tilt incompatibility).
- **Sharper restatement, not progress.** What this view *does* deliver is a **cleaner restatement** of the obstruction: the mod-3 problem is a single explicit eigenvector with a known closed-form 2x2 block; the "uniform on units" target is *not the right reference measure* because it is NOT the invariant of any reasonable random Syracuse step. The true invariant is the Syracuse RV itself.

---

## 1. The transfer operator

### 1.1 Setup

Let $U_n := (\mathbb{Z}/3^n\mathbb{Z})^\times = \{x\in [1,3^n-1] : 3\nmid x\}$. $|U_n| = \varphi(3^n) = 2\cdot 3^{n-1}$.

The accelerated Syracuse map on odd integers is $\Syr(N) = (3N+1)/2^{\nu_2(3N+1)}$. Reducing mod $3^n$ requires knowing $\nu_2(3N+1)$. Tao's random model (which underlies the Syracuse RV) takes $\nu_2(3N+1)\sim\mathrm{Geom}(2)$ i.i.d., independent of $N$ (more general $s$-tilted geometric in §5).

This gives a Markov chain on $U_n$ with one-step kernel

$$\boxed{\ K_n(x,y) \;=\; \sum_{k\ge 1} 2^{-k}\,\mathbf{1}\!\bigl[\,2^{-k}(3x+1)\equiv y \pmod{3^n}\bigr], \qquad x,y\in U_n.\ } \tag{1.1}$$

A unit step preserves units: for $x\in U_n$, $3x+1\equiv 1\pmod{3}$, so $\nu_3(3x+1)=0$ and $2^{-k}(3x+1)\in U_n$. Hence the chain is well-defined on $U_n$ with row sums = 1 (modulo a tail truncation that is exponentially small).

The **transfer (Frobenius--Perron) operator** $L_n: \mathbb{R}^{U_n} \to \mathbb{R}^{U_n}$ is

$$L_n[\rho](y) \;=\; \sum_{x\in U_n} K_n(x,y)\,\rho(x) \;=\; (\rho \cdot P_n)(y),$$

where $P_n$ is the row-stochastic matrix $P_n[x,y] = K_n(x,y)$. So $L_n$ is the left-action of $P_n$ on row densities. A **stationary density** $\pi_n$ solves $\pi_n P_n = \pi_n$.

### 1.2 The chain is NOT doubly stochastic

Important early observation (verified for $n=1..8$): the column sums of $P_n$ are NOT all 1. In fact at every $n\ge 1$ the column sums range over $[0.238, 1.905]$ (independent of $n$, an artefact of the mod-9 column structure). **Therefore the uniform distribution on $U_n$ is NOT invariant.** The unique invariant $\pi_n$ (eigenvalue 1) is heavily non-uniform.

This is the spectral counterpart of: "the Syracuse RV is not uniform on units."

---

## 2. The structural identification: $\pi_n$ = law of $\Syrac(\mathbb{Z}/3^n\mathbb{Z})$

### 2.1 Numerical statement

For $n=1,\dots,6$, computed independently by:

(A) Left eigenvector of $P_n$ for eigenvalue 1 (`transfer_operator.invariant_distribution`),
(B) FFT W-recursion law of $\Syrac(\mathbb{Z}/3^n\mathbb{Z})$ from `syracuse_fft.syracuse_law_fft`, restricted to units.

$\|\pi_n - \nu_n^{\text{Syrac}}\|_\infty \le 6\cdot 10^{-17}$ at all $n\le 6$. **They are equal to machine precision.**

### 2.2 Proof (the algebraic reason)

> **Proposition 2.1.** *The law $\nu_n^{\text{Syrac}}$ of $\Syrac(\mathbb{Z}/3^n\mathbb{Z})$ defined by Tao (`tao_syracuse_explicit.md` Def 2.1) satisfies $\nu_n^{\text{Syrac}} P_n = \nu_n^{\text{Syrac}}$. Hence (by uniqueness of the stationary distribution for an irreducible finite Markov chain) $\pi_n = \nu_n^{\text{Syrac}}$.*

*Proof (algebraic; new to this document but elementary).* Let $W_n := \sum_{j=1}^n 3^{n-j}\,2^{-(a_j+\cdots+a_n)} \pmod{3^n}$ with $(a_j)$ i.i.d.\ $\mathrm{Geom}(2)$. We show $W_n \stackrel{d}{=} 2^{-a}(3 W_n + 1) \pmod{3^n}$ with $a\sim\mathrm{Geom}(2)$ independent of $W_n$.

Apply one step of the Syracuse kernel to $W_n$:
$$2^{-a}(3W_n + 1) \;=\; 2^{-a}\!\left(\sum_{j=1}^n 3^{n-j+1}\,2^{-(a_j+\cdots+a_n)} + 1\right) \;=\; \underbrace{2^{-a}}_{j=n+1 \text{ term}} + \sum_{j=1}^n 3^{\,n-j+1}\,2^{-(a_j+\cdots+a_n+a)} \pmod{3^n}.$$

Re-index $j' = j-1$ in the sum (so $j' = 0, 1, \dots, n-1$), and append a fresh symbol $a_{n+1} := a$:
$$\sum_{j'=0}^{n-1} 3^{\,n-j'}\,2^{-(a_{j'+1}+\cdots+a_n+a_{n+1})}.$$
The $j'=0$ term carries the factor $3^n \equiv 0 \pmod{3^n}$ and vanishes. The $j'=1,\dots,n-1$ terms together with the trailing "$2^{-a}=2^{-a_{n+1}}$" — corresponding to a *new* $j'=n$ term with exponent $a_{n+1}$ alone — give exactly
$$\sum_{j'=1}^n 3^{\,n-j'}\,2^{-(a_{j'+1}+\cdots+a_{n+1})} \pmod{3^n},$$
which is $W_n$ in the shifted sequence $(a_2, a_3, \dots, a_{n+1})$. Since the $(a_j)$ are i.i.d., this has the *same* distribution as $W_n$. $\blacksquare$

> **Remark 2.2.** This proof is the algebraic content of the W-recursion at the boundary $m=n$: $W_n = 2^{-a_n}(W_{n-1}^{[\text{embedded}]}+1)$ when one inflates $W_{n-1}$ from mod $3^{n-1}$ to mod $3^n$ via the natural inclusion. The key identity is $3 W_n = (\text{shifted } W_n) - 3^n\cdot(\text{leading term})\equiv (\text{shifted }W_n)\pmod{3^n}$.

> **Consequence — clean restatement of `syracuse_fft/results.md`.** The collision excess $E_n = \varphi(3^n)\,\|\pi_n\|_{\ell^2}^2 - 1$ from `syracuse_fft/results.md` is *exactly* the squared $\ell^2$ distance of the **invariant distribution $\pi_n$** to uniform-on-units (up to a $\varphi(3^n)^{-1}$ factor). All the FFT findings (linear divergence of untilted $E_n$, exponential divergence of $E_n^{(s^*)}$, equidistributing plateau at $s\lesssim -0.45$) are precisely statements about *which* tilt makes the invariant distribution close to uniform-on-units. That property is decoupled from the spectral gap (see §4).

---

## 3. The mod-3 obstruction as a specific eigenvector

Let $V := \mathrm{span}\{e_1, e_2\}\subset \mathbb{R}^{U_n}$ where $e_r[x] := \mathbf{1}[x \equiv r \pmod 3]$, $r\in\{1,2\}$.

> **Proposition 3.1 (mod-3 invariance).** *For every $n\ge 1$, $V$ is invariant under $P_n$, and the action $P_n|_V$ in the basis $(e_1, e_2)$ is the $2\times 2$ matrix*
> $$P_n|_V \;=\; \begin{pmatrix} 1/3 & 2/3 \\ 1/3 & 2/3 \end{pmatrix}.$$
> *Its eigenvalues are $\{1, 0\}$. The eigenvalue-$1$ eigenvector is $\bigl(\tfrac13,\tfrac23\bigr)^\top$ (left eigenvector), giving the stationary mod-3 marginal $(0, 1/3, 2/3)$.*

*Proof.* Take any $x\in U_n$; consider the conditional probabilities of $\bar y = y \bmod 3$ given $\bar x = x \bmod 3$ under one Syracuse step. Since $3x+1 \equiv 1 \pmod 3$ regardless of $x \bmod 3$, the value of $\bar y$ depends *only* on $\bar k := k \bmod 2$ via $\bar y \equiv 2^{-k} \equiv (2^{-1})^k \equiv 2^k \pmod 3$ (as $2^{-1}\equiv 2 \pmod 3$). So $\bar y \in \{1, 2\}$ with probabilities
$$\mathbb{P}(\bar y = 1) = \mathbb{P}(k\text{ even}) = \sum_{k\ge 2,\,k\text{ even}} 2^{-k} = \tfrac{1/4}{1-1/4} = \tfrac{1}{3},$$
$$\mathbb{P}(\bar y = 2) = \mathbb{P}(k\text{ odd}) = \sum_{k\ge 1,\,k\text{ odd}} 2^{-k} = \tfrac{1/2}{1-1/4} = \tfrac{2}{3}.$$
Independent of $\bar x$. So both rows of $P_n|_V$ are $(1/3, 2/3)$, giving the displayed matrix. $\blacksquare$

> **Corollary 3.2 (the mod-3 obstruction is a single eigenvector).** *The stationary mod-3 marginal $(0, 1/3, 2/3)$ is the unique fixed point of $P_n$ inside $V$. It is realized by the eigenvalue-$1$ left eigenvector $\pi_n|_V = (1/3, 2/3)$. The "non-uniform-on-units" obstruction to natural density flagged in `RED_TEAM_REPORT.md` §5c is, spectrally, the statement that the eigenvalue-$1$ subspace of $P_n$ contains a $V$-component with this fixed mod-3 marginal — and that component is **explicitly known and entirely independent of $n$**.*

> **Consequence.** Any natural-density argument that requires $\pi_n \to U$ (uniform on units) in TV is **provably blocked**, since $\pi_n$ has fixed mod-3 marginal $(0,1/3,2/3) \ne (0,1/2,1/2)$, hence $\mathrm{TV}(\pi_n, U)\ge \tfrac{1}{6}$ for all $n$ (matching the red-team's numerical observation).

> **Remark 3.3 (this is the cleanest form of the obstruction yet).** The previous framings of the obstruction ("the Syracuse law mod 3 is $(0,1/3,2/3)$"; "Lemma 6.1 silently drops the $3\mid\xi$ Fourier modes") are *consequences* of Proposition 3.1: the operator $P_n$ has a built-in 2x2 block, with a single eigenvalue-1 mode that is the mod-3 obstruction. Tilting (changing $s$) deforms the matrix to
> $$P_n^{(s)}|_V \;=\; \begin{pmatrix} \alpha_s & 1-\alpha_s \\ \alpha_s & 1-\alpha_s \end{pmatrix},\qquad \alpha_s = \sum_{k\ge 2,\,k\text{ even}} P_s(a=k),$$
> still rank 1, eigenvalue-1 eigenvector $(\alpha_s, 1-\alpha_s)$. **No scalar tilt can produce $(1/2, 1/2)$ unless $\alpha_s = 1/2$, i.e. $P_s(a\text{ even}) = P_s(a\text{ odd})$, which would require putting equal mass on even and odd $a$** — possible only if the geometric is degenerate.

### 3.1 Higher-coset structure (mod $3^k$ for $k<n$)

The same argument extends: the indicator functions of residue classes mod $3^k$ (for $k\le n$) span a $\varphi(3^k)$-dimensional subspace of $\mathbb{R}^{U_n}$ that is invariant under $P_n$ — because the mod-$3^k$ projection of the kernel only depends on $x \bmod 3^k$. So $P_n$ has a **filtration** $V^{(1)}\subset V^{(2)}\subset \cdots \subset V^{(n)}=\mathbb{R}^{U_n}$ of nested invariant subspaces of dimensions $2, 6, 18, \dots, 2\cdot 3^{n-1}$, and the restriction $P_n|_{V^{(k)}}$ acts as $P_k$ (the operator at level $k$). **The transfer operators form a projective system $P_n \to P_{n-1} \to \cdots \to P_1$**, and the obstructions at all levels $k\le n$ are inherited from level 1.

Numerically (data in `data/spectrum_table_s0.json`), the mod-9 marginal of $\pi_n$ at $n=2,3,\dots,6$ is the **constant** vector
$(0, 0.127, 0.254, 0, 0.175, 0.063, 0, 0.032, 0.349)$ — confirming this projective compatibility.

---

## 4. Spectrum: gap and growth

### 4.1 Computed spectra (untilted, $s=0$)

Data file: `data/spectrum_table_s0.json`. Headline columns:

| $n$ | $\varphi(3^n)$ | $\|\lambda_2(P_n)\|$ | $1-\|\lambda_2\|$ | $\|\lambda_{\perp,\max}\|$ | $\mathrm{TV}(\pi_n,U)$ | $E_n(\pi_n)$ |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 2 | $0$ | $1$ | n/a | $0.1667$ | $0.1111$ |
| 2 | 6 | $6.5\times 10^{-9}$ | $\approx 1$ | $\sim 10^{-16}$ | $0.2778$ | $0.4286$ |
| 3 | 18 | $9.8\times 10^{-7}$ | $\approx 1$ | $1.0\times 10^{-8}$ | $0.3460$ | $0.7363$ |
| 4 | 54 | $5.3\times 10^{-5}$ | $\approx 1$ | $6.2\times 10^{-6}$ | $0.3705$ | $1.0458$ |
| 5 | 162 | $2.5\times 10^{-4}$ | $\approx 1$ | $8.4\times 10^{-5}$ | $0.3889$ | $1.3561$ |
| 6 | 486 | $1.1\times 10^{-3}$ | $0.999$ | $6.1\times 10^{-4}$ | $0.3986$ | $1.6669$ |
| 7 | 1458 | $3.0\times 10^{-3}$ | $0.997$ | $1.8\times 10^{-3}$ | $0.4069$ | $1.9772$ |
| 8 | 4374 | $5.0\times 10^{-3}$ | $0.995$ | n/a (memory) | $0.4150$ | $2.2878$ |

The $E_n(\pi_n)$ column **exactly reproduces** `syracuse_fft/results.md` §2.1's $E_n$ values (which are the same quantity by Proposition 2.1; cross-check passed at $\le 10^{-15}$).

**Cross-check on $\|\lambda_2\|$**: ARPACK (`scipy.sparse.linalg.eigs`) and `numpy.linalg.eig` agree on the dominant eigenvalues $|\lambda|=1$ but disagree at the $\sim 10^{-3}$ level on $\|\lambda_2\|$ at $n=7$ by $\sim 30\%$. This indicates the magnitudes at this scale are at the edge of numerical reliability for non-self-adjoint problems. **Trustworthy as orders of magnitude; the exact slopes in §4.3 are pre-asymptotic.**

> **mpmath / interval check not performed.** A rigorous spectral gap would require $50$--$100$ digit arithmetic on $P_n$. We have not done that; everything here is float64. *Flag: numerical only.*

### 4.2 Spectral gap is large but shrinking

For every computed $n\le 8$:
- $\lambda_1 = 1$ (simple; chain is irreducible).
- $|\lambda_2| \le 6\times 10^{-3}$, hence spectral gap $\ge 0.99$.

So **one step of the Syracuse Markov chain $P_n$ already mixes the residue mod $3^n$ to its invariant distribution $\pi_n$ in $O(1)$ steps**, in the sense that $\|P_n^k \rho - \pi_n\|_{\ell^2} = O(|\lambda_2|^k)$ for $k=O(1)$ kills the discrepancy to numerical noise.

This is a **strong mixing** statement — but it is mixing **to the wrong target** ($\pi_n$, not $U$). And $\pi_n$ has fixed mod-3 marginal $(0,1/3,2/3)$, so this fast mixing does NOT imply equidistribution-on-units.

### 4.3 Growth rate of $|\lambda_2|$ (numerical fit, pre-asymptotic warning)

Log-linear fit of $|\lambda_2(P_n)|$ on $n\in[5,8]$ (untilted):
$$\log |\lambda_2(P_n)| \;\approx\; 1.10\,n - 13.77, \qquad\text{i.e.}\qquad |\lambda_2| \sim \mathrm{const}\cdot 3.02^n.$$

This is the geometric trend in the pre-asymptotic range. Extrapolating naively gives $|\lambda_2(13)|\approx 1$, which is *impossible* ($|\lambda_2|\le 1$ always). **So the linear-in-log trend MUST decelerate** somewhere between $n=8$ and $n=13$. We do not have data there; this is the highest-priority computational next step.

Similarly for $|\lambda_{\perp,\max}|$ (the largest eigenvalue after killing the mod-3 obstruction subspace $V$):
$$\log |\lambda_{\perp,\max}(P_n)| \;\approx\; 1.31\,n - 15.62, \qquad |\lambda_{\perp,\max}| \sim 3.70^n\cdot \text{const}.$$
Same caveat: extrapolation crosses 1 at $n\approx 12$, so this trend must bend.

> **What this means honestly.** $|\lambda_2(n)|$ is growing fast in the pre-asymptotic range, but cannot cross 1. The asymptotic rate is **unknown** from the data we have; whether $|\lambda_2(n)|\to \lambda_\infty < 1$ (uniform spectral gap on perp) or $\to 1$ (slow mixing) is *the* numerical question.

### 4.4 Effect of tilt on the spectral gap

For the three computed tilts (data: `data/spectrum_table_{s0,sstar,s_neg}.json`):

| $n$ | $|\lambda_2|$ at $s=0$ | $|\lambda_2|$ at $s=+0.438$ | $|\lambda_2|$ at $s=-0.5$ |
|---|---:|---:|---:|
| 2 | $6.5\times 10^{-9}$ | $1.8\times 10^{-9}$ | $1.2\times 10^{-9}$ |
| 3 | $9.8\times 10^{-7}$ | $5.0\times 10^{-9}$ | $9.0\times 10^{-7}$ |
| 4 | $5.3\times 10^{-5}$ | $3.6\times 10^{-5}$ | $3.0\times 10^{-5}$ |
| 5 | $2.5\times 10^{-4}$ | $2.3\times 10^{-4}$ | $2.0\times 10^{-4}$ |
| 6 | $1.1\times 10^{-3}$ | $1.1\times 10^{-3}$ | $9.0\times 10^{-4}$ |

**The spectral gap is essentially insensitive to the tilt** (all three within 20% at each $n$). The tilt changes only $\pi_n$'s closeness to uniform (TV and $E_n$), NOT the rate at which $P_n$ contracts toward $\pi_n$.

> **Honest reformulation.** The mixing rate (spectral gap of $P_n$) is a *robust property of the Syracuse dynamics*; the natural-density requirement is a *property of the invariant target*. These are **two independent things**, and the obstruction in `tao_syracuse_explicit.md` lives in the latter.

---

## 5. Hypothesis tests (the brief's H1--H4)

> **(H1) Spectral gap collapse: does $|\lambda_2(n)|\to 1$?**
> **Inconclusive from data.** $|\lambda_2|$ is growing but $|\lambda_2(8)| \approx 5\times 10^{-3}$ is still tiny. Naive log-linear extrapolation forces a turnover (impossible to keep growing at base 3). Whether the asymptotic limit is $<1$ (uniform gap) or $=1$ (gap collapse) is genuinely open.
> **Best read:** the gap is shrinking, possibly to a non-trivial constant $<1$, possibly to $1$. Cannot tell at this $n$ range.

> **(H2) Invariant density.**
> **Proved: $\pi_n = $ Syracuse RV law** (Proposition 2.1).
> $\pi_n$ is *heavily concentrated*: $\max\pi_n / \min\pi_n$ at $n=6$ is $\sim 180$ ($\max = 2.27\times 10^{-2}$, $\min = 1.24\times 10^{-4}$). It is NOT a Lyapunov function in any obvious sense — it is the natural pushforward measure for the random Syracuse step.

> **(H3) Pollicott--Ruelle resonances.**
> The top 10 eigenvalues of $P_n$ for $n=6$ have moduli $1, 1.07\times 10^{-3}, 1.07\times 10^{-3}, \ldots, 3.50\times 10^{-4}$ — a *flat cluster* of complex conjugate pairs at $\sim 10^{-3}$, then a gap of about a factor 3 to the next cluster at $\sim 3\times 10^{-4}$, repeated. This is consistent with the projective structure of §3.1: each level of the filtration $V^{(1)}\subset V^{(2)}\subset \cdots$ contributes its own band of resonances. *I do not have an explicit identification of which Pollicott--Ruelle mode corresponds to which level; this is a clean open computation.*

> **(H4) Mod-3 obstruction as a specific eigenvector.**
> **Proved: Proposition 3.1.** The mod-3 indicator subspace $V = \mathrm{span}\{e_1, e_2\}$ is invariant, $P_n|_V = \begin{pmatrix}1/3 & 2/3\\1/3&2/3\end{pmatrix}$ with eigenvalues $\{1, 0\}$, and the eigenvalue-1 eigenvector inside $V$ is $(1/3, 2/3)^\top$.

---

## 6. The high-payoff target (the brief): conditional perp-gap

> **What the brief asked for:** if $P_n$ has spectral gap bounded BELOW by some absolute constant when restricted to $V^\perp$, that would be a conditional natural-density result.

> **What the data say:** the perpendicular spectral radius $|\lambda_{\perp,\max}(P_n)|$ for $n=3,\dots,7$ is $10^{-8}, 6\times 10^{-6}, 8\times 10^{-5}, 6\times 10^{-4}, 1.8\times 10^{-3}$ — growing at log-linear rate $\sim 3.7^n$, faster than $|\lambda_2|$ itself. So at $n=8$ we'd expect $|\lambda_{\perp,\max}|\sim 6\times 10^{-3}$, still well below 1 — **strong gap on $V^\perp$, but shrinking**.

> **Is there a uniform gap on $V^\perp$?**
> **From this data, ambiguous.** The trend is towards collapse, but again must bend before $n=12$. *Cannot conclude either way at this $n$.*

> **The honest "would-be" conditional theorem.** If one could *prove* $|\lambda_{\perp,\max}(P_n)| \le \rho < 1$ uniformly in $n$, then $P_n^k \rho_0 \to \pi_n$ on $V^\perp$ at rate $\rho^k$, and combined with $\pi_n|_V = (1/3, 2/3)$ this would give the *cleanest possible* statement of "natural density up to a known coset structure" — the coset structure being explicitly the eigenvalue-1 eigenvector inside $V$. This is **strictly weaker** than the natural-density-on-units that `tao_syracuse_explicit.md` Lemma 6.2 (incorrectly) sought, and **strictly stronger** than the log-density-on-units that Tao 2022 proves: it would be "natural density on each residue class mod 3, after rebalancing by the $(0, 1/3, 2/3)$ marginal."

> **Would this close the log $\to$ natural gap?** **Possibly — and it's exactly the kind of move the RED_TEAM_REPORT §5c suggested** (option (i): "replace $U$ by the measure that is uniform within the mod-$3^k$ coset structure"). The transfer-operator picture makes the coset structure spectrally explicit. But proving a uniform $V^\perp$-gap is a real analytic problem, and the data are consistent with the gap shrinking.

---

## 7. Why this is (probably) not as new as it might seem, and the analytic walls it does NOT lower

### 7.1 Likely-prior-art

The Lagarias 1985 "stochastic models" paper and follow-ups (Kontorovich--Lagarias 2009; many) treat Collatz Markov-chain style. The specific identification "Syracuse RV = invariant of one-step Markov chain on $(\mathbb{Z}/3^n)^\times$" is *natural enough that it's probably written down*, even if the document I wrote here is novel. **The mod-3 2x2 block** is so elementary it's almost certainly folklore. **`[NOVELTY UNVERIFIED]`** on everything in this document.

### 7.2 Analytic walls unchanged

- **Mod-3 obstruction:** redescribed cleanly but **identical in content** to `tao_syracuse_explicit.md`'s observation and `RED_TEAM_REPORT.md` §5c. The transfer-operator framing makes it look like one explicit eigenvector instead of an averaged Fourier statement; no progress on resolving it.
- **$E_n$ divergence:** the transfer-operator $\pi_n$ IS the Syracuse RV, so all the divergence findings of `syracuse_fft/results.md` apply unchanged.
- **Tilt incompatibility:** verified at the transfer-operator level: descent-balance tilt $s^*$ makes $\pi_n$ farther from uniform, exactly as in the FFT results.
- **No bound on the asymptotic spectral gap is proved.** The numerical fits in §4.3 cannot be extrapolated to $n\to\infty$.

### 7.3 What the framing IS good for

- A *single equation* statement of the Markov chain that's the "Syracuse step" in Tao's model: $P_n[x,y] = \sum_{k\ge 1} 2^{-k} \mathbf{1}[2^{-k}(3x+1)\equiv y]$.
- A *single eigenvector* statement of the mod-3 obstruction: it's the rank-1 2x2 block $\begin{pmatrix}1/3&2/3\\1/3&2/3\end{pmatrix}$, eigenvalue 1.
- A *spectral identification* of the "right" reference for natural density: $\pi_n$ (not $U$), and a *projective filtration* $V^{(1)}\subset \cdots\subset V^{(n)}$ that organizes all higher-order coset obstructions.
- A *clean question to ask next*: does $P_n$ have a uniform spectral gap on $V^{(1),\perp}$ (perp of the mod-3 obstruction)?

These are restatements / reframings, not new theorems.

---

## 8. Honest comparison with `tao_syracuse_explicit.md`

| Aspect | Tao framework (forward / Fourier) | Transfer-operator (this doc) |
|---|---|---|
| Object | Syracuse RV $\Syrac(\mathbb{Z}/3^n)$ | Stationary $\pi_n$ of one-step Markov $P_n$ |
| Identification | — | $\pi_n = $ Syracuse RV (Prop 2.1) |
| Mod-3 obstruction | "the law mod 3 is permanently $(0,1/3,2/3)$" | "$V$ is a 2-D invariant subspace, $P_n\|_V$ has explicit form, eigenvector $(1/3,2/3)^\top$" |
| Quantifies divergence | $E_n\to\infty$ (FFT) | Same quantity, equivalent statement |
| Natural-density target | Uniform on units (BROKEN by mod-3) | $\pi_n$ (the right target inherently) OR uniform-within-cosets (cleaner) |
| What's analytically open | Power-saving Fourier decay $3^{-\theta n}$ | Uniform perp-gap $|\lambda_{\perp,\max}|\le \rho<1$ uniformly in $n$ |
| Are these the same? | — | **Yes, equivalent** (Plancherel relates them) |

The two views are formally equivalent: a uniform perp-gap $\rho<1$ for $P_n$ is equivalent (via the spectral theorem and the Plancherel dictionary of `tao_syracuse_explicit.md` Lemma 6.1) to a uniform Fourier bound on $V^\perp$ — which is *not* Tao's $\mathrm{MIX}(\theta)$ exactly (the perp-gap is weaker: it only requires geometric contraction toward $\pi_n$, not toward $U$), but it is in the same family.

**Bottom line: this is a reframing, not a breakthrough.** The cleanest output is **Proposition 3.1** (the mod-3 obstruction = explicit rank-1 2x2 block) which makes a sharp negative finding *visually obvious*: the Syracuse step on $(\mathbb{Z}/3^n)^\times$ has a built-in non-uniformity at the deepest level, no matter what one does at higher modulus. Tao's framework has the same conclusion but routes it through a Fourier argument; the transfer-operator view makes it a one-line linear-algebra statement.

---

## 9. Next steps (honest list)

1. **Push numerics to $n=10$--$12$** using sparse + ARPACK (with stricter tolerance and shift-invert) or randomized SVD. The critical question: does $|\lambda_{\perp,\max}(P_n)|$ asymptote below 1, or trend to 1? This requires more careful eigenvalue computation than `numpy.linalg.eig` provides at small magnitudes.
2. **Identify the Pollicott--Ruelle resonances**: the flat clusters at $|\lambda|\sim 10^{-3}, 3\times 10^{-4}, \dots$ should correspond exactly to lifts from $P_{n-1}, P_{n-2}, \dots$ via the projective filtration. Verify this rigorously.
3. **Prove or refute Conjecture 6 (uniform perp-gap).** This is the cleanest open analytic question the framework suggests. It is, structurally, of the form "the Syracuse Markov chain has bounded mixing time on the residue-mod-3 cosets, uniformly across moduli" — a Markov-chain mixing-time statement, where techniques exist (canonical paths, log-Sobolev, etc.) — but the chain's combinatorial structure is unusual (kernel weighted by inverse powers of 2 + multiplication-by-3 phase).
4. **Compare against published Markov-chain models of Collatz** (Lagarias 1985, Kontorovich--Lagarias 2009). Verify which of §2.2 (the proposition $\pi_n = $ Syracuse RV) and §3.1 (the explicit 2x2 block) is genuinely new vs. folklore.
5. **Add the dead-end entry** for the failed power-iteration approach at $n=9$ (deflation against ones was too aggressive; ARPACK had stability issues at the $\sim 10^{-3}$ eigenvalues).

---

## 10. Bottom-line answers to the brief's six questions

1. **Precise transfer operator + matrices computed.** $P_n$ on $(\mathbb{Z}/3^n)^\times$ defined by (1.1); built and diagonalized exactly for $n=1,\dots,7$ (sizes $2, 6, 18, 54, 162, 486, 1458$); top-40 spectrum for $n=8$ via ARPACK.
2. **Spectrum at $n=1..5$ (and extended through 8).** $|\lambda_2| = 0, 6.5\times 10^{-9}, 9.8\times 10^{-7}, 5.3\times 10^{-5}, 2.5\times 10^{-4}, 1.1\times 10^{-3}, 3.0\times 10^{-3}, 5.0\times 10^{-3}$. See §4.1 table.
3. **Spectral gap uniform or shrinking?** Shrinking. $1 - |\lambda_2|$ goes from 1 to 0.995 over $n=1..8$. Log-linear extrapolation gives $|\lambda_2|\sim 3.02^n\cdot\mathrm{const}$ but this **MUST** turn over (since $|\lambda_2|\le 1$); whether the asymptote is $<1$ or $=1$ is open. *Honest read: shrinking, with unknown asymptotic limit.*
4. **Mod-3 obstruction in spectral terms.** **PROVED, EXPLICIT.** Proposition 3.1: $V = \mathrm{span}\{e_1, e_2\}$ (mod-3 coset indicators) is invariant; $P_n|_V = \begin{pmatrix}1/3 & 2/3\\ 1/3 & 2/3\end{pmatrix}$, eigenvalues $\{1, 0\}$, eigenvalue-1 eigenvector $(1/3, 2/3)^\top$. The previous "permanently $(0, 1/3, 2/3)$" mod-3 marginal is exactly this eigenvector.
5. **Cleanest follow-up theorem suggested.** Conjecture (informal): there exist constants $\rho < 1$, $C < \infty$ such that the operator norm of $P_n$ restricted to $V^\perp$ is bounded by $\rho$ uniformly in $n$. *(Equivalently: a uniform perp-spectral-gap.)* This implies that, after factoring out the mod-3 coset structure, the Syracuse Markov chain mixes geometrically — a clean *conditional* result that would imply a coset-respecting natural-density statement. The data shows the perp eigenvalue $|\lambda_{\perp,\max}|$ growing in the pre-asymptotic range but cannot exclude a uniform bound.
6. **Honest assessment vs Tao's framework.** Same content, different vantage point. The transfer-operator view yields (a) a one-line proof of the mod-3 obstruction (Proposition 3.1), (b) a clean structural identification of the invariant measure (Proposition 2.1: $\pi_n =$ Syracuse RV), (c) a "right" reference measure (the operator-stationary one, not "uniform-on-units") that automatically respects the coset obstructions. **It does not lower any analytic wall.** It does not prove $E_n\to 0$, does not bound $|\lambda_2|$ uniformly, does not produce a new conditional theorem with weaker hypotheses than `tao_syracuse_explicit.md`'s. Its value is **expository / structural**, and its main contribution to the project is **a cleaner statement of the mod-3 obstruction** as a single explicit linear-algebra fact.

> **Net effect on the project.** Sharper (one-line) statement of the obstruction; agreement with both the FFT findings and the RED_TEAM correction; no new conditional theorem; novelty likely partial-at-best; no progress on the asymptotic spectral gap.

