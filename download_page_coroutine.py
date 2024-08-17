"""Download page asynchrounously high level coroutines(i.e. Streams)"""

import asyncio
import time 
import email  # use to parse HTTP headers
from urllib.parse import urlsplit

URL = 'https://www.example.com'

def parse_header(headers):
    message = email.message_from_string(headers)
    return dict(message.items())
async def headers(reader_co):
    headers = "Status: "
    while True:
        line = await reader_co.readline()
        line = line.decode('ascii')
        if line == "\r\n":
            break 
        headers += line 
    return parse_header(headers)
async def readhtml(reader_co, length):
    html = await reader_co.read(length)
    html = html.decode('utf-8')
    return html
async def download(url):    
    url = urlsplit(url)
    try:
        reader_co, writer_co = await asyncio.open_connection(host=url.hostname, port=443, ssl=True) 
        task_header = asyncio.create_task(headers(reader_co)) # add task to event loop 
        request = (
            f"GET /index.html HTTP/1.1\r\n"
            f"Host: {url.hostname}\r\n"
            f"\r\n"
        )
        writer_co.write(request.encode('ascii')) #write to server
        header = await task_header # server response 
        try:
            task_html = asyncio.create_task(readhtml(reader_co, int(header["Content-Length"])))
            html = await task_html
            return html
        except KeyError:
            print("Content-Length not found in header")
    except TimeoutError:
        print('connection timed out')
    except OSError as error:
        print('error: %r', error)

async def main():
    t1=time.perf_counter()
    result = await download(URL) # wait for co-routine to complete 
    t2=time.perf_counter()
    print(f'{(t2-t1)*1000:.3f} msec')
    if result:
        print()
        print(result)
asyncio.run(main()) # setup event loop 

