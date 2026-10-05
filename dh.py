import secrets, hashlib

p = 2**521 - 1                      # large public prime
g = 3                               # public base

a = secrets.randbelow(p - 3) + 2    # Alice's private key
b = secrets.randbelow(p - 3) + 2    # Bob's private key
A, B = pow(g, a, p), pow(g, b, p)   # public keys (exchanged openly)

# Both sides compute the same secret, then hash it into a 256-bit key
key_a = hashlib.sha256(str(pow(B, a, p)).encode()).digest()
key_b = hashlib.sha256(str(pow(A, b, p)).encode()).digest()
print("Keys match:", key_a == key_b)

# Alice encrypts with XOR, Bob decrypts with his key (message must be under 32 bytes)
msg = b"Hello Bob!"
cipher = bytes(m ^ k for m, k in zip(msg, key_a))
print("Encrypted:", cipher.hex())
print("Decrypted:", bytes(c ^ k for c, k in zip(cipher, key_b)).decode())