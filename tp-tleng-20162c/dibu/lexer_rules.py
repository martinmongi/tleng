from dibu.exceptions import SyntacticException

tokens = [
    # METODOS
    'SIZE',
    'RECTANGLE',
    'LINE',
    'CIRCLE',
    'ELLIPSE',
    'POLYLINE',
    'POLYGON',
    'TEXT',

    # VARIABLES
    'UPPER_LEFT',
    'HEIGHT',
    'WIDTH',
    'FROM',
    'TO',
    'CENTER',
    'RADIUS',
    'RX',
    'RY',
    'POINTS',
    'T',
    'AT',
    'STYLE',

    # VARIABLES OPCIONALES
    'FONT_FAMILY',
    'FONT_SIZE',
    'FILL',
    'STROKE',
    'STROKE_WIDTH',

    # PARAMETROS
    'NUMBER',
    'POINT',
    'L_SQUARE_BRACKET',
    'R_SQUARE_BRACKET',
    "STRING",

    "EQUAL",
    "COMMA"

]


def t_error(token):
    message = "Token desconocido:"
    message += "\ntype:" + token.type
    message += "\nvalue:" + str(token.value)
    message += "\nline:" + str(token.lineno)
    message += "\nposition:" + str(token.lexpos)
    raise SyntacticException(message)


def t_NUMBER(token):
    r"""(([0-9]+\.[0-9]+)|([0-9]+\.)|(\.[0-9]+)|([1-9][0-9]+|[0-9]))"""
    if "." in token.value:
        token.value = float(token.value)
    else:
        token.value = int(token.value)
    return token


def t_POINT(token):
    r"\([0-9]+,(\s?)[0-9]+\)"
    token.value = tuple(map(int, token.value[1:-1].split(',')))
    return token


t_L_SQUARE_BRACKET = r"\["
t_R_SQUARE_BRACKET = r"\]"
t_STRING = r'\"([a-z 0-9 , . : = ; -])*\"'
t_EQUAL = r"="
t_COMMA = r","

t_SIZE = r"size"
t_RECTANGLE = r"rectangle"
t_LINE = r"line"
t_CIRCLE = r"circle"
t_ELLIPSE = r"ellipse"
t_POLYLINE = r"polyline"
t_POLYGON = r"polygon"
t_TEXT = r"text"

# VARIABLES
t_UPPER_LEFT = r"upper_left"
t_HEIGHT = r"height"
t_WIDTH = r"width"
t_FROM = r"from"
t_TO = r"to"
t_CENTER = r"center"
t_RADIUS = r"radius"
t_RX = r"rx"
t_RY = r"ry"
t_POINTS = r"points"
t_T = r"t"
t_AT = r"at"
t_STYLE = r"style"

# VARIABLES OPCIONALES
t_FONT_FAMILY = r"font-family"
t_FONT_SIZE = r"font-size"
t_FILL = r"fill"
t_STROKE = r"stroke"
t_STROKE_WIDTH = r"stroke-width"

t_ignore = " \t\n"
