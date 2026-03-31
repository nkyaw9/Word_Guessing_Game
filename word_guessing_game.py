import random
import requests

base_url = "https://random-words-api.kushcreates.com/"

def main():

    player_name = input("Enter your name: ")

    while True:
        try:
            difficulty = int(input("Difficulty -> Easy (1) | Medium (2) | Hard (3): "))
            break
        except ValueError:
            print("Input a number corresponding to the difficulty")
    
    if difficulty == 1:
        attempts = 2
        word_length = 5
    elif difficulty == 2:
        attempts = 3
        word_length = 7
    elif difficulty == 3:
        attempts = 4
        word_length = 10

    word = str(get_random_word(word_length))
    word_copy = word
    if word == -1:
        return
    
    num_of_char = len(word)

    my_list = ["_"] * word_length 
    counter = 1
    while True:
        if attempts == 0:
            print("You lose")
            print(f"Answer: {word}")
            break
        if "".join(my_list) == word:
            print("You win!")
            print(f"Total guesses: {counter - 1}")
            break
        print(" ".join(my_list))
        char_guess = input(f"Guess #{counter}: ")
        if len(char_guess) != 1:
            print("Input only 1 character")
            continue
        counter += 1
        if char_guess in my_list:
            print("Already found")
        elif char_guess in word:
            print("Found")
            word_copy = place_letter(my_list, word, char_guess, word_copy)
        else:
            print("No match")
            attempts -= 1
            reveal_letter = random.randrange(0, len(word_copy), 1)
            word_copy = place_letter(my_list, word, word_copy[reveal_letter], word_copy)
        
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
        return word_data[0]['word']
    else:
        print("Error:", response.status_code, response.text)
        return -1



main()