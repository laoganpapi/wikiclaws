# Instrument Design v2

Revision applying the 35 verified findings in design_review_memo.md, with feasibility and
affordability as governing constraints. v1 is in git history. Changes from v1 are marked with the
finding numbers they answer.

## 0. What changed at the architecture level

1. **The point economy is gone as the stakes engine** (findings 1, 2, 4, 5, 6, 8, 9, 32). Points
   could not carry stakes without scoring correctness, and one currency contaminated three
   systems. Stakes are now denominated in **review probability**: every Arena item carries a
   disclosed chance that the respondent will explain that answer to the AI at the end of the
   sitting (none, 1-in-4, certain). Accountability is the stake at every tier, so tier no longer
   confounds accountability with stakes (finding 7). No exemption can be bought (8, 21). Which
   items are review-eligible is not identifiable in-flight beyond the disclosed probability, which
   blocks the flat-slope script (9).
2. **Per-person stake-slopes are demoted; baselines are the v1 headline** (15, 16, 19). Individual
   reports state each axis baseline per mode, plus a three-category stake response (rises, flat,
   falls) that is only reported when it clears a pre-registered reliability gate. Continuous
   per-person trend lines become a cohort-level research output until parallel forms and item
   counts can support them. This one decision cuts item demands, burden, and cost more than any
   other.
3. **Two sittings, not three** (28, 30): 40 and 45 minutes, aversive-adjacent content split across
   both. Stated batteries move to a 10-minute asynchronous touchpoint. Bottom-up time budgets
   below; nothing ships until 3 Arena items and 1 DRM day are prototyped with real teenagers and
   the budget holds.
4. **Ethics package rebuilt for minors** (20, 21, 22, 23, 24). Guardian consent plus specific
   assent naming staged disagreement and ambiguity; mandatory end-of-session debrief naming both
   probes; no-penalty withdrawal at any point; distress circuit-breakers that pause probes and
   mark items unscoreable; a binding use policy (below); gap reporting constrained.
5. **Reactivity is estimated only outside the Arena stake manipulation** (17, 26, 31): the
   friction-probe recovery curve plus stated stability. The moderation of S2 slopes by reactivity
   becomes a testable cross-loading in the pilot model, not a built-in identity.
   Physio-linguistic drift is logged as telemetry, not scored in v1.

## 1. Module A: The Arena (thinking machine)

### Items and phases

**15 scenarios** (5 decision types × 3 review-probability tiers), split-battery design
(finding 13): **9 F-only and 6 S-only**, matched within decision type and tier, plus **2 two-phase
items** kept as a revision-behavior probe, and **4 trap items** (counterbalanced decisive-card
variants, finding 14). Tier order randomized within person (finding 3).

**F items** (finding 10): unlimited reading time; the response clock (5 seconds) starts at choice
onset; a concurrent-load element (hold a 4-digit code) on half the F items. Each F item includes
one forced binary probe under the same clock: one free peek, data card vs principle card
(finding 11). The one-line "what drove that?" is coded but classified as stated-side data;
probe wording varies per item and near-duplicate rationales are flagged (12).

**S items**: up to 4 minutes; shelf cards are **free but budgeted** (3 non-bankable opens per
item, dwell and scroll telemetry per card, findings 5 and the dismissed skim-cite objection);
structuring tools are scored on **engagement, not opening**: the tool's own output must be
congruent with the chosen option, and click-plus-incongruent-rationale flags the item
(finding 25). Behavioral and text channels corroborate only if conditionally independent.

### Scoring

Per mode and axis: a baseline (IRT-style, behavioral and coded indicators) and a categorical
stake response with an error-aware contrast against a permutation null, tier coding prespecified
(finding 15). Mode divergence is disattenuated before reporting. A per-person **stake-salience
check** (does review probability move anything at all for this respondent) gates interpretation
of flat profiles (2, 17).

## 2. Module B: The Ledger (social energy)

- **One-day DRM** (yesterday), 15-minute budget honestly stated (28). The second day and the EMA
  companion move to phase 2.
- Portfolio inventory unchanged (countable recall).
- **Risk appetite indicators**: review-election behavior (accept a certain-review bonus item or
  not; free, no fee, finding 21), the two message-drafting simulations, and the challenge
  election. Scored only on convergence of at least three indicators; group-mean invariance is
  tested on the elections specifically, with a pre-registered drop rule (23).
- Stated battery: asynchronous, after both sittings.

## 3. Module C: The Room (disposition)

- SJT set: 6 vignettes (forced choice plus open attention question).
- **Attention target gets a behavioral indicator** (18): in two vignettes the respondent spends a
  free probe budget between check-your-own-reaction and read-the-field probes before answering.
- Probes: one dispute, one friction, both disclosed in specific assent, both debriefed, both with
  circuit-breakers (22, 21). Probe-window behavior is reported as a **lower bound** on reactivity
  (26).
- Reactivity: friction recovery curve plus stated stability only (17, 31).

## 4. Module D: The Compass (objectives)

- Elicitation rule (binds every stated measure, all modules): open text only where answering is
  easy; structured choice wherever it reduces noise. Nobody is asked to articulate their
  objectives from a blank page.
- The opening prompt is a catalogue: ten concrete, kid-legible objectives spanning the five
  motives, pick one or two, with room to name your own. The laddered open "why" follows the pick,
  where it is easy to answer. Intake notes follow the same rule: pick-from-options with an
  optional say-it-your-way override, never a bare completion like "when it comes to money, I
  value…".
- Tradeoffs: 16 pairs, motive contrasts **disguised in scenario texture** with filler dimensions
  and rotated framings; cross-framing inconsistency is the Module D integrity signal (27).
- The spend: no points. One end-of-assessment choice among five **report-deliverable** options
  (which insight leads your report, see the hardest-truths page*, preview the experimental module
  description, enter the cohort comparison view, lock and finish) (32). *Hardest-truths page is
  adult-only (22).

## 5. Use policy (binding; supersedes the finding-20 version)

1. The instrument does not predict and is never validated for prediction. Scores exist for the
   subject's own self-understanding. Selection use (hiring, admission, ranking, screening,
   placement) is a misuse the instrument disowns, permanently, not pending validation.
2. The assessment is offered only inside the authors' own venture and program. Results are never
   disclosed to schools or employers; there is no institutional copy. The subject holds the report
   and controls any sharing. Inside the program, readings may tailor and offer, never deny, rank,
   or gate.
3. Reactivity and stability carry a clinical bar as well: never used to diagnose, screen for, or
   flag a mental-health condition; reported only as dated, session-scoped observations.
4. Clean or silent: no stated-revealed gap and no stake-slope appears unless it clears a
   pre-specified reliability threshold. Below threshold the report says "no clear gap" or "no
   clear shift" — never a shaky number softened by a caveat.
5. Minors' scores expire after 18 months and never enter a permanent record. For minors, gaps are
   reported at system level only, framed symmetrically.
6. Report language is neutral and descriptive: past-tense, session-scoped, no valence (collapse,
   degrade, volatile, and spike are barred words), no praise, no deficit, no forecast, and no
   performance speculation in either direction.
7. The ethics reader signs off on this policy before any minor cohort.

## 6. Coding operations (finding 31)

- Roughly 25 codable texts per respondent (down from ~60 in v1; the split battery and item cuts
  do this).
- Dual AI passes with span evidence stay; disagreements widen error bars.
- Expert calibration: stratified 10 percent with a power justification, budgeted below.
- Fluency audit stays; it conditions on behavioral signals only where channel independence holds.

## 7. Burden budget (bottom-up, finding 28)

| Component | Items | Est. minutes |
|---|---|---|
| Sitting 1: intake, reading-speed calibration (33), 8 Arena items, DRM | | 40 |
| Sitting 2: 7 Arena + traps, SJT 6, probes, Compass prompt + 16 pairs, spend, debrief | | 45 |
| Async: stated batteries S1 + S3 | | 10 |
| **Total** | | **95** |

Gate: prototype timing with real teenagers before build-out. If the budget breaks, cut Arena to
12 items and re-run the reliability simulation, in that order.

## 8. Cost model (estimates; all numbers are assumptions to validate, not quotes)

**Per-respondent variable cost** (production):
- AI liaison inference (2 sittings, adaptive dialogue): ~$0.75–2.50
- Dual-pass coding, ~25 texts + spans + audits: ~$0.30–1.00
- Infra, telemetry, storage: ~$0.25
- **Total: roughly $1.50–4 per respondent**, which prices a school cohort of 500 at under $2k
  variable.

**Fixed build (v1)**:
- Scenario and item authoring (15 Arena + 4 traps + 6 SJT + 16 pairs + parallel Form B of the
  Arena for retest, finding 19): the largest single line; ~6–10 expert-weeks.
- Interface with process logging (no economy to build; the review mechanic is a dialog flow):
  meaningfully cheaper than v1's ledger, leaderboard, challenge round, and experimental module,
  all of which are cut or deferred (32).
- Coding stack and fluency audit: ~3–4 engineer-weeks on top of prompt work.

**Pilot** (finding 29, rescoped):
- 450 starts targeting 300 completers (30), stratified; partial-data report schema prespecified.
- Pre-registration: equivalence tests on **baselines only** vs ICAR-16 with multiplicity
  correction; DIF is screening-only at this n; phase-2 confirmatory sample named now with
  per-group n targets (~150 per focal group).
- Expert calibration coding: 10 percent × 300 × ~25 texts ≈ 750 texts dual-coded ≈ **190–300
  expert-hours** (~$15k–30k at market rates), budgeted as a line item.
- Incentives for 450 starts (~$25–40 each): ~$11k–18k.
- **Pilot total, order of magnitude: $40k–80k** plus internal build labor.

**Deferred to phase 2** (affordability): EMA companion, second DRM day, leaderboard and cohort
mechanics, challenge round, experimental module, continuous per-person slopes, full DIF program.
There is no criterion study, deferred or otherwise: the instrument does not predict outcomes and
is never validated as if it did.

## 9. Validation plan (rescoped; the burden is truth-of-description, not prediction)

1. Mode elicitation check, now against Type-1 markers (load-task interference patterns, probe
   choices), not latency compression (10; the latency check is kept as constraint enforcement
   only, per the dismissed objection).
2. Discriminant vs ICAR-16 on baselines, |r| < .20 prespecified with reliability-corrected
   bounds (29): the empirical proof that this measures preference, not intelligence.
3. Convergent battery unchanged (BFI-2, NFC, REI, values), plus an MTMM model with a coded-prose
   method factor for the S2-sourcing vs S3-attention separation (18).
4. Retest on parallel Form B at 4–6 weeks; slope categories below r = .4 revert to cohort-level
   reporting, prespecified (19). Retest is read against the snapshot stance: agreement is
   consistency of the instrument, and change over time is not failure.
5. AI-human ICC ≥ .75; fairness battery adds report-precision-by-language-group (33) and the
   election invariance tests (23).
6. Attrition analysis pre-registered: early-behavior predictors of dropout, because dropout is
   endogenous to the constructs (30).
7. **Discrimination study (owed by the self-understanding stance).** Each participant rates their
   own profile and a matched stranger's profile, blinded. Own-profile fit must beat stranger-profile
   fit by a prespecified margin, and the analysis reports the reliability of the gap difference
   scores themselves, not just their components. Without this, no claim that the reading is about
   the person rather than about everyone.
8. **Format-swap check on the gap.** For a subsample, the stated side is re-elicited in the same
   scenario-choice format as the revealed side. A gap that shrinks under matched formats was
   measuring the difference between a questionnaire and a scenario, not the person; only gaps that
   survive the swap may be shown or treated as training-relevant.
9. **Stated-stream validation.** Evidence that the open-prompt "wants" are stable enough across a
   short interval and across phrasings to be read as wants rather than one-off stories.

## 10. What v2 gives up, stated plainly

- Continuous per-person stake-slopes (the most novel v1 promise) until phase 2 earns them.
- The gamified economy and its engagement value; the review mechanic must carry stake salience
  alone, and the stake-salience check tells us per person whether it did.
- Real-world reach of the EMA companion in v1.
- Some fast-mode purity: F items are cleaner than v1 but the mode claim now rests on load-task
  and probe evidence, and if the pilot's Type-1 markers fail, Module A reverts to a single-graph
  instrument as before.

## 11. Build order

1. Prototype 3 Arena items + 1 DRM day with 5 teenagers; validate the burden table.
2. Author full item set + Form B; ethics package to the external reader.
3. Coding stack on synthetic data; channel-independence checks.
4. Assemble sittings; internal dry runs; timing re-check.
5. Pre-register; pilot 450 starts.
