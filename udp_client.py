"""Create UDP client"""
import asyncio
from udp_constants import remotehost, port

class ClientDatagramProtocol(asyncio.DatagramProtocol):
    def datagram_received(self, data, addr) -> None:
        message = data.decode('utf-8')
        print('Rcvd', message, 'from', addr)
async def main():
    loop = asyncio.get_running_loop() 
    transport, protocol = await loop.create_datagram_endpoint(lambda: ClientDatagramProtocol(), local_addr=(remotehost, port))
    await asyncio.sleep(1000)
    transport.close()
asyncio.run(main())