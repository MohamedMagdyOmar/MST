# -*- coding: utf-8 -*-
import unicodedata
import re

f = open("/home/mohamed/Desktop/test.txt", 'r')
read_data = f.readlines()
f.close()

listOfWords = []

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

f = open("/home/mohamed/Desktop/UpdatedSa7e7Moslem2.txt", 'w')

for word in listOfWords:
    f.write(word)
    f.write(' ')

f.close()