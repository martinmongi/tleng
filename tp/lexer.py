import ply.lex as lex

tokens = (
    'CHARACTER',
    'CARET',
    'UNDERSCORE',
    'SLASH',
    'LBRACE',
    'RBRACE',
    'LPAREN',
    'RPAREN'
)
t_CHARACTER = r'[^\^_/\(\)\{\}]+'
t_CARET = r'\^'
t_UNDERSCORE = r'_'
t_SLASH = r'/'
t_LBRACE = r'\('
t_RBRACE = r'\)'
t_LPAREN = r'\{'
t_RPAREN = r'\}'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

data = '(A^BC^D/E^F_G+H)-I'

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
