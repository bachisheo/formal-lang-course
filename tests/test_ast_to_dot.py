import pytest
from networkx import MultiDiGraph
from project.Lagraph.utils import parse_from, to_graph, Node
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
    prnt = Node("print", 2)
    set_start = Node("set_start", 3)
    gr = MultiDiGraph(
        [
            ("program", prnt, 0),
            (prnt, set_start),
            (set_start, "a", 0),
            (set_start, "graph_x", 1),
        ]
    )
    ast = to_graph(parse_from("print setStart a to graph_x"))
    assert is_eq(gr, ast)


def test_expr_get_stmt():
    prnt = Node("print", 2)
    get_start = Node("get_starts", 3)
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
    vars = Node("var_list", 3)

    gr = MultiDiGraph(
        [
            ("program", prnt, 0),
            (prnt, map),
            (map, lmb, 0),
            (lmb, vars, 0),
            (vars, "x", 0),
            (lmb, "12", 1),
            (map, "eee", 1),
        ]
    )
    ast = to_graph(parse_from("print map (\\ x -> 12) on eee"))
    assert is_eq(gr, ast)
