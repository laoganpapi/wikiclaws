# Dead Ends — Collatz theory track (Vectors A and C)

**Purpose.** Append-only record of sub-approaches that did NOT work. Vector A
entries (upgrade of Tao 2022 from logarithmic to natural density) come first;
**Vector C entries (cycle exclusion) are appended at the bottom.**
Companion to `shared/dead_ends.md` (project-wide), `theory/tao_syracuse_explicit.md`
(Vector A), and `theory/cycle_exclusion_explicit.md` (Vector C).

Read before re-attempting any of these.

Template per `shared/dead_ends.md`. Entries append below; do not edit prior entries.

---

## 2026-06-02 — [collatz] — "The dyadic decomposition $N=2^a m$ is the source of log-density"

**Agent / author:** Alex Ye (AI-assisted).
**Time invested:** ~1 hour of theory.
**Attack vector:** Initial hypothesis that Tao uses log-density only because the
reduction $\Col_{\min}(N)=\Syr_{\min}(N/2^a)$ weights the dyadic shells $\{2^a\cdot\mathrm{odd}\}$
by $2^{-a}$, and that this weighting is intrinsically logarithmic. If true, fixing
the density notion would be a bookkeeping exercise on the $\nu_2$ decomposition.

**Why it failed:** The dyadic shell $\{N=2^a m: m\text{ odd}\}$ has natural density
$2^{-a}$ in $\NN$ *and* logarithmic density $2^{-a}$ — the two agree exactly on these
shells. Lemma 4.1 (proved in full in `tao_syracuse_explicit.md` §4.1) shows the
decomposition is **measure-neutral**: a natural-density-0 failure set on the odds
lifts to a natural-density-0 failure set on $\NN$. So this step is NOT where log-density
is forced. The real obstruction is one level deeper, in the stationarity of the
*sampling measure* under the multiplicative first-passage map (Proposition 4.2):
the map acts as a translation on $\log N$, which preserves $dN/N$ (log) but not $dN$
(natural). Re-pointed the whole analysis at that.

**Counter-example (if any):** n/a (the hypothesis was not false, just misidentified
as the bottleneck; the dyadic step is genuinely harmless, which is the opposite of
what the hypothesis needed).

**Pointer to artifacts:** `tao_syracuse_explicit.md` §4.1 (Lemma 4.1), §4.2 (Prop 4.2).
**Verdict:** abandoned (mis-localization corrected).
**Lesson:** Always check whether natural and log density *agree* on the specific
sets a reduction touches before blaming the reduction. They agree on dyadic shells;
the divergence between the two densities only appears under the multiplicative
(scale-changing) dynamics, which is exactly where Tao's transport lives.

---

## 2026-06-02 — [collatz] — "Amplify Tao's $n^{-A}$ Fourier decay to exponential $3^{-\theta n}$ by tensoring"

**Agent / author:** Alex Ye (AI-assisted).
**Time invested:** ~2 hours of theory.
**Attack vector:** Tao's Prop 1.17 gives $|\widehat\nu_n(\xi)|\le C_A n^{-A}$ (superpolynomial).
Natural density needs $|\widehat\nu_n(\xi)|\le C\,3^{-\theta n}$ (exponential), per Lemma 6.2.
Hope: $\Syrac(\ZZ/3^n\ZZ)$ is built from $n$ geometric inputs, so maybe it is (close to)
an $n$-fold convolution; then $\widehat\nu_n=\prod_j\widehat{(\cdot)}_j$ with each factor
$<1$ in modulus would give exponential decay $\prod_j(1-\delta)=e^{-\delta' n}$ for free,
upgrading $n^{-A}$ to $3^{-\theta n}$ by a soft tensor-power argument.

**Why it failed:** The convolution structure (eq (2.2)) is **skew, not direct**:
$$\Syrac(\ZZ/3^n\ZZ)\stackrel d= \Syrac(\ZZ/3^m\ZZ)+3^m2^{-(a_1+\cdots+a_m)}\Syrac'(\ZZ/3^{n-m}\ZZ).$$
The second block is dilated by the *random unit* $3^m2^{-(a_1+\cdots+a_m)}$, so the frequency
the second block "sees" is itself randomized by the first block's geometric variables.
Hence $\widehat\nu_n(\xi)\ne\prod_j(\text{per-factor})$; there is no per-coordinate product
formula to multiply. This skewness is precisely why Tao's submultiplicativity (2.3)
$c_{n_1+n_2-1}\ge c_{n_1}c_{n_2}$ goes only in the *lower-bound-on-min-atom* direction
and CANNOT be reversed into an exponential *upper* bound on $|\widehat\nu_n|$. Numerically,
$c_n3^n$ decreases slowly ($1.00,0.286,0.165,0.145,0.108$ for $n\le5$) — consistent with
the possibility $\beta>1$, i.e. a genuine *failure* of the exponential rate, which a soft
argument could never rule out. Tensoring is dead.

**Counter-example (if any):** Structural: the skew dilation breaks the product form.
No numerical counterexample needed; the method simply does not produce the claimed product.

**Pointer to artifacts:** `tao_syracuse_explicit.md` §6.4 (first bullet); `verify_syracuse_rv.py`
(the $c_n3^n$ column).
**Verdict:** gap-not-closeable (by this method).
**Lesson:** The skew convolution is the heart of the difficulty. Any approach to
$\mathrm{MIX}(\theta)$ must engage the randomized-frequency coupling directly (it is a
genuine exponential-sum cancellation problem, §6.3 (B2)), not route around it via a
product/tensor identity. This is the same wall as Tao's $\beta=1$ conjecture.

---

## 2026-06-02 — [collatz] — "Use the untilted law in the natural-density transport"

**Agent / author:** Alex Ye (AI-assisted).
**Time invested:** ~1.5 hours of theory.
**Attack vector:** Try to run Tao's transport directly under natural-density sampling
$dN$ using the *plain* (untilted, $s=0$) Syracuse distribution, hoping the only change
from the log-density argument is the sampling measure and that the residue equidistribution
is identical.

**Why it failed:** Under $dN$ the first-passage map's pushforward acquires a Radon–Nikodym
factor $e^{-D_n}$ (Prop 4.2), $D_n=\sum a_j\log2-n\log3$ the log-drift. The plain law has
$\EE_0[\sum a_j]=2n$, so $\EE_0[D_n]=(2\log2-\log3)n=n\log(4/3)>0$: the untilted measure
drifts, and the $e^{-D_n}$ tilt is NOT mean-neutral — it systematically reweights toward
*smaller* drift (slower descent), which is exactly the wrong direction and does not converge
to a stationary natural-density measure. The correct fix is to tilt the geometric inputs to
$s^*$ with $\EE_{s^*}[a]=\log_2 3$, making $\EE_{s^*}[D_n]=0$ (eq (5.2)); only then is the
natural-density measure approximately stationary. Hence the *tilted* law $\Syrac_{s^*}$, not
the plain law, is the object whose equidistribution (Hypothesis $\mathrm{MIX}(\theta)$, eq (5.3))
must be established.

**Counter-example (if any):** The drift $\EE_0[D_n]=n\log(4/3)\ne0$ is the obstruction;
explicit and unavoidable for $s=0$.
**Pointer to artifacts:** `tao_syracuse_explicit.md` §5.1 (Remark 5.1), §4.2 (Prop 4.2).
**Verdict:** abandoned (corrected — led to the tilt formulation, which is the right one).
**Lesson:** Natural-density stationarity *requires* the descent-balance tilt $s^*$ with
$\EE_{s^*}[a]=\log_2 3$ (the Korec balance point). This is why $\mathrm{MIX}(\theta)$ is stated
for the tilted law: it is not a cosmetic change, it is forced by drift-neutrality. A pleasant
by-product: the same constant $\log_2 3$ that governs Korec's descent exponent reappears as
the unique natural-density-stationary tilt — a small unification, not a coincidence.

---

## 2026-06-02 — [collatz] — "Hope that the descent-balance tilt $s^*$ restores TV-equidistribution of the Syracuse law"

**Agent / author:** Alex Ye (AI-assisted).
**Time invested:** ~2 hours theory + compute.
**Attack vector:** Having reduced the natural-density upgrade to $E_n^{(s^*)}:=\varphi(3^n)\mathrm{CP}_n^{(s^*)}-1\to0$
(exact-leading-constant equidistribution of the *tilted* Syracuse law; eq (6.4) of
`tao_syracuse_explicit.md`), and having found the *untilted* law fails this ($E_n\sim0.31n\to\infty$),
the natural hope was: the descent-balance tilt $s^*$ (which removes the mean log-drift) would
re-center the distribution and restore $E_n^{(s^*)}\to0$. Verify numerically.

**Why it failed:** Computed $E_n^{(s^*)}=0.212,0.854,1.772,3.090,4.972,7.643$ ($n=1..6$,
`verify_syracuse_rv.py:collision_study`): grows **super-linearly** and is **larger** than the
untilted $E_n$ at every $n$. Mechanism: the tilt $s^*\approx0.438$ *thins* the geometric tail
(lowers $\EE[a]$ from $2$ to $\log_23$), concentrating the valuations $a_j$ and *lowering the
entropy* of the multiplier $2^{-\sum a_j}$, which *raises* the collision probability. Drift-
neutrality (needed for natural-density *stationarity*) and high entropy (needed for residue
*equidistribution*) pull in opposite directions under a single scalar tilt. So at small $n$
the tilt makes equidistribution strictly worse.

**Counter-example (if any):** The tilted excess values above; explicit and reproducible.
**Pointer to artifacts:** `tao_syracuse_explicit.md` §6.4 (tilted finding + readings (i)/(ii)/(iii)),
`experiments/verify_syracuse_rv.py` (`collision_study`), `verify_syracuse_rv_log.md` item 5.
**Verdict:** abandoned at small $n$ — NOT a refutation (the requirement is asymptotic; small-$n$
growth could reverse), but it kills the easy optimism and is logged as a genuine negative datum.
**Lesson:** Do not assume drift-neutrality implies equidistribution — they are *different* and here
*antagonistic* properties. The single-scalar Esscher tilt of §5.1 is likely too crude; the right
object may be a $\xi$- or $n$-dependent tilt, or natural density may genuinely fail (reading (iii)),
which would redirect effort to Vector B. Decisive test: push $E_n^{(s^*)}$ to $n\sim10$–$14$ by FFT.

---
---

# VECTOR C — Cycle exclusion (Diophantine approximation)

Companion: `theory/cycle_exclusion_explicit.md`, `experiments/verify_cycle_exclusion.py`.

---

## 2026-06-02 — [collatz] — "Improve $m^\*$ by improving the irrationality measure of $\log_2 3$"

**Agent / author:** Alex Ye (AI-assisted).
**Time invested:** ~2 hours of theory + source verification.
**Attack vector:** The brief, `survey.md` §11 (Vector C), and `open_problems.md` D.1/D.2
all frame cycle exclusion as rate-limited by the *effective irrationality measure
$\mu(\log_2 3)$*. Plan: find the best post-2023 bound on $\mu$ (e.g. via $\mu(\log 3)\le5.116$,
Wu–Wang 2014) and plug it in to raise the excludable number of circuits $m$.

**Why it failed (what is solidly verified):** Reconstructing the argument
(`cycle_exclusion_explicit.md` §2, §5.1, double-confirmed via WebSearch) shows the published
Steiner–Simons–de Weger–Hercher proofs **do not use $\mu(\log_2 3)$ at all**: the *upper* bound
on cycle length comes from the **two-log linear-forms estimate** (Laurent/LMN; de Weger's form
$\Lambda>2^{-0.158K}$ for $K\ge32$), and the *lower* bound from **Crandall's lemma**. So the
constant that bounds $m^\*$ is the two-log estimate's leading constant ($24.34\,D^4$ / de Weger
exponent $0.158$) plus the circuit budget plus $B$ — improving $\mu(\log_2 3)$ touches none of
these. **Intuition (flagged `[CLAIM-UNVERIFIED]` in §5.2):** a one-dimensional measure gives only
a *polynomial* lower bound $\Lambda>K^{1-\mu}$ vs the two-log *linear-in-exponent* bound, which is
plausibly why it cannot substitute; but I did **not** rigorously prove "a $\mu$-route is impossible"
(the cycle's own forcing on $\Lambda$ is $K$-dependent, making the naive comparison delicate).

**Counter-example (if any):** n/a. (`verify_cycle_exclusion.py` C5b illustrates the
exponential-vs-polynomial decay-rate gap; it supports the intuition but is not a proof of impossibility.)

**Pointer to artifacts:** `cycle_exclusion_explicit.md` §5.1–§5.2, §7, §8; `verify_cycle_exclusion.py` C5.
**Verdict:** prior-art — the published method does not use $\mu(\log_2 3)$, so improving it is not the
route Vector C should pursue. (Not claiming a $\mu$-route is provably impossible; claiming it is not
the lever the proofs use.)
**Lesson:** The lever is the **two-log linear-forms estimate** (leading constant $24.34D^4$ /
de Weger exponent $0.158$), or the combinatorial circuit-budget, or the verification bound $B$ —
NOT the one-dimensional irrationality measure. `survey.md` §7.5/§11 and `open_problems.md` D.1/D.2
are wrong on this and should be corrected (`cycle_exclusion_explicit.md` §8).

---

## 2026-06-02 — [collatz] — Mis-framed Step-1 check (C5 v1): "two-log bound is numerically larger than the $\mu$ bound"

**Agent / author:** Alex Ye (AI-assisted).
**Time invested:** ~30 min.
**Attack vector:** First draft of `verify_cycle_exclusion.py` C5 tried to confirm "two-log is the
binding constraint" by comparing magnitudes $\log_{10}|\Lambda|_{\text{LMN}}$ vs
$\log_{10}|\Lambda|_{\mu}$ at the optimal convergent, expecting LMN to be larger.

**Why it failed:** Returned FALSE (the $\mu$ figure was larger at the convergent), aborting Step 1.
The *check* was wrong, not the literature: the relevant question is not "which lower bound is larger
at the optimal $N/K$" but "which decays fast enough in $K$ to cap the cycle length" (directionality).
A larger-magnitude but wrong-shape (polynomial) bound is useless.

**Counter-example (if any):** The FALSE output itself: at $K=10^3$, LMN $\log_{10}|\Lambda|\gtrsim-732$
vs per-convergent $\mu$ figure $\sim-12.5$; misreading this as "$\mu$ stronger" was the error.

**Pointer to artifacts:** `verify_cycle_exclusion_log.md` (Run 1 note); `verify_cycle_exclusion.py`
(rewritten C5a/C5b).
**Verdict:** falsified (the check), then corrected — C5 now tests de Weger's actual inequality
($K\ge32$ threshold, largest solution at $K=29$) and the slope/direction; both pass.
**Lesson:** When a Step-1 check fails, decide whether the *claim* or the *check* is wrong before
touching the theory. Here a sloppy check encoded a sloppy claim; fixing both resolved it. Textbook
`verification_protocol.md` anti-pattern caught.

---

## 2026-06-02 — [collatz] — Computing a concrete new $m^\*>91$ inside this environment

**Agent / author:** Alex Ye (AI-assisted).
**Time invested:** ~1 hour (mostly fighting source access).
**Attack vector:** Instantiate the corrected squeeze with (i) Barina's $B=2^{71}$ instead of
Hercher's $3\cdot2^{69}$, and/or (ii) the Laurent-2008 two-log constant instead of LMN-1995, to
claim $m^\*\ge92$.

**Why it failed (incomplete, not falsified):** Both need the **explicit function $F(m,\log B)$ and
constants from Hercher's paper** (arXiv:2201.00406 / JIS) and the **explicit improved constant from
Laurent 2008** (Acta Arith. 133.4). Every academic PDF host (arXiv + mirrors, JIS/uwaterloo, AMS,
ScienceDirect, ResearchGate, EUDML, matwbn, Leiden, Wikipedia) returned **HTTP 403** to both WebFetch
and sandboxed `curl`; only WebSearch snippets were available. Without Hercher's $F$ and the Laurent-2008
constant, a new $m^\*$ can only be asserted, not derived — which the ABSOLUTE RULES forbid.

**Counter-example (if any):** n/a (blocked, not false).
**Pointer to artifacts:** `cycle_exclusion_explicit.md` §6.4, §7.
**Verdict:** abandoned-in-environment (source access). The route is real; recommended next step when
PDFs are reachable: re-run Hercher's squeeze with $B=2^{71}$, an estimated honest $+1$ to $+3$ in $m^\*$.
**Lesson:** A correctly-cited published Diophantine input is required to claim a number. We have the
mechanism and the bottleneck identification (solid deliverables) but not a new bound.
