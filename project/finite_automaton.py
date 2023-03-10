from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import (
    State,
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)
from networkx import MultiDiGraph


def build_minimal_dfa_from_regex(reg: Regex) -> DeterministicFiniteAutomaton:
    """Transforms the regular expression into an minimal DFA

    Parameters
    ----------
    reg: Regex
        pyformlang regular expression

    Returns
    -------
    dfa: DeterministicFiniteAutomaton
        The minimal DFA equivalent to the regex
    """
    nfa = reg.to_epsilon_nfa()
    return nfa.minimize()


def build_minimal_dfa_from_regex_str(reg_str: str) -> DeterministicFiniteAutomaton:
    """Transforms the regular expression into an minimal DFA

    Parameters
    ----------
    reg_str: str
        regular expression in string

    Returns
    -------
    dfa: DeterministicFiniteAutomaton
        The minimal DFA equivalent to the regex
    """
    reg = Regex(str)
    return build_minimal_dfa_from_regex(reg)


def build_nfa_from_graph(
    graph: MultiDiGraph, start_states=None, final_states=None
) -> NondeterministicFiniteAutomaton:
    """Convert a networkx graph into an finite state automaton

    Parameters
    ----------
    graph : MultiDiGraph
        The graph representation of the automaton
    start_states: iterable
        Numbers of nodes in the graph that will be marked as the initial states of the automaton. By default, all vertices are marked.
    final_states: iterable
        Numbers of nodes in the graph that will be marked as the final states of the automaton. By default, all vertices are marked.

    Returns
    -------
    nfa : NondeterministicFiniteAutomaton
       An epsilon nondeterministic finite automaton read from the graph
    """
    states = {x: State(x) for x in graph.nodes()}
    nfa = NondeterministicFiniteAutomaton.from_networkx(graph)
    if start_states == None:
        start_states = states
    if final_states == None:
        final_states = states

    for st in start_states.values():
        nfa.add_start_state(st)
    for st in final_states.values():
        nfa.add_final_state(st)
    return nfa
