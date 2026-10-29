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
    tabella = []
    righe_originali = []  # <--- NUOVA RIGA
    with open(FILE_CONTROLLO, 'r', encoding='utf-8') as h:
        for row in h:
            if row.strip():
                righe_originali.append(row)  # <--- NUOVA RIGA
                riga = row.split(';')
                riga[5] = str(int(riga[5]))
                tabella.append(riga)
    
    previsioni_da_eliminare = set()  # <--- NUOVA RIGA (tiene traccia di chi ha vinto)

            
    for i in range(len(tabella)):
        colpo = 0
        with open(FILE_INPUT, 'r', encoding='utf-8') as f:
            trovato = 0
            for row2 in f:
                riga2 = row2.split('\t')
                if ((datetime.datetime.strptime(str(tabella[i][0]),"%Y/%m/%d")) < (datetime.datetime.strptime(str(riga2[0]),"%Y/%m/%d")) and colpo < 6):
                    if (tabella[i][1] == riga2[1]):
                        estratti_puliti = [x.strip() for x in riga2[2:7]]
                        numero = 0
                        esito = []
                        if tabella[i][2].strip() in estratti_puliti:
                            trovato = 1
                            numero += 1
                            esito.append(tabella[i][2])
                        if tabella[i][3].strip() in estratti_puliti:
                            trovato = 1
                            numero += 1
                            esito.append(tabella[i][3])
                        if tabella[i][4].strip() in estratti_puliti:
                            trovato = 1
                            numero += 1
                            esito.append(tabella[i][4])
                        if tabella[i][5].strip() in estratti_puliti:
                            trovato = 1
                            numero += 1
                            esito.append(tabella[i][5])
                        colpo += 1
                        if (numero > 0):
                            print(f"Previsione {tabella[i][:]} Data di uscita {riga2[0]} colpo {colpo} Ruota {riga2[1]} esito {esito}")
                            previsioni_da_eliminare.add(i)
                        else:
                            if ((colpo == 6) and (trovato == 0)):
                                print(f"Previsione {tabella[i][:]} colpo fallito Data di uscita {riga2[0]}")
                                previsioni_da_eliminare.add(i)
                                
    with open(FILE_CONTROLLO, 'w', encoding='utf-8') as h_out:
        for indice, riga_testo in enumerate(righe_originali):
            if indice not in previsioni_da_eliminare:
                h_out.write(riga_testo)                            
else:
    # Carichiamo prima tutto l'archivio in memoria per poter scorrere i colpi successivi
    with open(FILE_INPUT, 'r', encoding='utf-8') as f:
        archivio = [row.strip().split('\t') for row in f if row.strip()]

    with open(FILE_OUTPUT, 'w', encoding='utf-8') as g:
        for i, riga_corrente in enumerate(archivio):
            if len(riga_corrente) < 7: continue
            
            data_corrente = datetime.datetime.strptime(riga_corrente[0], "%Y/%m/%d")
            ruota_corrente = riga_corrente[1]
            
            estrazione_array = [int(riga_corrente[2]), int(riga_corrente[3]), int(riga_corrente[4]), int(riga_corrente[5]), int(riga_corrente[6])]
            arrayscelti = somma90(estrazione_array)
            
            if len(arrayscelti) > 0:
                # Calcoliamo la previsione teorica
                ambata_uno = prima_ambata(arrayscelti)
                ambata_due = seconda_ambata(estrazione_array, arrayscelti)
                ambata_tre = terza_ambata(estrazione_array, arrayscelti)
                
                # Creiamo la quartina teorica per il controllo preventivo (con il 90 fisso)
                numeri_previsione = [str(int(ambata_uno)), str(int(ambata_due)), str(int(ambata_tre)), "90"]
                
                colpi_passati = 0
                gia_sfaldato = False
                
                # Controlliamo cosa è successo nei colpi successivi su quella ruota
                for riga_successiva in archivio[i+1:]:
                    if riga_successiva[1] == ruota_corrente:
                        data_successiva = datetime.datetime.strptime(riga_successiva[0], "%Y/%m/%d")
                        if data_successiva > data_corrente:
                            colpi_passati += 1
                            
                            # Controlliamo se è uscito un numero nei colpi precedenti
                            if colpi_passati <= 5:
                                estratti_reali = [x.strip() for x in riga_successiva[2:7]]
                                for num in numeri_previsione:
                                    if num in estratti_reali:
                                        gia_sfaldato = True
                
                # Calcoliamo il colpo a cui è arrivata la previsione per la prossima estrazione
                colpo_prossimo = colpi_passati + 1
                
                # LA LISTA DELLA SPESA: Mostra le previsioni vergini che si trovano tra il 3° e il 5° colpo utile
                if 3 <= colpo_prossimo <= 5 and not gia_sfaldato:
                    # Modificata la stringa di scrittura: inserisce il colpo corrente alla fine della riga
                    g.write(f"{str(riga_corrente[0])};{str(riga_corrente[1])};{int(ambata_uno)};{int(ambata_due)};{int(ambata_tre)};90;COLPO_{colpo_prossimo}\n")
