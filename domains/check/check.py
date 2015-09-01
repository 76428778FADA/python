# coding=utf-8
import requests
import time
import os
from threading import Thread, current_thread
from queue import Queue


theard_count = 300
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
domain_file = "domains.txt"
#domain_temp = ""


def check_url(host):
    url = 'http://'+host+'/wp-login.php'

    try:
        response = requests.get(url, timeout=10, headers=headers)
    except Exception:
        return False
    else:
        if response.status_code == 200:
            if response.text.find('wp-admin')>0:
                return True
            else:
                return False       
        else:
            return False

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

    queue.join()

    print(time.time() - start_time)

if __name__ == '__main__':
    main()
