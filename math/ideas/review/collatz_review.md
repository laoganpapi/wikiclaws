# Adversarial Review — COLLATZ non-moment idea search

> **Reviewer role:** independent re-score + hard disqualification of the top candidates for
> escaping the proven obstruction (the natural-density barrier in the EXACT non-uniform
> stationary `π_n` of the Syracuse transfer operator `P_n` on `(ℤ/3ⁿ)ˣ`; `χ_{P_n}=λ^{φ−1}(λ−1)`;
> `P_n−Π` nilpotent of index `n`; mod-3 marginal frozen `(0,1/3,2/3)`; `TV(π_n,U)≥1/6`;
> moment / averaging / spectral-radius quantities inert).
>
> **Status:** review only. I re-ran three discriminator probes myself (off-coset Fourier
> decomposition; quadratic-vs-linear phase; residue⟂drift MI at deeper digits). Results below
> are mine, reproduced from the exact kernel in `collatz/experiments/perp_gap.py`.
> Wrote ONLY this file. `[NOVELTY UNVERIFIED]` on all underlying proposals.

---

## 0. Executive verdict (read first)

- **The cluster IS essentially one idea**, and it is sharper to say *why* than the synthesis draft did.
  Representation-theory (graded nilpotent off `V^(1)`), ergodic-E1 (Jordan ladder `im(Nᵏ)=V^(n−k)`),
  and probability-B.2 (3-adic `W` contraction, `v₃(X′−Y′)=v₃(X−Y)+1`) are **literally the same operator
  `N=P_n−Π` viewed three ways** (graded module / image-flag / synchronous coupling). All three live
  **in the residue variable that `P_n` already integrated the drift out of** — so they inherit the same
  "grading is descent-blind" failure the ergodic agent itself flagged (E1 §1.4). They are a *sharper
  restatement* of `perp_gap.md`, not an escape.
- **The two that genuinely try to leave the residue marginal** are ergodic-E2 (residue⟂drift
  disjointness / `Ψ_n(ξ,t)` factorization) and probability-B.4 (joint `(residue,drift)` martingale
  coupling) — these are **the same idea too** (the joint `(residue,drift)` law, Prop 4.2), and they are
  the *only* formulations that touch the real open content.
- **I killed the headline empirical signals of the two most-hyped candidates:**
  1. **Higher-order-additive "42% off-coset quadratic mass" — DEAD.** The off-coset (`3∤ξ`) fraction
     **shrinks** with `n` (74%→42%→30%→23% for `n=2..5`), is **diffuse** (top freq 3.6% at `n=5`),
     and a quadratic phase beats the best linear phase by only ~17–22% at `n=3,4` and by **0% at `n=5`**
     (best quadratic `a=0`, i.e. it *is* linear). There is **no quadratic obstruction to subtract** — the
     42% is the next coset levels (mod 9, 27, …) plus a decaying diffuse tail, exactly failure-mode #2 the
     agent itself flagged. (My probe, §3.1.)
  2. **Ergodic-E2 "I(R;drift)≈0.02 ⇒ near-disjoint" — DEAD as evidence.** That ≈0.02 bits is a
     **mod-3 measurement artifact.** Resolving the residue deeper: `I(res;drift-sign)` is ≈0.02 (mod 3),
     ≈0.09–0.18 (mod 9), ≈0.18–0.40 (mod 27); at full resolution mod 3ⁿ it is **0.30–0.45 bits and does
     not decay** in `n`. Residue and drift are **substantially coupled** — the disjointness the route
     needs is *false*, not "plausibly true." (My probe, §3.2.) The agent admitted it only tested mod 3.
- **Nothing clears the bar to "certified barrier-escaping with a plausible path to a conditional
  natural-density result."** The honest certification is a **conditional / least-dead candidate**:
  **probability-B.4 ≡ ergodic-E2, the joint `(residue,drift)` object**, certified *only* as "the single
  correct target," with a sharpened next experiment (the `Ψ_n(ξ,t)` factorization probe) whose **likely
  outcome, given §3.2, is a clean negative** that converts the open problem into a precise quantitative
  coupling bound. Confidence it yields descent: **low (≈10–15%).**

---

## 1. Scored table (Collatz proposals × 4 axes, 1–5)

Axes: **Esc** = escapes-barrier (engages exact `π_n`/nilpotent grading, not inert on it; make-or-break);
**Con** = concrete (runnable first step / precise statement); **Pl** = plausible (could yield
descent / conditional natural-density, or is killed by the `π_n` ceiling / archimedean–2-adic decoupling);
**Nov** = novel-potential vs folklore.

| Proposal | Esc | Con | Pl | Nov | One-line justification |
|---|---|---|---|---|---|
| **rep-theory** (branch-group contraction off `V^(1)`) | 3 | 4 | 2 | 2 | Sharpest *structural* localization (graded nilpotency; obstruction = one 2-d isotype) — but the named "contracting norm" is the **missing** ingredient, lives in the residue var (descent-blind), and `‖P_n−Π‖₂↗2` is the same wall. |
| **ergodic E1** (Jordan ladder `im(Nᵏ)=V^(n−k)`) | 2 | 4 | 1.5 | 2 | Rigorous & exact, but it is `perp_gap.md` re-graded; agent itself concedes the grading is **descent-blind** (descent is in the 2-adic/size var `P_n` integrated out). Same object as rep-theory. |
| **ergodic E2** (residue⟂drift disjointness / `Ψ_n(ξ,t)`) | 4 | 4 | 2 | 3 | Names the *exact* open content (Prop 4.2 joint law) as a disjointness — genuinely off the residue marginal. **But its encouraging signal (I≈0.02) is a mod-3 artifact; deeper-digit MI is large (§3.2) ⇒ disjointness likely FALSE.** Still the right target. |
| **probability B.2** (3-adic `W` contraction) | 2 | 5 | 1.5 | 2 | The `1/3` contraction is exact and pretty, but it is **literally `N` dropping a 3-adic digit** (= E1) — contracts to the *wrong* target `π_n`, the textbook `perp_gap.md` trap. Inert. |
| **probability B.4** (joint `(residue,drift)` martingale) | 4 | 3 | 2 | 3 | **Same idea as E2.** The only object that keeps the joint law; dodges TV≥1/6 by construction. Killed-or-saved by the same `Ψ_n(ξ,t)` test; §3.2 leans killed. Highest-upside, highest-risk. |
| **higher-order additive** (quadratic `U³` off-coset) | 2 | 4 | 1 | 2 | **Falsified by my probe (§3.1):** off-coset mass shrinks, is diffuse, and carries **no quadratic phase** (Q/L→1 at `n=5`). The 42% is the mod-9/27 coset tower, not `U³` structure — failure-mode #2 the agent flagged is the actual situation. |
| **p-adic/automorphic** (Livšic coboundary of `log3−a log2`) | 3 | 3 | 1.5 | 3 | Correctly names the deepest framing, but reduces to the coboundary/decoupling problem ≈ the conjecture itself; agent's own Step-2 shows easy heights inert. Step-4 (multiplicative harmonics) is a cheap *diagnostic*, not a lever. |
| **poset-topology** (mod-3 obstruction as `H¹` class) | 2 | 3 | 1.5 | 2 | Cohomological *restatement* of Prop 3.1 (`H¹` non-coboundary). Wall-preserving; "enlarge structure group" is undeveloped. |
| **spectral-graph/HDX** (Cheeger of symmetrized `P_n`) | 1.5 | 3 | 1 | 1.5 | A **rate** quantity; obstruction is the *target* `π_n`, not the rate. Agent self-rates 1.5/5; correct. Inert. |
| **matroid/tropical** (min-plus eigenvalue over parity words) | 2 | 4 | 1 | 1.5 | `λ_max=log₂3−1>0` (all-odd climbs); worst-case reformulation, not tool. Min-plus-over-realizable ≡ the conjecture (reformulation). |
| **logic/model-theory** (no monotone-rank proof; RCA₀ delimiter) | 2 | 3 | 1.5 | 3 | A *delimiter* (correct, possibly publishable) — tells you what proof shape *cannot* work, supplies no descent. Non-moment but non-constructive. |

(`sos_lasserre`, `commutative_algebra`, `category_sheaf` are Frankl-only; skimmed — **no Collatz content**.)

---

## 2. One-idea-or-not verdict, and the sharpest formulation

**Yes — but it is two ideas, not one, and the synthesis draft conflated them.**

There are exactly **two distinct objects** in the cluster, and the make-or-break axis separates them cleanly:

### Cluster A — "contract the nilpotent residue tail off `V^(1)`"  (rep-theory ≡ E1 ≡ probability-B.2)
These are **the same operator `N=P_n−Π` in three costumes**:
- E1's image-flag `im(Nᵏ)=V^(n−k)` (lose one 3-adic digit per step),
- rep-theory's graded isotypes `V^(k)/V^(k−1)` (each nilpotent, radius 0),
- probability-B.2's synchronous coupling `v₃(X′−Y′)=v₃(X−Y)+1` (= 3-adic `W` contraction by `1/3`).

The contraction identity `v₃(3(x−y))=v₃(x−y)+1` is *exactly* the statement `N` drops one digit. So
"branch-group contracting norm," "Jordan ladder cochain," and "3-adic Wasserstein contraction" are **one
fact wearing three hats**. **This cluster is INERT.** It lives entirely in the residue variable, which
`P_n` formed by integrating out the drift `D_n` (the size/2-adic variable that actually carries descent).
Contracting it beautifully reaches the *wrong target* `π_n` — the precise `perp_gap.md` §4 trap, and the
exact "grading is descent-blind" failure the ergodic agent honestly flagged (E1 §1.4). **`λ₂^⊥=0` is
already the strongest possible contraction statement and it gives nothing; re-grading it gives nothing.**

### Cluster B — "keep the JOINT `(residue, drift)` law"  (E2 ≡ probability-B.4)
The disjointness reformulation (E2) and the joint martingale coupling (B.4) are **the same object**: the
joint law of `(R_n = X_n mod 3ⁿ, D_n = (Σaⱼ)log2 − n log3)`, which is exactly Prop 4.2 of
`natural_density_obstruction.md`. This is the **only** part of the cluster that leaves the residue
marginal — i.e. the only part that is not automatically inert. It correctly *quotients out* the frozen
mod-3 factor instead of fighting TV→uniform.

**Sharpest formulation:** Cluster B, phrased as E2's **disjointness / factorization** statement —
`Ψ_n(ξ,t) := E[e(ξ R_n/3ⁿ) e^{−t D_n}]` factorizes as `Ψ_n(ξ,0)·Ψ_n(0,t)·(1+o(1))` for all `3∤ξ` at the
Esscher `t*`. It is the most actionable because it is a single, exactly-computable DP, and a power-saving
factorization *would be* the `MIX(θ)`-off-the-coset that the natural-density upgrade needs (sidestepping
the killed Lemma 6.2). B.4's "martingale coupling" is the same content with weaker tooling.

---

## 3. Adversarial stress-test (kill-attempts + survivors)

### 3.1 KILL — higher-order-additive (the "42% off-coset quadratic" claim)

**Kill mechanism: it is the next abelian coset level, not quadratic structure; and it decays.**

My probe (exact `π_n` from `perp_gap.kernel_float`, additive FFT on `ℤ/3ⁿ`, restricted to the units' support):

| `n` | ℓ²-disc(`π_n`,U) | coset mass (`3∣ξ`, ≠0) | off-coset (`3∤ξ`) | off-coset % |
|---|---|---|---|---|
| 2 | 0.07143 | 0.01852 | 0.05291 | **74.1%** |
| 3 | 0.04090 | 0.02381 | 0.01710 | **41.8%** |
| 4 | 0.01937 | 0.01363 | 0.00573 | **29.6%** |
| 5 | 0.00837 | 0.00646 | 0.00192 | **22.9%** |

(The agent's "42% at `n=2`" is actually the **`n=3`** number; at `n=2` it is 74%. Either way the trend is
**downward** — the coset/linear tower increasingly dominates.)

Quadratic-vs-linear discriminator on the off-coset residual (best `|Σ hoff(x) e(−(a x²+b x)/3ⁿ)|`):

| `n` | best LINEAR phase | best QUADRATIC phase | Q/L ratio | best `a` |
|---|---|---|---|---|
| 3 | 0.00934 | 0.01096 | 1.173 | 16 |
| 4 | 0.00219 | 0.00266 | 1.218 | 47 |
| 5 | 0.00053 | 0.00053 | **1.000** | **0** |

And the off-coset mass is **diffuse**: top single off-coset frequency carries 13.8% (`n=3`) → 3.6% (`n=5`)
of off-coset mass; no quadratic peak. **Verdict:** at `n=5` the best "quadratic" phase has `a=0` — it *is*
linear; the marginal Q-over-L gain at small `n` is finite-size noise, vanishing as `n` grows. There is **no
2-step nilsequence to subtract**. The off-coset mass is the projective coset tower (mod 9, 27, …) plus a
diffuse, shrinking high-frequency tail — exactly the agent's own failure-mode #2 ("re-finding mod-9 coset
imbalance, not true quadratic structure"). **DEAD.**

### 3.2 KILL — ergodic-E2 / probability-B.4 encouraging signal ("residue ⟂ drift, I≈0.02")

**Kill mechanism: the ≈0.02 bits is a mod-3-only artifact; the real coupling is large and non-decaying.**

The agent measured `I(R mod 3 ; drift-sign) ≈ 0.02` and read "nearly disjoint." But mod 3 the residue is
slaved to the *single bounded* last valuation `a_n`, which carries almost no information about the `O(n)`-scale
drift — so small MI there is *expected and uninformative*. Resolving the residue to the depth the route
actually needs (my DP from the exact recursion `X′=2^{−a}(3X+1) mod 3ⁿ`, `aⱼ` iid Geom(2)):

| `n` | `I(res mod 3 ; sgn D)` | `I(res mod 9 ; sgn D)` | `I(res mod 27 ; sgn D)` |
|---|---|---|---|
| 3 | 0.0277 | 0.1795 | 0.3996 |
| 4 | 0.0198 | 0.1218 | 0.2622 |
| 5 | 0.0162 | 0.0859 | 0.1755 |

Full resolution `I(res mod 3ⁿ ; sgn D)` across `n`: **0.295, 0.400, 0.451, 0.427, 0.434** bits for `n=2..6`
— **substantial and non-decaying.** The residue at full resolution *is* (a function of) the valuation
sequence `(a₁,…,aₙ)`, and `D_n=(Σaⱼ)log2−n log3` is *also* that sequence — they cannot be disjoint, and the
numbers confirm it. (And `sgn D` is only a 1-bit coarsening of `D`; the `Ψ_n(ξ,t)` the route needs sees the
full real `D`, i.e. *more* coupling.) **The disjointness premise is false at every digit past the first.**
The "encouraging" signal was a measurement artifact of probing only the one digit (`a_n`) that is bounded.
**The empirical support for E2/B.4 is killed.**

**Survivor note:** E2/B.4 are not *refuted as a target* — the joint `(residue,drift)` law is still the
correct object and the obstruction genuinely does not pass through the residue-marginal TV. What is killed is
the claim that disjointness/factorization is *plausibly true*. §3.2 says the honest prior is that
`Ψ_n(ξ,t)` does **not** factorize, i.e. the route most likely produces a **clean negative** (a quantitative
non-disjointness), which is itself valuable: it would pin the natural-density obstruction as a precise
residue–drift coupling rather than a mixing defect.

### 3.3 KILL — rep-theory / E1 / B.2 (Cluster A) as a single object

**Kill mechanism: reduces to spectral-radius-0 (already proven, inert) re-graded; descent-blind.**

- Does it secretly reduce to a spectral-radius/moment statement? **Yes.** `perp_gap.md` already proved
  `λ₂^⊥=0` exactly. Grading the nilpotent `N` by isotypes / by image-flag / by 3-adic balls adds **no new
  scalar** beyond "radius 0," and the agents concede there is no `n`-uniform *norm* contraction
  (`‖P_n−Π‖₂↗2`, nilpotency index `=n→∞`). The "branch-group contracting norm" is named but **not
  constructed**, and is the *exact* missing ingredient `perp_gap.md §4.3` proved absent.
- Does the promised descent live in the variable `P_n` integrated out? **Yes** — `P_n` is the residue
  marginal; descent lives in `D_n` (the size/2-adic variable). B.2 contracts the residue, never `D_n`.
  This is the recurring "grading is descent-blind" failure, conceded by E1 §1.4.
- **Survivor:** as a **structural sharpening** only (obstruction = one 2-d isotype + self-similar tail).
  Zero path to descent on its own. It is the *correct decomposition into which Cluster B must be embedded*,
  not an escape by itself.

### 3.4 Secondary kills (brief)

- **p-adic Step-4 (multiplicative harmonics):** cheap and worth running once as a *diagnostic*, but a single
  bad multiplicative character reproduces the mod-3 obstruction; the deep content (Livšic coboundary of
  `log3−a log2`) is the archimedean–2-adic decoupling = the conjecture. No lever.
- **tropical / HDX / poset-H¹ / logic:** all either reformulations equivalent to the conjecture
  (tropical min-plus, function-field decoupling), rate quantities inert on `π_n` (HDX Cheeger), or
  restatements of Prop 3.1 (poset `H¹`) / delimiters (logic). None engages the joint law. Not certifiable.

---

## 4. CERTIFICATION

**No candidate clears the bar to "genuinely barrier-escaping with a credible path to a conditional
natural-density result."** Honest report. The certified **least-dead / correct-target** candidate, with the
caveat that my own probe (§3.2) leans toward its likely failure:

### Certified candidate: **the joint `(residue, drift)` law** — ergodic-E2 ≡ probability-B.4

**Why it (alone) escapes the barrier mechanism.** The proven obstruction is a property of the **residue
marginal** `π_n` (frozen mod-3 `(0,1/3,2/3)`, `TV≥1/6`, `E_n→∞`) and the inertness of every residue-only
scalar (spectral radius, moment, mixing rate). The joint `(R_n,D_n)` law is *not* a residue-marginal
quantity and is *not* a moment/spectral-radius of `P_n` (which has integrated `D_n` out). It is the one
object `natural_density_obstruction.md` §5 explicitly lists as open ("act on the joint, not the marginal"),
and the disjointness/factorization framing correctly *quotients out* the frozen mod-3 common factor instead
of fighting TV→uniform. The TV≥1/6 ceiling and the archimedean–2-adic decoupling **do not directly apply**
to a factorization statement about `Ψ_n(ξ,t)` at `3∤ξ`.

**EXACT next experiment (the discriminator).** The `Ψ_n(ξ,t)` disjointness-factorization probe:
1. Extend the DP I already wrote in §3.2 (it keeps the full `(residue, S=Σaⱼ)` joint law exactly) to compute
   `Ψ_n(ξ,t) = Σ_{res,S} p(res,S) · e(ξ·res/3ⁿ) · e^{−t(S log2 − n log3)}` for all `3∤ξ`, at the Esscher
   `t* = s*` (`E_{t*}[D_n]=0`), for `n=2..8`.
2. Test the **multiplicative factorization** `R(ξ,t) := Ψ_n(ξ,t) / (Ψ_n(ξ,0)·Ψ_n(0,t))`. Tabulate
   `max_{3∤ξ}|R(ξ,t*)−1|` vs `n`.
   - **Power-saving decay** (`|R−1| ≲ 3^{−θn}`) ⇒ disjointness/`MIX(θ)`-off-coset holds ⇒ a genuine
     *component* of a natural-density argument (still needs the coset-respecting reference glued on). This
     would be the real escape.
   - **Bounded-below `|R−1|`** ⇒ residue and drift are coupled, route fails *as a descent tool* but yields a
     clean, citable quantitative **non-disjointness** theorem (the obstruction is a residue–drift coupling).
3. Stratify by `v₃(ξ)` to localize *where* the coupling lives (my §3.2 predicts it strengthens with depth).

**What would falsify it (and my prediction):** §3.2 already shows `I(R mod 3^k; sgn D)` grows with `k` to
0.3–0.45 bits at full resolution and does not decay in `n`. **Prediction: `max|R(ξ,t*)−1|` is bounded below,
the factorization FAILS, and Cluster B is a negative result.** A falsification of *the barrier-escape* is:
`max_{3∤ξ}|R(ξ,t*)−1| → 0` with a power saving as `n→∞`. I put that at **≈10–15%**.

*(Secondary, cheap, do-first as a sanity gate: p-adic Step-4 multiplicative-character mass of `π_n` — one
line on the existing spectra — to confirm/deny that any harmonic basis sees `π_n` closer to uniform. Expected
negative; if it surprises, re-open.)*

---

## 5. Honest confidence

- **One-idea verdict (two clusters; A inert, B is the only live target):** **high confidence (~85%).**
  The reductions A≡(E1≡rep-theory≡B.2) and B≡(E2≡B.4) are structural identities I can see directly
  (`N` drops a 3-adic digit; the joint law is Prop 4.2 verbatim).
- **Kill of higher-order-additive quadratic route:** **high (~85%).** My probe shows Q/L→1 and diffuse,
  shrinking off-coset mass; the quadratic obstruction does not exist. (Caveat: I tested `e(−(ax²+bx)/3ⁿ)`
  surrogate phases, not full 2-step nilsequences with bracket terms; a GTZ nilsequence could in principle
  hide where my polynomial phase cannot reach — but the *diffuseness* and *decay* argue strongly against any
  low-complexity structure.)
- **Kill of E2's "I≈0.02 ⇒ disjoint" evidence:** **high (~90%).** Deeper-digit MI is unambiguous and the
  mechanism (residue mod 3ⁿ *is* the valuation sequence *is* the drift) is structural.
- **Certified candidate yields descent / conditional natural density:** **low (~10–15%).** Certified as the
  *correct target with the decisive experiment defined*, not as a likely win. My own data lean negative.
- **Overall:** **No candidate is a credible near-term barrier-escape.** The wave's real output is (i) a clean
  structural map (Cluster A = inert sharpening of `perp_gap.md`; Cluster B = the unique live target), and
  (ii) two decisive small experiments (`Ψ_n(ξ,t)` factorization; multiplicative-harmonic mass) that will
  most likely **convert the open problem into a precise residue–drift coupling statement** rather than break it.

### Target for the next wave
Drop Cluster A as an independent line (it is `perp_gap.md` re-graded). Run the `Ψ_n(ξ,t)` factorization probe
to decision. **If it fails (likely):** the next genuinely-new object must act on the **2-adic / size variable
`D_n` directly** — i.e. the Livšic coboundary of `log3 − a log2` on the Lagarias 2-adic shift (p-adic Step-3),
the one place a *pointwise* (non-moment) descent could live. That is the deepest framing and the honest place
the obstruction actually sits (archimedean–2-adic decoupling), even though its prior of existing is low.
