import asyncio
import network
import secrets

# asyncio.run(...)

async def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.NETWORK_SSID, secrets.NETWORK_PASSWORD)

    max_attempts = 10
    for attempt in range(1, max_attempts + 1):
        conn_msg = f"Conn attmpt {attempt}/{max_attempts}"
        print(conn_msg)
        
        if wlan.isconnected():
            print(f"Connected with IP: {wlan.ifconfig()[0]}")
            return
        else:
            print(f"Status: {decode_status(wlan.status())}")
            await asyncio.sleep(2)

    print("No WiFi :(")


async def send_data(ip, port, message):
    print(f"Opening connection to IP: {ip}, port: {port}")
    reader, writer = await asyncio.open_connection(
        ip,
        port
    )

    # await asyncio.sleep(5)
    to_send = bytearray(2)
    msg_bytes = bytes(message, "ascii")
    to_send.extend(msg_bytes)
    uint16_len_bytes = len(msg_bytes).to_bytes(2, "big")
    to_send[0] = uint16_len_bytes[0]
    to_send[1] = uint16_len_bytes[1]
    print("sending data")
    writer.write(to_send)
    await writer.drain()
    writer.close()
    await writer.wait_closed()
    print("closing writer")