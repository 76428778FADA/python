#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import os
import sys

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
input = open('shells.txt', 'r')                               
good = open('good.txt','w')
bad = open('bad.txt','w')
good_count = 0
bad_count = 0
pbcount = 0

def check_url(url):
    global shell_count
    global pbcount
    global good_count
    global bad_count
    sys.stdout.write("\033[0;32m\r%d" %pbcount + " / "+str(shell_count)+' || Good: ' + str(good_count) + ' || Bad: ' + str(bad_count))
    sys.stdout.flush()
    try:
        response = requests.get(url, timeout=10, headers=headers, allow_redirects=False)
    except Exception:
        return 0
    if response.status_code == 200:
        good_count = good_count + 1
        #print('Good')
        return 1
    else:
        bad_count = bad_count + 1
        #print('Bad')
        return 0
linesarray = input.readlines()
input.close()
shell_count = len(open('shells.txt', 'r').readlines())
seen = []
seen = linesarray
for i in range(len(seen)):
    #print(seen[i])
    status = check_url(seen[i].strip())
    pbcount = pbcount + 1
    if status == 1:
        good.write(seen[i])
    if status == 0:
        bad.write(seen[i])
good.close()
bad.close()
print('Complete')                                                                                                                                                                    
