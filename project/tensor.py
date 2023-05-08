from project import fa_utils as fa
from pyformlang.finite_automaton import EpsilonNFA
from functools import reduce
from networkx import MultiDiGraph


def all_pair_rpq_from_graph(
    bd_graph: MultiDiGraph, query: fa.Regex, start_states=None, final_states=None
):
    """Executes a regular query to `bd`. The transitive closure of the intersection of the logical representation
      `bd` and `query` is used.

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
    """Executes a regular query to `bd`. The transitive closure of the intersection
    of the logical representation `bd` and `query` is used.

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
    intersect = fa.intersection(bd, fa.build_minimal_dfa_from_regex(query))
    arrays, _, states = fa.boolean_decomposition(intersect)
    array: fa.array_type = reduce(
        lambda a, b: a + b,
        arrays.values(),
        fa.array_type((len(states), len(states)), dtype=bool),
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
