"""
A module for calculations with Finite Automaton
"""
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)
from networkx import MultiDiGraph


def build_minimal_dfa_from_regex(reg: Regex) -> DeterministicFiniteAutomaton:
    """
    Builds a minimal deterministic finite automaton (DFA) equivalent to
    the given regular expression `reg`.

    Parameters
    ----------
    reg: ~`pyformlang.regular_expression.Regex`
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
    reg = Regex(reg_str)
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
