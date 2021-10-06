"""Conversion from regex to automata."""
from automata.automaton import FiniteAutomaton, State, Transition
from automata.re_parser_interfaces import AbstractREParser
from typing import Set


class REParser(AbstractREParser):
    """Class for processing regular expressions in Kleene's syntax."""

    def _next_state_name(self) -> str:
        """
        This method obtains the next state name to use, adding one (1)
        to the state_counter attribute. Only used internally
        """
        self.state_counter += 1
        return str(self.state_counter)


    def _create_automaton_empty(
        self,
    ) -> FiniteAutomaton:
        q0 = State(name=self._next_state_name(), is_final=False)
        qf = State(name=self._next_state_name(), is_final=True)

        symbols : Set[str] = set()
        transitions : Set[Transition] = set()
        states = set([q0, qf])

        return FiniteAutomaton(initial_state=q0, states=states, symbols=symbols, transitions=transitions)


    def _create_automaton_lambda(
        self,
    ) -> FiniteAutomaton:
        q0 = State(name=self._next_state_name(), is_final=False)
        qf = State(name=self._next_state_name(), is_final=True)

        # Note that None is only considered in transition.symbol, not in automata.symbols
        symbols : Set[str] = set()
        transitions = set([Transition(initial_state=q0, symbol=None, final_state=qf)])
        states  = set([q0, qf])

        return FiniteAutomaton(initial_state=q0, states=states, symbols=symbols, transitions=transitions)


    def _create_automaton_symbol(
        self,
        symbol: str,
    ) -> FiniteAutomaton:
        q0 = State(name=self._next_state_name(), is_final=False)
        qf = State(name=self._next_state_name(), is_final=True)

        symbols = set([symbol])
        transitions = set([Transition(initial_state=q0, symbol=symbol, final_state=qf)])
        states = set([q0, qf])

        return FiniteAutomaton(initial_state=q0, states=states, symbols=symbols, transitions=transitions)


    def _create_automaton_star(
        self,
        automaton: FiniteAutomaton,
    ) -> FiniteAutomaton:
        q0 = State(name=self._next_state_name(), is_final=False)
        qf = State(name=self._next_state_name(), is_final=True)

        # Note that set() makes a copy of the collection
        symbols = set(automaton.symbols)
        transitions = set(automaton.transitions)
        transitions.update([
            Transition(initial_state=q0, symbol=None, final_state=qf),
            Transition(initial_state=qf, symbol=None, final_state=q0),
            Transition(initial_state=q0, symbol=None, final_state=automaton.initial_state)
        ])
        # Change final states and make transitions to new final state
        for fs in automaton.states:
            if fs.is_final:
                fs.is_final = False
                transitions.add(Transition(initial_state=fs, symbol=None, final_state=qf))

        states = set([q0, qf])
        states.update(automaton.states)

        return FiniteAutomaton(initial_state=q0, states=states, symbols=symbols, transitions=transitions)


    def _create_automaton_union(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        q0 = State(name=self._next_state_name(), is_final=False)
        qf = State(name=self._next_state_name(), is_final=True)

        # Note that set() makes a copy of the collection
        symbols = set(automaton1.symbols)
        symbols.update(automaton2.symbols)

        transitions = set(automaton1.transitions)
        transitions.update(automaton2.transitions)
        transitions.update([
            Transition(initial_state=q0, symbol=None, final_state=automaton1.initial_state),
            Transition(initial_state=q0, symbol=None, final_state=automaton2.initial_state)
        ])
        # Change final states and make transitions to new final state
        for fs in automaton1.states:
            if fs.is_final:
                fs.is_final = False
                transitions.add(Transition(initial_state=fs, symbol=None, final_state=qf))
        for fs in automaton2.states:
            if fs.is_final:
                fs.is_final = False
                transitions.add(Transition(initial_state=fs, symbol=None, final_state=qf))

        states = set([q0, qf])
        states.update(automaton1.states)
        states.update(automaton2.states)

        return FiniteAutomaton(initial_state=q0, states=states, symbols=symbols, transitions=transitions)


    def _create_automaton_concat(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        q0 = State(name=self._next_state_name(), is_final=False)
        qf = State(name=self._next_state_name(), is_final=True)

        # Note that set() makes a copy of the collection
        symbols = set(automaton1.symbols)
        symbols.update(automaton2.symbols)

        transitions = set(automaton1.transitions)
        transitions.update(automaton2.transitions)
        transitions.update([
            Transition(initial_state=q0, symbol=None, final_state=automaton1.initial_state)
        ])
        # Change final states and make transitions to new final state
        for fs in automaton1.states:
            if fs.is_final:
                fs.is_final = False
                transitions.add(Transition(initial_state=fs, symbol=None, final_state=automaton2.initial_state))
        for fs in automaton2.states:
            if fs.is_final:
                fs.is_final = False
                transitions.add(Transition(initial_state=fs, symbol=None, final_state=qf))

        states = set([q0, qf])
        states.update(automaton1.states)
        states.update(automaton2.states)

        return FiniteAutomaton(initial_state=q0, states=states, symbols=symbols, transitions=transitions)
