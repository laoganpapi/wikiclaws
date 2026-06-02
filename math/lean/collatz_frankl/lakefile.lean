import Lake
open Lake DSL

package "collatz_frankl" where
  -- Settings applied to both builds and interactive editing
  leanOptions := #[
    ⟨`pp.unicode.fun, true⟩ -- pretty-prints `fun a ↦ b`
  ]

require "leanprover-community" / "mathlib"

@[default_target]
lean_lib «Collatz» where
  -- The Collatz library

@[default_target]
lean_lib «Frankl» where
  -- The Frankl library
