import ply.yacc as yacc

# Get the token map from the lexer.
from lexer import tokens


class Operation(object):
    def render(self, fout, x, y):
        raise NotImplementedError('subclass responsibility')


class ConcatenationOp(Operation):
    def __init__(self, child1, child2):
        self.value = child1.value + child2.value
        self.scale = max(child1.scale, child2.scale)
        self.width = child1.width + child2.width
        self.height = max(child1.height, child2.height)
        self.children = [child1, child2]

    def __repr__(self):
        return "Concat" + repr((self.value,
                                self.scale,
                                self.width,
                                self.height,
                                self.children))

    def render(self, fout, x, y):
        self.children[0].render(fout, x, y)
        self.children[1].render(fout, x + self.children[0].width, y)


class DivisionOp(Operation):
    def __init__(self, child1, child2):
        self.value = child1.value + child2.value
        self.scale = max(child1.scale, child2.scale)
        self.width = max(child1.width, child2.width)
        self.height = child1.height + child2.height + self.scale * .4
        self.children = [child1, child2]

    def __repr__(self):
        return "Division" + repr((self.value,
                                  self.scale,
                                  self.width,
                                  self.height,
                                  self.children))

    def render(self, fout, x, y):
        self.children[0].render(fout, x, y)
        fout.write('<line x1="' + str(x) +
                   '" y1="' + str(y - self.scale * .6 + self.children[0].height) +
                   '" x2="' + str(x + max(self.children[0].width, self.children[1].width)) +
                   '" y2="' + str(y - self.scale * .6 + self.children[0].height) +
                   '" stroke-width="0.03" stroke="black"/>\n')
        self.children[1].render(fout, x, y + self.children[0].height + self.scale * .4)


class CaretOp(Operation):
    def __init__(self, child1, child2):
        self.value = child1.value + child2.value
        self.scale = max(child1.scale, child2.scale) * 0, 7
        self.width = child1.width, child2.width
        self.height = max(child1.height, child1.height * 0.45 + child2.height)
        self.children = [child1, child2]

    def __repr__(self):
        return "Caret" + repr((self.value,
                               self.scale,
                               self.width,
                               self.height,
                               self.children))

    def render(self, fout, x, y):
        self.children[0].render(fout, x, y)
        self.children[1].render(fout, x + self.children[0].width, y - self.children[1].height * 0.45)


class CharLeaf(Operation):
    def __init__(self, c):
        self.value = c
        self.scale = 1.
        self.width = .6
        self.height = 1
        self.children = []

    def __repr__(self):
        return "Leaf" + repr((self.value,
                              self.scale,
                              self.width,
                              self.height))

    def render(self, fout, x, y):
        fout.write('<text x="' + str(x * self.scale) +
                   '" y="' + str(y * self.scale) +
                   '" font-size="1">' + self.value +
                   '</text>\n')


start = 'expression'


def p_expression_slash(p):
    'expression : expression SLASH concat'
    p[0] = DivisionOp(p[1], p[3])


def p_concat_1(p):
    'concat : concat term'
    p[0] = ConcatenationOp(p[1], p[2])


def p_pass_through(p):
    '''expression : concat
       concat     : term
       term       : factor'''
    p[0] = p[1]


def p_term_1(p):
    'term : factor CARET factor'
    p[0] = CaretOp(p[1], p[3])


# def p_term_2(p):
#     'term : factor UNDERSCORE factor'
#     p[0] = "[" + p[1] + " sub " + p[3] + "]"

# def p_term_3(p):
#     'term : factor CARET factor UNDERSCORE factor'
#     p[0] = "[" + p[1] + " super " + p[3] + " sub " + p[5] + "]"

# def p_term_4(p):
#     'term : factor UNDERSCORE factor CARET factor'
#     p[0] = "[" + p[1] + " sub " + p[3] + " super " + p[5] + "]"

def p_factor_paren(p):
    'factor : LPAREN expression RPAREN'
    p[0] = ConcatenationOp(ConcatenationOp(CharLeaf("("), p[2]), CharLeaf(")"))


def p_factor_brace(p):
    'factor : LBRACE expression RBRACE'
    p[0] = p[2]


def p_factor(p):
    'factor : CHAR'
    p[0] = CharLeaf(p[1])


def p_error(p):
    print("Syntax error in input!")


# Build the parser
parser = yacc.yacc()

try:
    s = raw_input(u'Expresion a parsear: ')
except EOFError:
    exit()
if not s:
    exit()
result = parser.parse(s)
print(result)
