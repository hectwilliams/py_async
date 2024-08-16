""" Custom Process Manager

    Similar to sync_man_custom.py with a custom proxy

"""

import multiprocessing 
import multiprocessing.managers
import multiprocessing.pool
import multiprocessing.process
import threading
import time 

class Vector3():
    
    """ 3D vector. This custom datatype will be registered to process manager."""
    
    def __init__(self):
        self.x=0 
        self.y=0
        self.z=0
    def setxy(self, value:tuple):
        self.x=value[0] 
        self.y=value[1]
        self.z=value[2]
    def getxy(self):
        return (self.x, self.y, self.z)
    vector = property(getxy, setxy)

class Vector3Proxy(multiprocessing.managers.BaseProxy):
    
    """proxy which redirects methods to the server object"""

    _exposed_ = ('setxy', 'getxy')
    def get(self):
        return self._callmethod('getxy')
    def set(self, value: tuple):
        return self._callmethod('setxy', (value,))
    value = property(get, set) 

class CustomManager(multiprocessing.managers.SyncManager):
    """ Inherit custom manager"""
    pass 

CustomManager.register("vector3", callable=Vector3, proxytype=Vector3Proxy)

def some_func(vector3: Vector3, lock: threading.Lock):
    """Worker processes set vector3 object"""
    with lock:
        print(f'{multiprocessing.process.current_process().name} process acquired lock')
        vector3.value = (0,0,1)

if __name__ == '__main__':
    proc_manager = CustomManager()
    proc_manager.start()
    vector3 = proc_manager.vector3() # shared vector3 object 
    lock = proc_manager.Lock() # shared lock object 
    p1 = multiprocessing.Process(target=some_func, args=(vector3,lock), name="vultron")
    p1.start()
    p1.join() 
    print(vector3.value)
