import utils
import copy



################################
### CALCOLO DENSITà SUBGRAFO ###
################################

def averageDens(dic):
    a = 0
    if (len(dic) == 0):
        return a
    for i in dic.keys():
        ###print ('prova',i)
        a += len(dic[i])  # 'a' non sarà per forza uguale al totale delle coppie perché se si ripetono non conta
    # print('a',a)
    b = a / len(dic)  # Questa è la densità del sottografo, Nell'altro codice era pari a {a = a / (2.0 * len(dic))} <- come mai?
    return b


########################################################################################################
### CONVERSIONE DA DIZIONARIO INIZIALE A DIZIONARIO UTILE PER CALCOLO CHARIKAR (dizionario dei nodi) ###
########################################################################################################

def dizionario(li_iniziale):
    flat_list = [item for sublist in li_iniziale for item in
                 sublist]  # Con questo ciclo invece passo da una lista di liste a una lista semplice di elementi in modo da poter applicare charikar

    dic_fin = {}
    deg = {}
    # print (li)
    # print (len(li))
    for elem in flat_list:
        elem = list(elem)  # Trasformo da tupla a lista
        elem[0] = int(elem[0])  # Trasformo da stringa a numeri per comodità
        elem[1] = int(elem[1])
        # print (elem)
        if elem[0] not in dic_fin.keys():
            dic_fin[elem[0]] = []
            deg[elem[0]] = 0
        if elem[1] not in dic_fin[elem[
            0]]:  # In questo modo non lascio che si ripetano più volte gli stessi soggetti all'interno della lista dei valori
            dic_fin[elem[0]].append(elem[1])
            deg[elem[0]] += 1

        if elem[1] not in dic_fin.keys():
            dic_fin[elem[1]] = []
            deg[elem[1]] = 0
        if elem[0] not in dic_fin[elem[
            1]]:  # In questo modo non lascio che si ripetano più volte gli stessi soggetti all'interno della lista dei valori
            dic_fin[elem[1]].append(elem[0])
            deg[elem[1]] += 1
        # break

    return dic_fin, deg  # Riporta il dizionario con chiave un nodo e come valore l'altro nodo a cui si "attacca" (se A è collegato con B, avremo sia {A:B che B:A}


######################
### RIMOZIONE NODO ###
######################


def rimozione(counter, deg, dic):  #
    nodes = []  # Lista che avrà i nodi da rimuovere

    for i in deg.keys():  # Così scorro su tutte le chiavi del dizionario avente come chiave il nodo e come valore il numero di nodi associati

        if (deg[
            i] == counter):  # Scorro tutti i valori del dizionario con la numerosità dei collegamenti e quando sono uguali al valore minimo (counter) messo in imput nella
            # funzione allora svolge le seguenti funzioni
            nodes.append(i)  # Aggiungo alla lista dei nodi da eliminare tutti i nodi con la condizione if

    for k in nodes:  # Scorro tutti i nodi che sono da eliminare
        for j in dic[k]:  # j corrisponde a tutti i nodi nella lista dei valori del dizionario in chiave k
            # Applico un nuovo ciclo per poter eliminare quel nodo non solo come chiave del dizionario ma anche dalla lista dei valori delle altre chiavi e dal
            # dizionario deg che invece conta il totale dei collegamenti. Ad esempio: se A è da eliminare, si elimina {A:[B,C]} ma si deve eliminare anche a da {B:[A,C]}

            (dic[j]).remove(k)  # Con questo comando rimuovo il nodo k da tutte le altre chiavi
            deg[j] = deg[
                         j] - 1  # Con questo comando diminuisco il valore dei collegamenti di 1 da tutte le altre chiavi che hanno un collegamento con k

        del dic[k]  # Elimino la chiave k dal dizionario con la lista di valori
        del deg[k]  # Elimino la chiave k dal dizionario con la somma dei collegamenti

    return dic,deg


################
### CHARIKAR ###
################

def charikar(dic, deg):
    maxdens = 0
    subgraph = []


    while (len(deg) > 0):
        mindeg = float('inf')  # In questo modo imposto il mindeg = infinito per comodità

        for i in deg.keys():
            mindeg = min(deg[i], mindeg)

        rim = rimozione(mindeg, deg, dic)
        dic = rim[0]
        deg = rim[1]

        if averageDens(dic) > maxdens:
            maxdens = averageDens(dic)
            dic_maxdens = copy.deepcopy(dic) # differenza fra copy e copy.deep? https://www.askpython.com/python/dictionary/copy-a-dictionary-in-python#:~:text=Using%20%3D%20operator%20to%20Copy%20a%20Dictionary%20in%20Python&text=And%20directly%20copy%20it%20to,to%20the%20new%20dictionary%2C%20dict2

    #print('Dizionario sottografo denso:', dic_maxdens)

    return maxdens

