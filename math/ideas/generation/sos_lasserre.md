# Sum-of-squares / Lasserre / Positivstellensatz (degree ≥ 4) on Frankl

**Author:** Alex Ye (no AI on author line).
**Date:** 2026-06-03.
**Field assignment:** SOS / Lasserre / Positivstellensatz hierarchies, degree ≥ 4.
**Status:** DIRECTION, not a proof. `[NOVELTY UNVERIFIED — Lasserre/SOS relaxations
of extremal set-theory problems exist (Raymond–Saunderson–Singh–Thomas; Bachoc–Vallentin
flag-SOS; Gribling–de Laat–Laurent); a Frankl-specific incidence-variable Lasserre
formulation is flagged new but is plausibly folklore in the SOS community. arXiv 403
this session.]`
**Companion code (this dir):** `sos_probe.py`, `sos_probe2.py`, `sos_validate.py`.
**Does NOT touch** `frankl/paper/`, `collatz/paper/`, or any `theory/`/`experiments/`
file. All work is under `ideas/generation/`.

> **One-paragraph verdict.** The project's moment/LP barrier is precisely the
> **Lasserre level 1** (degree-2) relaxation *over the incidence variables, after
> S_n symmetry reduction*. I make that identification exact (proved + verified
> n≤3: the S_n-invariant level-1 incidence invariants partition all UC families
> into *identically the same cells* as the degree-2 frequency pair-statistics —
> 9 cells at n=2, 37 at n=3). So degree-2 SOS provably collapses to the barrier.
> **Going higher is NOT automatically barred**, because the S_n-invariant
> *level-2* incidence moments `L[y_S y_T y_U]`, `L[y_S y_T y_U y_V]` are
> orbit-functions of **subset-triples/quadruples** — they are symmetric in the
> *ground set* but are NOT moments of the *frequency vector*, so the barrier
> theorem (which is exactly "symmetric convex moments of the frequency vector")
> does not cover them. This is the one genuine crack. **BUT** the cube ceiling is
> degree-independent: I verify rigorously (honest 0/1 moment vector, no solver)
> that the Boolean cube `2^[k]` is PSD-feasible at level 2 with abundance exactly
> 1/2 for every `k`, so **no Lasserre level can ever certify abundance > 1/2** —
> the most any level-d relaxation can do is *reach* 1/2. The live, unresolved
> question is whether level d≥2 reaches 1/2 *where level 1 falls short* (the
> lopsided sub-½ families of `lp_duality.md`/`ji_overlap.md`). My sandbox SDP
> solver (alternating projection; no cvxpy/mosek) is reliable at level 1 but has a
> non-convergence floor at level 2, so this is left as the concrete next probe for
> an environment with a real SDP solver. **Plausibility 2/5.**

---

## 1. The polynomial-optimization formulation

### 1.1 Variables = the incidence/decision bits, NOT the frequency vector

This is the whole point. Fix `n`. The "universe of possible members" is all `2^n`
subsets `S ⊆ [n]`. A union-closed family `F` is a subset of `2^[n]`, encoded by
**incidence indicators**
$$
y_S \in \{0,1\}, \qquad y_S = 1 \iff S \in F \qquad (S \subseteq [n]).
$$
There are `2^n` Boolean variables `y_S`. The frequency of a ground element `i` and
the family size are **linear** forms in `y`:
$$
\mathrm{freq}_i \;=\; \sum_{S \ni i} y_S, \qquad M := |F| \;=\; \sum_{S} y_S .
$$

### 1.2 Frankl as 0/1 polynomial *infeasibility*

A union-closed family is a counterexample iff every element is non-abundant,
`2\,\mathrm{freq}_i \le M-1` for all `i`. So

> **(FRK-n)** *Frankl holds on `[n]`* ⟺ *the following 0/1 system is **infeasible**:*
> $$
> \begin{aligned}
> &y_S^2 = y_S &&\text{(BOOL)}\\
> &y_A\,y_B\,(1 - y_{A\cup B}) = 0 &&\forall A,B \subseteq [n] \quad\text{(UNION-CLOSURE)}\\
> &M - 2\,\mathrm{freq}_i - 1 \ge 0 &&\forall i \in [n] \quad\text{(NOT-ABUNDANT)}\\
> &M - 2 \ge 0 &&\text{(nondegenerate)}.
> \end{aligned}
> $$

A **degree-`2d` Positivstellensatz refutation** of this system *is* a proof of
Frankl on `[n]`. Dually, the **Lasserre level-`d` pseudo-moment SDP** is feasible
iff no degree-`2d` refutation exists:

> **(LAS-d)** A *level-`d` pseudo-expectation* is a linear functional `L` on
> polynomials in `y` of degree ≤ `2d` with `L[1]=1`, the **moment matrix**
> `M_d(L) = (L[u\,v])_{u,v}` (rows = monomials of degree ≤ `d`) PSD, each
> **localizing matrix** `L[g_j \cdot u\,v]` PSD for the inequalities `g_j ≥ 0`, and
> `L[h \cdot u] = 0` for the equalities `h = 0` (BOOL + UNION-CLOSURE).  *(LAS-d)*
> feasible ⟺ no degree-`2d` certificate ⟺ Frankl unproven at that degree.

Because `y_S^2 = y_S` is in the ideal, every monomial reduces to a **squarefree**
monomial = a *set* of variables, so the moment indexed by `{S_1,…,S_k}` is
`L[y_{S_1}\cdots y_{S_k}] = \Pr`-like co-membership of the named subsets
`S_1,…,S_k`. This bookkeeping is implemented exactly in `sos_probe.py` /
`sos_probe2.py`.

### 1.3 Which level, and why it could escape the degree-2 barrier

**Propose level `d = 2` (degree-4), with the level-3 (degree-6) probe as fallback.**
The reason is structural, argued in §2: level 1 *is* the barrier; the first level
whose invariant moments are not frequency-moments is level 2.

---

## 2. Why this is genuinely beyond symmetric convex moments — and where it isn't

### 2.1 The symmetry-reduction theorem (the load-bearing argument)

`S_n` acts on `[n]`, hence permutes subsets `S`, hence permutes the variables
`y_S`, hence acts on pseudo-expectations by `(\sigma\!\cdot\!L)[p] = L[p\circ\sigma^{-1}]`.

> **Lemma 2.1 (invariance of the feasible set).** The constraint set of *(LAS-d)*
> is `S_n`-invariant: UNION-CLOSURE relations permute among themselves
> (`g_{A,B}\mapsto g_{\sigma A,\sigma B}`), BOOL relations permute among
> themselves, the *family* `{`NOT-ABUNDANT`_i\}_{i}` permutes among itself
> (`h_i\mapsto h_{\sigma i}`), and `M`, the PSD conditions are invariant. Hence if
> `L` is feasible so is `\sigma\!\cdot\!L`, and (feasible set convex) so is the
> average `\bar L = \tfrac1{n!}\sum_\sigma \sigma\!\cdot\!L`, which is
> `S_n`-**invariant**.

> **Corollary 2.2.** *(LAS-d)* is feasible ⟺ it has an `S_n`-**invariant** feasible
> point. So at *every* level we may restrict to `S_n`-invariant `L` without changing
> the feasible/infeasible verdict. *(This is the standard symmetry reduction —
> Gatermann–Parrilo / Bachoc–Vallentin — and it is the same averaging that drives
> the project's barrier.)*

### 2.2 Level 1 = the proven barrier (exactly)

An `S_n`-invariant `L` assigns to each squarefree monomial a value depending only
on the `S_n`-**orbit** of the subset-tuple. At level 1 the moments are:
$$
L[y_S] \ \to\ \text{function of } |S|, \qquad
L[y_S y_T] \ \to\ \text{function of } (|S|,|T|,|S\cap T|).
$$
These are *exactly* the symmetric pair-statistics of `second_moment.md` /
`ji_overlap.md` (the fibre/overlap second moment `\sum_x\mathrm{freq}_x^2 =
\sum_{A,B}|A\cap B|`).

> **Validation 2.3 (rigorous, exhaustive, `sos_validate.py`).** Over *all* UC
> families at `n=2` (13 families) and `n=3` (121 families), the partition induced
> by the `S_n`-invariant **level-1 incidence invariants** *coincides exactly* with
> the partition induced by the **degree-2 frequency pair-statistics**
> `(\,|F|,\ \text{freq multiset},\ \sum_{A,B}|A\cap B|\,)`: **9 cells vs 9 cells**
> at `n=2`, **37 vs 37** at `n=3`, and neither strictly refines the other. ⇒
> **Lasserre level 1 over incidence variables collapses *onto* the degree-2
> symmetric-moment barrier.** *(Corroborated by `sos_probe2.py`: the full-incidence
> and frequency-symmetric level-1 SDPs return identical `min_eig` to ≥3 sig figs
> at every threshold `t`.)*

So degree-2 SOS provably buys **nothing** over the barrier. This is the crisp
"why degree-2 collapses" the brief asks to confirm — and it explains *why* the
project's LP/moment work was the right object to call "the degree-2 relaxation."

### 2.3 Level ≥ 2: orbit-functions of subset-triples are NOT frequency moments

At level 2 the `S_n`-invariant moments newly include
$$
L[y_S\,y_T\,y_U]\ \to\ \text{function of the orbit-type of the triple }(S,T,U),
\qquad L[y_S\,y_T\,y_U\,y_V]\ \text{(quadruples)}.
$$
**These are still `S_n`-symmetric (orbit functions) but they are NOT moments of the
frequency vector.** The barrier theorem is, verbatim, *"every symmetric convex
moment of the frequency vector is flat-minimized by the cube at 1/2."* The
frequency vector's moments live in the algebra generated by the linear forms
`\mathrm{freq}_i`; its degree-`k` symmetric moments are the power sums
`\sum_i \mathrm{freq}_i^k`. But `L[y_S y_T y_U]` records the **co-occurrence type of
three named subsets** (e.g. "how often do three pairwise-incomparable members with
a common pairwise intersection coexist") — a function of the **subset-incidence
configuration**, which does *not* factor through `(\mathrm{freq}_i)_i`. Symmetry
reduction kills the *ground-set* labelling freedom (the exact thing the
`join_irreducible_labelling.md` crux is about) but **does not** lower the
*set-configuration degree*.

> **This is the precise sense in which "go higher" escapes the stated barrier:**
> the barrier is a statement about a *specific, low-dimensional* invariant
> sub-algebra (frequency moments). Level-2 incidence SOS lives in a strictly larger
> invariant algebra. The barrier theorem, as proved, simply does not apply to it.

### 2.4 The catch: the cube ceiling is degree-independent

Escaping the *barrier* is necessary but not sufficient — the cube must still be
allowed to sit at 1/2, or any "proof" would be false.

> **Validation 2.4 (rigorous, no solver, `sos_validate.py`).** For the Boolean
> cube `F = 2^[k]`, the honest 0/1 point `y_S = \mathbf 1[S\in F]` is a genuine
> feasible pseudo-expectation at level 2 (its moment matrix is rank-1 PSD,
> `min\_eig \ge -10^{-14}`, all constraints hold) with abundance **exactly 1/2**,
> for `k=1,2,3` (matrices `4\times4`, `11\times11`, `37\times37`). The same
> construction works at *every* level and every `k`.

> **Corollary 2.5 (degree-independent ceiling).** Since the cube provides a
> feasible level-`d` point at abundance 1/2 for all `d`, **no Lasserre/SOS level can
> certify abundance `> 1/2`.** Every level-`d` relaxation can at best *reach* 1/2.
> The "does the degree-4 certificate stay flat on the cube?" test → **yes, the cube
> stays flat at all degrees**; the cube is a degree-independent extremizer.

So the *only* possible win from higher degree is the **conditional** one: certify
`abundance \ge 1/2` (reach the ceiling) on the families where level 1 certifies
strictly less — the lopsided "one near-universal element + parasites" families
where the frequency second moment dips to 0.444 (`lp_duality.md` §6,
`ji_overlap.md` §2). The question is whether the level-2 *triple* moments are
constrained by union-closure enough to lift those families to 1/2. That is exactly
what the probe is built to test.

---

## 3. Concrete first step: the degree-4 pseudo-moment SDP for small `n`

`sos_probe.py` / `sos_probe2.py` build *(LAS-d)* for `n ≤ 3` from scratch
(squarefree-monomial moment indexing, UNION-CLOSURE moment equalities, localizing
matrices for NOT-ABUNDANT, optional `S_n`-/frequency-symmetrization). With **no
SDP solver in the sandbox** (`cvxpy`/`mosek`/`scs`/`cvxopt` all absent), feasibility
is tested by **alternating projection** between the affine moment-equality subspace
(exact) and the PSD cone of the stacked moment+localizing matrices.

**Reliable findings (level 1):**

| `n` | level | full-incidence `min_eig` at `t=0.5 / 0.45 / 0.40` | freq-SYM (barrier) | verdict |
|---|---|---|---|---|
| 2 | 1 | `-3e-7 / -5e-7 / -2e-6` | `-3e-7 / -5e-7 / -2e-6` | identical → collapse |
| 3 | 1 | `-2e-12 / -1e-9 / -9e-8` | `-5e-16 / -1e-9 / -9e-8` | identical → collapse, feasible to t=0.4 |

The level-1 full-incidence and barrier SDPs are numerically **indistinguishable**,
confirming Validation 2.3 from the SDP side. (At `n=3`, level 1 is feasible even at
`t=0.40`, i.e. level-1 SOS does **not** prove Frankl for `n=3` on its own — exactly
the barrier's sub-½ gap.)

**Honest limitation (level 2).** The alternating-projection solver has a
non-convergence *floor* at level 2 (e.g. `n=2,d=2` returns `min_eig ≈ -0.12`
*uniformly* across all `t`, including `t=0.5` where the cube makes it provably
feasible — so the floor is a solver artifact, not infeasibility). Therefore the
solver **cannot** decide level-2 feasibility here. The relative full-vs-symmetric
comparison still matches (so symmetry reduction is corroborated), but the absolute
level-2 verdict needs a real SDP solver.

**What to run next (the decisive experiment), in an env with `cvxpy`+`MOSEK`/`SCS`:**
1. Solve *(LAS-2)* (symmetry-reduced via Cor 2.2 — only ~tens of orbit variables)
   for `n = 3,4,5`, computing the certified abundance lower bound `lb_2(n)` =
   smallest `t` with *(LAS-2)* feasible.
2. Compare to `lb_1(n)` (= the barrier value, which dips to 0.444 on the lopsided
   families). **Escape signal:** `lb_2 = 1/2` on a family where `lb_1 < 1/2`.
3. If `lb_2(n) = 1/2` for all UC configurations at `n=4,5` (i.e. level-2 SOS proves
   Frankl for those `n`), extract the dual SOS certificate and inspect whether its
   multipliers are `n`-uniform (→ candidate for an `n`-independent proof) or grow
   with `n` (→ degree must grow, a Lasserre-degree lower bound — itself a publishable
   barrier strengthening).

---

## 4. Small validation on `n ≤ 3` (what is and isn't established here)

- **Established (rigorous):**
  (i) Level-1 incidence SOS ≡ degree-2 frequency-moment barrier (Validation 2.3,
  exhaustive n≤3; partitions coincide 9/9, 37/37).
  (ii) The Boolean cube is PSD-feasible at level 2 with abundance exactly 1/2
  (Validation 2.4, k≤3) ⇒ degree-independent ½ ceiling (Cor 2.5).
  (iii) Level-1 SOS does **not** prove Frankl at `n=3` (feasible at `t=0.40`),
  matching the barrier's sub-½ gap.
- **NOT established (left open by the sandbox's missing SDP solver):** whether
  level-2 (degree-4) SOS lifts the lopsided sub-½ families to 1/2 — i.e. whether
  there is any genuine separation `lb_2 > lb_1`. This is the entire question of
  whether the direction *works*; only the *framework* and the *barrier-collapse at
  level 1* are settled here.

---

## 5. Plausibility, failure modes, novelty

**Plausibility: 2 / 5.** The direction is *logically not excluded* by the proven
barrier (§2.3) — a real and non-obvious point — and the formulation is concrete and
runnable. But three things weigh it down:

- **Failure mode A — collapse-by-tautology (most likely).** The same mechanism that
  flattens level 1 may recur: the UNION-CLOSURE equalities `y_A y_B = y_A y_B
  y_{A\cup B}` may force the level-2 triple-moments to be *determined* by the
  pair-moments (just as Lemma 3.1 of `ji_overlap.md` showed `↑a∩↑b=↑(a∨b)` drained
  all slack from the overlap lever). If the triple invariants are functions of the
  pair invariants modulo the union ideal, level 2 collapses to level 1 and the
  barrier reasserts itself one degree up. This is my central worry and the first
  thing the real-SDP probe should check (compare `lb_2` vs `lb_1` on the 6 lopsided
  n≤5 families).
- **Failure mode B — degree blow-up.** Even if some finite level proves Frankl(n)
  for each `n`, the required level may grow with `n` (a Lasserre-degree lower bound,
  cf. the slice-rank/`polynomial_method.md` finding that the relevant degree is
  `Ω(n)` per coordinate). Then SOS gives no uniform proof — though a *proven* growth
  rate would be a clean, publishable hardness result delimiting the SOS method
  (a positive byproduct of a negative outcome).
- **Failure mode C — ceiling, not floor.** Cor 2.5 caps every level at ½; SOS can at
  most *reach* the conjecture, never give slack, so even full success is "a proof,"
  not "a margin." Fine for Frankl (½ is the target) but means no robustness.

**Novelty:** `[NOVELTY UNVERIFIED]`. The incidence-variable Lasserre formulation of
Frankl and the level-1-is-the-barrier identification are flagged new for this
project but are plausibly known to the SOS community (Raymond–Saunderson–Singh–Thomas
symmetry-reduced SOS for set problems; Gribling–de Laat–Laurent). The genuinely
useful, defensible contributions regardless of prior art are the two *rigorous*
small-`n` facts: **(a)** degree-2 SOS = the barrier (exact, exhaustive n≤3), and
**(b)** the cube ceiling is degree-independent (rigorous, all `k` via the honest
moment vector) — i.e. **SOS can only ever reach ½, and only level ≥ 2 even has a
chance.** If a future real-SDP run shows `lb_2 = lb_1` on the lopsided families,
that is a crisp "SOS collapses to the barrier at degree 4 too" — itself the valid
deliverable the brief allows.

---

## 6. Reproduction

```
cd math/ideas/generation
python3 sos_validate.py     # rigorous, ~seconds: level-1 collapse (n<=3) + cube ceiling (k<=3)
python3 sos_probe2.py       # alternating-projection SDP probe (level 1 reliable; level 2 floored)
python3 sos_probe.py        # earlier variant (decision-form feasibility scan)
```
`sos_validate.py` is the trustworthy artifact (no solver dependence). The two
`sos_probe*.py` scripts are throwaway SDP probes whose level-2 verdicts are *not*
reliable without a real SDP backend (`cvxpy`+`MOSEK`/`SCS`); they are kept for the
level-1 corroboration and as the scaffold for the decisive level-2 run.
