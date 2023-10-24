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

    parser.add_argument(
        "-j",
        "--job",
        help="The job to send"
    )

    return parser


async def main():
    """
    Entry point for the script.
    """
    parser = get_parser()
    args = parser.parse_args()
    await send_job(args.ip_address, int(args.port), args.message, job=args.job)

async def send_job(ip_addr, port, message, job=None):
    # This will raise a OSError: [WinError 121] The semaphore timeout period has expired
    # But putting it in the wait_for seems to prevent that from happening...
    # reader, writer = await asyncio.open_connection(
    #     ip_addr, port)

    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip_addr, port),
            timeout=5.0
        )
    except ConnectionRefusedError:
        print("Connection was refused. (How rude.)")
        return
    except asyncio.TimeoutError:
        print("Connection Timeout!")
        return

    if job is None:
        job = {
            "id":"1A2B3C",
            "function": "print_msg",
            "args": [message]
        }
    else:
        print(job)
        job=json.loads(job)

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