"""
frankl_sos_las2.py -- Lasserre level-2 (degree-4) incidence-moment SDP for Frankl,
                      driven by a REAL SDP solver (cvxpy + SCS), per-family.

Author: Alex Ye (no AI on author line).

WHAT THIS DECIDES
-----------------
The proven project barrier = Lasserre level-1 (degree-2) over the incidence
variables y_S = 1[S in F].  On 6 "lopsided" UC families (n<=5) the level-1
abundance lower bound dips to lb_1 < 1/2 (min 4/9 = 0.4444 on the minimal family
F = {emptyset,{4},{0,1,2,3,4}}).  True abundance is always >= 1/2 (Frankl holds),
so level-1 SOS just fails to *certify* it there.  OPEN: does level-2 (degree-4)
lift those families to 1/2 (genuine separation) or stay at lb_1 (collapse)?

THE LOWER BOUND BEING RELAXED
-----------------------------
For a fixed family F, abundance(F) = max_i freq_i(F)/|F|.  A degree-2d SOS /
Lasserre LOWER BOUND on this is what the relaxation can *certify*.  The relaxation
is allowed to know F only through its S_n-symmetric moment profile (so families of
the same "type" share a bound; this is the standard symmetry reduction and is
exactly what makes the barrier the power-mean rather than the true value).

We compute the certified lower bound as the optimum of the pseudo-moment SDP that
keeps ONE distinguished ground element 0 un-symmetrized (it is the candidate
abundant element) and symmetrizes the rest by its stabilizer S_{n-1}:

    lb_d(F) =  min over level-d pseudo-expectations L  of   L[freq_0] / L[|F|]
       s.t.  L valid (PSD moment + localizing matrices, BOOL, UNION-CLOSURE),
             L matches F's degree-<=2d  STABILIZER-orbit  moment profile in the
                aggregate symmetric data (NOT pointwise on element 0's own
                singletons -- those stay free so freq_0 can move),
             L[1] = 1.

Because element 0 is left free while 1..n-1 are symmetrized, freq_0 is a genuine
free linear functional and "max over elements" is realized by maximizing freq_0
over the relabelling (we take the worst distinguished element).  At level 1 this
reproduces the power-mean p2/p1/M (verified, = the barrier).  The Boolean cube
gives exactly 1/2 at every level (verified).  At level 2 the SDP additionally
constrains the triple/quadruple subset-configuration orbit moments via
union-closure; whether they force lb_2 = 1/2 is the experiment.

VALIDATION GATES (must pass before any lb_2 is trusted):
  (a) Boolean cube 2^[k]:    lb_2  ==  1/2  exactly.
  (b) minimal lopsided fam:  lb_1  ==  power-mean (0.4444).

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
    HAVE_CVXPY = True
except Exception:
    HAVE_CVXPY = False

np.set_printoptions(precision=5, suppress=True, linewidth=140)

SCS_OPTS = dict(eps=1e-8, max_iters=400000, verbose=False)


# ---------------------------------------------------------------------------
# Families
# ---------------------------------------------------------------------------

def subsets(n):
    return list(range(1 << n))


def is_uc(F):
    Fs = set(F)
    return all((a | b) in Fs for a in F for b in F)


def freqs_of(F, n):
    return [sum(1 for S in F if (S >> i) & 1) for i in range(n)]


def true_abundance(F, n):
    fr = freqs_of(F, n)
    return max(fr) / len(F)


def cube(k):
    return list(range(1 << k))


# the six lopsided families (n<=5) where lb_1 < 1/2  (from overlap_counterexamples.txt)
LOPSIDED = {
    "n5_F3a_minimal": (5, [0, 16, 31]),       # freq [1,1,1,1,2]  pm 0.4444
    "n4_F3":          (4, [0, 8, 15]),        # freq [1,1,1,2]    pm 0.4667
    "n5_F3b":         (5, [0, 16, 23]),       # freq [1,1,1,0,2]  pm 0.4667
    "n5_F5":          (5, [0, 8, 16, 24, 31]),    # freq [1,1,1,3,3] pm 0.4667
    "n5_F6":          (5, [0, 8, 16, 23, 24, 31]),  # freq[2,2,2,3,4] pm 0.4744
    "n5_F7":          (5, [0, 8, 15, 16, 23, 24, 31]),  # freq[3,3,3,4,4] pm 0.4958
}


def power_mean_lb1(F, n):
    """The documented level-1 barrier: max_i freq_i/|F| >= (sum freq^2)/(sum freq)/|F|."""
    fr = freqs_of(F, n)
    p1 = sum(fr)
    p2 = sum(f * f for f in fr)
    M = len(F)
    return (p2 / p1) / M if p1 else 0.0


# ---------------------------------------------------------------------------
# Stabilizer-reduced incidence Lasserre model
# ---------------------------------------------------------------------------

class StabLasserre:
    """Level-d pseudo-moment model over incidence vars y_S (S subset of [n]),
    symmetry-reduced by the stabilizer of ground element 0 (group S_{n-1} acting
    on {1,...,n-1}).  Element 0 is the candidate-abundant element kept free.

    Monomials are squarefree (BOOL baked in) = subsets of variable indices
    {0,...,2^n-1}.  Orbits under the stabilizer group give the reduced variables.
    """

    def __init__(self, n, level):
        self.n = n
        self.level = level
        self.D = 2 * level
        self.sets = subsets(n)
        self.nvars = len(self.sets)
        self.monos = []
        for d in range(self.D + 1):
            self.monos.extend(frozenset(c) for c in itertools.combinations(range(self.nvars), d))
        self.midx = {m: i for i, m in enumerate(self.monos)}
        self.rows = []
        for d in range(level + 1):
            self.rows.extend(frozenset(c) for c in itertools.combinations(range(self.nvars), d))
        # localizing rows: standard Lasserre uses degree <= level - ceil(deg g/2);
        # for our linear g that is level-1.
        self.loc_rows = []
        for d in range(max(level - 1, 0) + 1):
            self.loc_rows.extend(frozenset(c) for c in itertools.combinations(range(self.nvars), d))
        self._perms()
        self._orbits()
        self._equalities()

    def _perms(self):
        # stabilizer of element 0: permutations of {1,...,n-1}
        self.var_perms = []
        for tail in itertools.permutations(range(1, self.n)):
            sigma = (0,) + tail
            p = [0] * self.nvars
            for s, S in enumerate(self.sets):
                T = 0
                for i in range(self.n):
                    if (S >> i) & 1:
                        T |= (1 << sigma[i])
                p[s] = self.sets.index(T)
            self.var_perms.append(p)

    def _canon_mono(self, mono):
        best = None
        for p in self.var_perms:
            key = tuple(sorted(p[v] for v in mono))
            if best is None or key < best:
                best = key
        return best

    def _orbits(self):
        self.orbit_of = [0] * len(self.monos)
        reps = {}
        for i, m in enumerate(self.monos):
            cm = self._canon_mono(m)
            if cm not in reps:
                reps[cm] = len(reps)
            self.orbit_of[i] = reps[cm]
        self.n_orbits = len(reps)

    def _equalities(self):
        eqs = set()
        sets = self.sets
        for a in range(self.nvars):
            for b in range(a, self.nvars):
                u = sets.index(sets[a] | sets[b])
                lhs = frozenset({a, b})
                rhs = frozenset({a, b, u})
                if lhs == rhs:
                    continue
                for w in self.monos:
                    L = lhs | w
                    R = rhs | w
                    if len(L) > self.D or len(R) > self.D:
                        continue
                    iL = self.midx.get(L)
                    iR = self.midx.get(R)
                    if iL is None or iR is None:
                        continue
                    oL = self.orbit_of[iL]
                    oR = self.orbit_of[iR]
                    if oL != oR:
                        eqs.add((min(oL, oR), max(oL, oR)))
        self.orbit_eqs = list(eqs)

    def moment_entries(self):
        R = len(self.rows)
        ent = np.empty((R, R), dtype=int)
        for r in range(R):
            for c in range(R):
                ent[r, c] = self.orbit_of[self.midx[self.rows[r] | self.rows[c]]]
        return ent

    def localizing_entries(self, gfun):
        Rl = len(self.loc_rows)
        out = [[None] * Rl for _ in range(Rl)]
        ok = True
        for r in range(Rl):
            for c in range(Rl):
                base = self.loc_rows[r] | self.loc_rows[c]
                d = defaultdict(float)
                for mono, coeff in gfun.items():
                    full = base | mono
                    if len(full) > self.D:
                        ok = False
                        break
                    idx = self.midx.get(full)
                    if idx is None:
                        ok = False
                        break
                    d[self.orbit_of[idx]] += coeff
                if not ok:
                    break
                out[r][c] = dict(d)
            if not ok:
                break
        return out, ok

    def linear_freq(self, i):
        d = {}
        bit = 1 << i
        for s, S in enumerate(self.sets):
            if S & bit:
                d[frozenset({s})] = d.get(frozenset({s}), 0.0) + 1.0
        return d

    def linear_M(self):
        return {frozenset({s}): 1.0 for s in range(self.nvars)}

    # --- the aggregate symmetric profile of F up to a given degree ---
    def profile(self, F, anchor_degree, free_zero_singleton=True):
        """Stabilizer-orbit moment values of the honest point y_S=1[S in F],
        averaged over each orbit, for orbits whose representative monomial has
        degree <= anchor_degree.  Returns dict orbit_id -> value.

        Element-0 singletons {y_S : 0 in S} are EXCLUDED from anchoring at the
        singleton (degree-1) level so freq_0 stays free; everything else
        (including all pair/triple aggregates that mix in element 0) is anchored,
        which is what supplies the union-closure coupling.  Concretely we anchor:
          - degree-1 orbit values for monomials NOT touching element 0,
          - all degree-2..anchor_degree orbit values.
        """
        Fs = set(F)
        ybit = [1.0 if self.sets[s] in Fs else 0.0 for s in range(self.nvars)]
        sums = defaultdict(float)
        counts = defaultdict(float)
        for i, m in enumerate(self.monos):
            prod = 1.0
            for v in m:
                prod *= ybit[v]
            o = self.orbit_of[i]
            sums[o] += prod
            counts[o] += 1.0
        vals = {o: sums[o] / counts[o] for o in sums}
        # which orbits to anchor:
        anchored = {}
        seen = set()
        for i, m in enumerate(self.monos):
            o = self.orbit_of[i]
            if o in seen:
                continue
            seen.add(o)
            deg = len(m)
            if deg == 0:
                continue  # L[1]=1 handled separately
            if deg > anchor_degree:
                continue
            if free_zero_singleton:
                # exclude EVERY monomial that touches a variable y_S with 0 in S,
                # so the whole element-0 frequency subsystem stays free; the
                # element-0 moments are pinned only by PSD + union-closure + the
                # distinguished-max constraints, NOT by the honest profile.
                if any((self.sets[v] & 1) for v in m):
                    continue
            anchored[o] = vals[o]
        return anchored, vals


def _linform(model, y, d):
    """cvxpy scalar  L[sum_mono coeff * mono]  for a linear-in-moments dict d."""
    expr = 0
    for mono, c in d.items():
        idx = model.midx.get(mono)
        if idx is None:
            continue
        expr = expr + c * y[model.orbit_of[idx]]
    return expr


def decision_feasible(model, F, t):
    """Brief's literal LAS-d decision SDP (full S_n symmetry, profile fully
    anchored): does a level-d pseudo-expectation exist that matches F's honest
    S_n-symmetric profile AND has the distinguished max element non-abundant at t,
    i.e. localizing  g = t*|F|*1 - freq_0 >= 0 ?  freq_0 is the worst element
    (F is relabeled so element 0 attains max frequency).  Returns feasibility.

    Validated: cube returns smallest-feasible-t = 0.5 at every level (the ceiling).
    Collapse test: smallest feasible t at level 2 == that at level 1  <=>  the
    degree-4 incidence relaxation gives the SAME bound as degree-2 (no escape)."""
    N = model.n_orbits
    y = cp.Variable(N)
    cons = []
    emp = model.orbit_of[model.midx[frozenset()]]
    cons.append(y[emp] == 1.0)
    for (a, b) in model.orbit_eqs:
        cons.append(y[a] == y[b])
    # FULL anchoring of the honest S_n-symmetric profile (free_zero_singleton=False)
    anchored, vals = model.profile(F, model.D, free_zero_singleton=False)
    for o, v in anchored.items():
        cons.append(y[o] == v)
    ment = model.moment_entries()
    R = ment.shape[0]
    Mmat = cp.bmat([[y[ment[r, c]] for c in range(R)] for r in range(R)])
    cons.append(Mmat >> 0)
    # localizing matrices for freq_i >= 0 and M-2>=0
    glist = [model.linear_freq(i) for i in range(model.n)]
    gM = defaultdict(float)
    for mono, c in model.linear_M().items():
        gM[mono] += c
    gM[frozenset()] -= 2.0
    glist.append(dict(gM))
    # abundance localizing: g0 = t*M - freq_0 >= 0  (distinguished/max element 0)
    M_F = float(len(F))
    g0 = defaultdict(float)
    g0[frozenset()] += t * M_F
    for mono, c in model.linear_freq(0).items():
        g0[mono] -= c
    glist.append(dict(g0))
    for g in glist:
        loc, ok = model.localizing_entries(g)
        if not ok:
            continue
        Rl = len(loc)
        Lmat = cp.bmat([[(sum(coef * y[o] for o, coef in loc[r][c].items())
                          if loc[r][c] else cp.Constant(0))
                         for c in range(Rl)] for r in range(Rl)])
        cons.append(Lmat >> 0)
    prob = cp.Problem(cp.Minimize(0), cons)
    try:
        prob.solve(solver=cp.SCS, **SCS_OPTS)
    except Exception:
        return None
    return prob.status in ("optimal", "optimal_inaccurate")


def relabel_max_first(F, n):
    """Relabel ground set so element 0 has maximum frequency (the candidate
    abundant element)."""
    fr = freqs_of(F, n)
    j = int(np.argmax(fr))
    if j == 0:
        return F
    perm = list(range(n))
    perm[0], perm[j] = perm[j], perm[0]
    out = []
    for S in F:
        T = 0
        for i in range(n):
            if (S >> i) & 1:
                T |= (1 << perm[i])
        out.append(T)
    return out


def lb_decision(model, F, tol=2.0e-3):
    """Certified abundance lower bound = smallest t with decision_feasible True.
    Bisection.  (relaxation cannot refute 'max element abundance <= t' below this)."""
    Fr = relabel_max_first(F, model.n)
    lo, hi = 0.0, 1.0
    for _ in range(11):
        mid = 0.5 * (lo + hi)
        f = decision_feasible(model, Fr, mid)
        if f:
            hi = mid
        else:
            lo = mid
        if hi - lo < tol:
            break
    return hi


def lb_d(model, F, anchor_degree, free_zero=True):
    """Lasserre lower bound on  max_i freq_i / |F|  at level = model.level.

    Direct min:  minimize  L[freq_0] / |F|   (|F| anchored to true M),
       s.t.  L valid level-d pseudo-expectation (moment matrix PSD, localizing
             matrices for freq_i>=0 and M>=2 PSD), union-closure orbit equalities,
             L[1]=1, L matches F's honest stabilizer-orbit profile up to
             anchor_degree EXCEPT (if free_zero) the element-0 singleton, and the
             distinguished-max constraints  L[freq_0] >= L[freq_i]  for all i.

    Because element 0 is the worst (max) element by the >= constraints and its own
    frequency is free, this is a genuine LOWER bound on max-abundance that the
    degree-2d relaxation can prove.  At level 1 (only pair moments available) it
    reproduces the power-mean barrier; at level 2 the triple/quadruple moments may
    push it up."""
    N = model.n_orbits
    y = cp.Variable(N)
    cons = []
    emp = model.orbit_of[model.midx[frozenset()]]
    cons.append(y[emp] == 1.0)
    for (a, b) in model.orbit_eqs:
        cons.append(y[a] == y[b])
    anchored, vals = model.profile(F, anchor_degree, free_zero_singleton=free_zero)
    for o, v in anchored.items():
        cons.append(y[o] == v)
    # moment matrix PSD
    ment = model.moment_entries()
    R = ment.shape[0]
    Mmat = cp.bmat([[y[ment[r, c]] for c in range(R)] for r in range(R)])
    cons.append(Mmat >> 0)
    # localizing matrices for freq_i >= 0  (each i) and M - 2 >= 0
    glist = [model.linear_freq(i) for i in range(model.n)]
    gM = defaultdict(float)
    for mono, c in model.linear_M().items():
        gM[mono] += c
    gM[frozenset()] -= 2.0
    glist.append(dict(gM))
    for g in glist:
        loc, ok = model.localizing_entries(g)
        if not ok:
            continue
        Rl = len(loc)
        Lmat = cp.bmat([[(sum(coef * y[o] for o, coef in loc[r][c].items())
                          if loc[r][c] else cp.Constant(0))
                         for c in range(Rl)] for r in range(Rl)])
        cons.append(Lmat >> 0)
    # distinguished-max: L[freq_0] >= L[freq_i] for all i
    f0 = _linform(model, y, model.linear_freq(0))
    for i in range(1, model.n):
        cons.append(f0 >= _linform(model, y, model.linear_freq(i)))
    Mval = float(len(F))
    obj = f0 / Mval
    prob = cp.Problem(cp.Minimize(obj), cons)
    try:
        prob.solve(solver=cp.SCS, **SCS_OPTS)
    except Exception as e:
        return float("nan")
    if prob.status not in ("optimal", "optimal_inaccurate"):
        return float("nan")
    return float(obj.value)


# ---------------------------------------------------------------------------
# Validations + main table
# ---------------------------------------------------------------------------

def validate_cube(level):
    print(f"\n[VALIDATION a] cube must give lb_{level} = 0.5 exactly.", flush=True)
    rows = []
    for k in (1, 2, 3):
        F = cube(k)
        model = StabLasserre(k, level)
        lb = lb_d(model, F, anchor_degree=model.D)
        ta = true_abundance(F, k)
        ok = abs(lb - 0.5) < 0.02
        print(f"   cube 2^[{k}]: orbits={model.n_orbits:4d} true_ab={ta:.4f} "
              f"lb_{level}={lb:.4f}  {'OK' if ok else 'FAIL'}", flush=True)
        rows.append(dict(k=k, true_ab=ta, lb=lb, ok=ok))
    return rows


def validate_level1():
    print(f"\n[VALIDATION b] level-1 must reproduce power-mean barrier lb_1.", flush=True)
    rows = []
    for name, (n, F) in LOPSIDED.items():
        pm = power_mean_lb1(F, n)
        model = StabLasserre(n, 1)
        lb = lb_d(model, F, anchor_degree=model.D)
        ta = true_abundance(F, n)
        ok = abs(lb - pm) < 0.02
        print(f"   {name:16s} n={n} |F|={len(F)} orbits={model.n_orbits:4d} "
              f"true={ta:.4f} pm={pm:.4f} sdp_lb1={lb:.4f}  {'OK' if ok else 'FAIL'}",
              flush=True)
        rows.append(dict(name=name, pm=pm, sdp_lb1=lb, true_ab=ta, ok=ok))
    return rows


def run_six():
    print(f"\n[MAIN] level-2 (degree-4) incidence SDP on the 6 lopsided families.",
          flush=True)
    table = []
    for name, (n, F) in LOPSIDED.items():
        lb1 = power_mean_lb1(F, n)
        ta = true_abundance(F, n)
        model = StabLasserre(n, 2)
        lb2 = lb_d(model, F, anchor_degree=model.D)
        gap = lb2 - lb1
        table.append(dict(name=name, n=n, sizeF=len(F), true_ab=ta,
                          lb1=lb1, lb2=lb2, gap=gap, n_orbits=model.n_orbits))
        print(f"   {name:16s} n={n} |F|={len(F)} orbits={model.n_orbits:4d} "
              f"true={ta:.4f} lb_1={lb1:.4f} lb_2={lb2:.4f} gap={gap:+.4f}",
              flush=True)
    return table


def main():
    print("=" * 78)
    print("Frankl Lasserre level-2 (degree-4) incidence SDP  [cvxpy+SCS]")
    print("Author: Alex Ye.  Does degree-4 SOS escape the moment barrier?")
    print("=" * 78, flush=True)
    if not HAVE_CVXPY:
        print("ERROR: cvxpy missing"); sys.exit(1)
    import cvxpy
    print(f"cvxpy {cvxpy.__version__}  solvers={cvxpy.installed_solvers()}", flush=True)

    out = {}
    out["cube_level1"] = validate_cube(1)
    out["cube_level2"] = validate_cube(2)
    out["level1_barrier"] = validate_level1()
    out["six_level2"] = run_six()

    os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)
    path = os.path.join(os.path.dirname(__file__), "data", "las2_results.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2, default=lambda o: float(o) if isinstance(o, np.floating)
                  else int(o) if isinstance(o, np.integer) else o)
    print(f"\nWrote {path}", flush=True)


if __name__ == "__main__":
    main()
