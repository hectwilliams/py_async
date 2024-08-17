"""Utilize locks on coroutine"""

import asyncio
import asyncio.locks

async def count():
    global my_counter
    global my_lock 
    for _ in range(1000):
            async with my_lock: # LOCK FIXES RACE CONDITION
                # 4) task_1 write to temp 
                # 6) task_2 write to temp
                temp = my_counter + 1
                # 5) task_1 released thread
                # 7) task_2 released thread
                await asyncio.sleep(0) # LOCK PREVENTS TASK SUSPEND; REMAINING TASKS WAIT UNTIL CURRENT TASK IS COMPLETE 
                # 8) task_1 write temp value to my_counter
                # 10) task_2 write temp value to my_counter
                my_counter = temp 
                # 9) task_1 ends
                # 10) task_2 ends
                print(my_counter)
async def main():
    # 2) add tasks to event loop
    t1=asyncio.create_task(count())
    t2=asyncio.create_task(count())
    # 3) caller suspends main coroutine; thread move to handle event loop
    await asyncio.wait([t1,t2])
    # 11) thread requuired caller coroutine
    print(my_counter, 'AA')
    # 12) caller coroutine ends
    
my_counter = 0
my_lock =asyncio.locks.Lock()
# 1) main thread starts event loop
asyncio.run(main()) 