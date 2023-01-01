class Model:
    def fit(self, data):
        raise NotImplementedError('Metodo non implementato')
    
    def predict(self, data):
        raise NotImplementedError('Metodo non implementato')

class IncrementModel(Model):
    def predict(self, data):
        previous_value = None
        increment = []
        
        try:
            for item in data:
                if previous_value == None:
                    previous_value = item
                    pass
                else:
                    increment.append(item - previous_value)
                    previous_value = item 
    
            average_increment = sum(increment)/(len(data)-1)
            prediction = previous_value + average_increment
            return prediction

        except:
            raise ZeroDivisionError
            
# data = []
# data_prediction = IncrementModel()
# p = data_prediction.predict(data)
# print('\nPredizione = ', p, '\n')