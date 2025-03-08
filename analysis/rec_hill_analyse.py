from sympy import Matrix
import numpy as np
import re
from math import gcd

while True:
    try:
        lang = int(input("Choose language (1 - Russian, 2 - English): "))
        if lang == 1:
            alphabet_low = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
            alphabet_size = 33
            break
        if lang == 2:
            alphabet_low = 'abcdefghijklmnopqrstuvwxyz'
            alphabet_size = 26
            break
        else: 
            raise Exception
    except Exception:
        print('You need to choose 1 or 2!')

def find_inv(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"Determinant {a} has no inverse modulo {m}. Maybe your text is too short, try another one.")

def find_inv_key(key, alphabet_size):
    det = int(round(np.linalg.det(key))) 
    det_mod = det % alphabet_size

    inv_det = find_inv(det_mod, alphabet_size)
    matrix = Matrix(key)
    adjugate_matrix = matrix.adjugate()
    inv_matrix = (inv_det * adjugate_matrix) % alphabet_size

    return np.array(inv_matrix, dtype=int)

def stroke_to_blocks(message, block_size):
    indexes = []
    for char in message:
        indexes.append(alphabet_low.find(char))
    
    blocks = [indexes[i:i+block_size] for i in range(0, len(indexes), block_size)]
    return blocks

def blocks_to_stroke(blocks):
    result = ''
    indexes = sum(blocks, [])
    for index in indexes:
        result += alphabet_low[index]
    return result


while True:
    try:
        text_1 = input('Enter the first plaintext: ')
        text_1 = text_1.lower()
        text_1 = re.sub(r"[\s\d\W]+", "", text_1)

        cipher_1 = input('Enter the first ciphertext: ')
        cipher_1 = cipher_1.lower()
        cipher_1 = re.sub(r"[\s\d\W]+", "", cipher_1)

        text_2 = input('Enter the second plaintext: ')
        text_2 = text_2.lower()
        text_2 = re.sub(r"[\s\d\W]+", "", text_2)

        cipher_2 = input('Enter the second ciphertext: ')
        cipher_2 = cipher_2.lower()
        cipher_2 = re.sub(r"[\s\d\W]+", "", cipher_2)

        if len(text_1) != len(cipher_1):
            num = 'first'
            raise ValueError
        
        if len(text_2) != len(cipher_2):
            num = 'second'
            raise ValueError
        
        if not text_1 and not cipher_1 and not text_2 and not cipher_2:
            raise IndexError
        else:
            break
    
    except ValueError:
        print(f'The length of the {num} plaintext and {num} ciphertext are different, please enter them again!')
    except IndexError:
        print('You did not enter the plaintexts and ciphertexts')

while True:
    try:
        block_size = int(input("Enter the block size for dividing the text: "))
        for text in text_1, text_2:
            if block_size > len(text) or block_size <= 1:
                raise Exception
        break
    except Exception:
        print(f'The block size is greater than the length of the message ({len(text)}) or you entered incorrect data')

for text in text_1, text_2:
    if len(text) % block_size != 0:
                while len(text) % block_size != 0:
                    text += alphabet_low[0]
for cipher in cipher_1, cipher_2:
    if len(cipher) % block_size != 0:
                while len(cipher) % block_size != 0:
                    cipher += alphabet_low[0]

plaintext_blocks_1 = stroke_to_blocks(text_1, block_size)
cipher_blocks_1 = stroke_to_blocks(cipher_1, block_size)
plaintext_blocks_2 = stroke_to_blocks(text_2, block_size)
cipher_blocks_2 = stroke_to_blocks(cipher_2, block_size)

def find_right(block_size, block_1, block_2, cipher_blocks_1, cipher_blocks_2):
    keys = []
    for i in 0,1:
        plaintext_matrix = np.array([block_1[i], block_2[i]])
        det_val = np.linalg.det(plaintext_matrix)
        if isinstance(det_val, np.ndarray):
            det = int(np.round(det_val.item()))
        else:
            det = int(np.round(det_val))

        if gcd(det, alphabet_size) == 1:
            try:
                inv_plaintext_matrix = find_inv_key(plaintext_matrix, alphabet_size)
                cipher_matrix = np.array([cipher_blocks_1[i], cipher_blocks_2[i]])
                key = (np.dot(inv_plaintext_matrix, cipher_matrix) % 26).T
                keys.append((key, i))
            except Exception as e:
                print(f"Failed to compute the key for block {i}: {e}")
    return keys

keys = find_right(block_size, plaintext_blocks_1, plaintext_blocks_2, cipher_blocks_1, cipher_blocks_2)

for key in keys:
    print(f'Possible key for block {key[1]}:')
    print(key[0])
