# Book Harness

Reusable multi-agent workflow for the personality framework. One run = one task against one or all
four systems, with guards always on.

## Agent roster

Per system subgroup (S1 social energy, S2 thinking machine, S3 emotional/social disposition,
S4 objectives):

1. **Claim scanner** — extracts the chapter's 3-6 load-bearing empirical claims. Extraction only;
   it never checks them. Skipped when the run supplies claims explicitly.
2. **Supporting-case literature checkers** — search the research literature for the strongest
   evidence FOR each claim. One checker per batch of ≤3 claims.
3. **Contradicting-case literature checkers** — strongest evidence AGAINST: boundary conditions,
   failed replications, contested findings. Same ≤3-claim batching.
4. **Novelty watcher** — dedicated agent that flags any construct risking relabeling an
   established one. Split out of the supporting checker so neither job dilutes the other.
5. **Citation verifiers** — confirm each cited work exists and says what we claim it says. Each
   verifier gets ≤8 citation→claimed-use pairs, never the full evidence JSON.
6. **Framework constructor** — reconciles the verified evidence digest into keep/revise/add/retire
   proposals. Writes its full proposal to `book/proposals/<sys>_construction.md` and returns only
   a short summary.
7. **Writer** — reads the chapter and the constructor's proposal file itself, drafts revised
   chapter text to `book/proposals/<sys>_draft.md`. Never edits live chapters.
8. **Canon keeper (per system)** — enforces the axioms on this one system's digest and output
   files: preference-not-ability, three lanes, no-valence (barred words), clean-or-silent,
   snapshot-not-verdict, stated/revealed symmetry.
9. **Red team (per system)** — hostile psychometrician + hostile domain expert pass over this one
   system's outputs.

Global (the only agents that see more than one system, and only as compressed digests):

10. **Cross-system canon keeper** — runs only when >1 system is in the run; checks ONLY defects
    that span systems (boundary bleed, double-measured constructs, contradictory changes).
11. **Instrument impact assessors** — one agent per artifact (metrics catalog / instrument design
    doc / app), each reading only its own file and receiving only the compressed change list, so
    book and test never drift apart.
12. **Editor-in-chief** — consolidates the run into one plain-English memo from digests and guard
    verdicts, reading proposal files on demand.

Coordination is the workflow script itself, deterministically — not an agent. A coordinator agent
per subgroup was considered and rejected: LLM-mediated coordination is lossy and drifts; judgment
belongs in agents, control flow belongs in code.

## Context discipline

Every agent gets one bounded job, and nothing unbounded is ever inlined into a prompt:

- **Derive vs check are separate agents.** The claim scanner extracts; checkers only check.
- **Batching caps.** Literature checkers hold ≤3 claims; citation verifiers hold ≤8 citations.
  More claims or citations means more agents, not bigger ones.
- **Digests, not dumps.** Downstream prompts (constructor, guards, editor) receive a capped
  evidence digest (claims/verdicts/evidence excerpts, flagged citations only), never raw checker
  JSON.
- **Long output goes to files.** The constructor writes its full proposal to disk and returns a
  summary; the writer and editor read those files themselves by path.
- **Per-system guards first, cross-system second.** Canon keeper and red team run per system on
  one digest each; a single cross-system pass (digests only) catches what spans systems.
- **One artifact per impact assessor.** The catalog, design doc, and app each get their own
  assessor; the app assessor is told to Grep the large file rather than read it end to end.
- **Hard caps.** Any text inlined into a prompt passes through a truncation helper (`cap`), so a
  runaway agent output cannot flood the next agent's context.

## Token policy

Each agent runs on the cheapest model that can do its one job; nothing inherits an expensive
session model (Fable/Opus) by accident. The routing lives in the `MODELS`/`EFFORT` constants at
the top of the script:

| Agent | Model | Effort | Why |
|---|---|---|---|
| Claim scanner | haiku | low | extraction against a rubric — no judgment |
| Literature checkers | sonnet | medium | search + reading comprehension |
| Novelty watcher | sonnet | medium | same profile as the checkers |
| Citation verifiers | haiku | low | existence lookups — mechanical |
| Framework constructor | *inherits session model* | high | keep/revise/add/retire calls — the one step worth the cost |
| Writer | sonnet | medium | prose to a fixed template, decisions already made |
| Canon keeper (per system) | sonnet | low | checklist enforcement |
| Red team (per system) | sonnet | high | adversarial judgment, but bounded to one digest |
| Cross-system canon | sonnet | high | spans systems, still digest-only |
| Impact assessors | sonnet | low | change-to-edit mapping against one artifact |
| Editor-in-chief | sonnet | high | consolidation of already-compressed digests |

The constructor only runs on `develop`/`full`, so a `research` run never touches the session model
at all. Override per run via args: `models: {construct: "sonnet"}` to make even a full run
frugal, or `effort: {redteam: "max"}` to push harder on one seat.

## Usage

Invoke via the Workflow tool with `scriptPath: harness/book_harness.js` and `args`:

- `system`: `s1` | `s2` | `s3` | `s4` | `all`
- `task`:
  - `research` — literature + citation verification only (cheapest)
  - `develop` — research + framework constructor
  - `write` — research + writer (draft to proposals/)
  - `full` — everything
- `claims`: array of claim strings to check (optional; omitted = the claim scanner derives the
  chapter's load-bearing claims). Supplied claims apply to every chosen system, so pair explicit
  claims with a single system.
- `focus`: free-text steer for the constructor/writer (optional)

Examples:

- Check S4's motive taxonomy against motivation research:
  `{system: "s4", task: "research", claims: ["Five motives (order/peace, triumph, power, truth-seeking, novelty) span the motive space", "Control collapses into power", "Validation is orthogonal to motivation"]}`
- Full development pass on one system: `{system: "s3", task: "full", focus: "..."}`

Guards and the editor-in-chief run on every task. Outputs: a memo (returned), proposal files under
`book/proposals/` when the constructor/writer run, and a guard-violation count. Nothing edits live
chapters, the catalog, the design doc, or the app — the harness proposes, the authors dispose.
