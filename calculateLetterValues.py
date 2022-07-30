import io

import numpy as np
import json


# reads in the english dictionary and removes all words that arnt length 5
import helper


def get_dictionary(file_path):
   with io.open(file_path, mode="r", encoding="iso-8859-15") as f:
      words = f.read()
      words = words.split("\n")

   return words

#def create_gray_tuple(letter_indexes, letter_states):


def remove_grays(words, letter_indexes, letter_states):
   for i in range(5):
      if letter_states[i] == 0:
         for word in words:
            if helper.letter_indices_to_word(letter_indexes[i]) in word:
               words.remove(word)



normal_words = get_dictionary("dictionaries/acutalWords.txt")
all_words = get_dictionary("dictionaries/english.txt")




