# Ring Theory

> Two operations, one structure: how the arithmetic of $\mathbb{Z}$ and polynomials becomes a theory.

**Convention used throughout this document:** all rings have a multiplicative identity element $1$ (a "ring with unity"). When we say "ring" we mean "ring with $1$". We allow $1 = 0$, but that forces the ring to be the trivial zero ring $\{0\}$, which we usually ignore. Subrings are required to contain the same $1$.

---

## 0. Why this matters (the big picture)

Groups captured *one* operation (think of symmetry: composing motions). But the number systems you grew up with, $\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{R}$, and polynomials, carry *two* intertwined operations: addition and multiplication. A **ring** is the abstract structure that captures exactly this "arithmetic with $+$ and $\times$" pattern. The slogan to keep in mind: **rings are to ($\mathbb{Z}$ and polynomials) what groups are to symmetry.** And just as *normal subgroups* were exactly the subgroups you could quotient by, **ideals** are exactly the sub-objects of a ring you can quotient by. They are the "normal subgroups of ring theory."

**Motivating question.** In $\mathbb{Z}$, the equation $2x = 1$ has no solution, but in $\mathbb{Q}$ it does. In $\mathbb{Z}_6$ (arithmetic mod $6$), we even get the strange fact $2 \cdot 3 = 0$ with neither factor zero. Which rings behave "nicely" (no such surprises), which let you divide, and how do we build new rings (like the complex numbers $\mathbb{C}$) out of old ones (like the real polynomials $\mathbb{R}[x]$)? Ring theory answers all three.

---

## 1. Key terms, explained simply

Throughout, $R$ denotes a ring. Notation: $a + b$ and $ab$ (we write multiplication by juxtaposition); $0$ is the additive identity, $1$ the multiplicative identity, and $-a$ the additive inverse of $a$. "Abelian" means commutative as a group under $+$.

---

**Ring.**

(a) *Intuition.* A set where you can add, subtract, and multiply, with the two operations linked by the familiar distributive law $a(b+c) = ab + ac$. You are **not** promised division. $\mathbb{Z}$ is the prototype.

(b) *Formal definition.* A **ring** $(R, +, \cdot)$ is a set $R$ with two binary operations such that:
- $(R, +)$ is an **abelian group**: $+$ is associative and commutative, has identity $0$, and every $a$ has an inverse $-a$.
- $\cdot$ is **associative**: $(ab)c = a(bc)$, and has a **multiplicative identity** $1$ with $1a = a1 = a$ for all $a$.
- The **distributive laws** hold: $a(b+c) = ab+ac$ and $(a+b)c = ac+bc$ for all $a,b,c$.

(c) *Example.* $\mathbb{Z}$ with ordinary $+$ and $\times$. The integers form an abelian group under addition, multiplication is associative with identity $1$, and distributivity holds.

---

**Commutative ring.**

(a) *Intuition.* A ring where the order of multiplication never matters, just like ordinary numbers.

(b) *Formal definition.* A ring $R$ is **commutative** if $ab = ba$ for all $a, b \in R$. (Addition is *always* commutative in a ring; the word "commutative ring" refers only to multiplication.)

(c) *Example.* $\mathbb{Q}$, $\mathbb{R}$, $\mathbb{Z}_n$ are commutative. The ring $M_2(\mathbb{R})$ of $2\times 2$ real matrices is **not** (see below).

---

**Some standard rings (our running cast).**

- $\mathbb{Z}$: the integers. Commutative.
- $\mathbb{Z}_n = \{0, 1, \dots, n-1\}$: integers mod $n$, with addition and multiplication done modulo $n$. Commutative. Notation: $\overline{a}$ or just $a$ means the class of $a$.
- $\mathbb{Q}, \mathbb{R}, \mathbb{C}$: rationals, reals, complex numbers. All commutative; in fact **fields** (defined below).
- $R[x]$: **polynomials** in one variable $x$ with coefficients in a ring $R$, e.g. $\mathbb{R}[x]$, $\mathbb{Z}[x]$, $\mathbb{Z}_2[x]$. Add and multiply polynomials as usual. Commutative when $R$ is. The identity is the constant polynomial $1$.
- $M_2(R)$: the **matrix ring** of $2 \times 2$ matrices over $R$, with matrix addition and multiplication. The identity is $\begin{bmatrix}1 & 0\\ 0 & 1\end{bmatrix}$. **Noncommutative** (for $|R|>1$): for instance
$$\begin{pmatrix}0&1\\0&0\end{pmatrix}\begin{pmatrix}0&0\\1&0\end{pmatrix}=\begin{pmatrix}1&0\\0&0\end{pmatrix},\qquad \begin{pmatrix}0&0\\1&0\end{pmatrix}\begin{pmatrix}0&1\\0&0\end{pmatrix}=\begin{pmatrix}0&0\\0&1\end{pmatrix}.$$
- $\mathbb{Z}[i] = \{a + bi : a, b \in \mathbb{Z}\}$: the **Gaussian integers**, a subring of $\mathbb{C}$ (here $i^2 = -1$). Commutative.

**Non-examples and why.**
- $\mathbb{N} = \{0,1,2,\dots\}$ is **not** a ring: it is not a group under $+$ (no additive inverses, e.g. no $-1$).
- The set of **odd** integers is not a ring (not closed under $+$: $1+1=2$ is even; also no $0$).
- $2\mathbb{Z} = \{\dots,-2,0,2,\dots\}$ is a ring **without unity** ($1 \notin 2\mathbb{Z}$). Under our "ring = ring with $1$" convention it is not a ring (it is a non-unital ring, and it is an *ideal* of $\mathbb{Z}$, see below).
- The vector space $\mathbb{R}^3$ with the cross product $\times$ is **not** a ring: the cross product is not associative.

---

**Unit (invertible element) and the group of units $R^\times$.**

(a) *Intuition.* A unit is an element you are allowed to "divide by." In $\mathbb{Z}$, only $\pm 1$ qualify; in $\mathbb{Q}$, everything nonzero does.

(b) *Formal definition.* $u \in R$ is a **unit** if there exists $v \in R$ with $uv = vu = 1$. The set of all units forms a group under multiplication, the **group of units** $R^\times$ (also written $R^*$ or $U(R)$).

(c) *Example.* $\mathbb{Z}^\times = \{1, -1\}$. $\mathbb{Q}^\times = \mathbb{Q}\setminus\{0\}$. In $\mathbb{Z}_5$, $2 \cdot 3 = 6 = 1$, so $2$ is a unit with inverse $3$; in fact $\mathbb{Z}_5^\times = \{1,2,3,4\}$.

---

**Zero divisor.**

(a) *Intuition.* A nonzero element that can multiply another nonzero element to give $0$. This is the "surprise" that breaks ordinary cancellation.

(b) *Formal definition.* A nonzero $a \in R$ is a **zero divisor** if there exists a nonzero $b \in R$ with $ab = 0$ or $ba = 0$.

(c) *Example.* In $\mathbb{Z}_6$, $2 \cdot 3 = 0$, so $2$ and $3$ are zero divisors.

**Units vs. zero divisors (the key contrast).** In any ring, an element cannot be both a unit and a zero divisor. Proof: if $u$ is a unit with inverse $v$, and $ub = 0$, then $b = vub = v\cdot 0 = 0$, so no nonzero $b$ works. Units are the "best behaved" elements; zero divisors are the "worst behaved."

---

**Integral domain.**

(a) *Intuition.* A commutative ring that behaves like $\mathbb{Z}$: no zero divisors, so a product is zero only if a factor is zero, and you can cancel.

(b) *Formal definition.* An **integral domain** is a commutative ring with $1 \neq 0$ that has **no zero divisors**: $ab = 0 \implies a = 0$ or $b = 0$.

(c) *Example.* $\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{R}$, $\mathbb{C}$, and (we will prove) $F[x]$ for any field $F$, and $\mathbb{Z}[i]$. But $\mathbb{Z}_6$ is **not** an integral domain.

---

**Field.**

(a) *Intuition.* A commutative ring where you can divide by anything nonzero: full-blown arithmetic. $\mathbb{Q}$ and $\mathbb{R}$ are the models.

(b) *Formal definition.* A **field** is a commutative ring with $1 \neq 0$ in which **every nonzero element is a unit**. Equivalently, $(F\setminus\{0\}, \cdot)$ is an abelian group.

(c) *Example.* $\mathbb{Q}$, $\mathbb{R}$, $\mathbb{C}$, and $\mathbb{Z}_p$ for $p$ prime.

---

**Characteristic.**

(a) *Intuition.* How many times you must add $1$ to itself to get back to $0$. In $\mathbb{Z}_n$ that is $n$; in $\mathbb{Z}$ you never get there.

(b) *Formal definition.* The **characteristic** $\operatorname{char}(R)$ is the smallest positive integer $n$ with $\underbrace{1 + 1 + \cdots + 1}_{n} = 0$; if no such $n$ exists, $\operatorname{char}(R) = 0$.

(c) *Example.* $\operatorname{char}(\mathbb{Z}) = \operatorname{char}(\mathbb{Q}) = 0$; $\operatorname{char}(\mathbb{Z}_n) = n$. The characteristic of an integral domain is either $0$ or a prime (proved in Advanced Exercise 4).

---

**Subring.**

(a) *Intuition.* A ring living inside a bigger ring, using the same operations, the same $0$, and the same $1$.

(b) *Formal definition.* A subset $S \subseteq R$ is a **subring** if it contains $1$ and is closed under subtraction and multiplication. **Subring test:** $S \subseteq R$ is a subring iff (i) $1 \in S$, (ii) $a - b \in S$ for all $a, b \in S$, and (iii) $ab \in S$ for all $a, b \in S$. (Closure under subtraction makes $S$ an additive subgroup, which gives $0$ and additive inverses for free.)

(c) *Example.* $\mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R} \subset \mathbb{C}$ is a chain of subrings. $\mathbb{Z}[i]$ is a subring of $\mathbb{C}$.

---

**Ideal.**

(a) *Intuition.* An ideal is a "super-absorbing" additive subgroup: multiplying *any* ring element by an ideal element keeps you inside the ideal. Think of $2\mathbb{Z}$ in $\mathbb{Z}$: an even number times *any* integer is still even. Ideals are to rings what **normal subgroups** were to groups: precisely the sub-objects you can quotient by.

(b) *Formal definition.* A subset $I \subseteq R$ is a (two-sided) **ideal** if:
- $I$ is a subgroup of $(R, +)$ (closed under subtraction, contains $0$), and
- **absorption:** for all $r \in R$ and $a \in I$, both $ra \in I$ and $ar \in I$.

In a commutative ring the two absorption conditions coincide. Note: an ideal $I$ contains $1$ **iff** $I = R$ (since then $r = r\cdot 1 \in I$ for all $r$). So a proper ideal is almost never a subring.

(c) *Example.* In $\mathbb{Z}$, the ideals are exactly the sets $n\mathbb{Z}$. In $\mathbb{R}[x]$, the set of all multiples of $x^2+1$ is an ideal.

---

**Principal ideal.**

(a) *Intuition.* The smallest ideal containing one chosen element $a$: all its multiples.

(b) *Formal definition.* In a commutative ring $R$, the **principal ideal generated by $a$** is
$$(a) = aR = \{ra : r \in R\}.$$
More generally $(a_1,\dots,a_k) = \{r_1a_1 + \cdots + r_k a_k : r_i \in R\}$.

(c) *Example.* In $\mathbb{Z}$, $(n) = n\mathbb{Z}$. In $F[x]$, $(p(x))$ is all polynomial multiples of $p(x)$.

**Sum and product of ideals.** For ideals $I, J$: the **sum** $I + J = \{a + b : a \in I, b \in J\}$ is the smallest ideal containing both, and the **product** $IJ = \big\{\sum_{k} a_k b_k : a_k \in I,\ b_k \in J\big\}$ (all *finite* sums) is an ideal contained in $I \cap J$. In $\mathbb{Z}$: $(m) + (n) = (\gcd(m,n))$ and $(m)(n) = (mn)$.

---

**Quotient ring $R/I$.**

(a) *Intuition.* "Set $I$ to zero." You glue together any two elements differing by something in $I$, exactly as $\mathbb{Z}/n\mathbb{Z}$ glues integers differing by a multiple of $n$.

(b) *Formal definition.* For an ideal $I \subseteq R$, the **quotient ring** $R/I$ has elements the cosets $a + I$, with operations
$$(a+I) + (b+I) = (a+b) + I, \qquad (a+I)(b+I) = ab + I.$$
Absorption is exactly what makes multiplication well defined (independent of coset representatives).

(c) *Example.* $\mathbb{Z}/n\mathbb{Z} = \mathbb{Z}_n$. And $\mathbb{R}[x]/(x^2+1) \cong \mathbb{C}$ (Worked Example 3).

---

**Ring homomorphism.**

(a) *Intuition.* A map between rings that respects both operations and the identity: a "structure-preserving translation."

(b) *Formal definition.* A function $\varphi : R \to S$ is a **ring homomorphism** if for all $a, b \in R$:
$$\varphi(a+b) = \varphi(a) + \varphi(b), \quad \varphi(ab) = \varphi(a)\varphi(b), \quad \varphi(1_R) = 1_S.$$
Its **kernel** is $\ker\varphi = \{a \in R : \varphi(a) = 0\}$ and its **image** is $\operatorname{im}\varphi = \{\varphi(a) : a \in R\}$. An **isomorphism** is a bijective homomorphism; we write $R \cong S$.

(c) *Example.* The reduction map $\mathbb{Z} \to \mathbb{Z}_n$, $a \mapsto a \bmod n$, is a homomorphism with kernel $n\mathbb{Z}$. The **evaluation map** $\mathbb{R}[x] \to \mathbb{R}$, $p(x) \mapsto p(2)$, is a homomorphism.

**Two facts we will use:** $\ker\varphi$ is always an **ideal** of $R$, and $\operatorname{im}\varphi$ is always a **subring** of $S$. (Compare groups: kernels there were normal subgroups; here they are ideals, reinforcing "ideals = normal subgroups of ring theory.")

---

**Prime ideal and maximal ideal.**

(a) *Intuition.* A **prime ideal** generalizes "$p$ is prime" via the property "$p \mid ab \implies p\mid a$ or $p\mid b$." A **maximal ideal** is one with no room above it except the whole ring.

(b) *Formal definition* (commutative $R$). A proper ideal $P \neq R$ is **prime** if $ab \in P \implies a \in P$ or $b \in P$. A proper ideal $M \neq R$ is **maximal** if the only ideals containing $M$ are $M$ and $R$.

(c) *Example.* In $\mathbb{Z}$: $(p)$ is prime (and maximal) iff $p$ is prime; $(0)$ is prime but not maximal; $(6)$ is neither. We will see $R/P$ is an integral domain iff $P$ is prime, and $R/M$ is a field iff $M$ is maximal.

---

**PID and UFD.**

(a) *Intuition.* A **PID** (principal ideal domain) is an integral domain where *every* ideal is generated by a single element, the cleanest possible ideal theory. A **UFD** (unique factorization domain) is one where every nonzero non-unit factors into irreducibles uniquely (up to order and units), exactly like the Fundamental Theorem of Arithmetic.

(b) *Formal definition.* A **PID** is an integral domain in which every ideal is principal. A **UFD** is an integral domain in which every nonzero non-unit is a product of irreducible elements, unique up to ordering and multiplication by units.

(c) *Example.* $\mathbb{Z}$ is a PID and a UFD. For any field $F$, $F[x]$ is a PID and a UFD. (Every PID is a UFD; the converse fails, e.g. $\mathbb{Z}[x]$ is a UFD but not a PID since $(2,x)$ is not principal.)

---

## 2. Worked examples

### Worked Example 1: Units and zero divisors in $\mathbb{Z}_{12}$

**Claim.** In $\mathbb{Z}_n$, an element $\overline{a}$ is a unit iff $\gcd(a,n)=1$, and $\overline{a}$ (with $a\not\equiv 0$) is a zero divisor iff $\gcd(a,n)>1$. So every nonzero element of $\mathbb{Z}_n$ is *either* a unit *or* a zero divisor.

**Why.** If $\gcd(a,n)=1$, Bezout gives integers $x,y$ with $ax + ny = 1$, so $ax \equiv 1 \pmod n$, making $\overline{x}$ the inverse of $\overline{a}$. Conversely if $d = \gcd(a,n) > 1$, set $b = n/d$. Then $0 < b < n$ so $\overline{b}\neq 0$, and $ab = a(n/d) = (a/d)n \equiv 0 \pmod n$, so $\overline{a}$ is a zero divisor.

**For $n = 12$.** Compute $\gcd(a,12)$ for $a = 1,\dots,11$:

| $a$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $\gcd(a,12)$ | 1 | 2 | 3 | 4 | 1 | 6 | 1 | 4 | 3 | 2 | 1 |

So the **units** are $\mathbb{Z}_{12}^\times = \{1, 5, 7, 11\}$ (the $a$ with $\gcd=1$), a group of order $\varphi(12)=4$. Check: $5\cdot 5 = 25 = 1$, $7\cdot 7 = 49 = 1$, $11 \cdot 11 = 121 = 1$, so each of these is its own inverse. The **zero divisors** are $\{2,3,4,6,8,9,10\}$. For example $4 \cdot 3 = 12 = 0$ and $8 \cdot 6 = 48 = 0$.

### Worked Example 2: The units of the Gaussian integers $\mathbb{Z}[i]$

**Tool: the norm.** Define $N(a+bi) = a^2 + b^2$. Since $N(z) = z\overline{z}$ where $\overline{z}$ is the complex conjugate, the norm is **multiplicative**: $N(zw) = N(z)N(w)$. For $z \in \mathbb{Z}[i]$, $N(z)$ is a nonnegative integer, and $N(z) = 0$ iff $z = 0$.

**Claim.** $z \in \mathbb{Z}[i]$ is a unit iff $N(z) = 1$, and the units are exactly $\{1, -1, i, -i\}$.

**Proof.** If $zw = 1$ then $N(z)N(w) = N(1) = 1$ with both factors positive integers, forcing $N(z) = 1$. Conversely if $N(z) = z\overline z = 1$ then $\overline z \in \mathbb{Z}[i]$ is a multiplicative inverse, so $z$ is a unit. Now solve $a^2 + b^2 = 1$ in integers: the only solutions are $(\pm 1, 0)$ and $(0, \pm 1)$, giving $z \in \{1, -1, i, -i\}$. As a group, $\mathbb{Z}[i]^\times \cong \mathbb{Z}_4$ (cyclic, generated by $i$, since $i^1=i, i^2=-1, i^3=-i, i^4=1$).

### Worked Example 3: $\mathbb{R}[x]/(x^2+1) \cong \mathbb{C}$

This is the cleanest illustration of "quotient = impose a relation." Setting $x^2 + 1 = 0$ means decreeing $x^2 = -1$, which is exactly how $i$ behaves.

**Setup.** Let $I = (x^2+1) \subseteq \mathbb{R}[x]$, the ideal of all multiples of $x^2+1$. Work in $R = \mathbb{R}[x]/I$, writing $\overline{p} = p + I$. In $R$ we have $\overline{x}^2 = \overline{x^2} = \overline{-1} = -\overline 1$ (because $x^2 - (-1) = x^2 + 1 \in I$). Set $\alpha = \overline{x}$, so $\alpha^2 = -1$.

**Step 1: every element of $R$ is $\overline{a + bx}$ with $a, b \in \mathbb{R}$.** Given any $p(x)$, divide by $x^2 + 1$ (division algorithm in $\mathbb{R}[x]$): $p(x) = q(x)(x^2+1) + r(x)$ with $\deg r < 2$, so $r(x) = a + bx$. Since $q(x)(x^2+1) \in I$, we get $\overline{p} = \overline{r} = \overline a + \overline b\,\alpha$. So $R = \{a + b\alpha : a,b\in\mathbb{R}\}$.

**Step 2: this representation is unique.** If $a + b\alpha = a' + b'\alpha$ in $R$, then $(a - a') + (b - b')x \in I$, i.e. $x^2+1$ divides the degree-$\le 1$ polynomial $(a-a') + (b-b')x$. A nonzero multiple of $x^2+1$ has degree $\ge 2$, so $(a-a') + (b-b')x = 0$, giving $a = a'$ and $b = b'$.

**Step 3: build the isomorphism.** Define $\varphi : \mathbb{C} \to R$ by $\varphi(a + bi) = a + b\alpha$. By Steps 1-2 it is a bijection. It is additive by inspection. For multiplication, using $\alpha^2 = -1 = i^2$:
$$\varphi\big((a+bi)(c+di)\big) = \varphi\big((ac - bd) + (ad+bc)i\big) = (ac-bd) + (ad+bc)\alpha,$$
$$\varphi(a+bi)\,\varphi(c+di) = (a + b\alpha)(c + d\alpha) = ac + (ad + bc)\alpha + bd\,\alpha^2 = (ac - bd) + (ad+bc)\alpha.$$
They agree, and $\varphi(1) = 1$. Hence $\varphi$ is a ring isomorphism and $\mathbb{C} \cong \mathbb{R}[x]/(x^2+1)$. $\qquad\blacksquare$

*Remark.* This also shows $\mathbb{R}[x]/(x^2+1)$ is a **field**, which matches the theory: $x^2+1$ is irreducible over $\mathbb{R}$, so $(x^2+1)$ is maximal, so the quotient is a field (see Section on prime/maximal ideals).

### Worked Example 4: First Isomorphism Theorem via an evaluation map

**First Isomorphism Theorem (rings).** If $\varphi : R \to S$ is a ring homomorphism, then $\ker\varphi$ is an ideal, $\operatorname{im}\varphi$ is a subring, and
$$R/\ker\varphi \;\cong\; \operatorname{im}\varphi.$$

**Application.** Let $\varphi : \mathbb{R}[x] \to \mathbb{C}$ be evaluation at $i$: $\varphi(p(x)) = p(i)$. This is a ring homomorphism (plugging a fixed number into polynomials respects $+$, $\times$, and sends $1 \mapsto 1$).

- **Image.** $\varphi$ is onto $\mathbb{C}$: for $a + bi \in \mathbb{C}$, the polynomial $a + bx$ maps to $a + bi$. So $\operatorname{im}\varphi = \mathbb{C}$.
- **Kernel.** $p(i) = 0$ means $i$ is a root of $p$. Since $p$ has real coefficients, $\overline i = -i$ is also a root, so $(x - i)(x + i) = x^2 + 1$ divides $p$. Conversely every multiple of $x^2+1$ vanishes at $i$. Thus $\ker\varphi = (x^2 + 1)$.

By the theorem, $\mathbb{R}[x]/(x^2+1) \cong \mathbb{C}$, recovering Worked Example 3 in one line. This is the power of the isomorphism theorem: identify a surjection and its kernel, and the quotient is handed to you.

---

## 3. Basic exercises

1. In $\mathbb{Z}_{15}$, list all units and all zero divisors. How many units are there?
2. Is the subset $S = \{a + b\sqrt{2} : a, b \in \mathbb{Z}\} \subseteq \mathbb{R}$ a subring? Use the subring test.
3. Find all units of the ring $\mathbb{Z}_2[x]$. (Hint: think about degrees; what can a product of two polynomials have for degree?)
4. Compute the multiplicative inverse of $\overline 7$ in $\mathbb{Z}_{20}$, or explain why it has none.
5. List the elements of the quotient ring $\mathbb{Z}_2[x]/(x^2 + x + 1)$ and write its full multiplication table. Is it a field?
6. Give the ideal of $\mathbb{Z}$ equal to $(8) + (12)$, and the ideal equal to $(8)(12)$. (Express each as $(n)$.)
7. True or false, with a one-line reason each: (a) $\mathbb{Z}_4$ is an integral domain. (b) Every field is an integral domain. (c) The map $\varphi:\mathbb{Z}\to\mathbb{Z}$, $\varphi(a)=2a$, is a ring homomorphism.

### Solutions

**1.** $a$ is a unit iff $\gcd(a,15)=1$. Units: $\{1,2,4,7,8,11,13,14\}$, which is $\varphi(15)=\varphi(3)\varphi(5)=2\cdot 4 = 8$ units. The nonzero non-units are the zero divisors: $\{3,5,6,9,10,12\}$ (the multiples of $3$ or $5$ in range). Check: $3\cdot 5 = 15 = 0$.

**2.** Yes. (i) $1 = 1 + 0\sqrt2 \in S$. (ii) $(a+b\sqrt2) - (c+d\sqrt2) = (a-c) + (b-d)\sqrt2 \in S$. (iii) $(a+b\sqrt2)(c+d\sqrt2) = (ac + 2bd) + (ad+bc)\sqrt2 \in S$. All three hold, so $S$ is a subring (it is $\mathbb{Z}[\sqrt2]$).

**3.** Only the constants $1$. In $\mathbb{Z}_2[x]$, the leading coefficients are $1$, so $\deg(fg) = \deg f + \deg g$ (no cancellation since $\mathbb{Z}_2$ is a field, hence a domain). If $fg = 1$ then $\deg f + \deg g = 0$, forcing $\deg f = \deg g = 0$, so $f, g$ are nonzero constants; the only nonzero constant in $\mathbb{Z}_2$ is $1$. Thus $\mathbb{Z}_2[x]^\times = \{1\}$. (Same argument: $F[x]^\times = F^\times$ for any field $F$.)

**4.** $\gcd(7,20)=1$, so an inverse exists. Solve $7x \equiv 1 \pmod{20}$: $7\cdot 3 = 21 \equiv 1$. So $\overline 7^{\,-1} = \overline 3$.

**5.** Let $\alpha = \overline x$, so $\alpha^2 = \alpha + 1$ (since $x^2 + x + 1 \equiv 0$ means $x^2 = -x - 1 = x + 1$ in characteristic $2$). Every element reduces to degree $< 2$, giving four elements $\{0, 1, \alpha, \alpha+1\}$. Multiplication (addition is mod $2$ componentwise):
$$\alpha\cdot\alpha = \alpha + 1,\quad \alpha(\alpha+1) = \alpha^2 + \alpha = (\alpha+1)+\alpha = 1,\quad (\alpha+1)(\alpha+1) = \alpha^2 + 1 = \alpha.$$

| $\times$ | $1$ | $\alpha$ | $\alpha+1$ |
|---|---|---|---|
| $1$ | $1$ | $\alpha$ | $\alpha+1$ |
| $\alpha$ | $\alpha$ | $\alpha+1$ | $1$ |
| $\alpha+1$ | $\alpha+1$ | $1$ | $\alpha$ |

Every nonzero element has an inverse ($1^{-1}=1$, $\alpha^{-1} = \alpha+1$, $(\alpha+1)^{-1}=\alpha$), so this is a **field** with $4$ elements, the field $\mathbb{F}_4$. (Consistent with theory: $x^2+x+1$ is irreducible over $\mathbb{Z}_2$, as it has no root there: $0^2+0+1=1$, $1^2+1+1=1$.)

**6.** $(8) + (12) = (\gcd(8,12)) = (4)$. $(8)(12) = (8\cdot 12) = (96)$. (Note $(8)\cap(12) = (\operatorname{lcm}(8,12)) = (24)$, which is bigger than $(96)$ as a set, consistent with $IJ \subseteq I\cap J$.)

**7.** (a) **False:** $2\cdot 2 = 0$ in $\mathbb{Z}_4$, so $2$ is a zero divisor. (b) **True:** in a field, if $ab=0$ and $a\neq 0$, multiply by $a^{-1}$ to get $b=0$; no zero divisors. (c) **False:** $\varphi(1) = 2 \neq 1$ (and $\varphi(1\cdot 1) = 2 \neq 4 = \varphi(1)\varphi(1)$), so it is not a ring homomorphism under our unity convention.

---

## 4. Advanced exercises

1. **(Finite integral domains are fields.)** Prove: every finite integral domain $D$ is a field.
2. **($\mathbb{Z}_n$ field iff $n$ prime.)** Prove that $\mathbb{Z}_n$ is a field iff $n$ is prime, and is an integral domain iff $n$ is prime. (So for $\mathbb{Z}_n$, "field" and "integral domain" coincide.)
3. **(Prime vs. maximal via quotients.)** Let $R$ be a commutative ring and $I$ a proper ideal. Prove: (a) $R/I$ is an integral domain iff $I$ is prime; (b) $R/I$ is a field iff $I$ is maximal. Deduce that every maximal ideal is prime.
4. **(Characteristic of a domain.)** Prove that the characteristic of an integral domain is either $0$ or a prime number.
5. **(Eisenstein and irreducibility.)** Show $f(x) = x^4 + 10x + 5 \in \mathbb{Q}[x]$ is irreducible. Then show $g(x) = x^3 - x - 1$ is irreducible over $\mathbb{Q}$ using the rational root test, and that $\overline g = x^3 + x + 1$ is irreducible over $\mathbb{Z}_2$.

### Solutions

**1.** Let $D = \{0, a_1, \dots, a_n\}$ be a finite integral domain and fix a nonzero $a \in D$. Consider the map $\mu_a : D \to D$, $\mu_a(x) = ax$. It is **injective**: if $ax = ay$ then $a(x - y) = 0$, and since $a \neq 0$ and $D$ has no zero divisors, $x - y = 0$. An injective map from a finite set to itself is **surjective**. So some $b \in D$ has $ab = 1$. Since $D$ is commutative, $b$ is a two-sided inverse, so $a$ is a unit. As $a$ was an arbitrary nonzero element, every nonzero element is a unit: $D$ is a field. $\blacksquare$

**2.** ($\Leftarrow$) If $n = p$ is prime, then for $1 \le a \le p-1$ we have $\gcd(a,p) = 1$, so $a$ is a unit (Worked Example 1); thus $\mathbb{Z}_p$ is a field, hence an integral domain. ($\Rightarrow$) If $n$ is composite, write $n = ab$ with $1 < a, b < n$. Then $\overline a, \overline b \neq 0$ but $\overline a\,\overline b = \overline n = 0$, so $\overline a$ is a zero divisor: $\mathbb{Z}_n$ is **not** an integral domain (hence not a field). Also $n=1$ gives the zero ring, excluded. Combining: $\mathbb{Z}_n$ is a field $\iff$ it is an integral domain $\iff$ $n$ is prime. $\blacksquare$

**3.** Write cosets as $\overline a = a + I$. Recall $\overline a = \overline 0$ in $R/I$ means $a \in I$.

(a) $R/I$ is an integral domain iff: it is nonzero (i.e. $I \neq R$, given) **and** has no zero divisors, i.e. $\overline a\,\overline b = \overline 0 \implies \overline a = \overline 0$ or $\overline b = \overline 0$. Translating: $ab \in I \implies a \in I$ or $b \in I$. That is *exactly* the definition of $I$ prime. $\blacksquare$

(b) ($\Rightarrow$) Suppose $R/I$ is a field and $J$ is an ideal with $I \subsetneq J \subseteq R$. Pick $a \in J \setminus I$, so $\overline a \neq \overline 0$; being in a field it has an inverse $\overline b$, i.e. $ab - 1 \in I \subseteq J$. Since $a \in J$, also $ab \in J$, so $1 = ab - (ab - 1) \in J$, forcing $J = R$. Hence $I$ is maximal.
($\Leftarrow$) Suppose $I$ is maximal and take $\overline a \neq \overline 0$, i.e. $a \notin I$. The ideal $I + (a)$ properly contains $I$, so by maximality $I + (a) = R$. Thus $1 = i + ra$ for some $i \in I$, $r \in R$, giving $\overline r\,\overline a = \overline{ra} = \overline{1 - i} = \overline 1$. So $\overline a$ is invertible, and $R/I$ is a field. $\blacksquare$

(Deduction.) Maximal $\Rightarrow R/I$ field $\Rightarrow R/I$ integral domain $\Rightarrow I$ prime. So **every maximal ideal is prime.** (The converse fails: $(0) \subset \mathbb{Z}$ is prime, since $\mathbb{Z}$ is a domain, but not maximal.)

**4.** Let $D$ be an integral domain with $\operatorname{char}(D) = n > 0$. Suppose $n = ab$ with $1 < a, b < n$. Writing $k\cdot 1$ for $1 + \cdots + 1$ ($k$ times), distributivity gives $(a\cdot 1)(b\cdot 1) = (ab)\cdot 1 = n\cdot 1 = 0$. Since $D$ is a domain, $a\cdot 1 = 0$ or $b\cdot 1 = 0$. But $a, b < n$ and $n$ is the *smallest* positive integer with $n \cdot 1 = 0$, a contradiction. Hence $n$ has no such factorization: $n$ is prime. $\blacksquare$

**5.** *Eisenstein's criterion:* if $f(x) = a_nx^n + \cdots + a_0 \in \mathbb{Z}[x]$ and a prime $p$ satisfies $p \nmid a_n$, $p \mid a_i$ for all $i < n$, and $p^2 \nmid a_0$, then $f$ is irreducible over $\mathbb{Q}$.

For $f(x) = x^4 + 10x + 5$, take $p = 5$: $5 \nmid 1$ (leading), $5 \mid 10$, $5\mid 0$ (coeffs of $x^3, x^2$), $5 \mid 5$, and $5^2 = 25 \nmid 5$. Eisenstein applies, so $f$ is **irreducible over $\mathbb{Q}$**.

*Rational root test:* a rational root $p/q$ (in lowest terms) of an integer polynomial has $p \mid a_0$ and $q \mid a_n$. For $g(x) = x^3 - x - 1$, $a_0 = -1$, $a_n = 1$, so the only candidate roots are $\pm 1$: $g(1) = -1 \neq 0$, $g(-1) = -1 \neq 0$. A **cubic** with no root in $\mathbb{Q}$ cannot factor (any factorization over $\mathbb{Q}$ would include a linear factor, hence a rational root). So $g$ is **irreducible over $\mathbb{Q}$**.

For $\overline g(x) = x^3 + x + 1 \in \mathbb{Z}_2[x]$ (this is $g$ reduced mod $2$): check for roots in $\mathbb{Z}_2$. $\overline g(0) = 1$, $\overline g(1) = 1 + 1 + 1 = 1 \neq 0$. No roots, and it is a cubic, so it is **irreducible over $\mathbb{Z}_2$**. (*Reduction mod $p$:* if a monic integer polynomial stays the same degree and is irreducible mod some prime $p$, it is irreducible over $\mathbb{Q}$; here this confirms $g$ is irreducible over $\mathbb{Q}$ a second way.)

---

## 5. Real-world relevance

Ring theory is the algebraic backbone of much of computing and engineering. A few concrete landing spots, expanded in **doc #5 (Real-World Applications)**:

- **Cryptography.** RSA lives in the ring $\mathbb{Z}_n$ with $n = pq$; security rests on the structure of its unit group $\mathbb{Z}_n^\times$ and Euler's theorem. Modern lattice and elliptic-curve schemes use polynomial quotient rings and finite fields.
- **Error-correcting codes.** CDs, QR codes, deep-space communication, and disk arrays use Reed-Solomon and BCH codes, built from polynomials over finite fields $\mathbb{F}_q = F[x]/(p(x))$ with $p$ irreducible (exactly the construction in Basic Exercise 5).
- **Hashing and arithmetic hardware.** CRC checksums are remainders in $\mathbb{Z}_2[x]$; fast integer/polynomial multiplication uses the ring-theoretic number-theoretic transform.
- **Computer algebra systems** (Sage, Mathematica) represent symbolic computation as exact arithmetic in polynomial rings and their quotients, relying on PID/UFD factorization algorithms.

The unifying idea: model your data as elements of a well-chosen ring, then let the ring's structure (units, ideals, quotients, factorization) do the work.

---

## 6. Common pitfalls & misconceptions

- **"A subring is the same kind of thing as an ideal."** No. A subring must contain $1$; a proper ideal never does. Subrings are closed under multiplication *among themselves*; ideals must *absorb* multiplication by the entire ring. (Compare: a subgroup vs. a normal subgroup.)
- **Confusing zero divisors with units.** They are opposites: a unit can be canceled; a zero divisor cannot. No element is ever both. In $\mathbb{Z}_n$, every nonzero element is exactly one of the two.
- **Assuming you can always cancel or divide.** Cancellation ($ab = ac \Rightarrow b = c$) needs *no zero divisors* (integral domain). Division needs *units* (fields). Neither holds in a general ring; $\mathbb{Z}_6$ breaks both.
- **Forgetting $\varphi(1) = 1$.** Under our convention a ring homomorphism must send $1$ to $1$. The doubling map $a \mapsto 2a$ on $\mathbb{Z}$ fails this and is *not* a ring homomorphism.
- **"$\mathbb{Z}_n$ is always a field."** Only when $n$ is prime. $\mathbb{Z}_4, \mathbb{Z}_6, \mathbb{Z}_{12}$ are not even integral domains.
- **Mixing up the field $\mathbb{Z}_p$ with the field of $p^k$ elements.** $\mathbb{Z}_n$ is a field only for prime $n$; the finite field with $p^k$ elements ($k>1$) is a *quotient* $\mathbb{Z}_p[x]/(p(x))$, not $\mathbb{Z}_{p^k}$ (which has zero divisors).
- **Thinking "irreducible" means "no real roots."** Over $\mathbb{R}$, $(x^2+1)^2$ has no real roots but is reducible. "Irreducible" means "cannot be factored into lower-degree polynomials over the given field." Degrees $2$ and $3$ are special: there, "no root in $F$" *does* imply irreducible.
- **Assuming every ring is commutative.** $M_2(R)$ is the standard counterexample; order of multiplication matters, and it has zero divisors and non-units galore.

---

## 7. What to learn next

You now know that quotients of polynomial rings by *maximal* ideals produce **fields**, and that $F[x]/(p(x))$ with $p$ irreducible is the engine for building new fields. **Doc #4 (Fields & Galois Theory)** runs with this: field extensions, splitting fields, finite fields $\mathbb{F}_{p^k}$, and the stunning Galois correspondence linking field extensions to symmetry groups, tying ring theory back to where the series began.
