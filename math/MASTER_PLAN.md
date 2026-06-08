# Master Research Plan: Collatz & Frankl Conjectures

**Goal:** Publishable paper(s) on the Collatz Conjecture and Frankl's Union-Closed Sets Conjecture. Two independent tracks; whichever shows more progress before resources run out becomes the lead deliverable.

**Branch:** `claude/epic-dirac-p1oQo`
**Authors:** Alex Ye with Claude (AI-assisted methodology disclosed per current publication norms).

---

## Strategic Frame

We are not assuming we will prove either conjecture. We are running a serious multi-agent investigation that produces, at minimum:

1. A rigorous **state-of-the-art survey** with original synthesis.
2. **Computational experiments** that probe specific subquestions.
3. **Theoretical exploration** of under-explored attack vectors.
4. A **paper draft** suitable for arXiv submission. Best case: a new partial result.

The Frankl track has a clearer frontier (push the entropy-method constant from ~0.38 toward 0.5). The Collatz track will focus on (a) extending Tao's logarithmic-density approach, (b) automaton/2-adic structural results, and (c) computational invariants.

## Tracks

### Track A — Frankl Union-Closed Sets
- **A1 Literature**: Gilmer 2022 → Sawin → Chase-Lovett → Alweiss-Huang-Sellke → Cambie → 2024-2025 updates. Compile all entropy-method variants.
- **A2 Theory**: Identify the bottleneck in current entropy proofs. Can we replace Shannon entropy with a Rényi or relative entropy variant? Is there slack in the convexity step?
- **A3 Experiments**: Build computational verifier for small union-closed families. Test conjectured strengthenings on families of size ≤ 20. Search for extremal examples.
- **A4 Paper**: Draft survey-with-experiments paper; integrate any new theoretical observation.

### Track B — Collatz 3n+1
- **B1 Literature**: Lagarias survey → Terras → Tao 2019 → recent 2024-2025 work. Catalog all structural approaches (ergodic, p-adic, automaton, dynamical).
- **B2 Theory**: Examine Tao's logarithmic-density approach. What blocks "almost bounded" → "bounded"? Explore 2-adic / Sylvester-Fibonacci connections.
- **B3 Experiments**: Replicate verification frontier (~2^68). Statistical analysis of stopping times. Search for invariants on residue classes mod 2^k.
- **B4 Paper**: Draft survey + computational + any theoretical observation.

## Agent Deployment Plan

**Phase 1 — Foundation (parallel, ~now):**
- Agent A1: Frankl literature survey
- Agent B1: Collatz literature survey
- Agent S0: Set up shared bibliography & notation conventions

**Phase 2 — Investigation (parallel, after Phase 1):**
- Agent A2: Frankl theoretical analysis
- Agent A3: Frankl computational experiments
- Agent B2: Collatz theoretical analysis
- Agent B3: Collatz computational experiments

**Phase 3 — Synthesis:**
- Agent A4: Frankl paper draft
- Agent B4: Collatz paper draft
- Agent X: Cross-pollination — look for shared techniques between tracks

**Phase 4 — Adversarial:**
- Red-team agent: hunt for errors, holes, prior art we missed
- Verifier agent: formalize key lemmas in Lean 4 where feasible

## Deliverables Per Phase

Each agent writes to its assigned directory:
- `collatz/literature/`, `collatz/experiments/`, `collatz/theory/`, `collatz/paper/`
- `frankl/literature/`, `frankl/experiments/`, `frankl/theory/`, `frankl/paper/`
- `shared/` for bibliography, notation, and cross-cutting notes

Every agent must produce concrete artifacts (markdown, code, data) — no hand-waving.

## Honesty Discipline

If an agent claims a proof, the verifier track must independently check. Failed attempts get recorded in a `dead_ends.md` per track so we don't repeat work. Negative results are valuable and stay in the record.
