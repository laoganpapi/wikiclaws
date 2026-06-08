# Step-1 verification log — AHS reconstruction and attack vectors

**Author:** Alex Ye (AI assistance disclosed separately)
**Date:** 2 June 2026
**Code:** `frankl/experiments/verify_ahs.py`, `single_letter.py`, `vector_analysis.py`
**Test scope:** all union-closed families on $[n]$ for $n\le 5$ enumerated as **$S_n$-orbit
representatives** (29,327 orbits at $n=5$; all quantities used — entropies, marginals,
abundance, $\Delta_2$ — are isomorphism-invariant, so orbit representatives are a sound and
complete test set for these quantities). Spot checks at $n=6$ (orbit reps; partial, where the
enumerator completes in time). Labeled $n=5$ has 2,771,104 families and is too slow to fully
enumerate (~670 s just to list); orbit reps are the correct and sufficient test set.

All entropies computed **exactly** by summation over the $\le|\mathcal F|^2$ atoms of the joint
law of $(A,B)$, $A,B$ i.i.d. uniform on $\mathcal F$. No Monte Carlo.

---

## Run 1 — AHS proof internals (consistency of every inequality in the reconstruction)

Command: validation block over $n\le4$ orbit reps (412 families).

| Quantity | Value | Required | Status |
|---|---|---|---|
| Lemma 2 grid min $G(u,v)$, mesh 600 + refine | $0.000$ at $(0,0)$, golden pt $\sigma=0.618$ | $\ge0$ | PASS |
| $\max_{\mathcal F}\,[H(A\cup B)-H(A)]$ | $0.00\mathrm e{+}0$ | $\le0$ (union-closure, eq (1.2)) | PASS |
| $\max_{\mathcal F}\,[\text{chainLB}-H(A\cup B)]$ | $4.44\mathrm e{-}16$ | $\le0$ (eq (1.6)) | PASS (FP) |
| $\max_{\mathcal F}\,[\text{ahsLB}-H(A\cup B)]$ | $0.00\mathrm e{+}0$ | $\le0$ (eq (2.4)) | PASS |
| $\min_{\mathcal F}$ abundance | $0.500000$ | $\ge\psi=0.381966$ (thm); conj $\ge0.5$ | PASS |

**Conclusion.** Every inequality in `ahs_proof_explicit.md` holds on all tested families with
deficit at most floating-point noise. The reconstruction is internally consistent.

## Run 2 — Single-letter optimization (the asymptotic constant of each strategy)

Command: `python3 single_letter.py`. Grid $N=800$ with local refinement.

| strategy | $\mu=\inf \Phi/B$ | closing factor | constant $c=1-\text{cf}/\mu$ | argmin | verdict |
|---|---|---|---|---|---|
| **ahs** (track $H(A\cup B)$, budget $H(A)$) | $0.80902$ | $1/2$ | **$0.381966$** | $(\psi,\psi)$ | **= $\psi$ (anchor OK)** |
| v2_joint_sym (track $H(\cup,\cap)$, budget $2H(A)$) | $0.75000$ | $1$ | $-0.333333$ | $(0.5,0.5)$ | useless |
| v2_joint_ahsbudget (WRONG budget) | $0.87636$ | $1/2$ | $0.429460$ | $(0.035,0.035)$ | **artifact** |

The anchor (`ahs` $=\psi$ exactly, argmin at the golden point) validates the optimizer. The
"0.4295" for the joint objective is exposed as an **artifact of using the single-$H(A)$ budget
for a quantity whose honest budget is $2H(A)$**; with the correct budget the constant is
$-1/3$.

## Run 3 — Chain-rule slack $\Delta_2$ (Vector 1 diagnostic)

$\Delta_2(\mathcal F):=H(A\cup B)-\sum_i H(C_i\mid A_{<i},B_{<i})=\sum_i I(C_i;(A_{<i},B_{<i})\mid C_{<i})\ge0$.

- On the **extremal families** (abundance $=0.5$: power sets $2^{[k]}$ and products thereof),
  $\Delta_2 = 0$ to machine precision (verified on $2^{[1]},\dots,2^{[4]}$ and products).
- Among the 330 families with $c_{AHS}$ within $0.005$ of the minimum (the near-bottleneck set),
  $\max \Delta_2 = 2.37\mathrm e{-}2$ and $\max \Delta_2/H(A\cup B)=7.1\mathrm e{-}3$, shrinking
  toward 0 as $c_{AHS}\to\psi$.
- Where $\Delta_2$ is **largest** ($\Delta_2/H(A\cup B)\approx0.288$), $c_{AHS}\approx0.58$ —
  far above $\psi$. **Anticorrelation:** $\Delta_2$ is large only off the bottleneck.

**Conclusion (Vector 1).** Recapturing $\Delta_2$ gives **zero asymptotic improvement**: the
chain-rule slack vanishes on exactly the (product) configuration that drives the constant.

## Run 4 — Intersection budgets (Vector 2 linchpin)

Tested over $n\le5$ orbit reps (29,738 families incl. $n\le5$):

| Hypothesis (needed for a Vector-2 budget) | violations | worst excess | verdict |
|---|---|---|---|
| $H(A\cap B)\le H(A)$ | 22,361 / 29,738 | ratio up to $1.530$ | **FALSE** |
| $H(A\cup B,A\cap B)\le H(A)$ | 402 / 412 ($n\le4$) | $+2.126$ | **FALSE** |
| $H(A\triangle B)\le H(A)$ | 366 / 412 ($n\le4$) | $+1.321$ | **FALSE** |

**Conclusion (Vector 2).** Union-closure constrains $A\cup B$ (forces $\in\mathcal F$) but gives
no control on $A\cap B$, $A\triangle B$, or the joint — all routinely exceed $H(A)$. No valid
budget exists for an intersection-augmented objective; the only honest budget ($2H(A)$ for the
joint) defeats the gain.

---

## Failures / flagged cases

None in the sense of inequality violations of the AHS reconstruction. The two "improvements"
that initially appeared (V2-joint $0.4295$; a buggy per-family diagnostic giving $0.5$) were
both traced to **invalid budget accounting** and are recorded in `dead_ends.md`. The corrected
analyses give no improvement. This is the honest negative outcome.

## Reproduction

```
cd frankl/experiments
python3 verify_ahs.py        # Lemma 2 grid + psi
python3 single_letter.py     # single-letter constants for all strategies
python3 vector_analysis.py   # per-family diagnostics (note: heuristic; see dead_ends)
```
