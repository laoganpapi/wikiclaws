# Step-1 Verification Log — cycle_bound_attempt.md

**Track:** collatz / Vector C (cycle exclusion — from-scratch cycle-length derivation)
**Author:** Alex Ye (AI assistance disclosed separately)
**Protocol:** `shared/verification_protocol.md` Step 1 (computational sanity check)

---

## Run 1 — 2026-06-02

**Code paths:** `collatz/experiments/verify_cycle_bound.py` (new), plus the extended
`collatz/experiments/cycles.py` (`circuit_decomposition`, `check_bound_consistency`).

**Environment:** Python 3.11, `mpmath` available (dps=120). Linux sandbox (academic PDF hosts
HTTP-403 / not in network allowlist, as documented).

**Test scope and results:**

| Check | What it verifies | Result |
|---|---|---|
| D1 | Per-circuit identity $2^{L_j}x_{j+1}=3^{a_j}x_j+(3^{a_j}-2^{a_j})$ by **direct iteration of $T$** (400 random $(a,x)$ with genuine ascending runs; no algebra trusted) | PASS |
| D2 | Cyclic fixed point $x_1=R/(2^N-3^K)$ with explicit $R=\sum_j d_j3^{P_j}2^{N-Q_j}$ closes (80 random circuit lists, exact `Fraction` iteration) | PASS |
| D3 | **Exact identity** $\Lambda=N\log2-K\log3=\sum_j\log(1+d_j/(3^{a_j}x_j))$ (Thm 3); max abs error $\approx3.9\times10^{-120}$ over 80 cases | PASS |
| D4 | **Rigorous bounds** $0<\Lambda<m/x_{\min}$ (global) and $0<\varepsilon_j\le1/x_j$ (per-term) on **17,762 genuine positive fixed points** | PASS (both) |
| D5 | Crandall continued-fraction lower bound on $K$ at $B=3\cdot2^{69}$ ($K>2.617\times10^{10}$) and $B=2^{71}$ ($K>3.489\times10^{10}$); identification $q_{23}=137{,}528{,}045{,}312=1.375\times10^{11}$ = Hercher's stated target | PASS |
| cycles.py | No nontrivial positive cycle for parity length $\le22$; orbit search $n\le2\times10^5$ finds none; circuit-decomposition + identity $\Lambda=\sum\varepsilon_j$ + bound $0<\Lambda<m/n$ hold on all positive fixed points found (the trivial cycle) | PASS |

**D6 (provisional bookkeeping, NOT a Step-1 pass/fail):** the largest excludable $m^\*$ at $B=2^{71}$
under two transparent models of Hercher's upper bound $F(m)$: Model P (power law) $\to m^\*\approx99$;
Model H (Hercher-calibrated) $\to m^\*\approx91$–$92$. Reported as a `[PROVISIONAL]` bracket
$91\le m^\*\le99$, trustworthy estimate $\{91,92\}$. This is **not** verified — it depends on $F(m)$,
which is not reconstructed (see `cycle_bound_attempt.md` §3, §6).

**Failures:** 0 on the rigorous checks (D1–D5 + cycles.py).

**Flagged cases / notes:**
- **D4 non-vacuity.** An earlier draft of D4 required $x_{\min}>10^6$ and tested **0** fixed points
  (vacuous pass — exactly the `verification_protocol.md` anti-pattern "it worked on 0 cases"). Fixed:
  D4 now enumerates **all** genuine positive fixed points (17,762 of them) and checks the scale-free
  algebraic inequality on each, plus the per-term bound $\varepsilon_j\le1/x_j$. A positive fixed point
  with $x_{\min}>10^6$ requires $N/K$ to be a high-order convergent of $\log_2 3$ (3^K astronomically
  large), not enumerable here; since the inequality is scale-free, the accessible-scale enumeration is a
  faithful check, and the $x_{\min}>B$ regime is covered by the proof (Cor 4), not the enumeration. This
  is documented in the code.
- **Direction finding (Prop 5).** The self-contained bound $0<\Lambda<m/B$ combines with the de Weger /
  LMN lower bound to give only a **lower** bound on $K$ (the Crandall side), not the upper bound $F(m)$.
  This is proved (not just observed) and is the honest limit of the from-scratch reconstruction.
- **Constants.** $\log_2 3$, its convergents, and the $m/B$ bound are **self-derived / exact** (no
  external constant). The de Weger exponent $0.158$ / threshold $K\ge32$ are snippet-sourced and
  independently reproduced in `verify_cycle_exclusion.py` C5a. The LMN $24.34\,D^4$ remains
  **`[CONSTANT UNVERIFIED]`** (primary PDF unreachable). $B=2^{71}$ is web-verified (Barina, J.
  Supercomput. 81, 2025). Hercher's target $1.375\times10^{11}$ and $B=3\cdot2^{69}$ are web-verified
  and the former is confirmed to be exactly $q_{23}$.

**Verdict:** Step 1 PASSED for the rigorous core (§1–§4 of `cycle_bound_attempt.md`: the cycle equation,
the exact $\Lambda=\sum\varepsilon_j$ identity, the bound $0<\Lambda<m/B$, the Crandall lower-bound
values). The upper-bound side $F(m)$ is **not reconstructed** and the $m^\*>91$ question is
**`[PROVISIONAL]` / `[UNVERIFIED — needs Hercher 2023 primary source]`**. Step 1 is necessary, not
sufficient; Steps 2–4 (red-team, Lean of the core lemmas, human sign-off) remain.
