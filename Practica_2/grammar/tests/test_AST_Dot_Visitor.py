# Ejemplo
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import ast
import inspect
from ast_utils import ASTDotVisitor

def print_next_if_pos(num):
    if num > 0:
        print(num + 1)

source = inspect.getsource(print_next_if_pos)
my_ast = ast.parse(source)
dot_visitor = ASTDotVisitor()
dot_visitor.visit(my_ast)
    # Debería generar este texto dot