from time import sleep

import ply.yacc as yacc
from IPython.core.display import SVG, display_svg

from dibu import parser_rules
# from .lexer_rules import tokens
from xml.dom.minidom import parseString as xmlParse

from ply.lex import lex

from dibu import lexer_rules
from svgwrite import *


def parse(str):
    """Dado un string, me lo convierte a SVG."""
    lexer = lex(module=lexer_rules)
    parser = yacc.yacc(module=parser_rules)
    abstract_syntax_tree = parser.parse(str, lexer)

    return abstract_syntax_tree.evaluate()


if __name__ == '__main__':
    # Build the parser
    lexer = lex(module=lexer_rules)
    parser = yacc.yacc(module=parser_rules)
    text = 'rectangle upper_left=(0,0), size=(200, 200), fill="yellow" ' \
           'polygon points=[(0,0), (50, 50), (0, 100)], style="stroke: black; stroke-width: 3; fill: none;" ' \
           'polygon points=[(0,0), (50, 50), (100, 0)], style="stroke: black; stroke-width: 3; fill: none;" ' \
           'polygon points=[(0, 100), (50, 150), (0, 200)], style="stroke: black; stroke-width: 3; fill: none;" ' \
           'polygon points=[(0, 200), (50, 150), (100, 200)], style="stroke: black; stroke-width: 3; fill: none;" ' \
           'polygon points=[(100, 200), (150, 150), (200, 200)], style="stroke: black; stroke-width: 3; fill: none;" ' \
           'polygon points=[(200, 200), (150, 150), (200, 100)], style="stroke: black; stroke-width: 3; fill: none;" ' \
           'polygon points=[(200, 100), (150, 50), (200, 0)], style="stroke: black; stroke-width: 3; fill: none;" ' \
           ' ' \
           'polygon points=[(200, 0), (150, 50), (100, 0)], style="stroke: black; stroke-width: 3; fill: none;" ' \
           'line to=(0, 100), from=(25, 50)' \
           'circle center=(100,100), radius=20' \
           'polyline points=[(200, 100), (150, 50), (200, 0)]' \
           'ellipse center=(100,100), rx=20, ry=20, stroke="black", stroke-width=3' \
           'text t="esto es un texto", at=(10, 20)' \
           'text t="esto es un texto", at=(10, 20), font-family="bakbatn", font-size="12"' \
           'size height=100, width=100'

    abstract_syntax_tree = parser.parse(text, lexer)
    result = abstract_syntax_tree.evaluate()
    print(result)

    pretty_xml = xmlParse(result).toprettyxml()
    print(pretty_xml)
