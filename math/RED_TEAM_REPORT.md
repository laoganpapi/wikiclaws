# RED-TEAM REPORT — Phase 2 mathematical claims

**Red-team author:** (adversarial audit, AI-assisted; not on the project author line)
**Date:** 2026-06-02
**Scope:** Internal logical/mathematical consistency (PART A, done fully offline) + enumeration of
novelty/prior-art questions requiring primary sources (PART B, deferred — arXiv/journal PDFs are
HTTP-403 in this environment).
**Method:** Every load-bearing inequality re-derived by hand and/or re-checked numerically with an
*independent* implementation (not trusting the project's own code), then the project's own checkers
were re-run and stress-tested with adversarial inputs (e.g. perturbing the sharp constant to confirm
the certifier actually fails). Test suites: 44/44 Frankl, 61/61 Collatz pass.

---

## EXECUTIVE SUMMARY

**Which claims survive (internally sound):**
1. **AHS `(3−√5)/2` reconstruction** — SOUND. Every inequality verified; ψ-algebra exact; the load-
   bearing Sawin inequality G≥0 holds with a genuine isolated touch-zero at (ψ,ψ) (positive-definite
   Hessian), and the constant λ=φ/2 is provably sharp (bumping it up 0.1% makes G<0). End-to-end chain
   verified on 4389 union-closed families (n≤4): 0 violations, worst abundance exactly 0.5 ≥ ψ.
2. **Vector 1 (Δ₂≡0 at product extremizer)** — SOUND. Independently confirmed Δ₂=0 (to machine zero)
   on all product families and Δ₂>0 on correlated ones; Δ₂≥0 always.
3. **Vector 2 (H(A∩B)≰H(A) for UC families; 0.4295/0.5 are budget-mismatch artifacts)** — SOUND.
   Independently reproduced H(A∩B)>H(A) on 35/121 UC families at n=3 (ratio up to 1.367; doc's 1.53 at
   n≤5 is consistent), the joint-objective excess H(∪,∩)>H(A) on 113/121, and μ=¾→c=−⅓ exactly. The
   artifacts are genuinely errors and do **not** leak into any live claim.
4. **ψ interval-arithmetic certificate** — SOUND and genuinely rigorous (not a rubber stamp): the
   mean-value certifier CERTIFIES at the true λ and correctly FAILS (finds a real bad box) when λ is
   bumped up 0.1%. Reproduces +4.43e-9 (δ=0.02) / +4.96e-9 (δ=0.01). Exemption of (ψ,ψ) is justified.
5. **Collatz cycle-exclusion factual core + de Weger threshold** — SOUND. The historical claim "the
   Steiner–SdW–Hercher proofs use the two-log linear-forms estimate (LMN/Laurent), not μ(log₂3)" is a
   correct reading. De Weger threshold `0<Λ<2^{−0.158K}` independently verified: solutions exactly at
   K∈{1,2,3,4,5,6,8,10,15,17,29}, largest at **K=29**, none for K≥32 (verified to K=4999). All
   continued-fraction / convergent-numerator anchors (357638239, 17087915, 85137581, 301994,
   217976794617, …) reproduce exactly; CF of log₂3 matches; Simons m=2 squeeze (K>1.38e8 vs K<86000)
   reproduces.
6. **Collatz 3^{n/2} Plancherel exponent** — the exponent **n/2 is correct** (Parseval normalization
   verified; ‖·‖_{ℓ¹}≤√(support)·‖·‖_{ℓ²}, support=φ(3ⁿ)<3ⁿ; θ>½ threshold arithmetic correct).

**Which claims die / are wounded:**
- **Tao-Syracuse Lemma 6.1 + Lemma 6.2 contain a genuine mathematical ERROR** (the *only* hard error
  found). They drop the Fourier mass at the `3∣ξ` frequencies as if it were zero ("discrepancy carried
  entirely by {3∤ξ}"), but the Syracuse law's projection mod 3 is permanently **(0, ⅓, ⅔)** — never
  uniform — so a non-vanishing chunk of the ℓ² discrepancy lives at 3∣ξ. Consequence: **MIX(θ) as
  stated (bounds only 3∤ξ coefficients) does NOT imply TV→0**, so Lemma 6.2 — which the document calls
  "the crux, proved in full" — is false as written, and ν provably can **never** converge to U in TV
  (TV ≥ 1/6 for all n). This breaks the *stated* form of the conditional theorem's proof, though the
  document's honest bottom-line (the natural-density route is open/blocked/possibly-false) actually
  survives and is *reinforced* by this finding.

**The single biggest risk to the project's credibility:**
> **NOVELTY, not correctness.** The internally-sound results are reconstructions of published work or
> *negative/no-improvement* findings. The one structural claim with any "new observation" flavor — *the
> entropy method caps at ψ within i.i.d. couplings (Vector 1: Δ₂≡0 at the product extremizer; Vector 3:
> enlarging the coupling weakens (IV))* — is **very likely already known**. Sawin (arXiv:2211.11504)
> and follow-ups explicitly discussed the entropy method's ceiling, and the product-extremizer /
> tensorization picture is standard in Gilmer/AHS/Sawin. **This must be checked against primary sources
> before any "new observation" is asserted; if it is already in Sawin 2022 or Cambie 2023, the claim
> has no novelty.** The project's own docs mostly frame these as honest negatives (good), but the
> framing "main expository contribution / sharpened obstruction" should not be upgraded to a *result*
> without the prior-art pass. Secondary credibility risk: the Tao-Syracuse Lemma 6.2 error is presented
> as "proved in full," which would not survive review of that specific lemma.

---

## PER-CLAIM VERDICTS

### Doc 1 — `frankl/theory/ahs_proof_explicit.md` (AHS reconstruction)

**VERDICT: internally-sound.**

Checks performed and passed:
- ψ²−3ψ+1=0, crossover 2ψ−ψ²=1−ψ, (1−ψ)²=ψ, σ=1/φ, λ=φ/2<1 — all exact to 60 digits.
- Sawin/Lemma-2 inequality `G(u,v)=h(uv)−λ[v·h(u)+u·h(v)]≥0`: grid min = 0 at corners and (σ,σ);
  equality at (σ,σ); Hessian there is PD (eigenvalues 0.142, 0.858) → genuine isolated min.
- **Sharpness:** bumping λ→λ(1+1e-4) makes min G ≈ −6.6e-5 < 0 near the diagonal → ψ is forced.
- Diagonal φ(s)=h(s²)−2λs·h(s)≥0 with φ(σ)=0 and φ′(σ)=0 (tangency) — verified.
- The doc's §2.3.1 *honest admission* that the slick diagonal reduction fails (Θ_s″(0) changes sign
  near s≈0.17) is **correct** — verified numerically; the doc correctly falls back to interval
  arithmetic rather than claiming a false analytic reduction.
- End-to-end inequality chain (1.2)/(1.6)/(2.4) on 4389 UC families (n≤4): 0 violations of
  H(A∪B)≤H(A), 0 violations of AHS-lower-bound ≤ H(A∪B), abundance ≥ ψ everywhere.

Minor blemishes (cosmetic, not errors): the Lemma-2 statement (2.1) has a visibly garbled fragment
"`(1-\psi)^2 = 1-\psi\cdot\tfrac{?}{}` …" (a leftover TODO) before the correct boxed identity
`(1−ψ)²=ψ`. Severity: **minor** (typo; correct identity stated immediately after).

**PART-B novelty question:** None — this is explicitly a reconstruction of AHS (arXiv:2211.11731,
EJC 31(3) #P3.35) following Gilmer (2211.09055) and Sawin (2211.11504). To confirm the *exposition*
adds nothing claimed-as-new, read AHS §3 and Sawin §2–3 (the "one branch checked by computer /
interval arithmetic" statement should be located verbatim to confirm the doc's framing).

---

### Doc 2 — `frankl/theory/vector1_shearer_chain_rule.md` (Vector 1 fails: Δ₂≡0)

**VERDICT: internally-sound.** (Conclusion "no improvement" is correct *within the i.i.d. coupling*.)

- Lemma 1 (chain rule lossless on independent coordinates ⇒ Δ₂=0): independently verified — Δ₂=0 to
  machine zero on 2^[2], 2^[3], 2^[2]×2^[1]; Δ₂>0 on correlated families ({3,5,6,7}: 0.170; chain
  {0,1,3,7}: 0.081); Δ₂≥0 on all n=3 UC families (it is a sum of conditional mutual informations).
- The §4 argument that Shearer/Han cannot help (they are *upper* bounds, tight on products; the
  required direction is not a generic entropy inequality) is logically correct.

**Load-bearing logical caveat (the doc states it honestly; flagging for the record):** Theorem 1's
"the AHS optimum lives where Δ₂=0" is **not** a from-scratch tensorization proof that *no* correlated
family does better. The doc explicitly says it only needs *some* extremizing sequence to be product
(to upper-bound the Vector-1 gain by 0 along it), which Lemma 1 + single-letter tightness deliver.
That is logically sufficient for the *negative* conclusion "Vector-1 gain ≤ 0 along this sequence,"
**but it does not rigorously exclude that a correlated family with Δ₂>0 beats ψ via a different
balance.** This is the one place a skeptic could push; the doc's hedge (§2.4 "Caveat on full rigor")
is appropriate and the claim is stated at the right confidence. Severity: **needs-caveat** (already
caveated in-doc).

**PART-B novelty question (HIGH PRIORITY — biggest novelty risk):**
> *Is "Δ₂≡0 at the product extremizer ⇒ entropy method caps at ψ within i.i.d." already known?*
> Strong suspicion: **YES.** Must read **Sawin arXiv:2211.11504** (the §/remarks discussing why the
> method does not exceed ψ and what is needed to go beyond — Sawin's improvement uses a *non-i.i.d.*
> coupling, which presupposes exactly this ceiling) and **Cambie arXiv:2306.12351 §3** (reweighting).
> Also **Liu arXiv:2306.08824** and **Yu arXiv:2212.00658** (conditional-U couplings move the
> extremizer off the product point — implicitly acknowledging Δ₂=0 there). If any of these states the
> product-extremizer ceiling, Vector 1 has **no novelty** as an "observation."

---

### Doc 3 — `frankl/theory/vector2_intersection_term.md` (Vector 2 fails)

**VERDICT: internally-sound.**

- **Theorem 2 (H(A∩B)≰H(A)):** independently reproduced — 35/121 UC families at n=3 have H(A∩B)>H(A)
  (max ratio 1.367; doc's 1.53 at n≤5 is consistent with growth in n). Mechanism (A∩B ranges over the
  intersection-closure, which can be larger than F) is correct. **No** family ever has H(A∪B)>H(A)
  (0 violations) — union-closure direction is solid.
- **Theorem 1 (joint budget ⇒ c=−⅓):** μ_joint = inf H_pair/(h(α)+h(β)) = ¾ at (½,½) exactly
  (H_pair(½,½)=1.5 bits, h+h=2), closing factor 1 ⇒ c=1−4/3=−⅓. Reproduced independently.
- **Prop 3 (0.4295 artifact):** μ′=0.87636 at boundary (0.035,0.035), c=0.42946 reproduced; it
  assumes H(∪,∩)≤H(A), which is FALSE on 113/121 families at n=3 (excess up to 1.529). Genuinely an
  artifact. The "0.5" artifact is documented as a buggy per-family diagnostic (vector_analysis.py:11).
- **Artifact-leakage check:** the certified-ψ pipeline (`joint_opt.py::base_program`) uses only the
  correct (IV) with the AHS budget; the `_WRONG` budget exists only in `single_letter.py` labeled as a
  demonstration. **No live claim depends on the artifacts.**

**PART-B novelty question:** Whether the intersection-side obstruction (Reimer's theorem is a
first-moment statement, not an entropy bound on A∩B; A∩B lives in the intersection-closure) is already
noted in the literature. Read **Reimer (Combin. Probab. Comput. 2003, average-set-size)** and the
**survey §7.x** the doc cites; check whether **Cambie 2023** or **Sawin** already remark that union-
closure gives no control on H(A∩B). Likely a known asymmetry; low novelty stakes since this is a
*negative* result.

---

### Doc 4 — `frankl/experiments/results.md` + `certificate_0.38197.md` (ψ certificate)

**VERDICT: internally-sound.**

- Closed-form part (A): ψ quadratic, crossover, δ_ψ feasible & tight, Sawin (S)+independence ⇒
  E[P]≥ψ — the two-line averaging is correct (`E[(1−Q)h(P)]=(1−E[P])E[h(P)]` by independence; combine
  with (IV)). Verified.
- Interval part (B): **genuinely rigorous.** Reproduced min interval lower bound +4.43e-9 (δ=0.02),
  +4.96e-9 (δ=0.01). The mean-value (centered) extension is sound; I confirmed the certifier is not a
  rubber stamp by re-running it with λ→λ·1.001 — it correctly **fails** (bad box at (0.455,0.448),
  lower bound −3.0e-11), and with λ→λ·0.999 it certifies (weaker inequality). The (ψ,ψ) exemption is
  justified: dense point-scan inside the 1e-3 neighborhood shows G only *touches* 0 (PD Hessian), so
  no positive-width box can bound it strictly above 0 — the point is discharged exactly by A.2/A.4.
  Boundary strips handled analytically via G(0,q)=(1−λ)h(q)≥0 (λ=φ/2<1). **The constant is certified.**
- Vector-3 "plateau at ψ" + "enlarging the coupling lowers the threshold below ψ (≈0.359)": the
  *direction* is independently confirmed (an arbitrary off-diagonal coupling with equal marginals
  drives inf E[P] well below ψ). This is a *different* mechanism from Vector 1's Δ₂=0 (see cross-check
  below), so the two Frankl tracks are not a common-mode restatement.

**Cross-check of the "two independent agents converge" question:** The two tracks genuinely *agree in
conclusion* (method caps at ψ; richer couplings move the wrong way) via *distinct* arguments —
Track A (Vector 1): Δ₂=0 *at the specific product extremizer*; Track B (Vector 3): *enlarging* the
coupling class makes (IV) a weaker necessary condition so inf E[P] drops, hence gains require *adding*
constraints. These are complementary, not the same lemma reworded. **Shared assumption (potential
common-mode):** both rest on the *dimension-free single-letter reduction* being the correct object and
on the extremizer being a product/i.i.d. configuration. That shared frame is standard (Gilmer/AHS),
not an error — but it is exactly the assumption a novelty/priority check must confront (see Doc 2 B).

**PART-B novelty question:** ψ itself is peer-reviewed AHS 2024 (no novelty claimed — correct). The
only thing to confirm is that **no constant > 0.38271 (Liu) is claimed** (it is not; explicitly
"NOT reproduced"). No primary source needed for the certificate's validity.

---

### Doc 5 — `collatz/theory/tao_syracuse_explicit.md` (conditional natural-density theorem)

**VERDICT: error-found (in Lemmas 6.1/6.2), with the rest internally sound.**

**(5a) The 3^{n/2} Plancherel claim — SOUND.** Parseval normalization verified with the doc's sign
convention; ℓ¹≤√(support)·ℓ²; support=φ(3ⁿ)<3ⁿ so the toll is ≤3^{n/2}; TV ≤ ½C·3^{(½−θ)n} ⇒ TV→0
iff θ>½. The exponent is genuinely **n/2**. The "superpolynomial n^{−A} cannot pay a 3^{n/2} toll, need
3^{−θn}" framing is correct.

**(5b) `β=1` insufficient / collision-probability finding — SOUND (and independently reproduced).**
E_n=φ(3ⁿ)·CP_n−1 for the untilted law: **0.111, 0.429, 0.736, 1.046, 1.357, 1.667** (constant
differences ≈0.31) — reproduced *exactly* by an independent Syracuse implementation. Tilted E_n grows
super-linearly and is worse — reproduced. The conclusion "β=1 (exponential order) is necessary but not
sufficient; need exact-leading-constant equidistribution" is correct. The descent-balance tilt
s*≈0.438 with E_{s*}[a]=log₂3 is exact.

**(5c) ERROR — Lemma 6.1 and Lemma 6.2.** Location: §6.1 Lemma 6.1 displayed inequality
`‖ν−U‖²_{ℓ²} ≤ (1/3ⁿ)Σ_{3∤ξ}|ν̂(ξ)|²` and its justification "for 3∣ξ … the discrepancy from uniform
is carried entirely by {3∤ξ}"; propagates into Lemma 6.2's proof (first line "By Lemma 6.1, …").

*The error:* The Syracuse law's projection **mod 3 is permanently (0, ⅓, ⅔)** — I verified this is
(0,⅓,⅔) for n=1,2,3,4 (it is the n=1 law, since `b mod 3 = 2^{−aₙ} mod 3`; the project's own code
comment at `verify_syracuse_rv.py:214-215` states the same). Therefore ν is **not** uniform across the
unit-cosets mod 3, so the Fourier coefficients of ν−U at the `3∣ξ` frequencies (e.g. ξ=3,6 at n=2) are
**nonzero** (|diff|=0.289 each), and a *non-vanishing* fraction of ‖ν−U‖²_{ℓ²} lives there
(n=2: 0.0185 of 0.0714; n=3: 0.0238 of 0.0409). Concretely the displayed inequality is **false**:
at n=2 the LHS 0.0714 exceeds the claimed bound 0.0529; at n=3, 0.0409 > 0.0171.

*Why it is load-bearing:* `MIX(θ)` (eq 5.3) bounds **only** the 3∤ξ coefficients. Lemma 6.2 uses
Lemma 6.1 to convert that into a full-ℓ² bound and then TV→0. That step is invalid. In fact
**TV(ν,U) ≥ 1/6 for all n** (the mod-3 imbalance alone forces it), so ν can **never** converge to
U in TV — Lemma 6.2's conclusion is not merely unproven, it is *false for the stated reference U*.

*Corrected statement:* Either (i) replace U by the measure that is uniform *within* the mod-3^k coset
structure the offset actually realizes (so the fixed coset masses are not counted as "discrepancy"),
**or** (ii) strengthen MIX(θ) to also control the `3∣ξ` coefficients / the within-coset equidistribution
at every level. Under either fix the "need exponential decay, factor 3^{n/2}" headline can plausibly
be salvaged, but the fix is non-trivial (it changes what MIX must assert) and must be redone — the
lemma cannot be cited as "proved in full" as written. *(Charitable note: Tao's actual Prop 1.17 also
bounds only 3∤ξ, which is consistent with the truth that the 3∣ξ / coset part is handled separately in
his framework — further evidence that the doc's Lemma 6.1 over-claims by folding it into one line.)*

Severity: **blocks-publication for Lemmas 6.1/6.2 specifically** (they are stated as rigorous). The
document's *overall* deliverable (a conditional reduction whose hypothesis is open, plus a negative
finding that the route may fail) **survives and is even reinforced** — but the proof architecture of
Theorem 5.2 must be re-stated to route through the corrected lemma.

**(5d) Minor error — "TV → ∞".** §6.4 (lines ~311–313) writes `‖ν_n−U‖_TV ≈ ½√(0.31n) → ∞`. TV is
≤1 by definition; only the *upper bound* ½√(E_n) goes vacuous (>1). Actual TV saturates (0.167, 0.278,
0.346, 0.371, 0.389…). The conclusion "TV does not →0" is correct; "TV→∞" is a misstatement.
Severity: **minor** (rewrite as "the ℓ²→TV bound becomes vacuous; TV stays bounded away from 0").

**(5e) Minor error — Ramanujan aside at n=1.** Lemma 6.1's parenthetical "Û(ξ)=0 for 3∤ξ" is true for
n≥2 (μ(3ⁿ)=0) but **false at n=1** (c₃(ξ)=μ(3)=−1, so Û(ξ)=−1/φ=−½). Does not affect the asymptotics
or the E_n identity (which uses only ⟨ν,U⟩=1/φ and holds at all n). Severity: **minor**.

**PART-B novelty questions:**
> 1. *Is the conditional reduction "MIX(θ) ⇒ natural density" already in the literature?* Must read
>    **Tao arXiv:1909.03562 (Forum Math Pi 10:e12)** §1 (the transport/Prop 1.7–1.11 region) and §7
>    (Prop 1.17) to (a) confirm the tilt/Esscher mechanism is genuinely new vs. Tao's own remarks, and
>    (b) check the coset handling (does Tao compare to uniform-on-units or to a coset-respecting
>    measure?) — this is exactly the (5c) fix.
> 2. *Is "β=1 is necessary but not sufficient (exact-leading-constant needed)" already known?* Check
>    **Tao's 2020 blog** "Equidistribution of Syracuse random variables …" and any follow-up; the
>    distinction L²-order vs exact-constant may already be folk knowledge.
> 3. The §6.3 claim that no power-saving for the specific 3-adic flow-twisted sum (6.3) is in the
>    literature — verify against **Bugeaud's survey**, **Cluckers–Veys / Igusa local zeta** literature.

---

### Doc 6 — `collatz/theory/cycle_exclusion_explicit.md` (Steiner–SdW–Hercher; two-log vs μ)

**VERDICT: internally-sound on the load-bearing factual/numerical claims; one framing caveat.**

- **De Weger threshold** `0<(K+S)log2−Klog3<2^{−0.158K}`: independently verified — solutions exactly
  at K∈{1,2,3,4,5,6,8,10,15,17,29}; **largest at K=29; none for K≥32** (checked to K=4999). Exact match.
  (Aside: K=30,31 also have no solution, so the threshold is slightly conservative — consistent with
  de Weger's stated "K≥32".)
- Continued fraction of log₂3 = [1;1,1,2,2,3,1,5,2,23,2,2,1,1,55,…] — exact match. All cited magic
  numbers are convergent numerators/denominators (357638239/225644606 with |δ−p/q|≈1.08e-17, etc.).
- Simons m=2 squeeze: K>357638239/(1+δ)≈1.38e8 vs K<86000 ⇒ contradiction — reproduced.
- Hercher bound 1536·2⁶⁰=3·2⁶⁹ — verified. Cycle equation Lemma 1 (2^N>3^K) and the affine derivation
  are correct.
- **Headline correction "the bottleneck is the two-log linear-forms estimate (LMN/Laurent), not
  μ(log₂3)":** the *factual* half — that the published proofs apply a two-log estimate and never use
  μ(log₂3) — is a correct reading of the literature and a legitimate correction to the survey.

**Caveat / potential framing error (the doc hedges it correctly, so not fatal):** The §5.2 *intuition*
for *why* the two-log estimate is "the right tool and μ is the wrong tool" is presented via a slope
comparison (C5b): two-log exponent 0.158K (linear in K) vs μ-bound exponent (μ−1)log₂K (slope→0). A
naive reader could conclude the two-log estimate is a *stronger Diophantine lower bound on |Λ|*. **It
is not:** for large K the μ-based bound |Λ|>c·K^{1−μ} (polynomial decay) is **exponentially LARGER**
than 2^{−0.158K} (exponential decay), i.e. a *stronger* lower bound on |Λ|. So "two-log is stronger
because its exponent is linear in K" is backwards as a statement about Diophantine strength; what is
true is the historical fact that the *proofs use* the two-log form (heights of 2 and 3 enter
separately) and that the de Weger packaging is the operative inequality. **The doc explicitly tags the
"why" as `[CLAIM-UNVERIFIED]` and states it has *not* settled whether a μ-route is possible** — so this
is appropriately hedged, but the slope-comparison presentation invites the wrong inference and should
be reworded. Severity: **needs-caveat.**

- The `[PARTIAL-DEF]` note on circuit-count vs local-minima count (68 vs 76; both → 91/92 for Hercher)
  and the `[PARTIAL-CONST]` flags on LMN's 24.34 / Laurent-2008 constants are honest and appropriate;
  they are exactly the items requiring primary sources.

**PART-B novelty questions:**
> 1. *Confirm the directionality and constants against primaries:* **Simons, Math. Comp. 74 (2005)
>    1565–1572** (the "24.34(log3)²" snippet, Lemma 6, K<86000); **Hercher arXiv:2201.00406**
>    (m≥92, the circuit-averaging "bounds on sums of arbitrary number of terms," and *which* two-log
>    constant Hercher used — LMN-1995 vs Laurent-2008); **Laurent, Acta Arith. 133.4 (2008)** (is its
>    constant actually < 24.34 in the cycle parameter window?). The "new m* > 91 follows immediately if
>    Hercher used the older constant" claim (§6.2) is **entirely contingent on the Hercher PDF** and
>    must not be asserted without it.
> 2. **LMN arXiv/JNT 55 (1995) 285–321** and **Laurent Acta Arith. 66.2 (1994)** to lock the constant
>    24.34, the (log b′+0.14)² structure, and the floor 21 vs 21/D — currently `[PARTIAL-CONST]`.
> 3. *Is the "bottleneck is two-log not μ" correction already standard?* Likely yes among specialists;
>    confirm via **Bugeaud, "Linear forms in logarithms and applications"** and the survey the doc cites
>    — this affects whether the "correction to our own survey" is a genuine contribution or just fixing
>    a local mis-statement.

---

## TABLE OF VERDICTS

| Claim | Verdict | Severity | Primary source to settle novelty |
|---|---|---|---|
| AHS (3−√5)/2 reconstruction | internally-sound | minor (one typo) | AHS 2211.11731 §3; Sawin 2211.11504 §2–3 |
| Vector 1: Δ₂≡0 at product extremizer | internally-sound | needs-caveat (no tensorization) | **Sawin 2211.11504; Cambie 2306.12351; Liu 2306.08824** |
| Vector 2: H(A∩B)≰H(A); 0.4295/0.5 artifacts | internally-sound | minor | Reimer 2003; survey §7 |
| ψ interval-arithmetic certificate | internally-sound | none (genuinely rigorous) | n/a (ψ is peer-reviewed) |
| Tao 3^{n/2} Plancherel exponent | internally-sound | none | Tao 1909.03562 §7 |
| Tao β=1-insufficient / E_n finding | internally-sound | none | Tao 2020 blog |
| **Tao Lemma 6.1 / 6.2 (MIX⇒TV→0)** | **error-found** | **blocks-publication (for these lemmas)** | Tao 1909.03562 §1, §7 (coset handling) |
| Tao "TV→∞" wording | error-found | minor | n/a |
| Tao Ramanujan aside at n=1 | error-found | minor | n/a |
| Cycle de Weger threshold (K=29/none ≥32) | internally-sound | none | de Weger/Simons MC 2005 |
| Cycle "bottleneck = two-log not μ" (fact) | internally-sound | none | Simons 2005; Hercher 2201.00406 |
| Cycle §5.2 "why μ is wrong tool" (intuition) | unverifiable-offline / framing-issue | needs-caveat | Bugeaud survey; Laurent 2008 |
| Cycle "new m*>91 if Hercher used old constant" | unverifiable-offline | needs-caveat (contingent) | **Hercher 2201.00406; Laurent 2008** |

---

## ADVERSARIAL TESTS RUN (for reproducibility)

- ψ-algebra & crossover at 60 digits; Sawin G≥0 grid + fine search; Hessian at (ψ,ψ); **λ-sharpness**
  (bump up ⇒ G<0).
- `certify_psi.py` re-run; **interval certifier stress test** (λ·1.001 ⇒ correctly fails; λ·0.999 ⇒
  certifies) — proves the certificate is not a rubber stamp.
- Independent UC-family enumeration (n=3 full = 121 families; n≤4 = 4389): H(A∪B)≤H(A) always;
  H(A∩B)>H(A) on 35/121; H(∪,∩)>H(A) on 113/121; Δ₂=0 on products, >0 on correlated, ≥0 always;
  abundance ≥ ψ always.
- Independent single-letter constants: AHS→ψ, v2_joint_sym→−⅓ (μ=¾ exact), v2_wrong→0.4295 (boundary).
- Independent Syracuse distribution: E_n reproduced exactly; **mod-3 projection = (0,⅓,⅔) for all n**;
  Lemma 6.1 inequality shown false at n=2,3; TV(ν,U)≥1/6; Ramanujan c_{3ⁿ}(ξ)=−1 at n=1, 0 at n≥2.
- De Weger threshold to K=4999; CF & convergent anchors; Simons m=2 squeeze; tilt s*.
- Test suites: 44/44 Frankl, 61/61 Collatz.

## BOTTOM LINE

Five of six documents are internally sound; their constants, inequalities, and certificates hold up to
adversarial numerical attack, and the ψ interval certificate is genuinely rigorous. **One real
mathematical error**: the Tao-Syracuse Lemmas 6.1/6.2 invalidly discard the permanent mod-3 coset
discrepancy, so "MIX(θ) ⇒ TV→0" is false as stated and ν cannot converge to U in TV — these lemmas,
billed as "proved in full," need to be re-derived against a coset-respecting reference. Plus a handful
of minor blemishes (a "TV→∞" overstatement, an n=1 Ramanujan slip, a typo in Lemma 2, and a
backwards-leaning slope-comparison intuition in the cycle doc — the last three already hedged in-doc).
**The dominant risk is not correctness but novelty/priority**: the only result with a "new observation"
flavor (entropy method caps at ψ within i.i.d. couplings) is very likely already known to Sawin and
others and must be checked against primary sources before any such claim is made.
