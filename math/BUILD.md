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
  - Collatz: `\T` (Collatz map), `\stop` (stopping time),
    `\totstop` (total stopping time), `\pv` (parity vector), `\logdens`.
- `\TODO{...}` and `\NOTE{...}` markers render in red/blue for
  in-draft annotations.

---

## 2. Lean 4 scaffolding

Lean 4 project lives at `math/lean/collatz_frankl/`.

```
math/lean/collatz_frankl/
  ├── lakefile.lean
  ├── lean-toolchain          # pins the Lean version
  ├── Collatz.lean            # root of Collatz library
  ├── Collatz/Basic.lean      # T, CollatzHolds, collatz_conjecture
  ├── Frankl.lean             # root of Frankl library
  └── Frankl/Basic.lean       # UnionClosed, abundance, frankl_conjecture
```

Both `collatz_conjecture` and `frankl_conjecture` are stated with `sorry`
bodies — they typecheck but are not proved.

### Prerequisites

Install `elan` (the Lean toolchain manager) and let it install the version
pinned in `lean-toolchain`:

```bash
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y
source ~/.elan/env
```

If the default `release.lean-lang.org` endpoint is firewalled in your
environment, you can side-load a release from GitHub:

```bash
# Example for v4.31.0-rc1 (matches lean-toolchain)
curl -L -o /tmp/lean.tar.zst \
  https://github.com/leanprover/lean4/releases/download/v4.31.0-rc1/lean-4.31.0-rc1-linux.tar.zst
mkdir -p ~/.elan/toolchains/leanprover--lean4---v4.31.0-rc1
tar --use-compress-program=unzstd -xf /tmp/lean.tar.zst \
  -C ~/.elan/toolchains/leanprover--lean4---v4.31.0-rc1 --strip-components=1
elan default leanprover/lean4:v4.31.0-rc1
```

### Mathlib dependency

`lakefile.lean` pulls Mathlib via a direct git URL (the Reservoir lookup
is bypassed because some sandboxed networks deny `reservoir.lean-lang.org`).
The pinned revision matches the Lean toolchain.

### Build

```bash
cd math/lean/collatz_frankl
lake update    # fetches Mathlib source (~slow first time)
lake build Collatz Frankl
```

If Mathlib's binary cache is reachable, `lake exe cache get` (after
`lake update`) substantially speeds up the first build. Without the cache,
the first build compiles Mathlib source from scratch and can take 1–2
hours on a fast machine.

Subsequent builds are incremental.

### Files

- `Collatz/Basic.lean` defines `T : ℕ → ℕ`, the iterated-map proposition
  `CollatzHolds n := ∃ k, T^[k] n = 1`, and the conjecture
  `collatz_conjecture : ∀ n, 0 < n → CollatzHolds n := by sorry`.
- `Frankl/Basic.lean` defines `UnionClosed`, the rational-valued
  `abundance`, and `frankl_conjecture` (with `sorry`).

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
