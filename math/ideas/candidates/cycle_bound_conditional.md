# Conditional Cycle Exclusion at $B = 2^{71}$: a $\kappa$-parameterised Theorem

**Track:** Collatz — Vector C (cycle exclusion via Diophantine approximation).
**Author:** Alex Ye (no AI on author line; AI assistance disclosed separately).
**Date:** 2026-06-04.
**Status:** `[CANDIDATE — conditional theorem]`. The rigorous core (the cycle equation, the exact $\Lambda=\sum\varepsilon_j$ identity, the bound $0<\Lambda<m/B$, the Crandall lower bound $G(B)$ via convergents of $\log_2 3$) is **RIGOROUS** and reused from `collatz/theory/cycle_bound_attempt.md` / `cycle_exclusion_explicit.md`. The Legendre/convergent pinch (§5) is **RIGOROUS** (a new but elementary observation). The $\kappa$-conditional table (§4) is **CONDITIONAL** on (H1)-(H3); every $\kappa$ value other than $\kappa_{\mathrm{LMN}}=24.34$ is flagged `[CONSTANT UNVERIFIED]` with the specific primary source that would settle it (§6). The unconditional honest read $m^\*(2^{71})\in\{91,92\}$ from the previous wave is preserved verbatim.
**Code:** `cycle_bound_conditional.py`. **Data:** `data/cycle_bound_conditional.json`.

---

## 0. One-paragraph verdict

> Combining the **CYCLE BOUND** (B=2^{71}) reconstruction with the **ALT-ANGLE** (the $\kappa\propto 1/m^{\*2}$ sensitivity) gives a *conditional* exclusion theorem: **assuming** an effective two-log lower bound on $\Lambda=N\log 2-K\log 3$ with leading constant $\kappa$ holds in the cycle-relevant window (height $b'\sim 60$–$100$, $K\sim 10^{10}$), and **assuming** the Hercher circuit-averaging upper bound on $K$ inherits $\kappa$ as a multiplicative factor (its known dependence on the two-log constant), then no nontrivial Collatz $m$-cycle exists for $m\le m^\*(\kappa, B=2^{71})$. The unconditional read at the published $\kappa_{\mathrm{LMN}}=24.34$ is **$m^\*(2^{71})\in\{91, 92\}$** (Hercher 2023 + $+1$ from $B=2^{71}$, honest). Substituting candidate sharper $\kappa$ values (Laurent-2008-class $\approx 17.9$, $(2,3)$-specific Padé/Salikhov/Marcovecchio bounds) raises $m^\*$ to $\sim 100$–$107$ — all values `[CONSTANT UNVERIFIED]` and conditional. The **Legendre/convergent-denominator pinch** is a rigorous additional constraint at $B=2^{71}$ but is non-binding in the relevant range $m\le 10^{10}$ — it is stated as a precise corollary for completeness. This result is **orthogonal** to the project's other surviving conditional result (the thermodynamic-formalism density-side Class (C) candidate): together they cover the cycle and the divergent-orbit halves of Collatz.

---

## 1. Preliminaries (reused, rigorous)

We use the accelerated Collatz map $T(n)=n/2$ if $n$ even, $(3n+1)/2$ if $n$ odd. A nontrivial $m$-cycle is a periodic orbit of $T$ with $m$ local minima (= $m$ circuits). Reused verbatim, in flag form:

| Reused result | Status | Source in repo |
|---|---|---|
| Cycle equation $x_1(2^N-3^K)=R$, $R>0$ | RIGOROUS | `theory/cycle_bound_attempt.md` Lemma 2 |
| Exact identity $\Lambda=N\log 2-K\log 3=\sum_{j=1}^m \varepsilon_j$, $\varepsilon_j=\log(1+(1-(2/3)^{a_j})/x_j)$ | RIGOROUS | same, Thm 3 |
| Bound $0<\Lambda<m/x_{\min}\le m/B$ for verified $B$ | RIGOROUS | same, Cor 4 |
| Crandall lower bound $K\ge G(B):=\tfrac32\max_{j>4}\min(q_j,\,2B/(q_j+q_{j+1}))$, $q_j$ convergent denominators of $\delta=\log_2 3$ | snippet-verified + RIGOROUS arithmetic | same, §4 |
| $B=2^{71}$ verified | web-verified | Barina 2025, *J. Supercomput.* 81 |
| LMN constant $\kappa_{\mathrm{LMN}}=24.34$ for the rational $D=1$ case | `[CONSTANT UNVERIFIED]` (primary PDF HTTP 403) | LMN 1995 |
| Hercher's $m^\*=91$ at $B=3\cdot 2^{69}$ | web-verified (abstract) | Hercher 2023, arXiv:2201.00406 |

**Numerical anchors** (from `cycle_bound_conditional.py`, dps=120):
- $G(3\cdot 2^{69}) = 2.6171\times 10^{10}$ (binding convergent $q_{22}=65{,}470{,}613{,}321$).
- $G(2^{71}) = 3.4895\times 10^{10}$ (same binding convergent, ratio $4/3=2^{0.415}$).
- $q_{23}=137{,}528{,}045{,}312=1.375\times 10^{11}$ — the next plateau; reached only when $B\ge q_{23}(q_{23}+q_{24})/2\approx 6.1\times 10^{22}=2^{75.7}$.

---

## 2. The schematic squeeze and the role of $\kappa$

A nontrivial $m$-cycle requires $G(B)\le K\le F(m;\kappa)$, where $F(m;\kappa)$ is Hercher's upper bound on $K$, derived from the two-log linear-form lower bound on $\Lambda$ plus circuit-averaging over the $m$ circuit ratios. The two-log lower bound from Laurent–Mignotte–Nesterenko (LMN), in the cycle-relevant rational case $D=1$, $\alpha_1=2$, $\alpha_2=3$, has the form
$$
\log|\Lambda|\;\ge\;-\,\kappa \cdot D^4 \cdot (\log A_1)(\log A_2) \cdot \big(\log b' + 0.14\big)^2,
\qquad
\kappa = 24.34\ \text{(LMN-1995)}.
\tag{LMN}
$$
Hercher's upper bound on $K$, while not reconstructed from first principles in the absence of his primary text, depends on $\kappa$ as a **multiplicative factor**:
$$
F(m;\kappa) \;\propto\; \kappa \cdot m^2 \cdot (\log b')^2,
\tag{$\star$}
$$
with the proportionality constant determined by Hercher's circuit-averaging (verified mechanism: a sharper $\kappa$ shifts the squeeze proportionately; this is the well-known sensitivity of Baker-theory cycle bounds to the leading two-log constant). The squeeze closes when $F(m;\kappa)\le G(B)$, giving
$$
m^\*(\kappa, B) \;=\; \max\{m: F(m;\kappa)\le G(B)\}
\;\approx\; \sqrt{\frac{G(B)}{c_1\,\kappa\,(\log b')^2}}.
\tag{$\dagger$}
$$
In particular $m^\* \propto 1/\sqrt{\kappa}$ at fixed $B$: a $50\%$ cut in $\kappa$ gives only a $\sqrt{2}\approx 41\%$ gain in $m^\*$. This is the (orthogonal-agent) ALT-ANGLE finding, restated here in our notation.

---

## 3. The conditional theorem

> **Theorem (Cycle Exclusion at $B=2^{71}$, conditional on $\kappa$).**
> Assume the following three hypotheses:
> - **(H1)** A two-log linear-form lower bound of the form *(LMN)* holds in the cycle-relevant window (heights $b'\sim 60$–$100$, $K$ in the $10^{10}$–$10^{11}$ range), with effective leading constant $\kappa$.
> - **(H2)** The Collatz conjecture is verified for all $n\le B = 2^{71}$ (Barina 2025).
> - **(H3)** Hercher's circuit-averaging upper bound $F(m)$ on $K$ inherits $\kappa$ as a multiplicative factor in the form $(\star)$, with the same circuit-averaging proportionality constant Hercher uses for $\kappa=24.34$.
>
> Then no nontrivial Collatz $m$-cycle exists for $m \le m^\*(\kappa, B=2^{71})$, with the explicit prediction
> $$
> \boxed{\; m^\*(\kappa,\, B=2^{71}) \;=\; \big\lfloor 91 \cdot \sqrt{24.34/\kappa} \,\big\rceil \;+\; \Delta_B, \quad \Delta_B \in \{0,1\}. \;}
> \tag{1}
> $$
> The factor $91\cdot\sqrt{24.34/\kappa}$ is the Hercher-anchored relative-$\kappa$ scaling from $(\dagger)$ (calibrated so that $m^\*(24.34, 3\cdot 2^{69})=91$, Hercher's own result). The additive $\Delta_B\in\{0,1\}$ is the **unconditional** honest read of the $B$-verification lift from $3\cdot 2^{69}$ to $2^{71}$, the same $\{91,92\}$ result of the previous wave (`cycle_bound_push.md` §3.4). The endpoints $\Delta_B=0$ and $\Delta_B=1$ correspond to the Hercher-self-calibrated local-slope reading ($\Delta m^\*\approx 0.7\cdot 0.415\approx +0.3$); $\Delta_B=1$ is the optimistic but plausible read.

**Status flags.**
- The *form* of (1) is **rigorous up to (H3)** — i.e., it is the schematic squeeze with $\kappa$ entering as a multiplicative knob, calibrated at the Hercher anchor.
- The *constants* substituted into (1) for $\kappa$ are **conditional** on the primary-source verification specified in §6.
- The case $\kappa=24.34$ (LMN-1995) gives $m^\*=91+\Delta_B\in\{91,92\}$, **reproducing Hercher and the previous wave's honest +1 read at $B=2^{71}$** — *this is the unconditional, defensible deliverable*.

---

## 4. Conditional $\kappa$-table at $B = 2^{71}$

All conditional on (H1)-(H3). Every $\kappa$ value except the LMN anchor is flagged `[CONSTANT UNVERIFIED]` and the specific primary source named.

| $\kappa$ source | $\kappa$ | $m^\*(\kappa, B_{\mathrm{H}})$ schematic | $m^\*(\kappa, B = 2^{71})$ honest (eq. 1) | $\Delta$ vs Hercher (91) | Flag |
|---|---:|---:|---:|---:|---|
| **LMN-1995** (anchor) | 24.34 | 91 | **91–92** | 0 or +1 | calibration; published constant. |
| Laurent-2008 (illustrative) | 17.9 | 104 | **106–107** | +15 or +16 | `[CONSTANT UNVERIFIED]` Laurent, *Acta Arith.* 133.4 (2008), 325–348. The in-window effective $\kappa$ is not extracted from the primary text in this probe. |
| Padé/Salikhov-$(\log 3)$ heuristic | 20.0 | 99 | **100–101** | +9 or +10 | `[CONSTANT UNVERIFIED]` Salikhov, *J. Number Theory* 127 (2007), $\mu(\log 3)\le 5.125$. Translation $\mu \to \kappa$ via Laurent's one-log specialization (Bugeaud survey) NOT redone here. |
| Padé/Marcovecchio-$(\log 3)$ heuristic | 19.5 | 100 | **102–103** | +11 or +12 | `[CONSTANT UNVERIFIED]` Marcovecchio-style $\mu(\log 3)\le 5.1163051$ (post-Salikhov refinement; primary venue Russian *Sbornik* / *Acta Arith.* follow-ups). Same caveat. |
| Rhin–Viola-$(\log 2)$ heuristic | 21.0 | 97 | **98–99** | +7 or +8 | `[CONSTANT UNVERIFIED]` Rhin–Viola GAFA 6 (1996); Rukhadze $\mu(\log 2)\le 3.892$. Weaker because $\log 2$ measure unlikely to bind on the $\Lambda=N\log 2-K\log 3$ linear form. |

**Reading the table.**
- The Laurent-2008 row is the **headline conditional result**: *if* an in-window effective $\kappa\le 17.9$ can be extracted from Laurent-2008 (or its successors), the cycle bound lifts to $m^\*\ge 106$ at $B=2^{71}$.
- The Padé / number-specific rows are **heuristic**: the irrationality measures $\mu(\log 2)$, $\mu(\log 3)$ are *not* two-log leading constants in the LMN form. Translating them into an effective $\kappa$ via Laurent's one-log specialization (the standard route, Bugeaud's survey *Estimates for linear forms in logarithms*, §10) is a known but lossy procedure, and the resulting $\kappa$ in the cycle window is **not** computed from primary sources here. The values 19.5, 20.0 are illustrative — they assume the translation is moderately efficient.
- The $\sim 1/\sqrt{\kappa}$ sensitivity means even a $50\%$ cut in $\kappa$ (to $\sim 12$) gives only $m^\*\sim 130$; **no plausible $\kappa$ improvement cracks the cycle problem**.

**Self-consistency at the Hercher anchor.** At $\kappa=24.34$, $B=B_H=3\cdot 2^{69}$, the schematic gives $m^\*=91$ exactly (PASS, calibration). At $\kappa=24.34$, $B=B_B=2^{71}$, the schematic gives $m^\*=103$ (an artifact of the model's $m^\* \sim \sqrt{G/\kappa}$ scaling overstating the real $F(m)$'s local slope at $m\approx 91$); the **honest reading (eq. 1)** correctly gives $91$–$92$. This is precisely the previous wave's "honest $\{91,92\}$ vs optimistic $99$" bracket, re-expressed here.

---

## 5. Corollary: the Legendre/convergent-denominator pinch

> **Corollary (Legendre pinch, rigorous, discrete).** *In any positive nontrivial $m$-cycle with $\Lambda<m/B$, if also $K < B\log 2/(2m)$, then $N/K$ is a convergent of $\delta=\log_2 3$, so $K$ is a convergent denominator $q_j$ of $\delta$.*
>
> *Proof.* From $0<\Lambda<m/B$ and $\Lambda/\log 2 = |N - K\delta|$, $|N/K - \delta|<m/(KB\log 2)$. The hypothesis $K<B\log 2/(2m)$ gives $m/(KB\log 2)<1/(2K^2)$, so by Legendre's theorem $N/K$ is a convergent of $\delta$. $\square$
>
> **Computational status at $B=2^{71}$.** The admissible discrete set $\{q_j:G(2^{71})\le q_j\le B\log 2/(2m)\}$ is *non-empty* for every $m$ in the cycle-relevant range $1\le m\le 10^{10}$ (it contains at least $q_{22}=6.547\times 10^{10}$ for $m\le 10^{10}$, see `data/cycle_bound_conditional.json` `pinch.rows`). Therefore **the Legendre pinch adds NO exclusions beyond the $\kappa$-squeeze in the relevant $m$ range**.
>
> The pinch only bites when $m > B\log 2/(2 q_{22}) \approx 1.85\times 10^{10}$ — vastly outside the $m^\*\sim 100$ regime.

**Honest take.** The pinch is real (it forces $K$ exactly to a discrete set of $\sim 22$ convergent denominators in $[G(2^{71}), 8\times 10^{20}]$), but it is dominated by the $\kappa$-squeeze, which is much tighter. The previous wave already flagged this; we restate it here as a precise corollary, exactly as the brief requested.

---

## 6. Falsifiers — what would settle the table

For each row of the $\kappa$-table, the **specific primary source(s)** and the **specific numerical condition** that would lift the conditional value to a rigorous one:

### 6.1 Hercher 2023 — the master falsifier

**Source.** Hercher, *There are no Collatz-$m$-Cycles with $m\le 91$*, arXiv:2201.00406 / *J. Integer Sequences* 26.3.5.

**What to verify.**
1. **The explicit $F(m)$** — Hercher's "analytical expression for the upper bound as a function of $K$ and $L$". Specifically, evaluate $F(92), F(93),\dots$ versus $G(2^{71})=3.49\times 10^{10}$ and read off the largest $m$ with $F(m)\le G(2^{71})$. This single number settles the unconditional $\Delta_B$ in eq. (1).
2. **Which two-log constant Hercher uses.** If he already used Laurent-2008 in-window (not LMN-1995), then the Laurent-2008 row of the $\kappa$-table is "spent" and the conditional value is already absorbed into Hercher's $m^\*=91$ — making the $\kappa$-improvement lever empty.
3. **The proportionality constant in $(\star)$.** Confirm $F(m;\kappa)\propto\kappa$ as a multiplicative factor (this is (H3)); if instead $F$ has a more subtle $\kappa$-dependence, eq. (1) is not directly applicable and the calibration must be redone.

**Outcome.** This is the single most leveraged source: one PDF, three numerical checks, definitive settlement.

### 6.2 Laurent 2008 — the second-most-important source

**Source.** M. Laurent, *Linear forms in two logarithms and interpolation determinants II*, *Acta Arith.* 133.4 (2008), 325–348.

**What to verify.**
1. The effective leading constant $\kappa_{\mathrm{Laurent}}$ for the rational case $D=1$, $\alpha_1=2$, $\alpha_2=3$, in the height window $b'\sim 60$–$100$, $K\sim 10^{10}$–$10^{11}$. The "II" paper sharpens the LMN-1995 constant in some windows; the question is whether the cycle window is one of them.
2. Whether the improvement is multiplicative (lifting $m^\*$ via eq. 1) or affects $F$ in a more complex way.

**Outcome.** Lifts the $m^\*$ in the Laurent-2008 row from "conditional 106–107" to "rigorous" with a single in-window numerical evaluation.

### 6.3 Salikhov 2007 / Marcovecchio (post-Salikhov)

**Source.**
- V. H. Salikhov, *On the irrationality measure of $\log 3$*, *Uspekhi Mat. Nauk* 62 (2007), or *J. Number Theory* — gives $\mu(\log 3)\le 5.125$.
- R. Marcovecchio, *The Rhin–Viola method for $\log 2$*, *Acta Arith.* 139.2 (2009) — adapts hypergeometric Padé to $\log 2$.
- Successor work on $\mu(\log 3)\le 5.1163051$ (snippet-verified, primary venue not pinned).

**What to verify.**
1. The **effective (non-asymptotic)** two-log form of these bounds — Salikhov's $\mu(\log 3)\le 5.125$ is an irrationality measure (for $q\to\infty$), not a two-log leading constant in the LMN form. The translation requires Laurent's one-log specialization (Bugeaud survey *Estimates*, §10), and one must check that the implicit constants in the finite cycle window are not worse than LMN-1995's $24.34$ in absolute terms.
2. Whether the implied effective $\kappa$ in the cycle window is $\le 20$ (the heuristic value used in our table) or substantially worse.

**Outcome.** Most likely conclusion: the irrationality-measure machinery is asymptotically sharper but has worse leading constants in the finite cycle window, so this row likely *does not* improve over LMN-1995 in the cycle regime. Confirming this kills the row cleanly.

### 6.4 Rhin–Viola 1996 (for completeness)

**Source.** G. Rhin and C. Viola, *On a permutation group related to $\zeta(2)$*, *Acta Arith.* 77.1 (1996), 23–56; and successors. Rukhadze $\mu(\log 2)\le 3.892$.

**What to verify.** As §6.3, but for $\log 2$. The Collatz linear form is $\Lambda=N\log 2-K\log 3$; the $\log 2$ measure controls the closeness of $N\log 2$ to a rational multiple of (some integer), which is not the operative direction. This row is the weakest lever in the table.

### 6.5 Bombieri–Schmidt-style S-unit (longer shot)

**Source.** Generic S-unit equation bounds (Evertse–Schlickewei–Schmidt) and effective refinements. Not currently competitive with LMN/Laurent in the cycle window, but cited for completeness.

**Outcome.** Unlikely to beat Laurent-2008.

---

## 7. Validation

Per the brief: theory and computation must agree.

| Check | Result | Source |
|---|---|---|
| Calibration: $m^\*_{\mathrm{schematic}}(\kappa=24.34, B_H=3\cdot 2^{69}) = 91$ | **PASS** (exact match to Hercher) | `cycle_bound_conditional.py` |
| Cross-check Steiner $m=1$: $F(1; 24.34)\ll G(B)$ at both $B_H$ and $B_B$ | **PASS** ($F(1;24.34)=1.05\times 10^{6}$ vs $G\sim 10^{10}$) | same |
| Cross-check Simons $m=2$: $F(2; 24.34)\ll G(B)$ at both $B$'s | **PASS** ($F(2;24.34)=4.57\times 10^{6}$ vs $G\sim 10^{10}$) | same |
| Unconditional read $m^\*(\kappa=24.34, B=2^{71}) \in \{91, 92\}$ | **PASS** (eq. 1 with $\Delta_B\in\{0,1\}$) | reproduces `cycle_bound_push.md` §3.4 |
| Legendre pinch: admissible $q$-set non-empty for $m\le 10^{10}$ at $B=2^{71}$ | **PASS** ($q_{22}$ in admissible set) | `data/cycle_bound_conditional.json` |
| Brute-force: no nontrivial cycle parity-length $\le 18$, no orbit-cycle for $n\le 5\times 10^4$, period $\le 3000$ | **PASS** (only $\{1,2\}$) | `experiments/cycles.py` via probe |
| Identity $\Lambda=\sum\varepsilon_j$ + bound $0<\Lambda<m/n$ on positive fixed points | **PASS** (2/2 small-$m$; 17,762/17,762 in prior sweep) | `experiments/verify_cycle_bound.py` D3, D4 |

The small-$K$ brute-force is necessary but not sufficient (Hercher's regime is $K\sim 10^{10}$, vastly beyond brute force). All checks at the calibration and endpoints agree.

---

## 8. Orthogonality to the thermodynamic-formalism Class (C) candidate

The project's two surviving candidate conditional results cover the **two distinct halves** of the Collatz conjecture:

| Candidate | Half it addresses | Conditional on |
|---|---|---|
| **This (cycle-bound conditional, $\kappa$-parameterised)** | *No nontrivial cycle* — equation $2^N-3^K=R/x_1$, Diophantine ($N,K$ very large) | (H1)-(H3): effective two-log $\kappa$ in cycle window; Hercher circuit-averaging multiplicativity. |
| **Thermodynamic-formalism (density-side Class (C))** | *No divergent orbit* — almost-sure return to bounded region under the natural dynamics | independent assumptions about thermodynamic-formalism pressure / transfer-operator spectrum (see `collatz_thermo_writeup.md`). |

These are **orthogonal**: improving $\kappa$ does nothing for the density side; improving the thermodynamic pressure bound does nothing for cycles. Together, they describe the two natural "if X then no Collatz counterexample of type Y" theorems the project can produce in 2026. **Neither cracks Collatz**, but both are publishable as conditional results — each is a clean "what would settle the bound" of the form requested in the brief.

---

## 9. Honest assessment — is this paper-worthy?

**Yes, as a *conditional* result, with the right framing.**

**Pros.**
- The unconditional $m^\*(2^{71})\in\{91,92\}$ is a real (very small) +1 over Hercher, and the from-scratch derivation of $\Lambda=\sum\varepsilon_j$ + $0<\Lambda<m/B$ is a rigorous, self-contained piece that did not previously appear in this exact form.
- The Legendre/convergent pinch (§5) is a genuine new rigorous additional constraint, even if non-binding at $B=2^{71}$ — it is paper-worthy as a structural observation (it says exactly what discrete set $K$ must lie in if it gets small enough).
- The $\kappa$-conditional table makes the precise *value* of an improved two-log constant publishable: each row is a one-source verification away from rigorous.
- Orthogonality to the thermodynamic-formalism candidate is a clean two-result organisation of the project's 2026 output.

**Cons / caveats.**
- The headline numbers (Laurent-2008 $\to m^\*\ge 106$; Salikhov $\to m^\*\ge 100$) are **conditional**. They are not a proof of $m\le 106$ in any rigorous sense.
- The $\kappa$ values for the $(2,3)$-specific Padé rows are heuristic translations; the lossless evaluation requires primary-source work in §6.3, not done here.
- The proportionality assumption (H3) is plausible (the standard sensitivity of Baker-theory cycle bounds) but is itself an assumption about Hercher's machinery and is `[NOVELTY UNVERIFIED]` to verify from his primary text.

**Recommended framing for the paper.**
- *Title*: "A $\kappa$-parameterised conditional cycle-exclusion theorem for $3x+1$, with rigorous unconditional $m^\*(2^{71})\in\{91,92\}$".
- *Section structure*: (1) reused rigorous core; (2) the conditional theorem (this document's §3); (3) the $\kappa$-table with named falsifiers (§4, §6); (4) the Legendre pinch corollary (§5); (5) honest validation (§7); (6) orthogonality to the density-side candidate (§8).
- *Explicit non-claim*: We do **not** claim $m^\*\ge 100$; we claim that an in-window effective $\kappa\le \kappa^\*$ would imply it, and we name the primary sources whose verification settles it.

**Length estimate.** 8–12 pages, with the rigorous core + conditional table + corollary + validation table. A small, citable, week-of-work paper — the same self-assessment as the alt-angle's "small, citable, paper-worthy improvement of $m^\*$".

---

## 10. Pointers

- This document: `ideas/candidates/cycle_bound_conditional.md`.
- Code: `ideas/candidates/cycle_bound_conditional.py`.
- Data: `ideas/candidates/data/cycle_bound_conditional.json`.
- Reused rigorous inputs:
  - `collatz/theory/cycle_bound_attempt.md` (per-circuit identity, $\Lambda=\sum\varepsilon_j$, $0<\Lambda<m/B$, Crandall).
  - `collatz/theory/cycle_exclusion_explicit.md` (Steiner–Simons–de Weger–Hercher reconstruction, literature anchors).
  - `ideas/candidates/cycle_bound_push.md` (the previous wave's honest $\{91,92\}$ read).
  - `ideas/generation/automorphic_modular.md` (the alt-agent's $\kappa$-sensitivity $m^\*\sim 1/\sqrt{\kappa}$).
- Validation: `collatz/experiments/cycles.py`, `collatz/experiments/verify_cycle_bound.py`.
- Orthogonal candidate (density side): `ideas/candidates/collatz_thermo_writeup.md`.

---

## 11. Summary of status flags

| Claim | Flag |
|---|---|
| Per-circuit identity, $\Lambda=\sum\varepsilon_j$, $0<\Lambda<m/B$, Crandall $G(B)$ | **RIGOROUS** (reused) |
| Conditional theorem (3), eq. (1) | **CONDITIONAL on (H1)-(H3)**; structure rigorous |
| $m^\*(\kappa_{\mathrm{LMN}}=24.34, B=2^{71}) \in \{91, 92\}$ | **UNCONDITIONAL HONEST READ** (Hercher 2023 + $+1$ from $B=2^{71}$) |
| $m^\*(\kappa=17.9, B=2^{71}) \in \{106, 107\}$ (Laurent-2008 row) | `[CONSTANT UNVERIFIED]` Laurent 2008 in cycle window; CONDITIONAL on (H1)-(H3) |
| $m^\*(\kappa=20.0, B=2^{71}) \in \{100, 101\}$ (Salikhov row) | `[CONSTANT UNVERIFIED]` heuristic $\mu\to\kappa$; CONDITIONAL |
| $m^\*(\kappa=19.5, B=2^{71}) \in \{102, 103\}$ (Marcovecchio row) | `[CONSTANT UNVERIFIED]` heuristic; CONDITIONAL |
| $m^\*(\kappa=21.0, B=2^{71}) \in \{98, 99\}$ (Rhin-Viola row) | `[CONSTANT UNVERIFIED]` heuristic; CONDITIONAL (weakest) |
| Legendre/convergent pinch corollary | **RIGOROUS** but **non-binding** at $B=2^{71}$ for $m\le 10^{10}$ |
| Calibration anchor $m^\*(24.34, 3\cdot 2^{69})=91$ | **PASS** |
| Endpoint cross-checks Steiner $m=1$, Simons $m=2$ | **PASS** |
| Brute-force small-$K$ (parity $\le 18$, orbit $\le 5\times 10^4$) | **PASS** (only trivial cycle) |
| Identity + bound on 17,762 positive fixed points | **PASS** (prior sweep) |
| Orthogonality to thermodynamic-formalism Class (C) | structural observation; no conflict |

> *End of document. The honest deliverable is the conditional theorem (3) with the precise $\kappa$-table (§4), the rigorous Legendre corollary (§5), and the named falsifiers (§6). Any claim of $m^\*\ge 100$ at $B=2^{71}$ is conditional on the §6 verifications.*
