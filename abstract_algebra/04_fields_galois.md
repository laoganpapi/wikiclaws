# Fields & Galois Theory

> A dictionary between the symmetry of a polynomial's roots and the structure of the field they live in, powerful enough to decide which equations and which geometric constructions are possible at all.

## 0. Why this matters (the big picture)

You learned the quadratic formula as a child. There are also (uglier) formulas for the cubic and the quartic. So the natural question is: **is there a formula for the quintic?** More precisely, can every polynomial equation be solved by *radicals*, meaning starting from the coefficients and combining them with $+,-,\times,\div$ and $n$-th roots? Galois theory answers this, and the answer is no. The same circle of ideas settles three problems the Greeks could not crack with straightedge and compass: doubling the cube, trisecting an arbitrary angle, and squaring the circle. The trick in every case is the same astonishing move: translate a question about *numbers* into a question about a *group of symmetries*, and let the group do the talking.

**The motivating question:** *Which polynomial equations are solvable by radicals, and which angles, lengths, and figures can be constructed with straightedge and compass alone?*

## 1. Key terms, explained simply

Recall from doc #3: a **field** is a commutative ring in which every nonzero element has a multiplicative inverse. So you can add, subtract, multiply, and divide (except by $0$). Examples: $\mathbb{Q}$ (rationals), $\mathbb{R}$ (reals), $\mathbb{C}$ (complex), and the finite field $\mathbb{F}_p = \mathbb{Z}/p\mathbb{Z}$ for $p$ prime. Throughout, $F[x]$ means polynomials in $x$ with coefficients in $F$, and a polynomial is **monic** if its leading coefficient is $1$.

**Field extension $K/F$.**
(a) *Intuition.* A bigger field $K$ sitting on top of a smaller field $F$, like $\mathbb{C}$ sitting on top of $\mathbb{R}$. You enlarge $F$ by throwing in new numbers and everything they generate.
(b) *Definition.* $K/F$ (read "$K$ over $F$") means $F$ is a subfield of $K$. The slash is **not** division; it is the standard notation for an extension.
(c) *Example.* $\mathbb{C}/\mathbb{R}$, and $\mathbb{R}/\mathbb{Q}$.

**Degree $[K:F]$.**
(a) *Intuition.* Here is the key idea that makes the whole theory work: if $F \subseteq K$, then $K$ is automatically a **vector space over $F$** (you can add elements of $K$ and scale them by elements of $F$). The degree is the dimension of that vector space, a single number measuring "how much bigger" $K$ is.
(b) *Definition.* $[K:F] = \dim_F K$, the dimension of $K$ as an $F$-vector space. The extension is **finite** if $[K:F]<\infty$ and **infinite** otherwise.
(c) *Example.* $\mathbb{C} = \mathbb{R} + \mathbb{R}\, i$ has basis $\{1, i\}$ over $\mathbb{R}$, so $[\mathbb{C}:\mathbb{R}] = 2$. Meanwhile $[\mathbb{R}:\mathbb{Q}] = \infty$.

**Algebraic and transcendental elements.**
(a) *Intuition.* An element of $K$ is algebraic over $F$ if it is the root of some polynomial equation with coefficients in $F$; otherwise it is transcendental ("escapes" all such equations).
(b) *Definition.* $\alpha \in K$ is **algebraic over $F$** if $f(\alpha)=0$ for some nonzero $f \in F[x]$; otherwise $\alpha$ is **transcendental over $F$**.
(c) *Example.* $\sqrt2$ is algebraic over $\mathbb{Q}$ (root of $x^2 - 2$). The numbers $\pi$ and $e$ are transcendental over $\mathbb{Q}$ (hard theorems, stated later).

**Minimal polynomial $m_\alpha(x)$.**
(a) *Intuition.* Among all polynomials over $F$ killed by $\alpha$, there is a unique simplest one. It is the "true equation" satisfied by $\alpha$, and every other equation $\alpha$ satisfies is a multiple of it.
(b) *Definition.* For $\alpha$ algebraic over $F$, the **minimal polynomial** $m_\alpha(x)$ is the unique monic polynomial in $F[x]$ of least degree with $m_\alpha(\alpha)=0$. It is always **irreducible** over $F$, and it generates the kernel of the evaluation map $\mathrm{ev}_\alpha: F[x]\to K$, $f \mapsto f(\alpha)$. That is, $f(\alpha)=0 \iff m_\alpha \mid f$.
(c) *Example.* Over $\mathbb{Q}$, the minimal polynomial of $\sqrt2$ is $x^2 - 2$; of $i$ it is $x^2+1$; of $\sqrt[3]{2}$ it is $x^3 - 2$.

**Simple extension $F(\alpha)$.**
(a) *Intuition.* The smallest field containing $F$ and one new element $\alpha$. You are forced to include all sums, products, and inverses, but it turns out you get everything as polynomials in $\alpha$.
(b) *Definition.* $F(\alpha)$ is the smallest subfield of $K$ containing $F$ and $\alpha$. When $\alpha$ is algebraic, $F(\alpha) = \{c_0 + c_1\alpha + \dots + c_{n-1}\alpha^{n-1} : c_i \in F\}$ where $n = \deg m_\alpha$.
(c) *Example.* $\mathbb{Q}(\sqrt2) = \{a + b\sqrt2 : a,b\in\mathbb{Q}\}$.

**Splitting field.**
(a) *Intuition.* Take a polynomial that does not fully factor over $F$. The splitting field is the smallest extension where it *does* break into linear factors, i.e. where it finally has all its roots.
(b) *Definition.* The **splitting field** of $f \in F[x]$ over $F$ is the smallest field $K \supseteq F$ in which $f$ factors completely into linear factors, $f(x)=c\prod_i (x-\alpha_i)$, equivalently $K = F(\alpha_1,\dots,\alpha_n)$ generated by all roots.
(c) *Example.* The splitting field of $x^2 - 2$ over $\mathbb{Q}$ is $\mathbb{Q}(\sqrt2)$, since the roots are $\pm\sqrt2$.

**Field automorphism, and $\mathrm{Gal}(K/F)$.**
(a) *Intuition.* A symmetry of $K$: a relabeling of its elements that respects $+$ and $\times$ and leaves every element of the base field $F$ untouched. Such a map can only shuffle roots of a polynomial among themselves, so it is a "symmetry of the roots."
(b) *Definition.* An **$F$-automorphism** of $K$ is a bijection $\sigma:K\to K$ with $\sigma(x+y)=\sigma x+\sigma y$, $\sigma(xy)=\sigma x\,\sigma y$, and $\sigma(a)=a$ for all $a\in F$. These form a group under composition, the **Galois group** $\mathrm{Gal}(K/F)$ (also written $\mathrm{Aut}(K/F)$).
(c) *Example.* $\mathrm{Gal}(\mathbb{C}/\mathbb{R}) = \{\mathrm{id},\ \text{complex conjugation}\}$, a group of order $2$.

**Normal, separable, and Galois extensions.**
(a) *Intuition.* "Normal" means $K$ is closed under taking conjugate roots: if it contains one root of an irreducible polynomial, it contains them all (no root is left behind). "Separable" means irreducible polynomials have no repeated roots, so an irreducible of degree $n$ genuinely has $n$ distinct roots. "Galois" = both, the well-behaved case where symmetry counts are exactly right.
(b) *Definition.* A finite extension $K/F$ is **normal** if it is the splitting field of some polynomial over $F$. It is **separable** if the minimal polynomial of every element of $K$ has no repeated roots. It is **Galois** if it is both normal and separable, and this happens exactly when $|\mathrm{Gal}(K/F)| = [K:F]$. *Good news for beginners:* in **characteristic $0$** (e.g. any subfield of $\mathbb{C}$) and over finite fields, every extension is separable, so we may quietly ignore separability and read "Galois" as "normal" (= splitting field). Fields with this automatic-separability property are called **perfect**.
(c) *Example.* $\mathbb{Q}(\sqrt2)/\mathbb{Q}$ is Galois (it splits $x^2-2$, and $|\mathrm{Gal}|=2=[\mathbb{Q}(\sqrt2):\mathbb{Q}]$). By contrast $\mathbb{Q}(\sqrt[3]{2})/\mathbb{Q}$ is **not** normal: it contains the real cube root of $2$ but not the two complex ones, so it splits nothing of degree $3$.

**Solvable group.**
(a) *Intuition.* A group built up out of abelian (commutative) pieces, layer by layer. "Solvable" is named exactly for its connection to solving equations.
(b) *Definition.* A finite group $G$ is **solvable** if there is a chain $\{e\}=G_0 \trianglelefteq G_1 \trianglelefteq \dots \trianglelefteq G_k = G$ (each $G_i$ normal in the next) such that every quotient $G_{i+1}/G_i$ is abelian. (The symbol $\trianglelefteq$ means "normal subgroup of"; quotients were covered in docs #2/#3.)
(c) *Example.* Every abelian group is solvable. $S_3$ is solvable via $\{e\}\trianglelefteq A_3 \trianglelefteq S_3$ with quotients of orders $3$ and $2$, both abelian.

## 2. Worked examples

### Example A: The minimal polynomial and degree of $\sqrt[3]{2}$, with $\mathbb{Q}(\sqrt[3]{2})$ explicit

Let $\alpha = \sqrt[3]{2}$. It satisfies $x^3 - 2 = 0$.

*Is $x^3-2$ the minimal polynomial?* We need it irreducible over $\mathbb{Q}$. By **Eisenstein's criterion** at the prime $p=2$ (recall doc #3: $p$ divides every non-leading coefficient, $p$ does not divide the leading coefficient, and $p^2$ does not divide the constant term), $x^3 - 2$ is irreducible. Being monic, irreducible, and killed by $\alpha$, it **is** $m_\alpha(x)$.

*Degree.* The fundamental theorem of simple algebraic extensions says
$$[F(\alpha):F] = \deg m_\alpha(x).$$
Here $[\mathbb{Q}(\sqrt[3]{2}):\mathbb{Q}] = 3$, with $F$-basis $\{1,\ \alpha,\ \alpha^2\}$. So every element is $a + b\sqrt[3]{2} + c\sqrt[3]{4}$ with $a,b,c\in\mathbb{Q}$.

*Why a basis of three?* Inside $\mathbb{Q}(\alpha)$ we can reduce any power of $\alpha$ using $\alpha^3 = 2$: for instance $\alpha^4 = \alpha\cdot\alpha^3 = 2\alpha$. So $1,\alpha,\alpha^2$ already span, and they are independent because no nonzero polynomial of degree $<3$ kills $\alpha$.

*Bonus, computing an inverse without guessing.* To invert $1+\alpha$, use that $\gcd(x^3-2,\ 1+x)=1$ in $\mathbb{Q}[x]$. Since $(-1)^3 - 2 = -3$, we have $x^3 - 2 = (x+1)(x^2 - x + 1) - 3$, so $(1+\alpha)(\alpha^2-\alpha+1) = 3$, giving $(1+\alpha)^{-1} = \tfrac13(\alpha^2 - \alpha + 1)$. This is the practical payoff of "minimal polynomial generates the kernel."

### Example B: $\mathbb{Q}(i)$ and a sanity check that it is a field

Let $\alpha = i$, root of $x^2 + 1$. This has no real (hence no rational) roots, so as a degree-$2$ polynomial it is irreducible over $\mathbb{Q}$; thus $m_i(x) = x^2 + 1$ and $[\mathbb{Q}(i):\mathbb{Q}] = 2$ with basis $\{1, i\}$. So $\mathbb{Q}(i) = \{a+bi : a,b\in\mathbb{Q}\}$ (the **Gaussian rationals**). To see division works: 
$$\frac{1}{a+bi} = \frac{a-bi}{a^2+b^2},$$
and $a^2+b^2 \ne 0$ whenever $(a,b)\ne(0,0)$, so every nonzero element is invertible, confirming it is a field. The single nontrivial automorphism is $i \mapsto -i$ (conjugation), so $\mathrm{Gal}(\mathbb{Q}(i)/\mathbb{Q}) \cong \mathbb{Z}/2\mathbb{Z}$.

### Example C: The Tower Law in action, and the splitting field of $x^3 - 2$

**Tower Law.** For fields $F \subseteq K \subseteq L$ with finite degrees,
$$[L:F] = [L:K]\,[K:F].$$
(Reason: if $\{u_i\}$ is a $K$-basis of $L$ and $\{v_j\}$ an $F$-basis of $K$, then $\{u_i v_j\}$ is an $F$-basis of $L$; the dimensions multiply.)

Now build the splitting field of $f(x)=x^3 - 2$ over $\mathbb{Q}$. The three roots are
$$\sqrt[3]{2},\quad \omega\sqrt[3]{2},\quad \omega^2\sqrt[3]{2},\qquad \omega = e^{2\pi i/3}=\tfrac{-1+\sqrt{-3}}{2},$$
where $\omega$ is a primitive cube root of unity satisfying $\omega^2+\omega+1=0$. The splitting field is $K=\mathbb{Q}(\sqrt[3]{2},\omega)$.

Compute $[K:\mathbb{Q}]$ via a tower:
$$\mathbb{Q} \ \subseteq\ \mathbb{Q}(\sqrt[3]{2}) \ \subseteq\ \mathbb{Q}(\sqrt[3]{2},\omega).$$
- $[\mathbb{Q}(\sqrt[3]{2}):\mathbb{Q}] = 3$ (Example A).
- $\mathbb{Q}(\sqrt[3]{2})$ is a subfield of $\mathbb{R}$, but $\omega$ is not real, so $\omega \notin \mathbb{Q}(\sqrt[3]{2})$. Its minimal polynomial over $\mathbb{Q}(\sqrt[3]{2})$ is $x^2+x+1$ (degree $2$, no root in a real field), so $[\mathbb{Q}(\sqrt[3]{2},\omega):\mathbb{Q}(\sqrt[3]{2})]=2$.

By the Tower Law, $[K:\mathbb{Q}] = 2\cdot 3 = 6$. (Compare: the splitting field of $x^2 - 2$ is just $\mathbb{Q}(\sqrt2)$, degree $2$, because both roots $\pm\sqrt2$ already lie there once one does.)

### Example D: $F(\alpha) \cong F[x]/(m_\alpha)$, constructing $\mathbb{F}_4$

The structural heart of simple extensions: if $\alpha$ is algebraic over $F$ with minimal polynomial $m_\alpha$, then
$$F(\alpha) \ \cong\ F[x]/\bigl(m_\alpha(x)\bigr).$$
*Why:* the evaluation map $\mathrm{ev}_\alpha: F[x]\to F(\alpha)$ is a surjective ring homomorphism with kernel $(m_\alpha)$; the First Isomorphism Theorem (doc #3) gives the result. Because $m_\alpha$ is irreducible, $(m_\alpha)$ is a maximal ideal, so the quotient is a field, exactly as it must be.

This is also how we *build* new fields from scratch. Take $F=\mathbb{F}_2=\{0,1\}$ and $m(x)=x^2+x+1$. It has no root in $\mathbb{F}_2$ (check: $0\mapsto 1$, $1\mapsto 1$), so it is irreducible. Then
$$\mathbb{F}_4 := \mathbb{F}_2[x]/(x^2+x+1) = \{0,\ 1,\ \alpha,\ \alpha+1\},\qquad \alpha^2 = \alpha+1,$$
a field with $4 = 2^2$ elements. Its multiplication is forced by $\alpha^2=\alpha+1$. For instance $\alpha^3 = \alpha\cdot\alpha^2 = \alpha(\alpha+1)=\alpha^2+\alpha=(\alpha+1)+\alpha=1$, so $\alpha$ has multiplicative order $3$ and generates $\mathbb{F}_4^\times$. We will reuse this construction in Section 1's finite-field discussion below.

## 3. Basic exercises

1. Find the minimal polynomial of $\sqrt5$ over $\mathbb{Q}$ and state $[\mathbb{Q}(\sqrt5):\mathbb{Q}]$.
2. Find the minimal polynomial of $\sqrt[4]{2}$ over $\mathbb{Q}$ and give a $\mathbb{Q}$-basis of $\mathbb{Q}(\sqrt[4]{2})$.
3. Using the Tower Law, compute $[\mathbb{Q}(\sqrt2,\sqrt3):\mathbb{Q}]$. (You may use that $\sqrt3 \notin \mathbb{Q}(\sqrt2)$.)
4. Show that $x^2 + x + 1$ is irreducible over $\mathbb{F}_2$ but reducible over $\mathbb{F}_4$. (For the second part, recall $\mathbb{F}_4$ contains its roots.)
5. What is the splitting field of $x^2 + 1$ over $\mathbb{R}$? Over $\mathbb{Q}$? Give the degree in each case.
6. List all elements of $\mathbb{F}_9 = \mathbb{F}_3[x]/(x^2+1)$, and find the multiplicative order of $i$ (the class of $x$). Is $i$ a generator of $\mathbb{F}_9^\times$?
7. Express $(1 + \sqrt2)^{-1}$ in the form $a + b\sqrt2$ with $a,b\in\mathbb{Q}$.

### Solutions

**1.** $\sqrt5$ satisfies $x^2 - 5$, irreducible over $\mathbb{Q}$ (Eisenstein at $5$, or: no rational root since $5$ is not a perfect square). So $m(x)=x^2-5$ and $[\mathbb{Q}(\sqrt5):\mathbb{Q}]=2$.

**2.** $\sqrt[4]{2}$ satisfies $x^4 - 2$, irreducible by Eisenstein at $2$. So $[\mathbb{Q}(\sqrt[4]{2}):\mathbb{Q}]=4$ with basis $\{1,\ \sqrt[4]{2},\ \sqrt[4]{2}^{\,2},\ \sqrt[4]{2}^{\,3}\} = \{1,\ 2^{1/4},\ 2^{1/2},\ 2^{3/4}\}$.

**3.** Tower $\mathbb{Q}\subseteq\mathbb{Q}(\sqrt2)\subseteq\mathbb{Q}(\sqrt2,\sqrt3)$. First step: $[\mathbb{Q}(\sqrt2):\mathbb{Q}]=2$. Second: $\sqrt3$ has minimal polynomial $x^2 - 3$ over $\mathbb{Q}(\sqrt2)$ (it is degree $2$ and $\sqrt3\notin\mathbb{Q}(\sqrt2)$ by hypothesis, so it stays irreducible), giving degree $2$. Total $[\mathbb{Q}(\sqrt2,\sqrt3):\mathbb{Q}] = 2\cdot 2 = 4$, with basis $\{1,\sqrt2,\sqrt3,\sqrt6\}$.

**4.** Over $\mathbb{F}_2$: plug in both elements, $f(0)=1\neq 0$ and $f(1)=1+1+1=1\neq 0$; a degree-$2$ polynomial with no roots is irreducible. Over $\mathbb{F}_4$: the element $\alpha$ (with $\alpha^2=\alpha+1$, i.e. $\alpha^2+\alpha+1=0$) is a root, so $(x-\alpha)$ divides $f$. Indeed $x^2+x+1 = (x-\alpha)(x-(\alpha+1))$ over $\mathbb{F}_4$ (the two roots are $\alpha$ and $\alpha+1=\alpha^2$).

**5.** Over $\mathbb{R}$: roots are $\pm i$, splitting field $\mathbb{R}(i)=\mathbb{C}$, degree $2$. Over $\mathbb{Q}$: splitting field $\mathbb{Q}(i)$, degree $2$.

**6.** $\mathbb{F}_9 = \{a + bi : a,b\in\mathbb{F}_3\}$ with $i^2=-1$, i.e. the nine elements $0,1,2,i,1+i,2+i,2i,1+2i,2+2i$. Order of $i$: $i^2 = -1 = 2$, $i^3 = -i = 2i$, $i^4 = (i^2)^2 = 1$, so $\mathrm{ord}(i)=4$. Since $|\mathbb{F}_9^\times| = 8$ and $4 \neq 8$, $i$ is **not** a generator. (A generator is $1+i$: its powers run $1+i,\ 2i,\ 1+2i,\ 2,\ 2+2i,\ i,\ 2+i,\ 1$, hitting all eight nonzero elements, so $\mathrm{ord}(1+i)=8$.)

**7.** Rationalize: $\dfrac{1}{1+\sqrt2} = \dfrac{1-\sqrt2}{(1+\sqrt2)(1-\sqrt2)} = \dfrac{1-\sqrt2}{1-2} = \dfrac{1-\sqrt2}{-1} = -1 + \sqrt2$. So $a=-1,\ b=1$. (Check: $(1+\sqrt2)(-1+\sqrt2) = -1+\sqrt2-\sqrt2+2 = 1$.)

## 4. Advanced exercises

1. **Finite fields exist and are unique.** Construct $\mathbb{F}_8$ explicitly as $\mathbb{F}_2[x]/(p(x))$ for a suitable irreducible cubic $p$, and exhibit a generator of $\mathbb{F}_8^\times$. Then explain in one or two sentences why $\mathbb{F}_8$ is **not** a subfield of $\mathbb{F}_{16}$, even though $8$ and $16$ are both powers of $2$.
2. **The Galois correspondence for $\mathbb{Q}(\sqrt2,\sqrt3)/\mathbb{Q}$.** Show $\mathrm{Gal}(\mathbb{Q}(\sqrt2,\sqrt3)/\mathbb{Q})$ is the Klein four-group, and list the complete bijection between its subgroups and the intermediate fields.
3. **Doubling the cube is impossible.** Assuming the theorem that any constructible number has degree a power of $2$ over $\mathbb{Q}$, prove that you cannot construct $\sqrt[3]{2}$ with straightedge and compass.
4. **A quintic with Galois group $S_5$.** Show $f(x)=x^5 - 4x + 2$ is irreducible over $\mathbb{Q}$, determine how many real roots it has, and conclude that $\mathrm{Gal}(f/\mathbb{Q}) \cong S_5$. Why does this make $f$ unsolvable by radicals?
5. **The Frobenius automorphism.** Let $K=\mathbb{F}_{p^n}$. Show the map $\varphi(x)=x^p$ is a field automorphism of $K$ fixing $\mathbb{F}_p$, and that it has order exactly $n$ in $\mathrm{Gal}(K/\mathbb{F}_p)$, so $\mathrm{Gal}(\mathbb{F}_{p^n}/\mathbb{F}_p) \cong \mathbb{Z}/n\mathbb{Z}$ is cyclic, generated by $\varphi$.

### Solutions

**1.** Take $p(x)=x^3 + x + 1$ over $\mathbb{F}_2$. It has no root ($p(0)=1$, $p(1)=1+1+1=1$), and a cubic with no root is irreducible. So
$$\mathbb{F}_8 = \mathbb{F}_2[x]/(x^3+x+1) = \{a_0 + a_1\alpha + a_2\alpha^2 : a_i\in\mathbb{F}_2\},\qquad \alpha^3=\alpha+1,$$
which has $2^3=8$ elements. Generator: $|\mathbb{F}_8^\times|=7$ is prime, so **every** nonzero non-identity element has order $7$; in particular $\alpha$ generates (e.g. $\alpha^3=\alpha+1$, $\alpha^4 = \alpha^2+\alpha$, etc., cycling through all seven). Why $\mathbb{F}_8 \not\subseteq \mathbb{F}_{16}$: a subfield $\mathbb{F}_{p^d}\subseteq\mathbb{F}_{p^m}$ exists iff $d \mid m$ (this comes from the Tower Law applied to degrees over $\mathbb{F}_p$). Here $d=3$, $m=4$, and $3 \nmid 4$, so $\mathbb{F}_8$ is not inside $\mathbb{F}_{16}$. The containment chain for powers of $2$ goes $\mathbb{F}_2\subset\mathbb{F}_4\subset\mathbb{F}_{16}\subset\cdots$ ($d\mid m$), skipping $\mathbb{F}_8$.

**2.** Let $K=\mathbb{Q}(\sqrt2,\sqrt3)$; by Basic Exercise 3, $[K:\mathbb{Q}]=4$. An automorphism $\sigma$ must send each generator to a root of its minimal polynomial: $\sigma(\sqrt2)=\pm\sqrt2$ and $\sigma(\sqrt3)=\pm\sqrt3$, independently. That gives at most $4$ automorphisms, and since $K/\mathbb{Q}$ is Galois (it is the splitting field of $(x^2-2)(x^2-3)$), there are exactly $4$:
$$\mathrm{id},\quad \sigma:\ \sqrt2\mapsto-\sqrt2,\ \sqrt3\mapsto\sqrt3,\quad \tau:\ \sqrt2\mapsto\sqrt2,\ \sqrt3\mapsto-\sqrt3,\quad \sigma\tau:\ \sqrt2\mapsto-\sqrt2,\ \sqrt3\mapsto-\sqrt3.$$
Each is its own inverse ($\sigma^2=\tau^2=(\sigma\tau)^2=\mathrm{id}$), so $G \cong \mathbb{Z}/2 \times \mathbb{Z}/2$, the **Klein four-group** $V_4$. The Galois correspondence is the inclusion-reversing bijection $H \leftrightarrow K^H$ (fixed field). The three subgroups of order $2$ correspond to the three intermediate fields of degree $2$:

| Subgroup of $G$ | Fixed field | $[\,\cdot:\mathbb{Q}]$ |
|---|---|---|
| $\{\mathrm{id}\}$ | $K=\mathbb{Q}(\sqrt2,\sqrt3)$ | $4$ |
| $\langle\sigma\rangle=\{\mathrm{id},\sigma\}$ | $\mathbb{Q}(\sqrt3)$ | $2$ |
| $\langle\tau\rangle=\{\mathrm{id},\tau\}$ | $\mathbb{Q}(\sqrt2)$ | $2$ |
| $\langle\sigma\tau\rangle=\{\mathrm{id},\sigma\tau\}$ | $\mathbb{Q}(\sqrt6)$ | $2$ |
| $G$ | $\mathbb{Q}$ | $1$ |

Note the reversal: bigger subgroup $\leftrightarrow$ smaller field. The subtle entry is $\mathbb{Q}(\sqrt6)$: $\sigma\tau$ sends $\sqrt6=\sqrt2\,\sqrt3 \mapsto (-\sqrt2)(-\sqrt3)=\sqrt6$, so $\sqrt6$ is fixed by $\langle\sigma\tau\rangle$. Also $|H|\cdot[K^H:\mathbb{Q}] = 4 = |G|$ in every row, as the correspondence guarantees ($[K:K^H]=|H|$).

**3.** Constructing a length $\ell$ from a unit segment means $\ell$ is a constructible number. By the stated theorem, $[\mathbb{Q}(\ell):\mathbb{Q}]$ must be a power of $2$. "Doubling the cube" means building a cube of twice the volume, i.e. side $\ell$ with $\ell^3 = 2$, so $\ell=\sqrt[3]{2}$. But $[\mathbb{Q}(\sqrt[3]{2}):\mathbb{Q}]=3$ (Example A), and $3$ is not a power of $2$. Contradiction, so $\sqrt[3]{2}$ is not constructible. The cube cannot be doubled.

**4.** *Irreducible:* Eisenstein at $p=2$ ($2 \mid 4,\ 2\mid 2,\ 2\nmid 1$ leading, $2^2=4 \nmid 2$ constant), so $f$ is irreducible over $\mathbb{Q}$. *Real roots:* $f'(x)=5x^4 - 4$ has two real zeros at $x=\pm(4/5)^{1/4}$, so $f$ has at most $3$ real roots; evaluating, $f(-2)=-32+8+2<0$, $f(0)=2>0$, $f(1)=1-4+2<0$, $f(2)=32-8+2>0$ gives sign changes on $(-2,0),(0,1),(1,2)$, so exactly $3$ real roots and hence $2$ complex (conjugate) roots. *Galois group:* Let $G=\mathrm{Gal}(f/\mathbb{Q})\le S_5$ acting on the $5$ roots. Irreducibility of degree $5$ forces $5 \mid |G|$, so by Cauchy $G$ contains an element of order $5$, a $5$-cycle. Complex conjugation restricts to an automorphism of the splitting field that swaps the two non-real roots and fixes the three real ones, i.e. a transposition in $G$. A $5$-cycle together with a transposition generate all of $S_5$. Hence $G=S_5$. *Unsolvable:* by the main theorem of Section "Solvability" below, $f$ is solvable by radicals iff $G$ is a solvable group; but $S_5$ is not solvable (its only nontrivial proper normal subgroup is the simple non-abelian $A_5$). So $x^5-4x+2=0$ has **no** solution by radicals.

**5.** *Homomorphism:* $\varphi(xy)=(xy)^p=x^p y^p=\varphi(x)\varphi(y)$ always. For addition, the binomial theorem gives $(x+y)^p=\sum_{k=0}^{p}\binom{p}{k}x^k y^{p-k}$, and for $0<k<p$ the coefficient $\binom{p}{k}$ is divisible by $p$, hence $0$ in characteristic $p$; only the $k=0,p$ terms survive, so $(x+y)^p=x^p+y^p$ (the "freshman's dream"). *Bijective:* $\varphi$ is injective (a field homomorphism has trivial kernel) and $K$ is finite, so it is a bijection, hence an automorphism. *Fixes $\mathbb{F}_p$:* every $a\in\mathbb{F}_p$ satisfies $a^p=a$ by Fermat's little theorem, so $\varphi$ fixes $\mathbb{F}_p$ pointwise. *Order:* $\varphi^k(x)=x^{p^k}$. We have $\varphi^k=\mathrm{id}$ iff $x^{p^k}=x$ for all $x\in K$, i.e. every element of $K$ is a root of $x^{p^k}-x$. That polynomial has at most $p^k$ roots, while $|K|=p^n$, so we need $p^k\ge p^n$, i.e. $k\ge n$; and $k=n$ works since every element of $\mathbb{F}_{p^n}$ satisfies $x^{p^n}=x$. Thus $\varphi$ has order exactly $n$. Since $[K:\mathbb{F}_p]=n=|\langle\varphi\rangle|\le|\mathrm{Gal}(K/\mathbb{F}_p)|\le n$, equality holds and $\mathrm{Gal}(\mathbb{F}_{p^n}/\mathbb{F}_p)=\langle\varphi\rangle\cong\mathbb{Z}/n\mathbb{Z}$.

## 5. Real-world relevance

- **Cryptography and coding theory run on finite fields.** Every finite field has order $p^n$ for a prime $p$ (its **characteristic**), and for each prime power there is exactly one such field up to isomorphism, written $\mathbb{F}_{p^n}$ or $\mathrm{GF}(p^n)$. Its multiplicative group $\mathbb{F}_{p^n}^\times$ is **cyclic** of order $p^n-1$; a generator is a "primitive element." The AES block cipher does its mixing arithmetic in $\mathbb{F}_{2^8}=\mathbb{F}_{256}$ (bytes as field elements), Reed-Solomon codes (CDs, DVDs, QR codes, deep-space telemetry) encode data as evaluations of polynomials over $\mathbb{F}_{2^m}$, and elliptic-curve cryptography lives over $\mathbb{F}_p$ and $\mathbb{F}_{2^m}$. The cyclic structure of $\mathbb{F}_p^\times$ is exactly what makes the Diffie-Hellman key exchange and discrete-log problem tick. See **doc #5, Real-World Applications**, for the engineering details.
- **Ancient geometry, finally settled.** The constructible-number machinery turns three classical questions into degree computations: doubling the cube and trisecting a general angle both require a number of degree $3$ over $\mathbb{Q}$ (impossible, since constructibles have $2$-power degree), and squaring the circle requires $\sqrt\pi$, hence $\pi$, to be algebraic, which **Lindemann's theorem** (1882) says it is not. The same theory, via **Gauss**, says a regular $n$-gon is constructible iff $n = 2^k p_1\cdots p_r$ with the $p_i$ distinct **Fermat primes** (primes of the form $2^{2^t}+1$: namely $3,5,17,257,65537$). This is why the $17$-gon is constructible (Gauss's teenage triumph) but the regular $7$-gon and $9$-gon are not.

## 6. Common pitfalls & misconceptions

- **The slash in $K/F$ is not a quotient or division.** It just means "$K$ as an extension of $F$." Quotient *rings* $F[x]/(f)$ use the same slash for a genuinely different operation; context disambiguates.
- **Degree multiplies, it does not add.** In a tower $[L:F]=[L:K][K:F]$, never $[L:K]+[K:F]$.
- **The minimal polynomial must be irreducible.** $x^4 - 1$ is satisfied by $i$, but it is not $i$'s minimal polynomial; $x^2+1$ is. Always reduce to the irreducible factor that $\alpha$ actually satisfies.
- **A generator of the additive structure is not a generator of $\mathbb{F}_{p^n}^\times$.** In $\mathbb{F}_9$, the element $i$ has order $4$, not $8$; you must check the multiplicative order.
- **Not every extension is Galois (normal).** $\mathbb{Q}(\sqrt[3]{2})/\mathbb{Q}$ has only the trivial automorphism, so $|\mathrm{Aut}|=1\neq 3=[\,\cdot:\mathbb{Q}]$; it is missing the complex conjugate roots. The Galois correspondence applies only to Galois extensions.
- **"Solvable group" is a precise structural condition, not a vague one.** $S_4$ *is* solvable (so the quartic has a formula), but $S_5$ is not. The cutoff at $n=5$ comes from $A_n$ being simple and non-abelian for $n\ge 5$.
- **Unsolvable-by-radicals does not mean "no solutions."** The quintic still has $5$ complex roots (Fundamental Theorem of Algebra). It means there is no *radical formula* in the coefficients valid for all quintics; specific quintics and numerical methods are fine.
- **Solvable by radicals is about the general/specific polynomial, not the degree alone.** Plenty of individual high-degree polynomials (e.g. $x^5-2$, whose group is solvable) *are* solvable by radicals; Abel-Ruffini is about the *general* equation of degree $\ge 5$.

## 7. What to learn next

You now hold the dictionary that converts equations and constructions into group theory, the conceptual summit of a first course in algebra. Head to **doc #5, Real-World Applications**, to see this machinery do real work: finite fields powering AES and Reed-Solomon error correction, cyclic multiplicative groups underpinning Diffie-Hellman and elliptic-curve cryptography, and constructibility closing the book on the classical Greek geometry problems.
