'''Canceling a task shared by single thread'''

import asyncio 

async def test1(msg):
    # 4) thread running task (event loop task)
    print("task_co running")
    try:
        print("task_co sleep")
        # 5) task gives up control of thread
        await asyncio.sleep(0)
        print("task_co awake")
    except asyncio.exceptions.CancelledError:
        print("[EXCEPTION]: CANCEL ERROR, TASK STARTED")
    # 9) tasks get control of thread 
    return msg
async def main():
    # 2) task added to event loop 
    t1=asyncio.create_task(test1("tron")) 
    # 3) main gives up control of thread 
    await asyncio.sleep(0) 
    # 6) main regains control of thread 
    print('task_co cancel')
    # 7) main cancels task 
    t1.cancel() # if placed before sleep, tasks cancels safely 
    print("hello from main")
    # 8) main gives up control of thread 
    await asyncio.sleep(0)
    # 10) main regain control of thread 
    print(t1.result())
asyncio.run(main()) # 1) main thread runs 'main' and starts event loop

