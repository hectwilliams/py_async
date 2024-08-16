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
    return html

def _init() -> None:
    r = str(random.randint(1, 100))
    os.environ["DUMMY_KEY"] = r

def threadpool() -> None:
    with concurrent.futures.ThreadPoolExecutor(initializer=_init) as executor:
        f1=executor.submit(download)
        f2=executor.submit(download)
        
        # step through futures as they resolve
        # for f in concurrent.futures.as_completed([f1,f2]): 
        #     print(f.result()[:15])
        
        # wait for first completed 
        res = concurrent.futures.wait([f1,f2], return_when=concurrent.futures.FIRST_COMPLETED)
        for f in res.done:
            print(f.result()[:10])
        

if __name__ == '__main__':
    threadpool()

"""Executors call on single process, different threads"""
