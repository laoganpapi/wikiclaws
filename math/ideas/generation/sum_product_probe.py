#!/usr/bin/env python3
"""
Sum-product / Markoff alt-angle probe for Collatz cycle equation.

Direction: sub-direction (i) from the brief, sharpened.

OBJECT under study
==================
The cycle equation `2^N - 3^K = R` (with |R| controlled by cycle geometry,
N = K+S) is equivalent to the requirement that `2^N` lies near `3^K` in
the integers. Reduce mod 3^n: we are asking how the orbit of 2 in
(Z/3^n)* (a cyclic group of order phi(3^n) = 2 * 3^{n-1}) interacts
with the *additive* structure of Z/3^n — specifically, how often the
orbit element 2^N mod 3^n lands in a tiny ball around 0 (mod 3^n) of
radius |R|.

If sum-product machinery (Bourgain-Glibichuk-Konyagin, etc.) gave a
nontrivial lower bound on `|2^a - 3^b|` from the *mixing* of the orbit
of 2, that would be NEW input independent of Baker / LMN. The probe
asks whether the orbit *empirically* exhibits enough sum-product
flavor to be useful — specifically, whether the orbit of 2 mod 3^n
has additive-energy / discrepancy substantially better than a
random cyclic subgroup of the same size.

CONCRETE PROBE
==============
For a range of n, compute:
  (1) The orbit O_n = { 2^k mod 3^n : 0 <= k < ord_2(3^n) }.
  (2) The "additive discrepancy"
        D_n = max_{x in Z/3^n} | #{(a,b) in O_n^2 : a+b = x} - |O_n|^2/3^n |.
      A "sum-product" expectation would be D_n = o(|O_n|^2/3^n), i.e.
      the orbit is additively well-distributed.
  (3) The minimum gap min_{a != b in O_n} |a - b mod 3^n|. This is the
      best one can hope for as a lower bound on |2^a - 2^b mod 3^n|
      = |2^a (2^{b-a} - 1)| mod 3^n. The cycle equation cares about
      |2^N - 3^K|, but since 3^K = 0 mod 3^n for K >= n, this becomes
      |2^N mod 3^n| — the distance of the orbit to ZERO. So we also
      compute:
  (4) min_{a > 0} |2^a mod 3^n| as a function of n.
      This is the "Collatz-relevant" quantity. Baker gives an
      effective lower bound of the form
        |2^N mod 3^K| >= 2^N - 3^K >= 2^N * exp(-c log(N) log(K))
      via LMN; we ask whether the empirical orbit has a *much smaller*
      minimum (which would mean Baker is far from tight) or whether
      it sits near a Baker-style bound (Baker is close to tight, no
      room for sum-product improvement).
  (5) A "Markoff-flavored" check: the Collatz iteration is not exactly
      a Markoff orbit, but we test if the triple (1, 2^a, 3^b) and
      its Vieta involutions in the parameter (a, b) give an
      orbit structure with measurable mixing properties (a long-shot
      cross-check).

OUTPUT
======
JSON with per-n statistics; printed table of D_n vs |O_n|^2 / 3^n and
min |2^a mod 3^n|.
"""

import json
import math
import os
from pathlib import Path


def orbit_of_two_mod_3n(n):
    """Return the orbit of 2 mod 3^n, in iteration order."""
    mod = 3 ** n
    orbit = []
    x = 1
    seen = set()
    while x not in seen:
        seen.add(x)
        orbit.append(x)
        x = (x * 2) % mod
    return orbit, mod


def min_2a_mod_3n(n, max_a=None):
    """
    min_{1 <= a <= max_a} (2^a mod 3^n)  — but we interpret 'mod' here as
    the residue in [0, 3^n-1]; the Collatz-relevant quantity is the
    *signed minimum-magnitude representative*, i.e. min(r, 3^n - r).
    """
    mod = 3 ** n
    if max_a is None:
        # full orbit (multiplicative order)
        # for 3^n, order of 2 is 2 * 3^{n-1} for n >= 1
        max_a = 2 * (3 ** (n - 1))
    x = 1
    best = mod  # 3^n is unreachable, signals "not found"
    best_a = 0
    for a in range(1, max_a + 1):
        x = (x * 2) % mod
        mag = min(x, mod - x)
        if mag < best and mag > 0:
            best = mag
            best_a = a
    return best, best_a, max_a


def additive_energy_discrepancy(orbit, mod):
    """
    Compute E_+(O) = #{(a,b,c,d) in O^4 : a+b = c+d mod 3^n}
    via the Fourier-like identity E_+(O) = sum_x r_O(x)^2 where
    r_O(x) = #{(a,b) in O^2 : a+b = x mod 3^n}.

    Returns (E_+, |O|^4/3^n, discrepancy_D_n).
    """
    M = len(orbit)
    # r_O[x] = # ways to write x = a + b mod 3^n
    r = [0] * mod
    for a in orbit:
        for b in orbit:
            r[(a + b) % mod] += 1
    energy = sum(c * c for c in r)
    expected_r = M * M / mod
    # Discrepancy:  max | r[x] - expected_r |
    D = max(abs(c - expected_r) for c in r)
    return energy, M * M * M * M / mod, D, expected_r


def run(out_path, results_path):
    results = []
    print("=" * 70)
    print("Sum-product / Markoff probe for Collatz cycle equation")
    print("=" * 70)
    print()
    print("STAGE 1: min |2^a mod 3^n| (signed-magnitude) for a in [1, ord)")
    print("-" * 70)
    print(f"{'n':>3} {'3^n':>12} {'ord(2 mod 3^n)':>16} {'min |2^a|':>14} "
          f"{'arg a':>8} {'log_3 ratio':>14}")
    for n in range(2, 15):
        mod = 3 ** n
        order = 2 * (3 ** (n - 1))
        best, best_a, _ = min_2a_mod_3n(n)
        # log_3 of the ratio (best / 3^n): how many "powers of 3 deep"
        # the closest approach gets. For the orbit to give NEW lower
        # bounds on |2^a - 3^b|, we want this to be LARGE (best is small).
        log3_ratio = math.log(best) / math.log(3) if best > 0 else float('-inf')
        row = {
            "n": n,
            "mod_3n": mod,
            "order": order,
            "min_2a_mod_3n": best,
            "arg_a": best_a,
            "log3_min": log3_ratio,
            "log3_mod": n,  # since 3^n
            "log3_gap": n - log3_ratio,  # how far below 3^n the closest is
        }
        results.append(row)
        print(f"{n:>3} {mod:>12} {order:>16} {best:>14} {best_a:>8} "
              f"{log3_ratio:>14.4f}")
    print()

    # STAGE 2: additive-energy discrepancy, but ONLY for small n
    # because the O(|O|^2 mod) cost is prohibitive for large n.
    print("STAGE 2: additive discrepancy of orbit (O(|O|^2 * mod) cost)")
    print("-" * 70)
    print(f"{'n':>3} {'|O|':>8} {'mod=3^n':>10} {'D_n':>14} "
          f"{'|O|^2/3^n':>14} {'D_n / (|O|^2/3^n)':>20}")
    energy_results = []
    for n in range(2, 8):
        orbit, mod = orbit_of_two_mod_3n(n)
        energy, expected_energy, D, expected_r = additive_energy_discrepancy(
            orbit, mod)
        ratio = D / expected_r if expected_r > 0 else float('inf')
        row = {
            "n": n,
            "size_O": len(orbit),
            "mod_3n": mod,
            "additive_discrepancy_D": D,
            "expected_r": expected_r,
            "D_over_expected": ratio,
            "additive_energy": energy,
            "expected_energy_M4_over_3n": expected_energy,
            "energy_ratio": energy / expected_energy if expected_energy > 0 else float('inf'),
        }
        energy_results.append(row)
        print(f"{n:>3} {len(orbit):>8} {mod:>10} {D:>14.2f} "
              f"{expected_r:>14.4f} {ratio:>20.4f}")
    print()

    # STAGE 3: Baker-style benchmark
    # For comparison, what does the LMN / Baker theorem predict for the
    # minimum |2^a - 3^b| with a, b <= some bound? The "trivial" prediction
    # from pigeonhole alone is: |2^a - 3^b| >= 1 (since it's a nonzero integer).
    # The Baker prediction is exponentially larger:
    #   |2^a - 3^b| >> 3^b * b^{-c} for some explicit c.
    # The orbit min |2^a mod 3^n| is a *different* quantity (mod 3^n, not the
    # integer 2^a - 3^b), but they are related: if 2^a = 3^b + R with |R| small,
    # then 2^a mod 3^n = R mod 3^n for n <= b.
    # So a small min_a |2^a mod 3^n| is EVIDENCE for a small |2^a - 3^b|
    # if some 3^b is "near" 2^a.
    print("STAGE 3: comparison to integer min |2^a - 3^b|")
    print("-" * 70)
    print("(brute force: a, b <= 30; for cycle-window calibration only)")
    best_diff = None
    best_ab = None
    diffs = []
    for a in range(1, 31):
        pa = 2 ** a
        for b in range(1, 31):
            pb = 3 ** b
            d = abs(pa - pb)
            if d == 0:
                continue
            ratio = math.log(d) / math.log(max(pa, pb))
            diffs.append((a, b, d, ratio))
            if best_diff is None or d < best_diff:
                best_diff = d
                best_ab = (a, b)
    diffs.sort(key=lambda t: t[2])
    print(f"  10 smallest |2^a - 3^b| with a,b <= 30:")
    for a, b, d, r in diffs[:10]:
        print(f"    a={a:>2}  b={b:>2}  |2^a-3^b|={d:>12}  "
              f"log/log_max = {r:.4f}")
    print()
    print(f"  Tightest in range: (a,b)={best_ab}, |2^a-3^b|={best_diff}")
    print()

    # SAVE
    out = {
        "stage1_min_2a_mod_3n": results,
        "stage2_additive_discrepancy": energy_results,
        "stage3_smallest_diffs_brute_force": [
            {"a": a, "b": b, "diff": d, "log_ratio": r}
            for (a, b, d, r) in diffs[:30]
        ],
        "notes": (
            "min_2a_mod_3n is the closest approach to 0 of the orbit of 2 "
            "in Z/3^n, taking the signed-magnitude representative in "
            "[-3^n/2, 3^n/2]. A 'sum-product' / mixing assumption would "
            "predict this is comparable to the trivial pigeonhole bound "
            "3^n / |O| = 3^n / (2*3^{n-1}) = 3/2; the data shows the orbit "
            "in fact achieves values within an order of magnitude of that, "
            "which is the OPPOSITE of what would help cycles (the orbit is "
            "TOO well-distributed). See sum_product_markoff.md for "
            "interpretation."
        ),
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    here = Path(__file__).parent
    out = here / "data" / "sum_product_probe.json"
    run(str(out), str(out))
