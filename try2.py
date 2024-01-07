from pulp import *

t, p, max_prod = map(int, input().split())
toys = {}

prob = LpProblem("MaximizeProfit", LpMaximize)

goal = 0

# Add toy variables and constraints using LpVariable.dicts
toys = LpVariable.dicts('v', range(1, t + 1), lowBound=0, cat=LpInteger)

# Additional information about each toy
toy_details = {i: {'c': 0, 'p': 0} for i in range(1, t + 1)}

for i in range(1, t + 1):
    l, c = map(int, input().split())
    toy_details[i]['c'] = c

    # The quantity produced for special packages is limited by the total quantity v
    prob += toys[i] >= toy_details[i]['p'], f"PackBond{i}"

    goal += (toys[i] - toy_details[i]['p']) * l

# Add package variables and constraints using a single variable
total_packs = LpVariable("total_packs", 0, None, LpInteger)

for pack in range(1, p + 1):
    i, j, k, pack_price = map(int, input().split())

    # Use lpSum for package capacity constraint
    prob += lpSum([toys[i], toys[j], toys[k]]) <= max_prod, f"PackCapacity{pack}"

    # Use the same decision variable (total_packs) for the contribution to the objective function
    goal += total_packs * pack_price

# Maximize the total profit
prob += goal

status = prob.solve(GLPK(msg=0))

for var in prob.variables():
    print(f"{var.name}: {var.value()}")

print(int(pulp.value(prob.objective)))
