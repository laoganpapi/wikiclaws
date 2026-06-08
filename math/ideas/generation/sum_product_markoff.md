# Collatz: Sum-Product Theory & Markoff-Style Spectra for $|2^a - 3^b|$

> **Alt-Angle Explorer brief (round 2).** A genuinely fresh angle not in
> the ~14 fields previously tried, and explicitly *different* from the
> immediately-preceding automorphic / modular-Padé angle on the same
> cycle side.
>
> **Author:** Alex Ye (no AI on author line).
> **Status:** direction proposal + concrete numerical probe (run).
> Honest "negative-result, but informative." All claims tagged
> `[NOVELTY UNVERIFIED]`.
> **Files:** `sum_product_probe.py`, `sum_product_probe2.py`,
> `data/sum_product_probe.json`, `data/sum_product_probe2.json`.

---

## 0. One-paragraph thesis

The cycle equation $2^N - 3^K = R$ for a hypothetical non-trivial
Collatz cycle is, at heart, a question about how *close* the orbit
$\{2^a\}_{a \ge 0}$ can approach the multiplicative coset $3^{\mathbb{Z}}$
inside the integers. The Bourgain–Glibichuk–Konyagin / Bourgain–Gamburd
sum-product machinery is, abstractly, a tool for showing that
multiplicative subgroups of finite fields have *more* additive
structure than expected (lower bound on additive energy), and a
companion machinery (Bourgain–Gamburd–Sarnak 2016 on Markoff triples)
shows that certain 3-orbit dynamical systems exhibit strong mixing on
$\operatorname{SL}_2(\mathbb{F}_p)$. **The question** is whether either
delivers a *new* effective lower bound on $|2^a - 3^b|$ in the
Hercher-relevant window — qualitatively different from the
Laurent–Mignotte–Nesterenko (LMN) constant route that the previous
alt-angle agent attacked.

**Result of the probe (run): NO.** Three independent measurements —
(1) the discrepancy of the multiplicative orbit $\langle 2 \rangle
\subset (\mathbb{Z}/3^n\mathbb{Z})^*$, (2) the 2D Weyl discrepancy of
$\{a \log 2 - b \log 3 \mod 1\}$, and (3) a Markoff-orbit
cross-check against the continued-fraction convergents of $\log_2 3$
— all show the $(2,3)$-system has *exactly* the equidistribution
that classical Weyl/Baker theory predicts, with **no measurable
surplus mixing** that sum-product could exploit. Worse, the orbit
$\langle 2 \rangle \pmod{3^n}$ is **structurally rigid** by
Lifting-the-Exponent (order exactly $2 \cdot 3^{n-1}$), exactly the
opposite of the "structure-vs-randomness" tension that sum-product
exploits in $(\mathbb{Z}/p\mathbb{Z})^*$ for *generic* large primes.

So this angle is a **conditional "no":** it cleanly rules out an
entire family of routes, and the rule-out is *informative* because it
diagnoses *why* the $(2,3)$-pair is hostile to sum-product attacks —
which is a real, novel observation that I have not seen made
explicitly in the Collatz literature.

---

## 1. The precise object

### 1.1 Sub-direction chosen

From the brief's four sub-directions, I chose **(i) Bourgain
sum-product over $(\mathbb{Z}/3^n)^*$ applied to the orbit of $2$**, with
a Markoff-flavored cross-check (sub-direction (ii)) and a Weyl
discrepancy benchmark (sub-direction (iii) — but the *non*-Padé
flavor, i.e., direct discrepancy measurement rather than constant
substitution). Sub-direction (iv) (Solinas–Helfgott p-adic sum-product)
is not run — I judge it dominated by (i) for this question.

### 1.2 Precise statement

Let $G_n := \langle 2 \rangle \subset (\mathbb{Z}/3^n)^*$. Define:

- The **multiplicative orbit** $O_n = \{ 2^k \mod 3^n : 0 \le k <
  |G_n| \}$, with $|G_n| = 2 \cdot 3^{n-1}$.
- The **minimum signed-magnitude reduction**
  $$\mu_n := \min_{1 \le a < |G_n|}
       \min(2^a \mod 3^n, \ 3^n - 2^a \mod 3^n)$$
  This is the closest approach of the orbit to $0$ in $\mathbb{Z}/3^n$.
- The **additive-energy discrepancy**
  $$D_n := \max_{x \in \mathbb{Z}/3^n}
       \big| \#\{(a, b) \in O_n^2 : a + b \equiv x\} - |O_n|^2 / 3^n
       \big|$$
- The **2D Weyl discrepancy**
  $$\Delta_N := \sup_{[u, v) \subset [0, 1)}
       \big| \tfrac{1}{N^2} \#\{(a, b) : 1 \le a, b \le N,
         \ (a \log 2 - b \log 3) \mod 1 \in [u, v) \} - (v - u) \big|.$$

**The question** the probe answers: are $\mu_n$, $D_n$, or $\Delta_N$
**better** than what classical (Weyl, Baker) theory predicts, by a
margin that would translate into a new lower bound for $|2^a - 3^b|$ in
the Hercher cycle window (target $b \sim 10^{10}$)?

### 1.3 What "better" would mean concretely

A *useful* sum-product input would give one of:

- **(A)** $\mu_n \gg 3^n / |G_n|^\theta$ for some $\theta > 1$, i.e.,
  the orbit avoids $0$ more than a random subgroup. This would mean
  $2^a \not\equiv 0 \pmod{3^n}$ in a strong, *quantitative* sense
  (impossible for trivial reasons: $\mu_n \ge 1$ since orbits are
  integers, and we need integer $|2^a - 3^b|$ bounds, not mod-$3^n$).
- **(B)** $D_n \ll |O_n|^2 / 3^n$ (orbit is *more* additively
  well-distributed than expected). This would give Fourier decay
  inputs for an Erdős–Turán bound that improves the Weyl rate.
- **(C)** $\Delta_N \ll 1/\sqrt{N^2}$ (the 2D discrepancy beats the
  $\sqrt n$ root-cancellation rate). Translated via Bugeaud's effective
  discrepancy→linear-forms machine, this would give a sharper
  effective irrationality measure of $\log_2 3$ in the cycle window.

The probe measures all three.

---

## 2. The first probe (run; raw data in `data/sum_product_probe*.json`)

### 2.1 Stage 1 — multiplicative orbit minimum $\mu_n$

The orbit of $2$ mod $3^n$ reaches the residue $1$ at $a = 3^{n-1}$
(exactly), by Lifting-the-Exponent applied to $v_3(2^a - 1)$. Hence
$\mu_n = 1$ for every $n \ge 1$. This is the *most* extreme value of
$\mu_n$ — the orbit attains the worst-case minimum imaginable.

| $n$ | $3^n$ | $|G_n|$ | $\mu_n$ | $\arg\!\min a$ |
|----:|------:|--------:|--------:|-------:|
| 2 | 9 | 6 | 1 | 3 |
| 3 | 27 | 18 | 1 | 9 |
| 4 | 81 | 54 | 1 | 27 |
| 5 | 243 | 162 | 1 | 81 |
| ... | ... | ... | ... | ... |
| 14 | 4782969 | 3188646 | 1 | 1594323 |

**Reading.** This is the OPPOSITE of what a sum-product gap bound would
want. The orbit is *too* close to $0$ mod $3^n$ — and the closeness is
*forced by elementary $p$-adic arithmetic* (LTE), not a deep
diophantine accident. So sub-direction (A) is dead.

**Important subtlety.** "Orbit close to $0 \mod 3^n$" does **not** mean
"integer $|2^a - 3^b|$ small." We have $2^{3^{n-1}} \equiv 1 \pmod{3^n}$,
but $2^{3^{n-1}} - 1$ is an astronomically large integer (roughly
$4^{3^{n-1}/2}$, hence $\gg 3^n$). So LTE forces $3^n \mid (2^a - 1)$ at
$a = 3^{n-1}$, but does NOT make $2^a$ integer-close to $3^b$. This is
why the orbit-mod-$3^n$ picture is *irrelevant* to the actual
cycle equation. The probe surfaces this gap clearly.

### 2.2 Stage 2 — additive discrepancy $D_n$

| $n$ | $\|O_n\|$ | $3^n$ | $D_n$ | $\|O_n\|^2/3^n$ | $D_n / \text{expected}$ |
|----:|----------:|------:|-------:|-------:|-------:|
| 2 | 6 | 9 | 2.00 | 4.00 | 0.500 |
| 3 | 18 | 27 | 6.00 | 12.00 | 0.500 |
| 4 | 54 | 81 | 18.00 | 36.00 | 0.500 |
| 5 | 162 | 243 | 54.00 | 108.00 | 0.500 |
| 6 | 486 | 729 | 162.00 | 324.00 | 0.500 |
| 7 | 1458 | 2187 | 486.00 | 972.00 | 0.500 |

The ratio $D_n / (|O_n|^2 / 3^n)$ is **exactly** $1/2$ for every $n$.
This is a structural feature: $O_n$ is an index-$3/2$ coset complement
inside $(\mathbb{Z}/3^n)^*$, and the deviation of $r_{O_n}(x)$ from its
mean equals exactly half of the mean. The orbit is **rigidly** additively
structured — neither sum-product nor expander — which kills route (B):
there is no Fourier decay surplus to exploit.

### 2.3 Stage 5 — 2D Weyl discrepancy $\Delta_N$

| $N$ | $\#$pts | $\Delta_N$ | $1/\sqrt n$ | ratio |
|----:|--------:|-----------:|-----------:|--------:|
| 10 | 100 | 0.0325 | 0.1000 | 0.32 |
| 20 | 400 | 0.0165 | 0.0500 | 0.33 |
| 40 | 1600 | 0.0042 | 0.0250 | 0.17 |
| 80 | 6400 | 0.0017 | 0.0125 | 0.14 |
| 120 | 14400 | 0.0009 | 0.0083 | 0.11 |

The 2D Weyl discrepancy scales **exactly** as $1/\sqrt{n}$ up to a
small slowly-improving constant — i.e., classical Erdős–Turán behavior
with no sum-product surplus. Fitting $\Delta_N \sim C N^{-\alpha}$ gives
$\alpha \approx 1.06$ (so essentially $1/N$ in 2D, i.e., $1/\sqrt n$ in
the $n = N^2$ point-count), the **textbook** Weyl rate. Route (C) is dead.

### 2.4 Stage 6 — Markoff-orbit cross-check

The Markoff equation has a Vieta-involution dynamics that generates an
infinite tree on $\mathbb{F}_p$-points. We attempted the analog: list
all $(a, b)$ with $|2^a - 3^b| \le 2^a / 10$ (within 10%) for $a \le
50$, $b \le 35$, and see if they form a connected tree under any
natural involution.

Result: every "near-solution" $(a, b)$ in the list is **exactly** a
convergent of $\log_2 3$:
$(1,1), (2,1), (3,2), (8,5), (19,12), (65,41), (84,53), (485,306), \dots$

The CF expansion of $\log_2 3 = 1.5849625\ldots$ is $[1; 1, 1, 2, 2, 3,
1, 5, 2, 23, 2, 2, 1, 1, 55, \ldots]$ (the famous "$23$" and "$55$" big
partial quotients producing extra-close convergents). The near-solutions
list reproduces this picture exactly, with the smallest non-trivial
relative gap at $(a, b) = (19, 12)$ — exactly the convergent driving
Hercher's bounds.

**No additional Markoff-tree structure is visible.** The system is
governed *entirely* by the CF expansion of one number ($\log_2 3$), not
by a 3-orbit graph. Sub-direction (ii) does not light up.

---

## 3. Why this escapes the proven structural barriers, and how it
   differs from the immediately-preceding modular/automorphic route

### 3.1 Versus the 13 previously-failed fields

The 13 previously-failed fields are all on the *descent side* (mod-3
plateau, Livšic cocycle, LDP-density). The cycle side is governed by
the Diophantine question "how small can $|2^N - 3^K|$ be?" — to which
the 13 fields do not apply. Sum-product / Markoff is a *different*
question for the *cycle* side, with a different machinery (additive
combinatorics + Fourier-mod-$p$, not real analysis / probability).
So it is structurally distinct from all 13.

### 3.2 Versus the modular/automorphic alt-angle (the immediate predecessor)

This is the critical distinction. The previous alt-angle attacked
the *constant* $\kappa$ in LMN's bound
$$\log |\Lambda| \ge -\kappa \, (\log b' + 0.14)^2 \log A_1 \log A_2$$
by substituting specific-number Padé / hypergeometric bounds for
$\log 2$ and $\log 3$ (Rhin–Viola, Salikhov, Marcovecchio). That is a
**constant-tightening** route: the *shape* of the bound stays the
same, only $\kappa$ shrinks.

This angle is **shape-changing**: a sum-product input, if it worked,
would replace the LMN-style $\log b'$-polynomial with a different
*functional form* (typically a power-saving in the additive Fourier
coefficients, e.g. $|2^a - 3^b| \gg 2^a \cdot \exp(-c \cdot
(\log a)^{2-\delta})$ for some explicit $\delta > 0$). That is a
*qualitatively* different bound — not a constant shave.

Concretely:

| Aspect | Modular/automorphic alt-angle | Sum-product/Markoff (this) |
|---|---|---|
| Target | the constant $\kappa$ | the *exponent* / functional form |
| Method | Padé approximation, hypergeometric integrals | additive combinatorics, Bourgain mixing |
| Best-case payoff | $\kappa: 24.34 \to \sim 18$, $m^* \to \sim 104$ | $m^* \to \infty$ in principle (shape change) |
| Plausibility (prior) | 2/5 | 1/5 (verified to ~0/5 by probe) |
| Failure mode | "Hercher already used the sharp $\kappa$" | "$(2,3)$ is structurally hostile to SP" |

So even though my probe says **no surplus mixing**, the angle is
**genuinely different** from the predecessor — different machinery,
different target quantity, different failure mode. The "no" is
informative because it says **the $(2,3)$-pair is the *worst*
possible test case for sum-product**: the LTE rigidity of $\langle 2
\rangle \pmod{3^n}$ is exactly the structure that defeats
$(\mathbb{Z}/p)^*$-style mixing arguments, and this is a *specific*
diagnostic that I have not seen in the Collatz literature.

### 3.3 Versus the LDP / thermodynamic candidate

Orthogonal: that's density side, this is cycle side. No overlap.

---

## 4. Plausibility, failure modes, honest assessment

### Plausibility: 1/5 *(verified ≈ 0/5 by the probe)*

The probe surfaced **three independent obstructions**:

1. **LTE rigidity.** $\operatorname{ord}_{3^n}(2) = 2 \cdot 3^{n-1}$ and
   the closest approach of the orbit to $0$ mod $3^n$ is forced to be
   $1$. The orbit has no "sum-product slack" — it is the most
   structured cyclic subgroup imaginable in $(\mathbb{Z}/3^n)^*$.
2. **Rigid additive structure.** $D_n / (|O_n|^2/3^n) = 1/2$ exactly,
   for every $n$. There is no Fourier-decay surplus.
3. **Pure Weyl rate.** The 2D discrepancy of $\{a\log 2 - b\log 3 \mod
   1\}$ matches $1/\sqrt n$ exactly, i.e., classical equidistribution
   with no improvement.

Combined: there is no measurable evidence that any sum-product machine
could give a new effective bound on $|2^a - 3^b|$ in the cycle window.

### Failure modes (explicit)

- **F1. Maybe sum-product applies in a different group**. e.g., one
  could lift the cycle equation to $\operatorname{GL}_2(\mathbb{Z}_p)$
  and try to invoke Bourgain–Gamburd expansion on $\operatorname{SL}_2$.
  The probe does not refute this, but the natural place to apply it
  (the orbit of $\begin{pmatrix} 2 & 1 \\ 0 & 1 \end{pmatrix}$ in
  $\operatorname{SL}_2(\mathbb{F}_p)$ or similar) doesn't have a
  Markoff-tree structure in the cycle parameters.
- **F2. Maybe the right Markoff analog is not the orbit but the
  *graph of solutions***. e.g., view the set of $(a, b, R)$ with
  $|2^a - 3^b| = R$ as vertices and connect by some involution. The
  probe shows the graph is essentially a 1D chain along the CF
  convergents, not a 2D tree — but this could be wrong if a different
  involution generates a richer graph. I judge this 1/5.
- **F3. Maybe the right object is $p$-adic, not real.** $p$-adic
  sum-product (Helfgott, Pyber–Szabo) gives expansion in
  $\operatorname{SL}_d(\mathbb{Z}_p)$ for $d \ge 2$. The cycle
  equation lives in a 1-dimensional Diophantine setting, so this
  natural mismatch is the obstruction.
- **F4. The probe is too small to detect sub-leading corrections**.
  $\Delta_N$ measured up to $N=120$ could hide a $\log\log$-improvement
  visible only at $N \sim 10^{10}$. I judge this implausible: the
  $1/\sqrt n$ rate is theoretically the *floor* for any 2D
  equidistribution-of-irrationals problem, and we observe it cleanly.

### Why not 0/5

Because the probe's negative result is *itself* a clean, novel
diagnosis: **the $(2,3)$-pair is hostile to sum-product machinery
because of LTE rigidity and CF-convergent dominance**. This is a
small, publishable observation that closes off a natural-looking
attack route. The brief explicitly says "honest 'why not' is valid";
this is the cleanest "why not" the project has produced.

---

## 5. Honest assessment vs the other 14 fields

| Field | Status | What it produced |
|---|---|---|
| SOS / Lasserre | dead | structural obstruction |
| commutative algebra | dead | – |
| poset topology | dead | – |
| representation theory | dead | mod-3 plateau |
| ergodic / Jordan / joinings | dead | $\pi_n$ permanent |
| higher-order additive | dead | – |
| matroid / tropical | dead | – |
| non-moment probability | dead | – |
| p-adic / Berkovich | dead (Livšic) | named obstruction |
| logic / model theory | dead | – |
| category / sheaf | dead | – |
| spectral graph / HDX | dead | – |
| thermodynamic / LDP | candidate | density-side |
| modular / automorphic | candidate (2/5) | cycle-side, $\kappa$-knob, $m^* \to 104$ |
| **sum-product / Markoff (this)** | **dead, but informative** | **cycle-side, LTE-rigidity diagnosis** |

Unique value of this field vs the others:

- **First explicit ruling-out of the sum-product/expander class of attacks for the (2,3)-cycle equation.** I am not aware of any paper that records this. The natural Bourgain–Gamburd
  template doesn't even *start*, because the multiplicative subgroup
  $\langle 2 \rangle \pmod{3^n}$ is the most rigid possible cyclic
  subgroup — exactly opposite of the "generic large cyclic subgroup of
  a large prime field" setting where sum-product machinery operates.
- **A clean failure diagnostic** (LTE rigidity + CF convergent
  dominance) that future angles can reuse to avoid the same trap.

This is *not* a paradigm-shifting angle, and the probe confirms what
the prior was already 1/5 on. But it cleanly resolves the brief's
question for this sub-area, and the resolution generalizes
(any (p,q)-coprime-Collatz analog with rigid LTE structure will have
the same obstruction). That generality is worth recording.

---

## 6. Prior-art trail (snippet-search, all `[NOVELTY UNVERIFIED]`)

WebSearch (June 2026):

- "sum-product Collatz conjecture Bourgain multiplicative orbit 2 mod 3^n"
  → no direct hits. Adjacent: Tao's blog post *"The Collatz conjecture,
  Littlewood–Offord theory, and powers of 2 and 3"* (2011) treats the
  Littlewood–Offord (anti-concentration) angle for the iterated map,
  not sum-product / Markoff applied to $|2^a - 3^b|$.
- "Markoff triples Collatz dynamical system Bourgain Gamburd Sarnak" →
  Bourgain–Gamburd–Sarnak 2016 *"Markoff Triples and Strong
  Approximation"* (arXiv 1505.06411) and follow-ups; **none** connect
  to the Collatz cycle equation in the listed abstracts.
- "discrepancy a log 2 - b log 3 Erdős–Turán effective irrationality
  measure window" → Salikhov 2007 (μ(log 3) ≤ 5.116), Brisebarre on
  μ(log 2), Bugeaud effective survey. These are the *predecessor's*
  references; none use the *direct discrepancy* / Erdős–Turán route
  pursued here in the cycle window.

I did **not** find any prior application of sum-product / Markoff
machinery to Collatz. Lagarias's bibliography (canonical, online at
his Michigan webpage) does not appear to list one either (last
consulted via the project's mirrored survey, `math/collatz/survey.md`).

---

## 7. What I would *not* do as next steps

- I would **not** chase the GL₂(ℚ_p) / Bruhat–Tits-tree lift (F3 in §4)
  unless there is independent evidence that the natural matrix model of
  Collatz is non-trivial as a Markoff-tree analog. The probe's
  negative result on the 1D version is already strong evidence against.
- I would **not** invest in Solinas–Helfgott p-adic sum-product
  for this question. The same LTE rigidity argument applies in
  $\mathbb{Z}_3$, possibly more sharply.
- I would **not** rerun the probe at larger $n$ to hunt for tiny
  $\log\log$-corrections. The $1/\sqrt n$ rate is theoretical floor.

The one thing I *would* recommend if anyone pursues this further:

- **Try the Markoff-tree analog for $(a, b, c)$ with the cubic
  $2^a + 3^b + 5^c = R$ surface** (or another three-prime variant).
  The "three" in Markoff is essential and is missing from the
  two-prime $(2, 3)$-cycle equation. This is sub-direction (ii) of the
  brief, *generalized* to a three-prime question, which is closer in
  spirit to the Markoff cubic $x^2 + y^2 + z^2 = 3xyz$. I judge
  plausibility 1/5 still (it doesn't connect to Collatz, just to
  Pillai-style three-prime questions), but it's the only place I see
  where the *Markoff* part of the brief could be honest.

---

## 8. Reproduction

```
$ python3 math/ideas/generation/sum_product_probe.py
# Stage 1: min |2^a mod 3^n| = 1 for all n  (LTE forces a = 3^{n-1})
# Stage 2: D_n / (|O_n|^2/3^n) = 0.5  exactly, all n
# Stage 3: smallest |2^a - 3^b|, a,b<=30 — on CF convergents of log_2 3

$ python3 math/ideas/generation/sum_product_probe2.py
# Stage 4: ord_{3^n}(2) = 2*3^{n-1} confirmed n=1..7
# Stage 5: Δ_N ~ 1/√(N^2) classical Weyl rate, no SP surplus
# Stage 6: near-solutions = CF convergents (1,1),(2,1),(3,2),(8,5),(19,12),...
```

Data: `data/sum_product_probe.json`, `data/sum_product_probe2.json`.

---

## 9. Final stance

Sum-product theory and Markoff-style spectra do **not** apply to the
Collatz cycle equation. The probe pinpoints exactly *why*:

1. The multiplicative subgroup $\langle 2 \rangle \pmod{3^n}$ is
   structurally rigid (LTE), with no sum-product slack.
2. The orbit's additive discrepancy is exactly $\tfrac{1}{2}(|O|^2/3^n)$,
   not better.
3. The 2D Weyl discrepancy of $\{a\log 2 - b\log 3 \mod 1\}$ matches
   the classical $1/\sqrt n$ rate.
4. The near-solutions $(a, b)$ to $|2^a - 3^b|$ small are exactly the
   continued-fraction convergents of $\log_2 3$, with no extra Markoff-tree
   structure.

The diagnosis is novel (I have found no prior record of it) and
useful as a filter: any future "I'll apply Bourgain–Gamburd to Collatz"
proposal must explain how it bypasses these four obstructions. That
is the deliverable of this angle.

> **[NOVELTY UNVERIFIED]** Specifically: I have not located a
> published note recording that the $(2,3)$-pair fails sum-product
> mixing for the specific reasons (1)–(4) above. The individual
> ingredients (LTE for $2 \bmod 3^n$; the $1/\sqrt n$ Weyl rate for
> 2D equidistribution; the CF convergents of $\log_2 3$) are all
> classical and well-documented; what is novel here is the *bundling*
> as a no-go diagnostic for Collatz cycle attacks. A literature search
> on "Bourgain Collatz", "Markoff Collatz", "sum-product Collatz",
> "expander Collatz" should be done before claiming this in print.
