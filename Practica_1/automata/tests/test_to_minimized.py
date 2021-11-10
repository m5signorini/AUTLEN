"""Test evaluation of automatas."""
import unittest
from abc import ABC, abstractmethod
from typing import Optional, Type

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from automata.automaton import FiniteAutomaton
from automata.automaton_evaluator import FiniteAutomatonEvaluator
from automata.utils import AutomataFormat, deterministic_automata_isomorphism, write_dot


class TestEvaluatorBase(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _check_to_minimized(
        self,
        automaton: FiniteAutomaton,
        automaton_minimized: FiniteAutomaton,
    ) -> None:
        our_minimized = automaton.to_minimized()
        print(write_dot(automaton_minimized))
        print(write_dot(our_minimized))

        equiv_map = deterministic_automata_isomorphism(automaton_minimized, our_minimized)

        self.assertTrue(equiv_map is not None)


    def test_case1(self) -> None:
            """Test Case 1"""
            automaton_str = """
            Automaton:
                Symbols: 01
                q0 final
                q1
                q2 final
                q3
                q4 final
                q5
                --> q0
                q0 -0-> q1
                q0 -1-> q1
                q1 -0-> q2
                q1 -1-> q2
                q2 -0-> q3
                q2 -1-> q3
                q3 -0-> q4
                q3 -1-> q4
                q4 -0-> q5
                q4 -1-> q5
                q5 -0-> q0
                q5 -1-> q0
            """

            automaton = AutomataFormat.read(automaton_str)

            expected_str = """
            Automaton:
                Symbols: 01
                q024 final
                q135
                --> q024
                q024 -0-> q135
                q024 -1-> q135
                q135 -0-> q024
                q135 -1-> q024
            """

            expected = AutomataFormat.read(expected_str)

            self._check_to_minimized(automaton, expected)

    def test_case2(self) -> None:
            """Test Case 2"""
            automaton_str = """
            Automaton:
                Symbols: ab
                q0
                q1 final
                q2
                q3 final
                q4
                --> q0
                q0 -a-> q1
                q0 -b-> q3
                q1 -a-> q2
                q1 -b-> q1
                q2 -a-> q1
                q2 -b-> q2
                q3 -a-> q4
                q3 -b-> q3
                q4 -a-> q3
                q4 -b-> q4
            """

            automaton = AutomataFormat.read(automaton_str)

            expected_str = """
            Automaton:
                Symbols: ab
                q0
                q13 final
                q24
                --> q0
                q0 -a-> q13
                q0 -b-> q13
                q13 -a-> q24
                q13 -b-> q13
                q24 -a-> q13
                q24 -b-> q24
            """

            expected = AutomataFormat.read(expected_str)

            self._check_to_minimized(automaton, expected)

    def test_case3(self) -> None:
                """Test Case 3"""
                automaton_str = """
                Automaton:
                    Symbols: abc
                    A final
                    B final
                    C final
                    D final
                    E
                    --> A
                    A -a-> B
                    A -b-> C
                    A -c-> B
                    B -a-> B
                    B -b-> C
                    B -c-> B
                    C -a-> B
                    C -b-> D
                    C -c-> B
                    D -a-> E
                    D -b-> E
                    D -c-> E
                    E -a-> E
                    E -b-> E
                    E -c-> E
                """

                automaton = AutomataFormat.read(automaton_str)

                expected_str = """
                Automaton:
                    Symbols: abc
                    AB final
                    C final
                    D final
                    E
                    --> AB
                    AB -a-> AB
                    AB -b-> C
                    AB -c-> AB
                    C -a-> AB
                    C -b-> D
                    C -c-> AB
                    D -a-> E
                    D -b-> E
                    D -c-> E
                    E -a-> E
                    E -b-> E
                    E -c-> E
                """

                expected = AutomataFormat.read(expected_str)

                self._check_to_minimized(automaton, expected)

    def test_case4(self) -> None:
                """Test Case 4"""
                automaton_str = """
                Automaton:
                    Symbols: 01
                    A
                    B
                    C final
                    D
                    E
                    F
                    G
                    H
                    --> A
                    A -0-> B
                    A -1-> F
                    B -0-> G
                    B -1-> C
                    C -0-> A
                    C -1-> C
                    D -0-> C
                    D -1-> G
                    E -1-> F
                    E -0-> H
                    F -0-> C
                    F -1-> G
                    G -0-> G
                    G -1-> E
                    H -0-> G
                    H -1-> C
                """

                automaton = AutomataFormat.read(automaton_str)

                expected_str = """
                Automaton:
                    Symbols: 01
                    AE
                    BH
                    F
                    G
                    C final
                    --> AE
                    AE -0-> BH
                    AE -1-> F
                    BH -0-> G
                    BH -1-> C
                    F -0-> C
                    F -1-> G
                    G -0-> G
                    G -1-> AE
                    C -0-> AE
                    C -1-> C
                """

                expected = AutomataFormat.read(expected_str)

                self._check_to_minimized(automaton, expected)

    def test_case5(self) -> None:
                """Test Case 5, example were every state is indistinguishable and final"""
                automaton_str = """
                Automaton:
                    Symbols: 01
                    A final
                    B final
                    C final
                    --> A
                    A -0-> B
                    A -1-> C
                    B -0-> C
                    B -1-> A
                    C -0-> A
                    C -1-> B
                """

                automaton = AutomataFormat.read(automaton_str)

                expected_str = """
                Automaton:
                    Symbols: 01
                    ABC final
                    --> ABC
                    ABC -0-> ABC
                    ABC -1-> ABC
                """

                expected = AutomataFormat.read(expected_str)

                self._check_to_minimized(automaton, expected)


    def test_case6(self) -> None:
                """Test Case 6, example were every state is distinguishable"""
                automaton_str = """
                Automaton:
                    Symbols: 01
                    AE
                    BH
                    F
                    G
                    C final
                    --> AE
                    AE -0-> BH
                    AE -1-> F
                    BH -0-> G
                    BH -1-> C
                    F -0-> C
                    F -1-> G
                    G -0-> G
                    G -1-> AE
                    C -0-> AE
                    C -1-> C
                """

                automaton = AutomataFormat.read(automaton_str)

                expected_str = """
                Automaton:
                    Symbols: 01
                    AE
                    BH
                    F
                    G
                    C final
                    --> AE
                    AE -0-> BH
                    AE -1-> F
                    BH -0-> G
                    BH -1-> C
                    F -0-> C
                    F -1-> G
                    G -0-> G
                    G -1-> AE
                    C -0-> AE
                    C -1-> C
                """

                expected = AutomataFormat.read(expected_str)

                self._check_to_minimized(automaton, expected)

    def test_case7(self) -> None:
                """Test Case 7, example were classes 0 and 1 are in the next iteration just divided in two more classes, we start with 2 and we end with 4 partitions"""
                automaton_str = """
                Automaton:
                    Symbols: 01
                    A
                    B
                    C
                    D
                    E final
                    F final
                    G final
                    H final
                    --> A
                    A -0-> C
                    A -1-> D
                    B -0-> D
                    B -1-> C
                    C -0-> E
                    C -1-> F
                    D -0-> F
                    D -1-> E
                    E -1-> G
                    E -0-> H
                    F -0-> H
                    F -1-> G
                    G -0-> A
                    G -1-> B
                    H -0-> B
                    H -1-> A
                """

                automaton = AutomataFormat.read(automaton_str)

                expected_str = """
                Automaton:
                    Symbols: 01
                    AB
                    CD
                    EF final
                    GH final
                    --> AB
                    AB -0-> CD
                    AB -1-> CD
                    CD -0-> EF
                    CD -1-> EF
                    EF -0-> GH
                    EF -1-> GH
                    GH -0-> AB
                    GH -1-> AB
                """

                expected = AutomataFormat.read(expected_str)

                self._check_to_minimized(automaton, expected)



if __name__ == '__main__':
    unittest.main()
