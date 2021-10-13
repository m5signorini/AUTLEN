"""Automaton implementation."""
from typing import Collection, Set, Optional, Dict

from automata.interfaces import (
    AbstractFiniteAutomaton,
    AbstractState,
    AbstractTransition,
)


class State(AbstractState):
    """State of an automaton."""

    # You can add new attributes and methods that you think that make your
    # task easier, but you cannot change the constructor interface.
    transitions: Dict[Optional[str], Set['State']]

    def __init__(self, name: str, *, is_final: bool = False) -> None:
        super().__init__(name=name, is_final=is_final)
        self.transitions = {}

    def set_transitions(self, trans: Collection[AbstractTransition]) -> None:
        """
        Create dictionary simulating transitions for this particular state
        """
        for t in trans:
            if t.initial_state == self :
                if t.symbol in self.transitions :
                    # If key 'symbol' exists in the dict update entry
                    self.transitions[t.symbol].add(t.final_state)
                else :
                    # Create new entry
                    self.transitions[t.symbol] = {t.final_state}
        return

    def get_transitions(self, symbol: Optional[str]) -> Set['State']:
        """
        Obtain set of final states reached from this state using the arg symbol.
        """
        return self.transitions.get(symbol, set())

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
        # Add here additional initialization code.

        for s in self.states:
            s.set_transitions(self.transitions)

        # Do not change the constructor interface.
    def _get_lambda_closure(self, set_to_complete: Set[State]) -> None:
        """
        Given a set of states , returns the set of states connected by lambda
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


    def _get_symbol_closure(self, init_states: Collection[State], symbol: str) -> Set[State]:
        """
        Given a set of states and a symbol, obtains the lambda closure of the states
        connected to it by the symbol
        Ex: A -a-> B -None-> C => _get_symbol_closure({A}, a) = {C}
        """
        next_states = set()
        for st in init_states:
            next_states.update(st.get_transitions(symbol))
        self._get_lambda_closure(next_states)
        return next_states

    def _set_is_final_state(self, states: Collection[State]) -> bool:
        """
        Given a set of states returns if it contains a final state
        """
        for st in states:
            if st.is_final:
                return True
        return False


    def to_deterministic(
        self,
    ) -> "FiniteAutomaton":

        # Diccionario que relaciona el nuevo estado con el estado-conj al que se refiere
        nname = 0

        # Obtener nuevo estado inicial como clausura lambda de q0
        # Usamos frozen para que sea hasheable
        q0_set_nonfrozen = set([self.initial_state])
        self._get_lambda_closure(q0_set_nonfrozen)
        q0_set = frozenset(q0_set_nonfrozen)

        q0 = State(name='q'+str(nname), is_final=self._set_is_final_state(q0_set))
        new_states_map = {q0_set: q0}
        new_transitions = set()
        nname += 1

        # Bucle sobre los estado-conjs pendientes
        to_expand_sets = set()
        to_expand_sets.update([q0_set])

        while len(to_expand_sets) > 0:
            expanding_set = to_expand_sets.pop()
            # Bucle sobre los simbolos
            for symbol in self.symbols:
                # Para el simbolo actual obtenemos estado-conj a los que se llega
                qn = frozenset(self._get_symbol_closure(expanding_set, symbol))
                if qn not in new_states_map.keys():
                    # Basta ver que no estaba en el diccionario para añadirlo a to_expand_sets
                    to_expand_sets.add(qn)
                    new_states_map[qn] = State(name='q'+str(nname),is_final=self._set_is_final_state(qn))
                    nname += 1
                    # Añadir transicion desde el estado asociado a expanding_set hasta qn por simbolo
                    new_transitions.add(Transition(initial_state=new_states_map[expanding_set], symbol=symbol, final_state=new_states_map[qn]))
                    
        # Crear nuevo automata
        new_automaton = FiniteAutomaton(states=set(new_states_map.values()),symbols=self.symbols,transitions=new_transitions,initial_state=q0)
        return new_automaton

    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        raise NotImplementedError("This method must be implemented.")
