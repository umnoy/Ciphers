from math import gcd

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
        if lang == 2:
            alphabet = alf_en
            alphabet_low = alf_enm
            break
        else: 
            raise Exception
    except Exception:
        print('You need to choose 1 or 2!')


def find_decrypt_alpha(a):
    for x in range(1, n):
        if (a * x) % n == 1:
            return x
    return None 


def decrypt(message, key_alpha, key_beta):
    result = ''
    for char in message:
        if char in alphabet_low:
            index = alphabet_low.find(char)
            decrypt_alpha = find_decrypt_alpha(key_alpha)
            decrypted_text_index = (index - key_beta) * decrypt_alpha % n
            result += alphabet_low[decrypted_text_index]
        elif char in alphabet:
            index = alphabet.find(char)
            decrypt_alpha = find_decrypt_alpha(key_alpha)
            decrypted_text_index = (index - key_beta) * decrypt_alpha % n
            result += alphabet[decrypted_text_index]
        else:
            result += char
            
    return result

cipher = input('Enter the cipher text: ')
alphas = []
n = len(alphabet)
for a in range(n):
    if gcd(a, n) == 1:
        alphas.append(a)


with open("affine_output.txt", "w", encoding="utf-8") as file:
    for a in alphas:
        for b in range(n):
            file.write(f'({a}, {b}): {decrypt(cipher, a, b)}\n')

print("\033[32mResults have been saved in affine_output.txt\033[0m")
