M = 0xFFFFFFFF

def arctan(x, one):                      # used to compute pi
    t = total = one // x
    k = 1
    while t:
        t //= x * x
        k += 2
        total += (-1) ** ((k - 1) // 2) * (t // k)
    return total

# Blowfish's tables are just the hex digits of pi (1042 words of 32 bits)
BITS = 1042 * 32 + 64
one = 1 << BITS
pi = 4 * (4 * arctan(5, one) - arctan(239, one))
frac = pi - 3 * one
words = [(frac >> (BITS - 32 * (i + 1))) & M for i in range(1042)]
P_INIT, S_INIT = words[:18], words[18:]

def block(L, R, P, S):                   # encrypt one 64-bit block
    for i in range(16):
        L ^= P[i]
        a, b, c, d = L >> 24, (L >> 16) & 255, (L >> 8) & 255, L & 255
        R ^= ((((S[a] + S[256 + b]) & M) ^ S[512 + c]) + S[768 + d]) & M
        L, R = R, L
    L, R = R, L
    return L ^ P[17], R ^ P[16]

def make_keys(key):
    P = [P_INIT[i] ^ int.from_bytes(bytes(key[(4*i + j) % len(key)] for j in range(4)), "big")
         for i in range(18)]
    S = S_INIT[:]
    L = R = 0
    for table in (P, S):                 # fill P then S by encrypting zeros repeatedly
        for i in range(0, len(table), 2):
            L, R = block(L, R, P, S)
            table[i], table[i + 1] = L, R
    return P, S

def blowfish(data, key, decrypt=False):  # data length must be multiple of 8
    P, S = make_keys(key)
    if decrypt:
        P.reverse()
    out = b""
    for i in range(0, len(data), 8):
        L = int.from_bytes(data[i:i+4], "big")
        R = int.from_bytes(data[i+4:i+8], "big")
        L, R = block(L, R, P, S)
        out += L.to_bytes(4, "big") + R.to_bytes(4, "big")
    return out

key = b"secretkey"
text = b"HELLOWORLD"
text += b" " * (-len(text) % 8)
enc = blowfish(text, key)
print(enc.hex())
print(blowfish(enc, key, True))