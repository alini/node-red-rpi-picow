import network

# Configure your Wi-Fi credentials
SSID     = 'PeachCastle'
PASSWORD = 'Spit1500!'

wlan     = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID,PASSWORD)

while not wlan.isconnected():
    pass

print('Connected to Wi-Fi')
print(wlan.ifconfig())
