# Book Harness

Reusable multi-agent workflow for the personality framework. One run = one task against one or all
four systems, with guards always on.

## Agent roster

Per system subgroup (S1 social energy, S2 thinking machine, S3 emotional/social disposition,
S4 objectives):

1. **Supporting-case literature checker** — searches the research literature for the strongest
   evidence FOR each claim; doubles as novelty watch.
2. **Contradicting-case literature checker** — searches for the strongest evidence AGAINST:
   boundary conditions, failed replications, contested findings.
3. **Citation verifier** — separate from the checkers: confirms each cited work exists and says
   what we claim it says. Catches stretched and hallucinated citations.
4. **Framework constructor** — reconciles verified evidence into keep/revise/add/retire proposals
   for the system's constructs, options-with-a-lean where genuinely open.
5. **Writer** — drafts revised chapter text to `book/proposals/<sys>_draft.md`. Never edits live
   chapters; the author decides what merges.

Global (run once over all packages, because cross-system defects need the whole picture):

6. **Canon keeper** — enforces the axioms everywhere: preference-not-ability, three lanes,
   no-valence (barred words), clean-or-silent, snapshot-not-verdict, stated/revealed symmetry,
   cross-system boundaries.
7. **Red team** — hostile psychometrician + hostile domain expert pass over everything produced.
8. **Instrument impact assessor** — maps every framework change to the exact edits owed in the
   metrics catalog, the instrument design, and the app, so book and test never drift apart.
9. **Editor-in-chief** — consolidates the run into one plain-English memo.

Coordination is the workflow script itself, deterministically — not an agent. A coordinator agent
per subgroup was considered and rejected: LLM-mediated coordination is lossy and drifts; judgment
belongs in agents, control flow belongs in code.

## Usage

Invoke via the Workflow tool with `scriptPath: harness/book_harness.js` and `args`:

- `system`: `s1` | `s2` | `s3` | `s4` | `all`
- `task`:
  - `research` — literature + citation verification only (cheapest)
  - `develop` — research + framework constructor
  - `write` — research + writer (draft to proposals/)
  - `full` — everything
- `claims`: array of claim strings to check (optional; omitted = checkers derive the chapter's
  load-bearing claims themselves)
- `focus`: free-text steer for the constructor/writer (optional)

Examples:

- Check S4's motive taxonomy against motivation research:
  `{system: "s4", task: "research", claims: ["Five motives (order/peace, triumph, power, truth-seeking, novelty) span the motive space", "Control collapses into power", "Validation is orthogonal to motivation"]}`
- Full development pass on one system: `{system: "s3", task: "full", focus: "..."}`

Guards and the editor-in-chief run on every task. Outputs: a memo (returned), proposal files under
`book/proposals/` when the writer runs, and a guard-violation count. Nothing edits live chapters,
the catalog, the design doc, or the app — the harness proposes, the authors dispose.
