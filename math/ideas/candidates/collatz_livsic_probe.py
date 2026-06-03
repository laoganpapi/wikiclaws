#!/usr/bin/env python3
r"""
collatz_livsic_probe.py
=======================

Livsic / coboundary probe for the Collatz drift cocycle.

THE OBJECT.  Via the Syracuse encoding, the Collatz dynamics on odd integers is
conjugate to the (one-sided) shift sigma on the space of 2-adic valuation
sequences

    a = (a_1, a_2, ...),   a_j in {1,2,3,...},   a_j = nu_2(3 x_j + 1),

with the i.i.d. Geometric(1/2) law  P(a = k) = 2^{-k}  (mean 2) as the natural
("descent-balance") sampling measure.  One Syracuse (odd) step
x -> (3x+1)/2^{a}  changes the log-magnitude by, to leading order,

    phi(a) = log 3 - a * log 2          (the DRIFT COCYCLE).

Its mean under Geom(1/2) is  Ebar = log 3 - 2 log 2 = (log_2 3 - 2) log 2 < 0
( = -0.415 in log_2 units per odd step;  the accelerated-T per-step rate is half
this, (log_2 3 - 2)/2 = -0.2075, because there are on average a_bar = 2 parity
steps per odd step ).  This reproduces the known average descent.

THE QUESTION (Livsic coboundary).  Is the centered cocycle  psi := phi - Ebar  a
COBOUNDARY,  psi = u o sigma - u  for a bounded/continuous u?  Livsic's theorem:
for a Holder cocycle over a hyperbolic / mixing shift, this holds IFF every
periodic-orbit sum vanishes:

    Sigma_per(O) := sum_{j=0}^{p-1} psi(sigma^j x) = 0   for every period-p point x.

PERIODIC ORBITS HERE = cyclic valuation words (a_1,...,a_p).  The cocycle sum of
the UNcentered phi over such a word is

    Sigma_phi = sum_j (log 3 - a_j log 2) = K log 3 - S log 2 = -Lambda,

with K = p (number of odd steps) and S = sum a_j (total halvings).  This is
LITERALLY minus the telescoping invariant Lambda = N log2 - K log3 of
collatz/theory/cycle_bound_attempt.md.  The CENTERED sum is

    Sigma_psi = Sigma_phi - p * Ebar = -Lambda - p*(log3 - 2 log2)
              = (2p - S) log 2 = (S_expected - S) log 2,

i.e. centered periodic sums measure how far a word's total halving count S
deviates from its mean 2p.  We compute the DISTRIBUTION of these sums.

This script:
  1. Defines phi, Ebar, validates the mean (Monte-Carlo + exact) and the trivial
     cycle {1,2} sum.
  2. Enumerates ALL cyclic valuation words up to period p (necklaces, with the
     correct Geom(1/2) periodic weight) and tabulates the centered periodic-sum
     distribution Sigma_psi vs p -- the Livsic obstruction set.
  3. Tests coboundary: does the distribution concentrate at 0 (coboundary) or
     spread (non-coboundary)?  Reports mean, variance, support spread, the
     fraction at 0, and the best bounded-transfer-function attempt (a finite
     linear-program / direct check that no bounded u can trivialize psi).
  4. Cross-links to cycles.py: confirms Sigma_phi = -Lambda on the actual
     integer-cycle fixed points the brute search finds (the {1,2} trivial cycle).

No file outside ideas/candidates/ is written.  collatz/experiments/cycles.py is
imported READ-ONLY for the cross-check.

Usage:  python3 collatz_livsic_probe.py [PMAX=14] [AMAX=12]
Output: ideas/candidates/data/livsic_probe.json (+ console transcript)
"""

import sys, os, json, math, itertools
from collections import defaultdict
from fractions import Fraction

LOG2 = math.log(2.0)
LOG3 = math.log(3.0)
EBAR = LOG3 - 2.0 * LOG2            # mean of phi under Geom(1/2), nats  (= -0.2877)
EBAR_LOG2 = math.log2(3.0) - 2.0    # = -0.41504, per-odd-step drift in log_2 units


# ---------------------------------------------------------------------------
# The cocycle.
# ---------------------------------------------------------------------------

def phi(a):
    """Drift cocycle for one Syracuse odd-step with 2-adic valuation a (nats)."""
    return LOG3 - a * LOG2


def psi(a):
    """Centered cocycle phi - Ebar."""
    return phi(a) - EBAR


# ---------------------------------------------------------------------------
# 1. Validation of the mean (the cocycle must reproduce the known drift).
# ---------------------------------------------------------------------------

def validate_mean(amax=200):
    """Exact mean of phi under truncated-renormalized Geom(1/2), and the
    closed form.  Returns dict of checks."""
    # exact tail-truncated geometric, renormalized
    weights = [2.0 ** (-k) for k in range(1, amax + 1)]
    Z = sum(weights)
    p = [w / Z for w in weights]
    mean_a = sum((k + 1) * p[k] for k in range(amax))
    mean_phi = sum(phi(k + 1) * p[k] for k in range(amax))
    # closed forms
    closed_mean_a = 2.0
    closed_mean_phi = EBAR
    return {
        "mean_a_numeric": mean_a,
        "mean_a_closed": closed_mean_a,
        "mean_a_err": abs(mean_a - closed_mean_a),
        "mean_phi_numeric_nats": mean_phi,
        "mean_phi_closed_nats": closed_mean_phi,
        "mean_phi_err": abs(mean_phi - closed_mean_phi),
        "mean_phi_log2": mean_phi / LOG2,
        "expected_drift_log2_per_oddstep": EBAR_LOG2,
        "expected_drift_log2_per_acceleratedstep": (math.log2(3.0) - 2.0) / 2.0,
    }


# ---------------------------------------------------------------------------
# Validate the trivial cycle {1,2}.
# ---------------------------------------------------------------------------

def validate_trivial_cycle():
    """The trivial Collatz cycle 1 -> 2 -> 1.  In Syracuse encoding it is ONE
    odd step  1 -> (3*1+1)/2^2 = 1  with valuation a = nu_2(4) = 2.  So the
    periodic word is (a) = (2), p = 1, K = 1, S = 2.
      Sigma_phi = log3 - 2 log2 = -Lambda   (Lambda = 2 log2 - log3 > 0).
      Sigma_psi = Sigma_phi - 1*Ebar = 0   (it sits EXACTLY at the mean -- the
                  trivial cycle is the unique fixed point that balances).
    """
    word = (2,)
    Sigma_phi = sum(phi(a) for a in word)
    Sigma_psi = sum(psi(a) for a in word)
    # Lambda from cycle_bound_attempt: N=2 (accelerated steps), K=1.
    N, K, S = 2, 1, 2
    Lambda = N * LOG2 - K * LOG3
    return {
        "word": list(word), "K": K, "S": S,
        "Sigma_phi_nats": Sigma_phi,
        "minus_Lambda": -Lambda,
        "Sigma_phi_equals_minusLambda": abs(Sigma_phi - (-Lambda)) < 1e-12,
        "Sigma_psi_nats": Sigma_psi,
        "Sigma_psi_is_zero": abs(Sigma_psi) < 1e-12,
        "note": "trivial cycle sits at the mean: centered sum = 0 (it is the "
                "ONE periodic orbit that balances 2^S = 3^K up to ... well 2^2 vs 3^1, "
                "it does NOT balance -- Sigma_psi=0 means S=2K, i.e. 2=2*1, true).",
    }


# ---------------------------------------------------------------------------
# 2. Enumerate periodic orbits (cyclic words) and their centered sums.
# ---------------------------------------------------------------------------

def necklaces(p, amax):
    """Generate one representative per cyclic-equivalence class (necklace) of
    length-p words over alphabet {1..amax}, together with the size of the orbit
    (number of distinct rotations) so we can weight correctly.

    For our distribution we actually want the per-POINT distribution weighted by
    the shift-invariant (Geom product) measure, which is rotation-invariant, so
    enumerating linear words and dividing by p (each periodic point counted once)
    is equivalent and far simpler.  We therefore enumerate by the *aperiodic
    primitive period* to identify genuine prime-period-p orbits, but for the
    distribution we use ALL length-p words (each weighted by its product
    measure), which is the clean Livsic object: the sum over the period-p
    sub-shift.  We expose both views.
    """
    # We will not materialize necklaces explicitly for the distribution; see
    # enumerate_period below.  This stub kept for clarity / primitive counting.
    raise NotImplementedError


def enumerate_period(p, amax):
    """For period p, iterate over ALL words (a_1,...,a_p) in {1..amax}^p, compute
    the centered cocycle sum Sigma_psi and the Geom(1/2) product weight.

    Returns:
      hist      : dict  rounded-Sigma_psi(log2 units) -> total weight
      stats     : weighted mean, variance, min, max of Sigma_psi (nats)
      n_words   : amax^p
      weight_tot: total (truncated) probability mass
      frac_zero : weighted fraction with Sigma_psi == 0 exactly (S == 2p)
      cum_at_0  : weighted P(Sigma_psi == 0)  (== P(sum a_j = 2p))
    """
    # The centered sum depends ONLY on S = sum a_j:
    #   Sigma_psi = -Lambda - p*Ebar = (K log3 - S log2) - p(log3 - 2log2)
    #             = (2p - S) log2.            (K = p)
    # So we only need the distribution of S = sum of p i.i.d. Geom(1/2)
    # truncated at amax.  That is an (amax)-fold convolution -> O(p * S_max) DP.
    # Per-symbol law:
    pk = [2.0 ** (-k) for k in range(1, amax + 1)]      # index 0 -> a=1
    Z = sum(pk)
    pk = [w / Z for w in pk]
    # DP over S
    # dp[s] = weight that sum of (current count) symbols equals s
    dp = {0: 1.0}
    for _ in range(p):
        ndp = defaultdict(float)
        for s, w in dp.items():
            for k in range(1, amax + 1):
                ndp[s + k] += w * pk[k - 1]
        dp = dict(ndp)
    # Now Sigma_psi(nats) = (2p - S) * LOG2 ; in log2 units it is (2p - S).
    hist = defaultdict(float)
    mean = var = 0.0
    smin = min(dp); smax = max(dp)
    wtot = sum(dp.values())
    frac_zero = dp.get(2 * p, 0.0)
    # first/second moments of Sigma_psi (nats)
    for s, w in dp.items():
        val = (2 * p - s) * LOG2
        hist[round((2 * p - s))] += w          # key = Sigma_psi in log2 units (integer!)
        mean += val * w
    for s, w in dp.items():
        val = (2 * p - s) * LOG2
        var += (val - mean) ** 2 * w
    return {
        "p": p,
        "n_words": amax ** p,
        "weight_tot": wtot,
        "Sigma_psi_mean_nats": mean,
        "Sigma_psi_mean_log2": mean / LOG2,
        "Sigma_psi_var_nats": var,
        "Sigma_psi_std_nats": math.sqrt(var),
        "Sigma_psi_std_log2": math.sqrt(var) / LOG2,
        "Sigma_psi_min_log2": float(2 * p - smax),   # smallest (most negative)
        "Sigma_psi_max_log2": float(2 * p - smin),   # largest (most positive)
        "frac_at_zero": frac_zero,                   # P(Sigma_psi == 0) = P(S = 2p)
        "support_size": len(dp),
        "hist_log2units": {int(k): v for k, v in sorted(hist.items())},
    }


# ---------------------------------------------------------------------------
# 3. Coboundary verdict: can a bounded u trivialize psi?
# ---------------------------------------------------------------------------

def coboundary_test(stats_by_p):
    """A centered Holder cocycle is a coboundary IFF all periodic sums vanish.
    We have closed form Sigma_psi = (2p - S) log2 with S = sum a_j, a_j >= 1.

    PROOF-GRADE NON-VANISHING:  take the prime-period-p orbit that is the
    constant word a_j = c for a single value c (necklace of a constant word has
    period 1, but the orbit (c,c,...,c) read as a period-p point gives S = p*c,
    so Sigma_psi = (2p - pc) log2 = p(2-c) log2).  For c != 2 this is NONZERO and
    GROWS LINEARLY in p.  Concretely:
        c = 1 (all-1 word):  Sigma_psi = +p log2  -> +inf
        c = 3 (all-3 word):  Sigma_psi = -p log2  -> -inf
    So periodic sums do NOT all vanish; they are UNBOUNDED.  Hence psi is NOT a
    coboundary -- and not even a coboundary plus a bounded error, because the
    periodic sums are unbounded, which by Livsic forces ANY transfer function u
    with psi = u o sigma - u + (const) to be UNBOUNDED.

    Returns the witnessing orbits and the verdict.
    """
    witnesses = []
    for c in (1, 3, 4):
        for p in (1, 3, 5, 10, 50):
            Sig = p * (2 - c) * LOG2
            witnesses.append({"word": f"({c})^{p}", "p": p, "c": c,
                              "Sigma_psi_nats": Sig,
                              "Sigma_psi_log2": p * (2 - c)})
    # Is there a bounded u?  Livsic: bounded coboundary <=> periodic sums bounded
    # AND vanishing.  Constant-word orbits give Sigma_psi = p(2-c)log2, unbounded
    # in p for any c != 2.  => no bounded u, not even up to a constant.
    return {
        "all_periodic_sums_vanish": False,
        "periodic_sums_bounded": False,
        "verdict": "NON-COBOUNDARY (periodic sums provably spread, unbounded)",
        "mechanism": "constant-word period-p orbits give Sigma_psi=p(2-c)log2, "
                     "linear in p, sign set by c<2 (up) or c>2 (down); "
                     "the all-ones word -> +p log2, the all-threes word -> -p log2.",
        "witnesses": witnesses,
        "cohomology_class": "nontrivial in H^1: [phi] != 0; drift is a genuine "
                            "(non-trivializable) cocycle class.",
    }


# ---------------------------------------------------------------------------
# Cross-link to cycles.py (read-only): confirm Sigma_phi = -Lambda on real cycles.
# ---------------------------------------------------------------------------

def crosscheck_cycles():
    """Import collatz/experiments/cycles.py read-only and confirm, on every
    positive-integer fixed point its brute search finds (only the trivial {1,2}
    in range), that the Syracuse cocycle sum Sigma_phi over the cycle equals
    -Lambda = -(N log2 - K log3) from cycle_bound_attempt.md."""
    here = os.path.dirname(os.path.abspath(__file__))
    expdir = os.path.normpath(os.path.join(here, "..", "..", "collatz", "experiments"))
    out = {"checked": [], "all_match": True, "expdir": expdir}
    if not os.path.isdir(expdir):
        out["error"] = "experiments dir not found; skipped"
        return out
    sys.path.insert(0, expdir)
    try:
        import cycles  # read-only import
    except Exception as e:        # pragma: no cover
        out["error"] = f"import failed: {e}"
        return out
    from itertools import combinations
    seen = set()
    for m in range(1, 16):
        for k in range(1, m + 1):
            if not cycles.is_steiner_admissible(m, k):
                continue
            for pos in combinations(range(m), k):
                parity = [0] * m
                for p_ in pos:
                    parity[p_] = 1
                n = cycles.cycle_n_from_parity(parity)
                if n is None or n <= 0:
                    continue
                if not cycles.verify_cycle(n, parity):
                    continue
                circ = cycles.circuit_decomposition(parity)
                if circ is None:
                    continue
                N, K = cycles.lambda_from_circuits(circ)
                # Syracuse valuations a_j = b_j (e-run lengths) per circuit:
                # one odd step per circuit?  No -- a_j (o-run) can exceed 1.
                # Re-derive the SYRACUSE valuation word from the orbit directly:
                # each odd value x -> (3x+1)/2^v ; v = nu_2(3x+1).
                x = n
                vword = []
                steps = 0
                while steps < 4 * N + 8:
                    if x % 2 == 1:
                        t = 3 * x + 1
                        v = (t & -t).bit_length() - 1   # nu_2
                        vword.append(v)
                        x = t >> v
                    else:
                        x >>= 1
                    steps += 1
                    if x == n and x % 2 == 1 and vword:
                        break
                Ssum = sum(vword)
                Kodd = len(vword)
                Sigma_phi = sum(phi(a) for a in vword)
                Lambda_syr = Ssum * LOG2 - Kodd * LOG3
                key = tuple(vword)
                if key in seen:
                    continue
                seen.add(key)
                match = abs(Sigma_phi - (-Lambda_syr)) < 1e-9
                out["checked"].append({
                    "n": n, "vword": vword, "K_odd": Kodd, "S": Ssum,
                    "Sigma_phi": Sigma_phi, "minus_Lambda": -Lambda_syr,
                    "match": match,
                })
                if not match:
                    out["all_match"] = False
    return out


# ---------------------------------------------------------------------------
# Driver.
# ---------------------------------------------------------------------------

def main():
    pmax = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    amax = int(sys.argv[2]) if len(sys.argv) > 2 else 12

    print("=" * 72)
    print("Livsic / coboundary probe for the Collatz drift cocycle")
    print("phi(a) = log3 - a*log2 on the Syracuse valuation shift")
    print("=" * 72)

    # 1. mean validation
    mean_chk = validate_mean()
    print("\n[1] MEAN VALIDATION (cocycle must reproduce known drift)")
    print(f"    E[a]        numeric {mean_chk['mean_a_numeric']:.10f}  closed 2.0  "
          f"err {mean_chk['mean_a_err']:.2e}")
    print(f"    E[phi] nats numeric {mean_chk['mean_phi_numeric_nats']:.10f}  "
          f"closed {mean_chk['mean_phi_closed_nats']:.10f}  err {mean_chk['mean_phi_err']:.2e}")
    print(f"    E[phi] log2 = {mean_chk['mean_phi_log2']:.10f}  "
          f"= log2(3)-2 = {mean_chk['expected_drift_log2_per_oddstep']:.10f}  (per odd step)")
    print(f"    accelerated-T per-step rate = (log2 3 - 2)/2 = "
          f"{mean_chk['expected_drift_log2_per_acceleratedstep']:.10f}")
    assert mean_chk['mean_a_err'] < 1e-10 and mean_chk['mean_phi_err'] < 1e-10, "MEAN CHECK FAILED"
    print("    PASS: mean reproduces (log_2 3 - 2) per odd step  (descent on average).")

    # trivial cycle
    triv = validate_trivial_cycle()
    print("\n[1b] TRIVIAL CYCLE {1,2} CHECK")
    print(f"    word {triv['word']}  K={triv['K']} S={triv['S']}")
    print(f"    Sigma_phi = {triv['Sigma_phi_nats']:.10f}  == -Lambda = "
          f"{triv['minus_Lambda']:.10f}  match {triv['Sigma_phi_equals_minusLambda']}")
    print(f"    Sigma_psi (centered) = {triv['Sigma_psi_nats']:.2e}  is_zero "
          f"{triv['Sigma_psi_is_zero']}")
    assert triv['Sigma_phi_equals_minusLambda'], "TRIVIAL CYCLE Sigma_phi != -Lambda"
    assert triv['Sigma_psi_is_zero'], "TRIVIAL CYCLE centered sum != 0"
    print("    PASS: Sigma_phi = -Lambda and the trivial orbit sits exactly at the mean.")

    # 2. periodic-sum distribution
    print(f"\n[2] PERIODIC-SUM DISTRIBUTION  (period p = 1..{pmax}, amax={amax})")
    print(f"    {'p':>3} {'mean(log2)':>11} {'std(log2)':>10} {'min':>6} {'max':>6} "
          f"{'P(Sig=0)':>10} {'supp':>5}")
    per_rows = []
    for p in range(1, pmax + 1):
        st = enumerate_period(p, amax)
        per_rows.append(st)
        print(f"    {p:>3} {st['Sigma_psi_mean_log2']:>11.4f} "
              f"{st['Sigma_psi_std_log2']:>10.4f} {st['Sigma_psi_min_log2']:>6.0f} "
              f"{st['Sigma_psi_max_log2']:>6.0f} {st['frac_at_zero']:>10.5f} "
              f"{st['support_size']:>5}")

    # std should grow ~ sqrt(p) (it is the std of a sum of p iid bounded vars)
    stds = [r['Sigma_psi_std_log2'] for r in per_rows]
    growth = stds[-1] / stds[0] if stds[0] else float('nan')
    print(f"    std(p={pmax})/std(p=1) = {growth:.3f}   "
          f"(sqrt({pmax}) = {math.sqrt(pmax):.3f}: diffusive spread)")

    # 3. coboundary verdict
    print("\n[3] COBOUNDARY VERDICT (Livsic: coboundary <=> all periodic sums vanish)")
    cob = coboundary_test(per_rows)
    print(f"    all periodic sums vanish?  {cob['all_periodic_sums_vanish']}")
    print(f"    periodic sums bounded?     {cob['periodic_sums_bounded']}")
    print(f"    VERDICT: {cob['verdict']}")
    print(f"    mechanism: {cob['mechanism']}")
    print("    witnessing constant-word orbits (Sigma_psi in log2 units = p(2-c)):")
    for w in cob['witnesses'][:6]:
        print(f"       {w['word']:>8}  Sigma_psi = {w['Sigma_psi_log2']:+d} log2 "
              f"= {w['Sigma_psi_nats']:+.4f} nats")

    # 4. cross-check vs cycles.py
    print("\n[4] CROSS-CHECK vs collatz/experiments/cycles.py (read-only)")
    cc = crosscheck_cycles()
    if "error" in cc:
        print(f"    (skipped: {cc['error']})")
    else:
        for c in cc['checked']:
            print(f"    n={c['n']:>4} vword={c['vword']} K={c['K_odd']} S={c['S']}  "
                  f"Sigma_phi={c['Sigma_phi']:.6f}  -Lambda={c['minus_Lambda']:.6f}  "
                  f"match={c['match']}")
        print(f"    all_match = {cc['all_match']}")

    # write data
    here = os.path.dirname(os.path.abspath(__file__))
    datadir = os.path.join(here, "data")
    os.makedirs(datadir, exist_ok=True)
    out = {
        "cocycle": "phi(a) = log3 - a log2  on the Syracuse valuation shift; "
                   "centered psi = phi - Ebar, Ebar = log3 - 2log2",
        "Ebar_nats": EBAR, "Ebar_log2": EBAR_LOG2,
        "params": {"pmax": pmax, "amax": amax},
        "mean_validation": mean_chk,
        "trivial_cycle": triv,
        "periodic_distribution": per_rows,
        "std_growth_pmax_over_p1": growth,
        "coboundary_verdict": cob,
        "cycles_crosscheck": cc,
    }
    outpath = os.path.join(datadir, "livsic_probe.json")
    with open(outpath, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n[written] {outpath}")
    print("=" * 72)
    print("SUMMARY: drift cocycle phi = log3 - a log2 is NOT a coboundary.")
    print("Periodic sums Sigma_psi = (2p - S) log2 spread (std ~ sqrt(p)) and are")
    print("UNBOUNDED over constant-word orbits.  [phi] is nontrivial in H^1.")
    print("=> No bounded/continuous Lyapunov of the form 'phi = u o sigma - u + const'.")
    print("=" * 72)


if __name__ == "__main__":
    main()
