from ast import Tuple
import cfpq_data as cd
import networkx as nx
from collections import namedtuple

GraphInfo = namedtuple("GraphInfo", ["number_of_edges", "number_of_nodes", "labels"])


def load_graph_by_name(name: str) -> nx.MultiDiGraph:
    path_to_graph = cd.download(name)
    graph = cd.graph_from_csv(path_to_graph)
    return graph


def graph_info_by_name(name: str) -> GraphInfo:
    graph = load_graph_by_name(name)
    return GraphInfo(
        graph.number_of_edges(), graph.number_of_nodes(), unique_labels(graph)
    )


def unique_labels(graph: nx.MultiDiGraph):
    labels = set()
    for edge_info in graph.edges(data="label"):
        if edge_info:
            labels.add(edge_info[2])
    return labels


def generate_two_cycles_graph(
    edges_number_1: int, edges_number_2: int, labels, path_to_save: str = None
) -> nx.MultiDiGraph:
    graph = cd.labeled_two_cycles_graph(edges_number_1, edges_number_2, labels=labels)
    if path_to_save:
        nx.nx_pydot.write_dot(graph, path_to_save)
    return graph
