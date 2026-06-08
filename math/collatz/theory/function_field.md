# The $\mathbb{F}_2[T]$ Collatz Analog: a Provably Convergent Model, and the Structural Disanalogy with $\mathbb{Z}$

> **Status:** `[STRUCTURAL RESULT — proved for the analog; says NOTHING about integer Collatz]`.
> The $\mathbb{F}_2[T]$ analog is provably convergent via a degree Lyapunov function. Its only
> use for the real conjecture is *diagnostic*: it isolates the exact archimedean feature of
> $\mathbb{Z}$ that the $3n+1$ step exploits and the polynomial ring lacks.
>
> **Track:** Collatz, "why it's hard" / obstruction catalogue.
>
> **Author:** Alex Ye (AI-assisted computation; AI not on author line per project rules).
>
> **Novelty:** `[NOVELTY UNVERIFIED]`. Function-field $3x+1$ analogs exist in the literature
> (Hicks–Mullen–Yucas, "Polynomial analogues of the $3N+1$ problem", *Amer. Math. Monthly*
> 115 (2008); also work in the Matthews / generalized-Collatz circle). We have located these
> only at snippet level and have NOT verified that the specific $\mathbb{F}_2[T]$ map below,
> or the degree-Lyapunov framing, coincides with theirs. Treat the map and the disanalogy
> framing as folklore-level; claim no priority.
>
> **Companion files / data:**
> - `experiments/function_field.py` — the map $\Phi$, cycle/fixed-point search, stopping-time and degree-Lyapunov tables.
> - `experiments/data/function_field.json` — the data (re-run and verified, see §6).

---

## 1. The analog, chosen for structural faithfulness

We replace the prime $2\in\mathbb{Z}$ by the irreducible $T\in\mathbb{F}_2[T]$ and ask for the
"cleanest" map on $\mathbb{F}_2[T]$ mirroring $n\mapsto n/2$ (even) / $(3n+1)/2$ (odd).
"Even" becomes "$T\mid f$"; "halve" becomes "divide by $T$". For the odd branch we need a
fixed multiplier (the analog of $3$) and a fixed constant (the analog of $+1$) such that the
result is *always* divisible by $T$ when $T\nmid f$. Define

$$
\boxed{\;\Phi:\mathbb{F}_2[T]\to\mathbb{F}_2[T],\qquad
\Phi(f)=\begin{cases} f/T & \text{if }T\mid f,\\[4pt] \dfrac{(T+1)\,f+1}{T} & \text{if }T\nmid f.\end{cases}\;}
$$

**Why $(T+1)f+1$ is forced, and why $p=2$ is special.** We need $(T+1)f+1\equiv0\pmod T$
when $T\nmid f$. Reducing mod $T$ (i.e. evaluating the constant term):
$((T+1)f+1)\bmod T = f(0)+1$. We need this to vanish for *every* admissible $f$ (every $f$
with $f(0)\ne0$), with a *single fixed* multiplier. In $\mathbb{F}_2$ the only nonzero
constant term is $1$, and $1+1=0$: so $f(0)+1=0$ automatically, and $(T+1)f+1$ is divisible
by $T$ for all odd $f$. Over $\mathbb{F}_p$ with $p>2$ no fixed multiplier achieves this
uniformly (the required constant would depend on $f(0)$), which is exactly why the clean
analog lives over $\mathbb{F}_2$. This is a known feature of the function-field $3x+1$ story
`[NOVELTY UNVERIFIED]`.

**Implementation.** Polynomials are Python ints (bit $i$ = coefficient of $T^i$); addition is
XOR, $f(0)$ is the low bit, division by $T$ is a right shift. The odd branch admits a fast
identity, verified in code against the direct definition over all $f$ with $\deg f\le12$:
$$
\Phi(f)=f\oplus\big((f\oplus1)\gg1\big)\qquad(f\text{ odd}).
$$

---

## 2. The degree Lyapunov function — proof of non-increase

Let $\deg$ be the usual polynomial degree ($\deg 0=-1$). It is the order/valuation at the
**infinite place** of $\mathbb{F}_2(T)$: $\deg f=-v_\infty(f)$.

**Proposition 1 (degree is non-increasing under $\Phi$).** For all $f\ne0$,
$\deg\Phi(f)\le\deg f$, with the two branches behaving as:
$$
\deg\Phi(f)=\deg f-1\ \ (T\mid f),\qquad \deg\Phi(f)=\deg f\ \ (T\nmid f).
$$

*Proof.* If $T\mid f$ then $\Phi(f)=f/T$ and $\deg(f/T)=\deg f-1$ (strict drop by 1).
If $T\nmid f$ then $f\ne0$ so $\deg f\ge0$; $\deg((T+1)f)=\deg f+1$ and adding the constant
$1$ does not change the top degree, so $\deg((T+1)f+1)=\deg f+1$; dividing by $T$ subtracts
$1$, giving $\deg\Phi(f)=\deg f$. In neither case does the degree increase. $\qquad\blacksquare$

So $\deg$ is a genuine Lyapunov function — bounded below by $-1$, with **finite level sets**
($\{\deg\le d\}$ has exactly $2^{d+1}$ elements), strictly decreasing on the "even" branch and
constant (never increasing) on the "odd" branch. This is the structural contrast with
$\mathbb{Z}$: there the magnitude $\log_2 n$ *increases* by $\log_2 3-1>0$ on the odd branch
(cf. `theory/digit_lyapunov.md` §4). Here the analog of the multiplier-3 step *cannot* raise
the Lyapunov value.

---

## 3. Convergence — proof

Non-increase alone is not termination, because the odd branch leaves $\deg$ constant. We need:
from any $f$, finitely many steps reach an even ($T\mid f$) step, forcing a strict drop.

**Proposition 2 (odd steps cannot persist).** For odd $f$ (low bit $1$), $\Phi(f)$ is even
$\iff$ the coefficient of $T^1$ in $f$ is $1$. Consequently the only odd polynomials whose
image is again odd are those with $f\bmod T^2=1$.

*Proof.* For odd $f$, $\Phi(f)=f\oplus((f\oplus1)\gg1)$. Its low bit is
$(f\&1)\oplus(((f\oplus1)\gg1)\&1)=1\oplus((f\gg1)\&1)$, since $f\oplus1$ only flips $f$'s low
bit, which the shift discards. Hence $\Phi(f)$ is even iff $(f\gg1)\&1=1$, i.e. iff the
$T^1$-coefficient of $f$ is $1$. $\qquad\blacksquare$

**Proposition 3 (convergence).** Every orbit of $\Phi$ reaches a fixed point; the fixed
points are exactly $0$ and $1$, and $\Phi$ has no nontrivial cycles. Hence $\Phi$ is globally
convergent.

*Proof sketch (rigorous core; full induction is routine).* By Proposition 1 the degree never
increases, and it strictly drops on every even step, so it suffices to bound the number of
consecutive odd steps. Write an odd $f$ that stays odd as $f=1+T^2g$ (Prop 2). A direct
computation in $\mathbb{F}_2[T]$ gives $\Phi(1+T^2g)=1+Tg+T^2g$ (when $g\ne0$; bits are
distinct), so $\Phi(f)\bmod T^2 = 1+T(g\bmod 2)$, which equals $T+1$ (an even-next image)
exactly when the bottom coefficient of $g$ is $1$. Each consecutive odd step therefore
consumes one more low coefficient of $f$; since $f$ has finite degree, after at most
$\deg f$ odd steps the $T^1$-coefficient becomes $1$ and the next step is even, dropping the
degree. So between successive strict degree drops there are at most $\deg f$ odd steps, and the
degree is a strictly-decreasing-on-a-bounded-subsequence non-negative integer: the orbit
reaches degree $\le0$, i.e. lands in $\{0,1\}$. Both are fixed ($\Phi(0)=0$; $\Phi(1)=1$ since
$(T+1)\cdot1+1=T$ and $T/T=1$). $\qquad\blacksquare$

The empirical bound on consecutive odd steps (§5) is $\le14$ for $\deg\le14$, consistent with
"$\le\deg f$".

---

## 4. The structural disanalogy with $\mathbb{Z}$ (the diagnostic payload)

This is the only thing the analog says about real Collatz, and it is purely *diagnostic*:

- $\mathbb{F}_2(T)$ has a degree (infinite-place, **non-archimedean**) valuation $v_\infty$,
  and the odd-branch multiplier $(T+1)$ raises $\deg$ by exactly $1$, which the forced
  division by $T$ then removes — net zero. The "growth" and the "shrink" live at the *same*
  place and cancel by a clean valuation identity. Degree is therefore a Lyapunov function.

- $\mathbb{Z}$ has one archimedean absolute value $|\cdot|$ (giving magnitude $\log_2 n$) and,
  separately, the $2$-adic valuation $\nu_2$ (controlling the halving). The Collatz odd step
  $n\mapsto3n+1$ **multiplies the archimedean size by $\approx3$ while the divisions are
  governed by $\nu_2$ at a different place.** The two valuations are *not* tied together by an
  identity: $\nu_2(3n+1)$ is (heuristically) geometric and independent of $\log n$, so the
  magnitude growth $\log_2 3$ per odd step is only *cancelled on average* by the $\nu_2$-driven
  halving (the Tao/Lagarias–Weiss $\tfrac12(\log_2 3-2)<0$ heuristic). There is no pointwise
  cancellation, hence no Lyapunov function from magnitude — exactly the (O2) obstruction
  catalogued in `theory/digit_lyapunov.md`.

**One-line statement.** *Over $\mathbb{F}_2[T]$ the multiplier and the divisor act at the same
(non-archimedean) place, so degree cannot increase and a Lyapunov proof goes through; over
$\mathbb{Z}$ the $3n+1$ step mixes the archimedean place (size $\times3$) with the $2$-adic
place (halving), and these two valuations are decoupled, so magnitude can increase and only a
probabilistic average descent survives.* The $\mathbb{F}_2[T]$ model is the controlled
experiment in which the archimedean/non-archimedean mixing is switched off — and convergence
becomes provable, pinpointing that mixing as the source of difficulty.

This says **nothing** about whether integer Collatz is true. It only certifies that the
difficulty is *located* in the archimedean–$2$-adic decoupling, not in (say) cycle bookkeeping
or digit combinatorics.

---

## 5. Data

From `data/function_field.json` (re-run, verified §6):

- **Cycles / fixed points** ($\deg\le8$, all $512$ polynomials): exactly $2$ fixed points,
  $0$ (basin $1$: only itself) and $1$ (basin $511$: everything else). No nontrivial cycles.
  Note $\Phi(T)=1$ and $\Phi(T+1)=T$, so $T+1$ flows into $1$; it is not itself fixed.
- **Stopping times to $\{0,1\}$** ($\deg\le14$, $32768$ polynomials): every polynomial
  converges. Mean stopping time grows linearly in degree ($\approx 2d$): e.g. $\deg14$ has
  mean $\sigma\approx25.87$, max $\sigma=43$.
- **Degree-Lyapunov audit** ($\deg\le16$, $131072$ polynomials): $n_{\text{increase}}=0$,
  $n_{\text{strict-decrease}}=65535$ (the even polynomials), $n_{\text{equal}}=65536$ (the
  odd polynomials), $0$ excluded. Status `PASS_NONINCREASING`. (Half decrease, half stay
  equal — exactly Proposition 1: even $\Rightarrow$ strict drop, odd $\Rightarrow$ equal.)
- **Consecutive odd-step runs** ($\deg\le14$): max $14$, attained at $T^{14}+1$ (the extremal
  $f=1+T^k$ family of Proposition 3); mean $\approx1.999$.

---

## 6. Reproduction / verification log

Re-ran `function_field.py` (2026-06-03, defaults $\deg_{\text{cycles}}=8$, $\deg_\sigma=14$,
$\deg_{\text{lyap}}=16$) and compared against committed `data/function_field.json`:
**identical bit-for-bit** (all of cycles, stopping distribution, degree-Lyapunov audit, and
consecutive-odd-step table). Additional independent checks:

- The fast odd-branch formula $\Phi(f)=f\oplus((f\oplus1)\gg1)$ equals the direct
  $((T+1)f+1)/T$ for all $f$ with $\deg f\le12$, and the quotient is always exact (the
  intermediate is divisible by $T$). Confirmed.
- $\deg\Phi(f)\le\deg f$ for all $f\in[1,2\times10^5)$ (inc $0$, eq $100000$, dec $99999$).
  Confirmed.
- Fixed points $\{0,1\}$ confirmed; $\Phi(T)=1$, $\Phi(T+1)=T$ confirmed.

**No discrepancy.**

---

## 7. Verdict / fit with the paper's "why it's hard" section

- The convergence result is **clean, proved, and entirely about the analog** — it is *not*
  evidence for integer Collatz and must never be presented as such.
- Its worth is as a **one-paragraph diagnostic** for a "why is $3n+1$ hard" discussion: it
  gives a crisp, checkable statement of the obstruction — *the $3n+1$ step couples the
  archimedean magnitude to the $2$-adic valuation, and it is precisely this coupling (absent
  over $\mathbb{F}_2[T]$, where multiplier and divisor share one non-archimedean place) that
  destroys the existence of a magnitude Lyapunov function.* This dovetails exactly with the
  digit-Lyapunov negative result (`theory/digit_lyapunov.md`), giving the paper a matched
  pair: a setting where a Lyapunov proof works (degree) and the explicit reason it fails to
  port to $\mathbb{Z}$ (valuation decoupling).
- **Recommendation:** include as a short "controlled-experiment" remark in the obstruction /
  background section, not as a result. Keep the `[NOVELTY UNVERIFIED]` flag and cite
  Hicks–Mullen–Yucas (2008) as the likely prior function-field treatment; do not claim
  originality for the map or the convergence, only (tentatively) for the explicit
  archimedean/non-archimedean framing of the disanalogy.
