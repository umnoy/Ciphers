import numpy as np
from math import gcd
import re
from sympy import Matrix

alf_ru = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
alf_rum = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
alf_en = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alf_enm = 'abcdefghijklmnopqrstuvwxyz'


def generate_key(size_sq, alphabet_len):
    size = size_sq
    n = alphabet_len

    while True:
        matrix = np.random.randint(1, n, (size, size))
        determ = int(np.round(np.linalg.det(matrix)))
        if gcd(n, determ) == 1:
            return matrix


def spaces_and_symbols(message):
    chars = []
    indexes = []

    for index, char in enumerate(message):
        if char not in alphabet_low and char not in alphabet:
            chars.append(char)
            indexes.append(index)
        
    message = re.sub(r"[\s\d\W]+", "", message)
    
    return message, chars, indexes


def upper_letters(message):
    upper = []

    for index, char in enumerate(message):
        if char in alphabet:
            upper.append(index)

    return message.lower(), upper


def return_everything(message, chars, indexes, upper):
    
    for upper_letter in upper:
        message = message[:upper_letter] + alphabet[alphabet_low.find(message[upper_letter])] + message[upper_letter + 1:]
    
    for i in range(len(chars)):
        message = message[:indexes[i]] + chars[i] + message[indexes[i]:]
    
    return message


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


def encrypt(message, keys, block_size):
    result = []
    blocks = stroke_to_blocks(message, block_size)
    keys = generate_keys_massive(keys, blocks)

    for i in range(len(blocks)):
        block = np.array(blocks[i]).T
        encrypted_block = np.dot(keys[i], blocks[i]).T % len(alphabet_low) 
        result.append(encrypted_block)
    
    result = [arr.tolist() for arr in result]
    result = blocks_to_stroke(result)

    return result


def find_inv(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"Determinant {a} does not have an inverse modulo {m}")


def find_inv_key(key, alphabet_size):
    det = int(round(np.linalg.det(key))) 
    det_mod = det % alphabet_size

    inv_det = find_inv(det_mod, alphabet_size)
    matrix = Matrix(key)
    adjugate_matrix = matrix.adjugate()
    inv_matrix = (inv_det * adjugate_matrix) % alphabet_size

    return np.array(inv_matrix, dtype=int)


def decrypt(message, keys, block_size, alphabet_size):
    result = []
    blocks = stroke_to_blocks(message, block_size)

    keys = generate_keys_massive(keys, blocks)
    inv_keys = [find_inv_key(key, alphabet_size) for key in keys]

    for i in range(len(blocks)):
        block = np.array(blocks[i]).T
        encrypted_block = np.dot(inv_keys[i], blocks[i]).T % len(alphabet_low) 
        result.append(encrypted_block)
    
    result = [arr.tolist() for arr in result]
    result = blocks_to_stroke(result)

    return result


def generate_keys_massive(keys, blocks):
    mod = len(alphabet_low)
    while len(keys) < len(blocks):
        key = np.dot(keys[-2], keys[-1]) % mod
        keys.append(key)
    return keys


while True:
    try:
        lang = int(input("Choose language (1 - Russian, 2 - English): "))
        if lang == 1:
            alphabet = alf_ru
            alphabet_low = alf_rum
            break
        if lang == 2:
            alphabet = alf_en
            alphabet_low = alf_enm
            break
        else: 
            raise Exception
    except Exception:
        print('You need to choose 1 or 2!')


alphabet_size = len(alphabet)
while True:
    try:
        message = input('Enter the text: ')
        if message:
            break
        else:
            raise Exception
    except Exception:
        print("You entered an empty string")


while True:
    try:
        block_size = int(input("Enter the block size for dividing the text: "))
        if block_size > len(message) or block_size <= 1:
            raise Exception
        else: 
            break
    except Exception:
        print(f'Block size is greater than the message length ({len(message)}) or invalid input format')


while True:
    try:
        user_choice = int(input("Do you want to preserve punctuation marks, spaces, and letter case? (1 - yes, 2 - no): "))
        if user_choice == 1 or user_choice == 2:
            break
        else: 
            raise Exception
    except Exception:
        print('You need to choose 1 or 2!')


while True:
    try:
        key_choice = int(input("Do you want to use your own key or generate a random one? (1 - own, 2 - random): "))
        if key_choice == 1:
            rows = block_size 
            elements = list(map(int, input(f"Enter {rows * rows} numbers for the first key separated by spaces: ").split()))
            key1 = np.array(elements).reshape(rows, rows)
            
            elements = list(map(int, input(f"Enter {rows * rows} numbers for the second key separated by spaces: ").split()))
            key2 = np.array(elements).reshape(rows, rows)
            
            determ = int(np.round(np.linalg.det(key1)))
            determ2 = int(np.round(np.linalg.det(key2)))

            if gcd(determ, alphabet_size) != 1:
                raise NameError
            if gcd(determ2, alphabet_size) != 1:
                raise NameError
            break
        elif key_choice == 2:
            key1 = generate_key(block_size, alphabet_size)
            key2 = generate_key(block_size, alphabet_size)
            break
        else:
            raise LookupError   
    except NameError:
        print(f'The determinant of the matrix and the alphabet size ({alphabet_size}) must be coprime!')
    except LookupError:
        print('Choose 1 or 2!')
    except Exception:
        print("Invalid input, please try again or choose automatic key generation")

keys = [key1, key2]

while True:
    try:
        act = int(input("1 - Encryption, 2 - Decryption: "))
        if act == 1 or act == 2:
            break
        else:
            raise Exception
    except Exception:
        print('You need to choose 1 or 2!')

message, chars, indexes = spaces_and_symbols(message)
message, upper = upper_letters(message)


if len(message) % block_size != 0:
        while len(message) % block_size != 0:
            message += alphabet_low[0]
            
if act == 1:
    message = encrypt(message, keys, block_size)
    type_mes = "ciphertext"

else:
    message = decrypt(message, keys, block_size, alphabet_size)
    type_mes = "decrypted text"


if user_choice == 1:
    message = return_everything(message, chars, indexes, upper)
    print(f"\033[32mYour {type_mes}: \033[0m", message)
    print(f"Key:\n {keys[0], keys[1]}")
elif user_choice == 2:
    message = message.upper()
    print(f"\033[32mYour {type_mes}: \033[0m", message)
    print(f"Key:\n {keys[0], keys[1]}")
