"""
Program two threads, not including main thread: one daemon and one non-deamone
"""

import threading
import multiprocessing

def my_thread():
    """ Executes a while loop """
    while True:
        pass 

t0 = threading.main_thread()
t1 = threading.Thread(target=my_thread, daemon=False) # thread never ends, program held even after main thread exits (thread has exit priority)
t2 = threading.Thread(target=my_thread, daemon=True) # thread killed when t1 is main thread exits
t1.start()
t2.start()
print(t0.native_id)
print(t1.native_id)
print(t2.native_id)
print("main thread ending")
print(f"current process {multiprocessing.current_process().pid}")




