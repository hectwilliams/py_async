"""Method to capture the first finished thread"""

import threading
import time 
import urllib.request

URL = "https://science.nasa.gov/mars/"

def download_html(html, lock):
    with urllib.request.urlopen(url = URL) as f:
        html.append(f.read().decode('utf-8'))
    lock.release() # semaphores allow lock to be released many times 

html1 = [] 
html2 = [] 
sem = threading.Semaphore() # |sem_count = 1|

th1 = threading.Thread(target=download_html, args=(html1,sem,))
th2 = threading.Thread(target=download_html, args=(html2,sem,))

sem.acquire() # |sem_count = 0|
th1.start() # sem_count = 1?
th2.start() # sem_count = 1?
sem.acquire() # |sem_count = 0|

# first finished request is captured 
if html1:
    print("first page")
if html2:
    print("second page")
    # print(html2)
