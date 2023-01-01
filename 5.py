class CSVFile:
    def __init__(self, name):
        self.name = name
        self.can_read = True

        try:
            file = open(self.name, 'r')
            file.readline()

        except Exception as e:
            self.can_read = False
            print('Errore in apertura del file: ', e)

    def get_data(self):
        if not self.can_read:
            print('Errore in apertura del file')
            return None

        else:
            # empty = True
            data = []

            file = open(self.name, 'r')

            for line in file:
                elements = line.split(',')
                elements[-1] = elements[-1].strip()

                if elements[0] != 'Date':
                    data.append(elements)
                    # empty = False

        file.close()

        # if empty == True:
        #     return None
        # else:
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


# mio_file = CSVFile('error_file.csv')
# print('\nNome del file: "{}"'.format(mio_file.name),'\n')
# print('\nDati contenuti nel file: "{}"'.format(mio_file.get_data()),'\n')

# my_file = CSVFile('vdhoiqe.csv')
# print('dati: ', my_file.get_data())