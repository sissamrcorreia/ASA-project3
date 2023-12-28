# Projeto 2 - Análise de Sistemas de Algoritmos - 2023

# Grupo: AL002
# Cecília Correia - 106827
# Luísa Fernandes - 102460

# Importar PuLP modeller functions
from pulp import *

def maximizar_lucro_brinquedos_simples(n_brinquedos, max_producao, dados_brinquedos):
    # Criação do problema de maximização para brinquedos individuais
    prob_brinquedos = LpProblem("MaximizarLucroBrinquedosSimples", LpMaximize)

    # Criação das variáveis de decisão para brinquedos individuais
    brinquedos = LpVariable.dicts("Brinquedo", range(1, n_brinquedos + 1), lowBound=0, upBound=max_producao, cat=LpInteger)

    # Função objetivo apenas para brinquedos individuais
    prob_brinquedos += lpSum(dados_brinquedos[i-1][0] * brinquedos[i] for i in range(1, n_brinquedos + 1)), "LucroBrinquedosIndividuais"

    # Restrições de produção para cada brinquedo
    for i in range(1, n_brinquedos + 1):
        prob_brinquedos += brinquedos[i] <= dados_brinquedos[i-1][1]

    # Restrição de produção total
    prob_brinquedos += lpSum(brinquedos[i] for i in range(1, n_brinquedos + 1)) <= max_producao

    # Resolve o problema para brinquedos individuais
    prob_brinquedos.solve()

    # Calcula o lucro máximo possível sem usar pacotes
    lucro_max_brinquedos = int(value(prob_brinquedos.objective))

    return lucro_max_brinquedos 

def maximizar_lucro_pacotes(n_brinquedos, n_pacotes, max_producao, dados_brinquedos, dados_pacotes):
    # Criação do problema de maximização
    prob = LpProblem("MaximizarLucroPacotes", LpMaximize)

    # Criação das variáveis de decisão
    brinquedos = LpVariable.dicts("Brinquedo", range(1, n_brinquedos + 1), lowBound=0, upBound=max_producao, cat=LpInteger)
    pacotes = LpVariable.dicts("Pacote", range(1, n_pacotes + 1), lowBound=0, upBound=max_producao//3, cat=LpInteger)

    # Função objetivo apenas para pacotes
    prob += lpSum(dados_pacotes[j-1][3] * pacotes[j] for j in range(1, n_pacotes + 1)), "LucroPacotes"

    # Restrições de produção para cada brinquedo
    for i in range(1, n_brinquedos + 1):
        prob += brinquedos[i] <= dados_brinquedos[i-1][1]

    # Restrição de produção total
    prob += lpSum(brinquedos[i] for i in range(1, n_brinquedos + 1)) + 3 * lpSum(pacotes[j] for j in range(1, n_pacotes + 1)) <= max_producao

    # Restrições de quantidade máxima por tipo de brinquedo
    for i in range(1, n_brinquedos + 1):
        prob += lpSum(pacotes[j] for j in range(1, n_pacotes + 1) if i in dados_pacotes[j-1][0:3]) <= dados_brinquedos[i-1][1]

    # Resolve o problema
    prob.solve()

    # Retornando a produção de pacotes e brinquedos individuais
    producao_pacotes = {i: int(value(pacotes[i])) for i in range(1, n_pacotes + 1)}
    producao_brinquedos = {i: int(value(brinquedos[i])) for i in range(1, n_brinquedos + 1)}

    return producao_pacotes, producao_brinquedos

def maximizar_lucro_brinquedos_individuais(n_brinquedos, max_producao, dados_brinquedos, producao_pacotes):
    # Criação do problema de maximização
    prob = LpProblem("MaximizarLucroBrinquedosIndividuais", LpMaximize)

    # Criação das variáveis de decisão
    brinquedos = LpVariable.dicts("Brinquedo", range(1, n_brinquedos + 1), lowBound=0, upBound=max_producao, cat=LpInteger)

    # Função objetivo apenas para brinquedos individuais
    prob += lpSum(dados_brinquedos[i-1][0] * brinquedos[i] for i in range(1, n_brinquedos + 1)), "LucroBrinquedosIndividuais"

    # Restrições de produção para cada brinquedo
    for i in range(1, n_brinquedos + 1):
        prob += brinquedos[i] <= dados_brinquedos[i-1][1] - sum(producao_pacotes[j] for j in range(1, n_pacotes + 1) if i in dados_pacotes[j-1][0:3])

    # Restrição de produção total
    prob += lpSum(brinquedos[i] for i in range(1, n_brinquedos + 1)) <= max_producao - 3 * lpSum(producao_pacotes[j] for j in range(1, n_pacotes + 1))

    # Resolve o problema
    prob.solve()

    # Retorna o resultado
    return int(value(prob.objective))

# Recebe o input
n_brinquedos, n_pacotes, max_producao = map(int, input().split())
dados_brinquedos = [list(map(int, input().split())) for _ in range(n_brinquedos)]
dados_pacotes = [list(map(int, input().split())) for _ in range(n_pacotes)]

copia_brinquedos = dados_brinquedos.copy()

# Calcula lucro maximo de pacotes e de seguida dos brinquedos individuais que sobraram
producao_pacotes, _ = maximizar_lucro_pacotes(n_brinquedos, n_pacotes, max_producao, dados_brinquedos, dados_pacotes)
lucro_brinquedos_individuais = maximizar_lucro_brinquedos_individuais(n_brinquedos, max_producao, dados_brinquedos, producao_pacotes)

# Calcula o lucro total
resultado_total = sum(producao_pacotes[j] * dados_pacotes[j-1][3] for j in range(1, n_pacotes + 1)) + lucro_brinquedos_individuais
#print(resultado_total)

# Calcula o lucro maximo de brinquedos individuais sem pacotes
lucro_alternativo = maximizar_lucro_brinquedos_simples(n_brinquedos, max_producao, copia_brinquedos)
#print(lucro_alternativo)

print(max(resultado_total, lucro_alternativo))