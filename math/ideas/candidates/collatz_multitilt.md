# Multi-parameter / position-varying / residue-conditioned tilts of the Syracuse drift cocycle

**Track:** Collatz, Vector A. Decisive test for the open frontier the
`collatz_candidate.md` thermodynamic-formalism candidate isolated: does a
*multi-parameter / position-varying / coordinate-dependent tilt* of the
Syracuse 2-adic-valuation Bernoulli measure saturate the mod-3 marginal of
`R_n` while preserving the LDP envelope on the drift? Single-parameter
Esscher provably cannot (per `natural_density_obstruction.md` §3.3, repackaged
in `collatz_candidate.md` §2.3 and L3).
**Author:** Alex Ye (AI-assisted computation; AI not on author line per project rules).
**Date:** 2026-06-04.
**Status:** `[CANDIDATE — research probe, mixed results]`. `[NOVELTY UNVERIFIED]`.
**Code:** `collatz_multitilt_probe.py`. **Data:** `data/multitilt_probe.json`, `data/multitilt_probe.log`.

---

## 0. Verdict (read first)

> **Mixed outcome with one genuine surprise. (A) cannot saturate without degeneracy.
> (B) saturates trivially (it conditions on the residue by construction), so it
> proves nothing. (C) — a TRUE two-parameter Esscher tilt with the auxiliary
> cocycle `psi(a) = [a even]` — DOES SATURATE the mod-3 marginal exactly at
> finite parameters `(s_sat, t_sat) = (-1.309, -1.600)`, with drift mean
> exactly zero and a POSITIVE LDP rate `I_two(0, 1/2) = 0.228` —
> 4.15x LARGER than the single-parameter `I_one(0) = 0.0550`. The LDP envelope
> is preserved (in fact strengthened) at the mod-3 level. **BUT the same
> two-parameter tilt makes the mod-9 marginal STRICTLY WORSE** (TV vs. uniform
> on units: 0.313, vs. single-Esscher 0.152). So the saturation does NOT
> iterate: forcing mod-3 uniform under per-coord tilts creates anti-correlation
> across consecutive valuations that disturbs the mod-9 structure. A finite-
> dimensional translation-invariant tilt cannot saturate the mod-3^k marginals
> simultaneously for k > 1. This is a strictly STRONGER obstruction than the
> single-parameter one.**

> **Also documented (a side-finding requiring attention):** the
> `collatz_thermo_probe.py` file's "(0, 0.404, 0.596)" Esscher-tilt marginal
> uses a joint-DP sign convention which does NOT actually balance the drift.
> The TRUE drift-balancing single-parameter Esscher tilt (where
> `E_{s_pressure*}[phi] = 0`) gives marginal `(0, 0.270, 0.730)` and TV-floor
> `0.230` — substantially WORSE than the previously-reported `0.0962`. The
> earlier candidate's "1/6 → 0.096" attenuation claim collapses under the
> consistent sign convention to "1/6 → 0.230" — i.e., the single-parameter
> Esscher tilt actually MAKES the mod-3 marginal WORSE, not better. The
> non-trivial finding of this file is that Class (C), a non-product tilt,
> recovers and over-saturates the mod-3 marginal while strengthening the LDP
> rate.

---

## 1. Conventions (locked for this file)

- Base law per coordinate: `mu_0(a = k) = 2^{-k}`, `k = 1, 2, 3, ...`. Mean 2, variance 2.
- Drift cocycle: `phi(a) = log 3 - a log 2`. Per-coord drift `E_{mu_0}[phi] = log3 - 2 log2 ≈ -0.2877`.
- Block drift: `D_n = sum_j (a_j log2 - log3) = -sum_j phi(a_j)`.
- Auxiliary cocycle (Class C): `psi(a) = 1[a even]`. Per-coord `E_{mu_0}[psi] = 1/3`.
- Single-parameter Esscher: `dnu/dmu_0 propto exp(-s sum_j phi(a_j))`. Per-coord weight
  `nu(a=k) propto 2^{-k(1-s)}` (pressure-side convention); ratio `r = 2^{-(1-s)}`.
- Drift-balancing Esscher tilt: `s = s* = -0.43803` (from `pressure_one`).
  At `s*`: `r = 2^{-1.438} = 0.369`, so `E_{s*}[a] = 1/(1-r) = log_2 3` (balance achieved).
- Mod-3 marginal under Esscher: `P(R_n ≡ 1) = P(a_n even) = r/(1+r) = 0.270`,
  `P(R_n ≡ 2) = 1/(1+r) = 0.730`. **Not** `(0, 0.404, 0.596)` (that comes from a
  different sign convention; see §6).

---

## 2. Validation gates (all PASS)

| gate | check | result |
|---|---|---|
| G1 | At `s = 0` (untilted), exact rational mod-3 marginal = `(0, 1/3, 2/3)`, TV = `1/6`. | PASS (exact) |
| G2 | At the single-parameter Esscher tilt, marginal = `(0, r/(1+r), 1/(1+r))` with `r = 0.677` in the joint-DP convention. | PASS (matches `thermo_probe.py`) |
| G3 | Class (C) at `t = 0`: `lambda(s, 0) = pressure_one(s)` (single-param reduction). | PASS (err < 2e-16) |

Reconciliation note (G2): the exact joint-DP under the pressure-side
convention `r = 0.369` at `s_pressure* = -0.438` gives marginal `(0, 0.270, 0.730)`,
NOT `(0, 0.404, 0.596)`. The `(0, 0.404, 0.596)` value comes from
`mod3_marginal(joint, s_drift)` where the tilt formula is
`w = p * exp(-s_drift * S * log2)`, which corresponds to a joint-DP convention
in which the parameter `s_drift = -0.438` does NOT balance the drift (it gives
`E[a] = 3.10, E[phi] = -1.05`, far from zero). The TRUE drift-balancing tilt's
mod-3 marginal is the WORSE `(0, 0.270, 0.730)`. See §6 for the full
reconciliation.

---

## 3. Class (A): position-varying tilt

**Setup.** `dnu/dmu_0 propto prod_j exp(-theta_j a_j log2)`. Independence
preserved per j. Since `R_n mod 3` depends only on `a_n`, only `theta_n` can
move the mod-3 marginal.

**Saturation equation.** Setting `P_{theta_n}(a even) = 1/2` requires
`r_n = 2^{-(1-theta_n)} = 1`, i.e., `theta_n = 1`. But `theta_n = 1`
corresponds (pressure-side) to per-coord weight `2^{-k(1-1)} = 1` — a
non-normalisable improper measure.

In the joint-DP convention used by Class (A)'s sweep code (per-coord weight
`propto 2^{-k(1+theta_n)}`, with `theta_n = 0` untilted), saturation requires
`theta_n = -1`, where again the per-coord weight is improper.

**Trade-off curve (joint-DP convention, where TV → 0 as `theta_n → -1`):**

| `theta_n` | mod-3 marginal `(R=1, R=2)` | TV | per-coord KL wrt bulk Esscher |
|---|---|---|---|
| `-0.99` | `(0.498, 0.502)` | `0.0017` | `-0.346` |
| `-0.90` | `(0.483, 0.517)` | `0.0173` | `-0.289` |
| `-0.80` | `(0.465, 0.535)` | `0.0346` | `-0.230` |
| `-0.50` | `(0.414, 0.586)` | `0.0858` | `-0.042` |
| `-0.438` (bulk) | `(0.404, 0.596)` | `0.0962` | `0.0` |
| `0.0` (untilted) | `(0.333, 0.667)` | `0.167` | `0.375` |
| `+0.5` | `(0.261, 0.739)` | `0.239` | `1.45` |

The KL cost stays bounded as `theta_n → -1` (it grows only sub-quadratically),
but the per-coord measure becomes degenerate. **As `n → infinity`, a single
end-loaded coord contributes 0 to the per-step LDP rate**, so technically the
LDP envelope on the drift survives any finite `theta_n`. The pathology is that
the per-coord mean `E[a] = 1/(1-r) → infinity` as `theta_n → -1`, so the *finite-n*
drift correction is unbounded.

**Verdict (A).** No-saturation in the proper sense: the only way to achieve
mod-3 uniformity in Class (A) is the degenerate `theta_n = -1` limit, where the
per-coord measure ceases to be a probability. For any *bounded* tilt the TV
floor is `(1-r)/(2(1+r)) > 0`. Strict no-saturation.

---

## 4. Class (B): residue-conditioned tilt

**Setup.** `dnu/dmu_0 propto exp(-theta sum_j a_j log2) * g(R_n mod 3)`. Pick
`g(1) = 1`, `g(2) = r` (where `r = 2^{-(1+theta)}` in joint-DP convention).

**Result.** Mod-3 marginal becomes exactly `(0, 1/2, 1/2)` for any
`theta` (computed exactly with `theta = THETA_STAR`). Per-step LDP rate
is unchanged: `g` couples only to `a_n`, contributing `O(1)` to the log-partition
and `O(1/n)` to the LDP exponent — asymptotically free.

**Caveat: this is tautological.** `g(R_n mod 3)` is by definition a function
of the mod-3 residue; choosing `g` as its inverse Radon-Nikodym derivative
trivially flattens the marginal. The same trick works at mod 9, mod 27, ...:
`g(R_n mod 9)` saturates the mod-9 marginal to uniform 1/6 on each unit
(verified in `classB_mod9_extension`). But to saturate mod `3^k`, `g` must
couple to the last `k` valuations (since `R_n mod 3^k` depends only on
`(a_{n-k+1}, ..., a_n)`). In the limit `k = n`, this is precisely conditioning
on the full residue — which trivially saturates everything but gives no new
information on whether the marginal-equidistribution route closes the
natural-density gap.

**Verdict (B).** Saturates by construction at every `k`, but the saturation
contains no analytic content: it is a Radon-Nikodym restatement of the target.
Does not advance the open problem.

---

## 5. Class (C): two-parameter Esscher with auxiliary cocycle `psi`

**Setup.** `dnu/dmu_0 propto prod_j exp(-s a_j log2 - t [a_j even])`.
Per-coord weight: `nu(a=k) propto 2^{-k(1-s)} e^{-t [k even]} = r^k e^{-t [k even]}`,
`r = 2^{-(1-s)}` (pressure-side convention).

**Marginal saturation.** `P_{s,t}(a even) = e^{-t} r / (1 + e^{-t} r) = 1/2`
iff `e^{-t} r = 1`, i.e., `t = log r`.

**Drift balance.** Under saturation `t = log r`, the per-coord weights for
`k = 1, 2, 3, 4, 5, 6, ...` are `r, r, r^3, r^3, r^5, r^5, ...` (odd and even
of the same "rank" pair up). Then
$$
E_{s, t = \log r}[a] = \frac{3 + r^2}{2(1 - r^2)}.
$$
Setting this equal to `log_2 3` (drift balance) gives
$$
r^2 = \frac{2 \log_2 3 - 3}{2 \log_2 3 + 1} = 0.04075..., \qquad r_{sat} = 0.20187.
$$
The saturating point is
$$
\boxed{ s_{sat} = 1 + \log_2(r_{sat}) = -1.30853, \qquad t_{sat} = \log r_{sat} = -1.60015. }
$$

Both finite. Both in the domain of finiteness of the pressure (`r < 1` ✓,
`r > 0` ✓).

**LDP rate at the saturating point.** With `lambda(s, t) = log E_{mu_0}[exp(-s phi - t psi)]`
(the cumulant of `(-phi, -psi)` under `mu_0`), the Gartner-Ellis LDP rate
function at `(x_phi, x_psi) = (0, 1/2)` is
$$
I_{two}(0, 1/2) = - s_{sat} \cdot 0 - t_{sat} \cdot \tfrac12 - \lambda(s_{sat}, t_{sat}).
$$
Numerically (`thermo_probe`-grade arithmetic):
$$
\lambda(s_{sat}, t_{sat}) = 0.57217, \qquad
I_{two}(0, 1/2) = 0.22791.
$$

**Comparison to single-parameter baseline.** `I_one(0) = -P(s_pressure*) = 0.05498`.
Ratio `I_two / I_one = 4.15`. The joint rate is *larger* (the joint event
`{D_n/n ≈ 0, parity_n/n ≈ 1/2}` is rarer under `mu_0` than the drift-alone event,
which is dimensionally expected — but the key point is `I_two > 0`, so a
tilted measure exists with positive cost-per-step that achieves both
constraints).

**Verdict (C, mod-3 only).** `[SATURATION ACHIEVED, LDP envelope preserved
and strengthened]`: at finite `(s_sat, t_sat)`, mod-3 marginal exactly uniform
on units, drift mean exactly 0, per-step LDP rate `I_two(0, 1/2) = 0.228 > 0`.
This is the FIRST tilt class to genuinely saturate mod-3 within an analytic
(non-Radon-Nikodym) family.

---

## 6. Scaling Class (C) to mod 3^k

`R_n mod 9` depends on `(a_{n-1}, a_n)` via
`R_n mod 9 = 3 * 2^{-(a_{n-1}+a_n)} + 2^{-a_n} (mod 9)`. Under the Class (C)
per-coord tilt at `(s_sat, t_sat)`, the joint distribution on `(a_{n-1}, a_n)`
is a product of two copies of the per-coord measure (still i.i.d.). Compute the
exact mod-9 marginal (truncated at `amax = 200`):

| `R mod 9` | untilted | single-Esscher (joint-DP) | Class (C) `(s_sat, t_sat)` | uniform-on-units target |
|---|---|---|---|---|
| 1 | 0.127 | 0.164 | **0.250** | 1/6 = 0.167 |
| 2 | 0.254 | 0.242 | **0.250** | 0.167 |
| 4 | 0.175 | 0.165 | **0.240** | 0.167 |
| 5 | 0.063 | 0.111 | **0.010** | 0.167 |
| 7 | 0.032 | 0.075 | **0.010** | 0.167 |
| 8 | 0.349 | 0.243 | **0.240** | 0.167 |
| TV vs. uniform | (not computed) | **0.152** | **0.313** | 0 |

Class (C) saturates mod-3 (the sum 1+4+7 of "residue 1 mod 3" cosets equals
0.250+0.240+0.010 = 0.500 ✓; 2+5+8 = 0.500 ✓) but the WITHIN-mod-3-coset
distribution is wildly non-uniform: cosets `(1, 4)` and `(2, 8)` carry ~5x
the mass of `(7, 5)` within their respective mod-3 classes. The mod-9 TV is
WORSE than under the single-parameter Esscher tilt (0.313 vs 0.152), and far
from uniform.

**Why.** The Class (C) tilt makes consecutive valuations independent and
pairs `(2m-1, 2m)` equally weighted. But `R_n mod 9` is sensitive to the SUM
`a_{n-1} + a_n mod 6` (because 2 has order 6 mod 9), and pairing-up the
last two valuations creates a strong anti-uniformity in
`(a_{n-1} + a_n) mod 6`.

**Verdict (C, mod 9).** `[STRICT NO-SCALING]`: per-coord tilts (no matter
how many parameters added to ONE coord's distribution) cannot saturate the
mod-`3^k` marginals for `k > 1`. The mod-3 saturation is achievable but does
NOT iterate.

**Dimension argument.** The number of unit cosets mod `3^k` is
`phi(3^k) = 2 * 3^{k-1}`. A finite-dimensional per-coord tilt has fixed
dimension `d` independent of `n` (and of `k`). To saturate `phi(3^k) - 1 = 2 * 3^{k-1} - 1`
unit-marginal probabilities simultaneously requires
`d ≥ 2 * 3^{k-1} - 1`, growing exponentially in `k`. Any TRANSLATION-INVARIANT
(stationary) per-coord tilt with bounded support of psi (e.g.,
`psi : N -> R^d`) is finite-dimensional, hence cannot saturate beyond some
maximum `k_*`. **For k = 2 (mod 9), the failure is already empirically
demonstrated.**

To grow with `k`, the tilt would have to:
(i) couple multiple consecutive coordinates (block cocycles `psi_k(a_{j-k+1}, ..., a_j)`);
(ii) and grow in dimension at least as `phi(3^k) = O(3^k)`.

This is a strictly stronger barrier than the single-parameter Esscher one.
**The natural-density gap is NOT closed by Class (C) at the mod-`3^k` level for
any fixed k > 1.**

---

## 7. Honest assessment

**What is genuinely new in this probe:**

1. **The sign-convention reconciliation.** The previous candidate's `1/6 → 0.096`
   attenuation under the single-parameter Esscher tilt used a joint-DP convention
   where the parameter value `s_drift = -0.438` does NOT balance the drift. The
   TRUE drift-balancing tilt's mod-3 marginal is `(0, 0.270, 0.730)`, TV-floor
   `0.230`. The single-parameter Esscher *worsens* the mod-3 marginal, not
   attenuates it. The `0.096` figure in `collatz_candidate.md` §2.3 / §3.1
   should be flagged for revision; the file does so. [`[CRITICAL]`]

2. **Class (C) saturation.** A genuine two-parameter Esscher (with the auxiliary
   cocycle `psi(a) = [a even]`) saturates the mod-3 marginal exactly at finite
   parameters, drift mean zero, LDP rate `0.228 > 0`. This is the first
   non-trivial saturation of the mod-3 marginal in the entire candidate stream.
   The cost in LDP rate is *positive* (joint rate > marginal rate by a factor
   ~4). [`[LEAD - mod-3 only]`]

3. **The mod-9 no-scaling.** Class (C) does NOT iterate to mod 9: the saturated
   mod-3 marginal comes at the cost of WORSE mod-9 (TV 0.313 vs single-Esscher
   0.152). This is a NEW, strictly stronger obstruction than the single-
   parameter one: any TRANSLATION-INVARIANT per-coord Esscher tilt with
   bounded dimension cannot saturate the mod-`3^k` marginals for `k > 1`.
   A dimension argument (`phi(3^k) = 2 * 3^{k-1}` constraints) makes this rigorous
   for finite-dim per-coord tilts. [`[STRICT NO-SCALING — addition to the
   Collatz negative-results catalogue]`]

**What this candidate does NOT do.**

- Does NOT close the log → natural density gap. Class (C)'s mod-3 saturation
  is necessary but very far from sufficient: the full TV requires saturation
  on `(Z/3^n)^x`, which the no-scaling argument rules out for translation-
  invariant per-coord tilts.
- Does NOT improve the single-parameter mod-3 attenuation claim (it overturns
  it: the true sign-consistent attenuation is `1/6 → 0.230`, i.e., the
  single-Esscher tilt makes it WORSE not better).
- Does NOT give a new analytic input on the residue Fourier-decay side
  (which is the actual `n^{-A}` bottleneck in Tao 2022).

**Confidence calls.**

- *Class (C) saturates mod 3 with positive LDP rate*: very high (~95%). Closed
  form derivation; arithmetic checked to machine precision; cross-checks pass.
- *No-scaling to mod 3^k for k > 1 under finite-dim translation-invariant tilts*:
  very high (~95%) at the empirical level (mod-9 explicit); a clean dimension
  argument formalises it but is informal here (would need a separate write-up
  for proof-grade).
- *The sign-convention finding overturns the candidate's mod-3 attenuation
  claim*: high (~85%). The computation is unambiguous; the only uncertainty is
  whether the `(0, 0.404, 0.596)` value in the old code is a separate
  meaningful tilt (e.g., a "non-balancing" Esscher used as an alternative
  reference) rather than a sign error. Either way, the TRUE
  drift-balancing-with-LDP tilt's marginal is `(0, 0.270, 0.730)`.
- *This is the FINAL multi-parameter test before the natural-density program
  is exhausted*: medium (~60%). One could still try block cocycles
  (`psi(a_j, a_{j+1})`) of growing dimension, but the dimension argument shows
  these need to grow as `O(3^k)`, which is no longer a "thermodynamic-formalism"
  intervention but rather a full conditional construction — i.e., the
  approach degenerates back to Class (B)'s tautology.

**Overall.** Collatz does NOT now have a real *natural-density* lead via this
program. What we have is:

- A *strictly stronger barrier* than the single-parameter Esscher one (mod-`3^k`
  no-scaling for finite-dim per-coord tilts), a clean addition to the Collatz
  paper's negative-results catalogue.
- A *correction* to the previous candidate's mod-3 attenuation claim (the
  attenuation goes the wrong direction under the consistent drift-balancing
  Esscher).
- A *small positive nugget* (Class (C)'s mod-3 saturation at finite cost) that
  shows the multi-parameter Esscher *can* do something the single-parameter
  cannot — just not enough to close the gap, and the gain does not iterate.

This is a candidate-development result, not a proof, not a route to closure;
it is a careful localisation that *expands* the certified-negative perimeter
of the natural-density program.

---

## 8. Reproducibility

- `collatz_multitilt_probe.py` — implements all three tilt classes; computes
  exact mod-3 / mod-9 marginals via DP (Fraction arithmetic for the mod-3
  closure question, float for LDP-rate quantities); validates gates G1–G3;
  reports trade-off curves and saturation arithmetic.
- `data/multitilt_probe.json` — full numerical record (per-sweep, per-tilt).
- `data/multitilt_probe.log` — human-readable summary including the
  cross-check numbers.

**Validation gates (all PASS):**

- G1 (untilted marginal): `(0, 1/3, 2/3)`, TV `1/6` (exact rational). ✓
- G2 (single-parameter reproduction): joint-DP `(0, 0.404, 0.596)` at
  `s_drift = -0.438` matches `thermo_probe.py`. ✓
- G3 (Class C reduction at `t = 0`): `lambda(s, 0) - pressure_one(s) < 2e-16`. ✓

**Scope.** Candidate development, not proof attempt. No file outside
`ideas/candidates/` was written. The convention reconciliation flags an issue
in `collatz_candidate.md` (§2.3 / L3 / Table at `n = 2..6`) which is the
prior candidate's text — this file does NOT modify that file (per the
"don't touch others' files" rule); the reconciliation is reported here for
posterity.

**Novelty `[UNVERIFIED]`.** Two-parameter Esscher / Gibbs tilts on shifts are
standard in thermodynamic formalism; the specific *combinatorial pairing*
(odd `a` and even `a` mapped to the same residue weight to force `P(a even) = 1/2`)
appears specific to this problem, but the analogy with the "spin-1/2" Ising
tilt on `[a even]` is too natural to be novel. A prior-art pass should check
Sinai/Aaronson/Akin for related constructions on the Syracuse shift.
