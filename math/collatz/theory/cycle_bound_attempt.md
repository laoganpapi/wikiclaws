# From-Scratch Cycle-Length Derivation and the $B = 2^{71}$ Squeeze for Collatz $m$-Cycles

**Track:** collatz — Vector C (cycle exclusion via Diophantine approximation)
**Author:** Alex Ye (AI assistance disclosed separately)
**Status:** `[unverified]` — Step-1 numerics pass (`experiments/verify_cycle_bound.py`, `cycles.py`);
the rigorous core (§2–§4) is self-contained and computer-checked; the $m^\*$ bookkeeping (§6) is
**`[PROVISIONAL]`** and **`[UNVERIFIED — needs check vs Hercher 2023 primary source]`**.
**Date:** 2026-06-02
**Companion:** `cycle_exclusion_explicit.md` (the earlier reconstruction; this note **completes** its
`[PARTIAL-DERIV]` gap as far as is possible without Hercher's PDF, and is explicit about what remains).

---

## 0. Purpose and honest framing (read first)

The earlier note `cycle_exclusion_explicit.md` reconstructed the *inputs* to the
Steiner–Simons–de Weger–Hercher cycle-exclusion argument (the two-log linear-forms estimate, de
Weger's $2^{-0.158K}$ packaging, the Crandall lower bound, the verified bound $B$) but left the
**cycle-length function itself** as a black box flagged `[PARTIAL-DERIV]`. This note re-derives the
machinery **from scratch**:

1. **§1–§2 (rigorous, self-contained, computer-checked).** I derive the cycle equation and a *new*,
   exact telescoping identity
   $$
   \Lambda \;=\; N\log 2 - K\log 3 \;=\; \sum_{j=1}^{m}\varepsilon_j,\qquad
   \varepsilon_j=\log\!\Big(1+\tfrac{1-(2/3)^{a_j}}{x_j}\Big),
   $$
   from which the **rigorous bound $0<\Lambda<m/B$** follows for any nontrivial positive $m$-cycle.
   Every step is justified and numerically verified to $\sim 10^{-100}$.

2. **§3 (the honest finding about direction).** Combining $0<\Lambda<m/B$ with the de Weger / LMN
   **lower** bound on $\Lambda$ reproduces a **lower** bound on the cycle length $K$ — i.e. it
   reproduces the *Crandall side* of the squeeze, **not** an upper bound $F(m)$. I prove (by a clean
   directional argument) that the self-contained geometry $\Lambda<m/B$ **cannot, by itself**, produce
   the upper bound $F(m)$ on $K$: the genuine upper bound needs the sharper circuit-ratio analysis of
   Simons–de Weger / Hercher, which I could **not** reconstruct without their primary text. This is
   stated as a limitation, not hidden.

3. **§4–§5 (the squeeze, anchored to verified literature numbers).** I assemble the squeeze with the
   **Crandall continued-fraction lower bound** (verified verbatim) and the **verified bound $B$**, and
   compute the lower bound on $K$ at $B=3\cdot 2^{69}$ (Hercher) and $B=2^{71}$ (Barina 2025).

4. **§6 (`[PROVISIONAL]`).** I estimate the largest excludable $m^\*$ at $B=2^{71}$ under a transparent,
   two-way-bracketed model for Hercher's upper bound $F(m)$. **The honest conclusion is that $B=2^{71}$
   alone does NOT robustly beat $m=91$** (best case $+1$, to $m^\*=92$); the optimistic extrapolation
   ($m^\*\approx 99$) is not trustworthy. This **must** be checked against Hercher's exact $F(m)$.

**Deliverable honesty.** The solid, citable output of this note is the **complete from-scratch
derivation of the cycle equation, the exact $\Lambda=\sum\varepsilon_j$ identity, and the rigorous
$0<\Lambda<m/B$ bound**, plus the precise localization of *why* the upper bound $F(m)$ is the hard part
and *exactly* what in Hercher's paper is needed to finish. The $m^\*>91$ question is left **open and
provisional**, as the ABSOLUTE RULES require.

> **Convention, fixed once and explicitly (see §1.1).** Throughout, **$m$ = the number of circuits =
> the number of local minima = the number of maximal ascending (o-step) runs** of the cyclic sequence.
> This is the Simons–de Weger / Hercher "$m$-cycle" convention (verified: Simons–de Weger define an
> $m$-cycle as a periodic orbit with $m$ local minima, and prove none for $1\le m\le 68$; Hercher
> extends to $m\le 91$). $K$ = number of o-steps, $N=K+S$ = number of $T$-steps in one period.

---

## 1. Setup, convention, and the cycle equation (from scratch)

### 1.1 The map, circuits, and the count $m$

We use the accelerated map (`notation.md` §2.1)
$$
T(n)=\begin{cases} n/2, & n\text{ even},\\ (3n+1)/2, & n\text{ odd}.\end{cases}
$$
An **o-step** is $x\mapsto(3x+1)/2$ (applied when $x$ odd); an **e-step** is $x\mapsto x/2$.

A nontrivial cycle is a finite positive periodic orbit of $T$ not equal to $\{1,2\}$. Read cyclically,
the parity sequence is a concatenation of **maximal ascending runs** (consecutive o-steps) and
**maximal descending runs** (consecutive e-steps). One ascending run followed by the descending run
that brings the value back down to the next local minimum is a **circuit** (Steiner's terminology).

- $m$ := number of circuits = number of maximal ascending runs = number of **local minima** $x_1,\dots,x_m$ (each odd).
- Circuit $j$: $a_j\ge 1$ o-steps (ascending) then $b_j\ge 1$ e-steps (descending), $j=1,\dots,m$.
- $K=\sum_{j=1}^m a_j$ (total o-steps), $\;L_j=a_j+b_j$ (length of circuit $j$), $\;N=\sum_{j=1}^m L_j=K+S$ (period).

> **Why $b_j\ge1$.** After an ascending run ends, the value $(3\cdot(\text{odd})+1)/2$ is reached from an
> odd number, but more to the point: a *new* ascending run can only start at an **odd** local minimum,
> and the value immediately after the last o-step of a run is **even** (the run ended because the next
> $T$-image is even, i.e. an e-step follows). Hence every circuit has at least one e-step, $b_j\ge1$.
> (This is the standard circuit structure; it is what makes $m$ well-defined and is verified
> combinatorially by `cycles.py::circuit_decomposition`.)

### 1.2 The per-circuit identity (rigorous, iteration-checked)

**Lemma 1 (one circuit).** *If $x_j$ is an odd local minimum and circuit $j$ consists of $a_j$ o-steps
then $b_j$ e-steps, ending at the next local minimum $x_{j+1}$, then*
$$
\boxed{\,2^{L_j}\,x_{j+1} \;=\; 3^{a_j}\,x_j \;+\; \big(3^{a_j}-2^{a_j}\big),\qquad L_j=a_j+b_j.\,}
\tag{1}
$$

*Proof.* Applying $x\mapsto(3x+1)/2$ exactly $a$ times to an odd $x$ (all intermediate values odd,
which is what "ascending run of length $a$" means) gives, by induction,
$$
x\;\longmapsto\;\frac{3^{a}x+(3^{a}-2^{a})}{2^{a}}.
$$
(Base $a=1$: $(3x+1)/2=(3x+3-2)/2=(3^1x+(3^1-2^1))/2$. Step: if after $a$ steps the value is
$y=(3^{a}x+(3^{a}-2^{a}))/2^{a}$, one more o-step gives $(3y+1)/2=(3^{a+1}x+(3^{a+1}-2^{a+1}))/2^{a+1}$,
using $3(3^a-2^a)+2^a=3^{a+1}-2^{a+1}$.) Then $b$ e-steps divide by $2^{b}$, giving
$x_{j+1}=\big(3^{a_j}x_j+(3^{a_j}-2^{a_j})\big)/2^{L_j}$, which is (1). $\square$

**Verified** (`verify_cycle_bound.py::check_per_circuit_identity`, D1): for $400$ random $(a,x)$ with a
genuine ascending run, (1) holds by direct iteration of $T$ — **no algebra trusted**. PASS.

### 1.3 The cycle equation

Set $d_j:=3^{a_j}-2^{a_j}>0$. Iterating (1) around the loop ($x_{m+1}=x_1$) and solving the cyclic
linear recurrence $x_{j+1}=(3^{a_j}x_j+d_j)/2^{L_j}$ for its fixed point:

**Lemma 2 (cycle equation).**
$$
\boxed{\,x_1\,(2^{N}-3^{K}) \;=\; R,\qquad
R=\sum_{j=1}^{m} d_j\,3^{\,P_j}\,2^{\,N-Q_j},\quad
P_j=\!\!\sum_{i>j}a_i,\;\; Q_j=\!\!\sum_{i\ge j}L_i.\,}
\tag{2}
$$
*Moreover $R>0$, so $2^{N}-3^{K}$ has the same sign as $x_1$; for a positive cycle $2^N>3^K$, i.e.*
$$
N>K\log_2 3,\qquad \Lambda:=N\log 2-K\log 3>0.
\tag{3}
$$

*Proof.* Unrolling the recurrence once around the loop,
$x_1=\big(\prod_j 3^{a_j}/2^{L_j}\big)x_1+\sum_j d_j\,3^{P_j}2^{-(\,\text{trailing }L\,)}$. The product of
multipliers is $3^{K}/2^{N}$, so $x_1(1-3^K/2^N)=\sum_j d_j\,3^{P_j}/2^{Q_j}$; multiplying by $2^N$ gives
(2). Each $d_j>0$ and the powers are nonnegative, so $R>0$. Positivity of $x_1$ then forces
$2^N-3^K>0$, equivalently (3). $\square$

**Verified** (`verify_cycle_bound.py::check_fixed_point`, D2): for $80$ random circuit lists, the closed
form $x_1=R/(2^N-3^K)$ is the exact fixed point of the recurrence (exact `Fraction` iteration closes).
PASS. (This is the same denominator $2^N-3^K$ used in `cycles.py::cycle_n_from_parity`, cross-checked.)

> This reproduces **Lemma 1 of `cycle_exclusion_explicit.md`** ($2^N>3^K$) with an *explicit* $R$ built
> from the circuits — the piece the earlier note left implicit.

---

## 2. The exact $\Lambda=\sum\varepsilon_j$ identity and the bound $0<\Lambda<m/B$ (NEW, rigorous)

This is the technical heart and the genuinely new, fully-derived content.

**Theorem 3 (telescoping identity for $\Lambda$).** *For any positive $m$-cycle with local minima
$x_1,\dots,x_m$,*
$$
\boxed{\;\Lambda \;=\; N\log 2-K\log 3 \;=\; \sum_{j=1}^{m}\varepsilon_j,\qquad
\varepsilon_j \;=\; \log\!\Big(1+\frac{d_j}{3^{a_j}x_j}\Big)
\;=\;\log\!\Big(1+\frac{1-(2/3)^{a_j}}{x_j}\Big)\; >0.\;}
\tag{4}
$$

*Proof.* Rewrite the per-circuit identity (1) as
$2^{L_j}x_{j+1}=3^{a_j}x_j\big(1+d_j/(3^{a_j}x_j)\big)$ (valid since $x_j>0$). Take logarithms:
$$
\log x_{j+1}+L_j\log2 \;=\; a_j\log3+\log x_j+\varepsilon_j,
\qquad \varepsilon_j=\log\!\Big(1+\tfrac{d_j}{3^{a_j}x_j}\Big).
$$
Rearranged: $\log x_{j+1}-\log x_j = a_j\log3-L_j\log2+\varepsilon_j$. Sum over the cyclic index
$j=1,\dots,m$. The left side telescopes to $0$ (since $x_{m+1}=x_1$), giving
$0=K\log3-N\log2+\sum_j\varepsilon_j$, i.e. $\sum_j\varepsilon_j=N\log2-K\log3=\Lambda$. Finally
$d_j/(3^{a_j}x_j)=(3^{a_j}-2^{a_j})/(3^{a_j}x_j)=(1-(2/3)^{a_j})/x_j>0$, so each $\varepsilon_j>0$. $\square$

**Verified** (`verify_cycle_bound.py::check_lambda_identity`, D3): max abs error $\approx 3.9\times10^{-120}$
over $80$ random circuit fixed points. The identity is exact. PASS.

**Corollary 4 (the rigorous, self-contained $\Lambda$-bound).** *For a positive $m$-cycle with smallest
element $x_{\min}=\min_j x_j$,*
$$
\boxed{\;0 \;<\; \Lambda \;=\;\sum_{j=1}^{m}\varepsilon_j \;<\; \frac{m}{x_{\min}}.\;}
\tag{5}
$$
*In particular, if the Collatz conjecture is verified for all $n\le B$ (so $x_{\min}>B$),*
$$
\boxed{\;0 \;<\; \Lambda \;<\; \frac{m}{B}\qquad(\text{nats}).\;}
\tag{6}
$$

*Proof.* Each $\varepsilon_j=\log(1+t_j)$ with $0<t_j=(1-(2/3)^{a_j})/x_j<1/x_j\le 1/x_{\min}$ (using
$a_j\ge1\Rightarrow 0<1-(2/3)^{a_j}<1$ and $x_j\ge x_{\min}$). Since $\log(1+t)<t$ for $t>0$,
$\varepsilon_j<1/x_{\min}$, and summing the $m$ terms gives $\Lambda<m/x_{\min}$. Positivity is (4). For
(6) use $x_{\min}>B$. $\square$

**Verified** (`verify_cycle_bound.py::check_lambda_bound_positive`, D4): on **17,762 genuine positive
fixed points** of the circuit recurrence (all local minima $>0$, $2^N-3^K>0$), both the global bound
$0<\Lambda<m/x_{\min}$ and the per-term bound $0<\varepsilon_j\le 1/x_j$ hold on **every** one. PASS.
(Caveat: reachable fixed points have modest $x_{\min}$; a positive fixed point with $x_{\min}>10^6$
needs $N/K$ a high-order convergent of $\log_2 3$ and is not enumerable. Since (5) is a *scale-free
algebraic consequence*, the small-scale enumeration is a faithful, non-vacuous check; the $x_{\min}>B$
regime is covered by the **proof** above, not the enumeration. This is flagged in the code.)

> **What §2 establishes, cleanly and citably:** a nontrivial positive $m$-cycle forces the two-log form
> $\Lambda=N\log2-K\log3$ into the window $(0,\,m/B)$. Constants here are **exact and self-derived** —
> no external citation, no `[CONSTANT UNVERIFIED]` tag. This is the rigorous floor of the deliverable.

---

## 3. Which way does (6) cut? — the honest directional finding

Equation (6) is an **upper** bound on $\Lambda$. The squeeze needs to turn cycle existence into a
**bounded interval** for $K$. There are two Diophantine facts about $\Lambda=N\log2-K\log3$:

- **(LMN / de Weger lower bound on $\Lambda$).** Verified verbatim (`cycle_exclusion_explicit.md`
  §5.1b, reproduced numerically in `verify_cycle_exclusion.py` C5a): *the inequality
  $0<\Lambda<2^{-0.158K}$ has no solution for $K\ge32$,* i.e.
  $$
  \Lambda\;\ge\;2^{-0.158\,K}\qquad(K\ge32).
  \tag{7}
  $$
  More fundamentally, LMN gives $\Lambda\ge\exp\!\big(-C(\log K)^2\big)$, $C\approx24.34\log3$ (the
  $24.34\,D^4$ constant; **`[CONSTANT UNVERIFIED]`**, primary PDF unreachable — see §5.3 of the earlier
  note). Both are **lower** bounds that *shrink* as $K$ grows.

- **(Geometry upper bound on $\Lambda$).** Corollary 4: $\Lambda<m/B$ — a bound that is **constant in
  $K$** (depends only on $m,B$).

**Proposition 5 (direction).** *Combining (6) with any positive lower bound $\Lambda\ge\ell(K)$ yields a
**lower** bound on $K$, never an upper bound. In particular (6)+(7) give*
$$
2^{-0.158K} \;\le\; \Lambda \;<\; \frac{m}{B}
\;\;\Longrightarrow\;\;
\boxed{\,K \;>\; \frac{\log_2(B/m)}{0.158}\,.}
\tag{8}
$$

*Proof.* $\ell(K)\le\Lambda<m/B$ gives $\ell(K)<m/B$. Since $\ell$ is **decreasing** in $K$ (both
$2^{-0.158K}$ and $\exp(-C(\log K)^2)$ are), the inequality $\ell(K)<m/B$ is satisfied precisely for
$K$ *large*; it bounds $K$ **below**. For (7) explicitly: $2^{-0.158K}<m/B\iff -0.158K<\log_2(m/B)\iff
K>\log_2(B/m)/0.158$. $\square$

**This is the crux of the honest finding.** The self-contained geometry (6) reproduces only the
**lower** bound on the cycle length — the *Crandall side* of the squeeze. It does **not** produce the
**upper** bound $F(m)$ on $K$. (The same observation appears, unproven, in the parenthetical at the end
of `cycle_exclusion_explicit.md` §2; here it is **proved** as Prop 5.)

> **Consequence for the reconstruction.** The upper bound $F(m)$ — the quantity that, set against the
> Crandall lower bound, makes the interval for $K$ *empty* for $m\le m^\*$ — **cannot** come from
> $\Lambda<m/B$ plus transcendence. It requires a **sharper geometric input**: a bound on $\Lambda$ (or
> on the circuit ratios) that *decays in $K$ faster than the LMN lower bound*, so that for $K>F(m)$ the
> cycle is impossible. The literature supplies this as "an analytical expression for an upper bound as a
> function of $K$ and $L$, by theoretical approximation of the ratio between numbers in possible cycles"
> (verified snippet, Simons–de Weger) and, in Hercher, as sharpened "bounds on averages and on sums of
> an arbitrary number of terms" over the $m$ circuit ratios. **I was unable to reconstruct $F(m)$ from
> scratch**: my attempts to extract a $K$-decaying upper bound on $\Lambda$ from the circuit geometry
> all collapsed back to lower bounds on $K$ (Prop 5). Reproducing $F(m)$ rigorously needs Hercher's /
> Simons–de Weger's primary text, which is HTTP-403 in this environment. This is the residual
> `[PARTIAL-DERIV]`, now **sharply localized**: it is exactly the upper-bound side, and §6 treats
> $F(m)$ as an anchored model rather than a derived object.

---

## 4. The lower bound on $K$: Crandall's continued-fraction bound (verified) + the verified $B$

The sharp lower bound on the cycle length is **not** (8) (which is lossy) but Crandall's
continued-fraction bound, verified verbatim (WebSearch 2026-06-02):

**Crandall's lemma (as restated).** *If $N_0$ is the lowest element of a positive $3x+1$ cycle and
$p_j/q_j$ ($j>4$) are the convergents of $\log3/\log2$, then the number $K$ of o-steps satisfies*
$$
\boxed{\;K \;>\; \frac32\,\max_{j>4}\,\min\!\Big(q_j,\;\frac{2N_0}{q_j+q_{j+1}}\Big),\qquad N_0>B.\;}
\tag{9}
$$

The $q_j$ are convergent denominators of $\delta=\log_2 3$; this is the operative *lower* bound, and it
is **stronger** than (8) because it exploits the *quality* of rational approximation (the
$2B/(q_j+q_{j+1})$ branch), not merely the magnitude $m/B$.

**Computed** (`verify_cycle_bound.py`, D5; convergents self-derived at dps $=120$):

| $B$ | source | Crandall lower bound on $K$ | binding $q_j$ |
|---|---|---|---|
| $3\cdot2^{69}$ | Hercher 2023 | $K>2.617\times10^{10}$ | $q_{22}=65{,}470{,}613{,}321$ |
| $2^{71}$ | **Barina 2025** | $K>3.489\times10^{10}$ | $q_{22}=65{,}470{,}613{,}321$ |

The ratio is exactly $2^{71}/(3\cdot2^{69})=2^{71}/2^{70.585}=2^{0.415}\approx1.333$.

> **Verified anchor (decisive structural check).** Hercher states the target needed to push past $m=91$
> is $K\ge1.375\times10^{11}$. Our convergent computation gives $q_{23}=137{,}528{,}045{,}312
> =1.375\times10^{11}$ **exactly** — so Hercher's "$1.375\times10^{11}$" is precisely the convergent
> denominator $q_{23}$ of $\log_2 3$ (`verify_cycle_bound.py` D5, PASS). This confirms the Crandall
> mechanism is the operative lower bound and that "the next $K$-plateau is $q_{23}$".

---

## 5. The squeeze, assembled

A nontrivial positive $m$-cycle requires
$$
\underbrace{K \;>\; \tfrac32\max_{j>4}\min\!\big(q_j,\tfrac{2B}{q_j+q_{j+1}}\big)}_{\text{lower bound }G(B)\ \text{(Crandall, §4)}}
\qquad\text{and}\qquad
\underbrace{K \;<\; F(m)}_{\text{upper bound (LMN circuit analysis, §3 — not reconstructed)}}.
$$
$G(B)$ **increases** with $B$ (more verification ⟹ longer forced cycle). $F(m)$ **increases** with $m$
(more circuits ⟹ weaker forcing ⟹ longer cycle admitted). A cycle can exist only if $G(B)<F(m)$;
hence **no cycle when $F(m)\le G(B)$**, and the largest excluded count is
$$
\boxed{\,m^\* \;=\; \max\{\,m : F(m)\le G(B)\,\}.\,}
\tag{10}
$$

**Monotonicity in $B$ (the cheap lever).** Since $G(B)$ increases with $B$ while $F(m)$ is fixed, a
larger verified $B$ raises $G$, so the threshold $F(m)\le G(B)$ is met for **more** $m$ — i.e.
**$m^\*$ is nondecreasing in $B$.** Barina's $B=2^{71}$ raises $G$ from $2.617\times10^{10}$ to
$3.489\times10^{10}$ (a factor $1.333$), so $m^\*(2^{71})\ge m^\*(3\cdot2^{69})=91$. The question is **how
much** it rises — which needs $F(m)$ (§6).

> **To reach the next $K$-plateau $q_{23}=1.375\times10^{11}$** (the value Hercher flags as needed to go
> further), the Crandall bound must clear the $2B/(q_j+q_{j+1})$ branch at $j=23$:
> $2B/(q_{23}+q_{24})\ge q_{23}$, i.e. $B\ge q_{23}(q_{23}+q_{24})/2\approx 6.12\times10^{22}=2^{75.70}$.
> **Barina's $2^{71}$ falls well short of $2^{75.7}$** (`verify_cycle_bound.py` D6), so $B=2^{71}$ keeps
> the Crandall bound in the $q_{22}$ regime ($\sim3.5\times10^{10}$), only $1.333\times$ above Hercher's.

---

## 6. Largest excludable $m$ at $B=2^{71}$ — `[PROVISIONAL]`, `[UNVERIFIED — needs Hercher 2023]`

To turn (10) into a number we need $F(m)$, which §3 could not derive. We therefore **model** $F(m)$ two
ways, **both pinned so that $m^\*(3\cdot2^{69})=91$** (self-consistency with Hercher's verified result),
and report the **bracket**. *This entire section is provisional bookkeeping, not a derivation.*

**Anchors (verified literature numbers).**
- Simons $m=2$: LMN upper bound $F(2)\approx 8.6\times10^4$ (verified, `cycle_exclusion_explicit.md` §4.2).
- Hercher $m^\*=91$ at $B=3\cdot2^{69}$, so $F(91)\approx G(3\cdot2^{69})=2.617\times10^{10}$ and $F(92)$ just above it.
- Hercher's abstract: pure **verification-bound** improvement moved $m^\*$ from $75$ (Simons–de Weger,
  $\approx2^{58}$-era $B$) to $82$ ("$m\ge83$ with newer checked bounds", $\approx2^{68}$-era $B$) — i.e.
  **$+7$ in $m^\*$ over $\approx10$ doublings of $B$**, before Hercher's own combinatorial gain ($+9$, to $91$).

**Model P (power law, optimistic).** $F(m)=c\,m^{p}$ through $(2,\,8.6\times10^4)$ and
$(91,\,2.617\times10^{10})$ gives $p\approx3.31$, $c\approx8.7\times10^3$. Then $F(m)\le G(2^{71})=3.489\times10^{10}$
holds up to **$m^\*\approx 99$** (`verify_cycle_bound.py` D6). *This is almost certainly too optimistic*:
$F(m)$ is LMN-determined, not a clean power law, and a $2$-point extrapolation across $m=2\to91$ is
unreliable near the crossover.

**Model H (Hercher-calibrated, conservative).** Calibrate the *local* slope from Hercher's own datum:
$+7$ in $m^\*$ per $\approx10$ doublings of $B$ ⟹ $\approx0.7$ units of $m^\*$ per doubling of $G$.
Barina over Hercher is $\log_2(G(2^{71})/G(3\cdot2^{69}))=\log_2(1.333)=0.415$ doublings, so
$$
\Delta m^\* \;\approx\; 0.7\times0.415 \;\approx\; +0.3
\qquad\Longrightarrow\qquad
m^\*(2^{71}) \;\approx\; 91\text{–}92.
$$

**Bracket and honest conclusion.**
$$
\boxed{\;91 \;\le\; m^\*(2^{71}) \;\lesssim\; 99,\quad\text{with the trustworthy estimate } m^\*(2^{71})\in\{91,\,92\}.\;}
$$
The two models disagree widely precisely because **the answer is governed by $F(m)$'s local growth rate
at $m\approx91$, which only Hercher's explicit constants pin down.** The conservative,
Hercher-self-calibrated read is that **$B=2^{71}$ alone does NOT robustly beat $91$** — at best it gives
$m^\*=92$, and quite possibly it leaves $m^\*=91$ because the jump is only $1.333\times$ (well short of
the $2^{75.7}$ needed to reach the next convergent plateau $q_{23}$).

> ### `[UNVERIFIED — needs check vs Hercher 2023 primary source]`
> Any claim that $m^\*>91$ at $B=2^{71}$ is **provisional** and rests on a *model* of $F(m)$, because I
> reconstructed the lower-bound side from scratch but **could not** reconstruct Hercher's upper bound
> $F(m)$ (§3) — his PDF (arXiv:2201.00406 / JIS 26) is HTTP-403 here. To confirm or refute "$m^\*=92$ at
> $B=2^{71}$" one needs, from Hercher's paper:
> 1. the **explicit $F(m)$** (his "analytical expression for the upper bound as a function of $K$ and
>    $L$"), to evaluate $F(92)$ and check whether $F(92)\le G(2^{71})=3.489\times10^{10}$;
> 2. confirmation of **which two-log constant** he used (LMN-1995 $24.34$ vs Laurent-2008), since a
>    sharper constant would independently shift $F$;
> 3. whether his $m^\*=91$ is already *tight* against $G(3\cdot2^{69})$ or has slack (if $F(92)$ is only
>    marginally above $2.617\times10^{10}$, then Barina's $3.489\times10^{10}$ *does* clear it and
>    $m^\*=92$; if $F(92)\gg3.5\times10^{10}$, it does not).
>
> **I do NOT claim an improvement over $m=91$.** The honest, confirmed deliverable is the from-scratch
> derivation of §1–§4 and the precise localization of the residual gap.

---

## 7. Summary of what is rigorous vs. provisional

| Result | Status | Evidence |
|---|---|---|
| Per-circuit identity (1) | **rigorous, self-contained** | Lemma 1; D1 (iteration) PASS |
| Cycle equation (2)–(3), explicit $R$ | **rigorous, self-contained** | Lemma 2; D2 PASS |
| **Exact identity $\Lambda=\sum\varepsilon_j$ (4)** | **rigorous, NEW** | Thm 3; D3 ($10^{-120}$) PASS |
| **Bound $0<\Lambda<m/B$ (6)** | **rigorous, self-contained, NEW** | Cor 4; D4 (17,762 cases) PASS |
| Direction: (6) ⟹ *lower* bound on $K$ (Prop 5) | **rigorous** | §3; (8) |
| $F(m)$ (upper bound on $K$) | **NOT reconstructed** | §3 limitation; needs Hercher PDF |
| Crandall lower bound (9), values at $B$ | facts **verified**; values **computed** | §4; D5 PASS; $q_{23}=1.375\times10^{11}$ exact |
| de Weger $\Lambda\ge2^{-0.158K}$, $K\ge32$ | snippet-verified + reproduced | (7); `verify_cycle_exclusion.py` C5a |
| LMN constant $24.34\,D^4$ | **`[CONSTANT UNVERIFIED]`** | primary PDF 403 |
| $B=2^{71}$ (Barina 2025) | **web-verified** | J. Supercomput. 81 (2025) |
| $m^\*(2^{71})\in\{91,92\}$ (best case $+1$) | **`[PROVISIONAL]` / `[UNVERIFIED vs Hercher]`** | §6 model bracket |

**Does the from-scratch cycle-length function match the red-team's reproduced inequality?** Yes,
partially and informatively: the red-team reproduced de Weger's $0<\Lambda<2^{-0.158K}$ (no solution
$K\ge32$), which is the **lower** bound on $\Lambda$ / **lower** bound on $K$. My from-scratch derivation
produces the complementary **upper** bound on $\Lambda$, $\Lambda<m/B$, and Prop 5 shows the two combine
to a **lower** bound on $K$ — i.e. they are mutually consistent and together reproduce the *Crandall
side* of the squeeze. The from-scratch derivation does **not** reproduce Hercher's *upper* bound $F(m)$
on $K$; that remains the open piece.

---

## 8. Self-contained citation-free fallback (for completeness)

If one refuses *all* external transcendence input (no LMN, no de Weger), the integrality
$2^N-3^K\ge1$ gives the citation-free lower bound $\Lambda\ge\log(1+3^{-K})>3^{-K}/2$, and combined with
(6), $3^{-K}/2<m/B\Rightarrow K>\log_3(B/(2m))$. At $B=2^{71}$, $m=91$ this is only $K>40.6$
(`verify_cycle_exclusion`-style arithmetic) — far weaker than Crandall's $3.5\times10^{10}$, but it
needs **no citation** and shows the squeeze's *lower* side is real without any black-box constant. (It
does not, of course, exclude any $m$; the strong lower bound and the upper bound $F(m)$ are what do the
work.) This is the honest fallback the brief asked for: a self-contained constant ($3^{-K}$) replacing
the snippet-sourced $0.158$, at the cost of strength.

---

## 9. Pointers

- Derivation checker: `experiments/verify_cycle_bound.py` (D1–D6).
- Brute-force + circuit decomposition + bound consistency: `experiments/cycles.py`
  (`circuit_decomposition`, `check_bound_consistency`; wired into `run_cycle_search`).
- Literature-anchor checker (de Weger threshold, convergents, Hercher arithmetic):
  `experiments/verify_cycle_exclusion.py` (unchanged; still PASS).
- Earlier reconstruction (inputs, bottleneck identification): `theory/cycle_exclusion_explicit.md`.
- Failed sub-approaches: `theory/dead_ends.md` (this note's entries appended).
