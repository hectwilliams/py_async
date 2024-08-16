""" Client connect to remote server"""

import multiprocessing
import multiprocessing.managers
import multiprocessing.process
import threading
import time 

IP_ADDRESS='127.0.0.1'
PORT=50000
AUTHKEY=b'ABC'

class Vector3ListProxy(multiprocessing.managers.BaseProxy):
    _exposed_=('getxyz','setxyz')
    def get(self):
        return self._callmethod('getxyz')
    def set(self, value):
        return self._callmethod('setxyz', value)
    vector=property(get, set)
    
class ClientCustomManager(multiprocessing.managers.BaseManager):
    pass 
ClientCustomManager.register("Vector3", proxytype=Vector3ListProxy)

if __name__ == '__main__':
    cli_proc_manager = ClientCustomManager(address=(IP_ADDRESS, PORT), authkey=AUTHKEY)
    cli_proc_manager.connect()
    vector3 = cli_proc_manager.Vector3()
    vector3.set((0,0,1)) # client writes to remote server
    data = vector3.get()
    print(data) 