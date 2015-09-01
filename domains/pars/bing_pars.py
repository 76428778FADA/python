import requests
import re
import os
import string

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; rv:14.0) Gecko/20100101 Firefox/14.0.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'DNT': '1'
}

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
#http://www.google.ru/#q=flowers&newwindow=1&start=210
        req = ('https://www.bing.com/search?q=' + search + '&first='+str(count))
        try:	
            response = requests.get(req, headers=headers, timeout=10)
        except:
            print('Error get bing.com')
        req = ''	
        try:
            link = re.findall('<h2><a href="(.+?)"', response.text, re.DOTALL)
            for i in range(len(link)):
                #print(link[i])
                #if link[i].find('http://bs.yandex.ru'):
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
output = open('domains.txt', 'w')

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
