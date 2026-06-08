# Literature Survey: Frankl's Union-Closed Sets Conjecture

**Authors:** Alex Ye with Claude
**Compiled:** 2 June 2026
**Status:** Working draft for Phase 2 (theory + computation tracks).

> **Verification discipline used in this document.** Every numerical constant, theorem statement, and attribution below was checked against the arXiv abstract page, the published version, or a contemporaneous secondary source (Kalai's blog, Aldridge's blog, Cambie's survey, the Bruhn–Schaudt survey). Items I could not independently verify are flagged `[UNVERIFIED]`. No fabricated citation has been included.

---

## 1. The Conjecture and Equivalent Formulations

### 1.1 The set-theoretic statement

A family `F` of finite sets is **union-closed** if `A, B ∈ F ⇒ A ∪ B ∈ F`. The **Frankl Union-Closed Sets Conjecture (FUCC)**, attributed to Péter Frankl (1979), asserts:

> For every finite union-closed family `F ≠ {∅}` there exists an element `x` of the ground set such that `x` belongs to at least `|F|/2` members of `F`.

The conjecture first appeared in print in Duffus's question after a 1984 conference (it spread initially by word of mouth and through Rival's *Graphs and Order* problem session). See the surveys of Bruhn–Schaudt and Cambie below for the historical thread.

### 1.2 Lattice formulation (Poonen 1992; Abe 2000)

**Poonen (1992)** translated FUCC to lattice theory:

> Every finite lattice `L` with `|L| > 1` contains a **join-irreducible** element `j` such that `j ≤ x` for at most `|L|/2` elements `x ∈ L`.

Poonen proved equivalence (his Theorem 4) and verified FUCC for several lattice classes (distributive, geometric, complemented, and certain size restrictions). **Abe (2000)** independently formulated the lattice version and proved it for **modular** lattices. **Reinhold (2000)** then proved it for **lower semimodular** lattices, the strongest such class to date. The lattice formulation underlies the most recent structural work, including Bouchard (arXiv 2503.00277, 2025), which extracts necessary conditions on a minimum-size counterexample in the lattice setting.

### 1.3 Graph formulation (Bruhn–Charbit–Schaudt–Telle 2015)

In *European J. Combin.* **43** (2015) 210–219, Bruhn–Charbit–Schaudt–Telle showed FUCC is equivalent to:

> In every finite bipartite graph `G` with at least one edge, there are two adjacent vertices each belonging to at most half of the maximal stable sets of `G`.

They proved the graph formulation for chordal bipartite graphs, subcubic bipartite graphs, bipartite series-parallel graphs, and bipartitioned circular interval graphs. (For non-bipartite graphs the statement is trivial.)

---

## 2. Pre-2022 Quantitative Bounds

Let `c(F) = max_x |{A ∈ F : x ∈ A}| / |F|` denote the best frequency. FUCC says `c(F) ≥ 1/2`.

### 2.1 Knill (1994) and Wójcik (1999): logarithmic bounds

**Knill** (arXiv math/9409215; *Graph Generated Union-Closed Families*) gave the first non-trivial bound: there exists `x` belonging to at least `(|F|−1)/log₂|F|` sets, i.e., `c(F) ≳ 1/log₂|F|`. **Wójcik** (*Discrete Math.* **199** (1999), 173–182) refined this and conjectured that the minimum average-set density tends to `(1+o(1)) log₂ n / (2n)`. Both bounds go to 0 as `|F|→∞`, so they are *qualitatively weaker* than any constant lower bound.

### 2.2 Reimer (2003): average set size

**Reimer**, *An average set size theorem*, *Combin. Probab. Comput.* **12** (2003) 89–93:

> For any union-closed family `F`, the average set size `(1/|F|) Σ_{A∈F} |A| ≥ ½ log₂|F|`.

The result is sharp on power sets `2^[n]`. It is most useful when *combined* with other constraints (e.g., bounded ground-set size).

### 2.3 Bošnjak & Marković (2008): ground-set bound

**Bošnjak–Marković**, *The 11-element case of Frankl's conjecture*, *Electron. J. Combin.* **15(1)** (2008) #R88:

> FUCC holds whenever the ground set has at most 11 elements.

I.e., any counterexample must have `|⋃ F| ≥ 12`. Vučković–Živković (*IPSI BgD Trans.* **13** (2017) 65–71) later pushed the threshold to **12**, by computer assistance.

### 2.4 Roberts–Simpson (2010): family-size bound

**Roberts & Simpson** (*Australas. J. Combin.* **47** (2010) 265–267):

> Any counterexample has `|F| ≥ 4q − 1` where `q` is the minimum union size, hence at least **47** sets.

(The "Frankl proven for ≤ 46 sets" folk version originates here.)

### 2.5 Czédli–Maróti–Schmidt (~2009), Balla–Bollobás–Eccles (2013): averaging / large families

**Balla–Bollobás–Eccles**, *Union-closed families of sets*, *J. Combin. Theory A* **120** (2013) 531–544:

> If `|F| ≥ (2/3) · 2^n` (where `n` is the ground-set size), then FUCC holds.

They determined the exact minimum-average-set-size of an `m`-element union-closed family on `[n]`, settling a conjecture of Czédli–Maróti–Schmidt.

### 2.6 Karpas (2017): families of density ≥ 1/2

**Karpas**, *Two results on union-closed families*, arXiv:1708.01434 (2017):

> There is an absolute constant `c > 0` such that any union-closed family `F ⊆ 2^[n]` with `|F| ≥ (1/2 − c) · 2^n` satisfies FUCC.

Proof technique: discrete Fourier analysis on the Boolean cube — the first time Fourier methods played a role in this problem. (See Kalai's blog posts of 26 Dec 2017 and 9 March 2018.) Karpas also proved that if every set outside `F` covers at most one set in `F`, FUCC holds.

### 2.7 FC-families (Poonen, Morris, Marić et al.)

A family `B ⊆ 2^[m]` is an **FC-family** if every union-closed family containing `B` has an element of one of its sets appearing in ≥ |F|/2 members. Successive computational efforts (Poonen 1992; Morris 2006; Marić–Živković–Vučković 2012; Marić 2019 with full Isabelle/HOL verification for `m=6` — arXiv:1902.08765) have enumerated FC-families to prune the search space.

---

## 3. The Gilmer Breakthrough (November 2022)

### 3.1 Gilmer's main theorem

**Gilmer**, *A constant lower bound for the union-closed sets conjecture*, arXiv:2211.09055 (16 Nov 2022).

> **Main theorem.** For every nonempty union-closed family `F ⊆ 2^[n]`, there is an element `i ∈ [n]` contained in at least a `0.01` fraction of the sets of `F`.

The constant `0.01` is *not optimized*. Gilmer's deeper contribution is the **information-theoretic strengthening** he proves:

> **Theorem (info-theoretic form).** Let `A, B` be i.i.d. samples from a distribution on `2^[n]`. If `Pr[i ∈ A] ≤ 0.01` for every `i ∈ [n]`, then `H(A ∪ B) ≥ 1.26 · H(A)`.

Combined with the obvious upper bound `H(A ∪ B) ≤ H(A,B) = 2H(A)` for `A,B` independent, this forces a constant lower bound on `max_i Pr[i ∈ A]`. The bridging combinatorial step says: if `F` is union-closed and `A` is uniform on `F`, then `A ∪ B` is supported on `F`, so `H(A ∪ B) ≤ log|F| = H(A)`, contradicting the above unless some marginal `Pr[i ∈ A]` is bounded away from 0.

### 3.2 Core technique

The crucial **per-coordinate entropy inequality** (Gilmer's Lemma 3):

> For `0 ≤ p, q ≤ 1`: `h((1−p)(1−q)) ≥ (1/(2(1−ψ))) · ((1−q) h(p) + (1−p) h(q))`,
> where `h` is binary entropy and `ψ = (3 − √5)/2`.

The proof proceeds coordinate-by-coordinate using the chain rule plus this inequality. Gilmer conjectured that, with the *sharp* form of the per-coordinate inequality, his method should yield the constant `ψ = (3 − √5)/2 ≈ 0.38197`. He also stated a stronger conjecture (an inequality on KL divergences) which, if true, would have implied FUCC outright.

### 3.3 What was new

Prior bounds were qualitatively `o(1)` (Knill, Wójcik) or required structural restrictions (Karpas, Balla–Bollobás–Eccles, Roberts–Simpson, Bošnjak–Marković). Gilmer's method is the first **dimension-free**, **unconditional**, **constant** lower bound. The proof is short (≈3 pages) and entirely information-theoretic.

---

## 4. The November 2022 "Five-paper rush" to `(3 − √5)/2`

Within one week of Gilmer's posting, four independent works (three on 21 Nov 2022, one on 23 Nov 2022) verified Gilmer's conjectured limit `ψ = (3 − √5)/2 ≈ 0.38197`:

### 4.1 Sawin (arXiv:2211.11504, 21 Nov 2022, final v3 19 Jun 2023)

**Will Sawin**, *An improved lower bound for the union-closed set conjecture*:

> **Theorem.** Every nonempty union-closed family `F ⊆ 2^[n]` has an element of frequency `≥ (3 − √5)/2`.

He replaces Gilmer's Lemma 3 by a sharp version. He *also* proves that the constant `(3 − √5)/2` is *not* the limit of the entropy method: he sketches a refinement using non-i.i.d. couplings producing a constant `> ψ`. Finally, Sawin disproves the stronger KL-divergence conjecture of Gilmer (a related disproof was found independently by D. Ellis).

### 4.2 Chase & Lovett (arXiv:2211.11689, 21 Nov 2022)

**Zachary Chase & Shachar Lovett**, *Approximate union closed conjecture*:

> **Theorem.** (i) Same `(3 − √5)/2` bound for union-closed `F`.
> (ii) Same bound holds for **approximately** union-closed families (those for which a `(1 − ε)` fraction of pairs `A ∪ B` lies in `F`).
> (iii) The bound `(3 − √5)/2` is **optimal** for the approximate version.

The third result — sharpness for the approximate problem — is the strongest evidence that the entropy method alone cannot exceed `(3 − √5)/2` *without using union-closure beyond approximation*.

### 4.3 Alweiss, Huang, Sellke (arXiv:2211.11731, 21 Nov 2022; *Electron. J. Combin.* **31(3)** #P3.35, 2024)

**Ryan Alweiss, Brice Huang, Mark Sellke**, *Improved lower bound for Frankl's union-closed sets conjecture*:

> **Theorem.** For every nonempty union-closed family `F ⊆ 2^[n]`, some `i ∈ [n]` is in at least a `(3 − √5)/2 ≈ 0.38` fraction of the sets.

They verify the explicit one-variable entropy inequality conjectured by Gilmer; one branch is checked by computer calculation (interval arithmetic suffices to make rigorous). This is the version most often cited as "the" `(3 − √5)/2` proof, because it was peer-reviewed (Electronic J. Combinatorics, 2024).

### 4.4 Pebody (arXiv:2211.13139, 23 Nov 2022)

**Luke Pebody**, *Extension of a method of Gilmer*. Independently obtains `(3 − √5)/2` by solving the underlying optimization in terms of the conditional entropy `H(X | S)` of a binary `X` given a side variable `S`.

> **Note on attribution.** A common convention in the literature (e.g., Aldridge's blog, Cambie's survey) is to attribute the **value** `(3 − √5)/2` jointly to these four works.

---

## 5. Beyond `(3 − √5)/2`: 2023–2025

### 5.1 Chase & Lovett (December 2022) — entropy upgrade

**Chase & Lovett**, *Better bounds for the union-closed sets conjecture using the entropy approach*, arXiv:2212.12500. Strengthens 2211.11689 with sharper entropy comparisons and gives further structural results for approximate union-closed families.

### 5.2 Yu (December 2022) — dimension-free formulation

**Lei Yu**, *Dimension-Free Bounds for the Union-Closed Sets Conjecture*, arXiv:2212.00658; published *Entropy* **25** (2023) no. 5, 767.

> **Theorem.** Yu reformulates the entropy approach in a dimension-free convex-optimization form, derives bounds that include Sawin's improvement as a special case, gives cardinality bounds on auxiliary random variables (making the optimization *computable*), and proves numerically `c(F) ≥ 0.38234` — beating `(3 − √5)/2 ≈ 0.38197`.

This is the first paper to **rigorously certify a constant strictly larger than `(3 − √5)/2`** via the computable form of Sawin's idea.

### 5.3 Cambie (June 2023) — survey + refinement

**Stijn Cambie**, *Progress on the union-closed conjecture and offsprings in winter 2022–2023*, arXiv:2306.12351 (21 June 2023). A combined survey and research paper. Cambie:

- Surveys the five-paper rush;
- Independently obtains the numerical bound ≈ `0.38234` via Sawin's convex-combination-of-couplings approach made computable;
- Proves FUCC for **infinitely many Maxwell–Boltzmann distributions** (a variant where the uniform distribution on `F` is replaced by a weighted one);
- Proves a version of FUCC for "non-uniform distributions" with inverse temperature bounded below.

(Cambie's "non-uniform" non-uniform paper is arXiv:2305.19338.)

### 5.4 Liu (June 2023; updated 2024) — conditional i.i.d. coupling

**Jingbo Liu**, *Improving the lower bound for the union-closed sets conjecture via conditionally i.i.d. coupling*, arXiv:2306.08824; published in IEEE ISIT 2024.

> **Theorem (numerical, conditional on Liu's optimization).** Replacing the i.i.d. coupling with one where `A, B` are i.i.d. *conditioned on* an auxiliary random variable `U` strictly improves the bound. Under numerically verified hypotheses, `c(F) ≥ 0.38271`.

The bound `0.38271` is currently (as of arXiv submission date) the **best published constant**. Liu also gives an analytic equation whose solution is the optimum of the conditional-coupling approach.

### 5.5 Phan (December 2024) — necessary-and-sufficient form

**Veronica Phan**, *Entropy approach for a generalization of Frankl's conjecture*, arXiv:2412.18622 (17 Dec 2024). Phan derives a **necessary and sufficient** information-theoretic condition for the existence of an element of frequency ≥ ½. The framing is currently the cleanest entry point for attacking FUCC with entropy.

### 5.6 Recent structural / lattice / graph results

- **Bouchard**, *Conjectures on union-closed families of sets*, arXiv:2310.02482. Proves `UC_x` (the conjecture's variant indexed by elements `x ∈ [n]`) for `x ∈ [⌈n/3⌉+1]`.
- **Bouchard**, *On the lattice formulation of the union-closed sets conjecture*, arXiv:2503.00277 (2025). Derives several necessary conditions on a minimum counterexample in the lattice formulation.
- **Bouchard**, *An averaging result for union-closed families of sets*, arXiv:2509.12537 (Sept 2025). New averaging-style result reachable without entropy.
- **Colbert**, *Chain conditions and optimal elements in generalized union-closed families of sets*, arXiv:2412.18740 (2024; to appear in *Order*). Recovers FUCC for finite or infinite union-closed families whose chains have length ≤ 3.
- **Gendler**, *Partial results for union-closed conjectures on the weighted cube*, arXiv:2504.13347 (April 2025). Generalizes Karpas (density ½) and Knill (logarithmic) to non-uniform product measures on the Boolean cube.

### 5.7 False alarms

Several arXiv preprints have claimed full proofs (e.g., arXiv:1507.01270 Reinhold-style, 1607.01007, 1711.02665, 2302.03484 by Scandone — withdrawn, 2405.03731 by Demontis). **None have been accepted by the community.** Scandone's 2302.03484 was reported to mishandle conditional information in the entropy argument and was withdrawn.

---

## 6. State of the Art — Quick Reference

| Paper | Year | Bound `c(F) ≥` | Method | Verification |
|---|---|---|---|---|
| Knill | 1994 | `(|F|−1)/log₂|F|` | combinatorial | published, *Graphs Combin.* |
| Wójcik | 1999 | `~1/log` refinement | combinatorial | *Discrete Math.* |
| Reimer | 2003 | avg set size ≥ ½log₂|F| | averaging | *Combin. Probab. Comput.* |
| Bošnjak–Marković | 2008 | true for `n ≤ 11` | computer search | *EJC* |
| Roberts–Simpson | 2010 | true for `|F| ≤ 46` | structural | *Australas. J. Combin.* |
| Balla–Bollobás–Eccles | 2013 | true for `|F| ≥ (2/3)2ⁿ` | averaging | *J. Combin. Theory A* |
| Karpas | 2017 | true for `|F| ≥ (½−c)2ⁿ` | Fourier | arXiv |
| Vučković–Živković | 2017 | true for `n ≤ 12` | computer | journal |
| Gilmer | Nov 2022 | `0.01` | entropy | arXiv |
| Sawin / Chase–Lovett / AHS / Pebody | Nov 2022 | `(3−√5)/2 ≈ 0.38197` | entropy | AHS in EJC 2024 |
| Yu | Dec 2022 | `0.38234` | entropy + couplings | *Entropy* 2023 |
| Cambie | Jun 2023 | `0.38234` | entropy | arXiv |
| Liu | 2023/24 | `0.38271` (numerical) | conditional i.i.d. coupling | IEEE ISIT 2024 |

The current best fully-rigorous constant is **`(3 − √5)/2 ≈ 0.38197`** (Alweiss–Huang–Sellke, peer-reviewed). Yu's `0.38234` and Liu's `0.38271` are best-known *numerical* lower bounds, contingent on the optimization being correctly carried out.

---

## 7. Frontier Analysis — Where the Slack Is

This is the section Phase 2 theory should attack. I have organized the bottleneck into seven specific "slack points" in the current best proofs (AHS, Sawin, Yu, Liu). Each comes with my (Claude's) assessment of how much room there appears to be.

### 7.1 The per-coordinate entropy inequality (Gilmer Lemma 3 / AHS Lemma)

**The inequality.** For `0 ≤ p, q ≤ 1`:
`h((1−p)(1−q)) ≥ (1/(2(1−ψ))) · ((1−q) h(p) + (1−p) h(q))`, ψ = (3−√5)/2.

**Why it bottlenecks at ψ.** This inequality is *sharp* at `p = q = ψ`, with equality. The constant `1/(2(1−ψ))` is forced by this single point of equality. Chase–Lovett's *approximate-union-closed* sharpness result (§4.2) shows that within the i.i.d. coupling, no constant > ψ can possibly come out — because the equality is attained by an approximately-union-closed family.

**Slack.** *Within i.i.d. couplings, none.* The inequality is sharp. *Beyond i.i.d. couplings* (Sawin's refinement, Yu's couplings, Liu's conditional couplings), the equality case shifts and there is **provable slack**. Most likely-fruitful: **identify a new family of couplings** where the local entropy comparison is tight at a point with `p, q > ψ`. Sawin's sketch + Liu's conditional-coupling extension are the only known systematic moves; both produce `≤ ~0.39`. So the slack here is *small*: probably exhausted by Liu's framework up to maybe `0.385 → 0.40`. (Speculative.)

### 7.2 The chain-rule reduction (Gilmer §2)

**The step.** Gilmer shows `H(A ∪ B) ≥ c · H(A)` coordinate-by-coordinate using
`H((A∪B)_i | (A∪B)_{<i}) ≥ H((A∪B)_i | A_{<i}, B_{<i})`,
then applies the per-coordinate inequality and sums.

**Slack.** *Significant*. The inequality `H(X | Y) ≥ H(X | Z)` whenever `σ(Y) ⊆ σ(Z)` is loose by an amount equal to the conditional mutual information `I((A∪B)_{<i} ; (A_{<i}, B_{<i}) | (A∪B)_i)`. **This conditional mutual information is exactly the structural information about union-closure we are throwing away by coordinatewise application.** This is the most promising place to attack, because:

1. It is the *only* step in the chain that introduces a non-tight inequality before the per-coordinate inequality is applied;
2. The lost information is exactly "how the past coordinates of `A` and `B` carry more info than just their union" — which is *zero* on i.i.d. coordinates (justifying Gilmer's chain-rule move) but **non-zero** in dimensions exhibiting structural union-closure;
3. No paper in §4–§5 attempts to quantify this slack.

**Concrete Phase-2 question.** Is there a sub-additive replacement of the chain rule that uses correlations between coordinates *induced by union closure*? Cf. **submodularity** of entropy (Han's inequality, Shearer's lemma) — none of the existing entropy works exploit Shearer-style bounds on a union-closed family.

### 7.3 The "uniform-distribution-over-F" reduction

**The step.** The combinatorial reduction reads: choose `A` uniformly from `F`, so that `H(A) = log|F|`, and `A∪B ∈ F`, so `H(A∪B) ≤ log|F| = H(A)`. Comparing to the info-theoretic statement (which lower-bounds `H(A∪B)` by `(1+c)H(A)`) forces a contradiction unless some `Pr[i ∈ A] ≥ const`.

**Slack.** *Significant but tricky*. The bound `H(A∪B) ≤ log|F|` uses that `A∪B ∈ F` but **not** that `|F|` is small relative to the support of `B`. A *non-uniform* distribution on `F` (Cambie's Maxwell–Boltzmann distributions) gives different `H(A)`, and the optimization can be re-run. Cambie shows this beats `(3−√5)/2` in the weighted setting. **No paper yet has optimized over both the coupling and the distribution simultaneously, jointly with the structural constraints.** This is a candidate for an optimization-LP track in Phase 2.

### 7.4 Ignoring intersection structure

**The omission.** All entropy proofs use `A ∪ B` but never `A ∩ B`. Union-closure does *not* assume intersection-closure. But a union-closed family is automatically "monotone" with respect to its order ideal generated by minima, and Reimer's average-set-size bound (§2.2) is exactly an `intersection-side` lemma.

**Slack.** Likely large but unstructured. Combining Reimer-style averaging with Gilmer-style entropy is *missing* from the literature. Phase 2 should specifically try: *replace `H(A∪B)` by `H(A∪B) + λ H(A∩B)` for some `λ`*, then re-derive the chain-rule bound.

### 7.5 The "no structure on F" implicit assumption

**The omission.** The proofs treat `F` purely as a subset of `2^[n]`. They never use:

- the lattice height of `F` under inclusion;
- the number of join-irreducibles in the corresponding lattice (Poonen formulation);
- the bipartite graph induced by Bruhn–Charbit–Schaudt–Telle's reduction.

**Slack.** Structural. The most likely-fruitful crossover: **use the AHS entropy bound as a "global" inequality and the lattice / graph reductions as "structural" constraints**. Concretely: for `F` with small lattice height `≤ h`, the per-coordinate inequality should be improvable by a factor depending on `h`. No paper has done this.

### 7.6 Algorithmic / probabilistic alternative methods

**Gap.** No randomized algorithm constructively finds a heavy element of frequency `≥ c`. The proofs are non-constructive. A *constructive* proof of frequency `≥ ½` would presumably go through some explicit potential function.

### 7.7 The auxiliary random variable in Liu / Yu

**The step.** Liu introduces an auxiliary `U` and considers `A, B | U` i.i.d.; the optimization over the joint distribution of `(A, B, U)` is parameterized by a finite-dimensional convex program.

**Slack.** *Moderate*. The cardinality of `U` is unbounded in principle but Yu (and Liu) bound it. The bound is loose: each finite cardinality `k` of `U` gives a tighter constant, and the limit `k → ∞` is the relevant optimum. Liu has not computed the `k=∞` optimum analytically. Phase 2's computational track should attempt larger-`k` numerical optimizations and search for the limit.

### 7.8 Summary of slack ranking (Claude's qualitative judgment)

| Slack point | Where in proof | Estimated room | Phase-2 actionability |
|---|---|---|---|
| 7.2 chain-rule | structural | **large** | high — try Shearer/submodular |
| 7.4 ignored ∩ | conceptual | large | medium — find the right `λ` |
| 7.5 ignored lattice/graph | structural | large | medium — crossover |
| 7.3 uniform distrib. | choice of measure | medium | medium — joint optim. |
| 7.7 cardinality of `U` | optimization | medium | high — pure computation |
| 7.1 per-coord ineq. | local inequality | **small** | low — already sharp at ψ |
| 7.6 constructive | meta | n/a (different goal) | medium-low |

**Recommended attack vectors for Phase 2 (top 3):**

1. **Shearer-style chain rule (§7.2).** Replace the per-coordinate chain rule by a Shearer-type entropy inequality that respects union-closure. This is the **cleanest single point of slack** in the existing proof and has not been investigated in any of the 2022–2025 papers.
2. **Adding intersection terms (§7.4).** Augment the entropy target to `H(A∪B) + λH(A∩B)`; for the right `λ`, Reimer-style bounds on `H(A∩B)` should combine multiplicatively with the union entropy bound.
3. **Joint coupling-and-measure optimization (§7.3 + §7.7).** Run Liu's conditional-i.i.d.-coupling optimization with `U` of cardinality up to (say) 16, and *simultaneously* re-weight the distribution on `F` à la Cambie. This is the cleanest computational target.

---

## 8. Open Problems (high level)

(Detailed in `open_problems.md`.) The four most-cited open subproblems are:

1. **Beat 0.38271.** Push the entropy-method constant past Liu's bound.
2. **Reach 0.4.** This is the threshold above which one would credibly believe a clean entropy-only proof of FUCC is possible.
3. **Verify FUCC for `n = 13`.** The Bošnjak–Marković / Vučković–Živković computational frontier.
4. **Prove FUCC for `|F|` in `[47, 100]`.** Push the Roberts–Simpson family-size bound.

Other long-standing variants and open problems (Cambie's survey, §5; the Bruhn–Schaudt survey, §5–§7) include all 14 of the items in `open_problems.md`.

---

## 9. Notation reference

- `F`: a union-closed family of subsets of a finite ground set;
- `n = |⋃ F|`: ground-set size;
- `h(p) = −p log p − (1−p) log(1−p)`: binary entropy in nats (or bits — be consistent);
- `ψ = (3 − √5)/2 = (1 − 1/φ)`, where `φ = (1+√5)/2` is the golden ratio;
- `c(F) = max_x |{A ∈ F : x ∈ A}| / |F|`: best element frequency;
- `H(X)`: Shannon entropy of `X`;
- `KL(P‖Q)`: Kullback–Leibler divergence.

---

## 10. Bibliography

See `bibliography.bib` in the same directory for BibTeX entries for every paper cited here.
