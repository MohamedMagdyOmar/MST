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


delete from parseddocument where UnDiacritizedCharacter = 'bos' or UnDiacritizedCharacter = 'space' or UnDiacritizedCharacter = 'eos';
delete from encodedwords where UnDiacritizedCharacter = 'bos' or UnDiacritizedCharacter = 'space' or UnDiacritizedCharacter = 'eos';
delete from ListOfWordsAndSentencesInEachDoc where word = 'bos' or word = 'space' or word = 'eos';
delete from arabic_letters_without_diacritics where arabic_letter = 'bos' or arabic_letter = 'space' or arabic_letter = 'eos';
delete from distinctdiacritics where id > 14;
delete from diaconehotencoding where idDiacritizedCharacter > 479;
-- reset auto increment column
SET SQL_SAFE_UPDATES = 0;
SET  @num := 0;
UPDATE distinctdiacritics SET id= @num := (@num+1);
ALTER TABLE distinctdiacritics AUTO_INCREMENT =1;


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
SET  @num := 0;
UPDATE undiaconehotencoding SET idUnDiacritizedCharacter= @num := (@num+1);
ALTER TABLE undiaconehotencoding AUTO_INCREMENT =1;

SET SQL_SAFE_UPDATES = 0;
SET  @num := 0;
UPDATE diaconehotencoding SET idDiacritizedCharacter= @num := (@num+1);
ALTER TABLE diaconehotencoding AUTO_INCREMENT =1;

SET SQL_SAFE_UPDATES = 0;
SET  @num := 0;
UPDATE distinctdiacritics SET id= @num := (@num+1);
ALTER TABLE distinctdiacritics AUTO_INCREMENT =1;

SET SQL_SAFE_UPDATES = 0;
SET  @num := 0;
UPDATE dictionary SET idDictionary= @num := (@num+1);
ALTER TABLE dictionary AUTO_INCREMENT =1;

SET SQL_SAFE_UPDATES = 0;
SET  @num := 0;
UPDATE arabic_letters_with_diacritics SET id= @num := (@num+1);
ALTER TABLE arabic_letters_with_diacritics AUTO_INCREMENT =1;

SET SQL_SAFE_UPDATES = 0;
SET  @num := 0;
UPDATE arabic_letters_without_diacritics SET id= @num := (@num+1);
ALTER TABLE arabic_letters_without_diacritics AUTO_INCREMENT =1;

-- the following "update" commands is for "atb3"
-- update parseddocument set Diacritics='ٰ';file:/D:/Repos/MST/MST/Encoding/CreatingOneHotNew.py
UPDATE parseddocument SET Diacritics = REPLACE(Diacritics,'ٰ','');
UPDATE parseddocument SET Diacritics = REPLACE(Diacritics,'ًً','ً');
UPDATE parseddocument SET DiacritizedCharacter = REPLACE(DiacritizedCharacter,'اًً','اً');

-- Dictionary Table Creation
insert into dictionary (DiacritizedWord,UnDiacritizedWord)
(select word, UnDiacritizedWord from parseddocument where   LetterType='training' group by word order by UnDiacritizedWord asc);

-- presence of shadda only mistake
select  distinct idCharacterNumber, Diacritics from parseddocument where lettertype='testing' and diacritics = 'ّ'