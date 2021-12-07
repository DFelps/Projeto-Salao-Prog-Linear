from random import randint, randrange, uniform
from math import ceil
from classes import Pilha

def precosAle(N):
    x = list(range(N))
    for i in x:
        x[i] = float(randrange(99, 999)) / 100
    return x


def valor(x, precos):
    tot = int(0)
    i = int(0)

    while (i < len(precos)):
        tot = (x[i] * precos[i]) + tot

        i += 1

    return round(tot, 2)


def solucaoInicial(max, precos, N):
    tot = int(0)
    pilha = Pilha()

    lista = list(range(N))
    for i in lista:
        lista[i] = int(0)
    while tot <= max:
        temp = randint(0, N - 1)
        if tot + precos[temp] <= max:
            pilha.Push(temp)
            tot += precos[temp]
        else:
            break

    for i in range(0, pilha.Size()):
        temp = pilha.Pop()
        lista[temp] += 1

    return lista


def populacaoInicial(max, precos, tp, N):
    pop = []

    for i in range(tp):
        pop.append(solucaoInicial(max, precos, N))
    return pop


def aptidao(max, precos, pop, tp):
    f = []
    soma = 0

    for i in range(tp):
        res = valor(pop[i], precos)
        if res == max:
            f.append(99999999)
        else:
            f.append(res)
        soma += f[i]

    for i in range(tp):
        f[i] = f[i] / soma
    return f

def somaAptidao(x, tp):
    a = 0
    for i in range(tp):
        a = a + x[i]
    return a


def roleta(f):
    ale = uniform(0, 1)
    soma = f[0]
    p = 0
    while soma < ale:
        p += 1
        soma += f[p]
    return p


def cruzamento(pop, f, TC):
    desc = []
    tam1 = len(pop)
    qc = ceil(TC * tam1)

    tam2 = len(pop[0])
    corte = randrange(tam2)

    for i in range(qc):
        p1 = roleta(f)
        p2 = roleta(f)

        linha = []
        for j in range(0, corte):
            linha.append(pop[p1][j])
        for j in range(corte, tam2):
            linha.append(pop[p2][j])
        desc.append(linha)

        linha = []
        for j in range(0, corte):
            linha.append(pop[p2][j])
        for j in range(corte, tam2):
            linha.append(pop[p1][j])
        desc.append(linha)

    return desc


def aptidaoDesc(max, precos, desc, N):
    for i in range(len(desc)): # 10 descendentes
        x = desc[i] # x = desc[0] | x = [2,0,2] |
        if valor(x, precos) > max:
            y = checar(max, x, precos, N)
            desc[i] = y
    return desc


def checar(max, x, precos, N):
    v = valor(x, precos) # v = 16
    while v > max: #
        rand = randint(0, N-1) # rand = 2
        if x[rand] > 0:
            x[rand] -= 1 # x[rand] | x = [2,0,2] | x = 2 - 1 | x = [2,0,1]
        v = valor(x, precos) # v = 10
    return x

def mutacao(pop, desc, tm, precos):
    tam1 = len(pop) # 10
    qm = ceil(tm * tam1) # qm = TM * tam1 | qm = 0.1 * 10 | qm = 1
    tam2 = len(desc) # tam2 = 10

    for i in range(qm):
        ind = randrange(tam2) # ind = 0, 9 | randrange(10) | randrange 0,9 | ind = 0
        aux = desc[ind] # aux = desc[ind] | desc[0] | aux = [2,0,1]
        y = randrange(len(desc[ind])) # y = randrange(len(desc[ind])) | len(desc[0]) = 3 | 0, 2 | randrange(3) | 0, 1, 2 | y = 1
        while True:
            if aux[y] != 0 or valor(aux, precos) == 0:
                break
            y = randrange(len(desc[ind])) # y = 2
        if aux[y] > 0:
            if randint(0, 1) == 0: # randint = 1
                aux[y] -= 1
            else:
                aux[y] += 1

        desc[ind] = aux
        # desc.append(aux)
    return desc


def sort(p, f):
    for i in range(len(p) - 1):
        for j in range(i + 1, len(p)):
            if (f[i] < f[j]):
                aux = f[i]
                f[i] = f[j]
                f[j] = aux

                aux = p[i]
                p[i] = p[j]
                p[j] = aux


def novaPop(pop, desc, ig):
    tam = len(pop) # tam = 10 | pop = [[2,0,1],[1,0,0],[1,0,1],...,[1,0,1]]
    elite = ceil(ig * tam) # elite = 0.1 * 10 | elite = 6
    for i in range(elite, tam): # 1, 10
        pop[i] = desc[i - elite] # pop[6] = desc[6 - 6] | pop[0]


def algoritmoGenetico(N, V, P, TP, NG, IG, TC, TM):
    max = V
    precos = P
    pop = []
    fit = []
    desc = []
    fit_d = []

    pop = populacaoInicial(max, precos, TP, N)
    fit = aptidao(max, precos, pop, TP)

    for t in range(NG):
        # Gerar descendente
        desc = cruzamento(pop, fit, TC)

        # Gerar mutacao em descendentes
        desc = mutacao(pop, desc, TM, precos)
        desc = aptidaoDesc(max, precos, desc, N)

        # Avaliar descendentes
        fit_d = aptidao(max, precos, desc, len(desc))

        # Colocar os descendentes e pop. atual em ordem decrescente
        sort(pop, fit)
        sort(desc, fit_d)

        # Gera nova população
        novaPop(pop, desc, IG)

        # Calcula aptidão da população atual
        fit = aptidao(max, precos, pop, TP)

    # Colocar pop. atual em ordem decrescente
    sort(pop, fit)
    # Seleciona o melhor indivíduo como resposta
    x = pop[0]

    return x, valor(x, precos)


if __name__ == '__main__':
    # Variáveis do problema mochila
    N = 10 # - Quantidade de produtos
    V = 100  # - Valor máximo a ser gasto
    P = precosAle(N)  # - Valor de cada produto

    # Variáveis do algortimo genético
    TP = [10, 50, 100]  # - Tamanho da população
    NG = [50, 100, 200]  # - Número de gerações
    TC = [0.5, 0.8]  # - Taxa de cruzamento
    IG = [0, 0.1, 0.6]  # - Intervalo de gerações
    TM = [0, 0.1, 0.4]  # - Taxa de mutação

    for a in range(len(TP)):
        for b in range(len(NG)):
            for c in range(len(TC)):
                for d in range(len(TM)):
                    for e in range(len(IG)):
                        x, v = algoritmoGenetico(N, V, P, TP[a], NG[b], IG[e], TC[c], TM[d])
                        print("Estou usando a combinação de TP = ",TP[a]," NG = ",NG[b], " IG = ",IG[e]," TC = ",TC[c]," e TM = ",TM[d])
                        print("A melhor combinação é: ", x, "\nGastando o total de: ", v)

    print(P, "- Precos")