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
  concerns preference. We hold this line across every system, including the thinking machine, which
  measures reliance on kinds of thinking and not the strength of any of them.
- **Three lanes: preference, capability, pathology.** A person can be described along three
  separate lanes: preference (what they tend toward), capability (what they can do), and pathology
  (what is clinically wrong, if anything). This framework occupies the preference lane only. It
  does not measure capability (the province of intelligence and aptitude instruments) and does not
  measure pathology (the province of clinical assessment). Where a preference reading resembles
  data from another lane, the resemblance is not a claim. This scope statement belongs in the
  prologue, and every system inherits it.

## Design axioms

1. **Preference, not ability.** Every system records what a person prefers or leans toward, not
   what they are capable of doing. This is the line separating the framework from intelligence
   research, and it now holds everywhere. The Thinking Machine (System 2) is the place it was most
   at risk: an earlier draft measured the *strength* of the fast and slow systems, which is
   capacity. We retired that. The thinking machine measures *reliance*, which kind of thinking a
   person leans on given their mode and the stakes, and fast and slow are conditions we elicit, not
   strengths we score. System 3 was the other place at risk: an earlier draft framed it as
   emotional intelligence and social competence, which measures skill. We retired that too. System
   3 now measures stated or revealed preferences and tendencies in emotional and social situations,
   not how well a person performs in them. The preference-not-ability line now holds cleanly across
   every system.
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

## Purpose and validity stance

This framework is built for self-understanding, not prediction. It does not forecast what a person
will do, and it refuses that goal on principle. A predictive reading handed to a young person
tends to become self-fulfilling, and a measure that shapes the outcome it claims to foresee has
already surrendered the neutrality that made it worth trusting. The instrument's value is that it
gives the subject a structured account of their own tendencies, stated and revealed, to understand
in the pursuit of their own ends. The subject need not be able to predict themselves; they need
only understand what they want.

This choice reassigns the validity burden; it does not remove it.

- **Not criterion validity.** We make no claim that any metric predicts a job, grade, or life
  outcome, and no score may be used to select, hire, admit, rank, or screen out any person. Any
  such use is a misuse the framework disowns: the instrument was never built to predict.
- **No valence, no compliments.** Every metric is a neutral, bipolar observation of tendency,
  neither pole better than the other. The report carries no praise and no deficit language. This
  binds the stake response above all: a shift in thinking or emotional settings as stakes rise is a
  migration, not a degradation. Nobody is "collapsing under pressure"; they are changing
  instruments, and the change may serve them well or badly — a question this framework does not
  answer, because performance belongs to the capability lane. Words like collapse, degrade,
  volatile, and spike are barred from every system description and every report sentence.
- **The burden we carry is discrimination, not universality.** A neutral observation can still be
  near-universal ("sometimes you trust your gut, sometimes you deliberate") and feel personal while
  describing everyone. The instrument owes evidence that its readings discriminate: two different
  people receive meaningfully different profiles, and a person's own profile fits them better than a
  stranger's. This is smaller and more honest than prediction, and it is what the validation study
  must establish.
- **Nothing is valuable in a vacuum.** No single tendency is presented as the finding. The unit of
  insight is the configuration across systems and, above all, the stated-revealed gaps, which are
  computed from a person's own two data streams and so cannot be generic. The report must never
  hang an insight on one isolated tendency.
- **Descriptive, never prophetic.** Report language stays past-tense and about the session: "here
  is how your thinking moved today, when it counted," never "under pressure you will retreat to your
  models."
- **Clean or silent (hard rule).** No difference score (any stated-revealed gap) and no slope (any
  stake-response) is shown unless it clears a pre-specified reliability threshold. Below the
  threshold the report shows nothing on that reading, or says "no clear gap" / "no clear shift." It
  never displays a shaky number softened by a caveat. A reading the instrument cannot stand behind
  does not appear. This is a hard constraint on the report, not a preference.
- **The gap is a starting point, not a verdict.** Self-reported preference often conflicts with
  revealed behavior, because what a person wants or believes they are differs from what the evidence
  shows. That is expected and carries no judgment. The stated-revealed gap is the most actionable
  reading in the report: it is the distance between the self a person wants and the self their
  behavior reveals, and because people are plastic and trainable, that distance is movable. A person
  who wants to think or act differently can be helped to train toward it. This makes reliability a
  safeguard for the person, not a formality: a gap may be reported, and may become a training
  target, only when it clears a stated reliability bar, because training someone to close a gap that
  was measurement noise asks them to change themselves to fix a phantom.

## Permitted and prohibited uses (per metric)

The self-understanding stance is enforced metric by metric, not only in principle. Every score
carries a use label with the same normative weight as the system register. The default for all
metrics is developmental and reflective use by the subject. On top of that default, the following
metrics are barred outright from any use that sorts, ranks, screens, places, selects, hires, or
admits a person, whether by a school, an employer, or the assessing company itself:

- **Social risk tolerance** (System 1)
- **Reactivity under load** and **Baseline stability** (System 3)
- **Every stated-revealed gap** and the cross-cutting divergence metric

These are the readings most open to misuse against a young person and least defensible as selection
inputs. Their prohibition is a framework obligation, not implementer discretion. No such metric may
be exported, aggregated, or written to a student information system for a sorting purpose. The
prohibition holds regardless of intent, because any delivered number tends to drift toward the
decision it can influence.

**Distribution and custody.** The assessment is offered only inside the venture's own program.
Results are never disclosed to schools or employers; there is no institutional copy. The subject
holds the report and controls any sharing; minors' results expire after 18 months and are never
written to a permanent record. The readings carry no signal about what a person is good at, only
what they tend to like and dislike, which caring parents and teachers already infer constantly and
noisily; the instrument formalizes that inference, and a formalized inference needs a custody rule
an informal one does not. Inside the program, readings may tailor and offer — never deny, rank, or
gate. Preference data may open doors suited to a person's leanings; it may not close one.

A second bar, on the pathology lane. **Reactivity under load** and **baseline stability** (System 3)
carry a further prohibition: they may not be used to diagnose, screen for, or flag any
mental-health condition. Their behavioral signature resembles what a clinician reads as a symptom,
but this framework measures preference, not pathology (see the three-lane scope), and a preference
reading is not a clinical one. The report states these as dated, session-scoped observations ("on
the higher-stakes items today, your settings shifted"), never as a trait label or a diagnosis, and no
downstream reader may treat them as a mental-health signal.

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
| 2 | The thinking machine | Adopted | What kinds of thinking a person leans on, by mode, as stakes rise |
| 3 | Emotional and social disposition | Adopted | Preferences and tendencies in emotional and social situations, and steadiness under load |
| 4 | Objectives | Adopted | What a person is oriented toward; the external cause |

The set remains open. Neuroticism was previously a separate system; it now lives inside System 3
as emotional stability (baseline and reactivity under load), because it belongs to the same
emotional channel and because its main role is to moderate the other systems' stake responses.
Candidates not yet adopted are logged in open questions.

## Measures by system (working list)

- **System 1, Social energy economy.** (a) Energy gain: the sources and rates that replenish
  social energy. (b) Game choice: which social interactions a person enters and invests in.
  (c) Risk appetite: willingness to stake social standing or capital on an interaction's outcome.
- **System 2, The thinking machine.** A plane defined by two axes of reliance, observed under two
  modes, driven by a modulator. Axis A, cognitive sourcing: Internal versus External (reasoning
  from one's own theory and models versus from empirical data and the world). Axis B, method:
  Formal versus Informal (rigorous, communicable frameworks versus non-rigorous thought such as
  visualization and simulation). Modes: the Fast system and the Slow system (Kahneman), elicited as
  conditions, not scored for strength. Modulator: stakes. The output is two graphs, one per mode,
  each plotting the person's weight on the two axes as stakes rise. We measure reliance, not
  strength.
- **System 3, Emotional and social disposition.** Stated or revealed preferences and tendencies in
  emotional and social situations, not competence or skill. (a) Agreeableness versus Confrontation:
  tendency to accommodate versus to contest. (b) Introspection versus Situational awareness: which
  a person tends to orient by, their own emotional state versus the field of others (target of
  attention, not accuracy of reading it). (c) Emotional stability: baseline steadiness, and
  reactivity under load (how far and fast the baseline shifts as stakes rise). The stability
  measure moderates the other systems' stake responses.
- **System 4, Objectives.** An open prompt of what motivates a person, coded into a motive profile
  over: order and peace; triumph; power and influence (absorbing the earlier control motive);
  truth-seeking; novelty. Multi-label with weights; people carry more than one motive. A
  validation-and-excellence motive was dropped as orthogonal to motivation rather than a motive in
  its own right.

## Cross-system links we have noticed

These are real and should be modeled, not hidden. They are also where a reviewer will probe
independence.

- **System 3's reactivity under load moderates the thinking machine's stake response.** High
  reactivity likely predicts steeper trend lines in System 2's two graphs as stakes rise. Stability
  is therefore read partly through the steepness of System 2's graphs, not only on its own
  scenarios. This is the reason neuroticism was folded into System 3 rather than left standing
  alone.
- **System 2's Internal/External cognitive sourcing brushes System 3's Introspection/Situational
  awareness.** Boundary we are drawing: System 2 is the source of reasoning (theory versus data);
  System 3 is emotional and social attention (one's own feeling versus reading others). Related,
  separable, discriminant validity to be demonstrated.
- **System 1's risk appetite is social and domain-specific; System 2's stakes is a general
  modulator of thinking reliance.** Keep distinct; expect them to correlate.

## Expected objections (for the second opinion, and to pre-empt)

1. **Eliciting fast versus slow cleanly.** We no longer measure slow-system strength, which
   retires the "this is just fluid intelligence" objection at the root. The narrower residual
   concern: can the instrument elicit a genuine fast condition and a genuine slow condition well
   enough that the two graphs are distinct measurements and not the same one taken twice? This is
   now the live design risk in System 2, not the strength question.
2. **Dual-process theory is contested.** Kahneman's fast/slow framing has been criticized on
   replication and oversimplification grounds. The chapter acknowledges this and states that we use
   it as a modeling layer for observed mode-switching, and only as two elicited conditions, not as
   a claim about brain architecture.
3. **Discriminant validity across Systems 2 and 3.** The thinking machine's Internal/External
   cognitive sourcing and System 3's Introspection/Situational awareness, and within System 3 the
   stability measure versus the attention measures, could be re-derivations of fewer underlying
   factors. We owe evidence, or at least a falsifiable claim, that they separate.
4. **AI coding of free text.** A reviewer will ask how reliably an AI codes a response as formal
   versus informal, or internal versus external, and whether that coding is biased by writing
   ability, language, or culture, especially in a young and diverse population.
5. **Consequential use on minors.** High-stakes assessment of high schoolers demands fairness
   evidence and a clear account of what decisions the score may and may not inform.
6. **Novelty vs. the social-cognitive tradition.** A reviewer will note that situation-contingent
   personality (persons as if-then trajectories) is a decades-old result. The framework must not
   present it as new; the honest novelty is the one-session, auditable parameterization and the
   AI-coded instrument, not the underlying idea. Chapter 3 is written to concede this up front.

## Internal: novelty watch (NOT for the manuscript)

Kept only so we do not reinvent a known construct under a new name while building de novo. None of
this appears in the working paper.

- System 1 energy gain overlaps a known energy-direction axis; the differentiator is game choice
  and risk appetite. Keep those load-bearing.
- System 2's Internal/External and Formal/Informal axes brush a known perception axis and a known
  need-for-cognition construct; the differentiator is the two-graph reliance picture under stakes,
  by mode. Keep the stake-conditioned graphs load-bearing.
- The "person as trajectory, not point" framing is NOT ours to claim: it is the social-cognitive
  tradition (Mischel & Shoda 1995 situation-behavior signatures; Fleeson 2001 density
  distributions; Fleeson & Jayawickreme 2015 whole-trait theory; Moskowitz & Zuroff 2004
  flux/pulse/spin; Minbashian, Wood & Beckmann 2010 task-contingent conscientiousness). Chapter 3
  now credits this lineage explicitly and states the narrower instrument claim. Do not let the
  manuscript reintroduce trajectory-not-point as a founding discovery.
- System 3 now spans three well-known broad factors (agreeableness, an attention split, and
  emotional stability), and System 4 a fourth. De novo presentation is a stylistic choice, not a
  claim of unprecedented constructs; the reviewer will see the lineage, so our novelty must live in
  the measures and the cross-system dynamics (stability moderating the thinking machine), not in
  renaming.

## Style

- Declarative and precise. No em dashes. Semicolons, colons, commas, parentheses are fine.
- Define before you use. One definition per term, used consistently after.
- Unsettled claims go in Open Questions, not in the body as if settled.
