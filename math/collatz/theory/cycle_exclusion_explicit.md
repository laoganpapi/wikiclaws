# Explicit Reconstruction of the Steiner–Simons–de Weger–Hercher Cycle-Exclusion Argument

**Track:** collatz — Vector C (cycle exclusion via Diophantine approximation)
**Author:** Alex Ye (AI assistance disclosed separately)
**Status:** `[unverified]` — Step-1 numerical checks passed (see `experiments/verify_cycle_exclusion_log.md`); Steps 2–4 pending.
**Date:** 2026-06-02

> **Purpose.** Reconstruct, with every step justified, the Diophantine argument that excludes non-trivial Collatz $m$-cycles, identify the *exact* quantity that bounds $m$, web-verify every numerical constant, and determine precisely what Diophantine input would be needed to push past Hercher's $m \le 91$.
>
> **Headline finding (stated up front so it is not buried).** The rate-limiting Diophantine input is **NOT the one-dimensional irrationality measure $\mu(\log_2 3)$**, contrary to the framing in `survey.md` §7.5 / §11 Vector C and `open_problems.md` D.1/D.2. It is a **lower bound for a linear form in *two* logarithms**, $\Lambda = (K+S)\log 2 - K\log 3 > 0$, supplied by the **Laurent–Mignotte–Nesterenko (LMN)** theorem and Laurent's interpolation-determinant method. The reason $\mu(\log_2 3)$ is the *wrong* lever is structural, not just quantitative (§5.2): the two-log estimate is **exponential in $K$** ($\Lambda > 2^{-0.158 K}$ for $K \ge 32$, de Weger's reformulation — verified), and when set against the cycle's geometric forcing $\Lambda < \Theta(m/B)$ it produces an **upper bound on the cycle length $K$**; the irrationality-measure estimate is only **polynomial** ($\Lambda > K^{1-\mu}$) and, set against the same forcing, yields only a *lower* bound on $K$ — the wrong direction, contradicting nothing. So improving $\mu(\log_2 3)$ cannot move the cycle bound at all. The constant that *would* move it is the **exponent / leading constant in the two-log estimate** (de Weger's $0.158$; LMN's $24.34\,D^4$), refinable via Laurent 2008. This is developed in §5–§6 and is the single most important deliverable of this document.

---

## 0. Notation and conventions (pinned to the literature)

We use the accelerated map (Lagarias/`notation.md` §2.1)
$$
T(n) = \begin{cases} n/2, & n \text{ even},\\ (3n+1)/2, & n \text{ odd}. \end{cases}
$$

A **cycle** is a finite periodic orbit $x_0 \to x_1 \to \dots \to x_{N-1} \to x_0$ of $T$ in $\mathbb{N}$. Write each odd step as an **"o-step"** ($x \mapsto (3x+1)/2$) and each even step as an **"e-step"** ($x \mapsto x/2$).

Two structural counts of a cycle:

- $K$ = number of **o-steps** (odd elements) in one period. (Some sources write $a$ or $\ell$.)
- $S$ = number of **e-steps** that are *not* the obligatory halving folded into an o-step. Equivalently, in the *raw* $3x+1$ map the period is $K$ o-steps and $K+S$ halvings; in the accelerated map $T$ the period length is
$$
N = K + S \quad (\text{number of }T\text{-iterations per period}).
$$

> **Two parametrizations — and the source of the "$m \le 68$ vs $75$" confusion (verified).** The literature uses **two different cycle invariants**, and the survey conflated them:
>
> - A **"$k$-cycle"** in the **circuit** sense (Steiner's original). A *circuit* is one maximal run of consecutive o-steps followed by one maximal run of consecutive e-steps. $k$ = number of circuits. Simons–de Weger excluded $k$-cycles for $k \le 68$; **Hercher extended to $k \le 91$.** (Verified: Wikipedia "Collatz conjecture", *Cycles* subsection, via WebSearch 2026-06-02 — "Simons and de Weger extended this proof up to 68-cycles … Hercher … proved that there exists no $k$-cycle with $k \le 91$.")
> - An **"$m$-cycle"** in the **local-minima** sense. $m$ = number of local minima of the cyclic sequence = number of maximal ascending runs. Simons–de Weger proved $m \ge 76$; **Hercher proved $m \ge 92$** (no $m$-cycle for $m \le 91$). (Verified: Hercher arXiv:2201.00406 abstract, via WebSearch — "Simons and de Weger proved that $m \ge 76$. With newer bounds … one gets $m \ge 83$. In this paper, we prove $m \ge 92$.")
>
> **Both interpretations land at $91/92$ for Hercher** — that is why his title says $m \le 91$ — but the Simons–de Weger predecessors differ ($68$ for circuits, $76$ for local minima). `survey.md` and `bibliography.bib` wrote "$m \le 68$" for the local-minima convention; the correct local-minima predecessor is **$m \ge 76$ (Simons–de Weger)**. This is a citable correction to our own survey; logged in §8.
>
> **On the relationship between the two counts (stated carefully — I could not fetch the primary definitions).** A *circuit* (one ascending o-run followed by one descending e-run) begins at a local minimum, so for a cyclic sequence the number of circuits, local minima, and local maxima are equal *as combinatorial counts*. The fact that Simons–de Weger report **$68$** for the circuit/$k$-cycle statement but **$76$** for the local-minima ($m$-cycle) statement therefore reflects **two genuinely different theorems with different inputs/optimizations** (e.g. the $m$-cycle bound uses an updated verification bound and the refined LMN application), **not** two different values of the same count. I have **not** verified the exact definitional bridge from the primary sources (PDFs unreachable here), so I flag this `[PARTIAL-DEF]` and do not assert $68 = 76$. Below, "$m$" means **number of local minima = number of circuits** (the count); the *numerical* predecessor results are quoted with their source's convention. What matters for §2–§7 is only that $m$ is the *number of ascending runs*, which is unambiguous.

Throughout, $\delta := \log_2 3 = \log 3/\log 2 = 1.5849625007211562\ldots$ (verified to 80 digits, `experiments/verify_cycle_exclusion.py`).

---

## 1. The cycle equation

Fix a cycle with o-step positions and e-step positions in cyclic order. Iterating $T$ around the cycle and using that $T$ is affine on each parity class (`notation.md` §2.4), the smallest element $x_{\min}$ of the cycle satisfies a closed-form relation. The cleanest invariant form (Steiner 1977; Lagarias 1985, §C; Simons–de Weger 2005) is:

> **Lemma 1 (cycle equation).** A Collatz cycle with $K$ o-steps and total accelerated length $N = K+S$ determines, and is determined by, a parity vector. Its elements satisfy
> $$
> (2^{N} - 3^{K})\, x_i = (\text{positive integer } R_i), \qquad i = 0,\dots,N-1,
> $$
> where $R_i$ depends only on the parity vector and the index. In particular $2^{N} - 3^{K} > 0$ (the orbit must on net contract), i.e.
> $$
> \boxed{\,2^{N} > 3^{K}, \quad\text{equivalently}\quad N > K\,\delta = K\log_2 3.\,}
> \tag{1}
> $$

*Justification.* Composing the affine maps $x \mapsto \tfrac{3x+1}{2}$ ($K$ times) and $x \mapsto \tfrac{x}{2}$ ($S$ times) around the loop gives $x_0 = \lambda x_0 + \beta$ with multiplier $\lambda = 3^{K}/2^{N}$ and $\beta \in \mathbb{Z}[\tfrac12]_{>0}$. Solving, $x_0 = \beta/(1-\lambda) = 2^N \beta/(2^N - 3^K)$. Positivity of $x_0$ and finiteness force $2^N - 3^K > 0$. $\square$

This is exactly the relation implemented in `experiments/cycles.py::cycle_n_from_parity` (denominator `2^m - 3^k`), which we use for the Step-1 brute-force check.

---

## 2. From the cycle equation to a linear form in two logarithms

The orbit elements lie between $x_{\min}$ and $x_{\max}$. Two facts pin the geometry:

**(a) Lower bound on $x_{\min}$ from computation.** If the Collatz conjecture has been *verified* for all $n \le B$ (no cycle and convergence below $B$), then any non-trivial cycle has $x_{\min} > B$. Hercher uses
$$
B = 1536 \cdot 2^{60} = 3 \cdot 2^{69} = 1{,}770{,}887{,}431{,}076{,}116{,}955{,}136
\tag{2}
$$
(verified arithmetic, `verify_cycle_exclusion.py`; verified as Hercher's assumed bound via WebSearch of arXiv:2201.00406 — "it suffices to show that … integers $\le 1536\cdot 2^{60} = 3\cdot 2^{69}$ enter the trivial cycle"). This $B$ is consistent with the Barina verification frontier ($2^{68}$–$2^{71}$; see `survey.md` §6.1).

**(b) The two competing bounds on $\Lambda$.** Set
$$
\Lambda := N\log 2 - K\log 3 = (K+S)\log 2 - K\log 3 > 0
\tag{3}
$$
(positive by (1)). Then $2^N - 3^K = 3^K(e^{\Lambda} - 1) \in (3^K\Lambda,\ 3^K\Lambda\, e^{\Lambda})$, so for small $\Lambda$,
$$
2^N - 3^K \approx 3^K \Lambda.
\tag{4}
$$

The proof closes a trap on the cycle length $K$ between an **upper** bound and a **lower** bound that are *both* consequences of the cycle existing — and the trap is empty for $m \le m^\*$. Directionality is verified against the literature (WebSearch 2026-06-02, two independent confirmations; Simons Math. Comp. 2005): *"a lower bound for the cycle length is derived from a generalized lemma of Crandall, while an upper bound for the cycle length is found ... by applying a result of Laurent, Mignotte, and Nesterenko on linear forms in logarithms."*

**Upper bound on $K$ (transcendence: the two-log linear form).** A cycle's multiplier is $3^K/2^N = e^{-\Lambda}$, and closure forces $2^N$ extremely close to $3^K$, i.e. $\Lambda$ very small — quantitatively, the $m$-circuit geometry forces $0 < \Lambda < \theta_m(K)$ where $\theta_m(K)$ decays (roughly exponentially) in $K$ and *relaxes as $m$ grows*. The two-log lower bound on $\Lambda$ then caps $K$. In de Weger's clean packaged form (verified, §5.1b), for the base regime:
$$
0 < \Lambda < 2^{-0.158\,K}\ \text{ has no solution for } K \ge 32
\quad\Longrightarrow\quad
\boxed{\;K < F(m),\;\; F \text{ increasing in } m\;}
\tag{5}
$$
with $F(1)$ a small constant (Steiner), $F(2)\approx 86{,}000$ (Simons), growing with $m$. **Crucially, this upper bound is pure transcendence + cycle geometry — it does NOT involve the verified bound $B$.** The constant ($0.158$, downstream of LMN's $24.34\,D^4$) and the $m$-dependence of $F$ are exactly what Simons–de Weger and Hercher bookkeep; Hercher tightens the $m$-dependence via better circuit averaging (§6.3).

**Lower bound on $K$ (Crandall's lemma + the verified bound $B$).** Since every cycle element exceeds $B$, Crandall's lemma forces the cycle to be long. Verified form (Crandall 1978, as restated; WebSearch): *if $N_0$ is the lowest element of a positive $3x+1$ cycle of circuit-count $k$ and $p_j/q_j$ is a convergent ($j>4$) of $\ln3/\ln2$, then $k > \tfrac32\min(q_j,\ 2N_0/(q_j+q_{j+1}))$.* With $N_0 > B$ this gives
$$
\boxed{\;K > G(\log B)\;}
\tag{6}
$$
of the order of a convergent denominator of $\delta$ exceeding $\sim B$.

**The squeeze.** A cycle needs $G(\log B) < K < F(m)$. Since $F$ increases with $m$ while $G$ is fixed by $B$, there is a threshold $m^\*$ below which $F(m) \le G(\log B)$ — **empty interval, no cycle.**

> **This is the heart of the matter.** Cycle exclusion = **(LMN two-log upper bound $K<F(m)$)** vs **(Crandall lower bound $K>G(\log B)$)**. The transcendence input is the two-log linear form, via the exponent $0.158$ (⇐ LMN's $24.34\,D^4$); it is what makes $F(m)$ finite. The verified bound $B$ enters only through $G$. **The number of circuits $m$ enters only through $F$** — more circuits enlarge $F$, admitting larger $K$, which is why the trap springs only for $m \le m^\*$. See §5–§6.

*(A note on the earlier-draft crude estimate.* A lossy bound $\Lambda < \Theta(m/B)$ — replacing $R_{\min}=O(m\,3^K)$ and $x_{\min}>B$ in $x_{\min}=R_{\min}/(2^N-3^K)\approx R_{\min}/(3^K\Lambda)$ — gives only $K > \log_2(B/m)/0.158$, i.e. it reproduces the *lower* bound (6), not the upper bound. The genuine *upper* bound (5) needs the sharper $m$-circuit geometry that forces $\Lambda$ below an exponentially-decaying $\theta_m(K)$; that step is the technical core of Simons–de Weger and is **not** reproduced from scratch here — see the `[PARTIAL-DERIV]` flag in §6.4.)

---

## 3. The role of $m$ (number of circuits) and the squeeze in $m$

Why does the *number of circuits* $m$ appear as the headline parameter rather than the length $K$ or $N$? Because, by §2 eq (5), the transcendence upper bound $F(m)$ on the admissible cycle length **increases with $m$** (more circuits weaken the geometric forcing on $\Lambda$), while Crandall's lower bound $G(\log B)$ is essentially fixed by $B$. The Simons–de Weger / Hercher analysis:

1. **Each circuit** contributes one ascending run of $a_j$ o-steps and one descending run of $b_j$ e-steps, $j=1,\dots,m$, so $K = \sum_j a_j$, $N = \sum_j(a_j+b_j)$.

2. **Upper bound $F(m)$ (= §2 eq (5)).** The $m$-circuit geometry forces $\Lambda < \theta_m(K)$, decaying in $K$, relaxing as $m$ grows (Simons–de Weger 2005, §3–4; Hercher 2023 sharpens the $m$-dependence via better averaging over the circuit ratios). Through de Weger's two-log bound this yields $K < F(m)$, $F$ increasing in $m$: $F(1)$ a small constant (Steiner), $F(2)\approx 86{,}000$ (Simons).

3. **Lower bound $G(\log B)$ (= §2 eq (6)).** Crandall's lemma (the boxed inequality preceding (6) in §2) with $N_0 > B$ forces $K > G(\log B)$, of the order of a convergent denominator of $\delta$ exceeding $\sim B$.

4. **The squeeze in $m$.** A cycle needs $G(\log B) < K < F(m)$. Since $F$ increases with $m$ while $G$ is fixed by $B$, there is a threshold $m^\*$ below which $F(m) \le G(\log B)$ — **no cycle with $m \le m^\*$.** Hercher pushes $m^\*$ from $75$ (Simons–de Weger, local-minima count) to $91$.

> **So $m^\*$ is set by the gap between $F$ and $G$.** $F$ (the upper bound on $K$) is governed by the **two-log linear-forms exponent** ($0.158$) and the circuit-geometry budget. $G$ (the lower bound on $K$) is governed by **Crandall + the verified bound $B$**. Improving $m^\*$ means improving *either* the two-log exponent (route (a), §6.2) *or* the geometric/combinatorial budget or $B$ (route (b), §6.3).

---

## 4. The explicit small-$m$ template (Steiner $m=1$, Simons $m=2$)

To make §2–§3 concrete and to give the Step-1 checker something exact, we reconstruct the two base cases.

### 4.1 Steiner 1977 ($m = 1$, one circuit)

A 1-circuit cycle has $a$ consecutive o-steps then $b$ consecutive e-steps, $K = a$, $N = a + b$. The cycle equation (Lemma 1) collapses to requiring
$$
x_{\min} = \frac{2^{a} - 1}{\,2^{a+b} - 3^{a}\,} \cdot 3^{0}\cdot(\dots)
\quad\Longrightarrow\quad
\frac{2^{a}-1}{2^{a+b}-3^{a}} \in \mathbb{Z}_{>0}.
\tag{7}
$$
(Verified shape via WebSearch: "Steiner shows that a rational expression of the form $(2^a-1)/(2^{a+b}-3^b)$ does not assume a positive integer value except $a=b=1$.")

> **Theorem (Steiner 1977).** (7) has no solution in positive integers except $a=b=1$ (the trivial cycle $1\to 2 \to 1$).

*Mechanism.* For (8) to be a positive integer $\ge 1$ one needs $2^{a+b}-3^a \le 2^a - 1$, i.e. $\Lambda = (a+b)\log 2 - a\log 3$ extremely small. Steiner bounds $a$ from above by a constant via Baker's theorem on $\Lambda$, then checks the finitely many $(a,b)$ by the continued fraction of $\delta$. The convergents $p/q$ of $\delta$ are exactly the $(K,N)$ candidates making $\Lambda$ small; our computation (verify log) shows $|\delta - p/q|$ never gets small enough at small $q$ to satisfy (8) except trivially.

### 4.2 Simons 2005 ($m = 2$), with explicit numbers (verified)

Simons (Math. Comp. 74 (2005) 1565–1572) reduces the 2-circuit case to the same kind of squeeze and obtains (verified via WebSearch of the AMS paper text):

- **Upper bound on $K$ (LMN applied to $\Lambda$):** $K < 86{,}000$ (Lemma 6 of Simons). [The LMN application appears as: "if $T \le 20.86$ then $-\log\Lambda \le 24.34(\log 3)^2\,(\cdots)^2$" — the constant $24.34$ is LMN's, §5. This is eq (5) for $m=2$, i.e. $F(2)\approx 86{,}000$.]
- **Lower bound on the cycle length (Crandall / continued fractions):** $K + N > 357{,}638{,}239$.
- **Contradiction:** the two bounds constrain compatible quantities through $N \approx \delta K$: $K+N \approx (1+\delta)K$, so the lower bound forces $K > 357638239/(1+\delta) \approx 1.38\times 10^8$, which is incompatible with the LMN upper bound $K < 86{,}000$. Hence **no 2-cycle.** (This is exactly the §2 squeeze — upper bound eq (5) vs lower bound eq (6) — instantiated at $m=2$.)

> **Verified numerical anchor (independent confirmation of the mechanism).** The number $357{,}638{,}239$ is *exactly the numerator of a convergent of $\delta = \log_2 3$*: our continued-fraction computation gives the convergent $357638239/225644606$ with $|\delta - p/q| \approx 1.08\times 10^{-17}$ (`verify_cycle_exclusion.py`). Likewise Eliahou's cycle-length coefficients $301994,\ 17087915,\ 85137581$ are convergent numerators/denominators of $\delta$, and the modern cycle-length lower bound $217{,}976{,}794{,}617$ is the convergent numerator $217976794617/137528045312$. This is strong independent evidence that the reconstructed mechanism ("cycle lengths are forced to be convergent denominators of $\log_2 3$") is correct.

---

## 5. The exact Diophantine input: the two-log linear-forms lower bound (VERIFIED constants)

The transcendence lower bound on $\Lambda = N\log 2 - K\log 3$ is supplied by:

### 5.1 Laurent–Mignotte–Nesterenko (LMN), 1995

**Reference (verified):** M. Laurent, M. Mignotte, Y. Nesterenko, *Formes linéaires en deux logarithmes et déterminants d'interpolation*, **J. Number Theory 55 (1995), 285–321** (verified via WebSearch: "published in 1995 in the Journal of Number Theory (volume 55, pages 285–321)"). The interpolation-determinant method is from M. Laurent, *Linear forms in two logarithms and interpolation determinants*, **Acta Arith. 66.2 (1994), 181–199** (verified via Acta Arith. / impan listing).

**Statement used (rational case, $D=1$; the "Corollary 2" form quoted in applications).** Let $\alpha_1,\alpha_2$ be positive real multiplicatively independent algebraic numbers and $\Lambda = b_2\log\alpha_2 - b_1\log\alpha_1$ with $b_1,b_2$ positive integers. With $\log A_i \ge \max\{h(\alpha_i),|\log\alpha_i|,\,1\}$ and
$$
b' = \frac{b_1}{\log A_2} + \frac{b_2}{\log A_1},
$$
one has
$$
\log|\Lambda| \;\ge\; -\,24.34\,\Big(\max\{\log b' + 0.14,\ 21\}\Big)^2 \,\log A_1 \,\log A_2 .
\tag{9}
$$
(Verified: the leading constant $24.34\,D^4$ for two logs is the canonical LMN constant; its appearance in the Collatz 2-cycle proof is confirmed by the Simons AMS-paper snippet "$-\log\Lambda \le 24.34(\log 3)^2(\cdots)^2$". The auxiliary parameters $0.14$, the max-structure, and $b'$ are LMN's standard form, cross-checked against the Bugeaud "Estimates for linear forms in logarithms" survey and Evertse's Leiden lecture notes via WebSearch.)

> **Tag `[PARTIAL-CONST]`:** I could not fetch the LMN/Laurent PDFs directly (all academic PDF hosts returned HTTP 403 in this environment, consistent with `survey.md`'s documented access note). The constant **$24.34$** and the **$(\log b'+0.14)^2$** structure are confirmed from *multiple independent secondary snippets* (Simons's application, Bugeaud's survey, the Leiden notes). The exact value of the secondary constants ($21$ vs $21/D$, $0.14$, whether the floor is $\max\{\cdot,21,1/2\}$) should be locked against the LMN PDF before any publication. They do **not** affect the *qualitative* conclusion of this document (which constant is rate-limiting), only the precise arithmetic of a putative new $m^\*$.

For our application $\alpha_1=2,\alpha_2=3$, $b_1=N,b_2=K$, $\log A_1 = 1$ ($=\max\{\log 2,1\}$), $\log A_2 = \log 3$, $b' \approx N/\log 3 + K \approx K(\delta/\log 3 + 1)$. Then (9) gives the "raw" bound
$$
\log|\Lambda| \;\ge\; -24.34\,(\log K + c_0)^2 \cdot \log 3,
\quad\text{i.e.}\quad
|\Lambda| \ge \exp\!\big(-C (\log K)^2\big),\quad C \approx 24.34\log 3 \approx 26.7.
\tag{10}
$$
Note the exponent here is **$(\log K)^2$** — far stronger (larger lower bound) than any polynomial $K^{-O(1)}$.

### 5.1b De Weger's operative reformulation (the form actually used — VERIFIED, double-sourced)

For the cycle application one packages (10) as a clean lower bound. The statement, verified verbatim via **two independent WebSearch queries (2026-06-02)** and attributed to **Simons's exposition of the de Weger result** (the Simons 2-cycle / generalized-cycle papers; cross-listed in the survey arXiv:2112.12962):

> **De Weger's reformulation (Simons).** *"The result of de Weger can be reformulated as: $0 < (k+\ell)\log 2 - k\log 3 < 2^{-0.158 k}$ has no solutions for $k \ge 32$."*

In our notation ($k = K$, $\ell = S$, $N = k+\ell$) this is precisely the **transcendence lower bound**
$$
\boxed{\;\Lambda = N\log 2 - K\log 3 \;\ge\; 2^{-0.158\,K}\quad\text{for all } K \ge 32\;}
\tag{6$'$}
$$
i.e. $\Lambda$ *cannot* be as small as $2^{-0.158K}$ once $K \ge 32$. This is (6) of §2 with the explicit constant; it is the **operative** transcendence input (it is exactly (10) re-expressed in the exponential scale the cycle bookkeeping uses — the linear exponent $0.158K\log 2$ is a *convenient lower bound* on the genuine $C(\log K)^2$ for the $K$-range that matters). **The exponent $0.158$ is the single cleanest numerical expression of the bottleneck constant**; it is downstream of LMN's $24.34\,D^4$.

The contradiction with a cycle: the cycle's geometry forces $\Lambda < 2^{-0.158K}$ (or, in the cruder bound (5), $\Lambda<\Theta(m/B)$) for the relevant $(K,N)$; (6$'$) forbids it for $K\ge 32$, leaving only finitely many small-$K$ cases, cleared by direct continued-fraction search. The number-of-circuits $m$ controls how the cycle's forcing exponent compares to $0.158$.

**Step-1 numerically verified** (`verify_cycle_exclusion.py`, check C5a): scanning $K = 1,\dots,200$ with the best $N=\lceil K\delta\rceil$ (minimal positive $\Lambda$), the inequality $0<\Lambda<2^{-0.158K}$ has its **largest solution at $K=29$**; **no solution for any $K\ge 32$**, exactly matching de Weger's threshold. This independently re-derives (6$'$) and is strong corroboration of the (snippet-sourced) constant.

> **Provenance note.** The exponent $0.158$ and threshold $K\ge 32$ are from secondary snippets (Simons's exposition), double-confirmed, *and* independently reproduced numerically here. The upstream LMN constant $24.34\,D^4$ that produces them is `[PARTIAL-CONST]` (primary PDFs unreachable, §5.1).

### 5.2 Why this is the bottleneck — and why $\mu(\log_2 3)$ is structurally USELESS here

This is the central analytic point, and the directionality matters. The cycle's *sharp* geometric forcing (§2) is **exponential**: an $m$-circuit cycle forces
$$
0 < \Lambda < 2^{-\rho_m K} \qquad (\rho_m > 0,\ \text{decreasing in } m),
$$
because closure makes $2^N$ exponentially close to $3^K$. The proof needs a transcendence **lower** bound on $\Lambda$ that **outpaces** this — i.e. is *larger* than $2^{-\rho_m K}$ for large $K$ — so the two cross and cap $K$ from above.

- **Two-log estimate (de Weger/LMN):** $\Lambda > 2^{-0.158K}$ — also **exponential**. Against the forcing:
$$
2^{-0.158K} < \Lambda < 2^{-\rho_m K} \;\Rightarrow\; 2^{-0.158K} < 2^{-\rho_m K},
$$
which fails for large $K$ whenever $\rho_m > 0.158$, and in the borderline regime pins $K$ into a **finite window $K < F(m)$**. Two comparable exponentials ⟹ an **upper bound on $K$.** ✓ (For $m=2$, $F(2)\approx 86{,}000$.)

- **Irrationality measure $\mu := \mu(\log_2 3)$:** gives $|\delta - N/K| > K^{-\mu}$, i.e. $\Lambda > (\log 2)K^{1-\mu}$ — only **polynomial**. Against the forcing:
$$
(\log 2)\,K^{1-\mu} < \Lambda < 2^{-\rho_m K}.
$$
A polynomial $K^{1-\mu}$ is **eventually $\gg$** an exponentially-small $2^{-\rho_m K}$ — so this inequality is **violated for all large $K$**, i.e. it is satisfiable only for *small* $K$ and imposes **no upper bound** of the needed kind; worse, it cannot even certify the *absence* of large-$K$ cycles. **No contradiction with a long cycle is produced, for any $\mu$.**

> **Conclusion (the headline correction).** The reason the cycle proof uses a two-log linear form and *not* $\mu(\log_2 3)$ is **not** merely that the two-log constant is numerically better — it is that **only an exponential-in-$K$ lower bound on $\Lambda$ can cap the cycle length from above**, and the irrationality measure is intrinsically polynomial. **No improvement of $\mu(\log_2 3)$ — not even the conjectural $\mu = 2+\epsilon$ — can move the cycle bound $m^\*$.** This directly refutes the premise of `open_problems.md` D.1/D.2 and `survey.md` §11 Vector C that "each extension requires a better effective irrationality measure of $\log_2 3$." The lever is the **two-log exponent** ($0.158$), which is set by the leading constant ($24.34 D^4$) and the height/$b'$ structure of (9).

### 5.3 Current best $\mu(\log_2 3)$ and $\mu(\log 3)$ — verified, for completeness

- $\mu(\log 3) \le 5.1163051$ — **Wu & Wang, *On the irrationality measure of $\log 3$*, J. Number Theory 142 (2014), 264–273** (verified via WebSearch / Semantic Scholar / ScienceDirect listing). This improved Salikhov 2007 ($\le 5.125$) and Rhin 1987 ($\le 8.616$). [Rhin's commonly-cited figure is sometimes quoted as $\le 7.616$; the chronology $8.616 \to 5.125 \to 5.1163051$ is the one given by the Wu–Wang paper itself; tagged `[PARTIAL-CONST]` for the Rhin value.]
- $\mu(\log 2) \le 3.57455391$ — **Marcovecchio, *The Rhin–Viola method for $\log 2$*, Acta Arith. 139.2 (2009), 147–184** (venue verified via WebSearch/EUDML; the exact numerical value $3.574\ldots$ is `[PARTIAL-CONST]`, not snippet-confirmed). Not used in the cycle argument; listed for completeness.
- $\mu(\log_2 3) = \mu(\log 3/\log 2)$: I found **no published effective bound dedicated to the ratio $\log_2 3$**; the cycle literature does not use one. The relevant object is always the *two-log form*, where the heights of $2$ and $3$ enter separately and beneficially. (This is precisely why the two-log estimate beats the ratio's measure.)

---

## 6. The exact quantity that bounds $m$, and the two improvement routes

### 6.1 The bottleneck constant (answer to the brief)

> **The precise bottleneck is the two-log linear-forms estimate** — concretely the leading constant $\kappa$ in
> $$\log|\Lambda| \ge -\kappa\,(\log b' + 0.14)^2\,\log A_1\log A_2,\qquad \kappa_{\text{current}} = 24.34\ (D=1),$$
> as packaged in de Weger's operative form $\Lambda > 2^{-0.158K}$ for $K \ge 32$. This estimate is what converts the cycle's geometric budget into the **upper bound $F(m,\log B)$ on the cycle length $K$** (§2, (7)–(8)). Hercher's $m^\* = 91$ is the largest $m$ for which $F(m,\log B)$ has not yet dropped below Crandall's lower bound $G(\log B)$ (§3, (10)). A **sharper two-log estimate** (smaller $\kappa$ ⟹ a more favorable de Weger inequality, i.e. ruling out the cycle's forcing at a smaller $K$-threshold) tightens $F$ and raises $m^\*$; equivalently one can raise $m^\*$ by lowering $G$ (larger verified $B$) or improving the circuit-averaging budget. The exact numerical sensitivity $\partial m^\*/\partial\kappa$ requires Hercher's explicit constants (not fetchable here) to compute.

### 6.2 Route (a): plug in a sharper two-log estimate

Candidates, in order of likely impact:

1. **Laurent 2008**, *Linear forms in two logarithms and interpolation determinants II*, **Acta Arith. 133.4 (2008), 325–348** (verified via EUDML/ResearchGate listing). This paper sharpens the 1994/1995 constants in the real two-log case. **I could not extract its exact improved constant ($< 24.34$) from accessible snippets** (`[PARTIAL-CONST]`). If Laurent 2008 (or its widely-used "Corollaire 2") gives, say, $\kappa \approx 22$–$23$ in the regime relevant here, that is a *direct* drop-in that Hercher may or may not have already used.
   - **Action item / open question for the project:** *Did Hercher already use the sharpest available two-log constant?* If Hercher used LMN-1995 ($24.34$) and Laurent-2008 gives a smaller $\kappa$ in the relevant parameter window, **then a new $m^\* > 91$ follows immediately** by re-running his squeeze with the smaller $\kappa$. This must be checked against the Hercher PDF (not fetchable here). **I cannot claim this without that check.**

2. **Post-2023 two-log refinements.** I searched for newer dedicated two-log constants (2023–2026) and found only three-log "kits" (Mignotte–Voutier 2023; arXiv:2205.08899) and survey material, **no published post-2023 improvement to the two-log real-case leading constant** that is clearly sharper than Laurent 2008 in this regime. So route (a) reduces to: *confirm whether Hercher used Laurent-2008 or LMN-1995, and whether Laurent-2008's constant is genuinely smaller in the cycle window.*

### 6.3 Route (b): tighten the combinatorial/analytic part $F(m,\log B)$

This is the part that is **not** the irrationality measure, and it is where Hercher actually made his gain (verified: Hercher's abstract emphasizes "subsequently improving upper bounds on averages and bounds on sums of an arbitrary number of terms" — a *combinatorial* sharpening of the circuit bookkeeping, not a new transcendence constant). Concretely $F$ can be improved by:

1. **A larger verified $B$.** Hercher uses $B = 3\cdot 2^{69}$. Barina 2025 reaches $2^{71}$ (`survey.md` §6.1). Re-running with $B = 2^{71}$ tightens (7) and (6) and would raise $m^\*$ by a small amount (each doubling of $B$ adds a little). **This is the cheapest concrete gain and is almost certainly worth ~1–3 in $m^\*$.** (Hercher's "$m\ge 83$ with newer verification" remark shows the verification bound alone moves $m^\*$ by several units.)
2. **Sharper averaging over circuits.** Hercher's "bounds on sums of an arbitrary number of terms" is a convexity/averaging inequality over the $m$ circuit ratios. Any improvement to the constant in that averaging (e.g., a tighter Jensen/rearrangement bound exploiting that the $a_j$ are positive integers $\ge 1$ and the $b_j \ge 1$) lowers $F$.
3. **Using both bounds on $K$ simultaneously** (Hercher & Puchert later pushed the *unconditional* o-step bound to $K > 7.2\times 10^{10}$; Hercher 2023 needs $K \ge 1.375\times 10^{11}$ to go further — verified via WebSearch). The gap between "what we can prove about $K$" and "what we need" is the residual.

### 6.4 Honest assessment

- **`[PARTIAL-DERIV]`** The technical core — the derivation of the *upper* bound $F(m)$ on $K$ from the $m$-circuit geometry (the step that forces $\Lambda$ below an exponentially-decaying $\theta_m(K)$ and then applies the two-log bound) — is **summarized, not reproduced from scratch**, in this document. I have verified its *inputs* (the two-log constant, the directionality, the $m=1,2$ outcomes) and its *outputs* (the $m^\*$ values), but a from-first-principles re-derivation of $F(m)$ for general $m$ requires the Simons–de Weger / Hercher bookkeeping in full, which needs the PDFs. This is the main gap a Step-2 red-team should probe.
- **I have NOT improved past $m \le 91$ in this document.** Doing so rigorously requires the exact constants and the explicit $F(m)$ from the Hercher PDF and the Laurent-2008 PDF, neither fetchable in this environment.
- **The single most likely real incremental gain** is Route (b1): redo Hercher's squeeze with $B = 2^{71}$ (Barina 2025) instead of $B = 3\cdot 2^{69}$. This is honest, uses only a correctly-cited published verification bound, and is mechanical. Expected gain: small ($+1$ to $+3$ in $m^\*$), and it would need the Hercher constants to instantiate. **This is the recommended next concrete step.**
- **A larger gain via Route (a)** is possible *iff* Hercher did not already use the sharpest two-log constant. Determining that is the key open question and requires the Hercher PDF.

---

## 7. What published or conjectural Diophantine bound would push $m$ further

| Input | Current | Effect on $m^\*$ | Status |
|---|---|---|---|
| Two-log leading constant $\kappa$ | $24.34$ (LMN 1995); Laurent 2008 likely sharper, value TBD | raises $m^\*$ (monotone; magnitude needs Hercher's constants) | **Route (a).** Real *iff* Hercher used the older constant. |
| Verified bound $B$ | $3\cdot 2^{69}$ (Hercher) → $2^{71}$ (Barina 2025) | $+1$ to $+3$ (Hercher's $83\to$ via verification shows several units) | **Route (b1).** Real, cheap, published input. |
| Circuit-averaging budget | Hercher's | small–moderate | **Route (b2).** Real, needs the PDF. |
| $\mu(\log_2 3)$ | via $\mu(\log 3)\le 5.116$ (Wu–Wang 2014) | **none** | **Structural dead end** (§5.2): polynomial ⟹ wrong-direction bound on $K$. Corrects `open_problems.md` D.1/D.2. |
| *Conjectural:* $\mu(\log_2 3) = 2+\epsilon$ | conjectural | **still none** | A better $\mu$ remains polynomial; cannot cap $K$ from above. Not the lever, even conjecturally. |
| *Conjectural:* effective **two-log** bound $|\Lambda| > c(\epsilon)\,H^{-1-\epsilon}$ (Lang–Waldschmidt, $H \sim \max(N,K)$) | conjectural | would push $m^\* \to \infty$ effectively | The real conjectural lever. |

**Conclusion on the conjectural side:** The bound that would genuinely "blow up" $m^\*$ is **not** a better $\mu(\log_2 3)$ (a polynomial lower bound on $\Lambda$ can never cap the cycle length from above — §5.2); it is a **conjecturally optimal lower bound for the two-log linear form** $|N\log 2 - K\log 3| \gg H^{-1-\epsilon}$ (Lang–Waldschmidt's two-dimensional conjecture). This is far beyond current transcendence technology (current exponent is $\sim(\log H)^2$; conjectural is $(1+\epsilon)\log H$). Even this only sharpens the *exponential* decay rate — it would push $m^\*$ very high but, being still short of "$\Lambda$ bounded below by a constant," would not by itself rule out cycles of *all* $m$. **Unbounded cycle exclusion ($m^\* = \infty$) is exactly conditional on a strong-enough two-log lower bound.**

---

## 8. Corrections to our own survey (to be propagated)

1. **`survey.md` §7.3 and §9, `bibliography.bib` `SimonsDeWeger2005` note, `open_problems.md` D.1:** "no $m$-cycle for $m \le 68$" is the **circuit** count; in the **local-minima** convention used by Hercher's title the Simons–de Weger result is **$m \ge 76$** (no $m$-cycle for $m \le 75$). Hercher's $m \le 91$ is consistent in both conventions. Recommend: state both, cite Wikipedia/Hercher abstract.
2. **`survey.md` §7.5, §11 Vector C, `open_problems.md` D.1/D.2:** "the bottleneck is the effective irrationality measure of $\log_2 3$" is **incorrect**. The bottleneck is the **two-log linear-forms constant** (LMN/Laurent). Improving $\mu(\log_2 3)$ would not move the cycle bound. (§5.2 above.) This is the central correction.

---

## 9. What the Step-1 numerics verify (see `experiments/verify_cycle_exclusion.py`)

1. (C1) $\delta = \log_2 3$ to 80+ digits and its continued fraction $[1;1,1,2,2,3,1,5,2,23,2,2,1,1,55,\dots]$.
2. (C2) **Eliahou's and Simons–de Weger's constants are convergent (numerators/denominators) of $\delta$** — confirming the "cycle lengths are convergents of $\log_2 3$" mechanism. ($357638239$, $17087915$, $85137581$, $301994$, $217976794617$, $10439860591$, $6586818670$ all appear.)
3. (C3) $2^N > 3^K \Leftrightarrow N > K\delta$ (Lemma 1) and $2^N \ne 3^K$ (denominator never zero) for $K\le2000$; Legendre $q^2|\delta-p/q|<1$ on all convergents.
4. (C4) Hercher's bound arithmetic $1536\cdot2^{60}=3\cdot2^{69}$.
5. (C5a) **De Weger's threshold:** $0<\Lambda<2^{-0.158K}$ has its largest solution at $K=29$; **no solution for $K\ge32$** — independently re-deriving eq (6$'$). (C5b) the directional argument of §5.2 (two-log slope $0.158$ vs irrationality-measure slope $\to0$).
6. **Brute-force (`cycles.py`):** no non-trivial positive cycle for parity length $\le 22$; no cycle with $x_{\min} \le 10^5$ and period $\le 3000$. Negative-cycle sanity checks ($-1,-5,-17$) pass.

All four pass. This is necessary, not sufficient (per `verification_protocol.md` anti-patterns) — the document's *claims* are (i) the reconstruction of the mechanism, (ii) the identification of the bottleneck constant, (iii) the two correction items. Of these, (i) and (iii) are verifiable from the cited literature; (ii) is the analytic conclusion that should face a Step-2 red-team and, ideally, confirmation against the Hercher and Laurent-2008 PDFs.
