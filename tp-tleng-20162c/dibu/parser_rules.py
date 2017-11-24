# coding=utf-8
from dibu.exceptions import SyntacticException
from lexer_rules import tokens
from expressions import *

start = 'program'


def p_program_1(subexpressions):
    """program : code_line program"""
    program = subexpressions[2]
    code_line = subexpressions[1]
    program.add(code_line)
    subexpressions[0] = program


def p_program_empty(subexpressions):
    """program : """
    subexpressions[0] = Program()


def p_code_line(subexpressions):
    """code_line : identifier parameters"""
    parameters = subexpressions[2]
    identifier = subexpressions[1]
    subexpressions[0] = CodeLine(identifier, parameters)


def p_identifier(subexpressions):
    """identifier : SIZE
                 | RECTANGLE
                 | LINE
                 | CIRCLE
                 | ELLIPSE
                 | POLYLINE
                 | POLYGON
                 | TEXT"""
    subexpressions[0] = subexpressions[1]


def p_parameters(subexpressions):
    """parameters : param_name EQUAL literal parameters_list"""
    parameter_name = subexpressions[1]
    literal = subexpressions[3]
    parameter_list = subexpressions[4]

    subexpressions[0] = parameter_list + [Parameter(parameter_name, literal)]


def p_parameter_list(subexpressions):
    """parameters_list : COMMA parameters"""
    parameters_list = subexpressions[2]
    subexpressions[0] = parameters_list


def p_empty_parameter_list(subexpressions):
    """parameters_list : """
    subexpressions[0] = []


def p_param_name(subexpressions):
    """param_name : HEIGHT
                  | WIDTH
                  | SIZE
                  | UPPER_LEFT
                  | FROM
                  | TO
                  | RADIUS
                  | CENTER
                  | RX
                  | RY
                  | POINTS
                  | T
                  | AT
                  | FONT_FAMILY
                  | FONT_SIZE
                  | FILL
                  | STROKE
                  | STROKE_WIDTH
                  | STYLE"""
    subexpressions[0] = subexpressions[1]


def p_literal(subexpressions):
    """literal : NUMBER
                  | POINT
                  | list
                  | STRING
                     """
    subexpressions[0] = subexpressions[1]

def p_list(subexpressions):
    """list : L_SQUARE_BRACKET list_items R_SQUARE_BRACKET"""
    subexpressions[0] = subexpressions[2]


def p_list_items(subexpressions):
    """list_items : literal COMMA list_items"""
    subexpressions[0] = [subexpressions[1]] + subexpressions[3]


def p_list_items_one(subexpressions):
    """list_items : literal"""
    subexpressions[0] = [subexpressions[1]]


def p_list_items_empty(subexpressions):
    """list_items : """
    subexpressions[0] = []


def p_error(subexpressions):
    if subexpressions:
        raise SyntacticException("Error: no se esperaba el token '%s' (línea %s posición %s)" %
                          (subexpressions.value, subexpressions.lexer.lineno, subexpressions.lexer.lexpos))
    else:
        raise SyntacticException("Final del input inesperado")
