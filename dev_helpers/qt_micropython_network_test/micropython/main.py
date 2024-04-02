from machine import Pin, I2C
import asyncio
import network
import time

from keypad import Keypad
from gpiodefs import KEYPAD_ROW_GPIOS, KEYPAD_COL_GPIOS, OLED_SDA_GPIO_NO, OLED_SCL_GPIO_NO
import ssd1306
import secrets

# https://github.com/micropython/micropython-lib/blob/master/python-stdlib/functools/functools.py
def partial(func, *args, **kwargs):
    def _partial(*more_args, **more_kwargs):
        kw = kwargs.copy()
        kw.update(more_kwargs)
        return func(*(args + more_args), **kw)

    return _partial

async def main():
    row_pins = [Pin(gpio_num) for gpio_num in KEYPAD_ROW_GPIOS]
    col_pins = [Pin(gpio_num) for gpio_num in KEYPAD_COL_GPIOS]
    keypad = Keypad(row_pins, col_pins)
    keypad.set_pressed_callback(0, 0, partial(display_message, "1"))
    keypad.set_pressed_callback(0, 1, partial(display_message, "2"))
    keypad.set_pressed_callback(0, 2, partial(display_message, "3"))
    keypad.set_pressed_callback(0, 3, partial(display_message, "A"))
    keypad.set_pressed_callback(1, 0, partial(display_message, "4"))
    keypad.set_pressed_callback(1, 1, partial(display_message, "5"))
    keypad.set_pressed_callback(1, 2, partial(display_message, "6"))
    keypad.set_pressed_callback(1, 3, partial(display_message, "B"))
    keypad.set_pressed_callback(2, 0, partial(display_message, "7"))
    keypad.set_pressed_callback(2, 1, partial(display_message, "8"))
    keypad.set_pressed_callback(2, 2, partial(display_message, "9"))
    keypad.set_pressed_callback(2, 3, partial(display_message, "C"))
    keypad.set_pressed_callback(3, 0, partial(display_message, "*"))
    keypad.set_pressed_callback(3, 1, partial(display_message, "0"))
    keypad.set_pressed_callback(3, 2, partial(display_message, "#"))
    keypad.set_pressed_callback(3, 3, partial(display_message, "D"))

    # display = ssd1306.SSD1306_I2C(
    #     128,
    #     64,
    #     I2C(1, sda=Pin(OLED_SDA_GPIO_NO), scl=Pin(OLED_SCL_GPIO_NO))
    # )
    # display.fill(0)
    # display.text("Hello", 0, 0, 1)
    # display.show()

    led_pin = Pin("LED", Pin.OUT)

    tasks = []
    tasks.append(asyncio.create_task(run_keypad(keypad)))
    tasks.append(asyncio.create_task(forever_toggle(led_pin)))
    tasks.append(asyncio.create_task(connect_to_wifi()))

    server = await asyncio.start_server(
        handle_connection,
        host='0.0.0.0',
        port=8888
    )

    # Run all tasks concurrently
    await asyncio.gather(*tasks)


async def handle_connection(reader, writer):

    addr = writer.get_extra_info('peername')
    print(f"Got connection from {addr!r}")
    # print("Waiting 1 second")
    # await asyncio.sleep(1)

    print("Reading 2 bytes")
    data = await reader.read(2)
    message_length = int.from_bytes(data, "big")
    remaining_bytes = message_length 

    print(f"There are {message_length} more bytes to read")

    if message_length == 0:
        print("No more bytes to read, closing")
        # print("Waiting 1 second")
        # await asyncio.sleep(1)

        print("Closing")
        reader.close()
        await reader.wait_closed()
        writer.close()
        await writer.wait_closed()
    else:
        print(f"Reading remaining {message_length} bytes")
        data = await reader.read(message_length)

        message = data.decode("ascii")
        print(f"Received {message!r}")

        display_message(message)

        # print("Waiting 1 second")
        # await asyncio.sleep(1)

        print("Meaasge recieved, closing")
        reader.close()
        await reader.wait_closed()
        writer.close()
        await writer.wait_closed()



async def forever_toggle(pin):
    """
    Togle the state of the passed in pin forever
    """
    
    while True:
        pin.toggle()
        await asyncio.sleep(1)


async def run_keypad(keypad):
    """
    Run the keypad

    Args:
        keypad (Keypad): Keypad object.
    """
    while True:
        keypad.update()
        await asyncio.sleep(0.1)

async def connect_to_wifi():

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.NETWORK_SSID, secrets.NETWORK_PASSWORD)

    max_attempts = 10
    for attempt in range(1, max_attempts + 1):
        conn_msg = f"Conn attmpt {attempt}/{max_attempts}"
        print(conn_msg)
        display_message(conn_msg)
        
        if wlan.isconnected():
            print(f"Connected with IP: {wlan.ifconfig()[0]}")
            break
        else:
            print(f"Status: {decode_status(wlan.status())}")
            await asyncio.sleep(2)

    if wlan.isconnected():
        display_message(wlan.ifconfig()[0])
    else:
        display_message("No WiFi :(")

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

def display_message(msg):
    display.fill(0)
    display.text(msg, 0, 0, 1)
    display.show()

display = ssd1306.SSD1306_I2C(
    128,
    64,
    I2C(1, sda=Pin(OLED_SDA_GPIO_NO), scl=Pin(OLED_SCL_GPIO_NO))
)

asyncio.run(main())