from keypad import Keypad
from queue import Queue
import secrets

from machine import Pin
import uasyncio
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
        await uasyncio.sleep(0.1)


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
                        await uasyncio.sleep(1)
                else:
                    pass
                    # await uasyncio.sleep(1)
        elif source == "remote":
            if job.get("function") == "print_msg":
                print("Will send message that execution has begun")
                msg = job["args"][0]
                print(msg)
                if msg == "A":
                    num_secs = 6
                    for i in range(num_secs):
                        print(f"Sleeping for second {i + 1} of {num_secs}")
                        await uasyncio.sleep(1)
                else:
                    pass
                    # await uasyncio.sleep(1)
                print("Will send message that execution has completed")
        else:
            print("Unknown job source: {source}")


# class SocketConnToQueue():
#     def __init__(self, queue):
#         self.queue = queue


async def handle_socket_conn(queue, reader, writer):

    addr = writer.get_extra_info('peername')
    print(f"Got connection from {addr!r}")

    # print("Sleeping for 1 second")
    # await uasyncio.sleep(1)

    recd_bytes = await reader.read(-1)
    # print(f"Got {recd_bytes.decode("ascii")} as data.")
    data = ujson.loads(recd_bytes.decode("ascii"))
    # data = recd_bytes.decode()

    
    print(f"Received {data!r} from {addr!r}")

    data["source"] = "remote"
    data["return_ip"] = addr[0]

    queue.put_nowait(data)

    # data["extra"] = "oh hai!"

    # print("Sending some data")
    # writer.write("fanks".encode("ascii"))
    # await writer.drain()

    print("Close the connection")
    writer.close()
    await writer.wait_closed()


async def pulse():
    while True:
        print("pulse")
        await uasyncio.sleep(5)



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

    keypad_task = uasyncio.create_task(keypad_update(keypad))

    queue_processor_task = uasyncio.create_task(queue_processor(job_queue))

    pulse_task = uasyncio.create_task(pulse())

    socket_handler = partial(handle_socket_conn, job_queue)
    server = await uasyncio.start_server(
        socket_handler,
        '0.0.0.0',
        8888,
    )

    await uasyncio.gather(
        keypad_task,
        queue_processor_task,
        pulse_task,
    )

    print("uasyncio done!")

if __name__ == "__main__":
    uasyncio.run(main())

def dev_main():
    uasyncio.run(main())