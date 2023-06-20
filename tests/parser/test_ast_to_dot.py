import pytest
from networkx import MultiDiGraph
from project.Lagraph.Parser import Node
from project.Lagraph.parser_utils import parse_from, to_graph
from networkx.drawing.nx_pydot import write_dot, read_dot, to_pydot


def is_eq(g1: MultiDiGraph, g2: MultiDiGraph):
    d1 = to_pydot(g1).to_string()
    d2 = to_pydot(g2).to_string()
    return d1 == d2


def test_empty():
    gr = MultiDiGraph()
    gr.add_node("program")
    ast = to_graph(parse_from(""))
    assert is_eq(gr, ast)


def test_bind_int():
    let = Node("let", 1)
    gr = MultiDiGraph(
        [
            ("program", let, 0),
            (let, "x", "name"),
            (let, "3", "value"),
        ]
    )
    ast = to_graph(parse_from("let x = 3"))
    assert is_eq(gr, ast)


def test_bind():
    let = Node("let", 1)
    gr = MultiDiGraph(
        [
            ("program", let, 0),
            (let, "x", "name"),
            (let, '"strstr"', "value"),
        ]
    )
    ast = to_graph(parse_from('let x = "strstr"'))
    assert is_eq(gr, ast)


def test_print():
    prnt = Node("print", 2)
    gr = MultiDiGraph(
        [
            ("program", prnt, 0),
            (prnt, '"strstr"'),
        ]
    )
    ast = to_graph(parse_from('print "strstr"'))
    assert is_eq(gr, ast)


def test_expr_set_stmt():
    prog = Node("program", 1)
    prnt = Node("print", 2)
    set_start = Node("setStart", 3)
    set_ = Node("set", 4)
    a = Node("a", 5)
    graph = Node("graph_x", 6)
    gr = MultiDiGraph(
        [
            (prog, prnt, 0),
            (prnt, set_start, 0),
            (set_start, set_, 0),
            (set_, a, 0),
            (set_start, graph, 1),
        ]
    )
    ast = to_graph(parse_from("print setStart {a} to graph_x"))
    assert is_eq(gr, ast)


def test_expr_get_stmt():
    prnt = Node("print", 2)
    get_start = Node("startOf", 3)
    gr = MultiDiGraph(
        [
            ("program", prnt, 0),
            (prnt, get_start),
            (get_start, "g"),
        ]
    )
    ast = to_graph(parse_from("print startOf g"))
    assert is_eq(gr, ast)


def test_expr_map():
    prnt = Node("print", 2)
    map = Node("map", 3)
    lmb = Node("lambda", 3)

    gr = MultiDiGraph(
        [
            ("program", prnt, 0),
            (prnt, map),
            (map, lmb, 0),
            (lmb, "x", "variable"),
            (lmb, "12", "expr"),
            (map, "eee", 1),
        ]
    )
    ast = to_graph(parse_from("print map (\\ x -> 12) on eee"))
    assert is_eq(gr, ast)
