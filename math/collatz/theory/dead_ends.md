# Dead Ends — Vector A (log → natural density), Collatz theory track

**Purpose.** Append-only record of sub-approaches tried while attacking the
upgrade of Tao 2022 from logarithmic to natural density, that did NOT work.
Companion to `shared/dead_ends.md` (project-wide) and `theory/tao_syracuse_explicit.md`.

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
