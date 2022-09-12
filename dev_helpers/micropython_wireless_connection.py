from machine import Pin, SoftI2C
import ssd1306
# import time

led = Pin("LED", Pin.OUT)
led.value(1)
# while True:
#     time.sleep_ms(500)
#     led.toggle()

import network
import uasyncio
import ujson

SSID = "SSID"
KEY = "KEY"


def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to network")
        wlan.connect(SSID, KEY)
        while not wlan.isconnected():
            pass
        
    print("Connected!")
    print(wlan.ifconfig())

async def handle_socket(reader, writer):
    """
    https://github.com/peterhinch/micropython-async/blob/master/v3/as_drivers/client_server/userver.py
    """
    addr = writer.get_extra_info('peername')
    print("Got connection from {addr}".format(addr=addr))

    recd_bytes = await reader.read(100)
    data = ujson.loads(recd_bytes.decode("ascii"))
    
    print("Received {data} from {addr}".format(data=data, addr=addr))

    data["extra"] = "oh hai!"

    print("Sending some data")
    writer.write(ujson.dumps(data).encode("ascii"))
    await writer.drain()

    print("Close the connection")
    writer.close()
    await writer.wait_closed()
    
    led.toggle()

resp = """
<html>
    <head>
         <title>ESP Web Server</title>
         <meta name="viewport" content="width=device-width, initial-scale=1">
         <link rel="icon" href="data:,">
         <style>
             html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
             h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
             border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
             .button2{background-color: #4286f4;}
         </style>
    </head>
    <body>
        <h1>Toggle the light</h1> 
        <p><a href="/"><button class="button">TOGGLE</button></a></p>
    </body>
</html>
"""

html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
.button2{background-color: #4286f4;}</style></head><body> <h1>ESP Web Server</h1> 
<p>GPIO state: <strong>FOO</strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p>
<p><a href="/?led=off"><button class="button button2">OFF</button></a></p></body></html>"""

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
    print("got http connection")

    recd_bytes = await reader.read(2048)
    recd_string = recd_bytes.decode("utf8")
    if recd_string.startswith("GET /toggle"):
        led.toggle()
    
        print(recd_string)

#   writer.write("HTTP/1.0 200 OK\r\n\r\nHello world.\r\n")
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
  
    
    
async def main():
    socket_server = await uasyncio.start_server(
        handle_socket,
        "0.0.0.0",
        8888
    )
    
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

connect()
uasyncio.run(main())

