class ExamException(Exception):
    pass

class MovingAverage:
    def __init__(self, window_len):
        self.window_len = window_len

        if window_len == None:
            raise ExamException('errore! non è stato inserito nessun valore')

        if not isinstance(window_len, int):
            raise ExamException('errore! la lunghezza della finestra deve essere un itero')

        if window_len <= 0:
            raise ExamException('errore! la lunghezza della finestra deve essere un valore positivo')

    def compute(self, value_list):
        counter = 0
        result = []

        if not isinstance(value_list, list):
            raise ExamException('errore! l input deve essere una lista')

        if len(value_list) == 0:
            raise ExamException('errore! lista vuota')
        
        for item in value_list:
            if not isinstance(item, int) and not isinstance(item, float):
                raise ExamException('errore! la lista deve essere composta da numeri')

        if self.window_len > len(value_list):
            raise ExamException('errore! la finestra è più lunga della lista')

        while counter < len(value_list) - self.window_len + 1:
            window = value_list[counter : counter + self.window_len]

            current_average = sum(window)/self.window_len
            result.append(current_average)
            counter += 1

        return result

# moving_average = MovingAverage(-1)
# result = moving_average.compute([2,4,8,16])
# print(result) # Deve stampare a schermo [3,6,12]