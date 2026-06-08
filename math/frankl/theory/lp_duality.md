# LP duality / fractional relaxation attack on Frankl's union-closed conjecture

**Author:** Alex Ye (no AI on author line).
**Date:** 2026-06-03.
**Status:** `[NOVELTY UNVERIFIED — Poonen (1992) weight functions and LP relaxations
of Frankl very likely exist in the literature; arXiv 403 this session. Every
"new" framing flagged below.]` Deliverable is an **obstruction** (a fifth method
delimited), not a proof.
**Companion code:** `frankl/experiments/lp_duality.py`.
**Data:** `frankl/experiments/data/lp_sweep_n{0..5}.jsonl`, `lp_summary.{txt,json}`,
`lp_duality_run.txt`.
**Tests:** `tests/test_uc.py::TestLPDuality` (4 tests, pass); full suite 63 pass.
**Cross-ref:** `survey.md` §1.2 (Poonen), §2.2 (Reimer), §7.3/§7.4 (measure choice,
ignored intersection); `lattice_attack.md` §1.4 (fibre = filter), §3 (height bound);
`boolean_fourier.md` §3–4 and `polynomial_method.md` §4 (the **same** Boolean-cube
obstruction); `RED_TEAM_REPORT.md` and `shared/dead_ends.md` (the 0.43/0.45/0.5
budget-mismatch traps).

> **What this is.** A genuinely different lever from the project's four exhausted
> methods (i.i.d. entropy capped at ψ; slice-rank = |F| vacuous; abundance not a
> lattice invariant; Boolean-Fourier quadratics can't see abundance). We phrase
> Frankl as a linear program and ask whether **LP duality forces a certificate**.
> The honest outcome — anticipated by the brief and matching the other four
> methods — is a **clean obstruction with the Boolean cube as the universal
> extremizer**: the natural LP relaxation's certified bound **caps at exactly
> 1/2**, saturated by `2^[k]` with a **degenerate (zero-margin) dual certificate**,
> and **dips strictly below 1/2** on lopsided families. We pinpoint the exact
> linear inequality the LP misses.

---

## 0. The headline, up front

1. **Getting the LP right is the whole game.** The *naïve* "put a free probability
   weight `w` on members and minimise the max weighted abundance" LP is **vacuous**
   (value 0, attained by mass on ∅): it does **not** have Frankl as its value. This
   is the LP-shaped form of the documented budget-mismatch trap. We record it
   explicitly so it is never mistaken for a bound (§2).
2. **The right object is the dual *cover/averaging* certificate** (Reimer / Knill /
   Poonen weight-function lineage), evaluated at the **uniform** measure (the measure
   Frankl is actually about). Reconstructed in LP-dual language in §3.
3. **The averaging cover LP caps at exactly 1/2 and is degenerate on the cube.**
   For `2^[k]`: `avg_set_size = k/2`, ground size `k`, so the certified abundance
   bound `avg_set_size / k = 1/2` **exactly**, with Reimer's inequality
   `avg ≥ ½ log₂|F|` **tight** (`|F| = 2^k`). Zero margin — the certificate
   degenerates precisely on the FUCC extremizer (§4). Same cube, same death, as the
   polynomial and Fourier methods.
4. **The LP relaxation has a real, non-artifact gap below 1/2.** On exactly **6 of
   29 723** UC families (n≤5) the averaging certificate certifies `< 1/2` (min
   **0.40**), while the true abundance is high (0.78–0.89). These 6 are the LP's
   integrality/relaxation gap, and they share one structure (§5).
5. **The missing inequality is "max vs mean."** Averaging certifies the *mean*
   abundance `(1/n)Σᵢ abᵢ`; Frankl needs the *max*. The gap is exactly the
   **spread** of the frequency vector, which the linear averaging functional cannot
   see. The single most promising valid inequality to add is a **convexity / second-
   moment ("variance") inequality** on the fibre-filter sizes (§6).

All numbers validated on **all 29 723 UC families with |F|≥2, n≤5** (Frankl holds:
min true abundance exactly 0.5; 0 below half).

---

## 1. Set-up: Frankl as an optimization over a combinatorial domain

Fix a union-closed `F ⊆ 2^[n]` with members `A₁,…,A_m` (`m = |F|`). Let
`freqᵢ = |{A ∈ F : i ∈ A}|` and `abᵢ = freqᵢ / m`. Frankl:

$$ \mathrm{abundance}(F) \;=\; \max_{i\in[n]} ab_i \;\ge\; \tfrac12 . \tag{F}$$

Two linear objects sit behind (F).

* **Incidence matrix** `M ∈ {0,1}^{n×m}`, `M_{i,k} = 1[i ∈ A_k]`.
  Then `(M·\mathbf 1/m)_i = ab_i`, where `\mathbf 1` is the all-ones weight.
* **Averaging identity** (a one-line, exact linear fact, used throughout):
  $$ \sum_{i\in[n]} ab_i \;=\; \frac1m\sum_{A\in F} |A| \;=:\; \overline{s}(F)\quad
     (\text{average set size}). \tag{1.1}$$
  Proof: `Σ_A |A| = Σ_A Σ_i 1[i∈A] = Σ_i freq_i = m·Σ_i ab_i`. (Verified exact on
  all n≤4 families, `TestLPDuality::test_reimer_holds_and_avg_equals_sum_abundance`.)

The combinatorial domain is "all UC families"; the LP question is whether a *fixed
recipe of linear multipliers* on the structure of `F` forces `max_i ab_i ≥ ½`.

---

## 2. The trap: the naïve weighting LP is vacuous `[NOVELTY UNVERIFIED]`

The brief's literal reading ("put a probability weight `w(A) ≥ 0`, `Σw=1`, ask
whether `Σ_{A∋i} w(A) ≥ ½` is forced"). Make the adversary pick `w` to *minimise*
the best element:

> **(P-weight)**
> $$ \mathrm{val}_{\mathrm{pw}}(F)\;=\;\min_{w\in\Delta(F)}\ \max_{i\in[n]}\
>    \sum_{A\ni i} w(A)
>  \;=\; \min_w\{\,t : (Mw)_i\le t\ \forall i,\ \mathbf 1^\top w=1,\ w\ge0\,\}. $$
> A linear program (epigraph variable `t`). `code: lp_min_max_abundance`.

**This is the wrong LP, and it is vacuous.** Putting all weight on the bottom
element ∅ (or, in general, on a member that omits the would-be heavy elements)
drives every `Σ_{A∋i} w(A)` to 0. Exhaustively:

> **Finding 2.1 (Step-1).** Over all 29 723 UC families n≤5,
> `min_F val_{pw}(F) = 0` (attained by any `F ∋ ∅`), and **20 240** families have
> `val_{pw} < ½`. The gap `true_abundance − val_{pw}` reaches **0.941** (at
> `cone(2^[4])`). (`lp_summary.txt`; `TestLPDuality::test_pweight_lp_is_vacuous`.)

The fix is not to add constraints to `w`: **union-closure imposes no linear
inequality on the abundance vector of a *free* measure.** Each fibre
`Fib(i)={A:i∈A}` is a filter of the lattice (`lattice_attack.md` §1.4), but
`Σ_{A∈Fib(i)} w(A)` is unconstrained by `w` being a probability vector — a free `w`
can starve any chosen filter. (`lp_min_max_abundance_with_uc_constraints` returns
the same value, documenting this.) So **the measure must be fixed to uniform** —
which is exactly what Frankl is about. This is the LP-shaped twin of the
`0.43`/`0.45`/`0.5` budget-mismatch traps in `dead_ends.md`: charging the wrong
object (a free measure) gives a meaningless number.

> **Lesson 2.2.** The only LP whose optimum *equals* the true abundance is the
> trivial "uniform measure, pick the best element" LP
> `max_{z∈Δ([n])} Σ_i z_i ab_i = max_i ab_i` (`primal_abundance_lp`); its dual is
> `min{τ : τ ≥ ab_i ∀i}`, the single tight element. **Abundance is already an
> LP-free max; the relaxation lives entirely in *which valid inequalities you are
> allowed to use to lower-bound it*** — i.e. in the dual cover (§3).

---

## 3. The right object: the averaging / cover dual certificate (Reimer in LP-dual language)

Fix the **uniform** measure. A *dual certificate for Frankl on `F`* is a recipe
that lower-bounds `max_i ab_i` using only nonnegative combinations of **valid
inequalities** about `F`. The classical one is **averaging**:

> **(D-avg) Averaging cover.** By (1.1), `max_i ab_i ≥ (1/n) Σ_i ab_i = \overline
> s(F)/n`. This is a dual certificate: the multiplier vector is uniform `λ_i = 1/n`
> on the per-element identities, and the certified lower bound is `\overline s(F)/n`.

This is exactly **Reimer's average-set-size theorem** (`survey.md` §2.2) in dual
form. Reimer proves the *valid inequality*
$$ \overline s(F)\;\ge\;\tfrac12\log_2|F| \tag{R}$$
(equality on power sets), so the averaging certificate also reads
`max_i ab_i ≥ (log₂ m)/(2n)`. **(R) is itself a weighting/compression certificate**
(Reimer's proof is an averaging over an injection); restating it as a multiplier
recipe is the "Reimer = dual certificate" identification the brief asks for.

> **Strengthening with order-ideal inequalities.** Union-closure gives one more
> *valid linear inequality* usable in the certificate (`lattice_attack.md` Prop 3.1):
> along a longest chain `∅=C_0⋖C_1⋖⋯⋖C_h`, any element `x∈C_1` lies in all of
> `C_1,…,C_h`, so `freq_x ≥ h = height(L)`, i.e. `max_i ab_i ≥ height/m`. This is the
> "height witness" multiplier (a single tight element).

We package both into the **cover certificate**
$$ \boxed{\ \mathrm{cert}(F)\;=\;\max\Big(\ \underbrace{\overline s(F)/n}_{\text{averaging}},\ \underbrace{\mathrm{height}(L)/m}_{\text{order ideal}}\ \Big)\ \le\ \max_i ab_i.\ } \tag{3.1}$$
`code: lp_cover_certificate`. If `cert(F) ≥ ½`, the LP-dual **proves Frankl for `F`**.

> **Finding 3.1 (Step-1).** Reimer (R) holds with **0 violations** on all 29 723
> families n≤5. The cover certificate (3.1) proves Frankl
> (`cert ≥ ½`) for **29 717 of 29 723** families. (`lp_summary.txt`.)

---

## 4. The obstruction: the cover LP caps at exactly 1/2, **degenerate on the cube**

> **Theorem 4.1 (cube saturation — the extremizer).** For the Boolean cube
> `F = 2^[k]` (k ≥ 1):
> `\overline s = k/2`, ground size `n = k`, `|F| = 2^k`, so
> $$ \mathrm{cert}(2^{[k]}) \;=\; \frac{\overline s}{n} \;=\; \frac{k/2}{k} \;=\; \tfrac12
>    \quad\text{exactly, for every }k, $$
> and Reimer's inequality (R) is **tight**: `\overline s = k/2 = \tfrac12\log_2 2^k =
> \tfrac12\log_2|F|`. The certified bound equals the true abundance (`= ½`) with
> **zero margin**, and the certifying multipliers are uniform — i.e. **degenerate**.
> (Verified k=1..5, `TestLPDuality::test_cube_saturates_averaging_at_half_reimer_tight`.)

The cube is therefore the **universal extremizer** of the LP method, exactly as in:
`polynomial_method.md` (slice-rank `= |F|`, no info on the cube) and
`boolean_fourier.md` §3 (trivial spectrum on the cube). The reason is structural and
identical across all three: **the FUCC extremizer `2^[k]` is perfectly "flat" —
every element has abundance exactly ½ — so every *symmetric / first-order* functional
(slice rank, quadratic spectrum, average abundance) is saturated at its boundary
with no slack to certify a strict inequality.** Any cover bound `cert ≤ max_i ab_i`
that is built from averaging (R) must satisfy `cert(2^[k]) = ½` with equality, so it
can **never certify `max_i ab_i ≥ ½ + ε`** and cannot push past ½.

> **Corollary 4.2 (no shortcut from averaging).** The averaging cover certificate
> (3.1) — and any nonnegative combination of (R) with the order-ideal inequality —
> certifies abundance `≥ ½` **at best**, with the cube forcing exactly ½. Reimer is
> *sharp on cubes by design*; the LP dual inherits that sharpness as an obstruction.

---

## 5. The integrality gap: 6 lopsided families where the LP dips below 1/2

The cover certificate is not merely tight at ½ — it **fails** (certifies `< ½`) on a
small, structured set of families, which are exactly the LP's relaxation gap.

> **Finding 5.1 (Step-1).** Over all 29 723 UC families n≤5, the cover certificate
> (3.1) certifies `< ½` on **exactly 6 families** (min `cert = 0.40`), while their
> true abundance is **0.78–0.89**. (`lp_summary.txt`, `cover_fail_examples`.)

| sorted freq vector | `m` | n | `cert(F)` | true abundance |
|---|---|---|---|---|
| `[4,4,5,8]` | 9 | 5 | 0.467 | 0.889 |
| `[4,5,6,8]` | 10 | 5 | 0.460 | 0.800 |
| `[4,4,6,7]` | 9 | 5 | 0.467 | 0.778 |
| `[2,3,3,4]` | 5 | 5 | 0.480 | 0.800 |
| `[2,3,4]` (+1 dead slot) | 5 | 5 | **0.400** | 0.800 |
| `[2,3,4]` (+1 dead slot) | 5 | 4 | 0.450 | 0.800 |

> **This `0.40`/`0.45` is a REAL LP value, not a budget-mismatch artifact.** Cross-
> ref `dead_ends.md`: the documented `0.4295`/`0.45`/`0.5` traps all arise from
> charging a *doubled or wrong* budget (`H(A∪B,A∩B)` against a single `H(A)`; a free
> measure). Here the number is the **honest** value of the averaging identity (1.1):
> e.g. `[2,3,4]` with one dead element has `Σ ab_i = 9/5 = 1.8` spread over `n=4`
> ground slots, so `mean = 1.8/4 = 0.45 < ½`; over `n=5` it is `0.40`. The averaging
> certificate **genuinely loses** here. (`test_averaging_certificate_has_a_real_gap_below_half`.)

**Common structure of all 6.** Each has **one near-universal element** (`freq` close
to `m`, the FUCC-heavy element, abundance 0.78–0.89) **plus one or two low-frequency
"parasitic" elements** (`freq` small) that drag the *mean* below ½ even though the
*max* is high. The mean is fooled by low-abundance elements; the LP, working with the
linear average, cannot tell them apart from the heavy one. **This is the integrality
gap: averaging controls the mean, Frankl needs the max.**

---

## 6. The missing inequality, and the most promising one to add

The gap of §5 is *exactly* the spread between mean and max of the abundance vector.

> **Diagnosis 6.1.** The averaging dual certifies `max_i ab_i ≥ mean_i ab_i`, off by
> `max − mean = ` (spread). To recover `max ≥ ½` from `mean` we need either
> (i) a lower bound on the *mean restricted to heavy elements*, or
> (ii) an *upper* bound on the spread / a convexity (second-moment) inequality that
> says the abundance vector cannot be both flat-enough-to-have-low-max and
> consistent with union-closure.

The single most promising **additional valid inequality** to add to the LP:

> **Candidate 6.2 (second-moment / Reimer-on-pairs) `[NOVELTY UNVERIFIED]`.**
> Reimer bounds the *first* moment `Σ_i ab_i = \overline s ≥ ½ log₂ m`. The natural
> next step is a **second-moment valid inequality** `Σ_i ab_i² ≥ g(m,n)` from
> union-closure (a "Reimer for pairs": `Σ_i freq_i²` counts ordered pairs `(A,B)`
> sharing an element, `= Σ_{A,B} |A∩B|`, which union-closure ties to `A∪B∈F`). The
> hope is the **power-mean ("weighted-by-itself") bound**
> `max_i ab_i ≥ (Σ ab_i²)/(Σ ab_i) ≥ mean`, strictly larger when the vector is spread.
>
> **Honesty check (Step-1, decisive).** The power-mean bound computed *from the raw
> abundance vector alone* keeps the cube at exactly ½ (good) **but still dips below ½
> on 6 families** (min **0.444**, e.g. `{∅,{4},{0,1,2,3,4}}` with `ab = [⅓,⅓,⅓,⅓,1]`,
> power-mean `= (4/9+1)/(4/3+1) ≈ 0.571`… and worse cases to 0.444). So the
> power-mean inequality **by itself is NOT strong enough** — it does not clear the
> gap. (`lp_duality.py`, second-moment probe.) The bound only helps **if and only if
> union-closure supplies a genuine lower bound `g(m,n)` on `Σ_i freq_i²` that the raw
> vector does not already give.** Whether such a `g` exists is **open and not
> established here**; the naive power-mean is refuted as a standalone certificate.

> **Honest caveat.** Even if Candidate 6.2 worked on n≤5, the cube keeps it pinned at
> exactly ½ (Theorem 4.1), so — like every method in this project — it could at most
> *reach* ½, never exceed it. A second-moment inequality is the right *next valid
> inequality*; it is **not** a route to a constant `> ½`.

---

## 7. Verdict and relation to the project's other four methods

> **Verdict.**
> * **No uniform dual certificate that proves Frankl was found** (and none is
>   claimed). The naïve weighting LP is **vacuous** (§2); the correct averaging/
>   cover dual (§3) **caps at exactly ½**, is **degenerate on the cube** (§4), and
>   has a **real integrality gap below ½ on 6 lopsided families** (§5).
> * **The obstruction is the same Boolean cube** that kills the polynomial and
>   Boolean-Fourier methods: `2^[k]` is perfectly flat (every `ab_i = ½`), so every
>   first-order/symmetric LP functional saturates at ½ with a degenerate certificate.
> * **This delimits a FIFTH method.** Pattern across all five:

| method | object | invariant | dies because (on the cube `2^[k]`) |
|---|---|---|---|
| i.i.d. entropy | `H(A∪B)` | per-coord crossover | sharp at ψ; `Δ₂=0` at product |
| polynomial / slice rank | tensor `1[A∪B=C]` | slice-rank | `= |F|`, vacuous |
| lattice invariants | lattice `(F,∪)` | height/width/#JI/… | abundance not invariant (cone) |
| Boolean Fourier | `1_F` spectrum | `W^k, I, Stab_ρ` | trivial spectrum `δ_{∅}` |
| **LP / fractional (this)** | **averaging cover** | **`\overline s/n`, Reimer** | **= ½ exactly, Reimer tight, zero margin** |

> **The one live sub-direction:** a **second-moment ("variance") valid inequality**
> `Σ_i freq_i² ≥ g(m,n)` from union-closure, feeding the power-mean bound
> `max ≥ (Σ ab_i²)/(Σ ab_i)` (§6). It would close the §5 gap while leaving the cube
> at ½. Establishing or refuting `g(m,n)` needs the literature (Reimer-pairs /
> Kleitman-style correlation; arXiv blocked) and is logged as the open follow-up.
> `[NOVELTY UNVERIFIED]`.

---

## 8. Reproduction & certification status

* **Step 1 (computational): PASS.**
  - `python3 lp_duality.py 5` → `data/lp_sweep_n{0..5}.jsonl`, `lp_summary.{txt,json}`
    (29 723 families, |F|≥2, n≤5).
  - True abundance min = 0.5, 0 below half (Frankl re-verified n≤5).
  - (P-weight) LP vacuous: min 0, 20 240 below half (§2).
  - Reimer (R): 0 violations; averaging identity (1.1) exact (§3).
  - Cover certificate: proves Frankl 29 717/29 723; 6 real gaps, min 0.40 (§4–5).
  - `pytest tests/test_uc.py::TestLPDuality` → 4 pass; full suite 63 pass.
* **Steps 2–4 (red-team / Lean / human): N/A — no new theorem is claimed.** The
  deliverable is an obstruction (construction + exhaustive check) plus a likely-known
  certificate (Reimer in dual form). The second-moment candidate (§6) is **open**,
  flagged, and **not** asserted.
* **No PENDING RED-TEAM claim**, by design. `[NOVELTY UNVERIFIED]` on all framings;
  Poonen weight-functions and LP relaxations of Frankl are very likely prior art.

**Bottom line.** LP duality does **not** beat the project's reach. The naïve
weighting LP is the budget-mismatch trap in LP clothing; the correct averaging/cover
dual is **Reimer**, which is **sharp on the Boolean cube at exactly ½** and has a real
sub-½ integrality gap on lopsided families. The method joins the other four as a
delimited fifth, with the **second-moment valid inequality** as its single open lever.
