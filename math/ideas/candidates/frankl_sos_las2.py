"""
frankl_sos_las2.py -- Lasserre / SOS incidence-moment SDP for Frankl, driven by a
                      REAL SDP solver (cvxpy + SCS).  Decides whether degree-4 SOS
                      ESCAPES the degree-2 (moment / power-mean) barrier on the
                      lopsided union-closed families, or COLLAPSES onto it.

Author: Alex Ye (no AI on author line).   [NOVELTY UNVERIFIED]

--------------------------------------------------------------------------------
THE OBJECT
--------------------------------------------------------------------------------
Variables = incidence indicators y_S = 1[S in F], S subset of [n] (2^n of them).
freq_i = sum_{S ni i} y_S,  |F| = sum_S y_S.  For a fixed family F, abundance(F)
= max_i freq_i / |F| (the project must show this is >= 1/2; Frankl).

A degree-2d SOS / Lasserre LOWER bound on max_i freq_i is what the relaxation can
certify.  The relaxation knows F only through its S_n-symmetric (orbit) moment
profile -- the standard symmetry reduction (Gatermann-Parrilo / Bachoc-Vallentin),
and exactly what makes the proven barrier the power-mean p2/p1/|F| rather than the
true value.  We compute, per family, the certified lower bound

    lb(F; mdeg, mult) = min t  s.t.  there is a pseudo-expectation L with
        L[1]=1, moment matrix (rows = monomials up to degree `mdeg`) PSD,
        union-closure orbit equalities  L[y_A y_B] = L[y_A y_B y_{AuB}],
        L matches F's honest S_n-orbit profile EXCEPT on the element-0 frequency
            subsystem (so freq_0, the distinguished candidate-max element after
            relabelling F so element 0 is heaviest, stays free), and the
        localizing matrix of  g = t*|F| - freq_0  with multiplier rows up to
            degree `mult`  is PSD   (the Schmuedgen/Putinar abundance term).

  * (mdeg, mult) = (2, 1)  ->  degree-2 / "level-1" certificate.  The localizing
    multiplier of degree 1 makes the term see the pair moments L[y_S y_T], i.e.
    the second power sum p2 = sum_{A,B}|A cap B| -- so this reproduces the
    power-mean barrier  p2/p1/|F|.  This is the proven barrier value lb_1.
  * (mdeg, mult) = (2, 2)  ->  degree-4 / "level-2": multiplier degree 2 brings in
    the subset-TRIPLE moments L[y_S y_T y_U] and the union-closure coupling among
    them -- the genuinely-non-frequency content the barrier theorem does not
    cover.  This value is lb_2.  (mdeg can also be raised to 3/4 for a fuller
    degree-6/8 moment matrix; mult is the part that lifts the abundance bound.)

VERDICT RULE:  lb_2 = 1/2 > lb_1 on a lopsided family => GENUINE degree-4
separation.  lb_2 = lb_1 => collapse (degree-4 = the barrier, a tautology).

--------------------------------------------------------------------------------
VALIDATION GATES (printed first; must pass before lb_2 is trusted):
  (a) Boolean cube 2^[k]: lb = 1/2 EXACTLY at every (mdeg,mult)  (the proven
      degree-independent ceiling -- SOS can at most REACH 1/2).
  (b) (mdeg,mult)=(2,1) reproduces the power-mean barrier on the lopsided families.
--------------------------------------------------------------------------------
Run:  python3 frankl_sos_las2.py
"""
from __future__ import annotations
import itertools
import json
import os
import sys
from collections import defaultdict
import numpy as np

try:
    import cvxpy as cp
    HAVE = True
except Exception:
    HAVE = False

SCS = dict(eps=1e-8, max_iters=200000, verbose=False)

# the six lopsided n<=5 families where lb_1 (power-mean) dips below 1/2
# (from frankl/experiments/data/overlap_counterexamples.txt; masks bit-encode subsets)
LOPSIDED = {
    "n5_F3a_minimal": (5, [0, 16, 31]),       # freq [1,1,1,1,2]  pm 0.4444  {emptyset,{4},[5]}
    "n4_F3":          (4, [0, 8, 15]),        # freq [1,1,1,2]    pm 0.4667
    "n5_F3b":         (5, [0, 16, 23]),       # freq [1,1,1,0,2]  pm 0.4667
    "n5_F5":          (5, [0, 8, 16, 24, 31]),    # freq [1,1,1,3,3] pm 0.4667
    "n5_F6":          (5, [0, 8, 16, 23, 24, 31]),  # freq [2,2,2,3,4] pm 0.4744
    "n5_F7":          (5, [0, 8, 15, 16, 23, 24, 31]),  # freq [3,3,3,4,4] pm 0.4958
}


def subsets(n):
    return list(range(1 << n))


def freqs_of(F, n):
    return [sum(1 for S in F if (S >> i) & 1) for i in range(n)]


def true_ab(F, n):
    return max(freqs_of(F, n)) / len(F)


def power_mean(F, n):
    fr = freqs_of(F, n)
    p1, p2, M = sum(fr), sum(f * f for f in fr), len(F)
    return (p2 / p1) / M if p1 else 0.0


def relabel_max_first(F, n):
    fr = freqs_of(F, n)
    j = int(np.argmax(fr))
    if j == 0:
        return list(F)
    p = list(range(n))
    p[0], p[j] = p[j], p[0]
    return [sum(1 << p[i] for i in range(n) if (S >> i) & 1) for S in F]


class Model:
    """S_n-orbit-reduced incidence pseudo-moment model for one family F."""

    def __init__(self, n, F, mdeg, mult):
        self.n = n
        self.F = relabel_max_first(F, n)
        self.mdeg = mdeg
        self.mult = mult
        self.sets = subsets(n)
        nv = len(self.sets)
        self.nv = nv
        self.maxdeg = max(2 * mdeg, 2 * mult + 1, mdeg + mult)
        self.monos = [frozenset(c) for d in range(self.maxdeg + 1)
                      for c in itertools.combinations(range(nv), d)]
        self.midx = {m: i for i, m in enumerate(self.monos)}
        self.rows = [frozenset(c) for d in range(mdeg + 1)
                     for c in itertools.combinations(range(nv), d)]
        self.locrows = [frozenset(c) for d in range(mult + 1)
                        for c in itertools.combinations(range(nv), d)]
        self._orbits()
        self._profile()
        self._equalities()

    def _orbits(self):
        perms = []
        for sg in itertools.permutations(range(self.n)):
            p = [0] * self.nv
            for q, S in enumerate(self.sets):
                T = sum(1 << sg[i] for i in range(self.n) if (S >> i) & 1)
                p[q] = self.sets.index(T)
            perms.append(p)

        def canon(m):
            best = None
            for p in perms:
                k = tuple(sorted(p[v] for v in m))
                if best is None or k < best:
                    best = k
            return best
        orb = {}
        self.orbof = [0] * len(self.monos)
        for i, m in enumerate(self.monos):
            c = canon(m)
            if c not in orb:
                orb[c] = len(orb)
            self.orbof[i] = orb[c]
        self.N = len(orb)

    def _profile(self):
        Fs = set(self.F)
        yb = [1.0 if self.sets[q] in Fs else 0.0 for q in range(self.nv)]
        sm = defaultdict(float)
        cn = defaultdict(float)
        for i, m in enumerate(self.monos):
            pr = 1.0
            for v in m:
                pr *= yb[v]
            sm[self.orbof[i]] += pr
            cn[self.orbof[i]] += 1.0
        self.vals = {o: sm[o] / cn[o] for o in sm}

    def _equalities(self):
        eqs = set()
        for a in range(self.nv):
            for b in range(a, self.nv):
                u = self.sets.index(self.sets[a] | self.sets[b])
                lhs = frozenset({a, b})
                rhs = frozenset({a, b, u})
                if lhs == rhs:
                    continue
                for w in self.monos:
                    L = lhs | w
                    R = rhs | w
                    if len(L) > self.maxdeg or len(R) > self.maxdeg:
                        continue
                    iL = self.midx.get(L)
                    iR = self.midx.get(R)
                    if iL is None or iR is None:
                        continue
                    oL, oR = self.orbof[iL], self.orbof[iR]
                    if oL != oR:
                        eqs.add((min(oL, oR), max(oL, oR)))
        self.eqs = list(eqs)

    def _linform(self, y, d):
        e = 0
        for mono, co in d.items():
            idx = self.midx.get(mono)
            if idx is not None:
                e = e + co * y[self.orbof[idx]]
        return e

    def _freq(self, i):
        bit = 1 << i
        d = defaultdict(float)
        for q, S in enumerate(self.sets):
            if S & bit:
                d[frozenset({q})] += 1.0
        return dict(d)

    def lb(self):
        """Certified Lasserre LOWER bound on max_i freq_i / |F|.

        DIRECT minimization (F relabeled so element 0 is heaviest):
            minimize   L[freq_0] / |F|
            s.t.  moment matrix PSD, union-closure orbit equalities, L[1]=1,
                  the element-0 frequency subsystem FREE (so freq_0 can move) but
                  the rest of F's honest symmetric profile anchored,
                  the AGGREGATE first moment anchored  L[sum_i freq_i] = p1  (so
                    pulling freq_0 down must push the others up -> coupling),
                  the localizing matrix of freq_0 >= 0 (deg-`mult` multipliers) PSD
                    -- this brings the pair/triple moments of freq_0 into play,
                  and the distinguished-max constraints  L[freq_0] >= L[freq_i].
        The PSD moment matrix + the union-closure + the anchored Sum freq^2 (a
        degree-2 symmetric datum) force  L[freq_0] >= p2/p1  at mult>=1 (the
        power-mean barrier); mult=2 additionally couples the subset-triple moments."""
        y = cp.Variable(self.N)
        cons = [y[self.orbof[self.midx[frozenset()]]] == 1.0]
        # anchor honest profile, EXCEPT monomials touching the element-0 subsystem
        seen = set()
        for i, m in enumerate(self.monos):
            o = self.orbof[i]
            if o in seen:
                continue
            seen.add(o)
            if len(m) == 0:
                continue
            if any(self.sets[v] & 1 for v in m):
                continue
            cons.append(y[o] == self.vals[o])
        for a, b in self.eqs:
            cons.append(y[a] == y[b])
        # aggregate first moment: L[sum_i freq_i] = p1 (couples freq_0 to the rest)
        fr = freqs_of(self.F, self.n)
        p1 = float(sum(fr))
        allfreq = defaultdict(float)
        for i in range(self.n):
            for mono, co in self._freq(i).items():
                allfreq[mono] += co
        cons.append(self._linform(y, dict(allfreq)) == p1)
        # aggregate second moment: L[sum_i freq_i^2] = p2 (the degree-2 symmetric
        # datum = sum_{A,B}|A&B|).  freq_i^2 = sum_{S,T ni i} y_S y_T.
        p2 = float(sum(f * f for f in fr))
        sq = defaultdict(float)
        for i in range(self.n):
            bit = 1 << i
            mem = [q for q, S in enumerate(self.sets) if S & bit]
            for a in mem:
                for b in mem:
                    sq[frozenset({a, b})] += 1.0
        cons.append(self._linform(y, dict(sq)) == p2)
        # moment matrix PSD
        Rr = len(self.rows)
        Mm = cp.bmat([[y[self.orbof[self.midx[self.rows[r] | self.rows[c]]]]
                       for c in range(Rr)] for r in range(Rr)])
        cons.append(Mm >> 0)
        # localizing matrix for freq_0 >= 0 with degree-`mult` multipliers
        f0 = self._freq(0)
        lr = self.locrows
        Rl = len(lr)
        Lent = [[None] * Rl for _ in range(Rl)]
        okall = True
        for r in range(Rl):
            for c in range(Rl):
                base = lr[r] | lr[c]
                d = defaultdict(float)
                ok = True
                for mono, co in f0.items():
                    full = base | mono
                    iF = self.midx.get(full)
                    if iF is None:
                        ok = False
                        break
                    d[self.orbof[iF]] += co
                if not ok:
                    okall = False
                Lent[r][c] = (sum(co * y[o] for o, co in d.items())
                              if ok else cp.Constant(0))
        if okall:
            cons.append(cp.bmat(Lent) >> 0)
        # distinguished-max: L[freq_0] >= L[freq_i]
        e0 = self._linform(y, f0)
        for i in range(1, self.n):
            cons.append(e0 >= self._linform(y, self._freq(i)))
        MF = float(len(self.F))
        obj = e0 / MF
        prob = cp.Problem(cp.Minimize(obj), cons)
        try:
            prob.solve(solver=cp.SCS, **SCS)
        except Exception:
            return float("nan")
        if prob.status not in ("optimal", "optimal_inaccurate"):
            return float("nan")
        return float(obj.value)


def main():
    print("=" * 78)
    print("Frankl incidence-moment SOS  [cvxpy+SCS]   Author: Alex Ye")
    print("Does degree-4 (mult=2) SOS escape the degree-2 (mult=1) power-mean barrier?")
    print("=" * 78, flush=True)
    if not HAVE:
        print("ERROR: cvxpy missing")
        sys.exit(1)
    import cvxpy
    print(f"cvxpy {cvxpy.__version__}  SCS opts={SCS}", flush=True)

    out = {"validation_cube": [], "validation_pm": [], "verdict": []}

    print("\n[VALIDATION a] cube 2^[k] must give lb = 0.5 at every (mdeg,mult).", flush=True)
    for k in (1, 2, 3):
        F = subsets(k)
        row = {"k": k}
        for (md, mu) in [(2, 1), (2, 2)]:
            m = Model(k, F, md, mu)
            v = m.lb()
            row[f"lb_md{md}_mu{mu}"] = v
            print(f"   cube 2^[{k}] (mdeg{md},mult{mu}): lb={v:.4f} N={m.N} "
                  f"{'OK' if abs(v - 0.5) < 0.03 else 'FAIL'}", flush=True)
        out["validation_cube"].append(row)

    print("\n[VALIDATION b] (mdeg2,mult1) must reproduce power-mean barrier lb_1.",
          flush=True)
    for name, (n, F) in LOPSIDED.items():
        pm = power_mean(F, n)
        m = Model(n, F, 2, 1)
        v = m.lb()
        ok = abs(v - pm) < 0.03
        print(f"   {name:16s} pm={pm:.4f}  sdp_lb1={v:.4f}  "
              f"{'OK' if ok else 'CHECK'}", flush=True)
        out["validation_pm"].append({"name": name, "pm": pm, "sdp_lb1": v, "ok": ok})

    print("\n[VERDICT] lb_1 (mult1, degree-2) vs lb_2 (mult2, degree-4):", flush=True)
    for name, (n, F) in LOPSIDED.items():
        pm = power_mean(F, n)
        ta = true_ab(F, n)
        m1 = Model(n, F, 2, 1)
        lb1 = m1.lb()
        m2 = Model(n, F, 2, 2)
        lb2 = m2.lb()
        gap = lb2 - lb1
        print(f"   {name:16s} true={ta:.4f}  lb_1={lb1:.4f}  lb_2={lb2:.4f}  "
              f"gap={gap:+.4f}  N1={m1.N} N2={m2.N}", flush=True)
        out["verdict"].append({"name": name, "n": n, "sizeF": len(F),
                               "true_ab": ta, "power_mean": pm,
                               "lb1": lb1, "lb2": lb2, "gap": gap,
                               "N1": m1.N, "N2": m2.N})

    path = os.path.join(os.path.dirname(__file__), "data", "las2_results.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(out, f, indent=2, default=lambda o: float(o)
                  if isinstance(o, np.floating) else int(o)
                  if isinstance(o, np.integer) else o)
    print(f"\nWrote {path}", flush=True)


if __name__ == "__main__":
    main()
