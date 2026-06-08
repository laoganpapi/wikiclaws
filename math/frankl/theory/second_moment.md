# Second-moment / variance valid inequality on Frankl's union-closed conjecture

**Author:** Alex Ye (no AI on author line).
**Date:** 2026-06-03.
**Status:** `[NOVELTY UNVERIFIED — second-moment / Reimer-on-pairs framings of Frankl
very likely exist in the literature (Reimer 2003 average-set-size; Kleitman-style
correlation); arXiv 403 this session. Every framing flagged. Deliverable is an
OBSTRUCTION — a SEVENTH delimited method — not a proof.]`
**Companion code:** `frankl/experiments/second_moment.py`, `second_moment_probe.py`.
**Data:** `frankl/experiments/data/secmom_n{0..5}.jsonl`, `secmom_summary.txt`,
`secmom_run.txt`.
**Cross-ref:** `lp_duality.md` §6 (the lever was surfaced there as "Candidate 6.2,"
the single live sub-direction; this document RESOLVES it); `lattice_attack.md` §4
(the cone / cube extremizer); `boolean_fourier.md` §1.3, §3 (level-1 identity and the
trivial-spectrum cube); `RED_TEAM_REPORT.md` + `shared/dead_ends.md` (the 0.43/0.45/0.5
budget-mismatch traps, and the prior six methods).

> **What this is.** A direct test of the ONE concrete lever the LP-duality attack left
> open: a **second-moment (variance) valid inequality** on element frequencies,
> `Σ_i freq_i² ≥ g(|F|, n)`, feeding the power-mean bound
> `max_i ab_i ≥ (Σ ab_i²)/(Σ ab_i)`. The honest expected outcome — anticipated by
> the brief and matching all six prior methods — is realized: **the Boolean cube pins
> the power-mean ratio at exactly ½, and is the minimizer of that ratio at its own
> parameters; union-closure supplies NO second-moment lower bound beyond the
> parameter-free Cauchy–Schwarz identity.** This is a **seventh obstruction**, with the
> same cube extremizer as the other six.

---

## 0. Headline, up front

1. **The exact identity (task a, PROVED + verified).** The second moment of the
   frequency vector counts total pairwise-intersection size over `F×F`:
   $$ M_2 := \sum_i \mathrm{freq}_i^2 = \sum_{(A,B)\in F\times F} |A\cap B|
      = 2m\,M_1 - U, \qquad U := \sum_{(A,B)} |A\cup B|, $$
   where `m=|F|`, `M_1 := Σ_i freq_i = Σ_A |A|`. Verified to exact integer equality on
   **all 29 723 UC families** (|F|≥2, n≤5): **0 violations** (`secmom_summary.txt`).

2. **Union-closure adds nothing to the second moment beyond Cauchy–Schwarz (task b,
   d).** The only inequality union-closure naturally supplies on `U` is an *upper*
   bound `U ≤ |T|·m²` (`T=⋃F∈F`), giving `M_2 ≥ 2mM_1 − |T|m²`. This bound is
   **never** tighter than the parameter-free Cauchy–Schwarz `M_2 ≥ M_1²/n_active`:
   Cauchy–Schwarz is strictly tighter on **all 29 723** families, the union bound on
   **0**. So **no `g(m,n)` stronger than the free Cauchy–Schwarz floor was found**, and
   the natural union-closure route to one is provably weak (§4).

3. **The cube minimizes the power-mean ratio at its parameters (task c, the
   obstruction).** The power-mean ratio `R(F) := M_2/(m M_1) = (Σ ab_i²)/(Σ ab_i)`
   equals **exactly ½** on `2^[k]` for every `k`. For **fixed (m, M_1)**, `R` is
   minimized by the *flat* frequency vector (Cauchy–Schwarz equality case); the cube
   IS the flat vector at its `(m,M_1)`, so the cube **attains the per-class minimum**
   `R=½`. Verified: in each of the 5 cube classes (`m=2,4,8,16,32`), `min R = ½`,
   achieved by the cube's flat vector (`secmom_summary.txt`).

4. **The dips below ½ are real but HARMLESS and USELESS (task c/e).** The *raw*
   power-mean ratio `R(F)` dips to **0.444** (min over all n≤5, at frequency vector
   `[1,1,1,1,2]`, `m=3`), confirming `lp_duality.md` §6. **Decisively:** among the
   **39** families with true abundance *exactly* ½ (the Frankl-tight families,
   including all cubes), `R` is **exactly ½ — min = max = 0.500000**, and **0** of them
   have `R<½`. Every sub-½ dip occurs at true abundance **strictly > ½**. So the
   power-mean lever (i) never threatens a would-be counterexample (harmless), and
   (ii) is undercut by non-cube families below ½ while pinned at ½ on the cube
   (useless as a certificate). Both facts together kill it.

5. **Multiplicity sub-direction (task d) is a dead end.** `r(C) := #{(A,B):A∪B=C}`
   satisfies `r(C)≥1` for all `C∈F` (take `A=B=C`); for the top `r(T)>1` always
   (`r(T)=1` on **0/29 723** families). But to *lower*-bound `M_2 = 2mM_1−U` one needs
   an *upper* bound on `U=Σ_C |C|r(C)`, and lower bounds on `r(C)` push `U` the wrong
   way (up), so they **weaken** the `M_2` bound. The multiplicity structure is real but
   has the wrong sign for this lever.

All numbers validated on **all 29 723 UC families with |F|≥2, n≤5**.

---

## 1. Set-up and the exact identity (task a)

Fix a union-closed `F ⊆ 2^[n]`, `m=|F|`, `freq_i = |{A∈F:i∈A}|`, `ab_i = freq_i/m`.
Two moments of the frequency vector:
$$ M_1 := \sum_i \mathrm{freq}_i = \sum_{A\in F}|A| = m\sum_i ab_i, \qquad
   M_2 := \sum_i \mathrm{freq}_i^2 = m^2\sum_i ab_i^2 . $$
`M_1` is the first-moment averaging identity (Reimer's object; `lp_duality.md` (1.1)).

> **Identity 1.1 (what the second moment counts).** For every family `F`,
> $$ M_2 = \sum_i \mathrm{freq}_i^2
>        = \#\{(i,A,B): i\in A,\ i\in B,\ A,B\in F\}
>        = \sum_{(A,B)\in F\times F} |A\cap B|. $$
> **Proof.** `freq_i² = |{A:i∈A}|·|{B:i∈B}| = #{(A,B):i∈A,i∈B}`. Sum over `i` and swap
> the order of summation: `Σ_i #{(A,B): i∈A∩B} = Σ_{A,B} #{i: i∈A∩B} = Σ_{A,B}|A∩B|.` □

So **the second moment is the total pairwise-intersection size over `F×F`** — a
correlation quantity. Now apply inclusion–exclusion `|A∩B| = |A|+|B|−|A∪B|`:

> **Identity 1.2 (union-closure form).** With `U := Σ_{(A,B)∈F×F}|A∪B|`,
> $$ M_2 = \sum_{A,B}(|A|+|B|-|A\cup B|) = 2m\!\sum_A|A| - U = 2m\,M_1 - U. $$
> **Union-closure enters here:** `A∪B∈F` for all `A,B`, so the multiset `{A∪B}` lives
> in `F`. Writing `r(C):=#{(A,B):A∪B=C}` (the **join multiplicity**, `Σ_C r(C)=m²`),
> $$ U = \sum_{C\in F} |C|\,r(C). $$

**Step-1 verification.** `M_2 = 2mM_1 − U` holds with **0 violations** (exact integer
arithmetic) on all 29 723 UC families n≤5 (`second_moment.py`; `secmom_summary.txt`).

The power-mean ("weighted-by-itself") bound is the reason a *lower* bound on `M_2`
would matter:
$$ \max_i ab_i \;\ge\; \frac{\sum_i ab_i^2}{\sum_i ab_i}
   \;=\; \frac{M_2}{m\,M_1} \;=:\; R(F) \;\ge\; \frac{1}{n}\sum_i ab_i \;=\;\text{mean}.
   \tag{PM} $$
`R(F)` is `≥ mean` and `> mean` exactly when the frequency vector is spread, which is
precisely the §5/§6 integrality gap of `lp_duality.md`. The whole question is whether
union-closure forces `R(F) ≥ ½` (or any useful constant).

---

## 2. The cube pins the power-mean ratio at ½ and minimizes it at its parameters (task c)

> **Lemma 2.1 (cube saturation).** For `F = 2^[k]`: `freq_i = 2^{k-1}` for all `i`, so
> `M_1 = k·2^{k-1}`, `M_2 = k·4^{k-1}`, `m=2^k`, and
> $$ R(2^{[k]}) = \frac{M_2}{m\,M_1} = \frac{k\,4^{k-1}}{2^k\cdot k\,2^{k-1}}
>    = \frac{4^{k-1}}{4^{k-1+? }} = \frac{1}{2} \quad\text{exactly, every }k. $$
> (Cleanly: `M_2/(mM_1) = (k4^{k-1})/(k 2^{2k-1}) = 4^{k-1}/2^{2k-1} = 2^{2k-2}/2^{2k-1}
> = ½`.) Verified k=1..7 (`secmom_summary.txt` cube table).

This is the same death as the LP averaging certificate (`lp_duality.md` Thm 4.1): the
cube is **perfectly flat** (`ab_i ≡ ½`), so `R = (Σ ab_i²)/(Σ ab_i) = ab_i = ½` with
zero margin. The deeper structural fact is that the cube *minimizes* `R` at its own
parameters:

> **Lemma 2.2 (flat vector minimizes `R` for fixed `(m,M_1)`).** Over all nonnegative
> integer frequency vectors with a fixed sum `M_1` on a fixed number of active
> coordinates `t`, the ratio `R = M_2/(mM_1) = (Σ freq_i²)/(mM_1)` is minimized exactly
> when the `freq_i` are as equal as possible (Cauchy–Schwarz / convexity of `x↦x²`),
> giving `M_2 ≥ M_1²/t` with equality at the flat vector. The Boolean cube realizes the
> **perfectly flat** vector `freq_i ≡ 2^{k-1}` at `(m,M_1)=(2^k, k2^{k-1})`, so it is
> the per-`(m,M_1)`-class minimizer with `R = ½`.

**Step-1 verification (decisive for "is the cube the minimizer?").** Bucketing all
families by `(m, M_1)` and taking `min R` per bucket: in each of the 5 cube buckets
(`(2,1),(4,4),(8,12),(16,32),(32,80)`) the minimum is **exactly ½, attained by the
cube's flat vector** `[1],[2,2],[4,4,4],[8,8,8,8],[16,16,16,16,16]`
(`second_moment_probe.py`, "CUBE BUCKETS" block). So:

> **Answer to task (c): YES, the cube minimizes the power-mean ratio at its
> parameters, so the lever caps at exactly ½.** Like averaging, the second-moment
> ratio is a symmetric/convex functional saturated at its boundary by the flat
> extremizer; it cannot certify `max_i ab_i ≥ ½+ε`.

---

## 3. The dips below ½ are real, harmless, and useless (task c/e)

The *raw* power-mean ratio (not restricted to fixed parameters) does dip below ½:

> **Finding 3.1.** Over all 29 723 UC families n≤5, `min_F R(F) = 0.444…`, at frequency
> vector `[1,1,1,1,2]` (`m=3`, `n=5`); exactly **6** families have `R < ½` (min 0.444,
> then 0.467, …). This reproduces `lp_duality.md` §6's "min 0.444, refuted as a
> standalone certificate." (`secmom_summary.txt`, power-mean block.)

But the decisive cut is **what abundance those dips occur at**:

> **Finding 3.2 (decisive — the lever never touches the Frankl-tight families).**
> Among the **39** UC families with true abundance **exactly ½** at n≤5 (the
> conjecture's tight cases, which include all Boolean cubes `2^[k]`), the power-mean
> ratio `R` is **exactly ½ for every one** — `min R = max R = 0.500000`, and **0** of
> them have `R<½`. Every family with `R<½` has true abundance **strictly > ½** (the
> `[1,1,1,1,2]` witness has abundance `2/3`). (`second_moment_probe.py`, "P2" block.)

Consequences, both negative:
* **Harmless.** The sub-½ dips never coincide with an abundance-½ (would-be
  counterexample) family, so the lever's failure cannot produce a false alarm. The dip
  is an artifact of spreading the frequency vector at *high* abundance.
* **Useless.** On the extremizer it is pinned at exactly ½ (Lemma 2.1/2.2), and on
  other families it is *undercut* below ½ — so `R(F) ≥ ½` is **false** as a universal
  inequality, hence cannot be a certificate. This is the same shape as the LP cover
  certificate's behavior (`lp_duality.md` §5): caps at ½ on the cube, real sub-½ gap
  elsewhere.

`[NOTE — TRAP AVOIDED.]` This 0.444 is **not** a budget-mismatch artifact (cf. the
0.43/0.45/0.5 traps in `dead_ends.md`): it is the honest value of `(Σ ab_i²)/(Σ ab_i)`
on a genuine UC family, exactly as the LP doc's 0.40 is the honest averaging value. The
trap would be to read `R < ½` as evidence *against* Frankl; Finding 3.2 shows `R` and
the true abundance decouple precisely on the tight families, so no such inference is
available.

---

## 4. Union-closure supplies no second-moment lower bound (task b, d)

To get a *useful* `g(m,n)` with `M_2 ≥ g`, union-closure must beat the parameter-free
Cauchy–Schwarz floor `M_2 ≥ M_1²/n_active` (Lemma 2.2), which uses NO closure. Via
Identity 1.2, lower-bounding `M_2 = 2mM_1 − U` is the same as **upper**-bounding
`U = Σ_C |C|r(C)`.

> **Finding 4.1 (the union-closure-aware bound is never tighter).** The natural
> union-closure upper bound is `|A∪B| ≤ |T|` (`T=⋃F∈F`, so this *is* a closure fact:
> the top is a member), giving `U ≤ |T|·m²` and hence
> $$ M_2 \;\ge\; 2mM_1 - |T|\,m^2. $$
> This holds (0 violations) but is **strictly weaker than Cauchy–Schwarz on all
> 29 723 families** (Cauchy–Schwarz strictly tighter on 29 723; the top-bound strictly
> tighter on 0). (`second_moment_probe.py`, "P1" block.)

So the only second-moment lower bound union-closure cleanly produces is dominated by
the trivial one. **No `g(m,n)` stronger than `M_1²/n_active` survives** — and that
floor is parameter-free (true for *any* family, UC or not), so it is exactly the
"raw vector identity" the brief warned was already refuted, not a structural
second-moment inequality.

### 4.1 The multiplicity sub-direction has the wrong sign (task d)

`r(C) = #{(A,B):A∪B=C}` is the natural place union-closure lives in `U`. Structurally:

> **Finding 4.2.** `r(C) ≥ 1` for every `C∈F` (take `A=B=C`); and `r(T) > 1` for the
> top on **every** family (`r(T)=1` on **0/29 723**; e.g. for `{∅,{0}}`, `r({0})=3`
> from `(∅,{0}),({0},∅),({0},{0})`). More generally any chain below `C` contributes
> multiple pairs joining to `C`.

But this is **the wrong direction**: `U = Σ_C |C| r(C)` and we need `U` *small* to make
`M_2 = 2mM_1−U` *large*. A **lower** bound on `r(C)` (which union-closure gives)
**increases** the natural estimate of `U`, weakening the `M_2` bound. To help one would
need an **upper** bound on `Σ_C |C| r(C)` that beats `|T|m²` — and the high-`|C|`
terms (large sets) carry the most weight precisely where `r(C)` is large, so the
multiplicity structure works *against* a good `M_2` lower bound. **Dead end.**

---

## 5. Verdict and relation to the project's other six methods

> **Verdict.**
> * **The exact identity is clean and confirmed:** `Σ freq_i² = Σ_{A,B}|A∩B| =
>   2mM_1 − U` (Identity 1.1/1.2), 0 violations on all 29 723 families. Union-closure
>   ties `U` to the join multiplicities `r(C)` of members of `F`.
> * **No structural second-moment lower bound exists from union-closure.** The only
>   closure-aware bound (`M_2 ≥ 2mM_1 − |T|m²`) is dominated by the parameter-free
>   Cauchy–Schwarz floor on every family; the multiplicity route has the wrong sign.
> * **The cube minimizes the power-mean ratio at its parameters, pinning the lever at
>   exactly ½** (Lemma 2.1/2.2). The raw ratio dips to 0.444 but *only* at abundance
>   `> ½`; on the 39 abundance-½ families it is exactly ½. So the lever is both
>   harmless and useless, exactly like the LP cover certificate.
> * **This delimits a SEVENTH method**, with the identical Boolean-cube obstruction.

| method | object | invariant | dies because (on the cube `2^[k]`) |
|---|---|---|---|
| i.i.d. entropy | `H(A∪B)` | per-coord crossover | sharp at ψ; `Δ₂=0` at product |
| polynomial / slice rank | tensor `1[A∪B=C]` | slice-rank | `= |F|`, vacuous |
| lattice invariants | lattice `(F,∪)` | height/width/#JI/… | abundance not invariant (cone) |
| Boolean Fourier | `1_F` spectrum | `W^k, I, Stab_ρ` | trivial spectrum `δ_∅` |
| shadows / compression | shift `S_{ij}` | shadow/profile/FKG | cube is a shift fixed point |
| LP / fractional | averaging cover | `\overline s/n`, Reimer | `= ½` exactly, Reimer tight |
| **2nd moment (this)** | **`Σ freq_i²`** | **`R=M_2/(mM_1)`** | **`= ½`, cube minimizes `R` at `(m,M_1)`** |

> **The structural reason is the same every time.** The FUCC extremizer `2^[k]` is
> **perfectly flat** (`ab_i ≡ ½`), so every *symmetric/convex* functional of the
> frequency vector — mean (LP), variance/second moment (this), level-2 Fourier weight,
> slice rank — is saturated at its boundary value with no slack. The second moment is
> literally the variance partner of the first: `Var(freq) = M_2/n − (M_1/n)²`, and the
> flat extremizer is the *minimizer* of variance at fixed mean. Asking the second
> moment to certify `max > mean` fails on exactly the family where `max = mean = ½`.

### 5.1 Connection to the level-2 Fourier weight (brief's note)

The brief notes `Σ freq_i²` is "closely related to the level-2 Fourier weight / the
number of pairs `(A,B)` with `A∩B ≠ ∅`." Identity 1.1 makes this exact: `M_2 =
Σ_{A,B}|A∩B|` is the **size-weighted** count of intersecting ordered pairs (each pair
`(A,B)` contributes `|A∩B|`, which is `>0` iff `A∩B≠∅`). In Fourier language
(`boolean_fourier.md` §1.1, `L²`-normalized `1_F` with `p=m/2^n`), one has
`Σ_i Inf_i(1_F) = I[1_F] = Σ_S|S|f̂(S)²` and the level-1 identity
`f̂({i}) = p(1−2ab_i)`; the per-element second moment `Σ_i ab_i²` is a *quadratic in
the level-1 signed coefficients* `Σ_i (1−f̂({i})/p)²/4`. Since the cube has trivial
spectrum (`f̂=δ_∅`, so every `f̂({i})=0` and every `ab_i=½`), the second moment there is
forced to its flat value — **the same trivial-spectrum collapse** that kills the
quadratic Fourier method (`boolean_fourier.md` §3, Thm 4.3). The two obstructions are
the same fact viewed through (PM) vs. through Parseval.

---

## 6. Reproduction & certification status

* **Step 1 (computational): PASS.**
  - `python3 second_moment.py 5` → `data/secmom_n{0..5}.jsonl`, `secmom_summary.txt`,
    `secmom_run.txt` (29 723 families, |F|≥2, n≤5).
  - Identity `M_2 = 2mM_1 − U = Σ_{A,B}|A∩B|`: **0 violations** (exact integers).
  - Power-mean ratio: min `0.444`; **6** families `< ½`; on the **39** abundance-½
    families, `R ≡ ½` exactly (min=max=0.5).
  - `python3 second_moment_probe.py 5` → cube minimizes `R` per `(m,M_1)` class
    (`min R = ½` in all 5 cube classes); the union bound `M_2 ≥ 2mM_1−|T|m²` is
    tighter than Cauchy–Schwarz on **0/29 723**; `r(T)>1` on all families.
* **Steps 2–4 (red-team / Lean / human): N/A — no new theorem is claimed.** The
  deliverable is an obstruction (identity + exhaustive check) showing the lever caps at
  ½, plus a likely-known identity (`Σ freq² = Σ|A∩B|`, elementary double counting).
* **No PENDING RED-TEAM claim**, by design. `[NOVELTY UNVERIFIED]` on all framings.

**Bottom line.** The second-moment / variance lever — the single live sub-direction the
LP-duality attack left open — **does not beat ½**. The exact identity `Σ freq_i² =
Σ_{A,B}|A∩B| = 2mM_1 − U` is clean and union-closure ties `U` to the member join
multiplicities, but the only closure-aware second-moment bound is dominated by trivial
Cauchy–Schwarz, the multiplicity route has the wrong sign, and the Boolean cube
minimizes the power-mean ratio at its parameters — pinning the lever at exactly ½ with
the raw ratio decoupled from abundance on the tight families. It joins the other six as
a **seventh delimited method** with the same cube extremizer.
