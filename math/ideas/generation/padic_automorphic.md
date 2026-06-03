# Collatz: p-adic & Arithmetic-Dynamics Directions (heights, Berkovich, automorphic)

> **Field cluster 9** (PLAN.md): number-theoretic heavy artillery for Collatz.
> **Status:** SPECULATIVE directions, not proofs. Every claim flagged.
> **Author:** Alex Ye (AI-assisted). `[NOVELTY UNVERIFIED]` throughout.
> **Brief:** find a NON-MOMENT / NON-SYMMETRIC lever that escapes the proven
> barrier — the *exact* non-uniform stationary `π_n` of the Syracuse transfer
> operator (mod-3 marginal `(0,1/3,2/3)`; `P_n` charpoly `λ^{φ-1}(λ-1)`,
> nilpotent perp). Moment / averaging / spectral-radius arguments are inert
> (Phase 3–5 verdict). We want an *arithmetic* invariant that is not a
> probabilistic average.
>
> **Companion files read:** `theory/{transfer_operator, natural_density_obstruction,
> cycle_bound_attempt, function_field}.md`; `PROGRESS.md`; `literature/survey.md`.
> **Computations below** run against `collatz/experiments/verifier.py` (the map `T`)
> and the 10^7 baseline; all are reproducible one-liners (recorded in §6).

---

## 0. The one-paragraph thesis

The barrier is a statement about a **measure** (`π_n`) and an **ℓ²/Fourier norm**
(Plancherel on `(ℤ/3ⁿ)ˣ`). Every tool the project has thrown at it — Esscher
tilts, spectral gaps, TV, second moments — lives in that probabilistic/archimedean
category, and they are all flat against `π_n`'s frozen mod-3 marginal. **Heights and
p-adic norms are categorically different objects: they are not averages.** A height
descends *pointwise* (per orbit) or not at all; a p-adic norm *sees* the mod-3 (or
mod-2) coset structure as its primary feature rather than as a contaminating
marginal. The proposal is to replace "show `π_n → uniform` in an archimedean norm"
by "exhibit a **canonical-height / local-height functional** whose **non-negativity +
descent** bounds orbits," where the mod-3 obstruction is *absorbed into the metric*
(a 3-adic place) instead of fought as a distributional defect. There is one concrete,
verified identity (§2) that already realizes the Collatz orbit as a **height
telescoping** with a summable positive defect — exactly the shape of a Call–Silverman
canonical height — and the open problem becomes a *uniform lower bound on a local
height at the place 3*, which is a Diophantine/equidistribution question, not a mixing
question.

---

## 1. Why archimedean moments are inert and p-adic norms might not be

The proven obstruction (`natural_density_obstruction.md` Thm 3.3, `transfer_operator.md`
Prop 3.1): `X_n mod 3 ≡ 2^{-a_n}` is **permanently** `(0,1/3,2/3)`, so
`TV(π_n, U) ≥ 1/6` for every scalar tilt, and `P_n|_V = [[1/3,2/3],[1/3,2/3]]` has
eigenvector `(1/3,2/3)`. In the archimedean `ℓ²` world this is a *defect to be killed*
and it cannot be killed.

**Reframe at the place 3.** Consider the 3-adic absolute value `|·|_3`. The mod-3
marginal `(0,1/3,2/3)` is the statement "`X_n` is a 3-adic unit, and its image in the
residue field `𝔽_3ˣ = {1,2}` is `(1/3,2/3)`." A 3-adic norm does **not** penalize
this — it *expects* units to be non-uniform in any fixed finite quotient unless there
is equidistribution in `ℤ_3ˣ`, and equidistribution in `ℤ_3ˣ` is governed by Haar
measure on a compact group, where the relevant question is *Fourier decay of a measure
against multiplicative characters of `ℤ_3ˣ`*, i.e. a **Mellin/automorphic** question,
not the additive `ℓ²` Plancherel the project has been doing. **Key point:** the
project's `ℓ²` on `(ℤ/3ⁿ)ˣ` uses **additive** characters `e(ξ·/3ⁿ)`; the natural
group structure of the units is **multiplicative**, and `2` is a primitive root mod
`3ⁿ`. Switching from additive to multiplicative harmonics is the single concrete move
a p-adic/automorphic viewpoint forces, and it is *not* a re-skin of the moment barrier
(the barrier theorems are all about additive/symmetric moments).

> **Named anchors.** Bilu equidistribution and Yuan's arithmetic equidistribution of
> small points; Favre–Rivera-Letelier equidistribution of preimages on Berkovich `ℙ¹`;
> Call–Silverman canonical heights; Baker–Rumely potential theory on Berkovich space.
> These are the tools whose *output* is "an orbit/measure equidistributes w.r.t. a
> canonical measure," and whose *norm* is a height (an arithmetic intersection number),
> never a probabilistic moment.

---

## 2. The arithmetic-dynamics object + the verified telescoping (the concrete core)

### 2.1 The height-reconstruction identity (verified, exact)

For an odd `x`, one Syracuse jump is `x ↦ x' = (3x+1)/2^{a}`, `a = ν₂(3x+1)`. Then

```
log x' = log x + log 3 − a·log 2 + δ(x),   δ(x) = log(1 + 1/(3x)) > 0.
```

Telescoping along the full orbit `n₀ → 1` (`S` odd steps, `K = Σ a_j`):

> **Identity H (verified to 1e−14, §6).**
> ```
> log n₀  =  K·log 2  −  S·log 3  −  Σ_{j} δ(x_j),     δ(x_j)=log(1+1/(3x_j)) > 0.
> ```

This is **exactly** the cycle identity `Λ = Σε_j` of `cycle_bound_attempt.md` Thm 3,
but for a *descending* (acyclic) orbit, and it is the skeleton of a **canonical
height**. Read it as an Arakelov/adelic product formula:

- `log n₀ = log|n₀|_∞` is the **archimedean local height**.
- `K·log2 = −Σ log|·|_2` contributions and `S·log3` the place-3 contributions are the
  **non-archimedean local heights** accumulated along the orbit.
- `Σδ(x_j)` is a **convergent, strictly positive** correction (since `δ(x_j) < 1/(3x_j)`
  and the `x_j` are bounded below by `1`, with most large): it is the analog of the
  *local height at the archimedean place of the canonical-height limit* — the piece
  that, in Call–Silverman, is the bounded difference `ĥ − h`.

The Collatz statement "every orbit reaches 1" becomes: **the adelic balance
`K log2 − S log3` overshoots `log n₀` by exactly the summable defect `Σδ`, and `S, K`
are finite.** Non-negativity of `log n₀` plus finiteness of the defect *is* a descent
statement. The open content is uniformity: bound `S` (equivalently the orbit length)
in terms of `n₀` via a *lower bound on the per-step place-3 height*.

### 2.2 The candidate canonical height

Define, formally, for the Syracuse map `Syr` on odd integers, the **Call–Silverman-style
canonical height** as the (conjectural) limit

```
ĥ(n) := lim_{N→∞} [ log |Syr^N(n)|_∞  +  (place-2,3 local corrections) ] ,
```

the regularized archimedean size along the orbit. Identity H says the *increments* of
the naive height `h = log|·|_∞` are `log3 − a log2 + δ`, whose **conditional mean under
Tao's model is `log3 − 2log2 < 0`** (verified mean `−0.276` vs heuristic `−0.288`, §6) —
a *negative average drift*, which is exactly why `ĥ` "wants" to be a descending
height. The barrier is that the drift is only negative *on average* (the `Σδ` is fine;
the `−a log2` term has the `a`-distribution that the whole project studies). **The
arithmetic-dynamics move:** instead of asking for almost-sure negativity (a moment
statement, inert), ask for a **place-3 local height `λ_3`** whose descent is *pointwise*
because `λ_3` is built from `ν₃`-data of `3x+1` rather than from the size.

> **Candidate functional (to test, §4).**
> `H_c(n) := log n  +  c · Λ_3(n)`, where `Λ_3(n)` is a 3-adic local-height term
> measuring how `3x+1` sits 3-adically — e.g. `Λ_3(x) = −log|3x+1|_3 = ν₃(3x+1)·log3`
> (note `ν₃(3x+1)=0` for `x` a unit, so this is *trivial in one step* — the real content
> is the **3-adic distance of the orbit to the cycle `{1,2}`** as a point of Berkovich
> `ℙ¹`, see §3). The honest expectation (§4) is that the naive `Λ_3` is too coarse; the
> point of writing it is to make the search concrete and to locate *which* 3-adic
> invariant is non-trivial.

---

## 3. Berkovich-space framing of the 2-adic Collatz map (idea (b))

Lagarias's conjugacy makes Collatz a shift on `ℤ_2`. The Syracuse map extends to a map
on `ℤ_2` (and the parity-vector map `Q_∞: ℤ_2 → ℤ_2` is a measure-preserving
homeomorphism conjugating `T` to the shift). Two arithmetic-dynamics statements become
available:

1. **Equidistribution of preimages (Favre–Rivera-Letelier).** For a rational map of
   degree `≥ 2` on Berkovich `ℙ¹_{ℂ_p}`, preimages of any non-exceptional point
   equidistribute toward the canonical measure `μ_f`. Collatz is not a single rational
   map, but the **inverse Collatz tree** (preimages of `1`) *is* exactly the object Tao's
   `c_n` (`survey.md` §5.4) counts: `c_n = #{Syracuse preimages of 1 mod 3ⁿ}`. The
   `β=1` heuristic `c_n = 3^{−n+o(n)}` is precisely an **equidistribution-of-preimages**
   statement for the inverse branches on `(ℤ/3ⁿ)ˣ`. The Favre–Rivera-Letelier paradigm
   says: prove that the inverse-branch IFS (the two maps `x ↦ 2x/3`-type branches on the
   3-adic units) has a *unique invariant measure with full support*, and the preimage
   counts follow. **This is a genuinely different target than `π_n → U`:** it is about the
   *forward-invariant measure of the inverse system*, an equilibrium measure, not a
   mixing rate. Equilibrium measures are pinned by a **variational principle** (maximize
   metric entropy − energy), which is where heights enter (Baker–Rumely: the equilibrium
   measure is the one minimizing an Arakelov–Green energy). Energy minimization is **not**
   a symmetric moment.

2. **The 3-adic place is the right base field.** The obstruction lives mod 3, and the
   inverse Syracuse branches are `x ↦ (2^k x − 1)/3` — *division by 3*. On `ℙ¹_{ℂ_3}`
   this is where the dynamics is interesting (3 is the residue characteristic). So the
   Berkovich picture that matters is over `ℂ_3`, **not** `ℂ_2`. The mod-3 marginal
   `(0,1/3,2/3)` is then the residue-field projection of the canonical measure `μ`, and
   the question "is `μ` equidistributed in `ℤ_3ˣ`?" is the right form of `β=1`.

> **Why this dodges the moment barrier.** The barrier (`transfer_operator.md`) is that
> the *additive ℓ² distance of `π_n` to uniform* is forced positive. The equilibrium-
> measure / energy framing never computes that distance: it asks whether `μ` is the
> energy-minimizer, a global variational fact. The `(0,1/3,2/3)` marginal is then a
> *property of the canonical measure*, accepted not fought — precisely the
> "coset-respecting reference measure" that `natural_density_obstruction.md` §5 flagged
> as the open escape route, now given a canonical (Berkovich/Arakelov) identity.

---

## 4. Concrete first step + small validation

**Step 1 — verify Identity H (done, §6).** Confirms the height telescoping is exact and
the defect `Σδ` is small and positive. ✅ residuals `< 4e−14` on `n₀ ∈ {27,…,837799}`.

**Step 2 — test pointwise descent of height candidates on the 10^7 data.** For each
candidate `H_c(n) = log n + c·Λ_3(n)` and the *raw* `ĥ`-increment, measure on real orbit
steps: `P[H_c(T n) ≤ H_c(n)]`, mean drift, and max increase. **Result (§6, 20k orbits):**
the naive 3-adic term `Λ_3 = ν₃(3x+1)·log3` is identically `0` on units ⇒ `H_c ≡ log n`,
which is *not* pointwise descending (odd steps increase it by `log3 − a log2`, positive
whenever `a=1`, i.e. `~50%` of odd steps). **This is the expected negative**: a *single*
local height at one place cannot descend pointwise, exactly because the descent is a
*place-2-vs-place-∞ cancellation that only balances on average*. The validation's job
is to confirm the naive candidate fails and to localize *what must be non-trivial*: a
height that descends must read the **2-adic valuation stream** `(a_j)` — i.e. it must be
a functional of the Lagarias 2-adic coordinate `Q_∞(n) ∈ ℤ_2`, not of `n mod 3^k`.

**Step 3 — the real candidate: a height on the 2-adic coordinate.** Define
`g(n) := log n − ρ · ⟨ a-stream weight ⟩` where the second term is a *bounded* function
of `Q_∞(n)` chosen so that its increment under the shift cancels the `−a log2` term
pointwise. This is the **transfer/cohomological coboundary** question: does the function
`φ(x) = log3 − a(x) log2` (whose Birkhoff average is `<0`) admit a *bounded* solution
`u` to `φ = u∘Syr − u + (negative const)`? If `u` exists and is bounded, `log n + u` is a
genuine Lyapunov height. The 2-adic obstruction to such `u` is a **cohomology class**
(Livšic-type) — a non-moment invariant. **Concrete probe (next session):** compute
empirical coboundary residuals `u_M(n) = Σ_{j<M}(φ(x_j) + |drift|)` along orbits and test
boundedness vs `M`; unboundedness pins the obstruction as a Livšic cocycle, not a mixing
defect. (Listed as the highest-value follow-up; not yet run.)

**Step 4 — multiplicative-harmonics probe of `π_n`.** Recompute the Syracuse-RV Fourier
mass against **multiplicative** characters `χ` of `(ℤ/3ⁿ)ˣ` (Dirichlet/Hecke characters,
the automorphic harmonics) instead of additive `e(ξ·/3ⁿ)`. The barrier theorems are
stated for additive moments; whether `π_n` is closer to uniform in the *multiplicative*
basis is **untested** and is exactly the "does a different norm see it differently"
question the brief poses. Cheap to run on existing `transfer_operator.py` spectra.

---

## 5. Plausibility, failure modes, novelty

**Plausibility: 2 / 5** (honest). Rationale:

- The height-telescoping Identity H is *real and verified*, and recasting Collatz as a
  canonical-height descent is structurally legitimate (it is literally the cycle identity
  generalized). The Berkovich/equilibrium-measure reframing of `β=1` as
  equidistribution-of-preimages is a genuine, named, non-moment target.
- BUT: the verified Step-2 negative shows the *easy* p-adic heights are inert, and the
  live content (Step 3) reduces to a **Livšic-cohomology / coboundary** question that is
  morally equivalent to the open problem itself — heights do not magically supply the
  cancellation; they relocate it to a cohomology class. This is the standard failure mode
  of Lyapunov/height attacks on Collatz (cf. `function_field.md`: over `𝔽_2[T]` the two
  places coincide and a degree-height works; over `ℤ` they decouple and no pointwise
  height exists). The arithmetic-dynamics framing makes the obstruction *named*
  (a non-trivial Livšic cocycle / a non-equidistributed equilibrium measure) but does not
  obviously make it *tractable*.

**Failure modes (explicit):**
1. **The coboundary doesn't exist (most likely).** If `φ = log3 − a log2` is a genuine
   non-coboundary, no bounded height correction exists and Step 3 dead-ends — the
   archimedean/2-adic decoupling of `function_field.md` is exactly this, restated.
2. **Berkovich machinery needs a single rational map.** Favre–Rivera-Letelier is for
   `deg ≥ 2` rational maps; the inverse-Syracuse IFS is a *correspondence*, so one must
   port equidistribution to the IFS/transfer-operator setting (Lyubich/thermodynamic
   formalism on the Berkovich tree) — plausible but real work, and may circle back to the
   same `π_n`.
3. **Multiplicative harmonics may obstruct identically.** The mod-3 marginal could be
   equally bad against `χ` (a single bad character), making Step 4 a quick negative.
4. **Cycle side is rate-limited by Baker (two logs)** regardless — heights don't improve
   the linear-forms-in-logs bound that caps cycle exclusion at `m ≤ 91`
   (`cycle_bound_attempt.md`); this direction is orthogonal to that and claims no help
   there.

**Strongest sub-claim worth pursuing first:** Step 4 (multiplicative/automorphic
harmonics of `π_n`) — cheap, directly tests the brief's "does a p-adic-flavored norm see
`π_n` differently," and is genuinely outside the additive-moment barrier. Then Step 3
(Livšic coboundary of `log3 − a log2` on the 2-adic shift) — the one place a *height*
could in principle supply a pointwise (non-moment) descent, with a clean
boundedness/unboundedness numerical test.

**Novelty: `[NOVELTY UNVERIFIED]`.** Lagarias 2-adic conjugacy (1985) and Berkovich/
arithmetic-dynamics are both standard; their *combination* targeting `c_n` as a
Favre–Rivera-Letelier preimage-equidistribution, and the explicit reading of Identity H
as a Call–Silverman canonical height with the mod-3 obstruction absorbed into the place-3
local height, is — to the best of the (arXiv-403-blocked) check — not written down. The
Livšic-coboundary phrasing of "why no Lyapunov height" is likely folklore-adjacent
(ergodic-theory of the 2-adic shift). Prior-art pass required against: arithmetic
dynamics of `3x+1` (Silverman's book ch. on canonical heights; any Berkovich-Collatz
note), Lagarias 1985 §2-adic, Tao 2020 blog (preimage density). All flagged.

---

## 6. Reproduction log (all run this session against `experiments/verifier.py`)

- **Mean odd-jump drift:** `mean(log x' − log x) = −0.2762` over 20k random odd
  `x ∈ [10^6,10^9]` vs heuristic `log3 − 2log2 = −0.2877`; `mean ν₂(3x+1) = 1.983`
  (heuristic 2). Confirms the height increment is on-average negative (the canonical
  height "wants" to descend) — but only on average.
- **Identity H (height telescoping):** `log n₀ = K log2 − S log3 − Σδ` verified to
  residual `< 4e−14` for `n₀ ∈ {27, 97, 871, 6171, 77031, 837799}` (S up to 195,
  K up to 329). Exact reconstruction of the archimedean height from the place-(2,3)
  valuation stream plus the summable positive defect `Σδ = Σ log(1+1/(3x_j))`.
- **Step-2 negative:** naive 3-adic local height `ν₃(3x+1)·log3 ≡ 0` on units ⇒ no
  pointwise descent; localizes the live content to a functional of the 2-adic
  coordinate (Step 3 Livšic coboundary). Confirmed expected failure.

**Not yet run (next session, with open network for prior-art):** Step 3 coboundary
boundedness test along 10^7 orbits; Step 4 multiplicative-character Fourier mass of
`π_n` from `transfer_operator.py`.
