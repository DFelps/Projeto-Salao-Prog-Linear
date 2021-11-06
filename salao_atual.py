from random import randrange, uniform, randint
from copy import deepcopy
from math import exp
import numpy as np
import math as matematica

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



#def sol_inicial(n,max):

    # criar lista com os índices de todos os produtos
 #   s_ini = np.zeros(n,int)
  #  resul = 0
   # while resul<max:
    #    ind  = randrange(0,n)
     #   if s_ini[ind]==0:
        #    s_ini[ind] = 1
        #    resul += prod[ind]
    #if resul!=max:
     #  s_ini[ind] = 0

    #return s_ini

# GERA UM CROMOSSOMO
def cromossomo(n, max):
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
        
#ROTINA POP
def pop_inicial(tp, n):
    pop = np.zeros((tp, n), int)
    #aleatorio uniforme
    for i in range (tp):
        pop[i] = cromossomo(n, max)
    return pop
#FIM DA ROTINA

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
# FIM DA ROTINA----------------------------------------------------


# CONFIG AG
TP = 10      # tamanho da população
TC = 0.8     # taxa de cruzamento
TM = 0.1     # taxa de mutação
IG = 0.1     # intervalo de geração
NG = 100     # número de gerações

# CÓDIGO PRINCIPAL
n   = 10       # numero de PRODUTOS
si  = []      # solução inicial
sf   = []      # solução final
prod  = []      # vetor PRODUTOS
max = 100       # capacidade maxima
sv1 = sv2 = 0
te = 1

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


#RESULTADO AG ---------------------------------
sol = ag(n,TP,NG,TC,TM,IG)
print("Raiz encontrada: ",sol)
vl = eq2grau(sol)
