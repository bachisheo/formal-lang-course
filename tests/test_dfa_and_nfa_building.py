import pytest
import networkx as nx

# on import will print something from __init__ file
from project import dfa_and_nfa_building as bfa
from project import graph_utils as gu


@pytest.mark.parametrize(
    "regex_str, accepts_true, accepts_false, edge_num",
    [("a b c|d", "abc", "abcd", 4), ("a (b | c) k |d", "ack", "abc", 5)],
)
def test_dfa_from_regex_building(regex_str, accepts_true, accepts_false, edge_num):
    regex = bfa.Regex(regex_str)
    dfa = bfa.build_minimal_dfa_from_regex(regex)
    assert dfa.is_deterministic()
    assert dfa.get_number_transitions() == edge_num
    assert dfa.accepts(accepts_true)
    assert dfa.accepts(accepts_false) == False


@pytest.mark.parametrize(
    "nodes1, nodes2",
    [
        (3, 4),
        (4, 8),
    ],
)
def test_nfa_from_two_cycle_graph_building(nodes1: int, nodes2: int):
    graph = gu.generate_two_cycles_graph(nodes1, nodes2, ("label1", "label2"))
    nfa = bfa.build_nfa_from_graph(graph)
    assert nfa.symbols == {"label1", "label2"}
    assert nfa.accepts(["label1", "label1"])
    assert nfa.accepts(["label1", "label1", "label1", "label2"])
    assert len(nfa.start_states) == nodes1 + nodes2 + 1
    assert len(nfa.final_states) == nodes1 + nodes2 + 1


@pytest.mark.parametrize(
    "graph_name",
    [
        ("skos"),
        ("wc"),
        ("travel"),
        ("univ"),
        ("atom"),
    ],
)
def test_nfa_from_named_cycle_graph_building(graph_name: str):
    graph = gu.load_graph_by_name(graph_name)
    nfa = bfa.build_nfa_from_graph(graph)
    assert nfa.symbols == gu.unique_labels(graph)
    assert len(nfa.start_states) == graph.number_of_nodes()
    assert len(nfa.final_states) == graph.number_of_nodes()
