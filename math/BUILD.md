# BUILD.md — Building the math research artifacts

Authors: Alex Ye with Claude (Anthropic)
Branch: `claude/epic-dirac-p1oQo`

This document describes how to build the LaTeX papers and the Lean 4
scaffolding locally and in CI.

---

## 1. LaTeX papers

Two papers live under `math/`:

```
math/frankl/paper/
  ├── main.tex          # entry point
  ├── macros.tex        # local notation
  └── bibliography.bib  # references

math/collatz/paper/
  ├── main.tex
  ├── macros.tex
  └── bibliography.bib
```

### Prerequisites

```bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-bibtex-extra \
    texlive-fonts-recommended \
    latexmk
```

### Build

From the repo root:

```bash
# Frankl
cd math/frankl/paper
latexmk -pdf -interaction=nonstopmode main.tex

# Collatz
cd ../../collatz/paper
latexmk -pdf -interaction=nonstopmode main.tex
```

`latexmk` runs `pdflatex` and `bibtex` the required number of times.
The resulting `main.pdf` lives in each paper directory.

To clean intermediate files:

```bash
latexmk -C
```

### Style choices

- `amsart` document class.
- `natbib` with `numbers,sort&compress` for citations.
- `bibtex` (via `\bibliography{bibliography}`) — not biblatex, for maximal
  portability with arXiv and amsart.
- Local macros in `macros.tex`. Common names:
  - Frankl: `\UC` (a union-closed family), `\abun` (abundance),
    `\E`, `\HH` (Shannon entropy), `\target` ($\tfrac{1}{2}$), `\golden`
    ($\tfrac{3-\sqrt 5}{2}$).
  - Collatz: `\T` (Collatz map), `\stop` (stopping time, override of a
    LaTeX primitive via `\renewcommand`), `\totstop` (total stopping
    time), `\pv` (parity vector), `\logdens`.
- `\TODO{...}` and `\NOTE{...}` markers render in red/blue for
  in-draft annotations.

### Known compile-time gotchas

- `amsart` requires `\thanks{...}` to appear **after** the closing `}` of
  `\author{...}`, not inside it. Both papers follow this layout.
- `\Pr` is already defined by `amsmath`; the macros files use
  `\renewcommand{\Pr}{\mathbb{P}}` to override.
- `\stop` is a LaTeX primitive; the Collatz `macros.tex` uses
  `\renewcommand` to install the stopping-time meaning.

---

## 2. Lean 4 scaffolding

Lean 4 project lives at `math/lean/collatz_frankl/`.

```
math/lean/collatz_frankl/
  ├── lakefile.lean
  ├── lean-toolchain          # pins the Lean version (v4.31.0-rc1)
  ├── Collatz.lean            # root of Collatz library
  ├── Collatz/Basic.lean      # T, Titer, CollatzHolds, collatz_conjecture
  ├── Frankl.lean             # root of Frankl library
  └── Frankl/Basic.lean       # UnionClosed, freq, frankl_conjecture
```

Both `collatz_conjecture` and `frankl_conjecture` are stated with `sorry`
bodies — they typecheck but are not proved.

### Prerequisites

Install `elan` (the Lean toolchain manager):

```bash
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y
source ~/.elan/env
```

`elan` resolves Lean releases through `release.lean-lang.org`. If that
endpoint is firewalled (some sandboxed networks deny it), you can
side-load a release archive from GitHub instead:

```bash
# Example for v4.31.0-rc1 (matches lean-toolchain)
sudo apt-get install -y zstd
curl -L -o /tmp/lean.tar.zst \
  https://github.com/leanprover/lean4/releases/download/v4.31.0-rc1/lean-4.31.0-rc1-linux.tar.zst
mkdir -p ~/.elan/toolchains/leanprover--lean4---v4.31.0-rc1
tar --use-compress-program=unzstd -xf /tmp/lean.tar.zst \
  -C ~/.elan/toolchains/leanprover--lean4---v4.31.0-rc1 --strip-components=1
elan default leanprover/lean4:v4.31.0-rc1
```

### Build (current configuration: stdlib only)

```bash
cd math/lean/collatz_frankl
lake build Collatz Frankl
```

Expected output: build completes in seconds, with two `sorry`
warnings — one per conjecture. That is success.

### Mathlib upgrade path (optional)

The `Basic.lean` files are written against Lean core so that they
typecheck in environments without a full Mathlib build (compiling
Mathlib from source takes 1–2 hours on a fast machine). To upgrade:

1. Uncomment the `require mathlib` block in `lakefile.lean`. The
   `require` uses a direct GitHub URL because Reservoir
   (`reservoir.lean-lang.org`) is unreachable in some sandbox networks.
2. Run `lake update`.
3. Optionally pull pre-built `.olean` cache:
   `lake exe cache get`.
   (This requires the Azure-hosted Mathlib cache to be reachable.
   It is also commonly firewalled; if so, the next step compiles
   Mathlib from source.)
4. Rewrite `Collatz/Basic.lean` to use `Function.iterate` (notation
   `T^[k]`) from `Mathlib.Logic.Function.Iterate`.
5. Rewrite `Frankl/Basic.lean` to use `Finset (Finset α)` and
   rational-valued abundance from `Mathlib.Data.Finset.Basic` and
   `Mathlib.Data.Rat.Defs`.

### Files

- `Collatz/Basic.lean` defines `T : Nat → Nat`, an explicit iterate
  `Titer n k`, the proposition `CollatzHolds n := ∃ k, Titer n k = 1`,
  and the conjecture
  `collatz_conjecture : ∀ n, 0 < n → CollatzHolds n := by sorry`.
- `Frankl/Basic.lean` defines a `Family` as `List (List α)`,
  `UnionClosed`, `freq`, and the conjecture
  `frankl_conjecture : ... ∃ a, 2 * freq a F ≥ F.length := by sorry`.

---

## 3. CI

The GitHub Actions workflow at `.github/workflows/math-build.yml`
runs on every push and pull request that touches `math/**` on the
`claude/epic-dirac-p1oQo` branch.

- `build-papers` always runs and uploads `frankl-paper` and
  `collatz-paper` as workflow artifacts.
- `build-lean` is best-effort: it warns rather than fails if `elan`
  cannot be installed or if `lake build` errors out. This is so that
  paper progress is never blocked by Lean infrastructure churn.

Manually trigger via `workflow_dispatch` in the Actions UI.

---

## 4. Provenance & infrastructure notes

The initial setup was performed under `claude/epic-dirac-p1oQo` on
2026-06-02. Infrastructure roadblocks encountered and their resolutions:

| Issue | Resolution |
|---|---|
| `release.lean-lang.org` returned HTTP 403 | Side-loaded Lean toolchain from `github.com/leanprover/lean4/releases`. |
| `reservoir.lean-lang.org` returned HTTP 403 | Used direct git URL in `lakefile.lean` to require Mathlib. |
| Mathlib binary cache (Azure blob storage) returned HTTP 403 | Documented; users with cache access can run `lake exe cache get`; otherwise compile from source. |
| Full Mathlib source build is multi-hour | Default `Basic.lean` files use Lean stdlib only so the scaffolding typechecks in seconds. Mathlib upgrade path documented above. |
