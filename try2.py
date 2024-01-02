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

    v = LpVariable("v_" + str(i), 0, c, LpInteger) # variável de decisão para a quantidade de brinquedo i a serem produzidos
    sp = LpVariable("sp_" + str(i), 0, c, LpInteger) # quantidade de brinquedo i a serem produzidos para pacotes especiais
    toys.append({'l' : l, 'c' : c, 'v' : v, 'sp' : sp, 'p': 0})
    
    # restrição para garantir que a quantidade de brinquedos produzida para pacotes especiais (sp) 
    # não exceda a quantidade total produzida (v)
    prob += sp <= v, "SumBond" + str(i)
    
    # lucro de cada brinquedo para o objetivo total, tendo em consideração a produção para pacotes especiais (sp)
    goal += (v - sp) * l
    
    # restrição todos os brinquedos produzidos tem de ser menor que o max_prod


for pack in range(p):
    i, j, k, l = input().split()
    i = int(i) # brinquedo 1
    j = int(j) # brinquedo 2
    k = int(k) # brinquedo 3
    l = int(l) # lucro do pacote especial
    
    # quantidade total de pacotes especiais produzidos
    pack_vars = LpVariable(f"pack_{pack}", 0, None, LpInteger) 
    
    # Restrição para garantir que a quantidade total produzida para pacotes especiais não exceda a capacidade fixme
    prob += pack_vars * (toys[i]['c'] + toys[j]['c'] + toys[k]['c']) <= max_prod, f"PackCapacity{pack}"
    
    # Restrição para garantir que a quantidade de brinquedos produzida para pacotes especiais (sp) não exceda a quantidade total produzida (v)
    prob += pack_vars <= toys[i]['sp'], f"PackBond{i}_toy_{pack}"
    prob += pack_vars <= toys[j]['sp'], f"PackBond{j}_toy_{pack}"
    prob += pack_vars <= toys[k]['sp'], f"PackBond{k}_toy_{pack}"
        
    # Contribuição do lucro de cada pacote especial ao objetivo total
    goal += pack_vars * l

# maximizar o lucro total
prob += goal

prob.solve()
# Imprimir quantidades ótimas de cada brinquedo
for var in prob.variables():
    print(f"{var.name}: {var.value()}")

print(int(prob.objective.value()))