from __future__ import annotations

from typing import Collection, Optional
import numbers
import ast
from ast import iter_fields
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


class ASTDotVisitor(ast.NodeVisitor):

    level: int
    n_node: int
    last_parent: Optional[int]
    last_field_name: str

    def __init__(self) -> None:
        self.level = 0
        self.n_node = 0
        self.last_parent: Optional[int] = None
        self.last_field_name = ""
    
    def print_first(self) -> None:
        print("digraph {")
        return 
    
    def print_node_info(self, name, fields) -> None:
        # Imprime un nodo con identificador, argumentos...
        # Ejemplo: s1[label="FunctionDef(name='print_next_if_pos', returns=None)"]
        result = 's{}'.format(self.n_node)
        result += '[label="{}('.format(name)
        # Recorremos campos del nodo primitivos
        num = 0
        for field, value in fields:
            num += 1
            if isinstance(value, str):
                result += "{}='{}'".format(field, value)
            else:
                result += "{}={}".format(field, value)
            if num < len(fields):
                result += ', '
        result += ')"]'
        print(result)
        return

    def print_link(self) -> None:
        # Imprime arista ident -> ident y el nombre de arista
        edge = 's{} -> s{}[label="{}"]'.format(self.last_parent, self.n_node, self.last_field_name)
        print(edge)
        return

    def print_end(self) -> None:
        # Imptime el cierre del .dot
        print("}")
        return
        
    def is_primitive(self, value) -> bool:
        # Devuelve si el valor es un nodo nuevo o un campo
        if isinstance(value, list) or isinstance(value, ast.AST):
            return False
        else:
            return True

    def generic_visit(self, node: ast.AST) -> None:
        # A medida que visita nodos, recopila la informacion
        # necesaria para generar el .dot

        primitives = []

        for field, value in iter_fields(node):
            # Dividir entre campos primitivos y no primitivos
            if self.is_primitive(value):
                primitives.append((field, value))

        # PRE VISITA
        ##############
        # Imprimir nodo actual usando los campos primitivos
        #El primer nodo explorado inicia la impresión del fichero .dot
        if self.level == 0:
            self.print_first()
        else:
            # El nodo raiz no tiene link padre
            self.print_link()
        self.print_node_info(type(node).__name__, primitives)
        this_n_node = self.n_node
        self.level += 1
        self.n_node += 1

        # MID VISITA
        ##############
        # Continuar recorrido del arbol con los no primitivos
        # Default:
        for field, value in iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.last_field_name = field
                        self.last_parent = this_n_node
                        self.visit(item)
            elif isinstance(value, ast.AST):
                self.last_field_name = field
                self.last_parent = this_n_node
                self.visit(value)
        
        # POS VISITA
        ##############
        self.level -= 1

        if self.level == 0:
            self.print_end()
    
    def visit(self, node: ast.AST) -> None:
        # Genera el formato .dot
        # Por defecto visit solo llama al visit
        # correspondiente o a generic_visit si no existe tal
        super().visit(node)