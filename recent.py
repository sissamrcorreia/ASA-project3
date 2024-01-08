from pulp import *

# Leitura dos dados de entrada
nb, np, m = map(int, input().split())
toys = []
packs = []
prob = LpProblem("Ma", LpMaximize)

for i in range (1, nb+1):
    l, c = map(int, input().split())
    x = LpVariable("xb"+str(i), 0, c, LpInteger)
    toys.append([l,c,x])

for j in range (1, np+1):
    t1, t2, t3, l = map(int, input().split())
    r = toys[t1-1][0]+toys[t2-1][0]+toys[t3-1][0]
    p = LpVariable("pac" + str(j), 0, m // 3, LpInteger)
    packs.append([t1, t2, t3, l, p, r])
    toy_indices = [packs[j - 1][0] - 1, packs[j - 1][1] - 1, packs[j - 1][2] - 1]
    prob += packs[j - 1][4] <= lpSum(toys[i][2] for i in toy_indices)

# Combine objective function parts
prob += lpSum(toys[i - 1][0] * toys[i-1][2] for i in range(1, nb + 1)) + \
        lpSum((packs[j - 1][3] - packs[j-1][5]) * packs[j-1][4] for j in range(1, np + 1))

# Total production constraint
prob += lpSum(toy[2] for toy in toys) <= m

# Constraints for individual toys in packages
for i in range(1, nb + 1):
    prob += lpSum(pack[4] for pack in packs if i in pack[:-3]) <= toys[i - 1][2]

# Solve the problem
prob.solve(GLPK(msg=0))

print(int(value(prob.objective)))

# Imprimir informações finais
#for var in prob.variables():
#    print(f"{var.name} = {var.varValue}")