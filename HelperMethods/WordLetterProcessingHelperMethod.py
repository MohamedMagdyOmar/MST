# -*- coding: utf-8 -*-
import unicodedata
from copy import deepcopy


class LetterPosition:
    letter = "",
    location = ""

    def __init__(self):
        self.letter = ""
        self.location = ""


def get_each_chars_and_its_location_in_this(sentence):
    chars_in_sentence_with_its_location = []

    for each_word in sentence:
        letter_position_object = LetterPosition()

        for x in range(0, len(each_word)):
            if x == 0 and len(each_word) == 1:
                letter_position_object.letter = each_word[x]
                letter_position_object.location = 'oneCharWord'
                chars_in_sentence_with_its_location.append(deepcopy(letter_position_object))

            else:
                if x == 0:
                    letter_position_object.letter = each_word[x]
                    letter_position_object.location = 'first'
                    chars_in_sentence_with_its_location.append(deepcopy(letter_position_object))

                elif x == (len(each_word) - 1):
                    letter_position_object.letter = each_word[x]
                    letter_position_object.location = 'last'
                    chars_in_sentence_with_its_location.append(deepcopy(letter_position_object))

                else:
                    letter_position_object.letter = each_word[x]
                    letter_position_object.location = 'middle'
                    chars_in_sentence_with_its_location.append(deepcopy(letter_position_object))

    return chars_in_sentence_with_its_location


def remove_diacritics_from_this(character):
    nkfd_form = unicodedata.normalize('NFKD', unicode(character))
    char = u"".join([c for c in nkfd_form if not unicodedata.combining(c) or c == u'ٓ' or c == u'ٔ' or c == u'ٕ'])
    return char


def reform_word_from(list_of_objects_of_chars_and_its_location):
    list_of_words = []
    word = ""
    for each_char_object in list_of_objects_of_chars_and_its_location:
        if each_char_object.location == 'oneCharWord':
            list_of_words.append(each_char_object.letter)

        elif each_char_object.location != 'last':
            word += each_char_object.letter

        elif each_char_object.location == 'last':
            word += each_char_object.letter
            list_of_words.append(word)
            word = ""

    return list_of_words

