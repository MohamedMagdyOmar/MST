

def get_diac_version_with_smallest_dist(list_of_objects):

    list_of_actual_words_after_dictionary_correction = []

    for each_object in list_of_objects:

        minimum_error = 100000000
        dictionary_diacritized_words = get_corresponding_diacritized_versions(each_un_diacritized_word)
        if len(dictionary_diacritized_words) == 0:
            dictionary_diacritized_words.append(each_corrected_word)

        dictionary_diacritized_words_after_sukun_correction = sukun_correction_for_dictionary_words(dictionary_diacritized_words)

        if do_we_need_to_search_in_dictionary(dictionary_diacritized_words_after_sukun_correction, each_corrected_word):

            error_count = 0

            for each_word in dictionary_diacritized_words_after_sukun_correction:

                decomposed_dic_word, decomposed_act_word = decompose_word_into_letters(each_word, each_corrected_word)
                norm_dic_word, norm_act_word = normalize_words_under_comparison(decomposed_dic_word, decomposed_act_word)

                for each_diacritized_version_letter, each_current_word_letter in zip(norm_dic_word, norm_act_word):

                    if (len(each_diacritized_version_letter) - len(each_current_word_letter) == 1) or (
                            (len(each_diacritized_version_letter) - len(each_current_word_letter) == -1)):
                        error_count += 1

                    elif (len(each_diacritized_version_letter) - len(each_current_word_letter) == 2) or (
                            (len(each_diacritized_version_letter) - len(each_current_word_letter) == -2)):
                        error_count += 2

                    else:
                        for each_item_in_diacritized_version, each_item_in_current_word in zip(each_diacritized_version_letter, each_current_word_letter):
                            if each_item_in_diacritized_version != each_item_in_current_word:
                                error_count += 1

                if error_count < minimum_error:
                    minimum_error = error_count
                    selected_dictionary_word = each_word

            list_of_actual_words_after_dictionary_correction.append(selected_dictionary_word)
        else:
            list_of_actual_words_after_dictionary_correction.append(each_corrected_word)

    x = convert_list_of_words_to_list_of_chars(list_of_actual_words_after_dictionary_correction)
    return convert_list_of_words_to_list_of_chars(list_of_actual_words_after_dictionary_correction)


def get_corresponding_diacritized_versions(word):
    connect_to_db()

    selected_sentence_query = "select DiacritizedWord from dictionary where  UnDiacritizedWord = " + "'" +word + "'"
    cur.execute(selected_sentence_query)
    corresponding_diacritized_words = cur.fetchall()
    corresponding_diacritized_words = [each_word[0] for each_word in corresponding_diacritized_words]

    return corresponding_diacritized_words


def sukun_correction_for_dictionary_words(dictionary_list):
    dictionary_words_without_sukun = []
    overall = ""
    for each_word in dictionary_list:
        for each_char in each_word:
            spaChar = unicodedata.normalize('NFC', each_char)
            if u'ْ' in spaChar:
                    if not unicodedata.combining(spaChar):
                        overall += spaChar
                        dictionary_words_without_sukun.append(unicodedata.normalize('NFC', overall))
            else:
                overall += spaChar
        dictionary_words_without_sukun.append(unicodedata.normalize('NFC', overall))
        overall = ""
    return dictionary_words_without_sukun


def do_we_need_to_search_in_dictionary(dictionary, word):

    for each_word in dictionary:
        decomposed_dict, decomposed_act = decompose_word_into_letters(each_word, word)
        norm_dict, norm_act = normalize_words_under_comparison(decomposed_dict, decomposed_act)

        if len(norm_dict) != len(norm_act):
            raise ValueError("Bug Found In 'do_we_need_to_search_in_dictionary'")

        if sorted(norm_dict) == sorted(norm_act):
            return False

    for each_word in dictionary:
        decomposed_dict, decomposed_act = decompose_word_into_letters(each_word, word)
        norm_dict, norm_act = normalize_words_under_comparison(decomposed_dict, decomposed_act)
        for x in range(0, len(norm_act)):
            # compare letters before last letter
            if x < (len(norm_act) - 1):
                if norm_dict[x] != norm_act[x]:
                    # so diff is in first or middle letters
                    break
            else:
                # so diff is in last letter so ignore it
                return False

    return True


def decompose_word_into_letters(word_in_dictionary, actual_word):
    decomposed_dictionary_word = []
    decomposed_actual_word = []
    inter_med_list = []
    found_flag = False
    for each_letter in word_in_dictionary:
        if not unicodedata.combining(each_letter):
            if found_flag:
                decomposed_dictionary_word.append(inter_med_list)
            inter_med_list = []
            inter_med_list.append(each_letter)
            found_flag = True

        elif found_flag:
            inter_med_list.append(each_letter)
    # required because last character will not be added above, but here
    decomposed_dictionary_word.append(inter_med_list)

    inter_med_list = []
    found_flag = False
    for each_letter in actual_word:
        if not unicodedata.combining(each_letter):
            if found_flag:
                decomposed_actual_word.append(inter_med_list)
            inter_med_list = []
            inter_med_list.append(each_letter)
            found_flag = True

        elif found_flag:
            inter_med_list.append(each_letter)
            # required because last character will not be added above, but here
    decomposed_actual_word.append(inter_med_list)

    return decomposed_dictionary_word, decomposed_actual_word


def normalize_words_under_comparison(word_in_dictionary, actual_word):

    locale.setlocale(locale.LC_ALL, "")
    for x in range(0, len(word_in_dictionary)):
        word_in_dictionary[x].sort(cmp=locale.strcoll)

    locale.setlocale(locale.LC_ALL, "")
    for x in range(0, len(actual_word)):
        actual_word[x].sort(cmp=locale.strcoll)
    return word_in_dictionary, actual_word