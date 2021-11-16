from random import randint, uniform, randrange
from math import ceil
import numpy as np


# CALCULA EQ. 2º GRAU
def eq2grau(x):
    return abs(x*x + 3*x - 4)
# FIM DA ROTINA


# CONVERTE BINÁRIO PARA DECIMAL
def bin_to_dec(p):
    x = 0
    tam = len(p)
    for i in range(1,tam):
        x += p[i]*(2**(len(p)-i-1))

    if p[0]==1:
        x = -x

    return x
# FIM DA ROTINA

"""
# ORDENAÇÃO - MÉTODO DA BOLHA
def sort(p,f):
    for i in range(len(p)-1):
        for j in range(i+1,len(p)):
            if(f[i]<f[j]):
                aux  = f[i]
                f[i] = f[j]
                f[j] = aux

                aux  = p[i]
                p[i] = p[j]
                p[j] = aux
#FIM DA ROTINA


# CALCULA A APTIDÃO
def aptidao(pop,tp):
    f = np.zeros(tp,float)
    soma = 0
    for i in range(tp):
        # converte para DECIMAL
        x = bin_to_dec(pop[i])

        # aplico na eq segundo grau
        res = eq2grau(x)

        if res==0:
            f[i] = 9999
        else:
            f[i] = 1/res   # minimização

        soma += f[i]

    for i in range(tp):
        f[i] = f[i]/soma

    return f
# FIM DA ROTINA

# ROTINA ROLETA
def roleta(f):
    ale = uniform(0,1)
    soma = f[0]
    ind=0
    while soma<ale:
        ind += 1
        soma += f[ind]
    ind -=1
    return ind
#FIM DA ROTINA

# ROTINA TORNEIO
def torneio(f):
    ind1 = randrange(0,TP)
    ind2 = randrange(0,TP)
    if f[ind1]>f[ind2]:
        return ind1
    else:
        return ind2
#FIM DA ROTINA

# ROTINA CRUZAMENTO
def cruzamento(pop,fit,tc,tp):
    desc = []
    qc = ceil(tc*tp)

    tam2 = len(pop[0])
    corte = randrange(tam2)

    for i in range(qc):
        # escolhe pai 1
        p1 = roleta(fit)

        # escolhe pai2
        p2 = roleta(fit)

        #descendente 1
        linha = []
        for j in range(0,corte):
            linha.append(pop[p1][j])
        for j in range(corte,tam2):
            linha.append(pop[p2][j])
        desc.append(linha)

        #descendente 2
        linha = []
        for j in range(0,corte):
            linha.append(pop[p2][j])
        for j in range(corte,tam2):
            linha.append(pop[p1][j])
        desc.append(linha)

    return desc
# FIM DA ROTINA

# ROTINA MUTAÇÃO (TORCA SIMPLES)
def mutacao(pop,desc,tm,tp):

    qm = ceil(tm*tp)

    qt_desc = len(desc)

    for i in range(qm):
        # escolhe descendente
        ind = randrange(qt_desc)

        # escolhe pai
        #ind = randrange(tp)

        aux = []
        aux = desc[ind]
        #aux = pop[ind]

        pos = randrange(len(aux))

        # alterando o valor do bit selecionado
        aux[pos] = 1 - aux[pos]

        desc.append(aux)
# FIM DA ROTINA

# ROTINA NOVA POPULAÇÃO
def nova_pop(pop,desc,ig,tp):

    elite = ceil(ig*tp)
    for i in range(elite,tp):
        pop[i] = desc[i-elite]

"""

# GERA UM CROMOSSOMO
def cromossomo(n):
    ind = np.zeros(n,int)
    for i in range(n):
        # aleatório uniforme
        ind[i] = randint(0,1)

    return ind
# FIM DA ROTINA


# GERA A POPULAÇÃO INICIAL
def pop_inicial(tp,n):
    pop = np.zeros((tp,n),int)

    # aleatorio uniforme
    for i in range(tp):
        pop[i] = cromossomo(n)

    return pop
# FIM DA ROTINA


# ROTINA ALGORITMO GENÉTICO
def ag(n,tp,ng,tc,tm,ig):
    pop   = np.zeros((tp,n),int)
    fit   = np.zeros(tp,float)
    desc  = []
    fit_d = []

    # população inicial
    pop = pop_inicial(tp,n)
    print("*** População Inicial ***")
    for i in range(tp):
        print("Indivíduo ",i+1,":\t",pop[i])

    #seleciona melhor indivíduo como resposta
    x = bin_to_dec(pop[0])

    return x
"""
    #print("\nAptdidao:")
    fit = aptidao(pop,tp)
    #print(fit)

    for t in range(ng):

        # gera descendente por cruzamento
        desc = cruzamento(pop,fit,tc,tp)

        # gera descendente por cruzamento
        mutacao(pop,desc,tm,tp)

        #print("Descendentes")
        #print(desc)

        # avalia descendentes
        fit_d = aptidao(desc,len(desc))
        #print("\nAptdidao dos descendentes:")
        #print(fit_d)

        # colocar os descendentes e pop. atual
        # em ordem descrescente
        sort(pop,fit)
        sort(desc,fit_d)

        #gerar a nova população
        nova_pop(pop,desc,ig,tp)

        # calcula aptidão da população atual
        fit = aptidao(pop,tp)

    # colocar pop. atual em ordem descrescente
    sort(pop,fit)
  
    #seleciona melhor indivíduo como resposta
    x = bin_to_dec(pop[0])

    return x
"""
# MÓDULO PRINCIPAL

# CONFIGURAÇÃO

N  =  8      # tamanho de um indivíduo
TP = 10      # tamanho da população
TC = 0.8     # taxa de cruzamento
TM = 0.1     # taxa de mutação
IG = 0.1     # intervalo de geração
NG = 100     # número de gerações

sol = ag(N,TP,NG,TC,TM,IG)
print("Raiz encontrada: ",sol)
vl = eq2grau(sol)
