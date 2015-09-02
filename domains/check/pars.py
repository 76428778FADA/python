# coding=utf-8
import os

domains = open('dom.txt' , 'r')
domains_list = domains.readlines()
domains.close()

for i in range(len(domains_list)):
    t = domains_list[i].strip()
    s = t.split('	')
    print(s[0])
    open('domains.txt', 'a+').write(s[0] + '\n')
