from parser import result


f = open('test.svg', 'w')
f.write('<?xml version="1.0"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" >\n'
        '<g transform="scale(40) translate(0, .62)" font-family="Courier" >\n')

print(result)
result.propagate_scale(1)
print(result)
result.synthesize_sizes()
print(result)
result.propagate_position(10,10)
print(result)
result.render(f)

f.write('</g>\n</svg>\n')
f.close()
