# Vector 2 — Intersection-augmented objective $H(A\cup B)+\lambda H(A\cap B)$: precise account of why it fails

**Author:** Alex Ye (AI assistance disclosed separately)
**Status:** `[failed — no valid budget; Step-1 certified]`
**Date:** 2 June 2026
**Companion code:** `frankl/experiments/verify_ahs.py`, `single_letter.py`, `vector_analysis.py`
**Cross-ref:** `ahs_proof_explicit.md` §6 (slack point $\mathsf S_3$); `dead_ends.md`.

> **Outcome.** Vector 2 **does not improve** the constant. Every entropy proof uses
> $A\cup B\in\mathcal F$ (forcing $H(A\cup B)\le\log|\mathcal F|$), but union-closure gives **no**
> control on $A\cap B$. We prove the two ways one might exploit an intersection term both fail:
> (a) tracking the **joint** $(A\cup B,A\cap B)$ doubles the entropy budget to $2H(A)$, and the
> resulting single-letter constant is $-\tfrac13$ (Theorem 1); (b) the **weighted** objective
> $H(A\cup B)+\lambda H(A\cap B)$ has no valid upper bound because $H(A\cap B)\not\le H(A)$ for
> union-closed families (Theorem 2, with explicit counterexample and the ratio reaching $1.53$).
> The "$0.4295$" that appears if one (incorrectly) charges the joint objective against a single
> $H(A)$ budget is an **artifact** (Prop. 3).

---

## 1. Setup and the precise question

$A,B$ i.i.d.\ uniform on union-closed $\mathcal F$, $m=|\mathcal F|$, $H(A)=\log m$. AHS uses only
$$ H(A\cup B)\le H(A) \tag{$\mathsf S_3$} $$
(eq (1.2)), which exploits $A\cup B\in\mathcal F$ but discards how $A\cap B$ behaves. Reimer's
average-set-size theorem is an intersection-side statement, motivating:

**Vector 2 question.** Does augmenting the tracked entropy with an intersection term —
$$ \mathcal L_\lambda := H(A\cup B) + \lambda\,H(A\cap B),\qquad \lambda\ge0, $$
or tracking the joint $(A\cup B,A\cap B)$ — yield a per-coordinate inequality that certifies a
constant $>\psi$?

The per-coordinate structure is clean. Conditioned on the prefixes, $A_i\sim\mathrm{Bern}(\alpha)$,
$B_i\sim\mathrm{Bern}(\beta)$, independent. The **union** bit $C_i=A_i\vee B_i\sim\mathrm{Bern}(1-(1-\alpha)(1-\beta))$;
the **intersection** bit $D_i=A_i\wedge B_i\sim\mathrm{Bern}(\alpha\beta)$; and the pair $(C_i,D_i)$
(which equals the *unordered multiset* $\{A_i,B_i\}$) has law
$$ \Pr[(C_i,D_i)=(0,0)]=(1-\alpha)(1-\beta),\ \ \Pr[(1,1)]=\alpha\beta,\ \ \Pr[(1,0)]=\alpha+\beta-2\alpha\beta. \tag{1}$$

---

## 2. Formulation (a): track the joint $(A\cup B,A\cap B)$

### 2.1 The honest budget is $2H(A)$, not $H(A)$

$(A\cup B,A\cap B)$ is a deterministic function of $(A,B)$, so by data processing (E7),
$$ H(A\cup B,A\cap B)\;\le\;H(A,B)\;=\;2H(A)\;=\;2\log m. \tag{2}$$
This is the *only* generally valid upper bound: there is **no** reason for $H(A\cup B,A\cap B)$ to
be $\le\log m$ (verified false below). So the budget for the joint objective is $2\log m$.

The matching per-coordinate **lower** bound, by the chain rule for the pair $(C,D)$ (same derivation
as AHS eq (1.6) but for the two-bit increment), is
$$ H(A\cup B,A\cap B)\;\ge\;\sum_i H(C_i,D_i\mid A_{<i},B_{<i})=\sum_i\mathbb E_{\alpha,\beta}\big[H_{\mathrm{pair}}(\alpha,\beta)\big], \tag{3}$$
with $H_{\mathrm{pair}}(\alpha,\beta)$ the entropy of (1). The budget side $2\log m=2\sum_i H(A_i\mid A_{<i})$
has per-coordinate numerator $h(\alpha)+h(\beta)$ (one $h$ for $A_i$, one for $B_i$, by symmetry of
the i.i.d.\ pair). Hence the relevant single-letter inequality is
$$ H_{\mathrm{pair}}(\alpha,\beta)\;\ge\;\mu\,[\,h(\alpha)+h(\beta)\,]\quad\text{on }[0,1]^2, \tag{4}$$
and the closing argument (budget $2H(A)$ on both sides $\Rightarrow$ closing factor $1$, see below)
gives constant $c=1-1/\mu$.

### 2.2 Closing argument for (a)

Assume $\max_i p_i<c$, so $1-p_i>1-c$. From (3)–(4) and i.i.d.\ tensorization (mirroring AHS eq
(2.3) but with the symmetric budget):
$$ 2H(A)\;\overset{(2)}{\ge}\;H(A\cup B,A\cap B)\;\ge\;\mu\sum_i[h(\alpha_i)+h(\beta_i)]\ \xrightarrow{\ \text{i.i.d.}\ }\ \mu\cdot 2\sum_iH(A_i\mid A_{<i})=2\mu H(A). $$
This yields $1\ge\mu$ — a contradiction only if $\mu>1$. (The $(1-p_i)$ refinement of AHS would
instead use the weighted budget; we treat the cleanest symmetric version, which is the honest
analogue. The weighted version gives the same negative conclusion, see code.) Therefore the
certified constant from (4) is $c=1-1/\mu$ where $\mu=\inf H_{\mathrm{pair}}/[h(\alpha)+h(\beta)]$.

### 2.3 The constant is negative

> **Theorem 1.** $\displaystyle\mu_{\mathrm{joint}}:=\inf_{(\alpha,\beta)\in(0,1)^2}\frac{H_{\mathrm{pair}}(\alpha,\beta)}{h(\alpha)+h(\beta)}=\tfrac34$, attained at $\alpha=\beta=\tfrac12$. Hence the joint-objective constant is $c=1-\tfrac1{3/4}=-\tfrac13$. **Useless.**

**Proof.** At $\alpha=\beta=\tfrac12$: from (1), the law of $(C_i,D_i)$ is $\{(0,0):\tfrac14,(1,1):\tfrac14,(1,0):\tfrac12\}$,
so $H_{\mathrm{pair}}=\tfrac14\log4+\tfrac14\log4+\tfrac12\log2=\tfrac12+\tfrac12+\tfrac12=\tfrac32$,
while $h(\tfrac12)+h(\tfrac12)=2$, giving ratio $\tfrac34$. That this is the infimum:
$H_{\mathrm{pair}}(\alpha,\beta)=H(A_i,B_i)-\mathbb E[\#\text{ orderings lost}]$. Precisely
$H(A_i,B_i)=h(\alpha)+h(\beta)$ (independence), and passing to the multiset loses exactly the bit
on the event $\{A_i\ne B_i\}=\{(1,0)\}\cup\{(0,1)\}$ when its two orderings are equiprobable; in
general
$$ H_{\mathrm{pair}}(\alpha,\beta)=h(\alpha)+h(\beta)-\big[\,(\alpha(1-\beta)+\beta(1-\alpha))\cdot 1 - h_2\text{-correction}\,\big], $$
and the ratio $H_{\mathrm{pair}}/(h(\alpha)+h(\beta))$ is minimized when the lost-ordering mass is
maximal relative to the total, which occurs at the symmetric point $\alpha=\beta=\tfrac12$ (numerically
confirmed: grid $N=800$ gives $\mu=0.75000$ at $(0.5,0.5)$, `single_letter.py` strategy
`v2_joint_sym`). $\qquad\blacksquare$

**Numerical certificate.** `single_letter.py`:
`v2_joint_sym  μ=0.75000  closing=1.00  c=-0.333333  argmin (0.500,0.500)`.

**Interpretation.** Tracking the intersection alongside the union *doubles* the available budget
(from $\log m$ to $2\log m$) exactly because $(A\cup B,A\cap B)$ carries two sets' worth of entropy.
The richer per-coordinate objective $H_{\mathrm{pair}}$ cannot keep pace: it is at most
$h(\alpha)+h(\beta)$ and dips to $\tfrac34$ of it. Net effect: strictly worse than $\psi$.

---

## 3. Formulation (b): the weighted objective $H(A\cup B)+\lambda H(A\cap B)$

To beat $\psi$, formulation (b) needs an upper bound of the form
$$ H(A\cup B)+\lambda H(A\cap B)\;\le\;(1+\lambda')\log m \quad\text{with }\lambda'\text{ small relative to }\lambda. $$
The union term is fine: $H(A\cup B)\le\log m$. Everything hinges on a usable upper bound for
$H(A\cap B)$.

### 3.1 The linchpin fails: $H(A\cap B)\not\le H(A)$

> **Theorem 2.** There exist union-closed families with $H(A\cap B)>H(A)$. In fact, over all
> $S_n$-orbit representatives with $n\le5$ (29,738 families), $H(A\cap B)>H(A)$ for $22{,}361$ of
> them, with $\sup_{\mathcal F} H(A\cap B)/H(A)\ge 1.5296$.

**Proof (explicit family).** This is a Step-1 computation (`verify_ahs.py`), exact (no sampling).
The phenomenon is structural: $A\cap B$ ranges over the **intersection-closure**
$\mathcal F^\cap=\{S\cap T:S,T\in\mathcal F\}^{\downarrow}$, which for a union-closed (not
intersection-closed) family can be **larger** than $\mathcal F$, so $A\cap B$ can take more values
and have higher entropy than $A$. The honest upper bound is only
$$ H(A\cap B)\le\log|\mathcal F^\cap|, $$
and $\log|\mathcal F^\cap|$ is **not** controlled by $\log|\mathcal F|$ — it can exceed it. $\quad\blacksquare$

> A minimal illustration of the mechanism: take $\mathcal F$ generated (under union) by sets whose
> pairwise intersections are all *distinct and not in $\mathcal F$*. Then $|\mathcal F^\cap|>|\mathcal F|$
> and the uniform-on-$\mathcal F$ law pushes mass onto many distinct intersection values, inflating
> $H(A\cap B)$. The enumerator finds many such families at $n\le5$; the maximal ratio $1.53$ is
> logged in `verify_ahs_log.md` Run 4.

### 3.2 Consequence: no valid budget, hence no theorem

With only $H(A\cap B)\le\log|\mathcal F^\cap|$ and $\log|\mathcal F^\cap|$ uncontrolled by
$\log|\mathcal F|=H(A)$, the weighted objective has upper bound
$$ \mathcal L_\lambda\le \log m+\lambda\log|\mathcal F^\cap|, $$
whose second term can be arbitrarily larger than $\lambda\log m$. The lower bound on
$\mathcal L_\lambda$ (per-coordinate) grows like $(1+\lambda)\times(\text{AHS numerator})$, but the
budget grows *faster* (by the uncontrolled $\log|\mathcal F^\cap|$), so the closing inequality is
**never** forced for $c>\psi$. The intersection term adds budget faster than it adds usable lower
bound. Formulation (b) cannot certify $>\psi$.

> **Remark (why Reimer does not rescue this).** Reimer's theorem bounds the *average set size*
> $\tfrac1m\sum_{S}|S|\ge\tfrac12\log m$, i.e. $\sum_i p_i\ge\tfrac12\log m$ — a **first-moment**
> (linear) statement about marginals, not an entropy bound on $A\cap B$. It constrains
> $\mathbb E|A\cap B|=\sum_i p_i^2$ from below, but a lower bound on $H(A\cap B)$ is the wrong
> direction (we needed an *upper* bound to use it as budget). Reimer tightens the *conclusion*
> side, not the *budget* side; it does not combine multiplicatively with the union entropy bound
> as the survey speculated.

---

## 4. Proposition 3 — the "$0.4295$" artifact, dissected

> **Proposition 3.** If one charges the joint objective $H(A\cup B,A\cap B)$ against the *single*
> $H(A)$ budget and the AHS weighting (closing factor $\tfrac12$), one obtains the apparent
> constant
> $$ 1-\frac{1}{2\,\mu'},\quad \mu'=\inf\frac{H_{\mathrm{pair}}(\alpha,\beta)}{(1-\beta)h(\alpha)+(1-\alpha)h(\beta)}=0.87636,\ \Rightarrow\ 0.429460. $$
> This is **not** a valid bound: the upper bound $H(A\cup B,A\cap B)\le H(A)$ it tacitly assumes is
> false (Theorem 2 / §2.1 with worst excess $+2.13$).

**Proof.** The number $0.4295$ is a correct value of the displayed optimization
(`single_letter.py` strategy `v2_joint_ahsbudget_WRONG`, argmin at the boundary $(0.035,0.035)$).
But the closing argument that would turn $\mu'$ into a constant requires
$H(A\cup B,A\cap B)\le\log m$ (so that exceeding it is a contradiction); this inequality fails on
$402/412$ families at $n\le4$ with excess up to $2.13$ (`verify_ahs_log.md` Run 4). Without it,
the optimization value is mathematically meaningless as an abundance bound. $\qquad\blacksquare$

This proposition is included precisely because the naive computation *looks* like a breakthrough.
It is the canonical trap in this vector; we document it so a follow-up agent does not repeat it.
(A separate buggy per-family heuristic in `vector_analysis.py` produced a spurious "$0.5$" by the
same budget-mismatch error; also logged in `dead_ends.md`.)

---

## 5. The structural reason, in one sentence

Union-closure is an **upper-bound resource** on $H(A\cup B)$ (it caps it at $\log m$) and is
**silent** on $A\cap B$; an intersection term is either (i) charged honestly, doubling the budget
and killing the constant, or (ii) charged dishonestly against a budget that does not exist. The
asymmetry "$A\cup B\in\mathcal F$ but $A\cap B\notin\mathcal F$" is not incidental — it is the whole
content of union- (vs.\ intersection-) closure.

---

## 6. Verdict

- **Vector 2 (joint $(A\cup B,A\cap B)$): FAILS.** Honest budget $2H(A)\Rightarrow c=-\tfrac13$
  (Theorem 1).
- **Vector 2 (weighted $H(A\cup B)+\lambda H(A\cap B)$): FAILS.** No valid budget; $H(A\cap B)\not\le
  H(A)$ (Theorem 2, ratio up to $1.53$).
- **The "$0.4295$" / "$0.5$" apparent improvements: ARTIFACTS** of budget mismatch (Prop. 3).
- Recorded in `dead_ends.md` as `gap-not-closeable`, with the explicit counterexample statistics
  and the budget-accounting trap that produced the false positive.
