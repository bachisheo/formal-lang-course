import pytest
import project

from antlr4 import InputStream, CommonTokenStream
from project.Lagraph.Interpreter import InterpretingVisitor
from project.Lagraph.Types import *
from project.antlr_out.Lagraph.LagraphLexer import LagraphLexer
from project.antlr_out.Lagraph.LagraphParser import LagraphParser
from project import fa_utils as ufa
from project.graph_utils import load_graph_by_name


def get_visitor(script: str) -> InterpretingVisitor:
    input_stream = InputStream(script)
    lexer = LagraphLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LagraphParser(stream)
    tree = parser.prog()
    visitor = InterpretingVisitor()
    visitor.visit(tree)
    return visitor


def test_bind():
    variables = [
        ("x", "42", 42),
        ("y", '"string value"', "string value"),
    ]

    script = "".join([f"let {name} = {val}\n" for name, val, _ in variables])

    visitor = get_visitor(script)

    for name, _, expected_value in variables:
        expr = visitor.mem.get_val(name)
        assert expr is not None
        assert expr == expected_value


def test_print():
    variables = [
        ("x", "42"),
        ("y", '"some string value"'),
    ]
    outputs = [42, "some string value"]
    script = "".join(
        [f"let {name} = {val}\n print {name}\n" for name, val in variables]
    )
    visitor = get_visitor(script)

    output = "".join([f"{str(val)}\n" for val in outputs])

    assert output == visitor.get_log() + "\n"


def test_print_graph():
    x = EpsilonNFA()
    edges_x = [
        ("s1", "a", "s2"),
        ("s2", "b", "s3"),
    ]
    x.add_transitions(edges_x)
    x.write_as_dot("tmp/x.dot")
    script = """
    let g = loadFrom path "tmp/x.dot"
    print g
    """
    visitor = get_visitor(script)
    graph_view = visitor.get_log()
    assert (
        graph_view
        == 'digraph  {\ns3 [is_final=True, is_start=True, label=s3, peripheries=2];\ns3_starting [height="0.0", label="", shape=None, width="0.0"];\ns1 [is_final=True, is_start=True, label=s1, peripheries=2];\ns1_starting [height="0.0", label="", shape=None, width="0.0"];\ns2 [is_final=True, is_start=True, label=s2, peripheries=2];\ns2_starting [height="0.0", label="", shape=None, width="0.0"];\ns3_starting -> s3  [key=0];\ns1 -> s2  [key=0, label=a];\ns1_starting -> s1  [key=0];\ns2 -> s3  [key=0, label=b];\ns2_starting -> s2  [key=0];\n}\n'
    )


def test_from_regex():
    regex_str = "(ab)* | (cdx)"
    script = f'let gr = fromRegex "{regex_str}"'
    visitor = get_visitor(script)

    expected_nfa = ufa.PythonRegex(regex_str).to_epsilon_nfa()
    x = visitor.mem.get_val("gr")
    assert isinstance(x, FSMType)
    if isinstance(x, EpsilonNFA):
        assert expected_nfa.is_equivalent_to(x.value)


def test_map():
    script = """
    let forty = map (\\x -> 42) on {1, 2, 3, 4}
    """
    visitor = get_visitor(script)
    forty = visitor.mem.get_val("forty")
    assert forty == {42, 42, 42, 42}


def test_filter():
    script = """
    let forty = filter (\\x -> x == 42) on {1, 2, 3, 4, 42}
    """
    visitor = get_visitor(script)
    forty = visitor.mem.get_val("forty")
    assert forty == {42}


def test_in_set():
    script = """
    let s = {"a", "b", "c"}
    let yes =  "a" in s
    let no = "r" in s
    """
    visitor = get_visitor(script)
    assert visitor.mem.get_val("yes") == 1
    assert visitor.mem.get_val("no") == 0


def test_loading():
    x = EpsilonNFA()
    edges_x = [
        ("s1", "a", "s2"),
        ("s2", "b", "s3"),
    ]
    x.add_transitions(edges_x)
    x.write_as_dot("tmp/x.dot")
    y = EpsilonNFA.from_networkx(load_graph_by_name("avrora"))
    script = """
    let x = loadFrom path "tmp/x.dot"
    let y = loadFrom name "avrora"
    """
    visitor = get_visitor(script)
    x_ = visitor.mem.get_val("x").value
    y_ = visitor.mem.get_val("y").value
    assert x.states == x_.states
    assert y.is_equivalent_to(y_)
