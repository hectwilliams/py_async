"""
Compute Pi using synchronous 

Compute Pi using different process

Evalute performance of each

"""

import time
import multiprocessing
import threading

def my_pi(m, n):
    """ Compute pi series from m-th to the n-th term
        pi = 4 * (a + b + c + d ...)
        a = 1
        b = -1/3
        c = 1/5 
        d = -1/7


    Args:
        m: m-th number in series to calculate 
        n: n-th number in series to calculate

    Return:
        None 
    
    """

    pi = 0
    for k in range(m, n + 1):
        s = 1 if k%2 else -1
        pi += s / ((2*k)-1)
    print(4 * pi, ":)")

def sync_mode(n):
    """ Compute Pi using single process thread"""

    t1=time.perf_counter()
    my_pi(1, n)
    t2=time.perf_counter() 
    print(f"{n} series compute pi synchronous approach:  {(t2- t1) * 1e3 :.3f} milliseconds\n---\n")

def mulit_process_mode(n):
    """ Compute Pi using 2 processes"""

    p1 = multiprocessing.Process(target=my_pi, args=(n//2 + 1, n))
    t1 = time.perf_counter()
    p1.start() # child process call 
    my_pi(1, N//2) # parent call
    p1.join() # parent suspended, waiting on child 
    t2 = time.perf_counter() 
    print(f"{n} series compute pi parent-child process approach:  {(t2- t1) * 1e3 :.3f} milliseconds\n--\n")

def thread_mode(n):
    """ Compute Pi using multi-threading"""
    
    th1 = threading.Thread(target=my_pi, args=(n//2 + 1, n))
    t1 = time.perf_counter()
    th1.start()
    my_pi(1, n//2)
    th1.join()
    t2 = time.perf_counter()
    print(f"{n} series compute pi thread approach:  {(t2- t1) * 1e3 :.3f} milliseconds\n--\n")

# small N - synchronous single process is faster
# large N - Multi process is faster  
N = round(1e7)

# ensures setup code doesn't get run in child process
if __name__ == '__main__':
    sync_mode(N)
    mulit_process_mode(N)
    thread_mode(N)