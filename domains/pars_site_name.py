input = open('shell_copy.txt', 'r')
output = open('site.txt', 'w')
linesarray = input.readlines()
input.close()
seen = []
seen = linesarray
for i in range(len(seen)):
    url = seen[i].split('/')
    print(url[2])
    #print(url[0]+'/'+url[1]+'/'+url[2])
    output.write(url[0]+'/'+url[1]+'/'+url[2]+'\n')
output.close()
print('Complete')
