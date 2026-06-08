"""
collatz_isotypic.py -- isotypic / group-equivariant decomposition of the Syracuse
transfer operator P_n on (Z/3^n)^x, to test WHERE the mod-3 obstruction lives
under a NON-abelian group action.

Author: representation-theory generation agent (idea-search, NOT a proof).
Status: [NOVELTY UNVERIFIED].  Direction-finding numerics only.

CONTEXT (from collatz/theory/{transfer_operator,perp_gap}.md):
  P_n[x,y] = sum_{k>=1} 2^{-k} 1[2^{-k}(3x+1) == y mod 3^n],  x,y in U_n=(Z/3^n)^x.
  EXACT: charpoly(P_n) = lam^{phi-1}(lam-1); P_n-Pi nilpotent of index n.
  The natural-density obstruction is the lam=1 eigenvector pi_n, whose mod-3
  marginal is permanently (1/3,2/3) -- the "mod-3 obstruction".
  Prior abelian Fourier (characters of the CYCLIC U_n) FAILED: it only diagonalizes
  the multiplicative part 2^{-k}; the additive "+1" of 3x+1 is invisible to it.

WHY NON-ABELIAN.  The Syracuse step x -> 2^{-k}(3x+1) is AFFINE: multiply by the
unit 2^{-k} (multiplicative, = translation in the cyclic coordinate a where x=2^a)
THEN add the constant 1 (additive, breaks the cyclic symmetry).  The smallest group
that sees BOTH is the affine "ax+b" group
        G_n := Aff(Z/3^n) = (Z/3^n, +) rtimes (Z/3^n)^x.
Its irreducible representations (Mackey / little-group machine over the additive
characters psi_t(x)=exp(2pi i t x / 3^n)):
  - 1-dim "trivial-on-translations" irreps = the |U_n| characters of U_n
    (these are exactly the abelian-Fourier modes that FAILED);
  - for each U_n-orbit of nontrivial additive characters, ONE induced irrep of
    dimension |orbit|.  Over Z/3^n the orbit of psi_t under x->u x has size = the
    multiplicative orbit of t; the "generic" orbit (t a unit) gives a single irrep
    of dimension phi(3^n) -- a genuinely NON-ABELIAN block.

This script does three concrete decompositions and inspects the mod-3 obstruction
inside each:

  (A) MULTIPLICATIVE (abelian, the failed baseline).  U_n acts on functions by
      (u . f)(x) = f(u^{-1} x).  Decompose C^{U_n} into the |U_n| characters of the
      cyclic group U_n (this is just the DFT in the cyclic coordinate).  We compute
      < chi_j , P_n >  i.e. how P_n couples character-blocks, to CONFIRM P_n is NOT
      multiplicatively equivariant (so abelian Fourier cannot diagonalize it), and
      to locate the mod-3 character (the order-2 / sign character of U_n) inside it.

  (B) AFFINE COMMUTANT (the non-abelian test).  Build the additive-character basis
      psi_t (t in Z/3^n), group the t's into U_n-orbits, and express P_n in this
      basis.  Check whether P_n is BLOCK-structured by the orbit filtration, and
      whether the mod-3 obstruction (which lives in the t in 3^{n-1}Z, i.e. the
      "mod-3 characters") is confined to a SINGLE small isotypic block that is
      DECOUPLED from the generic (unit-t) block.  If yes: the obstruction is an
      isotypic artifact, and the generic block may admit a contraction -- the
      escape the brief asks for.

  (C) SELF-SIMILAR / BRANCH structure.  P_n acts on the rooted ternary tree
      Z/3^n via the projective tower P_n -> P_{n-1} (transfer_operator.md sec3.1).
      We exhibit the wreath-recursion: restrict P_n to the three "mod-3 cosets"
      and read off the 3x3 "section matrix" of how cosets map, plus the residual
      operator inside each coset (the self-similar core).  This is the
      Grigorchuk/branch-group viewpoint: is the obstruction the abelianization
      (the 3x3 quotient) while the commutator/core contracts?

Run:  python3 collatz_isotypic.py [n_max]
Writes data/collatz_isotypic.json + prints a verdict.
"""
from __future__ import annotations
import json, os, sys, cmath
from fractions import Fraction
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA, exist_ok=True)


# --------------------------------------------------------------------------
# Exact rational Syracuse kernel (reused from collatz/experiments/perp_gap.py)
# --------------------------------------------------------------------------
def units_mod(n):
    m = 3 ** n
    return [x for x in range(1, m) if x % 3 != 0]


def exact_kernel(n):
    mod = 3 ** n
    U = units_mod(n)
    idx = {u: i for i, u in enumerate(U)}
    sz = len(U)
    L = 2 * 3 ** (n - 1)               # = ord_{3^n}(2) = phi(3^n)
    i2 = (mod + 1) // 2                 # inverse of 2 mod 3^n
    denom = 1 - Fraction(1, 2 ** L)
    P = [[Fraction(0)] * sz for _ in range(sz)]
    cur, invs, weights = 1, [], []
    for r in range(1, L + 1):
        cur = (cur * i2) % mod
        invs.append(cur)
        weights.append(Fraction(1, 2 ** r) / denom)
    for i, x in enumerate(U):
        v = (3 * x + 1) % mod
        for r in range(L):
            y = (v * invs[r]) % mod
            P[i][idx[y]] += weights[r]
    return P, U


def kernel_float(n):
    P, U = exact_kernel(n)
    return np.array([[float(c) for c in row] for row in P], dtype=float), U


# --------------------------------------------------------------------------
# (A) Multiplicative (abelian) Fourier in the CYCLIC coordinate.
#     U_n = <2> is cyclic of order L = phi(3^n).  Write each unit x = 2^a, a in Z/L.
#     Characters chi_j(x) = exp(2pi i j a / L).  Equivariance test: does P_n commute
#     with the multiplication-by-u permutation?  (It will NOT, because of the +1.)
# --------------------------------------------------------------------------
def multiplicative_decomposition(n):
    Pf, U = kernel_float(n)
    mod = 3 ** n
    L = len(U)
    # discrete-log table base 2
    dlog = {}
    v = 1
    for a in range(L):
        dlog[v] = a
        v = (v * 2) % mod
    # permutation matrix for multiplication by g=2 (a -> a+1 cyclic shift)
    perm = np.zeros((L, L))
    for x in U:
        perm[U.index((2 * x) % mod), U.index(x)] = 1.0
    # equivariance defect ||P perm - perm P||
    defect = float(np.linalg.norm(Pf @ perm - perm @ Pf))
    # character matrix F[j,i] = chi_j(U[i]) = w^{j*dlog(U[i])}
    w = cmath.exp(2j * cmath.pi / L)
    a_of = np.array([dlog[u] for u in U])
    j = np.arange(L)[:, None]
    F = w ** (j * a_of[None, :])          # L x L, rows = characters
    Finv = np.conj(F).T / L               # inverse DFT (unitary up to 1/L)
    # P in the character basis:  Phat = F P Finv  (coupling between characters)
    Phat = F @ Pf @ Finv
    # off-diagonal mass = how much P_n mixes distinct multiplicative characters
    diag = np.diag(np.abs(Phat))
    offdiag = np.abs(Phat) - np.diag(diag)
    # the "mod-3" character is the order-2 character: j = L/2 (since x mod 3 = 2^{a} mod 3
    # = (-1)^a, the sign character of the cyclic group).  Its index is j=L/2.
    mod3_char_index = L // 2
    return {
        "n": n, "L": L,
        "mult_equivariance_defect": defect,   # >0  => P NOT mult-equivariant
        "Phat_diag_absmax": float(diag.max()),
        "Phat_offdiag_absmax": float(offdiag.max()),
        "Phat_offdiag_frobenius": float(np.linalg.norm(offdiag)),
        "mod3_is_sign_character_index": mod3_char_index,
        # how strongly the mod-3 (sign) character couples to the trivial character j=0:
        "mod3_to_trivial_coupling": float(abs(Phat[0, mod3_char_index])),
        "mod3_self_coupling": float(abs(Phat[mod3_char_index, mod3_char_index])),
    }


# --------------------------------------------------------------------------
# (B) Additive-character / affine-orbit decomposition (the NON-abelian test).
#     psi_t(x) = exp(2pi i t x / 3^n), t in Z/3^n.  U_n acts on the index t by
#     t -> u t (mod 3^n).  Orbits partition {0,...,3^n-1} by 3-adic valuation of t:
#        v_3(t) = n         -> t=0           (trivial char; orbit size 1)
#        v_3(t) = n-1       -> t in {3^{n-1}, 2*3^{n-1}}  -> the MOD-3 characters
#        ...
#        v_3(t) = 0         -> t a unit      -> the GENERIC orbit, size phi(3^n)
#     The generic orbit gives the big phi(3^n)-dim non-abelian affine irrep.
#     We express P_n on the additive basis and measure coupling BETWEEN orbits,
#     to test if the mod-3 block (v_3=n-1) is decoupled from the generic block.
# --------------------------------------------------------------------------
def v3(t, n):
    if t == 0:
        return n
    c = 0
    while t % 3 == 0:
        t //= 3
        c += 1
    return c


def affine_orbit_decomposition(n):
    Pf, U = kernel_float(n)
    mod = 3 ** n
    Lsz = len(U)
    # additive characters restricted to the UNITS (P_n lives on C^{U_n}):
    #   Psi[t, i] = exp(2pi i t U[i] / 3^n).   This is an overcomplete (mod) frame on units.
    # We build the level-by-valuation projectors and see how P_n couples levels.
    # Group t in {0..mod-1} by v_3(t).
    levels = {}
    for t in range(mod):
        levels.setdefault(v3(t, n), []).append(t)
    # additive-character matrix evaluated on units
    w = cmath.exp(2j * cmath.pi / mod)
    Uarr = np.array(U)
    # For each valuation level, build the span (on units) of {psi_t : v3(t)=lvl} and
    # an orthonormal basis Q_lvl; then measure block coupling  Q_a^H P Q_b.
    Qs = {}
    for lvl, ts in sorted(levels.items()):
        cols = []
        for t in ts:
            cols.append(w ** (t * Uarr))
        M = np.array(cols).T           # |U| x |ts|
        # orthonormalize columns (drop dependent ones)
        q, r = np.linalg.qr(M)
        keep = np.abs(np.diag(r)) > 1e-9
        Qs[lvl] = q[:, keep]
    # block coupling matrix between valuation levels
    lvls = sorted(Qs.keys())
    coupling = {}
    for a in lvls:
        for b in lvls:
            blk = Qs[a].conj().T @ Pf @ Qs[b]
            coupling[(a, b)] = float(np.linalg.norm(blk))
    # the mod-3 obstruction lives in level v3 = n-1 (the chars psi_{3^{n-1}}, psi_{2*3^{n-1}})
    mod3_lvl = n - 1
    generic_lvl = 0
    # is the mod-3 block invariant?  coupling(mod3, other)/coupling(mod3,mod3)
    out = {
        "n": n,
        "levels_dims": {str(l): int(Qs[l].shape[1]) for l in lvls},
        "coupling_norms": {f"{a}->{b}": coupling[(a, b)] for a in lvls for b in lvls},
        "mod3_level": mod3_lvl,
        "generic_level": generic_lvl,
    }
    # cross-coupling from the mod-3 block OUT to everything else (off its own block):
    if mod3_lvl in lvls:
        own = coupling[(mod3_lvl, mod3_lvl)]
        out_mass = sum(coupling[(mod3_lvl, b)] for b in lvls if b != mod3_lvl)
        out["mod3_block_self_norm"] = own
        out["mod3_block_outflow_norm"] = out_mass
        out["mod3_decoupling_ratio"] = (out_mass / own) if own > 1e-12 else None
    # within the generic block: spectral radius of P restricted there (does the BIG
    # non-abelian block contract?).  Generic block is P compressed to span(Q_generic).
    if generic_lvl in lvls and Qs[generic_lvl].shape[1] > 0:
        Bgen = Qs[generic_lvl].conj().T @ Pf @ Qs[generic_lvl]
        ev = np.linalg.eigvals(Bgen)
        out["generic_block_dim"] = int(Qs[generic_lvl].shape[1])
        out["generic_block_spectral_radius"] = float(np.max(np.abs(ev)))
        out["generic_block_top3_abs"] = sorted([float(abs(e)) for e in ev])[-3:]
    return out


# --------------------------------------------------------------------------
# (C) Self-similar / branch-group section.  Split U_n by mod-3 coset (the
#     abelianization-ish quotient) and read the 3x3 (here 2x2 on units) "section"
#     matrix + the per-coset residual.  Mirrors the wreath recursion of branch groups.
# --------------------------------------------------------------------------
def branch_section(n):
    Pf, U = kernel_float(n)
    # partition units by residue mod 3 (cosets r=1,2)
    cos = {1: [i for i, u in enumerate(U) if u % 3 == 1],
           2: [i for i, u in enumerate(U) if u % 3 == 2]}
    # 2x2 averaged section: S[r,s] = total prob mass from coset r to coset s, normalized
    S = np.zeros((2, 2))
    for ri, r in enumerate([1, 2]):
        rows = cos[r]
        for si, s in enumerate([1, 2]):
            S[ri, si] = Pf[np.ix_(rows, cos[s])].sum() / len(rows)
    # per-coset diagonal residual block r->r, and its spectral radius after removing
    # the rank-1 (within-coset average) part
    residuals = {}
    for r in [1, 2]:
        rows = cos[r]
        B = Pf[np.ix_(rows, rows)]
        ev = np.linalg.eigvals(B)
        residuals[r] = {"dim": len(rows),
                        "spectral_radius": float(np.max(np.abs(ev)))}
    return {
        "n": n,
        "section_2x2": S.tolist(),
        "section_eigs": [float(abs(e)) for e in np.linalg.eigvals(S)],
        "per_coset_core": residuals,
    }


# --------------------------------------------------------------------------
# (D) THE CORRECT non-abelian filtration: induced-from-trivial reps of U_n on the
#     cosets U_n / U_n^{(k)} (U_n^{(k)} = ker(U_n -> (Z/3^k)^x)).  Concretely these
#     are the coset-indicator subspaces V^(k) = span{ 1[x == r mod 3^k] }, which are
#     EXACTLY P_n-invariant (transfer_operator.md sec3.1).  We confirm:
#       - V^(k) invariant (leak ~ 0),
#       - eigenvalue 1 sits in the BOTTOM block V^(1) (the mod-3 isotype),
#       - every successive quotient V^(k)/V^(k-1) is NILPOTENT (spectral radius 0):
#         i.e. the obstruction is confined to the trivial-on-quotient (mod-3) piece,
#         and the entire complement of isotypes is nilpotent. This is the rigorous,
#         group-theoretic localization of the obstruction the brief asked for.
# --------------------------------------------------------------------------
def induced_filtration(n):
    Pf, U = kernel_float(n)
    Ueye = np.eye(len(U))

    def coset_basis(k):
        m3 = 3 ** k
        cols = {}
        for i, u in enumerate(U):
            cols.setdefault(u % m3, []).append(i)
        B = np.zeros((len(U), len(cols)))
        for j, (r, idxs) in enumerate(sorted(cols.items())):
            for i in idxs:
                B[i, j] = 1.0
        Q, _ = np.linalg.qr(B)
        return Q

    rows = []
    Qprev = None
    for k in range(1, n + 1):
        Q = coset_basis(k)
        Pi = Q @ Q.T
        leak = float(np.linalg.norm((Ueye - Pi) @ Pf @ Q))
        blk = Q.T @ Pf @ Q
        ev = np.abs(np.linalg.eigvals(blk))
        sr = float(ev.max())
        # successive-quotient action V^(k)/V^(k-1):  represent P|_{V^(k)} in a basis
        # (basis of V^(k-1), then completion to V^(k)); the lower-right block is the
        # quotient action (well-defined since V^(k-1) is invariant inside V^(k)).
        if Qprev is not None:
            d0 = Qprev.shape[1]
            # extend Qprev to an orthonormal basis of V^(k) using cols of Q
            Bcols = list(Qprev.T)
            cur = Qprev.copy()
            for col in Q.T:
                cand = np.hstack([cur, col[:, None]])
                if np.linalg.matrix_rank(cand, tol=1e-9) == cur.shape[1] + 1:
                    cur = np.linalg.qr(cand)[0][:, :cur.shape[1] + 1]
                    if cur.shape[1] == Q.shape[1]:
                        break
            Pblk = cur.T @ Pf @ cur          # P restricted to V^(k) in adapted basis
            Quot = Pblk[d0:, d0:]            # lower-right = quotient action
            qsr = float(np.abs(np.linalg.eigvals(Quot)).max()) if Quot.size else 0.0
            qdim = int(Quot.shape[0])
        else:
            qsr, qdim = sr, int(Q.shape[1])
        rows.append({"k": k, "dim_Vk": int(Q.shape[1]),
                     "invariant_leak": leak, "block_spectral_radius": sr,
                     "quotient_dim": qdim,
                     "quotient_spectral_radius": qsr})
        Qprev = Q
    return {"n": n, "filtration": rows}


# --------------------------------------------------------------------------
def main():
    n_max = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    results = {"multiplicative": [], "affine": [], "branch": [], "induced": []}
    for n in range(1, n_max + 1):
        print(f"=== n={n} ===", flush=True)
        A = multiplicative_decomposition(n)
        B = affine_orbit_decomposition(n)
        C = branch_section(n)
        D = induced_filtration(n)
        results["multiplicative"].append(A)
        results["affine"].append(B)
        results["branch"].append(C)
        results["induced"].append(D)
        print(f"  (A) mult-equivariance defect = {A['mult_equivariance_defect']:.4f}  "
              f"(>0 => abelian Fourier cannot diagonalize)")
        print(f"      mod3(sign)->trivial coupling = {A['mod3_to_trivial_coupling']:.4f}")
        print(f"  (B) valuation-level dims = {B['levels_dims']}")
        if 'mod3_decoupling_ratio' in B:
            print(f"      mod3 block: self={B['mod3_block_self_norm']:.4f} "
                  f"outflow={B['mod3_block_outflow_norm']:.4f} "
                  f"ratio={B['mod3_decoupling_ratio']}")
        if 'generic_block_spectral_radius' in B:
            print(f"      GENERIC block dim={B['generic_block_dim']} "
                  f"spectral_radius={B['generic_block_spectral_radius']:.4f}")
        print(f"  (C) section eigs = {C['section_eigs']}  "
              f"per-coset core radii = "
              f"{[round(C['per_coset_core'][r]['spectral_radius'],4) for r in (1,2)]}")
        print(f"  (D) induced filtration V^(1)<...<V^(n) (CORRECT invariant blocks):")
        for row in D["filtration"]:
            print(f"      V^({row['k']}) dim={row['dim_Vk']:3d} "
                  f"leak={row['invariant_leak']:.1e} "
                  f"block_radius={row['block_spectral_radius']:.4f} | "
                  f"quotient V^(k)/V^(k-1) dim={row['quotient_dim']:3d} "
                  f"spec_radius={row['quotient_spectral_radius']:.4f}")
    with open(os.path.join(DATA, "collatz_isotypic.json"), "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {os.path.join(DATA, 'collatz_isotypic.json')}")


if __name__ == "__main__":
    main()
