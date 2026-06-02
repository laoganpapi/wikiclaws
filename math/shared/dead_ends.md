# Dead Ends — Approaches That Did Not Work

**Project:** Collatz + Frankl research project
**Authors:** Alex Ye with Claude
**Purpose:** Record every approach that we tried and that failed (computationally falsified, found in the prior literature as already-defeated, proven impossible, or abandoned after time-boxed effort).

Agents must read this file before launching a new attack vector to avoid re-doing failed work. Agents must append to this file whenever an approach fails the verification protocol or is otherwise abandoned.

This file is part of the project's honesty discipline: negative results are valuable. Recording them protects us and others from wasted cycles.

---

## How to add an entry

Append a new H2 section with the template below. Entries are append-only; do not delete or edit prior entries (correct earlier mistakes only by adding a follow-up entry that references the earlier one).

```
## YYYY-MM-DD — [track: collatz|frankl|cross] — [short descriptive title]

**Agent / author:** [agent name and/or Alex Ye]
**Time invested:** [e.g., 4 hours of compute / 2 days of theory]
**Attack vector:** [one paragraph: what was the plan]
**Why it failed:** [one to three paragraphs: the specific obstruction, with line/file references to the failed attempt]
**Counter-example (if any):** [explicit input where the claim/method breaks, or "n/a"]
**Pointer to artifacts:** [files in track/ subdirs that show the failed work]
**Verdict:** [one of: falsified, prior-art, computationally infeasible, gap-not-closeable, abandoned]
**Lesson:** [what we learned that informs future attacks]
```

---

## Entries

## 2026-06-02 — [collatz] — Cycle exclusion (Vector C): three dead ends — see `collatz/theory/dead_ends.md`

**Agent / author:** Alex Ye (AI-assisted).
**Time invested:** ~4 hours theory + source verification.
**Attack vector:** Improve Hercher's $m\le 91$ cycle-exclusion bound, per Vector C.
**Why it failed (summary; full entries in `collatz/theory/dead_ends.md`):**
1. *Improving $\mu(\log_2 3)$ is not the route* — the published proofs do not use the one-dim
   irrationality measure at all: the upper bound on cycle length comes from the **two-log
   linear-forms estimate** (Laurent/LMN), the lower bound from **Crandall**. So the bottleneck
   constant is the two-log estimate's ($24.34\,D^4$ / de Weger exponent $0.158$), not $\mu$.
   Corrects `survey.md` §7.5/§11 and `open_problems.md` D.1/D.2. (Strong "$\mu$ provably useless"
   claim downgraded to `[CLAIM-UNVERIFIED]` intuition.)
2. *Mis-framed Step-1 check (C5 v1)* — compared bound magnitudes instead of decay direction;
   caught and corrected (Step-1 self-error).
3. *Computing a concrete $m^\*>91$ here* — blocked: all academic PDF hosts returned HTTP 403,
   so Hercher's explicit $F(m)$ and the Laurent-2008 constant were unavailable.
**Counter-example (if any):** n/a (1 = reading of the literature; 3 = blocked; 2 = the FALSE check output).
**Pointer to artifacts:** `collatz/theory/cycle_exclusion_explicit.md`,
`collatz/experiments/verify_cycle_exclusion.py`, `collatz/experiments/verify_cycle_exclusion_log.md`,
`collatz/theory/dead_ends.md` (Vector C section).
**Verdict:** (1) prior-art (not the method's lever); (2) falsified-then-corrected; (3) abandoned-in-environment.
**Lesson:** The cycle-exclusion lever is the **two-log linear-forms estimate** (const $24.34D^4$ /
de Weger exponent $0.158$) + the verification bound $B$ + circuit averaging — not $\mu(\log_2 3)$.

## 2026-06-02 — [track: frankl] — Vector 1: Shearer/submodular recapture of the chain-rule slack $\Delta_2$

**Agent / author:** Phase-2 theory agent (AI), for Alex Ye
**Time invested:** ~1 day theory + exact computation over all UC orbit reps $n\le5$ (29,327 families at $n=5$).
**Attack vector:** Gilmer's coordinatewise chain rule discards $\Delta_2=\sum_i I(C_i;(A_{<i},B_{<i})\mid C_{<i})\ge0$ (the conditional mutual information between the union bit and the individual prefixes, given the union prefix), where $C=A\cup B$, $A,B$ i.i.d. uniform on $\mathcal F$. Plan: recapture $\Delta_2$ (optimistically, all of it) via a submodular/Shearer-type inequality and add it to the AHS lower bound $H(C)\ge\frac1{1-c}\sum_i(1-p_i)H(A_i\mid A_{<i})+\Delta_2$, hoping to force a contradiction for some $c>\psi=(3-\sqrt5)/2$.

**Why it failed:** $\Delta_2\equiv0$ on **product families** (independent coordinates) — proved in `frankl/theory/vector1_shearer_chain_rule.md` Lemma 1 (independence of coordinates $\Rightarrow (A_i,B_i)\perp(A_{<i},B_{<i})\Rightarrow C_i\perp C_{<i}\Rightarrow\delta_i=0$). The AHS single-letter optimum is attained at the i.i.d.-Bernoulli$(\psi)$ product configuration (Theorem 1; optimizer `single_letter.py` gives $\mu^\*=0.809017$, argmin $(\psi,\psi)$ on the diagonal). Hence at the extremizer $\Delta_2=0$ and the optimistic Vector-1 bound reduces verbatim to AHS, giving $c_{V1}=\psi$ (Cor. 2). Numerically (exact, all orbit reps $n\le5$): among the 330 families with $c_{AHS}$ within $0.005$ of its minimum, $\max\Delta_2/H(C)=7.1\times10^{-3}\to0$ as $c_{AHS}\to\psi$; where $\Delta_2$ is large ($\Delta_2/H(C)\approx0.29$) the family already has $c_{AHS}\approx0.54$–$0.58$ (anticorrelation). Shearer/Han substitution fails for the same reason: those inequalities are tight on product distributions and the required *lower* bound on $H(C)$ is not a generic entropy inequality.

**Counter-example (if any):** n/a (no false claim was made). The obstruction is the family $2^{[k]}$ (and products): abundance exactly $0.5$, $\Delta_2=0$ to machine precision.

**Pointer to artifacts:** `frankl/theory/vector1_shearer_chain_rule.md`; `frankl/experiments/verify_ahs.py` (`delta2`, `chain_rule_lower_bound`); `frankl/experiments/verify_ahs_log.md` Run 3.

**Verdict:** gap-not-closeable (within the i.i.d. coupling).

**Lesson:** The chain-rule slack is a *correlation* quantity; union-closure does not lower-bound it (a union-closed family can have $\Delta_2=0$). The only live follow-up is to recapture $\Delta_2$ at a **non-i.i.d. (Liu) extremizer**, where $\Delta_2>0$ — that leaves Vector 1's premise and is logged as the top follow-up.

## 2026-06-02 — [track: frankl] — Vector 2: intersection-augmented objective $H(A\cup B)+\lambda H(A\cap B)$

**Agent / author:** Phase-2 theory agent (AI), for Alex Ye
**Time invested:** ~1 day theory + exact computation over all UC orbit reps $n\le5$.
**Attack vector:** Every entropy proof uses $A\cup B$ but never $A\cap B$. Plan: track either the joint $(A\cup B,A\cap B)$ or the weighted objective $H(A\cup B)+\lambda H(A\cap B)$, and derive a per-coordinate inequality on the multiset $(C_i,D_i)=(A_i\vee B_i,A_i\wedge B_i)$ beating the union-only one. Reimer's average-set-size theorem was hoped to supply the intersection-side budget.

**Why it failed:** (a) Joint objective: $(A\cup B,A\cap B)$ is a function of $(A,B)$ so its honest upper budget is $2H(A)$, not $H(A)$. The sharp per-coordinate ratio is $\mu_{\rm joint}=\inf H_{\rm pair}/(h(\alpha)+h(\beta))=3/4$ at $\alpha=\beta=1/2$ (Theorem 1, `single_letter.py` `v2_joint_sym`), giving $c=1-1/\mu=-1/3$. Budget-doubling exactly defeats the richer objective. (b) Weighted objective: needs an upper bound on $H(A\cap B)$. But $H(A\cap B)\not\le H(A)$ for union-closed families — **FALSE in 22,361 of 29,738 orbit reps ($n\le5$), ratio up to 1.530** (Theorem 2, exact computation). Reason: $A\cap B$ ranges over the intersection-closure $\mathcal F^\cap$, which for a union- (not intersection-) closed family can be larger than $\mathcal F$; the only honest bound $H(A\cap B)\le\log|\mathcal F^\cap|$ is uncontrolled by $\log|\mathcal F|$. Reimer gives a *lower* bound on intersection size (wrong direction for a budget). So no valid budget exists.

**Counter-example (if any):** Union-closed families with $H(A\cap B)>H(A)$ are abundant; the enumerator (`verify_ahs.py`) exhibits 22,361 at $n\le5$, max ratio $H(A\cap B)/H(A)=1.5296$. Also $H(A\cup B,A\cap B)>H(A)$ on $402/412$ families at $n\le4$ (excess up to $+2.13$); $H(A\triangle B)>H(A)$ on $366/412$.

**Pointer to artifacts:** `frankl/theory/vector2_intersection_term.md`; `frankl/experiments/verify_ahs.py` (`exact_entropy_intersection`, `exact_entropy_union_and_intersection`); `frankl/experiments/single_letter.py`; `frankl/experiments/verify_ahs_log.md` Run 4.

**Verdict:** gap-not-closeable (no valid budget; the asymmetry $A\cup B\in\mathcal F$ vs $A\cap B\notin\mathcal F$ is the whole content of union-closure).

**Lesson:** TRAP — charging the joint objective $H(A\cup B,A\cap B)$ against a single $H(A)$ budget yields a *false* "improvement" of $0.4295$ (`single_letter.py` `v2_joint_ahsbudget_WRONG`, argmin at boundary $(0.035,0.035)$); a related per-family heuristic in `vector_analysis.py` produced a spurious "$0.5$". Both are budget-mismatch artifacts (Prop. 3 in the writeup). Any intersection-side idea MUST first exhibit a *provable* upper bound on the intersection-side entropy; none exists from union-closure alone.

*(append further entries above this line as approaches fail)*
