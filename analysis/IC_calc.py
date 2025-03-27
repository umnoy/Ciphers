from collections import Counter
import re
import matplotlib.pyplot as plt

def index_of_coincidence(text):
    
    text = text.upper()  
    frequency = Counter(text)
    N = len(text)  
    
    if N < 2:
        return 0
    
    ic = sum(f * (f - 1) for f in frequency.values()) / (N * (N - 1))
    return ic

def IC_for_blocks(text, key_length):
    
    blocks = ['']*key_length
    for i in range(len(text)):
        blocks[i % key_length] += text[i]

    ic_values = [index_of_coincidence(block) for block in blocks if len(block) > 1]
    return sum(ic_values) / len(ic_values) if ic_values else 0



while True:
    try:
        text = input('Enter ciphertext: ')
        if text:
            break
        else:
            raise Exception
    except Exception:
        print("You enterned an empty string!")


text = re.sub(r"[\s\d\W]+", "", text)

max_key_length = min(50, len(text) // 2)
key_lengths = list(range(1, max_key_length))
ic_values = [IC_for_blocks(text, k) for k in key_lengths]

plt.figure(figsize=(10, 5))
plt.plot(key_lengths, ic_values, marker='o', linestyle='-')
plt.xlabel("Key length")
plt.ylabel("Index of Coincidence")
plt.title("Determining the key length using the Index of Coincidence")
plt.grid()
plt.show()