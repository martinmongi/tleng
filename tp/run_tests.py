f = open('tests.txt', 'r')

import os
import string

i = 0
for line in f:
    i += 1
    command = "python gen.py '" + \
        string.strip(line) + "' " + str(i) + ".svg"
    print command
    os.system(command)
