"""
A module for calculations with Finite Automaton
"""
from pyformlang.regular_expression import PythonRegex
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    Epsilon,
)
from networkx import MultiDiGraph
from pyformlang.finite_automaton import EpsilonNFA, State
from collections import namedtuple
from scipy import sparse
from scipy.sparse import csc_array as array_type


def build_nfa_from_string(reg_str: str) -> EpsilonNFA:
    """
    Builds a  NFA equivalent to
    the given regular expression in string `reg_str`.
    """
    reg = PythonRegex(reg_str)
    nfa = reg.to_epsilon_nfa()
    return nfa


def build_minimal_dfa_from_regex(reg: PythonRegex) -> DeterministicFiniteAutomaton:
    """
    Builds a minimal deterministic finite automaton (DFA) equivalent to
    the given regular expression `reg`.

    Parameters
    ----------
    reg: ~`pyformlang.regular_expression.PythonRegex`
        pyformlang regular expression object

    Returns
    -------
    dfa: DeterministicFiniteAutomaton
        The minimal DFA equivalent to the regex
    """
    nfa = reg.to_epsilon_nfa()
    return nfa.minimize()


def build_minimal_dfa_from_regex_str(reg_str: str) -> DeterministicFiniteAutomaton:
    """
    Builds a minimal deterministic finite automaton (DFA) equivalent to
    the given regular expression (reg_str) in string.

    Parameters
    ----------
    reg_str: str
        Regular expression in string form

    Returns
    -------
    dfa: `~pyformlang.finite_automaton.DeterministicFiniteAutomaton`
        The minimal DFA equivalent to the regex
    """
    reg = PythonRegex(reg_str)
    return build_minimal_dfa_from_regex(reg)


def build_nfa_from_graph(
    graph: MultiDiGraph, start_states=None, final_states=None
) -> NondeterministicFiniteAutomaton:
    """
    Builds a non-deterministic finite automaton (NFA) from a given networkx graph.

    Parameters
    ----------
    graph : `~networkx.MultiDiGraph`
        The graph representation of the automaton
    start_states: iterable or None
        Nodes in the graph that will be marked as the initial states of the automaton. If None, all vertices are marked.
    final_states: iterable or None
        Nodes in the graph that will be marked as the final states of the automaton. If None, all vertices are marked.

    Returns
    -------
    nfa : `~pyformlang.finite_automaton.NondeterministicFiniteAutomaton~
        An epsilon non-deterministic finite automaton read from the graph
    """
    nfa = NondeterministicFiniteAutomaton.from_networkx(graph)
    if start_states is None:
        start_states = graph.nodes()
    if final_states is None:
        final_states = graph.nodes()

    for st in start_states:
        nfa.add_start_state(st)
    for st in final_states:
        nfa.add_final_state(st)
    return nfa


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
    f_auto = f_auto.remove_epsilon_transitions()
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


def union(first_fa: EpsilonNFA, second_fa: EpsilonNFA) -> EpsilonNFA:
    """
    Union of two EpsilonNFA.
    """
    fa = EpsilonNFA()

    for from_, symb, to in first_fa:
        fa.add_transition(from_.value, symb, to.value)

    for from_, symb, to in second_fa:
        fa.add_transition(from_.value, symb, to.value)

    for s1 in first_fa.start_states:
        fa.add_start_state((1, s1.value))

    for s2 in second_fa.start_states:
        fa.add_start_state((2, s2.value))

    for s1 in first_fa.final_states:
        fa.add_final_state((1, s1.value))

    for s2 in second_fa.final_states:
        fa.add_final_state((2, s2.value))

    return fa


def concatenation(first_fa: EpsilonNFA, second_fa: EpsilonNFA) -> EpsilonNFA:
    """
    Concatenation of two EpsilonNFA.
    """
    fa = EpsilonNFA()

    for from_, symb, to in first_fa:
        fa.add_transition(from_.value, symb, to.value)

    for from_, symb, to in second_fa:
        fa.add_transition(from_.value, symb, to.value)

    for st1 in first_fa.start_states:
        fa.add_start_state(st1.value)

        for s2 in second_fa.final_states:
            fa.add_transition(st1.value, Epsilon(), s2.value)

    for st2 in second_fa.final_states:
        fa.add_final_state(st2.value)

    return fa
