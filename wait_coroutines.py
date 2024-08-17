""" waiting on coroutines"""

import asyncio 
import random

async def counter():
    result = 0
    for _ in range(int(100000)):
        result += 1
    await asyncio.sleep(0.0) 
    return result 
async def rand_counter():
    result = 0
    for num in [random.randint(1, 100) for _ in range(10)]:
        result += num
    return result
async def main(mode=0):
    if mode == 0:
        '''Wait for task to complete'''
        coroutine = counter()
        task = await asyncio.wait_for(coroutine, timeout=float(3))
        print(task)
    elif mode == 1:
        '''Wait for multiple task to complete'''
        task1 = asyncio.create_task(counter())
        task2 = asyncio.create_task(rand_counter())
        done, pending = await asyncio.wait([task1, task2], return_when=asyncio.ALL_COMPLETED)
        for t in done:
            print(t.result())
        print("Coroutines completed")
    elif mode == 2:
        """similar to mode 1, cleaner code"""
        result = await asyncio.gather(counter(), rand_counter())
        print(result)
result_co = asyncio.run(main(2)) # setup event loop
