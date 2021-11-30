from random import randrange, uniform, randint
from copy import deepcopy
from math import exp
import numpy as np
from backpacks import generate_backpack
from items import generating_list_item, get_lighter_item
from math import ceil

# ROTINA PARA GERAR VETOR
def vetor_peso(n,c):

    vet = []
        
    for i in range(n):
        vet.append(randrange(c,c+15))

    return vet
# FIM DA ROTINA


# ROTINA PARA GERAR SOLUÇÃO INICIAL
def sol_inicial(n,max):

    # criar lista com os índices de todos os produtos
    s_ini = np.zeros(n,int)
    resul = 0
    while resul<max:
        ind  = randrange(0,n)
        if s_ini[ind]==0:
            s_ini[ind] = 1
            resul += prod[ind]
    if resul!=max:
       s_ini[ind] = 0

    return s_ini
# FIM DA ROTINA

# ROTINA AVALIA
def avalia(sf,prod):
    
    resul = 0
    for i in range(0,len(sf)):
        resul += prod[i]*sf[i]*1

    return resul
# FIM DA ROTINA

# ROTINA SUCESSORES - SUBIDA
def sucessor(atual,prod):
      
    melhor = deepcopy(atual)   
    vm = avalia(melhor,prod)

    # item dentro da mochila aleatoriamente
    while True:
        c = randrange(0,len(atual))
        if atual[c]==1:
            break

    aux = deepcopy(atual)
    aux[c] = 0
    for i in range(len(aux)):
        if aux[i]==0 and i!=c:
            aux[i] = 1
            vaux = avalia(aux,prod)
            if vaux>vm and vaux<=max:
                vm = vaux
                melhor = deepcopy(aux)
            aux[i] = 0

    return melhor
# FIM DA ROTINA

# ROTINA SUCESSORES - TEMPERA
def sucessor_temp(atual):

    c1 = randrange(0,len(atual))
    c2 = randrange(0,len(atual))

    aux = deepcopy(atual)
    # troca de posição para gerar sucessor
    x       = aux[c1]
    aux[c1] = aux[c2]
    aux[c2] = x

    return aux
# FIM DA ROTINA

# ROTINA SUBIDA DE ENCOSTA
def subida_encosta(s_ini,prod):
    
    atual = deepcopy(s_ini)
    va = avalia(atual,prod)
    
    while True:
        prox = sucessor(atual,prod)
        vp = avalia(prox,prod)
        if vp<=va:
            break
        else:
            atual = prox
            va = vp
    return atual, va
# FIM DA ROTINA

# ROTINA SUBIDA DE ENCOSTA ALTERADA
def subida_alterada(s_ini,prod):
    
    t = 0
    TMAX = len(s_ini)-1
    atual = deepcopy(s_ini)
    va = avalia(atual,prod)
    
    while True:
        prox = sucessor(atual,prod)
        vp = avalia(prox,prod)
        if vp<=va:
            if t<=TMAX:
                t += 1
            else:
                break
        else:
            atual = prox
            va = vp
            t = 0
    return atual, va
# FIM DA ROTINA

# ROTINA TEMPERA SIMULADA
def tempera(s_ini,t_ini,t_fim):
    
    atual = deepcopy(s_ini)
    va = avalia(atual,prod)
    temp = t_ini
    fr = 0.9

    while temp>t_fim:
        prox = sucessor_temp(atual)
        vp = avalia(prox,prod)
        de = vp - va
        if de<0:
            atual = prox
            va = vp
        else:
            ale = uniform(0,1)
            aux = exp(-de/temp)
            if(ale<aux):
                atual = prox
                va = vp
        temp = temp * fr

    return atual, va
# FIM DA ROTINA

# CALCULA A APTIDÃO
def aptidao(pop,tp,prod):
    f = np.zeros(tp,int)
    soma = 0
    for i in range(tp):
        f[i] = avalia(pop[i], prod)   # minimização

        soma += f[i]
    for i in range(tp):
        f[i] = f[i]/soma
    return f
# FIM DA ROTINA

# CONFIG AG
TP = 10      # tamanho da população
TC = 0.8     # taxa de cruzamento
TM = 0.1     # taxa de mutação
IG = 0.1     # intervalo de geração
NG = 100     # número de gerações
POP = []

# CÓDIGO PRINCIPAL
n   = 10       # numero de PRODUTOS
si  = []      # solução inicial
sf   = []      # solução final
prod  = []      # vetor PRODUTOS
max = 100       # capacidade maxima
sv1 = sv2 = 0
te = 1
fit = 0

prod = vetor_peso(n,5)
print("***** CONFIGURAÇÕES ******")
print("Total de itens: ",n)
print("Preco dos",n,"itens: ",prod)
print("Valor maximo permitido: ",max)
si = sol_inicial(n,max)
vi = avalia(si,prod)
print("\nSolução inicial.........: ",si," Custo: ",vi)

sf,v1 = subida_encosta(si,prod)
print("Subida de Encosta.......: ",sf," Custo: ",v1,"Ganho.....: {:.2f}".format(100*(float(v1-vi))/vi),"%")


# 3 TENTATIVAS
sf,v2 = subida_alterada(si,prod)
print("Subida Enc. Alterada (1): ",sf," Custo: ",v2,"Ganho.....: {:.2f}".format(100*(float(v2-vi))/vi),"%")

sf,v2 = subida_alterada(si,prod)
print("Subida Enc. Alterada (2): ",sf," Custo: ",v2,"Ganho.....: {:.2f}".format(100*(float(v2-vi))/vi),"%")

sf,v2 = subida_alterada(si,prod)
print("Subida Enc. Alterada (3): ",sf," Custo: ",v2,"Ganho.....: {:.2f}".format(100*(float(v2-vi))/vi),"%")


# 3 TENTATIVAS
t_ini = 900
t_fim = 0.1
sf,v1 = tempera(si,t_ini,t_fim)
print("Tempera Simulada (1)....: ",sf," Custo: ",v1,"Ganho.....: {:.2f}".format(100*(float(v1-vi))/vi),"%")


t_ini = 600
t_fim = 0.8
sf,v1 = tempera(si,t_ini,t_fim)
print("Tempera Simulada (2)....: ",sf," Custo: ",v1,"Ganho.....: {:.2f}".format(100*(float(v1-vi))/vi),"%")

t_ini = 900
t_fim = 0.09
sf,v1 = tempera(si,t_ini,t_fim)
print("Tempera Simulada (3)....: ",sf," Custo: ",v1,"Ganho.....: {:.2f}".format(100*(float(v1-vi))/vi),"%")
# FIM CÓDIGO PRINCIPAL



#ROTINA ALGORITMO GENETICO -----------------------------------------------


def get_random_item(list_items):
    position_item = randint(0, len(list_items) - 1)

    return position_item

def insert_item_in_backpack(backpack, list_items):

    position_item = get_random_item(list_items)

    if backpack["available_weight"] >= list_items[position_item]:
        
        backpack["available_weight"] -= list_items[position_item]
        backpack["list_items"][position_item] = 1
    
    return backpack


def initial_solution(backpack, list_items, minimum_value):
    
    while backpack["available_weight"] > minimum_value:
        insert_item_in_backpack(backpack, list_items)
    
    return backpack


def initial_population(population, population_size, backpack, list_items, lighter_item):
    
    for t in range(population_size):
        individual = (initial_solution(deepcopy(backpack), list_items, lighter_item))
        population.append(individual)
        print(population[t])
    

    return population 



def evaluate(backpack,list_items):
    value = 0

    for i in range(len(backpack["list_items"])):
        if backpack["list_items"][i] == 1:
            value += list_items[i]
    
    return value


def fi_population(population):
    fi = []

    for value in population:
        if value["available_weight"] == 0 :
            fi.append(9999)

        else:
            fi.append(1/value["available_weight"])
    
    return fi

def fit_population(fi):
    fits = []
    soma = sum(fi)
    
    for values_fi in fi:
               
        fits.append(values_fi/soma)
        
    print("Fit população: ",sum(fits))

    return fits


def select_parents(fits):
    
    parents = []

    while len(parents) < 2:
        ale = uniform(0,1)
        soma = 0
        for i in range(0, len(fits)):
            
            if soma > ale :
                soma+=fits[i]

            parents.append(i-1)
    
    return parents

def reproduction(population, fits, crossing_rate, size_population, max, backpack_aux):

    list_descendants = []

    cutoff = randrange(1,max)
    #print("cutoff: ",cutoff)
    number_of_intersections = ceil(size_population * crossing_rate)

    for i in range(2*number_of_intersections):
        linha=[]

        for j in range (max):
            linha.append(0)
        
        list_descendants.append(linha)
    k=0

    for i in range(number_of_intersections):
        p = select_parents(fits)

        s1 = population[p[0]]['list_items']
        s2 = population[p[1]]['list_items']

        for j in range(cutoff-1):

            list_descendants[k][j]   = s1[j]
            list_descendants[k+1][j] = s2[j]

        for j in range (cutoff, max):
            list_descendants[k][j]   = s2[j]
            list_descendants[k+1][j] = s1[j]

        k+=2
    
    #print("Quantidade de filho2: ", len(list_descendants[1]))
    print("Filhos: ", list_descendants)

    #Seleciona um dos 4 filhos aleatóriamente
    filhoSelecionado = randint(0,3)
    print("Filho selecionado: ",filhoSelecionado+1)
    #Seleciona um dos 10 elementos dentro do filho
    eleSelecionado = randint(0,9)
    print("Cromossomo dentro do filho selecionado: ",eleSelecionado+1)

    novoFilho = list_descendants[filhoSelecionado]

    if (list_descendants[filhoSelecionado][eleSelecionado] == 0):
        list_descendants[filhoSelecionado][eleSelecionado] = 1
    else:
        list_descendants[filhoSelecionado][eleSelecionado] = 0

    print("Filho após a mutação: ", novoFilho)

    return list_descendants


def new_population(list_descendants):
    
    population_new = []
    values = []
    #print("tamanho de descendants:", len(list_descendants))
    for pop in list_descendants:
        values.append(pop)
    
    #print("tamanho de values: ", len(values))

    '''for i in range(10):
        population_new.append(list_descendants[values.index(min(values))])          
        del(list_descendants[values.index(min(values))])
        del(values[values.index(min(values))])'''

    #print("tamanho de descendants após for:", len(list_descendants))
    #print("tamanho de values após for: ", len(values))

    return population_new

# Setup

backpack_aux = generate_backpack(10,1000)
backpack = generate_backpack(10,1000)
list_items = generating_list_item(10,1000)
lighter_item = get_lighter_item(list_items)

# Parametros Genéticos

population_size = 10
crossing_rate = 0.2
generation_interval = 0.1
number_of_generations = 1

def genetic_algorithm(population_size, crossing_rate, generation_interval, number_of_generations):

    population = []   

    initial_population(population, population_size, backpack, list_items, lighter_item)

    #print (population[0])

    for t in range(number_of_generations):
        
        fi = fi_population(population)
        fit_p = fit_population(fi)
        #parents = select_parents(fit_p)
        descendent = reproduction(population, fit_p, crossing_rate, population_size, 10,backpack_aux)
        population_new = new_population(descendent)

        #print("Nova População: ", descendent)
        #print("descenden: ",descendent)
        #population_new = 0
    print("Nova População: ",descendent)  
    print("tamanho da nova pop: ",len(descendent)) 
    return descendent


solution = genetic_algorithm(population_size,
                             crossing_rate,
                             generation_interval,
                             number_of_generations)

# FIM DA ROTINA----------------------------------------------------