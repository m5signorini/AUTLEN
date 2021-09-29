"""Automaton implementation."""
from typing import Collection

from interfaces import (
    AbstractFiniteAutomaton,
    AbstractState,
    AbstractTransition,
)


class State(AbstractState):
    """State of an automaton."""

    # You can add new attributes and methods that you think that make your
    # task easier, but you cannot change the constructor interface.
    transitions: dict[Optional[str], Set[State]]

    def __init__(self, name: str, *, is_final: bool = False) -> None:
        super().__init__(name=str, is_final=True)
        self.transitions = {}

    def set_transitions(self, trans: Collection[Transition]) -> None:
        for t in trans:
            if t.initial_state == self :
                if t.symbol in transitions :
                    # If key 'symbol' exists in the dict update entry
                    self.transitions[t.symbol].add(t.final_state)
                else :
                    # Create new entry
                    self.transitions[t.symbol]=t.final_state
        return

    def get_transitions(self,symbol: Optional[str]) -> :
        return transition[symbol]

class Transition(AbstractTransition[State]):
    """Transition of an automaton."""

    # You can add new attributes and methods that you think that make your
    # task easier, but you cannot change the constructor interface.


class FiniteAutomaton(
    AbstractFiniteAutomaton[State, Transition],
):
    """Automaton."""

    def __init__(
        self,
        *,
        initial_state: State,
        states: Collection[State],
        symbols: Collection[str],
        transitions: Collection[Transition],
    ) -> None:
        super().__init__(
            initial_state=initial_state,
            states=states,
            symbols=symbols,
            transitions=transitions,
        )


        state.set_transitions(transitions)
        for i in states:
            i.set_transitions(transitions)
        # Add here additional initialization code.
        # Do not change the constructor interface.

    def to_deterministic(
        self,
    ) -> "FiniteAutomaton":
        raise NotImplementedError("This method must be implemented.")

    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        raise NotImplementedError("This method must be implemented.")
