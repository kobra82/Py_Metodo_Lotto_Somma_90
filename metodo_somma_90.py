import argparse
from sys import exit
from os import system

def somma90(array):
    ele1=99
    ele2=99
    for i in range(len(array)):
        for j in range(i+1,(len(array))):
            if (array[i]+array[j] == 90):
                ele1 = int(array[i])
                ele2 = int(array[j])
    scelti = []
    if ele1 != 99:
        scelti.append(ele1)
    if ele2 != 99:
        scelti.append(ele2)
    return scelti

def prima_ambata(array):
    if array[0] > array[1]:
        prima = array[0]-array[1]
    else:
        prima = array[1]-array[0]
    return prima

def seconda_ambata(array, array2):
    sum = 0
    for i in range(len(array)):
        if array[i] not in array2:
            sum+=array[i]
    if sum > 90:        
        return sum%90
    else:
        return sum

def terza_ambata(array,array2):
    nuovo_array = []
    for i in range(len(array)):
        if array[i] not in array2:
            if array[i] < 10:
                nuovo_array.append(array[i])
            else:
                decine = int(array[i]/10)
                unita = int(array[i])-(decine*10)
                nuovo_array.append(decine)
                nuovo_array.append(unita)
    while (len(nuovo_array)>2):
        nuovo_array2 = []
        for i in range(len(nuovo_array)-1):
            sum = nuovo_array[i]+nuovo_array[i+1]
            if sum > 9:
                sum = sum - 9
            nuovo_array2.append(sum)
        nuovo_array=nuovo_array2
    stringa = int(str(nuovo_array[0])+str(nuovo_array[1]))
    if stringa > 90:        
        return stringa%90
    else:
        return stringa
    
parser = argparse.ArgumentParser()
parser.add_argument('-f1','--filein', help='file in ingresso')
parser.add_argument('-f2','--fileout', help='file in uscita')
args = parser.parse_args()

if (args.filein):
    FILE_INPUT = args.filein
else:
    system("python.exe .\metodo_somma_90.py -h")
    exit()
if (args.fileout):
    FILE_OUTPUT = args.fileout
else:
    system("python.exe .\metodo_somma_90.py -h")
    exit()

with open(FILE_INPUT, 'r', encoding='utf-8') as f:
    with open(FILE_OUTPUT, 'w', encoding='utf-8') as g:
        for row in f:
            array = row.split('\t')
            estrazione_array = [int(array[2]),int(array[3]),int(array[4]),int(array[5]),int(array[6])]
            # print("Trovo i numeri che formano la somma 90")
            arrayscelti = somma90(estrazione_array)
            if len(arrayscelti)>0:
                # print("Calcolo la prima ambata")
                ambata_uno = prima_ambata(arrayscelti)
                # print("Calcolo la seconda ambata")
                ambata_due = seconda_ambata(estrazione_array, arrayscelti)
                # print("Calcolo la terza ambata")
                ambata_tre = terza_ambata(estrazione_array, arrayscelti)  
                # print("Stampo il risultato nel file di uscita")
                g.write(f"{str(array[0])};{str(array[1])};{int(ambata_uno)};{int(ambata_due)};{int(ambata_tre)}\n")
print("Procedura eseguita. File scritto con successo")