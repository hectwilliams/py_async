"""async read and write files

    read/write modes
    'w'  write text
    'r'  read text 
    'a'  append text 

    'r+' read + write text 
    'w+' read + write text 
    'a+' append + read text

    'rb' read binary
    'wb' write binary
    'ab' append binary
    'rb+' read + write binary 
    'wb+' read + write binary 
    'ab+' append + read binary 

"""

import aiofiles
import asyncio 

async def io_wr(f):
    """Delayed message simulates a delayed IO task"""
    ticks = 5
    for _ in range(ticks):
        await f.write(b"Not Now\n")
        await asyncio.sleep(0.5) # suspend, try another event in event loop
    await f.write(b"Go Now")
async def hi():
    while True:
        print('hi')
        await asyncio.sleep(2) # suspend, try another event in event loop
async def main():
    fname= "example.txt"
    async with aiofiles.open(file=fname, mode="wb+") as f:
        # add tasks to event loop
        task_1 = asyncio.create_task(io_wr(f))
        _= asyncio.create_task(hi())
        # main suspended and event loop task_1 gets thread
        await task_1 # once task_1 is complete main gets thread
        # nothing more to do 
asyncio.run(main())