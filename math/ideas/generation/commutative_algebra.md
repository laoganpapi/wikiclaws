# Commutative-algebra attack directions for Frankl's union-closed conjecture

**Field:** Stanley–Reisner theory, monomial free resolutions, local cohomology,
Alexander duality (Hochster, Reisner, Eagon–Reiner, Gasharov–Peeva–Welker).
**Author role:** generation-wave proposer (directions, not proofs).
**Date:** 2026-06-03.
**Status:** `[NOVELTY UNVERIFIED — arXiv 403 this session; the lcm-lattice/GPW and
Eagon–Reiner dictionaries are classical, the Frankl framing below is flagged new
but plausibly folklore]`.
**Companion code (new, self-contained):** `math/ideas/generation/sr_probe.py`
(reuses only `frankl/experiments/{enumerate,uc_family}.py` read-only).
**Data:** `math/ideas/generation/sr_probe_n5.jsonl`.
**Honors the proven barriers:** the *moment* barrier (every symmetric convex
moment of the frequency vector is flat-minimized by the cube at ½) **and** the
*cone* barrier (`frankl/theory/lattice_attack.md` §4: abundance is **not** a
lattice invariant — `cone(G) ≅ G` as a lattice but abundance jumps from ½ to
`1−1/|L|`). The second barrier is the harder one for this field and I confront it
head-on below.

---

## 0. TL;DR (honest verdict up front)

* **The right monomial object is forced and clean:** a union-closed family **is**
  an lcm-closed set of squarefree monomials, so its **lcm-lattice is exactly
  `L=(F,⊆,∪)`** and (Gasharov–Peeva–Welker) the *entire* multigraded free
  resolution of the ideal `I_F` is read off the **order complexes of open
  intervals of `L`**: `β_{i,A}(I_F)=\dim \tilde H_{i-2}((\hat0,A)_L)` for `A∈L`.
* **Homological invariants genuinely ESCAPE the moment barrier:** they are
  **non-flat on the cube**. The cube `2^{[k]}` has ideal `I_F=(x_1,…,x_k)=\mathfrak m`,
  resolved by the **Koszul complex** — `projdim=k`, `reg=1`, total Betti `2^k−1`,
  strictly growing in `k`. No symmetric convex moment does that (they are all
  pinned flat at ½). **Verified** `n≤5` (`sr_probe.py` CONTROL block).
* **But the COARSE (Z-graded / iso-invariant) homology is killed by the cone
  barrier**, exactly as predicted: `projdim, reg, total Betti` are invariants of
  the abstract lattice `L`, so `cone` leaves them fixed while abundance moves.
  Coarse homology therefore *cannot* bound abundance. (This is the cone barrier
  re-derived in homological language — a clean "why not".)
* **The live escape is the FINE multigrading**, indexed by the actual subsets
  `A⊆[n]` — the *labelling* data (open problem F.2) the cone shuffles but does not
  erase. I built and tested the most natural fine-graded forcing rule
  (a "homology-load" element). **It nearly works (29 732/29 738 at `n≤5`) but
  fails on 6 parasitic families** in the *same wrong-sign way* the second-moment
  lever failed (`frankl/theory/ji_overlap_inequality.md` §4). So this exact rule
  is **not** a proof, but the failure is diagnosed and points to the one sub-
  direction I would actually pursue: **Alexander duality / Eagon–Reiner**, where
  abundance becomes a *degree in the dual resolution* and the cube is non-flat.

**Plausibility: 2.5/5** (down-weighted by the cone barrier, up-weighted because
homology is the first invariant in this project that is provably non-flat on the
cube). Best single bet inside the field: **§5 (Eagon–Reiner)**.

---

## 1. Which complex, which invariant

### 1.1 The forced object: the monomial ideal `I_F` and its lcm-lattice `= L`

Encode `A∈F` as the squarefree monomial `m_A=∏_{i∈A}x_i∈k[x_1,…,x_n]`. Then
**`union = lcm`**, so:

> **`F` union-closed ⟺ `{m_A}` is closed under lcm ⟺ the lcm-lattice of the ideal
> `I_F=(m_A : A a minimal member of F)` is exactly `L=(F,⊆,∪)`** (with `\hat0=∅`,
> `\hat1=⋃F`). The minimal members are the atoms of `L`; every other element of
> `L` is an lcm of atoms.

This is not a modelling choice — it is the canonical commutative-algebra avatar of
"closed under join." It pulls in the full toolkit:

* **Gasharov–Peeva–Welker (lcm-lattice).** The multigraded Betti numbers are
  $$\beta_{i,A}(I_F)=\dim_k \tilde H_{i-2}\big((\hat0,A)_L\big),\qquad A\in L,$$
  where `(\hat0,A)_L` is the **open interval** in `L` and `\tilde H` is reduced
  simplicial homology of its order complex. (Equivalently Hochster's formula on
  the lcm-lattice.) So *the whole resolution is poset topology of `L`, graded by
  the actual subsets `A`.*
* **Eagon–Reiner / Alexander duality.** For the Stanley–Reisner ideal of a complex
  `Δ`, `reg(I_Δ)=\projdim k[Δ^∨]` and `Δ` is Cohen–Macaulay ⟺ `I_{Δ^∨}` has a
  linear resolution. This is the second, dual lens (§5).
* **Reisner / Hochster (local cohomology).** Depth and `\tilde H^i_{\mathfrak m}`
  via links — the depth/shellability side the brief flags.

### 1.2 The invariants I bring

`projdim I_F`, `reg I_F`, total and **fine** multigraded Betti `β_{i,A}`, the
**Alexander-dual projective dimension** (`= reg`), and the per-element **homology
load** `S(x):=∑_{A∋x}∑_i β_{i,A}` (a labelling-weighted, non-symmetric scalar).

---

## 2. WHY it escapes the moment barrier (non-flat on the cube)

The moment barrier says: every symmetric convex moment `∑_x φ(freq(x))` is
*flat-minimized* by the cube at ½ — the cube's frequency vector is constant
`(|F|/2,…,|F|/2)`, so it kills the second-order term every such functional relies
on. Homological invariants are **not** functionals of the frequency vector at all;
they are functionals of the *incidence/lcm structure*. Concretely:

> **Non-flatness on the cube (the escape, verified `n≤5`).** For `F=2^{[k]}` the
> minimal members are the `k` singletons, so `I_F=(x_1,…,x_k)=\mathfrak m` and the
> minimal resolution is the **Koszul complex**:
> $$\beta_{i,A}= \mathbf 1[\,|A|=i,\ A\subseteq[k]\,],\quad
> \projdim=k,\ \reg=1,\ \text{total Betti}=2^k-1.$$
> These **grow with `k`** and depend on the cube's exact incidence — the polar
> opposite of a flat moment. (`sr_probe.py` CONTROL: cube total Betti
> `1,3,7,15,31` for `|F|=2,4,8,16,32`.) A symmetric convex moment cannot see this:
> it only sees `freq≡|F|/2`.

So *as functionals*, homological invariants live outside the moment cone — they
are exactly the "non-symmetric, structural, sensitive to actual face/incidence
structure" data the brief asks for. **This part is clean and is the reason the
field is worth a look.**

The catch is the *second* barrier, §3.

---

## 3. The cone barrier, re-derived homologically (the honest obstruction)

The cone `G ↦ cone(G)={∅}∪\{A∪\{z\}:A∈G,A≠∅\}` adjoins a fresh variable `x_z` to
every minimal generator: `I_{cone(G)} = x_z · I_G'` (up to the bottom). Two facts:

> **3.1 `cone(G) ≅ G` as a lattice ⇒ same lcm-lattice ⇒ identical coarse
> homology.** By GPW, `β_{i,A}` is read off `L`'s open intervals; an lcm-lattice
> isomorphism preserves all `β_i` (the Z-graded Betti), `projdim`, `reg`, depth,
> total Betti. So **every coarse/iso-invariant homological number is constant
> along the cone family**, while abundance runs from ½ to `1−1/|L|`. *(Verified:
> `sr_probe.py` CONTROL — coarse Betti does **not** separate `abund<.55` from
> `≥.55`; means overlap.)*

> **3.2 Homologically, the abundant element is the variable that divides
> everything — a *cone apex*, which TRIVIALIZES rather than creates homology.**
> If a variable `x` divides every minimal generator (`x∈` every minimal member),
> then `x` is in every member (up-closure), so `freq(x)=|F|`, abundance `1`. In
> the resolution this `x` factors out: `I_F=x·I'`, the resolution is just shifted,
> and **`x` contributes no homology of its own** — it is a Koszul/cone apex.
> *(Verified: `sr_probe.py` TEST1 — 834 families have such a variable; they are
> the high-abundance ones, but the abundant element there is homology-trivial.)*

**Consequence (the obstruction):** abundance correlates with being a *cone-apex
variable*, which is precisely where homology is **absent**. So you cannot read
abundance off "where the homology is" — on the worst (lopsided/parasitic)
families the homology concentrates on the *low*-frequency elements. This is the
**same wrong-sign / parasite mechanism** that defeated the second-moment and
JI-overlap levers (`ji_overlap_inequality.md` §4): one heavy near-apex element
(little homology) plus several light "parasitic" elements (where the resolution is
complicated). The cone barrier and the moment barrier meet here.

---

## 4. Concrete computation done + small validation (`n≤5`)

`sr_probe.py` computes, for **all 29 738 UC families** (`∅` adjoined, nonempty
ground set, `n≤5`): GPW total Betti, `projdim`, the fine `β_{·,A}`, the
homology-load `S(x)=∑_{A∋x}β(\text{interval}(\hat0,A))`, and the
common-divisor/apex variables. (Homology computed by F_p boundary-rank; the cube
Koszul numbers reproduce exactly, validating the code.)

**Tested forcing rule (the most natural fine-graded one):**

> **Rule (homology-load witness).** Let `x^\* = \arg\max_x S(x)`. Claim:
> `freq(x^\*) ≥ |F|/2` (a *homologically distinguished* element is abundant).

**Validation result `n≤5`:**

| test | result |
|---|---|
| Rule holds (homology-heaviest element clears ½) | **29 732 / 29 738** |
| Rule FAILS | **6** families, all `n=5` |
| within-family `cov(freq, S)` sign | **+24 296 / −1 538 / 0:3 904** (usually abundant ⇒ homology-heavy) |
| inverted rule ("abundant = homology-lightest") | fails **10 324** — decisively worse |
| cube non-flat (CONTROL) | total Betti `1,3,7,15,31`, `projdim=k` ✓ |

The **6 failures** are the parasitic families, e.g.
`freqs=[13,10,9,9,8], S=[4,4,6,4,4]` (`|F|=17`, abundance `0.765`): the abundant
element (freq 13) has *below-average* homology load `4`, while the
homology-heaviest element (load 6) has freq `9<|F|/2`. Same shape as the
`ji_overlap` minimal counterexample (a near-universal element + parasites). So
**the rule is true for 99.98 % of `n≤5` families but is genuinely FALSE**, and its
failure mode is the project's recurring max-vs-mean / parasite wall — now
re-derived an *n*-th way through homology. No constant `>½` is established.

**What is solid and reusable:** (i) the cube non-flatness (escape from the moment
barrier), (ii) the exact dictionary abundance ↔ cone-apex-variable ⇒ homology
trivialization (the obstruction), (iii) a clean, fast `n≤5` homological census.

---

## 5. The one sub-direction I would actually pursue: Eagon–Reiner / Alexander duality

The §3 obstruction says *primal* homology has the wrong sign (abundant = where
homology is absent). **Alexander duality flips exactly this.** Build the
Stanley–Reisner complex `Δ_F` on `[n]` whose faces are the **complements of
members of `F`** (or, dually, encode `F` as the *minimal non-faces* of a complex);
then by **Eagon–Reiner**:
$$\reg(I_F)=\projdim k[\Delta_F^{\vee}],\qquad
\beta_{i,A}(I_F)=\beta_{?,\,[n]\setminus A}(I_{\Delta_F^\vee}).$$

Under duality, *"`x` divides every generator" (apex, abundance-1)* becomes
*"`x` is in no minimal non-face on the dual side"* — i.e. abundance maps to a
**low** homological degree / a **free** direction of the *dual* module, which is
where dual invariants are *large*. Two precise things to attempt (network-enabled
pass):

> **5.1 Target.** Express abundance `max_x freq(x)/|F|` as (a monotone function of)
> a **multigraded degree of `H^•_{\mathfrak m}(k[\Delta_F^\vee])`** (local
> cohomology via Hochster's *dual* formula, indexed by **links** `lk_{Δ^\vee}(W)`).
> Links are *non-symmetric* and survive the cone with a controlled shift (the apex
> variable becomes a *deletion*, not a contraction, on the dual). The hope: the
> top-degree socle / canonical-module generators of `k[\Delta_F^\vee]` sit on the
> abundant element with the *right* sign, undoing §3.2.

> **5.2 Cube check (must be non-flat).** For `2^{[k]}`, `I_F=\mathfrak m`, dual
> `Δ^\vee` is the boundary of the simplex, `k[\Delta^\vee]` Cohen–Macaulay,
> `reg=1`; the dual invariants are again `k`-dependent (non-flat) — so the cube
> does *not* trivially saturate, unlike every moment. This is the prerequisite the
> brief asks for, and it passes.

> **5.3 First lemma to attempt.** Prove or refute, on `n≤5` first:
> *the element `x` maximizing the number of top-multidegree socle elements of
> `k[\Delta_F^\vee]` supported away from `x` is abundant.* If the dual sign is
> right, the 6 §4 failures should flip to successes. This is a 1-day script
> extension of `sr_probe.py` (compute `Δ_F^\vee`, its SR-ideal, Eagon–Reiner
> `β_{·,W}` by the same open-interval homology on the dual lcm-lattice).

A second, structural sub-direction (the brief's shellability prompt): the order
complex `Δ(L)` is **Cohen–Macaulay / shellable** for many `L` (e.g. the cube's is
the Coxeter/barycentric sphere), but **CM-ness is a lattice invariant ⇒ cone-dead
for abundance**, so shellability *per se* cannot force abundance. The non-dead
refinement is **`A`-graded shellability**: a shelling order compatible with the
*set labels* (which subset `A⊆[n]` each face carries). That is again the F.2
labelling, and is the only place a shelling argument could bite — but I have no
concrete handle on it and rate it below §5.1.

---

## 6. Plausibility, failure modes, novelty

**Plausibility: 2.5 / 5.**
* `+` Homology is the **first invariant in this project provably non-flat on the
  cube** (Koszul) — it truly escapes the *moment* barrier, unlike SOS-of-the-
  frequency-vector, entropy, second moment, etc.
* `+` The lcm-lattice = `L` identity and GPW formula give an exact, computable,
  *labelling-graded* handle (the fine `β_{i,A}`), which is genuinely F.2 data.
* `−` The **cone barrier is brutal**: it kills *every* coarse/iso-invariant
  homological number outright (§3.1), and worse, the *sign* is wrong — abundance
  lives at cone-apex variables, where homology is *absent* (§3.2). The natural
  fine-graded rule inherits the parasite failure (§4, 6 counterexamples).
* The only credible route is **§5 (Alexander duality)**, which is duality-flips-
  the-sign *speculation* until the §5.3 script is run.

**Failure modes (how this dies):**
1. **Dual sign also wrong.** If Eagon–Reiner duality maps the parasite families to
   *dual* parasite families (likely — duality is an involution, it may just relabel
   the obstruction), §5 dies the same death as §4. This is my leading worry.
2. **Coarse-only forcing.** Any rule that ends up depending only on
   `projdim/reg/total Betti` is automatically cone-dead. A live rule **must** use
   the multidegrees `A⊆[n]` essentially; it is easy to fool oneself here.
3. **CM/shellable is a lattice invariant** ⇒ cannot force abundance (cone). Only
   *label-graded* shellability could, and I have no lever on it.

**Discipline check.** No proof claimed; no constant `>½` claimed; the cube
saturates nothing here (it has *maximal* homology, not flat) — so this does not
trip the "cube must be tight/flat" red-team in the moment sense, but it *does*
sit behind the cone barrier, which I have stated explicitly rather than hidden.

**`[NOVELTY UNVERIFIED]`** — lcm-lattice/GPW (Gasharov–Peeva–Welker 1999),
Eagon–Reiner (1998), Reisner (1976), Hochster (1977) are classical; the Frankl
framing (abundance ↔ cone-apex variable ↔ homology trivialization; the dual
socle/abundance target) is flagged new but is plausibly folklore. arXiv 403 this
session — prior-art uncheckable.

---

## 7. Reproduction

```
cd math/ideas/generation
python3 sr_probe.py 5       # -> sr_probe_n5.jsonl  (~9 min, 29 738 families)
# prints: CONTROL (cube Koszul, coarse-Betti non-separation),
#         TEST1 (apex variable => abundance, homology-trivial),
#         TEST3 (homology-load rule: 6 failures), TEST5 (sign of cov(freq,S)).
```

**Step-1 (computational): PASS** (homology code validated against the cube's
Koszul numbers). **Steps 2–4: N/A** — this is a generation-wave *direction*, not a
theorem. The deliverable is: (a) the cube-non-flatness escape from the moment
barrier, (b) the homological re-derivation of the cone barrier as the obstruction,
(c) one live sub-direction (Eagon–Reiner/Alexander duality, §5) with a concrete
`n≤5` first script to run next.
