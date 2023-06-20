"""
Semantic module for interpretor
"""
from project.Lagraph.Exceptions import InterpretingError
from project.Lagraph.Types import LambdaType, FSMType
from pyformlang.finite_automaton import EpsilonNFA

from project.fa_utils import (
    build_nfa_from_string,
    intersection,
    union,
    concatenation,
    PythonRegex,
)
from project.graph_utils import load_graph_by_name, load_graph_from_file
from project.tensor import start_final_states_rpq


def set_expression(states, graph, operator):
    """
    Sets the start or final states of a graph.

    Args:
        states (set): The set of states to be set.
        graph (FSMType): The graph on which the operation is performed.
        operator (str): The type of operation to be performed. Can be "setStart", "setFinal", "addStart", or "addFinal".

    Returns:
        FSMType: The graph after applying the operation.

    Raises:
        InterpretingError: If the input is not of the correct types.
    """
    if not isinstance(states, set):
        raise InterpretingError(f"Cant insert not set value in '{operator}'")

    nfa: EpsilonNFA = EpsilonNFA()
    if isinstance(graph, FSMType):
        nfa = graph.value
    else:
        raise InterpretingError(f"Cant apply '{operator}' operations to not graph")
    if operator == "setStart":
        for st in nfa.states:
            nfa.remove_start_state(st)
        for st in states:
            nfa.add_start_state(st)
    elif operator == "setFinal":
        for st in nfa.states:
            nfa.remove_final_state(st)
        for st in states:
            nfa.add_final_state(st)
    elif operator == "addStart":
        for st in states:
            nfa.add_start_state(st)
    elif operator == "addFinal":
        for st in states:
            nfa.add_final_state(st)

    return FSMType(nfa)


def get_expression(graph, operator):
    """
    Retrieves information from a graph.

    Args:
        graph (RSMType or FSMType): The graph from which information is retrieved.
        operator (str): The type of operation to be performed. Can be "startOf", "finalOf", "reachableOf", "verticesOf",
            "edgesOf", or "labelsOf".

    Returns:
        set or dict: The result of the operation.

    Raises:
        InterpretingError: If the input is not of the correct types.
    """
    if isinstance(graph, FSMType):
        nfa = graph.value
    else:
        raise InterpretingError(f"Cant apply '{operator}' operations to not graph")
    if operator == "startOf":
        return nfa.start_states
    elif operator == "finalOf":
        return nfa.final_states
    elif operator == "reachableOf":
        all_pairs = start_final_states_rpq(nfa, PythonRegex.from_python_regex(".*"))
        s = {to.value for from_, to in all_pairs}
        return s

    elif operator == "verticesOf":
        return {x.value for x in nfa.states}
    elif operator == "edgesOf":
        return {(from_.value, symb.value, to.value) for from_, symb, to in nfa}
    elif operator == "labelsOf":
        return {symb.value for _, symb, _ in nfa}


def map_expression(visiter, lambda_: LambdaType, set_var):
    """
    Applies a lambda function to each element in a set.

    Args:
        visiter: The visiter object.
        lambda_ (LambdaType): The lambda function to apply.
        set_var (set): The set of elements.

    Returns:
        set: The resulting set after applying the lambda function to each element.

    Raises:
        InterpretingError: If the lambda function or the input set is not of the correct type.
    """
    if not isinstance(lambda_, LambdaType):
        raise InterpretingError("Not lambda type")
    if not isinstance(set_var, set):
        raise InterpretingError("Not set type")
    return set([lambda_.call(x, visiter) for x in set_var])


def filter_expression(visiter, lambda_: LambdaType, set_var):
    """
    Filters a set based on a lambda function.

    Args:
        visiter: The visiter object.
        lambda_ (LambdaType): The lambda function to apply for filtering.
        set_var (set): The set of elements to filter.

    Returns:
        set: The resulting set after filtering based on the lambda function.

    Raises:
        InterpretingError: If the lambda function or the input set is not of the correct type.
    """
    if not isinstance(lambda_, LambdaType):
        raise InterpretingError("Not lambda type")
    if not isinstance(set_var, set):
        raise InterpretingError("Not set type")
    return set([x for x in set_var if lambda_.call(x, visiter)])


def binary_operation(expr1, expr2, operator):
    """
    Performs a binary operation on two expressions.

    Args:
        expr1: The first expression.
        expr2: The second expression.
        operator (str): The binary operator to apply.

    Returns:
        The result of the binary operation.

    Raises:
        InterpretingError: If the expressions are not of compatible types or the operator is not supported.
    """
    if operator == "==":
        if type(expr1) != type(expr2):
            raise InterpretingError("Cant compare object of different types")
        return int(expr1 == expr2)

    if isinstance(expr1, FSMType) and isinstance(expr2, FSMType):
        x1 = expr1.value
        x2 = expr2.value
        if operator == "&&":
            return intersection(x1, x2)
        if operator == "++":
            return concatenation(x1, x2)
        if operator == "||":
            return union(x1, x2)
    raise InterpretingError


def load_graph(way: str, source: str):
    """
    Loads a graph based on the specified way and source.

    Args:
        way (str): The way to load the graph. Can be "path", "regex", or "name".
        source (str): The source information for loading the graph.

    Returns:
        FSMType: The loaded graph.

    Raises:
        InterpretingError: If the way is not supported or an error occurs during graph loading.
    """
    if way == "path":
        graph = load_graph_from_file(source)
        nfa = EpsilonNFA.from_networkx(graph)
        return FSMType(nfa)

    elif way == "regex":
        nfa = build_nfa_from_string(source)
        return FSMType(nfa)

    elif way == "name":
        nfa = load_graph_by_name(source)
        return FSMType(EpsilonNFA.from_networkx(nfa))

    raise InterpretingError


def Star(graph):
    """
    Applies the star operation to a graph.

    Args:
        graph (FSMType): The graph to apply the star operation to.

    Returns:
        FSMType: The resulting graph after applying the star operation.

    Raises:
        InterpretingError: If the input is not of the correct type.
    """
    if not isinstance(graph, FSMType):
        raise InterpretingError(f"Cant apply star operation to not graph type")
    return FSMType(graph.value.kleene_star())


def is_in_set(elem, set_) -> int:
    """
    Checks if an element is in a set.

    Args:
        elem: The element to check.
        set_ (set): The set to check.

    Returns:
        int: Returns 1 if the element is in the set, otherwise returns 0.
    """
    for x in set_:
        if type(elem) == type(x) and elem == x:
            return 1
    return 0
