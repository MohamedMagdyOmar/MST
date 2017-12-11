import unittest

import MySQLdb
import MySQLdb.cursors

class MyTestCase1(unittest.TestCase):
    selected_words = []
    # Only use setUp() and tearDown() if necessary

    def setUp(self):
        class LetterPosition:
            letter = "",
            location = ""

            def __init__(self):
                self.letter = ""
                self.location = ""

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

        selected_words_query = "select distinct word, DiacritizedCharacter from parseddocument where UnDiacritizedCharacter = (select arabic_letter from arabic_letters_without_diacritics where id = 7)"
        cur.execute(selected_words_query)
        selected_words1 = (cur.fetchall())
        selected_words1 = [each_number[0] for each_number in selected_words1]
        selected_letters1 = [each_number[1] for each_number in selected_words1]

        selected_words_query = "select distinct word, DiacritizedCharacter from parseddocument where UnDiacritizedCharacter = (select arabic_letter from arabic_letters_without_diacritics where id = 2)"
        cur.execute(selected_words_query)
        selected_words2 = (cur.fetchall())
        selected_words2 = [each_number[0] for each_number in selected_words2]
        selected_letters2 = [each_number[1] for each_number in selected_words2]


        selected_words_query = "select distinct word, DiacritizedCharacter from parseddocument where UnDiacritizedCharacter = (select arabic_letter from arabic_letters_without_diacritics where id = 34)"
        cur.execute(selected_words_query)
        selected_words3 = (cur.fetchall())
        selected_words3 = [each_number[0] for each_number in selected_words3]
        selected_letters3 = [each_number[1] for each_number in selected_words3]


        selected_words = []
        selected_letters = []
        selected_words = selected_words1 + selected_words2 + selected_words3
        for each_word in selected_words:
            for each_letter in each_word:
                selected_letters.append(each_letter)
        x = 1


    def tearDown(self):
        x = 1

    def test_feature_one(self):
        # Test feature one.
        x = 1

    def test_feature_two(self):
        # Test feature two.
        x = 1



