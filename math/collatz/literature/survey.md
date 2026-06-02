# A Literature Survey of the Collatz Conjecture (3n+1 Problem)

**Authors:** Alex Ye with Claude
**Date:** June 2026
**Status:** Phase 1 literature survey for a multi-agent research project on the Collatz conjecture.

> **Scope and verification.** This survey covers peer-reviewed and well-cited arXiv work on the Collatz / 3n+1 problem from the 1970s through 2025. Every theorem statement, numerical constant, and arXiv identifier was cross-checked via WebSearch against at least two independent sources (publisher metadata, Semantic Scholar, MathSciNet citations appearing in third-party papers, the author's own webpage). Where a fact could only be confirmed from one source, or where a venue / page range is uncertain, the entry is marked **[PARTIAL]**. We did not blindly fabricate any constant, theorem, or attribution; uncertain claims are flagged inline as **[UNVERIFIED]** or are simply omitted.
>
> Direct fetching of `arxiv.org`, `terrytao.wordpress.com`, `dml.cz`, and several publisher PDFs was blocked by HTTP 403 during this survey, so quoted statements rely on multi-source web search reporting rather than verbatim PDF extraction. We have been correspondingly careful to use only the parts that appear consistently across sources.

---

## 1. The conjecture

Define the **accelerated Collatz map**
$$T : \mathbb{N}_{\ge 1} \to \mathbb{N}_{\ge 1}, \qquad T(n) = \begin{cases} n/2, & n \text{ even,}\\ (3n+1)/2, & n \text{ odd.} \end{cases}$$
Equivalently, work with the **raw Collatz map** $\mathrm{Col}(n) = n/2$ for even $n$ and $\mathrm{Col}(n) = 3n+1$ for odd $n$; the two differ only by absorbing the obligatory halving step after every odd step into the definition.

**The Collatz conjecture.** For every $n \ge 1$, there exists $k \ge 0$ with $T^k(n) = 1$.

Equivalently, $\mathrm{Col}_{\min}(n) := \inf_k \mathrm{Col}^k(n) = 1$ for all $n$.

The problem is variously attributed to Lothar Collatz (1937), Shizuo Kakutani, Stanis{\l}aw Ulam, Helmut Hasse, and Sir Bryan Thwaites (whence the names *3x+1 problem*, *Kakutani's problem*, *Hasse's algorithm*, *Syracuse problem*, *Thwaites conjecture*, *Ulam's problem*) [Lagarias 1985].

We distinguish three natural arithmetic invariants of an orbit:

- **Stopping time** $\sigma(n) := \inf\{k \ge 1 : T^k(n) < n\}$ — first descent below the starting value.
- **Total stopping time** $\sigma_\infty(n) := \inf\{k \ge 0 : T^k(n) = 1\}$ — first time the orbit reaches $1$.
- **Glide / max-height** $\max_k T^k(n)$ — peak excursion of the trajectory.

A *nontrivial cycle* is a periodic orbit other than $\{1, 2\}$. A nontrivial divergent orbit is one with $T^k(n) \to \infty$. The conjecture is equivalent to: there are no nontrivial cycles AND no divergent orbits.

---

## 2. Approach families: a taxonomy

We will organize the literature into six approach families, each with characteristic tools and characteristic gaps:

| Family | Representative work | Tool | Captures | Misses |
|---|---|---|---|---|
| (1) Ergodic / statistical density | Terras 1976; Korec 1994; Krasikov–Lagarias 2003; Tao 2022 | Markov chains on residues mod $2^k$, $3^k$; logarithmic averaging | Almost-all-type statements | A measure-zero "bad set" can still contain cycles or divergent orbits |
| (2) 2-adic / 3-adic / automaton | Lagarias 1985, Bernstein–Lagarias 1996, Akin 2004 | Topological conjugacy with the shift on $\mathbb{Z}_2$ | Encoding of parity sequences as 2-adic integers | Conjugacy is measure-preserving but does not single out integers |
| (3) Computational verification | Oliveira e Silva 2010; Barina 2021, 2025 | Sieve methods, GPU/SIMD, residue tables | Empirical certainty up to $2^{71}$ | Says nothing about $n > 2^{71}$ |
| (4) Cycle exclusion | Steiner 1977; Eliahou 1993; Simons–de Weger 2005; Hercher 2023 | Baker's theorem on linear forms in logs; continued fractions of $\log_2 3$ | Cycle length / structure lower bounds | Cannot rule out *divergent* orbits |
| (5) Generalizations & undecidability | Conway 1972; Conway 1987 (FRACTRAN); Kurtz–Simon 2007 | Reduction from Turing machines / Minsky machines | Hardness of broader function families | Specific $T$ is not covered by the reduction |
| (6) PDE / dispersive estimates | Tao 2022 + 2020 blog | Characteristic functions on $\mathbb{Z}/3^n\mathbb{Z}$, large-frequency estimates | Mixing / equidistribution of Syracuse random variables | Only logarithmic density; only "almost bounded" descent |

We treat each family below.

---

## 3. Family (1): Ergodic / statistical density results

### 3.1 Terras (1976) — natural density of finite stopping times

> **Theorem (Terras 1976).** The set $\{n \ge 1 : \sigma(n) < \infty\}$ — integers whose Collatz orbit dips below the starting value — has natural density $1$.

Terras's proof analyzes the parity sequence of $T^j(n)$ for $j \le k$, showing that the number of odd iterates in the first $k$ steps is asymptotically Gaussian in $k$ with mean $k/2$. From this he extracts that the "stopping time exists" event captures density $1$. (The argument was flagged as having a gap by M{\"o}ller 1978; Allouche 1979 supplied a corrected proof. See [Terras 1976; M{\"o}ller 1978; Allouche 1979].)

**Key technique.** Encoding the trajectory by its parity vector (a 0/1 string) — the same encoding that makes the 2-adic conjugacy work — and applying a local central-limit theorem.

**What it does NOT prove.** A density-zero exceptional set is allowed, which could in principle contain *cycles* or *divergent orbits*. Stopping time finite does not imply *total* stopping time finite.

### 3.2 Everett (1977) — independent proof

Independently of Terras, Everett 1977 proved the same density-1 result. The two proofs differ in technique; Everett's argument is more combinatorial.

### 3.3 Crandall (1978) — first polynomial lower bound

> **Theorem (Crandall 1978).** There exists a constant $c > 0$ such that
> $$ \#\{m \le x : \sigma_\infty(m) < \infty\} \ge x^c $$
> for all sufficiently large $x$.

Crandall also tied the conjecture to the Diophantine equation $2^X - 3^Y = p$.

### 3.4 Korec (1994) — $\log_4 3 \approx 0.7925$ descent exponent

> **Theorem (Korec 1994).** For every real $c > \log_4 3 = 0.79248\ldots$, almost every $n$ (in the sense of natural density) admits some $k$ with $T^k(n) < n^c$.

This was the standing record for descent-exponent until Tao 2022 effectively replaced $n^c$ by any $f(n) \to \infty$.

**Why the constant $\log_4 3$?** Each $T$-step kills a factor $4$ (two halvings on average per odd step) but introduces a factor $3$ (the $3n+1$). The exponent at which odd-step contributions exactly balance even-step contractions is $\log 3 / \log 4 = \log_4 3$.

**What it does NOT prove.** Almost every $n$ has *one* iterate below $n^{0.79}$ — but Korec gives no control over what happens after, and again leaves a measure-zero exceptional set unaddressed.

### 3.5 Applegate–Lagarias (1995) and Krasikov–Lagarias (2003) — the $\gamma > 0.84$ bound

Krasikov 1989 introduced *difference inequalities*: linear inequalities relating the counts $N_k(x) := \#\{n \le x : T^k(n) \le x\}$ for different $k$. These give lower bounds for the count of pre-images of any fixed integer.

Applegate–Lagarias 1995 (Density Bounds I, II) refined this to the form: for any fixed $a$ not divisible by $3$ and any large enough $x$,
$$ \#\{n \le x : a \text{ appears in the forward orbit of } n\} \ge x^{\gamma} $$
for some explicit $\gamma$.

> **Theorem (Krasikov–Lagarias 2003).** The above bound holds with $\gamma > 0.84$.

This remained, until Tao 2022, the strongest unconditional density-of-descent result. The technique combines linear programming on a finite system of difference inequalities with a careful analysis of the inverse tree of the $T$-map.

**What it does NOT prove.** The bound $x^{0.84}$ is below $x$ — i.e., a positive fraction of integers below $x$ might *not* reach $1$. This is consistent with the existence of a density-$\ge 0.16$ "bad" set.

### 3.6 Lagarias–Weiss (1992) — stochastic models and the $\gamma_{LW} = 2/\log(4/3) \approx 6.95$ heuristic

> **Heuristic (Lagarias–Weiss 1992).** Modeling the parity of $T^k(n)$ as i.i.d. fair coin flips, the expected total stopping time of a random integer near $n$ is asymptotically $\gamma_{LW} \log n$ where $\gamma_{LW} = 2/\log(4/3) \approx 6.9521$.

This is not a theorem about $T$; it is a Branching/Random Walk model that *agrees beautifully* with computer experiment. It also predicts that, conjecturally, there is no nontrivial cycle of any reasonable length and no divergent orbit (the random walk drifts to $-\infty$ logarithmically).

### 3.7 Sinai (2003) and Kontorovich

> **Theorem (Sinai 2003).** Considered as a map on $\mathbb{Z}_2$, the iteration $T$ has well-defined statistical limit laws: certain renormalized increments $(r_m, \delta_m)$ converge in distribution as $m \to \infty$.

This makes the random-walk heuristic of Lagarias–Weiss into rigorous limit theorems — but, again, on $\mathbb{Z}_2$, *not* on $\mathbb{N}$, and not addressing convergence.

### 3.8 Tao (2022) — the current SOTA in family (1)

We treat this in §5 in dedicated detail.

---

## 4. Family (2): 2-adic / 3-adic / automaton approach

### 4.1 The 2-adic shift conjugacy

The set $\mathbb{Z}_2$ of 2-adic integers carries the shift map $\sigma(x) = (x-1)/2$ if $x$ odd, $x/2$ if $x$ even.

> **Theorem (Bernstein–Lagarias 1996).** There exists a continuous, measure-preserving (under Haar measure) bijection $\Phi : \mathbb{Z}_2 \to \mathbb{Z}_2$ such that $T \circ \Phi = \Phi \circ \sigma$.

That is, the accelerated Collatz map on $\mathbb{Z}_2$ is *topologically conjugate to the shift*. The conjugacy is given explicitly by the "parity encoding": the $k$th binary digit of $\Phi^{-1}(n)$ records the parity of $T^k(n)$.

**Consequence.** The orbit dynamics of $T$ are as wild as the shift — Bernoulli, hence ergodic of any kind one could ask for — *on $\mathbb{Z}_2$*. The hard problem is that the conjugacy $\Phi$ sends a Cantor-fractal subset of $\mathbb{Z}_2$ (the parity sequences of integers) to the integers themselves, and *that subset is not preserved by the shift*. Akin 2004 makes this discrepancy precise and uses it to explain "why $3x+1$ is hard": any tool that respects the 2-adic measure cannot detect the integers.

### 4.2 The 3-adic side and Tao's Syracuse random variables

A parallel encoding works mod $3^n$: the *Syracuse map* $\mathrm{Syr}(N) = $ largest odd divisor of $3N+1$, restricted to odd $N$ coprime to $3$, induces a Markov-style chain on $(\mathbb{Z}/3^n\mathbb{Z})^\times$. Tao 2020 (blog) and Tao 2022 work directly with the characteristic function (Fourier coefficients) of this chain.

### 4.3 Conjugacy mod $2^n$

The conjugacy $\Phi$ descends to a permutation $\Phi_n$ of $\mathbb{Z}/2^n\mathbb{Z}$. Bernstein–Lagarias and follow-ups studied the order of $\Phi_n$; it grows like $2^{n-4}$ for $n \ge 6$, exhibiting "maximal complexity" from a combinatorial standpoint.

---

## 5. Family (6) and the centerpiece: Tao (2022)

### 5.1 The main theorem

The published version is in *Forum of Mathematics, Pi*, vol. 10 (2022), article e12, DOI `10.1017/fmp.2022.8`, 56 pages, also arXiv:1909.03562 (posted 10 Sep 2019).

> **Theorem 1.3 [Tao 2022].** For any function $f : \mathbb{N}_{\ge 1} \to \mathbb{R}$ with $\lim_{N \to \infty} f(N) = +\infty$, the lower-bound function $\mathrm{Col}_{\min}(N) \le f(N)$ holds for almost every $N \ge 1$ in the sense of **logarithmic density**.

That is, the exceptional set $E_f := \{N : \mathrm{Col}_{\min}(N) > f(N)\}$ has logarithmic density $0$:
$$ \frac{1}{\log X} \sum_{\substack{N \le X \\ N \in E_f}} \frac{1}{N} \xrightarrow{X \to \infty} 0. $$
The function $f$ can grow as slowly as desired — $f(N) = \log\log\log\log N$ is allowed, as is any sub-iterated-log $f$.

### 5.2 What the theorem allows to still exist

The theorem leaves the following possibilities open:

1. **Nontrivial cycles** of any length whose elements form a set of logarithmic density $0$. (Any single cycle is finite, so it has density $0$ trivially.)
2. **Divergent orbits** starting from a set of logarithmic density $0$ — for instance, the set of all $n$ with $\mathrm{Col}^k(n) \to \infty$ could be any set whose log-density vanishes.
3. The exceptional set $E_f$ for a given $f$ is allowed to be infinite, even of natural density up to $1$, as long as it has *logarithmic* density $0$.

Tao explicitly notes (blog post 2019/09/10 and paper §1) that he believes logarithmic density can probably be upgraded to natural density via additional "fine-scale mixing" work; but as of June 2026 that upgrade has not appeared in the literature.

### 5.3 The technique in outline

Tao's proof has four key innovations:

(i) **Syracuse random variables.** Let $\mathrm{Syrac}(\mathbb{Z}/3^n\mathbb{Z})$ denote the law of the residue mod $3^n$ obtained after iterating the Syracuse map (the accelerated 3-adic map) for a number of steps $\sim n \log n$. This is a discrete probability distribution on $(\mathbb{Z}/3^n\mathbb{Z})^\times$.

(ii) **First-passage approximate transport.** Tao establishes that the first time an orbit drops a fixed multiple in $\log$, its residue mod $3^n$ is well-approximated by $\mathrm{Syrac}(\mathbb{Z}/3^n\mathbb{Z})$. This is the "approximate transport property" — a controlled coupling.

(iii) **Fourier on $\mathbb{Z}/3^n\mathbb{Z}$ at high frequencies.** The crucial input is estimating $|\widehat{\mathrm{Syrac}_n}(\xi)|$ for $\xi \in \widehat{\mathbb{Z}/3^n\mathbb{Z}}$ of high "3-adic frequency". Tao bounds the characteristic function of a certain skew random walk in 3-adic frequency space, in the style of dispersive/Strichartz estimates familiar from PDE — this is the "PDE-flavoured" framing.

(iv) **Iteration with renormalization.** Combining (i)–(iii) gives a non-trivial mixing rate that one can iterate. Each iterate doubles the orbit length but only multiplicatively dilutes the failure mode, eventually pushing the failure set into log-density-$0$ territory.

### 5.4 Tao 2020 blog: Equidistribution of Syracuse random variables

In Tao's *Equidistribution of Syracuse random variables and density of Collatz preimages* (blog post, 25 Jan 2020), he distills a follow-up question: define
$$ c_n := \inf_{\substack{b \in \mathbb{Z}/3^n\mathbb{Z} \\ 3 \nmid b}} \mathbb{P}\bigl(\mathrm{Syrac}(\mathbb{Z}/3^n\mathbb{Z}) = b\bigr). $$
He proves:
- **Submultiplicativity:** $c_{n_1 + n_2 - 1} \ge c_{n_1} c_{n_2}$.
- **Heuristic implication:** if $c_n = 3^{-n + o(n)}$ (the "$\beta = 1$" equidistribution heuristic), then preimage density of $\{1\}$ in $[1,x]$ is $x^{1 - o(1)}$.

This is — explicitly — a research program. Proving $c_n = 3^{-n + o(n)}$ would substantially strengthen Tao 2022, but remains open.

### 5.5 What Tao does NOT prove (the gap)

We treat the gap analysis in §10. In short:

- He does **not** rule out exceptional sets of logarithmic density 0.
- He does **not** improve "almost bounded" to "bounded": the asymptotic descent only beats *any function going to infinity*, not "below $C$" for an absolute constant $C$.
- He does **not** address cycles or divergent orbits directly.

---

## 6. Family (3): Computational verification

### 6.1 History of the verification frontier

- **1992**: $5.6 \times 10^{13}$ (Leavens–Vermeulen)  [UNVERIFIED date / authors precisely; widely cited as such]
- **2009**: $20 \cdot 2^{58} \approx 5.76 \times 10^{18}$ (Oliveira e Silva, documented in *The Ultimate Challenge* 2010)
- **2017**: $\sim 87 \cdot 2^{60}$ (yoyo@home BOINC project, cross-checking Oliveira e Silva up to that point) [PARTIAL]
- **2020/21**: $2^{68} \approx 2.95 \times 10^{20}$ (Barina 2021)
- **2025**: $2^{71} \approx 2.36 \times 10^{21}$ (Barina 2025)

### 6.2 Barina's algorithmic improvements

The Barina 2021 paper *Convergence verification of the Collatz problem* (Journal of Supercomputing 77, 2681–2688) made one critical change: it replaced the $O(2^N)$-entry precomputed sieve table (which dominated memory traffic in earlier verifications) by an $O(N)$-entry hierarchical lookup table. Reported throughput:

- Single-threaded CPU (Intel Xeon Gold 5218): $4.2 \times 10^9$ 128-bit numbers per second.
- OpenCL GPU (NVIDIA GeForce RTX 2080): $2.2 \times 10^{11}$ 128-bit numbers per second.

Barina 2025 reports a cumulative algorithmic speedup of $1335\times$ from the CPU baseline to the current GPU implementation; the search was distributed across several European supercomputers and now reaches $2^{71}$, with four additional path records.

### 6.3 What computation has (and has not) ruled out

Computation rules out *finite-sized cycles starting below $2^{71}$* and *divergent trajectories starting below $2^{71}$*. It says nothing about $n > 2^{71}$ — and that is an *infinite* deficit.

By itself, computation cannot close the conjecture. Its theoretical role is:

- Eliminating low-lying counterexamples that would otherwise complicate any general argument.
- Empirically validating the Lagarias–Weiss random-walk heuristic and refining the predicted distribution of total stopping times.
- Providing data for path-record analysis (orbits whose maximum exceeds previous records), which both Roosendaal and Barina maintain.

---

## 7. Family (4): Cycle exclusion

### 7.1 Steiner (1977): no nontrivial 1-cycle

A *$k$-cycle* is conventionally indexed by the number $k$ of local minima — equivalently, the number of distinct "descent valleys" in the cycle. A 1-cycle is a cycle in which odd steps form a single contiguous block followed by even steps, modulo the cyclic order.

> **Theorem (Steiner 1977).** The only Collatz $1$-cycle is the trivial cycle $\{1, 2\}$.

The proof reduces existence of a nontrivial 1-cycle to a Diophantine inequality of the form $|a \log 2 - b \log 3 + c| < \epsilon$ for specific integers $a, b, c$, and rules this out using Baker's theorem on linear forms in logarithms together with the continued-fraction expansion of $\log_2 3$. Lagarias remarked that the use of transcendence theory for so concrete a question is "surprisingly heavy".

### 7.2 Eliahou (1993): cycle length lower bound

> **Theorem (Eliahou 1993).** The period $p$ of any nontrivial cycle satisfies
> $$ p = 301{,}994 a + 17{,}087{,}915 b + 85{,}137{,}581 c $$
> for some non-negative integers $a, b, c$ with $b \ge 1$ and $ac = 0$. In particular $p \ge 17{,}087{,}915$.

This is sharpest when combined with the *lowest* verification bound: the higher $N$ for which we verify no cycle below $N$, the stronger the lower bound on $p$ becomes via continued-fraction sharpening.

### 7.3 Simons (2005) and Simons–de Weger (2005)

> **Theorem (Simons 2005).** No nontrivial $2$-cycle.
> **Theorem (Simons–de Weger 2005).** No nontrivial $m$-cycle for $1 \le m \le 68$.

Both proofs follow the Steiner template: parameterize the would-be cycle, derive a Diophantine inequality of "Baker type", reduce by continued fractions of $\log_2 3$, and exhaust a finite list of remaining cases by direct computation.

### 7.4 Hercher (2023)

> **Theorem (Hercher 2023).** No nontrivial $m$-cycle for $1 \le m \le 91$.

A direct extension of Simons–de Weger by tightening the Baker-type bounds.

### 7.5 What cycle-exclusion does NOT prove

These methods provide strong constraints on cycles but say nothing about divergent orbits. They are also asymptotic in $m$: ruling out cycles for *all* $m$ simultaneously requires unconditional improvements in irrationality measure for $\log_2 3$ (Liouville-type effective bounds), which currently fall short.

---

## 8. Family (5): Generalizations and undecidability

### 8.1 Conway (1972)

Conway considered generalized maps of the form $g(n) = a_i n + b_i$ when $n \equiv i \pmod{P}$, with rationals $a_i, b_i$ such that $g$ maps integers to integers.

> **Theorem (Conway 1972).** It is algorithmically undecidable whether, given such a generalized Collatz map $g$ and a starting integer $n$, the iterate $g^k(n)$ ever reaches $1$.

The proof simulates a Minsky / register machine using residue conditions, and inherits the halting-problem undecidability.

### 8.2 FRACTRAN (Conway 1987)

FRACTRAN is a clean reformulation: given a finite list of positive rationals $p_1, \ldots, p_m$ and a starting integer $n$, repeatedly find the first $p_i$ such that $p_i \cdot n$ is an integer, and replace $n$ by $p_i \cdot n$. Halt when no such $p_i$ exists.

FRACTRAN is Turing-complete; Conway exhibited FRACTRAN programs computing primes, the Fibonacci sequence, etc.

### 8.3 Kurtz–Simon (2007)

> **Theorem (Kurtz–Simon 2007).** The generalized Collatz problem is $\Pi^0_2$-complete.

That is, it sits exactly two quantifier alternations above decidable — neither computably enumerable nor co-computably enumerable. The reduction uses Conway's FRACTRAN encoding to simulate arbitrary Turing machines.

**Why this does NOT settle the classical $3x+1$ conjecture.** The reduction uses an *infinite family* of maps parameterized by Turing machines — it shows the class of maps cannot be uniformly decided. The single map $T(n) = n/2$ or $(3n+1)/2$ is not in the image of this reduction. Indeed, for any fixed map, the orbit-reachability question may very well be decidable; we just don't have a method.

---

## 9. Comparative summary table

| Result | What it proves | What remains open |
|---|---|---|
| Terras 1976, Everett 1977 | Density-1 of integers with finite *stopping time* | Total stopping time; the density-0 exceptional set |
| Korec 1994 | Density-1 of integers with iterate $< n^{0.7925}$ | What happens after that drop |
| Krasikov–Lagarias 2003 | Pre-image density $\ge x^{0.84}$ for any fixed $a$ | Pre-image density $= x^{1-o(1)}$ |
| Sinai 2003 | Statistical limit laws on $\mathbb{Z}_2$ | Convergence on $\mathbb{N}$ |
| Lagarias–Weiss 1992 | Random-walk heuristic, $\gamma_{LW} \approx 6.95$ | Not a theorem |
| Tao 2022 | $\mathrm{Col}_{\min}(N) \le f(N)$ for log-density-1 of $N$ | Natural density; "bounded" instead of "almost bounded"; cycles; divergence |
| Bernstein–Lagarias 1996 | 2-adic conjugacy with shift | Conjugacy does not single out $\mathbb{N}$ |
| Steiner 1977 | No nontrivial 1-cycle | Higher $k$-cycles |
| Simons–de Weger 2005, Hercher 2023 | No $k$-cycle for $k \le 91$ | All $k$; divergent orbits |
| Eliahou 1993 | Cycle length $\ge 17{,}087{,}915$ | Sharper bound |
| Conway 1972; Kurtz–Simon 2007 | Generalized Collatz undecidable / $\Pi^0_2$-complete | Classical $T$ not covered |
| Barina 2025 | Verified to $2^{71}$ | All $n > 2^{71}$ |

---

## 10. Gap analysis: from Tao 2022 to the full Collatz conjecture

This is the critical section per the project brief: we examine, precisely, what Tao 2022 leaves unproven and what new ingredient would close each gap.

### 10.1 The four nested levels of "almost all attain almost bounded"

Tao's statement
$$ \mathrm{Col}_{\min}(N) \le f(N) \text{ for log-density-1 of } N $$
has four parameters that can each be tightened:

(a) **The density measure.** Logarithmic density vs. natural density vs. *every* $N$.

(b) **The exceptional set's size.** Density 0 vs. positive but small.

(c) **The descent target.** $f(N) \to \infty$ vs. an absolute constant $C$ vs. exactly $1$.

(d) **The descent type.** Some iterate $\le f(N)$ vs. all iterates eventually $\le 1$ (handles cycles).

The full conjecture corresponds to: (a) every $N$, (c) absolute constant $1$, (d) all iterates eventually $1$ (rules out cycles AND divergence). Tao currently gives (a) log-density 1, (c) any $f(N)\to\infty$, (d) some iterate.

### 10.2 What "logarithmic density 1" still allows to exist

Logarithmic density is more permissive than natural density:
$$ \delta_{\log}(E) = \lim_{X \to \infty} \frac{1}{\log X} \sum_{n \in E, n \le X} \frac{1}{n}. $$
If $E$ has natural density $\delta$, it has log-density $\delta$. But $E$ can have log-density $0$ while having *positive* natural density on each block $[X, 2X]$ that decays as $1 / \log X$. Concretely:

- The set of $N$ that *fail* Tao's bound could be a thin set in each dyadic block $[2^k, 2^{k+1}]$, of size $\sim 2^k / k$ — log-density 0, but *infinite*.
- It could contain entire arithmetic progressions of moderate density.
- It could in principle contain (a) infinitely many distinct cycles or (b) the basins of attraction of finitely many divergent orbits, provided those basins are appropriately thin.

The upgrade Tao informally proposed (blog 10 Sep 2019) is to natural density. He suggests this requires a *fine-scale mixing* result for the Syracuse Markov chain, analogous to upgrading weak convergence to total-variation convergence in a Markov chain mixing argument. Specifically, one would need to prove that the convergence of $\mathrm{Syrac}(\mathbb{Z}/3^n\mathbb{Z})$ to uniform is fast not only in the $L^2$ sense (which is what gives log-density) but also in a stronger $L^\infty$ or total-variation sense.

### 10.3 Closing the "almost bounded → bounded" gap

This is the more substantial gap. To replace "$\le f(N)$ for any $f \to \infty$" by "$\le C$ for an absolute constant $C$" would require *uniform* control of the exit time in $N$. The current proof gives an exit time that depends on $f$ via an unbounded — though slowly so — function. Closing this gap means:

(i) Proving that the descent half-time $\tau_{1/2}(N)$ (the first time $T^k(N) < N/2$, say) satisfies an unconditional upper bound that does **not** depend on $N$. The Lagarias–Weiss heuristic predicts $\tau_{1/2}(N) = O(\log N)$ for typical $N$, but unconditionally we have no such bound.

(ii) An *energy* or *entropy* monotonicity argument on the parity sequence — e.g., a Lyapunov function $V$ on $\mathbb{Z}_2$ such that $V \circ \sigma \le V - \epsilon$ on a positive-measure subset. This would be a 2-adic analogue of dissipativity for a PDE.

In Tao's PDE-style framing: the current argument is like proving "the solution stays bounded for a randomly chosen initial data". Closing the gap is like proving "the solution stays bounded for every initial data" — i.e., upgrading from "almost-sure" to "deterministic" boundedness for a non-linear dynamical system. This is *the* standard hard step in dispersive PDE.

### 10.4 Handling cycles and divergence

Tao's theorem does not directly rule out (a) cycles or (b) divergent orbits. Each is logically independent of "almost bounded descent":

- A *cycle* not containing $1$ would be a fixed finite set; it has both natural and logarithmic density 0, so Tao's theorem applies vacuously to it.
- A *divergent orbit*'s starting integer can sit in any thin set; if the basin is thin enough, Tao does not catch it.

To rule out cycles, one essentially needs *cycle-exclusion* (family 4) or a structural / 2-adic argument. To rule out divergence, one needs Lyapunov-style descent (§10.3 above).

### 10.5 The missing ingredient — synthesis

Stepping back, the conjecture would follow from any *one* of:

**(α)** A pointwise (every-$N$) Lyapunov function $V : \mathbb{N} \to \mathbb{R}_{\ge 0}$ such that $V(T(n)) \le V(n) - \epsilon$ for all but finitely many $n$. (Trivial-sounding, but no candidate is known. The Lagarias–Weiss random-walk heuristic suggests $V(n) = \log n$ works *on average*, but the realized walk can stay near $V$ much longer than expected.)

**(β)** A *deterministic* fine-scale mixing result for the Syracuse Markov chain (Tao's program). This would close (a) and (b) above, leaving still cycle-exclusion and divergence-exclusion.

**(γ)** A *2-adic obstruction*: an invariant submanifold or a measure-zero structure on $\mathbb{Z}_2$ that contains the integers and is contracted by the shift on $\Phi^{-1}(\mathbb{N})$. (Akin 2004 frames this; no construction is known.)

**(δ)** A clever *combinatorial* finite-state argument capturing exactly $T$ and not the Conway generalizations. The Conway/FRACTRAN undecidability says no method working uniformly across all generalized maps can succeed; but a method depending sharply on the specific arithmetic of $2, 3$ might.

The single most cited "missing ingredient" in expert commentary is **(β)**: a strengthening of Tao 2022 from log-density to natural density via Syracuse equidistribution, combined with the assumption that no Liouville-type Diophantine pathology of $\log_2 3$ produces a hidden divergent orbit.

---

## 11. Three most promising attack vectors for Phase 2

Based on the above gap analysis, the three most promising attack vectors for a Phase-2 research program (theoretical/computational) are:

### Vector A — Strengthen Tao 2022's log-density to natural density

This is Tao's own suggested follow-up. Concretely: prove a fine-scale mixing result for the Markov chain on $(\mathbb{Z}/3^n\mathbb{Z})^\times$ induced by the Syracuse map. The technical ingredient is bounding $\|\widehat{\mathrm{Syrac}_n} \mathbf{1}_{|\xi| > 3^{n-\delta n}}\|_\infty$ in a strong sense — a uniform decay rather than $L^2$ decay. The Tao 2020 blog post proves submultiplicativity of $c_n$; what is needed is a lower bound $c_n \ge 3^{-n - o(n)}$.

*Tools.* Fourier analysis on $\mathbb{Z}/3^n\mathbb{Z}$; large-sieve-style methods; possibly automorphic-form input via the rational $\log_2 3$.

*Expected impact.* Upgrade Tao 2022 to natural density. Does NOT close the conjecture but converts it into "for every $N$, $\mathrm{Col}_{\min}(N) \le f(N)$ up to a sparse set", which is a far more useful starting point.

### Vector B — Construct a Lyapunov function via 2-adic representation theory

Akin 2004 frames the question: find a function $V : \mathbb{Z}_2 \to \mathbb{R}_{\ge 0}$ such that $V$ restricted to $\mathbb{N}$ provides a Lyapunov function for $T$. The 2-adic conjugacy $\Phi$ tells us that on $\mathbb{Z}_2$ there is no such $V$ (the shift is conservative). So any $V$ must distinguish $\mathbb{N}$ from $\mathbb{Z}_2 \setminus \mathbb{N}$ — a *boundary* (in 2-adic topology) condition.

*Tools.* 2-adic Lie group representations; Mahler functionals on $\mathbb{Z}_2$; possibly $p$-adic harmonic analysis.

*Expected impact.* This is the riskiest but most direct approach. A success would close the conjecture entirely; a failure would still produce structural obstructions of independent interest (in line with Akin 2004's program).

### Vector C — Hybrid cycle-exclusion via $\log_2 3$ irrationality measure

Steiner–Simons–de Weger–Hercher have pushed cycle exclusion to $m \le 91$ using Baker's theorem. The bottleneck is the effective irrationality measure of $\log_2 3$, currently $\le 5.something$ via Baker's method. Any unconditional improvement of the irrationality measure of $\log_2 3$ would automatically push cycle-exclusion to a much higher $m$. This is *not* a Collatz technique per se, but it would translate effort in Diophantine approximation into bigger $m$-bounds.

*Tools.* Effective transcendence theory; Padé approximants to $\log_2 3$; the LLL algorithm for finding sharper continued-fraction-style relations.

*Expected impact.* Modest in scope (only rules out cycles of bounded $m$), but uses well-developed external techniques that may give immediate gains. Useful as a "low-risk" parallel branch alongside (A) and (B).

(A) is the most cited, (B) the most ambitious, (C) the lowest-risk. For Phase 2 we recommend pursuing **(A) as the primary track and (C) as a fast parallel track**, with **(B) as exploratory background**.

---

## 12. Selected references and pointers to bibliography

Full bibliographic data is in `bibliography.bib`. Open problems extracted from the above are in `open_problems.md`. Key reading list:

1. **Lagarias 1985** — orientation survey.
2. **Lagarias 2010** book — read the Tao-style overview and the Steiner reprint.
3. **Tao 2022** + 2019/2020 blog posts — the modern state of the art.
4. **Krasikov–Lagarias 2003** — the strongest pre-Tao density result.
5. **Bernstein–Lagarias 1996** + **Akin 2004** — the 2-adic point of view.
6. **Simons–de Weger 2005** + **Hercher 2023** — cycle exclusion.
7. **Barina 2025** — current verification state of the art.
8. **Conway 1972** + **Kurtz–Simon 2007** — undecidability of the broader class.

---

## 13. Caveats and honest disclaimers

A literature survey of the Collatz problem is uniquely hazardous because:

- **Crank density is high.** The arXiv hosts hundreds of "proofs" of the Collatz conjecture, almost all wrong. Within this survey we have restricted attention to peer-reviewed work (or to preprints by well-cited mathematicians of the field — Tao, Lagarias, Sinai, Akin, Conway). We have not relied on any unpublished "proof" of any subcase.

- **Multiple naming conventions exist.** Some papers use $\mathrm{Col}(n) = 3n+1$ (raw), others $T(n) = (3n+1)/2$ (accelerated), others $\mathrm{Syr}(n) = $ largest odd divisor of $3n+1$ (Syracuse). When stating density exponents (e.g., Korec's $\log_4 3$ vs. $\log 3 / \log 2$), we have stuck with the convention used by Tao 2022. Be aware that constants appearing in older literature may use other conventions.

- **Direct PDF access was frequently blocked during this survey.** Several theorem statements were assembled from multiple search-result snippets rather than from direct PDF extraction. We have tried to flag remaining uncertainty with [PARTIAL] / [UNVERIFIED] tags. Where a result is *only* paraphrased and a precise version exists in the source, we recommend Phase 2 directly download the PDFs (perhaps via institutional access) to lock down the exact statements.

- **Numerical constants in the literature are sometimes inconsistent.** For example: the "5.76 × 10^18" Oliveira–e-Silva bound is sometimes quoted as "20 × 2^58" and sometimes as "5.764 × 10^18", which agree to 4 significant figures but should be checked in any paper-ready citation.

End of survey.
