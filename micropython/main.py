"""
Main entry point for Micropython functionality
"""

from machine import Pin
import asyncio
import network
import time
import json

from front_panel import FrontPanel
from display import Display
from keypad import Keypad
from gpiodefs import KEYPAD_GPIOS, KEYPAD_ROW_GPIOS, KEYPAD_COL_GPIOS
import secrets
from queue import Queue

PORT = 8888

def log(msg):
    print(msg)
    # pass

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

def main_old():
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

# asyncio.run(main())








class Manager():
    """
    Manages the front panel and keypad/network inputs
    """

    def __init__(self):
        """
        Initialise the class
        """
        self.socket_connected = False
        self.read_socket = None
        self.write_socket = None
        self.port = 8888
        self.keypad = None
        self.display = Display()
        # self.panel = FrontPanel()
        self.init_keypad()
        self.panel_method_call_queue = Queue()
        self.led_pin = Pin("LED", Pin.OUT)

    def init_keypad(self):
        """
        Initialise the keypad.
        """

        row_pins = [Pin(gpio_num) for gpio_num in KEYPAD_ROW_GPIOS]
        col_pins = [Pin(gpio_num) for gpio_num in KEYPAD_COL_GPIOS]
        self.keypad = Keypad(row_pins, col_pins)
        # Lots of:
        # keypad.set_pressed_callback(...)
        # keypad.set_released_callback(...)
        self.keypad.set_pressed_callback(0, 0, self.press_1)
        self.keypad.set_pressed_callback(0, 1, self.press_2)

    def press_1(self):
        log("1")
        self.display.set_port("1")

    def press_2(self):
        log("2")
        self.display.set_port("2")

    async def pulse(self):
        """
        Blink the onboard LED forever
        """
        
        while True:
            self.led_pin.toggle()
            await asyncio.sleep(0.3)

    async def run(self):
        """
        Run the manager - never returns.
        """

        server = await asyncio.start_server(
            self.handle_connection,
            host='0.0.0.0',
            port=self.port
        )

        tasks = []
        tasks.append(asyncio.create_task(self.run_keypad()))
        tasks.append(asyncio.create_task(self.pulse()))
        # tasks.append(asyncio.create_task(self.run_reader()))
        tasks.append(asyncio.create_task(self.connect_to_wifi()))
        # tasks.append(
        #     asyncio.create_task(self.process_panel_method_queue_forever())
        # )

        # Run all tasks concurrently
        await asyncio.gather(*tasks)

    async def connect_to_wifi(self):
        """
        Connect to the WiFi network.
        """
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(secrets.NETWORK_SSID, secrets.NETWORK_PASSWORD)
        connection_seconds = 10
        for second in range(0, connection_seconds + 1):
            conn_msg = f"Conn {second}/{connection_seconds}s"
            log(conn_msg)
            self.display.set_ip(conn_msg)

            if wlan.isconnected():
                log(f"Connected with IP: {wlan.ifconfig()[0]}")
                self.display.set_ip(wlan.ifconfig()[0])
                break
            else:
                log(f"Status: {self.decode_status(wlan.status())}")
                await asyncio.sleep(1)
        else:
            log(f"Unable to connect to Wifi.")
            self.display.set_ip("No WiFi")

    def decode_status(status):
        """
        Decode the status from a network.WLAN.

        https://docs.micropython.org/en/latest/library/network.WLAN.html#network.WLAN.status

        Args:
            status (?): The statues from the WLAN object
        Return:
            str: The human readable equivalent of the status constant.
        """

        if status == network.STAT_IDLE:
            return "No connection and no activity."
        elif status == network.STAT_CONNECTING:
            return "Connecting in progress."
        elif status == network.STAT_WRONG_PASSWORD:
            return "Failed due to incorrect password."
        elif status == network.STAT_NO_AP_FOUND:
            return "Failed because no access point replied."
        elif status == network.STAT_CONNECT_FAIL:
            return "Failed due to other problems."
        elif status == network.STAT_GOT_IP:
            return "Vonnection successful."
        else:
            return f"Unknown status: {status}"

    async def handle_connection(self, reader, writer):
        """
        Handle a connection to the server.

        Args:
            reader (asyncio.Stream): Reads data from the connection.
            writer (asyncio.Stream): Writes data to the connection.
        """
        if self.socket_connected:
            # Only one connection is allowed
            log(
                "Can only support one connection, closing new connection "
                f"from {writer.get_extra_info('peername')!r}"
            )
            reader.close()
            await reader.wait_closed()
            writer.close()
            await writer.wait_closed()
        else:
            log(f"Got connection from {writer.get_extra_info('peername')!r}")
            self.socket_connected = True
            self.read_socket = reader
            self.write_socket = writer

    async def write(self, data):
        """
        Write data to the connected client.

        Args:
            data (<json serialisable object>): The data to send. This is
                typically a dictionary.
        """

        # Caller should check if the socket is connected, adding here as
        # a safety check
        if self.socket_connected:
            to_send = bytearray(2)
            msg_bytes = bytes(json.dumps(data), "ascii")
            uint16_len_bytes = len(msg_bytes).to_bytes(2, "big")
            to_send.extend(msg_bytes)
            to_send[0] = uint16_len_bytes[0]
            to_send[1] = uint16_len_bytes[1]
            log(f"sending data (len {len(msg_bytes)}) {to_send}")
            self.write_socket.write(to_send)
            await self.write_socket.drain()

    async def process_panel_method_queue_forever(self):
        """
        Process jobs on the panel method call queue forever.

        Jobs on this queue can come from a connected client, or the
        keypad.
        """
        while True:
            display_needs_update = False
            outcome = None
            job_id = None

            call = await self.panel_method_call_queue.get()

            if "job_id" in call:
                # It's a call from the network
                job_id = call["job_id"]
                if "method" not in call:
                    log(
                        "No \"method\" key in network call with job_id "
                        f"{job_id}, skipping."
                    )
                    outcome = Outcome(
                        False,
                        msg="Missing \"method\" key"
                    )
                else:
                    method = getattr(self.panel, call["method"])
                    if method is None:
                        log(
                            f"Panel object has no {call['method']} method"
                            f"in call with job_id {job_id}."
                        )
                        outcome = Outcome(
                            False,
                            msg=f"Panel object has no {call['method']} method."
                        )
                    else:
                        # Call the method with the args and kwargs
                        args = call.get("args", [])
                        kwargs = call.get("kwargs", {})
                        outcome = method(*args, **kwargs)
                        display_needs_update = True
            else:
                # It's a local call
                if "method" not in call:
                    log("No \"method\" key in local call, skipping.")
                else:
                    method = getattr(self.panel, call["method"])
                    if method is None:
                        log(
                            f"Panel object has no {call['method']} method, "
                            "skipping."
                        )
                    else:
                        # Call the method with the args and kwargs
                        args = call.get("args", [])
                        kwargs = call.get("kwargs", {})
                        method(*args, **kwargs)
                        display_needs_update = True

            # Reply back to the calling job that we're done, if necessary
            if outcome is not None:
                await self.reply_to_job(job_id, outcome)

            # Update the local and remote displays, if necessary
            if display_needs_update:
                panel_display_state = self.panel.get_display_state()
                self.display.update_panel_state(panel_display_state)
                await self.update_remote_display_state(panel_display_state)

            # Finish the task, more useful/necessary if we have multiple
            # queue processors - but good practice.
            self.panel_method_call_queue.task_done()

            await asyncio.sleep(0.1)

    async def run_keypad(self):
        """
        Run the keypad
        """
        while True:
            self.keypad.update()
            await asyncio.sleep(0.1)

def main():
    manager = Manager()
    asyncio.run(manager.run())

main()