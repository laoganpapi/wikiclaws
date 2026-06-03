# Real-World Applications of Abstract Algebra

> The same groups, rings, and fields from docs #0-#4 quietly run your bank card, your phone, your streaming service, and our best theories of nature.

## 0. Why this matters (the big picture)

Abstract algebra can feel like a tower of definitions stacked on definitions. This document is the payoff. Every structure you met in docs #0-#4 (groups, rings, fields, finite fields, group actions) turns out to be the exact tool engineers and scientists reach for when they face a concrete problem: keeping a secret over a public wire, fixing a scratched disc, catching a typo in an account number, counting objects that look the same after you flip them, or writing down the symmetries of a molecule or of the universe. The abstraction is the point: one theory of "symmetry and structure" solves problems that look completely unrelated on the surface.

## 1. Key terms, explained simply

A quick recap of just the structures we use below. Each points back to an earlier document.

- **Group** (doc #1): a set with one operation that is associative, has an identity, and gives every element an inverse. Intuition: the collection of "moves" you can undo. Example: rotations of a square, or addition on a clock.
- **Cyclic group** (doc #2): a group where every element is a power $g, g^2, g^3, \dots$ of a single generator $g$. Intuition: one move, repeated, reaches everything.
- **Modular arithmetic / $\mathbb{Z}_n$** (doc #0, doc #3): the integers $\{0, 1, \dots, n-1\}$ with "wrap around at $n$" addition and multiplication, i.e. clock arithmetic. We write $a \equiv b \pmod{n}$ when $n$ divides $a - b$.
- **Units mod $n$, written $(\mathbb{Z}/n\mathbb{Z})^\times$** (doc #3): the elements of $\mathbb{Z}_n$ that have a multiplicative inverse, namely those coprime to $n$. They form a group under multiplication. Its size is $\varphi(n)$, Euler's totient.
- **Finite field $\mathbb{F}_p$** (doc #4): when $p$ is prime, $\mathbb{Z}_p$ is a field: you can add, subtract, multiply, and divide by anything nonzero. The one fact we reuse constantly: in $\mathbb{F}_p$ every nonzero element has an inverse.
- **Finite field $\mathbb{F}_{p^n}$** (doc #4): for each prime power $p^n$ there is exactly one field with $p^n$ elements. The simplest beyond $\mathbb{F}_p$ is $\mathbb{F}_{2^8}$ with 256 elements, the "byte field" used in error correction and AES.
- **Group action** (doc #2): a group $G$ "acting" on a set $X$ means each $g \in G$ permutes $X$, consistently with the group operation. Intuition: symmetries shuffling the objects they act on. The **orbit** of a point is everything it can be moved to.

That is all the vocabulary you need. Everything below is built from it.

## 2. The applications

### 2.1 Cryptography 1: Diffie-Hellman key exchange

**The real problem.** Alice and Bob have never met and share no secret, yet they want to agree on a secret key while an eavesdropper, Eve, records every message they send. How can two people create a shared secret in public?

**The algebra.** Work in the cyclic group $(\mathbb{Z}/p\mathbb{Z})^\times$ of units modulo a prime $p$. Pick a generator $g$ (a "primitive root"). The security rests on the **discrete logarithm problem**: given $g$ and $g^a \bmod p$, recovering $a$ is believed to be hard for large $p$, even though computing $g^a$ from $a$ is easy. Exponentiation is a one-way street.

**Worked example.** Public parameters: $p = 23$, $g = 5$. First check $5$ generates: its powers mod 23 are
$$5, 2, 10, 4, 20, 8, 17, 16, 11, 9, 22, \dots$$
which run through many distinct values, so $5$ is a good base.

1. Alice picks secret $a = 6$ and sends $A = g^a = 5^6 \bmod 23$. Compute $5^2 = 25 \equiv 2$, so $5^6 = (5^2)^3 \equiv 2^3 = 8$. She sends $A = 8$.
2. Bob picks secret $b = 15$ and sends $B = g^b = 5^{15} \bmod 23 = 19$. (From the power table, the 15th power of 5 is 19.)
3. Alice computes $s = B^a = 19^6 \bmod 23$. Bob computes $s = A^b = 8^{15} \bmod 23$.

Both get the **same** number because $B^a = (g^b)^a = g^{ab} = (g^a)^b = A^b$. Let us check: $19^2 = 361 = 15\cdot 23 + 16 \equiv 16$; $19^3 \equiv 16 \cdot 19 = 304 = 13 \cdot 23 + 5 \equiv 5$; then $19^6 = (19^3)^2 \equiv 5^2 = 25 \equiv 2$. So the shared secret is $\boxed{2}$. Eve sees $p, g, 8, 19$ but cannot easily find $a$ or $b$, so she cannot compute $g^{ab}$.

### 2.2 Cryptography 2: RSA

**The real problem.** Alice wants anyone to be able to send her a private message, using a key she publishes openly, while only she can read what comes back. This is **public-key** encryption.

**The algebra.** Work with units modulo $n = pq$, a product of two large primes. The engine is Euler's theorem.

> **Fermat's little theorem.** If $p$ is prime and $\gcd(a, p) = 1$, then $a^{p-1} \equiv 1 \pmod p$.
>
> **Euler's theorem (the generalization).** If $\gcd(a, n) = 1$, then $a^{\varphi(n)} \equiv 1 \pmod n$, where $\varphi(n)$ is the number of units mod $n$. For $n = pq$, $\varphi(n) = (p-1)(q-1)$.

In group language: $a$ lives in the group $(\mathbb{Z}/n\mathbb{Z})^\times$ of order $\varphi(n)$, and any element raised to the order of the group gives the identity. RSA chooses an encryption exponent $e$ and a decryption exponent $d$ that are inverses modulo $\varphi(n)$, so $ed \equiv 1$. Then raising to the $e$ then the $d$ returns the original message, because the exponent $ed$ is $1$ plus a multiple of $\varphi(n)$.

**Worked example.** Pick $p = 5$, $q = 11$, so $n = 55$ and $\varphi(n) = (5-1)(11-1) = 4 \cdot 10 = 40$.

1. Choose public exponent $e = 3$. Check $\gcd(3, 40) = 1$. Good.
2. Find the private exponent $d$ with $3d \equiv 1 \pmod{40}$. Trying multiples: $3 \cdot 27 = 81 = 2\cdot 40 + 1 \equiv 1$. So $d = 27$.
3. Public key: $(n, e) = (55, 3)$. Private key: $d = 27$.
4. Encrypt message $m = 7$: $c = m^e = 7^3 \bmod 55$. Now $7^2 = 49$, and $7^3 = 343 = 6 \cdot 55 + 13 \equiv 13$. Ciphertext $c = 13$.
5. Decrypt: $m = c^d = 13^{27} \bmod 55$. Rather than a giant power, trust the theorem: $ed = 81 = 2\varphi(n) + 1$, so $c^d = m^{ed} = m^{1 + 2\varphi(n)} = m \cdot (m^{\varphi(n)})^2 \equiv m \cdot 1^2 = m = 7$.

The message round-trips: $7 \to 13 \to 7$. Anyone can encrypt with $(55, 3)$, but only the holder of $d = 27$ (which requires knowing $\varphi(n)$, which requires factoring $n$) can decrypt. RSA's security is the difficulty of factoring $n = pq$ for large primes.

### 2.3 Cryptography 3: elliptic curves (intuition)

**The real problem.** Diffie-Hellman and RSA need large numbers (thousands of bits) for safety, which costs bandwidth and battery on phones and smart cards. Can we get the same security with smaller keys?

**The algebra.** Take an elliptic curve, the solutions $(x, y)$ to an equation like $y^2 = x^3 + ax + b$, over a finite field $\mathbb{F}_p$, plus one extra "point at infinity" $\mathcal{O}$. Remarkably, **these points form an abelian group**, with $\mathcal{O}$ as the identity.

**The group law, in words.** To add two points $P$ and $Q$: draw the straight line through them. Over $\mathbb{R}$ this line hits the curve in exactly one more point; reflect that third point across the $x$-axis to get $P + Q$. To double a point, use the tangent line instead. The point at infinity plays the role of zero, and the reflection of $P$ across the $x$-axis is its inverse $-P$. Over a finite field the same recipe runs as algebra with explicit slope formulas.

**A tiny addition over $\mathbb{F}_5$.** Take $y^2 = x^3 + x + 1$ over $\mathbb{F}_5$. The affine points are
$$(0,1),(0,4),(2,1),(2,4),(3,1),(3,4),(4,2),(4,3),$$
which with $\mathcal{O}$ gives a group of order 9. Add $P = (0,1)$ and $Q = (2,4)$. The slope of the chord is
$$\lambda = \frac{y_Q - y_P}{x_Q - x_P} = \frac{4 - 1}{2 - 0} = \frac{3}{2} = 3 \cdot 2^{-1} \pmod 5.$$
In $\mathbb{F}_5$, $2^{-1} = 3$ (since $2 \cdot 3 = 6 \equiv 1$), so $\lambda = 3 \cdot 3 = 9 \equiv 4$. Then
$$x_R = \lambda^2 - x_P - x_Q = 16 - 0 - 2 = 14 \equiv 4, \qquad y_R = \lambda(x_P - x_R) - y_P = 4(0 - 4) - 1 = -17 \equiv 3.$$
So $P + Q = (4, 3)$, which is indeed on the curve ($3^2 = 9 \equiv 4$ and $4^3 + 4 + 1 = 69 \equiv 4$). 

**Why smaller keys.** The discrete-log problem on a well-chosen elliptic curve has no known shortcut faster than generic square-root-time attacks, unlike ordinary mod-$p$ groups where faster index-calculus methods exist. So a 256-bit elliptic-curve key gives security comparable to a 3072-bit RSA key. That efficiency is why elliptic-curve cryptography secures most modern phones, messaging apps, and TLS connections.

### 2.4 Error-correcting codes

**The real problem.** Real channels are noisy: a CD gets scratched, a Wi-Fi packet picks up interference, a probe near Saturn has a weak signal. Bits flip. We want the receiver to not just detect errors but **correct** them without asking for a resend.

**The algebra.** A **binary linear code** is a subspace of $\mathbb{F}_2^n$ (vectors of bits, added mod 2). We describe it two ways:
- a **generator matrix** $G$ whose rows span the code: a message $m$ becomes the codeword $c = mG$;
- a **parity-check matrix** $H$ with $Hc^{\mathsf T} = 0$ for every codeword $c$.

The **Hamming distance** between two words is the number of positions where they differ. A code that keeps all codewords at distance $\geq 3$ can correct any single-bit error, because a corrupted word is still closest to the unique codeword it came from.

**The [7,4] Hamming code, fully worked.** It encodes 4 data bits into 7 bits and corrects any single error. In systematic form $G = [\,I_4 \mid P\,]$ and $H = [\,P^{\mathsf T} \mid I_3\,]$:
$$
G = \begin{pmatrix} 1&0&0&0&1&1&0 \\ 0&1&0&0&1&0&1 \\ 0&0&1&0&0&1&1 \\ 0&0&0&1&1&1&1 \end{pmatrix}, \qquad
H = \begin{pmatrix} 1&1&0&1&1&0&0 \\ 1&0&1&1&0&1&0 \\ 0&1&1&1&0&0&1 \end{pmatrix}.
$$

*Encode* the message $m = (1,0,1,1)$. The first four output bits copy $m$; the last three are parity bits (all sums mod 2):
$$p_5 = m_1 + m_2 + m_4 = 1+0+1 = 0,\quad p_6 = m_1 + m_3 + m_4 = 1+1+1 = 1,\quad p_7 = m_2 + m_3 + m_4 = 0+1+1 = 0.$$
So $c = mG = (1,0,1,1,0,1,0)$.

*Corrupt* it: flip bit 6, giving the received word $r = (1,0,1,1,0,0,0)$.

*Decode* by computing the **syndrome** $s = Hr^{\mathsf T}$ (mod 2). Multiplying $H$ by $r$:
$$s = (0,\,1,\,0).$$
Now compare $s$ to the columns of $H$. Column 6 of $H$ is exactly $(0,1,0)^{\mathsf T}$. A nonzero syndrome equal to column $j$ says "the error is in position $j$," so the error is in position 6. Flip bit 6 back: $r \to (1,0,1,1,0,1,0) = c$. Read off the first four bits: the original message $(1,0,1,1)$ is recovered. (A zero syndrome would mean "no detectable error.")

The reason it works: $H r^{\mathsf T} = H(c + e)^{\mathsf T} = Hc^{\mathsf T} + He^{\mathsf T} = 0 + He^{\mathsf T}$, and for a single-bit error $e$ in position $j$, $He^{\mathsf T}$ is precisely the $j$-th column of $H$. The syndrome literally points at the broken bit.

**Beyond Hamming.** **Reed-Solomon codes** are linear codes over larger finite fields such as $\mathbb{F}_{2^8}$ (256-element symbols, i.e. bytes). Treating data as evaluations of a polynomial over a finite field, they correct whole bursts of errors, which is why they protect CDs, DVDs, Blu-ray discs, QR codes, and NASA deep-space links.

### 2.5 Check digits

**The real problem.** People mistype account numbers and product codes. The two commonest slips are a **single wrong digit** and a **transposition** (swapping two adjacent digits). We want a cheap test that catches these the moment they happen.

**The algebra.** Append a redundant digit so the whole string satisfies a weighted-sum congruence modulo some number. Using a **prime modulus** makes the weights invertible, which is exactly what guarantees both error types are caught.

**ISBN-10 (mod 11), worked.** For digits $d_1 \dots d_{10}$ the rule is
$$\sum_{i=1}^{10} i \, d_i \equiv 0 \pmod{11},$$
with the last digit allowed to be $X = 10$. Take the first nine digits of $0\text{-}306\text{-}40615$, i.e. $0,3,0,6,4,0,6,1,5$. The weighted sum is
$$1\cdot 0 + 2\cdot 3 + 3\cdot 0 + 4\cdot 6 + 5\cdot 4 + 6\cdot 0 + 7\cdot 6 + 8\cdot 1 + 9\cdot 5 = 6 + 24 + 20 + 42 + 8 + 45 = 145 \equiv 2 \pmod{11}.$$
We need $145 + 10 d_{10} \equiv 0$, i.e. $10 d_{10} \equiv -2 \equiv 9 \pmod{11}$. Since $10 \equiv -1$, this is $-d_{10} \equiv 9$, so $d_{10} = 2$. The full ISBN $0\text{-}306\text{-}40615\text{-}2$ checks out: the total is $145 + 20 = 165 = 15 \cdot 11 \equiv 0$.

*Why it catches errors.* If one digit $d_k$ is wrong by $\delta \neq 0$, the sum changes by $k\delta$, and modulo the prime 11 this is never $0$ for $1 \le k \le 10$, so the error shows up. If adjacent digits $d_k, d_{k+1}$ are swapped, the sum changes by $(d_{k+1} - d_k)$, again nonzero mod 11 unless the digits were equal. Concretely, swapping the 3rd and 4th digits of our valid ISBN gives $0,3,6,0,4,\dots$ whose weighted sum is $145 + (6-0)\cdot(\text{net } +1) \not\equiv 0$, and the check fails as it should.

**Others.** **UPC-A** (12 digits) uses weights alternating $3$ and $1$ modulo 10: for $036000291452$, the odd-position sum is $14$, the even-position sum is $16$, and $3\cdot 14 + 16 = 58 \equiv 0 \pmod{10}$ once the check digit $2$ is included, so it is valid (this catches all single-digit errors, though not every transposition, since 10 is not prime). **IBAN** bank numbers move the first four characters to the end, turn letters into numbers, and require the result to be $\equiv 1 \pmod{97}$; for `GB82WEST12345698765432` the reduction is exactly $1$, so it is valid. The big modulus 97 catches the vast majority of errors.

### 2.6 Symmetry in chemistry and physics

**The real problem.** A molecule's symmetry determines which vibrations are infrared-active, whether it has a dipole moment, and how its orbitals combine. Crystals come in a limited number of repeating patterns. And the deepest laws of physics are statements about symmetry. We need a precise language for "looks the same after this transformation."

**The algebra.** The set of symmetry operations of an object (rotations, reflections, inversions that map it to itself) forms a group, with composition as the operation.

**Molecular point groups.** Water $\mathrm{H_2O}$ has symmetry group $C_{2v}$, of order 4: the identity, a $180^\circ$ rotation about the axis through the oxygen, and two mirror planes. Composing the rotation with one mirror gives the other mirror, so the set closes up into a group. Ammonia $\mathrm{NH_3}$ has group $C_{3v}$, of order 6: the identity, two rotations by $\pm 120^\circ$, and three mirror planes through each N-H bond. ($C_{3v}$ is isomorphic to the symmetric group $S_3$, the smallest non-abelian group from doc #1.)

**Crystallographic groups.** Demanding a symmetry pattern that repeats to fill space forces strong restrictions. In two dimensions there are exactly **17 wallpaper groups** (every periodic 2D pattern, every tiling and fabric print, is one of these). In three dimensions there are exactly **230 space groups**, the complete catalogue of crystal symmetries used by every crystallographer.

**Noether's theorem.** This is one of the most beautiful results in physics: every continuous symmetry of a physical system corresponds to a conserved quantity. Invariance under shifts in time gives conservation of energy; invariance under shifts in space gives conservation of momentum; invariance under rotation gives conservation of angular momentum. The symmetries here form continuous (Lie) groups, and the conservation law falls out of the group's structure. Symmetry is not decoration; it is why the fundamental bookkeeping quantities of the universe stay constant.

**Gauge groups of the Standard Model.** The forces of particle physics are encoded by continuous symmetry groups acting on quantum fields: $U(1)$ for electromagnetism, $SU(2)$ for the weak force, and $SU(3)$ for the strong force, often written $U(1) \times SU(2) \times SU(3)$. The entire framework of modern fundamental physics is, at its core, a statement about which group acts on the fields.

### 2.7 The Rubik's Cube as a group

**The real problem.** A scrambled cube has an astronomical number of states. How many, and how do speedcubers design reliable sequences that fix a few pieces without wrecking the rest?

**The algebra.** Each legal move (a face turn) is a permutation of the cube's stickers, and sequences of moves compose. The set of all positions reachable from solved is a group: every move can be undone (its inverse is the reverse turn), composition is associative, and "do nothing" is the identity.

**The order of the group.** The number of reachable configurations is exactly
$$43{,}252{,}003{,}274{,}489{,}856{,}000 = 8! \cdot 3^{7} \cdot 12! \cdot 2^{10}.$$
This factorization is **meaningful**, not random. The four factors count, in order: the $8!$ ways to permute the 8 corner pieces, the $3^7$ ways to twist them (the eighth corner's twist is forced by the other seven), the $12!$ ways to permute the 12 edge pieces, and the $2^{10}$ ways to flip them (the twelfth flip is forced). The divisions by the "last piece is determined" constraints are why $3^8$ and $2^{12}$ shrink to $3^7$ and $2^{10}$, and why you cannot, for example, flip a single edge in isolation. Its prime factorization is $2^{27} \cdot 3^{14} \cdot 5^{3} \cdot 7^{2} \cdot 11$.

**Why commutators.** A **commutator** is a sequence of the form $ABA^{-1}B^{-1}$. If $A$ and $B$ overlap in only a few pieces, their commutator disturbs only those few and returns everything else to where it started. This is the key trick of cube solving: commutators let you build "surgical" moves that, say, cycle three corners and leave all 50-plus other facets untouched. The non-commutativity of the cube group (the fact that $AB \neq BA$) is not a nuisance; it is the resource that makes precise repairs possible.

### 2.8 Counting with Burnside's lemma

**The real problem.** How many genuinely different ways can you color something, when rotations or reflections make some colorings count as "the same"? Think bracelets, dice faces, board-game tiles, or chemical isomers. Naive counting wildly overcounts.

**The algebra.** A symmetry group $G$ acts on the set of all colorings; two colorings are "the same" when one maps to the other. We want the number of **orbits**.

> **Burnside's lemma.** The number of orbits equals the average number of colorings fixed by each group element:
> $$\#\text{orbits} = \frac{1}{|G|} \sum_{g \in G} |\mathrm{Fix}(g)|,$$
> where $\mathrm{Fix}(g)$ is the set of colorings unchanged by $g$.

The practical shortcut: a symmetry $g$ permutes the positions in some cycles, and a coloring is fixed by $g$ exactly when each cycle is a single color. So if $g$ has $c(g)$ cycles and there are $k$ colors, $|\mathrm{Fix}(g)| = k^{c(g)}$.

**Worked example 1: necklaces, 4 beads, 2 colors, rotations only.** The group is the cyclic group $C_4 = \{e, r, r^2, r^3\}$. Count cycles of each rotation acting on 4 positions:
- $e$: every bead is its own cycle, $4$ cycles, fixes $2^4 = 16$.
- $r$ (rotate one step): one 4-cycle, $1$ cycle, fixes $2^1 = 2$.
- $r^2$ (rotate two steps): two 2-cycles, $2$ cycles, fixes $2^2 = 4$.
- $r^3$: one 4-cycle, fixes $2^1 = 2$.

$$\#\text{orbits} = \frac{16 + 2 + 4 + 2}{4} = \frac{24}{4} = 6.$$
There are **6** distinct necklaces. You can list them by hand to confirm: all-black; all-white; one black; one white; two black adjacent; two black opposite. Six.

**Worked example 2: square corners, rotations and reflections.** Now the group is the dihedral group $D_4$ of order 8: four rotations and four reflections. Acting on the 4 corners of a square, the cycle counts are:
- identity: $4$ cycles;
- two $90^\circ$ rotations ($r, r^3$): one 4-cycle each, $1$ cycle;
- $180^\circ$ rotation ($r^2$): two 2-cycles, $2$ cycles;
- two reflections through opposite corners: each fixes 2 corners and swaps the other two, $3$ cycles;
- two reflections through edge midpoints: two 2-cycles each, $2$ cycles.

So for $k$ colors the count is
$$\frac{k^4 + 2k^1 + k^2 + 2k^3 + 2k^2}{8} = \frac{k^4 + 2k^3 + 3k^2 + 2k}{8}.$$
With $k = 2$: $(16 + 16 + 12 + 4)/8 = 48/8 = 6$ distinct colorings. With $k = 3$: $(81 + 54 + 27 + 6)/8 = 168/8 = 21$. Both are confirmable by direct enumeration.

### 2.9 A fun one: music theory

**The real problem.** Western music groups the infinitely many pitches into 12 **pitch classes** (C, C#, D, ..., B) that repeat every octave. Composers transpose melodies (shift them up or down) and invert them (flip them upside down). Is there structure here?

**The algebra.** Label the pitch classes $0$ through $11$, i.e. $\mathbb{Z}_{12}$. The two basic operations are:
- **Transposition** $T_n: x \mapsto x + n \pmod{12}$ (shift by $n$ semitones);
- **Inversion** $I_n: x \mapsto n - x \pmod{12}$ (flip around a center).

The 12 transpositions and 12 inversions together form a group of order 24, acting on pitch classes (and on chords, which are just subsets). This group is the **dihedral group $D_{12}$**, the very same symmetry group as a regular 12-gon. Transpositions are its rotations; inversions are its reflections.

**Worked example.** The C major triad is $\{C, E, G\} = \{0, 4, 7\}$.
- Transpose up a perfect fourth, $T_5$: $\{0+5, 4+5, 7+5\} = \{5, 9, 0\} = \{F, A, C\}$, the F major triad. Transposition just relabels the same chord shape at a new pitch.
- Invert about $0$, $I_0: x \mapsto -x$: $\{0, -4, -7\} = \{0, 8, 5\} = \{C, G\sharp, F\}$, which is the **F minor** triad. Inversion turns major into minor.

A neat structural fact, easy to verify: composing two inversions gives a transposition, $I_a \circ I_b = T_{a-b}$. (Check: $I_a(I_b(x)) = a - (b - x) = (a - b) + x$.) This is exactly the dihedral relation "reflection times reflection equals rotation," now heard as music.

## 3. Basic exercises

1. **Diffie-Hellman.** With $p = 23$, $g = 5$, suppose Alice's secret is $a = 4$ and Bob's public value is $B = 19$. Compute Alice's view of the shared secret $B^a \bmod 23$.
2. **RSA encrypt.** Using the public key $(n, e) = (55, 3)$ from the text, encrypt the message $m = 2$.
3. **RSA decrypt.** With $d = 27$ and $n = 55$, you receive ciphertext $c = 8$. Recover $m$. (Hint: it should match the previous answer.)
4. **ISBN check digit.** Find the ISBN-10 check digit for the first nine digits $1,4,9,1,9,8,9,3,8$.
5. **UPC verify.** Are the 12 digits $0,1,2,0,0,0,0,0,0,0,0,5$ a valid UPC-A code? Use weights $3,1,3,1,\dots$ and modulus 10.
6. **Orbit / necklaces.** Using Burnside, count the distinct necklaces with **3** beads in **2** colors under rotation (group $C_3$).

### Solutions

1. Compute $19^4 \bmod 23$. From the text, $19^2 \equiv 16$, so $19^4 = (19^2)^2 \equiv 16^2 = 256 = 11\cdot 23 + 3 \equiv 3$. Alice's shared value is $\mathbf{3}$. (Indeed $g^{ab} = 5^{4\cdot 15}$ would also reduce to 3 for Bob.)
2. $c = 2^3 \bmod 55 = 8$. Ciphertext $\mathbf{8}$.
3. $m = 8^{27} \bmod 55$. By the round-trip property, $8^{27} \equiv 2$ (it undoes exercise 2). Message $\mathbf{2}$.
4. Weighted sum of $1,4,9,1,9,8,9,3,8$: $1\cdot1 + 2\cdot4 + 3\cdot9 + 4\cdot1 + 5\cdot9 + 6\cdot8 + 7\cdot9 + 8\cdot3 + 9\cdot8 = 1+8+27+4+45+48+63+24+72 = 292$. Now $292 = 26\cdot 11 + 6$, so $292 \equiv 6 \pmod{11}$. Need $292 + 10 d_{10} \equiv 0$, i.e. $-d_{10} \equiv -6$, so $d_{10} = \mathbf{6}$. (This is the real ISBN $1\text{-}491989\text{-}38\text{-}6$ pattern: total $292 + 60 = 352 = 32\cdot 11$.)
5. Odd-position digits (1st, 3rd, ..., 11th): $0,2,0,0,0,0$, sum $2$. Even-position digits (2nd, 4th, ..., 12th): $1,0,0,0,0,5$, sum $6$. Total $3\cdot 2 + 6 = 12 \equiv 2 \pmod{10}$. Since this is **not** $0$, the code is **invalid**.
6. $C_3 = \{e, r, r^2\}$ on 3 positions. Cycles: $e$ has 3 cycles ($2^3 = 8$ fixed); $r$ is one 3-cycle ($2^1 = 2$); $r^2$ is one 3-cycle ($2$). Orbits $= (8 + 2 + 2)/3 = 12/3 = \mathbf{4}$. (The four: all-black, all-white, two-black-one-white, one-black-two-white.)

## 4. Advanced exercises

1. **Hamming syndrome decoding.** Using the parity-check matrix $H$ from section 2.4, you receive $r = (1,1,1,1,0,1,0)$. Compute the syndrome, locate any single-bit error, correct it, and read off the 4 data bits.
2. **Burnside, full dihedral necklaces.** Count the distinct bracelets with **4** beads in **3** colors when both rotations **and** reflections are allowed (group $D_4$, order 8). Use the cycle-count formula from section 2.8.
3. **Small Diffie-Hellman with a fresh check.** With $p = 23$, $g = 5$, Alice's secret $a = 6$, Bob's secret $b = 3$: compute both public values and verify both parties reach the same shared secret.
4. **Build a Hamming codeword from scratch.** Encode the 4-bit message $m = (1,1,0,0)$ with the generator matrix $G$ of section 2.4. Give the full 7-bit codeword, then state its Hamming distance from the all-zeros codeword.
5. **Elliptic-curve doubling.** On $y^2 = x^3 + x + 1$ over $\mathbb{F}_5$, compute $2P$ for $P = (2,1)$ using the tangent (doubling) formula $\lambda = (3x_1^2 + a)/(2y_1)$.

### Solutions

1. Multiply $H$ by $r = (1,1,1,1,0,1,0)$ over $\mathbb{F}_2$.
   - Row 1 $(1,1,0,1,1,0,0)\cdot r = 1+1+0+1+0+0+0 = 3 \equiv 1$.
   - Row 2 $(1,0,1,1,0,1,0)\cdot r = 1+0+1+1+0+1+0 = 4 \equiv 0$.
   - Row 3 $(0,1,1,1,0,0,1)\cdot r = 0+1+1+1+0+0+0 = 3 \equiv 1$.
   
   Syndrome $s = (1,0,1)^{\mathsf T}$. This equals **column 2** of $H$, so the error is in position 2. Flip it: $r \to (1,0,1,1,0,1,0)$. The first four bits give the data $\mathbf{(1,0,1,1)}$. (This is the same codeword as the worked example, recovered from a different single error.)
2. Using $\dfrac{k^4 + 2k^3 + 3k^2 + 2k}{8}$ with $k = 3$: numerator $= 81 + 2\cdot 27 + 3\cdot 9 + 2\cdot 3 = 81 + 54 + 27 + 6 = 168$, so $168/8 = \mathbf{21}$ distinct bracelets.
3. Alice sends $A = 5^6 \bmod 23 = 8$ (as in the text). Bob sends $B = 5^3 \bmod 23$: $5^3 = 125 = 5\cdot 23 + 10 \equiv 10$, so $B = 10$. Alice computes $B^a = 10^6 \bmod 23$; Bob computes $A^b = 8^3 \bmod 23$. Check Bob's: $8^3 = 512 = 22\cdot 23 + 6 \equiv 6$. Check Alice's: $10^2 = 100 \equiv 8$, so $10^6 = (10^2)^3 \equiv 8^3 \equiv 6$. Both get $\mathbf{6}$, matching $g^{ab} = 5^{18}$.
4. With $m = (1,1,0,0)$: the first four bits are $1,1,0,0$, and the parity bits are $p_5 = m_1+m_2+m_4 = 1+1+0 = 0$, $p_6 = m_1+m_3+m_4 = 1+0+0 = 1$, $p_7 = m_2+m_3+m_4 = 1+0+0 = 1$. Codeword $c = \mathbf{(1,1,0,0,0,1,1)}$. It has four 1s, so its Hamming distance from $(0,0,0,0,0,0,0)$ is $\mathbf{4}$. (Every nonzero codeword of this code has weight $\geq 3$, consistent with single-error correction.)
5. For $P = (2,1)$ with $a = 1$: $\lambda = \dfrac{3\cdot 2^2 + 1}{2\cdot 1} = \dfrac{13}{2} \equiv \dfrac{3}{2} \pmod 5$. Since $2^{-1} = 3$, $\lambda = 3\cdot 3 = 9 \equiv 4$. Then $x_3 = \lambda^2 - 2x_1 = 16 - 4 = 12 \equiv 2$, and $y_3 = \lambda(x_1 - x_3) - y_1 = 4(2 - 2) - 1 = -1 \equiv 4$. So $2P = \mathbf{(2, 4)}$, which is on the curve ($4^2 = 16 \equiv 1$ and $2^3 + 2 + 1 = 11 \equiv 1$).

## 5. Where to go deeper

- **Cryptography:** Hoffstein, Pipher, and Silverman, *An Introduction to Mathematical Cryptography*, for RSA, Diffie-Hellman, and elliptic curves with full proofs.
- **Coding theory:** Hill, *A First Course in Coding Theory*, or van Lint, *Introduction to Coding Theory*, for linear, Hamming, and Reed-Solomon codes.
- **Symmetry in science:** Cotton, *Chemical Applications of Group Theory*, for point groups; any modern particle-physics text for gauge groups and Noether's theorem.
- **Combinatorics:** any text covering Burnside's lemma and Polya enumeration (the cycle-index generalization).
- **Recreational:** Joyner, *Adventures in Group Theory*, for the Rubik's Cube treated rigorously as a group.

## 6. Common pitfalls & misconceptions

- **Discrete log is not just "taking a logarithm."** Over the integers, logarithms are easy; the security comes from doing it inside a finite group, where no efficient method is known.
- **RSA needs $\gcd(m, n) = 1$ in the clean proof**, but the round-trip still holds for all $m$ by the Chinese Remainder Theorem; just do not panic if a message shares a factor with $n$ (in practice messages are padded and $n$ is huge).
- **A check digit detects errors; it does not correct them.** Detection (does it pass?) and correction (which bit is wrong?) are different jobs. Hamming codes correct; ISBN/UPC only detect.
- **Modulus matters.** ISBN uses the prime 11, which is why it catches every single-digit and adjacent-transposition error; UPC's modulus 10 is not prime, so it misses some transpositions.
- **Burnside averages over the whole group, including the identity.** Forgetting the identity term (which contributes $k^{(\text{number of positions})}$) is the most common mistake; so is using only rotations when reflections also count.
- **"Symmetry" means an operation that leaves the object unchanged**, not merely that the object "looks symmetric." Always check the set of operations forms a group (closure and inverses).
- **The cube group is non-abelian, and that is a feature.** If moves commuted, commutators would be trivial and surgical edits impossible.
- **Field versus group.** Cryptography and codes lean on the field property (division by nonzeros). $\mathbb{Z}_n$ is a field only when $n$ is prime; for composite $n$, $(\mathbb{Z}/n\mathbb{Z})^\times$ is still a group, but not every nonzero element is invertible.

## 7. Recap of the whole series

We began with the language of sets, maps, and operations (doc #0), built up groups as the mathematics of symmetry and reversible action (docs #1-#2), added a second operation to reach rings (doc #3), and demanded division to arrive at fields and the elegant theory of finite fields and Galois symmetry (doc #4). This final document closed the loop: the cyclic groups of doc #2 secure your messages, the finite fields of doc #4 repair your data, the group actions of doc #2 count and classify, and continuous symmetry groups underwrite the laws of physics. Abstract algebra is abstract precisely so that one set of ideas can serve all of these at once, which is exactly why it is worth learning.
