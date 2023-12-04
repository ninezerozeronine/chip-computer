"""
Main entry point for Micropython functionality
"""

from machine import Pin
import asyncio
import network
import time
import json

from front_panel import FrontPanel
from keypad import Keypad
from gpiodefs import KEYPAD_GPIOS
import secrets
from queue import Queue

PORT = 8888
DEBUG = False

def log(msg):
    if DEBUG:
        print(msg)

# https://github.com/micropython/micropython-lib/blob/master/python-stdlib/functools/functools.py
def partial(func, *args, **kwargs):
    def _partial(*more_args, **more_kwargs):
        kw = kwargs.copy()
        kw.update(more_kwargs)
        return func(*(args + more_args), **kw)

    return _partial


def connect(panel):
    """
    Connect to WiFi

    Args:
        panel (FrontPanel): Front panel object for the Computer.
    Returns:
        bool: True if connection was successful, false if not.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    max_attempts = 5
    if not wlan.isconnected():
        for attempt in range(1, max_attempts + 1):
            panel.set_ip(f"Conn attmpt {attempt}/{max_attempts}")
            wlan.connect(secrets.NETWORK_SSID, secrets.NETWORK_PASSWORD)
            if wlan.isconnected():
                break
            else:
                time.sleep(5)

    if wlan.isconnected():
        panel.set_ip(wlan.ifconfig()[0])
        panel.set_port(str(PORT))
        return True
    else:
        panel.set_ip("No WiFi :(")
        return False

async def run_keypad(keypad):
    """
    Run the keypad

    Args:
        keypad (Keypad): Keypad object.
    """
    while True:
        keypad.update()
        await asyncio.sleep(0.1)

async def handle_socket_conn(queue, panel, reader, writer):
    """
    Handle something connecting to the server

    Expects to be wrapped in a partial, hence reader and writer not
    being the first two args.

    Args:
        queue (Queue): asyncio queue object to put functions to call on.
        panel (FrontPanel): Front pnale object for the Computer.
        reader (Stream): asyncio Stream object for reading.
        writer (Stream):asyncio Stream object for reading.

    """
    addr = writer.get_extra_info('peername')
    log(f"Got connection from {addr!r}")

    recd_bytes = await reader.read(-1)
    try:
        data = json.loads(recd_bytes.decode("ascii"))
    except ValueError:
        writer.write("Unable to decode data as json".encode("ascii"))
        await writer.drain()

        writer.close()
        await writer.wait_closed()
        return

    if "id" not in data:
        writer.write("Job missing id key".encode("ascii"))
        await writer.drain()

        writer.close()
        await writer.wait_closed()
        return

    if "function" not in data:
        writer.write("Job missing function key".encode("ascii"))
        await writer.drain()

        writer.close()
        await writer.wait_closed()
        return

    function = None
    try:
        function = getattr(panel, data["function"])
    except AttributeError:
        pass

    if function is None:
        writer.write(f"Job ID: {data["id"]} - Front Panel class has no {data["function"]} method.".encode("ascii"))
        await writer.drain()

        writer.close()
        await writer.wait_closed()
        return

    args = data.get("args", [])
    kwargs = data.get("kwargs", {})
    queue_callable = partial(function, *args, **kwargs)
    queue.put_nowait(queue_callable)

    writer.write(f"Job: {data["id"]} recieved.".encode("ascii"))
    await writer.drain()

    writer.close()
    await writer.wait_closed()

async def pulse():
    """
    Blink the onboard LED forever
    """
    led_pin = Pin("LED", Pin.OUT)
    while True:
        led_pin.toggle()
        await asyncio.sleep(1)

async def queue_processor(queue):
    """
    Process items on the queue forevever.

    Args:
        queue (Queue): asyncio queue object to put functions to call on.
    """
    while True:
        job = await queue.get()
        job()
        queue.task_done()

def main():
    """
    Main async runner for the computer
    """

    row_pins = [
        Pin(KEYPAD_GPIOS[0]),
        Pin(KEYPAD_GPIOS[1]),
        Pin(KEYPAD_GPIOS[2]),
        Pin(KEYPAD_GPIOS[3]),
    ]
    column_pins = [
        Pin(KEYPAD_GPIOS[4]),
        Pin(KEYPAD_GPIOS[5]),
        Pin(KEYPAD_GPIOS[6]),
        Pin(KEYPAD_GPIOS[7]),
        Pin(KEYPAD_GPIOS[8]),
        Pin(KEYPAD_GPIOS[9]),
        Pin(KEYPAD_GPIOS[10]),
        Pin(KEYPAD_GPIOS[11]),
    ]

    panel = FrontPanel()
    keypad = Keypad(row_pins, column_pins)
    job_queue = Queue()
    connected = connect(panel)

    # Digits on numpbers keypad
    keypad.set_pressed_callback(3, 3, partial(job_queue.put_nowait, partial(panel.propose_user_input_character, "1")))
    keypad.set_pressed_callback(3, 2, partial(job_queue.put_nowait, partial(panel.propose_user_input_character, "2")))
    keypad.set_pressed_callback(3, 1, partial(job_queue.put_nowait, partial(panel.propose_user_input_character, "3")))
    keypad.set_pressed_callback(2, 3, partial(job_queue.put_nowait, partial(panel.propose_user_input_character, "4")))
    keypad.set_pressed_callback(2, 2, partial(job_queue.put_nowait, partial(panel.propose_user_input_character, "5")))
    keypad.set_pressed_callback(2, 1, partial(job_queue.put_nowait, partial(panel.propose_user_input_character, "6")))
    keypad.set_pressed_callback(1, 3, partial(job_queue.put_nowait, partial(panel.propose_user_input_character, "7")))
    keypad.set_pressed_callback(1, 2, partial(job_queue.put_nowait, partial(panel.propose_user_input_character, "8")))
    keypad.set_pressed_callback(1, 1, partial(job_queue.put_nowait, partial(panel.propose_user_input_character, "9")))
    keypad.set_pressed_callback(0, 3, partial(job_queue.put_nowait, partial(panel.propose_user_input_character, ".")))
    keypad.set_pressed_callback(0, 2, partial(job_queue.put_nowait, partial(panel.propose_user_input_character, "0")))

    # Functions on numbers keypad
    keypad.set_pressed_callback(0, 1, partial(job_queue.put_nowait, panel.delete_last_user_input_char))
    keypad.set_pressed_callback(0, 0, partial(job_queue.put_nowait, panel.clear_user_input))
    
    # Control keypad
    keypad.set_pressed_callback(3, 7, partial(job_queue.put_nowait, panel.read_memory))
    keypad.set_pressed_callback(3, 6, partial(job_queue.put_nowait, panel.half_step))
    keypad.set_pressed_callback(3, 5, partial(job_queue.put_nowait, panel.full_step))
    keypad.set_pressed_callback(3, 4, partial(job_queue.put_nowait, panel.step))

    keypad.set_pressed_callback(2, 7, partial(job_queue.put_nowait, panel.set_readwrite_address_from_user_input))
    keypad.set_pressed_callback(2, 6, partial(job_queue.put_nowait, panel.decr_readwrite_address))
    keypad.set_pressed_callback(2, 5, partial(job_queue.put_nowait, panel.incr_readwrite_address))
    keypad.set_pressed_callback(2, 4, partial(job_queue.put_nowait, panel.run))

    keypad.set_pressed_callback(1, 7, partial(job_queue.put_nowait, panel.set_word_from_user_input))
    keypad.set_pressed_callback(1, 6, partial(job_queue.put_nowait, panel.set_word_from_user_input_then_incr_addr))
    keypad.set_pressed_callback(1, 5, partial(job_queue.put_nowait, panel.next_clock_source))
    keypad.set_pressed_callback(1, 4, partial(job_queue.put_nowait, panel.stop))

    keypad.set_pressed_callback(0, 7, partial(job_queue.put_nowait, panel.set_frequency_from_user_input))
    keypad.set_pressed_callback(0, 6, partial(job_queue.put_nowait, panel.next_program))
    keypad.set_pressed_callback(0, 5, partial(job_queue.put_nowait, panel.set_current_program))
    keypad.set_pressed_callback(0, 4, partial(job_queue.put_nowait, partial(panel.set_reset, True)))
    keypad.set_released_callback(0, 4, partial(job_queue.put_nowait, partial(panel.set_reset, False)))

    # Setup asyncio tasks ready to run the Computer
    tasks = []
    tasks.append(asyncio.create_task(run_keypad(keypad)))
    tasks.append(asyncio.create_task(queue_processor(job_queue)))
    tasks.append(asyncio.create_task(pulse()))

    # If connected to WiFi, set up a server and a connection handler
    if connected:
        socket_handler = partial(handle_socket_conn, job_queue, panel)
        server = await asyncio.start_server(
            socket_handler,
            host='0.0.0.0',
            port=8888
        )

    # Run all tasks concurrently
    await asyncio.gather(*tasks)

asyncio.run(main())
