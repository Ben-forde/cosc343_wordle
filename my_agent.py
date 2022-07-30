__author__ = "<your name>"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "<your e-mail>"

import io

import helper
import copy
import random


class WordleAgent():
    """
       A class that encapsulates the code dictating the
       behaviour of the Wordle playing agent

       ...

       Attributes
       ----------
       dictionary : list
           a list of valid words for the game
       letter : list
           a list containing valid characters in the game
       word_length : int
           the number of letters per guess word
       num_guesses : int
           the max. number of guesses per game
       mode: str
           indicates whether the game is played in 'easy' or 'hard' mode

       Methods
       -------
       AgentFunction(percepts)
           Returns the next word guess given state of the game in percepts
       """

    def __init__(self, dictionary, letters, word_length, num_guesses, mode):
        """
      :param dictionary: a list of valid words for the game
      :param letters: a list containing valid characters in the game
      :param word_length: the number of letters per guess word
      :param num_guesses: the max. number of guesses per game
      :param mode: indicates whether the game is played in 'easy' or 'hard' mode
      """

        self.dictionary = dictionary
        self.letters = letters
        self.word_length = word_length
        self.num_guesses = num_guesses
        self.mode = mode

    def AgentFunction(self, percepts):
        """Returns the next word guess given state of the game in percepts

      :param percepts: a tuple of three items: guess_counter, letter_indexes, and letter_states;
               guess_counter is an integer indicating which guess this is, starting with 0 for initial guess;
               letter_indexes is a list of indexes of letters from self.letters corresponding to
                           the previous guess, a list of -1's on guess 0;
               letter_states is a list of the same length as letter_indexes, providing feedback about the
                           previous guess (conveyed through letter indexes) with values of 0 (the corresponding
                           letter was not found in the solution), -1 (the correspond letter is found in the
                           solution, but not in that spot), 1 (the corresponding letter is found in the solution
                           in that spot).
      :return: string - a word from self.dictionary that is the next guess
      """

        test_words = ["ABACA", "ABACK", "DOGES", "AARON", "ABOUT","TIMED"]

        letters = self.letters
        # This is how you extract three different parts of percepts.
        guess_counter, letter_indexes, letter_states = percepts
        # Here's where you should put in your code
        # .
        # .
        # .

        if guess_counter == 0:

            #self.words = list(test_words)
            self.words =  list(self.dictionary)
            print("list length is :" + str(len(self.words)))
            return "FISTS"

        if guess_counter == self.num_guesses:
            print("in reset")
            self.words = copy.deepcopy(list(self.dictionary))

        self.words = delete_words(self.words, letter_indexes, letter_states, letters)

       # print(words)
        # Currently this agent always returns the first word from the dictionary - probably
        # a good idea to replace this with a better guess based on your code above.
        n = random.randint(0, len(self.words)-1)
        print(self.words)
        return self.words[n]


def delete_words(words, letter_indexes, letter_states, letters):
    words = remove_grays(words, letter_indexes, letter_states, letters)
    words = deal_with_yellows(words, letter_indexes, letter_states, letters)
    words = deal_with_greens(words, letter_indexes, letter_states, letters)
    return words



def get_dictionary(file_path):
    with io.open(file_path, mode="r", encoding="iso-8859-15") as f:
        words = f.read()
        words = words.split("\n")
    return words


# def create_gray_tuple(letter_indexes, letter_states):





def remove_grays(words, letter_indexes, letter_states, letters):
    letter_states = check_for_yellows_greens_for_grey_method(letter_indexes, letter_states)
    deleted_words = []
    guess = helper.letter_indices_to_word(letter_indexes, letters)
    copy_dictionary = copy.deepcopy(words)

    for i in range(len(guess)):
        if letter_states[i] == 0:
            for x in range(len(words)):
                if guess[i] in words[x]:
                    if words[x] not in deleted_words:
                        copy_dictionary.remove(words[x])
                        deleted_words.append(words[x])
    return copy_dictionary

def check_for_yellows_greens_for_grey_method(letter_indexes, letter_states):
    new_letter_states = copy.deepcopy(letter_states)
    for i in range(len(letter_indexes)):
        if letter_states[i] == -1 or letter_states[i] == 1:
            for x in range(len(letter_indexes)):
                if letter_indexes[x] == letter_indexes[i]:
                    new_letter_states[x] = -1

    return new_letter_states


def deal_with_yellows(words, letter_indexes, letter_states, letters):
    """
    check the logic on the if statement about removing from copy_dictionary
    :param words:
    :param letter_indexes:
    :param letter_states:
    :param letters:
    :return:
    """
    deleted_words = []
    letter_counts = check_for_multiple_yellows(letter_indexes, letter_states)
    copy_dictionary = copy.deepcopy(words)
    for word in words:
        for key in letter_counts:
            letter = letters[key]
            amount = letter_counts[key]
            if letter in word:
                for ch in word:
                    if ch == letter:
                        amount -= 1
            if amount != 0 and word not in deleted_words:
                copy_dictionary.remove(word)
                deleted_words.append(word)
    print(deleted_words)
    return copy_dictionary





def check_for_multiple_yellows(letter_indexes, letter_states):
    letter_counts = {}
    for i in range(len(letter_states)):
        if letter_states[i] == -1 or letter_states[i] == 1:
            if letter_indexes[i] not in letter_counts:
                letter_counts[letter_indexes[i]]=1
            else:
                value = letter_counts[letter_indexes[i]]
                letter_counts[letter_indexes[i]] = value + 1

    return letter_counts

def get_green_location(letter_indexes, letter_states):
    green_map = {}
    for i in range(len(letter_indexes)):
        if letter_states[i] == 1:
            if letter_indexes[i] not in green_map:
                location_index = []
                location_index.append(i)
                green_map[letter_indexes[i]] = location_index
            else:
                location_index = green_map.get(letter_indexes[i])
                location_index.append(i)
                green_map[letter_indexes[i]] = location_index

    return green_map

def deal_with_greens(words, letter_indexes, letter_states, letters):

    green_map = get_green_location(letter_indexes, letter_states)
    if green_map:
        copy_dictionary = copy.deepcopy(words)
        delete_words = []
        print(green_map)
        for word in words:
            flag = True
            for key in green_map:
                letter = letters[key]
                index_list = green_map[key]
                for i in index_list:
                    if word[i] != letter:
                        flag = False
                if not flag and word not in delete_words:
                    copy_dictionary.remove(word)
                    delete_words.append(word)
        return copy_dictionary
    else:
        return words


def reset_dictionary(dictionary):
    temp_word = []
    with io.open(dictionary, mode="r", encoding="iso-8859-15") as f:
        words = f.read()
        words = words.split("\n")
        for word in words:
            if len(word) == 5:
                temp_word.append(word)

    return temp_word


# Do something
