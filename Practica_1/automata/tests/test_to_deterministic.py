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
from automata.utils import AutomataFormat, is_deterministic, write_dot

DOT_PATH = os.path.join(os.path.join(os.path.dirname(__file__), "."), "dot_files")

class TestToDeterministicBase(ABC, unittest.TestCase):
    """Base class for to_deterministic tests"""

    automaton: FiniteAutomaton
    automaton_deterministic: FiniteAutomaton
    evaluator: FiniteAutomatonEvaluator
    evaluator_deterministic: FiniteAutomatonEvaluator

    @abstractmethod
    def _create_automata(self) -> FiniteAutomaton:
        pass

    def setUp(self) -> None:
        """Set up the tests."""
        self.automaton = self._create_automata()
        self.evaluator = FiniteAutomatonEvaluator(self.automaton)
        self.automaton_deterministic = self.automaton.to_deterministic()
        self.evaluator_deterministic = FiniteAutomatonEvaluator(self.automaton_deterministic)

    def _check_accept_body(
        self,
        string: str,
        should_accept: bool = True,
    ) -> None:
        accepted = self.evaluator.accepts(string)
        accepted_deterministic = self.evaluator_deterministic.accepts(string)
        self.assertEqual(accepted, should_accept)
        self.assertEqual(accepted_deterministic, should_accept)

    def _check_accept(
        self,
        string: str,
        should_accept: bool = True,
        exception: Optional[Type[Exception]] = None,
    ) -> None:

        with self.subTest(string=string):
            if exception is None:
                self._check_accept_body(string, should_accept)
            else:
                with self.assertRaises(exception):
                    self._check_accept_body(string, should_accept)
    
    def _check_is_deterministic(
        self,
    ) -> None:
        """ Check if self.automaton_deterministic is in fact deterministic """
        self.assertEqual(
            is_deterministic(self.automaton_deterministic),
            True
        )

class TestToDetFixedStrings(TestToDeterministicBase):
    """
    Test for accepting fixed strings.

    Both self.automaton and self.automaton_deterministic should
    accept the same fixed strings.
    Here we test that the evaluations for different strings
    matches between both versions of the Automata.
    """

    def _create_automata(self) -> FiniteAutomaton:

        description = """
        Automaton:
            Symbols: Tiburon

            Empty
            T
            Ti
            Tib
            Tibu
            Tibur
            Tiburo
            Tiburon final

            --> Empty
            Empty -T-> T
            T -i-> Ti
            Ti -b-> Tib
            Tib -u-> Tibu
            Tibu -r-> Tibur
            Tibur -o-> Tiburo
            Tiburo -n-> Tiburon
        """

        return AutomataFormat.read(description)

    def test_fixed(self) -> None:
        """Test for a fixed string."""
        self._check_is_deterministic()
        self._check_accept("Tiburon", should_accept=True)
        self._check_accept("Tib", should_accept=False)
        self._check_accept(" Tibu", exception=ValueError)
        self._check_accept("iborun", should_accept=False)
        self._check_accept("", should_accept=False)
        self._check_accept("TiburonT", should_accept=False)
        self._check_accept("a", exception=ValueError)
        self._check_accept("Tiburona", exception=ValueError)

        with open(os.path.join(DOT_PATH, 'test1_to_det.txt'), 'w+') as f:
            f.write(write_dot(self.automaton))
            f.write(write_dot(self.automaton_deterministic))


class TestToDetBasicND(TestToDeterministicBase):
    """
    Test basic non-deterministic automata.

    Here we test if an automata with a state with
    multiple transitions for the same symbol gets
    correctly converted.
    """
    def _create_automata(self) -> FiniteAutomaton:

        description = """
        Automaton:
            Symbols: ab

            1
            2
            3
            4
            5
            6 final

            --> 1
            1 -a-> 2
            1 -a-> 3
            2 -b-> 4
            3 -a-> 5
            5 --> 6
            4 --> 6
        """
        return AutomataFormat.read(description)

    def test_result(self) -> None:
        """ Test if deterministic and same """
        self._check_is_deterministic()
        self._check_accept("ab", should_accept=True)
        self._check_accept("aa", should_accept=True)
        self._check_accept("a", should_accept=False)
        self._check_accept("b", should_accept=False)
        self._check_accept("ba", should_accept=False)
        self._check_accept("bb", should_accept=False)
        self._check_accept("", should_accept=False)
        self._check_accept("aab", should_accept=False)
        self._check_accept("aaa", should_accept=False)
        self._check_accept("aba", should_accept=False)
        self._check_accept("abb", should_accept=False)

        with open(os.path.join(DOT_PATH, 'test2_to_det.txt'), 'w+') as f:
            f.write(write_dot(self.automaton))
            f.write(write_dot(self.automaton_deterministic))

        

class TestToDetLambdasOnly(TestToDeterministicBase):
    """
    Test only lambdas automaton.

    Here we test if the trivial lambda automata
    gets properly converted.
    """
    def _create_automata(self) -> FiniteAutomaton:

        description = """
        Automaton:
            Symbols:

            1
            2 final
            3
            4

            --> 1
            1 --> 2
            2 --> 3
            3 --> 4
            4 --> 2
        """
        return AutomataFormat.read(description)

    def test_lambda_only(self) -> None:
        self._check_is_deterministic()
        self._check_accept("", should_accept=True)
        self._check_accept("a", exception=ValueError)
        with open(os.path.join(DOT_PATH, 'test3_to_det.txt'), 'w+') as f:
            f.write(write_dot(self.automaton))
            f.write(write_dot(self.automaton_deterministic))



class TestToDetMultiple(TestToDeterministicBase):
    """
    Test for making a deterministic automata from
    non-deterministic-lambda automata

    Here we test an automata with multiple final
    states and multiple transitions with the same
    symbol
    """

    def _create_automata(self) -> FiniteAutomaton:

        description = """
        Automaton:
            Symbols: xy

            1
            2
            3
            4 final
            5
            6 final

            --> 1
            1 -x-> 2
            1 -x-> 2
            1 -x-> 2
            1 -x-> 5
            2 -y-> 3
            2 -y-> 1
            3 -y-> 4
            4 --> 5
            1 -x-> 6
        """

        return AutomataFormat.read(description)

    def test_lambda(self) -> None:
        self._check_is_deterministic()
        self._check_accept("xyy", should_accept=True)
        self._check_accept("xyxyy", should_accept=True)
        self._check_accept("xyxx", should_accept=False)
        self._check_accept("y", should_accept=False)
        self._check_accept("x", should_accept=True)
        self._check_accept("", should_accept=False)
        self._check_accept("a", exception=ValueError)
        with open(os.path.join(DOT_PATH, 'test4_to_det.txt'), 'w+') as f:
            f.write(write_dot(self.automaton))
            f.write(write_dot(self.automaton_deterministic))


class TestToDetLoops(TestToDeterministicBase):
    """
    Test for loops in non deterministic.

    Here we test if transitions from one state to
    itself get properly converted.
    """

    def _create_automata(self) -> FiniteAutomaton:

        description = """
        Automaton:
            Symbols: hm

            vacio
            silencio
            asentir
            dudar final
            pensar final
            comprender final
            saborear
            meditar final

            --> vacio
            vacio -h-> silencio
            vacio --> vacio
            silencio -h-> silencio
            silencio -m-> asentir
            asentir -m-> dudar
            dudar -m-> pensar
            pensar -m-> comprender
            comprender -m-> saborear
            saborear -m-> meditar
            meditar -m-> meditar
        """

        return AutomataFormat.read(description)

    def test_loops(self) -> None:
        self._check_is_deterministic()
        self._check_accept("h", should_accept=False)
        self._check_accept("hh", should_accept=False)
        self._check_accept("hhhhhhhhhh", should_accept=False)
        self._check_accept("hm", should_accept=False)
        self._check_accept("hmh", should_accept=False)
        self._check_accept("hmm", should_accept=True)
        self._check_accept("hmmm", should_accept=True)
        self._check_accept("hmmmm", should_accept=True)
        self._check_accept("hmmmmm", should_accept=False)
        self._check_accept("hmmmmmmmmmmmmmmmmmm", should_accept=True)
        self._check_accept("hmmmmmmmmmmmmmmmmmmh", should_accept=False)
        with open(os.path.join(DOT_PATH, 'test5_to_det.txt'), 'w+') as f:
            f.write(write_dot(self.automaton))
            f.write(write_dot(self.automaton_deterministic))


class TestToDetTrivial(TestToDeterministicBase):
    """
    """
    def _create_automata(self) -> FiniteAutomaton:

        description = """
        Automaton:
            Symbols:

            fin final

            --> fin
        """

        return AutomataFormat.read(description)
    
    def test_trivials(self) -> None:
        self._check_is_deterministic()
        self._check_accept("", should_accept=True)
        with open(os.path.join(DOT_PATH, 'test6_to_det.txt'), 'w+') as f:
            f.write(write_dot(self.automaton))
            f.write(write_dot(self.automaton_deterministic))


if __name__ == '__main__':
    unittest.main()
