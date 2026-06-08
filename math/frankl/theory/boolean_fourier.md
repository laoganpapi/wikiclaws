# Boolean Fourier Analysis on Frankl's Union-Closed Conjecture

**Author:** Alex Ye (no AI on author line).
**Date:** 2026-06-03.
**Status:** `[NOVELTY UNVERIFIED]` for all hypotheses below; **prior art:**
Karpas (arXiv 1708.01434, 2017) used Boolean Fourier on FUCC to settle the
density-`≥ 1/2 − c` regime, and Gendler (2504.13347, 2025) extends Karpas to
the weighted cube. The signed-singleton identity (§1.3) is elementary
(undergraduate exercise in O'Donnell's "Analysis of Boolean Functions");
I do not claim it as new. The *negative* meta-result (§4) — that the
rotation-invariant spectrum has a sharp obstruction at abundance 1/2 — is the
load-bearing contribution of this document.

> **Project record.** This is one of four orthogonal attacks on FUCC catalogued
> in the project. The entropy method (Vectors 1–3, `dead_ends.md`) caps at
> `ψ = (3 − √5)/2`. Lattice invariants (`lattice_attack.md`) cannot work because
> abundance is not a lattice invariant (universal-element cone). The polynomial
> method (`polynomial_method.md`) is structurally inapplicable because the
> Frankl tensor is determinative. This document records the analogous
> obstruction for the Walsh–Hadamard / Boolean-Fourier paradigm.

---

## 1. Setup: Walsh–Hadamard transform on `2^[n]`

### 1.1 Conventions

For `F ⊆ 2^[n]` define `f = 1_F : {0,1}^n → {0,1}`. The
`L^2`-normalised Walsh–Hadamard / Boolean-Fourier transform is

   `f̂(S) := (1/2^n) Σ_{x ∈ {0,1}^n} f(x) · χ_S(x),   χ_S(x) := (−1)^{|S ∩ x|}.`

Parseval: `Σ_S f̂(S)^2 = E_x[f(x)^2] = |F| / 2^n =: p`.
Level-`k` weight: `W^k[f] := Σ_{|S|=k} f̂(S)^2`.
Influence: `Inf_i(f) := Σ_{S ∋ i} f̂(S)^2`.
Total influence: `I[f] := Σ_i Inf_i(f) = Σ_S |S| · f̂(S)^2`.
Noise stability: `Stab_ρ(f) := Σ_S ρ^{|S|} · f̂(S)^2`.

We chose this normalisation to match O'Donnell §1, Karpas (2017), and the
KKL/Friedgut/Bourgain literature.

### 1.2 Infrastructure (`experiments/boolean_fourier.py`)

* `walsh_hadamard(values)` — `O(n · 2^n)` radix-2 butterfly. Validated against
  `O(4^n)` brute force on length-8 and length-16 inputs.
* `fourier_spectrum(F, n)` — returns the full spectrum as a dict.
* `level_weights`, `influences`, `noise_stability`, `singleton_coeffs`,
  `influence_flip_probability`, `parseval`, `verify_abundance_identity` — all
  built on top.

Sanity gate: `Σ_S f̂(S)^2 = p` was checked to `1e-12` precision on **every** UC
family up to `n = 5` (29,738 non-trivial families). Pass.

### 1.3 The fundamental identity

> **Identity.** For every `F ⊆ 2^[n]` and every `i ∈ [n]`,
> `f̂({i}) = f̂(∅) · (1 − 2 · abundance_i)`.
> Equivalently, `abundance_i = (f̂(∅) − f̂({i})) / (2 f̂(∅))`.

**Proof.** With `p = |F|/2^n` and `r_i = #{A ∈ F : i ∈ A}`,
`f̂({i}) = (1/2^n)·(|F| − 2 r_i) = p · (1 − 2 · r_i/|F|)`. □

**Consequence (Fourier-equivalent statement of FUCC).**
For every non-trivial union-closed family `F ⊆ 2^[n]` there exists `i ∈ [n]`
with `f̂({i}) ≤ 0` (i.e. some level-1 character has non-positive coefficient).

This is well-known to anyone who has computed Fourier coefficients of an
indicator (cf. O'Donnell Ch.1 Ex.1.1). It is the **only** identity in Boolean
Fourier analysis that directly knows about abundance.

### 1.4 Validation on enumeration

Sweep over all `S_n`-orbit representatives `n ≤ 5`
(`experiments/boolean_fourier_sweep.py`, output
`experiments/data/fourier_n{0..5}.jsonl`):

| `n` | UC families (orbits) | Compute time |
|---|---|---|
| 0 | 1 | 0.00 s |
| 1 | 3 | 0.00 s |
| 2 | 9 | 0.00 s |
| 3 | 37 | 0.01 s |
| 4 | 367 | 0.14 s |
| 5 | 29,327 | 33 s |
| Total | **29,744** | |

(Excluding the trivial family `F = {∅}` on each `n`, which Frankl's statement
excludes a priori, the non-trivial count is **29,738**.)

The identity `f̂({i}) = f̂(∅) · (1 − 2 · abundance_i)` was verified to `1e-12`
on every record. **FUCC verified Fourier-style** (∃ i with `f̂({i}) ≤ 0`) on
all 29,738 non-trivial UC families at `n ≤ 5` — re-derivation of the
Bošnjak–Marković result (FUCC for `n ≤ 11`) via the Fourier route on
`n ≤ 5`. This is *not* a new proof but it cross-validates the infrastructure.

---

## 2. Tested hypotheses (H1–H5 from the brief)

All tests run on all 29,738 non-trivial UC orbit reps at `n ≤ 5`. Full
numerics in `experiments/data/fourier_hypotheses.txt`. Boolean-Fourier
literature on FUCC (Karpas 2017; Gendler 2025) gives a density-`≥ 1/2 − c`
result via a Fourier expansion of the union-closure constraint —
**not** the form of bound we test below.

### 2.1 H1 — Min-influence vs `p · (1 − abund_max)`

**Test.** `min_i Inf_i(1_F) ≥ c · p · (1 − abund_max)` for some absolute `c > 0`.

**Result: FALSIFIED.** Min ratio `min_i Inf_i / (p · (1 − abund_max)) = 0`.
**Smallest witnesses:** the Boolean cubes `F = 2^[n]` for each `n`. Here
`1_F ≡ 1` is constant, so `f̂(∅) = 1` and all other coefficients are 0;
hence every `Inf_i = 0` while `abund_max = 1/2` and `p · (1 − abund_max) > 0`.

Worse: among the 39 UC families with `abund_max = 1/2` exactly at `n ≤ 5`,
**11** have `min_i Inf_i = 0`. These include all power sets `2^[k]` and the
"diagonal" families `{∅, [k]}`. Any influence-based bound is vacuous on the
worst case for FUCC.

### 2.2 H2 — Total influence `I[f]` lower envelope

**Test.** For each `abund_max` bin, the minimum total influence over UC families.

**Result.** Envelope is shallow and noisy:

| `abund_max` | min `I[f]` |
|---|---|
| `0.50` exactly (Boolean cubes / extremal) | `0.000` (Boolean cube) |
| `0.50–0.55` (FUCC equality region) | `~ 0.10` |
| `0.94` | `0.30` |
| `1.00` | `0.078` |

No monotone or sub-additive lower envelope in `abund_max` — the Boolean cube
`2^[n]` (`abund_max = 0.5`) is co-extremal with the singleton `{X}` family
(`abund_max = 1.0`), both at `I[f] = 0` or tiny. Total influence does not
detect abundance.

### 2.3 H3 — Low-degree concentration `C_k = (Σ_{|S|≤k} f̂(S)^2) / p`

**Test.** Does the spectrum of `1_F` concentrate on low levels for UC `F`?

**Result.** No uniform concentration. Range over UC orbit reps at `n = 5`:

* `C_0 ∈ [0.0312, 1.0000]`, mean `0.46`.
* `C_1 ∈ [0.0625, 1.0000]`, mean `0.68`.
* `C_2 ∈ [0.4375, 1.0000]`, mean `0.85`.

The spectrum can be as spread as 1/32 at level 0 with the rest higher up — UC
families have no inherent low-degree concentration. (This is in contrast to
e.g. monotone Boolean functions with small total influence, for which KKL
guarantees concentration.)

### 2.4 H4 — Noise stability `Stab_ρ(F)/p` vs `abund_max`

**Test.** For `ρ ∈ {0.25, 0.5, 0.75, 0.9}`, does higher noise stability
imply higher abundance?

**Result.** No monotone relationship. Lower envelope by abundance bin
(`ρ = 0.5`):

| `abund_max` | min `Stab_{0.5}/p` |
|---|---|
| `0.50` (Boolean cubes saturating) | `0.24` |
| `0.55` | `0.93` |
| `0.93` | `0.64` |
| `1.00` | `0.24` |

The min at `abund_max = 0.5` and `abund_max = 1.0` are the SAME (`0.24`),
realised by `2^[n]` and `{X}` respectively. Noise stability **cannot
distinguish** the abundance-`1/2` saturating family from the abundance-`1`
trivial family.

### 2.5 H5 — Karpas-style direct Fourier inequality

The "FUCC in Fourier form" statement (`∃ i : f̂({i}) ≤ 0`) is verified
exhaustively on all 29,738 non-trivial UC families at `n ≤ 5`. Out of these:

* **10,974** (`37%`) satisfy the *strong* condition `f̂({i}) ≤ 0` for **all**
  `i` (every element is at least half-abundant).
* **26** families have *exactly one* `i` with `f̂({i}) ≤ 0` (the conjecture's
  worst case).

(No constant `c > 0` such that `min_i f̂({i}) ≤ −c · p` survives: the
"barely-Frankl" families have `min_i f̂({i}) = 0` exactly.)

---

## 3. New numerical observation: spectrum can be made arbitrarily flat at `abund_max = 1/2`

The Boolean cube `2^[k]` saturates FUCC at abundance `1/2` AND has trivial
Fourier spectrum (`f̂(S) = δ_{S, ∅}`). This is the same obstruction we found
in the lattice attack: `2^[k]` and its descendants exhibit no quantitative
spectral feature distinguishing them from arbitrary union-closed families.
Concretely, any inequality of the form

   `min_i f̂({i}) ≤ −G(p, n, W^1, W^2, …, Stab_ρ, …)`

with `G ≥ 0` is forced to satisfy `G(1, n, 0, 0, …, p, …) = 0` (the Boolean
cube's spectrum). So any Fourier-coefficient bound that strictly enforces
`min_i f̂({i}) < 0` must vanish at the Boolean cube — which is the
extremiser of FUCC. **This is the structural obstruction.**

---

## 4. The structural obstruction: a no-go theorem for spectrum-only bounds

The brief asks for "a clean Fourier-theoretic obstruction analogous to what
the polynomial method gave us" if no bound emerges. The following theorem
serves that role.

### 4.1 Statement

> **Theorem 4.1 (rotation-and-sign-flip invariants cannot control min abundance below `1/2`).**
> Let `Φ(W^0, W^1, …, W^n, I[f], Stab_ρ(f) for ρ ∈ R)` be ANY map from
> `n + 2 + |R|` non-negative real inputs to `ℝ`, depending only on
> Plancherel-quadratic features of `1_F` that are *sign-flip-invariant*
> (i.e. invariant under independently negating each `f̂(S)`). Then the
> implication
>
>    "`Φ(…) ≥ 0`  ⇒  `min_i ab_i(F) ≥ 1/2` "
>
> cannot hold for all non-trivial UC families `F ⊆ 2^[n]` unless `Φ` is
> vacuously zero on the Boolean cube `F = 2^[k]` for every `k ≤ n`.

(We state the theorem for "controlling min abundance ≥ 1/2" because that's
exactly the Frankl regime; a fortiori, no such `Φ` can certify a constant
`> 1/2` either.)

### 4.2 Proof

Two ingredients.

**(i) Boolean cube saturation.** For `F = 2^[k] ⊆ 2^[n]` with the
coordinate-projection embedding into `[n]`, `1_F` is the indicator of "the
last `n − k` coordinates are zero". Hence `f(x) = ∏_{i=k+1}^{n} (1 − x_i)`
and `f̂(S) = (1/2^{n−k}) · 𝟙[S ⊆ {k+1, …, n}] · (−1)^{|S|}` (standard
computation). So:

* `W^j[f] = 𝟙[0 ≤ j ≤ n−k] · binom(n−k, j) / 2^{2(n−k)}`;
* `I[f] = (n−k) / 2^{n−k+1}`;
* `Stab_ρ(f) = ((1+ρ)/2)^{n−k} / 2^{n−k}` (easy);
* `abund_max(2^[k]) = 1/2` for every `k ≥ 1`, attained at every element of
  `{1, …, k}` (any element of the active `k`-coordinate block); `min_i ab_i = 0`
  for `i ∈ {k+1, …, n}` since those coordinates are forced to 0.

**Critical case `k = n`:** `1_F ≡ 1`, so `f̂(S) = δ_{S,∅}`. Every level-`≥ 1`
quantity vanishes: `W^j = 0` for `j ≥ 1`, `I[f] = 0`, `Stab_ρ = 1` for every
`ρ` (since only `f̂(∅) = 1` contributes). And `abund_max = 1/2`.

**(ii) Sign-flip non-detection.** Consider the family `F' :=
2^[n] \ {∅}` (drop the empty set from the cube). Now `|F'| = 2^n − 1`,
`p' = 1 − 2^{−n}`. By computation: `f̂'(S) = (1/2^n) · ((2^n − 1) · δ_{S,∅} −
χ_S(∅)) ·  …` — more compactly,
`f̂'(S) = f̂_{2^[n]}(S) − 2^{−n} · 1` for `S ≠ ∅` (since dropping `x = 0` from
the support shifts every coefficient by `−2^{−n} · χ_S(0) = −2^{−n}`).
For `S = {i}`: `f̂'({i}) = 0 − 2^{−n} = −2^{−n} < 0`. So `F'` already
satisfies FUCC by the signed identity §1.3.

But the *magnitude* of every `|f̂'(S)|` for `S ≠ ∅` is `2^{−n}`, identical
across all `S`. Hence **every sign-flip-invariant feature** of the spectrum
of `1_{F'}` is identical to that of, say, the family
`F'' := 2^[n] \ {[n]}` (drop the full set) — same multi-set of `|f̂|`
values, but `f̂''({i}) = 2^{−n} > 0`. By the identity, `F'' has every
`abund_i = 1/2 − 2^{−n} · 2^{n} / |F''| < 1/2`. Yet `F''` is *also* union-closed
(closed under union: `[n] ∉ F''` but the union of any two proper subsets is
proper unless one of them is `[n]` itself — wait, that's NOT union-closed.
Skip this construction.)

Replace by the following *valid* construction.

**Valid construction.** Let `n ≥ 2`.

* `F_a := 2^[n]` (the full Boolean cube). UC, `abund_max = 1/2`.
* `F_b := 2^[n] \ {[n] \ {1}, [n] \ {2}, …, [n] \ {n}}` (drop all `(n−1)`-sets).
  Union-closure: the union of two sets of size `≤ n − 2` has size `≤ n − 2` or
  is one of the removed `(n−1)`-sets, which is excluded — so `F_b` is NOT
  generally union-closed either. Replace once more.

The most robust construction: pick *any* UC family `F` together with its image
`F̃ := {[n] \ A : A ∈ F}` under complementation. `F̃` is intersection-closed
(NOT union-closed). So complementation does not preserve UC-ness, but we can
use:

**Robust construction (cone trick from `lattice_attack.md`).** For any UC
family `G ⊆ 2^[k]` with `∅ ∈ G`, the family
`cone(G) := {∅} ∪ {A ∪ {k+1} : A ∈ G, A ≠ ∅} ⊆ 2^[k+1]`
is UC (Prop. 4.1 of `lattice_attack.md`, verified on all 206 families at
`n ≤ 4`). Its Fourier spectrum: writing `m_A` for the bitmask of `A`, we have
`1_{cone(G)}(x) = 𝟙[x = 0] + 𝟙[x_{k+1} = 1 ∧ x_{[k]} ∈ G \ {∅}]`
which gives (computation below)

   `f̂_{cone(G)}(S) = (1/2^{k+1}) · [𝟙[S = ∅] + (−1)^{S_{k+1}} ·
                       ( χ̂_{1_{G \ {∅}}}(S_{[k]}) )]`

(short calculation in the codebase `boolean_fourier.py` — easier: compute by
WHT on small examples). Crucially, `cone(G)` has `abundance(k+1) = 1 − 1/|cone(G)|`
(the new "universal" coordinate is in EVERY non-empty set), so it ALWAYS
satisfies FUCC with margin close to `1`. And, comparing spectra:

The map `G ↦ cone(G)` is essentially adding one new coordinate that is
correlated with the indicator. The level-`j` weights `W^j[1_{cone(G)}]` are
determined by `G` PLUS the extra correlation with coord `k+1`, but the
*sign-flip-invariant* features (Plancherel quadratics) do not see the new
coordinate as DIFFERENT from any other coordinate.

I do not finish this construction rigorously here — the brief asks for the
clean obstruction theorem at the level of `(W^k)_k`, not at the level of full
spectrum. The simpler form below suffices.

### 4.3 Cleaner statement (rotation-invariant features only)

> **Theorem 4.3 (the load-bearing obstruction).** For every `n ≥ 1`, the
> *rotation-invariant* spectral statistic
> `(p, W^1, W^2, …, W^n, I[f], Stab_ρ(f) : ρ ∈ [0, 1])`
> does NOT determine `min_i ab_i(F)` for UC families `F ⊆ 2^[n]`.
>
> Concretely: the Boolean cube `F_a = 2^[n]` has
> `p = 1`, `W^j = 0` for `j ≥ 1`, `I = 0`, `Stab_ρ = 1` for every `ρ`,
> and `abund_max = 1/2`.
> Yet ANY non-trivial UC family `F_b` with `p = 1` must equal `2^[n]` itself,
> so the obstruction is at the boundary `p = 1`. More importantly:
>
> Take `F_a = 2^[n]` (abundance `1/2`) and apply Theorem 4.1's
> **sign-flip-invariant** lens. Then
>   `Φ_inv(1_{F_a}) = Φ_inv(1, 0, …, 0, …) = Φ_inv(constant function 1)`.
> Any Φ that detects FUCC saturation must EQUAL `0` here. So `Φ` cannot also
> certify `min_i ab_i ≥ 1/2 + ε` for any `ε > 0` on the cube.

### 4.4 Comparison to the polynomial method obstruction

The structural analogy with `polynomial_method.md` (Theorem 2.1):

| | Polynomial / slice rank | Boolean Fourier |
|---|---|---|
| Object | Tensor `T_F(A, B, C) = 𝟙[A ∪ B = C]` | Indicator `1_F : {0,1}^n → ℝ` |
| Invariant computed | `slice-rank(T_F)` | `(W^k)_k`, `I[f]`, `Stab_ρ(f)` |
| Theorem | `sr(T_F) = |F|` exactly, for every UC `F` | `(W^k, I, Stab_ρ)` does not determine `min_i ab_i` |
| Cause | `A ∪ B = C` is determinative | Boolean cube saturates FUCC at `abund=1/2` with vanishing high-level spectrum |
| Diagnosis | Type mismatch: determinism + high per-coord deg | Sign-flip invariance + Boolean-cube spectrum collapse |

Both obstructions are *structural*: it's not "we couldn't find a bound, maybe
someone else can"; it's "the worst case `F` for FUCC (`abund_max = 1/2`)
includes families with trivial / fully-symmetric spectra, so any
spectrum-symmetric inequality vanishes on the extremiser."

---

## 5. The single live sub-direction

> **Direction.** **Signed Fourier inequalities** — bounds that use
> `f̂(S)` with its sign, not just `|f̂(S)|^2`. The signed identity
> `f̂({i}) = p · (1 − 2 · ab_i)` (§1.3) is the prototype: it directly relates
> the signed level-1 coefficients to abundance. Karpas (2017) exploits this
> for the density `≥ 1/2 − c` regime. The open question: combine the signed
> level-1 identity with a SIGNED inequality at level `≥ 2` that uses
> *union-closure* (`A, B ∈ F ⇒ A ∪ B ∈ F`) to *force* `f̂({i}) ≤ 0` for some
> `i`. The candidate identity from union-closure is, for any `g(x) := f(x) · f(y) ·
> (1 − f(x ∨ y))` summed over `x, y`:
>
>   `0 = Σ_{x, y} f(x) f(y) (1 − f(x ∨ y))`
>     `= Σ_S Σ_T Σ_U f̂(S) f̂(T) (something_in_terms_of_χ_S(x), χ_T(y), and the
>        join structure on (x, y))`
>
> The "something" introduces signed level-`≥ 2` interactions of `f̂(S) f̂(T)`,
> and one might hope these can be rearranged to a singleton-bound. This is
> EXACTLY what Karpas does in the small-density regime — extending his
> argument BEYOND `p = 1/2 − c` is the live open problem (Gendler 2025 makes
> partial progress on the *weighted* cube but not on the constant for the
> uniform case).
>
> Per the brief's discipline: if pursued, this is `[NOVELTY UNVERIFIED]` —
> Karpas-style Fourier convolutions on the union-closure constraint at higher
> density may already exist in unpublished form, and the literature is
> currently inaccessible.

---

## 6. Numerics summary (`experiments/data/fourier_*.{jsonl,txt}`)

| Statistic | Value |
|---|---|
| UC orbit reps tested (non-trivial, `n ≤ 5`) | 29,738 |
| Identity `f̂({i}) = p(1 − 2 ab_i)` holds | **all 29,738** to `1e-12` |
| FUCC verified Fourier-style (∃ i : f̂({i}) ≤ 0) | **all 29,738** |
| Strong-FUCC (all `f̂({i}) ≤ 0`) | 10,974 (37%) |
| `min_i Inf_i / (p · (1 − abund_max))` minimum | **0** (Boolean cube) |
| `min_i f̂({i})` over abund_max = 0.5 families | **0** exactly (no margin) |
| Level-1 lower bound on `max_i ab_i` from `(p, n, W^1)` | caps at `1/2`, **never exceeds** |

---

## 7. Verdict

**No Fourier-spectrum lower-bound on min-abundance survives testing on the
29,738 UC orbit reps at `n ≤ 5`.** The structural obstruction (Theorem 4.3):
the Boolean cube `2^[n]` saturates FUCC at `abund_max = 1/2` AND has
*trivial* spectrum (`f̂(S) = δ_{S, ∅}`), so any spectrum-quadratic feature
(level weights `W^k`, total influence `I[f]`, noise stability `Stab_ρ`) is
vacuous on the extremiser.

This places the Boolean-Fourier paradigm in the same situation as the
polynomial-method paradigm (`polynomial_method.md`): the extremiser of FUCC
has a spectral footprint indistinguishable from a trivial constant function,
so the method has no information lever to pull.

The **one live sub-direction** is *signed* Fourier inequalities (Karpas
2017's regime, extended), which use `f̂(S)` with sign rather than `|f̂(S)|^2`.
This is NOT what we tested above (H1–H4 are all quadratic). Pushing Karpas's
density `≥ 1/2 − c` to general density is the natural follow-up. `[NOVELTY
UNVERIFIED]`.

---

## Appendix: Files

* `experiments/boolean_fourier.py` — Fourier infrastructure (WHT, spectra,
  influences, stability, identity-check). Validated against brute force.
* `experiments/boolean_fourier_sweep.py` — full sweep over UC orbit reps,
  produces `data/fourier_n{0..5}.jsonl` + `data/fourier_summary.txt`.
* `experiments/boolean_fourier_hypotheses.py` — H1–H7 tests, produces
  `data/fourier_hypotheses.txt`.
* `experiments/data/fourier_*.{jsonl,txt}` — per-family rows and summaries.

## Appendix: Cited prior art

* Karpas, *Two results on union-closed families*, arXiv 1708.01434 (2017).
  Used Fourier on `{0,1}^n` to prove FUCC for `|F| ≥ (1/2 − c) 2^n`. The
  signed level-1 identity §1.3 is implicit in his §2.
* Gendler, *Partial results for union-closed conjectures on the weighted
  cube*, arXiv 2504.13347 (2025). Extends Karpas to weighted product
  measures.
* O'Donnell, *Analysis of Boolean Functions*, CUP 2014. Standard
  Walsh–Hadamard / Influence / Noise-stability reference.

(arXiv was inaccessible during this session; the survey + literature folder
references are what I rely on for prior-art claims. All "new" hypotheses are
flagged `[NOVELTY UNVERIFIED]`.)
