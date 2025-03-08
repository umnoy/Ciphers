from sympy import Matrix
import numpy as np
import re
from math import gcd

while True:
    try:
        lang = int(input("Choose a language (1 - Russian, 2 - English): "))
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
    raise ValueError(f"Determinant {a} has no inverse modulo {m}. Your text might be too short, try another one.")


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
        text = input('Enter the plaintext: ')
        text = text.lower()
        text = re.sub(r"[\s\d\W]+", "", text)

        cipher = input('Enter the ciphertext: ')
        cipher = cipher.lower()
        cipher = re.sub(r"[\s\d\W]+", "", cipher)

        if len(text) != len(cipher):
            raise ValueError

        if not text and not cipher:
            raise IndexError
        else:
            break
    
    except ValueError:
        print('Plaintext and ciphertext lengths do not match, please enter them again!')
    except IndexError:
        print('You did not enter plaintext and ciphertext')


while True:
    try:
        block_size = int(input("Enter the text block size: "))
        if block_size > len(text) or block_size <= 1:
            raise Exception
        else: 
            break
    except Exception:
        print(f'Block size is larger than the message length ({len(text)}) or you entered an incorrect format')

if len(text) % block_size != 0:
            while len(text) % block_size != 0:
                text += alphabet_low[0]
                cipher += alphabet_low[0]

blocks = stroke_to_blocks(text, block_size)
cipher_blocks = stroke_to_blocks(cipher, block_size)

def find_right(block_size):
    keys = []
    for i in range(block_size - 1, len(blocks)):
        if i >= block_size - 1:
            plaintext_matrix = np.array([blocks[i - j] for j in range(block_size - 1, -1, -1)])
            det_val = np.linalg.det(plaintext_matrix)
            if isinstance(det_val, np.ndarray):
                det = int(np.round(det_val.item()))
            else:
                det = int(np.round(det_val))

            if gcd(det, alphabet_size) == 1:
                try:
                    inv_plaintext_matrix = find_inv_key(plaintext_matrix, alphabet_size)
                    cipher_matrix = np.array([cipher_blocks[i - j] for j in range(block_size - 1, -1, -1)])
                    key = (np.dot(inv_plaintext_matrix, cipher_matrix) % 26).T
                    keys.append((key, i))
                except Exception as e:
                    print(f"Failed to compute key for block {i}: {e}")
    return keys

keys = find_right(block_size)
unique_keys = {tuple(map(tuple, key[0])) for key in keys}

for key in keys:
    print(f'Possible key for block {key[1]}:')
    print(key[0])
