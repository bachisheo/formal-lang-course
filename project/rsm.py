"""
A module for calculations with Recursive State Machine
"""

from typing import Dict
from project.ecfg import ECFG

from pyformlang.finite_automaton import EpsilonNFA, Symbol
from pyformlang.regular_expression import Regex

from project.fa_utils import boolean_decomposition


class RSM:
    """
    Representation of Recursive State Machine
    """

    def __init__(
        self,
        transitions: Dict[Symbol, EpsilonNFA] = {},
        start_symbol: Symbol = None,
    ):
        """
        Initializes an instance of the RSM class.

        Parameters
        ----------
        transitions : dict of pyformlang.finite_automaton.EpsilonNFA
            The transitions of the RSM. The keys are the symbols that can be followed
            from the start state.
        start_state : set of pyformlang.finite_automaton.Symbol, optional
            The start state of the RSM. If not specified, the default start state is an empty set.
        """
        self._transitions = transitions
        self._start_symbol = start_symbol

    def to_matrix(self) -> Dict[Symbol, "BooleanDecomposition"]:
        """
        Returns a dictionary with the Boolean decompositions of the NFA of each symbol.

        Returns
        -------
        dict of Symbol : BooleanDecomposition
            A dictionary where the keys are the symbols and the values are their Boolean decompositions.
        """
        return {
            sym: boolean_decomposition(nfa) for sym, nfa in self._transitions.items()
        }

    def minimize(self) -> "RSM":
        """
        Returns a new RSM that is the minimized version of the current one.

        Returns
        -------
        RSM
            Minimized version of RSM
        """
        min_transitions = {
            non_term: fa.minimize() for non_term, fa in self._transitions.items()
        }
        return RSM(min_transitions, self._start_symbol)

    @staticmethod
    def from_ecfg(grammar: ECFG) -> "RSM":
        """
        Constructs an RSM from an ECFG.

        Parameters
        ----------
        grammar : ECFG
            The ECFG that the RSM is constructed from.

        Returns
        -------
        RSM
            An RSM instance constructed from the given ECFG.
        """
        transitions = {
            symbol: regex.to_epsilon_nfa()
            for symbol, regex in grammar._productions.items()
        }
        return RSM(transitions, grammar._start_symbol)

    @staticmethod
    def from_file(path: str) -> "RSM":
        """
        Constructs an RSM from an ECFG file.

        Parameters
        ----------
        path : str
            The path of the ECFG file.

        Returns
        -------
        RSM
            An RSM instance constructed from the given ECFG file.
        """
        return RSM.from_ecfg(ECFG.from_file(path))

    @staticmethod
    def from_string_ecfg(ecfg: str) -> "RSM":
        """
        Constructs an RSM from an ECFG string.

        Parameters
        ----------
        ecfg : str
            The ECFG string.

        Returns
        -------
        RSM
            An RSM instance constructed from the given ECFG string.
        """
        return RSM.from_ecfg(ECFG.from_text(ecfg))

    def __getitem__(self, item) -> EpsilonNFA:
        return self._transitions[item]

    def __str__(self):
        res = ""
        for symb, nfa in self._transitions:
            res += f"{symb}: {nfa.to_str()}"
        return res
