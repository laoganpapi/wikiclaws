# Category theory / topos / sheaf cohomology / persistent homology — non-moment directions for Frankl and Collatz

**Field cluster 11 (+ applied topology).** Generation-wave output.
**Status:** SPECULATIVE DIRECTIONS, not proofs. Every framing flagged
`[NOVELTY UNVERIFIED]`. Honest "why-not / aspirational" included where that is
the truthful answer.
**Companion code:** `sheaf_persistence_probe.py` (this dir). Runs on the
project's standard census (all 29,723 UC families, n≤5) reusing
`frankl/experiments/{enumerate,uc_family,lattice}.py`.
**Cross-ref:** `frankl/theory/join_irreducible_labelling.md` (fibres = filters;
cube = unique minab=½ extremizer), `frankl/theory/ji_overlap_inequality.md` (the
second-moment/overlap wall, Lemma 3.1 tautology), `collatz/theory/transfer_operator.md`
(the projective filtration `V^(1)⊂…⊂V^(n)`, the nilpotent `P_n−Π`).

---

## 0. The one honest sentence

Of the four objects the brief floats, **three degenerate** for a reason worth
recording (the cube is too topologically simple — its order complex and every
fibre are contractible), and **one survives as a genuinely non-moment structural
dichotomy** that the census confirms: *abundance hits the Frankl boundary ½ only
when the heavy fibre is a **representable / principal** co-presheaf*, and is
**strictly > ½ whenever it is not** (min 0.5556 over 11,886 families, n≤5). That
dichotomy is real, computed, and non-symmetric — but it reduces the hard case to
Poonen's join-irreducible statement rather than escaping it. Below: the object,
why it is non-moment, the computation, the validation, and the brutally honest
plausibility.

---

## 1. The categorical / sheaf / persistence objects

### 1.1 The lattice as a category; fibres as co-presheaves (setup)

`L = (F, ⊆, ∪)` is a finite poset, hence a (thin) category: one object per
`A∈F`, a unique arrow `A→B` iff `A⊆B`. Adjoin `0̂=∅`, so `L` is a bounded
lattice with top `T=⋃F`. For a ground element `x∈[n]` the **fibre**
`Fib(x)={A∈L : x∈A}` is an **up-set (filter)**, equivalently a **sub-co-presheaf
of the terminal `Set`-valued co-presheaf** — the characteristic function
`1_{Fib(x)} : L → {0≤1}` is **monotone** (order-preserving into the Sierpiński
poset `Ω`), i.e. it is a point of the **subobject classifier of the presheaf
topos `Ŝet^{L}`** restricted to monotone (open) subobjects. So the fibre system
`{Fib(x)}` is a family of **opens of the Alexandrov topology** on `L`.

- **abundance(F) = max_x μ(Fib(x))**, `μ` = uniform counting measure on `L`.
- **Frankl ⟺ some open `Fib(x)` has measure ≥ ½.**

This is the clean topos-theoretic restatement: Frankl asks whether the Heyting
algebra of opens `O(L)` (the filters of `L`) contains an open of the *special
form* `Fib(x)` with measure ≥ ½.

### 1.2 Object A (the survivor) — the **representability / principal** stratification of the heavy fibre

A filter `U` is **principal** (`U = ↑m`, has a minimum) **iff** the co-presheaf
`1_U` is **representable** (`= Hom_L(m, −)`), iff `1_U` is a **free / projective**
object in the relevant sense, iff its order complex `Δ(U)` is a **cone** (hence
contractible). Define the **structural type of `F`**:

> `type(F) := ` *is the heavy fibre `Fib(x*)` (x* = argmax) **principal**?*

This is a Boolean, non-numeric, non-symmetric invariant of the fibre system —
it depends on the *order structure* of the argmax fibre, not on any average.

### 1.3 Object B (the cellular sheaf) — the constant sheaf on `Δ(L)` and its fibre-twist

Following **Curry (2014), *Sheaves, Cosheaves and Applications*** and
**Hansen–Ghrist** cellular sheaf cohomology: put the **cellular sheaf `𝓕_x`**
on the order complex `Δ(L)` (or the Hasse 1-skeleton) whose stalk over a chain
`σ` is `𝔽₂` if `min(σ)∈Fib(x)` (equivalently the whole chain lies in the
up-set), `0` otherwise, with identity restriction maps where both stalks are
`𝔽₂`. Then `H⁰(Δ(L); 𝓕_x) = H⁰(Δ(Fib(x)); 𝔽₂)` and the higher
`Hᵏ` are the reduced cohomology of the **order complex of the fibre**. So the
sheaf cohomology of the fibre-twisted constant sheaf **is** the simplicial
(co)homology of the sub-poset `Fib(x)` — the object we actually compute in §3.

### 1.4 Object C (persistence) — the `|·|`-filtration of `Δ(L)`

Filter `Δ(L)` by the **cover-number** `c(A) = #{x : A∈Fib(x)} = |A|` (the
"ground multiplicity" of a lattice element): `K_t = ` full subcomplex of `Δ(L)`
on `{A : |A| ≤ t}`. This is a genuine **sublevel filtration** (Edelsbrunner–
Harer persistence): as `t` grows we glue in heavier elements and the
**persistence barcode** records *in what order the lattice assembles by ground-
multiplicity*. The barcode is a non-symmetric, order-sensitive invariant.

### 1.5 Object D (Collatz) — persistence/coalgebra of the return-time structure

For Collatz: the brief's transfer operator `P_n` already exhibits a **projective
filtration of invariant subspaces** `V^(1)⊂V^(2)⊂…⊂V^(n)=ℝ^{U_n}` (the mod-`3^k`
coset indicators), and `P_n−Π` is **nilpotent of index `n`** (`transfer_operator.md`
§3.1, `perp_gap.md`). This is *exactly* a **filtered / graded object** — a
candidate for persistence of the spectral filtration, or for a **coalgebraic**
invariant of the Syracuse dynamics (final-coalgebra / behavioural-equivalence of
the residue automaton). See §6.

---

## 2. Why these are NON-MOMENT (the barrier-escape argument)

The proven Frankl barrier: *every symmetric convex moment of the frequency
vector is flat-minimized by the Boolean cube at ½* (`join_irreducible_labelling.md`,
`ji_overlap_inequality.md`). The mechanism is that the cube's frequency vector is
**flat** (all `freq=|L|/2`), so any symmetric convex average sits at its minimum.
The overlap/second-moment lever dies by the same flatness plus Lemma 3.1
(`↑a∩↑b=↑(a∨b)` is an exact identity, zero slack).

**Cohomology and persistence are not averages.** Concretely:

1. **A moment is `Σ_x φ(freq(x))` for convex `φ`** — a symmetric function of the
   multiset of fibre *sizes*. Sheaf cohomology `H*(Δ(L);𝓕_x)` and the
   persistence barcode are **not functions of the size multiset at all**: two
   families with the *same* frequency vector can have *different* barcodes /
   different fibre homotopy types (the order in which elements glue differs).
   So they live outside the class the barrier covers — **this is the precise
   sense in which they escape it.**

2. **The cube's topology is special, not flat-symmetric.** What is the cube's
   sheaf cohomology / barcode?
   - **Cube fibre cohomology:** the cube `2^[k]` is **distributive**, so every
     fibre `Fib(x)=↑{x}` is **principal** ⇒ `Δ(Fib(x))` is a **cone** ⇒
     `H̃*(Δ(Fib(x)))=0`. *Verified, §3: all 5 cubes have heavy-fibre reduced
     Betti = 0.*
   - **Cube order complex:** `Δ(B_k)` (proper part, i.e. the open interval
     `(0̂,T)`) is homotopy equivalent to `S^{k-2}` (a `(k-2)`-sphere) — the
     classical fact that the Möbius function of the Boolean lattice is `(−1)^k`,
     `H̃_{k-2}(Δ(B_k))=𝔽₂`, all other reduced groups 0. So the cube **is**
     topologically marked — by a *sphere*, the most symmetric possible class.
   - **Cube barcode (the `|·|`-filtration):** `K_t` adds all `|A|≤t`; this is the
     `t`-skeleton-by-rank of the cube's order complex. Its barcode is the
     **rank-filtration barcode of a `(k-2)`-sphere** — a single long `H_{k-2}`
     bar appearing at `t=k` (the top arrives). Non-trivial, and *different* from
     a generic lattice's barcode.

   The key asymmetry: **the cube is flat in every *moment* but is a *sphere* in
   *homology*.** A moment cannot tell `B_k` from a relabelled non-cube of the
   same frequency vector; the **homotopy type of `Δ(L)` and of the fibres can**.
   That is the non-moment lever in one line.

3. **Object A is manifestly non-symmetric.** `type(F)` = "is the *argmax* fibre
   principal" depends on *which* element is heaviest and on the *order* structure
   of its fibre — it is not invariant under arbitrary symmetric operations on the
   frequency multiset. The census (§3) shows it is **not** a disguised moment:
   it strictly separates abundance-½ families from abundance-`>½` families.

---

## 3. The concrete first step (COMPUTED) — `sheaf_persistence_probe.py`

The probe computes, over **all 29,723 UC families (n≤5)**, reusing the project's
enumerator and lattice code:

- **(III/A) heavy-fibre principality** (representable co-presheaf? = filter has a
  minimum);
- **(II/B) the full reduced `𝔽₂`-homology of the heavy fibre's order complex**
  `Δ(Fib(x*))` (= the cellular-sheaf cohomology `H*(Δ(L);𝓕_{x*})` of §1.3),
  computed by exact boundary-matrix ranks over `𝔽₂` to the FULL dimension
  (no truncation — truncation gave spurious top classes in a first pass; fixed
  and sanity-checked: cube fibres and the M3 fibre are correctly contractible).

**Results (n≤5, full census).**

| invariant | value | min abundance | #(abundance < ½) |
|---|---|---:|---:|
| heavy fibre **principal** (representable) | 17,837 families | **0.5000** | 0 |
| heavy fibre **non-principal** | 11,886 families | **0.5556** | 0 |
| heavy fibre `Δ` reduced Betti total `= 0` (contractible) | 29,679 | 0.5000 | 0 |
| heavy fibre `Δ` reduced Betti total `= 1` | 43 | 0.5000 | 0 |
| heavy fibre `Δ` reduced Betti total `= 3` | 1 | 1.0000 | 0 |

**Boolean cubes `B_k` (k=1..5):** heavy fibre **principal**, reduced Betti **0**,
abundance **exactly 0.5000** — for every `k`.

> **Finding 3.1 (the survivor — a non-moment dichotomy).** Over n≤5:
> **abundance attains the Frankl boundary ½ ⟹ the heavy fibre is principal
> (representable).** Equivalently: **a non-principal heavy fibre forces
> abundance ≥ 0.5556 > ½** (11,886 witnesses, zero exceptions). The
> abundance-½ extremal stratum (cubes and friends) lies **entirely inside the
> "representable heavy fibre" cell.** `[NOVELTY UNVERIFIED]`

> **Finding 3.2 (why per-fibre cohomology alone is too weak).** The heavy
> fibre's *own* order complex is **contractible in 29,679/29,723 families**
> (only 44 have any reduced homology, and those are uniformly *high*-abundance,
> mean 0.80). A filter usually has a minimum or is a cone; its intrinsic
> cohomology rarely fires. **So Object B (the fibre-twisted constant sheaf) is
> not by itself a Frankl certificate.** The structural content is in the
> *principality* (Object A), not the higher cohomology.

This converts the abstract "sheaf on `L`" idea into a **sharp, verified,
non-symmetric stratification**: Frankl, restricted to its own extremal stratum,
is *exactly* the statement about **principal (representable) heavy fibres**.

---

## 4. Validation, and the honest obstacle

**Validation (passes):**
- Sanity: cube fibres and the M3 non-principal fibre have correct (contractible)
  homology after the full-dimension fix; `f₂`-rank boundary computation
  cross-checked by hand on `B_3, B_4, M3`.
- The dichotomy is **exact on the full census** (0 counterexamples / 29,723):
  abundance = ½ ⇒ heavy fibre principal.
- Consistent with `join_irreducible_labelling.md` H5 (cube = unique minab=½):
  the cube is distributive ⇒ all fibres principal ⇒ it sits at the *bottom* of
  the representable stratum at exactly ½.

**The honest obstacle (why this is a direction, not a proof).** Finding 3.1 says
the *hard* case (abundance = ½) is the **principal/representable** one — but in
that case `Fib(x*) = ↑m` and `μ(Fib(x*)) = |↑m|/|L|`, which is **exactly the
Poonen join-irreducible quantity** (`join_irreducible_labelling.md` §2). So the
categorical stratification **localizes** Frankl to "every lattice has a
join-irreducible `j` with `|↑j| ≥ |L|/2`" on the principal stratum — i.e. it
**reduces the hard case to Poonen**, which is the *known* equivalent form, not an
escape. The non-principal stratum is handled (it is strictly > ½, automatically),
but that was already the easy side. **The lever relocates the difficulty into a
categorical cell; it does not yet add a new inequality inside that cell.**

What *would* make this escape the barrier (the genuinely open, aspirational
part): a **cohomological obstruction on the principal stratum** — e.g. a sheaf on
`L` whose `H¹` *vanishes iff* some principal fibre is heavy, turning Frankl into
"`H¹(L;𝓢)=0`". The natural candidate is the **cellular sheaf of "local Frankl
budgets"** (stalk = local abundance deficit, restriction = the union-closure
constraint); Frankl would be `H⁰`-globalization of local ≥½ data. **This sheaf
is not yet constructed**; building it (with restriction maps that genuinely
encode union-closure, not just the poset) is the precise next brick. Until then,
Object B's higher cohomology is provably inert (Finding 3.2), so the claim is:
**the *gluing* (cohomological) content must come from a sheaf whose restriction
maps see union-closure — which Object B's constant sheaf does not.**

---

## 5. Plausibility, failure modes, novelty

**Plausibility: 2 / 5 (Frankl).** The non-moment dichotomy (Finding 3.1) is real,
verified, and genuinely outside the moment-barrier class — that part is solid and
mildly interesting. But it reduces the hard case to Poonen rather than cracking
it, and the higher cohomology that would add *new* gluing content is provably
zero for the obvious (constant) sheaf. A *useful* sheaf with union-closure-aware
restriction maps is plausible to define but its `H¹` controlling abundance is
**aspirational** — no construction in hand.

**Failure modes:**
1. **Contractibility collapse (confirmed, Finding 3.2).** Filters are usually
   cones; the constant sheaf's cohomology is almost always zero — it cannot be a
   certificate. *Mitigation:* a non-constant sheaf encoding union-closure in the
   restriction maps; unbuilt.
2. **Poonen reduction (confirmed, §4).** On the extremal stratum the invariant
   *is* `|↑m|/|L|` — the known equivalent. No new slack unless a cohomological
   obstruction is added on that stratum.
3. **Möbius = Euler-char trap.** The cube's `Δ(L)` is a sphere
   (`H̃_{k-2}=𝔽₂`), but `χ̃(Δ(L)) = μ_L(0̂,T)` is a *single integer* and is a
   linear (Euler-characteristic) functional — at risk of being a disguised
   alternating moment. The *barcode* / homotopy type carries more than `χ̃` and
   is the part that escapes; one must use the full barcode, not just `μ`.
   (The companion `poset_topology_probe.py` already explores `μ`/crosscut Euler
   char; this note's contribution beyond it is the **fibre-level
   principality/cohomology** and the persistence framing, not `μ_L` again.)
4. **Persistence may be a moment in disguise.** The `|·|`-filtration barcode's
   *Betti curve* `t ↦ dim H_*(K_t)` integrates to Euler characteristics — if one
   only reads Betti numbers per level, that can collapse to moments. The escape
   requires the *bars* (birth–death pairs / the bottleneck or persistence-
   landscape metric), which are genuinely non-linear and non-symmetric.

**Collatz (Object D): plausibility 2 / 5, mostly aspirational.** The projective
filtration `V^(1)⊂…⊂V^(n)` and nilpotent `P_n−Π` are *literally* a filtered/graded
object — the right shape for a persistence or coalgebraic invariant. The concrete,
*actionable* sub-step (already half-done in `_probe/jordan_probe.py`): test
whether the **Jordan/nilpotent flag of `P_n−Π` coincides with the mod-`3^k` coset
filtration** — if so, the obstruction is exactly a **graded persistence module**
whose barcode is the `(0,⅓,⅔)` mod-3 marginal lifted through scales, a clean
*structural* invariant of the non-uniform `π_n`. The genuinely new (aspirational)
ask: a **final-coalgebra / behavioural** invariant of the Syracuse residue
automaton whose non-triviality is the mod-3 obstruction — *not constructed*; it
would need the automaton's bisimulation quotient to be computed and related to
`π_n`. Honest read: the persistence-of-the-nilpotent-flag step is computable and
worth doing; the coalgebraic invariant is hand-waving until a concrete functor is
named.

**Novelty.** `[NOVELTY UNVERIFIED]`. Cellular-sheaf cohomology (Curry,
Hansen–Ghrist), poset order-complex homology (`μ_L` = reduced Euler char,
Björner), persistence (Edelsbrunner–Harer) are all standard. The
**representable/principal stratification of the *heavy* fibre as a non-moment
Frankl invariant** is the flagged-new framing here; prior is moderate that the
"abundance-½ ⇒ principal heavy fibre" dichotomy is folklore via the Poonen
dictionary, but I did not find it stated. No proof, no constant > ½ claimed.

---

## 6. Reproduction & next bricks

```
cd math/ideas/generation
python3 sheaf_persistence_probe.py 5    # full census n<=5; prints the tables above
```

**Concrete next bricks (in increasing aspiration):**
1. *(buildable now)* Define the **union-closure cellular sheaf** `𝓢` on `Δ(L)`:
   stalk over chain `σ` = local abundance budget at `min σ`; restriction maps =
   the constraint `freq(x) ≥ Σ over JI-filters` of `(R)`. Compute `H⁰,H¹` and
   test whether `H¹=0 ⟺ ` a principal fibre clears ½. **This is the real test of
   whether sheaf cohomology adds anything beyond Object B's inert constant
   sheaf.**
2. *(buildable now, Collatz)* Extend `_probe/jordan_probe.py`: confirm
   `ker((P_n−Π)^k) = V^(n−k+1)` exactly over ℚ ⇒ the nilpotent flag **is** the
   coset persistence module; read its barcode.
3. *(aspirational)* A topos/site whose **sheaf cohomology globalizes local
   ≥½ data** for Frankl; a final-coalgebra behavioural invariant for Syracuse.
   Named here, not built.

**Step-1 (computational): PASS** — 29,723 families; the non-moment principality
dichotomy is exact (0 exceptions). **Steps 2–4: N/A** — no theorem claimed; this
is a direction with one verified structural finding and an explicit, honest
obstacle (Poonen reduction + constant-sheaf inertness). `[NOVELTY UNVERIFIED]`.
