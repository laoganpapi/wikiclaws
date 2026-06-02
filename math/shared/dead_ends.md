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

## 2026-06-02 — [track: frankl] — Vector 3: joint coupling+measure single-letter optimization plateaus at ψ; Liu 0.38271 not reproduced

**Agent / author:** Vector-3 computational agent (AI), for Alex Ye
**Time invested:** ~1 day formulation + compute.
**Attack vector:** Survey §7.3+§7.7 / open problem B.7 — jointly optimize the
dimension-free single-letter entropy program over (a) conditional-i.i.d.
couplings with auxiliary $U$, $|U|\in\{2,4,8,16\}$, and (b) a Cambie-style
reweighted base measure, aiming to beat Liu's numerical $0.38271$. Artifacts:
`frankl/experiments/{opt_formulation.md, joint_opt.py, certify_psi.py,
certificate_0.38197.md, results.md, verify_opt_formulation.py, figures/}`.

**Why it failed (to beat ψ):**
1. *Reweighting alone = free choice of the marginal law $\mu$ in the dim-free
   limit*, over which the base i.i.d. program already optimizes; optimum is
   exactly $\psi$ (closed form: crossover $h(2p-p^2)=h(p)\iff p=\psi$). No gain.
2. *Auxiliary $U$ (faithfully reconstructed, "diagonal") gives no gain:* given
   $U{=}j$, $(A_i,B_i)$ iid $\mathrm{Bern}(p_j)$ puts the single-letter $(P,Q)$ on
   the diagonal $\{(p_j,p_j)\}$; (IV) becomes a mixture over the same per-point
   crossover, threshold $\psi$ for every $|U|$. Confirmed $|U|\in\{2,4,8,16\}$.
3. *Enlarging the coupling class is the WRONG direction:* a free off-diagonal
   coupling LOWERS the certified threshold to $\approx0.359<\psi$, because a larger
   class makes the feasibility inequality (IV) a weaker necessary condition.
   Beating $\psi$ needs *added* constraints (the §7.2/B.6 chain-rule slack
   $\Delta_2$), not a richer coupling. (Independently corroborated by the Vector-1
   entry above: the AHS extremizer is the iid $\mathrm{Bern}(\psi)$ product, where
   $\Delta_2=0$.)
4. *Liu's exact functional inaccessible:* arXiv abs/pdf/ar5iv/mirrors all returned
   HTTP 403 / host-not-in-allowlist. Two from-first-principles reconstructions of
   his $I(C;U)/I(A;U)$ bookkeeping failed — one collapses (no gain), the other
   (`conditional_U_functional(mode='liu_refund')`) admits a degenerate optimizer
   with atoms at $p\in\{0,1\}$ driving the bound to $0$ (double-counts the refund).
   No constant was claimed from it.

**Counter-example (if any):** n/a (no false claim). The trap was that "minimize
$E[P]$ over the feasible set" returns $0$ via the degenerate $\mu=\delta_0$; fixed
by a threshold-via-bisection with non-degeneracy constraint $E[h(P)]>0$.

**Pointer to artifacts:** as listed above; run log `data/joint_opt_run.txt`.

**Verdict:** abandoned for the beat-0.38271 goal / partial-success: the
sanity-floor $\psi$ IS reproduced and *certified* (closed form + mean-value-form
interval arithmetic, `[0.01,0.99]^2`, min lower bound $+5\times10^{-9}$).

**Lesson:** (i) The entropy-method improvement beyond $\psi$ is NOT reachable by
generalizing the coupling/measure inside the feasibility inequality — that only
weakens the bound; the lever is a *tighter lower bound on $H(A\cup B)$* capturing
union-closure (§7.2). The literal "joint optimization over more couplings" reading
of B.7 is a dead end; the live route is recapturing $\Delta_2$ at a non-i.i.d.
(Liu) extremizer (same conclusion as Vector 1). (ii) Naive interval arithmetic on
the 2-D Sawin inequality is hopeless (dependency blowup, ~60% spurious-negative
boxes); the mean-value/centered extension is necessary & sufficient (seconds).
(iii) Always reformulate "minimize the marginal" as a threshold problem with an
explicit non-degeneracy constraint, else the empty-family law silently wins.

*(append further entries above this line as approaches fail)*
