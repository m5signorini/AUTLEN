"""Evaluation of automata."""
from typing import Set

from automaton import FiniteAutomaton, State
from interfaces import AbstractFiniteAutomatonEvaluator


class FiniteAutomatonEvaluator(
    AbstractFiniteAutomatonEvaluator[FiniteAutomaton, State],
):
    """Evaluator of an automaton."""

    def process_symbol(self, symbol: str) -> None:
        """
        Procesa un símbolo de la cadena (y cualquier número de
        transiciones lambdas inmediatamente después, mediante la llamada a
        _complete_lambdas)
        """

        self._complete_lambdas(self.current_states)
        raise NotImplementedError("This method must be implemented.")

    def _complete_lambdas(self, set_to_complete: Set[State]) -> None:
        """
        Añade al conjunto de estados pasado como argumento
        todos los estados que sean alcanzables mediante un número arbitrario de
        transiciones lambda
        """
        raise NotImplementedError("This method must be implemented.")

    def is_accepting(self) -> bool:
        """
        Indica si la cadena que se ha procesado hasta el momento se
        acepta o no.
        """
        raise NotImplementedError("This method must be implemented.")
