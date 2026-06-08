# Frankl candidate — JI-overlap / max-vs-mean spread on the upper-semimodular class

**Author:** Alex Ye (no AI on author line).
**Date:** 2026-06-04.
**Status:** FOUNDATIONAL CHECK FAILED — the program premise (USM blocks the
parasite mechanism) is FALSE on the n≤5 census.  This file is the honest
write-up of that result, with the precise restated program, the falsifier
outcome, and the residue that survives the failure.  **No proof of Frankl is
claimed.**  `[NOVELTY UNVERIFIED]` on every framing (arXiv 403 this session;
Reinhold's lower-semimodular statement reproduced from snippet-level memory).
**Companion code:** `frankl_usm_probe.py`.
**Data:** `data/usm_probe.json`.
**Cross-ref:**
`frankl/theory/lattice_attack.md` §5.2 (cone-blocked-class recommendation),
`frankl/theory/join_irreducible_labelling.md` §6 (Candidate 6.1, the
JI-overlap),
`frankl/theory/ji_overlap_inequality.md` §2 (the 6 parasite families
that defeat the lever; §3 the join-overlap tautology Lemma 3.1),
`frankl/experiments/data/overlap_counterexamples.txt` (parasite registry),
`ideas/candidates/frankl_sos_negative.md` (archived prior candidate —
level-4 SOS, decided negative on the same parasites),
`ideas/STATUS.md` (handover line for this candidate).

---

## 0. Why this file replaced the SOS candidate

Both formerly-live "certified shortcuts" came back NEGATIVE:

* **Lasserre level-2 (degree-4) incidence SOS** — collapses to the degree-2
  power-mean barrier on the parasite families; clean Lemma-3.1-style tautology
  (`frankl_sos_negative.md` §4 VERDICT; `data/las2_main_run.json`).
* **Alexander-dual fine Betti** — the only runnable forcing rule relocates to
  the same 6 parasite families (homology absent at apex; `frankl_review.md` §2,
  Kill-attempt C).

Three independent notes (the lattice attack §5.2, the JI-labelling §6, and the
review §4) converge on a single follow-up: **attack the JI-overlap / max-vs-mean
spread inequality restricted to the upper-semimodular (USM) class of lattices**,
where (the claim was) the 6 parasite families cannot be built.  This file turns
that claim into a probe and reports the result.

---

## 1. Precise statement

### 1.1 Notation (carried over)

Fix `F ⊆ 2^[n]` union-closed with `∅ ∈ F`.  Form the lattice `L = (F, ⊆, ∪)`
with join `=` set union (lattice_attack.md §1).  For a ground element `x ∈ [n]`
the **fibre** `Fib(x) = {A ∈ F : x ∈ A}` is a filter of `L`, with `freq(x) =
|Fib(x)|`.  Set

$$
P_1 = \sum_{A \in F}|A| = \sum_x \mathrm{freq}(x), \qquad
P_2 = \sum_x \mathrm{freq}(x)^2 = \sum_{A,B \in F}|A \cap B| =: \mathrm{OVL}(F),
$$

(the fibre-2nd-moment identity, classical double-counting; verified 0 violations
n≤5 in `ji_overlap_inequality.md` §1).  Frankl's conjecture in this language:
`max_x \mathrm{freq}(x) \ge |F|/2`.

### 1.2 Upper-semimodularity

A finite lattice `L` is **upper-semimodular** (USM) iff for all `a,b ∈ L`,
$$
b\ \text{covers}\ (a \wedge b)\quad\Longrightarrow\quad (a \vee b)\ \text{covers}\ a.
$$
Equivalently: whenever `a ⋖ a∨b` then `a∧b ⋖ b`.  `L` is **lower-semimodular**
(LSM) iff the dual condition holds (`a∧b ⋖ a ⟹ b ⋖ a∨b`).  Distributive
⊆ modular ⊆ (USM ∩ LSM) — modular lattices are both upper- and
lower-semimodular.  Computed by `frankl/experiments/lattice.py
::is_upper_semimodular`; validated on B₂, M₃, N₅, chains, cubes
(`tests::test_known_lattice_invariants`).

### 1.3 Reinhold's lower-semimodular Frankl theorem  `[NOVELTY UNVERIFIED]`

**Reproduced from secondary references (arXiv 403 this session, cannot verify
the primary statement):**

> **Reinhold's theorem (lower-semimodular Frankl, *informal restatement*).**
> If the lattice `L = (F, ⊆, ∪)` is **lower-semimodular**, then Frankl's
> conjecture holds for `F`: there exists a join-irreducible `j ∈ L` with
> `|↑j| \le |L|/2`, equivalently a ground element in `\ge |F|/2` members of `F`.

The dual statement (the upper-semimodular Frankl conjecture) does **not**
follow because the proof method uses a specific covering / shellability
property of LSM lattices that does not dualise.  This is the open sub-case
the brief names.

> **Caveat.** The Reinhold attribution is a snippet-level memory; the primary
> source is inaccessible this session.  The literature also discusses Frankl for
> *modular* lattices (subsumed by LSM if Reinhold's result is taken as stated,
> since modular ⇒ LSM) and *geometric* lattices (atomistic + semimodular —
> these are USM by definition, so a Frankl theorem for geometric lattices is
> a special case of the USM target; whether it is independently proven I cannot
> verify here).  Adjacent-class status table is §6.  Treat every attribution
> below as `[NOVELTY UNVERIFIED]`.

### 1.4 The candidate inequality (the target this program tried to attack)

> **Target inequality (JI-overlap on USM).**  For every union-closed `F`
> whose lattice `L` is **upper-semimodular**,
> $$
> 2\,\mathrm{OVL}(F) \;\ge\; |F| \cdot P_1(F).
> \tag{TARGET-USM}
> $$
> Equivalently, the power-mean density `P_2 / P_1 / |F| \ge 1/2`, which by
> Cauchy–Schwarz / power-mean (§1 of `ji_overlap_inequality.md`) implies
> Frankl: `\max_x \mathrm{freq}(x) \ge P_2/P_1 \ge |F|/2`.

The general-class version of this inequality is `FALSE` on 6 parasite
families (`ji_overlap_inequality.md` §2; minimum value `4/9 ≈ 0.4444`).
The candidate program asserts:

> **Program claim (P).**  The 6 parasite families are NOT upper-semimodular.
> Restricted to USM, the inequality (TARGET-USM) holds with strict slack
> except on the Boolean cubes `2^[k]`, where it holds with exact equality.

### 1.5 The lemmas that would close the program (the research plan, not a proof)

* **L1 (parasite exclusion):** every family in `ji_overlap_inequality.md` §2's
  parasite registry has a non-modular cover structure incompatible with USM.
  Mechanism: the heavy element `z` shared by every nonempty member acts like a
  *cone apex*; the parasites are produced by `cone(G)` (`lattice_attack.md` §4),
  which typically breaks (semi)modularity by inserting a fresh element above all
  of `L \ {0̂}` with a single cover.

* **L2 (exact JI-overlap identity on USM):** the JI-overlap sum
  `Σ_{j,k}|↑j ∩ ↑k|` admits a closed form on USM that exploits
  `(a ∨ b)` covering `a` — call this the cover-rank identity.  In particular:
  $$
  |\uparrow\!a \cap \uparrow\!b| = |\uparrow(a \vee b)|
  $$
  (tautology of the join, Lemma 3.1 of `ji_overlap_inequality.md`, holds in
  every lattice).  On USM, the rank function of `↑(a∨b)` is forced by the
  cover-rank of `a` and `b` (semimodular rank inequality).

* **L3 (strict inequality lift on USM):** there is a `c(L) > 0` such that
  $$
  2\,\mathrm{OVL}(F) - |F|\cdot P_1(F) \;\ge\; c(L) \cdot (|F|-1)
  $$
  for every USM realisation `F` of `L`, with equality only for the Boolean
  cube.  This would be the operational closing inequality.

These are *targets*, not theorems — none of L1, L2, L3 is proved here.  The
foundational check below decides whether L1 (the premise on which L2/L3 rest) is
even consistent with the n≤5 data.

---

## 2. Foundational verification (the n≤5 probe)

### 2.1 Method

`frankl_usm_probe.py` walks the canonical 29,723 UC families (n ≤ 5, |F| ≥ 2)
via `frankl/experiments/enumerate.all_uc_families`, builds the lattice with
`frankl/experiments/lattice.invariants`, and per family records:

* the four lattice-class flags (distributive, modular, LSM, USM),
* abundance,
* `P_1, P_2 = OVL`,
* the target slack `2·OVL − |F|·P_1`.

For each class C ∈ {all, distributive, modular, LSM, USM} it tabulates the
minimum power-mean density, count of (TARGET-F) failures, count of
abundance-exactly-½ families, and the worst-case witness.  The 6 named
parasites are checked individually first.

### 2.2 Parasite check — **the program premise (P) FAILS**

The verification of (P) — "the parasites are not USM" — comes back negative:
**5 of the 6 parasite families are USM, and moreover they are *distributive*.**

| family                | n | masks                       | true ab | pm dens | dist | mod | LSM | USM |
|-----------------------|--:|-----------------------------|--------:|--------:|:----:|:---:|:---:|:---:|
| `n5_F3a_minimal`      | 5 | `[0,16,31]`                 | 0.6667  | 0.4444  | ✔    | ✔   | ✔   | **✔** |
| `n4_F3`               | 4 | `[0,8,15]`                  | 0.6667  | 0.4667  | ✔    | ✔   | ✔   | **✔** |
| `n5_F3b`              | 5 | `[0,16,23]`                 | 0.6667  | 0.4667  | ✔    | ✔   | ✔   | **✔** |
| `n5_F5`               | 5 | `[0,8,16,24,31]`            | 0.6000  | 0.4667  | ✔    | ✔   | ✔   | **✔** |
| `n5_F6`               | 5 | `[0,8,16,23,24,31]`         | 0.6667  | 0.4744  | ✔    | ✔   | ✔   | **✔** |
| `n5_F7`               | 5 | `[0,8,15,16,23,24,31]`      | 0.5714  | 0.4958  | ✘    | ✘   | ✔   | ✘   |

The minimal parasite `n5_F3a_minimal = {∅, {4}, {0,1,2,3,4}}` — the one
that defeated the SOS, LP, Fourier, lattice-invariant, Kruskal-Katona,
second-moment, JI-overlap, and Alexander-dual levers — is a **3-element
chain**.  Chains are distributive, hence modular, hence both upper- and
lower-semimodular.  The parasite mechanism is *not* a non-modular cover
structure; it is *labelling*.  Five distinct ground elements label a
2-step chain `∅ ⊂ {4} ⊂ [5]`: one heavy (element `4` in the middle and the
top), four parasites (in the top only).  The abstract lattice is the most
restricted lattice imaginable; the labelling is what produces the lopsided
frequency vector.

The single non-USM parasite (`n5_F7`) is the largest one and the *least*
lopsided (true abundance 0.5714, slack only `-1`), confirming that USM-failure
correlates with parasite-mildness, not the other way around.

### 2.3 Class minima — the lever undershoots on every restricted class

| class               | count |  min pm density |  target_F fails |  at_½  |
|---------------------|------:|----------------:|---------------:|------:|
| all                 | 29,723 | **0.4444**     | 6              | 39    |
| distributive        | 649    | **0.4444**     | 5              | 39    |
| modular             | 815    | **0.4444**     | 5              | 39    |
| lower_semimodular   | 2,811  | **0.4444**     | 6              | 39    |
| upper_semimodular   | 941    | **0.4444**     | 5              | 39    |

The minimum power-mean density is exactly `0.4444 < 1/2` on **every** class,
witnessed by the same family `[0,16,31]` (the minimal parasite, which lives in
all of them).  USM does not move the lever's worst case at all.  In particular
Reinhold's LSM theorem, even if interpreted as "abundance ≥ ½ on LSM" (which
the census confirms — LSM count 2,811, all satisfy Frankl since the project's
census does), does **not** route through this power-mean inequality: the lever
fails on LSM families with abundance > ½ (the parasites).  Reinhold must use a
different mechanism (probably the LSM atom / lower-cover structure directly,
not a JI-overlap bound).

### 2.4 Tightness on the USM class — not unique to the cube

| USM with target slack > 0 (strict)        | 886 |
| USM with target slack = 0 (equality)      | 50  |
| USM with target slack < 0 (FAILURE)       | 5   |
| USM at abundance == ½                     | 39  |

The 39 USM families at abundance exactly ½ are **all distributive**, and
include the Boolean cubes B₁..B₅ as well as 34 other distributive realisations
(products of chains, half-cubes, etc.).  So the H5 result of
`join_irreducible_labelling.md` — "cube is the unique lattice iso class
where the *worst labelling* achieves abundance ½" — is consistent with this
table (the *iso classes* are unique to cubes), but at the *family* level
many distributive labellings are tight.  The cube is not isolated within USM.

---

## 3. Why this candidate would have escaped the proven barrier (and why that no longer matters)

The barrier theorem (`frankl/theory/ji_overlap_inequality.md` §3.2;
`PROGRESS.md` Phase 6 capstone) says: every symmetric convex moment of the
frequency vector is flat-minimised by the Boolean cube at exactly ½.  The
candidate program intended to escape it by **restricting the *class* of
admissible lattices** — not the form of the functional.  On the USM class:

* The cube *is* USM (it is distributive ⊆ modular ⊆ USM), so the cube need
  not be escaped — it is in the class and remains the (or *a*) tight extremum.
* The lever (TARGET-USM) is a symmetric convex moment functional (the
  power-mean), but the question is its value on the restricted class, not on
  all UC families.  A bound tight at the cube and strict elsewhere on USM
  would have been consistent with the barrier (barrier says "tight at cube";
  USM-restricted result would say "strict elsewhere on USM" — these are
  compatible).

This is the correct logical structure of a "restricted-class escape."  It is
**not** what failed.  What failed is the empirical premise: the parasite
families that drive the lever below ½ are themselves in the class (in fact in
the much smaller distributive subclass).  The barrier is not the issue; the
class-restriction did not carve away the parasites.

---

## 4. Falsifier — the sharp run

### 4.1 Falsifier definition

The candidate is dead iff there exists a USM UC family at n ≤ 5 with **true
abundance > ½ AND target slack < 0** (i.e. the JI-overlap inequality fails on
that USM family with positive abundance margin — the same failure mode the
6 parasites give on the full census).

### 4.2 Falsifier result

```
FOUND 5 witnesses -- candidate DIES.
n=4  masks=[0, 8, 15]                ab=0.6667 pm=0.4667 slack=-1  dist,mod
n=5  masks=[0, 8, 16, 23, 24, 31]    ab=0.6667 pm=0.4744 slack=-4  dist,mod
n=5  masks=[0, 8, 16, 24, 31]        ab=0.6000 pm=0.4667 slack=-3  dist,mod
n=5  masks=[0, 16, 31]               ab=0.6667 pm=0.4444 slack=-2  dist,mod
n=5  masks=[0, 16, 23]               ab=0.6667 pm=0.4667 slack=-1  dist,mod
```

These are 5 of the 6 named parasites, all USM, all distributive.  The
candidate inequality (TARGET-USM) is **FALSE** on 5 USM (in fact 5 distributive)
families at n ≤ 5.  The minimum value of the power-mean density on the USM
class is `4/9 = 0.4444`, attained at `[0, 16, 31]`, **identical** to the
unrestricted-class minimum.

The minimum power-mean density on the *distributive* class is also `0.4444`,
attained on the same family.  Distributive lattices, where Frankl is trivial
(Poonen 1992; well known), STILL host the parasite labelling — the parasite is
not a lattice obstruction at all.  The picture is now sharply sharper than the
review's "everything localises to the JI-overlap kernel": even within the most
restricted lattice class (distributive), the JI-overlap kernel fails the lever.

### 4.3 The bottom line

**The 6 parasite families do NOT disappear in USM, modular, LSM, or
distributive lattices.**  Specifically 5 of them are *chains plus a heavy
element* — the most elementary distributive lattices.  The "cone-blocked class"
intuition was wrong: the cone construction (which produces non-trivial
lattice-isomorphic high-abundance UC realisations) is one mechanism for
*labelling freedom*, but it is not the *only* mechanism, and certainly not the
one that produces the JI-overlap parasites.  The parasites need only a chain
and 5 ground-set labels.

---

## 5. Adjacent restricted-class Frankl cases

| Class                  | Frankl status (snippet-level, `[NOVELTY UNVERIFIED]`)                                                | JI-overlap (TARGET-F) on n≤5 census                          |
|------------------------|------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| Boolean / cube         | **trivial** (each singleton in ½ of members)                                                          | exact equality on every `2^[k]` (verified)                   |
| Distributive           | **proven** (Birkhoff: every distributive lattice is `J(P)` of a poset; folklore-trivial via Poonen)   | min pm density **0.4444** on 5 distributive parasites        |
| Modular                | **proven** (Abe; also subsumed if Reinhold's LSM result holds, since modular ⊆ LSM)                   | min pm density **0.4444** on 5 modular parasites             |
| Lower-semimodular      | **proven** (Reinhold) `[ATTRIBUTION UNVERIFIED]`                                                      | min pm density **0.4444** on 6 LSM parasites                 |
| Upper-semimodular      | **OPEN** (the brief's target sub-case; dual of Reinhold does not follow)                              | min pm density **0.4444** on 5 USM parasites                 |
| Geometric              | **OPEN** (atomistic + USM; subclass of USM; not separately settled AFAIK)                             | (subclass of USM; same failure)                              |
| Relatively complemented| **OPEN** (Abe-style result for some sub-cases)                                                       | (not separately tabulated)                                   |

Two observations:

1. The "USM is open" statement is a real open sub-case, and the brief's
   identification of it as the convergence chokepoint is correct.  This file
   does not weaken that — USM Frankl really is open and worth attacking.
2. The *lever for attacking it* (JI-overlap / power-mean) is **not the right
   lever**, because the same lever fails on the smaller proven classes
   (distributive, modular, LSM).  Whatever proof Reinhold uses for LSM, it
   cannot be a JI-overlap inequality of the form (TARGET-USM/F/L).  So the
   surviving USM target needs a different mechanism — *not* a moment of the
   fibre vector, even restricted.

---

## 6. Honest assessment

**This candidate does NOT survive its foundational check.**  Specifically:

* (a) Foundational premise (P) is FALSE: 5 of 6 parasite families are
  upper-semimodular; all 5 are distributive (the most restricted class above
  cube).  Restricting to USM does NOT remove the parasite mechanism.
* (b) The candidate inequality (TARGET-USM) is FALSE on 5 explicit n ≤ 5 USM
  families with abundance strictly above ½ — the same parasite failure pattern
  as the unrestricted (TARGET-F).  Falsifier triggered.
* (c) The minimum power-mean density on USM is `4/9 = 0.4444`, identical to
  the unrestricted minimum.  USM does NOT improve the worst case at all.
* (d) Adjacent-class data shows the parasite mechanism survives every
  restricted class down to distributive.  So the "find a restricted class
  where the JI-overlap holds" strategy cannot work at the *moment-functional*
  level: any moment-of-fibre lever that fails on the parasites on the full
  census also fails on the chains containing them.

**Does the parasite mechanism just relocate to within the class?** Yes,
literally.  The parasites *are* in the class (in fact in every restricted
class we tested).  The cone construction (`lattice_attack.md` §4) is the
mechanism for labelling-freedom on a *fixed* abstract lattice (it pushes
abundance up); the parasite phenomenon (`ji_overlap_inequality.md` §4.2) is
the mechanism for *labelling lopsided fibre vectors* on a fixed abstract
lattice (it pushes the power-mean density down).  Both are labelling, but
they are different labelling moves, and USM blocks only the cone move (and
only some cones — many USM lattices do admit a coning relabelling; we did
not exhaustively check).

### 6.1 What survives the failure (the residue worth recording)

1. **The brief's identification of USM as the open Frankl sub-case is
   correct.**  USM Frankl is genuinely open (modulo the unverified Reinhold
   attribution and arXiv-blocked literature pass).  A future attack on it must
   use a non-moment mechanism — the *cover-structure* of USM directly, not any
   fibre-moment.  Candidate non-moment mechanisms suggested by the data:

   * **L1 reformulation (non-moment).**  For USM `L`, every covering chain
     from `0̂` to `T` has the same length (the Jordan–Hölder property).  This
     is a *structural* fact about `L`, not a fibre quantity, and a
     forcing-rule that uses this length directly (e.g. an argument that
     pigeonholes the heavy ground element along a maximal chain) is the
     natural next attempt.  The conditional bound `abundance ≥ height/|L|`
     (`lattice_attack.md` §3) is one cheap instantiation; it is weak in
     general but, on USM where height is constrained by Jordan–Hölder, it
     may be exploitable in conjunction with other structure.

   * **Atom / co-atom structure.**  On USM, every join of atoms equals its
     join-of-covers; the "atom-spread" of `Fib(x)` (count of atoms in `Fib(x)`)
     is a non-moment statistic that this probe did not test.  If `Fib(x)` is
     forced to contain `≥ |L|/2` atoms when the cover graph is USM, Frankl
     follows for USM (by Birkhoff on atoms when `L` is atomistic).

2. **The "restricted-class" strategy at the moment-functional level is now
   *characterised as dead*.**  This is a clean negative: any candidate
   inequality of the form
   `f(fibre vector) ≥ |F|/2` (`f` symmetric convex) restricted to USM
   inherits its worst case from the chain-with-heavy-element families,
   because those are USM.  In particular the JI-overlap, second moment,
   power mean, LP-dual, and incidence-SOS levers are all uniformly capped
   below ½ on USM by the parasite chain `{∅, {z}, [n]}`.  This generalises
   the §3.2 barrier collapse to the restricted-class setting.

3. **The cube remains the canonical extremiser.**  `[0,16,31]`, etc. are
   distributive realisations *different from* the cube but at abundance ½ +
   ε; the cube `2^[k]` is at abundance exactly ½.  H5 of
   `join_irreducible_labelling.md` (cube uniqueness as iso class) remains
   compatible with this file (it is at the iso-class level, not the family
   level).

### 6.2 Concrete next direction (if the program is to be salvaged)

The right surviving move is not a different *class*; it is a different
*functional* on USM (or on the full census).  Specifically:

* **A non-moment forcing rule using the Jordan–Hölder length of USM**
  (atom-count / chain-length statistic).  Probe `Σ_x (\#\text{atoms below
  Fib}(x))` versus abundance on USM.
* **A non-symmetric statistic that distinguishes "heavy element" from
  "parasites" in the fibre vector** (already named as the genuine missing
  ingredient at `PROGRESS.md` §"Barrier theorem capstone"): some asymmetric
  function of *which* element is heavy.

These are the targets identified by `frankl_review.md` §4 "bottom line" as the
next wave; this candidate's failure does not invalidate them, it just confirms
that "JI-overlap on USM" was not the path.

---

## 7. Reproduction

```
cd math/ideas/candidates
python3 frankl_usm_probe.py 5
```

Reads from `../../frankl/experiments/{enumerate,lattice,uc_family}.py` (read-
only).  Writes `data/usm_probe.json` and prints the parasite check, the class-
minima table, and the falsifier verdict.

* Total UC families n ≤ 5, |F| ≥ 2: **29,723** (canonical count).
* USM families: **941**; modular: 815; LSM: 2,811; distributive: 649.
* Parasites that are USM: **5/6** (all 5 are also distributive).
* Falsifier witnesses (USM family with abundance > ½ and target slack < 0):
  **5** (all distributive).
* Minimum power-mean density on USM: **4/9 = 0.4444** (= unrestricted min).
* USM at abundance == ½: **39** (= all distributive families at ½, including
  the 5 Boolean cubes `2^[k]`, k = 1..5).

`[NOVELTY UNVERIFIED]` on every framing.  No proof of Frankl.  No constant
above ½.  Foundational check FAILED — candidate dies before the first lemma.
