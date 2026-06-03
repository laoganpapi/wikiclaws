# Generator-incidence (non-symmetric) attack on Frankl's union-closed conjecture

**Author:** Alex Ye (no AI on author line).
**Date:** 2026-06-03.
**Status:** `[NOVELTY UNVERIFIED — Birkhoff/Poonen generator (join-irreducible)
representation is classical (Birkhoff 1937, Poonen 1992); the singleton lemma
is folklore; the *invsize* generator-asymmetric pick rule is flagged new but is
PRESUMED FLAWED — it has no proof and is almost certainly a finite-n
coincidence. arXiv 403 this session.]`
**This is a NON-SYMMETRIC generator-incidence study — NOT a proof.**
**No proof of Frankl is claimed. No constant > ½ is claimed.**
**Companion code:** `frankl/experiments/generator_attack.py`.
**Data:** `frankl/experiments/data/genattack_n{0..5}.jsonl`,
`genattack_summary.{txt,json}`, `genattack_redteam.txt`.
**Cross-ref:** `join_irreducible_labelling.md` (the fibre=union-of-filters
identity, here read at the generator level), `ji_overlap_inequality.md`
(why the symmetric overlap moment is dead), `lattice_attack.md` §1.4 (the
ground↔generator dictionary, the cone), `PROGRESS.md` "BARRIER THEOREM",
`shared/dead_ends.md` (the 0.43/0.5 traps and all eight prior dead ends).

> **The barrier this attacks.** The project's BARRIER THEOREM: all eight prior
> methods (entropy, polynomial, Boolean-Fourier-quadratic, lattice-invariant,
> shadow, LP, second-moment, JI-overlap) reduce to a **symmetric convex moment
> of the frequency/fibre vector**, and every such moment is **flat-minimized by
> the Boolean cube at exactly ½**. No symmetric moment can prove Frankl. The
> needed ingredient must be **non-symmetric** — sensitive to *which* element is
> heavy and to the generator incidence structure. This note pursues exactly
> that: quantities built from the **generator incidence matrix** `M`, which are
> not symmetric in the ground elements.

> **One-paragraph verdict.** (1) The generator-incidence formula for abundance
> is exact and clean (§1), verified 0 violations on all 29,723 families. (2) The
> first non-symmetric candidate — "the **most frequent generator element** is
> ≥½-abundant" — is **FALSE** (356 failures, min 0.333; clean counterexample in
> §2). (3) The natural generator-weighted abundances (weight `g` by `|g|`,
> `1/|g|`, `|↑g|`, lower-cover count) all **fail as certificates AND give the
> cube slack** (they drop to `1/k` on `2^[k]`, not ½) — a *new* failure mode,
> opposite to the symmetric methods (§3). (4) One non-symmetric **pick rule**
> survives all n≤5 and ~660,000 larger-n tests with min exactly ½ and cube
> equality: the **combined singleton/invsize rule** (§4). Its provable half is
> the classical singleton case; its other half (the *invsize* argmax) **has no
> proof and is PRESUMED FLAWED** — I devote §5 to breaking it and explain (via
> non-separability) exactly why it is almost certainly a finite-n coincidence.
> (5) Net: the generator angle is the *right* non-symmetric language, but the
> barrier **extends** to every *separable* generator-asymmetric quantity I
> tried; the one surviving object is non-separable, has no proof, and is
> flagged accordingly (§6).

All numbers validated on **all 29,723 UC families with |F|≥2, n≤5** (orbit reps;
∅ adjoined so the generator picture is exact), plus the larger-n break attempts
in §5.

---

## 1. Generator-incidence formulation of abundance (Task a)

Fix `F` union-closed; adjoin `∅` so `L = (F, ⊆, ∪)` is a lattice. The
**generators** of `F` are
$$
G \;=\; \{\,m \in F : m \neq \varnothing,\ m \neq \textstyle\bigcup\{a \in F : a \subsetneq m\}\,\}
$$
— the members not expressible as a union of strictly smaller members. These are
exactly the **join-irreducibles** of `L` (Birkhoff). Then
$$
\boxed{\ F \;=\; \{\,\textstyle\bigcup S : S \subseteq G\,\}\ }\qquad(\textstyle\bigcup\varnothing=\varnothing),
$$
verified (the union-closure of `G` reproduces `F` exactly, 0/29,723 violations,
`closure_of_generators`). Encode `G` as the 0-1 **incidence matrix**
`M[g,x] = 1 ⟺ x ∈ g`, of shape `|G| × n`.

> **Identity 1.1 (exact abundance from `M` and the union-lattice).** For each
> ground element `x`,
> $$
> \mathrm{freq}(x) \;=\; \big|\{A \in L : x \in A\}\big| \;=\; \big|\mathrm{Fib}(x)\big|,
> \qquad
> \mathrm{abundance}(F) = \max_x \frac{\mathrm{freq}(x)}{|L|}.
> $$
> The fibre is reconstructed from the incidence matrix by the **union-of-filters
> identity**
> $$
> \boxed{\ \mathrm{Fib}(x) \;=\; \bigcup_{\,g \in G,\ M[g,x]=1\,} {\uparrow}g\ }
> \tag{R-gen}
> $$
> where `↑g = {A ∈ L : g ⊆ A}` is the principal filter of the generator `g`.
> *(Verified: 0 violations / 148,164 (x, F) pairs, n≤5; `generator_attack.py`,
> and the sweep asserts `abundance_from_generators == direct` per family,
> 0/29,723.)*

This is the same reconstruction `Fib(x) = ⋃_{j∈JI, x∈j} ↑j` of
`join_irreducible_labelling.md` (R), here phrased on the **generators /
incidence matrix** rather than the abstract JIs. The content of (R-gen) for the
attack: **abundance is a UNION (overlap) size of generator filters, not a
separable sum** of per-generator contributions. Every separable statistic of `M`
is therefore only a *proxy*, and §5 shows this is the decisive obstruction.

**Why this is non-symmetric.** Identity 1.1 reads off `M`, whose columns are the
ground elements. Permuting columns permutes the elements; the abundance is the
max over columns of a quantity (`|⋃ ↑g|`) that depends on *which* generators a
column hits and on *how their filters overlap*. Unlike the eight prior methods,
nothing here is averaged over `x`: we are allowed to privilege a particular
column. That is exactly the freedom the barrier says is needed.

---

## 2. The "most frequent generator element" heuristic is FALSE (Task b)

The simplest non-symmetric statistic is the **generator-element frequency**
(column sums of `M`):
$$
\mathrm{gfreq}(x) \;=\; \#\{g \in G : x \in g\} \;=\; \sum_{g} M[g,x].
$$
**Heuristic H-gfreq.** *The element `x*` maximising `gfreq` is ≥½-abundant in `F`.*

> **Finding 2.1 (H-gfreq is FALSE).** Over all 29,723 families: the
> `gfreq`-argmax element has true abundance `< ½` in **356** families; its
> minimum true abundance is **0.3333**. `gfreq` picks the genuinely most
> abundant element in only **20,909 / 29,723** families.
> *(`genattack_summary.txt`.)*

**The clean minimal counterexample** (smallest `|F|`, then fewest generators):
$$
G = \big\{\{2\},\ \{0,1,2\},\ \{3\},\ \{0,1,3\}\big\},\qquad
L = \{\varnothing,\{2\},\{3\},\{0,1,2\},\{0,1,3\},\{2,3\},\{0,1,2,3\}\},\ |L|=7.
$$
Every element `0,1,2,3` lies in exactly **two** generators, so `gfreq ≡ 2`
(flat) and the tie-break picks `x=0`. But the true frequencies are
`freq = (3,3,4,4)`: elements `2,3` are ≥½-abundant (`4/7 ≈ 0.571`), elements
`0,1` are not (`3/7`). **The incidence count is flat and blind**; the abundant
elements `2,3` are precisely the ones sitting in the *small* generators `{2}`,
`{3}`, which the raw count does not weight. Lesson: a bare generator-incidence
count is the wrong non-symmetric statistic — it ignores generator *size*.

---

## 3. Asymmetric generator-weighted abundances fail — and give the CUBE slack (Task b)

Generalize: weight each generator `g` by a structural `w(g)` (non-symmetric, not
element-symmetric) and define `Wab(x) = (Σ_{g∋x} w(g)) / (Σ_g w(g))`. Tested
weights: `w(g)=|g|`, `w(g)=1/|g|`, `w(g)=|↑g|` (Poonen filter size in `L`),
`w(g)=1+\#\{h∈G: h⊊g\}` (a generation-order rank).

> **Finding 3.1 (all four fail as standalone certificates — a NEW failure
> mode).** Each `max_x Wab(x)` drops to **0.200** on the cube `2^[5]` and fails
> `< ½` on 180–3,116 families. *(`genattack_summary.txt`.)* Crucially, **the
> cube does NOT saturate at ½**: on `2^[k]` (`k` singleton generators, each
> element in exactly one generator), `Wab(x) = w({x})/Σ_j w({j}) = 1/k` for
> every weight. So these statistics give the cube **slack `1/k → 0`, not ½**.

This is the **opposite** failure of the eight symmetric methods. The symmetric
moments are *flat-minimized at ½ by the cube* (the cube is their extremal). The
generator-weighted abundances instead **undershoot the cube to `1/k`**: the cube
is the *worst* case for them, because the cube's generators (singletons) are
maximally spread, so no element's generator-weight share exceeds `1/k`. By the
red-team discipline (a valid proof must give the cube *equality* at ½), **any
weighted-abundance functional that drops to `1/k` on the cube is immediately
disqualified** — it cannot be a Frankl certificate. The generator weights see
the cube as *least* abundant when it is exactly the threshold case; the mismatch
is structural and kills the whole "weighted abundance" family.

---

## 4. The one surviving non-symmetric object: the combined pick rule (Tasks b, c)

The lesson of §2–§3: a *value* certificate from a separable generator weight
fails (cube slack). But a **pick rule** — a non-symmetric *selector* of one
element, whose TRUE abundance we then read off — is not a moment and is not
disqualified by the cube (the cube has abundance exactly ½ at every element, so
*any* pick is tight there). I tested selectors built from `M`.

**The invsize score (size-inverse generator incidence).**
$$
\mathrm{invsize}(x) \;=\; \sum_{g \in G,\ x\in g} \frac{1}{|g|},
\qquad\text{with the exact identity}\quad \sum_x \mathrm{invsize}(x) = |G|
$$
(each generator spreads a total weight `1` over its elements). This privileges
elements in **small** generators — exactly what §2's counterexample showed is
needed.

> **The combined non-symmetric pick rule `[EXTRAORDINARY — PRESUMED FLAWED PENDING RED-TEAM]`.**
> - **(i) singleton branch:** if some generator is a singleton `{x}`, pick `x`;
> - **(ii) invsize branch:** otherwise pick `x = argmax_x invsize(x)`
>   (ties → smallest index).

> **Finding 4.1 (survives n≤5 with cube equality).** Over all 29,723 families
> the combined rule's picked element has true abundance `≥ ½` with **0 failures,
> minimum exactly 0.5, and 377 equality (=½) cases**, including every Boolean
> cube `2^[k]` (`comb_ab = ½` exactly, `k=1..5`). The two branches:
> - singleton branch: **23,741** families, 0 failures, min ½;
> - invsize branch (no-singleton): **5,982** families, 0 failures, min ½.
> *(`genattack_summary.txt`.)*

**Branch (i) is a theorem (the classical singleton case).** If `{x} ∈ F` then
the map `A ↦ A ∪ {x}` is an injection from `{A∈F : x∉A}` into `{A∈F : x∈A}`
(its image lands in `F` by union-closure and contains `x`; it is injective
because removing `x` is a left inverse on its image). Hence
`freq(x) ≥ |F|/2`, with **equality on the cube** (where `{x}∈F` for every `x`).
This is elementary and **folklore** (`[PRIOR-ART — NOT claimed new]`); it is
*not* the new content. It does, however, cover 23,741/29,723 families on its own.

**Branch (ii) is the genuinely non-symmetric, genuinely new — and PRESUMED
FLAWED — part.** On the 5,982 no-singleton families it selects the invsize
argmax, and that element is ≥½-abundant in every n≤5 case. The selector is
*authentically* non-symmetric: in **652** of the 5,982 no-singleton families the
invsize argmax is **not** the most-frequent element, yet it still lands ≥½
(`generator_attack.py` disagreement probe). So invsize is not a disguised
"pick the max frequency"; it is a structural selector off the incidence matrix
that happens, on n≤5, to always land in the abundant zone.

**Deletion/induction (Task c).** The singleton branch is exactly a non-symmetric
induction pivot: removing the singleton generator `{x}` and inducting on `F\{x}`
is the classical reduction. The invsize branch was tested as an inductive pivot
(remove the invsize-heaviest generator) but no inductive step closes — the
abundance of the deleted-generator subfamily does not control `F`'s in a usable
direction (the union-lattice changes nonlinearly under generator deletion). No
working asymmetric induction beyond the singleton case was found.

---

## 5. RED-TEAM: the invsize branch is almost certainly a finite-n coincidence (Task e)

Per the discipline (Frankl is OPEN; any apparent proof is presumptively WRONG),
I devote this section to **breaking** branch (ii). Summary in
`data/genattack_redteam.txt`.

**Break attempts (all 0 counterexamples, but bounded):**
1. **Exhaustive n≤5:** 5,982 no-singleton families, 0 failures, min exactly ½.
2. **Random no-singleton n=6,7,8** (generators size 2–4): **400,000** families,
   0 failures.
3. **Targeted near-extremal no-singleton** (`M_t` = all 2-subsets of `[t]`;
   `M3×M3` products; dense 2-generator graphs on `[5..7]`): **200,019**
   families, 0 failures, worst 0.5192.
4. **Exhaustive n=6**, generators of size ≤3, up to 4 generators: **57,560**
   distinct no-singleton families, 0 failures, worst exactly ½.
5. **Hand-built adversarial** families replicating the n=5 *singleton*-branch
   failure structure (an element in many small generators whose advantage is
   "unioned away") but *without* singletons: no counterexample.

**Why I nonetheless presume it FLAWED — the non-separability obstruction.** The
break attempts found nothing, but the *reason to distrust* is structural, not
empirical:

> **Finding 5.1 (no separable certificate underwrites the pick).** The candidate
> per-element inequality
> $$
> \mathrm{abundance}(x) \;\ge\; \frac{\mathrm{invsize}(x)}{|G|}\qquad(\forall x)
> $$
> is **FALSE** — **12 / 29,723** violations. So invsize does **not** certify
> abundance through any per-element separable bound. *(`generator_attack.py` C1
> probe.)*

> **Finding 5.2 (the true quantity is non-separable, by R-gen).** By Identity
> 1.1, `abundance(x) = |⋃_{g∋x} ↑g| / |L|` is the size of a **union** of
> generator filters. invsize is a **separable sum** `Σ_{g∋x} 1/|g|`. The argmax
> of a separable proxy has **no structural reason** to coincide with the argmax
> of a non-separable union size: the union size is depressed by *overlap* among
> the filters `↑g` (`g∋x`), which invsize entirely ignores. The n=5
> singleton-branch failure of the bare incidence count (§2) is precisely this
> overlap effect; invsize happens to compensate for it on n≤5, but there is no
> mechanism forcing it to keep compensating as the overlap geometry grows richer
> at larger `n`.

This is the **barrier reasserting itself**: the barrier says the live quantity
must be non-symmetric *and* must capture the non-separable overlap of the
fibre/generator filters. invsize is non-symmetric (good) but **separable** (bad)
— so it is exactly the kind of object the barrier predicts will eventually fail,
and Finding 5.1 confirms it has no separable certificate. The honest reading:
**the combined rule's invsize branch is an unproven heuristic, presumed to be a
finite-n coincidence, and is NOT a path to a proof.**

**Discipline gate (PASS).** No false refutation is possible: every recorded
invsize *miss* on n≤5 (the 2 cases that fall to the singleton branch in the
combined rule, and the §2 gfreq misses) occurs at a family where Frankl *holds*
via a different element — the rule fails to *find* the abundant element, never
falsely claims a sub-½ family is a counterexample. And the cube saturates the
combined rule at **exactly ½** (Finding 4.1), as a valid proof must.

---

## 6. Verdict — the barrier EXTENDS to separable generator-asymmetric methods (Task e)

1. **Generator-incidence formula (Identity 1.1, R-gen): exact, verified
   0/29,723.** The correct non-symmetric language: abundance is the max over
   columns of `M` of a **union size** of generator filters.
2. **"Most frequent generator element ≥½-abundant": FALSE** (356 failures, min
   0.333; clean counterexample `G={{2},{0,1,2},{3},{0,1,3}}`, §2).
3. **Generator-weighted abundances (`|g|`, `1/|g|`, `|↑g|`, lower-cover rank):
   FAIL and give the cube slack `1/k`** — a new failure mode, opposite to the
   symmetric methods, disqualified by the cube-equality discipline (§3).
4. **The combined singleton/invsize pick rule survives n≤5 + ~660,000 larger-n
   tests with min exactly ½ and cube equality**, but:
   - its singleton branch is the **classical folklore** case (not new);
   - its invsize branch **has NO proof, no separable certificate (Finding 5.1),
     and a clear reason to distrust (non-separability, Finding 5.2)**. It is
     flagged **`[EXTRAORDINARY — PRESUMED FLAWED PENDING RED-TEAM]`** and is
     almost certainly a finite-n coincidence. **No proof of Frankl is claimed.**
5. **The barrier EXTENDS.** Every *separable* generator-asymmetric quantity
   tested (incidence count, all four weighted abundances, the invsize
   *certificate* C1) **fails**. The only object that empirically survives is a
   non-symmetric *selector* with no certificate, and the obstruction to proving
   it is exactly the non-separable overlap the barrier identifies. The honest,
   sharp contribution is therefore a **stronger barrier statement**:

> **Extended barrier (generator-asymmetric) `[NOVELTY UNVERIFIED]`.** No
> *separable* function of the generator incidence matrix `M` — i.e. any
> `Φ(x) = Σ_{g∋x} w(g, |g|, |↑g|, \mathrm{rank}(g))` with generator-local
> weights — certifies abundance ≥ ½: the bare count is false (§2), every
> size/filter/rank-weighted version fails and mis-handles the cube (§3), and the
> natural separable certificate C1 is false (Finding 5.1). The reason is
> Identity 1.1 / R-gen: abundance is a **non-separable union size** of generator
> filters; separable proxies cannot see the filter overlap. A genuine
> generator-asymmetric proof must control the **overlap of the generator filters
> `↑g`** for the generators sharing a fixed element `x` — precisely the
> non-separable object `ji_overlap_inequality.md` showed the *symmetric* moment
> cannot reach. The non-symmetric, non-separable overlap of generator filters is
> the residual target; it is not delivered by any quantity in this note.

**No proof of Frankl. No constant > ½.** All framings `[NOVELTY UNVERIFIED]`;
the singleton lemma is `[PRIOR-ART — folklore, not claimed new]`; the invsize
rule is `[PRESUMED FLAWED]`.

---

## 7. Reproduction

```
cd math/frankl/experiments
python3 generator_attack.py 5     # -> data/genattack_n{0..5}.jsonl,
                                  #    data/genattack_summary.{txt,json}
# red-team / break attempts log: data/genattack_redteam.txt
```

**Step-1 (computational): PASS.** 29,723 families n≤5 + ~660,000 larger-n
break-attempt families.
- `F = {⋃S : S⊆G}` and abundance-from-generators == direct: **0 violations**.
- `Fib(x) = ⋃_{g∋x} ↑g` (R-gen): **0 violations / 148,164** pairs.
- H-gfreq (most frequent generator element): **FALSE**, 356 failures, min 0.333.
- Four weighted abundances: fail (180–3,116), drop to `1/k` on the cube.
- Combined pick rule: 0 failures n≤5, min ½, 377 equalities, cube = ½ exactly;
  invsize branch survives ~660,000 larger-n families but C1 certificate FALSE
  (12/29,723) ⇒ presumed flawed.

**Steps 2–4 (red-team / Lean / human): the only theorem is the folklore
singleton lemma; the invsize rule is explicitly PRESUMED FLAWED, not a claim.**
The deliverable is (a) the exact generator-incidence formula, (b) the falsified
heuristics with explicit counterexamples, and (c) the extended barrier statement
covering separable generator-asymmetric methods. `[NOVELTY UNVERIFIED]`.
