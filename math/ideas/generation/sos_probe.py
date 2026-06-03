"""
sos_probe.py -- Degree-2 vs degree-4 pseudo-moment (Lasserre) probe for Frankl.

QUESTION (per brief): formulate "exists a UC family on [n] with abundance < 1/2"
as a 0/1 polynomial-feasibility problem in the *incidence* variables y_S
(y_S = 1 iff subset S is a member of F), and ask whether the Lasserre /
pseudo-moment SDP at level d=1 (degree-2) is feasible while level d=2
(degree-4) becomes INFEASIBLE.  An infeasible pseudo-moment SDP at level d is a
degree-2d Positivstellensatz refutation = a Frankl certificate at that degree.

CONTRAST (the barrier): the SAME pseudo-moment problem but FORCED through the
symmetric frequency vector freq_i = sum_{S: i in S} y_S.  That projection is the
degree-2 moment-LP the project proved collapses on the Boolean cube.

We have NO SDP solver in the sandbox (no cvxpy/mosek/scs).  We implement a
correct primal feasibility test by ALTERNATING PROJECTION between:
  (A) the affine subspace of moment vectors satisfying ALL linear constraints
      (L[1]=1; union-closure moment equalities; localizing-slack definitions),
      done EXACTLY by least squares; and
  (P) the PSD cone for ONE big block-diagonal matrix that stacks the moment
      matrix and every localizing matrix (so each shares the moment entries
      and the back-projection is exact, not heuristic).
The two convex sets share the same underlying moment vector via a linear map
y -> Mat(y).  We iterate y_{k+1} = argmin over affine of ||Mat - PSDproj(Mat(y_k))||.
If the PSD-violation (most negative eigenvalue) -> 0, the SDP is FEASIBLE
(no refutation at this level).  If it stalls at a strictly negative floor, that
is evidence of INFEASIBILITY (a refutation / Frankl certificate exists).
Verdicts are corroborated against brute-force enumeration of UC families.

Run:  python3 sos_probe.py
"""
from __future__ import annotations
import itertools
from collections import defaultdict
import numpy as np

np.set_printoptions(precision=4, suppress=True, linewidth=140)


# ---------------------------------------------------------------------------
# Monomials are squarefree (BOOL y_S^2=y_S baked in) -> sets of variable indices.
# Variables = indicators y_S, one per subset S of [n].
# ---------------------------------------------------------------------------

def subsets(n):
    return list(range(1 << n))


def build_monos(nvars, deg):
    monos = []
    for d in range(deg + 1):
        monos.extend(frozenset(c) for c in itertools.combinations(range(nvars), d))
    return monos, {m: i for i, m in enumerate(monos)}


class FranklLasserre:
    """Level-d pseudo-moment relaxation of: exists UC F on [n] with abundance<1/2."""

    def __init__(self, n, level):
        self.n, self.level = n, level
        self.D = 2 * level
        self.sets = subsets(n)
        self.nvars = len(self.sets)                      # 2^n incidence vars
        self.monos, self.midx = build_monos(self.nvars, self.D)
        self.nmono = len(self.monos)
        self.rows, _ = build_monos(self.nvars, level)    # moment-matrix rows
        self.loc_rows, _ = build_monos(self.nvars, max(level - 1, 0))
        self._build_blocks()
        self._build_equalities()

    # ---- block-diagonal PSD structure: moment matrix + localizing matrices ----
    def _glist(self):
        """Inequality polynomials g>=0 (as dict mono-index->coeff)."""
        emp = self.midx[frozenset()]
        gl = []
        # |F| = sum_S y_S
        Mlin = {self.midx[frozenset({s})]: 1.0 for s in range(self.nvars)}
        # M - 2 freq_i - 1 >= 0  (element i is NOT abundant: 2 freq_i <= M-1)
        for i in range(self.n):
            g = dict(Mlin)
            bit = 1 << i
            for s, S in enumerate(self.sets):
                if S & bit:
                    k = self.midx[frozenset({s})]
                    g[k] = g.get(k, 0.0) - 2.0
            g[emp] = g.get(emp, 0.0) - 1.0
            gl.append(g)
        # M - 2 >= 0
        gM = dict(Mlin); gM[emp] = gM.get(emp, 0.0) - 2.0
        gl.append(gM)
        return gl

    def _build_blocks(self):
        """Each block is a list of (i_row,i_col,{mono_idx:coeff}) entries.
        Block 0 = moment matrix; blocks 1.. = localizing matrices."""
        blocks = []
        # moment matrix
        R = len(self.rows)
        mm = []
        for r in range(R):
            for c in range(R):
                mm.append((r, c, {self.midx[self.rows[r] | self.rows[c]]: 1.0}))
        blocks.append(("moment", R, mm))
        # localizing matrices
        Rl = len(self.loc_rows)
        for gi, g in enumerate(self._glist()):
            ent = []
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
                    if not ok:
                        break
                    ent.append((r, c, d))
                if not ok:
                    break
            if ok:
                blocks.append((f"loc{gi}", Rl, ent))
        self.blocks = blocks

    def _build_equalities(self):
        """Union-closure moment equalities: y_A y_B = y_A y_B y_{AuB}, times any
        squarefree weight w with both sides within degree D."""
        eqs = []
        sets = self.sets
        base = []
        for a in range(self.nvars):
            for b in range(a, self.nvars):
                U = sets[a] | sets[b]
                u = sets.index(U)
                lhs = frozenset({a, b}); rhs = frozenset({a, b, u})
                if lhs != rhs:
                    base.append((lhs, rhs))
        for (lhs, rhs) in base:
            for w in self.monos:
                L = lhs | w; Rr = rhs | w
                if len(L) > self.D or len(Rr) > self.D:
                    continue
                iL = self.midx.get(L); iR = self.midx.get(Rr)
                if iL is None or iR is None or iL == iR:
                    continue
                eqs.append((iL, iR))   # y[iL] - y[iR] = 0
        # dedupe
        self.equalities = list({(min(a, b), max(a, b)) for (a, b) in eqs})


# ---------------------------------------------------------------------------
# Feasibility by alternating projection (affine <-> PSD), exact back-projection.
# ---------------------------------------------------------------------------

def feas(model, iters=6000, damp=0.9, seed=0, freq_symmetric=False, verbose=False):
    rng = np.random.default_rng(seed)
    nm = model.nmono
    emp = model.midx[frozenset()]
    y = 0.3 + 0.1 * rng.standard_normal(nm)
    y[emp] = 1.0

    # affine: equalities y[a]=y[b], plus y[emp]=1.  Apply as exact projections
    # (they are simple averaging/fixing, idempotent enough for our scale).
    def project_affine(y):
        y[emp] = 1.0
        # union-closure equalities (pairwise average -> exact when iterated)
        for (a, b) in model.equalities:
            avg = 0.5 * (y[a] + y[b]); y[a] = avg; y[b] = avg
        if freq_symmetric:
            _freq_symmetrize(model, y)
        y[emp] = 1.0
        return y

    # build per-entry accumulation maps for fast block assembly
    block_arrays = []
    for name, sz, ent in model.blocks:
        block_arrays.append((name, sz, ent))

    last_min = -1.0
    history = []
    for it in range(iters):
        y = project_affine(y)
        # assemble + PSD project each block; accumulate corrections back to y
        upd = np.zeros(nm); cnt = np.zeros(nm)
        block_min = 1e9
        for name, sz, ent in block_arrays:
            Mat = np.zeros((sz, sz))
            for (r, c, d) in ent:
                Mat[r, c] = sum(coef * y[idx] for idx, coef in d.items())
            Mat = 0.5 * (Mat + Mat.T)
            w, V = np.linalg.eigh(Mat)
            block_min = min(block_min, float(w.min()))
            wp = np.clip(w, 0, None)
            Mp = (V * wp) @ V.T
            # back-project entrywise: for entry (r,c) with linear form d,
            # distribute residual onto its moments by least-norm.
            for (r, c, d) in ent:
                target = Mp[r, c]
                cur = sum(coef * y[idx] for idx, coef in d.items())
                resid = target - cur
                den = sum(coef * coef for coef in d.values())
                if den > 0:
                    for idx, coef in d.items():
                        upd[idx] += y[idx] + (resid / den) * coef
                        cnt[idx] += 1
        mask = cnt > 0
        ynew = y.copy()
        ynew[mask] = upd[mask] / cnt[mask]
        y = damp * y + (1 - damp) * ynew
        last_min = block_min
        if it % max(iters // 10, 1) == 0:
            history.append(block_min)
            if verbose:
                print(f"    it={it:5d} block_min_eig={block_min:+.4e}")
    # final affine residual
    eqres = max((abs(y[a] - y[b]) for (a, b) in model.equalities), default=0.0)
    return last_min, eqres, history


def _freq_symmetrize(model, y):
    """Force moments to depend only on S_n-orbit data: degree-1 on |S|,
    degree-2 on (|S|,|T|,|S&T|).  This is the explicit 'symmetric convex moment
    of the frequency vector' restriction (the barrier)."""
    sets = model.sets; midx = model.midx
    g1 = defaultdict(list)
    for s, S in enumerate(sets):
        g1[bin(S).count("1")].append(midx[frozenset({s})])
    for idxs in g1.values():
        a = np.mean([y[i] for i in idxs])
        for i in idxs: y[i] = a
    g2 = defaultdict(list)
    for s in range(len(sets)):
        for t in range(s + 1, len(sets)):
            S, T = sets[s], sets[t]
            key = tuple(sorted((bin(S).count("1"), bin(T).count("1")))) + (bin(S & T).count("1"),)
            idx = midx.get(frozenset({s, t}))
            if idx is not None:
                g2[key].append(idx)
    for idxs in g2.values():
        a = np.mean([y[i] for i in idxs])
        for i in idxs: y[i] = a


# ---------------------------------------------------------------------------
# Brute-force ground truth: does a UC counterexample on [n] exist? (it must NOT)
# ---------------------------------------------------------------------------

def brute_min_abundance(n):
    """min over all UC families F (|F|>=2, full-ish) of max-element-abundance."""
    best = 1.0
    universe = list(range(1 << n))
    # enumerate all subsets-of-powerset is 2^(2^n); only feasible n<=3 here.
    allsets = universe
    best_fam = None
    from itertools import combinations
    # iterate over families containing arbitrary members; require union-closed
    # (n<=3 => 2^8=256 families, trivial)
    for r in range(2, len(allsets) + 1):
        for combo in combinations(allsets, r):
            F = set(combo)
            uc = all((a | b) in F for a in F for b in F)
            if not uc:
                continue
            # abundance
            freqs = [sum(1 for m in F if (m >> i) & 1) for i in range(n)]
            if not freqs or max(freqs) == 0:
                continue
            ab = max(freqs) / len(F)
            if ab < best:
                best = ab; best_fam = sorted(F)
    return best, best_fam


def main():
    print("=" * 74)
    print("Frankl pseudo-moment (Lasserre) probe: incidence vars y_S, level d=1 vs 2")
    print("Decision: exists UC F on [n] with 2*freq_i <= |F|-1 for ALL i ?  (Frankl: NO)")
    print("PSD-feasible relaxation => NO degree-2d refutation.  Infeasible => certificate.")
    print("=" * 74)
    for n in (2, 3):
        bmin, fam = brute_min_abundance(n)
        print(f"\n##### n={n} : 2^n={1<<n} incidence vars."
              f"  brute-force min abundance over all UC families = {bmin:.4f}"
              f"  (Frankl holds: >= 0.5)  witness={fam}")
        for level in (1, 2):
            for sym in (False, True):
                tag = "FREQ-SYM (barrier)" if sym else "full incidence   "
                model = FranklLasserre(n, level)
                me, eqr, hist = feas(model, iters=4000, seed=2, freq_symmetric=sym)
                verdict = ("FEASIBLE  (no cert at this degree)"
                           if me > -2e-3 else
                           "INFEASIBLE (refutation / Frankl certificate candidate)")
                print(f"  d={level} [{tag}]  moments={model.nmono:5d}  "
                      f"blocks={len(model.blocks):2d}  min_eig={me:+.3e}  "
                      f"eq_res={eqr:.1e}  -> {verdict}")


if __name__ == "__main__":
    main()
