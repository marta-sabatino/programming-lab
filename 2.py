# Scrivete una funzione sum_list(my_list)
# che sommi tutti gli elementi di una lista

def sum_list(lista):
    if len(lista)==0:
        return None
    else:
        return sum(lista)

mylist = []
print(sum_list(mylist))