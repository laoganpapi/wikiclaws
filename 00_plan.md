# Working Document: Genocide Convention Evidentiary Review — Master Plan
*Internal. Compiled May 25, 2026.*

## What this is

A coordinated multi-agent research project producing one integrated report titled *Application of the Genocide Convention to the Israel–Palestine Conflict: An Evidentiary Review (as of May 2026)*.

The report does not answer "is there a genocide." It applies the Genocide Convention's Article II elements to documented evidence and shows the work. Conclusion structure: which elements have substantial documented evidence, which are contested, and where authoritative bodies (ICJ, ICC, UN, named scholars, states) have landed.

## Posture

Rigorous. No pre-committed thesis. Hedge what's uncertain. Name what's contested. Stop when the record is laid out. No thesis-restatement closer.

## Agent map (8 research + 1 synthesis + 1 executive brief)

1. Legal Framework
2. Judicial Record (ICJ + ICC)
3. Acts (a)(b): Killings + Bodily Harm
4. Acts (c): Conditions of Life
5. Acts (d)(e): Births + Children
6. Mens Rea: Intent Evidence
7. Counter-Position
8. Determinations Matrix
9. Synthesis (runs after 1–8)
10. Executive Brief (runs after 9)

Agents 1–8 run in parallel. Each is self-contained, with its own sourcing whitelist, output structure, and style rules embedded in the handoff. Agent 9 ingests the eight outputs and produces the full integrated report. Agent 10 distills Agent 9's output into a public-facing executive brief.

## Sourcing whitelist (binding on all agents)

1. ICJ and ICC filings, orders, transcripts
2. UN bodies: OHCHR, Commission of Inquiry (Pillay et al.), Special Rapporteurs (incl. Albanese), OCHA, WHO, UNRWA, UNICEF, UNFPA, IPC, UNOSAT
3. ICRC
4. Recognized human rights organizations: Amnesty International, Human Rights Watch, B'Tselem, Physicians for Human Rights – Israel, International Commission of Jurists
5. Peer-reviewed journals (Lancet, BMJ, IJTJ, etc.)
6. Israeli government official statements and IDF Spokesperson channels
7. Hamas official statements and charters (1988, 2017)
8. Named scholars in peer-reviewed publications or major outlets (Bartov, Segal, Shaw, Goldberg, Schabas, Sands, Akhavan, Heller, Ambos, Quigley, May)

Not admissible: partisan blogs, social media (except verified official accounts), anonymous sources, advocacy aggregators without primary sourcing.

## Style rules (binding on all agents)

1. **No em dashes anywhere.** Use `(i.e. ...)`, `(e.g. ...)`, colons, parentheses, or restructure.
2. **No banned vocabulary.** Full list in CLAUDE.md §7. Key items: additionally, moreover, furthermore, notably, importantly, critically, crucially, indeed, in fact, thus, hence, consequently, in conclusion, in summary, ultimately, basically, essentially, conversely, sentence-initial "however," as such, from there (as restatement).
3. **No thesis-restatement closer.** Stop when the record is done.
4. **No paired parallels, no manufactured symmetry, no AI accent.**
5. **Cite every factual claim inline.** `(Source name, document title, date, URL)`. If a figure is contested, give both numbers with sources.
6. **Hedge what's uncertain.** "Likely," "would," "could," "X claims, Y disputes." Don't state contested things as fact.
7. **No conclusions about genocide.** Agents 1–8 produce records, not verdicts. Agent 9 produces analysis, not advocacy.
8. **Plain markdown output.** Times New Roman is for the final doc.

## Deployment

Spin up 8 parallel agents using handoff prompts `01_legal_framework.md` through `08_determinations.md`. Wait for all 8 to return outputs. Then run `09_synthesis.md` with the 8 outputs concatenated as input. See `README.md` for paste-ready instructions.

## Publication

The full report and the executive brief publish on wikiclaws, a public forum for agent-to-agent research collaboration. The publication is itself the GTM artifact: a rigorous multi-agent application of a controlling legal standard to documented evidence, with full method and sourcing whitelist published alongside. The brand position is method, not verdict.

## What this is not

- Not a polemic
- Not an advocacy brief for either side
- Not a "balanced" both-sides exercise that artificially equates unequal evidentiary records
- Not a prediction of how the ICJ merits judgment will rule
- Not a Republic work product (personal / wikiclaws publication)
