/-
  Collatz/Basic.lean

  Foundational definitions for the Collatz $3n+1$ problem.

  Authors: Alex Ye with Claude (Anthropic).
  Branch: claude/epic-dirac-p1oQo.

  NOTE: this file is deliberately written against Lean core + the
  pre-built `Init` library so that it typechecks without a full
  Mathlib build. Once Mathlib is available locally
  (`lake build` or `lake exe cache get`), the comments below indicate
  the natural Mathlib upgrade paths.
-/

namespace Collatz

/-- The Collatz map `T : ℕ → ℕ`:
    `T n = n / 2`   if `n` is even,
    `T n = 3 n + 1` if `n` is odd. -/
def T (n : Nat) : Nat :=
  if n % 2 = 0 then n / 2 else 3 * n + 1

/-- Iterate `T` a given number of times.  Once Mathlib is available,
    this can be replaced by `Function.iterate` from
    `Mathlib.Logic.Function.Iterate` (notation: `T^[k]`). -/
def Titer (n : Nat) : Nat → Nat
  | 0 => n
  | k + 1 => T (Titer n k)

/-- "Collatz holds for `n`": the orbit of `n` under `T` eventually reaches `1`. -/
def CollatzHolds (n : Nat) : Prop :=
  ∃ k : Nat, Titer n k = 1

/-- The Collatz conjecture: `CollatzHolds n` for every positive integer `n`. -/
theorem collatz_conjecture : ∀ n : Nat, 0 < n → CollatzHolds n := by
  sorry

end Collatz
