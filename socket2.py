"""UDP server using socket module"""

import asyncio 
import socket 
import udp_constants
async def main():
    loop = asyncio.get_running_loop()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data=b'hello'
    await loop.sock_connect(sock, (udp_constants.remotehost, udp_constants.port))
    await loop.sock_sendall(sock, data)
asyncio.run(main())