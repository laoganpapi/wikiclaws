# Probability beyond moments: couplings, optimal transport, martingale embeddings, Stein

**Track:** non-moment / non-symmetric attack candidates for Frankl and Collatz.
**Field cluster #8** (PLAN.md §20): probability beyond moments — couplings & monotone
coupling, optimal transport / Wasserstein contraction, martingale (Skorokhod) embeddings,
Stein's method / exchangeable pairs, stochastic domination, entropy-free FKG/Holley.
**Author:** Alex Ye (AI-assisted; AI not on author line per project rules).
**Date:** 2026-06-03.
**Status:** `[NOVELTY UNVERIFIED]` throughout. **Directions, not proofs.** No constant > 1/2
(Frankl) or natural-density result (Collatz) is claimed. Self-assessed plausibilities in §F.

> **One-sentence thesis.** A coupling / transport map is *not* a symmetric convex moment
> of the frequency (Frankl) or a spectral/averaging statistic of `P_n` (Collatz): it carries
> the *joint* law of two coordinates / two trajectories, and the barriers this project proved
> are all about *marginal averaged* quantities. So a coupling is a structurally legitimate place
> to look for slack. The honest finding below is that the two most natural couplings **degenerate
> on the same extremizers** (Boolean cube / `π_n`) — but in a *different way* than moments do, and
> §A.4 / §B.4 isolate exactly the non-degenerate residue worth a computational probe.

Cross-references: `frankl/theory/join_irreducible_labelling.md` (the fibre=filter dictionary,
reconstruction identity (R), cube-uniqueness H5, the JI-overlap lever); `frankl/theory/lp_duality.md`
(40.5% anti-correlation killing FKG); `frankl/theory/second_moment.md`; `collatz/theory/transfer_operator.md`
(P_n, π_n = Syracuse RV, mod-3 block); `collatz/theory/natural_density_obstruction.md` (TV ≥ 1/6).

---

## PART A — FRANKL

### A.0 Why moments fail and why a coupling is a different object

The BARRIER THEOREM (PROGRESS.md §193): every symmetric convex moment
`Φ(freq) = Σ_x g(freq(x)/|F|)` of the frequency vector is flat-minimized by the Boolean cube
`2^[n]` at exactly 1/2. The cube is the *unique* extremal lattice (H5, 13,734 iso classes n≤5).
A moment is a function of the **marginals** `freq(x)`. A coupling is a function of a **joint law**
`P(x∈A, y∈A)` — it lives one tensor level up, on `F×F` or `[n]×[n]`, and the projection to marginals
deliberately discards it. *This is precisely the "coupling the invariant methods throw away"*
that `join_irreducible_labelling.md` (R) identifies. So the question is not "is there slack"
(there is, structurally) but "does a coupling **certify** ≥ 1/2 without re-collapsing to a marginal."

**FKG is dead here** (`lp_duality.md`: uniform-on-`F` is not log-supermodular; 40.5% of element
pairs are *anti-correlated*). So I must propose a coupling structure that does **not** need positive
association. Two candidates: (A.1) a **monotone/Strassen coupling driven by the join operation**
`A ↦ A∪B`; (A.2) a **Stein / exchangeable-pairs** identity on the join-action that needs no FKG.

### A.1 The join-coupling (Strassen / stochastic domination) — and why it half-works

**Object.** Let `μ` = uniform on `F`. The union-closure axiom gives a canonical *monotone Markov
kernel* on `F`: pick `B ∼ μ` and map `A ↦ A∪B`. Call this kernel `J` (the "join-with-a-random-member"
operator). `J` is **monotone** (`A⊆A'` ⟹ `A∪B ⊆ A'∪B` pointwise) and `μ`-**stationary is FALSE** in
general, but `J` pushes mass *up* the lattice: `JA ⊇ A` always. By Strassen's theorem the relation
"`Jμ` stochastically dominates `μ`" holds iff there is a monotone coupling — and here it holds *by
construction* (the identity map `A↦A∪B` IS the coupling, with `A∪B ⊇ A`).

**The lever.** For a fixed element `x`, abundance `= P_μ(x∈A) = freq(x)/|F|`. Apply `J`:
`P_{Jμ}(x ∈ A∪B) = P(x∈A) + P(x∉A)·P(x∈B | x∉A) ≥ P_μ(x∈A)`, with the gain term
`Δ_x := P(x∉A, x∈B)`. Summing identities like this over `x` and using that `J` is a *contraction
toward the top* `T=⋃F` is the entropy-free analogue of Gilmer's `A∪B` argument — **but as a
stochastic-domination statement, not an entropy inequality.** The point: Gilmer bounds `H(A∪B)`
(a moment of the join law); here we instead track the **monotone coupling** `(A, A∪B)` and ask for
an element whose "up-flux" `Δ_x` is large.

**Why it half-works (honest).** The fixed point of `J` is the top filter; iterating `J` sends every
mass to `T`, so `J^k μ → δ_T` and *every* element of `T` becomes abundant in the limit — but that
limit is the trivial statement "T contains every element." The single step is the informative one.
On the **cube** `2^[n]`: `Δ_x = P(x∉A)P(x∈B) = (1/2)(1/2) = 1/4` for every `x` (independence), and
`freq(x)/|F| = 1/2` already — so the join-coupling gain is **flat across x and reproduces 1/2 with
zero margin**, exactly like every moment. The coupling sees the cube the same way. *So A.1 alone does
not escape — it degenerates on the cube too.*

### A.2 The fix: a NON-symmetric, exchangeable-pairs (Stein) identity on the join-action

The escape is to make the coupling **asymmetric in which element is heavy** — the barrier theorem
says the missing ingredient must be sensitive to *which* `x` is heavy, not an average. Stein's method
via **exchangeable pairs** is built for exactly this: it controls a target functional through a *single*
antisymmetric kernel, never through a symmetric moment.

**Object (exchangeable pair on `F`).** Define an exchangeable pair `(A, A')` by: draw `A∼μ`, draw
`B∼μ` independent, set `A' = A∪B` *with probability 1/2* and `A' = A∩'B` with probability 1/2, where
`A∩'B := the largest member of F contained in A∩B` (the *meet in the lattice* `L=(F,∪)`,
which exists since `F` is a lattice — `lattice.py:meet_in_L`). The pair `(A,A')` is **not** exchangeable
in general (union-closure breaks the `∪`/`∩` symmetry — this is V2's obstruction, `H(A∩B)≤H(A)` FALSE),
and *that asymmetry is the signal*. The Stein discrepancy
`D(x) := E[ (1_{x∈A'} − 1_{x∈A}) · f(A) ]` for the linear test `f(A)=1_{x∈A}` measures the
**net up-flux minus down-flux of `x` under the symmetrized join/meet action**.

**The non-symmetric certificate (proposed).** Union-closure makes the join branch *over-represented*
relative to the meet branch (every join stays in `F`; not every meet is `T`-ward). The claim to test:
**`Σ_x w(x) D(x) > 0` for a non-uniform weight `w` concentrated on a join-heavy element, and the
witness element of the max is ≥ 1/2-abundant.** This is genuinely outside the moment barrier because
`D(x)` is *antisymmetric* (a difference of two coupled indicators), and the weight `w` is *generator-
asymmetric* (it picks the element, it is not `Σ_x g(freq_x)`). It is the probabilistic incarnation of
the `join_irreducible_labelling.md` lever: `Fib(x) = ⋃_{j: x∈j} ↑j`, so the heavy element is the one
whose JI-filters' *join-flux* dominates.

### A.3 Why it (provably) cannot be a disguised moment

A symmetric convex moment is a function of `{freq(x)}` invariant under relabelling `[n]`. The objects
above are **not** of that form:
- `Δ_x = P(x∉A, x∈B)` is a *second-order* (pair) correlation `= freq(x)/|F| − Σ_A 1_{x∈A}·(|↑A∩Fib(x)|)/|F|²`
  — it depends on the joint `(A,B)` law, i.e. on `Σ_{x,y}` overlap data, the `second_moment.md` /
  JI-overlap object, **not** recoverable from the marginal vector. (Concretely: two families with the
  same `freq` vector but different join-tables give different `Δ_x` — testable, see A.4.)
- The Stein weight `w` breaks `[n]`-symmetry by design; the barrier theorem only forbids
  *symmetric* convex moments.
So a positive answer to A.2 would **not** be flat-minimized by the cube: on the cube the up-flux and
down-flux *cancel* (`D(x)≡0` by `∪/∩` symmetry of `2^[n]`, which IS distributive), so the cube sits at
the *boundary* `D=0`, while every non-distributive lattice has `D(x)>0` for some `x` (the meet branch
loses mass to `F`). **That is the desired non-flatness: the cube is the zero of `D`, not the minimum of
a moment.** (Consistency with H5: cube = unique tight case, here = unique `D≡0` case.)

### A.4 CONCRETE FIRST STEP (computable now on n≤5)

Add `frankl/experiments/join_coupling_stein.py` using the existing toolkit
(`uc_family.is_union_closed`, `frequencies`, `lattice.meet_in_L`, `enumerate.all_uc_families`):

1. **Two-families-same-freq probe (kills the "disguised moment" worry empirically).** Search the
   29,723 families n≤5 for pairs with identical sorted `freq` vector but different `Δ_x` profile
   `{P(x∉A,x∈B)}_x`. If found ⟹ `Δ_x` is provably not a function of `freq` ⟹ outside the moment class.
   *(Expected: easy to find; M3 vs a chain of the same `|F|`.)*
2. **Stein discrepancy sweep.** For every family compute `D(x)` (the join−meet up-flux) and the weighted
   max `max_x D(x)` and the abundance of `argmax_x D(x)`. **Test the conjecture: the element maximizing
   `D(x)` is ≥ 1/2-abundant** (or: `Σ_x relu(D(x))` lower-bounds `abundance − 1/2`). Report violations.
3. **Cube boundary check.** Verify `D(x) ≡ 0` on all five Boolean cubes `B_1..B_5` (predicted by A.3),
   and `D(x) > 0` somewhere on every non-distributive family — i.e. the certificate is *non-flat exactly
   off the cube*. This is the decisive escape-the-barrier diagnostic.

**Small validation (hand-checkable).** M3 = `{∅,{0,1},{0,2},{1,2},{0,1,2}}`, `|F|=5`, each element
abundance `3/5` (`join_irreducible_labelling.md` §2). Meet in `L`: `{0,1}∧{0,2}=∅` (their set-meet `{0}∉F`,
largest `F`-member below is `∅`). So the meet branch from `A={0,1},B={0,2}` lands at `∅` — element `0` is
*lost*; the join branch `A∪B={0,1,2}` *keeps* `0`. Net up-flux `D(0)>0`. Predicted argmax is abundant
(3/5 ≥ 1/2). ✓ direction. On `B_2={∅,{0},{1},{0,1}}`: distributive, `∪`/`∩` both close in `F`,
`D(x)=0` ✓ boundary.

### A.5 Failure mode (the most likely one)

Same as every method in this project: the certificate degenerates on the cube. The *novelty* here is
that it degenerates as a **zero of an antisymmetric kernel** (a Stein fixed point) rather than a minimum
of a moment — so step A.4.3 might show `Σ relu(D(x))` is a *valid lower bound on slack `ε(L)=abundance−1/2`*
that is positive off the cube. If instead `D(x)` is anti-correlated with abundance (large `D` ⟺ already-
heavy, the V1 pattern), the lever collapses. **This is the single decisive small computation.**

---

## PART B — COLLATZ

### B.0 Why the spectral/moment route is inert and what transport changes

`transfer_operator.md` + `perp_gap.md`: `P_n` on `(ℤ/3ⁿ)ˣ` has spectrum `{1, 0,...,0}`
(`P_n−Π` nilpotent), so spectral-gap / mixing-rate (an `ℓ²`-moment) statements are *inert* — there is
no rate defect, the obstruction is the **exact non-uniform stationary `π_n`** (= Syracuse RV) and its
permanent mod-3 marginal `(0,1/3,2/3)` (TV ≥ 1/6 vs uniform-on-units, `natural_density_obstruction.md`).
The barrier is that every prior route *averages toward the wrong reference `U`*.

**The transport reframing.** Optimal transport / Wasserstein contraction is **not** an averaging-to-`U`
statement: it measures distance in a *metric on the state space* one is free to choose. The brief's
key instruction: use a **Wasserstein metric adapted to `π_n`, not `ℓ²`/TV**. Because TV is metric-blind
(it counts only mass moved, not how far), TV ≥ 1/6 is a TV obstruction *that a Wasserstein contraction
need not see at all* — if the mod-3 imbalance is "cheap" in the chosen ground metric, `W` can still
contract while TV stays ≥ 1/6.

### B.1 The 3-adic Wasserstein object

**Ground metric.** Equip `(ℤ/3ⁿ)ˣ` with the **3-adic metric** `d(x,y)=3^{−v_3(x−y)}` (ultrametric),
NOT the discrete/Hamming metric that underlies TV. Let `W = W_1^{(3-adic)}` be the order-1 Kantorovich–
Wasserstein distance on probability measures over `(ℤ/3ⁿ)ˣ` with this cost.

**Why this metric.** The whole obstruction is *mod-3 graded*: `π_n`'s defect lives in the coarsest 3-adic
layer (the mod-3 marginal), and the projective filtration `V^{(1)}⊂...⊂V^{(n)}` of `transfer_operator.md`
§3.1 is *exactly the 3-adic ball filtration*. In the 3-adic metric, the mod-3 imbalance is a *bounded-
distance* perturbation (it moves mass within the top-level balls, cost `≤ 3^0=1`), whereas in TV it is a
permanent 1/6 floor. So `W^{(3-adic)}(π_n, U)` and `TV(π_n,U)` measure genuinely different things —
**the transport object is not the moment/TV object.**

### B.2 Wasserstein contraction of `P_n` (the proposed contraction)

**Claim to test (Wasserstein contraction).** There is `ρ<1`, uniform in `n`, with
`W(μ P_n, π_n) ≤ ρ · W(μ, π_n)` for all `μ`, in the **3-adic** `W`. Equivalently `P_n` is a strict
3-adic contraction toward its stationary `π_n`. This is a *path-coupling* (Bubley–Dyer) statement:
couple two copies `X, Y` of the Syracuse step sharing the **same valuation `a∼Geom(2)`**
(`x ↦ 2^{−a}(3x+1)`); then `3X+1−(3Y+1) = 3(X−Y)`, so `2^{−a}(3X+1) − 2^{−a}(3Y+1) = 3·2^{−a}(X−Y)`,
i.e. **`v_3(X'−Y') = v_3(X−Y) + 1` deterministically under the synchronous coupling.** So
`d(X',Y') = 3^{−1} d(X,Y)`: **the synchronous-valuation coupling contracts the 3-adic distance by exactly
1/3 every step.** This is a clean, *exact* one-step contraction — and it is NOT a spectral statement
(`P_n` is nilpotent on `V^⊥`, yet here we get geometric 3-adic contraction directly from the `×3` in
`3x+1`).

### B.3 Why this escapes the inert-spectrum / mod-3 barrier

- **Not a moment / not spectral.** The contraction factor 1/3 comes from `v_3(3(x−y))=v_3(x−y)+1`,
  a *coupling* identity on the joint `(X,Y)` law, not from any eigenvalue of `P_n` (which are `{1,0}`).
  Wasserstein contraction with a nilpotent generator is perfectly possible and is exactly what the
  `P_n−Π` nilpotency *predicts*: nilpotent of index `n` ⟺ the 3-adic distance is killed after `n` steps
  (`3^{−n}` = full collapse mod `3ⁿ`). **The nilpotency IS the contraction, read in the right metric.**
  This *reinterprets* the "inert spectrum" obstruction as a *feature*.
- **Not blocked by TV ≥ 1/6.** The mod-3 imbalance is a top-ball (cost-1) phenomenon; a 3-adic
  contraction toward `π_n` says nothing about `π_n` being uniform — it contracts toward the *correct*
  non-uniform target, which is what `transfer_operator.md` §6 argued is the right reference. The point is
  not to reach `U` but to get **quantitative convergence to `π_n` in a metric, with a rate the natural-
  density transport can use** — converting Tao's log-density transport (which needs stationarity of the
  sampling measure) into a *contraction estimate* on the joint `(residue, drift)` law.

### B.4 The real target: a `(residue, drift)` Wasserstein contraction (where the gap lives)

The genuine open content (`natural_density_obstruction.md` §2-L2) is the **joint** law of
`(residue mod 3ⁿ, drift D_n = (Σa_j)log2 − n log3)`. Natural density (vs log) needs the Radon–Nikodym
factor `e^{−D_n}` controlled *jointly* with the residue. Proposal: a Wasserstein contraction on the
**product metric** `d((x,u),(y,v)) = 3^{−v_3(x−y)} + λ|u−v|` (3-adic on residue × Euclidean on log-drift),
with `λ` tuned to the descent-balance tilt `s*`. The synchronous coupling contracts the residue by 1/3
(B.2); the drift coordinate is a *random walk* `u ↦ u − D_n`, which under the `s*`-tilt is **drift-neutral**
(`E_{s*}[D_n]=0`) — a *martingale* in `u`. So the joint object is "3-adic contraction × martingale drift,"
a **Skorokhod-embedding / martingale-coupling** target rather than a moment.

**Why this is the non-moment escape.** The scalar-Esscher route died because it sought TV-equidistribution
of the *residue marginal* to `U` (§B.0). A martingale embedding of the drift coordinate *coupled to* the
3-adic-contracting residue never forms the residue marginal alone — it keeps the joint, exactly the object
L2 says the natural-density gap lives in. The mod-3 obstruction (a residue-marginal fact) is invisible to
the *joint* contraction if the drift martingale carries the equidistribution. **This is the one route
`natural_density_obstruction.md` §5 lists as open ("act on the joint (residue, drift), not the marginal").**

### B.5 CONCRETE FIRST STEP (computable now on small n)

Extend `collatz/experiments/transfer_operator.py`:

1. **Verify the 1/3 contraction (B.2) exactly.** For `n=1..8`, build the synchronous-valuation coupling
   and confirm `v_3(X'−Y') = v_3(X−Y)+1` for all unit pairs and all `a` (rational arithmetic; this is a
   *theorem* to confirm, not a numeric). Then compute `W_1^{(3-adic)}(δ_x P_n, π_n)` for a few `x` and the
   contraction ratio `W(μP_n,π_n)/W(μ,π_n)`; **check it is ≤ 1/3 + o(1) uniformly in n** (the prediction).
2. **`W` vs TV divergence (decisive non-moment diagnostic).** Tabulate `W_1^{(3-adic)}(π_n, U)` next to
   `TV(π_n,U)` (already known `→0.4`). **Prediction: `W^{(3-adic)}(π_n,U)` stays bounded / small while TV
   stays ≥ 1/6** — confirming the two metrics see the obstruction differently (the whole point). If `W`
   *also* floors away from 0, the metric does not help and B.1–B.3 collapse to TV.
3. **Joint contraction probe (B.4).** On the product space `(residue, discretized drift)`, estimate the
   `s*`-tilted joint-Wasserstein contraction ratio for `n=1..6` by Sinkhorn/LP on the small transport
   problem. **Test whether the joint contracts (`<1`) even though the residue marginal does not
   equidistribute** — the crux that would distinguish this from the dead scalar-Esscher route.

**Small validation (hand-checkable, n=1).** `U_1=(ℤ/3)ˣ={1,2}`. Step: `x↦2^{−a}(3x+1)`. For `x=1`:
`3·1+1=4≡1 mod3`, times `2^{−a}≡2^a`: residue `2^a mod3 ∈{2,1,2,1,...}`. For `x=2`: `3·2+1=7≡1 mod3`,
same → residue depends only on `a`, *not on x*. So after one step `X',Y'` are *equal* whenever the
coupled `a` agrees: `d(X',Y')=0 = 3^{−∞}` ✓ (contraction past 1/3 at n=1, since mod 3 is the whole
space — consistent with nilpotency index `n=1`). `π_1=(1/3,2/3)`, `W^{(3-adic)}(π_1,U)≤3^0·TV=1/6`
bounded ✓.

### B.6 Failure modes

1. **`W^{(3-adic)}` floors too** (B.5.2 fails): if the 3-adic metric still puts the mod-3 imbalance at
   bounded-below cost, transport buys nothing over TV. *Most likely failure;* the n=1 check is the canary.
2. **Contraction to `π_n` is "true but useless"** — same trap as `perp_gap.md`: you contract beautifully
   to the *wrong* target and the natural-density question is entirely in `π_n`'s shape, untouched. The
   joint `(residue,drift)` probe (B.4/B.5.3) is the only version that dodges this, and it is the riskiest.
3. **The drift martingale and the residue contraction may be incompatible under one tilt** — exactly the
   `s_c≈−0.4` phase transition (`natural_density_obstruction.md` §4): drift-neutrality wants `s*=+0.438`,
   residue-spreading wants `s<−0.45`. A *single* scalar coupling cannot do both; a genuinely non-scalar
   (xi-dependent, operator) coupling is needed, which is unconstrained but also unconstructed.

---

## C — Eldan stochastic localization (a long-shot for Frankl, noted for completeness)

Eldan's stochastic localization builds a martingale `μ_t` of measures with `μ_0=μ`, `μ_∞=` point masses,
tilting along a Brownian control. For Frankl: run localization on uniform-on-`F`, tilting *toward the
top filter* using the join generator `J` (A.1) as the drift. The terminal measures are point masses on
members of `F`; the abundance of `x` is `E_t[μ_t(x∈·)]`, a *martingale*, so by optional stopping
`abundance(x) = E[1_{x∈A_∞}]` for the localized endpoint — and the localization path can be steered to
concentrate on `T` (which contains every element). This is the **martingale-embedding** view of A.1; its
escape value is identical to A.2 (the drift must be join-asymmetric) and its failure mode identical
(cube = flat path). Listed as a unifying frame, not a separate candidate. **Plausibility low; included
because Eldan localization is the canonical "martingale instead of moment" device and a reviewer asked
for it by name.**

---

## D — WHY each object escapes the barrier (summary table)

| Object | Barrier it dodges | The non-moment mechanism |
|---|---|---|
| Frankl join-coupling `Δ_x` (A.1) | symmetric convex moment of `freq` | pair correlation `P(x∉A,x∈B)`, lives on `F×F`, not on marginals |
| Frankl Stein/exchangeable-pairs `D(x)` (A.2) | "must be sensitive to *which* x" | antisymmetric kernel + generator-asymmetric weight; cube = zero of `D`, not min of moment |
| Collatz 3-adic `W`-contraction (B.2) | inert spectrum (`P_n` nilpotent) | nilpotency *re-read* as exact 1/3 contraction in 3-adic metric; coupling identity `v_3(3Δ)=v_3(Δ)+1` |
| Collatz joint `(residue,drift)` `W` (B.4) | TV ≥ 1/6 to `U` | contracts to correct `π_n`, keeps joint; mod-3 marginal fact invisible to joint contraction |

The unifying point (PLAN.md discipline): none of these is `Σ_x g(freq_x)` (Frankl) or a spectral
radius / averaging-to-`U` statement (Collatz). All are **joint-law** objects. That is the entire reason
to look here, and the entire reason they *might* be a disguised moment after collapse — which is what the
§A.4 / §B.5 probes decide.

---

## E — Concrete deliverables checklist (what to build next, no proofs)

- [ ] `frankl/experiments/join_coupling_stein.py`: A.4 steps 1–3 over n≤5 census. Key outputs:
      (i) a same-`freq`/different-`Δ_x` pair (escape-the-moment-class witness);
      (ii) does `argmax_x D(x)` certify ≥ 1/2? violation count;
      (iii) `D(x)≡0` on cubes, `>0` off-cube (non-flatness diagnostic).
- [ ] `collatz/experiments/wasserstein_3adic.py`: B.5 steps 1–3. Key outputs:
      (i) exact 1/3 synchronous-coupling contraction confirmed n≤8;
      (ii) `W^{(3-adic)}(π_n,U)` vs `TV` table (does `W` stay bounded while TV floors?);
      (iii) joint `(residue,drift)` Sinkhorn contraction ratio under `s*`.
- Both isolated under their experiments dirs; touch nothing outside `math/ideas/generation/` for *this*
  document. (The code is a *proposed* next step, not part of this deliverable's file footprint.)

---

## F — PLAUSIBILITY, failure modes, novelty

**Frankl — Stein/exchangeable-pairs join-coupling (A.2/A.4): plausibility 2.5/5.**
- *For:* genuinely non-symmetric (antisymmetric kernel + asymmetric weight), cube sits at the *boundary*
  `D=0` rather than at a moment-minimum (a qualitatively new place to be), and it is the probabilistic
  twin of the JI-overlap lever two independent agents already converged on. The same-freq/different-`Δ`
  probe can *prove* it is outside the moment class.
- *Against (failure modes):* (1) `D(x)` may anti-correlate with abundance (the V1 pattern: heavy ⟺ large
  flux, so the certificate adds nothing); (2) Stein bounds typically need a *Poisson-equation solution*
  whose smoothness on a non-FKG lattice is unclear; (3) most likely it reaches *exactly* 1/2 with zero
  margin (cube), like all 8 methods, just dressed as a coupling. **The A.4.2 sweep settles 2.5→{≥3 or ≤1.5}
  in one run.**
- *Frankl monotone join-coupling alone (A.1): plausibility 1.5/5* — degenerates on the cube transparently;
  valuable only as the drift inside A.2/C.

**Collatz — 3-adic Wasserstein contraction (B.2/B.3): plausibility 3/5 for the *contraction fact*,
2/5 for *natural-density payoff*.**
- *For:* the 1/3 contraction is an **exact, provable** coupling identity (the `×3` in `3x+1`), and it
  reinterprets the project's strongest Collatz obstruction (nilpotent `P_n`) as a *feature* in the right
  metric — a real conceptual reframing. It is exactly "a Wasserstein contraction in a metric adapted to
  `π_n`, not `ℓ²`/TV," as the brief requested.
- *Against (failure modes):* (1) "true but useless" — contracts to the wrong target `π_n` (the `perp_gap.md`
  trap); (2) `W^{(3-adic)}(π_n,U)` may floor like TV (B.6.1), killing the metric advantage; (3) the joint
  `(residue,drift)` contraction (B.4 — the only version that touches the real gap) collides with the
  `s_c≈−0.4` phase transition and likely needs a non-scalar coupling that is not constructed here.
- *Joint `(residue,drift)` martingale-coupling (B.4): plausibility 2/5* — highest upside (it is the open
  route `natural_density_obstruction.md` §5.2 names), highest risk (phase-transition incompatibility).

**Eldan localization (C): plausibility 1/5** — unifying frame, no independent traction.

**`[NOVELTY UNVERIFIED]` on everything.** Likely-prior-art: Stein/exchangeable-pairs on lattices
(Chatterjee, Röllin); path-coupling for Markov chains (Bubley–Dyer); 3-adic / ultrametric dynamics and
Collatz (Akin 2004; Bernstein–Lagarias 2-adic conjugacy — the 3-adic contraction may be a known
restatement of the `3x+1` map's 3-adic expansion/contraction structure, **check this first**, it is the
biggest novelty risk for Part B). arXiv was 403 this session; no primary-source verification performed.

**Named theorems invoked (as directions, not applied as proofs):** Strassen's coupling/domination
theorem (A.1), Bubley–Dyer path coupling + Kantorovich–Rubinstein duality (B.2), Stein's method via
exchangeable pairs / Chen–Stein (A.2), Skorokhod embedding & martingale optional stopping (B.4, C),
Eldan stochastic localization (C), Holley's criterion / FKG (noted as **inapplicable**, §A.0).

**Honest bottom line.** Two of these are real "non-moment" objects with exact structural content
(Frankl `D(x)` antisymmetry; Collatz 1/3 3-adic contraction), each decided by *one small computation*
already specified. Both most-likely degenerate on the canonical extremizer — but *differently* from a
moment (as a kernel-zero / as a contraction-to-`π_n`), and that difference is exactly what the §A.4 /
§B.5 probes are designed to expose. No proof; no improved constant; no natural-density result claimed.
