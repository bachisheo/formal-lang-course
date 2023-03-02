from pyformlang.regular_expression import Regex
import pyformlang.finite_automaton as fa
from networkx import MultiDiGraph


def build_minimal_dfa_from_regex(reg: Regex) -> fa.DeterministicFiniteAutomaton:
    nfa = reg.to_epsilon_nfa()
    nfa.minimize()
    dfa = nfa.to_deterministic()
    return dfa


def build_nfa_from_graph(
    graph: MultiDiGraph, start_states=None, final_states=None
) -> fa.NondeterministicFiniteAutomaton:
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
