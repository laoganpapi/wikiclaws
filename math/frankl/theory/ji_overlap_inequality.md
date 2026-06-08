# The JI-filter overlap inequality: the exact crux, and why it is FALSE in general

**Author:** Alex Ye (no AI on author line).
**Date:** 2026-06-03.
**Status:** `[NOVELTY UNVERIFIED — the fibre 2nd-moment identity Σ_x|Fib(x)|² =
Σ_{A,B}|A∩B| is classical double-counting (= second_moment.md Identity 1.1
restricted to the lattice L); the JI-overlap framing is flagged new but very
likely folklore. arXiv 403 this session.]`
**This is an OBSTRUCTION + a sharp residual-gap characterization — NOT a proof.**
**No proof of Frankl is claimed. No constant > ½ is claimed.**
**Companion code:** `frankl/experiments/ji_overlap.py`.
**Data:** `frankl/experiments/data/overlap_n{0..5}.jsonl`, `overlap_summary.{txt,json}`,
`overlap_counterexamples.txt`.
**Cross-ref:** `join_irreducible_labelling.md` §6 (Candidate 6.1, the lever this
note RESOLVES); `second_moment.md` (the F×F second moment; this is its
fibre/lattice incarnation); `lp_duality.md` §6 (max-vs-mean); `shared/dead_ends.md`
(my entry below; the 0.43/0.5 and 0.444 power-mean traps).

> **One-paragraph verdict.** The 28-agent convergence pinned the crux as a
> lower bound on the join-irreducible filter overlap `Σ_{j,k}|↑j∩↑k|` that would
> force a heavy fibre via Cauchy–Schwarz. This note states that inequality
> **exactly**, tests it on all 29 723 UC families (n≤5), and finds it is
> **FALSE**: it fails on 6–12 families (depending on |F| vs |L| normalization),
> *every one with true abundance strictly above ½*. Two structural facts explain
> the failure decisively: **(i)** the brief's "structured overlap" `↑j∩↑k ⊇
> ↑(j∨k)` is in fact an **exact identity** `↑j∩↑k = ↑(j∨k)` in *every* lattice
> (a tautology of the join), so it supplies **zero slack** to exploit; **(ii)**
> the fibre second moment `Σ_x|Fib(x)|²` equals `Σ_{A,B∈L}|A∩B|` exactly, so the
> JI-overlap lever **is** the raw second-moment lever of `second_moment.md`, which
> already caps at ½ and dips to 0.444 on the same lopsided families. The cube
> saturates the target with **exact equality** (slack 0), consistent with
> cube-uniqueness. **This is the final wall for the second-moment / overlap family
> of levers, not a path through it.** The residual gap is characterized precisely
> in §4.

All numbers validated on **all 29 723 UC families with |F|≥2, n≤5**.

---

## 1. The exact overlap ↔ abundance identity (Task 1)

Fix `F` union-closed, adjoin `∅` so `L=(F,⊆,∪)` is a lattice, `|L|=m`,
top `T=⋃F`. For `x∈[n]` the fibre `Fib(x)={A∈L: x∈A}` is a filter (up-set), and
`freq(x):=|Fib(x)|`. Two moments of the fibre-size vector:
$$
P_1 := \sum_{x} |\mathrm{Fib}(x)| = \sum_{A\in L}|A|, \qquad
P_2 := \sum_{x} |\mathrm{Fib}(x)|^2 .
$$

> **Identity 1.1 (the whole game — fibre 2nd moment = total overlap).**
> $$
> P_2 \;=\; \sum_{x}|\mathrm{Fib}(x)|^2 \;=\; \sum_{(A,B)\in L\times L} |A\cap B| \;=:\; \mathrm{OVL}(L).
> $$
> **Proof.** `|Fib(x)|² = #{(A,B): x∈A, x∈B}`. Sum over `x` and swap order:
> `Σ_x #{(A,B): x∈A∩B} = Σ_{A,B} #{x: x∈A∩B} = Σ_{A,B}|A∩B|.` □
> *(Verified as exact-integer equality, **0 violations / 29 723**;
> `ji_overlap.py` asserts `P2 == OVL` per family.)*

This is exactly `second_moment.md` Identity 1.1, now read on the **lattice** `L`
(with the bottom adjoined) and on the **fibre** vector rather than the raw
frequency vector. (They agree because `∅` contributes 0 to every `|A∩B|` and to
every `|A|`, so adjoining the bottom changes neither side.)

### 1.1 The inclusion–exclusion derivation the brief demands

The brief stresses: `Fib(x)` is a **union of filters** `Fib(x)=⋃_{j∈JI, x∈j}↑j`
(reconstruction `(R)`, verified 0 violations), so expanding `Σ_x|Fib(x)|²`
*should* bring in the overlaps within each fibre. It does — and the bookkeeping
**collapses to Identity 1.1** because of a tautology. Writing `J(x)={j∈JI: x∈j}`,
$$
|\mathrm{Fib}(x)|^2 = \Big|\bigcup_{j\in J(x)}{\uparrow}j\Big|^2,
$$
and inclusion–exclusion on the union *inside* the square is the standard
$$
\Big|\bigcup_{j\in J(x)}{\uparrow}j\Big| = \sum_{\emptyset\ne S\subseteq J(x)} (-1)^{|S|+1}\Big|\bigcap_{j\in S}{\uparrow}j\Big|,
\qquad
\bigcap_{j\in S}{\uparrow}j = {\uparrow}\!\Big(\bigvee_{j\in S} j\Big).
$$
The intersection identity `⋂_{j∈S}↑j = ↑(⋁ j)` is the key (Lemma 2.1). But we
do **not** need to carry the alternating sum: Identity 1.1 already evaluates
`Σ_x|Fib(x)|²` in closed form as `OVL(L)`. The inclusion–exclusion is the
*explanation* of where the overlaps live; Identity 1.1 is the *value*.

### 1.2 The power-mean bridge to abundance — the SUFFICIENT inequality

The weighted-by-itself (power-mean) bound over ground elements `x`:
$$
\max_x |\mathrm{Fib}(x)| \;\ge\; \frac{\sum_x |\mathrm{Fib}(x)|^2}{\sum_x |\mathrm{Fib}(x)|} \;=\; \frac{P_2}{P_1} \;=\; \frac{\mathrm{OVL}(L)}{\sum_{A\in L}|A|}.
$$
Frankl (lattice form) asks `max_x|Fib(x)| ≥ |L|/2`. So a **sufficient** overlap
inequality is:

> **Target inequality (L-normalized).**
> $$
> \boxed{\ \mathrm{OVL}(L)=\sum_{(A,B)\in L\times L}|A\cap B| \;\ge\; \frac{|L|}{2}\sum_{A\in L}|A|\ }
> \tag{TARGET-L}
> $$
> equivalently `2·OVL ≥ |L|·P₁`. The family-normalized version (abundance `=
> max freq/|F|`, threshold `|F|/2`) is `2·OVL ≥ |F|·P₁` **(TARGET-F)**, identical
> in `OVL,P₁` but with the smaller threshold when `∅∉F` (so TARGET-F is the
> *weaker* ask; TARGET-L the stronger).

This is **precisely** Candidate 6.1 of `join_irreducible_labelling.md` made
quantitative, and **precisely** the `lp_duality.md` §6 / `second_moment.md`
second-moment lever, now localized to the fibre/lattice overlap. The hoped-for
chain was: *overlap lower bound (TARGET) ⇒ power-mean ⇒ abundance ≥ ½, tight on
the cube.* The power-mean step and the cube-tightness are real (§3). **The
overlap lower bound itself is false (§2).**

---

## 2. The target overlap inequality is FALSE (Task 2)

> **Finding 2.1 (decisive).** Over all 29 723 UC families (n≤5):
> - **TARGET-L** `2·OVL ≥ |L|·P₁` **FAILS on 12 families** (holds on 29 711).
> - **TARGET-F** `2·OVL ≥ |F|·P₁` **FAILS on 6 families** (holds on 29 717).
>
> The power-mean density `(P₂/P₁)/|L|` dips to **0.4444 < ½** (min over families),
> reproducing the 0.444 of `lp_duality.md` §6 and `second_moment.md` §3 — now as
> a *fibre-overlap* quantity. *(`overlap_summary.txt`.)*

> **Finding 2.2 (the residual gap is entirely above ½ — harmless but useless).**
> **Every** TARGET failure has **true abundance ≥ 0.5714 > ½**. There is **no**
> failure at abundance ≤ ½. *(`overlap_summary.txt`, `overlap_counterexamples.txt`.)*
> - **Harmless:** the inequality never fails on a would-be counterexample
>   (abundance-½ family), so its failure cannot produce a false refutation.
> - **Useless:** `2·OVL ≥ |F|·P₁` is genuinely false, so it cannot be a
>   certificate. The cube pins it at equality; lopsided families undercut it.

**The minimal / sharpest counterexample.**
$$
F=\{\emptyset,\{4\},\{0,1,2,3,4\}\}\quad(\text{masks }[0,16,31],\ n=5).
$$
Frequency vector `[1,1,1,1,2]`: a near-universal heavy element `4` plus four
*parasitic* elements `0,1,2,3` each in a single member. Then `P₁=Σ|A|=6`,
`P₂=OVL=8`, power-mean `=P₂/P₁=8/6=4/3`, density `=(4/3)/3 = 4/9 = 0.444 < ½`,
while **true abundance `=2/3 > ½`**. This is the *same* lopsided structure that
defeated the LP averaging certificate (`lp_duality.md` §5, the 6 sub-½ families)
and the raw second moment (`second_moment.md` §3) — the second moment is dragged
down by the parasites while the max is held up by the heavy element. The overlap
re-derivation **inherits the identical failure family**, as it must (§3.2).

---

## 3. Why it fails — two structural collapses (Task 3, and the red-team)

I did **not** obtain a proof of TARGET; the data refute it. The interesting
content is *why* the structured-overlap idea cannot work, which kills the lever
cleanly rather than leaving it open.

### 3.1 The "structured overlap" `↑j∩↑k ⊇ ↑(j∨k)` is an EXACT identity (no slack)

The brief's central hope was that `↑j∩↑k ⊇ ↑(j∨k)` (the join `j∨k∈L` since `L`
is a lattice) gives a *structured lower bound* on overlaps that union-closure can
exploit. But:

> **Lemma 3.1 (tautology).** In **any** lattice, for **any** `a,b`,
> $$
> {\uparrow}a \cap {\uparrow}b \;=\; {\uparrow}(a\vee b)\quad\text{(equality, not just ⊇).}
> $$
> **Proof.** `x∈↑a∩↑b ⟺ a≤x ∧ b≤x ⟺ a∨b≤x ⟺ x∈↑(a∨b)`, the middle step being
> the *definition* of the join. □ *(Verified: **0 violations / 25 668 pairs**
> over all `(a,b)` pairs in all lattices n≤5, not just JI pairs;
> `ji_overlap.py` cross-check.)*

Consequently the "structured" overlap sum equals its own lower bound **exactly**:
$$
\mathrm{JIOVL}:=\sum_{(j,k)\in JI^2}|{\uparrow}j\cap{\uparrow}k| \;=\; \sum_{(j,k)\in JI^2}|{\uparrow}(j\vee k)| \;=:\; \mathrm{JIOVL\_lb}
$$
on **all 29 723 families** (ratio `JIOVL/JIOVL_lb ≡ 1.0000`; **0 families** with
strict inequality). **The `⊇` the brief hoped to leverage has empty slack.** The
join structure tells you the overlap *exactly*; it gives nothing to bound *below*
that union-closure could amplify. This is the first reason the lever degenerates.

### 3.2 The JI-overlap lever IS the raw second moment (no localization gain)

The fibre second moment is `P₂ = OVL(L) = Σ_{A,B∈L}|A∩B|` (Identity 1.1). This is
*exactly* the `second_moment.md` object `M₂=Σ_{A,B∈F}|A∩B|` (the bottom `∅` adds
nothing). So the "localized to the JI-labelling" overlap lever and the raw
second-moment lever are the **same inequality**. Everything `second_moment.md`
proved transfers verbatim:
- the cube minimizes the power-mean ratio at its `(m,P₁)` parameters (pinned at ½);
- the raw ratio dips to 0.444 on lopsided families at abundance `>½`;
- union-closure supplies no second-moment lower bound beyond Cauchy–Schwarz.

The JI/fibre re-framing did **not** add a new constraint; it re-expressed the same
quantity. The hoped-for "localization gain" does not exist, *because* of Lemma 3.1:
the only place JI-structure could have entered (the overlaps) is pinned to an exact
value by the join.

### 3.3 Red-team: the cube must saturate with EQUALITY — and it does

The brief's hard test: *any* purported proof giving the cube slack is broken. Here
TARGET is **false**, so the question is the converse — does the cube at least sit
on the boundary (slack 0)? It must, by the cube-uniqueness result (H5).

> **Finding 3.2 (cube saturation, verified).** For `2^{[k]}`, `k=1..5`:
> `2·OVL − |L|·P₁ = 0` and `2·OVL − |F|·P₁ = 0` **exactly** (cube slacks `[0]`).
> All 63 abundance-½ families (L-norm) / 39 (F-norm) satisfy TARGET with **exact
> equality**. *(`overlap_summary.txt`, "DECOUPLING CHECK".)*

So the cube is on the knife-edge `OVL=(|L|/2)P₁`, as required. The failure of
TARGET is **strictly on the high-abundance side** (Finding 2.2): the inequality is
not "the cube + ε is broken" (which would be catastrophic) but "lopsided families
above ½ have *less* overlap than `(|L|/2)P₁`, which is fine because their max is
carried by a single heavy element, not by overlap." The variance/overlap functional
is *minimized* at the flat cube and the parasitic families undercut it — exactly the
`second_moment.md` Lemma 2.2 mechanism. **No step here proves Frankl; there is no
proof to break.** The discipline check (cube tight, no sub-½ false alarm) passes.

---

## 4. The precise residual gap (Task 4)

The lever fails on `R := {F : 2·OVL < |F|·P₁}` (6 families n≤5; the L-version 12).
Characterize `R` exactly:

> **Characterization 4.1 (the gap set).** `F∈R` ⟺ the fibre-size vector
> `(freq(x))_x` is **spread** enough that its power mean `P₂/P₁` falls below
> `|F|/2`. Equivalently (Cauchy–Schwarz equality analysis), `R` is the set of
> families whose frequency vector is **far from flat** — one or few heavy
> coordinates (`freq≈|F|`) plus several light *parasitic* coordinates
> (`freq` small). All 6 n≤5 witnesses have this shape: a near-universal element
> plus low-frequency elements (the FUCC-cone-like families). For these the
> **max** is carried by the single heavy coordinate, *not* by the overlap mass,
> so the power-mean lower bound is loose by exactly the spread `max−mean`.

> **Characterization 4.2 (the gap is exactly max−mean, again).** The deficiency
> `|F|/2 − P₂/(P₁) ` (when positive) is the same max-vs-mean spread that
> `lp_duality.md` §6 isolated. The overlap reformulation does **not** shrink it:
> `P₂/P₁` is a *mean* (weighted by fibre size) and Frankl needs the *max*. On
> flat families (cube) mean = max = ½ (lever tight); on spread families
> mean < ½ < max (lever loose). The residual gap is precisely the spread, and the
> overlap identity provides no new upper bound on it.

So the residual gap is **not** closed and is **not** closeable by this lever: it is
the project's recurring max-vs-mean wall, re-derived a seventh way (after entropy,
polynomial, lattice-invariant, Fourier, shadow, LP, second-moment). The
JI-overlap is the **eighth delimited method**, and it coincides with the
second-moment method by Identity 1.1 + Lemma 3.1.

---

## 5. Brutally honest assessment (Task 5)

**This is the final wall for the overlap / second-moment family of levers, not a
path to a proof.** Concretely:

1. The exact identity `Σ_x|Fib(x)|² = Σ_{A,B∈L}|A∩B|` is clean, classical, and
   verified (0 violations). It is the correct overlap↔abundance bridge.
2. The overlap lower bound that would close Frankl, `2·OVL ≥ |F|·P₁` (TARGET-F),
   is **FALSE** — 6 explicit counterexamples n≤5, all at abundance > ½.
3. The brief's structural hook `↑j∩↑k ⊇ ↑(j∨k)` is an **exact identity**
   (Lemma 3.1), so it has **no slack**: the JI-overlap equals the raw second
   moment (Identity 1.1), inheriting all of `second_moment.md`'s obstructions.
4. The cube saturates TARGET with **exact equality** (slack 0), consistent with
   cube-uniqueness; the failure is strictly above ½ (harmless but useless).
5. The residual gap is the **max-vs-mean spread**, the project's recurring wall,
   not reduced by the overlap reformulation.

**Could the lever be rescued?** Only by an inequality that bounds the *spread*
(max−mean) from above, or that lower-bounds `OVL` using *more than* the join
structure (which is exhausted by Lemma 3.1). The natural union-closure facts on
`OVL` are upper bounds (`|A∪B|≤|T|`), wrong sign (`second_moment.md` §4). The honest
position: **the second-moment / overlap direction is closed.** A genuinely new
ingredient (not a moment of the frequency/fibre vector, since every symmetric
convex moment is flat-minimized by the cube) is required. The value of this note is
**negative and sharp**: it converts the "single most promising lever" (Candidate
6.1) into a *characterized dead end* with an explicit minimal counterexample and a
one-line tautological reason (Lemma 3.1) the structure cannot help.

`[NOVELTY UNVERIFIED]` on all framings. No proof of Frankl. No constant > ½.

---

## 6. Reproduction

```
cd math/frankl/experiments
python3 ji_overlap.py 5      # -> data/overlap_n{0..5}.jsonl, overlap_summary.{txt,json}
```

**Step-1 (computational): PASS.** 29 723 families n≤5.
- Identity `P₂ = OVL = Σ_{A,B}|A∩B|`: **0 violations** (asserted exact).
- Reconstruction `Fib(x)=⋃_{j:x∈j}↑j`: 0 violations (cross-check).
- `↑a∩↑b = ↑(a∨b)`: 0 violations / 25 668 pairs (Lemma 3.1, exact identity).
- TARGET-F false on 6, TARGET-L false on 12; all failures at abundance > ½.
- Cube slack `= 0` exactly (k=1..5); min power-mean density `0.4444`.

**Steps 2–4 (red-team / Lean / human): N/A — no theorem is claimed.** The
deliverable is an obstruction: the precise sufficient overlap inequality, its exact
counterexamples, the tautology that drains the structural hook, and the residual
max-vs-mean gap. `[NOVELTY UNVERIFIED]`.
