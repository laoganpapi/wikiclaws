# Step-1 Verification Log — cycle_exclusion_explicit.md

**Track:** collatz / Vector C (cycle exclusion)
**Author:** Alex Ye (AI assistance disclosed separately)
**Protocol:** `shared/verification_protocol.md` Step 1 (computational sanity check)

---

## Run 1 — 2026-06-02

**Code path:** `collatz/experiments/verify_cycle_exclusion.py` (commit-local), plus
`collatz/experiments/cycles.py` brute-force.

**Environment:** Python 3.11, `mpmath` available (dps=120). Linux sandbox.

**Test scope and results:**

| Check | What it verifies | Result |
|---|---|---|
| C1 | $\delta=\log_2 3$ to 80+ digits; continued fraction $[1;1,1,2,2,3,1,5,2,23,\dots]$ | PASS |
| C2 | Literature "magic numbers" ($301994$, $190537$, $17087915$, $85137581$, $357638239$, $217976794617$, $10439860591$, $6586818670$) are all convergent numerators/denominators of $\delta$ | PASS (8/8) |
| C3 | Legendre $q^2|\delta-p/q|<1$ for all convergents; $2^N\ne 3^K$ for $K\le2000$ (denominator never zero) | PASS |
| C4 | Hercher's verified bound arithmetic $1536\cdot2^{60}=3\cdot2^{69}=1{,}770{,}887{,}431{,}076{,}116{,}955{,}136$ | PASS |
| C5a | **De Weger's reformulation:** $0<N\log2-K\log3<2^{-0.158K}$ has no solution for $K\ge32$ (largest solution at $K=29$) | PASS |
| C5b | Directional argument (theory §5.2): two-log lower bound on $|\Lambda|$ has linear-in-$K$ exponent (slope $0.158$, caps $K$ from above); irrationality-measure bound has slope $\to0$ (gives only a lower bound on $K$) | PASS (illustrative) |
| cycles.py | No non-trivial positive cycle for parity length $\le22$; no cycle with $x_{\min}\le10^5$, period $\le3000$; negative cycles $-1,-5,-17$ close correctly | PASS |

**Failures:** 0 (after the C5 fix — see below).

**Flagged cases / notes:**
- **C5 was rewritten after an initial failure.** The first version of C5 compared the *numerical magnitudes* of the LMN lower bound and the irrationality-measure lower bound on $|\Lambda|$ at the optimal convergent, and concluded (incorrectly) that the irrationality bound was "larger." This reflected a **mis-statement of the claim**, not a flaw in the literature: the correct claim (theory §5.2) is *directional* — only an exponentially-decaying (in $K$) lower bound on $\Lambda$ can produce an **upper** bound on the cycle length $K$; a polynomial bound (irrationality measure) gives only a **lower** bound on $K$ and so cannot contribute to the contradiction. C5 now tests (a) de Weger's actual inequality and (b) the slope/direction. The episode is logged in `shared/dead_ends.md` (2026-06-02 entry). This is exactly the kind of self-error Step 1 is meant to catch.
- The constants in the LMN estimate (9) in the theory note — the leading $24.34$, the auxiliary $0.14$, the $\max$-floor — are tagged `[PARTIAL-CONST]`: confirmed from multiple secondary snippets (Simons's AMS-paper application; Bugeaud survey; Evertse Leiden notes) but **not** from the primary LMN/Laurent PDFs, which returned HTTP 403 in this environment (consistent with `survey.md`'s documented access limitation). The de Weger exponent $0.158$ and threshold $K\ge32$ are independently re-derived numerically here (C5a), so the *operative* form is verified even though the upstream LMN constant is only partially verified.

**Verdict:** Step 1 PASSED. The numerical claims of `theory/cycle_exclusion_explicit.md` (§4.2, §5.1b, §9) are confirmed. Step 1 is necessary, not sufficient; the document's analytic conclusions (bottleneck = two-log estimate; $\mu(\log_2 3)$ structurally useless) still require Step 2 (red-team) and, ideally, confirmation against the primary Hercher / Laurent-2008 PDFs.
