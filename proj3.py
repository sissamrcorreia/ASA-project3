# Importar pulp
from pulp import *

# Leitura dos dados de entrada
nb, np, m = map(int, input().split())
toys = []
packs = []

# Criar o problema
prob = LpProblem("Ma", LpMaximize)

# Criar LpVariable para os brinquedos
for i in range (1, nb + 1):
    l, c = map(int, input().split())
    x = LpVariable("xb" + str(i), 0, c, LpInteger)
    toys.append([l, c, x])

# Cirar LpVariable para os pacotes
for j in range (1, np + 1):
    t1, t2, t3, l = map(int, input().split())
    r = toys[t1 - 1][0] + toys[t2 - 1][0] + toys[t3 - 1][0]
    p = LpVariable("pac" + str(j), 0, m // 3, LpInteger)
    packs.append([t1, t2, t3, l, p,r])
    cur = packs[j -1]
    toy_indices = [cur[0] - 1, cur[1] - 1, cur[2] - 1]
    prob += cur[4] <= lpSum(toys[i][2] for i in toy_indices)

# Função objetivo
prob += lpSum(toys[i - 1][0] * toys[i - 1][2] for i in range(1, nb + 1)) + \
        lpSum((packs[j - 1][3] - packs[j - 1][5]) * packs[j - 1][4] for j in range(1, np + 1))

# Restrição do máximo de produção diária
prob += lpSum(toy[2] for toy in toys) <= m

# Criar um dicionário que mapeia índices de brinquedos para os pacotes associados
toy_to_packs = {}
for j, pack in enumerate(packs):
    for toy_index in pack[: -3]:
        if toy_index not in toy_to_packs:
            toy_to_packs[toy_index] = []
        toy_to_packs[toy_index].append(j)

# Usar o dicionário para criar as restrições
for i in range(1, nb + 1):
    if i in toy_to_packs:
        prob += lpSum(packs[j][4] for j in toy_to_packs[i]) <= toys[i - 1][2]

# Resolver o problema
prob.solve(GLPK(msg=0))

print(int(value(prob.objective)))