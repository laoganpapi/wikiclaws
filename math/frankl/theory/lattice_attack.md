# Lattice-structural attack on Frankl's union-closed conjecture

**Author:** Alex Ye (AI assistance disclosed separately)
**Status:** `[partial result + sharp obstruction — Step-1 certified; PRIOR-ART CHECK PENDING on every claim]`
**Date:** 2 June 2026
**Companion code:** `frankl/experiments/lattice.py`, `lattice_sweep.py`,
`lattice_analyze.py`, `lattice_minab.py`, `lattice_cone.py`,
`lattice_parametric.py`.
**Run log:** `frankl/experiments/data/lattice_attack_run.txt`,
`data/lattice_sweep_n{0..5}.jsonl`. Tests:
`tests/test_uc.py::TestLatticeAttack` (9 tests, all pass).
**Cross-ref:** `survey.md` §1.2 (Poonen), §7.5 (ignored lattice/graph structure);
`open_problems.md` A.2, E.1–E.5, F.2; `vector1_…md`, `vector3_…md` (why entropy
caps at ψ); `shared/dead_ends.md`.

> **What this is.** A genuinely different angle from the entropy method (which our
> project showed is provably capped at ψ = (3−√5)/2). We use the **order/lattice
> structure** that the entropy proofs discard. The honest outcome is the realistic
> one the brief anticipated: **a sharp obstruction** — *abundance is not a function
> of the lattice* — together with **one clean conditional lattice bound**
> (`abundance ≥ height/|L|`, tight on chains; certifies Frankl for tall lattices).
> No general bound. Every claim is validated on all 29,723 UC families with |F|≥2,
> n≤5, and the obstruction is backed by an **exact construction** valid for all n.

> **Honesty flags.** The literature is network-blocked this session; novelty is
> uncheckable. **Every statement below is marked [PRIOR-ART CHECK PENDING].** The
> conditional bound is elementary and very probably folklore / subsumed by
> chain-condition results (Colbert 2024, and Frankl-for-chains is classical); it is
> recorded as an internal certificate, **not** claimed new. Poonen's exact
> statement is reproduced from `survey.md` and marked **[CONSTANT/STATEMENT
> UNVERIFIED]** (primary source inaccessible).

---

## 1. The lattice formulation, set up precisely

### 1.1 A union-closed family is a join-semilattice

Let `F ⊆ 2^[n]` be union-closed: `A, B ∈ F ⇒ A ∪ B ∈ F`. Order `F` by inclusion
`⊆`. Then `(F, ⊆)` is a **join-semilattice** with **join = ∪**: for `A,B ∈ F`,
the least upper bound is `A ∪ B ∈ F`.

To get a **lattice** `L` we adjoin a bottom when needed: set
`L = F ∪ {∅}` (∅ is the unit for ∪, so `L` is still union-closed and is the same
poset with a guaranteed minimum `0̂ = ∅`). A finite join-semilattice with a
minimum is automatically a lattice: the **meet** `a ∧ b` is the join of all common
lower bounds (the set of common lower bounds is nonempty — it contains `0̂` — and
join-closed, so it has a top, which is the meet). The top of `L` is
`T = ⋃F`. **Code:** `lattice.as_lattice`, `lattice.meet_in_L`.

> **Caveat — meet ≠ intersection.** The lattice meet in `L` is generally **not**
> set-intersection: `A ∧ B = ⋃{X ∈ L : X ⊆ A, X ⊆ B}`, which can be a proper
> subset of `A ∩ B` (and may even be `∅` when `A ∩ B ∉ L`). Equality of meet and
> ∩ holds iff `L` is closed under intersection, i.e. iff `L` is **distributive**
> as a sublattice of `2^[n]`. This is the first place where lattice structure and
> set structure diverge, and it drives §4.3. (Verified: `lattice.meet_in_L` vs ∩.)

### 1.2 Join-irreducibles

An element `j ∈ L` is **join-irreducible** (a JI) if `j ≠ 0̂` and `j` has exactly
one lower cover (equivalently `j ≠ a ∨ b` for any `a, b < j`). In `L = (F, ∪)` the
JIs are the members of `F` that are **not** the union of strictly smaller members.
**Code:** `lattice.join_irreducibles` (elements with a unique lower cover).

By **Birkhoff's theorem** (true in every finite lattice) every `x ∈ L` is the join
of the JIs below it: `x = ⋁{j ∈ JI(L) : j ≤ x}`. The map
`φ(x) = {j ∈ JI(L) : j ≤ x}` is therefore **injective** (verified). It is a
**join-embedding into `2^{JI(L)}`** (so `{φ(x)}` is union-closed) **iff `L` is
distributive** — for non-distributive `L`, `φ(a ∨ b) ⊋ φ(a) ∪ φ(b)` can be strict,
so the Birkhoff image need not be union-closed. (Verified: `φ`-image is UC for B2,
chains; **not** UC for M3, N5 — `lattice_minab` / the §1 probe.)

### 1.3 The Poonen lattice formulation **[CONSTANT/STATEMENT UNVERIFIED]**

Reproduced from `survey.md` §1.2 (Poonen 1992; the primary source is inaccessible
this session, so the exact statement is unverified):

> **Poonen (1992), lattice form.** Every finite lattice `L` with `|L| > 1` contains
> a **join-irreducible** `j` such that `j ≤ x` for **at most** `|L|/2` elements
> `x ∈ L`. Poonen proved this is **equivalent** to FUCC.

Write `↑j = {x ∈ L : j ≤ x}` (the **principal filter** of `j`) and
`|↑j|` its size — the **Poonen frequency** of `j`. Poonen asks for a JI with a
**small** filter. **Code:** `lattice.principal_filter_size`,
`lattice.poonen_min_filter`.

> **The equivalence is GLOBAL, not per-family.** Poonen ⇔ FUCC is a statement about
> the two *families of statements* (all lattices vs all UC families), not a
> per-object identity. On a *fixed* UC family `F`, "Frankl on `F`" (some ground
> element in ≥ |F|/2 sets) and "Poonen on `L=(F,∪)`" (some JI with |↑j| ≤ |L|/2)
> are **different** statements that happen to both hold. The bridge is the
> realization direction (§1.4). (Verified: both hold, with the expected
> `|L|`-vs-`|F|` threshold difference, on all 29,723 families; 0 Poonen
> violations, 113 Poonen-tight.)

### 1.4 The ground-set ↔ lattice dictionary (the load-bearing correspondence)

Fix a UC family `F` (with `∅ ∈ F`, so `F = L`). For a ground element `x ∈ [n]`
define its **fibre** `Fib(x) = {A ∈ F : x ∈ A}`. Then (all verified exactly,
`lattice_minab`/§1 probe over 766 (x,F) pairs, n≤4):

* **`Fib(x)` is always a filter** (up-set) of `L`: `A ⊇ B ∋ x ⇒ A ∋ x`.
* Let `m_x = ⋀ Fib(x)` be the lattice-meet of the fibre. **`Fib(x) = ↑m_x`
  (a principal filter) iff `x ∈ m_x`.** When `x ∈ m_x`, `m_x` is a
  **join-irreducible** and `freq(x) = |Fib(x)| = |↑m_x|`.
* **When `x ∉ m_x`** (possible only if `L` is non-distributive), `Fib(x)` is a
  **non-principal** filter — a union of several principal filters — and `x`
  corresponds to **no single JI**. (Exactly the 316 of 766 pairs where `x ∉ m_x`;
  these are precisely the mismatch cases. Example: every ground element of M3.)

So the precise content of "ground-set element ↔ join-irreducible" is:

> **Dictionary.** Ground elements `x` with `x ∈ m_x` (equivalently: `Fib(x)` is a
> principal filter) are in bijection with a subset of the join-irreducibles of `L`,
> and there `freq(x) = |↑j|`. In a **distributive** lattice **all** ground elements
> are of this type and the bijection is onto the JIs (Birkhoff); this is why
> Poonen ⇔ Frankl is transparent for distributive `L` but requires the global
> realization argument in general.

Consequently:
$$
\mathrm{abundance}(F) \;=\; \max_x \frac{|\mathrm{Fib}(x)|}{|F|}, \qquad
\mathrm{Fib}(x)\ \text{a filter of }L. \tag{1.1}
$$
The abundance is the largest **filter density** over filters that arise as ground-
element fibres. **Which filters arise — i.e. how ground elements label the lattice
— is data NOT contained in the abstract lattice `L`.** This single sentence is the
seed of the obstruction (§4).

---

## 2. The concrete question and the toolkit

**The question (brief §2).** Does a structural parameter of the lattice — height,
number of join-irreducibles, width (max antichain), modularity/semimodularity
defect — yield an abundance bound? Specifically: **is there an element whose
abundance ≥ 1/2 forced by lattice structure rather than entropy?**

**Toolkit.** `lattice.py` computes, for any UC `F`: the lattice `L`, the cover
(Hasse) relation, join-/meet-irreducibles, atoms, principal-filter sizes, the
Poonen minimum, **height** (longest chain, in edges), **width** (max antichain via
Dilworth/bipartite matching), and the **distributive / modular / lower-semimodular
/ upper-semimodular** flags. Validated on the textbook lattices **B2** (distributive),
**M3** (modular, non-distributive, semimodular both ways), **N5** (non-modular,
neither semimodular), chains, and Boolean cubes — all flags correct
(`tests::test_known_lattice_invariants`).

---

## 3. A clean conditional lattice bound: `abundance ≥ height/|L|`

This is the one genuine *positive* lattice fact extracted. It is elementary and
**[PRIOR-ART CHECK PENDING] — almost surely folklore / subsumed by chain-condition
results**; recorded as an internal certificate, not claimed new.

> **Proposition 3.1 (height bound).** For every union-closed `F` with `|L| ≥ 2`,
> $$ \mathrm{abundance}(F)\ \ge\ \frac{\mathrm{height}(L)}{|L|}. $$
> Moreover the certifying element is explicit: any `x` in the first atom of a
> longest chain.

**Proof.** Let `∅ = c_0 ⋖ c_1 ⋖ ⋯ ⋖ c_h = T` be a longest chain in `L`, of length
`h = height(L)`. The atom `c_1` is nonempty; pick any ground element `x ∈ c_1`.
Since `c_1 ⊆ c_2 ⊆ ⋯ ⊆ c_h`, we have `x ∈ c_i` for every `i ≥ 1`, so
`Fib(x) ⊇ {c_1, …, c_h}` and `freq(x) ≥ h`. Therefore
`abundance(F) = max_y freq(y)/|F| ≥ h/|L|` (using `|F| = |L|` when `∅ ∈ F`; if
`∅ ∉ F` then `|F| = |L| − 1` and the bound only improves). ∎

**Code & validation.** `lattice.height_lower_bound_witness` returns
`(x, freq_x, height)` with `freq_x ≥ height`. **Step-1: zero violations of
`abundance ≥ height/|L|` over all 29,723 UC families (|F|≥2, n≤5)**
(`data/lattice_attack_run.txt`; `tests::test_height_lower_bound`).

> **Corollary 3.2 (Frankl for tall lattices).** If `2·height(L) ≥ |L|` then
> `abundance(F) ≥ 1/2`. This covers **all chains** (where the bound is **tight**:
> a chain `C_h` has `abundance = height/|L| = h/(h+1)`), and more generally any
> lattice whose longest chain meets at least half of `L`. **Step-1:** all 1,947
> tall families (`2·height ≥ |L|`) at n≤5 satisfy `abundance ≥ 1/2`, min exactly
> `0.5` (`tests::test_height_bound_tight_on_chains`).

**Honest scope.** The bound is **weak**: `height/|L|` exceeds `1/2` only for
tall/thin lattices and is `≪ 1/2` for wide ones (e.g. `B_k`: `height/|L| = k/2^k`).
It does **not** approach a general bound, and it is **not** the entropy method's
ψ in disguise — it is a purely order-theoretic counting fact the entropy method
never produces. Its value is (i) it is a *structural* certificate independent of
the capped entropy machinery, and (ii) it makes precise *which* lattices are
"easy from the order side." It does not, and cannot (by §4), extend to a
constant-factor improvement over `1/2` for general lattices.

---

## 4. The sharp obstruction: **abundance is not a lattice invariant**

This is the main deliverable. We show that **no function of the abstract lattice
`L` — and a fortiori no coarse invariant (height, width, #JI, #MI, #atoms,
modularity/semimodularity flags) — controls abundance**, by exhibiting
lattice-isomorphic UC families with wildly different abundance. The witness is an
**explicit construction valid for all `n`**, so the obstruction does not depend on
the n≤5 enumeration being complete.

### 4.1 The universal-element **cone** construction

> **Definition (cone).** Let `G ⊆ 2^[n]` be any UC family with `∅ ∈ G`. Pick a
> fresh ground element `z = n`. Define
> $$ \mathrm{cone}(G)\ :=\ \{\varnothing\}\ \cup\ \{\,A \cup \{z\} : A \in G,\ A \neq \varnothing\,\}. $$
> (Keep the bottom; adjoin `z` to every nonempty member of `G`.)

> **Proposition 4.1 (cone preserves the lattice, destroys abundance).**
> 1. `cone(G)` is union-closed.
> 2. `cone(G)` is **lattice-isomorphic** to `G` (via `∅ ↦ ∅`, `A ↦ A ∪ {z}`,
>    which is an order-isomorphism preserving joins). Hence **every lattice
>    invariant of `cone(G)` equals that of `G`** — same `|L|`, height, width,
>    #JI, #MI, #atoms, and the same distributive/modular/lsm/usm flags.
> 3. `abundance(cone(G)) = (|G|−1)/|G| = 1 − 1/|L|`, attained at `z`
>    (which lies in every member except `∅`).

**Proof.** (1) For `A,B ∈ G` nonempty, `(A∪{z}) ∪ (B∪{z}) = (A∪B)∪{z}` and
`A∪B ∈ G` (G union-closed); unions with `∅` are trivial. (2) The map is a
bijection `G → cone(G)` that preserves `⊆` in both directions and sends `∪` to
`∪` (the extra `z` is shared), hence a lattice isomorphism. (3) `z ∈ A∪{z}` for
all nonempty `A`, so `freq(z) = |G|−1`; no element can beat that since `z` is in
everything but the bottom. ∎

**Step-1 (exhaustive).** Over **all 206** UC families `G` (`∅ ∈ G`, `|G| ≥ 2`) at
n≤4, the conjunction (UC ∧ lattice-iso ∧ `abundance = 1−1/|L|`) holds with
**0 failures** (`lattice_cone.check_construction`;
`tests::test_cone_construction_exhaustive_small`).

### 4.2 The minimal clean witness pairs (Boolean lattices)

The cleanest instances realize the **Boolean lattice `B_k`** at abundance exactly
`1/2` (the standard cube) and at `1 − 1/2^k` (its cone):

| lattice | LOW realization | abundance | HIGH realization | abundance |
|---|---|---|---|---|
| `B_2` (|L|=4) | `2^[2]` | **0.5000** | `cone(2^[2])` | **0.7500** |
| `B_3` (|L|=8) | `2^[3]` | **0.5000** | `cone(2^[3])` | **0.8750** |
| `B_4` (|L|=16) | `2^[4]` | **0.5000** | `cone(2^[4])` | **0.9375** |
| `B_5` (|L|=32) | `2^[5]` | **0.5000** | `cone(2^[5])` | **0.9688** |

Both columns realize the **same abstract lattice** (`exact_lattice_iso` returns
`True`) with **literally identical** `LatticeInvariants`
(`tests::test_cone_is_lattice_iso_and_pushes_abundance_up`). Explicitly, the
`B_3` pair, both containing `∅` so `F = L`:

* LOW: `F₁ = 2^[3] = {∅,{0},{1},{2},{0,1},{0,2},{1,2},{0,1,2}}`, abundance **0.5**;
* HIGH: `F₂ = {∅} ∪ {S∪{3} : ∅≠S⊆{0,1,2}}`, abundance **0.875** (element `3`).

`Invariants(F₁) = Invariants(F₂)` exactly, yet abundances differ by `0.375`.
(`tests::test_abundance_not_determined_by_invariants`.)

> **Conclusion 4.2.** Abundance is **not** a function of the lattice. The *only*
> lattice-invariant lower bound on abundance that can possibly hold is the one
> Poonen already encodes (and that is *equivalent* to FUCC, hence no shortcut). In
> particular **no coarse invariant forces abundance above `1/2`** — the cone fixes
> every coarse invariant while driving abundance to `1`.

### 4.3 Coarse invariants do not even control the **minimum** abundance

One might hope that, while a *single* lattice spreads abundance over `[≈½, 1]`, the
*minimum* over realizations, `minab(L) := min{abundance(F') : F' ≅ L}`, is
controlled by coarse invariants (Poonen ⇔ `minab(L) ≥ 1/2` always). It is not.

Grouping the n≤5 families with `∅ ∈ F` into **true lattice-isomorphism classes**
(strong 1-WL fingerprint on the cover digraph + an **exact** back-tracking
isomorphism check, `lattice_minab.exact_lattice_iso`), and bucketing classes by
their coarse-invariant signature:

> **Finding 4.3 (Step-1).** Among the 235 coarse-invariant signatures (|L|≤12) that
> host ≥2 non-isomorphic lattices, **112 host lattices with different `minab`**.
> Sharpest witness: the coarse signature
> `(|L|=9, height=4, width=3, #JI=4, #MI=4, #atoms=3, modular=F, distributive=F,
> lsm=F, usm=F)` hosts lattices with `minab` ranging from **0.5556 to 0.7778**
> (spread `0.222`). So the coarse invariants do not determine even the *minimum*
> achievable abundance. (`lattice_minab.main`.)

### 4.4 Refuting the apparent "floors" in the raw n≤5 statistics

The raw sweep (`lattice_analyze` part A/B) shows *apparent* floors — e.g.
"width ∈ {4,5} ⇒ abundance ≥ 0.57", "#JI ≥ 6 ⇒ abundance ≥ 0.53", "non-modular ⇒
abundance ≥ 0.516". **These are small-`n` artifacts, not structural bounds**, and
the parametric families kill them:

> **Finding 4.4 (Step-1).** The Boolean lattices `B_k` have **abundance exactly
> `1/2` for every `k`**, while `#JI = k → ∞`, `width = C(k,⌊k/2⌋) → ∞`,
> `height = k → ∞`. Hence **no monotone function of (height, width, #JI) can lower-
> bound abundance above `1/2`**. (`lattice_parametric`;
> `tests::test_boolean_lattices_stay_at_half`.) The n≤5 "floors" arise only because
> the small-abundance distributive witnesses of a given (width, #JI) first appear
> at `n` larger than 5 (e.g. the width-`C(k,⌊k/2⌋)` cube `B_k` needs `n=k`).

Note the apparent "floor" of `0.6` for the **modular-non-distributive** class is
the same kind of artifact: it is `M3`-driven (`M_t` lattices have abundance
`t/(t+1) > 1/2`), but modular-non-distributive lattices can be **coned** to push
abundance up *and* producted to push it toward (but not below) `1/2`; the class
minimum at n≤5 is simply not yet the asymptotic one. We do **not** claim a
modular-class improvement.

### 4.5 Why this is the *right* obstruction (relation to the entropy cap)

The entropy method caps at ψ because the only union-closure input it uses is the
zeroth-order fact `A∪B ∈ F` (a cardinality constraint), and the chain-rule slack
`Δ₂` that a Shearer move would recapture is a *correlation* quantity union-closure
does not lower-bound (`vector1_…md`, `vector3_…md`). The lattice attack asks
whether the *order* structure supplies what entropy cannot. The answer of §4 is a
matching negative at a **different** layer:

> **The order type of `L` is exactly the information the entropy method also lacks
> the right *labelling* of.** Abundance (1.1) is a property of how the ground set
> *labels* the join-irreducibles (which filters `Fib(x)` arise), and the cone shows
> this labelling is free given `L`. So **neither the entropy functional nor any
> lattice invariant sees the labelling**, and the labelling is exactly where
> abundance lives. This identifies the missing ingredient precisely (open problem
> F.2): a useful inequality must constrain the **JI-labelling / fibre filters**,
> not the abstract lattice and not the i.i.d. entropy.

---

## 5. Verdict and the most promising lattice sub-direction

### 5.1 Verdict

* **General lattice bound: NONE, and provably impossible from invariants.** §4 is a
  hard obstruction with an exact, all-`n` construction.
* **Conditional bound: `abundance ≥ height/|L|`** (Prop. 3.1), certifying Frankl for
  tall lattices (Cor. 3.2), tight on chains. **[PRIOR-ART PENDING; very likely
  folklore]**, not claimed new.
* **Poonen formulation** set up precisely (§1), with the exact ground↔JI dictionary
  (§1.4) and the global-equivalence caveat (§1.3). Poonen's statement itself
  **[UNVERIFIED]** (source blocked).
* **No false positive.** The apparent statistical floors (§4.4) are dissected as
  small-`n` artifacts and refuted by `B_k`. No number above `1/2` is claimed for any
  infinite class.

### 5.2 The single most promising lattice sub-direction for a future (network-enabled) pass

> **Constrain the fibre-filter labelling on a *fixed* structured lattice class where
> the cone is blocked.** The obstruction is powered by the freedom to attach a
> *fresh universal coordinate* `z`. That freedom is exactly what is **forbidden**
> in the classes where the lattice conjecture is already proven —
> **lower-semimodular** (Reinhold), **modular** (Abe), **geometric/distributive**
> (Poonen) — because adding a universal element typically breaks (semi)modularity or
> the geometric exchange axiom. The live program is therefore **not** "find an
> invariant" (dead, §4) but:
> 1. **Upper-semimodular lattices** (open problem E.2; Reinhold's lower-semimodular
>    proof does **not** dualize). Our toolkit computes the usm flag and the JI
>    filters; the concrete target is to prove a *filter-density* statement
>    `min_{JI} |↑j| ≤ |L|/2` directly from the **upper-covering (exchange)**
>    condition, where the cone obstruction is structurally unavailable. The fibre-
>    filter formulation (1.1) + the exact ground↔JI dictionary (§1.4) is the right
>    language for it.
> 2. **Bouchard's minimum-counterexample lattice conditions** (arXiv 2503.00277,
>    network-blocked here): cross our `minab`-over-realizations machinery
>    (`lattice_minab`) with his necessary conditions to test whether a minimal
>    counterexample's lattice can be coned/producted — possibly shrinking the search
>    or yielding a contradiction.
>
> Rationale: every *successful* lattice result in the literature restricts the
> lattice **class** (not an invariant), precisely because — as we now show
> rigorously — invariants alone are powerless. The first new brick is the
> **upper-semimodular** case, attacked through the JI-filter/exchange structure with
> the cone explicitly ruled out.

---

## 6. Reproduction & certification status

* **Step 1 (computational): PASS.**
  - `python3 lattice_sweep.py` → `data/lattice_sweep_n{0..5}.jsonl` (29,723
    families, |F|≥2, n≤5).
  - `python3 lattice_analyze.py` → class minima, candidate inequalities, Poonen
    check (0 violations), invariant-collision obstruction.
  - `python3 lattice_minab.py` → true lattice-iso classes, `minab` spreads,
    coarse-invariant-vs-`minab` obstruction (112 signatures).
  - `python3 lattice_cone.py` → exhaustive (C1–C3) verification (0 failures, n≤4)
    + Boolean witness pairs.
  - `python3 lattice_parametric.py` → `B_k` stays at `1/2`; floors refuted.
  - `pytest tests/test_uc.py::TestLatticeAttack` → 9 tests pass; full suite 57 pass.
  - Consolidated log: `data/lattice_attack_run.txt`.
* **Steps 2–4 (red-team / Lean / human): N/A — no new theorem is claimed.** The
  obstruction is a construction + exhaustive check (Step-1 complete). The
  conditional bound (Prop. 3.1) is elementary and flagged PRIOR-ART PENDING; if a
  future pass wishes to *publish* it as ours it would need Steps 2–4, but its near-
  certain folklore status means the correct action is a citation, not a claim.
* **No PENDING RED-TEAM claim**, by design: the deliverable is a negative
  (obstruction) plus a likely-known certificate.

**Bottom line.** The lattice angle does **not** beat the entropy method's reach, but
it produces a *clean, exact* obstruction the entropy work did not have:
**abundance is extrinsic to the lattice** (cone construction, identical invariants,
abundance `1/2` vs `1 − 1/|L|`), so no lattice invariant can bound it. The one real
lattice fact is the elementary `abundance ≥ height/|L|`. The honest next brick is
the **upper-semimodular class**, where the cone is structurally blocked.
