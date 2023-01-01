# Scrivete una funzione sum_csv(file_name)
# che sommi tutti i valori delle vendite degli
# shampoo del file passato come argomento

def sum_csv(file_name):
    values = [] # lista in cui salverò i valori

    file = open(file_name, 'r') # apro il file in modalità lettura

    empty = True # variabile che controlla se il file è vuoto

    for line in file:
        elements = line.split(',') # faccio lo split dopo la virgola

        if elements[0]!= 'Date': # se sono sulla riga successiva alla data

            value = elements[1] # variabile valore è l'elemento di posto 1 (i dati sono disposti come: 0 | 1, ovvero data | valore)

            try: # provo a convertire a float
                value = float(value) # trasformo in float
                values.append(value) # aggiungo alla lista dei valori
                empty = False # allora la lista non è vuota

            except Exception as e: # ma se non ci riesco
                print(e) # alzo l'eccezione

    if empty == True: # se la lista è vuota
        return None # non ritorno nulla
    else: # altrimenti 
        return sum(values) # ritorno la somma dei valori

# print('\nprova su file vero:\n')
# print(sum_csv('shampoo_sales.csv'))
# print('\nprova su file vuoto:\n')
# print(sum_csv('empty_file.csv'))
# print('\nprova su file con valori non numerici:\n')
# print(sum_csv('error_file.csv'))