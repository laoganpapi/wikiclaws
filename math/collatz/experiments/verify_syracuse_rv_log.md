# Step-1 Verification Log — Syracuse random variable structural check

**Date:** 2026-06-02
**Code:** `collatz/experiments/verify_syracuse_rv.py`
**Supports:** `collatz/theory/tao_syracuse_explicit.md` (Definitions 2.1, eqs (2.2)–(2.3), (5.1)–(5.2); Lemmas 6.1–6.2 arithmetic).
**Author:** Alex Ye (AI assistance disclosed separately).

## Scope of this Step-1 check

The main theorem under study (Conditional Theorem 5.2) and the hypotheses
$\mathrm{MIX}(\theta)$, Prop 1.17 are **asymptotic** ($n\to\infty$) and are therefore
not finitely testable. Per the verification protocol, for such claims Step 1 is
satisfied by **test-case construction** of the underlying finite objects plus the
exact small-$n$ values that the asymptotic statements specialize to. We verify:

1. **Definition 2.1 (Syracuse random variable) is correctly transcribed.**
   - `syracuse_law(n)` builds the EXACT law (rationals; truncation $a_j\le 40$, loss $<n\,2^{-40}$) via the suffix-sum recursion from eq (2.1).
   - $n=1$ closed form by hand: $\Syrac(\ZZ/3\ZZ)=2^{-a_1}\bmod 3$ $=2$ iff $a_1$ odd. So $P(2)=\sum_{k\,\mathrm{odd}}2^{-k}=2/3$, $P(1)=1/3$, $P(0)=0$.
   - **Result:** computed $P(0)=0.000000,\ P(1)=0.333333,\ P(2)=0.666667$. **Match: True.** Support on units $(\ZZ/3\ZZ)^\times=\{1,2\}$ confirmed.

2. **Submultiplicativity (2.3): $c_{n_1+n_2-1}\ge c_{n_1}c_{n_2}$.**
   - Tested all $n_1,n_2\in\{1,2,3\}$. **All 9 cases hold.** (This is a nontrivial check that the skew-convolution recursion in `syracuse_law` is consistent with Tao 2020.)

3. **$c_n$ and $c_n\cdot 3^n$ (the $\beta=1$ diagnostic).**

   | $n$ | $c_n$ | $c_n\cdot 3^n$ | $\sup_{3\nmid\xi}|\widehat\nu_n(\xi)|$ | argmax $\xi$ |
   |---|---|---|---|---|
   | 1 | 3.333e-01 | 1.000000 | 0.577350 | 1 |
   | 2 | 3.175e-02 | 0.285714 | 0.377924 | 5 |
   | 3 | 6.096e-03 | 0.164590 | 0.252237 | 19 |
   | 4 | 1.789e-03 | 0.144916 | 0.176999 | 65 |
   | 5 | 4.446e-04 | 0.108034 | 0.129274 | 211 |

   - $c_n3^n$ is **decreasing** — the Syracuse law is not exactly uniform, and the
     deviation persists. Consistent with $\beta=1$ (sub-exponential correction) but
     does NOT prove it; consistent also with $\beta>1$ on this tiny range.
   - $\sup|\widehat\nu_n|$ decreasing; small-$n$ data **cannot** distinguish Tao's
     $n^{-A}$ from the conjectural $3^{-\theta n}$ (they agree to leading order on $n\le5$).
     This is exactly why the gap is open: it is invisible at finite $n$.

4. **Descent-balance tilt $s^*$ (eq (5.2)).**
   - Tilted geometric mean $\EE_s[a]=1/(1-2^{-(1+s)})$; $\EE_0[a]=2$ (recovers $\Geom(2)$).
   - Solve $\EE_{s^*}[a]=\log_2 3$: $r^*=2^{-(1+s^*)}=1-1/\log_2 3=0.369070$, $s^*=0.438033$.
   - **Result:** $\EE_{s^*}[a]=1.584962501=\log_2 3$ to machine precision. **Match: True.**

## Additional arithmetic verified inline (not in the committed script run, but checked)

- **Lemma 6.2 Plancherel factor.** $\#\{\xi:3\nmid\xi\}=\varphi(3^n)=2\cdot3^{n-1}=\tfrac23\,3^n$ (confirmed for $n=3,5,10$). The $\ell^2\to$ TV passage costs $\sqrt{\varphi(3^n)}\sim 3^{n/2}$, so the natural-density threshold is $\theta>\tfrac12$. **Confirmed.**

## Pass criterion

Zero failures on all constructed test cases (Def 2.1 at $n=1$; submultiplicativity on $n\le5$; tilt $s^*$). **PASSED** for the definitional/finite content. The asymptotic hypotheses remain (necessarily) untested by computation and are handled by the structural derivation in the theory doc + the §6 reduction.

## Caveats

- This Step-1 check validates that our **transcription** of Tao's objects is correct and our **elementary arithmetic** (tilt, Plancherel factor) is correct. It does NOT validate the conditional theorem's transport steps (§5 Steps A/C), which require Step-2 red-team review against Tao's actual paper.
- Truncation $a_j\le40$: tail mass $<n\cdot2^{-40}\approx 10^{-11}$, far below the reported precision.
