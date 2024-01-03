from pulp import *

# Input
n, p, maxp = map(int, input().split())
lista_brinquedos = [list(map(int, input().split())) for _ in range(n)]
lista_pacotes = [list(map(int, input().split())) for _ in range(p)]

# Create the problem
prob = LpProblem("MaximizarLucroBrinquedosIndividuais", LpMaximize)

xbrinquedos = LpVariable.dicts("Brinquedo", range(1, n + 1), lowBound=0, upBound=maxp, cat=LpInteger)
pacotes = LpVariable.dicts("Pacote", range(1, p + 1), lowBound=0, upBound=maxp // 3, cat=LpContinuous)

# Combine objective function parts
prob += lpSum(lista_brinquedos[i - 1][0] * xbrinquedos[i] for i in range(1, n + 1)) + \
        lpSum((lista_pacotes[j - 1][3] - lpSum(lista_brinquedos[i - 1][0] for i in lista_pacotes[j - 1][:-1])) * pacotes[j] for j in range(1, p + 1))

# Total production constraint
prob += lpSum(xbrinquedos[i] for i in range(1, n + 1)) <= maxp

# Constraints for individual toys and in packages
for i in range(1, n + 1):
    prob += xbrinquedos[i] <= lista_brinquedos[i - 1][1]
    prob += lpSum(pacotes[j] for j in range(1, p + 1) if i in lista_pacotes[j - 1][:-1]) <= lista_brinquedos[i - 1][1]

# Package constraints
for j in range(1, p + 1):
    for i in lista_pacotes[j - 1][:-1]:
        prob += pacotes[j] <= xbrinquedos[i]
        prob += xbrinquedos[i] >= pacotes[j]

# Solve the problem
prob.solve(GLPK(msg=0))

# Print the result
print(int(value(prob.objective)))