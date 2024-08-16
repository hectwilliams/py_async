""" Method to capture the m of n finished thread """

import urllib.request
import threading
import time 

def download_html(html, lock):
    with urllib.request.urlopen(url = URL) as f:
        html.append(f.read().decode('utf-8'))
    lock.release() # semaphores allow lock to be released many times 

def who_finished(html):
    if html[0]:
        print("first page acquired")
        html[0] = []
    elif html[1]:
        print("second page acquired")
        html[1] = []
    elif html[2]:
        print("third page acquired")
        html[2] = []
        
URL = "https://science.nasa.gov/mars/"
M = 2
N = 3 
html = [[]] * N
sem = threading.Semaphore(M)
th1=threading.Thread(target=download_html, args=(html[0],sem ))
th2=threading.Thread(target=download_html, args=(html[1],sem ))
th3=threading.Thread(target=download_html, args=(html[2],sem ))

for _ in range(M):
    sem.acquire(M)
th1.start()
th2.start()
th3.start()
for _ in range(M):
    sem.acquire()
    who_finished(html)




