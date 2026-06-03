# Group Theory II: Structure & Maps

> Cosets slice a group into equal pieces, normal subgroups let you glue those pieces into a smaller group, and homomorphisms let you compare groups: this is how we actually understand structure.

## 0. Why this matters (the big picture)

In doc #1 you learned what a group is and met subgroups, cyclic groups, permutations, order, and Lagrange's theorem (stated). That gave you the nouns. This document gives you the verbs: how to *take a group apart* (cosets, quotients, factoring into direct products), how to *compare two groups* (homomorphisms, isomorphisms), and how to *act* with a group on a set (group actions). These tools turn "here is a multiplication table" into "here is why this group looks the way it does." Concrete motivating question to keep in mind: **there are exactly two groups of order 4 and exactly two of order 6, but how many groups are there of order 8, and how could we ever be sure we found them all?** By the end you will be able to answer the order-8 question completely.

Throughout, a one-line reminder of facts from doc #1 that we lean on:
- A **group** $(G, \cdot)$ has an associative operation, an identity $e$, and inverses. **Abelian** means $ab = ba$ for all $a,b$.
- $|G|$ is the **order** of the group (number of elements); $|g|$ is the **order of an element** $g$ (smallest $n>0$ with $g^n = e$).
- A **subgroup** $H \le G$ is a subset that is itself a group under the same operation.
- **Lagrange (stated in doc #1):** if $G$ is finite and $H \le G$, then $|H|$ divides $|G|$. We will *prove* this here.
- Standard groups: $\mathbb{Z}_n$ (integers mod $n$ under addition), $S_n$ (permutations of $n$ symbols), $A_n$ (even permutations), $D_n$ (symmetries of a regular $n$-gon, order $2n$), and the **Klein four-group** $V = \{e,a,b,c\}$ with every non-identity element of order 2.

A note on our $D_4$ notation (symmetries of a square): we write $r$ for rotation by $90^\circ$ and $s$ for a fixed reflection, so
$$D_4 = \{e, r, r^2, r^3, s, sr, sr^2, sr^3\}, \quad r^4 = e,\quad s^2 = e,\quad sr = r^{-1}s = r^3 s.$$
The relation $sr = r^3 s$ (equivalently $rs = sr^3$) is the only thing you need to multiply elements of $D_4$ by hand.

---

## 1. Key terms, explained simply

For each term: (a) plain-English intuition, (b) formal definition, (c) a small concrete example.

### Coset

(a) **Intuition.** Pick a subgroup $H$. A coset is a "shifted copy" of $H$. Translating $H$ by an element $g$ slides the whole subgroup somewhere else inside $G$. These shifted copies are all the same size and they tile $G$ perfectly, like identical floor tiles covering a room with no gaps and no overlaps.

(b) **Definition.** For $H \le G$ and $g \in G$, the **left coset** is $gH = \{ gh : h \in H\}$ and the **right coset** is $Hg = \{ hg : h \in H\}$. The **index** $[G:H]$ is the number of distinct left cosets of $H$ in $G$.

(c) **Example.** In $\mathbb{Z}_6 = \{0,1,2,3,4,5\}$ (operation is $+$, so we write $g + H$), take $H = \{0, 3\}$. The cosets are
$$0 + H = \{0,3\}, \quad 1 + H = \{1,4\}, \quad 2 + H = \{2,5\}.$$
Three cosets, each of size 2, covering all 6 elements. So $[\mathbb{Z}_6 : H] = 3$.

### Normal subgroup

(a) **Intuition.** A normal subgroup is one that does not care whether you shift from the left or the right: every left coset is also a right coset. Equivalently, you can "conjugate" (sandwich) the subgroup by any group element and land back on the same subgroup. These are exactly the subgroups you are allowed to divide by.

(b) **Definition.** $N \le G$ is **normal**, written $N \trianglelefteq G$, if $gNg^{-1} = N$ for every $g \in G$, where $gNg^{-1} = \{ gng^{-1} : n \in N\}$. Equivalent conditions: $gN = Ng$ for all $g$ (left cosets equal right cosets), or $gng^{-1} \in N$ for all $g \in G, n \in N$.

(c) **Example.** $A_3 = \{e, (123), (132)\}$ is normal in $S_3$ (it has index 2, and index-2 subgroups are always normal, proved below). **Non-example:** $H = \{e, (12)\}$ is *not* normal in $S_3$, since $(13)(12)(13)^{-1} = (23) \notin H$.

### Quotient group

(a) **Intuition.** If $N$ is normal, collapse each coset to a single point. The set of cosets, with a natural multiplication, becomes a brand-new group, smaller than $G$, that records "$G$ as seen through $N$-blurred glasses." Working mod $N$ is exactly the familiar idea of arithmetic mod $n$, generalized.

(b) **Definition.** For $N \trianglelefteq G$, the **quotient group** $G/N$ is the set of left cosets $\{ gN : g \in G\}$ with operation $(aN)(bN) = (ab)N$. (Normality is what makes this operation well-defined; see Section 1's last entry and Section 2.) Its order is $|G/N| = [G:N]$.

(c) **Example.** $\mathbb{Z}/3\mathbb{Z}$: here $G = \mathbb{Z}$, $N = 3\mathbb{Z} = \{\dots,-3,0,3,6,\dots\}$. The cosets are $\bar 0, \bar 1, \bar 2$ and the quotient is just $\mathbb{Z}_3$, the integers mod 3.

### Group homomorphism

(a) **Intuition.** A homomorphism is a map between groups that respects the operation: do the operation first and then map, or map first and then do the operation, and you get the same answer. It is a "structure-preserving translation."

(b) **Definition.** A function $f : G \to H$ is a **homomorphism** if $f(ab) = f(a)f(b)$ for all $a,b \in G$. (Left side multiplies in $G$; right side multiplies in $H$.) Its **kernel** is $\ker f = \{ g \in G : f(g) = e_H\}$ and its **image** is $\operatorname{im} f = \{ f(g) : g \in G\}$.

(c) **Example.** $f : \mathbb{Z} \to \mathbb{Z}_n$ given by $f(k) = k \bmod n$. Then $f(a+b) = (a+b)\bmod n = f(a) + f(b)$, so $f$ is a homomorphism with $\ker f = n\mathbb{Z}$ and image all of $\mathbb{Z}_n$.

### Isomorphism

(a) **Intuition.** An isomorphism is a homomorphism that is also a perfect relabeling (a bijection). If two groups are isomorphic, they are "the same group wearing different clothes": same size, same multiplication pattern, same everything that group theory can see.

(b) **Definition.** A homomorphism $f : G \to H$ is an **isomorphism** if it is a bijection. We write $G \cong H$ and say $G$ and $H$ are **isomorphic**. (Equivalently, a homomorphism is an isomorphism iff $\ker f = \{e\}$ and $\operatorname{im} f = H$.)

(c) **Example.** $f : (\mathbb{Z}_4, +) \to (\{1,i,-1,-i\}, \times)$ with $f(k) = i^k$ is an isomorphism. Both are cyclic of order 4.

### Direct product

(a) **Intuition.** Glue two groups side by side and operate in each slot independently, like running two odometers at once.

(b) **Definition.** The **(external) direct product** $G \times H$ has underlying set the ordered pairs $\{(g,h)\}$ with componentwise operation $(g_1,h_1)(g_2,h_2) = (g_1 g_2,\, h_1 h_2)$. Its order is $|G|\cdot|H|$.

(c) **Example.** $\mathbb{Z}_2 \times \mathbb{Z}_2$ has elements $(0,0),(1,0),(0,1),(1,1)$, each non-identity element of order 2. This is the Klein four-group $V$.

### Group action

(a) **Intuition.** A group action is a group "doing things" to the points of a set: each group element is a way of rearranging the set, consistently with the group operation. Think of the rotation group of a cube acting on the cube's 8 corners.

(b) **Definition.** An **action** of $G$ on a set $X$ is a map $G \times X \to X$, written $g \cdot x$, such that $e \cdot x = x$ and $(gh)\cdot x = g \cdot (h \cdot x)$ for all $g,h \in G, x \in X$. The **orbit** of $x$ is $\mathrm{Orb}(x) = \{ g\cdot x : g \in G\}$; the **stabilizer** is $\mathrm{Stab}(x) = \{ g \in G : g \cdot x = x\}$, which is always a subgroup of $G$.

(c) **Example.** $D_4$ acts on the 4 corners of a square $\{1,2,3,4\}$. The orbit of corner $1$ is all four corners (you can rotate $1$ anywhere); $\mathrm{Stab}(1)$ is $\{e, \text{reflection through corner } 1\}$, size 2. Note $4 \cdot 2 = 8 = |D_4|$: a preview of Orbit-Stabilizer.

### Why normality is the key (well-definedness)

(a) **Intuition.** To multiply cosets by the rule $(aN)(bN) = (ab)N$, the answer must depend only on the cosets, not on the particular names $a,b$ we picked. Normality is precisely the condition that guarantees this.

(b) **Statement.** The operation $(aN)(bN) = (ab)N$ on cosets is well-defined **if and only if** $N \trianglelefteq G$. (Proof in Section 2, Example 3.)

(c) **Example.** With $N$ non-normal, well-definedness fails: in $S_3$ with $H=\{e,(12)\}$, the coset $(13)H$ multiplied by $H$ gives different answers depending on the representative, so $S_3/H$ is *not* a group.

---

## 2. Worked examples

### Example 1: Cosets tile $D_4$, and we read off the index

Let $G = D_4$ (order 8) and let $H = \{e, s\}$ (a reflection subgroup, order 2). We compute all left cosets $gH$.

- $eH = \{e, s\}$.
- $rH = \{r, rs\}$. Using $rs = sr^3$ we may also write $rs = sr^3$, but as a set $rH = \{r, rs\}$.
- $r^2 H = \{r^2, r^2 s\}$.
- $r^3 H = \{r^3, r^3 s\}$.

That is already 8 elements ($\{e,r,r^2,r^3,s,rs,r^2s,r^3s\}$ is all of $D_4$), so these 4 cosets tile $G$. Hence $[D_4 : H] = 4$, and indeed $|H|\cdot[D_4:H] = 2 \cdot 4 = 8 = |D_4|$.

**Right cosets differ here.** Compute $Hr = \{r, sr\} = \{r, r^3 s\}$ (since $sr = r^3 s$). But $rH = \{r, rs\} = \{r, sr^3\}$. Since $sr^3 \ne r^3 s$ in general (they are different elements: $sr^3$ vs $sr$), we get $rH \ne Hr$. This is a concrete witness that $H = \{e,s\}$ is **not normal** in $D_4$.

### Example 2: A clean PROOF of Lagrange's theorem via cosets

**Claim.** If $G$ is a finite group and $H \le G$, then $|H|$ divides $|G|$, and in fact $|G| = |H| \cdot [G:H]$.

**Step 1: Cosets all have the same size as $H$.** Fix $g \in G$. The map $H \to gH$, $h \mapsto gh$, is a bijection: it is onto by definition of $gH$, and it is one-to-one because $gh_1 = gh_2 \Rightarrow h_1 = h_2$ by cancellation (multiply by $g^{-1}$). Hence $|gH| = |H|$ for every $g$.

**Step 2: Distinct cosets are disjoint.** Suppose two left cosets overlap: $aH \cap bH \ne \varnothing$. Then some element equals $ah_1 = bh_2$ with $h_1,h_2 \in H$. So $a = b h_2 h_1^{-1} \in bH$. Then for any $ah \in aH$ we have $ah = b(h_2 h_1^{-1} h) \in bH$, giving $aH \subseteq bH$; symmetrically $bH \subseteq aH$. Thus $aH = bH$. Contrapositive: if $aH \ne bH$ they are disjoint. (So "lies in the same left coset" is an equivalence relation, and cosets are its equivalence classes.)

**Step 3: Count.** The left cosets partition $G$ into $[G:H]$ disjoint pieces, each of size $|H|$ by Step 1. Therefore
$$|G| = \sum_{\text{distinct cosets}} |gH| = [G:H]\cdot |H|.$$
In particular $|H|$ divides $|G|$. $\blacksquare$

**Two instant corollaries.** (i) For any $g \in G$, the order $|g|$ divides $|G|$ (apply Lagrange to $H = \langle g\rangle$, whose order equals $|g|$). (ii) Every group of prime order $p$ is cyclic: a non-identity element $g$ has order dividing $p$ and $>1$, so $|g|=p$, so $\langle g\rangle = G$.

### Example 3: Building a quotient group, and seeing why normality is forced

We build $S_3 / A_3$ and prove the coset operation is well-defined exactly when $N$ is normal.

Recall $S_3 = \{e,(123),(132),(12),(13),(23)\}$ and $A_3 = \{e,(123),(132)\}$ (the rotations / even permutations). Since $[S_3 : A_3] = 6/3 = 2$, there are exactly two cosets:
$$A_3 \quad\text{(the evens)}, \qquad (12)A_3 = \{(12),(13),(23)\} \quad\text{(the odds)}.$$
Label them $E$ (even) and $O$ (odd). The multiplication is forced by parity: even$\cdot$even = even, even$\cdot$odd = odd, odd$\cdot$odd = even. So $S_3/A_3 \cong \mathbb{Z}_2$.

**Why this is legitimate: well-definedness.** Define $(aN)(bN) := (ab)N$. We must check: if $aN = a'N$ and $bN = b'N$, then $(ab)N = (a'b')N$. Write $a' = a n_1$ and $b' = b n_2$ with $n_1,n_2 \in N$ (this is exactly what $aN=a'N$ means: $a' \in aN$). Then
$$a' b' = a n_1 b n_2 = a b \,(b^{-1} n_1 b)\, n_2.$$
For $(a'b')N = (ab)N$ we need $(b^{-1} n_1 b) n_2 \in N$, i.e. $b^{-1} n_1 b \in N$. This must hold for all $b \in G$ and all $n_1 \in N$, which is precisely the statement $b^{-1} N b = N$, i.e. **$N$ is normal**. Conversely, if $N$ is normal this computation shows the product is well-defined. So the construction works **if and only if $N \trianglelefteq G$**, and $A_3$ qualifies because index-2 subgroups are always normal. $\blacksquare$

**Why index 2 forces normality.** If $[G:H]=2$ there are two left cosets, $H$ and $G\setminus H$, and likewise two right cosets, $H$ and $G\setminus H$. For $g \in H$: $gH = H = Hg$. For $g \notin H$: $gH = G\setminus H = Hg$ (both are "everything except $H$"). So $gH = Hg$ for all $g$, hence $H \trianglelefteq G$.

### Example 4: A quotient of $D_4$, and the First Isomorphism Theorem in action

Inside $D_4$, the center is $Z = \{e, r^2\}$ (you can check $r^2$ commutes with everything: $r^2 \cdot s = s \cdot r^2$ since $s r^2 = r^{-2} s = r^2 s$). The center is always normal, so $D_4 / Z$ makes sense, and $|D_4/Z| = 8/2 = 4$.

The four cosets are
$$\{e,r^2\},\quad \{r, r^3\},\quad \{s, r^2 s\},\quad \{rs, r^3 s\}.$$
Call them $\bar e, \bar r, \bar s, \overline{rs}$. Each non-identity coset squares to $\bar e$: e.g. $\bar r^2 = \overline{r^2} = \bar e$, and $\bar s^2 = \overline{s^2} = \overline{e} = \bar e$, and $\overline{rs}^2 = \overline{(rs)^2}$; using $rs\cdot rs = r (s r) s = r(r^3 s)s = r^4 s^2 = e$, so $\overline{rs}^2 = \bar e$. Every non-identity element has order 2, so
$$D_4 / Z \cong V \quad(\text{Klein four-group}).$$
This is a famous fact: $D_4$ modulo its center is the Klein four-group, *not* cyclic, which tells you $D_4$ is "more abelian-looking" after collapsing the center but still not cyclic.

---

## 3. Basic exercises

1. In $\mathbb{Z}_{12}$, let $H = \langle 4 \rangle = \{0,4,8\}$. List all left cosets of $H$ and state $[\mathbb{Z}_{12}:H]$.
2. In $S_3$, list all left cosets and all right cosets of $H = \{e,(12)\}$. Are they the same? What does this say about normality?
3. Define $f:\mathbb{Z} \to \mathbb{Z}$ by $f(n) = 2n$. Is $f$ a homomorphism? Is it injective? Surjective? What is $\ker f$ and $\operatorname{im} f$?
4. List the elements of $\mathbb{Z}_2 \times \mathbb{Z}_3$ and find the order of each. Is the group cyclic? Which familiar group is it isomorphic to?
5. Is $\mathbb{Z}_2 \times \mathbb{Z}_2$ isomorphic to $\mathbb{Z}_4$? Justify by comparing element orders.
6. $D_4$ acts on the four corners $\{1,2,3,4\}$ of a square (labeled in order around the square). Find $\mathrm{Orb}(1)$ and $\mathrm{Stab}(1)$, and verify $|\mathrm{Orb}(1)|\cdot|\mathrm{Stab}(1)| = |D_4|$.
7. Show that the identity coset $eN = N$ is the identity element of $G/N$, and that the inverse of $gN$ is $g^{-1}N$.

### Solutions

**1.** $H=\{0,4,8\}$. Cosets: $0+H=\{0,4,8\}$, $1+H=\{1,5,9\}$, $2+H=\{2,6,10\}$, $3+H=\{3,7,11\}$. These four sets of size 3 cover all 12 elements, so $[\mathbb{Z}_{12}:H]=4$ (consistent with $12 = 3\cdot 4$).

**2.** Left cosets of $H=\{e,(12)\}$:
$eH=\{e,(12)\}$, $(13)H=\{(13),(13)(12)\}=\{(13),(132)\}$, $(23)H=\{(23),(23)(12)\}=\{(23),(123)\}$.
Right cosets:
$He=\{e,(12)\}$, $H(13)=\{(13),(12)(13)\}=\{(13),(123)\}$, $H(23)=\{(23),(12)(23)\}=\{(23),(132)\}$.
Compare: $(13)H=\{(13),(132)\}$ but $H(13)=\{(13),(123)\}$. They differ, so $H$ is **not normal** in $S_3$.

**3.** $f(m+n)=2(m+n)=2m+2n=f(m)+f(n)$, so $f$ is a homomorphism. Injective: $2m=2n\Rightarrow m=n$, yes. Surjective: no, odd numbers are not hit. $\ker f = \{n : 2n=0\} = \{0\}$. $\operatorname{im} f = 2\mathbb{Z}$ (the even integers).

**4.** Elements with orders ($\mathrm{lcm}$ of component orders): $(0,0)$ order 1; $(1,0)$ order 2; $(0,1)$ order 3; $(0,2)$ order 3; $(1,1)$ order $\mathrm{lcm}(2,3)=6$; $(1,2)$ order 6. There is an element of order 6 in a group of order 6, so it is **cyclic**, hence $\mathbb{Z}_2\times\mathbb{Z}_3 \cong \mathbb{Z}_6$. (This is the smallest case of the Chinese Remainder Theorem, Section 4.)

**5.** No. In $\mathbb{Z}_4$ the element $1$ has order 4. In $\mathbb{Z}_2\times\mathbb{Z}_2$ every non-identity element has order 2 (e.g. $(1,1)+(1,1)=(0,0)$), so there is no element of order 4. An isomorphism preserves element orders, so they cannot be isomorphic. (Two groups of the same order, 4, that are not isomorphic.)

**6.** Rotations send corner $1$ to each of $1,2,3,4$, so $\mathrm{Orb}(1)=\{1,2,3,4\}$, size 4. $\mathrm{Stab}(1)$: which symmetries fix corner $1$? The identity, and the reflection across the diagonal through corner $1$ (and corner $3$). So $|\mathrm{Stab}(1)|=2$. Check: $4\cdot 2 = 8 = |D_4|$.

**7.** Identity: $(eN)(gN)=(eg)N = gN$ and $(gN)(eN)=(ge)N=gN$, so $eN=N$ is a two-sided identity. Inverse: $(gN)(g^{-1}N)=(gg^{-1})N=eN=N$ and $(g^{-1}N)(gN)=(g^{-1}g)N=N$, so $(gN)^{-1}=g^{-1}N$. (Associativity is inherited from $G$: $((aN)(bN))(cN)=(abc)N=(aN)((bN)(cN))$. So $G/N$ is genuinely a group.)

---

## 4. Advanced exercises

1. **(Kernel is normal; image is a subgroup.)** Let $f:G\to H$ be a homomorphism. Prove $f(e_G)=e_H$ and $f(g^{-1})=f(g)^{-1}$. Then prove $\ker f \trianglelefteq G$ and $\operatorname{im} f \le H$.
2. **(First Isomorphism Theorem.)** With $f:G\to H$ a homomorphism, prove $G/\ker f \cong \operatorname{im} f$ via the map $\bar f(g\ker f) = f(g)$. (Check: well-defined, homomorphism, injective, surjective onto the image.)
3. **(Orbit-Stabilizer.)** For a group $G$ acting on a set $X$ and $x\in X$, prove $|\mathrm{Orb}(x)| = [G : \mathrm{Stab}(x)]$. Deduce that if $G$ is finite, $|\mathrm{Orb}(x)|$ divides $|G|$.
4. **(Cauchy + a Sylow application.)** (i) State Cauchy's theorem. (ii) Use the Sylow theorems to prove every group of order 15 is cyclic, hence isomorphic to $\mathbb{Z}_{15}$.
5. **(Counting via Sylow.)** Prove that no group of order 20 is simple (find a normal Sylow subgroup).
6. **(Fundamental Theorem of Finite Abelian Groups.)** List, up to isomorphism, all abelian groups of order 8 and all abelian groups of order 12. For order 8, identify which one is $\mathbb{Z}_2\times\mathbb{Z}_2\times\mathbb{Z}_2$ and confirm it is not cyclic.

### Solutions

**1.** *Identity.* From $f(e_G)=f(e_G e_G)=f(e_G)f(e_G)$, cancel one $f(e_G)$ (multiply by its inverse in $H$) to get $e_H = f(e_G)$.
*Inverses.* $f(g)f(g^{-1}) = f(gg^{-1}) = f(e_G)=e_H$, and similarly on the other side, so $f(g^{-1})=f(g)^{-1}$.
*$\operatorname{im} f \le H$.* It contains $e_H=f(e_G)$; it is closed since $f(a)f(b)=f(ab)\in\operatorname{im} f$; it has inverses since $f(a)^{-1}=f(a^{-1})\in\operatorname{im} f$.
*$\ker f \trianglelefteq G$.* First $\ker f$ is a subgroup: $f(e_G)=e_H$ so $e_G\in\ker f$; if $a,b\in\ker f$ then $f(ab)=f(a)f(b)=e_H e_H = e_H$; and $f(a^{-1})=f(a)^{-1}=e_H^{-1}=e_H$. Normality: for $g\in G$, $k\in\ker f$,
$$f(gkg^{-1}) = f(g)f(k)f(g)^{-1} = f(g)\,e_H\,f(g)^{-1} = e_H,$$
so $gkg^{-1}\in\ker f$. Hence $g(\ker f)g^{-1}\subseteq \ker f$ for all $g$; applying this to $g^{-1}$ gives the reverse inclusion, so $g(\ker f)g^{-1}=\ker f$. Thus $\ker f$ is normal. $\blacksquare$

**2.** Let $K=\ker f$. Define $\bar f : G/K \to \operatorname{im} f$ by $\bar f(gK)=f(g)$.
*Well-defined.* If $gK=g'K$ then $g'=gk$ for some $k\in K$, so $f(g')=f(g)f(k)=f(g)e_H=f(g)$. The value does not depend on the representative.
*Homomorphism.* $\bar f((aK)(bK)) = \bar f(abK) = f(ab) = f(a)f(b) = \bar f(aK)\bar f(bK)$.
*Injective.* If $\bar f(gK)=e_H$ then $f(g)=e_H$, so $g\in K$, so $gK=K$, the identity of $G/K$. A homomorphism with trivial kernel is injective.
*Surjective onto $\operatorname{im} f$.* Any element of $\operatorname{im} f$ is $f(g)=\bar f(gK)$ for some $g$.
A bijective homomorphism is an isomorphism, so $G/\ker f \cong \operatorname{im} f$. $\blacksquare$

**3.** Define $\varphi : \{\text{left cosets of } S:=\mathrm{Stab}(x)\} \to \mathrm{Orb}(x)$ by $\varphi(gS) = g\cdot x$.
*Well-defined and injective at once.* For $a,b\in G$:
$$aS = bS \iff b^{-1}a \in S \iff (b^{-1}a)\cdot x = x \iff a\cdot x = b\cdot x.$$
The middle step uses the definition of stabilizer; the last uses the action axioms ($a\cdot x = b\cdot x \iff (b^{-1}a)\cdot x = x$ by acting with $b^{-1}$). So $\varphi$ is well-defined ($\Rightarrow$) and injective ($\Leftarrow$).
*Surjective.* Every orbit element is $g\cdot x = \varphi(gS)$.
Hence $\varphi$ is a bijection and $|\mathrm{Orb}(x)| = [G:\mathrm{Stab}(x)]$. If $G$ is finite, $[G:\mathrm{Stab}(x)] = |G|/|\mathrm{Stab}(x)|$ divides $|G|$. $\blacksquare$

**4.** (i) **Cauchy's theorem:** if $G$ is a finite group and a prime $p$ divides $|G|$, then $G$ has an element of order $p$ (equivalently, a subgroup of order $p$).
(ii) $|G|=15=3\cdot 5$. By Sylow III (below), the number $n_5$ of Sylow $5$-subgroups satisfies $n_5 \equiv 1 \pmod 5$ and $n_5 \mid 3$; the only possibility is $n_5=1$. Likewise $n_3 \equiv 1 \pmod 3$ and $n_3 \mid 5$ forces $n_3=1$. A Sylow subgroup that is unique is normal (its conjugates are again Sylow subgroups of the same order, and uniqueness pins it down). So there is a normal subgroup $P$ of order 5 and a normal subgroup $Q$ of order 3. They intersect trivially ($|P\cap Q|$ divides $\gcd(5,3)=1$), and $|PQ| = |P||Q|/|P\cap Q| = 15 = |G|$, so $G = PQ$. With both factors normal and trivial intersection, $G \cong P\times Q \cong \mathbb{Z}_5\times\mathbb{Z}_3 \cong \mathbb{Z}_{15}$ (the last step is CRT since $\gcd(3,5)=1$). So every group of order 15 is cyclic. $\blacksquare$

**5.** $|G|=20=2^2\cdot 5$. By Sylow III, $n_5\equiv 1\pmod 5$ and $n_5 \mid 4$. Divisors of 4 that are $\equiv 1 \pmod 5$: only $n_5=1$. So the Sylow 5-subgroup is unique, hence normal. A group with a nontrivial proper normal subgroup is **not simple**. (Concretely, that normal subgroup has order 5, strictly between 1 and 20.) $\blacksquare$

**6.** *Order 8* ($8=2^3$). Partitions of the exponent 3: $3$, $2+1$, $1+1+1$. The abelian groups are
$$\mathbb{Z}_8,\qquad \mathbb{Z}_4\times\mathbb{Z}_2,\qquad \mathbb{Z}_2\times\mathbb{Z}_2\times\mathbb{Z}_2.$$
Exactly three, up to isomorphism. The last is $\mathbb{Z}_2\times\mathbb{Z}_2\times\mathbb{Z}_2$; every non-identity element has order 2, so the maximum element order is 2 < 8, hence it is **not cyclic**. (Only $\mathbb{Z}_8$ is cyclic.)
*Order 12* ($12 = 2^2\cdot 3$). Handle each prime separately. For $2^2$: $\mathbb{Z}_4$ or $\mathbb{Z}_2\times\mathbb{Z}_2$. For $3$: only $\mathbb{Z}_3$. Combine:
$$\mathbb{Z}_4\times\mathbb{Z}_3 \cong \mathbb{Z}_{12}, \qquad \mathbb{Z}_2\times\mathbb{Z}_2\times\mathbb{Z}_3 \cong \mathbb{Z}_2\times\mathbb{Z}_6.$$
Exactly two abelian groups of order 12, up to isomorphism. $\blacksquare$

---

## 5. Real-world relevance

The structure tools here are not just bookkeeping; they are the working language of large parts of applied mathematics, computer science, and physics. Doc #5 (Applications) develops these; here is where the present chapter lands.

- **Cryptography.** The map $\mathbb{Z} \to \mathbb{Z}_n$ and the structure of $(\mathbb{Z}/n\mathbb{Z})^\times$ underlie RSA and Diffie-Hellman. The Chinese Remainder Theorem ($\mathbb{Z}_{mn}\cong\mathbb{Z}_m\times\mathbb{Z}_n$ when $\gcd(m,n)=1$) is used directly to speed up RSA decryption.
- **Error-correcting codes.** Quotient groups $\mathbb{Z}_2^n / C$ and coset decoding (each received word lies in a coset of the code $C$; you correct to the coset's lowest-weight representative) are exactly the cosets of Section 1, applied to data transmission.
- **Symmetry in physics and chemistry.** Group actions, orbits, and stabilizers classify the symmetries of molecules and crystals; Orbit-Stabilizer is the counting engine behind counting distinct configurations (Burnside / Polya counting), e.g. counting distinct colorings of a cube's faces.
- **Solvability of equations.** Quotients and normal subgroups build the notion of a *solvable group*, which (doc #4, Galois Theory) is exactly what decides whether a polynomial is solvable by radicals.
- **Puzzles.** Cayley's theorem ("every group sits inside some $S_n$") is why the Rubik's cube group is a concrete subgroup of a permutation group, and why orbit-stabilizer counts reachable states.

---

## 6. Common pitfalls & misconceptions

- **"$gH = Hg$ always."** False unless $H$ is normal. Left and right cosets can genuinely differ (see $\{e,s\}$ in $D_4$, Example 1).
- **"Every subgroup gives a quotient group."** No. You can only form $G/N$ when $N$ is normal. Otherwise coset multiplication is not well-defined (Example 3).
- **"Same order means isomorphic."** No. $\mathbb{Z}_4 \not\cong \mathbb{Z}_2\times\mathbb{Z}_2$ (order 4), and $\mathbb{Z}_6 \not\cong S_3$ (order 6: one is abelian, one is not). Isomorphism must preserve element orders, abelianness, and more.
- **"Cosets are subgroups."** Only the coset $eN = N$ is a subgroup. A coset $gN$ with $g\notin N$ does not contain the identity, so it is not a subgroup.
- **"The kernel is the image, or kernel lives in $H$."** The kernel lives in the domain $G$ and is normal there; the image lives in the codomain $H$ and is a subgroup there. Do not mix the two sides.
- **"$gNg^{-1}\subseteq N$ is weaker than $=N$."** For finite groups these are equivalent (conjugation by $g$ is a bijection preserving size). State normality as $gNg^{-1}=N$ to be safe; for infinite groups the equality form is the correct definition.
- **"Sylow's theorem gives a *unique* subgroup."** Sylow I only guarantees *existence* of a Sylow $p$-subgroup. Uniqueness (hence normality) happens only when the count $n_p = 1$, which you must verify from the congruence and divisibility conditions.
- **"$\mathbb{Z}_m\times\mathbb{Z}_n$ is always cyclic."** Only when $\gcd(m,n)=1$. $\mathbb{Z}_2\times\mathbb{Z}_2$ is not cyclic.

---

## 7. What to learn next

You now know how to take groups apart and compare them; the natural sequel is to keep *two* operations at once. Continue to **doc #3 (Ring Theory)**, where the quotient and homomorphism machinery you just learned reappears almost verbatim: ideals play the role of normal subgroups, quotient rings $R/I$ generalize $G/N$, and there is a First Isomorphism Theorem for rings too.

---

### Appendix: statements you can rely on (quick reference)

- **Lagrange:** $|G| = |H|\cdot[G:H]$ for $H\le G$ finite. (Proved, Example 2.)
- **First Isomorphism Theorem:** $G/\ker f \cong \operatorname{im} f$. (Proved, Adv. Ex. 2.)
- **Second (Diamond) Isomorphism Theorem:** if $H\le G$ and $N\trianglelefteq G$, then $HN\le G$, $H\cap N \trianglelefteq H$, and $HN/N \cong H/(H\cap N)$.
- **Third Isomorphism Theorem:** if $N\trianglelefteq G$, $K\trianglelefteq G$, and $N\subseteq K$, then $K/N\trianglelefteq G/N$ and $(G/N)/(K/N) \cong G/K$.
- **Orbit-Stabilizer:** $|\mathrm{Orb}(x)| = [G:\mathrm{Stab}(x)]$. (Proved, Adv. Ex. 3.)
- **Cayley:** every group $G$ embeds (injective homomorphism) into the symmetric group on $|G|$ symbols, via $g \mapsto (x \mapsto gx)$ (left multiplication). Idea: left multiplication by $g$ permutes $G$, and the map $G\to\operatorname{Sym}(G)$ is an injective homomorphism because $gx = x$ for all $x$ forces $g=e$.
- **Cauchy:** if prime $p \mid |G|$, then $G$ has an element of order $p$.
- **Sylow I (existence):** if $|G| = p^k m$ with $p \nmid m$, then $G$ has a subgroup of order $p^k$ (a Sylow $p$-subgroup).
- **Sylow II (conjugacy):** all Sylow $p$-subgroups are conjugate to one another; every $p$-subgroup lies inside some Sylow $p$-subgroup.
- **Sylow III (count):** the number $n_p$ of Sylow $p$-subgroups satisfies $n_p \equiv 1 \pmod p$ and $n_p \mid m$. In particular $n_p = 1$ iff the Sylow $p$-subgroup is normal.
- **Fundamental Theorem of Finite Abelian Groups:** every finite abelian group is a direct product of cyclic groups of prime-power order, and this decomposition is unique up to reordering the factors.
- **Simple group:** a group $G \ne \{e\}$ with no normal subgroups other than $\{e\}$ and $G$. These are the "atoms" of finite group theory; the complete classification of finite simple groups (finished around 1980-2004, thousands of pages) is one of the great achievements of mathematics. Examples: $\mathbb{Z}_p$ for prime $p$ (the only abelian simple groups) and $A_n$ for $n\ge 5$.

**Quick classification facts you can now justify.**
- *Order $p$ (prime):* only $\mathbb{Z}_p$ (Lagrange corollary, Example 2).
- *Order $2p$ ($p$ an odd prime):* exactly two groups, $\mathbb{Z}_{2p}$ (cyclic) and $D_p$ (dihedral, non-abelian). For example, order 6: $\mathbb{Z}_6$ and $S_3 = D_3$; order 10: $\mathbb{Z}_{10}$ and $D_5$.
