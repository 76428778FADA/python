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

request_file = "request.txt"

theard_count = 10

pages = 20

file = open('url_pars.txt', 'w')
file.close()
#-------------------------------------------------------------------------------------------
def pars(request):
    for i in range(len(request_list)):
        search = request_list[i].strip()
        print('Use request: '+search)
        count = 1
        while (count < pages):
#http://www.bing.com/search?q=index.php?id=&go=&filt=all&first=1&FORM=PERE3
            req = ('http://www.bing.com/search?q=' + search + '&first='+str(count))
            try:	
                response = requests.get(req)
            except:
                print('Error get bing.com')
            req = ''	
            try:
                link = re.findall('<h2><a href="(.+?)"', response.text, re.DOTALL)
                for i in range(len(link)):
                    #print(link[i])
                    if link[i].find('http://bs.yandex.ru'):
                        print('url: '+link[i])
                        t = link[i].split('//')
                        s = t[1].split('/')	
                        open('url_pars.txt', 'a+').write(s[0] +'\n')
            except:
                print('Error parsing url')
            count = count+10
#----------------------------------------------------------------------------------------

def run(queue, result_queue):
    # Цикл продолжается пока очередь задач не станет пустой
    while not queue.empty():
        # получаем первую задачу из очереди
        request = queue.get_nowait()
        print('Checking in thread {}'.format(current_thread()))
        print(request)
	# проверяем URL
        try:
            status = pars(request)
        except Exception:
            print('Error in thread')
        # сохраняем результат для дальнейшей обработки
        result_queue.put_nowait((status, request))
        # сообщаем о выполнении полученной задачи
        queue.task_done()
        if status:
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

    # Сначала загружаем все URL из файла в очередь задач
    with open(request_file) as f:
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
#---------------------Delete duplicates-------------------------

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

print('Removing duplicates...')
input = open('url_pars.txt', 'r')
output = open('url.txt', 'w')

linesarray = input.readlines()
input.close()
seen = []
seen = f7(linesarray)
#print(seen)
for i in range(len(seen)):
    output.write(seen[i])
output.close()
print('Complete')
os.remove('url_pars.txt')
