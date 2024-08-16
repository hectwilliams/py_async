"""Client watches server for changes and updates vector point"""
import matplotlib.pyplot as plt
import multiprocessing
import multiprocessing.managers
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
    val=property(get, set)
class ClientCustomManager(multiprocessing.managers.BaseManager):
    pass 
ClientCustomManager.register("Vector3", proxytype=Vector3ListProxy)

if __name__ == '__main__':
    rng = np.random.Generator(PCG64())
    cli_proc_manager = ClientCustomManager(address=(IP_ADDRESS, PORT), authkey=AUTHKEY)
    remote_man_cli_2_helper.wait_for_server(cli_proc_manager)
    vector3 = cli_proc_manager.Vector3()

    ax = plt.figure().add_subplot(projection='3d')
    x = np.linspace(0, 1, 100)
    y = np.sin(x*2*np.pi)/2 + 0.5
    ax.plot(x, y, zs=0, zdir='z', label='curve on (x,y) plane')

    ax.legend()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(0, 1)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    for i in range(100):
        x = vector3.val[0]
        y = vector3.val[1]
        z = vector3.val[2]
        s= ax.scatter(x, y, zs=0, zdir='y')
        plt.pause(0.01)
        s.remove()
