# Ejemplo
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import ast
import inspect
from ast_utils import ASTRemoveConstantIf, ASTDotVisitor

def my_fun(p):
    if True:
        return 1
    else:
        return 0

source = inspect.getsource(my_fun)
my_ast= ast.parse(source)

if_remover= ASTRemoveConstantIf()
new_ast= if_remover.visit(my_ast)

dot_visitor = ASTDotVisitor()
dot_visitor.visit(new_ast)
