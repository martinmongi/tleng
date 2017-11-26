import ply.lex as lex

tokens = (
    'CHAR',
    'CARET',
    'UNDERSCORE',
    'SLASH',
    'LBRACE',
    'RBRACE',
    'LPAREN',
    'RPAREN'
)
t_CHAR = r'[^\^_/\(\)\{\}]'
t_CARET = r'\^'
t_UNDERSCORE = r'_'
t_SLASH = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = '\t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()