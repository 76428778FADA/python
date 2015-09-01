# coding=utf-8
import os

#------------------source list----------------------------------
source = open('source.txt' , 'w')
source.close()
#--------------------------------------------------------------
#------------------login list----------------------------------
login = open('login.txt' , 'r')
login_list = login.readlines()
login.close()
#--------------------------------------------------------------
#------------------pwd list----------------------------------
pwd = open('pwd.txt' , 'r')
pwd_list = pwd.readlines()
pwd.close()
#--------------------------------------------------------------
#------------------domains list----------------------------------
domains = open('domains.txt' , 'r')
domains_list = domains.readlines()
domains.close()
#--------------------------------------------------------------

theard_count = 1
def gen():
    #t = domains.split('.')
    #s = t[0]
    for i in range(len(login_list)):
        login = login_list[i].strip()
        for i in range(len(pwd_list)):
            pwd = pwd_list[i].strip()
            for i in range(len(domains_list)):
                #domains = domains_list
                open('source.txt', 'a+').write(login+' '+pwd+' '+domains_list[i])

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

gen()
gen_host()
'''def run(queue, result_queue):
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
        # сохраняем результат для дальнейшей обработки
        result_queue.put_nowait((status, host))
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
    main()'''
