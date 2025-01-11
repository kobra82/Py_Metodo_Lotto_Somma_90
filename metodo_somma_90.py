import argparse
from sys import exit
from os import system
import datetime

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
        if (array[i] not in array2):
            sum+=array[i]
    if (sum > 90):        
        return sum%90
    else:
        return sum

def terza_ambata(array,array2):
    nuovo_array = []
    for i in range(len(array)):
        if (array[i] not in array2):
            if (array[i] < 10):
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
            if (sum > 9):
                sum-=9
            nuovo_array2.append(sum)
        nuovo_array=nuovo_array2
    stringa = int(str(nuovo_array[0])+str(nuovo_array[1]))
    if (stringa > 90):        
        return stringa%90
    else:
        return stringa
    
parser = argparse.ArgumentParser()
parser.add_argument('-f1','--filein', help='file in ingresso')
parser.add_argument('-f2','--fileout', help='file in uscita')
parser.add_argument('-f3','--filecontrollo', help='file da controllare')

args = parser.parse_args()

if (args.filein):
    FILE_INPUT = args.filein
if (args.fileout):
    FILE_OUTPUT = args.fileout
   
if args.filecontrollo:
    FILE_CONTROLLO = args.filecontrollo
    with open(FILE_CONTROLLO, 'r', encoding='utf-8') as h:
        tabella = []
        for row in h:
            riga = row.split(';')
            riga[5] = str(int(riga[5]))
            tabella.append(riga)
            
    for i in range(len(tabella)):
        colpo = 0
        with open(FILE_INPUT, 'r', encoding='utf-8') as f:
            trovato = 0
            for row2 in f:
                riga2 = row2.split('\t')
                if ((datetime.datetime.strptime(str(tabella[i][0]),"%Y/%m/%d")) < (datetime.datetime.strptime(str(riga2[0]),"%Y/%m/%d")) and colpo < 6):
                    if (tabella[i][1] == riga2[1]):
                        numero = 0
                        esito = []
                        if tabella[i][2] in riga2[2:7]:
                            trovato = 1
                            numero += 1
                            esito.append(tabella[i][2])
                        if tabella[i][3] in riga2[2:7]:
                            trovato = 1
                            numero += 1
                            esito.append(tabella[i][3])
                        if tabella[i][4] in riga2[2:7]:
                            trovato = 1
                            numero += 1
                            esito.append(tabella[i][4])
                        if tabella[i][5] in riga2[2:7]:
                            trovato = 1
                            numero += 1
                            esito.append(tabella[i][5])
                        colpo += 1
                        if (numero > 0):
                            print(f"Previsione {tabella[i][:]} Data di uscita {riga2[0]} colpo {colpo} Ruota {riga2[1]} esito {esito}")
                        else:
                            if ((colpo == 6) and (trovato == 0)):
                                print(f"Previsione {tabella[i][:]} colpo fallito Data di uscita {riga2[0]}")
else:
    with open(FILE_INPUT, 'r', encoding='utf-8') as f:
        with open(FILE_OUTPUT, 'w', encoding='utf-8') as g:
            for row in f:
                array = row.split('\t')
                estrazione_array = [int(array[2]),int(array[3]),int(array[4]),int(array[5]),int(array[6])]
                arrayscelti = somma90(estrazione_array)
                if len(arrayscelti)>0:
                    ambata_uno = prima_ambata(arrayscelti)
                    ambata_due = seconda_ambata(estrazione_array, arrayscelti)
                    ambata_tre = terza_ambata(estrazione_array, arrayscelti)  
                    g.write(f"{str(array[0])};{str(array[1])};{int(ambata_uno)};{int(ambata_due)};{int(ambata_tre)};90\n")