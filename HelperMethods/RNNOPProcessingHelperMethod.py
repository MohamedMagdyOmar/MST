

def get_neurons_numbers_with_highest_output_value(csv_file_op):
    list_of_neurons_indices_with_highest_value = []
    # Take care !!!, that the array is zero index
    for row in csv_file_op:
        list_of_neurons_indices_with_highest_value.append(row.index(max(row)))

    return list_of_neurons_indices_with_highest_value


def deduce_from_rnn_op_predicted_chars(list_of_all_diacritized_letters, neurons_locations_with_highest_output):
    rnn_predicted_chars = []
    for neuron_location in neurons_locations_with_highest_output:
        # Take care, we make +1 because "neurons_locations_with_highest_output" is zero index
        rnn_predicted_chars.append(list_of_all_diacritized_letters[neuron_location - 1])

    return rnn_predicted_chars
