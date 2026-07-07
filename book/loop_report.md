# Loop report: two persona rounds and adversarial review

## 1. What the loop fixed

Two persona-driven repair rounds ran against `app/v2.html`; both ended with the full-flow regression passing (`test_v2.mjs`), plus a 30-assertion spot-check suite in round 2.

**Report honesty and overclaim removal (round 1).** Neutral Likert answers are no longer binarized into stances; straight-lining and five other engagement screens now trigger a "read with caution" banner that overrides the interpretability pass; the lead card no longer celebrates zero engagement as a "clearest lean"; friction, deliberation, challenge, and memory-recall lines were rewritten to stop praising noise ("under a second" instead of "0.0s", no courage credit for a button click); DRM energy averages are suppressed with an honest note when the slider was never moved; the mid-assessment AI summary requires 2+ real peeks and states ties as ties.

**Bugs (round 1).** F3 memory code hidden during recall; DRM chip carryover corrupting energy scores fixed, with scenes persisted and restored on resume; retracted objections no longer stored as the agreeing reply; resume-decline now actually writes the promised backup; import viewer got shape validation and strict read-only handling; the F2 savings numbers were changed so the peek no longer contradicts the binary; tradeoff filler pairs are disclosed and counted honestly.

**Round 2 bugs.** Tradeoffs resume no longer loses or duplicates picks; portfolio bands de-overlapped and scales made proportional; grid congruence only computed when an honest reading exists; the spend pick's +0.1 motive bump is now disclosed; the development-only use policy is printed on every report and embedded in exports; the repaired friction question no longer accepts a silent blank; the debrief count is generated, not hardcoded.

**Consent, refusal, and non-answers (round 2).** Fifth consent checkbox naming the recorded telemetry channels; explicit "I don't agree" ending with an erase option; a clean pre-consent stop path; "I'd rather not answer" recorded as data on the compass interview and DRM; the report counts declined and blank prompts as kept stances.

**Shared device, resume, and imported view (round 2).** Resume confirm names the session owner and step; resumes are logged and disclosed in the report; mid-screen drafts persist; the report names its respondent with a not-yours warning; imported reports carry a read-only banner and hide Stop.

**Report precision, accessibility, copy (round 2).** A third "NO READING" verdict, n= labels on every dot, scene counts on every average, hedged interpretability wording, zero-engagement and thin-evidence caveats, snap first-tap-final disclosure with the pick echoed back, colorblind-safe selected states (glyph plus border, aria-pressed), and a comparability line stating results cannot be ranked across people.

## 2. What was deliberately NOT changed

These were skipped because they alter what the instrument measures, which is the authors' call. Each got a disclosure or wording fix instead where one existed.

- **Snap-clock mechanics:** window length scaled to reading speed or an accessibility toggle; first-tap-final replaced by changeable picks or a mistap checkbox; tenths display as default (reduced-motion users now get whole seconds). Timing-out remains recorded and fine.
- **Commit mechanics:** undo-last-pick or confirmation beats on single-click screens; blank-driver confirms after every snap answer. Forward-only flow is disclosed up front instead.
- **Friction probe gating:** accepting an empty submit on the garbled question after one blocked attempt. Conflicts with the round-2 fix that tightened the blank gate; the "a guess counts" reassurance was added instead. (Adversarial review later confirmed a remaining problem here; see finding below.)
- **Sourcing measure:** suppressing DELIBERATE dots at zero engagement. Opening nothing is itself the measured own-compass signal; honest caveats and n= labels were added instead.
- **Review-draw and resume scope:** restricting 1-in-4 draws to the original sitting; persisting mid-slow-item timers and card state across resume. Wording fixes and the resumed-session disclosure cover these.
- **Scoring design:** softening timing flags when resumes are frequent (resume counts are disclosed next to the flags instead); per-item versus collapsed grid-congruence reporting.
- **Data schema:** offset-based telemetry timestamps (would break existing exports); dropping friction attemptText (hard rule forbids removing capture; it is disclosed and honestly named instead).
- **Progress bar** advancing during the 20-pick block: the per-pick counter is honest; faking global movement would not be.
- **Shared-device chooser UI:** the native confirm was made accurate rather than replaced.

## 3. Confirmed adversarial findings to address

All 24 findings below were confirmed against the code. Severity tiers are our triage; items in Critical block any pilot with minors.

### Critical

1. **No distress circuit-breakers; SJT has no decline path** (ethics-minors). The design mandates pause/skip affordances that mark items unscoreable; none exist, and the most aversive content (the cyberbullying vignette) hard-blocks with an alert. A distressed 14-year-old's only exits are Stop (which routes into their own report) or closing the tab. Fix: add a low-key "skip this one / take a break" on every probe and SJT item recorded as declined, a report-free branch in the Stop flow, and one line of support signposting in the debrief and withdrawn path.
2. **Consent decline or pre-consent stop, then reload, resurrects the live assessment with a dead Stop button** (code-quality). The withdrawn save records screen=1; resume promises "reopens its report" then renders consent, and the Stop handler returns early on `S.withdrawn` for the entire run. Fix: persist the ended state as a real terminal screen, gate Stop on "already on a terminal screen", and add a regression test: decline consent, reload, resume, assert the ended screen renders.
3. **Any student can open, continue, or export another minor's session** (product-deployment). Identity is one unauthenticated localStorage slot guarded by a confirm() honor system; the single backup slot silently destroys the previous student's data on the third use of a machine (v2.html:1547 overwrites `assessment_v2_app_prev` unconditionally while the dialog promises it is kept). Fix: server-backed sessions keyed to roster ID plus per-student access codes; until then, guard the backup slot (refuse or confirm before overwrite, or per-session keys listed on the data card).
4. **The full answer key, staged moments, and anti-gaming thresholds ship in view-source; retakes are free and untracked** (product-deployment). sealedFavors, SJT option values, filler pairs, and every flag threshold are readable via Ctrl+U; "Clear & restart" allows unlimited retakes; there is no proctor visibility at all. Fix: score server-side, issue single-use session codes, add a minimal proctor dashboard (started/finished/resumed/flagged), rotate variants per cohort.

### Major

5. **Mid-assessment AI read discloses the scored channels before every high-stakes item** (measurement). All hi-tier items follow the disclosure, all lo-tier items precede it, so the hi-vs-lo drift measures reaction to the disclosure. Fix: move the challenge screen after the last Arena item, or strip channel names and counts from it, or randomize tier across sittings so the confound cancels.
6. **Stakes axis is order- and content-confounded** despite design v2 claiming randomization (psychometric). FLOW is fixed: none-tier items in sitting 1, certain-tier in sitting 2, decision types unmatched. Fix: assign tiers at build() time across matched shells and interleave; until then, the salience line must say it is confounded with session order rather than hedging with "cautiously".
7. **Every stakes cell is n=1 yet per-person verdicts still print** (psychometric). The 0.3 drift threshold equals one opened card; design v2's own reliability gate is absent. Fix: suppress the salience verdict and hi/lo dot contrast when any cell has n<3; render pooled baseline dots only.
8. **Portfolio cross-check confirm coaches respondents out of the contradiction, then flags the honest ones anyway** (measurement). `crossCheckKept` is recorded but never read; the raw combination alone trips the whole-report caution banner. Fix: consult crossCheckKept in score() (an affirmed pattern must not trip the flag), or drop the confirm and keep the silent screen.
9. **Friction blank gates convert refusal into forced typing and time UI compliance** (measurement, and a separate ethics finding: the report promises "choosing not to answer is a real answer here" while this screen has no non-answer path). Fix: add an explicit "I can't answer this" option on both sub-questions recorded as data, stop confusedMs/recoveryMs at first submit attempt rather than first accepted submit, and log blocked attempts.
10. **One moved slider launders every untouched default-0 DRM scene into the energy averages** (measurement). energyTouched is recorded per scene but gated per session via `eps.some(...)`. Fix: filter per scene, count untouched scenes in the uncovered note, and require the touched count to clear the minimum before said-vs-did and lead-card comparisons run.
11. **Said-vs-did can hang a WORTH A LOOK chip on a single scene, and only straightlining gets the in-panel caveat** (ethics). Fix: require a minimum behavior sample per row (chosenSmallN >= 2, >= 2 SJT scenarios), fall back to NO READING otherwise, and fire the in-panel caveat on any lowSignal, not just straightlining.
12. **Age band is collected but never used**: the adult-only truth spend and the minors' system-level-only gap rule from the build's own embedded use policy are unenforced (psychometric). Fix: thread intake.age through scoring; for 14-17, placeholder the truth spend and collapse the gap card to one system-level sentence. Roughly 20 lines.
13. **Trap check is n=1 with a ~50% pass base rate, printed as an unqualified green PASS** (psychometric). Fix cheaply: give PASS the same instrument-framed wording as the inconclusive branch and drop the green styling; fully: author the remaining 3 counterbalanced traps.
14. **Import validation passes files that crash score() to a silent blank page** (security and code-quality, two confirmed findings). State is swapped before the crash and render() has no try/catch, so the round-1 claim of "no half-swapped state, no raw JS exception" is false on both halves. Fix: validate every field score() dereferences (sjt, friction, reviews, drafts, compass.prompt, per-entry cardsOpened) or wrap the import render in try/catch that restores prior state; on resume parse failure stash the raw blob under the backup key instead of discarding it.
15. **Persistence and confidentiality copy exceeds localStorage reality** (security). save() swallows all failures while the UI asserts unconditional persistence; the plaintext session under a guessable key is readable by any same-origin script. Fix: read-back verification with a persistent "export before closing" banner on failure; document the dedicated-origin requirement; consider encrypting or namespacing the stored blob.
16. **Saves persist a raw positional FLOW index with no version guard; withdrawal hardcodes `FLOW.length - 2`** (code-quality). The next FLOW edit silently resumes every in-flight save at the wrong screen. Fix: store per-screen ids (or a FLOW hash) in the save, honor session.version at resume, look up the debrief by id, dedup arena pushes by item id.
17. **Review draw re-rolls on every render and marks items reviewed as a render side effect** (code-quality). A reload changes the draw; Stop on the review screen persists reviewed-with-no-text. Fix: draw once, persist drawn ids (as the tradeoffs fix did), set `_reviewed` only in the Done handler.
18. **Stop confirm burns the wall-clock snap timer**: pressing "Stop anytime — no penalty" mid-snap and cancelling returns to an expired clock and a permanent timedOut record (ethics). Fix: pause snap and slow timers while any blocking dialog is open, or mark dialog-interrupted items "interrupted, not scored".
19. **The only withdrawal regression test targets the v1 build**, and the 1,555-line file's render-time side effects and orphaned intervals make behavior order-dependent (code-quality). Fix immediately: point test_withdraw.mjs at v2.html and add a reload-and-resume sweep across every FLOW screen; structurally, extract score() and the item bank into testable blocks and centralize timer teardown.

### Minor

20. **Export retains content the UI said was removed**: deleted DRM scenes logged with full content, retracted objections, and on withdrawal the intake and DRM drafts ride into the export despite "your report covers only what you completed". Fix: log removals by index or hash only, delete drafts on withdrawal, disclose retractedDraft retention at the moment of retraction, and enumerate edit/removal telemetry before export.
21. **The free-choice items announce "your pick is itself recorded" at the decision point**, converting the deliberation-default channel into self-presentation. Fix: keep the equal-weight randomized buttons, move the recording disclosure to consent and debrief like every other channel.
22. **h() keeps a live unused innerHTML branch and the page has no CSP**; XSS is absent only incidentally while the import viewer feeds attacker-controlled JSON into the same pipeline. Fix: delete the dead `html:` branch and add a restrictive CSP meta tag.
23. **The debrief claims "you agreed to staged moments up front" for four elements when the assent named two** (the sealed card and filler pairs were never in the checkbox). Fix: extend the assent to honestly cover built-in checks and unscored camouflage, or reword the debrief to claim agreement only for the two assented elements.

## 4. Before-first-paid-pilot checklist

- [ ] Ship the distress circuit-breaker: skip/pause on every probe and SJT item, report-free Stop branch, support signposting (finding 1).
- [ ] Fix the withdrawal state machine and dead Stop button; add the decline-reload regression test (finding 2).
- [ ] Replace the localStorage honor system with roster-keyed access codes and server-side scoring; guard or version the backup slot; add proctor visibility and retake control (findings 3, 4).
- [ ] Gate all per-person stakes, trap, and said-vs-did verdicts on minimum n; state the order confound plainly until tiers are randomized (findings 6, 7, 11, 13).
- [ ] Move or strip the mid-assessment channel disclosure; wire crossCheckKept and per-scene energyTouched into score(); add the friction non-answer path with honest timing (findings 5, 8, 9, 10).
- [ ] Enforce the age band: no truth spend for minors, system-level gap reporting only (finding 12).
- [ ] Harden import and persistence: deep validation or try/catch restore, save write-back verification with a failure banner, versioned saves, one-time review draw (findings 14, 15, 16, 17).
- [ ] Pause timers during blocking dialogs (finding 18).
- [ ] Point the withdrawal test at v2, add the reload-at-every-screen sweep, and begin extracting score() for isolated testing (finding 19).
- [ ] Close the disclosure gaps: export retention of deleted content, debrief assent scope, free-choice recording notice location, CSP and dead innerHTML branch (findings 20 to 23).
- [ ] Decide the open measurement-design questions from section 2 (snap window accessibility, friction gating, review-draw scope, telemetry timestamp schema) and record the decisions so future loops stop re-litigating them.