# The Entropy-Method Optimization: Precise Formulation

**Track:** Frankl Vector 3 (joint optimization + certification)
**Author:** Alex Ye (AI assistance disclosed separately)
**Status:** `[step-1 passed]` for the base reduction (= ψ); see §6 for what is and is not certified.
**Companion code:** `joint_opt.py`, `certificate_0.38197.md`, `results.md`.

This document states the exact objective and constraints of the entropy-method
optimization, citing the paper each constraint comes from. Every inequality is
**direction-checked** and the base reduction is numerically verified to reproduce
`ψ = (3 − √5)/2`. The point of this file is the discipline the brief demands:
*a wrong formulation produces a meaningless number.* So we derive every step.

All entropies are in **nats** (natural log). Ratios and thresholds are
dimensionless, so the nats-vs-bits choice does not affect the constant; we fix
nats for the optimizer and note where the sibling module `verify_ahs.py` uses bits.

Notation follows `shared/notation.md` and `literature/survey.md` §9:
`h(p) = −p ln p − (1−p) ln(1−p)`, `ψ = (3−√5)/2 ≈ 0.3819660`, `φ = (1+√5)/2`,
and note the identity `1/(1−ψ) = φ` and `1/(2(1−ψ)) = φ/2 ≈ 0.8090170`.

---

## 1. The combinatorial-to-information reduction (Gilmer 2022)

**Source:** Gilmer, arXiv:2211.09055, §2; survey §3.1–§3.2.

Let `F ⊆ 2^[n]` be union-closed, `F ≠ {∅}`. Sample `A, B` **i.i.d. uniform on
`F`**. Write `C := A ∪ B`. Because `F` is union-closed, `C ∈ F`. Two facts:

- **(Budget)** `H(C) ≤ log|F| = H(A)`.  *Uses union-closure.*  [Gilmer §2]
- For each `i ∈ [n]`, `p_i := Pr[A_i = 1] = freq_F(i)/|F|` is the marginal /
  abundance of element `i`.

The conjecture's goal is `max_i p_i ≥ 1/2`; the entropy method certifies
`max_i p_i ≥ c` for the best constant `c` the inequalities below can force.

---

## 2. The chain-rule lower bound on H(C) (Gilmer 2022, §2)

**Source:** Gilmer §2; the slack at this step is survey §7.2 / open problem B.6.

Process coordinates left to right. Let `A_{<i} = (A_1,…,A_{i−1})`, similarly
`B_{<i}`, `C_{<i}`. Then

```
H(C) = Σ_i H(C_i | C_{<i}).                                              (2.1)
```

`C_{<i}` is a **deterministic function** of `(A_{<i}, B_{<i})` (coordinatewise
OR). Conditioning on a finer σ-algebra cannot increase entropy:

```
H(C_i | C_{<i}) ≥ H(C_i | A_{<i}, B_{<i}).                              (2.2)
```

> **Direction check.** (2.2) lower-bounds `H(C)`; this is the direction we want
> (we will contradict the budget `H(C) ≤ H(A)`). The inequality is **lossy** by
> exactly `Σ_i I(C_i ; (A_{<i},B_{<i}) | C_{<i}) ≥ 0` — the structural slack
> studied in survey §7.2 and implemented exactly in `verify_ahs.py:delta2`.

Given `(A_{<i}=x, B_{<i}=y)`: because `A ⟂ B` (independent draws) and `A, B`
have the same law, `A_i ~ Bern(a(x))` and `B_i ~ Bern(a(y))` are **independent**,
where `a(·)` is the common conditional-marginal function. Hence `C_i =
A_i ∨ B_i ~ Bern(1 − (1−a(x))(1−a(y)))` and

```
H(C_i | A_{<i}, B_{<i}) = E_{x,y}[ h( 1 − (1−a(x))(1−a(y)) ) ],          (2.3)
```

with `x, y` **independent** copies of the conditional state (same law). Writing
`P := a(X)`, `Q := a(Y)` with `X, Y` i.i.d.,

```
H(C) ≥ Σ_i E_{P,Q iid}[ h(1 − (1−P)(1−Q)) ].                            (2.4)
```

---

## 3. The upper bound on H(A) and the feasibility inequality

**Source:** Gilmer §2 (chain rule for `H(A)`).

```
H(A) = Σ_i H(A_i | A_{<i}) = Σ_i E_X[ h(a(X)) ] = Σ_i E[ h(P) ].         (3.1)
```

Combining the budget `H(C) ≤ H(A)` with (2.4) and (3.1), **per coordinate** (the
coordinates decouple into the same single-letter inequality in the law of `P`):

```
   E_{P,Q iid ~ μ}[ h(1 − (1−P)(1−Q)) ]   ≤   E_{μ}[ h(P) ].             (IV)
```

Here `μ` is the law on `[0,1]` of the conditional marginal `P` of a coordinate.
**(IV) is a necessary condition** that any union-closed family must satisfy, in
the dimension-free single-letter limit.

> **Direction check.** (IV) has the *union entropy* on the left and the *single-
> coordinate entropy* on the right. Verified numerically: when every atom of `μ`
> lies below ψ, the LHS strictly exceeds the RHS, so (IV) is violated — see
> `joint_opt.py::verify_floor_argument` / `verify_optimization.py`.

---

## 4. The base optimization and why its value is exactly ψ

The certified constant is the **smallest mean marginal** consistent with (IV):

```
   c_iid  :=  inf { E_μ[P]  :  μ a probability measure on [0,1] satisfying (IV) }.   (OPT-iid)
```

**Claim.** `c_iid = ψ = (3 − √5)/2`.

*Proof of `c_iid ≥ ψ` (this is the lower bound that matters for the theorem).*
Use the **sharp Sawin per-coordinate inequality** (survey §3.2, §7.1; AHS Lemma):

```
   h(1 − (1−p)(1−q))  ≥  (1/(2(1−ψ))) · [ (1−q) h(p) + (1−p) h(q) ]      (S)
```

for all `p, q ∈ [0,1]`, with **equality at `p = q = ψ`**. (Verified: at
`p=q=ψ` both sides equal `0.665018…`; the constant `1/(2(1−ψ)) = φ/2` is forced
by that single equality point — survey §7.1.) Taking `E` over i.i.d. `P, Q`
and using independence `E[(1−Q)h(P)] = (1−E[Q]) E[h(P)]`:

```
   E[h(1−(1−P)(1−Q))]  ≥  (1/(1−ψ)) (1 − E[P]) E[h(P)].                  (S')
```

Combine (S') with (IV): if `E[h(P)] > 0`,

```
   (1/(1−ψ)) (1 − E[P]) E[h(P)]  ≤  E[h(P)]  ⟹  1 − E[P] ≤ 1 − ψ  ⟹  E[P] ≥ ψ.
```

(If `E[h(P)] = 0` then `μ` is supported on `{0,1}`; the family is degenerate and
contributes nothing.) ∎

*Proof of `c_iid ≤ ψ` (tightness).* Take `μ = δ_ψ` (point mass at ψ). Then both
sides of (IV) reduce, via the **crossover identity**, to equality: `h(1−(1−ψ)^2)
= h(2ψ−ψ^2) = h(1−ψ) = h(ψ)` because `2ψ − ψ^2 = 1 − ψ ⟺ ψ^2 − 3ψ + 1 = 0`,
which is the defining equation of ψ. So `μ = δ_ψ` is feasible with `E[P] = ψ`. ∎

> **Crossover identity, verified.** `h(2p−p^2) = h(p) ⟺ 2p−p^2 = 1−p ⟺
> p^2−3p+1 = 0 ⟺ p = ψ`. For `p < ψ` the union coordinate carries *more* entropy
> than a single coordinate, so (IV) is violated unless mass sits at/above ψ.

**This is the load-bearing fact: the i.i.d. single-letter program has optimum
exactly ψ.** It is the sanity floor required by the brief, and `joint_opt.py`
reproduces it both by the closed form and by direct numerical optimization
(min over a fine grid ≈ 0.38203, → ψ as the grid refines).

---

## 5. The two relaxations the brief asks for

### 5.1 Reweighting the base measure (Cambie-style)

**Source:** Cambie, arXiv:2306.12351 §3; survey §7.3; open problem B.7.

Cambie replaces uniform-on-`F` by a weighted ("Maxwell–Boltzmann") measure.
In the **dimension-free single-letter** picture this is *exactly* the freedom to
choose the law `μ` of `P` (different weightings of `F` induce different marginal
laws). **(OPT-iid) already optimizes over all `μ`.** Therefore:

> **Consequence (verified).** Reweighting *alone*, inside the i.i.d. coupling,
> cannot beat ψ in the dimension-free limit, because (OPT-iid) is already the
> infimum over all `μ` and equals ψ. Cambie's finite gain comes from coupling
> the reweighting with a non-i.i.d. structure **and** from finite-`n` effects.
> We record this as a genuine (negative) finding, not an omission.

### 5.2 Conditional-i.i.d. coupling with auxiliary `U`, `|U| = k`

**Source:** Liu, arXiv:2306.08824; Yu, arXiv:2212.00658; survey §7.7; B.5.

Introduce an auxiliary variable `U ∈ {1,…,k}` with weights `w_j`. The coupling:
`A, B` are i.i.d. **conditioned on `U`**; given `U=j`, the coordinate marginal is
`p_j`. The marginal coupling of `(A_i,B_i)` is the mixture
`Σ_j w_j Bern(p_j)^{⊗2}`.

The gain over §4 must come from a **tighter** lower bound on `H(C)` (a *larger*
LHS in a feasibility inequality forces `E[P]` higher), specifically by recovering
part of the slack `Σ_i I(C_i;(A_{<i},B_{<i})|C_{<i})` in (2.2) using the shared
`U`. The relevant entropy identities are

```
H(C)  = H(C|U) + I(C;U),     H(A) = H(A|U) + I(A;U).
```

> **Honest status (read §6).** The *correct* single-letter functional for the
> conditional-`U` relaxation requires Liu's precise bookkeeping of how `I(C;U)`
> and `I(A;U)` enter. We were **unable to retrieve** arXiv:2306.08824 /
> arXiv:2212.00658 in this environment (network blocked; HTTP 403 on
> `arxiv.org`, `ar5iv`, mirrors, and direct download). Two from-first-principles
> reconstructions we tried either (a) collapse to the marginal (giving no gain
> beyond ψ), or (b) admit a degenerate optimizer with atoms at `p∈{0,1}` that
> drives the bound spuriously to 0 — a sign the naive "refund" double-counts.
> We therefore **do not** assert a reconstructed Liu functional as correct, and
> we **do not** claim Liu's 0.38271. `joint_opt.py` implements the auxiliary-`U`
> machinery and the *valid* relaxations we can certify, and documents the
> conditional-`U` functional as `[unverified — needs source / human review]`.

---

## 6. What is certified, what is not

| Quantity | Value | Status |
|---|---|---|
| Base i.i.d. single-letter optimum `c_iid` | exactly `ψ = (3−√5)/2` | **derived + numerically verified + interval-certified** (see `certificate_0.38197.md`) |
| Sharp Sawin per-coordinate inequality (S) | constant `1/(2(1−ψ))` | verified pointwise; tight at `p=q=ψ`; cross-checked by `verify_ahs.py:lemma2_G` |
| Reweighting alone beats ψ? | **No** (in the dim-free limit) | derived + verified negative result |
| Conditional-`U` functional (Liu) | claims 0.38271 | **NOT reproduced** — source inaccessible; reconstructions failed (see §5.2). Documented honestly. |

**Sanity floor:** met — the method reproduces `ψ ≈ 0.38197` exactly. **Liu
checkpoint (0.38271):** *not* reproduced; the discrepancy is documented in
`results.md` with the specific obstruction (inaccessible source + degenerate
reconstruction), per the brief's honest-negative-result rule.

---

## 7. The optimization, stated compactly (for `joint_opt.py`)

Decision variables: a discrete law `μ = {(p_a, w_a)}` on a grid of `[0,1]`, and
(for the auxiliary version) a coupling `T` / auxiliary weights `w_j, p_j`.

**Base program (certified):**
```
minimize    Σ_a w_a p_a
subject to  Σ_{a,b} w_a w_b · h(1 − (1−p_a)(1−p_b))  ≤  Σ_a w_a h(p_a)      (IV)
            Σ_a w_a = 1,   w_a ≥ 0,   p_a ∈ [0,1].
```
Optimum = ψ. This is the program we certify from the correct (lower-bound) side
in `certificate_0.38197.md`.

**Caveat for the auxiliary/coupling extensions:** a *larger* coupling class makes
(IV) a *weaker* necessary condition, so naively minimizing `E[P]` over a larger
class **lowers** the certified threshold (we observed `≈0.359 < ψ` with a free
off-diagonal coupling). Improvements beyond ψ therefore require *adding* valid
constraints (the recovered mutual information), **not** enlarging the feasible
set. This is the central subtlety and the reason §5.2 is left unverified rather
than guessed.
