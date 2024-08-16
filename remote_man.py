""" Remote Manager"""

import multiprocessing
import multiprocessing.managers
import multiprocessing.process
import threading
import time 

IP_ADDRESS='127.0.0.1'
PORT=50000
AUTHKEY=b'ABC'

class SharedList():
    """ Shared list of numbers shared by processes"""
    def __init__(self):
        self.list=[1,2,3,4]
    def getdata(self):
        return self.list 
    def setdata(self, value, index):
        self.list[index]=value 

_sharedList=SharedList()
def SharedList():
    """ Instance of SharedList"""
    return _sharedList 

class SharedListProxy(multiprocessing.managers.BaseProxy):
    """proxy which redirects methods to the server object"""
    _exposed_ = ('setdata', 'getdata')
    def get_data(self):
        return self._callmethod('getdata')
    def set_data(self, value: tuple):
        return self._callmethod('setdata', (value,))

class CustomManager(multiprocessing.managers.SyncManager):
    """ Inherit custom manager"""
    pass 

CustomManager.register("SharedList", callable=SharedList, proxytype=SharedListProxy)

def some_func(sharedlist, lock: threading.Lock):
    """Worker processes set sharedlist object"""
    with lock:
        print(f'{multiprocessing.process.current_process().name} process acquired lock')
        # do nothing
        
if __name__ == '__main__':
    proc_manager = CustomManager(address=(IP_ADDRESS,PORT), authkey=AUTHKEY)
    # proc_manager.start()
    # sharelist = proc_manager.SharedList() # shared SharedList object 
    # lock = proc_manager. # shared Lock object 
    # p1 = multiprocessing.Process(target=some_func, args=(vector3,lock), name="vultron")
    # p1.start()
    # proc_manager.join()
    # print(sharelist.get_data())
    print(proc_manager.address)
    s=proc_manager.get_server() # get server object 
    s.serve_forever()


    # p1.join() 