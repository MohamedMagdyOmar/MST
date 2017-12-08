# -*- coding: utf-8 -*-
import re
import unicodedata
import MySQLdb
import math
import os
import random

# 1

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


def get_all_files():
    list_of_files_paths = []
    list_of_doc_name = []
    for file_name in os.listdir("D:\MasterRepo\MSTRepo\PaperCorpus\Doc"):
        if file_name.endswith(".txt"):
            list_of_files_paths.append(os.path.join("D:\MasterRepo\MSTRepo\PaperCorpus\Doc", file_name))
            list_of_doc_name.append(file_name)
            print(os.path.join("D:\MasterRepo\MSTRepo\PaperCorpus\Doc", file_name))

    return list_of_files_paths, list_of_doc_name


def read_doc(each_doc, list_of_paths, list_of_docs):

    f = open(list_of_paths[each_doc], 'r')
    document_name = list_of_docs[each_doc]
    data = f.readlines()
    f.close()

    return document_name, data


def extract_and_clean_words_from_doc(data):
    list_of_words = []
    for eachSentence in data:
        words_in_sentence = eachSentence.split()
        for word in words_in_sentence:
            word = word.decode('utf-8', 'ignore') # variable line
            word = re.sub(u'[-;}()/]', '', word)
            word = re.sub(u'[-;}()0123456789/]', '', word)
            word = re.sub(u'["{"]', '', word)
            word = re.sub(u'[:]', ' :', word)

            word = re.sub(u'[ـ]', '', word)
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
            if not (word == u''):
                list_of_words.append(word)

    return list_of_words


def bind_words_with_sentence_number_in_this_doc(doc_name, list_of_words, raw_data):
    global wordCount
    global sentenceCount
    list_of_words_in_doc_and_corresponding_sentence_number = []

    if doc_name != 'quran-simple.txt' and not (doc_name.startswith('ANN2002')):
        for word in list_of_words:
            if not (word in listOfPunctuationSymbols):
                if word.find(u'.') != -1:
                    wordCount += 1
                    word = re.sub(u'[.]', '', word)
                    if word != u'':
                        list_of_words_in_doc_and_corresponding_sentence_number.append([word, sentenceCount])

                    list_of_words_in_doc_and_corresponding_sentence_number.append(["eos", sentenceCount])
                    sentenceCount += 1
                else:
                    wordCount += 1
                    list_of_words_in_doc_and_corresponding_sentence_number.append([word, sentenceCount])
                    list_of_words_in_doc_and_corresponding_sentence_number.append(["space", sentenceCount])
            else:
                sentenceCount += 1
                list_of_words_in_doc_and_corresponding_sentence_number.append(["bos", sentenceCount])

    else:
        sentenceCount = 0
        wordCount = 0
        for eachVersus in raw_data:
            sentenceCount += 1
            each_word_in_versus = eachVersus.split()
            list_of_words_in_doc_and_corresponding_sentence_number.append(["bos", sentenceCount])
            for eachWord in each_word_in_versus:
                wordCount += 1
                list_of_words_in_doc_and_corresponding_sentence_number.append([eachWord, sentenceCount])
                list_of_words_in_doc_and_corresponding_sentence_number.append(["space", sentenceCount])

            list_of_words_in_doc_and_corresponding_sentence_number.pop()
            list_of_words_in_doc_and_corresponding_sentence_number.append(["eos", sentenceCount])

    return list_of_words_in_doc_and_corresponding_sentence_number


def get_list_of_undiacritized_word_from_diacritized_word(list_of_extracted_words_without_numbers):

    listOfUnDiacritizedWord = []
    for word in list_of_extracted_words_without_numbers:
        word[0] = word[0].decode('utf-8', 'ignore')
        if word[0] != "space" and word[0] != "bos" and word[0] != "eos":
            if not word[0] in listOfPunctuationSymbols:

                if word[0].find('.') != -1:
                    word[0] = re.sub('[.]', '', word[0])

                #word[0] = word[0].decode('utf-8', 'ignore')
                nfkd_form = unicodedata.normalize('NFKD', word[0])

                word[0] = u"".join([c for c in nfkd_form if not unicodedata.combining(c) or c == u'ٔ' or c == u'ٕ'])
                listOfUnDiacritizedWord.append(word)
        else:
            listOfUnDiacritizedWord.append(word)

    return listOfUnDiacritizedWord


def character_encoder(list_of_extracted_words_without_numbers):
    listOfEncodedCharacters = []
    listOfEncodedCharactersInHexFormat = []

    for word[0] in list_of_extracted_words_without_numbers:
        if word != "space" and word != "eos" and word != "bos":
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
        else:
            listOfEncodedCharacters.append(word)
            listOfEncodedCharactersInHexFormat.append(word)

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
        if eachObject[0] != 'space' and eachObject[0] != 'bos' and eachObject[0] != 'eos':

            spaChar = unicodedata.normalize('NFC', eachObject[0])

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
        else:
            newObject = DbObject()

            newObject.diacritizedCharacter = eachObject[0]
            newObject.diacritizedWord = eachObject[0]

            newObject.undiacritizedCharacter = eachObject[0]
            newObject.undiacritizedWord = eachObject[0]

            newObject.diacritics = ""
            newObject.sentenceNumber = eachObject[1]
            DbList.append(newObject)


    return DbList


def connectToDB():
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


def prepare_list_for_randomization():
    list_of_sentence_content = []

    sentence_number = listOfDbSentenceNumber[0]
    counter = 0

    for current_sentence_number in listOfDbSentenceNumber:
        if current_sentence_number == 6235:
            x = 1
        if current_sentence_number == sentence_number:
            intermediate_list = []
            intermediate_list.append(docName)
            intermediate_list.append(unDiacritizedCharacter[counter])
            intermediate_list.append(diacritizedCharacter[counter])
            intermediate_list.append(listOfDbSentenceNumber[counter])
            intermediate_list.append(listOfDBWords[counter])
            intermediate_list.append(listOfInputSequenceEncodedWords[counter])
            intermediate_list.append(listOfTargetSequenceEncodedWords[counter])
            intermediate_list.append(listOfInputSequenceEncodedWordsInHexFormat[counter])
            intermediate_list.append(listOfTargetSequenceEncodedWordsInHexFormat[counter])
            intermediate_list.append(DiacriticsOnly[counter])
            intermediate_list.append(final_ListOfUndiacritized_Word[counter])

            list_of_sentence_content.append(intermediate_list)

            counter += 1
        else:
            list_of_all_sentence.append(list_of_sentence_content)

            intermediate_list = []
            list_of_sentence_content = []

            sentence_number += 1

            intermediate_list.append(docName)
            intermediate_list.append(unDiacritizedCharacter[counter])
            intermediate_list.append(diacritizedCharacter[counter])
            intermediate_list.append(listOfDbSentenceNumber[counter])
            intermediate_list.append(listOfDBWords[counter])
            intermediate_list.append(listOfInputSequenceEncodedWords[counter])
            intermediate_list.append(listOfTargetSequenceEncodedWords[counter])
            intermediate_list.append(listOfInputSequenceEncodedWordsInHexFormat[counter])
            intermediate_list.append(listOfTargetSequenceEncodedWordsInHexFormat[counter])
            intermediate_list.append(DiacriticsOnly[counter])
            intermediate_list.append(final_ListOfUndiacritized_Word[counter])

            list_of_sentence_content.append(intermediate_list)

            counter += 1

    list_of_all_sentence.append(list_of_sentence_content)
    x = 1


def randomize_Data():
    global randomized_Sentence
    randomized_Sentence = random.sample(list_of_all_sentence, len(list_of_all_sentence))


def pushDataIntoDB():
    global randomized_Sentence
    requiredPercentageForValidation = math.ceil((len(randomized_Sentence) * 12) / 100)
    trainingCounter = len(randomized_Sentence) - (requiredPercentageForValidation)
    isTrainingDataIsFinished = False
    isValidationDataIsFinished = False
    # Part A : filling "Encoded Words" Table
    for x in range(0, len(listOfInputSequenceEncodedWords)):
        cur.execute(
            "INSERT INTO EncodedWords(InputSequenceEncodedWords,TargetSequenceEncodedWords,diacritizedCharacter,"
            "undiacritizedCharacter,InputSequenceEncodedWordsInHexFormat,TargetSequenceEncodedWordsInHexFormat, "
            "Diacritics) "
            "VALUES ( "
            "%s,%s,%s,%s,%s,%s,%s)",
            (listOfInputSequenceEncodedWords[x], listOfTargetSequenceEncodedWords[x], diacritizedCharacter[x],
             unDiacritizedCharacter[x], listOfInputSequenceEncodedWordsInHexFormat[x],
             listOfTargetSequenceEncodedWordsInHexFormat[x], DiacriticsOnly[x]))
    x = len(randomized_Sentence)
    y = randomized_Sentence[len(randomized_Sentence) - 1]
    for each_sent in randomized_Sentence:
        if trainingCounter >= 0:
            for each_letter in each_sent:
                cur.execute(
                    "INSERT INTO ParsedDocument(DocName, UnDiacritizedCharacter,DiacritizedCharacter,LetterType,"
                    "SentenceNumber, "
                    "Word, "
                    "InputSequenceEncodedWords,TargetSequenceEncodedWords, InputSequenceEncodedWordsInHexFormat,"
                    "TargetSequenceEncodedWordsInHexFormat, Diacritics, UnDiacritizedWord) VALUES (%s,%s,%s,%s,%s,%s,"
                    "%s, "
                    "%s,%s,%s,%s,%s)",
                    (each_letter[0], each_letter[1], each_letter[2], "training", each_letter[3], each_letter[4], each_letter[5], each_letter[6], each_letter[7],
                     each_letter[8], each_letter[9], each_letter[10]))
            trainingCounter -= 1
        else:
            for each_letter in each_sent:
                cur.execute(
                    "INSERT INTO ParsedDocument(DocName, UnDiacritizedCharacter,DiacritizedCharacter,LetterType,"
                    "SentenceNumber, "
                    "Word, "
                    "InputSequenceEncodedWords,TargetSequenceEncodedWords, InputSequenceEncodedWordsInHexFormat,"
                    "TargetSequenceEncodedWordsInHexFormat, Diacritics, UnDiacritizedWord) VALUES (%s,%s,%s,%s,%s,%s,%s,"
                    "%s,%s,%s,%s,%s)",
                    (each_letter[0], each_letter[1], each_letter[2], "testing", each_letter[3], each_letter[4],
                    each_letter[5], each_letter[6], each_letter[7],
                    each_letter[8], each_letter[9], each_letter[10]))

    for x in range(0, len(listOfWordsInSent)):
        cur.execute(
            "INSERT INTO ListOfWordsAndSentencesInEachDoc(word,SentenceNumber,DocName) VALUES (%s,%s,%s)",
            (listOfWordsInSent[x][0], listOfWordsInSent[x][1], docName))

    db.commit()
    db.close()


def resetAllLists():
    del unDiacritizedCharacter[:]
    del diacritizedCharacter[:]
    del listOfDbSentenceNumber[:]
    del listOfDBWords[:]
    del listOfInputSequenceEncodedWords[:]
    del listOfTargetSequenceEncodedWords[:]
    del listOfInputSequenceEncodedWordsInHexFormat[:]
    del listOfTargetSequenceEncodedWordsInHexFormat[:]
    del listOfWordsInSent[:]
    del list_of_all_sentence[:]
    del randomized_Sentence[:]

if __name__ == "__main__":
    listOfFilesPaths, ListOfDocs = get_all_files()

    for eachDoc in range(0, len(listOfFilesPaths)):
        doc_name = listOfFilesPaths[eachDoc]
        selected_doc, raw_data = read_doc(eachDoc, listOfFilesPaths, ListOfDocs)
        cleaned_data = extract_and_clean_words_from_doc(raw_data)
        listOfWordsAndCorrespondingSentenceNumber = bind_words_with_sentence_number_in_this_doc(selected_doc, cleaned_data, raw_data)
        listOfUndiacritizedWords = get_list_of_undiacritized_word_from_diacritized_word(listOfWordsAndCorrespondingSentenceNumber)

        encodedInput, encodedInputInHexFormat = character_encoder(listOfUndiacritizedWords)
        encodedTarget, encodedTargetInHexFormat = character_encoder(cleaned_data)
        dbList = extract_each_character_from_word_with_its_diacritization(
            listOfWordsAndCorrespondingSentenceNumber, listOfUndiacritizedWords)
        connectToDB()
        prepare_list_for_randomization()
        randomize_Data()
        pushDataIntoDB()
        resetAllLists()

