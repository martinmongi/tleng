import ply.yacc as yacc

# Get the token map from the lexer.
from lexer import tokens


class Operation(object):
    def render(self, fout):
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
        self.div_line_offset = self.scale * .72

    def propagate_position(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def render(self, fout):
        fout.write('<text x="' + str(self.pos_x) +
                   '" y="' + str(self.pos_y + self.height) +
                   '" font-size="' + str(self.scale) +
                   '">' + self.value +
                   '</text>\n')

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
        self.div_line_offset = max(
            self.children[0].div_line_offset, self.children[1].div_line_offset)

    def propagate_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.children[0].propagate_position(
            x,
            y + self.div_line_offset - self.children[0].div_line_offset)
        self.children[1].propagate_position(
            x + self.children[0].width,
            y + self.div_line_offset - self.children[1].div_line_offset)

    def render(self, fout):
        self.children[0].render(fout)
        self.children[1].render(fout)

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
            self.children[1].height + self.scale * .3
        self.div_line_offset = self.children[0].height + self.scale * .3

    def propagate_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        up_y = self.pos_y
        down_y = self.pos_y + self.div_line_offset
        self.children[0].propagate_position(
            x + (self.width - self.children[0].width) / 2, up_y)
        self.children[1].propagate_position(
            x + (self.width - self.children[1].width) / 2, down_y)

    def render(self, fout):
        self.children[0].render(fout)
        fout.write('<line x1="' + str(self.pos_x) +
                   '" y1="' + str(self.pos_y + self.div_line_offset) +
                   '" x2="' + str(self.pos_x + max(self.children[0].width, self.children[1].width)) +
                   '" y2="' + str(self.pos_y + self.div_line_offset) +
                   '" stroke-width="' + str(self.scale * 0.06) +
                   '" stroke="black"/>\n')
        self.children[1].render(fout)

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
        self.width = self.script.width + \
            max(self.superscript.width, self.subscript.width)

        self.height = max(self.script.height * .5, self.superscript.height) + \
            self.script.height * .2 + \
            max(self.script.height * .3, self.subscript.height)

        self.div_line_offset = self.script.div_line_offset + max(
            0, self.superscript.height - self.script.height * .5)

    def propagate_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.script.propagate_position(x, y + max(
            0, self.superscript.height - self.script.height * .5))
        self.superscript.propagate_position(
            x + self.script.width, y)
        self.subscript.propagate_position(
            x + self.script.width,
            y + self.script.height * .2 + max(self.script.height * .5, self.superscript.height))

    def render(self, fout):
        self.script.render(fout)
        self.superscript.render(fout)
        self.subscript.render(fout)

    def __repr__(self):
        return "SuperSub" + repr((self.value,
                                  self.scale,
                                  self.width,
                                  self.height,
                                  [self.script, self.superscript, self.subscript]))


class ParenthesesOp(Operation):
    def __init__(self, child):
        self.child = child
        self.value = '(' + child.value + ')'
        self.scale = self.width = self.height = self.pos_x = self.pos_y = -1

    def propagate_scale(self, scale):
        self.child.propagate_scale(scale)
        self.scale = scale

    def synthesize_sizes(self):
        self.child.synthesize_sizes()
        self.width = self.scale * 1.2 + self.child.width
        self.height = self.child.height
        self.div_line_offset = self.child.div_line_offset

    def propagate_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.child.propagate_position(x + 0.6 * self.scale, y)

    def render(self, fout):
        fout.write('<text x="0" y="0" font-size="' + str(self.scale) +
                   '" transform="translate(' + str(self.pos_x) +
                   ',' + str(self.pos_y + self.height * .85) +
                   ') scale(1,' + str(self.height / self.scale / .77) + ')">(</text>')
        self.child.render(fout)
        fout.write('<text x="0" y="0" font-size="' + str(self.scale) +
                   '" transform="translate(' + str(self.pos_x + self.child.width + 0.6 * self.scale) +
                   ',' + str(self.pos_y + self.height * .85) +
                   ') scale(1,' + str(self.height / self.scale / .77) + ')">)</text>')

    def __repr__(self):
        return "Parentheses" + repr((self.value,
                                     self.scale,
                                     self.width,
                                     self.height,
                                     self.pos_x,
                                     self.pos_y,
                                     self.child))


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
