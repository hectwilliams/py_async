"""Introduction to context variable"""

import random 
import asyncio
import contextvars

id_global=0

# ERROR PRONE CODE
def err_produce_func():
    async def inner(id_param):
        global id_global
        # 4) task1 suspends (id_param=a)
        # 6) task2 suspends (id_param=b)
        await asyncio.sleep(0)
        # 7) a != b
        # 9) b == b
        if id_param!=id_global:
            print("error")
        # 8) task1 ends
        # 10) task1 ends
    async def outer():
        global id_global
        id=random.randint(0, 10000)
        # 3) task1 sets global (r=a)
        # 5) task2 sets (id_param=b)
        id_global=id
        await inner(id)
    async def main():
        # 2) add tasks to event loop, and wait on tasks to complete 
        await asyncio.gather(outer(), outer()) 
    # 1) main thread starts event loop
    asyncio.run(main())

def err_free_func():
    """context variable used to make id_param global"""
    id_global_ctx = contextvars.ContextVar('id')
    async def inner(id_param):
        # 4) task1 suspends (id_param=a)
        # 6) task2 suspends (id_param=b)
        await asyncio.sleep(0)
        # 7) task1 a == a (id_global_ctx = a)
        # 9) task1 b == b (id_global_ctx = b)
        print(id_param, id_global_ctx.get(), end= " ")
        if id_param!=id_global_ctx.get():
            print("error", end=" ")
        print()
        # 8) task1 ends
        # 10) task1 ends
    async def outer():
        id=random.randint(0, 10000)
        # 3) task1 sets global context (r=a)
        # 5) task2 sets global context (r=b)
        id_global_ctx.set(id) # each tasks contains a non-shared global
        await inner(id)
    async def main():
        # 2) add tasks to event loop, and wait on tasks to complete 
        await asyncio.gather(outer(), outer()) 
    # 1) main thread starts event loop
    asyncio.run(main())
err_free_func()