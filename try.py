from pulp import LpProblem, LpVariable, lpSum, LpMaximize

# Criar um problema de maximização
prob = LpProblem("MaximizeProfit", LpMaximize)

# Definir as variáveis
x1 = LpVariable("x1", lowBound=0, cat="Integer")
x2 = LpVariable("x2", lowBound=0, cat="Integer")
x3 = LpVariable("x3", lowBound=0, cat="Integer")
x4 = LpVariable("x4", lowBound=0, cat="Integer")
x5 = LpVariable("x5", lowBound=0, cat="Integer")
x6 = LpVariable("x6", lowBound=0, cat="Integer")
x7 = LpVariable("x7", lowBound=0, cat="Integer")
x8 = LpVariable("x8", lowBound=0, cat="Integer")
# Variável adicional para indicar presença simultânea dos tipos 3, 4 e 6
pack1 = LpVariable("pack1", lowBound=0, cat="Continuous")
pack2 = LpVariable("pack2", lowBound=0, cat="Continuous")
pack3 = LpVariable("pack3", lowBound=0, cat="Continuous")
pack4 = LpVariable("pack4", lowBound=0, cat="Continuous")
pack5 = LpVariable("pack5", lowBound=0, cat="Continuous")

# Adicionar a função objetivo
prob += 5 * x1 + 24 * x2 + 32 * x3 + 37 * x4 + 8 * x5 + 15 * x6 + 3 * x7 + 34 * x8 + 39*pack1+ 48*pack2+25*pack3+65*pack4+37*pack5, "TotalGastos"

# Adicionar as restrições
prob += x1 <= 20, "RestricaoTipo1"
prob += pack2 + pack3 <= 20, "RestricaoBrinquedo1Pack"
prob += x2 <= 14, "RestricaoTipo2"
prob += pack2 + pack4 + pack5 <= 14, "RestricaoBrinquedo2Pack"
prob += x3 <= 5, "RestricaoTipo3"
prob += pack1 + pack3 + pack4 + pack5<= 5, "RestricaoBrinquedo3Pack"
prob += x4 <= 12, "RestricaoTipo4"
prob += x5 <= 17, "RestricaoTipo5"
prob += pack2 + pack5 <= 17, "RestricaoBrinquedo5Pack"
prob += x6 <= 1, "RestricaoTipo6"
# Restrição para garantir que o brinquedo 6 só seja usado em um pack
prob += pack1 + pack3 <= 1, "RestricaoBrinquedo6Pack"
prob += x7 <= 1, "RestricaoTipo7"
prob += pack1 + pack4 <= 1, "RestricaoBrinquedo7Pack"
prob += x8 <= 6, "RestricaoTipo8"

prob+=x3>=pack1;
prob+=x7>=pack1;
prob+=x6>=pack1;

prob+=x1>=pack2;
prob+=x2>=pack2;
prob+=x5>=pack2;

prob+=x1>=pack3;
prob+=x3>=pack3;
prob+=x6>=pack3;

prob+=x2>=pack4;
prob+=x3>=pack4;
prob+=x7>=pack4;

prob+=x5>=pack5;
prob+=x2>=pack5;
prob+=x3>=pack5;

# Restrição de produção total
prob += x1+x2+x3+x4+x5+x6+x7+x8 <= 70

# Resolver o problema
prob.solve()

# Imprimir resultados
print("Status:", prob.status)
print("Total gasto: €", round(prob.objective.value(), 2))

# Imprimir quantidades ótimas de cada brinquedo
for var in prob.variables():
    print(f"{var.name}: {var.value()}")

