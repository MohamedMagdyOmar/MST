# -*- coding: utf-8 -*-
import re
import unicodedata
import MySQLdb
import math
import os
import random

# 1
diacritizedCharacter = []
DiacriticsOnly = []
unDiacritizedCharacter = []
listOfDBWords = []
listOfDbSentenceNumber = []
randomized_Sentence = []
listOfPunctuationBySymbol = [u' .', u'.', u' :', u'«', u'»', u'،', u'؛', u'؟', u'.(', u').', u':(', u'):', u'» .', u'».']
final_ListOfUndiacritized_Word = []
listOfArabicDiacriticsUnicode = [["064b", "064c", "064d", "064e", "064f", "0650", "0651", "0652", "0670"],
                                 [1, 2, 3, 4, 5, 6, 8, 7, 9]]


def declareGlobalVariables():
    global wordCount
    wordCount = 0
    global sentenceCount
    sentenceCount = 1

    global list_of_all_sentence
    list_of_all_sentence = []


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
    docName = list_of_docs[each_doc]
    data = f.readlines()
    f.close()

    return doc_name, data


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
            if not (word in listOfPunctuationBySymbol):
                if word.find(u'.') != -1:
                    wordCount += 1
                    word = re.sub(u'[.]', '', word)
                    if word != u'':
                        list_of_words_in_doc_and_corresponding_sentence_number.append([word, sentenceCount])
                    sentenceCount += 1
                else:
                    wordCount += 1
                    list_of_words_in_doc_and_corresponding_sentence_number.append([word, sentenceCount])
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


def encodingDiacritizedCharacter():
    global listOfTargetSequenceEncodedWords
    global listOfInputSequenceEncodedWordsInHexFormat
    global listOfTargetSequenceEncodedWordsInHexFormat
    global listOfInputSequenceEncodedWords
    global listOfUnDiacritizedWord
    listOfInputSequenceEncodedWords = []
    listOfUnDiacritizedWord = []
    listOfTargetSequenceEncodedWords = []
    listOfInputSequenceEncodedWordsInHexFormat = []
    listOfTargetSequenceEncodedWordsInHexFormat = []

    for word in listOfWords:
        if not word in listOfPunctuationBySymbol:
            if word.find(u'.') != -1:
                word = re.sub(u'[.]', '', word)
#            word = word.decode('utf-8', 'ignore') may be need to return itback

            nfkd_form = unicodedata.normalize('NFKD', word)

            unDiacritizedWord = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
            listOfUnDiacritizedWord.append(unDiacritizedWord)

            letterFoundFlag = False
            prevCharWasDiac = False

            for c in word:

                if not unicodedata.combining(c):  # letter
                    letterFoundFlag = True

                    hexAsString = hex(ord(c))[2:].zfill(4)

                    binaryAsString = bin(int(hexAsString, 16))[2:].zfill(16)
                    integer = int(hexAsString, 16)
                    maskedInt = integer & 255
                    maskedBinaryAsString = bin(integer & 255)[2:].zfill(16)
                    shiftedInt = maskedInt << 4
                    shiftedIntInBin = bin(shiftedInt)

                    listOfTargetSequenceEncodedWordsInHexFormat.append(hex(shiftedInt))
                    listOfTargetSequenceEncodedWords.append(bin(shiftedInt)[2:].zfill(16))
                    listOfInputSequenceEncodedWordsInHexFormat.append(hex(shiftedInt))
                    listOfInputSequenceEncodedWords.append(str(bin(shiftedInt)[2:].zfill(16)))

                elif letterFoundFlag and c != u'ٔ' and c != u'ٕ':  # first diacritization
                    prevCharWasDiac = True
                    letterFoundFlag = False

                    hexDiacAsString = hex(ord(c))[2:].zfill(4)
                    if hexDiacAsString == '0670' :
                        x = 1
                    binaryAsString = bin(int(hexDiacAsString, 16))[2:].zfill(16)
                    integerDiac = listOfArabicDiacriticsUnicode[1][
                        listOfArabicDiacriticsUnicode[0].index(hexDiacAsString)]
                    integerDiacAfterORing = shiftedInt | integerDiac
                    listOfTargetSequenceEncodedWords.pop()
                    listOfTargetSequenceEncodedWords.append(bin(integerDiacAfterORing)[2:].zfill(16))

                    listOfTargetSequenceEncodedWordsInHexFormat.pop()
                    listOfTargetSequenceEncodedWordsInHexFormat.append(hex(integerDiacAfterORing))
                elif prevCharWasDiac and c != u'ٔ' and c != u'ٕ':  # second diacritization

                    letterFoundFlag = False
                    prevCharWasDiac = False

                    hexSecDiacAsString = hex(ord(c))[2:].zfill(4)

                    integerSecDiac = listOfArabicDiacriticsUnicode[1][
                        listOfArabicDiacriticsUnicode[0].index(hexSecDiacAsString)]
                    integerSecDiacAfterORing = integerDiacAfterORing | integerSecDiac
                    listOfTargetSequenceEncodedWords.pop()
                    listOfTargetSequenceEncodedWords.append(bin(integerSecDiacAfterORing)[2:].zfill(16))
                    listOfTargetSequenceEncodedWordsInHexFormat.pop()
                    listOfTargetSequenceEncodedWordsInHexFormat.append(hex(integerSecDiacAfterORing))


def encodingunDiacritizedCharacter():
    global listOfUnDiacritizedWord
    global listOfInputSequenceEncodedWords
    listOfUnDiacritizedWord = []
    listOfInputSequenceEncodedWords = []

    for word in listOfWords:
        if not word in listOfPunctuationBySymbol:

            if word.find('.') != -1:
                word = re.sub('[.]', '', word)

            word = word.decode('utf-8', 'ignore')
            nfkd_form = unicodedata.normalize('NFKD', word)

            unDiacritizedWord = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
            listOfUnDiacritizedWord.append(unDiacritizedWord)

            for c in word:

                if not unicodedata.combining(c):  # letter
                    letterFoundFlag = True

                    hexAsString = hex(ord(c))[2:].zfill(4)

                    binaryAsString = bin(int(hexAsString, 16))[2:].zfill(16)
                    integer = int(hexAsString, 16)
                    maskedInt = integer & 255
                    maskedBinaryAsString = bin(integer & 255)[2:].zfill(16)
                    shiftedInt = maskedInt << 4
                    shiftedIntInBin = bin(shiftedInt)
                    listOfInputSequenceEncodedWords.append(bin(shiftedInt)[2:].zfill(16))


def convertToString():
    for item in range(0, len(listOfInputSequenceEncodedWords)):
        listOfInputSequenceEncodedWords[item] = str(listOfInputSequenceEncodedWords[item])


first = ""
second = ""
third = ""
overall = ""
#  = unicodedata.normalize('NFC', word)

def extractEachCharacterFromWordWithItsDiacritization():
    letterFoundFlag = False
    prevCharWasDiac = False
    loopCount = 0
    first = ""
    second = ""
    third = ""
    overall = ""
    diacritics_only_overall = ""

    for word in listOfWords:

        if not word in listOfPunctuationBySymbol:

            if word.find(u'.') != -1:
                word = re.sub(u'[.]', '', word)

#            word = word.decode('utf-8', 'ignore') may be return back

            # removing diacritization from characters
            nfkd_form = unicodedata.normalize('NFKD', word)
            unDiacritizedWord = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
            try:
                sentenceNumber = listOfWordsInSent[loopCount][1]
            except:
                x = 1
            loopCount += 1

            spaChar = unicodedata.normalize('NFC', word)
            for c in spaChar:

                if not unicodedata.combining(c):
                    first = c
                    letterFoundFlag = True
                    overall = c
                    comp = unicodedata.normalize('NFC', c)
                    diacritizedCharacter.append(comp)

                    listOfDbSentenceNumber.append(sentenceNumber)

                    listOfDBWords.append(word)

                    listOfUnDiacritizedWord.append(unDiacritizedWord)
                    unDiacritizedCharacter.append(c)
                    DiacriticsOnly.append("")
                    unDiacritizedWord = u"".join([c for c in nfkd_form if not unicodedata.combining(c) or c == u'ٔ' or c == u'ٕ'])
                    final_ListOfUndiacritized_Word.append(unDiacritizedWord)

                elif letterFoundFlag and c != u'ٔ' and c != u'ٕ':
                    second = c
                    prevCharWasDiac = True
                    letterFoundFlag = False
                    overall += c
                    diacritics_only_overall = c

                    comp = unicodedata.normalize('NFC', overall)
                    comp_diacritics_Only = unicodedata.normalize('NFC', diacritics_only_overall)

                    diacritizedCharacter.pop()
                    diacritizedCharacter.append(comp)

                    DiacriticsOnly.pop()
                    DiacriticsOnly.append(comp_diacritics_Only)
                elif prevCharWasDiac and c != u'ٔ' and c != u'ٕ':  # second diacritization
                    third = c
                    letterFoundFlag = False
                    prevCharWasDiac = False
                    overall += c
                    diacritics_only_overall += c

                    comp = unicodedata.normalize('NFC', overall)
                    comp_diacritics_Only = unicodedata.normalize('NFC', diacritics_only_overall)

                    diacritizedCharacter.pop()
                    diacritizedCharacter.append(comp)

                    DiacriticsOnly.pop()
                    DiacriticsOnly.append(comp_diacritics_Only)
                    # for word in listOfUnDiacritizedWord:
                    # for char in word:
                    #  unDiacritizedCharacter.append(char)


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
    intermediate_list = []
    #list_of_all_sentence = []
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
    declareGlobalVariables()
    for eachDoc in range(0, len(listOfFilesPaths)):
        doc_name = listOfFilesPaths[eachDoc]
        selected_doc, raw_data = read_doc(eachDoc, listOfFilesPaths, ListOfDocs)
        cleaned_data = extract_and_clean_words_from_doc(raw_data)
        bind_words_with_sentence_number_in_this_doc(doc_name, cleaned_data, raw_data)

        encodingDiacritizedCharacter()
        # encodingunDiacritizedCharacter()
        #  convertToString()
        extractEachCharacterFromWordWithItsDiacritization()
        connectToDB()
        prepare_list_for_randomization()
        randomize_Data()
        pushDataIntoDB()
        resetAllLists()

