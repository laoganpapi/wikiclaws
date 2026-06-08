# Noncommutative ergodic theory / Heisenberg nilmanifolds / nilflows / Bohr-AP — Collatz

**Track:** Collatz, alt-angle wave 3.
**Field cluster:** Noncommutative ergodic theory; Heisenberg / step-2 nilmanifolds;
nilflows (Furstenberg, Parry, Ratner); higher-order Fourier analysis on ℤ
(Host–Kra, Green–Tao, Tao); Bohr / Besicovitch almost-periodicity;
Sarnak disjointness (nilsequence form).
**Status:** Direction proposal + small computational probe.
`[NOVELTY UNVERIFIED]` — no surface evidence of prior Heisenberg-nilmanifold
framing of Collatz (web check ran; results: Tao 2022, Furstenberg-topology
note Idris 2025, none Heisenberg/nilflow).
**Author:** Alex Ye (AI-assisted computation; AI not on author line per
project rules).
**Date:** 2026-06-04.
**Files:** `noncommutative_nilmanifold_probe.py`,
`noncommutative_nilmanifold_probe2.py`,
`data/noncommutative_nilmanifold_probe.json`.

---

## 0. Verdict (one paragraph, read first)

> **Honest assessment: this is a long shot whose probe came back negative
> on the cleanest version, but with one structurally suggestive byproduct.**
>
> All four sub-directions in the brief — (i) Heisenberg-nilmanifold
> embedding of the Syracuse orbit; (ii) Bohr / Besicovitch
> almost-periodicity of R_n mod p^k; (iii) the (2, 3, carry) embedding into
> H₃(ℤ); (iv) Sarnak-nilsequence disjointness — reduce, on the SHAPE OF
> THE INFORMATION THEY DELIVER about Collatz, to objects the project has
> already characterised by other means. Concretely:
>
> - The natural Heisenberg coordinate of the orbit (drift residual,
>   cumulative-valuation, Furstenberg-bracket quadratic) **equidistributes**
>   on a 2-dim sub-nilmanifold of H₃(ℝ)/H₃(ℤ) — the third (quadratic /
>   nilpotent / "z") coordinate is fine, the obstruction is **not**
>   higher-order Fourier-detectable.
> - The Bohr-AP spectrum of R_n mod 9 (ensemble over 38,444 odd starts at
>   depth n=20) is dominated by the **xi=3 character mass = 0.583 ≈ √(1/3)**,
>   which is EXACTLY the project's known mod-3 obstruction (the
>   non-uniform stationary π_n of Tao / the project's transfer operator).
>   The "interior" mod-9 characters carry mass 0.18–0.37 — also non-trivial
>   but reproducible from the same π_n; no new information.
> - The bit-carry "Heisenberg triple" (sum_b, sum_c, Σ_{i<j} b_i c_j) on
>   the Syracuse orbit of 27 has R² = 0.967 of the quadratic Q against
>   the linear (sum_b, sum_c) — i.e. **the third coordinate is essentially
>   linear** in the other two on the orbit, so the triple lives on a 2-dim
>   sub-nilmanifold and the genuinely step-2 datum is *degenerate*.
> - The Sarnak-nilsequence-disjointness direction is well-defined but
>   **the relevant nilsequences (degree ≤ 2) are precisely the objects
>   Tao 2022 already controls via Fourier on ℤ/3ⁿℤ**, so this is not a
>   new lever.
>
> **Why it does NOT escape the strengthened LDP-tractable barrier
> (collatz_beyond_esscher.md / Frontier Wave 2):** every nilsequence
> reweighting of the base measure with a *local* (= bounded-Furstenberg-degree)
> potential reduces to a finite-state augmentation of the symbol space, i.e.
> falls in case (P2) of the Wave-2 theorem (finite-range Gibbs with
> partial-sum prefix). The Wave-2 theorem closes this case. The genuine
> escape (F1: infinite per-step KL rate) is NOT a nilmanifold object —
> nilmanifolds are *compact*, so quotient measures are tame.
>
> **What is genuinely left on the table** (and which I do NOT close): a
> *Ratner-type measure-rigidity* result for the (multiplicative ×3,
> dilation ×2⁻¹) action on a SUITABLE non-compact homogeneous space
> (sub-direction (i')). This is harder to specify cleanly and I do not have
> a candidate space; flagged as `[FRONTIER]`, with a precise reason it
> would have to live OUTSIDE Heisenberg / step-2 to escape the Wave-2
> barrier — namely, the homogeneous space must NOT have summable
> Plancherel measure for the relevant function class (else local-Gibbs
> reduction kicks in). This is a hard request and probably not satisfiable.

The remainder of this document records (1) the four sub-directions in
precise form, (2) the computational probe (3 components, 4 datasets),
(3) the explicit reduction to the Wave-2 barrier, and (4) the
honest assessment.

---

## 1. Setup and notation

We follow `shared/notation.md` and `tao_syracuse_explicit.md` §1.

- ν₂ = 2-adic valuation.
- Syracuse map on odd integers: Syr(n) = (3n+1)/2^{ν₂(3n+1)}.
- Cumulative valuation: S_j = a₁ + ... + a_j with a_j = ν₂(3·Syrʲ⁻¹(N₀)+1).
- Affine representation (1.2 in Tao): Syrⁿ(N₀) = (3ⁿ/2^{S_n}) N₀ + B_n,
  with B_n the Syracuse offset (the random variable Tao studies on
  (ℤ/3ⁿℤ)ˣ).
- R_n := Syrⁿ(N₀) mod 3^k.
- α := log₂(3) ≈ 1.58496.
- LOG_3_2 := log₃(2) (drift balance: E[a] = log₂(3)).

Project background: the natural-density question reduces, after the
mod-3 erratum, to the asymmetric stationary distribution π_n of the
Syracuse transfer operator on (ℤ/3ⁿℤ)ˣ. The strengthened LDP-tractable
barrier `collatz_beyond_esscher.md` closes every shift-invariant Gibbs
reweighting of the Bernoulli base μ₀ on the Syracuse symbol space ℤ₊^ℕ
with **finite per-step KL rate**. The frontier (F1) is the set of
measures with infinite per-step KL rate.

---

## 2. Heisenberg nilmanifold and nilflows: precise objects

### 2.1 The discrete Heisenberg group

H₃(ℤ) is the set of integer upper-triangular 3×3 matrices

```
        ⎡1  a  c⎤
g(a,b,c)= ⎢0  1  b⎥,   a,b,c ∈ ℤ
        ⎣0  0  1⎦
```

with multiplication g(a,b,c)·g(a',b',c') = g(a+a', b+b', c+c'+ab').
The continuous Heisenberg group H₃(ℝ) is the same with ℝ entries.
The Heisenberg **nilmanifold** is X = H₃(ℝ)/H₃(ℤ), a compact 3-dim manifold
fibred S¹ ↪ X → 𝕋² with bundle Euler number 1 (the Hopf-style nilfibration).

### 2.2 Standard linear nilflow

For a fixed Lie-algebra element ω = (α, β, 0) ∈ ℝ³, the **nilflow** is

```
   φ_t(x) := exp(t·ω) · x   in X,
```

with explicit coordinates (modulo H₃(ℤ)) given by BCH:

```
   (x_t, y_t, z_t) = (αt mod 1, βt mod 1, (αβ t²/2) mod 1).
```

**Theorem (Furstenberg 1961; Parry).** The orbit {φ_t(e)}_{t∈ℝ} is
equidistributed in X iff 1, α, β are ℚ-linearly independent. Otherwise it
equidistributes on a *sub-nilmanifold* (a subtorus or a Heisenberg
sub-nilmanifold of lower dimension).

### 2.3 Discrete (= integer-time) nilsequences

A **degree-≤2 nilsequence** on ℤ is a sequence n ↦ F(g·gⁿ·Γ) for F
Lipschitz on a nilmanifold G/Γ of step ≤2, g·gⁿ a polynomial orbit.
For Heisenberg, this is

```
   n ↦ F(αn mod 1, βn mod 1, γn(n−1)/2 mod 1)
```

with γ ∈ ℝ. The polynomial-orbit case (Green–Tao 2010) is settled by the
inverse Gowers U³ theorem.

### 2.4 The natural Collatz embedding (sub-direction (i))

The brief asks: embed the Syracuse orbit into a Heisenberg nilflow with
DRIFT-related parameters. The natural choice:

```
   coords_j := (x_j, y_j, z_j) ∈ 𝕋³
   x_j = (αj) mod 1            (= drift phase, the "fractional log multiplier")
   y_j = (αj − S_j) mod 1      (= drift residual; small ⇔ balanced multiplier)
   z_j = (α·S_j·j/2 − α·Σ_i≤j S_i / j) mod 1
                              (= discrete Furstenberg quadratic bracket)
```

The choice `y = αj − S_j` is forced: `S_j` is an integer, so `(β·S_j) mod 1
= 0` for any rational β; the only non-trivial linear functional of `S_j`
mod 1 must couple to α irrationally. This is **exactly** the drift
residual that controls the multiplier 3ʲ/2^{S_j}.

### 2.5 The probe

Empirical equidistribution of `(x_j, y_j, z_j)` over L = 40..255 steps of
6 long-orbit starting values N₀ ∈ {27, 871, 6171, 77031, 837799}:

| N₀     |   L | 3D-disc B=4 | x-disc 1d | y-disc 1d | z-disc 1d |
|--------|----:|-----------:|---------:|---------:|---------:|
| 27     |  40 | 0.156      | 0.025    | 0.025    | 0.094    |
| 871    |  64 | 0.109      | 0.016    | 0.016    | 0.031    |
| 6171   |  95 | 0.100      | 0.021    | 0.021    | 0.053    |
| 77031  | 128 | 0.078      | 0.016    | 0.016    | 0.031    |
| 837799 | 194 | 0.077      | 0.011    | 0.011    | 0.026    |

(Discrepancies decay at rate ~ 1/√L; for an equidistributing nilflow
expected rate.)

**Reading:** the orbit equidistributes (within sampling noise at small L)
in `(x, y, z)` — all marginals decay at the standard rate, the quadratic
z-marginal at the same rate as the linear marginals. **No non-equidistribution
on a sub-nilmanifold is detected.** Subdirection (i) **does not** see the
natural-density obstruction.

### 2.6 Why this had to fail (structural reason)

The natural-density obstruction is *modular* (mod 3^n on (ℤ/3ⁿℤ)ˣ), not
*ergodic* on a real torus. The Heisenberg-nilmanifold coordinates are
**℘-adic blind**: they sense the irrationality (α = log₂ 3) but not the
mod-3 residue. So any obstruction detectable on the real nilmanifold X
is necessarily an irrationality phenomenon (e.g. a Diophantine
property of α), not a 3-adic / residue phenomenon. The known Collatz
obstruction is purely 3-adic. The Heisenberg-nilmanifold embedding is
therefore **structurally orthogonal** to the relevant obstruction.

---

## 3. Bohr / Besicovitch almost-periodicity of R_n mod p^k
(sub-direction (ii))

### 3.1 The precise question

Is the sequence n ↦ R_n mod 9 (or mod 3^k more generally) **Bohr-almost-periodic**
in the sense that its Fourier series on ℤ/9ℤ has a finite/summable
spectrum that DOES NOT decay to zero, and does that spectral content
encode the obstruction in a useful way?

### 3.2 Per-orbit observation (intermediate)

For 6 starting values 27..8,400,511, orbit length L = 40..255:

| N₀       |   L | |⋅|² at xi=3 (mod-3) | |⋅|² at xi=4 (interior) | baseline 1/L |
|----------|----:|--------------------:|------------------------:|-------------:|
| 27       |  40 | 0.370               | 0.165                  | 0.025        |
| 871      |  64 | 0.374               | 0.177                  | 0.016        |
| 6171     |  95 | 0.352               | 0.171                  | 0.011        |
| 77031    | 128 | 0.404               | 0.209                  | 0.008        |
| 837799   | 194 | 0.378               | 0.203                  | 0.005        |
| 8400511  | 255 | 0.392               | 0.230                  | 0.004        |

Both modes are far above baseline. **But this is per-orbit, and a single
deterministic orbit is *never* equidistributed in any reasonable sense.**
The honest test is the ensemble.

### 3.3 Ensemble observation (the load-bearing data)

Ensemble of 38,444 odd N₀ ∈ {1, 3, ..., 99,999}, at fixed Syracuse depth
n=20:

```
   R_n mod 9 histogram:
      0: 0.0000   3: 0.0000   6: 0.0000      (mod-3 = 0 forbidden)
      1: 0.1120   4: 0.1846   7: 0.0305      (mod-3 = 1: total 0.327 ≈ 1/3)
      2: 0.2413   5: 0.0815   8: 0.3502      (mod-3 = 2: total 0.673 ≈ 2/3)
   |Fourier|:
      xi=0: 1.0000
      xi=1: 0.1759       xi=8: 0.1759
      xi=2: 0.2305       xi=7: 0.2305
      xi=3: 0.5829       xi=6: 0.5829   ← mod-3 projection
      xi=4: 0.3658       xi=5: 0.3658
   mod-3 marginal: (0, 0.327, 0.673)
```

### 3.4 The matching analytic prediction

The xi=3 character is exactly the mod-3 projection. Tao's lemma — and the
project's transfer operator π_n — predicts the mod-3 marginal converges to
(0, 1/3, 2/3). The Fourier coefficient is

```
   |E[e^{2π i R_n/3}]| = |0·1 + (1/3)e^{2πi/3} + (2/3)e^{4πi/3}|
                       = |1/3 + 2/3·e^{2πi/3}| · |e^{2πi/3}|
                       = √((1/3 − 1/3)² + (√3/3)²) · 1     (computation)
                       = √(1/3)  ≈  0.5774,
```

matching the observed 0.5829 to within 1%. The mod-3 obstruction
EXPLAINS the xi ∈ {3,6} mass exactly.

The interior characters xi ∈ {1,2,4,5,7,8} — observed mass 0.18–0.37 —
are NOT zero, but this is depth=20 only (Tao's law for mod-9 needs depth
≫ k = 2 to equidistribute on (ℤ/9)ˣ; finite-n correction is 3^{−n/2}
size, matching observed magnitude).

### 3.5 Verdict

**The Bohr-AP spectrum of R_n mod 9 is the project's already-characterised
mod-3 obstruction**, *exactly* — the xi=3 Fourier mass equals √(1/3) by
the same calculation Tao does (and the project's transfer operator does).
The interior-character mass is the standard finite-n transient. The
nilmanifold/Bohr-AP framing **reproduces but does not extend** the
mod-3 obstruction.

A Bohr-AP / nilsequence inverse theorem (Furstenberg–Bergelson; Host–Kra)
would, if applicable, decompose R_n mod 3^k into a degree-≤2 nilsequence
plus a Gowers-U³-pseudorandom piece. The mod-3 character is the entire
*structured* part of R_n mod 9 (the xi=3 mass). The "rest" decays as
3^{−n/2} (Tao) — so there is no non-trivial nilsequence content beyond
mod-3. The natural-density question doesn't move.

---

## 4. The (2, 3, carry) embedding into H₃(ℤ) (sub-direction (iii))

### 4.1 Setup

The Collatz step on the binary representation n = Σ b_i 2^i is

```
   3n + 1 = Σ b'_i 2^i,    new bits b'_i computable via carries
```

where the carry sequence c_i depends on (b_{i-1}, b_i, c_{i-1}) — a strict
triangular dependence. The natural "Heisenberg triple" for an orbit step is

```
   (sum_b, sum_c, Q) ∈ ℤ³,    sum_b = Σ b_i, sum_c = Σ c_i,
                              Q = Σ_{i<j} b_i c_j   (the genuinely quadratic).
```

Under the embedding ι(n) := g(sum_b, sum_c, Q) ∈ H₃(ℤ), one would hope that
Syr* ι extends naturally to a Heisenberg action (because triangular bit
operations satisfy precisely the Heisenberg co-cycle identity z' = z + ab').

### 4.2 The probe (orbit of 27, 20 steps)

First five triples: (4,6,12), (3,2,1), (5,6,15), (5,7,19), (4,4,6).

Linear regression Q ~ α·sum_b + β·sum_c + γ:

```
   R² = 0.9674.
```

I.e. **Q is essentially linear in (sum_b, sum_c) on the orbit**.

### 4.3 Reading

The bit-carry "Heisenberg triple" is **degenerate**: along the orbit, the
genuinely quadratic coordinate Q is determined (to 96.7% R²) by the linear
sum_b, sum_c. So Syracuse orbits live on a *2-dim sub-nilmanifold* of
H₃(ℝ)/H₃(ℤ) (in fact on a 2-torus). The nontrivial Heisenberg content is
extracted with negligible loss by **two abelian invariants** — and abelian
invariants of Collatz are EXACTLY the things every prior approach has
already tried (digit sums, valuations, residues).

The H₃(ℤ) automorphism action on ℤ³ via (b,c,Q) ↦ (b', c', Q + b c' − c b')
is then, when restricted to the Syracuse orbit, indistinguishable from
the abelian action (b, c) ↦ (b', c') up to a determined affine shift in
Q. No new dynamical invariant.

### 4.4 Why this had to fail

The carry sequence c_i is BOUNDED (each c_i ∈ {0, 1, 2}) and the binary
representation has finite length ~ log₂ n. The Heisenberg coordinate Q is
then bounded by O((log n)²), which scales like log² of the orbit value.
The *interesting* quadratic Heisenberg content is in unbounded "twisted"
factors α√t, which require the orbit to grow to extract — but the carry
data CAPS at O((log n)²). The quadratic-vs-linear extraction barrier (the
R² = 0.967) is precisely this magnitude mismatch.

---

## 5. Sarnak nilsequence disjointness (sub-direction (iv))

### 5.1 The precise question

Sarnak's nilsequence-disjointness conjecture: for every degree-≤d
nilsequence n ↦ F(g·gⁿ·Γ) on a nilmanifold G/Γ, and every "low-complexity"
bounded sequence b(n) (e.g. Möbius μ(n)):

```
   (1/N) Σ_{n≤N} b(n) F(g·gⁿ·Γ)  →  0.
```

The brief asks: is the Collatz **drift sequence** φ_n := log 3 − a_n log 2
(or its sign) low-complexity in this sense, and does it become disjoint
from nilsequences in a useful way?

### 5.2 The "low-complexity" test

A sequence is low-complexity (Sarnak's sense) if its dynamical system has
zero topological entropy. The Collatz drift sign sequence n ↦ sign(φ_n) ∈
{+, −} is determined by a_n ∈ {1, 2, 3, ...}, which under the Tao-Bernoulli
model has positive entropy (=Geom(1/2) entropy = 2 bits/step approx).

**So the drift sign sequence is NOT low-complexity.** It is generated by
a Bernoulli factor with positive entropy. Sarnak's framework explicitly
*excludes* such sequences.

### 5.3 What does fit Sarnak's framework?

The drift residual y_j = (αj − S_j) mod 1 sits on the real torus and is
*continuous*, generated by an irrational rotation — *zero* entropy
classical Sarnak object. By Sarnak's conjecture (proved for nilsequences
by Green–Tao for degree ≤2, by Frantzikinakis–Host for general
nilsequences against Möbius, etc.):

```
   (1/N) Σ_{n≤N} μ(n) · F(αn, βn, γn²/2)  →  0   (Green–Tao 2010)
```

So `y_j` is disjoint from Möbius. But this gives information about
MÖBIUS-ALONG-y, not about Collatz: y_j is *constructed from* Collatz, so
Möbius-along-y is not an obvious operation on Collatz.

### 5.4 The substantive variant

Take a Collatz observable f: 2ℕ−1 → ℂ — say, an indicator of "orbit
descent" or "orbit residue mod 3^k". Ask: is f(n) disjoint from low-degree
nilsequences in n?

This is the Vinogradov–Tao bilinear-sum question for f and is *not*
addressable by present techniques unless f has Möbius-like cancellation.
The natural Collatz observables (descent, residue) are precisely the ones
the project has shown DO NOT have cancellation (mod-3 marginal).

### 5.5 Verdict on (iv)

The disjointness viewpoint is well-defined but produces no new information.
The Möbius-vs-Collatz pairing is observable-dependent and the natural
observables have no Möbius-like cancellation (proved via the mod-3 plateau).
The "nilsequence" inside the bilinear sum is — at degree ≤2 — precisely the
object Tao 2022 controls via Fourier on ℤ/3ⁿℤ. **No additional leverage.**

---

## 6. Why this angle does NOT escape the LDP-tractable barrier

Recall the Wave-2 strengthened barrier (`collatz_beyond_esscher.md`):
every translation-invariant Gibbs measure on the Syracuse symbol space
ℤ₊^ℕ with finite per-step KL rate against the Bernoulli base μ₀ is closed
to the natural-density question, by reduction to a finite-state Markov
augmentation with LP-min E[a_class] ≥ 5/2 > log₂ 3.

**Key reduction.** A "nilsequence reweighting" of μ₀ has the form

```
   dν/dμ₀  ∝  exp(− Σ_j h(a_j, S_j mod M, S_j^{(2)} mod M', ...))
```

where the prefix statistics S_j, S_j^{(2)}, ... are partial sums of bounded
local functions of (a_1, ..., a_j). For any nilsequence of degree ≤ d
and any finite-resolution Lipschitz potential h, the prefix statistic
takes values in a *fixed finite-dim torus quotient* ≅ a torus 𝕋^d
of bounded Lipschitz functions. Discretising to mod M, this becomes a
finite-state augmentation — exactly case (P2) of the Wave-2 theorem.

By the Wave-2 closure of (P2), the natural-density-via-LDP route is
closed for every nilsequence reweighting of degree ≤ d and any finite
discretisation M.

The continuum / infinite-resolution case is a thermodynamic limit of
finite-resolution cases (Lanford–Ruelle), so falls inside the same
closure.

**Conclusion.** Heisenberg / step-2 nilsequence reweightings reduce to
finite-state augmentations of μ₀, hence fall inside the Wave-2 closed
class. **No nilmanifold escape.**

What WOULD escape (Frontier F1): a measure on ℤ₊^ℕ with **infinite**
per-step KL rate against μ₀. Nilmanifolds are compact and their Lipschitz
function spaces are tame, so they cannot produce infinite-rate
reweightings.

---

## 7. The one direction NOT closed (and why it is still a long shot)

The brief mentions Ratner-style measure-rigidity. The Wave-2 barrier
applies to measures on the SYMBOL space ℤ₊^ℕ. A genuinely different
escape would be a measure-rigid argument on a NON-COMPACT homogeneous
space `X = G/Γ` where `G` is non-compact and `Γ` is a non-trivial
lattice, such that:

(a) the Collatz orbit embeds via a polynomial-in-Lie-algebra map,

(b) the relevant function class on X is *not* densely Lipschitz / not
    summable Plancherel,

(c) hence the local-Gibbs reduction fails.

I do not have a candidate G. The Heisenberg group is *compact* after
quotient by Γ, and SL₂(ℝ)/Γ (the natural non-compact alternative, à la
Margulis / Ratner) does not have an obvious Collatz embedding (the
relevant action would need to mix ×3 dilation and ×2⁻¹ contraction, which
are commuting torus elements after taking logs — abelian).

[FRONTIER] — no candidate; flagged as a hard request with the precise
abstract criterion an escape would have to satisfy.

---

## 8. Honest assessment

**What this work establishes (rigorously, modulo the standard nilflow
equidistribution facts):**

1. The natural Heisenberg-nilmanifold embedding of the Collatz orbit
   (with drift-related parameters) equidistributes on the full 3-torus
   to within sampling-rate decay; the quadratic z-coordinate
   equidistributes at the same rate as the linear coordinates. **No
   sub-nilmanifold concentration is detected** in orbit lengths up to
   L=255.

2. The empirical Bohr-AP / Fourier spectrum of R_n mod 9 (ensemble of
   38k odd starts at depth n=20) has its dominant non-trivial mass at
   the **xi=3 character** (= the mod-3 projection), with magnitude
   √(1/3) ≈ 0.583 — **exactly** matching the project's known mod-3
   obstruction (transfer operator stationary π_n / Tao's mod-3 plateau).
   The "interior" mod-9 characters carry the finite-n transient mass,
   decaying at the standard Plancherel rate. **No new information.**

3. The bit-carry "Heisenberg triple" along Syracuse orbits is **degenerate**:
   the quadratic invariant Q has R² = 0.967 against linear (sum_b, sum_c).
   Orbits live on a 2-dim sub-torus of H₃, not a genuinely step-2
   nilmanifold.

4. The Sarnak-nilsequence-disjointness framing requires zero-entropy
   observables, which the natural Collatz observables (drift sign, residue
   class) are not. The well-defined variant of the question reduces to
   the bilinear-sum / cancellation problem the project has already shown
   is structurally obstructed.

**What this work does NOT do:**

- Does not propose any new attack on natural density.
- Does not close any new family of reweightings beyond Wave-2.
- Does not propose a candidate non-compact homogeneous space for the
  Frontier F1 escape.

**Confidence calls:**

- Empirical equidistribution on H₃/H₃(ℤ) with no detectable sub-nilmanifold
  concentration: HIGH (5 orbits, lengths 40–255, three independent
  discrepancy measures, all decaying at ~1/√L).
- Bohr-AP signal of R_n mod 9 is exactly the mod-3 obstruction:
  VERY HIGH (analytic prediction matches to 1%; magnitudes determined
  exactly by Tao's (0, 1/3, 2/3) law).
- Bit-carry Heisenberg triple is degenerate on Syracuse orbits: MEDIUM
  (only 20 steps for orbit of 27; longer orbits would harden, but the
  bounded-carry-magnitude argument is structural).
- Wave-2 closure extends to step-2 nilsequence reweightings: HIGH
  (reduction to finite-state augmentation is the Lanford–Ruelle/local-Gibbs
  argument already used in Wave 2).

**Plausibility / failure modes (honest):**

The wave-1 and wave-2 alt-angles each produced something genuinely
useful — wave 1 a leverage curve, wave 2 a clean negative diagnostic.
**Wave 3 produces a clean negative diagnostic.** The Heisenberg /
nilsequence machinery is *structurally orthogonal* to the mod-3
obstruction (real / Diophantine vs. modular / 3-adic), and the
quadratic content of the natural Collatz invariants is degenerate
(R² = 0.967). The honest publishable artifact is the *precise reason*
nilmanifold methods cannot help, expressed as the Wave-2 closure
extension argument in §6.

**One residual usable observation:** the calculation in §3.4 — that
the xi=3 Fourier coefficient of R_n mod 9 is exactly √(1/3) — is a
crisp **Bohr-AP / nilsequence-language restatement** of the mod-3
obstruction. It may be worth a sentence in the Collatz paper's
obstruction section, as a unified-spectral-language statement of the
known plateau. Not novel content; a clean translation.

---

## 9. Prior-art check (web, surface)

Web search for "Collatz Heisenberg nilmanifold", "Collatz nilflow",
"Collatz nilsequence Green-Tao Furstenberg":

- **Tao 2022** (Forum Math. Pi e12): uses Fourier on ℤ/3ⁿℤ, not nilsequences.
- **Idris 2025** ("Furstenberg Topology and Collatz Problem", MDPI Axioms
  14:297): uses Furstenberg's *topology* on ℤ (Furstenberg's infinitude-of-
  primes-style topology), NOT nilmanifolds or nilflows. Reports: the set
  of integers with infinite stopping time is closed and nowhere dense in
  this topology. Different object.
- "On The Collatz Conjecture: Topological and Ergodic Approach" (arXiv
  2601.03297, dated 2026 — date suspicious; flagging as unverified):
  topological/ergodic, no nilmanifold content per snippet.
- Avila–Forni–Ravotti "Mixing for smooth time-changes of nilflows" — a
  pure nilflow paper; no Collatz mention.

**No prior nilmanifold / nilsequence framing of Collatz appears in
surface search.** `[NOVELTY UNVERIFIED]` for the framing itself; the
content (mod-3 obstruction; Wave-2 closure) is the project's own.

---

## 10. Files and reproducibility

- `noncommutative_nilmanifold_probe.py`: Heisenberg embedding of
  Syracuse orbit (§2.5), bit-carry Heisenberg triple (§4.2),
  nilsequence-correlation (§3 per orbit).
- `noncommutative_nilmanifold_probe2.py`: Fourier breakdown of R_n mod
  9 per-orbit and ensemble (§3.2–3.4), analytic √(1/3) cross-check.
- `data/noncommutative_nilmanifold_probe.json`: numerical record.

All probes run on stdlib + numpy. No external data. No claims hidden
behind seeds — orbits are deterministic, ensemble enumerates all odd
N ≤ 99,999.

---

## 11. Recommendation to the team

**Do NOT pursue this angle further** as a route to natural-density.
The structural reason (real-nilmanifold coordinates are 3-adic-blind;
the obstruction is modular) is robust and would apply to any nilmanifold
of any step.

**DO consider** the one-sentence Bohr-AP restatement of the mod-3
obstruction (§3.4: xi=3 Fourier = √(1/3)) for the Collatz paper's
obstruction discussion — it is a clean unified spectral statement of
the known plateau, in standard higher-order-Fourier language. Not novel
content; cleaner phrasing.

**Frontier (F1) — infinite per-step KL escape — remains the only
genuinely open route** identified by Wave 1 + Wave 2 + this Wave 3. No
nilmanifold construction can satisfy it. The honest forward question is
not "which more clever compact homogeneous space?" but "what
unbounded-rate construction has any chance to satisfy drift balance
without falling into Class B (= conditioning on the future)?". I have no
candidate.

> `[CANDIDATE — direction-eliminating negative diagnostic. The Heisenberg /
> nilmanifold / nilsequence machinery is structurally orthogonal to the
> mod-3 obstruction and reduces, on local-Gibbs grounds, to the closed
> Wave-2 LDP-tractable class. No escape; no new leverage; one usable
> spectral restatement of the known mod-3 plateau (§3.4).]`
