class ExamException(Exception):
    pass

class CSVFile:
    def __init__(self, name=None):
        self.name = name

    def get_data(self):
        data = []
        try:
            my_file = open(self.name, 'r')
        except FileExistsError as e:
            raise ExamException

        header = my_file.readline()

        for line in my_file:
            elements = line.split(',')
            elements[-1] = elements[-1].strip()
            if elements[0]!=header:
                data.append(elements)

        my_file.close()
        return data

def clean_line(line):
    try:
        line[0] = int(float(line[0]))
        line[1] = float(line[1])
        return True
    except Exception:
        return False

class CSVTimeSeriesFile(CSVFile):
        
    def get_data(self):
        # if not isinstance(self.name, str):
        #     raise ExamException('Errore! nome del file non valido')
        
        # try:
        #     file = open(self.name, 'r')
        # except:
        #     raise ExamException('Errore! file non leggibile')
        
        # try:
        #     file.readline()
        # except:
        #     file.close()
        #     raise ExamException('Errore! file non leggibile')
            
        # else:
        data_original = super().get_data()
        data = []
        my_file = open(self.name, 'r')

        header = my_file.readline()

        prev_epoch = None

        for elements in data_original:
            # elements = line.split(',')
            elements[-1] = elements[-1].strip()
            if elements[0]!=header:
                if clean_line(elements):
                    current_epoch = elements[0]
                    if prev_epoch != None and current_epoch <= prev_epoch:
                        raise ExamException('Errore! lista non ordinata')
                    else:
                        prev_epoch = current_epoch
                        elements = elements[0 : 2]
                        data.append(elements)
                else:
                    continue
        return data


def convert_day(epoch):
    return int(epoch) - (int(epoch)%86400)

def compute_daily_max_difference(time_series):
    final_list = []
    counter = 0
    while counter < len(time_series):
        tmp_list = []
        current_day = convert_day(time_series[counter][0])
        tmp_list.append(time_series[counter][1])
        for i in range(counter + 1, len(time_series)):
            day = convert_day(time_series[i][0])
            if day == current_day:
                tmp_list.append(time_series[i][1])
            else:
                break
        counter += len(tmp_list) + 1
        if len(tmp_list) > 1:
            final_list.append(max(tmp_list)-min(tmp_list))
        else:
            final_list.append(None)
    return final_list               

my_file = CSVTimeSeriesFile('data.csv')
time_series = my_file.get_data()
print('lista dei dati:\n', time_series)

diff_list = compute_daily_max_difference(time_series)
print('lista delle escursioni termiche giornaliere:\n', diff_list)