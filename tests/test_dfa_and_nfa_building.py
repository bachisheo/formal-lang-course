import pytest
from networkx import MultiDiGraph
from project import fa_utils as bfa
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
    assert not dfa.accepts(accepts_false)


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


def test_build_nfa_from_graph_all_states():
    graph = MultiDiGraph()
    graph.add_nodes_from(range(0, 5))
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 2, label="b")
    graph.add_edge(1, 3, label="c")
    graph.add_edge(3, 4, label="d")
    f_auto = bfa.build_nfa_from_graph(graph)
    assert f_auto.accepts("ab")
    assert f_auto.accepts("acd")
    assert f_auto.accepts("cd")
    assert f_auto.accepts("ac")
    assert f_auto.accepts("ba") == False
    assert f_auto.accepts("ca") == False
    assert f_auto.accepts("cab") == False
    assert f_auto.accepts("abc") == False


def test_build_nfa_from_graph_set_states():
    graph = MultiDiGraph()
    graph.add_nodes_from(range(0, 5))
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 2, label="b")
    graph.add_edge(1, 3, label="c")
    graph.add_edge(3, 4, label="d")
    f_auto = bfa.build_nfa_from_graph(graph, [0], [2, 4])
    assert f_auto.accepts("ab")
    assert f_auto.accepts("acd")
    assert f_auto.accepts("ac") == False
    assert f_auto.accepts("abc") == False
    assert f_auto.accepts("ba") == False
    assert f_auto.accepts("ca") == False
    assert f_auto.accepts("cab") == False
