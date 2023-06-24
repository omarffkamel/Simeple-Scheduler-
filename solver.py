from parser import *
from z3 import *
from parser import ParseDep, ParseIf


text_file = input("Enter the text file name: ")
with open(text_file, "r",encoding="utf-8") as f:
    file_data = f.readlines()

# Parse expressions with Or operator
class ParseExpressions(Parser):

    def __init__(self):
        self.parser = (ParseTerm() >> (lambda x: \
                       ParseIf(lambda a: a == "or", 2) >> (lambda _: \
                       ParseExpressions() >> (lambda b: \
                       Return(Or(x, b)))))) ^ ParseTerm()


# Parse terms with And Operator
class ParseTerm(Parser):

    def __init__(self):
        self.parser = (ParseFactor() >> (lambda x: \
                       ParseIf(lambda a: a == "and", 3) >> (lambda _: \
                       ParseTerm() >> (lambda b: \
                       Return(And(x, b)))))) ^ Pfactor()

# Represents a factor, either a single task or an expression with parentheses
class ParseFactor(Parser):

    def __init__(self):
        self.parser = ParseTask() >> (lambda v: Return(v)) ^ \
                      (ParseChar('(') >> (lambda _: \
                      ParseExpressions() >> (lambda v: \
                      ParseChar(')') >> (lambda _: \
                      Return(v)))))

# Storing Parsed Results
ts = []
dr = []
dp = []
task_list = []

for i in file_data:

    if i.isspace():
        continue

    pt = ParseTask().parse(i)

    if (pt != []):
        ts.append(result(pt))

    d = ParseDependency().parse(i)

    if (d != []):
        dr.append(result(d))

    t = ParseDuration().parse(i)

    if (t != []):
        dp.append(result(t))

for j in range(len(ts)):
    task_list.append(CreateTask(ts[j],dr[j],dp[j]))

solver  =Solver()

for i in range(len(ts)):
    a = ParseExpressions().parse(dp[j])
    solver.add(Implies(result(a), ts[j]))

def true_operator(m_model):
    list_m = [m_model.eval(i) for i in ts]
    if all(list_m):
        return 1

    else:
        return 0

def if_unique(solver):
    m_model = solver.model()
    l1, l2 = Bool("l1"), Bool("l2")

    for l in [l1,l2]:
        if m_model[l] == True:
            solver.push()
            solver.add(l != True)
            if solver.check() == sat:
                solver.pop()
                return 0
            solver.pop()
            solver.check()

    return 1

def solution(solver, sat=None):

    if solver.check() == sat:
        if if_unique(s):
            if true_operator(solver.model()):
                return solver
            return solver
        else:
            print("Solution not unique!")
            return solver
    else:
        print("No solution")
        return solver

solution(solver)

def computedSolution(ts, dp):
    tasklist = ts[:]
    dplist = dep[:]
    retlist = []
    solver_a = Solver()
    for i in range(len(ts)):
        if dp[i] is None:
            retlist.append(ts[i])
            tasklist.remove(ts[i])
            dplist.remove(dp[i])
            solver_a.add(ts[i])

    while len(tasklist) > 0:
        for i in range(len(tasklist)):
            solver_a.push()
            solver_a.add(Implies(dplist[i], tasklist[i]))
            if solver_a.check() == sat:
                if true_operator(a.model()):
                    retlist.append(tasklist[i])
                    tasklist.pop(i)
                    dplist.pop(i)
                    break
            else:
                solver_a.pop()
    return retlist

answer = computedSolution(ts, dp)

def show_solution(u):

    solution = []
    a, b = 0, 0
    for i in range(len(u)):
        for j in range(len(ts)):
            if order[i] == ts[j]:
                b = a + dr[j]
                solution.append((u[i], a, b))
                a = b
    print(solution)

show_solution(answer)


