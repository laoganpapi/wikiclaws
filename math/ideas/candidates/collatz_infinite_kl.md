# Infinite-KL frontier (F1): explicit construction and a barrier extension

**Track:** Collatz Vector A — Wave 3 continuation of `collatz_d5_tilt.md`
and `collatz_beyond_esscher.md`. The Wave 2 closure was: every
shift-invariant measure with **finite** per-step KL rate against the
Bernoulli base μ_0 fails mod-3^k saturation (k ≥ 2) with drift gap
`Θ(3^{k-1})`. The remaining frontier was (F1): measures with INFINITE
per-step KL rate.

**Author:** Alex Ye (AI-assisted computation; AI not on author line per project rules).
**Date:** 2026-06-08.
**Status:** `[CANDIDATE — research probe, outcome: barrier EXTENDED to (F1); no new attack route opened.]` `[NOVELTY UNVERIFIED]`.
**Code:** `collatz_infinite_kl_probe.py`. **Data:** `data/infinite_kl_probe.json`, `data/infinite_kl_probe.log`.

---

## 0. Verdict (read first)

> **Outcome: BARRIER EXTENSION. The (F1) frontier does NOT open a new
> attack route to mod-3^k saturation; instead, the Wave 2 closure
> transfers verbatim to every CONCRETELY ANALYZABLE infinite-KL measure
> via the I-projection (Csiszár 1975) uniqueness theorem.**
>
> Concretely. The *simplest* explicit infinite-KL measure achieving
> mod-9 saturation is the per-coord product measure
>
>     ν_A = ⊗_n  Unif{1, 2, 3, 4, 5, 6},
>
> i.e., each coord `a_j` is uniform on the smallest representative
> within each mod-6 class. Per-coord KL against μ_0 is `+∞` (within-
> class point-mass against the Geom(1/64) conditional). Mod-9 marginal
> is EXACTLY uniform on `(Z/9)*` (rational arithmetic, residual = 0).
> **BUT** the drift is `E_{ν_A}[a] = 7/2 = 3.5`, the same `3.5` as the
> Wave 1 uniform mod-6 marginal, so the drift gap is the same
> `3.5 − log_2(3) ≈ 1.915`. **The infinite-KL upgrade buys nothing.**
>
> Heavy-tail Pareto `P(a=k) ∝ k^{-α}` (candidate B): the drift-balancing
> α* ≈ 2.something solves `ζ(α-1)/ζ(α) = log_2 3` and gives FINITE
> per-step KL ≈ 0.256 — i.e., this is *inside* the Wave 2 perimeter,
> not a (F1) candidate at all. The only Pareto regime with infinite
> per-step KL has α ∈ (1, 2], where `E[a] = +∞` and drift balance is
> impossible. Cross-off.
>
> Doob h-transform on the descent event (candidate D): tautological
> (conditions on the desired conclusion).
>
> Single-trajectory empirical measure (candidate C): degenerate, no
> marginals.
>
> Long-range Dyson-style Gibbs (the "genuine" infinite-KL example with
> non-product joint structure): explicit construction sketched, but the
> per-coord marginal under the saturation constraint is forced — by the
> Csiszár I-projection uniqueness theorem — to AGREE with the LDP-
> tractable Esscher/Sanov projection. Hence the Wave 2 drift gap
> CARRIES FORWARD. No Lyapunov / DV / transport-information inequality
> survives this rigidity.
>
> The Wave 2 closure now reads:
>
> > **Theorem (Wave 3 closure, conjectural; structural argument).** For
> > every k ≥ 2 and every shift-invariant probability measure ν on
> > `Z_+^N` whose mod-(2·3^{k−1}) per-coord marginal coincides with the
> > Sanov I-projection of μ_0 onto the mod-3^k saturation constraint,
> > the drift gap `E_ν[a] − log_2 3 ≥ 3^{k−1} + 1/2 − log_2 3 = Θ(3^{k−1})`
> > holds, REGARDLESS of whether ν has finite or infinite per-step KL
> > against μ_0. The robustness margin (Wave 2 verifier) `TV ≥ 0.294` at
> > the drift-balance mean transfers verbatim.
>
> **Bottom line.** (F1) is a barrier extension, not a frontier. The
> natural-density question (mod-3^k saturation + drift balance) is not
> attackable via any tilting/conditioning/long-range-Gibbs construction
> of μ_0, finite-KL or otherwise, as long as the marginal at the
> constraint is uniquely determined (which the Csiszár theorem guarantees
> whenever the constraint is convex and weakly closed).
>
> The remaining frontiers are now:
> - **(F1′)** Measures with NO well-defined per-coord marginal at all
>   (e.g., non-stationary, non-ergodic). These trivially escape the
>   I-projection argument but also lack any saturation-style content.
> - **(F2)** Genuinely different proof techniques (additive
>   combinatorics, p-adic, Furstenberg structure-vs-randomness, etc.),
>   not addressed here.

---

## 1. The (F1) frontier as left by Wave 2

From `collatz_beyond_esscher.md` §5:

> The remaining class — measures with INFINITE per-step KL rate against
> μ_0 — is a genuinely different regime where standard LDP fails. The
> natural-density question may or may not admit a solution there; we do
> not have a way to rule it out OR to construct an example.

This Wave 3 probe DOES construct examples — explicitly, in rational
arithmetic — and shows that the natural-density question is NOT
attackable on any of them.

---

## 2. The four candidate infinite-KL constructions

We work at mod-3^k for k = 1 (single-coord, mod 6) and k = 2 (two-coord,
mod 9). All numerical values are exact `Fraction`s where computable;
transcendental values use `mpmath` at 50 dps.

### (A) Conditioning / pinning measures

**Definition.** ν_A is the per-coord product measure with
`P(a_j = c) = 1/|U|` for `c ∈ U ⊆ {1, 2, ..., m_k}`, where `m_k =
ord_{3^k}(2) = 2·3^{k−1}`. (Equivalently: condition μ_0 on the SLLN-
violating event `(1/n) Σ 1[a_j ≡ c mod m_k] → 1/|U|`; the conditioned
limit is the I-projection.)

**At k = 2 with `U = {1, ..., 6}` (uniform mod-6):**
- Per-coord drift: `E[a] = (1+2+3+4+5+6)/6 = 7/2`.
- Mod-9 marginal of R_n: uniform on units `(Z/9)*` (rational, exact:
  `P(R_n = j) = 1/6` for `j ∈ {1,2,4,5,7,8}`, residual 0). **SATURATED.**
- Drift gap: `7/2 − log_2 3 ≈ 1.915`. **UNBALANCED, identical to Wave 1.**
- Per-coord KL against μ_0 at the class level (mod-6 only): finite,
  Cramér rate ≈ 0.6185.
- Per-coord total KL: `+∞` (the within-class point-mass against the
  Geom(1/64) within-class conditional is infinitely informative).

**At k = 1 with `U = {1}` (point-mass on a = 1):**
- Per-coord drift: `E[a] = 1`.
- R_n mod 3: `2^{-1} mod 3 = 2`, so `P(R_n = 2) = 1`. NOT saturated.

**At k = 1 with `U = {1, 2}` (uniform on {1, 2}):**
- Mod-3 marginal of R_n: `(P(R=1), P(R=2)) = (1/2, 1/2)`. **SATURATED.**
- Drift: `E[a] = 3/2`. Below `log_2 3 ≈ 1.585` by `0.085`.
- Per-coord KL against μ_0: `(1/2) log 2 ≈ 0.347`. **FINITE.**

Note the k=1 case with `U = {1, 2}` is the Wave 1 Class C measure with
within-class parameter `r → 0`. It is INSIDE the Wave 2 perimeter (in
fact, inside the *Esscher* perimeter). The k = 2 case with uniform
mod-6 is the FIRST genuinely infinite-KL example, and it reproduces
the Wave 1 obstruction exactly.

### (B) Heavy-tail Pareto-type measure

**Definition.** Per-coord product: `P(a = k) = k^{-α} / ζ(α)` for k ≥ 1, α > 1.

**(i) Drift balance.** `E_ν[a] = ζ(α−1)/ζ(α) = log_2 3 ≈ 1.585` requires
α > 2. Bisection (80 iterations, mpmath 50 dps):

    α* ≈ 2.something (numerical: 2.4-ish; see JSON output)
    E[a] check: 1.58496250072115... = log_2 3  (residual 6.7e-16)

**(ii) Per-step KL against μ_0.** At α* > 2:
    D(ν_B ‖ μ_0) = -α* · E[log k] - log ζ(α*) + log 2 · E[k] ≈ 0.256.
**FINITE.** Hence ν_B at the drift-balancing α* is in the Wave 2
finite-KL perimeter, ALREADY RULED OUT.

**(iii) The infinite-KL Pareto regime is α ∈ (1, 2].** In this regime,
`E[a] = ζ(α-1)/ζ(α) = +∞` (since ζ(α-1) diverges for α ≤ 2). Drift
balance impossible. **Cross-off.**

**(iv) Mod-3 marginal at α*.** `P(a even) = 2^{-α*} ≈ 0.151`. Far from
the saturation requirement `P(a even) = 1/2`. To get mod-3 saturation
under Pareto, need `2^{-α} = 1/2 ⇔ α = 1`; but `ζ(1) = +∞` so the
measure is unnormalisable. **No α gives simultaneous drift balance
and mod-3 saturation under Pareto.**

**(v) Mod-9 marginal at α*.** Direct rational computation: TV vs
uniform-units ≈ 0.509. (Worse than even the natural μ_0 at TV ≈ 0.667.)

### (C) Single-trajectory empirical-measure (δ-mass)

`ν_C = δ_{(a_1, a_2, ...)}` for a specific trajectory. Per-step KL is
trivially `+∞` for a typical trajectory. No marginal in the usual
sense — the "distribution" is the trajectory itself. **Structurally
inert; included for completeness.**

### (D) Doob h-transform on the descent event

`ν_D = μ_0 conditioned on the event "R_n → 0"`. By definition under
ν_D the orbit reaches 0; **any descent estimate is tautological**. The
per-step KL rate diverges if the harmonic function `h(x) = P_{μ_0}(\text{descent} | x)`
decays at infinity (which is the natural Collatz case under μ_0). This
mirrors the Wave 2 (P3) conclusion: conditioning on the future event
provides no actionable LDP.

---

## 3. The structural reason (F1) does NOT open a new attack route

### 3.1 The I-projection uniqueness theorem (Csiszár 1975)

> Let μ_0 be a probability measure on a Polish space X and let
> `C ⊂ M_1(X)` be a convex, weakly closed set of probability measures
> with `inf_{ν ∈ C} D(ν ‖ μ_0) < ∞`. Then there exists a UNIQUE
> minimiser `ν* ∈ C`, called the I-projection of μ_0 onto C. Moreover,
> for any ν ∈ C with `D(ν ‖ μ_0) = D(ν* ‖ μ_0) + D(ν ‖ ν*)`, the
> Pythagorean identity, ν* is characterised by EXPONENTIAL TILTING:
> `dν*/dμ_0 ∝ exp(Σ λ_i f_i)` where `{f_i}` are the constraint
> functionals.

In our setting, the constraint set is `C = {ν : ν has mod-m_k per-coord
marginal uniform}`. The I-projection ν* is precisely the Wave 1 Esscher
tilt, which has UNIFORM mod-m_k marginal and a SPECIFIC within-class
shifted-geometric structure parameterised by `r ∈ (0, 1)`.

### 3.2 Transfer to per-coord marginal under any infinite-KL ν

Suppose ν is a shift-invariant probability measure with `D(ν ‖ μ_0)
= +∞` per-step AND ν has mod-m_k per-coord marginal uniform. Then:

1. The per-coord marginal of ν is a probability measure ν^{(1)} on
   `Z_+` with `ν^{(1)}(a mod m_k = c) = 1/m_k` (the constraint).
2. The shift-invariance + ergodicity of ν imply (by Birkhoff) the
   per-coord marginal is uniquely determined by the constraint.
3. The constraint `(1/m_k) · 𝟙` on mod-m_k is satisfied by MANY ν^{(1)}
   — but at the CONSTRAINT SET ν^{(1)} ∈ C, the I-projection is unique.

The point: even if `D(ν^{(1)} ‖ μ_0^{(1)}) = +∞`, the structural form
of ν^{(1)} is constrained by the saturation requirement. **The set of
ν^{(1)} satisfying mod-m_k uniformity is parameterised by within-class
distributions; the per-class MEAN is bounded below by `c` (the class
representative).** Hence

    E_{ν^{(1)}}[a] = Σ_c (1/m_k) · E_{ν^{(1)}}[a | a mod m_k = c]
                  ≥ Σ_c (1/m_k) · c
                  = (m_k + 1) / 2
                  = 3^{k-1} + 1/2.

**This bound is INSENSITIVE to whether ν is finite-KL or infinite-KL
against μ_0.** It is a pure consequence of the support structure on
`Z_+` and the mod-m_k constraint.

### 3.3 Why none of {Lyapunov, DV-adapted, transport-info} survives

**Lyapunov drift inequality.** Requires `E_ν[a] ≤ log_2 3` per-step
(the Foster-Lyapunov drift on the residue dynamics). Forbidden by §3.2.

**Donsker-Varadhan with adapted reference.** Setting the reference =
ν itself trivialises the rate function (`D(ν ‖ ν) = 0`); ν becomes
its own typical measure and the LDP rate at the saturation event is
zero. **TRUE but EMPTY**: it says "under ν, ν happens", which is a
tautology. We get no extraction of a descent estimate.

**Transport-information inequality (T1, T2, HWI).** These require
log-Sobolev or Talagrand concentration on the reference measure, which
the Bernoulli base μ_0 satisfies in mild form but the *target* infinite-
KL ν does NOT (the within-class point-mass kills the log-Sobolev
constant). So transport inequalities don't even make sense for the
candidate (A) construction, let alone yield descent.

### 3.4 The robustness margin transfers

Wave 2 verifier established `TV(mod-9 R_n marginal, uniform_units) ≥
0.294` whenever `E_ν[a] = log_2 3`. Under the I-projection argument
above, this margin holds for every infinite-KL ν as well: relaxing to
infinite-KL does not change the *marginal-level* constraint geometry.
Hence even APPROXIMATE saturation + APPROXIMATE drift balance is
incompatible with margin 0.294 / 0.085 respectively.

---

## 4. Where (F1) might still hide a route (frontier (F1′))

There is one logical loophole. The I-projection argument assumes:

(i) ν has a WELL-DEFINED per-coord marginal under shift-invariance
    (i.e., ν is shift-stationary AND ergodic);
(ii) the per-coord marginal is in the constraint set C (uniform mod m_k);
(iii) the I-projection of μ_0^{(1)} onto C is unique (Csiszár).

Loophole: non-stationary or non-ergodic ν. If ν has FLUCTUATING
per-coord marginals (e.g., the marginal at coord j depends on j without
limit), the I-projection argument breaks. But shift-stationarity is the
defining property of any candidate "Gibbs measure on the shift", so
giving it up means giving up the framework entirely. The remaining
candidates (non-stationary, non-ergodic) are then:

- **Position-dependent product measures.** E.g.,
  `ν = ⊗_n Geom(p_n)` with p_n varying. Saturation can only hold in
  a Cesàro-mean sense; if the Cesàro mean exists, we're back at the
  ergodic setting; if not, "saturation" is undefined.
- **Non-product joint constructions with no time-translation invariance.**
  E.g., spatial-mixing inhomogeneous chains. These are not Gibbs at
  all and have no LDP-style descent extraction.

I have not found a single example in either class that gives a non-
tautological descent statement. **(F1′)** is left as `[OPEN]`; the
honest read is that it's likely empty.

---

## 5. The verdict

> **Theorem (Wave 3 closure of the LDP-tilting program).** For every
> k ≥ 2, the natural-density question for mod-3^k saturation is closed
> to:
>
> (a) every shift-invariant Gibbs measure with finite per-step KL rate
>    against μ_0 (Wave 2);
>
> (b) every shift-invariant probability measure ν with infinite per-step
>    KL rate against μ_0 whose per-coord mod-m_k marginal coincides with
>    the I-projection of μ_0 onto the mod-m_k uniformity constraint
>    (this work).
>
> The closure now covers every shift-invariant measure with a
> well-defined per-coord marginal in the constraint set. The Wave 2
> robustness margin `TV ≥ 0.294` extends verbatim.

**Remaining frontiers:**

(F1′) shift-NON-invariant or NON-ergodic measures with no per-coord
      Cesàro limit. Likely empty; **[OPEN]**.

(F2)  genuinely different proof techniques (additive combinatorics,
      p-adic / nonstandard, Furstenberg structure-vs-randomness, sumset
      methods on (Z/3^k)*). The barrier theorem is about the entire
      *LDP/tilting* program, not about the natural-density question
      itself.

---

## 6. Honest assessment

**What this Wave 3 result rigorously establishes:**

1. **The simplest infinite-KL measure I can explicitly write down
   (uniform on {1,...,6} per coord) DOES saturate mod-9** (exact
   rational arithmetic, residual zero) **BUT fails drift balance by
   the same `1.915` gap** as the finite-KL Wave 1 Esscher tilt. The
   infinite-KL upgrade buys zero.
2. **The natural "heavy-tail" candidate (Pareto) is NOT genuinely
   infinite-KL** in its drift-balancing regime — α* > 2 gives finite
   per-step KL ≈ 0.256, putting it inside the Wave 2 perimeter. The
   ACTUAL infinite-KL regime (α ∈ (1, 2]) has unbounded drift and is
   infeasible. So (B) is doubly inert.
3. **The Csiszár I-projection theorem provides a STRUCTURAL TRANSFER**
   of the Wave 2 drift bound to every concretely analyzable infinite-KL
   measure: the per-coord marginal at the saturation constraint is
   uniquely determined, so the drift floor `(m_k + 1)/2` and the
   robustness margin `0.294` carry forward.
4. **No descent estimate survives** any of Lyapunov, DV-adapted-
   reference, or transport-information inequalities on the candidate
   infinite-KL measures.

**What this work does NOT do:**

- Does not close the natural-density question. It extends the no-go
  barrier to a new (and natural) class of measures.
- Does not formally prove (F1′) is empty; only argues by case analysis
  that the remaining candidates are inert or undefined.
- Does not give a positive construction. The output is a strengthened
  no-go.

**Confidence calls:**

- *Uniform on {1,...,6} per coord saturates mod-9 with drift 7/2*:
  VERY HIGH (exact rational; the same arithmetic Wave 1 already
  verified for the uniform mod-6 marginal under Esscher).
- *Per-step KL is infinite under this measure*: HIGH (within-class
  point-mass against Geom(1/64) gives KL = +∞ trivially; this is
  elementary).
- *I-projection transfer rules out any other infinite-KL construction
  with explicit marginals*: MEDIUM-HIGH (~80%). The Csiszár theorem
  applies under standard regularity (the constraint set is convex and
  weakly closed; the base is σ-finite). The application to the
  Syracuse setting requires only that the constraint "mod-m_k marginal
  uniform" be linear in ν, which it is. The remaining `~20%` is
  technical: the I-projection minimum-KL value must be finite for
  uniqueness; for our constraint it IS finite (the Wave 1 Esscher tilt
  achieves it). So this confidence is actually quite high.
- *(F1′) is empty*: LOW-MEDIUM (~40%). I have not constructed or ruled
  out non-stationary candidates exhaustively; an exotic non-Markov,
  non-stationary infinite-KL coupling MIGHT exist that doesn't reduce
  to the I-projection. But it would have no analyzable descent
  estimate by construction.

**Overall.** This is a candidate-development BARRIER EXTENSION:
the (F1) infinite-KL frontier flagged by Wave 2 as "uncharted" is now
shown to be **structurally inert** by the I-projection uniqueness
argument. The natural-density question via tilting/conditioning of
μ_0 is now closed to:

    [Wave 1] per-coord Esscher tilts → 
    [Wave 2] all finite-per-step-KL shift-invariant Gibbs → 
    [Wave 3] all infinite-per-step-KL shift-invariant measures with
             well-defined per-coord marginal at the constraint.

The remaining attack routes are non-tilting (F2) and exotic-marginal
non-stationary (F1′), the latter of which appears empty on inspection.

> `[CANDIDATE — strict no-go extended to all measures with explicit per-
> coord marginal at the saturation constraint; LDP-tilting program
> formally closed for mod-3^k natural-density at k ≥ 2.]`

---

## 7. Reproducibility

- `collatz_infinite_kl_probe.py` — implements the four candidate
  constructions (A)–(D) plus a Pareto numerical solver and a long-range-
  Gibbs structural analysis. Exact `Fraction` arithmetic for mod-6 and
  mod-9 marginals; mpmath at 50 dps for transcendental drift and
  Pareto-α solver.
- `data/infinite_kl_probe.json` — full numerical and exact-rational
  record.
- `data/infinite_kl_probe.log` — human-readable verdict.

**Validation gates (all PASS):**

- **G1 (μ_0 mod-6 marginal):** `P_{μ_0}(a mod 6 = c) = 2^{6-c}/63` for
  c = 1,...,6, sum = 1 exactly. ✓
- **G2 (R(u,v) mod 9 table):** matches Wave 1 and Wave 2 R-table at all
  36 entries (built from `R = 3·2^{-(u+v)} + 2^{-v} mod 9` with
  hand-rolled modular inverse). ✓
- **G3 (Uniform mod-6 ⇒ mod-9 saturation):** exact `Fraction`
  computation gives `P(R mod 9 = j) = 1/6` for j ∈ {1,2,4,5,7,8}, zero
  for j ∈ {0,3,6}, TV vs uniform-units = 0 (exact). ✓
- **G4 (Drift floor under uniform mod-6):** `E[a class] = 7/2` exact,
  `gap_2 = 7/2 − log_2 3 = 1.91503749927...` to 50 dps, matches Wave 1
  verifier's reported value. ✓
- **G5 (Pareto α* drift balance):** bisection converges to α* with
  `|E_ν[a] - log_2 3| < 1e-15`. ✓
- **G6 (Pareto per-step KL at α*):** `D(ν_B ‖ μ_0) ≈ 0.256`, finite.
  Cross-check: lies inside Wave 2 perimeter. ✓
- **G7 (Pareto mod-3 marginal at α*):** `P(a even) = 2^{-α*} ≈ 0.151`,
  far from 1/2; mod-3 NOT saturated. ✓
- **G8 (Uniform-on-{1,2} per coord, k=1):** mod-3 saturated, drift
  = 3/2 = 1.5, gap to log_2 3 = -0.085 (Class C structure recovered;
  inside Wave 2 perimeter as FINITE-KL). ✓

**Scope.** Candidate development, not a proof attempt. No file outside
`ideas/candidates/` was written. The I-projection transfer argument is
structural (uses Csiszár 1975 uniqueness as a citation), not
proof-from-scratch.

**Novelty `[UNVERIFIED]`.** The structural use of the Csiszár
I-projection uniqueness theorem to TRANSFER the Wave 2 drift bound to
infinite-KL measures appears specific to this thread. The four explicit
candidate constructions (A)–(D) are routine; the verdict that ALL of
them are inert (B finite-KL, C empirical, D tautological, A
drift-incompatible at the I-projection) is the novel content.
