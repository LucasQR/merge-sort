# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 02:00:03 2023

@author: kamma
"""

import csv 
import numpy as np
import sys
import math
import os
 
# Lendo o arquivo original 
with open('data''.csv', 'r') as read_obj: 
    csv_reader = csv.reader(read_obj) 
    list_of_csv = list(csv_reader) 
    print(list_of_csv)

bit_size = 1000 #byte tamanho nos queremos em cada "buffer"

# Aqui aproximando que cada objecto tem mais ou menos o mesmo tamanho
N = math.ceil(sys.getsizeof(list_of_csv)/bit_size)
list_size = np.shape(list_of_csv)[0]/N #Numeros de objetos em  cada "buffer"

#Criando e salvando arquvos, onde cada um contêm um parte das dados.
start = 0
filename = 0
for i in np.arange(1,N+1):
    data_buf = list_of_csv[start: int(i*list_size)]
    start = int(i*list_size)
    np.savetxt("buffer" + str(filename) + ".csv",data_buf, delimiter =",", fmt ='% s') 
    filename += 1




def mergeSort(myList):
    if len(myList) > 1:
        #Criando seperacão de dados
        left = myList[:len(myList) // 2] 
        right = myList[len(myList) // 2:]
        
        #recucão
        mergeSort(left)
        mergeSort(right)
        merge(myList, left,right)
        #combinar
        
def merge(myList, left,right):
        i = 0 #array esquerta
        j = 0 #array direta
        k = 0 #array novo
        
        while i < len(left) and j < len(right): #tem mais dados em ambos left e right 
            if int(left[i][0]) < int(right[j][0]):
                myList[k] = left[i]
                i+=1
            else:
                myList[k] = right[j]
                j+=1
            k+=1
        
        #Só tem mais dodos em left
        while i < len(left):
            myList[k] = left[i]
            i+=1
            k+=1
            
        #Só tem mais dados em right
        while j < len(right):
            myList[k] = right[j]
            j+=1
            k+=1
        
#Agora nos vamos fazer a ordanacao para cada buffer
for i in np.arange(0,N):
    with open('buffer' + str(i) + '.csv', 'r') as read_obj: 
        csv_reader = csv.reader(read_obj) 
        list_of_csv = list(csv_reader)  
        mergeSort(list_of_csv)
        #salvamos os aquivos ordenado como "sorteret"
        np.savetxt("sorteret" + str(i) + ".csv",list_of_csv, delimiter =",", fmt ='% s')
        read_obj.close()
        os.remove('buffer' + str(i) + '.csv') #aqui nos deletamos os buffers que não estava ordenados.


#Aqui nos combinamos os arquivos
merge_nr = 0 
while merge_nr <=np.ceil(np.log(9)): #o numero de vezes nos precisamos combinar todos os arquivos dois e dois
    for i in np.arange(0,np.ceil(N/2)): #Metade do numero de arquivos
        #Ler arquivo numero 2*i e 2*i+1
        with open('sorteret' + str(int(i*2)) + '.csv', 'r') as read_obj_1: 
             csv_reader_1 = csv.reader(read_obj_1) 
             list_of_csv_1 = list(csv_reader_1)  
        if i*2+1 < N:
          with open('sorteret' + str(int(i*2+1)) + '.csv', 'r') as read_obj_2: 
             csv_reader_2 = csv.reader(read_obj_2) 
             list_of_csv_2 = list(csv_reader_2)          
          #Criar uma nova lista onde a combinacão dos dois listas vai ser salvado
          myList = [None]*(len(list_of_csv_1) + len(list_of_csv_2))
          merge(myList, list_of_csv_1,list_of_csv_2) #fazer o merge
          os.remove('sorteret' + str(int(i*2+1)) + '.csv') #deletar os dois arquivos já usados  
          os.remove('sorteret' + str(int(i*2)) + '.csv')  
          #salvar o novo arquivo com o numero i
          np.savetxt("sorteret" + str(int(i)) + ".csv",myList, delimiter =",", fmt ='% s') 
        else:
        #Para o caso onde nós temos um numero impar de dados, 
        # aí o ultimo vai ser salvado sem fazendo o "merge".
         np.savetxt("sorteret" + str(int(i)) + ".csv",list_of_csv_1, delimiter =",", fmt ='% s')
         os.remove('sorteret' + str(int(i*2)) + '.csv')  
    merge_nr += 1
    N = np.ceil(N/2)
     