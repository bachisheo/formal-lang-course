import pytest
import project.fa_utils as fa
from pyformlang.finite_automaton import EpsilonNFA, State
from project import fa_utils as my_fa
from networkx import MultiDiGraph
import project.tensor as rpq


@pytest.mark.parametrize(
    "fa1_regex, fa2_regex",
    [
        (my_fa.PythonRegex("(a b)*"), my_fa.PythonRegex("a b")),
        (my_fa.PythonRegex("(a b)* | (c d x)"), my_fa.PythonRegex("x")),
        (my_fa.PythonRegex("(a b)*"), my_fa.PythonRegex("a b a a b")),
        (my_fa.PythonRegex("(a b)*"), my_fa.PythonRegex("a b a b a b")),
    ],
)
def test_intersection(fa1_regex, fa2_regex):
    fa1 = my_fa.build_minimal_dfa_from_regex(fa1_regex)
    fa2 = my_fa.build_minimal_dfa_from_regex(fa2_regex)
    intersect = fa1.get_intersection(fa2)
    my_intersect = fa.intersection(fa1, fa2)
    assert intersect.is_equivalent_to(my_intersect)


@pytest.mark.parametrize(
    "reg1, reg2, correct_word",
    [
        (my_fa.PythonRegex("(ab)*"), my_fa.PythonRegex("ab"), "ab"),
        (my_fa.PythonRegex("(ab)*"), my_fa.PythonRegex("abababab"), "abababab"),
        (my_fa.PythonRegex("(ab|cdx)*"), my_fa.PythonRegex("(cdxab)*"), "cdxabcdxab"),
    ],
)
def test_intersection_acception(reg1, reg2, correct_word):
    fa1 = my_fa.build_minimal_dfa_from_regex(reg1)
    fa2 = my_fa.build_minimal_dfa_from_regex(reg2)
    my_intersect = fa.intersection(fa1, fa2)
    assert my_intersect.accepts(correct_word)


@pytest.mark.parametrize(
    "q_regex, reachable_node_count",
    [
        (my_fa.PythonRegex("(ab)*"), 1),
        (my_fa.PythonRegex("(ab)* | (ac)"), 2),
        (my_fa.PythonRegex("(a)*"), 0),
    ],
)
def test_rpq_with_one_start_state(q_regex, reachable_node_count):
    states = [State("st"), State("mid"), State("fin1"), State("fin2")]
    bd = EpsilonNFA()
    bd.add_start_state(states[0])
    bd.add_final_state(states[2])
    bd.add_final_state(states[3])
    bd.add_transition(states[0], "a", states[1])
    bd.add_transition(states[1], "b", states[2])
    bd.add_transition(states[1], "c", states[3])

    result = rpq.start_final_states_rpq(bd, q_regex)
    assert len(result) == reachable_node_count


def test_empty_fa_rpq():
    states = [State("a"), State("b")]
    bd = EpsilonNFA()
    for state in states:
        bd.add_start_state(state)
        bd.add_final_state(state)
    result = rpq.start_final_states_rpq(bd, my_fa.PythonRegex("ab ba |ba ab"))
    assert len(result) == 0


def test_full_fa_rpq():
    states = [State("a"), State("b")]
    bd = EpsilonNFA()
    for state in states:
        bd.add_start_state(state)
        bd.add_final_state(state)
    bd.add_transition(states[0], "a", states[1])
    bd.add_transition(states[1], "b", states[0])
    result = rpq.start_final_states_rpq(bd, my_fa.PythonRegex("(a|b)*"))
    assert len(result) == len(bd.states) ** 2
    for start in bd.start_states:
        for final in bd.final_states:
            assert (start, final) in result


@pytest.mark.parametrize(
    "q_regex, reachable_node_count",
    [
        (my_fa.PythonRegex("(ab)*"), 1),
        (my_fa.PythonRegex("(ab)* | (ac)"), 2),
        (my_fa.PythonRegex("(a)*"), 0),
    ],
)
def test_rpq_with_one_start_state_graph(q_regex, reachable_node_count):
    bd = MultiDiGraph(
        [(0, 1, {"label": "a"}), (1, 2, {"label": "b"}), (1, 3, {"label": "c"})]
    )
    result = rpq.all_pair_rpq_from_graph(
        bd, q_regex, start_states=[0], final_states=[2, 3]
    )
    assert len(result) == reachable_node_count


def test_empty_intersect_with_graph_rpq():
    bd = MultiDiGraph()
    bd.add_nodes_from([0, 1])
    result = rpq.all_pair_rpq_from_graph(
        bd, my_fa.PythonRegex("ab ba |ba ab"), [1], [0]
    )
    assert len(result) == 0


def test_full_graph_rpq():
    bd = MultiDiGraph([(0, 1, {"label": "a"}), (1, 0, {"label": "b"})])
    result = rpq.all_pair_rpq_from_graph(bd, my_fa.PythonRegex("(a|b)*"))
    assert len(result) == len(bd.nodes()) ** 2
    for start in bd.nodes():
        for final in bd.nodes():
            assert (start, final) in result
