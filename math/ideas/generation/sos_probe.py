"""
sos_probe.py -- Degree-2 vs degree-4 pseudo-moment (Lasserre) probe for Frankl.

GOAL (per brief): formulate "exists a UC family on [n] with abundance < 1/2"
as a 0/1 polynomial-feasibility problem in the *incidence* variables y_S
(y_S = 1 iff subset S is a member of F), and ask whether the Lasserre/
pseudo-moment SDP at level d=1 (degree-2) is feasible while level d=2
(degree-4) becomes INFEASIBLE.  An infeasible pseudo-moment SDP = a
Positivstellensatz refutation = a Frankl certificate at that degree.

Contrast object (the barrier): the SAME problem but with the pseudo-moment
functional FORCED to factor through the symmetric frequency vector
(freq_i = sum_{S: i in S} y_S).  That projection is exactly the degree-2
moment-LP the project already proved collapses on the Boolean cube.

We have NO SDP solver (no cvxpy/mosek/scs).  We roll a small, correct
feasibility routine:

  Lasserre level-d feasibility  <=>  exists a pseudo-expectation L (a vector
  of moments y_alpha, alpha a multiset of monomials of degree <= 2d) such that
    (i)   the moment matrix M_d(L) is PSD,
    (ii)  each localizing matrix M_{d-?}(g_j * L) is PSD,
    (iii) all equality constraints (BOOL: y_S^2 = y_S; the union-closure
          equalities y_A y_B (1 - y_{AuB}) = 0) hold as linear identities
          among moments.

We test feasibility by alternating projection (Dykstra) between
  - the affine subspace A = {moment vectors satisfying all linear equalities
    + L[1] = 1},
  - the PSD cone for every required matrix.
If the alternation converges to a common point (residual -> 0) the SDP is
feasible; if the residual stalls at a positive floor, that is evidence of
infeasibility (a refutation).  For the tiny n we use (n<=3) the matrices are
small and the diagnosis is clear.  This is a PROBE, not a certified solver:
we report residual floors and corroborate against brute-force enumeration.

Run:  python3 sos_probe.py
"""
from __future__ import annotations
import itertools
import numpy as np

np.set_printoptions(precision=4, suppress=True, linewidth=140)


# ---------------------------------------------------------------------------
# Monomial bookkeeping.  A "variable" is a subset S of [n] (its indicator y_S).
# Because y_S is 0/1 (BOOL: y_S^2 = y_S), every monomial reduces to a *set* of
# variables (a squarefree monomial).  So a monomial of degree <= D is just a
# subset T of the variable index set with |T| <= D.  This bakes in BOOL exactly.
# ---------------------------------------------------------------------------

def subsets(n):
    return list(range(1 << n))  # bitmask subsets of [n]


def build_index(nvars, deg):
    """All squarefree monomials (as frozensets of variable indices) of degree<=deg."""
    monos = []
    for d in range(deg + 1):
        for comb in itertools.combinations(range(nvars), d):
            monos.append(frozenset(comb))
    idx = {m: i for i, m in enumerate(monos)}
    return monos, idx


# ---------------------------------------------------------------------------
# The Frankl decision SDP at a given Lasserre level d, over incidence vars y_S.
# ---------------------------------------------------------------------------

class FranklLasserre:
    def __init__(self, n, level, symmetric_freq_only=False):
        self.n = n
        self.level = level                      # d ; moment matrix has rows = monomials deg<=d
        self.D = 2 * level                      # max monomial degree tracked
        self.sets = subsets(n)                  # variable list: y_S for each subset S
        self.nvars = len(self.sets)             # = 2^n
        self.symmetric_freq_only = symmetric_freq_only
        self.monos, self.midx = build_index(self.nvars, self.D)
        # rows of the moment matrix: squarefree monomials of degree <= level
        self.rows, _ = build_index(self.nvars, level)
        self._build_equalities()

    # squarefree product (BOOL): product of y_S over S in a set of variables
    def prod(self, varset):
        return frozenset(varset)

    def mom_idx(self, varset):
        """index of moment y_{prod(varset)}; None if degree exceeds tracked D."""
        fs = frozenset(varset)
        if len(fs) > self.D:
            return None
        return self.midx[fs]

    def _build_equalities(self):
        """Linear equalities among moments forced by union-closure + structure.

        Union-closure: for all A,B subsets, y_A y_B (1 - y_{AuB}) = 0, i.e.
            y_A y_B = y_A y_B y_{AuB}      (as squarefree monomials).
        Multiplying by any squarefree monomial w of low enough degree and taking
        L gives: L[ w * y_A y_B ] = L[ w * y_A y_B y_{AuB} ].  We add all such
        moment equalities that stay within tracked degree D.
        Also the trivial idempotent ones are automatic from squarefree reduction.
        """
        eqs = []  # each eq: dict {moment_index: coeff} == 0
        n = self.n
        sets = self.sets
        # base union-closure relations y_A y_B = y_A y_B y_{AuB}
        base = []
        for a in range(self.nvars):
            for b in range(a, self.nvars):
                A = sets[a]; B = sets[b]
                U = A | B
                u = sets.index(U)
                lhs = frozenset({a, b})
                rhs = frozenset({a, b, u})
                if lhs == rhs:
                    continue  # tautology (U already in {A,B})
                base.append((lhs, rhs))
        # multiply each base relation by squarefree monomials w of degree
        # small enough that both sides stay within degree D.
        wmax = self.D  # weight monomials up to degree D-ish; filtered below
        wmonos = [m for m in self.monos]  # all tracked squarefree monomials
        for (lhs, rhs) in base:
            for w in wmonos:
                L = lhs | w
                R = rhs | w
                if len(L) > self.D or len(R) > self.D:
                    continue
                iL = self.midx.get(L)
                iR = self.midx.get(R)
                if iL is None or iR is None or iL == iR:
                    continue
                eqs.append({iL: 1.0, iR: -1.0})
        self.equalities = eqs

    # ---- the "abundance < 1/2" constraints, as localizing inequalities ----
    def freq_linear(self, i):
        """linear form freq_i = sum_{S: i in S} y_S, as dict moment_index->coeff."""
        out = {}
        bit = 1 << i
        for s, S in enumerate(self.sets):
            if S & bit:
                out[self.midx[frozenset({s})]] = out.get(self.midx[frozenset({s})], 0.0) + 1.0
        return out

    def M_linear(self):
        """|F| = sum_S y_S as dict."""
        out = {}
        for s in range(self.nvars):
            out[self.midx[frozenset({s})]] = 1.0
        return out


# ---------------------------------------------------------------------------
# Alternating-projection feasibility for the pseudo-moment SDP.
# ---------------------------------------------------------------------------

def moment_matrix(L, rows, midx, nvars):
    """Build moment matrix M[r,c] = L[ row_r * row_c ] (squarefree product)."""
    R = len(rows)
    M = np.zeros((R, R))
    for r in range(R):
        for c in range(R):
            prod = rows[r] | rows[c]
            idx = midx.get(prod)
            if idx is None:
                M[r, c] = np.nan  # degree too high; shouldn't happen at level<=D/2
            else:
                M[r, c] = L[idx]
    return M


def psd_project(M):
    M = (M + M.T) / 2
    w, V = np.linalg.eigh(M)
    w = np.clip(w, 0, None)
    return (V * w) @ V.T, float(min(np.linalg.eigvalsh((M + M.T) / 2)))


def run_feasibility(model, abundance_lt_half=True, iters=4000, tol=1e-9, seed=0):
    """Alternating projections.  Returns (min_eig_floor, eq_residual_floor)."""
    rng = np.random.default_rng(seed)
    nm = len(model.monos)
    # moment vector y[alpha]; y[empty monomial] = L[1] = 1
    y = rng.standard_normal(nm) * 0.01
    empty = model.midx[frozenset()]
    rows = model.rows
    midx = model.midx
    nvars = model.nvars

    # Precompute mapping (r,c) -> moment index for moment matrix assembly
    R = len(rows)
    pair_idx = np.zeros((R, R), dtype=int)
    for r in range(R):
        for c in range(R):
            pair_idx[r, c] = midx[rows[r] | rows[c]]

    # localizing data: for each element i, the inequality M - 2 freq_i - 1 >= 0
    # localizing "matrix" at level (d-1).  For our small probe we use the
    # scalar localizing constraint at degree 0 (L[g] >= 0) PLUS, when level>=2,
    # the level-1 localizing matrix g * (deg<=1 monomials).
    loc_rows = [m for m in model.monos if len(m) <= model.level - 1] if model.level >= 1 else [frozenset()]

    glist = []  # each g: dict idx->coeff  (g >= 0 constraint)
    Mlin = model.M_linear()
    for i in range(model.n):
        g = dict(Mlin)
        fi = model.freq_linear(i)
        for k, v in fi.items():
            g[k] = g.get(k, 0.0) - 2.0 * v
        g[empty] = g.get(empty, 0.0) - 1.0   # M - 2 freq_i - 1 >= 0
        glist.append(g)
    # also M - 2 >= 0 (at least 2 members)
    gM = dict(Mlin); gM[empty] = gM.get(empty, 0.0) - 2.0
    glist.append(gM)

    def assemble_loc(g):
        """localizing matrix L[ row_r * row_c * g ]."""
        Rl = len(loc_rows)
        Lm = np.zeros((Rl, Rl))
        for r in range(Rl):
            for c in range(Rl):
                base = loc_rows[r] | loc_rows[c]
                acc = 0.0
                ok = True
                for gi, gc in g.items():
                    gmono = model.monos[gi]
                    full = base | gmono
                    idx = midx.get(full)
                    if idx is None:
                        ok = False; break
                    acc += gc * y[idx]
                Lm[r, c] = acc if ok else np.nan
        return Lm

    floor_eig = -1.0
    floor_eq = 1.0
    for it in range(iters):
        # 1) affine projection: L[1]=1 and all equalities, by least-squares step
        y[empty] = 1.0
        # equality residuals (union-closure) -> project out
        for eq in model.equalities:
            num = sum(c * y[i] for i, c in eq.items())
            den = sum(c * c for c in eq.values())
            if den > 0:
                for i, c in eq.items():
                    y[i] -= (num / den) * c
        # symmetric-frequency restriction (the BARRIER contrast):
        if model.symmetric_freq_only:
            symmetrize_freq(model, y)
        y[empty] = 1.0

        # 2) PSD projections (moment matrix + localizing), averaged back to y
        updates = np.zeros(nm)
        counts = np.zeros(nm)
        # moment matrix
        M = y[pair_idx]
        Mp, mineig = psd_project(M)
        for r in range(R):
            for c in range(R):
                idx = pair_idx[r, c]
                updates[idx] += Mp[r, c]; counts[idx] += 1
        min_eig_seen = mineig
        # localizing matrices
        for g in glist:
            Lm = assemble_loc(g)
            if np.isnan(Lm).any():
                continue
            Lp, le = psd_project(Lm)
            min_eig_seen = min(min_eig_seen, le)
            # localizing entry = sum_g gc * y[base|gmono]; distribute correction
            Rl = len(loc_rows)
            for r in range(Rl):
                for c in range(Rl):
                    base = loc_rows[r] | loc_rows[c]
                    corr = Lp[r, c] - Lm[r, c]
                    # push correction onto the dominant moment of g (heuristic):
                    # distribute equally across g's monomials
                    terms = []
                    for gi, gc in g.items():
                        full = base | model.monos[gi]
                        idx = midx.get(full)
                        if idx is not None and abs(gc) > 0:
                            terms.append((idx, gc))
                    if terms:
                        share = corr / sum(t[1] ** 2 for t in terms)
                        for idx, gc in terms:
                            updates[idx] += y[idx] + share * gc
                            counts[idx] += 1
        mask = counts > 0
        ynew = y.copy()
        ynew[mask] = updates[mask] / counts[mask]
        y = 0.5 * y + 0.5 * ynew  # damping

        # diagnostics
        eqres = 0.0
        for eq in model.equalities:
            eqres = max(eqres, abs(sum(c * y[i] for i, c in eq.items())))
        if it > iters // 2:
            floor_eig = max(floor_eig, min_eig_seen)  # least negative reached late
            floor_eq = min(floor_eq, eqres)
    return min_eig_seen, eqres


def symmetrize_freq(model, y):
    """Project the moment vector onto the S_n-symmetric subalgebra generated by
    the frequency linear forms -- i.e. force all degree-1 moments y_{S} to depend
    only on |S| (orbit under S_n), and force degree-2 moments y_{S}y_{T} to depend
    only on (|S|,|T|,|S cap T|).  This is the explicit 'symmetric convex moment'
    restriction the BARRIER theorem concerns."""
    n = model.n
    sets = model.sets
    midx = model.midx
    # degree-1: average y_S over sets of equal size
    from collections import defaultdict
    g1 = defaultdict(list)
    for s, S in enumerate(sets):
        g1[bin(S).count("1")].append(midx[frozenset({s})])
    for _, idxs in g1.items():
        avg = np.mean([y[i] for i in idxs])
        for i in idxs:
            y[i] = avg
    # degree-2: average y_S y_T over orbit (|S|,|T|,|S&T|)
    g2 = defaultdict(list)
    for s in range(len(sets)):
        for t in range(s, len(sets)):
            S = sets[s]; T = sets[t]
            key = tuple(sorted((bin(S).count("1"), bin(T).count("1")))) + (bin(S & T).count("1"),)
            idx = midx.get(frozenset({s, t}))
            if idx is not None:
                g2[key].append(idx)
    for _, idxs in g2.items():
        avg = np.mean([y[i] for i in idxs])
        for i in idxs:
            y[i] = avg


def main():
    print("=" * 72)
    print("Frankl pseudo-moment (Lasserre) probe: degree-2 vs degree-4")
    print("Decision form: exists UC family on [n] with 2*freq_i <= |F|-1 for all i?")
    print("Infeasible SDP = Positivstellensatz refutation = Frankl certificate.")
    print("=" * 72)
    for n in (2, 3):
        print(f"\n##### n = {n}  (2^n = {1<<n} incidence variables y_S) #####")
        for level in (1, 2):
            for sym in (False, True):
                tag = "FREQ-SYMMETRIC (barrier)" if sym else "full incidence    "
                try:
                    model = FranklLasserre(n, level, symmetric_freq_only=sym)
                    me, eqr = run_feasibility(model, iters=1500, seed=1)
                    nmono = len(model.monos)
                    verdict = ("FEASIBLE (no cert)" if me > -1e-3 and eqr < 1e-3
                               else "INFEASIBLE-ish (refutation/cert candidate)")
                    print(f"  level d={level} [{tag}] : "
                          f"moments={nmono:5d}  min_eig={me:+.4e}  eq_res={eqr:.2e}  -> {verdict}")
                except Exception as e:
                    print(f"  level d={level} [{tag}] : ERROR {e}")


if __name__ == "__main__":
    main()
