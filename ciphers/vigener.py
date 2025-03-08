import re

alf_ru = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
alf_rum = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
alf_en = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alf_enm = 'abcdefghijklmnopqrstuvwxyz'


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


def encrypt(message, key):
    result = ''
    for i in range(len(message)):
        if message[i] in alphabet_low:
            plain_char = message[i]
            key_char = key[i]

            plain_index = alphabet_low.find(plain_char)
            key_index = alphabet_low.find(key_char)

            encrypted_index = (plain_index + key_index) % alphabet_size
            result += alphabet_low[encrypted_index]
        else:
            result += message[i]
    return result


def decrypt(message, key):
    result = ''
    for i in range(len(message)):
        if message[i] in alphabet_low:
            cipher_char = message[i]
            key_char = key[i]

            cipher_index = alphabet_low.find(cipher_char)
            key_index = alphabet_low.find(key_char)

            decrypted_index = (cipher_index - key_index) % alphabet_size
            result += alphabet_low[decrypted_index]
        else:
            result += message[i]
    return result


def repeat_gamma(key, message):
    while len(key) < len(message):
        key += key
    
    key = key[:len(message)]
    return(key)


def plaintext_gamma(key, message):
    key += message
    return(key[:len(message)])


def ciphertext_gamma(key, message):
    if len(key) >= len(message):
        pass
    else:
        for char in message:
            key += encrypt(char, key[-1])

    return key[:len(message)]


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


alphabet_size = len(alphabet_low)


while True:
    try:
        message = input('Enter the text: ')
        if message:
            break
        else:
            raise Exception
    except Exception:
        print("You entered an empty string")


message, chars, indexes = spaces_and_symbols(message)
message, upper = upper_letters(message)


while True:
    try:
        key = input('Enter the key: ').lower()
        if key:
            key = re.sub(r"[\s\d\W]+", "", key)
            break
        else:
            raise Exception
    except Exception:
        print("You entered an empty string")


while True:
    try:
        gamma_type = int(input("Choose the type of gamma generation:\n\
1 - Key repetition\n\
2 - Gamma based on plaintext\n\
3 - Gamma based on ciphertext\n\
---> "))
        if gamma_type == 1:
            key = repeat_gamma(key, message)
            break
        if gamma_type == 2:
            key = plaintext_gamma(key, message)
            break
        if gamma_type == 3:
            key = ciphertext_gamma(key, message)
            break
        else: 
            raise Exception
    except Exception:
        print('You need to choose 1, 2, or 3!')


while True:
    try:
        user_choice = int(input("Do you want to preserve punctuation, spaces, and letter case? (1 - yes, 2 - no): "))
        if user_choice == 1 or user_choice == 2:
            break
        else: 
            raise Exception
        
    except Exception:
        print('You need to choose 1 or 2!')


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
    message = encrypt(message, key)
    type_mes = "ciphertext"

else:
    message = decrypt(message, key)
    type_mes = "decrypted text"


if user_choice == 1:
    message = return_everything(message, chars, indexes, upper)
    print(f"\033[32mYour {type_mes}: \033[0m", message)

elif user_choice == 2:
    message = message.upper()
    print(f"\033[32mYour {type_mes}: \033[0m", message)
