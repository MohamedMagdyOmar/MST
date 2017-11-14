# -*- coding: utf-8 -*-

import MySQLdb
import NumpyOneHotEncoding as encoding
import numpy as np

# 4

db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                     user="root",  # your username
                     passwd="Islammega88",  # your password
                     db="mstdb",  # name of the data base
                     use_unicode=True,
                     charset="utf8",
                     init_command='SET NAMES UTF8')

cur = db.cursor()

SQLQuery = "select distinct Diacritics from alldiacriticsinalldocuments"
cur.execute(SQLQuery)


rowsOfDiacriticsInDB = cur.fetchall()
rowsOfDiacriticsInDB = list(set(list(rowsOfDiacriticsInDB)))

for x in range(0, len(rowsOfDiacriticsInDB)):
    rowsOfDiacriticsInDB[x] = (rowsOfDiacriticsInDB[x][0]).encode('utf-8')

rowsOfDiacriticsInDB = np.array(rowsOfDiacriticsInDB)
one_hot_list_for_diacritized = encoding.encodeMyCharacterWith1Parameter(rowsOfDiacriticsInDB)

DiacritizedOneHotInNDimArrayForm = np.array(one_hot_list_for_diacritized)
DiacritizedOneHotInNDimArrayForm = DiacritizedOneHotInNDimArrayForm.astype(np.int8)


for x in range(0, len(one_hot_list_for_diacritized)):
    cur.execute("insert into distinctdiacritics (diacritics,encoding)"
                " VALUES (%s,%s)",
                (rowsOfDiacriticsInDB[x], DiacritizedOneHotInNDimArrayForm[x]))

db.commit()

db.close()
