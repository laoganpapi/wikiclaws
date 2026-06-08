# Sustained Collatz Team — Status After Wave 4

## The barrier in its final form

After 5 waves and ~40 agent runs, the strengthened LDP-natural-density barrier stands as:

> **Theorem (consolidated).** For every k ≥ 2 and every measure ν on the Bernoulli sequence space ℤ₊^ℕ satisfying:
> - ν has well-defined per-coord support ⊆ ℤ₊;
> - The Cesàro per-coord drift mean exists and equals log₂3 (drift balance);
> - The Syracuse pushforward of ν has uniform mod-3^k marginal on (ℤ/3^k)*;
>
> Such ν does not exist. Equivalently, in any candidate route to natural density via reweighting the Bernoulli base measure, the trio (drift balance, uniform mod-3^k saturation, well-defined Cesàro frequencies) is incompatible.

**The proof:** elementary support-floor identity E_ν[a] = (1/m_k) Σ_c E[a | a ≡ c] ≥ (1/m_k) Σ_c c = (m_k+1)/2 = 3^(k−1) + 1/2 > log₂3 for k ≥ 2 (Verifier Wave 3); robustness margin TV ≥ 0.294 (Verifier Wave 2); pathology coverage by Choquet decomposition + category-mismatch (Frontier Wave 4); two-step proof for finite-KL via Lanford–Ruelle (Frontier Wave 2).

**Confidence:** conceptually complete ~95%; formally complete ~85% (the (F1′-a-2) soft step requires a category statement about natural density being shift-stationary-defined; can be formalized).

## What it does NOT close

| Frontier | Why it survives the barrier | Has the team produced a candidate? |
|----------|----------------------------|------------------------------------|
| (F2-add) additive combinatorics | Doesn't go via reweighting μ_0 | No — sum-product / Markoff cleanly negative |
| (F2-padic) p-adic / Berkovich | Doesn't tilt; uses different measure category | No — p-adic alt-angle gave a Livšic coboundary (also closed) |
| (F2-furst) Furstenberg multiple-recurrence | Doesn't tilt; ergodic-theory framework different | No — explored under ergodic theory wave, came back negative |
| (F2-noncom) noncommutative geometry | Could escape via Type-III KMS / infinite-KL | No — KMS wave reduced to LDP barrier |
| (F2-sieve) sieve / analytic NT on integers | Integer-side, not symbol-space | **One open signal: Q3 smoothness 24% drop — control test running NOW** |

## The one live frontier

**Sieve Q3:** y=10 smooth Collatz numbers in dyadic shell [16,20) show a 24% drop in mean σ∞/log₂n vs all integers. Survived dyadic-shell stratification. **The deciding v_2(n) control test is running**: if the gap closes after matching 2-adic valuation, the signal was the trivial "smooth integers are even-rich, free halvings" artifact. If it survives, sieve methods on integer orbits become the **only surviving non-LDP attack route the team has identified.**

## Two surviving paper-worthy results

| Half of Collatz | Result | Confidence |
|----------------|--------|------------|
| Density side | Strengthened 4-layer LDP-tractable barrier + Class C mod-3 saturation + drift LDP refinement of Tao 2022 | High (now elementary) |
| Cycle side | κ-conditional cycle-exclusion theorem, m*(2^71) ∈ {91, 92} unconditional; rows up to 107 conditional on primary-source κ | Honest scoped |

Both in Collatz paper at 23pp.

## Iteration rule going forward
- If Sieve Q3 control passes: pivot Synthesis to fold the smoothness signal as a third open frontier; relaunch Frontier on the Hildebrand framework.
- If Sieve Q3 control fails: the team has genuinely exhausted the actionable structural frontier; the deliverable is the consolidated paper + final-status doc; the next-session move is the network-enabled prior-art pass.
