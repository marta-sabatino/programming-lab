import csv

class CSVFile:
    def __init__(self, name):
        self.name = name
        if not isinstance(self.name, str):
            raise Exception('Errore! il nome non è una stringa')
        self.can_read = True

        try:
            file = open(self.name, 'r')
            file.readline()

        except Exception as e:
            self.can_read = False
            print('Errore in apertura del file: ', e)

    def get_data(self, start=None, end=None):
        if not self.can_read:
            print('Errore in apertura del file')
            return None

        else:
            data = []

            file = open(self.name)
            reader = csv.reader(file)

            # counter = 0

            for i in range(start):
                next(reader)

            for line in file:
                elements = line.split(',')
                elements[-1] = elements[-1].strip()

                # while counter < start:
                #     counter += 1
                #     continue

                if elements[0] != 'Date':
                    # counter += 1
                    data.append(elements)

                if reader.line_num == end: 
                    break

        file.close()

        return data

class NumericalCSVFile(CSVFile):

    def get_data(self):
        string_data = super().get_data()
        numerical_data = []

        for string_row in string_data:
            numerical_row = []

            for i, element in enumerate(string_row):

                if i==0:
                    numerical_row.append(element)

                else:                
                    try:
                        numerical_row.append(float(element))
                    except Exception as e:
                        print('Errore di conversione: ', e)
                        break

            if len(numerical_row) == len(string_row):
                numerical_data.append(numerical_row)

        return numerical_data


myfile = CSVFile('shampoo_sales.csv')
print(myfile.get_data(10,15))