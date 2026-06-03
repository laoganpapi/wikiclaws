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

---

## 2026-06-02 — [collatz] — "Derive the upper bound $F(m)$ on cycle length from the self-contained geometry $\Lambda < m/B$"

**Agent / author:** Alex Ye (AI-assisted).
**Time invested:** ~4 hours theory + compute (the core from-scratch attempt).
**Attack vector:** Complete the `[PARTIAL-DERIV]` gap in `cycle_exclusion_explicit.md` by deriving the
upper bound $F(m)$ on the number of o-steps $K$ from first principles. Plan: derive an exact expression
for $\Lambda=N\log2-K\log3$ from the circuit structure, bound it from above in terms of $m$ and the
verified bound $B$, then combine with a transcendence lower bound on $\Lambda$ to cap $K$ from above.

**What SUCCEEDED (kept, now in `theory/cycle_bound_attempt.md` §2):** The exact telescoping identity
$\Lambda=\sum_{j=1}^m\varepsilon_j$, $\varepsilon_j=\log(1+(1-(2/3)^{a_j})/x_j)$ (Thm 3, verified to
$10^{-120}$), and the rigorous self-contained bound $0<\Lambda<m/x_{\min}<m/B$ (Cor 4, verified on
17,762 positive fixed points). These are genuine, fully-derived, citation-free deliverables.

**Why the GOAL failed (rigorously, Prop 5):** The bound $\Lambda<m/B$ is **constant in $K$**. Any
transcendence *lower* bound $\Lambda\ge\ell(K)$ (de Weger $2^{-0.158K}$, or LMN $\exp(-C(\log K)^2)$) is
**decreasing in $K$**. Combining $\ell(K)\le\Lambda<m/B$ therefore forces $\ell(K)<m/B$, which (since
$\ell$ decreases) holds for $K$ **large** — it bounds $K$ **below**, never above. So the self-contained
geometry reproduces only the *Crandall/lower* side of the squeeze ($K>\log_2(B/m)/0.158$), NOT the
upper bound $F(m)$. I tried three routes to a $K$-decaying upper bound on $\Lambda$ and all collapsed to
lower bounds on $K$: (a) bounding $R/3^K$ via $R=\sum_j(1-(2/3)^{a_j})P_{j-1}$ — but this identity is
**circular** for bounding $\Lambda$ (it gives $\Lambda\le(R/3^K)/x_{\min}$ with $R/3^K\sim x_{\min}\Lambda$,
i.e. $\Lambda\le\Lambda$); (b) bounding $x_{\min}$ below by a growing-in-$K$ function — but a genuine
cycle only forces $x_{\min}>B$ (fixed), giving no $K$-decay; (c) the partial-product $P_j$ bound — the
products can grow because $f_i=2^{b_i}(2/3)^{a_i}$ need not be $\le1$ individually.

**Counter-example (if any):** n/a — not falsified, this is a genuine *direction* obstruction proved as
Prop 5. The upper bound $F(m)$ genuinely exists (Simons $F(2)\approx8.6\times10^4$; Hercher $F(91)$) but
comes from the **sharper circuit-ratio averaging** ("analytical expression for the upper bound as a
function of $K$ and $L$"; Hercher's "bounds on averages/sums of an arbitrary number of terms"), which
needs the primary text — HTTP-403 here (arXiv:2201.00406, AMS, de Weger's site, JIS HTML, all blocked;
de Weger's site is in fact not in the sandbox network allowlist).

**Pointer to artifacts:** `cycle_bound_attempt.md` §2 (kept), §3 + Prop 5 (the obstruction);
`verify_cycle_bound.py` (D1–D5 PASS).
**Verdict:** gap-not-closeable (by self-contained geometry) — the **lower-bound side is now fully
reconstructed from scratch**; the **upper bound $F(m)$ remains** the residual, sharply localized to the
circuit-averaging step and contingent on Hercher's PDF.
**Lesson:** $\Lambda<m/B$ is the wrong tool for the *upper* bound on $K$ — it is constant in $K$ while
the contradiction needs an *upper* bound on $\Lambda$ that **decays in $K$**. The earlier note's
parenthetical (its §2 crude-estimate footnote) was right and is now proved (Prop 5). Effort to push
$m^\*$ must engage the circuit-ratio averaging directly, not the global $\Lambda$ bound.

---

## 2026-06-02 — [collatz] — "Power-law extrapolation of $F(m)$ to claim $m^\*\approx99$ at $B=2^{71}$"

**Agent / author:** Alex Ye (AI-assisted).
**Time invested:** ~1 hour compute.
**Attack vector:** Lacking Hercher's explicit $F(m)$, fit a power law $F(m)=c\,m^p$ through the two
anchors $(2,\,8.6\times10^4)$ and $(91,\,2.617\times10^{10})$, then read off the largest $m$ with
$F(m)\le G(2^{71})=3.489\times10^{10}$. This gives $p\approx3.31$ and $m^\*\approx99$ (i.e. $+8$ over 91).

**Why it failed (over-optimistic; not trustworthy):** $F(m)$ is LMN-determined, not a power law; a
2-point fit across the enormous range $m=2\to91$ has no claim to local accuracy at the crossover
$m\approx91$, which is exactly where $m^\*$ is decided. Cross-checking against Hercher's OWN datum —
pure verification-bound improvement moved $m^\*$ from 75 to 82 ($+7$) over $\approx10$ doublings of $B$,
i.e. $\approx0.7$ units of $m^\*$ per doubling of $G$ — and Barina/Hercher is only $\log_2(1.333)=0.415$
doublings, giving $\Delta m^\*\approx+0.3$, i.e. $m^\*\approx91$–$92$. The power-law's $+8$ is
$\sim25\times$ the Hercher-calibrated estimate. Kept only as the *optimistic* end of a bracket, loudly
marked `[PROVISIONAL]`.

**Counter-example (if any):** Internal inconsistency: the two models ($+8$ vs $+0.3$) disagree by an
order of magnitude, which is itself the signal that $F(m)$'s local slope (only in Hercher's PDF) is the
deciding unknown.
**Pointer to artifacts:** `cycle_bound_attempt.md` §6 (both models, bracketed); `verify_cycle_bound.py` D6.
**Verdict:** abandoned (untrustworthy extrapolation) — superseded by the conservative Hercher-calibrated
estimate $m^\*\in\{91,92\}$. The honest conclusion is **$B=2^{71}$ alone does not robustly beat 91**
(best case $+1$), correcting the earlier `cycle_exclusion_explicit.md` §6.4 optimism of "$+1$ to $+3$":
because Barina's bound is only $1.333\times$ Hercher's (not a full doubling), the realistic gain is
$\le+1$, and reaching the next convergent plateau $q_{23}=1.375\times10^{11}$ needs $B\ge2^{75.7}\gg2^{71}$.
**Lesson:** Never extrapolate an LMN-determined quantity by a 2-point power law across two decades of the
variable; calibrate the *local* slope from the literature's own incremental data. The cheap $B$-lever is
weaker than hoped because $2^{71}/(3\cdot2^{69})=2^{0.415}$ is far less than one doubling.

---

## 2026-06-03 — [collatz] — "Transfer-operator spectrum will give a new natural-density route"

**Agent / author:** Alex Ye (AI-assisted).
**Time invested:** ~3 hours of theory + computation.
**Attack vector:** Set up the Frobenius--Perron operator $P_n$ for the
Syracuse step on $(\mathbb{Z}/3^n\mathbb{Z})^\times$, compute its spectrum
exactly for $n\le 8$, hope that (a) a uniform spectral gap or (b) a clean
spectral identification of the mod-3 obstruction lets us bypass the
Plancherel-style Lemma 6.2 errors and prove natural density.

**Why it failed (as a route to a new bound, but the framing still helps):**
- The spectral gap of $P_n$ is **large** ($1-|\lambda_2(8)|\approx 0.995$),
  but **shrinking with $n$** ($|\lambda_2|$ grows from $0$ at $n=1$ to
  $5\times 10^{-3}$ at $n=8$). Log-linear extrapolation suggests growth
  $\sim 3^n$, which must turn over before $n=13$ (else $|\lambda_2|>1$).
  **No analytic bound on the asymptotic gap is produced.**
- The unique invariant distribution $\pi_n$ of $P_n$ is **exactly the
  Syracuse RV** ($\nu_n^{\text{Syrac}}$); proved algebraically
  (`theory/transfer_operator.md` §2.2) and verified to $10^{-16}$ for
  $n\le 6$. So everything `syracuse_fft/results.md` says about $E_n$
  diverging applies unchanged at the operator level. **The transfer-operator
  view does NOT change the $E_n$ divergence finding.**
- The mod-3 obstruction shows up as the explicit rank-1 2x2 block
  $P_n|_V = \binom{1/3\ 2/3}{1/3\ 2/3}$ on the mod-3 indicator subspace,
  with eigenvalue 1 and eigenvector $(1/3, 2/3)$. **This makes the
  obstruction sharper** (one linear-algebra fact, no Plancherel needed)
  but does NOT resolve it: the eigenvalue is permanently 1, by direct
  computation. The descent-balance tilt $s^*$ and the equidistributing
  tilt $s=-0.5$ both preserve the rank-1 structure with different fixed
  marginals; no scalar tilt makes the marginal uniform.
- Power iteration at $n=9$ converged to numerical zero ($\sim 10^{-16}$),
  not the true $|\lambda_2|$ — deflation against the all-ones right
  eigenvector was over-aggressive (the chain mixes very fast). ARPACK
  gave $|\lambda_2(n=7)|\approx 8\times 10^{-3}$ vs. numpy's full eig
  $\approx 3\times 10^{-3}$ — disagreement at the $\sim 30\%$ relative level
  for eigenvalues this small. **Float64 is at the edge of reliability
  here**; rigorous mpmath / interval arithmetic would be needed for
  $n\ge 7$ headline numbers.

**Counter-example (if any):** No counter-example; the framing is correct
but produces *no new analytic bound*. It recasts the known obstruction in
a cleaner form. The hope of a uniform $V^\perp$-gap as a route to
"coset-respecting natural density" is consistent with the data but not
proved; the data are also consistent with the perp-gap shrinking to 0.

**Pointer to artifacts:**
- `theory/transfer_operator.md` (full writeup, §10 honest bottom line)
- `experiments/transfer_operator.py` (kernel + spectrum)
- `experiments/transfer_operator_deep.py` (mod-3 / pi diagnostics)
- `experiments/transfer_operator_validate.py` (pi_n = Syracuse RV proof)
- `experiments/transfer_operator_final.py` (the data tables)
- `experiments/data/spectrum_table_*.json` and `spectrum_summary.txt`

**Verdict:** abandoned as a route to a *new* natural-density bound; kept
as a cleaner *statement* of the existing obstruction. The mod-3 2x2 block
(`theory/transfer_operator.md` Prop 3.1) and the invariant identification
(Prop 2.1) survive and may be useful expositionally.

**Lesson:** The "Markov chain / transfer-operator on $(\mathbb{Z}/3^n)^\times$"
is the *forward* picture in operator-theoretic clothes — its stationary
distribution IS Tao's Syracuse RV by an explicit shift-of-indices algebra
(W-recursion = one Markov step at the boundary $m=n$, mod $3^n$). So no
information is "added" by going adjoint. The mod-3 obstruction is robust
across formulations and is, *qua* spectral block, the rank-1 matrix
$\binom{1/3\ 2/3}{1/3\ 2/3}$. Future agents: don't expect the operator
view to bypass the obstruction; it makes the obstruction explicit, but
also makes its rigidity obvious.

---

## 2026-06-03 — [collatz] — "Binary-digit statistics (Hamming weight / runs / carries) as a Lyapunov function, pure or hybridized with $\log_2 n$"

**Agent / author:** Alex Ye (AI-assisted).
**Time invested:** ~1 hour (re-validation + writeup of an orphaned prior run).
**Attack vector:** Hope that a binary-digit observable $X(n)\in\{s(n)=\text{Hamming
weight},\,r(n)=\text{run-count},\,c(n)=\text{carry-count}\}$ is pointwise
anti-correlated with the magnitude jump of the $3n+1$ step, so that some hybrid
$L_{\alpha,\beta}(n)=\alpha X(n)+\beta\log_2 n$ is a *strict pointwise* Lyapunov
function (which would prove the conjecture). Systematic $(\alpha,\beta)$ drift sweep
over all trajectories from $n\in[2,10^5)$ ($\approx7.2\times10^6$ steps).

**Why it failed — two independent obstructions:**
1. **Magnitude-blindness** of pure statistics ($\beta=0$): $s(2^k)=r(2^k)=1$,
   $c(2^k)=0$ for all $k$, so they have no finite level sets and cannot bound the
   trajectory regardless of drift.
2. **Average-only descent** of the hybrids: across $\approx7.2\times10^6$ steps,
   **zero** of the $\approx90$ nontrivial $(X,\alpha,\beta)$ candidates has
   $\max_{\text{steps}}\Delta L\le0$ — every one strictly increases somewhere.
   The digit term cancels the odd-step magnitude jump $\beta(\log_2 3-1)\approx
   0.585\beta$ only in the *mean*, exactly reproducing the Tao/Lagarias–Weiss
   $\tfrac12(\log_2 3-2)\approx-0.208$ heuristic descent and adding no rigour.
   Raising $\beta$ lowers the mean but raises $\max\Delta L$.

**Counter-example (if any):** Pointwise increase witnessed for every candidate;
e.g. pure Hamming $\max\Delta s=+8$, and best-mean hybrid (runs, $\alpha=5,\beta=2$,
mean $-0.94$) still has $\max\Delta L=+61.2$. The odd-step $\log_2$ drift is
$+0.591$ (vs. closed form $\log_2 3-1=0.585$): magnitude genuinely grows every odd step.

**Pointer to artifacts:**
- `theory/digit_lyapunov.md` (full writeup, drift tables, §7 verdict)
- `experiments/lyapunov_search.py` and `experiments/data/lyapunov_sweep.json`
  (re-run 2026-06-03: reproduces committed data bit-for-bit incl. seeded
  random-parity and uniform-bit blocks).

**Verdict:** abandoned as a Lyapunov route. Kept expositionally: it pins down what a
working Lyapunov function must do that these cannot — be simultaneously
magnitude-aware (finite level sets) *and* pointwise (not merely average) decreasing
across the $3n+1$ jump. The $\mathbb{F}_2[T]$ analog (`theory/function_field.md`)
exhibits both via the degree valuation, isolating the archimedean/$2$-adic decoupling
in $\mathbb{Z}$ as the obstruction.

**Lesson:** "Drifts down on average" $\ne$ "is a Lyapunov function." Any digit
statistic that is bounded on the powers of two is automatically disqualified
(magnitude-blind), and hybridizing with $\log_2 n$ only re-imports the known average
descent — never the pointwise strictness a proof needs. `[NOVELTY UNVERIFIED]`:
$s(n)$ not decreasing is noted in Lagarias's survey; the systematic sweep + the
pointwise-supermartingale audit appear new but were not exhaustively checked.
