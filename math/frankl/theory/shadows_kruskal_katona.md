# Shadow / Kruskal–Katona attack on Frankl's union-closed conjecture

**Author:** Alex Ye (no AI on author line).
**Date:** 2026-06-03.
**Status:** `[NOVELTY UNVERIFIED]` for every hypothesis below. **Outcome: a
sharp negative — compression/shifting does NOT preserve union-closure, and the
shadow-containment lever a Kruskal–Katona reduction would need fails on the
FUCC extremizer.** No bound is claimed; nothing is `PENDING RED-TEAM` because
the deliverable is an obstruction + exhaustive falsification, not a theorem.
**Companion code:** `frankl/experiments/shadows.py`.
**Data:** `frankl/experiments/data/shadows_n{1..5}.jsonl`,
`data/shadows_summary.txt`. **Tests:**
`tests/test_uc.py::TestShadowsKruskalKatona` (6 tests, all pass; full suite
69 pass).

> **Honesty flags.** arXiv is 403-blocked this session, so novelty is
> uncheckable. Shadow methods are **classical** (Kruskal 1963, Katona 1968) and
> the shifting/compression operator `S_{ij}` is the standard Frankl-shifting
> tool used throughout extremal set theory; **they may already have been tried
> on FUCC.** Every statement is flagged `[NOVELTY UNVERIFIED]`. The
> *positive* facts here (e.g. `S_{ij}` preserves layer sizes; FKG requires
> log-supermodularity) are textbook; the *load-bearing contribution* is the
> exhaustively-verified negative: **the standard compression toolkit does not
> apply to union-closed families**, which explains why the powerful
> Kruskal–Katona machinery has not yielded a FUCC bound.

> **Project record.** This is the fifth orthogonal attack catalogued in the
> project, distinct from the four exhausted methods: entropy (caps at
> `ψ = (3−√5)/2`, `dead_ends.md` Vectors 1–3), lattice invariants
> (`lattice_attack.md`: abundance is not a lattice invariant — universal-element
> cone), polynomial/slice-rank (`polynomial_method.md`: `sr(T_F) = |F|`,
> vacuous), and Boolean Fourier (`boolean_fourier.md`: spectrum-quadratic
> features vanish on the Boolean cube). The shadow attack lands the SAME
> structural obstruction at a new layer — and adds a genuinely new one specific
> to compression.

---

## 0. Setup and the split

Let `F ⊆ 2^[n]` be union-closed, `F ≠ {∅}`. For `i ∈ [n]`:

* `F_i  = {A ∈ F : i ∈ A}`, `F_{¬i} = {A ∈ F : i ∉ A}`.
* `abundance_i = |F_i|/|F|`; **FUCC ⟺ ∃ i with `|F_i| ≥ |F_{¬i}|`.**
* `F_{¬i}` is **itself union-closed** (closed under ∪). And the cross-relation
  `A ∈ F_i, B ∈ F_{¬i} ⇒ A ∪ B ∈ F_i` holds (the union contains `i`).
* The **link** (contraction) `link_i = {A \ {i} : A ∈ F_i}` and the **trace**
  (deletion) `trace_i = F_{¬i}`, both union-closed families on `[n] \ {i}`, with
  `|link_i| = |F_i|`, `|trace_i| = |F_{¬i}|`. So **FUCC ⟺ ∃ i: |link_i| ≥
  |trace_i|.**

The **lower shadow** `∂G = {B : B = A \ {x}, A ∈ G, x ∈ A}` and **upper shade**
`∇G = {A ∪ {x} : A ∈ G, x ∉ A}` are the Kruskal–Katona objects. The *hope* of a
shadow attack is a Kruskal–Katona-type inequality forcing `|link_i| ≥ |trace_i|`
for some `i` from shadow data. All infrastructure is in `shadows.py`
(`lower_shadow`, `upper_shade`, `split`, `link_and_trace`, `profile`), validated
on all 29,738 nontrivial UC orbit reps at `n ≤ 5` (cross-check: **0 Frankl
violations**, re-deriving Bošnjak–Marković for `n ≤ 5`).

---

## 1. (a) Compression/shifting does NOT preserve union-closure — the main obstruction

### 1.1 The operator

The classical **down-compression** `S_{ij}` (for `i < j`), the workhorse of
extremal set theory: for each `A ∈ F` with `j ∈ A, i ∉ A`, set
`A' = (A \ {j}) ∪ {i}`; replace `A` by `A'` **iff `A' ∉ F`** (otherwise keep
`A`). `S_{ij}` is a size-preserving bijection that preserves every **layer size**
`f_k = #{A : |A| = k}` and pushes incidence mass from coordinate `j` toward `i`.
A family fixed by all `S_{ij}` is **compressed/shifted**. (`shadows.py`:
`shift_family`, `fully_compressed`, `compress_to_fixed_point`.)

For *intersecting* families, antichains, and most Kruskal–Katona applications,
`S_{ij}` **preserves the relevant closure property** — which is exactly why
compression reduces those problems to a shifted base case. **The question for
FUCC: does `S_{ij}` preserve union-closure?**

### 1.2 The answer: NO. Minimal witness at n = 4.

> **Finding 1.2 `[NOVELTY UNVERIFIED]`.** Down-compression does **not** preserve
> union-closure. The minimal witness is
> $$ F = \{\,\{0,1\},\ \{2,3\},\ \{0,1,2,3\}\,\}\qquad (n=4). $$
> `F` is union-closed (`{0,1} ∪ {2,3} = {0,1,2,3} ∈ F`). Applying `S_{0,2}`
> (rename element `2 → 0`) sends `{2,3} ↦ {0,3}` while fixing the other two
> sets, giving
> $$ S_{0,2}(F) = \{\,\{0,1\},\ \{0,3\},\ \{0,1,2,3\}\,\}, $$
> which is **not** union-closed: `{0,1} ∪ {0,3} = {0,1,3} ∉ S_{0,2}(F)`.

**Why.** Union-closure is a *global join* constraint, not a coordinatewise/down
constraint. The witnessing join `{0,1} ∪ {2,3} = {0,1,2,3}` relies on the two
sets being **coordinate-disjoint**; the shift `2 → 0` collides their supports, so
their union shrinks from `{0,1,2,3}` to `{0,1,3}`, which the family no longer
contains. Compression is designed to preserve *down-sets / shadows*; the union
operation is an *up*-operation whose value depends on disjointness, exactly the
data compression scrambles. (Verified: `tests::test_minimal_compression_breaks_uc`.)

### 1.3 Exhaustive census (`n ≤ 5`)

| `n` | UC families | single `S_{ij}` breaks UC | compress→fixed-point breaks UC | compression **raises** abundance |
|---|---|---|---|---|
| 1 | 2 | 0 | 0 | 0 |
| 2 | 8 | 0 | 0 | 0 |
| 3 | 36 | 0 | 0 | 4 |
| 4 | 366 | 16 | 2 | 142 |
| 5 | 29,326 | 5,516 | 520 | 22,668 |
| **Σ** | **29,738** | **5,532** | **522** | **22,814 (76.7%)** |

(`data/shadows_summary.txt`; the per-`n` split is reproducible via the jsonl.)
Shifting preserves UC for **all** `n ≤ 3` — the first failures appear at `n = 4`,
exactly the minimal witness of §1.2.

### 1.4 Worse: compression goes the WRONG direction for a reduction

A compression reduction needs `S_{ij}` to (i) preserve UC and (ii) only
*decrease* max-abundance, so the extremal (hardest) case is compressed. **Both
fail.** Beyond breaking UC, when it *does* stay UC, compression **increases**
max-abundance on **22,814 of 29,738 families (77%)** — e.g.
`{{0,1},{2},{0,1,2}}` has abundance `2/3` but compresses to abundance `1`. So
the compressed families are *easier* for FUCC, not harder; a reduction "to the
compressed case" would discard precisely the extremal families. (Verified:
`tests::test_compression_can_increase_abundance`.)

> **Conclusion 1.4.** The standard compression/shifting toolkit is structurally
> **inapplicable** to FUCC: `S_{ij}` neither preserves union-closure (first
> failure `n = 4`, minimal witness `{{0,1},{2,3},{0,1,2,3}}`) nor monotonically
> reduces max-abundance (it raises it on 77% of families). **This is the
> explanation for why the powerful Kruskal–Katona / shifting machinery — which
> trivializes many extremal-set problems — has not produced a FUCC bound.** It is
> a genuine "delimiting the method" result `[NOVELTY UNVERIFIED]`.

---

## 2. (b) The F_i/F_{¬i} split and the shadow-containment lever

The natural Kruskal–Katona route to `|link_i| ≥ |trace_i|` for some `i` would
come from a **containment** `trace_i ⊆ link_i` (then `|F_i| = |link_i| ≥
|trace_i| = |F_{¬i}|` immediately, giving Frankl at `i`). The cross-relation
`A ∈ F_i, B ∈ F_{¬i} ⇒ A∪B ∈ F_i` *almost* suggests this: every `B ∈ trace_i`
joins with the top `T = ⋃F ∈ F_i` to land in `F_i`. But the map `B ↦ B` (not
`B ↦ B ∪ {i}`) need not land `B` itself in `link_i`.

> **Finding 2.1 (the lever FAILS) `[NOVELTY UNVERIFIED]`.** The containment
> `trace_i ⊆ link_i` fails. Tested as candidate **C6** (at the most-abundant
> `i`) and **C7** (at some `i`):
> * **C6** (`trace ⊆ link` at the max-`|F_i|` element): **8,164 violations**
>   of 29,738.
> * **C7** (`trace ⊆ link` at *some* `i`): **3,075 violations**.
>
> The minimal witness is the saturating diagonal family `F = {∅, {0,1}}`
> (`n = 2`, abundance exactly `1/2`): at the most-abundant `i = 0`,
> `link_0 = {A \ {0} : A ∈ F_0} = {\{1\}}` (deleting `0` from `{0,1}`) while
> `trace_0 = F_{¬0} = {∅}`, and `∅ ∉ {\{1\}}`, so `trace_0 ⊄ link_0`. (By
> symmetry the same holds at `i = 1`.) Frankl *still* holds here — `|F_0| = 1 =
> |F_{¬0}|` — but **not via the containment**, which is exactly the point: the
> shadow-containment lever is absent even on the simplest extremal family.
> (`data/shadows_summary.txt`, C6/C7 worst witness `masks=[0,3]`.)

So the would-be shadow lever does not exist: **abundance is not forced by a
shadow containment.** Two *downstream symptoms* of the split DO survive testing,
but neither is an independent lever:

* **C2** (`|∂(link_i)| ≥ |∂(trace_i)|` at the most-abundant `i`): **0
  violations.** But this is a *consequence* of `link_i` carrying more mass at the
  abundant element, not a cause of it — it cannot be used to *prove* `|F_i| ≥
  |F_{¬i}|` because it presupposes the choice of the abundant `i`.
* **C5** (Reimer average-set-size `≥ ½ log₂|F|`): **0 violations** — a sanity
  re-derivation of Reimer (2003), confirming the toolkit.

Candidate **C3** (a shade-size calibration bound) had 1,689 violations and **C4**
(`average set size ≥ n/2`) had 508 violations — both falsified, confirming UC
families are **not** uniformly "top-heavy" (see §3).

---

## 3. (c) Profile / LYM analysis

The **profile** `(f_0, …, f_n)`, `f_k = #{A : |A| = k}`. One hopes union-closure
forces a top-heavy profile (mass at large sets ⇒ high abundance). It does not, at
the level needed:

> **Finding 3.1 `[NOVELTY UNVERIFIED]`.** The candidate profile inequality
> **C4: average set size `≥ n/2`** is **FALSE** (508 violations at `n ≤ 5`).
> Minimal witness `F = {∅, {4}}` (`n = 5`): average size `0.5 ≪ 2.5 = n/2`. UC
> families can be arbitrarily "bottom-heavy" on the *active* coordinates while
> living in a large ground set. (`data/shadows_summary.txt`.)
>
> Note `Σ_i (|F_i| − |F_{¬i}|) = 2·(total incidences) − n|F| = |F|·(2·avgsize/… )`,
> so `avg set size ≥ n/2 ⟺ Σ_i(|F_i|−|F_{¬i}|) ≥ 0` — a *sum* over `i` being
> nonnegative does **not** give a *single* `i` with `|F_i| ≥ |F_{¬i}|` unless the
> max exceeds the mean, which UC does not force. This is precisely the LYM-style
> averaging gap.

The only profile-level fact that survives is **Reimer's** `avg ≥ ½ log₂|F|` (C5,
0 violations) — already in the literature (survey §2.2), tight on power sets, and
known to be insufficient alone.

---

## 4. (d) Ahlswede–Daykin / FKG — fails outright

The Four Functions Theorem (Ahlswede–Daykin) and FKG give positive correlation
of up-events **for log-supermodular (FKG) measures**. If the uniform measure on
`F` were FKG, the up-events `U_i = {A : i ∈ A}` would be positively correlated,
plausibly forcing some `abundance_i` up. **But uniform-on-`F` is not FKG**: a
union-closed family is **not** an up-set, so log-supermodularity fails.

> **Finding 4.1 (FKG fails) `[NOVELTY UNVERIFIED]`.** Over all 295,572
> element-pairs `(i,j)` across UC families `n ≤ 5`, the positive-correlation
> inequality `Pr[i,j ∈ A] ≥ Pr[i∈A]·Pr[j∈A]` is **VIOLATED on 119,662 pairs
> (40.5%)**, with minimum correlation `−0.1667`. The minimal witness is the
> "diagonal cross"
> $$ F = \{\,\{0\},\ \{1\},\ \{0,1\}\,\}: \quad
>    \Pr[0]=\Pr[1]=\tfrac23,\ \Pr[0,1]=\tfrac13<\tfrac49, \ \text{corr}=-\tfrac19. $$
> Elements `0,1` are **anti**-correlated: they co-occur only forced (in the
> join), never on their own generators. (`tests::test_fkg_fails_on_minimal_witness`.)

> **Conclusion 4.1.** Correlation inequalities (Ahlswede–Daykin / FKG /
> Harris–Kleitman) supply **no** abundance pressure for UC families, because
> union-closure produces *negative* element-correlation (joins force
> co-occurrence that is absent in the generators). This is the opposite of what a
> correlation-based proof would need.

---

## 5. The recurring extremizer (why this matches the project pattern)

The **Boolean cube** `2^[n]` is again the obstruction, now from the shadow side:

| object | abundance | shift-compressed? | role |
|---|---|---|---|
| `2^[n]` (cube) | **0.5000** | **yes** (a `S_{ij}` fixed point) | FUCC extremizer |
| `cone(2^[n])` | `1 − 1/2^n` (→1) | n/a | identical profile structure, abundance pushed up |

(`shadows.py::cone_extremizer_check`; `tests::test_cone_cube_extremizer`.) The
cube saturates FUCC at `½`, is already a compression fixed point (so compression
extracts nothing from it), and its cone — the lattice-attack's universal-element
construction — drives abundance to `1` while the layer/shadow profile is the same
shape shifted by one coordinate. **Shadow statistics cannot distinguish the
abundance-`½` cube from the abundance-`1` cone**, the identical collapse the
lattice (`lattice_attack.md` §4) and Fourier (`boolean_fourier.md` §4) attacks
found. The extremizer is **shadow-trivial**.

---

## 6. Verdict and the single most-promising shadow sub-direction

### 6.1 Verdict

1. **Compression/shifting does NOT preserve union-closure** (first failure
   `n = 4`, minimal witness `{{0,1},{2,3},{0,1,2,3}}`; 522 fixed-point failures,
   5,532 single-step failures at `n ≤ 5`), and **raises** max-abundance on 77% of
   families. The standard shifting reduction is structurally unavailable for FUCC.
   `[NOVELTY UNVERIFIED]` — likely the reason Kruskal–Katona has not bitten here.
2. **F_i/F_{¬i} split:** the shadow-containment lever `trace_i ⊆ link_i` fails
   (8,164 / 3,075 violations); only downstream symptoms (C2) and Reimer (C5)
   survive, neither an independent lever.
3. **Profile/LYM:** no top-heaviness inequality (`avg ≥ n/2` false, 508
   violations); only Reimer `½ log₂|F|` survives — already known insufficient.
4. **Ahlswede–Daykin / FKG:** **fails** (40.5% of pairs anti-correlated; min
   `−1/6`); union-closure gives *negative* correlation, the wrong sign.
5. **No bound** is produced; **no PENDING RED-TEAM** claim is made. The
   deliverable is the compression-non-preservation obstruction + exhaustive
   falsification of the shadow/profile/correlation levers.

### 6.2 The single live sub-direction

> **Direction: a union-closure-respecting compression.** The standard `S_{ij}`
> fails because it is a *down*-shift, while ∪ is an *up*-operation sensitive to
> support-disjointness. The live question `[NOVELTY UNVERIFIED]`: **is there an
> alternative compression `T` that (i) preserves union-closure and (ii)
> monotonically reduces max-abundance toward the extremal `½`?** The minimal
> witness §1.2 pinpoints the requirement: `T` must not collide the supports of a
> *generating* join. A candidate is a **join-respecting / generator-level**
> compression acting on the join-irreducibles (the lattice's atoms) rather than
> on raw coordinates — i.e. compress in the `lattice_attack.md` JI-labelling, not
> in `2^[n]`. Whether such a `T` exists and reduces abundance is open; if it
> does, it would be the first compression reduction for FUCC. The obstruction of
> §5 (the cube is already a fixed point of any coordinate compression) means `T`
> must act on **labelling/fibre** data, tying back to the lattice attack's
> identified missing ingredient (open problem F.2: constrain the JI-labelling).
> This is the same chokepoint the other four methods hit, now reached from the
> shadow side — strong (if negative) corroboration that the missing lever is the
> **fibre/labelling structure**, not any coordinatewise/order/spectral invariant.

---

## 7. Reproduction & certification

* **Computational: PASS.**
  - `python3 shadows.py` → `data/shadows_n{1..5}.jsonl` (29,738 families),
    `data/shadows_summary.txt` (the §1.3 census, candidate-inequality violation
    counts, FKG aggregates, cone/cube table).
  - `pytest tests/test_uc.py::TestShadowsKruskalKatona` → 6 tests pass; full
    suite **69 pass**.
* **No theorem claimed** ⇒ Steps 2–4 (red-team / Lean / human) N/A. The
  obstruction is a construction + exhaustive check (minimal witnesses are exact,
  not enumeration-dependent: §1.2 and §4.1 are explicit for all `n ≥ 4`,
  resp. `n ≥ 2`).

**Bottom line.** The shadow / Kruskal–Katona angle does not beat the entropy
method, and it adds a *new, sharp* obstruction the other four attacks did not
have: **the standard compression/shifting operator does not preserve
union-closure** (minimal witness `{{0,1},{2,3},{0,1,2,3}}`), and the shadow,
profile, and Ahlswede–Daykin/FKG levers all fail on the Boolean-cube extremizer —
which is shadow-trivial. The one live brick is a *join-respecting* compression
acting on the JI-labelling, the same fibre/labelling chokepoint identified by the
lattice attack.
