import asyncio

async def handle_connection(reader, writer):

    addr = writer.get_extra_info('peername')
    print(f"Got connection from {addr}")

    recd_bytes = await reader.read(-1)
    data = recd_bytes.decode(encoding="ascii")
    
    print(f"Received {data} from {addr}")

    print("Close the connection")
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(
        handle_connection,
        host='0.0.0.0',
        port=8889
    )

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

    await chatty()


async def chatty():
    while True:
        await asyncio.sleep(5)
        print("Server running")

asyncio.run(main())