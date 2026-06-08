# Vector 3 — Recapturing the chain-rule slack Δ₂ at a *non-product* extremizer: why it still does not exceed ψ

**Author:** Alex Ye (AI assistance disclosed separately)
**Status:** `[failed — quantitative obstruction; Step-1 certified; ψ sharp within this family]`
**Date:** 2 June 2026
**Companion code:** `frankl/experiments/vector3_delta2_nonproduct.py` (new),
`verify_ahs.py`, `joint_opt.py`, `single_letter.py`, `entropy_bounds.py` (reused).
**Run log:** `frankl/experiments/data/vector3_delta2_run.txt`.
**Cross-ref:** `vector1_shearer_chain_rule.md` (Δ₂≡0 at the *product* extremizer);
`experiments/results.md` (Vector 3 "enlarging the coupling ⇒ threshold ↓0.359");
`shared/dead_ends.md` (the false 0.4295 / 0.5 budget-mismatch artifacts);
`RED_TEAM_REPORT.md` (Doc 2, Doc 4 verdicts).

> **Outcome.** Recapturing Δ₂ at a **non-product** extremizer **does not beat
> ψ = (3−√5)/2**. We construct an explicit family of non-product couplings (the
> shared-auxiliary-`U` conditionally-i.i.d. coupling, and a correlated-Bernoulli
> coupling) on which Δ₂ > 0, and prove — analytically and over all UC orbit reps
> at n≤5 (29,723 with |F|≥2; 29,327 at n=5 alone) — that the recaptured Δ₂
> **cannot lift the certified constant above ψ**, because:
> 1. **(asymptotic obstruction)** On the shared-`U` coupling, Δ₂ ≤ I(C;U) ≤
>    H(U) ≤ log₂k is **O(1)**, while the budget H(A) is **Θ(n)**. Per coordinate
>    the recaptured slack vanishes: Δ₂/n → 0. The dimension-free constant is
>    governed by the per-coordinate ratio, on which Δ₂ contributes nothing.
> 2. **(direction obstruction)** In the honest finite-block ledger, recapturing
>    Δ₂ *subtracts* it from the comparison denominator, which moves the certified
>    constant **the wrong way** (c_aug ≤ c_AHS, with equality iff Δ₂=0). The
>    apparent gains (the "0.43–0.5" numbers, and the ρ>0 correlated coupling) are
>    exactly the **budget-mismatch / favourable-coupling artifacts already logged
>    in `dead_ends.md`** — we reproduce them deliberately and dissect why they are
>    not certificates.
> 3. **(sharpness gate)** The per-coordinate Sawin lower bound that the whole
>    assembly relies on is **invalid for every c > ψ** (its minimum over (p,q)
>    flips negative exactly past ψ). No augmentation of the *additive* Δ₂ term can
>    repair a lower bound that has already failed.
>
> **Best CERTIFIED constant: ψ.** No fabricated certificate; no number > ψ
> survives the gate + the all-families sweep.

---

## 1. The augmented objective, stated precisely

### 1.1 The exact identity and the honest necessary condition

Let `F ⊆ 2^[n]` be union-closed, `A,B` i.i.d. with some law on the indicator
cube (uniform-on-`F` in the base case, or a coupling defined in §3–§4),
`C = A∪B`. Gilmer's chain rule (`opt_formulation.md` §2) splits

```
H(C) = Σ_i H(C_i | C_{<i})
     = Σ_i H(C_i | A_{<i},B_{<i})  +  Σ_i I(C_i;(A_{<i},B_{<i})|C_{<i})
     =:        chain-LB            +        Δ₂                          (1.1)
```

with `Δ₂ ≥ 0` (sum of conditional mutual informations). The AHS method then
**drops Δ₂** (uses `chain-LB ≤ H(C)`), applies the per-coordinate Sawin
inequality to `chain-LB`, and closes against the budget `H(C) ≤ H(A)`.

**Recapturing Δ₂** means *keeping* the `+Δ₂` term. Under the contradiction
hypothesis `max_i p_i < c`, the Sawin per-coordinate inequality (S_c) below gives
`chain-LB ≥ (1/(2(1−c)))·S` with `S := Σ_i (1−p_i) H(A_i|A_{<i})`, so by (1.1) and
the budget,

```
(1/(2(1−c)))·S  +  Δ₂   ≤   chain-LB + Δ₂  =  H(C)  ≤  H(A) = log₂|F|.      (AUG)
```

A contradiction (hence `max_i p_i ≥ c`) is forced as soon as the left side
exceeds `H(A)`. **(AUG) is the augmented necessary condition**; the AHS bound is
the special case where the `+Δ₂` is discarded.

### 1.2 What would have to hold for the certified constant to exceed ψ

The method certifies a constant `c` iff **two** things hold:

* **(Gate) the per-coordinate inequality is valid at level `c`:**
  ```
  h(1−(1−p)(1−q)) ≥ (1/(2(1−c)))·[(1−q)h(p)+(1−p)h(q)]   for all p,q∈[0,1].   (S_c)
  ```
  This is the *only* lower bound on `chain-LB` the method has. **(S_c) holds iff
  `c ≤ ψ`** — equality at `(ψ,ψ)`, and `min_{p,q} G_c < 0` for any `c > ψ`
  (verified, `sawin_lower_bound_min`; this is the AHS sharpness, RED-TEAM Doc 1).
* **(Leverage) the assembled left side of (AUG) exceeds `H(A)`** at the worst
  configuration with `max_i p_i = c`.

To beat ψ via Δ₂-recapture, the `+Δ₂` term would have to supply enough leverage
at some `c > ψ` to compensate the **already-negative** slack of (S_c) at that `c`.
The rest of this document shows it provably cannot, in the families we construct:
the Δ₂ available is too small (asymptotically zero per coordinate) and enters with
the wrong sign in the finite ledger.

> **Direction sanity (defeats the first false positive).** Writing the
> finite-block certified constant as `c_aug = 1 − S/(budget − Δ₂)`: since `Δ₂ ≥ 0`,
> subtracting it can only *decrease* the denominator, hence *decrease* `c_aug`.
> Recapturing Δ₂ **lowers** the per-block constant unless Δ₂ = 0. So at the level
> of the honest ledger, Δ₂-recapture is not even pointed uphill. (The only way to
> make it look like a gain is to inflate the *budget* — the trap of §5.)

---

## 2. The product baseline (Vector 1, recalled) and the one escape it leaves

`vector1_shearer_chain_rule.md` proved **Δ₂ ≡ 0 at the AHS product extremizer**
(i.i.d. Bern(ψ), independent coordinates), so (AUG) collapses to the AHS bound and
`c = ψ`. The single escape it flagged: move the worst case **off the product**,
onto a coupling with `Δ₂ > 0`, and hope the recaptured Δ₂ now bites. This document
takes that escape and closes it. We need an explicit non-product family; §3 builds
the natural one (shared `U`), §4 the correlated-Bernoulli one.

---

## 3. A family of non-product couplings: shared auxiliary `U` (conditionally i.i.d.)

### 3.1 Definition (explicit `U`)

Fix `k ≥ 1`, atoms `p_1,…,p_k ∈ [0,1]`, weights `w_1,…,w_k ≥ 0`, `Σw_j = 1`.

> **Coupling `Q_{p,w}^{(n)}`.** Draw `U = j` with probability `w_j`. Given `U=j`,
> draw the `n` coordinate pairs `(A_i,B_i)`, `i=1..n`, **i.i.d.** with `A_i,B_i`
> independent `Bern(p_j)`. The **same** `U` is shared across all `n` coordinates.

This is **non-product**: marginally, the coordinates of `A` are exchangeable but
*not* independent — they are correlated through the latent `U`. It is exactly the
conditionally-i.i.d. ("de Finetti with `k` atoms") coupling that Liu/Yu-type
constructions live on, and the class where `vector1` said Δ₂ > 0. The single-letter
marginal of a coordinate pair is the mixture `Σ_j w_j Bern(p_j)^{⊗2}`, whose
support sits on the **diagonal** `{(p_j,p_j)}` of the `(P,Q)`-plane (because given
`U` the two are i.i.d. with the *same* parameter). Implemented and computed
**exactly** (no Monte Carlo) in `SharedUCoupling`, exploiting exchangeability
(group by popcount / prefix-count classes).

### 3.2 The exact ledger and the asymptotic obstruction

For `Q_{p,w}^{(n)}` the four quantities decompose cleanly (all exact):

```
H(A)   = H(U) + n·E_j[h(p_j)],                                    (3.1)  [A iid given U]
H(C|U) = n·E_j[h(u_j)],   u_j := 2p_j − p_j²,                     (3.2)
H(C)   = H(C|U) + I(C;U),     with  0 ≤ I(C;U) ≤ H(U) ≤ log₂k,    (3.3)
Δ₂     = H(C) − chain-LB  ≤  I(C;U).                              (3.4)
```

**Lemma 3 (Δ₂ ≤ I(C;U)).** *In `Q_{p,w}^{(n)}`,
`Δ₂ = H(C) − Σ_i H(C_i|A_{<i},B_{<i}) ≤ I(C;U) = H(C) − H(C|U)`.*

*Proof.* For each `i`, conditioning on the extra variable `U` cannot increase
entropy, and given `U` the coordinate `C_i` is independent of the prefixes
`(A_{<i},B_{<i})`:
`H(C_i|A_{<i},B_{<i}) ≥ H(C_i|A_{<i},B_{<i},U) = H(C_i|U)`. Summing over `i`,
`chain-LB ≥ Σ_i H(C_i|U) = H(C|U)` (coordinates i.i.d. given `U`). Hence
`Δ₂ = H(C) − chain-LB ≤ H(C) − H(C|U) = I(C;U)`. ∎ *(Verified numerically to
machine precision, `vector3…py`/run log: Δ₂ ≤ I(C;U) on every case, gap > 0.)*

**Corollary 4 (per-coordinate Δ₂ vanishes).** `Δ₂/n ≤ I(C;U)/n ≤ (log₂k)/n → 0`.

> **Remark 4′ (the obstruction survives `k → ∞`: the full exchangeable/de Finetti
> class).** One might try to defeat Cor. 4 by letting the number of atoms `k` grow
> with `n`, so `H(U)` is no longer `O(1)`. It does not help. For *any* exchangeable
> coupling on the cube, de Finetti's theorem represents the law as a mixture over a
> **one-dimensional** directing parameter `θ ∈ [0,1]` (the per-coordinate `Bern(θ)`
> rate); the latent `θ` is statistically resolvable from `n` coordinates only to
> precision `O(1/√n)`, so the relevant `I(C; θ) = O(log n)`, whence
> `Δ₂/n = O((log n)/n) → 0` **for the entire conditionally-i.i.d. class**, finite-`k`
> or not. Verified directly with `k = n` atoms (run log/stress test): `H(U) = log₂k`
> grows but `Δ₂/n ≤ 0.0071 → 0` and `c_aug ≤ c_AHS` throughout. The shared-`U`
> obstruction is therefore *not* an artifact of finitely many atoms — it is the
> generic fact that a single latent mixing parameter carries only `O(log n)` bits.

This is the **asymptotic obstruction**. The dimension-free constant is determined
by the *per-coordinate* limits

```
H(A)/n → E_j[h(p_j)],     H(C)/n → E_j[h(u_j)],     Δ₂/n → 0,                 (3.5)
```

(the `H(U)` and `I(C;U)` terms are `O(1)` and wash out). The recaptured slack Δ₂
is asymptotically **negligible against the budget** `H(A) = Θ(n)`. Numerically
(run log, k=6, n=128): `H(A)/n = 0.7386 → E[h(P)]=0.7194`, `H(C)/n=0.6351 →
E[h(U)]=0.6156`, `Δ₂/n = 0.0056 → 0`. The biggest finite-n recapture we see is
`Δ₂/H(A) ≈ 0.026` (k=6, n≈8), peeling off as n grows.

### 3.3 The single-letter limit is the diagonal mixture ⇒ threshold ψ

By (3.5) the dimension-free feasibility inequality (IV) for `Q_{p,w}` is

```
E_j[h(u_j)]  ≤  E_j[h(p_j)]               (Δ₂ contributes 0 per coordinate),   (3.6)
```

a **mixture over the same per-point crossover** `h(2p−p²) ≤ h(p)` whose threshold
is `ψ` for *every* atom (crossover identity `2p−p²=1−p ⟺ p²−3p+1=0 ⟺ p=ψ`). So
the minimal mean marginal consistent with (3.6) is again `ψ`: the shared-`U`
coupling, despite `Δ₂ > 0` at finite `n`, certifies **exactly ψ** in the limit.
This is the *same conclusion* as the "diagonal" auxiliary-`U` reading in
`joint_opt.py`/`results.md` §3.2 — and now we see *why* recapturing Δ₂ does not
rescue it: the only Δ₂ available is the `O(1)` term `I(C;U)`, which is exactly the
`O(1)` correction that the per-coordinate normalization discards.

### 3.4 The finite-block reading, and the anticorrelation made exact

One might still hope a **finite** block of `k` coordinates with a *fixed* `Δ₂ > 0`,
charged against a *fixed* `H(A)`, beats ψ. It does not, for the direction reason of
§1.2: in the honest ledger `c_aug = 1 − S/(H(C) − Δ₂)`, the recaptured Δ₂ shrinks
the denominator, so `c_aug ≤ c_AHS = 1 − S/H(C)`, with equality iff Δ₂=0. The data
(run log, PART A) shows this on every coupling and every `n`:

| coupling | n | Δ₂ | c_AHS | c_aug (honest, budget H(C)) |
|---|---|---|---|---|
| k=6 spread | 8 | 0.177 | 0.3928 | **0.3747** (↓) |
| k=4 spread | 16 | 0.164 | 0.3572 | **0.3490** (↓) |
| k=2 [.3,.5] | 32 | 0.110 | 0.3801 | **0.3778** (↓) |

`c_aug` is **always ≤ c_AHS**: recapturing Δ₂ moves the certified constant *down*.
And the two values **coincide exactly where it matters** — as the configuration
approaches the extremizer (`c_AHS → ψ`), `Δ₂ → 0`, so the recapture is null.

> **The anticorrelation, quantified (the core honest deliverable).** Over all UC
> orbit reps n≤5, bucketed by abundance, `max Δ₂/H(C)` grows monotonically with
> abundance: it is **0 at abundance 0.5** (the extremizer) and only reaches
> `≈0.19–0.23` at abundance ≥ 0.75 (families already far above ψ). Among the
> families within `5×10⁻³` of the AHS floor, `max Δ₂/H(C) ≈ 2.1×10⁻³ → 0` as
> `c_AHS → ψ`. **Large Δ₂ ⟺ already-high abundance.** The slack you could recapture
> is, to leading order, *proportional to how far above ψ you already are* — so it
> can never *create* the gap from ψ; it only appears once the gap is already there.
> This is the exact mechanism by which the empirical anticorrelation "reasserts
> itself and cancels the gain" (the brief's question, answered: **it cancels**).

---

## 4. The correlated-Bernoulli coupling, and the favourable-coupling trap

### 4.1 Definition

Single parameter `p` and a Pearson correlation `ρ` between `A_i` and `B_i`:
`P(A_i=B_i=0) = (1−p)² + ρ p(1−p)`, so `P(C_i=1) = 1 − P(0,0) = u_ρ(p)`. `ρ=0`
recovers the independent AHS coupling. Implemented as `correlated_union_p`.

### 4.2 Why ρ>0 *appears* to beat ψ — and why it is not a certificate

The single-letter crossover `h(u_ρ(p)) ≤ h(p)` has threshold (run log, PART C):

| ρ | crossover p\* | vs ψ |
|---|---|---|
| −0.30 | 0.3518 | −0.030 |
| 0 | **0.38197** | **ψ** |
| +0.10 | 0.3927 | +0.011 |
| +0.50 | 0.4385 | +0.057 |

Positive correlation `ρ>0` **lowers** the union probability `u_ρ(p)` (A and B
overlap more, so their union is smaller), which raises the crossover above ψ. This
is the mirror image of `results.md`'s "enlarging the coupling ⇒ threshold ↓0.359":
there a *free off-diagonal* coupling (which includes `ρ<0`) lowers the bound;
here a *forced `ρ>0`* coupling raises it. **Neither is a valid certificate for
Frankl**, for the same structural reason:

> The entropy method's budget `H(C) ≤ H(A)` and the chain-rule decomposition
> **presuppose `A ⟂ B`** (two independent uniform draws). A union-closed family
> sampled by two i.i.d. copies has `ρ = 0` **forced**; you cannot choose `ρ>0`.
> Imposing `ρ>0` is choosing a *favourable* coupling that does **not** correspond
> to any i.i.d.-sample necessary condition — it changes the meaning of `H(A)` and
> silently injects `I(A;B) > 0` that the budget does not account for. It is a
> *sufficient*-direction artifact, not a lower bound valid for all UC families.

The gate (§1.2, S_c) makes this rigorous and **rejects it automatically**: the only
constant the method can certify is gated by `min_{p,q} G_c ≥ 0`, i.e. `c ≤ ψ`,
*regardless* of which coupling one daydreams about, because (S_c) must hold for
**all** `(p,q)` — including the independent point `ρ=0` that the budget actually
forces.

---

## 5. The two traps reproduced and dissected (so they are not "rediscovered")

`dead_ends.md` records two false positives a prior agent killed: a **0.4295** from
a single-budget mismatch and a **0.5** from a buggy per-family heuristic. The
present family *reproduces both* if one is careless — we surface them on purpose:

* **Budget-mismatch (the 0.43–0.5).** Define the **dishonest** ledger
  `c_augHA := 1 − S/(H(A) − Δ₂)` using the *raw* budget `H(A)` instead of the
  value `H(C)` that appears in the tight chain. On finite families `H(A) > H(C)`
  (union closure concentrates mass: `2^[2]` has `H(A)=2` bits but `H(C)=1.6226`),
  so the larger `H(A)` in the denominator inflates the constant — `2^[2] → exactly
  0.5`, and `min_F c_augHA = 0.44998` over n≤5. **This is the documented artifact.**
  The gap `H(A) − H(C)` is the union-closure slack that vanishes per coordinate
  asymptotically (§3.2); treating it as headroom for Δ₂ **double-counts** the same
  bits. The honest ledger uses `H(C)` (equivalently `budget − Δ₂ = chain-LB`), and
  gives `min_F c_aug = 0.38235` — which, like the AHS finite-family minimum
  `0.38266`, sits a hair *above* ψ only because finite families are not the
  asymptotic extremizer, and satisfies `c_aug ≤ c_AHS` family-by-family, both → ψ.
  *(If your number smells like 0.43 or 0.5, you used `H(A)` where you owed `H(C)` —
  exactly this bug.)*
* **Floor-sweep non-sequitur (the would-be 0.39).** The family-level floor
  `(1/(2(1−c)))S + Δ₂ ≤ H(A)` **does** hold numerically on all small UC families
  even at `c = ψ + 10⁻²` — but this certifies nothing, because the per-coordinate
  lower bound (S_c) it rests on is **already invalid for `c > ψ`** (gate flips
  negative at `(p,q)≈(ψ,ψ)`). Small finite families simply are not the extremizer;
  "the floor holds on a finite list" is not "the bound is valid." The run log
  prints the gate and the floor sweep **side by side** so the non-sequitur is
  visible: gate `INVALID` while floor `HOLDS` for every `c > ψ`.

Both traps share a signature: a quantity that is `Θ(1)` slack on small/finite
families (the `H(A)−H(C)` gap; the finite-family floor headroom) is mistaken for
asymptotic room. The discipline that kills them is the same: **normalize per
coordinate / use the gate**, where every such finite slack is `o(1)`.

---

## 6. The verdict and exactly how the tradeoff balances

**There is NO non-product configuration in this family with a certified constant
> ψ.** Quantitatively, recapturing Δ₂ at a non-product extremizer buys

```
gain  =  Δ₂           ≤  I(C;U)  ≤  H(U)  ≤  log₂k     =  O(1),
cost  =  the budget against which it is charged, H(A)  =  Θ(n),
```

so the **per-coordinate** gain `Δ₂/n → 0`: in the dimension-free constant the
recaptured Δ₂ contributes **exactly zero**, and the constant is the diagonal
`U`-mixture threshold **ψ** (§3.3). In the **finite-block** ledger the recaptured
Δ₂ enters with the **wrong sign** (`c_aug = 1 − S/(H(C)−Δ₂) ≤ c_AHS`, §1.2/§3.4),
so it cannot help there either; and the only way to flip the sign — using `H(A)`
in place of `H(C)` — is the documented **budget-mismatch artifact** (§5). Finally,
the **anticorrelation is exact** (§3.4): the recoverable Δ₂ is, to leading order,
proportional to the amount by which abundance already exceeds ½, so it can only
appear *after* the gap from ψ exists, never *create* it. The Δ₂-gain is offset
**three times over** — asymptotically (→0), directionally (wrong sign), and
structurally (anticorrelated with the deficit it would need to fill).

### 6.1 Does this close "is the method's ceiling exactly ψ"?

**Partially — it closes it for the families we can construct and certify, and it
sharpens the obstruction; it does not settle the fully general question.** What is
now established (Step-1 certified, all-families sweep, gate):

* Within the **i.i.d.** coupling: ceiling ψ (Vector 1, Δ₂≡0 at product).
* Within the **shared-`U` conditionally-i.i.d.** coupling (the natural non-product
  class, where Liu-type constructions live): ceiling ψ, because Δ₂/n→0 and the
  limit is the diagonal `U`-mixture (§3). **This is the new content** relative to
  Vector 1: it removes the "but Δ₂>0 off the product" escape by showing the off-
  product Δ₂ is asymptotically irrelevant in this class.
* The **favourable-coupling** routes (ρ≠0, free off-diagonal) do not give valid
  necessary conditions (§4), so they are not loopholes.

**The honest gap that remains.** We have *not* reproduced Liu's `0.38271` (his
exact `I(C;U)/I(A;U)` functional is in an arXiv paper that is HTTP-403 in this
environment — see `results.md` §4, `dead_ends.md`). Liu's gain is real and *does*
exceed ψ; our analysis shows it **cannot come from the additive Δ₂ term as
formalized in (AUG)** within the shared-`U` class — it must come from a *different*
bookkeeping of `I(C;U)` vs `I(A;U)` (a **finite-`n` / boundary** effect, or a
*relative* `I(C;U)/I(A;U)` comparison, not the additive `+Δ₂`). Pinning down
exactly which of those Liu exploits — and whether *that* mechanism caps at his
`0.38271` or could be pushed further — requires the primary source and is **left
open**. So: the method's ceiling is **ψ for the pure additive-Δ₂ recapture in the
i.i.d. and shared-`U` classes** (closed here), but the *general* entropy-method
ceiling (with Liu's relative-information bookkeeping) is **> ψ and not settled by
this work**.

---

## 7. Reproduction & certification status

* **Step 1 (computational):** PASS. `python3 vector3_delta2_nonproduct.py`
  reproduces (a) Δ₂ ≤ I(C;U) and Δ₂/n→0 on the shared-`U` family; (b) the diagonal
  `U`-mixture limit; (c) the ρ-coupling crossover table; (d) the all-families
  (n≤5, 29,723 reps with |F|≥2) sweep: `min c_aug (honest) = 0.38235`, no
  certified value above ψ; (e) the gate flipping `INVALID` for every `c > ψ` while the floor sweep
  `HOLDS` (the non-sequitur exhibited). Run log: `data/vector3_delta2_run.txt`.
* **No new constant is claimed.** The best **certified** constant is **ψ**, by the
  already-certified AHS route (`certificate_0.38197.md`); nothing here is
  upgraded. There is therefore **no** "PENDING RED-TEAM" claim — by design, since
  the verdict is a negative.
* **Honesty checks honored:** the 0.43–0.5 and 0.39 numbers that *do* appear are
  explicitly the `dead_ends.md` artifacts, reproduced and dissected, **not**
  presented as improvements.

**Bottom line.** The one live lever — recapture Δ₂ off the product — is closed for
the i.i.d. and shared-`U` non-product classes: the off-product Δ₂ is `O(1)`, hence
**per-coordinate zero**, enters the finite ledger with the wrong sign, and is
anticorrelated with the very deficit it would need to fill. **ψ stands.**
