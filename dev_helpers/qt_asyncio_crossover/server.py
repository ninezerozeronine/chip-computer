import asyncio
import json

async def handle_echo(reader, writer):

    addr = writer.get_extra_info('peername')
    print(f"Got connection from {addr!r}")

    print("Sleeping for 1 second")
    await asyncio.sleep(1)

    recd_bytes = await reader.read(100)
    data = json.loads(recd_bytes.decode(encoding="ascii"))
    
    print(f"Received {data!r} from {addr!r}")

    data["extra"] = "oh hai!"

    print("Sending some data")
    writer.write(json.dumps(data).encode("ascii"))
    await writer.drain()

    print("Close the connection")
    writer.close()
    await writer.wait_closed()

    # print("Closing")
    # writer.close()
    # await writer.wait_closed()

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

    await chatty()

    async with server:
        await server.serve_forever()


async def chatty():
    while True:
        await asyncio.sleep(5)
        print("Hello!")

asyncio.run(main())