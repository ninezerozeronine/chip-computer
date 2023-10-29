from keypad import Keypad
from queue import Queue
import secrets

from machine import Pin
import asyncio
import network
import ujson


def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to network")
        wlan.connect(secrets.NETWORK_SSID, secrets.NETWORK_PASSWORD)
        while not wlan.isconnected():
            pass
        
    print("Connected!")
    print(wlan.ifconfig())

# https://github.com/micropython/micropython-lib/blob/master/python-stdlib/functools/functools.py
def partial(func, *args, **kwargs):
    def _partial(*more_args, **more_kwargs):
        kw = kwargs.copy()
        kw.update(more_kwargs)
        return func(*(args + more_args), **kw)

    return _partial

async def keypad_update(keypad):
    while True:
        keypad.update()
        await asyncio.sleep(0.1)


async def queue_processor(queue):
    while True:
        job = await queue.get()
        source = job.get("source")
        if source == "keypad":
            if job.get("function") == "print_msg":
                msg = job["args"][0]
                print(msg)
                if msg == "A":
                    num_secs = 6
                    for i in range(num_secs):
                        print(f"Sleeping for second {i + 1} of {num_secs}")
                        await asyncio.sleep(1)
                else:
                    pass
                    # await asyncio.sleep(1)
        elif source == "remote":
            if job.get("function") == "print_msg":
                # print(f"Will send message to {job["return_ip"]}:8889 that execution of job {job["id"]} has begun")
                await send_update(
                    job["return_ip"],
                    8889,
                    f"Job {job["id"]} has begun."
                )
                msg = job["args"][0]
                print(msg)
                if msg == "A":
                    num_secs = 6
                    for i in range(num_secs):
                        print(f"Sleeping for second {i + 1} of {num_secs}")
                        await asyncio.sleep(1)
                else:
                    pass
                    # await asyncio.sleep(1)
                # print(f"Will send message to {job["return_ip"]}:8889 that execution of job {job["id"]} has completed")
                await send_update(
                    job["return_ip"],
                    8889,
                    f"Job {job["id"]} has completed."
                )
        else:
            print("Unknown job source: {source}")


async def send_update(ip_addr, port, message):
    # try:
    #     reader, writer = await asyncio.wait_for(
    #         asyncio.open_connection(ip_addr, port),
    #         timeout=5.0
    #     )
    # # except ConnectionRefusedError:
    # #     print("Connection was refused. (How rude.)")
    # #     return
    # except asyncio.TimeoutError:
    #     print("Connection Timeout!")
    #     return

    reader, writer = await asyncio.open_connection(ip_addr, port)

    print(f"Sending message: {message} to ip {ip_addr} on port {port}")
    writer.write(message.encode("ascii"))
    await writer.drain()

    print('Close the connection in send update')
    writer.close()
    await writer.wait_closed()

    reader.close()
    await reader.wait_closed()


async def handle_socket_conn(queue, reader, writer):

    addr = writer.get_extra_info('peername')
    print(f"Got connection from {addr!r}")

    # print("Sleeping for 1 second")
    # await asyncio.sleep(1)

    recd_bytes = await reader.read(-1)
    # print(f"Got {recd_bytes.decode("ascii")} as data.")
    # data = recd_bytes.decode("ascii")
    try:
        data = ujson.loads(recd_bytes.decode("ascii"))
    except ValueError:
        writer.write("Unable to decode data as json".encode("ascii"))
        await writer.drain()

        print("Close the connection")
        writer.close()
        await writer.wait_closed()
        return

    if "id" not in data:
        writer.write("Job missing id key".encode("ascii"))
        await writer.drain()

        print("Close the connection")
        writer.close()
        await writer.wait_closed()
        return

    if "function" not in data:
        writer.write("Job missing function key".encode("ascii"))
        await writer.drain()

        print("Close the connection")
        writer.close()
        await writer.wait_closed()
        return

    print(f"Received {data!r} from {addr!r}")

    data["source"] = "remote"
    data["return_ip"] = addr[0]
    # data["return_ip"] = "123.123.123.123"

    queue.put_nowait(data)

    # print("Sending some data")
    writer.write(f"Job: {data["id"]} recieved.".encode("ascii"))
    await writer.drain()

    print("Close the connection in handle socket conn")
    writer.close()
    await writer.wait_closed()


async def pulse():
    while True:
        print("pulse")
        await asyncio.sleep(5)



def make_keypad_job(msg):
    return {
        "id":123,
        "source":"keypad",
        "function": "print_msg",
        "args": [msg],
        "kwargs": {},
    }


def main():

    connect()

    row_pins = [
        Pin(9),
        Pin(8),
        Pin(7),
        Pin(6),
    ]
    column_pins = [
        Pin(5),
        Pin(4),
        Pin(3),
        Pin(2),
    ]

    keypad = Keypad(row_pins, column_pins)

    job_queue = Queue()

    keypad.set_pressed_callback(0, 0, partial(job_queue.put_nowait, make_keypad_job("1")))
    keypad.set_pressed_callback(0, 1, partial(job_queue.put_nowait, make_keypad_job("2")))
    keypad.set_pressed_callback(0, 2, partial(job_queue.put_nowait, make_keypad_job("3")))
    keypad.set_pressed_callback(0, 3, partial(job_queue.put_nowait, make_keypad_job("A")))
    keypad.set_pressed_callback(1, 0, partial(job_queue.put_nowait, make_keypad_job("4")))
    keypad.set_pressed_callback(1, 1, partial(job_queue.put_nowait, make_keypad_job("5")))
    keypad.set_pressed_callback(1, 2, partial(job_queue.put_nowait, make_keypad_job("6")))
    keypad.set_pressed_callback(1, 3, partial(job_queue.put_nowait, make_keypad_job("B")))
    keypad.set_pressed_callback(2, 0, partial(job_queue.put_nowait, make_keypad_job("7")))
    keypad.set_pressed_callback(2, 1, partial(job_queue.put_nowait, make_keypad_job("8")))
    keypad.set_pressed_callback(2, 2, partial(job_queue.put_nowait, make_keypad_job("9")))
    keypad.set_pressed_callback(2, 3, partial(job_queue.put_nowait, make_keypad_job("C")))
    keypad.set_pressed_callback(3, 0, partial(job_queue.put_nowait, make_keypad_job("*")))
    keypad.set_pressed_callback(3, 1, partial(job_queue.put_nowait, make_keypad_job("0")))
    keypad.set_pressed_callback(3, 2, partial(job_queue.put_nowait, make_keypad_job("#")))
    keypad.set_pressed_callback(3, 3, partial(job_queue.put_nowait, make_keypad_job("D")))

    keypad_task = asyncio.create_task(keypad_update(keypad))

    queue_processor_task = asyncio.create_task(queue_processor(job_queue))

    pulse_task = asyncio.create_task(pulse())



    socket_handler = partial(handle_socket_conn, job_queue)

    server = await asyncio.start_server(
        socket_handler,
        host='0.0.0.0',
        port=8888
    )

    await asyncio.gather(
        keypad_task,
        queue_processor_task,
        pulse_task,
    )

    print("asyncio done!")

if __name__ == "__main__":
    asyncio.run(main())

def dev_main():
    asyncio.run(main())