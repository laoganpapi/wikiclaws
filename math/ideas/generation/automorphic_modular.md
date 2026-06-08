# Collatz: Modular Forms / Automorphic L-functions for the (2,3)-Coincidence

> **Alt-Angle Explorer brief.** A genuinely fresh angle *not* in any of the
> ~13 fields previously tried (SOS/Lasserre, commutative algebra, poset
> topology, representation theory, ergodic/Jordan/joinings, higher-order
> additive/Gowers, matroid/tropical, non-moment probability, p-adic/heights/
> Berkovich, logic/model theory, category/sheaf, spectral graph/HDX,
> thermodynamic/LDP).
>
> **Author:** Alex Ye (no AI on author line).
> **Status:** direction proposal + small sensitivity probe. Honest "long
> shot." All claims tagged `[NOVELTY UNVERIFIED]`.
> **Files:** `automorphic_probe.py`, `data/automorphic_probe.json`.

---

## 0. One-paragraph thesis

The cycle side of Collatz is *not* rate-limited by a structural obstruction
(no analog of the mod-3 marginal / `π_n` plateau): it is rate-limited by an
**effective transcendence constant** — the leading constant `κ` in the
Laurent–Mignotte–Nesterenko (LMN) bound on linear forms in two logarithms
(`κ = 24.34` for the rational case `D=1`). Hercher's threshold `m^\* = 91`
is set by a *squeeze* in which `κ` enters as a multiplicative knob.

A separate body of mathematics — **Padé-approximation / hypergeometric /
modular-style refinements of irrationality measures of `log 2` and `log 3`
specifically** (Rhin–Viola for `log 2`, Salikhov / Marcovecchio for `log 3`,
Rivoal et al.) — produces sharper *number-specific* bounds for exactly the
two logarithms that appear in Collatz, by methods (hypergeometric integrals,
modular generating series for the auxiliary functions, automorphic-flavored
Padé denominators) that are **distinct from the general LMN machinery**.

Concrete question:

> **Have the number-specific Padé / modular Padé refinements for the pair
> `(log 2, log 3)` been substituted into Hercher's squeeze?** If they
> yield a smaller effective `κ` *in the parameter window relevant to
> Collatz cycles*, the threshold `m^\*` moves immediately, with no new
> theorem needed.

This is sub-direction **(iii)** of the brief, sharpened: not a generic
S-unit-equation improvement, but the **specific-numbers Padé/modular
techniques specialized to `(log 2, log 3)`**, applied to a specific
inequality (Hercher's squeeze). Plausibility 2/5 (probably the constant
doesn't budge enough), but **the probe is cheap, the failure mode is
informative, and the answer is verifiable against a single published
paper**.

---

## 1. The precise object

### 1.1 The cycle-exclusion squeeze (verified against
`collatz/theory/cycle_exclusion_explicit.md`)

For a hypothetical non-trivial Collatz cycle with `K` odd steps, `N = K+S`
total iterations, and `m` circuits / local minima:

```
G(log B)   <   K   <   F(m;  κ)
   ↑                       ↑
Crandall (lower)      LMN two-log (upper)
```

- `G(log B) ≈ q(B)` where `q(B)` is the first continued-fraction
  denominator of `δ = log_2 3` exceeding `B / δ`. With Hercher's
  `B = 1536 · 2^{60} ≈ 1.77 × 10^{18}`, this gives an unconditional
  lower bound on `K`.
- `F(m;κ)` comes from LMN applied to `Λ = K log 3 − N log 2`:
  `−log Λ ≤ κ · D^4 · (log A_1)^2 (log A_2)^2 · (log b')^2 + …`
  with `κ = 24.34`, `D = 1`, `log A_1 = log 3`, `log A_2 = log 2`,
  and `b'` a small log of the cycle parameters. To leading order
  in the cycle window:
  ```
  F(m; κ)  ≈  c_1 · κ · m^2 · (log b')^2
  ```
  (the `m^2` is the geometric "circuit budget" — more circuits give
  more freedom in Λ; see `cycle_exclusion_explicit.md` §3).
- The squeeze closes (no cycle) iff `F(m;κ) ≤ G(log B)`, i.e.
  ```
  m^\*(κ)  ≈  √( G(log B) / (c_1 κ (log b')^2) ).
  ```
- Hercher's result: `m^\*(24.34) = 91`. Improving to `m^\*(κ_new) ≥ 92`
  *would re-prove Hercher's theorem with a different constant*;
  improving to `m^\* ≥ 200, 1000, …` is the next-frontier asymptotic
  question.

### 1.2 The candidate refinement: number-specific Padé / modular bounds

The general LMN bound is *generic* in the algebraic numbers `α_1, α_2`. For
the specific pair `(2, 3)`, *better* lower bounds on `|2^a − 3^b|` are
known from **hypergeometric Padé approximations** (Rhin–Viola, Salikhov,
Marcovecchio, Rivoal). These bounds are typically stated as irrationality
measures `μ(log_2 3)` or `μ(log 3)` and are tightest at the specific
real numbers:

- `μ(log 2) ≤ 3.891310…` (Rukhadze).
- `μ(log 3) ≤ 5.116305…` (Salikhov 2007 / Marcovecchio 2009;
  improvements as recent as 2024). See [Rivoal survey].
- These translate (via Laurent's two-log → one-log specialization /
  Bugeaud's "Estimates" survey machinery) into an effective lower bound
  ```
  |b_1 log 2 + b_2 log 3|  ≥  c · max(b_1, b_2)^{−(μ−1)}
  ```
  with `μ` close to the irrationality measure of `log_2 3`.
- The relevant question is: **is the leading constant `κ_specific`
  obtained from these number-specific bounds smaller than `κ = 24.34`
  in the *parameter window* (`b' ~ 60–100`, `K ~ 10^{18}`) actually
  relevant to Hercher?** This is **NOT** the same as "is the
  irrationality measure smaller" — the parameter-window dependence
  is subtle, and many number-specific bounds give better *asymptotic*
  exponents but worse *leading constants* in the finite window.

> **[NOVELTY UNVERIFIED]** I am not aware of a published paper that
> substitutes the Salikhov/Marcovecchio/Rivoal `log 3` irrationality-
> measure machinery into Hercher's specific squeeze. The
> *cycle_exclusion_explicit.md* §6.2 action item already flags
> "did Hercher use the sharpest available two-log constant?" — this
> proposal sharpens that to "did Hercher use the sharpest **specific
> to (2,3)** constant?", which is a finer question.

---

## 2. The first probe (run; results in `data/automorphic_probe.json`)

### 2.1 Setup

Treat `κ` as a knob in the schematic squeeze `F(m;κ) ≈ c_1 · κ · m^2 ·
(log m + c_2)^2`, calibrated so that `m^\*(κ = 24.34) = 91` (matching
Hercher's published threshold). Then **the relative sensitivity**
`m^\*(κ_new) − 91` is meaningful even if absolute constants are
schematic.

### 2.2 Result table

| κ source                        | κ       | m^\*  | Δm vs Hercher |
|---------------------------------|---------|-------|---------------|
| LMN-1995 (the published κ)      | 24.340  | 91    | 0             |
| Laurent-2008 pessimistic        | 21.500  | 96    | +5            |
| Laurent-2008 optimistic         | 17.900  | 104   | +13           |
| Dream κ = 15                    | 15.000  | 112   | +21           |
| Dream κ = 12                    | 12.000  | 124   | +33           |
| Dream κ = 10                    | 10.000  | 134   | +43           |
| Dream κ = 7                     |  7.000  | 157   | +66           |
| Dream κ = 5                     |  5.000  | 182   | +91           |

**Inverse:** to push `m^\* = 92` (already a one-better result) needs only
`κ ≤ 23.74`, a **2.47 % improvement** over LMN-1995. To push
`m^\* = 200` needs `κ ≤ 4.05`, an **83 %** improvement (out of reach
for any current method).

### 2.3 Reading

- The squeeze is **mildly sensitive** to `κ`. A 26 % improvement in `κ`
  (from 24.34 to 17.9, which is roughly what Laurent's 2008 "II" paper
  attains in *some* parameter windows according to the Bugeaud survey)
  would raise `m^\*` from 91 to ~104 — a publishable but not
  paradigm-shifting improvement.
- The sensitivity is `m^\* ~ 1/√κ`. Doubling `m^\*` to ~180 requires
  quartering `κ` to ~6 — far beyond any plausible improvement.
- **Therefore: the modular/automorphic angle's most plausible payoff
  is ≤ +10–20 cycles beyond Hercher.** It does NOT crack the cycle
  problem; it nibbles the threshold.

---

## 3. Why this escapes the proven structural barriers

The barriers that have killed the previous 13 fields are all on the
**descent side** of Collatz, where the mod-3 marginal `(0, 1/3, 2/3)`,
the `λ^{φ−1}(λ−1)` charpoly, and the LDP plateau live. The cycle side
is *qualitatively different*:

1. **No mod-3 plateau on the cycle side.** A non-trivial cycle is a
   *single* algebraic-number equation `2^N − 3^K = R` with `|R|` controlled
   by the cycle geometry. There is no `π_n` to fight. The obstruction is
   purely Diophantine.

2. **The bottleneck is a numerical constant, not a structural class.**
   Improving Hercher = improving `κ`. There is no "Livšic cocycle" or
   "non-coboundary obstruction" — only the standard Baker-theory question
   "how small can `|2^N − 3^K|` be?" The barriers in the other 13 fields
   simply don't apply to this question.

3. **The (2,3)-specific Padé / modular machinery is genuinely separate
   from LMN.** LMN is a *generic* lower bound for *any* pair of
   multiplicatively independent algebraic numbers; the Rhin–Viola /
   Salikhov machinery is *specific* to integer logarithms and uses
   hypergeometric / modular generating series that don't appear in LMN.
   So "substitute the specific bound into Hercher" is a meaningful,
   under-explored avenue.

4. **The LDP/thermodynamic candidate (current survivor) attacks the
   density side; this attacks the cycle side.** Orthogonal. Even if
   LDP doesn't pan out for density, this could move `m^\*`.

---

## 4. Plausibility, failure modes, honest assessment

### Plausibility: 2 / 5

- Hercher and his predecessors are experts in transcendence theory; the
  prior expectation that they used the sharpest *generic* constant
  (Laurent 2008 vs LMN 1995) is high. The specific Padé/modular bounds
  for `(2, 3)`, however, are **plausibly not in their toolkit** because
  these come from a different research community (Rivoal, Marcovecchio,
  Salikhov — irrationality-measures specialists) and are typically
  packaged as `μ(log 3) ≤ ...` rather than as a "leading two-log constant
  in the rational case."
- Counter-evidence: the brief probe shows even the dream `κ = 12`
  (a ~50 % cut) only gains ~33 cycles. The cycle problem isn't *cracked*
  by anything in this regime.
- This is one of the few angles where a **small, citable, week-of-work
  paper** ("Pushing Hercher to `m^\* ≥ 100` via Salikhov–Marcovecchio
  bounds for `log 3`") is plausible, even if the conjecture stays out
  of reach. That makes it useful at a different level than the other
  failed angles.

### Failure modes (explicit)

1. **Hercher already implicitly used the sharp constant** (most likely).
   Confirming requires fetching the Hercher PDF and reading §3–5; not
   doable from this environment.
2. **The number-specific bounds are tight asymptotically but loose in
   the finite window**. Salikhov's `μ(log 3) ≤ 5.116` is for `q → ∞`;
   the cycle window has `q` on the order of `B ~ 10^{18}`, which is
   "asymptotic" but the implicit constants might be worse than the
   LMN-1995 constants in that window. Without re-deriving the
   *effective* (non-asymptotic) form, one can't tell.
3. **The translation "irrationality measure → two-log constant" loses
   sharpness**. The known machinery (Bugeaud's survey, Laurent's
   specialization) is not loss-free; the most one can hope for is a
   modest improvement of `κ`.
4. **`m^\*` doesn't move enough to matter.** Even a 26 % cut gives only
   `m^\* = 104`, which is a paper but not progress on Collatz.

### Why not 1/5

Because the probe shows the leverage is *concrete and computable*, the
prior-art question is *answerable from one PDF*, and the failure mode
("we checked; Hercher used the sharpest constant; nothing to do") is
itself a definitive resolution of the brief's question. This is better
than the "Livšic-cocycle" failure mode of p-adic-heights, where even
the failure is not crisp.

---

## 5. Honest assessment vs the other 13 fields

| Field                       | Status                | What it produced |
|-----------------------------|-----------------------|------------------|
| SOS / Lasserre              | dead                  | structural obstruction |
| commutative algebra         | dead                  | -                |
| poset topology              | dead                  | -                |
| representation theory       | dead                  | mod-3 plateau    |
| ergodic / Jordan / joinings | dead                  | π_n is permanent |
| higher-order additive       | dead                  | -                |
| matroid / tropical          | dead                  | -                |
| non-moment probability      | dead                  | -                |
| p-adic / Berkovich          | dead (Livšic cocycle) | named obstruction|
| logic / model theory        | dead                  | -                |
| category / sheaf            | dead                  | -                |
| spectral graph / HDX        | dead                  | -                |
| thermodynamic / LDP         | candidate             | density-side     |
| **modular/automorphic (this)** | **probe + plausibility 2/5** | **cycle-side, +10–20 cycles plausible, paradigm-shift not** |

Unique value of this field vs the others:
- It is the **only** angle that attacks the **cycle side** (not density).
- It has a **concrete leverage point** (the constant `κ`) with a known
  numerical sensitivity.
- The **failure mode is fast to confirm** (one PDF, one substitution).
- The **upside is small but real** (a citable improvement of `m^\*`).

This is the right kind of "ALT-ANGLE": not paradigm-shifting, but
*orthogonal* to the proven barriers and *productive* even on failure.

---

## 6. Concrete next steps (if pursued)

1. **Fetch Hercher 2022 PDF** and identify the exact two-log constant
   used (LMN 24.34 vs Laurent-2008-II vs Mignotte's three-log "kit").
2. **Fetch Salikhov 2007 / Marcovecchio 2009 / Rivoal 2024** and extract
   the effective (non-asymptotic) two-log constant for the pair
   `(log 2, log 3)` in the parameter window `(b' ~ 60–100, q ~ 10^{18})`.
3. **Substitute and re-run** Hercher's optimization (his auxiliary
   parameters; not the schematic model here). Confirm or refute
   `m^\*_new > 91`.
4. **(Optional) Sub-direction (ii) on Hecke eigenvalues.** Investigate
   whether the *correspondences* `x ↦ 3x+1` and `x ↦ x/2` admit a
   reading as Hecke operators on a Shimura variety (e.g. the
   Bruhat–Tits tree for `GL_2(ℚ_2)` and `GL_2(ℚ_3)`). This is a
   genuinely different probe than (i)/(iii). I judge plausibility
   1/5 (too much representation-theory ceremony for the question we
   actually need answered), so I did not pursue it here.

---

## 7. Reproduction

```
$ python3 math/ideas/generation/automorphic_probe.py
# Calibration: c1 = 2422.58, c2 = 2.0
# Sanity: m*(κ=24.34) = 91  (matches Hercher)
# κ-sensitivity table:
LMN-1995          24.340   91   +0
Laurent-2008 pess 21.500   96   +5
Laurent-2008 opt  17.900  104  +13
Dream κ=15        15.000  112  +21
Dream κ=12        12.000  124  +33
Dream κ=10        10.000  134  +43
Dream κ=7          7.000  157  +66
Dream κ=5          5.000  182  +91

# Inverse:
target m=92    needs κ ≤ 23.74    ( 2.47% improvement)
target m=100   needs κ ≤ 19.62    (19.41% improvement)
target m=200   needs κ ≤  4.05    (83.36% improvement)
target m=1000  needs κ ≤  0.11    (99.55% improvement)

# m^* ~ 1/√κ
```

Data: `data/automorphic_probe.json`.

---

## 8. Prior-art trail (snippet-search, all `[NOVELTY UNVERIFIED]`)

- Laurent, Mignotte, Nesterenko, J. Number Theory **55** (1995), 285–321 —
  the κ = 24.34 constant. ([Semantic Scholar][LMN])
- Laurent, "Linear forms in two logarithms and interpolation determinants II",
  Acta Arith. **133.4** (2008), 325–348 — sharper κ in some parameter windows.
  ([EUDML][LaurentII])
- Salikhov, irrationality measure of `log 3` — `μ ≤ 5.116…`.
  ([ScienceDirect][Salikhov])
- Hercher, "There are no Collatz-m-Cycles with m ≤ 91", arXiv:2201.00406 —
  the squeeze. ([arXiv][Hercher])
- Rivoal et al. "Convergents and irrationality measures of logarithms" —
  Padé/automorphic style proofs for `log 2`, `log 3`. ([Rivoal][Rivoal])
- Lagarias's connections to modular themes (Lagarias 1985 survey;
  Lagarias's later writings on `c_n` and L-function analogies) — adjacent,
  no direct substitution into Hercher noted in this session's searches.

[LMN]: https://www.semanticscholar.org/paper/Formes-lin%C3%A9aires-en-deux-logarithmes-et-Laurent-Mignotte/c38cde00830c9bcba0219093a4781b9ffc6dac19
[LaurentII]: https://eudml.org/doc/278141
[Salikhov]: https://www.sciencedirect.com/science/article/pii/S0022314X14001218
[Hercher]: https://arxiv.org/abs/2201.00406
[Rivoal]: https://rivoal.perso.math.cnrs.fr/articles/logconvergents.pdf

---

**Final stance.** Modular/automorphic L-function theory does **not**
crack Collatz, and the brief's expectation of "very long shot" is
correct. But it does offer the cleanest available *cycle-side* nibble:
a sub-direction with a concrete leverage point, a small computable
upside (`m^\*` from 91 to ~100–104), and a definitive prior-art check
that resolves the question either way. That is rare enough among the
~13 dead fields to be worth the file.
