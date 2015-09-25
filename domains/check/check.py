# coding=utf-8
import requests
import time
import os
from threading import Thread, current_thread
from queue import Queue


theard_count = 300
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
domain_file = "domains.txt"
open('good_wp.txt','w')
open('good_joo.txt','w')
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
                return 2
            #else:
                #return False       
        #else:
            #return False
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
            print('WPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWP')
            open('good_wp.txt', 'a+').write(host + '\n')
        else:
            pass
        if status == 3:
            print('JOOJOOJOOJOOJOOJOOJOOJOOJOOJOOJOOJOOJOOJOOJOOJOO')
            open('good_joo.txt', 'a+').write(host + '\n')
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
