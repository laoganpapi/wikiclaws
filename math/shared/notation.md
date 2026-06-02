# Notation Conventions

**Project:** Collatz Conjecture and Frankl's Union-Closed Sets Conjecture
**Authors:** Alex Ye with Claude
**Purpose:** Single canonical notation used across all agents, drafts, and the final paper(s). When in doubt, defer to the conventions in Lagarias (Collatz) and Frankl / Gilmer (Union-Closed).

This file is the source of truth. If a draft deviates, it is the draft that is wrong.

---

## 1. General conventions

- $\mathbb{N} = \{1, 2, 3, \dots\}$ (positive integers; no zero).
- $\mathbb{N}_0 = \mathbb{N} \cup \{0\}$.
- $\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{R}$, $\mathbb{C}$ as usual.
- $\mathbb{Z}_p$ denotes the ring of $p$-adic integers; $\mathbb{Q}_p$ its fraction field.
- For $n \in \mathbb{N}$, $[n] := \{1, 2, \dots, n\}$.
- $2^{[n]}$ is the power set of $[n]$.
- $\log$ without subscript is the natural logarithm; $\log_2$ is binary; $\log_p$ is $p$-adic only when explicitly noted.
- $\lvert S \rvert$ is the cardinality of a finite set $S$.
- All limits, sums, and products range over $\mathbb{N}$ unless otherwise stated.
- $\nu_p(n)$ is the $p$-adic valuation of $n \in \mathbb{Z} \setminus \{0\}$: the unique nonneg. integer $k$ with $p^k \mid n$ but $p^{k+1} \nmid n$.
- $\lvert n \rvert_p := p^{-\nu_p(n)}$ is the $p$-adic norm.

---

## 2. Collatz / 3x+1 notation (Lagarias conventions)

We follow Lagarias, *The 3x+1 problem: An annotated bibliography* (Parts I–II) and *The Ultimate Challenge: The 3x+1 Problem* (AMS, 2010).

### 2.1 The maps

The **Collatz function** (full form):
$$
C(n) \;=\; \begin{cases} n/2 & n \text{ even} \\ 3n+1 & n \text{ odd.} \end{cases}
$$

The **Collatz map** (Lagarias's preferred form, which absorbs the trailing division by 2):
$$
T(n) \;=\; \begin{cases} n/2 & n \equiv 0 \pmod 2 \\ (3n+1)/2 & n \equiv 1 \pmod 2. \end{cases}
$$
We work with $T$ unless explicitly stated otherwise. $T : \mathbb{N} \to \mathbb{N}$. We extend $T$ to $\mathbb{Z}_2$ by the same formula on parity classes (this is well-defined and continuous).

The **Syracuse map** $S$ acts on odd integers and is obtained by composing $T$ until the result is again odd:
$$
S(n) \;=\; \frac{3n+1}{2^{\nu_2(3n+1)}} \qquad (n \text{ odd}).
$$
Equivalently $S = T^{a(n)+1}$ where $a(n) = \nu_2(3n+1)$.

### 2.2 Orbits, trajectories, parity sequences

The **forward orbit** of $n$ under $T$ is $\mathcal{O}_T(n) = \{T^k(n) : k \geq 0\}$ where $T^0(n) = n$ and $T^{k+1} = T \circ T^k$.

The **parity sequence** (or **parity vector**) of $n$ is the sequence
$$
\mathbf{v}(n) \;=\; \bigl(v_0(n), v_1(n), v_2(n), \dots\bigr), \qquad v_k(n) := T^k(n) \bmod 2 \in \{0,1\}.
$$
Truncations: $\mathbf{v}_k(n) := (v_0(n), \dots, v_{k-1}(n)) \in \{0,1\}^k$.

The **finite parity vector** $Q_k(n)$ of length $k$ is the same as $\mathbf{v}_k(n)$; we use $Q_k$ when emphasizing it as a function $Q_k : \mathbb{N} \to \{0,1\}^k$. Terras (1976) and Lagarias (1985) showed $Q_k$ induces a bijection $\mathbb{Z}/2^k\mathbb{Z} \to \{0,1\}^k$.

### 2.3 Stopping times

Three different stopping times appear in the literature; we standardize on the Lagarias forms.

**Stopping time** $\tau(n)$ — first time the orbit goes strictly below $n$:
$$
\tau(n) \;=\; \inf\bigl\{ k \geq 1 \;:\; T^k(n) < n \bigr\}.
$$

**Total stopping time** $\sigma_\infty(n)$ — first time the orbit reaches $1$:
$$
\sigma_\infty(n) \;=\; \inf\bigl\{ k \geq 0 \;:\; T^k(n) = 1 \bigr\}.
$$
The Collatz Conjecture is the statement $\sigma_\infty(n) < \infty$ for all $n \in \mathbb{N}$.

**Coefficient stopping time** $\gamma(n)$ — the least $k$ such that the parity vector $\mathbf{v}_k(n)$ has $\lambda_k(\mathbf{v}_k(n)) < 1$, where $\lambda_k$ is the multiplier function defined in 2.4.

Total stopping time **ratio** (used in normalized statements):
$$
\rho(n) := \frac{\sigma_\infty(n)}{\log n}.
$$

### 2.4 Multipliers and the affine form

Given a parity vector $\mathbf{e} = (e_0, \dots, e_{k-1}) \in \{0,1\}^k$, with $s_k(\mathbf{e}) := \sum_{i<k} e_i$ (the number of odd steps), $T^k$ acts on residues with parity vector $\mathbf{e}$ as an affine map
$$
T^k(n) \;=\; \lambda_k(\mathbf{e}) \, n + \beta_k(\mathbf{e}),
$$
where
$$
\lambda_k(\mathbf{e}) \;=\; \frac{3^{s_k(\mathbf{e})}}{2^k} \qquad \text{and} \qquad \beta_k(\mathbf{e}) \in \mathbb{Z}\bigl[\tfrac{1}{2}\bigr].
$$

### 2.5 Extensions and 2-adic structure

The map $T$ extends to a continuous, measure-preserving (w.r.t. Haar measure on $\mathbb{Z}_2$) map $T_\infty : \mathbb{Z}_2 \to \mathbb{Z}_2$. The parity-vector map extends to a continuous bijection $Q_\infty : \mathbb{Z}_2 \to \mathbb{Z}_2$ (identifying $\{0,1\}^\mathbb{N}$ with $\mathbb{Z}_2$ via base-2 expansion).

### 2.6 3-adic norm, statistical objects

For random-model statements, we use:
- $\mu_2$: Haar measure on $\mathbb{Z}_2$.
- $\mathbb{P}_n$: uniform probability on $\{1, 2, \dots, n\}$.
- Logarithmic density: $\delta_{\log}(A) := \lim_{N\to\infty} \frac{1}{\log N} \sum_{n \in A, n \leq N} 1/n$ (when limit exists).
- Tao's "almost bounded" statement uses logarithmic density on $\mathbb{N}$.

---

## 3. Frankl / Union-Closed notation

We follow Frankl's original formulation, Gilmer's 2022 entropy paper (arXiv:2211.09055), and the Sawin / Chase-Lovett / Alweiss-Huang-Sellke refinements.

### 3.1 Families and ground set

The **ground set** is $[n] := \{1, \dots, n\}$.

A **family** $\mathcal{F} \subseteq 2^{[n]}$ is a collection of subsets of $[n]$. We always assume $\mathcal{F}$ is finite and nonempty.

$\mathcal{F}$ is **union-closed** if for every $A, B \in \mathcal{F}$ we have $A \cup B \in \mathcal{F}$.

To avoid the trivial counterexample we assume $\mathcal{F} \neq \{\emptyset\}$; equivalently $\bigcup_{A \in \mathcal{F}} A \neq \emptyset$.

### 3.2 Frequency, abundance, frequent elements

The **frequency** of $x \in [n]$ in $\mathcal{F}$ is
$$
f_\mathcal{F}(x) \;=\; \bigl\lvert \{ A \in \mathcal{F} : x \in A \} \bigr\rvert.
$$
The **abundance** of $x$ is $f_\mathcal{F}(x) / \lvert \mathcal{F} \rvert \in [0,1]$.

An element $x$ is **abundant** (or "frequent") if its abundance is $\geq 1/2$.

**Frankl's Union-Closed Sets Conjecture (UCC).** For every finite union-closed family $\mathcal{F}$ with $\mathcal{F} \neq \{\emptyset\}$, there exists $x \in [n]$ with $f_\mathcal{F}(x) \geq \lvert \mathcal{F} \rvert / 2$.

For a constant $c \in (0, 1/2]$, the **$c$-UCC** is the weaker statement: some $x$ has abundance $\geq c$.

### 3.3 Entropy notation (Gilmer line)

For a discrete random variable $X$ on a finite alphabet, **Shannon entropy** (in nats; switch to $\log_2$ explicitly for bits when needed):
$$
H(X) \;=\; -\sum_x \mathbb{P}(X = x) \log \mathbb{P}(X = x).
$$
**Conditional entropy:** $H(X \mid Y) = H(X, Y) - H(Y)$.

**Mutual information:** $I(X; Y) = H(X) + H(Y) - H(X, Y) = H(X) - H(X \mid Y)$.

For a Bernoulli-$p$ random variable $B_p$ we write $h(p) := H(B_p) = -p\log p - (1-p)\log(1-p)$ (binary entropy, in nats).

### 3.4 The Gilmer setup

Let $A, B$ be i.i.d. samples from a distribution $\mu$ on $\mathcal{F}$. Gilmer's argument analyses
$$
H(A \cup B) \quad \text{vs.} \quad H(A).
$$
Define the **per-coordinate marginal** $p_i = \mathbb{P}(i \in A)$, viewing $A$ as $\mathbf{1}_A \in \{0,1\}^n$. The union law:
$$
\mathbb{P}(i \in A \cup B) \;=\; 1 - (1 - p_i)^2 \;=\; 2 p_i - p_i^2.
$$

### 3.5 Approximately union-closed (Gilmer's relaxation)

For $\varepsilon \in [0,1]$, a family $\mathcal{F}$ is **$\varepsilon$-approximately union-closed** with respect to a distribution $\mu$ on $\mathcal{F}$ if
$$
\mathbb{P}_{A, B \sim \mu}\bigl( A \cup B \in \mathcal{F} \bigr) \;\geq\; 1 - \varepsilon.
$$
Gilmer's argument proves: if $\mathcal{F}$ is $\varepsilon$-approximately union-closed for some explicit $\varepsilon(p)$, then there exists $i$ with $p_i \geq c$. This relaxation is essential to the entropy method.

### 3.6 The Frankl constant

$$
c^* \;:=\; \sup \bigl\{ c \in (0, 1/2] \;:\; c\text{-UCC holds for all finite union-closed } \mathcal{F} \neq \{\emptyset\} \bigr\}.
$$
- Frankl conjectures $c^* = 1/2$.
- Gilmer 2022: $c^* \geq 0.01$ (later $\geq 3 - 2\sqrt{2} \approx 0.172$ in the same paper, refined).
- Sawin / Chase-Lovett / Pebody / Alweiss-Huang-Sellke (Nov 2022): $c^* \geq (3-\sqrt 5)/2 \approx 0.38197$.
- Cambie 2023+: minor improvements; the entropy method is conjectured by Gilmer to cap at $(3-\sqrt 5)/2$.

### 3.7 Other Frankl-flavor objects

- The **trace** of $\mathcal{F}$ on $S \subseteq [n]$: $\mathcal{F}|_S = \{ A \cap S : A \in \mathcal{F}\}$.
- The **link** of $x$: $\mathcal{F}_x = \{ A \in \mathcal{F} : x \in A\}$.
- The **deletion**: $\mathcal{F} \setminus x = \{ A \setminus \{x\} : A \in \mathcal{F}\}$.

---

## 4. LaTeX macros (drop into `macros.tex`)

Save as `macros.tex` and `\input{macros}` at the top of any draft. These macros are deliberately conservative: no semantic redefinitions of common symbols, no exotic packages required.

```latex
% =========================================================
% macros.tex
% Collatz + Frankl shared macros. Drop into preamble via
%   \input{macros}
% Requires: amsmath, amssymb, mathtools (recommended).
% =========================================================

% --- General number systems ---
\newcommand{\NN}{\mathbb{N}}
\newcommand{\ZZ}{\mathbb{Z}}
\newcommand{\QQ}{\mathbb{Q}}
\newcommand{\RR}{\mathbb{R}}
\newcommand{\CC}{\mathbb{C}}
\newcommand{\FF}{\mathbb{F}}
\newcommand{\Zp}{\mathbb{Z}_p}
\newcommand{\Qp}{\mathbb{Q}_p}
\newcommand{\Ztwo}{\mathbb{Z}_2}
\newcommand{\Zthree}{\mathbb{Z}_3}

% --- General ---
\newcommand{\eps}{\varepsilon}
\newcommand{\set}[1]{\{#1\}}
\newcommand{\setbuild}[2]{\{#1 \,:\, #2\}}
\newcommand{\abs}[1]{\left\lvert #1 \right\rvert}
\newcommand{\norm}[1]{\left\lVert #1 \right\rVert}
\newcommand{\inner}[2]{\langle #1, #2 \rangle}
\newcommand{\bigO}{O}
\newcommand{\smallo}{o}
\newcommand{\indicator}{\mathbf{1}}
\newcommand{\onevec}{\mathbf{1}}
\DeclareMathOperator*{\argmin}{arg\,min}
\DeclareMathOperator*{\argmax}{arg\,max}
\DeclareMathOperator{\dom}{dom}
\DeclareMathOperator{\supp}{supp}
\DeclareMathOperator{\val}{val}

% --- p-adic ---
\newcommand{\nuP}{\nu_p}
\newcommand{\nuTwo}{\nu_2}
\newcommand{\nuThree}{\nu_3}
\newcommand{\absp}[1]{\abs{#1}_p}

% --- Collatz / 3x+1 ---
% Maps
\newcommand{\Collatz}{C}                  % full Collatz function (n/2 or 3n+1)
\newcommand{\Cmap}{T}                     % Lagarias map (default); n/2 or (3n+1)/2
\newcommand{\Syr}{S}                      % Syracuse map on odd integers
\newcommand{\Cext}{T_{\infty}}            % 2-adic extension of T
% Iterates
\newcommand{\iter}[2]{#1^{#2}}            % T^k(n): \iter{\Cmap}{k}(n)
% Orbits
\newcommand{\orbit}[1]{\mathcal{O}_{\Cmap}(#1)}
% Parity
\newcommand{\parity}{\mathbf{v}}          % parity sequence
\newcommand{\parityk}[1]{\parity_{#1}}    % truncated parity vector of length k
\newcommand{\Qk}{Q_k}                     % Terras-Lagarias parity map
\newcommand{\Qinf}{Q_{\infty}}
\newcommand{\sk}[1]{s_k(#1)}              % # of odd steps in parity vector
% Multipliers
\newcommand{\lamk}{\lambda_k}
\newcommand{\betk}{\beta_k}
% Stopping times
\newcommand{\stopT}{\tau}                 % stopping time: first k with T^k(n) < n
\newcommand{\stopInf}{\sigma_{\infty}}    % total stopping time: first k with T^k(n) = 1
\newcommand{\stopCoeff}{\gamma}           % coefficient stopping time
% Statistical
\newcommand{\Haar}{\mu_2}
\newcommand{\Plog}{\delta_{\log}}         % logarithmic density

% --- Frankl / Union-closed ---
\newcommand{\family}{\mathcal{F}}
\newcommand{\ucfam}{\mathcal{F}}          % alias when emphasizing union-closure
\newcommand{\ground}[1][n]{[#1]}          % ground set [n]
\newcommand{\powerset}[1]{2^{#1}}
\newcommand{\freq}[2][\family]{f_{#1}(#2)}        % frequency f_F(x)
\newcommand{\abund}[2][\family]{\freq[#1]{#2} / \abs{#1}} % abundance
\newcommand{\trace}[2]{#1\big|_{#2}}      % \trace{F}{S}
\newcommand{\link}[2][\family]{#1_{#2}}    % link F_x
\newcommand{\del}[2][\family]{#1 \setminus #2} % deletion F \ x
\newcommand{\cstar}{c^{\ast}}             % Frankl constant
% Entropy
\newcommand{\entropy}{H}
\newcommand{\condent}[2]{\entropy(#1 \mid #2)}
\newcommand{\mutinf}[2]{I(#1 ; #2)}
\newcommand{\bent}{h}                     % binary entropy function

% --- Theorem-like (use only if not already defined by your class file) ---
% \newtheorem{theorem}{Theorem}[section]
% \newtheorem{lemma}[theorem]{Lemma}
% \newtheorem{proposition}[theorem]{Proposition}
% \newtheorem{corollary}[theorem]{Corollary}
% \theoremstyle{definition}
% \newtheorem{definition}[theorem]{Definition}
% \newtheorem{example}[theorem]{Example}
% \newtheorem{remark}[theorem]{Remark}

% --- Citation shorthands (optional) ---
\newcommand{\Lagarias}{\textsc{Lagarias}}
\newcommand{\Tao}{\textsc{Tao}}
\newcommand{\Gilmer}{\textsc{Gilmer}}
\newcommand{\Frankl}{\textsc{Frankl}}
```

---

## 5. Cross-track conventions

When both problems are discussed in the same document:

- Use $\family$ (calligraphic) for Frankl families; never overload it with Collatz objects.
- Use $T$ for the Collatz map; never as a generic "transformation" elsewhere in a paper that also touches Frankl.
- The letter $n$ is the ground-set size for Frankl AND a generic integer for Collatz. Disambiguate locally: "Let $n \in \NN$ be a positive integer (Collatz)" / "Let $n$ be the ground-set size (Frankl)."
- Use $k$ for parity-vector length / iteration count (Collatz) and for "rank" parameters in Frankl entropy proofs; rename in any joint section.

---

## 6. Sources

- J. C. Lagarias, *The 3x+1 problem: An annotated bibliography (1963-1999)*, arXiv:math/0309224.
- J. C. Lagarias (ed.), *The Ultimate Challenge: The 3x+1 Problem*, AMS, 2010.
- R. Terras, *A stopping time problem on the positive integers*, Acta Arithmetica 30 (1976).
- T. Tao, *Almost all orbits of the Collatz map attain almost bounded values*, arXiv:1909.03562, 2019.
- J. Gilmer, *A constant lower bound for the union-closed sets conjecture*, arXiv:2211.09055, 2022.
- W. Sawin, *An improved lower bound for the union-closed set conjecture*, arXiv:2211.11504, 2022.
- Z. Chase and S. Lovett, *Approximate union closed conjecture*, arXiv:2211.11689, 2022.
- R. Alweiss, B. Huang, M. Sellke, *Improved lower bound for union-closed sets conjecture*, arXiv:2211.11731, 2022.
- L. Pebody, *Extension of a method of Gilmer*, arXiv:2211.13139, 2022.
- S. Cambie, *Better bounds for the union-closed sets conjecture using the entropy approach*, 2022.
