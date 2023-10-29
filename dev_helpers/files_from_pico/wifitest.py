import network

def main():

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to network")
        wlan.connect("foo", "bar")
        # wlan.connect(secrets.NETWORK_SSID, secrets.NETWORK_PASSWORD)
        print("Done!")
        print(wlan.isconnected())
