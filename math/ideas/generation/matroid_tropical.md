# Matroid / Lorentzian / tropical directions for Frankl and Collatz

**Field cluster (PLAN.md #7):** matroid & oriented-matroid theory, tropical /
min-plus algebra, Lorentzian / log-concave polynomials (Brändén–Huh), and matroid
Hodge theory (Adiprasito–Huh–Katz, Huh–Wang).

**Status:** `[GENERATION — speculative directions, NOT proofs. NOVELTY UNVERIFIED.]`
Author line: Alex Ye (AI-assisted; AI not on author line per project rules).

**Scope discipline.** This note touches nothing outside `math/ideas/generation/`.
The four exploratory probes below were run read-only against the existing toolkit
(`frankl/experiments/{enumerate,uc_family,lattice}.py`) inside this note's
reasoning; the standalone reproducible script is
`math/ideas/generation/matroid_tropical_probe/probe.py` (created here, isolated).

**Bottom line up front.** I report **two honest negatives with teeth** and **one
live-but-thin positive direction**, plus a Collatz tropical object that is
**diagnostic, not a descent**:

- **Frankl–Lorentzian (NEGATIVE, sharp):** the natural Lorentzian/Hodge object —
  the **JI-filter overlap Gram form** — is a Gram matrix of 0/1 indicator
  vectors, hence **positive definite for all 29,723 families n≤5** (signature
  `(r,0,0)`), and stays PD even after subtracting the rank-1 first-moment part.
  It is **never Lorentzian** (never signature `(1, r−1, ·)`). So the Hodge-index
  inequality that powers AHK/Brändén–Huh **does not arise here**: there is no
  "exactly one positive eigenvalue" to exploit. This kills the most direct
  importation of matroid Hodge theory and explains *why* (Cauchy–Schwarz on a PD
  Gram form is exactly the symmetric second-moment the BARRIER already covers).
- **Frankl–matroid (NEGATIVE, structural):** a union-closed family is **not a
  matroid** and its lattice **is not geometric** in general; the natural rank
  grading (cardinality) is **not even log-concave** (19,638 / 29,723 families have
  a non-log-concave cardinality f-vector). So there is no ambient matroid whose
  basis-exchange could be invoked. The *correct* object is a **polymatroid /
  submodular rank from union-closure**, and a genuinely **non-symmetric** test on
  it (the M-convexity / discrete-Lorentzian exchange, §2.3) is the one direction
  here that is *not* obviously a disguised symmetric moment — this is the live
  lever, plausibility 2.
- **Collatz–tropical (DIAGNOSTIC negative):** the accelerated map is
  min/max-plus-affine on `x=log₂n`; its **max-plus eigenvalue = maximal cycle
  mean** over admissible parity words is **positive** (the all-odd word gives
  `λ=log₂3−1≈+0.585>0`). So the tropical/Lyapunov *worst-case* eigenvalue gives
  **no descent** — it reproduces exactly the (O2) "average not pointwise"
  obstruction already in `digit_lyapunov.md`. The only non-vacuous tropical object
  is the **min-plus eigenvalue restricted to realizable cycles**, which is the
  Collatz conjecture itself (a fixed-point statement), so tropical algebra
  **reformulates but does not crack** it.

---

## 1. The objects, precisely

### 1.1 Lorentzian / log-concave polynomials (Brändén–Huh) — what we would need

A homogeneous polynomial `p∈ℝ≥0[w₁,…,w_r]` of degree `d` is **Lorentzian** if its
supports are M-convex and every order-`(d−2)` directional derivative `∂_v p` is a
quadratic form of **Lorentzian signature** `(+,−,…,−)` (one positive eigenvalue).
Lorentzian polynomials are exactly the natural "continuous shadow" of matroid Hodge
theory (Adiprasito–Huh–Katz, *Hodge theory for combinatorial geometries*,
Ann. of Math. 2018; Brändén–Huh, *Lorentzian polynomials*, Ann. of Math. 2020).
Their headline consequence is **log-concavity of structured sequences**
(coefficients of `p`), via the **Hodge–Riemann relation in degree 1**: the
defining quadratic form has exactly one positive eigenvalue, and the
log-concavity inequality `a_k² ≥ a_{k−1}a_{k+1}` is its `2×2` minor.

**To use this for Frankl** we would need a degree-2 form `Q` attached to a UC
family whose **Hodge signature `(1, r−1)`** forces, via its one-positive-eigenvalue
structure, that some coordinate (= ground element) is heavy. The crucial point:
the Hodge-index inequality is **not** a symmetric average — it is an
**inertia/signature** statement, asymmetric in the privileged Perron direction
versus the rest. That asymmetry is exactly the BARRIER-escaping ingredient the
project wants. The question is whether the relevant `Q` actually has that
signature. **§2 shows it does not, for the obvious candidate.**

### 1.2 Tropical / min-plus (Collatz) — what we would need

The accelerated Collatz map `T(n)=n/2` (even), `(3n+1)/2` (odd) is **piecewise
affine**; on `x=log₂n` the two branches are the tropical-linear maps
`x↦x−1` and `x↦x+(log₂3−1)` (the `+1` is `O(2^{−x})`, negligible). A descent
proof in this language is a **max-plus / min-plus eigenvalue** statement: viewing
the parity dynamics as walks in a weighted automaton, the **maximal cycle mean**
(the max-plus eigenvalue `λ_max`) is the worst-case per-step drift, and `λ_max<0`
would give a Lyapunov descent (the tropical analogue of spectral radius `<1`).
This is **not** a probabilistic average over residues — it is a **worst-case
(min/max over cycles)** object, which is exactly why it escapes the
`π_n`-stationary obstruction (that obstruction is about the *invariant measure*;
the cycle-mean eigenvalue ignores measure entirely). **§3 shows `λ_max>0`**, so the
worst-case object fails, but it fails *for a different reason* than the moment
route — which is itself informative.

---

## 2. Frankl: matroid / polymatroid / Lorentzian structure

### 2.1 Why there is no ambient matroid (and the cardinality grading is not even log-concave)

A union-closed family `F` is a **join-semilattice under ∪**, not a matroid, and
`L=(F,∪)` is **not geometric** (not atomistic + semimodular) in general — e.g. M3
and the cone families are not geometric. So there is **no basis-exchange axiom** to
invoke directly: matroid Hodge theory needs a matroid, and we do not have one.

**Concrete check (probe 1, run on all 29,723 families n≤5).** The most naive
"rank grading" is the **cardinality f-vector** `W_k=#{A∈F:|A|=k}`. If `F` carried a
matroid-like Lorentzian structure, `(W_k)` would be log-concave. It is **not**:

| families (|F|≥2, n≤5) | cardinality f-vector log-concave | NOT log-concave |
|---|---|---|
| 29,723 | 10,085 | **19,638** |

(e.g. `F` with level-sequence `[1,1,1,3]` at abundance 0.667 fails LC, also from
internal zeros). **Conclusion:** the cardinality grading is the *wrong* grading and
there is no matroid behind it. Any Lorentzian attack must use a **different,
union-closure-aware** form — which sends us to the lattice/JI structure (§2.2).

### 2.2 The natural Lorentzian candidate: the JI-filter overlap Gram form — and why it is NOT Lorentzian (sharp negative)

The `join_irreducible_labelling.md` crown result reduced Frankl to a **lower bound
on the JI-filter overlap** `Σ_{j,k}|↑j∩↑k|`. The natural Lorentzian/Hodge object is
the **overlap Gram form**: for join-irreducibles `j₁,…,j_r`, set indicator vectors
`u_i=𝟙_{↑j_i}∈{0,1}^L` and

```
G_{ik} = ⟨u_i,u_k⟩/|L| = |↑j_i ∩ ↑j_k|/|L|     (diagonal = filter densities).
```

Frankl-via-Cauchy–Schwarz wants `max_x |Fib(x)| ≥ (Σ overlaps)/(Σ sizes)`. The
Lorentzian/Hodge hope was that `G` (or a centered version) has **signature
`(1,r−1)`** so that a *Hodge-index* inequality — not Cauchy–Schwarz — controls the
heavy fibre.

**Probe 2 (run on all 29,723 families n≤5).** Signature of `G`:

| signature `(pos,neg,zero)` | always |
|---|---|
| `(r, 0, 0)` (positive definite) | **29,723 / 29,723** |

`G` is **always positive definite** — because it is literally a Gram matrix of 0/1
indicator vectors, `G=U Uᵀ/|L|` with `U` full row-rank. **It is never Lorentzian.**

**Probe 3 (centered form).** Subtracting the rank-1 first-moment direction
(`f_i=|↑j_i|/|L|` in the same normalized units, so the correction is `f fᵀ` on the
normalized `G`, equivalently `ffᵀ/|L|²` on the integer counts), the centered form
`C = G − f fᵀ` is **still positive definite in
29,708 / 29,723 families** (only 15 degenerate to one zero eigenvalue; **none**
become negative semidefinite, **none** become Lorentzian). The Boolean cubes `B_k`
give `C` with signature `(k,0,0)` — fully positive, *no* privileged Hodge direction.

> **Negative Theorem 2.2 `[NOVELTY UNVERIFIED]`.** The JI-filter overlap Gram form
> of a union-closed family is a Gram matrix of indicator vectors, hence **positive
> definite**, never Lorentzian. Therefore the Adiprasito–Huh–Katz / Brändén–Huh
> Hodge-index inequality (signature `(1,r−1)`, the engine of all their
> log-concavity theorems) **does not apply to the Frankl overlap form**. The only
> inequality a PD Gram form supplies is **Cauchy–Schwarz / the power-mean bound**
> — which is exactly the *symmetric second moment* `M₂=Σfreq²` that the project's
> BARRIER theorem already proved is flat-minimized by the cube at ½. So the direct
> Lorentzian importation **collapses onto the known barrier**, with no new
> ingredient.

This is a *useful* negative: it tells future work that **PD Gram structure ⇒
Cauchy–Schwarz ⇒ symmetric moment ⇒ barrier**, so any Lorentzian attack must build
a form that is **genuinely indefinite** (Lorentzian), which the indicator-vector
overlap form structurally cannot be.

### 2.3 The one live lever: discrete M-convexity / polymatroid exchange (non-symmetric)

Where Lorentzian theory could still bite — *not* via signature of an overlap form,
but via **M-convexity (discrete Lorentzian) of the support**:

- Union-closure gives a **submodular-type structure**: the map
  `μ(S) = |{A∈F : A⊇S}|` (the "filter-size / upper-shadow" function) on `S⊆[n]`,
  or its complement `A∈F ↦ |A|`, can be tested for **submodularity**; a submodular
  `μ` defines a **polymatroid**, and the **generating polynomial of the bases /
  the multivariate independence polynomial** of a polymatroid **is Lorentzian**
  (Brändén–Huh Thm; also Murota's M-convexity). The associated log-concavity is a
  **non-symmetric** statement: it is sensitive to *which* coordinate you
  differentiate (= which ground element you condition on), unlike a symmetric
  moment.
- **The non-moment hook (why this could escape the barrier).** The BARRIER kills
  *symmetric* convex moments. An **M-convex exchange inequality** — "for the
  support of the family's multivariate generating polynomial, given members
  differing in their content at elements `x,y`, you can exchange `x↔y` staying in
  the family" — is **asymmetric**: it privileges the pair `(x,y)` and the *direction*
  of exchange. If union-closure forces an exchange asymmetry biased toward a fixed
  heavy element, that is precisely a *non-symmetric structural* ingredient.

> **Candidate Object 2.3 `[NOVELTY UNVERIFIED, plausibility 2]`.** Define the
> **content polymatroid** of `F` via `μ(S)=|⋃{A∈F:A⊆ comp}|`-type rank (the exact
> submodular surrogate is a design choice — see failure modes). Test whether the
> **multivariate generating polynomial** `g_F(w)=Σ_{A∈F} ∏_{x∈A} w_x` (or a
> normalized version) is **Lorentzian / M-convex-supported**. If it is, the
> degree-1 Hodge–Riemann relation yields, for each *ordered* pair `(x,y)`, an
> inequality on `∂_x∂_y g_F` vs `∂_x²g_F · ∂_y²g_F` that is **asymmetric** and
> might be lower-bounded by union-closure in a direction that forces one heavy
> `∂_x`. **This is the only direction in this note that is plausibly non-moment**:
> it is an inertia/exchange property of a *multivariate* polynomial, not an average
> of the frequency vector.

**Honest caveat (probe-grade).** I did **not** verify `g_F` is Lorentzian; in fact
the support of `g_F` is the family `F` itself viewed in `{0,1}^n`, and **M-convexity
of a 0/1 support = the support is the set of bases of a matroid**, which §2.1 says
is generally **false** for UC families. So `g_F` is **probably not** Lorentzian
either, and the live lever is really: *find the right submodular truncation/rank so
that some derived polynomial IS Lorentzian while still seeing abundance.* That is
genuinely open and genuinely hard — hence plausibility 2, not higher.

---

## 3. Collatz: the tropical / min-plus eigenvalue

### 3.1 The object

On `x=log₂n` the accelerated map is the **max-plus (tropical) piecewise-linear**
system with two affine branches `x↦x−1` (even) and `x↦x+(log₂3−1)` (odd). Reading
the parity sequence as a path in a 1-state automaton with two edge weights
`{−1, log₂3−1}`, the **max-plus eigenvalue** (Cuninghame-Green / Baccelli–Cohen
theory) is the **maximal cycle mean**

```
λ_max = max over admissible parity words W of  (1/|W|) Σ_{steps} weight.
```

`λ_max<0` would be a **tropical Lyapunov descent** — and crucially it is a
**worst-case (max over cycles)** object, NOT a probabilistic average over `(ℤ/3ⁿ)ˣ`.
So it sidesteps the *exact-stationary-`π_n`* obstruction by construction: the
cycle-mean eigenvalue does not reference any invariant measure.

### 3.2 Probe 4 (the computation) — and the verdict

The weights are `w_even=−1`, `w_odd=log₂3−1≈+0.585`. The drift of a word with
fraction `p` odd is `λ(p)=p(log₂3−1)+(1−p)(−1)=p·log₂3−1`. Hence:

| `p` (fraction odd) | tropical drift `λ(p)` |
|---|---|
| 1.0 (all-odd) | **+0.585** |
| 0.631 = 1/log₂3 | **0.000** (critical) |
| 0.5 (Tao/heuristic typical) | −0.208 |

The **critical fraction is `p* = 1/log₂3 ≈ 0.6309`**; above it, drift is positive.
Short all-odd (or odd-heavy) admissible words exist (Mersenne-like climbs,
`n=2^k−1` rises for `k` steps), so

> **Negative Theorem 3.2.** The max-plus eigenvalue of the accelerated Collatz
> tropical system over *finite admissible parity words* is **`λ_max = log₂3−1 >
> 0`** (attained by all-odd runs). The worst-case tropical Lyapunov object gives
> **no descent**; it reproduces exactly the `digit_lyapunov.md` (O2) obstruction
> ("magnitude grows pointwise on every odd step; descent is only an average").

### 3.3 Why this is not a dead loss (the diagnostic content)

The tropical computation **relocates** the difficulty cleanly and *differently*
from the `π_n` story:
- The **min-plus** eigenvalue over the *realizable* cycle set is `< 0` **iff**
  there is no non-trivial Collatz cycle and every orbit descends — i.e. the
  min-plus eigenvalue statement is **equivalent** to (the cycle half of) the
  conjecture. So tropical algebra is a faithful *reformulation*, not a tool.
- The gap between `λ_max=+0.585` (all parity words) and the conjectured `λ<0`
  (only **realizable** words) is **exactly the arithmetic constraint** "which
  parity words are achievable as Syracuse orbits" — the `mod 2^k` admissibility
  that the function-field analog (`function_field.md`) shows is **automatically
  benign over `𝔽₂[T]`** (degree can't rise) but **archimedean-vs-2-adic-decoupled
  over ℤ**. The tropical eigenvalue thus **names the missing ingredient as a
  realizability constraint on parity words**, a min-plus *automaton* question:
  *which infinite words over `{even,odd}` are Syracuse-admissible, and is their
  max cycle-mean `<0`?* That is the (very hard) tropical-automaton reformulation,
  and it is **non-moment** (worst-case over an admissible language, no measure).

> **Candidate Object 3.3 `[NOVELTY UNVERIFIED, plausibility 1–2]`.** Build the
> **Syracuse parity automaton** `𝒜_k` on states `ℤ/2^k` (transition = one
> accelerated step, edge weight `−1` or `log₂3−1` by parity), and compute the
> **max-plus eigenvalue (maximal cycle mean) of `𝒜_k`** as `k→∞`. If `λ_max(𝒜_k)`
> were `<0` for some finite `k`, the conjecture's no-cycle/descent half would
> follow by a finite tropical certificate. **Prediction (and failure mode):** it
> is `≥0` for every `k` (the all-odd local climbs survive every finite mod-`2^k`
> truncation), mirroring `λ₂≡1` in the transfer operator — i.e. the tropical
> eigenvalue is **permanently non-negative at every finite level**, the exact
> tropical shadow of the `π_n` rigidity. Worth computing once to *confirm* the
> obstruction is tropical-level-uniform (a clean negative), low chance of descent.

---

## 4. Validations (small, concrete, reproducible)

All four probes are in `matroid_tropical_probe/probe.py` (isolated dir created by
this note). They re-use only `enumerate.py`, `uc_family.py`, `lattice.py` (Frankl)
and a 6-line standalone computation (Collatz). Headline numbers:

1. **Cardinality f-vector log-concavity:** 10,085 LC / 19,638 NOT-LC out of 29,723
   (n≤5). ⇒ no ambient matroid grading.
2. **JI-overlap Gram signature:** `(r,0,0)` for **all** 29,723 ⇒ always PD, never
   Lorentzian.
3. **Centered overlap form `C=G−ffᵀ` (normalized units):** PD in 29,708, one-zero in 15, **0**
   indefinite ⇒ no Hodge `(1,r−1)` signature anywhere; cubes give full-positive
   `(k,0,0)`.
4. **Tropical max-plus eigenvalue:** `λ_max=log₂3−1≈+0.585>0`; critical
   `p*=1/log₂3≈0.6309`; `λ(½)=−0.208`.

Each is a deterministic exhaustive (Frankl) or closed-form (Collatz) check —
re-derivable by hand for small cases (cube `B_3`: `G` is the `3×3` matrix with
diagonal `4/8=½`, off-diagonal `2/8=¼`, eigenvalues `{1, ¼, ¼}` — all positive,
confirming PD/non-Lorentzian by hand).

---

## 5. Plausibility, novelty, failure modes

| Direction | Plausibility (1–5) | Verdict |
|---|---|---|
| **Frankl: Lorentzian overlap form (§2.2)** | **1** | **Refuted** — PD Gram, never Lorentzian; collapses to the known symmetric-moment barrier. A *clean publishable "why-not"*: matroid Hodge theory cannot attach to the overlap form. |
| **Frankl: polymatroid M-convexity / generating-polynomial exchange (§2.3)** | **2** | **Live but thin.** The non-symmetric exchange inequality is the only genuinely non-moment object here, but the obvious generating polynomial `g_F` is M-convex iff `F` is a matroid (generally false). Needs a *new* submodular truncation; open. |
| **Collatz: tropical max-plus eigenvalue (§3)** | **1–2** | **Diagnostic.** `λ_max>0` ⇒ worst-case tropical descent fails (reproduces O2). The min-plus-over-realizable-words version is *equivalent* to the conjecture (reformulation, not tool). Worth one computation of `λ_max(𝒜_k)` to confirm tropical-level-uniform non-negativity. |

**Why non-moment (the argument).** A symmetric convex moment is a function of the
*multiset* of frequencies, invariant under relabeling. The two objects here that
are *not* of that form: (a) a **Hodge signature / inertia** is a function of an
asymmetric quadratic form privileging one eigendirection — but §2.2 shows the
relevant form is PD, so no signature lever exists, and the surviving inequality
(Cauchy–Schwarz) *is* a symmetric moment ⇒ barrier. (b) an **M-convex exchange**
inequality is asymmetric in the ordered pair `(x,y)` and the exchange direction —
this is the genuinely non-symmetric candidate (§2.3), but it lacks a verified
Lorentzian carrier. (c) a **max-plus cycle-mean eigenvalue** is a worst-case (not
average) over an admissible language, hence non-moment by construction — but it is
positive (§3), so it gives a reformulation not a descent.

**Non-flat on the cube?** §2.2 is explicitly **flat on the cube** (cube ⇒ `G`
diagonal-dominant PD, abundance exactly ½, Cauchy–Schwarz tight) — that is *why* it
fails (it inherits the barrier's cube-flatness). §2.3's exchange inequality *could*
be non-flat on the cube (the cube is distributive, so its content polymatroid is
the free/Boolean one, where M-convexity is non-degenerate) — establishing
non-flatness there is the **first concrete test** if §2.3 is pursued. The tropical
object §3 has no cube analogue (different problem).

**Failure modes.**
- §2.2: none — it is a proved structural fact (Gram ⇒ PD). The risk is only that
  someone reads "Lorentzian" optimistically; the probe refutes it exhaustively.
- §2.3: the generating polynomial is **not** Lorentzian (support not M-convex);
  every "natural" submodular rank we'd write down is likely either (i) the
  cardinality function (gives the non-LC f-vector of §2.1) or (ii) a symmetric
  moment in disguise. The honest risk is **>50% this is a dead end** like every
  other lattice-invariant route (cone obstruction, `lattice_attack.md` §4).
- §3: `λ_max(𝒜_k)≥0` at every finite `k` is near-certain (all-odd local climbs);
  the equivalent min-plus statement is the conjecture, so no finite certificate is
  expected. Failure mode = "true but useless," same shape as `perp_gap.md`.

**`[NOVELTY UNVERIFIED]`** on all framings (arXiv 403 this session). Prior art to
check next network-enabled pass: (i) Brändén–Huh / Murota M-convexity applied to
set systems / antichains; (ii) any "Lorentzian polynomial + union-closed" or
"polymatroid + Frankl" literature (suspect none, but unverified); (iii) tropical /
max-plus formulations of Collatz (Conway-FRACTRAN-adjacent; the max-plus cycle-mean
framing is likely folklore in the dynamics community).

---

## 6. Honest one-paragraph summary for the reviewer

The matroid/Lorentzian field gives a **sharp negative** for Frankl: the only
natural Hodge object (the JI-filter overlap form) is a positive-definite Gram
matrix, never Lorentzian, so Adiprasito–Huh–Katz / Brändén–Huh signature
inequalities cannot attach, and what survives is Cauchy–Schwarz = the symmetric
second moment the BARRIER already blocks (verified PD on all 29,723 families; cube
flat). The *only* non-moment escape the field offers is a **polymatroid M-convex
exchange** inequality (§2.3) — genuinely asymmetric — but it lacks a Lorentzian
carrier because UC families are not matroids (cardinality f-vector non-log-concave
in 2/3 of families), so it is a thin, open lever (plausibility 2). For Collatz, the
tropical **max-plus cycle-mean eigenvalue is `+log₂3−1>0`** (worst-case descent
fails, reproducing the average-not-pointwise obstruction); the min-plus version
over *realizable* parity words is equivalent to the conjecture — a faithful
non-moment **reformulation**, not a tool. Net: the field **delimits** both problems
crisply (a publishable "why Hodge theory can't attach to Frankl") and surfaces one
narrow live Frankl lever (M-convex exchange) worth a single non-flatness probe on
the cube.
