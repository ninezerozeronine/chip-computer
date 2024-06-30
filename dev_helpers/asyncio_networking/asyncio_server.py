import asyncio

async def handle_echo(reader, writer):

    addr = writer.get_extra_info('peername')
    print(f"Got connection from {addr!r}")

    await asyncio.sleep(1)

    print("Insta closing")
    writer.close()
    await writer.wait_closed()

    # data = await reader.read(100)
    # message = data.decode(encoding="utf-8")
    
    # print(f"Received {message!r} from {addr!r}")

    # # await asyncio.sleep(5)

    # print(f"Send: {message!r}")
    # writer.write(data)
    # await writer.drain()



    # print("Close the connection")
    # writer.close()
    # await writer.wait_closed()

async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())