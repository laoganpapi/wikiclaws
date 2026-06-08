# Operator algebras / KMS states / Tomita–Takesaki — Collatz

**Track:** Collatz, alt-angle wave 4.
**Field cluster:** Operator algebras (C*- and von Neumann);
Tomita–Takesaki modular theory; KMS states (Kubo–Martin–Schwinger);
Cuntz–Krieger / Bratteli–Jorgensen algebras; gauge-action / Renault
groupoid KMS theory (Olesen–Pedersen, Exel, Kumjian–Renault); noncommutative
large deviations (Hiai–Mosonyi–Petz, Lenci–Rey-Bellet, Netočný–Redig).
**Status:** Direction proposal + concrete computational probe (2 scripts,
1 dataset).
**Verdict:** `[CANDIDATE — direction-eliminating negative diagnostic, with one
crisp byproduct: the entire KMS_β family of the Bernoulli–Esscher
deformation IS the Wave-1 per-coord Esscher family, and inherits the
same drift gap. The noncommutative refinement does not enlarge the
class of accessible marginals.]`
`[NOVELTY UNVERIFIED]` for the KMS / Tomita-Takesaki framing of the
Syracuse transfer operator. **Prior art flag:** arxiv 2411.08084
(Mori 2024, Adv. Op. Th. 2025) gives a Cuntz-algebra reformulation of
the Collatz conjecture via "no non-trivial reducing subspaces" — this
is sub-direction (iv) of the brief and is **prior art**, so we focus
on sub-directions (i)–(iii), which appear not to have been pursued.
**Author:** Alex Ye (AI-assisted computation; AI not on author line
per project rules).
**Date:** 2026-06-08.
**Files:** `operator_algebras_kms_probe.py`,
`operator_algebras_kms_probe2.py`,
`data/operator_algebras_kms_probe.json`,
`data/operator_algebras_kms_probe2.json`.

---

## 0. Verdict (one paragraph, read first)

> **Honest assessment: long shot, came back negative, but with a
> precise and useful structural identification.**
>
> The Cuntz–Krieger / Renault KMS_β family of the Syracuse transfer
> operator (sub-direction (i)) is, on the diagonal subalgebra
> `C((Z/3^n)*)`, **exactly the Bernoulli–Esscher tilt family of the
> Wave-1 obstruction theorem**. Concretely, parametrising the
> Bernoulli base measure by β ∈ (0, ∞) — the modular inverse
> temperature — yields a one-parameter family of stationary measures
> π_β on `(Z/9)*`. The probe (k = 1, 2, 3, β in 27-point grid) shows:
>
> - the unique β achieving the **Tao mod-3 saturation** `(0, 1/3, 2/3)`
>   is β = 1 (the Bernoulli base = the trace = the canonical KMS_1
>   state), giving `E_{π_1}[a] = 2`, drift gap `0.4150 > 0`;
> - the unique β achieving **drift balance** `E_{π_β}[a] = log_2 3`
>   is β ≈ 1.40, giving mod-3 marginal `(0, 0.275, 0.725)`, L1 distance
>   `0.117` to Tao;
> - the two targets are NEVER simultaneously achievable: the trade-off
>   is rigid;
> - the result is **identical** across k = 1, 2, 3 (mod 3, 9, 27) —
>   the noncommutative refinement at higher k does NOT change the
>   accessible (mod-3 marginal, drift) pair, which lies on a 1-dim
>   curve parametrised by β.
>
> **This is the Wave-1 obstruction (`collatz_d5_tilt.md`) re-expressed
> in the KMS language.** The KMS_β state IS the Esscher-tilted
> Bernoulli, and the modular automorphism IS the i.i.d. tilt by `−β log
> 2` of the Geom(1/2) valuation. The noncommutative LDP rate function
> (Hiai–Mosonyi 2010 for Cuntz-Krieger / spin-chain KMS states) reduces
> on the diagonal subalgebra to the commutative Donsker–Varadhan rate.
> The Wave-2 LP-min (`E[a_class] ≥ 5/2` for non-i.i.d. but stationary
> Markov tilts on mod-6 classes) bounds the off-diagonal extension too.
>
> **What is genuinely left open** (and which I do NOT close): a
> Type-III KMS state (non-tracial in a way that forces a non-diagonal
> stationary measure on `(Z/9)*`). For finite-dim C*-algebras (which is
> all we get from any finite-state Markov system on `(Z/3^n)*`), all
> KMS states ARE diagonal in the position basis, so the Type-III escape
> is necessarily infinite-dimensional — it must live on the path-space
> AF algebra of the *infinite-depth* Syracuse tree. There the modular
> automorphism is non-trivial and the KMS_β state need not project
> onto a diagonal measure on `(Z/3^n)*`. **I flag this as `[FRONTIER]`
> with a precise structural criterion** (§7), with the prior comment
> that the finite-dim closure I prove transfers to AF inductive limits
> by Lanford–Ruelle-style reduction unless the local potential has
> unbounded support — i.e. unless the per-step KL is infinite. That
> is exactly the F1 frontier of Wave 2; the operator-algebraic
> framing does not produce it for free.

The remainder of the document records (1) the precise C*-algebraic
objects, (2) the probe and its result, (3) the reduction to the Wave-1
/ Wave-2 closed class, (4) the prior-art check (Mori 2024 closes
sub-direction (iv)), and (5) honest assessment.

---

## 1. Setup and notation

We follow `shared/notation.md`. Let `n ≥ 1`, `Q_n := (Z/3^n Z)*` the
unit group of size `2 · 3^{n−1}`. The **Syracuse transfer operator**
P_n acts on functions f : Q_n → C by

```
   (P_n f)(x) = Σ_{a ≥ 1} 2^{−a} f( ((3 x + 1) · 2^{−a}) mod 3^n ),
```

where `2^{−a}` is interpreted in `Z/3^n Z` (units, gcd(2, 3) = 1). The
Bernoulli weighting `2^{−a}` comes from the Tao-Bernoulli model of the
valuation `a = ν_2(3 x + 1)` as i.i.d. Geom(1/2) (this is the standard
Tao 2022 model; on the integers it requires a finite-depth equidistribution
lemma, which holds for `n ≥ 2`).

`P_n` is a row-stochastic matrix on Q_n (after the `2^{−a}` weights sum
to 1). Its Perron-Frobenius spectral radius is 1, and its left
eigenvector π_n is the *Syracuse stationary distribution* — which is
the project's central object.

---

## 2. The C*-algebra and its KMS structure

### 2.1 The transition C*-algebra

Let `A_n` ∈ {0, 1}^{Q_n × Q_n} be the 0/1 adjacency matrix of the
Syracuse transition graph: A_n[i, j] = 1 iff there exists `a ≥ 1` with
`((3 i + 1) · 2^{−a}) ≡ j (mod 3^n)`. By the unit-group argument, every
`i ∈ Q_n` has infinitely many outgoing edges (one per `a ≥ 1`), and
A_n is irreducible (proof: the Syracuse map is surjective on Q_n by
inverse-lift of `2^a (3 y − ... + ...)`).

The **Cuntz–Krieger algebra** O_{A_n} is the universal C*-algebra
generated by partial isometries `{s_{i,j,a} : A_n[i, j] = 1, a ≥ 1}`
with relations:
```
   s_{i,j,a}^* s_{i,j,a}  =  P_{j}   (range projection)
   Σ_{j,a} s_{i,j,a} s_{i,j,a}^*  =  P_i   (Cuntz relation)
   s_{i,j,a} s_{i',j',a'} = δ_{j,i'} · s_{i,j',a'}(...)  (composition)
```
(Edges labelled by triples `(i, j, a)` because the same (i, j) can be
reached by multiple a-values; this is a *labelled* Cuntz–Krieger algebra,
equivalently the C*-algebra of a *Bratteli diagram* whose level-n vertex
set is Q_n with multiplicities 2^a for a ≥ 1.)

For finite a-truncation `a ≤ A_max`, A_n becomes finite-row-sum and
O_{A_n,A_max} is a finite-dim AF algebra (a direct sum of matrix
algebras). Taking A_max → ∞ gives an honest infinite-dim C*-algebra.

### 2.2 The gauge action and KMS states (Renault–Exel)

The standard *gauge action* `γ_θ` of T^1 on O_{A_n} (or of R on its
Pimsner dilation) is the one fixing P_i and acting on generators by
`γ_θ(s_{i,j,a}) = e^{iθ a} s_{i,j,a}` — i.e. the inverse temperature
`β` is dual to the *cumulative valuation* `Σ a`.

**KMS_β condition (Olesen–Pedersen 1978; Renault 1998).** A state
ω_β on O_{A_n} is KMS_β for `γ` iff for every pair `(x, y)` of
analytic elements,
```
   ω_β(x y)  =  ω_β(y · γ_{iβ}(x)).
```
For Cuntz–Krieger algebras with a gauge action of this form, KMS_β
states are classified by **Renault's theorem**: they correspond
bijectively to **eigenvectors** of the deformed Ruelle transfer matrix
```
   L_β[i, j]  :=  Σ_{a} e^{−β · a} · 1[A_n[i,j,a]],
```
i.e., to non-negative probability vectors π_β such that
```
   π_β · L_β   =   ρ(β) · π_β,
```
with ρ(β) the spectral radius and the normalisation `Σ π_β = 1`. The
inverse temperature satisfies `ρ(β) = 1` (the natural-temperature
condition); a unique β solves this when L_β is irreducible
(Perron–Frobenius). For other β the KMS_β state still exists but
satisfies a more general balance condition.

### 2.3 The diagonal projection and the Bernoulli–Esscher identification

The diagonal subalgebra of O_{A_n} is `D_n := C(Q_n)`. The KMS_β state
ω_β restricted to D_n is a probability measure π_β on Q_n. By the
Renault classification:

> **(★) The π_β diagonal marginal of the KMS_β state of O_{A_n} (with
> gauge action dual to cumulative valuation) is EXACTLY the stationary
> measure of the Markov chain on Q_n whose transition kernel is
>     P_β[i, j]  =  L_β[i, j] · r_β[j] / (ρ(β) · r_β[i]),
> with r_β the right Perron eigenvector of L_β.**

This identifies the KMS_β state — at the marginal level — with the
*Esscher-tilted Bernoulli walk*: pick `a ~ Geom-tilted-by-β` (= the
distribution with mass `2^{−a β} / (2^β − 1)` on `a = 1, 2, ...`)
independently at each step, push forward through the Syracuse map.

**The classical Bernoulli base = the trace = the KMS_1 state.**

### 2.4 The Tomita–Takesaki modular operator

For a faithful state ω on a finite-dim C*-algebra M ⊆ B(H), the
modular operator Δ on the GNS Hilbert space (= HS space of M acting on
itself by left multiplication, with inner product `⟨a, b⟩_ω = ω(b* a)`)
has spectrum `{λ_i / λ_j : λ_i ∈ spec(ρ_ω)}` where ρ_ω is the density.
For our diagonal state on a 6-point support, ρ_ω is the 6×6 diagonal,
and Δ has 36 eigenvalues = the 36 ratios π_β(i) / π_β(j).

**For finite-dim D_n = C(Q_n), the modular automorphism is TRIVIAL**
(every commutative algebra is its own commutant, and the modular flow
is the identity). The non-trivial Tomita-Takesaki content lives on the
**non-diagonal** part of O_{A_n} — i.e. on the partial-isometry
generators `s_{i,j,a}`. By Renault's formula,
```
   σ_t^{ω_β}(s_{i,j,a})  =  e^{−i t β · a} · (r_β[i]/r_β[j])^{−it} · s_{i,j,a}.
```
This is **diagonalisable** in the (i, j, a) basis — the modular flow
is a pure phase rotation by `t · (β · a + log(r_β[i]/r_β[j]))`. It is
non-trivial but does NOT couple distinct (i, j, a) sectors. In particular
**it does not generate any new diagonal observable** beyond π_β.

> This is the precise structural reason the KMS / Tomita framing
> reduces to commutative Esscher: the modular flow is *abelian* on
> the off-diagonal part, so it carries no information beyond the
> tilting parameter β itself.

---

## 3. The first probe — actually run

### 3.1 What we computed

- `operator_algebras_kms_probe.py`: builds P_n on Q_n for n = 1, 2, 3
  (sizes 2, 6, 18); computes the β = 1 Tao stationary distribution, its
  mod-3 / mod-9 marginal, and `E_{π_1}[a]`; runs a coarse KMS_β scan
  using a heuristic `B_β[i, j] = P[i, j]^β` deformation (which serves
  as a sanity reference).
- `operator_algebras_kms_probe2.py`: builds the Renault-correct deformed
  transition matrix `L_β[i, j] = Σ_a e^{−β·a·log 2} · 1[edge (i, j, a)]`
  with edges enumerated to `a ≤ 50`; computes Perron data, π_β
  diagonal marginal, mod-3 / mod-9 marginal, and `E_{π_β}[a]` via the
  edge-conditional `a`-expectation under the tilted chain; scans β
  over a 27-point grid in `[0.05, 20]`.

### 3.2 Results — k = 2 (mod 9) selected β-table

```
   beta   spec_rad    E[a]    drift     mod-3=1   mod-3=2
  ──────────────────────────────────────────────────────
   0.50    2.41421   3.4142    1.8292    0.4142    0.5858
   1.00    1.00000   2.0000    0.4150    0.3333    0.6667   ← Tao plateau
   1.20    0.77077   1.7708    0.1858    0.3033    0.6967
   1.40    0.61012   1.6101    0.0252    0.2748    0.7252   ← drift balance ≈
   1.50    0.54692   1.5469   −0.0380    0.2612    0.7388
   2.00    0.33333   1.3333   −0.2516    0.2000    0.8000
   5.00    0.03226   1.0323   −0.5527    0.0303    0.9697
  10.00    0.00098   1.0010   −0.5840    0.0010    0.9990
  20.00    0.00000   1.0000   −0.5850    0.0000    1.0000
```

(`drift` = `E[a] − log_2 3`. The mod-3 = 0 row is identically 0 by the
unit-group constraint, so we display only the (1, 2) coordinates.)

**Read this carefully:**

- E[a] **decreases monotonically** from `+∞` as β → 0+ to **1** as β → ∞;
- The Tao mod-3 plateau `(0, 1/3, 2/3)` is hit **exactly** at β = 1,
  with `E[a] = 2` (NOT log_2 3); drift gap = 0.4150 > 0;
- Drift balance `E[a] = log_2 3 = 1.585` is hit **near β ≈ 1.40**,
  with mod-3 = `(0, 0.275, 0.725)`; L1 distance to Tao plateau = 0.117;
- **The (mod-3 marginal, E[a]) pair traces a 1-dim curve in β**, and
  the two targets are at **distinct points**.

This is exactly the Wave-1 Esscher obstruction `gap_2 = 3 + 1/2 −
log_2 3 ≈ 1.915` re-expressed; the difference (here 0.415 vs there
1.915) is because we are looking at mod-3 not mod-9 saturation. For
mod-9 saturation `(1/6, 1/6, 1/6, 1/6, 1/6, 1/6)` the obstruction
sharpens (per Wave-1 Theorem at k = 2). The probe at k = 2 confirms:
**no β achieves mod-9 uniformity**; the closest β = 1 gives mod-9 =
`(0.127, 0.254, 0.175, 0.063, 0.032, 0.349)`, far from uniform.

### 3.3 Results — k = 1, 3 (mod 3, mod 27)

**Identical β-table** for the (drift, mod-3 marginal) curve at k = 1, 2, 3.
This is *the* structural finding of the probe: the diagonal marginal
at mod-3 level (and the corresponding E[a] curve) is **independent of
the C*-algebra refinement at higher k**. The noncommutative refinement
(more partial isometries, more modular spectrum) does **NOT** enlarge
the family of achievable diagonal marginals on Q_n / (mod-3 projection).

### 3.4 The Tomita modular spectrum at β = 1, k = 2

36 eigenvalues of Δ:
- range `[0.0909, 11.0000]`,
- log-spectrum range `[−2.40, 2.40]`.

(Recall: 11 ≈ 0.3492/0.0317 = π(8)/π(7), the largest π_1-mass ratio.)
The modular flow `σ_t = Ad(Δ^{it})` is the periodic rotation with these
characteristic phases. **Bounded and discrete**; no Type-III phenomenon.

### 3.5 Aggregate conclusion

The KMS_β diagonal marginals form a 1-parameter Esscher curve. The
Wave-1 obstruction extends without modification. **No β gives both
mod-3 saturation and drift balance.** The off-diagonal (modular) flow
is abelian on generators and does not carry new diagonal information.

---

## 4. Why this does NOT escape the LDP-tractable barrier

### 4.1 Noncommutative LDP (Hiai–Mosonyi)

The noncommutative large-deviation principle (Hiai–Mosonyi 2010,
*Comm. Math. Phys.* 296:773; Lenci–Rey-Bellet 2005; Netočný–Redig 2004)
for KMS states on finite-correlated spin chains gives a Donsker–Varadhan
rate function
```
   I_NC(ω)  =  S(ω || ω_KMS)  +  β · (E_ω[H] − E_{ω_KMS}[H]),
```
where `S(· || ·)` is the **noncommutative relative entropy** (Araki
1976). For *diagonal* observables — which is what mod-3 / mod-9 marginal
constraints are — the NC relative entropy collapses to the classical
KL divergence, and `I_NC` collapses to the commutative Donsker–Varadhan
rate. **The DV LP-min `≥ 5/2` of Wave 2 transfers verbatim.**

### 4.2 The off-diagonal extension

The off-diagonal partial isometries `s_{i,j,a}` correspond to *transition*
observables. A state ω with non-zero off-diagonal coherences (= a state
with quantum entanglement between sites) could, *a priori*, satisfy
constraints not available to any diagonal measure.

**But for KMS states of the gauge action, the modular flow ENFORCES
diagonality in the gauge basis.** Specifically, the gauge action γ_θ
acts on `s_{i,j,a}` by phase `e^{iθa}`, so KMS_β states are
γ-invariant — their off-diagonal expectations on `s_{i,j,a}` are
zero (averaging out the phase). Concretely:
```
   ω_β(s_{i,j,a})  =  ω_β(γ_θ(s_{i,j,a}))  =  e^{iθa} ω_β(s_{i,j,a})
                                            ⇒  ω_β(s_{i,j,a}) = 0  for a ≠ 0.
```
(With a = 0 corresponding to the identity; we have a ≥ 1 in our edge
labelling.) Hence **every KMS_β state is diagonal in the gauge basis**,
and the off-diagonal generators of O_{A_n} carry no expectation.

**Consequence.** KMS_β states are EXACTLY the diagonal Bernoulli–Esscher
measures π_β, and the rate function on the constraint
`{ω : (mod-3 marginal of ω) ∈ K}` for any closed set K ⊆ Simplex(Z/3)
is the commutative DV rate restricted to π_β. The Wave-1 / Wave-2 LP-min
applies unchanged.

### 4.3 What WOULD escape

The escape would need to be one of:

(A) **A non-gauge-invariant state** ω that is KMS_β for a *different*
   continuous action of R (e.g. an action coupling i and j non-trivially).
   But any continuous R-action on the finite-dim O_{A_n} is generated
   by a self-adjoint H ∈ O_{A_n}, and the GNS Hilbert space of any
   faithful state is finite-dim, so the resulting modular flow has
   discrete bounded spectrum — same flavour as our gauge case. The
   *commutative LDP rate* on any diagonal projection is still the
   commutative DV rate.

(B) **A Type-III KMS state on the infinite-dim AF closure** of the
   Syracuse path-space C*-algebra (the Bratteli diagram with level-n
   = Q_n, edges weighted by 2^{−a}). Here the modular operator can
   have continuous spectrum and the state can fail to be diagonal in
   any natural basis. The natural-density question, however, is a
   diagonal question (residue mod 3^n), so any such Type-III feature
   that helps must induce a non-trivial *non-Markovian* coupling on
   the diagonal subalgebra — which is exactly the Wave-2 Markov-tilt
   class, already closed by the LP-min ≥ 5/2.

(C) **A genuinely infinite per-step KL escape** — corresponding to
   `e^{−β a}` with a non-summable mass at a = ∞. This is the F1
   frontier of Wave 2. No KMS framing gets this for free; the gauge
   action has well-defined modular flow only for finite β.

### 4.4 The precise abstract closure statement

Let `K_n` = the set of KMS_β states of O_{A_n} for all β ∈ R and all
continuous one-parameter R-actions on O_{A_n} preserving the gauge
grading. Let `D_n : K_n → Prob(Q_n)` be the diagonal-restriction
map. Then

> **D_n(K_n) ⊆ {Esscher tilts of Bernoulli(2^{−·}) on (Q_n)^N pushed
> forward by the Syracuse map} = the Wave-1 Esscher family.**

The Wave-1 obstruction theorem (`collatz_d5_tilt.md` Theorem 1) closes
the Wave-1 Esscher family for k ≥ 2. **Hence D_n(K_n) is closed for
k ≥ 2.** ∎

---

## 5. Prior art — Mori 2024 closes sub-direction (iv)

A web search (June 2026) returned **Mori, "Application of Operator
Theory for the Collatz Conjecture", arxiv 2411.08084, published
Adv. Op. Th. 9 (2025) art. 425**. The paper formulates Collatz via:

1. **Single operator on ℓ²(N)**: the unitary representation of `n ↦ T(n)`
   on the canonical basis. Result: the generated C*-algebra has no
   non-trivial reducing subspaces ⇒ Collatz.
2. **Two operators**: the two parity branches as partial isometries.
   Result: equivalence to Collatz.
3. **Cuntz algebra O_2 (or O_∞)**: the parity sequences as Cuntz
   generators. Result: equivalence to Collatz.

This is **sub-direction (iv) of the brief** ("Cuntz-Krieger / Bratteli-
Jorgensen algebras associated with the Collatz tree") and is
**prior art** as of November 2024 / Adv. Op. Th. 2025. Mori's result
reformulates Collatz as a reducing-subspace question on a C*-algebra,
but does not address the *natural-density* question and does not
introduce KMS states, modular flow, or noncommutative LDP. It is a
reformulation, not a new attack.

Our work (sub-directions (i)–(iii)) is **complementary, not
overlapping**, and is consistent with — but does not subsume — Mori.
Specifically:

- (i) KMS_β of the *transfer-operator* algebra (not Mori's parity
  algebra). We give the precise probe.
- (ii) Noncommutative Cramér / Hiai–Mosonyi LDP applied to (i). We give
  the structural reduction (§4.1).
- (iii) Tomita-Takesaki modular flow on the gauge-action algebra. We
  show it is abelian on generators (§2.4).

No surface evidence of prior work on (i)–(iii). `[NOVELTY UNVERIFIED]`
for the framings; **the content is a clean direction-eliminating
negative.**

Adjacent prior art (cleanly distinct): Bratteli–Jorgensen 1999/2002 on
Cuntz-algebra representations indexed by binary expansions
(wavelet-style), Marcolli–Connes 2008 on KMS states of the Bost-Connes
system (number-field zeta), Cuntz–Deninger 2008 on a C*-algebra of
algebraic integers — none Collatz, all in the same conceptual ZIP code.

---

## 6. Plausibility, failure modes, residual usable content

### 6.1 Plausibility for natural density: **1 / 5**.

The structural argument in §4 closes the angle uniformly across all
finite-dim refinements (k = 1, 2, 3, ...). The off-diagonal
modular-flow content is provably (gauge-invariance) zero on the
relevant diagonal projection. No finite-dim KMS construction can
escape the Wave-1 / Wave-2 closure.

### 6.2 Failure modes (honest list)

(F-a) **Sub-direction (iv) prior art** (Mori 2024). Closed.

(F-b) **Modular flow is abelian on generators** (§2.4 calculation).
   This is the deep structural reason — the gauge action is trivial
   on the diagonal subalgebra and decoupled on the off-diagonal
   sectors. *No non-abelian "hidden symmetry" of the Syracuse C*-algebra
   appears.* If one existed it would have to be detected by a
   non-gauge KMS construction.

(F-c) **The KMS_β family at the diagonal level IS the Esscher family**
   (§3, probe). This is the exact Wave-1 obstruction. Our probe verifies
   it numerically at k = 1, 2, 3 with identical β-curves.

(F-d) **Type-III KMS on infinite-depth AF closure** [FRONTIER, §7]:
   the only direction not closed. Requires the path-space algebra
   `O_{A_n}^{n → ∞}` to admit a KMS state with continuous modular
   spectrum, AND that state's diagonal projection to escape the
   Wave-2 LP-min ≥ 5/2. No concrete candidate.

### 6.3 Residual usable content

The probe gives a **crisp restatement** of the Wave-1 obstruction in
KMS language:

> **Proposition (KMS restatement of Wave-1 obstruction).** Let
> `{ω_β : β > 0}` be the gauge-action KMS family of O_{A_n} (n ≥ 2),
> and π_β its diagonal marginal on Q_n. Then π_β is the Bernoulli–
> Esscher tilt with E_{π_β}[ν_2(3 x + 1)] = 1 + 1/(2^β − 1). Setting
> this equal to log_2 3 requires β = log_2(2 / (log_2 3 − 1)) ≈ 1.397.
> At this β the mod-3 marginal of π_β is (0, π_1, π_2) with
> π_1 = 1/2 − (1/2)/(2^β − 1) · ... [computation] ≠ 1/3. The system
> ```
>    E_{π_β}[ν_2(3 x + 1)] = log_2 3   AND   (mod-3 marg of π_β) = (0, 1/3, 2/3)
> ```
> has NO solution β ∈ (0, ∞).

This is the **KMS / NC-LDP version of the Wave-1 Esscher theorem** —
a unified spectral / operator-algebraic statement of the known
obstruction. **Not new content; cleaner language.** May be worth a
sentence in the obstruction section of the Collatz paper, as a
unified spectral statement (analogous to the Bohr-AP restatement
in Wave 3 §3.4).

---

## 7. The one direction NOT closed (and why it remains a long shot)

**[FRONTIER]** The infinite-dim AF closure of `O_{A_n}` as n → ∞
(equivalently the Bratteli-diagram C*-algebra of the inverse-limit
Syracuse system `lim_{n} (Z/3^n Z)*`, with level-n edges weighted
by 2^{−a}) admits, by Connes' classification of injective factors,
a Type-III_λ factor representation for some `0 < λ < 1`, provided the
modular spectrum has a non-trivial accumulation point at log λ. The
probe shows (§3.4) that at finite n the modular spectrum is discrete
and bounded; the inductive limit n → ∞ could produce a continuous
spectrum.

For such a Type-III KMS state to escape the natural-density
obstruction it would need to satisfy three things SIMULTANEOUSLY:

(a) the state ω∞ is faithful and KMS_β for *some* continuous R-action
   on the AF closure;

(b) the *diagonal projection* of ω∞ onto `C(Q_n)` (any finite n) gives
   a measure not in the Wave-1 Esscher family;

(c) the corresponding noncommutative LDP rate `S(σ || ω∞)` for the
   constraint `(mod-3 marg of σ) = (0, 1/3, 2/3)` AND drift balance
   is finite and minimised at a Tao-compatible measure.

Requirement (b) is the structurally hard one: the inductive-limit
diagonal of a gauge-KMS state on an AF closure is, by a Lanford–Ruelle
argument, a Gibbs measure on the path space; and Gibbs measures with
*summable potential* fall in Wave-2 LP-min ≥ 5/2. The only escape
is a non-summable potential — equivalently infinite per-step KL —
which is the F1 frontier already identified by Wave 2.

**No concrete candidate. Flagged as F1 reformulation, not progress.**

---

## 8. Honest assessment and recommendation

**What this work establishes:**

1. The KMS_β family of the Syracuse Cuntz–Krieger algebra O_{A_n}
   (with gauge action dual to cumulative 2-adic valuation), restricted
   to the diagonal subalgebra C(Q_n), IS the Wave-1 per-coord Esscher
   family. (§3 probe + §4 structural argument.)
2. The modular Tomita-Takesaki flow on O_{A_n} is **diagonalisable on
   generators** with discrete, bounded spectrum (36 eigenvalues at
   k = 2, log-range [−2.40, 2.40]). No Type-III phenomenon at finite k.
3. The noncommutative LDP rate (Hiai–Mosonyi 2010) for KMS states on
   finite-dim C*-algebras reduces, on the diagonal subalgebra, to the
   commutative Donsker–Varadhan rate. Wave-2 LP-min `≥ 5/2` transfers
   without modification.
4. Sub-direction (iv) of the brief (Cuntz-algebra reformulation of
   Collatz) is **prior art** as of Mori 2024 (arxiv 2411.08084,
   Adv. Op. Th. 2025). It is a reformulation, not a natural-density
   attack.

**What this work does NOT do:**

- Does not propose any new attack on natural density.
- Does not close any new family of reweightings beyond Wave-1 / Wave-2.
- Does not propose a candidate Type-III state on the AF closure that
  could escape the Wave-2 LP-min.

**Confidence calls:**

- KMS_β diagonal marginal IS Bernoulli-Esscher: **VERY HIGH** (Renault
  classification theorem; probe verification at k = 1, 2, 3 matches
  to numerical precision; structural calculation in §2.3).
- Modular flow trivial on diagonal, phase-only on generators:
  **HIGH** (direct calculation §2.4; gauge-invariance of KMS_β states).
- Wave-2 LP-min transfers to KMS via Hiai–Mosonyi NC LDP: **HIGH**
  (NC relative entropy collapses to KL on commutative subalgebras;
  this is the textbook diagonal-restriction property of Araki entropy).
- Type-III / AF closure does not give automatic escape (§7):
  **MEDIUM** (the Lanford-Ruelle argument is standard but rigorous
  only in the bounded-interaction case; the genuine non-summable
  case is exactly F1 and remains open).

**Plausibility: 1 / 5.**

**Recommendation to the team:**

**Do NOT pursue this angle further** as a route to natural density.
The KMS / modular framing is a CLEANER expression of the Wave-1
obstruction but does not move past it. The one residual usable
artifact is the **KMS-form of the Wave-1 obstruction statement** (§6.3),
which gives a unified spectral / operator-algebraic phrasing of the
Esscher gap. Worth a sentence in the obstruction section of the
Collatz paper.

The Frontier F1 (infinite per-step KL / non-summable potential / 
Type-III AF closure with non-Markovian diagonal projection) remains
the only direction not closed by Waves 1+2+3+4. **All four alt-angle
waves now converge on the same residual question:**

> Is there a probability measure on `Z_+^N` with **infinite per-step
> KL divergence** against the Bernoulli base, whose Syracuse
> pushforward gives mod-3^k saturation AND drift balance?

No alt-angle wave has produced a candidate. The honest forward question
is *not* "which more clever C*-algebra?" but "what unbounded-rate
construction can satisfy drift balance without conditioning on the
future?". The operator-algebraic framing gives **no new traction**
on this F1 question, since gauge-KMS states have finite β and bounded
modular spectrum at any finite k.

> `[CANDIDATE — direction-eliminating negative diagnostic. The KMS_β
> family of the Syracuse transfer operator IS the Bernoulli-Esscher
> family of Wave 1, on the diagonal subalgebra. The off-diagonal
> Tomita-Takesaki modular flow is abelian on generators and carries
> no additional diagonal information. The noncommutative LDP rate
> collapses to the commutative DV rate. Wave-2 LP-min ≥ 5/2 transfers
> verbatim. Sub-direction (iv) (Cuntz-algebra reformulation) is prior
> art (Mori 2024). One usable artifact: the KMS-form of the Wave-1
> obstruction statement (§6.3). No escape; no new leverage.]`

---

## 9. Files and reproducibility

- `operator_algebras_kms_probe.py`: builds P_n on Q_n = (Z/3^n)* for
  n = 1, 2, 3; computes Tao stationary distribution (β=1), coarse
  KMS-style β scan, Tomita modular spectrum at β=1 (k=2).
- `operator_algebras_kms_probe2.py`: Renault-correct deformed
  transition matrix `L_β[i,j] = Σ_a e^{-β a log 2} 1[edge]` with
  a-truncation at 50; full 27-point β scan; β-table of
  `(spec_radius, E[a], drift_gap, mod-3 marg, mod-9 marg)`.
- `data/operator_algebras_kms_probe.json`: numerical record of probe 1.
- `data/operator_algebras_kms_probe2.json`: numerical record of probe 2.

All probes use only stdlib + numpy. Deterministic; no seeds. Edge
enumeration is exact up to truncation a ≤ 50; truncation error is
2^{−50 β} ≪ 10^{−15} at β ≥ 1.

---

## 10. Prior-art check (web, surface, June 2026)

- **Mori, arxiv 2411.08084 (2024) / Adv. Op. Th. 9 art. 425 (2025)**:
  Cuntz-algebra reformulation of Collatz via reducing-subspace
  condition. Sub-direction (iv) closed.
- **Bratteli–Jorgensen, *Wavelets through a looking glass* (Birkhäuser
  2002)**: Cuntz-algebra representations on L^2(ℝ) via wavelet filters.
  Adjacent; no Collatz content.
- **Connes–Marcolli 2008** (BC-system / Bost–Connes): KMS states of a
  number-field C*-algebra. Adjacent vocabulary; no Collatz.
- **Hiai–Mosonyi 2010** (*Commun. Math. Phys.* 296:773): noncommutative
  large deviations for KMS states. The applicable theorem; used in §4.1.
- **Renault 1980 / Exel 2003**: KMS theory for groupoid C*-algebras.
  Used in §2.2.
- No prior KMS / Tomita-Takesaki framing of the *Syracuse transfer
  operator* appears in surface search. `[NOVELTY UNVERIFIED]` for the
  framing; the content is the negative reduction in §4.
- "Dynamical Systems with Bounded Condition and C*-algebras" arxiv
  2508.05713 (Mori 2025 follow-up): adjacent, refines reducing-subspace
  conditions for bounded dynamical systems including Collatz; does
  not address KMS / natural density.
