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

            counter = 0

            for line in file:
                elements = line.split(',')
                elements[-1] = elements[-1].strip()
                counter += 1

            # non gestisce caso in cui solo start/end è None

                # if start == None and end == None:
                #     if elements[0]!='Date':
                #         data.append(elements)

                # else:
                try:
                    if start == None:
                        start = 0
                    if end == None:
                        end = len(list(file))

                    start = int(start)
                    end = int(end)

                    if end < start:
                        raise Exception

                    if elements[0] != 'Date' and counter >= start:
                        data.append(elements)

                    if counter == end: 
                        break

                except:
                    raise Exception
    
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
print(myfile.get_data())