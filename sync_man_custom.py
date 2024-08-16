""" Custom Process Manager

    Similar to sync_man.py, sharing a custom data type object 

"""

import multiprocessing 
import multiprocessing.managers
import multiprocessing.pool
import time 


class CustomManager(multiprocessing.managers.BaseManager):
    """ Inherit custom manager"""
    pass 

class Vector3():
    
    """ 3D vector. This custom datatype will be registered to process manager."""
    
    def __init__(self):
        self._x=0 
        self._y=0
        self._z=0
    def setxy(self,x,y,z):
        self._x=x 
        self._y=y
        self._z=z
    def getxy(self):
        return (self._x, self._y, self._z)

def some_func(vector3: Vector3):
    """Worker processes set vector3 object"""
    vector3.setxy(0,0,1)

CustomManager.register("vector3", Vector3)

if __name__ == '__main__':
    proc_manager = CustomManager()
    proc_manager.start()
    vector3 = proc_manager.vector3() # read vector3 object 
    p1 = multiprocessing.Process(target=some_func, args=(vector3,))
    p1.start()
    p1.join() 
    print(vector3.getxy())