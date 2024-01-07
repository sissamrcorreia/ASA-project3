from pulp import *

# Leitura dos dados de entrada
nb, np, max_value = map(int, input().split())
toys = {}
packs = {}
prob = LpProblem("m", LpMaximize)

# Create toys dictionary
for i in range(1, nb + 1):
    l, c = map(int, input().split())
    x = LpVariable("xb" + str(i), 0, c, LpInteger)
    toys[i] = {'l': l, 'c': c, 'x': x}

# Create packs dictionary
for j in range(1, np + 1):
    t1, t2, t3, l = map(int, input().split())
    r = toys[t1]['l'] + toys[t2]['l'] + toys[t3]['l']
    p = LpVariable("pac" + str(j), 0, max_value // 3, cat=LpContinuous)
    packs[j] = {'t1': t1, 't2': t2, 't3': t3, 'l': l, 'p': p, 'r': r}

# Combine objective function parts
prob += lpSum(toys[i]['l'] * toys[i]['x'] for i in range(1, nb + 1)) + \
        lpSum((packs[j]['l'] - packs[j]['r']) * packs[j]['p'] for j in range(1, np + 1))

# Total production constraint
prob += lpSum(toys[i]['x'] for i in range(1, nb + 1)) <= max_value

# Constraints for individual toys and in packages
for i in range(1, nb + 1):
    prob += lpSum(packs[j]['p'] for j in range(1, np + 1) if i in (packs[j]['t1'], packs[j]['t2'], packs[j]['t3'])) <= toys[i]['x']

# Package constraints
for j in range(1, np + 1):
    prob += packs[j]['p'] <= toys[packs[j]['t1']]['x']
    prob += packs[j]['p'] <= toys[packs[j]['t2']]['x']
    prob += packs[j]['p'] <= toys[packs[j]['t3']]['x']

# prob.writeLP("teste.lp")
# Solve the problem
prob.solve(GLPK(msg=0))

print(int(value(prob.objective)))
