import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
from typing import AbstractSet

from grammar.grammar import Grammar
from grammar.utils import GrammarFormat

class TestFirst(unittest.TestCase):
    def _check_first(
        self,
        grammar: Grammar,
        input_string: str,
        first_set: AbstractSet[str],
    ) -> None:
        with self.subTest(
            string=f"First({input_string}), expected {first_set}",
        ):
            computed_first = grammar.compute_first(input_string)
            self.assertEqual(computed_first, first_set)

    def test_case1(self) -> None:
        """Test Case 1."""
        grammar_str = """
        E -> TX
        X -> +E
        X ->
        T -> iY
        T -> (E)
        Y -> *T
        Y ->
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "E", {'(', 'i'})
        self._check_first(grammar, "T", {'(', 'i'})
        self._check_first(grammar, "X", {'', '+'})
        self._check_first(grammar, "Y", {'', '*'})
        self._check_first(grammar, "", {''})
        self._check_first(grammar, "Y+i", {'+', '*'})
        self._check_first(grammar, "YX", {'+', '*', ''})
        self._check_first(grammar, "YXT", {'+', '*', 'i', '('})

    def test_case2(self) -> None:
        """Test Case 2."""
        grammar_str = """
        E -> TX
        X -> +TE
        X ->  
        T -> FY
        Y -> *FY
        Y -> 
        F -> (E)
        F -> i
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "E", {'(', 'i'})
        self._check_first(grammar, "X", {'+', ''})
        self._check_first(grammar, "T", {'(', 'i'})
        self._check_first(grammar, "Y", {'*', ''})
        self._check_first(grammar, "F", {'(', 'i'})

    def test_case3(self) -> None:
        """Test Case 3."""
        grammar_str = """
        A -> Aa
        A -> BCD
        B -> b
        B -> 
        C -> c
        C ->
        D -> d
        D -> Ce 
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "A", {'b', 'c', 'd', 'e'})
        self._check_first(grammar, "B", {'b', ''})
        self._check_first(grammar, "C", {'c', ''})
        self._check_first(grammar, "D", {'d', 'c', 'e'})


if __name__ == '__main__':
    unittest.main()
