"""Use Lock(i.e. mutex)  with processes"""

import multiprocessing # supports Lock
import time 

def my_process(mutex_lock):
    mutex_lock.acquire()
    time.sleep(2) # Do something | Suspends thread for 2 seconds | No other thread can run because thread has lock 
    mutex_lock.release() 

multiprocessing.set_start_method(method='fork')

llock = multiprocessing.Lock()
p1 = multiprocessing.Process(name="tranform-ps", target=my_process, args=(llock,))
p2 = multiprocessing.Process(name= "translate-ps", target=my_process, args=(llock,))
t1=time.perf_counter()
p1.start()
p2.start() 
p1.join()
p2.join() 
t2 = time.perf_counter() 
print(f"Elasped time ==> \t {(t2-t1)*1000} milliseconds")


"""
    processes using mutex run slower than processes without mutex. The 
    latter runs concurrently, while the former is delayed by switching as 
    both process try to acquite one lock   
"""