# Frankl candidate — degree-4 (Lasserre level-2) SOS over incidence variables

**Author:** Alex Ye (no AI on author line).
**Date:** 2026-06-03.
**Status:** DECIDED — see VERDICT. `[NOVELTY UNVERIFIED]` (Lasserre/SOS for
extremal set theory exists — Raymond–Saunderson–Singh–Thomas, Bachoc–Vallentin,
Gribling–de Laat–Laurent; the Frankl-specific incidence formulation is flagged
new but plausibly folklore).
**Solver:** cvxpy 1.9.1 + SCS 3.2.11 (a real SDP solver). All numbers below come
from that solver unless marked "closed form".
**Code:** `frankl_sos_las2.py` (incidence SDP), `frankl_freqsos.py` (frequency
power-sum companion). Data in `data/las2_results.json`, `data/freqsos_results.json`.
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
  moments ⇒ reproduces the **power-mean barrier `lb_1`**.
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

**(b) mult=1 reproduces the power-mean barrier `lb_1`.**
<!-- FILLED FROM RUN -->

---

## 3. The lb₂ vs lb₁ table (6 lopsided families)

<!-- FILLED FROM RUN -->

---

## 4. VERDICT

<!-- FILLED FROM RUN -->

---

## 5. Honest scope

- Per-family, small `n` (`n≤5`). The real question for a *proof* of Frankl is a
  **uniform degree bound** — whether a fixed Lasserre level proves Frankl for all
  `n`. Nothing here addresses that.
- SCS is numerical; all reported gaps are checked against solver noise (eps=1e-8).
- The ½ ceiling is proven and re-confirmed (cube=½), so any "separation" can only
  mean *reaching* ½ where level-1 fell short — fine, since Frankl IS the `≥½`
  statement.
