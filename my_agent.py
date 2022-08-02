__author__ = "<your name>"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "<your e-mail>"
"https://github.com/Argel-Tal/COSC343-Genetic/blob/main/cosc343report/COSC343%20Genetic%20AI%20-%20Report.ipynb"

import io
from operator import itemgetter
from collections import OrderedDict
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

        test_words = ["FITTS", "ALLOW", "TOUGH", "ALLOW", "FISTS", "CRANE"]
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

        test_words = ["ABACA", "ABACK", "DOGES", "AARON", "ABOUT", "TIMED"]

        letters = self.letters
        # This is how you extract three different parts of percepts.
        guess_counter, letter_indexes, letter_states = percepts
        # Here's where you should put in your code
        # .
        # .
        # .

        if guess_counter == 0:
            # self.words = list(test_words)
            self.words = list(self.dictionary)
            return "CRANE"

        if guess_counter == self.num_guesses:
            self.words = copy.deepcopy(list(self.dictionary))

        self.words = delete_words(self.words, letter_indexes, letter_states, letters)

        n = random.randint(0, len(self.words) - 1)
        updated_letter_map = get_letter_value_map(self.words)

        #return self.words[n]
        return get_word_value(self.words, updated_letter_map)

        # get_word_value(self.words)





def get_letter_value_map(words):
   total_letters = 0
   map_values = {}
   for word in words:
      for char in word:
         total_letters += 1
         if char not in map_values:
            map_values[char] = 1
         else:
            count = map_values[char]
            count += 1
            map_values[char] = count

   for char in map_values:
      val = map_values[char]
      val = val/total_letters
      map_values[char] = val


   return map_values




def delete_words(words, letter_indexes, letter_states, letters):
    words = deal_with_greens(words, letter_indexes, letter_states, letters)
    words = deal_with_yellows(words, letter_indexes, letter_states, letters)
    words = remove_yellows_in_sample_place(words, letter_indexes, letter_states, letters)
    words = remove_grays(words, letter_indexes, letter_states, letters)

    words = remove_guess(words, letter_indexes, letter_states, letters)
    return words


def remove_guess(words, letter_indexes, letter_states, letters):
    flag = True
    for i in letter_states:
        if i != 1:
            flag = False

    if not flag:
        word = ""

        for ch in letter_indexes:
            letter = letters[ch]
            word += letter
        if word in words:
            words.remove(word)
    return words


def get_dictionary(file_path):
    """
    returns the dictionary as a list from the file path
    :param file_path: path to dictonary
    :return: a list of words
    """
    with io.open(file_path, mode="r", encoding="iso-8859-15") as f:
        words = f.read()
        words = words.split("\n")
    return words


def remove_grays(words, letter_indexes, letter_states, letters):
    """
    removes words which contain letters with a state given as gray
    :param words: a list of possible words
    :param letter_indexes: an array of letters given as a index through the alphabet
    :param letter_states: an array of states indicating weather a green, yellow or gray
    :param letters: array of letters in alphabet
    :return: a new list of words which dont contain gray letters
    """
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
    """
  creates a new letter states so that words which arnt supposed to be removed
  dont get removed.

    :param letter_indexes: an array of letters given as a index through the alphabet
    :param letter_states: an array of states indicating weather a green, yellow or gray
    :return:
    """
    new_letter_states = copy.deepcopy(letter_states)
    for i in range(len(letter_indexes)):
        if letter_states[i] == -1 or letter_states[i] == 1:
            for x in range(len(letter_indexes)):
                if letter_indexes[x] == letter_indexes[i]:
                    new_letter_states[x] = -1
    return new_letter_states


def deal_with_yellows(words, letter_indexes, letter_states, letters):
    """
    removes words where the yellow occures and those which dont contain yellows.

    :param words: a list of possible words
    :param letter_indexes: an array of letters given as a index through the alphabet
    :param letter_states: an array of states indicating weather a green, yellow or gray
    :param letters: array of letters in alphabet
    :return: a new list of words potential words with yellows filterd
    """
    deleted_words = []
    letter_counts = check_for_multiple_yellows(letter_indexes, letter_states)
    copy_dictionary = copy.deepcopy(words)

    for word in words:
        for key in letter_counts:
            letter = letters[key]
            amount = letter_counts[key]
            for char in word:
                if char == letter:
                    amount -= 1
            if amount > 0 and word not in deleted_words:
                deleted_words.append(word)
                copy_dictionary.remove(word)

    return copy_dictionary


def check_for_multiple_yellows(letter_indexes, letter_states):
    """
    creates a map for removing yellows
    :param letter_indexes: an array of letters given as a index through the alphabet
    :param letter_states: an array of states indicating weather a green, yellow or gray
    :return: a dictionary of yellows to be removed
    """
    letter_counts = {}
    for i in range(len(letter_states)):
        if letter_states[i] == -1 or letter_states[i] == 1:
            if letter_indexes[i] not in letter_counts:
                letter_counts[letter_indexes[i]] = 1
            else:
                value = letter_counts[letter_indexes[i]]
                letter_counts[letter_indexes[i]] = value + 1

    return letter_counts


def get_yellow_map(letter_indexes, letter_states, letters):
    """
    creates a map of yellows and there index of where to remove them from.
     :param letter_indexes: an array of letters given as a index through the alphabet
    :param letter_states: an array of states indicating weather a green, yellow or gray
    :param letters: array of letters in alphabet
    :return: a dictionary of letters to be removed
    """
    yellow_map = {}
    for i in range(len(letter_indexes)):
        if letter_states[i] == -1:
            letter = letters[letter_indexes[i]]
            if (letter not in yellow_map):
                index_list = []
                index_list.append(i)
                yellow_map[letter] = index_list
            else:
                index_list = yellow_map[letter]
                index_list.append(i)
                yellow_map[letter] = index_list

    return yellow_map


def remove_yellows_in_sample_place(words, letter_indexes, letter_states, letters):
    copy_dictionary = copy.deepcopy(words)
    yellow_map = get_yellow_map(letter_indexes, letter_states, letters)
    delete_words = []
    for word in words:
        for key in yellow_map:
            index_list = yellow_map[key]
            for i in index_list:
                if word[i] == key and word not in delete_words:
                    copy_dictionary.remove(word)
                    delete_words.append(word)
    return copy_dictionary


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





def get_word_value(words, letter_values):

    word_val_dict = {}
    for word in words:
        val = 0
        check_multi = ""
        for char in word:
            if char not in check_multi:
                val += letter_values[char]
            check_multi += char
        word_val_dict[word] = val

    sorted_x = OrderedDict(sorted(word_val_dict.items(), key=itemgetter(1)))
    word = sorted_x.popitem(last=True)
    return word[0]
# Do something
