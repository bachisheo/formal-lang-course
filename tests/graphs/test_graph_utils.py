import pytest
import networkx as nx
from project import graph_utils as gu


def test_saving_to_file():
    path = "tmp.dot"
    num1, num2 = 3, 4
    label1, label2 = "one", "two"
    two_cycle = gu.generate_two_cycles_graph(num1, num2, (label1, label2), path)
    cycle_from_file = nx.nx_pydot.read_dot(path)
    assert two_cycle.number_of_edges() == cycle_from_file.number_of_edges()
    assert gu.unique_labels(two_cycle) == gu.unique_labels(cycle_from_file)


def test_graph_generation():
    num1, num2 = 3, 4
    label1, label2 = "one", "two"
    two_cycle = gu.generate_two_cycles_graph(num1, num2, (label1, label2))
    assert two_cycle.number_of_edges() == (num1 + num2 + 2)
    assert two_cycle.number_of_nodes() == (num1 + num2 + 1)
    assert gu.unique_labels(two_cycle) == {label1, label2}


def test_graph_loading():
    avrora_graph = gu.load_graph_by_name("avrora")
    assert isinstance(avrora_graph, nx.MultiDiGraph)


def test_graph_info():
    avrora_graph = gu.load_graph_by_name("avrora")
    info = gu.graph_info_by_name("avrora")
    assert info.number_of_edges == avrora_graph.number_of_edges()
    assert info.number_of_nodes == avrora_graph.number_of_nodes()
    assert info.labels == gu.unique_labels(avrora_graph)
