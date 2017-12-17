import DBHelperMethod
import DERCalculationHelperMethod
import DictionaryCorrection
import ExcelHelperMethod
import FathaCorrection
import RNNOPProcessingHelperMethod
import SukunCorrection
import WordLetterProcessingHelperMethod
import os
import glob

extension = 'csv'
path = 'D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample\\'

if __name__ == "__main__":
    type = 'testing'
    list_of_sentence_numbers = DBHelperMethod.get_list_of_sentence_numbers_by(type)
    os.chdir(path)
    result = [i for i in glob.glob('*.{}'.format(extension))]
    current_sentence_counter = 0

    if len(list_of_sentence_numbers) != len(result):
        raise Exception('Mismatch In Number Of Sentences')

    for file_name, sentence_number in zip(result, list_of_sentence_numbers):

        selected_sentence = DBHelperMethod.get_sentence_by(sentence_number)

        rnn_output = ExcelHelperMethod.read_rnn_op_csv_file(path + file_name)
        neurons_locations = RNNOPProcessingHelperMethod.get_neurons_numbers_with_highest_output_value(rnn_output)

        list_of_available_diacritics = DBHelperMethod.get_all_diacritics()
        RNN_Predicted_diacritics = RNNOPProcessingHelperMethod.\
            deduce_from_rnn_op_predicted_chars(list_of_available_diacritics, neurons_locations)

        IP_Undiacritized_Chars = DBHelperMethod.get_un_diacritized_chars_by(sentence_number, type)
        RNN_Predicted_chars = WordLetterProcessingHelperMethod.attach_diacritics_to_chars(IP_Undiacritized_Chars, RNN_Predicted_diacritics)

        RNN_Predicted_Chars_Count = WordLetterProcessingHelperMethod.get_chars_count_for_each_word_in_this(selected_sentence)
        RNN_Predicted_Chars_And_Its_Location = WordLetterProcessingHelperMethod.get_location_of_each_char(RNN_Predicted_chars, RNN_Predicted_Chars_Count)

        RNN_Predicted_Chars_After_Sukun = SukunCorrection.sukun_correction()



        Target_Chars = DBHelperMethod.get_diacritized_chars_by(sentence_number, type)