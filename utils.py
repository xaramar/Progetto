import numpy as np
import networkx as nx
from networkx.utils import powerlaw_sequence
import time
import sys
import importlib #per poter usare il comando reload

import pickle
import os.path

importlib.reload(sys)  #questo è il comando per python3
# Ricarica un modulo precedentemente importato . L'argomento deve essere un oggetto modulo, quindi deve essere stato importato con successo prima. Ciò è utile se hai modificato il
# file sorgente del modulo utilizzando un editor esterno e desideri provare la nuova versione senza lasciare l'interprete Python. Il valore restituito è l'oggetto modulo
# (che può essere diverso se la reimportazione causa l'inserimento di un oggetto diverso sys.modules).
if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8") # Modifica necessaria per l'utilizzo in python3 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

from datetime import datetime, timedelta
# Si può usare datetime per eseguire operazioni aritmetiche basiche sulle date con la classe timedelta. La sottrazione tra date produce un timedelta, ed un timedelta può essere
# aggiunto o sottratto ad una data per produrre un'altra data. I valori interni per timedelta sono conservati in giorni, secondi, e microsecondi.








def generateGraph(n = 100, seed = 1.0): #@# Questo valore può essere modificato quando si richiama la funzione?
    generated = False
    while not generated:
        try: # try except serve per evitare che il programma si blocchi con gli errori
            z = nx.utils.create_degree_sequence(n, powerlaw_sequence) #@# Cosa genero esattamente qui? @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            G = nx.configuration_model(z, seed = seed)
            # Restituisce un grafico casuale con la sequenza di gradi data.
            # Il modello di configurazione genera uno pseudografo casuale (grafico con bordi paralleli e loop automatici) assegnando in modo casuale i bordi per abbinare la
            # sequenza di gradi data.
            #
            # z = deg_sequence = elenco di numeri interi, ogni voce dell'elenco corrisponde al grado di un nodo
            # seed = seme per generare numeri casuali

            generated = True
        except:
            pass
    G = nx.Graph(G) #@# Cosa ottengo con questo comando? @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    G.remove_edges_from(G.selfloop_edges()) #@# Cosa ottengo con questo comando? @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    return G
    
def readdata(filename, unix = True):
    timestamps = []
    with open(filename, 'r') as f:    # Con with il file viene chiuso in automatico non appena si esce dal blocco di with. In questo caso si evita che si dimentichi di chiuderlo.
        for line in f:                
            line = line.strip().split(' ')
            if not unix: # Non capito questa parta @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                tstr =  line[0][1:] + ' ' + line[1][0:-1] # in questo modo ottengo solo questo risultato 2006-05-09 04:10:57 da una stringa "2006-05-09 04:10:57" 12830 14791
                t = datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S') # stampando type di t vedrei che ora è di tido datetime.datetime anche se facendo solo print sarebbero uguali ma a
                # cosa serve questo t? @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                timestamp = time.mktime(datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S').timetuple()) # Questo comando mi restituisce il tempo in secondi a partire dalla mia "base",
                # ovvero il 1970
                
                tst, n1, n2 = int(timestamp), line[2], line[3] # In questo modo ho su tst il timestamp in secondi, in n1 e n2 gli altri valori della stringa importata
            else: # Domanda collegata al perché si usa unix @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                timestamp = int(line[0])
                tst, n1, n2 = int(line[0]), int(line[1]), int(line[2])
            
            if n1 == n2:
                continue
            
            if n2 < n1:
                n1, n2 = n2, n1            
            timestamps.append((tst, n1, n2))    # aggiungo alla lista timestamp
        timestamps.sort() # ordino la lista timestamp
    return timestamps
    
def readdata_dict(filename, unix = True):
    timestamps = {}
    with open(filename, 'r') as f:    
        for line in f:                
            line = line.strip().split(' ')
            if not unix:
                tstr =  line[0][1:] + ' ' +line[1][0:-1]
                t = datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S')
                timestamp = time.mktime(datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S').timetuple())
                
                tst, n1, n2 = int(timestamp), line[2], line[3]
            else:
                timestamp = int(line[0])
                tst, n1, n2 = int(line[0]), int(line[1]), int(line[2])
            
            if n1 == n2:
                continue
            
            if n2 < n1:
                n1, n2 = n2, n1
            if tst not in timestamps:
                timestamps[tst] = [] # fin qui tutto prima come la funzione readdata ma a questo punto si crea un dizionario con chiave la somma tempo in secondi (timestamp) e
                # come valore un lista vuota
            timestamps[tst].append((n1, n2)) # A questo punto si aggiungono alla lista vuota i due valori n1 e n2. Quindi ottengo un dizionario con chiave il timestamp e
            # valore n1 e n2
    return timestamps
    
def readdata_dict_limit(filename, limit = 1000, unix = True):
    timestamps = {}
    with open(filename, 'r') as f:
        c = 0
        for line in f:                
            line = line.strip().split(' ')
            if not unix:
                tstr =  line[0][1:] + ' ' +line[1][0:-1]
                t = datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S')
                timestamp = time.mktime(datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S').timetuple())
                
                tst, n1, n2 = int(timestamp), line[2], line[3]
            else:
                timestamp = int(line[0])
                tst, n1, n2 = int(line[0]), int(line[1]), int(line[2])
            
            if n1 == n2:
                continue
            
            if n2 < n1:
                n1, n2 = n2, n1
            if tst not in timestamps:
                timestamps[tst] = []
            timestamps[tst].append((n1, n2))
            c += 1
            if c >= limit:   # Funzione identica alla precedente ma pongo un limite con c che quando viene raggiunto (diventa uguale a limit) applica il return e quindi
                # conclude la funzione
                return timestamps
    return timestamps












def readgraph(filename, unix = True):
    G = nx.Graph()
    with open(filename, 'r') as f:    
        for line in f:                
            line = line.strip().split(' ')
            n1, n2 = int(line[2]), int(line[3])            
            if n1 != n2:
                if n2 < n1:
                    n1, n2 = n2, n1  
                G.add_edge(n1, n2)
    return G        

def generateTS(G, len = 10000):
    timestamps = []
    edges = G.edges()
    idx = np.random.choice(G.number_of_edges(), len)
    for tst in range(len):    # modifico da xrange a range per python3
        n1, n2 = edges[idx[tst]]
        if n2 < n1:
            n1, n2 = n2, n1            
        timestamps.append((tst, n1, n2))
    return timestamps
    
def generateTS_dict(G, len = 10000):
    timestamps = {}
    edges = G.edges()
    idx = np.random.choice(G.number_of_edges(), len)
    for tst in range(len):   # modifico da xrange a range per python3
        n1, n2 = edges[idx[tst]]
        if n2 < n1:
            n1, n2 = n2, n1
        if tst not in timestamps:
            timestamps[tst] = []
        timestamps[tst].append((n1, n2))
    return timestamps
        
    
def generateTS_planted(G, len = 100, k = 10, clique_size = 5, interval = 10):
    timestamps = []
    edges = G.edges()
    idx = np.random.choice(G.number_of_nodes(), len)
    for tst in range(len):   # modifico da xrange a range per python3
        n1, n2 = edges[idx[tst]]
        if n2 < n1:
            n1, n2 = n2, n1            
        timestamps.append((tst, n1, n2))
    
    cl = nx.complete_graph(clique_size)    
    start = interval
    max_ID = max(G.nodes())  
    tst = start
    for i in range(k):    # modifico da xrange a range per python3
        cl_tmp = nx.relabel_nodes(cl, {n: i+max_ID+1 for (i, n) in enumerate(cl.nodes())})
        for (n1, n2) in cl_tmp.edges():
            if n2 < n1:
                n1, n2 = n2, n1
            timestamps.append((tst, n1, n2))
        tst += interval
        max_ID = max(cl_tmp.nodes())
        
    timestamps.sort()
    return timestamps
