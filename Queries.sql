select * from parseddocument where   LetterType='training' ;
select * from parseddocument where   LetterType='validation';
select  * from parseddocument where LetterType='testing';
SELECT SentenceNumber, COUNT(idCharacterNumber) FROM parseddocument GROUP BY SentenceNumber ORDER BY SentenceNumber ASC;
SELECT SentenceNumber, COUNT(*)
FROM parseddocument
GROUP BY SentenceNumber;

select distinct SentenceNumber, Word from parseddocument;
select * from parseddocument where SentenceNumber >29 and SentenceNumber < 35;
select Word from parseddocument where DocName = 'ANN20021015.0101.txt' order by idCharacterNumber;

-- this represent alef when it is found above character, this is found only in atb3
select  * from parseddocument where Diacritics= 'ٰ';
select  * from parseddocument where UnDiacritizedCharacter= 'ـ';
select  * from parseddocument where Diacritics= 'ًً';

-- the following "update" commands is for "atb3"
-- update parseddocument set Diacritics='ٰ';
UPDATE parseddocument SET Diacritics = REPLACE(Diacritics,'ٰ','');

UPDATE parseddocument SET Diacritics = REPLACE(Diacritics,'ًً','ً');
UPDATE parseddocument SET DiacritizedCharacter = REPLACE(DiacritizedCharacter,'اًً','اً');

select * from encodedwords;

select * from undiaconehotencoding;
select * from UnDiacOneHotEncoding where UnDiacritizedCharacter='' or UnDiacritizedCharacter='.';
select * from diaconehotencoding order by DiacritizedCharacter asc;

select * from dictionary;

select * from ListOfWordsAndSentencesInEachDoc where word = '' ;
select * from ListOfWordsAndSentencesInEachDoc;
select distinct SentenceNumber, DocName from listofwordsandsentencesineachdoc;

select * from distinctdiacritics;

select * from alldiacriticsinalldocuments;


select * from arabic_letters_without_diacritics;
select * from arabic_letters_with_diacritics;
select * from arabic_diacritics;
select * from labels;


SET NAMES 'utf8' COLLATE 'utf8_general_ci';
ALTER DATABASE mstdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


-- reset auto increment column
SET SQL_SAFE_UPDATES = 0;
SET  @num := 0;
UPDATE parseddocument SET idCharacterNumber= @num := (@num+1);
ALTER TABLE parseddocument AUTO_INCREMENT =1;

SET SQL_SAFE_UPDATES = 0;
SET  @num := 0;
UPDATE encodedwords SET id= @num := (@num+1);
ALTER TABLE encodedwords AUTO_INCREMENT =1;

SET SQL_SAFE_UPDATES = 0;
SET  @num := 0;
UPDATE ListOfWordsAndSentencesInEachDoc SET idWord= @num := (@num+1);
ALTER TABLE ListOfWordsAndSentencesInEachDoc AUTO_INCREMENT =1;


SET SQL_SAFE_UPDATES = 0;
delete  from parseddocument;
SET SQL_SAFE_UPDATES = 0;
delete  from encodedwords;
SET SQL_SAFE_UPDATES = 0;
delete  from ListOfWordsAndSentencesInEachDoc;
SET SQL_SAFE_UPDATES = 0;
delete  from diaconehotencoding;
SET SQL_SAFE_UPDATES = 0;
delete  from undiaconehotencoding;
SET SQL_SAFE_UPDATES = 0;
delete from alldiacriticsinalldocuments;
SET SQL_SAFE_UPDATES = 0;
delete from distinctdiacritics;
SET SQL_SAFE_UPDATES = 0;
delete from dictionary;
SET SQL_SAFE_UPDATES = 0;
delete from arabic_letters_with_diacritics;
SET SQL_SAFE_UPDATES = 0;
delete from arabic_diacritics;
SET SQL_SAFE_UPDATES = 0;
delete from labels;



CREATE TABLE new_foo LIKE parseddocument;
RENAME TABLE parseddocument TO old_foo, new_foo TO parseddocument;
DROP TABLE old_foo;

CREATE TABLE new_foo LIKE encodedwords;
RENAME TABLE encodedwords TO old_foo, new_foo TO encodedwords;
DROP TABLE old_foo;

CREATE TABLE new_foo LIKE ListOfWordsAndSentencesInEachDoc;
RENAME TABLE ListOfWordsAndSentencesInEachDoc TO old_foo, new_foo TO ListOfWordsAndSentencesInEachDoc;
DROP TABLE old_foo;

SET SQL_SAFE_UPDATES = 0;
UPDATE diaconehotencoding SET DiacritizedCharacterOneHotEncoding = REPLACE(DiacritizedCharacterOneHotEncoding, ' ', '');
UPDATE diaconehotencoding SET DiacritizedCharacterOneHotEncoding = REPLACE(DiacritizedCharacterOneHotEncoding, '[', '');
UPDATE diaconehotencoding SET DiacritizedCharacterOneHotEncoding = REPLACE(DiacritizedCharacterOneHotEncoding, ']', '');
UPDATE diaconehotencoding SET DiacritizedCharacterOneHotEncoding = REPLACE(DiacritizedCharacterOneHotEncoding, '\n', '');


SET SQL_SAFE_UPDATES = 0;
UPDATE undiaconehotencoding SET UnDiacritizedCharacterOneHotEncoding = REPLACE(UnDiacritizedCharacterOneHotEncoding, ' ', '');
UPDATE undiaconehotencoding SET UnDiacritizedCharacterOneHotEncoding = REPLACE(UnDiacritizedCharacterOneHotEncoding, '[', '');
UPDATE undiaconehotencoding SET UnDiacritizedCharacterOneHotEncoding = REPLACE(UnDiacritizedCharacterOneHotEncoding, ']', '');
UPDATE undiaconehotencoding SET UnDiacritizedCharacterOneHotEncoding = REPLACE(UnDiacritizedCharacterOneHotEncoding, '\n', '');

SET SQL_SAFE_UPDATES = 0;
UPDATE distinctdiacritics SET encoding = REPLACE(encoding, ' ', '');
UPDATE distinctdiacritics SET encoding = REPLACE(encoding, '[', '');
UPDATE distinctdiacritics SET encoding = REPLACE(encoding, ']', '');



ALTER TABLE ListOfWordsAndSentencesInEachDoc CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

insert into diaconehotencoding (idDiacritizedCharacter, DiacritizedCharacter) values (422, 'عًّ');
insert into alldiacriticsinalldocuments (Diacritics) values ('عًّ');
UPDATE alldiacriticsinalldocuments SET Diacritics = SUBSTR(Diacritics, 1);
insert into dictionary (DiacritizedWord,UnDiacritizedWord)(select word, UnDiacritizedWord from parseddocument group by word order by UnDiacritizedWord asc);


select distinct SentenceNumber, DocName from listofwordsandsentencesineachdoc;

update parseddocument Set LetterType = 'training' where idCharacterNumber < 1172931;

update parseddocument Set LetterType = 'testing' where idCharacterNumber >= 1172931;

select distinct DocName, SentenceNumber from parseddocument where LetterType = 'testing' order by  idCharacterNumber asc;

select * from 
listofwordsandsentencesineachdoc where DocName='ANN20021015.0100.txt'



