import Lake
open Lake DSL

package "collatz_frankl" where
  -- Settings applied to both builds and interactive editing.
  leanOptions := #[
    ⟨`pp.unicode.fun, true⟩
  ]

-- Mathlib is optional for the scaffolding. To enable, uncomment the
-- `require` below and re-run `lake update`. We pull from GitHub
-- directly because Reservoir is unreachable in some sandbox networks.
-- require mathlib from git
--   "https://github.com/leanprover-community/mathlib4.git" @ "v4.31.0-rc1"

@[default_target]
lean_lib «Collatz» where

@[default_target]
lean_lib «Frankl» where
