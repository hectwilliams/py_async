""" Simple process futures example"""

import os 
import time
import random
import ctypes
import concurrent.futures
import multiprocessing.sharedctypes
import urllib.request
import multiprocessing

def download() -> str:
    """download html from google.com"""
    with urllib.request.urlopen('https://www.google.com/') as f:
        html = f.read().decode('utf-8')
        print(f' [Request Complete]\tenv variable = {os.environ['DUMMY_KEY']}')
    return html

def _init():
    os.environ["DUMMY_KEY"] = str(random.randint(1, 100))
    print(f' [Init]\t\tenv variable = {os.environ['DUMMY_KEY']}')

if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor(initializer=_init) as executor:

        t1=time.perf_counter()
        f1=executor.submit(download)
        f2=executor.submit(download)
        t2=time.perf_counter()
        print( f'{ ((t2-t1)*1000) :.3f} milliseconds') 
        print(f1.result()[:10])
        print(f2.result()[:10])

"""Executors call on seperate processes"""
