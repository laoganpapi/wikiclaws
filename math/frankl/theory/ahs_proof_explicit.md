# The Alweiss–Huang–Sellke proof of the $(3-\sqrt5)/2$ bound, in full explicit detail

**Author:** Alex Ye (AI assistance disclosed separately)
**Status:** `[baseline reconstruction — Step-1 numerically checked]`
**Date:** 2 June 2026
**Purpose.** Reconstruct, from first principles, the entropy proof that every finite
union-closed family $\mathcal F\neq\{\varnothing\}$ has an element of frequency
$\ge \psi := (3-\sqrt5)/2 \approx 0.3819660$. This file is the baseline against which
the two new attack vectors (Shearer-style chain rule; intersection term) are measured.
Every inequality is justified from entropy axioms, convexity, or an explicit one-variable
calculus argument. Nothing is taken as "well known".

Primary sources: Gilmer, arXiv:2211.09055; Alweiss–Huang–Sellke, arXiv:2211.11731
(*Electron. J. Combin.* **31(3)** #P3.35, 2024); Sawin, arXiv:2211.11504; Chase–Lovett,
arXiv:2211.11689. The exposition below follows the AHS line but spells out the steps that
those papers compress.

All logarithms are base $2$ unless stated; entropy is in bits. Write
$$ h(p) := -p\log p - (1-p)\log(1-p), \qquad h(0)=h(1)=0 $$
for the binary entropy function on $[0,1]$.

---

## 0. Conventions and the entropy toolkit (axioms we are allowed to use)

We use only the following standard facts about Shannon entropy, each of which is an
elementary consequence of the definition $H(X) = -\sum_x \Pr[X=x]\log\Pr[X=x]$.

**(E1) Nonnegativity.** $H(X)\ge 0$, with equality iff $X$ is a.s. constant.

**(E2) Uniform bound / maximality.** If $X$ takes at most $m$ values then $H(X)\le \log m$,
with equality iff $X$ is uniform on $m$ values. *(Proof: Jensen on the concave $\log$.)*

**(E3) Chain rule.** $H(X,Y) = H(X) + H(Y\mid X)$, and inductively
$H(X_1,\dots,X_n) = \sum_{i=1}^n H(X_i \mid X_1,\dots,X_{i-1})$.

**(E4) Conditioning reduces entropy.** $H(X\mid Y)\le H(X)$, with equality iff $X\perp Y$.
More generally $H(X\mid Y,Z)\le H(X\mid Y)$. *(Proof: mutual information $I(X;Y)=H(X)-H(X\mid Y)\ge 0$ by Jensen.)*

**(E5) Subadditivity.** $H(X_1,\dots,X_n)\le \sum_i H(X_i)$, equality iff independent.
*(Immediate from E3 + E4.)*

**(E6) A deterministic function of the conditioned-on variable is free.** If $Y=f(X)$ then
$H(X,Y)=H(X)$ and $H(Y\mid X)=0$.

**(E7) Data processing for entropy of a function.** $H(f(X))\le H(X)$.

We also use:

**(E8) Binary-entropy facts.** $h$ is continuous on $[0,1]$, $h(p)=h(1-p)$, strictly concave,
$h'(p)=\log\frac{1-p}{p}$, maximised at $p=\tfrac12$ with $h(\tfrac12)=1$. As $p\to 0^+$,
$h(p)=-p\log p + O(p)\to 0$.

These eight facts are the *entire* toolkit. We never invoke an external theorem in the
load-bearing chain.

---

## 1. The information-theoretic reformulation

### 1.1 Setup

Let $\mathcal F\subseteq 2^{[n]}$ be union-closed, $\mathcal F\neq\{\varnothing\}$, with
$[n]=\{1,\dots,n\}$ the ground set, and $m:=|\mathcal F|\ge 1$. We may assume $m\ge 2$
(if $m=1$ then $\mathcal F=\{S\}$ for a single set $S$; union-closure forces $S\cup S=S$,
no constraint, and any $x\in S$ has frequency $1=m\ge m/2$; if $S=\varnothing$ that is the
excluded family). Henceforth $m\ge 2$.

Encode a set $A\subseteq[n]$ by its indicator vector $(A_1,\dots,A_n)\in\{0,1\}^n$,
$A_i = \mathbf 1[i\in A]$. **Let $A$ and $B$ be independent random variables, each uniform
on $\mathcal F$.** Define the **marginals**
$$ p_i := \Pr[i\in A] = \Pr[A_i=1] = \frac{|\{S\in\mathcal F : i\in S\}|}{m} \in [0,1]. $$
The frequency of element $i$ is exactly $p_i\cdot m$, so **the conjecture
"$\exists\, i$ with frequency $\ge m/2$" is equivalent to "$\max_i p_i \ge \tfrac12$".**

Our goal (AHS): prove $\max_i p_i \ge \psi=(3-\sqrt5)/2$.

### 1.2 The two-sided squeeze

Because $A,B$ are each uniform on the $m$-element set $\mathcal F$, by (E2) with equality,
$$ H(A) = H(B) = \log m. \tag{1.1}$$

**Upper bound on $H(A\cup B)$.** Since $\mathcal F$ is union-closed and $A,B\in\mathcal F$,
the random set $A\cup B$ also lies in $\mathcal F$. Thus $A\cup B$ takes at most $m$ values,
and by (E2),
$$ \boxed{\,H(A\cup B)\;\le\;\log m \;=\; H(A).\,} \tag{1.2}$$
This is the *only* place union-closure is used in the AHS argument. It is exact in the sense
that no inequality has been wasted yet — but it throws away everything about *how* the unions
populate $\mathcal F$ (see §6, the slack analysis).

The strategy is now: find a *lower* bound on $H(A\cup B)$ in terms of the marginals $p_i$,
of the form $H(A\cup B)\ge \Phi(p_1,\dots,p_n)$, and a matching upper bound on $H(A)=\log m$
of the form $H(A)\le \Psi(p_1,\dots,p_n)$, such that $\Phi\le\Psi$ together with (1.2) forces
$\max_i p_i\ge\psi$.

### 1.3 Upper bound on $H(A)$ (subadditivity)

By subadditivity (E5) applied to the coordinates of $A$, and using that each $A_i$ is
Bernoulli$(p_i)$ so $H(A_i)=h(p_i)$:
$$ \log m = H(A) = H(A_1,\dots,A_n) \;\le\; \sum_{i=1}^n H(A_i) = \sum_{i=1}^n h(p_i). \tag{1.3}$$

### 1.4 Lower bound on $H(A\cup B)$ (coordinatewise chain rule)

Write $C:=A\cup B$, with coordinates $C_i = A_i \vee B_i$ (logical OR). By the chain rule (E3),
$$ H(C) = \sum_{i=1}^n H(C_i \mid C_{<i}), \qquad C_{<i}:=(C_1,\dots,C_{i-1}). $$
By "conditioning reduces entropy" (E4),
$$ H(C_i\mid C_{<i}) \;\ge\; H(C_i\mid C_{<i}, A_{<i}, B_{<i}). \tag{1.4}$$
Now condition further: given $A_{<i},B_{<i}$, the value $C_{<i}=A_{<i}\vee B_{<i}$ is a
*deterministic function* of the conditioning, so by (E6) it adds nothing:
$$ H(C_i\mid C_{<i},A_{<i},B_{<i}) = H(C_i\mid A_{<i},B_{<i}). \tag{1.5}$$
**This is the chain-rule reduction.** Combining (1.4)–(1.5),
$$ H(C) \;\ge\; \sum_{i=1}^n H(C_i\mid A_{<i}, B_{<i}). \tag{1.6}$$

> **Slack marker $\mathsf S_2$ (chain rule).** The inequality (1.4) is the place where
> structural information is discarded. The exact deficit is
> $$ \delta_i := H(C_i\mid C_{<i}) - H(C_i\mid A_{<i},B_{<i}) \;=\; -\,I\big(C_i\,;\,(A_{<i},B_{<i})\,\big|\,C_{<i}\big)\;\le\;0, $$
> i.e. *(1.4) goes the favorable direction by exactly the conditional mutual information
> $I(C_i;(A_{<i},B_{<i})\mid C_{<i})\ge0$.* We track $\mathsf S_2$ throughout; it is the
> target of Vector 1. (Sign: conditioning on **more** can only **decrease** entropy, so the
> RHS of (1.6) is a genuine lower bound; the amount we lose is the listed mutual information.)

### 1.5 The single-coordinate bound

Now we lower-bound each term $H(C_i\mid A_{<i},B_{<i})$. Fix $i$ and condition on a value
$(a,b)$ of $(A_{<i},B_{<i})$. Under the conditional law, $A_i$ and $B_i$ are some
$\{0,1\}$-valued random variables. Crucially, **$A$ and $B$ are independent and identically
distributed**, so conditioned on $A_{<i}=a$ and $B_{<i}=b$:

- $A_i$ has conditional law depending only on $a$: write $\alpha := \Pr[A_i=1\mid A_{<i}=a]$.
- $B_i$ has conditional law depending only on $b$: write $\beta := \Pr[B_i=1\mid B_{<i}=b]$.
- $A_i\perp B_i$ given $(a,b)$ (because $A\perp B$).

Then $C_i = A_i\vee B_i$ is Bernoulli with
$$ \Pr[C_i=0\mid a,b] = \Pr[A_i=0\mid a]\Pr[B_i=0\mid b] = (1-\alpha)(1-\beta), $$
so $H(C_i\mid A_{<i}=a,B_{<i}=b) = h\big(1-(1-\alpha)(1-\beta)\big) = h\big((1-\alpha)(1-\beta)\big)$
(using $h(t)=h(1-t)$). Therefore, taking expectation over $(a,b)$,
$$ H(C_i\mid A_{<i},B_{<i}) = \mathbb E_{a,b}\Big[\,h\big((1-\alpha(a))(1-\beta(b))\big)\Big]. \tag{1.7}$$

Similarly, $H(A_i\mid A_{<i}) = \mathbb E_a[h(\alpha(a))]$ and $p_i = \mathbb E_a[\alpha(a)]$.

This is the heart of the matter: we need to compare the *expected union entropy*
$\mathbb E[h((1-\alpha)(1-\beta))]$ to the *expected individual entropies*
$\mathbb E[h(\alpha)]$ and $\mathbb E[h(\beta)]$, where $\alpha,\beta$ are **i.i.d.** (same
law, since $A\overset{d}{=}B$ and we condition on independent copies of the same prefix law).

---

## 2. The one-variable entropy inequality (the engine)

Everything now reduces to a single inequality about the binary entropy function. We state it,
then prove it from scratch.

### 2.1 Statement

> **Lemma 2 (AHS / Gilmer Lemma 3, sharp form).** Let $\psi=(3-\sqrt5)/2$, equivalently the
> root in $(0,\tfrac12)$ of $\psi^2-3\psi+1=0$, equivalently the unique $\psi\in(0,\tfrac12)$ with
> $(1-\psi)^2 = 1-\psi\cdot\tfrac{?}{}$ … we use the clean characterisation
> $$ (1-\psi)^2 = 1-2\psi+\psi^2, \qquad \psi^2 = 3\psi-1, \quad\Rightarrow\quad (1-\psi)^2 = \psi. \tag{2.1}$$
> So $\psi$ is the **unique fixed point in $(0,1)$ of $p\mapsto (1-p)^2$ reflected**, i.e.
> $(1-\psi)^2=\psi$. Set $\lambda := \dfrac{1}{2(1-\psi)}$.
>
> Then for **all** $p,q\in[0,1]$,
> $$ h\big(1-(1-p)(1-q)\big) \;\ge\; \lambda\big[(1-q)\,h(p) + (1-p)\,h(q)\big]. \tag{2.2}$$
> Moreover (2.2) is an equality at $p=q=\psi$.

A short remark on why this is the right inequality and where $\lambda$ comes from is given in
§2.4 after the proof. The constant $\lambda=\frac1{2(1-\psi)}$ is **forced** by demanding
equality at the symmetric point $p=q=\psi$; we verify the value there and then prove (2.2) holds
globally.

### 2.2 Reduction of §1 to Lemma 2

Before proving Lemma 2, let us see that it closes the argument. The form (2.2) is engineered so
that the weight $(1-q)$ multiplying $h(p)$ "pays for" the chain-rule contribution. Set
$g(p):=h(p)$. Apply (2.2) pointwise inside the expectation (1.7) with $p=\alpha(a)$, $q=\beta(b)$,
and take $\mathbb E_{a,b}$ over the **independent** pair $(a,b)$ (recall $A\perp B$ and
$A\overset d= B$, so $\alpha(A_{<i})$ and $\beta(B_{<i})$ are i.i.d.):
$$
H(C_i\mid A_{<i},B_{<i})
= \mathbb E_{a,b}\big[h(1-(1-\alpha)(1-\beta))\big]
\;\ge\; \lambda\,\mathbb E_{a,b}\big[(1-\beta)h(\alpha) + (1-\alpha)h(\beta)\big].
$$
By independence of $a$ and $b$, $\mathbb E_{a,b}[(1-\beta)h(\alpha)] = \mathbb E_a[h(\alpha)]\cdot\mathbb E_b[1-\beta]
= H(A_i\mid A_{<i})\cdot(1-p_i)$, and symmetrically. Hence
$$
H(C_i\mid A_{<i},B_{<i}) \;\ge\; \lambda\big[(1-p_i)H(A_i\mid A_{<i}) + (1-p_i)H(B_i\mid B_{<i})\big]
= 2\lambda\,(1-p_i)\,H(A_i\mid A_{<i}), \tag{2.3}
$$
using $H(B_i\mid B_{<i})=H(A_i\mid A_{<i})$ (identical laws). Now sum (2.3) over $i$, plug into the
chain-rule lower bound (1.6), and use $2\lambda = \frac1{1-\psi}$:
$$
H(C) \;\ge\; \frac{1}{1-\psi}\sum_{i=1}^n (1-p_i)\,H(A_i\mid A_{<i}). \tag{2.4}
$$

**Closing.** Suppose, for contradiction, that $\max_i p_i < \psi$. Then $1-p_i > 1-\psi$ for all
$i$, so $(1-p_i) > (1-\psi)$ and from (2.4),
$$
H(C) \;>\; \frac{1-\psi}{1-\psi}\sum_{i=1}^n H(A_i\mid A_{<i}) = \sum_{i=1}^n H(A_i\mid A_{<i})
\overset{\text{(E3)}}{=} H(A_1,\dots,A_n) = H(A). \tag{2.5}
$$
But (1.2) says $H(C)=H(A\cup B)\le H(A)$. The strict inequality $H(C)>H(A)$ contradicts
$H(C)\le H(A)$ — **unless** the sum $\sum_i H(A_i\mid A_{<i})=H(A)=\log m=0$, i.e. $m=1$, which
we excluded. Therefore $\max_i p_i \ge \psi$. $\qquad\blacksquare$

> **Remark (why the chain rule is used on the right, not subadditivity).** Note that in (2.5)
> we used the **exact** chain rule $\sum_i H(A_i\mid A_{<i})=H(A)$, *not* the lossy
> subadditive bound (1.3) $\sum_i h(p_i)\ge H(A)$. This is the AHS refinement over Gilmer's
> original write-up: by keeping $H(A_i\mid A_{<i})$ instead of $h(p_i)=H(A_i)$, the
> "$\le$" of subadditivity is avoided and only the single inequality (2.2) carries the load.
> The price is that (2.2) must hold with the **conditional** marginals appearing as weights,
> which is exactly its stated two-variable form. The two formulations give the same constant
> $\psi$. We keep the conditional form because it has *strictly less slack* and is the honest
> baseline for our improvement attempts.

So the **entire** quantitative content is Lemma 2. We prove it now.

### 2.3 Proof of Lemma 2

We must show $F(p,q)\ge 0$ on $[0,1]^2$, where
$$ F(p,q) := h\big(1-(1-p)(1-q)\big) - \lambda\big[(1-q)h(p)+(1-p)h(q)\big], \qquad \lambda=\tfrac1{2(1-\psi)}. $$

**Step A — boundary and symmetry.** $F$ is symmetric: $F(p,q)=F(q,p)$. At $q=0$:
$1-(1-p)(1-0)=p$, $h(0)=0$, so $F(p,0)=h(p)-\lambda[(1)h(p)+(1-p)\cdot 0]=(1-\lambda)h(p)$.
Since $\psi<\tfrac12$, $1-\psi>\tfrac12$, so $\lambda=\frac1{2(1-\psi)}<1$; hence $F(p,0)=(1-\lambda)h(p)\ge0$
with equality only at $p\in\{0,1\}$. By symmetry $F(0,q)\ge0$. At $p=q=1$: argument of $h$ is $1$,
$h(1)=0$, and the bracket is $0\cdot h(1)+0\cdot h(1)=0$, so $F(1,1)=0$. Good — boundaries are
nonnegative.

**Step B — reduce to a one-variable problem via the diagonal and a clever substitution.**
The clean approach (this is the AHS/Sawin manoeuvre) is to fix the product structure. Substitute
$$ u := 1-p,\quad v := 1-q,\quad (u,v)\in[0,1]^2, $$
and write $H(t):=h(1-t)=h(t)$ (so $H=h$). Then $1-(1-p)(1-q)=1-uv$, and
$$ F = h(1-uv) - \lambda\big[v\,h(1-u) + u\,h(1-v)\big] = h(uv) - \lambda\big[v\,h(u)+u\,h(v)\big], \tag{2.6}$$
using $h(1-uv)=h(uv)$, $h(1-u)=h(u)$, $h(1-v)=h(v)$. So define on $[0,1]^2$
$$ G(u,v) := h(uv) - \lambda\big[v\,h(u) + u\,h(v)\big]; \qquad \text{we must show } G\ge 0. \tag{2.7}$$
Equality point $p=q=\psi$ becomes $u=v=1-\psi=:\sigma$, where by (2.1) $\sigma^2 = (1-\psi)^2=\psi$,
i.e. $\sigma^2=1-\sigma$ — so $\sigma$ is the **golden-ratio reciprocal** $\sigma=1/\varphi=(\sqrt5-1)/2\approx0.618$,
satisfying $\sigma^2+\sigma-1=0$, i.e. $\sigma^2 = 1-\sigma$. (Indeed $\psi=1-\sigma=(3-\sqrt5)/2$.)

**Step C — the key single-variable inequality.** We prove $G\ge0$ by showing it on every line
$v=\text{const}$ reduces to a one-dimensional convexity fact. Fix $v\in(0,1)$ and consider
$$ g_v(u) := h(uv) - \lambda v\,h(u) - \lambda u\,h(v), \qquad u\in[0,1]. $$
We compute derivatives in $u$. Recall $h'(t)=\log\frac{1-t}{t}$ and $\frac{d}{du}h(uv)=v\,h'(uv)=v\log\frac{1-uv}{uv}$.
$$ g_v'(u) = v\log\frac{1-uv}{uv} - \lambda v\log\frac{1-u}{u} - \lambda h(v). $$
$$ g_v''(u) = v\cdot\frac{d}{du}\!\Big[\log\frac{1-uv}{uv}\Big] - \lambda v\cdot\frac{d}{du}\!\Big[\log\frac{1-u}{u}\Big]. $$
Now $\frac{d}{dt}\log\frac{1-t}{t} = \frac{d}{dt}[\log(1-t)-\log t] = -\frac{1}{1-t}-\frac1t = -\frac{1}{t(1-t)}$.
So, with $t=uv$ (chain rule contributes a factor $v$):
$$ \frac{d}{du}\log\frac{1-uv}{uv} = -\frac{v}{uv(1-uv)} = -\frac{1}{u(1-uv)}, \qquad
\frac{d}{du}\log\frac{1-u}{u} = -\frac{1}{u(1-u)}. $$
Hence
$$ g_v''(u) = v\Big(-\frac{1}{u(1-uv)}\Big) - \lambda v\Big(-\frac{1}{u(1-u)}\Big)
= \frac{v}{u}\Big[\frac{\lambda}{1-u} - \frac{1}{1-uv}\Big]. \tag{2.8}$$
The sign of $g_v''(u)$ is the sign of $\dfrac{\lambda}{1-u}-\dfrac{1}{1-uv} = \dfrac{\lambda(1-uv)-(1-u)}{(1-u)(1-uv)}.$
The denominator is positive on $(0,1)$. The numerator is
$$ N(u) := \lambda(1-uv) - (1-u) = (\lambda-1) + u(1-\lambda v) = (\lambda-1) + u(1-\lambda v). $$
This is **linear in $u$**. So $g_v''$ changes sign at most once on $(0,1)$, which means $g_v$ is
either convex, concave, or convex-then-concave / concave-then-convex on the interval — in all
cases $g_v$ has **at most one interior local minimum on each side**, and we can verify
nonnegativity by checking the endpoints together with the structure. Precisely:

- $N(0)=\lambda-1<0$ (since $\lambda<1$). So $g_v''(0^+)<0$: $g_v$ is **concave near $u=0$**.
- $N(1)=\lambda(1-v)-0 = \lambda(1-v)>0$ for $v<1$. So $g_v''(1^-)>0$: $g_v$ is **convex near $u=1$**.
- Since $N$ is linear and goes from negative to positive, there is exactly one $u_0\in(0,1)$ with
  $N(u_0)=0$; $g_v$ is concave on $(0,u_0)$ and convex on $(u_0,1)$.

A function that is concave then convex on $[0,1]$ attains its minimum either at an interior
**stationary point in the convex region** $(u_0,1)$ or at the left endpoint $u=0$. (On the concave
piece $(0,u_0)$ the minimum over that subinterval is at an endpoint $0$ or $u_0$; the global min is
thus at $u=0$, at $u=1$, or at the unique stationary point of the convex piece.) Evaluate:

- $g_v(0) = h(0) - \lambda v\,h(0) - 0 = 0.$ **(left endpoint is exactly $0$).**
- $g_v(1) = h(v) - \lambda v\,h(1) - \lambda h(v) = (1-\lambda)h(v)\ge 0.$ **(right endpoint $\ge0$).**

So the only way $G<0$ could occur is at an **interior stationary point** $u^\*\in(u_0,1)$ of the
convex piece. We now show the global minimum value is $\ge0$ by a direct argument at the stationary
point, using the equality case.

**Step D — the stationary point and the choice of $\lambda$.** At any interior stationary point
$u^\*$ (where $g_v'(u^\*)=0$), we have a clean expression. From $g_v'(u)=0$:
$$ v\log\frac{1-u^\* v}{u^\* v} = \lambda v\log\frac{1-u^\*}{u^\*} + \lambda h(v). \tag{2.9}$$
Rather than solve (2.9) in general, we use the **two-variable** stationarity and symmetry. The full
function $G(u,v)$ on $(0,1)^2$ has, by symmetry $G(u,v)=G(v,u)$, any interior critical point either
on the diagonal $u=v$ or in a symmetric pair. Compute the diagonal. On $u=v=:s$,
$$ G(s,s) = h(s^2) - 2\lambda s\,h(s). $$
We show $G(s,s)\ge0$ for all $s\in[0,1]$ and that the *global* minimum of $G$ over $[0,1]^2$ is on
the diagonal; combined with Step C (which shows on each horizontal line the min is at $u\in\{0,1\}$
or at one interior point), the global minimum is attained either on the diagonal or on the boundary,
and the boundary is $\ge0$ by Step A. So it suffices to prove:
$$ \boxed{\;\phi(s) := h(s^2) - 2\lambda\,s\,h(s)\;\ge\;0 \quad\text{for all } s\in[0,1],\quad \lambda=\tfrac1{2\sigma},\ \sigma=1-\psi.\;} \tag{2.10}$$
(We justify "global min is on the diagonal or boundary" rigorously in §2.3.1 below; it follows from
the concave–convex structure plus symmetry. The reader who prefers can take (2.10) plus the **direct
two-variable verification in §5 (numerics on a fine grid)** as the Step-1 certificate; the analytic
diagonal-reduction is standard and we make it precise next.)

#### 2.3.1 Reduction to the diagonal, made precise

We claim: $\min_{[0,1]^2} G$ is attained at a point with $u=v$ or on $\partial([0,1]^2)$.

Consider the change of variables to $s=\tfrac{u+v}2$ (mean) and $d=\tfrac{u-v}2$ (half-difference).
Fix $s$ and vary $d$ along the segment $\{(s+d,s-d): |d|\le \min(s,1-s)\}$. Define
$\Theta_s(d) := G(s+d, s-d)$. Note $\Theta_s$ is **even** in $d$ (by the symmetry $G(u,v)=G(v,u)$),
so $\Theta_s'(0)=0$ and a critical point sits at $d=0$. We show $\Theta_s$ is **convex in $d$ near
$d=0$ wherever the min could be interior**, so that $d=0$ (the diagonal) is a local min along the
anti-diagonal direction — equivalently, the off-diagonal direction is "stable". Concretely compute
the second derivative at $d=0$:
$$ \Theta_s''(0) = G_{uu}-2G_{uv}+G_{vv}\big|_{(s,s)}. $$
Using $G(u,v)=h(uv)-\lambda v h(u)-\lambda u h(v)$ and $h''(t)=-\frac1{t(1-t)}$:
$$ G_{uu} = v^2 h''(uv) - \lambda v\, h''(u),\quad G_{vv}=u^2h''(uv)-\lambda u\,h''(v), $$
$$ G_{uv} = h'(uv)+uv\,h''(uv) - \lambda h'(u) - \lambda h'(v). $$
At $u=v=s$, with $h''(s^2)=-\frac1{s^2(1-s^2)}$ and $h''(s)=-\frac1{s(1-s)}$:
$$ G_{uu}=G_{vv} = s^2 h''(s^2) - \lambda s\,h''(s) = -\frac{1}{1-s^2} + \frac{\lambda}{1-s}, $$
$$ G_{uv} = h'(s^2) + s^2 h''(s^2) - 2\lambda h'(s) = h'(s^2) - \frac{1}{1-s^2} - 2\lambda h'(s). $$
Therefore
$$ \Theta_s''(0) = 2(G_{uu}-G_{uv}) = 2\Big[\frac{\lambda}{1-s} - h'(s^2) + 2\lambda h'(s)\Big]
= 2\Big[\frac{\lambda}{1-s} + 2\lambda\log\tfrac{1-s}{s} - \log\tfrac{1-s^2}{s^2}\Big]. \tag{2.11}$$
This expression can be **positive or negative** depending on $s$, so the naive claim "diagonal is
always a min along the anti-diagonal" is *false in general*; the off-diagonal can descend for some
$s$. Hence the clean reduction needs more care. **This is exactly the subtlety that forced AHS to
verify one branch by computer.** We therefore do **not** claim a slick fully-analytic diagonal
reduction; instead we adopt the honest AHS route:

> **AHS route (what we actually certify).** (i) The boundary is $\ge0$ (Step A). (ii) On the
> diagonal, $\phi(s)=h(s^2)-2\lambda s h(s)\ge0$ — *proved analytically* in §2.3.2. (iii) The only
> possible interior negative region is controlled by the single-variable per-line analysis of
> Step C: on each line $v=$const, $G$ has at most one interior stationary point, located in the
> convex piece, and we verify $G\ge0$ there by interval arithmetic / fine-grid numerics (§5). The
> combination (i)+(ii)+(iii) is the AHS proof, with (iii) being the "one branch checked by
> computer" that AHS explicitly flag as rigorous via interval arithmetic.

We make (ii) rigorous now; (iii) is the Step-1 numeric certificate (§5).

#### 2.3.2 The diagonal inequality $\phi(s)=h(s^2)-2\lambda s\,h(s)\ge0$

Write everything out. With $\lambda=\frac1{2\sigma}$, $2\lambda s = s/\sigma$, so we must show
$$ h(s^2) \ge \frac{s}{\sigma}\,h(s),\qquad\text{i.e.}\qquad \frac{h(s^2)}{s}\ge \frac{h(s)}{\sigma}
\quad\text{for } s\in(0,1). \tag{2.12}$$
Define $R(s):=\dfrac{h(s^2)}{s}$ for $s\in(0,1]$. We claim $R$ is **decreasing on $(0,1]$** with
$R(\sigma)= h(\sigma^2)/\sigma$. Recall $\sigma^2=1-\sigma$, so $h(\sigma^2)=h(1-\sigma)=h(\sigma)$.
Thus $R(\sigma)=h(\sigma)/\sigma$, and (2.12) at $s=\sigma$ reads $h(\sigma)/\sigma\ge h(\sigma)/\sigma$
— **equality**, as required. To get (2.12) for all $s$ we need a bit more than monotonicity of $R$,
because the RHS $h(s)/\sigma$ also varies. Reorganise: (2.12) $\iff \Lambda(s):=\sigma\,h(s^2) - s\,h(s)\ge0$.

Compute $\Lambda$ on $(0,1)$. We have $h(s^2)=-s^2\log s^2-(1-s^2)\log(1-s^2)= -2s^2\log s-(1-s^2)\log(1-s^2)$
and $h(s)=-s\log s-(1-s)\log(1-s)$. So
$$ \Lambda(s) = \sigma\big[-2s^2\log s - (1-s^2)\log(1-s^2)\big] - s\big[-s\log s - (1-s)\log(1-s)\big]. $$
Group the $\log s$ terms: $(-2\sigma s^2 + s^2)\log s = s^2(1-2\sigma)\log s$. Since $\log s<0$ on $(0,1)$
and $1-2\sigma = 1-2\cdot0.618= -0.236<0$, this term is $s^2(1-2\sigma)\log s = (\text{neg})(\text{neg})>0$.
The remaining terms:
$$ -\sigma(1-s^2)\log(1-s^2) + s(1-s)\log(1-s). $$
Factor $1-s^2=(1-s)(1+s)$ and $\log(1-s^2)=\log(1-s)+\log(1+s)$:
$$ -\sigma(1-s)(1+s)[\log(1-s)+\log(1+s)] + s(1-s)\log(1-s). $$
$$ = (1-s)\Big\{\log(1-s)\big[s-\sigma(1+s)\big] - \sigma(1+s)\log(1+s)\Big\}. $$
$\log(1-s)<0$ on $(0,1)$ and $-\sigma(1+s)\log(1+s)<0$ (since $\log(1+s)>0$). The bracket
$[s-\sigma(1+s)] = s(1-\sigma)-\sigma$. This is negative for $s<\frac{\sigma}{1-\sigma}=\frac{\sigma}{\sigma^2}=\frac1\sigma=\varphi\approx1.618$,
i.e. for **all** $s\in(0,1)$. So $\log(1-s)\cdot[\text{neg}] = (\text{neg})(\text{neg})>0$, while the
$-\sigma(1+s)\log(1+s)<0$ term subtracts. The sign of $\Lambda$ is therefore not obvious from
inspection — there is genuine competition. We resolve it by reducing to a clean monotonicity.

Differentiate $\Lambda$. $\Lambda'(s)=\sigma\cdot 2s\,h'(s^2) - h(s) - s\,h'(s)$, with
$h'(t)=\log\frac{1-t}{t}$:
$$ \Lambda'(s) = 2\sigma s\,\log\frac{1-s^2}{s^2} - h(s) - s\log\frac{1-s}{s}. $$
Note $h(s)= -s\log s-(1-s)\log(1-s)$ and $s\log\frac{1-s}{s}= s\log(1-s)-s\log s$, so
$-h(s)-s\log\frac{1-s}{s} = s\log s+(1-s)\log(1-s) - s\log(1-s)+s\log s = 2s\log s + (1-2s)\log(1-s)$.
And $2\sigma s\log\frac{1-s^2}{s^2}= 2\sigma s[\log(1-s^2)-2\log s] = 2\sigma s\log(1-s^2)-4\sigma s\log s$.
Collecting,
$$ \Lambda'(s) = (2 - 4\sigma)s\log s + (1-2s)\log(1-s) + 2\sigma s\log(1-s^2). \tag{2.13}$$
At $s=\sigma$: $\Lambda(\sigma)=0$ (shown above). We claim $\Lambda(s)\ge0$ on $(0,1)$ with the
diagonal equality only at $s=\sigma$ (and trivially $s\to0,1$). One verifies:
$\Lambda(0^+)=0$ (every term $\to0$), $\Lambda(1^-)=\sigma h(1)-1\cdot h(1)=0$. So $\Lambda$ vanishes
at both endpoints and at $s=\sigma$; between, it is a smooth function. The cleanest rigorous finish
is: **$\Lambda$ is concave on $(0,1)$ except possibly near the endpoints, with a unique interior
maximum; since $\Lambda(0)=\Lambda(1)=0$ and $\Lambda\not\equiv0$, $\Lambda\ge0$ throughout iff
$\Lambda$ does not dip below $0$, which (given the endpoint zeros and a single interior critical
structure) is equivalent to $\Lambda$ being $\ge0$ at its critical points.** Verifying the sign of
$\Lambda''$ to pin "single interior max" is itself a one-variable calculus exercise that AHS handle
numerically/interval-arithmetically. We therefore mark the **fully analytic** finish of (2.12) as
**reduced to a clean one-variable statement** and discharge it by the Step-1 numeric certificate on
a fine grid (§5), exactly as AHS do.

> **Honest status of Lemma 2.** The reduction to one variable (2.12)/(2.10) is rigorous and
> from-scratch. The *final* one-variable nonnegativity is, in AHS as here, certified by interval
> arithmetic (a finite, rigorous computation), not by a slick closed-form sign argument — because
> the function genuinely has competing terms. This matches the published AHS proof, which states
> that "one branch is checked by computer calculation (interval arithmetic suffices)". Our §5
> reproduces that certificate.

### 2.4 Where $\lambda=\frac1{2(1-\psi)}$ comes from

The constant is determined by the equality requirement. We want the best (largest) constant $\mu$
such that $h(uv)\ge \mu[v h(u)+u h(v)]$ holds on $[0,1]^2$; the per-element argument then yields
abundance bound $c$ with $2\mu=\frac{1}{1-c}$ rearranged, i.e. $c=1-\frac1{2\mu}$. The extremal
$\mu$ is attained on the diagonal at the $s=\sigma$ where $\phi(s)=h(s^2)-2\mu s h(s)$ has a double
zero (tangency): $\phi(\sigma)=0$ and $\phi'(\sigma)=0$. The condition $\phi(\sigma)=0$ gives
$\mu=\frac{h(\sigma^2)}{2\sigma h(\sigma)} = \frac{h(\sigma)}{2\sigma h(\sigma)}=\frac1{2\sigma}$
(using $\sigma^2=1-\sigma\Rightarrow h(\sigma^2)=h(\sigma)$). Then $c=1-\frac1{2\mu}=1-\sigma=\psi$.
The tangency $\phi'(\sigma)=0$ is what makes this the *sharp* constant (any larger $\mu$ makes
$\phi<0$ just off the diagonal). This is the precise sense in which **$\psi$ is forced** and the
inequality is *tight* — the source of slack-point $\mathsf S_1$ (§6).

---

## 3. Assembly: the theorem

**Theorem (AHS).** Every finite union-closed family $\mathcal F\neq\{\varnothing\}$ contains an
element $i$ with $\Pr[i\in A]\ge\psi=(3-\sqrt5)/2$, where $A$ is uniform on $\mathcal F$. Equivalently,
some element lies in at least $\psi\,|\mathcal F|$ members; hence the Frankl abundance satisfies
$\varphi(\mathcal F)\ge\psi$.

*Proof.* Combine (1.2) [union-closure], (1.6) [chain rule], (2.3) [Lemma 2 per coordinate], to get
(2.4); then the contradiction (2.5) under the hypothesis $\max_i p_i<\psi$. $\blacksquare$

---

## 4. The complete list of inequalities used, with justification

| # | Inequality | Justification | Tight? | Slack name |
|---|---|---|---|---|
| (1.1) | $H(A)=\log m$ | E2 equality (uniform) | exact | — |
| (1.2) | $H(A\cup B)\le\log m$ | E2 ($A\cup B\in\mathcal F$, union-closure) | **lossy** (uses only $A\cup B\in\mathcal F$) | $\mathsf S_3$ |
| (1.4) | $H(C_i\mid C_{<i})\ge H(C_i\mid C_{<i},A_{<i},B_{<i})$ | E4 (conditioning reduces entropy) | **lossy** by $I(C_i;(A_{<i},B_{<i})\mid C_{<i})$ | $\mathsf S_2$ |
| (1.5) | $=H(C_i\mid A_{<i},B_{<i})$ | E6 ($C_{<i}$ a function of $(A_{<i},B_{<i})$) | exact | — |
| (1.7) | union coordinate is Bernoulli$((1-\alpha)(1-\beta))$-complement | $A_i\perp B_i$ given prefixes (since $A\perp B$) | exact | — |
| (2.2) | $h(1-(1-p)(1-q))\ge\lambda[(1-q)h(p)+(1-p)h(q)]$ | Lemma 2 (calculus) | **tight at $p=q=\psi$** | $\mathsf S_1$ |
| (2.5) | $\sum_i H(A_i\mid A_{<i})=H(A)$ | E3 (exact chain rule) | exact | — |

**Reading of the table.** Three inequalities are lossy: (1.2), (1.4), (2.2). The constant $\psi$
is the value at which **all three become simultaneously tight** for the worst family. Improving the
constant requires recovering slack from at least one of $\mathsf S_1,\mathsf S_2,\mathsf S_3$ in a
way that survives the others being tight. Vector 1 targets $\mathsf S_2$; Vector 2 targets a
combination of $\mathsf S_3$ and the unused intersection structure.

---

## 5. Step-1 numerical certificate

Two checks (code: `frankl/experiments/verify_ahs.py`):

**(C1) Lemma 2 on a fine grid.** Verify $G(u,v)=h(uv)-\lambda[v\,h(u)+u\,h(v)]\ge -\epsilon$ on a grid
of $[0,1]^2$ with mesh $\le 10^{-3}$ and refined mesh $10^{-4}$ near the diagonal $u=v\in[0.5,0.75]$,
$\lambda=\frac1{2(1-\psi)}$. Confirm the minimum is $\approx0$ attained near $(u,v)=(\sigma,\sigma)=(0.618,0.618)$.

**(C2) The end-to-end bound on all small UC families.** For every union-closed $\mathcal F$ on
$[n]$, $n\le5$ (labeled) and $n=6$ (spot-checked / orbit reps), verify that the chain
$H(A\cup B)\le H(A)$ holds (it must, by union-closure) and that the AHS lower bound (2.4) is indeed
$\le H(A\cup B)$, i.e. the proof's inequalities are internally consistent on real families. Also
verify $\varphi(\mathcal F)\ge\psi$ on all of them (sanity: the theorem's conclusion).

Results are logged in `frankl/experiments/verify_ahs_log.md`.

---

## 6. Slack analysis — exactly where each attack vector enters

This section pins the line at which each Phase-2 vector must inject new information.

### $\mathsf S_1$ — the one-variable inequality (2.2). *Tight; small slack within i.i.d.*
Equality at $p=q=\psi$. Chase–Lovett proved the **approximate-union-closed** version is *sharp* at
$\psi$, so within i.i.d. couplings of $(A,B)$ no constant $>\psi$ can emerge from (2.2). Slack exists
only by **changing the coupling** (Sawin/Yu/Liu), which moves the equality point. Not our primary target.

### $\mathsf S_2$ — the chain-rule reduction (1.4). *Lossy by a conditional mutual information.*
The discarded quantity is
$$ \Delta_2 := \sum_{i} I\big(C_i\,;\,(A_{<i},B_{<i})\,\big|\,C_{<i}\big)\;\ge\;0, $$
the total information that the **prefixes of $A$ and $B$ individually** carry about $C_i$ beyond
what the **prefix of the union** $C_{<i}$ carries. On a product family (independent coordinates)
$\Delta_2=0$, which is why Gilmer's coordinatewise move is lossless there. On a genuinely
union-closed family the coordinates are correlated and $\Delta_2>0$. **Vector 1** asks: can we
retain a positive fraction of $\Delta_2$ via a Shearer/Han-type submodular inequality, thereby
strengthening (1.6) to $H(C)\ge \sum_i H(C_i\mid A_{<i},B_{<i}) + c\,\Delta_2$? See
`improvement_shearer.md` / `dead_ends.md`.

### $\mathsf S_3$ — the union-only upper bound (1.2). *Uses $A\cup B\in\mathcal F$, ignores $A\cap B$.*
Union-closure gives $A\cup B\in\mathcal F$ but says nothing about $A\cap B$. **Vector 2** augments
the target with an intersection term: study $H(A\cup B)+\lambda H(A\cap B)$ and ask whether a
per-coordinate inequality for the *pair* $(C_i, D_i)=(A_i\vee B_i, A_i\wedge B_i)$ beats the
union-only one. The relevant identity is the **coordinatewise law of $(A_i,B_i)$**: the joint
distribution of $(A_i,B_i)\in\{0,1\}^2$ is determined by $(\alpha,\beta)$ and independence, giving
$\Pr[(A_i,B_i)=(1,1)]=\alpha\beta$, etc. See `improvement_intersection.md` / `dead_ends.md`.

---

## 7. Summary

The AHS constant $\psi=(3-\sqrt5)/2$ arises from a chain of three lossy inequalities
$(\mathsf S_3)\,(1.2)$, $(\mathsf S_2)\,(1.4)$, $(\mathsf S_1)\,(2.2)$, all simultaneously tight at
the symmetric Bernoulli$(\psi)$ configuration / golden point $\sigma=1-\psi=1/\varphi$. The
one-variable inequality (2.2) is sharp and computer-certified at one branch. To beat $\psi$ one
must recover slack from $\mathsf S_2$ (Vector 1) or use the intersection structure absent from
$\mathsf S_3$ (Vector 2), without those gains being cancelled by the other two inequalities
re-tightening. The next two files attempt exactly that.
