# coding=utf-8


"""
Lista de tokens

El analizador léxico de PLY (al llamar al método lex.lex()) va a buscar
para cada uno de estos tokens una variable "t_TOKEN" en el módulo actual.

t_TOKEN puede ser:

- Una expresión regular
- Una función cuyo docstring sea una expresión regular (bizarro).

En el segundo caso, podemos hacer algunas cosas "extras", como quedarnos
con algún valor de ese elemento.

"""
from ply.lex import lex

import lexer_rules


class Applier(object):
    def apply(self, string):
        u"""Aplica el análisis léxico al string dado."""
        lexer.input(string)

        return list(lexer)


# Build the lexer
lexer = lex(module=lexer_rules)
Applier().apply("size height=200, width=200 rectangle upper_left=(0,0), size=(50, 50), fill=\"red\" rectangle upper_left=(100,0), size=(50, 50) rectangle upper_left=(50,50), size=(50, 50) rectangle upper_left=(150,50), size=(50, 50) rectangle upper_left=(0,100), size=(50, 50) rectangle upper_left=(100,100), size=(50, 50) rectangle upper_left=(50,150), size=(50, 50) rectangle upper_left=(150,150), size=(50, 50)")
