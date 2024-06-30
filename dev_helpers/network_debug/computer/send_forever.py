import argparse
import json
import asyncio
import datetime

def get_parser():
    """
    Generate arg parser for the command line script.

    Returns:
        argparse.ArgumentParser: The argument parser.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Send messages to a microcontroller"
        )
    )

    parser.add_argument(
        "ip_address", help="IP address to send to."
    )

    parser.add_argument(
        "port", help="The port to connect to."
    )

    parser.add_argument(
        "retport", help="The port to return the message to."
    )


    return parser


async def main():
    """
    Entry point for the script.
    """
    parser = get_parser()
    args = parser.parse_args()
    # await send_job(args.ip_address, int(args.port), int(args.retport))

    # while True:
    #     await send_job(args.ip_address, int(args.port), int(args.retport))
    #     for i in range(5, 0, -1):
    #         print(i)
    #         await asyncio.sleep(1)

    await keep_connection(args.ip_address, int(args.port), int(args.retport))



async def keep_connection(ip_addr, port, ret_port):

    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip_addr, port),
            timeout=3.0
        )
    except ConnectionRefusedError:
        print("Connection refused.")
        return
    except asyncio.TimeoutError:
        print("Connection Timeout.")
        return


    while True:
        await asyncio.sleep(5)

        data = {
            "msg": str(datetime.datetime.now()),
            "ret_prt": ret_port,
        }
        data_str = json.dumps(data)
        print(f"Sending: {data_str}")
        data_bytes = data_str.encode("ascii")

        to_send = bytearray(2)
        to_send.extend(data_bytes)
        uint16_len_bytes = len(data_bytes).to_bytes(2, "big")
        to_send[0] = uint16_len_bytes[0]
        to_send[1] = uint16_len_bytes[1]
        writer.write(to_send)
        await writer.drain()

        socket_data = await reader.read(2)
        data_length = int.from_bytes(socket_data, "big")

        print(f"There are {data_length} bytes of data to read.")

        if data_length == 0:
            print("No more bytes to read, sending some more")

        # Read the rest of the data
        print(f"Reading remaining {data_length} bytes")
        socket_data = await reader.read(data_length)
        data_str = socket_data.decode("ascii")
        print(f"Received: {data_str}")
        print("Waiting, then sending more data")


async def send_job(ip_addr, port, ret_port):
    # This will raise a OSError: [WinError 121] The semaphore timeout period has expired
    # But putting it in the wait_for seems to prevent that from happening...
    # reader, writer = await asyncio.open_connection(
    #     ip_addr, port)

    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip_addr, port),
            timeout=3.0
        )
    except ConnectionRefusedError:
        print("Connection refused.")
        return
    except asyncio.TimeoutError:
        print("Connection Timeout.")
        return


    data = {
        "msg": str(datetime.datetime.now()),
        "ret_prt": ret_port,
    }
    data_str = json.dumps(data)
    print(f"Sending: {data_str}")
    data_bytes = data_str.encode("ascii")

    to_send = bytearray(2)
    to_send.extend(data_bytes)
    uint16_len_bytes = len(data_bytes).to_bytes(2, "big")
    to_send[0] = uint16_len_bytes[0]
    to_send[1] = uint16_len_bytes[1]
    writer.write(to_send)

    # Close out the connection
    await writer.drain()
    writer.close()
    await writer.wait_closed()
    # reader.close()
    # await reader.wait_closed()
    print("Connection closed")


if __name__ == "__main__":
    asyncio.run(main())