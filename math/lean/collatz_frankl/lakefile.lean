import Lake
open Lake DSL

package "collatz_frankl" where
  -- Settings applied to both builds and interactive editing
  leanOptions := #[
    ⟨`pp.unicode.fun, true⟩ -- pretty-prints `fun a ↦ b`
  ]

-- Mathlib pulled from GitHub directly (Reservoir is not reachable in this
-- sandbox; using the git URL avoids the lookup).
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.31.0-rc1"

@[default_target]
lean_lib «Collatz» where
  -- The Collatz library

@[default_target]
lean_lib «Frankl» where
  -- The Frankl library
