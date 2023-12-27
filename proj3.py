# Projeto 2 - Análise de Sistemas de Algoritmos - 2023

# Grupo: AL002
# Cecília Correia - 106827
# Luísa Fernandes - 102460

# Importar PuLP modeller functions
from pulp import LpProblem, LpMaximize, LpVariable

def calcular_lucro_maximo(n, p, max_brinquedos, brinquedos, pacotes):
    # Criar o problema de programação linear
    problema = LpProblem("Maximizar_Lucro", LpMaximize)

    # Variáveis: quantidade de cada brinquedo a ser produzida
    quantidades = [LpVariable(f"x{i}", lowBound=0, cat="Integer") for i in range(1, n + 1)]

    # Função objetivo: maximizar o lucro total
    problema += sum(quantidades[i - 1] * brinquedos[i - 1][0] for i in range(1, n + 1)), "Lucro_Total"

    # Restrição de capacidade de produção
    problema += sum(quantidades[i - 1] * brinquedos[i - 1][1] for i in range(1, n + 1)) <= max_brinquedos, "Capacidade_Producao"

    # Adicionar restrições dos pacotes especiais
    for i, j, k, lucro in pacotes:
        problema += quantidades[i - 1] + quantidades[j - 1] + quantidades[k - 1] <= 2, f"Pacote_{i}_{j}_{k}"

    problema.solve()

    # Retornar lucro máximo
    return int(problema.objective.value())


# Ler a entrada
t, p, max_brinquedos = map(int, input().split()) # map para converter strings em inteiros
brinquedos = [tuple(map(int, input().split())) for _ in range(t)]
pacotes = [tuple(map(int, input().split())) for _ in range(p)]

# Calcular e imprimir o lucro máximo
resultado = calcular_lucro_maximo(t, p, max_brinquedos, brinquedos, pacotes)
print(resultado)