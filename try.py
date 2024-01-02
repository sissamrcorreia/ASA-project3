import cProfile
# Importar PuLP modeller functions
from pulp import *
# Desativar mensagens de impressão do PuLP
LpSolverDefault.msg = 0

def calcular_lucro_maximo(n_brinquedos, n_pacotes, max_producao, dados_brinquedos, producao_pacotes):
    # Criação do problema de maximização
    prob = LpProblem("MaximizarLucroBrinquedosIndividuais", LpMaximize)

    # Criação das variáveis de decisão
    xbrinquedos = LpVariable.dicts("Brinquedo", range(1, n_brinquedos + 1), lowBound=0, upBound=max_producao, cat=LpInteger)
    pacotes = LpVariable.dicts("Pacote", range(1, n_pacotes + 1), lowBound=0, upBound=max_producao//3, cat=LpContinuous)

    # Função objetivo para brinquedos 
    parte1 = sum(dados_brinquedos[i-1][0] * xbrinquedos[i] for i in range(1, n_brinquedos + 1))

    # Função objetivo para pacotes
    parte2 = sum((producao_pacotes[j-1][3] - sum(dados_brinquedos[i-1][0] for i in producao_pacotes[j-1][:-1])) * pacotes[j] for j in range(1, n_pacotes + 1))

    # Adiciona diretamente à função objetivo a diferença entre o preço do pacote e o preço dos brinquedos que o compõem
    prob += parte1 + parte2 

    # Restrição de produção total
    prob += sum(xbrinquedos[i] for i in range(1, n_brinquedos + 1)) <= max_producao

    # Restrições de pacotes
    for j in range(1, n_pacotes + 1):
        # Restrição de quantidade de pacotes disponíveis
        for i in producao_pacotes[j-1][:-1]:
            prob += pacotes[j] <= xbrinquedos[i]
            prob += xbrinquedos[i] >= pacotes[j]

    # Restrições para brinquedos individuais e em pacotes
    for i in range(1, n_brinquedos + 1):
        prob += xbrinquedos[i] <= dados_brinquedos[i-1][1]
        prob += sum(pacotes[j] for j in range(1, n_pacotes + 1) if i in producao_pacotes[j-1][:-1]) <= dados_brinquedos[i-1][1]

    # Resolve o problema
    prob.solve(PULP_CBC_CMD(msg=False, timeLimit=200))

    
    # Retorna o resultado
    return int(value(prob.objective))

# Recebe o input
n, p, maxp = map(int, input().split())
lista_brinquedos = [list(map(int, input().split())) for _ in range(n)]
lista_pacotes = [list(map(int, input().split())) for _ in range(p)]

# Calcular e imprimir o lucro máximo
resultado = calcular_lucro_maximo(n, p, maxp, lista_brinquedos, lista_pacotes)
print(resultado)