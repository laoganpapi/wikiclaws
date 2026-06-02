/-
  Collatz/Basic.lean

  Foundational definitions for the Collatz $3n+1$ problem.

  Authors: Alex Ye with Claude (Anthropic).
  Branch: claude/epic-dirac-p1oQo.
-/

import Mathlib.Data.Nat.Basic
import Mathlib.Logic.Function.Iterate

namespace Collatz

/-- The Collatz map `T : ℕ → ℕ`:
    `T n = n / 2`   if `n` is even,
    `T n = 3 n + 1` if `n` is odd. -/
def T (n : ℕ) : ℕ :=
  if n % 2 = 0 then n / 2 else 3 * n + 1

@[simp] lemma T_even {n : ℕ} (h : n % 2 = 0) : T n = n / 2 := by
  unfold T; simp [h]

@[simp] lemma T_odd {n : ℕ} (h : n % 2 = 1) : T n = 3 * n + 1 := by
  unfold T
  have h0 : n % 2 ≠ 0 := by omega
  simp [h0]

/-- "Collatz holds for `n`": the orbit of `n` under `T` eventually reaches `1`. -/
def CollatzHolds (n : ℕ) : Prop :=
  ∃ k : ℕ, T^[k] n = 1

/-- The Collatz conjecture: `CollatzHolds n` for every positive integer `n`. -/
theorem collatz_conjecture : ∀ n : ℕ, 0 < n → CollatzHolds n := by
  sorry

end Collatz
