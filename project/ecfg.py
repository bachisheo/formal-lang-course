"""
A module for calculations with Extended Context-Free Grammar
"""
from typing import Set, Dict
from pyformlang.cfg import CFG, Variable
from pyformlang.regular_expression import Regex


class ECFG:
    """Representation of Extended Context-Free Grammar"""

    def __init__(self, productions, start_symbol=Variable("S")):
        self._start_symbol = start_symbol
        self._productions = productions

    @staticmethod
    def from_cfg(cfg: CFG) -> "ECFG":
        """Convert Context Free Grammar to Extended Context-Free Grammar

        Parameters
        ----------
        cfg: ~`pyformlang.cfg.CFG`
            Context free grammar

        Returns
        -------
        cfg: `ECFG`
            Extended Context-Free Grammar"""
        return ECFG.from_text(cfg.to_text(), cfg.start_symbol)

    @staticmethod
    def from_file(path: str) -> "ECFG":
        """Read context free grammar from file `path` and convert it into ECFG

        Parameters
        ----------
        path: str
            path to file with Context Free Grammar

        Returns
        -------
        cfg: `ECFG`
            Extended Context-Free Grammar"""
        with open(path) as src:
            return ECFG.from_text(src.read())

    @staticmethod
    def from_text(text: str, start_symbol: Variable = Variable("S")) -> "ECFG":
        """
        Parses a string of context-free grammar rules in the form of 'A -> BCD'
        and returns an ECFG object.

        Parameters
        ----------
        text: `str`
        a string containing context-free grammar rules
        start_symbol: `~pyformlang.cfg.Variable`
        the start symbol of the grammar

        Returns
        ----------
        An ECFG object representing the parsed grammar
        """
        variables: Set[Variable] = set()
        productions: Dict[Variable, Regex] = {}
        for prod in text.splitlines():
            prod = prod.strip()
            if not prod:
                continue

            prod_values = prod.split("->")
            if len(prod_values) != 2:
                raise Exception(f"Invalid production {prod} encountered twice")

            head = Variable(prod_values[0].strip(" "))
            if head in variables:
                raise Exception(f"Production for not terminal {head} encountered twice")

            variables.add(head)
            productions[head] = Regex(prod_values[1])

        return ECFG(productions, start_symbol)

    def __str__(self):
        res = ""
        for sym, regex in self._productions.items():
            res += f"{sym}-> {str(regex)}\n"
        return res
