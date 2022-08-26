import asyncio
import json
import sys

async def tcp_echo_client(data):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    await asyncio.sleep(5)

    writer.write("foo".encode(encoding="utf-8"))
    await writer.drain()

    print(f"Writer closed? {writer.is_closing()}")

    writer.close()
    await writer.wait_closed()

    print(f"Writer closed? {writer.is_closing()}")

    # print(f'Send: {data!r}')
    # send_json_string = json.dumps(data)
    # writer.write(send_json_string.encode(encoding="utf-8"))

    # recieved = await reader.read(100)
    # if recieved:
    #     recieve_json_string = recieved.decode(encoding="utf-8")
    #     print(f'Received raw: {recieve_json_string!r}')
    #     recieved_to_object = json.loads(recieve_json_string)
    #     print(f"recieved json {recieved_to_object}")
    # else:
    #     print("recieved was not truthy")
    #     print(recieved)

    # print('Close the connection')
    # writer.close()


def main():
    data = {
        "a":1,
        "prog": [
            [1, 100],
            [2, 200],
        ]
    }

    if len(sys.argv) > 1:
        data["cmdl_args"] = sys.argv[1]

    asyncio.run(tcp_echo_client(data))

if __name__ == "__main__":
    main()