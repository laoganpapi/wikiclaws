"""
MANDATORY cross-check (n=2..6): the FFT W-recursion law must reproduce the exact
direct DP (the prior agent's `verify_syracuse_rv.py` algorithm, re-implemented
independently in reference_bruteforce.py) and the prior agent's PUBLISHED E_n
values, for BOTH the untilted (s=0) and descent-balance-tilted (s=s*) laws.

If this fails, the FFT is wrong and nothing at large n should be trusted.

Run:  python3 crosscheck.py
"""

from __future__ import annotations

import math
import sys

import numpy as np

from syracuse_fft import syracuse_law_fft, collision_excess_from_law
from reference_bruteforce import reference_law_dp


# Prior agent's published E_n (tao_syracuse_explicit.md sec 6.4), n=1..6.
PUBLISHED_UNTILTED = [0.111, 0.429, 0.736, 1.046, 1.356, 1.667]
PUBLISHED_TILTED = [0.212, 0.854, 1.772, 3.090, 4.972, 7.643]

S_STAR = -math.log2(1 - 1 / math.log(3, 2)) - 1.0  # ~0.438033


def run_crosscheck(a_max: int = 55, verbose: bool = True) -> bool:
    ok = True
    rows = []
    for label, s, published in [
        ("UNTILTED s=0", 0.0, PUBLISHED_UNTILTED),
        (f"TILTED s*={S_STAR:.5f}", S_STAR, PUBLISHED_TILTED),
    ]:
        if verbose:
            print(f"\n=== {label} ===")
            print(f"  {'n':>2} {'E_n(FFT)':>12} {'E_n(DP)':>12} {'|FFT-DP|':>10} "
                  f"{'published':>10} {'maxLawErr':>11}")
        for n in range(2, 7):
            law_fft = syracuse_law_fft(n, s=s)
            law_ref = reference_law_dp(n, a_max=a_max, s=s)
            law_err = float(np.max(np.abs(law_fft - law_ref)))
            En_fft = collision_excess_from_law(law_fft, n)
            En_ref = collision_excess_from_law(law_ref, n)
            d = abs(En_fft - En_ref)
            pub = published[n - 1]
            # Agreement criteria:
            #  (a) FFT law == DP law to ~1e-10 (both exact up to truncation)
            #  (b) FFT E_n matches published to its printed 3-decimal precision
            agree_dp = (law_err < 1e-9) and (d < 1e-7)
            agree_pub = abs(En_fft - pub) < 5e-3
            ok = ok and agree_dp and agree_pub
            rows.append((label, n, En_fft, En_ref, d, pub, law_err,
                         agree_dp, agree_pub))
            if verbose:
                flag = "OK" if (agree_dp and agree_pub) else "FAIL"
                print(f"  {n:>2} {En_fft:>12.6f} {En_ref:>12.6f} {d:>10.2e} "
                      f"{pub:>10.3f} {law_err:>11.2e}  {flag}")
    if verbose:
        print(f"\nCROSS-CHECK {'PASS' if ok else 'FAIL'} "
              f"(FFT law == exact DP to <1e-9, and matches prior published E_n).")
    return ok


if __name__ == "__main__":
    success = run_crosscheck()
    sys.exit(0 if success else 1)
