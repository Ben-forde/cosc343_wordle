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






all_words = get_dictionary("dictionaries/english.txt")

get_letter_value_map(all_words)




