# Cycle Bound Push at $B = 2^{71}$: Reconstruction Attempt and Honest Bracket

**Track:** Collatz — Vector C (cycle exclusion via Diophantine approximation).
**Author:** Alex Ye (AI assistance disclosed; not on author line).
**Date:** 2026-06-04.
**Status:** `[CANDIDATE — squeeze-bookkeeping]`. The from-scratch core (per-circuit identity, exact $\Lambda=\sum\varepsilon_j$ identity, the bound $0<\Lambda<m/B$, Crandall lower bound on $K$) is RIGOROUS and reused from `collatz/theory/cycle_bound_attempt.md` (which this builds on). The **upper-bound function $F(m)$ on $K$** — the one missing piece — is **NOT from-scratch reconstructed**; the best I produced are three calibrated/discrete surrogates (§3), each honestly labelled. **Headline conclusion: at $B=2^{71}$ alone (no new $F(m)$ derivation), the honest read is $m^\*\in\{91,92\}$ — i.e. $B=2^{71}$ at best gives $+1$ over Hercher.** All novelty `[NOVELTY UNVERIFIED]`; new bound claims `[PROVISIONAL — needs verification vs Hercher 2023]`.
**Code:** `cycle_bound_push.py`. **Data:** `data/cycle_bound_push.json`.

---

## 0. Verdict (read first)

> **I did not succeed in deriving Hercher's $F(m)$ from first principles.** The prior agent (`theory/cycle_bound_attempt.md`) already localized the gap and proved (Prop 5 there) that the self-contained geometry $\Lambda < m/B$ combined with the two-log linear-form lower bound on $\Lambda$ produces a **lower** bound on $K$ (Crandall side), not an upper bound. I re-confirm this directional finding numerically (§3.1, $K_{\text{LMN-LB}}\approx 1.3$ at every $m$ — vacuous) and add one new rigorous constraint: the **Legendre / convergent-denominator pinch** (§3.2). That pinch is real (it forces $K$ to be exactly a convergent denominator $q_j$ of $\log_2 3$ in the regime $K < B\log 2/(2m)$) but is a **discrete** constraint, not a decaying upper bound. Without Hercher's circuit-averaging argument, I model $F(m)$ as a calibrated power law (§3.3) and report the bracket honestly.
>
> **Squeeze at $B=2^{71}$, all numbers verified by computation in §4–§5:**
> - $G(2^{71}) = 3.4895 \times 10^{10}$ (Crandall lower bound), vs $G(3{\cdot}2^{69}) = 2.6171 \times 10^{10}$ (Hercher). Ratio $4/3 = 2^{0.415}$.
> - Power-law model (calibrated through Simons $F(2)=8.6\times10^4$ and Hercher $F(91)=G(3{\cdot}2^{69})$): $F(m) = c\,m^p$, $p \approx 3.31$. At $B=2^{71}$ this model gives $m^\*=99$. **`[PROVISIONAL — optimistic; the prior agent flagged the same model as unreliable]`.**
> - Hercher-calibrated local-slope model (each doubling of $G$ adds $\approx 0.7$ to $m^\*$; verification alone moved $m^\*$ from $75$ to $82$ over $\sim 10$ doublings of $B$): $\Delta m^\* \approx 0.7 \cdot 0.415 \approx +0.3$, i.e. $m^\*(2^{71}) \in \{91, 92\}$. **This is the honest reading.**
> - Computational validation (small-$K$ side): no nontrivial Collatz cycle exists with parity-period $\le 18$, no orbit-minimum in $[2, 5\times 10^4]$ closes in $\le 3000$ steps, and the from-scratch identity $\Lambda=\sum\varepsilon_j$ + bound $0<\Lambda<m/n$ hold on every reachable positive fixed point.
>
> **Comparison with Hercher's $m \le 91$:** I do **not** confirm a new bound. At best $m^\*(2^{71})=92$ (a +1 push), but this rests on the unverified power-law $F(m)$ extrapolation. The cleanest honest statement is: $B=2^{71}$ moves $G(B)$ by a factor $4/3$, which is $\log_2(4/3) \approx 0.415$ doublings — well short of the $\sim 4.7$ doublings needed to reach the next convergent plateau $q_{23}=1.375\times 10^{11}$. So $B=2^{71}$ alone is **almost certainly not** worth more than $+1$ in $m^\*$.

---

## 1. What is reused (rigorous) and what is at stake

Reused verbatim from `theory/cycle_bound_attempt.md` / `theory/cycle_exclusion_explicit.md`, all flagged in those notes as RIGOROUS or `[CONSTANT UNVERIFIED]` as appropriate:

| Result | Status | Source |
|---|---|---|
| Per-circuit identity $2^{L_j} x_{j+1} = 3^{a_j} x_j + (3^{a_j}-2^{a_j})$ | rigorous | Lemma 1 of `cycle_bound_attempt.md`, D1 PASS |
| Cycle equation $x_1(2^N - 3^K) = R$, $R>0$ | rigorous | Lemma 2 of same, D2 PASS |
| Exact identity $\Lambda = N\log 2 - K\log 3 = \sum_j \varepsilon_j$, $\varepsilon_j = \log(1+(1-(2/3)^{a_j})/x_j)$ | rigorous | Thm 3 of same, D3 PASS to $10^{-120}$ |
| Bound $0 < \Lambda < m/x_{\min} \le m/B$ | rigorous | Cor 4 of same, D4 PASS on 17,762 cases |
| Crandall lower bound $K > \tfrac32 \max_{j>4} \min(q_j, 2B/(q_j+q_{j+1}))$ | snippet-verified + computed | Crandall 1978 (restated); D5 PASS |
| de Weger operative form $\Lambda > 2^{-0.158K}$ for $K\ge 32$ | snippet-verified + numerically reproduced | de Weger / Simons; `verify_cycle_exclusion.py` C5a |
| LMN-1995 leading constant $24.34\,D^4$ for $\log\|\Lambda\| \ge -24.34(\log b'+0.14)^2\log A_1\log A_2$ | `[CONSTANT UNVERIFIED]` | LMN-1995 PDF HTTP 403 |
| $B = 2^{71}$ verified | web-verified | Barina, J. Supercomput. 81 (2025) |

What is **at stake** (the missing piece this candidate tries to push on):

> **The upper-bound function $F(m)$ on $K$.** A from-scratch reconstruction of Hercher's $F(m)$, the upper bound such that $K \le F(m)$ is forced by the cycle's geometry + transcendence, would let us combine $G(B) \le K \le F(m)$ and exclude every $m$ with $F(m) \le G(B)$.

---

## 2. Directional analysis (why the "obvious" reconstruction does not work)

This is the core finding of `theory/cycle_bound_attempt.md` §3 (Prop 5), re-derived here and numerically re-verified, then attempted-to-tighten.

**Setup.** The cycle implies $0 < \Lambda < m/B$ (upper bound on $\Lambda$, Cor 4). The LMN-1995 two-log lower bound (rational case, $D=1$, $\alpha_1=2$, $\alpha_2=3$, $b_1=N$, $b_2=K$, $\log A_1 = 1$, $\log A_2 = \log 3$, $b' = N/\log 3 + K \approx K(1 + \delta/\log 3)$) gives
$$
\log|\Lambda| \;\ge\; -\,24.34\,(\log b' + 0.14)^2 \cdot \log 3,
\qquad \delta = \log_2 3.
$$
For $K$ very large $b' \approx K \cdot 1.86$, so $\log b' \approx \log K + 0.62$.

**Naive squeeze.** $\Lambda$ both $\le m/B$ (cycle) and $\ge \exp(-C(\log K + c_0)^2)$ (LMN) with $C = 24.34\log 3$, $c_0 \approx 0.76$:
$$
\exp(-C(\log K + c_0)^2) \;\le\; \Lambda \;\le\; m/B.
$$
The RHS being smaller than the LHS contradicts cycle existence. So a cycle requires
$$
\exp(-C(\log K+c_0)^2) \;<\; m/B
\;\Longleftrightarrow\;
(\log K + c_0)^2 > \log(B/m)/C
\;\Longleftrightarrow\;
K \;>\; \exp\!\Big(\sqrt{\log(B/m)/C} - c_0\Big).
$$

This is a **lower** bound on $K$, not an upper bound. Numerical values at $B=2^{71}$:

| $m$ | $K_{\text{LMN-LB}}$ from the squeeze above |
|---|---|
| 2  | 1.37 |
| 91 | 1.30 |
| 100 | 1.30 |
| 110 | 1.29 |

Effectively vacuous (Crandall's $G(2^{71}) = 3.49\times 10^{10}$ dominates).

**Why this happens (Prop 5 of `cycle_bound_attempt.md`).** Any LOWER bound $\Lambda \ge \ell(K)$ with $\ell$ decreasing in $K$ (which LMN's is), combined with $\Lambda \le m/B$, gives only $\ell(K) \le m/B$, satisfied for $K$ LARGE. **Hence the upper bound $F(m)$ cannot come from $\Lambda < m/B$ + transcendence alone; it requires a sharper UPPER bound on $\Lambda$ that DECAYS in $K$.** Hercher's $F(m)$ comes from such a sharper bound, derived from circuit-averaging over the $m$ circuit ratios. The published primary text (arXiv:2201.00406; JIS 26.3.5) is HTTP 403 in this environment; I could not reproduce it.

---

## 3. Three concrete $F(m)$ surrogates (rigid → calibrated)

Given the directional obstruction, I offer three concrete $F(m)$ functions of varying status. Numerical values at $B=2^{71}$ are in §4.

### 3.1 (F-LMN, control / null) — the directional control

$F_{\text{LMN}}(m)$ = the $K$ at which the LMN lower bound on $\Lambda$ meets $m/B$, namely
$$
F_{\text{LMN}}(m) \;=\; \exp\!\Big(\sqrt{\log(B/m)/C} - c_0\Big),
\quad C = 24.34 \log 3,\; c_0 \approx 0.76.
$$
By §2, this is a **lower** bound on $K$, *not* an upper bound. **It does not exclude any $m$.** I report it only as a null-result control that confirms the directional analysis (values $\approx 1.3$ in the table, dwarfed by $G(2^{71})$).

### 3.2 (F-conv, rigorous discrete) — Legendre's convergent-denominator pinch

This is the **one new rigorous additional pinch** I can produce.

**Claim (rigorous).** *In any positive nontrivial $m$-cycle with $\Lambda < m/B$, if also $K < B\log 2 /(2m)$, then $N/K$ is a convergent of $\delta = \log_2 3$, so $K$ is a convergent denominator $q_j$ of $\delta$.*

*Proof.* $\Lambda/\log 2 = |N - K\delta|$. By Cor 4, $\Lambda/\log 2 < m/(B\log 2)$. So $|N/K - \delta| < m/(K B \log 2)$. The hypothesis $K < B\log 2/(2m)$ gives $m/(KB\log 2) < 1/(2K^2)$, hence $|N/K - \delta| < 1/(2K^2)$, so by Legendre's theorem ([standard]) $N/K$ is a convergent of $\delta$. $\square$

**Application.** Combine with Crandall: $K \ge G(B)$ AND $K = q_j$ for some convergent denominator AND $K < B\log 2/(2m)$. The cycle is forced into the discrete set
$$
F_{\text{conv}}(B, m) \;:=\; \{q_j : G(B) \le q_j \le B\log 2/(2m)\}.
$$
If this set is **empty**, no cycle. Numerical: at $B=2^{71}$, $G(2^{71}) = 3.49 \times 10^{10}$, so the smallest admissible convergent denominator is $q_{22} = 6.547 \times 10^{10}$. For $m=91$, the upper end is $B\log 2/(2m) \approx 8.99 \times 10^{18}$, vastly larger than $q_{22}$ — so the set is nonempty (in fact contains $q_{22}, q_{23}, \dots, q_{26}$), and this argument alone excludes nothing. The pinch only bites at much smaller $B$ or vastly larger $m$.

**Honest read:** $F_{\text{conv}}$ is rigorous and is, to my knowledge, **not** how Hercher gets his $F(m)$ — Hercher's $F(m)$ is a continuous upper bound on $K$, not a discrete constraint. So $F_{\text{conv}}$ is a complementary, mild constraint that does not exclude any $m$ at $B=2^{71}$. It is reported for transparency. **`[NOVELTY UNVERIFIED]`** — Legendre + the cycle Diophantine bound is elementary, and this observation is plausibly folklore.

### 3.3 (F-power, calibrated / provisional) — the power-law model

$F_{\text{power}}(m) = c\, m^p$ pinned through the two anchors **(verified literature)**:
- Simons 2005 gives $F(2) \approx 8.6 \times 10^4$ (§4.2 of `cycle_exclusion_explicit.md`, verified).
- Hercher 2023's $m^\* = 91$ at $B=3{\cdot}2^{69}$ implies $F(91) \approx G(3{\cdot}2^{69}) = 2.62 \times 10^{10}$ (i.e. Hercher's $F(91)$ is just at the Crandall threshold).

Fit: $p = \log(2.62\times 10^{10}/8.6\times 10^4)/\log(91/2) \approx 3.31$, $c = 8.6\times 10^4 / 2^{3.31} \approx 8.7\times 10^3$.

By construction, $m^\*_{\text{power}}(B = 3{\cdot}2^{69}) = 91$ (self-consistency PASS, see `cycle_bound_push.py` output).

**At $B=2^{71}$, $G=3.49\times 10^{10}$, this gives $m^\*_{\text{power}}(2^{71}) = 99$.** This is the **optimistic** end of the bracket. The prior agent (`cycle_bound_attempt.md` §6) flagged this same model as unreliable.

**Why it is `[PROVISIONAL]`.** A pure power-law fit through two points spanning $m\in\{2,91\}$ is a $K$-extrapolation across the LMN regime change. The true Hercher $F(m)$ likely has subexponential corrections in $m$ that make the local slope at $m\approx 91$ much smaller than the global $p \approx 3.31$. The Hercher-calibrated local-slope model (next) gives the honest read.

### 3.4 (F-Hercher-local, calibrated to Hercher's own data) — the conservative bracket

From Hercher's abstract: *"Simons–de Weger proved $m \ge 76$. With newer bounds … one gets $m \ge 83$. In this paper we prove $m \ge 92$."* The verification-only step ($m^\* = 75 \to 82$) corresponds to roughly $10$ doublings of $B$ (from $\sim 2^{58}$ to $\sim 2^{68}$), so $+7$ in $m^\*$ over $10$ doublings is $\Delta m^\*/\text{doubling}(G) \approx 0.7$.

Barina's $2^{71}$ over Hercher's $3{\cdot}2^{69}$ is $\log_2(G(2^{71})/G(3{\cdot}2^{69})) = \log_2(4/3) = 0.415$ doublings. So
$$
\Delta m^\* \;\approx\; 0.7 \times 0.415 \;\approx\; +0.3,
\quad\text{i.e.}\quad
m^\*(2^{71}) \in \{91, 92\}.
$$

**This is the honest, Hercher-self-calibrated reading.** It says: $B=2^{71}$ at best gives $+1$ in $m^\*$, and even that requires Hercher's $F(92)$ to be only marginally above his $G(3{\cdot}2^{69})$.

---

## 4. The squeeze, numerically, at $B = 2^{71}$

Computed by `cycle_bound_push.py` (mpmath, dps=120):

```
At B = 2^71, G = 3.4895e+10:
   m   F_power     F-power<=G?  F_conv          pinch_upper     K_lmn_LB
   2   86000       True         65470613321     4.09e+20        1.369
   5   1.78e+06    True         65470613321     1.64e+20        1.351
  10   1.76e+07    True         65470613321     8.18e+19        1.338
  20   1.74e+08    True         65470613321     4.09e+19        1.325
  50   3.61e+09    True         65470613321     1.64e+19        1.308
  75   1.38e+10    True         65470613321     1.09e+19        1.300
  82   1.85e+10    True         65470613321     9.98e+18        1.299
  91   2.62e+10    True         65470613321     8.99e+18        1.297
  92   2.71e+10    True         65470613321     8.89e+18        1.297
  93   2.81e+10    True         65470613321     8.80e+18        1.296
  95   3.02e+10    True         65470613321     8.61e+18        1.296
  99   3.46e+10    True         65470613321     8.27e+18        1.295
 100   3.58e+10    False        65470613321     8.18e+18        1.295
 110   4.90e+10    False        65470613321     7.44e+18        1.293

m*_power (largest m with F_power(m) <= G(2^71))    = 99       [PROVISIONAL, optimistic]
m*_local (Hercher-self-calibrated, Δm* ≈ +0.3)     = 91-92    [honest read]
m*_LMN  (LMN-only direction control)               = 0        (wrong direction)
m*_conv (Legendre pinch alone)                     = 0        (regime-non-empty at B=2^71)
```

**Self-consistency at $B = 3{\cdot}2^{69}$.** The power-law model gives $m^\*(3{\cdot}2^{69}) = 91$ by construction (PASS, see code output).

**Why $F_{\text{conv}}$ is constant ($q_{22}$) across all $m$:** the smallest convergent $\ge G(2^{71})$ is $q_{22}$ for every $m$ in this range; the pinch upper-end $B\log 2/(2m)$ stays $\gg q_{22}$ until $m \gtrsim B/(2 q_{22}\log 2) \approx 1.5 \times 10^{10}$ (vastly outside the regime of interest).

---

## 5. Computational validation (small-$K$ side)

Per the brief: theory and computation must agree where feasible. The brute-force side validates the small-$K$ end.

`cycle_bound_push.py` runs (or re-uses `experiments/cycles.py`):

1. **Parity-length brute force, $L \le 18$.** All $\sum_{m=2}^{18}\binom{m}{k_{\text{adm}}}$ parity sequences with $2^m > 3^k$ examined; no nontrivial positive cycle found (only the trivial $\{1,2\}$). Total ~$10^5$ sequences.
2. **Orbit-elemental brute force, $n \in [2, 5\times 10^4]$, period $\le 3000$.** No cycle found other than $\{1,2\}$.
3. **Bound consistency on positive fixed points.** The from-scratch identity $\Lambda = \sum_j \varepsilon_j$ and the rigorous bound $0 < \Lambda < m/n$ hold on every reachable positive fixed point (2/2 in this short run; 17,762/17,762 in the prior `verify_cycle_bound.py` D4 sweep). PASS.

**Limitations:** Hercher's $F(m) \approx 10^{10}$–$10^{11}$ is astronomically beyond brute-force range ($K=20$ vs $K=10^{10}$). Brute force can only validate the small-$K$ end (necessary, not sufficient).

---

## 6. Comparison with Hercher's $m \le 91$ — honest, item-by-item

| Question | Answer | Confidence |
|---|---|---|
| Did I reproduce Hercher's $F(m)$ from first principles? | **No.** The directional obstruction (Prop 5 of `cycle_bound_attempt.md`, §2 here) shows the self-contained geometry $\Lambda<m/B$ + LMN gives only a lower bound on $K$. Hercher's $F(m)$ requires his circuit-averaging argument, which I could not extract without his primary text (HTTP 403). | High (the directional finding is rigorous; the extraction failure is environment-imposed, not a math finding). |
| Did I push past $m=91$? | **No, not rigorously.** Best PROVISIONAL gain: $+1$ to $m^\*=92$ at $B=2^{71}$, under the Hercher-self-calibrated local-slope model. The optimistic power-law gives $m^\*=99$ but is unreliable (the prior agent's same finding). | Low (depends on Hercher's exact $F(m)$). |
| Does my $F(m)$ at $m=92$ "nearly exclude"? | The power-law $F_{\text{power}}(92) = 2.71\times 10^{10}$ vs $G(2^{71}) = 3.49\times 10^{10}$ — a comfortable margin of ~28%. Under power-law, even $m=99$ excludes ($F_{\text{power}}(99) = 3.46\times 10^{10}$, just under $G$). | Provisional. |
| If $F(m)$ strictly weaker than Hercher's, what am I missing? | The **decaying upper bound on $\Lambda$** that Hercher derives from circuit-averaging over the $m$ circuit ratios (the "bounds on averages and on sums of an arbitrary number of terms" of his abstract). I sketched the algebra (per-circuit identity → $R \le 3^K \sum_{j} \prod_{i<j} r_i$ with $r_i = 2^{L_i}/3^{a_i}$, $\prod r_i = e^\Lambda$) but could not get a $K$-decaying bound without a primary-source inequality I'm missing. | High. The missing step is precisely the one flagged in `cycle_bound_attempt.md` §3. |
| Is the $m^\*=92$ claim verified against Hercher? | **No.** It rests on the power-law extrapolation pinned at his $m=91$ anchor. To confirm or refute, one needs Hercher's $F(92)$ vs $G(2^{71})=3.49\times 10^{10}$: if $F(92) \le 3.49\times 10^{10}$, then yes; otherwise no. The Hercher-self-calibrated reading ($\Delta m^\*\approx +0.3$) suggests it is on the knife edge. | High that this needs primary-source check. |

> ### `[PROVISIONAL — needs verification vs Hercher 2023 primary source]`
> Any claim of $m^\* \ge 92$ at $B=2^{71}$ is provisional and rests on a *model* of $F(m)$, not a from-scratch derivation. The strict, defensible deliverable of this candidate is:
> - **Confirmation** of the prior agent's directional finding (Prop 5): self-contained geometry $+ $ LMN does not produce $F(m)$.
> - **One new rigorous discrete pinch** (§3.2, Legendre/convergent-denominator constraint) — does not exclude $m$ at $B=2^{71}$ but is a real additional constraint.
> - **Honest bracket**: $m^\*(2^{71}) \in \{91, 92\}$ (Hercher-calibrated) up to $99$ (optimistic power-law). The honest reading is **+1 over Hercher, at best**.
>
> **`[CONSTANT UNVERIFIED]` LMN-1995 leading constant $24.34\,D^4$**: primary PDF HTTP 403; the constant appears in multiple secondary snippets (Simons's application, Bugeaud's survey, Evertse's Leiden notes). Whether Laurent-2008 gives a sharper constant in the relevant regime is **not resolved here**; if so, that is an *independent* lever, but Hercher may have used it already (also unknown).

---

## 7. Sharper levers — Laurent 2008 and circuit-averaging

**Laurent 2008** (Acta Arith. 133.4): claims a sharper two-log constant than LMN-1995 in some regimes. WebSearch hits confirm the existence of the paper but **could not extract a sharper numerical constant in the cycle regime** (`[CONSTANT UNVERIFIED]`). If Hercher already used Laurent-2008's constant, no new gain from this lever. If he used LMN-1995's $24.34$, plugging in Laurent's improved constant might give a sub-multiplicative reduction in the LMN-derived $F(m)$, plausibly $\Delta m^\* = +1$ further (informed guess; not verified).

**Circuit-averaging** is the heart of the Hercher gain over Simons-de Weger ($+16$ from $m^\*=75$ to $91$). I attempted to reproduce it (sketched §6 above and in `cycle_bound_attempt.md` §3) and failed: the cleanest algebraic upper bound on $R = \sum_j d_j 3^{P_j} 2^{N-Q_j}$ collapses to $R < 3^K \cdot $ (geometric-mean-like quantity that does not decay in $K$). Further progress on this lever requires Hercher's PDF.

---

## 8. What would actually push past $91$ (concrete asks)

1. **Hercher's $F(92)$.** If $F(92) \le 3.49\times 10^{10} = G(2^{71})$, then $m^\*=92$ is rigorous at $B=2^{71}$. The single most important number to extract from the Hercher PDF.
2. **Hercher's $F(93), F(94), \dots$** to bracket the actual $m^\*(2^{71})$ in the range $\{92, \dots, 99\}$.
3. **Laurent-2008 constant** for the two-log $\log A_1=1, \log A_2=\log 3$, $b' \sim 10^{11}$ regime, vs LMN-1995's $24.34$.
4. **The next Collatz verification record** beyond $2^{71}$. The Crandall plateau $q_{23} = 1.375\times 10^{11}$ requires $B \ge q_{23}(q_{23}+q_{24})/2 \approx 6.1\times 10^{22} = 2^{75.7}$; Barina is at $2^{71}$, so $\sim 4.7$ more doublings needed. That's a $\sim 25\times$ verification push.

---

## 9. Pointers

- This document: `ideas/candidates/cycle_bound_push.md`.
- Code: `ideas/candidates/cycle_bound_push.py`.
- Data: `ideas/candidates/data/cycle_bound_push.json`.
- Inputs (rigorous, reused): `collatz/theory/cycle_bound_attempt.md` (from-scratch identity + $\Lambda$ bound + Prop 5), `collatz/theory/cycle_exclusion_explicit.md` (Simons-de Weger-Hercher reconstruction + literature anchors).
- Brute-force toolkit: `collatz/experiments/cycles.py` (parity, orbit, circuit-decomposition, bound-consistency).
- Validation: `collatz/experiments/verify_cycle_bound.py` (D1-D6 PASS); `collatz/experiments/verify_cycle_exclusion.py` (C1-C5b PASS).
- Survey: `collatz/literature/survey.md` §7 (cycle exclusion family).

---

## 10. Summary of status flags

| Claim | Flag |
|---|---|
| Per-circuit identity, $\Lambda = \sum\varepsilon_j$, $0 < \Lambda < m/B$ | RIGOROUS (reused) |
| Crandall lower bound $G(2^{71}) = 3.49\times 10^{10}$ | RIGOROUS (computed; Crandall snippet-verified) |
| Directional obstruction: $\Lambda < m/B$ + LMN $\Rightarrow$ lower bound on $K$ only | RIGOROUS (Prop 5, reproduced) |
| Legendre / convergent-denominator pinch (§3.2) | RIGOROUS, `[NOVELTY UNVERIFIED]`, weak at $B=2^{71}$ |
| Power-law model $F(m) = c m^p$ | `[PROVISIONAL]`, optimistic |
| Hercher-self-calibrated $\Delta m^\* \approx +0.3$ | `[PROVISIONAL]`, conservative; honest read |
| $m^\*(2^{71}) \in \{91,92\}$ (honest) up to $99$ (optimistic) | `[PROVISIONAL — needs Hercher 2023 primary source]` |
| Computational validation for small $K$ (parity $\le 18$, orbit $\le 5\times 10^4$) | PASS, but small-$K$ side only |
| LMN constant $24.34\,D^4$ | `[CONSTANT UNVERIFIED]` |
| Laurent-2008 improved constant | `[CONSTANT UNVERIFIED]`; status vs Hercher unknown |
| $B = 2^{71}$ Barina 2025 | web-verified |
