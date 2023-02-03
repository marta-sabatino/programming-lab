import os

def check_existance(file): # funzione che controlla se il file esiste
    if os.path.exists(file):
        return True # se esiste ritorno vero
    else:
        return False # altrimenti falso

class ExamException(Exception): # classe ExamException che estende Exception
    pass

def clean_line(line): # funzione che controlla se la riga è 'pulita', la userò dopo per stabilire cosa aggiungere alla lista da ritornare
    try: # controllo se posso castare a numerici i valori
        line[0] = int(float(line[0])) # l'epoch deve essere un intero
        line[1] = float(line[1]) # la temperatura invece un float
        return True # se entrambi i cast sono andati a buon fine ritorno vero
    except Exception: # se invece incorro in un'eccezione
        return False # ritorno falso, ignorerò questa riga

class CSVTimeSeriesFile: # definisco la classe che ritornerà la lista time_series con i valori estratti dal CSV
    def __init__(self, name=None): # l'unico parametro è il nome del file
        self.name = name 

    def get_data(self): # funzione che estrae i dati e ritorna una lista
        if not isinstance(self.name, str): # se il nome non è una stringa
            raise ExamException('Errore! nome del file non valido') # alzo un'eccezione
        
        if not check_existance(self.name): # se il file non esiste
            raise ExamException('Errore! file non trovato') # alzo un'eccezione

        try: # provo ad aprire il file
            file = open(self.name, 'r')
            file.readline() # leggo la prima riga
        except:
            raise ExamException('Errore! file non leggibile') # se non riesco alzo un'eccezione
            
        data = [] # lista in cui salverò i dati

        prev_epoch = None # variabile in cui salverò l'epoch precedente, alla prima iterazione non c'è un precedente e quindi è None

        for line in file: # leggo linea per linea il file
            elements = line.split(',') # divido gli elementi in base alla virgola
            elements[-1] = elements[-1].strip() # faccio lo strip dal campo -1
            if clean_line(elements): # se la linea è 'pulita', allora posso aggiungere gli elementi
                current_epoch = elements[0] # l'epoch corrente è quello di posto 0, lo userò per controllare che la lista sia in ordine
                if prev_epoch != None and current_epoch <= prev_epoch: # se il precedente non è None e gli epoch non sono ordinati
                    raise ExamException('Errore! lista non ordinata') # alzo l'eccezione
                else: # altrimenti, se gli epoch sono in ordine cronologico
                    prev_epoch = current_epoch # switcho il precedente con il corrente per proseguire col controllo alla prossima iterazione
                    elements = elements[0 : 2] # salvo solo i primi due elementi, così da risolvere il problema dei campi aggiuntivi
                    data.append(elements) # aggiungo gli elementi alla lista data
            else: # altrimenti, se la mia linea non era 'pulita'
                continue # vado avanti con l'esecuzione senza salvare quei dati

        file.close() 
        return data # ritorno la lista finale

def convert_day(epoch): # funzione che ritorna solo il giorno rappresentato da un epoch
    return epoch - (epoch%86400)

# def daily_difference(time_series, start):
#     daily_list = []
#     start_day = convert_day(time_series[start][0])
#     for element in time_series:
#         if convert_day(element[0]) == start_day:
#             daily_list.append(element[1])
            
#     if len(daily_list)>1:
#         return daily_list
#     else:
#         return None

def compute_daily_max_difference(time_series):
    final_list = [] # lista finale in cui salverò le escursioni termiche
    start = 0 # contatore per le righe della time_series
    while start < len(time_series): # itero finché non arrivo alla fine della lista
        daily_list = []
        start_day = convert_day(time_series[start][0])
        for element in time_series:
            if convert_day(element[0]) == start_day:
                daily_list.append(element[1])
        if len(daily_list)>1:
            final_list.append(max(daily_list)-min(daily_list))
        else:
            final_list.append(None)
        start += len(daily_list)
    return final_list # ritorno la lista delle escursioni termiche giornaliere          

# def compute_daily_max_difference(time_series):
#     final_list = [] # lista finale in cui salverò le escursioni termiche
#     counter = 0 # contatore per le righe della time_series
#     if not clean_list(time_series):
#         return
#     while counter < len(time_series): # itero finché non arrivo alla fine della lista 
#         tmp_list = [] # lista temporanea per le temperature di un singolo giorno
#         current_day = convert_day(time_series[counter][0]) # converto l'epoch di inizio al solo giorno 
#         tmp_list.append(time_series[counter][1]) # aggiungo la temperatura associata 
#         for i in range(counter + 1, len(time_series)): # itero sui successivi
#             day = convert_day(time_series[i][0]) # converto ogni epoch a giorno
#             if day == current_day: # controllo se il giorno è lo stesso
#                 tmp_list.append(time_series[i][1]) # aggiungo la temperatura associata alla lista temporanea
#             else: # se non sto più lavorando sullo stesso giorno
#                 break # esco dal for interno
#         counter += len(tmp_list) + 1 # salto le righe che appartenevano allo stesso giorno e ricomincio dalla successiva
#         if len(tmp_list) > 1: # se avevo più di una misurazione per un dato giorno
#             final_list.append(max(tmp_list)-min(tmp_list)) # aggiungo la differenza massima
#         else: 
#             final_list.append(None) # altrimenti aggiungo None
#     return final_list # ritorno la lista delle escursioni termiche giornaliere

def end_of_day(epoch):
    return convert_day(epoch) + 86400

my_file = CSVTimeSeriesFile(name='data.csv')
time_series = my_file.get_data()
print('lista dei dati:\n', time_series)

diff_list = compute_daily_max_difference(time_series)
print('lista delle escursioni termiche giornaliere:\n', diff_list)


# import os

# def check_existance(file): # funzione che controlla se il file esiste
#     if os.path.exists(file):
#         return True # se esiste ritorno vero
#     else:
#         return False # altrimenti falso

# class ExamException(Exception): # classe ExamException che estende Exception
#     pass

# def clean_line(line): # funzione che controlla se la riga è 'pulita', la userò dopo per stabilire cosa aggiungere alla lista da ritornare
#     try: # controllo se posso castare a numerici i valori
#         line[0] = int(float(line[0])) # l'epoch deve essere un intero
#         line[1] = float(line[1]) # la temperatura invece un float
#         return True # se entrambi i cast sono andati a buon fine ritorno vero
#     except Exception: # se invece incorro in un'eccezione
#         return False # ritorno falso, ignorerò questa riga

# class CSVTimeSeriesFile: # definisco la classe che ritornerà la lista time_series con i valori estratti dal CSV
#     def __init__(self, name=None): # l'unico parametro è il nome del file
#         self.name = name 

#     def get_data(self): # funzione che estrae i dati e ritorna una lista
#         if not isinstance(self.name, str): # se il nome non è una stringa
#             raise ExamException('Errore! nome del file non valido') # alzo un'eccezione

#         try: # provo ad aprire il file
#             file = open(self.name, 'r')
#             # file.readline() # leggo la prima riga
#         except FileNotFoundError as e:
#             raise ExamException('Errore! file non leggibile', e) # se non riesco alzo un'eccezione
            
#         data = [] # lista in cui salverò i dati
#         # my_file = open(self.name, 'r') # apro il file in lettura

#         prev_epoch = None # variabile in cui salverò l'epoch precedente, alla prima iterazione non c'è un precedente e quindi è None

#         for line in my_file: # leggo linea per linea il file
#             elements = line.split(',') # divido gli elementi in base alla virgola
#             elements[-1] = elements[-1].strip() # faccio lo strip dal campo -1
#             if clean_line(elements): # se la linea è 'pulita', allora posso aggiungere gli elementi
#                 current_epoch = elements[0] # l'epoch corrente è quello di posto 0, lo userò per controllare che la lista sia in ordine
#                 if prev_epoch != None and current_epoch <= prev_epoch: # se il precedente non è None e gli epoch non sono ordinati
#                     raise ExamException('Errore! lista non ordinata') # alzo l'eccezione
#                 else: # altrimenti, se gli epoch sono in ordine cronologico
#                     prev_epoch = current_epoch # switcho il precedente con il corrente per proseguire col controllo alla prossima iterazione
#                     elements = elements[0 : 2] # salvo solo i primi due elementi, così da risolvere il problema dei campi aggiuntivi
#                     data.append(elements) # aggiungo gli elementi alla lista data
#             else: # altrimenti, se la mia linea non era 'pulita'
#                 continue # vado avanti con l'esecuzione senza salvare quei dati

#         my_file.close() 
#         return data # ritorno la lista finale

# def convert_day(epoch): # funzione che ritorna solo il giorno rappresentato da un epoch
#     return int(epoch) - (int(epoch)%86400)

# def compute_daily_max_difference(time_series):
#     final_list = [] # lista finale in cui salverò le escursioni termiche
#     counter = 0 # contatore per le righe della time_series
#     while counter < len(time_series): # itero finché non arrivo alla fine della lista 
#         tmp_list = [] # lista temporanea per le temperature di un singolo giorno
#         current_day = convert_day(time_series[counter][0]) # converto l'epoch di inizio al solo giorno 
#         tmp_list.append(time_series[counter][1]) # aggiungo la temperatura associata 
#         for i in range(counter + 1, len(time_series)): # itero sui successivi
#             day = convert_day(time_series[i][0]) # converto ogni epoch a giorno
#             if day == current_day: # controllo se il giorno è lo stesso
#                 tmp_list.append(time_series[i][1]) # aggiungo la temperatura associata alla lista temporanea
#             else: # se non sto più lavorando sullo stesso giorno
#                 break # esco dal for interno
#         counter += len(tmp_list) + 1 # salto le righe che appartenevano allo stesso giorno e ricomincio dalla successiva
#         if len(tmp_list) > 1: # se avevo più di una misurazione per un dato giorno
#             final_list.append(max(tmp_list)-min(tmp_list)) # aggiungo la differenza massima
#         else: 
#             final_list.append(None) # altrimenti aggiungo None
#     return final_list # ritorno la lista delle escursioni termiche giornaliere               

# my_file = CSVTimeSeriesFile(name='datasfa.csv')
# time_series = my_file.get_data()
# print('lista dei dati:\n', time_series)

# diff_list = compute_daily_max_difference(time_series)
# print('lista delle escursioni termiche giornaliere:\n', diff_list)



# # def compute_daily_max_difference(time_series):
# #     final_list = []

# #     for counter in range(len(time_series)):
# #         daily_list = []
# #         daily_list.append(float(time_series[counter][1]))
# #         current_day = int(time_series[counter][0]) - (int(time_series[counter][0])%86400)
        
# #         for i in range(counter+1, len(time_series)):
# #             day = int(time_series[i][0]) - (int(time_series[i][0])%86400)
# #             if day == current_day:
# #                 daily_list.append(float(time_series[i][1]))
# #             else:
# #                 break
# #             i += 1
# #         final_list.append(max(daily_list)-min(daily_list))
# #     return daily_list



# # print('\nNome del file: "{}"'.format(my_file.name),'\n')
# # print('\nDati contenuti nel file: "{}"'.format(my_file.get_data()),'\n')


# # print('prova = ', (int(time_series[0][0]) - (int(time_series[0][0])%86400))) # con questa formula troviamo il giorno con un resto trascurabile 
# # # per vedere se due timestamp indicano lo stesso giorno divido per
# # print('timestamp = ', time_series[0][0])
# # print(daily_difference(time_series, 28))



# # def compute_daily_max_difference(time_series):
# #     final_list = []
# #     current_day = 0
# #     for current_day in range(len(time_series)):
# #         current_day_list = daily_difference(time_series, current_day)
# #         final_list.append(max(current_day_list) - min(current_day_list))
# #         current_day = len(current_day_list) + 1
# #         if current_day == len(time_series):
# #             break
# #     return final_list

# # def compute_daily_max_difference(time_series):
# #     final_list = []

# #     for i in range (len(time_series)):
# #         current_day = int(time_series[i][0]) - (int(time_series[i][0])%86400)        
# #         index = i + 1

# #         for index in range(len(time_series) - 1):
#             tmp_list = []
#             tmp_list.append(float(time_series[i][1]))
#             day = int(time_series[index][0]) - (int(time_series[index][0]) % 86400)        
#             while day == current_day:
#                 tmp_list.append(float(time_series[index][1]))
#                 index += 1
#             final_list.append(max(tmp_list)-min(tmp_list))

#         i = index + 1 
#     return final_list

# def compute_daily_max_difference(time_series):
#     final_list = []
#     start_day = 0
#     for start_day in range(len(time_series)):
#         tmp_list = daily_difference(time_series, start_day)
#         if len(tmp_list) > 1:
#             difference = max(tmp_list) - min(tmp_list)
#             final_list.append(difference)
#         else:
#             final_list.append(None)
#         start_day = len(tmp_list)
    
#     return final_list

# def extract_epochs(time_series):
#     epoch_list = []
#     for i in range(len(time_series)):
#         epoch_list.append(int(time_series[i][0]))
#     return epoch_list

# def only_days(epoch_list):
#     for i in range(len(epoch_list)):
#         epoch_list[i] = epoch_list[i] - (epoch_list[i]%86400)
#     return epoch_list



# def count_different(epoch_list):
#     epoch_list = only_days(epoch_list)
#     return len(set(epoch_list))

# def count_occurrences(value, lst):
#     return lst.count(value)

# epoch_list = extract_epochs(time_series)
# print('numero di epoch = ', len(epoch_list))
# print('numero di giorni = ', count_different(epoch_list))

# day_list = daily_difference(time_series, 48)
# print(day_list)
# print(max(day_list)-min(day_list))
# print(len(day_list))
# print(set(only_days(epoch_list)))


# def daily_difference(time_series, start):
#     daily_list = []
#     daily_list.append(float(time_series[start][1]))
#     current_day = int(time_series[start][0]) - (int(time_series[start][0])%86400)
#     for i in range(start+1, len(time_series)):
#         day = int(time_series[i][0]) - (int(time_series[i][0])%86400)
#         if day == current_day:
#             daily_list.append(float(time_series[i][1]))
#         else:
#             break
#         i += 1
#     return daily_list

# def compute_daily_max_difference(time_series):
#     final_list = []
#     counter = 0
#     while counter < len(time_series):
#         tmp_list = list(daily_difference(time_series, counter))
#         counter += len(tmp_list) + 1
#         if len(tmp_list) > 1:
#             final_list.append(max(tmp_list) - min(tmp_list))
#         else: 
#             final_list.append(None)
#     return final_list



# class CSVTimeSeriesFile:
#     def __init__(self, name):
#         self.name = name
#         if not isinstance(self.name, str):
#             raise ExamException('Errore! il nome del file deve essere una stringa')

#         self.can_read = True
#         try:
#             file = open(self.name, 'r')
#             file.readline()
#         except:
#             raise ExamException('Errore! file non leggibile')
            

#     def get_data(self):
#         data = []
#         my_file = open(self.name, 'r')

#         for line in my_file:
#             elements = line.split(',')
#             elements[-1] = elements[-1].strip()
#             if elements[0] != 'epoch':
#                 try:
#                     elements[0] = int(elements[0])
#                 except:
#                     raise ExamException('Errore! non riesco a convertire a valori numerici')
#                 data.append(elements)
#         my_file.close()    
#         return data