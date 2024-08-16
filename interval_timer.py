"""Create Interval Timer using Threading object"""

import threading
import time 

class IntervalTimer(threading.Thread):
    
    def __init__(self, interval, function, args=(None), kwargs=(None)):
        threading.Thread.__init__(self)
        self.interval = interval
        self.function = function 
        self.args = args 
        self.kwargs = kwargs 
        self.finished = threading.Event()
    
    def cancel(self):
        """Set the event flag, canceling the repeated timed function"""
        self.finished.set() 
    
    def run(self):
        """Thread executes a repeated timed function when start() is called."""
        while(True):
            self.finished.wait(self.interval)
            if self.finished.is_set():
                break 
            else:
                self.function(self.args, self.kwargs)

def my_function(args, kwargs):
    """some dummy function"""
    print("function id", threading.current_thread().ident)

interval_timer = IntervalTimer(interval=1, function=my_function)
interval_timer.start()

count = 0
while True:
    count += 1
    print('main-id', threading.current_thread().ident)
    if count == 5:
        interval_timer.cancel() # cancel interval timer thread 
        break 
    time.sleep(1)
interval_timer.join()
    
    