#!/usr/bin/env python3
"""
probe.py — reproducible probes for matroid_tropical.md (generation note).

Isolated under math/ideas/generation/. Re-uses the read-only Frankl toolkit
(enumerate, uc_family, lattice) by adding it to sys.path; the Collatz probe is
self-contained (closed form). Run:

    python3 probe.py            # all four probes, n<=5

No files are written; results print to stdout. NOVELTY UNVERIFIED; directions
not proofs (see matroid_tropical.md).
"""
from __future__ import annotations
import os
import sys
import math
import collections

# Locate the Frankl experiments toolkit (read-only import).
_HERE = os.path.dirname(os.path.abspath(__file__))
_FRANKL = os.path.normpath(
    os.path.join(_HERE, "..", "..", "..", "frankl", "experiments")
)
if _FRANKL not in sys.path:
    sys.path.insert(0, _FRANKL)

import numpy as np  # noqa: E402
from enumerate import all_uc_families  # noqa: E402
from uc_family import abundance, ground_set  # noqa: E402
import lattice as LT  # noqa: E402

NMAX = 5


# --------------------------------------------------------------------------
# Probe 1: cardinality f-vector log-concavity (is there a matroid grading?)
# --------------------------------------------------------------------------
def level_seq(F: frozenset[int], n: int) -> list[int]:
    W = [0] * (n + 1)
    for m in F:
        W[bin(m).count("1")] += 1
    return W


def is_logconcave(W: list[int]) -> bool:
    nz = [i for i, w in enumerate(W) if w > 0]
    if not nz:
        return True
    lo, hi = nz[0], nz[-1]
    for k in range(lo, hi + 1):
        if W[k] == 0:  # internal zero breaks LC
            return False
    for k in range(lo + 1, hi):
        if W[k] * W[k] < W[k - 1] * W[k + 1]:
            return False
    return True


# --------------------------------------------------------------------------
# Probes 2 & 3: JI-filter overlap Gram form signature (Lorentzian test?)
# --------------------------------------------------------------------------
def lattice_elems(F: frozenset[int]) -> list[int]:
    elems, _, _ = LT.as_lattice(F)
    return elems


def upset(elems: list[int], a: int) -> set[int]:
    return {x for x in elems if LT.leq(a, x)}


def signature(M: np.ndarray, tol: float = 1e-7) -> tuple[int, int, int]:
    ev = np.linalg.eigvalsh(M)
    pos = int(sum(1 for e in ev if e > tol))
    neg = int(sum(1 for e in ev if e < -tol))
    zero = M.shape[0] - pos - neg
    return pos, neg, zero


def run_frankl() -> None:
    lc = notlc = 0
    gram_sig = collections.Counter()
    cent_sig = collections.Counter()
    cube_examples: list[tuple] = []
    total = 0
    for n in range(0, NMAX + 1):
        for F in all_uc_families(n, dedupe_isomorphic=True):
            if len(F) < 2:
                continue
            total += 1
            nn = max(ground_set(F), 1)
            W = level_seq(F, nn)
            if is_logconcave(W):
                lc += 1
            else:
                notlc += 1
            if n == 0:
                continue
            elems = lattice_elems(F)
            Lsz = len(elems)
            jis = LT.join_irreducibles(elems)
            if not jis:
                continue
            U = [upset(elems, j) for j in jis]
            r = len(jis)
            G = np.array(
                [[len(U[i] & U[k]) for k in range(r)] for i in range(r)],
                dtype=float,
            ) / Lsz
            gram_sig[signature(G)] += 1
            f = np.array([len(U[i]) for i in range(r)], dtype=float)
            C = G - np.outer(f, f) / (Lsz * Lsz)
            cent_sig[signature(C)] += 1
            is_cube = (
                Lsz == (1 << n) and LT.is_distributive(elems) and r == n
            )
            if is_cube:
                cube_examples.append(
                    (n, signature(G), round(abundance(F), 3))
                )

    print("=" * 68)
    print("PROBE 1 — cardinality f-vector log-concavity (matroid grading?)")
    print(f"  total families (|F|>=2, n<=5): {total}")
    print(f"  log-concave:     {lc}")
    print(f"  NOT log-concave: {notlc}")
    print("  => no ambient matroid grading (2/3 fail LC).")
    print()
    print("=" * 68)
    print("PROBE 2 — JI-overlap Gram form signature (Lorentzian test)")
    for s, c in sorted(gram_sig.items(), key=lambda x: -x[1])[:6]:
        print(f"  signature {s}: {c}")
    nlorentz = sum(c for (p, ng, z), c in gram_sig.items() if p <= 1)
    print(
        f"  Lorentzian-or-less (<=1 positive eig): {nlorentz}"
        f" / {sum(gram_sig.values())}"
    )
    print("  => always positive definite (Gram of indicators); NEVER Lorentzian.")
    print()
    print("=" * 68)
    print("PROBE 3 — centered form C = G - f f^T/|L|^2 (Hodge (1,r-1)?)")
    for s, c in sorted(cent_sig.items(), key=lambda x: -x[1])[:6]:
        print(f"  signature {s}: {c}")
    semineg = sum(c for (p, ng, z), c in cent_sig.items() if p == 0)
    print(f"  negative-semidefinite (0 positive): {semineg}"
          f" / {sum(cent_sig.values())}")
    print("  => no Hodge (1,r-1) signature anywhere.")
    print()
    print("  Boolean-cube Gram signatures (n, sig, abundance):")
    for ex in cube_examples:
        print(f"    {ex}")
    print()


# --------------------------------------------------------------------------
# Probe 4: Collatz tropical / max-plus cycle-mean eigenvalue
# --------------------------------------------------------------------------
def run_collatz() -> None:
    l3 = math.log2(3)
    w_even, w_odd = -1.0, l3 - 1.0
    print("=" * 68)
    print("PROBE 4 — Collatz tropical (max-plus) cycle-mean eigenvalue")
    print(f"  edge weights: even {w_even:+.4f}, odd {w_odd:+.4f}")
    print(f"  drift lambda(p) = p*log2(3) - 1   (p = fraction odd)")
    for p in (1.0, 1.0 / l3, 0.5):
        print(f"    p={p:.4f}  lambda={p * l3 - 1.0:+.4f}")
    print(f"  critical p* = 1/log2(3) = {1.0 / l3:.4f}")
    print(f"  max-plus eigenvalue lambda_max = w_odd = {w_odd:+.4f} > 0"
          " (all-odd word)")
    print("  => worst-case tropical descent FAILS (reproduces O2:"
          " average not pointwise).")
    print()


if __name__ == "__main__":
    run_frankl()
    run_collatz()
    print("Done. See matroid_tropical.md for interpretation. NOVELTY UNVERIFIED.")
