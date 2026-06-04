"""
Independent check of the alleged sign correction.

We're checking the agent's claim that the previous candidate's '1/6 -> 0.096'
mod-3 attenuation used a tilt that doesn't actually drift-balance the cocycle.

Setup (from collatz_livsic.md / collatz_thermo_probe.py):
- Bernoulli base measure: a ~ Geom(1/2) on {1,2,3,...}, i.e. P(a=k) = 2^(-k).
- Cocycle: phi(a) = log(3) - a*log(2).  Mean E_mu0[phi] = log3 - 2 log2 < 0 (descent).
- Esscher family: P_s(a=k) ∝ 2^(-k) * exp(-s*phi(k)) = 2^(-k) * exp(s*a*log2) * exp(-s*log3)
                                                 ∝ 2^((s-1)*k)  (geometric in k, parameter 2^(s-1))
  So P_s(a=k) = (1 - 2^(s-1)) * 2^((s-1)*k * ... )  -- careful, let's redo cleanly:
  Let r = 2^(s-1). For convergence need r < 1, i.e. s < 1. Then
    Z(s) = sum_{k>=1} 2^(-k) * exp(-s*(log3 - k log2))
         = exp(-s log3) * sum_{k>=1} 2^(-k) * 2^(s*k)
         = exp(-s log3) * sum_{k>=1} 2^((s-1)*k)
         = exp(-s log3) * r/(1-r)
  P_s(a=k) = 2^(-k) exp(-s*phi(k)) / Z(s)
           = (1-r) * r^(k-1)    (Geom(1-r) on {1,2,...})

So under P_s, a ~ Geom(1-r), mean E_s[a] = 1/(1-r) = 1/(1 - 2^(s-1)).

Drift balancing: E_s[phi] = log3 - E_s[a] log2 = 0
  => E_s[a] = log(3)/log(2) = log_2 3 ≈ 1.585
  => 1/(1 - 2^(s_star-1)) = log_2 3
  => 1 - 2^(s_star-1) = 1/log_2 3
  => 2^(s_star-1) = 1 - 1/log_2 3 = (log_2 3 - 1)/log_2 3
  => s_star - 1 = log_2((log_2 3 - 1)/log_2 3)
  => s_star = 1 + log_2((log_2 3 - 1)/log_2 3)

The thermo_probe.py reports s* ≈ -0.43803. Let's check.
"""
import math
log2 = math.log(2)
log3 = math.log(3)
log2_3 = log3/log2

# Drift-balancing Esscher s*
s_star = 1 + math.log((log2_3 - 1)/log2_3) / log2
print(f"log_2(3) = {log2_3:.6f}")
print(f"s_star (drift-balancing) = {s_star:.6f}")
r_star = 2**(s_star - 1)
print(f"r_star = 2^(s*-1) = {r_star:.6f}")
print(f"  Geom(1-r*) param 1-r* = {1-r_star:.6f}")
print(f"  E_s*[a] = 1/(1-r*) = {1/(1-r_star):.6f}   (target log_2 3 = {log2_3:.6f})")
print(f"  E_s*[phi] = log3 - E[a]*log2 = {log3 - (1/(1-r_star))*log2:.2e}   (should be ~0)")

# Mod-3 marginal of R_n where R_n mod 3 = 2^(-a_n) mod 3.
# 2^(-a) mod 3: 2 ≡ -1 (mod 3), so 2^(-a) ≡ (-1)^(-a) ≡ (-1)^a (mod 3).
# a even: 2^(-a) ≡ 1 (mod 3)
# a odd:  2^(-a) ≡ -1 ≡ 2 (mod 3)
# So R_n mod 3 ∈ {1, 2} depending on parity of a_n (never 0 on units).
#
# Under Geom(1-r), P(a odd) = sum_{k odd} (1-r) r^(k-1) = (1-r)/(1-r^2) = 1/(1+r)
#                  P(a even) = r/(1+r)
print()
print("=== mod-3 marginal at the DRIFT-BALANCING Esscher tilt ===")
p_odd = 1/(1+r_star)
p_even = r_star/(1+r_star)
# Mod-3 marginal on units (0 has mass 0)
m1 = p_even   # R mod 3 = 1 corresponds to a even
m2 = p_odd    # R mod 3 = 2 corresponds to a odd
print(f"P(a even) = {p_even:.6f}  => P(R mod 3 = 1) = {m1:.6f}")
print(f"P(a odd)  = {p_odd:.6f}   => P(R mod 3 = 2) = {m2:.6f}")
print(f"Marginal on units: ({m1:.6f}, {m2:.6f})  (target uniform = (1/2, 1/2))")
# TV vs uniform on UNITS (excluding 0 coset which has mass 0)
TV_units = 0.5*(abs(m1-0.5)+abs(m2-0.5))
print(f"TV(marginal, Unif on units) = {TV_units:.6f}")
# TV vs uniform on Z/3 (3 cosets each with mass 1/3)
# But the actual law lives on units: (0, m1, m2) vs (1/3, 1/3, 1/3)
TV_uniform = 0.5*(1/3 + abs(m1 - 1/3) + abs(m2 - 1/3))
print(f"TV(marginal vs uniform-on-Z/3) = {TV_uniform:.6f}")

print()
print("=== Untilted (s=0): r=1/2, Geom(1/2) ===")
r0 = 0.5
p_even0 = r0/(1+r0)
p_odd0 = 1/(1+r0)
print(f"P(a even) = {p_even0:.6f}  P(a odd) = {p_odd0:.6f}")
m1_0 = p_even0; m2_0 = p_odd0
print(f"R mod 3 marginal: (0, {m1_0:.6f}, {m2_0:.6f}) = (0, 1/3, 2/3) -- the canonical obstruction")
TV0_units = 0.5*(abs(m1_0-0.5)+abs(m2_0-0.5))
TV0_uniform = 0.5*(1/3 + abs(m1_0 - 1/3) + abs(m2_0 - 1/3))
print(f"TV vs uniform-on-units = {TV0_units:.6f}")
print(f"TV vs uniform-on-Z/3   = {TV0_uniform:.6f}   (= 1/3 expected)")
