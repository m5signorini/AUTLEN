import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
from typing import AbstractSet

from grammar.grammar import Grammar
from grammar.utils import GrammarFormat


class TestFollow(unittest.TestCase):
    def _check_follow(
        self,
        grammar: Grammar,
        symbol: str,
        follow_set: AbstractSet[str],
    ) -> None:
        with self.subTest(string=f"Follow({symbol}), expected {follow_set}"):
            computed_follow = grammar.compute_follow(symbol)
            self.assertEqual(computed_follow, follow_set)

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
        self._check_follow(grammar, "E", {'$', ')'})
        self._check_follow(grammar, "T", {'$', ')', '+'})
        self._check_follow(grammar, "X", {'$', ')'})
        self._check_follow(grammar, "Y", {'$', ')', '+'})

    def test_case2(self) -> None:
        """Test Case 2."""
        grammar_str = """
        E -> TX
        X -> +TX
        X ->  
        T -> FY
        Y -> *FY
        Y -> 
        F -> (E)
        F -> i
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "E", {'$', ')'})
        self._check_follow(grammar, "X", {'$', ')'})
        self._check_follow(grammar, "T", {'+','$', ')'})
        self._check_follow(grammar, "Y", {'$', ')', '+'})
        self._check_follow(grammar, "F", {'$', ')', '+','*'})

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
        self._check_follow(grammar, "A", {'$', 'a'})
        self._check_follow(grammar, "B", {'c', 'd', 'e'})
        self._check_follow(grammar, "C", {'c', 'd', 'e'})
        self._check_follow(grammar, "D", {'$', 'a'})


if __name__ == '__main__':
    unittest.main()
