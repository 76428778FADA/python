#!/usr/bin/python
# -*- coding: utf-8 -*-
#import progressbar
import requests
import time
import os
import sys
from threading import Thread, current_thread
from queue import Queue

good_wp = 0
good_joo = 0
#domains_count = 0
pbcount = 0
theard_count = 300
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
domain_file = "domains_clear.txt"
open('domains.txt','w')
#domain_temp = ""


def check_url(host):
    global pbcount
    global domains_count
    global good_wp
    global good_joo
    pbcount = pbcount + 1
    sys.stdout.write("\033[0;32m\r%d" %pbcount + " / "+str(domains_count)+' || WordPress: ' + str(good_wp) + ' || Joomla: ' + str(good_joo))
    sys.stdout.flush()
    url = 'http://'+host+'/wp-login.php'
    try:
        response = requests.get(url, timeout=5, headers=headers)
    except Exception:
        return False
    else:
        #if response.status_code == 200:
        if response.text.find('wp-admin')>0:
            return 2
            #else:
                #return False       
        #else:
            #return False
    url = 'http://'+host+'/administrator/index.php'
    try:
        response = requests.get(url, timeout=5, headers=headers)
    except Exception:
        return False
    else:
        #if response.status_code == 200:
        if response.text.find('loginform')>0:
            return 3
            #else:
                #return False       
        #else:
            #return False

def run(queue, result_queue):
    global good_wp
    global good_joo
    # Цикл продолжается пока очередь задач не станет пустой
    while not queue.empty():
        # получаем первую задачу из очереди
        host = queue.get_nowait()
        #print('{} checking in thread {}'.format(host, current_thread()))
        # проверяем URL
        status = check_url(host)
        # сохраняем результат для дальнейшей обработки
        result_queue.put_nowait((status, host))
        # сообщаем о выполнении полученной задачи
        queue.task_done()
        if status == 2:
            #print('WPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWPWP')
            good_wp = good_wp + 1
            #print(str(good_wp))
            open('domains.txt', 'a+').write('0 '+host + '\n')
        if status == 3:
            #print('JOOJOOJOOJOOJOOJOOJOOJOOJOOJOOJOOJOOJOOJOOJOOJOO')
            good_joo = good_joo + 1
            open('domains.txt', 'a+').write('1 '+host + '\n')
        #print('{} finished in thread {}. Result={}'.format(host, current_thread(), status))
    #print('{} closing'.format(current_thread()))
# Remove duplicate
'''def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]'''
    
# MAIN
def main():
    global pbcount
    global domains_count
    start_time = time.time()
    # Для получения задач и выдачи результата используем очереди
    queue = Queue()
    result_queue = Queue()
   
    '''#Delete dupicate
    print('Removing duplicates...')
    input = open('domains_dub.txt', 'r')
    output = open('domains_clear.txt', 'w')
    linesarray = input.readlines()
    #count_line = len(linesarray)
    input.close()
    #print(str(count_line))
    #bar = progressbar.ProgressBar(maxval=count_line).start()
    seen = []
    seen = f7(linesarray)
    for i in range(len(seen)):
        #bar.update(i)
        output.write(seen[i])
    output.close()
    #bar.finish()
    print('Complete')'''
    #fr_success = os.path.join(domain_temp, "good.txt")
    #fr_errors  = os.path.join(domain_temp, "error.txt")

    # Сначала загружаем все URL из файла в очередь задач
    domains_count = len(open('domains_clear.txt', 'r').readlines())
    #print(str(domains_count))
    with open(domain_file) as f:	
        for line in f:
            queue.put(line.strip())
    # Затем запускаем необходимое количество потоков
    for i in range(theard_count):
        thread = Thread(target=run, args=(queue, result_queue))
        thread.daemon = True
        thread.start()
    queue.join()
    print('/n Complete...')
    #print(time.time() - start_time)

if __name__ == '__main__':
    main()
