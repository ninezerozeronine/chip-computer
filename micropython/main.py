"""
Main entry point for Micropython functionality
"""

from machine import Pin
import asyncio
import network
import time
import json
import gc

from front_panel import FrontPanel
from dummy_panel import DummyPanel
from display import Display
from keypad import Keypad
from socket_connection import SocketConnection
from queue import Queue
from gpiodefs import KEYPAD_GPIOS, KEYPAD_ROW_GPIOS, KEYPAD_COL_GPIOS
from programs import PROGRAMS
from outcome import Outcome
import secrets

PORT = 8888

def log_print(msg):
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
    log_print(f"Got connection from {addr!r}")

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
        self.connection = SocketConnection()
        self.connection.purpose_handlers["panel_method_call"] = self.handle_panel_method_call
        self.connection.connect_callbacks.append(self.init_client)
        self.port = 8888
        self.keypad = None
        self.display = Display()
        self.display.set_connection_ref(self.connection)
        self.panel = FrontPanel()
        self.panel.set_display_ref(self.display)
        self.panel_method_call_queue = Queue()
        self.init_keypad()
        self.led_pin = Pin("LED", Pin.OUT)

    def init_keypad(self):
        """
        Initialise the keypad.
        """

        row_pins = [Pin(gpio_num) for gpio_num in KEYPAD_ROW_GPIOS]
        col_pins = [Pin(gpio_num) for gpio_num in KEYPAD_COL_GPIOS]
        self.keypad = Keypad(row_pins, col_pins)

        self.keypad.set_pressed_callback(3, 3, partial(self.panel_method_call_queue.put_nowait, {"method":"propose_user_input_character", "args":["1"]}))
        self.keypad.set_pressed_callback(3, 2, partial(self.panel_method_call_queue.put_nowait, {"method":"propose_user_input_character", "args":["2"]}))
        self.keypad.set_pressed_callback(3, 1, partial(self.panel_method_call_queue.put_nowait, {"method":"propose_user_input_character", "args":["3"]}))
        self.keypad.set_pressed_callback(2, 3, partial(self.panel_method_call_queue.put_nowait, {"method":"propose_user_input_character", "args":["4"]}))
        self.keypad.set_pressed_callback(2, 2, partial(self.panel_method_call_queue.put_nowait, {"method":"propose_user_input_character", "args":["5"]}))
        self.keypad.set_pressed_callback(2, 1, partial(self.panel_method_call_queue.put_nowait, {"method":"propose_user_input_character", "args":["6"]}))
        self.keypad.set_pressed_callback(1, 3, partial(self.panel_method_call_queue.put_nowait, {"method":"propose_user_input_character", "args":["7"]}))
        self.keypad.set_pressed_callback(1, 2, partial(self.panel_method_call_queue.put_nowait, {"method":"propose_user_input_character", "args":["8"]}))
        self.keypad.set_pressed_callback(1, 1, partial(self.panel_method_call_queue.put_nowait, {"method":"propose_user_input_character", "args":["9"]}))
        self.keypad.set_pressed_callback(0, 3, partial(self.panel_method_call_queue.put_nowait, {"method":"propose_user_input_character", "args":["0"]}))
        self.keypad.set_pressed_callback(0, 2, partial(self.panel_method_call_queue.put_nowait, {"method":"propose_user_input_character", "args":["."]}))

        self.keypad.set_pressed_callback(0, 1, partial(self.panel_method_call_queue.put_nowait, {"method":"delete_last_user_input_char"}))
        self.keypad.set_pressed_callback(0, 0, partial(self.panel_method_call_queue.put_nowait, {"method":"clear_user_input"}))

        self.keypad.set_pressed_callback(3, 6, partial(self.panel_method_call_queue.put_nowait, {"method":"half_steps"}))
        self.keypad.set_pressed_callback(3, 5, partial(self.panel_method_call_queue.put_nowait, {"method":"full_steps"}))
        self.keypad.set_pressed_callback(3, 4, partial(self.panel_method_call_queue.put_nowait, {"method":"set_mode_to_step"}))

        self.keypad.set_pressed_callback(2, 7, partial(self.panel_method_call_queue.put_nowait, {"method":"set_head_from_user_input"}))
        self.keypad.set_pressed_callback(2, 6, partial(self.panel_method_call_queue.put_nowait, {"method":"decr_head"}))
        self.keypad.set_pressed_callback(2, 5, partial(self.panel_method_call_queue.put_nowait, {"method":"incr_head"}))
        self.keypad.set_pressed_callback(2, 4, partial(self.panel_method_call_queue.put_nowait, {"method":"set_mode_to_run"}))

        self.keypad.set_pressed_callback(1, 7, partial(self.panel_method_call_queue.put_nowait, {"method":"set_word_from_user_input"}))
        self.keypad.set_pressed_callback(1, 6, partial(self.panel_method_call_queue.put_nowait, {"method":"set_word_from_user_input_then_incr_head"}))
        self.keypad.set_pressed_callback(1, 5, partial(self.panel_method_call_queue.put_nowait, {"method":"next_clock_source"}))
        self.keypad.set_pressed_callback(1, 4, partial(self.panel_method_call_queue.put_nowait, {"method":"set_mode_to_stop"}))

        self.keypad.set_pressed_callback(0, 7, partial(self.panel_method_call_queue.put_nowait, {"method":"set_frequency_from_user_input"}))
        self.keypad.set_pressed_callback(0, 6, partial(self.panel_method_call_queue.put_nowait, {"method":"next_program"}))
        self.keypad.set_pressed_callback(0, 5, partial(self.panel_method_call_queue.put_nowait, {"method":"load_current_program"}))
        self.keypad.set_pressed_callback(0, 4, partial(self.panel_method_call_queue.put_nowait, {"method":"set_reset", "args":[True]}))
        self.keypad.set_released_callback(0, 4, partial(self.panel_method_call_queue.put_nowait, {"method":"set_reset", "args":[False]}))


    async def init_client(self):
        await self.display.initialise_client()

    def handle_panel_method_call(self, body):
        self.panel_method_call_queue.put_nowait(body)

    async def pulse(self):
        """
        Blink the onboard LED forever
        """
        
        while True:
            self.led_pin.toggle()
            await asyncio.sleep(0.3)

    async def report_mem(self):
        while True:
            print(f"Free mem: {gc.mem_free()}")
            await asyncio.sleep(2)

    async def run(self):
        """
        Run the manager - never returns.
        """

        server = await asyncio.start_server(
            self.connection.handle_connection,
            host='0.0.0.0',
            port=self.port
        )

        tasks = []
        tasks.append(asyncio.create_task(self.panel.initialise()))
        tasks.append(asyncio.create_task(self.run_keypad()))
        tasks.append(asyncio.create_task(self.pulse()))
        tasks.append(asyncio.create_task(self.connection.run_reader()))
        tasks.append(asyncio.create_task(self.connect_to_wifi()))
        tasks.append(
            asyncio.create_task(self.process_panel_method_queue_forever())
        )
        # tasks.append(asyncio.create_task(self.report_mem()))

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
            log_print(conn_msg)
            await self.display.set_ip(conn_msg)

            if wlan.isconnected():
                log_print(f"Connected with IP: {wlan.ifconfig()[0]}")
                await self.display.set_ip(wlan.ifconfig()[0])
                await self.display.set_port(str(self.port))
                break
            else:
                log_print(f"Status: {self.decode_status(wlan.status())}")
                await asyncio.sleep(1)
        else:
            log_print(f"Unable to connect to Wifi.")
            await self.display.set_ip("No WiFi")

    def decode_status(self, status):
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

    async def process_panel_method_queue_forever(self):
        """
        Process jobs on the panel method call queue forever.

        Jobs on this queue can come from a connected client, or the
        keypad.
        """
        while True:

            # display_needs_update = False
            outcome = None
            job_id = None

            call = await self.panel_method_call_queue.get()

            if "job_id" in call:
                # It's a call from the network
                job_id = call["job_id"]
                if "method" not in call:
                    log_print(
                        "No \"method\" key in network call with job_id "
                        f"{job_id}, skipping."
                    )
                    outcome = Outcome(
                        False,
                        message="Missing \"method\" key"
                    )
                else:
                    method = getattr(self.panel, call["method"], None)
                    if method is None:
                        log_print(
                            "Panel object has no {method} method in "
                            "call with job_id {job_id}.".format(
                                method=call["method"],
                                job_id=job_id
                            )
                        )
                        outcome = Outcome(
                            False,
                            message=f"Panel object has no {call['method']} method."
                        )
                    else:
                        # Call the method with the args and kwargs
                        args = call.get("args", [])
                        kwargs = call.get("kwargs", {})
                        outcome = await method(*args, **kwargs)
                        # display_needs_update = True
            else:
                # It's a local call
                if "method" not in call:
                    log_print("No \"method\" key in local call, skipping.")
                else:
                    method = getattr(self.panel, call["method"], None)
                    if method is None:
                        log_print(
                            f"Panel object has no {call['method']} method, "
                            "skipping."
                        )
                    else:
                        # Call the method with the args and kwargs
                        args = call.get("args", [])
                        kwargs = call.get("kwargs", {})
                        await method(*args, **kwargs)
                        # display_needs_update = True

            # Reply back to the calling job that we're done, if necessary
            if outcome is not None:
                await self.reply_to_job(job_id, outcome)

            # Update the local and remote displays, if necessary
            # if display_needs_update:
            #     panel_display_state = self.panel.get_display_state()
            #     self.display.update_panel_state(panel_display_state)
            #     await self.update_remote_display_state(panel_display_state)

            # Finish the task, more useful/necessary if we have multiple
            # queue processors - but good practice.
            self.panel_method_call_queue.task_done()

            await asyncio.sleep(0.1)

    async def reply_to_job(self, job_id, outcome):
        data = {
            "purpose": "job_comms",
            "body": {
                "job_id": job_id,
                "outcome": outcome.to_dict()
            }
        }
        if self.connection.connected:
            await self.connection.write(data)


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