import csv


def read_rnn_op_csv_file(csv_complete_path):

    rnn_op = []

    with open(csv_complete_path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')

        for row in reader:
            rnn_op.append(map(float, row))

        return rnn_op
