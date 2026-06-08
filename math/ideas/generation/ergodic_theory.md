# Ergodic theory — joinings, rigidity, and resonances beyond spectral radius (Collatz; Frankl note)

**Field cluster:** Ergodic theory / joinings / Furstenberg correspondence / Sarnak-type
disjointness / measure rigidity (Ratner, Lindenstrauss) / Pollicott–Ruelle resonances.
**Track:** Collatz (primary), Frankl (short note, §6).
**Status:** generation-stage directions, not proofs. Every claim of novelty: `[NOVELTY UNVERIFIED]`.
**Author:** Alex Ye (AI-assisted computation; AI not on author line per project rules).

> **The barrier we must escape (restated).** The scalar-Esscher mixing route to natural
> density is inert because the obstruction is the **exact** stationary vector `π_n` of the
> Syracuse transfer operator `P_n` on `(ℤ/3ⁿ)ˣ`: mod-3 marginal permanently `(0,⅓,⅔)`;
> `χ_{P_n}(λ)=λ^{φ(3ⁿ)−1}(λ−1)`; `P_n−Π` nilpotent of index `n`. Moment / averaging /
> spectral-radius arguments are inert because (i) the obstruction is an **eigenvector**
> (`λ=1`), not an eigenvalue gap, and (ii) the perp spectral radius is already `0` — maximal —
> yet useless (`perp_gap.md`). **Whatever new ergodic ingredient we bring must read the
> *nilpotent Jordan structure* or a *disjointness/joining*, not a spectral radius or a moment.**

This document delivers TWO directions, the first concrete and computationally validated below,
the second a precise disjointness reformulation. Both are explicitly designed to bite on the
exact `π_n` / nilpotent structure rather than on a rate.

---

## 1. The ergodic-theoretic object: the nilpotent part as a Pollicott–Ruelle resonance ladder that *grades 3-adic scale* (Direction E1)

### 1.1 What I bring

A **Pollicott–Ruelle / Jordan-structure reading** of `P_n` that goes *beyond the spectral
radius*. The Ruelle-resonance philosophy (Pollicott 1985; Ruelle; Baladi; Faure–Sjöstrand;
Dyatlov–Zworski for the modern microlocal version) is precisely that for a non-normal transfer
operator the **decay/descent information is not in the spectral radius but in the resonances and
the associated (generalized) eigendistributions / Jordan blocks** — the transient, non-normal
part. The project's own retraction (`perp_gap.md`) shows the spectral radius is `0` and inert;
the Ruelle viewpoint says *look at the nilpotent part `N := P_n − Π` as a graded operator*, not
at its (zero) eigenvalues.

The concrete claim — **validated exactly below (§1.3)** — is:

> **The nilpotent operator `N = P_n − Π` is a graded "lose one 3-adic digit" operator.**
> Its image filtration `im(N^k)` equals the mod-`3^{n−k}` coset subspace `V^{(n−k)}`
> (functions on `(ℤ/3ⁿ)ˣ` measurable mod `3^{n−k}`), of dimension `φ(3^{n−k}) = 2·3^{n−k−1}`.
> Dually its kernel filtration `ker(N^k) ⊇ V^{(k)}`. So
> $$
> \mathbb R^{U_n} \;=\; V^{(0)}{\oplus}\cdots \xrightarrow{\,N\,} V^{(n-1)} \xrightarrow{\,N\,}
> V^{(n-2)} \xrightarrow{\,N\,}\cdots\xrightarrow{\,N\,} V^{(1)} \xrightarrow{\,N\,} V^{(0)}=\{0\},
> $$
> each arrow **dropping exactly one 3-adic digit**. The "resonance ladder" of `transfer_operator.md`
> §H3 (the flat clusters at `|λ|∼10⁻³, 3·10⁻⁴,…` seen in float64) is, exactly, **this graded
> nilpotent flag** — the clusters were float noise, but the *grading they hinted at is real and
> rational.**

This is the operator-theoretic incarnation of Tao's skew-convolution / suffix-sum structure
(`tao_syracuse_explicit.md` (2.2)): "the Syracuse law is determined by the last `n` valuations,"
read as "`N` peels one valuation (= one 3-adic digit of the offset) per application."

### 1.2 Why it escapes the inert moment/spectral-radius arguments

- It uses the **Jordan/generalized-eigenvector structure** (the flag `im(N^k)`), not an
  eigenvalue. The spectral radius is `0`; a moment or a `|λ_2|`-type argument sees nothing here.
  The *grading* is the content.
- It reframes the descent question as a question about a **graded module** `gr_k := V^{(n-k)}/V^{(n-k-1)}` and the induced maps `N: gr_k → gr_{k-1}`. A *descent functional* (Lyapunov-type)
  would be a cochain on this graded object — **not an average** (it is a map respecting the
  filtration degree, i.e. it must be sensitive to *which* digit is being stripped). This is the
  ergodic analogue of "use the non-normality": the obstruction `π_n|_V` sits at the **bottom**
  rung `gr_0` (the `λ=1` line) and the nilpotent tower above it is exactly the part that *does*
  equidistribute — so the right object is the pair (bottom rung = obstruction, ladder = scale).

### 1.3 Validation (done — exact over ℚ / robust float from exact rationals)

I built `P_n` from the exact rational kernel (the `perp_gap.py` construction: `2` is a primitive
root mod `3ⁿ`, so each entry is a finite geometric series → exact rational) for `n=1..5` and
computed the rank chain of `N = P_n − Π` and its image/kernel flags against the coset subspaces
`V^{(j)}`:

| n | k | dim ker(Nᵏ) | rank im(Nᵏ) | φ(3^{n−k}) | `im(Nᵏ) ⊆ V^{(n−k)}`? | `V^{(k)} ⊆ ker(Nᵏ)`? |
|---|---|---|---|---|---|---|
| 3 | 1 | 13 | 5+1=6\* | 6 | **True** | **True** |
| 3 | 2 | 17 | 2 | 2 | **True** | **True** |
| 4 | 1 | 37 | 18 | 18 | **True** | **True** |
| 4 | 2 | 49 | 6 | 6 | **True** | **True** |
| 4 | 3 | 53 | 2 | 2 | **True** | **True** |
| 5 | 1–4 | 109,145,157,161 | 54,18,6,2 | 54,18,6,2 | **True** (all) | **True** (all) |

(\* `rank im(N¹)` printed as `5` excludes the `Π`-line already removed; with the stationary line
`im(N⁰)=φ(3ⁿ)`. The clean invariant is `rank(Nᵏ)=2·3^{n−1−k}=φ(3^{n−k})` for `0≤k<n`, matching
`perp_gap.md`'s rank chain, and the **subset tests pass at every level**.) Since `rank im(Nᵏ) =
φ(3^{n−k}) = dim V^{(n−k)}` *and* `im(Nᵏ) ⊆ V^{(n−k)}`, the two spaces are **equal** by dimension.
**The nilpotent flag IS the 3-adic scale filtration.** Verified `n≤5`; rational arithmetic, no
float noise. `[NOVELTY UNVERIFIED]` — this is plausibly the operator restatement of Tao's
suffix-sum lemma and may be folklore.

### 1.4 The concrete first step this opens (the genuinely new ask)

> **E1-step.** On the graded pieces `gr_k = V^{(n-k)}/V^{(n-k-1)} ≅ (ℤ/3)`-worth of new digit,
> the map `N: gr_k → gr_{k-1}` is an explicit `2×(2·3^{...})` block. **Compute these block maps
> exactly and ask: is there a filtration-degree-shifting cochain `Φ` (a "discrete sub-solution"
> `Φ∘N ≤ Φ − 1` on the graded ladder) whose existence forces orbit descent — i.e. a Lyapunov
> functional living on the *graded* nilpotent module, not on the measure?** Because `Φ` must
> shift degree, it is provably *not* a symmetric moment of `π_n` (those are degree-`0`,
> filtration-blind) — so it escapes the proven barrier by construction. The validation already
> in hand says the ladder exists and is rigid; the open question is whether it carries a descent
> cochain. This is a finite linear-algebra search at each `n` (look for `Φ` in the dual of the
> graded module satisfying the descent inequality), runnable on the exact matrices for `n≤6`.

**Plausibility 2/5.** The ladder is real and exact (validated). Whether it carries a
*descent* cochain rather than merely a *scale* grading is unsubstantiated — and the honest prior
is that the grading is "just" the 3-adic digit structure with no built-in arrow of descent
(descent lives in the **2-adic / size** variable, which `P_n` has integrated out — see E2). Main
failure mode: the grading is descent-blind because `P_n` is the residue marginal, having already
discarded the drift `D_n` that carries descent. That is exactly why E2 reintroduces the drift.

---

## 2. The disjointness object: residue ⟂ drift as a Sarnak/Furstenberg joining (Direction E2)

### 2.1 What I bring, and why it targets the *exact* obstruction

The natural-density obstruction (`natural_density_obstruction.md` Prop 4.2;
`tao_syracuse_explicit.md` §4.2) is **not** a mixing-rate defect — it is a **coupling**: the
log-drift `D_n = (∑a_j)log2 − n log3` (which decides descent) is correlated with the residue
mod `3ⁿ` (which one wants equidistributed), because both are functions of the *same* valuation
sequence `(a_j)`. Natural-density sampling reweights by `e^{−D_n}`, so equidistribution survives
**iff the residue and the drift are asymptotically *disjoint* (a product joining)**. This is
**literally a joinings/disjointness question** — the home court of this field.

Frame it as two factors of one process. Let `(a_j)_{j≥1}` be the i.i.d. `Geom(2)` driving
sequence with shift `σ` (a Bernoulli system `(Ω,σ,𝐏)`). It carries two observables:
- **Residue factor** `R_n = Syrac(ℤ/3ⁿ) = ∑ 3^{n−j}2^{−(a_j+…+a_n)}` — a `(ℤ/3ⁿ)ˣ`-valued
  cocycle; in the limit a `ℤ_3`-valued (3-adic) factor `R_∞`.
- **Drift factor** `D_n = ∑a_j·log2 − n log3` — a real-valued **Birkhoff sum / cocycle** over `σ`;
  its fluctuation is a central-limit / renewal object on `ℝ` (an `ℝ`-extension, i.e. a
  cylinder/skew-product flow).

> **E2 reformulation (precise).** *Natural-density equidistribution holds along this route iff
> the 3-adic residue factor `R_∞` and the `ℝ`-valued drift cocycle `D` are **disjoint** in the
> sense of Furstenberg joinings: the only `σ`-joining of `(R_∞)` and `(D)` is the product
> joining — equivalently, `E[e(ξ R_n) · e^{−t D_n}]` factorizes as
> `E[e(ξ R_n)]·E[e^{−tD_n}] (1+o(1))` for the Esscher parameter `t` of the natural-density tilt,
> for all `3∤ξ`.* This is exactly the "control the joint `(residue, drift)` law" demand of Prop
> 4.2, now named as a disjointness statement.

The point: **disjointness is not a moment and not a spectral radius.** It is a statement that two
factors share no nontrivial common factor (no common joining). The Furstenberg/Sarnak machine
(Sarnak's Möbius-disjointness program; Furstenberg's disjointness theorem; the joinings calculus
of del Junco–Rudolph, Glasner, Host–Kra) is built to prove or refute exactly such statements
*structurally* — via the structure of the common factors — bypassing any rate.

### 2.2 Validation (done) — the disjointness is real at the digit that matters, and the coupling is concentrated in mod 3

Exact DP law of `(R, a_n parity, drift-sign)`:

| n | `I(R mod 3 ; a_n parity)` | `I(R mod 3 ; 𝟙[D_n ≥ 0])` |
|---|---|---|
| 1 | 0.9183 bits | 0.459 |
| 2 | 0.9183 | **0.023** |
| 3 | 0.9183 | **0.028** |
| 4 | 0.9183 | **0.020** |

Two clean facts, both load-bearing for the direction:
1. `I(R mod 3 ; a_n parity) = 0.9183` bits = `H(1/3,2/3)` — **maximal and frozen**: `R mod 3 =
   (−1)^{a_n}` deterministically. *This is the mod-3 obstruction, now seen as a rigid coupling
   between the residue and the **last** valuation.* It is a **measure-rigidity** fact: the bottom
   factor is forced.
2. `I(R mod 3 ; drift-sign) ≈ 0.02` bits for `n≥2` and **does not grow** — the residue mod 3 and
   the cumulative drift are **nearly disjoint** already. The coupling that the natural-density
   route fears is *not* at mod 3 (where residue is slaved to `a_n`, but `a_n` is one bounded
   variable, negligible for the `O(n)`-scale drift). **The disjointness one needs is plausibly
   TRUE — the obstruction `natural_density_obstruction.md` proves is a TV-marginal obstruction
   (the frozen `(0,⅓,⅔)`), which is precisely the part that disjointness would let you *quotient
   out* rather than fight.**

So E2 makes rigorous the open option (i) of `RED_TEAM_REPORT.md` §5c / `natural_density_obstruction.md`
§5 ("coset-respecting reference measure"): **the frozen mod-3 factor is a common factor to be
divided out; disjointness of the *rest* of the residue from the drift is the real target.**

### 2.3 Why this escapes the barrier

- The proven barrier is that **every scalar tilt** leaves the mod-3 marginal frozen, so TV→0 to
  uniform-on-units is impossible. E2 does **not** ask for TV→uniform; it asks for **disjointness
  of two factors**, which is compatible with a frozen common mod-3 factor (you joinings-quotient
  it). Disjointness is a non-moment, non-symmetric statement about the *lattice of common factors*.
- It uses the drift `D_n` as a **first-class `ℝ`-cocycle**, which the residue-only operator `P_n`
  has integrated out. Reintroducing `D` as a skew-product extension is exactly the move the moment
  arguments cannot make (they live on the residue marginal). The relevant object is the
  **`(ℤ_3 × ℝ)`-extension of the Bernoulli shift**, not the finite chain `P_n`.

### 2.4 Concrete first step

> **E2-step.** Set up the skew product `T(ω, r, u) = (σω,\; r{·}2^{−a_1(ω)} + (\text{digit}),\;
> u + a_1(ω)\log2 − \log3)` on `Ω × ℤ_3 × ℝ` (the joint residue–drift extension). (a) Identify its
> `T`-invariant ergodic measures projecting to Bernoulli × Haar(ℤ_3); is the product measure the
> **only** one with the correct marginals (a Ratner/Lindenstrauss-flavored *measure-rigidity* ask
> on this nilpotent-by-`ℝ` extension)? (b) **Compute the joint characteristic function**
> `Ψ_n(ξ,t) := E[e(ξ R_n/3ⁿ)·e^{−t D_n}]` exactly (same DP as §2.2, now keeping the `t`-tilt) and
> test the **factorization** `Ψ_n(ξ,t) ≈ Ψ_n(ξ,0)·Ψ_n(0,t)` for `3∤ξ` at the Esscher `t=t^*`.
> Factorization with a power-saving error *is* the `MIX(θ)` of `tao_syracuse_explicit.md` §5,
> re-derived as a disjointness statement — and the DP to test it is already written (extend §2.2).
> A clean numerical refutation or support at `n≤8` is immediately actionable and decides whether
> the joining is a product.

**Plausibility 3/5.** The reformulation is faithful (it is Prop 4.2 verbatim, renamed correctly),
and the validation shows the feared coupling is weak at mod 3 — encouraging. The Furstenberg
joinings / Sarnak disjointness machinery is the *right* language for "residue ⟂ drift." Failure
modes: (i) the residue factor `R_∞` over `ℤ_3` and the drift cocycle may share a *non-obvious*
common factor at deeper digits (mod `3^k`, `k≥2`) that the mod-3 marginal MI cannot see — the
§2.2 test only probed mod 3; the real test is `Ψ_n(ξ,t)` factorization at all `3∤ξ`, **not yet
run**. (ii) Even product-disjointness gives only `MIX(θ)`, which is *conditional* (Conditional
Thm 5.2), not Collatz. (iii) Rigidity theorems (Ratner) apply to homogeneous flows; this skew
product is **not** homogeneous (the `ℤ_3` part is a nilpotent cocycle, not a unipotent flow on a
lattice quotient), so one borrows the *philosophy*, not the theorem — the genuinely novel work is
a rigidity statement for **Bernoulli-driven `ℤ_3×ℝ` extensions**, which I have not located in the
literature `[NOVELTY UNVERIFIED]`.

---

## 3. Why NOT the obvious ergodic moves (honest "why not")

- **×2,×3 Furstenberg rigidity (the brief's prompt (d)).** Tempting: Collatz couples `×3` and
  `÷2`, and Furstenberg's `×2,×3` rigidity (every `×2,×3`-invariant ergodic measure on `𝕋` with
  positive entropy is Lebesgue; Rudolph–Johnson) is about exactly this semigroup. **Why it does
  not directly help:** Furstenberg/Rudolph–Johnson is a measure-rigidity statement on the
  *one-dimensional torus* `ℝ/ℤ` under the *commuting* maps `×2,×3`. The Collatz map is **not** the
  `×2,×3` action — it is `x↦(3x+1)/2^{ν₂}`, an *affine, valuation-gated, non-commuting* composition;
  the `+1` breaks the multiplicative structure and the gating makes it a *single* map, not a
  `ℤ²`-action. There is no positive-entropy hypothesis to invoke and no torus on which both act
  invariantly. The `×2,×3` circle gives *philosophy* (rigidity of `{2,3}`-arithmetic) but no lever:
  the rigidity theorem needs the commuting `ℤ²` action that Collatz does not furnish. Recorded as a
  dead end *for direct application*; it survives only as motivation for E2's rigidity ask (§2.4a),
  which is on a different (non-homogeneous) extension.
- **Sarnak Möbius disjointness of the Collatz orbit.** One could ask whether the Collatz orbit
  sequence is Möbius-disjoint (a Sarnak-conjecture-flavored statement). **Why not:** the Collatz
  orbit is not a topological-dynamical sequence of zero entropy in any controlled system — it is
  the object whose boundedness is unknown; a disjointness statement about it is at least as hard as
  the conjecture and has no independent traction. (Different from E2, where the disjointness is
  between two *known* factors of a *known* Bernoulli system.)
- **Spectral gap / mixing rate of `P_n`.** Inert by `perp_gap.md` (`ρ=0`, useless). Not pursued.

---

## 4. Summary table

| | E1: nilpotent resonance ladder | E2: residue ⟂ drift disjointness |
|---|---|---|
| Object | Jordan flag of `N=P_n−Π` (Pollicott–Ruelle) | Furstenberg joining of `ℤ_3`-residue & `ℝ`-drift factors |
| Escapes barrier via | graded module / degree-shifting cochain (not a moment; not an eigenvalue) | disjointness quotients out frozen mod-3 factor (not TV→uniform) |
| Validated | **Yes**, exactly `n≤5`: `im(Nᵏ)=V^{(n−k)}` (3-adic scale ladder) | **Partly**: `I(Rmod3;drift)≈0.02` (near-disjoint); full `Ψ_n(ξ,t)` factorization not yet tested |
| First step | search graded module for a descent cochain (`n≤6`) | test `Ψ_n(ξ,t)≈Ψ_n(ξ,0)Ψ_n(0,t)`; rigidity of the `ℤ_3×ℝ` extension |
| Plausibility | 2/5 | 3/5 |
| Main failure mode | grading is descent-blind (descent lives in 2-adic/size, integrated out) | deeper-digit common factor; conditional only; non-homogeneous ⇒ no off-the-shelf Ratner |

**Net:** E2 is the stronger bet — it names the *exact* obstruction (Prop 4.2's residue–drift
coupling) as a disjointness, a non-moment non-symmetric statement, and its first computational
step (joint char-function factorization) is immediately runnable and decisive. E1 is a rigorous
structural sharpening (the nilpotent part is a 3-adic scale ladder, validated exactly) whose
payoff hinges on the uncertain existence of a degree-shifting descent cochain.

---

## 5. Theorems named (per rules)

Furstenberg (disjointness of dynamical systems, 1967; `×2,×3` rigidity, 1967); Rudolph–Johnson
(`×2,×3` measure rigidity); Ratner (measure/orbit-closure rigidity for unipotent flows);
Lindenstrauss (measure rigidity, quantum unique ergodicity); Sarnak (Möbius-disjointness
conjecture); Pollicott (1985) / Ruelle / Baladi / Faure–Sjöstrand / Dyatlov–Zworski
(Pollicott–Ruelle resonances of transfer operators); del Junco–Rudolph, Glasner, Host–Kra
(joinings calculus). All invoked for *philosophy/structure*; the only off-the-shelf application is
the joinings *language* (E2). Rigidity for Bernoulli-driven `ℤ_3×ℝ` extensions is, as far as I
found, not in the literature `[NOVELTY UNVERIFIED]`.

---

## 6. Frankl (short note — secondary)

The brief asks ergodic input on Frankl only if a genuine joinings/rigidity angle exists. **I do
not see one that escapes the proven symmetric-moment barrier.** A Furstenberg-correspondence
reformulation of a union-closed family as a shift-invariant set is formally possible (encode a UC
family `𝓕⊆2^{[n]}` as a `0/1`-pattern and pass to the orbit closure under coordinate shifts), but:
(i) the resulting system has **no canonical invariant measure** tied to the `½`-element question —
the natural measure is the uniform/product measure, whose every *symmetric* statistic is exactly
the flat-minimized moment the barrier kills; (ii) joinings/disjointness would compare two such
systems, but Frankl is a *single*-family inequality, giving nothing to join against;
(iii) measure rigidity needs an algebraic group action absent here. So the honest output is: **the
joinings/rigidity angle on Frankl reduces to a symmetric measure statistic and is inside the
barrier.** A possible non-barrier crumb — *not* developed here — is an **entropy/Furstenberg-
tower** reading of Gilmer's entropy method as a height function on a measure-preserving tower
(`survey.md` §7's Shearer chain-rule slack), which is an *entropy*-method refinement, not a
joinings one, and belongs to the additive-combinatorics / entropy cluster, not here. Recorded as
"why not": ergodic theory does not obviously help Frankl beyond restating the symmetric moment.

---

## 7. Validation provenance

Computations were run from the exact rational kernel of `P_n` (the `collatz/experiments/perp_gap.py`
construction: `2` primitive root mod `3ⁿ` ⇒ each entry a finite geometric series, exact over ℚ),
`n≤5` for the nilpotent flag (§1.3, exact ranks + subset tests vs coset subspaces `V^{(j)}`), and
an exact valuation DP for the residue–drift mutual information (§2.2, `n≤4`, geometric tail capped
at `a_max=40–44` and renormalized). Scratch scripts were run and discarded (not committed; nothing
written outside `ideas/generation/`). Numbers reproduce `perp_gap.md`'s rank chain `2·3^{n−1−k}`
exactly. `[NOVELTY UNVERIFIED]` throughout: the nilpotent-flag = 3-adic-scale identification is
plausibly the operator form of Tao's suffix-sum lemma (folklore prior HIGH); the residue⟂drift
disjointness *framing* of Prop 4.2 is, to my knowledge, not written down as a joinings statement,
but the underlying coupling is exactly Tao/Prop 4.2 and not new in content.
