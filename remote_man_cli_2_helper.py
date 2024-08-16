"""Helper functions for remote_man clients 
"""
import multiprocessing
import multiprocessing.managers
import time
import sys 

def wait_for_server(client: multiprocessing.managers.BaseManager):
    flag_rdy = False 
    while True:
        try:
            client.connect()
            break
        except ConnectionError:
            if not flag_rdy:
                flag_rdy = (print("program waiting for server to start", file=sys.stderr)) or True
        time.sleep(0.5)