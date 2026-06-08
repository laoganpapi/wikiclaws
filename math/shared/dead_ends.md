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

## 2026-06-02 — [track: frankl] — Vector 3 (the live lever): recapturing Δ₂ at a NON-PRODUCT extremizer

**Agent / author:** Phase-2 theory agent (AI), for Alex Ye
**Time invested:** ~1 day theory + exact computation (shared-U coupling to n=128; all UC orbit reps n≤5, 29,723 families).
**Attack vector:** The ONE lever the prior agents + red-team left open (Vector 1 §5, the "Vector 1 × Liu coupling" follow-up). Vector 1 killed Δ₂-recapture *within the i.i.d. coupling* because Δ₂≡0 at the product extremizer. The hope: move the worst case OFF the product onto a non-product coupling where Δ₂>0, recapture it via the augmented necessary condition $(1/(2(1-c)))S + \Delta_2 \le H(C) \le H(A)$, and force a contradiction for some $c>\psi=(3-\sqrt5)/2$. Constructed our OWN non-product families (Liu's exact scheme is HTTP-403): (a) the shared-auxiliary-$U$ conditionally-i.i.d. coupling $Q^{(n)}_{p,w}$ (draw $U=j$ w.p. $w_j$; given $U=j$ every coordinate pair iid $\mathrm{Bern}(p_j)$, $U$ shared across all $n$ coords — non-product, $\Delta_2>0$); (b) correlated-Bernoulli pairs with Pearson $\rho$.

**Why it failed (THREE independent offsets, all certified Step-1):**
1. *Asymptotic (the decisive one).* On $Q^{(n)}_{p,w}$, **Lemma 3**: $\Delta_2 \le I(C;U)$ (conditioning on $U$ makes $C_i\perp$ prefixes, so $\mathrm{chain\text-LB}\ge H(C|U)$). **Cor 4**: $I(C;U)\le H(U)\le\log_2 k = O(1)$, hence $\Delta_2/n\to0$. The dimension-free constant is the per-coordinate ratio, on which the recaptured $\Delta_2$ contributes **exactly zero**; the limit is the diagonal $U$-mixture $E_j[h(u_j)]\le E_j[h(p_j)]$, threshold $\psi$ for every atom. (Verified exactly: k=6, n=128: $H(A)/n=0.7386$, $H(C)/n=0.6351$, $\Delta_2/n=0.0056\to0$; biggest finite recapture $\Delta_2/H(A)\approx0.026$, peeling off as $n\uparrow$.)
2. *Direction.* In the honest finite-block ledger $c_\text{aug}=1-S/(H(C)-\Delta_2)$, subtracting $\Delta_2\ge0$ shrinks the denominator, so $c_\text{aug}\le c_\text{AHS}$ (equality iff $\Delta_2=0$). Recapturing $\Delta_2$ moves the certified constant the **wrong way**. (All 29,723 reps n≤5: $\min c_\text{aug}^\text{honest}=0.382353 \le \min c_\text{AHS}=0.382663$; both $\to\psi$.)
3. *Anticorrelation, quantified (the brief's exact question).* Over all UC reps, $\max\Delta_2/H(C)$ bucketed by abundance is **0 at abundance 0.5** (extremizer) and only reaches $\approx0.19$–$0.23$ at abundance $\ge0.75$; among families within $5\times10^{-3}$ of the AHS floor, $\max\Delta_2/H(C)\to0$. The recoverable $\Delta_2$ is, to leading order, proportional to how far above $\psi$ abundance ALREADY is — it can never create the gap from $\psi$, only appears once the gap exists. **The anticorrelation cancels the gain.**

Plus the **certification gate**: the per-coordinate Sawin lower bound $(S_c)$ underlying the whole assembly is INVALID for every $c>\psi$ ($\min_{p,q}G_c<0$ at $(\psi,\psi)$); no additive $\Delta_2$ can repair an already-failed lower bound.

**Counter-example (if any):** n/a (no false claim). BUT this family **reproduces both documented artifacts if mis-handled**, and we surface them deliberately: (i) the **budget-mismatch 0.43–0.5** — using $H(A)$ instead of $H(C)$ in the denominator (the gap $H(A)-H(C)$ is union-closure slack, vanishes per-coord; double-counts) gives $c_\text{augHA}=0.5$ exactly on $2^{[2]}$, $\min_F=0.4500$ over n≤5; (ii) the **floor-sweep non-sequitur** — the family floor $(1/(2(1-c)))S+\Delta_2\le H(A)$ holds numerically on small UC families even at $c=\psi+10^{-2}$, but certifies nothing because $(S_c)$ is already invalid there; (iii) the **$\rho>0$ favourable-coupling** — positive A–B correlation raises the crossover to $>\psi$, but the budget $H(C)\le H(A)$ presupposes $A\perp B$ ($\rho=0$ forced for an i.i.d. sample), so it is not a valid necessary condition.

**Pointer to artifacts:** `frankl/theory/vector3_delta2_nonproduct.md`; `frankl/experiments/vector3_delta2_nonproduct.py` (`SharedUCoupling`, `shared_u_augmented_constant`, `sawin_lower_bound_min`, `correlated_crossover`); `frankl/experiments/data/vector3_delta2_run.txt`; tests `tests/test_uc.py::TestVector3Delta2NonProduct`.

**Verdict:** gap-not-closeable (within the i.i.d. + shared-$U$ conditionally-i.i.d. classes, for the additive-$\Delta_2$ recapture). The lever is closed; $\psi$ stands as the best CERTIFIED constant.

**Lesson:** The off-product $\Delta_2$ is real but **asymptotically irrelevant**: it is the $O(1)$ latent-information term $I(C;U)$, exactly the correction the per-coordinate normalization discards. Vector 1's "but $\Delta_2>0$ off the product" escape is closed — moving off the product makes $\Delta_2>0$ at finite $n$ but $\Delta_2/n\to0$. **Open gap (NOT closed here):** Liu's $0.38271$ is real and exceeds $\psi$, but our analysis shows it CANNOT come from the additive $+\Delta_2$ in the shared-$U$ class — it must use a *relative* $I(C;U)/I(A;U)$ bookkeeping or a finite-$n$/boundary effect, which needs Liu's (inaccessible) source to pin down. The general entropy-method ceiling with that bookkeeping remains $>\psi$ and unsettled.

## 2026-06-02 — [track: frankl] — Lattice attack: lattice invariants cannot control abundance (sharp obstruction)

**Agent / author:** Lattice-attack theory agent (AI), for Alex Ye
**Time invested:** ~1 day; full lattice toolkit + exact sweep over all UC orbit reps n≤5 (29,723 with |F|≥2) + parametric classes + exhaustive cone verification.
**Attack vector:** A genuinely different angle from the entropy method (capped at ψ): use the **lattice/order structure** the entropy proofs discard. `F` is a join-semilattice under ⊆ (join=∪); adjoin ∅ to get a lattice `L` with top `T=∪F`. Poonen (1992) [STATEMENT UNVERIFIED — source blocked] reformulates FUCC as: every finite lattice has a join-irreducible `j` with `|↑j| ≤ |L|/2`. Plan: find a structural parameter (height, #join-irreducibles, width, modularity/semimodularity defect) that forces an abundant element (abundance ≥ 1/2) — i.e. a lattice-structural bound the entropy method misses. Toolkit: `frankl/experiments/lattice.py` (covers, JIs/MIs, atoms, height, width via Dilworth, distributive/modular/lower-/upper-semimodular flags, Poonen filter), validated on B2/M3/N5/chains/Booleans.

**Why it failed (to give a general bound) — the sharp obstruction:** **Abundance is NOT a lattice invariant.** The decisive construction is the **universal-element cone**: for any UC family `G` (∅∈G), `cone(G) := {∅} ∪ {A∪{z} : A∈G, A≠∅}` with a fresh element `z` is (i) union-closed, (ii) **lattice-isomorphic to `G`** (so ALL invariants — |L|, height, width, #JI, #MI, #atoms, distributive/modular/lsm/usm — are identical), yet (iii) has **abundance `1−1/|L|`** (element `z` is in every member but the bottom). Proved (Prop. 4.1) and verified exhaustively: **0 failures over all 206 families `G` at n≤4** (`lattice_cone.check_construction`). Minimal clean witnesses: the Boolean lattice `B_k` realized as the cube `2^[k]` (abundance **exactly 1/2**) vs `cone(2^[k])` (abundance `1−1/2^k`) — same abstract lattice, **literally identical `LatticeInvariants`**, abundance 0.5 vs up to 0.97. Consequently no function of the abstract lattice — a fortiori no coarse invariant — can lower-bound abundance above 1/2; the only lattice-invariant bound possible is the one Poonen already encodes, which is *equivalent* to FUCC (no shortcut). Stronger: coarse invariants don't even control `minab(L) = min abundance over realizations` — **112 coarse-invariant signatures (|L|≤12) host non-isomorphic lattices with different `minab`** (sharpest spread 0.556→0.778), via exact lattice-iso classification (`lattice_minab`).

**Counter-example (if any):** The obstruction witnesses ARE the explicit counter-examples to "invariants control abundance": `F₁=2^[3]` (abundance 0.5) vs `F₂={∅}∪{S∪{3}:∅≠S⊆{0,1,2}}` (abundance 0.875) — `Invariants(F₁)==Invariants(F₂)` exactly. Also `B_k` for all k: abundance ≡ 1/2 with #JI=k, width=C(k,⌊k/2⌋), height=k all →∞ (`tests::test_boolean_lattices_stay_at_half`) — this REFUTES the apparent n≤5 statistical "floors" (e.g. "width≥4 ⇒ abundance>1/2", "#JI≥6 ⇒ ≥0.53"), which are small-`n` artifacts (the low-abundance cube `B_k` of a given width/#JI first appears at n=k>5).

**Partial positive (NOT a general bound, likely folklore):** `abundance ≥ height(L)/|L|` (Prop. 3.1), via the explicit witness "any element in the first atom of a longest chain is in all `height` chain-elements". **0 violations over all 29,723 families n≤5.** Certifies Frankl for **tall lattices** (`2·height ≥ |L|`; all 1,947 such at n≤5 have abundance ≥ 1/2, min exactly 0.5), tight on chains. **[PRIOR-ART CHECK PENDING — elementary, almost surely folklore / subsumed by Colbert 2024 chain conditions; recorded as an internal certificate, NOT claimed new.]**

**Pointer to artifacts:** `frankl/theory/lattice_attack.md`; `frankl/experiments/{lattice.py, lattice_sweep.py, lattice_analyze.py, lattice_minab.py, lattice_cone.py, lattice_parametric.py}`; `frankl/experiments/data/{lattice_attack_run.txt, lattice_sweep_n0..5.jsonl}`; tests `tests/test_uc.py::TestLatticeAttack` (9 tests pass; full suite 57 pass).

**Verdict:** gap-not-closeable from lattice invariants (sharp obstruction, exact all-`n` construction). The conditional height bound is a likely-known certificate, not a path to a constant > 1/2.

**Lesson:** Abundance lives in the **labelling** of join-irreducibles by ground-set elements (precisely: each ground element `x` has a *fibre* `Fib(x)={A:x∈A}`, always a **filter** of `L`, principal `=↑m_x` iff `x∈m_x`; abundance = max filter-density of these fibres, eq. (1.1)). The cone shows this labelling is **free given `L`** — a fresh universal coordinate sends abundance to ≈1 without touching the lattice. So invariants are powerless, which is exactly why **every successful lattice result in the literature restricts the lattice CLASS** (distributive/modular/lower-semimodular — Poonen/Abe/Reinhold) rather than bounding an invariant: those classes **forbid the cone** (a universal element breaks (semi)modularity / the exchange axiom). The live next brick is the **upper-semimodular** class (open problem E.2; Reinhold's lsm proof does not dualize), attacked via the JI-filter/exchange structure with the cone structurally ruled out — NOT via any invariant.

---

## 2026-06-02 — [track: frankl] — polynomial method / slice rank (CLP / Ellenberg–Gijswijt / Tao 2016) on Frankl

**Agent / author:** Alex Ye (with AI assistance disclosed). `[NOVELTY UNVERIFIED — possibly tried in Croot–Lev–Pach successor literature; check on next session.]`
**Time invested:** ~1 session of code + theory.
**Attack vector:** Encode each `A ⊆ [n]` as its indicator `x_A ∈ {0,1}^n`. The relation `A ∪ B = C` is per-coordinate `c_i = a_i + b_i − a_i b_i` (char ≠ 2). Build the 3-tensor `T_F(A,B,C) = 1{A ∪ B = C}` over `F × F × F` for a UC family `F`, and compute its slice rank (Tao 2016) over `𝔽_p` for `p ∈ {2,3,5,7}`. The hope (cap-set analogue): a polynomial-rank upper bound `|F| ≤ f(n, abundance)` decaying like `2.756^n`, by mimicking Croot–Lev–Pach: tensor low-degree expression + diagonal-on-set-of-interest ⇒ size bound.

**Why it failed (the obstruction is structural and exact):**

> **Theorem.** For every union-closed `F` and every field `𝔽`, `slice-rank(T_F) = |F|`. In particular, each unfolding matrix rank equals `|F|`, **independent of `F`'s structure** (and hence of abundance). Hence no abundance bound is extractable from the standard slice-rank machinery applied to `T_F`. ([`polynomial_method.md`](../frankl/theory/polynomial_method.md), Theorem 2.1 + Cor. 2.2.)

The root cause is a *type mismatch* between cap-set and Frankl:
* Cap-set's `x + y + z = 0` is **non-determinative** (for `(x,y)` there's a unique `z` that typically falls outside a cap-set), and the indicator polynomial `1 − (x_i+y_i+z_i)^2` has degree 2 *independent of `n`*. Tensor is diagonal on the cap-set; polynomial method gives `|S| ≤ 3 · M_n = O(2.756^n)`, well below `3^n`.
* Frankl's `A ∪ B = C` is **fully determinative** (given `(A,B)`, `C := A ∪ B` is unique and always in `F` by closure), so `T_F` is a *transport plan* with each `(A,B)` mapped to one `C`. Unfolding rank along `C` is exactly `|F|` (the columns `{(C,C) : C ∈ F}` form an identity submatrix in the unfolding, since `T_F(C', C', C) = 1{C' ∪ C' = C} = δ_{C', C}`). The polynomial identity for the union indicator has per-coordinate degree ≥ 2 (each factor `(1 − (c_i − a_i − b_i + a_i b_i)^2)` is degree 4), so the polynomial-rank bound is `≥ \binom{2n}{n} = Ω(4^n)` — vacuous against `|F| ≤ 2^n`.

Variant tensors (`T_∩`, `T_△`, `T_∪³` = 3-cover) were also tested. `T_∩` shares the obstruction (same identity-submatrix argument). `T_△` and `T_∪³` have non-trivial slice rank but **no useful inequality** to abundance survives; both candidates `sr/|F| ≤ 1 - abundance` and `sr/|F| ≥ 1 - abundance` are falsified on small explicit families (n=4 with abundance=0.8 has `sr_T△=0`; n=3 cube has `sr_T△/|F|=1.0 > 0.5 = 1-abundance`).

**Counter-example (if any):** *All 416 UC orbit reps at n≤4 (|F|≥1), every prime in {2,3,5,7}* witness `slice-rank(T_F) = |F|`. 0 violations across 1664 (F, p) checks. Boolean cube `2^[n]` is the cleanest witness: `slice-rank = 2^n = |F|`, abundance = 1/2 — no information extracted. Data in `frankl/experiments/data/polymethod_n{0..4}.jsonl`.

**Pointer to artifacts:**
* `frankl/theory/polynomial_method.md` — full writeup (theorem-proof format, with the structural diagnosis in §4).
* `frankl/experiments/polynomial_method.py` — slice-rank computations over `𝔽_p`.
* `frankl/experiments/data/polymethod_n{0..4}.jsonl` — per-family raw data.
* `frankl/experiments/data/polymethod_summary.txt` — human-readable summary.

**Verdict:** **gap-not-closeable** from standard CLP / Ellenberg–Gijswijt / Tao slice rank applied to the natural Frankl tensor. The obstruction is exact, has an explicit construction (identity submatrix), is validated exhaustively at n≤4, and is **diagnosed structurally** (determinism + high per-coordinate polynomial degree, the two ingredients that defeat the CLP scheme). The only sub-direction worth a future pass is the *weighted partition rank* with a Boltzmann-style abundance weighting, plus a Fourier-side combination — neither produced a bound here.

**Lesson:** **The polynomial method shrinks "sets where a low-degree algebraic relation has only trivial solutions." Frankl asks for a frequency lower bound on element appearances in a family closed under a high-degree, deterministic operation.** The two problem shapes are misaligned at the *type* level. Any future polynomial-method attack must (a) replace the deterministic `A ∪ B = C` by a non-determinative substitute (the 3-cover `A ∪ B ∪ C = [n]` is the cleanest candidate but produces no useful bound), AND (b) find a polynomial identity for the substitute relation of degree `o(n)` per coordinate. Neither lever has a candidate; the prior is "this paradigm does not transfer." If a future session finds it has been previously published, our role becomes: cite + record.

## 2026-06-03 — [track: frankl] — Boolean Fourier / Walsh–Hadamard quadratic invariants on UC families

**Agent / author:** Alex Ye (AI-assisted). `[NOVELTY UNVERIFIED — Karpas arXiv:1708.01434 (2017) and Gendler arXiv:2504.13347 (2025) prior art for the density `≥ 1/2 − c` regime; arXiv inaccessible this session.]`
**Time invested:** ~1 session of theory + compute. Full sweep over all 29,738 non-trivial UC orbit representatives at n ≤ 5 (~33 s WHT compute on n=5).
**Attack vector:** For each UC family `F`, compute the Walsh-Hadamard spectrum `(f̂(S))_S` of `1_F : {0,1}^n → {0,1}` (`L²`-normalized: `Σ f̂² = |F|/2^n`). Test five hypotheses tying *quadratic* (sign-flip-invariant) spectral statistics — level weights `W^k = Σ_{|S|=k} f̂(S)²`, influences `Inf_i = Σ_{S ∋ i} f̂(S)²`, total influence `I[f]`, noise stability `Stab_ρ` — to abundance. The hope: a Karpas-style Fourier inequality that constrains `min_i f̂({i})` from above (FUCC says some `f̂({i}) ≤ 0` by the identity `f̂({i}) = p · (1 − 2 ab_i)`).

**Why it failed:** the Boolean cube `2^[n]` is the structural obstruction. It saturates FUCC at `abund_max = 1/2` AND has trivial spectrum (`f̂(S) = δ_{S,∅}`, since `1_{2^[n]} ≡ 1`), so EVERY level-`≥ 1` quadratic invariant is zero: `W^k[1_{2^[n]}] = 0` for `k ≥ 1`, `I[1_{2^[n]}] = 0`, `Stab_ρ[1_{2^[n]}] = 1` (the constant). Any inequality of the form `min_i f̂({i}) ≤ −G(p, W^1, …, W^n, I, (Stab_ρ)_ρ)` with `G ≥ 0` must vanish on the cube, hence cannot certify `min_i f̂({i}) < 0` strictly. Validated exhaustively on the n ≤ 5 sweep:

1. **H1 (min-influence lower bound):** `min_i Inf_i / (p·(1-abund_max)) = 0` — falsified by `2^[n]` and by 11 of the 39 families at `abund_max = 1/2 exactly`. No constant `c > 0` exists.
2. **H2 (total influence vs abundance):** `I[f]` lower envelope is `0` at `abund=0.5` (cube) AND `0.078` at `abund=1.0` ({X}). No useful monotonicity.
3. **H3 (low-degree concentration):** `C_0 ∈ [0.03, 1.0]`, `C_1 ∈ [0.06, 1.0]` over UC reps at n=5 — no uniform concentration. UC does not imply low-degree.
4. **H4 (noise stability):** `Stab_ρ/p` at `abund_max = 0.5` and `abund_max = 1.0` are the same (`0.24` at `ρ=0.5`) — can't distinguish FUCC-saturating from trivial.
5. **H5 (Fourier FUCC form `∃ i : f̂({i}) ≤ 0`):** verified on all 29,738 non-trivial UC families (sanity gate); 10,974 satisfy strong form `∀ i : f̂({i}) ≤ 0` — but no quantitative lower bound `|min f̂({i})| ≥ c·p` survives (the "barely-Frankl" families have `min_i f̂({i}) = 0` exactly).
6. **H6 (level-1-only LP bound):** `max ab_i ≥ (1 − √(W¹/(np²)))/2` — caps at exactly `1/2`, never exceeds, on 29,743 records.

The fundamental identity `f̂({i}) = f̂(∅) · (1 − 2 · ab_i)` (§1.3 of writeup) is elementary (O'Donnell Ch.1 Ex.1.1) and was verified to `1e-12` on every record; the *Fourier form* of Frankl is `∃ i : f̂({i}) ≤ 0`. Karpas (2017) uses exactly this signed level-1 character to push FUCC in the density `≥ 1/2 − c` regime. Extending Karpas's signed-Fourier argument to all densities is the live sub-direction — but it is NOT a quadratic-spectrum approach, so this dead-end is specifically about *rotation/sign-flip-invariant* spectral statistics.

**Counter-example (if any):** The Boolean cubes `2^[n]` ARE the explicit counter-examples to every quadratic-spectrum bound: spectrum `δ_{S,∅}`, abundance exactly `1/2`. Also the families `{∅, [k]}` (level weights split between `W^0` and `W^k`) have the same `(W^j)_j` regardless of the labelling of the `k`-element "active block", but their min abundance over labellings ranges from `0` to `1/2` — confirming rotation invariance fails.

**Pointer to artifacts:** `frankl/theory/boolean_fourier.md`; `frankl/experiments/boolean_fourier.py` (WHT, spectrum, influences, stability, identity-check); `frankl/experiments/boolean_fourier_sweep.py`; `frankl/experiments/boolean_fourier_hypotheses.py`; `frankl/experiments/data/fourier_n{0..5}.jsonl`; `frankl/experiments/data/fourier_summary.txt`; `frankl/experiments/data/fourier_hypotheses.txt`.

**Verdict:** **gap-not-closeable** for spectrum-quadratic Boolean-Fourier methods (sign-flip-invariant features) — structural obstruction at the Boolean cube, validated on all 29,738 non-trivial UC orbit reps at n ≤ 5. Analogous to the polynomial-method obstruction (`polynomial_method.md`): the worst case for FUCC (abundance exactly `1/2`) has a SPECTRUM indistinguishable from the constant function.

**Lesson:** Boolean-Fourier methods on FUCC split into two camps. (i) *Quadratic / Plancherel-style* (level weights, influences, noise stability, KKL/Friedgut-style isoperimetry) — **structurally dead** because the Boolean cube has trivial spectrum but saturates FUCC. (ii) *Signed / convolution-style* (Karpas's regime, using `f̂({i})` with sign) — **live**, since the signed identity `f̂({i}) = p(1 - 2 ab_i)` IS exactly Frankl's statement at level 1. Any future Boolean-Fourier attack must be signed at every level it uses, not quadratic. The natural target is to extend Karpas (2017) past density `1/2 − c` using a signed level-2 inequality from the union-closure constraint `Σ_{x,y} f(x) f(y) (1 - f(x ∨ y)) = 0`; this introduces signed `f̂(S) f̂(T)` cross terms whose sign structure is not handled by Plancherel. `[NOVELTY UNVERIFIED — Karpas-extension may exist; arXiv inaccessible.]`

## 2026-06-03 — [track: frankl] — Shadow / Kruskal–Katona: compression does NOT preserve union-closure; shadow/profile/FKG levers all fail

**Agent / author:** Alex Ye (AI-assisted). `[NOVELTY UNVERIFIED — shadow methods are classical (Kruskal 1963, Katona 1968); the shifting operator `S_{ij}` is the standard Frankl-shifting tool; may already have been tried on FUCC. arXiv 403-blocked this session.]`
**Time invested:** ~1 session theory + compute. Full sweep over all 29,738 non-trivial UC orbit reps at n ≤ 5 (compression + split + shadow/shade + FKG; ~minutes).
**Attack vector:** Apply the Kruskal–Katona / shadow machinery — the classical tool for relating a family to its lower shadow `∂F` and upper shade `∇F`. Four concrete sub-attacks: (a) the standard down-compression / shifting operator `S_{ij}` (rename `j → i` when free), hoping it PRESERVES union-closure and only DECREASES max-abundance, which would reduce FUCC to compressed families; (b) the `F_i / F_{¬i}` split (`F_{¬i}` is itself UC; `abundance_i ≥ ½ ⟺ |F_i| ≥ |F_{¬i}|`), seeking a KK-type shadow-containment `trace_i ⊆ link_i` forcing `max_i |F_i| ≥ |F|/2`; (c) a profile/LYM inequality forcing top-heaviness; (d) Ahlswede–Daykin / FKG correlation forcing abundance.

**Why it failed:** all four levers fail, and the FAILURE OF (a) is itself the valuable finding.

1. **(a) Compression does NOT preserve union-closure.** Minimal witness (exact, valid for all n ≥ 4): `F = {{0,1},{2,3},{0,1,2,3}}` is UC (`{0,1}∪{2,3}={0,1,2,3}∈F`), but `S_{0,2}` (rename element 2→0) sends `{2,3}↦{0,3}`, giving `{{0,1},{0,3},{0,1,2,3}}` which is NOT UC: `{0,1}∪{0,3}={0,1,3}∉F`. Union-closure is a global JOIN constraint sensitive to support-disjointness; the down-shift collides supports and shrinks a generating join. Census n≤5: single `S_{ij}` breaks UC on **5,532 / 29,738** families, compress-to-fixed-point breaks UC on **522**; first failures appear at n=4 (UC preserved for ALL n≤3). WORSE: even when UC is preserved, compression INCREASES max-abundance on **22,814 / 29,738 (77%)** families — the wrong direction for a reduction (it discards the hard extremal families). So the standard shifting reduction is structurally unavailable for FUCC.

2. **(b) The shadow-containment lever fails.** `trace_i ⊆ link_i` (which would give `|F_i| ≥ |F_{¬i}|` immediately) is VIOLATED: at the most-abundant i, 8,164 violations; at SOME i, 3,075 violations. Minimal failure is the saturating diagonal `F = {∅,{0,1}}` (abundance exactly ½): at i=0, `link_0={{1}}`, `trace_0={∅}`, `∅∉{{1}}`. Frankl holds there but NOT via containment. Surviving symptoms (C2: `|∂link_i| ≥ |∂trace_i|` at the abundant i, 0 violations; C5: Reimer avg-size ≥ ½log₂|F|, 0 violations) are downstream consequences, not independent levers.

3. **(c) No profile/LYM top-heaviness.** Candidate "average set size ≥ n/2" is FALSE (508 violations; e.g. `{∅,{4}}` at n=5 has avg 0.5 ≪ 2.5). `Σ_i(|F_i|−|F_{¬i}|) ≥ 0 ⟺ avg ≥ n/2` is a SUM being nonnegative, which does not give a single i with `|F_i| ≥ |F_{¬i}|` (the LYM averaging gap). Only Reimer ½log₂|F| survives — already known insufficient (survey §2.2).

4. **(d) Ahlswede–Daykin / FKG fails outright.** Uniform-on-F is NOT log-supermodular (a UC family is not an up-set), so positive correlation fails: `Pr[i,j∈A] ≥ Pr[i]Pr[j]` is VIOLATED on **119,662 / 295,572 pairs (40.5%)**, min correlation `−1/6`. Minimal witness `{{0},{1},{0,1}}`: elements 0,1 anti-correlated (`Pr[0,1]=⅓ < 4/9`), because joins force co-occurrence absent in the generators. Union-closure produces NEGATIVE element-correlation — the opposite sign of what an FKG proof needs.

**Counter-example (if any):** Compression-breaks-UC: `F = {{0,1},{2,3},{0,1,2,3}}` (n=4), `S_{0,2}(F)` not UC. FKG/anti-correlation: `F = {{0},{1},{0,1}}` (n=2), corr `−1/9`. The recurring extremizer is again the Boolean cube `2^[n]`: abundance exactly ½, IS a shift-compression fixed point (compression extracts nothing), and shadow-trivial — its cone `cone(2^[n])` (abundance `1−1/2^n`) has the same layer/shadow profile shape, so shadow statistics cannot distinguish abundance-½ from abundance-1. Same collapse as `lattice_attack.md` §4 and `boolean_fourier.md` §4.

**Pointer to artifacts:** `frankl/theory/shadows_kruskal_katona.md`; `frankl/experiments/shadows.py` (`shift_family`, `fully_compressed`, `compress_to_fixed_point`, `split`, `link_and_trace`, `lower_shadow`, `upper_shade`, `profile`, `fkg_correlation`, `cone_extremizer_check`); `frankl/experiments/data/shadows_n{1..5}.jsonl`, `data/shadows_summary.txt`; tests `tests/test_uc.py::TestShadowsKruskalKatona` (6 tests pass; full suite 69 pass).

**Verdict:** **gap-not-closeable** for the standard compression/shifting reduction (it neither preserves union-closure — first failure n=4 — nor reduces max-abundance) and for the shadow-containment, profile/LYM, and Ahlswede–Daykin/FKG levers (all falsified on the n≤5 enumeration). No bound produced; no false claim made.

**Lesson:** The powerful Kruskal–Katona / shifting toolkit is **structurally inapplicable** to FUCC, and now we know precisely why: `S_{ij}` is a DOWN-shift on coordinates, but ∪ is an UP-operation whose value depends on coordinate-disjointness, so the shift scrambles generating joins (minimal witness `{{0,1},{2,3},{0,1,2,3}}`). This is likely the reason no FUCC bound has come from compression despite its dominance elsewhere in extremal set theory. The one live brick is a **join-respecting compression** acting on the join-irreducibles / fibre-labelling (the `lattice_attack.md` JI structure) rather than on raw coordinates — which is exactly the fibre/labelling chokepoint identified by the lattice attack (open problem F.2). Five orthogonal methods (entropy, lattice invariants, polynomial, Boolean Fourier, shadows) now all bottom out at the same place: the Boolean cube is the extremizer and the missing lever is the *labelling* of join-irreducibles, not any coordinatewise / order / spectral / shadow invariant. `[NOVELTY UNVERIFIED]`

## 2026-06-03 — [track: frankl] — LP duality / fractional relaxation (Poonen weight-functions, Reimer-as-dual)

**Agent / author:** LP-duality theory agent (AI-assisted), for Alex Ye. `[NOVELTY UNVERIFIED — Poonen 1992 weight functions + LP relaxations of Frankl very likely prior art; arXiv 403 this session.]`
**Time invested:** ~1 session theory + full sweep over all 29,723 UC orbit reps (|F|≥2, n≤5), per-family LP solves via scipy.optimize.linprog (HiGHS).
**Attack vector:** Phrase Frankl as an LP and ask whether LP duality forces a dual certificate proving max_i abundance_i ≥ 1/2. Three formulations contrasted (`lp_duality.py`): (P-weight) adversary picks a free probability weight `w` on members, minimise the max weighted abundance; (D-Reimer/cover) fix the uniform measure and certify via averaging + order-ideal valid inequalities; (Sec.6) a second-moment/power-mean candidate strengthening.

**Why it failed (three nested obstructions, all Step-1 certified):**
1. *(P-weight) is the WRONG LP — vacuous.* `min_w max_i Σ_{A∋i} w(A) = 0` (put all mass on ∅, or on a member omitting the heavy elements). 20,240 of 29,723 families have value < 1/2; max gap true−minmax = 0.941 (cone(2^[4])). It does NOT have Frankl as its value. **This is the LP-shaped twin of the documented 0.43/0.45/0.5 budget-mismatch traps** (charging a free measure instead of the uniform one). Union-closure imposes NO linear inequality on the abundance vector of a free measure (each fibre is a filter, but `Σ_{A∈filter} w(A)` is free), so the measure MUST be fixed to uniform — which is exactly what Frankl is about.
2. *(D-Reimer/cover) caps at exactly 1/2, degenerate on the Boolean cube.* The correct dual is **Reimer's average-set-size theorem in multiplier form**: max_i ab_i ≥ avg_set_size/n (averaging identity Σ_i ab_i = avg_set_size, exact). On the cube `2^[k]`: avg_set_size = k/2, n = k, so cert = 1/2 EXACTLY for every k, with Reimer's inequality `avg ≥ ½log₂|F|` TIGHT (|F|=2^k). Zero margin, uniform (degenerate) multipliers. **Same universal extremizer `2^[k]` as the polynomial method (slice-rank=|F|) and Boolean-Fourier (trivial spectrum)**: the FUCC extremizer is perfectly flat (every ab_i = 1/2), so every first-order/symmetric LP functional saturates at 1/2 with no slack. The cover certificate proves Frankl on 29,717/29,723 families but can never exceed 1/2.
3. *Real integrality gap below 1/2 on 6 lopsided families.* The cover certificate certifies < 1/2 on EXACTLY 6 families (min 0.40), true abundance 0.78–0.89. All 6 share one structure: a near-universal heavy element (the FUCC element) plus 1–2 low-frequency parasitic elements that drag the MEAN below 1/2 while the MAX stays high. **The 0.40/0.45 here are REAL averaging values, not budget-mismatch artifacts** (e.g. freq vector [2,3,4]+dead slot: Σab=1.8 over n=4 slots = 0.45; over n=5 = 0.40). The gap IS exactly mean-vs-max: averaging controls the mean, Frankl needs the max.

**Counter-example (if any):** n/a (no false claim). Obstruction witnesses: the cube `2^[k]` (cover=1/2, Reimer tight, all k) and the 6 lopsided families (cover < 1/2, true abundance high). The **second-moment/power-mean candidate** `max ≥ (Σab²)/(Σab)` (Sec.6) was tested and **REFUTED as a standalone certificate**: it keeps the cube at exactly 1/2 (good) but STILL dips below 1/2 (min 0.444, e.g. {∅,{4},{0,1,2,3,4}}, ab=[⅓,⅓,⅓,⅓,1]). It helps only IF union-closure supplies a genuine lower bound g(m,n) on Σ_i freq_i² — an OPEN question, not established.

**Pointer to artifacts:** `frankl/theory/lp_duality.md`; `frankl/experiments/lp_duality.py` (`lp_min_max_abundance`, `lp_cover_certificate`, `reimer_bound`, `order_ideal_valid_inequalities`, `power_mean_bound`); `frankl/experiments/data/lp_sweep_n{0..5}.jsonl`, `lp_summary.{txt,json}`, `lp_duality_run.txt`; tests `tests/test_uc.py::TestLPDuality` (4 pass; full suite 63 pass).

**Verdict:** gap-not-closeable from the averaging/cover LP dual (sharp obstruction: cube saturates at exactly 1/2 with degenerate certificate; real sub-1/2 integrality gap). Same Boolean-cube killer as the entropy/polynomial/lattice/Fourier/shadow methods already catalogued above.

**Lesson:** (i) The naive "free weighting" LP is vacuous and is the budget-mismatch trap in LP clothing — the measure must be fixed to uniform; union-closure adds no linear constraint on a free measure's abundance vector. (ii) The correct LP dual IS Reimer's averaging, which is sharp on cubes at exactly 1/2 by design, so the LP inherits a hard 1/2 ceiling. (iii) The relaxation gap is precisely max-vs-mean (the spread/variance of the frequency vector). The single live lever is a **second-moment ("variance") valid inequality** `Σ_i freq_i² ≥ g(m,n)` from union-closure feeding the power-mean bound — it would close the gap while leaving the cube at 1/2, but the naive power-mean is insufficient and the existence of `g` is open (needs Reimer-pairs / Kleitman-correlation literature; arXiv blocked). `[NOVELTY UNVERIFIED]`.

## 2026-06-03 — [track: frankl] — Second-moment / variance valid inequality (the LP-duality lever)

**Agent / author:** Second-moment theory agent (AI-assisted), for Alex Ye. `[NOVELTY UNVERIFIED — second-moment / Reimer-on-pairs framings of Frankl very likely prior art (Reimer 2003 average-set-size; Kleitman-style correlation); arXiv 403 this session.]`
**Time invested:** ~1 session theory + full sweep over all 29,723 UC orbit reps (|F|≥2, n≤5), exact integer arithmetic.
**Attack vector:** The ONE concrete lever the LP-duality attack surfaced (`lp_duality.md` §6, "Candidate 6.2," the single live sub-direction): a **second-moment (variance) valid inequality** `Σ_i freq_i² ≥ g(|F|,n)` from union-closure, feeding the power-mean bound `max_i ab_i ≥ (Σ ab_i²)/(Σ ab_i) = M_2/(m M_1)`. The naive power-mean was already refuted as a standalone certificate (dips to 0.444); the open question was whether union-closure ITSELF forces a structural lower bound on `M_2 = Σ freq_i²` strong enough to push max-abundance up. Plan: (a) identify what `M_2` counts; (b) test the strongest `g(m,n)` holding on all families; (c) decide whether the cube minimizes the power-mean ratio; (d) analyze the union term `U=Σ_{A,B}|A∪B|` and the join multiplicities `r(C)=#{(A,B):A∪B=C}`. Artifacts: `frankl/experiments/second_moment.py`, `second_moment_probe.py`.

**Why it failed (the lever caps at exactly ½ — a SEVENTH obstruction):**
1. *Exact identity (task a, PROVED + verified, 0 violations).* `M_2 = Σ_i freq_i² = #{(i,A,B):i∈A,i∈B} = Σ_{(A,B)∈F×F}|A∩B|` (double counting), and by inclusion–exclusion `|A∩B|=|A|+|B|−|A∪B|`, `M_2 = 2m·M_1 − U` with `U:=Σ_{A,B}|A∪B|` and `M_1:=Σ freq_i=Σ_A|A|`. Union-closure enters via `A∪B∈F`: `U=Σ_{C∈F}|C|·r(C)`, `r(C)=#{(A,B):A∪B=C}`, `Σ_C r(C)=m²`. So the second moment is the TOTAL pairwise-intersection size over `F×F` — a correlation quantity. Verified to exact integer equality on all 29,723 families.
2. *No structural lower bound from union-closure (task b, d).* To LOWER-bound `M_2=2mM_1−U` one needs an UPPER bound on `U`. The only closure-aware upper bound is `|A∪B|≤|T|` (`T=⋃F∈F` is a member), giving `M_2 ≥ 2mM_1 − |T|m²`. This holds (0 violations) but is **strictly weaker than the parameter-free Cauchy–Schwarz floor `M_2 ≥ M_1²/n_active` on ALL 29,723 families** (Cauchy–Schwarz strictly tighter on 29,723; the union bound on 0). The Cauchy–Schwarz floor uses NO union-closure (it is the raw vector identity, already known refuted). So no `g(m,n)` stronger than the trivial floor survives.
3. *The cube minimizes the power-mean ratio at its parameters (task c — the obstruction).* `R(F):=M_2/(m M_1)=(Σ ab_i²)/(Σ ab_i)=½` exactly on `2^[k]` (flat vector `freq_i=2^{k-1}`; `M_2=k·4^{k-1}`, `M_1=k·2^{k-1}`, `m=2^k`). For FIXED `(m,M_1)`, `R` is minimized by the flat vector (convexity of `x↦x²`/Cauchy–Schwarz equality); the cube IS the flat vector at its parameters, so `min R = ½` in every cube class (verified `(m,M_1)∈{(2,1),(4,4),(8,12),(16,32),(32,80)}`). Like averaging (LP), this convex/symmetric functional is saturated at its boundary by the flat extremizer — it can never certify `max ≥ ½+ε`.
4. *The dips below ½ are real but HARMLESS and USELESS (task e).* The RAW `R(F)` dips to **0.444** (min over n≤5, at freqs `[1,1,1,1,2]`, `m=3`), reproducing `lp_duality.md` §6; exactly 6 families have `R<½`. DECISIVELY: among the **39** families with true abundance EXACTLY ½ (the Frankl-tight families, incl. all cubes), `R` is exactly ½ — **min=max=0.500000, 0 with R<½**. Every sub-½ dip occurs at abundance STRICTLY > ½ (the `[1,1,1,1,2]` witness has abundance 2/3). So `R<½` never coincides with a would-be counterexample (harmless), and `R≥½` is FALSE as a universal inequality (useless as a certificate) — pinned at ½ on the cube, undercut below ½ elsewhere.
5. *Multiplicity `r(C)` sub-direction has the WRONG SIGN (task d).* `r(C)≥1` for `C∈F` (via `A=B=C`); `r(T)>1` on every family (`r(T)=1` on 0/29,723). But `U=Σ_C|C|r(C)` and we need `U` SMALL to make `M_2` large, so a LOWER bound on `r(C)` (which union-closure gives) pushes `U` UP, weakening the `M_2` bound. The high-`|C|` (large set) terms carry the most weight exactly where `r(C)` is large. Dead end.

**Counter-example (if any):** n/a (no false claim). Obstruction witnesses: the cube `2^[k]` (`R=½` exactly, minimizes `R` at its `(m,M_1)`, all k) and the 6 lopsided families with `R<½` (min 0.444, e.g. freqs `[1,1,1,1,2]`, abundance 2/3 > ½). The 39 abundance-½ families all have `R≡½` — the lever and true abundance decouple precisely on the tight cases. NOTE: the 0.444 is the HONEST value of `(Σ ab²)/(Σ ab)` (like `lp_duality.md`'s 0.40 averaging value), NOT a budget-mismatch artifact; the trap avoided is reading `R<½` as evidence against Frankl (Finding 3.2 shows it never co-occurs with abundance ½).

**Pointer to artifacts:** `frankl/theory/second_moment.md`; `frankl/experiments/second_moment.py` (`family_stats`, `candidate_bounds`, `boolean_cube_reference`, `sweep`), `second_moment_probe.py` (per-`(m,M_1)` cube-minimizer check, union-bound-vs-Cauchy–Schwarz, `r(top)`); `frankl/experiments/data/secmom_n{0..5}.jsonl`, `secmom_summary.txt`, `secmom_run.txt`.

**Verdict:** gap-not-closeable from the second-moment / variance valid inequality (sharp obstruction: cube minimizes the power-mean ratio `M_2/(mM_1)` at its parameters, pinning it at exactly ½; the only closure-aware `M_2` lower bound is dominated by trivial Cauchy–Schwarz; the multiplicity route has the wrong sign). Same Boolean-cube killer as the entropy/polynomial/lattice/Fourier/shadow/LP methods. **Seventh delimited method.**

**Lesson:** The second moment `Σ freq_i² = Σ_{A,B}|A∩B|` is the VARIANCE partner of Reimer's first moment `Σ freq_i = Σ_A|A|` (`Var = M_2/n − (M_1/n)²`). The Boolean cube is the flat extremizer that MINIMIZES variance at fixed mean, so asking the second moment to certify `max > mean` fails on exactly the family where `max = mean = ½`. This is the SAME trivial-spectrum collapse as the quadratic Boolean-Fourier method (`Σ ab_i²` is a quadratic in the signed level-1 coefficients `f̂({i})=p(1−2ab_i)`, all zero on the cube) — the two obstructions are one fact seen through power-mean vs. Parseval. Union-closure's content (`A∪B∈F`, encoded in `U=Σ_C|C|r(C)`) constrains `U` only from BELOW (via `r(C)≥1`), the wrong direction for a second-moment LOWER bound. The seventh method confirms the project-wide convergence: the missing lever is the **labelling of join-irreducibles by ground elements** (open problem F.2), not any symmetric/convex functional of the frequency vector. `[NOVELTY UNVERIFIED]`.

## 2026-06-03 — [track: frankl] — Join-irreducible / fibre-labelling: principal & co-atom fibres fail; cube is the unique worst-labelling extremizer

**Agent / author:** Fibre/JI-labelling agent (AI-assisted), for Alex Ye. `[NOVELTY UNVERIFIED — Birkhoff JI representation (1937) and the fibre=filter / Poonen dictionary are classical; the quantitative fibre-overlap framing very likely folklore; arXiv 403 this session.]`
**Time invested:** ~1 session theory + full sweeps over all 29,723 UC orbit reps (|F|≥2, n≤5), exact arithmetic; exact lattice-iso classification into 13,734 classes.
**Attack vector:** Attack the fibre/JI system DIRECTLY (the chokepoint the six methods converge on, `lattice_attack.md` §1.4, open problem F.2), NOT via any lattice/spectral/LP invariant. Each `Fib(x)={A:x∈A}` is a filter of `L=(F,∪)`; `abundance=max_x|Fib(x)|/|L|`. Tested H1 (principal/JI fibres), H2 (co-atom/meet-irreducible fibres), H3 (counting identity), H4 (rigid lattices), H5 (labelling freedom: min over realizations of max-abundance, per exact iso class). Artifacts: `frankl/experiments/ji_labelling.py`, `ji_labelling_sweep.py`, `ji_labelling_constraint.py`, `ji_labelling_h5.py`.

**Why it failed (principal/co-atom fibres NEVER suffice; the labelling freedom bottoms out exactly at the cube):**
1. *Reconstruction identity (R), PROVED-form + verified 0 violations.* `Fib(x) = ⋃_{j∈JI, x∈j} ↑j` — every fibre is the UNION of the principal join-irreducible filters of the JIs containing `x`. This is the exact coupling the invariant methods throw away (the fibre system must reconstruct `F`: `A={x:A∈Fib(x)}`). Verified on all 29,723 families.
2. *H1 FALSE — single join-irreducible filters are the WRONG object.* `min` over families of `max_j|↑j|/|L|` (best single JI-filter density) `= 0.2353` (≪ ½). In **2,254** families abundance `≥ ½` while NO single JI-filter reaches ½; in **11,230** families abundance STRICTLY beats the best single JI-filter (max gap 0.5833). Clean witness M3 (`{∅,{0,1},{0,2},{1,2},{0,1,2}}`): every fibre non-principal (`x∉m_x`), each JI-filter density 0.4, each fibre = union of TWO JI-filters sharing the top ⇒ abundance 0.6. ONE positive: `abundance ≥ max_j|↑j|/|L|` always (29,723/29,723) — a genuine but USELESS lower bound (dips to 0.2353).
3. *H2 FALSE, worse.* Co-atom/meet-irreducible fibres are the SMALL end (`↑c={c,T,…}`, density `2/|L|`): some co-atom filter `≥ ½` in only **133** families. Abundance lives at the join-irreducible (bottom) end, in UNIONS — confirming the JI-labelling, not the MI structure, is the locus.
4. *H3 is the averaging identity again.* `Σ_x|Fib(x)|=Σ_A|A|` (0 violations) is the SAME first-moment identity that `lp_duality.md` (1.1) caps at the mean (cube pins at ½). No forcing from H3 alone — it is max-vs-mean.
5. *H5 — the labelling-freedom characterization (the deliverable).* Over **13,734 exact lattice-iso classes** (strong fingerprint + back-tracking cover-digraph iso): `minab(L) < ½` in **0** classes (Frankl on every class); `minab(L) = ½ EXACTLY` in **exactly 5** classes — and those are PRECISELY the **Boolean cubes `B_k`** (`|L|∈{2,4,8,16,32}`, realized at the min by the standard cube `2^[k]`); `minab(L) > ½` in all **13,729** other classes. **The Boolean cube is the UNIQUE lattice whose worst labelling reaches the FUCC boundary ½.** [PENDING — n≤5; cube part exact for all k, but a non-cube lattice could in principle realize ½ at larger n.]

**Counter-example (if any):** n/a (no false claim). Obstruction witnesses: M3 (H1/H2 fail: single JI-filter 0.4 < ½ < 0.6 abundance, principal fibres impossible) and the cube `2^[k]` (the UNIQUE minab=½ extremizer; JIs are the `k` singletons, each `↑{i}` density ½, fibres principal, no union effect). The 2,254 union-essential families (abundance `≥ ½`, every single JI-filter `< ½`) are the explicit counter-examples to "principal fibres certify Frankl."

**Pointer to artifacts:** `frankl/theory/join_irreducible_labelling.md`; `frankl/experiments/{ji_labelling,ji_labelling_sweep,ji_labelling_constraint,ji_labelling_h5}.py`; `frankl/experiments/data/ji_sweep_n{0..5}.jsonl`, `ji_summary.txt`, `ji_constraint_summary.txt`, `ji_h5_summary.txt`, `ji_h5_classes.jsonl`; `tests/test_ji_labelling.py` (9 tests).

**Verdict:** principal (single-JI) and co-atom/meet-irreducible fibres NEVER suffice as a stand-alone certificate; the only positive is the weak lower bound `abundance ≥ max_j|↑j|/|L|`. The labelling freedom (the cone mechanism) bottoms out at exactly ½ ONLY on the Boolean cube — the unique extremizer. Same cube killer, now at the FIBRE LEVEL.

**Lesson:** Abundance is a **union-of-join-irreducible-filters** quantity, not a single-filter one (H1/H2 dead). The right next lever — CONVERGENT with the parallel second-moment agent's entry above, which independently lands on "the labelling of join-irreducibles" — is a union-closure LOWER bound on the **JI-filter OVERLAP** `Σ_{j,k}|↑j∩↑k|` (all `↑j∋T`, so overlaps are structured: `↑j∩↑k⊇↑(j∨k)`), feeding a Cauchy–Schwarz/power-mean bound on the heavy union `max_x|Fib(x)|`. This is the `lp_duality.md` §6 second-moment lever **localized to the JI-labelling**: tight on the cube (overlaps all the generic shared `T`/up-sets, abundance ½ — consistent with H5 cube-uniqueness), so at best REACHES ½, never exceeds. Whether union-closure forces such an overlap lower bound is OPEN. NOTE the avoided trap: the sub-½ numbers here (single-JI density 0.2353) are honestly *failed lower bounds* ("single JI is the wrong object"), NEVER dressed up as a certificate — distinct from the 0.43/0.5 budget-mismatch artifacts. `[NOVELTY UNVERIFIED]`.

## 2026-06-03 — [track: frankl] — The JI-filter OVERLAP inequality (the convergence crux) is FALSE

**Agent / author:** JI-overlap agent (AI-assisted), for Alex Ye. `[NOVELTY UNVERIFIED — fibre 2nd-moment identity is classical double-counting; JI-overlap framing very likely folklore; arXiv 403 this session.]`
**Time invested:** ~1 session compute + theory.
**Attack vector:** The 28-agent convergence (JI-labelling agent's Candidate 6.1 + second-moment agent) pinned the crux as a union-closure LOWER bound on the join-irreducible filter overlap `Σ_{j,k}|↑j∩↑k|`, using `↑j∩↑k ⊇ ↑(j∨k)`, feeding a Cauchy–Schwarz/power-mean bound `max_x|Fib(x)| ≥ Σ_x|Fib(x)|²/Σ_x|Fib(x)|` to force a heavy fibre ≥ |L|/2 (Frankl), tight on the cube. Plan: state the exact sufficient overlap inequality, test on all 29,723 families n≤5, attempt to prove it from union-closure.

**The exact identity (correct, verified 0/29723):** `P₂ := Σ_x|Fib(x)|² = Σ_{(A,B)∈L×L}|A∩B| =: OVL(L)` (swap summation order). Power-mean over ground elements gives `max_x|Fib(x)| ≥ P₂/P₁` with `P₁ = Σ_A|A|`. So the SUFFICIENT overlap inequality for Frankl is **(TARGET-F)** `2·OVL ≥ |F|·Σ_A|A|` (equivalently power-mean density ≥ ½).

**Why it failed (the inequality is FALSE):**
1. *TARGET is FALSE.* TARGET-F fails on **6** families, TARGET-L (threshold |L|/2) fails on **12** families (n≤5). Power-mean density dips to **0.4444 < ½** — the exact 0.444 of `lp_duality.md §6` / `second_moment.md §3`, now as a fibre-overlap quantity. Minimal counterexample `F={∅,{4},{0,1,2,3,4}}` (masks [0,16,31]): freq vector `[1,1,1,1,2]`, P₁=6, P₂=OVL=8, density (8/6)/3 = 4/9 = 0.444 < ½, but TRUE abundance 2/3 > ½. Same near-universal-heavy-element + parasites family that defeated LP averaging and raw 2nd moment.
2. *The brief's structural hook has ZERO slack (the decisive reason).* `↑j∩↑k ⊇ ↑(j∨k)` is in fact an **EXACT identity** `↑j∩↑k = ↑(j∨k)` in ANY lattice — a tautology of the join (`a≤x ∧ b≤x ⟺ a∨b≤x`). Verified 0 violations / 25,668 pairs (ALL pairs, not just JI). So `Σ_{j,k}|↑j∩↑k| = Σ_{j,k}|↑(j∨k)|` exactly on all 29,723 families (ratio ≡ 1.0). The `⊇` the convergence hoped to leverage supplies NOTHING to bound below; the join pins the overlap to its exact value.
3. *No localization gain.* By the identity, `P₂ = OVL(L) = Σ_{A,B∈F}|A∩B|` IS the `second_moment.md` object M₂ (∅ adds 0). The "JI-localized" overlap lever and the raw second-moment lever are the SAME inequality — inheriting verbatim all of second_moment.md's obstructions (cube minimizes the ratio, 0.444 dips, no closure-side lower bound).

**Counter-example:** `F={∅,{4},{0,1,2,3,4}}` (masks [0,16,31], n=5), power-mean density 4/9=0.444 < ½, true abundance 2/3. Full list (6) in `frankl/experiments/data/overlap_counterexamples.txt`.

**Cube tightness / discipline check (PASS):** the cube `2^[k]` (k=1..5) satisfies TARGET with **exact equality** (slack `2·OVL−|L|·P₁ = 0` and `2·OVL−|F|·P₁ = 0`); all 63 abundance-½ families (L-norm) / 39 (F-norm) saturate with equality. Every TARGET FAILURE has true abundance ≥ 0.5714 > ½ — the inequality fails ONLY strictly above the Frankl threshold (harmless: no false refutation possible; useless: genuinely false so cannot certify). No proof of Frankl produced, hence none to break; the cube-uniqueness discipline is respected.

**Residual gap:** exactly the **max-vs-mean spread** (`P₂/P₁` is a fibre-size-weighted mean; Frankl needs the max). On flat families (cube) mean=max=½ (lever tight); on spread/lopsided families mean<½<max (lever loose by the spread). The overlap identity provides no upper bound on the spread.

**Pointer to artifacts:** `frankl/theory/ji_overlap_inequality.md`, `frankl/experiments/ji_overlap.py`, `frankl/experiments/data/overlap_n{0..5}.jsonl`, `overlap_summary.{txt,json}`, `overlap_counterexamples.txt`.

**Verdict:** gap-not-closeable (the sufficient overlap inequality is false; the structural hook `↑j∩↑k⊇↑(j∨k)` is a slack-free tautology; the lever reduces to the already-dead second moment).

**Lesson:** The 28-agent convergence's "single most promising lever" is a **characterized dead end**. The fatal one-liner is **Lemma 3.1: `↑a∩↑b = ↑(a∨b)` exactly in any lattice** — the join-irreducible filter overlaps are *determined* by the lattice's join, leaving NO inequality for union-closure to amplify; and `Σ_x|Fib(x)|² = Σ_{A,B}|A∩B|` makes the "JI-localized overlap" literally equal to the raw second moment (`second_moment.md`), which already caps at ½. This is the EIGHTH delimited method, coinciding with the second-moment method, with the same cube extremizer and the same max-vs-mean residual gap. To progress, a NEW ingredient is needed that is NOT a symmetric convex moment of the frequency/fibre vector (all such are flat-minimized by the cube at exactly ½). NOTE on traps: the 0.444 here is the HONEST power-mean value (like `lp_duality.md`'s 0.40 averaging value), NOT a budget-mismatch artifact — Finding 2.2 shows it decouples from true abundance, never co-occurring with an abundance-½ family. `[NOVELTY UNVERIFIED]`.

## 2026-06-03 — [track: frankl] — Generator-incidence (NON-SYMMETRIC) attack: separable generator-asymmetric quantities all fail; one unproven invsize pick rule presumed flawed

**Agent / author:** Generator-asymmetric agent (AI-assisted), for Alex Ye. `[NOVELTY UNVERIFIED — Birkhoff/Poonen generator (join-irreducible) representation classical; singleton lemma folklore; invsize pick rule flagged new but PRESUMED FLAWED. arXiv 403 this session.]`
**Time invested:** ~1 session theory + compute. Full sweep over all 29,723 UC orbit reps (|F|≥2, n≤5, ∅ adjoined) + ~660,000 larger-n break-attempt families (random + targeted + exhaustive n=6 small-generator).
**Attack vector:** The ONE class the BARRIER THEOREM (PROGRESS.md) does not immediately kill — NON-SYMMETRIC, generator-incidence quantities. A UC family is exactly `F = {⋃S : S⊆G}` for its generators `G` = join-irreducibles (members not a union of strictly smaller members). Encode `G` as the incidence matrix `M[g,x]=1⟺x∈g`. Express abundance via `M` and the union-lattice; test asymmetric weightings (by generator size / filter size / lower-cover rank / generation order), the "most frequent generator element" heuristic, deletion/induction pivots, and the Knill/Wójcik generator graph. Goal: a non-symmetric quantity forcing max abundance ≥ ½, OR an extension of the barrier to generator-asymmetric methods. Artifacts: `frankl/experiments/generator_attack.py`.

**Why it failed (the barrier EXTENDS to separable generator-asymmetric methods):**
1. *Generator-incidence formula (exact, PROVED-form + verified 0/29,723).* `F={⋃S:S⊆G}` and `freq(x)=|Fib(x)|`, `Fib(x)=⋃_{g∋x}↑g` (R-gen, the union-of-generator-filters identity; verified 0 violations / 148,164 (x,F) pairs). KEY: abundance is a **non-separable UNION (overlap) size** of generator filters, not a separable sum of per-generator contributions.
2. *"Most frequent generator element ≥½-abundant" is FALSE.* The element maximizing `gfreq(x)=#{g∈G:x∈g}` (column sums of `M`) has true abundance <½ in **356** families, min **0.3333**; picks the genuinely abundant element in only 20,909/29,723. Clean minimal counterexample `G={{2},{0,1,2},{3},{0,1,3}}` (|L|=7): `gfreq≡2` flat (every element in exactly 2 generators), tie-break picks x=0 (freq 3/7<½), but the abundant elements 2,3 (freq 4/7>½) are the ones in the SMALL generators {2},{3} that the bare count ignores.
3. *All four generator-weighted abundances FAIL and give the CUBE SLACK (a NEW failure mode).* Weight `g` by `|g|`, `1/|g|`, `|↑g|`, or lower-cover rank; `Wab(x)=(Σ_{g∋x}w(g))/Σ_g w(g)` drops to **0.200** on `2^[5]` and fails <½ on 180–3,116 families. On `2^[k]` every weighted abundance = `1/k`, NOT ½ — the cube is the WORST case for these (opposite to the eight symmetric methods, which the cube flat-minimizes AT ½). By the cube-equality discipline this disqualifies the whole weighted-abundance family immediately.
4. *One non-symmetric PICK RULE survives — but its new half is PRESUMED FLAWED.* The combined rule: (i) if a singleton generator {x} exists, pick x; (ii) else pick x = argmax invsize(x), `invsize(x)=Σ_{g∋x}1/|g|` (`Σ_x invsize=|G|`). On n≤5: **0 failures, min exactly ½, 377 equality cases, cube=½ exactly.** Branch (i) is the CLASSICAL singleton case ({x}∈F ⇒ freq(x)≥|F|/2 via the injection A↦A∪{x}; folklore, NOT new; covers 23,741/29,723). Branch (ii) is genuinely non-symmetric (in 652/5,982 no-singleton families invsize-argmax ≠ freq-argmax yet still ≥½) and genuinely NEW — but has NO PROOF.

**Red-team of the invsize branch (PRESUMED FLAWED):** survives exhaustive n≤5 (5,982 no-singleton families, 0 fail, min ½), 400,000 random n=6,7,8, 200,019 targeted near-extremal (M_t / M3×M3 / dense 2-gen graphs, worst 0.5192), exhaustive n=6 small-generator (57,560 distinct, worst exactly ½), and hand-built adversarial families — 0 counterexamples. BUT it is presumed flawed structurally: the separable certificate `abundance(x) ≥ invsize(x)/|G|` is **FALSE (12/29,723 violations)**, so no per-element separable bound underwrites the pick; and by R-gen the true quantity is a non-separable union size whose argmax has no structural reason to match a separable proxy's argmax (the union is depressed by filter overlap, which invsize ignores). This is the barrier reasserting itself: invsize is non-symmetric (good) but separable (bad). Almost certainly a finite-n coincidence.

**Counter-example (if any):** To the FALSE heuristics: `G={{2},{0,1,2},{3},{0,1,3}}` (gfreq flat at 2, abundant elements 2,3 in the small generators, gfreq-pick x=0 only 3/7). To the separable certificate C1: 12 families violate `abundance(x)≥invsize(x)/|G|`. NO counterexample found to the combined pick rule itself (it is presumed flawed for lack of proof, not falsified) — and none is a false refutation (every miss is at a family where Frankl holds via another element; cube saturates at exactly ½).

**Pointer to artifacts:** `frankl/theory/generator_asymmetric.md`; `frankl/experiments/generator_attack.py`; `frankl/experiments/data/genattack_n{0..5}.jsonl`, `genattack_summary.{txt,json}`, `genattack_redteam.txt`.

**Verdict:** gap-not-closeable from SEPARABLE generator-asymmetric quantities (the barrier extends: incidence count false, all weighted abundances fail + mis-handle the cube, separable certificate C1 false). The combined pick rule's singleton branch is the folklore singleton case; its invsize branch is an UNPROVEN heuristic, presumed flawed (non-separability), NOT a proof of Frankl.

**Lesson:** The generator incidence matrix `M` IS the right non-symmetric language (Identity 1.1 / R-gen exact), and the barrier's prediction is confirmed sharply: abundance is a **non-separable overlap of generator filters**, so every SEPARABLE function of `M` (count, size/filter/rank-weighted abundance, the C1 certificate) fails, and the cube — which the symmetric moments flat-minimize at ½ — is instead the WORST case for generator weights (they drop to 1/k). The only object that empirically clears ½ with cube equality is a non-symmetric *selector* (invsize argmax) with no certificate and a clear non-separability reason to distrust. The residual target is exactly the non-separable object `ji_overlap_inequality.md` showed the symmetric overlap moment cannot reach: a union-closure control on the OVERLAP of the generator filters `↑g` over the generators sharing a fixed element. The barrier now covers symmetric moments AND separable generator-asymmetric methods. `[NOVELTY UNVERIFIED]`.

*(append further entries above this line as approaches fail)*
