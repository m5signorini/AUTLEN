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

    """automaton: FiniteAutomaton
    automaton_minimized: FiniteAutomaton
    evaluator: FiniteAutomatonEvaluator
    evaluator_deterministic: FiniteAutomatonEvaluator

    @abstractmethod
    def _create_automata(self) -> FiniteAutomaton:
        pass

    def setUp(self) -> None:
        
        self.automaton = self._create_automata()
        self.evaluator = FiniteAutomatonEvaluator(self.automaton)
        self.automaton_minimized = self.automaton.to_minimized()
        self.evaluator_deterministic = FiniteAutomatonEvaluator(self.automaton_deterministic)"""

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


if __name__ == '__main__':
    unittest.main()
