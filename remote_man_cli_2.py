""" Client connect to remote server"""

import multiprocessing
import multiprocessing.managers
import multiprocessing.process
import numbers
import time 
import numpy as np 
from numpy.random import Generator, PCG64
import remote_man_cli_2_helper

IP_ADDRESS='127.0.0.1'
PORT=50000
AUTHKEY=b'abc'

class Vector3ListProxy(multiprocessing.managers.BaseProxy):
    def get(self):
        return self._callmethod('getxyz')
    def set(self, value:tuple):
        return self._callmethod('setxyz', (value,))
    def mag(self):
        return self._callmethod('mag')    
    def __mul__(self, val):
        if type(val) in [float, int]:
            return self._callmethod('mult_k', (val,))
        if [isinstance(ele, numbers.Number) for ele in val] ==[True, True, True] and len(val)==3:
            return self._callmethod('mult_tuple', (val,))
    def __rmul__(self, val):
        return self.__mul__(val)
    val=property(get, set)
    
class ClientCustomManager(multiprocessing.managers.SyncManager):
    pass 
ClientCustomManager.register("Vector3", proxytype=Vector3ListProxy)

if __name__ == '__main__':
    rng= np.random.Generator(PCG64())
    cli_proc_manager = ClientCustomManager(address=(IP_ADDRESS, PORT), authkey=AUTHKEY)
    remote_man_cli_2_helper.wait_for_server(cli_proc_manager)
    vector3 = cli_proc_manager.Vector3()
    vector3.val=(0,0,1)

    # TESTS

    # vector3 * k
    print(f'\n-----\n\tMultiply  {vector3.val} by {3} => {vector3*3}\n-----\n')
    
    # k * vector 
    print(f'\n-----\n\tMultiply {3} by {vector3.val}  => {3*vector3}\n-----\n')

    # vector3 * (x,x,x)
    print(f'\n-----\n\tMultiply  {vector3.val} by {(1,1,2)} => {vector3*(1,1,2)}\n-----\n')

    # (x,x,x) * vector3 
    print(f'\n-----\n\tMultiply {(1,1,2)} by {vector3.val}  => { (1,1,2) * vector3 }\n-----\n')

    # magnitude 
    print(f'\n-----\n\tMagnitude of {vector3.val} => {vector3.mag()}\n-----\n')

    while True:
        vector3.val = (rng.normal(0, 0.3), rng.normal(0, 0.3), rng.normal(0, 0.3))
        time.sleep(0.001)