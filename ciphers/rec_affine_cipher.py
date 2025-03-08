from math import gcd
import re


alf_ru = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
alf_rum = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
alf_en = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alf_enm = 'abcdefghijklmnopqrstuvwxyz'

keys = []
idexes = []

while True:
    try:
        lang = int(input("Choose language (1 - Russian, 2 - English): "))
        if lang == 1:
            alphabet = alf_ru
            alphabet_low = alf_rum
            n = 33
            break
        if lang == 2:
            alphabet = alf_en
            alphabet_low = alf_enm
            n = 26
            break
        else: 
            raise Exception
    except Exception:
        print('You need to choose 1 or 2!')

message = input('Enter the text: ')

while True:
    try:
        user_choice = int(input("Do you want spaces and punctuation marks to participate in encryption as well? (1 - yes, 2 - no): "))
        if user_choice == 1:
            alphabet += " .,/:;!?&*()@#$%"
            alphabet_low += " .,/:;!?&*()@#$%"
            clear_message = message
            break
        if user_choice == 2:
            clear_message = re.sub(r"[\s\d\W]+", "", message)
            break
        else: 
            raise Exception
    except Exception:
        print('You need to choose 1 or 2!')

n = len(alphabet)

while True:
    try:
        user_input = input('Enter 4 keys separated by spaces: ').split()
        key1_alpha, key1_beta, key2_alpha, key2_beta = map(int, user_input)
        if (gcd(key1_alpha, n) != 1) or (gcd(key2_alpha, n) != 1):
            raise KeyError
        else:
            keys.append((key1_alpha, key1_beta))
            keys.append((key2_alpha, key2_beta))
            break
    except ValueError:
        print('You need to enter 4 numeric values, please try again')
    except KeyError:
        print('The Alpha keys and the alphabet size must be coprime. Enter different values')

def find_decrypt_alpha(a):
    for x in range(1, n):
        if (a * x) % n == 1:
            return x
    return None 

def keys_calculation(keys):
    for _ in range(len(clear_message)):
        alpha_1, beta_1 = keys[len(keys) - 2]
        alpha_2, beta_2 = keys[len(keys) - 1]
        current_key = ((alpha_1 * alpha_2) % n, (beta_1 + beta_2) % n)
        keys.append(current_key)
    return keys

def encrypt(message):
    result = ''
    count  = 0
    for char in message:
        if char in alphabet_low:
            key_alpha, key_beta = keys[count]
            index = alphabet_low.find(char)
            cipher_text_index = (key_alpha * index + key_beta) % n
            result += alphabet_low[cipher_text_index]
            count += 1
        elif char in alphabet:
            key_alpha, key_beta = keys[count]
            index = alphabet.find(char)
            cipher_text_index = (key_alpha * index + key_beta) % n
            result += alphabet[cipher_text_index]
            count += 1
        else:
            result += char

    return result

def decrypt(message):
    result = ''
    count = 0
    for char in message:
        if char in alphabet_low:
            index = alphabet_low.find(char)
            key_alpha, key_beta = keys[count]
            decrypt_alpha = find_decrypt_alpha(key_alpha)
            decrypted_text_index = (index - key_beta) * decrypt_alpha % n
            result += alphabet_low[decrypted_text_index]
            count += 1

        elif char in alphabet:
            index = alphabet.find(char)
            key_alpha, key_beta = keys[count]
            decrypt_alpha = find_decrypt_alpha(key_alpha)
            decrypted_text_index = (index - key_beta) * decrypt_alpha % n
            result += alphabet[decrypted_text_index]
            count += 1

        else:
            result += char

    return result

keys = keys_calculation(keys)

while True:
    try:
        act = int(input("1 - Encryption, 2 - Decryption: "))
        if act == 1 or act == 2:
            break
        else:
            raise Exception
    except Exception:
        print('You need to choose 1 or 2!')

if act == 1:
    message = encrypt(message)
    print("\033[32mYour ciphertext: \033[0m", message)

else:
    message = decrypt(message)
    print("\033[32mYour decrypted text: \033[0m", message)
