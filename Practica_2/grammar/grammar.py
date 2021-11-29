#from __future__ import annotations

from collections import deque
from typing import AbstractSet, Collection, MutableSet, Optional
from typing import Union, List

class RepeatedCellError(Exception):
    """Exception for repeated cells in LL(1) tables."""

class SyntaxError(Exception):
    """Exception for parsing errors."""

class Production:
    """
    Class representing a production rule.

    Args:
        left: Left side of the production rule. It must be a character
            corresponding with a non terminal symbol.
        right: Right side of the production rule. It must be a string
            that will result from expanding ``left``.

    """

    def __init__(self, left: str, right: str) -> None:
        self.left = left
        self.right = right

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.left == other.left
            and self.right == other.right
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.left!r} -> {self.right!r})"
        )

    def __hash__(self) -> int:
        return hash((self.left, self.right))

class Grammar:
    """
    Class that represent a grammar.

    Args:
        terminals: Terminal symbols of the grammar.
        non_terminals: Non terminal symbols of the grammar.
        productions: Production rules of the grammar.
        axiom: Axiom of the grammar.

    """

    def __init__(
        self,
        terminals: AbstractSet[str],
        non_terminals: AbstractSet[str],
        productions: Collection[Production],
        axiom: str,
    ) -> None:
        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        if axiom not in non_terminals:
            raise ValueError(
                "Axiom must be included in the set of non terminals.",
            )

        for p in productions:
            if p.left not in non_terminals:
                raise ValueError(
                    f"{p}: "
                    f"Left symbol {p.left} is not included in the set "
                    f"of non terminals.",
                )
            if p.right is not None:
                for s in p.right:
                    if (
                        s not in non_terminals
                        and s not in terminals
                    ):
                        raise ValueError(
                            f"{p}: "
                            f"Invalid symbol {s}.",
                        )

        self.terminals = terminals
        self.non_terminals = non_terminals
        self.productions = productions
        self.productions_aux = productions.copy()
        self.axiom = axiom

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"axiom={self.axiom!r}, "
            f"productions={self.productions!r})"
        )


    def compute_first(self, sentence: str) -> AbstractSet[str]:
        """
        Method to compute the first set of a string.

        Args:
            str: string whose first set is to be computed.

        Returns:
            First set of str.
        """

        sentence_firsts = set()
        i = 0

        if sentence != "":
            letter = sentence[i]
        else:
            letter = sentence
        if letter in self.terminals:
            sentence_firsts.add(letter)
            return sentence_firsts
        elif letter in self.non_terminals:
            for prod in self.productions:
                if prod.left == letter:
                    if prod.right != "" and prod.right[0] != letter:
                        sentence_firsts = sentence_firsts.union(self.compute_first(prod.right))
                    elif prod.right == "":
                        i+=1
                        if len(sentence) > i:
                           sentence_firsts = sentence_firsts.union(self.compute_first(sentence[i]))
                           while "" in sentence_firsts:
                            i+=1
                            sentence_firsts.remove("")
                            if len(sentence) > i:
                                sentence_firsts = sentence_firsts.union(self.compute_first(sentence[i]))
                            elif len(sentence) == i:
                                sentence_firsts.add("")
                            else:
                                sentence_firsts.add("")
                                break
                        elif len(sentence) == i:
                            sentence_firsts.add("")
        elif letter == "":
            sentence_firsts.add("")

        return sentence_firsts

    def check_for_loops(self, symbol, previous_symbol) -> Collection[Production]:
        aux = self.productions.copy()

        for prod in self.productions:
            if symbol in prod.right:
                i = prod.right.index(symbol)
                if prod.right[i+1:] == "" and prod.left == previous_symbol:
                    aux.remove(prod)

        return aux


    def compute_follow(self, symbol: str) -> AbstractSet[str]:
        """
        Method to compute the follow set of a non-terminal symbol.

        Args:
            symbol: non-terminal whose follow set is to be computed.

        Returns:
            Follow set of symbol.
        """

	# TO-DO: Complete this method for exercise 4...
        symbol_follow = set()

        if symbol == self.productions[0].left:
            symbol_follow.add("$")

        for prod in self.productions_aux:
            if symbol in prod.right:
                i = prod.right.index(symbol)
                symbol_follow = symbol_follow.union(self.compute_first(prod.right[i+1:]))
                if "" in symbol_follow:
                    symbol_follow.remove("")
                    if symbol != prod.left and symbol != symbol_follow:
                        self.productions_aux = self.check_for_loops(prod.left, symbol)
                        symbol_follow = symbol_follow.union(self.compute_follow(prod.left))
                        self.productions_aux = self.productions

        return symbol_follow

    """
    def remove_left_ll1_indirect_recursion(self) -> Collection[Production]:
        non_recursive = self.productions.copy()

        for prod in self.productions():
            if prod.right in prod:
                

        return non_recursive
    """

    def get_ll1_table(self) -> Optional['LL1Table']:
        """
        Method to compute the LL(1) table.

        Returns:
            LL(1) table for the grammar, or None if the grammar is not LL(1).
        """

	# TO-DO: Complete this method for exercise 5...

        cells = []

        for prod in self.productions:
            first = self.compute_first(prod.right)
            for ele in first:
                if ele in self.terminals:
                    cells.append(TableCell(prod.left, ele, prod.right))
                elif ele == "":
                    follow = self.compute_follow(prod.left)
                    if "$" in follow:
                        cells.append(TableCell(prod.left, "$", prod.right))
                    for foll in follow:
                        if foll in self.terminals:
                            cells.append(TableCell(prod.left, foll, prod.right))


        return LL1Table(self.non_terminals, self.terminals.union("$"), cells)



    def is_ll1(self) -> bool:
        return self.get_ll1_table() is not None

class TableCell:
    """
    Cell of a LL1 table.

    Args:
        non_terminal: Non terminal symbol.
        terminal: Terminal symbol.
        right: Right part of the production rule.

    """

    def __init__(self, non_terminal: str, terminal: str, right: str) -> None:
        self.non_terminal = non_terminal
        self.terminal = terminal
        self.right = right

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.non_terminal == other.non_terminal
            and self.terminal == other.terminal
            and self.right == other.right
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.non_terminal!r}, {self.terminal!r}, "
            f"{self.right!r})"
        )

    def __hash__(self) -> int:
        return hash((self.non_terminal, self.terminal))

class ParseTree():
    """
    Parse Tree.

    Args:
        root: root node of the tree.
        children: list of children, which are also ParseTree objects.
    """
    def __init__(self, root: str, children: Collection['ParseTree'] = []) -> None:
        self.root = root
        self.children = children

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.root!r}: {self.children})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.root == other.root
            and len(self.children) == len(other.children)
            and all([x.__eq__(y) for x, y in zip(self.children, other.children)])
        )

    def add_children(self, children: Collection['ParseTree']) -> None:
        self.children = children

class LL1Table:
    """
    LL1 table.

    Args:
        non_terminals: Set of non terminal symbols.
        terminals: Set of terminal symbols.
        cells: Cells of the table.

    """

    def __init__(
        self,
        non_terminals: AbstractSet[str],
        terminals: AbstractSet[str],
        cells: Collection[TableCell],
    ) -> None:

        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        for c in cells:
            if c.non_terminal not in non_terminals:
                raise ValueError(
                    f"{c}: "
                    f"{c.non_terminal} is not included in the set "
                    f"of non terminals.",
                )
            if c.terminal not in terminals:
                raise ValueError(
                    f"{c}: "
                    f"{c.terminal} is not included in the set "
                    f"of terminals.",
                )
            for s in c.right:
                if (
                    s not in non_terminals
                    and s not in terminals
                ):
                    raise ValueError(
                        f"{c}: "
                        f"Invalid symbol {s}.",
                    )

        self.terminals = terminals
        self.non_terminals = non_terminals
        self.cells = {(c.non_terminal, c.terminal): c.right for c in cells}

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"cells={self.cells!r})"
        )

    def add_cell(self, cell: TableCell) -> None:
        """
        Adds a cell to an LL(1) table.

        Args:
            cell: table cell to be added.

        Raises:
            RepeatedCellError: if trying to add a cell already filled.
        """
        if (cell.non_terminal, cell.terminal) in self.cells:
            raise RepeatedCellError(
                f"Repeated cell ({cell.non_terminal}, {cell.terminal}).")
        else:
            self.cells[(cell.non_terminal, cell.terminal)] = cell.right

    def analyze(self, input_string: str, start: str) -> ParseTree:
        """
        Method to analyze a string using the LL(1) table.

        Args:
            input_string: string to analyze.
            start: initial symbol.

        Returns:
            ParseTree object with either the parse tree (if the elective exercise is solved)
            or an empty tree (if the elective exercise is not considered).

        Raises:
            SyntaxError: if the input string is not syntactically correct.
        """

	    # TO-DO: Complete this method for exercise 2...

        # We use a list as if it was a stack
        stack = []
        stack.append("$")

        for ele in start[::-1]:
            tree = ParseTree(ele)
            stack.append((ele, tree))
            if ele == start[-1]:
                root = tree

        # We itter til the last element in the stack is "$"
        while len(stack) != 1:
            top_tuple = stack.pop()

            current_tree = top_tuple[1]
            top = top_tuple[0]

            if top in self.non_terminals and len(input_string):
                first_input = input_string[0]
                if (top, first_input) in self.cells.keys():
                    new_top = self.cells[(top, first_input)]
                    if new_top or new_top == '':
                        children = []
                        if new_top == "":
                            child = ParseTree("λ")
                            children.append(child)
                        for ele in new_top[::-1]:
                            child = ParseTree(ele)
                            children.append(child)
                            stack.append((ele, child))
                        current_tree.add_children(children[::-1])
                    else:
                        raise SyntaxError
                else:
                    raise SyntaxError

            elif top in self.terminals:
                if len(input_string) != 0:
                    if top == input_string[0]:
                        if input_string != "$":
                            input_string = input_string[1:]
                    else:
                        raise SyntaxError
                else:
                    raise SyntaxError
            else:
                raise SyntaxError

        if(len(input_string) != 1):
            raise SyntaxError

        return root # Return an empty tree by default.
