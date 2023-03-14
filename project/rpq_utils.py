from project import finite_automaton as fa
from pyformlang.finite_automaton import EpsilonNFA, State
from collections import namedtuple
from scipy import sparse
from scipy.sparse import csc_array as array_type
from functools import reduce
from networkx import MultiDiGraph


BooleanDecomposition = namedtuple("BooleanDecomposition", ["arrays", "idx", "states"])


def boolean_decomposition(f_auto: EpsilonNFA) -> BooleanDecomposition:
    """
    Represents an automaton in the form of a dictionary,
    where the key is the symbol x,
    the value is a matrix with transitions only on x.

    Parameters
    ----------
    f_auto: `~pyformlang.finite_automaton.EpsilonNFA`

    Returns
    -------
    decomp: `BooleanDecomposition`
    The named tuple with graph decomposition, where
    `arrays` - dictionary with symbol and their boolean matrix
    `idx` - list with States of graph (fixed indexes)
    `states` - dictionary with State and their index in matrix
    """
    states = list(f_auto.states)
    idxs = dict()
    for i in range(len(states)):
        idxs[states[i]] = i
    arrays = {
        symbol: array_type((len(states), len(states)), dtype=bool)
        for symbol in f_auto.symbols
    }
    for from_, symb, to in f_auto:
        arrays[symb][idxs[from_], idxs[to]] = True
    return BooleanDecomposition(arrays, idxs, states)


def intersection(fa1: EpsilonNFA, fa2: EpsilonNFA) -> EpsilonNFA:
    """Computes the intersection of two finite automata
    using the tensor product of the boolean decomposition of automata.

    Parameters
    ----------
    fa1: `~pyformlang.finite_automaton.EpsilonNFA`
        First finite automation, located on the left in the product
    fa2: `~pyformlang.finite_automaton.EpsilonNFA`
        Second finite automation, located on the right in the product

    Returns
    -------
    fa3: `~pyformlang.finite_automaton.EpsilonNFA`
        The intersection of the two Epsilon NFAs
    """
    arrays1, idxs1, states1 = boolean_decomposition(fa1)
    arrays2, idxs2, states2 = boolean_decomposition(fa2)
    len1 = len(states1)
    len2 = len(states2)
    symbols3 = fa1.symbols.intersection(fa2.symbols)
    states3 = [None] * (len1 * len2)
    for i in range(len1):
        for j in range(len2):
            states3[i * len2 + j] = State((states1[i], states2[j]))
    fa3 = EpsilonNFA()

    for i in fa1.final_states:
        for j in fa2.final_states:
            fa3.add_final_state(states3[idxs1[i] * len2 + idxs2[j]])

    for i in fa1.start_states:
        for j in fa2.start_states:
            fa3.add_start_state(states3[idxs1[i] * len2 + idxs2[j]])

    for symb in symbols3:
        bool_array = sparse.kron(arrays1[symb], arrays2[symb])
        from_idx, to_idx = bool_array.nonzero()
        for i in range(len(to_idx)):
            fa3.add_transition(states3[from_idx[i]], symb, states3[to_idx[i]])

    return fa3


def all_pair_rpq_from_graph(
    bd_graph: MultiDiGraph, query: fa.Regex, start_states=None, final_states=None
):
    """Executes a regular query to `bd`. The transitive closure of the intersection of the logical representation `bd` and `query` is used.

    Parameters
    ----------
    bd: `networkx.MultiDiGraph`
        A finite automaton with the specified start and final States
    query: `pyformlang.regular_expression.Regex`
        Query regular expression
    start_states: iterable
        Numbers of nodes in the graph that will be marked as the initial states of the automaton. By default, all vertices are marked.
    final_states: iterable
        Numbers of nodes in the graph that will be marked as the final states of the automaton. By default, all vertices are marked.

    Returns
    -------
    result: Set[`pyformlang.finite_automaton.State`, `pyformlang.finite_automaton.State`]
        Unique pairs of start and final States of `bd` that are connected by a path from `query`.
    """
    fa_bd = fa.build_nfa_from_graph(bd_graph, start_states, final_states)
    return start_final_states_rpq(fa_bd, query)


def start_final_states_rpq(bd: EpsilonNFA, query: fa.Regex):
    """Executes a regular query to `bd`. The transitive closure of the intersection of the logical representation `bd` and `query` is used.

    Parameters
    ----------
    bd: `~pyformlang.finite_automaton.EpsilonNFA`
        A finite automaton with the specified start and final States
    query: `pyformlang.regular_expression.Regex`
        Query regular expression

    Returns
    -------
    result: Set[`pyformlang.finite_automaton.State`, `pyformlang.finite_automaton.State`]
        Unique pairs of start and final States of `bd` that are connected by a path from `query`.
    """
    intersect = intersection(bd, fa.build_minimal_dfa_from_regex(query))
    arrays, _, states = boolean_decomposition(intersect)
    array: array_type = reduce(
        lambda a, b: a + b,
        arrays.values(),
        array_type((len(states), len(states)), dtype=bool),
    )

    trans_closure = array + array @ array
    a = array.count_nonzero()
    b = trans_closure.count_nonzero()
    while array.count_nonzero() != trans_closure.count_nonzero():
        array = trans_closure
        trans_closure = array + array @ array

    result = set()
    from_idx, to_idx = trans_closure.nonzero()
    for i in range(len(from_idx)):
        from_state = states[from_idx[i]].value[0]
        to_state = states[to_idx[i]].value[0]
        if from_state in bd.start_states:
            if to_state in bd.final_states:
                result.add((from_state, to_state))
    return result
