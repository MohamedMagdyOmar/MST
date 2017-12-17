# -*- coding: utf-8 -*-

import unicodedata


def sukun_correction(list_of_objects_of_chars_and_its_location):
    list_of_objects = []

    for each_object in list_of_objects_of_chars_and_its_location:
        each_object.letter = remove_sukun_diacritics_if_exists(each_object.letter)
        list_of_objects.append(each_object)

    return list_of_objects


def remove_sukun_diacritics_if_exists(char):

    normalized_char = unicodedata.normalize('NFC', char)

    if u'ْ' in normalized_char:
        for c in normalized_char:
            if not unicodedata.combining(c):
                return unicodedata.normalize('NFC', c)
    else:
        return char
