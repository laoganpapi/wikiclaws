# Poset & algebraic topology: Möbius / order-complex / crosscut attacks on Frankl (and a Collatz note)

**Author:** Alex Ye (no AI on author line).
**Date:** 2026-06-03.
**Field cluster:** #3 (algebraic & poset topology — order complexes, Möbius
functions, crosscut/nerve/Quillen-fiber theorems, discrete Morse).
**Status:** `[NON-MOMENT direction + a SHARP negative — both established
computationally on all 29 723 UC families n≤5. NOVELTY UNVERIFIED.]`
**Companion code:** `poset_topology_probe.py` (this directory; reuses
`frankl/experiments/{enumerate,uc_family,lattice}.py`).
**Cross-ref:** `frankl/theory/lattice_attack.md` §4 (cone obstruction — the wall
this note's main object hits), `ji_overlap_inequality.md` (the crosscut complex on
JI is *literally* the object there), `join_irreducible_labelling.md` §6
(Candidate 6.1), `collatz/theory/transfer_operator.md` (§7 below).

> **One-paragraph verdict.** The Möbius function `μ_L(0̂,1̂)`, the reduced Euler
> characteristic / homology of the order complex `Δ(L̄)` (proper part), and the
> reduced Euler char of the **crosscut complex on the join-irreducibles** are
> genuinely **non-moment, non-symmetric** invariants — they are NOT convex
> moments of the frequency vector, so the project's flat-minimization barrier does
> **not** apply to them a priori. I computed all three on all 29 723 UC families
> n≤5. **Three clean facts emerge.** (1) **Identity (verified):**
> `μ_L(0̂,1̂) = χ̃(Cr_JI)` exactly on every family (Philip Hall + crosscut theorem;
> JI is a crosscut here), and on the Boolean cube `B_k` both equal `(−1)^k` =
> reduced Euler char of a `(k−2)`-sphere — the textbook sanity check passes. (2)
> **The decisive wall:** every one of these invariants is a **function of the
> abstract lattice `L`**, hence is annihilated by the `lattice_attack.md` §4 *cone*
> construction: `cone(B_3)` has identical `μ = −1 = χ̃` as `B_3` but abundance
> jumps `0.5 → 0.875`. So **Möbius/homotopy-type of `L` cannot force abundance** —
> same obstruction as every other lattice invariant. (3) **The fibre/nerve
> complexes are contractible:** the down-closure complex `Δ_F` (= nerve of the
> fibre cover) has reduced Euler char `≡ 0` on all 29 723 families, because the top
> `T` is a cone point. **The honest conclusion:** the *invariant* layer of poset
> topology is dead by the cone; the *only* live topological object is a
> **labelled/relative** one (a fibrewise or `T`-deleted complex that the cone does
> change), and §5 isolates exactly which one. Plausibility **2/5**.

All numbers validated on **all 29 723 UC families with |F|≥2, n≤5**.

---

## 1. The topological objects and invariants (Task 1)

Fix `F` union-closed, adjoin `∅` so `L = (F,⊆,∪)` is a lattice with bottom `0̂=∅`,
top `T=⋃F`, `|L|=m`. Three classical poset-topology objects:

**(O1) Möbius number `μ_L := μ_L(0̂, 1̂)`.** The value at `(bottom, top)` of the
Möbius function of the incidence algebra (`mobius_lattice` in the probe). By
**Philip Hall's theorem**, `μ_L(0̂,1̂) = χ̃(Δ(L̄))`, the reduced Euler
characteristic of the **order complex of the open interval** `L̄=(0̂,1̂)` (chains
of proper non-bottom/non-top elements). This is a homotopy invariant of `Δ(L̄)`.

**(O2) Order complex / homology `H̃_*(Δ(L̄))`.** The full homotopy type, of which
`μ_L` is the Euler-characteristic shadow. For the **Boolean lattice** `B_k`,
`Δ(B̄_k) ≃ S^{k-2}` (a sphere), so `H̃_*` is concentrated in degree `k−2` and
`μ = (−1)^k`.

**(O3) Crosscut complex on the join-irreducibles, `Cr_JI`.** A **crosscut** of a
lattice is an antichain `C` meeting every maximal chain such that no subset of `C`
has a join/meet escaping the interval. The **crosscut theorem** (Folkman; Rota)
says `Δ(L̄)` is homotopy equivalent to the **crosscut complex** `Cr(C)`, whose
faces are the subsets `S⊆C` that are **bounded** (here: `⋁S ≠ 1̂`). I take `C=JI`
(the join-irreducibles); a face is `S⊆JI` with `⋁S ≠ T`. This is **exactly** the
object of `ji_overlap_inequality.md` / `join_irreducible_labelling.md` §6: the
union/overlap structure of the principal JI-filters `↑j`. `χ̃(Cr_JI)` is its
reduced Euler characteristic (`crosscut_euler_on_JI` in the probe).

> **Verified identity (29 723/29 723 families, 0 exceptions).**
> $$\mu_L(0̂,1̂)\;=\;χ̃(\mathrm{Cr}_{JI})\qquad\text{exactly.}$$
> This is Philip Hall + crosscut theorem made arithmetic: both equal the reduced
> Euler char of `Δ(L̄)`. The probe computes the two sides by completely different
> routes (full Möbius recursion vs. enumerating bounded JI-subsets) and they agree
> on every family. So the **crosscut complex on JI is a genuine model of the
> homotopy type of `L`** in this census — the JI-overlap object of
> `ji_overlap_inequality.md` literally computes the Möbius number.

---

## 2. Why these are non-moment & non-flat on the cube (Task 2)

**Non-moment / non-symmetric.** `μ_L`, `H̃_*(Δ(L̄))`, `χ̃(Cr_JI)` are computed from
the **incidence/chain structure** of `L`, not from the multiset of frequencies
`{freq(x)}`. They are **not** convex (or any) functions of the frequency vector:
two families with the *same* frequency multiset can have different `μ_L` (different
Hasse diagrams), and — sharper — `μ_L` is a `±`-alternating signed count of chains,
not a monotone/convex functional of any vector. The project's barrier
("every symmetric convex moment of the frequency vector is flat-minimized by the
cube at ½") therefore **does not apply**: these are not moments at all. This is the
intended escape hatch.

**Cube sanity (Task-2 explicit computation, verified).** For the genuine Boolean
cube `2^{[k]}` (with `∅`, so `|L|=2^k`):

| `k` | `|L|` | `μ_L(0̂,1̂)` | `χ̃(Cr_JI)` | homotopy of `Δ(L̄)` | abundance |
|---|---|---|---|---|---|
| 1 | 2 | `−1` | `−1` | `S^{-1}` (∅) | 0.5000 |
| 2 | 4 | `+1` | `+1` | `S^{0}` | 0.5000 |
| 3 | 8 | `−1` | `−1` | `S^{1}` | 0.5000 |
| 4 | 16 | `+1` | `+1` | `S^{2}` | 0.5000 |
| 5 | 32 | `−1` | `−1` | `S^{3}` | 0.5000 |

So `μ_{B_k}=(−1)^k`, `Δ(B̄_k)≃S^{k-2}`, **exactly the brief's sanity target**, and
**abundance is exactly ½** for the cube at every `k` (the project's extremal
family). The invariant is *non-flat across families* (it ranges over
`{−6,…,+4}` at n≤5; see §3) and on the cube it tracks the sphere dimension — a
genuinely topological, non-moment signal. The escape from the moment barrier is
**real at this level**. The problem is at the next level (§4).

---

## 3. The correlation on all UC families n≤5 (Task 3 + 4: compute + validate)

`poset_topology_probe.py 5` computes `μ_L`, `χ̃(Cr_JI)`, `χ̃(Cr_atoms)`, and
abundance for all 29 723 families. Headline cross-tabulation `μ_L → abundance`:

| `μ_L` | #families | min abund | max abund | mean abund | #abund<½ |
|---|---|---|---|---|---|
| −6 | 2 | 0.6471 | 0.6875 | 0.667 | 0 |
| −5 | 10 | 0.6471 | 0.7333 | 0.693 | 0 |
| −4 | 80 | 0.6250 | 0.7857 | 0.700 | 0 |
| −3 | 484 | 0.5833 | 1.0000 | 0.711 | 0 |
| −2 | 2504 | 0.5833 | 1.0000 | 0.722 | 0 |
| **−1** | 8097 | **0.5000** | 1.0000 | 0.730 | 0 |
| **0** | 16834 | 0.5161 | 1.0000 | 0.756 | 0 |
| **+1** | 1520 | **0.5000** | 1.0000 | 0.742 | 0 |
| +2 | 164 | 0.5517 | 1.0000 | 0.696 | 0 |
| +3 | 24 | 0.5556 | 1.0000 | 0.686 | 0 |
| +4 | 4 | 0.5556 | 0.8333 | 0.670 | 0 |

(`χ̃(Cr_JI)` gives the **identical** table — the §1 identity.) **Validation
(Task 4): Frankl holds** — `#abund<½` is `0` in every bucket; the global minimum
abundance is exactly `0.5`. Two structural readings:

- **A weak signal exists.** Large `|μ_L|` correlates with higher *minimum*
  abundance: `|μ_L|≥4 ⇒ abund ≥ 0.625`; `|μ_L|≥2 ⇒ abund ≥ 0.5517`. The
  abundance-½ families sit only at `μ_L∈{−1,+1}` (small `|μ|`). Topologically
  "rich" lattices (big Möbius number, high-dimensional `Δ(L̄)`) are **never**
  tight. This is a *non-moment* observation the moment barrier cannot make.
- **But the signal does not isolate the extremal family** and **mean abundance is
  highest at `μ_L=0`** (acyclic order complex), i.e. the topological size of `L`
  does not monotonically track abundance. Crucially, the ½-tight family lives at
  `μ=±1`, the *same* values carried by huge numbers of high-abundance families.

The honest test is §4: can a *fixed* `μ_L` value coexist with both ½ and ≫½?

---

## 4. The decisive wall: Möbius/homotopy of `L` is cone-killable (Task 5 core)

> **Finding 4.1 (verified).** The cone construction of `lattice_attack.md` §4
> fixes `μ_L` and the entire homotopy type of `Δ(L̄)` while driving abundance to 1.
> Explicitly, for `B_3` vs its cone:
>
> | family | `|L|` | `μ_L` | `χ̃(Cr_JI)` | abundance |
> |---|---|---|---|---|
> | `B_3 = 2^{[3]}` | 8 | `−1` | `−1` | **0.5000** |
> | `cone(B_3)` | 8 | `−1` | `−1` | **0.8750** |
>
> Same lattice (cone is a lattice isomorphism, `lattice_attack.md` Prop 4.1), so
> **every** poset-topology invariant — `μ_L`, `H̃_*(Δ(L̄))`, `χ̃(Cr_JI)`,
> `χ̃(Cr_atoms)`, the whole homotopy type — is **identical**, yet abundance differs
> by 0.375. (Verified across the cone family; `μ=−1` alone hosts 57 distinct
> abundances `0.5…1.0`, 23 of them tight at ½.)

This is the **same obstruction** `lattice_attack.md` §4 proves for height/width/#JI:
**abundance is not a function of the abstract lattice**, and `μ_L`/homotopy type
*are* functions of the abstract lattice, so they cannot force abundance. The
non-moment escape of §2 is genuine but **lands on the cone wall instead of the
flat-minimization wall** — a *different* barrier, equally fatal to any invariant
that sees only `L`.

### 4.1 The nerve of the fibres is contractible (second wall)

The natural *labelled* topological object is the **nerve of the fibre cover**:
`{Fib(x)}_{x∈[n]}` covers `L∖{0̂}`, and the nerve `N` has a face `X⊆[n]` iff
`⋂_{x∈X}Fib(x)=\{A: X⊆A\}≠∅`, i.e. iff `X⊆A` for some `A∈F`. So **the nerve of
the fibres is exactly the down-closure simplicial complex `Δ_F={X:X⊆A,\,A∈F}`**
(F viewed as a complex). By the **nerve theorem** (the `Fib(x)` are filters, their
nonempty intersections are filters hence contractible-in-`L`), `Δ_F` models the
homotopy type of the union `L∖{0̂}`.

> **Finding 4.2 (verified, 29 723/29 723).** `χ̃(Δ_F) ≡ 0` on **every** family —
> `Δ_F` is **always contractible**. Reason: `T=⋃F∈F`, so the full vertex set
> `[supp]` is a face and is a **cone point** (every face `X⊆T`). The nerve of the
> fibres carries **no homology whatsoever.**

So both natural complexes fail: `Δ(L̄)` is a lattice invariant (cone-killable),
and `Δ_F` (the fibre nerve, which *is* labelling-sensitive) is **contractible** by
the union-closure top element. **Union-closure, which gives `Δ_F` its cone point,
is exactly what destroys the homology that might have forced an abundant vertex.**
This is a sharp, slightly ironic obstruction: the hypothesis kills the invariant.

---

## 5. The ONLY live topological object: a relative / `T`-deleted complex

The two walls pin down what a *working* topological attack must look like. It must
be **(a) labelling-sensitive** (so the cone moves it — rules out `μ_L`,
`H̃_*(Δ(L̄))`, `χ̃(Cr_JI)`) **and (b) not coned off by the top `T`** (rules out
`Δ_F`). The candidate that survives both:

> **Object 5.1 `[NOVELTY UNVERIFIED — not computed yet]`.** The **deleted /
> relative** fibre complex `Δ_F^{−T}` obtained by removing the cone point `T`
> (work in `L∖{0̂,1̂}`, the proper part, but with the **vertex weighting by ground
> elements**): faces `X⊆[n]` with `X⊆A` for some **proper** `A∈F∖{T}`. Equivalently
> the nerve of the *restricted* fibres `Fib(x)∖{T}` on the proper part `L̄`.
> Deleting `T` removes the cone point, so `Δ_F^{−T}` can have nontrivial homology;
> and it is **labelling-sensitive** (the cone changes which `X` are faces because
> it changes which sets are proper), so the cone obstruction does not trivially
> apply. The **abundance question becomes a vertex-degree / Garland-type local
> statement on `Δ_F^{−T}`**: `freq(x) = |Fib(x)|`, and the heavy-vertex search is a
> max-degree statement on a complex whose *global* homology is now nonzero.

**Concrete lever (the Morse/Quillen route).** Run **discrete Morse theory** on
`Δ(L̄)` with a matching that pairs each proper element with a chosen ground
element it contains (a *labelled* acyclic matching). Critical cells then localize
at ground elements whose fibre cannot be "absorbed"; the **Morse inequalities**
bound `dim H̃_*` below by (#critical cells), and a critical cell at a vertex `x`
forces `freq(x)` large. The **Quillen fiber lemma** applied to the map
`L̄ → 2^{[n]}`, `A ↦ A`, has fibres = the fibre filters; if every fibre were
"small" (low abundance) and contractible, Quillen would force `Δ(L̄)` contractible
(`μ_L=0`) — so **`μ_L≠0` obstructs all fibres being simultaneously small**. The
§3 correlation (`|μ_L|≥4 ⇒ abund≥0.625`) is the **shadow of exactly this Quillen
mechanism** and is the one genuinely promising quantitative thread: *a lower bound
on `|μ_L|` (or `dim H̃_*(Δ(L̄))`) might force a heavy fibre via Quillen, on the
sub-class of lattices where the cone is structurally blocked* — dovetailing with
`lattice_attack.md` §5.2's upper-semimodular target (where adding a universal `z`
breaks semimodularity, so the cone is forbidden and `μ_L` is *not* free).

This is **not** a moment and **not** flat on the cube (the cube has `μ=(−1)^k≠0`,
so it is *not* in the `μ=0` degenerate class), so it escapes the moment barrier;
and it is labelling/relative, so it is not the bare lattice invariant the cone
kills — *provided* one restricts to a cone-blocked class. That restriction is the
price, and it is the same price `lattice_attack.md` §5.2 already identified.

---

## 6. Plausibility, failure modes, validation (Task 5)

**Plausibility: 2/5.**
- The **invariant** layer (`μ_L`, `H̃_*(Δ(L̄))`, `χ̃(Cr_JI)`) is **dead — 1/5**:
  cone-killable (Finding 4.1), exactly as `lattice_attack.md` §4 predicts for any
  function of `L`. The crosscut complex on JI is the `ji_overlap_inequality.md`
  object, already characterized there as a dead end (the `↑j∩↑k=↑(j∨k)` tautology
  drains its slack); the §1 identity `μ_L=χ̃(Cr_JI)` *explains why* — it is a
  homotopy invariant of `L`, hence cone-blind.
- The **relative/Morse/Quillen** layer (§5) is **3/5** and is the only reason this
  note is not a flat "no": it is non-moment, non-cone-trivial *on a restricted
  class*, and the §3 data (`|μ_L|` weakly forcing abundance via the Quillen
  shadow) is a real, non-moment correlation no symmetric-moment method produces.

**Failure modes.**
1. **Cone (primary).** Any quantity depending only on `L` is annihilated;
   confirmed for all of §1. The relative complex `Δ_F^{−T}` must be shown to
   *actually* change under cone and to lower-bound abundance — neither is done.
2. **Contractibility by the top (secondary).** Union-closure supplies a top, which
   cones off the fibre nerve (Finding 4.2). Any labelled complex must delete `T`
   (or weight it away) or it is homology-trivial.
3. **Folklore.** `μ_L=χ̃(Cr_JI)` and `Δ(B̄_k)≃S^{k-2}` are textbook (Folkman/Rota;
   Björner's *Topological Methods*). The *correlation with abundance* and the
   *cone-kills-Möbius* observation are flagged new but likely folklore-adjacent.
   `[NOVELTY UNVERIFIED]`.
4. **Restricted-class escape may be empty.** The §5 program only bites on classes
   where the cone is blocked (upper-semimodular, geometric). If `μ_L` is *still*
   not abundance-forcing there, the direction collapses to `lattice_attack.md` §5.2
   with no topological gain.

**Validation (n≤5, done).** 29 723 families. (i) `μ_L=χ̃(Cr_JI)`: 0 exceptions.
(ii) Cube `μ_{B_k}=(−1)^k`, abundance ½: k=1..5 exact. (iii) Frankl holds in every
`μ`-bucket (min abundance 0.5). (iv) Cone fixes `μ`, moves abundance 0.5→0.875.
(v) `χ̃(Δ_F)≡0` (fibre nerve contractible). Reproduce: `python3
poset_topology_probe.py 5`.

---

## 7. Collatz note: topological obstruction to a section (brief's optional ask)

The brief asks whether there is a topological obstruction to a **section** of the
Collatz map on the boundary of the binary tree / `2`-adic integers `ℤ₂` (or the
profinite `Ẑ`). Reading `collatz/theory/transfer_operator.md`, the live structure
is the **projective system** `P_n → P_{n-1} → ⋯ → P_1` of transfer operators on
`(ℤ/3^nℤ)^×` (§3.1 there: nested invariant subspaces `V^{(1)}⊂⋯⊂V^{(n)}`), with
the mod-3 obstruction the rank-1 block with eigenvector `(1/3,2/3)`.

**The topological reframing (speculative, plausibility 2/5).** A projective system
of finite sets `{U_n}` with the Syracuse maps is a **profinite dynamical system**
on `lim←U_n = ℤ₃^×` (the `3`-adic units). "Natural density on units" is a *section*
of the projection `ℤ₃^× → (ℤ/3)^×` that is invariant under the Syracuse map. The
transfer-operator finding "no scalar tilt gives `(1/2,1/2)`" (Prop 3.1 there) is
**exactly a cohomological obstruction to a continuous invariant section**: the
mod-3 marginal `(1/3,2/3)` is a non-trivial class in `H^1` of the profinite system
with the Syracuse `ℤ`-action (a `1`-cocycle that is not a coboundary — no
coordinate change kills it). This is **non-moment** (it is the *exact* `π_n`
structure, not a mixing rate) and matches the brief's "exploit the exact `π_n`,
not a spectral-radius bound."

**Concrete first step.** Compute the **Čech/group cohomology** `H^1` of the
inverse system `(U_n, P_n)` with the `(ℤ/2)`-action `k mod 2` (the parity of
`ν₂(3N+1)` that drives the mod-3 block). The claim to test computationally (the
probe in `transfer_operator.py` already builds `P_n|_V`): the obstruction class
`[(1/3,2/3) − (1/2,1/2)]` is **non-zero in `H^1` for every `n` and is the image of
a single generator** — i.e. the obstruction is `1`-dimensional and `n`-independent,
matching the rank-1 block. If so, "Collatz natural density" is blocked by a
*single explicit cohomology class*, the topological avatar of Prop 3.1. **This does
not lower any wall** — like the transfer-operator note, it is a sharper *statement*
of the obstruction (now as `H^1`), not a way through. Honest plausibility **2/5**;
its value is identifying the obstruction as cohomological, which suggests the
*real* lever is a **larger structure group** (the full `2`-adic `GL` action, not
scalar tilts) under which the class might become a coboundary — the analogue of
§5's "enlarge the object so the obstruction moves."

---

## 8. Bottom line

The poset-topology invariants are the **right kind** of object for the brief —
genuinely non-moment, non-symmetric, escaping the flat-minimization barrier (§2,
cube sanity passes: `μ=(−1)^k`, sphere homotopy). But the *invariant* layer dies on
a **different** wall — the cone (§4, `μ` fixed while abundance 0.5→0.875) — and the
*fibre-nerve* layer dies on contractibility-by-the-top (§4.1). The **single live
thread** is a **relative / discrete-Morse / Quillen-fiber** statement on the
`T`-deleted fibre complex, **restricted to a cone-blocked class** (upper-semimodular),
where `|μ_L|` weakly forces abundance in the data (§3) and Quillen could in
principle convert `μ_L≠0` into a heavy fibre (§5). Plausibility **2/5** overall,
**3/5** for that one thread. For Collatz, the topological content is a
**cohomological restatement** of the exact `π_n` / mod-3 obstruction as a non-trivial
`H^1` class (§7), non-moment but wall-preserving; the only forward lever is
enlarging the structure group. **No proof claimed. `[NOVELTY UNVERIFIED]`.**
