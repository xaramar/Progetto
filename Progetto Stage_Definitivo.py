import random # Permette di generare numeri in modo randomico
import os.path
import utils
import Charikar_finale as ch
import operator
from random import choices
import time

#############################
### IMPOSTAGIONI GENERALI ###
#############################

popolazione = 100 # n. DELLA POPOLAZIONE
generazioni = 10 # n. DELLE GENERAZIONI
n_inter = 5 # n. INTERVALLI INTERNI AL CROMOSOMA
file = 'students'


#########################
### IMPORTAZIONE FILE ###
#########################
data = file+'.txt'


######################
### SCRITTURA FILE ###
######################
file_risultati = 'risultati_'+file+'_pop'+str(popolazione)+'_gen'+str(generazioni)+'_n_inter'+str(n_inter)+'.txt'



#dataset = 'students'
#filename = os.path.join('data', dataset+'.txt')
TS = utils.readdata_dict(data, unix = False)
#print(TS)











##################################################################################################
########################################                  ########################################
########################################     FUNZIONI     ########################################
########################################                  ########################################
##################################################################################################


#####################################
### GENERARE POPOLAZIONE INIZIALE ###
#####################################

####### Creazione cromosoma che partiziona il dominio T in k intervalli casuali

def cromo_casuale():
    global n_inter, TS
    tot = len(TS)
    cut = random.sample(range(1,tot-1), n_inter-1) # Imposto tot-1 in modo che non si possa creare un intervallo sopra l'intervallo finale
    cut.append(0)
    cut.sort()

    return cut



####### Creazione cromosoma che partiziona il dominio T in k intervalli casuali

def cromo_ipercube():
    global n_inter, TS
    tot = len(TS)
    div = round(tot / (n_inter - 1))
    cut = [0]
    start = 0
    stop = div
    for elem in range(0, n_inter - 1):
        gene = random.sample(range(start + 1, stop),1)  # Imposto tot-1 in modo che non si possa creare un intervallo sopra l'intervallo finale
        cut.append(gene[0])
        start += div
        stop += div
        if elem == n_inter - 3:
            stop = tot  # sarebbe len(TS)
    return cut


####### Creazione popolazione iniziale #@#@#@#@ Si può aggiustare togliendolo

def pop_iniziale(h_random,h_iper):
    global TS
    pop = []
    for elem in range(0,h_iper):
        cromo = cromo_ipercube()
        pop.append(cromo)
    for elem in range(0,h_random):
        cromo = cromo_casuale()
        pop.append(cromo)

    return pop



#################
### CROSSOVER ###
#################

def crossover(ind1,ind2):
    tot = len(ind1) # In questo modo ottengo la lunghezza degli individui per poter estrarre casualmente un punto di taglio
    split = random.randint(2,tot-1) # Ho posto di estrarre un numero random da 2 a tot-1 in modo che i due individui si scambino almeno qualche gene.
    #print (split)
    ind1_new = ind1[:split] + ind2[split:]
    ind2_new = ind2[:split] + ind1[split:]
    ind1_new = sorted(ind1_new)
    ind2_new = sorted(ind2_new)

    return [ind1_new,ind2_new]



#################
### MUTAZIONE ###
#################

def mutazione(ind,prob):
    global TS
    l = len(ind)
    for elem in range (1, l):
        #print(elem)
        if random.random() < prob:
            if elem < l-1:
                ind[elem] = random.randint(int(ind[elem-1]+1),int(ind[elem+1]-1))
            else:
                ind[elem] = random.randint(int(ind[elem - 1] + 1), int(len(TS)))

    return ind



################################
### PARTIZIONE PER CROMOSOMA ###
################################

# Questa funzione serve per partizionare il dataset in base all'intervallo di tempo del cromosoma

def partizione(TS,cromo):
    valori = list(TS.values())
    stop = len(TS)
    TS_cromo = []
    for elem in range(0,n_inter):  # In questo ciclo vado a creare una lista di liste con gli istanti temporali divisi nei miei punti di taglio
        if elem == n_inter-1:
            TS_cromo.append(valori[cromo[elem]:stop])
        else:
            TS_cromo.append(valori[cromo[elem]:cromo[elem + 1]])
    #print ('cazzu cazzu',TS_cromo)
    return TS_cromo # In questo modo ottengo TS diviso per i vari timestamp



#########################################
### VALORE DI FITNESS DI UN CROMOSOMA ###
#########################################

def val_fitness(TS_cromo): #TS_cromo è la lista delle coppie di nodi collegati da un arco divisi per i timestamp ottenuta dalla funzione partizione
    li_dens = []
    dens = 0
    for elem in range (0,n_inter):
        gene = ch.dizionario(TS_cromo[elem])
        dens_gene = ch.charikar(gene[0],gene[1])
        li_dens.append(dens_gene)
        dens += dens_gene
    #print('cazzu cazzu', dens)
    return dens
    # return li_dens # Questo nel caso si volesse il vettore delle densità da sommare in seguito



#########################
### ELITIST SELECTION ###
#########################

def elitist(pop,diz_fitness):
    n_elit = round(len(pop)/3)
    sortedDict = sorted(diz_fitness.items(), key=operator.itemgetter(1), reverse=True) # Ordino il dizionario dal valore più grande al più piccolo
    elite = sortedDict[0:n_elit]
    pop_elite = []
    for elem in elite:
        pop_elite.append(pop[elem[0]])
    return pop_elite

# exampleDict.items restituisce la coppia di elementi chiave del dizionario. key=operator.itemgetter(1) specifica che la chiave di confronto è il valore del dizionario,
# mentre operator.itemgetter(0) ha la chiave di confronto della chiave del dizionario.



#####################
### ACCOPPIAMENTO ###
#####################

def accoppiamento(pop,diz_dens):
    population = list(diz_dens.keys())
    weights = list(diz_dens.values())
    gen1 = choices(population, weights)
    #print ('GENITORE 1',gen1[0])
    gen1 = pop[gen1[0]]

    j = True
    while j == True:  # Condizione per evitare di selezionare lo stesso gene sia come genitore 1 che come genitore 2
        gen2 = choices(population, weights)

        if gen2 != gen1:
            j = False
    gen2 = pop[gen2[0]]
    return gen1,gen2



############################################################################################################
########################################                            ########################################
########################################     ALGORITMO GENETICO     ########################################
########################################                            ########################################
############################################################################################################
print ('Inizio algoritmo')

pop = pop_iniziale(popolazione,0) # DEFINISCO LA POPOLAZIONE COME LA VOGLIO - Primo valore per numerosità popolazione formata in modo del tutto casuale;
# secondo valore per numerosità popolazione formata con ipercube
start = time.time()
print ('popolazione iniziale',pop)
i=0

while i < generazioni:

    #@@@@@# print('popolazione di partenza', pop)
    #@@@@@# print('generazione', i+1)

    sum_fitness = 0 # Somma di tutte le densità necessario per il crossover con selezione a roulette
    diz_fitness = {} # Associo a ogni cromosoma la sua densità necessario per l'elitist selection
    diz_dens = {} # Dizionario per la selezione a roulette dei genitori
    for elem in range(0,len(pop)):
        dens = val_fitness(partizione(TS, pop[elem]))
        diz_fitness[elem] = dens
        sum_fitness += dens

    for elem in range(0,len(pop)):
        dens = val_fitness(partizione(TS, pop[elem]))/sum_fitness
        diz_dens[elem] = dens

    ### Elitist Selection
    new_pop = elitist(pop,diz_fitness)

    #@@@@@# print('new_pop con solo elitist',new_pop)

    #@@@@@# print('dizionario delle densità per vedere le probabilità di accoppiarsi',diz_dens)


    pop2 = []
    ### Crossover
    for elem in range(0,round(len(pop)/2)):
        j = True
        while j == True: #condizione per evitare che si creino cromosomi uguali - evita la convergenza @@@@@@@@@@@@@@@@@@@@
            genitori = accoppiamento(pop,diz_dens)
            figli = crossover(genitori[0],genitori[1])
            if figli[0] not in pop2:
                if figli[1] not in pop2:
                    j = False

        pop2.append(figli[0])
        pop2.append(figli[1])

    #@@@@@# print('pop2 con crossover',pop2)

    ### Mutazione
    for elem in range(0,len(pop2)):
        j = True
        while j == True:
            mut = mutazione(pop2[elem],1/len(pop))
            #print(mut)
            if mut != pop2[elem]:
                if mut not in pop2:
                    j = False
            else:
                j = False
        pop2[elem] = mut

    #@@@@@# print('pop2 con mutazione',pop2)

    for elem in pop2:
        new_pop.append(elem)
    new_pop = new_pop[:len(pop)] #elimino l'eccesso di cromosomi visto che prima avevo fatto la elitist selection
    #print(len(pop))

    #@@@@@# print('nuova new_pop',new_pop)

    pop = new_pop

    diz_fitness_finale = {} # Associo a ogni cromosoma la sua densità necessario per l'elitist selection
    for elem in range(0, len(pop)):
        dens = val_fitness(partizione(TS, pop[elem]))
        diz_fitness_finale[elem] = dens
    #@@@@@# print('diz_fitness_finale',diz_fitness_finale)
    ordinaz = sorted(diz_fitness_finale.items(), key=operator.itemgetter(0), reverse=False) # Ordino il dizionario dal valore più grande al più piccolo
    densest = (pop[ordinaz[0][0]],ordinaz[0][1])
    #@@@@@# print('densest subgraph', densest, '\n\n' )

    f = open(file_risultati, 'a')
    f.write(str(densest))
    f.write('\n')
    f.close()

    i += 1


print('densest subgraph', densest)

end = time.time()
tempo = end - start
#@@@@@# print('Tempo impiegato',tempo)

f = open(file_risultati,'a')
f.write('TIME')
f.write(str(tempo))
f.write('\n')
f.close()