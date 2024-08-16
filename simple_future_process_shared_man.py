"""
    Processes call future(s) with manager regulated shared object

    Process manager passes the shared objects to the processes. 
    Unlike simple_future_process_shared.py no initialization of
    shared objects is required.  
"""

import concurrent.futures
import multiprocessing
import multiprocessing.managers
import time 
import ctypes 

def counter(count, my_name, my_list, my_lock):
    """Counter to size of range by process"""
    for _ in range(10):
        with my_lock:
            if count.value == 0:
                my_name.value = b"tron"
                my_list[0].value = b"best"
                my_list[1].value = b"list"
            count.value = count.value + 1

if __name__ == '__main__':
    with multiprocessing.Manager() as man:
        with concurrent.futures.ProcessPoolExecutor(2) as execute:
            my_counter=man.Value(u'i', 0)  #i-int
            my_name = man.Value(u'b', b"JOHNDOE" ) #u-c_wchar
            my_list = [man.Value(u'b', b'DEADBEEF') for _ in range(2)]
            my_lock = man.Lock()
            t1=time.perf_counter()
            f1=execute.submit(counter, my_counter, my_name, my_list, my_lock)
            f2=execute.submit(counter, my_counter, my_name, my_list, my_lock)
            concurrent.futures.wait([f1,f2], return_when=concurrent.futures.ALL_COMPLETED)
            t2=time.perf_counter()
            print(my_counter.value, my_name, my_list[0], my_list[1])
    print(f'elasped time\t {(t2-t1)*1000:.3f} milliseconds')