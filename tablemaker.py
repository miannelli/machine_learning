import csv
from os import path


def make_table(file, column_headers, rows):
    """
    A simple csv maker function that writes to tables/<file>
    :param file: file to write to
    :param column_headers: list containing first row of column headers
    :param rows: iterable of lists containing subsequent rows to be written to csv file
    :return: void
    """
    with open(path.realpath('tables/{filename}.csv'.format(filename=file)), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, dialect='excel', delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(column_headers)
        for row in rows:
            writer.writerow(row)