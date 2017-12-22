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
delete from distinctdiacritics;
SET SQL_SAFE_UPDATES = 0;
delete from alldiacriticsinalldocuments;
SET SQL_SAFE_UPDATES = 0;
delete from dictionary;
SET SQL_SAFE_UPDATES = 0;
delete from arabic_letters_without_diacritics;
SET SQL_SAFE_UPDATES = 0;
delete from arabic_letters_with_diacritics;
SET SQL_SAFE_UPDATES = 0;
delete from arabic_diacritics;
SET SQL_SAFE_UPDATES = 0;
delete from labels;

SET SQL_SAFE_UPDATES = 0;
delete from parseddocument where LetterType='training'