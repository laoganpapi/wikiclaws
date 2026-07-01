# Instrument Design: The Assessment

Working design for the AI-liaisoned assessment that administers the four-system framework. This
document specifies what the respondent experiences, what is captured, how raw capture becomes the
33 metrics of the catalog, and how the whole thing is validated. It is a design, not a final
protocol; every module lists its known risks.

## 0. Design principles

Everything below follows from six commitments.

1. **Revealed first.** The empirical literature shows trait self-report of exactly our constructs
   (social energy above all) is contaminated by identity and forecasting error. The spine of the
   instrument is observed behavior; self-report is retained deliberately as the *stated* side of
   the stated-revealed gap, which is a first-class result.
2. **Real stakes, not imagined ones.** The instrument runs an internal point economy with
   consequences the respondent actually cares about (visibility, rank, unlocks, audit exposure).
   Stakes are experienced, not narrated.
3. **Process over product.** We instrument what the respondent *does* on the way to an answer:
   what information they pay to open, whether they reach for structuring tools, latency, revision.
   Process tracing is harder to fake and cheaper to code than prose.
4. **Modes are elicited, not asked about.** Fast thinking is invisible to the thinker. The same
   scenario is answered twice: a forced snap response, then an invited deliberation. The pair is
   the measurement.
5. **Auditable coding.** Every AI-coded judgment carries span-level evidence (which words or
   actions drove the code), a confidence, and a second independent coding pass. Codes must survive
   a fluency audit: writing quality must not predict the code once choice structure is controlled.
6. **Preference, never ability.** No response is scored for correctness or quality anywhere in the
   personality battery. Scenarios are engineered so that formal and informal, internal and
   external routes are all viable; only the *choice of route* is recorded.

## 1. Architecture overview

Four modules, deliverable in three sittings of 25 to 35 minutes, plus an optional
experience-sampling companion. Total core burden about 90 minutes.

| Module | Nickname | System served | Core method |
|---|---|---|---|
| A | The Arena | S2 Thinking machine (+ S3 reactivity) | Two-phase decisions in a staked point economy with process tracing |
| B | The Ledger | S1 Social energy economy | Day reconstruction, portfolio inventory, staked social choices |
| C | The Room | S3 Emotional and social disposition | Situational judgments plus live standardized probes from the AI |
| D | The Compass | S4 Objectives | Open prompt with laddering, forced tradeoffs, a one-shot behavioral probe |

The AI liaison runs all four: it presents, converses, probes, and codes. The point economy spans
the whole assessment and is the stake engine for Module A and the behavioral probe for Module D.

### The point economy (stake engine)

The respondent earns points across the assessment. Points are not decoration; they buy things the
respondent values: visibility controls on their own report, early unlocks, challenge attempts, and
standing on an opt-in leaderboard for cohort deployments. Three properties matter.

- **Escalation.** Arena scenarios are grouped in blocks with rising multipliers (1x, 5x, 25x). The
  respondent is told the multiplier before each block. This is the stakes axis.
- **Exposure.** At the top stake tier, the respondent is told that one of their answers, chosen at
  random, will be "audited": the AI will challenge it and they will defend or revise it live.
  Social stake rides on top of point stake.
- **Honesty.** The economy is real within the product: promised consequences always happen. A
  stake engine that bluffs teaches respondents to ignore stakes by item ten.

Known risk: point sensitivity varies by person, and for minors, competitive framings interact with
fairness. Pilot must calibrate stake salience per cohort, and leaderboards stay opt-in.

## 2. Module A: The Arena (thinking machine)

The centerpiece. Produces the eight core S2 metrics (per-mode baselines and stake-slopes on both
axes), the three derived S2 metrics, and, jointly with Module C, the reactivity measure.

### 2.1 Scenario design

Each Arena item is a decision problem with no correct answer and four engineered properties:

1. **A live internal-external conflict.** Every scenario ships with an optional *data shelf*
   (cards of empirical information: base rates, testimonials, track records) and is written so a
   reasonable answer can also be built from priors and models alone. Crucially, the shelf and a
   natural prior point in different directions, so the sourcing choice is revealed, not
   ornamental.
2. **A viable formal route and a viable informal route.** The interface offers optional
   *structuring tools*: a scratchpad, a pro-con grid, a weighting table, a probability slider.
   Reaching for a tool, or not, is a behavioral method signal that costs nothing to code.
3. **Age-native content.** Course selection, team conflicts, first-job offers, social media
   dilemmas, purchase and savings choices, group project triage. Reading level grade 8.
4. **Stake-scalable framing.** The same decision type recurs across stake tiers so slopes are
   estimated within decision type, not confounded by content.

### 2.2 The two-phase response

Every scenario is answered twice.

- **Phase F (fast).** A response window of 15 seconds with a countdown, then the choice plus one
  line: "what drove that?" No shelf, no tools; the shelf is visible as closed cards only.
- **Phase S (slow).** The same scenario reopens. Up to four minutes. The shelf can be opened (each
  card costs a small, visible number of points: willingness to pay for external data is revealed
  external sourcing). Tools available. The respondent may keep or revise their Phase F choice and
  writes a short rationale.

The pair is the measurement. Order is always F then S; the known cost is that S is anchored by F,
which we accept because the reverse order destroys F entirely. A subset of scenarios appears in
only one phase as a within-battery check on the anchoring.

### 2.3 What is captured per item

| Channel | Signal | Feeds |
|---|---|---|
| Shelf behavior | Cards opened, when, willingness to pay | Sourcing (revealed) |
| Tool behavior | Structuring tool opened and used vs not | Method (revealed) |
| Rationale text | Argues from model and principle vs cites shelf data | Sourcing (coded) |
| Rationale text | Builds explicit framework vs narrates feel and simulation | Method (coded) |
| Latency and revision | Response time distributions, F-to-S revision distance | Mode manipulation check; mode divergence |
| Physio-linguistic drift | Tone, error rate, latency shift across stake tiers | Reactivity (with Module C) |

Text codes are two signed scores in [-1, +1] (sourcing, method), each with quoted spans as
evidence, produced by two independent AI coding passes with an adjudication rule (disagreement
beyond 0.4 flags for human review in pilot; in production, widens the item's error bar).

### 2.4 From capture to the two graphs

For each mode m in {fast, slow} and axis a in {sourcing, method}, fit per respondent:

    score_{m,a}(stake) = baseline_{m,a} + slope_{m,a} * stake_tier + noise

Behavioral and coded signals enter as parallel indicators of the same latent score (a small
measurement model, estimable with IRT-style machinery). Eight parameters = the two graphs.
Derived: mode divergence (distance between fast and slow parameter vectors), total
stake-sensitivity (norm of the four slopes), deliberation default (from free-choice items where
the respondent may answer immediately or request the slow phase, plus F-phase latency style).

### 2.5 Manipulation checks (the load-bearing risk)

The whole design stands on F and S being genuinely different modes. Three checks are built in:

- Latency distributions in F must be compressed and near-floor; in S, dispersed.
- Coded method scores must differ between phases within respondent on average (population-level
  check that the elicitation moves anything at all).
- A planted "trap" pair per battery: a scenario where the shelf contains one decisive card. Fast
  answers cannot have seen it; slow answers that still ignore it reveal sourcing, but if *fast*
  responses statistically reflect shelf content, the F window is leaking and must be tightened.

If fast and slow graphs are indistinguishable across the pilot population, the elicitation failed
and the design reverts to a single-graph instrument with mode as a self-report facet. This is
stated in advance as the falsifiable core of Module A.

## 3. Module B: The Ledger (social energy economy)

Three revealed layers and one stated layer, ordered so the revealed layers cannot be contaminated
by the trait questions.

### 3.1 Day reconstruction (revealed energy gain)

An adaptation of the Day Reconstruction Method: the respondent rebuilds yesterday (and one
weekend day) as a sequence of episodes, then rates each episode on momentary energy and affect,
and tags its social composition (alone; one close person; small familiar group; large or
unfamiliar group) and voluntariness (chosen vs obliged). The AI liaison makes this conversational
and fast (target 12 minutes).

From episode-level data: **net social charge** (within-person contrast of energy in social vs
solitary episodes, by company type), **recovery rate** (energy trajectory of solitary episodes
that follow social ones), **source concentration** (variance of the charge effect across company
types), **voluntariness correction** (chosen vs obliged solitude are scored separately; the
literature says only chosen solitude regulates). This dodges the trait self-theory problem: we
never ask "do people drain you," we compute it from remembered episodes, which the DRM literature
shows carry far less identity bias.

### 3.2 Portfolio inventory (revealed game choice)

A structured, countable inventory: who did you interact with this week, how often, initiated by
whom, in service of what. Produces portfolio breadth, allocation share, and selectivity from
near-factual recall rather than self-characterization.

### 3.3 Staked social choices (revealed risk appetite)

Risk appetite cannot be asked ("are you socially bold?" is the most inflated self-report in a
young population). The assessment embeds real choices:

- **Audit election.** Before the Arena's top tier, the respondent chooses: accept the random
  audit for a large point bonus, or pay points to be exempt. Staking comfort for gain, revealed.
- **Visibility elections.** Opt into or out of cohort leaderboard; choose whether their strongest
  and weakest system are visible on the shareable report version.
- **Message drafting.** Two simulation tasks: deliver unwelcome feedback to a friend character;
  ask a high-status character for something. Coded for approach vs avoidance, softening,
  deferral. (Coded for *choice structure*: did they raise the hard thing at all, how directly;
  never for eloquence.)
- **Challenge election.** After the AI's mid-assessment summary of them, the respondent may
  contest it. Contesting a machine evaluation is a mild but real social-risk act and doubles as a
  Module C probe.

### 3.4 Stated layer

A short trait battery covering every S1 metric, administered *last* in the module. Its purpose is
the gap: stated-vs-revealed divergence per metric, which the literature (forecasting-error work)
predicts will be large and informative exactly here.

## 4. Module C: The Room (emotional and social disposition)

Two layers: standardized situational judgment, and live probes inside the relationship the
respondent already has with the AI liaison.

### 4.1 Situational judgment set

Charged, age-native vignettes (a friend takes credit for your work; a group chat turns on
someone; a teammate is quietly failing). For each: a forced choice among four responses spanning
the agreeableness-confrontation axis, then an open "what would you actually be paying attention
to here?" The open response is coded for **attention target**: self-referential feeling language
vs reading of the other parties and the field. Span-evidenced, dual-coded, fluency-audited.

### 4.2 Live probes

The assessment itself is a social situation with real (if mild) charge, and the AI can
standardize it:

- **The dispute.** The AI politely pushes back on one mid-stakes Arena rationale ("I'm not sure
  that follows; here's why"). Standardized script, calibrated mildness. Measured: contest vs
  accommodate vs withdraw, and whether the respondent's next answers shift (accommodation
  spillover).
- **The friction.** One task arrives with genuinely ambiguous instructions; the AI is briefly
  unhelpful, then repairs. Measured: tone and latency drift, error spike, recovery time after
  repair. This is the standardized stressor for **baseline stability** and, with the Arena's
  stake-tier drift, **reactivity under load**.
- **The audit** (from the point economy) is the highest-charge probe and is scored for both S1
  risk behavior and S3 friction handling.

Ethics gate for minors: probes are mild by design (a disagreement, an ambiguity, never mockery or
personal criticism), disclosed in assent language ("parts of this assessment include challenge
and pushback"), always followed by in-flow repair, and reviewed by an external ethics reader
before any minor cohort. Reactivity is reported as a tendency reading, never as a clinical
signal; given the population, reports must say a reading at seventeen is a reading of seventeen.

### 4.3 Reactivity as the shared parameter

Reactivity under load is estimated once, jointly, from: stake-tier drift in the Arena, the
friction probe recovery curve, and stability self-reports (stated side). The same parameter feeds
S3's metric and moderates interpretation of S2's slopes, implementing the cross-system claim of
the framework in the measurement model itself rather than as prose.

## 5. Module D: The Compass (objectives)

### 5.1 Open prompt with laddering

"Tell me about something you're working toward, and what a good life looks like from where you
stand." The AI follows with two or three laddering probes ("why does that matter to you?"),
walking means-end chains toward terminal motives. Coded to the five motive weights with quoted
spans; laddering matters because first answers are goals (get into a program) and motives live
two rungs down (what the program is *for*).

### 5.2 Forced tradeoffs (revealed weights)

Around 18 to 20 paired scenarios, each pitting two motives cleanly: a sure win nobody sees
(Triumph vs Validation-free framing), the fascinating role vs the influential role
(Truth vs Power), the calm year vs the unrepeatable adventure (Order vs Novelty). Choices fit a
pairwise-comparison model (Bradley-Terry) yielding revealed weights on the same five-simplex as
the coded prompt weights.

### 5.3 The spend (behavioral one-shot)

At the end, the respondent spends their accumulated points on exactly one of five options,
engineered to map one-to-one onto the motives: lock in your rank and finish clean (Order); enter
the head-to-head challenge round (Triumph); choose which single insight from your report gets
shown first to whoever you share it with (Power/influence over the narrative); open the sealed
"hardest truths" page of your own results (Truth); unlock the experimental never-before-run
module (Novelty). One choice, real consequence, five-way motive probe. Low reliability alone, but
a sharp tiebreaker and a memorable end.

Motive profile = measurement-model blend of 5.1 (stated), 5.2 (revealed), 5.3 (behavioral);
concentration and the stated-revealed motive gap fall out arithmetically.

## 6. Optional companion: five-day experience sampling

For cohorts that can support it (a school week, an onboarding class): three brief phone pings a
day for five days: what are you doing, with whom, energy and mood now. This is the gold-standard
S1 stream (it is the method the energy literature is built on), sharpens the DRM estimates, and
gives S3 baseline stability a real-world trace. The core assessment must stand without it; the
companion upgrades confidence, never gates the report.

## 7. Coding governance (applies to every free-text code)

1. Two independent AI coding passes per response, different prompts, blind to each other.
2. Every code ships with quoted span evidence and a confidence; disagreements widen error bars
   rather than silently averaging.
3. A human-coded calibration set (pilot: 20 percent of responses, expert dual-coded) anchors the
   AI codes; production AI-human ICC target at or above 0.75 per code family.
4. Fluency audit: writing quality scores (length, syntax, vocabulary) are computed for every
   response and must not predict codes once behavioral signals are controlled; where they do, the
   code family is redesigned toward behavioral capture (shelf, tools, choices) and away from prose.
5. Language and dialect fairness: coding validated per major language variety in the population;
   differential item functioning analysis on every coded item.

## 8. Scoring and the report

- Each of the 33 catalog metrics gets: a point estimate, an error bar, and where applicable a
  stated value, a revealed value, and the gap.
- S2 is reported as the two graphs, drawn, with confidence bands, plus a plain-language
  trajectory sentence ("under pressure, your quick thinking moves toward your own models and gets
  more structured; given time, you stay with the data").
- No composite "personality score" exists anywhere. The framework says systems are separable;
  the report honors it.
- Stated-revealed gaps are presented as findings with care ("you describe yourself as X; your
  choices here looked like Y; that difference is worth knowing"), never as accusations of
  self-ignorance. For minors this framing is reviewed with the ethics reader.

## 9. Validation plan (what we owe the second opinion)

Pre-registered pilot, target n = 300, stratified across high school, college, early workforce.

1. **Mode elicitation check** (the falsifiable core): fast and slow parameter vectors must differ
   within persons; latency separation must hold. Failure reverts Module A to single-graph.
2. **Discriminant validity against intelligence**: administer a public-domain cognitive battery
   (e.g., ICAR-16) alongside. Every S2 metric must correlate near zero with it (prespecified
   |r| < .20). This is the empirical cash-out of preference-not-ability, and the single most
   important number for the academic reviewer.
3. **Convergent and discriminant mapping**: BFI-2, need-for-cognition, rational-experiential
   inventory, trait EI, and a values measure. We predict moderate convergence where lineage
   exists and demand separation where the framework claims novelty (S2 sourcing vs S3 attention
   target; S1 risk appetite vs S2 stake slopes). The de novo stance governs the manuscript, not
   the validation study; the validation study must name and measure the neighbors.
4. **Test-retest** at four to six weeks (personality is non-static, but not week-noisy; target
   r > .70 on baselines, with slopes allowed lower and reported honestly).
5. **AI-coding reliability**: AI-human ICC ≥ .75; inter-AI agreement; fluency-audit pass.
6. **Fairness**: DIF by gender, language background, and age band on every scored item; stake
   salience calibration by cohort; leaderboard and audit mechanics reviewed for anxiety load in
   the youngest band.
7. **Criterion glimpse** (secondary): supervisor or teacher ratings and 3-month outcomes for a
   subsample, purely exploratory at pilot scale.

## 10. Known open problems, stated plainly

- **Anchoring in the F-then-S design.** Accepted cost; partially checked by single-phase items.
  If anchoring dominates, S-phase data degrades toward F echoes; the check will show it.
- **Stake ceiling.** Points and visibility are real but bounded stakes; the theory's claims about
  high-stakes migration are tested only in the range the instrument can ethically create.
  Reports must scope claims to that range. The EMA companion reaches further into real life.
- **The audit and dispute probes measure disposition toward an AI**, which may not transfer to
  humans at full strength. Pilot compares probe behavior with SJT and message-draft behavior to
  bound the transfer question.
- **Five motives may not span the space.** The open prompt will surface residue; coding includes
  an explicit "other" bucket, and if the bucket runs heavy, the motive list grows.
- **Gaming.** Once stakes matter, some respondents optimize the image they project. The
  process-tracing layer (shelf, tools, latency) is much harder to game than prose, which is a
  main reason it is the spine. Detection analytics (implausible latency-code combinations) flag
  rather than punish.

## 11. Build order

1. Author 24 Arena scenarios (8 decision types × 3 stake tiers) plus the trap pairs.
2. Build the point economy and the two-phase interface with full process logging.
3. Stand up the coding governance stack (dual coder, spans, fluency audit) on synthetic data.
4. DRM conversational flow (Module B1) next; it is the least risky and independently useful.
5. Modules C and D; ethics review pass for the probe scripts.
6. Pilot, pre-registered, n = 300.

The adversarial design review (simulated psychometrician, dual-process skeptic, fairness
reviewer) belongs between steps 5 and 6, before a single real respondent, and before the real
second opinion is spent.
