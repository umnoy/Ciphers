from math import gcd

alf_ru = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
alf_rum = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
alf_en = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alf_enm = 'abcdefghijklmnopqrstuvwxyz'

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
        user_choice = int(input("Do you want spaces and punctuation to also be encrypted? (1 - Yes, 2 - No): "))
        if user_choice == 1:
            alphabet += " .,/:;!?&*()@#$%"
            alphabet_low += " .,/:;!?&*()@#$%"
            break
        if user_choice == 2:
            break
        else: 
            raise Exception
    except Exception:
        print('You need to choose 1 or 2!')

n = len(alphabet)

while True:
    try:
        user_input = input('Enter the Alpha and Beta keys separated by space: ').split()
        key_alpha, key_beta = map(int, user_input)
        if gcd(key_alpha, n) != 1:
            raise KeyError
        else:
            break
    except ValueError:
        print('You need to enter 2 numerical values, please enter them again')
    except KeyError:
        print(f'The Alpha key and the size of the alphabet ({len(alphabet)}) must be coprime. Please enter different values')

while True:
    try:
        act = int(input("1 - Encryption, 2 - Decryption: "))
        if act == 1 or act == 2:
            break
        else:
            raise Exception
    except Exception:
        print('You need to choose 1 or 2!')

def find_decrypt_alpha(key_alpha):
    decrypt_alpha = 0
    while (key_alpha*decrypt_alpha) % n != 1:
        decrypt_alpha += 1
    return decrypt_alpha


def encrypt(message):
    result = ''
    for char in message:
        if char in alphabet_low:
            index = alphabet_low.find(char)
            cipher_text_index = (key_alpha * index + key_beta) % n
            result += alphabet_low[cipher_text_index]
        elif char in alphabet:
            index = alphabet.find(char)
            cipher_text_index = (key_alpha * index + key_beta) % n
            result += alphabet[cipher_text_index]
        else:
            result += char

    return result


def decrypt(message):
    result = ''
    decrypt_alpha = find_decrypt_alpha(key_alpha)
    for char in message:
        if char in alphabet_low:
            index = alphabet_low.find(char)
            decrypted_text_index = (index - key_beta) * decrypt_alpha % n
            result += alphabet_low[decrypted_text_index]
        elif char in alphabet:
            index = alphabet.find(char)
            decrypted_text_index = (index - key_beta) * decrypt_alpha % n
            result += alphabet[decrypted_text_index]
        else:
            result += char

    return result


if act == 1:
    message = encrypt(message)
    print("\033[32mYour ciphertext: \033[0m", message)
else:
    message = decrypt(message)
    print("\033[32mYour decrypted text: \033[0m", message)
