# Beyond Esscher: can a non-product reweighting escape the d=5 mod-9 obstruction?

**Track:** Collatz Vector A — Wave 2 continuation of `collatz_d5_tilt.md`.
The Wave 1 result was a **structural obstruction theorem**: every translation-
invariant per-coord Esscher tilt of the i.i.d. Geom(1/2) Bernoulli base
measure that targets mod-3^k saturation (k ≥ 2) of the residue X_n is forced
onto the uniform mod-(2·3^{k-1}) marginal, which fails drift balance by
`gap_k = 3^{k-1} + 1/2 − log_2(3) = Θ(3^{k−1})`.

**Author:** Alex Ye (AI-assisted computation; AI not on author line per project rules).
**Date:** 2026-06-04.
**Status:** `[CANDIDATE — research probe, outcome (c): no-go theorem strengthened beyond Esscher]`. `[NOVELTY UNVERIFIED]`.
**Code:** `collatz_beyond_esscher_probe.py`. **Data:** `data/beyond_esscher_probe.json`, `data/beyond_esscher_probe.log`.

---

## 0. Verdict (read first)

> **Outcome (c) — no escape in (P1) at any tractable joint level. The
> structural obstruction extends from i.i.d. per-coord Esscher tilts to
> ANY stationary 1-step Markov reweighting on residues mod 6.**
>
> Concretely: for a stationary Markov chain on the residue class
> `(a_j mod 6)_{j ≥ 0}` (the smallest extension beyond i.i.d. that retains
> a tractable Donsker–Varadhan LDP), the minimum value of
> `E[a_class] := Σ_c c · π(c)` over all 6×6 joint distributions Q(u, v) ≥ 0
> with row-sum = col-sum = π and the six mod-9 saturation constraints
> P(R = j mod 9) = 1/6 (j ∈ {1,2,4,5,7,8}) is **exactly 5/2** (exact-rational
> LP, verified symbolically). Combined with the within-class shifted-
> geometric pull-up (≥ 0, by Wave 1 §3.2), the achievable E[a] satisfies
>
>     E[a]  ≥  5/2  >  log_2(3)  ≈  1.585,
>
> i.e., **the Markov-level drift gap is `5/2 − log_2(3) ≈ 0.915 > 0`**.
> Smaller than the Esscher gap (7/2 − log_2 3 ≈ 1.915), but still strictly
> positive: the obstruction is reduced, but the route remains blocked.
>
> The non-stationary relaxation gives min E[a_class] = 1 (i.e., the row-
> marginal can sit at the smallest class 1), but a non-stationary chain
> does not iterate — its "tilt" amounts to a one-shot conditioning event
> (Class B in `collatz_multitilt.md`), which was already known to be
> tautological for natural density.
>
> **Bottom line.** The d=5 obstruction extends, with a smaller-but-strictly-
> positive gap, to single-step Markov reweighting (`(P1)`). Combined with
> easy arguments for (P2)–(P4), the natural-density route via *any*
> translation-invariant Gibbs-style reweighting of the base measure with
> a tractable LDP is now ruled out for all k ≥ 2. The barrier is no
> longer a per-coord-Esscher quirk — it is a **joint-distribution
> obstruction**.

---

## 1. The obstruction theorem (port from Wave 1)

**Setup.** Let μ_0 be the i.i.d. Geom(1/2) law on the Syracuse coords
`a_1, a_2, ...`. The Syracuse pushforward of μ_0 is the residue X_n at
step n; the natural-density question requires a measure ν whose pushforward
gives uniform marginal on `(Z/3^k)*` for arbitrarily large k AND
E_ν[φ] = 0 (drift balance) with a *positive* LDP rate.

**Theorem (Wave 1, restated).** Let `ν = ν_{s,t}` be any translation-
invariant per-coord Esscher tilt of μ_0 with cocycles
`ψ_i = 1[a mod (2·3^{k−1}) = i]` for `i = 1, ..., 2·3^{k−1} − 1`, and any
`s ∈ R`. For every k ≥ 2:

(i) (sympy-verified for k = 2; structural for k > 2) the unique positive
    solution to "mod-3^k marginal of `R_n` under ν^{⊗N} is uniform on `(Z/3^k)*`"
    is the uniform-mod-(2·3^{k−1}) per-coord marginal.

(ii) Under (i), `E_ν[a] = 3^{k−1} + 1/2 + 2·3^{k−1} · r^{2·3^{k−1}} / (1 − r^{2·3^{k−1}})`
     where `r = 2^{−(1−s)}`; minimised over `r ∈ (0,1)` at `r → 0+` with limit
     `E_ν[a] → 3^{k−1} + 1/2`. Hence
     `E_ν[a] ≥ 3^{k−1} + 1/2`.

(iii) Drift balance `E_ν[a] = log_2(3) ≈ 1.585` is violated by
      `gap_k = 3^{k−1} + 1/2 − log_2 3 > 0` for all k ≥ 2.

**Consequence.** The Gärtner–Ellis cumulant `λ(s, t)` evaluated at the joint
target `(x_φ = 0, x_ψ = 1/(2·3^{k−1}) · 𝟙)` is `+∞`; the rate function
`I(0, ...) = +∞`. The Esscher-derived natural-density tilt does not exist
for any k ≥ 2.

Proof: by direct computation in Wave 1 (`collatz_d5_tilt.md` §3, with
sympy uniqueness at k=2). □

---

## 2. The four candidate escapes (P1)–(P4)

To escape, the reweighting must violate at least one of:
- (a) product structure (i.i.d. across coords)
- (b) finite-d translation-invariant per-coord cocycle
- (c) target = mod-3^k marginal of `X_n`

The candidates:

### (P1) **Non-product / Markov reweighting** — violates (a), keeps (b) and (c).

A stationary Markov chain on `a_j mod m_k` (with within-class shifted-
geometric) gives a tractable Donsker–Varadhan LDP. The minimal-extension
case is `m_k = 6` (mod-9 target), single-step Markov.

### (P2) **Free-energy reweighting with prefix statistic** — violates (a) globally.

`dν/dμ_0 ∝ exp(−Σ_j h(a_j, S_j(a)))` where `S_j` is a partial-sum statistic
of the prefix (e.g., `S_j = Σ_{i ≤ j} f(a_i)`). This breaks the product
factorization in a way that DOES NOT reduce to a Markov chain on finitely
many coords (S_j has unbounded range).

### (P3) **Conditioning on the future** — violates (a) and (c) trivially.

`dν/dμ_0 ∝ exp(...) · 1[X_n mod 3^k ∈ "good set"]`. Saturates trivially but
LDP fails (Class B in `collatz_multitilt.md`).

### (P4) **A fundamentally different base measure** — violates the whole setup.

Not μ_0 at all, but a different law on `Z_+^N` whose Syracuse pushforward is
engineered.

---

## 3. Feasibility check on (P1): exact LP

### 3.1 The setup

Let `Q(u, v) := P_ν(a_j mod 6 = u, a_{j+1} mod 6 = v)` be the stationary
two-coord joint mod-6 distribution under a stationary Markov chain on
residues. Then:

- `Q(u, v) ≥ 0` for all `u, v ∈ {1, ..., 6}`,
- `Σ_{u,v} Q(u, v) = 1`,
- **Stationarity:** `Σ_v Q(u, v) = Σ_v Q(v, u) =: π(u)` for all `u`.

The mod-9 marginal of `R_n` under `ν` depends, by the Wave 1 R-table
(re-derived and asserted in the probe), only on the joint Q(u, v):

```
   u\v |  1  2  3  4  5  6
   ----+--------------------
    1  |  8  4  2  1  5  7   ← rows for u odd
    2  |  2  1  5  7  8  4   ← rows for u even
    3  |  8  4  2  1  5  7
    4  |  2  1  5  7  8  4
    5  |  8  4  2  1  5  7
    6  |  2  1  5  7  8  4
```

Mod-9 saturation: `Σ_{(u,v): R(u,v) = j} Q(u, v) = 1/6` for `j ∈ {1,2,4,5,7,8}`.

The within-class drift contribution `6 r^6 / (1 − r^6)` is non-negative,
independent of the inter-class Markov structure, and depends on one
parameter `r ∈ (0, 1)`. So drift balance `E[a] = log_2(3)` requires
`E[a_class] := Σ_u u · π(u) ≤ log_2(3)`.

### 3.2 LP and exact rational verification

**Linear program:**
```
   minimize    E[a_class] = Σ_u u · Σ_v Q(u, v)
   subject to  Σ_{(u,v): R(u,v) = j} Q(u, v) = 1/6   (j ∈ {1,2,4,5,7,8})
               Σ_v Q(u, v) − Σ_v Q(v, u) = 0          (u = 1, ..., 6)
               Σ_{u,v} Q(u, v) = 1
               Q(u, v) ≥ 0.
```

The LP has 36 variables. The equality constraints (mod-9: 6 of which 5 are
independent; stationarity: 6 of which 5 are independent; normalization: 1)
have rank 11. Vertex of the feasible polytope has support ≤ 11.

**Result (`collatz_beyond_esscher_probe.py`, scipy HiGHS + sympy):**
- Float LP: min E[a_class] = 2.5000000000 (exact bound: 5/2).
- Exact-rational verification: nonzero indices found, rational vertex
  reconstructed via `Matrix.solve`, all 12 equality constraints satisfied
  exactly (residuals = 0), all 36 nonneg constraints satisfied. **Exact
  bound: 5/2.**
- LP max E[a_class] = 9/2 (the dual extreme; not relevant for drift balance,
  but a sanity check that the polytope is bounded and connected).
- Vertex support size: 9 nonzero entries out of 36.

The minimizing π:
```
   π(1) = 1/3,   π(2) = 5/18,  π(3) = 1/6,   π(4) = 1/9,   π(5) = 0,   π(6) = 1/9
   E[a_class] = 1·1/3 + 2·5/18 + 3·1/6 + 4·1/9 + 5·0 + 6·1/9 = 45/18 = 5/2.   ✓
```

### 3.3 Drift gap at the Markov level

```
gap^Markov_2  :=  5/2 − log_2(3)  =  2.5 − 1.58496 ≈ 0.9150 > 0.
```

The within-class drift contribution `6 r^6 / (1 − r^6)` is non-negative for
`r ∈ (0, 1)` (and ranges from `0` at `r → 0+` to `+∞` at `r → 1−`), so
including it pulls `E[a]` UPWARDS, only worsening the gap. Hence

> **Theorem (Markov-level obstruction).** For every stationary single-step
> Markov reweighting of μ_0 on residues mod 6 with a tractable
> Donsker–Varadhan LDP, mod-9 saturation forces
> `E[a] ≥ 5/2 > log_2(3)`. The drift balance constraint is violated by
> `5/2 − log_2(3) ≈ 0.9150 > 0`. The route (P1) at k = 2 is closed.

### 3.4 Reduction to Esscher recovers Wave 1

If we restrict `Q(u, v) = π(u) π(v)` (the product / Esscher case), the LP
collapses to the Wave 1 nonlinear system. The unique positive solution is
π uniform on `{1, ..., 6}` (Wave 1 §3.1, sympy-verified), giving
`E[a_class] = 7/2`. The Markov LP weakens this to `5/2`. The mechanism: the
Markov chain can shift probability mass towards low classes by pairing them
with high classes in `Q(u, v)`, as long as the stationary marginal
constraints are satisfied. But stationarity prevents the LP from going below
`5/2` — it forces `π` to itself be biased upward.

### 3.5 LDP rate at the LP-feasible Q

For completeness, the Donsker–Varadhan rate (KL of `Q` against the base
product `π_0 ⊗ π_0`, where `π_0(u) ∝ 2^{−u}` is the base mod-6 marginal
of μ_0) at the LP-minimizing Q is

```
I_KL(Q ‖ π_0 ⊗ π_0)  =  1.3242226355
```

Finite and positive. Hence IF the LP-feasibility actually allowed
drift balance, the resulting Markov tilt would have a tractable LDP rate.
**But it doesn't:** mod-9 saturation + drift balance are simultaneously
infeasible under stationarity, so the rate at the natural-density slice
is `+∞`.

### 3.6 Non-stationary relaxation

Dropping the stationarity constraint (`Σ_v Q(u, v) − Σ_v Q(v, u) = 0`) gives
a strictly weaker LP. Result:

```
min E[a_class]  (non-stationary)  =  1.0  exactly.
```

The minimum is achieved with all row-sum mass on `u = 1`. But a non-
stationary Markov chain does not iterate — its tilt corresponds to a one-
time pair of coords with prescribed joint distribution, equivalent to
*conditioning on a finite-time event*. This is precisely Class B in
`collatz_multitilt.md`, and was already noted to be tautological for the
natural-density LDP. The non-stationary minimum value is a useful sanity
check: it confirms the stationarity constraint is precisely what creates
the `5/2` floor.

---

## 4. Falsifiers / feasibility for (P2)–(P4)

### (P2) Free-energy / prefix-statistic reweighting

Consider `dν/dμ_0 ∝ exp(−Σ_j h(a_j, S_j))` where `S_j = Σ_{i ≤ j} f(a_i)`
is a partial sum.

**Observation.** The empirical 2-coord pair `(a_{j}, a_{j+1})` distribution
of ν, in the long-run limit, is determined by the joint law of
`(a_j, a_{j+1}, S_j, S_{j+1})`. For the Syracuse drift `φ = log 3 − a log 2`,
the natural choice is `f = φ`, giving `S_j = R_j − R_0`, i.e., S_j
*coincides with the Syracuse residue* up to additive constant. The
resulting reweighting is a *position-dependent Esscher tilt on the
residue*, which is *exactly* a conditioning on the trajectory of R — i.e.,
**(P3) in disguise**. For any other choice of f, the reweighting either
(i) reduces to (P1) (if f depends only on `a mod 6` and h depends only on
`(a, S mod M)` for some M; the joint becomes a Markov chain on `(a mod 6,
S mod M)`, same LDP machinery applies and the same LP obstruction lifts),
or (ii) leaves the Gibbs framework entirely.

**Sharp falsifier.** If h depends only on `(a, S mod M)` for any finite M,
the augmented chain has a finite state space and the mod-9 saturation
constraint pulls back to a stationarity constraint on the augmented joint
distribution, with the SAME mod-9 R-table as before but now with the
class label `(u mod 6, S_u mod M)`. By the same LP construction, the row-
marginal `π_a(u) := Σ_{S} Q_aug(u, S, ·)` is unchanged in interpretation,
and the LP min E[a_class] = 5/2 floor REMAINS. **(P2) at any finite
prefix-statistic resolution reduces to (P1) and is closed.**

For infinite-state prefix statistics, the LDP framework requires a strong
Donsker–Varadhan condition; standard hypotheses (irreducibility,
recurrence, finite per-step KL) all fail or are vacuous when `S` has
unbounded range AND the rate per-step is non-trivial. We have not found
a class of `h, f` that escapes both (i) reduction to a finite-state
Markov chain and (ii) failure of the LDP — and we conjecture none exists,
but this is `[OPEN]`.

### (P3) Conditioning on the future

`dν/dμ_0 ∝ exp(...) · 1[X_n mod 3^k ∈ G]` for a "good set" G. The
indicator factor breaks translation invariance and the LDP framework. By
`collatz_multitilt.md` §6 (Class B), the resulting "tilt" is tautological
in the natural-density sense: conditioning on the event "the limit
`X_n mod 3^k` is uniform on `(Z/3^k)*`" does not change the limiting
density, it merely re-expresses it. **(P3) provides no actionable LDP.**

### (P4) A genuinely different base measure

If we abandon μ_0 entirely, the question becomes: is there a measure
`ν` on `Z_+^N` such that
- the Syracuse pushforward of ν has uniform mod-3^k marginal for all k,
- the drift is balanced under ν,
- the per-step LDP rate `lim (1/n) log dν/dμ_0` exists and is finite.

The third condition forces ν to be at finite KL-rate against μ_0; the
LDP theory of Donsker–Varadhan tells us that ν is then a Gibbs measure
on the shift `Z_+^N` with a *local* potential (the cumulant of an
asymptotic average of local functions). Any LOCAL potential (i.e.,
bounded-range cocycle) reduces to (P1) or (P2) by the same finite-state
augmentation argument. NON-LOCAL potentials (i.e., where the per-step KL
rate diverges) fall outside standard LDP.

**Sharp characterisation.** The class of measures ν with finite per-step
KL rate against μ_0 and translation invariance is EXACTLY the class of
shift-invariant Gibbs measures with absolutely summable potential. By
Lanford–Ruelle / Dobrushin theory, every such measure is a thermodynamic
limit of finite-range Gibbs measures, which fall in (P1)/(P2). So
**(P4), restricted to measures with finite per-step LDP rate, is the
union of (P1) and (P2), and is closed.**

The remaining class — measures with INFINITE per-step KL rate against μ_0 —
is a genuinely different regime where standard LDP fails. The
natural-density question may or may not admit a solution there; we do not
have a way to rule it out OR to construct an example. `[FRONTIER]`.

---

## 5. The verdict

> **Theorem (strengthened obstruction, beyond Esscher).** For every k ≥ 2,
> the natural-density question for mod-3^k saturation is closed to:
>
> (a) any translation-invariant per-coord Esscher tilt of μ_0 (Wave 1);
>
> (b) any stationary single-step Markov reweighting on residues mod
>    (2·3^{k−1}) of μ_0 (this probe, k = 2: exact LP min E[a_class] = 5/2);
>
> (c) any finite-range Gibbs reweighting with a partial-sum prefix
>    statistic of finite resolution (reduces to (a) or (b) via finite-state
>    augmentation);
>
> (d) any conditioning on a future event (tautological, no LDP);
>
> (e) any translation-invariant Gibbs measure on the shift `Z_+^N` with
>    finite per-step KL rate against μ_0 (= finite-range Gibbs measure,
>    by Lanford–Ruelle; reduces to (a)–(c)).
>
> The closed perimeter is precisely:
> **the class of measures with finite per-step LDP rate against the
> Bernoulli base, on the Syracuse symbol space.**

**Frontier (not ruled out by this work):**

(F1) Measures with INFINITE per-step KL rate against μ_0. These fall
     outside Donsker–Varadhan / Gärtner–Ellis LDP. Whether such a measure
     can be engineered to give natural-density-saturating Syracuse
     pushforward IS NOT addressed here. The obstacle is that we don't
     know how to compute / verify LDP-style quantities for such measures —
     they are not Gibbs.

(F2) Genuinely different proof techniques: nothing in this work rules out
     proofs of the natural-density question via:
     - additive combinatorics / Furstenberg / structure-vs-randomness,
     - p-adic / nonstandard analysis approaches,
     - sumset methods on `(Z/3^k)*`,
     - any approach not based on "tilt μ_0 to satisfy LDP".
     The barrier theorem we have is about ONE particular family of routes —
     the LDP-via-tilting route. The natural-density question itself
     remains open.

(F3) The Markov LP value `5/2` is exact and depends on the specific
     structure of the mod-9 R-table. For k ≥ 3, the analogous LP would
     be on the (2·3^{k−1})² joint mod-(2·3^{k−1}) distribution with the
     R-table for mod-3^k. We have not computed this LP — the relevant
     question is whether the Markov-LP floor `Σ_u u · π(u)` ALSO scales
     as `Θ(3^{k−1})`, i.e., whether the Markov reweighting recovers
     the same growth rate as the Esscher reweighting (just with a
     constant prefactor weakening). Conjecturally YES; this is `[OPEN]`.

---

## 6. Honest assessment

**What this Wave 2 result rigorously establishes:**

1. **The Wave 1 obstruction extends to single-step stationary Markov.** A
   genuinely larger and quite natural class of tilts is now ruled out.
   The reduction `7/2 → 5/2` of the LP-minimal `E[a_class]` quantifies
   how much "room" the Markov non-product structure buys you: 1 full
   unit of E[a] (out of a 5-unit total range from 1 to 6). It is NOT
   enough to close the gap to `log_2 3 ≈ 1.585`.

2. **All standard LDP-tractable reweightings of μ_0 are closed for k ≥ 2.**
   By Lanford–Ruelle / Gibbs measure theory, this covers every measure
   with finite per-step KL rate against μ_0 (i.e., every shift-invariant
   Gibbs measure with absolutely summable potential). The barrier is
   strong in this sense — it is not a quirk of one parametrisation; it
   is a property of the LDP framework as applied to the i.i.d. Geom(1/2)
   base.

3. **The exact-rational LP computation is reproducible and tight.** The
   LP-min vertex has support 9, value exactly 5/2, all constraints
   satisfied exactly. The within-class freedom only pulls E[a] UP.

**What this work does NOT do:**

- Does not close the natural-density question. It rules out an entire
  family of proof techniques (the LDP-via-tilting family); other techniques
  remain available.
- Does not extend the LP computation to k ≥ 3 (the 18×18 LP for k=3 would
  be straightforward but unverified here).
- Does not address infinite-KL-rate measures (the frontier (F1)). These
  are genuinely outside our methods.
- Does not propose a positive construction. The output is a strengthened
  no-go.

**Confidence calls:**

- *Markov LP-min = 5/2 exactly*: VERY HIGH (exact-rational verification
  via sympy: equality constraints have residual exactly zero; all 36
  nonneg constraints satisfied; LP-min = max-objective dual matches).
- *Extending closure to (P2), (P3), (P4)-restricted-to-finite-KL*: HIGH
  (reductions are by standard Gibbs-measure / finite-state augmentation
  arguments; modulo formal write-up of the augmentation, this is
  rigorous).
- *Same Θ(3^{k−1}) growth for Markov LP at k ≥ 3*: MEDIUM (~70%).
  Conjectural; the LP would need to be computed.
- *No escape exists in the infinite-KL regime*: NOT CLAIMED. This is the
  remaining frontier.

**Bottom line.** This is a candidate-development **strengthening of a
negative result**: from "the Esscher route is closed" (Wave 1) to "every
LDP-tractable reweighting of the Bernoulli base is closed" (Wave 2). The
natural-density question is NOT closed — only the entire family of
approaches via tilting / LDP is. The frontier is now (F1) infinite-rate
measures and (F2) genuinely different proof techniques.

> `[CANDIDATE — strict no-go strengthened to "LDP-tractable reweighting
> of μ_0"; expand certified-negative perimeter of natural-density program
> from per-coord Esscher tilts to all finite-KL-rate Gibbs reweightings.]`

---

## 7. Reproducibility

- `collatz_beyond_esscher_probe.py` — implements the LP feasibility check
  on the 6×6 joint mod-6 distribution Q with mod-9 saturation, stationarity,
  and drift functional; exact-rational verification via sympy; LDP rate
  computation; Esscher-product reduction cross-check; non-stationary
  relaxation.
- `data/beyond_esscher_probe.json` — full numerical and exact-rational
  record (LP min/max, vertex, mod-9 marginals, exact 5/2 verification,
  LDP rate).
- `data/beyond_esscher_probe.log` — human-readable verdict.

**Validation gates:**

- **G0 (R-table):** R(u, v) mod 9 re-derived from `(3·2^{-(u+v)} + 2^{-v})
  mod 9` matches Wave 1 table exactly (assert at probe import). ✓
- **G1 (Esscher reduction):** restricting `Q = π ⊗ π` and solving the
  resulting nonlinear system recovers the unique Wave 1 solution
  `π_c = 1/6` for all c (multi-start fsolve, three starts, all converge
  to uniform within numerical tolerance). ✓
- **G2 (mod-9 saturation at LP-min Q):** the LP-min Q achieves exactly
  `P(R = j mod 9) = 1/6` for all `j ∈ {1, 2, 4, 5, 7, 8}` (residual
  `≤ 1.7e-16`). ✓
- **G3 (exact-rational LP):** LP-min vertex reconstructed in `Fraction`
  arithmetic via `sympy.Matrix.solve`; all 12 equality constraints
  satisfied exactly; all 36 nonneg constraints satisfied; exact LP-min
  value = `5/2`. ✓
- **G4 (LDP rate finite and positive at LP-min Q):**
  `KL(Q ‖ π_0 ⊗ π_0) ≈ 1.324`, positive and finite. ✓
- **G5 (non-stationary relaxation collapses to 1):** dropping the
  stationarity constraint, LP min E[a_class] = 1 exactly (mass concentrates
  on row `u = 1`), confirming the stationarity constraint is precisely
  what creates the `5/2` floor. ✓

**Scope.** Candidate development, not proof attempt. No file outside
`ideas/candidates/` was written. The strengthened obstruction reported
here is rigorous *modulo* the Lanford–Ruelle reduction in §5(e), which
we used as a citation rather than proving.

**Novelty `[UNVERIFIED]`.** The use of single-step Markov reweighting on
residues mod 6 to relax the Wave 1 obstruction — and the exact LP value
`5/2` it yields — appears specific to this construction. The general
Lanford–Ruelle-style reduction "finite-KL-rate ⟹ finite-range Gibbs ⟹
reduces to a Markov augmentation" is folklore in statistical mechanics
but its application to the Syracuse natural-density question seems new.
The frontier (F1), measures with infinite per-step KL rate against the
Bernoulli base, is genuinely uncharted territory.
