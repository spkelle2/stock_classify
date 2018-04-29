from pulp import *


def split(rows, y, percent_gap=0.001):
    """split an attribute of our dataframe into two groups by minimizing the
    total distance all points are from our dividing threshold

    :param rows: range(0, number of rows) to represent indices when iterating
    over attribute and variable values
    :param y: a series representing the values of our attribute being split
    :param percent_gap: how short of optimality we stop the solver.
    0.001x100% = .1% from optimality
    
    :return: results: a dictionary detailing the objective value of our model
    as well as the values of each variable
    """

    # arbitrarily large number
    M = 100000

    # Create a variable, "prob", to contain our problem data
    prob = LpProblem("split", LpMinimize)

    # Create problem variables
    # Force distance to be ignored if right of split
    b = LpVariable.dicts('b', rows, lowBound=0, upBound=None, cat='Continuous')

    # Whether or not a data point x is left or right of a split
    x = LpVariable.dicts('x', rows, lowBound=0, upBound=1, cat='Integer')

    # Absolute value of distance from average
    z = LpVariable.dicts('z', rows, lowBound=0, upBound=None, cat='Continuous')

    # 1
    # Objective is to minimize total distance from mean
    prob += lpSum([b[i] for i in rows])

    # 2.1
    # make z greater than absolute value of the distance of the value from the mean
    for i in rows:
        prob += y[i]*sum([x[j] for j in rows]) - sum([x[j]*y[j] for j in rows]) \
                <= z[i]

    # 2.2
    # make z greater than absolute value of the distance of the value from the mean
    for i in rows:
        prob += y[i] * sum([x[j] for j in rows]) - sum([x[j]*y[j] for j in rows]) \
                >= -z[i]

    # 3
    # coerce z to some value (josh explain)
    for i in rows:
        prob += b[i] + M*(1-x[i]) >= z[i]

    # The problem data is written to an lp file
    prob.writeLP('split.lp')

    # The problem is solved using PuLP's choice of Solver
    prob.solve(PULP_CBC_CMD(fracGap=percent_gap))

    results = {
        'status': LpStatus[prob.status],
        'objective': value(prob.objective),
        'variables': prob.variables()
    }

    return results
