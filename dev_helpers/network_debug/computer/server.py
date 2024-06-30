import asyncio

async def handle_connection(reader, writer):

    addr = writer.get_extra_info('peername')
    print(f"Got connection from {addr!r}")

    # Read first 2 bytes to determine how much data was sent
    socket_data = await reader.read(2)
    data_length = int.from_bytes(socket_data, "big")

    print(f"There are {data_length} bytes of data to read.")

    if data_length == 0:
        print("No more bytes to read, closing writer")
        writer.close()
        await writer.wait_closed()
        return

    # Read the rest of the data
    print(f"Reading remaining {data_length} bytes")
    socket_data = await reader.read(data_length)
    data_str = socket_data.decode("ascii")
    print(f"Received: {data_str}")

    # Close out the connection
    print("Message recieved, closing writer")
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(
        handle_connection,
        "0.0.0.0",
        8899
    )

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    # async with server:
    #     await server.serve_forever()


    while True:
        print("Alive")
        await asyncio.sleep(10)
    # await server.serve_forever()



asyncio.run(main())