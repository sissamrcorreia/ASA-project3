# Projeto 2 - Análise de Sistemas de Algoritmos - 2023

# Grupo: AL002
# Cecília Correia - 106827
# Luísa Fernandes - 102460

# Importar PuLP modeller functions
from pulp import *


def calcular_lucro_maximo(n, p, max_brinquedos, brinquedos, pacotes):
    # Criar o problema de programação linear
    prob = LpProblem("Maximizar_Lucro", LpMaximize)

    # Variáveis: quantidade de cada brinquedo a ser produzida
    quant = [LpVariable(f"x{i}", lowBound=0, cat="Integer") for i in range(1, n + 1)]

    # Maximizar o lucro total
    prob += sum(quant[i - 1] * brinquedos[i - 1][0] for i in range(1, n + 1)), "Lucro_Total"

    # Restrição de capacidade de produção
    prob += sum(quant[i - 1] * brinquedos[i - 1][1] for i in range(1, n + 1)) <= max_brinquedos, "Capacidade_Producao"

    # Adicionar restrições dos pacotes especiais
    for i, j, k, lucro in pacotes:
        prob += quant[i - 1] + quant[j - 1] + quant[k - 1] <= 2, f"Pacote_{i}_{j}_{k}"

    prob.solve()

    # Retornar lucro máximo
    return int(prob.objective.value())


# Ler a entrada
t, p, max_brinquedos = input().split()
t = int(t) # numero de brinquedos
p = int(p) # numero de pacotes
max_brinquedos = int(max_brinquedos) # capacidade máxima de produção
brinquedos = [tuple(map(int, input().split())) for _ in range(t)]
pacotes = [tuple(map(int, input().split())) for _ in range(p)]

# Calcular e imprimir o lucro máximo
resultado = calcular_lucro_maximo(t, p, max_brinquedos, brinquedos, pacotes)
print(resultado)