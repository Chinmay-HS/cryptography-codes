from string import ascii_uppercase as ABC

key = "QWERTYUIOPASDFGHJKLZXCVBNM"   # substitution key (shuffled alphabet)
text = "ATTACKATDAWN"

# Substitution
enc = "".join(key[ABC.index(ch)] for ch in text)
dec = "".join(ABC[key.index(ch)] for ch in enc)
print("Substitution:", enc, "->", dec)

# Transposition (write in rows of 4, read columns)
n = 4
text2 = "ATTACKATDAWN"
cols = [text2[i::n] for i in range(n)]
enc2 = "".join(cols)
rows = len(text2) // n
dec2 = "".join(enc2[c * rows + r] for r in range(rows) for c in range(n))
print("Transposition:", enc2, "->", dec2)