""" Process manager 

    Server running on individual process controls interoperability of shared resource with worker processes 

"""

import multiprocessing
import multiprocessing.pool
import time 

def some_func(sh_list):
    """shared list(i.e. x) items are squared and reassigned
    
    Args:
        x: list object created by process management server 
    """

    for i in range(len(sh_list)):
        sh_list[i] = sh_list[i]**2

if __name__ == '__main__':
    proc_manager = multiprocessing.Manager() 
    proxy_shared_list = proc_manager.list([1, 2, 3, 4, 5, 6]) # create shared list in server
    p1 = multiprocessing.Process(target=some_func, args=(proxy_shared_list,))
    p2 = multiprocessing.Process(target=some_func, args=(proxy_shared_list,))
    t1 = time.perf_counter()
    p1.start() # process executes on proxy shared data 
    p2.start()
    p1.join() 
    p2.join()
    t2 = time.perf_counter() 
    print(f'Delay {(t2-t1)*1000 :.3f} milliseconds')
    print(proxy_shared_list)


