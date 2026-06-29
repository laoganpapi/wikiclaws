# Architecture and Working Spine

This is the working document for the framework, not part of the manuscript. It records the
decisions that govern the theory, the template every system follows, and the register of systems
we have adopted or are still considering. Edit this first when a decision changes; the chapters
follow from it.

## Authors

A new theory of personality. With Steven Pham.

## Deliverable sequence

1. A working paper that sets out the framework (current focus).
2. A formal, AI-enabled assessment built on the framework.
3. A second opinion on both from an academic, cognitive scientist, or psychologist.

The assessment is for a company evaluating high school students, college students, and young
people entering the workforce. Two consequences follow and bind the writing:

- **Operationalizable.** Every measure must be administrable. A later instrument should read a
  system's chapter and know what it asks a person and what it does with the answer.
- **Defensible to an expert.** The framework is going to a trained reviewer. Where a measure
  brushes against an established construct or a contested theory, the chapter must say so plainly
  and state our position, rather than hope the reviewer does not notice. A list of the objections
  we expect is kept at the end of this document.

Because the population is young and the use is consequential, age-appropriate items, plain
reading level, and fairness across groups are first-order design constraints, not later polish.

## Core definitions

- **Personality** is a set of preferences, stated or revealed, that govern how an individual
  makes decisions and responds to any and every stimulus in their conscious existence.
- Personality is **not static**. Experience and environment change it. The theory measures a
  person at a time, not for life.
- The theory is **agnostic to nature versus nurture**. The origin of a preference does not change
  what the preference is or how it operates now.
- Personality is **distinct from intelligence**. Intelligence concerns capacity. This theory
  concerns preference. See the amended axiom below for the one place we deliberately cross this
  line, and why.

## Design axioms

1. **Preference, not ability (with one deliberate exception).** Most systems record what a person
   prefers to do, not what they are capable of doing. This is the line separating the framework
   from intelligence research. The Thinking Machine (System 2) is the deliberate exception: to
   tell its dynamic story we measure the *strength* of the fast and slow systems as well as the
   *preference* over thinking mode. Strength is capacity. We cross the line on purpose, we label
   it where we cross it, and we owe the reviewer an account of how slow-system strength is not
   simply fluid intelligence (see expected objections). Emotional competence (System 3) carries a
   milder version of the same tension.
2. **De novo.** The manuscript presents the theory on its own terms. It does not name, map to, or
   argue against existing typologies in the body. The one external name we do use is Kahneman's
   fast and slow systems, because System 2 builds on it directly and a reviewer would expect the
   lineage acknowledged. (Internal-only novelty notes are at the end.)
3. **Open and extensible.** The set of systems is not closed. We adopt new systems as we uncover
   them. The architecture must accommodate a system we have not yet written.
4. **Instrumentable and AI-liaisoned.** See the deliverable sequence. No measure without a
   conceivable administration, and the administration may use an AI to present adaptive scenarios
   and to code free-text responses, provided the coding is rigorous and auditable.
5. **Stated versus revealed.** Where stated and revealed preference diverge, the theory privileges
   revealed preference for prediction and treats the gap as itself informative.

## The system template

Every chapter that defines a system follows this structure. Uniformity is what makes separate
essays into one theory, and it is what the instrument will read.

1. **The phenomenon.** What part of decision and response this system governs.
2. **The measures.** The axes along which people vary, each defined by what you would observe.
   State whether each records preference or, where unavoidable, capacity.
3. **The decision rule.** How the measures resolve into an actual decision under a stimulus.
4. **The strategy or dynamic layer.** The behavior the system produces over time. For the Thinking
   Machine this is the central content, not an afterthought.
5. **Illustrations.** Two or three concrete profiles, distinct on this system alone.
6. **Open questions.** What is unresolved, so the next pass knows where to dig.

## System register

| # | System | Status | Governs |
|---|--------|--------|---------|
| 1 | Social energy economy | Adopted | How social interaction is fueled, chosen, and risked |
| 2 | The thinking machine | Adopted | Where, how, and how fast a person thinks, and how that moves under stakes |
| 3 | Emotional intelligence and social competence | Adopted | How a person attends to and acts on emotion, in self and others |
| 4 | Objectives | Adopted | What a person is oriented toward; the external cause |
| 5 | Neuroticism | Adopted | Baseline emotional stability and reactivity under pressure |

The set remains open. Candidates not yet adopted are logged in open questions.

## Measures by system (working list)

- **System 1, Social energy economy.** (a) Energy gain: the sources and rates that replenish
  social energy. (b) Game choice: which social interactions a person enters and invests in.
  (c) Risk appetite: willingness to stake social standing or capital on an interaction's outcome.
- **System 2, The thinking machine.** A plane defined by two axes plus a modal layer plus a
  modulator. Axis A: Internal versus External sourcing (reasoning from one's own theory and models
  versus from empirical data and the world). Axis B: Formal versus Informal method (rigorous,
  communicable frameworks versus non-rigorous thought such as visualization and simulation). Modal
  layer: the Fast system and the Slow system (Kahneman), each with a measured strength. Modulator:
  stakes, how much a person has to gain or lose. The output is a trajectory across the plane and
  between modes as stakes rise, not a single point.
- **System 3, Emotional intelligence and social competence.** (a) Agreeableness versus
  Confrontation: disposition to accommodate versus to contest. (b) Introspection versus
  Situational awareness: attention to one's own emotional state versus reading the emotional field
  of others and the situation.
- **System 4, Objectives.** An open prompt of what motivates a person, coded into a motive
  profile over: order and peace; triumph; control; power and influence; truth-seeking; novelty;
  validation and excellence. Multi-label with weights; people carry more than one motive.
- **System 5, Neuroticism.** Baseline emotional stability versus volatility and reactivity, and
  how reactivity changes under load.

## Cross-system links we have noticed

These are real and should be modeled, not hidden. They are also where a reviewer will probe
independence.

- **Neuroticism moderates the thinking machine's stake response.** High reactivity likely predicts
  faster collapse from slow to fast mode, or a sharper migration across the plane, as stakes rise.
  Neuroticism may be best read partly through System 2's trajectory.
- **System 2's Internal/External axis brushes System 3's Introspection/Situational awareness.**
  Boundary we are drawing: System 2 is cognitive sourcing for reasoning and decision (theory
  versus data); System 3 is emotional and social attention (one's own feeling versus reading
  others). Related, separable, discriminant validity to be demonstrated.
- **System 1's risk appetite is social and domain-specific; System 2's stakes is a general
  modulator of thinking mode.** Keep distinct; expect them to correlate.

## Expected objections (for the second opinion, and to pre-empt)

1. **Slow-system strength versus fluid intelligence.** If we measure how strong a person's slow
   system is, how is that not a working-memory or g measurement, which would collapse our
   distinction from intelligence? We need a preference-aware design: measure the *disposition to
   engage* the slow system and the *quality of mode-switching*, not raw deliberative horsepower.
2. **Dual-process theory is contested.** Kahneman's fast/slow framing has been criticized on
   replication and oversimplification grounds. The chapter should acknowledge this and state that
   we use it as a modeling layer for observed mode-switching, not as a claim about brain
   architecture.
3. **Discriminant validity across Systems 2, 3, and 5.** Internal/external, introspection, and
   neuroticism could be re-derivations of one or two underlying factors. We owe evidence, or at
   least a falsifiable claim, that they separate.
4. **AI coding of free text.** A reviewer will ask how reliably an AI codes a response as formal
   versus informal, or internal versus external, and whether that coding is biased by writing
   ability, language, or culture, especially in a young and diverse population.
5. **Consequential use on minors.** High-stakes assessment of high schoolers demands fairness
   evidence and a clear account of what decisions the score may and may not inform.

## Internal: novelty watch (NOT for the manuscript)

Kept only so we do not reinvent a known construct under a new name while building de novo. None of
this appears in the working paper.

- System 1 energy gain overlaps a known energy-direction axis; the differentiator is game choice
  and risk appetite. Keep those load-bearing.
- System 2's Internal/External and Formal/Informal axes brush a known perception axis and a known
  need-for-cognition construct; the differentiator is the dynamic trajectory under stakes and the
  orthogonal fast/slow layer. Keep the trajectory load-bearing.
- Systems 3, 4, and 5 run close to three well-known broad factors. De novo presentation is a
  stylistic choice, not a claim of unprecedented constructs; the reviewer will see the lineage, so
  our novelty must live in the measures and the cross-system dynamics, not in renaming.

## Style

- Declarative and precise. No em dashes. Semicolons, colons, commas, parentheses are fine.
- Define before you use. One definition per term, used consistently after.
- Unsettled claims go in Open Questions, not in the body as if settled.
