from __future__ import annotations

from typing import Collection
import numbers
import ast
import inspect
#import constant


class ASTMagicNumberDetector(ast.NodeVisitor):

    magic_numbers: int
    non_magic_numbers: Collection[complex]

    def __init__(self) -> None:
        self.magic_numbers = 0
        self.non_magic_numbers = [0, 1, 1j]
    
    def _check_magic_number(self, number: complex) -> None:
        # Modifica self.magic_numbers
        # Comprobamos si es un numerico necesario para el caso Constant
        if isinstance(number, numbers.Number):
            if number not in self.non_magic_numbers:
                self.magic_numbers += 1


    def visit_Num(self, node: ast.Num) -> None:
        # Vease https://greentreesnakes.readthedocs.io/en/latest/nodes.html
        value = node.n
        self._check_magic_number(value)
    
    def visit_Constant(self, node: ast.Constant) -> None:
        value = node.value
        self._check_magic_number(value)