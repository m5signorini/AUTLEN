"""Automaton implementation."""
from typing import Collection, Set, Optional, Dict
from typing_extensions import final

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
                if qn not in new_states_map.keys() and len(qn)>0 :
                    # Basta ver que no estaba en el diccionario para añadirlo a to_expand_sets
                    to_expand_sets.add(qn)
                    new_states_map[qn] = State(name='q'+str(nname),is_final=self._set_is_final_state(qn))
                    nname += 1
                    # Añadir transicion desde el estado asociado a expanding_set hasta qn por simbolo
                if len(qn)>0:
                    new_transitions.add(Transition(initial_state=new_states_map[expanding_set], symbol=symbol, final_state=new_states_map[qn]))

        # Crear nuevo automata
        new_automaton = FiniteAutomaton(states=set(new_states_map.values()),symbols=self.symbols,transitions=new_transitions,initial_state=q0)
        return new_automaton


    def to_minimized(
        self,
    ) -> "FiniteAutomaton":

        # Inicializar nuevo automata

        # Crear lista de equivalencia Q/E0 segun equivalencia por cadenas de longitud 0

        # Bucle hasta que Q/Ei+1 = Q/Ei

        def get_state_by_name(states: Collection[State], name: str) -> Optional[State]:
            """
            """
            for st in states:
                if st.name == name:
                    return st
            return None

        def get_class_list(d: Dict[State, int], clase: int) -> Collection[State]:
            """
            """
            states = []
            for st in d.keys():
                if d[st] == clase:
                    states.append(st)
            return states

        def compare_state_transition_classes(d: Dict[State, int], s1: State, s2: State) -> bool:
            """
            """
            # First we generate the list for the elements that are from the same class as s1

            for smb in self.symbols:
                # tr are sets of states
                tr1 = s1.get_transitions(smb)
                tr2 = s2.get_transitions(smb)
                for st1 in tr1:
                    for st2 in tr2:
                        if d[st1] != d[st2]:
                            return False
            return True


        # Vamos a eliminar estado innaccesibles del automata

        # Lo primero que hacemos es generar el set de estados inaccesibles, ahora debemos eliminarlos del automata
        accesible_aux = [self.initial_state]
        #accesible_aux.add(self.initial_state)
        marked = set()

        while len(accesible_aux) > 0 :
            st = accesible_aux.pop()
            for sym in st.transitions.keys():
                aux = st.transitions[sym].pop()
                st.transitions[sym].add(aux)
                if aux not in marked:
                    accesible_aux.append(aux)
            marked.add(st)


        # Los eliminamos del automata
        self.states = marked

        #Tambien eliminamos todas las transiciones que tienen este, como estado inicial
        transitions_aux = list(self.transitions)
        for tr in self.transitions:
            if tr.initial_state not in self.states or tr.final_state not in self.states:
                transitions_aux.remove(tr)
        self.transitions = transitions_aux

        # Dada la lista de clases Q/Ei, para obtener Q/Ei+1:
        # 1) Hallar inicio de clase
        # 2) Por cada elemento de la misma clase, se comprueba con cada simbolo
        #    de alfabeto que la transicion lleva a un estado de la misma clase
        #    en Q/Ei
        # 3) Si no, no sigue en la misma clase. En otro caso, se mantiene la clase
        # 4) Repetir para todos los estados de la misma clase partiendo del inicial

        
        Q_0 = dict()
        Q_1 = dict()

        # Inicializamos Q0 segun si los estados son finales (1) iniciales (0)
        for st in self.states:
            if st.is_final:
                Q_0[st] = 1
            else:
                Q_0[st] = 0

        clases = list(set(Q_0.values()))
        while Q_0 != Q_1:
            Q_1 = dict()
            unclassed = list(Q_0.keys())
            # Identificar inicio de clase
            # Marcar estados que mantienen clases
            for cl in clases:
                class_list = get_class_list(Q_0, cl)
                for st in class_list:
                    if compare_state_transition_classes(Q_0, class_list[0], st):
                        Q_1[st] = cl
                        unclassed.remove(st)
            # Para los estados que cambian de clase:
            while len(unclassed) > 0:
                # Crear nueva clase
                clases.append(clases[-1]+1)
                max_clase = clases[-1]
                repr = unclassed.pop(0)
                Q_1[repr] = max_clase
                # Comprobar para los que quedan sin clase
                for st in unclassed[:]:
                    if Q_0[st] == Q_0[repr]:
                        if compare_state_transition_classes(Q_0, st, repr):
                            Q_1[st] = max_clase
                            unclassed.remove(st)
            Q_0, Q_1 = Q_1, Q_0
            # Para los que no pertenecen a una clase ya existente, vamos creando nuevas
            # Observacion: seguro que no pertenecen a otra clase distinta ya existente
        
        final_initial_state = None
        init_cl = Q_0[self.initial_state]

        # Creamos conjunto nuevo de estados
        final_states = set()
        for cl in clases:
            states = get_class_list(Q_0, cl)
            repres = states[0]
            new_state = State(str(cl), is_final=repres.is_final)
            final_states.add(new_state)
            if cl == init_cl:
                final_initial_state = new_state
        
        
        # Creamos conjunto nuevo de transiciones
        final_transitions = set()
        for st in final_states:
            cl = int(st.name)
            states = get_class_list(Q_0, cl)
            repres = states[0]
            for symbol in self.symbols:
                next_sts = repres.get_transitions(symbol)
                # Nos fijamos en uno cualquiera, ya que el automata se
                # presupone ya determinista
                for nst in next_sts:
                    next_cl = Q_0[nst]
                    break
                final_transitions.add(Transition(st, symbol, get_state_by_name(final_states, str(next_cl))))

        new_automaton = FiniteAutomaton(states=final_states, symbols=self.symbols, transitions=final_transitions, initial_state=final_initial_state)
        return new_automaton

