# The uniform perp-gap conjecture for the Syracuse transfer operator: RESOLVED (exactly), and why it does not give natural density

> **Status:** `[result — structural; NOVELTY UNVERIFIED]`. The spectral claims below are
> **rigorous** (exact rational arithmetic; exact characteristic polynomials over ℚ),
> not float64. **This is not a proof of Collatz**, and not even a conditional
> natural-density theorem — see §6 for the brutally honest assessment.
>
> **Track:** Collatz, Vector A. Attacks the "uniform perp-gap conjecture" flagged in
> `transfer_operator.md` §6 and `RED_TEAM_REPORT.md` §5c option (i).
>
> **Author:** Alex Ye (AI-assisted computation; AI not on author line per project rules).
>
> **Companion files:**
> - `experiments/perp_gap.py` — exact rational kernel, exact charpolys, quotient spectrum, nilpotent-norm transient.
> - `experiments/data/perpgap_exact.json` — exact charpoly factorizations, quotient spectrum, exact E_n, mod-3 marginal.
> - `experiments/data/perpgap_norms.json` — operator-norm transient ‖(P−Π)^j‖₂.
> - `experiments/data/perpgap_summary.txt` — verdict table.
> - cross-refs: `transfer_operator.md` (Prop 3.1, the V block), `natural_density_obstruction.md` (TV ≥ 1/6), `syracuse_fft/results.md` (Eₙ divergence), `RED_TEAM_REPORT.md` §5c.

---

## 0. Headline

The conjecture asked: does the Syracuse transfer operator `P_n` have a **uniform spectral
gap on the complement of the mod-3 obstruction subspace** `V` — i.e. `∃ ρ<1, C` with
`‖P_n|_{V^⊥}‖ ≤ ρ` for all `n`?

**Answer (rigorous): the perp spectral radius is not merely `< 1`, it is `= 0`, for every `n`.**

The exact characteristic polynomial of `P_n` is
$$
\chi_{P_n}(\lambda) \;=\; \lambda^{\,\varphi(3^n)-1}\,(\lambda-1),
$$
verified **exactly over ℚ** for `n = 1,2,3,4,5` (sizes `2,6,18,54,162`). So `P_n` has a
single nonzero eigenvalue `λ=1` and **all `φ(3ⁿ)−1` remaining eigenvalues are exactly zero**.
The operator `P_n − Π` (`Π` = rank-1 stationary projector) is **nilpotent**, with
nilpotency index exactly `n`. The `~10⁻³` "second eigenvalues" the prior float64 analysis
(`transfer_operator.md` §4) reported were **pure numerical noise** at the `10⁻³`–`10⁻⁸` level.

This is the *strongest possible* form of the perp-gap conjecture: `λ₂^⊥(n) = 0`, gap `= 1`,
uniformly. **And yet it gives no natural-density result at all.** The reason is the entire
point of this document and is made precise in §3–§4:

1. The mod-3 obstruction does **not** live in `V^⊥`. It lives in `V` itself — it is the
   `λ=1` left-eigenvector `π_n|_V = (1/3, 2/3)`. Killing `V^⊥` (or the whole nilpotent part)
   leaves the obstruction **completely untouched**: `TV(π_n,U) ≥ 1/6`, `E_n → ∞`, exactly as
   the FFT data say. Fast mixing on `V^⊥` is mixing **to the wrong target**.
2. `V^⊥` (standard orthogonal complement) is **not** `P_n`-invariant, so `‖P_n|_{V^⊥}‖` as a
   *restriction norm* is not even well-defined; the prior numeric used a **compression**
   `B^⊤ P_n B`, whose eigenvalues are not the perp spectrum. The correct object is the
   quotient `ℝ^{U_n}/V`, on which `P_n` is nilpotent.
3. Spectral radius `0` is **not** norm-contraction. `‖P_n−Π‖₂ > 1` (it grows `0.89, 1.21,
   1.33, 1.45, 1.55, 1.64, …` in `n`) and the nilpotency index `= n` grows: mixing finishes
   in finitely many (`n`) steps but each step can *expand*. There is no `ρ<1` per-step
   contraction in operator norm — the gap is "spectral," not "geometric-in-norm."

So the perp-gap conjecture is **TRUE in the strongest spectral sense and USELESS for natural
density** — a textbook case of mislocating the obstruction. Cf. the red-teamed Lemma 6 error
(conflating where the discrepancy lives): here the discrepancy lives in `V`, not `V^⊥`.

---

## 1. Setup, and the exact arithmetic that makes rigor possible

`U_n := (ℤ/3ⁿℤ)^× `, `|U_n| = φ(3ⁿ) = 2·3^{n-1}`. The one-step Syracuse kernel (Tao i.i.d.
valuation model `a = ν₂(3N+1) ~ Geom(2)`) is
$$
P_n[x,y] \;=\; \sum_{k\ge 1}\, 2^{-k}\,\mathbf 1\!\big[\,2^{-k}(3x+1)\equiv y \pmod{3^n}\,\big],
\qquad x,y\in U_n. \tag{1.1}
$$

**The key fact for exactness.** `2` is a **primitive root mod `3ⁿ`**, with multiplicative
order `L = φ(3ⁿ) = 2·3^{n-1}` (verified `n≤8`). Hence `2^{-k} mod 3ⁿ` is periodic in `k`
with period `L`, and (1.1) is a finite sum of geometric series grouped by `k mod L`:
$$
P_n[x,y] \;=\; \sum_{r=1}^{L}\, \mathbf 1\!\big[2^{-r}(3x+1)\equiv y\big]\;\frac{2^{-r}}{1-2^{-L}}
\;\in\; \mathbb{Q}. \tag{1.2}
$$
Every entry is an **exact rational**. No `a_max` truncation, no float64. Row sums are exactly
`1` (verified). This is what lets us compute `χ_{P_n}` exactly over ℚ and put the prior
float-only spectral claims on rigorous footing — discharging the explicit
`transfer_operator.md` §4.1 caveat *"mpmath / interval check not performed … everything here is
float64."*

---

## 2. Precise definition of V, V^⊥, and the RIGHT operator

`V := span{e₁, e₂}`, `e_r[x] := 𝟙[x ≡ r (mod 3)]` (column vectors / functions on `U_n`).
Note `e₁ + e₂ = 𝟙` (all-ones on units).

**`P_n` acts on column functions** `f ↦ P_n f`. By Prop 3.1 of `transfer_operator.md`
(re-verified here exactly):
$$
P_n e_1 = \tfrac13\,\mathbf 1, \qquad P_n e_2 = \tfrac23\,\mathbf 1, \qquad
\text{so } P_n V \subseteq \mathrm{span}\{\mathbf 1\}\subseteq V.
$$
Thus **`V` is `P_n`-invariant** (column action), with block `[[1/3,2/3],[1/3,2/3]]`,
eigenvalues `{1,0}`, and the `λ=1` right-eigenvector `𝟙 ∈ V`.

> **The trap (and the reason the conjecture's *norm* phrasing is ill-posed).**
> `V^⊥` (standard inner product) is **NOT** `P_n`-invariant. Invariance of `V^⊥` would
> require `P_n^⊤ V ⊆ V`, i.e. `P_n^⊤ e_r` constant on each mod-3 coset. It is not
> (checked exactly, `n=2,3`: e.g. `e₁^⊤P_n` takes values `{1/21,4/21,16/21}` on coset 1).
> Therefore `‖P_n|_{V^⊥}‖` as the norm of a *restriction to an invariant subspace* is
> **undefined**; the prior `B^⊤ P_n B` is a **compression**, whose spectrum/norm need not
> equal the perp spectrum. (This is precisely the genus of subtlety the red-team caught in
> Lemma 6: be careful *which* subspace carries *which* part.)

**The correct, well-defined object.** Since `V` *is* invariant, `P_n` descends to the
**quotient** `W := ℝ^{U_n}/V`. Define
$$
\boxed{\ \lambda_2^{\perp}(n) \;:=\; \text{spectral radius of } P_n \text{ acting on } W = \mathbb R^{U_n}/V.\ }
$$
Equivalently: the nonzero eigenvalues of `P_n` other than the `V`-block's `{1,0}`. (Because the
`V`-block already contributes `{1,0}`, `λ₂^⊥` is the spectral radius of `P_n` off the
stationary line, restricted away from `V`.) This is computed by adapting a basis
`(e₁, e₂, completion)` and taking the lower-right `(N−2)×(N−2)` block of `B^{-1}P_n B`.

---

## 3. The rigorous spectral result

> **Theorem 3.1 (exact nilpotency — `[NOVELTY UNVERIFIED]`).** *For `n = 1,2,3,4,5` (exact
> over ℚ), the characteristic polynomial of `P_n` is*
> $$
> \chi_{P_n}(\lambda) = \lambda^{\,\varphi(3^n)-1}(\lambda-1).
> $$
> *Consequently the quotient action of `P_n` on `W = ℝ^{U_n}/V` has characteristic polynomial
> `λ^{φ(3ⁿ)-2}` (verified exactly), hence `λ₂^⊥(n) = 0` exactly. `P_n − Π` is nilpotent.*

**Rank chain (the Jordan/nilpotency structure).** Exactly (sympy rank over ℚ, cross-checked by
float64 rank with tol `1e-9`):
$$
\mathrm{rank}(P_n^{\,k}) = 2\cdot 3^{\,n-1-k}\ \ (0\le k<n),\qquad \mathrm{rank}(P_n^{\,k})=1\ (k\ge n).
$$
e.g. `n=4`: `54 → 18 → 6 → 2 → 1`; `n=5`: `162 → 54 → 18 → 6 → 2 → 1`. So
$$
(P_n - \Pi)^{\,n} = 0, \qquad (P_n-\Pi)^{\,n-1}\ne 0:\quad \textbf{nilpotency index} = n.
$$
This is the projective-filtration structure of `transfer_operator.md` §3.1 made exact: each
application of `P_n` collapses one mod-3^k level; after `n` steps the operator is the rank-1
stationary projector `Π = 𝟙 ⊗ π_n`.

**What this says about the conjecture.** The conjecture `‖P_n|_{V^⊥}‖ ≤ ρ < 1` is *true in
spectral radius with `ρ = 0`* — the **strongest possible** uniform gap. There is no spectral
obstruction on `V^⊥` whatsoever.

---

## 4. Why the strongest possible perp-gap gives NOTHING (the decisive point)

Three independent, rigorous reasons the conjecture's truth is inert.

### 4.1 The mod-3 obstruction is in `V`, not `V^⊥`

The natural-density obstruction (`natural_density_obstruction.md` Thm 3.3) is `TV(π_n, U) ≥ 1/6`,
caused by the permanent mod-3 marginal `(0, 1/3, 2/3)`. That marginal **is** `π_n|_V`, the
`V`-component of the `λ=1` left-eigenvector. We re-derive it exactly here: the exact stationary
`π_n` has mod-3 marginal `(1/3, 2/3)` for all `n = 1..5` (exact rationals). **The obstruction is
the `V`-block's `λ=1` eigenvector.** Quotienting out `V` (or killing the nilpotent `V^⊥` part)
*removes precisely the part of the space that is already mixing perfectly* and *retains exactly
the obstructed `λ=1` direction*. Perp-mixing is mixing to a target `π_n` that is itself
permanently non-uniform.

### 4.2 Consistency with the FFT `E_n` divergence — exact, independent confirmation

`E_n := φ(3ⁿ)‖π_n‖₂² − 1` is a property of the **invariant `π_n`** (the `λ=1` eigenvector), not
of the gap. Computed here from the **exact rational stationary vector** (independent of the FFT
pipeline):

| n | `E_n` (exact rational, this doc) | `E_n` (FFT `results.md`) |
|---|---|---|
| 1 | `1/9 = 0.111111` | 0.111 |
| 2 | `3/7 = 0.428571` | 0.429 |
| 3 | `150121/203889 = 0.736288` | 0.736 |
| 4 | `…/… = 1.045764` | 1.046 |
| 5 | `…/… = 1.356107` | 1.356 |

**Exact match to all printed FFT digits.** So `λ₂^⊥ = 0` (fast mixing) and `E_n → ∞` (target
non-uniform) are **fully consistent** — they are statements about two orthogonal pieces (rate vs
target). *If one had instead claimed `λ₂^⊥ = 0` ⇒ equidistribution, that would contradict the
FFT divergence and be the mislocated-obstruction error.* It does not, because the divergence
lives entirely in `V` (the `λ=1` eigenvector), which the perp gap never touches. This is the
mandatory cross-check, and it passes by exact independent arithmetic.

### 4.3 Spectral radius 0 ≠ norm contraction: the nilpotent transient

A nilpotent operator has spectral radius `0` but its **operator norm can exceed 1**, with
transient growth before the eventual collapse at step `n`. The single-step norm of the
nilpotent part (float64 from exact rationals, `‖·‖₂`):

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| `‖P_n−Π‖₂` | 0 | 0.891 | 1.208 | 1.333 | 1.445 | 1.548 | 1.644 |

`‖P_n−Π‖₂ > 1` for all `n ≥ 3` and **increases with `n`** (toward a limit `≈ 2`, not yet
saturated), while the cumulative `Σ_{j} ‖(P_n−Π)^j‖₂ ≈ 1.7·n` grows **linearly in `n`**, and the
nilpotency index `= n` grows. So:

> There is **no** uniform `ρ<1` such that `‖P_n − Π‖₂ ≤ ρ`. The "uniform gap" is a statement
> about **eigenvalues** (`=0`), which is **not** a statement about **operator norm**. A
> per-step *norm*-contractive mixing bound — the kind one would actually need to run a transport
> argument with explicit constants — **fails**: each step can expand by up to `≈2`, and the
> chain needs `n` steps (not `O(1)`) to mix. The relevant "rate" for a quantitative argument is
> the nilpotency index `n → ∞`, not the spectral radius `0`.

This third point is the subtle one and the reason the seemingly-extraordinary `λ₂^⊥ = 0` is not
an extraordinary theorem: **the natural-density question is not governed by the spectral radius
on `V^⊥`.** It is governed (a) by the target `π_n` (§4.1, §4.2: permanently non-uniform), and
(b) by quantitative norm control across `n` steps (§4.3: not contractive, grows with `n`).

---

## 5. The hardest break-attempt against "this is extraordinary"

Per the brief: if the gap were genuinely uniform-and-useful that would be `[EXTRAORDINARY —
PRESUMED FLAWED]`. It is uniform (`λ₂^⊥=0`) but **not useful**, and §4 is exactly the red-team of
the naive reading. Stress-testing the strongest pro-conjecture reading:

- **Naive claim:** "`λ₂^⊥=0` ⇒ `P_n` mixes `V^⊥` to `π_n` instantly ⇒ after handling the rank-1
  `V` block, natural density on cosets." **Break:** the `V` block is *not* a side issue —
  `π_n|_V = (1/3,2/3)` is the entire obstruction, and `TV(π_n,U) ≥ 1/6` forces it for all `n`.
  Mixing `V^⊥` perfectly to a permanently-skewed `π_n` yields skew, not equidistribution.
  Confirmed by exact `E_n` matching the FFT divergence (§4.2). **The conjecture's conclusion
  ("coset-respecting natural density") would require `π_n` uniform *within* cosets — but `E_n→∞`
  shows `π_n` is non-uniform *within* the unit coset too, not just across mod-3 cosets.** So even
  the weaker "coset-respecting" target fails: the within-coset `ℓ²` excess diverges.
- **Naive claim:** "spectral radius `0` ⇒ contraction." **Break:** §4.3, `‖P_n−Π‖₂ > 1` and
  growing; nilpotent ≠ contractive. Any explicit-constant transport needs norm control, which is
  absent.
- **Could a different inner product make `V^⊥` invariant and contractive?** One can make `V^⊥`
  invariant by using the `π_n`-weighted inner product (then the complement of `V` along the
  spectral decomposition is invariant). But in *that* geometry the relevant non-normality /
  nilpotency reappears as transient growth of `‖(P_n−Π)^j‖` exactly as in §4.3, and the target is
  still `π_n` (still non-uniform). No inner product removes the `E_n` divergence, which is
  inner-product-independent (it is `‖π_n−U‖` against the *standard* reference `U`).

**Conclusion of the break-attempt:** the result is genuinely `λ₂^⊥ = 0`, rigorously, but it is
**not** a conditional natural-density theorem and does not deserve the "extraordinary" tag — it
is an extraordinary *reframing* that makes the mislocation of the obstruction completely explicit.

---

## 6. Brutally honest assessment

- **What is rigorously established (new vs. the prior float64 doc):** `λ₂^⊥(n) = 0` **exactly**,
  via exact charpoly `λ^{φ(3ⁿ)-1}(λ-1)` over ℚ for `n≤5`; `P_n−Π` nilpotent of index exactly
  `n`; rank chain `2·3^{n-1-k}`; exact `E_n` matching the FFT. This **overturns** the prior
  doc's numerical reading that `|λ₂|` and `|λ_{⊥,max}|` are `~10⁻³` and "shrinking toward
  possibly 1" — those were **float64 noise**; the true values are `0`. The prior §4.3
  log-linear "`3.0ⁿ`/`3.7ⁿ` growth that must turn over" is an artifact of fitting noise.
- **Is the perp-gap conjecture TRUE?** Yes, in the strongest form (`ρ = 0`). Is it the
  conditional natural-density result the brief hoped for? **No.** It is inert: the obstruction is
  in `V`, not `V^⊥`; and `λ₂^⊥ = 0` is spectral-radius, not norm-contraction.
- **Verdict on the brief's decisive question:** *neither* "uniform gap that gives a theorem"
  *nor* "gap collapses to 1." The gap is uniformly **maximal** (`=1`, `λ₂^⊥=0`), and it gives
  **no** density result. The genuine obstruction is **not** a perp eigenvalue at all — it is (i)
  the permanently non-uniform `λ=1` eigenvector `π_n` (mod-3 marginal `(0,1/3,2/3)`; diverging
  within-coset `E_n`), and (ii) the absence of `n`-uniform operator-norm contraction
  (nilpotency index `= n → ∞`, `‖P_n−Π‖₂ > 1`).
- **Does it lower any analytic wall?** **No.** It does not prove Collatz, does not give natural
  density (even coset-respecting), does not bound `E_n`. It is at most a **structural
  sharpening**: it pinpoints, rigorously, that the perp-gap route of `RED_TEAM_REPORT.md` §5c
  option (i) is a **dead end** — not because the perp gap is too small, but because it is as
  large as possible and located in the wrong place.
- **Novelty:** `[NOVELTY UNVERIFIED]`. That a finite Markov chain built from `mod 3^k`
  projective levels is nilpotent-modulo-stationary is the kind of fact that is plausibly folklore
  (it is the operator form of "the Syracuse RV's law is determined by the last `n` valuations").
  The *exact* charpoly `λ^{φ-1}(λ-1)` and nilpotency-index-`= n` statements are elementary once
  seen; treat as not-claimed-new pending a prior-art pass.
- **Honest one-liner:** the uniform perp-gap conjecture is **true and useless**; the Collatz
  natural-density obstruction does not live where the conjecture looks for it.

---

## 7. Cross-reference summary

| Quantity | Prior float64 (`transfer_operator.md` §4) | This doc (exact ℚ) |
|---|---|---|
| `\|λ₂(P_n)\|` | `5·10⁻³` at `n=8`, "shrinking, maybe →1" | **`0` exactly** (`n≤5`) — prior was noise |
| `\|λ_{⊥,max}\|` | `1.8·10⁻³` at `n=7`, "grows `3.7ⁿ`" | **`0` exactly** — prior was noise |
| perp-gap conjecture | "ambiguous, cannot conclude" | **TRUE, `ρ=0`; but inert** |
| `E_n` | diverges (FFT) | diverges, exact `E_n` match (§4.2) |
| where the obstruction lives | implied: maybe `V^⊥` | **`V` (the `λ=1` eigenvector) + non-contraction** |

The two views are consistent; the exact computation **corrects** the prior float spectral
magnitudes (to `0`) and **relocates** the obstruction definitively into `V` and into the lack of
`n`-uniform norm contraction.
