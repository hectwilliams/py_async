"""Processes call future(s) with shared object"""

import concurrent.futures
import multiprocessing
from multiprocessing.sharedctypes import SynchronizedArray, Synchronized
import time 
import ctypes 

def counter():
    """Counter to size of range by process"""
    global count # global shared variable
    global my_name
    global my_list 
    for _ in range(10000):
        with count: # global ctypes contains default lock 
            count.value = count.value + 1
    my_name.value = b"tut" 
    my_list[0].value = b"hello"
    my_list[1].value = b"world"
             
def setup(var1: Synchronized, var2:SynchronizedArray, var3:SynchronizedArray):
    """Shared objects are initialized"""
    global count # global shared variable
    global my_name
    global my_list
    count = var1 # global count reference ctype object (var) 
    my_name = var2 
    my_list = var3

if __name__ == '__main__':
    my_counter=multiprocessing.Value(ctypes.c_int, 0)
    my_name = multiprocessing.Array(ctypes.c_char, 10) 
    my_list = [multiprocessing.Array(ctypes.c_char, 8) for _ in range(2)]  # two 8 byte mem blocks 
    #   multiprocessing.Array( ctypes.c_char_p ,1)    # array of pointers, creates a string list
    with concurrent.futures.ProcessPoolExecutor(2, initializer=setup, initargs=(my_counter, my_name, my_list )) as execute:
        t1=time.perf_counter()
        f1=execute.submit(counter)
        f2=execute.submit(counter)
        concurrent.futures.wait([f1,f2], return_when=concurrent.futures.ALL_COMPLETED)
        t2=time.perf_counter()
        print(my_counter.value, my_name.value, my_list[0][:], my_list[1][:])
    print(f'elasped time\t {(t2-t1)*1000:.3f} milliseconds')