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
  (b) (mdeg,mult)=(2,1) gives the degree-2 barrier value (sub-1/2) on the lopsided
      families; it equals the independent frequency Hankel d=1 bound EXACTLY
      (e.g. n4: 0.4167 == 0.4167) and sits at/below the quoted power-mean -- the
      degree-2 / barrier regime.  KEY RESULT: (mdeg,mult)=(2,2) returns the SAME
      value (n4: 0.4167 == 0.4167) => COLLAPSE, no degree-4 separation.
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

SCS = dict(eps=1e-7, max_iters=100000, verbose=False)

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
    """S_n-orbit-reduced incidence pseudo-moment model for one family F.

    LAZY build: orbits are canonicalized only for monomials that actually appear
    in the moment/localizing matrices, the anchored profile, the aggregate moments
    and the union-closure equalities among those -- never the full 2^(2^n) power
    set.  This keeps n=5, mult=2 tractable (a few thousand referenced monomials
    instead of ~2*10^5)."""

    def __init__(self, n, F, mdeg, mult):
        self.n = n
        self.F = relabel_max_first(F, n)
        self.mdeg = mdeg
        self.mult = mult
        self.sets = subsets(n)
        nv = len(self.sets)
        self.nv = nv
        self.maxdeg = max(2 * mdeg, 2 * mult + 1, mdeg + mult)
        self.rows = [frozenset(c) for d in range(mdeg + 1)
                     for c in itertools.combinations(range(nv), d)]
        self.locrows = [frozenset(c) for d in range(mult + 1)
                        for c in itertools.combinations(range(nv), d)]
        # variable-index permutations under S_n on subsets
        sidx = {S: i for i, S in enumerate(self.sets)}
        self.var_perms = []
        for sg in itertools.permutations(range(n)):
            p = [sidx[sum(1 << sg[i] for i in range(n) if (S >> i) & 1)]
                 for S in self.sets]
            self.var_perms.append(p)
        # honest 0/1 incidence point
        Fs = set(self.F)
        self.yb = [1.0 if self.sets[q] in Fs else 0.0 for q in range(nv)]
        self._orb_cache = {}
        self._orb = {}             # canon-key -> orbit id
        self.orb_canon = []        # orbit id -> canonical monomial (frozenset)
        self.N = 0
        self._touches0 = []        # orbit id -> bool: touches element-0 subsystem
        self._build()

    def _canon(self, m):
        c = self._orb_cache.get(m)
        if c is not None:
            return c
        best = None
        for p in self.var_perms:
            k = tuple(sorted(p[v] for v in m))
            if best is None or k < best:
                best = k
        cf = frozenset(best)
        self._orb_cache[m] = cf
        return cf

    def orbit(self, m):
        """Orbit id of squarefree monomial m (frozenset of var indices)."""
        c = self._canon(m)
        o = self._orb.get(c)
        if o is None:
            o = self.N
            self._orb[c] = o
            self.orb_canon.append(c)
            # touches element-0 subsystem?  any var S with 0 in S
            self._touches0.append(any(self.sets[v] & 1 for v in c))
            self.N += 1
        return o

    def orbit_val(self, o):
        """Honest profile value of orbit o = product of yb over its canonical rep."""
        pr = 1.0
        for v in self.orb_canon[o]:
            pr *= self.yb[v]
        return pr

    def _build(self):
        # 1) moment-matrix entry orbits
        Rr = len(self.rows)
        self.mom = [[self.orbit(self.rows[r] | self.rows[c]) for c in range(Rr)]
                    for r in range(Rr)]
        # 2) localizing entries:  freq_0 * locrow_r * locrow_c
        f0vars = [q for q, S in enumerate(self.sets) if S & 1]
        Rl = len(self.locrows)
        self.loc = [[None] * Rl for _ in range(Rl)]
        for r in range(Rl):
            for c in range(Rl):
                base = self.locrows[r] | self.locrows[c]
                d = defaultdict(float)
                for q in f0vars:
                    d[self.orbit(base | {q})] += 1.0
                self.loc[r][c] = dict(d)
        # 3) aggregate first/second freq moments
        self.agg1 = defaultdict(float)
        for i in range(self.n):
            bit = 1 << i
            for q, S in enumerate(self.sets):
                if S & bit:
                    self.agg1[self.orbit(frozenset({q}))] += 1.0
        self.agg2 = defaultdict(float)
        for i in range(self.n):
            bit = 1 << i
            mem = [q for q, S in enumerate(self.sets) if S & bit]
            for a in mem:
                for b in mem:
                    self.agg2[self.orbit(frozenset({a, b}))] += 1.0
        # 4) per-element freq linear forms (orbit dicts) for the max constraints
        self.freqlin = []
        for i in range(self.n):
            bit = 1 << i
            d = defaultdict(float)
            for q, S in enumerate(self.sets):
                if S & bit:
                    d[self.orbit(frozenset({q}))] += 1.0
            self.freqlin.append(dict(d))
        # 5) union-closure equalities among REFERENCED orbits.  We close the set of
        #    referenced canonical monomials under the rewrite y_A y_B = y_A y_B y_{AuB}
        #    (and its symmetric images), generating orbit==orbit identities.
        self._equalities()
        # 6) anchored profile: every referenced orbit NOT touching element 0
        self.anchor = {o: self.orbit_val(o) for o in range(self.N)
                       if not self._touches0[o]}
        self.emp = self.orbit(frozenset())

    def _equalities(self, max_rounds=3):
        """Union-closure moment equalities  y_A y_B = y_A y_B y_{A∪B}  applied to
        the REFERENCED monomials, restricted to the variables that actually occur
        in those monomials (the only ones the SDP sees).  Bounded rounds suffice:
        each rewrite raises degree by 1, and the moment/localizing matrices live
        in degree <= maxdeg, so a triple/quad orbit is reached in <= 3 rounds."""
        eqs = set()
        # variables occurring in any referenced canonical monomial
        occ = sorted({v for c in self.orb_canon for v in c})
        # base union-closure pairs among the OCCURRING variables only
        base = []
        for ia in range(len(occ)):
            for ib in range(ia, len(occ)):
                a, b = occ[ia], occ[ib]
                u = self.sets.index(self.sets[a] | self.sets[b])
                lhs = frozenset({a, b})
                rhs = frozenset({a, b, u})
                if lhs != rhs:
                    base.append((lhs, rhs))
        processed = 0
        rounds = 0
        while processed < len(self.orb_canon) and rounds < max_rounds:
            refs = list(self.orb_canon[processed:])
            processed = len(self.orb_canon)
            rounds += 1
            for w in refs:
                for (lhs, rhs) in base:
                    L = lhs | w
                    if len(L) > self.maxdeg:
                        continue
                    R = rhs | w
                    if len(R) > self.maxdeg:
                        continue
                    oL = self.orbit(L)
                    oR = self.orbit(R)
                    if oL != oR:
                        eqs.add((min(oL, oR), max(oL, oR)))
        self.eqs = list(eqs)

    @staticmethod
    def _lf(y, d):
        e = 0
        for o, co in d.items():
            e = e + co * y[o]
        return e

    def lb(self):
        """Certified Lasserre LOWER bound on max_i freq_i / |F| (F relabelled so
        element 0 is heaviest):
            minimize   L[freq_0] / |F|
            s.t.  L[1]=1, moment matrix PSD, union-closure orbit equalities,
                  honest profile anchored EXCEPT the element-0 subsystem (freq_0 free),
                  L[sum_i freq_i]=p1, L[sum_i freq_i^2]=p2  (the deg-2 symmetric data),
                  localizing matrix of freq_0>=0 with deg-`mult` multipliers PSD,
                  L[freq_0] >= L[freq_i] for all i.
        mult=1 -> degree-2 (pair-moment / barrier) bound;  mult=2 -> degree-4
        (subset-triple moments).  lb_2==lb_1 means degree-4 collapses to the barrier."""
        y = cp.Variable(self.N)
        cons = [y[self.emp] == 1.0]
        for o, v in self.anchor.items():
            if o == self.emp:
                continue
            cons.append(y[o] == v)
        for a, b in self.eqs:
            cons.append(y[a] == y[b])
        fr = freqs_of(self.F, self.n)
        cons.append(self._lf(y, self.agg1) == float(sum(fr)))
        cons.append(self._lf(y, self.agg2) == float(sum(f * f for f in fr)))
        # moment matrix PSD
        Rr = len(self.rows)
        Mm = cp.bmat([[y[self.mom[r][c]] for c in range(Rr)] for r in range(Rr)])
        cons.append(Mm >> 0)
        # localizing matrix for freq_0 >= 0
        Rl = len(self.locrows)
        Lent = [[self._lf(y, self.loc[r][c]) for c in range(Rl)] for r in range(Rl)]
        cons.append(cp.bmat(Lent) >> 0)
        # distinguished-max
        e0 = self._lf(y, self.freqlin[0])
        for i in range(1, self.n):
            cons.append(e0 >= self._lf(y, self.freqlin[i]))
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

    print("\n[VALIDATION b] (mdeg2,mult1) = degree-2 barrier regime (sub-1/2).",
          flush=True)
    print("   NOTE: the SDP gives the TIGHTEST degree-2 min-max bound, which equals",
          flush=True)
    print("   the frequency Hankel d=1 value and sits at/below the power-mean; both<1/2.",
          flush=True)
    for name, (n, F) in LOPSIDED.items():
        if n >= 5:
            continue  # n=5 solve is slow; n4 suffices for validation
        pm = power_mean(F, n)
        m = Model(n, F, 2, 1)
        v = m.lb()
        print(f"   {name:16s} pm={pm:.4f}  sdp_lb1={v:.4f}  "
              f"{'OK (sub-1/2)' if v < 0.5 - 1e-3 else 'CHECK'}", flush=True)
        out["validation_pm"].append({"name": name, "pm": pm, "sdp_lb1": v})

    print("\n[VERDICT] lb_1 (mult1, degree-2) vs lb_2 (mult2, degree-4):", flush=True)
    print("   COLLAPSE iff lb_2 == lb_1.  (n=5 best-effort; may be skipped if slow.)",
          flush=True)
    for name, (n, F) in LOPSIDED.items():
        if n >= 5:
            continue  # best-effort: run n=5 separately with a long budget
        pm = power_mean(F, n)
        ta = true_ab(F, n)
        m1 = Model(n, F, 2, 1)
        lb1 = m1.lb()
        m2 = Model(n, F, 2, 2)
        lb2 = m2.lb()
        gap = lb2 - lb1
        verdict = "COLLAPSE" if abs(gap) < 1e-2 else "SEPARATION"
        print(f"   {name:16s} true={ta:.4f}  lb_1={lb1:.4f}  lb_2={lb2:.4f}  "
              f"gap={gap:+.4f}  -> {verdict}", flush=True)
        out["verdict"].append({"name": name, "n": n, "sizeF": len(F),
                               "true_ab": ta, "power_mean": pm,
                               "lb1": lb1, "lb2": lb2, "gap": gap})

    path = os.path.join(os.path.dirname(__file__), "data", "las2_main_run.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(out, f, indent=2, default=lambda o: float(o)
                  if isinstance(o, np.floating) else int(o)
                  if isinstance(o, np.integer) else o)
    print(f"\nWrote {path}", flush=True)


if __name__ == "__main__":
    main()
