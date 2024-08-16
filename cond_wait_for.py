""" Condtional object using wait for"""

from urllib import request
import threading
import time 

def download_html(html: list, condition: threading.Condition):
    global my_count 
    with request.urlopen('https://www.google.com') as f:
        html.append(f.read().decode('utf-8'))
    with condition:
        my_count += 1
        condition.notify() 

my_count = 0

html_list = [[]] * 3 
lock = threading.Lock()
my_cond = threading.Condition(lock)

thread1 = threading.Thread(target=download_html, args=(html_list[0], my_cond))
thread2 = threading.Thread(target=download_html, args=(html_list[1], my_cond))
thread3 = threading.Thread(target=download_html, args=(html_list[2], my_cond))
thread1.start()
thread2.start()
thread3.start()

with my_cond:
    my_cond.wait_for(lambda: my_count>=2)

if html_list[0]:
    print("worker thread 1")

if html_list[1]:
    print("worker thread 2")

if html_list[2]:
    print("worker thread 3")


