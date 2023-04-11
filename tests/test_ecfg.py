import pytest
from project.ecfg import ECFG
from project import cfg_utils as cu
from pyformlang.cfg import CFG, Variable
from pyformlang.regular_expression import Regex


def setup_module(module):
    print("basic setup module")


def teardown_module(module):
    print("basic teardown module")


def assert_equal(cfg_text1: str, cfg_text2: str) -> bool:
    def to_set(str):
        return {
            line.strip().replace(" ", "")
            for line in str.splitlines()
            if line.strip() != ""
        }

    assert to_set(cfg_text1) == to_set(cfg_text2)


def test_from_cfg():
    cfg_text = """
    S -> A B
    A -> a
    B -> b"""
    ecfg_text = """
    S -> (A.B)
    A -> a
    B -> b"""
    cfg = CFG.from_text(cfg_text)
    ecfg = ECFG.from_cfg(cu.to_wcnf(cfg))
    assert_equal(ecfg_text, str(ecfg))


def test_wrong_grammar():
    cfg_text = """
    S -> A
    S -> B
    B -> b"""
    cfg = CFG.from_text(cfg_text)
    with pytest.raises(Exception):
        ECFG.from_cfg(cfg)
    with pytest.raises(Exception):
        ECFG.from_text(cfg_text)


def test_from_text():
    ecfg_text = """
    S -> A B|C
    C -> A|c
    A -> a|$
    B -> b"""
    from_reg_text = """
    S -> ((A.B)|C)
    C -> (A|c)
    A -> (a|$)
    B -> b"""
    ecfg = ECFG.from_text(ecfg_text)
    assert_equal(from_reg_text, str(ecfg))
