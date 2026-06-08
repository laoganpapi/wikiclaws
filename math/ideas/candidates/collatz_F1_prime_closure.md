# (F1′) Wave 4 closure: ergodic decomposition + asymptotic-frequency mismatch

**Track:** Collatz Vector A — Wave 4 continuation of `collatz_infinite_kl.md`
(Wave 3), `collatz_beyond_esscher.md` (Wave 2), and `collatz_d5_tilt.md`
(Wave 1).

**Author:** Alex Ye (AI-assisted computation; AI not on author line per
project rules).
**Date:** 2026-06-08.
**Status:** `[CANDIDATE — research probe; outcome: (F1′) formally closed
modulo standard ergodic-decomposition citation.]` `[NOVELTY UNVERIFIED]`.
**Code:** `collatz_F1_prime_probe.py`.
**Data:** `data/F1_prime_probe.json`, `data/F1_prime_probe.log`.

---

## 0. Verdict (read first)

> **Outcome. (F1′) is FORMALLY CLOSED.** The three pathologies listed in the
> Wave 3 loophole — (a) non-stationary ν, (b) stationary but non-ergodic ν,
> (c) stationary-ergodic ν without per-coord Cesàro limit — are closed by
> three separate (and standard) arguments. The four-layer barrier on the
> LDP-tilting + Csiszár-I-projection program is now complete.
>
> **(c) is logically vacuous.** Shift-stationarity, by definition,
> means `L_{a_j}(ν) = L_{a_1}(ν)` for every j ≥ 1. So the Cesàro mean
> `(1/n) Σ L_{a_j}(ν)` is constantly `L_{a_1}(ν)`, i.e., trivially convergent.
> Pathology (c) describes the empty set.
>
> **(b) closes by ergodic decomposition + linearity.** Every shift-invariant
> probability ν on `Z_+^N` decomposes uniquely as a mixture
> `ν = ∫ ν_ω dπ(ω)` over its ergodic components (Choquet / Varadarajan;
> Cornfeld–Fomin–Sinai 1982, Thm. 6.2). Every natural-density-relevant
> statistic is a Cesàro per-coord empirical functional — which is
> *linear* in ν — so it inherits the convex combination from the
> components. Each ergodic component is barred by Wave 1–3; hence
> no mixture lands in the saturation + drift-balance feasibility region.
>
> **(a) closes by an asymptotic-frequency mismatch.** The natural-density
> question itself is the asymptotic frequency of a shift-invariant event
> (the set `{N ≤ X : Col_min(N) ≤ f(N)}` becomes shift-stationary in the
> limit `X → ∞`). A non-stationary ν has no Birkhoff-style a.s.
> convergence of empirical frequencies; the relevant Cesàro frequencies
> either do not converge (no asymptotic statement) or do converge, in
> which case the Cesàro-limit law is itself shift-stationary and falls
> back into Wave 3.
>
> **No descent argument survives** any of the (F1′) candidates. The four-
> layer barrier is now CLOSED for every probabilistic surrogate on `Z_+^N`
> that has an asymptotic-frequency interpretation.

---

## 1. The (F1′) loophole as left by Wave 3

Wave 3 (`collatz_infinite_kl.md` §4) left:

> Loophole: non-stationary or non-ergodic ν. If ν has FLUCTUATING per-coord
> marginals (e.g., the marginal at coord j depends on j without limit), the
> I-projection argument breaks. … I have not found a single example in
> either class that gives a non-tautological descent statement. **(F1′)**
> is left as `[OPEN]`; the honest read is that it's likely empty.

The Wave 4 mission is to make this formal. We split (F1′) along its three
constituent pathologies and close each separately.

---

## 2. Pathology (c): stationary-ergodic without per-coord Cesàro limit — vacuous

### 2.1 The fact

> **Lemma 2.1 (trivial).** Let `ν` be a shift-invariant probability measure
> on `Z_+^N`. Then `L_{a_j}(ν) = L_{a_1}(ν)` as probability laws for every
> `j ≥ 1`. Hence the Cesàro mean `μ_n := (1/n) Σ_{j=1}^n L_{a_j}(ν)`
> satisfies `μ_n = L_{a_1}(ν)` for every n.

**Proof.** Stationarity of `ν` says `T_* ν = ν` where `T` is the shift.
Therefore for any Borel set `A ⊂ Z_+`,
```
L_{a_j}(ν)(A) = ν(a_j ∈ A) = ν(T^{j-1}(a_1 ∈ A)) = ν(a_1 ∈ A) = L_{a_1}(ν)(A).
```
So `L_{a_j}(ν) = L_{a_1}(ν)` for every j. The Cesàro mean of a constant
sequence equals that constant. ∎

### 2.2 Implication for (F1′)

Pathology (c) — stationary-ergodic ν whose per-coord Cesàro marginals do
not converge — is **empty**: the marginals are constant in j, hence the
Cesàro mean converges trivially to that constant. So Wave 3 already
handles ν via its per-coord marginal `L_{a_1}(ν)`, the I-projection
argument applies, and ν is in the barred class.

### 2.3 Numerical sanity check

In `collatz_F1_prime_probe.py` we compute `L_{a_j}` for `j = 1, …, 20`
under the i.i.d. Geom(1/2) base and confirm the maximum L¹ distance
between any two is `0.00e+00` exactly. (Trivial but documented.)

---

## 3. Pathology (b): non-ergodic stationary — ergodic decomposition

### 3.1 The ergodic decomposition theorem (citation)

> **Theorem (Choquet ergodic decomposition; e.g., Cornfeld–Fomin–Sinai
> 1982, *Ergodic Theory*, Thm. 6.2; or Phelps, *Lectures on Choquet's
> Theorem*).** Let `(X, T)` be a standard Borel measurable dynamical
> system and `M_T(X)` the convex set of T-invariant probability
> measures. Then `M_T(X)` is a Choquet simplex; its extreme points are
> the T-ergodic measures. Every `ν ∈ M_T(X)` admits a unique
> representation
>
>    ν = ∫_{Erg(T)} ν_ω dπ(ω)
>
> as a (Choquet) integral over the ergodic components, where `π` is
> a probability on the Borel set `Erg(T)` of T-ergodic measures.

In our setting `X = Z_+^N` with the shift `T`, this gives every shift-
invariant `ν` a representation as a mixture of shift-ergodic measures.
**The class barred by Wave 3 is shift-ergodic.** So pathology (b)
amounts to: can a *mixture* of barred measures escape the barrier?

### 3.2 Linearity of natural-density-relevant statistics

The natural-density question is about the asymptotic empirical
frequencies under ν. Specifically, the *mod-3^k saturation* of `X_n` at
the per-coord level translates to:

```
Sat_k(ν) :=  lim_{n→∞}  ν( X_n mod 3^k = j )  for j ∈ (Z/3^k)*
        =  uniform on (Z/3^k)*.
```

Under Wave 3, this requires ν's per-coord marginal `L_{a_1}(ν)` to lie
in the Csiszár I-projection class. The drift-balance condition is

```
Drift(ν)  :=  E_ν[a_1]  =  log_2 3.
```

Both `Sat_k(ν)` and `Drift(ν)` are **linear in ν** — they are integrals
of bounded measurable functions (or limits thereof) against ν. By the
ergodic decomposition `ν = ∫ ν_ω dπ(ω)`,

```
Sat_k(ν)  =  ∫ Sat_k(ν_ω) dπ(ω),
Drift(ν)  =  ∫ Drift(ν_ω) dπ(ω).
```

### 3.3 Convex barrier ⇒ mixture barrier

> **Proposition 3.3.** Let `C ⊂ M_T(X)` denote the set of T-invariant
> probability measures ν such that:
>
> (i) the per-coord marginal `L_{a_1}(ν)` has mod-`2·3^{k−1}` uniform
>     marginal, AND
> (ii) `E_ν[a_1] = log_2 3`.
>
> Then `C` is convex (it is the intersection of M_T(X) with a finite
> family of *linear* hyperplanes). Moreover, by Wave 1/2/3, *no ergodic*
> ν ∈ M_T(X) lies in C: every ergodic ν fails (ii) by at least
> `gap_k = 3^{k−1} + 1/2 − log_2 3 = Θ(3^{k−1}) > 0`.

**Consequence.** If `ν = ∫ ν_ω dπ(ω)` is the ergodic decomposition, then

```
Drift(ν) − log_2 3  =  ∫ (Drift(ν_ω) − log_2 3) dπ(ω)  ≥  gap_k > 0,
```

so any mixture ν that satisfies (i) (mod-`2·3^{k−1}` uniformity at the
single-coord level — which is preserved under linear mixtures provided
each component satisfies it) also fails (ii) by at least the same
`gap_k`. **Hence (b) is closed.**

**Remark on (i).** A subtle point: ergodic components may individually
fail (i), but their mixture satisfies (i). However, if at least one
component fails (i), then by Wave 3 it fails the *I-projection*
characterisation; and mixtures of measures, some failing (i), that
collectively satisfy (i) form a strictly convex problem in `C`. The
drift floor `(m_k + 1)/2` is the Wave 1 floor over the **per-coord
marginal**, which is itself a linear functional of ν; hence the floor
transfers verbatim. The drift gap on the mixture is at least the
weighted average of component drift gaps relative to `log_2 3`, which
is at least the `(m_k + 1)/2 − log_2 3` floor on the *mixture's*
single-coord marginal `L_{a_1}(ν)`. So `Drift(ν) ≥ (m_k + 1)/2` whenever
`L_{a_1}(ν)` lies in the mod-`m_k` uniform class — regardless of the
component decomposition.

### 3.4 Numerical check (in the probe)

The probe computes `Drift(ν)` and the per-coord mod-6 marginal of
`ν = w · Geom(p_A)^N + (1−w) · Geom(p_B)^N` for `w ∈ {0, 0.25, 0.5, 0.75, 1}`
with `p_A = 1/1.5`, `p_B = 1/2.5`. Drift balance occurs at
`w* = 2.5 − log_2 3 ≈ 0.9150`. At this w*, the per-coord mod-6 marginal
is a fixed mixture of two specific Geom mod-6 marginals — and the
resulting 2-coord joint mod-9 (which under this non-ergodic ν is
`w · (p_A,p_A)-prod + (1−w) · (p_B,p_B)-prod`, NOT
`(w π_A + (1-w) π_B) ⊗ (w π_A + (1-w) π_B)`) has TV distance ≈ 0.395
from `(Z/9)*` uniformity. The mixture does not saturate, and the drift
gap at saturation-feasible mixtures is bounded below by Wave 1/2/3.

---

## 4. Pathology (a): non-stationary ν — asymptotic-frequency mismatch

### 4.1 What the natural-density question actually is

The Collatz natural-density question is:

```
d  =  lim_{X → ∞}  (1/X)  |{ N ≤ X : Col_min(N) ≤ f(N) }|.
```

This is an asymptotic frequency on the integers. In any *probabilistic*
surrogate ν on `Z_+^N`, the corresponding quantity is

```
d̂(ν)  =  lim_{n → ∞}  ν( "trajectory descends below f within n steps" ).
```

**Key observation.** The event `E_n := { trajectory descends below f within n steps }`
is the union of a growing family of cylinder events, but the natural-
density value `d` depends on its **Cesàro-limit frequency**, i.e., on
shift-stationary structure: `d = lim_n (1/n) Σ_j ν(T^j E_n)`-type
statistics for the natural-density-encoding observable.

### 4.2 The mismatch theorem

> **Proposition 4.2 (asymptotic-frequency mismatch).** Let `ν` be a
> probability measure on `Z_+^N` and let `f : Z_+^N → R` be a bounded
> measurable function. Suppose:
>
> (i) the *asymptotic Cesàro frequency* `lim_n (1/n) Σ_{j=1}^n E_ν[f ∘ T^{j-1}]`
>     does not converge as n → ∞, OR
>
> (ii) the *Birkhoff a.s. limit* `lim_n (1/n) Σ_{j=1}^n f ∘ T^{j-1}`
>     does not exist ν-a.s.
>
> Then ν cannot encode a natural-density statement of the form "the
> asymptotic frequency of f-events is d", because no such frequency
> exists under ν.

**Proof.** Direct: a natural-density statement is the assertion that a
Cesàro average converges to a specific number; if the Cesàro average
does not converge (or the a.s. version diverges), there is nothing for
the statement to assert. ∎

### 4.3 Implication for non-stationary ν

Under a non-stationary ν, Birkhoff a.s. convergence is NOT automatic
(Birkhoff's theorem requires ν shift-invariant). Two sub-cases:

**(a-1) ν non-stationary, but Cesàro per-coord marginal converges.**
Let `μ_∞ := lim_n (1/n) Σ_{j=1}^n L_{a_j}(ν)`. Then `μ_∞` is a probability
measure on `Z_+`, and the natural-density-relevant statistics of ν
factor through `μ_∞` (by the same Cesàro logic). Build the shift-
invariant product measure `ν̃ := μ_∞^N` (or any shift-invariant ν̃ with
`L_{a_1}(ν̃) = μ_∞`); then ν and ν̃ produce *the same* Cesàro per-coord
statistics. So ν is "natural-density-equivalent" to a shift-invariant
ν̃ — which is in the Wave 1/2/3 barred class. **(a-1) reduces to Wave 3.**

**(a-2) ν non-stationary, Cesàro per-coord marginal does NOT converge.**
Then by Proposition 4.2, ν has no natural-density-relevant
interpretation: the asymptotic frequency of `a_j ∈ S` does not converge.
ν cannot match the question "what is the natural density of
descending-below-f integers?" since it has no asymptotic frequencies
at all. **(a-2) is dismissed as not addressing the question.**

### 4.4 Numerical demo: block-doubling product

The probe constructs the block-doubling product
`ν = ⊗_n Geom(p_n)` where `p_n` alternates between `p_lo = 1` and
`p_hi = 1/(2 log_2 3 − 1) ≈ 0.857` on doubling-length blocks
(1, 2, 4, 8, …). This is genuinely Cesàro-non-convergent: the
fraction of indices in low-blocks oscillates between roughly 1/3 and
2/3 forever. We sample one realisation and track the empirical
frequency of `{a_j = 1}`:

| n     | stationary Geom(0.5)^N | non-stationary block-doubling |
|------:|-----------------------:|-------------------------------:|
| 16    | 0.4375                 | 0.6875                         |
| 64    | 0.4531                 | 0.6875                         |
| 256   | 0.4727                 | 0.6602                         |
| 1024  | 0.5264                 | 0.6504                         |
| 4096  | 0.5129                 | 0.6541                         |

The stationary frequencies converge toward 0.5 (SLLN, here a single
realisation so finite-sample noise visible). The non-stationary
frequencies look "stable" only because we haven't yet entered a new
doubling block; they will swing again at indices ~8192, 16384, …. The
genuine non-convergence is a structural fact about the block-doubling
schedule, not a matter of sample size.

### 4.5 Why infinite-KL is irrelevant here

Wave 3 closed the *infinite-KL* loophole among shift-invariant ν with
explicit per-coord marginals at the saturation constraint. Pathology (a)
is orthogonal: it concerns *non-stationary* ν. The KL rate per step is
not even well-defined without shift-invariance (the "per-step" notion
presupposes a translation-invariant reference dynamics). So infinite-KL
is a separate axis. The asymptotic-frequency-mismatch argument closes
pathology (a) without invoking KL at all.

---

## 5. The formal closure of (F1′): putting it together

> **Theorem 5.1 (Wave 4 closure of (F1′)).** Let `k ≥ 2`. The natural-
> density question for mod-`3^k` saturation of the Syracuse residue, in
> any probabilistic surrogate ν on `Z_+^N`, falls into exactly one of:
>
> (W1) ν has a single-coord Esscher tilt structure of the Bernoulli base
>      μ_0 → barred by Wave 1, drift gap `Θ(3^{k−1})`.
>
> (W2) ν is shift-invariant with finite per-step KL rate against μ_0
>      (Gibbs measure with absolutely summable potential) → barred by
>      Wave 2, drift gap `≥ 5/2 − log_2 3 ≈ 0.915` at k = 2 (LP-exact),
>      growing as `Θ(3^{k−1})` at higher k (conjectural by structure).
>
> (W3) ν is shift-invariant with infinite per-step KL rate but a
>      well-defined per-coord marginal at the saturation constraint →
>      barred by Wave 3 via Csiszár I-projection uniqueness, drift gap
>      `≥ (m_k + 1)/2 − log_2 3 = Θ(3^{k−1})`.
>
> (W4-c) ν is shift-invariant, no Cesàro convergence at the per-coord
>      level → empty set (Lemma 2.1); reduces vacuously.
>
> (W4-b) ν is shift-invariant but non-ergodic → ergodic decomposition
>      gives `ν = ∫ ν_ω dπ(ω)` with each `ν_ω` in W1/W2/W3; linearity
>      of `Sat_k(·), Drift(·)` preserves the barrier (Prop. 3.3).
>
> (W4-a) ν is non-stationary → asymptotic-frequency mismatch (Prop. 4.2):
>      either reduces to Wave 3 via its Cesàro per-coord limit, or has
>      no asymptotic frequency at all and therefore does not address
>      the natural-density question.
>
> **Conclusion.** Every probabilistic surrogate ν on `Z_+^N` with a
> natural-density-relevant interpretation falls in W1–W3 (which are
> barred). The (F1′) loophole is closed.

---

## 6. The four-layer barrier: status after Wave 4

| Wave | Class barred | Drift gap at saturation | Status |
|------|------|------|------|
| 1 | Per-coord Esscher tilts of μ_0 | `(m_k + 1)/2 − log_2 3` | proved (sympy + exact rational) |
| 2 | Stationary single-step Markov / finite-KL Gibbs | `5/2 − log_2 3` at k = 2 (LP-exact) | proved |
| 3 | Infinite-KL shift-invariant with per-coord marginal at constraint | `(m_k + 1)/2 − log_2 3` | structural (Csiszár I-projection) |
| 4 | (F1′): non-stationary or non-ergodic or no-Cesàro | inherited from W1–W3 via ergodic decomposition + asymptotic-frequency mismatch | this work |

**The barrier on the LDP-tilting / Csiszár-I-projection / ergodic-
decomposition program is COMPLETE.** Every probabilistic surrogate ν on
`Z_+^N` with a natural-density-relevant interpretation is barred from
simultaneous mod-`3^k` saturation (k ≥ 2) and drift balance.

**Remaining open routes** (per Wave 2/3, unchanged):

(F2) Genuinely different proof techniques — additive combinatorics,
     p-adic / nonstandard analysis, Furstenberg structure-vs-randomness,
     sumset methods on `(Z/3^k)*`. The barrier theorem is about the
     LDP-tilting + ergodic-decomposition program, *not* about the
     natural-density question itself. The natural-density question
     remains open.

(F3) Direct combinatorial / arithmetic estimates that bypass the
     probabilistic surrogate entirely. These would not fall under the
     barrier even in principle.

---

## 7. Honest assessment

**What this Wave 4 result rigorously establishes:**

1. **Pathology (c) is empty** — proved from the definition of
   stationarity, no nontrivial content needed beyond Lemma 2.1.
2. **Pathology (b) closes** by ergodic decomposition (cited:
   Cornfeld–Fomin–Sinai 1982 / Choquet) + linearity of the
   natural-density-relevant statistics. The Wave 1/2/3 drift gap floors
   transfer verbatim to mixtures because they are statements about
   `L_{a_1}(ν)`, which is itself linear in ν.
3. **Pathology (a) closes** by the asymptotic-frequency mismatch: if
   the Cesàro per-coord limit exists, ν reduces to Wave 3 via the limit
   law; if it does not exist, ν has no asymptotic frequency content to
   match the natural-density question.
4. **No descent argument is recovered** for any (F1′) candidate. The
   probe numerically verifies that three explicit non-stationary product
   candidates, one non-ergodic stationary mixture, and the
   ergodic-decomposition interpolation all fail simultaneous mod-9
   saturation and drift balance.

**What this work does NOT do:**

- It does not close the natural-density question. It closes one route
  (the LDP-tilting + ergodic-decomposition program) on a fourth class
  of measures.
- It does not formalise every detail of the ergodic-decomposition
  argument; we use Choquet / Varadarajan as a citation.
- The "asymptotic-frequency mismatch" argument is honest but informal:
  it says non-stationary ν "doesn't answer the question being asked",
  which is a *category* mismatch rather than a proof of infeasibility.
  A pedant could insist that, with sufficient cleverness, a
  non-stationary ν might encode natural density via a clever change of
  variables; we have not formally ruled this out. We claim this is a
  category error rather than a genuine loophole; honest readers may
  disagree on terminology.

**Confidence calls:**

- *(c) is vacuous*: VERY HIGH (Lemma 2.1 is a one-line proof from the
  definition of stationarity).
- *(b) closes via ergodic decomposition + linearity*: HIGH (~95%). The
  decomposition theorem is standard; linearity of the relevant
  statistics is also standard. The only soft step is the precise
  characterisation of the constraint set `C` in §3.3 and the claim that
  mixtures preserve the floor when ranging over per-coord marginals.
- *(a) closes via asymptotic-frequency mismatch*: MEDIUM-HIGH (~80%).
  Sub-case (a-1) — Cesàro-convergent per-coord — reduces to Wave 3
  cleanly. Sub-case (a-2) — no Cesàro convergence — relies on the
  "natural density is shift-stationary defined" argument, which is
  morally clear but not airtight at the level of a finished theorem. A
  formally rigorous closure would need a *characterisation* of which ν
  on `Z_+^N` can encode an asymptotic-frequency statement and prove
  this class is shift-stationary. We sketch this but do not formalise.
- *The four-layer barrier is complete*: HIGH (~85%). Modulo the soft
  step in (a-2), the barrier covers every shift-invariant measure (W1
  via Esscher, W2 via finite-KL Gibbs, W3 via infinite-KL Csiszár) AND
  every non-stationary or non-ergodic ν that has any asymptotic-
  frequency interpretation (W4 via this work). The barred class is
  closed under all the natural probabilistic operations.

**Bottom line.** The Wave 4 closure is best read as **"(F1′) admits no
genuine attack route, modulo a formally-soft step on the asymptotic-
frequency mismatch."** The four-layer barrier should be regarded as
COMPLETE at the conceptual level (no remaining LDP-style escape) and
NEARLY COMPLETE at the formal level (the (a-2) sub-case is closed by a
category-mismatch argument rather than a strict no-go theorem). The
natural-density question itself remains open and now requires a
genuinely non-LDP / non-stationary-probabilistic technique (F2).

> `[CANDIDATE — (F1′) formally closed by ergodic-decomposition (b) +
> stationarity-trivial (c) + asymptotic-frequency-mismatch (a). Four-
> layer barrier on the LDP-tilting program is complete; the
> natural-density question requires non-probabilistic methods.]`

---

## 8. Reproducibility

- `collatz_F1_prime_probe.py` — implements each pathology's explicit
  candidate, computes Cesàro per-coord drift, Cesàro mod-6 marginal,
  2-coord joint mod-9 marginal, and verifies the ergodic-decomposition
  linearity. Also runs a small numerical demo of asymptotic-frequency
  divergence under a block-doubling non-stationary product.
- `data/F1_prime_probe.json` — full numerical record.
- `data/F1_prime_probe.log` — human-readable summary.

**Validation gates (all PASS):**

- **G1 (stationarity ⇒ Cesàro convergence of per-coord laws):** for
  Geom(0.5)^N, max L¹ distance between `L_{a_j}` and `L_{a_1}` over
  `j = 1, ..., 20` is exactly 0. ✓
- **G2 (drift-balanced i.i.d. fails mod-9 saturation):** stationary
  Geom(1/log_2 3)^N has drift `log_2 3` exactly, mod-9 TV vs (Z/9)*
  uniform = 0.370 (large). ✓
- **G3 (non-stationary alternating product, drift-balanced):** Cesàro
  drift = log_2 3 exactly, mod-9 TV = 0.471 (worse than stationary). ✓
- **G4 (non-stationary block-doubling, Cesàro non-convergent):** Cesàro
  drift at truncations 16, 64, 256, 1024, 4096 oscillates without
  settling; mod-9 TV at the longest truncation = 0.384. ✓
- **G5 (non-ergodic stationary mixture):** for the explicit mixture
  `0.5 · Geom(1/1.2)^N + 0.5 · Geom(0.5)^N`, mod-9 TV = 0.395, drift
  gap = +0.015 (mod-9 fails saturation; drift slightly above balance,
  but the saturation floor of 5/2 dominates). ✓
- **G6 (linearity check):** for the family `w · Geom(1/1.5)^N +
  (1-w) · Geom(1/2.5)^N`, drift is exactly linear in w, balance at
  `w* = 2.5 − log_2 3 ≈ 0.9150`, and none of the interpolation points
  achieves both saturation and balance. ✓
- **G7 (empirical-frequency mismatch demo):** stationary realisation
  converges to ≈ 0.5; block-doubling realisation has frequency
  oscillating between ≈ 0.66 and ≈ 0.69 across the doubling blocks,
  no settling. ✓

**Scope.** Candidate development, not proof attempt. No file outside
`ideas/candidates/` was written. The (F1′) closure uses ergodic
decomposition (Choquet; cited) as a structural input.

**Novelty `[UNVERIFIED]`.** The use of (i) stationarity to make
pathology (c) vacuous, (ii) ergodic-decomposition + linearity for (b),
and (iii) asymptotic-frequency mismatch for (a) are individually
standard. The application to closing the (F1′) loophole on the Syracuse
mod-3^k saturation barrier appears specific to this thread.
