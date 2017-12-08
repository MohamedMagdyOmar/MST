# -*- coding: utf-8 -*-
import re
import unicodedata
import MySQLdb
import os

# 1 for atb3

pathOfDataFiles = "D:\MasterRepo\MSTRepo\PaperCorpus\Doc"
listOfPunctuationSymbols = [u' .', u'.', u' :', u'«', u'»', u'،', u'؛', u'؟', u'.(', u').', u':(', u'):', u'» .', u'».']
listOfArabicDiacriticsUnicode = [["064b", "064c", "064d", "064e", "064f", "0650", "0651", "0652", "0670"],
                                 [1, 2, 3, 4, 5, 6, 8, 7, 9]]
sentenceCount = 0


class DbObject:
    diacritizedCharacter = "",
    diacritizedWord = ""

    undiacritizedCharacter = "",
    undiacritizedWord = ""

    diacritics = "",
    sentenceNumber = 0

    def __init__(self):
        self.diacritizedCharacter = ""
        self.diacritizedWord = ""

        self.undiacritizedCharacter = ""
        self.undiacritizedWord = ""

        self.diacritics = ""
        self.sentenceNumber = ""


def read_selected_doc(path_of_selected_file):
    f = open(path_of_selected_file, 'r')
    data = f.readlines()
    f.close()
    return data


def clean_word_from_strange_characters(word):

    word = word.decode('utf-8', 'ignore')
    word = re.sub(u'[-;}()/]', '', word)
    word = re.sub(u'[-;}()0123456789/]', '', word)
    word = re.sub(u'["{"]', '', word)
    word = re.sub(u'[:]', ' :', word)
    word = re.sub(u'[_]', '', word)
    word = re.sub(u'[`]', '', word)
    word = re.sub(u'[[]', '', word)
    word = re.sub(u'[]]', '', word)
    word = re.sub(u'[L]', '', word)
    word = re.sub(u'[+]', '', word)
    word = re.sub(u'[!]', '', word)
    word = re.sub(u'[\']', '', word)
    word = re.sub(u'[...]', '', word)
    word = re.sub(u'[*]', '', word)
    word = re.sub(u'[&]', '', word)
    word = re.sub(u'[_]', '', word)
    word = re.sub(u'[q]', '', word)
    word = re.sub(u'[u]', '', word)
    word = re.sub(u'[o]', '', word)
    word = re.sub(u'[t]', '', word)
    word = re.sub(u'ٰ', '', word)
    word = re.sub(u'ـ', '', word)

    return word


def extract_and_clean_words_from_strange_character_from_doc_and_return_list_of_purified_words(data_file):
    listOfWords = []
    for eachSentence in data_file:
        wordsInSentence = eachSentence.split()
        for word in wordsInSentence:
            word = clean_word_from_strange_characters(word)

            if not (word == u''):
                listOfWords.append(word)

    return listOfWords


def bind_words_with_sentence_number_in_this_doc(doc):

    listOfWordsInDocAndCorrespondingSentenceNumber = []

    for eachSentence in doc:
        global sentenceCount
        # count sentence only if there is words in the sentence
        sentenceCounterFlag = True

        allWordsInSelectedSentence = eachSentence.split()

        for eachWord in allWordsInSelectedSentence:
            eachWord = clean_word_from_strange_characters(eachWord)
            if not (eachWord == u''):
                if sentenceCounterFlag:
                    sentenceCounterFlag = False
                    sentenceCount += 1
                listOfWordsInDocAndCorrespondingSentenceNumber.append([eachWord, str(sentenceCount)])

    return listOfWordsInDocAndCorrespondingSentenceNumber


def get_list_of_undiacritized_word_from_diacritized_word(list_of_extracted_words_without_numbers):

    listOfUnDiacritizedWord = []

    for word in list_of_extracted_words_without_numbers:
        if not word in listOfPunctuationSymbols:

            if word.find('.') != -1:
                word = re.sub('[.]', '', word)

            # word = word.decode('utf-8', 'ignore')
            nfkd_form = unicodedata.normalize('NFKD', word)

            unDiacritizedWord = u"".join([c for c in nfkd_form if not unicodedata.combining(c) or c == u'ٔ' or c == u'ٕ'])
            listOfUnDiacritizedWord.append(unDiacritizedWord)

    return listOfUnDiacritizedWord


def character_encoder(list_of_extracted_words_without_numbers):

    listOfEncodedCharacters = []
    listOfEncodedCharactersInHexFormat = []

    for word in list_of_extracted_words_without_numbers:
        if not word in listOfPunctuationSymbols:
            if word.find(u'.') != -1:
                word = re.sub(u'[.]', '', word)

            letterFoundFlag = False
            prevCharWasDiac = False

            for c in word:
                if not unicodedata.combining(c):  # letter
                    letterFoundFlag = True
                    hexAsString = hex(ord(c))[2:].zfill(4)
                    integer = int(hexAsString, 16)
                    maskedInt = integer & 255
                    shiftedInt = maskedInt << 4
                    listOfEncodedCharactersInHexFormat.append(hex(shiftedInt))
                    listOfEncodedCharacters.append(bin(shiftedInt)[2:].zfill(16))

                elif letterFoundFlag and c != u'ٔ' and c != u'ٕ':  # first diacritization
                    prevCharWasDiac = True
                    letterFoundFlag = False

                    hexDiacAsString = hex(ord(c))[2:].zfill(4)

                    integerDiac = listOfArabicDiacriticsUnicode[1][
                        listOfArabicDiacriticsUnicode[0].index(hexDiacAsString)]
                    integerDiacAfterORing = shiftedInt | integerDiac
                    listOfEncodedCharacters.pop()
                    listOfEncodedCharacters.append(bin(integerDiacAfterORing)[2:].zfill(16))

                    listOfEncodedCharactersInHexFormat.pop()
                    listOfEncodedCharactersInHexFormat.append(hex(integerDiacAfterORing))

                elif prevCharWasDiac and c != u'ٔ' and c != u'ٕ':  # second diacritization

                    letterFoundFlag = False
                    prevCharWasDiac = False

                    hexSecDiacAsString = hex(ord(c))[2:].zfill(4)

                    integerSecDiac = listOfArabicDiacriticsUnicode[1][
                        listOfArabicDiacriticsUnicode[0].index(hexSecDiacAsString)]
                    integerSecDiacAfterORing = integerDiacAfterORing | integerSecDiac
                    listOfEncodedCharacters.pop()
                    listOfEncodedCharacters.append(bin(integerSecDiacAfterORing)[2:].zfill(16))
                    listOfEncodedCharactersInHexFormat.pop()
                    listOfEncodedCharactersInHexFormat.append(hex(integerSecDiacAfterORing))

    return listOfEncodedCharacters, listOfEncodedCharactersInHexFormat


def extract_each_character_from_word_with_its_diacritization(list_of_extracted_words_and_corresponding_sentence_number, un_diacritized_words):

    DbList = []
    letterFoundFlag = False
    prevCharWasDiac = False
    loopCount = 0
    overall = ""
    diacritics_only_overall = ""

    for eachObject, un_diacritized_word in zip(list_of_extracted_words_and_corresponding_sentence_number, un_diacritized_words):
        diacritizedWord = eachObject[0]
        sentenceNumber = eachObject[1]

        loopCount += 1
        spaChar = unicodedata.normalize('NFC', diacritizedWord)

        for c in spaChar:

            if not unicodedata.combining(c):
                letterFoundFlag = True
                overall = c
                comp = unicodedata.normalize('NFC', c)
                newObject = DbObject()

                newObject.diacritizedCharacter = comp
                newObject.diacritizedWord = diacritizedWord

                newObject.undiacritizedCharacter = c
                newObject.undiacritizedWord = un_diacritized_word

                newObject.diacritics = ""
                newObject.sentenceNumber = sentenceNumber

                DbList.append(newObject)

            elif letterFoundFlag and c != u'ٔ' and c != u'ٕ':

                prevCharWasDiac = True
                letterFoundFlag = False
                overall += c
                diacritics_only_overall = c

                newObject.diacritizedCharacter = unicodedata.normalize('NFC', overall)
                newObject.diacritics = unicodedata.normalize('NFC', diacritics_only_overall)
                newObject.sentenceNumber = sentenceNumber

                DbList.pop()
                DbList.append(newObject)

            elif prevCharWasDiac and c != u'ٔ' and c != u'ٕ':  # second diacritization

                letterFoundFlag = False
                prevCharWasDiac = False
                overall += c
                diacritics_only_overall += c

                newObject.diacritizedCharacter = unicodedata.normalize('NFC', overall)
                newObject.diacritics = unicodedata.normalize('NFC', diacritics_only_overall)
                newObject.sentenceNumber = sentenceNumber

                DbList.pop()
                DbList.append(newObject)

    return DbList


def connect_to_db():

    global db
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                         user="root",  # your username
                         passwd="Islammega88",  # your password
                         db="MSTDB",  # name of the data base
                         use_unicode=True,
                         charset="utf8",
                         init_command='SET NAMES UTF8')

    global cur
    cur = db.cursor()


def push_data_into_db(db_list_of_object, encoded_input, encoded_input_in_hex_format, encoded_target, encoded_target_in_hex_format, list_of_words_in_this_doc_and_corresponding_sentence_number):

    for x in range(0, len(db_list_of_object)):

        cur.execute(
            "INSERT INTO EncodedWords("
            "InputSequenceEncodedWords,"
            "TargetSequenceEncodedWords,"
            "diacritizedCharacter,"
            "undiacritizedCharacter,"
            "InputSequenceEncodedWordsInHexFormat,"
            "TargetSequenceEncodedWordsInHexFormat, "
            "Diacritics) "
            "VALUES ( "
            "%s,%s,%s,%s,%s,%s,%s)",
            (encoded_input[x],
             encoded_target[x],
             db_list_of_object[x].diacritizedCharacter,
             db_list_of_object[x].undiacritizedCharacter,
             encoded_input_in_hex_format[x],
             encoded_target_in_hex_format[x],
             db_list_of_object[x].diacritics))

        cur.execute(
            "INSERT INTO ParsedDocument("
            "DocName, "
            "UnDiacritizedCharacter,"
            "DiacritizedCharacter,"
            "LetterType,"
            "SentenceNumber, "
            "Word, "
            "InputSequenceEncodedWords,"
            "TargetSequenceEncodedWords, "
            "InputSequenceEncodedWordsInHexFormat,"
            "TargetSequenceEncodedWordsInHexFormat, "
            "Diacritics, "
            "UnDiacritizedWord) VALUES (%s,%s,%s,%s,%s,%s,%s,""%s,%s,%s,%s,%s)",
            (docName,
             db_list_of_object[x].undiacritizedCharacter,
             db_list_of_object[x].diacritizedCharacter,
             'testing',
             db_list_of_object[x].sentenceNumber,
             db_list_of_object[x].diacritizedWord,
             encoded_input[x],
             encoded_target[x],
             encoded_input_in_hex_format[x],
             encoded_target_in_hex_format[x],
             db_list_of_object[x].diacritics,
             db_list_of_object[x].undiacritizedWord))

    for x in range(0, len(list_of_words_in_this_doc_and_corresponding_sentence_number)):
        cur.execute(
            "INSERT INTO ListOfWordsAndSentencesInEachDoc(word,SentenceNumber,DocName) VALUES (%s,%s,%s)",
            (list_of_words_in_this_doc_and_corresponding_sentence_number[x][0],
             list_of_words_in_this_doc_and_corresponding_sentence_number[x][1],
             docName))

    db.commit()
    db.close()


if __name__ == "__main__":

    for each_file in os.listdir(pathOfDataFiles):
        pathOfSelectedFile = ""
        docName = each_file

        if each_file.endswith(".txt"):
            pathOfSelectedFile = (os.path.join("D:\MasterRepo\MSTRepo\PaperCorpus\Doc", each_file))
            print(os.path.join("D:\MasterRepo\MSTRepo\PaperCorpus\Doc", each_file))

        dataInThisDoc = read_selected_doc(pathOfSelectedFile)

        listOfWordsInThisDocAndCorrespondingSentenceNumber = bind_words_with_sentence_number_in_this_doc(dataInThisDoc)

        listOfExtractedWordsFromDoc = extract_and_clean_words_from_strange_character_from_doc_and_return_list_of_purified_words(dataInThisDoc)

        listOfUndiacritizedWords = get_list_of_undiacritized_word_from_diacritized_word(listOfExtractedWordsFromDoc)

        encodedInput, encodedInputInHexFormat = character_encoder(listOfUndiacritizedWords)

        encodedTarget, encodedTargetInHexFormat = character_encoder(listOfExtractedWordsFromDoc)

        dbList = extract_each_character_from_word_with_its_diacritization(listOfWordsInThisDocAndCorrespondingSentenceNumber, listOfUndiacritizedWords)

        connect_to_db()

        push_data_into_db(dbList, encodedInput, encodedInputInHexFormat, encodedTarget, encodedTargetInHexFormat, listOfWordsInThisDocAndCorrespondingSentenceNumber)

