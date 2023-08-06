import csv

def readColumn(file, read_col_number, is_numbers=False, header=False, cols_separated_by=","):

    col_values = []

    with open(file, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=cols_separated_by)

        if header:
            next(csvreader)

        for row in csvreader:

            if is_numbers:
                col_values.append(float(row[read_col_number]))

            else:
                col_values.append(row[read_col_number])

    return col_values

def zipValues_asDict(*values, keys):
    values = list(map(tuple, zip(*values)))

    dictionary = {}

    for i in range(len(keys)):
        dictionary[keys[i]] = values[i]

    return dictionary
    #return dict(zip(keys, zip(*values)))

def zipValues_asList(*values):
    values = list(map(tuple, zip(*values)))

    liste = []

    for i in values:
        liste.append(list(i))

    return liste

def zipValues_asTuple(*values):
    values = list(map(tuple, zip(*values)))

    liste_of_tuples = []

    for i in values:
        liste_of_tuples.append(i)

    return liste_of_tuples