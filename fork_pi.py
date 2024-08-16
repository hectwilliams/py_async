""" Fork parent process in python"""

import multiprocessing

def my_process():
    print("Hello Process World")
    print(f"child target process-id \t{multiprocessing.current_process().pid}")

multiprocessing.set_start_method(method='fork')
p1 = multiprocessing.Process(target=my_process)
p1.start() # fork
print(f"parent process-id\t{multiprocessing.current_process().pid}")
print(f"child process-id\t{p1.pid}")
print("finished")
