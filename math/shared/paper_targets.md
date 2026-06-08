# Paper Targets

**Project:** Collatz + Frankl research project
**Authors:** Alex Ye with Claude
**Last verified:** 2026-06-02 (current journal policies cited inline)

This document fixes a target-venue strategy for each track. We are not committing to one venue at the outset; we are committing to writing each paper *to the standards of the highest-quality target* in its band, then submitting top-down.

The default plan is: **arXiv first** (math.CO for Frankl, math.NT primary + math.DS cross for Collatz), then journal submission. See section 5 for the arXiv-only backup.

---

## 1. Frankl Union-Closed (combinatorics)

### Primary candidates

| Venue | Publisher | Style | Typical length | Notes |
|---|---|---|---|---|
| Journal of Combinatorial Theory, Series A (JCTA) | Elsevier | Top-tier combinatorics; structural and enumerative | 20–40 pp typical | Best fit if we have a structural/extremal result. Strict AI disclosure required (see section 4). |
| Journal of Combinatorial Theory, Series B (JCTB) | Elsevier | Top-tier; graph theory + structural combinatorics | 20–40 pp | Frankl-flavored results have appeared; lower fit than A unless we get into graph-theoretic reductions. |
| Combinatorica | Springer / Bolyai Math. Soc. | Top-tier "central European" combinatorics | $\leq$ 30 pp in 11-pt LaTeX, US-letter, 1-in margins | Submission via EditFlow (`https://ef.msp.org/submit/combinatorica`). Strong fit for entropy-method papers. |
| Discrete Mathematics | Elsevier | Broad combinatorics; Contributions, Notes, Perspectives | Notes <15 pp; Contributions 15–40 pp; Perspectives = surveys | Workhorse venue. Less prestige than JCTA but faster, broader scope. |
| Electronic Journal of Combinatorics (E-JC) | Open-access OJS | Open-access, no APC | No hard cap; 20–40 pp typical | Must use the journal's LaTeX style file (`e-jc.sty`) and `ejc-sample.tex` template. Authors do final typesetting themselves. |

### LaTeX templates

- **JCTA / JCTB / Discrete Math:** Elsevier `elsarticle` class (LaTeX template on Overleaf and Elsevier's site). Cross-platform standard.
- **Combinatorica:** Springer LaTeX `svjour3` / EditFlow custom style; 11-pt main text.
- **E-JC:** `e-jc.sty` is mandatory at acceptance; authors typeset the final version.

### Submission processes

- **JCTA / JCTB:** ScienceDirect Editorial Manager. Disclosure of AI use is mandatory at submission and again in the manuscript (see section 4).
- **Combinatorica:** EditFlow (MSP) — PDF + cover letter + suggested referees optional.
- **Discrete Math:** Editorial Manager (Elsevier).
- **E-JC:** OJS platform at `combinatorics.org`; PDF for initial submission; LaTeX source upon acceptance.

### Expected review time

- **JCTA / JCTB / Combinatorica:** 6–18 months is normal for top-tier combinatorics. Plan on 12 months median; revisions can add another 6.
- **Discrete Math:** 4–9 months typical first round.
- **E-JC:** Generally faster than print venues; 3–9 months first round commonly reported.

### Track recommendation

- **If we produce a constant improvement** ($c^* > (3-\sqrt 5)/2$ with a new method): aim **JCTA** first; **Combinatorica** second; **Discrete Math** as third.
- **If we produce a strong survey + small refinements**: aim **Discrete Math (Perspectives)** or **E-JC**.

### arXiv

- Primary: **math.CO**.
- Cross-list: **math.IT** if entropy techniques are central; **math.PR** if probabilistic.

---

## 2. Collatz (number theory / dynamics)

### Primary candidates

| Venue | Publisher | Style | Typical length | Notes |
|---|---|---|---|---|
| Journal of Number Theory (JNT) | Elsevier | Three sections: JNT PRIME (long, complete proofs), General (shorter), Computational | PRIME: unrestricted long; General: 10–30 pp typical | Best fit if we have a clean number-theoretic result. PRIME explicitly welcomes long detailed papers. |
| Acta Arithmetica | IMPAN (Polish Academy of Sciences) | Classical pure number theory | No hard limit; 15–40 pp typical | Template: amsart or IMPAN article style; 12-pt, 13.5cm text width. Email submissions to `actarith@amu.edu.pl`. |
| Experimental Mathematics | Taylor & Francis | Formal results inspired by computation; conjectures with experimental support | 15–30 pp typical | Excellent fit if our work is computational + theoretical. Single-anonymous peer review; mean review time >12 weeks. |
| Discrete and Continuous Dynamical Systems (DCDS) | AIMS | Dynamical systems theory and methods | 20–40 pp typical | Strong fit if we frame Collatz as 2-adic dynamics or ergodic problem. Published by American Institute of Mathematical Sciences. |

### LaTeX templates

- **JNT:** Elsevier `elsarticle`.
- **Acta Arithmetica:** IMPAN provides `IMPAN-amsart.tex` and `IMPAN-article.tex` templates with style files.
- **Experimental Mathematics:** Taylor & Francis `interact` LaTeX class; templates on the journal site.
- **DCDS:** AIMS provides a custom LaTeX class file (on `aimsciences.org`).

### Submission processes

- **JNT:** Editorial Manager (Elsevier). Choose section (PRIME / General / Computational) at submission. AI disclosure required.
- **Acta Arithmetica:** PDF emailed to editorial office; TeX source on acceptance.
- **Experimental Mathematics:** T&F online Submission Portal; single-anonymous review.
- **DCDS:** AIMS submission system at `aimsciences.org`.

### Expected review time

- **JNT:** 6–12 months first round; PRIME section can be slower (longer papers).
- **Acta Arithmetica:** 6–12 months typical; can extend to 18+ months for involved papers.
- **Experimental Mathematics:** 3–6 months commonly; mean reported >12 weeks.
- **DCDS:** 4–9 months first round.

### Track recommendation

- **If we have a clean partial theorem** (e.g., a strengthening of Tao's almost-density bound): **JNT PRIME** first; **Acta Arithmetica** second.
- **If we have substantial computational results** (verification frontier extension, statistical invariants): **Experimental Mathematics** first.
- **If we have a dynamical / 2-adic structural result**: **DCDS** is the natural home; **JNT General** as backup.

### arXiv

- Primary: **math.NT**.
- Cross-list: **math.DS** (almost always relevant for Collatz dynamics).
- Cross-list: **math.PR** if statistical / random-model.
- Cross-list: **math.CO** only if a combinatorial reformulation drives the paper.

---

## 3. Quality bars to satisfy

We write to the *highest* bar in each track, regardless of where we submit:

- **Top combinatorics venues** require: clean exposition; explicit bounds; non-trivial improvement on a tracked frontier; complete proofs (no "details omitted").
- **Top number-theory venues** require: rigorous proofs of every claim; sharp constants where applicable; computational claims must include code or pseudocode and the verifying data.
- **Both** require: explicit comparison with prior art; clear statement of what is new; identification of where the bottleneck moves after our contribution.

---

## 4. AI assistance disclosure compliance per venue

See `ai_collaboration_norms.md` for the full template. Summary by publisher:

- **Elsevier journals** (JCTA, JCTB, Discrete Math, JNT): mandatory declaration at submission. A disclosure statement must appear in a dedicated section in the manuscript, placed before the references, naming the tool, version, and purpose. AI tools cannot be listed as authors. AI cannot be used to fabricate data, results, or references.
- **Springer journals** (Combinatorica): generative AI use must be documented (typically in Methods or Acknowledgments). AI-assisted copy-editing for readability/style is exempt from disclosure. AI cannot be listed as an author. AI-generated images not allowed.
- **AMS / IMPAN journals** (Acta Arithmetica): follow general academic norms; explicit disclosure in acknowledgments recommended.
- **Open-access venues** (E-JC): follow general academic norms; explicit disclosure recommended in acknowledgments.
- **AIMS** (DCDS): no published formal policy specific to AI as of 2026-06; default to disclosure in acknowledgments and at cover-letter level.
- **Taylor & Francis** (Experimental Mathematics): publisher policy requires disclosure of AI use in a section of the manuscript and at submission.

**Hard rule for our project:** Our acknowledgments section will name Claude (Anthropic), specify the model identifier where known, and describe the scope of AI assistance, on every submitted manuscript regardless of whether the venue formally requires it. See `ai_collaboration_norms.md` for the boilerplate paragraph.

---

## 5. Backup: arXiv-only release, journal later

If we are not ready to commit to a journal — or if the result needs community vetting first — the default fallback is:

1. **arXiv release** with full disclosure in acknowledgments.
2. **Public claim** is the arXiv paper. We are then bound by it: any revision must update arXiv before the journal version.
3. **Journal submission** when the result has held up for 4–8 weeks post-arXiv (no errata, no major prior-art collisions).

arXiv release standards (which are *higher* than venue minimums on some axes):

- Endorsement: as of Dec 2025, arXiv math no longer accepts institutional email alone as the qualifier; we will need a human endorser in math.CO and/or math.NT. Plan: Alex secures the endorser before any post is attempted.
- AI content: as of 2025, arXiv imposes a 1-year submission ban for "incontrovertible evidence" of unchecked LLM output (e.g., hallucinated citations). Every reference in the bibliography must be hand-verified. Every claim must trace to a real source. This is non-negotiable.
- LLM-generated mathematical claims: must be fully proved, not just LLM-suggested. The verification protocol (see `verification_protocol.md`) is the gate.

If a result is too speculative for either arXiv or a journal, it goes in `dead_ends.md` or a `notes/` directory, not in public release.

---

## 6. Decision tree (when ready to release)

```
Do we have a complete, verified theorem?
├── Yes
│   ├── Frankl-side improvement in c^*?           --> JCTA, then Combinatorica
│   ├── Collatz partial result (density/stopping)? --> JNT PRIME, then Acta Arithmetica
│   ├── Strong computational + theoretical?        --> Experimental Math (Collatz) /
│   │                                                  E-JC (Frankl)
│   └── 2-adic / dynamical Collatz framework?      --> DCDS
└── No (survey + small observations)
    ├── Frankl  --> Discrete Math (Perspectives) or E-JC
    └── Collatz --> Experimental Math or arXiv-only
```

In every branch: arXiv post precedes journal submission.

---

## 7. Sources

- [Journal of Combinatorial Theory, Series A — Guide for Authors (ScienceDirect)](https://www.sciencedirect.com/journal/journal-of-combinatorial-theory-series-a/publish/guide-for-authors)
- [Combinatorica home page](https://combinatorica.hu/)
- [Combinatorica EditFlow submission](https://ef.msp.org/submit/combinatorica)
- [Electronic Journal of Combinatorics — Submissions](https://www.combinatorics.org/ojs/index.php/eljc/about/submissions)
- [Acta Arithmetica — Information for Authors (IMPAN)](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/information-for-authors)
- [Journal of Number Theory — Guide for Authors (ScienceDirect)](https://www.sciencedirect.com/journal/journal-of-number-theory/publish/guide-for-authors)
- [Experimental Mathematics — Taylor & Francis Online](https://www.tandfonline.com/journals/uexm20)
- [Discrete and Continuous Dynamical Systems — AIMS](https://www.aimsciences.org/)
- [Elsevier policy: use of generative AI in writing](https://www.elsevier.com/about/policies-and-standards/the-use-of-generative-ai-and-ai-assisted-technologies-in-writing-for-elsevier)
- [Springer Nature: AI guidance for researchers](https://group.springernature.com/gp/group/ai/ai-guidance-for-our-researchers-and-communities)
- [arXiv blog: updated endorsement policy for math (Dec 2025)](https://blog.arxiv.org/2025/12/10/updated-endorsement-policy-for-arxiv-mathematics/)
- [arXiv blog: updated endorsement policy (Jan 2026)](https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/)
