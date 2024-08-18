"""Simple webserver using server object"""

import email
import asyncio
import email
import email.utils 

def parse_header(headers):
    message = email.message_from_string(headers)
    return dict(message.items())

async def handle_request(reader:asyncio.StreamReader, writer:asyncio.StreamWriter) -> None:
    headers = "Query: "
    while True:
        line = await reader.readline() 
        line = line.decode('ascii')
        if line == "\r\n":
            break 
        headers += line 
    # Print request from client 
    print(headers)
    print('client request')
    # serve basic html
    html = ("<html><head><title>Test Page</title></head><body>"
            "page content"
            "</p></body></html>"
            "\r\n"
            )
    # header response to client
    headers = ("HTTP/1.1 200 OK\r\n"
               "Content-Type: text/html; charset=UTF-8\r\n"
               "Server:PythonAcyncio\r\n"
               f"Date: {email.utils.formatdate(timeval=None, localtime=False, usegmt=True)}\r\n"
               f"Content-Length:{len(html)}\r\n"
               f"\r\n"
            )
    data = headers.encode("ascii") + html.encode("utf-8")
    writer.write(data)
    await writer.drain() 
    await writer.wait_closed() # handle one rquest and close server 

async def main() -> None:
    server = await asyncio.start_server(client_connected_cb=handle_request, host="", port=8080)
    async with server:
        await server.serve_forever() 

asyncio.run(main())