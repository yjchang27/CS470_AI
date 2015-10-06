import re

f = open('constraints', 'r')
pattern = re.compile(r'\d+|\+|=')

for line in f:
    line = line.strip()
    if line == '':
        continue
    elif line[0] == '#':
        print(line)
        continue
    tokens = pattern.findall(line)
    for token in tokens:
        endchar = ' '
        if token == tokens[-1]:
            endchar = ','
        if token.isdigit():
            print('v[{}]'.format(int(token)-1), end=endchar)
        else:
            if token == '=': token = '=='
            print(token, end=endchar)
    print()
