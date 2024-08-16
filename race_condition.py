"""Execute race conditioned counter using two local threads"""

from cmath import sqrt
import threading
import time 

my_counter = 0

def count():
    global my_counter 
    for i in range(100000):
        temp = my_counter + 1
        x = sqrt(2) # thread suspends releasing GIL to ecexute C Librarie's sqrt function
        my_counter = temp 

thread1 = threading.Thread(target=count)
thread2 = threading.Thread(target=count)
t1 = time.perf_counter()
thread1.start()
thread2.start()
thread1.join()
thread2.join()
t2 = time.perf_counter() 
print(f"Time elasped {(t2-t1)*1000} global counter")
print(my_counter)

