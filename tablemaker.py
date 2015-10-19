import csv
from os import path



def make_table(file, column_headers, rows):
    with open(path.realpath('tables/{filename}.csv'.format(filename=file)), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, dialect='excel', delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(column_headers)
        for row in rows:
            writer.writerow(row)