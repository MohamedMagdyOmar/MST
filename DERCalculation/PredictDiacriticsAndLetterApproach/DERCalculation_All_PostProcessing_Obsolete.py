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
final_list_of_actual_letters = []
dictionary_correction_list = []

list_of_actual_letters = []
list_of_expected_letters = []
list_of_testing_words = []
list_of_actual_letters_errors = []
list_of_expected_letters_errors = []
current_sentence = []
list_of_required_info = []
location_of_last_character = []

list_of_actual_letters_with_its_location = []

letters_of_fatha_correction = [u'ة', u'ا', u'ى']
locations_of_fatha_correction_letters = []
list_of_location_types = []
total_error = 0
sentence_number = 0
currentSentence = 0
row_of_letters_excel_file = 0
first_time = True
path = 'D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample'
diacritization_error_excel_file_path = "D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample\Errors" \
                                       "\Book1.xls "
extension = 'csv'

row_of_errors_excel_file = 1
last_character_location = 0

workbook = xlsxwriter.Workbook(diacritization_error_excel_file_path)
worksheet = workbook.add_worksheet()
worksheet.write(0, 0, 'Expected')
worksheet.write(0, 1, 'Actual')
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


def get_number_of_first_testing_sentence():
    sentence_number_of_testing_query = "select SentenceNumber from parseddocument where LetterType='testing' limit 1"

    cur.execute(sentence_number_of_testing_query)

    global sentence_number
    sentence_number = (cur.fetchall())
    sentence_number = int((sentence_number[0])[0])


def get_sentence_from_db():
    connect_to_db()
    selected_sentence_query = "select Word from parseddocument where LetterType='testing' and SentenceNumber = " + \
                              str(sentence_number)

    cur.execute(selected_sentence_query)

    global current_sentence
    current_sentence = cur.fetchall()
    current_sentence = sorted(set(current_sentence), key=lambda x: current_sentence.index(x))


def read_csv_file(filename):
    path_of_file = 'D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample\\' + filename

    # with open('D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample\\1.csv', 'rb') as csvfile:

    with open(path_of_file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        global rnn_output_for_one_seq
        rnn_output_for_one_seq = []
        for row in reader:
            rnn_output_for_one_seq.append(map(float, row))


def get_neurons_numbers_with_highest_output_value():
    global rnn_output_for_one_seq
    global neurons_locations_with_highest_output_for_a_seq
    neurons_locations_with_highest_output_for_a_seq = []
    for row in rnn_output_for_one_seq:
        neurons_locations_with_highest_output_for_a_seq.append(row.index(max(row)))


def get_all_letters_from_db():
    list_of_all_diacritized_letters_query = "select DiacritizedCharacter from diaconehotencoding"

    cur.execute(list_of_all_diacritized_letters_query)

    global list_of_all_diacritized_letters
    list_of_all_diacritized_letters = cur.fetchall()


def get_actual_letters():

    global list_of_actual_letters_before_sukun_correction
    list_of_actual_letters_before_sukun_correction = []

    global neurons_locations_with_highest_output_for_a_seq
    for neuron_location in neurons_locations_with_highest_output_for_a_seq:
        list_of_actual_letters_before_sukun_correction.append(list_of_all_diacritized_letters[neuron_location - 1])


def get_expected_letters():
    global sentence_number
    list_of_expected_diacritized_letters_query = "select DiacritizedCharacter from parseddocument where " \
                                                 "LetterType='testing' and SentenceNumber = " + str(sentence_number)

    cur.execute(list_of_expected_diacritized_letters_query)

    global list_of_expected_letters_before_sukun_correction
    list_of_expected_letters_before_sukun_correction = []
    list_of_expected_letters_before_sukun_correction = cur.fetchall()


def sukun_correction():
    global list_of_actual_letters
    list_of_actual_letters = []

    global list_of_expected_letters
    list_of_expected_letters = []

    for each_character in list_of_actual_letters_before_sukun_correction:
        spaChar = unicodedata.normalize('NFC', each_character[0])
        if u'ْ' in spaChar:
            for c in spaChar:
                if not unicodedata.combining(c):
                    list_of_actual_letters.append(tuple(unicodedata.normalize('NFC', c)))
        else:
            list_of_actual_letters.append(each_character)

    for each_character in list_of_expected_letters_before_sukun_correction:
        spaChar = unicodedata.normalize('NFC', each_character[0])
        if u'ْ' in spaChar:
            for c in spaChar:
                if not unicodedata.combining(c):
                    list_of_expected_letters.append(tuple(unicodedata.normalize('NFC', c)))
        else:
            list_of_expected_letters.append(each_character)


def sukun_correction_for_dictionary_words(dictionary_list):
    dictionary_words_without_sukun = []
    overall = ""
    for each_row in dictionary_list:
        for each_char in each_row[1]:
            spaChar = unicodedata.normalize('NFC', each_char)
            if u'ْ' in spaChar:
                    if not unicodedata.combining(spaChar):
                        overall += spaChar
                        dictionary_words_without_sukun.append(unicodedata.normalize('NFC', overall))
            else:
                overall += spaChar
        dictionary_words_without_sukun.append(unicodedata.normalize('NFC', overall))
        overall = ""

    counter_x = 0

    # convert dictionary_list to list of list to be able to assign values
    list_of_lists = [list(elem) for elem in list(dictionary_list)]
    for each_word in dictionary_words_without_sukun:
        (list_of_lists[counter_x])[1] = each_word
        counter_x += 1

    return list_of_lists


def write_data_into_excel_file(path_of_file):
    global first_time
    if first_time:
        workbook = xlsxwriter.Workbook(path_of_file)
        worksheet = workbook.add_worksheet()

    else:
        wb = open_workbook(path_of_file)
        w = copy(wb)
        worksheet = w.get_sheet(0)

    global row_of_letters_excel_file
    row_of_letters_excel_file += 1

    column = 0

    for expected_letter, actual_letter in zip(list_of_expected_letters, list_of_actual_letters):
        worksheet.write(row_of_letters_excel_file, column, expected_letter[0])
        column = 1
        worksheet.write(row_of_letters_excel_file, column, actual_letter[0])
        row_of_letters_excel_file += 1
        column = 0

    row_of_letters_excel_file += 1

    if not first_time:
        w.save(path_of_file)

    first_time = False
    workbook.close()


def get_location_of_last_characters_in_current_sentence():

    list_of_location_of_last_characters_query = "select Word from parseddocument " \
                                                "where LetterType='testing' and SentenceNumber =" + \
                                                str(sentence_number) + " order by idCharacterNumber asc"

    cur.execute(list_of_location_of_last_characters_query)
    global list_of_required_info
    list_of_required_info = []
    list_of_required_info = cur.fetchall()

    grouped_testing_words_with_consecutive_repeated_number = [(k, sum(1 for i in g)) for k, g in
                                                              groupby(list_of_required_info)]

    global last_character_location
    global location_of_last_character
    location_of_last_character = []
    summation = 0
    for each_word in grouped_testing_words_with_consecutive_repeated_number:
        location_of_last_character.append(each_word[1] + summation)
        summation += each_word[1]


def fatha_correction():
    counter = 0
    global final_list_of_actual_letters
    final_list_of_actual_letters = []

    for each_letter in list_of_actual_letters_with_its_location:
        final_list_of_actual_letters.append((each_letter[0])[0])
        if ((each_letter[0])[0] in letters_of_fatha_correction) and (each_letter[1] != 'first'):
            spaChar = unicodedata.normalize('NFC', ((list_of_actual_letters_with_its_location[counter - 1])[0])[0])
            for c in spaChar:
                if not unicodedata.combining(c):
                    overall = c
                    comp = unicodedata.normalize('NFC', c)
                    final_list_of_actual_letters[counter - 1] = comp

                elif c == u'َ' or c == u'ّ' or c == u'ً':
                    overall += c
                    comp = unicodedata.normalize('NFC', overall)
                    final_list_of_actual_letters[counter - 1] = comp

                else:
                    if each_letter[1] == 'middle':
                        c = u'َ'
                    else:
                        c = u'ً'
                    overall += c
                    comp = unicodedata.normalize('NFC', overall)
                    final_list_of_actual_letters[counter - 1] = comp
            counter += 1
        else:
            counter += 1

    counter += 1


def get_location_of_each_character_in_current_sentence():

    global list_of_actual_letters
    global location_of_last_character
    global list_of_actual_letters_with_its_location
    list_of_actual_letters_with_its_location = []
    intermediate_list = []

    first_time = True

    counter_x = 1
    counter_y = 0
    for each_letter in list_of_actual_letters:
        if first_time:
            intermediate_list.append(each_letter)
            intermediate_list.append('first')
            list_of_actual_letters_with_its_location.append(intermediate_list)
            intermediate_list = []
            first_time = False
            counter_x += 1
        elif counter_x < location_of_last_character[counter_y]:
            intermediate_list.append(each_letter)
            intermediate_list.append('middle')
            list_of_actual_letters_with_its_location.append(intermediate_list)
            intermediate_list = []
            first_time = False
            counter_x += 1

        elif counter_x == location_of_last_character[counter_y]:
            intermediate_list.append(each_letter)
            intermediate_list.append('last')
            list_of_actual_letters_with_its_location.append(intermediate_list)
            intermediate_list = []
            first_time = True
            counter_x += 1
            counter_y += 1

    x = 1


def reform_word():

    global list_of_actual_letters_with_its_location
    global final_list_of_actual_letters
    global dictionary_correction_list
    global final_list_of_word
    final_list_of_word = []
    dictionary_correction_list = []
    med_list = []

    for x in range(0, len(list_of_actual_letters_with_its_location)):
        letter = ((list_of_actual_letters_with_its_location[x])[0])[0]
        position = ((list_of_actual_letters_with_its_location[x])[1])
        med_list.append(letter)
        med_list.append(position)
        dictionary_correction_list.append(med_list)
        med_list = []

    counter = 0
    for each_letter in final_list_of_actual_letters:
        (dictionary_correction_list[counter])[0] = each_letter
        counter += 1

    word = ""
    list_of_words = []

    # re-form the words from the actual o/p letters
    for each_row in dictionary_correction_list:
        if each_row[1] != 'last':
            word += each_row[0]
        else:
            word += each_row[0]
            list_of_words.append(word)
            word = ""
    undiacritized_version_list = get_undiacritized_version(list_of_words)

    counter_x = 0
    for each_word in undiacritized_version_list:
        diacritized_versions = get_corresponding_diacritized_versions(each_word)
        if len(diacritized_versions) == 0:
            final_list_of_word.append(list_of_words[counter_x])
        else:
            dictionary_words_after_removing_sukun = sukun_correction_for_dictionary_words(diacritized_versions)
            final_list_of_word.append(get_diac_version_with_smallest_dist(dictionary_words_after_removing_sukun,
                                                                          list_of_words[counter_x]))
        counter_x += 1

    overall = ""
    comp = ""
    letterFoundFlag = False
    global final_list_of_actual_letters_after_post_processing
    final_list_of_actual_letters_after_post_processing = []
    for each_word in final_list_of_word:
        for each_letter in each_word:
            if not unicodedata.combining(each_letter):
                if letterFoundFlag:
                    final_list_of_actual_letters_after_post_processing.append(tuple([comp]))

                overall = each_letter
                letterFoundFlag = True
                comp = unicodedata.normalize('NFC', overall)
            elif letterFoundFlag:
                overall += each_letter
                comp = unicodedata.normalize('NFC', overall)

    x = 1


def get_undiacritized_version(list_of_words):
    overall = ""
    comp = ""
    undiacritized_list = []
    for each_word in list_of_words:
        spaChar = unicodedata.normalize('NFC', each_word)
        for c in spaChar:
            if not unicodedata.combining(c):
                overall += c
                comp = unicodedata.normalize('NFC', overall)

        undiacritized_list.append(comp)
        overall = ""
        comp = ""
    return undiacritized_list


def get_corresponding_diacritized_versions(word):
    connect_to_db()

    selected_sentence_query = "select * from dictionary"
    cur.execute(selected_sentence_query)
    dictionary_outcome = cur.fetchall()


    return [t for t in dictionary_outcome if unicodedata.normalize('NFC', t[2]) == word]


def get_diac_version_with_smallest_dist(diacritized_versions, current_word):
    min = 100000000
    final_selected_word = ""

    current_word_list = list(current_word)
    inter_med_list = []
    letterFoundFlag = False
    final_list_for_current_word = []
    for each_letter in current_word_list:
        if not unicodedata.combining(each_letter):
            if letterFoundFlag:
                final_list_for_current_word.append(inter_med_list)

            inter_med_list = []
            inter_med_list.append(each_letter)
            letterFoundFlag = True

        elif letterFoundFlag:
            inter_med_list.append(each_letter)

    # required because last character will not be added above, but here
    final_list_for_current_word.append(inter_med_list)

    locale.setlocale(locale.LC_ALL, "")
    for x in range(0, len(final_list_for_current_word)):
        final_list_for_current_word[x].sort(cmp=locale.strcoll)


    for each_diac_word in diacritized_versions:
        # convert first dictionary word in the form of list of objects [letter, and diacritization]
        final_list_for_diacritized_version = []
        inter_med_list = []
        letterFoundFlag = False
        for each_letter in each_diac_word[1]:
            if not unicodedata.combining(each_letter):
                if letterFoundFlag:
                    final_list_for_diacritized_version.append(inter_med_list)

                inter_med_list = []
                inter_med_list.append(each_letter)
                letterFoundFlag = True

            elif letterFoundFlag:
                inter_med_list.append(each_letter)

        # required because last character will not be added above, but here
        final_list_for_diacritized_version.append(inter_med_list)

        for x in range(0, len(final_list_for_diacritized_version)):
            final_list_for_diacritized_version[x].sort(cmp=locale.strcoll)

        error_count = 0
        # calculating number of errors between selected dictionary word, and actual word
        for each_diacritized_version_letter, each_current_word_letter in zip(final_list_for_diacritized_version, final_list_for_current_word):
            if (len(each_diacritized_version_letter) - len(each_current_word_letter) == 1) or (
               (len(each_diacritized_version_letter) - len(each_current_word_letter) == -1)):
                error_count += 1

            elif (len(each_diacritized_version_letter) - len(each_current_word_letter) == 2) or (
               (len(each_diacritized_version_letter) - len(each_current_word_letter) == -2)):
                error_count += 2

            else:
                for each_item_in_diacritized_version, each_item_in_current_word in zip(each_diacritized_version_letter,each_current_word_letter):
                    if each_item_in_diacritized_version != each_item_in_current_word:
                        error_count += 1

        if error_count < min:
            min = error_count
            final_selected_word = each_diac_word[1]

    return final_selected_word


def get_diacritization_error():
    global list_of_actual_letters_errors
    global list_of_expected_letters_errors
    global total_error

    number_of_diacritization_errors = 0
    counter = 0
    letter_location = 0
    list_of_error_locations = []

    for letter in final_list_of_actual_letters_after_post_processing:
        letter_location += 1
        if (letter[0] != (list_of_expected_letters[counter])[0]):# and (not(letter_location in location_of_last_character)):
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
    get_number_of_first_testing_sentence()

    os.chdir(path)
    result = [i for i in glob.glob('*.{}'.format(extension))]

    for file_name in result:
        get_sentence_from_db()
        read_csv_file(file_name)
        get_neurons_numbers_with_highest_output_value()
        connect_to_db()
        get_all_letters_from_db()
        get_actual_letters()
        get_expected_letters()
        sukun_correction()
        get_location_of_last_characters_in_current_sentence()
        get_location_of_each_character_in_current_sentence()
        fatha_correction()
        reform_word()
        # write_data_into_excel_file('D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample\Book2.xlsx')
        get_diacritization_error()
        currentSentence += 1
        print 'sentence number: ', currentSentence
        sentence_number += 1
