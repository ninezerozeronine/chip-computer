from machine import Pin, I2C
import asyncio
import network
import time
import json

from keypad import Keypad
from gpiodefs import KEYPAD_ROW_GPIOS, KEYPAD_COL_GPIOS, OLED_SDA_GPIO_NO, OLED_SCL_GPIO_NO
import ssd1306
import secrets
from display import Display
from fake_panel import Panel

# https://github.com/micropython/micropython-lib/blob/master/python-stdlib/functools/functools.py
def partial(func, *args, **kwargs):
    def _partial(*more_args, **more_kwargs):
        kw = kwargs.copy()
        kw.update(more_kwargs)
        return func(*(args + more_args), **kw)

    return _partial


class Manager():
    def __init__(self):
        self.last_transmission_recieved = 0
        self.ever_recieved_connection = False
        self.socket_connected = False
        self.read_socket = None
        self.write_socket = None
        self.port = 8888
        self.keypad = None
        #self.led_pin = Pin("LED", Pin.OUT)
        self.display = Display()
        self.panel = Panel()
        self.init_keypad()

    def init_keypad(self):
        row_pins = [Pin(gpio_num) for gpio_num in KEYPAD_ROW_GPIOS]
        col_pins = [Pin(gpio_num) for gpio_num in KEYPAD_COL_GPIOS]
        self.keypad = Keypad(row_pins, col_pins)
        self.keypad.set_pressed_callback(0, 0, partial(self.display.set_port, "1"))
        self.keypad.set_pressed_callback(0, 1, partial(self.display.set_port, "2"))
        self.keypad.set_pressed_callback(0, 2, partial(self.display.set_port, "3"))
        self.keypad.set_pressed_callback(0, 3, partial(self.display.set_port, "A"))
        self.keypad.set_pressed_callback(1, 0, partial(self.display.set_port, "4"))
        self.keypad.set_pressed_callback(1, 1, partial(self.display.set_port, "5"))
        self.keypad.set_pressed_callback(1, 2, partial(self.display.set_port, "6"))
        self.keypad.set_pressed_callback(1, 3, partial(self.display.set_port, "B"))
        self.keypad.set_pressed_callback(2, 0, partial(self.display.set_port, "7"))
        self.keypad.set_pressed_callback(2, 1, partial(self.display.set_port, "8"))
        self.keypad.set_pressed_callback(2, 2, partial(self.display.set_port, "9"))
        self.keypad.set_pressed_callback(2, 3, partial(self.display.set_port, "C"))
        self.keypad.set_pressed_callback(3, 0, partial(self.display.set_port, "*"))
        self.keypad.set_pressed_callback(3, 1, partial(self.display.set_port, "0"))
        self.keypad.set_pressed_callback(3, 2, partial(self.display.set_port, "#"))
        self.keypad.set_pressed_callback(3, 3, partial(self.display.set_port, "D"))

    def display_message(self, message):
        self.display.fill(0)
        self.display.text(message, 0, 0, 1)
        self.display.show()

    async def run(self):
        """

        """
        tasks = []
        tasks.append(asyncio.create_task(self.run_keypad()))
        # tasks.append(asyncio.create_task(self.forever_toggle()))
        tasks.append(asyncio.create_task(self.run_reader()))
        tasks.append(asyncio.create_task(self.connect_to_wifi()))
        # tasks.append(asyncio.create_task(self.check_connection_health()))

        server = await asyncio.start_server(
            self.handle_connection,
            host='0.0.0.0',
            port=self.port
        )

        # Run all tasks concurrently
        await asyncio.gather(*tasks)

    async def run_keypad(self):
        """
        Run the keypad

        """
        while True:
            self.keypad.update()
            await asyncio.sleep(0.1)


    # async def forever_toggle(self):
    #     """
    #     Togle the state of the passed in pin forever
    #     """
        
    #     while True:
    #         self.led_pin.toggle()
    #         await asyncio.sleep(1)


    async def process_panel_method_queue_forever(self):
        while True:
            job = await queue.get()
            if "method" not in job:
                print("No method in job, skipping")
                queue.task_done()
                continue

            method = getattr(self.panel, job["method"])
            if method is None:
                print(f"Panel object has no {job['method']} method.")
                queue.task_done()
                continue

            # Call the method with the args and kwargs
            args = job.get("args", [])
            kwargs = job.get("kwargs", {})
            outcome = method.(*args. **kwargs)

            if "job_id" in job:
                if not isinstance(job["job_id"], int):
                    print(f"Value for 'id' key is not an int. Got: {job['job_id']}")
                else:
                    # Reply back to the calling job that we're done
                    await self.reply_to_job(job_id, outcome)

            # Update all the displays of the panel
            panel_display_state = self.panel.get_display_state()
            self.display.update_panel_state(panel_display_state)
            await self.update_remote_display_state(panel_display_state)

            queue.task_done()

            await asyncio.sleep(0.05)
 




    async def update_remote_display_state(self, panel_display_state):
        data = {
            "purpose": "panel_display_update",
            "body": panel_display_state
        }
        if self.socket_connected:
            await self.write(data)

    async def reply_to_job(self, job_id, outcome):
        data = {
            "purpose": "job_comms",
            "body": outcome.to_dict()
        }
        if self.socket_connected:
            await self.write(data)

    async def run_reader(self):
        while True:
            if self.socket_connected:
                try:
                    socket_data = await self.read_socket.read(2)
                except OSError as e:
                    # The connection died for some reason
                    print("Connection died waiting for read")
                    self.socket_connected = False
                    continue

                if len(socket_data) == 0:
                    print("Tried to read 2 bytes, got none. Connection probably dead")
                    self.socket_connected = False
                    continue

                self.last_transmission_recieved = time.ticks_ms()
                num_data_bytes = int.from_bytes(socket_data, "big")

                if num_data_bytes == 0:
                    print("No more bytes to read, waiting for more data")
                    continue

                try:
                    socket_data = await self.read_socket.read(num_data_bytes)
                except OSError as e:
                    # The connection died for some reason
                    print("Connection died waiting for read")
                    self.socket_connected = False
                    continue

                num_bytes_recieved = len(socket_data)
                if num_bytes_recieved < num_data_bytes:
                    print("Tried to read {num_data_bytes} bytes, got {num_bytes_recieved}. Connection probably dead")
                    self.socket_connected = False
                    continue

                self.last_transmission_recieved = time.ticks_ms()
                data = json.loads(socket_data.decode("ascii"))
                print(f"Recieved: {data}")
                self.display.set_port(data["msg"])


                if not isinstance(data, dict):
                    print(f"Recieved invalid datatype - needs to be a dict. Got: {data}")
                    continue

                if "purpose" not in data:
                    print(f"'purpose' key not in data. Got: {data}")
                    continue

                if data["purpose"] == "panel_method_call":
                    if "job_id" not in data:
                        print(f"'id' key not in data. Got: {data}")
                        continue 

                    if not isinstance(data["job_id"], int):
                        print(f"Value for 'id' key is not an int. Got: {data}")
                        continue

                    self.panel_method_call_queue.put_nowait(data)

                elif data["purpose"] == "test":
                    if "job_id" not in data:
                        print(f"'id' key not in data. Got: {data}")
                        continue

                    if not isinstance(data["job_id"], int):
                        print(f"Value for 'id' key is not an int. Got: {data}")
                        continue

                    if "msg" not in data:
                        print(f"'msg' key not in data. Got: {data}")
                        continue

                    await asyncio.sleep(0.1)

                    ret = {
                        "purpose": "job_comms",
                        "id": data["job_id"],
                        "body": {
                            "type": "completion",
                            "success": True,
                            "message": f"Pico got the {data['msg']} message."
                        }
                    }

                    await self.write(ret)

                else:
                    print(f"Unknown message purpose. Got: {data['purpose']}")
                    continue

            else:
                # Wait for the socket connection to come back online
                await asyncio.sleep(0.5)


    async def check_connection_health(self):
        while True:
            if self.socket_connected and time.ticks_diff(time.ticks_ms(), self.last_transmission_recieved) > 5000:
                print("Too long has passed since last message from client. Closing connection")
                self.socket_connected = False
                if self.read_socket is not None:
                    self.read_socket.close()
                    await self.read_socket.wait_closed()
                if self.write_socket is not None:
                    self.write_socket.close()
                    await self.write_socket.wait_closed()
            await asyncio.sleep(2.5)


    async def handle_connection(self, reader, writer):
        if self.socket_connected:
            # Only one connection is allowed
            print(f"Can only support one connection, closing new connection from {writer.get_extra_info('peername')!r}")
            reader.close()
            await reader.wait_closed()
            writer.close()
            await writer.wait_closed()
        else:
            print(f"Got connection from {writer.get_extra_info('peername')!r}")
            self.socket_connected = True
            self.ever_recieved_connection = True
            self.last_transmission_recieved = time.ticks_ms()
            self.read_socket = reader
            self.write_socket = writer


    async def write(self, data):
        # Caller should check this, adding as a safety check
        if self.socket_connected:
            to_send = bytearray(2)
            msg_bytes = bytes(json.dumps(data), "ascii")
            to_send.extend(msg_bytes)
            uint16_len_bytes = len(msg_bytes).to_bytes(2, "big")
            to_send[0] = uint16_len_bytes[0]
            to_send[1] = uint16_len_bytes[1]
            print("sending data")
            self.write_socket.write(to_send)
            await self.write_socket.drain()


    async def connect_to_wifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(secrets.NETWORK_SSID, secrets.NETWORK_PASSWORD)
        connection_seconds = 10
        for second in range(0, connection_seconds + 1):
            conn_msg = f"Conn {second}/{connection_seconds}s"
            print(conn_msg)
            self.display.set_ip(conn_msg)

            if wlan.isconnected():
                print(f"Connected with IP: {wlan.ifconfig()[0]}")
                self.display.set_ip(wlan.ifconfig()[0])
                break
            else:
                print(f"Status: {decode_status(wlan.status())}")
                await asyncio.sleep(1)
        else:
            print(f"Unable to connect to Wifi.")
            self.display.set_ip("No WiFi")


def decode_status(status):
    if status == network.STAT_IDLE:
        return "no connection and no activity."
    elif status == network.STAT_CONNECTING:
        return "connecting in progress."
    elif status == network.STAT_WRONG_PASSWORD:
        return "failed due to incorrect password."
    elif status == network.STAT_NO_AP_FOUND:
        return "failed because no access point replied."
    elif status == network.STAT_CONNECT_FAIL:
        return "failed due to other problems."
    elif status == network.STAT_GOT_IP:
        return "connection successful."
    else:
        return f"Unknown status: {status}"


manager = Manager()
asyncio.run(manager.run())