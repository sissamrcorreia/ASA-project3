from pulp import *

LpSolverDefault.msg = 0

def calcular_lucro_maximo(n_brinquedos, n_pacotes, max_producao, dados_brinquedos, producao_pacotes):
    prob = LpProblem("MaximizarLucroBrinquedosIndividuais", LpMaximize)

    xbrinquedos = LpVariable.dicts("Brinquedo", range(1, n_brinquedos + 1), lowBound=0, upBound=max_producao, cat=LpInteger)
    pacotes = LpVariable.dicts("Pacote", range(1, n_pacotes + 1), lowBound=0, upBound=max_producao // 3, cat=LpContinuous)

    # Combine objective function parts
    prob += lpSum(dados_brinquedos[i - 1][0] * xbrinquedos[i] for i in range(1, n_brinquedos + 1)) + \
            lpSum((producao_pacotes[j - 1][3] - lpSum(dados_brinquedos[i - 1][0] for i in producao_pacotes[j - 1][:-1])) * pacotes[j] for j in range(1, n_pacotes + 1))

    # Total production constraint
    prob += lpSum(xbrinquedos[i] for i in range(1, n_brinquedos + 1)) <= max_producao

    # Constraints for individual toys and in packages
    for i in range(1, n_brinquedos + 1):
        prob += xbrinquedos[i] <= dados_brinquedos[i - 1][1]
        prob += lpSum(pacotes[j] for j in range(1, n_pacotes + 1) if i in producao_pacotes[j - 1][:-1]) <= dados_brinquedos[i - 1][1]

    # Package constraints
    for j in range(1, n_pacotes + 1):
        for i in producao_pacotes[j - 1][:-1]:
            prob += pacotes[j] <= xbrinquedos[i]
            prob += xbrinquedos[i] >= pacotes[j]

    # Solve the problem
    prob.solve()

    return int(value(prob.objective))

# Input
n, p, maxp = map(int, input().split())
lista_brinquedos = [list(map(int, input().split())) for _ in range(n)]
lista_pacotes = [list(map(int, input().split())) for _ in range(p)]

# Calculate and print the maximum profit
resultado = calcular_lucro_maximo(n, p, maxp, lista_brinquedos, lista_pacotes)
print(resultado)