"""
vector_analysis.py — End-to-end numerical analysis of Attack Vectors 1 and 2.

⚠️  CAVEAT (read before trusting any number here): the per-family "certified
    constant" diagnostics below (ahs_certified_constant, v1_*, v2_*) are HEURISTIC
    proxies of the form `1 - numerator/budget`. They are useful for RELATIVE
    comparison and for locating worst-case families, and the AHS/V1 columns are
    meaningful because their budgets are honest. BUT the V2-λ proxy uses the
    family's TRUE H(A∩B) as if it were a provable budget, which it is NOT
    (H(A∩B) ≰ H(A) for union-closed F — see verify_ahs.py / theory/vector2).
    Consequently the V2-λ column can report a spurious "improvement" (e.g. 0.5);
    that is a budget-mismatch artifact, NOT a valid bound. The RIGOROUS object is
    the single-letter optimization in `single_letter.py`. See dead_ends.md.

For each union-closed family F (A,B iid uniform on F), we compute the *actual*
certifiable abundance constant that each proof strategy would yield IF its
single-letter inequality were sharp, by directly evaluating the family-level
quantities. This bypasses the single-letter optimization and tests whether the
strategy can possibly beat psi on the families that matter.

Strategies compared:
  AHS    : uses H(A∪B) <= H(A); lower bound (1/(1-psi)) Σ(1-p_i)H(A_i|A_<i).
  V1     : Vector 1 (Shearer/chain-rule recapture): adds the conditional
           mutual information Δ2 = H(A∪B) - Σ_i H(C_i|A_<i,B_<i) back.
  V2-join: Vector 2 (joint union+intersection): tracks (A∪B,A∩B), budget = H(A∪B,A∩B).
  V2-lam : Vector 2 (weighted): tracks H(A∪B)+λ H(A∩B), with the honest budget.

The "certifiable constant per family" is defined operationally below for each.

Author: Alex Ye (AI assistance disclosed separately).
"""
from __future__ import annotations
import math
from collections import defaultdict
import verify_ahs as V

h = V.h
PSI = V.psi_const()


def family_marginals_and_condH(F, n):
    """Return (p_i list, H(A_i|A_<i) list)."""
    Fl = list(F); m = len(Fl)
    ps = []; chs = []
    for i in range(n):
        bit = 1 << i
        ps.append(sum(1 for a in Fl if a & bit) / m)
        chs.append(V.H_Ai_given_prefix(Fl, i))
    return ps, chs


def ahs_certified_constant(F, n):
    """
    Largest c such that the AHS chain (using THIS family's exact internals) does
    not yet derive a contradiction:  H(A∪B) >= (1/(1-c)) Σ (1-p_i)H(A_i|A_<i)
    must FAIL to exceed H(A) for the proof to NOT conclude c. We instead report
    the constant the family 'permits': the proof concludes max p_i >= c whenever
        (1/(1-c)) Σ(1-p_i)H(A_i|A_<i) > H(A).
    But that uses the assumption max p_i < c. The clean per-family diagnostic:
    define c_AHS(F) = 1 - [Σ(1-p_i)H(A_i|A_<i)] / H(A∪B). Then the AHS inequality
    H(A∪B) >= (1/(1-psi))Σ(1-p_i)H(A_i|A_<i) is exactly c_AHS(F) >= psi (rearranged),
    using H(A∪B)<=H(A). This c_AHS(F) is the abundance the family 'looks like' to AHS.
    """
    Hu = V.exact_entropy_union(F)
    ps, chs = family_marginals_and_condH(F, n)
    S = sum((1 - ps[i]) * chs[i] for i in range(n))
    if Hu < 1e-12:
        return 1.0
    return 1.0 - S / Hu


def v1_certified_constant(F, n):
    """
    Vector 1: recapture Δ2. Same as AHS but replace the chain-rule lower bound
    Σ_i H(C_i|A_<i,B_<i) with the TRUE H(A∪B) (i.e. add back the full Δ2). This is
    the most optimistic Vector-1: assume we recover ALL of Δ2. Then the certified
    constant is 1 - S / H(A∪B) where S is the same numerator BUT now compared
    against the true union entropy with the chain slack folded in.
    Actually the honest V1 statement: H(A∪B) = Σ_i H(C_i|A_<i,B_<i) + Δ2. If the
    per-coordinate ineq gives Σ_i H(C_i|..) >= (1/(1-c)) S, then
        H(A∪B) >= (1/(1-c)) S + Δ2.
    Setting H(A∪B)<=H(A) and assuming max p_i<c (so S>(1-c)... ) the BEST possible
    V1 constant solves:  (1/(1-c)) S + Δ2 <= H(A)  becomes binding.
    We report c_V1(F) such that (1/(1-c_V1)) S + Δ2 = H(A∪B) (the family's own union
    entropy), i.e. 1-c_V1 = S/(H(A∪B)-Δ2) = S / chainLB.
    """
    Hu = V.exact_entropy_union(F)
    clb = V.chain_rule_lower_bound(F, n)  # = H(A∪B) - Δ2
    ps, chs = family_marginals_and_condH(F, n)
    S = sum((1 - ps[i]) * chs[i] for i in range(n))
    if clb < 1e-12:
        return 1.0
    return 1.0 - S / clb


def v2_joint_certified_constant(F, n):
    """
    Vector 2 (joint): track (A∪B, A∩B). Budget = H(A∪B,A∩B) (the family's true
    joint entropy; honest upper bound, since (A∪B,A∩B) is a function of (A,B) so
    H(A∪B,A∩B)<=2H(A), but we use the TRUE value which is what a tight proof sees).
    Lower bound: chain rule Σ_i H(C_i,D_i|A_<i,B_<i) = Σ_i E[H_pair_CD(α,β)].
    The matching 'budget numerator' for the joint is the FULL pair conditional
    entropy Σ_i [H(A_i|A_<i)+H(B_i|B_<i)] = 2 Σ_i H(A_i|A_<i) (NOT weighted by 1-p).
    But to mirror AHS we use the weighted form that the per-coord inequality
    H_pair_CD(a,b) >= μ[(1-b)h(a)+(1-a)h(b)] provides. The closing (see derivation)
    gives c = 1 - [Σ(1-p_i)2H(A_i|A_<i)... ].
    Operationally: c_V2joint(F) = 1 - S2 / H(A∪B,A∩B), where S2 = Σ_i 2(1-p_i)H(A_i|A_<i)
    is the lower-bound numerator (factor 2 because both A_i and B_i contribute).
    """
    Hcd = V.exact_entropy_union_and_intersection(F)
    ps, chs = family_marginals_and_condH(F, n)
    S2 = sum(2 * (1 - ps[i]) * chs[i] for i in range(n))
    if Hcd < 1e-12:
        return 1.0
    return 1.0 - S2 / Hcd


def v2_lambda_certified_constant(F, n, lam):
    """
    Vector 2 (weighted): objective H(A∪B) + lam*H(A∩B).
    Honest budget: H(A∪B)+lam*H(A∩B) <= H(A∪B) + lam*H(A∩B) ... we need an upper
    bound. Use H(A∪B)<=H(A) [union-closure] and H(A∩B)<=H(A∩B,A∪B)-H(A∪B|A∩B)...
    The clean honest budget: H(A∪B)+lam H(A∩B) <= H(A)+lam*H_int_upper where
    H_int_upper is the best provable upper bound on H(A∩B). Since A∩B ⊆ A and ⊆ B,
    no union-closure bound applies; the safe bound is H(A∩B) <= H(A) (NOT valid in
    general!) -- so we instead use the TRUE family values to see the best case:
    budget = H(A∪B)+lam*H(A∩B) (true), lower bound numerator = (1+lam) Σ(1-p_i)H(A_i|A_<i)
    [union gives Σ(1-p)H(.), inter gives by symmetry lam*Σ p... actually different].
    For a HONEST best-case diagnostic we compute:
      c = 1 - [ Σ(1-p_i)H(A_i|A_<i) + lam*(inter lower bound numerator) ] / (H(A∪B)+lam H(A∩B)).
    The intersection lower bound: H(A∩B) >= Σ_i H(D_i|A_<i,B_<i)=Σ E[h(αβ)]; its 'AHS-style'
    numerator is lam * Σ p_i H(A_i|A_<i) (mirror image). We use that.
    """
    Hu = V.exact_entropy_union(F)
    Hi = V.exact_entropy_intersection(F)
    ps, chs = family_marginals_and_condH(F, n)
    S_union = sum((1 - ps[i]) * chs[i] for i in range(n))
    S_inter = sum(ps[i] * chs[i] for i in range(n))  # mirror numerator
    budget = Hu + lam * Hi
    num = S_union + lam * S_inter
    if budget < 1e-12:
        return 1.0
    return 1.0 - num / budget


def true_abundance(F, n):
    Fl = list(F); m = len(Fl)
    freqs = [sum(1 for a in Fl if a & (1 << i)) for i in range(n)]
    return max(freqs) / m if freqs else 0.0


if __name__ == "__main__":
    from enumerate import all_uc_families
    import statistics

    print(f"PSI = {PSI:.6f}\n")
    print("Per-family certified constants (the abundance each strategy 'sees').")
    print("A strategy BEATS AHS iff its min over families is > AHS's min (closer to true 0.5).\n")

    rows = []
    NMAX = 5
    for n in range(NMAX + 1):
        for F in all_uc_families(n, dedupe_isomorphic=True):
            if not F or F == frozenset({0}):
                continue
            HA = V.exact_H_A(F)
            if HA < 1e-9:
                continue
            ab = true_abundance(F, n)
            c_ahs = ahs_certified_constant(F, n)
            c_v1 = v1_certified_constant(F, n)
            c_v2j = v2_joint_certified_constant(F, n)
            c_v2l = v2_lambda_certified_constant(F, n, lam=1.0)
            rows.append((ab, c_ahs, c_v1, c_v2j, c_v2l, n, F))

    # The certified constant of a STRATEGY = min over families of its per-family value
    # (the worst family is what bounds the provable constant).
    min_ahs = min(r[1] for r in rows)
    min_v1 = min(r[2] for r in rows)
    min_v2j = min(r[3] for r in rows)
    min_v2l = min(r[4] for r in rows)
    print(f"  Strategy   |  min over families (= certifiable constant on this test set)")
    print(f"  AHS        |  {min_ahs:.6f}")
    print(f"  V1 (Δ2)    |  {min_v1:.6f}   {'>AHS' if min_v1>min_ahs+1e-9 else '= or < AHS'}")
    print(f"  V2 joint   |  {min_v2j:.6f}   {'>AHS' if min_v2j>min_ahs+1e-9 else '= or < AHS'}")
    print(f"  V2 λ=1     |  {min_v2l:.6f}   {'>AHS' if min_v2l>min_ahs+1e-9 else '= or < AHS'}")
    print()
    # show the worst families for AHS and whether V1/V2 help THERE
    rows.sort(key=lambda r: r[1])
    print("  Worst families for AHS (smallest c_AHS), with V1/V2 on the same family:")
    print(f"  {'abund':>7} {'c_AHS':>8} {'c_V1':>8} {'c_V2j':>8} {'c_V2λ1':>8} {'n':>2}")
    for r in rows[:12]:
        print(f"  {r[0]:7.4f} {r[1]:8.5f} {r[2]:8.5f} {r[3]:8.5f} {r[4]:8.5f} {r[5]:2d}")
