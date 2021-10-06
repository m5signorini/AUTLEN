"""Evaluation of automata."""
from typing import Set

from automata.automaton import FiniteAutomaton, State
from automata.interfaces import AbstractFiniteAutomatonEvaluator


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
        # Important: Do not modify self.current_states, instead assign it
        # a new set of states to avoid changing old_states from evaluator

        if symbol not in self.automaton.symbols:
            raise ValueError

        new_current_states = set()
        for s in self.current_states:
            new_current_states.update(s.get_transitions(symbol))

        self._complete_lambdas(new_current_states)
        self.current_states = new_current_states
        return

    def _complete_lambdas(self, set_to_complete: Set[State]) -> None:
        """
        Añade al conjunto de estados pasado como argumento
        todos los estados que sean alcanzables mediante un número arbitrario de
        transiciones lambda
        """
        # Auxiliary set of already expanded states and expected to expand
        expanded_states = set()
        to_expand_states = set()
        to_expand_states.update(set_to_complete)

        while len(to_expand_states) > 0:
            # Completing lambdas doesnt need an specific order (random with pop)
            check_state = to_expand_states.pop()
            expanded_states.add(check_state)
            # Expand check_state
            for linked in check_state.get_transitions(None):
                # Avoid potential infinite loops
                if linked not in expanded_states:
                    to_expand_states.add(linked)  # No need to check duplicates

        set_to_complete.update(expanded_states)
        return

    def is_accepting(self) -> bool:
        """
        Indica si la cadena que se ha procesado hasta el momento se
        acepta o no.
        """
        for s in self.current_states:
            if s.is_final:
                return True
        return False
