"""Coroutine suspend and restart a task"""

import asyncio
import threading
import time 

async def count_n(n):
    ''' coroutine counts and returns sum'''
    
    print("task_co run") # 'main' coroutine logic
    result = 0
    for i in range(1, n + 1):
        result += i
        print(i)
    print("task_co sleep")
    await asyncio.sleep(2.3)
    print("task_co awake")
    return result 

async def main(val):
    '''main_co, which calls other coroutines with await'''

    print('main_co run')
    task1 = asyncio.create_task(count_n(5)) # add 'count_n' task to event loop
    print("main_co suspend") # 'main' coroutine logic
    await asyncio.sleep(1) # 'main' coroutine logic; coroutine is suspended not the main thread!
    print("main_co awake")    
    try:
        result_t1 = task1.result()
        print("task1 will not require await")
    except asyncio.exceptions.InvalidStateError:
        print("main_co waits on task_co")    
        result_t1 = await task1 # wait for task to complete
    print(f'task_co result\t {result_t1}')
    return val # 'main' coroutine logic

async def main2(val):
    '''Similar to main() function, but there is no task. Only coroutine'''

    print('main_co run')
    print("main_co suspend") 
    await asyncio.sleep(2) 
    print("main_co awake")    
    print("main_co waits on task_co")    
    result_t1 = await count_n(5) 
    print(f'task_co result\t {result_t1}')
    return val 

def run_coroutine_example():
    ''' task_co added to event queue: task_co may run as a task and a coroutine'''
    t1= time.perf_counter()
    result = asyncio.run(main=(main(22))) # setup event loop ( main loop lives in event loop island until return)
    print(f'main_co result {result}')
    t2= time.perf_counter()
    print(f'time elasped {(t2 - t1) * 1000:.3f} msec' )

if __name__ == '__main__':
    run_coroutine_example()