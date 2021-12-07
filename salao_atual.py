from random import randrange, uniform
from copy import deepcopy
from math import exp
import numpy as np
from math import ceil
from numpy.core.numeric import correlate

from numpy.lib.shape_base import vsplit

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





#ROTINA ALGORITMO GENETICO -----------------------------------------------
# função para gerar pesos dos itens
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
                j = uniform(0,n)
                if desc[i][j]==1:
                    break
            desc[i][j] = 0

    return desc

# função para gerar população inicial
def Cromossomo(n,max,pe):
    cr = np.zeros(n,int)
    pm = 0
    while pm<max:
        ind = uniform(0,n)
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
        vl = avalia(pop[i],tp,pe)
        f[i] = vl
        soma += f[i]
    
    for i in range(TP):
        f[i] /= soma
    
    return f
# fim da função para calcular a fitness

# função para execução do operador de cruzamento
def Crossover(n,pop,fit,tp,tc):

    qc = exp.ceil(tc*tp)
    corte = uniform(0,n)

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
    qm = exp.ceil(tp*tm)
    qd = len(desc)

    for i in range(qm):
        j = uniform(0,qd)
        aux = desc[j]
        p1 = uniform(0,n)

        aux[p1] = 1 - aux[p1]

        desc.append(aux)

    return desc
# fim da função para execução do operador de mutação

# função para gerar a nova população
def NovaPop(pop,desc,fit,fit_d,tp,ig):
    elite = exp.ceil(tp*ig)

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
TP = 10      # tamanho da população
TC = 0.8     # taxa de cruzamento
TM = 0.1     # taxa de mutação
IG = 0.1     # intervalo de geração
NG = 1    # número de gerações


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

prod = vetor_peso(N,5)
print("***** CONFIGURAÇÕES ******")
print("Total de itens: ",N)
print("Preco dos",N,"itens: ",prod)
print("Valor maximo permitido: ",max)
si = sol_inicial(N,max)
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

pg = Gerar_Pesos(N)
print("\nPesos Gerados.........: ",pg)