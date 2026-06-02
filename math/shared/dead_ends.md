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

*(append further entries above this line as approaches fail)*
