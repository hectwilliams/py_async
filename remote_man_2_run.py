""" Scripts"""

import subprocess
import os
import time
import sys 
import threading
import queue

python_files = [
    'remote_man_2.py',
    'remote_man_cli_2_plotter.py',
    'remote_man_cli_2.py'
]
child_process_file = 'remote_man_2_child_process.py'

def run_remote_man_2():
    child_processes = []
    for f in python_files:
        child_processes.append(subprocess.Popen(['python', f]))
    # child_processes[0].wait()
    # child_processes[1].wait()
    # child_processes[2].wait()

def run_command():
    ret = subprocess.run(['python', child_process_file, '-i'], input=b"y\n", capture_output=True) # capture_output returns stdout and stderr attributes
    print(ret.stderr)
    print(ret.stdout)

def pipe_command():
    """Synchronous pipe read"""
    p = subprocess.Popen(['python', child_process_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE) # capture_output returns stdout and stderr attributes

    # child asks question
    rcvd = p.stdout.readline()
    print("msg", rcvd)
    
    # parent responds to child
    p.stdin.write(b"tron\n")
    p.stdin.flush()  

    # child response to parent 
    rcvd = p.stdout.readline()
    print("msg", rcvd)

class AsyncReader():
    """ inefficient async byte reader """

    def __init__(self, stream):
        self._stream = stream 
        self._char = ''
        self._thr = threading.Thread(target=self._get, daemon=True)
        self._thr.start()
    def _get(self):
        self._char = self._stream.read(1) # used by thread, thread is alive until it reads a byte character 
    def get(self):
        self._thr.join(0.10)
        if self._thr.is_alive():
            return ""
        else:
            result = self._char 
            self._thr = threading.Thread(target=self._get, daemon=True)
            self._thr.start()
            return result 
    def read_message(self):
        ans = "" 
        while True:
            char = self.get()
            if char == "":
                break 
            else:
                ans += char
        return ans 

class AsyncReaderV2():
    """ efficient async byte reader using single thread and queue """

    def __init__(self, stream):
        self._queue= queue.Queue()
        self._stream = stream 
        self._char = ''
        self._thr = threading.Thread(target=self._get, daemon=True)
        self._thr.start()
    def _get(self):
        while True:
            self._char = self._stream.read(1) 
            if self._char:
                self._queue.put(self._char)
    def get(self):
        result = ""
        self._thr.join(0.10)
        curr_queue_size = self._queue.qsize() # prevents need for lock, queue is dynamic 
        for _ in range(curr_queue_size):
            result += self._queue.get()
        return result 
    def read_message(self):
        return self.get()
    
def pipe_command_async():
    """Asynchronous pipe read"""
    p = subprocess.Popen(['python', child_process_file], stdout=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=1, universal_newlines=True) 

    # async reader instance 
    async_read = AsyncReaderV2(p.stdout)

    # child asks question
    rcvd = async_read.read_message()
    print(f'child msg:\t{rcvd}')
    
    # # child responds to user
    p.stdin.write("tron\n")
    
    # # main responds with confirmation 
    rcvd = async_read.read_message()
    print(f'child msg:\t{rcvd}')

pipe_command_async() 