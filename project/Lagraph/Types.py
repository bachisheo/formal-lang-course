from dataclasses import dataclass
from pyformlang.finite_automaton import EpsilonNFA
from networkx.drawing.nx_pydot import to_pydot


class LagraphType:
    def __init__(self):
        self.value = None

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, LagraphType):
            return self.value == __value.value
        return False


@dataclass
class FSMType(LagraphType):
    """Finite state machine"""

    value: EpsilonNFA

    def get_val(self) -> EpsilonNFA:
        return self.value

    def __str__(self) -> str:
        return to_pydot(self.value.to_networkx()).to_string()


class RSMType(LagraphType):
    """Recursive state machine"""

    pass


class LambdaType(LagraphType):
    def __init__(self, var_name, expr):
        self.var_name = var_name
        self.expr = expr

    def call(self, value: LagraphType, visiter):
        visiter.mem.set_var(self.var_name, value)
        return self.expr.accept(visiter)

    def __str__(self):
        return "lambda: \\ {self.var_name} : {str(self.expr)}"
