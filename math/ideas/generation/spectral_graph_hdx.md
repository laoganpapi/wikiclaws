# Spectral graph theory / HDX / Garland — a non-moment direction for Frankl (and a note on Collatz)

**Author:** Alex Ye (no AI on author line).
**Date:** 2026-06-03.
**Status:** `[NOVELTY UNVERIFIED]` on all framings; this is a **direction**, not a
proof. Computational probe + small validation done at n≤5; everything analytic
is flagged speculative.
**Scope rule:** lives entirely under `math/ideas/generation/`. Companion code:
`math/ideas/generation/_probe/cover_graph_spectrum.py`; data
`_probe/cover_spectrum_n{0..5}.jsonl`. It imports the read-only frankl toolkit
(`lattice.py`, `uc_family.py`, `enumerate.py`, `ji_labelling.py`) but modifies
nothing outside `generation/`.

---

## 0. The one-paragraph pitch

Every prior spectral attack in this project used the **abelian (Z/2)^n Walsh
spectrum of `1_F` on the ambient hypercube** (`boolean_fourier.md`). The proven
barrier (Thm 4.3 there) is that this spectrum is rotation+sign-invariant in the
ground elements — a *symmetric convex moment* — so it collapses to `δ_{S,∅}` on
the Boolean cube `2^[k]`, the unique Frankl extremizer (`join_irreducible_label
ling.md`, H5). **This document changes the underlying graph.** Instead of the
abelian cube, put the spectral object on the **cover graph (Hasse diagram)** and
the **comparability graph** of the lattice `L = (F, ⊆, ∪)`, and on the **order
complex** (a simplicial complex whose links carry *local* spectra à la
Garland/Oppenheim). These spectra are functions of the **incidence structure of
the order**, not of the abelian characters, and they are **non-trivial on the
cube** (the cover graph of `2^[k]` is the hypercube graph `Q_k`, whose Laplacian
spectrum is the full set `{0,2,…,2k}`, not a delta). So the barrier's mechanism —
"the extremizer has trivial spectrum" — **does not fire here.** The honest probe
result (n≤5): the cover-graph algebraic connectivity (Fiedler value) is a genuine
non-symmetric correlate of abundance (Pearson −0.40; clean monotone bucket
trend), but it still **caps at the cube** rather than exceeding it, so it is a
*lever*, not yet a certificate. The deliverable is the precise object, why it
escapes the barrier's collapse, and the validated correlation + failure modes.

---

## 1. The graph / complex and the spectral object

Fix a union-closed `F` with `∅ ∈ F` (adjoin `∅` if absent), so
`L = (F, ⊆, ∪)` is a finite lattice with bottom `0̂ = ∅`, top `T = ⋃F`, and
`|L| = |F|`. Abundance `= max_x |Fib(x)|/|L|` where `Fib(x) = {A ∈ F : x ∈ A}` is
a **filter** (up-set). Frankl ⟺ some fibre has density ≥ ½.

We build three spectral objects on `L` (all in
`_probe/cover_graph_spectrum.py`).

### 1.1 Cover-graph (Hasse) Laplacian

`G_cov`: vertices `= L`, undirected edge `{A,B}` iff `A ⋖ B` (cover relation).
Compute the **unnormalized graph Laplacian** `Lap = D − A` and its spectrum
`0 = μ_1 ≤ μ_2 ≤ … ≤ μ_m`. The headline statistic is the **algebraic
connectivity / Fiedler value** `μ_2(G_cov)` (the cover-graph spectral gap), plus
`λ_max` of the normalized Laplacian. **Theorem named:** Fiedler's theorem
(`μ_2 > 0` ⟺ connected; `μ_2` lower-bounds vertex/edge connectivity), and the
Hoffman ratio bound (below).

### 1.2 Comparability-graph Laplacian + Hoffman ratio bound

`G_cmp`: vertices `= L`, edge `{A,B}` iff `A < B` or `B < A` (comparable). This
is the **comparability graph** of the poset. The relevant named tool is the
**Hoffman / ratio bound**: for a `d`-regular graph with least adjacency
eigenvalue `λ_min`, the independence number satisfies
`α ≤ |V| · (−λ_min)/(d − λ_min)`. A **fibre `Fib(x)` is a filter, i.e. a clique
in `G_cmp` is a chain, an independent set is an antichain** — abundance is the
max *filter* density, which is neither, so the raw Hoffman bound on `α(G_cmp)`
does not directly read abundance. The probe therefore applies the ratio/expander
idea to the **fibre-incidence bipartite graph** `B` (ground elements `x` vs
members `A`, edge iff `x ∈ A`): abundance `= (max row weight of B)/|L|`, and the
**expander-mixing lemma** bounds how far the max row weight can sit above the
mean in terms of the **second singular value `σ₂(B̃)`** of the normalized
incidence. This `σ₂` is the genuinely *labelling-sensitive*, non-symmetric
ingredient (it sees *which* element is heavy).

### 1.3 Garland / Oppenheim local spectrum on the order complex

`X`: the **order complex** of `L` (simplices = chains). For each vertex `A`, its
**link** is the order complex of the comparable elements; the **local spectral
gap** `λ_loc(A) = μ_2` of the link's normalized Laplacian. **Theorems named:**
*Garland's method* (vanishing of higher cohomology / Poincaré inequalities from
local spectral gaps), *Oppenheim's trickle-down* (if every link is a
`λ`-one-sided local spectral expander then the whole complex is, and global
expansion is controlled by the **minimum** local gap), and *Kaufman–Oppenheim*
(local-to-global for HDX random walks). The probe reports
`min_A λ_loc(A)` — the quantity trickle-down propagates upward.

---

## 2. Why this escapes the abelian-hypercube barrier

The barrier (`boolean_fourier.md` Thm 4.3, `join_irreducible_labelling.md` §5)
has a single mechanism: **the Frankl extremizer (the Boolean cube `2^[k]`) has a
*trivial / fully-symmetric* spectral footprint**, so any rotation+sign-invariant
quadratic of the abelian spectrum vanishes there and cannot certify ≥ ½.

The cover-graph and link spectra **break this mechanism on three counts.**

1. **Non-trivial on the cube.** The cover graph of `2^[k]` is the hypercube
   graph `Q_k`. Its Laplacian spectrum is `{ 2j : multiplicity C(k,j) }`,
   ranging over `[0, 2k]`, Fiedler value exactly `2`. The probe confirms (output
   §4): `B_1,…,B_4` all have Fiedler(cover)`=2.0000`, Laplacian range `[0, 2k]`,
   and a *non-trivial* `min_link_gap` (`1.0, 0.667, 0.583` for `k=2,3,4`). This
   is the polar opposite of the Walsh spectrum `f̂(S)=δ_{S,∅}` which is literally
   a point mass. **The extremizer is spectrally rich here, not collapsed.**

2. **Non-symmetric in the ground elements.** The abelian spectrum is symmetric
   under the `(Z/2)^n` group (sign flips) and under `S_n` (coordinate rotations);
   that symmetry is exactly what forces it to be a moment. The cover/comparability
   graph is built from the **order relation among members of `F`**, whose
   automorphism group is the (much smaller) lattice-automorphism group, and the
   **fibre-incidence singular value `σ₂(B̃)` further depends on the labelling**
   (which `x` lands in which `A`). The cone trick (`lattice_attack.md` §4) shows
   the labelling is exactly what carries abundance; `σ₂(B̃)` is the first spectral
   object in this project that *sees* it (it changes when you relabel even if `L`
   is fixed). So this is genuinely outside the "symmetric convex moment" class the
   barrier theorem delimits.

3. **Incidence-/link-sensitive (HDX).** Garland/Oppenheim local spectra are
   *local* invariants of the incidence structure: `λ_loc(A)` depends on the
   geometry of the interval around `A`, not on any global average. The barrier is
   a statement about *global symmetric moments*; **local spectral expansion is a
   non-moment, non-symmetric quantity by construction.** Whether it controls
   abundance is the open question — but it is not in the delimited class.

**Honest caveat (the barrier's shadow).** Items 1–3 say the *mechanism* of the
barrier (collapse on the extremizer) does not apply. They do **not** say a
cover-graph bound *will* beat ½. The probe (next section) shows the cover-graph
Fiedler value still *caps* at the cube: the families with abundance exactly ½ are
precisely the maximally-cover-connected ones (Fiedler `= 2`). So any **monotone**
cover-spectral bound still bottoms out *at* the cube — it can *reach* ½, the same
ceiling every method hits. The escape, if real, must come from a quantity that is
non-monotone in the cube direction — the strongest candidate being the
**labelling-sensitive `σ₂(B̃)` / Hoffman bound on the fibre incidence**, which is
NOT a lattice invariant and so is not pinned by the cube-uniqueness theorem.

---

## 3. Concrete first step (done): spectrum of all UC families n≤5, correlated with abundance

`_probe/cover_graph_spectrum.py` enumerates every non-trivial UC orbit rep at
n≤5 (the project's standard census, 29,723 families) and computes, per family:
`fiedler_cover = μ_2(G_cov)`, `fiedler_comparability = μ_2(G_cmp)`,
`lmax_norm_cover`, `min_link_gap` / `mean_link_gap` (Garland local spectrum),
and the fibre-incidence Hoffman block `avg_fib_density`, `σ₂(B̃)`, `hoffman_gap`,
`max_fib_density (= abundance)`.

**Pearson correlation with abundance (29,723 families, n≤5):**

| statistic | corr | reading |
|---|---|---|
| `max_fib_density` | **+1.000** | tautology — it *is* abundance (pipeline sanity) |
| `hoffman_gap` (= ab − mean) | +0.879 | the spread the ratio bound governs |
| `fiedler_cover` | **−0.397** | low cover-connectivity ⟹ high abundance |
| `fiedler_comparability` | −0.308 | same sign, weaker |
| `mean_link_gap` (Garland) | +0.287 | small positive |
| `avg_fib_density` (symmetric mean) | +0.252 | a moment — weak |
| `σ₂_bipartite` (Hoffman) | −0.252 | more expansion ⟹ flatter ⟹ lower abundance |
| `lmax_norm_cover` | +0.018 | inert |

**The clean signal — cover-graph Fiedler buckets vs abundance:**

| `μ_2(G_cov)` ≈ | #families | min abundance | mean abundance |
|---|---:|---:|---:|
| 0.3 | 14 | 0.714 | 0.810 |
| 0.5 | 266 | 0.636 | 0.802 |
| 0.8 | 3882 | 0.529 | 0.744 |
| 1.0 | 5594 | 0.565 | 0.712 |
| 1.3 | 1878 | 0.529 | 0.686 |
| 1.7 | 60 | 0.533 | 0.687 |
| **2.0** | 183 | **0.500** | 0.647 |

A clear monotone trend: **the more connected the Hasse diagram (higher Fiedler),
the lower the abundance**, and abundance bottoms out at ½ *exactly* in the
maximally-connected bucket `μ_2 = 2` — which contains the Boolean cubes. This is
a real, non-symmetric, incidence-based correlate that the abelian spectrum did
not have (there, the cube had trivial spectrum and zero discriminating power).

**The named-theorem quantity (Hoffman / expander mixing).** `avg_fib_density`
(the mean fibre density, a symmetric moment) is `≥ ½` in **29,283/29,723**
families but **fails in 440** (min 0.36) — so the mean *alone* cannot prove
Frankl (consistent with the barrier: it is a symmetric moment). In those 440
"mean-fails" families abundance still ranges `[0.529, 0.857]`; the *gap*
`abundance − mean` is exactly what `σ₂(B̃)` (expander mixing) governs. **The
concrete open lever:** a union-closure lower bound on `σ₂(B̃)`-type spread that
forces `max ≥ ½` precisely when the mean dips below — this is the spectral
incarnation of the `ji_labelling` "JI-filter overlap" lever (`join_irreducible_
labelling.md` §6), now phrased as an expander-mixing / Hoffman inequality on the
fibre incidence.

## 4. Small validation (n≤5)

Reproduce:
```
cd math/ideas/generation/_probe
python3 cover_graph_spectrum.py 5     # ~6 min; writes cover_spectrum_n{0..5}.jsonl
```
Validated facts (from the run, full output in the script's stdout):
- **Census matches the project standard:** 1 / 6 / 33 / 362 / 29,321 non-trivial
  UC orbit reps at n = 1..5 (totals 29,723), agreeing with `boolean_fourier.md`
  and `join_irreducible_labelling.md`. Frankl holds: min abundance `= 0.5000`.
- **Cube cover-spectra are non-trivial** (the escapes-the-barrier check):
  `B_k` has cover-graph `= Q_k`, Fiedler `= 2.0000`, Laplacian range `[0, 2k]`,
  `min_link_gap` `∈ {1.0, 0.667, 0.583}` for `k = 2,3,4`. Contrast: the Walsh
  spectrum of the cube is `δ_{S,∅}` (trivial). **The barrier's collapse does not
  occur for these graph spectra.**
- **The 63 families at abundance exactly ½** all have `fiedler_cover = 2.0000`
  (max possible), i.e. they are the maximally-cover-connected lattices — the
  spectral fingerprint of the extremal set is "most connected cover graph,"
  a *non-symmetric* characterization the abelian spectrum could not give.
- **Monotone bucket trend** (table §3) verified across all 29,723 families.

## 5. Plausibility, failure modes, novelty

**Plausibility: 2 / 5.**

Rationale. The direction *cleanly clears the stated barrier* (the cube has rich,
non-trivial cover/link spectra, and `σ₂(B̃)` is labelling-sensitive, hence
outside the symmetric-convex-moment class the barrier theorem delimits). That is
the main positive. But the n≤5 evidence shows the *order-only* graph spectra
(`fiedler_cover`, comparability, Garland local gaps) are **lattice invariants**,
and `lattice_attack.md` *proves* abundance is **not** a lattice invariant (the
cone trick: lattice-isomorphic families, abundance 0.5 vs 0.875, identical Hasse
spectrum). **⇒ Any bound using only `G_cov`/`G_cmp`/order-complex link spectra is
provably incapable of certifying abundance** — it can correlate (the −0.40 we
see) but cannot prove. The *only* sub-direction that survives this is the
**fibre-incidence `σ₂(B̃)` / Hoffman bound**, which is not a lattice invariant.
That single lever keeps the plausibility above 1, but it is exactly the same
"second-moment / overlap" lever already flagged by three other methods
(`lp_duality.md` §6, `second_moment`, `join_irreducible_labelling.md` §6) — so
this is a *spectral repackaging* of a known crux, not an independent new route.
Honest score 2/5: clears the barrier, gives a measured signal, but the order-only
half is killed by the cone and the surviving half is not new.

**Failure modes.**
1. **Cone / lattice-invariance (the decisive one).** All of §1.1, §1.2 (cmp
   half), §1.3 are lattice-iso invariants ⟹ blind to the labelling ⟹ `lattice_
   attack.md`'s cone obstruction makes them provably non-certifying. The −0.40
   correlation is real but cannot be upgraded to a bound. **The probe already
   exhibits this:** abundance-½ families and abundance-0.875 cone families can
   share Hasse spectra.
2. **Caps at the cube (the barrier's shadow).** Even the labelling-sensitive
   `σ₂(B̃)` is, on the cube, exactly the generic value (the cube's incidence is
   a regular design), so any *monotone* Hoffman bound still reaches only ½. To
   exceed ½ one needs a *strict* expander-mixing improvement that is `> 0`
   precisely off the cube — unproven and possibly false.
3. **HDX needs a balanced complex.** Garland/Oppenheim trickle-down and
   Kaufman–Oppenheim local-to-global are sharpest for *pure, well-linked*
   complexes (Ramanujan complexes, partite HDX). The order complex of an
   arbitrary UC lattice is **not pure** (chains have varying length) and not a
   designed HDX, so the clean trickle-down constants do not apply off the shelf;
   one would have to engineer a balanced sub/auxiliary complex (e.g. the
   bipartite JI-vs-fibre incidence as a 1-dimensional HDX with a chosen
   weighting). That construction is undone here.
4. **Numerics, not proof.** All correlations are float64 at n≤5; n≤5 cannot rule
   out that a larger-`n` non-cube lattice realizes a different spectral/abundance
   relation (same caveat as `join_irreducible_labelling.md` §5).

**Novelty.** `[NOVELTY UNVERIFIED]`. Cover-graph / comparability-graph spectra of
lattices are classical (algebraic graph theory; Stanley). Garland's method,
Oppenheim trickle-down, Kaufman–Oppenheim local-to-global, and the Hoffman ratio
bound are all standard named tools. Applying HDX/local-spectral machinery to
*Frankl specifically* is plausibly new in this project's context but the prior is
**moderate-to-high that the cover-graph correlation is folklore** (anyone who has
computed Hasse Laplacians of UC lattices would see it). The genuinely
project-specific observation — *that the order-only spectra are lattice
invariants and hence killed by the cone, while only the fibre-incidence `σ₂`
survives* — is a clean **delimiting** statement in the same family as the other
seven obstructions, not a new bound. Prior-art check (blocked this session,
arXiv 403) is required before any claim.

---

## 6. Note on Collatz (the same toolkit, a different graph)

The brief asks whether a Cheeger/expansion bound on a **reverse-Collatz / 3-adic
shell graph** controls descent in a way the abelian spectrum missed. The relevant
project fact (`transfer_operator.md`, `perp_gap.md`): the one-step Syracuse Markov
chain `P_n` on `(Z/3^n)^×` has `P_n − Π` **nilpotent** (char. poly
`λ^{φ(3^n)−1}(λ−1)`), so the *abelian/eigenvalue* spectral gap is degenerate —
the obstruction is the **non-uniform stationary `π_n`** (the Syracuse RV), with a
permanent mod-3 marginal `(0,⅓,⅔)` realized as the rank-1 block
`[[⅓,⅔],[⅓,⅔]]` (`transfer_operator.md` Prop 3.1), giving `TV(π_n,U) ≥ ⅙`.

**Where an HDX/expander angle could differ from the abelian spectrum.** The dead
abelian object is the *eigenvalue spectrum of `P_n`*. A non-abelian replacement:
build the **reverse Collatz tree as a 1-dim'l complex / bipartite incidence**
between residue shells mod `3^k` (the projective filtration
`V^{(1)} ⊂ ⋯ ⊂ V^{(n)}` of `transfer_operator.md` §3.1) and apply a
**Cheeger / conductance** (not eigenvalue) bound across shells. Conductance is a
**combinatorial expansion** quantity, *not* a moment of the spectrum, so it is
not inert under the nilpotency that kills the eigenvalue gap: a chain can have
zero spectral gap on a subspace yet positive conductance between shells.

**Plausibility for Collatz: 1.5 / 5.** Honest "why not": `transfer_operator.md`
already shows the difficulty is the *target measure* `π_n`, not the *mixing rate*
— and conductance, like the spectral gap, is a property of the *rate*, so it is
likely *also* inert against the `π_n` obstruction (TV≥⅙ holds regardless of how
fast the chain mixes). The one thing conductance buys that the eigenvalue
spectrum does not is sensitivity to the **non-normal / nilpotent** structure:
`P_n` is non-self-adjoint, so its singular values (hence its Cheeger constant via
the *symmetrized* chain `P_n P_n^*`) can be bounded below even when eigenvalues
are zero. A concrete first probe (not done here; flagged for a Collatz agent):
compute the **Cheeger constant `h(P_n)` of the symmetrized Syracuse chain on each
mod-`3^k` shell** for `n ≤ 8`, and test whether `h` stays bounded below
**uniformly across the filtration** — the conductance analogue of the
"uniform perp-gap" question (`transfer_operator.md` §6). If yes, it gives a
*coset-respecting* descent control; it still cannot remove the mod-3 obstruction,
so it inherits the same ceiling. Recommend NOT prioritizing over the Frankl
sub-direction.

---

## 7. Verdict

- **Frankl direction:** put the spectral object on the **cover graph / order
  complex / fibre incidence** of `L`, not the abelian cube. This *cleanly clears
  the barrier's collapse mechanism* (the cube has rich cover/link spectra) and
  yields a **validated non-symmetric correlate of abundance** (`fiedler_cover`,
  corr −0.40, monotone buckets, 29,723 families n≤5). **But** the order-only
  spectra are lattice invariants ⟹ killed by the cone obstruction; the only
  surviving lever is the **labelling-sensitive fibre-incidence Hoffman /
  expander-mixing `σ₂(B̃)`**, which is a *spectral repackaging of the already-
  identified second-moment / JI-overlap crux*. Plausibility **2/5**: clears the
  barrier, partial signal, but order-only half provably can't certify and the
  surviving half is not independent of known levers.
- **Collatz note:** a Cheeger/conductance (singular-value) bound on the
  symmetrized Syracuse chain across the mod-`3^k` filtration is the only HDX-style
  object that is *not* inert under the proven nilpotency — but it is still a
  *rate* quantity and the obstruction is the *target* `π_n` (TV≥⅙), so
  plausibility **1.5/5**; a single concrete probe is named but deprioritized.

All claims `[NOVELTY UNVERIFIED]`; no proof, no constant > ½ claimed; every number
validated at n≤5 in `_probe/`.
