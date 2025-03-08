from collections import Counter
import re
import matplotlib.pyplot as plt

def char_frequency_analysis(text):
    frequency = Counter(text)
    length = len(text)
    percentage_frequency = sorted(
    [(char, freq / length * 100) for char, freq in frequency.items()], key=lambda x: x[1], reverse=True
    )
    
    return percentage_frequency


def plot_frequency(frequency):
    chars, counts = zip(*frequency)
    plt.figure(figsize=(10, 5))
    plt.bar(chars, counts, color='skyblue')
    plt.xlabel("Characters")
    plt.ylabel("Frequency (%)")
    plt.title("Character Frequency Analysis")
    plt.show()

text = input("Enter the text for analysis: ").lower()

while True:
    try:
        user_choice = int(input("Include punctuation in the analysis? (1 - Yes, 2 - No): "))
        if user_choice == 1:
            clear_message = text
            break
        if user_choice == 2:
            clear_message = re.sub(r"[\s\d\W]+", "", text)
            break
        else: 
            raise Exception
    except Exception:
        print('You need to choose 1 or 2!')


exceptions = input('Enter the characters you want to exclude from the analysis, separated by spaces (leave empty if none): ').split()

result = char_frequency_analysis(clear_message)

if exceptions:
    result = [item for item in result if str(item[0]) not in exceptions]

print("\nCharacter frequency analysis:")
for char, freq in result:
    print(f"'{char}': {freq}%")
    
print(len(result))
plot_frequency(result)