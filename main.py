import subprocess, sys

def analyse():
     while True:
        try:
            analyse = int(input("\nChoose an analysis:\n\
    1 - Frequency analysis\n\
    2 - Brute force for affine cipher\n\
    3 - Brute force for recurrent affine cipher\n\
    4 - Key calculation for Hill cipher\n\
    5 - Key calculation for recurrent Hill cipher\n\
    6 - Index of Coincidence calculation\n\
    7 - Back\n\
    ---> "))
            if analyse == 1: subprocess.run(["python", "analysis/freq_analysis.py"])
            if analyse == 2: subprocess.run(["python", "analysis/affine_bf.py"])
            if analyse == 3: subprocess.run(["python", "analysis/rec_affine_bf.py"])
            if analyse == 4: subprocess.run(["python", "analysis/hill_analyse.py"])
            if analyse == 5: subprocess.run(["python", "analysis/rec_hill_analyse.py"])
            if analyse == 6: subprocess.run(["python", "analysis/IC_calc.py"])
            if analyse == 7: break
            else: raise Exception
        except Exception:
             print("Please choose an option from the list!")

def ciphers():
    while True:
        try:
            choice = int(input("\nChoose a cipher:\n\
    1 - Simple substitution cipher\n\
    2 - Affine cipher\n\
    3 - Recurrent affine cipher\n\
    4 - Hill cipher\n\
    5 - Recurrent Hill cipher\n\
    6 - Vigenère cipher\n\
    7 - Back\n\
    ---> "))
            if choice == 1: subprocess.run(["python", "ciphers/simple_substitution.py"])
            elif choice == 2: subprocess.run(["python", "ciphers/affine_cipher.py"])
            elif choice == 3: subprocess.run(["python", "ciphers/rec_affine_cipher.py"])
            elif choice == 4: subprocess.run(["python", "ciphers/hill_cipher.py"])
            elif choice == 5: subprocess.run(["python", "ciphers/rec_hill_cipher.py"])
            elif choice == 6: subprocess.run(["python", "ciphers/vigener.py"])
            elif choice == 7: break
            else: raise ValueError
        except ValueError:
            print('\n\033[31mPlease choose an option from the list!\033[0m')

while True:
        try:
            mode = int(input("\nChoose encryption or analysis:\n\
    1 - Ciphers\n\
    2 - Cryptanalysis\n\
    3 - Exit program\n\
    ---> "))
            if mode == 1:
                 ciphers()
            elif mode == 2:
                 analyse()
            elif mode == 3:
                 sys.exit()
            else: 
                 raise Exception
        except Exception:
             print("Please choose an option from the list!")
