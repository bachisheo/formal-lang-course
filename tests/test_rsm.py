import pytest
from project.ecfg import ECFG
from project.rsm import RSM
from project.fa_utils import boolean_decomposition


def test_ecfg_to_rsm():
    ecfg = ECFG.from_text(
        """
    S -> ((A.B)|C)
    C -> (A|c)
    A -> (a|$)
    B -> b"""
    )
    rsm = RSM.from_ecfg(ecfg)
    assert len(rsm._transitions) == len(ecfg._productions)
    assert rsm["S"].accepts("AB")
    assert rsm["C"].accepts("c")
    assert not rsm["S"].accepts("")
    assert rsm["A"].accepts("")


def test_rsm_minimize():
    ecfg = ECFG.from_text(
        """
    S -> ((A.B)|C)
    C -> (A|c)
    A -> (a|$)
    B -> b"""
    )
    rsm = RSM.from_ecfg(ecfg)
    min_rsm = rsm.minimize()
    assert len(min_rsm._transitions) == len(ecfg._productions)
    for nfa in min_rsm._transitions.values():
        min_nfa = nfa.minimize()
        assert min_nfa.is_equivalent_to(nfa)


def test_matrices():
    ecfg = ECFG.from_text(
        """
    S -> (A.B)
    A -> a
    B -> b"""
    )
    rsm = RSM.from_ecfg(ecfg)
    matrices = rsm.to_matrix()
    assert len(matrices) == len(ecfg._productions)
    for sym, mtr in matrices.items():
        mtr2 = boolean_decomposition(rsm[sym])
        assert mtr.idx == mtr2.idx
        assert mtr.arrays.keys() == mtr2.arrays.keys()
        for k in mtr.arrays.keys():
            assert mtr.arrays[k].count_nonzero() == mtr2.arrays[k].count_nonzero()
