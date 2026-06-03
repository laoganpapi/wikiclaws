"""
cover_graph_spectrum.py — Spectral-graph / HDX probe for Frankl (open exploration).

Lives under math/ideas/generation/_probe/ (idea-generation sandbox; touches
nothing in frankl/experiments). It imports the read-only frankl toolkit
(lattice.py, uc_family.py, enumerate.py) to enumerate UC families n<=5 and, for
each, builds NON-MOMENT spectral objects on the *cover graph* (Hasse diagram)
and the *comparability graph* of the lattice L=(F,subseteq,cup), then correlates
them with abundance.

WHY this might escape the abelian-hypercube barrier
---------------------------------------------------
The proven barrier (boolean_fourier.md, Thm 4.3) is about the (Z/2)^n Walsh
spectrum of 1_F on the *ambient* cube. That spectrum is rotation+sign invariant
in the ground elements, so it is a SYMMETRIC moment and degenerates on 2^[k].

Here the spectral object is the Laplacian of a graph whose VERTICES are the
members of F (not the ground elements) and whose EDGES are the *order/cover*
relations. This is NOT a function of the abelian cube characters; it is sensitive
to the incidence structure of the lattice. Two lattice-isomorphic families share
this spectrum (it is an iso-invariant of L) but the LABELLING is what carries
abundance (cone trick) -- so we expect the *graph* spectrum alone to be a lattice
invariant (hence, by lattice_attack.md, NOT a complete certificate). The point of
the probe is to MEASURE how much of abundance the cover-graph / link spectra
capture, and in particular whether the Hoffman ratio bound on a fibre-weighted
graph -- which DOES see the labelling -- correlates.

Objects computed per family:
  (1) cover graph G_cov: vertices = L, edges = cover (Hasse) pairs.
      - L2 = second-smallest eigenvalue (algebraic connectivity / spectral gap)
        of the (unnormalized) graph Laplacian.
      - lmax_norm = largest eigenvalue of the normalized Laplacian.
  (2) comparability graph G_cmp: vertices = L, edges = comparable pairs a<b.
      - Hoffman ratio bound on the independence number using the fibre Fib(x)
        as a candidate independent-ish / clique-ish set is NOT meaningful (fibres
        are chains-of-filters), so instead we use the Hoffman bound to bound the
        max fibre = abundance from the spectrum of a FIBRE-WEIGHTED operator.
  (3) Garland / local-spectral (Oppenheim trickle-down) quantity:
      the order complex (simplicial complex of chains in L) has links; for each
      vertex v=A in L, the link is the order complex of the open interval
      (0hat, T) restricted to elements comparable-and-distinct from A, i.e. of
      L \ {A} induced ... we use the simplest 1-skeleton local spectral gap:
      for each vertex v of G_cov, lambda2 of the LINK graph (neighbours of v in
      the comparability graph with induced comparability edges). min over v is
      the local spectral expansion lambda_loc; Garland/Oppenheim say global
      expansion trickles up from min local. We report min_v lambda2(link).

The HOFFMAN-RATIO connection to abundance (the load-bearing idea):
  abundance = max_x |Fib(x)|/|L|. Fib(x) is a FILTER (up-set), hence an
  *independent set* in NO standard sense -- but its complement-of-non-fibre is.
  We instead test the cleanest spectral lower bound on the max filter:
  for the fibre-incidence bipartite graph B (ground elements x vs members A,
  edge iff x in A), abundance = (max row weight)/|L|. The Hoffman/expander-mixing
  lemma gives, for the normalized adjacency of B, a lower bound on max row weight
  in terms of the average degree and the second singular value. We compute the
  expander-mixing slack and check whether it ever forces >= 1/2.

Outputs:
  data/cover_spectrum_n{0..5}.jsonl  -- one row per UC family (orbit rep).
  prints a correlation summary to stdout.

Reproduce:
  cd math/ideas/generation/_probe
  python3 cover_graph_spectrum.py 5
"""

from __future__ import annotations

import json
import math
import os
import sys

# import the READ-ONLY frankl toolkit (we add its path; we do not modify it)
_HERE = os.path.dirname(os.path.abspath(__file__))
_FRANKL_EXP = os.path.normpath(
    os.path.join(_HERE, "..", "..", "..", "frankl", "experiments")
)
sys.path.insert(0, _FRANKL_EXP)

import numpy as np  # noqa: E402

import lattice as lat  # noqa: E402
from enumerate import all_uc_families  # noqa: E402
from uc_family import abundance, frequencies  # noqa: E402
from ji_labelling import with_bottom, fibres  # noqa: E402


# ---------------------------------------------------------------------------
# Graph builders on the lattice L
# ---------------------------------------------------------------------------

def cover_edges(elements: list[int]) -> list[tuple[int, int]]:
    """Hasse / cover edges (i,j) as index pairs into `elements`."""
    below = lat.cover_relation(elements)
    idx = {e: i for i, e in enumerate(elements)}
    edges = []
    for y, xs in below.items():
        for x in xs:
            edges.append((idx[x], idx[y]))
    return edges


def comparability_edges(elements: list[int]) -> list[tuple[int, int]]:
    """All comparable distinct pairs (i<j by inclusion) as index pairs."""
    idx = {e: i for i, e in enumerate(elements)}
    edges = []
    m = len(elements)
    for i in range(m):
        for j in range(m):
            if i == j:
                continue
            a, b = elements[i], elements[j]
            if (a & b) == a and a != b:  # a subset of b, a != b
                edges.append((idx[a], idx[b]))
    # dedupe undirected
    und = set()
    for (i, j) in edges:
        und.add((min(i, j), max(i, j)))
    return sorted(und)


def laplacian_spectrum(m: int, undirected_edges: list[tuple[int, int]]):
    """Return sorted eigenvalues of the unnormalized Laplacian and of the
    normalized Laplacian (skipping isolated-vertex degeneracies)."""
    A = np.zeros((m, m))
    for (i, j) in undirected_edges:
        A[i, j] = 1.0
        A[j, i] = 1.0
    deg = A.sum(axis=1)
    L = np.diag(deg) - A
    evL = np.sort(np.linalg.eigvalsh(L))
    # normalized Laplacian L_sym = I - D^{-1/2} A D^{-1/2}
    with np.errstate(divide="ignore"):
        dinv = np.where(deg > 0, 1.0 / np.sqrt(deg), 0.0)
    Lsym = np.eye(m) - (dinv[:, None] * A * dinv[None, :])
    evN = np.sort(np.linalg.eigvalsh(Lsym))
    return evL, evN, deg


def algebraic_connectivity(evL: np.ndarray) -> float:
    """Second-smallest Laplacian eigenvalue (Fiedler value). 0 if disconnected."""
    if len(evL) < 2:
        return 0.0
    return float(evL[1])


# ---------------------------------------------------------------------------
# Garland / Oppenheim local spectral expansion on the comparability graph
# ---------------------------------------------------------------------------

def min_link_spectral_gap(elements: list[int], cmp_edges: list[tuple[int, int]]):
    """
    Crude 1-dimensional local spectral quantity. For each vertex v, take its link
    = induced comparability subgraph on N(v) (the comparable elements), and
    compute the normalized-Laplacian spectral gap of that link. Garland/Oppenheim
    'trickle-down': if every link is a good expander, the global complex expands.
    We return min over v of lambda2(normalized Laplacian of link), and the mean.

    Vertices with link size < 2 are skipped (no meaningful gap).
    """
    m = len(elements)
    adj = {i: set() for i in range(m)}
    for (i, j) in cmp_edges:
        adj[i].add(j)
        adj[j].add(i)
    gaps = []
    for v in range(m):
        nbrs = sorted(adj[v])
        if len(nbrs) < 2:
            continue
        local_idx = {u: k for k, u in enumerate(nbrs)}
        loc_edges = []
        for a in nbrs:
            for b in adj[a]:
                if b in local_idx and a < b:
                    loc_edges.append((local_idx[a], local_idx[b]))
        if not loc_edges:
            gaps.append(0.0)
            continue
        _, evN, _ = laplacian_spectrum(len(nbrs), loc_edges)
        gaps.append(float(evN[1]) if len(evN) >= 2 else 0.0)
    if not gaps:
        return None, None
    return min(gaps), sum(gaps) / len(gaps)


# ---------------------------------------------------------------------------
# Hoffman / expander-mixing bound on the fibre-incidence bipartite graph
# ---------------------------------------------------------------------------

def fibre_incidence_hoffman(F, n: int, elements: list[int]):
    """
    Bipartite incidence B between ground elements x in [n] and members A in L,
    edge iff x in A. abundance = (max over x of fibre size)/|L|.

    The expander-mixing / Hoffman-style heuristic lower bound on the max row
    weight: let d_bar = average fibre size = (sum_x |Fib(x)|)/n_active. The max
    is at least the average, and the second singular value sigma2 of the
    normalized bipartite adjacency quantifies how far the max can sit ABOVE the
    average. We report:
      avg_fib_density = d_bar/|L|              (a clean LOWER bound on abundance)
      sigma2          = 2nd singular value of D_r^{-1/2} B D_c^{-1/2}
      hoffman_gap     = abundance - avg_fib_density   (the 'spread' sigma2 governs)
    The QUESTION the probe answers: is avg_fib_density (a non-spectral mean) ever
    >= 1/2, and does sigma2 correlate with the gap abundance - mean?
    """
    m = len(elements)
    active = [x for x in range(n) if any((A >> x) & 1 for A in elements)]
    if not active:
        return None
    B = np.zeros((len(active), m))
    for r, x in enumerate(active):
        for c, A in enumerate(elements):
            if (A >> x) & 1:
                B[r, c] = 1.0
    rdeg = B.sum(axis=1)  # fibre sizes
    cdeg = B.sum(axis=0)  # |A| for each member
    avg_fib = float(rdeg.mean())
    max_fib = float(rdeg.max())
    # normalized bipartite adjacency singular values
    with np.errstate(divide="ignore"):
        dr = np.where(rdeg > 0, 1.0 / np.sqrt(rdeg), 0.0)
        dc = np.where(cdeg > 0, 1.0 / np.sqrt(cdeg), 0.0)
    Bn = dr[:, None] * B * dc[None, :]
    sv = np.linalg.svd(Bn, compute_uv=False)
    sigma2 = float(sv[1]) if len(sv) >= 2 else 0.0
    return {
        "avg_fib_density": avg_fib / m,
        "max_fib_density": max_fib / m,  # == abundance restricted to L
        "sigma2_bipartite": sigma2,
        "hoffman_gap": (max_fib - avg_fib) / m,
    }


# ---------------------------------------------------------------------------
# Per-family record
# ---------------------------------------------------------------------------

def analyze(F, n: int) -> dict:
    L = with_bottom(F)
    elements, bottom, top = lat.as_lattice(L)
    m = len(elements)
    ab = abundance(L)

    cov = cover_edges(elements)
    cov_und = sorted({(min(i, j), max(i, j)) for (i, j) in cov})
    cmp_e = comparability_edges(elements)

    evL_cov, evN_cov, deg_cov = laplacian_spectrum(m, cov_und)
    evL_cmp, evN_cmp, deg_cmp = laplacian_spectrum(m, cmp_e)

    fiedler_cov = algebraic_connectivity(evL_cov)
    fiedler_cmp = algebraic_connectivity(evL_cmp)
    lmax_norm_cov = float(evN_cov[-1]) if len(evN_cov) else 0.0

    min_link, mean_link = min_link_spectral_gap(elements, cmp_e)
    hoff = fibre_incidence_hoffman(F, n, elements)

    rec = {
        "n": n,
        "m": m,
        "abundance": ab,
        "fiedler_cover": fiedler_cov,
        "fiedler_comparability": fiedler_cmp,
        "lmax_norm_cover": lmax_norm_cov,
        "min_link_gap": min_link,
        "mean_link_gap": mean_link,
    }
    if hoff is not None:
        rec.update(hoff)
    return rec


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main(nmax: int):
    rows = []
    for n in range(0, nmax + 1):
        cnt = 0
        outpath = os.path.join(_HERE, f"cover_spectrum_n{n}.jsonl")
        with open(outpath, "w") as fh:
            for F in all_uc_families(n, dedupe_isomorphic=True):
                if len(F) < 2:  # Frankl excludes trivial; need >=2 members
                    continue
                rec = analyze(F, n)
                fh.write(json.dumps(rec) + "\n")
                rows.append(rec)
                cnt += 1
        print(f"n={n}: {cnt} non-trivial UC orbit reps -> {os.path.basename(outpath)}")

    # ---- correlation summary ----
    def col(name):
        return np.array([r[name] for r in rows if r.get(name) is not None], dtype=float)

    def paired(a_name, b_name):
        a, b = [], []
        for r in rows:
            if r.get(a_name) is not None and r.get(b_name) is not None:
                a.append(r[a_name])
                b.append(r[b_name])
        a = np.array(a, dtype=float)
        b = np.array(b, dtype=float)
        if len(a) < 3 or a.std() == 0 or b.std() == 0:
            return float("nan")
        return float(np.corrcoef(a, b)[0, 1])

    ab = col("abundance")
    print("\n=== Summary over", len(rows), "non-trivial UC families (n<=%d) ===" % nmax)
    print(f"abundance: min={ab.min():.4f} mean={ab.mean():.4f} max={ab.max():.4f}")
    print("Pearson corr(abundance, X):")
    for x in [
        "fiedler_cover", "fiedler_comparability", "lmax_norm_cover",
        "min_link_gap", "mean_link_gap",
        "avg_fib_density", "sigma2_bipartite", "hoffman_gap", "max_fib_density",
    ]:
        print(f"  {x:24s} {paired('abundance', x):+.4f}")

    # KEY non-spectral lower bound check: is avg_fib_density ever >= 1/2?
    afd = col("avg_fib_density")
    print(f"\navg_fib_density (mean fibre / |L|): min={afd.min():.4f} "
          f"max={afd.max():.4f}; >=0.5 in {(afd >= 0.5 - 1e-9).sum()}/{len(afd)} families")

    # Does any single spectral quantity force abundance >= 1/2 monotonically?
    # Report, among families with abundance == 0.5 EXACTLY (the cube/extremal set),
    # the spread of each spectral statistic -> shows degeneracy (barrier echo).
    half = [r for r in rows if abs(r["abundance"] - 0.5) < 1e-9]
    print(f"\nFamilies at abundance == 0.5 exactly: {len(half)}")
    for x in ["fiedler_cover", "fiedler_comparability", "min_link_gap",
              "sigma2_bipartite", "max_fib_density"]:
        vals = [r[x] for r in half if r.get(x) is not None]
        if vals:
            print(f"  {x:24s} range over the 0.5-extremal set: "
                  f"[{min(vals):.4f}, {max(vals):.4f}]")

    # Cube footprint: the Boolean cubes 2^[k] are the unique minab=1/2 lattices.
    # Print their cover-graph spectrum to show it is NON-trivial (unlike the
    # Walsh spectrum which collapses) -- the central 'escapes-the-barrier' claim.
    print("\n=== Boolean cube cover-graph spectra (the abelian barrier extremizer) ===")
    for k in range(1, min(nmax, 4) + 1):
        cube = frozenset(range(1 << k))  # all subsets of [k]
        elements, _, _ = lat.as_lattice(cube)
        cov = cover_edges(elements)
        cov_und = sorted({(min(i, j), max(i, j)) for (i, j) in cov})
        evL, evN, _ = laplacian_spectrum(len(elements), cov_und)
        ml, _ = min_link_spectral_gap(elements, comparability_edges(elements))
        print(f"  B_{k} (|L|={len(elements)}): Fiedler(cover)={evL[1]:.4f}, "
              f"Lap spectrum range=[{evL[0]:.3f},{evL[-1]:.3f}], "
              f"min_link_gap={ml}")


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    main(nmax)
