# Frankl Experiments Toolkit

Computational infrastructure for research on **Frankl's Union-Closed Sets
Conjecture**.

> *Conjecture (Frankl, 1979).* Let F be a finite family of sets, closed
> under union, with F ≠ {∅}. Then there exists an element x in the ground
> set with |{A ∈ F : x ∈ A}| ≥ |F|/2.

This package is the Phase-1 experimental scaffolding for our multi-agent
research effort. Phase-2 theory agents will use these tools to test
candidate entropy inequalities, search for tight examples, and produce
data tables that go into the paper.

## File map

| File                  | Purpose                                                       |
|-----------------------|---------------------------------------------------------------|
| `uc_family.py`        | Core types: `Family` = `frozenset[int]` (bitmask sets), with `is_union_closed`, `union_closure`, `frequency`, `abundance`, `canonical_form`. |
| `enumerate.py`        | DFS enumeration of UC families on `[n]`, either labeled or up to S_n-orbit. |
| `_canonical.py`       | Fast canonical-form computation using element-signature partition refinement. |
| `extremal_search.py`  | Find UC families minimising the maximum element abundance.    |
| `entropy_bounds.py`   | Shannon entropy, Gilmer's inequality, the (3-√5)/2 constant, and a generic candidate-inequality sweep harness. |
| `verify_frankl.py`    | Direct verification of Frankl on all UC families with n ≤ 5.  |
| `run_baseline.py`     | End-to-end smoke run; writes a JSON snapshot to `data/`.      |
| `tests/test_uc.py`    | pytest suite for every module above.                          |

## Representation

A family `F` over ground set `[n] = {0, …, n-1}` is a
`frozenset[int]`. Each `int` is a bitmask: bit `k` set ⇔ element `k` is in
that subset. So `family_from_sets([[0,1], [2]])` yields
`frozenset({0b011, 0b100}) = frozenset({3, 4})`.

Why bitmasks? Union is a single `|` instruction; membership tests on
individual elements are bit tests; `frozenset(int)` is hashable, so a
family is itself a hashable first-class value. Python's arbitrary-precision
ints take over transparently if `n > 30`.

## Entropy methodology

`entropy_bounds.py` implements Gilmer's inequality (arXiv:2211.09055) and
the constant `c = (3-√5)/2 ≈ 0.382` from Alweiss-Huang-Sellke
(arXiv:2211.11731), Chase-Lovett (arXiv:2211.11504), and Sawin
(arXiv:2211.13139). The constant is *computed* by bisection on the
algebraic equation `c² - 3c + 1 = 0` — never hard-coded.

The pluggable harness `sweep_inequality(inequality, n_max)` takes any
candidate inequality

    inequality : Family → (LHS, RHS),

interpreted as the assertion `LHS ≤ RHS for every UC family`, and sweeps
it against all UC families on `[0..n_max]`. Phase-2 agents will use this
to:

  * Falsify candidate strengthenings (search for a violating family).
  * Quantify empirical slack (`RHS - LHS`) on the extremal families.

## Running

```bash
cd math/frankl/experiments
python run_baseline.py                # full baseline, n ≤ 5
python run_baseline.py --n-max 4      # quicker
python -m pytest tests/               # unit tests
```

Output JSON is written to `data/baseline.json`.

## Status & roadmap

  * Phase 1 (done — this PR): primitives, enumeration up to n = 5,
    Gilmer's inequality, sweep harness.
  * Phase 2 (next): catalog extremal families up to n = 6; test
    candidate strengthenings of Gilmer; structured search for high-slack
    coordinate distributions.
  * Phase 3: integrate with the paper draft under `../paper/`.

## References

  * Gilmer, *A constant lower bound for the union-closed sets conjecture*, arXiv:2211.09055 (2022).
  * Alweiss, Huang, Sellke, *Improved Lower Bound for Frankl's Union-Closed Sets Conjecture*, arXiv:2211.11731 (2022; *Electron. J. Combin.* 31(3), 2024).
  * Chase, Lovett, *An improved lower bound for the union-closed set conjecture*, arXiv:2211.11504 (2022).
  * Sawin, *Extension of a Method of Gilmer*, arXiv:2211.13139 (2022).
  * Cambie, *Better bounds for the union-closed sets conjecture using the entropy approach*, arXiv:2212.12500 (2022).
  * Yu, *Improving the Lower Bound for the Union-closed Sets Conjecture via Conditionally IID Coupling*, arXiv:2306.08824 (2023).
