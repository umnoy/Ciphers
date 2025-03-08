import re, random

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

        
default_alphabet = "".join(random.sample(alphabet_low, len(alphabet_low)))


def create_custom_alphabet(user_input, base_alphabet = alphabet_low):

    if user_input == "": base_alphabet = default_alphabet
    user_alphabet = "".join(dict.fromkeys(user_input))
    remaining_letters = [char for char in base_alphabet if char not in user_alphabet]
    full_alphabet = user_alphabet + "".join(remaining_letters)

    return full_alphabet


def encrypt(message):
    encrypted = ''
    for char in message:
        if char in alphabet_low:
            index = alphabet_low.find(char)
            encrypted += key_alphabet[index]
        elif char in alphabet:
            index = alphabet.find(char)
            encrypted += key_alphabet_up[index]
        else:
            encrypted += char
    
    return encrypted


def decrypt(message):
    decrypted = ''
    for char in message:
        if char in key_alphabet:
            index = key_alphabet.find(char)
            decrypted += alphabet_low[index]
        elif char in key_alphabet_up:
            index = key_alphabet_up.find(char)
            decrypted += alphabet[index]
        else:
            decrypted += char
    
    return decrypted


message = input('Enter the text: ')

while True:
    try:
        user_alphabet = input('Enter the alphabet for substitution: ').lower()
        user_alphabet = re.sub(r"[\s\d\W]+", "", user_alphabet)
        for char in user_alphabet:
            if char not in alphabet_low:
                print(char)
                raise Exception

        key_alphabet = create_custom_alphabet(user_alphabet)
        key_alphabet_up = key_alphabet.upper()
        break
    except Exception:
        print('You entered characters from a different alphabet, please enter the alphabet again')

while True:
    try:
        act = int(input("1 - Encryption, 2 - Decryption: "))
        if act == 1 or act == 2:
            break
        else:
            raise Exception
    except Exception:
        print('You need to choose 1 or 2!')


print(f'Your alphabet: {key_alphabet}')

if act == 1:
    message = encrypt(message)
    print("\033[32mYour ciphertext: \033[0m", message)
else:
    message = decrypt(message)
    print("\033[32mYour decrypted text: \033[0m", message)
