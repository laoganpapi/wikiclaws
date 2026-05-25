# Adversarial Review Plan — Five Rounds, 15+ Agents

## Goal

Produce a version of the synthesis report (`09_synthesis_output.md`) and the executive brief (`10_executive_brief_output.md`) where the most credible attack from any direction has been considered, tested, and either remediated or explicitly defended in place with documented rationale. Published version survives sophisticated peer review from biased and expert adversaries alike.

## Threat model — attack vectors covered

The five rounds collectively defend against these seven categories of attack on the published report:

1. **Pro-Israel legal-defense critique.** The sophisticated IDF/MFA legal advisor or sympathetic international-law scholar (e.g. Bell, Kontorovich, Shany pre-evolution). Attacks: MoH-figures-are-Hamas-controlled; Albanese is biased and unreliable; SA application paragraph counts are mischaracterised; Hamas embedding ignored; evacuation/aid record underweighted; rhetoric vs. policy conflated; jus ad bellum vs. jus in bello conflated; provisional measures treated as merits; +972/Local Call cited as if independent.

2. **Pro-Palestine prosecution critique.** The sophisticated South Africa legal team / Albanese / Segal / Erakat perspective. Attacks: false equivalence; counter-position given more weight than the evidentiary asymmetry supports; Israeli counter-narrative platformed without commensurate scrutiny; decades of occupation context erased; Pillay CoI treated as "one body" rather than the most authoritative UN finding; western state rejections weighted disproportionately; Hamas comparator analysis distorts the central legal question.

3. **Citation accuracy critique.** Every quote, paragraph number, date, source attribution, name spelling, figure, and report ID checked against primary sources. The single highest-probability source of public takedown.

4. **Legal doctrine critique.** Every legal claim checked against ICJ, ICC, ICTY, ICTR jurisprudence. Especially: Akayesu standard for (b); Krstić for "in part" / "substantial part"; *Bosnia* ¶¶297–376 on dolus specialis; *Croatia* ¶¶437–441 on alternative inferences; the purpose-based vs. knowledge-based intent debate; the plausibility-vs-merits distinction; the "fully conclusive" standard.

5. **Statistical / empirical critique.** Every figure cross-checked for methodology, confidence intervals, source reconciliation, and proper presentation. Lancet methodology debate handled fairly. Cross-source divergence (COGAT vs. OCHA, MoH vs. IDF) presented without slant.

6. **Framing / AI-detection / whitelist critique.** Reads from "how does this get dismissed by a sophisticated skeptic." Hunts for AI accent, paired parallels, banned-vocabulary slippage, headline framing biases, missing counter-evidence, ordering biases, whitelist-composition challenges (e.g. why HRW is in but JPost-affiliated scholars are not).

7. **Independent academic genocide-studies critique.** Engages from the IAGS / Bartov / Schabas / Heller / Ambos scholarly framework. Tests the report's legal reasoning against the most credible peer-reviewed scholarship on genocide intent inference.

## Round-by-round

### Round 1 — Adversarial Red Teams (7 parallel agents)

Each red team reads:
- The synthesis (`09_synthesis_output.md`)
- The executive brief (`10_executive_brief_output.md`)
- The relevant upstream evidence outputs (`01–08_*_output.md`)

Each red team produces a structured critique memo with:
- Executive summary of attack vector
- Severity-ranked findings (HIGH / MEDIUM / LOW)
- For each finding: location (section/line), claim being attacked, evidence/citation supporting the attack, recommended remediation
- Items considered and dismissed (test results — so triage knows what was tested)
- Overall assessment: would the report survive this attack? If publishing a takedown, what would the headline be?

Deliverables: 7 markdown critique memos (`11–17_redteam_*_output.md`).

### Round 2 — Triage (1 agent + my adjudication)

Triage agent reads all 7 memos. Outputs:
- Deduplicated finding list, sorted by severity and impact
- Cross-finding conflicts (where two red teams demand opposite changes — these need human adjudication)
- Remediation spec: what gets fixed, what gets reframed, what gets defended in place with rationale
- Per-finding routing: synthesis-only / brief-only / both

I review the spec and adjudicate contested calls before authorizing Round 3.

Deliverable: `18_triage_output.md` and my adjudicated final remediation spec.

### Round 3 — Remediation (2 parallel agents)

Synthesis reviser takes original synthesis + remediation spec + critique memos. Produces revised synthesis (`09_synthesis_v2.md`).

Brief reviser takes original brief + remediation spec + critique memos. Produces revised brief (`10_executive_brief_v2.md`).

Both revisers operate under the same style/sourcing rules. Brief reviser additionally constrained to remain within 2,000–2,800 words and stay consistent with the revised synthesis.

### Round 4 — Re-Attack (4 parallel agents)

The four Round 1 red teams whose critiques drove the most remediation re-attack the revised version. These are the citation/accuracy team, the legal doctrine team, plus the two political adversaries (pro-Israel and pro-Palestine) — selected because political adversaries will be the public-square critics on publication. Output: either "clean" or a fresh remediation list.

If Round 4 surfaces material new issues, a Round 4.5 remediation pass runs. If only minor, fixes go directly into Round 5.

Deliverables: `21–24_reattack_*_output.md`.

### Round 5 — Final Verification (1 agent)

Citation accuracy spot-check on every footnote. Style compliance scan (em dashes, banned vocab, AI accent). Publishability check including: cover page conformance, internal consistency between synthesis and brief, determinations matrix coherence, no broken cross-references. Output: green-light with no fixes, or specific fix list.

Deliverable: `25_verification_output.md`.

## Sequencing and time

Sequential phases: 1 → 2 → 3 → 4 → 5. Within each phase, agents run in parallel.

Estimated wall time: 4–8 hours total. Round 1 is the longest (7 parallel agents, each 30–90 min). Round 3 is the most context-heavy (revisers need to ingest all critiques + original + remediation spec). Rounds 4 and 5 are faster.

## Total agent count

15 agents minimum (7 + 1 + 2 + 4 + 1). +2 if a Round 4.5 remediation pass is needed.

## After completion

Publish to wikiclaws:
- Revised full integrated review
- Revised executive brief
- All 10 original handoff briefs
- All 15+ adversarial handoff briefs
- All Round 1 critique memos (so readers can see what was tested)
- The triage and remediation spec (so readers can see how each critique was handled)
- The Round 5 verification report

This makes the published method auditable end-to-end. Anyone can rerun the adversarial review and check whether the response was adequate. That is the wikiclaws differentiator.

## What could go wrong, and the mitigation

1. **Red team collusion** (similar prompts produce similar critiques). Mitigation: each red team gets a distinct attack vector and reads only the report + relevant upstream outputs, not other red teams' work.
2. **Triage misses high-severity items.** Mitigation: my review step before Round 3, with the original 7 memos available.
3. **Reviser over-corrects** (introduces new errors or weakens evidentiary record). Mitigation: Round 4 re-attack catches regressions.
4. **Style drift across revisions.** Mitigation: Round 5 verification scan.
5. **New evidence post-cutoff not captured.** Accepted limitation; report is dated and methodology is published.
6. **Reviser introduces partisan tilt under pressure of one-sided critique.** Mitigation: revisers see all critiques across attack vectors, not just one. Triage spec is symmetric.
7. **Adversarial review produces a less rigorous output via lowest-common-denominator hedging.** Mitigation: triage agent's instruction explicitly rejects this. Defensive hedging is not the goal; calibrated truth is.

## What this is not

- Not infinite review. Five rounds, then publish. Additional rounds have diminishing returns and risk introducing rather than catching errors.
- Not consensus among red teams. Some red teams will demand contradictory changes. Adjudication resolves these explicitly.
- Not a guarantee of zero criticism. The published report will still be attacked. The bar is: every attack has been anticipated, the strongest version of each has been tested, and the response is defensible.
