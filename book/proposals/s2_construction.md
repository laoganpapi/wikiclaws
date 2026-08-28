# System 2 Construction Proposal: Memory, Formal Learning, Informal Learning, Intuition

Status: internal design document, not manuscript prose. Feeds Chapter 3 (`03_thinking_machine.md`)
and the architecture's Open Questions apparatus (`00_architecture.md`). Written for a systems
architect who needs to draw the relationships as boxes and arrows and needs to know which arrows
are load-bearing on evidence and which are provisional.

Binding constraints carried from `00_architecture.md`: preference, not ability (three lanes —
preference / capability / pathology; this system occupies preference only); self-understanding,
not prediction; neutral bipolar measures, no valence; stated versus revealed are symmetric; clean
or silent on any reported gap or slope; snapshot, not verdict; de novo presentation, internal
novelty watch only. Memory and accumulated experience are an assumed capability substrate. This
system does not measure memory, does not score it, and proposes no change that would start
measuring it. Everything below that touches memory sits upstream of what the instrument reads, not
inside it.

---

## Part A — Relational model

### A1. Nodes

1. **Memory substrate (N1).** The retained record of a person's task-relevant past experience.
   Assumed as given. Never measured, scored, or reported by this framework, under any construct
   revision below.
2. **Formal learning route (N2).** Instruction or deliberate self-study that builds an explicit,
   abstracted schema and deposits it in the memory substrate.
3. **Informal learning route (N3).** Repeated task performance with outcome feedback that deposits
   unarticulated pattern knowledge in the memory substrate, without formal instruction.
4. **Environment validity (N4).** A property of the domain a learning route operated in, not of the
   person: whether the domain has stable, learnable regularities and fast, accurate feedback
   ("kind") or lacks them ("wicked").
5. **Grounded intuition (N5).** Reliable, fast, automatic judgment in a domain, drawn from memory
   substrate content laid down by either learning route.
6. **Domain structural similarity (N6).** The degree to which the task domain a person is currently
   in shares underlying relational structure, not surface features, with a domain where grounded
   intuition was built.
7. **Axis B reading: Formal/Informal (N7).** The observed, per-occasion choice to externalize a
   thought into communicable structure (Formal) or leave it as unarticulated simulation (Informal).
   The only node in this graph the instrument actually reports.
8. **Axis A reading: Internal/External (N8).** The observed per-occasion choice to reason from one's
   own models (Internal) or from external data (External). Included because grounded intuition can
   source from either pole; also reported by the instrument.
9. **Fast mode / Slow mode (N9).** The two elicited conditions under which N7 and N8 are observed.
10. **Stakes (N10).** The modulator that moves a person's N7/N8 lean as gain-or-loss magnitude rises
    within a mode.

### A2. Directed edges

1. **N2 to N1: deposits.** Formal learning writes an explicit, abstracted schema into the memory
   substrate. Licensed by Gick & Holyoak 1983 (schema induction from concrete analogs raises
   transfer versus single-case exposure) and Gentner's structure-mapping theory. **Settled.**
2. **N3 to N1: deposits, conditional.** Informal learning writes unarticulated pattern knowledge
   into the memory substrate, provided it includes prolonged practice with valid corrective
   feedback. Licensed by Kahneman & Klein 2009 ("Conditions for Intuitive Expertise: A Failure to
   Disagree"). **Settled**, with the gate in edge 3 attached.
3. **N4 gates N3 to N1.** The N3-to-N1 deposit is reliable only when the learning occurred in a
   kind environment (N4). In a wicked environment, practice can build confident pattern-matching
   without building anything that deserves the name grounded intuition. Licensed by Hogarth's
   kind-versus-wicked learning environments and the Camerer & Johnson process-performance paradox,
   read alongside Kahneman & Klein 2009. **Evidenced, not yet incorporated in Chapter 3 text — see
   Part B, P3.**
4. **N1 to N5: draws on.** Grounded intuition is memory-substrate content, however it was
   deposited, retrieved as fast, automatic judgment. This is the chapter's central claim about
   intuition. **Settled.**
5. **N5 to N7 (Informal pole), under fast mode: surfaces unexternalized.** When a person draws on
   grounded intuition without deliberately restructuring it, the observable behavior reads as
   Informal on Axis B. Licensed by the chapter's own position: "informal expression is grounded in
   accumulated experience... rather than the absence of grounding." **Settled.**
6. **N5 to N7 (Formal pole): surfaces externalized.** The same grounded content, deliberately put
   into explicit, communicable structure, reads as Formal on Axis B. Licensed by the chapter: "two
   people with the same depth of grounding... can land on opposite poles." **Settled.**
7. **N6 to N5: transfer.** Grounded intuition built in one domain is available in a second domain to
   the degree the two domains share structural similarity. Near-transfer (structurally similar
   domains) occurs; far-transfer (structurally unrelated domains) is rare and typically small.
   Licensed by Gick & Holyoak 1980/1983, Gentner's structure-mapping, Ross 1987, Holyoak & Koh 1987
   on the positive side, and Detterman 1993, Barnett & Ceci 2002, Sala & Gobet 2017-2019 on the
   ceiling. **Evidenced but currently mis-stated as a clean binary — see Part B, P5 (revise).**
8. **N1 to N7/N8, common cause (confound edge).** Domain-specific memory structure — chunking
   (Chase & Simon 1973), long-term working memory (Ericsson & Kintsch 1995) — may determine both
   how a person sources reasoning (N8) and how they externalize it (N7) on a given occasion,
   independent of any real-time preference the instrument means to capture. This is the edge that
   threatens, not just borders, the preference/capability line. **Open — see Part B, P1. Not
   resolved by this pass; logged, not fixed.**
9. **N10 to N7/N8, within N9: modulates.** Stakes move the N7/N8 lean within a mode. Pre-existing
   architecture, unaffected by this evidence pass. **Settled (unchanged).**
10. **N7 (observed) to {N2, N3, N6}: underdetermines.** A single Informal reading on Axis B is
    consistent with (a) no grounding, (b) grounding built via the formal route (N2), (c) grounding
    built via the informal route (N3), and (d) grounding transferred from a structurally similar
    domain (N6) with no learning route active in the current domain at all. The instrument cannot
    currently distinguish these four backing states from the reading alone. **Settled as a
    measurement-scope limit** — the chapter already states this, and the literature cited against
    the surrounding "no valence, style-only" framing (Meehl 1954; Dawes, Faust & Meehl 1989; Grove
    et al. 2000; Schooler & Engstler-Schooler 1990; Dodson, Johnson & Schooler 1997) was checked and
    found off-topic to this specific claim on verification (clinical-versus-actuarial prediction and
    verbal-overshadowing memory effects, not structure externalization). The narrow claim survives.

### A3. Worked traces

Three traces reaching the **same destination node — N7 at the Informal pole, observed in Fast
mode, at high stakes** — by three different upstream routes. This is the underdetermination edge
(A2.10) made concrete: the instrument returns one reading for all three people.

**Trace 1 — formal route, unexternalized under speed.**
N2 (years of structured chess instruction: openings, tactics, endgame theory) → N1 (schema-form
memory) → N5 (grounded intuition for board states) → N9 fast mode, N10 high stakes → N5 to N7:
the player moves instantly in a blitz game without narrating a reason → **N7 = Informal.**

**Trace 2 — informal route in a kind environment, unexternalized under speed.**
N3 (fifteen years on the job, unstructured, no formal fire-behavior coursework) + N4 = kind (fire
behavior is regular enough, and feedback — the structure holds or it does not — is fast and
unambiguous) → N1 (pattern-form memory) → N5 (grounded intuition for structural failure) → N9 fast
mode, N10 high stakes → N5 to N7: the firefighter orders an evacuation on a read, no articulated
chain of reasoning → **N7 = Informal.**

**Trace 3 — transferred grounding, no learning route active in this domain.**
N2 or N3 in domain X (structural engineering: load paths, failure cascades) → N1 → N5 in domain X →
N6 (domain Y, e.g. a financial-contagion scenario in the Arena, shares cascade-failure structure
with domain X) → N5 available in domain Y without any N2/N3 edge ever running in domain Y itself →
N9 fast mode, N10 high stakes → N5 to N7: an instantaneous, unarticulated read of the financial
scenario → **N7 = Informal.**

All three people receive the identical Axis B reading at the identical mode and stakes level. The
instrument has no edge back from N7 to N2, N3, or N6 (per A2.10); it cannot tell these three people
apart, and the architecture does not ask it to. This is the intended reading of "landing on the
informal pole says nothing about whether a foundation exists or which route built it" — traced out
as a graph rather than asserted as a sentence.

### A4. Settled versus open, by edge

| Edge | Status |
|---|---|
| N2 to N1 (formal deposits) | Settled |
| N3 to N1 (informal deposits) | Settled, conditional on edge 3 |
| N4 gates N3 to N1 (kind/wicked boundary) | Evidenced; not yet in Chapter 3 text |
| N1 to N5 (memory grounds intuition) | Settled |
| N5 to N7 Informal, fast (unexternalized surfacing) | Settled |
| N5 to N7 Formal (externalized surfacing) | Settled |
| N6 to N5 (structural transfer) | Evidenced; currently mis-stated as binary |
| N1 to N7/N8 common-cause confound | Open, unresolved |
| N10 to N7/N8 within N9 (stakes modulation) | Settled, out of scope for this pass |
| N7 underdetermines {N2, N3, N6} | Settled as a scope limit |

---

## Part B — Constructor proposal (keep / revise / add / retire)

### P1. Memory as an assumed, unmeasured capability substrate — **KEEP**, with an added caveat

Evidence for keeping it unmeasured: the CHC (Cattell-Horn-Carroll) model of intelligence places
long-term storage/retrieval and working memory in the ability taxonomy alongside fluid reasoning
and processing speed. Memory is squarely a capability-lane construct. Measuring it would cross the
line the architecture draws (three lanes; preference lane only). This part of the call is
one-sided. Decision: keep memory substrate as an assumed, unmeasured node.

Evidence against leaving it unremarked: Chase & Simon 1973 (chunking) and Ericsson & Kintsch 1995
(long-term working memory) show that domain-specific memory structure is not a clean substrate
sitting neutrally behind style choices — it can be constitutive of the very expertise that produces
a Formal or Informal reading. This licenses edge A2.8: memory structure as a possible common cause
of Axis A and Axis B placement, which threatens discriminant independence between what this system
reports (preference) and what it explicitly disowns (capability).

Axiom this must respect: "preference not ability" and the three-lane scope statement, plus the
architecture's own instruction that "where a measure brushes against an established construct... the
chapter must say so plainly."

**Decision (not open):** do not measure memory, ever, under any version of this proposal. **Add** an
Open Questions entry naming the memory-structure confound (A2.8) explicitly, so the instrument's
scope claim is not silently overstated. This is a documentation change, not an instrumentation
change.

### P2. "Formal training... tends to transfer across domains" (body text) — **REVISE**

The evidence is one-sided against the unqualified claim. Detterman 1993 concludes far transfer
"virtually never happens spontaneously." Sala & Gobet's meta-analyses (2017-2019) find far-transfer
effect sizes close to zero across chess, music, and working-memory training. Barnett & Ceci 2002
formalize the near/far distinction the body text elides. Gick & Holyoak 1983, the chapter's own
positive citation, supports only near transfer between structurally similar problems, and even that
required schema induction, not passive exposure.

Axiom: house style bars stating an unsettled claim as settled outside Open Questions. The chapter's
own Open Questions section already states this more carefully than the body text does ("Related,
not unrelated, is the honest scope").

**Decision (not open, evidence is one-sided): revise.** Narrow the body-text sentence to
"formalized knowledge tends to transfer between structurally similar domains" and remove the
unqualified "across domains" phrasing so the body no longer contradicts the chapter's own Open
Questions section.

### P3. Equivalence of formal and informal routes to grounded intuition — **REVISE (add a boundary condition)**

Kahneman & Klein 2009 is correctly cited and the equivalence claim is not wrong; it is
incomplete. The same lineage (Hogarth's kind-versus-wicked environments; Camerer & Johnson's
process-performance paradox) establishes that prolonged practice with feedback builds trustworthy
intuition only in high-validity ("kind") domains. In wicked domains, practice can build fluent,
confident, wrong pattern-matching. This is edge A2.3 (N4 gates N3-to-N1).

Axiom: "defensible to an expert" — a reviewer versed in the judgment-and-decision-making literature
will ask this question directly, and the chapter currently has no answer in the text.

**Preliminary lean, not fully settled:** add environment validity as a **named boundary condition
in Open Questions**, not as a new measured axis. Measuring "how kind is this domain" would require
either an external, validated task-domain taxonomy (out of scope for a self-report/AI-coded
instrument) or a judgment call by the instrument that edges toward evaluating domain quality — a
capability-adjacent judgment the architecture does not currently make and should not add lightly.
Recommend: log the boundary condition in prose; do not instrument it in this revision. Flag for a
future pass whether a coarse, self-reported "how much reliable feedback did you get in this
domain" item could gate the equivalence claim without becoming a capability score.

### P4. "No valence, style only" framing around the informal pole — **KEEP**

The narrow claim (a single occasion's Informal reading cannot rule out hidden grounding) is
logically sound and nothing in the literature disproves it. The broader challenge to the
surrounding neutrality framing cites Meehl 1954, Dawes/Faust/Meehl 1989, Grove et al. 2000
(clinical-versus-actuarial prediction) and Schooler & Engstler-Schooler 1990, Dodson/Johnson/
Schooler 1997 (verbal overshadowing in eyewitness memory). On verification, none of these are about
structure externalization or Axis B; they are topically unaligned with the claim they were cited
against.

Axiom: neutral bipolar measures, no valence. This construct already satisfies the axiom; the
challenge to it does not hold up under citation verification.

**Decision (not open, evidence is one-sided in favor of keeping): keep**, unchanged in substance.
Light-touch addition only: state explicitly, once, that "neutral" describes what the instrument can
observe (an externalization choice), not a claim that all possible groundings behind an Informal
reading are equally likely or equally verifiable — which the chapter already implies but has not
said in one sentence.

### P5. "Transfer holds for related domains and fails for unrelated domains" (binary framing) — **REVISE**

The directional claim is right; the binary is not. Gick & Holyoak's own studies found that
spontaneous transfer between structurally analogous problems is unreliable without a retrieval cue
(subjects often fail to transfer even a genuinely applicable analog unless prompted). Ross 1987 and
Holyoak & Koh 1987 show surface similarity also drives transfer, not structural similarity alone.
Sala & Gobet's later work frames near-transfer as reduced, not binary "holds."

Axiom concern specific to this system: a crisp "holds/fails" bipolar claim about transfer risks
reading as a hidden capability measure (how good is this person's transfer ability), which is
exactly the kind of ability-lane claim the architecture retired once already (the fast/slow
strength retirement, System 2's own precedent). The chapter must not reintroduce an ability claim
through the transfer back door.

**Decision (not open, evidence is one-sided against the binary): revise.** Replace "holds... fails"
with a graded statement: transfer between structurally similar domains is possible but unreliable
and typically depends on a retrieval cue, not on structural similarity alone; transfer to
structurally unrelated domains is rare and small. Keep this in Open Questions, where it already
lives, worded this way rather than as a bipolar claim.

### P6. The relational graph itself (Part A) — **ADD, but to internal design docs only**

The node/edge/trace model in Part A is useful and, per the routing task, evidence-backed where
marked settled. It is not manuscript prose: it is denser and more formal than the architecture's
house style permits for the reader-facing chapter ("plain register a smart non-specialist reads
easily"). **Decision:** keep this graph as an internal architecture artifact (this document, and a
pointer from `03_thinking_machine.md`'s Open Questions if useful), not as new chapter body text. Do
not add boxes-and-arrows language to the manuscript.

### P7. Core measured constructs (Axis A, Axis B, Fast/Slow modes, Stakes modulator) — **no change, RETIRE nothing**

Nothing in this evidence pass threatens the axes themselves. The evidence targets the wording of
claims about what grounds an Informal reading and how far grounding travels between domains — it
does not undermine the observation that people vary, per occasion, in cognitive sourcing and
externalization. **Decision (not open): retire nothing.**

---

## Appendix — Novelty watch note (internal only, not for manuscript)

Flagged during evidence verification, logged per the architecture's existing novelty-watch
mechanism rather than acted on here: Axis A's label, "Cognitive sourcing: Internal versus
External," names-collides with Rotter's Internal-External Locus of Control (Rotter 1954/1966), a
long-established bipolar construct in personality psychology. The content differs — Rotter's axis
is attribution of causal control over outcomes (effort versus luck/powerful others); this axis is
the source material of reasoning (own models versus external data) — but the shared label risks a
reviewer reading it as the same construct renamed. No construct change is proposed here; this is a
labeling risk for the writer's pass, consistent with the architecture's standing practice of
logging such collisions without resolving them in this document.

## Summary table

| # | Construct | Decision | Openness |
|---|---|---|---|
| P1 | Memory substrate, unmeasured | Keep + add confound caveat | Confound edge open; scope decision settled |
| P2 | Formal transfer "across domains" | Revise (narrow to similar domains) | Settled |
| P3 | Formal/informal route equivalence | Revise (add kind/wicked boundary) | Open — logged, not instrumented |
| P4 | "No valence, style only" framing | Keep | Settled |
| P5 | Transfer "holds/fails" binary | Revise (soften to graded/cued) | Settled |
| P6 | Node/edge relational graph | Add to internal docs only | Settled |
| P7 | Core axes, modes, modulator | No change | Settled |
