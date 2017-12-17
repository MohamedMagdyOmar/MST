import MySQLdb
import MySQLdb.cursors


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


def get_list_of_sentence_numbers_by(sentence_type):

    connect_to_db()
    get_sentence_number_query = "select distinct SentenceNumber from parseddocument where LetterType = " + \
                                sentence_type + "order by idCharacterNumber asc "

    cur.execute(get_sentence_number_query)

    sentence_numbers = (cur.fetchall())
    sentence_numbers = [each_number[0] for each_number in sentence_numbers]
    sentence_numbers = list(map(int, sentence_numbers))

    return sentence_numbers


def get_sentence_by(sentence_number):

    connect_to_db()
    get_sentence_query = "select Word from listofwordsandsentencesineachdoc where SentenceNumber = " + \
                         str(sentence_number)

    cur.execute(get_sentence_query)

    current_sentence = cur.fetchall()
    current_sentence = [eachTuple[0] for eachTuple in current_sentence]

    return current_sentence


def get_all_diacritics():

    connect_to_db()
    get_all_diacritics_query = "select diacritics from distinctdiacritics"

    cur.execute(get_all_diacritics_query)

    distinct_diacritics = cur.fetchall()
    distinct_diacritics = [eachTuple[0] for eachTuple in distinct_diacritics]

    return distinct_diacritics


def get_un_diacritized_chars_by(sentence_number, sentence_type):

    connect_to_db()
    get_un_diacritized_chars_query = "select UnDiacritizedCharacter from parseddocument where " \
                                     "LetterType = " + sentence_type + "and SentenceNumber = " + str(sentence_number)

    cur.execute(get_un_diacritized_chars_query)

    un_diacritized_chars = cur.fetchall()
    un_diacritized_chars = [eachTuple[0] for eachTuple in un_diacritized_chars]

    return un_diacritized_chars


def get_diacritized_chars_by(sentence_number, sentence_type):

    connect_to_db()
    get_diacritized_chars_query = "select DiacritizedCharacter from parseddocument where " \
                                  "LetterType = " + sentence_type + "and SentenceNumber = " + str(sentence_number)

    cur.execute(get_diacritized_chars_query)

    diacritized_chars = cur.fetchall()
    diacritized_chars = [eachTuple[0] for eachTuple in diacritized_chars]

    return diacritized_chars


def get_available_diacritized_chars():

    connect_to_db()
    get_available_diacritized_chars_query = "select DiacritizedCharacter from diaconehotencoding"

    cur.execute(get_available_diacritized_chars_query)

    diacritized_chars = cur.fetchall()
    diacritized_chars = [eachTuple[0] for eachTuple in diacritized_chars]

    return diacritized_chars
