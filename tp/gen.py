from parser import result, ConcatenationOp, CharLeaf, DivisionOp


def render(ast, fout, x, y):
    if ast.__class__ == ConcatenationOp:
        render(ast.children[0], fout, x, y)
        render(ast.children[1], fout, x + ast.children[0].width, y)
    elif ast.__class__ == DivisionOp:
        render(ast.children[0], fout, x, y)
        fout.write('<line x1="' + str(x) +
                   '" y1="' + str(y - ast.scale * .6 + ast.children[0].height) +
                   '" x2="' + str(x + max(ast.children[0].width, ast.children[1].width)) +
                   '" y2="' + str(y - ast.scale * .6 + ast.children[0].height) +
                   '" stroke-width="0.03" stroke="black"/>\n')
        render(ast.children[1], fout, x, y +
               ast.children[0].height + ast.scale * .4)
    elif ast.__class__ == CharLeaf:
        fout.write('<text x="' + str(x * ast.scale) +
                   '" y="' + str(y * ast.scale) +
                   '" font-size="1">' + ast.value +
                   '</text>\n')


f = open('test.svg', 'w')
f.write('<?xml version="1.0"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" >\n'
        '<g transform="scale(40) translate(0, .62)" font-family="Courier" >\n')

render(result, f, 1, 1)

f.write('</g>\n</svg>\n')
f.close()
