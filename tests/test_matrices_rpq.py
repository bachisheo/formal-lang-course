import pytest
import project
from pyformlang.cfg import Variable, CFG
from project import graph_utils as gu
import project.cfqp as cfqp
from networkx import MultiDiGraph

simple_cfg_text = """
    S -> A N
    N -> B C
    A -> a
    B -> b
    C -> c
    """


def test_all_pair_rpq():
    gr = MultiDiGraph(
        [
            (0, 1, {"label": "a"}),
            (1, 2, {"label": "b"}),
            (2, 3, {"label": "c"}),
            (1, 2, {"label": "d"}),
        ]
    )

    cfg = CFG.from_text(simple_cfg_text)

    expected = {
        (0, Variable("A"), 1),
        (1, Variable("B"), 2),
        (2, Variable("C"), 3),
        (1, Variable("N"), 3),
        (0, Variable("S"), 3),
    }
    res = cfqp.all_pairs_rpq(cfqp.RPQMethods.Matrix, gr, cfg)
    assert expected == res


def test_from_text():
    gr = MultiDiGraph(
        [
            (0, 1, {"label": "a"}),
            (1, 2, {"label": "b"}),
            (2, 3, {"label": "c"}),
            (1, 2, {"label": "d"}),
        ]
    )

    expected = {
        (0, Variable("A"), 1),
        (1, Variable("B"), 2),
        (2, Variable("C"), 3),
        (1, Variable("N"), 3),
        (0, Variable("S"), 3),
    }
    res = cfqp.all_pair_rpq_text(cfqp.RPQMethods.Matrix, gr, simple_cfg_text)
    assert expected == res


def test_with_non_terms():
    gr = MultiDiGraph(
        [(0, 1, {"label": "a"}), (1, 2, {"label": "b"}), (2, 3, {"label": "c"})]
    )

    cfg = CFG.from_text(
        """
    S -> B C
    B -> b
    C -> c"""
    )

    expected = {(1, Variable("B"), 2)}
    res = cfqp.rpq(cfqp.RPQMethods.Matrix, gr, cfg, Variable("B"))
    assert expected == res


def test_with_starts():
    gr = MultiDiGraph(
        [(0, 1, {"label": "a"}), (1, 2, {"label": "b"}), (2, 3, {"label": "c"})]
    )

    cfg = CFG.from_text(simple_cfg_text)

    expected = {(1, Variable("N"), 3), (1, Variable("B"), 2)}
    res = cfqp.rpq(cfqp.RPQMethods.Matrix, gr, cfg, None, [1])
    assert expected == res
