from machine import Pin, SoftI2C
import network
import uasyncio
import ujson

import ssd1306
import creds

# Turn on the internal LED
# It's global because I'm lazy :(
led = Pin("LED", mode=Pin.OUT)
led.on()

hct_pin = Pin(12)
input_pin = Pin(22, mode=Pin.IN, pull=Pin.PULL_DOWN)

def setup_display():
    # Set up display
    i2c = SoftI2C(sda=Pin(20), scl=Pin(21))
    display = ssd1306.SSD1306_I2C(128, 32, i2c)
    display.text('Hello, World!', 0, 0, 1)
    display.show()
    return display

display = setup_display()

def setup_hct245_pins():
    # Set the pins going to the HCT245 as outputs
    for gpio in [12, 13, 14, 15, 16, 17, 18, 19]:
        pin = Pin(gpio, mode=Pin.OUT)
        pin.off()

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to network")
        wlan.connect(creds.SSID, creds.KEY)
        while not wlan.isconnected():
            pass
        
    print("Connected!")
    return wlan.ifconfig()

page = """
<html>
    <head>
        <title>Pi Pico Fun</title>
    </head>
    <body>
        <h1>Light toggler</h1>
        <a href="/toggle"><p>Click to toggle</p></a>
    </body>
</html>
"""

async def handle_http(reader, writer):
    """
    https://github.com/pfalcon/pycopy-lib/blob/master/uasyncio/example_http_server.py
    https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/
    """

    recd_bytes = await reader.read(2048)
    recd_string = recd_bytes.decode("utf8")
    if recd_string.startswith("GET /toggle"):
        led.toggle()
        hct_pin.toggle()
        display.fill(0)
        display.text("Input: " + str(input_pin.value()), 0, 0, 1)
        display.show()
    
        writer.write("HTTP/1.1 200 OK\r\n\r\n")
        writer.write(page)
        writer.write("\r\n")
        await writer.drain()
    
    else:
        writer.write("HTTP/1.1 200 OK\r\n\r\n")
        writer.write("Not found. Go to /toggle")
        writer.write("\r\n")

    writer.close()
    await writer.wait_closed()

async def setup_http_server():
    http_server = await uasyncio.start_server(
        handle_http,
        "0.0.0.0",
        80
    )
    
    num = 1

    while True:
        print("Serving...", num)
        num += 1
        await uasyncio.sleep(10)

async def main():
    setup_hct245_pins()
    ifconfig = connect_to_wifi()
    display.text(ifconfig[0], 0, 8, 1)
    display.show()
    await setup_http_server()



uasyncio.run(main())

