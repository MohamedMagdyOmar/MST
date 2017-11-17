# -*- coding: utf-8 -*-

import csv
import xlsxwriter
import MySQLdb
import MySQLdb.cursors
import os
import glob
import unicodedata
from xlrd import open_workbook
from itertools import groupby
from xlutils.copy import copy
import locale

final_list_of_actual_letters_after_post_processing = []
final_list_of_word = []
rnn_output_for_one_seq = []
neurons_locations_with_highest_output_for_a_seq = []
list_of_all_diacritized_letters = []

list_of_actual_letters_before_sukun_correction = []
list_of_expected_letters_before_sukun_correction = []

dictionary_correction_list = []

list_of_actual_letters = []
list_of_expected_letters = []
list_of_testing_words = []
list_of_actual_letters_errors = []
list_of_expected_letters_errors = []


# letters_of_fatha_correction = [u'ة', u'ا', u'ى']
letters_of_fatha_correction = [u'ة', u'ى']
locations_of_fatha_correction_letters = []
list_of_location_types = []
total_error = 0
sentence_number = 0

row_of_letters_excel_file = 0

path = 'D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample'
diacritization_error_excel_file_path = "D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample\Errors" \
                                       "\Book1.xls "
extension = 'csv'

row_of_errors_excel_file = 1
last_character_location = 0

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
        list_of_actual_letters_before_sukun_correction.append(list_of_all_diacritized_letters[neuron_location + 1])

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
    intermediate_list = []
    first_time = True
    counter = 1

    for each_letter, each_index in zip(__list_of_actual_letters, __chars_count_for_each_word_in_current_sentence):

        if each_index == 1:
            intermediate_list.append(each_letter)
            intermediate_list.append('firstOneLetter')
            list_of_actual_letters_with_its_location.append(intermediate_list)
            intermediate_list = []
            counter = 1

        else:

            if first_time:
                intermediate_list.append(each_letter)
                intermediate_list.append('first')
                list_of_actual_letters_with_its_location.append(intermediate_list)
                intermediate_list = []
                first_time = False
                counter += 1
            elif counter < each_index:
                intermediate_list.append(each_letter)
                intermediate_list.append('middle')
                list_of_actual_letters_with_its_location.append(intermediate_list)
                intermediate_list = []
                first_time = False
                counter += 1

            elif counter == each_index:
                intermediate_list.append(each_letter)
                intermediate_list.append('last')
                list_of_actual_letters_with_its_location.append(intermediate_list)
                intermediate_list = []
                first_time = True
                counter = 1

    return list_of_actual_letters_with_its_location


def fatha_correction(__list_of_actual_letters_with_its_location):
    counter = 0
    actual_letters_after_fatha_correction = []

    for each_letter in __list_of_actual_letters_with_its_location:
        actual_letters_after_fatha_correction.append((each_letter[0]))
        if ((each_letter[0]) in letters_of_fatha_correction) and (each_letter[1] != 'first'):

            # get prev char
            spaChar = unicodedata.normalize('NFC', ((__list_of_actual_letters_with_its_location[counter - 1])[0]))
            for c in spaChar:
                if not unicodedata.combining(c):
                    overall = c
                    comp = unicodedata.normalize('NFC', c)
                    actual_letters_after_fatha_correction[counter - 1] = comp

                elif c == u'َ' or c == u'ّ' or c == u'ً':
                    overall += c
                    comp = unicodedata.normalize('NFC', overall)
                    actual_letters_after_fatha_correction[counter - 1] = comp

                else:
                    if each_letter[1] == 'middle':
                        c = u'َ'
                    elif each_letter[1] == 'last':
                        c = u'ً'
                    overall += c
                    comp = unicodedata.normalize('NFC', overall)
                    actual_letters_after_fatha_correction[counter - 1] = comp
            counter += 1
        else:
            counter += 1

        #counter += 1

    return actual_letters_after_fatha_correction


def reform_word_after_sukun_and_fatha_correction(list_of_chars):

    



def get_diacritization_error():
    global list_of_actual_letters_errors
    global list_of_expected_letters_errors
    global total_error

    number_of_diacritization_errors = 0
    counter = 0
    letter_location = 0
    list_of_error_locations = []
    for letter in final_list_of_actual_letters:
    #uncommnet below line and comment above line if dictionary correction is needed
    #for letter in final_list_of_actual_letters_after_post_processing:
        letter_location += 1
        #if (letter[0] != (list_of_expected_letters[counter])[0]):# and (not(letter_location in location_of_last_character)):
        if (letter != (list_of_expected_letters[counter])[0]):
            list_of_actual_letters_errors.append(letter)
            list_of_expected_letters_errors.append(list_of_expected_letters[counter])
            list_of_error_locations.append(letter_location)
            number_of_diacritization_errors += 1

        counter += 1

    total_error += number_of_diacritization_errors

    print number_of_diacritization_errors
    print 'total error: ', total_error

    wb = open_workbook(diacritization_error_excel_file_path)
    w = copy(wb)
    worksheet = w.get_sheet(0)

    global row_of_errors_excel_file
    row_of_errors_excel_file += 1

    column = 0
    i = 0
    for expected_letter, actual_letter in zip(list_of_expected_letters_errors, list_of_actual_letters_errors):
        worksheet.write(row_of_errors_excel_file, column, expected_letter[0])

        column = 1
        worksheet.write(row_of_errors_excel_file, column, actual_letter)

        column = 2
        worksheet.write(row_of_errors_excel_file, column, list_of_error_locations[i])

        i += 1
        row_of_errors_excel_file += 1
        column = 0

    all_sentence = ''
    for each_word in current_sentence:
        all_sentence += each_word[0] + ' '

    worksheet.write(row_of_errors_excel_file, column, all_sentence)

    row_of_errors_excel_file += 1

    w.save(diacritization_error_excel_file_path)

    workbook.close()

    list_of_actual_letters_errors = []
    list_of_expected_letters_errors = []


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

        actual_letters_after_fatha_correction = fatha_correction(location_of_each_char)
        reform_word_after_sukun_and_fatha_correction(actual_letters_after_fatha_correction)

        # write_data_into_excel_file('D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample\Book2.xlsx')
        get_diacritization_error()
        currentSentence += 1
        print 'sentence number: ', currentSentence
        sentence_number += 1
