def pattern(n, rails):                   # which rail each letter lands on
    p, r, d = [], 0, 1
    for _ in range(n):
        p.append(r)
        if r == 0: d = 1
        if r == rails - 1: d = -1
        r += d
    return p

def encrypt(text, rails):
    p = pattern(len(text), rails)
    return "".join(text[i] for r in range(rails) for i in range(len(text)) if p[i] == r)

def decrypt(cipher, rails):
    p = pattern(len(cipher), rails)
    order = [i for r in range(rails) for i in range(len(cipher)) if p[i] == r]
    out = [""] * len(cipher)
    for ch, i in zip(cipher, order):
        out[i] = ch
    return "".join(out)

c = encrypt("WEAREDISCOVEREDRUNATONCE", 3)
print(c, decrypt(c, 3))