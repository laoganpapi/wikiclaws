# Logic / model theory generation note — definable selectors (Frankl) and proof-theoretic strength (Collatz)

**Author:** Alex Ye (no AI on author line).
**Date:** 2026-06-03.
**Field cluster:** #10 — model theory (o-minimality, NIP, stability), descriptive
set theory, reverse mathematics / proof-theoretic strength, definability & the
polynomial/constructible hierarchy, automatic structures.
**Status:** SPECULATIVE DIRECTIONS, not proofs. Every claim flagged
`[NOVELTY UNVERIFIED]`; arXiv/journal access was 403 this session, so prior-art
is snippet-level only. Several sub-claims are flagged `[PRESUMED FLAWED]` where I
can already see the failure mode.
**Cross-ref:** `frankl/theory/generator_asymmetric.md` (§4 invsize selector,
§5 non-separability obstruction), `frankl/theory/join_irreducible_labelling.md`
(R-identity, cube-uniqueness H5), `collatz/theory/function_field.md` (degree
Lyapunov ⇒ analog converges), `collatz/literature/survey.md` §8 (Conway /
Kurtz–Simon Π⁰₂), `PROGRESS.md` BARRIER THEOREM.

---

## 0. The two questions, and the one honest reframe

The brief asks: (Frankl) is there a **uniformly definable choice function** in
some logic that selects a ≥½-abundant element, escaping the symmetric-moment
barrier *because definability is inherently non-symmetric*? (Collatz) what is the
**proof-theoretic strength** of "Collatz holds" / the function-field analog, and
does reverse math reveal a missing principle? Is the orbit relation **automatic**
so boundedness is decidable?

The honest reframe up front, because it governs everything below:

- **Frankl.** "Definable selector" is the *correct diagnosis* of what the barrier
  demands, and it sharpens the project's existing language — but as a *proof*
  device it has a hard ceiling I make precise in §2.3: a selector that is
  **first-order / bounded-quantifier definable in the incidence structure with
  parameters only the lattice order** is, by an Ehrenfeucht–Fraïssé /
  homogeneity argument, *symmetric under lattice automorphisms*, and on the
  Boolean cube the automorphism group is transitive on ground elements ⇒ any such
  selector is forced to be "pick an arbitrary element," which is fine on the cube
  (½ everywhere) but gives **no leverage** off it. The escape is to allow the
  selector to depend on a feature the automorphism group does *not* act
  transitively on — i.e. **size / cardinality**, which is NOT a lattice-order
  invariant (that is exactly `lattice_attack.md`'s cone obstruction: order alone
  is free). So the live object is a **definable selector in the structure
  enriched with the ground-set membership relation `∈` (equivalently the
  incidence matrix `M`)**, not in the abstract lattice. The `invsize` rule of
  `generator_asymmetric.md` is exactly such an `∈`-definable selector. This note's
  contribution is to (a) place it in a definability hierarchy, (b) explain via VC
  / honest-definitions *why* it is non-symmetric, and (c) say precisely what
  would have to be true (a **uniform definability with bounded quantifier rank
  independent of `n`**) for it to be more than a finite-`n` coincidence — and why
  I still presume it flawed.

- **Collatz.** The clean, *true*, and probably-publishable logic content is a
  **negative/diagnostic** one, and it is the mirror image of `function_field.md`:
  the function-field analog converges precisely *because* it has a degree Lyapunov
  function with **finite, primitive-recursively bounded level sets**, which makes
  its convergence provable in a **very weak** system (I argue RCA₀, even
  PRA-level); whereas any proof of integer Collatz must, by Kurtz–Simon, live in
  a setting where the *uniform* problem is Π⁰₂-complete, so the single map's
  proof cannot come from any principle that relativizes uniformly across the
  Conway family. Reverse math's value here is **delimiting**: it tells you the
  missing ingredient is necessarily *non-uniform* (specific to the arithmetic of
  2 and 3), matching survey §8.3's "(δ) finite-state argument capturing exactly
  T." The "automatic structure ⇒ decidable" route is **[PRESUMED FLAWED]** and I
  kill it explicitly in §6.2 (the orbit graph is not automatic; if it were,
  Collatz would be decidable, contradicting nothing known but being wildly
  implausible and in fact refutable via the unbounded-trajectory geometry).

So: one **sharpening + concrete probe** for Frankl, one **diagnostic theorem
sketch + two killed routes** for Collatz. Plausibility ratings in §7.

---

## 1. The logical tools (named)

- **Sauer–Shelah lemma / VC dimension** (Vapnik–Chervonenkis 1971; Sauer 1972;
  Shelah 1972). A set system of VC-dim `d` on a ground set of size `m` has at most
  `O(m^d)` sets. Frankl families are set systems; their **dual** VC dimension and
  shatter function are non-symmetric refinements of the frequency vector.
- **NIP / stability / honest definitions** (Shelah; Chernikov–Simon, "Externally
  definable sets and dependent pairs", and the *honest definitions* theorem). In
  an NIP structure, every externally definable set is "honestly" approximated by a
  definable set *uniformly*; the honest definition is a **canonical, definable
  representative** — a definability-theoretic source of canonical (non-symmetric)
  selectors.
- **Definable choice / definable Skolem functions** (o-minimality: every
  o-minimal expansion of an ordered group has definable Skolem functions; more
  generally "definable choice" holds in many tame structures). This is the exact
  template for a "uniformly definable selector."
- **Reverse mathematics** (Friedman–Simpson; the Big Five RCA₀, WKL₀, ACA₀, ATR₀,
  Π¹₁-CA₀) and the **arithmetic/analytic hierarchy** (Π⁰₂-completeness, Kurtz–Simon
  2007). Tool for pinning the strength of "Collatz holds" and the function-field
  analog.
- **Automatic structures** (Khoussainov–Nerode 1995; Blumensath–Grädel): a
  relational structure whose domain and relations are recognized by finite
  automata has **decidable first-order theory**; reachability/boundedness
  questions on automatic graphs are often decidable.
- **Descriptive complexity** (Fagin's theorem: NP = ∃SO; the polynomial
  hierarchy = SO; first-order + counting). Tool for asking *in which logic* a
  selector is expressible, hence whether it is `n`-uniform.

---

## 2. FRANKL — the definable-selector program

### 2.1 The setup and why definability is the right non-symmetric language

The BARRIER THEOREM kills every **symmetric convex moment** of the frequency
vector. The reason a selector escapes it is structural, not a loophole:

> A **moment** is `∑_x φ(freq(x))` (or a max of such over a symmetric class) — a
> value, invariant under permuting `[n]`. A **selector** `σ(F) ∈ [n]` is a *point*
> in `[n]`; permuting `[n]` permutes its output equivariantly, not invariantly.
> Frankl asks for the existence of a heavy element, i.e. it is a **Σ-statement**
> (`∃x: freq(x) ≥ |F|/2`), and the natural witness for an existential is a
> **Skolem function** = a selector. The barrier lives on the Π-side (lower bounds
> on averages); the selector lives on the Σ-side (a witness). They are genuinely
> different logical objects. This is the precise sense in which "definability is
> non-symmetric by nature": a Skolem term has an *output coordinate*, which a
> symmetric moment provably cannot have.

This is not new mathematics yet — it is a **correct re-description** of why
`generator_asymmetric.md`'s pick-rule angle is the right register and the
moment angle is dead. The new content is the **definability hierarchy** I impose
on selectors, which yields a *falsifiable program*.

### 2.2 The selector definability hierarchy (the actual proposal)

Work in the two-sorted structure `M(F) = ([n], L, ∈, ⊆, ∪)`: ground sort `[n]`,
lattice sort `L = F∪{∅}`, membership `∈ ⊆ [n]×L`, order and join on `L`. A
**selector** is a formula `σ(x)` (possibly with the obvious "argmax over `x` of a
definable score" sugar) picking one `x∈[n]`. Stratify by what it may use:

- **Level 0 (order-only).** `σ` uses `⊆,∪` on `L` but **not** `∈`. CLAIM
  (§2.3): every such selector is automorphism-invariant ⇒ on the cube it is
  forced symmetric ⇒ **cannot** distinguish elements ⇒ provably no leverage. This
  is the lattice-invariant barrier (`lattice_attack.md`) in definability dress.
- **Level 1 (membership-separable).** `σ = argmax_x Φ(x)` where
  `Φ(x) = ∑_{g∋x} w(g)` is a **first-order-definable score that is separable over
  generators** (a sum over `g` with `x∈g`). The `invsize` rule
  (`w(g)=1/|g|`) is **Level 1**. Finding 5.1/5.2 of `generator_asymmetric.md`
  (no separable certificate; abundance is a non-separable union size) is exactly
  the statement that **Level 1 has no soundness certificate**.
- **Level 2 (overlap / non-separable).** `σ` may quantify over *pairs* of
  generators and use `|↑g ∩ ↑h|` — the **JI-filter overlap** of
  `join_irreducible_labelling.md` §6. This is the first level whose score can in
  principle equal the true abundance (which IS a union size). The barrier does
  **not** obviously kill Level 2, because a pairwise-overlap score is a *quadratic
  non-symmetric* functional with an output coordinate — neither a symmetric
  moment nor separable.

> **The program in one line.** Find the *lowest* level of this hierarchy at which
> a **uniformly definable** (bounded quantifier rank, independent of `n`) selector
> provably picks a ≥½-abundant element. Level 0 is dead (§2.3). Level 1 is the
> `invsize` rule — empirically survives n≤5 + 660K but is presumed a finite-`n`
> coincidence (no certificate). The genuine target is **Level 2**, and there the
> right object is a definable *argmax of a pairwise JI-overlap score*.

### 2.3 Why Level 0 is dead — an EF / homogeneity argument (this part is rigorous)

> **Observation 2.1 [NOVELTY UNVERIFIED — but elementary].** Let `σ` be any
> selector definable in `(L, ⊆, ∪)` *without* `∈` (Level 0), by a formula of any
> quantifier rank. Then `σ` is invariant under `Aut(L)`: if `π ∈ Aut(L)` then the
> induced action on ground elements (via the cone/labelling) commutes with `σ`.
> On the Boolean cube `2^[n]`, `Aut(L) = S_n` acts **transitively** on ground
> elements. Hence `σ` cannot prefer any element on the cube — but the cube is the
> *unique* extremizer (H5, `join_irreducible_labelling.md`), so on the boundary
> case the selector is forced to be a blind tie-break. More damningly, the **cone
> construction** (`lattice_attack.md` §4) gives two `(L,⊆,∪)`-isomorphic families
> with abundance 0.5 vs 0.875 and *different* heavy elements; a Level-0 `σ` must
> output the "same" (image) element in both, so it is **wrong on at least one**.
> Therefore no Level-0 selector certifies Frankl. ∎(sketch)

This is the definability-theoretic restatement of "abundance is not a lattice
invariant." It is the EF-game reason the selector **must** read `∈` (= size /
cardinality data), which is precisely the feature `Aut(L)` does not see. *This is
the part of the note I am most confident in and the cleanest deliverable: it
explains, in logic, exactly why the cone obstruction forces non-order data.*

### 2.4 VC dimension and honest definitions — can NIP supply a canonical heavy element?

The brief asks: is union-closure an NIP/stable structure where a definable heavy
element exists by VC / honest-definitions?

**The hope.** If the fibre system `{Fib(x)}` (or the generator system `{↑g}`) had
**bounded VC dimension `d` independent of `n`**, then Sauer–Shelah caps the number
of distinct fibres, and honest-definitions (Chernikov–Simon) would give a
*uniformly definable* canonical approximant to the "heavy" externally-definable
set — a candidate canonical selector that is non-symmetric by construction (honest
definitions break ties canonically using the order on parameters).

**The reality check (do this first; it is cheap).**
- The frequency vector and abundance are governed by `|L|`, but the **VC dimension
  of a union-closed family is generally Θ(log|F|)** and is *not* bounded
  independent of `n` — the Boolean cube `2^[n]` shatters `[n]` (VC-dim `= n`). So
  union-closed families are emphatically **NOT a uniformly NIP class** in the
  naive encoding: the cube is the maximal-VC object. This **kills the naive
  honest-definitions route**, because honest definitions are an *NIP* phenomenon
  and the cube is the IP (independence-property) extreme.
- BUT this is itself the diagnostic: the cube is simultaneously (i) the Frankl
  extremizer and (ii) the VC-maximal / most-independent family. **High VC = many
  independent coordinates = abundance exactly ½** (each coordinate a fair coin);
  **low VC = structured = abundance forced up**. So the *correct* non-symmetric
  quantity may be a **VC/shatter-function statistic of the dual system**, with the
  cube as the unique VC-maximal extremizer — mirroring H5 exactly. This is a
  genuinely different functional from a convex moment (the shatter function counts
  *traces*, an inclusion-exclusion object, not an average of `φ(freq)`).

> **Candidate 2.2 [NOVELTY UNVERIFIED — PRESUMED a long shot].** Frankl-type
> statement via the **dual shatter function**: for a UC family, the abundance is
> lower-bounded by a function of `1/VC*(F)` (dual VC dim), tight (=½) iff the dual
> shatter function is maximal (the cube). The escape from the barrier: the shatter
> function `π_F(k) = max_{|S|=k} |{A∩S : A∈F}|` is **not a symmetric moment of
> freq** — it is a non-separable trace count, and it has a built-in "which
> elements" via the maximizing `S`. *I have NOT checked this beyond the cube
> endpoint and flag it as speculative.*

### 2.5 Why I still presume the whole selector route flawed (honest)

The `invsize` selector and any Level-1 object inherit the **non-separability
obstruction** verbatim (`generator_asymmetric.md` Finding 5.2): a definable score
that is a *sum over generators* cannot see filter overlap, and abundance IS the
overlap (union size). Definability does **not** repair separability — a Level-1
formula is separable *by its syntactic form*. The only logically honest escape is
to climb to **Level 2** (a definable score quantifying over generator *pairs*),
and there the open inequality is identical to Constraint 6.1 of
`join_irreducible_labelling.md` — i.e. **the definability framing does not bypass
the hard inequality; it only re-licenses the search at the pairwise level.** That
is real but modest: logic clarifies *where* the selector must live, not that one
exists. Plausibility accordingly capped at 2/5 (§7).

---

## 3. FRANKL — concrete first step (build on `generator_asymmetric.md`)

A small, self-contained probe that the existing `generator_attack.py` data can
almost answer, and that tests the one non-dead level (Level 2):

> **Probe F1 (Level-2 definable overlap selector).** Define the **pairwise
> overlap score**
> `Ψ(x) = ∑_{g,h ∋ x} |↑g ∩ ↑h| = ∑_{g,h∋x} |↑(g ∨ h)|`
> (a Level-2, `∈`-definable, non-separable, non-symmetric score with an output
> coordinate). Selector `σ_2(F) = argmax_x Ψ(x)`. **Test on all 29,723 UC
> families n≤5:** does `σ_2` pick a ≥½-abundant element with min exactly ½ and
> cube-equality? Compare against `invsize` (Level 1): in the 652 families where
> `invsize`'s argmax ≠ max-frequency element, does `σ_2` agree with the true heavy
> element more often? **Predicted discriminator:** because `Ψ` is exactly the
> overlap quantity abundance is built from (R-identity), `σ_2` should track the
> true heavy element *more faithfully than any separable score* — if it does NOT
> beat `invsize`, that is strong evidence the whole selector route is a
> coincidence; if it does and survives, it is the first *non-separable* definable
> selector and the right object to try to prove (= Constraint 6.1).

> **Probe F2 (VC endpoint check).** Compute the **dual shatter function**
> `π*_F(k)` for all n≤5 families and correlate `1 − abundance` with the normalized
> dual shatter growth. **Predicted:** the cube maximizes dual shatter AND
> minimizes abundance at ½; if the correlation is monotone with the cube at the
> joint extreme, Candidate 2.2 is worth formalizing; if not, drop it. Pure data,
> no proof, ~30 lines on top of the existing census loader.

Both probes are **falsifiable on existing data this session** (modulo writing the
loop) and each has a clear kill condition. That is the deliverable's concrete
first step.

---

## 4. COLLATZ — proof-theoretic strength (the diagnostic theorem)

### 4.1 Strength of the function-field analog: it is WEAK, and that is the point

`function_field.md` proves: `Φ` on `𝔽₂[T]` has a **degree Lyapunov function**
`deg`, non-increasing, strictly decreasing on the `T|f` branch, with **finite
level sets** `|{deg ≤ d}| = 2^{d+1}`.

> **Observation 4.1 [NOVELTY UNVERIFIED].** "Every orbit of `Φ` reaches the fixed
> point" is provable in **RCA₀** (indeed in PRA / IΣ₁), because the convergence
> proof is a **bounded descent on a primitive-recursive well-founded ranking**:
> `deg` decreases on a definite proportion of steps and never increases, and each
> level set is finite and effectively enumerable. There is no use of WKL, ACA, or
> any infinitary principle — it is a finite-state-per-level argument. Reverse math
> assigns it the **weakest** Big-Five box.

The reverse-math content is therefore *contrastive*: the analog converges for a
reason that is **proof-theoretically trivial** (bounded monotone descent). Integer
Collatz manifestly lacks any such ranking — the odd step *raises* `log₂ n` by
`log₂3 − 1 > 0`, so no degree/magnitude Lyapunov exists (this is the archimedean
disanalogy `function_field.md` already isolates). The logic restatement:

> **Missing-principle diagnosis [NOVELTY UNVERIFIED].** Whatever proves integer
> Collatz cannot be a **monotone-descent / well-founded-ranking** argument over a
> primitive-recursive rank (those are RCA₀ and would transfer to the analog and to
> *every* Conway-family map with a rank — but Kurtz–Simon Π⁰₂-completeness shows
> the family has no uniform decision procedure, hence no uniform rank). The
> integer proof must use a principle that is **non-uniform across the Conway
> family** — i.e. it must exploit the *specific* arithmetic of (2,3) in a way that
> does not relativize. Candidate strength: the *statement* "∀n the T-orbit of n
> reaches 1" is Π⁰₂ as written (∀n ∃k T^k(n)=1); for the **single** map it may be
> far weaker if a (non-primitive-recursive but provably total) stopping-time bound
> exists, but no such bound is known and Tao's result is only almost-everywhere.

### 4.2 Why this escapes the moment/π_n barrier (Collatz side)

The project's Collatz barrier is analytic (the exact non-uniform stationary `π_n`,
TV ≥ 1/6; moment/mixing arguments inert). The reverse-math angle is **orthogonal**
to it: it is not an averaging statement at all. It says the *logical form* of the
needed argument is constrained — specifically, it **forbids** the entire class of
"global monotone potential" proofs (which is where most amateur attempts and some
serious Lyapunov attempts, cf. `digit_lyapunov.md`, live) by showing they would
prove too much (the whole Conway family). That is a genuine non-moment,
non-spectral *delimiter* — a "why the easy shape of proof can't work" result, the
Collatz analogue of the Frankl barrier theorem.

### 4.3 Is the orbit relation automatic? (asked; answered NO)

> **Observation 4.2 [PRESUMED FLAWED if claimed positive — here used negatively].**
> The Collatz orbit reachability relation `R(m,n) ≡ "n is on the orbit of m"` is
> **not** (and cannot be) a regular/automatic relation on base-`b` representations
> for any fixed `b`. If it were automatic, FO-theory (including boundedness
> `∃B ∀k T^k(n) ≤ B`) would be **decidable** by Khoussainov–Nerode — but the
> single-map decidability is open *and* the map's behaviour is the
> archetype of "automatic-method-resistant" (the `3n+1` step is not a
> finite-state operation on any fixed-base digit string because the carry from
> `×3` interacts globally with the `/2` shifts; the Syracuse map on `(ℤ/3ⁿℤ)ˣ` has
> growing modulus, the opposite of bounded automaton memory). The mod-3 obstruction
> `π_n` (TV ≥ 1/6) is the measure-theoretic shadow of exactly this
> non-automaticity. **Conclusion: the automatic-structure route is a dead end, and
> its deadness is itself informative** — it says the orbit relation has unbounded
> "memory," consistent with Π⁰₂-hardness of the family.

This is a "why-not," which the rules explicitly permit and which is valuable: it
closes off a tempting route (someone *will* try to make Collatz automatic) with a
clean reason.

---

## 5. COLLATZ — concrete first step

> **Probe C1 (pin the analog's strength, make the contrast a theorem).** Formalize
> Observation 4.1 at statement level: write the `Φ`-convergence proof as a bounded
> descent and check it uses only Σ⁰₁-induction (IΣ₁ / PRA). Concretely, in the
> existing `function_field.py`, certify the *uniform* bound "every `f` with
> `deg f ≤ d` reaches the fixed point in `≤ B(d)` steps" with `B(d)` an explicit
> primitive-recursive function (the data already has stopping times per degree —
> fit `B(d)` and verify it is PR, e.g. `O(2^d)` or polynomial). A verified
> explicit `B(d)` *is* the RCA₀/PRA certificate. Deliverable: a one-paragraph
> reverse-math classification of the analog + an explicit `B(d)`, contrasted with
> the *provable nonexistence* of any magnitude-monotone rank for integer `T`
> (odd-step increase `log₂3 − 1`). This is fully doable from existing data.

> **Probe C2 (Conway-family non-uniformity, sanity).** Exhibit two Conway-family
> maps — one with a degree/magnitude rank (converges, RCA₀) and one Kurtz–Simon
> encodes a non-halting TM (no rank) — to *witness* that "has a primitive-recursive
> monotone rank" is the dividing line. Confirms the missing-principle diagnosis is
> not vacuous. Small, illustrative, snippet-level (no PDF needed).

---

## 6. Two routes I explicitly KILL (rules: "why not" is valid)

- **6.1 (Frankl) Level-0 / lattice-definable selector — DEAD** (§2.3, EF/homogeneity
  + cone). Any order-only definable selector is `Aut(L)`-invariant; the cone gives
  two iso families with different heavy elements ⇒ wrong on one. Must read `∈`.
- **6.2 (Collatz) Automatic-structure decidability — DEAD** (§4.3). The orbit
  relation is not automatic; `×3`+carry is not finite-state on fixed-base digits;
  growing Syracuse modulus = unbounded automaton memory. Khoussainov–Nerode would
  give decidability, which is implausible and unsupported. The non-automaticity is
  the combinatorial face of the `π_n` / TV ≥ 1/6 obstruction.
- **6.3 (Frankl) Naive honest-definitions / NIP — DEAD as stated** (§2.4). UC
  families are VC-maximal at the cube (`2^[n]` shatters `[n]`, VC-dim `n`), so they
  are the IP extreme, not a uniform NIP class; honest definitions do not apply
  uniformly. Survives only as the *dual shatter function* reframe (Candidate 2.2,
  speculative).

---

## 7. Plausibility, failure modes, novelty

| Item | Plaus. (1–5) | Failure mode |
|---|---|---|
| §2.3 Level-0 selector is `Aut(L)`-invariant ⇒ dead | **4** | EF-sketch needs the cone↔labelling action made precise; but matches `lattice_attack.md` exactly, low risk. |
| Selector hierarchy as the right framing | **3** | It is a re-description; clarifies but does not solve. Honest value = it pinpoints Level 2 = Constraint 6.1. |
| §2.4 VC/shatter dual reframe (Cand. 2.2) | **2** | Only the cube endpoint checked; could be a coincidence; "tight at cube" is true of *every* method here. |
| Level-2 overlap selector probe F1 | **3** | If `σ_2` doesn't beat `invsize` on the 652-family discriminator, route is a coincidence — but that's a *clean negative*, still useful. |
| §4.1 analog provable in RCA₀/PRA | **4** | Bounded monotone descent is textbook-weak; low risk. The *contrast* (no integer rank) is already in `function_field.md`. |
| §4.2 missing-principle = "non-uniform across Conway family" | **3** | Delimiter, not a proof; the precise statement "no PR monotone rank for integer T" needs care (Tao gives a.e. bound, not a rank). |
| §4.3 / 6.2 orbit relation not automatic | **3** | "Not automatic" is morally clear but a *proof* would itself be a theorem; here used only to kill the route, which is safe. |

**Overall.** The strongest, lowest-risk deliverables are the two **delimiters**:
§2.3 (Frankl: order-only definable selectors are dead, in logic) and §4.1–4.3
(Collatz: the analog is RCA₀-weak, the integer proof must be non-uniform / the
orbit is not automatic). The one *forward* idea with a falsifiable next step is the
**Level-2 definable overlap selector** (Probe F1), which is the definability dress
of the project's existing crown lever (JI-filter overlap, Constraint 6.1) —
re-licensed at the pairwise level, not bypassing the hard inequality.

**Novelty.** All `[NOVELTY UNVERIFIED]`. The VC/Sauer–Shelah, honest-definitions
(Chernikov–Simon), definable-choice (o-minimal), reverse-math (Friedman–Simpson),
automatic-structure (Khoussainov–Nerode), Kurtz–Simon Π⁰₂, and Fagin theorems are
all classical and named. The *application* — selector definability hierarchy for
Frankl with the cube as the `Aut`-transitive / VC-maximal extremizer, and the
RCA₀-vs-non-uniform delimiter for Collatz — is plausibly new framing but
structurally a re-encoding of results this project already proved; I claim no
priority and presume the forward selector route ultimately flawed for the
non-separability reason (§2.5).
