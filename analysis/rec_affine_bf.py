from math import gcd
import re

alf_ru = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
alf_rum = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
alf_en = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alf_enm = 'abcdefghijklmnopqrstuvwxyz'

while True:
    try:
        lang = int(input("Choose a language (1 - Russian, 2 - English): "))
        if lang == 1:
            alphabet = alf_ru
            alphabet_low = alf_rum
            break
        elif lang == 2:
            alphabet = alf_en
            alphabet_low = alf_enm
            break
        else: 
            raise Exception
    except Exception:
        print('You need to choose 1 or 2!')


message = input('Enter the ciphertext to decrypt: ')
clear_message = re.sub(r"[\s\d\W]+", "", message)

n = len(alphabet)

alphas = [a for a in range(n) if gcd(a, n) == 1]

print('All possible alpha keys have been generated')


def keys_calculation(key_pair1, key_pair2, length):
    alpha_1, beta_1 = key_pair1
    alpha_2, beta_2 = key_pair2
    keys = [(alpha_1, beta_1), (alpha_2, beta_2)]
    
    for _ in range(2, length):
        new_alpha = (keys[-1][0] * keys[-2][0]) % n
        new_beta = (keys[-1][1] + keys[-2][1]) % n
        keys.append((new_alpha, new_beta))
    
    return keys[:length] 


def find_decrypt_alpha(a):
    for x in range(1, n):
        if (a * x) % n == 1:
            return x
    return None 


def decrypt(message, key_pair1, key_pair2):
    result = ''
    count = 0
    current_keys = keys_calculation(key_pair1, key_pair2, len(clear_message))
    
    for char in message:
        if char in alphabet_low:
            index = alphabet_low.find(char)
            key_alpha, key_beta = current_keys[count]
            alpha_inv = find_decrypt_alpha(key_alpha)
            if alpha_inv is None:
                return "" 
            decrypted_text_index = (alpha_inv * (index - key_beta)) % n
            result += alphabet_low[decrypted_text_index]
            count += 1

        elif char in alphabet:
            index = alphabet.find(char)
            key_alpha, key_beta = current_keys[count]
            alpha_inv = find_decrypt_alpha(key_alpha)
            if alpha_inv is None:
                return ""
            decrypted_text_index = (alpha_inv * (index - key_beta)) % n
            result += alphabet[decrypted_text_index]
            count += 1

        else:
            result += char

    return result


keys = [(a, b) for a in alphas for b in range(n)]

print('A set of keys has been generated')

with open("rec_affine_output.txt", "w", encoding="utf-8") as file:
    for pair_1 in keys:
        for pair_2 in keys:
            decrypted_text = decrypt(message, pair_1, pair_2)
            if decrypted_text:
                file.write(f'{pair_1}, {pair_2}: {decrypted_text}\n')

print("\033[32mResults have been saved in rec_affine_output.txt\033[0m")
