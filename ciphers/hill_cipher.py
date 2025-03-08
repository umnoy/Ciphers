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


def spaces_and_symblos(message):
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


def encrypt(message, key, block_size):
    result = []
    blocks = stroke_to_blocks(message, block_size)

    for block in blocks:
        block = np.array(block).T
        encrypted_block = np.dot(key, block).T % len(alphabet_low)
        result.append(encrypted_block)
    
    result = [arr.tolist() for arr in result]
    result = blocks_to_stroke(result)

    return result


def find_inv(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"The determinant {a} has no inverse modulo {m}")


def find_inv_key(key, alphabet_size):
    det = int(round(np.linalg.det(key))) 
    det_mod = det % alphabet_size

    inv_det = find_inv(det_mod, alphabet_size)
    matrix = Matrix(key)
    adjugate_matrix = matrix.adjugate()
    inv_matrix = (inv_det * adjugate_matrix) % alphabet_size

    return np.array(inv_matrix, dtype=int)


def decrypt(message, key, block_size, alphabet_size):
    result = []
    blocks = stroke_to_blocks(message, block_size)

    inv_key = find_inv_key(key, alphabet_size)

    for block in blocks:
        block = np.array(block).T
        encrypted_block = np.dot(inv_key, block).T % len(alphabet_low)
        result.append(encrypted_block)
    
    result = [arr.tolist() for arr in result]
    result = blocks_to_stroke(result)

    return result

if __name__ == "__main__":
    
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
            block_size = int(input("Enter the block size for splitting the text: "))
            if block_size > len(message) or block_size <= 0:
                raise Exception
            else: 
                break
        except Exception:
            print(f'The block size is larger than the message length ({len(message)}) or you entered incorrect data')


    while True:
        try:
            user_choice = int(input("Do you want to preserve punctuation, spaces, and letter case? (1 - Yes, 2 - No): "))
            if user_choice == 1 or user_choice == 2:
                break
            else: 
                raise Exception
        except Exception:
            print('You need to choose 1 or 2!')


    while True:
        try:
            key_choice = int(input("Do you want to use your own key or a random one? (1 - Your own, 2 - Random): "))
            if key_choice == 1:
                rows = block_size 
                elements = list(map(int, input(f"Enter {rows * rows} numbers separated by space: ").split()))
                key = np.array(elements).reshape(rows, rows)
                
                determ = int(np.round(np.linalg.det(key)))

                if gcd(determ, alphabet_size) != 1:
                    raise NameError
                break
            elif key_choice == 2:
                key = generate_key(block_size, alphabet_size)
                break
            else:
                raise LookupError   
        except NameError:
            print(f'The determinant of the matrix and the alphabet size ({alphabet_size}) must be coprime!')
        except LookupError:
            print('Choose 1 or 2!')
        except Exception:
            print("Incorrect data entered, try again or choose automatic key generation")

    while True:
        try:
            act = int(input("1 - Encryption, 2 - Decryption: "))
            if act == 1 or act == 2:
                break
            else:
                raise Exception
        except Exception:
            print('You need to choose 1 or 2!')

    message, chars, indexes = spaces_and_symblos(message)
    message, upper = upper_letters(message)

    if len(message) % block_size != 0:
            while len(message) % block_size != 0:
                message += alphabet_low[0]
                
    if act == 1:
        message = encrypt(message, key, block_size)
        type_mes = "ciphertext"

    else:
        message = decrypt(message, key, block_size, alphabet_size)
        type_mes = "decrypted text"


    if user_choice == 1:
        message = return_everything(message, chars, indexes, upper)
        print(f"\033[32mYour {type_mes}: \033[0m", message)
        print(f"Key:\n {key}")
    elif user_choice == 2:
        message = message.upper()
        print(f"\033[32mYour {type_mes}: \033[0m", message)
        print(f"Key:\n {key}")
