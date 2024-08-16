""" Two threads deadlock ( via context manager )"""

import threading
import time 

counters = [0,0]
N = round(1000)
TIMEOUT = 0.6
locks = [lock() for lock in [threading.Lock] * 2]

def timelock(lock, blocking=True, timeout=-1) -> object:
    """Generate and return context manager object"""
    
    class lock_cxt:
        def __enter__(self) -> None:
            if not lock.acquire(blocking, timeout):
                raise RuntimeError("Deadlock?")
        def __exit__(self, exception_type, exception_value, traceback)-> None:
            lock.release()
    return lock_cxt()

def count1(n) -> None: 
    """local thread counts main counters[0] and axuillary counters[1]"""

    for _ in range(n):
        try:
            with timelock(locks[0]):
                counters[0] += 1
                with timelock(locks[1], timeout=TIMEOUT):
                    counters[1] += 1
        except Exception:
            print("Deadlock Thread 1 on counter 2")

def count2(n) -> None:
    """local thread counts main counters[1] and axuillary counters[0]"""
    
    for _ in range(n):
        try:
            with timelock(locks[1]):
                counters[1] += 1
                with timelock(locks[0], timeout=TIMEOUT):
                    counters[0] += 1
        except Exception:
            print("Deadlock Thread 2 on counter 1")

count1_thread = threading.Thread(target=count1, args=(N,))
count2_thread = threading.Thread(target=count2, args=(N,))
t1 = time.perf_counter()
count1_thread.start()
count2_thread.start()
count1_thread.join()
count2_thread.join()
t2 = time.perf_counter()
print(f"Elaspsed time: {(t2 - t1)*1000 :.3f}\t\t counts {counters}")