import os # modulo che mi permette di controllare se il percorso file esiste

class ExamException(Exception): # classe ExamException che estende Exception
    pass

def clean_line(line): # funzione che controlla se la riga è 'pulita', la userò dopo per stabilire cosa aggiungere alla lista da ritornare
    try: 
        line[0] = int(float(line[0])) # l'epoch deve essere un intero
        line[1] = float(line[1]) # la temperatura invece un float
        return True # se entrambi i cast sono andati a buon fine ritorno vero
    except Exception: 
        return False # ritorno falso, ignorerò questa riga

def clean_list(series): # controlla se la squadra di scimmie ha fatto bene il suo lavoro - superfluo in questo caso
    if not isinstance(series, list): # se la serie passata non è una lista
        try:
            series = list(series) 
        except Exception:
            return False 
    for elements in series: # ciclo sugli elementi della serie
        if not isinstance(elements, list): # mi aspetto sia una lista di liste
            try: 
                elements = list(elements)
            except Exception:
                return False
        if not clean_line(elements): # provo a pulire la singola riga, ora che so che è accettabile
            return False 
        if len(elements) > 2: # se ha più di due elementi considero solo i primi due
            elements = elements[0 : 2] 
    return True

def convert_day(epoch): # funzione che ritorna solo il giorno rappresentato da un epoch
    return epoch - (epoch%86400)

class CSVTimeSeriesFile: # definisco la classe che ritornerà la lista time_series con i valori estratti dal CSV
    def __init__(self, name=None): # l'unico parametro è il nome del file
        self.name = name 

    def get_data(self): # funzione che estrae i dati e ritorna una lista
        if not isinstance(self.name, str): # se il nome non è una stringa
            raise ExamException('Errore! nome del file non valido') 
        
        if not os.path.exists(self.name): # se il file non esiste
            raise ExamException('Errore! file non trovato') 

        try: # provo ad aprire il file
            file = open(self.name, 'r')
        except Exception as e:
            raise ExamException('Errore! file non leggibile: ', e) 
            
        data = [] # lista in cui salverò i dati

        prev_epoch = None # variabile in cui salverò l'epoch precedente, alla prima iterazione non c'è un precedente e quindi è None

        for line in file: # leggo linea per linea il file
            elements = line.split(',') # divido gli elementi in base alla virgola
            elements[-1] = elements[-1].strip() # faccio lo strip dal campo -1
            if clean_line(elements): # se la linea è 'pulita', allora posso aggiungere gli elementi
                current_epoch = elements[0] # l'epoch corrente è quello di posto 0, lo userò per controllare che la lista sia in ordine
                if prev_epoch != None and current_epoch <= prev_epoch: # controllo se sono in ordine cronologico 
                    raise ExamException('Errore! lista non ordinata') 
                else:
                    prev_epoch = current_epoch # switcho il precedente con il corrente per proseguire col controllo alla prossima iterazione
                    elements = elements[0 : 2] # salvo solo i primi due elementi, così da risolvere il problema dei campi aggiuntivi
                    data.append(elements) 
            else: # altrimenti, se la mia linea non era 'pulita', la ignoro
                continue 

        file.close() 
        return data # ritorno la lista finale

def compute_daily_max_difference(time_series):
    final_list = [] # lista finale in cui salverò le escursioni termiche
    start = 0 # contatore per le righe della time_series
    if not clean_list(time_series):
        return []
    while start < len(time_series): # itero finché non arrivo alla fine della lista
        daily_list = [] 
        start_day = convert_day(time_series[start][0]) # estraggo il giorno dall'epoch da cui sto cominciando 
        for element in time_series:
            if convert_day(element[0]) == start_day: # se il giorno è lo stesso aggiungo l'elemento
                daily_list.append(element[1]) 
        if len(daily_list) > 1: # se per un giorno c'è più di una misurazione aggiungo la differenza
            final_list.append(max(daily_list)-min(daily_list))
        else: # altrimenti aggiungo None
            final_list.append(None)
        start += len(daily_list) + 1 # parto dal giorno successivo 
    return final_list                  

#my_file = CSVTimeSeriesFile(name='data.csv')
#time_series = my_file.get_data()
# print('lista dei dati:\n', time_series)

# diff_list = compute_daily_max_difference(time_series)
# print('lista delle escursioni termiche giornaliere:\n', diff_list)