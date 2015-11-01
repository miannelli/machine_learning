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
        types = []
        for r in rows[0]:
        	if isinstance(r,int):
        		types.append('int')
        	elif isinstance(r,float):
        		types.append('float')
        	else:
        		types.append('str')
        writer.writerow(types)
        for row in rows:
            writer.writerow(row)

def read_table(file):
    with open(path.realpath('tables/{filename}.csv'.format(filename=file)), 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, dialect='excel', delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        rows=[]
        column_headers = next(reader)
        types = next(reader)
        for row in reader:
        	converted_row = [eval(types[i])(row[i]) for i in range(len(row))]
        	rows.append(converted_row)
        return (column_headers, rows)
