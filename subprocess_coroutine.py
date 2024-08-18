"""Asynchronous subpross"""

import asyncio

child_process_file = 'remote_man_2_child_process.py'

async def respond_to_child_process(p):
    p.stdin.write(b"tron\n")
async def main():
    p = await asyncio.create_subprocess_exec('python', child_process_file, stdout=asyncio.subprocess.PIPE, stdin=asyncio.subprocess.PIPE)
    asyncio.create_task(respond_to_child_process(p))
    msg = await p.stdout.readline()
    print(msg)
    msg = await p.stdout.readline()
    print(msg)
asyncio.run(main())