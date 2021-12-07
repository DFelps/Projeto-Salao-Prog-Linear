from random import randrange, uniform
from math import ceil
import numpy as np

#ROTINA ALGORITMO GENETICO -----------------------------------------------
# função para gerar pesos dos 

# ROTINA AVALIA
def avalia(sf,n,prod):
    
    resul = 0
    for i in range(0,n):
        resul += prod[i]*sf[i]*1

    return resul
# FIM DA ROTINA

def Gerar_Pesos(n):
    
    pe = np.zeros(n,int)
    for i in range(n):
        pe[i] = uniform(5,20)
    return pe
    

# método de ordenação (BUBBLE SORT)
def Sort(p,f,qp):
    for i in range(qp-1):
        for j in range(qp):
            if f[i]>f[j]:
                aux_f = f[i]
                f[i]  = f[j]
                f[j]  = aux_f

                aux_p = p[i]
                p[i]  = p[j]
                p[j]  = aux_p
    return p, f
# Correção dos individuos
def Restricao(n,desc,qd,pe,max):

    for i in range(qd):
        while avalia(desc[i],n,pe)>max:
            while True:
                j = randrange(0,n)
                if desc[i][j]==1:
                    break
            desc[i][j] = 0

    return desc

# função para gerar população inicial
def Cromossomo(n,max,pe):
    cr = np.zeros(n,int)
    pm = 0
    while pm<max:
        ind = randrange(0,n)
        if cr[ind] == 0:
            cr[ind] = 1
        pm += pe[ind]

    cr[ind] = 0

    return cr

# Roleta
def Roleta(tp,fit):
    soma = 0
    p= 0
    ale = randrange(0,1)
    while(soma<ale):
        p += 1
        soma += fit[p]
    return p

# função para gerar população inicial
def PopIni(n,max,pe,tp):
    pop = np.zeros((tp,n),int)

    for i in range(tp):
        pop[i] = Cromossomo(n,max,pe)

    return pop
# fim da função para gerar população inicial

# função para calcular a fitness da população
def Aptidao(n,tp,pop,pe):
    
    f = np.zeros(tp,float)

    soma = 0
    for i in range(tp):
        vl = avalia(pop[i],n,pe)
        f[i] = vl
        soma += f[i]
    
    for i in range(tp):
        f[i] /= soma
    
    return f
# fim da função para calcular a fitness

# função para execução do operador de cruzamento
def Crossover(n,pop,fit,tp,tc):

    qc = ceil(tc*tp)
    corte = randrange(0,n)

    desc = []
    for i in range(qc):
        # pai 1
        pai1 = Roleta(tp,fit)

        # pai 2
        pai2 = Roleta(tp,fit)

        # primeiro descendente
        aux = []
        for j in range(0,corte):
            aux.append(pop[pai1][j])
        for j in range(corte,n):
            aux.append(pop[pai2][j])
        desc.append(aux)

        # segundo descendente
        aux = []
        for j in range(0,corte):
            aux.append(pop[pai2][j])
        for j in range(corte,n):
            aux.append(pop[pai1][j])
        desc.append(aux)

    return desc
# fim da função para execução do operador de cruzamento

# função para execução do operador de mutação
def Mutacao(n,desc,tp,tm):
    qm = ceil(tp*tm)
    qd = len(desc)

    for i in range(qm):
        j = randrange(0,qd)
        aux = desc[j]
        p1 = randrange(0,n)

        aux[p1] = 1 - aux[p1]

        desc.append(aux)

    return desc
# fim da função para execução do operador de mutação

# função para gerar a nova população
def NovaPop(pop,desc,fit,fit_d,tp,ig):
    elite = ceil(tp*ig)

    j= 0
    for i in range(elite,tp):
        pop[i] = desc[j]
        j += 1

    return pop
# fim da função para gerar a nova população

# rotina AG
def AlgGen(n,pe,c_max,tp,ng,tc,tm,ig):
    # Gera população inicial
    
    pop = PopIni(n,c_max,pe,tp)

    # calcula fitness da população
    fit = Aptidao(n,tp,pop,pe)

    # iteração para evolução das gerações
    for g in range(ng):
        # aplica cruzamento
        desc = Crossover(n,pop,fit,tp,tc)

        # aplica mutação
        desc = Mutacao(n,desc,tp,tm)

        # correção dos indíviduos para restrição
        # do problema
        desc = Restricao(n,desc,len(desc),pe,c_max)

        # calcula fitness de descendentes
        fit_d = Aptidao(n,len(desc),desc,pe)
    
        # ordena população atual
        pop, fit = Sort(pop,fit,tp)

        # ordena descendentes
        desc, fitd_d = Sort(desc,fit_d,len(desc))

        # gera nova população
        pop = NovaPop(pop,desc,fit,fit_d,tp,ig)

        # calcula fitness de população
        fit = Aptidao(n,tp,pop,pe)

    # ordena população atual
    Sort(pop,fit,tp)
    return pop[0]

# CONFIG AG
TP = [10,50,100]      # tamanho da população
TC = [0.8, 0.9]     # taxa de cruzamento
TM = [0.1, 0.2]     # taxa de mutação
IG = [0.1, 0.2]     # intervalo de geração
NG = [10, 50, 100]    # número de gerações


# CÓDIGO PRINCIPAL
N   = 10       # numero de PRODUTOS
si  = []      # solução inicial
sf   = []      # solução final
prod  = []      # vetor PRODUTOS
max = 100       # capacidade maxima
sv1 = sv2 = 0
te = 1
fit = 0
pe=0

# matriz de adjacências do grafo
peso = Gerar_Pesos(N)
for i_tp in range(len(TP)):
     for i_ng in range(len(NG)):
         for i_tc in range(len(TC)):
             for i_tm in range(len(TM)):
                 for i_ig in range(len(IG)):
                     sol = AlgGen(N,peso,max,TP[i_tp],
                                  NG[i_ng],TC[i_tc],TM[i_tm],
                                  IG[i_ig])
                     print("AG.: ",TP[i_tp],NG[i_ng],TC[i_tc],
                                   TM[i_tm],IG[i_ig],sol,
                                   avalia(sol,N,peso))

"""
sol = AlgGen(N,peso,max,TP, NG,TC,TM,IG)
print("AG.: ", sol, avalia(sol,N,peso))
"""