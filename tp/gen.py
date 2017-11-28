from parser import result


f = open('test.svg', 'w')
f.write('<?xml version="1.0"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" >\n'
        '<g transform="scale(40) translate(0, .62)" font-family="Courier" >\n')

result.render(f, 0, 0)

f.write('</g>\n</svg>\n')
f.close()
