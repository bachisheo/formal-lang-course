from pyformlang.regular_expression import Regex
import pyformlang.finite_automaton as fa
from networkx import MultiDiGraph


def build_minimal_dfa_from_regex(reg: Regex) -> fa.DeterministicFiniteAutomaton:
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


def build_nfa_from_graph(
    graph: MultiDiGraph, start_states=None, final_states=None
) -> fa.NondeterministicFiniteAutomaton:
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
    states = {x: fa.State(x) for x in graph.nodes()}
    nfa = fa.NondeterministicFiniteAutomaton.from_networkx(graph)
    if start_states == None:
        start_states = states
    if final_states == None:
        final_states = states

    for st in start_states.values():
        nfa.add_start_state(st)
    for st in final_states.values():
        nfa.add_final_state(st)
    return nfa
