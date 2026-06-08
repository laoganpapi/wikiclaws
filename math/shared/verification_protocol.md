# Verification Protocol

**Project:** Collatz + Frankl research project
**Authors:** Alex Ye with Claude
**Status:** Binding on every agent in the project.

This is the gate that every claimed result must pass before it leaves the repository (arXiv post, journal submission, blog, or any external mention). The protocol has **four steps**; all four must pass.

> **Strict rule:** No proof claim is published — internally or externally — until all four steps pass and the human author (Alex Ye) signs off. A result that has passed only some steps is labeled `[unverified]` in our docs and is not citable in our own writing as a theorem.

The protocol is intentionally strict because the cost of a wrong claim in either of these problems (Collatz, Frankl) is catastrophic: both attract a steady stream of mistaken proofs, and a flawed claim from us would damage Alex Ye's standing.

---

## Step 1 — Computational sanity check

**Purpose:** Catch trivially wrong claims before they consume reviewer attention. Computation is cheap; a wrong claim is expensive.

**Scope:** Applies to any claim whose statement can be empirically tested on at least one example. For pure existence claims with no finite witness, this step is replaced by *test-case construction* — producing the explicit object the claim asserts.

**Procedure:**

1. **Translate the claim** into a checker. Write the statement of the lemma/theorem as a function `claim(input) -> bool` in Python (or similar). Code lives in `collatz/experiments/verify_<short_name>.py` or `frankl/experiments/verify_<short_name>.py`.
2. **Pick test inputs:**
   - **Collatz** claims: run on all $n \leq 10^6$ at minimum; spot-check on $n$ up to $2^{40}$; deliberately include adversarial inputs (Mersenne primes, $n$ with many 1-bits, $n$ just below known long-trajectory records).
   - **Frankl** claims: enumerate all union-closed families with ground set $\leq 8$ (manageable in seconds); spot-check random families with $n \in \{9, 10, 11\}$. If the claim involves a constant $c$, verify the bound is tight to within $10^{-6}$ on the test set.
   - **Conjecture-style claims** (i.e., "the inequality $X \geq Y$ holds"): also include test inputs where the inequality is conjectured to be *tight*; if the gap blows up on small examples, that is a red flag.
3. **Record the test seed, the test set size, and any failures.** Even one failure aborts the step and triggers a return-to-theory.
4. **Record the test run** in `<track>/experiments/verify_<name>_log.md`: date, code path, test scope, result, any flagged cases.

**Pass criterion:** Zero failures on the test set, plus written confirmation of the test scope.

**Failure handling:** If a test fails, the claim is wrong (or the test is wrong; investigate which). Either fix the proof or mark `[failed verification]` in `dead_ends.md` with the counter-example.

---

## Step 2 — Independent red-team agent review

**Purpose:** Find errors that the author missed. A separate Claude agent, with no investment in the proof being correct, attacks it.

**Scope:** Every result that has passed Step 1.

**Procedure:**

1. **Spawn a red-team agent** in a fresh context, with the following brief:

   > Attached is a claimed proof of [statement]. Your job is to find any error: wrong invocation of a lemma, gap in logic, unstated assumption, off-by-one, incorrect numerical constant, mis-cited theorem, prior-art collision (someone proved it first, or someone disproved this kind of claim). Do not try to fix the proof; only find problems. Search the literature for prior art that might invalidate the claim or that the proof should cite. Produce a list of specific objections with line-references.

2. **Required attacks:**
   - **Prior-art search.** The red-team agent must perform a literature search and report whether the claim, or a stronger form, is already known. (Specific to our problems: the Collatz folklore literature is enormous; the Frankl literature post-Gilmer is fast-moving. Both attract crank proofs that look correct.)
   - **Counter-example hunt.** The red-team agent tries to construct a counter-example computationally; runs the Step-1 checker on adversarial inputs of its own choosing.
   - **Lemma-by-lemma re-derivation.** For every lemma cited, the red-team confirms either (a) it is a verifiable cited result, or (b) we proved it earlier and it passed the same protocol.
   - **Constant chase.** Numerical constants in the proof are re-derived from scratch.
3. **Output:** `<track>/red_team/redteam_<name>.md` listing every objection. If zero objections, the agent says so explicitly and shows what they searched for and didn't find.
4. **Resolution.** Every objection must be either: (a) refuted by the author (in writing, with a paragraph in the proof or a comment in the red-team file), or (b) accepted as a real flaw — back to theory.

**Pass criterion:** All red-team objections resolved. A claim with unresolved objections does not pass.

**Failure handling:** If the red-team finds a real error, the proof is wrong; revise or mark `[failed verification]` in `dead_ends.md`.

---

## Step 3 — Lean 4 formalization of core lemmas

**Purpose:** Achieve mechanically-verified ground truth on the load-bearing pieces. The Lean kernel, not human eyes, is the final referee for the formalized parts.

**Scope:** Every lemma that is **load-bearing** in the main theorem. A lemma is load-bearing if removing it breaks the proof. Auxiliary computational lemmas (e.g., "this specific union-closed family of size 12 has property X") are exempt — they are covered by Step 1.

**Procedure:**

1. **Translate** the statement of each core lemma into Lean 4 (using Mathlib for ambient definitions where possible: `Mathlib.Data.Nat`, `Mathlib.Combinatorics.SetFamily`, `Mathlib.Analysis.SpecialFunctions.Log`, `Mathlib.Probability.Independence`, etc.).
2. **State the lemma in Lean** even if we do not yet have a full Lean proof; the statement itself catches definitional ambiguities. Files live in `collatz/lean/` or `frankl/lean/`.
3. **Prove the lemma in Lean** as far as feasible:
   - For Frankl-side entropy bounds: Mathlib has Shannon-entropy infrastructure; this is tractable.
   - For Collatz-side stopping-time arithmetic: Mathlib has $p$-adic valuation and induction; this is tractable for the arithmetic core.
   - For results requiring extensive measure theory (Tao-style): a partial formalization of the discrete part is often enough.
4. **Use sorry sparingly.** A `sorry` in a load-bearing lemma means Step 3 has not passed for that lemma. List every remaining `sorry` in `<track>/lean/sorries.md` with the missing claim and a plausibility estimate.
5. **Compile and check** the Lean files with the project's Mathlib snapshot; the build artifact is the verification evidence.

**Pass criterion:** Every load-bearing lemma either (a) has a `sorry`-free Lean proof that compiles, or (b) is explicitly marked as "out of scope for Lean — covered by Steps 1, 2, and 4 only" with a written justification.

**Failure handling:** A lemma that we cannot formalize at all is suspicious. We either reduce the proof's reliance on it (refactor through provable lemmas) or escalate to "human deep review" in Step 4.

**Realism note:** Full Lean formalization of a Collatz or Frankl proof is a multi-month effort even for an established team. We do not expect to formalize the full main theorem in this project's lifetime. The standard is: formalize the **load-bearing core**, not the full paper.

---

## Step 4 — Human (Alex Ye) review

**Purpose:** Final human judgment. Decisive. Alex Ye signs off, or doesn't.

**Scope:** Every result that has passed Steps 1, 2, 3.

**Procedure:**

1. Alex Ye reads the full proof, the Step-1 test logs, the Step-2 red-team file, and the Lean compilation status.
2. Alex Ye explicitly considers: Do I believe this? Would I stake my reputation on it being correct? Would I bet $1000 it survives 12 months of public scrutiny?
3. Sign-off format: a one-line entry in `shared/verified_results.md`:

   ```
   YYYY-MM-DD  [track]  [short name]  verified by Alex Ye after Steps 1/2/3/4
   ```

4. If sign-off is conditional (e.g., "verified modulo the unformalized analytic step"), the condition is stated in the entry and in the paper's exposition.

**Pass criterion:** Alex Ye signs off in writing, in the `verified_results.md` log, with the date.

**Failure handling:** No sign-off = no publication. The proof goes back to theory or to `dead_ends.md`.

---

## When the protocol applies in reduced form

For routine claims that are **immediate from definitions** (e.g., "the empty family has frequency 0 for every element") we apply only Step 4. For claims that are **textbook cited results we are reusing** we cite the source and apply Step 4. The protocol's full force kicks in for any claim that is novel to this project, even mildly so.

For survey papers (no novel claims): Step 1 and Step 2 are still applied to the *bibliography* — every cited result must trace to a verified source. Step 3 is skipped. Step 4 is still required.

---

## Anti-patterns to refuse

- "Looks right to me" without Steps 1–3. Refused.
- "The proof is too long to Lean-formalize." Acceptable for sub-lemmas; not acceptable for the load-bearing core. Either reduce reliance, or break the lemma into smaller pieces.
- "I will check later." All checks are completed before "later." Otherwise the result stays in `<track>/theory/draft_<name>.md` with `[unverified]` in the title.
- "Claude verified it." Insufficient. Claude is the author of much of this work; Claude cannot also be the referee.
- "It worked on small cases." Necessary, not sufficient. Steps 2 and 3 are still required.

---

## File conventions

- `collatz/theory/` and `frankl/theory/` — drafts of proofs, with status tag `[unverified]`, `[step-1 passed]`, ..., `[verified]` in the filename or H1 title.
- `collatz/experiments/verify_<name>.py` and `frankl/experiments/verify_<name>.py` — Step 1 checkers.
- `collatz/red_team/` and `frankl/red_team/` — Step 2 outputs.
- `collatz/lean/` and `frankl/lean/` — Step 3 artifacts.
- `shared/verified_results.md` — Step 4 sign-off log (created lazily, on first verified result).
- `shared/dead_ends.md` — failed approaches; appended to as we go.

---

## Source of the protocol

Inspired by:

- Tao's blog discussions of Lean-assisted verification of the PFR conjecture.
- The DeepMind AlphaProof + Lean pipeline (Hubert et al., Nature 2025), where formal verification gates RL search.
- Math Inc.'s Gauss formalization of the strong PNT.
- The recurring lesson from Collatz folklore: many wrong proofs survive informal review for years.
- arXiv's 2025–2026 anti-slop policy: undisclosed unchecked content is now grounds for a 1-year ban.
