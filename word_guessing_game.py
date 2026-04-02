import random
import requests

base_url = "https://random-words-api.kushcreates.com/"

def main():

    used_letters = []
    counter = 1

    player_name = input("Enter your name: ")
    print(f"Welcome to Word Guessing Game {player_name}")

    while True:

        try:

            difficulty = int(input("Difficulty -> Easy (1) | Medium (2) | Hard (3): "))
            if difficulty > 3 or difficulty < 1:
                raise Exception("Enter 1, 2, or 3")
            
            if difficulty == 1:
                attempts = 3
                word_length = 5
            elif difficulty == 2:
                attempts = 3
                word_length = 7
            elif difficulty == 3:
                attempts = 3
                word_length = 10

            break

        except ValueError:
            print("Input a number corresponding to the difficulty")
        except Exception as e:
            print(e)
    
    word_dic = get_random_word(word_length)
    if word_dic == -1:
        return
    
    word = str(word_dic['word'])
    word_category = str(word_dic['category'])
    word_copy = word
    my_list = ["_"] * word_length 
    spaces = [i for i, ch in enumerate(word) if ch.isspace()]
    for index in spaces:
        my_list[index] = " "

    print("Word Category:", word_category, "| Attempts:", attempts)
    
    while True:
        
        print(" ".join(my_list))

        char_guess = input(f"Guess #{counter} ({attempts}) -> ")

        if char_guess in used_letters or char_guess in my_list:
            print("Already Guessed/Found")
            continue

        counter += 1

        if char_guess in word:
            print("Found")
            word_copy = place_letter(my_list, word, char_guess, word_copy)
        else:
            used_letters.append(char_guess)
            print("No match")
            attempts -= 1
            reveal_letter = random.randrange(0, len(word_copy), 1)
            word_copy = place_letter(my_list, word, word_copy[reveal_letter], word_copy)
        
        if attempts == 0:
            print("You lose")
            print(f"Answer: {word} | Total guesses: {counter - 1}")
            break
        if "".join(my_list) == word or char_guess == word:
            print("You win!")
            print(f"Answer: {word} | Total guesses: {counter - 1}")
            break
        
def place_letter(my_list, word, char_guess, word_copy):
    index = 0
    for char in word:
        if char_guess == char:
            my_list[index] = char_guess
            word_copy = word_copy.replace(char_guess, "")  
        index += 1
    return word_copy

def get_random_word(word_length):
    url = f"https://random-words-api.kushcreates.com/api?language=en&length={word_length}&words=1"
    response = requests.get(url)
    word_data = response.json()
    if response.status_code == requests.codes.ok:
        return word_data[0]
    else:
        print("Error:", response.status_code, response.text)
        return -1

if __name__ == '__main__':
    main()
