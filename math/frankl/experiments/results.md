# Results: joint optimization of the entropy-method constant

**Track:** Frankl Vector 3 (joint optimization + certification)
**Author:** Alex Ye (AI assistance disclosed separately)
**Date:** 2026-06-02
**Reproduce:** `python3 joint_opt.py`, `python3 certify_psi.py`,
`python3 verify_opt_formulation.py`, `python3 make_figures.py`.

---

## 1. Headline

| quantity | value | how certified |
|---|---|---|
| **Best CERTIFIED constant** | **`c = ψ = (3 − √5)/2 ≈ 0.3819660`** | closed-form proof + interval arithmetic (`certificate_0.38197.md`) |
| Sanity floor (ψ) reproduced? | **YES** (base = `0.38196592`, → ψ) | `joint_opt.py`, `verify_opt_formulation.py` |
| Liu checkpoint `0.38271` reproduced? | **NO** | source inaccessible + reconstruction failed (see §4) |
| New constant `> 0.38271`? | **NO** | the program plateaus at ψ (see §3) |

We did **not** beat any existing number. The honest finding is a **plateau at ψ**:
within the relaxations we could implement *and certify*, the certified constant is
exactly the sanity floor ψ. This is recorded as an honest negative result per the
verification protocol.

---

## 2. What was run

The optimization is the **dimension-free single-letter** program of
`opt_formulation.md`. Decision object: a law `μ` of the per-coordinate marginal
`P` (and, for the auxiliary cases, an auxiliary `U` and conditional structure).
The certified constant is

```
c = sup{ t : (IV) is infeasible for every non-degenerate μ supported on [0,t] },
(IV)  E_{P,Q iid∼μ}[h(1−(1−P)(1−Q))] ≤ E_μ[h(P)].
```

located by **bisection on `t`** (the naive "minimize E[P] over the feasible set"
returns 0 via the degenerate `μ = δ_0` — see §4, lesson 1).

### 2.1 Numerical results (`python3 joint_opt.py`, ~5 min)

```
closed-form psi = 0.3819660112501051
base i.i.d.          c = 0.38196592   Δψ = −9.3e-08   [verified]
reweighting (Cambie) c = 0.38196592   Δψ = −9.3e-08   [verified]   (identical to base)
aux |U|=2  [diagonal] c = 0.38190421   Δψ = −6.2e-05  [verified]
aux |U|=4  [diagonal] c = 0.38190421   Δψ = −6.2e-05  [verified]
aux |U|=8  [diagonal] c = 0.38190421   Δψ = −6.2e-05  [verified]
aux |U|=16 [diagonal] c = 0.38190421   Δψ = −6.2e-05  [verified]
```

All values equal ψ to within the bisection/grid resolution (`Δψ` is negative and
`O(10⁻⁵–10⁻⁷)`, i.e. resolution, not a genuine sub-ψ bound). The base witness is a
single point mass at `p ≈ ψ` (`= δ_ψ`), exactly the closed-form extremizer.

### 2.2 Certification (`python3 certify_psi.py`, ~9 s)

- **Closed-form** (hand-verifiable): `ψ²−3ψ+1 = 0`; crossover `2ψ−ψ² = 1−ψ`;
  `δ_ψ` makes (IV) tight; Sawin's (S) + independence ⟹ `E[P] ≥ ψ`. (Details:
  `certificate_0.38197.md` §A.)
- **Interval arithmetic** (`mpmath.iv`, mean-value form): the load-bearing Sawin
  inequality `G(p,q) ≥ 0` is rigorously certified on `[0.01,0.99]²` with min
  interval lower bound `+4.96 × 10⁻⁹`, exempting only a `10⁻³`-neighborhood of the
  unique equality point `(ψ,ψ)`; boundary strips handled analytically.

---

## 3. Where the optimization plateaus, and why

**It plateaus at ψ.** Three distinct relaxations, all certified to give exactly ψ:

1. **Reweighting (Cambie), alone — no gain.** In the dimension-free limit,
   reweighting the base measure on `F` is *exactly* the freedom to choose the law
   `μ` of `P`. The base program already optimizes over all `μ`, and its optimum is
   ψ (closed form). So reweighting *alone* cannot beat ψ. This is a clean,
   verified statement, not a tuning failure. (Cambie's published gain comes from
   coupling reweighting with non-i.i.d. structure **and** finite-`n` effects, both
   outside this single-letter program.)

2. **Auxiliary `U`, faithfully reconstructed ("diagonal") — no gain.** In the
   conditional-i.i.d. coupling, given `U=j` the pair `(A_i,B_i)` is i.i.d.
   `Bern(p_j)`, so the single-letter `(P,Q)` sits on the **diagonal**
   `{(p_j,p_j)}`. (IV) then reads `Σ_j w_j h(2p_j−p_j²) ≤ Σ_j w_j h(p_j)`, a
   mixture over the *same per-point crossover*, whose threshold is again ψ for
   every `|U|`. The auxiliary variable, in the part we can rigorously justify,
   does nothing.

3. **The "obvious" way to use a richer coupling makes things WORSE.** Allowing the
   single-letter `(P,Q)` an arbitrary off-diagonal joint law (identical marginals)
   *lowers* the certified threshold to `≈ 0.359 < ψ`. Reason: a *larger* coupling
   class makes (IV) a *weaker* necessary condition, so minimizing the mean marginal
   over it can only *decrease* the bound. **Improvements beyond ψ require *adding*
   valid constraints (recovered mutual information), not enlarging the coupling.**
   This is the central structural reason the plateau is hard to cross from the
   "coupling side" and is exactly the slack identified in survey §7.2 (B.6).

**Why we did not reach Liu's 0.38271.** Liu's gain comes from a *tighter lower
bound* on `H(C)` that recovers part of `Σ_i I(C_i;(A_{<i},B_{<i})|C_{<i})` using a
shared `U`, via precise `I(C;U)`/`I(A;U)` bookkeeping. Implementing that correctly
requires Liu's exact functional (his "9-dimensional optimization"). We could not
obtain it (see §4).

---

## 4. Honest negatives / obstructions (also logged in `shared/dead_ends.md`)

1. **`min E[P]` is the wrong objective.** It admits the degenerate `μ = δ_0`
   (vacuously feasible, `E[P]=0`). Correct object: the *threshold* `t` at which
   (IV) flips from infeasible to feasible, with a non-degeneracy constraint
   `E[h(P)] > 0`. Fixed by bisection (`joint_opt.py`).

2. **Liu/Yu sources inaccessible in this environment.** `arxiv.org/abs/2306.08824`
   and `.../2212.00658` (and `ar5iv`, mirrors, direct PDF) all returned HTTP 403 /
   "host not in allowlist". We could not read Liu's exact functional.

3. **From-first-principles reconstruction of Liu's conditional-`U` functional
   FAILED.** Two attempts: (a) a "diagonal" reading gives no gain (§3.2); (b) a
   naive `I(C;U)/I(A;U)` "refund" collapses to `h(ū) ≤ h(p̄)` with
   `ū = 2p̄ − E[P²]`, which admits a degenerate optimizer with atoms at `p∈{0,1}`
   that drives the bound spuriously to 0 — a sign the refund double-counts. We did
   NOT certify any constant from this; it is retained only as
   `conditional_U_functional(mode='liu_refund')`, clearly marked UNVERIFIED.

4. **Plain interval arithmetic over the 2-D Sawin inequality is too slow / loose.**
   The naive natural interval extension over-estimates badly (variable sharing in
   `h(u), h(p), h(q)`): ~60 % of boxes show spurious negative lower bounds, and
   deep refinement at 140-bit precision times out. **Fix that worked:** a
   mean-value (centered) interval extension cancels the first-order dependency and
   certifies `[0.01,0.99]²` in ~4 s. The exact boundary `p∈{0,1}` (where
   `h'(t)→∓∞`) is covered analytically, not by interval arithmetic.

---

## 5. Status vs the verification protocol

- **Step 1 (computational sanity):** PASS for ψ — `verify_opt_formulation.py`
  (all checks pass), `certify_psi.py` (closed-form + interval).
- **Steps 2–4:** not required for ψ (an already peer-reviewed AHS 2024 constant we
  merely reproduce). **No new constant is claimed**, so no red-team / Lean / human
  sign-off is pending on a *new* result.

> If a future iteration obtains Liu's exact functional (or a corrected
> conditional-`U` bookkeeping) and the program returns `> 0.38271`, that would be a
> candidate new result and MUST be flagged "PENDING RED-TEAM + HUMAN REVIEW" — it
> is not the case here.

---

## 6. Files

| file | role |
|---|---|
| `opt_formulation.md` | exact objective + constraints, cited to source, direction-checked |
| `joint_opt.py` | the optimization (base / reweighting / auxiliary `U`∈{2,4,8,16}) |
| `verify_opt_formulation.py` | Step-1 checker for every inequality in the formulation |
| `certify_psi.py` | closed-form + interval-arithmetic certificate of `c = ψ` |
| `certificate_0.38197.md` | the certificate (the result) for the value ψ |
| `make_figures.py` → `figures/` | crossover, Sawin slack, threshold-vs-`|U|`, feasibility-vs-`t` |
| `data/joint_opt_run.txt` | captured run log |
