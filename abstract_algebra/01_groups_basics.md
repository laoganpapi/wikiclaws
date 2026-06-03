# Group Theory I: The Basics

> A group is the mathematics of symmetry and reversible actions: one set, one well-behaved operation, four simple rules.

## 0. Why this matters (the big picture)

Almost everything that can be "undone" has a group hiding inside it: rotating a square, shuffling a deck, adding clock hours, solving a Rubik's cube. A **group** is the minimal set of rules that captures "combine two actions to get another action, and every action can be reversed." Once you spot that pattern, a single theorem proves facts about integers, symmetries, and matrices all at once. That is the payoff of abstraction: prove it once, use it everywhere.

**Motivating question.** Take a square and label its corners. The rigid motions that leave it looking the same (rotations by $0, 90, 180, 270$ degrees, plus four reflections) can be done one after another. How many such motions are there, what happens when you combine two of them, and is combining them ever order-independent? By the end of this document you will answer all three precisely. (Spoiler: there are $8$, they form the dihedral group $D_4$, and order matters.)

## 1. Key terms, explained simply

Throughout, recall from doc #0: a **binary operation** on a set $G$ is a function $G \times G \to G$ that takes an ordered pair $(a,b)$ and returns one element written $a * b$ (or just $ab$). Also recall $\gcd$, and that $\mathbb{Z}_n = \{0,1,\dots,n-1\}$ with addition done "mod $n$" (wrap around after $n$).

---

**Group**

(a) *Intuition.* Think of the elements as reversible actions and $*$ as "do one action, then the other." You never leave the system, you can do nothing (the identity), and you can always back out (inverses). The order in which you group a chain of actions does not matter (associativity).

(b) *Definition.* A **group** is a pair $(G, *)$ where $G$ is a set and $*$ is a binary operation on $G$ satisfying:

1. **Closure.** For all $a,b \in G$, $a * b \in G$. (Built into "binary operation," but always worth checking.)
2. **Associativity.** For all $a,b,c \in G$, $(a * b) * c = a * (b * c)$.
3. **Identity.** There exists $e \in G$ with $e * a = a * e = a$ for all $a \in G$.
4. **Inverses.** For each $a \in G$ there exists $a^{-1} \in G$ with $a * a^{-1} = a^{-1} * a = e$.

(c) *Example.* $(\mathbb{Z}, +)$: closure (sum of integers is an integer), associativity (ordinary), identity $e = 0$, inverse of $a$ is $-a$. It is a group.

---

**Abelian (commutative) group**

(a) *Intuition.* The order of combining never matters: "socks then shoes" equals "shoes then socks." Most everyday number systems are abelian; most symmetry groups are not.

(b) *Definition.* A group $(G,*)$ is **abelian** if $a * b = b * a$ for all $a,b \in G$. (Named after Niels Henrik Abel.)

(c) *Example.* $(\mathbb{Z},+)$ is abelian since $a + b = b + a$. By contrast, the symmetries of a square are *not* abelian (we will see this in $\S2$).

---

**Order of a group**

(a) *Intuition.* Just the head count: how many elements are in the group.

(b) *Definition.* The **order** of a group $G$, written $|G|$, is the number of elements in $G$. If $G$ is infinite we write $|G| = \infty$.

(c) *Example.* $|\mathbb{Z}_4| = 4$; $|\mathbb{Z}| = \infty$.

---

**Order of an element**

(a) *Intuition.* How many times you must repeat one action before you are back to "do nothing." Rotating a square by $90$ degrees four times returns it to start, so that rotation has order $4$.

(b) *Definition.* For $g \in G$, the **order** of $g$, written $|g|$ or $\operatorname{ord}(g)$, is the smallest positive integer $n$ with $g^n = e$. If no such $n$ exists, $g$ has infinite order. Here $g^n$ means $g * g * \cdots * g$ ($n$ copies), $g^0 = e$, and $g^{-n} = (g^{-1})^n$. In a group written additively (operation $+$), we write $ng$ for "$g$ added to itself $n$ times," and the order is the smallest $n>0$ with $ng = 0$.

(c) *Example.* In $\mathbb{Z}_4$, the element $1$ has order $4$ (since $1,2,3,0$, reaching $0=e$ at the fourth step), while $2$ has order $2$ (since $2+2 = 0$).

---

**Cyclic group**

(a) *Intuition.* A group you can generate by repeatedly applying a single element, like ticking a clock one hour at a time until you have visited every hour.

(b) *Definition.* $G$ is **cyclic** if there is an element $g \in G$ (a **generator**) such that every element of $G$ equals some power $g^k$, $k \in \mathbb{Z}$. We write $G = \langle g \rangle$.

(c) *Example.* $\mathbb{Z}_4 = \langle 1 \rangle$ because $1, 1{+}1{=}2, 1{+}1{+}1{=}3, 1{+}1{+}1{+}1{=}0$ lists every element.

---

**Subgroup**

(a) *Intuition.* A smaller group living inside a bigger one, using the same operation: a self-contained sub-world that is closed and reversible on its own.

(b) *Definition.* A subset $H \subseteq G$ is a **subgroup**, written $H \le G$, if $H$ is itself a group under the operation of $G$. The **trivial subgroup** is $\{e\}$; the **improper subgroup** is $G$ itself. Any other subgroup is **proper and nontrivial**.

(c) *Example.* In $(\mathbb{Z},+)$, the even integers $2\mathbb{Z} = \{\dots,-2,0,2,4,\dots\}$ form a subgroup (closed under $+$, contains $0$, closed under negation).

---

**$U(n)$, the units mod $n$**

(a) *Intuition.* Mod $n$, you can always add, but you cannot always "divide." The numbers you *can* divide by are the ones with a multiplicative inverse; these are exactly the ones coprime to $n$, and they form a group under multiplication.

(b) *Definition.* $U(n) = \{\, a \in \{1,2,\dots,n-1\} : \gcd(a,n) = 1 \,\}$ with operation multiplication mod $n$. (Recall from doc #0: $a$ has an inverse mod $n$ iff $\gcd(a,n)=1$.) Its order $|U(n)|$ is denoted $\varphi(n)$ (Euler's totient).

(c) *Example.* $U(8) = \{1,3,5,7\}$, so $\varphi(8) = 4$. Check: $3 \cdot 3 = 9 \equiv 1$, so $3^{-1} = 3$ mod $8$.

---

**Symmetric group $S_n$**

(a) *Intuition.* All the ways to shuffle (rearrange) $n$ labeled objects. Combining two shuffles gives another shuffle.

(b) *Definition.* A **permutation** of $\{1,2,\dots,n\}$ is a bijection from that set to itself. $S_n$ is the set of all such permutations with operation **composition of functions**. We have $|S_n| = n!$.

(c) *Example.* $S_3$ has $3! = 6$ elements: the identity, three "swaps" of two elements, and two "three-cycles." Detailed in $\S1$'s notation note and $\S2$.

---

**Dihedral group $D_n$**

(a) *Intuition.* All rigid symmetries of a regular $n$-gon: rotations and flips that map the shape onto itself.

(b) *Definition.* $D_n$ is the group of symmetries of a regular $n$-gon: $n$ rotations (by multiples of $360/n$ degrees) and $n$ reflections, with operation "do one symmetry, then the other." So $|D_n| = 2n$.

(c) *Example.* $D_3$ (equilateral triangle) has $6$ elements: $3$ rotations and $3$ reflections.

> **Notation warning.** Some authors write $D_{2n}$ for this same group (emphasizing its order $2n$). We use $D_n$ with $|D_n| = 2n$. Always check an author's convention.

---

**Notation for permutations and our composition convention.** We use **right-to-left** composition, exactly like function composition: $(\sigma\tau)(x) = \sigma(\tau(x))$, meaning **apply $\tau$ first, then $\sigma$.** We will be consistent about this everywhere.

- *Two-line notation:* list inputs on top, outputs below. For $\sigma \in S_3$ sending $1\mapsto 2, 2\mapsto 3, 3 \mapsto 1$:
$$\sigma = \begin{pmatrix} 1 & 2 & 3 \\ 2 & 3 & 1 \end{pmatrix}.$$
- *Cycle notation:* $(a_1\, a_2\, \cdots\, a_k)$ means $a_1 \mapsto a_2 \mapsto \cdots \mapsto a_k \mapsto a_1$ and fixes everything else. The $\sigma$ above is $(1\,2\,3)$. A **transposition** is a $2$-cycle like $(1\,2)$ (swap two, fix the rest). Disjoint cycles (no shared symbols) commute.

## 2. Worked examples

### Example A: Verifying $\mathbb{Z}_n$ is a group, and it is cyclic

Take $(\mathbb{Z}_5, +)$ where addition is mod $5$.

- *Closure:* $a + b \bmod 5 \in \{0,1,2,3,4\}$. Yes.
- *Associativity:* inherited from ordinary integer addition (reducing mod $5$ at the end does not change the result). Yes.
- *Identity:* $0$, since $a + 0 = a$. Yes.
- *Inverses:* the inverse of $a$ is $5 - a$ (and $0$ is its own inverse): e.g. $2 + 3 = 5 \equiv 0$. Yes.

So $\mathbb{Z}_5$ is a group, and it is abelian. It is **cyclic** with generator $1$: the powers (here, multiples) of $1$ are
$$1,\ 1{+}1 = 2,\ 3,\ 4,\ 5 \equiv 0,$$
which lists all of $\mathbb{Z}_5$. In fact $\mathbb{Z}_n = \langle 1 \rangle$ for every $n$, so **every $\mathbb{Z}_n$ is cyclic.**

### Example B: Composing permutations in $S_3$ (order matters)

Let $\sigma = (1\,2\,3)$ and $\tau = (1\,2)$. Compute $\sigma\tau$ and $\tau\sigma$ using our right-to-left convention.

**Compute $\sigma\tau$ (apply $\tau$ first, then $\sigma$).** Track each input:
- $1 \xrightarrow{\tau} 2 \xrightarrow{\sigma} 3$, so $1 \mapsto 3$.
- $2 \xrightarrow{\tau} 1 \xrightarrow{\sigma} 2$, so $2 \mapsto 2$.
- $3 \xrightarrow{\tau} 3 \xrightarrow{\sigma} 1$, so $3 \mapsto 1$.

Result: $1\mapsto 3, 2\mapsto 2, 3\mapsto 1$, which is the transposition $(1\,3)$.

**Compute $\tau\sigma$ (apply $\sigma$ first, then $\tau$).**
- $1 \xrightarrow{\sigma} 2 \xrightarrow{\tau} 1$, so $1 \mapsto 1$.
- $2 \xrightarrow{\sigma} 3 \xrightarrow{\tau} 3$, so $2 \mapsto 3$.
- $3 \xrightarrow{\sigma} 1 \xrightarrow{\tau} 2$, so $3 \mapsto 2$.

Result: $(2\,3)$.

Since $(1\,3) \ne (2\,3)$, we have $\sigma\tau \ne \tau\sigma$: **$S_3$ is non-abelian.** This is the smallest non-abelian group ($|S_3| = 6$).

### Example C: Cayley tables, $\mathbb{Z}_4$ versus the Klein four-group

A **Cayley table** is the full "operation table": the entry in row $a$, column $b$ is $a * b$.

The **Klein four-group** $V$ is $\{e, a, b, c\}$ where every non-identity element is its own inverse and the product of any two distinct non-identity elements is the third. A concrete model is $\mathbb{Z}_2 \times \mathbb{Z}_2$ with componentwise addition mod $2$, taking $e=(0,0), a=(1,0), b=(0,1), c=(1,1)$.

$\mathbb{Z}_4$ (additive, mod $4$):

| $+$ | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **0** | 0 | 1 | 2 | 3 |
| **1** | 1 | 2 | 3 | 0 |
| **2** | 2 | 3 | 0 | 1 |
| **3** | 3 | 0 | 1 | 2 |

Klein four-group $V$:

| $*$ | $e$ | $a$ | $b$ | $c$ |
|---|---|---|---|---|
| **$e$** | $e$ | $a$ | $b$ | $c$ |
| **$a$** | $a$ | $e$ | $c$ | $b$ |
| **$b$** | $b$ | $c$ | $e$ | $a$ |
| **$c$** | $c$ | $b$ | $a$ | $e$ |

**Contrast.** Both have order $4$ and both are abelian (each table is symmetric across its main diagonal). But they are genuinely different groups: $\mathbb{Z}_4$ has an element of order $4$ (namely $1$: it takes four steps to reach $0$), so $\mathbb{Z}_4$ is cyclic. In $V$, every non-identity element has order $2$ (the diagonal is all $e$), so $V$ has **no** element of order $4$ and is **not** cyclic. Same size, different structure. (Notice each row and column of either table is a rearrangement of all the elements with no repeats: this always happens, by the cancellation laws in $\S1$ below.)

### Example D: A non-example, and fixing it

$(\mathbb{Z}, \times)$ is **not** a group. Closure, associativity, and identity ($1$) all hold, but inverses fail: $2$ has no integer $x$ with $2x = 1$. Only $\pm 1$ are invertible.

To get a group we must restrict to invertible elements with a compatible operation. Over the rationals this works: $(\mathbb{Q} \setminus \{0\}, \times)$ is a group (identity $1$, inverse of $p/q$ is $q/p$, and we drop $0$ precisely because it has no inverse). Similarly $(\mathbb{N}, +)$ (with $\mathbb{N} = \{0,1,2,\dots\}$) is not a group: $1$ has no additive inverse inside $\mathbb{N}$, since $-1 \notin \mathbb{N}$.

## 3. Basic exercises

1. Is $(\mathbb{Z}, -)$ (integers under subtraction) a group? Justify.
2. List the elements of $U(10)$ and write its Cayley table. Is it abelian?
3. In $\mathbb{Z}_6$, find the order of each element $0,1,2,3,4,5$.
4. In $S_3$, compute $(1\,2\,3)(1\,2\,3)$ and $(1\,2\,3)(1\,2\,3)(1\,2\,3)$. What is the order of $(1\,2\,3)$?
5. Write the permutation $\begin{pmatrix} 1 & 2 & 3 & 4 \\ 3 & 4 & 2 & 1 \end{pmatrix}$ in cycle notation, and find its order.
6. Which of these are subgroups of $(\mathbb{Z},+)$? (i) $3\mathbb{Z}$ (multiples of $3$); (ii) the odd integers; (iii) $\{0\}$. Justify each.
7. Find all generators of $\mathbb{Z}_6$ (the elements $g$ with $\langle g \rangle = \mathbb{Z}_6$).

### Solutions

**1.** No. Subtraction is not associative: $(5 - 3) - 2 = 0$ but $5 - (3 - 2) = 4$. (There is also no two-sided identity.) Not a group.

**2.** $U(10) = \{1,3,7,9\}$ (the numbers in $1..9$ coprime to $10$), so $\varphi(10)=4$. Multiplication mod $10$:

| $\times$ | 1 | 3 | 7 | 9 |
|---|---|---|---|---|
| **1** | 1 | 3 | 7 | 9 |
| **3** | 3 | 9 | 1 | 7 |
| **7** | 7 | 1 | 9 | 3 |
| **9** | 9 | 7 | 3 | 1 |

It is abelian (table symmetric across the diagonal; also $\times$ mod $10$ is commutative). Note $3 \cdot 7 = 21 \equiv 1$, so $3^{-1} = 7$.

**3.** Order of $g$ is the smallest $n>0$ with $ng \equiv 0 \pmod 6$:
- $0$: order $1$.
- $1$: $1,2,3,4,5,6{\equiv}0$, order $6$.
- $2$: $2,4,6{\equiv}0$, order $3$.
- $3$: $3,6{\equiv}0$, order $2$.
- $4$: $4,8{\equiv}2,12{\equiv}0$, order $3$.
- $5$: $5,10{\equiv}4,15{\equiv}3,20{\equiv}2,25{\equiv}1,30{\equiv}0$, order $6$.

(Notice every order divides $6 = |\mathbb{Z}_6|$, foreshadowing Lagrange.)

**4.** $(1\,2\,3)(1\,2\,3)$: applying $(1\,2\,3)$ twice, $1\mapsto 2\mapsto 3$, $2 \mapsto 3 \mapsto 1$, $3 \mapsto 1 \mapsto 2$, giving $(1\,3\,2)$. Applying a third time returns the identity $e$. So $(1\,2\,3)$ has order $3$.

**5.** Follow the cycle: $1\mapsto 3 \mapsto 2 \mapsto 4 \mapsto 1$, a single $4$-cycle $(1\,3\,2\,4)$. A $k$-cycle has order $k$, so its order is $4$.

**6.** (i) $3\mathbb{Z}$: yes. It contains $0$, is closed under $+$ ($3a + 3b = 3(a{+}b)$), and under negation ($-3a = 3(-a)$). (ii) Odd integers: no. Not closed ($1 + 1 = 2$ is even) and $0$ is missing. (iii) $\{0\}$: yes, the trivial subgroup.

**7.** Generators of $\mathbb{Z}_n$ are exactly the $g$ with $\gcd(g,n) = 1$. For $n = 6$: $\gcd(1,6)=\gcd(5,6)=1$, so the generators are $1$ and $5$. (Consistent with #3: those are the elements of order $6$.)

## 4. Advanced exercises

1. **Uniqueness of inverses.** Prove that in any group, each element $a$ has exactly one inverse. Then prove the **socks-shoes rule** $(ab)^{-1} = b^{-1}a^{-1}$.
2. **Subgroups of cyclic groups are cyclic.** Let $G = \langle g \rangle$ be cyclic and $H \le G$. Prove $H$ is cyclic.
3. **A finite closure shortcut.** Let $H$ be a nonempty *finite* subset of a group $G$ that is closed under the operation (for all $x,y \in H$, $xy \in H$). Prove $H$ is a subgroup. Show by a counterexample that "finite" cannot be dropped.
4. **Order of an element divides $|G|$ (a corollary of Lagrange).** Assuming Lagrange's theorem (the order of a subgroup divides the order of the group), prove that for any $g$ in a finite group $G$, $|g|$ divides $|G|$, and deduce $g^{|G|} = e$.
5. **Even and odd permutations.** Express $\pi = \begin{pmatrix} 1 & 2 & 3 & 4 & 5 \\ 3 & 5 & 4 & 1 & 2 \end{pmatrix}$ in cycle notation, write it as a product of transpositions, and determine its sign (even or odd).

### Solutions

**1.** *Uniqueness.* Suppose $b$ and $c$ are both inverses of $a$, so $ab = ba = e$ and $ac = ca = e$. Then
$$b = b e = b(ac) = (ba)c = e c = c,$$
using associativity. Hence $b = c$: the inverse is unique, and we may write $a^{-1}$.

*Socks-shoes.* We show $b^{-1}a^{-1}$ is the inverse of $ab$ by checking the defining equation (then uniqueness finishes it):
$$(ab)(b^{-1}a^{-1}) = a(bb^{-1})a^{-1} = a e a^{-1} = a a^{-1} = e,$$
and similarly $(b^{-1}a^{-1})(ab) = b^{-1}(a^{-1}a)b = b^{-1}eb = b^{-1}b = e$. By uniqueness of inverses, $(ab)^{-1} = b^{-1}a^{-1}$. (The order reverses: shoes off before socks.)

**2.** If $H = \{e\}$ it is cyclic (generated by $e$). Otherwise $H$ contains some $g^k$ with $k \ne 0$; since $H$ is closed under inverses it contains a *positive* power of $g$ (if $k<0$, use $g^{-k} \in H$). Let $m$ be the **smallest positive integer** with $g^m \in H$. Claim $H = \langle g^m \rangle$. Certainly $\langle g^m \rangle \subseteq H$ (closure). Conversely take any $g^t \in H$. Divide with remainder (doc #0): $t = qm + r$ with $0 \le r < m$. Then
$$g^r = g^{t - qm} = g^t (g^m)^{-q} \in H,$$
since $g^t \in H$ and $g^m \in H$. By minimality of $m$ and $0 \le r < m$, we must have $r = 0$. So $t = qm$ and $g^t = (g^m)^q \in \langle g^m \rangle$. Hence $H = \langle g^m \rangle$ is cyclic. $\blacksquare$

**3.** Let $a \in H$ (nonempty). Consider $a, a^2, a^3, \dots$, all in $H$ by closure. Since $H$ is finite, two powers coincide: $a^i = a^j$ for some $i < j$. Cancelling (multiply by $(a^{-1})^i$ in $G$) gives $a^{j-i} = e$ with $j - i \ge 1$, so $e \in H$. Let $n = j - i$. If $n = 1$ then $a = e$ and $a^{-1} = e \in H$; if $n \ge 2$ then $a \cdot a^{n-1} = a^n = e$, so $a^{-1} = a^{n-1} \in H$ (again by closure). Thus $H$ contains the identity and is closed under inverses and products, so $H \le G$.

*Why "finite" matters.* In $(\mathbb{Z},+)$, the subset $\mathbb{N} = \{0,1,2,\dots\}$ is nonempty and closed under $+$, but it is **not** a subgroup ($1$ has no inverse in $\mathbb{N}$). Closure alone suffices only in the finite case. $\blacksquare$

**4.** Let $g \in G$ and let $n = |g|$. The powers $\{e, g, g^2, \dots, g^{n-1}\}$ are distinct (if two coincided, a smaller positive power would equal $e$, contradicting minimality of $n$) and closed under the operation, so they form a subgroup $\langle g \rangle$ with $|\langle g \rangle| = n$. By Lagrange, $|\langle g \rangle|$ divides $|G|$, i.e. $n \mid |G|$. Writing $|G| = nk$,
$$g^{|G|} = g^{nk} = (g^{n})^{k} = e^{k} = e. \qquad \blacksquare$$
(For $G = U(n)$ this is exactly **Euler's theorem** $a^{\varphi(n)} \equiv 1 \pmod n$; doc #5 uses it for RSA.)

**5.** Trace cycles: $1 \mapsto 3 \mapsto 4 \mapsto 1$ gives $(1\,3\,4)$; the remaining $2 \mapsto 5 \mapsto 2$ gives $(2\,5)$. So
$$\pi = (1\,3\,4)(2\,5).$$
Decompose each cycle into transpositions using $(a_1\,a_2\,\cdots\,a_k) = (a_1\,a_k)\cdots(a_1\,a_3)(a_1\,a_2)$ (a $k$-cycle needs $k-1$ transpositions):
$$(1\,3\,4) = (1\,4)(1\,3), \qquad (2\,5) = (2\,5),$$
so $\pi = (1\,4)(1\,3)(2\,5)$, a product of $3$ transpositions. An odd number of transpositions means $\pi$ is an **odd** permutation, with sign $\operatorname{sgn}(\pi) = (-1)^3 = -1$. (The parity is well defined: a permutation can never be written as both an even and an odd number of transpositions.) $\blacksquare$

## 5. Real-world relevance

- **Symmetry in nature and art.** Crystal structures, molecular shapes, and tilings are classified by their symmetry groups (dihedral, cyclic, and larger). Chemists predict molecular behavior from $D_n$-type symmetry.
- **Clock and calendar arithmetic.** Hours, weekdays, and musical pitch classes are $\mathbb{Z}_n$ under addition.
- **Cryptography.** $U(n)$ and the theorem $g^{|G|} = e$ (Euler/Fermat) underlie RSA encryption and Diffie-Hellman key exchange.
- **Error-correcting codes and puzzles.** Permutation groups ($S_n$) model card shuffles, the $15$-puzzle, and Rubik's cube; parity (even/odd) decides which configurations are reachable.

Doc #5 (Applications) develops the RSA and Rubik's cube connections in full; this section is just the trailer.

## 6. Common pitfalls & misconceptions

- **Forgetting closure.** A subset can satisfy "identity and inverses" yet fail to be a subgroup because two elements multiply to something outside it. Always check closure.
- **Assuming commutativity.** Most groups are non-abelian ($S_3$, $D_n$ for $n \ge 3$, $GL_2$). Never write $ab = ba$ unless you have justified it.
- **Mixing up the two "orders."** $|G|$ counts elements of the group; $|g|$ is the smallest $n$ with $g^n = e$. Different concepts (linked by Lagrange).
- **Composition direction.** $\sigma\tau$ here means "$\tau$ first." Other books apply left-to-right. Pick a convention, state it, and never switch mid-problem.
- **$(ab)^{-1} = a^{-1}b^{-1}$ is wrong in general.** The correct rule reverses order: $(ab)^{-1} = b^{-1}a^{-1}$. (They agree only when $a,b$ commute.)
- **Thinking every group is cyclic.** $\mathbb{Z}_4$ is cyclic, but the same-size Klein four-group is not, and non-abelian groups are never cyclic.
- **"$\mathbb{Z}$ under multiplication is a group."** No: only $\pm 1$ are invertible. Watch which operation you are using.

## 7. What to learn next

Continue with **doc #2, "Group Theory II: Structure & Maps,"** which develops cosets and gives the full proof of Lagrange's theorem, then introduces homomorphisms, isomorphisms (making precise when two groups are "the same," like $\mathbb{Z}_4$ versus $V$), normal subgroups, and quotient groups. That is where the structure you have been computing by hand gets organized into a theory.
