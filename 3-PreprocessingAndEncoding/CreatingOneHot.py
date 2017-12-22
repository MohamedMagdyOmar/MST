# -*- coding: utf-8 -*-

# 2'

import MySQLdb
import NumpyOneHotEncoding as encoding
import numpy as np

db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                     user="root",  # your username
                     passwd="Islammega88",  # your password
                     db="mstdb",  # name of the data base
                     use_unicode=True,
                     charset="utf8",
                     init_command='SET NAMES UTF8')

cur = db.cursor()

sqlQuery = "select arabic_letter, location from arabic_letters_without_diacritics"
cur.execute(sqlQuery)
listOfUnDiacritizedCharacter = cur.fetchall()
listOfUnDiacritizedCharacterObject = list(listOfUnDiacritizedCharacter)
listOfUnDiacritizedCharacter = [i[0] for i in listOfUnDiacritizedCharacterObject]
listOfUnDiacritizedCharacterLocation = [i[1] for i in listOfUnDiacritizedCharacterObject]

sqlQuery = "select arabic_letter from arabic_letters_with_diacritics"
cur.execute(sqlQuery)
listOfDiacritizedCharacter = cur.fetchall()
listOfDiacritizedCharacter = list(listOfDiacritizedCharacter)
listOfDiacritizedCharacter = [i[0] for i in listOfDiacritizedCharacter]

sqlQuery = "select diacritics from arabic_diacritics"
cur.execute(sqlQuery)
listOfDiacritics = cur.fetchall()
listOfDiacritics = list(listOfDiacritics)
listOfDiacritics = [i[0] for i in listOfDiacritics]


for x in range(0, len(listOfUnDiacritizedCharacter)):
    listOfUnDiacritizedCharacter[x] = (listOfUnDiacritizedCharacter[x]).encode('utf-8')

for x in range(0, len(listOfDiacritizedCharacter)):
    listOfDiacritizedCharacter[x] = (listOfDiacritizedCharacter[x]).encode('utf-8')

for x in range(0, len(listOfDiacritics)):
    listOfDiacritics[x] = (listOfDiacritics[x]).encode('utf-8')

one_hot_list__for_un_diacritized_characters, one_hot_list__for_diacritized_characters = \
    encoding.encodeMyCharacterWith2Parameters(listOfUnDiacritizedCharacter, listOfDiacritizedCharacter)

one_hot_list_for_diacritized = encoding.encodeMyCharacterWith1Parameter(listOfDiacritics)


UnDiacritizedOneHotInNDimArrayForm = np.array(one_hot_list__for_un_diacritized_characters)
UnDiacritizedOneHotInNDimArrayForm = UnDiacritizedOneHotInNDimArrayForm.astype(np.int8)

diacritizedOneHotInNDimArrayForm = np.array(one_hot_list__for_diacritized_characters)
diacritizedOneHotInNDimArrayForm = diacritizedOneHotInNDimArrayForm.astype(np.int8)

DiacriticsOneHotInNDimArrayForm = np.array(one_hot_list_for_diacritized)
DiacriticsOneHotInNDimArrayForm = DiacriticsOneHotInNDimArrayForm.astype(np.int8)

# filling "UnDiacOneHotEncoding and DiacOneHotEncoding" Tables
print len(one_hot_list__for_un_diacritized_characters)
print len(one_hot_list__for_diacritized_characters)
print len(one_hot_list_for_diacritized)

for x in range(0, len(one_hot_list__for_un_diacritized_characters)):
    cur.execute("insert into UnDiacOneHotEncoding (UnDiacritizedCharacter,UnDiacritizedCharacterOneHotEncoding, location)"
                " VALUES (%s,%s,%s)",
                (listOfUnDiacritizedCharacter[x], UnDiacritizedOneHotInNDimArrayForm[x], listOfUnDiacritizedCharacterLocation[x]))

for x in range(0, len(one_hot_list__for_diacritized_characters)):
    cur.execute("insert into DiacOneHotEncoding (DiacritizedCharacter,DiacritizedCharacterOneHotEncoding)"
                " VALUES (%s,%s)",
                (listOfDiacritizedCharacter[x], diacritizedOneHotInNDimArrayForm[x]))

for x in range(0, len(one_hot_list_for_diacritized)):
    cur.execute("insert into distinctdiacritics (diacritics,encoding)"
                " VALUES (%s,%s)",
                (listOfDiacritics[x], DiacriticsOneHotInNDimArrayForm[x]))

db.commit()

db.close()
