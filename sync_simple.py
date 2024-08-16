""" .join free method to wait on a thread """

import threading
import time 

lock = threading.Lock() 

def work():
    """thread suspended to 2 seconds before releasing lock"""
    time.sleep(2)
    lock.release() 

th1 = threading.Thread(target=work)
lock.acquire() # main thread acquires lock
th1.start() # working thread 
lock.acquire() # main thread reaquires lock
print("reacquired - do more work")



