# Handoff: Harness to Assess Test-Design Options

**To:** Adnan
**From:** the personality-theory authors (with Steven Pham)
**Subject:** Build a harness that evaluates the options for designing an assessment that measures
personality, intelligence, and AI fitness, either as one integrated test or as separate tests.
**Status:** framework for the personality construct is drafted; intelligence and AI fitness are not
yet scoped. This handoff is the brief, not the answer.

---

## 1. What we need from you

We do not need you to build the test. We need a rigorous, decision-ready analysis of **how the test
should be architected**, produced by a harness you design and run. The single decision the harness
exists to inform is:

> Should personality, intelligence, and AI fitness be measured by one integrated instrument, by
> three separate instruments, or by a modular battery that shares administration but scores
> separately?

Everything else in this brief is the context and the constraints that decision has to respect. The
output is an options analysis with a recommendation, not a built product.

## 2. Why a harness is the right tool here

This is a design-exploration problem with several independent constructs, several candidate
architectures, and hard adversarial constraints (psychometric validity, fairness on minors,
defensibility to an academic reviewer, commercial fit). That is a good fit for a fan-out of
exploratory agents followed by an adversarial critique pass and a synthesis, which is the pattern
already used elsewhere in this repository. We are explicit about this because the authors do not
reach for a harness by default; here it earns its place.

## 3. The three constructs

### 3a. Personality (drafted)

A four-system framework already exists in this repository under `book/`. Read it first; the spine
is `book/00_architecture.md`. The four systems:

1. **Social energy economy** (energy gain, game choice, risk appetite).
2. **The thinking machine** (cognitive sourcing internal/external, method formal/informal, observed
   under fast and slow elicited conditions, with stakes as a modulator; output is two graphs of
   reliance, not a score).
3. **Emotional and social disposition** (agreeableness/confrontation, introspection/situational
   awareness, emotional stability under load).
4. **Objectives** (open-prompt motivation coded to five motives: order and peace, triumph, power
   and influence, truth-seeking, novelty).

Three properties of this framework are load-bearing and the harness must not quietly violate them:

- **Preference, not ability.** Personality here measures what a person prefers or tends to do,
  never what they are capable of. This is the deliberate line that keeps personality distinct from
  intelligence.
- **AI-liaisoned.** Administration may use an AI to present adaptive scenarios and to code
  free-text responses, provided the coding is auditable and bias-checked.
- **De novo presentation, but lineage acknowledged internally.** The manuscript does not name
  existing typologies; we are not naive about them. The harness should map our constructs to the
  established literature internally so we do not relabel known constructs.

### 3b. Intelligence (not built, deliberately)

Intelligence concerns **capacity**: what a mind can do. There is a large, mature literature and
many validated instruments. We have deliberately not built an intelligence measure and we may not
need to build one from scratch. The harness should treat this as a build-versus-adopt question:
whether to license or adapt an established measure, build a bespoke one, or omit a formal
intelligence score in favor of a lighter proxy. Whatever it recommends, the capacity-versus-
preference distinction from the personality framework has to survive.

### 3c. AI fitness (undefined, greenfield, highest risk)

This construct does not yet exist and is the most important thing for the harness to pin down
before anything else. **Defining AI fitness is the first task, not an input.** Our working
hypothesis, to be confirmed or replaced by the harness, is that AI fitness is a person's aptitude
and disposition for working productively with AI in study and work. Candidate sub-dimensions, all
provisional:

- Effective delegation to and direction of AI tools (a skill).
- Judgment about when to trust, verify, or override AI output (a skill plus a disposition).
- Metacognition about one's own and the model's limits.
- Willingness and speed of adoption of new AI tools (a preference, closer to personality).
- Adaptability as tools change underneath the user.

Note the tension already visible: AI fitness appears to be a **hybrid of ability and preference**,
which straddles the clean line we drew between personality and intelligence. How to handle that
hybrid is a central question, not a footnote. The harness must produce a defensible definition and
say honestly which parts are capacity, which are preference, and what that implies for where AI
fitness sits relative to the other two constructs.

## 4. The architecture options to evaluate

At minimum, score these three. Add others if the harness surfaces them.

- **Option A, one integrated test.** Single sitting, single instrument, combined report. Pro:
  coherent experience, shared scenarios. Con: mixes a preference measure with a capacity measure,
  which is psychometrically awkward and invites the criticism that the personality portion is
  contaminated by an implicit ability test.
- **Option B, three separate tests.** Independent instruments, independently validated. Pro: clean
  construct separation, each defensible on its own terms. Con: longer total burden, weaker
  cross-construct story, harder commercial packaging.
- **Option C, modular battery.** Shared administration shell and shared scenario material where it
  is honest to share, but separate scoring models and separately reported constructs. Pro:
  preserves construct separation while keeping one user experience. Con: more engineering, and the
  shared-material temptation can leak one construct into another's score.

The deepest issue running through all three is **whether a preference measure (personality), a
capacity measure (intelligence), and a hybrid (AI fitness) can share an instrument without
contaminating each other.** The harness should treat that as the crux.

## 5. Constraints every option must satisfy

- **Population:** high school students, college students, and young people entering the workforce.
  Age-appropriate content, plain reading level, and content validity for people with thin work
  history.
- **Consequential use on minors:** the test will inform real decisions about young people. Fairness
  across demographic groups and a clear statement of what each score may and may not be used for
  are first-order requirements, not polish.
- **AI-administered and AI-scored where appropriate:** must be auditable. A reviewer will ask how
  reliably an AI codes free text and whether that coding is biased by writing ability, language, or
  culture. Have an answer.
- **Defensible to a second opinion:** the whole design is going to an academic, cognitive
  scientist, or psychologist for review. Build for that audience. The known objections we already
  expect are listed in `book/00_architecture.md` under "Expected objections"; do not rediscover
  them, extend them.
- **Commercial fit:** there is a company behind this assessing the populations above. Total testing
  time, report legibility, and packaging are real constraints, not afterthoughts.

## 6. Decision criteria (score every option against these)

1. Construct validity and, critically, **discriminant validity** (do the three constructs come
   apart, or does one bleed into another).
2. Defensibility to an academic reviewer.
3. Fairness and appropriateness for minors and young adults.
4. Feasibility and auditability of AI administration and scoring.
5. Respondent burden (time, fatigue, comprehension).
6. Engineering and operational cost.
7. Commercial and reporting fit.

A recommendation that wins on commercial fit but fails discriminant validity is not a
recommendation. Rank criteria 1 through 4 above 5 through 7 when they conflict.

## 7. Deliverables

1. **A defined construct for AI fitness**, with sub-dimensions and an explicit account of which are
   ability and which are preference.
2. **An options matrix**: Options A, B, C (and any others) scored against the criteria in section 6,
   with reasoning, not just scores.
3. **A recommendation** with its rationale and its main risks stated plainly.
4. **A validity and fairness plan** sketch for the recommended option: what would have to be tested,
   on whom, to defend it.
5. **A list of what to put in front of the academic reviewer**, framed as questions, so the second
   opinion is used well.

## 8. Recommended harness shape (a starting point, override as you see fit)

Mirrors the parallel-build, adversarial-critique, synthesize pattern in this repository.

- **Phase 1, construct definition (parallel).** One agent per construct: personality (summarize and
  pressure-test the existing framework against the literature), intelligence (build-versus-adopt
  landscape), AI fitness (define it). AI fitness is the long pole; give it the most room.
- **Phase 2, architecture options (parallel).** One agent per option (A, B, C, plus any the
  Phase 1 agents surface), each developing the option against all seven criteria.
- **Phase 3, adversarial review (parallel).** Independent critics, each with a distinct lens: a
  psychometrician on validity and discriminant validity; a fairness reviewer for the young and
  diverse population; a dual-process skeptic for the thinking-machine portion; a product and
  commercial lens. Each tries to break the options, not bless them.
- **Phase 4, synthesis.** Reconcile, score, recommend, and produce the deliverables in section 7.

Keep construct separation honest throughout: the fastest way for this to fail is for an agent to
let intelligence leak into the personality score, or for AI fitness to absorb both.

## 9. Open questions to confirm with the authors

These are unresolved and the harness should not silently assume them away:

- The exact definition and scope of AI fitness (section 3c). This is the biggest open item.
- Whether a formal intelligence score is wanted at all, or a lighter proxy suffices (section 3b).
- The intended use and stakes of the scores for the company's populations, which drives the
  fairness bar.
- Whether "preference, not ability" is a hard constraint on the whole battery, or only on the
  personality portion, given that intelligence and AI fitness both involve ability.

## 10. Source material

- `book/00_architecture.md` — the personality framework's spine, axioms, cross-system links, and
  expected reviewer objections. Read this first.
- `book/01_introduction.md` through `book/05_objectives.md` — the four systems in full.
- `book/README.md` — index and current status.
