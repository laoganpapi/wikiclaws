# Explicit Reconstruction of the Steiner–Simons–de Weger–Hercher Cycle-Exclusion Argument

**Track:** collatz — Vector C (cycle exclusion via Diophantine approximation)
**Author:** Alex Ye (AI assistance disclosed separately)
**Status:** `[unverified]` — Step-1 numerical checks passed (see `experiments/verify_cycle_exclusion_log.md`); Steps 2–4 pending.
**Date:** 2026-06-02

> **Purpose.** Reconstruct, with every step justified, the Diophantine argument that excludes non-trivial Collatz $m$-cycles, identify the *exact* quantity that bounds $m$, web-verify every numerical constant, and determine precisely what Diophantine input would be needed to push past Hercher's $m \le 91$.
>
> **Headline finding (stated up front so it is not buried).** The rate-limiting Diophantine input is **NOT the one-dimensional irrationality measure $\mu(\log_2 3)$**, contrary to the framing in `survey.md` §7.5 and `open_problems.md` D.2. It is a **lower bound for a linear form in *two* logarithms**, $\Lambda = K\log 3 - (K+S)\log 2$, supplied by the **Laurent–Mignotte–Nesterenko (LMN)** theorem / Laurent's interpolation-determinant method. This bound is already *much stronger* than anything $\mu(\log_2 3)$ provides, so improving $\mu(\log_2 3)$ would **not** move the cycle bound. The relevant constant to improve is the **leading constant in the two-log linear-forms estimate** (currently $24.34\,D^4$ in LMN's rational case, refinable via Laurent 2008 / subsequent work). This correction is developed in §6 and is the single most important deliverable of this document.

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
> For a circuit / 1-circuit cycle the number of circuits, local minima, and local maxima all coincide. In general, **#circuits = #local minima = #local maxima = $m$** for a cyclic sequence, so the *combinatorial* meaning is the same; the discrepancy $68$ vs $76$ is because Simons–de Weger optimized the two cases with slightly different inputs, not because the definitions differ. We standardize on **$m$ = number of local minima = number of circuits** below and note where it matters.

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

**(b) The "$2^N \approx 3^K$" squeeze.** From (1), $2^N - 3^K > 0$. The cycle equation forces $2^N - 3^K$ to **divide** the bounded quantity $R_i$, and bounding $R_i \le (\text{const}) \cdot x_{\max} \cdot 2^N$-type estimates against $x_{\min} > B$ shows $2^N - 3^K$ cannot be too large relative to $3^K$. Writing
$$
\Lambda := N\log 2 - K\log 3 = (K+S)\log 2 - K\log 3 > 0,
\tag{3}
$$
we have $2^N - 3^K = 3^K(e^{\Lambda} - 1) \in (3^K\Lambda,\ 3^K\Lambda\, e^{\Lambda})$, so for small $\Lambda$,
$$
2^N - 3^K \approx 3^K \Lambda.
\tag{4}
$$

The cycle constraints (elements are integers $> B$, $\le$ a geometric bound in $N$) translate, after the Simons–de Weger bookkeeping over the $m$ circuits, into an **upper bound** of the shape
$$
\Lambda \;<\; \frac{C_{\mathrm{geom}}(m)}{2^{N}}\cdot(\text{poly factors}), \qquad\text{equivalently}\qquad
0 < \Lambda < e^{-c N}\ \text{for an explicit } c>0.
\tag{5}
$$
The precise form (Simons–de Weger 2005, Lemma; Hercher 2023) is what we reconstruct in §3–§4. The key qualitative point: **$\Lambda$ is forced to be exponentially small in $N$.**

On the other hand, $\Lambda = N\log 2 - K\log 3$ is a **non-zero linear form in the two logarithms $\log 2, \log 3$ with integer coefficients $N, -K$.** Transcendence theory gives a **lower bound** $\Lambda > e^{-c' \log N \cdot (\cdots)}$ that decays only *polynomially-in-exponent*, i.e. like $N^{-O(1)}$ up to the height terms. The clash between the exponential upper bound (5) and the much larger transcendence lower bound is the contradiction that excludes cycles — **once $N$ (hence $m$) is large enough.** For small $m$ the two bounds do not yet clash, and those finitely many cases are cleared by direct continued-fraction / computer search.

> **This is the heart of the matter.** Cycle exclusion = (exponentially small upper bound on $\Lambda$ from the cycle's integrality) vs. (transcendence lower bound on $\Lambda$). The transcendence lower bound is the **two-log linear form** estimate. See §5–§6.

---

## 3. The role of $m$ (number of circuits): bounding $N$ in terms of $m$

Why does the *number of circuits* $m$ (not the length $N$) appear as the headline parameter? Because the analytic upper bound (5) on $\Lambda$ degrades as the cycle is allowed more circuits, while the transcendence lower bound depends on $N$ through $\log N$. The Simons–de Weger / Hercher analysis proceeds:

1. **Each circuit** contributes one ascending run of $a_j$ o-steps and one descending run of $b_j$ e-steps, $j = 1,\dots,m$. So
$$
K = \sum_{j=1}^m a_j, \qquad N = \sum_{j=1}^m (a_j + b_j).
$$

2. **Per-circuit Diophantine inequality.** Steiner's 1-circuit identity generalizes: for the cycle to close with all elements $> B$, the *multiset* of circuit ratios $2^{a_j+b_j}/3^{a_j}$ must multiply to $2^N/3^K = e^{\Lambda}$ close to $1$, and each factor is bounded. This yields (Simons–de Weger 2005, §3–4) an **upper bound on $K$ (and hence $N$) that is polynomial in $m$ and in $\log B$**:
$$
K \;<\; F(m, \log B)
\tag{6}
$$
for an explicit increasing function $F$. Concretely for $m = 1$ (Steiner) $K$ is bounded by a small constant; the bound grows roughly linearly in $m$ for the leading behavior, with the precise constants determined by the LLL-reduced continued-fraction data of $\delta = \log_2 3$.

3. **Transcendence lower bound forces $K$ large.** The two-log lower bound on $\Lambda$ (§5), fed back through (4)–(5), forces
$$
K \;>\; G(\log B)
\tag{7}
$$
*independent of $m$* (it depends on how small $\Lambda$ can be, which is governed by the height of the form, i.e. by $\log N \approx \log K$).

4. **The squeeze.** Combine (6) and (7). For the would-be cycle to exist we need $G(\log B) < K < F(m,\log B)$. Since $F$ increases with $m$, there is a threshold $m^\*$ below which $F(m,\log B) \le G(\log B)$, making the interval empty: **no cycle with $m \le m^\*$.** Hercher's contribution is to push $m^\* $ from $75$ (Simons–de Weger, local-minima count) to $91$.

> **So the bound on $m$ is set by the gap between $F$ and $G$.** $G$ comes from the **two-log linear-forms lower bound** (the transcendence input). $F$ comes from the **combinatorial geometry of the circuits + the verification bound $B$**. Improving $m^\*$ requires improving *either* $G$ (sharper two-log estimate, route (a)) *or* $F$ (sharper combinatorics / larger $B$, route (b)). §6–§7.

---

## 4. The explicit small-$m$ template (Steiner $m=1$, Simons $m=2$)

To make §2–§3 concrete and to give the Step-1 checker something exact, we reconstruct the two base cases.

### 4.1 Steiner 1977 ($m = 1$, one circuit)

A 1-circuit cycle has $a$ consecutive o-steps then $b$ consecutive e-steps, $K = a$, $N = a + b$. The cycle equation (Lemma 1) collapses to requiring
$$
x_{\min} = \frac{2^{a} - 1}{\,2^{a+b} - 3^{a}\,} \cdot 3^{0}\cdot(\dots)
\quad\Longrightarrow\quad
\frac{2^{a}-1}{2^{a+b}-3^{a}} \in \mathbb{Z}_{>0}.
\tag{8}
$$
(Verified shape via WebSearch: "Steiner shows that a rational expression of the form $(2^a-1)/(2^{a+b}-3^b)$ does not assume a positive integer value except $a=b=1$.")

> **Theorem (Steiner 1977).** (8) has no solution in positive integers except $a=b=1$ (the trivial cycle $1\to 2 \to 1$).

*Mechanism.* For (8) to be a positive integer $\ge 1$ one needs $2^{a+b}-3^a \le 2^a - 1$, i.e. $\Lambda = (a+b)\log 2 - a\log 3$ extremely small. Steiner bounds $a$ from above by a constant via Baker's theorem on $\Lambda$, then checks the finitely many $(a,b)$ by the continued fraction of $\delta$. The convergents $p/q$ of $\delta$ are exactly the $(K,N)$ candidates making $\Lambda$ small; our computation (verify log) shows $|\delta - p/q|$ never gets small enough at small $q$ to satisfy (8) except trivially.

### 4.2 Simons 2005 ($m = 2$), with explicit numbers (verified)

Simons (Math. Comp. 74 (2005) 1565–1572) reduces the 2-circuit case to the same kind of squeeze and obtains (verified via WebSearch of the AMS paper text):

- **Upper bound (LMN applied to $\Lambda$):** $K < 86{,}000$ (Lemma 6 of Simons). [The LMN application appears as: "if $T \le 20.86$ then $-\log\Lambda \le 24.34(\log 3)^2\,(\cdots)^2$" — the constant $24.34$ is LMN's, §5.]
- **Lower bound (continued fractions / integrality):** the cycle length satisfies $K + N > 357{,}638{,}239$.
- **Contradiction:** $86{,}000 < 357{,}638{,}239$ — wait, these are bounds on *different* quantities ($K$ vs $K+N$); the actual contradiction is that the small set of $(K,N)$ with $\Lambda$ small enough (forced by $K+N$ being a large convergent denominator) all have $K$ exceeding the upper bound, leaving no admissible pair. Hence **no 2-cycle.**

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

For our application: $\alpha_1 = 2,\alpha_2 = 3$, $h(2)=\log 2,h(3)=\log 3$, so $\log A_1 = \log 2$-ish $\to$ take $\log A_1 = 1$ (since $\max\{\log 2,1\}=1$), $\log A_2 = \log 3 = 1.0986\ldots$; $b_1 = N, b_2 = K$, $b' \approx N/\log 3 + K \approx K(\delta/\log 3 + 1)$. Then (9) gives
$$
\log|\Lambda| \ge -24.34\,(\log K + c_0)^2 \cdot \log 3,
\quad\text{i.e.}\quad
|\Lambda| \ge \exp\!\big(-C (\log K)^2\big)
\tag{10}
$$
for an explicit $C \approx 24.34\log 3 \approx 26.7$ (plus lower-order terms). **This is $G$ of §3:** $\Lambda$ cannot be smaller than $\approx e^{-26.7(\log K)^2}$.

### 5.2 Why this is the bottleneck — and why $\mu(\log_2 3)$ is NOT

The cycle's integrality forces (5): $\Lambda < e^{-cN} = e^{-c\delta K}$ roughly (since $N \approx \delta K$). Setting the **exponential** upper bound against the **quasi-polynomial** lower bound (10):
$$
e^{-c\delta K} \;<\; |\Lambda| \;\text{ is impossible once }\; c\delta K \;>\; 24.34\log 3\,(\log K)^2,
$$
i.e. once $K \gtrsim (\log K)^2$ with the explicit constants — which happens for all $K$ above a moderate threshold. The *value* of that threshold, propagated back through the circuit bookkeeping (6), is exactly what determines $m^\*$. **A smaller leading constant in (9) lowers the threshold on $K$, hence raises $m^\*$.**

By contrast, the one-dimensional irrationality measure $\mu(\log_2 3)$ controls $|N - K\delta| = |\Lambda|/\log 2$ only through $|\delta - N/K| > K^{-\mu}$, i.e. $|\Lambda| > (\log 2)\,K^{1-\mu}$. With the **current best $\mu(\log_2 3)$ (see §5.3)** this is *far weaker* than (10) for the relevant range: a polynomial-in-$K$ lower bound with exponent $\sim -3$ to $-5$, versus LMN's $e^{-C(\log K)^2}$ which is *larger* (closer to $1$) for all moderately large $K$. **Hence the cycle proof uses LMN, not $\mu$, and improving $\mu(\log_2 3)$ does not help.** (This directly corrects `open_problems.md` D.2's premise that "each extension requires a better effective irrationality measure of $\log_2 3$.")

### 5.3 Current best $\mu(\log_2 3)$ and $\mu(\log 3)$ — verified, for completeness

- $\mu(\log 3) \le 5.1163051$ — **Wu & Wang, *On the irrationality measure of $\log 3$*, J. Number Theory 142 (2014), 264–273** (verified via WebSearch / Semantic Scholar / ScienceDirect listing). This improved Salikhov 2007 ($\le 5.125$) and Rhin 1987 ($\le 8.616$). [Rhin's commonly-cited figure is sometimes quoted as $\le 7.616$; the chronology $8.616 \to 5.125 \to 5.1163051$ is the one given by the Wu–Wang paper itself; tagged `[PARTIAL-CONST]` for the Rhin value.]
- $\mu(\log 2) \le 3.57455391$ (Marcovecchio 2009, via the Rhin–Viola method) — verified via WebSearch.
- $\mu(\log_2 3) = \mu(\log 3/\log 2)$: I found **no published effective bound dedicated to the ratio $\log_2 3$**; the cycle literature does not use one. The relevant object is always the *two-log form*, where the heights of $2$ and $3$ enter separately and beneficially. (This is precisely why the two-log estimate beats the ratio's measure.)

---

## 6. The exact quantity that bounds $m$, and the two improvement routes

### 6.1 The bottleneck constant (answer to the brief)

> **The precise bottleneck is the leading constant $\kappa$ in the two-log lower bound**
> $$\log|\Lambda| \ge -\kappa\,(\log b' + 0.14)^2\,\log A_1\log A_2,\qquad \kappa_{\text{current}} = 24.34\ (D=1).$$
> Equivalently, the bottleneck is the function $G(\log B)$ of §3 (the smallest $K$ for which (10) beats the cycle's exponential upper bound), and $G$ scales like $\kappa\,(\log K)^2$. Hercher's $m^\* = 91$ is the largest $m$ for which the combinatorial bound $F(m,\log B)$ does not yet exceed $G$.

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

- **I have NOT improved past $m \le 91$ in this document.** Doing so rigorously requires the exact constants from the Hercher PDF and the Laurent-2008 PDF, neither fetchable in this environment.
- **The single most likely real incremental gain** is Route (b1): redo Hercher's squeeze with $B = 2^{71}$ (Barina 2025) instead of $B = 3\cdot 2^{69}$. This is honest, uses only a correctly-cited published verification bound, and is mechanical. Expected gain: small ($+1$ to $+3$ in $m^\*$), and it would need the Hercher constants to instantiate. **This is the recommended next concrete step.**
- **A larger gain via Route (a)** is possible *iff* Hercher did not already use the sharpest two-log constant. Determining that is the key open question and requires the Hercher PDF.

---

## 7. What published or conjectural Diophantine bound would push $m$ further

| Input | Current | Effect on $m^\*$ | Status |
|---|---|---|---|
| Two-log leading constant $\kappa$ | $24.34$ (LMN 1995) / Laurent 2008 (sharper, value TBD) | $m^\*$ scales like $1/\sqrt\kappa$-ish via the $(\log K)^2$ balance | **Route (a).** Real if Hercher used the older constant. |
| Verified bound $B$ | $3\cdot 2^{69}$ (Hercher) → $2^{71}$ (Barina 2025) | $+1$ to $+3$ | **Route (b1).** Real, cheap, published input. |
| Circuit-averaging constant | Hercher's | small | **Route (b2).** Real, needs the PDF. |
| $\mu(\log_2 3)$ | $\approx$ via $\mu(\log 3)\le 5.116$ | **none** | **Dead end for cycles** (see §5.2). Corrects `open_problems.md` D.2. |
| *Conjectural:* $\mu(\log_2 3) = 2+\epsilon$ (Lang–Waldschmidt type) | conjectural | would make the *one-log* bound competitive but still not beat the two-log estimate in this regime | Not the lever. |
| *Conjectural:* an effective **two-log** bound of true "$abc$/Lang–Waldschmidt" strength $|\Lambda| > c(\epsilon)\,H^{-1-\epsilon}$ | conjectural | would push $m^\* \to \infty$ effectively (rule out *all* circuit cycles for $m$ up to enormous bounds) | The real conjectural lever. |

**Conclusion on the conjectural side:** The bound that would genuinely "blow up" $m^\*$ is **not** a better $\mu(\log_2 3)$; it is a **conjecturally optimal lower bound for the two-log linear form** $|N\log 2 - K\log 3|$ of the form $\gg H^{-1-\epsilon}$ (where $H \sim \max(N,K)$), i.e. the two-dimensional analogue of the Lang–Waldschmidt conjecture. Such a bound is far beyond current transcendence technology (current is $(\log H)^2$ in the exponent, conjectural is $(1+\epsilon)\log H$). This is the precise Diophantine statement on which unbounded cycle exclusion is conditional.

---

## 8. Corrections to our own survey (to be propagated)

1. **`survey.md` §7.3 and §9, `bibliography.bib` `SimonsDeWeger2005` note, `open_problems.md` D.1:** "no $m$-cycle for $m \le 68$" is the **circuit** count; in the **local-minima** convention used by Hercher's title the Simons–de Weger result is **$m \ge 76$** (no $m$-cycle for $m \le 75$). Hercher's $m \le 91$ is consistent in both conventions. Recommend: state both, cite Wikipedia/Hercher abstract.
2. **`survey.md` §7.5, §11 Vector C, `open_problems.md` D.1/D.2:** "the bottleneck is the effective irrationality measure of $\log_2 3$" is **incorrect**. The bottleneck is the **two-log linear-forms constant** (LMN/Laurent). Improving $\mu(\log_2 3)$ would not move the cycle bound. (§5.2 above.) This is the central correction.

---

## 9. What the Step-1 numerics verify (see `experiments/verify_cycle_exclusion.py`)

1. $\delta = \log_2 3$ to 80 digits and its continued fraction $[1;1,1,2,2,3,1,5,2,23,2,2,1,1,55,\dots]$.
2. **Eliahou's and Simons–de Weger's constants are convergent (numerators/denominators) of $\delta$** — confirming the mechanism. ($357638239$, $17087915$, $85137581$, $301994$, $217976794617$ all appear.)
3. The inequality $2^N > 3^K \Leftrightarrow N > K\delta$ (Lemma 1) holds exactly for all the relevant $(K,N)$, and the per-convergent $|\delta - p/q|$ is never small enough at small $q$ to admit a non-trivial cycle (consistent with Steiner $m=1$).
4. **Brute-force (`cycles.py`):** no non-trivial positive cycle for parity length $\le 22$; no cycle with $x_{\min} \le 2\times 10^5$ and period $\le 5000$. Negative-cycle sanity checks ($-1,-5,-17$) pass.

All four pass. This is necessary, not sufficient (per `verification_protocol.md` anti-patterns) — the document's *claims* are (i) the reconstruction of the mechanism, (ii) the identification of the bottleneck constant, (iii) the two correction items. Of these, (i) and (iii) are verifiable from the cited literature; (ii) is the analytic conclusion that should face a Step-2 red-team and, ideally, confirmation against the Hercher and Laurent-2008 PDFs.
