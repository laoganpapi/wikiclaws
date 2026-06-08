# Digit-Statistic Lyapunov Candidates for Accelerated Collatz: an Honest Negative Result

> **Status:** `[NEGATIVE RESULT — established]`. No new bound. We quantify, precisely
> and reproducibly, *why* binary-digit statistics (and their hybrids with $\log_2 n$)
> cannot serve as Lyapunov functions for the Collatz map.
>
> **Track:** Collatz, "why it's hard" / obstruction catalogue.
>
> **Author:** Alex Ye (AI-assisted computation; AI not on author line per project rules).
>
> **Companion files / data:**
> - `experiments/lyapunov_search.py` — the digit-statistic sweep (Hamming weight, run-count, carry-count; hybrids $\alpha X(n)+\beta\log_2 n$; random-parity and uniform-bit drift models).
> - `experiments/data/lyapunov_sweep.json` — the data (re-run and verified, see §6).
> - `experiments/verifier.py` — the accelerated map `T`.

---

## 0. Setup and notation

We work with the **accelerated Collatz map** $T:\mathbb{Z}_{\ge1}\to\mathbb{Z}_{\ge1}$,
$$
T(n)=\begin{cases} n/2 & n\text{ even},\\[2pt] (3n+1)/2 & n\text{ odd}. \end{cases}
$$
(This is one full "$3n+1$ then halve once" on odd $n$; it is the standard
acceleration that folds the forced division-by-2 into the odd step.)

A function $L:\mathbb{Z}_{\ge1}\to\mathbb{R}_{\ge0}$ is a **(strict) Lyapunov function**
for the Collatz problem if it is bounded below, has a level set $\{L\le c\}$ that is
finite, and satisfies $L(T(n))<L(n)$ for all $n$ outside a finite set. Existence of such
an $L$ would prove the conjecture: every orbit would strictly descend in $L$ until it
entered the finite low-level set, which one then checks by hand.

We study the family of **binary-digit statistics**:

| symbol | name | definition |
|---|---|---|
| $s(n)$ | Hamming weight | number of $1$-bits of $n$ (popcount) |
| $r(n)$ | run-count | number of maximal equal-bit runs of $n$ ($r(0)=0$) |
| $c(n)$ | carry-count | for $n$ odd, number of base-2 carries in the addition $n+(n+1)/2$ (which equals $T(n)$); $c(n)=0$ for $n$ even |
| $\log_2 n$ | size coordinate | the real logarithm — the *non*-digit "magnitude" coordinate |

and the **hybrid family**
$$
L_{\alpha,\beta}(n)=\alpha\,X(n)+\beta\log_2 n,\qquad X\in\{s,r,c\},\ \alpha,\beta\ge0.
$$

The carry-count has a classical reading: by Kummer's theorem the number of base-$p$
carries in $a+b$ equals $\nu_p\binom{a+b}{a}$, so $c(n)=\nu_2\binom{n+(n+1)/2}{n}$.

---

## 1. The two obstructions, stated up front

There are exactly two independent reasons no member of this family is a Lyapunov function.
Both are rigorous; the computation in §3–§5 only *quantifies* them.

**(O1) Magnitude-blindness of pure digit statistics.** Each of $s,r,c$ is bounded on
the infinite set of powers of two, while $n\to\infty$ there. Concretely
$$
s(2^k)=r(2^k)=1,\quad c(2^k)=0\qquad\text{for all }k\ge1,
$$
yet $2^k\to\infty$. So no level set $\{X\le c\}$ of a pure digit statistic is finite — the
basic structural requirement for a Lyapunov function fails outright. A pure digit
statistic *cannot bound the magnitude of the trajectory*, so even a perfect pointwise
decrease $X(T(n))<X(n)$ would not preclude an orbit escaping to infinity. (It also is not
true that $X$ decreases pointwise; see §3.) This kills $\beta=0$ for any $X$.

**(O2) Non-strictness of the log-drift, and absence of a pointwise supermartingale.**
The size coordinate $\log_2 n$ has finite level sets, so it fixes (O1); and on a *typical*
trajectory it drifts *downward* (this is the Tao/Lagarias–Weiss heuristic descent, §4).
But the drift is only an **average**, not a pointwise inequality: a single $3n+1$ step
*increases* $\log_2 n$ by $\log_2 3-1\approx0.585$. So $\log_2$ is, at best, an
*approximate/average* supermartingale, never a strict pointwise Lyapunov function. Adding
a digit term $\alpha X$ to repair the per-step sign does not work either: across the entire
$\approx7.2\times10^6$-step dataset, **not a single** hybrid $L_{\alpha,\beta}$ (other than
the trivial $\alpha=\beta=0$) achieves $\max_{\text{steps}}\big(L(T(m))-L(m)\big)\le0$
(see §5). Every candidate has a strictly increasing step somewhere. Equivalently: the
digit statistics are not correlated with the magnitude jump *in the right pointwise way* to
cancel it — they cancel it only on average, reproducing exactly the known heuristic and
adding no rigour.

The honest conclusion: **this family recasts the Tao/heuristic average descent in
digit-coordinates and inherits its single fatal feature — averageness — while the pure
statistics additionally fail the finiteness requirement.** No new bound is obtained.

---

## 2. Why these were worth checking at all

The hope (a reasonable one) was that a digit statistic might be pointwise *anti-correlated*
with the magnitude jump: the $3n+1$ step that grows $\log_2 n$ might *systematically*
destroy binary structure (lower the Hamming weight or run-count by enough that
$\alpha\Delta X$ cancels $\beta\Delta\log_2$ pointwise). If that held with a strict sign,
$L_{\alpha,\beta}$ would be a genuine Lyapunov function and Collatz would follow. The
data settle the question in the negative: the anti-correlation exists only in the mean.

---

## 3. Pure-statistic per-step drifts (deterministic sweep, $n\in[2,10^5)$)

Trajectory sweep over all starting $n\in[2,100001)$ down to $1$:
$3{,}564{,}892$ odd steps and $3{,}624{,}056$ even steps ($\approx7.19\times10^6$ total).
$\Delta X := X(T(m))-X(m)$ recorded per visited step $m$, bucketed by parity.

| statistic $X$ | $\mathbb{E}[\Delta X]$ all | odd-step | even-step | $P(\Delta X\le0)$ | $P(\Delta X<0)$ | $\max\Delta X$ |
|---|---:|---:|---:|---:|---:|---:|
| Hamming $s$ | $-0.09946$ | $-0.20058$ | $0.0$ | $0.8271$ | $0.2385$ | $+8$ |
| runs $r$ | $-0.10410$ | $+0.30374$ | $-0.50528$ | $0.7516$ | $0.4213$ | $+12$ |
| carry $c$ | $-0.04084$ | $-2.5402$ | $+2.4177$ | $0.6275$ | $0.3515$ | $+26$ |

Reading:
- **Even steps are transparent for $s$** ($\Delta s=0$ exactly: halving is a bit-shift, no
  change in popcount), so all of $s$'s average decrease is forced onto odd steps.
- Every statistic has $\max\Delta X>0$: pointwise increases occur. None is a pointwise
  supermartingale even before adding the magnitude term.
- The small *negative* means are real but tiny and noisy relative to $\max\Delta X$; they
  cannot control a trajectory.

---

## 4. The $\log_2$ drift: the heuristic descent, reproduced exactly

Same sweep, recording $\Delta\log_2 := \log_2 T(m)-\log_2 m$:

| | mean | predicted closed form |
|---|---:|---|
| odd steps | $+0.59114$ | $\log_2 3-1=0.584963$ |
| even steps | $-1.0$ (exact) | $-1$ |
| all steps | $-0.21098$ | $(\log_2 3-2)/2=-0.207519$ |

The odd-step mean sits just above $\log_2 3-1$ (the bare $\log_2 3-1$ ignores the $+1$ in
$3n+1$, which is positive but $O(1/n)$). The all-step mean matches the textbook
$\tfrac12(\log_2 3-2)<0$ Tao/Lagarias–Weiss heuristic descent rate. **This is exactly the
known average-descent heuristic** — the digit machinery reproduces it but does not upgrade
it to a pointwise statement: the odd-step $\log_2$ drift is $+0.585>0$, i.e. magnitude
*genuinely grows* on every single odd step.

---

## 5. Hybrids $L_{\alpha,\beta}=\alpha X+\beta\log_2 n$: no pointwise supermartingale

We swept $\alpha\in\{0,\tfrac14,\tfrac12,1,2,5\}$, $\beta\in\{0,\tfrac14,\tfrac12,1,2\}$ for each
$X\in\{s,r,c\}$ over the full step dataset. Representative rows (Hamming):

| $\alpha$ | $\beta$ | mean $\Delta L$ | $P(\Delta L<0)$ | $\max\Delta L$ |
|---:|---:|---:|---:|---:|
| $1$ | $0$ | $-0.09946$ | $0.2385$ | $+8.000$ |
| $1$ | $\tfrac12$ | $-0.20495$ | $0.7427$ | $+8.292$ |
| $1$ | $1$ | $-0.31044$ | $0.7427$ | $+8.585$ |
| $1$ | $2$ | $-0.52142$ | $0.5961$ | $+9.170$ |

The most negative *mean* in the entire sweep is $(\text{runs},\alpha=5,\beta=2)$ with mean
$-0.94244$ — but $\max\Delta L=+61.17$.

**Headline negative fact (machine-checked over $7.19\times10^6$ steps):**
$$
\#\big\{(X,\alpha,\beta):(\alpha,\beta)\ne(0,0),\ \max_{\text{steps}}\Delta L_{\alpha,\beta}\le0\big\}=0.
$$
Every nontrivial hybrid increases somewhere. Increasing $\beta$ buys a more negative mean
(it imports more of the heuristic descent) but **also raises $\max\Delta L$**, because the
$\beta\,(\log_2 3-1)$ jump on odd steps is always present and the digit term $\alpha\Delta X$
does not cancel it pointwise. The two coordinates anti-correlate in mean, never pointwise.

---

## 6. Reproduction / verification log

Re-ran `lyapunov_search.py --n-start 2 --n-end 100001` (2026-06-03) and diffed against the
committed `data/lyapunov_sweep.json`:

- **Trajectory sweep block:** identical bit-for-bit (same $3{,}564{,}892$ odd / $3{,}624{,}056$
  even step counts; all `per_stat`, `log2`, and `hybrid` summaries identical excluding the
  wall-clock `secs` field).
- **Random-parity model block** (seed-1 sampling at $n\sim10^7$): identical.
- **Closed-form uniform-bit block** (seed-1, bit-lengths $16,24,32$): identical.

The random-parity model (i.i.d. fair parity, the Tao/Lagarias–Weiss regime) gives
$\mathbb{E}_{\text{avg}}[\Delta\log_2]$ via the statistics: Hamming $-0.2092$, runs $-0.5207$,
carry $-0.2834$ — all negative-on-average, all with positive-mean *odd-step* magnitude jump,
consistent with the deterministic sweep. **No discrepancy found; the committed data
reproduce exactly.**

---

## 7. Verdict

- **(O1)** Pure digit statistics ($\beta=0$) are magnitude-blind: $s(2^k)=r(2^k)=1$,
  $c(2^k)=0$ for all $k$, so they have no finite level sets and cannot be Lyapunov
  functions regardless of drift.
- **(O2)** Hybrids fix the finiteness defect (the $\beta\log_2$ term has finite level sets)
  but inherit the *non-strict, average-only* descent of $\log_2$: zero of the
  $\approx90$ nontrivial $(X,\alpha,\beta)$ candidates is a pointwise supermartingale over
  $7.2\times10^6$ steps; the digit term cancels the magnitude jump only in the mean,
  reproducing the Tao/heuristic descent with no gain in rigour.

This is a clean **dead end** for the Lyapunov route via binary-digit observables. Its value
is expository: it pins down *what* a successful Lyapunov function would have to do that these
cannot — be simultaneously magnitude-aware (finite level sets) *and* pointwise (not merely
average) decreasing across the $3n+1$ jump. The function-field analog
(`theory/function_field.md`) exhibits a setting where *both* hold (the degree valuation), and
thereby isolates the precise archimedean feature of $\mathbb{Z}$ that defeats the program here.

**`[NOVELTY UNVERIFIED]`** that $s(n)$ does not decrease under Collatz is noted in Lagarias's
survey; the systematic $(\alpha,\beta)$ drift sweep with the pointwise-supermartingale audit
is, to our knowledge, not in the literature, but we have not exhaustively checked.
