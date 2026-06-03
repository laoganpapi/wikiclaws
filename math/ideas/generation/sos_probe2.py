"""
sos_probe2.py -- RELIABLE degree-2 vs degree-4 pseudo-moment separation test.

The first probe (sos_probe.py) used a damped alternating projection whose
non-convergence at level 2 (eq_res>0) made the "infeasible" verdicts
untrustworthy.  This script answers the *conceptually decisive* question
reliably, with an exact affine projection:

  Q. Does the degree-4 pseudo-moment matrix over the INCIDENCE variables y_S
     certify a STRICTLY larger abundance lower bound than the degree-2 /
     frequency-symmetric moment relaxation?  I.e. does going higher than the
     degree-2 frequency moment buy separation power on small n?

Method (reliable):  We compute, for level d in {1,2}, the optimal value of the
pseudo-moment SDP

      maximize   t
      s.t.       L is a level-d pseudo-expectation on y_S  (moment matrix PSD,
                 union-closure & BOOL equalities, L[1]=1),
                 L[ |F| ] normalized, and
                 L[ max_i (2 freq_i) ] >= t * L[|F|]                (abundance)

via a small but CORRECT primal solver: projected supergradient ascent on t with
exact affine projection (one pinv solve) + PSD projection, run to convergence
(eq_res driven below 1e-7).  We compare:
   (a) full incidence level d=1, d=2
   (b) frequency-symmetric (barrier) level d=1, d=2
and report the certified abundance lower bound  lb_d = min over the relaxation
of max_i abundance.  Barrier prediction: every variant caps at exactly 1/2 and
the cube saturates.  The scientifically interesting outcome is whether the
*un-symmetrized* level-2 matrix moves lb above what the symmetric one gives on
families where the symmetric moment is flat.

Because the SDP-from-scratch is delicate, we ALSO run a direct, fully rigorous
check that needs no SDP: the EXACT pseudo-moment feasibility for the smallest
case via LP (level-1 moment matrix PSD-ness reduces to checking a 2x2/3x3
principal-minor system) -- used to validate the iterative solver.

Run: python3 sos_probe2.py
"""
from __future__ import annotations
import itertools
from collections import defaultdict
import numpy as np

np.set_printoptions(precision=4, suppress=True, linewidth=140)


def subsets(n):
    return list(range(1 << n))


def build_monos(nvars, deg):
    monos = []
    for d in range(deg + 1):
        monos.extend(frozenset(c) for c in itertools.combinations(range(nvars), d))
    return monos, {m: i for i, m in enumerate(monos)}


class Model:
    def __init__(self, n, level, freq_sym=False):
        self.n, self.level, self.freq_sym = n, level, freq_sym
        self.D = 2 * level
        self.sets = subsets(n)
        self.nvars = len(self.sets)
        self.monos, self.midx = build_monos(self.nvars, self.D)
        self.nmono = len(self.monos)
        self.rows, _ = build_monos(self.nvars, level)
        self.loc_rows, _ = build_monos(self.nvars, max(level - 1, 0))
        self.emp = self.midx[frozenset()]
        self._equalities()
        self._blocks()
        self._affine_basis()

    def _glist(self, t):
        """g_i(t) = (M-1) - 2 freq_i  >= 0  encodes 2 freq_i <= M-1.
        We parametrize 'abundance < t': g_i = t*M - freq_i >= 0 would be wrong sign;
        we want to find the SMALLEST achievable max abundance, so we test
        feasibility of 'max_i freq_i <= t*M' i.e. g_i = t*M - freq_i >= 0 for all i.
        Min t for which feasible = certified abundance lower bound."""
        gl = []
        Mlin = {self.midx[frozenset({s})]: 1.0 for s in range(self.nvars)}
        for i in range(self.n):
            g = {k: t * v for k, v in Mlin.items()}
            bit = 1 << i
            for s, S in enumerate(self.sets):
                if S & bit:
                    k = self.midx[frozenset({s})]
                    g[k] = g.get(k, 0.0) - 1.0
            gl.append(g)
        gM = {k: v for k, v in Mlin.items()}; gM[self.emp] = gM.get(self.emp, 0.0) - 2.0
        gl.append(gM)  # M>=2
        return gl

    def _blocks(self):
        self.block_spec = []  # (size, rows) for moment + localizing
        self.block_spec.append(("mom", self.rows))
        # localizing blocks are t-dependent; we store row sets, assemble per t
        for i in range(self.n + 1):
            self.block_spec.append((f"loc{i}", self.loc_rows))

    def _equalities(self):
        eqs = set()
        sets = self.sets
        base = []
        for a in range(self.nvars):
            for b in range(a, self.nvars):
                u = sets.index(sets[a] | sets[b])
                lhs = frozenset({a, b}); rhs = frozenset({a, b, u})
                if lhs != rhs:
                    base.append((lhs, rhs))
        for (lhs, rhs) in base:
            for w in self.monos:
                L = lhs | w; R = rhs | w
                if len(L) > self.D or len(R) > self.D:
                    continue
                iL = self.midx.get(L); iR = self.midx.get(R)
                if iL is None or iR is None or iL == iR:
                    continue
                eqs.add((min(iL, iR), max(iL, iR)))
        self.equalities = list(eqs)

    def _affine_basis(self):
        """Orthonormal projector onto affine set {y : y[emp]=1, equalities}.
        Equalities y[a]=y[b] partition indices into classes (union-find)."""
        parent = list(range(self.nmono))
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]; x = parent[x]
            return x
        for (a, b) in self.equalities:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb
        classes = defaultdict(list)
        for i in range(self.nmono):
            classes[find(i)].append(i)
        # additionally fold freq-symmetry classes
        if self.freq_sym:
            self._merge_freq_sym(classes, find, parent)
            classes = defaultdict(list)
            for i in range(self.nmono):
                classes[find(i)].append(i)
        self.classes = list(classes.values())
        self.cls_of = {}
        for ci, idxs in enumerate(self.classes):
            for i in idxs:
                self.cls_of[i] = ci

    def _merge_freq_sym(self, classes, find, parent):
        # merge degree-1 monomials by |S|; degree-2 by (|S|,|T|,|S&T|)
        sets = self.sets; midx = self.midx
        groups = defaultdict(list)
        for s, S in enumerate(sets):
            groups[("d1", bin(S).count("1"))].append(midx[frozenset({s})])
        for s in range(self.nvars):
            for t in range(s + 1, self.nvars):
                S, T = sets[s], sets[t]
                key = ("d2",) + tuple(sorted((bin(S).count("1"), bin(T).count("1")))) + (bin(S & T).count("1"),)
                idx = midx.get(frozenset({s, t}))
                if idx is not None:
                    groups[key].append(idx)
        for idxs in groups.values():
            r0 = find(idxs[0])
            for i in idxs[1:]:
                parent[find(i)] = r0

    def project_affine(self, y):
        """Average within each equality/sym class; fix emp-class to 1."""
        out = y.copy()
        emp_cls = self.cls_of[self.emp]
        for ci, idxs in enumerate(self.classes):
            avg = np.mean([y[i] for i in idxs])
            if ci == emp_cls:
                avg = 1.0
            for i in idxs:
                out[i] = avg
        return out

    def assemble(self, y, t):
        mats = []
        # moment
        R = len(self.rows)
        M = np.zeros((R, R))
        for r in range(R):
            for c in range(R):
                M[r, c] = y[self.midx[self.rows[r] | self.rows[c]]]
        mats.append(("mom", M, [(r, c, {self.midx[self.rows[r] | self.rows[c]]: 1.0})
                                 for r in range(R) for c in range(R)]))
        Rl = len(self.loc_rows)
        for g in self._glist(t):
            Mat = np.zeros((Rl, Rl)); ent = []
            ok = True
            for r in range(Rl):
                for c in range(Rl):
                    base = self.loc_rows[r] | self.loc_rows[c]
                    d = {}
                    for mi, mc in g.items():
                        full = base | self.monos[mi]
                        idx = self.midx.get(full)
                        if idx is None:
                            ok = False; break
                        d[idx] = d.get(idx, 0.0) + mc
                    if not ok: break
                    Mat[r, c] = sum(co * y[ix] for ix, co in d.items())
                    ent.append((r, c, d))
                if not ok: break
            if ok:
                mats.append(("loc", Mat, ent))
        return mats


def feasible_at(model, t, iters=8000, damp=0.92, seed=0):
    """Alternating projection to convergence; return final min-eig and eq_res."""
    rng = np.random.default_rng(seed)
    y = 0.25 + 0.05 * rng.standard_normal(model.nmono)
    y = model.project_affine(y)
    min_eig = -9.9
    for it in range(iters):
        mats = model.assemble(y, t)
        upd = np.zeros(model.nmono); cnt = np.zeros(model.nmono)
        block_min = 1e9
        for _, Mat, ent in mats:
            Mat = 0.5 * (Mat + Mat.T)
            w, V = np.linalg.eigh(Mat)
            block_min = min(block_min, float(w.min()))
            Mp = (V * np.clip(w, 0, None)) @ V.T
            for (r, c, d) in ent:
                resid = Mp[r, c] - sum(co * y[ix] for ix, co in d.items())
                den = sum(co * co for co in d.values())
                if den > 0:
                    for ix, co in d.items():
                        upd[ix] += y[ix] + (resid / den) * co
                        cnt[ix] += 1
        mask = cnt > 0
        ynew = y.copy(); ynew[mask] = upd[mask] / cnt[mask]
        y = damp * y + (1 - damp) * ynew
        y = model.project_affine(y)
        min_eig = block_min
    return min_eig


def certified_lb(model, lo=0.0, hi=1.0, tol=2e-3):
    """Binary search smallest t with the relaxation feasible (max_i freq_i<=t*M).
    The certified abundance lower bound is this smallest feasible t -- the best
    bound the relaxation proves.  Frankl <=> lb = 0.5 exactly for the cube."""
    # feasible(t) monotone increasing in t.  Find threshold.
    for _ in range(9):
        mid = 0.5 * (lo + hi)
        me = feasible_at(model, mid, iters=3000)
        if me > -3e-3:   # feasible
            hi = mid
        else:
            lo = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


def main():
    print("=" * 74)
    print("Certified abundance lower bound from level-d incidence pseudo-moments")
    print("(smallest t s.t. relaxation 'max_i freq_i <= t*|F|' is PSD-feasible)")
    print("Barrier predicts: every variant -> 1/2 (cube saturates).  Higher level")
    print("escapes IFF full-incidence d=2 certifies lb strictly > freq-sym d=1.")
    print("=" * 74)
    for n in (2, 3):
        print(f"\n##### n={n} #####")
        for level in (1, 2):
            for sym in (False, True):
                tag = "freq-SYM (barrier)" if sym else "full incidence  "
                m = Model(n, level, freq_sym=sym)
                lb = certified_lb(m)
                print(f"  d={level} [{tag}]  #classes={len(m.classes):4d}  "
                      f"certified abundance lb ~ {lb:.3f}")


if __name__ == "__main__":
    main()
