def increment(data): # media degli incrementi
    prev_value = None
    increment = 0

    for item in data:
        if prev_value!=None:
            increment += item - prev_value
            increment = item
    
    return increment/len(data)

class Errore(Exception):
    pass

class Model():

    def fit(self, data):
        #fit non implementato nella classe base
        raise NotImplementedError('Metodo non implementato')

    def predict(self, data):
        #Predict non implementato nella classe base
        raise NotImplementedError('Metodo non implementato')


class IncrementModel(Model):

    def predict(self, data):  #data = [50,52,60]
        prev_value = None
        prediction = 0

        for item in data:
            if not isinstance(item, int):
                raise Errore('Non è possibile calcolare una previsione su dati non numerici')
            else:
                if prev_value != None:
                    prediction += item - prev_value
                    print('item: {}'.format(item))
                    prev_value = item
                    print('prediction: {}'.format(prediction))
                else:
                    prev_value = item
            print('data_len: {}'.format(len(data)))
        if len(data) <= 1:
            raise Errore("Troppi pochi dati per poter eseguire una previsione")
        else:
            prediction = prediction / (len(data) - 1) + data[-1]
            print('prediction: {}'.format(prediction))
        return prediction


class FitIncrementModel(IncrementModel):
    def __init__(self, global_avg_increment):
        self.global_avg_increment = global_avg_increment

    first_numbers = [8, 19, 31, 41]
    last_numbers = [50, 52, 60]

    def fit(self, data):
        super().fit(data)
        self.global_avg_increment = increment(first_numbers)+

    
data = [50, 52, 60]
print(increment(data))