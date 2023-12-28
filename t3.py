from pulp import *

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

    # Resolvendo o problema
    prob.solve()

    # Imprimir informações finais
    print("\nApós Resolução:")
    for var in prob.variables():
        print(f"{var.name} = {var.varValue}")

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

    # Resolvendo o problema
    prob.solve()

    # Imprimir informações finais
    print("\nApós Resolução:")
    for var in prob.variables():
        print(f"{var.name} = {var.varValue}")


    # Retornando o resultado
    return int(value(prob.objective))

# Exemplo de uso
n_brinquedos, n_pacotes, max_producao = map(int, input().split())
dados_brinquedos = [list(map(int, input().split())) for _ in range(n_brinquedos)]
dados_pacotes = [list(map(int, input().split())) for _ in range(n_pacotes)]

producao_pacotes, _ = maximizar_lucro_pacotes(n_brinquedos, n_pacotes, max_producao, dados_brinquedos, dados_pacotes)
lucro_brinquedos_individuais = maximizar_lucro_brinquedos_individuais(n_brinquedos, max_producao, dados_brinquedos, producao_pacotes)

# Calculando o lucro total
resultado_total = sum(producao_pacotes[j] * dados_pacotes[j-1][3] for j in range(1, n_pacotes + 1)) + lucro_brinquedos_individuais
print(resultado_total)
