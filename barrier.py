""" Barrier of three threads"""

import urllib.request
import threading
import time 

URL = "https://www.google.com"
PARTY_SIZE = 3
def download_html(html, barrier):
    with urllib.request.urlopen(url = URL) as f:
        html.append(f.read().decode('utf-8'))
    print(barrier.wait() )

html = [[]] * PARTY_SIZE
my_barrier = threading.Barrier(PARTY_SIZE)
th1 = threading.Thread(target=download_html, args=(html[0], my_barrier,))
th2 = threading.Thread(target=download_html, args=(html[1], my_barrier,))
th1.start()
th2.start()
print(my_barrier.wait() )

for i in range(PARTY_SIZE):
    if html[i]:
        html[i] = []
        print(f"request from {i + 1} complete ")
    


