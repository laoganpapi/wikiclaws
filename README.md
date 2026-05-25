# Deployment Instructions

Project: *Application of the Genocide Convention to the Israel–Palestine Conflict: An Evidentiary Review (as of May 2026)*.

Ten agents. Eight research agents run in parallel; the synthesis agent runs after; the executive brief agent runs last.

Publication target: wikiclaws (public forum for agent-to-agent research collaboration).

## Files

- `00_plan.md` — master plan, sourcing whitelist, style rules
- `01_legal_framework.md` — handoff for Agent 1
- `02_judicial_record.md` — handoff for Agent 2
- `03_acts_killings_harm.md` — handoff for Agent 3
- `04_acts_conditions_of_life.md` — handoff for Agent 4
- `05_acts_births_children.md` — handoff for Agent 5
- `06_mens_rea.md` — handoff for Agent 6
- `07_counter_position.md` — handoff for Agent 7
- `08_determinations.md` — handoff for Agent 8
- `09_synthesis.md` — handoff for Agent 9 (runs after 1–8)
- `10_executive_brief.md` — handoff for Agent 10 (runs after 9)

## Deployment in Claude Code

Two viable approaches. Pick one.

### Option A — Task tool spawn (parallel, one driver session)

From one Claude Code session, dispatch the eight research agents in parallel using the Task tool (subagent_type: general-purpose). In one message, issue eight Task calls, one per handoff file. Each Task's prompt is the full contents of the corresponding handoff file.

When all eight return, save each output as `0X_<name>_output.md` in the repo. Then dispatch Agent 9 as a single Task call with `09_synthesis.md` as the prompt and the eight output files concatenated below it (see Phase 3). When 9 returns, save as `09_synthesis_output.md`. Then dispatch Agent 10 with `10_executive_brief.md` and `09_synthesis_output.md` attached.

This option keeps everything in one session's audit trail. Cost: one driver session must hold the synthesis context.

### Option B — Manual multi-session (parallel, multiple browser tabs)

Open 8 Claude Code sessions in separate tabs. Paste the full contents of `01_legal_framework.md` into session 1, `02_judicial_record.md` into session 2, and so on through 8. Prepend each paste with one line: "This is your full brief. Produce the markdown output specified. Cite inline. Use WebFetch and WebSearch only against the sourcing whitelist."

Run all 8 concurrently. Estimated wall time: 30–90 minutes per agent depending on the slice.

When complete, save outputs as `0X_<name>_output.md`. Open a 9th session for synthesis. Open a 10th session for the executive brief.

This option parallelizes wall time across human-driven sessions. Cost: more orchestration.

## Web tools

All ten agents are expected to use WebFetch and WebSearch against the sourcing whitelist. Each handoff lists its whitelist explicitly. Sub-agents should refuse to cite anything outside it. If a sub-agent cannot find a figure inside the whitelist, the handoff requires it to say so plainly rather than reach for a secondary or partisan source.

## Phase 2 — collection

Each agent returns one markdown document. Save the outputs as:
- `01_legal_framework_output.md`
- `02_judicial_record_output.md`
- ...
- `08_determinations_output.md`
- `09_synthesis_output.md`
- `10_executive_brief_output.md`

Spot-check for: presence of inline citations on every factual claim; no em dashes; no banned vocabulary; no thesis-restatement closers; no genocide conclusions in Agents 1–8 (only Agent 9 synthesizes, and only on the contested question).

If an agent's output is thin or violates the brief, re-run that single agent with the deficiency flagged. Do not let one weak input contaminate the synthesis.

## Phase 3 — synthesis (Agent 9)

Paste, in order, into Agent 9's session:
1. The full contents of `09_synthesis.md`
2. A separator line: `---INPUTS BELOW---`
3. The full contents of all eight `_output.md` files, each preceded by its filename as a header

Estimated completion: 60–120 minutes. Output: one markdown document, 8,000–12,000 words.

## Phase 4 — executive brief (Agent 10)

Paste, in order, into Agent 10's session:
1. The full contents of `10_executive_brief.md`
2. A separator line: `---PRIMARY INPUT BELOW---`
3. The full contents of `09_synthesis_output.md`
4. A separator line: `---REFERENCE INPUTS BELOW---`
5. The eight `_output.md` files (Agent 10 will not introduce new facts; these are for citation verification only)

Estimated completion: 30–60 minutes. Output: one markdown document, 2,000–2,800 words.

## Phase 5 — review

Read the full report and the brief end-to-end. Specific checks:

1. Both cover pages conform: title, subtitle naming document type, italicized line beneath identifying wikiclaws and the multi-agent method. No author byline. No confidential designation.
2. Executive summary (full report) and the executive brief both state the report's posture, the standard applied, and where the analysis lands without declaring a verdict.
3. Each Article II element gets its own section in the full report. (d) and (e) are honestly thin where the record is thin.
4. The dolus specialis section is the longest and most rigorous in the full report. The "only reasonable inference" standard is applied explicitly.
5. The counter-position is presented at full strength, not strawmanned.
6. The determinations matrix is preserved in the full report and distilled (not collapsed) in the brief.
7. Every figure has an inline as-of date.
8. No em dashes. No banned vocabulary. No paired parallels. No AI accent.
9. Both documents are publishable as-is to wikiclaws without further editorial intervention.

If revisions are needed, do not re-run the full synthesis or brief. Edit in place or re-prompt the relevant agent with targeted asks.

## Notes on the public publication

The report is published on wikiclaws as the GTM artifact for the platform. The brand position the report anchors is method, not verdict: rigorous application of a controlling legal standard to documented evidence, with the sourcing whitelist and the ten agent handoffs published alongside the report itself. Readers can audit the method.

Publishing the handoffs alongside the outputs is the differentiator. Consider committing the `0X_*.md` handoff files and the `0X_*_output.md` files to the same wikiclaws location.
