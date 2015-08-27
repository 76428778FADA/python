import requests
#import os

#----domains.txt----
file = open('domains.txt' , 'r')
d_list = file.readlines()
file.close()
#----
def check(url):
    response = requests.get(url+'wp-login.php')
    if response.status_code == 200:
        #if response.text.find('admin-ajax.php')>0:
        if response.text.find('wp-admin')>0:
            return 1
            print(url)
        else:
            return 0
    else:
        return 0
for i in range(len(d_list)):
    url = d_list[i].strip()
    #headers = {'user-agent': 'my-app/0.0.1'}
    try:
        if check(url) == 1:
            print('1')
            open('good.txt', 'a+').write(url + '\n')
        else:
            print('0')
    except:
        print('error')
