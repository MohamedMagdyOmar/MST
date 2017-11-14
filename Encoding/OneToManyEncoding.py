# -*- coding: utf-8 -*-
import re
import unicodedata
# s = "ثُمَّ"
f = open("/home/mohamed/Desktop/Game3Sa7e7.txt", 'r')
read_data = f.readlines()
f.close()

listOfPunctuationBySymbol = [' .', ' :', '«', '»', '،', '؛', '؟', '.(', ').', ':(', '):', '» .']
listOfWords = []
listOfWordsInSent = []
ListOfWordsWithPunctuation = []
wordCount = 0

for eachSentence in read_data:
    wordsInSentence = eachSentence.split()
    for word in wordsInSentence:
        word = re.sub('[-;}()0123456789/]', '', word)
        word = re.sub('[.]', ' .', word)
        word = re.sub('["{"]', '', word)
        word = re.sub('[:]', ' :', word)

        if not (word == ''):
            listOfWords.append(word)

sentenceCount = 1

for word in listOfWords:

    if not (word in listOfPunctuationBySymbol):
        wordCount += 1
        listOfWordsInSent.append([word, sentenceCount])
        ListOfWordsWithPunctuation.append([word, sentenceCount])
    else:
        ListOfWordsWithPunctuation.append([word, sentenceCount])
        sentenceCount += 1

listOfUnDiacritizedWord = []
letterCount = 0
prevCharWasDiac = False
letterFoundFlag = False
lettersWithNoDiac = 0
lettersWithOneDiac = 0
lettersWithTwoDiac = 0

listOfLettersWith2Diac = []

for word in listOfWords:
    if not word in listOfPunctuationBySymbol:
        word = word.decode('utf-8', 'ignore')
        nfkd_form = unicodedata.normalize('NFKD', word)
        for c in word:
            print hex(ord(u"".join(c)))






