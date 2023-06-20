import pytest

from antlr4 import InputStream, CommonTokenStream
from project.Lagraph.Interpreter import InterpretingVisitor
from project.Lagraph.Types import *
from project.antlr_out.Lagraph.LagraphLexer import LagraphLexer
from project.antlr_out.Lagraph.LagraphParser import LagraphParser
from project import fa_utils as ufa

edges = [
    ("s1", "a", "s2"),
    ("s2", "b", "s3"),
    ("s2", "c", "s4"),
    ("s5", "d", "s6"),
]


def get_visitor(script: str) -> InterpretingVisitor:
    input_stream = InputStream(script)
    lexer = LagraphLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LagraphParser(stream)
    tree = parser.prog()
    visitor = InterpretingVisitor()
    visitor.visit(tree)
    return visitor


def do_get_expr(operator: str, start=None, final=None):
    path = "tmp/graph1.dot"
    prepare_graph(path)
    name_gr = "gr"
    set_name = "set_name"
    script = f'let {name_gr} = loadFrom path "{path}"\n'
    if start is not None:
        script += f"let {name_gr} = setStart {start} to {name_gr}\n"
    if final is not None:
        script += f"let {name_gr} = setFinal {final} to {name_gr}\n"
    script += f"let {set_name} = {operator} {name_gr}\n"
    visitor = get_visitor(script)

    return visitor.mem.get_val(set_name)


def prepare_graph(path: str):
    x = EpsilonNFA()
    x.add_transitions(edges)
    x.add_start_state("s1")
    x.add_final_state("s4")
    x.add_final_state("s3")

    x.write_as_dot(path)


def test_startOf():
    assert do_get_expr("startOf", start='{"s1"}') == {"s1"}


def test_finalOf():
    assert do_get_expr("finalOf", final='{"s4", "s3"}') == {"s4", "s3"}


def test_reachableOf():
    assert do_get_expr("reachableOf", start='{"s1"}', final='{"s4", "s3"}') == {
        "s3",
        "s4",
    }


def test_verticesOf():
    assert do_get_expr("verticesOf") == {"s1", "s2", "s3", "s4", "s5", "s6"}


def test_edgesOf():
    assert do_get_expr("edgesOf") == set(edges)


def test_labelsOf():
    assert do_get_expr("labelsOf") == {"a", "b", "c", "d"}


def test_binary_operation():
    x = EpsilonNFA()
    edges_x = [
        ("s1", "a", "s2"),
        ("s2", "b", "s3"),
    ]
    x.add_transitions(edges_x)
    x.write_as_dot("tmp/x.dot")
    y = EpsilonNFA()
    edges_y = [
        ("s1", "f", "s5"),
        ("s5", "e", "s6"),
    ]
    y.add_transitions(edges_y)
    y.write_as_dot("tmp/y.dot")

    script = f"""
    let x = loadFrom path "tmp/x.dot"
    let y = loadFrom path "tmp/y.dot"
    let x = setStart {{"s1"}} to x
    let x = setFinal {{"s3"}} to x
    let y = setStart {{"s1"}} to y
    let y = setFinal {{"s6"}} to y
    let union = x || y
    let concat = x ++ y
    let intersect = x && y
    """

    visitor = get_visitor(script)
    union: EpsilonNFA = visitor.mem.get_val("union")
    assert union.start_states == {(1, "s1"), (2, "s1")}
    assert union.final_states == {(1, "s3"), (2, "s6")}
    concat: EpsilonNFA = visitor.mem.get_val("concat")
    assert concat.start_states == {"s1"}
    assert concat.final_states == {"s6"}
    intersect: EpsilonNFA = visitor.mem.get_val("intersect")
    assert intersect.start_states == {("s1", "s1")}
    assert intersect.final_states == {("s3", "s6")}
