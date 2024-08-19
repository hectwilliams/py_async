"""Create UDP server"""
import asyncio 
from udp_constants import localhost, remotehost, port

async def main():
    loop = asyncio.get_running_loop()
    # connect to local network address
    transport, protocol = await loop.create_datagram_endpoint(protocol_factory=lambda: asyncio.DatagramProtocol(), local_addr=(localhost, port))
    # write to available host address (consumer)
    for _ in range(10):
        data = b'Hello World from UDP'
        transport.sendto(data, addr=(remotehost, port))
        transport.close()
asyncio.run(main())