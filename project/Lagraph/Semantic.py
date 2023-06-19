from project.Lagraph.Types import *
from project.fa_utils import intersection


def set_expression(vertexes, graph, operator):
    pass


def get_expression(graph, operator):
    if isinstance(graph, StateMachine):
        pass
    if isinstance(graph, RSM):
        x = graph.value
    else:
        x = graph.value
    if isinstance(x, EpsilonNFA):
        if operator == "startOf":
            return x.start_states
        if operator == "finalOf":
            return x.final_states
        if operator == "reachableOf":
            pass
        if operator == "verticesOf":
            return x.states
        if operator == "edgesOf":
            pass
        if operator == "labelsOf":
            return {symb for _, _, symb in x}
    raise ValueError


def map_expression(lambda_, graph):
    pass


def binary_operation(expr1, expr2, operator: str) -> EpsilonNFA:
    if isinstance(expr1, StateMachine) and isinstance(expr1, StateMachine):
        pass
    # if isinstance(graph, RSM):
    #     x = graph.value
    # else:
    #     x = graph.value
    x1 = expr1.value, x2 = expr2.value
    if isinstance(x1, EpsilonNFA) and isinstance(x2, EpsilonNFA):
        if operator == "&&":
            return intersection(x1, x2)
        if operator == "++":
            return x1.concatenate(x2)
        if operator == "||":
            return x1.union(x2)
    raise ValueError
