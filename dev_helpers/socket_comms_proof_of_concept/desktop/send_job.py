import argparse
import json
from pprint import pprint
import asyncio

def get_parser():
    """
    Generate arg parser for the command line script.

    Returns:
        argparse.ArgumentParser: The argument parser.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Send a job to the Pi Pico"
        )
    )

    parser.add_argument(
        "ip_address", help="IP address to send to."
    )

    parser.add_argument(
        "port", help="The port to connect to."
    )

    parser.add_argument(
        "message", help="The message to send."
        )

    return parser


async def main():
    """
    Entry point for the script.
    """
    parser = get_parser()
    args = parser.parse_args()
    await send_job(args.ip_address, int(args.port), args.message)

async def send_job(ip_addr, port, message):
    reader, writer = await asyncio.open_connection(
        ip_addr, port)

    job = {
        "id":"1A2B3C",
        "function": "print_msg",
        "args": [message]
    }

    print(f"Sending job:")
    pprint(job)
    writer.write(json.dumps(job).encode("ascii"))
    writer.write_eof()
    await writer.drain()

    data = await reader.read()
    print(f'Received: {data.decode("ascii")}')

    print('Close the connection')
    writer.close()

if __name__ == "__main__":
    asyncio.run(main())