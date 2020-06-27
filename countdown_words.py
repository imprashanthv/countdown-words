# imports
import random
from threading import Timer  # You can make it light weight by just importing Timer
import keyboard  # Dependency. please do 'pip install keyboard' before proceeding


# general purpose - string to dictionary builder.
def build_dict(list_to_build):
    built_dict = {}
    for k in list_to_build:
        if k not in built_dict:
            built_dict.__setitem__(k, 1)
        if k in built_dict:
            # get the value of i to update repetition
            value_of_i = built_dict.get(k)
            built_dict.__setitem__(k, value_of_i + 1)  # rep updated here
    return built_dict


# check if user input has letters within the selection boundary (letters and repetition)
def is_valid(letter_list, word):
    # note: user_letters is already a list
    # making user_word as a list
    user_word_list = [x for x in word]

    # preliminary check - any letter outside of user selection
    for k in user_word_list:
        if k not in letter_list:
            return False

    # building dictionaries
    user_letters_dict = build_dict(letter_list)
    user_word_dict = build_dict(user_word_list)

    # compare - trick is to compare the values for respected keys.
    for k in user_word_dict:
        if user_word_dict.get(k) <= user_letters_dict.get(k):
            return True
        else:
            return False


# this function enables to keep the time limit
def time_check():
    global user_word
    if user_word is not None:
        return
    else:
        print("sorry, time's up")
        keyboard.press_and_release('enter')


def start_game(name):
    global user_word
    timeout = 30
    print("\n\n" + name + " - Your turn.\nYou have " + str(timeout) + " seconds")
    t = Timer(timeout, time_check)
    t.start()
    user_word = input("Make a real word out of those letters: ")

    if user_word in english_words:
        if is_valid(user_letters, user_word):
            print("It's a dictionary word")
            score = len(user_word)

        else:
            print("It's a dictionary word. However, you've used letters outside your selection")
            score = 0
    else:
        print("Sorry, It's not a dictionary word!")
        score = 0

    t.cancel()
    user_word = None
    return score


# pre-data
vowels = ['a', 'e', 'i', 'o', 'u']
consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
# reading english words as a set from a text file
with open('english_dictionary_words.txt') as words:
    english_words = set(words.read().split())

# user-data
user_letters = []
user_word = None

# users shall have 9 choices to pick
for i in range(9):
    user_input = int(input("Pick a vowel by typing 1 (or)\nPick a consonant by typing 2: "))
    if user_input == 1:
        user_letters.append(random.choice(vowels))
    if user_input == 2:
        user_letters.append(random.choice(consonants))
    print("Choices so far: " + str(user_letters))
    print("-----------------------------------------------------------------------------")
# showing the selection
print("Your selection is " + str(user_letters))
print("-----------------------------------------------------------------------------")

# start game
player1_score = start_game("player 1")
player2_score = start_game("player 2")

if player1_score > player2_score:
    print("\n\nplayer 1 wins by " + str(player1_score - player2_score) + " points lead")
elif player2_score > player1_score:
    print("\n\nplayer 2 wins by " + str(player2_score - player1_score) + " points lead")
else:
    print("\n\nIt's a tie. Both of you have scored " + str(player1_score) + " points")
