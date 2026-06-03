# Foundations: The Language of Algebra

> Before you can study the rules of a game, you need to agree on the board, the pieces, and how to talk about them.

## 0. Why this matters (the big picture)

Abstract algebra is the study of *structure*: it looks past what objects "are" (numbers, shuffles of a deck, rotations of a square) and focuses on how they *combine*. To do that cleanly, we need a shared vocabulary: sets to hold our objects, functions to move between collections, equivalence relations to declare when two things "count as the same," and operations to combine objects into new ones. This document builds that vocabulary from the ground up, plus the number-theory and proof tools you will use on every page that follows.

**Motivating question.** On a 12-hour clock, $9 + 5 = 2$, not $14$. Is "clock arithmetic" a legitimate number system with its own consistent rules of $+$ and $\times$? If so, what *are* its objects, and what makes the rules work? By the end here you will be able to state this precisely, and it becomes your first real algebraic structure in doc #1.

## 1. Key terms, explained simply

### Sets and their members

**Set.**
- *Intuition:* a box that holds distinct things, with no order and no repeats. A box holding "apple, apple" is just the box holding "apple."
- *Formal:* a set is a well-defined collection of distinct objects. We write $x \in A$ ("$x$ is an element of $A$") when $x$ is in the set $A$, and $x \notin A$ otherwise. Two sets are equal exactly when they have the same elements.
- *Example:* $A = \{1, 2, 3\}$. Here $2 \in A$ but $5 \notin A$. Also $\{1,2,3\} = \{3,1,2\} = \{1,1,2,3\}$, since order and repetition do not matter.

**Element.**
- *Intuition:* a single thing inside the box.
- *Formal:* an object belonging to a set. Elements can themselves be sets: the set $\{\{1\}, 2\}$ has two elements, the set $\{1\}$ and the number $2$.
- *Example:* in $\{a, b, c\}$, the element $b$ is a member; the symbol $d$ is not.

**Empty set.**
- *Intuition:* the empty box.
- *Formal:* the unique set with no elements, written $\varnothing$ or $\{\,\}$. For every object $x$, $x \notin \varnothing$.
- *Example:* $\{n : n \text{ is a whole number and } n < 0 \text{ and } n > 0\} = \varnothing$. Note $\varnothing \neq \{\varnothing\}$: the first is an empty box; the second is a box containing one (empty) box, so it has one element.

**Subset.**
- *Intuition:* box $A$ fits inside box $B$ if everything in $A$ is also in $B$.
- *Formal:* $A \subseteq B$ means: for every $x$, if $x \in A$ then $x \in B$. If $A \subseteq B$ and $A \neq B$ we call $A$ a *proper* subset, written $A \subsetneq B$. The empty set is a subset of every set, and every set is a subset of itself.
- *Example:* $\{1, 2\} \subseteq \{1, 2, 3\}$, and in fact $\{1,2\} \subsetneq \{1,2,3\}$. Also $\varnothing \subseteq \{1,2,3\}$.

**Set-builder notation.**
- *Intuition:* describe a box by a rule its members satisfy, instead of listing them.
- *Formal:* $\{\, x : P(x) \,\}$ (read "the set of all $x$ such that $P(x)$ is true") collects exactly the objects making property $P$ true. The colon `:` is read "such that" (some books use a vertical bar `|`). We often restrict the universe first: $\{\, x \in \mathbb{Z} : P(x)\,\}$ means "$x$ ranges over integers."
- *Example:* $\{\, n \in \mathbb{Z} : n = 2k \text{ for some } k \in \mathbb{Z} \,\}$ is the set of even integers, $\{\dots, -2, 0, 2, 4, \dots\}$.

**Standard number sets (notation we use throughout).**
- $\mathbb{N} = \{0, 1, 2, 3, \dots\}$, the natural numbers (we include $0$; some authors start at $1$, so always check a book's convention).
- $\mathbb{Z} = \{\dots, -2, -1, 0, 1, 2, \dots\}$, the integers (from German *Zahlen*, "numbers").
- $\mathbb{Q}$, the rational numbers (fractions $a/b$ with $a, b \in \mathbb{Z}$ and $b \neq 0$).
- $\mathbb{R}$, the real numbers; $\mathbb{C}$, the complex numbers.

**Union, intersection, complement, difference.**
- *Intuition:* combine boxes (union), keep only shared items (intersection), or keep what is left out (complement).
- *Formal:* for sets $A, B$ inside a universe $U$,
  - union $A \cup B = \{\, x : x \in A \text{ or } x \in B \,\}$ (inclusive "or"),
  - intersection $A \cap B = \{\, x : x \in A \text{ and } x \in B \,\}$,
  - difference $A \setminus B = \{\, x : x \in A \text{ and } x \notin B \,\}$,
  - complement $A^{c} = U \setminus A = \{\, x \in U : x \notin A \,\}$ (depends on the chosen universe $U$).
  - Two sets are *disjoint* when $A \cap B = \varnothing$.
- *Example:* with $U = \{1,2,3,4,5\}$, $A = \{1,2,3\}$, $B = \{3,4\}$: $A \cup B = \{1,2,3,4\}$, $A \cap B = \{3\}$, $A \setminus B = \{1,2\}$, $A^{c} = \{4,5\}$.

**Cartesian product.**
- *Intuition:* all ways to pick one item from box $A$ and then one from box $B$, kept as *ordered* pairs (order matters, unlike inside a set).
- *Formal:* $A \times B = \{\, (a, b) : a \in A \text{ and } b \in B \,\}$. Here $(a,b) = (a', b')$ exactly when $a = a'$ and $b = b'$.
- *Example:* $\{1,2\} \times \{x, y\} = \{(1,x), (1,y), (2,x), (2,y)\}$. The plane $\mathbb{R}^2 = \mathbb{R} \times \mathbb{R}$ is the most familiar Cartesian product: points $(x,y)$.

**Cardinality.**
- *Intuition:* how many elements a set has.
- *Formal:* for a finite set $A$, $|A|$ is the number of its elements. For finite $A, B$ one has $|A \times B| = |A|\cdot|B|$, and $|A \cup B| = |A| + |B| - |A \cap B|$ (inclusion-exclusion). Infinite sets also have cardinalities, but we will only need finite counting here.
- *Example:* $|\{a,b,c\}| = 3$, $|\varnothing| = 0$, and $|\{1,2\} \times \{x,y\}| = 2\cdot 2 = 4$.

### Functions

**Function.**
- *Intuition:* a machine that takes an input and returns exactly one output. Same input, same output, every time.
- *Formal:* a function $f : A \to B$ assigns to each element $a \in A$ exactly one element $f(a) \in B$. The set $A$ is the **domain** (allowed inputs), $B$ is the **codomain** (the declared "type" of outputs).
- *Example:* $f : \mathbb{Z} \to \mathbb{Z}$, $f(n) = n^2$. Then $f(-3) = 9$. Every integer input has one integer output.

**Image (range).**
- *Intuition:* the outputs that actually get hit, which may be smaller than the whole codomain.
- *Formal:* the image of $f : A \to B$ is $\operatorname{im}(f) = \{\, f(a) : a \in A \,\} \subseteq B$. (Some books call this the range.)
- *Example:* for $f(n) = n^2$ with codomain $\mathbb{Z}$, the image is $\{0, 1, 4, 9, \dots\}$, the perfect squares. The codomain is all of $\mathbb{Z}$, but the image is a proper subset.

**Injective (one-to-one).**
- *Intuition:* different inputs never collide on the same output; no two arrows land on the same target.
- *Formal:* $f$ is injective if whenever $f(a_1) = f(a_2)$, then $a_1 = a_2$. (Equivalently, by contrapositive: $a_1 \neq a_2 \Rightarrow f(a_1) \neq f(a_2)$.)
- *Example:* $f : \mathbb{R} \to \mathbb{R}$, $f(x) = 2x + 1$ is injective: if $2a_1 + 1 = 2a_2 + 1$ then $a_1 = a_2$. But $g(x) = x^2$ on $\mathbb{R}$ is *not* injective, since $g(-2) = g(2) = 4$.

**Surjective (onto).**
- *Intuition:* every target in the codomain gets hit by at least one arrow; nothing is missed.
- *Formal:* $f : A \to B$ is surjective if for every $b \in B$ there exists some $a \in A$ with $f(a) = b$. Equivalently, $\operatorname{im}(f) = B$.
- *Example:* $f : \mathbb{R} \to \mathbb{R}$, $f(x) = 2x + 1$ is surjective: given any $b$, set $x = (b-1)/2$ to get $f(x)=b$. But $f : \mathbb{Z} \to \mathbb{Z}$, $f(n) = 2n$ is *not* surjective: nothing maps to $3$.

**Bijective.**
- *Intuition:* a perfect pairing, every input matched to a unique output and vice versa. It is exactly a *relabeling* of one set as another.
- *Formal:* $f$ is bijective if it is both injective and surjective. Then each $b \in B$ has exactly one $a \in A$ with $f(a) = b$.
- *Example:* $f : \mathbb{R} \to \mathbb{R}$, $f(x) = 2x + 1$ is bijective. So is the identity $\mathrm{id}_A : A \to A$, $\mathrm{id}_A(a) = a$.

**Composition.**
- *Intuition:* run one machine, then feed its output into the next.
- *Formal:* given $f : A \to B$ and $g : B \to C$, the composite $g \circ f : A \to C$ is defined by $(g \circ f)(a) = g(f(a))$. Read $g \circ f$ as "$g$ after $f$"; the right-hand function runs first. Composition is associative: $h \circ (g \circ f) = (h \circ g) \circ f$.
- *Example:* $f(x) = x + 1$, $g(x) = x^2$. Then $(g \circ f)(x) = (x+1)^2$, while $(f \circ g)(x) = x^2 + 1$. These differ, so composition is generally *not* commutative.

**Inverse function.**
- *Intuition:* a machine that undoes another, sending each output back to the input it came from.
- *Formal:* $g : B \to A$ is the inverse of $f : A \to B$ if $g \circ f = \mathrm{id}_A$ and $f \circ g = \mathrm{id}_B$. An inverse exists **if and only if** $f$ is bijective, and when it exists it is unique, written $f^{-1}$.
- *Example:* for $f(x) = 2x + 1$, solve $y = 2x+1$ for $x$ to get $f^{-1}(y) = (y - 1)/2$. Check: $f^{-1}(f(x)) = (2x+1-1)/2 = x$.

**Why bijections matter (relabeling).** A bijection $f : A \to B$ says "$A$ and $B$ are the same set wearing different name tags." Anything you can do structurally in $A$ you can mirror in $B$ by translating names through $f$. This idea, that two systems are "the same up to renaming," is the seed of *isomorphism*, the central theme of doc #2.

### Relations and equivalence

**Relation.**
- *Intuition:* a rule that, for each ordered pair of elements, says "related" or "not related."
- *Formal:* a (binary) relation on a set $A$ is a subset $R \subseteq A \times A$. We write $a \sim b$ to mean $(a, b) \in R$ ("$a$ is related to $b$").
- *Example:* on $\mathbb{Z}$, define $a \sim b$ iff $a \le b$. Then $2 \sim 5$ but not $5 \sim 2$.

**Equivalence relation.**
- *Intuition:* a relation that behaves like "is the same as" for some chosen notion of sameness. It groups elements that should be treated as interchangeable.
- *Formal:* a relation $\sim$ on $A$ is an equivalence relation if for all $a, b, c \in A$:
  1. **Reflexive:** $a \sim a$.
  2. **Symmetric:** if $a \sim b$ then $b \sim a$.
  3. **Transitive:** if $a \sim b$ and $b \sim c$ then $a \sim c$.
- *Example:* "has the same remainder when divided by $3$" is an equivalence relation on $\mathbb{Z}$ (we verify a version of this in Section 2).

**Equivalence class.**
- *Intuition:* the bin holding everything equivalent to a chosen representative.
- *Formal:* for $a \in A$, its equivalence class is $[a] = \{\, x \in A : x \sim a \,\}$. Every element lies in its own class (by reflexivity), and a key fact is: $[a] = [b]$ if and only if $a \sim b$; otherwise $[a] \cap [b] = \varnothing$ (proved in Section 4).
- *Example:* under "same remainder mod $3$," $[0] = \{\dots, -3, 0, 3, 6, \dots\}$ and $[1] = \{\dots, -2, 1, 4, 7, \dots\}$.

**Partition.**
- *Intuition:* a way to slice a set into non-overlapping, non-empty pieces that together cover everything, like cutting a pizza.
- *Formal:* a partition of $A$ is a collection $\mathcal{P}$ of non-empty subsets of $A$ such that (i) every element of $A$ lies in exactly one member of $\mathcal{P}$. Equivalently: the pieces are pairwise disjoint and their union is $A$.
- *Example:* $\{\, \{1,2\}, \{3\}, \{4,5\} \,\}$ is a partition of $\{1,2,3,4,5\}$.

**The link (fundamental).** Equivalence relations and partitions are two views of the same thing. Every equivalence relation on $A$ produces a partition of $A$ into its equivalence classes; conversely, every partition of $A$ defines an equivalence relation ("$a \sim b$ iff $a$ and $b$ lie in the same piece"). This correspondence is exact and underlies quotient constructions throughout algebra (cosets, quotient groups, quotient rings).

### Modular arithmetic

**Divisibility.**
- *Intuition:* $d$ divides $n$ if $n$ is a whole number of $d$'s, with nothing left over.
- *Formal:* for integers $d, n$, we say $d \mid n$ ("$d$ divides $n$") if there is an integer $k$ with $n = dk$. If no such $k$ exists we write $d \nmid n$.
- *Example:* $3 \mid 12$ (since $12 = 3 \cdot 4$), but $3 \nmid 7$. Note $d \mid 0$ for every $d$ (take $k = 0$), and $1 \mid n$ for every $n$.

**Congruence mod $n$.**
- *Intuition:* two integers are "the same on an $n$-hour clock" if they differ by a whole number of full laps.
- *Formal:* fix an integer $n \ge 1$ (the modulus). For integers $a, b$, we write $a \equiv b \pmod{n}$ ("$a$ is congruent to $b$ mod $n$") if $n \mid (a - b)$. Equivalently, $a$ and $b$ leave the same remainder when divided by $n$.
- *Example:* $17 \equiv 5 \pmod{12}$, because $17 - 5 = 12$ and $12 \mid 12$. On a clock, $17{:}00$ shows as $5$.

**The set $\mathbb{Z}_n$.**
- *Intuition:* the $n$ "clock positions," one bin per possible remainder.
- *Formal:* congruence mod $n$ is an equivalence relation on $\mathbb{Z}$, and it has exactly $n$ classes, one for each remainder. We name them by their smallest non-negative representatives: $\mathbb{Z}_n = \{0, 1, 2, \dots, n-1\}$, where each symbol $k$ stands for the class $[k] = \{\, x \in \mathbb{Z} : x \equiv k \pmod n \,\}$.
- *Example:* $\mathbb{Z}_4 = \{0, 1, 2, 3\}$. The label $2$ secretly means $\{\dots, -2, 2, 6, 10, \dots\}$.

**Addition and multiplication mod $n$.**
- *Intuition:* add or multiply as usual, then wrap around the clock by taking the remainder.
- *Formal:* define $a +_n b = (a + b) \bmod n$ and $a \cdot_n b = (a \cdot b) \bmod n$, where $x \bmod n$ denotes the remainder of $x$ on division by $n$ (an element of $\{0, \dots, n-1\}$). These are *well-defined*: replacing $a$ or $b$ by any congruent integer gives the same class as result (justified in Section 4). We usually drop the subscript when $n$ is clear.
- *Example:* in $\mathbb{Z}_{12}$, $9 + 5 = 14 \equiv 2$, and $7 \cdot 4 = 28 \equiv 4 \pmod{12}$. This answers the opening clock question: yes, it is a consistent system, and you build its full algebraic structure in docs #1 and #3.

### Binary operations and algebraic structures

**Binary operation.**
- *Intuition:* a rule that eats two elements of a set and spits out one element of the *same* set.
- *Formal:* a binary operation on a set $S$ is a function $* : S \times S \to S$. We write $a * b$ for the output. The phrase "on $S$, landing back in $S$" is built into the definition; that requirement is called closure.
- *Example:* ordinary addition $+ : \mathbb{Z} \times \mathbb{Z} \to \mathbb{Z}$ is a binary operation. So is $\max(a,b)$ on $\mathbb{N}$.

Properties an operation $*$ on $S$ may or may not have:

**Closure.**
- *Formal:* for all $a, b \in S$, $a * b \in S$. (This is exactly what makes $*$ a genuine operation *on* $S$.)
- *Example:* addition is closed on the even integers ($\text{even} + \text{even} = \text{even}$). It is **not** closed on the odd integers ($3 + 5 = 8$ is even), so "$+$ on the odds" fails to be a binary operation.

**Associativity.**
- *Formal:* for all $a, b, c \in S$, $(a * b) * c = a * (b * c)$. This lets us drop parentheses and write $a * b * c$ unambiguously.
- *Example:* addition and multiplication are associative. **Non-example:** subtraction on $\mathbb{Z}$ is not: $(8 - 3) - 2 = 3$ but $8 - (3 - 2) = 7$.

**Commutativity.**
- *Formal:* for all $a, b \in S$, $a * b = b * a$ (order does not matter).
- *Example:* addition is commutative. **Non-example:** subtraction is not: $8 - 3 = 5$ but $3 - 8 = -5$. Composition of functions is also generally non-commutative (Section 1, composition example).

**Identity element.**
- *Intuition:* a "do-nothing" element that leaves every input unchanged.
- *Formal:* an element $e \in S$ is an identity for $*$ if $a * e = a = e * a$ for all $a \in S$. If an identity exists, it is unique.
- *Example:* $0$ is the identity for $+$ on $\mathbb{Z}$ ($a + 0 = a$); $1$ is the identity for $\times$ ($a \cdot 1 = a$). Subtraction has a right identity ($a - 0 = a$) but no two-sided identity, since $0 - a = -a \neq a$ in general.

**Inverses.**
- *Intuition:* for each element, a partner that combines with it to give the do-nothing element.
- *Formal:* assuming an identity $e$ exists, an element $b$ is an inverse of $a$ if $a * b = e = b * a$. 
- *Example:* under $+$ on $\mathbb{Z}$, the inverse of $5$ is $-5$ (since $5 + (-5) = 0$). Under $\times$ on $\mathbb{Z}$, only $1$ and $-1$ have inverses; $2$ has no integer multiplicative inverse (you would need $1/2 \notin \mathbb{Z}$).

**Algebraic structure (informal).** An algebraic structure is a set together with one or more binary operations on it, plus a chosen list of axioms (rules) those operations must satisfy. For example, "a set with one associative operation that has an identity and in which every element has an inverse" is exactly a *group*, the subject of doc #1. Rings (doc #3) add a second operation. Keeping the set, the operation, and the axioms straight is the whole game; this section is the bridge to all of it.

### Number-theory toolkit

**Division algorithm.**
- *Intuition:* dividing with a remainder always works, uniquely.
- *Formal:* for any integer $a$ and any integer $n > 0$, there exist unique integers $q$ (quotient) and $r$ (remainder) with $a = nq + r$ and $0 \le r < n$.
- *Example:* $a = 17$, $n = 5$: $17 = 5 \cdot 3 + 2$, so $q = 3$, $r = 2$. For negatives, $a = -17$, $n = 5$: $-17 = 5 \cdot (-4) + 3$, so $q = -4$, $r = 3$ (remainder must be non-negative).

**Greatest common divisor (gcd).**
- *Intuition:* the largest number that divides both.
- *Formal:* for integers $a, b$ not both zero, $\gcd(a,b)$ is the largest integer $d$ with $d \mid a$ and $d \mid b$. If $\gcd(a,b) = 1$ we call $a, b$ *coprime* (relatively prime).
- *Example:* $\gcd(12, 18) = 6$. $\gcd(8, 15) = 1$, so $8$ and $15$ are coprime.

**Euclidean algorithm.**
- *Intuition:* replace the bigger number by its remainder against the smaller, repeat, and the last nonzero remainder is the gcd. It works because any common divisor of $a$ and $b$ is also a common divisor of $b$ and $a \bmod b$.
- *Formal:* the rule $\gcd(a, b) = \gcd(b,\, a \bmod b)$, with $\gcd(a, 0) = |a|$, terminates and returns the gcd. (Worked fully in Section 2.)
- *Example:* $\gcd(48, 18)$: $48 = 2\cdot 18 + 12$, then $\gcd(18, 12)$; $18 = 1\cdot 12 + 6$, then $\gcd(12, 6)$; $12 = 2 \cdot 6 + 0$, so $\gcd = 6$.

**Bezout's identity.**
- *Intuition:* the gcd can always be reached as an integer combination of the two numbers.
- *Formal:* for integers $a, b$ not both zero, there exist integers $x, y$ with $ax + by = \gcd(a,b)$. (The $x, y$ are not unique.) You find them by running the Euclidean algorithm backward (Section 2).
- *Example:* $\gcd(48, 18) = 6$, and indeed $48 \cdot (-1) + 18 \cdot 3 = -48 + 54 = 6$.

**Prime number.**
- *Intuition:* an "atom" of multiplication, with no factors besides $1$ and itself.
- *Formal:* an integer $p > 1$ is prime if its only positive divisors are $1$ and $p$. An integer $> 1$ that is not prime is *composite*. (By convention $1$ is neither.)
- *Example:* $2, 3, 5, 7, 11$ are prime; $6 = 2 \cdot 3$ is composite.

**Fundamental Theorem of Arithmetic.**
- *Intuition:* every whole number bigger than $1$ has one and only one prime "recipe."
- *Formal:* every integer $n > 1$ can be written as a product of primes, and this factorization is unique up to the order of the factors.
- *Example:* $360 = 2^3 \cdot 3^2 \cdot 5$, and no other multiset of primes multiplies to $360$.

### Proof techniques

**Direct proof.**
- *Idea:* assume the hypothesis, march straight to the conclusion using definitions and known facts.
- *Tiny example:* *If $n$ is even, then $n^2$ is even.* Proof: $n = 2k$ for some $k \in \mathbb{Z}$, so $n^2 = 4k^2 = 2(2k^2)$, which is even. $\blacksquare$

**Proof by contrapositive.**
- *Idea:* to prove "if $P$ then $Q$," instead prove the logically equivalent "if not $Q$ then not $P$."
- *Tiny example:* *If $n^2$ is even, then $n$ is even.* Contrapositive: if $n$ is odd then $n^2$ is odd. Proof: $n = 2k+1 \Rightarrow n^2 = 4k^2 + 4k + 1 = 2(2k^2 + 2k) + 1$, odd. $\blacksquare$

**Proof by contradiction.**
- *Idea:* assume the statement is false, derive an impossibility, conclude it must be true.
- *Tiny example:* *$\sqrt{2}$ is irrational.* Suppose instead $\sqrt 2 = a/b$ in lowest terms. Then $2b^2 = a^2$, so $a^2$ is even, so $a$ is even (previous result), say $a = 2c$; then $2b^2 = 4c^2$, so $b^2 = 2c^2$ is even, so $b$ is even. But then $a, b$ share factor $2$, contradicting "lowest terms." $\blacksquare$

**Mathematical induction.**
- *Idea:* prove a statement $P(n)$ for all $n \ge n_0$ by (base case) proving $P(n_0)$, then (inductive step) proving "if $P(k)$ then $P(k+1)$." Like dominoes: knock the first, and show each topples the next.
- *Tiny example:* *$1 + 2 + \dots + n = \frac{n(n+1)}{2}$ for all $n \ge 1$.* Base: $n=1$ gives $1 = \frac{1\cdot 2}{2}$. Step: assume $1 + \dots + k = \frac{k(k+1)}{2}$; then $1 + \dots + k + (k+1) = \frac{k(k+1)}{2} + (k+1) = \frac{(k+1)(k+2)}{2}$. $\blacksquare$

**Well-ordering principle.**
- *Idea:* every non-empty set of non-negative integers has a smallest element. This is the engine behind induction and the division algorithm.
- *Tiny example:* there is no integer strictly between $0$ and $1$. If the set $S = \{\, n \in \mathbb{Z} : 0 < n < 1 \,\}$ were non-empty, it would have a least element $m$ with $0 < m < 1$; but then $0 < m^2 < m < 1$, giving a smaller element of $S$, a contradiction. So $S = \varnothing$. $\blacksquare$

## 2. Worked examples

### Example A: Verifying an equivalence relation and finding its classes

Define a relation on $\mathbb{Z}$ by $a \sim b$ iff $a \equiv b \pmod 3$ (that is, $3 \mid (a-b)$). Show it is an equivalence relation and list its classes.

- **Reflexive:** $a - a = 0$ and $3 \mid 0$, so $a \sim a$. 
- **Symmetric:** if $3 \mid (a-b)$, write $a - b = 3k$; then $b - a = 3(-k)$, so $3 \mid (b - a)$, giving $b \sim a$.
- **Transitive:** if $3 \mid (a-b)$ and $3 \mid (b-c)$, write $a - b = 3k$ and $b - c = 3m$; adding, $a - c = 3(k + m)$, so $3 \mid (a-c)$, giving $a \sim c$.

All three hold, so $\sim$ is an equivalence relation. By the division algorithm every integer leaves remainder $0$, $1$, or $2$ on division by $3$, so there are exactly three classes:
$$[0] = \{\dots,-3,0,3,6,\dots\}, \quad [1] = \{\dots,-2,1,4,7,\dots\}, \quad [2] = \{\dots,-1,2,5,8,\dots\}.$$
These three classes are disjoint and their union is $\mathbb{Z}$, so they form a partition. This set of classes is exactly $\mathbb{Z}_3$.

### Example B: Modular arithmetic tables for $\mathbb{Z}_5$

Build the addition and multiplication tables for $\mathbb{Z}_5 = \{0,1,2,3,4\}$. Each entry is the ordinary result reduced mod $5$ (take the remainder).

Addition mod $5$ (entry in row $a$, column $b$ is $a + b \bmod 5$):

| $+$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| **0** | 0 | 1 | 2 | 3 | 4 |
| **1** | 1 | 2 | 3 | 4 | 0 |
| **2** | 2 | 3 | 4 | 0 | 1 |
| **3** | 3 | 4 | 0 | 1 | 2 |
| **4** | 4 | 0 | 1 | 2 | 3 |

For instance $3 + 4 = 7 = 5 + 2 \equiv 2$. Notice every row and column contains each element exactly once, and $0$ is the identity.

Multiplication mod $5$ (entry is $a \cdot b \bmod 5$):

| $\times$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| **0** | 0 | 0 | 0 | 0 | 0 |
| **1** | 0 | 1 | 2 | 3 | 4 |
| **2** | 0 | 2 | 4 | 1 | 3 |
| **3** | 0 | 3 | 1 | 4 | 2 |
| **4** | 0 | 4 | 3 | 2 | 1 |

For instance $3 \cdot 4 = 12 = 10 + 2 \equiv 2$. Here $1$ is the identity, and ignoring $0$, every nonzero element has an inverse: $2 \cdot 3 = 6 \equiv 1$ and $4 \cdot 4 = 16 \equiv 1$. (That this works so cleanly is because $5$ is prime; the deeper reason is the content of docs #1 and #3.)

### Example C: Euclidean algorithm and Bezout's identity

Compute $\gcd(252, 198)$ and find integers $x, y$ with $252x + 198y = \gcd(252,198)$.

Forward pass (division algorithm repeatedly; each remainder becomes the next divisor):
$$252 = 1 \cdot 198 + 54$$
$$198 = 3 \cdot 54 + 36$$
$$54 = 1 \cdot 36 + 18$$
$$36 = 2 \cdot 18 + 0$$
The last nonzero remainder is $18$, so $\gcd(252, 198) = 18$.

Back-substitution (solve each line for its remainder, then substitute upward):
$$18 = 54 - 1 \cdot 36.$$
From the second line, $36 = 198 - 3 \cdot 54$, so
$$18 = 54 - (198 - 3\cdot 54) = 4 \cdot 54 - 1 \cdot 198.$$
From the first line, $54 = 252 - 1 \cdot 198$, so
$$18 = 4(252 - 198) - 198 = 4 \cdot 252 - 5 \cdot 198.$$
Thus $x = 4$, $y = -5$. Check: $4 \cdot 252 - 5 \cdot 198 = 1008 - 990 = 18$. Correct.

### Example D: Counting with Cartesian products and a bijection

Let $A = \{1, 2, 3\}$ and $B = \{a, b\}$.

1. *Cardinality of the product.* $|A \times B| = |A| \cdot |B| = 3 \cdot 2 = 6$. Explicitly,
$$A \times B = \{(1,a),(1,b),(2,a),(2,b),(3,a),(3,b)\}.$$
2. *A bijection between two relabelings.* Define $f : \{1,2,3\} \to \{a,b,c\}$ by $f(1) = a$, $f(2) = b$, $f(3) = c$. It is injective (distinct inputs give distinct outputs) and surjective (every one of $a,b,c$ is hit), hence bijective. Its inverse is $f^{-1}(a) = 1$, $f^{-1}(b) = 2$, $f^{-1}(c) = 3$. This $f$ literally renames the numbers as letters, the relabeling idea in action.

## 3. Basic exercises

1. List all subsets of $\{1, 2\}$. How many are there? (Include $\varnothing$ and the whole set.)
2. With $U = \{1,2,3,4,5,6\}$, $A = \{1,2,3,4\}$, $B = \{3,4,5\}$, compute $A \cup B$, $A \cap B$, $A \setminus B$, $B \setminus A$, and $A^{c}$.
3. Compute $17 \bmod 5$, $(-1) \bmod 5$, and $23 \bmod 7$ (give the remainder in the correct range $0 \le r < n$).
4. In $\mathbb{Z}_6$, compute $4 + 5$, $5 + 5$, $4 \cdot 5$, and $3 \cdot 4$ (reduce mod $6$).
5. Is $f : \mathbb{Z} \to \mathbb{Z}$, $f(n) = n + 3$ injective? Surjective? Bijective? If it has an inverse, write it down.
6. Use the Euclidean algorithm to compute $\gcd(56, 35)$, showing each division step.
7. Decide whether the operation $a * b = a - b$ on $\mathbb{Z}$ is (a) closed, (b) commutative, (c) associative. Justify each with a reason or a counterexample.
8. Write the prime factorization of $84$.

### Solutions

**1.** The subsets are $\varnothing$, $\{1\}$, $\{2\}$, $\{1,2\}$. That is $4 = 2^2$ subsets. (In general a set with $n$ elements has $2^n$ subsets, since each element is independently in or out.)

**2.** 
$A \cup B = \{1,2,3,4,5\}$. 
$A \cap B = \{3,4\}$. 
$A \setminus B = \{1,2\}$ (in $A$, not in $B$). 
$B \setminus A = \{5\}$. 
$A^{c} = U \setminus A = \{5,6\}$.

**3.** $17 = 5\cdot 3 + 2$, so $17 \bmod 5 = 2$. For $-1$: $-1 = 5\cdot(-1) + 4$, so $(-1)\bmod 5 = 4$ (not $-1$; the remainder must be in $\{0,\dots,4\}$). $23 = 7\cdot 3 + 2$, so $23 \bmod 7 = 2$.

**4.** In $\mathbb{Z}_6$: $4 + 5 = 9 \equiv 3$. $5 + 5 = 10 \equiv 4$. $4 \cdot 5 = 20 = 18 + 2 \equiv 2$. $3 \cdot 4 = 12 \equiv 0$. (Note $3 \cdot 4 = 0$ with neither factor zero, a phenomenon impossible in $\mathbb{Z}_5$; this "zero divisor" idea returns in doc #3.)

**5.** Injective: if $n_1 + 3 = n_2 + 3$ then $n_1 = n_2$, yes. Surjective: given any $m \in \mathbb{Z}$, $n = m - 3$ gives $f(n) = m$, yes. So $f$ is bijective, with inverse $f^{-1}(m) = m - 3$.

**6.** $56 = 1 \cdot 35 + 21$; $35 = 1 \cdot 21 + 14$; $21 = 1 \cdot 14 + 7$; $14 = 2 \cdot 7 + 0$. Last nonzero remainder is $7$, so $\gcd(56, 35) = 7$.

**7.** (a) Closed: for integers $a, b$, $a - b$ is an integer, yes. (b) Commutative: no; $1 - 2 = -1 \neq 1 = 2 - 1$. (c) Associative: no; $(5 - 3) - 1 = 1$ but $5 - (3 - 1) = 3$.

**8.** $84 = 2 \cdot 42 = 2 \cdot 2 \cdot 21 = 2^2 \cdot 3 \cdot 7$. So $84 = 2^2 \cdot 3 \cdot 7$.

## 4. Advanced exercises

1. **Classes are equal or disjoint.** Let $\sim$ be an equivalence relation on a set $A$. Prove that for all $a, b \in A$, either $[a] = [b]$ or $[a] \cap [b] = \varnothing$. Conclude that the distinct equivalence classes form a partition of $A$.
2. **Congruence is well-behaved under $+$ and $\times$.** Prove: if $a \equiv a' \pmod n$ and $b \equiv b' \pmod n$, then $a + b \equiv a' + b' \pmod n$ and $ab \equiv a'b' \pmod n$. (This is what makes addition and multiplication on $\mathbb{Z}_n$ well-defined.)
3. **Composition of bijections.** Let $f : A \to B$ and $g : B \to C$ be bijections. Prove $g \circ f : A \to C$ is a bijection, and that $(g \circ f)^{-1} = f^{-1} \circ g^{-1}$.
4. **Infinitely many primes.** Prove there are infinitely many prime numbers. (Hint: contradiction; given a finite list, build a number that no listed prime divides.)
5. **A summation by induction.** Prove that $1 + 3 + 5 + \dots + (2n - 1) = n^2$ for every integer $n \ge 1$.

### Solutions

**1.** Suppose $[a] \cap [b] \neq \varnothing$; we show $[a] = [b]$. Pick $c \in [a] \cap [b]$, so $c \sim a$ and $c \sim b$. By symmetry $a \sim c$, and with $c \sim b$, transitivity gives $a \sim b$.

Now show $[a] \subseteq [b]$: take any $x \in [a]$, so $x \sim a$; combined with $a \sim b$, transitivity gives $x \sim b$, so $x \in [b]$. By the symmetric argument (using $b \sim a$, which holds by symmetry) $[b] \subseteq [a]$. Hence $[a] = [b]$.

So any two classes are equal or disjoint. Each $a \in A$ lies in $[a]$ (reflexivity), so the classes are non-empty and cover $A$; being pairwise equal-or-disjoint, the *distinct* ones are pairwise disjoint. Therefore the distinct classes form a partition of $A$. $\blacksquare$

**2.** By hypothesis $n \mid (a - a')$ and $n \mid (b - b')$, say $a - a' = n s$ and $b - b' = n t$ for integers $s, t$.

Sum: $(a + b) - (a' + b') = (a - a') + (b - b') = n s + n t = n(s + t)$, so $n \mid (a+b) - (a'+b')$, i.e. $a + b \equiv a' + b' \pmod n$.

Product: write $a = a' + ns$ and $b = b' + nt$. Then
$$ab = (a' + ns)(b' + nt) = a'b' + n(s b' + a' t + n s t),$$
so $ab - a'b' = n(s b' + a' t + n s t)$, an integer multiple of $n$. Hence $ab \equiv a'b' \pmod n$. Because the result depends only on the classes of $a$ and $b$ (not the chosen representatives), $+$ and $\times$ on $\mathbb{Z}_n$ are well-defined. $\blacksquare$

**3.** *Injective:* suppose $(g\circ f)(a_1) = (g \circ f)(a_2)$, i.e. $g(f(a_1)) = g(f(a_2))$. Since $g$ is injective, $f(a_1) = f(a_2)$; since $f$ is injective, $a_1 = a_2$. *Surjective:* take $c \in C$. Since $g$ is surjective there is $b \in B$ with $g(b) = c$; since $f$ is surjective there is $a \in A$ with $f(a) = b$. Then $(g\circ f)(a) = g(b) = c$. So $g \circ f$ is a bijection and has an inverse.

For the formula, it suffices to check $f^{-1}\circ g^{-1}$ undoes $g \circ f$ on both sides. Using associativity of composition and $g^{-1}\circ g = \mathrm{id}_B$, $f^{-1}\circ f = \mathrm{id}_A$:
$$(f^{-1}\circ g^{-1}) \circ (g \circ f) = f^{-1} \circ (g^{-1}\circ g) \circ f = f^{-1}\circ \mathrm{id}_B \circ f = f^{-1}\circ f = \mathrm{id}_A.$$
Similarly $(g \circ f)\circ(f^{-1}\circ g^{-1}) = \mathrm{id}_C$. By uniqueness of inverses, $(g\circ f)^{-1} = f^{-1}\circ g^{-1}$. (Note the order reverses: socks on then shoes on, so shoes off then socks off.) $\blacksquare$

**4.** Suppose, for contradiction, that there are only finitely many primes, say $p_1, p_2, \dots, p_k$. Consider
$$N = p_1 p_2 \cdots p_k + 1.$$
Since $N > 1$, by the Fundamental Theorem of Arithmetic it has at least one prime divisor $p$, which must be one of $p_1, \dots, p_k$. Then $p \mid N$ and $p \mid p_1\cdots p_k$, so $p \mid (N - p_1\cdots p_k) = 1$. But no prime divides $1$ (since $p \ge 2$), a contradiction. Hence there are infinitely many primes. $\blacksquare$

**5.** *Base case* ($n = 1$): the left side is $1$, the right side is $1^2 = 1$. They match.

*Inductive step:* assume for some $k \ge 1$ that $1 + 3 + \dots + (2k-1) = k^2$. The next odd number is $2(k+1) - 1 = 2k + 1$. Adding it to both sides,
$$1 + 3 + \dots + (2k-1) + (2k+1) = k^2 + (2k + 1) = (k+1)^2.$$
This is exactly the statement for $n = k+1$. By induction the formula holds for all $n \ge 1$. $\blacksquare$

## 5. Real-world relevance

- **Modular arithmetic runs modern cryptography.** RSA and Diffie-Hellman key exchange compute with congruences mod large numbers; coprimality and Bezout's identity (modular inverses) are the gears. See doc #5 for the deep dive.
- **Error-detecting and error-correcting codes** (ISBNs, UPC barcodes, the checksums in your bank-card numbers, QR codes) use arithmetic mod $n$ to catch typos and transmission errors.
- **Hashing and data structures** in computer science map keys into a fixed range using "mod table-size," a direct use of $\mathbb{Z}_n$.
- **Equivalence relations and partitions** model "sameness up to symmetry" everywhere: classifying shapes up to rotation, grouping data into categories, defining the rationals as fractions where $a/b$ and $2a/2b$ are identified.
- **Bijections underpin counting and probability**: showing two finite sets have equal size by exhibiting an explicit pairing is a workhorse of combinatorics.

Doc #5 (Real-World Applications) develops the cryptography and coding-theory examples in full.

## 6. Common pitfalls & misconceptions

- **$\varnothing$ vs $\{\varnothing\}$ vs $\{0\}$.** The empty set has $0$ elements; $\{\varnothing\}$ has $1$ element (an empty box inside a box); $\{0\}$ has $1$ element (the number zero). All three are different.
- **Subset vs element.** $1 \in \{1,2\}$ but $1 \nsubseteq \{1,2\}$ (a number is not a set). However $\{1\} \subseteq \{1,2\}$. Watch $\in$ versus $\subseteq$.
- **Codomain vs image.** A function can be non-surjective; the image may be a proper subset of the codomain. "Onto" is a claim about the *declared* codomain, so always state it.
- **Injective is not the same as surjective.** They are independent. Be ready to check each separately; only when both hold do you get a bijection (and hence an inverse).
- **Composition order.** $g \circ f$ means "do $f$ first." And $g \circ f \neq f \circ g$ in general.
- **Negative remainders.** $(-1) \bmod 5 = 4$, not $-1$. The division algorithm forces $0 \le r < n$.
- **Reading too much into one axiom.** Closure, associativity, identity, and inverses are *separate* properties. An operation can have some and lack others (subtraction has closure but not associativity or commutativity); do not assume the rest just because one holds.
- **$1$ is not prime.** Primes start at $2$. Treating $1$ as prime would break unique factorization.
- **"For some" vs "for all."** Surjectivity says "for every $b$, there exists $a$"; injectivity is a "for all" condition on collisions. Quantifier order and type are where most early proofs go wrong.

## 7. What to learn next

You now have the language: sets, functions, equivalence relations, modular arithmetic, binary operations, the number-theory toolkit, and the core proof methods. Next, in **doc #1, Group Theory I: The Basics**, you take a set with one well-behaved operation (closure, associativity, identity, inverses) and meet the *group*, where $\mathbb{Z}_n$ under addition becomes your very first concrete example.
