# Adversarial review — FRANKL non-moment generation wave

**Reviewer role:** adversarial re-scorer + kill-team for the Frankl side.
**Date:** 2026-06-03.
**Mandate:** independently re-score all 10 Frankl proposals, try hard to disqualify
the top candidates, certify the single genuinely-barrier-escaping lead (or report
that none clears the bar).
**Verification done this session (re-ran the agents' own probes / re-derived on the
census):**
- `sr_probe_n5.jsonl` re-parsed: cube total-Betti `1,3,7,15,31 = 2^k−1` CONFIRMED
  (non-flat on the cube); homology-load rule fails on **exactly 6** families
  (matches the note — verified via `freq(argmax_x S(x)) ≥ |F|/2`, 6/29738).
- `sos_validate.py` re-run: level-1 incidence SOS ≡ degree-2 frequency-moment cells
  (9/9 at n=2, 37/37 at n=3) CONFIRMED; cube PSD-feasible at level 2 at abundance ½
  for k=1,2,3 CONFIRMED (degree-independent ½ ceiling).
- `sheaf_persistence_probe.py 5` re-run: non-principal heavy fibre ⟹ abundance ≥
  **0.5556**, 0 exceptions / 11886; all abundance-½ families have a principal heavy
  fibre CONFIRMED.
- `matroid_tropical_probe/probe.py` re-run: JI-overlap Gram is PD `(r,0,0)` on every
  family, cube signature `(k,0,0)` — never Lorentzian CONFIRMED.
- `frankl_isotypic.json` re-parsed: **the rep-theory separator is broken** — 245/320
  families have a FLAT non-trivial isotype block yet abundance > ½ (see §Stress-test).

**Barrier recap (the two walls every candidate must clear).**
1. **Moment wall** (`ji_overlap_inequality.md`, `join_irreducible_labelling.md` H5):
   every symmetric convex moment `Σ_x φ(freq(x))` is flat-minimized by the Boolean
   cube at ½; the cube's frequency vector is flat, killing the 2nd-order term.
2. **Cone wall** (`lattice_attack.md` §4): abundance is NOT a function of the abstract
   lattice `L` — `cone(G) ≅ G` as a lattice but abundance jumps ½ → `1−1/|L|`. So any
   invariant of `L` alone is annihilated (fixed while abundance moves).
A genuine escape must (a) not be a symmetric convex moment of freq, (b) not be flat/
degenerate on the cube, and (c) not be a bare lattice invariant. Most candidates fail
(b) or (c); several "escape" only to **relocate** onto the JI-overlap / Poonen quantity
(the irreducible kernel `Σ_{j,k}|↑j∩↑k|`, which the cube pins at ½ exactly).

---

## 1. Scored table (10 Frankl proposals × 4 axes, 1–5)

| # | Proposal | Escapes-barrier | Concrete | Plausible | Novel-pot. | One-line justification |
|---|---|:--:|:--:|:--:|:--:|---|
| 1 | **commutative_algebra** (Alexander-dual / fine Betti) | **4** | **4** | 2 | 3 | The ONLY invariant verified non-flat on the cube (Betti 2^k−1 grows); but the live primal rule relocates to the parasite/max-vs-mean wall (6 failures), and the Eagon–Reiner dual is speculation — escape is real at the *invariant* level, unproven as a *forcing rule*. |
| 2 | **category_sheaf** (principal/non-principal heavy-fibre dichotomy) | 3 | **4** | 2 | 3 | Verified 0-exception non-moment dichotomy (non-principal ⟹ ≥0.5556); but the hard case (½) IS the principal stratum = exactly the Poonen `|↑m|/|L|` quantity. Pure relocation, no new inequality inside the cell. |
| 3 | **sos_lasserre** (level-2 incidence moments) | 3 | 3 | 2 | 2 | Level-2 orbit moments of subset-triples are genuinely NOT freq-moments (barrier theorem literally doesn't cover them); but cube is PSD-feasible at ½ at every level (verified) ⇒ degree-independent ½ ceiling; likely collapses to level-1 by a union-closure tautology (untested — no SDP solver). |
| 4 | **poset_topology** (Möbius / crosscut / Quillen) | 2 | 3 | 2 | 2 | μ_L, χ̃(Cr_JI) non-flat on cube (=(−1)^k) BUT are pure lattice invariants ⇒ cone-killed (μ fixed, abundance 0.5→0.875). Only the T-deleted/Quillen relative complex survives, restricted to a cone-blocked class — uncomputed. |
| 5 | **representation_theory** (Aut(L)-isotype spectral spread) | 2 | 3 | 1 | 2 | Separator "Φ(M)=0 iff cube" is FALSE: 245/320 families have flat non-trivial block yet abundance>½ (verified). Also Aut(L)=1 in 31.5% (decomposition vacuous). Relocates to JI-overlap Gram. |
| 6 | **spectral_graph_hdx** (cover-graph / Hoffman σ₂) | 2 | 3 | 2 | 2 | Cover-graph spectrum non-trivial on cube (escapes Fourier collapse!), corr −0.40; but order-only spectra are lattice invariants (cone-killed); surviving σ₂(B̃) lever is a spectral repackaging of the JI-overlap crux. |
| 7 | **matroid_tropical** (Lorentzian / M-convex) | 1 | 4 | 1 | 3 | Sharp NEGATIVE: JI-overlap Gram is PD (verified, never Lorentzian) ⇒ Hodge-index can't attach, only Cauchy–Schwarz=M₂ survives=barrier. The M-convex-exchange sub-lever lacks a Lorentzian carrier (UC≠matroid). |
| 8 | **logic_model_theory** (definable selector hierarchy) | 2 | 3 | 1 | 2 | Clean delimiter (Level-0 order-only selectors are Aut(L)-invariant ⇒ cone-dead, rigorous EF argument); but the only live "Level-2" selector IS the JI-overlap inequality verbatim. Re-licenses, doesn't bypass. |
| 9 | **probability_nonmoment** (Stein D(x) / join-coupling) | 2 | 3 | 2 | 2 | Antisymmetric kernel D(x), cube = zero of D (boundary not minimum) is a genuinely different degeneracy; but the proposed certificate is unrun, and D(x) most-likely anti-correlates with abundance (V1 parasite pattern) — same risk as every lever. |
| 10 | **higher_order_additive** (Gowers U^k) | 1 | 4 | 1 | 1 | FALSIFIED on data: cube is a coset/subgroup ⇒ U^k-flat (normalized=1, the floor) at EVERY order; U^3 corr 0.21 < U^2 0.31. Barrier STRENGTHENS, doesn't break. |

**Axis notes.** "Escapes-barrier" is graded strictly: 5 would require a verified
non-moment object that is non-degenerate on the cube AND not a relabelled JI-overlap
AND with a candidate forcing mechanism not yet refuted. Nobody earns 5. The cluster at
2 ("escapes the moment wall, dies on the cone wall or relocates to JI-overlap") is the
honest modal outcome and matches `SYNTHESIS_DRAFT.md`'s "everything localizes to the
JI-overlap/Poonen kernel."

---

## 2. Adversarial stress-test of the top 3

### Candidate 1 — commutative_algebra (Alexander-dual / fine multigraded Betti)

This is the SYNTHESIS_DRAFT's headline ("the ONLY cube-non-flat invariant"). I tried
to kill it four ways.

**Kill-attempt A — disguised moment?** *Survives, partially.* The fine Betti `β_{i,A}`
and total Betti are demonstrably NOT functions of the frequency vector: the cube total
Betti `2^k−1` grows with `k` while every symmetric moment of `freq≡|F|/2` is flat
(re-verified: cube sizeF→total_betti = {2:1, 4:3, 8:7, 16:15, 32:31}). So the *invariant*
genuinely lives outside the moment cone. This is the one true clearance of the moment
wall at the invariant level, and it is real.

**Kill-attempt B — cone wall.** *Lands a heavy blow.* The note concedes (§3.1) that
*coarse* (Z-graded / iso-invariant) homology — projdim, reg, total Betti — is a lattice
invariant, hence cone-killed exactly like every other `L`-invariant. So the cube-non-flat
*number* (total Betti) is cone-dead for forcing abundance. The escape can ONLY live in
the **fine multigrading** indexed by actual subsets `A⊆[n]` (the labelling data). That is
the correct call, but it means the headline "cube-non-flat invariant" is the cone-dead
half; the live half is the unproven fine-graded rule.

**Kill-attempt C — relocation / parasite.** *Lands a kill on the concrete rule.* The
note's one concrete fine-graded forcing rule (homology-load `S(x)=Σ_{A∋x}β`, claim
`freq(argmax S) ≥ |F|/2`) fails on exactly 6 families (re-verified: 6/29738). Critically,
the 6 failures are the SAME lopsided "one near-universal element + parasites" shape that
killed the second-moment / JI-overlap lever (`freqs=[16,...]` near-apex + light parasites,
homology concentrated on the wrong elements). So the only RUNNABLE homological rule
relocates verbatim onto the max-vs-mean parasite wall. The §3.2 dictionary makes the
mechanism explicit and unavoidable: the abundant element is a *cone-apex variable*
(divides every generator) which TRIVIALIZES homology — homology is structurally ABSENT
exactly where abundance is. That is a wrong-sign obstruction baked into the primal object.

**Kill-attempt D — does the Alexander dual actually flip the sign?** *Unverified — this
is the entire bet.* The §5 claim is that Eagon–Reiner duality maps "apex = homology-
absent" to "apex = dual-socle-large," undoing §3.2. The note's own leading worry (its
Failure mode 1): duality is an involution, so it may map parasite families to *dual*
parasite families and die the identical death. **Nothing in the probe data tests this** —
the dual resolution / dual socle was never computed. So the certification rests on an
unverified sign-flip.

**What survives:** the *fact* that fine multigraded Betti is non-flat on the cube and
labelling-sensitive (genuine F.2 data, genuinely non-moment). What does NOT survive: any
*forcing rule*. The primal rule relocates to the parasite wall; the dual rule that might
fix it is uncomputed speculation.

### Candidate 2 — category_sheaf (principal/non-principal heavy-fibre dichotomy)

**Kill-attempt A — disguised moment?** *Survives.* `type(F) = "is the argmax fibre
principal"` is a Boolean order-structural property of which element is heaviest; two
families with identical freq multiset can differ in it. Re-verified the dichotomy is
exact: non-principal heavy fibre ⟹ abundance ≥ 0.5556, **0 exceptions / 11886**. Not a
symmetric moment.

**Kill-attempt B — cube degeneracy.** *Survives as a stratification but the cube sits at
the BOTTOM of the principal cell at exactly ½.* The cube is distributive ⟹ all fibres
principal ⟹ it is inside the "representable" cell at ½. So the dichotomy does not collapse
on the cube; it correctly places the cube at the floor of the hard stratum. Good.

**Kill-attempt C — relocation.** *KILL.* This is decisive and the note is honest about it
(§4). On the principal stratum, `Fib(x*) = ↑m` and `μ(Fib(x*)) = |↑m|/|L|` — which is
**exactly the Poonen single-join-irreducible quantity**. And `join_irreducible_labelling.md`
§2 already proved that quantity dips to **0.2353** as a lower bound (H1 FALSE: single-JI
filters do NOT suffice; 2254 families need the *union* to clear ½). So the dichotomy
reduces Frankl-on-its-extremal-stratum to the *known* equivalent Poonen form and adds NO
inequality inside that cell. The non-principal side (≥0.5556) was already the easy side.

**Kill-attempt D — is the 0-exception law a certificate or just on the extremal stratum?**
*Just the stratum.* The 0-exception law only fires on the ≥0.5556 (non-principal) side,
which is automatically safe. It says nothing on the principal side except "= Poonen," the
open kernel. So the certificate content is zero; the structural content is a clean
*localization* of the hard case to Poonen. The aspirational fix (a union-closure-aware
cellular sheaf whose `H¹` controls the principal stratum) is explicitly *not constructed*,
and Finding 3.2 proves the obvious constant sheaf is inert (29679/29723 fibres
contractible).

**What survives:** a verified, non-moment, 0-exception localization of Frankl to "principal
heavy fibres satisfy Poonen." It does not escape — it relocates onto the irreducible kernel
in the cleanest possible language.

### Candidate 3 — sos_lasserre (level-2 incidence moments)

**Kill-attempt A — disguised moment?** *Survives at level ≥2.* Re-verified: level-1
`S_n`-invariant incidence cells coincide exactly with degree-2 frequency-pair cells (9/9,
37/37) ⇒ level-1 IS the barrier. Level-2 orbit moments `L[y_S y_T y_U]` are functions of
subset-TRIPLE orbit types, which provably do not factor through `(freq_i)_i`. The barrier
theorem ("symmetric convex moments of the frequency vector") literally does not cover them.
This is a genuine, non-obvious clearance of the *stated* moment wall.

**Kill-attempt B — cube cap.** *Lands a structural blow (the ½ ceiling).* Re-verified: the
honest 0/1 cube moment vector is PSD-feasible at level 2 at abundance exactly ½ for k=1,2,3
(min_eig ≥ −1.3e-14), and the construction works at every level. So **no Lasserre level can
certify abundance > ½** — every level can at best *reach* ½. This is not fatal for Frankl
(½ is the target) but it means SOS can only be "a proof," never a margin.

**Kill-attempt C — collapse-by-tautology (the relocation risk).** *Untested — the live
worry.* The note's own central worry (Failure mode A): the union-closure equalities
`y_A y_B = y_A y_B y_{A∪B}` may force level-2 triple-moments to be *determined* by pair-
moments modulo the ideal — exactly the way Lemma 3.1 of `ji_overlap_inequality.md`
(`↑a∩↑b=↑(a∨b)`, zero slack) drained the overlap lever. If so, level 2 collapses to level
1 = the barrier, one degree up. **This is the key experiment and it was NOT runnable** (no
cvxpy/MOSEK in sandbox; the alternating-projection solver floors at level 2). So whether
level 2 lifts the lopsided sub-½ families to ½ is genuinely open.

**Kill-attempt D — empirical signal a certificate or parasite?** *N/A — no signal yet.*
Unlike the other candidates there is no computed correlation to be a parasite; the entire
question is the unrun level-2 SDP separation `lb_2 > lb_1` on the 6 lopsided n≤5 families.

**What survives:** a logically-clean statement that level-2 incidence SOS is the *first*
relaxation not pre-collapsed onto the moment barrier, with a precisely-specified decisive
experiment (the `lb_2` vs `lb_1` SDP run) that the sandbox could not execute. The risk
(tautological collapse to level 1) is high but **unfalsified** — which is exactly what
distinguishes it from candidates 1, 2, 5, 7, which are falsified or relocated by data in
hand.

---

## 3. CERTIFICATION

### Certified lead: **sos_lasserre — level-2 (degree-4) incidence-moment SOS**

I certify SOS level-2 as the single most promising **genuinely-not-yet-refuted** lead,
ahead of the SYNTHESIS_DRAFT's pick (commutative algebra). Reasoning, stated against the
make-or-break "escapes-barrier" axis:

**Why it escapes the barrier (precisely).** The proven barrier is a theorem about ONE
explicit low-dimensional invariant sub-algebra: symmetric convex moments of the frequency
vector, i.e. the algebra generated by the linear forms `freq_i = Σ_{S∋i} y_S` (its symmetric
degree-k pieces are the power sums `Σ_i freq_i^k`). I verified the exact identification
**level-1 incidence SOS = this barrier** (the `S_n`-invariant level-1 cells equal the degree-2
frequency-pair cells, 9/9 and 37/37). The level-2 `S_n`-invariant moments `L[y_S y_T y_U]`,
`L[y_S y_T y_U y_V]` are orbit-functions of subset **triples/quadruples**. Symmetry
reduction kills the ground-set *labelling* freedom (the F.2 freedom, the cone's mechanism)
but does NOT lower the subset-configuration degree — these are `S_n`-symmetric yet provably
not moments of `freq`. They live in a strictly larger invariant algebra than the one the
barrier theorem covers. So the escape is not a claim that "this object feels different"; it
is the literal observation that the barrier theorem's hypothesis (frequency-vector moment)
fails to apply.

**Why this is stronger than the alternatives.** Every other candidate is either (i)
falsified/relocated by data already in hand — rep-theory's separator is broken on 245/320
families; matroid's Gram is PD everywhere; category's dichotomy = Poonen exactly; commutative
algebra's only runnable rule relocates to the 6-family parasite wall; Gowers is flat at all
orders — or (ii) cone-dead at the invariant level (poset topology, spectral order-only). SOS
level-2 is the unique candidate whose central failure mode (tautological collapse to level 1)
is **specified but unfalsified**, because the deciding computation needs an SDP solver the
sandbox lacks. It is also the most principled: it is the direct generalization of the
project's own moment-LP, so a clean negative ("level 2 collapses too") is itself a publishable
Lasserre-degree barrier strengthening, and a clean positive is a proof of Frankl(n) for the
tested n.

**Honest caveat on the certification.** SOS level-2 has a *degree-independent ½ ceiling*
(verified): it can only ever *reach* ½, and it shares the cube-saturation property of every
method. So "escapes the barrier" here means "is not pre-collapsed onto the proven moment
barrier," NOT "is guaranteed to break it." The real probability it works is modest (the
union-closure tautology that killed JI-overlap is a live analogue at level 2). I certify it
as the best *lead to test next*, not as a likely proof.

### EXACT next experiment (the decisive probe)

In an environment with `cvxpy` + `MOSEK`/`SCS`:
1. Build the `S_n`-symmetry-reduced level-2 (degree-4) Lasserre SDP (LAS-2) — only ~tens of
   orbit variables after Corollary 2.2 — for n = 3, 4, 5. The scaffold exists in
   `ideas/generation/sos_probe2.py` (level-1 reliable; needs a real SDP backend for level 2).
2. Compute `lb_2(F)` = smallest threshold `t` with LAS-2 feasible, for the **6 specific
   lopsided n≤5 families** where `lb_1` (the barrier) dips to 0.444 — the minimal one being
   `F={∅,{4},{0,1,2,3,4}}` (`ji_overlap_inequality.md` §2, freq `[1,1,1,1,2]`).
3. **Decision rule.** If `lb_2 = ½ > lb_1` on any of these ⟹ genuine separation, the first
   evidence a non-moment relaxation lifts the parasite families ⟹ pursue (extract the dual SOS
   certificate, check if multipliers are n-uniform). If `lb_2 = lb_1` on all ⟹ the union-closure
   equalities forced level-2 triple-moments to be determined by pair-moments (the Lemma-3.1
   analogue) ⟹ SOS collapses to the barrier at degree 4 too ⟹ certify the negative and move on.
   This single run converts the certification to ≥3 or ≤1.5.

### Runner-up: **commutative_algebra — Eagon–Reiner / Alexander-dual fine Betti (§5)**

Certified as runner-up specifically for its §5 dual direction, NOT its primal rule (which is
killed — relocates to the 6-family parasite wall, re-verified). It is the only candidate
besides SOS whose decisive test is unrun and runnable, and it is the only one with a verified
cube-non-flat invariant (Betti 2^k−1). **Exact next step:** the §5.3 script — for all n≤5,
build `Δ_F^∨` (Alexander dual), its SR-ideal, and compute Eagon–Reiner `β_{·,W}` (same
open-interval homology on the *dual* lcm-lattice); test whether the element maximizing dual
top-multidegree socle generators supported away from it is abundant, i.e. whether the 6 primal
failures FLIP to successes under duality. Leading risk (the note's own Failure mode 1, which I
endorse): duality is an involution and may map parasite families to dual-parasite families,
dying identically. ~1-day extension of `sr_probe.py`.

---

## 4. Honest confidence: do we have a real non-moment lead, or a relocated barrier?

**Confidence that we have a genuine, not-yet-relocated non-moment lead: LOW-to-MODERATE
(~30%).** Brutally:

- **7 of 10 candidates are confirmed relocations or kills** (in hand, by data I re-ran):
  category=Poonen exactly; rep-theory separator broken on 245/320; matroid Gram PD everywhere;
  Gowers flat at all orders; poset-topology + spectral order-only are cone-dead lattice
  invariants; logic Level-2 = JI-overlap verbatim. The SYNTHESIS_DRAFT's read — "everything
  localizes to the JI-overlap / Poonen kernel on cone-blocked lattices" — is CORRECT and if
  anything the review hardens it: the irreducible kernel `Σ_{j,k}|↑j∩↑k|` (cube-pinned at ½,
  parasite-undercut below) is where six independent fields land.

- **Only 2 candidates have an unfalsified escape, and both are bets, not results.** SOS level-2
  genuinely sits in a larger invariant algebra than the barrier covers (verified), but its
  collapse-to-level-1 risk is the exact Lemma-3.1 tautology that has killed every overlap
  lever — untested only because the sandbox lacks an SDP solver. Commutative-algebra fine Betti
  is verifiably non-flat on the cube, but its only runnable rule relocates to the parasite wall
  and the dual sign-flip is uncomputed.

- **The recurring parasite (the 6-family / max-vs-mean lopsided structure) is the real adjudicator
  and it has so far defeated every empirical signal that got computed.** It killed the homology-
  load rule (6 failures), it is what level-2 SOS must lift (untested), and it is the precise
  thing the category/rep/matroid relocations inherit. Any candidate whose "0-exception law" or
  "correlation" was actually computed turned out to either avoid the parasite by only firing on
  the safe side (category's ≥0.5556) or to fail on it (commutative algebra). No computed
  certificate survives the parasite.

**Bottom line.** We do NOT yet have a non-moment lever that demonstrably escapes — we have one
genuinely-uncovered-by-the-barrier formalism (level-2 SOS) whose decisive test could not be run,
and one verified non-flat-on-cube invariant (fine Betti) whose forcing rule is broken pending a
dual fix. Both are worth exactly one experiment each (the SDP run; the Alexander-dual socle
script). If both come back negative — level-2 SOS collapses to level 1, and Alexander duality
relabels rather than flips the parasite — then the project has exhausted the "single new invariant
/ relaxation" strategy, and a **second generation wave should target the kernel directly**: an
inequality that bounds the **max-vs-mean spread** (= true abundance minus the fibre power-mean)
from above using union-closure, restricted to the **cone-blocked (upper-semimodular / geometric)
class** where the cone construction is structurally forbidden — the one place
`lattice_attack.md` §5.2, `poset_topology.md` §5, and `join_irreducible_labelling.md` §6 all
independently point and where the parasite families cannot be constructed. That is the honest
recommendation: stop hunting for a magic non-moment invariant on all lattices, and attack the
overlap kernel on the restricted class where it is not free.

**Novelty note:** all framings reviewed carry `[NOVELTY UNVERIFIED]` (arXiv 403 this session);
I did not and cannot verify prior art. The SOS level-1-is-the-barrier identification and the
Alexander-dual abundance target are the two framings I judge least likely to be exact folklore,
but this is an assessment, not a verification.
