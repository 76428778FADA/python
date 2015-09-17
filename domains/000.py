import lxml.html
import requests

r = requests.get("http://tw1ns.mysit.ru/administrator")
parsed = lxml.html.fromstring(r.text)
links = parsed.xpath("//input[@value]")
list = []
for i in links:
    #print(i.attrib['value'])
    #t = (i.attrib['value'])
    list.append(i.attrib['value'])
for i in links:
    #print(i.attrib['name'])
    s = (i.attrib['name'])
#print(t)
print(s)
print(list[2])
