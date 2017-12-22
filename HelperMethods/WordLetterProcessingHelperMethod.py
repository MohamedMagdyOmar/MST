# -*- coding: utf-8 -*-
import unicodedata
import locale
from copy import deepcopy


class LetterPosition:
    letter = "",
    location = ""

    def __init__(self):
        self.letter = ""
        self.location = ""


def get_location_of_each_char(list_of_chars, chars_count_for_each_word):
    list_of_chars_with_its_location = []
    i = 0

    sum = 0
    for each_number in chars_count_for_each_word:
        sum += each_number

    if sum != len(list_of_chars):
        raise ValueError('bug appeared in "get_location_of_each_character_in_current_sentence"')

    for count_of_letters in chars_count_for_each_word:
        letter_position_object = LetterPosition()
        for x in range(0, count_of_letters):
            if count_of_letters == 1:
                letter_position_object.letter = list_of_chars[i]
                letter_position_object.location = 'firstOneLetter'
                list_of_chars_with_its_location.append(deepcopy(letter_position_object))

            else:
                if x == 0:
                    letter_position_object.letter = list_of_chars[i]
                    letter_position_object.location = 'first'
                    list_of_chars_with_its_location.append(deepcopy(letter_position_object))

                elif x == (count_of_letters - 1):
                    letter_position_object.letter = list_of_chars[i]
                    letter_position_object.location = 'last'
                    list_of_chars_with_its_location.append(deepcopy(letter_position_object))

                else:
                    letter_position_object.letter = list_of_chars[i]
                    letter_position_object.location = 'middle'
                    list_of_chars_with_its_location.append(deepcopy(letter_position_object))

            i += 1

    return list_of_chars_with_its_location


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


def decompose_word_into_letters(word):

    decomposed_word = []
    inter_med_list = []
    found_flag = False

    for each_letter in word:
        if not unicodedata.combining(each_letter):
            if found_flag:
                decomposed_word.append(inter_med_list)
            inter_med_list = []
            inter_med_list.append(each_letter)
            found_flag = True

        elif found_flag:
            inter_med_list.append(each_letter)
    # required because last character will not be added above, but here
    decomposed_word.append(inter_med_list)

    return decomposed_word


def decompose_diac_char_into_char_and_diacritics(diac_char):

    decomposed_char = []

    for each_letter in diac_char:
        decomposed_char.append(each_letter)

    return decomposed_char


def normalize(word):

    locale.setlocale(locale.LC_ALL, "")
    for x in range(0, len(word)):
        word[x].sort(cmp=locale.strcoll)

    return word


def convert_list_of_words_to_list_of_chars(list_of_words):

    found_flag = False
    overall = ""
    comp = ""
    final_list_of_actual_letters = []
    for each_word in list_of_words:
        for each_letter in each_word:
            x = unicodedata.combining(each_letter)
            if not unicodedata.combining(each_letter):
                if found_flag and comp != u'﻿':
                    final_list_of_actual_letters.append(comp)

                overall = each_letter
                found_flag = True
                comp = unicodedata.normalize('NFC', overall)
            elif found_flag:
                overall += each_letter
                comp = unicodedata.normalize('NFC', overall)

    final_list_of_actual_letters.append(comp)

    return final_list_of_actual_letters


def attach_diacritics_to_chars(un_diacritized_chars, diacritics):
    list_chars_attached_with_diacritics = []

    if len(un_diacritized_chars) != len(diacritics):
        raise Exception('attach_diacritics_to_chars')

    for each_char, each_diacritics in zip(un_diacritized_chars, diacritics):
        list_chars_attached_with_diacritics.append((each_char + each_diacritics))

    return list_chars_attached_with_diacritics


def get_chars_count_for_each_word_in_this(sentence):
    count = 0
    chars_count_of_each_word = []
    for each_word in sentence:
        for each_char in each_word:
            if not unicodedata.combining(each_char) and each_char != u'﻿':
                count += 1
        chars_count_of_each_word.append(count)
        count = 0

    return chars_count_of_each_word
