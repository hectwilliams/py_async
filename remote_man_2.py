""" Remote Manager """

import multiprocessing
import multiprocessing.managers
import multiprocessing.process
import threading
from decimal import Decimal
from math import sqrt

IP_ADDRESS='127.0.0.1'
PORT=50000
AUTHKEY=b'abc'

class Vector3():
    """ Custom object shared by processes"""
    def __init__(self,x=0, y=0, z=0):
        self.x=x
        self.y=y
        self.z=z
        self.lock = None 
        self.cli_rdy = [False]*2
    def getxyz(self):
        return (self.x, self.y, self.z) 
    def setxyz(self, value):
        self.x=value[0]
        self.y=value[1]
        self.z=value[2]

        if self.x < 0 :
            self.x = 0
        if self.x > 1 :
            self.x = 1
        
        if self.y < 0 :
            self.y = 0
        if self.y > 1 :
            self.y = 1
        
        if self.z < 0 :
            self.z = 0
        if self.z > 1 :
            self.z = 1         
            
    vector=property(getxyz,setxyz)
    def mag(self):
        return Decimal(sqrt(self.x**2 + self.y**2 + self.z**2)).quantize(Decimal('0.000001'))
    def mult_k(self, k):
        self.x =self.x*k
        self.y =self.y*k
        self.z =self.z*k
        return self.getxyz()
    def mult_tuple(self, arr):
        self.x = self.x*arr[0]
        self.y = self.y*arr[1]
        self.z = self.z*arr[2]
        return self.getxyz()

_Vector3=Vector3()
def Vector3():
    return _Vector3 

class Vector3ListProxy(multiprocessing.managers.BaseProxy):
    _exposed_=('getxyz','setxyz', 'mag', 'mult_k', 'mult_tuple', 'load_lock') # methods supported by local and remote proxies
class CustomManager(multiprocessing.managers.BaseManager):
    pass 
CustomManager.register("Vector3", callable=Vector3, proxytype=Vector3ListProxy)

if __name__ == '__main__':
    proc_manager = CustomManager(address=(IP_ADDRESS,PORT), authkey=AUTHKEY)
    print(f'server listening on {proc_manager.address}')
    s=proc_manager.get_server() # get server object 
    s.serve_forever()