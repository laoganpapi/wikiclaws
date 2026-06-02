# AI Collaboration Norms

**Project:** Collatz + Frankl research project
**Authors:** Alex Ye with Claude
**Last verified:** 2026-06-02

This document records current (2024–2026) norms for disclosing AI assistance in mathematics papers, then prescribes the concrete disclosure language we will use.

The summary of the field as of mid-2026: **AI assistance is no longer fringe; disclosure is mandatory at major venues; AI cannot be listed as an author**. The remaining open question is how detailed the disclosure must be, and what counts as "substantive" vs. "copy-editing" use.

---

## 1. Precedents — how recent AI-assisted math papers credit AI

### 1.1 AlphaProof and AlphaGeometry (DeepMind, Nature)

- **AlphaGeometry**: Trinh, Wu, Le, He, Luong, "Solving olympiad geometry without human demonstrations," *Nature* 625, 476–482 (Jan 2024). Authors are human researchers at Google DeepMind and NYU. AlphaGeometry is described as a system in the paper; not a co-author.
- **AlphaProof / AlphaGeometry 2**: Hubert et al., "Olympiad-level formal mathematical reasoning with reinforcement learning," *Nature* 651, 607–613 (2025). Same pattern: human authors; the system is the subject of the paper.

**Pattern:** When the AI *is* the research artifact, authors are humans; system is described in Methods. No paper to date in a top math venue lists an AI as author.

### 1.2 FunSearch (Romera-Paredes et al., Nature 2024)

- Citation: Romera-Paredes, Barekatain, Novikov, Balog, Kumar, Dupont, Ruiz, Ellenberg, Wang, Fawzi, Kohli, A. Fawzi, "Mathematical discoveries from program search with large language models," *Nature* 625, 468–475 (Jan 2024), DOI 10.1038/s41586-023-06924-6.
- Substance: an evolutionary loop pairing an LLM with an evaluator discovered new constructions for the cap-set problem and online bin-packing. These are **new mathematical results** that improved on best-known constructions.
- Authorship: 12 human authors. The LLM (a code-generating model) is described in Methods; not a co-author.
- The cap-set construction stands as a verified mathematical object — once produced, the result is human-verifiable independently of how it was found.

**Pattern:** When an AI system discovers a verifiable mathematical object, authors disclose the system in Methods, describe the search procedure, and include code. The mathematical fact is then human-verifiable, which protects the publication.

### 1.3 Terence Tao on AI-assisted math (blog, articles)

- Tao's running blog ("What's new") and his January 2025 article in the *Notices of the AMS* ("Machine-Assisted Proof") describe current AI as "a mediocre but not completely incompetent graduate student" (Sep 2024) revised by 2026 to "ready for primetime in math and theoretical physics."
- Tao formalized parts of the Polynomial Freiman-Ruzsa conjecture in **Lean** in 2023, with collaborators. The formalization is described in the paper / preprint and on the blog.
- In late 2024 Tao launched a collaborative "equational theories" project using ATPs, AI, and Lean to map implications between 4694 magma equational laws — explicitly multi-tooling.
- The Math Inc. "Gauss" formalization of the strong PNT in Lean (Jan 2024–Mar 2024) is publicly credited and discussed.

**Pattern:** Tao discloses AI use openly, names the model class, and treats the AI output as needing the same proof verification as any other contribution. He explicitly does not list AI as a co-author.

### 1.4 arXiv policy (2024–2026)

As of December 2025 and reinforced January 2026, arXiv mathematics:

- Endorsement: institutional email is no longer sufficient for first-time math submissions; an existing arXiv math author must endorse.
- AI-generated content: arXiv imposes an immediate **1-year submission ban** on authors when there is "incontrovertible evidence" that LLM-generated content was not checked — examples cited include hallucinated references, plagiarized content, and factual errors traceable to an LLM.
- The policy was prompted by a study (Zhao, Ginsparg et al.) finding ~150,000 hallucinated references across arXiv papers in 2025, climbing to ~1 in 277 papers in early 2026.

**What this means for us:** Every reference we cite must be hand-verified to exist. Every theorem we attribute must be sourced. The verification protocol (see `verification_protocol.md`) is the gate before any arXiv push.

### 1.5 Major journal policies

**Elsevier (JCTA, JCTB, Discrete Math, JNT)** — updated Sep 2025:
- Authors must disclose generative AI use in a dedicated section in the manuscript, placed before the references list, naming tool, version, and procedure(s).
- A declaration is also required at submission.
- AI tools cannot be authors or co-authors.
- AI cannot be used to fabricate data, results, or references.
- Reviewers are prohibited from using generative AI for evaluation.

**Springer Nature (Combinatorica and related)**:
- AI cannot be an author/co-author; human authors retain full responsibility.
- AI use must be documented in Methods.
- AI-assisted copy-editing (readability/style/grammar) is exempt from disclosure.
- AI-generated images are not permitted.
- Reviewers should not upload manuscripts to generative AI tools.

**Annals of Mathematics**:
- Does not consider papers generated using AI products.
- For human-authored papers that use AI as a tool: any use of AI/LLM must be declared as supplemental information, including extent and purpose.
- Only individuals who can take full responsibility may be authors.

**Taylor & Francis (Experimental Mathematics)**:
- Follows publisher-level policy: AI use must be disclosed in the manuscript and at submission.

**AIMS (DCDS), IMPAN (Acta Arithmetica), MSP venues**:
- No formal AI-specific policy published as of 2026-06; we default to disclosure in acknowledgments at the level we already apply.

---

## 2. Open questions in the norm space (2026)

These are still being negotiated by the field; flagged so we don't pretend they're settled:

1. **What level of AI use counts as "substantive"?** Elsevier and Springer agree that grammar/style fixes are exempt; substantive content creation must be disclosed. But "substantive" is undefined for tasks like literature review, conjecture generation, proof drafting, and error-finding. We will disclose all of these by default.
2. **Should the specific model and version be cited?** Best practice (FunSearch, Tao's blog) cites the model class; some venues now request the exact version (e.g., "Claude Opus 4.7" with date). We will cite the model and date.
3. **Is "co-pilot" framing accurate?** Field consensus tends toward "yes, AI is a tool; human is responsible." We will adopt the tool framing — Alex Ye is the responsible author.
4. **Lean formalization as evidence**: when a result is formalized in Lean, the proof object is independently checkable. This is becoming the gold standard for AI-assisted proofs (Tao, Math Inc., DeepMind). Where feasible we will formalize.

---

## 3. Concrete disclosure language (drop-in)

The following paragraph goes into the **Acknowledgments** section of every paper we submit. It is calibrated to satisfy the strictest of the policies surveyed (Elsevier's Sep-2025 update + Nature's policy + arXiv's anti-slop stance) and exceeds the minimum disclosure required by Springer, IMPAN, AIMS, and T&F.

For Elsevier and T&F venues, the disclosure also appears in a dedicated section before the references; the Acknowledgments paragraph can be reused verbatim there.

### 3.1 Standard paragraph

> **Use of AI assistance.** This research was conducted by Alex Ye in substantive collaboration with Anthropic's Claude (model: Claude Opus 4.7, 1M-context variant, accessed via the Claude Code agent SDK during the period 2026-05 to 2026-XX). Claude was used for: literature review and source synthesis; conjecture generation; proof drafting and counter-example search; computational scripting; LaTeX preparation; and adversarial red-team review of the manuscript's claims. Every mathematical claim in this paper, every cited reference, and every numerical result has been independently verified by Alex Ye and (where feasible) by Lean 4 formalization of the core lemmas. Claude is not listed as an author because authorship implies legal and ethical responsibility for the contents of the paper, which only a human can carry. Alex Ye is responsible for all errors. The choice of problem, the high-level research strategy, the final decisions about what to include, and the manuscript as published reflect Alex Ye's judgment.

### 3.2 Short variant (when space is tight)

> **Use of AI assistance.** This work was carried out by Alex Ye in collaboration with Anthropic's Claude (Opus 4.7, 1M-context) used as a research assistant for literature review, computation, proof drafting, and red-team review. Every claim was independently verified; core lemmas were formalized in Lean 4 where feasible. Claude is not an author; Alex Ye is responsible for all errors.

### 3.3 Dedicated section variant (for Elsevier venues that require a section before the references)

```
\section*{Declaration on the use of generative AI and AI-assisted technologies}

In the preparation of this work the author (Alex Ye) used Anthropic's Claude
(model: Claude Opus 4.7, 1M-context variant, accessed via the Claude Code
agent SDK) for the following tasks: literature search and synthesis;
generation of candidate conjectures and constructions; drafting of proofs;
adversarial review of intermediate results; computational scripting; and
LaTeX preparation. After using this tool, the author reviewed and edited the
content as needed, independently verified every mathematical claim and every
cited reference, and (where feasible) formalized core lemmas in Lean 4. The
author takes full responsibility for the content of the publication.
```

This wording is adapted from Elsevier's recommended template; we have added the verification and Lean formalization commitments, which exceed the minimum.

### 3.4 What we will NOT do

- We will **not** list Claude as an author.
- We will **not** cite Claude as the proof of any claim. Claude is the assistant; the proof stands or falls on its own.
- We will **not** use AI to fabricate references. Every citation is checked against the actual paper.
- We will **not** use AI-generated figures or images that are not directly produced from data we computed.
- We will **not** rely on AI to perform peer review of others' work.

---

## 4. Internal policy (for this project's agents)

This is binding on every agent in the project, in addition to the venue norms:

1. **Citation verification.** Every reference an agent adds to the bibliography must be marked verified by the agent (the agent reads the abstract/intro and confirms the claim, or marks the reference as "unverified — needs human check").
2. **No hallucinated authors, titles, journal names, or DOIs.** If unsure, the agent searches the web and confirms; if still unsure, the citation is dropped.
3. **Claim provenance.** Every theorem the project uses must trace to either: (a) a verified cited paper, (b) a proof in our own files that has passed the verification protocol, or (c) is marked explicitly as a *conjecture* / *work in progress* / *unverified*.
4. **Acknowledgments boilerplate.** Every draft includes the paragraph from section 3.1 from the first commit. We do not "add it later."
5. **AI use log.** A running log of substantive Claude sessions is kept in `shared/ai_use_log.md` (one line per session: date, agent, task, outcome). This is for our records, not for publication, but it lets us re-check the disclosure paragraph's claims if questioned.
6. **Lean as gold standard.** Where a result is central to the paper and formalizable in reasonable effort, it gets a Lean 4 statement and proof. See `verification_protocol.md` step 3.

---

## 5. Sources

- [Mathematical discoveries from program search with large language models (FunSearch, Nature 2024)](https://www.nature.com/articles/s41586-023-06924-6)
- [Olympiad-level formal mathematical reasoning with reinforcement learning (AlphaProof, Nature 2025)](https://www.nature.com/articles/s41586-025-09833-y)
- [Mathematicians put AI model AlphaProof to the test (Nature commentary)](https://www.nature.com/articles/d41586-025-03585-5)
- [Terry Tao — Machine-Assisted Proof (Notices of the AMS, Jan 2025) — and blog tag](https://terrytao.wordpress.com/tag/machine-assisted-proof/)
- [Tao: AI is ready for primetime in math and theoretical physics (OpenAI Academy, Mar 2026)](https://academy.openai.com/public/blogs/terence-tao-ai-is-ready-for-primetime-in-math-and-theoretical-physics-2026-03-06)
- [arXiv blog: ban for unchecked AI content (Times Higher Education coverage)](https://www.timeshighereducation.com/news/ban-authors-submitting-ai-content-welcome-unenforceable)
- [arXiv blog: 404 Media coverage of the 1-year ban policy](https://www.404media.co/new-arxiv-rules-ai-generated-papers-ban/)
- [arXiv blog: updated endorsement policy for arXiv mathematics (Dec 2025)](https://blog.arxiv.org/2025/12/10/updated-endorsement-policy-for-arxiv-mathematics/)
- [Elsevier policy: use of generative AI and AI-assisted technologies in writing](https://www.elsevier.com/about/policies-and-standards/the-use-of-generative-ai-and-ai-assisted-technologies-in-writing-for-elsevier)
- [Elsevier policy: use of generative AI in the review process](https://www.elsevier.com/about/policies-and-standards/the-use-of-generative-ai-and-ai-assisted-technologies-in-the-review-process)
- [Springer Nature: AI guidance for researchers](https://group.springernature.com/gp/group/ai/ai-guidance-for-our-researchers-and-communities)
- [Springer Nature editorial policies](https://www.springernature.com/gp/policies/editorial-policies)
- [Annals of Mathematics submission guidelines](https://annals.math.princeton.edu/submission-guidelines)
- [JCTA Guide for Authors (ScienceDirect)](https://www.sciencedirect.com/journal/journal-of-combinatorial-theory-series-a/publish/guide-for-authors)
- [AI Policies in Academic Publishing 2025: Guide & Checklist (third-party summary)](https://www.thesify.ai/blog/ai-policies-academic-publishing-2025)
