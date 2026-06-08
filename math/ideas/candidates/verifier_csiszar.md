# Independent verifier: Csiszár I-projection three-layer closure

**Track:** Collatz Vector A — Wave 3 verifier of `collatz_infinite_kl.md`.
**Author:** Alex Ye (AI-assisted computation; AI not on author line per project rules).
**Date:** 2026-06-08.
**Status:** `[VERIFIED — three-layer closure stands; one citation-strength nuance flagged; no result-level error.]` `[NOVELTY UNVERIFIED]`.
**Code:** `verifier_csiszar.py`. **Data:** `data/verifier_csiszar_probe.json`, `data/verifier_csiszar_probe.log`.

---

## 0. Verdict (read first)

> I red-teamed the Frontier writeup's three-layer closure
> (`collatz_infinite_kl.md`) by:
>
> (a) restating the Csiszár (1975) I-projection theorem with precise hypotheses,
> (b) re-deriving the I-projection of Geom(1/2) onto the constraint set
>     `C_m = {ν : ν(a ≡ c mod m) = 1/m, c = 1..m}` from scratch via Lagrange,
> (c) testing the drift-floor transfer claim on several explicit `ν ∈ C_m`,
>     including infinite-KL ones,
> (d) testing non-stationary loopholes for (F1').
>
> **Verdict.** The three-layer closure is **CONFIRMED**. The drift-floor
> bound `E_ν[a] ≥ (m_k + 1)/2 = 3^{k-1} + 1/2` is correct and holds
> universally over `ν ∈ C_m`. The infinite-KL frontier (F1) is closed.
>
> **One nuance flagged (severity: minor / citation strength, not result):**
> the Frontier writeup leans on Csiszár's uniqueness theorem to justify
> the floor bound `(m_k + 1)/2`, but in fact this bound is an *elementary*
> consequence of (i) the per-class probability constraint `ν(a ≡ c) = 1/m`
> and (ii) support `ν ⊆ {1, 2, ...}`. Csiszár's theorem is the right tool
> to **identify** the I-projection `ν*` (which has within-class
> Geom(1−2^{-m}) structure and mean `(m+1)/2 + m/(2^m−1)`, *strictly above*
> the floor), but it is not load-bearing for the descent-floor argument.
> The closure result is still correct; the citation is stronger than
> needed.
>
> No result-level error found. The transfer step in §3.2 of the Frontier
> writeup is therefore a clean elementary inequality (not invoking
> Csiszár), which is actually a STRENGTHENING of the argument: the floor
> is *universal* across `C_m`, not contingent on uniqueness of any
> projection.

---

## 1. Csiszár's I-projection uniqueness theorem (precise statement)

**Reference.** I. Csiszár, "I-divergence geometry of probability distributions
and minimization problems", *Ann. Probab.* **3** (1975), 146–158.
Theorems 2.1 / 3.1 (existence) and 2.2 (uniqueness, "Pythagorean identity").

**Statement (verifier's restatement).** Let `μ_0` be a σ-finite measure on
a measurable space `(X, F)`, and let `C ⊂ M_1(X)` be a convex set of
probability measures on `(X, F)`, closed under variation-norm convergence.
Assume the feasibility condition

    inf_{ν ∈ C}  D(ν ‖ μ_0)  <  +∞.                                    (*)

Then:

(C1) **Existence + uniqueness.** There exists a UNIQUE `ν* ∈ C`, the
     *I-projection of μ_0 onto C*, achieving the infimum in (*).

(C2) **Exponential form (under linear constraints).** If
     `C = {ν : E_ν[f_i] = c_i, i = 1..n}` for measurable `f_i` with
     `ν*` in the relative interior, then `dν*/dμ_0 ∝ exp(Σ λ_i f_i)`
     for some Lagrange multipliers `λ_i`.

(C3) **Pythagorean identity.** For every `ν ∈ C` with `D(ν ‖ μ_0) < ∞`,
     `D(ν ‖ μ_0) ≥ D(ν* ‖ μ_0) + D(ν ‖ ν*)`. (Equality on a linear
     subset.)

**Hypotheses verified for our setting:**

- `X = Z_+ = {1, 2, ...}` with counting σ-algebra (Polish, hence ok). ✓
- `μ_0 = Geom(1/2)`: `μ_0(k) = 2^{-k}` for `k ≥ 1`. σ-finite. ✓
- `C_m = {ν : Σ_{k ≡ c (mod m)} ν(k) = 1/m, c = 1..m}` is the
  intersection of finitely many linear constraints; convex and weakly
  closed in `M_1(Z_+)`. ✓
- Feasibility: the Esscher tilt below (computed in §2) achieves
  `D(ν* ‖ μ_0) = log[(1 − 2^{-m})/m] + (log 2)(m+1)/2 < ∞`. ✓

**Important subtlety.** What Csiszár gives is uniqueness of the
*minimizer* `ν*` in `C`. It does NOT say every `ν ∈ C` agrees with `ν*`
outside the minimizing event. So any "transfer" of a property of `ν*` to
a generic `ν ∈ C` must be justified *directly from the constraint*, not
from Csiszár's uniqueness. This is the nuance the Frontier writeup
glosses over.

---

## 2. The I-projection of Geom(1/2) onto C_m (derived from scratch)

**Problem.** Minimize `D(ν ‖ μ_0)` over probability measures ν on `Z_+`
subject to

    Σ_{k: k ≡ c (mod m)} ν(k) = 1/m,    c = 1, 2, ..., m.            (Λ_c)

**Lagrangian setup.** With Lagrange multipliers `λ_1, ..., λ_m`:

    L(ν) = Σ_k ν(k) log(ν(k)/μ_0(k)) + Σ_c λ_c (Σ_{k ≡ c} ν(k) − 1/m).

Stationarity (treating `ν(k)` as the variable, and including the
"probability" multiplier absorbed into `λ`):

    log(ν(k)/μ_0(k)) + 1 + λ_{[k mod m]} = 0
    ⇒ ν(k) = μ_0(k) · exp(−1 − λ_{[k mod m]}) =: μ_0(k) · β_c
                                                    where c = k mod m.

**Solving for β_c.** Constraint (Λ_c):

    Σ_{j ≥ 0} ν(c + jm) = β_c · Σ_{j ≥ 0} 2^{-(c+jm)}
                       = β_c · 2^{-c} / (1 − 2^{-m}) = 1/m.

Hence

    β_c = (1/m) · (1 − 2^{-m}) · 2^c.                                  (†)

**Closed form.** For `k = c + jm`, `c ∈ {1..m}`, `j ≥ 0`:

    ν*(k) = (1/m)(1 − 2^{-m}) · 2^{−jm}.

So conditional on `k ≡ c (mod m)`, the "block index" `j` is
`Geom(1 − 2^{-m})` on `{0, 1, 2, ...}`, independent of `c`. (This matches
the Wave-1 Esscher tilt with the within-class shifted-geometric structure
parameterised by `r = 2^{-m}`.)

**Mean.**

    E_{ν*}[k] = Σ_c (1/m) · (c + m · 2^{-m}/(1 − 2^{-m}))
              = (m+1)/2 + m/(2^m − 1).                                 (M*)

This **strictly exceeds** the floor `(m+1)/2` by `m/(2^m − 1)`.

**Numerical verification (exact rationals).**

| m  | (m+1)/2 (floor)    | I-proj mean (exact)         | I-proj mean (float) |
|----|--------------------|------------------------------|---------------------|
| 2  | 3/2                | 13/6                          | 2.1667              |
| 6  | 7/2                | 151/42                        | 3.5952              |
| 18 | 19/2               | 553417/58254                  | 9.5001              |

KL of I-projection (Wave-1 Esscher Cramér rate at uniform mod-m target):

    D(ν* ‖ μ_0) = log[(1 − 2^{-m})/m] + (log 2)(m+1)/2.

For m = 6: `D ≈ 0.6185`, matching Wave 1 / Wave 2's Cramér rate exactly.

**Match with Frontier's claim:** The Frontier writeup says "the
I-projection has per-coord mean (m_k + 1)/2 = 3^{k−1} + 1/2." Strictly,
this is **incorrect**: the I-projection has mean `(m+1)/2 + m/(2^m − 1)`,
which is STRICTLY LARGER than `(m+1)/2`. However, the floor `(m+1)/2` is
indeed correct as a UNIVERSAL LOWER BOUND on `E_ν[a]` for any `ν ∈ C_m`
(see §3 below). The Frontier's verbal description conflates "I-projection
mean" with "support floor of the I-projection's class-conditional means."
The conclusion stands; only the verbal labelling needs care.

---

## 3. The drift-floor transfer claim (universal, NOT contingent on Csiszár)

**Claim (to verify).** For every probability measure `ν` on `Z_+` with
`ν(a ≡ c mod m) = 1/m` for `c = 1..m`,

    E_ν[a] ≥ (m+1)/2.                                                  (F)

**Elementary proof.**

    E_ν[a] = Σ_c P(a ≡ c) · E[a | a ≡ c]
           = (1/m) Σ_c E[a | a ≡ c]                    [by constraint]
           ≥ (1/m) Σ_c c                              [since a ≥ c on the event a ≡ c]
           = (m+1)/2.                                  ∎

The inequality `E[a | a ≡ c] ≥ c` is elementary: conditional on
`a ≡ c (mod m)` and `a ∈ Z_+`, the smallest representative is `c` itself.
Equality holds iff the conditional is a point-mass at `c`.

**Independence from Csiszár.** This proof uses (i) the constraint `Λ_c`
and (ii) the support `ν ⊆ {1, 2, ...}`. It does NOT need Csiszár's
uniqueness theorem at all.

**Empirical verification on explicit ν candidates** (`verifier_csiszar.py`):

| ν                                          | m | E_ν[a] | (m+1)/2 | ≥ floor |
|---------------------------------------------|---|--------|---------|---------|
| Unif{1, 2}                                  | 2 | 3/2    | 3/2     | =       |
| Unif{1..6}                                  | 6 | 7/2    | 7/2     | =       |
| Heavier reps {1, 8, 15, 22, 29, 36}         | 6 | 37/2   | 7/2     | >       |
| Unif{1..12} (each class hit twice)          | 6 | 13/2   | 7/2     | >       |
| Esscher / I-projection (within-class Geom)  | 6 | 151/42 | 7/2     | >       |

The first two attain the floor (point-mass at class minimum); the rest
strictly exceed it. All four are INFINITE-KL against `μ_0 = Geom(1/2)`
when the within-class conditional is a point-mass (cases 1, 2, 3); case 4
is finite-KL (`= log 12 − …` finite); case 5 is the I-projection itself.

**Mod-9 R-marginal cross-check.** For each candidate ν on `m = 6`, the
mod-9 marginal of `R(u,v) = 3·2^{−(u+v)} + 2^{−v} (mod 9)` for IID
`u, v ~ ν` is:

| ν                                  | TV(R mod 9, uniform-units) | drift E[a] | drift − log_2 3 |
|------------------------------------|----------------------------|------------|------------------|
| Unif{1..6}                         | 0 (exact)                   | 3.5        | +1.915           |
| Heavier reps                       | 0 (exact)                   | 18.5       | +16.915          |
| Unif{1..12}                        | 0 (exact)                   | 6.5        | +4.915           |

All saturate mod 9; all fail drift balance by ≥ 1.915. The
"infinite-KL upgrade buys nothing" claim is confirmed.

---

## 4. (F1′) loophole tests: non-stationary measures

I tested four explicit non-stationary candidates:

1. **Position-dependent product with increasing M_n:** `ν = ⊗_n Unif{1..n}`.
   Per-step drift `(n+1)/2 → ∞`. Cesàro drift diverges. **No descent.**

2. **Alternating product:** `Unif{1..2}` at even coords, `Unif{1..6}` at odd.
   Per-step drifts alternate 3/2 and 7/2. Cesàro = 5/2 > log_2 3. **No descent.**

3. **Sparse point-mass:** `δ_1` at density ρ, `Unif{1..6}` elsewhere.
   For drift balance need ρ ≈ 0.766. But then mod-6 marginal at class 1 is
   `(5ρ + 1)/6 ≈ 0.805 ≠ 1/6`. Cannot simultaneously balance drift AND saturate.
   **Infeasible.**

4. **Long-range bursty Gibbs:** even without time-translation invariance,
   if the Cesàro empirical mod-m marginal converges to uniform, the floor
   `(m+1)/2` applies in Cesàro mean by Fatou/Jensen. If the Cesàro
   marginal does NOT converge to uniform, "mod-3^k saturation" is undefined
   on ν, so the natural-density question is vacuous on it. **Empty by
   either branch.**

No non-stationary candidate gives descent. The Frontier's (F1′) verdict
("likely empty") is correct in the natural-density-relevant sense.

---

## 5. Errors and nuances found

**[E1] Citation strength (MINOR, terminology only).** The Frontier
writeup attributes the floor bound `E_ν[a] ≥ (m+1)/2` to the Csiszár
I-projection uniqueness theorem. Strictly, the floor is an elementary
consequence of the linear constraint and the support (`{1, 2, ...}`),
not requiring Csiszár. Csiszár is the right tool to *identify* the
unique minimizer `ν*` (the Esscher tilt with within-class
`Geom(1 − 2^{-m})`), whose mean is `(m+1)/2 + m/(2^m − 1)`, strictly
above the floor. **Consequence:** the result is correct; the argument
is actually stronger than the writeup claims (no Csiszár dependence).

**[E2] Mislabel of "I-projection mean."** Frontier (sec 3.2 + sec 3.3 +
verdict §5) says "I-projection has mean `(m_k + 1)/2 = 3^{k−1} + 1/2`."
This is the FLOOR, not the I-projection mean (which is
`(m+1)/2 + m/(2^m − 1)`). The two coincide only as `m → ∞`. **Severity:
verbal-only.** The bound used in the descent argument is correct.

**[E3] (F1′) loophole closure.** The Frontier's analysis is structurally
right: any non-stationary ν compatible with the natural-density question
(i.e., having Cesàro-limit mod-m empirical marginal = uniform) still
satisfies the floor in Cesàro mean. Genuinely non-Cesàro-convergent ν
have no "saturation" defined on them. **(F1′) is empty in the relevant
sense.**

**[E4] Wave 1 / 2 mod-9 saturation arithmetic.** The Frontier's claim
that `Unif{1..6}` per coord gives mod-9 marginal exactly uniform on
`(Z/9)*` with drift 7/2 was independently reproduced here using a
hand-rolled `R(u, v)` table (modular inverse via extended Euclid). **Confirmed.**

---

## 6. Confirmation of three-layer closure

| Layer | Class of ν                                       | Drift floor               | Status |
|-------|--------------------------------------------------|---------------------------|--------|
| 1     | Per-coord Esscher tilts                          | (m+1)/2 + m/(2^m-1)       | ✓ (Wave 1) |
| 2     | All finite-per-step-KL shift-invariant Gibbs     | (m+1)/2 + Esscher floor   | ✓ (Wave 2) |
| 3     | All ν with mod-m_k per-coord marginal = uniform  | (m+1)/2                   | ✓ (this work) |

**Bottom line.** The Wave 3 closure is rigorous as an elementary
inequality on `C_m`, INDEPENDENTLY of Csiszár's uniqueness theorem. The
Csiszár theorem is correctly applicable to identify the I-projection
itself, but the structural transfer to ALL `ν ∈ C_m` follows from the
support floor alone. The natural-density question via tilting /
conditioning of `μ_0` is closed for mod-`3^k` saturation at `k ≥ 2`
across all three layers.

The drift gap `E_ν[a] − log_2 3 ≥ (m_k + 1)/2 − log_2 3 = 3^{k−1} + 1/2 −
log_2 3 ≈ 1.915` at k = 2 holds for ALL ν with uniform mod-`m_k` marginal,
regardless of KL.

> `[VERIFIED — three-layer closure stands. The infinite-KL barrier is
> a clean elementary inequality; Csiszár's role is confined to
> characterising the I-projection itself, not to transferring the floor
> bound.]`

---

## 7. Reproducibility

- `verifier_csiszar.py` — independent implementation. Re-derives:
  - The I-projection via Lagrange (exact `Fraction` betas).
  - The within-class conditional and exact mean `(m+1)/2 + m/(2^m − 1)`.
  - The KL of the I-projection at `m = 6`: 0.6185, matching Wave 1/2.
  - The mod-9 R-marginal of any IID per-coord ν via hand-rolled
    modular inverse (extended Euclid).
  - Four explicit ν candidates in `C_m` and verifies the floor.
  - Four non-stationary candidates and verifies no descent.
- `data/verifier_csiszar_probe.json` — full numerical record.
- `data/verifier_csiszar_probe.log` — human-readable log.

**Validation gates (all PASS):**

- **V1 (Csiszár hypotheses for our C_m):** σ-finite μ_0 ✓, convex and
  weakly-closed C_m ✓, finite I-projection KL ✓.
- **V2 (I-projection from Lagrange):** β_c = (1/m)(1 − 2^{-m}) 2^c ✓,
  within-class Geom(1 − 2^{-m}) ✓, mean = (m+1)/2 + m/(2^m − 1) ✓.
- **V3 (I-projection mean at m = 6):** exact `151/42 ≈ 3.595` (NOT
  `7/2`, contra the Frontier's verbal claim). Floor `7/2` is a SEPARATE
  universal bound.
- **V4 (Floor universality on C_m):** elementary proof; all four
  explicit ν candidates verify `E[a] ≥ (m+1)/2` ✓.
- **V5 (mod-9 saturation for Unif{1..6}):** TV = 0 (exact) ✓.
- **V6 (Drift gap for Unif{1..6}):** 7/2 − log_2 3 = 1.91503749927…
  (50 dps), matches Wave 1 verifier ✓.
- **V7 (Non-stationary candidates):** four explicit candidates, none
  give descent ✓.

**Scope.** Independent verification, no Frontier code imported.
`Fraction` exact arithmetic throughout; `mpmath` at 50 dps for KL.

**Novelty `[UNVERIFIED]`.** The observation that the floor bound
`(m+1)/2` is INDEPENDENT of Csiszár's uniqueness (and is a clean
elementary inequality) is a strengthening of the Frontier's argument
but uses standard techniques. The three-layer closure structure itself
is due to the Frontier agent.
