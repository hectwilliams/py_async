""" Two threads deadlock"""

import threading
import time 

counters = [0,0]
locks = [lock() for lock in [threading.Lock] * 2]
N = round(10)

def count1(n):
    """local thread counts main counters[0] and axuillary counters[1]"""

    for _ in range(n):
        locks[0].acquire()
        counters[0] += 1
        if locks[1].acquire(timeout=0.50):
            counters[1] += 1
            locks[1].release()
        else:
            print("deadlock observed on thread 1")
        locks[0].release()

def count2(n):
    """local thread counts main counters[1] and axuillary counters[0]"""

    for _ in range(n):
        locks[1].acquire()
        counters[1] += 1
        if locks[0].acquire(timeout=0.50):
            counters[0] += 1
            locks[0].release()
        else:
            print("deadlock observed on thread 2")
        locks[1].release()

count1_thread = threading.Thread(target=count1, args=(N,))
count2_thread = threading.Thread(target=count2, args=(N,))
t1 = time.perf_counter()
count1_thread.start()
count2_thread.start()
count1_thread.join()
count2_thread.join()
t2 = time.perf_counter()
print(f"Elaspsed time: {(t2 - t1)*1000 :.3f}\t\t counts {counters}")



