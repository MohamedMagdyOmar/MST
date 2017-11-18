# -*- coding: utf-8 -*-

import csv
import xlsxwriter
import MySQLdb
import MySQLdb.cursors
import os
import glob
import unicodedata
from xlrd import open_workbook
from xlutils.copy import copy
from copy import deepcopy
import locale

class LetterPosition:
    letter = "",
    location = ""

    def __init__(self):
        self.letter = ""
        self.location = ""

letters_of_fatha_correction = [u'ة', u'ا', u'ى']
# letters_of_fatha_correction = [u'ة', u'ى']

total_error = 0
row_of_letters_excel_file = 0
current_row_in_excel_file = 1
extension = 'csv'

path = 'D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample'
diacritization_error_excel_file_path = "D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample\Errors" \
                                       "\Book1.xls "

workbook = xlsxwriter.Workbook(diacritization_error_excel_file_path)
worksheet = workbook.add_worksheet()
worksheet.write(0, 0, 'Actual')
worksheet.write(0, 1, 'Expected')
worksheet.write(0, 2, 'Error Location')
workbook.close()


def connect_to_db():
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                         user="root",  # your username
                         passwd="Islammega88",  # your password
                         db="mstdb",  # name of the data base
                         cursorclass=MySQLdb.cursors.SSCursor,
                         use_unicode=True,
                         charset="utf8",
                         init_command='SET NAMES UTF8')
    global cur
    cur = db.cursor()


def get_list_of_sentence_numbers():
    sentence_number_of_testing_query = "select distinct SentenceNumber from parseddocument where LetterType='testing' "\
                                       "order by idCharacterNumber asc "

    cur.execute(sentence_number_of_testing_query)

    sentence_numbers = (cur.fetchall())
    sentence_numbers = [each_number[0] for each_number in sentence_numbers]
    sentence_numbers = list(map(int, sentence_numbers))
    return sentence_numbers


def get_sentence_from_db(counter, __list_of_sentence_numbers):

    current_sentence_number = __list_of_sentence_numbers[counter]
    connect_to_db()
    selected_sentence_query = "select Word from parseddocument where LetterType='testing' and SentenceNumber = " + \
                              str(current_sentence_number)

    cur.execute(selected_sentence_query)

    current_sentence = cur.fetchall()
    current_sentence = sorted(set(current_sentence), key=lambda x: current_sentence.index(x))
    current_sentence = [eachTuple[0] for eachTuple in current_sentence]

    return current_sentence, current_sentence_number


def read_csv_file_of_a_predicted_sentence(filename):
    path_of_file = 'D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample\\' + filename
    rnn_output_of_current_sentence = []
    with open(path_of_file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')

        for row in reader:
            rnn_output_of_current_sentence.append(map(float, row))

        return rnn_output_of_current_sentence


def get_neurons_numbers_with_highest_output_value(rnn_output):
    list_0f_neurons_indices_with_highest_value = []
    # Take care !!!, that the array is zero index
    for row in rnn_output:
        list_0f_neurons_indices_with_highest_value.append(row.index(max(row)))

    return list_0f_neurons_indices_with_highest_value


def get_all_letters_from_db():
    list_of_all_diacritized_letters_query = "select DiacritizedCharacter from diaconehotencoding"

    cur.execute(list_of_all_diacritized_letters_query)

    db_diacritized_letters = cur.fetchall()
    db_diacritized_letters = [eachTuple[0] for eachTuple in db_diacritized_letters]

    return db_diacritized_letters


def get_actual_letters(list_of_all_diacritized_letters, neurons_locations_with_highest_output):

    list_of_actual_letters_before_sukun_correction = []
    for neuron_location in neurons_locations_with_highest_output:
        # Take care, we make +1 because "neurons_locations_with_highest_output" is zero index
        list_of_actual_letters_before_sukun_correction.append(list_of_all_diacritized_letters[neuron_location - 1])

    return list_of_actual_letters_before_sukun_correction


def get_expected_letters(__sentence_number):

    list_of_expected_diacritized_letters_query = "select DiacritizedCharacter from parseddocument where " \
                                                 "LetterType='testing' and SentenceNumber = " + str(__sentence_number)

    cur.execute(list_of_expected_diacritized_letters_query)

    db_expected_letters_before_sukun_correction = cur.fetchall()
    db_expected_letters_before_sukun_correction = \
        [eachTuple[0] for eachTuple in db_expected_letters_before_sukun_correction]

    return db_expected_letters_before_sukun_correction


def sukun_correction(list_of_actual_letters_before_sukun_correction, list_of_expected_letters_before_sukun_correction):

    list_of_actual_letters_after_sukun_correction = []
    list_of_expected_letters_after_sukun_correction = []

    for each_actual_character, each_expected_letter in zip(list_of_actual_letters_before_sukun_correction,
                                                           list_of_expected_letters_before_sukun_correction):

        list_of_actual_letters_after_sukun_correction.append(remove_sukun_diacritics_if_exists(each_actual_character))
        list_of_expected_letters_after_sukun_correction.append(remove_sukun_diacritics_if_exists(each_expected_letter))

    return list_of_actual_letters_after_sukun_correction, list_of_expected_letters_after_sukun_correction


def remove_sukun_diacritics_if_exists(letter):
    normalized_char = unicodedata.normalize('NFC', letter)

    if u'ْ' in normalized_char:
        for c in normalized_char:
            if not unicodedata.combining(c):
                return unicodedata.normalize('NFC', c)
    else:
        return letter


def get_chars_count_for_each_word_in_current_sentence(sentence):

    count = 0
    chars_count_of_each_word = []
    for each_word in sentence:
        for each_char in each_word:
            if not unicodedata.combining(each_char):
                count += 1
        chars_count_of_each_word.append(count)
        count = 0
    '''
    list_of_location_of_last_characters_query = "select Word from parseddocument " \
                                                "where LetterType='testing' and SentenceNumber =" + \
                                                str(sentence_number) + " order by idCharacterNumber asc"

    cur.execute(list_of_location_of_last_characters_query)

    list_of_required_info = cur.fetchall()
    list_of_required_info = [each_word[0] for each_word in list_of_required_info]
    list_of_each_word_in_selected_sentence_and_its_count = [(k, sum(1 for i in g)) for k, g in
                                                              groupby(list_of_required_info)]

    chars_count_of_each_word = []
    for each_word in list_of_each_word_in_selected_sentence_and_its_count:
        chars_count_of_each_word.append(each_word[1])
    '''
    return chars_count_of_each_word


def get_location_of_each_character_in_current_sentence(__list_of_actual_letters, __chars_count_for_each_word_in_current_sentence):

    list_of_actual_letters_with_its_location = []
    i = 0

    for count_of_letters in __chars_count_for_each_word_in_current_sentence:
        letter_position_object = LetterPosition()
        for x in range(0, count_of_letters):
            if count_of_letters == 1:
                letter_position_object.letter = __list_of_actual_letters[i]
                letter_position_object.location = 'firstOneLetter'
                list_of_actual_letters_with_its_location.append(deepcopy(letter_position_object))

            else:
                if x == 0:
                    letter_position_object.letter = __list_of_actual_letters[i]
                    letter_position_object.location = 'first'
                    list_of_actual_letters_with_its_location.append(deepcopy(letter_position_object))

                elif x == (count_of_letters - 1):
                    letter_position_object.letter = __list_of_actual_letters[i]
                    letter_position_object.location = 'last'
                    list_of_actual_letters_with_its_location.append(deepcopy(letter_position_object))

                else:
                    letter_position_object.letter = __list_of_actual_letters[i]
                    letter_position_object.location = 'middle'
                    list_of_actual_letters_with_its_location.append(deepcopy(letter_position_object))

            i += 1

    return list_of_actual_letters_with_its_location


def fatha_correction(__list_of_actual_letters_with_its_location):
    counter = 0
    actual_letters_after_fatha_correction = []

    for each_letter_object in __list_of_actual_letters_with_its_location:
        actual_letters_after_fatha_correction.append((each_letter_object))
        if ((each_letter_object.letter) in letters_of_fatha_correction) and (each_letter_object.location != 'first'):

            # get prev char
            spaChar = unicodedata.normalize('NFC', ((__list_of_actual_letters_with_its_location[counter - 1]).letter))
            for c in spaChar:
                if not unicodedata.combining(c):
                    overall = c
                    comp = unicodedata.normalize('NFC', c)
                    actual_letters_after_fatha_correction[counter - 1].letter = comp

                elif c == u'َ' or c == u'ّ' or c == u'ً':
                    overall += c
                    comp = unicodedata.normalize('NFC', overall)
                    actual_letters_after_fatha_correction[counter - 1].letter = comp

                else:
                    if each_letter_object.location == 'middle':
                        c = u'َ'
                    elif each_letter_object.location == 'last':
                        c = u'ً'
                    overall += c
                    comp = unicodedata.normalize('NFC', overall)
                    actual_letters_after_fatha_correction[counter - 1].letter = comp
            counter += 1
        else:
            counter += 1

        #counter += 1

    return actual_letters_after_fatha_correction


def reform_word_after_sukun_and_fatha_correction(list_of_chars_with_its_position):
    list_of_words = []
    word = ""
    for each_char_object in list_of_chars_with_its_position:
        if each_char_object.location == 'firstOneLetter':
            list_of_words.append(each_char_object.letter)
        elif each_char_object.location != 'last':
            word += each_char_object.letter
        elif each_char_object.location == 'last':
            word += each_char_object.letter
            list_of_words.append(word)
            word = ""

    return list_of_words





def get_all_un_words_of_this_sentence_from_db(sentence_number):
    undiacritized_word_in_selected_sentence_query = "select distinct UnDiacritizedWord from parseddocument where LetterType='testing' and SentenceNumber = " + \
                              str(sentence_number)

    cur.execute(undiacritized_word_in_selected_sentence_query)

    undiacritized_word_in_selected_sentence = (cur.fetchall())
    undiacritized_word_in_selected_sentence = [each_tuple[0] for each_tuple in undiacritized_word_in_selected_sentence]

    return undiacritized_word_in_selected_sentence
def get_diac_version_with_smallest_dist(list_of_corrected_diacritized_words, list_of_undiacritized_words):

    list_of_actual_words_after_dictionary_correction = []
    for each_un_diacritized_word, each_corrected_word in zip(list_of_undiacritized_words, list_of_corrected_diacritized_words):
        dictionary_diacritized_words = get_corresponding_diacritized_versions(each_un_diacritized_word)
        for each_word in dictionary_diacritized_words:

            decomposed_dic_word, decomposed_act_word = decompose_word_into_letters(each_word, each_corrected_word)
            norm_dic_word, norm_act_word = normalize_words_under_comparison(decomposed_dic_word, decomposed_act_word)

            for each_diacritized_version_letter, each_current_word_letter in zip(norm_dic_word, norm_act_word):

                if (len(each_diacritized_version_letter) - len(each_current_word_letter) == 1) or (
                        (len(each_diacritized_version_letter) - len(each_current_word_letter) == -1)):
                    error_count += 1

                elif (len(each_diacritized_version_letter) - len(each_current_word_letter) == 2) or (
                        (len(each_diacritized_version_letter) - len(each_current_word_letter) == -2)):
                    error_count += 2

                else:
                    for each_item_in_diacritized_version, each_item_in_current_word in zip(each_diacritized_version_letter, each_current_word_letter):
                        if each_item_in_diacritized_version != each_item_in_current_word:
                            error_count += 1

            if error_count < min:
                min = error_count
                selected_dictionary_word = each_word

        list_of_actual_words_after_dictionary_correction.append(selected_dictionary_word)

    return list_of_actual_words_after_dictionary_correction
def get_corresponding_diacritized_versions(word):
    connect_to_db()

    selected_sentence_query = "select DiacritizedWord from dictionary where  UnDiacritizedWord = " + "'" +word + "'"
    cur.execute(selected_sentence_query)
    corresponding_diacritized_words = cur.fetchall()
    corresponding_diacritized_words = [each_word[0] for each_word in corresponding_diacritized_words]


    return corresponding_diacritized_words
def decompose_word_into_letters(word_in_dictionary, actual_word):
    decomposed_dictionary_word = []
    decomposed_actual_word = []
    inter_med_list = []
    letterFoundFlag = False
    for each_letter in word_in_dictionary:
        if not unicodedata.combining(each_letter):
            if letterFoundFlag:
                decomposed_dictionary_word.append(inter_med_list)
            inter_med_list = []
            inter_med_list.append(each_letter)
            letterFoundFlag = True

        elif letterFoundFlag:
            inter_med_list.append(each_letter)
    # required because last character will not be added above, but here
    decomposed_dictionary_word.append(inter_med_list)

    inter_med_list = []
    letterFoundFlag = False
    for each_letter in actual_word:
        if not unicodedata.combining(each_letter):
            if letterFoundFlag:
                decomposed_actual_word.append(inter_med_list)
            inter_med_list = []
            inter_med_list.append(each_letter)
            letterFoundFlag = True

        elif letterFoundFlag:
            inter_med_list.append(each_letter)
            # required because last character will not be added above, but here
    decomposed_actual_word.append(inter_med_list)

    return decomposed_dictionary_word, decomposed_actual_word
def normalize_words_under_comparison(word_in_dictionary, actual_word):

    locale.setlocale(locale.LC_ALL, "")
    for x in range(0, len(word_in_dictionary)):
        word_in_dictionary[x].sort(cmp=locale.strcoll)

    locale.setlocale(locale.LC_ALL, "")
    for x in range(0, len(actual_word)):
        actual_word[x].sort(cmp=locale.strcoll)
    return word_in_dictionary, actual_word















def get_diacritization_error(actual_letters, expected_letters):
    actual_letters_errors = []
    expected_letters_errors = []
    global total_error

    number_of_diacritization_errors = 0
    letter_location = 0
    error_locations = []

    for actual_letters, expected_letter in zip(actual_letters, expected_letters):
        letter_location += 1
        if actual_letters.letter != expected_letter:
            actual_letters_errors.append(actual_letters.letter)
            expected_letters_errors.append(expected_letter)
            error_locations.append(letter_location)
            number_of_diacritization_errors += 1

    total_error += number_of_diacritization_errors

    print 'total error in this sentence', number_of_diacritization_errors
    print 'total error in all sentences: ', total_error

    return actual_letters_errors, expected_letters_errors, error_locations


def write_data_into_excel_file(actual_letters_errors, expected_letters_errors, error_locations, current_sentence):
    wb = open_workbook(diacritization_error_excel_file_path)
    w = copy(wb)
    worksheet = w.get_sheet(0)

    global current_row_in_excel_file
    current_row_in_excel_file += 1
    column = 0

    for actual_letter, expected_letter, location in \
            zip(actual_letters_errors, expected_letters_errors, error_locations):

        worksheet.write(current_row_in_excel_file, column, actual_letter)

        column = 1
        worksheet.write(current_row_in_excel_file, column, expected_letter)

        column = 2
        worksheet.write(current_row_in_excel_file, column, location)

        current_row_in_excel_file += 1
        column = 0

    all_sentence = ''
    for each_word in current_sentence:
        all_sentence += each_word + ' '

    worksheet.write(current_row_in_excel_file, column, all_sentence)

    current_row_in_excel_file += 1

    w.save(diacritization_error_excel_file_path)
    workbook.close()


if __name__ == "__main__":
    connect_to_db()
    list_of_sentence_numbers = get_list_of_sentence_numbers()

    os.chdir(path)
    result = [i for i in glob.glob('*.{}'.format(extension))]
    current_sentence_counter = 0

    for file_name in result:
        selected_sentence, sentence_number = get_sentence_from_db(current_sentence_counter, list_of_sentence_numbers)

        rnn_output_for_one_seq = read_csv_file_of_a_predicted_sentence(file_name)

        neurons_locations_with_highest_output_for_a_seq = \
            get_neurons_numbers_with_highest_output_value(rnn_output_for_one_seq)

        connect_to_db()

        list_of_diacritized_letters = get_all_letters_from_db()

        actual_letters_before_sukun_correction = get_actual_letters(list_of_diacritized_letters,
                                                                    neurons_locations_with_highest_output_for_a_seq)

        expected_letters_before_sukun_correction = get_expected_letters(sentence_number)

        actual_letters_after_sukun_correction, expected_letters_after_sukun_correction = \
            sukun_correction(actual_letters_before_sukun_correction, expected_letters_before_sukun_correction)

        chars_count_for_each_word_in_current_sentence = get_chars_count_for_each_word_in_current_sentence(selected_sentence)

        location_of_each_char = get_location_of_each_character_in_current_sentence(actual_letters_after_sukun_correction, chars_count_for_each_word_in_current_sentence)

        actual_letters_after_sukun_and_fatha_correction = fatha_correction(location_of_each_char)

        list_of_words_in_sent_after_sukun_and_fatha_correction = reform_word_after_sukun_and_fatha_correction(actual_letters_after_sukun_and_fatha_correction)

        connect_to_db()
        list_of_undiacritized_words_in_current_sentence = get_all_un_words_of_this_sentence_from_db(sentence_number)
        get_diac_version_with_smallest_dist(list_of_words_in_sent_after_sukun_and_fatha_correction, list_of_undiacritized_words_in_current_sentence)








        list_of_actual_letters_errors, list_of_expected_letters_errors, list_of_error_locations = \
            get_diacritization_error(actual_letters_after_sukun_and_fatha_correction, expected_letters_after_sukun_correction)

        write_data_into_excel_file(list_of_actual_letters_errors, list_of_expected_letters_errors,
                                   list_of_error_locations, selected_sentence)

        current_sentence_counter += 1
        print 'sentence number: ', current_sentence_counter

