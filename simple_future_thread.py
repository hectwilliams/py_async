""" Simple thread futures example"""

import os 
import time
import random 
import urllib.request
import concurrent.futures

def download() -> str:
    """download html from google.com"""
    with urllib.request.urlopen('https://www.google.com/') as f:
        html = f.read().decode('utf-8')
        print(f' [Request Complete]\tenv variable = {os.environ['DUMMY_KEY']}')
    return html

def _init() -> None:
    r = str(random.randint(1, 100))
    os.environ["DUMMY_KEY"] = r
    print(f' [Init]\t\tenv variable = {os.environ['DUMMY_KEY']}')

def threadpool() -> None:
    with concurrent.futures.ThreadPoolExecutor(initializer=_init) as executor:
        t1=time.perf_counter()
        f1=executor.submit(download)
        f2=executor.submit(download)
        t2=time.perf_counter()
        print( f'{ ((t2-t1)*1000) :.3f} milliseconds' ) 
        print(f1.result()[:10])
        print(f2.result()[:10])
if __name__ == '__main__':
    threadpool()

"""Executors call on single process, different threads"""
