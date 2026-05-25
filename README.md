# Deployment Instructions

Project: *Application of the Genocide Convention to the Israel–Palestine Conflict: An Evidentiary Review (as of May 2026)*.

Nine agents. Eight run in parallel; the ninth runs after.

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
- `09_synthesis.md` — handoff for Agent 9 (runs last)

## Deployment

### Phase 1 — parallel research (8 agents)

Open 8 simultaneous agent sessions. Paste the entire contents of `01_legal_framework.md` into session 1, `02_judicial_record.md` into session 2, and so on through 8. Each handoff is self-contained — sourcing whitelist, output structure, style rules, and "what not to do" are embedded.

Tell each agent at the top of the paste: "This is your full brief. Produce the markdown output specified. Cite inline. Stay within the whitelist." Nothing else.

Run all 8 concurrently. Estimated completion per agent: 30–90 minutes depending on tool latency, complexity of the slice, and whether the agent has web search.

### Phase 2 — collection

Each agent returns one markdown document. Save the outputs as:
- `01_legal_framework_output.md`
- `02_judicial_record_output.md`
- ...
- `08_determinations_output.md`

Spot-check for: presence of inline citations on every factual claim; no em dashes; no banned vocabulary; no thesis-restatement closers; no genocide conclusions in Agents 1–8 (only Agent 9 synthesizes).

If an agent's output is thin or violates the brief, re-run that single agent with the deficiency flagged. Do not let one weak input contaminate the synthesis.

### Phase 3 — synthesis (Agent 9)

Open a ninth agent session. Paste, in order:
1. The full contents of `09_synthesis.md`
2. A separator line: `---INPUTS BELOW---`
3. The full contents of all eight `_output.md` files, each preceded by its filename as a header

Tell the agent: "This is your full brief followed by the eight inputs. Produce the integrated report per the brief."

Estimated completion: 60–120 minutes. Output: one markdown document, 8,000–12,000 words.

### Phase 4 — review

Read the synthesis end-to-end. Specific checks:

1. Cover page conforms to internal working-doc convention (title, subtitle, date, confidential if applicable; no author credit; no "integrating X/Y/Z" subtitle).
2. Executive summary states the report's posture, the standard applied, and where the analysis lands without declaring a verdict.
3. Each Article II element gets its own section. (d) and (e) are honestly thin where the record is thin.
4. The dolus specialis section is the longest and most rigorous. The "only reasonable inference" standard is applied explicitly.
5. The counter-position is presented at full strength, not strawmanned.
6. The determinations matrix is preserved (not collapsed).
7. The conclusion is structural (what is settled, what is contested, what is not yet adjudicable), not declarative.
8. No em dashes. No banned vocabulary. No paired parallels. No AI accent.
9. Every figure has an inline as-of date.

If revisions are needed, do not re-run the full synthesis. Edit in place or re-prompt Agent 9 with targeted asks.

## Notes

- The report is a working document, not a Republic work product. Personal / wikiclaws GTM.
- If a sub-agent surfaces a major development since training cutoff (e.g. ICJ merits judgment issued, ICC genocide charges added, new authoritative determinations), that development goes into the relevant section and may shift the conclusion's structural framing. The synthesis prompt is built to accommodate this.
- Do not publish or distribute outputs that include unverified figures. The whitelist exists for credibility — both for the report's own substantive integrity and for the wikiclaws brand position the report is meant to anchor.
