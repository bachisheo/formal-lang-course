from pyformlang.finite_automaton import EpsilonNFA
from networkx.drawing.nx_pydot import to_pydot

from project.Lagraph.Interpreter import InterpretingVisitor


class LagraphType:
    def __init__(self):
        self.value = None

    def __str__(self):
        str(self.value)


class String(LagraphType):
    def __init__(self, val: str):
        self.value = val


class Int(LagraphType):
    def __init__(self, val: str):
        self.value = int(val)


class Set(LagraphType):
    def __init__(self, vals):
        self.value = vals


class Lambda(LagraphType):
    def __init__(self, var_name, expr):
        self.var_name = var_name
        self.expr = expr

    def call(self, value: LagraphType, visiter: InterpretingVisitor):
        visiter.mem.add_var(self.var_name, value)
        return self.expr.accept(visiter)

    def __str__(self):
        return "lambda: \\ {self.var_name} : {str(self.expr)}"


class StateMachine(LagraphType):
    def __init__(self):
        pass


class FSM(StateMachine):
    """Finite state machine"""

    def __init__(self, fa: EpsilonNFA):
        self.value: EpsilonNFA = fa

    def __str__(self):
        to_pydot(self.value.to_networkx()).to_string()


class RSM(StateMachine):
    """Recursive state machine"""

    pass
