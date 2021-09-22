"""
Esta es la expresion regular para el ejercicio 0, que se facilita
a modo de ejemplo:
"""
RE0 = "[a-zA-Z]+"

"""
Completa a continuacion las expresiones regulares para los
ejercicios 1-5:
"""
_except_parenthesis = "[^\(\)]*"
RE1 = "([a-zA-Z]|_|[0-9])+\.py"
RE2 = "-?(((([1-9][0-9]*)|0)(\.[0-9]*)?)|(\.[0-9]+))"
RE3 = "[a-z]+\.[a-z]+@(estudiante\.)?uam\.es"
# Alternativa: ([^\(\)]*\([^\(\)]*\)[^\(\)]*)+
RE4 = "(" + _except_parenthesis + "\(" + _except_parenthesis + "\)" + _except_parenthesis + ")+"

# Alternativa: (([^\(\)]*\([^\(\)]*\)[^\(\)]*)+|[^\(\)]*)
_max_one_parenthesis = "(" + RE4 + "|" + _except_parenthesis + ")"
# Alternativa: ([^\(\)]*\((([^\(\)]*\([^\(\)]*\)[^\(\)]*)+|[^\(\)]*)\)[^\(\)]*)+
RE5 = "(" + _except_parenthesis + "\(" + _max_one_parenthesis + "\)" + _except_parenthesis + ")+"

"""
Recuerda que puedes usar el fichero prueba.py para probar tus
expresiones regulares.
"""

"""
EJERCICIO 6:
Incluye a continuacion, dentro de esta cadena, tu respuesta
al ejercicio 6.

Para poder crear dicha expresión regular habría que poder tener en cuenta un número
arbitrariamente grande de posibles niveles de anidación, lo cual implicaría que la
expresión regular tendría que ser arbitrariamente larga para lo cual no hay espacio
físico suficiente.

"""
