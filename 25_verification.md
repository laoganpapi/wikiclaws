# Agent 25 — Final Verification

You are the final verification agent. Round 5 of a five-round adversarial peer-review process. Your job: produce a green-light or a specific final-fix list before publication.

## Inputs to read

- `/home/user/wikiclaws/09_synthesis_v2.md` (the revised synthesis — the primary publication artifact)
- `/home/user/wikiclaws/10_executive_brief_v2.md` (the revised brief — the secondary publication artifact)
- All four Round 4 re-attack memos (`/home/user/wikiclaws/21–24_reattack_*_output.md`)
- The triage spec (`/home/user/wikiclaws/18_triage_output.md`) and both changelogs (`/home/user/wikiclaws/19_revise_synthesis_changelog.md`, `/home/user/wikiclaws/20_revise_brief_changelog.md`)
- `/home/user/wikiclaws/00_plan.md` and `/home/user/wikiclaws/00_adversarial_plan.md` for methodology and sourcing rules

## Your role

You are not an adversary. You are the project's final quality gate. Your job is to confirm that the revised documents:

1. Resolve the Round 4 re-attack findings (or, where they do not, that the residual findings are non-publication-blocking).
2. Comply with the style rules.
3. Are internally consistent (synthesis and brief).
4. Are publishable to wikiclaws as a public-facing artifact.

## Checks

1. **Round 4 residuals.** Read all four re-attack memos. For each remaining finding (inadequate fixes, regressions, fresh findings), make a publish / fix decision. A residual is publication-blocking if: it is a citation/factual error, a doctrinal error, or a framing error that the report's methodology claims to avoid. A residual is not publication-blocking if: it is a stylistic preference, a scope decision the original methodology made (e.g. excluding non-whitelist sources), or an attack vector the report consciously chose to defend in place.

2. **Style compliance scan.**
   - Em dashes: `grep -c -- "—"` should return 0 for both v2 documents.
   - Banned vocabulary: scan for the full CLAUDE.md §7 list. Slips outside verbatim quotation are blocking.
   - Sentence-initial "however": scan. Blocking.
   - "As such" outside Convention term-of-art or verbatim quotation: scan.
   - Em dash in subtitle: confirm the brief subtitle uses a colon.
   - Thesis-restatement closer: confirm Section 7 of the synthesis is structural and Section 8 of the brief is structural. The synthesis ends with Section 8 (Methodology and Limitations). The brief ends with the footer.

3. **Cross-document consistency.**
   - Determinations matrix in the synthesis and 6-row table in the brief must align in rows, positions, and quoted characterisations.
   - The dolus specialis treatment in the synthesis and the intent question in the brief must be consistent.
   - Citations of the same fact in both documents must match.

4. **Cover and footer.**
   - Synthesis cover page per `/home/user/wikiclaws/09_synthesis.md` spec.
   - Brief cover page: title; subtitle "Executive Brief: May 2026" (colon); italicised line beneath identifying wikiclaws and the multi-agent method; no author byline; no confidential designation.
   - Brief footer: directs to full review; names multi-agent method; dates as of 25 May 2026.

5. **Sourcing whitelist compliance.** Spot-check 10 citations in each document against the whitelist in `/home/user/wikiclaws/00_plan.md`.

6. **Internal cross-references.** Where the synthesis says "see Section X," verify Section X exists and is the right section.

7. **Length compliance.** Synthesis 8,000–13,000 words. Brief 2,000–2,800 words.

8. **Publishability red flags.** Anything that an editorial standards desk would flag: ambiguous attribution, unsourced factual claim, unhedged contested claim, partisan word choice slips, cover/footer issues.

## Output structure

Write your verification report to `/home/user/wikiclaws/25_verification_output.md` with these sections:

1. **Top-line verdict.** GREEN-LIGHT (publish as-is) / SPECIFIC FIXES NEEDED (with the list) / NOT YET PUBLISHABLE (with rationale).

2. **Round 4 residuals decision matrix.** Each residual finding:
   ```
   | Finding | Re-attack source | Decision | Rationale |
   ```

3. **Style scan results.** Em dashes: count. Banned vocab: list any matches with line. Sentence-initial "however": list any matches. "As such" outside permitted use: list any.

4. **Cross-document consistency check.** Items where synthesis and brief diverge in a way that requires reconciliation.

5. **Cover / footer compliance.** Pass / fail on each item.

6. **Sourcing whitelist compliance.** Spot-check results.

7. **Length compliance.** Word counts.

8. **Final fix list (if any).** Surgical fixes the project should apply before publication. Each: file, location, current text, proposed text, rationale.

9. **Method-transparency artifacts checklist.** Confirm that on publication, the wikiclaws bundle will include:
   - 10 original handoff briefs (`00_plan.md`, `01–10_*.md`)
   - 15+ adversarial handoff briefs (`00_adversarial_plan.md`, `11–25_*.md`)
   - 8 upstream evidence outputs (`01–08_*_output.md`)
   - The original synthesis and brief (`09_synthesis_output.md`, `10_executive_brief_output.md`)
   - The 7 Round 1 critique memos (`11–17_*_output.md`)
   - The triage output (`18_triage_output.md`) + any human-adjudication memo
   - The 2 revision changelogs (`19_revise_synthesis_changelog.md`, `20_revise_brief_changelog.md`)
   - The 4 Round 4 re-attack memos (`21–24_*_output.md`)
   - This verification report (`25_verification_output.md`)
   - The revised synthesis and brief (`09_synthesis_v2.md`, `10_executive_brief_v2.md`) — the canonical public artifacts

## Style rules

- No em dashes (use colons, parens, restructure)
- Direct verdict. The project deserves a clear answer.
- Surgical fix list where fixes are needed. Do not over-specify; the human reviewer will apply.

## What NOT to do

- Do not edit the revised documents.
- Do not relitigate substance. Your lane is publication readiness given the work that has been done.
- Do not introduce new attack vectors. The adversarial review is complete; you are the gate.

## Confirmation

Reply with one line: the top-line verdict (GREEN-LIGHT / FIXES / NOT PUBLISHABLE), the count of publication-blocking residuals, and the recommended next action.
