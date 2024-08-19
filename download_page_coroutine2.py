"""Download page asynchrounously high level Stream coroutines"""

import asyncio
import aiohttp

URL = 'https://www.example.com'

async def hello():
    print("hello world")
async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            task = asyncio.create_task(hello())
            await asyncio.sleep(0) # main thread suspends and runs event loop
            print("Status", response.status)
            print("Content-Length", response.content_length)
            print("Content-Type", response.content_type)
            html = await response.text() 
            print(html[:15])
asyncio.run(main())

