from pulp import *

t, p, max_prod = input().split()
t = int(t) # numero de brinquedos diferentes q podem ser produzidos
p = int(p) # numero de pacotes especiais
max_prod = int(max_prod) # numero maximo de brinquedos a ser produzido por dia

prob = LpProblem("MaximizeProfit", LpMaximize)

# vs = 0 o stor tinha esta linha q n percebi (maybe delete)
goal = 0
toys = [0]


for i in range(t):
    l, c = input().split()
    l = int(l) # lucro
    c = int(c) # capacidade de produção

    v = LpVariable("v_" + str(i), 0, c, LpInteger) 
    sp = LpVariable("cp_" + str(i), 0, c, LpInteger) 
    toys.append({'l' : l, 'c' : c, 'v' : v, 'sp' : sp, 'p': 0})
    
    prob += sp <= v, "SumBond" + str(i)
    
    goal += (v - sp) * l


for j in range(p):
    i, j, k, l = input().split()
    i = int(i) # brinquedo 1
    j = int(j) # brinquedo 2
    k = int(k) # brinquedo 3
    l = int(l) # lucro do pacote especial
    
    #pack_vars = toys[i - 1]['v'] + toys[j - 1]['v'] + toys[k - 1]['v']
    #pack_sp = toys[i - 1]['sp'] + toys[j - 1]['sp'] + toys[k - 1]['sp']
    #pack_profit = (toys[i - 1]['l'] + toys[j - 1]['l'] + toys[k - 1]['l']) * l
    #prob += pack_sp <= pack_vars, f"PackSum{j + 1}"
    
    #goal += pack_profit
    
prob += goal

#prob += lpSum([toy['v'] for toy in toys]) <= max_prod, "ProductionCapacity"

prob.solve()

print(int(prob.objective.value()))