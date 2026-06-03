# The join-irreducible / fibre-labelling structure of Frankl's union-closed conjecture

**Author:** Alex Ye (no AI on author line).
**Date:** 2026-06-03.
**Status:** `[NOVELTY UNVERIFIED — the fibre=filter / Birkhoff-JI dictionary is
classical (Birkhoff 1937, Poonen 1992); the *quantitative* fibre-overlap framing
below is flagged new but very likely folklore. arXiv 403 this session.]`
Deliverable is a **sharp structural characterization of the labelling freedom**
(open problem F.2) plus a **diagnosed forcing constraint** — **NOT a proof**.
**Companion code:** `frankl/experiments/ji_labelling.py`,
`ji_labelling_sweep.py`, `ji_labelling_h5.py`, `ji_labelling_constraint.py`.
**Data:** `frankl/experiments/data/ji_sweep_n{0..5}.jsonl`,
`ji_summary.txt`, `ji_h5_summary.txt`, `ji_h5_classes.jsonl`,
`ji_constraint_summary.txt`.
**Tests:** `tests/test_ji_labelling.py` (9 tests, pass).
**Cross-ref:** `lattice_attack.md` §1.4 (fibre=filter, the dictionary), §4 (cone
obstruction), open problem F.2; `lp_duality.md` §6 (max-vs-mean / second moment);
`shared/dead_ends.md` (my entry below; 0.43/0.5 budget traps).
**Foundation:** `lattice_attack.md` — this note attacks the fibre/JI system the
five-method convergence pinpointed, *directly*, not via any lattice invariant.

> **What this is.** The convergence of six independent methods (entropy,
> polynomial, lattice invariants, Boolean Fourier, Kruskal–Katona/shadows, LP
> duality) located the obstruction at the **labelling of join-irreducibles**:
> abundance is the max density of a ground-element fibre, each fibre is a *filter*
> of the lattice, and which filters arise (the labelling) is free given the
> abstract lattice (the cone, `lattice_attack.md` §4). This note attacks that
> fibre system head-on. The honest outcome — the realistic one — is:
> 1. **A sharp extremizer characterization (H5):** over all 13,734 exact
>    lattice-iso classes at n≤5, the worst labelling reaches abundance **exactly
>    1/2 only for the Boolean cubes `B_k`** and is **strictly > 1/2 for every
>    other lattice**. The cube is the *unique* minab=1/2 extremizer.
> 2. **A precise localization of the difficulty (H1/H2 both FALSE):** the
>    *principal* (single join-irreducible) fibres do **NOT** suffice — in 2,254
>    families abundance ≥ 1/2 while **no single JI-filter reaches 1/2** — and the
>    co-atom/meet-irreducible fibres are far worse. Abundance is a genuine
>    **union-of-JI-filters** quantity.
> 3. **The forcing constraint to attack:** the reconstruction identity
>    `Fib(x) = ⋃_{j∈JI, x∈j} ↑j` (verified, 0 violations) means abundance lives in
>    the **overlap of the join-irreducible filters that share the top `T`**, not
>    in their individual sizes. This is the single most promising lever (§6).

All numbers validated on **all 29,723 UC families with |F|≥2, n≤5** (the
project's standard census; Frankl holds, min abundance exactly 0.5).

---

## 1. The fibre / JI formalization (operational)

Fix `F` union-closed with `∅ ∈ F`, so `L = (F, ⊆, ∪)` is a lattice with bottom
`0̂ = ∅` and top `T = ⋃F`. (`ji_labelling.with_bottom`, `lattice.as_lattice`.)

**Fibre.** For a ground element `x ∈ [n]`, `Fib(x) = {A ∈ F : x ∈ A}`. Each
`Fib(x)` is a **filter** (up-set) of `L`. *(Verified exhaustively n≤4,
`test_fibre_is_a_filter`.)*

**Abundance.** `abundance(F) = max_x |Fib(x)|/|L|`. Frankl ⟺ some `Fib(x)` has
density ≥ 1/2. *(Eq. (1.1) of `lattice_attack.md`.)*

**Join-irreducibles (JI).** `j ∈ L` with a unique lower cover; in `L=(F,∪)` the
JIs are the members of `F` that are not unions of strictly smaller members
(`lattice.join_irreducibles`). By **Birkhoff**, every `A ∈ L` is
`A = ⋁{j ∈ JI : j ≤ A}`.

**The dictionary (recap, `lattice_attack.md` §1.4).** Let `m_x = ⋀ Fib(x)`. Then
`Fib(x) = ↑m_x` is a **principal** filter ⟺ `x ∈ m_x`, in which case `m_x` is a
join-irreducible and `freq(x) = |↑m_x|`. When `x ∉ m_x` (only possible in
non-distributive `L`), `Fib(x)` is a **non-principal** filter — a union of ≥2
principal JI-filters — and `x` corresponds to no single JI. *(Verified:
`test_principal_iff_x_in_meet`.)*

**The reconstruction constraint (the data invariants throw away).** The fibre
*system* `{Fib(x)}_{x∈[n]}` is not an arbitrary collection of filters: it must
reconstruct `F`, i.e. `A = {x : A ∈ Fib(x)}` for every `A`. Operationally this is
the exact identity
$$
\boxed{\ \mathrm{Fib}(x)\;=\;\bigcup_{\,j\in JI(L),\ x\in j\,}\ {\uparrow}j\ }
\tag{R}
$$
— each fibre is the **union of the principal JI-filters of the JIs that contain
`x` as a ground element**. *(Verified: 0 violations over all 29,723 families,
`ji_constraint_summary.txt`; `test_reconstruction_identity_H3`.)* This is the
coupling between filters that the lattice/spectral/LP invariants discard, and it
is where abundance lives.

---

## 2. H1 — principal (join-irreducible) fibres do NOT suffice (FALSE)

**Question.** Among principal filters `↑j` (`j` a JI), is the max density ≥ 1/2?

**Answer: NO, and decisively.** *(`ji_summary.txt`, `ji_constraint_summary.txt`.)*

| quantity | value (n≤5, 29,723 families) |
|---|---|
| min over families of `max_j |↑j|/|L|` (best single JI-filter density) | **0.2353** |
| families where `max_j |↑j|/|L| ≥ 1/2` | 27,469 / 29,723 |
| families where the best single JI-filter is `< 1/2` **yet abundance `≥ 1/2`** | **2,254** |
| families where abundance **strictly beats** the best single JI-filter | **11,230** |
| max gap `abundance − max_single_JI_density` | **0.5833** |

The clean witness is **M3** (`F = {∅,{0,1},{0,2},{1,2},{0,1,2}}`): every fibre is
**non-principal** (every `x ∉ m_x`), each single JI-filter has density `2/5 = 0.4`,
but each fibre is a union of **two** JI-filters sharing the top, giving abundance
`3/5 = 0.6`. *(`test_h1_false_M3`.)*

**One positive fact (a weak lower bound).**
`abundance(F) ≥ max_j |↑j|/|L|` holds for **all** 29,723 families
(`test_abundance_ge_single_ji_density_exhaustive`). So the Poonen/principal
quantity is a genuine *lower* bound on abundance — but a useless one (it dips to
0.2353). **Single join-irreducibles are the wrong object;** the union is essential.

---

## 3. H2 — co-atom / meet-irreducible fibres are worse (FALSE)

**Question.** Does the meet-irreducible / co-atom structure fare better?

**Answer: NO, much worse.** A co-atom `c` (lower cover of `T`) generates the
principal filter `↑c = {c, T, …}`, which is *tiny* (density `2/|L|` for a single
co-atom). *(`ji_summary.txt`.)*

| quantity | value |
|---|---|
| families where some co-atom filter density `≥ 1/2` | **133** / 29,723 |
| max-over-families of (max co-atom filter density) | 1.0000 (only `|L|=2`) |
| min-over-families of (max co-atom filter density) | 0.0625 |
| families where max meet-irreducible filter density `==` abundance | 340 |

Co-atom/meet-irreducible fibres almost never carry abundance: they are the
*small* end of the filter lattice. Abundance lives at the **join-irreducible
(bottom) end**, in unions — confirming the JI labelling, not the MI structure, is
the locus. *(`test_coatom_filter_is_small`.)*

---

## 4. H3 — the counting identity is the averaging identity (no forcing alone)

The reconstruction (R) yields the exact identity
`Σ_x |Fib(x)| = Σ_A |A|` (0 violations, `test_reconstruction_identity_H3`).
This is **the same first-moment averaging identity** that the LP/Reimer method
reduces to (`lp_duality.md` (1.1)). On its own it forces only the *mean* fibre
density `= s̄(F)/n`, which the cube pins at exactly 1/2 with zero margin
(`lp_duality.md` §4). So **H3 alone cannot force a heavy fibre** — it is the
max-vs-mean gap again. What (R) adds beyond the bare identity is the *filter*
structure of each summand (§6), which the LP throws away.

---

## 5. H5 — the labelling freedom: the cube is the UNIQUE minab=1/2 extremizer

**Question.** For a fixed abstract lattice `L`, range over all valid
ground-element labellings (concrete UC realizations iso to `L`). What is the worst
labelling `minab(L) = min{abundance(F') : F' ≅ L}`? Can it push below 1/2? Is the
worst always the cube-like 1/2?

**Method.** Bucket all UC families (n≤5) by a strong iso-invariant fingerprint
(`ji_labelling.lattice_fingerprint`: size/height/width/#JI/#MI/#atoms/
distributive/modular/lsm/usm + Hasse in/out-degree sequences + principal-filter-
size multiset), then split each bucket into **exact** lattice-iso classes with a
back-tracking cover-digraph isomorphism (`ji_labelling_h5.exact_lattice_iso`).
This yields **13,734** exact iso classes. *(`ji_h5_summary.txt`.)*

**Result (sharp).**

| `minab(L)` over the 13,734 classes | count |
|---|---|
| `< 1/2` (would refute Frankl) | **0** |
| `= 1/2` **exactly** (worst label is cube-like) | **5** |
| `> 1/2` | **13,729** |

> **Characterization 5.1 `[NOVELTY UNVERIFIED]`.** The **only** lattices whose
> worst labelling attains abundance exactly `1/2` are the **Boolean cubes `B_k`**
> (`|L| = 2,4,8,16,32`, k = 1..5), each realized at the minimum by the standard
> cube `2^[k]`. For **every other** lattice at n≤5, the labelling freedom
> **cannot** push abundance below `1/2 + ε(L)` for a strictly positive `ε(L)`.
> *(`ji_h5_classes.jsonl`; the 5 minab=1/2 class sizes are exactly the powers of 2;
> `test_cube_worst_label_is_half`.)*

This is the **deepest version of the obstruction** for open problem F.2: the
labelling freedom (the cone's mechanism, `lattice_attack.md` §4) lets you *raise*
abundance toward 1 on any lattice, but it can *lower* abundance to the FUCC
boundary `1/2` only on the Boolean cube. The cube is therefore not merely *an*
extremizer (`lp_duality.md`, `boolean_fourier.md`) — it is the **unique** lattice
at which the worst labelling is exactly tight.

**The spread (labelling freedom quantified).** The same lattice can host very
different abundances by relabelling: e.g. the `B_3` lattice ranges `0.5 → 0.875`
(cube vs cone), and large-spread classes reach spread `0.4` (`ji_h5_summary.txt`,
"Large-spread classes"). This is the cone phenomenon, now resolved per-lattice.

**Honest scope caveat.** `minab(L)` here is the minimum over realizations that
**fit in n≤5**. A non-cube lattice could in principle have a lower-abundance
realization at larger `n` (the census is incomplete above n=5). The **cube
result is robust** because the cube `2^[k]` is itself a realization (not
truncated), so `minab(B_k) = 1/2` is exact for all `k`; what n≤5 cannot certify is
that *no other* lattice reaches `1/2` at larger `n`. The claim "cube is the unique
extremizer" is therefore **`[PENDING — n≤5 only]`**, consistent with but not
proving the asymptotic statement.

---

## 6. H4 + the single most promising structural constraint

**H4 (rigid lattices).** Restricting to lattices where the JI-labelling is most
rigid: classes where **every** non-bottom element is join-irreducible (5 classes
at n≤5; these are essentially chains/near-chains) all have `minab ≥ 1/2` (min
exactly 0.5); classes with `|JI| = n` at the representative (772 classes) likewise
`minab ≥ 1/2`. Rigidity does not make Frankl *false*, and these are exactly the
lattices where the principal-fibre lower bound of §2 is *tight* (each ground
element is its own JI), so Frankl reduces to the Poonen statement there — the
*easy* case. The **hard** case is the opposite: many ground elements sharing few
JIs (M3-like), where unions dominate. *(`ji_h5_summary.txt` H4 block;
`test_chain_all_ji_meets_frankl`.)*

**The constraint to attack (§6, the deliverable lever).** Combining §2–§5: the
heavy fibre is, by (R), a **union of principal JI-filters that all contain the top
`T`**. Single filters are too small (§2, min 0.2353); their *union* carries
abundance (11,230 families need it strictly; 2,254 need it to clear 1/2). So the
right inequality is not about `|↑j|` but about the **overlap geometry of the JI-
filters**:

> **Candidate forcing constraint 6.1 `[NOVELTY UNVERIFIED — not proved]`.** Order
> the JIs `j_1,…,j_r`. Every `↑j_i ∋ T`, so the filters pairwise intersect (in at
> least `↑(j_i ∨ j_k)`). The reconstruction (R) writes each fibre as a union over
> a *down-closed-in-JI* set `J(x) = {j : x ∈ j}`. Frankl is the statement that
> **some union `⋃_{j∈J(x)} ↑j` covers ≥ half of `L`.** The lever is a *union
> bound run in reverse* (an inclusion–exclusion / covering inequality) on the
> JI-filters, constrained by:
> - **(a)** the filters all share `T` (and more: `↑j_i ∩ ↑j_k ⊇ ↑(j_i∨j_k)`), so
>   overlaps are *structured*, not free;
> - **(b)** the label sets `{lab(j)}` (which `x` pick up which `j`) must have
>   union `[n]` and reconstruct `F` — the §1 (R) coupling;
> - **(c)** `Σ_j |↑j|` is fixed by the first moment (§4), so a *second-moment /
>   overlap* control `Σ_{j,k} |↑j ∩ ↑k|` would feed a power-mean / Cauchy–Schwarz
>   bound `max_x |Fib(x)| ≥ (Σ overlaps)/(Σ sizes)` — exactly the **second-moment
>   valid inequality** flagged as the live lever in `lp_duality.md` §6, but now
>   localized to the **JI-filter overlap** rather than the raw frequency vector.

This is the precise, structural form of the `lp_duality.md` "max-vs-mean / second
moment" lever: the missing inequality is a **lower bound on the JI-filter overlap
`Σ_{j,k} |↑j ∩ ↑k|`** from union-closure, which would force a heavy union via
Cauchy–Schwarz while leaving the cube at exactly 1/2 (where all overlaps are the
single shared `T`, so the bound is tight — consistent with Characterization 5.1).
Whether union-closure supplies such an overlap lower bound is **open and not
established here**; it is the single most promising next brick, and it lives
entirely in the JI-labelling, exactly as open problem F.2 demands.

**Why the cube saturates it (consistency check).** For `2^[k]`: the JIs are the
`k` singletons `{i}`, each `↑{i}` has density `1/2`, any two filters
`↑{i} ∩ ↑{i'}` is the up-set of `{i,i'}` (density `1/4`), and each fibre is a
*single* `↑{i}` (the cube is distributive ⇒ all fibres principal). So no union
effect, abundance exactly `1/2`, overlaps exactly the generic `2^{k-2}` — the
overlap-bound is tight on the cube, matching that the cube is the unique
minab=1/2 extremizer (§5). The lever degenerates on the cube *by design*, like
every method in this project, so it can at best **reach** 1/2 — never exceed it.

---

## 7. Verdict

1. **H1 FALSE** — principal (single-JI) fibres dip to density 0.2353; in 2,254
   families abundance clears 1/2 with no single JI-filter reaching it.
2. **H2 FALSE** — co-atom/meet-irreducible fibres are the small end (≥1/2 in only
   133 families). Abundance lives at the join-irreducible / bottom end.
3. **Principal/co-atom fibres NEVER suffice** as a stand-alone certificate; the
   only positive is the weak lower bound `abundance ≥ max_j |↑j|/|L|`.
4. **Labelling-freedom characterization (H5):** over 13,734 exact iso classes,
   the worst labelling is `≥ 1/2` always, and `= 1/2` **only for the Boolean
   cubes** (unique extremizer); `> 1/2` for all 13,729 other lattices. The cube is
   the unique minab=1/2 lattice. `[PENDING — n≤5; cube part exact for all k.]`
5. **Most promising structural constraint:** a union-closure lower bound on the
   **JI-filter overlap** `Σ_{j,k}|↑j ∩ ↑k|` (Constraint 6.1), feeding a
   Cauchy–Schwarz/power-mean bound on the heavy union. This is the
   `lp_duality.md` second-moment lever **localized to the JI-labelling**, tight on
   the cube, and the precise next target for open problem F.2.

**No proof is claimed. No constant above 1/2 is claimed.** Every number is
exhaustively validated at n≤5; all framings are `[NOVELTY UNVERIFIED]`. The
0.43/0.5 budget-mismatch traps (`shared/dead_ends.md`) are **not** hit: the only
sub-1/2 numbers here (single-JI density 0.2353) are honestly *lower bounds that
fail*, explicitly flagged as "single JI is the wrong object," never dressed up as
a certificate.

## 8. Reproduction

```
cd math/frankl/experiments
python3 ji_labelling_sweep.py 5       # H1-H3  -> data/ji_sweep_n*.jsonl, ji_summary.txt
python3 ji_labelling_constraint.py 5  # (R) + single-vs-union -> ji_constraint_summary.txt
python3 ji_labelling_h5.py 5          # H4-H5 labelling freedom -> ji_h5_summary.txt, ji_h5_classes.jsonl
pytest tests/test_ji_labelling.py     # 9 tests
```

**Step-1 (computational): PASS.** 29,723 families n≤5; Frankl re-verified (min
abundance 0.5); reconstruction (R) 0 violations; H1/H2 false with explicit numbers;
H5 cube-uniqueness. **Steps 2–4 (red-team/Lean/human): N/A — no new theorem
claimed.** The deliverable is a structural characterization + a flagged open
constraint, not a bound. `[NOVELTY UNVERIFIED]` on all framings (Birkhoff/Poonen
dictionary classical; overlap framing very likely folklore).
