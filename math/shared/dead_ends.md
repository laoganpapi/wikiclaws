# Dead Ends — Approaches That Did Not Work

**Project:** Collatz + Frankl research project
**Authors:** Alex Ye with Claude
**Purpose:** Record every approach that we tried and that failed (computationally falsified, found in the prior literature as already-defeated, proven impossible, or abandoned after time-boxed effort).

Agents must read this file before launching a new attack vector to avoid re-doing failed work. Agents must append to this file whenever an approach fails the verification protocol or is otherwise abandoned.

This file is part of the project's honesty discipline: negative results are valuable. Recording them protects us and others from wasted cycles.

---

## How to add an entry

Append a new H2 section with the template below. Entries are append-only; do not delete or edit prior entries (correct earlier mistakes only by adding a follow-up entry that references the earlier one).

```
## YYYY-MM-DD — [track: collatz|frankl|cross] — [short descriptive title]

**Agent / author:** [agent name and/or Alex Ye]
**Time invested:** [e.g., 4 hours of compute / 2 days of theory]
**Attack vector:** [one paragraph: what was the plan]
**Why it failed:** [one to three paragraphs: the specific obstruction, with line/file references to the failed attempt]
**Counter-example (if any):** [explicit input where the claim/method breaks, or "n/a"]
**Pointer to artifacts:** [files in track/ subdirs that show the failed work]
**Verdict:** [one of: falsified, prior-art, computationally infeasible, gap-not-closeable, abandoned]
**Lesson:** [what we learned that informs future attacks]
```

---

## Entries

## 2026-06-02 — [collatz] — Cycle exclusion (Vector C): three dead ends — see `collatz/theory/dead_ends.md`

**Agent / author:** Alex Ye (AI-assisted).
**Time invested:** ~4 hours theory + source verification.
**Attack vector:** Improve Hercher's $m\le 91$ cycle-exclusion bound, per Vector C.
**Why it failed (summary; full entries in `collatz/theory/dead_ends.md`):**
1. *Improving $\mu(\log_2 3)$ does not help* — structural: the cycle proof needs an
   exponential-in-$K$ lower bound on the two-log form $\Lambda=N\log2-K\log3$ to cap the
   cycle length from above; the (polynomial) irrationality measure gives only a lower bound on $K$.
   Corrects `survey.md` §7.5/§11 and `open_problems.md` D.1/D.2.
2. *Mis-framed Step-1 check (C5 v1)* — compared bound magnitudes instead of decay direction;
   caught and corrected (Step-1 self-error).
3. *Computing a concrete $m^\*>91$ here* — blocked: all academic PDF hosts returned HTTP 403,
   so Hercher's explicit $F(m,\log B)$ and the Laurent-2008 constant were unavailable.
**Counter-example (if any):** n/a (1 and 3 structural/blocked; 2 = the FALSE check output).
**Pointer to artifacts:** `collatz/theory/cycle_exclusion_explicit.md`,
`collatz/experiments/verify_cycle_exclusion.py`, `collatz/experiments/verify_cycle_exclusion_log.md`,
`collatz/theory/dead_ends.md` (Vector C section).
**Verdict:** (1) gap-not-closeable via that route; (2) falsified-then-corrected; (3) abandoned-in-environment.
**Lesson:** The cycle-exclusion lever is the **two-log linear-forms estimate** (const $24.34D^4$ /
de Weger exponent $0.158$) + the verification bound $B$ + circuit averaging — not $\mu(\log_2 3)$.

*(append further entries above this line as approaches fail)*
