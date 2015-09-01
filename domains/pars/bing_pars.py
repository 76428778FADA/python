import requests
import re
import os
import string

file = open('url_pars.txt', 'w')
file.close()
#------------------request list----------------------------------
request = open('request.txt' , 'r')
request_list = request.readlines()
request.close()
#--------------------------------------------------------------
pages = int(input('Number of page: '))*10
for i in range(len(request_list)):
    search = request_list[i].strip()
    print('Use request: '+search)
    count = 1
    while (count < pages):
#http://www.bing.com/search?q=index.php?id=&go=&filt=all&first=1&FORM=PERE3
        req = ('http://www.bing.com/search?q=' + search + '&first='+str(count))
        try:	
            response = requests.get(req)
        except:
            print('Error get bing.com')
        req = ''	
        try:
            link = re.findall('<h2><a href="(.+?)"', response.text, re.DOTALL)
            for i in range(len(link)):
                #print(link[i])
                if link[i].find('http://bs.yandex.ru'):
                    print('url: '+link[i])
                    t = link[i].split('//')
                    s = t[1].split('/')	
                    open('url_pars.txt', 'a+').write(s[0] +'\n')
        except:
            print('Error parsing url')
        count = count+10
        #print(str(count))
#---------------------Delete duplicates-------------------------

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

print('Removing duplicates...')
input = open('url_pars.txt', 'r')
output = open('url.txt', 'w')

linesarray = input.readlines()
input.close()
seen = []
seen = f7(linesarray)
#print(seen)
for i in range(len(seen)):
    output.write(seen[i])
output.close()
print('Complete')
os.remove('url_pars.txt')
