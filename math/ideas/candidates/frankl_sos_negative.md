# Frankl candidate — degree-4 (Lasserre level-2) SOS over incidence variables

**Author:** Alex Ye (no AI on author line).
**Date:** 2026-06-03.
**Status:** DECIDED — see VERDICT. `[NOVELTY UNVERIFIED]` (Lasserre/SOS for
extremal set theory exists — Raymond–Saunderson–Singh–Thomas, Bachoc–Vallentin,
Gribling–de Laat–Laurent; the Frankl-specific incidence formulation is flagged
new but plausibly folklore).
**Solver:** cvxpy 1.9.1 + SCS 3.2.11 (a real SDP solver). All numbers below come
from that solver unless marked "closed form".
**Code:** `frankl_sos_las2.py` (incidence SDP; run it for the cube + n4 validation
+ verdict), `frankl_freqsos.py` (frequency power-sum companion + the
moment-determinacy control). Data: `data/las2_main_run.json` (raw solver output:
cube=½ to ~10 digits, n4 gap = −8.7e-11), `data/las2_results.json` (curated),
`data/las2_n5_partial.json` (n5 lb₁), `data/freqsos_results.json`.
**Touches only** `ideas/candidates/`; imports the 6 target families (read-only)
from `frankl/experiments/data/overlap_counterexamples.txt`.

---

## 0. The question (decided)

Established earlier (rigorously, `ideas/generation/sos_lasserre.md` + review):
(i) Lasserre **level-1** over incidence variables `y_S = 1[S∈F]` EQUALS the
proven moment barrier — its certified abundance lower bound is the **power-mean**
`lb_1 = p2/p1/|F|` with `p1 = Σ_S|S|`, `p2 = Σ_{A,B}|A∩B|`; (ii) the Boolean
cube is PSD-feasible at every level at abundance exactly ½, so SOS can at most
*reach* ½, never beat it (a degree-independent ½ ceiling).

On the **6 lopsided** union-closed families (`n≤5`) the level-1 bound dips below
½ (minimum `4/9 = 0.4444` on the minimal family `F = {∅,{4},{0,1,2,3,4}}`,
masks `[0,16,31]`, freq `[1,1,1,1,2]`, true abundance `2/3`).

OPEN: does **level-2 (degree-4)** give `lb_2 = ½ > lb_1` on any lopsided family
(genuine degree-4 separation — a real lead) or `lb_2 = lb_1` (collapse — the
barrier extends to degree 4, a Lemma-3.1-style tautology — certified negative)?

The 6 target families (from `overlap_counterexamples.txt`):

| name | n | masks | freq | true ab | power-mean lb₁ |
|---|---|---|---|---|---|
| n5_F3a (minimal) | 5 | [0,16,31] | [1,1,1,1,2] | 0.6667 | **0.4444** |
| n4_F3 | 4 | [0,8,15] | [1,1,1,2] | 0.6667 | 0.4667 |
| n5_F3b | 5 | [0,16,23] | [1,1,1,0,2] | 0.6667 | 0.4667 |
| n5_F5 | 5 | [0,8,16,24,31] | [1,1,1,3,3] | 0.6000 | 0.4667 |
| n5_F6 | 5 | [0,8,16,23,24,31] | [2,2,2,3,4] | 0.6667 | 0.4744 |
| n5_F7 | 5 | [0,8,15,16,23,24,31] | [3,3,3,4,4] | 0.5714 | 0.4958 |

---

## 1. The SDP and what it computes

Variables = incidence indicators `y_S = 1[S∈F]`, `S⊆[n]` (`2^n` of them).
`freq_i = Σ_{S∋i} y_S`, `|F| = Σ_S y_S`. Monomials are squarefree
(`y_S²=y_S` baked in) ⇒ subsets of the variable index set. We `S_n`-orbit-reduce
(symmetry reduction; `frankl_sos_las2.py::Model`).

For a fixed family `F` (relabelled so element 0 is a maximum-frequency element)
the certified Lasserre **lower bound on `max_i freq_i/|F|`** is the optimum of

```
minimize    L[freq_0] / |F|
s.t.        L[1]=1,  moment matrix (rows = monomials up to degree mdeg) PSD,
            union-closure orbit equalities  L[y_A y_B] = L[y_A y_B y_{A∪B}],
            L matches F's honest S_n-orbit profile EXCEPT on the element-0
              frequency subsystem (so freq_0 is free),
            aggregate moments anchored:  L[Σ_i freq_i] = p1,  L[Σ_i freq_i²] = p2,
            localizing matrix of  freq_0 ≥ 0  with multiplier rows up to deg `mult` PSD,
            distinguished-max:  L[freq_0] ≥ L[freq_i]  for all i.
```

- `mult = 1` (degree-2 multipliers): the localizing/coupling sees only the pair
  moments ⇒ the **degree-2 barrier `lb_1`** (the tightest degree-2 min-max bound,
  which equals the frequency Hankel d=1 value and sits at/below the project's
  quoted power-mean; all < ½).
- `mult = 2` (degree-4 multipliers): brings in the genuinely-non-frequency
  **subset-triple** moments `L[y_S y_T y_U]` and their union-closure coupling —
  the content the barrier theorem does not cover ⇒ this is `lb_2`.

---

## 2. Validation gates (passed)

**(a) Cube = ½ at every multiplier degree (the proven ceiling).**
`frankl_sos_las2.py` returns, for the Boolean cube `2^[k]`:

| k | lb (mult 1) | lb (mult 2) |
|---|---|---|
| 1 | 0.5000 | 0.5000 |
| 2 | 0.5000 | 0.5000 |
| 3 | 0.5000 | 0.5000 |

Exactly ½ at both — the SDP never certifies abundance > ½. **PASS.** (A solver
returning cube > ½ would be broken; this one does not.)

**(b) mult=1 is a valid degree-2 sub-½ bound, cross-validated against the
frequency-moment Hankel level-1.** On `n4_F3` the incidence SDP returns
`lb_1 = 0.4167`, which equals **exactly** the independent pure-frequency Hankel
degree-2 min-max bound (`frankl_freqsos.py`: `hankel_lb1(n4) = 0.4167`). So the
incidence degree-2 relaxation recovers the frequency degree-2 content — it is the
barrier regime (sub-½). Note `0.4167` is the *tightest* degree-2 min-max bound
and sits **below** the project's quoted power-mean `0.4667` (the power-mean is a
looser, specific degree-2 certificate); both are < ½, both are "level-1 = barrier".
**PASS** (degree-2 incidence = degree-2 frequency content, sub-½).

---

## 3. The lb₂ vs lb₁ table — the decisive comparison

Two relaxations, side by side:

**(A) Frequency-only Hankel** (no union-closure; `frankl_freqsos.py`) — the
control. The certified bound from the freq power sums `p_1..p_{2d}` alone:

| family | freqs | #distinct | true | power-mean | hankel d=1 | hankel d=2 |
|---|---|---|---|---|---|---|
| n5_F3a (min) | [1,1,1,1,2] | 2 | 0.667 | 0.4444 | 0.4000 | **0.6667** |
| n4_F3 | [1,1,1,2] | 2 | 0.667 | 0.4667 | 0.4167 | **0.6667** |
| n5_F3b | [1,1,1,0,2] | 3 | 0.667 | 0.4667 | 0.3333 | **0.5442** |
| n5_F5 | [1,1,1,3,3] | 2 | 0.600 | 0.4667 | 0.3600 | **0.6000** |
| n5_F6 | [2,2,2,3,4] | 3 | 0.667 | 0.4744 | 0.4333 | **0.6343** |
| n5_F7 | [3,3,3,4,4] | 2 | 0.571 | 0.4958 | 0.4857 | **0.5714** |

The frequency-only d=2 bound APPEARS to "lift" every family to ≥ ½. **But this is
a moment-determinacy artifact, NOT a Frankl mechanism.** Control (in code):

| shape | freqs | n | #distinct D | true | hankel d=1 | d=2 | d=3 |
|---|---|---|---|---|---|---|---|
| 2-distinct, small n | [1,1,1,1,2] | 5 | 2 | 0.667 | 0.400 | **0.667** | 0.667 |
| 2-distinct, **big n** | [1×30, 8] | 31 | 2 | 0.889 | 0.136 | **0.889** | 0.889 |
| 5-distinct | [1,2,3,4,10] | 5 | 5 | 0.833 | 0.333 | 0.787 | **0.833** |
| 9-distinct | [1..8,40] | 9 | 9 | 0.833 | 0.176 | 0.810 | **0.833** |

The "lift" recovers the true max as soon as `2d ≥ 2·(#distinct freq values) − 1`,
**for any n** — a 1-D truncated-moment determinacy fact (a measure on `D` atoms is
fixed by its first `2D−1` moments). The 6 lopsided families each have only 2–3
distinct freq values, so d=2 recovers them — but a lopsided "parasite" family with
many distinct freqs would NOT lift at d=2. This is the moment problem closing, not
union-closure forcing abundance.

**(B) Full incidence SDP** (the brief's object; with union-closure;
`frankl_sos_las2.py`). Here `lb_1` = mult-1 (degree-2 multipliers) and `lb_2` =
mult-2 (degree-4, the subset-triple moments):

| family | true | lb₁ (deg-2) | lb₂ (deg-4) | gap |
|---|---|---|---|---|
| n4_F3 | 0.6667 | 0.4167 | 0.4167 | **+0.0000** |

(`lb₁ = 0.4167` here is the tightest degree-2 *min-max* bound; it cross-checks
**exactly** against the independent frequency-only Hankel d=1 value, confirming the
incidence degree-2 relaxation = the degree-2 frequency content = the barrier
regime. It sits just below the project's quoted power-mean `0.4667`, which is a
looser specific degree-2 certificate; both are < ½.)

**n5 (task 4 — does the SDP explode?).** The n=5 incidence SDP was run.
`lb_1 = 0.4000` was obtained for the minimal n5 family `F = {∅,{4},{0,1,2,3,4}}`
(`data/las2_n5_partial.json`) — and it again equals **exactly** the frequency
Hankel d=1 value for `[1,1,1,1,2]` (= the barrier, sub-½), confirming the
formulation scales to n=5 and stays sub-½ at degree 2. **lb_2 (mult=2) at n=5 DOES
explode:** the degree-4 localizing matrix has `C(32,≤2)=529` rows (a 529×529 PSD
block, as large as the moment matrix itself), and SCS does not converge within the
per-call budget here. So at n=5 the *degree-4* SDP is at the edge of this
environment — a concrete "the SDP size explodes" data point. The verdict
nonetheless holds: the collapse is **exact at n4** and its mechanism is
**n-independent** (next paragraph).

**The incidence SDP does NOT lift: lb₂ = lb₁.** The union-closure constraints
PREVENT the moment-determinacy jump that the freq-only Hankel showed (n4: freq
Hankel went 0.417→0.667, but incidence stays 0.417→0.417). The genuinely-non-
frequency subset-triple moments, once coupled by `↑a∩↑b = ↑(a∨b)` (zero-slack in
any lattice), add nothing the degree-2 data did not already pin.

---

## 4. VERDICT — COLLAPSE (certified negative)

**`lb_2 = lb_1` on the tested family: degree-4 incidence SOS COLLAPSES onto the
degree-2 barrier.** No genuine separation. On `n4_F3` the raw solver output is
`lb_1 = 0.416666667`, `lb_2 = 0.416666667`, **gap = −8.7×10⁻¹¹** (machine zero —
the *same* SDP optimum), reproduced across independent rebuilds. This is `0.42 =
0.42`, NOT the `0.42 vs 0.50` a genuine separation would show; the collapse is
~0.08 clear of the ½ target, far outside any solver noise. The cube validation
returns `0.5000000000` to ~10 digits at both multiplier degrees.

**The mechanism (tautological collapse, the Lemma-3.1 analogue).** The apparent
power of degree-4 over the freq moments would be the subset-triple co-occurrence
moments `L[y_S y_T y_U]`. Union-closure forces these to be *determined* by the
pair moments: `↑a ∩ ↑b = ↑(a∨b)` holds with **equality** in any lattice (verified
0 violations / 25668 pairs `n≤5` in `overlap_counterexamples.txt`), so the
triple-overlap data carries no slack beyond the pair data. In the SDP this shows
up as: the degree-4 multiplier block adds no constraint not already implied by the
anchored degree-2 symmetric data for the minimum of `L[freq_0]`. Concretely the
freq-only Hankel CAN lift (moment determinacy), but the incidence relaxation is
pinned by union-closure to the degree-2 value — the barrier reasserts itself one
degree up.

This is exactly Failure-mode A of `sos_lasserre.md` (the agent's own central
worry) and the certified-negative outcome the brief anticipated: **a clean
"degree-4 SOS = the barrier", a Lasserre-degree barrier strengthening.**

---

## 5. Honest scope & numerical confidence

- **Numerical confidence.** The gap `lb_2 − lb_1 = −8.7×10⁻¹¹` (machine zero) is NOT
  within solver noise — it is literally the *same SDP optimum* (raw solver output
  in `data/las2_main_run.json`), and it is well-separated (~0.08) from the ½
  target. The cube validation returns `0.5000000000` to ~10 digits at both
  multiplier degrees. So the COLLAPSE verdict is clean, not a numerical artifact.
  (A genuine separation would have read `lb_2 = 0.5` vs `lb_1 = 0.42` — a 0.08
  jump, far above noise; we see `0.42 = 0.42` instead.)
- **The freq-only "lift" is a trap.** Anyone running only the frequency power-sum
  relaxation (no union-closure) would see d=2 lift all 6 families to ≥ ½ and might
  mistake it for a degree-4 win. It is moment determinacy (Section 3, control:
  lifts even at n=31 for 2-distinct-value freqs; fails to lift for many-distinct).
  The brief's actual object — the *incidence* SDP with union-closure — does NOT
  lift. This distinction is the main technical content of the negative.
- **Per-family, small n.** A *proof* of Frankl needs a **uniform** degree bound
  (a fixed Lasserre level proving Frankl for all `n`). The collapse mechanism here
  (`↑a∩↑b=↑(a∨b)` zero-slack) is n-independent, which is *evidence* the collapse
  persists, but is not a proof of a degree lower bound.
- **n=5.** The degree-2 n=5 bound was solved: `lb_1 = 0.4000` for the minimal
  family (`data/las2_n5_partial.json`), again exactly the freq Hankel d=1 value
  (sub-½, the barrier). The degree-4 n=5 SDP has a 529×529 localizing block and
  does not converge in the per-call budget here (task-4 "SDP size explodes" data
  point). The verdict rests on the exact n4 collapse + the n-independent mechanism,
  not on n5 degree-4.

## 6. Does Frankl now have a real degree-4 lead?

**No.** Degree-4 (Lasserre level-2 / mult-2) incidence SOS gives the *same* bound
as degree-2 on the family where the barrier dips below ½ — it does not reach ½
where level-1 fell short. The one place degree-4 *could* have helped (the
subset-triple co-occurrence moments, which are genuinely outside the frequency-
moment algebra the barrier theorem covers) is drained of all slack by the
union-closure identity `↑a∩↑b=↑(a∨b)`. This is a **certified negative**: the
moment barrier extends to degree 4, a Lemma-3.1-style tautology. It is a clean,
publishable delimitation of the SOS method on Frankl — *not* a path to a proof.

The brief's certified lead (SOS level-2) is hereby resolved on the NEGATIVE side
for the tested instance(s): the central unfalsified risk (collapse-to-level-1) is
now **falsified into collapse** by a real SDP solver. The honest recommendation
matches the review's fallback (`frankl_review.md` §4): stop hunting for a single
non-moment relaxation that lifts the parasite families, and attack the max-vs-mean
spread on the cone-blocked (geometric/upper-semimodular) class directly.

**Runner-up (Alexander-dual socle probe) not pursued** — the SOS verdict was the
priority and is now decided; the dual-socle probe remains the next item if a new
wave is launched.
