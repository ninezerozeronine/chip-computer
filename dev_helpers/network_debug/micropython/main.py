import asyncio
import network
import json

import secrets


async def connect_to_wifi():
    """
    Connect to WiFi network
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.NETWORK_SSID, secrets.NETWORK_PASSWORD)

    max_polls = 10
    for attempt in range(1, max_polls + 1):
        conn_msg = f"Connection update {attempt}/{max_polls}"
        print(conn_msg)
        
        if wlan.isconnected():
            print(f"Connected with IP: {wlan.ifconfig()[0]}")
            return True
        else:
            print(f"Waiting for connection")
            await asyncio.sleep(1)

    print("WiFi not connected")
    return False


async def handle_connection(reader, writer):
    """

    """
    addr = writer.get_extra_info('peername')
    print(f"Got connection from {addr!r}")

    # Read first 2 bytes to determine how much data was sent
    socket_data = await reader.read(2)
    data_length = int.from_bytes(socket_data, "big")

    print(f"There are {data_length} bytes of data to read.")

    if data_length == 0:
        print("No more bytes to read, closing reader and writer")
        reader.close()
        await reader.wait_closed()
        writer.close()
        await writer.wait_closed()
        return

    # Read the rest of the data
    print(f"Reading remaining {data_length} bytes")
    socket_data = await reader.read(data_length)
    data_str = socket_data.decode("ascii")
    print(f"Received {data_str}")

    # Close out the connection
    print("Message recieved, closing reader and writer")
    reader.close()
    await reader.wait_closed()
    writer.close()
    await writer.wait_closed()

    print("Waiting 1 second")
    await asyncio.sleep(1)

    # Process the data recieved
    # Should be a dict like:
    # {"ret_prt": 12345, "msg":"Hello"}
    data = json.loads(data_str)
    port = data["ret_prt"]
    print(f"Connecting to sender IP: {addr[0]}, port: {port}")
    reader, writer = await asyncio.open_connection(
        addr[0],
        port
    )

    to_send = bytearray(2)
    msg = f"Recieved the message: {data["msg"]}"
    msg_bytes = bytes(msg, "ascii")
    to_send.extend(msg_bytes)
    uint16_len_bytes = len(msg_bytes).to_bytes(2, "big")
    to_send[0] = uint16_len_bytes[0]
    to_send[1] = uint16_len_bytes[1]
    print(f"Sending: {msg}")
    writer.write(to_send)

    # Close out the connection
    await writer.drain()
    writer.close()
    await writer.wait_closed()
    reader.close()
    await reader.wait_closed()
    print("Connection closed")


async def handle_connection_persistent(reader, writer):
    """

    """
    addr = writer.get_extra_info('peername')
    print(f"Got connection from {addr!r}")


    while True:
        # Read first 2 bytes to determine how much data was sent
        socket_data = await reader.read(2)
        data_length = int.from_bytes(socket_data, "big")

        print(f"There are {data_length} bytes of data to read.")

        if data_length == 0:
            print("No more bytes to read, waiting for more data")
            continue

        # Read the rest of the data
        print(f"Reading remaining {data_length} bytes")
        socket_data = await reader.read(data_length)
        data_str = socket_data.decode("ascii")
        print(f"Received {data_str}")


        # Process the data recieved
        # Should be a dict like:
        # {"ret_prt": 12345, "msg":"Hello"}
        data = json.loads(data_str)

        to_send = bytearray(2)
        msg = f"Recieved the message: {data["msg"]}"
        msg_bytes = bytes(msg, "ascii")
        to_send.extend(msg_bytes)
        uint16_len_bytes = len(msg_bytes).to_bytes(2, "big")
        to_send[0] = uint16_len_bytes[0]
        to_send[1] = uint16_len_bytes[1]
        print(f"Sending: {msg}")
        writer.write(to_send)
        await writer.drain()


async def main():
    connected = await connect_to_wifi()

    if not connected:
        return

    server = await asyncio.start_server(
        handle_connection_persistent,
        host="0.0.0.0",
        port=8888
    )

    while True:
        print("Alive")
        await asyncio.sleep(10)


asyncio.run(main())