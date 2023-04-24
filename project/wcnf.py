"""
A module for converting context-free grammar to weakened Chomsky normal form
"""
from pyformlang.cfg import CFG


def to_wcnf(_cfg: CFG) -> CFG:
    """
    Convert context-free grammar to weakened Chomsky normal form (WNFX)

    Parameters
    ----------
    _cfg: ~`pyformlang.cfg.CFG`
        Any context free grammar

    Returns
    -------
    w_cfg: ~`pyformlang.cfg.CFG`
        The cfg in weakened Chomsky normal form (WNFX)
    """
    w_cfg = _cfg.eliminate_unit_productions()
    w_cfg = w_cfg.remove_useless_symbols()
    new_productions = w_cfg._get_productions_with_only_single_terminals()
    new_productions = w_cfg._decompose_productions(new_productions)
    w_cfg = CFG(start_symbol=w_cfg._start_symbol, productions=set(new_productions))
    return w_cfg


def wcnf_from_file(path: str) -> CFG:
    """
    Read context free grammar from file `path` and convert it into WNFX

    Parameters
    ----------
    path: str
        Path to file with cfg

    Returns
    -------
    cfg: ~`pyformlang.cfg.CFG`
        The cfg in weakened Chomsky normal form (WNFX)
    """
    with open(path) as src:
        _cfg = CFG.from_text(src.read())
        return to_wcnf(_cfg)
