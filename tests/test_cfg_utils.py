import pytest
import project  # on import will print something from __init__ file
from pyformlang.cfg import CFG, Production
from project import cfg_utils as cu


def setup_module(module):
    print("basic setup module")


def teardown_module(module):
    print("basic teardown module")


def assert_equal(cfg_text1: str, cfg_text2: str) -> bool:
    def to_set(str):
        return {line.strip() for line in str.splitlines() if line.strip() != ""}

    assert to_set(cfg_text1) == to_set(cfg_text2)


def test_simple():
    cfg_text = """
    S -> A B
    A -> a
    B -> b"""
    cfg = CFG.from_text(cfg_text)
    wh_cfg = cu.to_wcnf(cfg)
    assert_equal(cfg_text, wh_cfg.to_text())


def test_unit_productions():
    cfg_text = """
    S -> A B | C
    C -> A
    A -> a
    B -> b"""
    whnf_cfg_text = """
    S -> A B
    S -> a
    A -> a
    B -> b"""
    wh_cfg = cu.to_wcnf(CFG.from_text(cfg_text))
    assert_equal(whnf_cfg_text, wh_cfg.to_text())


def test_single_terminals():
    cfg_text = " S -> a b c "
    whnf_cfg_text = """
    S -> "VAR:a#CNF#" C#CNF#1
    C#CNF#1 -> "VAR:b#CNF#" "VAR:c#CNF#"
    b#CNF# -> b
    a#CNF# -> a
    c#CNF# -> c
    """
    wh_cfg = cu.to_wcnf(CFG.from_text(cfg_text))
    assert_equal(whnf_cfg_text, wh_cfg.to_text())


def test_long_productions():
    cfg_text = """
    S -> A B C D
    A -> a
    B -> b
    C -> c
    D -> d
    """
    whnf_cfg_text = """
    S -> A C#CNF#1
    A -> a
    C#CNF#1 -> B C#CNF#2
    C#CNF#2 -> C D
    D -> d
    B -> b
    C -> c
   """
    wh_cfg = cu.to_wcnf(CFG.from_text(cfg_text))
    assert_equal(whnf_cfg_text, wh_cfg.to_text())


def test_non_generating_symbols():
    cfg_text = """
    S -> A B | C
    A -> a
    C -> D
    B -> b"""
    whnf_cfg_text = """
    S -> A B
    A -> a
    B -> b"""
    wh_cfg = cu.to_wcnf(CFG.from_text(cfg_text))
    assert_equal(whnf_cfg_text, wh_cfg.to_text())


def test_non_reachable_symbols():
    cfg_text = """
    S -> A B
    A -> a
    D -> d
    B -> b"""
    whnf_cfg_text = """
    S -> A B
    A -> a
    B -> b"""
    wh_cfg = cu.to_wcnf(CFG.from_text(cfg_text))
    assert_equal(whnf_cfg_text, wh_cfg.to_text())


def test_useless_symbols():
    cfg_text = """
    S -> A B | C
    A -> a
    D -> C C
    D -> d A
    B -> b"""
    whnf_cfg_text = """
    S -> A B
    A -> a
    B -> b"""
    wh_cfg = cu.to_wcnf(CFG.from_text(cfg_text))
    assert_equal(whnf_cfg_text, wh_cfg.to_text())


def test_from_file():
    fname = "test.txt"
    cfg_text = """
    S -> A B | C
    A -> a
    D -> C C
    D -> d A
    B -> b"""
    whnf_cfg_text = """
    S -> A B
    A -> a
    B -> b"""
    with open(fname, "w") as f:
        f.write(cfg_text)
    cfg = cu.wcnf_from_file(fname)
    assert_equal(cfg.to_text(), whnf_cfg_text)
