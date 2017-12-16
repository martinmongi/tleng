import ply.yacc as yacc

# Get the token map from the lexer.
from lexer import tokens


class Operation(object):
    def render(self, fout):
        raise NotImplementedError('subclass responsibility')

    def amount_of_divitions_included(self):
        raise NotImplementedError('subclass responsibility')

    def synthesize_sizes(self):
        raise NotImplementedError('subclass responsibility')

    def propagate_scale(self, scale):
        raise NotImplementedError('subclass responsibility')


class EmptyLeaf(Operation):
    def __init__(self):
        self.value = ""
        self.scale = self.width = self.height = self.pos_x = self.pos_y = 0

    def propagate_scale(self, scale):
        pass

    def synthesize_sizes(self):
        pass

    def propagate_position(self, x, y):
        pass

    def amount_of_divitions_included(self):
        return 0

    def render(self, fout):
        pass

    def __repr__(self):
        return "EmptyLeaf"


class CharLeaf(Operation):
    def __init__(self, c):
        self.value = c
        self.scale = self.width = self.height = self.pos_x = self.pos_y = -1

    def propagate_scale(self, scale):
        self.scale = scale

    def synthesize_sizes(self):
        self.width = self.scale * .6
        self.height = self.scale

    def propagate_position(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def render(self, fout):
        fout.write('<text x="' + str(self.pos_x) +
                   '" y="' + str(self.pos_y) +
                   '" font-size="' + str(self.scale) +
                   '">' + self.value +
                   '</text>\n')

    def amount_of_divitions_included(self):
        return 0

    def __repr__(self):
        return "Leaf" + repr((self.value,
                              self.scale,
                              self.width,
                              self.height,
                              self.pos_x,
                              self.pos_y))


class ConcatenationOp(Operation):
    def __init__(self, child1, child2):
        self.value = child1.value + child2.value
        self.children = [child1, child2]
        self.scale = self.width = self.height = self.pos_x = self.pos_y = -1

    def propagate_scale(self, scale):
        self.scale = scale
        self.children[0].propagate_scale(scale)
        self.children[1].propagate_scale(scale)

    def synthesize_sizes(self):
        self.children[0].synthesize_sizes()
        self.children[1].synthesize_sizes()
        self.width = self.children[0].width + self.children[1].width
        self.height = max(self.children[0].height, self.children[1].height)

    def propagate_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.children[0].propagate_position(x, y)
        self.children[1].propagate_position(x + self.children[0].width, y)

    def render(self, fout):
        self.children[0].render(fout)
        self.children[1].render(fout)

    def amount_of_divitions_included(self):
        return self.children[0].amount_of_divitions_included() + self.children[1].amount_of_divitions_included()

    def __repr__(self):
        return "Concat" + repr((self.value,
                                self.scale,
                                self.width,
                                self.height,
                                self.pos_x,
                                self.pos_y,
                                self.children))


class DivisionOp(Operation):
    def __init__(self, child1, child2):
        self.value = child1.value + '/' + child2.value
        self.children = [child1, child2]
        self.scale = self.width = self.height = self.pos_x = self.pos_y = -1

    def propagate_scale(self, scale):
        self.scale = scale
        self.children[0].propagate_scale(scale)
        self.children[1].propagate_scale(scale)

    def synthesize_sizes(self):
        self.children[0].synthesize_sizes()
        self.children[1].synthesize_sizes()
        self.width = max(self.children[0].width, self.children[1].width)
        self.height = self.children[0].height + \
                      self.children[1].height

    def propagate_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.line_pos_y = self.pos_y - self.scale * .28
        up_y = self.line_pos_y - self.scale * .2
        down_y = self.line_pos_y + self.scale * .8
        print(up_y, self.line_pos_y, down_y)
        self.children[0].propagate_position(
            x + (self.width - self.children[0].width) / 2, up_y)
        self.children[1].propagate_position(
            x + (self.width - self.children[1].width) / 2, down_y)

    def render(self, fout):
        self.children[0].render(fout)
        fout.write('<line x1="' + str(self.pos_x) +
                   '" y1="' + str(self.line_pos_y) +
                   '" x2="' + str(self.pos_x + max(self.children[0].width, self.children[1].width)) +
                   '" y2="' + str(self.line_pos_y) +
                   '" stroke-width="' + str(self.scale * 0.06) +
                   '" stroke="black"/>\n')
        self.children[1].render(fout)

    def amount_of_divitions_included(self):
        return 1 + self.children[0].amount_of_divitions_included() + self.children[1].amount_of_divitions_included()

    def __repr__(self):
        return "Div" + repr((self.value,
                             self.scale,
                             self.width,
                             self.height,
                             self.pos_x,
                             self.pos_y,
                             self.children))


class SuperSubScriptOp(Operation):
    def __init__(self, script, superscript=None, subscript=None):
        superscript = superscript or EmptyLeaf()
        subscript = subscript or EmptyLeaf()
        self.value = script.value + '^' + superscript.value + '_' + subscript.value
        self.script = script
        self.superscript = superscript
        self.subscript = subscript
        self.scale = self.width = self.height = self.pos_x = self.pos_y = -1

    def propagate_scale(self, scale):
        self.scale = scale
        self.script.propagate_scale(scale)
        self.superscript.propagate_scale(scale * .7)
        self.subscript.propagate_scale(scale * .7)

    def synthesize_sizes(self):
        self.script.synthesize_sizes()
        self.superscript.synthesize_sizes()
        self.subscript.synthesize_sizes()
        self.width = self.script.width + max(self.superscript.width, self.subscript.width)
        self.height = max(self.script.height, self.superscript.height + self.superscript.height)

    def propagate_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.script.propagate_position(x, y)
        self.superscript.propagate_position(
            x + self.script.width, y - self.superscript.height * 0.45 * self.scale)
        self.subscript.propagate_position(
            x + self.script.width, y + self.subscript.height * 0.2 * self.scale)

    def render(self, fout):
        self.script.render(fout)
        self.superscript.render(fout)
        self.subscript.render(fout)

    def amount_of_divitions_included(self):
        return 0

    def __repr__(self):
        return "SuperSub" + repr((self.value,
                                  self.scale,
                                  self.width,
                                  self.height,
                                  [self.script, self.superscript, self.subscript]))


class ParenthesesOp(Operation):
    def __init__(self, child1):
        self.children = [child1]
        self.value = '(' + child1.value + ')'
        self.scale = self.width = self.height = self.pos_x = self.pos_y = self.amount_of_divitions = -1

    def propagate_scale(self, scale):
        self.children[0].propagate_scale(scale)
        self.scale = scale
        self.amount_of_divitions = self.calculate_amount_of_parentheses(self.children[0])

    def synthesize_sizes(self):
        self.children[0].synthesize_sizes()
        self.width = 2 * self.scale + self.children[0].width
        # fixme: the height is not well calculated
        self.height = self.children[0].height

    def propagate_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.children[0].propagate_position(x + 0.5, y)

    def render(self, fout):
        fout.write('<text x="' + str(self.pos_x) +
                   '" y="' + str(self.pos_y) +
                   '" font-size="' + "1" +
                   '" transform="translate(0, 0) scale(1,' + str(self.amount_of_divitions) + ')">(</text>')
        self.children[0].render(fout)
        fout.write('<text x="' + str(self.pos_x + self.children[0].width + 0.5) +
                   '" y="' + str(self.pos_y) +
                   '" font-size="' + "1" +
                   '" transform="translate(0, 0) scale(1,' + str(self.amount_of_divitions) + ')">)</text>')

    def amount_of_divitions_included(self):
        return self.children[0].amount_of_divitions_included()

    def __repr__(self):
        return "Parentheses" + repr((self.value,
                                     self.scale,
                                     self.width,
                                     self.height,
                                     self.pos_x,
                                     self.pos_y,
                                     self.amount_of_divitions,
                                     self.children))

    def calculate_amount_of_parentheses(self, child):
        amount_of_divitions_included = child.amount_of_divitions_included()
        if amount_of_divitions_included == 0:
            return 1
        return amount_of_divitions_included * 2.2


# class ParenthesesOp(Operation):
#     def __init__(self, child):
#         self.value = '(' + child.value + ')'
#         self.scale = self.width = self.height = self.pos_x = self.pos_y = -1
#         self.child = child

#     def propagate_scale(self, scale):
#         self.scale = scale
#         self.child.propagate_scale(scale)

#     def synthesize_sizes(self):
#         self.child.synthesize_sizes()
#         self.width = self.child.width + self.scale * 2
#         self.height = self.child.height

#     def propagate_position(self, x, y):
#         self.pos_x = x
#         self.pos_y = y
#         self.child.propagate_position(x + self.scale, y)

#     def render(self, fout):
#         fout.write(
#             '< text x="0" y="0" font - size="1" transform="translate(2.82, 1.36875) scale(1,2.475)" > ) < /text>')
#         self.child.render(fout)

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
    p[0] = SuperSubScriptOp(p[1], p[3], None)


def p_term_2(p):
    'term : factor UNDERSCORE factor'
    p[0] = SuperSubScriptOp(p[1], None, p[3])


def p_term_3(p):
    'term : factor CARET factor UNDERSCORE factor'
    p[0] = SuperSubScriptOp(p[1], p[3], p[5])


def p_term_4(p):
    'term : factor UNDERSCORE factor CARET factor'
    p[0] = SuperSubScriptOp(p[1], p[5], p[3])


def p_factor_paren(p):
    'factor : LPAREN expression RPAREN'
    p[0] = ParenthesesOp(p[2])
    # p[0] = ConcatenationOp(ConcatenationOp(CharLeaf("("), p[2]), CharLeaf(")"))


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
