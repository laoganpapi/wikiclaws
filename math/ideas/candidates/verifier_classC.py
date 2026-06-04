"""
Independent verification of Class (C) Esscher tilt claims for the Collatz cocycle.

Author: Alex Ye

This is an INDEPENDENT REPLICATION. We re-derive from first principles and do
not import the multi-tilt agent's code.

Setup
-----
Base measure: a ~ Geom(1/2) on {1, 2, 3, ...}, so P_0(a = k) = 2^{-k}.
  (Mean E_0[a] = 2.)

Cocycle:          phi(a) = log 3 - a * log 2          (drift cocycle)
Auxiliary:        psi(a) = 1 if a is even else 0       (parity indicator)

Two-parameter Esscher tilt of P_0 by exp(s*phi(a) + t*psi(a)):
    P_{s,t}(a = k)  ∝  2^{-k} * exp(s * (log3 - k*log2) + t * [k even])
                    =  3^s * 2^{-k(1+s)} * exp(t * [k even])

Let r = 2^{-(1+s)}.  Convergence requires r < 1, i.e. s > -1.

Pressure:
  Z(s, t) = 3^s * [ r/(1-r^2) + e^t * r^2/(1-r^2) ]
         = 3^s * r * (1 + e^t r) / (1 - r^2)

  log Z = s log 3 - (1+s) log 2 + log(1 + e^t r) - log(1 - r^2)

Derivatives:
  dr/ds = - (log 2) * r.

  E[phi] = ∂(log Z)/∂s
         = log 3 - log 2  -  (e^t * (log2) r) / (1 + e^t r)
                          -  (- 2 r * (-log2 r)) / (1 - r^2)
         = log 3 - log 2  -  log2 * e^t r / (1 + e^t r)
                          -  2 (log2) r^2 / (1 - r^2)

Wait check the last sign carefully:
   - log(1 - r^2);  d/ds [-log(1-r^2)] = -(-2r * dr/ds)/(1 - r^2)
                                       = -(-2r * (-log2 r))/(1 - r^2)
                                       = -(2 log2 r^2)/(1 - r^2)
                                       = -2 (log2) r^2 / (1 - r^2).
So
  E[phi] = log 3 - log 2 * [ 1 + e^t r/(1 + e^t r) + 2 r^2/(1 - r^2) ]

  E[psi] = ∂(log Z)/∂t = e^t r / (1 + e^t r).

Equations (Class C):
  (E1) E[phi] = 0
  (E2) E[psi] = 1/2  =>  e^t r = 1   =>   t = -log r = (1+s) log 2.

Plugging E2 into E1:
  log 3 = log 2 * [ 1 + 1/2 + 2 r^2 / (1 - r^2) ]
  log 3 / log 2 = 3/2 + 2 r^2 / (1 - r^2)
  log 3 / log 2 - 3/2 = 2 r^2 / (1 - r^2)

Let A := log 3 / log 2 - 3/2 = log_2(3) - 3/2 = log_2(3 / 2^{3/2}) = log_2(3 / (2√2)).
Numerically A ≈ 0.08496250.

  2 r^2 = A (1 - r^2)  =>  r^2 (2 + A) = A  =>  r^2 = A / (2 + A).

Equivalent closed form:
  A = (log 3 - (3/2) log 2)/log 2 = log(9/8) / (2 log 2),
  2 + A = (4 log 2 + log 3 - (3/2) log 2)/log 2 = ((5/2) log 2 + log 3)/log 2
        = log(2^{5/2} * 3)/log 2 = log(√32 * 3)/log 2... let me reconfirm:
    A = log_2(3) - 3/2 = log_2(3) - log_2(2^{3/2}) = log_2(3/(2√2))
    2 + A = log_2(4) + log_2(3/(2√2)) = log_2(12/(2√2)) = log_2(6/√2) = log_2(6) - 1/2
          = log_2(6/√2) = log_2(3√2).
  So r^2 = log_2(3/(2√2)) / log_2(3√2) = log(3/(2√2)) / log(3√2)
         = log(9/8) / log(18)         [multiply num & denom by 2]

  r^2 = log(9/8) / log(18).

Numerically r^2 ≈ 0.04075013, r ≈ 0.20186662.

  s_C = -log(r)/log 2 - 1.
  t_C = -log(r) = (1+s_C) log 2.

Numerical values follow.  Sign convention here: positive s tilts toward smaller a
(geometric thinned). Different sign conventions in the literature simply flip
the sign of s; the drift-balance equation is the same.

LDP rate:
  I(0, 1/2) = sup_{s,t} [ s * 0 + t * (1/2) - log Z(s, t) ]
            = t_C / 2 - log Z(s_C, t_C).

mod-3:  2 ≡ -1 mod 3, so 2^{-a} ≡ (-1)^a (mod 3). R = 1 if a even, 2 if a odd.
mod-9:  ord_9(2) = 6.  2^{-a} ≡ 5^a (mod 9), cycling through {5,7,8,4,2,1} for
        a = 1..6.  Tabulate residue by a mod 6.
"""

from fractions import Fraction
import mpmath as mp
import json

mp.mp.dps = 60

log2 = mp.log(2)
log3 = mp.log(3)
log6 = mp.log(6)
log32 = mp.log(mp.mpf(3) / 2)

results = {}

# ---------- Validation gate 1: untilted (s=0, t=0) ----------
P_even_untilted = Fraction(1, 3)
P_odd_untilted = Fraction(2, 3)
TV_untilted = (abs(P_even_untilted - Fraction(1,2)) + abs(P_odd_untilted - Fraction(1,2))) / 2
assert TV_untilted == Fraction(1, 6)
print("Validation gate 1 (untilted s=0,t=0): mod-3 = (1/3, 2/3), TV = 1/6. PASS.")
results["gate1_untilted_TV"] = "1/6 (exact rational)"

# ---------- Claim 1: single-parameter Esscher (t=0) drift-balancing ----------
# E[phi]=0 with t=0:
#  log3 = log2 * [1 + 2 r^2/(1-r^2)]   (set 1/2 term to zero by removing E2-derived simplification)
# Actually with t=0 the simpler form: P_s(a=k) is geometric (1-r) r^{k-1}.
# Mean = 1/(1-r); E[phi] = log3 - log2/(1-r) = 0 => 1-r = log2/log3 => r = 1 - log2/log3.
r_single = 1 - log2/log3
s_single = -mp.log(r_single)/log2 - 1
Ea_single = 1/(1 - r_single)
Ephi_single = log3 - Ea_single * log2
P_even_single = r_single / (1 + r_single)
P_odd_single = 1 / (1 + r_single)
TV_single = (abs(P_even_single - mp.mpf(1)/2) + abs(P_odd_single - mp.mpf(1)/2)) / 2

print(f"\n--- Single-parameter (t=0) drift-balancing tilt ---")
print(f"  r* = 1 - log2/log3 = {mp.nstr(r_single, 25)}")
print(f"  s* = {mp.nstr(s_single, 25)}")
print(f"  E[a]  = 1/(1-r) = log3/log2 = {mp.nstr(Ea_single, 25)}  (=log_2 3 ≈ 1.585)")
print(f"  E[phi] = {mp.nstr(Ephi_single, 6)}   (must be 0)")
print(f"  P(a even) = r/(1+r) = {mp.nstr(P_even_single, 25)}")
print(f"  P(a odd)  = 1/(1+r) = {mp.nstr(P_odd_single, 25)}")
print(f"  mod-3 marginal: P(R=1)={mp.nstr(P_even_single, 6)}, P(R=2)={mp.nstr(P_odd_single, 6)}")
print(f"  TV vs uniform-on-units = {mp.nstr(TV_single, 12)}  (untilted = 1/6 ≈ 0.16667)")
print(f"  -> single-param drift-balancing tilt INCREASES the mod-3 TV.")

results["single_param"] = {
    "r": mp.nstr(r_single, 20),
    "s": mp.nstr(s_single, 20),
    "E_phi": mp.nstr(Ephi_single, 6),
    "P_a_even": mp.nstr(P_even_single, 20),
    "P_a_odd": mp.nstr(P_odd_single, 20),
    "TV_mod3": mp.nstr(TV_single, 20),
}

# ---------- Locate the tilt that yields (0.404, 0.596) marginal ----------
# (Trying both assignments since the question is sign-convention sensitive.)
print(f"\n--- Diagnostic: which tilt gives marginal (0.404, 0.596)? ---")
# Case A: P(R=1) = 0.404, P(R=2) = 0.596  => P(a even) = 0.404 => r/(1+r)=0.404 => r=0.404/0.596.
rA = mp.mpf("0.404")/mp.mpf("0.596")
sA = -mp.log(rA)/log2 - 1
EaA = 1/(1-rA)
EphiA = log3 - EaA*log2
print(f"  Case A: r={mp.nstr(rA,6)}, s={mp.nstr(sA,6)}, E[a]={mp.nstr(EaA,6)}, E[phi]={mp.nstr(EphiA,6)}")
# Case B: P(R=1) = 0.596, P(R=2) = 0.404 (mass moved AWAY from 2 toward 1, i.e. toward even a)
# P(a even)=0.596 => r=0.596/0.404 > 1.  Invalid (no such Esscher tilt).
rB_num = mp.mpf("0.596")/mp.mpf("0.404")
print(f"  Case B: would need r = {mp.nstr(rB_num,6)} > 1, INVALID; not in Esscher family.")

# The (0.404, 0.596) marginal therefore corresponds to Case A: a tilt with
#   s ≈ -0.43904 (negative, opposite sign of drift-balancing s* ≈ +0.43803).
# At this point E[phi] ≈ -1.053 ≠ 0; this is NOT drift-balancing.
# It's roughly the *reflection* of the drift-balancing tilt about s=0.
print(f"  => (0.404, 0.596) arises at s ≈ {mp.nstr(sA, 6)}, NOT drift-balancing.")
print(f"     (Roughly the sign-flipped s; explains the propagating error.)")
results["bad_404_596"] = {
    "s": mp.nstr(sA, 12),
    "E_phi": mp.nstr(EphiA, 12),
    "note": "Not drift-balancing; opposite sign from s*.",
}

# ---------- Claim 2: Class (C) two-parameter tilt ----------
# From derivation: r^2 = log(9/8) / log(18); t = -log r.
log_9_8 = mp.log(mp.mpf(9)/8)
log_18 = mp.log(18)
r2_star = log_9_8 / log_18
r_star = mp.sqrt(r2_star)
s_C = -mp.log(r_star)/log2 - 1
t_C = -mp.log(r_star)

print(f"\n--- Class (C) two-parameter tilt ---")
print(f"  r_C^2 = log(9/8)/log(18) = {mp.nstr(r2_star, 30)}")
print(f"  r_C   = {mp.nstr(r_star, 30)}")
print(f"  s_C   = {mp.nstr(s_C, 30)}")
print(f"  t_C   = {mp.nstr(t_C, 30)}")

# Closed form verification:
# E[phi] = log3 - log2*[1 + 1/2 + 2 r^2/(1-r^2)]; with r^2 = A/(2+A), A = log3/log2 - 3/2:
# 2 r^2/(1-r^2) = 2 (A/(2+A)) / (1 - A/(2+A)) = 2A/(2+A) * (2+A)/2 = A. So bracket = 1 + 1/2 + A.
# E[phi] = log3 - log2*(3/2 + A) = log3 - log2*(3/2 + log3/log2 - 3/2) = log3 - log3 = 0. EXACT.
print(f"  E[phi] (symbolic) = 0 (exact identity)")

# E[psi] check
e_t_r = mp.exp(t_C) * r_star  # should equal 1 exactly
print(f"  e^t * r = {mp.nstr(e_t_r, 30)}  (target 1)")
P_a_even_C = e_t_r / (1 + e_t_r)
print(f"  P(a even) = e^t r/(1+e^t r) = {mp.nstr(P_a_even_C, 30)} (target 1/2)")

# LDP rate
log_Z = s_C*log3 - (1+s_C)*log2 + mp.log(1 + e_t_r) - mp.log(1 - r_star**2)
# Simplify since 1+e^t r = 2:
log_Z_simpler = s_C*log3 + t_C - log2 - mp.log(1 - r_star**2) - s_C*log2 + log2
# Let's just use the direct expression; cross-check:
log_Z_alt = mp.log(mp.power(3, s_C) * r_star * (1 + e_t_r) / (1 - r_star**2))
print(f"  log Z direct = {mp.nstr(log_Z, 30)}")
print(f"  log Z alt    = {mp.nstr(log_Z_alt, 30)}")
I_rate = t_C * mp.mpf(1)/2 - log_Z
print(f"  I(0, 1/2) = t_C/2 - log Z = {mp.nstr(I_rate, 30)}")
print(f"  I to 12 dp = {mp.nstr(I_rate, 14)}")

results["classC"] = {
    "r_squared": mp.nstr(r2_star, 30),
    "r": mp.nstr(r_star, 30),
    "s_C": mp.nstr(s_C, 30),
    "t_C": mp.nstr(t_C, 30),
    "E_phi": "0 (exact identity)",
    "P_a_even": "1/2 (exact identity)",
    "log_Z": mp.nstr(log_Z, 30),
    "I_rate": mp.nstr(I_rate, 30),
}

# ---------- Numerical sanity via series + E[a] closed form ----------
def normalize_and_moments(s, t, K=600):
    r = mp.power(2, -(1+s))
    Z = mp.power(3, s) * r * (1 + mp.exp(t) * r) / (1 - r*r)
    Ephi = mp.mpf(0); Pa_even = mp.mpf(0); mod6 = [mp.mpf(0)]*6; total = mp.mpf(0)
    Ea = mp.mpf(0)
    for k in range(1, K+1):
        w = mp.power(3, s) * mp.power(r, k)
        if k % 2 == 0: w *= mp.exp(t)
        total += w
        Ea += w*k
        Ephi += w * (log3 - k*log2)
        if k % 2 == 0: Pa_even += w
        mod6[k % 6] += w
    Ephi /= total; Pa_even /= total; Ea /= total
    mod6 = [x/total for x in mod6]
    return Z, total, Ea, Ephi, Pa_even, mod6

Z_C_num, tot_C, Ea_C_num, Ephi_C_num, Peven_C_num, mod6_C = normalize_and_moments(s_C, t_C, K=600)
print(f"\nSeries-based sanity check at (s_C, t_C):")
print(f"  Z (closed)  = {mp.nstr(Z_C_num, 30)}")
print(f"  Sum series  = {mp.nstr(tot_C, 30)}")
print(f"  E[a]        = {mp.nstr(Ea_C_num, 25)}")
print(f"  log_2(3)    = {mp.nstr(log3/log2, 25)}")
print(f"  E[phi] num  = {mp.nstr(Ephi_C_num, 25)} (target 0)")
print(f"  P(a even) num = {mp.nstr(Peven_C_num, 25)} (target 1/2)")

# ---------- Validation gate 2: t = 0, single-param recovery ----------
Z0, tot0, Ea0, Ephi0, Peven0, mod6_0 = normalize_and_moments(s_single, 0, K=600)
print(f"\nValidation gate 2 (t=0, drift-balancing): E[phi]={mp.nstr(Ephi0,8)}, P(even)={mp.nstr(Peven0,20)} vs single-param formula {mp.nstr(P_even_single,20)}.")
assert abs(Peven0 - P_even_single) < mp.mpf(10)**(-15)

# ---------- mod-3 marginal under Class C ----------
PR1_C = mp.mpf(1)/2
PR2_C = mp.mpf(1)/2
TV3_C = mp.mpf(0)
print(f"\nmod-3 marginal under (s_C, t_C): (1/2, 1/2), TV = 0 (exact)")
results["mod3_TV"] = "0 (exact)"

# ---------- Claim 3: mod-9 marginal under Class (C) ----------
# Closed-form mod-6 probabilities. With e^t r = 1 the unnormalized weights:
#   odd k: r^k.   even k: r^{k-1} = r^{k-1}.
# By residue j = k mod 6 in {1,..,6}, then convert 6 to 0.
# Group sums (k = j, j+6, j+12, ...):
#   j=1 (odd): r + r^7 + r^13 + ... = r/(1-r^6)
#   j=2 (even): r + r^7 + r^13 + ... wait: r^{2-1}=r, r^{8-1}=r^7,...= r/(1-r^6)
#   j=3 (odd): r^3 + r^9 + ... = r^3/(1-r^6)
#   j=4 (even): r^3 + r^9 + ... = r^3/(1-r^6)
#   j=5 (odd): r^5 + r^11 + ... = r^5/(1-r^6)
#   j=6 (even): r^5 + r^11 + ... = r^5/(1-r^6)
# Total = 2(r + r^3 + r^5)/(1-r^6) = 2r(1+r^2+r^4)/(1-r^6) = 2r/(1-r^2).
denom = 2 * (1 + r_star**2 + r_star**4)
P_mod6_closed = {
    1: 1 / denom,
    2: 1 / denom,
    3: r_star**2 / denom,
    4: r_star**2 / denom,
    5: r_star**4 / denom,
    0: r_star**4 / denom,  # j = 6 ≡ 0 mod 6
}

# Residue map: a ≡ j (mod 6, j in {1..6}) -> 2^{-a} mod 9 = 5^a mod 9.
# Since ord_9(5) = ord_9(2) = 6, depends only on a mod 6.
# a=1: 5, a=2: 25 mod 9 = 7, a=3: 125 mod 9 = 8, a=4: 625 mod 9 = 4, a=5: 5*4=20 mod 9 = 2, a=6: 5*2=10 mod 9 = 1.
res_map = {1: 5, 2: 7, 3: 8, 4: 4, 5: 2, 0: 1}
units = [1, 2, 4, 5, 7, 8]
P_res = {u: mp.mpf(0) for u in units}
for j in range(6):
    P_res[res_map[j]] += P_mod6_closed[j]
TV9 = sum(abs(P_res[u] - mp.mpf(1)/6) for u in units) / 2

print(f"\n--- mod-9 marginal under (s_C, t_C) (closed-form) ---")
for u in units:
    print(f"  P(R={u} mod 9) = {mp.nstr(P_res[u], 25)}")
print(f"  sum = {mp.nstr(sum(P_res[u] for u in units), 25)} (target 1)")
print(f"  TV vs uniform on units mod 9 = {mp.nstr(TV9, 30)}")
print(f"  TV to 10 dp = {mp.nstr(TV9, 12)}")

results["classC_mod9"] = {u: mp.nstr(P_res[u], 25) for u in units}
results["classC_mod9_TV"] = mp.nstr(TV9, 25)

# ---------- Compare to multi-tilt agent's claims ----------
print("\n" + "="*70)
print("COMPARISON TO MULTI-TILT AGENT'S REPORTED CLAIMS")
print("="*70)
print(f"Multi-tilt agent reported: (s_C, t_C) ≈ (-1.309, -1.600)")
print(f"Verifier (re-derived):     (s_C, t_C) =  ({mp.nstr(s_C, 8)}, {mp.nstr(t_C, 8)})")
print(f"  -> DIFFERENT VALUES; likely a sign-convention difference in s,t.")
print(f"")
print(f"Multi-tilt agent reported: I ≈ 0.228")
print(f"Verifier (re-derived):     I = {mp.nstr(I_rate, 12)}")
print(f"  -> DIFFERENT VALUES.")
print(f"")
print(f"Multi-tilt agent reported: TV(tilted ν mod 9, uniform on (Z/9)*) ≈ 0.313")
print(f"Verifier (re-derived):     TV mod 9 = {mp.nstr(TV9, 12)}")
print(f"  -> DIFFERENT VALUES.")
print(f"")
print(f"Agreement on STRUCTURAL claims:")
print(f"  - E[phi] = 0 and P(a even) = 1/2 are saturated exactly: CONFIRMED.")
print(f"  - mod-3 marginal becomes uniform on units (TV=0): CONFIRMED (exact).")
print(f"  - Iteration to mod-9 fails (TV > 0 substantially): CONFIRMED.")

# Save JSON data
with open('/home/user/wikiclaws/math/ideas/candidates/data/verifier_classC_results.json', 'w') as fp:
    json.dump(results, fp, indent=2)
print("\nResults JSON saved.")
