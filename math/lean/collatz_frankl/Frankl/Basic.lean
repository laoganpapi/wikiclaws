/-
  Frankl/Basic.lean

  Foundational definitions for Frankl's union-closed sets conjecture.

  Authors: Alex Ye with Claude (Anthropic).
  Branch: claude/epic-dirac-p1oQo.
-/

import Mathlib.Data.Finset.Basic
import Mathlib.Data.Set.Basic
import Mathlib.Data.Rat.Defs

namespace Frankl

variable {α : Type*} [DecidableEq α]

/-- A family `F` of finite subsets of a type `α` is *union-closed* if it is
    closed under binary unions. -/
def UnionClosed (F : Finset (Finset α)) : Prop :=
  ∀ A ∈ F, ∀ B ∈ F, A ∪ B ∈ F

/-- The *abundance* of an element `i` in a family `F` is the fraction of
    members of `F` containing `i`. Returned as a rational. -/
noncomputable def abundance (F : Finset (Finset α)) (i : α) : ℚ :=
  ((F.filter (fun A => i ∈ A)).card : ℚ) / (F.card : ℚ)

/-- Frankl's union-closed sets conjecture: every finite union-closed family
    other than `{∅}` contains an element of abundance at least `1/2`. -/
theorem frankl_conjecture
    (F : Finset (Finset α)) (hUC : UnionClosed F)
    (hne : F ≠ {∅}) (hnempty : F.Nonempty) :
    ∃ i : α, abundance F i ≥ (1 / 2 : ℚ) := by
  sorry

end Frankl
