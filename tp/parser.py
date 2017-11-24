import ply.yacc as yacc

# Get the token map from the lexer.
from lexer import tokens

start = 'expression'
def p_expression_slash(p):
    'expression : expression SLASH concat'
    p[0] = "[" + p[1] + " div " + p[3] + "]"

def p_expression_concatenation(p):
    'expression : concat'
    p[0] = p[1]

def p_concat_1(p):
    'concat : concat term'
    p[0] = p[1] + p[2]

def p_concat_2(p):
    'concat : term'
    p[0] = p[1]

def p_term_1(p):
    'term : factor CARET factor'
    p[0] = "[" + p[1] + " super " + p[3] + "]"

def p_term_2(p):
    'term : factor UNDERSCORE factor'
    p[0] = "[" + p[1] + " sub " + p[3] + "]"

def p_term_3(p):
    'term : factor CARET factor UNDERSCORE factor'
    p[0] = "[" + p[1] + " super " + p[3] + " sub " + p[5] + "]"

def p_term_4(p):
    'term : factor UNDERSCORE factor CARET factor'
    p[0] = "[" + p[1] + " sub " + p[3] + " super " + p[5] + "]"

def p_term_5(p):
    'term : factor'
    p[0] = p[1]

def p_factor_paren(p):
    'factor : LPAREN expression RPAREN'
    p[0] = "(" + p[2] + ")"

def p_factor_brace(p):
    'factor : LBRACE expression RBRACE'
    p[0] = p[2]

def p_factor(p):
    'factor : CHAR'
    p[0] = p[1]

def p_error(p):
    print("Syntax error in input!")


# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = raw_input(u'Expresion a parsear: ')
   except EOFError:
       break
   if not s:
       continue
   result = parser.parse(s)
   print(result)
