# 1. Substitution Cipher

**Analogy:** Imagine a decoder ring from a cereal box, where every letter of the alphabet is swapped for a different symbol or letter on a fixed wheel. If "A" maps to "D" on the ring, every single "A" in your message always becomes "D." Anyone with an identical ring can set it the same way and read the message.

**Real-world use case:** Pure substitution isn't used for real security today (it's broken by frequency analysis), but its descendants are everywhere. ROT13 is used informally online to hide spoilers or puzzle answers. More importantly, the *idea* of substitution — replacing one symbol with another via a lookup table — is the conceptual ancestor of the S-boxes used inside modern ciphers like AES and Blowfish.

**Algorithm (Caesar-style, simplest form):**
1. Choose a shift key *k* (e.g., k = 3).
2. For each letter in the plaintext, find its position in the alphabet (A=0 ... Z=25).
3. Add *k* to that position, then take the result mod 26, to "wrap around" past Z.
4. The letter at that new position is the ciphertext letter.
5. To decrypt, subtract *k* instead of adding, then mod 26 again.

---

# 2. Transposition Cipher

**Analogy:** Think of writing a sentence on a sheet of graph paper, one letter per box, filling in rows left to right. Now, instead of reading it back row by row, you read it column by column in a different order. The *letters themselves never change* — only their *positions* are scrambled, like shuffling a deck of cards without replacing any of them.

**Real-world use case:** Historically used by military and diplomatic services (the WWI German ADFGVX cipher combined substitution and transposition). Today, pure transposition isn't used alone for security, but the general principle — rearranging data blocks rather than changing their values — appears in parts of block cipher design and in some interleaving/permutation steps of modern cryptographic algorithms.

**Algorithm (Columnar Transposition):**
1. Choose a keyword or key sequence of numbers (e.g., `3142`), whose length sets the number of columns.
2. Write the plaintext into a grid, row by row, under the key, padding the last row with filler letters if needed.
3. Number the columns according to the alphabetical/numerical order of the key.
4. Read the grid out column by column, starting with column "1," then "2," and so on.
5. To decrypt, rebuild the grid using the ciphertext length and key, filling columns in key order, then read row by row.

---

# 3. Rail Fence Cipher

**Analogy:** Picture writing your message on a zigzagging fence made of a few horizontal rails, like a sound wave going down-up-down-up. You write one letter per rail as you move diagonally, bouncing between the top and bottom rails. To read the hidden message, someone just needs to know how many rails you used.

**Real-world use case:** Mostly a teaching tool today — it's one of the simplest transposition ciphers and is a common stepping stone in cryptography courses. It's also used in puzzle/escape-room design and CTF ("Capture The Flag") beginner challenges, since it's easy to implement but illustrates the transposition concept clearly.

**Algorithm:**
1. Choose the number of rails, *r*.
2. Write the plaintext diagonally across the rails, moving down from rail 1 to rail *r*, then back up to rail 1, repeating this zigzag for the whole message.
3. Read the letters off rail 1 first, then rail 2, and so on down to rail *r*, concatenating them.
4. That concatenation is the ciphertext.
5. To decrypt, recreate the zigzag *pattern* (which positions belong to which rail), figure out how many letters land on each rail, slot the ciphertext letters into those rail positions, and read off the zigzag path to recover the plaintext.

---

# 4. Diffie–Hellman Key Exchange

**Analogy:** Imagine two people, Alice and Bob, who want to agree on a secret paint color, but can only communicate by shouting across a crowded room (public channel). They publicly agree on a common base color, say yellow. Alice privately mixes in her own secret color and shows the *result* (not her secret) to Bob. Bob does the same, mixing his own secret into the yellow and showing *his* result to Alice. Each of them now takes the other's public mixture and mixes in their own private secret again. Mixing paint is easy, but *un-mixing* it to find someone's original secret color is essentially impossible. Both of them land on the exact same final color, even though no one watching ever saw the full recipe. That final shared color is the secret key.

**Real-world use case:** Diffie–Hellman (or its elliptic-curve variant, ECDH) is used every time you load an HTTPS website. It's the mechanism that lets your browser and a server, who have never met before, agree on a shared encryption key over the open internet without ever transmitting the key itself. It's also used in VPN protocols (IPSec) and secure messaging apps like Signal.

**Algorithm:**
1. Publicly agree on a large prime *p* and a base (generator) *g*.
2. Alice picks a private secret *a* and computes her public value A = gᵃ mod p.
3. Bob picks a private secret *b* and computes his public value B = gᵇ mod p.
4. Alice and Bob exchange A and B openly (an eavesdropper can see both).
5. Alice computes the shared key as K = Bᵃ mod p.
6. Bob computes the shared key as K = Aᵇ mod p.
7. Both arrive at the same K, because (gᵇ)ᵃ = (gᵃ)ᵇ = g^(ab) mod p. The eavesdropper, seeing only g, p, A and B, cannot efficiently compute K — this difficulty is called the discrete logarithm problem.

---

# 5. RSA Algorithm

**Analogy:** Think of a padlock that anyone can snap shut, but only you have the key to open. You hand out open padlocks (your public key) to anyone who wants to send you something secret — they put their message in a box, snap your padlock shut, and mail it. Only you, holding the private key, can unlock it. Even the sender can't reopen the box once it's locked, because locking and unlocking use mathematically related but practically irreversible operations: multiplying two huge prime numbers is easy, but figuring out the original primes from their product alone is extremely hard.

**Real-world use case:** RSA secures HTTPS certificates (though key exchange has largely shifted to Diffie–Hellman/ECDH for speed, RSA is still widely used for digital signatures and certificate authentication), SSH authentication, PGP/GPG email encryption, and code-signing for software updates.

**Algorithm:**
1. **Key generation:** pick two large prime numbers *p* and *q*. Compute n = p × q (this becomes part of both keys) and φ(n) = (p−1)(q−1).
2. Choose a public exponent *e* such that 1 < e < φ(n) and gcd(e, φ(n)) = 1 (commonly e = 65537).
3. Compute the private exponent *d*, the modular inverse of *e* mod φ(n), i.e., the value satisfying e·d ≡ 1 (mod φ(n)).
4. The public key is (e, n); the private key is (d, n). *p*, *q* and φ(n) are discarded/kept secret.
5. **Encryption:** convert the message to a number M (smaller than n), then compute ciphertext C = Mᵉ mod n.
6. **Decryption:** compute M = Cᵈ mod n, which recovers the original message using the private key.
7. Security relies on the fact that factoring n back into p and q is computationally infeasible for sufficiently large primes (2048 bits or more in practice).

---

# 6. Blowfish

**Analogy:** Picture an assembly line with 16 identical scrambling stations in a row (rounds). At each station, half of your data is mixed up using a secret lookup table (like a substitution cipher on steroids) and combined with the other half, then the two halves swap places before moving to the next station. Before any scrambling happens, though, there's a lengthy, expensive setup phase where the secret key is used to *build* those lookup tables from scratch — like custom-forging all the tools on the assembly line before using them, which is deliberately slow to make brute-force key guessing expensive.

**Real-world use case:** Blowfish was designed by Bruce Schneier in 1993 as a fast, free, unpatented alternative to DES. It's still found in some older VPN and SSH implementations, backup/archive tools, and famously underlies the `bcrypt` password-hashing function (which exploits Blowfish's slow key-setup phase specifically to make password-cracking attempts slow). It has mostly been succeeded by AES for new designs, mainly because its 64-bit block size is now considered too small for very large data volumes.

**Algorithm:**
1. **Key setup (done once per key):** initialize the P-array (18 subkeys) and four S-boxes (256 entries each) with fixed constants (digits of π). XOR the key, repeated as needed, into the P-array.
2. Encrypt an all-zero block with the current P-array/S-boxes, and use the output to replace the first two P-array entries. Repeat this process, each time encrypting the latest output, until every P-array and S-box entry has been replaced. This "bootstraps" key-dependent tables and is why Blowfish's setup is comparatively slow.
3. **Encryption of a 64-bit block:** split the block into two 32-bit halves, L and R.
4. For 16 rounds: XOR L with the round's P-array subkey, pass the result through the F-function (which splits L into 4 bytes, looks each up in an S-box, combines them with addition/XOR), XOR that output into R, then swap L and R.
5. After the 16th round, undo the final swap and XOR in the last two P-array entries.
6. **Decryption** uses the exact same process, but with the P-array subkeys applied in reverse order.