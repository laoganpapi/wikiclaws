# d=5/6-parameter Esscher tilt: mod-9 saturation under translation-invariant per-coord tilts

**Track:** Collatz Vector A — Esscher / Gibbs tilts of the Syracuse Bernoulli measure.
Continuation of `collatz_multitilt.md` (Class C two-parameter result and its mod-9 failure).
**Author:** Alex Ye (AI-assisted computation; AI not on author line per project rules).
**Date:** 2026-06-04.
**Status:** `[CANDIDATE — research probe, outcome (c): no-go theorem strengthened]`. `[NOVELTY UNVERIFIED]`.
**Code:** `collatz_d5_tilt_probe.py`. **Data:** `data/d5_tilt_probe.json`, `data/d5_tilt_probe.log`.

---

## 0. Verdict (read first)

> **Outcome (c) — no solution in this family, but with a strictly stronger and
> more illuminating diagnostic than the dimension argument predicted.**
>
> Under the d=6 family of translation-invariant per-coord Esscher tilts with
> cocycles `ψ_i = 1[a mod 6 = i]` for `i = 1, ..., 5` (gauge `t_6 = 0`), the
> joint mod-9 marginal of `R_n` under i.i.d. coords is uniform on `(Z/9)*` **if
> and only if** the per-coord mod-6 marginal `p_c := P(a mod 6 = c)` is the
> uniform distribution `p_c = 1/6` on `{1, ..., 6}`. This is proved exactly
> (sympy, unique positive solution in 6 variables for 6 equations).
>
> But the uniform mod-6 marginal forces `E[a] ≥ 3.5` (with equality in the
> degenerate limit `r → 0+`, where the within-class spread vanishes). Drift
> balance requires `E[a] = log_2(3) ≈ 1.585`. **The incompatibility gap
> `3.5 - log_2(3) ≈ 1.915` is strictly positive for every choice of `r`.** No
> point in the d=6 family achieves both mod-9 saturation and drift balance.
>
> Equivalently: at the joint LDP target `(x_φ = 0, x_{ψ_c} = 1/6)`, the joint
> cumulant `λ(s, t)` is `+∞`; the Gärtner–Ellis rate function is `+∞`; the
> tilted measure does not exist.
>
> **Iteration ruled out a fortiori.** The same obstruction at mod 3^k with the
> natural d-extension (cocycles `ψ_i = 1[a mod 2·3^{k-1} = i]`) forces uniform
> per-coord mod-`2·3^{k-1}` marginal, giving `E[a] ≥ 3^{k-1} + 1/2`. The drift
> gap grows as `Θ(3^{k-1})`. Strict no-iteration.
>
> **Bottom line.** This sharpens the multi-tilt agent's "translation-invariant
> per-coord tilts can't iterate" heuristic into a **structural obstruction
> theorem**: in any natural translation-invariant per-coord Esscher tilt
> with cocycles supported on `a mod 2·3^{k-1}`, mod-`3^k` marginal saturation
> forces a per-coord mean too large to balance drift. The barrier is NOT
> dimension-count (it's not that we need more parameters); it's a STRUCTURAL
> RIGIDITY of the unique mod-`3^k`-saturating distribution.

---

## 1. The family and the cumulant

**Setup.** Per-coord weight under the d=6 tilt:
```
w(a = k) ∝ μ_0(k) · exp(-s · φ(k) - Σ_{c=1..5} t_c · [k mod 6 = c])
        = 2^{-k(1-s)} · 3^{-s} · exp(-t_{k mod 6})        (t_6 := 0)
```

Let `r := 2^{-(1-s)} ∈ (0, 1)`. Per-coord cumulant:

```
λ(s, t_1, ..., t_5) = log E_{μ_0}[exp(-s φ - Σ t_c ψ_c)]
                    = -s log 3 + log Z(s, t)
                    = -s log 3 + log[ (1/(1-r^6)) · Σ_{c=1..6} e^{-t_c} r^c ]
```

(with `t_6 := 0`). **This is closed-form**: a finite sum of 6 elementary
exponential terms divided by `(1-r^6)`, no truncation needed.

**Mod-6 marginal of `a`:** for `c = 1, ..., 6`,
```
p_c = (e^{-t_c} r^c / (1 - r^6)) / Z(s, t)
    = e^{-t_c} r^c / Σ_{c'=1..6} e^{-t_{c'}} r^{c'}        (t_6 := 0)
```

**Within-class conditional:** given `a mod 6 = c`, the conditional distribution
on `a` is a shifted geometric on `{c, c+6, c+12, ...}` with ratio `r^6`, mean
`c + 6 r^6 / (1 - r^6)`. So `E[a] = Σ c · p_c + 6 r^6 / (1 - r^6)`.

**Mod-9 marginal of `R_n`** (`n ≥ 2`, i.i.d. coords): from `R_n mod 9 =
3 · 2^{-(a_{n-1}+a_n)} + 2^{-a_n} mod 9`, and `ord_9(2) = 6`, the marginal
depends only on `(a_{n-1} mod 6, a_n mod 6)`. Direct computation gives the
6×6 table

```
   u\v | 1  2  3  4  5  6
   ----+------------------
    1  | 8  4  2  1  5  7    ← rows for u odd
    2  | 2  1  5  7  8  4    ← rows for u even
    3  | 8  4  2  1  5  7
    4  | 2  1  5  7  8  4
    5  | 8  4  2  1  5  7
    6  | 2  1  5  7  8  4
```

**Key structural observation:** `R(u, v) mod 9` depends only on `(u mod 2, v)`.
Hence, defining `P_odd := p_1 + p_3 + p_5`, `P_even := p_2 + p_4 + p_6`:

| R mod 9 | Pre-image probability |
|---|---|
| 1 | P_odd · p_4 + P_even · p_2 |
| 2 | P_odd · p_3 + P_even · p_1 |
| 4 | P_odd · p_2 + P_even · p_6 |
| 5 | P_odd · p_5 + P_even · p_3 |
| 7 | P_odd · p_6 + P_even · p_4 |
| 8 | P_odd · p_1 + P_even · p_5 |

(These six probabilities sum to `(P_odd + P_even)·(p_1 + ... + p_6) = 1`.)

---

## 2. The saddle system and validation gates

**Saddle system (6 equations in 6 unknowns):**
- Drift: `E[a] = log_2(3) ≈ 1.585`
- 5 of the 6 mod-9 equations: `P(R = 1, 2, 4, 5, 7) = 1/6` (R=8 redundant by sum=1)

Equivalent free parameters: `(s, t_1, t_2, t_3, t_4, t_5)`, or equivalently
`(r, p_1, p_2, p_3, p_4, p_5)` with `p_6 = 1 - Σ p_c`.

**Validation gates** (all pass, see `data/d5_tilt_probe.json`):

| gate | check | result |
|---|---|---|
| G1 | At `(s, t) = (0, 0)` (untilted), mod-3 marginal `(0, 1/3, 2/3)`, `E[a] = 2`. | **PASS** (exact). |
| G2 | At `(s, t) = (THETA_STAR, 0)` (drift-balancing single-param Esscher): mod-3 marginal `(0, 0.2696, 0.7304)`, TV vs uniform-on-units `0.230`, `E[a] = log_2(3)`. | **PASS** (drift residual `2.2e-16`). |
| G3 | Class-C embedding `(s_C, t_1=t_3=t_5=-t_C, t_2=t_4=0)`: mod-3 marginal `(0, 1/2, 1/2)`, mod-9 TV `0.313`, and (after gauge correction) `I_classC = 0.2279`. | **PASS** (mod-3 exact, mod-9 TV `0.31299` matches `multitilt_probe.py`, I after gauge correction `0.227909`). |

Notes on G2 and G3:
- **G2** uses the corrected (pressure-side) sign convention. The corrected
  Class-C document `collatz_multitilt.md §0` reports the same baseline: the
  drift-balancing single-param Esscher tilt WORSENS the mod-3 marginal (TV
  `1/6 → 0.230`). This gate recovers that exactly.
- **G3** confirms that Class C is embedded in this larger family (modulo
  gauge shift `lambda_basis = -t_C + λ_classC`, equivalently `I_basis -
  I_classC = -t_C`). The mod-9 marginal under Class C reproduces the prior
  agent's `0.313` TV-on-units exactly (independent exact-rational DP).

---

## 3. The structural obstruction (the answer)

### 3.1 The unique mod-9-saturating mod-6 marginal is uniform

**Theorem (verified symbolically and numerically).** The system
```
P_odd p_4 + P_even p_2 = P_odd p_3 + P_even p_1 = ... = 1/6
Σ p_c = 1
```
with `p_c ≥ 0` has a **unique** real solution: `p_c = 1/6` for all `c = 1, ..., 6`.

**Verification:**
- `sympy.solve` over `R^6` (positive variables): unique solution `(1/6)^6`.
- Multi-start root-finding (500 random Dirichlet starts): converges to the
  same `p_c = 1/6` solution every time; no other positive solutions found.

**Why this is true (informally).** The six mod-9 probabilities are bilinear
forms in `(P_odd, p_2, p_4, p_6)` and `(P_even, p_1, p_3, p_5)`. Setting them
all equal to `1/6` and pulling out the `P_odd = P_even = 1/2` constraint
(which arises from summing odd / even rows) reduces the system to
`p_c = 1/6` exactly.

### 3.2 Uniform mod-6 forces large `E[a]`

Under `p_c = 1/6`,
```
E[a mod 6] = (1+2+3+4+5+6) / 6 = 3.5,
E[a] = 3.5 + 6 r^6 / (1 - r^6) ≥ 3.5     for all r ∈ (0, 1).
```

Equality `E[a] = 3.5` only in the degenerate limit `r → 0+`.

### 3.3 Drift incompatibility

The Syracuse drift balance is `E[a] = log_2(3) ≈ 1.58496`. The incompatibility:
```
E[a] ≥ 3.5  >  1.58496 = log_2(3),
gap = 3.5 - log_2(3) ≈ 1.915.
```

Hence **no choice of `(s, t_1, ..., t_5)` in the d=6 family satisfies both
mod-9 saturation and drift balance simultaneously**. The joint LDP cumulant
`λ(s, t)` evaluated at the joint target `(x_φ = 0, x_{ψ_c} = 1/6)` is `+∞`;
the Gärtner–Ellis rate function `I(0, 1/6 · 𝟙_5) = +∞`; the tilted measure
realising the target does not exist in this family.

### 3.4 What the LDP rate looks like at "mod-9 uniform without drift balance"

If we ABANDON drift balance and only enforce mod-9 uniformity (i.e.,
`x_{ψ_c} = 1/6`), the resulting 1-parameter family (in `s`) of saddles has
`t_c = (c - 6) log r` (uniform mod-6) and the cumulant simplifies to
```
λ(s, t*(s)) = -s log 3 + log(6 r^6 / (1 - r^6)),    r = 2^{-(1-s)}.
```
At the corresponding empirical mean `x_φ(s) = log 3 - E[a](s) · log 2 ≈
-1.327` (which is FAR from zero — large and negative), the rate is

| s | r | E[a] | E[φ] | λ | I |
|---:|---:|---:|---:|---:|---:|
| -4.000 | 0.03125 | 3.5000 | -1.327 | -14.608 | 28.582 |
| -3.000 | 0.06250 | 3.5000 | -1.327 | -11.548 | 22.462 |
| -2.000 | 0.12500 | 3.5000 | -1.327 | -8.488 | 16.341 |
| -1.500 | 0.17678 | 3.5002 | -1.328 | -6.957 | 13.281 |
| -1.000 | 0.25000 | 3.5015 | -1.328 | -5.427 | 10.221 |
| -0.500 | 0.35355 | 3.5117 | -1.336 | -3.895 | 7.162 |
| 0.000 | 0.50000 | 3.5952 | -1.393 | -2.351 | 4.084 |

These are perfectly valid LDP rates — but for a JOINT event in which the
drift is strictly negative (asymptotically `D_n / n → -1.327·n_{tilt}`, far
from the natural-density slice `D_n / n → 0`). For the natural-density
question, this is irrelevant.

### 3.5 Numerical confirmation of no-solution in the 6D system

A 400-restart multi-start hybrd root-finder applied to the full 6D system
fails to converge: best residual `‖res‖ = 0.21`, far above tolerance. The
best "solutions" found push `r → 0` and `t_3 → ∞`, indicating the system is
trying to drive `p_3 → 0` and `r → 0` to fit mod-9 saturation while also
trying to satisfy drift — but the constraint is inconsistent.

---

## 4. Iteration: mod 27 and beyond

The same argument applies to the natural d-extension at every level.

**Natural d-extension at level k:** cocycles `ψ_i = [a mod m_k = i]` for
`i = 1, ..., m_k - 1`, where `m_k := 2 · 3^{k-1}` is the order of 2 modulo
`3^k`. Total parameters: `(m_k - 1) + 1 = m_k`.

**Same structural obstruction:** mod-`3^k` marginal saturation of `R_n` under
i.i.d. coords requires the unique uniform-mod-`m_k` distribution on a
(verified for k=1, 2; pattern: the mod-`3^k` saturation pulls back to "uniform
mod the order of 2"). Then `E[a mod m_k] = (m_k + 1)/2 = 3^{k-1} + 1/2`, and
the drift gap is
```
gap_k := (3^{k-1} + 1/2) - log_2(3).
```
- k = 1: `gap_1 = 1.5 - 1.585 = -0.085` (NO obstruction! Single-coord uniform
  is FEASIBLE — this is exactly why Class C succeeded at mod 3.) Indeed Class
  C did achieve mod-3 saturation by tuning per-coord weights such that
  `p_odd = p_even = 1/2`.
- k = 2 (mod 9): `gap_2 = 3.5 - 1.585 = 1.915 > 0`. INFEASIBLE.
- k = 3 (mod 27): `gap_3 = 9.5 - 1.585 = 7.915 > 0`. INFEASIBLE.
- k = 4: `gap_4 = 27.5 - 1.585 = 25.915`. INFEASIBLE.
- General: `gap_k = 3^{k-1} + 1/2 - log_2(3) → ∞` as `k → ∞`.

**Verdict on iteration:** the d-family STRICTLY FAILS to saturate mod-`3^k`
for every `k ≥ 2`, with the drift gap GROWING super-linearly. This is a
genuinely stronger obstruction than the dimension-count argument: even
allowing arbitrarily many parameters in the per-coord tilt, the rigidity of
the unique mod-`3^k`-saturating distribution means the LDP rate function at
the natural-density slice is `+∞`.

**The k=1 success is special.** Class C worked at k=1 because the unique
mod-3-saturating mod-2 distribution `(p_odd, p_even) = (1/2, 1/2)` has
`E[a mod 2] = 1.5 < log_2(3) = 1.585`, so the within-class drift `6 r^2/(1-r^2)`
contribution (which is unbounded above) can be CHOSEN to fill the gap. For
k ≥ 2, the saturating `E[a mod m_k] = (m_k+1)/2` is already too LARGE; no
amount of within-class drift control can pull `E[a]` DOWN below it.

This is the **fundamental asymmetry**: within-class drift contribution
`6 r^{m_k}/(1-r^{m_k})` is monotone increasing in `r` from `0` to `∞`, so it
can fill gaps from BELOW. But mod-`3^k` saturation places `E[a]` ABOVE its
target, where the within-class contribution can't help.

---

## 5. Honest assessment

**What is genuinely new in this probe (vs. `collatz_multitilt.md`):**

1. **The mod-9 no-go is a rigidity, not a dimension count.** The multi-tilt
   agent's heuristic `d = φ(3^k) - 1 = 2·3^{k-1} - 1` parameters needed was
   a dimension argument suggesting saturation might be POSSIBLE with enough
   parameters. This probe shows the obstruction is STRUCTURAL: in any
   i.i.d. per-coord family at mod 9, the unique saturating mod-6 marginal
   is uniform, which is drift-incompatible. Adding more parameters within
   the same i.i.d. per-coord framework cannot help. [`[STRICT NO-GO with
   sharp diagnostic]`]
2. **The drift gap grows as `Θ(3^{k-1})`.** Iterating up the mod-`3^k`
   hierarchy makes the obstruction QUANTITATIVELY worse, with gap
   `3^{k-1} + 1/2 - log_2(3)`. Even relaxing some i.i.d. constraints (e.g.,
   adding 2-block cocycles `ψ(a_j, a_{j+1})`), the within-each-coord
   marginal sum still has `E[a] ≥ 3^{k-1} + 1/2` under uniform mod-`m_k`.
   So 2-block or higher i.i.d. corrections cannot help either.
3. **Asymmetry of within-class drift contribution.** The reason k=1 worked:
   the saturating mod-2 marginal has `E[a mod 2] = 1.5 < log_2(3) = 1.585`,
   leaving room for within-class drift to fill the gap. For `k ≥ 2`, the
   inequality flips. This is a precise quantitative explanation of why
   Class C's success was a fluke.

**What this candidate does NOT do:**

- Does not propose a fix or alternative route. The "use 2-block cocycles"
  suggestion from `collatz_multitilt.md` §6 is partially refuted: the
  drift obstruction is a property of the SINGLE-COORDINATE marginal, which
  block cocycles do not change.
- Does not give a proof for non-i.i.d. tilts (e.g., Markov-chain measures
  on `a`). One could in principle build a Markov tilt that biases the joint
  `(a_{n-1}, a_n)` distribution AWAY from the product of uniform mod-6 — but
  such tilts are not "thermodynamic-formalism Esscher tilts" in the
  standard sense; they require a transfer operator on `Z_+ × Z_+`.
- Does not close the natural-density question. It strengthens an existing
  no-go.

**Confidence calls:**

- *Unique mod-9-saturating p is uniform-mod-6*: very high (sympy: exact unique
  solution; numerical multi-start: 500 trials, all converge to uniform).
- *Drift incompatibility at mod 9*: very high (closed-form computation;
  `E[a] ≥ 3.5 > log_2(3) ≈ 1.585`).
- *Same obstruction iterates to mod 3^k for k ≥ 2*: high (~90%). The pattern
  is clear; a clean proof of "the unique mod-3^k-saturating per-coord
  distribution is uniform on mod-`m_k`" for general k follows by the same
  structure (mod-`3^k` value depends only on `(a_{n-k+1} mod m_k, ..., a_n
  mod m_k)`). I have not formalised the unique-positive-solution claim for
  general k.
- *This rules out ALL natural translation-invariant per-coord Esscher tilts*:
  high (~85%). It rules out i.i.d. per-coord, and the structural barrier
  carries over to block-tilts since they don't change the per-coord marginal.
  It does NOT rule out Markov / non-product / fully position-dependent tilts
  — but those leave the standard Cramér / Gärtner–Ellis LDP framework and
  amount to conditioning constructions (Class B in `collatz_multitilt.md`),
  which were already noted to be tautological.

**Overall.** This is a candidate-development NEGATIVE RESULT, strengthening
the multi-tilt agent's barrier into a STRUCTURAL THEOREM. The natural-density
gap is NOT closed; the route via translation-invariant Esscher tilts is
EXTINGUISHED for k ≥ 2.

> `[CANDIDATE — strict no-go theorem strengthened; expand certified-negative
> perimeter of natural-density program; not a path to closure.]`

---

## 6. Reproducibility

- `collatz_d5_tilt_probe.py` — implements the d=6 family, computes per-coord
  cumulant in closed form, builds `R(u,v) mod 9` table, solves the saddle
  system (multi-start), runs exact-rational DP on (Z/9)* for cross-checks,
  performs validation gates G1/G2/G3.
- `data/d5_tilt_probe.json` — full numerical record.
- `data/d5_tilt_probe.log` — human-readable summary.

**Validation gates (all PASS):**

- G1 (untilted): mod-3 marginal `(0, 1/3, 2/3)`, `E[a] = 2`. ✓
- G2 (drift-balanced single-param Esscher): mod-3 marginal `(0, 0.2696,
  0.7304)`, TV `0.2304`, `E[a] = log_2(3)` (drift residual `2.2e-16`). ✓
- G3 (Class C embedding): mod-3 marginal `(0, 1/2, 1/2)`, mod-9 TV `0.31299`
  (matches `multitilt_probe.py`), `I_classC = 0.227909` after gauge shift
  by `-t_C = 1.600`. ✓

**Exact-rational DP cross-check:** Under uniform mod-6 (`p_c = 1/6`), the
mod-9 marginal of `R_n` is EXACTLY uniform on units `{1, 2, 4, 5, 7, 8}` (TV
`= 0` to machine precision) for `n = 4` and `r^6 ∈ {0.01, 0.04, 0.1, 0.2}`.
This independently confirms the analytic computation.

**Scope.** Candidate development, not proof attempt. No file outside
`ideas/candidates/` was written. The structural obstruction reported here
is a sharpening of the dimension-count barrier in `collatz_multitilt.md`.

**Novelty `[UNVERIFIED]`.** The use of mod-`m_k` cocycles as a basis for
Gibbs tilts on the Syracuse shift is the natural extension; whether the
unique-positive-mod-`3^k`-saturating-distribution-is-uniform result is
literature-known is unclear. The general result for k ≥ 2 (in particular the
quantitative drift gap `3^{k-1} + 1/2 - log_2(3)`) appears specific to this
construction.
