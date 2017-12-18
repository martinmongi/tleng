from parser import parser
import argparse

argparser = argparse.ArgumentParser(description='Typeset lovely formulas')
argparser.add_argument('string_to_parse')
argparser.add_argument('output_filename')

args = argparser.parse_args()

result = parser.parse(vars(args)['string_to_parse'])


f = open(vars(args)['output_filename'], 'w')
f.write('<?xml version="1.0"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" >\n'
        '<g transform="scale(40) translate(10,10)" font-family="Courier" >\n')

if True:
    f.write(
        '<line x1="-100" y1="0" x2="100" y2="0" stroke-width="0.02" stroke="black"/>\n')
    f.write(
        '<line x1="0" y1="-100" x2="0" y2="100" stroke-width="0.02" stroke="black"/>\n')

    for i in range(1, 101):
        f.write('<line x1="' + str(i) + '" y1="-100" x2="' + str(i) +
                '" y2="100" stroke-width="0.01" stroke="black"/>\n')
        f.write('<line x1="-100" y1="' + str(i) + '" x2="100" y2="' +
                str(i) + '" stroke-width="0.01" stroke="black"/>\n')

result.propagate_scale(1)
result.synthesize_sizes()
result.propagate_position(0, 0)
result.render(f)

f.write('</g>\n</svg>\n')
f.close()
