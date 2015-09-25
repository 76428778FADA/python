import os
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

print('Removing duplicates...')
input = open('xaj', 'r')
output = open('xaj.txt', 'w')

linesarray = input.readlines()
input.close()
seen = []
seen = f7(linesarray)
for i in range(len(seen)):
    output.write(seen[i])
output.close()
print('Complete')
