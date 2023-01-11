class ExamException(Exception):
    pass

class Diff:
    def __init__(self, ratio=1):
        self.ratio = ratio

        if not isinstance(ratio, int) and not isinstance(ratio, float):
            raise ExamException('errore! ratio deve essere un numero')

        if ratio <= 0:
            raise ExamException('errore! ratio deve essere >= 1')

    def compute(self, value_list):
        result = []

        if not isinstance(value_list, list):
            raise ExamException('errore! l input deve essere una lista')

        if len(value_list) == 0:
            raise ExamException('errore! la lista è vuota')

        for item in value_list:
            if not isinstance(item, int) and not isinstance(item, float):
                raise ExamException('errore! la lista deve essere composta da numeri')

        if len(value_list) < 2:
            raise ExamException('errore! la lista deve contenere almeno due elementi')
        
        for i in range(len(value_list)-1):
            difference = value_list[i+1]-value_list[i]
            result.append(difference/self.ratio)
            i += 1

        return result

# diff = Diff()
# result = diff.compute([2,4,8,16])
# print(result) # Deve stampare a schermo [2.0,4.0,8.0]