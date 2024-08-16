""" Conditional Object """

from urllib import request
import threading
import time 

def download_html(html:list, condition: threading.Condition):
    with request.urlopen('https://www.google.com') as f:
        html.append(f.read().decode('utf-8'))
    with condition:
        condition.notify()

html1 = [] 
html2 = []
my_cond = threading.Condition() 
thread1 = threading.Thread( target=download_html, args = (html1, my_cond) )
thread2 = threading.Thread( target=download_html, args = (html2, my_cond) )
thread1.start()
thread2.start()

with my_cond:
    my_cond.wait()

if html1:
    print("worker thread 1")

if html2:
    print("worker thread 2")

