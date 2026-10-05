import random
from math import gcd

def gen_prime(bits=256):
    while True:
        n = random.getrandbits(bits) | (1 << bits - 1) | 1       # random odd number
        if all(pow(random.randrange(2, n - 1), n - 1, n) == 1 for _ in range(10)):
            return n                                              # passed Fermat test

p, q = gen_prime(), gen_prime()
n = p * q
phi = (p - 1) * (q - 1)
e = 65537
while gcd(e, phi) != 1:
    p, q = gen_prime(), gen_prime()
    n, phi = p * q, (p - 1) * (q - 1)
d = pow(e, -1, phi)                 # private key (Python 3.8+)

msg = "Hello RSA"
m = int.from_bytes(msg.encode(), "big")
c = pow(m, e, n)
dec = pow(c, d, n).to_bytes((n.bit_length() + 7) // 8, "big").lstrip(b"\0").decode()

print("Cipher:", c)
print("Plain :", dec)