'''import requests

file = open('sqlerr.txt' , 'r')
err_list = file.readlines()
file.close()
resp = requests.get('http://www.ya.ru')
#print resp.text 
#err = 'DOCTYPE'
err = str(err_list[0])
err = err.strip()
print err
if resp.text.find(err)>0:
    print 'YES'
else:
    print 'NO'

'''
import requests
import re
import os
import string
#------------------------sqlerr.txt------------------------------
file = open('sqlerr.txt' , 'r')
err_list = file.readlines()
file.close()
print' ______________________________________'
print'|                                      |'
print'|  Parser dork from                    |' 
print'|      _                               |'
print'|     |_) o ._   _     _  _  ._ _      |'
print'|     |_) | | | (_| o (_ (_) | | |     |'
print'|                _|                    |'
print'|______________________________________|'
print
#--------------------------------------------------------------
file = open('url_pars.txt', 'w')
file.close()
search = raw_input('Text of dork (example:index.php?id=):')
#search = 'post.php?id='
#------------------Dorks list----------------------------------
dorks = open('dorks.txt' , 'r')
dorks_list = dorks.readlines()
dorks.close()
#pages = int(raw_input('Number of page: '))*10
#pages = 10
headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'}
count = 1
while (count < pages):
#http://www.bing.com/search?q=index.php?id=&go=&filt=all&first=1&FORM=PERE3
	req = ('http://www.bing.com/search?q=' + search + '&first='+str(count))
	try:	
	    response = requests.get(req)
	except:
	    print 'ERROR'
	#print response.text	
	req = ''	
	link = re.findall('<h2><a href="(.+?)"', response.text, re.DOTALL)
	for i in range(len(link)):
		#print link[i]
		#if link[i].find('yandex'):
		#	print 'YANDEX'
		#else:
		if link[i].find('http://bs.yandex.ru'):	
		    open('url_pars.txt', 'a+').write(link[i] +'\'' + '\n')
		#else:
		    #print 'ya'
		#count = count+10
		#print count
	count = count+10
	#print count
#---------------------Delete duplicates-------------------------
print 'Removing duplicates...'
input = open('url_pars.txt', 'r')
output = open('url.txt', 'w')
linesarray = input.readlines()
input.close()
seen = []
for i in range(len(linesarray)):
    if seen.count(linesarray[i]) == 0:
        seen.append(linesarray[i])
	#if linesarray[i].find('http://bs.yandex.ru'):
	output.write(linesarray[i])		
        #else:
		#print 'ya'
	
#os.remove('url_pars.txt')
output.close()
print 'Complete'
print 'Checking error...'
#-------------------------url.txt--------------------------------
file = open('url_pars.txt' , 'r')
url_list = file.readlines()
file.close()
#------------------------Proverka--------------------------------
err_page = 0
good_page = 0
for i in range(len(url_list)):
        page = url_list[i].strip()
	print page
        try:
		responce = requests.get(page)
        except Exception, e:
                err_page = err_page+1
        else:
                for i in range(len(err_list)):
                        err = str(err_list[i])
			err = err.strip()			
                        if responce.text.find(err)>0:
                                print 'FIND "'+err+'" in '+page
                                open('good.txt', 'a+').write(page + '\n')
                #else:
                        #print ''
#-------------------------------------------------------------------
print 'Good pages: '+str(good_page)
print '404,403 pages: '+str(err_page)
print 'Complete. Press any key...'
raw_input()